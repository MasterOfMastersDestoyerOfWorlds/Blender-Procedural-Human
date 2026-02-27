from pathlib import Path
from datetime import datetime
from typing import Any
import bpy


def _create_plane_object(name: str) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(f"{name}Mesh")
    mesh.from_pydata(
        [(-0.5, -0.5, 0.0), (0.5, -0.5, 0.0), (0.5, 0.5, 0.0), (-0.5, 0.5, 0.0)],
        [],
        [(0, 1, 2, 3)],
    )
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    view_layer = getattr(bpy.context, "view_layer", None)
    if view_layer is not None:
        view_layer.objects.active = obj
    obj.select_set(True)
    return obj


def _active_object() -> Any:
    obj = getattr(bpy.context, "active_object", None)
    if obj is not None:
        return obj
    view_layer = getattr(bpy.context, "view_layer", None)
    if view_layer is not None:
        return getattr(view_layer.objects, "active", None)
    return None


def _log(message: str) -> None:
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        line = f"[{timestamp}] {message}\n"
        with _log_path().open("a", encoding="utf-8") as handle:
            handle.write(line)
    except Exception:
        pass


def _log_path() -> Path:
    from procedural_human.config import get_codebase_path, validate_codebase_path

    codebase = get_codebase_path()
    base_path = Path.cwd()
    if codebase:
        candidate = Path(codebase)
        if validate_codebase_path(candidate):
            base_path = candidate
    logs_dir = base_path / ".cursor" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir / "blender-server.log"
