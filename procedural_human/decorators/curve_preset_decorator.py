from typing import Optional

_preset_registry: dict = {}  # Maps display_name -> {"instance": PresetInstance, "location": {...}}

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
    import inspect
    import os

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

        # Capture file location
        frame = inspect.currentframe()
        try:
            # Go up the stack to find the file where the decorator is applied
            caller_frame = frame.f_back
            if caller_frame:
                caller_frame = caller_frame.f_back
                if caller_frame:
                    file_path = caller_frame.f_code.co_filename
                    if file_path and os.path.exists(file_path):
                        file_path = os.path.abspath(file_path)
                    else:
                        file_path = None
                else:
                    file_path = None
            else:
                file_path = None
        finally:
            del frame

        preset_instance = cls()
        
        # Store with location metadata
        _preset_registry[display_name] = {
            "instance": preset_instance,
            "location": {
                "file_path": file_path,
                "class_name": cls.__name__,
                "preset_name": display_name,
            },
        }
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


def register_preset_data(name: str, data: dict, file_path: Optional[str] = None):
    """
    Directly register preset data without using a decorator.

    Usage:
        register_preset_data("My Preset", {"key": value, ...})
        
    Args:
        name: Display name of the preset
        data: Preset data dictionary
        file_path: Optional file path where this preset is defined
    """
    _preset_registry[name] = {
        "instance": lambda: data,
        "location": {
            "file_path": file_path,
            "class_name": None,
            "preset_name": name,
        },
    }


def get_all_presets() -> dict:
    """
    Get all registered presets by calling their functions or instances.
    Returns a dictionary mapping display_name -> preset_data.
    """
    presets = {}
    for name, preset_entry in _preset_registry.items():
        try:
            # Handle new format with location metadata
            if isinstance(preset_entry, dict) and "instance" in preset_entry:
                preset_func_or_instance = preset_entry["instance"]
            else:
                # Backward compatibility with old format
                preset_func_or_instance = preset_entry

            if isinstance(preset_func_or_instance, Preset):
                presets[name] = preset_func_or_instance.get_data()
            elif callable(preset_func_or_instance):
                presets[name] = preset_func_or_instance()
            else:
                presets[name] = preset_func_or_instance
        except Exception as e:
            print(f"Warning: Failed to load preset '{name}': {e}")
    return presets


def get_preset_location(preset_name: str) -> Optional[dict]:
    """
    Get the file location information for a preset.
    
    Args:
        preset_name: Name of the preset
        
    Returns:
        Dictionary with location information or None if not found
    """
    if preset_name not in _preset_registry:
        return None
    
    preset_entry = _preset_registry[preset_name]
    if isinstance(preset_entry, dict) and "location" in preset_entry:
        return preset_entry["location"]
    
    return None


def clear_preset_registry():
    """Clear the preset registry (useful for reloading)."""
    _preset_registry.clear()


def get_preset(name: str) -> Optional[dict]:
    """Get a preset by name."""
    if name not in _preset_registry:
        return None
    
    preset_entry = _preset_registry[name]
    try:
        if isinstance(preset_entry, dict) and "instance" in preset_entry:
            preset_func_or_instance = preset_entry["instance"]
        else:
            preset_func_or_instance = preset_entry

        if isinstance(preset_func_or_instance, Preset):
            return preset_func_or_instance.get_data()
        elif callable(preset_func_or_instance):
            return preset_func_or_instance()
        else:
            return preset_func_or_instance
    except Exception as e:
        print(f"Warning: Failed to load preset '{name}': {e}")
        return None


def create_default_profile(profile_type: str = "X") -> list:
    """Create a default flat profile curve."""
    return [
        {"x": 0.0, "y": 0.5, "handle_type": "AUTO"},
        {"x": 0.5, "y": 0.5, "handle_type": "AUTO"},
        {"x": 1.0, "y": 0.5, "handle_type": "AUTO"},
    ]


def get_or_create_preset(name: str, profile_type: str = "X") -> dict:
    """Get a preset by name, or create a default one if it doesn't exist."""
    existing = get_preset(name)
    if existing is not None:
        return existing
    
    default_data = {f"{name}": create_default_profile(profile_type)}
    register_preset_data(name, default_data)
    return default_data


def resolve_profile_chain(name_chain: list, profile_type: str = "X"):
    """
    Resolve a profile by trying a chain of names with progressive fallback.
    
    Returns tuple of (preset_data, resolved_name).
    """
    if not name_chain:
        raise ValueError("name_chain cannot be empty")
    
    for name in name_chain:
        existing = get_preset(name)
        if existing is not None:
            return existing, name
    
    primary_name = name_chain[0]
    default_data = {primary_name: create_default_profile(profile_type)}
    register_preset_data(primary_name, default_data)
    return default_data, primary_name


def build_profile_name_chain(
    context_chain: list,
    component: str,
    index: Optional[int] = None,
    axis: str = "X"
) -> list:
    """Build a chain of profile names for fallback resolution."""
    names = []
    
    index_suffix = f"_{index}" if index is not None else ""
    axis_suffix = f"_{axis}"
    
    for i in range(len(context_chain) + 1):
        prefix_parts = context_chain[i:]
        if prefix_parts:
            prefix = "_".join(prefix_parts) + "_"
        else:
            prefix = ""
        
        name = f"{prefix}{component}{index_suffix}{axis_suffix}"
        names.append(name)
    
    return names


def get_registry_names() -> list:
    """Get all registered preset names."""
    return list(_preset_registry.keys())
