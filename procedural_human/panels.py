"""
UI Panel classes for Procedural Human Generator
"""

import bpy
from bpy.types import Panel

from .hand.finger.finger_operator import finger_panel

class PROCEDURAL_PT_main_panel(Panel):
    bl_label = "Procedural Human"
    bl_idname = "OBJECT_PT_procedural_human"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Procedural"

    def draw(self, context):
        layout = self.layout
        finger_panel.draw(self, context)


def register():
    bpy.utils.register_class(PROCEDURAL_PT_main_panel)


def unregister():
    bpy.utils.unregister_class(PROCEDURAL_PT_main_panel)
