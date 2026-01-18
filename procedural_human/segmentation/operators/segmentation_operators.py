"""
SAM3 Segmentation operators for the segmentation workflow.
"""

import bpy
import numpy as np
from bpy.types import Operator, PropertyGroup, UIList
from bpy.props import (
    StringProperty, FloatProperty, BoolProperty, IntProperty,
    FloatVectorProperty, CollectionProperty, PointerProperty
)

from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import logger


# ============================================================================
# Mask Item PropertyGroup and UIList
# ============================================================================

class SegmentationMaskItem(PropertyGroup):
    """Property group for individual segmentation mask data."""
    
    enabled: BoolProperty(
        name="Enabled",
        description="Include this mask in operations",
        default=True
    )
    
    color: FloatVectorProperty(
        name="Color",
        description="Display color for this mask",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.0, 0.8, 0.3, 0.5)
    )
    
    area: IntProperty(
        name="Area",
        description="Number of pixels in this mask",
        default=0
    )
    
    # Index into the global _current_masks list
    mask_index: IntProperty(
        name="Mask Index",
        default=-1
    )


class SEGMENTATION_UL_masks(UIList):
    """UIList for displaying segmentation masks."""
    
    bl_idname = "SEGMENTATION_UL_masks"
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            
            # Enable/disable checkbox
            row.prop(item, "enabled", text="", icon='CHECKBOX_HLT' if item.enabled else 'CHECKBOX_DEHLT')
            
            # Color swatch
            row.prop(item, "color", text="")
            
            # Mask name/index
            row.label(text=f"Mask {index + 1}")
            
            # Area info (compact)
            if item.area > 0:
                if item.area >= 1000000:
                    area_str = f"{item.area / 1000000:.1f}M px"
                elif item.area >= 1000:
                    area_str = f"{item.area / 1000:.1f}K px"
                else:
                    area_str = f"{item.area} px"
                row.label(text=area_str)
        
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.prop(item, "enabled", text="", icon='CHECKBOX_HLT' if item.enabled else 'CHECKBOX_DEHLT')


class SegmentationMaskSettings(PropertyGroup):
    """Scene-level settings for segmentation masks."""
    
    masks: CollectionProperty(type=SegmentationMaskItem)
    active_mask_index: IntProperty(name="Active Mask Index", default=0)


def generate_distinct_colors(n: int) -> list:
    """Generate n visually distinct colors using HSV rotation."""
    colors = []
    for i in range(n):
        # Rotate through hue, with some variation in saturation/value
        hue = (i * 0.618033988749895) % 1.0  # Golden ratio for good distribution
        saturation = 0.7 + (i % 3) * 0.1  # Vary saturation slightly
        value = 0.9 - (i % 2) * 0.1  # Vary value slightly
        
        # HSV to RGB conversion
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        colors.append((r, g, b, 0.5))  # Add alpha
    
    return colors


def sync_masks_to_collection(context, masks: list):
    """
    Synchronize the global masks list with the scene's CollectionProperty.
    
    Args:
        context: Blender context
        masks: List of numpy mask arrays
    """
    settings = context.scene.segmentation_mask_settings
    
    # Clear existing items
    settings.masks.clear()
    
    # Generate colors for masks
    colors = generate_distinct_colors(len(masks))
    
    # Add new items
    for i, mask in enumerate(masks):
        item = settings.masks.add()
        item.enabled = True
        item.color = colors[i] if i < len(colors) else (0.5, 0.5, 0.5, 0.5)
        item.area = int(np.sum(mask))
        item.mask_index = i
    
    # Reset active index
    settings.active_mask_index = 0 if len(masks) > 0 else -1


def get_enabled_mask_indices(context) -> list:
    """Get list of indices for enabled masks."""
    settings = context.scene.segmentation_mask_settings
    return [item.mask_index for item in settings.masks if item.enabled and item.mask_index >= 0]


def get_mask_colors(context) -> list:
    """Get list of colors for all masks."""
    settings = context.scene.segmentation_mask_settings
    return [tuple(item.color) for item in settings.masks]


