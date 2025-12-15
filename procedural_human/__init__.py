"""
Procedural Human Generator
A Blender add-on for creating procedural human characters using Geometry Nodes
"""

import bpy
import subprocess
import sys
from pathlib import Path
from procedural_human.dsl.finger_segment_const import SEGMENT_SAMPLE_COUNT
from procedural_human.logger import *

from procedural_human.decorators.curve_preset_decorator import register_preset_class
from procedural_human.decorators.panel_decorator import procedural_panel
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.decorators.module_discovery import (
    clear_discovered,
    import_all_modules,
)

REQUIRED_PACKAGES = [
    ("tree_sitter", "tree-sitter"),
    ("tree_sitter_python", "tree-sitter-python"),
]


def check_dependencies() -> list[tuple[str, str]]:
    """
    Check which required packages are missing.
    Returns list of (import_name, pip_name) tuples for missing packages.
    """
    missing = []
    for import_name, pip_name in REQUIRED_PACKAGES:
        try:
            __import__(import_name)
        except ImportError:
            missing.append((import_name, pip_name))
    return missing


def get_blender_python_executable() -> str:
    """Get the path to Blender's Python executable."""
    return sys.executable


def ensure_pip() -> bool:
    """Ensure pip is available in Blender's Python."""
    python_exe = get_blender_python_executable()
    try:
        result = subprocess.run(
            [python_exe, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return True

        logger.info("[Procedural Human] pip not found, running ensurepip...")
        result = subprocess.run(
            [python_exe, "-m", "ensurepip", "--upgrade"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return result.returncode == 0
    except Exception as e:
        logger.info(f"[Procedural Human] Error ensuring pip: {e}")
        return False


def install_package(pip_name: str) -> tuple[bool, str]:
    """
    Install a package into Blender's Python.
    Returns (success, message).
    """
    python_exe = get_blender_python_executable()
    try:
        result = subprocess.run(
            [python_exe, "-m", "pip", "install", pip_name],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            return True, f"Successfully installed {pip_name}"
        else:
            return False, f"Failed to install {pip_name}: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, f"Installation timed out for {pip_name}"
    except Exception as e:
        return False, f"Error installing {pip_name}: {e}"


_DEPENDENCIES_CHECKED = False
_DEPENDENCIES_INSTALLED = False
_MISSING_DEPENDENCIES: list[tuple[str, str]] = []


def ensure_dependencies() -> bool:
    """
    Check for missing dependencies and install them automatically.
    Called at registration.
    """
    global _DEPENDENCIES_CHECKED, _DEPENDENCIES_INSTALLED, _MISSING_DEPENDENCIES

    if _DEPENDENCIES_INSTALLED:
        return True

    missing = check_dependencies()

    if not missing:
        _DEPENDENCIES_CHECKED = True
        _DEPENDENCIES_INSTALLED = True
        _MISSING_DEPENDENCIES = []
        return True

    logger.info(f"\n{'='*60}")
    logger.info("PROCEDURAL HUMAN: Installing required dependencies...")
    logger.info(f"{'='*60}")

    if not ensure_pip():
        logger.info("ERROR: Could not ensure pip is available.")
        logger.info("Please install pip manually or run Blender as administrator.")
        logger.info(f"{'='*60}\n")
        _DEPENDENCIES_CHECKED = True
        _MISSING_DEPENDENCIES = missing
        return False

    all_installed = True
    for import_name, pip_name in missing:
        logger.info(f"  Installing {pip_name}...")
        success, message = install_package(pip_name)
        if success:
            logger.info(f"    ✓ {message}")
        else:
            logger.info(f"    ✗ {message}")
            all_installed = False

    final_missing = check_dependencies()

    if not final_missing:
        logger.info(f"\n✓ All dependencies installed successfully!")
        logger.info(f"{'='*60}\n")
        _DEPENDENCIES_CHECKED = True
        _DEPENDENCIES_INSTALLED = True
        _MISSING_DEPENDENCIES = []
        return True
    else:
        logger.info(f"\n✗ Some dependencies could not be installed:")
        for import_name, pip_name in final_missing:
            logger.info(f"    - {pip_name}")
        logger.info(f"\nTry running Blender as administrator, or install manually:")
        logger.info(
            f"  {get_blender_python_executable()} -m pip install {' '.join(pip for _, pip in final_missing)}"
        )
        logger.info(f"{'='*60}\n")
        _DEPENDENCIES_CHECKED = True
        _MISSING_DEPENDENCIES = final_missing
        return False


from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human import menus
from procedural_human import preferences


def update_profile_curves(self, context):
    """
    Update callback for profile curve changes.
    Finds all finger objects and updates their geometry node trees.
    """

    for obj in bpy.data.objects:
        if obj.type == "MESH" and hasattr(obj, "finger_data"):
            if obj.finger_data.is_finger:

                for modifier in obj.modifiers:
                    if modifier.type == "NODES" and modifier.node_group:

                        pass

    if context.view_layer:
        context.view_layer.update()


bl_info = {
    "name": "Procedural Human Generator",
    "author": "Procedural Human Team",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Add > Mesh",
    "description": "Generates complete procedural humans using Geometry Nodes",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}


def register():
    preferences.register()

    deps_ok = ensure_dependencies()
    if not deps_ok:
        logger.info(
            "Procedural Human: Some features disabled due to missing dependencies."
        )
        logger.info(
            "Install dependencies via addon preferences to enable all features."
        )

    import_all_modules()

    procedural_panel.discover_and_register_all_decorators()
    procedural_operator.discover_and_register_all_decorators()
    register_preset_class.discover_and_register_all_decorators()
    geo_node_group.discover_and_register_all_decorators()

    logger.info(f"Node group registry: {geo_node_group.registry}")
    # Ensure all registered node groups exist
    for func in geo_node_group.registry.values():
        try:
            logger.info(f"Creating node group {func.__name__}")
            func()
        except Exception as e:
            logger.info(f"Error creating node group {func.__name__}: {e}")

    menus.register()

    try:
        from procedural_human.utils.curve_serialization import (
            register_autosave_handlers,
        )

        register_autosave_handlers()
    except ImportError as e:
        logger.info(f"[Procedural Human] Could not register curve autosave: {e}")


def unregister():
    try:
        from procedural_human.utils.curve_serialization import unregister_autosave_handlers
        unregister_autosave_handlers()
    except ImportError:
        pass

    menus.unregister()
    procedural_panel.unregister_all_decorators()
    procedural_operator.unregister_all_decorators()
    register_preset_class.unregister_all_decorators()
    geo_node_group.unregister_all_decorators()
    preferences.unregister()
    clear_discovered()


if __name__ == "__main__":
    register()
