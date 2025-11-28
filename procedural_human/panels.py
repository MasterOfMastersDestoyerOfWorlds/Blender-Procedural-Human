"""
UI Panel classes for Procedural Human Generator

Panels are automatically discovered from the entire procedural_human directory.
Simply decorate your panel class with @procedural_panel and it will be registered.
"""

import bpy
from bpy.types import Panel

from procedural_human.decorators.panel_decorator import (
    procedural_panel,
    discover_and_register_all_panels,
    unregister_all_panels,
)


@procedural_panel
class MainPanel(Panel):
    """Main panel for Procedural Human Generator"""

    bl_label = "Procedural Human"
    bl_idname = "PROCEDURAL_PT_main_panel"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Procedural Human Generator")


def register():
    """Discover and register all panels using the decorator system"""
    discover_and_register_all_panels()


def unregister():
    """Unregister all panels using the decorator system"""
    unregister_all_panels()
