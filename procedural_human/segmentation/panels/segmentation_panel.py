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
            if SAM3Manager.is_loading():
                # Show loading progress
                progress = SAM3Manager.get_loading_progress()
                box.label(text="  Model: Loading...", icon='TIME')
                if progress:
                    col = box.column()
                    col.scale_y = 0.7
                    col.label(text=f"    {progress[:40]}...")
            elif SAM3Manager.is_loaded():
                box.label(text="  Model: Loaded", icon='CHECKMARK')
            else:
                error = SAM3Manager.get_loading_error()
                if error:
                    box.label(text="  Model: Load failed", icon='ERROR')
                    col = box.column()
                    col.scale_y = 0.6
                    col.label(text=f"    {error[:40]}...")
                else:
                    box.label(text="  Model: Not loaded", icon='TIME')
                    box.operator("segmentation.load_sam3_model", text="Load Model", icon='IMPORT')
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
        
        # Current masks info with UIList
        layout.separator()
        box = layout.box()
        box.label(text="Current Masks", icon='MOD_MASK')
        
        mask_count = context.scene.get("segmentation_mask_count", 0)
        
        if mask_count > 0:
            # Mask list with selection
            settings = context.scene.segmentation_mask_settings
            
            row = box.row()
            row.template_list(
                "SEGMENTATION_UL_masks",
                "",
                settings,
                "masks",
                settings,
                "active_mask_index",
                rows=min(4, max(2, len(settings.masks)))
            )
            
            # Selection buttons
            row = box.row(align=True)
            row.operator("segmentation.select_all_masks", text="All", icon='CHECKBOX_HLT')
            row.operator("segmentation.deselect_all_masks", text="None", icon='CHECKBOX_DEHLT')
            row.operator("segmentation.invert_mask_selection", text="Invert", icon='ARROW_LEFTRIGHT')
            row.operator("segmentation.refresh_overlay", text="", icon='FILE_REFRESH')
            
            # Count enabled masks
            enabled_count = sum(1 for m in settings.masks if m.enabled)
            box.label(text=f"  {enabled_count}/{mask_count} mask(s) selected")
            
            # Action buttons
            row = box.row(align=True)
            row.operator("segmentation.masks_to_curves", text="Convert to Curves", icon='CURVE_DATA')
            row.operator("segmentation.clear_masks", text="", icon='X')
        else:
            box.label(text="  No masks available")
        
        # Novel View Generation
        layout.separator()
        box = layout.box()
        box.label(text="3D Novel View", icon='VIEW3D')
        
        # Server status (uses cached value to avoid blocking UI)
        try:
            from procedural_human.novel_view_gen.server_manager import (
                is_server_running_cached,
                is_server_starting,
                get_server_start_error,
            )
            if is_server_running_cached():
                box.label(text="  Hunyuan3D: Running", icon='CHECKMARK')
            elif is_server_starting():
                box.label(text="  Hunyuan3D: Starting...", icon='TIME')
            else:
                error = get_server_start_error()
                if error:
                    box.label(text="  Hunyuan3D: Failed", icon='ERROR')
                    # Show truncated error
                    col = box.column()
                    col.scale_y = 0.6
                    col.label(text=f"    {error[:50]}...")
                else:
                    box.label(text="  Hunyuan3D: Not running", icon='TIME')
            box.operator("segmentation.check_hunyuan_server", text="Check Server", icon='FILE_REFRESH')
        except:
            box.label(text="  Hunyuan3D: Not available", icon='ERROR')
        
        # Check if generation is in progress
        try:
            from procedural_human.segmentation.operators.novel_view_operators import (
                is_generation_running,
                get_generation_progress,
            )
            generation_running = is_generation_running()
        except:
            generation_running = False
        
        # Novel view operators
        col = box.column(align=True)
        
        if generation_running:
            # Show progress
            progress = get_generation_progress()
            col.label(text=progress, icon='TIME')
            col.operator("segmentation.cancel_novel_view", text="Cancel", icon='CANCEL')
        elif mask_count > 0:
            col.operator("segmentation.generate_novel_view", text="Generate Novel View", icon='MESH_MONKEY')
        else:
            col.enabled = False
            col.operator("segmentation.generate_novel_view", text="Generate Novel View (need masks)", icon='MESH_MONKEY')
        
        # Show generated mesh count
        hunyuan_count = context.scene.get("hunyuan_mesh_count", 0)
        if hunyuan_count > 0:
            box.label(text=f"  {hunyuan_count} mesh(es) in Hunyuan_Meshes")
        
        # Novel view contour info
        front_pts = context.scene.get("novel_view_front_points", 0)
        side_pts = context.scene.get("novel_view_side_points", 0)
        
        if front_pts > 0 and side_pts > 0:
            row = box.row()
            row.label(text=f"  Front: {front_pts} pts, Side: {side_pts} pts")
            
            row = box.row(align=True)
            row.operator("segmentation.create_dual_mesh_curves", text="Create Mesh Curves", icon='MESH_DATA')
            row.operator("segmentation.clear_novel_contours", text="", icon='X')
        
        # Instructions
        layout.separator()
        box = layout.box()
        box.label(text="Instructions", icon='INFO')
        col = box.column(align=True)
        col.scale_y = 0.7
        col.label(text="1. Load an image (search or disk)")
        col.label(text="2. Use prompt or click to segment")
        col.label(text="3a. Convert masks to curves, OR")
        col.label(text="3b. Generate novel view (3D)")
        col.label(text="4. Create mesh curves from contours")
        col.label(text="5. Coons patch generates surface")


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
        
        # Test mesh curves
        layout.separator()
        box = layout.box()
        box.label(text="Testing", icon='EXPERIMENTAL')
        box.operator(
            "segmentation.create_mesh_from_test_contours",
            text="Create Test Mesh Curves",
            icon='MESH_TORUS'
        )


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


