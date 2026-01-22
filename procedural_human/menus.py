"""
Menu classes for Procedural Human Generator
"""

import bpy
from bpy.types import Menu


class PROCEDURAL_MT_add_menu(Menu):
    bl_idname = "PROCEDURAL_MT_add_menu"
    bl_label = "Procedural"

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.procedural_finger", text="Procedural Finger")


def menu_func(self, context):
    self.layout.menu("PROCEDURAL_MT_add_menu")


def register():
    try:
        bpy.utils.unregister_class(PROCEDURAL_MT_add_menu)
    except RuntimeError:
        pass
    
    bpy.utils.register_class(PROCEDURAL_MT_add_menu)
    try:
        bpy.types.VIEW3D_MT_add.remove(menu_func)
    except ValueError:
        pass
    bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
    try:
        bpy.utils.unregister_class(PROCEDURAL_MT_add_menu)
    except RuntimeError:
        pass
    try:
        bpy.types.VIEW3D_MT_add.remove(menu_func)
    except ValueError:
        pass
