"""
Preset location tracker using tree-sitter to find preset classes in the codebase.
"""

import os
import inspect
from typing import Dict, Optional, List
from procedural_human.utils.tree_sitter_utils import find_class_with_decorator


def get_caller_file_path() -> Optional[str]:
    """
    Get the file path of the caller (where the decorator is being applied).
    
    Returns:
        Absolute file path or None if not found
    """
    frame = inspect.currentframe()
    try:
        # Go up the stack to find the caller
        caller_frame = frame.f_back
        if caller_frame:
            caller_frame = caller_frame.f_back
            if caller_frame:
                file_path = caller_frame.f_code.co_filename
                if file_path and os.path.exists(file_path):
                    return os.path.abspath(file_path)
    finally:
        del frame
    
    return None


def locate_preset_in_file(file_path: str, preset_name: str) -> Optional[Dict]:
    """
    Locate a preset class in a file using tree-sitter.
    
    Args:
        file_path: Path to the Python file
        preset_name: Name of the preset (from decorator argument)
        
    Returns:
        Dictionary with location information or None if not found
    """
    if not os.path.exists(file_path):
        return None
    
    class_info = find_class_with_decorator(file_path, "register_preset_class", preset_name)
    
    if class_info:
        class_info["file_path"] = file_path
        return class_info
    
    return None


def scan_directory_for_presets(directory: str) -> List[Dict]:
    """
    Scan a directory for all preset classes.
    
    Args:
        directory: Directory to scan
        
    Returns:
        List of preset location dictionaries
    """
    presets = []
    
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common ignore patterns
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("__pycache__", "node_modules")]
        
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    # Try to find any preset classes in this file
                    # We'll need to parse and check for decorators
                    # For now, we'll rely on the registry to provide preset names
                    pass
                except Exception as e:
                    print(f"Error scanning {file_path}: {e}")
    
    return presets


