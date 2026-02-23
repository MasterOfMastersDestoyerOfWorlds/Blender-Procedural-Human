from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import (
    get_or_rebuild_node_group, link_or_set, separate_xyz, compare_op
)
from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group
from procedural_human.geo_node_groups.utilities.rivet import create_rivet_group
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_neck_trim_group():
    group_name = "NeckTrim"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Selection", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Vector", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    geo_in = group_input.outputs[0]
    uv_in = group_input.outputs[1]

    # Pipe edge selection: UV X ≈ 0.88
    uv_x, _, _ = separate_xyz(group, uv_in)
    pipe_select = compare_op(group, "EQUAL", "FLOAT", uv_x, 0.88)
    pipe_select.node.inputs[12].default_value = 0.021

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.domain = "POINT"
    link_or_set(group, separate_geometry.inputs[0], geo_in)
    link_or_set(group, separate_geometry.inputs[1], pipe_select)
    links.new(separate_geometry.outputs[0], group_output.inputs[0])

    join_for_pipes = nodes.new("GeometryNodeJoinGeometry")
    links.new(separate_geometry.outputs[0], join_for_pipes.inputs[0])
    links.new(geo_in, join_for_pipes.inputs[0])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.node_tree = create_pipes_group()
    link_or_set(group, pipes.inputs[0], join_for_pipes.outputs[0])

    # Rivets
    rivet = nodes.new("GeometryNodeGroup")
    rivet.node_tree = create_rivet_group()
    link_or_set(group, rivet.inputs[0], geo_in)
    rivet.inputs[1].default_value = False
    rivet.inputs[2].default_value = -1.06
    rivet.inputs[3].default_value = 0.94

    realize = nodes.new("GeometryNodeRealizeInstances")
    link_or_set(group, realize.inputs[0], rivet.outputs[0])

    # Join all: mesh + pipes + rivets
    join_all = nodes.new("GeometryNodeJoinGeometry")
    links.new(pipes.outputs[0], join_all.inputs[0])
    links.new(geo_in, join_all.inputs[0])
    links.new(realize.outputs[0], join_all.inputs[0])

    # Trim: delete faces where position.X >= 0
    position = nodes.new("GeometryNodeInputPosition")
    pos_x, _, _ = separate_xyz(group, position.outputs[0])
    trim_select = compare_op(group, "GREATER_EQUAL", "FLOAT", pos_x, 0.0)
    trim_select.node.inputs[12].default_value = 0.001

    delete_geo = nodes.new("GeometryNodeDeleteGeometry")
    delete_geo.mode = "ALL"
    delete_geo.domain = "FACE"
    link_or_set(group, delete_geo.inputs[0], join_all.outputs[0])
    link_or_set(group, delete_geo.inputs[1], trim_select)

    smooth = nodes.new("GeometryNodeSetShadeSmooth")
    smooth.domain = "FACE"
    link_or_set(group, smooth.inputs[0], delete_geo.outputs[0])
    links.new(smooth.outputs[0], group_output.inputs[1])

    frame = nodes.new("NodeFrame")
    frame.label = "Pipes"
    frame.shrink = True
    frame.label_size = 20
    pipes.parent = frame
    uv_x.node.parent = frame
    pipe_select.node.parent = frame
    separate_geometry.parent = frame
    join_for_pipes.parent = frame

    auto_layout_nodes(group)
    return group
