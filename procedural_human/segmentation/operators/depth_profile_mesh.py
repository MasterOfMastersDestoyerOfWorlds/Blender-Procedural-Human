import bpy
from bpy.types import Operator
from bpy.props import IntProperty, BoolProperty, FloatProperty
import numpy as np
from mathutils import Vector, Euler, Matrix
from procedural_human.logger import logger
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.segmentation.operators.mesh_curve_operators import (
    create_dual_loop_mesh, 
    apply_bezier_handles, 
    apply_charrot_gregory_patch_modifier
)
import cv2
from PIL import Image as PILImage
from scipy.ndimage import distance_transform_edt
import skfmm # NEW DEPENDENCY: pip install scikit-fmm
from scipy.ndimage import gaussian_filter # NEW IMPORT

def compute_medialness_speed(mask: np.ndarray, depth_map: np.ndarray, gamma: float = 10.0) -> np.ndarray:
    """
    Constructs the Medialness Field and Speed Map.
    Fuses Boundary Distance (EDT) and Volumetric Depth.
    Ref: Section 4.1 of the Report.
    """
    # 1. Smooth Depth to remove local noise spikes
    depth_smooth = gaussian_filter(depth_map, sigma=2.0)
    
    # 2. Euclidean Distance Transform (EDT) from boundary
    # This keeps the spine away from jagged edges
    if np.any(mask):
        edt = distance_transform_edt(mask)
    else:
        return np.zeros_like(depth_map)

    # 3. Normalize inputs to 0.0 - 1.0 range
    d_max = np.max(depth_smooth)
    e_max = np.max(edt)
    
    d_norm = depth_smooth / d_max if d_max > 0 else depth_smooth
    edt_norm = edt / e_max if e_max > 0 else edt
    
    # 4. Fusion (Medialness M)
    # Average of geometric center (EDT) and volumetric center (Depth)
    M = 0.5 * edt_norm + 0.5 * d_norm
    
    # 5. Potential & Speed Function
    # P(x) = exp(-gamma * M). Speed F = 1/P = exp(gamma * M).
    # We use a masked array so the Fast Marching Method ignores the background.
    speed = np.exp(gamma * M)
    
    return np.ma.masked_array(speed, ~mask)

def extract_geodesic_path(mask: np.ndarray, speed_map: np.ndarray) -> np.ndarray:
    """
    Performs the Double Sweep and Gradient Descent Backtracking.
    Ref: Section 5 and 6.2 of the Report.
    Returns: Nx2 array of (x, y) coordinates for the spine.
    """
    # --- Step 1: Endpoint Detection (Double Sweep) ---
    
    # Seed: Start at the point with maximum medialness (thickest/deepest point)
    seed_idx = np.unravel_index(np.argmax(speed_map), speed_map.shape)
    
    # Sweep 1: Seed -> All Pixels
    # Initialize travel time map with 0 at seed
    phi = np.ones_like(speed_map.data)
    phi[seed_idx] = 0
    # skfmm.travel_time computes geodesic distance on the manifold
    t1 = skfmm.travel_time(np.ma.masked_array(phi, ~mask), speed_map)
    
    if t1 is None: # Safety check for empty/invalid masks
        return np.array([seed_idx[::-1]]) # Return seed as single point (x,y)
        
    # Find Tip: The point furthest from the seed (Geodesic extremum 1)
    # t1 is a masked array, argmax handles the mask automatically
    tip_idx = np.unravel_index(np.argmax(t1), t1.shape)
    
    # Sweep 2: Tip -> All Pixels (The manifold we will backtrack on)
    phi[:] = 1
    phi[tip_idx] = 0
    t2 = skfmm.travel_time(np.ma.masked_array(phi, ~mask), speed_map)
    
    # Find Tail: The point furthest from the Tip (Geodesic extremum 2)
    tail_idx = np.unravel_index(np.argmax(t2), t2.shape)
    
    # --- Step 2: Backtracking (Gradient Descent) ---
    # Trace the path from Tail back to Tip by following the gradient of t2 "downhill"
    
    path = []
    current = np.array(tail_idx, dtype=np.float64)
    tip = np.array(tip_idx, dtype=np.float64)
    
    # Parameters for gradient descent
    step_size = 0.5
    max_steps = int(mask.size) # Prevent infinite loops
    
    path.append(current[::-1]) # Store as (x, y)
    
    for _ in range(max_steps):
        # Integer coordinates for indexing
        r, c = int(current[0]), int(current[1])
        
        # Stop if we are close to the tip (travel time is near zero)
        if t2[r, c] < 1.0 or np.linalg.norm(current - tip) < 1.0:
            break
            
        # Compute local gradient (central differences)
        # Handle boundaries by clamping
        r_min, r_max = max(0, r-1), min(mask.shape[0]-1, r+1)
        c_min, c_max = max(0, c-1), min(mask.shape[1]-1, c+1)
        
        grad_r = (t2[r_max, c] - t2[r_min, c]) / 2.0
        grad_c = (t2[r, c_max] - t2[r, c_min]) / 2.0
        
        grad = np.array([grad_r, grad_c])
        norm = np.linalg.norm(grad)
        
        if norm > 1e-6:
            grad /= norm
        else:
            break # Stuck in flat area
            
        # Move "downhill" (against the gradient of distance)
        current -= grad * step_size
        
        # Boundary check
        current[0] = np.clip(current[0], 0, mask.shape[0]-1)
        current[1] = np.clip(current[1], 0, mask.shape[1]-1)
        
        path.append(current[::-1]) # Append (x, y)
        
    return np.array(path)

