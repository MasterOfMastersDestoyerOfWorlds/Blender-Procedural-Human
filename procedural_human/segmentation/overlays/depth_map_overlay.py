import bpy
import numpy as np
from PIL import Image as PILImage
import matplotlib.cm as cm


_current_depth_map = None  # Store depth map
def get_current_depth_map():
    """Get the currently stored depth map."""
    return _current_depth_map


def set_current_depth_map(depth_map):
    """Store the depth map for later use."""
    global _current_depth_map
    _current_depth_map = depth_map

def apply_depth_overlay(image, depth_map, colormap='viridis'):
    """
    Apply a depth map overlay onto a Blender image.
    
    Args:
        image: Blender image to modify
        depth_map: Numpy array of depth values (H, W) normalized 0-1
        colormap: Colormap name ('viridis', 'plasma', 'inferno', 'magma', or 'grayscale')
    """
    if depth_map is None or image is None:
        return
    
    width, height = image.size
    if depth_map.shape[0] != height or depth_map.shape[1] != width:
        depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
        depth_pil = depth_pil.resize((width, height), PILImage.BILINEAR)
        depth_map = np.array(depth_pil).astype(np.float32) / 255.0
    depth_flipped = np.flipud(depth_map)
    if colormap == 'grayscale':
        depth_rgb = np.stack([depth_flipped, depth_flipped, depth_flipped], axis=2)
    else:
        try:
            cmap = cm.get_cmap(colormap)
            depth_rgb = cmap(depth_flipped)[:, :, :3]  # RGBA -> RGB
        except ImportError:
            depth_rgb = np.stack([depth_flipped, depth_flipped, depth_flipped], axis=2)
    pixels = np.array(image.pixels[:]).reshape((height, width, 4))
    alpha = 1.0
    pixels[:, :, :3] = pixels[:, :, :3] * (1 - alpha) + depth_rgb * alpha
    image.pixels[:] = pixels.flatten().tolist()
    image.update()
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.tag_redraw()