"""
SAM3 Segmentation operators for the segmentation workflow.
"""

import bpy
import numpy as np
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty, BoolProperty

from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import logger


# Global storage for current masks and original image
_current_masks = []
_current_image = None
_original_image_pixels = None  # Store original pixels for reset


def get_current_masks():
    """Get the currently stored segmentation masks."""
    return _current_masks


def set_current_masks(masks, image):
    """Store segmentation masks for later use."""
    global _current_masks, _current_image
    _current_masks = masks
    _current_image = image


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


def get_active_image(context):
    """Get the currently active image in the IMAGE_EDITOR."""
    for area in context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            for space in area.spaces:
                if space.type == 'IMAGE_EDITOR' and space.image:
                    return space.image
    return None


def blender_image_to_pil(image):
    """Convert a Blender image to a PIL Image."""
    from PIL import Image as PILImage
    
    # Get pixel data
    width, height = image.size
    pixels = np.array(image.pixels[:])
    
    # Reshape to (height, width, 4) RGBA
    pixels = pixels.reshape((height, width, 4))
    
    # Flip vertically (Blender's origin is bottom-left)
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
            from procedural_human.segmentation.sam_integration import SAM3Manager
            sam = SAM3Manager.get_instance()
            
            # Run segmentation
            self.report({'INFO'}, f"Segmenting with prompt: '{self.prompt}'...")
            masks = sam.segment_by_prompt(
                pil_image,
                self.prompt,
                threshold=self.threshold
            )
            
            # Store masks for later use
            set_current_masks(masks, image)
            
            # Update scene property
            context.scene["segmentation_mask_count"] = len(masks)
            
            # Apply mask overlay to display the segmentation result
            if masks:
                apply_mask_overlay(image, masks, color=(0.0, 0.8, 0.3), alpha=0.5)
            
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
        
        context.window_manager.modal_handler_add(self)
        self.report({'INFO'}, "Click on the object you want to segment")
        return {'RUNNING_MODAL'}
    
    def do_segmentation(self, context):
        """Perform segmentation at the clicked point."""
        image = get_active_image(context)
        if image is None:
            self.report({'WARNING'}, "No image loaded")
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
            from procedural_human.segmentation.sam_integration import SAM3Manager
            sam = SAM3Manager.get_instance()
            
            # Run segmentation with point prompt
            masks = sam.segment_by_point(
                pil_image,
                points=[(point_x, point_y)],
                labels=[1],  # Foreground
                threshold=self.threshold
            )
            
            # Store masks
            set_current_masks(masks, image)
            context.scene["segmentation_mask_count"] = len(masks)
            
            # Apply mask overlay to display the segmentation result
            if masks:
                apply_mask_overlay(image, masks, color=(0.0, 0.8, 0.3), alpha=0.5)
            
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
        masks = get_current_masks()
        
        if not masks:
            self.report({'WARNING'}, "No segmentation masks available. Run segmentation first.")
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


