import bpy
from bpy.types import Operator
from bpy.props import IntProperty, BoolProperty, FloatProperty
import numpy as np
from mathutils import Vector
from procedural_human.logger import logger
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.segmentation.operators.mesh_curve_operators import create_dual_loop_mesh, apply_bezier_handles, apply_charrot_gregory_patch_modifier
# from procedural_human.segmentation.operators.segmentation_operators import create_spine_contour_from_depth
from mathutils import Euler



def create_spine_contour_from_depth(
    mask: np.ndarray,
    depth_map: np.ndarray,
    image_width: int,
    image_height: int,
    num_points: int = 32
) -> np.ndarray:
    """
    Create a side profile (spine) contour from a mask and depth map.
    
    The spine is created by:
    1. Finding the vertical centerline of the mask
    2. Sampling depth values along this centerline
    3. Creating a symmetric two-sided profile (width proportional to depth)
    
    Args:
        mask: Boolean mask array (H, W)
        depth_map: Depth map array (H, W) normalized 0-1
        image_width: Width of the source image
        image_height: Height of the source image
        num_points: Number of points in the output contour
        
    Returns:
        Nx2 array of contour points in side view plane (X=Z, Y=Y)
    """
    # Resize depth map to match mask if needed
    if depth_map.shape != mask.shape:
        from PIL import Image as PILImage
        depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
        depth_pil = depth_pil.resize((mask.shape[1], mask.shape[0]), PILImage.BILINEAR)
        depth_map = np.array(depth_pil).astype(np.float32) / 255.0
    
    # Find vertical centerline of mask
    # For each row, find the center X coordinate of the mask
    rows_with_mask = []
    centerline_x = []
    centerline_depths = []
    
    for y in range(mask.shape[0]):
        row_mask = mask[y, :]
        if np.any(row_mask):
            # Find left and right edges
            mask_indices = np.where(row_mask)[0]
            if len(mask_indices) > 0:
                left = mask_indices[0]
                right = mask_indices[-1]
                center_x = (left + right) / 2.0
                rows_with_mask.append(y)
                centerline_x.append(center_x)
                
                # Sample depth at centerline (average over a small region)
                sample_width = max(1, int((right - left) * 0.1))
                sample_left = max(0, int(center_x - sample_width // 2))
                sample_right = min(mask.shape[1], int(center_x + sample_width // 2))
                depth_sample = np.mean(depth_map[y, sample_left:sample_right])
                centerline_depths.append(depth_sample)
    
    if len(rows_with_mask) < 2:
        logger.warning("Not enough mask rows for spine contour")
        # Return a simple default contour
        y_coords = np.linspace(-0.5, 0.5, num_points)
        x_coords = np.zeros_like(y_coords) * 0.1  # Default width
        return np.column_stack([x_coords, y_coords])
    
    # Normalize Y coordinates to [-0.5, 0.5]
    rows_array = np.array(rows_with_mask, dtype=np.float32)
    y_normalized = (rows_array / image_height) - 0.5
    y_normalized = -y_normalized  # Flip Y to match Blender coordinates
    
    # Interpolate to get evenly spaced Y values
    y_target = np.linspace(y_normalized.min(), y_normalized.max(), num_points)
    
    # Interpolate centerline X and depths
    centerline_x_array = np.array(centerline_x, dtype=np.float32)
    centerline_depths_array = np.array(centerline_depths, dtype=np.float32)
    
    # Normalize X to image coordinates (0-1 range, then center)
    centerline_x_normalized = (centerline_x_array / image_width) - 0.5
    
    # Interpolate
    x_interp = np.interp(y_target, y_normalized, centerline_x_normalized)
    depth_interp = np.interp(y_target, y_normalized, centerline_depths_array)
    
    # Create symmetric two-sided profile
    # Width is proportional to depth (deeper = wider)
    # Scale depth to reasonable width (0.05 to 0.3 of image width)
    depth_min = depth_interp.min()
    depth_max = depth_interp.max()
    if depth_max > depth_min:
        depth_normalized = (depth_interp - depth_min) / (depth_max - depth_min)
    else:
        depth_normalized = np.ones_like(depth_interp) * 0.5
    
    # Width ranges from 0.05 to 0.3 (as fraction of image width)
    width_factor = 0.05 + depth_normalized * 0.25
    
    # Create symmetric profile: left side (negative X) and right side (positive X)
    # In side view, X becomes Z (depth), so we create a symmetric shape
    contour_points = []
    
    # Right side (positive Z/X)
    for i in range(num_points):
        z = width_factor[i] * 0.5  # Half width on right side
        y = y_target[i]
        contour_points.append([z, y])
    
    # Left side (negative Z/X) - reverse order
    for i in range(num_points - 1, -1, -1):
        z = -width_factor[i] * 0.5  # Half width on left side
        y = y_target[i]
        contour_points.append([z, y])
    
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
            
            # Normalize front contour to image coordinates
            front_contour_norm = front_contour.astype(np.float32).copy()
            front_contour_norm[:, 0] = (front_contour_norm[:, 0] / image_width) - 0.5
            front_contour_norm[:, 1] = (front_contour_norm[:, 1] / image_height) - 0.5
            front_contour_norm[:, 1] = -front_contour_norm[:, 1]  # Flip Y
            
            # Center the front contour
            centroid = front_contour_norm.mean(axis=0)
            front_contour_norm -= centroid
            
            # Create spine contour from depth map
            spine_contour = create_spine_contour_from_depth(
                mask,
                depth_map,
                image_width,
                image_height,
                num_points=self.points_per_half * 2 + 2
            )
            
            # Apply depth scale
            spine_contour[:, 0] *= self.depth_scale
            
            # Create the mesh
            obj = create_dual_loop_mesh(
                front_contour_norm,
                spine_contour,
                name="DepthProfileMesh",
                points_per_half=self.points_per_half,
            )
            
            logger.info(f"Created depth profile mesh: {obj.name}")
            
            # Apply Bezier handles
            try:
                apply_bezier_handles(obj)
                logger.info("Applied Bezier handles")
            except Exception as e:
                logger.warning(f"Could not apply Bezier handles: {e}")
            
            # Apply Charrot-Gregory patch modifier
            try:
                apply_charrot_gregory_patch_modifier(
                    obj,
                    self.subdivisions,
                    self.merge_by_distance
                )
                logger.info(f"Applied Charrot-Gregory patch modifier (subdivisions={self.subdivisions})")
            except Exception as e:
                logger.warning(f"Could not apply Charrot-Gregory patch: {e}")
            
            # Transform mesh to align with camera
            # Get camera matrix
            camera_matrix = camera.matrix_world
            camera_location = camera_matrix.translation
            camera_rotation = camera_matrix.to_euler()
            
            # Calculate mesh bounding box to determine scale
            bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
            bbox_center = sum(bbox, Vector()) / len(bbox)
            bbox_size = max(
                (max(v.x for v in bbox) - min(v.x for v in bbox)),
                (max(v.y for v in bbox) - min(v.y for v in bbox)),
                (max(v.z for v in bbox) - min(v.z for v in bbox))
            )
            
            # Position mesh in front of camera
            # Camera looks down -Z in Blender, so position mesh along -Z from camera
            camera_forward = camera_matrix.to_quaternion() @ Vector((0, 0, -1))
            mesh_distance = 5.0  # Distance from camera
            target_location = camera_location + camera_forward * mesh_distance
            
            # Set mesh location and rotation to match camera view
            obj.location = target_location
            # Rotate to face camera (inverse of camera rotation)
            obj.rotation_euler = camera_rotation
            # Additional 90-degree rotation around X to align properly
            obj.rotation_euler.rotate(Euler((np.pi / 2, 0, 0), 'XYZ'))
            
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