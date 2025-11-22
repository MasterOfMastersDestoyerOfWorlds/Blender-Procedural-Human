"""
Operator decorator system for automatic registration.

This decorator automatically sets Blender operator attributes based on class name
and manages operator registration.
"""

import bpy
import re
from typing import List, Type, Callable, Any
from bpy.types import Operator


_operator_registry: List[Type[Operator]] = []
_preset_registry: dict = {}  


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
    
    
    if cls_or_kwargs is None or isinstance(cls_or_kwargs, str) or (kwargs and not isinstance(cls_or_kwargs, type)):
        def wrapper(cls):
            return _process_operator(cls, **kwargs)
        return wrapper
        
    
    if isinstance(cls_or_kwargs, type):
        return _process_operator(cls_or_kwargs)
        
    
    def wrapper(cls):
        return _process_operator(cls, **kwargs)
    return wrapper


def _process_operator(cls, **kwargs):
    """Internal processing of the operator class"""
    
    
    for key, value in kwargs.items():
        setattr(cls, key, value)

    class_name = cls.__name__
    name_without_prefix = re.sub(r"^PROCEDURAL_OT_", "", class_name)
    
    
    if not hasattr(cls, "bl_idname"):
        snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", name_without_prefix).lower()
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


def dynamic_enum_operator(enum_prop_name: str, items_getter: Callable[[], list], **kwargs):
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
            return items_getter()
        
        
        
        
        enum_prop_kwargs = {
            "name": kwargs.get("name", enum_prop_name.replace("_", " ").title()),
            "items": enum_items_wrapper,
        }
        
        
        if "default" in kwargs:
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


class Preset:
    """
    Base class for preset data.
    Subclasses should implement get_data() to return the preset dictionary.
    """
    
    def get_data(self) -> dict:
        """
        Returns the preset data dictionary.
        Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement get_data()")
    
    def __call__(self):
        """Allow preset instances to be called like functions."""
        return self.get_data()


def register_preset_class(name: str = None):
    """
    Decorator for registering preset classes.
    
    The decorated class should inherit from Preset and implement get_data().
    If name is not provided, it will be derived from the class name.
    
    Usage:
        @register_preset_class("New Finger Style")
        class MyPreset(Preset):
            def get_data(self):
                return {"key": value, ...}
        
        
        @register_preset_class()
        class PresetNewFingerStyle(Preset):
            def get_data(self):
                return {"key": value, ...}
    """
    def decorator(cls):
        
        if not issubclass(cls, Preset):
            
            class PresetWrapper(Preset, cls):
                pass
            PresetWrapper.__name__ = cls.__name__
            PresetWrapper.__module__ = cls.__module__
            cls = PresetWrapper
        
        
        if name:
            display_name = name
        else:
            
            class_name = cls.__name__
            if class_name.startswith("Preset"):
                display_name = class_name[6:].replace("_", " ").title()
            else:
                display_name = class_name.replace("_", " ").title()
        
        
        preset_instance = cls()
        _preset_registry[display_name] = preset_instance
        return cls
    
    
    if callable(name):
        
        cls = name
        name = None
        return decorator(cls)
    else:
        
        return decorator


def register_preset(name: str = None):
    """
    Decorator for registering preset data functions.
    
    The decorated function should return a dictionary containing preset data.
    If name is not provided, it will be derived from the function name.
    
    Usage:
        @register_preset("New Finger Style")
        def get_my_preset():
            return {"key": value, ...}
        
        
        @register_preset()
        def preset_new_finger_style():
            return {"key": value, ...}
    """
    def decorator(func):
        
        if name:
            display_name = name
        else:
            
            func_name = func.__name__
            if func_name.startswith("preset_"):
                display_name = func_name[7:].replace("_", " ").title()
            elif func_name.startswith("get_") and func_name.endswith("_preset"):
                display_name = func_name[4:-7].replace("_", " ").title()
            else:
                display_name = func_name.replace("_", " ").title()
        
        
        _preset_registry[display_name] = func
        return func
    
    
    if callable(name):
        
        func = name
        name = None
        return decorator(func)
    else:
        
        return decorator


def register_preset_data(name: str, data: dict):
    """
    Directly register preset data without using a decorator.
    
    Usage:
        register_preset_data("My Preset", {"key": value, ...})
    """
    _preset_registry[name] = lambda: data


def get_all_presets() -> dict:
    """
    Get all registered presets by calling their functions or instances.
    Returns a dictionary mapping display_name -> preset_data.
    """
    presets = {}
    for name, preset_func_or_instance in _preset_registry.items():
        try:
            
            if isinstance(preset_func_or_instance, Preset):
                presets[name] = preset_func_or_instance.get_data()
            elif callable(preset_func_or_instance):
                presets[name] = preset_func_or_instance()
            else:
                presets[name] = preset_func_or_instance
        except Exception as e:
            print(f"Warning: Failed to load preset '{name}': {e}")
    return presets


def clear_preset_registry():
    """Clear the preset registry (useful for reloading)."""
    _preset_registry.clear()
