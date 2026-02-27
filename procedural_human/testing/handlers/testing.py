import traceback
from typing import Any, Dict

import bpy

from procedural_human.testing.handlers.capture import handle_render_viewport
from procedural_human.testing.handlers.geometry import handle_apply_node_group


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
