

from bpy.types import Panel

from procedural_human import operator_utils

class finger_panel(Panel):
    bl_idname = "PROCEDURAL_PT_finger_panel"
    bl_label = "Finger Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Procedural"

    def draw(self, context):
        layout = self.layout
        finger_box = layout.box()
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