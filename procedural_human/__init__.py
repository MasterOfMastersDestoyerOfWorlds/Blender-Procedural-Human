"""
Procedural Human Generator
A Blender add-on for creating procedural human characters using Geometry Nodes

Dependencies are bundled as Python wheels in the ./wheels/ directory.
Blender automatically extracts and installs them when the extension is loaded.
For development mode (VS Code), wheels are installed on first run.
"""

import sys
import subprocess
import atexit
from pathlib import Path
import os
import time as _time_module
import json as _json_module

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["HF_HUB_DISABLE_EXPERIMENTAL_WARNING"] = "1"
import ctypes
_STARTUP_LOG_PATH = r"c:\Code\Blender-Procedural-Human\.cursor\debug.log"
_startup_times = {}
_startup_start = _time_module.perf_counter()

def _log_timing(phase, elapsed_ms):
    try:
        with open(_STARTUP_LOG_PATH, "a") as f:
            f.write(_json_module.dumps({"hypothesisId": "TIMING", "location": "__init__.py", "message": f"Startup phase: {phase}", "data": {"phase": phase, "elapsed_ms": round(elapsed_ms, 2)}, "timestamp": int(_time_module.time()*1000), "sessionId": "startup-timing"}) + "\n")
    except: pass


def _setup_python_path():
    """Add site-packages from the bundled venv to sys.path if not present."""
    import sys
    from pathlib import Path
    addon_dir = Path(__file__).parent
    venv_site_packages = addon_dir / ".venv" / "Lib" / "site-packages"
    
    if venv_site_packages.exists():
        site_packages_str = str(venv_site_packages)
        if site_packages_str not in sys.path:
            sys.path.insert(0, site_packages_str)
_setup_python_path()
_addon_dir = Path(__file__).parent
_addon_parent = _addon_dir.parent
if str(_addon_parent) not in sys.path:
    sys.path.insert(0, str(_addon_parent))
def _setup_torch_dll_path():
    """Add PyTorch DLL directory to search path before importing."""
    if "torch" in sys.modules:
        return

    if sys.platform != "win32":
        return
    torch_lib = None
    for path in sys.path:
        candidate = Path(path) / "torch" / "lib"
        if candidate.exists():
            torch_lib = candidate
            break
    
    if not torch_lib:
        return
    if hasattr(os, 'add_dll_directory'):
        try:
            os.add_dll_directory(str(torch_lib))
        except OSError:
            pass  # Already added or path doesn't exist
    current_path = os.environ.get("PATH", "")
    if str(torch_lib) not in current_path:
        os.environ["PATH"] = str(torch_lib) + os.pathsep + current_path
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
_t0 = _time_module.perf_counter()
_setup_torch_dll_path()
_log_timing("setup_torch_dll_path", (_time_module.perf_counter() - _t0) * 1000)
def _get_wheels_hash():
    """Get a hash of wheel filenames to detect changes."""
    _t = _time_module.perf_counter()
    import hashlib
    wheels_dir = _addon_dir / "wheels"
    if not wheels_dir.exists():
        _log_timing("_get_wheels_hash:no_dir", (_time_module.perf_counter() - _t) * 1000)
        return ""
    package_files = sorted([
        f.name for f in wheels_dir.iterdir() 
        if f.suffix in ('.whl', '.zip') or f.name.endswith('.tar.gz')
    ])
    result = hashlib.md5("|".join(package_files).encode()).hexdigest()[:16]
    _log_timing("_get_wheels_hash", (_time_module.perf_counter() - _t) * 1000)
    return result

def _check_packages_installed():
    """Check if required packages are already importable (without importing them)."""
    _t = _time_module.perf_counter()
    import importlib.util
    torch_spec = importlib.util.find_spec("torch")
    transformers_spec = importlib.util.find_spec("transformers")
    depth_anything_spec = importlib.util.find_spec("depth_anything_3")
    result = torch_spec is not None and transformers_spec is not None and depth_anything_spec is not None
    _log_timing(f"_check_packages_installed:torch={torch_spec is not None},transformers={transformers_spec is not None},depth_anything_3={depth_anything_spec is not None}", (_time_module.perf_counter() - _t) * 1000)
    return result

