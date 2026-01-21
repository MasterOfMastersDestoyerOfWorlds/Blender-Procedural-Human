import bpy
import bmesh
import numpy as np
import cv2
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, BoolProperty
from scipy.ndimage import gaussian_filter

from procedural_human.logger import logger
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.segmentation.operators.mesh_curve_operators import (
    apply_bezier_handles,
    apply_charrot_gregory_patch_modifier
)
from procedural_human.segmentation.operators.segmentation_utils import (
    simplify_polyline,
    bilinear_sample
)
from procedural_human.segmentation.operators.segmentation_operators import (
    get_current_masks,
    get_active_image,
    get_current_depth_map,
    set_current_hessian_map,
    set_current_ridge_curves
)


def compute_hessian_ridge_map(depth_map: np.ndarray, mask: np.ndarray, sigma: float = 2.0) -> tuple:
    """
    Compute Hessian matrix and extract ridge strength map.
    Returns: (ridge_strength, direction_field)
    
    Ref: Section 2.3 of the Report.
    """
    # 1. Gaussian smooth at scale sigma
    # Use mode='nearest' to avoid boundary artifacts
    depth_smooth = gaussian_filter(depth_map, sigma=sigma, mode='nearest')
    
    # 2. Compute gradients (First derivatives)
    dz_dy, dz_dx = np.gradient(depth_smooth)
    
    # 3. Compute Hessian components (Second derivatives)
    d2z_dy2, d2z_dxdy = np.gradient(dz_dy)
    d2z_dydx, d2z_dx2 = np.gradient(dz_dx)
    
    # 4. Eigenvalue decomposition
    # H = [[Hxx, Hxy], [Hxy, Hyy]]
    # Trace = Hxx + Hyy = lambda1 + lambda2
    # Det = Hxx*Hyy - Hxy*Hxy = lambda1 * lambda2
    # discriminant = sqrt(Trace^2 - 4*Det) = |lambda1 - lambda2|
    
    Hxx = d2z_dx2
    Hxy = d2z_dxdy
    Hyy = d2z_dy2
    
    trace = Hxx + Hyy
    det = Hxx * Hyy - Hxy * Hxy
    
    # Careful with sqrt of negative numbers (shouldn't happen for symmetric real matrices theoretically, but float precision)
    discriminant = np.sqrt(np.maximum(0, trace**2 - 4 * det))
    
    # Eigenvalues
    # lambda1 is the one with larger magnitude (or we sort them)
    # Here we calculate them directly
    l1 = (trace + discriminant) / 2
    l2 = (trace - discriminant) / 2
    
    # We want the eigenvalue with larger ABSOLUTE value to be lambda1 (max curvature)
    # Sort by magnitude
    abs_l1 = np.abs(l1)
    abs_l2 = np.abs(l2)
    
    lambda1 = np.where(abs_l1 > abs_l2, l1, l2)
    lambda2 = np.where(abs_l1 > abs_l2, l2, l1)
    
    # Ridge strength: We want high NEGATIVE curvature (convex ridge)
    # Valleys would be high POSITIVE curvature.
    # We invert the sign so that ridges are positive values in our strength map
    ridge_strength = -lambda1
    
    # Filter out valleys (where lambda1 > 0)
    ridge_strength = np.maximum(0, ridge_strength)
    
    # Mask out background
    if mask is not None:
        ridge_strength = ridge_strength * mask
        
    # Normalize for visualization
    r_max = np.max(ridge_strength)
    if r_max > 0:
        ridge_strength /= r_max
        
    return ridge_strength, None  # Direction field not implemented/needed yet


