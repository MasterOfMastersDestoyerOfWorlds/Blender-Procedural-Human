"""
UI Panel classes for Procedural Human Generator
"""

import bpy
from bpy.types import Panel


class PROCEDURAL_PT_main_panel(Panel):
    bl_label = "Procedural Human"
    bl_idname = "OBJECT_PT_procedural_human"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Procedural"

    def draw(self, context):
        layout = self.layout

        # Main creation button
        layout.operator("mesh.procedural_human", text="Create Full Human")

        # Component creation
        box = layout.box()
        box.label(text="Components:")
        row = box.row()
        row.operator("mesh.procedural_torso", text="Torso")
        row.operator("mesh.procedural_head", text="Head")
        
        # Finger operations
        finger_box = layout.box()
        finger_box.label(text="Finger Operations:")
        
        # Display scene properties for finger creation
        if hasattr(context.scene, "procedural_finger_type"):
            finger_box.prop(context.scene, "procedural_finger_type", text="Type")
            finger_box.prop(context.scene, "procedural_finger_curl_direction", text="Curl")
        
        # Create Finger operator - properties will be shown in operator dialog
        finger_box.operator("mesh.procedural_finger", text="Create Finger")
        
        # Realize Geometry button
        finger_box.operator("mesh.procedural_realize_finger", text="Realize Geometry")
        
        # Armature section - finger type is read from object custom property
        finger_box.separator()
        if hasattr(context.scene, "procedural_finger_create_animation"):
            finger_box.prop(context.scene, "procedural_finger_create_animation", text="Create Animation")
        
        # Add Armature operator - reads finger type from selected object
        finger_box.operator("mesh.procedural_add_finger_armature", text="Add Armature")
        
        # Show finger info if an object is selected
        if context.active_object and "finger_type" in context.active_object:
            info_box = finger_box.box()
            info_box.label(text=f"Selected: {context.active_object.get('finger_type', 'Unknown')} finger")
            info_box.label(text=f"Curl: {context.active_object.get('curl_direction', 'Unknown')}")


# Note: Parameters are set directly on operators when run


# Registration
def register():
    bpy.utils.register_class(PROCEDURAL_PT_main_panel)


def unregister():
    bpy.utils.unregister_class(PROCEDURAL_PT_main_panel)