def bilinear_sample(image: np.ndarray, x: float, y: float) -> float:
    """
    Bilinear interpolation for sampling image at sub-pixel coordinates.
    
    Args:
        image: 2D image array (H, W)
        x: X coordinate (column, can be fractional)
        y: Y coordinate (row, can be fractional)
        
    Returns:
        Interpolated value at (x, y)
    """
    h, w = image.shape
    # Clamp coordinates to valid range
    x = np.clip(x, 0, w - 1)
    y = np.clip(y, 0, h - 1)
    
    # Get integer coordinates (floor)
    x0, y0 = int(np.floor(x)), int(np.floor(y))
    x1 = min(x0 + 1, w - 1)
    y1 = min(y0 + 1, h - 1)
    
    # Get fractional parts
    fx = x - x0
    fy = y - y0
    
    # Bilinear interpolation
    v00 = image[y0, x0]
    v10 = image[y0, x1]
    v01 = image[y1, x0]
    v11 = image[y1, x1]
    
    v0 = v00 * (1 - fx) + v10 * fx
    v1 = v01 * (1 - fx) + v11 * fx
    v = v0 * (1 - fy) + v1 * fy
    
    return v

def resample_polyline(points: np.ndarray, n: int) -> np.ndarray:
    """
    Resample a polyline to have exactly n points, evenly spaced along the path.
    
    Args:
        points: Nx2 array of (x, y) coordinates
        n: Target number of points
        
    Returns:
        n x 2 array of resampled points
    """
    if len(points) < 2:
        return points
    
    # Compute cumulative distances along the path
    diffs = np.diff(points, axis=0)
    distances = np.sqrt(np.sum(diffs**2, axis=1))
    cumulative = np.concatenate([[0], np.cumsum(distances)])
    total_length = cumulative[-1]
    
    if total_length < 1e-6:
        # Path has zero length, return first point repeated
        return np.tile(points[0], (n, 1))
    
    # Generate evenly spaced parameter values
    t_target = np.linspace(0, total_length, n)
    
    # Interpolate points
    resampled = []
    for t in t_target:
        # Find the segment containing t
        idx = np.searchsorted(cumulative, t, side='right') - 1
        idx = max(0, min(idx, len(points) - 2))
        
        # Interpolate within the segment
        if cumulative[idx + 1] > cumulative[idx]:
            seg_t = (t - cumulative[idx]) / (cumulative[idx + 1] - cumulative[idx])
        else:
            seg_t = 0.0
        
        p0 = points[idx]
        p1 = points[idx + 1]
        p = p0 + seg_t * (p1 - p0)
        resampled.append(p)
    
    return np.array(resampled)

