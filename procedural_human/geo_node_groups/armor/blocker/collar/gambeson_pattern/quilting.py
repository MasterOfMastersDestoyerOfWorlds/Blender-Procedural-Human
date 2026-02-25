import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.geo_node_groups.node_helpers import combine_xyz, math_op
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_blocker_collar_gambeson_pattern_quilting_group():
    group_name = "BlockerCollarGambesonPatternQuilting"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Distance", in_out="OUTPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.target_element = "EDGES"
    geometry_proximity.inputs[1].default_value = 0
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity.inputs[3].default_value = 0

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    map_range.inputs[1].default_value = 0.0
    map_range.inputs[2].default_value = 0.009999999776482582
    map_range.inputs[3].default_value = 1.0
    map_range.inputs[4].default_value = 0.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(geometry_proximity.outputs[1], map_range.inputs[0])

    math_002 = math_op(group, "POWER", map_range.outputs[0], 2.0)
    math_002.node.inputs[2].default_value = 0.5

    math_004 = math_op(group, "SUBTRACT", 1.0, math_002)
    math_004.node.inputs[2].default_value = 0.5

    math_003 = math_op(group, "MULTIPLY", math_004, 0.0020000000949949026)
    math_003.node.inputs[2].default_value = 0.5

    combine_x_y_z = combine_xyz(group, 0.0, 0.0, math_003)

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.inputs[1].default_value = True
    set_position_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(combine_x_y_z, set_position_002.inputs[3])

    links.new(group_input.outputs[0], set_position_002.inputs[0])
    links.new(group_input.outputs[1], geometry_proximity.inputs[0])
    links.new(set_position_002.outputs[0], group_output.inputs[0])
    links.new(geometry_proximity.outputs[1], group_output.inputs[1])

    auto_layout_nodes(group)
    return group