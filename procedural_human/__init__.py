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
import time as _time_module
import json as _json_module
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["HF_HUB_DISABLE_EXPERIMENTAL_WARNING"] = "1"
import ctypes

# #region agent log - startup timing
_STARTUP_LOG_PATH = r"c:\Code\Blender-Procedural-Human\.cursor\debug.log"
_startup_times = {}
_startup_start = _time_module.perf_counter()

def _log_timing(phase, elapsed_ms):
    try:
        with open(_STARTUP_LOG_PATH, "a") as f:
            f.write(_json_module.dumps({"hypothesisId": "TIMING", "location": "__init__.py", "message": f"Startup phase: {phase}", "data": {"phase": phase, "elapsed_ms": round(elapsed_ms, 2)}, "timestamp": int(_time_module.time()*1000), "sessionId": "startup-timing"}) + "\n")
    except: pass
# #endregion


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
    
    # Skip if torch is already imported - DLLs are already loaded
    if "torch" in sys.modules:
        return

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
        try:
            os.add_dll_directory(str(torch_lib))
        except OSError:
            pass  # Already added or path doesn't exist
    
    # Also add to PATH if not already there
    current_path = os.environ.get("PATH", "")
    if str(torch_lib) not in current_path:
        os.environ["PATH"] = str(torch_lib) + os.pathsep + current_path
    
    # Pre-load critical DLLs in correct order to avoid initialization failures
    # Only do this on first load - DLLs stay loaded in memory
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
                pass  # Some DLLs may fail or already loaded, that's okay

# #region agent log - timing torch dll
_t0 = _time_module.perf_counter()
_setup_torch_dll_path()
_log_timing("setup_torch_dll_path", (_time_module.perf_counter() - _t0) * 1000)
# #endregion

# Install wheels for development mode, with version tracking
def _get_wheels_hash():
    """Get a hash of wheel filenames to detect changes."""
    _t = _time_module.perf_counter()
    import hashlib
    wheels_dir = _addon_dir / "wheels"
    if not wheels_dir.exists():
        _log_timing("_get_wheels_hash:no_dir", (_time_module.perf_counter() - _t) * 1000)
        return ""
    wheel_names = sorted([f.name for f in wheels_dir.glob("*.whl")])
    result = hashlib.md5("|".join(wheel_names).encode()).hexdigest()[:16]
    _log_timing("_get_wheels_hash", (_time_module.perf_counter() - _t) * 1000)
    return result

def _check_packages_installed():
    """Check if required packages are already importable (without importing them)."""
    _t = _time_module.perf_counter()
    import importlib.util
    # Use find_spec to check if packages exist without importing them (much faster)
    torch_spec = importlib.util.find_spec("torch")
    transformers_spec = importlib.util.find_spec("transformers")
    result = torch_spec is not None and transformers_spec is not None
    _log_timing(f"_check_packages_installed:torch={torch_spec is not None},transformers={transformers_spec is not None}", (_time_module.perf_counter() - _t) * 1000)
    return result

