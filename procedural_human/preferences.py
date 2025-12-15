"""
Addon preferences for Procedural Human Generator
"""

import bpy
from bpy.types import AddonPreferences, Operator
from bpy.props import StringProperty
from pathlib import Path
from procedural_human.logger import *
from procedural_human.decorators.operator_decorator import procedural_operator


class ProceduralHumanPreferences(AddonPreferences):
    """Preferences for the Procedural Human Generator addon"""

    bl_idname = "procedural_human"

    codebase_path: StringProperty(
        name="Codebase Path",
        description="Path to the Procedural Human development codebase (for exporting modifications)",
        default="",
        subtype="DIR_PATH",
    )

    def draw(self, context):
        layout = self.layout

        from procedural_human import _MISSING_DEPENDENCIES, check_dependencies

        missing = check_dependencies()
        if missing:
            dep_box = layout.box()
            dep_box.label(text="Missing Dependencies:", icon="ERROR")
            dep_box.label(text="(Auto-install failed - try as admin)", icon="INFO")
            for import_name, pip_name in missing:
                dep_box.label(text=f"  • {pip_name}", icon="DOT")
            dep_box.operator(
                "wm.procedural_install_dependencies",
                text="Retry Install",
                icon="FILE_REFRESH",
            )
            layout.separator()

        layout.label(text="Development Settings:", icon="SETTINGS")

        box = layout.box()
        box.label(text="Codebase Path Configuration:")
        box.prop(self, "codebase_path")

        from procedural_human.config import (
            detect_codebase_path,
            get_codebase_path,
            validate_codebase_path,
        )

        detected = detect_codebase_path()
        current = get_codebase_path()

        info_box = layout.box()
        info_box.label(text="Path Detection Info:", icon="INFO")

        if detected:
            row = info_box.row()
            row.label(text=f"Auto-Detected: {detected}")
            if validate_codebase_path(detected):
                row.label(text="", icon="CHECKMARK")
            else:
                row.label(text="(Invalid)", icon="ERROR")
        else:
            info_box.label(text="Auto-Detected: None", icon="ERROR")

        if current:
            row = info_box.row()
            row.label(text=f"Current: {current}")
            if validate_codebase_path(current):
                row.label(text="", icon="CHECKMARK")
            else:
                row.label(text="(Invalid)", icon="ERROR")
        else:
            info_box.label(text="Current: None (configure above)", icon="ERROR")

        row = layout.row()
        row.operator(
            "wm.procedural_refresh_codebase_path",
            text="Refresh Detection",
            icon="FILE_REFRESH",
        )

        help_box = layout.box()
        help_box.label(text="Help:", icon="QUESTION")
        help_box.label(
            text="• Auto-detection walks up from addon location to find project root"
        )
        help_box.label(text="• Looks for .git, pyproject.toml, or uv.lock markers")
        help_box.label(text="• Set manual path above if auto-detection fails")
        help_box.label(
            text="• Path is used when exporting profile curves to source code"
        )


@procedural_operator(bl_idname="wm.procedural_refresh_codebase_path")
class RefreshCodebasePath(Operator):
    """Refresh codebase path detection"""

    bl_options = {"INTERNAL"}

    def execute(self, context):
        from procedural_human.config import clear_cache, get_codebase_path

        clear_cache()
        new_path = get_codebase_path()

        if new_path:
            self.report({"INFO"}, f"Detected codebase at: {new_path}")
        else:
            self.report(
                {"WARNING"}, "Could not auto-detect codebase path. Please set manually."
            )

        return {"FINISHED"}


@procedural_operator(bl_idname="wm.procedural_install_dependencies")
class InstallDependencies(Operator):
    """Retry installing required Python packages into Blender's Python"""

    bl_options = {"INTERNAL"}

    def execute(self, context):
        from procedural_human import (
            check_dependencies,
            install_package,
            ensure_pip,
        )
        import procedural_human

        missing = check_dependencies()
        if not missing:
            self.report({"INFO"}, "All dependencies are already installed!")
            return {"FINISHED"}

        if not ensure_pip():
            self.report(
                {"ERROR"}, "Could not ensure pip is available. Run Blender as admin."
            )
            return {"CANCELLED"}

        all_success = True
        for import_name, pip_name in missing:
            self.report({"INFO"}, f"Installing {pip_name}...")
            success, message = install_package(pip_name)
            if success:
                self.report({"INFO"}, message)
            else:
                self.report({"ERROR"}, message)
                all_success = False

        procedural_human._DEPENDENCIES_CHECKED = False
        procedural_human._DEPENDENCIES_INSTALLED = False
        procedural_human._MISSING_DEPENDENCIES = []

        final_missing = check_dependencies()
        if not final_missing:
            self.report({"INFO"}, "All dependencies installed! Please restart Blender.")
        else:
            self.report(
                {"WARNING"},
                "Some dependencies failed. Try running Blender as administrator.",
            )

        return {"FINISHED"}


def register():
    try:
        bpy.utils.register_class(ProceduralHumanPreferences)
    except Exception as e:
        logger.info(f"Warning: Failed to register ProceduralHumanPreferences: {e}")


def unregister():
    try:
        bpy.utils.unregister_class(ProceduralHumanPreferences)
    except Exception as e:
        logger.info(f"Warning: Failed to unregister ProceduralHumanPreferences: {e}")
