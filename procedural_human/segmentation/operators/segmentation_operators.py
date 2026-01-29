"""
SAM3 Segmentation operators for the segmentation workflow.
"""

import bpy
import numpy as np
from bpy.types import Operator, PropertyGroup, UIList
from mathutils import Quaternion
from bpy.props import (
    StringProperty, FloatProperty, BoolProperty, IntProperty,
    FloatVectorProperty, CollectionProperty, PointerProperty
)
from PIL import Image as PILImage
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import logger
import matplotlib.cm as cm
from procedural_human.segmentation.operators.debug_planes import update_debug_planes_visibility, update_debug_planes_visibility_callback
from procedural_human.segmentation.overlays.curve_ridges_overlay import apply_ridge_curves_overlay
from procedural_human.segmentation.overlays.depth_map_overlay import apply_depth_overlay, get_current_depth_map, set_current_depth_map
from procedural_human.segmentation.overlays.hessian_overlay import apply_hessian_overlay
from procedural_human.segmentation.overlays.image_overlay import get_original_image_pixels, restore_original_image, store_original_image
from procedural_human.segmentation.overlays.medialness_overlay import apply_medialness_overlay
from procedural_human.segmentation.overlays.spine_overlay import apply_spine_overlay
from procedural_human.segmentation.segmentation_state import (
    get_current_masks, get_current_spine_path, set_masks_state,
    get_current_image_state, set_image_state,
    get_current_medialness_map, set_current_medialness_map,
    get_current_hessian_map, set_current_hessian_map,
    get_current_ridge_curves, set_current_ridge_curves
)

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
            row.prop(item, "enabled", text="", icon='CHECKBOX_HLT' if item.enabled else 'CHECKBOX_DEHLT')
            row.prop(item, "color", text="")
            row.label(text=f"Mask {index + 1}")
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
        hue = (i * 0.618033988749895) % 1.0  # Golden ratio for good distribution
        saturation = 0.7 + (i % 3) * 0.1  # Vary saturation slightly
        value = 0.9 - (i % 2) * 0.1  # Vary value slightly
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
    settings.masks.clear()
    colors = generate_distinct_colors(len(masks))
    for i, mask in enumerate(masks):
        item = settings.masks.add()
        item.enabled = True
        item.color = colors[i] if i < len(colors) else (0.5, 0.5, 0.5, 0.5)
        item.area = int(np.sum(mask))
        item.mask_index = i
    settings.active_mask_index = 0 if len(masks) > 0 else -1


def get_enabled_mask_indices(context) -> list:
    """Get list of indices for enabled masks."""
    settings = context.scene.segmentation_mask_settings
    return [item.mask_index for item in settings.masks if item.enabled and item.mask_index >= 0]


def get_mask_colors(context) -> list:
    """Get list of colors for all masks."""
    settings = context.scene.segmentation_mask_settings
    return [tuple(item.color) for item in settings.masks]

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

def refresh_mask_overlay(context):
    """Refresh the overlay with current view mode (masks, depth, or none)."""
    image = get_active_image(context)
    masks = get_current_masks()
    if masks is None:
        return
    if image is None:
        return
    stored_pixels = get_original_image_pixels()
    if stored_pixels is None:
        store_original_image(image)
    else:
        current_len = image.size[0] * image.size[1] * 4
        if len(stored_pixels) != current_len:
            store_original_image(image)
    restore_original_image(image)
    view_mode = context.scene.get("segmentation_view_mode", "MASKS")
    
    if view_mode == "NONE":
        update_debug_planes_visibility(context)
        return
    elif view_mode == "DEPTH":
        depth_map = get_current_depth_map()
        if depth_map is not None:
            apply_depth_overlay(image, depth_map)
    elif view_mode == "MASKS":
        masks = get_current_masks()
        if masks:
            settings = context.scene.segmentation_mask_settings
            
            for item in settings.masks:
                if item.enabled and 0 <= item.mask_index < len(masks):
                    mask = masks[item.mask_index]
                    color = tuple(item.color[:3])  # RGB only
                    alpha = item.color[3]
                    apply_mask_overlay(image, [mask], color=color, alpha=alpha)
    elif view_mode == "SPINE":
        spine_path = get_current_spine_path()
        if spine_path is not None:
            apply_spine_overlay(image, spine_path, color=(1.0, 0.0, 1.0), line_width=3)
    elif view_mode == "MEDIAL":
        medialness_map = get_current_medialness_map()
        if medialness_map is not None:
            apply_medialness_overlay(image, medialness_map, colormap='hot')
    elif view_mode == "HESSIAN":
        hessian_map = get_current_hessian_map()
        if hessian_map is not None:
            apply_hessian_overlay(image, hessian_map, colormap='viridis')
    elif view_mode == "RIDGES":
        curves = get_current_ridge_curves()
        if curves is not None:
            masks = get_current_masks()
            if masks:
                settings = context.scene.segmentation_mask_settings
                for item in settings.masks:
                    if item.enabled and 0 <= item.mask_index < len(masks):
                        mask = masks[item.mask_index]
                        apply_mask_overlay(image, [mask], color=(0.3, 0.3, 0.3), alpha=0.3)
                        break
            apply_ridge_curves_overlay(image, curves, color=(0.0, 1.0, 0.0))
    update_debug_planes_visibility(context, image, masks)


