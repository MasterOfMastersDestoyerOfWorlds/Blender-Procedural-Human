"""
Segmentation module for curve extraction from images using SAM3.

This module provides:
- Yandex image search integration
- SAM3 segmentation with point, box, and text prompts
- Mask to curve conversion
- Curve insertion into 3D scene
- Custom workspace layout for the segmentation workflow

Usage:
    1. Open the Curve Segmentation workspace via the operator
    2. Load an image from disk or search Yandex
    3. Use SAM3 to segment objects in the image
    4. Convert segmentation masks to Blender curves
    5. Insert curves into the 3D scene with LoftSpheriod modifier
"""

__all__ = [
    "SAM3Manager",
    "YandexImageSearch", 
    "mask_to_curves",
    "masks_to_curves",
    "CurveSegmentationWorkspace",
    "register_segmentation_properties",
    "unregister_segmentation_properties",
]


from procedural_human.image_search.search_panel import register_search_properties
from procedural_human.image_search.search_asset_manager import unregister_search_properties
from procedural_human.image_search.yandex_search import YandexImageSearch
from procedural_human.segmentation.mask_to_curve import mask_to_curves, masks_to_curves
from procedural_human.segmentation.operators.segmentation_operators import register_mask_properties, unregister_mask_properties
from procedural_human.segmentation.sam_integration import SAM3Manager
from procedural_human.segmentation.workspace import CurveSegmentationWorkspace


def register_segmentation_properties():
    """Register all segmentation-related properties."""
    register_search_properties()
    register_mask_properties()


def unregister_segmentation_properties():
    """Unregister all segmentation-related properties."""
    unregister_mask_properties()
    unregister_search_properties()


def __getattr__(name):
    """Lazy import for module attributes."""
    if name == "SAM3Manager":
        return SAM3Manager
    elif name == "YandexImageSearch":
        return YandexImageSearch
    elif name == "mask_to_curves":
        return mask_to_curves
    elif name == "masks_to_curves":
        return masks_to_curves
    elif name == "CurveSegmentationWorkspace":
        return CurveSegmentationWorkspace
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