def _ensure_wheels_installed():
    """Install wheels from ./wheels/ directory if dependencies are missing or changed."""
    _t_start = _time_module.perf_counter()
    wheels_dir = _addon_dir / "wheels"
    if not wheels_dir.exists():
        print(f"[Procedural Human] Wheels directory not found: {wheels_dir}")
        _log_timing("_ensure_wheels_installed:no_dir", (_time_module.perf_counter() - _t_start) * 1000)
        return
    
    # Check if wheels have changed since last install
    marker_file = Path(sys.prefix) / ".procedural_human_wheels_hash"
    _t = _time_module.perf_counter()
    current_hash = _get_wheels_hash()
    _log_timing("_ensure_wheels_installed:get_hash", (_time_module.perf_counter() - _t) * 1000)
    needs_install = False
    
    # First check: do packages already import successfully?
    _t = _time_module.perf_counter()
    packages_already_installed = _check_packages_installed()
    _log_timing("_ensure_wheels_installed:check_packages", (_time_module.perf_counter() - _t) * 1000)
    
    _t = _time_module.perf_counter()
    if marker_file.exists():
        stored_hash = marker_file.read_text().strip()
        _log_timing(f"_ensure_wheels_installed:read_marker(stored={stored_hash},current={current_hash})", (_time_module.perf_counter() - _t) * 1000)
        if stored_hash != current_hash:
            # Hash changed, but if packages are loaded we can't reinstall safely
            if packages_already_installed:
                print(f"[Procedural Human] Wheels changed but packages are already loaded. Restart Blender to update.")
                # Update the marker anyway to avoid repeated warnings
                try:
                    marker_file.write_text(current_hash)
                except Exception:
                    pass
                _log_timing("_ensure_wheels_installed:skip_reload_loaded", (_time_module.perf_counter() - _t_start) * 1000)
                return
            else:
                print(f"[Procedural Human] Wheels changed (hash: {stored_hash} -> {current_hash}), reinstalling...")
                needs_install = True
    else:
        _log_timing("_ensure_wheels_installed:no_marker_file", (_time_module.perf_counter() - _t) * 1000)
        # No marker file exists
        if packages_already_installed:
            # Packages are already installed, just write the marker and skip
            print("[Procedural Human] Packages already installed, creating marker file...")
            try:
                marker_file.write_text(current_hash)
            except Exception:
                pass
            _log_timing("_ensure_wheels_installed:skip_already_installed", (_time_module.perf_counter() - _t_start) * 1000)
            return
        else:
            # Packages not installed, need to install
            needs_install = True
    
    if not needs_install:
        _log_timing("_ensure_wheels_installed:skip_no_change", (_time_module.perf_counter() - _t_start) * 1000)
        return
    
    wheel_files = list(wheels_dir.glob("*.whl"))
    zip_files = list(wheels_dir.glob("*.zip"))
    all_packages = wheel_files + zip_files
    
    if not all_packages:
        print("[Procedural Human] No wheel/zip files found")
        _log_timing("_ensure_wheels_installed:no_packages", (_time_module.perf_counter() - _t_start) * 1000)
        return
    
    print(f"[Procedural Human] Installing {len(all_packages)} packages for development mode...")
    
    # Install wheels - don't use --force-reinstall to avoid removing locked DLLs
    # Use --ignore-installed instead to install even if already present
    _t = _time_module.perf_counter()
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--no-deps",
            "--ignore-installed",
            "--quiet",
            *[str(pkg) for pkg in all_packages]
        ])
        _log_timing("_ensure_wheels_installed:pip_install", (_time_module.perf_counter() - _t) * 1000)
        print("[Procedural Human] Wheels installed successfully")
        # Save the hash marker
        try:
            marker_file.write_text(current_hash)
        except Exception:
            pass  # Ignore if we can't write marker
        # Setup DLL path for the newly installed torch
        _setup_torch_dll_path()
    except subprocess.CalledProcessError as e:
        _log_timing("_ensure_wheels_installed:pip_failed", (_time_module.perf_counter() - _t) * 1000)
        print(f"[Procedural Human] Failed to install wheels: {e}")
    
    _log_timing("_ensure_wheels_installed:TOTAL", (_time_module.perf_counter() - _t_start) * 1000)
 
# #region agent log - timing wheels
_t0 = _time_module.perf_counter()
_ensure_wheels_installed()
_log_timing("ensure_wheels_installed", (_time_module.perf_counter() - _t0) * 1000)
# #endregion
 
# #region agent log - timing imports
_t0 = _time_module.perf_counter()
import bpy
from procedural_human.dsl.finger_segment_const import SEGMENT_SAMPLE_COUNT
from procedural_human.logger import *

