"""
Gizmo module for Procedural Human.

Contains GizmoGroup implementations for mesh editing tools,
including the Bezier handle gizmo system for lofting curves.
"""

import sys
from pathlib import Path

# Helper to add bundled venv site-packages to path
def _setup_gizmo_path():
    # Go up one level from gizmo/ to procedural_human/
    # Then look for .venv/Lib/site-packages
    # __file__ is procedural_human/gizmo/__init__.py
    current_dir = Path(__file__).parent
    addon_root = current_dir.parent
    venv_site_packages = addon_root / ".venv" / "Lib" / "site-packages"
    
    if venv_site_packages.exists():
        site_path = str(venv_site_packages)
        if site_path not in sys.path:
            sys.path.insert(0, site_path)

_setup_gizmo_path()

from procedural_human.gizmo.mesh_curves_gizmo import (
    register,
    unregister,
)

__all__ = [
    "register",
    "unregister",
] 
