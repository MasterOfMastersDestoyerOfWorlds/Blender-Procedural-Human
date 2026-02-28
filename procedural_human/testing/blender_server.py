"""
Blender HTTP Command Server

A lightweight HTTP server that runs inside Blender using bpy.app.timers,
allowing the CLI (``uv run blender-cli``) to send commands to Blender.

The server accepts JSON commands and executes Blender operators or Python code,
returning results as JSON responses.

Usage:
    from procedural_human.testing.blender_server import start_server, stop_server
    start_server(port=9876)
    import requests
    response = requests.post("http://localhost:9876/command", json={
        "action": "run_test",
        "params": {"subdivisions": 2}
    })
    print(response.json())
    stop_server()
"""

import bpy
import json
import threading
import traceback
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, Optional, Callable

from procedural_human.decorators.operator_decorator import procedural_operator
from bpy.types import Operator
from bpy.props import IntProperty, StringProperty
from procedural_human.testing.handlers.geometry import (
    handle_apply_node_group, handle_check_camera_visibility,
    handle_check_corner, handle_check_node_tree, handle_check_watertight,
    handle_get_mesh_metrics, handle_validate_geometry, handle_verify_topology,
)
from procedural_human.testing.handlers.nodes import (
    handle_diff_group, handle_export_group, handle_inspect_group,
    handle_list_groups,
)
from procedural_human.testing.handlers.lifecycle import (
    handle_clean_scene, handle_exec_python, handle_open_file,
    handle_reload_addon,
)
from procedural_human.testing.handlers.capture import (
    handle_capture_viewport, handle_render_viewport,
)
from procedural_human.testing.handlers.testing import (
    handle_apply_export, handle_get_csv_data, handle_get_point_data,
    handle_run_test, handle_setup_basalt_test, handle_setup_test,
)
from procedural_human.testing.handlers.common import _log


_server: Optional[HTTPServer] = None
_server_thread: Optional[threading.Thread] = None
_command_queue: list = []
_result_queue: dict = {}
_result_counter: int = 0
DEFAULT_COMMAND_TIMEOUT_SECONDS = 120


COMMAND_HANDLERS: Dict[str, Callable] = {
    "run_test": handle_run_test,
    "setup_test": handle_setup_test,
    "apply_export": handle_apply_export,
    "verify_topology": handle_verify_topology,
    "get_csv_data": handle_get_csv_data,
    "get_point_data": handle_get_point_data,
    "check_corner": handle_check_corner,
    "exec_python": handle_exec_python,
    "render_viewport": handle_render_viewport,
    "capture_viewport": handle_capture_viewport,
    "get_mesh_metrics": handle_get_mesh_metrics,
    "validate_geometry": handle_validate_geometry,
    "check_watertight": handle_check_watertight,
    "check_camera_visibility": handle_check_camera_visibility,
    "clean_scene": handle_clean_scene,
    "reload_addon": handle_reload_addon,
    "apply_node_group": handle_apply_node_group,
    "check_node_tree": handle_check_node_tree,
    "setup_basalt_test": handle_setup_basalt_test,
    "open_file": handle_open_file,
    "list_groups": handle_list_groups,
    "inspect_group": handle_inspect_group,
    "export_group": handle_export_group,
    "diff_group": handle_diff_group,
    "ping": lambda p: {"success": True, "message": "pong"},
    "list_commands": lambda p: {"success": True, "commands": list(COMMAND_HANDLERS.keys())},
}

class BlenderCommandHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Blender commands."""
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def _send_json_response(self, data: Dict[str, Any], status: int = 200):
        """Send a JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/status":
            self._send_json_response({
                "status": "running",
                "commands": list(COMMAND_HANDLERS.keys())
            })
        elif self.path == "/health":
            self._send_json_response({"healthy": True})
        else:
            self._send_json_response({"error": "Unknown endpoint"}, 404)
    
    def do_POST(self):
        """Handle POST requests (commands)."""
        global _command_queue, _result_counter
        
        if self.path != "/command":
            self._send_json_response({"error": "Unknown endpoint"}, 404)
            return
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError as e:
            self._send_json_response({"error": f"Invalid JSON: {e}"}, 400)
            return
        
        action = data.get("action")
        params = data.get("params", {})
        
        if not action:
            self._send_json_response({"error": "No action specified"}, 400)
            return
        
        if action not in COMMAND_HANDLERS:
            self._send_json_response({
                "error": f"Unknown action: {action}",
                "available": list(COMMAND_HANDLERS.keys())
            }, 400)
            return
        _result_counter += 1
        command_id = _result_counter
        started_at = time.time()
        _log(
            f"enqueue id={command_id} action={action} "
            f"queue_len={len(_command_queue) + 1} params={json.dumps(params, default=str)}"
        )
        _command_queue.append({
            "id": command_id,
            "action": action,
            "params": params,
        })
        timeout = int(params.get("timeout_seconds", DEFAULT_COMMAND_TIMEOUT_SECONDS))
        timeout = max(5, min(timeout, DEFAULT_COMMAND_TIMEOUT_SECONDS))
        start = time.time()
        
        while command_id not in _result_queue:
            if time.time() - start > timeout:
                _log(
                    f"timeout id={command_id} action={action} "
                    f"wait_s={time.time() - started_at:.3f} queue_len={len(_command_queue)}"
                )
                self._send_json_response({
                    "error": "Command timeout",
                    "command_id": command_id,
                    "timeout_seconds": timeout,
                }, 504)
                return
            time.sleep(0.05)
        result = _result_queue.pop(command_id)
        _log(
            f"complete id={command_id} action={action} "
            f"elapsed_s={time.time() - started_at:.3f} success={result.get('success')}"
        )
        self._send_json_response(result)