def _ensure_wheels_installed():
    """Install wheels from ./wheels/ directory if dependencies are missing or changed."""
    _t_start = _time_module.perf_counter()
    wheels_dir = _addon_dir / "wheels"
    if not wheels_dir.exists():
        print(f"[Procedural Human] Wheels directory not found: {wheels_dir}")
        _log_timing("_ensure_wheels_installed:no_dir", (_time_module.perf_counter() - _t_start) * 1000)
        return
    marker_file = Path(sys.prefix) / ".procedural_human_wheels_hash"
    _t = _time_module.perf_counter()
    current_hash = _get_wheels_hash()
    _log_timing("_ensure_wheels_installed:get_hash", (_time_module.perf_counter() - _t) * 1000)
    needs_install = False
    _t = _time_module.perf_counter()
    packages_already_installed = _check_packages_installed()
    _log_timing("_ensure_wheels_installed:check_packages", (_time_module.perf_counter() - _t) * 1000)
    
    _t = _time_module.perf_counter()
    if marker_file.exists():
        stored_hash = marker_file.read_text().strip()
        _log_timing(f"_ensure_wheels_installed:read_marker(stored={stored_hash},current={current_hash})", (_time_module.perf_counter() - _t) * 1000)
        if stored_hash != current_hash:
            if packages_already_installed:
                print(f"[Procedural Human] Wheels changed but packages are already loaded. Restart Blender to update.")
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
        if packages_already_installed:
            print("[Procedural Human] Packages already installed, creating marker file...")
            try:
                marker_file.write_text(current_hash)
            except Exception:
                pass
            _log_timing("_ensure_wheels_installed:skip_already_installed", (_time_module.perf_counter() - _t_start) * 1000)
            return
        else:
            needs_install = True
    
    if not needs_install:
        _log_timing("_ensure_wheels_installed:skip_no_change", (_time_module.perf_counter() - _t_start) * 1000)
        return
    
    wheel_files = list(wheels_dir.glob("*.whl"))
    zip_files = list(wheels_dir.glob("*.zip"))
    tar_files = list(wheels_dir.glob("*.tar.gz"))
    all_packages = wheel_files + zip_files + tar_files
    
    if not all_packages:
        print("[Procedural Human] No wheel/zip files found")
        _log_timing("_ensure_wheels_installed:no_packages", (_time_module.perf_counter() - _t_start) * 1000)
        return
    
    print(f"[Procedural Human] Installing {len(all_packages)} packages for development mode...")
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
        try:
            marker_file.write_text(current_hash)
        except Exception:
            pass  # Ignore if we can't write marker
        _setup_torch_dll_path()
    except subprocess.CalledProcessError as e:
        _log_timing("_ensure_wheels_installed:pip_failed", (_time_module.perf_counter() - _t) * 1000)
        print(f"[Procedural Human] Failed to install wheels: {e}")
    
    _log_timing("_ensure_wheels_installed:TOTAL", (_time_module.perf_counter() - _t_start) * 1000)
_t0 = _time_module.perf_counter()
_ensure_wheels_installed()
_log_timing("ensure_wheels_installed", (_time_module.perf_counter() - _t0) * 1000)
_t0 = _time_module.perf_counter()
import bpy
from procedural_human.dsl.finger_segment_const import SEGMENT_SAMPLE_COUNT
from procedural_human.logger import *
try:
    import procedural_human.logger as _ph_logger_module
    if hasattr(_ph_logger_module, "configure_logging"):
        _ph_logger_module.configure_logging()
except Exception:
    pass