# ============================================================================
# Mask Selection Operators
# ============================================================================

@procedural_operator
class SelectAllMasksOperator(Operator):
    """Select all segmentation masks"""
    
    bl_idname = "segmentation.select_all_masks"
    bl_label = "Select All Masks"
    bl_description = "Enable all segmentation masks"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.segmentation_mask_settings
        for item in settings.masks:
            item.enabled = True
        
        # Refresh overlay
        refresh_mask_overlay(context)
        return {'FINISHED'}


@procedural_operator
class DeselectAllMasksOperator(Operator):
    """Deselect all segmentation masks"""
    
    bl_idname = "segmentation.deselect_all_masks"
    bl_label = "Deselect All Masks"
    bl_description = "Disable all segmentation masks"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.segmentation_mask_settings
        for item in settings.masks:
            item.enabled = False
        
        # Refresh overlay
        refresh_mask_overlay(context)
        return {'FINISHED'}


@procedural_operator
class InvertMaskSelectionOperator(Operator):
    """Invert mask selection"""
    
    bl_idname = "segmentation.invert_mask_selection"
    bl_label = "Invert Selection"
    bl_description = "Toggle enabled state for all masks"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.segmentation_mask_settings
        for item in settings.masks:
            item.enabled = not item.enabled
        
        # Refresh overlay
        refresh_mask_overlay(context)
        return {'FINISHED'}


@procedural_operator
class RefreshMaskOverlayOperator(Operator):
    """Refresh the mask overlay display"""
    
    bl_idname = "segmentation.refresh_overlay"
    bl_label = "Refresh Overlay"
    bl_description = "Update the mask color overlay in the Image Editor"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        refresh_mask_overlay(context)
        self.report({'INFO'}, "Mask overlay refreshed")
        return {'FINISHED'}


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
    
    # Resize depth map to match image if needed
    if depth_map.shape[0] != height or depth_map.shape[1] != width:
        from PIL import Image as PILImage
        depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
        depth_pil = depth_pil.resize((width, height), PILImage.BILINEAR)
        depth_map = np.array(depth_pil).astype(np.float32) / 255.0
    
    # Flip depth map vertically to match Blender's coordinate system
    depth_flipped = np.flipud(depth_map)
    
    # Convert depth to RGB colormap
    if colormap == 'grayscale':
        depth_rgb = np.stack([depth_flipped, depth_flipped, depth_flipped], axis=2)
    else:
        try:
            import matplotlib.cm as cm
            cmap = cm.get_cmap(colormap)
            depth_rgb = cmap(depth_flipped)[:, :, :3]  # RGBA -> RGB
        except ImportError:
            # Fallback to grayscale if matplotlib not available
            depth_rgb = np.stack([depth_flipped, depth_flipped, depth_flipped], axis=2)
    
    # Get current pixels as numpy array
    pixels = np.array(image.pixels[:]).reshape((height, width, 4))
    
    # Blend depth map with original image
    # Use 1.0 alpha (opaque) to show just the depth map, as requested by user
    alpha = 1.0
    pixels[:, :, :3] = pixels[:, :, :3] * (1 - alpha) + depth_rgb * alpha
    
    # Update the image
    image.pixels[:] = pixels.flatten().tolist()
    image.update()
    
    # Redraw Image Editors
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.tag_redraw()


