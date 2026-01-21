"""
Shared utilities for segmentation and mesh generation operators.
"""

import numpy as np
import cv2
from procedural_human.logger import logger

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


def simplify_contour(contour: np.ndarray, epsilon: float = 0.01) -> np.ndarray:
    """
    Simplify a contour using the Douglas-Peucker algorithm.
    
    Args:
        contour: Contour array with shape (N, 2)
        epsilon: Approximation accuracy as fraction of arc length (0 = no simplification)
        
    Returns:
        Simplified contour array
    """
    if epsilon <= 0 or len(contour) < 3:
        return contour
    
    try:
        # Calculate epsilon based on arc length
        diffs = np.diff(contour, axis=0)
        arc_length = np.sum(np.sqrt(np.sum(diffs**2, axis=1)))
        actual_epsilon = epsilon * arc_length
        
        # Use cv2.approxPolyDP for Douglas-Peucker simplification
        approx = cv2.approxPolyDP(
            contour.reshape(-1, 1, 2).astype(np.float32), 
            actual_epsilon, 
            closed=True
        )
        
        simplified = approx.reshape(-1, 2)
        logger.info(f"Simplified contour: {len(contour)} -> {len(simplified)} points (epsilon={epsilon:.4f})")
        return simplified
    except Exception as e:
        logger.warning(f"Contour simplification failed: {e}")
        return contour


def simplify_polyline(points: np.ndarray, epsilon: float = 0.01) -> np.ndarray:
    """
    Simplify an open polyline using the Douglas-Peucker algorithm.
    
    Args:
        points: Polyline array with shape (N, 2) or (N, 3)
        epsilon: Approximation accuracy as fraction of arc length (0 = no simplification)
        
    Returns:
        Simplified polyline array
    """
    if epsilon <= 0 or len(points) < 3:
        return points
    
    try:
        # Handle 3D points by simplifying only X,Y and keeping Z
        if points.shape[1] == 3:
            xy = points[:, :2]
            z = points[:, 2]
        else:
            xy = points
            z = None
        
        # Calculate epsilon based on arc length
        diffs = np.diff(xy, axis=0)
        arc_length = np.sum(np.sqrt(np.sum(diffs**2, axis=1)))
        actual_epsilon = epsilon * arc_length
        
        # Use cv2.approxPolyDP for Douglas-Peucker simplification (open curve)
        approx = cv2.approxPolyDP(
            xy.reshape(-1, 1, 2).astype(np.float32), 
            actual_epsilon, 
            closed=False
        )
        
        simplified_xy = approx.reshape(-1, 2)
        
        if z is not None:
            # Interpolate Z values for the simplified points
            # Find the parameter along the original curve for each simplified point
            orig_diffs = np.diff(xy, axis=0)
            orig_dist = np.concatenate([[0], np.cumsum(np.sqrt(np.sum(orig_diffs**2, axis=1)))])
            
            simplified_z = []
            for pt in simplified_xy:
                # Find closest point on original curve
                dists = np.sqrt(np.sum((xy - pt)**2, axis=1))
                closest_idx = np.argmin(dists)
                simplified_z.append(z[closest_idx])
            
            simplified = np.column_stack([simplified_xy, simplified_z])
        else:
            simplified = simplified_xy
        
        logger.info(f"Simplified polyline: {len(points)} -> {len(simplified)} points (epsilon={epsilon:.4f})")
        return simplified
    except Exception as e:
        logger.warning(f"Polyline simplification failed: {e}")
        return points


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
