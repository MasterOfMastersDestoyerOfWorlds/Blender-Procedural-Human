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
def compute_hessian_ridge_map(depth_map: np.ndarray, mask: np.ndarray, sigma: float = 1.0, silhouette_thresh: float = 0.5) -> tuple:
    """
    Computes Principal Curvature Magnitude and Direction, explicitly suppressing silhouettes.
    """
    depth_inverted = 1.0 - depth_map
    depth_smooth = gaussian_filter(depth_inverted, sigma=sigma, mode='nearest')
    dz_dy, dz_dx = np.gradient(depth_smooth)
    grad_mag = np.sqrt(dz_dx**2 + dz_dy**2)
    avg_grad = np.mean(grad_mag[mask > 0]) if mask is not None else np.mean(grad_mag)
    is_surface = grad_mag < (avg_grad * silhouette_thresh * 5.0)
    d2z_dy2, d2z_dxdy = np.gradient(dz_dy)
    d2z_dydx, d2z_dx2 = np.gradient(dz_dx)
    Hxx = d2z_dx2
    Hxy = d2z_dxdy
    Hyy = d2z_dy2
    root = np.sqrt((Hxx - Hyy)**2 + 4 * Hxy**2)
    lambda1 = (Hxx + Hyy + root) / 2.0
    lambda2 = (Hxx + Hyy - root) / 2.0
    abs_k1 = np.abs(lambda1)
    abs_k2 = np.abs(lambda2)
    
    dominant_k = np.where(abs_k1 > abs_k2, lambda1, lambda2)
    feature_strength = np.abs(dominant_k)
    ridge_theta = 0.5 * np.arctan2(2 * Hxy, Hxx - Hyy)
    if mask is not None:
        from scipy.ndimage import binary_erosion
        eroded_mask = binary_erosion(mask, iterations=2)
        feature_strength *= eroded_mask
    feature_strength *= is_surface
    f_max = np.max(feature_strength)
    if f_max > 0:
        feature_strength /= f_max
        
    return feature_strength, ridge_theta

def non_max_suppression_ridges(img: np.ndarray, theta: np.ndarray) -> np.ndarray:
    """
    Perform Non-Maximum Suppression (NMS) on curvature map.
    Instead of thinning a thresholded blob, this finds the exact sub-pixel peak
    along the curvature normal.
    """
    M, N = img.shape
    Z = np.zeros((M,N), dtype=np.float32)
    angle = np.degrees(theta)
    angle[angle < 0] += 180
    padded = np.pad(img, 1, mode='constant')
    center = padded[1:-1, 1:-1]
    
    v_e = padded[1:-1, 2:]
    v_w = padded[1:-1, :-2]
    v_n = padded[:-2, 1:-1]
    v_s = padded[2:, 1:-1]
    v_ne = padded[:-2, 2:]
    v_sw = padded[2:, :-2]
    v_nw = padded[:-2, :-2]
    v_se = padded[2:, 2:]
    mask_0 = np.logical_or(angle < 22.5, angle >= 157.5)
    mask_45 = np.logical_and(angle >= 22.5, angle < 67.5)
    mask_90 = np.logical_and(angle >= 67.5, angle < 112.5)
    mask_135 = np.logical_and(angle >= 112.5, angle < 157.5)
    q = np.zeros_like(center)
    r = np.zeros_like(center)
    q[mask_0] = v_e[mask_0]
    r[mask_0] = v_w[mask_0]
    q[mask_45] = v_ne[mask_45]
    r[mask_45] = v_sw[mask_45]
    q[mask_90] = v_n[mask_90]
    r[mask_90] = v_s[mask_90]
    q[mask_135] = v_nw[mask_135]
    r[mask_135] = v_se[mask_135]
    keep_mask = (center >= q) & (center > r)
    Z[keep_mask] = center[keep_mask]
    
    return Z

def hysteresis_thresholding(img: np.ndarray, low_thresh: float, high_thresh: float) -> np.ndarray:
    """
    Connect weak ridge pixels to strong ridge pixels.
    """
    strong_i, strong_j = np.where(img >= high_thresh)
    weak_i, weak_j = np.where((img >= low_thresh) & (img < high_thresh))
    
    output = np.zeros_like(img, dtype=np.uint8)
    output[strong_i, strong_j] = 1 # Strong
    output[weak_i, weak_j] = 2     # Weak
    
    stack = list(zip(strong_i, strong_j))
    rows, cols = img.shape
    
    while stack:
        r, c = stack.pop()
        output[r, c] = 1 # Mark as definitely part of ridge
        for nr in range(r-1, r+2):
            for nc in range(c-1, c+2):
                if 0 <= nr < rows and 0 <= nc < cols:
                    if output[nr, nc] == 2: # If weak
                        output[nr, nc] = 1 # Make strong
                        stack.append((nr, nc))
                        
    return (output == 1).astype(np.uint8)

