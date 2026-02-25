import os
import re
import mathutils
from collections.abc import Iterable
from pathlib import Path

import bpy

from procedural_human.config import get_codebase_path

CODEBASE_PATH = get_codebase_path()

SOCKET_TYPE_MAP = {
    'VALUE': 'NodeSocketFloat',
    'INT': 'NodeSocketInt',
    'BOOLEAN': 'NodeSocketBool',
    'VECTOR': 'NodeSocketVector',
    'RGBA': 'NodeSocketColor',
    'STRING': 'NodeSocketString',
    'SHADER': 'NodeSocketShader',
    'GEOMETRY': 'NodeSocketGeometry',
    'OBJECT': 'NodeSocketObject',
    'IMAGE': 'NodeSocketImage',
    'COLLECTION': 'NodeSocketCollection',
    'MATERIAL': 'NodeSocketMaterial',
    'ROTATION': 'NodeSocketRotation',
    'MATRIX': 'NodeSocketMatrix',
    'MENU': 'NodeSocketMenu',
}

SKIP_PROPS = frozenset({
    "rna_type", "name", "label", "location", "width", "height",
    "inputs", "outputs", "parent", "color", "select", "dimensions",
    "interface", "bl_icon", "bl_label", "bl_static_type",
    "bl_width_default", "bl_width_min",
    "bl_width_max", "bl_height_default", "bl_height_min", "bl_height_max",
    "location_absolute", "warning_propagation", "use_custom_color",
    "show_options", "show_preview", "hide", "mute", "show_texture",
    "bl_description", "bl_idname", "active_item",
    "is_active_output", "input_type", "output_type",
})

SKIP_OBJECT_TYPES = (
    bpy.types.NodeSocket, bpy.types.NodeInputs, bpy.types.NodeOutputs,
)

SKIP_VALUE_TYPES = (
    bpy.types.Object, bpy.types.Collection, bpy.types.Image,
    bpy.types.Material, bpy.types.Texture,
)


def get_next_temp_file_path(base_dir, prefix="temp_"):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    files = os.listdir(base_dir)
    pattern = re.compile(f"{prefix}(\\d+).py")

    existing_indices = []
    for f in files:
        match = pattern.match(f)
        if match:
            existing_indices.append(int(match.group(1)))

    count = (max(existing_indices) + 1) if existing_indices else 0
    return os.path.join(base_dir, f"{prefix}{count}.py")


def clean_string(s):
    return s.replace('"', '\\"').replace("\n", "\\n")


def to_snake_case(name):
    s = name.replace(" ", "_").replace(".", "_").replace("/", "_")
    s = re.sub(r"[^\w]", "_", s)
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()
    return re.sub(r"_{2,}", "_", s).strip("_")


def get_unique_var_name(name, existing_names):
    base_name = to_snake_case(name)
    base_name = re.sub(r"_{2,}", "_", base_name)

    if base_name not in existing_names:
        return base_name
    count = 1
    while f"{base_name}_{count}" in existing_names:
        count += 1
    return f"{base_name}_{count}"


def to_python_repr(val):
    if isinstance(val, str):
        return f'"{clean_string(val)}"'
    if isinstance(val, (int, float, bool)):
        return str(val)
    if isinstance(val, mathutils.Euler):
        return f"Euler({val[:]!r}, '{val.order}')"
    if isinstance(val, mathutils.Vector):
        return f"Vector({val[:]!r})"
    if isinstance(val, mathutils.Color):
        return f"Color({val[:]!r})"
    if isinstance(val, mathutils.Matrix):
        return f"Matrix({[list(r) for r in val]!r})"

    if hasattr(val, "to_tuple"):
        return str(val.to_tuple())
    if hasattr(val, "to_list"):
        return str(val.to_list())
    if isinstance(val, Iterable):
        try:
            return str(list(val))
        except:
            pass
    return str(val)


def generate_curve_mapping_lines(var_name, node):
    """Generate code lines for a node's CurveMapping data."""
    if not hasattr(node, "mapping"):
        return []

    mapping = node.mapping
    lines = []
    lines.append(f"    {var_name}.mapping.extend = '{mapping.extend}'")
    lines.append(f"    {var_name}.mapping.use_clip = {mapping.use_clip}")
    lines.append(f"    {var_name}.mapping.clip_min_x = {mapping.clip_min_x}")
    lines.append(f"    {var_name}.mapping.clip_min_y = {mapping.clip_min_y}")
    lines.append(f"    {var_name}.mapping.clip_max_x = {mapping.clip_max_x}")
    lines.append(f"    {var_name}.mapping.clip_max_y = {mapping.clip_max_y}")

    for ci, curve in enumerate(mapping.curves):
        curve_var = f"{var_name}_curve_{ci}"
        lines.append(f"    {curve_var} = {var_name}.mapping.curves[{ci}]")
        for pi, point in enumerate(curve.points):
            x, y = point.location.x, point.location.y
            handle = point.handle_type
            if pi < 2:
                lines.append(f"    {curve_var}.points[{pi}].location = ({x}, {y})")
                lines.append(f"    {curve_var}.points[{pi}].handle_type = '{handle}'")
            else:
                pt_var = f"{curve_var}_pt{pi}"
                lines.append(f"    {pt_var} = {curve_var}.points.new({x}, {y})")
                lines.append(f"    {pt_var}.handle_type = '{handle}'")

    lines.append(f"    {var_name}.mapping.update()")
    return lines


def socket_index(socket, socket_list):
    for i, s in enumerate(socket_list):
        if s == socket:
            return i
    return -1


def resolve_socket_key(key, sockets):
    """Resolve a socket key (int index or str name) to an index."""
    if isinstance(key, int):
        return key
    for i, s in enumerate(sockets):
        if s.name == key:
            return i
    return None


def get_tmp_base_dir():
    """Get the tmp directory path for exports."""
    if CODEBASE_PATH:
        base_dir = CODEBASE_PATH / "tmp"
    else:
        base_dir = Path(os.path.dirname(__file__)).parent.parent / "tmp"
    base_dir.mkdir(parents=True, exist_ok=True)
    init_path = base_dir / "__init__.py"
    if not init_path.exists():
        try:
            init_path.touch()
        except Exception:
            pass
    return base_dir
