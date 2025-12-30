"""
SAM3 Segmentation operators for the segmentation workflow.
"""

import bpy
import numpy as np
from bpy.types import Operator
from bpy.props import StringProperty, FloatProperty, BoolProperty

from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import logger


# Global storage for current masks
_current_masks = []
_current_image = None


def get_current_masks():
    """Get the currently stored segmentation masks."""
    return _current_masks


def set_current_masks(masks, image):
    """Store segmentation masks for later use."""
    global _current_masks, _current_image
    _current_masks = masks
    _current_image = image


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
            # Convert to PIL
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
            # Convert click to pixel coordinates
            width, height = image.size
            point_x = int(self.click_x * width)
            point_y = int((1 - self.click_y) * height)  # Flip Y
            
            # Convert to PIL
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
    """Clear the current segmentation masks"""
    
    bl_idname = "segmentation.clear_masks"
    bl_label = "Clear Masks"
    bl_description = "Clear all current segmentation masks"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        set_current_masks([], None)
        context.scene["segmentation_mask_count"] = 0
        self.report({'INFO'}, "Segmentation masks cleared")
        return {'FINISHED'}


