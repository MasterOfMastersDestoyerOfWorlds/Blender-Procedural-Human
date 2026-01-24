import bpy
import numpy as np
from bpy.types import Operator, PropertyGroup, UIList
from bpy.props import (
    StringProperty, FloatProperty, BoolProperty, IntProperty,
    FloatVectorProperty, CollectionProperty, PointerProperty
)
from PIL import Image as PILImage
from matplotlib.cm import get_cmap

def apply_medialness_overlay(image, medialness_map, colormap='hot'):
    """
    Apply a medialness map overlay onto a Blender image.
    
    Args:
        image: Blender image object
        medialness_map: 2D numpy array of medialness values (can be masked array)
        colormap: Matplotlib colormap name
    """
    if medialness_map is None:
        return
    
    width, height = image.size
    if hasattr(medialness_map, 'filled'):
        data = medialness_map.filled(0)
        mask = medialness_map.mask if hasattr(medialness_map, 'mask') else np.zeros_like(data, dtype=bool)
    else:
        data = medialness_map
        mask = np.zeros_like(data, dtype=bool)
    if data.shape[0] != height or data.shape[1] != width:
        data_img = PILImage.fromarray((data * 255 / max(data.max(), 1e-6)).astype(np.uint8))
        data_img = data_img.resize((width, height), PILImage.BILINEAR)
        data = np.array(data_img).astype(np.float32) / 255.0
        
        mask_img = PILImage.fromarray((mask.astype(np.uint8) * 255))
        mask_img = mask_img.resize((width, height), PILImage.NEAREST)
        mask = np.array(mask_img) > 127
    data_min = data[~mask].min() if np.any(~mask) else 0
    data_max = data[~mask].max() if np.any(~mask) else 1
    if data_max > data_min:
        data_norm = (data - data_min) / (data_max - data_min)
    else:
        data_norm = np.zeros_like(data)
    try:
        
        cmap = get_cmap(colormap)
        colored = cmap(data_norm)[:, :, :3]  # RGB only
    except ImportError:
        colored = np.zeros((height, width, 3))
        colored[:, :, 0] = np.clip(data_norm * 3, 0, 1)  # Red
        colored[:, :, 1] = np.clip(data_norm * 3 - 1, 0, 1)  # Green
        colored[:, :, 2] = np.clip(data_norm * 3 - 2, 0, 1)  # Blue
    colored = np.flipud(colored)
    mask_flipped = np.flipud(mask)
    pixels = np.array(image.pixels[:]).reshape(height, width, 4)
    for c in range(3):
        channel = colored[:, :, c]
        channel[mask_flipped] = pixels[:, :, c][mask_flipped]  # Keep original where masked
        pixels[:, :, c] = channel
    
    image.pixels[:] = pixels.flatten()
    image.update()
