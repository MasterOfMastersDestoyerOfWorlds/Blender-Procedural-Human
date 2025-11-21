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
    - Sets default bl_options = {'REGISTER', 'UNDO'}
    - Allows optional override of any bl_* attributes
    
    Usage:
        @procedural_operator
        class CreateFinger(Operator):
            bl_label = "Create Procedural Finger"
            
            def execute(self, context):
                ...
    """
    
    class_name = cls.__name__
    
    # Generate bl_idname from class name
    # Remove PROCEDURAL_OT_ prefix if present
    name_without_prefix = re.sub(r'^PROCEDURAL_OT_', '', class_name)
    
    # Convert CamelCase to snake_case
    snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', name_without_prefix).lower()
    
    # Generate bl_idname with mesh.procedural_ prefix
    bl_idname = f"mesh.procedural_{snake_case}"
    
    # Set bl_idname if not explicitly set
    if not hasattr(cls, 'bl_idname'):
        cls.bl_idname = bl_idname
    
    # Set default bl_options if not explicitly set
    if not hasattr(cls, 'bl_options'):
        cls.bl_options = {'REGISTER', 'UNDO'}
    
    # Add to registry
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
    'procedural_operator',
    'register_all_operators',
    'unregister_all_operators',
    'clear_registry',
]

