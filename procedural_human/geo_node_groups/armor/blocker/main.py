import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.geo_node_groups.node_helpers import combine_xyz, compare_op, create_float_curve, math_op, separate_xyz, vec_math_op
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.tmp.blocker.chest import create_blocker_chest_group
from procedural_human.tmp.blocker.collar.main import create_blocker_collar_group


@geo_node_group
def create_blocker_group():
    group_name = "Blocker"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    nodes = group.nodes
    links = group.links
    chest = nodes.new("GeometryNodeGroup")
    chest.node_tree = create_blocker_chest_group()

    collar = nodes.new("GeometryNodeGroup")
    collar.node_tree = create_blocker_collar_group()

    join_geometry = nodes.new("GeometryNodeJoinGeometry")

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.domain = "FACE"
    set_shade_smooth.inputs[1].default_value = True
    set_shade_smooth.inputs[2].default_value = True
    links.new(join_geometry.outputs[0], set_shade_smooth.inputs[0])

    group_output = nodes.new("NodeGroupOutput")
    links.new(set_shade_smooth.outputs[0], group_output.inputs[0])

    links.new(chest.outputs[0], join_geometry.inputs[0])
    links.new(collar.outputs[0], join_geometry.inputs[0])

    auto_layout_nodes(group)
    return group