def create_spine_contour_from_depth(
    mask: np.ndarray,
    depth_map: np.ndarray,
    image_width: int,
    image_height: int,
    num_points: int = 32
) -> np.ndarray:
    """
    Create a side profile (spine) contour using Geodesic Pathfinding.
    
    Replaces row-scanning with Global Geodesic Extraction to find the 
    true ridge of the object, then projects it to the Y-axis for profile generation.
    """
    # Resize depth map to match mask if needed
    if depth_map.shape != mask.shape:
        depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
        depth_pil = depth_pil.resize((mask.shape[1], mask.shape[0]), PILImage.BILINEAR)
        depth_map = np.array(depth_pil).astype(np.float32) / 255.0
    
    # --- Geodesic Spine Extraction ---
    try:
        # 1. Compute Medialness Speed Map
        speed_map = compute_medialness_speed(mask, depth_map)
        
        # 2. Extract the Geodesic Ridge (list of x,y coordinates)
        spine_path_xy = extract_geodesic_path(mask, speed_map)
        
    except (ImportError, Exception) as e:
        logger.warning(f"Geodesic extraction failed ({e}), falling back to simple center.")
        # Fallback: create a dummy vertical line down the middle
        y_indices = np.where(np.any(mask, axis=1))[0]
        if len(y_indices) > 0:
            spine_path_xy = np.column_stack([
                np.full(len(y_indices), mask.shape[1]/2), 
                y_indices
            ])
        else:
            return np.column_stack([np.zeros(num_points), np.linspace(-0.5, 0.5, num_points)])

    if len(spine_path_xy) < 2:
         return np.column_stack([np.zeros(num_points), np.linspace(-0.5, 0.5, num_points)])

    # --- Sample Data along the Spine ---
    # We now have the TRUE ridge. We sample depth along this ridge.
    
    # Map coordinates to integers for sampling
    sample_x = np.clip(spine_path_xy[:, 0], 0, mask.shape[1]-1).astype(int)
    sample_y = np.clip(spine_path_xy[:, 1], 0, mask.shape[0]-1).astype(int)
    
    sampled_depths = depth_map[sample_y, sample_x]
    
    # --- Projection and Normalization ---
    # The mesh generator expects [Z, Y] where Y is the vertical coordinate.
    # We project our geodesic spine points onto the Y-axis.
    
    y_min, y_max = np.min(sample_y), np.max(sample_y)
    mask_height = max(1.0, y_max - y_min)
    mask_center_y = (y_max + y_min) / 2.0
    
    # Normalize Y to Blender coords [-0.5, 0.5] (Up is positive)
    # Image Y is down, so we flip signs.
    y_normalized = -(sample_y - mask_center_y) / mask_height
    
    # Sort data by Y to ensure the contour is monotonic for the mesh generator
    # (Note: This "straightens" curved spines into a vertical profile, 
    # which is required if the target mesh is a straight extrusion)
    sort_idx = np.argsort(y_normalized)
    y_sorted = y_normalized[sort_idx]
    depth_sorted = sampled_depths[sort_idx]
    
    # Remove duplicates in Y for interpolation
    unique_y, unique_indices = np.unique(y_sorted, return_index=True)
    unique_depths = depth_sorted[unique_indices]
    
    if len(unique_y) < 2:
         return np.column_stack([np.zeros(num_points), np.linspace(-0.5, 0.5, num_points)])

    # Interpolate to requested num_points
    y_target = np.linspace(unique_y[0], unique_y[-1], num_points)
    depth_interp = np.interp(y_target, unique_y, unique_depths)
    
    # Normalize depth (Local Contrast)
    d_min = depth_interp.min()
    d_max = depth_interp.max()
    if d_max > d_min:
        width_factor = (depth_interp - d_min) / (d_max - d_min)
    else:
        width_factor = np.full_like(depth_interp, 0.5)
        
    # --- Construct Output Contour ---
    contour_points = []
    
    # Right side (+Z)
    for i in range(num_points):
        contour_points.append([width_factor[i] * 0.5, y_target[i]])
        
    # Left side (-Z)
    for i in range(num_points - 1, -1, -1):
        contour_points.append([-width_factor[i] * 0.5, y_target[i]])
        
    return np.array(contour_points)


