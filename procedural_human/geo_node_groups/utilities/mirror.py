import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group

@geo_node_group
def create_mirror_group():
    group_name = "Mirror"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Skip", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.inputs[1].default_value = "Components"
    transform_geometry.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.inputs[1].default_value = True
    links.new(transform_geometry.outputs[0], flip_faces.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    links.new(flip_faces.outputs[0], join_geometry_005.inputs[0])

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.inputs[2].default_value = "All"
    merge_by_distance.inputs[3].default_value = 0.0010000000474974513

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    links.new(is_edge_boundary.outputs[0], merge_by_distance.inputs[1])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.data_type = "BOOLEAN"
    named_attribute.inputs[0].default_value = "gold"

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.domain = "FACE"
    links.new(separate_geometry.outputs[0], merge_by_distance.inputs[0])
    links.new(join_geometry_005.outputs[0], separate_geometry.inputs[0])
    links.new(named_attribute.outputs[0], separate_geometry.inputs[1])

    merge_by_distance_001 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_001.inputs[2].default_value = "All"
    merge_by_distance_001.inputs[3].default_value = 0.0010000000474974513
    links.new(is_edge_boundary.outputs[0], merge_by_distance_001.inputs[1])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    links.new(merge_by_distance_001.outputs[0], join_geometry.inputs[0])
    links.new(merge_by_distance.outputs[0], join_geometry.inputs[0])
    links.new(join_geometry.outputs[0], group_output.inputs[0])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.domain = "FACE"
    links.new(separate_geometry_001.outputs[0], merge_by_distance_001.inputs[0])
    links.new(separate_geometry.outputs[1], separate_geometry_001.inputs[0])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.data_type = "BOOLEAN"
    named_attribute_001.inputs[0].default_value = "fabric"
    links.new(named_attribute_001.outputs[0], separate_geometry_001.inputs[1])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.domain = "FACE"
    links.new(separate_geometry_001.outputs[1], separate_geometry_002.inputs[0])

    named_attribute_002 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.data_type = "BOOLEAN"
    named_attribute_002.inputs[0].default_value = "ruby"
    links.new(named_attribute_002.outputs[0], separate_geometry_002.inputs[1])

    separate_geometry_003 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_003.domain = "FACE"
    links.new(separate_geometry_002.outputs[1], separate_geometry_003.inputs[0])

    named_attribute_003 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003.data_type = "BOOLEAN"
    named_attribute_003.inputs[0].default_value = "saphire"
    links.new(named_attribute_003.outputs[0], separate_geometry_003.inputs[1])

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.inputs[2].default_value = "All"
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    links.new(is_edge_boundary.outputs[0], merge_by_distance_002.inputs[1])
    links.new(separate_geometry_002.outputs[0], merge_by_distance_002.inputs[0])
    links.new(merge_by_distance_002.outputs[0], join_geometry.inputs[0])

    merge_by_distance_003 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_003.inputs[2].default_value = "All"
    merge_by_distance_003.inputs[3].default_value = 0.0010000000474974513
    links.new(is_edge_boundary.outputs[0], merge_by_distance_003.inputs[1])
    links.new(separate_geometry_003.outputs[0], merge_by_distance_003.inputs[0])
    links.new(merge_by_distance_003.outputs[0], join_geometry.inputs[0])

    merge_by_distance_004 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_004.inputs[2].default_value = "All"
    merge_by_distance_004.inputs[3].default_value = 0.0010000000474974513
    links.new(is_edge_boundary.outputs[0], merge_by_distance_004.inputs[1])
    links.new(merge_by_distance_004.outputs[0], join_geometry.inputs[0])

    separate_geometry_004 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_004.domain = "FACE"
    links.new(separate_geometry_004.outputs[0], merge_by_distance_004.inputs[0])
    links.new(separate_geometry_003.outputs[1], separate_geometry_004.inputs[0])

    named_attribute_004 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_004.data_type = "BOOLEAN"
    named_attribute_004.inputs[0].default_value = "blocker"
    links.new(named_attribute_004.outputs[0], separate_geometry_004.inputs[1])

    merge_by_distance_005 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_005.inputs[2].default_value = "All"
    merge_by_distance_005.inputs[3].default_value = 0.0010000000474974513
    links.new(is_edge_boundary.outputs[0], merge_by_distance_005.inputs[1])
    links.new(separate_geometry_004.outputs[1], merge_by_distance_005.inputs[0])
    links.new(merge_by_distance_005.outputs[0], join_geometry.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.socket_idname = "NodeSocketGeometry"
    links.new(reroute.outputs[0], transform_geometry.inputs[0])
    links.new(reroute.outputs[0], join_geometry_005.inputs[0])

    separate_geometry_005 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_005.domain = "POINT"
    links.new(group_input.outputs[0], separate_geometry_005.inputs[0])
    links.new(group_input.outputs[1], separate_geometry_005.inputs[1])
    links.new(separate_geometry_005.outputs[1], reroute.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketGeometry"
    links.new(separate_geometry_005.outputs[0], reroute_001.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.socket_idname = "NodeSocketGeometry"
    links.new(reroute_002.outputs[0], join_geometry.inputs[0])
    links.new(reroute_001.outputs[0], reroute_002.inputs[0])

    auto_layout_nodes(group)
    return group