def set_current_masks(masks, image, context=None):
    """
    Store segmentation masks for later use.
    
    Args:
        masks: List of numpy mask arrays
        image: Blender image object
        context: Blender context (optional, for syncing to collection)
    """
    set_masks_state(masks)
    set_image_state(image)
    if context is not None and masks:
        sync_masks_to_collection(context, masks)



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
    pixels = np.array(image.pixels[:]).reshape((height, width, 4))
    for mask in masks:
        if mask.shape[0] != height or mask.shape[1] != width:
            mask_pil = PILImage.fromarray(mask.astype(np.uint8) * 255)
            mask_pil = mask_pil.resize((width, height), PILImage.NEAREST)
            mask = np.array(mask_pil) > 127
        mask_flipped = np.flipud(mask)
        for c in range(3):
            pixels[:, :, c] = np.where(
                mask_flipped,
                pixels[:, :, c] * (1 - alpha) + color[c] * alpha,
                pixels[:, :, c]
            )
    image.pixels[:] = pixels.flatten().tolist()
    image.update()
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
    if len(settings.masks) == 0:
        colors = generate_distinct_colors(len(masks))
        for i, mask in enumerate(masks):
            color = colors[i][:3] if i < len(colors) else (0.5, 0.5, 0.5)
            alpha = colors[i][3] if i < len(colors) else 0.5
            apply_mask_overlay(image, [mask], color=color, alpha=alpha)
    else:
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
    width, height = image.size
    pixels = np.array(image.pixels[:])
    pixels = pixels.reshape((height, width, 4))
    if flip_vertical:
        pixels = np.flipud(pixels)
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
        image = get_active_image(context)
        if image is None:
            self.report({'WARNING'}, "No image loaded in Image Editor")
            return {'CANCELLED'}
        from procedural_human.segmentation.sam_integration import SAM3Manager
        
        if SAM3Manager.is_loading():
            self.report({'WARNING'}, "SAM3 model is still loading. Please wait...")
            return {'CANCELLED'}
        
        if not SAM3Manager.is_loaded():
            SAM3Manager.start_loading_async()
            self.report({'INFO'}, "SAM3 model loading started. Please try again in a moment.")
            return {'CANCELLED'}
        
        try:
            if get_original_image_pixels() is None:
                store_original_image(image)
            else:
                restore_original_image(image)
            pil_image = blender_image_to_pil(image)
            sam = SAM3Manager.get_instance()
            self.report({'INFO'}, f"Segmenting with prompt: '{self.prompt}'...")
            masks = sam.segment_by_prompt(
                pil_image,
                self.prompt,
                threshold=self.threshold
            )
            set_current_masks(masks, image, context)
            context.scene["segmentation_mask_count"] = len(masks)
            context.scene["segmentation_view_mode"] = "MASKS"
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
            region = context.region
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
        from procedural_human.segmentation.sam_integration import SAM3Manager
        
        if SAM3Manager.is_loading():
            self.report({'WARNING'}, "SAM3 model is still loading. Please wait...")
            return {'CANCELLED'}
        
        if not SAM3Manager.is_loaded():
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
        from procedural_human.segmentation.sam_integration import SAM3Manager
        
        if not SAM3Manager.is_loaded():
            self.report({'WARNING'}, "SAM3 model not loaded")
            return
        
        try:
            if get_original_image_pixels() is None:
                store_original_image(image)
            else:
                restore_original_image(image)
            width, height = image.size
            point_x = int(self.click_x * width)
            point_y = int((1 - self.click_y) * height)  # Flip Y
            pil_image = blender_image_to_pil(image)
            sam = SAM3Manager.get_instance()
            masks = sam.segment_by_point(
                pil_image,
                points=[(point_x, point_y)],
                labels=[1],  # Foreground
                threshold=self.threshold
            )
            set_current_masks(masks, image, context)
            context.scene["segmentation_mask_count"] = len(masks)
            context.scene["segmentation_view_mode"] = "MASKS"
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
        enabled_indices = get_enabled_mask_indices(context)
        if not enabled_indices:
            self.report({'WARNING'}, "No masks selected. Enable at least one mask in the list.")
            return {'CANCELLED'}
        masks = [all_masks[i] for i in enabled_indices if i < len(all_masks)]
        
        if not masks:
            self.report({'WARNING'}, "Could not get selected masks")
            return {'CANCELLED'}
        
        try:
            from procedural_human.segmentation.mask_to_curve import masks_to_curves
            image = get_active_image(context)
            if image:
                width, height = image.size
            else:
                height, width = masks[0].shape[:2]
            curves = masks_to_curves(
                masks,
                image_width=width,
                image_height=height,
                name_prefix="Segment",
                simplify=self.simplify,
                simplify_epsilon=self.simplify_amount,
                scale=self.scale
            )
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
        image = get_active_image(context)
        if image is not None and get_original_image_pixels() is not None:
            restore_original_image(image)
        
        set_current_masks([], None)
        context.scene["segmentation_mask_count"] = 0
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
                self.cancel(context)
                self.report({'WARNING'}, "SAM3 loading ended unexpectedly")
                return {'CANCELLED'}
            progress = SAM3Manager.get_loading_progress()
            context.workspace.status_text_set(f"Loading SAM3: {progress}")
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
        SAM3Manager.start_loading_async()
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
        image = get_active_image(context)
        if image is None:
            self.report({'WARNING'}, "No image loaded in Image Editor")
            return {'CANCELLED'}
        from procedural_human.depth_estimation.depth_estimator import DepthEstimator
        
        try:
            depth_estimator = DepthEstimator.get_instance()
            pil_image = blender_image_to_pil(image)
            self.report({'INFO'}, "Estimating depth map...")
            depth_map = depth_estimator.estimate_depth(pil_image)
            set_current_depth_map(depth_map)
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