def refresh_mask_overlay(context):
    """Refresh the overlay with current view mode (masks, depth, or none)."""
    from procedural_human.segmentation.operators.segmentation_operators import (
        get_current_masks, get_active_image, get_original_image_pixels, 
        restore_original_image, get_current_depth_map, store_original_image
    )
    
    image = get_active_image(context)
    if image is None:
        return
    
    # Ensure we have the original saved before we do anything
    # If the original is not stored yet, store the current state as original
    # This prevents issues where switching views without segmentation dirties the image permanently
    stored_pixels = get_original_image_pixels()
    if stored_pixels is None:
        store_original_image(image)
    else:
        # Check if image dimensions match stored pixels
        # If not, the user likely switched images, so treat this as a new image
        current_len = image.size[0] * image.size[1] * 4
        if len(stored_pixels) != current_len:
            store_original_image(image)
    
    # Always restore original image first to clear previous overlays
    restore_original_image(image)
    
    # Get view mode from scene property
    view_mode = context.scene.get("segmentation_view_mode", "MASKS")
    
    if view_mode == "NONE":
        return
    elif view_mode == "DEPTH":
        depth_map = get_current_depth_map()
        if depth_map is not None:
            apply_depth_overlay(image, depth_map)
    elif view_mode == "MASKS":
        masks = get_current_masks()
        if masks:
            # Apply color overlay for each enabled mask with its color
            settings = context.scene.segmentation_mask_settings
            
            for item in settings.masks:
                if item.enabled and 0 <= item.mask_index < len(masks):
                    mask = masks[item.mask_index]
                    color = tuple(item.color[:3])  # RGB only
                    alpha = item.color[3]
                    apply_mask_overlay(image, [mask], color=color, alpha=alpha)


# ============================================================================
# Global storage for current masks and original image
# ============================================================================

_current_masks = []
_current_image = None
_original_image_pixels = None  # Store original pixels for reset
_current_depth_map = None  # Store depth map


def get_current_masks():
    """Get the currently stored segmentation masks."""
    return _current_masks


def set_current_masks(masks, image, context=None):
    """
    Store segmentation masks for later use.
    
    Args:
        masks: List of numpy mask arrays
        image: Blender image object
        context: Blender context (optional, for syncing to collection)
    """
    global _current_masks, _current_image
    _current_masks = masks
    _current_image = image
    
    # Sync to scene collection if context provided
    if context is not None and masks:
        sync_masks_to_collection(context, masks)


def store_original_image(image):
    """Store the original image pixels for later restoration."""
    global _original_image_pixels
    if image is not None:
        _original_image_pixels = np.array(image.pixels[:]).copy()


def get_original_image_pixels():
    """Get the stored original image pixels."""
    return _original_image_pixels


def restore_original_image(image):
    """Restore the image to its original pixels."""
    global _original_image_pixels
    if _original_image_pixels is not None and image is not None:
        image.pixels[:] = _original_image_pixels.tolist()
        image.update()


def apply_mask_overlay(image, masks, color=(0.0, 0.8, 0.3), alpha=0.5):
    """
    Apply a colored mask overlay onto a Blender image.
    
    Args:
        image: Blender image to modify
        masks: List of boolean numpy mask arrays (H, W)
        color: RGB tuple for mask color (0-1 range)
        alpha: Opacity of the mask overlay (0-1)
    """
    if not masks or image is None:
        return
    
    width, height = image.size
    
    # Get current pixels as numpy array
    pixels = np.array(image.pixels[:]).reshape((height, width, 4))
    
    # Process each mask
    for mask in masks:
        # Ensure mask matches image dimensions
        if mask.shape[0] != height or mask.shape[1] != width:
            # Resize mask if needed
            from PIL import Image as PILImage
            mask_pil = PILImage.fromarray(mask.astype(np.uint8) * 255)
            mask_pil = mask_pil.resize((width, height), PILImage.NEAREST)
            mask = np.array(mask_pil) > 127
        
        # Flip mask vertically to match Blender's coordinate system (origin at bottom-left)
        mask_flipped = np.flipud(mask)
        
        # Apply color overlay where mask is True
        for c in range(3):
            pixels[:, :, c] = np.where(
                mask_flipped,
                pixels[:, :, c] * (1 - alpha) + color[c] * alpha,
                pixels[:, :, c]
            )
    
    # Update the image
    image.pixels[:] = pixels.flatten().tolist()
    image.update()
    
    # Redraw Image Editors
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.tag_redraw()


