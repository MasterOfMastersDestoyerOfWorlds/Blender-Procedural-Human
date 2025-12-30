"""
Operator decorator system for automatic registration.

This decorator automatically sets Blender operator attributes based on class name
and manages operator registration.
"""

import bpy
import re
from procedural_human.decorators.discoverable_decorator import (
    DiscoverableClassDecorator,
)
from procedural_human.logger import *


class procedural_operator(DiscoverableClassDecorator):
    """
    Decorator for operator classes that automatically sets Blender operator attributes.
    """

    registry = {}

    @staticmethod
    def setup_decorator(cls, **kwargs):
        for key, value in kwargs.items():
            setattr(cls, key, value)
        class_name = cls.__name__
        name_without_prefix = re.sub(r"^PROCEDURAL_OT_", "", class_name)

        if not hasattr(cls, "bl_idname"):
            snake_case = DiscoverableClassDecorator.to_snake_case(name_without_prefix)
            cls.bl_idname = f"mesh.procedural_{snake_case}"

        if not hasattr(cls, "bl_label"):
            bl_label = re.sub(r"(?<!^)(?=[A-Z])", " ", name_without_prefix)
            cls.bl_label = bl_label

        if not hasattr(cls, "bl_description"):
            if cls.__doc__:
                description = cls.__doc__.strip().split("\n")[0].strip()
                cls.bl_description = description
            else:
                cls.bl_description = cls.bl_label

        if not hasattr(cls, "bl_options"):
            cls.bl_options = {"REGISTER", "UNDO"}

        procedural_operator.registry[cls.__name__] = cls

    @classmethod
    def discover_and_register_all_decorators(cls):
        """
        Discover all modules and register all decorated operator classes.
        """
        logger.info(
            f"[Operator Registry] Registering {len(procedural_operator.registry.keys())} operators"
        )
        for op_cls in procedural_operator.registry.values():
            try:
                # Unregister first if already registered (hot-reload support)
                try:
                    bpy.utils.unregister_class(op_cls)
                except RuntimeError:
                    pass
                bpy.utils.register_class(op_cls)
            except Exception as e:
                logger.info(
                    f"Warning: Failed to register operator {op_cls.__name__}: {e}"
                )
        logger.info(
            f"[Operator Registry] Registered: {[op_cls.bl_idname for op_cls in procedural_operator.registry.values()]}"
        )

    @classmethod
    def unregister_all_decorators(cls):
        """
        Unregister all decorated operator classes in reverse order.
        """
        for op_cls in reversed(procedural_operator.registry.values()):
            try:
                bpy.utils.unregister_class(op_cls)
            except Exception as e:
                logger.info(
                    f"Warning: Failed to unregister operator {op_cls.__name__}: {e}"
                )
        procedural_operator.registry.clear()
