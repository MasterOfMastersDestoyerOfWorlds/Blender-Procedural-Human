"""
Finger nail panel for UI controls
"""

from bpy.types import Panel
from procedural_human.panel_decorator import procedural_panel


@procedural_panel
class FingerNailPanel(Panel):
    """Panel for finger nail properties"""

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        row = box.row()
        icon = "TRIA_DOWN" if scene.procedural_finger_nail_expanded else "TRIA_RIGHT"
        row.prop(
            scene, "procedural_finger_nail_expanded", icon=icon, emboss=False, text=""
        )
        row.label(text="Nail Properties")

        if scene.procedural_finger_nail_expanded:
            content_box = box.box()

            if context.active_object and hasattr(context.active_object, "finger_data"):
                finger_data = context.active_object.finger_data
                if hasattr(finger_data, "nail_size"):
                    content_box.prop(finger_data, "nail_size", text="Nail Size")

            content_box.label(text="Nail customization options")
