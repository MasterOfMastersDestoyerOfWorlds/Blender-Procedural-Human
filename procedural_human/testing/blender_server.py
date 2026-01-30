"""
Blender HTTP Command Server

A lightweight HTTP server that runs inside Blender using bpy.app.timers,
allowing external tools (like an MCP server) to send commands to Blender.

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
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, Optional, Callable
from functools import partial
_server: Optional[HTTPServer] = None
_server_thread: Optional[threading.Thread] = None
_command_queue: list = []
_result_queue: dict = {}
_result_counter: int = 0

def handle_run_test(params: Dict[str, Any]) -> Dict[str, Any]:
    """Run the full Coon patch test."""
    subdivisions = params.get("subdivisions", 2)
    create_new = params.get("create_new_cube", True)
    subdivide_edge = params.get("subdivide_edge", False)
    
    try:
        result = bpy.ops.procedural.run_full_coon_test(
            subdivisions=subdivisions,
            create_new_cube=create_new,
            subdivide_edge=subdivide_edge
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


def handle_render_viewport(params: Dict[str, Any]) -> Dict[str, Any]:
    """Render the scene and save to file."""
    from procedural_human.config import get_codebase_path
    import os
    from datetime import datetime
    
    codebase = get_codebase_path()
    tmp_dir = str(codebase / "tmp") if codebase else ""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_path = os.path.join(tmp_dir, f"render_{timestamp}.png")
    output_path = params.get("output_path", default_path)
    resolution = params.get("resolution", [800, 600])
    
    try:
        scene = bpy.context.scene
        scene.render.resolution_x = resolution[0]
        scene.render.resolution_y = resolution[1]
        scene.render.filepath = output_path
        scene.render.image_settings.file_format = 'PNG'
        
        bpy.ops.render.render(write_still=True)
        
        return {
            "success": True,
            "path": output_path,
            "resolution": resolution
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def handle_capture_viewport(params: Dict[str, Any]) -> Dict[str, Any]:
    """Capture 3D viewport screenshot using OpenGL render."""
    from procedural_human.config import get_codebase_path
    import os
    from datetime import datetime
    
    codebase = get_codebase_path()
    tmp_dir = str(codebase / "tmp") if codebase else ""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_path = os.path.join(tmp_dir, f"viewport_{timestamp}.png")
    output_path = params.get("output_path", default_path)
    
    try:
        scene = bpy.context.scene
        scene.render.filepath = output_path
        scene.render.image_settings.file_format = 'PNG'
        
        bpy.ops.render.opengl(write_still=True)
        
        return {
            "success": True,
            "path": output_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def handle_get_mesh_metrics(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get geometric metrics for the active mesh object."""
    obj_name = params.get("object_name")
    
    try:
        if obj_name:
            obj = bpy.data.objects.get(obj_name)
            if not obj:
                return {"success": False, "error": f"Object '{obj_name}' not found"}
        else:
            obj = bpy.context.active_object
            if not obj:
                return {"success": False, "error": "No active object"}
        
        if obj.type != 'MESH':
            return {"success": False, "error": f"Object is not a mesh: {obj.type}"}
        
        mesh = obj.data
        
        # Count faces by number of sides
        face_sides = {}
        for poly in mesh.polygons:
            sides = len(poly.vertices)
            face_sides[sides] = face_sides.get(sides, 0) + 1
        
        # Calculate bounding box dimensions
        bbox = [list(v[:]) for v in obj.bound_box]
        
        return {
            "success": True,
            "object_name": obj.name,
            "vertex_count": len(mesh.vertices),
            "edge_count": len(mesh.edges),
            "face_count": len(mesh.polygons),
            "face_sides_histogram": face_sides,
            "bounding_box": bbox,
            "dimensions": list(obj.dimensions),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def handle_apply_node_group(params: Dict[str, Any]) -> Dict[str, Any]:
    """Create an object with a geometry node group applied."""
    group_name = params.get("group_name")
    inputs = params.get("inputs", {})
    object_name = params.get("object_name", "NodeGroupTest")
    
    if not group_name:
        return {"success": False, "error": "group_name is required"}
    
    try:
        # Create a simple mesh (plane or cube) as base
        bpy.ops.mesh.primitive_plane_add(size=1)
        obj = bpy.context.active_object
        obj.name = object_name
        
        # Add geometry nodes modifier
        mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
        
        # Get or create the node group
        if group_name in bpy.data.node_groups:
            node_group = bpy.data.node_groups[group_name]
        else:
            # Try to create it by calling the creation function
            # Import the geo_node_groups module to trigger registration
            from procedural_human import geo_node_groups
            
            # Check registry for creation function
            from procedural_human.decorators.geo_node_decorator import geo_node_group as decorator
            
            # Look for matching creation function
            create_func_name = f"create_{group_name.lower()}_group"
            for func_name, func in decorator.registry.items():
                if func_name.lower() == create_func_name.lower():
                    node_group = func()
                    break
            else:
                # Try direct group name match
                if group_name in bpy.data.node_groups:
                    node_group = bpy.data.node_groups[group_name]
                else:
                    return {"success": False, "error": f"Node group '{group_name}' not found"}
        
        mod.node_group = node_group
        
        # Set input values
        for input_name, value in inputs.items():
            if input_name in mod:
                mod[input_name] = value
        
        return {
            "success": True,
            "object_name": obj.name,
            "node_group": node_group.name,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def handle_setup_basalt_test(params: Dict[str, Any]) -> Dict[str, Any]:
    """Setup a basalt columns test scene with camera and lighting."""
    size_x = params.get("size_x", 10.0)
    size_y = params.get("size_y", 10.0)
    resolution = params.get("resolution", 20)
    render_after = params.get("render", True)
    
    try:
        # Clear existing objects (optional)
        if params.get("clear_scene", False):
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()
        
        # Create basalt columns
        result = handle_apply_node_group({
            "group_name": "BasaltColumns",
            "object_name": "BasaltTest",
            "inputs": {
                "Size X": size_x,
                "Size Y": size_y,
                "Resolution": resolution,
            }
        })
        
        if not result.get("success"):
            return result
        
        obj = bpy.data.objects.get(result["object_name"])
        
        # Position camera
        cam_data = bpy.data.cameras.new("TestCamera")
        cam = bpy.data.objects.new("TestCamera", cam_data)
        bpy.context.collection.objects.link(cam)
        
        # Isometric-ish view
        cam.location = (size_x * 1.5, -size_y * 1.5, size_x * 1.2)
        cam.rotation_euler = (1.1, 0, 0.8)
        bpy.context.scene.camera = cam
        
        # Add sun light
        light_data = bpy.data.lights.new("TestSun", type='SUN')
        light_data.energy = 3
        light = bpy.data.objects.new("TestSun", light_data)
        bpy.context.collection.objects.link(light)
        light.rotation_euler = (0.8, 0.2, 0.5)
        
        # Render if requested
        render_path = None
        if render_after:
            render_result = handle_render_viewport({
                "resolution": params.get("render_resolution", [800, 600])
            })
            if render_result.get("success"):
                render_path = render_result["path"]
        
        return {
            "success": True,
            "object_name": result["object_name"],
            "camera": cam.name,
            "render_path": render_path,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def handle_validate_geometry(params: Dict[str, Any]) -> Dict[str, Any]:
    """Validate that evaluated geometry has actual data (vertices, edges, faces).
    
    Uses the depsgraph to get the EVALUATED geometry after modifiers/geometry nodes,
    not just the base mesh data.
    """
    obj_name = params.get("object_name")
    
    try:
        obj = bpy.data.objects.get(obj_name) if obj_name else bpy.context.active_object
        if not obj:
            return {"success": False, "error": "No object found"}
        
        if obj.type != 'MESH':
            return {"success": False, "error": f"Object is not a mesh: {obj.type}"}
        
        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        data = eval_obj.data
        
        vertex_count = len(data.vertices) if hasattr(data, 'vertices') else 0
        edge_count = len(data.edges) if hasattr(data, 'edges') else 0
        face_count = len(data.polygons) if hasattr(data, 'polygons') else 0
        
        has_geometry = vertex_count > 0 or edge_count > 0 or face_count > 0
        
        return {
            "success": has_geometry,
            "object_name": obj.name,
            "vertex_count": vertex_count,
            "edge_count": edge_count,
            "face_count": face_count,
            "error": None if has_geometry else "Geometry has no vertices, edges, or faces"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


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
    "apply_node_group": handle_apply_node_group,
    "setup_basalt_test": handle_setup_basalt_test,
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
        
        _command_queue.append({
            "id": command_id,
            "action": action,
            "params": params,
        })
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
        return False
    
    try:
        _server = HTTPServer((host, port), BlenderCommandHandler)
        _server_thread = threading.Thread(target=_server.serve_forever, daemon=True)
        _server_thread.start()
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


def is_server_running() -> bool:
    """Check if the server is running."""
    return _server is not None


def get_server_url() -> Optional[str]:
    """Get the server URL if running."""
    if _server is None:
        return None
    host, port = _server.server_address
    return f"http://{host}:{port}"

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
