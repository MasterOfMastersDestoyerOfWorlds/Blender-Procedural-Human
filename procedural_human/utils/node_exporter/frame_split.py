from dataclasses import dataclass, field
from collections import defaultdict

from procedural_human.utils.node_exporter.utils import (
    SOCKET_TYPE_MAP, clean_string, to_snake_case, get_unique_var_name,
    to_python_repr, socket_index, resolve_socket_key, SKIP_VALUE_TYPES,
)


@dataclass
class FrameInterface:
    """Cross-boundary interface for a frame being split into a sub-group."""
    inputs: list = field(default_factory=list)
    outputs: list = field(default_factory=list)
    input_map: dict = field(default_factory=dict)
    output_map: dict = field(default_factory=dict)
    inbound_links: list = field(default_factory=list)
    outbound_links: list = field(default_factory=list)


def collect_frame_descendants(frame, all_nodes):
    """Collect all nodes that are descendants of a frame."""
    members = set()
    members.add(frame.name)
    for node in all_nodes:
        if node == frame:
            continue
        ancestor = node.parent
        while ancestor is not None:
            if ancestor == frame:
                members.add(node.name)
                break
            ancestor = ancestor.parent
    return members


def analyze_frame_interface(frame, members, node_group):
    """Determine the input/output interface of a frame by scanning cross-boundary links."""
    interface = FrameInterface()
    seen_inputs = {}
    seen_outputs = {}

    for link in node_group.links:
        if not link.is_valid:
            continue
        from_in = link.from_node.name in members
        to_in = link.to_node.name in members

        if not from_in and to_in:
            from_idx = socket_index(link.from_socket, link.from_node.outputs)
            source_key = (link.from_node.name, from_idx)
            if source_key not in seen_inputs:
                idx = len(interface.inputs)
                sock_type = SOCKET_TYPE_MAP.get(link.from_socket.type, 'NodeSocketFloat')
                name = link.to_socket.name or f"Input_{idx}"
                interface.inputs.append((name, sock_type))
                seen_inputs[source_key] = idx

            gi_idx = seen_inputs[source_key]
            to_idx = socket_index(link.to_socket, link.to_node.inputs)
            interface.input_map[(link.to_node.name, to_idx)] = (gi_idx, link.to_node.name, to_idx)
            interface.inbound_links.append((link.from_node.name, from_idx, gi_idx))

        elif from_in and not to_in:
            from_idx = socket_index(link.from_socket, link.from_node.outputs)
            source_key = (link.from_node.name, from_idx)
            if source_key not in seen_outputs:
                idx = len(interface.outputs)
                sock_type = SOCKET_TYPE_MAP.get(link.from_socket.type, 'NodeSocketFloat')
                name = link.from_socket.name or f"Output_{idx}"
                interface.outputs.append((name, sock_type))
                seen_outputs[source_key] = idx

            go_idx = seen_outputs[source_key]
            to_idx = socket_index(link.to_socket, link.to_node.inputs)
            interface.output_map[(link.from_node.name, from_idx)] = (
                link.from_node.name, from_idx, go_idx
            )
            interface.outbound_links.append((go_idx, link.to_node.name, to_idx))

    return interface


