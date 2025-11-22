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


def procedural_operator(cls_or_kwargs=None, **kwargs):
    """
    Decorator for operator classes that automatically sets Blender operator attributes.
    
    Can be used as @procedural_operator or @procedural_operator(bl_idname="my.id")
    
    Features:
    - Auto-generates bl_idname from class name if not provided (e.g., CreateFinger → mesh.procedural_create_finger)
    - Auto-generates bl_label from class name if not provided
    - Uses class docstring for bl_description if not provided
    - Sets default bl_options = {'REGISTER', 'UNDO'} if not provided
    """
    
    # Case 1: Decorator used with arguments @procedural_operator(bl_idname="...")
    if cls_or_kwargs is None or isinstance(cls_or_kwargs, str) or (kwargs and not isinstance(cls_or_kwargs, type)):
        def wrapper(cls):
            return _process_operator(cls, **kwargs)
        return wrapper
        
    # Case 2: Decorator used without arguments @procedural_operator
    if isinstance(cls_or_kwargs, type):
        return _process_operator(cls_or_kwargs)
        
    # Fallback for mixed usage
    def wrapper(cls):
        return _process_operator(cls, **kwargs)
    return wrapper


def _process_operator(cls, **kwargs):
    """Internal processing of the operator class"""
    
    # Apply manually passed kwargs first (e.g. bl_idname from decorator args)
    for key, value in kwargs.items():
        setattr(cls, key, value)

    class_name = cls.__name__
    name_without_prefix = re.sub(r"^PROCEDURAL_OT_", "", class_name)
    
    # Auto-generate bl_idname if not set
    if not hasattr(cls, "bl_idname"):
        snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", name_without_prefix).lower()
        cls.bl_idname = f"mesh.procedural_{snake_case}"

    # Auto-generate bl_label if not set
    if not hasattr(cls, "bl_label"):
        bl_label = re.sub(r"(?<!^)(?=[A-Z])", " ", name_without_prefix)
        cls.bl_label = bl_label

    # Auto-generate bl_description if not set
    if not hasattr(cls, "bl_description"):
        if cls.__doc__:
            description = cls.__doc__.strip().split("\n")[0].strip()
            cls.bl_description = description
        else:
            cls.bl_description = cls.bl_label

    # Set default bl_options if not set
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