def apply_colored_mask_overlays(context, image, masks):
    """
    Apply color-coded overlays for all masks using their assigned colors.
    
    Args:
        context: Blender context
        image: Blender image to modify
        masks: List of numpy mask arrays
    """
    if not masks or image is None:
        return
    
    settings = context.scene.segmentation_mask_settings
    
    # If no mask items yet, use default colors
    if len(settings.masks) == 0:
        colors = generate_distinct_colors(len(masks))
        for i, mask in enumerate(masks):
            color = colors[i][:3] if i < len(colors) else (0.5, 0.5, 0.5)
            alpha = colors[i][3] if i < len(colors) else 0.5
            apply_mask_overlay(image, [mask], color=color, alpha=alpha)
    else:
        # Use colors from the collection
        for item in settings.masks:
            if item.enabled and 0 <= item.mask_index < len(masks):
                mask = masks[item.mask_index]
                color = tuple(item.color[:3])
                alpha = item.color[3]
                apply_mask_overlay(image, [mask], color=color, alpha=alpha)


def get_active_image(context):
    """Get the currently active image in the IMAGE_EDITOR."""
    for area in context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            for space in area.spaces:
                if space.type == 'IMAGE_EDITOR' and space.image:
                    return space.image
    return None


def blender_image_to_pil(image, flip_vertical=True):
    """
    Convert a Blender image to a PIL Image.
    
    Args:
        image: Blender image object
        flip_vertical: Whether to flip the image vertically (default True for Blender coords)
        
    Returns:
        PIL Image object
    """
    from PIL import Image as PILImage
    
    # Get pixel data
    width, height = image.size
    pixels = np.array(image.pixels[:])
    
    # Reshape to (height, width, 4) RGBA
    pixels = pixels.reshape((height, width, 4))
    
    # Flip vertically (Blender's origin is bottom-left, PIL is top-left)
    if flip_vertical:
        pixels = np.flipud(pixels)
    
    # Convert to 8-bit RGB
    pixels = (pixels[:, :, :3] * 255).astype(np.uint8)
    
    return PILImage.fromarray(pixels, mode='RGB')


@procedural_operator
class SegmentByPromptOperator(Operator):
    """Segment the current image using a text prompt"""
    
    bl_idname = "segmentation.segment_by_prompt"
    bl_label = "Segment by Prompt"
    bl_description = "Use SAM3 to segment the image based on a text description"
    bl_options = {'REGISTER', 'UNDO'}
    
    prompt: StringProperty(
        name="Prompt",
        description="Describe what you want to segment",
        default=""
    )
    
    threshold: FloatProperty(
        name="Threshold",
        description="Detection confidence threshold",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    def execute(self, context):
        if not self.prompt:
            self.report({'WARNING'}, "Please enter a prompt")
            return {'CANCELLED'}
        
        # Get active image
        image = get_active_image(context)
        if image is None:
            self.report({'WARNING'}, "No image loaded in Image Editor")
            return {'CANCELLED'}
        
        # Check SAM3 model status
        from procedural_human.segmentation.sam_integration import SAM3Manager
        
        if SAM3Manager.is_loading():
            self.report({'WARNING'}, "SAM3 model is still loading. Please wait...")
            return {'CANCELLED'}
        
        if not SAM3Manager.is_loaded():
            # Start async loading and tell user to wait
            SAM3Manager.start_loading_async()
            self.report({'INFO'}, "SAM3 model loading started. Please try again in a moment.")
            return {'CANCELLED'}
        
        try:
            # Store original image pixels before any modification
            if get_original_image_pixels() is None:
                store_original_image(image)
            else:
                # Restore original before new segmentation
                restore_original_image(image)
            
            # Convert to PIL (from original, not overlaid)
            pil_image = blender_image_to_pil(image)
            
            # Get SAM3 manager
            sam = SAM3Manager.get_instance()
            
            # Run segmentation
            self.report({'INFO'}, f"Segmenting with prompt: '{self.prompt}'...")
            masks = sam.segment_by_prompt(
                pil_image,
                self.prompt,
                threshold=self.threshold
            )
            
            # Store masks for later use (with context to sync to collection)
            set_current_masks(masks, image, context)
            
            # Update scene property
            context.scene["segmentation_mask_count"] = len(masks)
            
            # Switch view mode to MASKS automatically
            context.scene["segmentation_view_mode"] = "MASKS"
            
            # Apply color-coded mask overlays
            if masks:
                apply_colored_mask_overlays(context, image, masks)
            
            self.report({'INFO'}, f"Found {len(masks)} segments")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Segmentation failed: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Segmentation failed: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "prompt")
        layout.prop(self, "threshold")