def zhang_suen_thinning(binary_image: np.ndarray) -> np.ndarray:
    """
    Perform Zhang-Suen thinning algorithm for skeletonization.
    """
    # Ensure binary 0/1
    img = binary_image.astype(np.uint8)
    if img.max() > 1:
        img = (img > 0).astype(np.uint8)
        
    # Standard thinning implementation
    # Using OpenCV if available, or manual implementation
    try:
        # OpenCV ximgproc thinning is faster but requires opencv-contrib-python
        return cv2.ximgproc.thinning(img * 255, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN) > 0
    except (AttributeError, ImportError):
        pass
        
    # Manual implementation as fallback
    skeleton = img.copy()
    
    # Kernel for neighbor processing
    # P9 P2 P3
    # P8 P1 P4
    # P7 P6 P5
    
    def iteration(im, iter_num):
        marker = np.zeros_like(im)
        rows, cols = im.shape
        for r in range(1, rows-1):
            for c in range(1, cols-1):
                if im[r, c] == 0:
                    continue
                
                # Get 8-neighbors
                p2 = im[r-1, c]
                p3 = im[r-1, c+1]
                p4 = im[r, c+1]
                p5 = im[r+1, c+1]
                p6 = im[r+1, c]
                p7 = im[r+1, c-1]
                p8 = im[r, c-1]
                p9 = im[r-1, c-1]
                
                neighbors = [p2, p3, p4, p5, p6, p7, p8, p9]
                
                # Condition A: Number of non-zero neighbors B(P1) is between 2 and 6
                B = sum(neighbors)
                if B < 2 or B > 6:
                    continue
                
                # Condition B: Number of 0->1 transitions A(P1) is 1
                # Sequence: p2, p3, p4, p5, p6, p7, p8, p9, p2
                transitions = 0
                seq = neighbors + [p2]
                for k in range(8):
                    if seq[k] == 0 and seq[k+1] == 1:
                        transitions += 1
                if transitions != 1:
                    continue
                
                # Condition C & D
                if iter_num == 0:
                    if (p2 * p4 * p6) == 0 and (p4 * p6 * p8) == 0:
                        marker[r, c] = 1
                else:
                    if (p2 * p4 * p8) == 0 and (p2 * p6 * p8) == 0:
                        marker[r, c] = 1
                        
        return im & ~marker
        
    prev = np.zeros_like(skeleton)
    while not np.array_equal(skeleton, prev):
        prev = skeleton.copy()
        skeleton = iteration(skeleton, 0)
        skeleton = iteration(skeleton, 1)
        
    return skeleton


def skeletonize_ridge_map(ridge_map: np.ndarray, mask: np.ndarray, threshold: float = 0.3) -> np.ndarray:
    """
    Threshold and skeletonize the ridge strength map.
    Returns: binary skeleton image
    """
    # 1. Thresholding
    binary_ridge = ridge_map > threshold
    
    # Apply mask
    if mask is not None:
        binary_ridge = binary_ridge & mask
    
    # 2. Thinning / Skeletonization
    try:
        from skimage.morphology import skeletonize
        skeleton = skeletonize(binary_ridge)
    except ImportError:
        # Fallback to custom Zhang-Suen implementation
        skeleton = zhang_suen_thinning(binary_ridge)
        
    return skeleton


