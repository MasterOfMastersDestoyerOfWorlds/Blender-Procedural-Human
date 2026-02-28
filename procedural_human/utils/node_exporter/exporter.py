import re
from dataclasses import dataclass
from collections import defaultdict, deque

from procedural_human.utils.node_exporter.utils import (
    SKIP_PROPS, SKIP_OBJECT_TYPES, SKIP_VALUE_TYPES,
    clean_string, to_snake_case, to_pascal_case, get_unique_var_name,
    to_python_repr, generate_curve_mapping_lines, socket_index,
    resolve_socket_key,
)
from procedural_human.utils.node_exporter.frame_split import (
    FrameInterface, collect_frame_descendants, analyze_frame_interface,
    generate_main_code,
)


def _typed_repr(socket):
    """Return to_python_repr of a socket's default_value, casting float→int for INT sockets."""
    val = socket.default_value
    if socket.type == 'INT' and isinstance(val, float):
        return repr(int(val))
    return to_python_repr(val)


@dataclass
class ExportOptions:
    include_locations: bool = False
    include_labels: bool = True
    include_names: bool = False
    use_helpers: bool = True
    split_frames: bool = False


_RESERVED_CODEGEN_NAMES = frozenset({
    'group_name', 'group', 'needs_rebuild', 'nodes', 'links',
    'group_input', 'group_output', 'socket',
    'bpy', 'Vector', 'Color', 'Matrix', 'Euler',
    'geo_node_group', 'get_or_rebuild_node_group', 'auto_layout_nodes',
})