def generate_main_code(exporter, node_group, function_name, group_base_name,
                       top_frames, frame_interfaces, frame_members, all_framed):
    """Generate the main.py composition function for frame-split exports."""
    opts = exporter.options
    unframed_nodes = [
        n for n in node_group.nodes if n.name not in all_framed
    ]
    all_main_names = {n.name for n in unframed_nodes}

    input_link_map = exporter._build_input_link_map(node_group.links)

    node_var_map = {}
    existing_var_names = set()
    frame_var_map = {}

    for node in unframed_nodes:
        base_name = node.name
        if hasattr(node, "node_tree") and node.node_tree:
            base_name = node.node_tree.name
        var = get_unique_var_name(base_name, existing_var_names)
        existing_var_names.add(var)
        node_var_map[node.name] = var

    for frame in top_frames:
        frame_label = frame.label or frame.name
        var = get_unique_var_name(frame_label, existing_var_names)
        existing_var_names.add(var)
        frame_var_map[frame.name] = var

    output_expr_map = {}
    consumed_sockets = set()

    for node in unframed_nodes:
        var = node_var_map[node.name]
        meta = exporter.helper_registry.get(node.bl_idname) if opts.use_helpers else None
        if meta:
            outputs = meta.resolve_outputs(node)
            for out_key, suffix in outputs.items():
                out_idx = resolve_socket_key(out_key, node.outputs)
                if suffix is None:
                    output_expr_map[(node.name, out_idx)] = var
                else:
                    output_expr_map[(node.name, out_idx)] = f"{var}{suffix}"
            for inp_key in meta.resolve_inputs(node):
                idx = resolve_socket_key(inp_key, node.inputs)
                if idx is not None and idx < len(node.inputs):
                    consumed_sockets.add((node.name, idx))
        else:
            for i in range(len(node.outputs)):
                output_expr_map[(node.name, i)] = f"{var}.outputs[{i}]"

    for frame in top_frames:
        interface = frame_interfaces[frame.name]
        fvar = frame_var_map[frame.name]
        for i, (name, stype) in enumerate(interface.outputs):
            output_expr_map[(f"__frame_{frame.name}", i)] = f"{fvar}.outputs[{i}]"

    lines = []
    lines.append("@geo_node_group")
    lines.append(f"def {function_name}():")
    lines.append(f'    group_name = "{node_group.name}"')
    lines.append(f"    group, needs_rebuild = get_or_rebuild_node_group(group_name)")
    lines.append(f"    if not needs_rebuild:")
    lines.append(f"        return group")
    lines.append("")

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

    for frame in top_frames:
        fvar = frame_var_map[frame.name]
        frame_label = frame.label or frame.name
        frame_snake = to_snake_case(clean_string(frame_label))
        sub_func = f"create_{group_base_name}_{frame_snake}_group"
        lines.append(f'    {fvar} = nodes.new("GeometryNodeGroup")')
        lines.append(f"    {fvar}.node_tree = {sub_func}()")
        lines.append("")

    sorted_unframed = exporter._topological_sort(
        unframed_nodes, node_group.links, all_main_names
    )

    node_helper_meta_main = {}
    used_output_main = defaultdict(set)
    for link in node_group.links:
        if link.is_valid and link.from_node.name in all_main_names:
            from_idx = socket_index(link.from_socket, link.from_node.outputs)
            used_output_main[link.from_node.name].add(from_idx)

    processed = set()
    for node in sorted_unframed:
        var = node_var_map[node.name]
        meta = exporter.helper_registry.get(node.bl_idname) if opts.use_helpers else None
        if meta:
            node_helper_meta_main[node.name] = meta
            exporter._emit_helper_node(
                lines, node, var, meta,
                input_link_map, output_expr_map, node_var_map,
                all_main_names, used_output_main, node_group
            )
        else:
            node_helper_meta_main[node.name] = None
            exporter._emit_raw_node(
                lines, node, var, node_group, consumed_sockets, input_link_map
            )

        processed.add(node.name)
        _emit_interleaved_links(
            lines, node, processed, node_group.links,
            all_main_names, consumed_sockets, output_expr_map, node_var_map
        )
        lines.append("")

    # Links between unframed nodes and frame sub-groups
    for frame in top_frames:
        interface = frame_interfaces[frame.name]
        fvar = frame_var_map[frame.name]

        seen_inbound = set()
        for from_node_name, from_idx, gi_idx in interface.inbound_links:
            key = (from_node_name, from_idx, gi_idx)
            if key in seen_inbound:
                continue
            seen_inbound.add(key)
            if from_node_name in node_var_map:
                from_expr = output_expr_map.get(
                    (from_node_name, from_idx),
                    f"{node_var_map[from_node_name]}.outputs[{from_idx}]"
                )
                lines.append(f"    links.new({from_expr}, {fvar}.inputs[{gi_idx}])")
            elif from_node_name in all_framed:
                for other_frame in top_frames:
                    other_iface = frame_interfaces[other_frame.name]
                    for sock_id, (fn, fi, go_idx) in other_iface.output_map.items():
                        if fn == from_node_name and fi == from_idx:
                            other_fvar = frame_var_map[other_frame.name]
                            lines.append(
                                f"    links.new({other_fvar}.outputs[{go_idx}], {fvar}.inputs[{gi_idx}])"
                            )

        seen_outbound = set()
        for go_idx, to_node_name, to_idx in interface.outbound_links:
            key = (go_idx, to_node_name, to_idx)
            if key in seen_outbound:
                continue
            seen_outbound.add(key)
            if to_node_name in node_var_map:
                lines.append(
                    f"    links.new({fvar}.outputs[{go_idx}], {node_var_map[to_node_name]}.inputs[{to_idx}])"
                )

    lines.append("")
    lines.append("    auto_layout_nodes(group)")
    lines.append("    return group")

    return "\n".join(lines)


def _emit_interleaved_links(lines, current_node, processed, all_links,
                            all_node_names, consumed_sockets,
                            output_expr_map, node_var_map):
    """Emit links where current_node is one end and the other end is already processed."""
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

        other = None
        if link.from_node == current_node and to_name in processed:
            other = link.to_node
        elif link.to_node == current_node and from_name in processed:
            other = link.from_node

        if other is None:
            continue

        from_idx = socket_index(link.from_socket, link.from_node.outputs)

        from_expr = output_expr_map.get(
            (from_name, from_idx),
            f"{node_var_map[from_name]}.outputs[{from_idx}]"
        )
        lines.append(
            f"    links.new({from_expr}, {node_var_map[to_name]}.inputs[{to_idx}])"
        )
