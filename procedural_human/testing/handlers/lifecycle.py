import traceback
from typing import Any, Dict

import bpy

from procedural_human.testing.handlers.common import _log


def handle_exec_python(params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute arbitrary Python code (use with caution)."""
    code = params.get("code", "")
    if not code:
        return {"success": False, "error": "No code provided"}
    
    try:
        local_ns = {"bpy": bpy, "result": None}
        exec(code, {"bpy": bpy}, local_ns)
        
        return {
            "success": True,
            "result": str(local_ns.get("result", None))
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def handle_clean_scene(params: Dict[str, Any]) -> Dict[str, Any]:
    """Reset to a clean scene and remove any default objects."""
    try:
        bpy.ops.wm.read_homefile(use_empty=True)
        removed = 0
        for obj in list(bpy.data.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
            removed += 1
        return {"success": True, "removed_objects": removed}
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }


def handle_open_file(params: Dict[str, Any]) -> Dict[str, Any]:
    """Open a .blend file in the running Blender instance.

    Re-registers the command queue timer after opening because
    ``open_mainfile`` resets Blender state including timers.
    """
    filepath = params.get("filepath", "")
    if not filepath:
        return {"success": False, "error": "No filepath provided"}

    from pathlib import Path
    p = Path(filepath)
    if not p.exists():
        return {"success": False, "error": f"File not found: {filepath}"}

    try:
        resolved = str(p.resolve())
        bpy.ops.wm.open_mainfile(filepath=resolved)
        from procedural_human.testing.blender_server import _process_command_queue
        if not bpy.app.timers.is_registered(_process_command_queue):
            bpy.app.timers.register(_process_command_queue, first_interval=0.1)
            _log("open_file_timer_reregistered")
        return {"success": True, "filepath": resolved}
    except Exception as e:
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}


def handle_reload_addon(params: Dict[str, Any]) -> Dict[str, Any]:
    """Reload addon and optionally clean scene before re-enable."""
    clean_scene = params.get("clean_scene", True)
    module_name = params.get("module_name", "procedural_human")
    def _ensure_timer():
        from procedural_human.testing.blender_server import _process_command_queue
        if not bpy.app.timers.is_registered(_process_command_queue):
            bpy.app.timers.register(_process_command_queue, first_interval=0.1)
            _log("reload_addon_timer_reregistered")

    try:
        clean_result = None
        if clean_scene:
            clean_result = handle_clean_scene({})
            if not clean_result.get("success"):
                return clean_result

        bpy.ops.preferences.addon_disable(module=module_name)
        bpy.ops.preferences.addon_enable(module=module_name)
        _ensure_timer()
        return {
            "success": True,
            "module": module_name,
            "clean_scene": clean_scene,
            "clean_result": clean_result,
        }
    except Exception as e:
        error_text = str(e)
        if "already registered as a subclass" in error_text:
            _log(f"reload_addon_fallback module={module_name} error={error_text}")
            import importlib
            import sys

            reloaded_modules = []
            for name in sorted(list(sys.modules.keys()), key=len, reverse=True):
                if name == module_name or name.startswith(f"{module_name}."):
                    module = sys.modules.get(name)
                    if module is None:
                        continue
                    try:
                        importlib.reload(module)
                        reloaded_modules.append(name)
                    except Exception as reload_error:
                        _log(f"reload_addon_fallback_module_error module={name} error={reload_error}")
            try:
                mod = sys.modules.get(module_name)
                if mod and hasattr(mod, "register"):
                    mod.register()
                    _log("reload_addon_fallback_register_called")
            except Exception as reg_err:
                _log(f"reload_addon_fallback_register_error error={reg_err}")

            _ensure_timer()
            return {
                "success": True,
                "module": module_name,
                "clean_scene": clean_scene,
                "warning": error_text,
                "fallback": "continued_with_existing_registration",
                "reloaded_module_count": len(reloaded_modules),
            }
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }
