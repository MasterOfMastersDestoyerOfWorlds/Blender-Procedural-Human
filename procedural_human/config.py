"""
Configuration for codebase paths

Detects the development codebase path to enable exporting modifications
back to source files rather than the installed addon copy.
"""

import os
from pathlib import Path
from typing import Optional


_cached_codebase_path: Optional[Path] = None


def detect_codebase_path() -> Optional[Path]:
    """
    Attempt to detect the actual codebase path.
    
    Strategies (in order):
    1. Walk up from current module looking for project markers (.git, pyproject.toml, uv.lock)
    2. Check for environment variable PROCEDURAL_HUMAN_CODEBASE
    3. Check addon preferences for saved path
    4. Fall back to addon installation directory (with warning)
    
    This defaults to where the codebase actually is by starting from __file__
    and walking up until we find the project root indicators.
    
    Returns:
        Path to the codebase root, or None if not found
    """
    
    current_file = Path(__file__).resolve()
    current_dir = current_file.parent
    
    
    markers = ['.git', 'pyproject.toml', 'uv.lock', 'TODO.md']
    
    
    check_dir = current_dir
    while check_dir.parent != check_dir:  
        
        for marker in markers:
            marker_path = check_dir / marker
            if marker_path.exists():
                
                return check_dir
        
        
        check_dir = check_dir.parent
    
    
    env_path = os.environ.get('PROCEDURAL_HUMAN_CODEBASE')
    if env_path:
        env_path_obj = Path(env_path)
        if env_path_obj.exists() and env_path_obj.is_dir():
            return env_path_obj
    
    
    try:
        import bpy
        if hasattr(bpy.context, 'preferences'):
            addon_prefs = bpy.context.preferences.addons.get('procedural_human')
            if addon_prefs and hasattr(addon_prefs, 'preferences'):
                prefs = addon_prefs.preferences
                if hasattr(prefs, 'codebase_path') and prefs.codebase_path:
                    prefs_path = Path(prefs.codebase_path)
                    if prefs_path.exists() and prefs_path.is_dir():
                        return prefs_path
    except (ImportError, AttributeError):
        pass
    
    
    
    addon_dir = current_file.parent
    while addon_dir.name != 'procedural_human' and addon_dir.parent != addon_dir:
        addon_dir = addon_dir.parent
    
    if addon_dir.name == 'procedural_human':
        return addon_dir.parent
    
    return None


def get_codebase_path() -> Optional[Path]:
    """
    Get the codebase path, with caching.
    
    Returns:
        Cached codebase path, or freshly detected path
    """
    global _cached_codebase_path
    
    if _cached_codebase_path is None:
        _cached_codebase_path = detect_codebase_path()
    
    return _cached_codebase_path


def set_codebase_path(path: Path) -> None:
    """
    Set the codebase path explicitly and cache it.
    
    Args:
        path: Path to the codebase root directory
    """
    global _cached_codebase_path
    _cached_codebase_path = Path(path) if path else None


def clear_cache() -> None:
    """Clear the cached codebase path, forcing re-detection on next call."""
    global _cached_codebase_path
    _cached_codebase_path = None


def validate_codebase_path(path: Path) -> bool:
    """
    Validate that a path is a valid codebase directory.
    
    Args:
        path: Path to validate
        
    Returns:
        True if path exists and contains expected structure
    """
    if not path or not path.exists() or not path.is_dir():
        return False
    
    
    expected_subdir = path / 'procedural_human'
    if not expected_subdir.exists():
        return False
    
    
    markers = ['.git', 'pyproject.toml', 'uv.lock', 'TODO.md']
    return any((path / marker).exists() for marker in markers)

