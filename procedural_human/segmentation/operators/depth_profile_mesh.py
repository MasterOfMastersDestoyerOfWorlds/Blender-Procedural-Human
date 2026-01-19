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
    set_current_spine_path,
    set_current_medialness_map
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
    logger.info(f"Geodesic seed (max medialness): {seed_idx}")
    
    # Sweep 1: Seed -> All Pixels
    # Initialize travel time map with 0 at seed
    phi = np.ones_like(speed_map.data)
    phi[seed_idx] = 0
    # skfmm.travel_time computes geodesic distance on the manifold
    t1 = skfmm.travel_time(np.ma.masked_array(phi, ~mask), speed_map)
    
    if t1 is None: # Safety check for empty/invalid masks
        return np.array([seed_idx[::-1]]) # Return seed as single point (x,y)
    
    # Convert to filled array for safe argmax (masked values become -inf so they're not selected)
    if hasattr(t1, 'filled'):
        t1_for_argmax = t1.filled(-np.inf)
    else:
        t1_for_argmax = np.where(np.isfinite(t1), t1, -np.inf)
        
    # Find Tip: The point furthest from the seed (Geodesic extremum 1)
    tip_idx = np.unravel_index(np.argmax(t1_for_argmax), t1.shape)
    
    # Sweep 2: Tip -> All Pixels (The manifold we will backtrack on)
    phi[:] = 1
    phi[tip_idx] = 0
    t2 = skfmm.travel_time(np.ma.masked_array(phi, ~mask), speed_map)
    
    # Convert to filled array for safe argmax
    if hasattr(t2, 'filled'):
        t2_for_argmax = t2.filled(-np.inf)
    else:
        t2_for_argmax = np.where(np.isfinite(t2), t2, -np.inf)
    
    # Find Tail: The point furthest from the Tip (Geodesic extremum 2)
    tail_idx = np.unravel_index(np.argmax(t2_for_argmax), t2.shape)
    
    # --- Step 2: Backtracking (Gradient Descent) ---
    # Trace the path from Tail back to Tip by following the gradient of t2 "downhill"
    
    # Convert masked array to regular array, filling masked values with large number
    # This ensures gradient descent stays inside the valid mask region
    if hasattr(t2, 'filled'):
        t2_filled = t2.filled(np.inf)
    else:
        t2_filled = np.where(np.isfinite(t2), t2, np.inf)
    
    # Verify tip and tail are deep inside the mask (not near boundary)
    # Compute EDT to measure distance from boundary
    edt = distance_transform_edt(mask)
    min_boundary_dist = 3  # Minimum pixels from boundary
    
    def find_interior_point(idx, t_filled, mask, edt, search_radius=20):
        """Find a valid interior point near idx that's away from mask boundary."""
        r, c = idx
        # Check if current point is valid and interior
        if mask[r, c] and np.isfinite(t_filled[r, c]) and edt[r, c] >= min_boundary_dist:
            return idx
        
        # Search for a point that's both valid and interior
        best_idx = None
        best_score = -np.inf
        for radius in range(1, search_radius + 1):
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < mask.shape[0] and 0 <= nc < mask.shape[1]:
                        if mask[nr, nc] and np.isfinite(t_filled[nr, nc]):
                            # Score based on travel time (want high) and boundary distance (want high)
                            boundary_dist = edt[nr, nc]
                            if boundary_dist >= min_boundary_dist:
                                score = t_filled[nr, nc] + boundary_dist * 0.1
                                if score > best_score:
                                    best_score = score
                                    best_idx = (nr, nc)
            if best_idx is not None:
                return best_idx
        
        # If no interior point found, just find any valid point
        for radius in range(1, search_radius + 1):
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < mask.shape[0] and 0 <= nc < mask.shape[1]:
                        if mask[nr, nc] and np.isfinite(t_filled[nr, nc]):
                            return (nr, nc)
        return idx  # Fallback to original
    
    # Ensure tip is interior
    if not mask[tip_idx] or not np.isfinite(t2_filled[tip_idx]) or edt[tip_idx] < min_boundary_dist:
        logger.warning(f"Tip {tip_idx} is near boundary (edt={edt[tip_idx]:.1f}), finding interior point...")
        tip_idx = find_interior_point(tip_idx, t2_filled, mask, edt)
        logger.info(f"Found interior tip at {tip_idx} (edt={edt[tip_idx]:.1f})")
    
    # Ensure tail is interior
    if not mask[tail_idx] or not np.isfinite(t2_filled[tail_idx]) or edt[tail_idx] < min_boundary_dist:
        logger.warning(f"Tail {tail_idx} is near boundary (edt={edt[tail_idx]:.1f}), finding interior point...")
        tail_idx = find_interior_point(tail_idx, t2_filled, mask, edt)
        logger.info(f"Found interior tail at {tail_idx} (edt={edt[tail_idx]:.1f})")
    
    # Log endpoint detection results
    tip_tail_dist = np.sqrt((tip_idx[0] - tail_idx[0])**2 + (tip_idx[1] - tail_idx[1])**2)
    logger.info(f"Geodesic endpoints: tip={tip_idx}, tail={tail_idx}, distance={tip_tail_dist:.1f}px")
    
    # Get the max travel time for relative threshold (tail is furthest from tip)
    max_travel_time = t2_filled[tail_idx]
    if not np.isfinite(max_travel_time) or max_travel_time <= 0:
        max_travel_time = 1.0
    
    # Use 1% of max travel time as threshold instead of absolute 1.0
    time_threshold = max_travel_time * 0.01
    
    logger.info(f"Geodesic backtrack: tip={tip_idx}, tail={tail_idx}, max_time={max_travel_time:.4f}, threshold={time_threshold:.4f}")
    
    path = []
    current = np.array(tail_idx, dtype=np.float64)
    tip = np.array(tip_idx, dtype=np.float64)
    
    # Parameters for gradient descent
    step_size = 0.5
    max_steps = int(mask.size) # Prevent infinite loops
    
    path.append(current[::-1].copy()) # Store as (x, y) - MUST copy to avoid all points being same
    
    for step_num in range(max_steps):
        # Integer coordinates for indexing
        r, c = int(current[0]), int(current[1])
        
        # Stop if we are close to the tip (travel time near zero relative to max)
        t2_val = t2_filled[r, c]
        if not np.isfinite(t2_val) or t2_val < time_threshold or np.linalg.norm(current - tip) < 1.0:
            logger.info(f"Geodesic backtrack stopped at step {step_num}: t2_val={t2_val:.4f}, dist_to_tip={np.linalg.norm(current - tip):.2f}")
            break
            
        # Compute local gradient (central differences)
        # Handle boundaries by clamping
        r_min, r_max = max(0, r-1), min(mask.shape[0]-1, r+1)
        c_min, c_max = max(0, c-1), min(mask.shape[1]-1, c+1)
        
        # Get values, treating inf as "wall" (don't go there)
        v_r_max = t2_filled[r_max, c]
        v_r_min = t2_filled[r_min, c]
        v_c_max = t2_filled[r, c_max]
        v_c_min = t2_filled[r, c_min]
        
        # If any neighbor is inf, use current value to avoid going that direction
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
            break # Stuck in flat area
            
        # Move "downhill" (against the gradient of distance)
        # Try the step, but validate we stay inside the mask
        new_pos = current - grad * step_size
        
        # Boundary check
        new_pos[0] = np.clip(new_pos[0], 0, mask.shape[0]-1)
        new_pos[1] = np.clip(new_pos[1], 0, mask.shape[1]-1)
        
        new_r, new_c = int(new_pos[0]), int(new_pos[1])
        
        # Check if new position is inside mask with finite travel time
        if not mask[new_r, new_c] or not np.isfinite(t2_filled[new_r, new_c]):
            # Try smaller steps
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
                # Try stepping directly toward tip if gradient fails
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
                # Can't move further, stop here
                break
        
        current = new_pos
        path.append(current[::-1].copy()) # Append (x, y) - MUST copy
        
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

