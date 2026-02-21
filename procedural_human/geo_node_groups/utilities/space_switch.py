import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group

@geo_node_group
def create_space_res_switch_group():
    group_name = "Space / Res Switch"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Output", in_out="OUTPUT", socket_type="NodeSocketInt")
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Menu", in_out="INPUT", socket_type="NodeSocketMenu")
    socket = group.interface.new_socket(name="Spacing", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Resolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")

    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    menu_switch_001 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_001.active_index = 1
    menu_switch_001.data_type = "INT"
    links.new(group_input.outputs[0], menu_switch_001.inputs[0])
    links.new(group_input.outputs[1], menu_switch_001.inputs[1])
    links.new(group_input.outputs[2], menu_switch_001.inputs[2])
    links.new(menu_switch_001.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
