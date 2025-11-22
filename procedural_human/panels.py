"""
UI Panel classes for Procedural Human Generator
"""

import bpy
from bpy.types import Panel


from .hand.finger.finger_panel import FingerPanel
from .hand.finger.finger_nail.finger_nail_panel import FingerNailPanel
from .hand.finger.finger_segment.finger_segment_panel import FingerSegmentPanel
from .panel_decorator import procedural_panel, register_all_panels, unregister_all_panels


@procedural_panel
class MainPanel(Panel):
    """Main panel for Procedural Human Generator"""
    
    
    bl_label = "Procedural Human"
    bl_idname = "PROCEDURAL_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Procedural Human Generator")


def register():
    """Register all panels using the decorator system"""
    register_all_panels()


def unregister():
    """Unregister all panels using the decorator system"""
    unregister_all_panels()
