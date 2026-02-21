import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group

@geo_node_group
def create_rivet_group():
    group_name = "Rivet"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Corners", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False
    socket = group.interface.new_socket(name="Offset", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.9399999976158142
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Spacing", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.9399999976158142
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1539.9998779296875, 160.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-820.0, 240.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    capture_attribute_005 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_005.name = "Capture Attribute.005"
    capture_attribute_005.label = ""
    capture_attribute_005.location = (-660.0, 240.0)
    capture_attribute_005.bl_label = "Capture Attribute"
    capture_attribute_005.active_index = 0
    capture_attribute_005.domain = "POINT"
    # Links for capture_attribute_005
    links.new(group_input.outputs[0], capture_attribute_005.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.label = ""
    normal.location = (-660.0, 120.0)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = False
    # Links for normal
    links.new(normal.outputs[0], capture_attribute_005.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (-260.0, 240.0)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Links for mesh_to_curve_001
    links.new(capture_attribute_005.outputs[0], mesh_to_curve_001.inputs[0])

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Group.005"
    is_edge_boundary.label = ""
    is_edge_boundary.location = (-840.0, 60.0)
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    is_edge_boundary.bl_label = "Group"
    # Links for is_edge_boundary

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (700.0, 320.0)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Position
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (340.0, 40.0)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "NORMALIZE"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (500.0, 40.0)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], set_position.inputs[3])
    links.new(vector_math_001.outputs[0], vector_math_002.inputs[0])

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.label = ""
    vector_math_007.location = (180.0, 40.0)
    vector_math_007.bl_label = "Vector Math"
    vector_math_007.operation = "CROSS_PRODUCT"
    # Vector
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_007.inputs[3].default_value = 1.0
    # Links for vector_math_007
    links.new(vector_math_007.outputs[0], vector_math_001.inputs[0])
    links.new(capture_attribute_005.outputs[1], vector_math_007.inputs[0])

    curve_tangent_002 = nodes.new("GeometryNodeInputTangent")
    curve_tangent_002.name = "Curve Tangent.002"
    curve_tangent_002.label = ""
    curve_tangent_002.location = (-160.0, -200.0)
    curve_tangent_002.bl_label = "Curve Tangent"
    # Links for curve_tangent_002

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (520.0, 320.0)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Length"
    # Count
    resample_curve_001.inputs[3].default_value = 59
    # Links for resample_curve_001
    links.new(resample_curve_001.outputs[0], set_position.inputs[0])
    links.new(mesh_to_curve_001.outputs[0], resample_curve_001.inputs[0])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.label = ""
    instance_on_points_001.location = (1180.0, 380.0)
    instance_on_points_001.bl_label = "Instance on Points"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Rotation
    instance_on_points_001.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_001.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_001

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    ico_sphere.label = ""
    ico_sphere.location = (1180.0, 280.0)
    ico_sphere.bl_label = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.0010000000474974513
    # Subdivisions
    ico_sphere.inputs[1].default_value = 3
    # Links for ico_sphere
    links.new(ico_sphere.outputs[0], instance_on_points_001.inputs[2])

    vertex_neighbors = nodes.new("GeometryNodeInputMeshVertexNeighbors")
    vertex_neighbors.name = "Vertex Neighbors"
    vertex_neighbors.label = ""
    vertex_neighbors.location = (-1160.0, -100.0)
    vertex_neighbors.bl_label = "Vertex Neighbors"
    # Links for vertex_neighbors

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (-1000.0, -100.0)
    compare_003.bl_label = "Compare"
    compare_003.operation = "EQUAL"
    compare_003.data_type = "INT"
    compare_003.mode = "ELEMENT"
    # A
    compare_003.inputs[0].default_value = 0.0
    # B
    compare_003.inputs[1].default_value = 0.0
    # B
    compare_003.inputs[3].default_value = 2
    # A
    compare_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_003.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_003.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_003.inputs[8].default_value = ""
    # B
    compare_003.inputs[9].default_value = ""
    # C
    compare_003.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_003.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_003.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_003
    links.new(vertex_neighbors.outputs[1], compare_003.inputs[2])

    evaluate_on_domain = nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.name = "Evaluate on Domain"
    evaluate_on_domain.label = ""
    evaluate_on_domain.location = (-840.0, -100.0)
    evaluate_on_domain.bl_label = "Evaluate on Domain"
    evaluate_on_domain.domain = "POINT"
    evaluate_on_domain.data_type = "BOOLEAN"
    # Links for evaluate_on_domain
    links.new(compare_003.outputs[0], evaluate_on_domain.inputs[0])

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.label = ""
    boolean_math_003.location = (-480.0, -60.0)
    boolean_math_003.bl_label = "Boolean Math"
    boolean_math_003.operation = "AND"
    # Links for boolean_math_003
    links.new(boolean_math_003.outputs[0], mesh_to_curve_001.inputs[1])
    links.new(is_edge_boundary.outputs[0], boolean_math_003.inputs[0])

    curve_of_point = nodes.new("GeometryNodeCurveOfPoint")
    curve_of_point.name = "Curve of Point"
    curve_of_point.label = ""
    curve_of_point.location = (-460.0, -340.0)
    curve_of_point.bl_label = "Curve of Point"
    # Point Index
    curve_of_point.inputs[0].default_value = 0
    # Links for curve_of_point

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (-140.0, -340.0)
    compare_004.bl_label = "Compare"
    compare_004.operation = "GREATER_EQUAL"
    compare_004.data_type = "INT"
    compare_004.mode = "ELEMENT"
    # A
    compare_004.inputs[0].default_value = 0.0
    # B
    compare_004.inputs[1].default_value = 0.0
    # B
    compare_004.inputs[3].default_value = 1
    # A
    compare_004.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_004.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_004.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_004.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_004.inputs[8].default_value = ""
    # B
    compare_004.inputs[9].default_value = ""
    # C
    compare_004.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_004.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_004.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_004

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.label = ""
    vector_math_008.location = (20.0, -200.0)
    vector_math_008.bl_label = "Vector Math"
    vector_math_008.operation = "SCALE"
    # Vector
    vector_math_008.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_008
    links.new(curve_tangent_002.outputs[0], vector_math_008.inputs[0])
    links.new(vector_math_008.outputs[0], vector_math_007.inputs[1])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (20.0, -340.0)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "INT"
    # False
    switch_001.inputs[1].default_value = 1
    # True
    switch_001.inputs[2].default_value = -1
    # Links for switch_001
    links.new(switch_001.outputs[0], vector_math_008.inputs[3])
    links.new(compare_004.outputs[0], switch_001.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-300.0, -340.0)
    math.bl_label = "Math"
    math.operation = "FLOORED_MODULO"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 2.0
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(curve_of_point.outputs[0], math.inputs[0])
    links.new(math.outputs[0], compare_004.inputs[2])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (500.0, -100.0)
    math_001.bl_label = "Math"
    math_001.operation = "MULTIPLY"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 0.009999999776482582
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math_001.outputs[0], vector_math_002.inputs[3])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (-660.0, -80.0)
    switch.bl_label = "Switch"
    switch.input_type = "BOOLEAN"
    # False
    switch.inputs[1].default_value = True
    # Links for switch
    links.new(switch.outputs[0], boolean_math_003.inputs[1])
    links.new(group_input.outputs[1], switch.inputs[0])
    links.new(evaluate_on_domain.outputs[0], switch.inputs[2])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (260.0, -120.0)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[2], math_001.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (340.0, 200.0)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 0.009999999776482582
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(math_002.outputs[0], resample_curve_001.inputs[4])
    links.new(group_input_001.outputs[3], math_002.inputs[0])

    group_input_002 = nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.label = ""
    group_input_002.location = (520.0, 560.0)
    group_input_002.bl_label = "Group Input"
    # Links for group_input_002

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (740.0, 560.0)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "FACES"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity
    links.new(group_input_002.outputs[0], geometry_proximity.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1000.0, 380.0)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001
    links.new(set_position_001.outputs[0], instance_on_points_001.inputs[0])
    links.new(set_position.outputs[0], set_position_001.inputs[0])
    links.new(geometry_proximity.outputs[0], set_position_001.inputs[2])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (1340.0, 360.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(realize_instances.outputs[0], group_output.inputs[0])
    links.new(instance_on_points_001.outputs[0], realize_instances.inputs[0])

    auto_layout_nodes(group)
    return group