@procedural_operator
class CreateDepthLoftObjectOperator(Operator):
    """Create a 3D object from the current depth map and mask using the Segmentation Depth Loft geometry node group"""
    
    bl_idname = "segmentation.create_depth_loft_object"
    bl_label = "Create Depth Loft Object"
    bl_description = "Create a mesh object with embedded depth and mask images using the Segmentation Depth Loft node group"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        depth_map = get_current_depth_map()
        if depth_map is None:
            self.report({'WARNING'}, "No depth map available. Run 'Estimate Depth' first.")
            return {'CANCELLED'}
        
        masks = get_current_masks()
        if not masks:
            self.report({'WARNING'}, "No segmentation masks available. Run segmentation first.")
            return {'CANCELLED'}
        
        enabled_indices = get_enabled_mask_indices(context)
        if not enabled_indices:
            self.report({'WARNING'}, "No masks selected. Enable at least one mask.")
            return {'CANCELLED'}
        
        try:
            from procedural_human.geo_node_groups.segmentation_depth_loft import create_segmentation_depth_loft_group
            node_group = create_segmentation_depth_loft_group()
            
            height, width = depth_map.shape[:2]
            
            # Create combined mask from enabled masks
            combined_mask = np.zeros((height, width), dtype=np.float32)
            for idx in enabled_indices:
                if idx < len(masks):
                    mask = masks[idx]
                    if mask.shape[0] != height or mask.shape[1] != width:
                        mask_pil = PILImage.fromarray(mask.astype(np.uint8) * 255)
                        mask_pil = mask_pil.resize((width, height), PILImage.NEAREST)
                        mask = np.array(mask_pil).astype(np.float32) / 255.0
                    else:
                        mask = mask.astype(np.float32)
                    combined_mask = np.maximum(combined_mask, mask)
            
            # Flip vertically for Blender coordinate system
            mask_flipped = np.flipud(combined_mask)
            depth_flipped = np.flipud(depth_map)
            
            # Create mask image with RGBA pixels
            mask_pixels = np.zeros(width * height * 4, dtype=np.float32)
            mask_flat = mask_flipped.flatten()
            mask_pixels[0::4] = mask_flat  # R
            mask_pixels[1::4] = mask_flat  # G
            mask_pixels[2::4] = mask_flat  # B
            mask_pixels[3::4] = mask_flat  # A (use mask as alpha too)
            
            mask_img_name = "DepthLoft_Mask"
            mask_img = bpy.data.images.get(mask_img_name)
            if mask_img:
                bpy.data.images.remove(mask_img)
            mask_img = bpy.data.images.new(mask_img_name, width=width, height=height, alpha=True)
            mask_img.pixels[:] = mask_pixels.tolist()
            mask_img.pack()
            mask_img.asset_mark()
            mask_img.asset_data.description = "Segmentation mask for Depth Loft"
            
            # Create depth image with RGBA pixels
            depth_pixels = np.zeros(width * height * 4, dtype=np.float32)
            depth_flat = depth_flipped.flatten()
            depth_pixels[0::4] = depth_flat  # R
            depth_pixels[1::4] = depth_flat  # G
            depth_pixels[2::4] = depth_flat  # B
            depth_pixels[3::4] = 1.0  # A
            
            depth_img_name = "DepthLoft_Depth"
            depth_img = bpy.data.images.get(depth_img_name)
            if depth_img:
                bpy.data.images.remove(depth_img)
            depth_img = bpy.data.images.new(depth_img_name, width=width, height=height, alpha=True)
            depth_img.pixels[:] = depth_pixels.tolist()
            depth_img.pack()
            depth_img.asset_mark()
            depth_img.asset_data.description = "Depth map for Depth Loft"
            
            # Create mesh object
            mesh = bpy.data.meshes.new("DepthLoftMesh")
            mesh.from_pydata([(0, 0, 0)], [], [])
            obj = bpy.data.objects.new("DepthLoft", mesh)
            context.collection.objects.link(obj)
            
            # Add geometry nodes modifier
            modifier = obj.modifiers.new(name="DepthLoft", type='NODES')
            modifier.node_group = node_group
            
            # Set images via modifier socket interface
            for item in node_group.interface.items_tree:
                if item.name == "SegmentationMask":
                    modifier[item.identifier] = mask_img
                elif item.name == "DepthMask":
                    modifier[item.identifier] = depth_img
            
            # Select the new object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            # Set 3D viewport to Front Orthographic
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.region_3d.view_perspective = 'ORTHO'
                            # Front view rotation quaternion (looking down -Y axis)
                            space.region_3d.view_rotation = Quaternion((0.7071, 0.7071, 0.0, 0.0))
                            break
                    break
            
            self.report({'INFO'}, f"Created DepthLoft object with embedded images ({width}x{height})")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to create depth loft object: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Failed to create depth loft object: {e}")
            return {'CANCELLED'}


_mask_classes = [
    SegmentationMaskItem,
    SEGMENTATION_UL_masks,
    SegmentationMaskSettings,
]


def register_mask_properties():
    """Register mask-related PropertyGroups and UIList."""
    for cls in _mask_classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.segmentation_mask_settings = PointerProperty(type=SegmentationMaskSettings)
    bpy.types.Scene.show_debug_planes = BoolProperty(
        name="Show Debug Planes",
        description="Show image planes in 3D view aligned to camera",
        default=False,
        update=update_debug_planes_visibility_callback
    )


def unregister_mask_properties():
    """Unregister mask-related PropertyGroups and UIList."""
    if hasattr(bpy.types.Scene, 'segmentation_mask_settings'):
        del bpy.types.Scene.segmentation_mask_settings
    
    if hasattr(bpy.types.Scene, 'show_debug_planes'):
        del bpy.types.Scene.show_debug_planes
    for cls in reversed(_mask_classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
