"""
Export Profile Curve operator for saving edited curves back to codebase
"""

import bpy
import re
from bpy.types import Operator
from bpy.props import EnumProperty
from pathlib import Path
from procedural_human.operator_decorator import procedural_operator
from procedural_human.config import get_codebase_path, validate_codebase_path
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import (
    SegmentType,
    ProfileType,
)
from procedural_human.hand.finger.finger_segment.finger_segment_curve_utils import (
    extract_profile_curve_data,
    format_profile_data_as_code,
)


@procedural_operator
class ExportProfileCurve(Operator):
    """Export selected curve to profile curve code in codebase"""

    segment_type: EnumProperty(
        name="Segment Type",
        items=[
            ("PROXIMAL", "Proximal", "Proximal segment (closest to hand)"),
            ("MIDDLE", "Middle", "Middle segment"),
            ("DISTAL", "Distal", "Distal segment (fingertip)"),
        ],
        default="PROXIMAL",
        description="Which finger segment this profile is for",
    )

    profile_type: EnumProperty(
        name="Profile Type",
        items=[
            ("X_PROFILE", "X Profile", "X-axis profile curve"),
            ("Y_PROFILE", "Y Profile", "Y-axis profile curve"),
        ],
        default="X_PROFILE",
        description="Which profile axis this curve represents",
    )

    @classmethod
    def poll(cls, context):

        if not context.active_object or context.active_object.type != "CURVE":
            return False

        codebase = get_codebase_path()
        return codebase and validate_codebase_path(codebase)

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Export Curve to Profile Data:")
        layout.prop(self, "segment_type")
        layout.prop(self, "profile_type")

        codebase = get_codebase_path()
        if codebase:
            target_file = (
                codebase
                / "procedural_human/hand/finger/finger_segment/finger_segment_profiles.py"
            )
            box = layout.box()
            box.label(text="Target File:", icon="FILE")
            box.label(text=str(target_file))

    def execute(self, context):
        import shutil

        codebase = get_codebase_path()
        if not codebase:
            self.report({"ERROR"}, "Codebase path not configured")
            return {"CANCELLED"}

        target_file = (
            codebase
            / "procedural_human/hand/finger/finger_segment/finger_segment_profiles.py"
        )

        if not target_file.exists():
            self.report({"ERROR"}, f"Codebase file not found: {target_file}")
            self.report({"INFO"}, "Please check addon preferences for codebase path")
            return {"CANCELLED"}

        curve_data, _ = extract_profile_curve_data(context.active_object)

        variable_name = f"DEFAULT_{self.profile_type}_{self.segment_type}"

        python_code = format_profile_data_as_code(curve_data, variable_name)

        backup_file = target_file.with_suffix(".py.backup")
        shutil.copy2(target_file, backup_file)

        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = re.compile(
            rf"^{re.escape(variable_name)}\s*=\s*\{{.*?\n\}}", re.MULTILINE | re.DOTALL
        )

        if pattern.search(content):
            new_content = pattern.sub(python_code, content)
        else:
            self.report({"ERROR"}, f"Could not find {variable_name} in file")
            return {"CANCELLED"}

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(new_content)

        self.report({"INFO"}, f"Exported {variable_name} to: {target_file}")
        self.report({"INFO"}, f"Backup saved to: {backup_file}")

        return {"FINISHED"}


def register():

    pass


def unregister():

    pass


__all__ = ["ExportProfileCurve", "register", "unregister"]
