"""
Finger segment panel for UI controls
"""

from bpy.types import Panel
from procedural_human.panel_decorator import procedural_panel
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import (
    SegmentType,
)
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)


@procedural_panel
class FingerSegmentPanel(Panel):
    """Panel for finger segment properties and profile curves"""

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        row = box.row()
        icon = "TRIA_DOWN" if scene.procedural_finger_segment_expanded else "TRIA_RIGHT"
        row.prop(
            scene,
            "procedural_finger_segment_expanded",
            icon=icon,
            emboss=False,
            text="",
        )
        row.label(text="Segment Profile Curves")

        if scene.procedural_finger_segment_expanded:
            content_box = box.box()

            content_box.label(text="Sampling Settings:", icon="MODIFIER")
            row = content_box.row()
            row.prop(
                scene, "procedural_finger_segment_sample_count", text="Sample Count"
            )
            row.label(text="", icon="QUESTION")
            row.active = False

            content_box.separator()

            content_box.separator()
            info_row = content_box.row()
            info_row.label(text="Select curve objects from the scene", icon="INFO")

            content_box.separator()
            export_box = content_box.box()
            export_box.label(text="Development Tools:", icon="TOOL_SETTINGS")

            from procedural_human.config import (
                get_codebase_path,
                validate_codebase_path,
            )

            codebase = get_codebase_path()

            if codebase and validate_codebase_path(codebase):
                status_row = export_box.row()
                status_row.label(text=f"Codebase: {codebase.name}", icon="CHECKMARK")

                export_row = export_box.row()
                export_row.operator(
                    "mesh.procedural_export_profile_curve",
                    text="Export Curve Object Profiles",
                    icon="EXPORT",
                )

                export_box.separator()
                export_box.label(text="Float Curve Presets:", icon="GRAPH")
                row = export_box.row(align=True)
                row.operator(
                    "node.procedural_save_float_curve_preset",
                    text="Save All Curves to Preset",
                    icon="IMPORT",
                )
                row.operator(
                    "node.procedural_load_float_curve_preset",
                    text="Load Preset",
                    icon="EXPORT",
                )

            else:
                status_row = export_box.row()
                status_row.label(text="Codebase not configured", icon="ERROR")
                config_row = export_box.row()
                config_row.label(text="Set path in addon preferences")
                config_row.operator("screen.userpref_show", text="", icon="PREFERENCES")
