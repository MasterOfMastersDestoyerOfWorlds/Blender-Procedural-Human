"""
DSL definition decorator system for automatic registration.

This decorator registers DSL definition files so they can be discovered
without scanning the entire dsl directory.
"""

from typing import Dict, List, Optional, Type, Any
import os
import inspect


_dsl_definition_registry: Dict[str, Dict[str, Any]] = {}
_definitions_loaded: bool = False


def ensure_definitions_loaded() -> None:
    """
    Ensure DSL definition modules have been imported and decorators triggered.
    
    This triggers module discovery if the registry is empty, ensuring that
    files like finger.py get imported and their @dsl_definition decorators
    populate the registry.
    """
    global _definitions_loaded
    
    if _definitions_loaded:
        return
    
    if not _dsl_definition_registry:
        try:
            from procedural_human.decorators.module_discovery import import_all_modules
            print("[DSL Definition Registry] Registry empty, triggering module discovery...")
            import_all_modules()
        except ImportError:
            pass
    
    _definitions_loaded = True


def dsl_definition(cls: Type) -> Type:
    """
    Decorator for DSL definition classes.
    
    Registers the class in the DSL definition registry for discovery.
    The file path is automatically detected from the class module.
    
    Usage:
        @dsl_definition
        class Finger:
            def __init__(self, ...):
                ...
        
        Index = Finger(...)
    """
    module = inspect.getmodule(cls)
    if module and hasattr(module, '__file__'):
        file_path = module.__file__
    else:
        file_path = "unknown"
    
    class_name = cls.__name__
    
    if file_path not in _dsl_definition_registry:
        _dsl_definition_registry[file_path] = {
            "file_path": file_path,
            "classes": [],
            "instances": [],
        }
    
    if class_name not in _dsl_definition_registry[file_path]["classes"]:
        _dsl_definition_registry[file_path]["classes"].append(class_name)
    
    return cls


def register_dsl_instance(file_path: str, instance_name: str) -> None:
    """
    Register a DSL instance manually.
    
    Called when module-level instances are created (e.g., Index = Finger(...)).
    """
    if file_path not in _dsl_definition_registry:
        _dsl_definition_registry[file_path] = {
            "file_path": file_path,
            "classes": [],
            "instances": [],
        }
    
    if instance_name not in _dsl_definition_registry[file_path]["instances"]:
        _dsl_definition_registry[file_path]["instances"].append(instance_name)


def get_all_dsl_definitions() -> Dict[str, Dict[str, Any]]:
    """Get all registered DSL definitions."""
    ensure_definitions_loaded()
    return _dsl_definition_registry.copy()


def get_dsl_files() -> List[str]:
    """Get list of all registered DSL file paths."""
    ensure_definitions_loaded()
    return list(_dsl_definition_registry.keys())


def get_dsl_instances_for_file(file_path: str) -> List[str]:
    """Get all registered instances for a specific file."""
    if file_path in _dsl_definition_registry:
        return _dsl_definition_registry[file_path]["instances"].copy()
    return []


def get_dsl_classes_for_file(file_path: str) -> List[str]:
    """Get all registered classes for a specific file."""
    if file_path in _dsl_definition_registry:
        return _dsl_definition_registry[file_path]["classes"].copy()
    return []


def clear_dsl_registry() -> None:
    """Clear the DSL definition registry (useful for reloading)."""
    global _definitions_loaded
    _dsl_definition_registry.clear()
    _definitions_loaded = False


def scan_registered_dsl_files() -> Dict[str, List[str]]:
    """
    Scan only registered DSL files and extract instance names.
    
    Returns dict mapping file_path -> list of instance names.
    """
    from procedural_human.dsl.executor import get_dsl_instances
    
    result = {}
    for file_path in get_dsl_files():
        if os.path.exists(file_path):
            try:
                instances = get_dsl_instances(file_path)
                result[file_path] = instances
                
                for instance_name in instances:
                    register_dsl_instance(file_path, instance_name)
            except Exception as e:
                print(f"Error scanning DSL file {file_path}: {e}")
                result[file_path] = []
    
    return result

