import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.geo_node_groups.node_helpers import combine_xyz, compare_op, create_float_curve, curve_circle, math_op, resample_curve, separate_xyz, set_position, store_named_attribute, switch_node, vec_math_op
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.armor.blocker.collar.gambeson_pattern.main import create_blocker_collar_gambeson_pattern_group
from procedural_human.geo_node_groups.armor.blocker.collar.thickness import create_blocker_collar_thickness_group
from procedural_human.geo_node_groups.armor.blocker.collar.u_v_map import create_blocker_collar_u_v_map_group
from procedural_human.geo_node_groups.armor.blocker.collar.general_collar_shape import create_blocker_collar_general_collar_shape_group
from procedural_human.geo_node_groups.armor.blocker.collar.displacement import create_blocker_collar_displacement_group


@geo_node_group
def create_blocker_collar_group():
    group_name = "BlockerCollar"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Switch", in_out="INPUT", socket_type="NodeSocketBool")

    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    gambeson_pattern = nodes.new("GeometryNodeGroup")
    gambeson_pattern.node_tree = create_blocker_collar_gambeson_pattern_group()

    thickness = nodes.new("GeometryNodeGroup")
    thickness.node_tree = create_blocker_collar_thickness_group()

    u_v_map = nodes.new("GeometryNodeGroup")
    u_v_map.node_tree = create_blocker_collar_u_v_map_group()

    general_collar_shape = nodes.new("GeometryNodeGroup")
    general_collar_shape.node_tree = create_blocker_collar_general_collar_shape_group()

    displacement = nodes.new("GeometryNodeGroup")
    displacement.node_tree = create_blocker_collar_displacement_group()

    position_005 = nodes.new("GeometryNodeInputPosition")

    normal_003 = nodes.new("GeometryNodeInputNormal")
    normal_003.legacy_corner_normals = False

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketVector"

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.socket_idname = "NodeSocketGeometry"

    switch_001 = switch_node(group, "GEOMETRY", general_collar_shape.outputs[2], group_input.outputs[0], displacement.outputs[0])

    sample_u_v_surface_001 = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface_001.data_type = "FLOAT_VECTOR"
    links.new(reroute_002.outputs[0], sample_u_v_surface_001.inputs[0])
    links.new(reroute_001.outputs[0], sample_u_v_surface_001.inputs[2])
    links.new(normal_003.outputs[0], sample_u_v_surface_001.inputs[1])

    sample_u_v_surface = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface.data_type = "FLOAT_VECTOR"
    links.new(reroute_002.outputs[0], sample_u_v_surface.inputs[0])
    links.new(reroute_001.outputs[0], sample_u_v_surface.inputs[2])
    links.new(position_005.outputs[0], sample_u_v_surface.inputs[1])

    store_named_attribute_001 = store_named_attribute(group, "BOOLEAN", "POINT", switch_001, True, "skip", True)

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "POINT"
    capture_attribute_002.capture_items.new("VECTOR", "Position")
    capture_attribute_002.capture_items.new("VECTOR", "Normal")
    capture_attribute_002.capture_items.new("VECTOR", "UVMap")
    links.new(sample_u_v_surface_001.outputs[0], capture_attribute_002.inputs[2])
    links.new(sample_u_v_surface.outputs[0], capture_attribute_002.inputs[1])

    store_named_attribute = store_named_attribute(group, "BOOLEAN", "POINT", store_named_attribute_001, True, "blocker", True)

    store_named_attribute_002 = store_named_attribute(group, "FLOAT2", "CORNER", capture_attribute_002.outputs[0], True, "UVMap", capture_attribute_002.outputs[3])

    set_position_003 = set_position(group, store_named_attribute_002, True, capture_attribute_002.outputs[1], thickness.outputs[0])

    links.new(gambeson_pattern.outputs[0], capture_attribute_002.inputs[0])
    links.new(u_v_map.outputs[1], thickness.inputs[0])
    links.new(capture_attribute_002.outputs[2], thickness.inputs[1])
    links.new(gambeson_pattern.outputs[0], u_v_map.inputs[0])
    links.new(u_v_map.outputs[0], sample_u_v_surface.inputs[3])
    links.new(u_v_map.outputs[0], sample_u_v_surface_001.inputs[3])
    links.new(u_v_map.outputs[0], capture_attribute_002.inputs[3])
    links.new(general_collar_shape.outputs[0], reroute_001.inputs[0])
    links.new(general_collar_shape.outputs[1], reroute_002.inputs[0])
    links.new(set_position_003, displacement.inputs[0])
    links.new(capture_attribute_002.outputs[3], displacement.inputs[1])
    links.new(store_named_attribute, group_output.inputs[0])

    auto_layout_nodes(group)
    return group