def vectorize_skeleton(skeleton: np.ndarray, mask: np.ndarray, simplify_amount: float = 0.01) -> list:
    """
    Convert pixel skeleton to list of polyline curves.
    
    Args:
        skeleton: Binary skeleton image
        mask: Segmentation mask (to check boundaries)
        simplify_amount: RDP epsilon
        
    Returns:
        List of Nx2 arrays (curves)
    """
    # Find all skeleton pixels
    points = np.column_stack(np.where(skeleton > 0))
    
    if len(points) == 0:
        return []
    
    # Build graph from skeleton pixels
    # Map pixel coords to index
    pmap = {tuple(p): i for i, p in enumerate(points)}
    adj = {i: [] for i in range(len(points))}
    
    rows, cols = skeleton.shape
    
    # Connect neighbors
    for i, (r, c) in enumerate(points):
        # Check 8-neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if skeleton[nr, nc] > 0:
                        neighbor_idx = pmap.get((nr, nc))
                        if neighbor_idx is not None and neighbor_idx > i: # Avoid duplicates
                            adj[i].append(neighbor_idx)
                            adj[neighbor_idx].append(i)
    
    # Find endpoints and junctions
    # Degree 1 = Endpoint
    # Degree 2 = Path node
    # Degree > 2 = Junction
    degrees = {i: len(neighbors) for i, neighbors in adj.items()}
    
    junctions = [i for i, d in degrees.items() if d > 2]
    endpoints = [i for i, d in degrees.items() if d == 1]
    
    # Start tracing from junctions and endpoints
    visited_edges = set() # Set of frozenset({u, v})
    curves = []
    
    # Nodes to start tracing from (junctions first, then endpoints)
    start_nodes = junctions + endpoints
    
    # If a closed loop exists without endpoints/junctions, we need to handle it too
    # But for now let's assume ridges end somewhere
    
    for start_node in start_nodes:
        # Trace all unvisited edges connected to this node
        for neighbor in adj[start_node]:
            edge = frozenset({start_node, neighbor})
            if edge in visited_edges:
                continue
            
            # Start a new curve
            path = [start_node, neighbor]
            visited_edges.add(edge)
            
            # Continue traversing
            curr = neighbor
            prev = start_node
            
            while True:
                # If current node is a junction or endpoint, stop
                if degrees[curr] != 2:
                    break
                    
                # Find next neighbor (that isn't prev)
                next_node = None
                for n in adj[curr]:
                    if n != prev:
                        next_node = n
                        break
                
                if next_node is None: # Should not happen for degree 2
                    break
                    
                edge = frozenset({curr, next_node})
                if edge in visited_edges: # Loop detected
                    break
                    
                path.append(next_node)
                visited_edges.add(edge)
                prev = curr
                curr = next_node
            
            # Convert indices back to coordinates
            # path is list of indices
            curve_coords = points[path] # Nx2 array of (row, col)
            
            # Store as (x, y) = (col, row)
            curve_xy = np.column_stack([curve_coords[:, 1], curve_coords[:, 0]])
            
            # Simplify
            if simplify_amount > 0:
                curve_xy = simplify_polyline(curve_xy, simplify_amount)
                
            curves.append(curve_xy)
            
    # Handle isolated loops (if any remain unvisited)
    # Simple sweep over all points
    # (Omitted for brevity, assuming ridges connect to boundaries or fade out)
    
    return curves


def create_ridge_mesh(curves: list, depth_map: np.ndarray, image_width: int, image_height: int, center_x: float, center_y: float, depth_scale: float = 1.0, min_depth: float = 0.0, name: str = "RidgeMesh") -> bpy.types.Object:
    """
    Create mesh from ridge curves.
    """
    bm = bmesh.new()
    
    # Store handle layers
    layer_handle_start_x = bm.edges.layers.float.new("handle_start_x")
    layer_handle_start_y = bm.edges.layers.float.new("handle_start_y")
    layer_handle_start_z = bm.edges.layers.float.new("handle_start_z")
    layer_handle_end_x = bm.edges.layers.float.new("handle_end_x")
    layer_handle_end_y = bm.edges.layers.float.new("handle_end_y")
    layer_handle_end_z = bm.edges.layers.float.new("handle_end_z")
    
    for curve in curves:
        if len(curve) < 2:
            continue
            
        # Create vertices for this curve
        verts = []
        for x_img, y_img in curve:
            # Sample depth
            d = bilinear_sample(depth_map, x_img, y_img)
            
            # Normalize coordinates to 3D space
            # Image X right -> Blender X right
            x_norm = (x_img - center_x) / image_width
            
            # Image Y down -> Blender Y up
            y_norm = -(y_img - center_y) / image_height
            
            # Depth to Z (thickness)
            # Similar scaling as in depth_profile_mesh
            z_norm = (d - min_depth) * 0.5 * depth_scale
            
            # Create vertex (offset by z_norm)
            # Wait, do we want to create a surface or just lines?
            # The prompt says "output a debug view... for the curves that it is going to create"
            # And "put data on the generated mesh that conforms to mesh_curves_gizmo"
            # This implies we create edges representing the ridges.
            # Let's create edges on the surface.
            
            v = bm.verts.new((x_norm, y_norm, z_norm))
            verts.append(v)
            
        # Connect vertices with edges
        for i in range(len(verts) - 1):
            e = bm.edges.new((verts[i], verts[i+1]))
            
            # Initialize handles to zero (will be auto-calculated later)
            e[layer_handle_start_x] = 0
            e[layer_handle_start_y] = 0
            e[layer_handle_start_z] = 0
            e[layer_handle_end_x] = 0
            e[layer_handle_end_y] = 0
            e[layer_handle_end_z] = 0
            
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    return obj


