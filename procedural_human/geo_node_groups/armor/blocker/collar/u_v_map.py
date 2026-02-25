import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_blocker_collar_u_v_map_group():
    group_name = "BlockerCollarUVMap"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Vector", in_out="OUTPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Position", in_out="OUTPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.inputs[1].default_value = False

    position_006 = nodes.new("GeometryNodeInputPosition")

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT_VECTOR"
    map_range_001.inputs[0].default_value = 1.0
    map_range_001.inputs[1].default_value = 0.0
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[3].default_value = 0.0
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[9].default_value = [0.009999999776482582, 0.009999999776482582, 0.009999999776482582]
    map_range_001.inputs[10].default_value = [0.9900000095367432, 0.9900000095367432, 0.9900000095367432]
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(position_006.outputs[0], map_range_001.inputs[6])
    links.new(bounding_box.outputs[1], map_range_001.inputs[7])
    links.new(bounding_box.outputs[2], map_range_001.inputs[8])

    links.new(group_input.outputs[0], bounding_box.inputs[0])
    links.new(map_range_001.outputs[1], group_output.inputs[0])
    links.new(position_006.outputs[0], group_output.inputs[1])

    auto_layout_nodes(group)
    return group