def extract_surface_topology(ridge_map: np.ndarray, theta_map: np.ndarray, mask: np.ndarray, 
                           low_t: float = 0.1, high_t: float = 0.3) -> np.ndarray:
    """
    Pipeline: NMS -> Hysteresis -> Binary Skeleton
    """
    thinned_ridges = non_max_suppression_ridges(ridge_map, theta_map)
    
    if mask is not None:
        thinned_ridges *= mask
    skeleton = hysteresis_thresholding(thinned_ridges, low_t, high_t)
    
    return skeleton
    
def zhang_suen_thinning(binary_image: np.ndarray) -> np.ndarray:
    """
    Perform Zhang-Suen thinning algorithm for skeletonization.
    """
    img = binary_image.astype(np.uint8)
    if img.max() > 1:
        img = (img > 0).astype(np.uint8)
    try:
        return cv2.ximgproc.thinning(img * 255, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN) > 0
    except (AttributeError, ImportError):
        pass
    skeleton = img.copy()
    
    def iteration(im, iter_num):
        marker = np.zeros_like(im)
        rows, cols = im.shape
        for r in range(1, rows-1):
            for c in range(1, cols-1):
                if im[r, c] == 0:
                    continue
                p2 = im[r-1, c]
                p3 = im[r-1, c+1]
                p4 = im[r, c+1]
                p5 = im[r+1, c+1]
                p6 = im[r+1, c]
                p7 = im[r+1, c-1]
                p8 = im[r, c-1]
                p9 = im[r-1, c-1]
                
                neighbors = [p2, p3, p4, p5, p6, p7, p8, p9]
                B = sum(neighbors)
                if B < 2 or B > 6:
                    continue
                transitions = 0
                seq = neighbors + [p2]
                for k in range(8):
                    if seq[k] == 0 and seq[k+1] == 1:
                        transitions += 1
                if transitions != 1:
                    continue
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
    binary_ridge = ridge_map > threshold
    if mask is not None:
        binary_ridge = binary_ridge & mask
    try:
        from skimage.morphology import skeletonize
        skeleton = skeletonize(binary_ridge)
    except ImportError:
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
    points = np.column_stack(np.where(skeleton > 0))
    
    if len(points) == 0:
        return []
    pmap = {tuple(p): i for i, p in enumerate(points)}
    adj = {i: [] for i in range(len(points))}
    
    rows, cols = skeleton.shape
    for i, (r, c) in enumerate(points):
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
    degrees = {i: len(neighbors) for i, neighbors in adj.items()}
    
    junctions = [i for i, d in degrees.items() if d > 2]
    endpoints = [i for i, d in degrees.items() if d == 1]
    visited_edges = set() # Set of frozenset({u, v})
    curves = []
    start_nodes = junctions + endpoints
    
    for start_node in start_nodes:
        for neighbor in adj[start_node]:
            edge = frozenset({start_node, neighbor})
            if edge in visited_edges:
                continue
            path = [start_node, neighbor]
            visited_edges.add(edge)
            curr = neighbor
            prev = start_node
            
            while True:
                if degrees[curr] != 2:
                    break
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
            curve_coords = points[path] # Nx2 array of (row, col)
            curve_xy = np.column_stack([curve_coords[:, 1], curve_coords[:, 0]])
            if simplify_amount > 0:
                curve_xy = simplify_polyline(curve_xy, simplify_amount)
                
            curves.append(curve_xy)
    
    return curves