@procedural_operator
class SegmentByPointOperator(Operator):
    """Segment the current image by clicking on a point"""
    
    bl_idname = "segmentation.segment_by_point"
    bl_label = "Segment by Point"
    bl_description = "Click on an object to segment it using SAM3"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Store click coordinates
    click_x: FloatProperty(default=0.5)
    click_y: FloatProperty(default=0.5)
    
    threshold: FloatProperty(
        name="Threshold",
        description="Detection confidence threshold",
        default=0.5,
        min=0.0,
        max=1.0
    )
    
    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Get click position in image coordinates
            region = context.region
            
            # Normalize to 0-1 range
            self.click_x = event.mouse_region_x / region.width
            self.click_y = event.mouse_region_y / region.height
            
            self.do_segmentation(context)
            return {'FINISHED'}
        
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        
        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        if context.area.type != 'IMAGE_EDITOR':
            self.report({'WARNING'}, "Use this in the Image Editor")
            return {'CANCELLED'}
        
        # Check SAM3 model status before starting
        from procedural_human.segmentation.sam_integration import SAM3Manager
        
        if SAM3Manager.is_loading():
            self.report({'WARNING'}, "SAM3 model is still loading. Please wait...")
            return {'CANCELLED'}
        
        if not SAM3Manager.is_loaded():
            # Start async loading and tell user to wait
            SAM3Manager.start_loading_async()
            self.report({'INFO'}, "SAM3 model loading started. Please try again in a moment.")
            return {'CANCELLED'}
        
        context.window_manager.modal_handler_add(self)
        self.report({'INFO'}, "Click on the object you want to segment")
        return {'RUNNING_MODAL'}
    
    def do_segmentation(self, context):
        """Perform segmentation at the clicked point."""
        image = get_active_image(context)
        if image is None:
            self.report({'WARNING'}, "No image loaded")
            return
        
        # Double-check SAM is loaded
        from procedural_human.segmentation.sam_integration import SAM3Manager
        
        if not SAM3Manager.is_loaded():
            self.report({'WARNING'}, "SAM3 model not loaded")
            return
        
        try:
            # Store original image pixels before any modification
            if get_original_image_pixels() is None:
                store_original_image(image)
            else:
                # Restore original before new segmentation
                restore_original_image(image)
            
            # Convert click to pixel coordinates
            width, height = image.size
            point_x = int(self.click_x * width)
            point_y = int((1 - self.click_y) * height)  # Flip Y
            
            # Convert to PIL (from original, not overlaid)
            pil_image = blender_image_to_pil(image)
            
            # Get SAM3 manager
            sam = SAM3Manager.get_instance()
            
            # Run segmentation with point prompt
            masks = sam.segment_by_point(
                pil_image,
                points=[(point_x, point_y)],
                labels=[1],  # Foreground
                threshold=self.threshold
            )
            
            # Store masks (with context to sync to collection)
            set_current_masks(masks, image, context)
            context.scene["segmentation_mask_count"] = len(masks)
            
            # Switch view mode to MASKS automatically
            context.scene["segmentation_view_mode"] = "MASKS"
            
            # Apply color-coded mask overlays
            if masks:
                apply_colored_mask_overlays(context, image, masks)
            
            self.report({'INFO'}, f"Found {len(masks)} segments at ({point_x}, {point_y})")
            
        except Exception as e:
            logger.error(f"Point segmentation failed: {e}")
            self.report({'ERROR'}, f"Segmentation failed: {e}")


