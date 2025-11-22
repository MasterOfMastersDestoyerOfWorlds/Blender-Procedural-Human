"""
Panel decorator system for automatic registration and hierarchy management.

This decorator automatically sets Blender panel attributes based on class name
and file location, and manages parent/child relationships from folder hierarchy.
"""

import bpy
import re
import inspect
from pathlib import Path
from typing import List, Type
from bpy.types import Panel


_panel_registry: List[Type[Panel]] = []


def procedural_panel(cls):
    """
    Decorator for panel classes that automatically sets Blender panel attributes.

    Features:
    - Auto-generates bl_idname from class name (e.g., FingerPanel → PROCEDURAL_PT_finger_panel)
    - Auto-generates bl_label from class name (e.g., FingerPanel → "Finger")
    - Sets standard bl_space_type, bl_region_type, and bl_category
    - Infers parent/child relationships from folder hierarchy

    Usage:
        @procedural_panel
        class FingerPanel(Panel):
            def draw(self, context):
                ...
    """

    module_path = inspect.getfile(cls)
    path_obj = Path(module_path)

    class_name = cls.__name__

    name_without_panel = re.sub(r"Panel$", "", class_name)

    snake_case_name = re.sub(r"(?<!^)(?=[A-Z])", "_", name_without_panel).lower()
    bl_idname = f"PROCEDURAL_PT_{snake_case_name}_panel"

    label_with_spaces = re.sub(r"(?<!^)(?=[A-Z])", " ", name_without_panel)
    bl_label = label_with_spaces

    if not hasattr(cls, "bl_idname"):
        cls.bl_idname = bl_idname
    if not hasattr(cls, "bl_label"):
        cls.bl_label = bl_label
    if not hasattr(cls, "bl_space_type"):
        cls.bl_space_type = "VIEW_3D"
    if not hasattr(cls, "bl_region_type"):
        cls.bl_region_type = "UI"
    if not hasattr(cls, "bl_category"):
        cls.bl_category = "Procedural"

    parts = path_obj.parts
    try:

        base_idx = parts.index("procedural_human")

        relative_parts = list(parts[base_idx + 1 : -1])

        if len(relative_parts) >= 2:
            current_folder = relative_parts[-1]
            parent_folder = relative_parts[-2]

            if current_folder.startswith(parent_folder + "_"):

                parent_bl_idname = f"PROCEDURAL_PT_{parent_folder}_panel"

                if not hasattr(cls, "bl_parent_id"):
                    cls.bl_parent_id = parent_bl_idname
    except (ValueError, IndexError):

        pass

    _panel_registry.append(cls)

    return cls


def register_all_panels():
    """Register all decorated panel classes."""
    for panel_cls in _panel_registry:
        try:
            bpy.utils.register_class(panel_cls)
        except Exception as e:
            print(f"Warning: Failed to register panel {panel_cls.__name__}: {e}")


def unregister_all_panels():
    """Unregister all decorated panel classes in reverse order."""
    for panel_cls in reversed(_panel_registry):
        try:
            bpy.utils.unregister_class(panel_cls)
        except Exception as e:
            print(f"Warning: Failed to unregister panel {panel_cls.__name__}: {e}")


def clear_registry():
    """Clear the panel registry (useful for reloading)."""
    _panel_registry.clear()
