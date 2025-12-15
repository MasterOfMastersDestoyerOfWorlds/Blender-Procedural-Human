"""
Panel decorator system for automatic registration and hierarchy management.

This decorator automatically sets Blender panel attributes based on class name
and file location, and manages parent/child relationships from folder hierarchy.
"""

import bpy
import re
import inspect
from pathlib import Path
from procedural_human.decorators.discoverable_decorator import (
    DiscoverableClassDecorator,
)
from procedural_human.decorators.module_discovery import import_all_modules
from procedural_human.logger import *


class procedural_panel(DiscoverableClassDecorator):
    registry = {}
    """
    Decorator for panel classes that automatically sets Blender panel attributes.
    """

    @staticmethod
    def setup_decorator(cls, **kwargs):
        module_path = inspect.getfile(cls)
        path_obj = Path(module_path)

        class_name = cls.__name__

        name_without_panel = re.sub(r"Panel$", "", class_name)

        snake_case_name = DiscoverableClassDecorator.to_snake_case(name_without_panel)
        bl_idname = f"PROCEDURAL_PT_{snake_case_name}_panel"

        label_with_spaces = DiscoverableClassDecorator.to_title_with_spaces(
            name_without_panel
        )
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

        procedural_panel.registry[cls.__name__] = cls

    @classmethod
    def discover_and_register_all_decorators(cls):
        """
        Discover all modules and register all decorated panel classes.
        """
        logger.info(
            f"[Panel Registry] Registering {len(procedural_panel.registry.keys())} panels"
        )
        for panel_cls in procedural_panel.registry.values():
            try:
                bpy.utils.register_class(panel_cls)
            except Exception as e:
                logger.info(
                    f"Warning: Failed to register panel {panel_cls.__name__}: {e}"
                )

        logger.info(
            f"[Panel Registry] Registered: {[panel_cls.bl_idname for panel_cls in procedural_panel.registry.values()]}"
        )

    @classmethod
    def unregister_all_decorators(cls):
        """
        Unregister all decorated panel classes in reverse order.
        """
        for panel_cls in reversed(procedural_panel.registry.values()):
            try:
                bpy.utils.unregister_class(panel_cls)
            except Exception as e:
                logger.info(
                    f"Warning: Failed to unregister panel {panel_cls.__name__}: {e}"
                )
        procedural_panel.registry.clear()
