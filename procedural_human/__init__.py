"""
Procedural Human Generator
A Blender add-on for creating procedural human characters using Geometry Nodes
"""

import bpy
import subprocess
import sys
import tomllib
from pathlib import Path
from procedural_human.dsl.finger_segment_const import SEGMENT_SAMPLE_COUNT
from procedural_human.logger import *

from procedural_human.decorators.curve_preset_decorator import register_preset_class
from procedural_human.decorators.panel_decorator import procedural_panel
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.decorators.workspace_decorator import procedural_workspace
from procedural_human.decorators.module_discovery import (
    clear_discovered,
    import_all_modules,
)

# Addon root directory (where this __init__.py lives)
_ADDON_ROOT = Path(__file__).parent.parent

# Mapping from pip package names to import names
# Only needed for packages where the import name differs from the pip name
_PIP_TO_IMPORT = {
    "tree-sitter": "tree_sitter",
    "tree-sitter-python": "tree_sitter_python",
    "opencv-python": "cv2",
    "pillow": "PIL",
    "scikit-image": "skimage",
    "huggingface_hub": "huggingface_hub",
}

# Packages to skip during dependency checking (dev tools, already in Blender, etc.)
_SKIP_PACKAGES = {
    "pytest",
    "black",
    "flake8",
    "mypy",
    "fake-bpy-module",
    "filemover",  # Git dependency, special handling needed
}


def _get_required_packages() -> list[tuple[str, str]]:
    """
    Parse pyproject.toml to get required packages.
    Returns list of (import_name, pip_name) tuples.
    """
    pyproject_path = _ADDON_ROOT / "pyproject.toml"
    
    if not pyproject_path.exists():
        logger.warning(f"pyproject.toml not found at {pyproject_path}")
        return []
    
    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
        
        dependencies = data.get("project", {}).get("dependencies", [])
        packages = []
        
        for dep in dependencies:
            # Parse dependency string (e.g., "opencv-python>=4.8.0" -> "opencv-python")
            # Handle various formats: pkg, pkg>=ver, pkg[extra], pkg @ url
            pip_name = dep.split(">=")[0].split("<=")[0].split("==")[0]
            pip_name = pip_name.split("[")[0].split("@")[0].strip()
            
            # Skip dev/excluded packages
            if any(pip_name.startswith(skip) for skip in _SKIP_PACKAGES):
                continue
            
            # Get import name (use mapping or convert dashes to underscores)
            import_name = _PIP_TO_IMPORT.get(pip_name, pip_name.replace("-", "_"))
            
            packages.append((import_name, pip_name))
        
        return packages
        
    except Exception as e:
        logger.error(f"Failed to parse pyproject.toml: {e}")
        return []


def check_dependencies() -> list[tuple[str, str]]:
    """
    Check which required packages are missing.
    Returns list of (import_name, pip_name) tuples for missing packages.
    """
    required_packages = _get_required_packages()
    missing = []
    for import_name, pip_name in required_packages:
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
    procedural_workspace.discover_and_register_all_decorators()

    logger.info(f"Node group registry: {geo_node_group.registry}")
    
    def create_registered_node_groups():
        logger.info("Initializing registered node groups...")
        for func in geo_node_group.registry.values():
            try:
                func()
            except Exception as e:
                logger.info(f"Error creating node group {func.__name__}: {e}")
        logger.info("Node group initialization complete.")
        return None

    bpy.app.timers.register(create_registered_node_groups, first_interval=0.1)

    menus.register()

    try:
        from procedural_human.utils.curve_serialization import (
            register_autosave_handlers,
        )

        register_autosave_handlers()
    except ImportError as e:
        logger.info(f"[Procedural Human] Could not register curve autosave: {e}")

    # Register segmentation properties (search input, thumbnails, etc.)
    try:
        from procedural_human.segmentation import register_segmentation_properties
        register_segmentation_properties()
    except ImportError as e:
        logger.info(f"[Procedural Human] Could not register segmentation properties: {e}")


def unregister():
    try:
        from procedural_human.utils.curve_serialization import unregister_autosave_handlers
        unregister_autosave_handlers()
    except ImportError:
        pass

    # Unregister segmentation properties
    try:
        from procedural_human.segmentation import unregister_segmentation_properties
        unregister_segmentation_properties()
    except ImportError:
        pass

    menus.unregister()
    procedural_panel.unregister_all_decorators()
    procedural_operator.unregister_all_decorators()
    register_preset_class.unregister_all_decorators()
    geo_node_group.unregister_all_decorators()
    procedural_workspace.unregister_all_decorators()
    preferences.unregister()
    clear_discovered()


if __name__ == "__main__":
    register()