from procedural_human.decorators.curve_preset_decorator import register_preset_class
from procedural_human.decorators.panel_decorator import procedural_panel
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.decorators.workspace_decorator import procedural_workspace
from procedural_human.decorators.gizmo_decorator import procedural_gizmo_group
from procedural_human.decorators.module_discovery import (
    clear_discovered,
    import_all_modules,
)
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.decorators.shader_node_decorator import shader_node_group
from procedural_human.decorators.node_helper_decorator import node_helper
from procedural_human import menus
from procedural_human import preferences
_log_timing("imports_total", (_time_module.perf_counter() - _t0) * 1000)


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
    _log_timing("=== NEW RELOAD CYCLE ===", 0)
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
    shader_node_group.discover_and_register_all_decorators()
    _log_timing("register:shader_nodes", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    procedural_workspace.discover_and_register_all_decorators()
    _log_timing("register:workspace", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    procedural_gizmo_group.discover_and_register_all_decorators()
    _log_timing("register:gizmo", (_time_module.perf_counter() - _t0) * 1000)
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human import gizmo
        gizmo.register()
        logger.info("[Procedural Human] Registered gizmo module")
    except Exception as e:
        logger.info(f"[Procedural Human] Could not register gizmo module: {e}")
    _log_timing("register:gizmo_module", (_time_module.perf_counter() - _t0) * 1000)

    logger.info(f"Node group registry: {geo_node_group.registry}")
    logger.info(f"Shader group registry: {shader_node_group.registry}")
    logger.info(f"Node helper registry: {list(node_helper.registry.keys())}")
    
    def validate_node_group(group, func_name):
        if group is None:
            return
        skip_types = {"GeometryNodeViewer"}
        for link in group.links:
            if not link.is_valid:
                if link.to_node and link.to_node.bl_idname in skip_types:
                    continue
                from_label = f"{link.from_node.name}.{link.from_socket.name}" if link.from_node else "?"
                to_label = f"{link.to_node.name}.{link.to_socket.name}" if link.to_node else "?"
                logger.warning(f"[Node Validation] {group.name}: invalid link {from_label} -> {to_label}")
        for node in group.nodes:
            if node.bl_idname in skip_types:
                continue
            for i, sock in enumerate(node.inputs):
                if sock.bl_idname == "NodeSocketVirtual" and any(l.to_socket == sock for l in group.links):
                    logger.warning(f"[Node Validation] {group.name}: virtual input socket {node.name}.inputs[{i}] has link (missing capture/repeat/index item?)")
            for i, sock in enumerate(node.outputs):
                if sock.bl_idname == "NodeSocketVirtual" and any(l.from_socket == sock for l in group.links):
                    logger.warning(f"[Node Validation] {group.name}: virtual output socket {node.name}.outputs[{i}] has link (missing capture/repeat/index item?)")

    def create_registered_node_groups():
        logger.info("Initializing registered node groups...")
        for func in geo_node_group.registry.values():
            try:
                group = func()
                validate_node_group(group, func.__name__)
            except Exception as e:
                logger.exception(f"Error creating node group {func.__name__}: {e}")
        logger.info("Node group initialization complete.")
        return None

    def create_registered_shader_groups():
        logger.info("Initializing registered shader groups...")
        for func in shader_node_group.registry.values():
            try:
                func()
            except Exception as e:
                logger.exception(f"Error creating shader group {func.__name__}: {e}")
        logger.info("Shader group initialization complete.")
        return None

    bpy.app.timers.register(create_registered_node_groups, first_interval=0.1) 
    bpy.app.timers.register(create_registered_shader_groups, first_interval=0.2)

    menus.register()

    _t0 = _time_module.perf_counter()
    try:
        from procedural_human.utils import node_export_ui
        node_export_ui.register()
    except Exception as e:
        logger.info(f"[Procedural Human] Could not register node export UI: {e}")
    _log_timing("register:node_export_ui", (_time_module.perf_counter() - _t0) * 1000)

    try:
        from procedural_human.utils.curve_serialization import (
            register_autosave_handlers,
        )

        register_autosave_handlers()
    except ImportError as e:
        logger.info(f"[Procedural Human] Could not register curve autosave: {e}")
    try:
        from procedural_human.segmentation import register_segmentation_properties
        register_segmentation_properties()
    except ImportError as e:
        logger.info(f"[Procedural Human] Could not register segmentation properties: {e}")
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human.image_search import search_asset_manager
        search_asset_manager.register()
        logger.info("[Procedural Human] Registered search asset manager")
    except Exception as e:
        logger.info(f"[Procedural Human] Could not register search asset manager: {e}")
    _log_timing("register:search_asset_manager", (_time_module.perf_counter() - _t0) * 1000)
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
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human.segmentation import unregister_segmentation_properties
        unregister_segmentation_properties()
    except ImportError:
        pass
    _log_timing("unregister:segmentation_props", (_time_module.perf_counter() - _t0) * 1000)
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human.image_search import search_asset_manager
        search_asset_manager.unregister()
    except Exception:
        pass
    _log_timing("unregister:search_asset_manager", (_time_module.perf_counter() - _t0) * 1000)
    _t0 = _time_module.perf_counter()
    try:
        from procedural_human import gizmo
        gizmo.unregister()
    except Exception:
        pass
    _log_timing("unregister:gizmo_module", (_time_module.perf_counter() - _t0) * 1000)

    _t0 = _time_module.perf_counter()
    try:
        from procedural_human.utils import node_export_ui
        node_export_ui.unregister()
    except Exception:
        pass
    _log_timing("unregister:node_export_ui", (_time_module.perf_counter() - _t0) * 1000)

    _t0 = _time_module.perf_counter()
    node_helper.registry.clear()
    _log_timing("unregister:node_helpers", (_time_module.perf_counter() - _t0) * 1000)

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
    shader_node_group.unregister_all_decorators()
    _log_timing("unregister:shader_nodes", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    procedural_workspace.unregister_all_decorators()
    _log_timing("unregister:workspace", (_time_module.perf_counter() - _t0) * 1000)
    
    _t0 = _time_module.perf_counter()
    procedural_gizmo_group.unregister_all_decorators()
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
