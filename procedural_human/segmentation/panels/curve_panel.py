"""
Curve insertion panel for the segmentation workflow.

Provides UI for inserting curves into the 3D scene.
"""

import bpy
from bpy.types import Panel

from procedural_human.decorators.panel_decorator import procedural_panel


@procedural_panel
class CurveInsertionPanel(Panel):
    """Curve insertion controls for 3D View"""
    
    bl_label = "Curve Insertion"
    bl_idname = "PROCEDURAL_PT_curve_insertion"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Segmentation"
    
    def draw(self, context):
        layout = self.layout
        selected_curves = [obj for obj in context.selected_objects if obj.type == 'CURVE']
        
        box = layout.box()
        box.label(text="Selected Curves", icon='CURVE_DATA')
        box.label(text=f"  {len(selected_curves)} curve(s) selected")
        
        if not selected_curves:
            box.operator(
                "segmentation.select_curves",
                text="Select Segmentation Curves",
                icon='RESTRICT_SELECT_OFF'
            )
        layout.separator()
        box = layout.box()
        box.label(text="Create New Object", icon='ADD')
        
        col = box.column(align=True)
        col.enabled = len(selected_curves) > 0
        col.operator(
            "segmentation.insert_curve_new_object",
            text="Create Lofted Object",
            icon='MESH_DATA'
        )
        
        col.scale_y = 0.7
        col.label(text="Uses LoftSpheriod node group")
        layout.separator()
        box = layout.box()
        box.label(text="Add to Existing Object", icon='LINKED')
        
        col = box.column(align=True)
        col.enabled = len(selected_curves) > 0
        col.operator(
            "segmentation.insert_curve_existing",
            text="Add Curves to Object",
            icon='CONSTRAINT'
        )
        
        col.scale_y = 0.7
        col.label(text="With 90° rotation offset")
        layout.separator()
        box = layout.box()
        box.label(text="Workspace", icon='WORKSPACE')
        box.operator(
            "workspace.open_curve_segmentation",
            text="Open Segmentation Workspace",
            icon='WINDOW'
        )


@procedural_panel
class CurveInsertionOptionsPanel(Panel):
    """Advanced curve insertion options"""
    
    bl_label = "Insertion Options"
    bl_idname = "PROCEDURAL_PT_curve_insertion_options"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Segmentation"
    bl_parent_id = "PROCEDURAL_PT_curve_insertion"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Target Object", icon='OBJECT_DATA')
        mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
        
        if mesh_objects:
            for obj in mesh_objects[:5]:  # Show first 5
                row = box.row()
                icon = 'RADIOBUT_ON' if obj == context.active_object else 'RADIOBUT_OFF'
                row.label(text=obj.name, icon=icon)
        else:
            box.label(text="  No mesh objects in scene")
        layout.separator()
        box = layout.box()
        box.label(text="Default Rotation", icon='ORIENTATION_GIMBAL')
        
        col = box.column(align=True)
        col.scale_y = 0.8
        col.label(text="XY Plane: 90°")
        col.label(text="Z Aligned")
        col.label(text="(Configurable in operator)")


@procedural_panel
class SegmentationCurvesListPanel(Panel):
    """List of curves created from segmentation"""
    
    bl_label = "Segmentation Curves"
    bl_idname = "PROCEDURAL_PT_segmentation_curves_list"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Segmentation"
    bl_parent_id = "PROCEDURAL_PT_curve_insertion"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        seg_curves = [
            obj for obj in bpy.data.objects 
            if obj.type == 'CURVE' and obj.name.startswith("Segment")
        ]
        
        if seg_curves:
            box = layout.box()
            for curve in seg_curves[:10]:  # Show first 10
                row = box.row()
                icon = 'CHECKBOX_HLT' if curve.select_get() else 'CHECKBOX_DEHLT'
                op = row.operator(
                    "object.select_pattern",
                    text="",
                    icon=icon,
                    emboss=False
                )
                op.pattern = curve.name
                op.extend = True
                
                row.label(text=curve.name)
                op = row.operator(
                    "object.delete",
                    text="",
                    icon='X',
                    emboss=False
                )
            
            if len(seg_curves) > 10:
                layout.label(text=f"  ... and {len(seg_curves) - 10} more")
        else:
            layout.label(text="No segmentation curves found")


