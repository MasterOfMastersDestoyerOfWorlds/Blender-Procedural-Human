import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group

@geo_node_group
def create_mirror_group():
    group_name = "Mirror"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Skip", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1500.0, 100.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1060.0, 40.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (-520.0, -40.0)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    # Links for transform_geometry

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.name = "Flip Faces"
    flip_faces.label = ""
    flip_faces.location = (-360.0, -40.0)
    flip_faces.bl_label = "Flip Faces"
    # Selection
    flip_faces.inputs[1].default_value = True
    # Links for flip_faces
    links.new(transform_geometry.outputs[0], flip_faces.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (-180.0, 40.0)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(flip_faces.outputs[0], join_geometry_005.inputs[0])

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.label = ""
    merge_by_distance.location = (1020.0, 260.0)
    merge_by_distance.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance.inputs[2].default_value = "All"
    # Distance
    merge_by_distance.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Is Edge Boundary"
    is_edge_boundary.label = ""
    is_edge_boundary.location = (560.0, 260.0)
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    is_edge_boundary.bl_label = "Group"
    # Links for is_edge_boundary
    links.new(is_edge_boundary.outputs[0], merge_by_distance.inputs[1])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (60.0, -20.0)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "BOOLEAN"
    # Name
    named_attribute.inputs[0].default_value = "gold"
    # Links for named_attribute

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (60.0, 120.0)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "FACE"
    # Links for separate_geometry
    links.new(separate_geometry.outputs[0], merge_by_distance.inputs[0])
    links.new(join_geometry_005.outputs[0], separate_geometry.inputs[0])
    links.new(named_attribute.outputs[0], separate_geometry.inputs[1])

    merge_by_distance_001 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_001.name = "Merge by Distance.001"
    merge_by_distance_001.label = ""
    merge_by_distance_001.location = (1020.0, 140.0)
    merge_by_distance_001.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_001.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_001.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_001
    links.new(is_edge_boundary.outputs[0], merge_by_distance_001.inputs[1])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (1260.0, 120.0)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(merge_by_distance_001.outputs[0], join_geometry.inputs[0])
    links.new(merge_by_distance.outputs[0], join_geometry.inputs[0])
    links.new(join_geometry.outputs[0], group_output.inputs[0])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.name = "Separate Geometry.001"
    separate_geometry_001.label = ""
    separate_geometry_001.location = (280.0, 80.0)
    separate_geometry_001.bl_label = "Separate Geometry"
    separate_geometry_001.domain = "FACE"
    # Links for separate_geometry_001
    links.new(separate_geometry_001.outputs[0], merge_by_distance_001.inputs[0])
    links.new(separate_geometry.outputs[1], separate_geometry_001.inputs[0])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.label = ""
    named_attribute_001.location = (280.0, -60.0)
    named_attribute_001.bl_label = "Named Attribute"
    named_attribute_001.data_type = "BOOLEAN"
    # Name
    named_attribute_001.inputs[0].default_value = "fabric"
    # Links for named_attribute_001
    links.new(named_attribute_001.outputs[0], separate_geometry_001.inputs[1])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.name = "Separate Geometry.002"
    separate_geometry_002.label = ""
    separate_geometry_002.location = (460.0, -60.0)
    separate_geometry_002.bl_label = "Separate Geometry"
    separate_geometry_002.domain = "FACE"
    # Links for separate_geometry_002
    links.new(separate_geometry_001.outputs[1], separate_geometry_002.inputs[0])

    named_attribute_002 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.name = "Named Attribute.002"
    named_attribute_002.label = ""
    named_attribute_002.location = (460.0, -200.0)
    named_attribute_002.bl_label = "Named Attribute"
    named_attribute_002.data_type = "BOOLEAN"
    # Name
    named_attribute_002.inputs[0].default_value = "ruby"
    # Links for named_attribute_002
    links.new(named_attribute_002.outputs[0], separate_geometry_002.inputs[1])

    separate_geometry_003 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_003.name = "Separate Geometry.003"
    separate_geometry_003.label = ""
    separate_geometry_003.location = (640.0, -120.0)
    separate_geometry_003.bl_label = "Separate Geometry"
    separate_geometry_003.domain = "FACE"
    # Links for separate_geometry_003
    links.new(separate_geometry_002.outputs[1], separate_geometry_003.inputs[0])

    named_attribute_003 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003.name = "Named Attribute.003"
    named_attribute_003.label = ""
    named_attribute_003.location = (640.0, -260.0)
    named_attribute_003.bl_label = "Named Attribute"
    named_attribute_003.data_type = "BOOLEAN"
    # Name
    named_attribute_003.inputs[0].default_value = "saphire"
    # Links for named_attribute_003
    links.new(named_attribute_003.outputs[0], separate_geometry_003.inputs[1])

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.name = "Merge by Distance.002"
    merge_by_distance_002.label = ""
    merge_by_distance_002.location = (1020.0, 20.0)
    merge_by_distance_002.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_002.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_002
    links.new(is_edge_boundary.outputs[0], merge_by_distance_002.inputs[1])
    links.new(separate_geometry_002.outputs[0], merge_by_distance_002.inputs[0])
    links.new(merge_by_distance_002.outputs[0], join_geometry.inputs[0])

    merge_by_distance_003 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_003.name = "Merge by Distance.003"
    merge_by_distance_003.label = ""
    merge_by_distance_003.location = (1020.0, -100.0)
    merge_by_distance_003.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_003.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_003.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_003
    links.new(is_edge_boundary.outputs[0], merge_by_distance_003.inputs[1])
    links.new(separate_geometry_003.outputs[0], merge_by_distance_003.inputs[0])
    links.new(merge_by_distance_003.outputs[0], join_geometry.inputs[0])

    merge_by_distance_004 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_004.name = "Merge by Distance.004"
    merge_by_distance_004.label = ""
    merge_by_distance_004.location = (1020.0, -220.0)
    merge_by_distance_004.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_004.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_004.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_004
    links.new(is_edge_boundary.outputs[0], merge_by_distance_004.inputs[1])
    links.new(merge_by_distance_004.outputs[0], join_geometry.inputs[0])

    separate_geometry_004 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_004.name = "Separate Geometry.004"
    separate_geometry_004.label = ""
    separate_geometry_004.location = (820.0, -180.0)
    separate_geometry_004.bl_label = "Separate Geometry"
    separate_geometry_004.domain = "FACE"
    # Links for separate_geometry_004
    links.new(separate_geometry_004.outputs[0], merge_by_distance_004.inputs[0])
    links.new(separate_geometry_003.outputs[1], separate_geometry_004.inputs[0])

    named_attribute_004 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_004.name = "Named Attribute.004"
    named_attribute_004.label = ""
    named_attribute_004.location = (820.0, -320.0)
    named_attribute_004.bl_label = "Named Attribute"
    named_attribute_004.data_type = "BOOLEAN"
    # Name
    named_attribute_004.inputs[0].default_value = "blocker"
    # Links for named_attribute_004
    links.new(named_attribute_004.outputs[0], separate_geometry_004.inputs[1])

    merge_by_distance_005 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_005.name = "Merge by Distance.005"
    merge_by_distance_005.label = ""
    merge_by_distance_005.location = (1020.0, -340.0)
    merge_by_distance_005.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_005.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_005.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_005
    links.new(is_edge_boundary.outputs[0], merge_by_distance_005.inputs[1])
    links.new(separate_geometry_004.outputs[1], merge_by_distance_005.inputs[0])
    links.new(merge_by_distance_005.outputs[0], join_geometry.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (-540.0, 0.0)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(reroute.outputs[0], transform_geometry.inputs[0])
    links.new(reroute.outputs[0], join_geometry_005.inputs[0])

    separate_geometry_005 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_005.name = "Separate Geometry.005"
    separate_geometry_005.label = ""
    separate_geometry_005.location = (-820.0, 60.0)
    separate_geometry_005.bl_label = "Separate Geometry"
    separate_geometry_005.domain = "POINT"
    # Links for separate_geometry_005
    links.new(group_input.outputs[0], separate_geometry_005.inputs[0])
    links.new(group_input.outputs[1], separate_geometry_005.inputs[1])
    links.new(separate_geometry_005.outputs[1], reroute.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (480.0, 400.0)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001
    links.new(separate_geometry_005.outputs[0], reroute_001.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (1180.0, 400.0)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], join_geometry.inputs[0])
    links.new(reroute_001.outputs[0], reroute_002.inputs[0])

    auto_layout_nodes(group)
    return group