@procedural_operator
class ConvertMasksToCurvesOperator(Operator):
    """Convert the current segmentation masks to Blender curves"""
    
    bl_idname = "segmentation.masks_to_curves"
    bl_label = "Convert Masks to Curves"
    bl_description = "Convert segmentation masks to Blender curve objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    simplify: BoolProperty(
        name="Simplify",
        description="Simplify curve contours",
        default=True
    )
    
    simplify_amount: FloatProperty(
        name="Simplify Amount",
        description="Higher values = more simplified (0.001 - 0.05)",
        default=0.005,
        min=0.001,
        max=0.05
    )
    
    scale: FloatProperty(
        name="Scale",
        description="Scale factor for curves",
        default=1.0,
        min=0.01,
        max=100.0
    )
    
    def execute(self, context):
        all_masks = get_current_masks()
        
        if not all_masks:
            self.report({'WARNING'}, "No segmentation masks available. Run segmentation first.")
            return {'CANCELLED'}
        
        # Get only enabled masks
        enabled_indices = get_enabled_mask_indices(context)
        if not enabled_indices:
            self.report({'WARNING'}, "No masks selected. Enable at least one mask in the list.")
            return {'CANCELLED'}
        
        # Filter masks by enabled indices
        masks = [all_masks[i] for i in enabled_indices if i < len(all_masks)]
        
        if not masks:
            self.report({'WARNING'}, "Could not get selected masks")
            return {'CANCELLED'}
        
        try:
            from procedural_human.segmentation.mask_to_curve import masks_to_curves
            
            # Get image dimensions
            image = get_active_image(context)
            if image:
                width, height = image.size
            else:
                # Use first mask dimensions
                height, width = masks[0].shape[:2]
            
            # Convert masks to curves
            curves = masks_to_curves(
                masks,
                image_width=width,
                image_height=height,
                name_prefix="Segment",
                simplify=self.simplify,
                simplify_epsilon=self.simplify_amount,
                scale=self.scale
            )
            
            # Select created curves
            bpy.ops.object.select_all(action='DESELECT')
            for curve in curves:
                curve.select_set(True)
            
            if curves:
                context.view_layer.objects.active = curves[0]
            
            self.report({'INFO'}, f"Created {len(curves)} curve objects")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Mask to curve conversion failed: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Conversion failed: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "simplify")
        if self.simplify:
            layout.prop(self, "simplify_amount")
        layout.prop(self, "scale")


@procedural_operator
class ClearSegmentationMasksOperator(Operator):
    """Clear the current segmentation masks and restore original image"""
    
    bl_idname = "segmentation.clear_masks"
    bl_label = "Clear Masks"
    bl_description = "Clear all current segmentation masks and restore original image"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        # Restore the original image before clearing
        image = get_active_image(context)
        if image is not None and get_original_image_pixels() is not None:
            restore_original_image(image)
        
        set_current_masks([], None)
        context.scene["segmentation_mask_count"] = 0
        
        # Clear the mask collection
        settings = context.scene.segmentation_mask_settings
        settings.masks.clear()
        settings.active_mask_index = -1
        
        self.report({'INFO'}, "Segmentation masks cleared, image restored")
        return {'FINISHED'}


@procedural_operator
class ResetOriginalImageOperator(Operator):
    """Reset the stored original image (use when loading a new image)"""
    
    bl_idname = "segmentation.reset_original"
    bl_label = "Reset Original"
    bl_description = "Clear the stored original image reference (use after loading a new image)"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        global _original_image_pixels
        _original_image_pixels = None
        self.report({'INFO'}, "Original image reference cleared")
        return {'FINISHED'}


