"""
Mask to Curve conversion utilities.

This module provides functions to convert binary segmentation masks
into Blender curve objects.
"""

import bpy
import numpy as np
from typing import List, Tuple, Optional
from mathutils import Vector

from procedural_human.logger import logger


def find_contours(mask: np.ndarray) -> List[np.ndarray]:
    """
    Find contours in a binary mask using OpenCV.
    
    Args:
        mask: Binary mask array (2D boolean or uint8)
        
    Returns:
        List of contour arrays, each with shape (N, 2)
    """
    try:
        import cv2
    except ImportError:
        logger.error("OpenCV not installed. Please run: pip install opencv-python")
        return []
    if mask.dtype == bool:
        mask_uint8 = mask.astype(np.uint8) * 255
    else:
        mask_uint8 = mask.astype(np.uint8)
    contours, hierarchy = cv2.findContours(
        mask_uint8, 
        cv2.RETR_EXTERNAL,  # Only external contours
        cv2.CHAIN_APPROX_SIMPLE  # Compress horizontal/vertical segments
    )
    result = []
    for contour in contours:
        points = contour.reshape(-1, 2)
        if len(points) >= 3:  # Need at least 3 points for a valid curve
            result.append(points)
    
    return result


def simplify_contour(
    contour: np.ndarray, 
    epsilon: float = 0.01
) -> np.ndarray:
    """
    Simplify a contour using the Douglas-Peucker algorithm.
    
    Args:
        contour: Contour array with shape (N, 2)
        epsilon: Approximation accuracy as fraction of arc length
        
    Returns:
        Simplified contour array
    """
    try:
        import cv2
    except ImportError:
        logger.warning("OpenCV not available for contour simplification")
        return contour
    arc_length = cv2.arcLength(contour.reshape(-1, 1, 2).astype(np.float32), closed=True)
    actual_epsilon = epsilon * arc_length
    approx = cv2.approxPolyDP(
        contour.reshape(-1, 1, 2).astype(np.float32), 
        actual_epsilon, 
        closed=True
    )
    
    return approx.reshape(-1, 2)


def contour_to_curve(
    contour: np.ndarray,
    image_width: int,
    image_height: int,
    name: str = "SegmentCurve",
    scale: float = 1.0,
    center: bool = True,
    flip_y: bool = True
) -> bpy.types.Object:
    """
    Convert a 2D contour to a Blender curve object.
    
    Args:
        contour: Contour array with shape (N, 2) in pixel coordinates
        image_width: Width of the source image
        image_height: Height of the source image
        name: Name for the curve object
        scale: Scale factor for the curve
        center: Whether to center the curve at origin
        flip_y: Whether to flip Y axis (image Y is typically inverted)
        
    Returns:
        The created Blender curve object
    """
    normalized = contour.astype(np.float32).copy()
    normalized[:, 0] = normalized[:, 0] / image_width - 0.5
    normalized[:, 1] = normalized[:, 1] / image_height - 0.5
    
    if flip_y:
        normalized[:, 1] = -normalized[:, 1]
    normalized *= scale
    if center:
        centroid = normalized.mean(axis=0)
        normalized -= centroid
    curve_data = bpy.data.curves.new(name=name, type='CURVE')
    curve_data.dimensions = '2D'
    curve_data.resolution_u = 12
    spline = curve_data.splines.new(type='BEZIER')
    spline.bezier_points.add(len(normalized) - 1)  # -1 because one point already exists
    spline.use_cyclic_u = True  # Close the curve
    for i, point in enumerate(normalized):
        bp = spline.bezier_points[i]
        bp.co = Vector((point[0], point[1], 0.0))
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    curve_obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(curve_obj)
    
    return curve_obj


def mask_to_curves(
    mask: np.ndarray,
    image_width: Optional[int] = None,
    image_height: Optional[int] = None,
    name_prefix: str = "Segment",
    simplify: bool = True,
    simplify_epsilon: float = 0.005,
    min_points: int = 4,
    scale: float = 1.0
) -> List[bpy.types.Object]:
    """
    Convert a binary segmentation mask to Blender curve objects.
    
    This function:
    1. Finds contours in the mask using OpenCV
    2. Optionally simplifies the contours
    3. Creates Blender curve objects from the contours
    
    Args:
        mask: Binary mask array (2D)
        image_width: Width of source image (uses mask width if not provided)
        image_height: Height of source image (uses mask height if not provided)
        name_prefix: Prefix for curve object names
        simplify: Whether to simplify contours
        simplify_epsilon: Simplification factor (higher = more simplified)
        min_points: Minimum points required for a valid curve
        scale: Scale factor for curves
        
    Returns:
        List of created Blender curve objects
    """
    if image_width is None:
        image_width = mask.shape[1]
    if image_height is None:
        image_height = mask.shape[0]
    
    logger.info(f"Converting mask ({image_width}x{image_height}) to curves...")
    contours = find_contours(mask)
    logger.info(f"Found {len(contours)} contours")
    
    curves = []
    for i, contour in enumerate(contours):
        if simplify:
            contour = simplify_contour(contour, simplify_epsilon)
        if len(contour) < min_points:
            logger.debug(f"Skipping contour {i} with only {len(contour)} points")
            continue
        curve_name = f"{name_prefix}_{i:03d}"
        curve_obj = contour_to_curve(
            contour,
            image_width,
            image_height,
            name=curve_name,
            scale=scale
        )
        curves.append(curve_obj)
        logger.info(f"Created curve: {curve_name} ({len(contour)} points)")
    
    return curves


def masks_to_curves(
    masks: List[np.ndarray],
    image_width: Optional[int] = None,
    image_height: Optional[int] = None,
    name_prefix: str = "Segment",
    **kwargs
) -> List[bpy.types.Object]:
    """
    Convert multiple segmentation masks to Blender curve objects.
    
    Args:
        masks: List of binary mask arrays
        image_width: Width of source image
        image_height: Height of source image
        name_prefix: Prefix for curve object names
        **kwargs: Additional arguments passed to mask_to_curves
        
    Returns:
        List of all created Blender curve objects
    """
    all_curves = []
    
    for mask_idx, mask in enumerate(masks):
        mask_prefix = f"{name_prefix}_{mask_idx:02d}"
        curves = mask_to_curves(
            mask,
            image_width=image_width,
            image_height=image_height,
            name_prefix=mask_prefix,
            **kwargs
        )
        all_curves.extend(curves)
    
    logger.info(f"Created {len(all_curves)} curves from {len(masks)} masks")
    return all_curves


