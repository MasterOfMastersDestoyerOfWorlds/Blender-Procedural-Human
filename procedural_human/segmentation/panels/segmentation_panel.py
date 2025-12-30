"""
Segmentation panel for the segmentation workflow.

Provides UI for SAM3 segmentation operations.
"""

import bpy
from bpy.types import Panel

from procedural_human.decorators.panel_decorator import procedural_panel


@procedural_panel
class SegmentationControlsPanel(Panel):
    """SAM3 Segmentation controls panel"""
    
    bl_label = "Segmentation"
    bl_idname = "PROCEDURAL_PT_segmentation_controls"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Segmentation"
    
    def draw(self, context):
        layout = self.layout
        
        # SAM3 Status
        box = layout.box()
        box.label(text="SAM3 Status", icon='MOD_MASK')
        
        try:
            from procedural_human.segmentation.sam_integration import SAM3Manager
            if SAM3Manager.is_loaded():
                box.label(text="  Model: Loaded", icon='CHECKMARK')
            else:
                box.label(text="  Model: Not loaded (loads on first use)", icon='TIME')
        except:
            box.label(text="  Model: Not available", icon='ERROR')
        
        # Segmentation methods
        layout.separator()
        box = layout.box()
        box.label(text="Segment Image", icon='SELECT_SET')
        
        # Text prompt segmentation
        col = box.column(align=True)
        col.operator("segmentation.segment_by_prompt", text="Segment by Prompt", icon='TEXT')
        
        # Point click segmentation
        col.operator("segmentation.segment_by_point", text="Click to Segment", icon='PIVOT_CURSOR')
        
        # Current masks info
        layout.separator()
        box = layout.box()
        box.label(text="Current Masks", icon='MOD_MASK')
        
        mask_count = context.scene.get("segmentation_mask_count", 0)
        box.label(text=f"  {mask_count} mask(s) available")
        
        if mask_count > 0:
            row = box.row(align=True)
            row.operator("segmentation.masks_to_curves", text="Convert to Curves", icon='CURVE_DATA')
            row.operator("segmentation.clear_masks", text="", icon='X')
        
        # Instructions
        layout.separator()
        box = layout.box()
        box.label(text="Instructions", icon='INFO')
        col = box.column(align=True)
        col.scale_y = 0.7
        col.label(text="1. Load an image (search or disk)")
        col.label(text="2. Use prompt or click to segment")
        col.label(text="3. Convert masks to curves")
        col.label(text="4. Insert curves into 3D scene")


@procedural_panel
class SegmentationAdvancedPanel(Panel):
    """Advanced segmentation settings"""
    
    bl_label = "Advanced Settings"
    bl_idname = "PROCEDURAL_PT_segmentation_advanced"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Segmentation"
    bl_parent_id = "PROCEDURAL_PT_segmentation_controls"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # SAM3 settings
        box = layout.box()
        box.label(text="SAM3 Configuration", icon='PREFERENCES')
        
        # Show model path
        col = box.column(align=True)
        col.scale_y = 0.7
        col.label(text="Model Path:")
        try:
            from procedural_human.segmentation.sam_integration import SAM3Manager
            col.label(text=f"  {SAM3Manager.MODEL_PATH}")
        except:
            col.label(text="  (bundled with addon)")
        
        # Memory management
        layout.separator()
        box = layout.box()
        box.label(text="Memory", icon='MEMORY')
        
        try:
            from procedural_human.segmentation.sam_integration import SAM3Manager
            if SAM3Manager.is_loaded():
                box.operator(
                    "segmentation.unload_sam",
                    text="Unload Model",
                    icon='CANCEL'
                )
            else:
                box.label(text="Model not loaded")
        except:
            box.label(text="SAM3 not available")


# Operator to unload SAM model
from bpy.types import Operator
from procedural_human.decorators.operator_decorator import procedural_operator


@procedural_operator
class UnloadSAMOperator(Operator):
    """Unload the SAM3 model from memory"""
    
    bl_idname = "segmentation.unload_sam"
    bl_label = "Unload SAM3"
    bl_description = "Unload the SAM3 model to free up GPU memory"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from procedural_human.segmentation.sam_integration import SAM3Manager
            SAM3Manager.unload()
            self.report({'INFO'}, "SAM3 model unloaded")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to unload: {e}")
            return {'CANCELLED'}