@procedural_operator
class CreateDepthProfileMeshOperator(Operator):
    """Create a mesh from segmentation mask and depth map, aligned to camera"""
    
    bl_idname = "segmentation.create_depth_profile_mesh"
    bl_label = "Create Depth Profile Mesh"
    bl_description = "Create mesh from mask and depth map, aligned to main camera with Charrot-Gregory patch"
    bl_options = {'REGISTER', 'UNDO'}
    
    points_per_half: IntProperty(
        name="Points per Half",
        description="Number of vertices per half-loop (excluding shared vertices)",
        default=16,
        min=4,
        max=64
    )
    
    subdivisions: IntProperty(
        name="Patch Subdivisions",
        description="Subdivisions for Charrot-Gregory patch surface",
        default=4,
        min=1,
        max=8
    )
    
    merge_by_distance: BoolProperty(
        name="Merge By Distance",
        description="Merge vertices at patch boundaries for smooth surface",
        default=True
    )
    
    depth_scale: FloatProperty(
        name="Depth Scale",
        description="Scale factor for depth-based thickness",
        default=1.0,
        min=0.1,
        max=5.0
    )
    
    def execute(self, context):
        from procedural_human.segmentation.operators.segmentation_operators import (
            get_current_masks, get_active_image, get_current_depth_map
        )
        from procedural_human.segmentation.mask_to_curve import find_contours
        
        # Get camera
        camera = context.scene.camera
        if camera is None:
            self.report({'WARNING'}, "No camera found in scene. Please set a camera as active.")
            return {'CANCELLED'}
        
        # Get mask
        masks = get_current_masks()
        if not masks:
            self.report({'WARNING'}, "No segmentation masks available. Run segmentation first.")
            return {'CANCELLED'}
        
        # Use first enabled mask or first mask
        settings = context.scene.segmentation_mask_settings
        mask_index = 0
        if len(settings.masks) > 0:
            enabled_indices = [item.mask_index for item in settings.masks if item.enabled and item.mask_index >= 0]
            if enabled_indices:
                mask_index = enabled_indices[0]
        
        if mask_index >= len(masks):
            mask_index = 0
        
        mask = masks[mask_index]
        
        # Get depth map
        depth_map = get_current_depth_map()
        if depth_map is None:
            self.report({'WARNING'}, "No depth map available. Run depth estimation first.")
            return {'CANCELLED'}
        
        # Get image dimensions
        image = get_active_image(context)
        if image:
            image_width, image_height = image.size
        else:
            image_height, image_width = mask.shape[:2]
        
        try:
            # Create front contour from mask
            contours = find_contours(mask)
            if not contours:
                self.report({'WARNING'}, "Could not extract contour from mask")
                return {'CANCELLED'}
            
            # Use largest contour
            front_contour = max(contours, key=len)
            
            # Calculate Visual Center using Distance Transform for better alignment
            # This ensures the "spine" aligns with the thickest part of the object
            try:
                dist = distance_transform_edt(mask)
                max_idx = np.argmax(dist)
                max_y, max_x = np.unravel_index(max_idx, dist.shape)
                center_x, center_y = float(max_x), float(max_y)
                # logger.info(f"Using visual center at ({center_x}, {center_y})")
            except ImportError:
                # Fallback to centroid
                M = cv2.moments(mask.astype(np.uint8)) if 'cv2' in locals() else None
                if M and M["m00"] != 0:
                    center_x = M["m10"] / M["m00"]
                    center_y = M["m01"] / M["m00"]
                else:
                    # Bounding box center
                    y_indices, x_indices = np.where(mask)
                    center_x = (np.min(x_indices) + np.max(x_indices)) / 2
                    center_y = (np.min(y_indices) + np.max(y_indices)) / 2
            
            # Normalize front contour to image coordinates centered on visual center
            front_contour_norm = front_contour.astype(np.float32).copy()
            
            # Normalize to 0-1 then center around visual center
            # Image coords: X=0..W, Y=0..H (down)
            # Blender coords: X=-0.5..0.5, Y=-0.5..0.5 (up)
            
            # Shift points so that (center_x, center_y) becomes (0,0)
            front_contour_norm[:, 0] = (front_contour_norm[:, 0] - center_x) / image_width
            
            # Flip Y and center
            # Image Y is down, Blender Y is up.
            # (y - center_y) / height -> if y > center (lower in image), result > 0.
            # We want y > center (lower image) -> y < 0 (lower blender).
            # So -(y - center_y) / height
            front_contour_norm[:, 1] = -(front_contour_norm[:, 1] - center_y) / image_height
            
            # Determine Z-depth and Positioning
            # Calculate mean depth value in the mask to handle layering (0=far, 1=close)
            # Mask depth values
            # Resize depth map to match mask if needed before indexing
            if depth_map.shape != mask.shape:
                depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
                depth_pil = depth_pil.resize((mask.shape[1], mask.shape[0]), PILImage.BILINEAR)
                depth_map_resized = np.array(depth_pil).astype(np.float32) / 255.0
                mask_depths = depth_map_resized[mask]
            else:
                mask_depths = depth_map[mask]
            
            if len(mask_depths) > 0:
                mean_depth_val = np.mean(mask_depths)
            else:
                mean_depth_val = 0.5
                
            # Define depth range for layering
            # Close objects (val ~1) should be closer to camera
            # Far objects (val ~0) should be further
            base_distance = 5.0
            depth_layering_range = 2.0  # Objects spread over 2 meters depth
            
            # Higher depth value = Closer = Smaller distance
            # distance = base - (val - 0.5) * range
            object_distance = base_distance - (mean_depth_val - 0.5) * depth_layering_range
            
            # Unproject visual center to 3D view plane
            # We assume the "center" of our mesh (0,0,0) should align with the ray through (center_x, center_y)
            
            # Camera parameters (approximated if not available)
            # Sensor width in mm, focal length in mm
            sensor_width = camera.data.sensor_width
            focal_length = camera.data.lens
            
            # Normalized coordinates of center (-0.5 to 0.5)
            # Account for aspect ratio if render settings available, otherwise assume square pixels
            render = context.scene.render
            aspect_ratio = render.resolution_x / render.resolution_y
            
            norm_cx = (center_x / image_width) - 0.5
            norm_cy = 0.5 - (center_y / image_height)  # Blender Y is up
            
            # Calculate view plane offsets at object_distance
            # tan(theta/2) = (sensor/2) / focal
            # view_width = 2 * distance * tan(theta/2) = distance * sensor / focal
            view_plane_width = object_distance * sensor_width / focal_length
            view_plane_height = view_plane_width / aspect_ratio
            
            offset_x = norm_cx * view_plane_width
            offset_y = norm_cy * view_plane_height
            
            # Create spine contour from depth map
            # Use the improved function that uses distance transform and local contrast
            spine_contour = create_spine_contour_from_depth(
                mask,
                depth_map,
                image_width,
                image_height,
                num_points=self.points_per_half * 2 + 2
            )
            
            # Apply depth scale
            # Spine X is Z-thickness.
            spine_contour[:, 0] *= self.depth_scale
            
            # Create the mesh
            obj = create_dual_loop_mesh(
                front_contour_norm,
                spine_contour,
                name=f"DepthMesh_{mask_index}",
                points_per_half=self.points_per_half,
            )
            
            # Scale the mesh to match view plane size
            # front_contour_norm is normalized to image dimensions (roughly -0.5 to 0.5)
            # We need to scale it up to physical dimensions at that distance
            obj.scale.x = view_plane_width
            obj.scale.y = view_plane_height  # Assuming normalized Y was also scaled by image height ratio?
            # Wait, front_contour_norm was divided by image_width/height separately.
            # So X units are fractions of width, Y units are fractions of height.
            # So scaling X by view_width and Y by view_height is correct.
            obj.scale.z = view_plane_width # Scale thickness proportionally to width? 
            # Or assume depth_scale handled it. Let's keep Z scale same as X for consistency.
            
            logger.info(f"Created depth profile mesh: {obj.name} at dist {object_distance:.2f}")
            
            # Apply Bezier handles
            try:
                apply_bezier_handles(obj)
            except Exception as e:
                logger.warning(f"Could not apply Bezier handles: {e}")
            
            # Apply Charrot-Gregory patch modifier
            try:
                apply_charrot_gregory_patch_modifier(
                    obj,
                    self.subdivisions,
                    self.merge_by_distance
                )
            except Exception as e:
                logger.warning(f"Could not apply Charrot-Gregory patch: {e}")
            
            # Transform mesh to align with camera
            # Get camera matrix
            camera_matrix = camera.matrix_world
            camera_location = camera_matrix.translation
            camera_rotation = camera_matrix.to_euler()
            
            # Calculate world position
            # Start at camera
            # Move forward (-Z local) by object_distance
            # Move right (+X local) by offset_x
            # Move up (+Y local) by offset_y
            
            # Get camera local axes
            cam_rot_mat = camera_rotation.to_matrix()
            cam_right = cam_rot_mat.col[0] # X
            cam_up = cam_rot_mat.col[1]    # Y
            cam_back = cam_rot_mat.col[2]  # Z
            
            target_location = camera_location - cam_back * object_distance + cam_right * offset_x + cam_up * offset_y
            
            # Set mesh location
            obj.location = target_location
            
            # Rotate to face camera (billboard)
            # Mesh "Front" is +Z? No, our contours are in XY plane.
            # create_dual_loop_mesh creates in XY.
            # We want Mesh XY plane to be parallel to Camera XY plane.
            # So Mesh Rotation = Camera Rotation.
            obj.rotation_euler = camera_rotation
            
            # Select the new object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            self.report({'INFO'}, f"Created depth profile mesh: {obj.name}")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to create depth profile mesh: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Failed: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "points_per_half")
        layout.prop(self, "depth_scale")
        layout.separator()
        layout.prop(self, "subdivisions")
        layout.prop(self, "merge_by_distance")
