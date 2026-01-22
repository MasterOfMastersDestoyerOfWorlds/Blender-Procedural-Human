"""
Gizmo module for Procedural Human.

Contains GizmoGroup implementations for mesh editing tools,
including the Bezier handle gizmo system for lofting curves.
"""

import sys
from pathlib import Path
def _setup_gizmo_path():
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
