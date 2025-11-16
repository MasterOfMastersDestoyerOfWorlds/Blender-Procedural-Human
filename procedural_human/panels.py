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
        row = box.row()
        row.operator("mesh.procedural_finger", text="Finger")


# Note: Parameters are set directly on operators when run


# Registration
def register():
    bpy.utils.register_class(PROCEDURAL_PT_main_panel)


def unregister():
    bpy.utils.unregister_class(PROCEDURAL_PT_main_panel)
