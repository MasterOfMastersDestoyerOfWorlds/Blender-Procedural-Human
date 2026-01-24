
from procedural_human.segmentation.overlays.medialness_overlay import apply_medialness_overlay

def apply_hessian_overlay(image, hessian_map, colormap='viridis'):
    """
    Apply a Hessian ridge map overlay onto a Blender image.
    """
    if hessian_map is None:
        return
    apply_medialness_overlay(image, hessian_map, colormap=colormap)