@procedural_operator
class LoadSAM3ModelOperator(Operator):
    """Load the SAM3 model asynchronously (non-blocking)"""
    
    bl_idname = "segmentation.load_sam3_model"
    bl_label = "Load SAM3 Model"
    bl_description = "Pre-load the SAM3 segmentation model in the background"
    bl_options = {'REGISTER'}
    
    _timer = None
    
    def modal(self, context, event):
        from procedural_human.segmentation.sam_integration import SAM3Manager
        
        if event.type == 'TIMER':
            # Check loading status
            if SAM3Manager.is_loaded():
                self.cancel(context)
                self.report({'INFO'}, "SAM3 model loaded successfully")
                return {'FINISHED'}
            
            if SAM3Manager.get_loading_error():
                error = SAM3Manager.get_loading_error()
                self.cancel(context)
                self.report({'ERROR'}, f"SAM3 loading failed: {error}")
                return {'CANCELLED'}
            
            if not SAM3Manager.is_loading():
                # Loading finished but not loaded and no error - unexpected state
                self.cancel(context)
                self.report({'WARNING'}, "SAM3 loading ended unexpectedly")
                return {'CANCELLED'}
            
            # Still loading - update UI
            progress = SAM3Manager.get_loading_progress()
            context.workspace.status_text_set(f"Loading SAM3: {progress}")
            
            # Redraw panels
            for area in context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    area.tag_redraw()
        
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        from procedural_human.segmentation.sam_integration import SAM3Manager
        
        if SAM3Manager.is_loaded():
            self.report({'INFO'}, "SAM3 model is already loaded")
            return {'FINISHED'}
        
        if SAM3Manager.is_loading():
            self.report({'INFO'}, "SAM3 model is already loading...")
            return {'CANCELLED'}
        
        # Start async loading
        SAM3Manager.start_loading_async()
        
        # Start timer to poll for completion
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.2, window=context.window)
        wm.modal_handler_add(self)
        
        context.workspace.status_text_set("Loading SAM3 model...")
        self.report({'INFO'}, "Loading SAM3 model in background...")
        
        return {'RUNNING_MODAL'}
    
    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
        context.workspace.status_text_set(None)


@procedural_operator
class EstimateDepthOperator(Operator):
    """Estimate depth map from the current image"""
    
    bl_idname = "segmentation.estimate_depth"
    bl_label = "Estimate Depth"
    bl_description = "Estimate depth map from the current image using Depth Anything V3"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Get active image
        image = get_active_image(context)
        if image is None:
            self.report({'WARNING'}, "No image loaded in Image Editor")
            return {'CANCELLED'}
        
        # Check Depth Estimator status
        from procedural_human.depth_estimation.depth_estimator import DepthEstimator
        
        try:
            depth_estimator = DepthEstimator.get_instance()
            
            # Convert to PIL
            pil_image = blender_image_to_pil(image)
            
            # Estimate depth
            self.report({'INFO'}, "Estimating depth map...")
            depth_map = depth_estimator.estimate_depth(pil_image)
            
            # Store depth map
            set_current_depth_map(depth_map)
            
            # Switch view mode to DEPTH automatically
            context.scene["segmentation_view_mode"] = "DEPTH"
            refresh_mask_overlay(context)
            
            self.report({'INFO'}, f"Depth map estimated: {depth_map.shape}")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Depth estimation failed: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Depth estimation failed: {e}")
            return {'CANCELLED'}


@procedural_operator
class SetSegmentationViewModeOperator(Operator):
    """Set the segmentation view mode (Masks, Depth, or None)"""
    
    bl_idname = "segmentation.set_view_mode"
    bl_label = "Set View Mode"
    bl_description = "Set the overlay view mode"
    bl_options = {'REGISTER'}
    
    mode: StringProperty(
        name="Mode",
        description="View mode: MASKS, DEPTH, or NONE",
        default="MASKS"
    )
    
    def execute(self, context):
        context.scene["segmentation_view_mode"] = self.mode
        refresh_mask_overlay(context)
        return {'FINISHED'}


# ============================================================================
# Registration
# ============================================================================

# Classes to register (order matters for PropertyGroups)
_mask_classes = [
    SegmentationMaskItem,
    SEGMENTATION_UL_masks,
    SegmentationMaskSettings,
]


def register_mask_properties():
    """Register mask-related PropertyGroups and UIList."""
    for cls in _mask_classes:
        bpy.utils.register_class(cls)
    
    # Add scene property
    bpy.types.Scene.segmentation_mask_settings = PointerProperty(type=SegmentationMaskSettings)


def unregister_mask_properties():
    """Unregister mask-related PropertyGroups and UIList."""
    # Remove scene property
    if hasattr(bpy.types.Scene, 'segmentation_mask_settings'):
        del bpy.types.Scene.segmentation_mask_settings
    
    # Unregister classes in reverse order
    for cls in reversed(_mask_classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

