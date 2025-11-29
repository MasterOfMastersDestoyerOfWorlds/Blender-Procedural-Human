"""
DSL definition decorator system for automatic registration.

This decorator registers DSL definition files so they can be discovered
without scanning the entire dsl directory.
"""

from typing import Dict, List, Optional, Type, Any
import os
import inspect
from procedural_human.logger import *

_dsl_definition_registry: Dict[str, Dict[str, Any]] = {}


def dsl_definition(cls: Type) -> Type:
    """
    Decorator for DSL definition classes. Registers the class in the DSL definition registry for discovery.
    The file path is automatically detected from the class module.
    @param cls: The class to register as a DSL definition.
    @return: The class.
    """
    module = inspect.getmodule(cls)
    if module and hasattr(module, "__file__"):
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
    @param file_path: The file path of the DSL definition.
    @param instance_name: The name of the DSL instance to register.
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
    """
    Get all registered DSL definitions.
    @return: A dictionary of all registered DSL definitions.
    """
    return _dsl_definition_registry.copy()


def get_dsl_files() -> List[str]:
    """
    Get list of all registered DSL file paths.
    @return: A list of all registered DSL file paths.
    """
    return list(_dsl_definition_registry.keys())


def get_dsl_instances_for_file(file_path: str) -> List[str]:
    """
    Get all registered instances for a specific file.
    @param file_path: The file path of the DSL definition.
    @return: A list of all registered instances for the specific file.
    """
    if file_path in _dsl_definition_registry:
        return _dsl_definition_registry[file_path]["instances"].copy()
    return []


def get_dsl_classes_for_file(file_path: str) -> List[str]:
    """
    Get all registered classes for a specific file.
    @param file_path: The file path of the DSL definition.
    @return: A list of all registered classes for the specific file.
    """
    if file_path in _dsl_definition_registry:
        return _dsl_definition_registry[file_path]["classes"].copy()
    return []


def clear_dsl_registry() -> None:
    """Clear the DSL definition registry (useful for reloading)."""
    _dsl_definition_registry.clear()


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
                logger.info(f"Error scanning DSL file {file_path}: {e}")
                result[file_path] = []

    return result
