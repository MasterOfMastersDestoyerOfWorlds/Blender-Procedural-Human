"""
Export Profile Curve operator for saving edited curves back to codebase
"""

import bpy
import re
from bpy.types import Operator
from procedural_human.operator_decorator import procedural_operator
from procedural_human.config import get_codebase_path, validate_codebase_path
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import (
    SegmentType,
    ProfileType,
)
from procedural_human.hand.finger.finger_segment.finger_segment_curve_utils import (
    extract_profile_curve_data,
    format_profile_data_as_code,
    normalize_profile_data,
)


@procedural_operator
class ExportProfileCurve(Operator):
    """Export profile curves (X & Y) for selected segments to codebase"""

    @classmethod
    def poll(cls, context):
        codebase = get_codebase_path()
        if not (codebase and validate_codebase_path(codebase)):
            return False

        curves = cls._collect_curve_objects(context)
        return bool(curves)

    @staticmethod
    def _collect_curve_objects(context):
        """Gather curve objects to export based on selection or defaults."""
        curves = set()

        
        selected_curves = [
            obj for obj in context.selected_objects if obj.type == "CURVE"
        ]

        if selected_curves:
            for curve_obj in selected_curves:
                mapping = ExportProfileCurve._detect_profile_mapping(curve_obj.name)
                if mapping:
                    segment_type, _ = mapping
                    
                    for profile_type in ProfileType:
                        curve_name = f"{segment_type.value}_{profile_type.value}"
                        if curve_name in bpy.data.objects:
                            curves.add(bpy.data.objects[curve_name])
                else:
                    curves.add(curve_obj)
        else:
            
            for segment_type in SegmentType:
                for profile_type in ProfileType:
                    curve_name = f"{segment_type.value}_{profile_type.value}"
                    if curve_name in bpy.data.objects:
                        curves.add(bpy.data.objects[curve_name])

        return list(curves)

    @staticmethod
    def _detect_profile_mapping(curve_name: str):
        """Detect segment/profile type from curve object name."""
        name = curve_name.lower()

        segment_type = None
        if "proximal" in name:
            segment_type = SegmentType.PROXIMAL
        elif "middle" in name:
            segment_type = SegmentType.MIDDLE
        elif "distal" in name:
            segment_type = SegmentType.DISTAL

        profile_type = None
        if "x_profile" in name or name.endswith("_x"):
            profile_type = ProfileType.X_PROFILE
        elif "y_profile" in name or name.endswith("_y"):
            profile_type = ProfileType.Y_PROFILE

        if segment_type and profile_type:
            return (segment_type, profile_type)
        return None

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

        curve_objects = self._collect_curve_objects(context)
        if not curve_objects:
            self.report({"ERROR"}, "No suitable curves found to export")
            return {"CANCELLED"}

        backup_file = target_file.with_suffix(".py.backup")
        shutil.copy2(target_file, backup_file)

        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()

        exported = 0
        skipped = []

        for curve_obj in curve_objects:
            mapping = self._detect_profile_mapping(curve_obj.name)
            if not mapping:
                skipped.append(curve_obj.name)
                continue

            segment_type, profile_type = mapping

            curve_data, _ = extract_profile_curve_data(curve_obj)
            curve_data = normalize_profile_data(curve_data)

            variable_name = f"DEFAULT_{profile_type.name}_{segment_type.name}"

            python_code = format_profile_data_as_code(curve_data, variable_name)

            pattern = re.compile(
                rf"^{re.escape(variable_name)}\s*=\s*\{{.*?\n\}}",
                re.MULTILINE | re.DOTALL,
            )

            new_content, replacements = pattern.subn(python_code, content, count=1)
            if replacements == 0:
                skipped.append(curve_obj.name)
                continue

            content = new_content
            exported += 1

        if exported == 0:
            self.report({"ERROR"}, "No curves exported - check names and selection")
            return {"CANCELLED"}

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)

        self.report(
            {"INFO"}, f"Exported {exported} curve(s) to: {target_file.name} (codebase)"
        )
        self.report({"INFO"}, f"Backup saved to: {backup_file.name}")

        if skipped:
            self.report(
                {"WARNING"},
                f"Skipped {len(skipped)} curve(s): {', '.join(sorted(skipped))}",
            )

        return {"FINISHED"}


def register():

    pass


def unregister():

    pass

