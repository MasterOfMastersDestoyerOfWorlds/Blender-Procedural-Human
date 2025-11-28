"""
Operator decorator system for automatic registration.

This decorator automatically sets Blender operator attributes based on class name
and manages operator registration.
"""

import bpy
import re
from typing import List, Type, Callable, Any, Optional
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

    if (
        cls_or_kwargs is None
        or isinstance(cls_or_kwargs, str)
        or (kwargs and not isinstance(cls_or_kwargs, type))
    ):

        def wrapper(cls):
            return _process_operator(cls, **kwargs)

        return wrapper

    if isinstance(cls_or_kwargs, type):
        return _process_operator(cls_or_kwargs)

    def wrapper(cls):
        return _process_operator(cls, **kwargs)

    return wrapper


def _to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case, handling acronyms properly.
    
    Examples:
        DSLCreateInstance -> dsl_create_instance
        CreateFinger -> create_finger
        HTTPServer -> http_server
    """
    # Handle transitions: lowercase->uppercase OR uppercase->uppercase+lowercase
    # e.g., "DSLCreate" -> "DSL_Create", "createFinger" -> "create_Finger"
    result = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    # Handle acronym followed by word: "DSLCreate" is now "DSL_Create"
    result = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', result)
    return result.lower()


def _process_operator(cls, **kwargs):
    """Internal processing of the operator class"""

    for key, value in kwargs.items():
        setattr(cls, key, value)

    class_name = cls.__name__
    name_without_prefix = re.sub(r"^PROCEDURAL_OT_", "", class_name)

    if not hasattr(cls, "bl_idname"):
        snake_case = _to_snake_case(name_without_prefix)
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

    _operator_registry.append(cls)
    return cls


def discover_and_register_all_operators():
    """Discover all modules and register all decorated operator classes."""
    from procedural_human.decorators.module_discovery import import_all_modules
    import_all_modules()
    register_all_operators()


def register_all_operators():
    """Register all decorated operator classes."""
    print(f"[Operator Registry] Registering {len(_operator_registry)} operators")
    for op_cls in _operator_registry:
        try:
            bpy.utils.register_class(op_cls)
            print(f"[Operator Registry] Registered: {op_cls.bl_idname}")
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


def dynamic_enum_operator(
    enum_prop_name: str, items_getter: Callable[[], list], **kwargs
):
    """
    Decorator for operators that need dynamic enum properties.

    This decorator:
    - Sets up an enum property that calls items_getter dynamically
    - Adds an invoke method if one doesn't exist to show invoke_props_dialog
    - Ensures enum items are refreshed each time the dialog is shown

    Args:
        enum_prop_name: Name of the enum property to create/update
        items_getter: Callable that returns a list of (identifier, name, description) tuples
        **kwargs: Additional keyword arguments to pass to EnumProperty

    Usage:
        @dynamic_enum_operator("preset_name", get_preset_enum_items)
        @procedural_operator
        class LoadPreset(Operator):
            ...
    """

    def decorator(cls):

        def enum_items_wrapper(self, context):
            items = items_getter()
            # Ensure we return a list
            if not items:
                return [("", "No presets available", "")]
            return items

        enum_prop_kwargs = {
            "name": kwargs.get("name", enum_prop_name.replace("_", " ").title()),
            "items": enum_items_wrapper,
        }

        # Set default to first item if available and not explicitly provided
        if "default" not in kwargs:
            items = items_getter()
            if items and len(items) > 0:
                enum_prop_kwargs["default"] = items[0][0]
        else:
            enum_prop_kwargs["default"] = kwargs["default"]

        for k, v in kwargs.items():
            if k not in ("name", "default"):
                enum_prop_kwargs[k] = v

        enum_prop = bpy.props.EnumProperty(**enum_prop_kwargs)
        setattr(cls, enum_prop_name, enum_prop)

        if not hasattr(cls, "invoke") or cls.invoke == Operator.invoke:

            def invoke(self, context, event):
                return context.window_manager.invoke_props_dialog(self)

            cls.invoke = invoke

        return cls

    return decorator