def create_ridge_mesh(curves: list, depth_map: np.ndarray, image_width: int, image_height: int, center_x: float, center_y: float, depth_scale: float = 1.0, min_depth: float = 0.0, name: str = "RidgeMesh") -> bpy.types.Object:
    """
    Create mesh from ridge curves.
    """
    bm = bmesh.new()
    layer_handle_start_x = bm.edges.layers.float.new("handle_start_x")
    layer_handle_start_y = bm.edges.layers.float.new("handle_start_y")
    layer_handle_start_z = bm.edges.layers.float.new("handle_start_z")
    layer_handle_end_x = bm.edges.layers.float.new("handle_end_x")
    layer_handle_end_y = bm.edges.layers.float.new("handle_end_y")
    layer_handle_end_z = bm.edges.layers.float.new("handle_end_z")
    
    for curve in curves:
        if len(curve) < 2:
            continue
        verts = []
        for x_img, y_img in curve:
            d = bilinear_sample(depth_map, x_img, y_img)
            x_norm = (x_img - center_x) / image_width
            y_norm = -(y_img - center_y) / image_height
            z_norm = (d - min_depth) * 0.5 * depth_scale
            
            v = bm.verts.new((x_norm, y_norm, z_norm))
            verts.append(v)
        for i in range(len(verts) - 1):
            e = bm.edges.new((verts[i], verts[i+1]))
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
    """Create a mesh from depth map ridges using Hessian NMS analysis"""
    
    bl_idname = "segmentation.create_hessian_ridge_mesh"
    bl_label = "Create Hessian Ridge Mesh"
    bl_description = "Extract surface ridges suppressing silhouettes using NMS"
    bl_options = {'REGISTER', 'UNDO'}
    
    sigma: FloatProperty(
        name="Gaussian Sigma",
        description="Scale of smoothing. Larger = major form, Smaller = texture details.",
        default=2.0, min=0.5, max=10.0
    )
    
    silhouette_cut: FloatProperty(
        name="Silhouette Suppression",
        description="Strength of occlusion boundary removal. Higher = removes more cliffs.",
        default=1.0, min=0.1, max=5.0
    )
    
    high_threshold: FloatProperty(
        name="Strong Ridge Threshold",
        description="Value above which a ridge is guaranteed to be kept.",
        default=0.2, min=0.01, max=1.0
    )
    
    low_threshold: FloatProperty(
        name="Weak Ridge Threshold",
        description="Value for connecting weak ridges to strong ones.",
        default=0.05, min=0.0, max=0.5
    )
    
    simplify_amount: FloatProperty(
        name="Simplify Amount",
        default=0.005, min=0.0, max=0.05
    )
    
    depth_scale: FloatProperty(name="Depth Scale", default=1.0)
    subdivisions: IntProperty(name="Patch Subdivisions", default=4)
    merge_by_distance: BoolProperty(name="Merge By Distance", default=True)
    
    def execute(self, context):
        masks = get_current_masks()
        if not masks:
            return {'CANCELLED'}
        
        settings = context.scene.segmentation_mask_settings
        enabled_indices = [item.mask_index for item in settings.masks if item.enabled and item.mask_index >= 0]
        
        depth_map = get_current_depth_map()
        if depth_map is None:
            return {'CANCELLED'}
        if depth_map.shape != masks[0].shape:
            from PIL import Image as PILImage
            depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
            depth_pil = depth_pil.resize((masks[0].shape[1], masks[0].shape[0]), PILImage.BILINEAR)
            depth_map = np.array(depth_pil).astype(np.float32) / 255.0
            
        created_objects = []
        all_curves = []
        
        for mask_index in enabled_indices:
            if mask_index >= len(masks): continue
            mask = masks[mask_index]
            logger.info(f"Computing Surface Ridges for mask {mask_index} (sigma={self.sigma})...")
            full_ridge_map, full_theta_map = compute_hessian_ridge_map(
                depth_map, 
                mask, 
                sigma=self.sigma,
                silhouette_thresh=self.silhouette_cut
            )
            masked_ridge = full_ridge_map * mask
            masked_theta = full_theta_map
            skeleton = extract_surface_topology(
                masked_ridge, 
                masked_theta, 
                mask,
                low_t=self.low_threshold, 
                high_t=self.high_threshold
            )
            curves = vectorize_skeleton(skeleton, mask, simplify_amount=self.simplify_amount)
            all_curves.extend(curves)
            
            if not curves: continue
            y_indices, x_indices = np.where(mask)
            if len(y_indices) > 0:
                center_x = (np.min(x_indices) + np.max(x_indices)) / 2
                center_y = (np.min(y_indices) + np.max(y_indices)) / 2
            else:
                center_x, center_y = mask.shape[1]/2, mask.shape[0]/2
                
            mask_depths = depth_map[mask]
            min_depth = mask_depths.min() if len(mask_depths) > 0 else 0.0
            
            obj = create_ridge_mesh(
                curves, depth_map, mask.shape[1], mask.shape[0], 
                center_x, center_y,
                depth_scale=self.depth_scale, min_depth=min_depth,
                name=f"RidgeMesh_{mask_index}"
            )
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
                cam_right = cam_rot_mat.col[0] # X
                cam_up = cam_rot_mat.col[1]    # Y
                cam_back = cam_rot_mat.col[2]  # Z
                
                target_location = camera_location - cam_back * object_distance + cam_right * offset_x + cam_up * offset_y
                
                obj.location = target_location
                obj.rotation_euler = camera_rotation
            
            try:
                apply_bezier_handles(obj)
                apply_charrot_gregory_patch_modifier(obj, self.subdivisions, self.merge_by_distance)
            except Exception as e:
                logger.warning(f"Modifier Error: {e}")
                
            created_objects.append(obj)
            
        set_current_hessian_map(full_ridge_map if 'full_ridge_map' in locals() else None)
        set_current_ridge_curves(all_curves)
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in created_objects: obj.select_set(True)
        if created_objects: context.view_layer.objects.active = created_objects[0]
        
        context.scene["segmentation_view_mode"] = "RIDGES"
        bpy.ops.segmentation.refresh_overlay()
        
        self.report({'INFO'}, f"Created {len(created_objects)} surface feature meshes")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)