def extract_spine_path_3d(
    mask: np.ndarray,
    depth_map: np.ndarray,
    image_width: int,
    image_height: int,
    center_x: float,
    center_y: float,
    num_points: int = 32
) -> np.ndarray:
    """
    Extract the 3D spine path along the medial axis with depth-based Z inflation.
    
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
        num_points: Number of points to resample the spine to
        
    Returns:
        Nx3 array of [x, y, z_extent] in Blender normalized coordinates
    """
    # Resize depth map to match mask if needed
    if depth_map.shape != mask.shape:
        depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
        depth_pil = depth_pil.resize((mask.shape[1], mask.shape[0]), PILImage.BILINEAR)
        depth_map = np.array(depth_pil).astype(np.float32) / 255.0
    
    # Get min/max depth within the mask for z_extent calculation
    mask_depths = depth_map[mask]
    if len(mask_depths) == 0:
        # Empty mask fallback
        return np.column_stack([
            np.zeros(num_points),
            np.linspace(-0.5, 0.5, num_points),
            np.zeros(num_points)
        ])
    
    min_depth = mask_depths.min()
    max_depth = mask_depths.max()
    depth_range = max_depth - min_depth if max_depth > min_depth else 1.0
    
    # --- Geodesic Spine Extraction ---
    try:
        # 1. Compute Medialness Speed Map
        speed_map = compute_medialness_speed(mask, depth_map)
        
        # Store medialness map for debug visualization
        set_current_medialness_map(speed_map.copy() if hasattr(speed_map, 'copy') else speed_map)
        
        # 2. Extract the Geodesic Ridge (list of x,y coordinates in image space)
        spine_path_xy = extract_geodesic_path(mask, speed_map)
        
        logger.info(f"Geodesic spine extracted: {len(spine_path_xy)} points, "
                    f"x range [{spine_path_xy[:, 0].min():.1f}, {spine_path_xy[:, 0].max():.1f}], "
                    f"y range [{spine_path_xy[:, 1].min():.1f}, {spine_path_xy[:, 1].max():.1f}]")
        
        # Store spine path for debug visualization
        set_current_spine_path(spine_path_xy.copy())
        
    except (ImportError, Exception) as e:
        logger.warning(f"Geodesic extraction failed ({e}), falling back to simple center.")
        # Fallback: create a vertical line down the middle
        y_indices = np.where(np.any(mask, axis=1))[0]
        if len(y_indices) > 0:
            spine_path_xy = np.column_stack([
                np.full(len(y_indices), mask.shape[1] / 2), 
                y_indices
            ])
        else:
            return np.column_stack([
                np.zeros(num_points),
                np.linspace(-0.5, 0.5, num_points),
                np.zeros(num_points)
            ])

    if len(spine_path_xy) < 2:
        return np.column_stack([
            np.zeros(num_points),
            np.linspace(-0.5, 0.5, num_points),
            np.zeros(num_points)
        ])

    # --- Resample the path evenly ---
    spine_resampled = resample_polyline(spine_path_xy, num_points)
    
    # --- Sample depth using bilinear interpolation ---
    sampled_depths = np.array([
        bilinear_sample(depth_map, x, y) 
        for x, y in spine_resampled
    ])
    
    logger.info(f"Sampled depths along spine: min={sampled_depths.min():.4f}, max={sampled_depths.max():.4f}, "
                f"mask depth range: [{min_depth:.4f}, {max_depth:.4f}]")
    
    # --- Compute z_extent: at min_depth -> 0, at max_depth -> depth_range ---
    # z_extent is in 0 to depth_range (typically 0 to ~1)
    z_extent = sampled_depths - min_depth
    
    # --- Convert X,Y from image space to Blender normalized coordinates ---
    # Image coords: X=0..W (right), Y=0..H (down)
    # Blender coords: X centered on center_x, Y flipped and centered on center_y
    
    x_normalized = (spine_resampled[:, 0] - center_x) / image_width
    # Flip Y: image Y down -> Blender Y up
    y_normalized = -(spine_resampled[:, 1] - center_y) / image_height
    
    # z_extent is in depth units (0 to depth_range, typically 0-1)
    # Scale it to be proportional to the normalized coordinates
    # We want max z_extent to produce visible thickness relative to the object size
    # Use a similar scale as X/Y (normalized to image dimensions)
    # The depth_range represents the full "thickness" of the object
    z_normalized = z_extent * 0.5  # Scale factor for visible thickness
    
    logger.info(f"Spine path 3D: x range [{x_normalized.min():.4f}, {x_normalized.max():.4f}], "
                f"y range [{y_normalized.min():.4f}, {y_normalized.max():.4f}], "
                f"z range [{z_normalized.min():.4f}, {z_normalized.max():.4f}], "
                f"depth range [{min_depth:.4f}, {max_depth:.4f}]")
    
    return np.column_stack([x_normalized, y_normalized, z_normalized])


