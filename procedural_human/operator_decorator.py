"""
Operator decorator system for automatic registration.

This decorator automatically sets Blender operator attributes based on class name
and manages operator registration.
"""

import bpy
import re
from typing import List, Type
from bpy.types import Operator


_operator_registry: List[Type[Operator]] = []


def procedural_operator(cls):
    """
    Decorator for operator classes that automatically sets Blender operator attributes.

    Features:
    - Auto-generates bl_idname from class name (e.g., CreateFinger → mesh.procedural_create_finger)
    - Auto-generates bl_label from class name (e.g., CreateFinger → "Create Finger")
    - Uses class docstring for bl_description (first line becomes both label and description)
    - Sets default bl_options = {'REGISTER', 'UNDO'}
    - Allows optional override of any bl_* attributes

    Usage:
        @procedural_operator
        class CreateFinger(Operator):
            '''Create a procedural finger with Geometry Nodes'''

            def execute(self, context):
                ...
    """

    class_name = cls.__name__

    name_without_prefix = re.sub(r"^PROCEDURAL_OT_", "", class_name)

    snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", name_without_prefix).lower()

    bl_idname = f"mesh.procedural_{snake_case}"

    if not hasattr(cls, "bl_idname"):
        cls.bl_idname = bl_idname

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

    _operator_registry.append(cls)

    return cls


def register_all_operators():
    """Register all decorated operator classes."""
    for op_cls in _operator_registry:
        try:
            bpy.utils.register_class(op_cls)
        except Exception as e:
            print(f"Warning: Failed to register operator {op_cls.__name__}: {e}")


def unregister_all_operators():
    """Unregister all decorated operator classes in reverse order."""
    for op_cls in reversed(_operator_registry):
        try:
            bpy.utils.unregister_class(op_cls)
        except Exception as e:
            print(f"Warning: Failed to unregister operator {op_cls.__name__}: {e}")


def clear_registry():
    """Clear the operator registry (useful for reloading)."""
    _operator_registry.clear()


__all__ = [
    "procedural_operator",
    "register_all_operators",
    "unregister_all_operators",
    "clear_registry",
]
