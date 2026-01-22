import bpy
import os
import re
import mathutils
from pathlib import Path
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.decorators.panel_decorator import procedural_panel
from procedural_human.config import get_codebase_path
from bpy.types import Operator, Panel
from collections.abc import Iterable

CODEBASE_PATH = get_codebase_path()


def get_next_temp_file_path(base_dir, prefix="temp_"):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    files = os.listdir(base_dir)
    count = 0
    pattern = re.compile(f"{prefix}(\d+).py")

    existing_indices = []
    for f in files:
        match = pattern.match(f)
        if match:
            existing_indices.append(int(match.group(1)))

    if existing_indices:
        count = max(existing_indices) + 1

    return os.path.join(base_dir, f"{prefix}{count}.py")


def clean_string(s):
    return s.replace('"', '\\"').replace("\n", "\\n")


def to_snake_case(name):
    s = name.replace(" ", "_").replace(".", "_")
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


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


class NodeGroupExporter:
    def __init__(self):
        self.visited_groups = set()
        self.generated_code_blocks = []

    def process_group(self, node_group):
        if node_group in self.visited_groups:
            return

        self.visited_groups.add(node_group)
        for node in node_group.nodes:
            if hasattr(node, "node_tree") and node.node_tree:
                if node.node_tree.library is not None:
                    continue  # Linked from external file
                if hasattr(node.node_tree, "asset_data") and node.node_tree.asset_data:
                    continue  # It's a bundled asset
                self.process_group(node.node_tree)
        function_name = f"create_{to_snake_case(clean_string(node_group.name))}_group"
        code = self.generate_group_code(node_group, function_name)
        self.generated_code_blocks.append(code)

    def generate_group_code(self, node_group, function_name):
        lines = []
        lines.append("@geo_node_group")
        lines.append(f"def {function_name}():")
        lines.append(f'    group_name = "{node_group.name}"')
        lines.append(f"    if group_name in bpy.data.node_groups:")
        lines.append(f"        return bpy.data.node_groups[group_name]")
        lines.append("")
        lines.append(
            f'    group = bpy.data.node_groups.new(group_name, "{node_group.bl_idname}")'
        )
        lines.append("")
        lines.append("    # --- Interface ---")
        for item in node_group.interface.items_tree:
            if item.item_type == "PANEL":
                continue
            socket_type = item.socket_type
            name = clean_string(item.name)

            io_type = item.in_out

            lines.append(
                f'    socket = group.interface.new_socket(name="{name}", in_out="{io_type}", socket_type="{socket_type}")'
            )
            if io_type == "INPUT":
                if hasattr(item, "default_value"):
                    val = item.default_value
                    if not isinstance(
                        val,
                        (
                            bpy.types.Object,
                            bpy.types.Collection,
                            bpy.types.Image,
                            bpy.types.Material,
                            bpy.types.Texture,
                        ),
                    ):
                        lines.append(
                            f"    socket.default_value = {to_python_repr(val)}"
                        )
            if hasattr(item, "min_value"):
                lines.append(f"    socket.min_value = {item.min_value}")
            if hasattr(item, "max_value"):
                lines.append(f"    socket.max_value = {item.max_value}")

        lines.append("")
        lines.append("    # --- Nodes ---")
        lines.append("    nodes = group.nodes")
        lines.append("    links = group.links")

        node_var_map = {}  # node.name -> var_name
        existing_var_names = set()
        for node in node_group.nodes:
            base_name_source = node.name
            if hasattr(node, "node_tree") and node.node_tree:
                base_name_source = node.node_tree.name

            var_name = get_unique_var_name(base_name_source, existing_var_names)
            existing_var_names.add(var_name)
            node_var_map[node.name] = var_name

        processed_nodes = set()
        skip_props = {
            "rna_type",
            "name",
            "label",
            "location",
            "width",
            "height",
            "inputs",
            "outputs",
            "parent",
            "color",
            "select",
            "dimensions",
            "interface",
            "bl_icon",
            "bl_width_default",
            "bl_width_min",
            "bl_width_max",
            "bl_height_default",
            "bl_height_min",
            "bl_height_max",
            "location_absolute",
            "warning_propagation",
            "use_custom_color",
            "show_options",
            "show_preview",
            "hide",
            "mute",
            "show_texture",
            "bl_description",
            "bl_idname",
            "active_item",
        }
        for node in node_group.nodes:
            var_name = node_var_map[node.name]

            lines.append(f'    {var_name} = nodes.new("{node.bl_idname}")')
            lines.append(f'    {var_name}.name = "{clean_string(node.name)}"')
            lines.append(f'    {var_name}.label = "{clean_string(node.label)}"')
            lines.append(
                f"    {var_name}.location = ({node.location.x}, {node.location.y})"
            )
            if hasattr(node, "node_tree") and node.node_tree:
                dep_func_name = (
                    f"create_{to_snake_case(clean_string(node.node_tree.name))}_group"
                )
                lines.append(f"    {var_name}.node_tree = {dep_func_name}()")
            for prop in node.bl_rna.properties:
                if prop.identifier in skip_props:
                    continue
                if prop.is_readonly:
                    continue
                if prop.identifier == "node_tree":
                    continue

                try:
                    val = getattr(node, prop.identifier)
                    if isinstance(
                        val,
                        (
                            bpy.types.NodeSocket,
                            bpy.types.NodeInputs,
                            bpy.types.NodeOutputs,
                        ),
                    ):
                        continue
                    lines.append(
                        f"    {var_name}.{prop.identifier} = {to_python_repr(val)}"
                    )
                except:
                    pass
            for j, inp in enumerate(node.inputs):
                if not inp.is_linked:
                    if hasattr(inp, "default_value"):
                        val = inp.default_value
                        if val is not None and not isinstance(
                            val,
                            (
                                bpy.types.Object,
                                bpy.types.Collection,
                                bpy.types.Image,
                                bpy.types.Material,
                                bpy.types.Texture,
                            ),
                        ):
                            lines.append(f"    # {inp.name}")
                            lines.append(
                                f"    {var_name}.inputs[{j}].default_value = {to_python_repr(val)}"
                            )
            processed_nodes.add(node.name)
            lines.append(f"    # Links for {var_name}")

            for link in node_group.links:
                if not link.is_valid:
                    continue

                from_node = link.from_node
                to_node = link.to_node
                other_node = None
                if from_node == node and to_node.name in processed_nodes:
                    other_node = to_node
                elif to_node == node and from_node.name in processed_nodes:
                    other_node = from_node

                if other_node:
                    from_var = node_var_map.get(from_node.name)
                    to_var = node_var_map.get(to_node.name)
                    from_idx = -1
                    for k, out in enumerate(from_node.outputs):
                        if out == link.from_socket:
                            from_idx = k
                            break

                    to_idx = -1
                    for k, inp in enumerate(to_node.inputs):
                        if inp == link.to_socket:
                            to_idx = k
                            break

                    if from_idx != -1 and to_idx != -1:
                        lines.append(
                            f"    links.new({from_var}.outputs[{from_idx}], {to_var}.inputs[{to_idx}])"
                        )

            lines.append("")

        lines.append("    auto_layout_nodes(group)")
        lines.append("    return group")

        return "\n".join(lines)

    def get_full_code(self):
        header = []
        header.append("import bpy")
        header.append("import math")
        header.append("from mathutils import Vector, Color, Matrix, Euler")
        header.append(
            "from procedural_human.utils.node_layout import auto_layout_nodes"
        )
        header.append(
            "from procedural_human.decorators.geo_node_decorator import geo_node_group"
        )
        header.append("")

        return "\n".join(header) + "\n\n" + "\n\n".join(self.generated_code_blocks)


