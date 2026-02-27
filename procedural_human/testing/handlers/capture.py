import traceback
from typing import Any, Dict

import bpy

from procedural_human.testing.handlers.common import _active_object, _log


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
        obj_name = params.get("object_name")
        obj = bpy.data.objects.get(obj_name) if obj_name else _active_object()

        # Ensure a validation camera exists and frames the active object.
        if not scene.camera:
            cam_data = bpy.data.cameras.new("ValidationRenderCamera")
            camera = bpy.data.objects.new("ValidationRenderCamera", cam_data)
            bpy.context.collection.objects.link(camera)
            scene.camera = camera
        else:
            camera = scene.camera

        if obj and obj.type == "MESH":
            from mathutils import Vector

            corners_world = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
            center = sum(corners_world, Vector((0.0, 0.0, 0.0))) / len(corners_world)
            max_extent = max(max(obj.dimensions.x, obj.dimensions.y), obj.dimensions.z, 1.0)
            camera.location = (
                center.x + max_extent * 2.5,
                center.y - max_extent * 2.5,
                center.z + max_extent * 2.0,
            )
            direction = center - camera.location
            camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

        # Ensure at least one key light in clean scenes.
        key_light = bpy.data.objects.get("ValidationKeyLight")
        if key_light is None:
            light_data = bpy.data.lights.new("ValidationKeyLight", type="SUN")
            light_data.energy = 4.0
            key_light = bpy.data.objects.new("ValidationKeyLight", light_data)
            bpy.context.collection.objects.link(key_light)
            key_light.rotation_euler = (0.8, 0.2, 0.5)

        # Use a fast, deterministic render setup for CLI validation.
        scene.render.engine = "BLENDER_EEVEE"
        if scene.world is None:
            scene.world = bpy.data.worlds.new("ValidationWorld")
        scene.world.color = (0.04, 0.04, 0.04)
        scene.render.resolution_x = resolution[0]
        scene.render.resolution_y = resolution[1]
        scene.render.filepath = output_path
        scene.render.image_settings.file_format = 'PNG'
        
        bpy.ops.render.render(write_still=True)

        # Guardrail: fallback to viewport capture if render is effectively black.
        try:
            img = bpy.data.images.load(output_path, check_existing=False)
            px = img.pixels
            if len(px) >= 4:
                sample_count = min(2048, len(px) // 4)
                step = max(1, (len(px) // 4) // sample_count)
                luminance_sum = 0.0
                count = 0
                for i in range(0, (len(px) // 4), step):
                    r = px[i * 4 + 0]
                    g = px[i * 4 + 1]
                    b = px[i * 4 + 2]
                    luminance_sum += (0.2126 * r + 0.7152 * g + 0.0722 * b)
                    count += 1
                avg_lum = luminance_sum / max(1, count)
                bpy.data.images.remove(img)
                if avg_lum < 0.01:
                    _log(f"render_black_fallback output={output_path} avg_lum={avg_lum:.6f}")
                    return handle_capture_viewport({"output_path": output_path})
        except Exception as img_exc:
            _log(f"render_brightness_check_failed error={img_exc}")
        
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
