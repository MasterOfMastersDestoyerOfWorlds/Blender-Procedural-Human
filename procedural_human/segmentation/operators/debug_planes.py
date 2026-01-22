import bpy
import numpy as np
from PIL import Image as PILImage
import logging
import importlib.util
import os

from procedural_human.segmentation.overlays.depth_map_overlay import get_current_depth_map
from procedural_human.segmentation.overlays.image_overlay import get_original_image_pixels
from procedural_human.segmentation.segmentation_state import get_current_masks

logger = logging.getLogger(__name__)

def update_debug_planes_visibility_callback(self, context):
    """Callback for show_debug_planes property update.
    Args:
        self: The PropertyGroup or Scene
        context: The Blender context
    """
    update_debug_planes_visibility(context)


def get_active_image(context):
    """Get the currently active image in the IMAGE_EDITOR."""
    for area in context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            for space in area.spaces:
                if space.type == 'IMAGE_EDITOR' and space.image:
                    return space.image
    return None


def update_image_pixels(image_name, width, height, pixels):
    """Update or create a Blender image with given pixels."""
    img = bpy.data.images.get(image_name)
    if img is None or img.size[0] != width or img.size[1] != height:
        if img:
            bpy.data.images.remove(img)
        img = bpy.data.images.new(image_name, width=width, height=height, alpha=True)
    
    if len(pixels) == width * height * 4:
        img.pixels[:] = pixels
        img.update()
    return img


def get_debug_plane_utils():
    """Import debug_plane utils dynamically."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        module_path = os.path.join(base_dir, "procedural_human", "novel_view_gen", "Hunyuan3D-2", "hy3dgen", "texgen", "utils", "debug_plane.py")
        
        if not os.path.exists(module_path):
            logger.error(f"Debug plane utility not found at {module_path}")
            return None
            
        spec = importlib.util.spec_from_file_location("debug_plane_utils", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        logger.error(f"Failed to load debug plane utils: {e}")
        return None


def create_debug_planes(context, image, masks):
    """Create or update debug planes for visualization."""
    if not context.scene.show_debug_planes:
        return
        
    camera = context.scene.camera
    if not camera:
        return
    if not image:
        return
    
    width, height = image.size
    orig_pixels = get_original_image_pixels()
    if orig_pixels is None:
        orig_pixels = np.array(image.pixels[:])
    
    img_orig = update_image_pixels("Debug_Original_Img", width, height, orig_pixels)
    img_depth = None
    depth_map = get_current_depth_map()
    if depth_map is not None:
        d_map = depth_map
        if depth_map.shape[0] != height or depth_map.shape[1] != width:
            depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
            depth_pil = depth_pil.resize((width, height), PILImage.BILINEAR)
            d_map = np.array(depth_pil).astype(np.float32) / 255.0
            
        d_flipped = np.flipud(d_map)
        d_flat = d_flipped.flatten()
        pixels_depth = np.zeros(width * height * 4, dtype=np.float32)
        pixels_depth[0::4] = d_flat # R
        pixels_depth[1::4] = d_flat # G
        pixels_depth[2::4] = d_flat # B
        pixels_depth[3::4] = 1.0    # A
        
        img_depth = update_image_pixels("Debug_Depth_Img", width, height, pixels_depth.tolist())
    img_masks = None
    if masks:
        pixels_masks = np.zeros((height, width, 4), dtype=np.float32)
        settings = context.scene.segmentation_mask_settings
        
        for item in settings.masks:
            if item.enabled and 0 <= item.mask_index < len(masks):
                mask = masks[item.mask_index]
                if mask.shape[0] != height or mask.shape[1] != width:
                     mask_pil = PILImage.fromarray(mask.astype(np.uint8) * 255)
                     mask_pil = mask_pil.resize((width, height), PILImage.NEAREST)
                     mask = np.array(mask_pil) > 127
                
                mask_flipped = np.flipud(mask)
                color = np.array(item.color)
                mask_bool = mask_flipped > 0
                pixels_masks[mask_bool] = color
        
        img_masks = update_image_pixels("Debug_Masks_Img", width, height, pixels_masks.flatten().tolist())
    utils = get_debug_plane_utils()
    if utils:
        utils.create_debug_plane(context, "DebugPlane_Original", img_orig, align_to_camera=True, z_offset=0.0, is_overlay=False)
        utils.create_debug_plane(context, "DebugPlane_Depth", img_depth, align_to_camera=True, z_offset=0.05, is_overlay=False)
        utils.create_debug_plane(context, "DebugPlane_Masks", img_masks, align_to_camera=True, z_offset=0.1, is_overlay=True)


def update_debug_planes_visibility(context, image=None, masks=None):
    """Update visibility of debug planes based on view mode."""
    if image is None:
        image = get_active_image(context)
    if masks is None:
        masks = get_current_masks()

    planes = ["DebugPlane_Original", "DebugPlane_Depth", "DebugPlane_Masks"]
    
    if not context.scene.show_debug_planes:
        for name in planes:
            obj = bpy.data.objects.get(name)
            if obj:
                obj.hide_viewport = True
                obj.hide_render = True
        return
    create_debug_planes(context, image, masks)
    
    mode = context.scene.get("segmentation_view_mode", "MASKS")
    vis = {
        "DebugPlane_Original": True,
        "DebugPlane_Depth": (mode == "DEPTH"),
        "DebugPlane_Masks": (mode == "MASKS")
    }
    
    for name, visible in vis.items():
        obj = bpy.data.objects.get(name)
        if obj:
            should_be_visible = visible
            
            if should_be_visible:
                if obj.hide_viewport: obj.hide_viewport = False
                if obj.hide_render: obj.hide_render = False
            else:
                if not obj.hide_viewport: obj.hide_viewport = True
                if not obj.hide_render: obj.hide_render = True