from procedural_human.decorators.curve_preset_decorator import register_preset_class
from procedural_human.decorators.panel_decorator import procedural_panel
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.decorators.workspace_decorator import procedural_workspace
from procedural_human.decorators.gizmo_decorator import procedural_gizmo
from procedural_human.decorators.module_discovery import (
    clear_discovered,
    import_all_modules,
)
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human import menus
from procedural_human import preferences
_log_timing("imports_total", (_time_module.perf_counter() - _t0) * 1000)
# #endregion


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
    # Log a marker for new reload cycle (don't delete log so we can see unregister timing)
    _log_timing("=== NEW RELOAD CYCLE ===", 0)

    # #region agent log - timing register
    _t_reg_start = _time_module.perf_counter()
    
    _t0 = _time_module.perf_counter()
    preferences.register()
    _log_timing("register:preferences", (_time_module.perf_counter() - _t0) * 1000)

    _t0 = _time_module.perf_counter()
    import_all_modules()
    _log_timing("register:import_all_modules", (_time_module.perf_counter() - _t0) * 1000)

    _t0 = _time_module.perf_counter()
    procedural_panel.discover_and_register_all_decorators()
    _log_timing("register:panels", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    procedural_operator.discover_and_register_all_decorators()
    _log_timing("register:operators", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    register_preset_class.discover_and_register_all_decorators()
    _log_timing("register:presets", (_time_module.perf_counter() - _t0) * 1000)
     
    _t0 = _time_module.perf_counter()
    geo_node_group.discover_and_register_all_decorators()
    _log_timing("register:geo_nodes", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    procedural_workspace.discover_and_register_all_decorators()
    _log_timing("register:workspace", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    procedural_gizmo.discover_and_register_all_decorators()
    _log_timing("register:gizmo", (_time_module.perf_counter() - _t0) * 1000)
    # #endregion
    
    # Register gizmo module (draw handlers, tools)
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human import gizmo
        gizmo.register()
        logger.info("[Procedural Human] Registered gizmo module")
    except Exception as e:
        logger.info(f"[Procedural Human] Could not register gizmo module: {e}")
    _log_timing("register:gizmo_module", (_time_module.perf_counter() - _t0) * 1000)

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
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human.segmentation import search_asset_manager
        search_asset_manager.register()
        logger.info("[Procedural Human] Registered search asset manager")
    except Exception as e:
        logger.info(f"[Procedural Human] Could not register search asset manager: {e}")
    _log_timing("register:search_asset_manager", (_time_module.perf_counter() - _t0) * 1000)
    
    # Start the test server for MCP/external tool integration
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human.testing.blender_server import start_server
        start_server(port=9876)
        logger.info("[Procedural Human] Started test server on port 9876")
    except Exception as e:
        logger.info(f"[Procedural Human] Could not start test server: {e}")
    _log_timing("register:test_server", (_time_module.perf_counter() - _t0) * 1000)
    
    _log_timing("register:TOTAL", (_time_module.perf_counter() - _t_reg_start) * 1000)
    _log_timing("startup:TOTAL_FROM_IMPORT", (_time_module.perf_counter() - _startup_start) * 1000)


def unregister():
    _t_unreg_start = _time_module.perf_counter()
    
    # Stop the test server if running (non-blocking)
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human.testing.blender_server import stop_server, is_server_running
        if is_server_running():
            stop_server()
    except Exception:
        pass
    _log_timing("unregister:test_server", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human.utils.curve_serialization import unregister_autosave_handlers
        unregister_autosave_handlers()
    except ImportError:
        pass
    _log_timing("unregister:autosave_handlers", (_time_module.perf_counter() - _t0) * 1000)

    # Unregister segmentation properties
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human.segmentation import unregister_segmentation_properties
        unregister_segmentation_properties()
    except ImportError:
        pass
    _log_timing("unregister:segmentation_props", (_time_module.perf_counter() - _t0) * 1000)

    # Cleanup search asset manager
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human.segmentation import search_asset_manager
        search_asset_manager.unregister()
    except Exception:
        pass
    _log_timing("unregister:search_asset_manager", (_time_module.perf_counter() - _t0) * 1000)

    # Unregister gizmo module first (draw handlers, tools)
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human import gizmo
        gizmo.unregister()
    except Exception:
        pass
    _log_timing("unregister:gizmo_module", (_time_module.perf_counter() - _t0) * 1000)

    _t0 = _time_module.perf_counter()
    menus.unregister()
    _log_timing("unregister:menus", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    procedural_panel.unregister_all_decorators()
    _log_timing("unregister:panels", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    procedural_operator.unregister_all_decorators()
    _log_timing("unregister:operators", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    register_preset_class.unregister_all_decorators()
    _log_timing("unregister:presets", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    geo_node_group.unregister_all_decorators()
    _log_timing("unregister:geo_nodes", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    procedural_workspace.unregister_all_decorators()
    _log_timing("unregister:workspace", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    procedural_gizmo.unregister_all_decorators()
    _log_timing("unregister:gizmo", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    preferences.unregister()
    _log_timing("unregister:preferences", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    clear_discovered()
    _log_timing("unregister:clear_discovered", (_time_module.perf_counter() - _t0) * 1000)
    
    _log_timing("unregister:TOTAL", (_time_module.perf_counter() - _t_unreg_start) * 1000)


if __name__ == "__main__":
    register()