class NodeGroupExporter:
    def __init__(self, options=None):
        self.options = options or ExportOptions()
        self.visited_groups = set()
        self.generated_code_blocks = []
        self.generated_files = {}
        self.known_groups = {}
        self.helper_registry = {}
        self.used_helpers = set()
        self.used_group_imports = []

    def _build_known_groups(self):
        from procedural_human.decorators.geo_node_decorator import geo_node_group
        for name, func in geo_node_group.registry.items():
            module = getattr(func, '__module__', '')
            if '.tmp.' in module or module.endswith('.tmp'):
                continue
            self.known_groups[name] = module

    def _get_reserved_names(self):
        """Collect names that will be in scope in generated code to prevent variable collisions."""
        reserved = set(_RESERVED_CODEGEN_NAMES)
        for meta in self.helper_registry.values():
            reserved.add(meta.func_name)
        reserved.update(self.known_groups.keys())
        return reserved

    def _build_helper_registry(self):
        """Build the helper registry by scanning node_helpers for decorated functions.

        Scans the module directly for ``_node_helper_meta`` attributes rather
        than relying on the class-level registry, which can be lost during
        Blender's fallback module-reload path.
        """
        from procedural_human.decorators.node_helper_decorator import node_helper
        if node_helper.registry:
            self.helper_registry = dict(node_helper.registry)
            return

        import sys
        import inspect
        nh_module = sys.modules.get('procedural_human.geo_node_groups.node_helpers')
        if nh_module is None:
            return
        for _name, obj in inspect.getmembers(nh_module, inspect.isfunction):
            meta = getattr(obj, '_node_helper_meta', None)
            if meta is not None:
                self.helper_registry[meta.bl_idname] = meta

    def process_group(self, node_group):
        self._build_known_groups()
        if self.options.use_helpers:
            self._build_helper_registry()
        self._process_recursive(node_group)

    def _process_recursive(self, node_group):
        if node_group.name in self.visited_groups:
            return
        self.visited_groups.add(node_group.name)

        for node in node_group.nodes:
            if not (hasattr(node, "node_tree") and node.node_tree):
                continue
            if node.node_tree.library is not None:
                continue
            if hasattr(node.node_tree, "asset_data") and node.node_tree.asset_data:
                continue

            func_name = f"create_{to_snake_case(clean_string(node.node_tree.name))}_group"
            if func_name in self.known_groups:
                module = self.known_groups[func_name]
                if (module, func_name) not in self.used_group_imports:
                    self.used_group_imports.append((module, func_name))
                continue

            self._process_recursive(node.node_tree)

        function_name = f"create_{to_snake_case(clean_string(node_group.name))}_group"

        if self.options.split_frames:
            self._generate_split(node_group, function_name)
        else:
            code = self._generate_group_code(node_group, function_name)
            self.generated_code_blocks.append(code)

    # =====================================================================
    # Topological sort
    # =====================================================================

    def _topological_sort(self, nodes, links, node_names):
        name_to_node = {n.name: n for n in nodes}
        dependencies = defaultdict(set)

        for link in links:
            if not link.is_valid:
                continue
            src = link.from_node.name
            dst = link.to_node.name
            if src in node_names and dst in node_names and src != dst:
                dependencies[dst].add(src)

        in_degree = {n.name: len(dependencies.get(n.name, set())) for n in nodes}

        queue = deque(n for n in nodes if in_degree[n.name] == 0)
        result = []
        while queue:
            node = queue.popleft()
            result.append(node)
            for other_name in list(node_names):
                if node.name in dependencies.get(other_name, set()):
                    in_degree[other_name] -= 1
                    if in_degree[other_name] == 0:
                        queue.append(name_to_node[other_name])

        seen = {n.name for n in result}
        for n in nodes:
            if n.name not in seen:
                result.append(n)

        return result

    # =====================================================================
    # Input expression resolution
    # =====================================================================

    def _build_input_link_map(self, links):
        """Map each input socket to its source link.

        Uses (node_name, socket_index) as keys since Blender creates ephemeral
        Python wrapper objects, making ``id()`` unreliable.
        """
        m = {}
        for link in links:
            if link.is_valid:
                to_idx = socket_index(link.to_socket, link.to_node.inputs)
                m[(link.to_node.name, to_idx)] = link
        return m

    def _resolve_input(self, node, inp_idx, input_link_map, output_expr_map, node_var_map):
        """Resolve a node input to an expression string.

        :returns: (expression_string, is_linked)
        """
        link = input_link_map.get((node.name, inp_idx))
        if link:
            from_node = link.from_node
            from_idx = socket_index(link.from_socket, from_node.outputs)
            expr = output_expr_map.get((from_node.name, from_idx))
            if expr is not None:
                return expr, True
            if from_node.name in node_var_map:
                return f"{node_var_map[from_node.name]}.outputs[{from_idx}]", True
            socket = node.inputs[inp_idx]
            if hasattr(socket, "default_value") and socket.default_value is not None:
                return _typed_repr(socket), False
            return "None", False

        socket = node.inputs[inp_idx]
        if hasattr(socket, "default_value") and socket.default_value is not None:
            return _typed_repr(socket), False
        return "None", False

    # =====================================================================
    # Code generation - single group
    # =====================================================================

    def _generate_group_code(self, node_group, function_name,
                             nodes_subset=None, group_name_override=None,
                             interface_inputs=None, interface_outputs=None,
                             boundary_input_map=None, boundary_output_map=None):
        """Generate code for a single @geo_node_group function.

        :param nodes_subset: If provided, only include these nodes.
        :param group_name_override: Override the group name.
        :param interface_inputs: List of (name, socket_type) for sub-group inputs.
        :param interface_outputs: List of (name, socket_type) for sub-group outputs.
        :param boundary_input_map: Dict mapping (node_name, inp_idx) -> (gi_out_idx, to_node_name, to_inp_idx).
        :param boundary_output_map: Dict mapping (node_name, out_idx) -> (from_node_name, from_out_idx, go_inp_idx).
        """
        opts = self.options
        all_nodes = list(nodes_subset) if nodes_subset else list(node_group.nodes)
        all_node_names = {n.name for n in all_nodes}
        gname = group_name_override or node_group.name

        input_link_map = self._build_input_link_map(node_group.links)

        node_var_map = {}
        existing_var_names = self._get_reserved_names()
        for node in all_nodes:
            base_name = node.name
            if hasattr(node, "node_tree") and node.node_tree:
                base_name = node.node_tree.name
            var = get_unique_var_name(base_name, existing_var_names)
            existing_var_names.add(var)
            node_var_map[node.name] = var

        # Classify nodes
        output_expr_map = {}
        consumed_sockets = set()
        node_helper_meta = {}
        used_output_indices = defaultdict(set)

        for link in node_group.links:
            if link.is_valid and link.from_node.name in all_node_names:
                from_idx = socket_index(link.from_socket, link.from_node.outputs)
                used_output_indices[link.from_node.name].add(from_idx)

        for node in all_nodes:
            var = node_var_map[node.name]
            meta = self.helper_registry.get(node.bl_idname) if opts.use_helpers else None

            if meta:
                node_helper_meta[node.name] = meta
                outputs = meta.resolve_outputs(node)
                resolved_outputs = {}
                for out_key, suffix in outputs.items():
                    out_idx = resolve_socket_key(out_key, node.outputs)
                    if suffix is None:
                        resolved_outputs[out_idx] = var
                    else:
                        resolved_outputs[out_idx] = f"{var}{suffix}"
                    output_expr_map[(node.name, out_idx)] = resolved_outputs[out_idx]

                inputs = meta.resolve_inputs(node)
                for inp_key in inputs:
                    idx = resolve_socket_key(inp_key, node.inputs)
                    if idx is not None and idx < len(node.inputs):
                        consumed_sockets.add((node.name, idx))
            else:
                node_helper_meta[node.name] = None
                for i in range(len(node.outputs)):
                    output_expr_map[(node.name, i)] = f"{var}.outputs[{i}]"

        node_input_map = dict(node_var_map)
        for node in all_nodes:
            meta = node_helper_meta.get(node.name)
            if not meta:
                continue
            var = node_var_map[node.name]
            outputs = meta.resolve_outputs(node)
            if any(suffix is None for suffix in outputs.values()):
                node_input_map[node.name] = f"{var}.node"
            else:
                used = used_output_indices.get(node.name, set())
                for out_key, suffix in outputs.items():
                    out_idx = resolve_socket_key(out_key, node.outputs)
                    if out_idx in used and suffix is not None:
                        node_input_map[node.name] = f"{var}{suffix}.node"
                        break
                else:
                    first_suffix = next(v for v in outputs.values() if v is not None)
                    node_input_map[node.name] = f"{var}{first_suffix}.node"

        sorted_nodes = self._topological_sort(all_nodes, node_group.links, all_node_names)

        # === Emit code ===
        lines = []
        lines.append("@geo_node_group")
        lines.append(f"def {function_name}():")
        lines.append(f'    group_name = "{gname}"')
        lines.append(f"    group, needs_rebuild = get_or_rebuild_node_group(group_name)")
        lines.append(f"    if not needs_rebuild:")
        lines.append(f"        return group")
        lines.append("")

        # Interface
        if interface_inputs is not None or interface_outputs is not None:
            for name, stype in (interface_outputs or []):
                lines.append(
                    f'    group.interface.new_socket(name="{name}", in_out="OUTPUT", socket_type="{stype}")'
                )
            for name, stype in (interface_inputs or []):
                lines.append(
                    f'    group.interface.new_socket(name="{name}", in_out="INPUT", socket_type="{stype}")'
                )
        else:
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
                        if not isinstance(val, SKIP_VALUE_TYPES):
                            lines.append(f"    socket.default_value = {to_python_repr(val)}")
                if hasattr(item, "min_value"):
                    lines.append(f"    socket.min_value = {item.min_value}")
                if hasattr(item, "max_value"):
                    lines.append(f"    socket.max_value = {item.max_value}")

        lines.append("")
        lines.append("    nodes = group.nodes")
        lines.append("    links = group.links")

        has_group_input = False
        has_group_output = False

        if boundary_input_map:
            lines.append('    group_input = nodes.new("NodeGroupInput")')
            has_group_input = True
        if boundary_output_map:
            lines.append('    group_output = nodes.new("NodeGroupOutput")')
            lines.append("    group_output.is_active_output = True")
            has_group_output = True

        # Emit nodes with interleaved links
        processed = set()
        emitted_links = set()

        for node in sorted_nodes:
            var = node_var_map[node.name]
            meta = node_helper_meta.get(node.name)

            if meta:
                self._emit_helper_node(
                    lines, node, var, meta,
                    input_link_map, output_expr_map, node_var_map,
                    all_node_names, used_output_indices, node_group
                )
            else:
                self._emit_raw_node(
                    lines, node, var, node_group,
                    consumed_sockets, input_link_map
                )

            processed.add(node.name)

            self._emit_interleaved_links(
                lines, node, processed, node_group.links,
                all_node_names, consumed_sockets,
                output_expr_map, node_var_map, emitted_links,
                node_input_map=node_input_map
            )

            lines.append("")

        # Emit boundary links for sub-groups
        if boundary_input_map:
            for sock_id, (gi_out_idx, to_node_name, to_inp_idx) in boundary_input_map.items():
                if to_node_name in node_var_map:
                    lines.append(
                        f"    links.new(group_input.outputs[{gi_out_idx}], "
                        f"{node_input_map[to_node_name]}.inputs[{to_inp_idx}])"
                    )
        if boundary_output_map:
            for sock_id, (from_node_name, from_out_idx, go_inp_idx) in boundary_output_map.items():
                if from_node_name in node_var_map:
                    from_expr = output_expr_map.get(
                        (from_node_name, from_out_idx),
                        f"{node_var_map[from_node_name]}.outputs[{from_out_idx}]"
                    )
                    lines.append(
                        f"    links.new({from_expr}, group_output.inputs[{go_inp_idx}])"
                    )

        # Frame nodes and parent assignments
        frame_nodes = [n for n in sorted_nodes if n.bl_idname == "NodeFrame"]
        for fnode in frame_nodes:
            var = node_var_map[fnode.name]
            lines.append(f'    {var} = nodes.new("NodeFrame")')
            if fnode.label:
                lines.append(f'    {var}.label = "{clean_string(fnode.label)}"')
            lines.append(f"    {var}.shrink = {fnode.shrink}")
            lines.append(f"    {var}.label_size = {fnode.label_size}")

        needs_parent = False
        for node in all_nodes:
            if node.parent is not None and node.parent.name in all_node_names:
                needs_parent = True
                break
        if needs_parent:
            lines.append("")
            for node in all_nodes:
                if node.parent is not None and node.parent.name in all_node_names:
                    child_var = node_var_map.get(node.name)
                    parent_var = node_var_map.get(node.parent.name)
                    if child_var and parent_var:
                        meta = node_helper_meta.get(node.name)
                        if meta:
                            lines.append(f"    {child_var}.node.parent = {parent_var}")
                        else:
                            lines.append(f"    {child_var}.parent = {parent_var}")

        lines.append("")
        lines.append("    auto_layout_nodes(group)")
        lines.append("    return group")

        return "\n".join(lines)

    # =====================================================================
    # Link emission
    # =====================================================================

    def _emit_interleaved_links(self, lines, current_node, processed, all_links,
                                all_node_names, consumed_sockets,
                                output_expr_map, node_var_map, emitted_links,
                                node_input_map=None):
        """Emit links where both endpoints have been processed."""
        nim = node_input_map or node_var_map
        for link in all_links:
            if not link.is_valid:
                continue
            from_name = link.from_node.name
            to_name = link.to_node.name
            if from_name not in all_node_names or to_name not in all_node_names:
                continue

            to_idx = socket_index(link.to_socket, link.to_node.inputs)
            if (to_name, to_idx) in consumed_sockets:
                continue

            if not (from_name in processed and to_name in processed):
                continue

            from_idx = socket_index(link.from_socket, link.from_node.outputs)

            link_key = (from_name, from_idx, to_name, to_idx)
            if link_key in emitted_links:
                continue
            emitted_links.add(link_key)

            from_expr = output_expr_map.get(
                (from_name, from_idx),
                f"{node_var_map[from_name]}.outputs[{from_idx}]"
            )
            lines.append(
                f"    links.new({from_expr}, {nim[to_name]}.inputs[{to_idx}])"
            )

    # =====================================================================
    # Emit: helper node
    # =====================================================================

    def _emit_helper_node(self, lines, node, var, meta,
                          input_link_map, output_expr_map, node_var_map,
                          all_node_names, used_output_indices, node_group):
        self.used_helpers.add(meta.func_name)

        def resolve_input(key):
            idx = resolve_socket_key(key, node.inputs)
            if idx is not None and idx < len(node.inputs):
                return self._resolve_input(
                    node, idx, input_link_map, output_expr_map, node_var_map
                )
            return "None", False

        if meta.custom_emit:
            emit_lines, out_map = meta.custom_emit(node, var, resolve_input)
            lines.extend(emit_lines)
            for out_idx, expr in out_map.items():
                output_expr_map[(node.name, out_idx)] = expr
            return

        args = ["group"]
        for prop in meta.prop_args:
            val = getattr(node, prop)
            if isinstance(val, str):
                args.append(f'"{val}"')
            else:
                args.append(repr(val))

        inputs = meta.resolve_inputs(node)
        optional = meta.resolve_optional_inputs(node)

        arg_positions = {name: i for i, name in enumerate(meta.arg_order)}
        sorted_inputs = sorted(inputs.items(), key=lambda x: arg_positions.get(x[1], 999))
        for inp_key, arg_name in sorted_inputs:
            expr, is_linked = resolve_input(inp_key)
            if not is_linked and inp_key in optional:
                continue
            args.append(expr)

        outputs = meta.resolve_outputs(node)
        used = used_output_indices.get(node.name, set())

        multi_outputs = {k: v for k, v in outputs.items() if v is not None}
        if multi_outputs:
            parts = []
            for out_key in sorted(multi_outputs.keys()):
                suffix = multi_outputs[out_key]
                out_idx = resolve_socket_key(out_key, node.outputs)
                if out_idx in used:
                    parts.append(f"{var}{suffix}")
                else:
                    parts.append("_")
            lhs = ", ".join(parts)
            lines.append(f"    {lhs} = {meta.func_name}({', '.join(args)})")
        else:
            lines.append(f"    {var} = {meta.func_name}({', '.join(args)})")

        if any(v is None for v in outputs.values()):
            node_accessor = f"{var}.node"
        elif multi_outputs:
            node_accessor = None
            for out_key in sorted(multi_outputs.keys()):
                suffix = multi_outputs[out_key]
                out_idx = resolve_socket_key(out_key, node.outputs)
                if out_idx in used:
                    node_accessor = f"{var}{suffix}.node"
                    break
            if node_accessor is None:
                return
        else:
            node_accessor = var

        consumed_keys = set(inputs.keys())
        for j, inp in enumerate(node.inputs):
            if j in consumed_keys or inp.name in consumed_keys:
                continue
            if not inp.is_linked and hasattr(inp, "default_value"):
                val = inp.default_value
                if val is not None and not isinstance(val, SKIP_VALUE_TYPES):
                    lines.append(f"    {node_accessor}.inputs[{j}].default_value = {_typed_repr(inp)}")

    # =====================================================================
    # Emit: raw node
    # =====================================================================

    def _emit_raw_node(self, lines, node, var, node_group,
                       consumed_sockets, input_link_map):
        opts = self.options

        if node.bl_idname == "NodeFrame":
            return

        lines.append(f'    {var} = nodes.new("{node.bl_idname}")')

        if opts.include_names:
            lines.append(f'    {var}.name = "{clean_string(node.name)}"')
        if opts.include_labels and node.label:
            lines.append(f'    {var}.label = "{clean_string(node.label)}"')
        if opts.include_locations:
            lines.append(f"    {var}.location = ({node.location.x}, {node.location.y})")

        if hasattr(node, "node_tree") and node.node_tree:
            func_name = f"create_{to_snake_case(clean_string(node.node_tree.name))}_group"
            lines.append(f"    {var}.node_tree = {func_name}()")

        for prop in node.bl_rna.properties:
            if prop.identifier in SKIP_PROPS:
                continue
            if prop.is_readonly:
                continue
            if prop.identifier == "node_tree":
                continue
            try:
                val = getattr(node, prop.identifier)
                if isinstance(val, SKIP_OBJECT_TYPES):
                    continue
                lines.append(f"    {var}.{prop.identifier} = {to_python_repr(val)}")
            except:
                pass

        lines.extend(generate_curve_mapping_lines(var, node))

        self._emit_dynamic_items(lines, node, var)

        for j, inp in enumerate(node.inputs):
            if (node.name, j) in consumed_sockets:
                continue
            if not inp.is_linked:
                if hasattr(inp, "default_value"):
                    val = inp.default_value
                    if val is not None and not isinstance(val, SKIP_VALUE_TYPES):
                        lines.append(
                            f"    {var}.inputs[{j}].default_value = {_typed_repr(inp)}"
                        )

    _DYNAMIC_ITEM_ATTRS = {
        "GeometryNodeCaptureAttribute": "capture_items",
        "GeometryNodeRepeatOutput": "repeat_items",
        "GeometryNodeSimulationOutput": "items",
        "GeometryNodeIndexSwitch": "index_switch_items",
    }

    _DATA_TYPE_TO_SOCKET_TYPE = {
        "FLOAT": "FLOAT",
        "INT": "INT",
        "BOOLEAN": "BOOLEAN",
        "FLOAT_VECTOR": "VECTOR",
        "FLOAT_COLOR": "RGBA",
        "FLOAT2": "VECTOR",
        "QUATERNION": "ROTATION",
        "FLOAT4X4": "MATRIX",
        "ROTATION": "ROTATION",
        "VECTOR": "VECTOR",
        "RGBA": "RGBA",
        "MATRIX": "MATRIX",
        "STRING": "STRING",
        "GEOMETRY": "GEOMETRY",
    }

    def _emit_dynamic_items(self, lines, node, var):
        attr_name = self._DYNAMIC_ITEM_ATTRS.get(node.bl_idname)
        if not attr_name:
            return
        items = getattr(node, attr_name, None)
        if items is None:
            return
        for item in items:
            data_type = getattr(item, "data_type", None)
            name = getattr(item, "name", "")
            if data_type is not None:
                socket_type = self._DATA_TYPE_TO_SOCKET_TYPE.get(data_type, data_type)
                lines.append(
                    f'    {var}.{attr_name}.new("{socket_type}", "{clean_string(name)}")'
                )
            else:
                lines.append(
                    f'    {var}.{attr_name}.new()'
                )

    # =====================================================================
    # Frame splitting
    # =====================================================================

    def _generate_split(self, node_group, function_name,
                        scope_nodes=None, file_prefix="",
                        group_name_override=None, parent_interface=None):
        """Split frames into separate files, recursing into sub-frames.

        :param scope_nodes: List of nodes to consider. None means all.
        :param file_prefix: Path prefix for generated files (e.g. ``"collar/"``).
        :param group_name_override: Override the Blender group name for sub-groups.
        :param parent_interface: FrameInterface from the parent split level.
        """
        if scope_nodes is not None:
            scoped = list(scope_nodes)
        else:
            scoped = list(node_group.nodes)

        scope_names = {n.name for n in scoped}

        top_frames = [
            n for n in scoped
            if n.bl_idname == "NodeFrame"
            and (n.parent is None or n.parent.name not in scope_names)
        ]

        if not top_frames:
            if scope_nodes is not None:
                code = self._generate_group_code(
                    node_group, function_name,
                    nodes_subset=scoped,
                    group_name_override=group_name_override,
                    interface_inputs=parent_interface.inputs if parent_interface else None,
                    interface_outputs=parent_interface.outputs if parent_interface else None,
                    boundary_input_map=parent_interface.input_map if parent_interface else None,
                    boundary_output_map=parent_interface.output_map if parent_interface else None,
                )
                parts = file_prefix.rstrip("/").split("/")
                filename = f"{parts[-1]}.py" if parts and parts[-1] else "output.py"
                parent_dir = "/".join(parts[:-1])
                if parent_dir:
                    self.generated_files[f"{parent_dir}/{filename}"] = code
                else:
                    self.generated_files[filename] = code
            else:
                code = self._generate_group_code(node_group, function_name)
                self.generated_code_blocks.append(code)
            return

        frame_members = {}
        for frame in top_frames:
            frame_members[frame.name] = collect_frame_descendants(frame, scoped)

        all_framed = set()
        for members in frame_members.values():
            all_framed.update(members)

        frame_interfaces = {}
        for frame in top_frames:
            interface = analyze_frame_interface(
                frame, frame_members[frame.name], node_group, scope=scope_names
            )
            frame_interfaces[frame.name] = interface

        base = function_name
        if base.startswith("create_"):
            base = base[len("create_"):]
        if base.endswith("_group"):
            base = base[:-len("_group")]
        group_base_name = base

        for frame in top_frames:
            interface = frame_interfaces[frame.name]
            members = frame_members[frame.name]
            frame_label = frame.label or frame.name
            frame_snake = to_snake_case(clean_string(frame_label))

            sub_func = f"create_{group_base_name}_{frame_snake}_group"
            parent_pascal = to_pascal_case(group_name_override or node_group.name)
            sub_group_name = f"{parent_pascal}{to_pascal_case(frame_label)}"

            member_nodes = [
                n for n in scoped
                if n.name in members and n != frame
            ]

            child_frames = [
                n for n in member_nodes
                if n.bl_idname == "NodeFrame" and n.parent == frame
            ]

            if child_frames:
                self._generate_split(
                    node_group, sub_func,
                    scope_nodes=member_nodes,
                    file_prefix=f"{file_prefix}{frame_snake}/",
                    group_name_override=sub_group_name,
                    parent_interface=interface,
                )
            else:
                code = self._generate_group_code(
                    node_group, sub_func,
                    nodes_subset=member_nodes,
                    group_name_override=sub_group_name,
                    interface_inputs=interface.inputs,
                    interface_outputs=interface.outputs,
                    boundary_input_map=interface.input_map,
                    boundary_output_map=interface.output_map,
                )
                self.generated_files[f"{file_prefix}{frame_snake}.py"] = code

        main_code = generate_main_code(
            self, node_group, function_name, group_base_name,
            top_frames, frame_interfaces, frame_members, all_framed,
            scope_names=scope_names,
            group_name_override=group_name_override,
            parent_interface=parent_interface,
        )
        self.generated_files[f"{file_prefix}main.py"] = main_code

    # =====================================================================
    # Output
    # =====================================================================

    def _build_header(self, for_main=False, sub_imports=None):
        header = []
        header.append("import bpy")
        header.append("from mathutils import Vector, Color, Matrix, Euler")
        header.append(
            "from procedural_human.decorators.geo_node_decorator import geo_node_group"
        )
        header.append(
            "from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group"
        )

        if self.used_helpers:
            helpers = sorted(self.used_helpers)
            header.append(
                f"from procedural_human.geo_node_groups.node_helpers import {', '.join(helpers)}"
            )

        header.append(
            "from procedural_human.utils.node_layout import auto_layout_nodes"
        )

        for module, func_name in self.used_group_imports:
            header.append(f"from {module} import {func_name}")

        if sub_imports:
            for mod, func in sub_imports:
                header.append(f"from {mod} import {func}")

        header.append("")
        return "\n".join(header)

    def get_full_code(self):
        header = self._build_header()
        return header + "\n\n" + "\n\n".join(self.generated_code_blocks)

    def get_files(self, package_name=None):
        """Get all generated files as a dict of {filepath: code_string}.

        For split_frames, returns multiple files including nested directories.
        Otherwise returns a single file.
        """
        if not self.generated_files:
            return {"output.py": self.get_full_code()}

        result = {}
        group_base = package_name or "output"

        def _is_main(filepath):
            return filepath == "main.py" or filepath.endswith("/main.py")

        def _resolve_sub_imports(filepath, code):
            sub_imports = []
            func_calls = re.findall(r"(create_\w+_group)\(\)", code)
            for func_name in func_calls:
                for other_file, other_code in self.generated_files.items():
                    if other_file == filepath:
                        continue
                    if f"def {func_name}()" in other_code:
                        mod = other_file.replace(".py", "").replace("/", ".").replace("\\", ".")
                        imp = (f"procedural_human.tmp.{group_base}.{mod}", func_name)
                        if imp not in sub_imports:
                            sub_imports.append(imp)
            return sub_imports

        def _build_leaf_header(code):
            per_file_helpers = set()
            for helper_name in self.used_helpers:
                if helper_name in code:
                    per_file_helpers.add(helper_name)

            h_lines = []
            h_lines.append("import bpy")
            h_lines.append("from mathutils import Vector, Color, Matrix, Euler")
            h_lines.append(
                "from procedural_human.decorators.geo_node_decorator import geo_node_group"
            )
            h_lines.append(
                "from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group"
            )
            if per_file_helpers:
                h_lines.append(
                    f"from procedural_human.geo_node_groups.node_helpers import {', '.join(sorted(per_file_helpers))}"
                )
            h_lines.append(
                "from procedural_human.utils.node_layout import auto_layout_nodes"
            )
            for module, func_name in self.used_group_imports:
                if func_name in code:
                    h_lines.append(f"from {module} import {func_name}")
            h_lines.append("")
            return "\n".join(h_lines)

        for filepath, code in self.generated_files.items():
            if _is_main(filepath):
                sub_imports = _resolve_sub_imports(filepath, code)
                header = self._build_header(for_main=True, sub_imports=sub_imports)
                result[filepath] = header + "\n\n" + code
            else:
                header = _build_leaf_header(code)
                result[filepath] = header + "\n\n" + code

        return result
