import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.geo_node_groups.node_helpers import math_op, separate_xyz, vec_math_op
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_blocker_collar_thickness_group():
    group_name = "BlockerCollarThickness"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Vector", in_out="OUTPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Vector", in_out="INPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Vector", in_out="INPUT", socket_type="NodeSocketVector")

    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    _, _, separate_x_y_z_003_z = separate_xyz(group, [0.0, 0.0, 0.0])

    math_005 = math_op(group, "MULTIPLY", separate_x_y_z_003_z, 1.2499998807907104)
    math_005.node.inputs[2].default_value = 0.5

    vector_math_004 = vec_math_op(group, "SCALE", [0.0, 0.0, 0.0], math_005)
    vector_math_004.node.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_004.node.inputs[2].default_value = [0.0, 0.0, 0.0]

    links.new(group_input.outputs[0], separate_x_y_z_003.inputs[0])
    links.new(group_input.outputs[1], vector_math_004.inputs[0])
    links.new(vector_math_004, group_output.inputs[0])

    auto_layout_nodes(group)
    return group