def create_inflated_mesh_from_spine(
    front_contour: np.ndarray,
    spine_path_3d: np.ndarray,
    name: str = "InflatedMesh",
    points_per_half: int = 16,
) -> 'bpy.types.Object':
    """
    Create a mesh from a front contour and a 3D curved spine path.
    
    Unlike create_dual_loop_mesh which forces the side contour to X=0,
    this function allows the spine to curve in 3D space with the actual
    medial axis X,Y coordinates and depth-based Z inflation.
    
    Args:
        front_contour: Front view contour Nx2 in XY plane (Blender normalized coords)
        spine_path_3d: Spine path Mx3 as [x, y, z_extent] where z_extent is the
                       inflation amount (symmetric ±Z from the path)
        name: Name for the mesh object
        points_per_half: Number of points per half-loop
        
    Returns:
        The created Blender mesh object
    """
    from procedural_human.segmentation.operators.mesh_curve_operators import (
        find_axis_crossing_indices,
        split_contour_at_crossings,
        resample_contour,
    )
    
    # Use front_contour as-is (already normalized in execute method)
    # Do NOT call normalize_contour again - that would double-transform and misalign with spine
    front_norm = front_contour
    
    # Find where front contour crosses X=0 (top and bottom poles)
    front_top_cross, front_bottom_cross = find_axis_crossing_indices(front_norm)
    
    # Split front contour at crossings
    front_half1, front_half2 = split_contour_at_crossings(front_norm, front_top_cross, front_bottom_cross)
    
    # Determine which half is left (X < 0) and which is right (X > 0)
    def get_dominant_x_sign(half):
        mid_idx = len(half) // 2
        if mid_idx < len(half):
            return -1 if half[mid_idx, 0] < 0 else 1
        return 0
    
    if get_dominant_x_sign(front_half1) < 0:
        front_left, front_right = front_half1, front_half2
    else:
        front_left, front_right = front_half2, front_half1
    
    # Resample front halves
    front_left_rs = resample_contour(front_left, points_per_half + 2)
    front_right_rs = resample_contour(front_right, points_per_half + 2)
    
    # --- Process 3D spine path ---
    # Resample spine to match points_per_half + 2
    num_spine_points = points_per_half + 2
    
    if len(spine_path_3d) < num_spine_points:
        # Need to interpolate spine
        spine_2d = spine_path_3d[:, :2]  # x, y
        spine_z = spine_path_3d[:, 2]    # z_extent
        
        # Resample the 2D path
        spine_2d_rs = resample_polyline(spine_2d, num_spine_points)
        
        # Interpolate z_extent along the resampled path
        if len(spine_path_3d) >= 2:
            # Compute arc length for original and resampled
            orig_diffs = np.diff(spine_2d, axis=0)
            orig_dist = np.concatenate([[0], np.cumsum(np.sqrt(np.sum(orig_diffs**2, axis=1)))])
            orig_len = orig_dist[-1] if orig_dist[-1] > 0 else 1.0
            
            rs_diffs = np.diff(spine_2d_rs, axis=0)
            rs_dist = np.concatenate([[0], np.cumsum(np.sqrt(np.sum(rs_diffs**2, axis=1)))])
            
            spine_z_rs = np.interp(rs_dist, orig_dist, spine_z)
        else:
            spine_z_rs = np.full(num_spine_points, spine_z[0] if len(spine_z) > 0 else 0)
        
        spine_resampled = np.column_stack([spine_2d_rs, spine_z_rs])
    else:
        spine_resampled = resample_polyline(spine_path_3d[:, :2], num_spine_points)
        # Interpolate z
        orig_diffs = np.diff(spine_path_3d[:, :2], axis=0)
        orig_dist = np.concatenate([[0], np.cumsum(np.sqrt(np.sum(orig_diffs**2, axis=1)))])
        
        rs_diffs = np.diff(spine_resampled, axis=0)
        rs_dist = np.concatenate([[0], np.cumsum(np.sqrt(np.sum(rs_diffs**2, axis=1)))])
        
        spine_z_rs = np.interp(rs_dist, orig_dist, spine_path_3d[:, 2])
        spine_resampled = np.column_stack([spine_resampled, spine_z_rs])
    
    # Keep spine in its original normalized coordinates (same as front contour)
    # This ensures spine overlays correctly on front contour like in debug view
    
    # Build the mesh
    bm = bmesh.new()
    
    # Use spine endpoints as the poles instead of front contour X=0 crossings
    # This ensures the mesh connects at the actual spine tip/tail positions
    spine_tip = spine_resampled[0]   # First point (tip in image coords, after path reversal)
    spine_tail = spine_resampled[-1]  # Last point (tail)
    
    # Create pole vertices at spine endpoints (Z=0 at poles)
    top_vert = bm.verts.new((spine_tip[0], spine_tip[1], 0))
    bottom_vert = bm.verts.new((spine_tail[0], spine_tail[1], 0))
    
    # Find the front contour points closest to spine endpoints for proper connection
    def find_closest_contour_idx(contour, point_xy):
        """Find index of closest point on contour to given x,y."""
        dists = np.sqrt((contour[:, 0] - point_xy[0])**2 + (contour[:, 1] - point_xy[1])**2)
        return np.argmin(dists)
    
    # Get full front contour (before splitting)
    # We need to resample based on spine endpoints, not X=0 crossings
    tip_idx_left = find_closest_contour_idx(front_left, spine_tip[:2])
    tip_idx_right = find_closest_contour_idx(front_right, spine_tip[:2])
    tail_idx_left = find_closest_contour_idx(front_left, spine_tail[:2])
    tail_idx_right = find_closest_contour_idx(front_right, spine_tail[:2])
    
    # Resample front halves to match spine point count
    front_left_rs = resample_contour(front_left, points_per_half + 2)
    front_right_rs = resample_contour(front_right, points_per_half + 2)
    
    # Front left vertices (X < 0, Z = 0)
    front_left_verts = []
    for i in range(1, len(front_left_rs) - 1):
        x, y = front_left_rs[i]
        v = bm.verts.new((x, y, 0))
        front_left_verts.append(v)
    
    # Front right vertices (X > 0, Z = 0)
    front_right_verts = []
    for i in range(1, len(front_right_rs) - 1):
        x, y = front_right_rs[i]
        v = bm.verts.new((x, y, 0))
        front_right_verts.append(v)
    
    # Spine back vertices (Z < 0, following curved path with actual coordinates)
    spine_back_verts = []
    for i in range(1, len(spine_resampled) - 1):
        spine_x = spine_resampled[i, 0]
        spine_y = spine_resampled[i, 1]  # Use actual Y, not rescaled
        z_ext = spine_resampled[i, 2]
        v = bm.verts.new((spine_x, spine_y, -z_ext))
        spine_back_verts.append(v)
    
    # Spine front vertices (Z > 0, following curved path with actual coordinates)
    spine_front_verts = []
    for i in range(1, len(spine_resampled) - 1):
        spine_x = spine_resampled[i, 0]
        spine_y = spine_resampled[i, 1]  # Use actual Y, not rescaled
        z_ext = spine_resampled[i, 2]
        v = bm.verts.new((spine_x, spine_y, +z_ext))
        spine_front_verts.append(v)
    
    bm.verts.ensure_lookup_table()
    
    # Create 4 quadrant faces
    # Q1: front_left + spine_back
    q1_verts = [top_vert] + front_left_verts + [bottom_vert] + list(reversed(spine_back_verts))
    if len(q1_verts) >= 3:
        try:
            bm.faces.new(q1_verts)
        except ValueError as e:
            logger.warning(f"Could not create Q1 face: {e}")
    
    # Q2: spine_front + front_left (reversed)
    q2_verts = [top_vert] + spine_front_verts + [bottom_vert] + list(reversed(front_left_verts))
    if len(q2_verts) >= 3:
        try:
            bm.faces.new(q2_verts)
        except ValueError as e:
            logger.warning(f"Could not create Q2 face: {e}")
    
    # Q3: front_right + spine_front (reversed)
    q3_verts = [top_vert] + front_right_verts + [bottom_vert] + list(reversed(spine_front_verts))
    if len(q3_verts) >= 3:
        try:
            bm.faces.new(q3_verts)
        except ValueError as e:
            logger.warning(f"Could not create Q3 face: {e}")
    
    # Q4: spine_back + front_right (reversed)
    q4_verts = [top_vert] + spine_back_verts + [bottom_vert] + list(reversed(front_right_verts))
    if len(q4_verts) >= 3:
        try:
            bm.faces.new(q4_verts)
        except ValueError as e:
            logger.warning(f"Could not create Q4 face: {e}")
    
    # Create mesh data
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    
    # Create object
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
            
            # Extract 3D spine path with curved medial axis and depth-based Z inflation
            spine_path_3d = extract_spine_path_3d(
                mask,
                depth_map,
                image_width,
                image_height,
                center_x,
                center_y,
                num_points=self.points_per_half * 2 + 2
            )
            
            # Apply depth scale to Z extent
            spine_path_3d[:, 2] *= self.depth_scale
            
            # Create the mesh using the new inflated mesh function
            obj = create_inflated_mesh_from_spine(
                front_contour_norm,
                spine_path_3d,
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
