from bpy.types import Panel

from procedural_human import operator_utils
from procedural_human.panel_decorator import procedural_panel


@procedural_panel
class FingerPanel(Panel):
    """Main panel for finger operations"""

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        row = box.row()
        icon = "TRIA_DOWN" if scene.procedural_finger_expanded else "TRIA_RIGHT"
        row.prop(scene, "procedural_finger_expanded", icon=icon, emboss=False, text="")
        row.label(text="Finger Operations")

        if scene.procedural_finger_expanded:
            finger_box = box.box()
            operator_utils.create_geometry_nodes_modifier(finger_box, context, "Finger")

            if hasattr(context.scene, "procedural_finger_type"):
                finger_box.prop(context.scene, "procedural_finger_type", text="Type")
                finger_box.prop(
                    context.scene, "procedural_finger_curl_direction", text="Curl"
                )

            if context.active_object and "finger_type" in context.active_object:
                info_box = finger_box.box()
                info_box.label(
                    text=f"Selected: {context.active_object.get('finger_type', 'Unknown')} finger"
                )
                info_box.label(
                    text=f"Curl: {context.active_object.get('curl_direction', 'Unknown')}"
                )
