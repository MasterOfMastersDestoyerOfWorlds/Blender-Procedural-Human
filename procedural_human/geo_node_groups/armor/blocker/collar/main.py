import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.geo_node_groups.node_helpers import combine_xyz, compare_op, create_float_curve, math_op, separate_xyz, vec_math_op
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.tmp.blocker.collar.gambeson_pattern.main import create_blocker_collar_gambeson_pattern_group
from procedural_human.tmp.blocker.collar.thickness import create_blocker_collar_thickness_group
from procedural_human.tmp.blocker.collar.u_v_map import create_blocker_collar_u_v_map_group
from procedural_human.tmp.blocker.collar.general_collar_shape import create_blocker_collar_general_collar_shape_group
from procedural_human.tmp.blocker.collar.displacement import create_blocker_collar_displacement_group


@geo_node_group
def create_blocker_collar_group():
    group_name = "BlockerCollar"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
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

    group_input_001 = nodes.new("NodeGroupInput")

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

    switch_001 = nodes.new("GeometryNodeSwitch")
    links.new(group_input_001.outputs[0], switch_001.inputs[0])

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "POINT"
    links.new(sample_u_v_surface_001.outputs[0], capture_attribute_002.inputs[2])
    links.new(sample_u_v_surface.outputs[0], capture_attribute_002.inputs[1])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    store_named_attribute_001.inputs[1].default_value = True
    store_named_attribute_001.inputs[2].default_value = "skip"
    store_named_attribute_001.inputs[3].default_value = True
    links.new(switch_001.outputs[0], store_named_attribute_001.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.data_type = "FLOAT2"
    store_named_attribute_002.domain = "CORNER"
    store_named_attribute_002.inputs[1].default_value = True
    store_named_attribute_002.inputs[2].default_value = "UVMap"
    links.new(capture_attribute_002.outputs[0], store_named_attribute_002.inputs[0])
    links.new(capture_attribute_002.outputs[3], store_named_attribute_002.inputs[3])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "blocker"
    store_named_attribute.inputs[3].default_value = True
    links.new(store_named_attribute_001.outputs[0], store_named_attribute.inputs[0])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.inputs[1].default_value = True
    links.new(store_named_attribute_002.outputs[0], set_position_003.inputs[0])
    links.new(capture_attribute_002.outputs[1], set_position_003.inputs[2])

    links.new(gambeson_pattern.outputs[0], capture_attribute_002.inputs[0])
    links.new(u_v_map.outputs[1], thickness.inputs[0])
    links.new(capture_attribute_002.outputs[2], thickness.inputs[1])
    links.new(thickness.outputs[0], set_position_003.inputs[3])
    links.new(gambeson_pattern.outputs[0], u_v_map.inputs[0])
    links.new(u_v_map.outputs[0], sample_u_v_surface.inputs[3])
    links.new(u_v_map.outputs[0], sample_u_v_surface_001.inputs[3])
    links.new(u_v_map.outputs[0], capture_attribute_002.inputs[3])
    links.new(general_collar_shape.outputs[0], reroute_001.inputs[0])
    links.new(general_collar_shape.outputs[1], reroute_002.inputs[0])
    links.new(general_collar_shape.outputs[2], switch_001.inputs[1])
    links.new(set_position_003.outputs[0], displacement.inputs[0])
    links.new(capture_attribute_002.outputs[3], displacement.inputs[1])
    links.new(displacement.outputs[0], switch_001.inputs[2])
    links.new(store_named_attribute.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group