@procedural_operator
class CreateHessianRidgeMeshOperator(Operator):
    """Create a mesh from depth map ridges using Hessian analysis"""
    
    bl_idname = "segmentation.create_hessian_ridge_mesh"
    bl_label = "Create Hessian Ridge Mesh"
    bl_description = "Extract ridges from depth map using Hessian analysis and create mesh curves"
    bl_options = {'REGISTER', 'UNDO'}
    
    sigma: FloatProperty(
        name="Gaussian Sigma",
        description="Scale of Gaussian smoothing for Hessian calculation",
        default=2.0,
        min=0.5,
        max=10.0
    )
    
    ridge_threshold: FloatProperty(
        name="Ridge Threshold",
        description="Threshold for ridge strength (0.0 - 1.0)",
        default=0.1,
        min=0.01,
        max=0.9
    )
    
    simplify_amount: FloatProperty(
        name="Simplify Amount",
        description="Curve simplification amount",
        default=0.005,
        min=0.0,
        max=0.05
    )
    
    depth_scale: FloatProperty(
        name="Depth Scale",
        description="Scale factor for Z-depth",
        default=1.0,
        min=0.1,
        max=5.0
    )
    
    subdivisions: IntProperty(
        name="Patch Subdivisions",
        description="Subdivisions for Charrot-Gregory patch",
        default=4,
        min=1,
        max=8
    )
    
    merge_by_distance: BoolProperty(
        name="Merge By Distance",
        description="Merge vertices at patch boundaries",
        default=True
    )
    
    def execute(self, context):
        # 1. Get Data
        masks = get_current_masks()
        if not masks:
            self.report({'WARNING'}, "No segmentation masks available")
            return {'CANCELLED'}
        
        # Get enabled masks
        settings = context.scene.segmentation_mask_settings
        enabled_indices = [item.mask_index for item in settings.masks if item.enabled and item.mask_index >= 0]
        
        if not enabled_indices:
            self.report({'WARNING'}, "No masks selected. Please enable at least one mask.")
            return {'CANCELLED'}
            
        depth_map = get_current_depth_map()
        if depth_map is None:
            self.report({'WARNING'}, "No depth map available")
            return {'CANCELLED'}
        
        # Resize depth map if needed (once)
        if depth_map.shape != masks[0].shape:
            # Simple resize for now, assuming all masks have same shape
            from PIL import Image as PILImage
            depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
            depth_pil = depth_pil.resize((masks[0].shape[1], masks[0].shape[0]), PILImage.BILINEAR)
            depth_map = np.array(depth_pil).astype(np.float32) / 255.0
            
        # 2. Hessian Analysis (Compute ONCE for the whole depth map)
        logger.info(f"Computing Hessian ridges (sigma={self.sigma})...")
        # Pass None as mask to get full ridge map
        full_ridge_map, _ = compute_hessian_ridge_map(depth_map, None, sigma=self.sigma)
        
        # Store for debug view (full map)
        set_current_hessian_map(full_ridge_map)
        
        created_objects = []
        all_curves = []
        
        for mask_index in enabled_indices:
            if mask_index >= len(masks):
                continue
            
            mask = masks[mask_index]
            
            # Apply specific mask to ridge map
            masked_ridge_map = full_ridge_map * mask
            
            # 3. Skeletonization
            skeleton = skeletonize_ridge_map(masked_ridge_map, mask, threshold=self.ridge_threshold)
            
            # 4. Vectorization
            curves = vectorize_skeleton(skeleton, mask, simplify_amount=self.simplify_amount)
            all_curves.extend(curves)
            
            if not curves:
                continue
                
            # 5. Mesh Creation
            # Calculate visual center for alignment
            y_indices, x_indices = np.where(mask)
            if len(y_indices) > 0:
                center_x = (np.min(x_indices) + np.max(x_indices)) / 2
                center_y = (np.min(y_indices) + np.max(y_indices)) / 2
            else:
                center_x = mask.shape[1] / 2
                center_y = mask.shape[0] / 2
                
            mask_depths = depth_map[mask]
            min_depth = mask_depths.min() if len(mask_depths) > 0 else 0.0
            
            obj = create_ridge_mesh(
                curves, 
                depth_map, 
                mask.shape[1], 
                mask.shape[0], 
                center_x, 
                center_y,
                depth_scale=self.depth_scale,
                min_depth=min_depth,
                name=f"RidgeMesh_{mask_index}"
            )
            
            # Align to camera
            camera = context.scene.camera
            if camera:
                mean_depth_val = np.mean(mask_depths) if len(mask_depths) > 0 else 0.5
                base_distance = 5.0
                depth_layering_range = 2.0
                object_distance = base_distance - (mean_depth_val - 0.5) * depth_layering_range
                
                sensor_width = camera.data.sensor_width
                focal_length = camera.data.lens
                render = context.scene.render
                aspect_ratio = render.resolution_x / render.resolution_y
                
                norm_cx = (center_x / mask.shape[1]) - 0.5
                norm_cy = 0.5 - (center_y / mask.shape[0])
                
                view_plane_width = object_distance * sensor_width / focal_length
                view_plane_height = view_plane_width / aspect_ratio
                
                offset_x = norm_cx * view_plane_width
                offset_y = norm_cy * view_plane_height
                
                obj.scale.x = view_plane_width
                obj.scale.y = view_plane_height
                obj.scale.z = view_plane_width
                
                camera_matrix = camera.matrix_world
                camera_location = camera_matrix.translation
                camera_rotation = camera_matrix.to_euler()
                cam_rot_mat = camera_rotation.to_matrix()
                
                cam_right = cam_rot_mat.col[0]
                cam_up = cam_rot_mat.col[1]
                cam_back = cam_rot_mat.col[2]
                
                target_location = camera_location - cam_back * object_distance + cam_right * offset_x + cam_up * offset_y
                obj.location = target_location
                obj.rotation_euler = camera_rotation
            
            # 6. Apply Handles and Patch
            try:
                apply_bezier_handles(obj)
                apply_charrot_gregory_patch_modifier(obj, self.subdivisions, self.merge_by_distance)
            except Exception as e:
                logger.warning(f"Failed to apply modifiers: {e}")
                
            created_objects.append(obj)
            
        # Store all curves for debug view
        set_current_ridge_curves(all_curves)
        
        # Select all created objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in created_objects:
            obj.select_set(True)
        if created_objects:
            context.view_layer.objects.active = created_objects[0]
        
        # Switch debug view to RIDGES
        context.scene["segmentation_view_mode"] = "RIDGES"
        # Trigger refresh
        bpy.ops.segmentation.refresh_overlay()
        
        self.report({'INFO'}, f"Created {len(created_objects)} ridge meshes")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
