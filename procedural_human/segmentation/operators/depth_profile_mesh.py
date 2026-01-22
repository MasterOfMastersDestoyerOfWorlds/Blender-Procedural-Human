import bpy
import bmesh
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
from procedural_human.segmentation.operators.segmentation_operators import (
    set_current_medialness_map
)
import cv2
from PIL import Image as PILImage
from procedural_human.segmentation.overlays.spine_overlay import set_current_spine_path
from scipy.ndimage import distance_transform_edt
import skfmm 
from scipy.ndimage import gaussian_filter 


def skeletonize_cv2(mask: np.ndarray) -> np.ndarray:
    """
    Compute the skeleton of a binary mask using OpenCV morphological thinning.
    """
    import cv2  
    img = mask.astype(np.uint8) * 255
    try:
        import cv2.ximgproc
        skeleton = cv2.ximgproc.thinning(img, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
        return skeleton
    except (ImportError, AttributeError):
        pass
    skeleton = np.zeros(img.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    temp_img = img.copy()
    
    while True:
        open_img = cv2.morphologyEx(temp_img, cv2.MORPH_OPEN, element)
        temp = cv2.subtract(temp_img, open_img)
        eroded = cv2.erode(temp_img, element)
        skeleton = cv2.bitwise_or(skeleton, temp)
        temp_img = eroded.copy()
        if cv2.countNonZero(temp_img) == 0:
            break
            
    return skeleton

def simplify_skeleton(skeleton: np.ndarray, epsilon: float = 2.0) -> list:
    """
    Convert a pixel skeleton into a simplified graph of branches.
    Returns: list of branches, where each branch is a list of (y,x) points.
    """
    y_idxs, x_idxs = np.where(skeleton > 0)
    if len(y_idxs) == 0:
        return []
        
    points = set(zip(y_idxs, x_idxs))
    junctions = []
    endpoints = []
    def get_neighbors(p):
        y, x = p
        ns = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0: continue
                n = (y + dy, x + dx)
                if n in points:
                    ns.append(n)
        return ns

    for p in points:
        ns = get_neighbors(p)
        count = len(ns)
        if count == 1:
            endpoints.append(p)
        elif count > 2:
            junctions.append(p)
    
    contours, _ = cv2.findContours(skeleton, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    simplified_branches = []
    for cnt in contours:
        cnt = cnt.squeeze()
        if len(cnt.shape) < 2: continue
        approx = cv2.approxPolyDP(cnt, epsilon, False) 
        approx = approx.squeeze()
        if len(approx.shape) < 2: continue
        simplified_branches.append(approx)
        
    return simplified_branches

def find_nearest_point_on_polyline(point: np.ndarray, polyline: np.ndarray) -> tuple:
    """
    Find the nearest point on a polyline to a query point.
    Returns: (nearest_point, distance, segment_index, t)
    """
    best_dist = float('inf')
    best_pt = None
    best_seg = -1
    
    p = point
    
    for i in range(len(polyline) - 1):
        a = polyline[i]
        b = polyline[i+1]
        ab = b - a
        ap = p - a
        len_sq = np.dot(ab, ab)
        if len_sq == 0:
            t = 0
        else:
            t = np.dot(ap, ab) / len_sq
            t = max(0.0, min(1.0, t))
            
        closest = a + t * ab
        dist = np.linalg.norm(p - closest)
        
        if dist < best_dist:
            best_dist = dist
            best_pt = closest
            best_seg = i
            
    return best_pt, best_dist, best_seg

def create_control_cage(
    boundary_contour_norm: np.ndarray,
    skeleton_branches: list,
    depth_map: np.ndarray,
    image_width: int,
    image_height: int,
    center_x: float,
    center_y: float,
    min_depth: float,
    depth_scale: float = 1.0,
    name: str = "ControlCage"
) -> 'bpy.types.Object':
    """
    Create a sparse Control Cage mesh for Charrot-Gregory Patches.
    """
    bm = bmesh.new()
    b_verts = []
    
    for i, (bx, by) in enumerate(boundary_contour_norm):
        ix = int(bx * image_width + center_x)
        iy = int(center_y - by * image_height)
        ix = max(0, min(image_width - 1, ix))
        iy = max(0, min(image_height - 1, iy))
        if iy < 0 or iy >= depth_map.shape[0] or ix < 0 or ix >= depth_map.shape[1]:
            d = 0.5  # Default/fallback
        else:
            d = depth_map[iy, ix]
            
        z = (d - min_depth) * depth_scale * 0.5 
        
        v = bm.verts.new((bx, by, 0.0)) 
        b_verts.append(v)
    b_edges = []
    for i in range(len(b_verts)):
        v1 = b_verts[i]
        v2 = b_verts[(i + 1) % len(b_verts)]
        e = bm.edges.new((v1, v2))
        b_edges.append(e)
    if not skeleton_branches:
        skeleton_branches = [np.array([[0, -0.5], [0, 0.5]])] 
    
    main_branch_pixels = max(skeleton_branches, key=lambda b: len(b)) 
    main_branch = []
    for px, py in main_branch_pixels:
        nx = (px - center_x) / image_width
        ny = -(py - center_y) / image_height
        main_branch.append((nx, ny))
        
    main_branch = np.array(main_branch)
    s_front_verts = []
    s_back_verts = []
    
    for nx, ny in main_branch:
        ix = int(nx * image_width + center_x)
        iy = int(center_y - ny * image_height)
        ix = max(0, min(image_width - 1, ix))
        iy = max(0, min(image_height - 1, iy))
        
        if iy < 0 or iy >= depth_map.shape[0] or ix < 0 or ix >= depth_map.shape[1]:
            d = 0.5
        else:
            d = depth_map[iy, ix]

        thickness = (d - min_depth) * depth_scale * 0.5
        
        vf = bm.verts.new((nx, ny, thickness))
        vb = bm.verts.new((nx, ny, -thickness))
        
        s_front_verts.append(vf)
        s_back_verts.append(vb)
    for i in range(len(s_front_verts) - 1):
        bm.edges.new((s_front_verts[i], s_front_verts[i+1]))
        bm.edges.new((s_back_verts[i], s_back_verts[i+1]))
    b_points = boundary_contour_norm
    top_idx = np.argmax(b_points[:, 1])
    bottom_idx = np.argmin(b_points[:, 1])
    bm.edges.new((b_verts[top_idx], s_front_verts[0])) 
    bm.edges.new((b_verts[top_idx], s_back_verts[0]))  
    bm.edges.new((b_verts[bottom_idx], s_front_verts[-1])) 
    bm.edges.new((b_verts[bottom_idx], s_back_verts[-1]))  
    b_left_verts = []
    idx = top_idx
    if top_idx <= bottom_idx:
        pass
    path1 = []
    curr = top_idx
    while True:
        path1.append(b_verts[curr])
        if curr == bottom_idx:
            break
        curr = (curr + 1) % len(b_verts)
    path2 = []
    curr = top_idx
    while True:
        path2.append(b_verts[curr])
        if curr == bottom_idx:
            break
        curr = (curr - 1) % len(b_verts)
    mid_p1 = path1[len(path1)//2].co.x
    mid_p2 = path2[len(path2)//2].co.x
    
    if mid_p1 < mid_p2:
        b_left_verts = path1
        b_right_verts = path2
    else:
        b_left_verts = path2
        b_right_verts = path1
    s_front_reversed = list(reversed(s_front_verts))
    
    left_front_loop = b_left_verts + s_front_reversed
    try:
        if len(left_front_loop) >= 3:
            bm.faces.new(left_front_loop)
    except ValueError:
        logger.warning("Failed to create Left Front face")
    b_right_up = list(reversed(b_right_verts))
    s_front_normal = list(s_front_verts)
    
    right_front_loop = b_right_up + s_front_normal
    try:
        if len(right_front_loop) >= 3:
            bm.faces.new(right_front_loop)
    except ValueError:
        logger.warning("Failed to create Right Front face")
    s_back_reversed = list(reversed(s_back_verts))
    b_left_up = list(reversed(b_left_verts)) 
    s_back_normal = list(s_back_verts) 
    
    left_back_loop = s_back_normal + b_left_up
    try:
        if len(left_back_loop) >= 3:
            bm.faces.new(left_back_loop)
    except ValueError:
        logger.warning("Failed to create Left Back face")
    
    right_back_loop = s_back_reversed + b_right_verts
    try:
        if len(right_back_loop) >= 3:
            bm.faces.new(right_back_loop)
    except ValueError:
        logger.warning("Failed to create Right Back face")

    bm.verts.ensure_lookup_table()
    bm.normal_update()
    
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def compute_medialness_speed(mask: np.ndarray, depth_map: np.ndarray, gamma: float = 10.0) -> np.ndarray:
    """
    Constructs the Medialness Field and Speed Map.
    Fuses Boundary Distance (EDT) and Volumetric Depth.
    Ref: Section 4.1 of the Report.
    """
    depth_smooth = gaussian_filter(depth_map, sigma=2.0)
    if np.any(mask):
        edt = distance_transform_edt(mask)
    else:
        return np.zeros_like(depth_map)
    d_max = np.max(depth_smooth)
    e_max = np.max(edt)
    
    d_norm = depth_smooth / d_max if d_max > 0 else depth_smooth
    edt_norm = edt / e_max if e_max > 0 else edt
    M = 0.5 * edt_norm + 0.5 * d_norm
    speed = np.exp(gamma * M)
    
    return np.ma.masked_array(speed, ~mask)

def extract_geodesic_path(mask: np.ndarray, speed_map: np.ndarray) -> np.ndarray:
    """
    Performs the Double Sweep and Gradient Descent Backtracking.
    Ref: Section 5 and 6.2 of the Report.
    Returns: Nx2 array of (x, y) coordinates for the spine.
    """
    seed_idx = np.unravel_index(np.argmax(speed_map), speed_map.shape)
    logger.info(f"Geodesic seed (max medialness): {seed_idx}")
    phi = np.ones_like(speed_map.data)
    phi[seed_idx] = 0
    t1 = skfmm.travel_time(np.ma.masked_array(phi, ~mask), speed_map)
    
    if t1 is None: 
        return np.array([seed_idx[::-1]]) 
    if hasattr(t1, 'filled'):
        t1_for_argmax = t1.filled(-np.inf)
    else:
        t1_for_argmax = np.where(np.isfinite(t1), t1, -np.inf)
    tip_idx = np.unravel_index(np.argmax(t1_for_argmax), t1.shape)
    phi[:] = 1
    phi[tip_idx] = 0
    t2 = skfmm.travel_time(np.ma.masked_array(phi, ~mask), speed_map)
    if hasattr(t2, 'filled'):
        t2_for_argmax = t2.filled(-np.inf)
    else:
        t2_for_argmax = np.where(np.isfinite(t2), t2, -np.inf)
    tail_idx = np.unravel_index(np.argmax(t2_for_argmax), t2.shape)
    if hasattr(t2, 'filled'):
        t2_filled = t2.filled(np.inf)
    else:
        t2_filled = np.where(np.isfinite(t2), t2, np.inf)
    edt = distance_transform_edt(mask)
    min_boundary_dist = 3  
    
    def find_interior_point(idx, t_filled, mask, edt, search_radius=20):
        """Find a valid interior point near idx that's away from mask boundary."""
        r, c = idx
        if mask[r, c] and np.isfinite(t_filled[r, c]) and edt[r, c] >= min_boundary_dist:
            return idx
        best_idx = None
        best_score = -np.inf
        for radius in range(1, search_radius + 1):
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < mask.shape[0] and 0 <= nc < mask.shape[1]:
                        if mask[nr, nc] and np.isfinite(t_filled[nr, nc]):
                            boundary_dist = edt[nr, nc]
                            if boundary_dist >= min_boundary_dist:
                                score = t_filled[nr, nc] + boundary_dist * 0.1
                                if score > best_score:
                                    best_score = score
                                    best_idx = (nr, nc)
            if best_idx is not None:
                return best_idx
        for radius in range(1, search_radius + 1):
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < mask.shape[0] and 0 <= nc < mask.shape[1]:
                        if mask[nr, nc] and np.isfinite(t_filled[nr, nc]):
                            return (nr, nc)
        return idx  
    if not mask[tip_idx] or not np.isfinite(t2_filled[tip_idx]) or edt[tip_idx] < min_boundary_dist:
        logger.warning(f"Tip {tip_idx} is near boundary (edt={edt[tip_idx]:.1f}), finding interior point...")
        tip_idx = find_interior_point(tip_idx, t2_filled, mask, edt)
        logger.info(f"Found interior tip at {tip_idx} (edt={edt[tip_idx]:.1f})")
    if not mask[tail_idx] or not np.isfinite(t2_filled[tail_idx]) or edt[tail_idx] < min_boundary_dist:
        logger.warning(f"Tail {tail_idx} is near boundary (edt={edt[tail_idx]:.1f}), finding interior point...")
        tail_idx = find_interior_point(tail_idx, t2_filled, mask, edt)
        logger.info(f"Found interior tail at {tail_idx} (edt={edt[tail_idx]:.1f})")
    tip_tail_dist = np.sqrt((tip_idx[0] - tail_idx[0])**2 + (tip_idx[1] - tail_idx[1])**2)
    logger.info(f"Geodesic endpoints: tip={tip_idx}, tail={tail_idx}, distance={tip_tail_dist:.1f}px")
    max_travel_time = t2_filled[tail_idx]
    if not np.isfinite(max_travel_time) or max_travel_time <= 0:
        max_travel_time = 1.0
    time_threshold = max_travel_time * 0.01
    
    logger.info(f"Geodesic backtrack: tip={tip_idx}, tail={tail_idx}, max_time={max_travel_time:.4f}, threshold={time_threshold:.4f}")
    
    path = []
    current = np.array(tail_idx, dtype=np.float64)
    tip = np.array(tip_idx, dtype=np.float64)
    step_size = 0.5
    max_steps = int(mask.size) 
    
    path.append(current[::-1].copy()) 
    
    for step_num in range(max_steps):
        r, c = int(current[0]), int(current[1])
        t2_val = t2_filled[r, c]
        if not np.isfinite(t2_val) or t2_val < time_threshold or np.linalg.norm(current - tip) < 1.0:
            logger.info(f"Geodesic backtrack stopped at step {step_num}: t2_val={t2_val:.4f}, dist_to_tip={np.linalg.norm(current - tip):.2f}")
            break
        r_min, r_max = max(0, r-1), min(mask.shape[0]-1, r+1)
        c_min, c_max = max(0, c-1), min(mask.shape[1]-1, c+1)
        v_r_max = t2_filled[r_max, c]
        v_r_min = t2_filled[r_min, c]
        v_c_max = t2_filled[r, c_max]
        v_c_min = t2_filled[r, c_min]
        if not np.isfinite(v_r_max): v_r_max = t2_val
        if not np.isfinite(v_r_min): v_r_min = t2_val
        if not np.isfinite(v_c_max): v_c_max = t2_val
        if not np.isfinite(v_c_min): v_c_min = t2_val
        
        grad_r = (v_r_max - v_r_min) / 2.0
        grad_c = (v_c_max - v_c_min) / 2.0
        
        grad = np.array([grad_r, grad_c])
        norm = np.linalg.norm(grad)
        
        if norm > 1e-6:
            grad /= norm
        else:
            break 
        new_pos = current - grad * step_size
        new_pos[0] = np.clip(new_pos[0], 0, mask.shape[0]-1)
        new_pos[1] = np.clip(new_pos[1], 0, mask.shape[1]-1)
        
        new_r, new_c = int(new_pos[0]), int(new_pos[1])
        if not mask[new_r, new_c] or not np.isfinite(t2_filled[new_r, new_c]):
            found_valid = False
            for substep in [0.25, 0.1, 0.05]:
                test_pos = current - grad * substep
                test_pos[0] = np.clip(test_pos[0], 0, mask.shape[0]-1)
                test_pos[1] = np.clip(test_pos[1], 0, mask.shape[1]-1)
                test_r, test_c = int(test_pos[0]), int(test_pos[1])
                if mask[test_r, test_c] and np.isfinite(t2_filled[test_r, test_c]):
                    new_pos = test_pos
                    found_valid = True
                    break
            
            if not found_valid:
                to_tip = tip - current
                to_tip_norm = np.linalg.norm(to_tip)
                if to_tip_norm > 1e-6:
                    to_tip /= to_tip_norm
                    for substep in [0.5, 0.25, 0.1]:
                        test_pos = current + to_tip * substep
                        test_pos[0] = np.clip(test_pos[0], 0, mask.shape[0]-1)
                        test_pos[1] = np.clip(test_pos[1], 0, mask.shape[1]-1)
                        test_r, test_c = int(test_pos[0]), int(test_pos[1])
                        if mask[test_r, test_c] and np.isfinite(t2_filled[test_r, test_c]):
                            new_pos = test_pos
                            found_valid = True
                            break
            
            if not found_valid:
                break
        
        current = new_pos
        path.append(current[::-1].copy()) 
        
    return np.array(path)

from procedural_human.segmentation.operators.segmentation_utils import (
    bilinear_sample,
    simplify_contour,
    simplify_polyline,
    resample_polyline
)

def extract_spine_path_3d(
    mask: np.ndarray,
    depth_map: np.ndarray,
    image_width: int,
    image_height: int,
    center_x: float,
    center_y: float,
) -> np.ndarray:
    """
    Extract the 3D spine path along the medial axis with depth-based Z inflation.
    
    Returns the natural number of points from geodesic path extraction (no resampling).
    
    Returns an Nx3 array of (x, y, z_extent) in Blender normalized coordinates where:
    - x, y follow the actual curved medial axis path (not projected to vertical)
    - z_extent = (depth - min_depth) for symmetric ±Z inflation
    
    Args:
        mask: Binary segmentation mask
        depth_map: Depth map (0-1 range)
        image_width: Image width in pixels
        image_height: Image height in pixels
        center_x: X coordinate of visual center in image space
        center_y: Y coordinate of visual center in image space
        
    Returns:
        Nx3 array of [x, y, z_extent] in Blender normalized coordinates
    """
    if depth_map.shape != mask.shape:
        depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
        depth_pil = depth_pil.resize((mask.shape[1], mask.shape[0]), PILImage.BILINEAR)
        depth_map = np.array(depth_pil).astype(np.float32) / 255.0
    mask_depths = depth_map[mask]
    if len(mask_depths) == 0:
        return np.array([[0, -0.5, 0], [0, 0.5, 0]])
    
    min_depth = mask_depths.min()
    max_depth = mask_depths.max()
    depth_range = max_depth - min_depth if max_depth > min_depth else 1.0
    try:
        speed_map = compute_medialness_speed(mask, depth_map)
        set_current_medialness_map(speed_map.copy() if hasattr(speed_map, 'copy') else speed_map)
        spine_path_xy = extract_geodesic_path(mask, speed_map)
        
        logger.info(f"Geodesic spine extracted: {len(spine_path_xy)} points, "
                    f"x range [{spine_path_xy[:, 0].min():.1f}, {spine_path_xy[:, 0].max():.1f}], "
                    f"y range [{spine_path_xy[:, 1].min():.1f}, {spine_path_xy[:, 1].max():.1f}]")
        set_current_spine_path(spine_path_xy.copy())
        
    except (ImportError, Exception) as e:
        logger.warning(f"Geodesic extraction failed ({e}), falling back to simple center.")
        y_indices = np.where(np.any(mask, axis=1))[0]
        if len(y_indices) > 0:
            spine_path_xy = np.column_stack([
                np.full(len(y_indices), mask.shape[1] / 2), 
                y_indices
            ])
        else:
            return np.array([[0, -0.5, 0], [0, 0.5, 0]])

    if len(spine_path_xy) < 2:
        return np.array([[0, -0.5, 0], [0, 0.5, 0]])
    sampled_depths = np.array([
        bilinear_sample(depth_map, x, y) 
        for x, y in spine_path_xy
    ])
    
    logger.info(f"Sampled depths along spine: min={sampled_depths.min():.4f}, max={sampled_depths.max():.4f}, "
                f"mask depth range: [{min_depth:.4f}, {max_depth:.4f}]")
    z_extent = sampled_depths - min_depth
    
    x_normalized = (spine_path_xy[:, 0] - center_x) / image_width
    y_normalized = -(spine_path_xy[:, 1] - center_y) / image_height
    z_normalized = z_extent * 0.5  
    
    logger.info(f"Spine path 3D: x range [{x_normalized.min():.4f}, {x_normalized.max():.4f}], "
                f"y range [{y_normalized.min():.4f}, {y_normalized.max():.4f}], "
                f"z range [{z_normalized.min():.4f}, {z_normalized.max():.4f}], "
                f"depth range [{min_depth:.4f}, {max_depth:.4f}]")
    
    return np.column_stack([x_normalized, y_normalized, z_normalized])


def create_inflated_mesh_from_spine(
    front_contour: np.ndarray,
    spine_path_3d: np.ndarray,
    name: str = "InflatedMesh",
) -> 'bpy.types.Object':
    """
    Create a mesh from a front contour and a 3D curved spine path.
    
    Uses the natural number of points from both contours without resampling.
    
    Args:
        front_contour: Front view contour Nx2 in XY plane (Blender normalized coords)
        spine_path_3d: Spine path Mx3 as [x, y, z_extent] where z_extent is the
                       inflation amount (symmetric ±Z from the path)
        name: Name for the mesh object
        
    Returns:
        The created Blender mesh object
    """
    from procedural_human.segmentation.operators.mesh_curve_operators import (
        find_axis_crossing_indices,
        split_contour_at_crossings,
    )
    front_norm = front_contour
    front_top_cross, front_bottom_cross = find_axis_crossing_indices(front_norm)
    front_half1, front_half2 = split_contour_at_crossings(front_norm, front_top_cross, front_bottom_cross)
    def get_dominant_x_sign(half):
        mid_idx = len(half) // 2
        if mid_idx < len(half):
            return -1 if half[mid_idx, 0] < 0 else 1
        return 0
    
    if get_dominant_x_sign(front_half1) < 0:
        front_left, front_right = front_half1, front_half2
    else:
        front_left, front_right = front_half2, front_half1
    spine = spine_path_3d
    bm = bmesh.new()
    spine_tip = spine[0]   
    spine_tail = spine[-1]  
    top_vert = bm.verts.new((spine_tip[0], spine_tip[1], 0))
    bottom_vert = bm.verts.new((spine_tail[0], spine_tail[1], 0))
    front_left_verts = []
    for i in range(len(front_left)):
        x, y = front_left[i]
        v = bm.verts.new((x, y, 0))
        front_left_verts.append(v)
    front_right_verts = []
    for i in range(len(front_right)):
        x, y = front_right[i]
        v = bm.verts.new((x, y, 0))
        front_right_verts.append(v)
    spine_back_verts = []
    for i in range(len(spine)):
        spine_x = spine[i, 0]
        spine_y = spine[i, 1]
        z_ext = spine[i, 2]
        v = bm.verts.new((spine_x, spine_y, -z_ext))
        spine_back_verts.append(v)
    spine_front_verts = []
    for i in range(len(spine)):
        spine_x = spine[i, 0]
        spine_y = spine[i, 1]
        z_ext = spine[i, 2]
        v = bm.verts.new((spine_x, spine_y, +z_ext))
        spine_front_verts.append(v)
    
    bm.verts.ensure_lookup_table()
    q1_verts = [top_vert] + front_left_verts + [bottom_vert] + list(reversed(spine_back_verts))
    if len(q1_verts) >= 3:
        try:
            bm.faces.new(q1_verts)
        except ValueError as e:
            logger.warning(f"Could not create Q1 face: {e}")
    q2_verts = [top_vert] + spine_front_verts + [bottom_vert] + list(reversed(front_left_verts))
    if len(q2_verts) >= 3:
        try:
            bm.faces.new(q2_verts)
        except ValueError as e:
            logger.warning(f"Could not create Q2 face: {e}")
    q3_verts = [top_vert] + front_right_verts + [bottom_vert] + list(reversed(spine_front_verts))
    if len(q3_verts) >= 3:
        try:
            bm.faces.new(q3_verts)
        except ValueError as e:
            logger.warning(f"Could not create Q3 face: {e}")
    q4_verts = [top_vert] + spine_back_verts + [bottom_vert] + list(reversed(front_right_verts))
    if len(q4_verts) >= 3:
        try:
            bm.faces.new(q4_verts)
        except ValueError as e:
            logger.warning(f"Could not create Q4 face: {e}")
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    logger.info(f"Created inflated mesh '{name}' with {len(mesh.vertices)} vertices")
    
    return obj


def create_spine_contour_from_depth(
    mask: np.ndarray,
    depth_map: np.ndarray,
    image_width: int,
    image_height: int,
    num_points: int = 32
) -> np.ndarray:
    """
    Create a side profile (spine) contour using Geodesic Pathfinding.
    
    NOTE: This is the legacy function that projects the spine to a vertical line.
    For curved 3D spines, use extract_spine_path_3d() + create_inflated_mesh_from_spine().
    """
    if depth_map.shape != mask.shape:
        depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
        depth_pil = depth_pil.resize((mask.shape[1], mask.shape[0]), PILImage.BILINEAR)
        depth_map = np.array(depth_pil).astype(np.float32) / 255.0
    try:
        speed_map = compute_medialness_speed(mask, depth_map)
        spine_path_xy = extract_geodesic_path(mask, speed_map)
        
    except (ImportError, Exception) as e:
        logger.warning(f"Geodesic extraction failed ({e}), falling back to simple center.")
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
    sample_x = np.clip(spine_path_xy[:, 0], 0, mask.shape[1]-1).astype(int)
    sample_y = np.clip(spine_path_xy[:, 1], 0, mask.shape[0]-1).astype(int)
    
    sampled_depths = depth_map[sample_y, sample_x]
    
    y_min, y_max = np.min(sample_y), np.max(sample_y)
    mask_height = max(1.0, y_max - y_min)
    mask_center_y = (y_max + y_min) / 2.0
    y_normalized = -(sample_y - mask_center_y) / mask_height
    sort_idx = np.argsort(y_normalized)
    y_sorted = y_normalized[sort_idx]
    depth_sorted = sampled_depths[sort_idx]
    unique_y, unique_indices = np.unique(y_sorted, return_index=True)
    unique_depths = depth_sorted[unique_indices]
    
    if len(unique_y) < 2:
         return np.column_stack([np.zeros(num_points), np.linspace(-0.5, 0.5, num_points)])
    y_target = np.linspace(unique_y[0], unique_y[-1], num_points)
    depth_interp = np.interp(y_target, unique_y, unique_depths)
    d_min = depth_interp.min()
    d_max = depth_interp.max()
    if d_max > d_min:
        width_factor = (depth_interp - d_min) / (d_max - d_min)
    else:
        width_factor = np.full_like(depth_interp, 0.5)
    contour_points = []
    for i in range(num_points):
        contour_points.append([width_factor[i] * 0.5, y_target[i]])
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
    
    simplify_amount: FloatProperty(
        name="Simplify Amount",
        description="Contour simplification - higher values = fewer points (0 = no simplification)",
        default=0.005,
        min=0.0,
        max=0.05
    )
    
    def execute(self, context):
        from procedural_human.segmentation.operators.segmentation_operators import (
            get_current_masks, get_active_image, get_current_depth_map
        )
        from procedural_human.segmentation.mask_to_curve import find_contours
        camera = context.scene.camera
        if camera is None:
            self.report({'WARNING'}, "No camera found in scene. Please set a camera as active.")
            return {'CANCELLED'}
        masks = get_current_masks()
        if not masks:
            self.report({'WARNING'}, "No segmentation masks available. Run segmentation first.")
            return {'CANCELLED'}
        settings = context.scene.segmentation_mask_settings
        mask_index = 0
        if len(settings.masks) > 0:
            enabled_indices = [item.mask_index for item in settings.masks if item.enabled and item.mask_index >= 0]
            if enabled_indices:
                mask_index = enabled_indices[0]
        if mask_index >= len(masks):
            mask_index = 0
        mask = masks[mask_index]
        depth_map = get_current_depth_map()
        if depth_map is None:
            self.report({'WARNING'}, "No depth map available. Run depth estimation first.")
            return {'CANCELLED'}
        image = get_active_image(context)
        if image:
            image_width, image_height = image.size
        else:
            image_height, image_width = mask.shape[:2]
        
        try:
            contours = find_contours(mask)
            if not contours:
                self.report({'WARNING'}, "Could not extract contour from mask")
                return {'CANCELLED'}
            front_contour = max(contours, key=len)
            if self.simplify_amount > 0:
                front_contour = simplify_contour(front_contour, self.simplify_amount)
            try:
                dist = distance_transform_edt(mask)
                max_idx = np.argmax(dist)
                max_y, max_x = np.unravel_index(max_idx, dist.shape)
                center_x, center_y = float(max_x), float(max_y)
            except ImportError:
                M = cv2.moments(mask.astype(np.uint8)) if 'cv2' in locals() else None
                if M and M["m00"] != 0:
                    center_x = M["m10"] / M["m00"]
                    center_y = M["m01"] / M["m00"]
                else:
                    y_indices, x_indices = np.where(mask)
                    center_x = (np.min(x_indices) + np.max(x_indices)) / 2
                    center_y = (np.min(y_indices) + np.max(y_indices)) / 2
            front_contour_norm = front_contour.astype(np.float32).copy()
            front_contour_norm[:, 0] = (front_contour_norm[:, 0] - center_x) / image_width
            front_contour_norm[:, 1] = -(front_contour_norm[:, 1] - center_y) / image_height
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
            base_distance = 5.0
            depth_layering_range = 2.0  
            object_distance = base_distance - (mean_depth_val - 0.5) * depth_layering_range
            sensor_width = camera.data.sensor_width
            focal_length = camera.data.lens
            render = context.scene.render
            aspect_ratio = render.resolution_x / render.resolution_y
            
            norm_cx = (center_x / image_width) - 0.5
            norm_cy = 0.5 - (center_y / image_height)  
            view_plane_width = object_distance * sensor_width / focal_length
            view_plane_height = view_plane_width / aspect_ratio
            
            offset_x = norm_cx * view_plane_width
            offset_y = norm_cy * view_plane_height


            logger.info("Starting Control Cage generation...")
            skeleton = skeletonize_cv2(mask)
            set_current_medialness_map(skeleton)
            if np.count_nonzero(skeleton) == 0:
                logger.warning("Skeletonize failed (empty), falling back to simple spine.")
                skeleton_branches = []
            else:
                skeleton_branches = simplify_skeleton(skeleton, epsilon=2.0)
            
            if skeleton_branches:
                main_branch = max(skeleton_branches, key=len)
                set_current_spine_path(main_branch)
            else:
                set_current_spine_path(None)

            if len(mask_depths) > 0:
                 min_depth = mask_depths.min()
            else:
                 min_depth = 0.0
            
            obj = create_control_cage(
                front_contour_norm,
                skeleton_branches,
                depth_map,
                image_width,
                image_height,
                center_x,
                center_y,
                min_depth,
                depth_scale=self.depth_scale,
                name=f"DepthMesh_{mask_index}",
            )
            obj.scale.x = view_plane_width
            obj.scale.y = view_plane_height
            obj.scale.z = view_plane_width 
            
            logger.info(f"Created control cage: {obj.name} at dist {object_distance:.2f}")
            try:
                apply_bezier_handles(obj)
            except Exception as e:
                logger.warning(f"Could not apply Bezier handles: {e}")
            try:
                apply_charrot_gregory_patch_modifier(
                    obj,
                    self.subdivisions,
                    self.merge_by_distance
                )
            except Exception as e:
                logger.warning(f"Could not apply Charrot-Gregory patch: {e}")
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
        layout.prop(self, "depth_scale")
        layout.prop(self, "simplify_amount")
        layout.separator()
        layout.prop(self, "subdivisions")
        layout.prop(self, "merge_by_distance")