@procedural_operator
class NODE_OT_export_active_group_to_python(Operator):
    """Export the currently active node group to a Python script"""

    bl_idname = "node.export_active_group_to_python"
    bl_label = "Export Active Node Group to Python"

    def execute(self, context):
        node_group = None
        if context.space_data and context.space_data.type == "NODE_EDITOR":
            node_group = context.space_data.edit_tree
            if not node_group:
                node_group = context.space_data.node_tree
        if not node_group and context.active_object:
            for mod in context.active_object.modifiers:
                if mod.type == "NODES" and mod.node_group:
                    node_group = mod.node_group
                    break

        if not node_group:
            self.report({"ERROR"}, "No active node group found")
            return {"CANCELLED"}

        exporter = NodeGroupExporter()
        exporter.process_group(node_group)
        code = exporter.get_full_code()
        if CODEBASE_PATH:
            base_dir = CODEBASE_PATH / "tmp"
        else:
            base_dir = Path(os.path.dirname(__file__)).parent / "tmp"
        try:
            base_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.report(
                {"WARNING"},
                f"Could not create directory {base_dir}: {e}. Falling back to default.",
            )
            base_dir = Path(os.path.dirname(__file__)).parent / "tmp"
            if not os.path.exists(str(base_dir)):
                os.makedirs(str(base_dir))
        init_path = base_dir / "__init__.py"
        if not init_path.exists():
            try:
                with open(init_path, "w") as f:
                    pass
            except Exception as e:
                self.report({"WARNING"}, f"Could not create __init__.py: {e}")

        file_path = get_next_temp_file_path(str(base_dir))

        with open(file_path, "w") as f:
            f.write(code)

        self.report({"INFO"}, f"Exported to {file_path}")
        return {"FINISHED"}


def get_tmp_base_dir():
    """Get the tmp directory path for exports."""
    if CODEBASE_PATH:
        base_dir = CODEBASE_PATH / "tmp"
    else:
        base_dir = Path(os.path.dirname(__file__)).parent / "tmp"
    base_dir.mkdir(parents=True, exist_ok=True)
    init_path = base_dir / "__init__.py"
    if not init_path.exists():
        try:
            init_path.touch()
        except Exception:
            pass
    
    return base_dir



@procedural_panel
class NODE_PT_node_export(Panel):
    bl_label = "Node Export"
    bl_idname = "PROCEDURAL_PT_node_export"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Procedural"

    def draw(self, context):
        layout = self.layout
        layout.operator("node.export_active_group_to_python")
        layout.operator("curve.export_curve_to_csv")
