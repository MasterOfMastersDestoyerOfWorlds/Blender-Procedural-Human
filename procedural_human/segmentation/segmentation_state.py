"""
State management for segmentation data to avoid circular imports.
"""

import numpy as np

# Global state variables
_current_masks = []
_current_image = None
_current_medialness_map = None
_current_hessian_map = None
_current_ridge_curves = None
_current_spine_path = None
_current_depth_map = None

def get_current_masks():
    """Get the currently stored segmentation masks."""
    return _current_masks

def set_masks_state(masks):
    """Set the segmentation masks state."""
    global _current_masks
    _current_masks = masks

def get_current_image_state():
    """Get the currently stored image."""
    return _current_image

def set_image_state(image):
    """Set the image state."""
    global _current_image
    _current_image = image

def get_current_medialness_map():
    """Get the currently stored medialness/speed map."""
    return _current_medialness_map

def set_current_medialness_map(medialness_map):
    """Store the medialness/speed map for debug visualization."""
    global _current_medialness_map
    _current_medialness_map = medialness_map

def get_current_hessian_map():
    """Get the currently stored Hessian ridge map."""
    return _current_hessian_map

def set_current_hessian_map(hessian_map):
    """Store the Hessian ridge map for debug visualization."""
    global _current_hessian_map
    _current_hessian_map = hessian_map

def get_current_ridge_curves():
    """Get the currently stored ridge curves."""
    return _current_ridge_curves

def set_current_ridge_curves(curves):
    """Store the ridge curves for debug visualization."""
    global _current_ridge_curves
    _current_ridge_curves = curves

def get_current_spine_path():
    """Get the currently stored spine path."""
    return _current_spine_path

def set_current_spine_path(spine_path):
    """Store the spine path for debug visualization."""
    global _current_spine_path
    _current_spine_path = spine_path

def get_current_depth_map():
    """Get the currently stored depth map."""
    return _current_depth_map

def set_current_depth_map(depth_map):
    """Store the depth map for debug visualization."""
    global _current_depth_map
    _current_depth_map = depth_map
