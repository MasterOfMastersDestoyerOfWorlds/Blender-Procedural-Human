from typing import Optional
import inspect
import os
from procedural_human.decorators.discoverable_decorator import DiscoverableClassDecorator
from procedural_human.logger import *
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


class register_preset_class(DiscoverableClassDecorator):
    """
    Decorator for registering preset classes.

    The decorated class should inherit from Preset and implement get_data().
    If name is not provided, it will be derived from the class name.
    """
    registry = {}

    @staticmethod
    def setup_decorator(cls, *args, **kwargs):
        for arg in args:
            setattr(cls, arg, arg)
        for key, value in kwargs.items():
            setattr(cls, key, value) 
        name = kwargs.get("name")
        if name:
            display_name = name
        else:

            class_name = cls.__name__
            if class_name.startswith("Preset"):
                display_name = class_name[6:].replace("_", " ")
            else:
                display_name = class_name.replace("_", " ")

        frame = inspect.currentframe()
        try:
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
        
        register_preset_class.registry[display_name] = {
            "instance": preset_instance,
            "location": {
                "file_path": file_path,
                "class_name": cls.__name__,
                "preset_name": display_name,
            },
        }

    @classmethod
    def register_preset_data(cls, name: str, data: dict, file_path: Optional[str] = None):
        """
        Directly register preset data without using a decorator.
        @param name: Display name of the preset
        @param data: Preset data dictionary
        @param file_path: Optional file path where this preset is defined
        """
        register_preset_class.registry[name] = { 
            "instance": lambda: data,
            "location": {
                "file_path": file_path,
                "class_name": None,
                "preset_name": name,
            },
        }



    @classmethod
    def get_preset_location(cls, preset_name: str) -> Optional[dict]:
        """
        Get the file location information for a preset.

        @param preset_name: Name of the preset 
        @return: Dictionary with location information or None if not found
        """
        if preset_name not in register_preset_class.registry:
            return None
        
        preset_entry = register_preset_class.registry[preset_name]
        if isinstance(preset_entry, dict) and "location" in preset_entry:
            return preset_entry["location"]
        
        return None


    @classmethod
    def get_preset(cls, name: str) -> Optional[dict]:
        """
        Get a preset by name.

        @param name: Name of the preset
        @return: Dictionary with preset data or None if not found
        """
        if name not in register_preset_class.registry:
            return None
        
        preset_entry = register_preset_class.registry[name]
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
            logger.info(f"Warning: Failed to load preset '{name}': {e}")
            return None
    @classmethod
    def discover_and_register_all_decorators(cls):
        """
        Discover all modules and register all decorated preset classes.
        """ 
        logger.info(
            f"[Preset Registry] Registering {len(register_preset_class.registry.keys())} presets"
        )
        logger.info(
            f"[Preset Registry] Registered presets: {list(register_preset_class.registry.keys())}"
        )

    @classmethod
    def unregister_all_decorators(cls):
        """
        Unregister all decorated preset classes in reverse order.
        """
        register_preset_class.registry.clear() 