def _process_command_queue():
    """Process pending commands in the main Blender thread."""
    global _command_queue, _result_queue
    
    while _command_queue:
        cmd = _command_queue.pop(0)
        started_at = time.time()
        _log(
            f"process_start id={cmd['id']} action={cmd['action']} "
            f"remaining_queue={len(_command_queue)}"
        )
        try:
            handler = COMMAND_HANDLERS.get(cmd["action"])
            if handler:
                result = handler(cmd["params"])
            else:
                result = {"error": f"Unknown action: {cmd['action']}"}
        except Exception as e:
            result = {
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        _log(
            f"process_end id={cmd['id']} action={cmd['action']} "
            f"elapsed_s={time.time() - started_at:.3f} success={result.get('success')}"
        )
        _result_queue[cmd["id"]] = result
    return 0.1

def start_server(port: int = 9876, host: str = "localhost") -> bool:
    """
    Start the HTTP command server.
    
    Args:
        port: Port to listen on (default 9876)
        host: Host to bind to (default localhost)
        
    Returns:
        True if server started successfully
    """
    global _server, _server_thread
    
    if _server is not None:
        print(f"[BlenderServer] Server already running on {host}:{port}")
        _log(f"server_already_running host={host} port={port}")
        return False
    
    try:
        _server = HTTPServer((host, port), BlenderCommandHandler)
        _server_thread = threading.Thread(target=_server.serve_forever, daemon=True)
        _server_thread.start()
        if not bpy.app.timers.is_registered(_process_command_queue):
            bpy.app.timers.register(_process_command_queue, first_interval=0.1)
        
        print(f"[BlenderServer] Started on http://{host}:{port}")
        print(f"[BlenderServer] Available commands: {list(COMMAND_HANDLERS.keys())}")
        _log(f"server_started host={host} port={port}")
        return True
        
    except Exception as e:
        print(f"[BlenderServer] Failed to start: {e}")
        _log(f"server_start_failed error={e}")
        _server = None
        _server_thread = None
        return False


def stop_server():
    """Stop the HTTP command server (non-blocking)."""
    global _server, _server_thread

    if _server is None:
        print("[BlenderServer] Server not running")
        _log("server_not_running")
        return
    if bpy.app.timers.is_registered(_process_command_queue):
        bpy.app.timers.unregister(_process_command_queue)
    server_to_stop = _server
    _server = None
    _server_thread = None
    
    def shutdown_async():
        try:
            server_to_stop.shutdown()
        except:
            pass
    
    shutdown_thread = threading.Thread(target=shutdown_async, daemon=True)
    shutdown_thread.start()

    print("[BlenderServer] Stopped")
    _log("server_stopped")


def is_server_running() -> bool:
    """Check if the server is running."""
    return _server is not None


def get_server_url() -> Optional[str]:
    """Get the server URL if running."""
    if _server is None:
        return None
    host, port = _server.server_address
    return f"http://{host}:{port}"


@procedural_operator
class PROC_OT_start_test_server(Operator):
    """Start the HTTP command server for external tool integration"""
    
    bl_idname = "procedural.start_test_server"
    bl_label = "Start Test Server"
    bl_options = {'REGISTER'}
    
    port: IntProperty(
        name="Port",
        description="Port to listen on",
        default=9876,
        min=1024,
        max=65535
    )
    
    host: StringProperty(
        name="Host",
        description="Host to bind to",
        default="localhost"
    )
    
    def execute(self, context):
        if start_server(port=self.port, host=self.host):
            self.report({'INFO'}, f"Server started on {self.host}:{self.port}")
        else:
            self.report({'WARNING'}, "Server already running or failed to start")
        return {'FINISHED'}


@procedural_operator
class PROC_OT_stop_test_server(Operator):
    """Stop the HTTP command server"""
    
    bl_idname = "procedural.stop_test_server"
    bl_label = "Stop Test Server"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        stop_server()
        self.report({'INFO'}, "Server stopped")
        return {'FINISHED'}
