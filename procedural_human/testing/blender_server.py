"""
Blender HTTP Command Server

A lightweight HTTP server that runs inside Blender using bpy.app.timers,
allowing external tools (like an MCP server) to send commands to Blender.

The server accepts JSON commands and executes Blender operators or Python code,
returning results as JSON responses.

Usage:
    # Start server (in Blender Python console or script)
    from procedural_human.testing.blender_server import start_server, stop_server
    start_server(port=9876)
    
    # Send commands from external process
    import requests
    response = requests.post("http://localhost:9876/command", json={
        "action": "run_test",
        "params": {"subdivisions": 2}
    })
    print(response.json())
    
    # Stop server
    stop_server()
"""

import bpy
import json
import threading
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, Optional, Callable
from functools import partial

# Server state
_server: Optional[HTTPServer] = None
_server_thread: Optional[threading.Thread] = None
_command_queue: list = []
_result_queue: dict = {}
_result_counter: int = 0


# ============================================================================
# COMMAND HANDLERS
# ============================================================================

def handle_run_test(params: Dict[str, Any]) -> Dict[str, Any]:
    """Run the full Coon patch test."""
    subdivisions = params.get("subdivisions", 2)
    create_new = params.get("create_new_cube", True)
    
    try:
        result = bpy.ops.procedural.run_full_coon_test(
            subdivisions=subdivisions,
            create_new_cube=create_new
        )
        
        # Get test results from scene
        passed = bpy.context.scene.get("coon_test_passed", 0)
        failed = bpy.context.scene.get("coon_test_failed", 0)
        total = bpy.context.scene.get("coon_test_total", 0)
        
        return {
            "success": failed == 0,
            "operator_result": str(result),
            "passed": passed,
            "failed": failed,
            "total": total,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def handle_setup_test(params: Dict[str, Any]) -> Dict[str, Any]:
    """Setup a test scene."""
    subdivisions = params.get("subdivisions", 2)
    use_existing = params.get("use_existing_cube", True)
    
    try:
        result = bpy.ops.procedural.setup_coon_test(
            subdivisions=subdivisions,
            use_existing_cube=use_existing
        )
        return {
            "success": result == {'FINISHED'},
            "operator_result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def handle_apply_export(params: Dict[str, Any]) -> Dict[str, Any]:
    """Apply modifier and export CSVs."""
    apply_mod = params.get("apply_modifier", True)
    export_pts = params.get("export_points", True)
    export_edg = params.get("export_edges", True)
    
    try:
        result = bpy.ops.procedural.apply_and_export(
            apply_modifier=apply_mod,
            export_points=export_pts,
            export_edges=export_edg
        )
        return {
            "success": result == {'FINISHED'},
            "operator_result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def handle_verify_topology(params: Dict[str, Any]) -> Dict[str, Any]:
    """Verify mesh topology."""
    point_csv = params.get("point_csv", "")
    edge_csv = params.get("edge_csv", "")
    
    try:
        result = bpy.ops.procedural.verify_topology(
            point_csv=point_csv,
            edge_csv=edge_csv
        )
        
        passed = bpy.context.scene.get("coon_test_passed", 0)
        failed = bpy.context.scene.get("coon_test_failed", 0)
        total = bpy.context.scene.get("coon_test_total", 0)
        
        return {
            "success": failed == 0,
            "operator_result": str(result),
            "passed": passed,
            "failed": failed,
            "total": total,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def handle_get_csv_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get CSV data from the latest exports."""
    from procedural_human.testing.topology_checker import (
        get_latest_csvs,
        load_point_csv,
        load_edge_csv,
    )
    from procedural_human.config import get_codebase_path
    
    codebase = get_codebase_path()
    tmp_dir = str(codebase / "tmp") if codebase else ""
    
    point_csv, edge_csv = get_latest_csvs(tmp_dir)
    
    if not point_csv or not edge_csv:
        return {
            "success": False,
            "error": "No CSV files found"
        }
    
    result = {
        "success": True,
        "point_csv": point_csv,
        "edge_csv": edge_csv,
    }
    
    # Optionally load point data
    if params.get("include_points", False):
        points = load_point_csv(point_csv)
        result["points"] = {
            pid: {
                "position": p.position,
                "face_idx": p.debug_orig_face_idx,
                "flip_domain": p.debug_flip_domain,
            }
            for pid, p in points.items()
        }
    
    # Optionally load edge data
    if params.get("include_edges", False):
        edges = load_edge_csv(edge_csv)
        result["edges"] = {
            eid: {
                "vert_x": e.vert_x,
                "vert_y": e.vert_y,
            }
            for eid, e in edges.items()
        }
    
    return result


def handle_get_point_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get data for a specific point."""
    from procedural_human.testing.topology_checker import (
        get_latest_csvs,
        load_point_csv,
    )
    from procedural_human.config import get_codebase_path
    
    point_id = params.get("point_id")
    if point_id is None:
        return {"success": False, "error": "point_id required"}
    
    codebase = get_codebase_path()
    tmp_dir = str(codebase / "tmp") if codebase else ""
    
    point_csv, _ = get_latest_csvs(tmp_dir)
    if not point_csv:
        return {"success": False, "error": "No point CSV found"}
    
    points = load_point_csv(point_csv)
    
    if point_id not in points:
        return {"success": False, "error": f"Point {point_id} not found"}
    
    p = points[point_id]
    return {
        "success": True,
        "point_id": point_id,
        "position": p.position,
        "face_idx": p.debug_orig_face_idx,
        "loop_start": p.debug_orig_loop_start,
        "flip_domain": p.debug_flip_domain,
        "on_edge": p.debug_on_edge,
        "domain_pos": (p.debug_domain_x, p.debug_domain_y),
        "raw_data": p.raw_data,
    }


def handle_check_corner(params: Dict[str, Any]) -> Dict[str, Any]:
    """Check topology for a specific corner point."""
    from procedural_human.testing.topology_checker import (
        get_latest_csvs,
        check_corner_topology,
    )
    from procedural_human.config import get_codebase_path
    
    corner_id = params.get("corner_id")
    if corner_id is None:
        return {"success": False, "error": "corner_id required"}
    
    codebase = get_codebase_path()
    tmp_dir = str(codebase / "tmp") if codebase else ""
    
    point_csv, edge_csv = get_latest_csvs(tmp_dir)
    if not point_csv or not edge_csv:
        return {"success": False, "error": "No CSV files found"}
    
    result = check_corner_topology(
        point_csv, edge_csv, corner_id,
        expected_edge_length=params.get("edge_length", 2.0),
        subdivisions=params.get("subdivisions", 2)
    )
    
    return {
        "success": True,
        "passed": result.passed,
        "corner_id": result.corner_id,
        "message": result.message,
        "connected_points": result.connected_points,
        "distances": result.distances,
        "star_pattern": result.star_pattern_detected,
        "details": result.details,
    }


def handle_exec_python(params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute arbitrary Python code (use with caution)."""
    code = params.get("code", "")
    if not code:
        return {"success": False, "error": "No code provided"}
    
    try:
        # Execute in a namespace with bpy available
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


# Command registry
COMMAND_HANDLERS: Dict[str, Callable] = {
    "run_test": handle_run_test,
    "setup_test": handle_setup_test,
    "apply_export": handle_apply_export,
    "verify_topology": handle_verify_topology,
    "get_csv_data": handle_get_csv_data,
    "get_point_data": handle_get_point_data,
    "check_corner": handle_check_corner,
    "exec_python": handle_exec_python,
    "ping": lambda p: {"success": True, "message": "pong"},
    "list_commands": lambda p: {"success": True, "commands": list(COMMAND_HANDLERS.keys())},
}


# ============================================================================
# HTTP SERVER
# ============================================================================

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
        
        # Read request body
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
        
        # Queue the command for execution in the main thread
        _result_counter += 1
        command_id = _result_counter
        
        _command_queue.append({
            "id": command_id,
            "action": action,
            "params": params,
        })
        
        # Wait for result (with timeout)
        import time
        timeout = 30  # seconds
        start = time.time()
        
        while command_id not in _result_queue:
            if time.time() - start > timeout:
                self._send_json_response({
                    "error": "Command timeout",
                    "command_id": command_id
                }, 504)
                return
            time.sleep(0.05)
        
        # Get and return result
        result = _result_queue.pop(command_id)
        self._send_json_response(result)


def _process_command_queue():
    """Process pending commands in the main Blender thread."""
    global _command_queue, _result_queue
    
    while _command_queue:
        cmd = _command_queue.pop(0)
        
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
        
        _result_queue[cmd["id"]] = result
    
    # Return time until next call (0.1 seconds)
    return 0.1


# ============================================================================
# SERVER CONTROL
# ============================================================================

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
        return False
    
    try:
        _server = HTTPServer((host, port), BlenderCommandHandler)
        _server_thread = threading.Thread(target=_server.serve_forever, daemon=True)
        _server_thread.start()
        
        # Register timer to process commands in main thread
        if not bpy.app.timers.is_registered(_process_command_queue):
            bpy.app.timers.register(_process_command_queue, first_interval=0.1)
        
        print(f"[BlenderServer] Started on http://{host}:{port}")
        print(f"[BlenderServer] Available commands: {list(COMMAND_HANDLERS.keys())}")
        return True
        
    except Exception as e:
        print(f"[BlenderServer] Failed to start: {e}")
        _server = None
        _server_thread = None
        return False


def stop_server():
    """Stop the HTTP command server (non-blocking)."""
    global _server, _server_thread

    if _server is None:
        print("[BlenderServer] Server not running")
        return

    # Unregister timer
    if bpy.app.timers.is_registered(_process_command_queue):
        bpy.app.timers.unregister(_process_command_queue)

    # Shutdown server in a separate thread to avoid blocking
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


def is_server_running() -> bool:
    """Check if the server is running."""
    return _server is not None


def get_server_url() -> Optional[str]:
    """Get the server URL if running."""
    if _server is None:
        return None
    host, port = _server.server_address
    return f"http://{host}:{port}"


# ============================================================================
# BLENDER OPERATORS
# ============================================================================

from procedural_human.decorators.operator_decorator import procedural_operator
from bpy.types import Operator
from bpy.props import IntProperty, StringProperty


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
