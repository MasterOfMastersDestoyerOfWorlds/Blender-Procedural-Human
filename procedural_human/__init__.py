"""
Procedural Human Generator
A Blender add-on for creating procedural human characters using Geometry Nodes

Dependencies are bundled as Python wheels in the ./wheels/ directory.
Blender automatically extracts and installs them when the extension is loaded.
For development mode (VS Code), wheels are installed on first run.
"""

import sys
import subprocess
from pathlib import Path
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"    
import os
import ctypes

# Add addon parent directory to sys.path for absolute imports
# This ensures "from procedural_human.xxx import yyy" works regardless of
# how Blender loads the addon (legacy addon vs extension system)
_addon_dir = Path(__file__).parent
_addon_parent = _addon_dir.parent
if str(_addon_parent) not in sys.path:
    sys.path.insert(0, str(_addon_parent))

# Fix DLL loading for PyTorch on Windows in Blender's embedded Python
def _setup_torch_dll_path():
    """Add PyTorch DLL directory to search path before importing."""

    if sys.platform != "win32":
        return
    
    # Find torch installation in site-packages
    torch_lib = None
    for path in sys.path:
        candidate = Path(path) / "torch" / "lib"
        if candidate.exists():
            torch_lib = candidate
            break
    
    if not torch_lib:
        return
    
    # Add to DLL search path (Windows 10+)
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(str(torch_lib))
    
    # Also add to PATH
    os.environ["PATH"] = str(torch_lib) + os.pathsep + os.environ.get("PATH", "")
    
    # Pre-load critical DLLs in correct order to avoid initialization failures
    dll_load_order = [
        "fbgemm.dll",
        "asmjit.dll", 
        "uv.dll",
        "libiomp5md.dll",
        "libiompstubs5md.dll",
        "c10.dll",
        "torch_cpu.dll",
    ]
    
    for dll_name in dll_load_order:
        dll_path = torch_lib / dll_name
        if dll_path.exists():
            try:
                ctypes.CDLL(str(dll_path))
            except OSError:
                pass  # Some DLLs may fail, that's okay

_setup_torch_dll_path()

# Install wheels for development mode if torch is not available
def _ensure_wheels_installed():
    """Install wheels from ./wheels/ directory if dependencies are missing."""
    try:
        import torch
        return  # Already installed and working
    except ImportError:
        needs_install = True
    except OSError as e:
        # DLL loading error - torch is installed but broken, skip reinstall
        print(f"[Procedural Human] PyTorch DLL error: {e}")
        print("[Procedural Human] Try installing Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe")
        return
    
    if not needs_install:
        return
    
    wheels_dir = _addon_dir / "wheels"
    if not wheels_dir.exists():
        print(f"[Procedural Human] Wheels directory not found: {wheels_dir}")
        return
    
    wheel_files = list(wheels_dir.glob("*.whl"))
    if not wheel_files:
        print("[Procedural Human] No wheel files found")
        return
    
    print(f"[Procedural Human] Installing {len(wheel_files)} wheels for development mode...")
    
    # Install all wheels using pip
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--no-deps",  # Dependencies are already in wheels
            "--quiet",
            *[str(whl) for whl in wheel_files]
        ])
        print("[Procedural Human] Wheels installed successfully")
        # Setup DLL path for the newly installed torch
        _setup_torch_dll_path()
    except subprocess.CalledProcessError as e:
        print(f"[Procedural Human] Failed to install wheels: {e}")

_ensure_wheels_installed()
 
import bpy
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

    # Register the search asset manager (for Yandex search results in Asset Browser)
    try:
        from procedural_human.segmentation import search_asset_manager
        search_asset_manager.register()
        logger.info("[Procedural Human] Registered search asset manager")
    except Exception as e:
        logger.info(f"[Procedural Human] Could not register search asset manager: {e}")


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

    # Cleanup search asset manager
    try:
        from procedural_human.segmentation import search_asset_manager
        search_asset_manager.unregister()
    except Exception:
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
