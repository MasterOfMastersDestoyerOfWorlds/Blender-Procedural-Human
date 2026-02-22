import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_rotate_on__centre_group():
    group_name = "Rotate on Centre"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Rotation", in_out="INPUT", socket_type="NodeSocketRotation")
    socket.default_value = Euler((0.0, 0.0, 0.0), 'XYZ')

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (655.9169921875, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-636.91650390625, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    transform_geometry_014 = nodes.new("GeometryNodeTransform")
    transform_geometry_014.name = "Transform Geometry.014"
    transform_geometry_014.label = ""
    transform_geometry_014.location = (276.9169921875, 22.100006103515625)
    transform_geometry_014.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_014.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_014.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Scale
    transform_geometry_014.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_014
    links.new(group_input.outputs[1], transform_geometry_014.inputs[3])

    transform_geometry_016 = nodes.new("GeometryNodeTransform")
    transform_geometry_016.name = "Transform Geometry.016"
    transform_geometry_016.label = ""
    transform_geometry_016.location = (116.9169921875, 22.100006103515625)
    transform_geometry_016.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_016.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_016.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_016.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_016
    links.new(transform_geometry_016.outputs[0], transform_geometry_014.inputs[0])
    links.new(group_input.outputs[0], transform_geometry_016.inputs[0])

    transform_geometry_017 = nodes.new("GeometryNodeTransform")
    transform_geometry_017.name = "Transform Geometry.017"
    transform_geometry_017.label = ""
    transform_geometry_017.location = (436.9169921875, 22.100006103515625)
    transform_geometry_017.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_017.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_017.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_017.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_017
    links.new(transform_geometry_014.outputs[0], transform_geometry_017.inputs[0])
    links.new(transform_geometry_017.outputs[0], group_output.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    bounding_box.label = ""
    bounding_box.location = (-363.0830078125, -57.899993896484375)
    bounding_box.bl_label = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = True
    # Links for bounding_box
    links.new(group_input.outputs[0], bounding_box.inputs[0])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.label = ""
    vector_math_008.location = (-43.0830078125, -57.899993896484375)
    vector_math_008.bl_label = "Vector Math"
    vector_math_008.operation = "SCALE"
    # Vector
    vector_math_008.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_008.inputs[3].default_value = -1.0
    # Links for vector_math_008
    links.new(vector_math_008.outputs[0], transform_geometry_016.inputs[2])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (-203.0830078125, -57.899993896484375)
    mix.bl_label = "Mix"
    mix.data_type = "VECTOR"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    # Factor
    mix.inputs[0].default_value = 0.5
    # Factor
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix.inputs[2].default_value = 0.0
    # B
    mix.inputs[3].default_value = 0.0
    # A
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix
    links.new(bounding_box.outputs[1], mix.inputs[4])
    links.new(mix.outputs[1], vector_math_008.inputs[0])
    links.new(bounding_box.outputs[2], mix.inputs[5])
    links.new(mix.outputs[1], transform_geometry_017.inputs[2])

    # Parent assignments

    auto_layout_nodes(group)
    return group

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

    # Parent assignments

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_pipes_group():
    group_name = "Pipes"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Mesh", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (520.0, 60.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-200.0, 80.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (40.0, 60.0)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Links for mesh_to_curve
    links.new(group_input.outputs[0], mesh_to_curve.inputs[0])

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Group.003"
    is_edge_boundary.label = ""
    is_edge_boundary.location = (-380.0, -140.0)
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    is_edge_boundary.bl_label = "Group"
    # Links for is_edge_boundary

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (200.0, 60.0)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_002.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002
    links.new(mesh_to_curve.outputs[0], curve_to_mesh_002.inputs[0])

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (200.0, -80.0)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Resolution
    curve_circle.inputs[0].default_value = 10
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle.inputs[4].default_value = 0.0020000000949949026
    # Links for curve_circle
    links.new(curve_circle.outputs[0], curve_to_mesh_002.inputs[1])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (360.0, 60.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(store_named_attribute.outputs[0], group_output.inputs[0])
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute.inputs[0])

    edge_neighbors = nodes.new("GeometryNodeInputMeshEdgeNeighbors")
    edge_neighbors.name = "Edge Neighbors"
    edge_neighbors.label = ""
    edge_neighbors.location = (-380.0, -240.0)
    edge_neighbors.bl_label = "Edge Neighbors"
    # Links for edge_neighbors

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (-200.0, -100.0)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "OR"
    # Links for boolean_math
    links.new(boolean_math.outputs[0], mesh_to_curve.inputs[1])
    links.new(is_edge_boundary.outputs[0], boolean_math.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (-200.0, -240.0)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    # A
    compare.inputs[0].default_value = 0.0
    # B
    compare.inputs[1].default_value = 0.0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513
    # Links for compare
    links.new(edge_neighbors.outputs[0], compare.inputs[2])
    links.new(compare.outputs[0], boolean_math.inputs[1])

    # Parent assignments

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_gold__wavies_group():
    group_name = "Gold Wavies"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Instances", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1500.0, 300.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.label = ""
    curve_line.location = (-620.0, 220.0)
    curve_line.bl_label = "Curve Line"
    curve_line.mode = "POINTS"
    # Start
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    # End
    curve_line.inputs[1].default_value = Vector((0.009999999776482582, 0.0, 0.0))
    # Direction
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    # Length
    curve_line.inputs[3].default_value = 1.0
    # Links for curve_line

    points_to_vertices = nodes.new("GeometryNodePointsToVertices")
    points_to_vertices.name = "Points to Vertices"
    points_to_vertices.label = ""
    points_to_vertices.location = (-300.0, 220.0)
    points_to_vertices.bl_label = "Points to Vertices"
    # Selection
    points_to_vertices.inputs[1].default_value = True
    # Links for points_to_vertices

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (-460.0, 220.0)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "COUNT"
    # Count
    curve_to_points.inputs[1].default_value = 18
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points
    links.new(curve_to_points.outputs[0], points_to_vertices.inputs[0])
    links.new(curve_line.outputs[0], curve_to_points.inputs[0])

    extrude_mesh_001 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.name = "Extrude Mesh.001"
    extrude_mesh_001.label = ""
    extrude_mesh_001.location = (100.0, 220.0)
    extrude_mesh_001.bl_label = "Extrude Mesh"
    extrude_mesh_001.mode = "VERTICES"
    # Offset Scale
    extrude_mesh_001.inputs[3].default_value = 0.0010000000474974513
    # Individual
    extrude_mesh_001.inputs[4].default_value = True
    # Links for extrude_mesh_001

    repeat_input = nodes.new("GeometryNodeRepeatInput")
    repeat_input.name = "Repeat Input"
    repeat_input.label = ""
    repeat_input.location = (-120.0, 220.0)
    repeat_input.bl_label = "Repeat Input"
    # Iterations
    repeat_input.inputs[0].default_value = 50
    # Top
    repeat_input.inputs[2].default_value = True
    # Links for repeat_input
    links.new(points_to_vertices.outputs[0], repeat_input.inputs[1])
    links.new(repeat_input.outputs[2], extrude_mesh_001.inputs[1])
    links.new(repeat_input.outputs[1], extrude_mesh_001.inputs[0])

    repeat_output = nodes.new("GeometryNodeRepeatOutput")
    repeat_output.name = "Repeat Output"
    repeat_output.label = ""
    repeat_output.location = (260.0, 220.0)
    repeat_output.bl_label = "Repeat Output"
    repeat_output.active_index = 1
    repeat_output.inspection_index = 0
    # Links for repeat_output
    links.new(extrude_mesh_001.outputs[1], repeat_output.inputs[1])
    links.new(extrude_mesh_001.outputs[0], repeat_output.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (-300.0, 60.0)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = True
    # Vector
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Scale
    noise_texture.inputs[2].default_value = 104.69999694824219
    # Detail
    noise_texture.inputs[3].default_value = 0.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Offset
    noise_texture.inputs[6].default_value = 0.0
    # Gain
    noise_texture.inputs[7].default_value = 1.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0
    # Links for noise_texture

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (-120.0, 60.0)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT_VECTOR"
    # Value
    map_range.inputs[0].default_value = 1.0
    # From Min
    map_range.inputs[1].default_value = 0.0
    # From Max
    map_range.inputs[2].default_value = 1.0
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0
    # Steps
    map_range.inputs[5].default_value = 4.0
    # From Min
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range.inputs[9].default_value = [-1.0, -1.0, 0.0]
    # To Max
    map_range.inputs[10].default_value = [1.0, 1.0, 0.05000000074505806]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(map_range.outputs[1], extrude_mesh_001.inputs[2])
    links.new(noise_texture.outputs[1], map_range.inputs[6])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (420.0, 220.0)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Selection
    mesh_to_curve_001.inputs[1].default_value = True
    # Links for mesh_to_curve_001
    links.new(repeat_output.outputs[0], mesh_to_curve_001.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (780.0, 200.0)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False
    # Links for curve_to_mesh_001

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (780.0, 60.0)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Resolution
    curve_circle.inputs[0].default_value = 6
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle.inputs[4].default_value = 0.0003000000142492354
    # Links for curve_circle
    links.new(curve_circle.outputs[0], curve_to_mesh_001.inputs[1])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.label = ""
    spline_parameter.location = (420.0, -40.0)
    spline_parameter.bl_label = "Spline Parameter"
    # Links for spline_parameter

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (420.0, 100.0)
    math_004.bl_label = "Math"
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    # Value
    math_004.inputs[0].default_value = 1.0
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(spline_parameter.outputs[0], math_004.inputs[1])
    links.new(math_004.outputs[0], curve_to_mesh_001.inputs[2])

    repeat_input_001 = nodes.new("GeometryNodeRepeatInput")
    repeat_input_001.name = "Repeat Input.001"
    repeat_input_001.label = ""
    repeat_input_001.location = (-1080.0, 360.0)
    repeat_input_001.bl_label = "Repeat Input"
    # Iterations
    repeat_input_001.inputs[0].default_value = 20
    # Links for repeat_input_001

    repeat_output_001 = nodes.new("GeometryNodeRepeatOutput")
    repeat_output_001.name = "Repeat Output.001"
    repeat_output_001.label = ""
    repeat_output_001.location = (1320.0, 300.0)
    repeat_output_001.bl_label = "Repeat Output"
    repeat_output_001.active_index = 0
    repeat_output_001.inspection_index = 19
    # Links for repeat_output_001
    links.new(repeat_output_001.outputs[0], group_output.inputs[0])

    index_switch = nodes.new("GeometryNodeIndexSwitch")
    index_switch.name = "Index Switch"
    index_switch.label = ""
    index_switch.location = (-900.0, 360.0)
    index_switch.bl_label = "Index Switch"
    index_switch.data_type = "FLOAT"
    # 0
    index_switch.inputs[1].default_value = 1.5700000524520874
    # 1
    index_switch.inputs[2].default_value = 0.3499999940395355
    # 2
    index_switch.inputs[3].default_value = 1.0099999904632568
    # 3
    index_switch.inputs[4].default_value = 1.2999999523162842
    # 4
    index_switch.inputs[5].default_value = 1.2999999523162842
    # 5
    index_switch.inputs[6].default_value = 2.569999933242798
    # 6
    index_switch.inputs[7].default_value = 3.6499998569488525
    # 7
    index_switch.inputs[8].default_value = 4.029999732971191
    # 8
    index_switch.inputs[9].default_value = 4.599999904632568
    # 9
    index_switch.inputs[10].default_value = 6.239999771118164
    # 10
    index_switch.inputs[11].default_value = 10.100000381469727
    # 11
    index_switch.inputs[12].default_value = 10.270000457763672
    # 12
    index_switch.inputs[13].default_value = 10.369999885559082
    # 13
    index_switch.inputs[14].default_value = 10.670000076293945
    # 14
    index_switch.inputs[15].default_value = 10.720000267028809
    # 15
    index_switch.inputs[16].default_value = 10.890000343322754
    # 16
    index_switch.inputs[17].default_value = 11.130000114440918
    # 17
    index_switch.inputs[18].default_value = 11.289999961853027
    # 18
    index_switch.inputs[19].default_value = 11.390000343322754
    # 19
    index_switch.inputs[20].default_value = 11.800000190734863
    # Links for index_switch
    links.new(repeat_input_001.outputs[0], index_switch.inputs[0])
    links.new(index_switch.outputs[0], noise_texture.inputs[1])

    geometry_to_instance = nodes.new("GeometryNodeGeometryToInstance")
    geometry_to_instance.name = "Geometry to Instance"
    geometry_to_instance.label = ""
    geometry_to_instance.location = (940.0, 200.0)
    geometry_to_instance.bl_label = "Geometry to Instance"
    # Links for geometry_to_instance
    links.new(curve_to_mesh_001.outputs[0], geometry_to_instance.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.label = ""
    join_geometry_006.location = (1140.0, 300.0)
    join_geometry_006.bl_label = "Join Geometry"
    # Links for join_geometry_006
    links.new(join_geometry_006.outputs[0], repeat_output_001.inputs[0])
    links.new(repeat_input_001.outputs[1], join_geometry_006.inputs[0])
    links.new(geometry_to_instance.outputs[0], join_geometry_006.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (600.0, 200.0)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Count"
    # Count
    resample_curve.inputs[3].default_value = 30
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve
    links.new(resample_curve.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(mesh_to_curve_001.outputs[0], resample_curve.inputs[0])

    # Parent assignments

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_gold__decorations_group():
    group_name = "Gold Decorations"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Curves", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Seed", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 30
    socket.min_value = -10000
    socket.max_value = 10000
    socket = group.interface.new_socket(name="Scale", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 4.049999713897705
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Count", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 18
    socket.min_value = 1
    socket.max_value = 10000

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2080.0, 200.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (280.0, -340.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    mesh_line = nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.label = ""
    mesh_line.location = (-1140.0, 220.0)
    mesh_line.bl_label = "Mesh Line"
    mesh_line.mode = "OFFSET"
    mesh_line.count_mode = "TOTAL"
    # Resolution
    mesh_line.inputs[1].default_value = 1.0
    # Start Location
    mesh_line.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset
    mesh_line.inputs[3].default_value = Vector((0.004999999888241291, 0.0, 0.0))
    # Links for mesh_line

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (-960.0, 220.0)
    instance_on_points.bl_label = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = True
    # Rotation
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points
    links.new(mesh_line.outputs[0], instance_on_points.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (-960.0, -100.0)
    random_value.bl_label = "Random Value"
    random_value.data_type = "INT"
    # Min
    random_value.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value.inputs[2].default_value = 0.0
    # Max
    random_value.inputs[3].default_value = 1.0
    # Min
    random_value.inputs[4].default_value = 0
    # Probability
    random_value.inputs[6].default_value = 0.5
    # ID
    random_value.inputs[7].default_value = 0
    # Links for random_value
    links.new(random_value.outputs[2], instance_on_points.inputs[4])

    scale_instances_001 = nodes.new("GeometryNodeScaleInstances")
    scale_instances_001.name = "Scale Instances.001"
    scale_instances_001.label = ""
    scale_instances_001.location = (-780.0, 160.0)
    scale_instances_001.bl_label = "Scale Instances"
    # Selection
    scale_instances_001.inputs[1].default_value = True
    # Scale
    scale_instances_001.inputs[2].default_value = Vector((1.0, -1.0, 1.0))
    # Center
    scale_instances_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Local Space
    scale_instances_001.inputs[4].default_value = True
    # Links for scale_instances_001
    links.new(instance_on_points.outputs[0], scale_instances_001.inputs[0])

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_008.name = "Join Geometry.008"
    join_geometry_008.label = ""
    join_geometry_008.location = (-440.0, 220.0)
    join_geometry_008.bl_label = "Join Geometry"
    # Links for join_geometry_008
    links.new(instance_on_points.outputs[0], join_geometry_008.inputs[0])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (-260.0, 220.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(join_geometry_008.outputs[0], realize_instances.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.name = "Flip Faces.003"
    flip_faces_003.label = ""
    flip_faces_003.location = (-620.0, 160.0)
    flip_faces_003.bl_label = "Flip Faces"
    # Selection
    flip_faces_003.inputs[1].default_value = True
    # Links for flip_faces_003
    links.new(scale_instances_001.outputs[0], flip_faces_003.inputs[0])
    links.new(flip_faces_003.outputs[0], join_geometry_008.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    bounding_box.label = ""
    bounding_box.location = (-80.0, -80.0)
    bounding_box.bl_label = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = True
    # Links for bounding_box
    links.new(realize_instances.outputs[0], bounding_box.inputs[0])

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.label = ""
    sample_curve.location = (480.0, -80.0)
    sample_curve.bl_label = "Sample Curve"
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = True
    sample_curve.data_type = "FLOAT"
    # Value
    sample_curve.inputs[1].default_value = 0.0
    # Length
    sample_curve.inputs[3].default_value = 0.0
    # Curve Index
    sample_curve.inputs[4].default_value = 0
    # Links for sample_curve
    links.new(group_input.outputs[0], sample_curve.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (-80.0, -20.0)
    position_002.bl_label = "Position"
    # Links for position_002

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.label = ""
    map_range_001.location = (100.0, -20.0)
    map_range_001.bl_label = "Map Range"
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT_VECTOR"
    # Value
    map_range_001.inputs[0].default_value = 1.0
    # From Min
    map_range_001.inputs[1].default_value = 0.0
    # From Max
    map_range_001.inputs[2].default_value = 1.0
    # To Min
    map_range_001.inputs[3].default_value = 0.0
    # To Max
    map_range_001.inputs[4].default_value = 1.0
    # Steps
    map_range_001.inputs[5].default_value = 4.0
    # To Min
    map_range_001.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_001.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_001
    links.new(position_002.outputs[0], map_range_001.inputs[6])
    links.new(bounding_box.outputs[1], map_range_001.inputs[7])
    links.new(bounding_box.outputs[2], map_range_001.inputs[8])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_003.name = "Separate XYZ.003"
    separate_x_y_z_003.label = ""
    separate_x_y_z_003.location = (280.0, -20.0)
    separate_x_y_z_003.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_003
    links.new(map_range_001.outputs[1], separate_x_y_z_003.inputs[0])
    links.new(separate_x_y_z_003.outputs[0], sample_curve.inputs[2])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1280.0, 220.0)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001
    links.new(realize_instances.outputs[0], set_position_001.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (900.0, 40.0)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "ADD"
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(sample_curve.outputs[1], vector_math_003.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (720.0, -160.0)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "SCALE"
    # Vector
    vector_math.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math
    links.new(vector_math.outputs[0], vector_math_003.inputs[1])
    links.new(sample_curve.outputs[3], vector_math.inputs[0])

    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_004.name = "Separate XYZ.004"
    separate_x_y_z_004.label = ""
    separate_x_y_z_004.location = (720.0, -440.0)
    separate_x_y_z_004.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_004
    links.new(separate_x_y_z_004.outputs[1], vector_math.inputs[3])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (720.0, -300.0)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "CROSS_PRODUCT"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(sample_curve.outputs[3], vector_math_001.inputs[1])
    links.new(sample_curve.outputs[2], vector_math_001.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (880.0, -300.0)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_002
    links.new(vector_math_001.outputs[0], vector_math_002.inputs[0])
    links.new(separate_x_y_z_004.outputs[2], vector_math_002.inputs[3])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (1080.0, 40.0)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "ADD"
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(vector_math_003.outputs[0], vector_math_004.inputs[0])
    links.new(vector_math_004.outputs[0], set_position_001.inputs[2])
    links.new(vector_math_002.outputs[0], vector_math_004.inputs[1])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (500.0, -380.0)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "SCALE"
    # Vector
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_005
    links.new(vector_math_005.outputs[0], separate_x_y_z_004.inputs[0])
    links.new(position_002.outputs[0], vector_math_005.inputs[0])
    links.new(group_input.outputs[2], vector_math_005.inputs[3])

    gold_wavies = nodes.new("GeometryNodeGroup")
    gold_wavies.name = "Group.002"
    gold_wavies.label = ""
    gold_wavies.location = (-1320.0, 20.0)
    gold_wavies.node_tree = create_gold__wavies_group()
    gold_wavies.bl_label = "Group"
    # Links for gold_wavies
    links.new(gold_wavies.outputs[0], instance_on_points.inputs[2])

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (-1320.0, -40.0)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "INSTANCES"
    # Links for domain_size
    links.new(gold_wavies.outputs[0], domain_size.inputs[0])
    links.new(domain_size.outputs[5], random_value.inputs[5])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (-1160.0, -200.0)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[1], random_value.inputs[8])
    links.new(group_input_001.outputs[3], mesh_line.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (1500.0, 220.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(store_named_attribute.outputs[0], group_output.inputs[0])
    links.new(set_position_001.outputs[0], store_named_attribute.inputs[0])

    # Parent assignments

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_gold_on__band_group():
    group_name = "Gold on Band"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Mesh", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Density", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 1000.0
    socket.min_value = 0.0
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="W", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 1.5699999332427979
    socket.min_value = -1000.0
    socket.max_value = 1000.0
    socket = group.interface.new_socket(name="Seed", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1200.0, 80.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1423.4365234375, -77.9857406616211)
    group_input.bl_label = "Group Input"
    # Links for group_input

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.name = "Distribute Points on Faces"
    distribute_points_on_faces.label = ""
    distribute_points_on_faces.location = (-1203.4364013671875, 102.0142593383789)
    distribute_points_on_faces.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    # Selection
    distribute_points_on_faces.inputs[1].default_value = True
    # Distance Min
    distribute_points_on_faces.inputs[2].default_value = 0.0
    # Density Max
    distribute_points_on_faces.inputs[3].default_value = 10.0
    # Density Factor
    distribute_points_on_faces.inputs[5].default_value = 1.0
    # Links for distribute_points_on_faces
    links.new(group_input.outputs[0], distribute_points_on_faces.inputs[0])
    links.new(group_input.outputs[1], distribute_points_on_faces.inputs[4])
    links.new(group_input.outputs[3], distribute_points_on_faces.inputs[6])

    points_to_vertices = nodes.new("GeometryNodePointsToVertices")
    points_to_vertices.name = "Points to Vertices"
    points_to_vertices.label = ""
    points_to_vertices.location = (-1003.4364624023438, 102.0142593383789)
    points_to_vertices.bl_label = "Points to Vertices"
    # Selection
    points_to_vertices.inputs[1].default_value = True
    # Links for points_to_vertices
    links.new(distribute_points_on_faces.outputs[0], points_to_vertices.inputs[0])

    extrude_mesh_001 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.name = "Extrude Mesh.001"
    extrude_mesh_001.label = ""
    extrude_mesh_001.location = (-483.4364318847656, 102.0142593383789)
    extrude_mesh_001.bl_label = "Extrude Mesh"
    extrude_mesh_001.mode = "VERTICES"
    # Offset Scale
    extrude_mesh_001.inputs[3].default_value = 0.0020000000949949026
    # Individual
    extrude_mesh_001.inputs[4].default_value = True
    # Links for extrude_mesh_001

    repeat_input = nodes.new("GeometryNodeRepeatInput")
    repeat_input.name = "Repeat Input"
    repeat_input.label = ""
    repeat_input.location = (-833.4364624023438, 102.0142593383789)
    repeat_input.bl_label = "Repeat Input"
    # Iterations
    repeat_input.inputs[0].default_value = 100
    # Top
    repeat_input.inputs[2].default_value = True
    # Links for repeat_input
    links.new(repeat_input.outputs[2], extrude_mesh_001.inputs[1])
    links.new(repeat_input.outputs[1], extrude_mesh_001.inputs[0])
    links.new(points_to_vertices.outputs[0], repeat_input.inputs[1])

    repeat_output = nodes.new("GeometryNodeRepeatOutput")
    repeat_output.name = "Repeat Output"
    repeat_output.label = ""
    repeat_output.location = (196.5635528564453, 102.0142593383789)
    repeat_output.bl_label = "Repeat Output"
    repeat_output.active_index = 1
    repeat_output.inspection_index = 0
    # Links for repeat_output
    links.new(extrude_mesh_001.outputs[0], repeat_output.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (-1183.4364013671875, -137.98573303222656)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = True
    # Vector
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Scale
    noise_texture.inputs[2].default_value = 39.5
    # Detail
    noise_texture.inputs[3].default_value = 0.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Offset
    noise_texture.inputs[6].default_value = 0.0
    # Gain
    noise_texture.inputs[7].default_value = 1.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0
    # Links for noise_texture
    links.new(group_input.outputs[2], noise_texture.inputs[1])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (-1003.4364624023438, -137.98573303222656)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT_VECTOR"
    # Value
    map_range.inputs[0].default_value = 1.0
    # From Min
    map_range.inputs[1].default_value = 0.0
    # From Max
    map_range.inputs[2].default_value = 1.0
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0
    # Steps
    map_range.inputs[5].default_value = 4.0
    # From Min
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range.inputs[9].default_value = [-1.0, -1.0, -1.0]
    # To Max
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(noise_texture.outputs[1], map_range.inputs[6])

    mesh_to_curve_002 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.name = "Mesh to Curve.002"
    mesh_to_curve_002.label = ""
    mesh_to_curve_002.location = (440.0, 80.0)
    mesh_to_curve_002.bl_label = "Mesh to Curve"
    mesh_to_curve_002.mode = "EDGES"
    # Selection
    mesh_to_curve_002.inputs[1].default_value = True
    # Links for mesh_to_curve_002
    links.new(repeat_output.outputs[0], mesh_to_curve_002.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (600.0, 80.0)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False
    # Links for curve_to_mesh_001
    links.new(mesh_to_curve_002.outputs[0], curve_to_mesh_001.inputs[0])

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (420.0, -60.0)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Resolution
    curve_circle.inputs[0].default_value = 6
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle.inputs[4].default_value = 0.0010000000474974513
    # Links for curve_circle
    links.new(curve_circle.outputs[0], curve_to_mesh_001.inputs[1])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.label = ""
    spline_parameter.location = (600.0, -200.0)
    spline_parameter.bl_label = "Spline Parameter"
    # Links for spline_parameter

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (600.0, -60.0)
    math_004.bl_label = "Math"
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    # Value
    math_004.inputs[0].default_value = 1.0
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(math_004.outputs[0], curve_to_mesh_001.inputs[2])
    links.new(spline_parameter.outputs[0], math_004.inputs[1])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (-843.4364624023438, -137.98573303222656)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "CROSS_PRODUCT"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(map_range.outputs[1], vector_math.inputs[0])
    links.new(distribute_points_on_faces.outputs[1], vector_math.inputs[1])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (-683.4364624023438, -137.98573303222656)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "NORMALIZE"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(vector_math_001.outputs[0], extrude_mesh_001.inputs[2])
    links.new(vector_math.outputs[0], vector_math_001.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (-203.4364471435547, -117.9857406616211)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "FACES"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (-363.4364318847656, -117.9857406616211)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[0], geometry_proximity.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (-23.43644142150879, -117.9857406616211)
    compare.bl_label = "Compare"
    compare.operation = "LESS_EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.0010000000474974513
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513
    # Links for compare
    links.new(geometry_proximity.outputs[1], compare.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (-23.43644142150879, 22.01426124572754)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "AND"
    # Links for boolean_math
    links.new(boolean_math.outputs[0], repeat_output.inputs[1])
    links.new(extrude_mesh_001.outputs[1], boolean_math.inputs[0])
    links.new(compare.outputs[0], boolean_math.inputs[1])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (780.0, 80.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(store_named_attribute.outputs[0], group_output.inputs[0])
    links.new(curve_to_mesh_001.outputs[0], store_named_attribute.inputs[0])

    # Parent assignments

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_gem_in__holder_group():
    group_name = "Gem in Holder"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Gem Radius", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.009999999776482582
    socket.min_value = 0.0
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Gem Material", in_out="INPUT", socket_type="NodeSocketString")
    socket.default_value = "ruby"
    socket = group.interface.new_socket(name="Gem Dual Mesh", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False
    socket = group.interface.new_socket(name="Profile Curve", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Profile Scale", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Scale", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.004999999888241291
    socket.min_value = 0.0
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Count", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 20
    socket.min_value = 0
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Seed", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 10
    socket.min_value = -10000
    socket.max_value = 10000
    socket = group.interface.new_socket(name="Wings", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False
    socket = group.interface.new_socket(name="Wing", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Wing Curve", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Array Count", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 6
    socket.min_value = 3
    socket.max_value = 512
    socket = group.interface.new_socket(name="Strand Count", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 10
    socket.min_value = 0
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Split", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0020000000949949026
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Seed", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 2.5099997520446777
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2440.0, -400.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (29.0, -135.79998779296875)
    group_input.bl_label = "Group Input"
    # Links for group_input

    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.name = "Ico Sphere.001"
    ico_sphere_001.label = ""
    ico_sphere_001.location = (189.0, -35.79998779296875)
    ico_sphere_001.bl_label = "Ico Sphere"
    # Subdivisions
    ico_sphere_001.inputs[1].default_value = 2
    # Links for ico_sphere_001

    dual_mesh = nodes.new("GeometryNodeDualMesh")
    dual_mesh.name = "Dual Mesh"
    dual_mesh.label = ""
    dual_mesh.location = (349.0, -35.79998779296875)
    dual_mesh.bl_label = "Dual Mesh"
    # Keep Boundaries
    dual_mesh.inputs[1].default_value = False
    # Links for dual_mesh
    links.new(ico_sphere_001.outputs[0], dual_mesh.inputs[0])

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (1289.0, -35.79998779296875)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Resolution
    curve_circle.inputs[0].default_value = 24
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for curve_circle
    links.new(group_input.outputs[0], curve_circle.inputs[4])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (1449.0, -35.79998779296875)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002
    links.new(curve_circle.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(group_input.outputs[3], curve_to_mesh_002.inputs[2])

    points = nodes.new("GeometryNodePoints")
    points.name = "Points"
    points.label = ""
    points.location = (429.0, -195.79998779296875)
    points.bl_label = "Points"
    # Radius
    points.inputs[2].default_value = 0.10000000149011612
    # Links for points
    links.new(group_input.outputs[4], points.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (269.0, -195.79998779296875)
    random_value.bl_label = "Random Value"
    random_value.data_type = "FLOAT_VECTOR"
    # Min
    random_value.inputs[0].default_value = [-0.5, -1.0, 0.0]
    # Max
    random_value.inputs[1].default_value = [0.5, 1.0, 0.0]
    # Min
    random_value.inputs[2].default_value = 0.0
    # Max
    random_value.inputs[3].default_value = 1.0
    # Min
    random_value.inputs[4].default_value = 0
    # Max
    random_value.inputs[5].default_value = 100
    # Probability
    random_value.inputs[6].default_value = 0.5
    # ID
    random_value.inputs[7].default_value = 0
    # Links for random_value
    links.new(random_value.outputs[0], points.inputs[1])
    links.new(group_input.outputs[5], random_value.inputs[8])

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    points_to_curves.label = ""
    points_to_curves.location = (589.0, -195.79998779296875)
    points_to_curves.bl_label = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0
    # Links for points_to_curves
    links.new(points.outputs[0], points_to_curves.inputs[0])

    gradient_texture = nodes.new("ShaderNodeTexGradient")
    gradient_texture.name = "Gradient Texture"
    gradient_texture.label = ""
    gradient_texture.location = (429.0, -335.79998779296875)
    gradient_texture.bl_label = "Gradient Texture"
    gradient_texture.gradient_type = "RADIAL"
    # Vector
    gradient_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Links for gradient_texture
    links.new(gradient_texture.outputs[1], points_to_curves.inputs[2])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    set_spline_cyclic.label = ""
    set_spline_cyclic.location = (749.0, -195.79998779296875)
    set_spline_cyclic.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = True
    # Links for set_spline_cyclic
    links.new(points_to_curves.outputs[0], set_spline_cyclic.inputs[0])

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.label = ""
    set_spline_type.location = (909.0, -195.79998779296875)
    set_spline_type.bl_label = "Set Spline Type"
    set_spline_type.spline_type = "NURBS"
    # Selection
    set_spline_type.inputs[1].default_value = True
    # Links for set_spline_type
    links.new(set_spline_cyclic.outputs[0], set_spline_type.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.label = ""
    transform_geometry_005.location = (689.0, -35.79998779296875)
    transform_geometry_005.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_005.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    # Rotation
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 0.6000000238418579))
    # Links for transform_geometry_005

    points_to_vertices = nodes.new("GeometryNodePointsToVertices")
    points_to_vertices.name = "Points to Vertices"
    points_to_vertices.label = ""
    points_to_vertices.location = (649.0, -215.13333129882812)
    points_to_vertices.bl_label = "Points to Vertices"
    # Selection
    points_to_vertices.inputs[1].default_value = True
    # Links for points_to_vertices

    extrude_mesh_001 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.name = "Extrude Mesh.001"
    extrude_mesh_001.label = ""
    extrude_mesh_001.location = (1769.0, -55.133331298828125)
    extrude_mesh_001.bl_label = "Extrude Mesh"
    extrude_mesh_001.mode = "VERTICES"
    # Offset Scale
    extrude_mesh_001.inputs[3].default_value = 0.0020000000949949026
    # Individual
    extrude_mesh_001.inputs[4].default_value = True
    # Links for extrude_mesh_001

    repeat_input_001 = nodes.new("GeometryNodeRepeatInput")
    repeat_input_001.name = "Repeat Input.001"
    repeat_input_001.label = ""
    repeat_input_001.location = (1589.0, -55.133331298828125)
    repeat_input_001.bl_label = "Repeat Input"
    # Iterations
    repeat_input_001.inputs[0].default_value = 60
    # Top
    repeat_input_001.inputs[2].default_value = True
    # Value
    repeat_input_001.inputs[3].default_value = [0.0, 0.0, 0.0]
    # Links for repeat_input_001
    links.new(repeat_input_001.outputs[2], extrude_mesh_001.inputs[1])
    links.new(repeat_input_001.outputs[1], extrude_mesh_001.inputs[0])
    links.new(points_to_vertices.outputs[0], repeat_input_001.inputs[1])

    repeat_output_001 = nodes.new("GeometryNodeRepeatOutput")
    repeat_output_001.name = "Repeat Output.001"
    repeat_output_001.label = ""
    repeat_output_001.location = (2289.0, -55.133331298828125)
    repeat_output_001.bl_label = "Repeat Output"
    repeat_output_001.active_index = 2
    repeat_output_001.inspection_index = 0
    # Links for repeat_output_001
    links.new(extrude_mesh_001.outputs[1], repeat_output_001.inputs[1])
    links.new(extrude_mesh_001.outputs[0], repeat_output_001.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (589.0, -495.1333312988281)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = False
    # Vector
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Scale
    noise_texture.inputs[2].default_value = 30.0
    # Detail
    noise_texture.inputs[3].default_value = 0.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Offset
    noise_texture.inputs[6].default_value = 0.0
    # Gain
    noise_texture.inputs[7].default_value = 1.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0
    # Links for noise_texture

    mesh_to_curve_003 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_003.name = "Mesh to Curve.003"
    mesh_to_curve_003.label = ""
    mesh_to_curve_003.location = (2449.0, -55.133331298828125)
    mesh_to_curve_003.bl_label = "Mesh to Curve"
    mesh_to_curve_003.mode = "EDGES"
    # Selection
    mesh_to_curve_003.inputs[1].default_value = True
    # Links for mesh_to_curve_003
    links.new(repeat_output_001.outputs[0], mesh_to_curve_003.inputs[0])

    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.name = "Curve to Mesh.003"
    curve_to_mesh_003.label = ""
    curve_to_mesh_003.location = (469.0, -35.80000305175781)
    curve_to_mesh_003.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_003.inputs[3].default_value = False
    # Links for curve_to_mesh_003

    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_003.name = "Spline Parameter.003"
    spline_parameter_003.label = ""
    spline_parameter_003.location = (49.0, -515.7999877929688)
    spline_parameter_003.bl_label = "Spline Parameter"
    # Links for spline_parameter_003

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (29.0, -175.8000030517578)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(spline_parameter_003.outputs[0], float_curve.inputs[1])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (289.0, -175.8000030517578)
    math.bl_label = "Math"
    math.operation = "MULTIPLY"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.004999999888241291
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(float_curve.outputs[0], math.inputs[0])
    links.new(math.outputs[0], curve_to_mesh_003.inputs[2])
    links.new(math.outputs[0], group_output.inputs[2])

    points_001 = nodes.new("GeometryNodePoints")
    points_001.name = "Points.001"
    points_001.label = ""
    points_001.location = (229.0, -315.1333312988281)
    points_001.bl_label = "Points"
    # Position
    points_001.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Radius
    points_001.inputs[2].default_value = 0.10000000149011612
    # Links for points_001

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (229.0, -495.1333312988281)
    index.bl_label = "Index"
    # Links for index

    capture_attribute_007 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_007.name = "Capture Attribute.007"
    capture_attribute_007.label = ""
    capture_attribute_007.location = (409.0, -315.1333312988281)
    capture_attribute_007.bl_label = "Capture Attribute"
    capture_attribute_007.active_index = 0
    capture_attribute_007.domain = "POINT"
    # Links for capture_attribute_007
    links.new(capture_attribute_007.outputs[0], points_to_vertices.inputs[0])
    links.new(points_001.outputs[0], capture_attribute_007.inputs[0])
    links.new(index.outputs[0], capture_attribute_007.inputs[1])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (429.0, -495.1333312988281)
    math_001.bl_label = "Math"
    math_001.operation = "MULTIPLY_ADD"
    math_001.use_clamp = False
    # Links for math_001
    links.new(capture_attribute_007.outputs[1], math_001.inputs[0])
    links.new(math_001.outputs[0], noise_texture.inputs[1])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.name = "Transform Geometry.006"
    transform_geometry_006.label = ""
    transform_geometry_006.location = (28.83331298828125, -79.56706237792969)
    transform_geometry_006.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_006.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_006.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_006.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    # Links for transform_geometry_006
    links.new(curve_to_mesh_003.outputs[0], transform_geometry_006.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.name = "Flip Faces.001"
    flip_faces_001.label = ""
    flip_faces_001.location = (188.83331298828125, -79.56706237792969)
    flip_faces_001.bl_label = "Flip Faces"
    # Selection
    flip_faces_001.inputs[1].default_value = True
    # Links for flip_faces_001
    links.new(transform_geometry_006.outputs[0], flip_faces_001.inputs[0])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (188.83331298828125, -39.56705856323242)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003
    links.new(flip_faces_001.outputs[0], join_geometry_003.inputs[0])
    links.new(curve_to_mesh_003.outputs[0], join_geometry_003.inputs[0])

    instance_on_points_003 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.name = "Instance on Points.003"
    instance_on_points_003.label = ""
    instance_on_points_003.location = (329.0, -155.8000030517578)
    instance_on_points_003.bl_label = "Instance on Points"
    # Selection
    instance_on_points_003.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_003.inputs[3].default_value = False
    # Instance Index
    instance_on_points_003.inputs[4].default_value = 0
    # Scale
    instance_on_points_003.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_003
    links.new(join_geometry_003.outputs[0], instance_on_points_003.inputs[2])

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.name = "Curve Circle.001"
    curve_circle_001.label = ""
    curve_circle_001.location = (189.0, -35.79999923706055)
    curve_circle_001.bl_label = "Curve Circle"
    curve_circle_001.mode = "RADIUS"
    # Point 1
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_001.inputs[4].default_value = 9.999999747378752e-05
    # Links for curve_circle_001
    links.new(curve_circle_001.outputs[0], instance_on_points_003.inputs[0])

    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.name = "Align Rotation to Vector.002"
    align_rotation_to_vector_002.label = ""
    align_rotation_to_vector_002.location = (189.0, -435.79998779296875)
    align_rotation_to_vector_002.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_002.axis = "X"
    align_rotation_to_vector_002.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_002.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_002.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_002
    links.new(align_rotation_to_vector_002.outputs[0], instance_on_points_003.inputs[5])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (189.0, -595.7999877929688)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_002.inputs[2])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (2860.0, 280.0)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004

    realize_instances_003 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.name = "Realize Instances.003"
    realize_instances_003.label = ""
    realize_instances_003.location = (509.0, -155.8000030517578)
    realize_instances_003.bl_label = "Realize Instances"
    # Selection
    realize_instances_003.inputs[1].default_value = True
    # Realize All
    realize_instances_003.inputs[2].default_value = True
    # Depth
    realize_instances_003.inputs[3].default_value = 0
    # Links for realize_instances_003
    links.new(instance_on_points_003.outputs[0], realize_instances_003.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (509.0, -35.79998779296875)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(switch.outputs[0], transform_geometry_005.inputs[0])
    links.new(dual_mesh.outputs[0], switch.inputs[2])
    links.new(ico_sphere_001.outputs[0], switch.inputs[1])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (29.0, -35.79998779296875)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[0], ico_sphere_001.inputs[0])
    links.new(group_input_001.outputs[2], switch.inputs[0])

    group_input_002 = nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.label = ""
    group_input_002.location = (29.0, -515.13330078125)
    group_input_002.bl_label = "Group Input"
    # Links for group_input_002
    links.new(group_input_002.outputs[8], points_001.inputs[0])
    links.new(group_input_002.outputs[9], math_001.inputs[1])
    links.new(group_input_002.outputs[10], math_001.inputs[2])

    group_input_003 = nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.label = ""
    group_input_003.location = (29.0, -95.80000305175781)
    group_input_003.bl_label = "Group Input"
    # Links for group_input_003
    links.new(group_input_003.outputs[7], curve_circle_001.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Profile"
    frame.location = (-2249.0, 615.7999877929688)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "Gem"
    frame_001.location = (1151.0, 1015.7999877929688)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Strands"
    frame_002.location = (-2709.0, -124.86666870117188)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Mesh"
    frame_003.location = (211.0, -24.19999885559082)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Mirror"
    frame_004.location = (875.6666870117188, -48.33333206176758)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = "Radial Array"
    frame_005.location = (1271.0, -44.20000076293945)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (2020.0, 460.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (2380.0, 500.0)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(store_named_attribute.outputs[0], join_geometry_005.inputs[0])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (869.0, -35.79998779296875)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001
    links.new(transform_geometry_005.outputs[0], store_named_attribute_001.inputs[0])
    links.new(store_named_attribute_001.outputs[0], join_geometry_005.inputs[0])
    links.new(group_input_001.outputs[1], store_named_attribute_001.inputs[2])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (1549.0, -635.13330078125)
    mix.bl_label = "Mix"
    mix.data_type = "VECTOR"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    # Factor
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix.inputs[2].default_value = 0.0
    # B
    mix.inputs[3].default_value = 0.0
    # A
    mix.inputs[4].default_value = [1.0, 1.0, 0.0]
    # B
    mix.inputs[5].default_value = [1.0, 1.0, 1.0]
    # A
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (1589.0, -295.1333312988281)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "MULTIPLY"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(vector_math.outputs[0], extrude_mesh_001.inputs[2])
    links.new(mix.outputs[1], vector_math.inputs[1])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (1189.0, -635.13330078125)
    position.bl_label = "Position"
    # Links for position

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (1189.0, -695.13330078125)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "LENGTH"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(position.outputs[0], vector_math_001.inputs[0])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (1389.0, -635.13330078125)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    # From Max
    map_range.inputs[2].default_value = 0.05000000074505806
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0
    # Steps
    map_range.inputs[5].default_value = 4.0
    # Vector
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(vector_math_001.outputs[1], map_range.inputs[0])
    links.new(map_range.outputs[0], mix.inputs[0])

    group_input_004 = nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.label = ""
    group_input_004.location = (1189.0, -815.13330078125)
    group_input_004.bl_label = "Group Input"
    # Links for group_input_004
    links.new(group_input_004.outputs[0], map_range.inputs[1])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (2020.0, 160.0)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_002.inputs[3].default_value = True
    # Links for store_named_attribute_002
    links.new(realize_instances_003.outputs[0], store_named_attribute_002.inputs[0])
    links.new(store_named_attribute_002.outputs[0], join_geometry_004.inputs[0])

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (2620.0, 360.0)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry
    links.new(join_geometry_005.outputs[0], transform_geometry.inputs[0])
    links.new(transform_geometry.outputs[0], join_geometry_004.inputs[0])

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (789.0, -495.1333312988281)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(noise_texture.outputs[1], separate_x_y_z.inputs[0])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (1129.0, -435.1333312988281)
    combine_x_y_z.bl_label = "Combine XYZ"
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], vector_math.inputs[0])
    links.new(separate_x_y_z.outputs[0], combine_x_y_z.inputs[0])
    links.new(separate_x_y_z.outputs[1], combine_x_y_z.inputs[1])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (949.0, -555.13330078125)
    math_002.bl_label = "Math"
    math_002.operation = "ABSOLUTE"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 0.5
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(separate_x_y_z.outputs[2], math_002.inputs[0])
    links.new(math_002.outputs[0], combine_x_y_z.inputs[2])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (1069.0, -195.79998779296875)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Count"
    # Count
    resample_curve.inputs[3].default_value = 12
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve
    links.new(resample_curve.outputs[0], curve_to_mesh_002.inputs[1])
    links.new(set_spline_type.outputs[0], resample_curve.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (2609.0, -55.133331298828125)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Length"
    # Count
    resample_curve_001.inputs[3].default_value = 10
    # Length
    resample_curve_001.inputs[4].default_value = 0.0007999999797903001
    # Links for resample_curve_001
    links.new(resample_curve_001.outputs[0], curve_to_mesh_003.inputs[0])
    links.new(mesh_to_curve_003.outputs[0], resample_curve_001.inputs[0])
    links.new(resample_curve_001.outputs[0], group_output.inputs[4])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (3060.0, 460.0)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Links for switch_001
    links.new(switch_001.outputs[0], group_output.inputs[0])
    links.new(join_geometry_004.outputs[0], switch_001.inputs[2])
    links.new(join_geometry_005.outputs[0], switch_001.inputs[1])

    group_input_005 = nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    group_input_005.label = ""
    group_input_005.location = (3060.0, 520.0)
    group_input_005.bl_label = "Group Input"
    # Links for group_input_005
    links.new(group_input_005.outputs[6], switch_001.inputs[0])

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.label = ""
    switch_002.location = (1769.0, -275.1333312988281)
    switch_002.bl_label = "Switch"
    switch_002.input_type = "VECTOR"
    # True
    switch_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for switch_002
    links.new(repeat_input_001.outputs[0], switch_002.inputs[0])
    links.new(vector_math.outputs[0], switch_002.inputs[1])

    evaluate_at_index = nodes.new("GeometryNodeFieldAtIndex")
    evaluate_at_index.name = "Evaluate at Index"
    evaluate_at_index.label = ""
    evaluate_at_index.location = (1929.0, -275.1333312988281)
    evaluate_at_index.bl_label = "Evaluate at Index"
    evaluate_at_index.domain = "POINT"
    evaluate_at_index.data_type = "FLOAT_VECTOR"
    # Index
    evaluate_at_index.inputs[1].default_value = 0
    # Links for evaluate_at_index
    links.new(switch_002.outputs[0], evaluate_at_index.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (2089.0, -275.1333312988281)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "ADD"
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], repeat_output_001.inputs[2])
    links.new(evaluate_at_index.outputs[0], vector_math_002.inputs[0])
    links.new(repeat_input_001.outputs[3], vector_math_002.inputs[1])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (389.0, -35.79998779296875)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_001
    links.new(curve_to_mesh_003.outputs[0], transform_geometry_001.inputs[0])

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.label = ""
    attribute_statistic.location = (2469.0, -255.13333129882812)
    attribute_statistic.bl_label = "Attribute Statistic"
    attribute_statistic.data_type = "FLOAT_VECTOR"
    attribute_statistic.domain = "POINT"
    # Selection
    attribute_statistic.inputs[1].default_value = True
    # Links for attribute_statistic
    links.new(repeat_output_001.outputs[0], attribute_statistic.inputs[0])
    links.new(repeat_output_001.outputs[2], attribute_statistic.inputs[2])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.label = ""
    align_rotation_to_vector.location = (29.0, -155.79998779296875)
    align_rotation_to_vector.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector
    links.new(attribute_statistic.outputs[3], align_rotation_to_vector.inputs[2])

    invert_rotation = nodes.new("FunctionNodeInvertRotation")
    invert_rotation.name = "Invert Rotation"
    invert_rotation.label = ""
    invert_rotation.location = (229.0, -155.79998779296875)
    invert_rotation.bl_label = "Invert Rotation"
    # Links for invert_rotation
    links.new(invert_rotation.outputs[0], transform_geometry_001.inputs[3])
    links.new(align_rotation_to_vector.outputs[0], invert_rotation.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = "Align to X"
    frame_006.location = (1311.0, -884.2000122070312)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (549.0, -35.79998779296875)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_003.inputs[3].default_value = True
    # Links for store_named_attribute_003
    links.new(store_named_attribute_003.outputs[0], group_output.inputs[3])
    links.new(transform_geometry_001.outputs[0], store_named_attribute_003.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (315.669921875, -66.96894073486328)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(reroute.outputs[0], curve_to_mesh_003.inputs[1])
    links.new(resample_curve.outputs[0], reroute.inputs[0])
    links.new(reroute.outputs[0], group_output.inputs[1])

    # Parent assignments
    group_input.parent = frame
    ico_sphere_001.parent = frame_001
    dual_mesh.parent = frame_001
    curve_circle.parent = frame
    curve_to_mesh_002.parent = frame
    points.parent = frame
    random_value.parent = frame
    points_to_curves.parent = frame
    gradient_texture.parent = frame
    set_spline_cyclic.parent = frame
    set_spline_type.parent = frame
    transform_geometry_005.parent = frame_001
    points_to_vertices.parent = frame_002
    extrude_mesh_001.parent = frame_002
    repeat_input_001.parent = frame_002
    repeat_output_001.parent = frame_002
    noise_texture.parent = frame_002
    mesh_to_curve_003.parent = frame_002
    curve_to_mesh_003.parent = frame_003
    spline_parameter_003.parent = frame_003
    float_curve.parent = frame_003
    math.parent = frame_003
    points_001.parent = frame_002
    index.parent = frame_002
    capture_attribute_007.parent = frame_002
    math_001.parent = frame_002
    transform_geometry_006.parent = frame_004
    flip_faces_001.parent = frame_004
    join_geometry_003.parent = frame_004
    instance_on_points_003.parent = frame_005
    curve_circle_001.parent = frame_005
    align_rotation_to_vector_002.parent = frame_005
    curve_tangent.parent = frame_005
    realize_instances_003.parent = frame_005
    switch.parent = frame_001
    group_input_001.parent = frame_001
    group_input_002.parent = frame_002
    group_input_003.parent = frame_005
    store_named_attribute_001.parent = frame_001
    mix.parent = frame_002
    vector_math.parent = frame_002
    position.parent = frame_002
    vector_math_001.parent = frame_002
    map_range.parent = frame_002
    group_input_004.parent = frame_002
    separate_x_y_z.parent = frame_002
    combine_x_y_z.parent = frame_002
    math_002.parent = frame_002
    resample_curve.parent = frame
    resample_curve_001.parent = frame_002
    switch_002.parent = frame_002
    evaluate_at_index.parent = frame_002
    vector_math_002.parent = frame_002
    transform_geometry_001.parent = frame_006
    attribute_statistic.parent = frame_002
    align_rotation_to_vector.parent = frame_006
    invert_rotation.parent = frame_006
    store_named_attribute_003.parent = frame_006
    reroute.parent = frame_003

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_swap__attr_group():
    group_name = "Swap Attr"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="ID", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Old", in_out="INPUT", socket_type="NodeSocketString")
    socket.default_value = "ruby"
    socket = group.interface.new_socket(name="New", in_out="INPUT", socket_type="NodeSocketString")
    socket.default_value = "saphire"

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (430.0, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-440.0, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (80.0, 140.0)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001
    links.new(group_input.outputs[0], store_named_attribute_001.inputs[0])
    links.new(group_input.outputs[3], store_named_attribute_001.inputs[2])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.label = ""
    random_value_001.location = (-240.0, 20.0)
    random_value_001.bl_label = "Random Value"
    random_value_001.data_type = "BOOLEAN"
    # Min
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_001.inputs[2].default_value = 0.0
    # Max
    random_value_001.inputs[3].default_value = 1.0
    # Min
    random_value_001.inputs[4].default_value = 0
    # Max
    random_value_001.inputs[5].default_value = 100
    # Probability
    random_value_001.inputs[6].default_value = 0.5
    # Seed
    random_value_001.inputs[8].default_value = 0
    # Links for random_value_001
    links.new(group_input.outputs[1], random_value_001.inputs[7])

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.label = ""
    boolean_math_002.location = (-80.0, 20.0)
    boolean_math_002.bl_label = "Boolean Math"
    boolean_math_002.operation = "AND"
    # Links for boolean_math_002
    links.new(boolean_math_002.outputs[0], store_named_attribute_001.inputs[1])
    links.new(random_value_001.outputs[3], boolean_math_002.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (-240.0, -140.0)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "BOOLEAN"
    # Links for named_attribute
    links.new(named_attribute.outputs[0], boolean_math_002.inputs[1])
    links.new(group_input.outputs[2], named_attribute.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (240.0, 140.0)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    # Value
    store_named_attribute_002.inputs[3].default_value = False
    # Links for store_named_attribute_002
    links.new(store_named_attribute_001.outputs[0], store_named_attribute_002.inputs[0])
    links.new(boolean_math_002.outputs[0], store_named_attribute_002.inputs[1])
    links.new(store_named_attribute_002.outputs[0], group_output.inputs[0])
    links.new(group_input.outputs[2], store_named_attribute_002.inputs[2])

    # Parent assignments

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_shoulders_group():
    group_name = "Shoulders"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (13900.0, 40.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    bézier_segment_004 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_004.name = "Bézier Segment.004"
    bézier_segment_004.label = ""
    bézier_segment_004.location = (249.0, -415.79998779296875)
    bézier_segment_004.bl_label = "Bézier Segment"
    bézier_segment_004.mode = "OFFSET"
    # Resolution
    bézier_segment_004.inputs[0].default_value = 16
    # Start
    bézier_segment_004.inputs[1].default_value = Vector((-0.23098699748516083, 0.009999999776482582, 0.39754199981689453))
    # Start Handle
    bézier_segment_004.inputs[2].default_value = Vector((0.0, -0.10000000149011612, 0.0))
    # End Handle
    bézier_segment_004.inputs[3].default_value = Vector((-0.05999999865889549, 0.029999999329447746, 0.019999999552965164))
    # End
    bézier_segment_004.inputs[4].default_value = Vector((-0.10215499997138977, -0.13706600666046143, 0.31426501274108887))
    # Links for bézier_segment_004

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (1969.0, -435.79998779296875)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh

    arc = nodes.new("GeometryNodeCurveArc")
    arc.name = "Arc"
    arc.label = ""
    arc.location = (1229.0, -735.7999877929688)
    arc.bl_label = "Arc"
    arc.mode = "RADIUS"
    # Resolution
    arc.inputs[0].default_value = 24
    # Start
    arc.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    arc.inputs[2].default_value = Vector((0.0, 2.0, 0.0))
    # End
    arc.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Start Angle
    arc.inputs[5].default_value = 1.3089969158172607
    # Sweep Angle
    arc.inputs[6].default_value = 0.5235987901687622
    # Offset Angle
    arc.inputs[7].default_value = 0.0
    # Connect Center
    arc.inputs[8].default_value = False
    # Invert Arc
    arc.inputs[9].default_value = False
    # Links for arc

    transform_geometry_012 = nodes.new("GeometryNodeTransform")
    transform_geometry_012.name = "Transform Geometry.012"
    transform_geometry_012.label = ""
    transform_geometry_012.location = (1389.0, -735.7999877929688)
    transform_geometry_012.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_012.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_012.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_012.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_012
    links.new(arc.outputs[0], transform_geometry_012.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    set_curve_tilt.label = ""
    set_curve_tilt.location = (409.0, -415.79998779296875)
    set_curve_tilt.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Tilt
    set_curve_tilt.inputs[2].default_value = -2.0682151317596436
    # Links for set_curve_tilt
    links.new(bézier_segment_004.outputs[0], set_curve_tilt.inputs[0])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.label = ""
    spline_parameter.location = (769.0, -575.7999877929688)
    spline_parameter.bl_label = "Spline Parameter"
    # Links for spline_parameter

    float_curve_003 = nodes.new("ShaderNodeFloatCurve")
    float_curve_003.name = "Float Curve.003"
    float_curve_003.label = ""
    float_curve_003.location = (769.0, -635.7999877929688)
    float_curve_003.bl_label = "Float Curve"
    # Factor
    float_curve_003.inputs[0].default_value = 1.0
    # Links for float_curve_003
    links.new(spline_parameter.outputs[0], float_curve_003.inputs[1])

    value_001 = nodes.new("ShaderNodeValue")
    value_001.name = "Value.001"
    value_001.label = ""
    value_001.location = (1229.0, -955.7999877929688)
    value_001.bl_label = "Value"
    # Links for value_001
    links.new(value_001.outputs[0], arc.inputs[4])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (1389.0, -995.7999877929688)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "SCALE"
    # Vector
    vector_math_003.inputs[0].default_value = [0.0, -0.9799999594688416, 0.0]
    # Vector
    vector_math_003.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_003
    links.new(value_001.outputs[0], vector_math_003.inputs[3])
    links.new(vector_math_003.outputs[0], transform_geometry_012.inputs[2])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (589.0, -415.79998779296875)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Count"
    # Count
    resample_curve.inputs[3].default_value = 16
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve
    links.new(set_curve_tilt.outputs[0], resample_curve.inputs[0])

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.label = ""
    capture_attribute.location = (1549.0, -735.7999877929688)
    capture_attribute.bl_label = "Capture Attribute"
    capture_attribute.active_index = 1
    capture_attribute.domain = "POINT"
    # Links for capture_attribute
    links.new(capture_attribute.outputs[0], curve_to_mesh.inputs[1])
    links.new(transform_geometry_012.outputs[0], capture_attribute.inputs[0])
    links.new(spline_parameter.outputs[0], capture_attribute.inputs[1])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (1769.0, -435.79998779296875)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 2
    capture_attribute_001.domain = "POINT"
    # Links for capture_attribute_001
    links.new(capture_attribute_001.outputs[0], curve_to_mesh.inputs[0])

    endpoint_selection = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection.name = "Endpoint Selection"
    endpoint_selection.label = ""
    endpoint_selection.location = (1389.0, -435.79998779296875)
    endpoint_selection.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection.inputs[0].default_value = 0
    # End Size
    endpoint_selection.inputs[1].default_value = 1
    # Links for endpoint_selection
    links.new(endpoint_selection.outputs[0], capture_attribute_001.inputs[1])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (789.0, -55.79999923706055)
    instance_on_points.bl_label = "Instance on Points"
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Scale
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points
    links.new(endpoint_selection.outputs[0], instance_on_points.inputs[1])

    arc_001 = nodes.new("GeometryNodeCurveArc")
    arc_001.name = "Arc.001"
    arc_001.label = ""
    arc_001.location = (369.0, -35.79999923706055)
    arc_001.bl_label = "Arc"
    arc_001.mode = "RADIUS"
    # Resolution
    arc_001.inputs[0].default_value = 32
    # Start
    arc_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    arc_001.inputs[2].default_value = Vector((0.0, 2.0, 0.0))
    # End
    arc_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    arc_001.inputs[4].default_value = 0.04000002145767212
    # Start Angle
    arc_001.inputs[5].default_value = 0.0
    # Sweep Angle
    arc_001.inputs[6].default_value = 3.1415927410125732
    # Offset Angle
    arc_001.inputs[7].default_value = 0.0
    # Connect Center
    arc_001.inputs[8].default_value = False
    # Invert Arc
    arc_001.inputs[9].default_value = False
    # Links for arc_001

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.label = ""
    align_rotation_to_vector.location = (209.0, -375.79998779296875)
    align_rotation_to_vector.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector

    set_curve_radius = nodes.new("GeometryNodeSetCurveRadius")
    set_curve_radius.name = "Set Curve Radius"
    set_curve_radius.label = ""
    set_curve_radius.location = (1149.0, -415.79998779296875)
    set_curve_radius.bl_label = "Set Curve Radius"
    # Selection
    set_curve_radius.inputs[1].default_value = True
    # Links for set_curve_radius
    links.new(set_curve_radius.outputs[0], capture_attribute_001.inputs[0])
    links.new(set_curve_radius.outputs[0], instance_on_points.inputs[0])
    links.new(float_curve_003.outputs[0], set_curve_radius.inputs[2])

    radius = nodes.new("GeometryNodeInputRadius")
    radius.name = "Radius"
    radius.label = ""
    radius.location = (1969.0, -575.7999877929688)
    radius.bl_label = "Radius"
    # Links for radius
    links.new(radius.outputs[0], curve_to_mesh.inputs[2])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.label = ""
    align_rotation_to_vector_001.location = (389.0, -375.79998779296875)
    align_rotation_to_vector_001.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_001.axis = "Y"
    align_rotation_to_vector_001.pivot_axis = "X"
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_001
    links.new(align_rotation_to_vector.outputs[0], align_rotation_to_vector_001.inputs[0])

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.name = "Normal.001"
    normal_001.label = ""
    normal_001.location = (29.0, -455.79998779296875)
    normal_001.bl_label = "Normal"
    normal_001.legacy_corner_normals = False
    # Links for normal_001
    links.new(normal_001.outputs[0], align_rotation_to_vector.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.name = "Rotate Rotation"
    rotate_rotation.label = ""
    rotate_rotation.location = (549.0, -395.79998779296875)
    rotate_rotation.bl_label = "Rotate Rotation"
    rotate_rotation.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation.inputs[1].default_value = Euler((-0.12514010071754456, 0.0, 0.0), 'XYZ')
    # Links for rotate_rotation
    links.new(rotate_rotation.outputs[0], instance_on_points.inputs[5])
    links.new(align_rotation_to_vector_001.outputs[0], rotate_rotation.inputs[0])

    transform_geometry_013 = nodes.new("GeometryNodeTransform")
    transform_geometry_013.name = "Transform Geometry.013"
    transform_geometry_013.label = ""
    transform_geometry_013.location = (549.0, -35.79999923706055)
    transform_geometry_013.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_013.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_013.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    # Rotation
    transform_geometry_013.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_013.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_013
    links.new(transform_geometry_013.outputs[0], instance_on_points.inputs[2])
    links.new(arc_001.outputs[0], transform_geometry_013.inputs[0])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    set_position_003.label = ""
    set_position_003.location = (3169.0, -495.79998779296875)
    set_position_003.bl_label = "Set Position"
    # Offset
    set_position_003.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_003
    links.new(capture_attribute_001.outputs[1], set_position_003.inputs[1])

    frame_013 = nodes.new("NodeFrame")
    frame_013.name = "Frame.013"
    frame_013.label = "End curve"
    frame_013.location = (1720.0, -820.0)
    frame_013.bl_label = "Frame"
    frame_013.text = None
    frame_013.shrink = True
    frame_013.label_size = 20
    # Links for frame_013

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (949.0, -55.79999923706055)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(instance_on_points.outputs[0], realize_instances.inputs[0])

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.label = ""
    sample_curve.location = (1109.0, -55.79999923706055)
    sample_curve.bl_label = "Sample Curve"
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = True
    sample_curve.data_type = "FLOAT"
    # Value
    sample_curve.inputs[1].default_value = 0.0
    # Length
    sample_curve.inputs[3].default_value = 0.0
    # Curve Index
    sample_curve.inputs[4].default_value = 0
    # Links for sample_curve
    links.new(realize_instances.outputs[0], sample_curve.inputs[0])
    links.new(sample_curve.outputs[1], set_position_003.inputs[2])
    links.new(capture_attribute.outputs[1], sample_curve.inputs[2])

    transform_geometry_015 = nodes.new("GeometryNodeTransform")
    transform_geometry_015.name = "Transform Geometry.015"
    transform_geometry_015.label = ""
    transform_geometry_015.location = (3809.0, -555.7999877929688)
    transform_geometry_015.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_015.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_015.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_015.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_015.inputs[4].default_value = Vector((1.0, -1.0, 1.0))
    # Links for transform_geometry_015

    flip_faces_006 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_006.name = "Flip Faces.006"
    flip_faces_006.label = ""
    flip_faces_006.location = (3969.0, -555.7999877929688)
    flip_faces_006.bl_label = "Flip Faces"
    # Selection
    flip_faces_006.inputs[1].default_value = True
    # Links for flip_faces_006
    links.new(transform_geometry_015.outputs[0], flip_faces_006.inputs[0])

    join_geometry_012 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_012.name = "Join Geometry.012"
    join_geometry_012.label = ""
    join_geometry_012.location = (4129.0, -495.79998779296875)
    join_geometry_012.bl_label = "Join Geometry"
    # Links for join_geometry_012
    links.new(flip_faces_006.outputs[0], join_geometry_012.inputs[0])

    endpoint_selection_001 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_001.name = "Endpoint Selection.001"
    endpoint_selection_001.label = ""
    endpoint_selection_001.location = (1389.0, -595.7999877929688)
    endpoint_selection_001.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection_001.inputs[0].default_value = 1
    # End Size
    endpoint_selection_001.inputs[1].default_value = 0
    # Links for endpoint_selection_001
    links.new(endpoint_selection_001.outputs[0], capture_attribute_001.inputs[2])

    curve_tangent_001 = nodes.new("GeometryNodeInputTangent")
    curve_tangent_001.name = "Curve Tangent.001"
    curve_tangent_001.label = ""
    curve_tangent_001.location = (209.0, -515.7999877929688)
    curve_tangent_001.bl_label = "Curve Tangent"
    # Links for curve_tangent_001
    links.new(curve_tangent_001.outputs[0], align_rotation_to_vector_001.inputs[2])

    set_position_004 = nodes.new("GeometryNodeSetPosition")
    set_position_004.name = "Set Position.004"
    set_position_004.label = ""
    set_position_004.location = (3589.0, -495.79998779296875)
    set_position_004.bl_label = "Set Position"
    # Offset
    set_position_004.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_004
    links.new(set_position_004.outputs[0], transform_geometry_015.inputs[0])
    links.new(set_position_004.outputs[0], join_geometry_012.inputs[0])
    links.new(set_position_003.outputs[0], set_position_004.inputs[0])

    position_004 = nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"
    position_004.label = ""
    position_004.location = (3329.0, -595.7999877929688)
    position_004.bl_label = "Position"
    # Links for position_004

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (3329.0, -655.7999877929688)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "MULTIPLY"
    # Vector
    vector_math_004.inputs[1].default_value = [1.0, 0.0, 1.0]
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(position_004.outputs[0], vector_math_004.inputs[0])
    links.new(vector_math_004.outputs[0], set_position_004.inputs[2])

    merge_by_distance_001 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_001.name = "Merge by Distance.001"
    merge_by_distance_001.label = ""
    merge_by_distance_001.location = (4309.0, -495.79998779296875)
    merge_by_distance_001.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_001.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_001.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_001
    links.new(join_geometry_012.outputs[0], merge_by_distance_001.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (3509.0, -555.7999877929688)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketBool"
    # Links for reroute
    links.new(reroute.outputs[0], set_position_004.inputs[1])
    links.new(capture_attribute_001.outputs[2], reroute.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (4269.0, -435.79998779296875)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketBool"
    # Links for reroute_001
    links.new(reroute_001.outputs[0], merge_by_distance_001.inputs[1])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (3529.0, -435.79998779296875)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketBool"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], reroute_001.inputs[0])
    links.new(reroute.outputs[0], reroute_002.inputs[0])

    mesh_to_curve_002 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.name = "Mesh to Curve.002"
    mesh_to_curve_002.label = ""
    mesh_to_curve_002.location = (209.0, -35.800018310546875)
    mesh_to_curve_002.bl_label = "Mesh to Curve"
    mesh_to_curve_002.mode = "EDGES"
    # Links for mesh_to_curve_002

    frame_014 = nodes.new("NodeFrame")
    frame_014.name = "Frame.014"
    frame_014.label = "Shoulder Cover"
    frame_014.location = (-5249.0, 875.7999877929688)
    frame_014.bl_label = "Frame"
    frame_014.text = None
    frame_014.shrink = True
    frame_014.label_size = 20
    # Links for frame_014

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Is Edge Boundary.001"
    is_edge_boundary.label = ""
    is_edge_boundary.location = (209.0, -175.80001831054688)
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    is_edge_boundary.bl_label = "Group"
    # Links for is_edge_boundary
    links.new(is_edge_boundary.outputs[0], mesh_to_curve_002.inputs[1])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (1209.0, -35.800018310546875)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_001.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False
    # Links for curve_to_mesh_001

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.label = ""
    curve_line.location = (809.0, -355.8000183105469)
    curve_line.bl_label = "Curve Line"
    curve_line.mode = "POINTS"
    # Start
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    # End
    curve_line.inputs[1].default_value = Vector((0.019999999552965164, 0.0, 0.0))
    # Direction
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    # Length
    curve_line.inputs[3].default_value = 1.0
    # Links for curve_line

    set_curve_tilt_001 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_001.name = "Set Curve Tilt.001"
    set_curve_tilt_001.label = ""
    set_curve_tilt_001.location = (769.0, -35.800018310546875)
    set_curve_tilt_001.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_001.inputs[1].default_value = True
    # Tilt
    set_curve_tilt_001.inputs[2].default_value = -7.752577304840088
    # Links for set_curve_tilt_001

    flip_faces_005 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_005.name = "Flip Faces.005"
    flip_faces_005.label = ""
    flip_faces_005.location = (1369.0, -35.800018310546875)
    flip_faces_005.bl_label = "Flip Faces"
    # Selection
    flip_faces_005.inputs[1].default_value = True
    # Links for flip_faces_005
    links.new(curve_to_mesh_001.outputs[0], flip_faces_005.inputs[0])

    frame_015 = nodes.new("NodeFrame")
    frame_015.name = "Frame.015"
    frame_015.label = "Outer Band"
    frame_015.location = (-729.0, 275.8000183105469)
    frame_015.bl_label = "Frame"
    frame_015.text = None
    frame_015.shrink = True
    frame_015.label_size = 20
    # Links for frame_015

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.name = "Capture Attribute.002"
    capture_attribute_002.label = ""
    capture_attribute_002.location = (989.0, -355.8000183105469)
    capture_attribute_002.bl_label = "Capture Attribute"
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "POINT"
    # Links for capture_attribute_002
    links.new(capture_attribute_002.outputs[0], curve_to_mesh_001.inputs[1])
    links.new(curve_line.outputs[0], capture_attribute_002.inputs[0])

    endpoint_selection_002 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_002.name = "Endpoint Selection.002"
    endpoint_selection_002.label = ""
    endpoint_selection_002.location = (989.0, -475.8000183105469)
    endpoint_selection_002.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection_002.inputs[0].default_value = 0
    # End Size
    endpoint_selection_002.inputs[1].default_value = 1
    # Links for endpoint_selection_002
    links.new(endpoint_selection_002.outputs[0], capture_attribute_002.inputs[1])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (473.83331298828125, -335.79998779296875)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "AND"
    # Links for boolean_math

    capture_attribute_003 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.name = "Capture Attribute.003"
    capture_attribute_003.label = ""
    capture_attribute_003.location = (989.0, -35.800018310546875)
    capture_attribute_003.bl_label = "Capture Attribute"
    capture_attribute_003.active_index = 1
    capture_attribute_003.domain = "POINT"
    # Links for capture_attribute_003
    links.new(capture_attribute_003.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(set_curve_tilt_001.outputs[0], capture_attribute_003.inputs[0])

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.label = ""
    spline_parameter_001.location = (989.0, -175.80001831054688)
    spline_parameter_001.bl_label = "Spline Parameter"
    # Links for spline_parameter_001
    links.new(spline_parameter_001.outputs[0], capture_attribute_003.inputs[1])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (113.83331298828125, -455.79998779296875)
    compare_001.bl_label = "Compare"
    compare_001.operation = "EQUAL"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = 0.5
    # A
    compare_001.inputs[2].default_value = 0
    # B
    compare_001.inputs[3].default_value = 0
    # A
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_001.inputs[8].default_value = ""
    # B
    compare_001.inputs[9].default_value = ""
    # C
    compare_001.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_001.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_001.inputs[12].default_value = 0.1210000067949295
    # Links for compare_001

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.label = ""
    extrude_mesh.location = (1853.833251953125, -115.79999542236328)
    extrude_mesh.bl_label = "Extrude Mesh"
    extrude_mesh.mode = "EDGES"
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.07000000029802322
    # Individual
    extrude_mesh.inputs[4].default_value = True
    # Links for extrude_mesh

    repeat_input = nodes.new("GeometryNodeRepeatInput")
    repeat_input.name = "Repeat Input"
    repeat_input.label = ""
    repeat_input.location = (673.8333129882812, -175.79998779296875)
    repeat_input.bl_label = "Repeat Input"
    # Value
    repeat_input.inputs[3].default_value = 0.0
    # Links for repeat_input
    links.new(flip_faces_005.outputs[0], repeat_input.inputs[1])
    links.new(repeat_input.outputs[1], extrude_mesh.inputs[0])
    links.new(boolean_math.outputs[0], repeat_input.inputs[2])
    links.new(repeat_input.outputs[2], extrude_mesh.inputs[1])

    repeat_output = nodes.new("GeometryNodeRepeatOutput")
    repeat_output.name = "Repeat Output"
    repeat_output.label = ""
    repeat_output.location = (2233.833251953125, -135.79998779296875)
    repeat_output.bl_label = "Repeat Output"
    repeat_output.active_index = 2
    repeat_output.inspection_index = 0
    # Links for repeat_output
    links.new(extrude_mesh.outputs[0], repeat_output.inputs[0])
    links.new(extrude_mesh.outputs[1], repeat_output.inputs[1])

    vector_002 = nodes.new("FunctionNodeInputVector")
    vector_002.name = "Vector.002"
    vector_002.label = ""
    vector_002.location = (1213.833251953125, -375.79998779296875)
    vector_002.bl_label = "Vector"
    vector_002.vector = Vector((-0.03999999910593033, 0.0, -0.14999999105930328))
    # Links for vector_002

    set_curve_tilt_002 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_002.name = "Set Curve Tilt.002"
    set_curve_tilt_002.label = ""
    set_curve_tilt_002.location = (769.0, -415.79998779296875)
    set_curve_tilt_002.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_002.inputs[1].default_value = True
    # Links for set_curve_tilt_002
    links.new(set_curve_tilt_002.outputs[0], set_curve_radius.inputs[0])
    links.new(resample_curve.outputs[0], set_curve_tilt_002.inputs[0])

    curve_tilt = nodes.new("GeometryNodeInputCurveTilt")
    curve_tilt.name = "Curve Tilt"
    curve_tilt.label = ""
    curve_tilt.location = (389.0, -175.79998779296875)
    curve_tilt.bl_label = "Curve Tilt"
    # Links for curve_tilt

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (569.0, -155.79998779296875)
    math_003.bl_label = "Math"
    math_003.operation = "SUBTRACT"
    math_003.use_clamp = False
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(curve_tilt.outputs[0], math_003.inputs[0])
    links.new(math_003.outputs[0], set_curve_tilt_002.inputs[2])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"
    spline_parameter_002.label = ""
    spline_parameter_002.location = (29.0, -35.79998779296875)
    spline_parameter_002.bl_label = "Spline Parameter"
    # Links for spline_parameter_002

    float_curve_004 = nodes.new("ShaderNodeFloatCurve")
    float_curve_004.name = "Float Curve.004"
    float_curve_004.label = ""
    float_curve_004.location = (29.0, -95.79998779296875)
    float_curve_004.bl_label = "Float Curve"
    # Factor
    float_curve_004.inputs[0].default_value = 1.0
    # Links for float_curve_004
    links.new(spline_parameter_002.outputs[0], float_curve_004.inputs[1])
    links.new(float_curve_004.outputs[0], math_003.inputs[1])

    capture_attribute_004 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_004.name = "Capture Attribute.004"
    capture_attribute_004.label = ""
    capture_attribute_004.location = (29.0, -55.800018310546875)
    capture_attribute_004.bl_label = "Capture Attribute"
    capture_attribute_004.active_index = 0
    capture_attribute_004.domain = "POINT"
    # Links for capture_attribute_004
    links.new(merge_by_distance_001.outputs[0], capture_attribute_004.inputs[0])
    links.new(capture_attribute_004.outputs[0], mesh_to_curve_002.inputs[0])

    normal_002 = nodes.new("GeometryNodeInputNormal")
    normal_002.name = "Normal.002"
    normal_002.label = ""
    normal_002.location = (29.0, -315.8000183105469)
    normal_002.bl_label = "Normal"
    normal_002.legacy_corner_normals = False
    # Links for normal_002

    set_curve_normal = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal.name = "Set Curve Normal"
    set_curve_normal.label = ""
    set_curve_normal.location = (469.0, -55.800018310546875)
    set_curve_normal.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal.inputs[1].default_value = True
    # Mode
    set_curve_normal.inputs[2].default_value = "Free"
    # Links for set_curve_normal
    links.new(mesh_to_curve_002.outputs[0], set_curve_normal.inputs[0])
    links.new(capture_attribute_004.outputs[1], set_curve_normal.inputs[3])
    links.new(set_curve_normal.outputs[0], set_curve_tilt_001.inputs[0])

    blur_attribute = nodes.new("GeometryNodeBlurAttribute")
    blur_attribute.name = "Blur Attribute"
    blur_attribute.label = ""
    blur_attribute.location = (29.0, -195.80001831054688)
    blur_attribute.bl_label = "Blur Attribute"
    blur_attribute.data_type = "FLOAT_VECTOR"
    # Iterations
    blur_attribute.inputs[1].default_value = 5
    # Weight
    blur_attribute.inputs[2].default_value = 1.0
    # Links for blur_attribute
    links.new(blur_attribute.outputs[0], capture_attribute_004.inputs[1])
    links.new(normal_002.outputs[0], blur_attribute.inputs[0])

    endpoint_selection_003 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_003.name = "Endpoint Selection.003"
    endpoint_selection_003.label = ""
    endpoint_selection_003.location = (989.0, -235.80001831054688)
    endpoint_selection_003.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection_003.inputs[0].default_value = 1
    # End Size
    endpoint_selection_003.inputs[1].default_value = 1
    # Links for endpoint_selection_003
    links.new(endpoint_selection_003.outputs[0], capture_attribute_003.inputs[2])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.label = ""
    boolean_math_001.location = (293.83331298828125, -455.79998779296875)
    boolean_math_001.bl_label = "Boolean Math"
    boolean_math_001.operation = "NIMPLY"
    # Links for boolean_math_001
    links.new(compare_001.outputs[0], boolean_math_001.inputs[0])
    links.new(boolean_math_001.outputs[0], boolean_math.inputs[1])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (873.8333129882812, -875.7999877929688)
    math_004.bl_label = "Math"
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 0.5
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004

    integer_001 = nodes.new("FunctionNodeInputInt")
    integer_001.name = "Integer.001"
    integer_001.label = ""
    integer_001.location = (673.8333129882812, -35.79999542236328)
    integer_001.bl_label = "Integer"
    integer_001.integer = 9
    # Links for integer_001
    links.new(integer_001.outputs[0], repeat_input.inputs[0])

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (673.8333129882812, -95.79999542236328)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "SUBTRACT"
    # Value
    integer_math.inputs[1].default_value = 1
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(integer_001.outputs[0], integer_math.inputs[0])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (673.8333129882812, -135.79998779296875)
    math_006.bl_label = "Math"
    math_006.operation = "DIVIDE"
    math_006.use_clamp = False
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(repeat_input.outputs[0], math_006.inputs[0])
    links.new(integer_math.outputs[0], math_006.inputs[1])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.label = ""
    math_007.location = (1053.833251953125, -875.7999877929688)
    math_007.bl_label = "Math"
    math_007.operation = "SIGN"
    math_007.use_clamp = False
    # Value
    math_007.inputs[1].default_value = 11.59999942779541
    # Value
    math_007.inputs[2].default_value = 0.5
    # Links for math_007
    links.new(math_004.outputs[0], math_007.inputs[0])

    math_008 = nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.label = ""
    math_008.location = (1213.833251953125, -595.7999877929688)
    math_008.bl_label = "Math"
    math_008.operation = "MULTIPLY"
    math_008.use_clamp = False
    # Value
    math_008.inputs[2].default_value = 0.5
    # Links for math_008
    links.new(math_007.outputs[0], math_008.inputs[1])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (1633.833251953125, -375.79998779296875)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "MULTIPLY_ADD"
    # Vector
    vector_math_005.inputs[0].default_value = [0.0, 0.09000000357627869, 0.0]
    # Scale
    vector_math_005.inputs[3].default_value = 1.0
    # Links for vector_math_005
    links.new(math_008.outputs[0], vector_math_005.inputs[1])
    links.new(vector_math_005.outputs[0], extrude_mesh.inputs[2])

    float_curve_005 = nodes.new("ShaderNodeFloatCurve")
    float_curve_005.name = "Float Curve.005"
    float_curve_005.label = ""
    float_curve_005.location = (953.8333129882812, -555.7999877929688)
    float_curve_005.bl_label = "Float Curve"
    # Factor
    float_curve_005.inputs[0].default_value = 1.0
    # Links for float_curve_005
    links.new(math_006.outputs[0], float_curve_005.inputs[1])
    links.new(float_curve_005.outputs[0], math_008.inputs[0])

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (1413.833251953125, -375.79998779296875)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "MULTIPLY_ADD"
    # Vector
    vector_math_006.inputs[0].default_value = [0.0, -0.003000000026077032, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006
    links.new(vector_math_006.outputs[0], vector_math_005.inputs[2])
    links.new(vector_002.outputs[0], vector_math_006.inputs[2])
    links.new(math_007.outputs[0], vector_math_006.inputs[1])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Arm Extension"
    frame.location = (946.1666870117188, -104.20000457763672)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    reroute_005 = nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.label = ""
    reroute_005.location = (233.83331298828125, -395.79998779296875)
    reroute_005.bl_label = "Reroute"
    reroute_005.socket_idname = "NodeSocketBool"
    # Links for reroute_005
    links.new(reroute_005.outputs[0], boolean_math_001.inputs[1])
    links.new(capture_attribute_003.outputs[2], reroute_005.inputs[0])

    reroute_006 = nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.label = ""
    reroute_006.location = (33.83331298828125, -455.79998779296875)
    reroute_006.bl_label = "Reroute"
    reroute_006.socket_idname = "NodeSocketFloat"
    # Links for reroute_006
    links.new(reroute_006.outputs[0], compare_001.inputs[0])
    links.new(capture_attribute_003.outputs[1], reroute_006.inputs[0])

    reroute_007 = nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    reroute_007.label = ""
    reroute_007.location = (313.83331298828125, -255.79998779296875)
    reroute_007.bl_label = "Reroute"
    reroute_007.socket_idname = "NodeSocketBool"
    # Links for reroute_007
    links.new(reroute_007.outputs[0], boolean_math.inputs[0])
    links.new(capture_attribute_002.outputs[1], reroute_007.inputs[0])

    reroute_008 = nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    reroute_008.label = ""
    reroute_008.location = (93.83331298828125, -855.7999877929688)
    reroute_008.bl_label = "Reroute"
    reroute_008.socket_idname = "NodeSocketFloat"
    # Links for reroute_008
    links.new(reroute_006.outputs[0], reroute_008.inputs[0])

    reroute_009 = nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    reroute_009.label = ""
    reroute_009.location = (833.8333129882812, -875.7999877929688)
    reroute_009.bl_label = "Reroute"
    reroute_009.socket_idname = "NodeSocketFloat"
    # Links for reroute_009
    links.new(reroute_009.outputs[0], math_004.inputs[0])
    links.new(reroute_008.outputs[0], reroute_009.inputs[0])

    reroute_010 = nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    reroute_010.label = ""
    reroute_010.location = (3460.0, -560.0)
    reroute_010.bl_label = "Reroute"
    reroute_010.socket_idname = "NodeSocketFloat"
    # Links for reroute_010
    links.new(reroute_006.outputs[0], reroute_010.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (3520.0, -540.0)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.5
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.10100000351667404
    # Links for compare
    links.new(reroute_010.outputs[0], compare.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (2053.833251953125, -195.79998779296875)
    switch.bl_label = "Switch"
    switch.input_type = "FLOAT"
    # Links for switch
    links.new(extrude_mesh.outputs[1], switch.inputs[0])
    links.new(switch.outputs[0], repeat_output.inputs[2])
    links.new(repeat_input.outputs[3], switch.inputs[1])
    links.new(math_006.outputs[0], switch.inputs[2])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.label = ""
    compare_002.location = (3520.0, -320.0)
    compare_002.bl_label = "Compare"
    compare_002.operation = "EQUAL"
    compare_002.data_type = "FLOAT"
    compare_002.mode = "ELEMENT"
    # B
    compare_002.inputs[1].default_value = 0.36000001430511475
    # A
    compare_002.inputs[2].default_value = 0
    # B
    compare_002.inputs[3].default_value = 0
    # A
    compare_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_002.inputs[8].default_value = ""
    # B
    compare_002.inputs[9].default_value = ""
    # C
    compare_002.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_002.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_002.inputs[12].default_value = 0.3409999907016754
    # Links for compare_002
    links.new(repeat_output.outputs[2], compare_002.inputs[0])

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.label = ""
    boolean_math_002.location = (3720.0, -360.0)
    boolean_math_002.bl_label = "Boolean Math"
    boolean_math_002.operation = "AND"
    # Links for boolean_math_002
    links.new(compare_002.outputs[0], boolean_math_002.inputs[0])
    links.new(compare.outputs[0], boolean_math_002.inputs[1])

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (3900.0, -240.0)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "FACE"
    # Links for separate_geometry
    links.new(repeat_output.outputs[0], separate_geometry.inputs[0])
    links.new(boolean_math_002.outputs[0], separate_geometry.inputs[1])

    rotate_on_centre = nodes.new("GeometryNodeGroup")
    rotate_on_centre.name = "Group"
    rotate_on_centre.label = ""
    rotate_on_centre.location = (13680.0, 80.0)
    rotate_on_centre.node_tree = create_rotate_on__centre_group()
    rotate_on_centre.bl_label = "Group"
    # Rotation
    rotate_on_centre.inputs[1].default_value = Euler((0.10437069833278656, 0.0, -0.04712388664484024), 'XYZ')
    # Links for rotate_on_centre
    links.new(rotate_on_centre.outputs[0], group_output.inputs[0])

    rotate_on_centre_1 = nodes.new("GeometryNodeGroup")
    rotate_on_centre_1.name = "Group.001"
    rotate_on_centre_1.label = ""
    rotate_on_centre_1.location = (73.83349609375, -92.86666870117188)
    rotate_on_centre_1.node_tree = create_rotate_on__centre_group()
    rotate_on_centre_1.bl_label = "Group"
    # Rotation
    rotate_on_centre_1.inputs[1].default_value = Euler((0.0, 0.2042035013437271, 0.0), 'XYZ')
    # Links for rotate_on_centre_1

    join_geometry_013 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_013.name = "Join Geometry.013"
    join_geometry_013.label = ""
    join_geometry_013.location = (12720.0, 0.0)
    join_geometry_013.bl_label = "Join Geometry"
    # Links for join_geometry_013

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (253.83349609375, -92.86666870117188)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((-0.006000000052154064, 0.0, -0.004999999888241291))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, 0.9800000190734863, 1.0))
    # Links for transform_geometry
    links.new(rotate_on_centre_1.outputs[0], transform_geometry.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (433.83349609375, -132.86666870117188)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.0, 0.019999999552965164))
    # Rotation
    transform_geometry_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0099999904632568, 0.9800000190734863, 1.0))
    # Links for transform_geometry_001

    reroute_004 = nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.label = ""
    reroute_004.location = (3200.0, 260.0)
    reroute_004.bl_label = "Reroute"
    reroute_004.socket_idname = "NodeSocketGeometry"
    # Links for reroute_004
    links.new(merge_by_distance_001.outputs[0], reroute_004.inputs[0])

    rotate_on_centre_2 = nodes.new("GeometryNodeGroup")
    rotate_on_centre_2.name = "Group.002"
    rotate_on_centre_2.label = ""
    rotate_on_centre_2.location = (3360.0, 460.0)
    rotate_on_centre_2.node_tree = create_rotate_on__centre_group()
    rotate_on_centre_2.bl_label = "Group"
    # Rotation
    rotate_on_centre_2.inputs[1].default_value = Euler((0.0, 0.02635446935892105, 0.0), 'XYZ')
    # Links for rotate_on_centre_2
    links.new(reroute_004.outputs[0], rotate_on_centre_2.inputs[0])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    transform_geometry_002.label = ""
    transform_geometry_002.location = (3520.0, 460.0)
    transform_geometry_002.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_002.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_002.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_002
    links.new(rotate_on_centre_2.outputs[0], transform_geometry_002.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (3520.0, 420.0)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "SCALE"
    # Vector
    vector_math.inputs[0].default_value = [-0.5799999833106995, 0.0, 0.19999998807907104]
    # Vector
    vector_math.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 0.009999999776482582
    # Links for vector_math
    links.new(vector_math.outputs[0], transform_geometry_002.inputs[2])

    join_geometry_014 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_014.name = "Join Geometry.014"
    join_geometry_014.label = ""
    join_geometry_014.location = (3560.0, 40.0)
    join_geometry_014.bl_label = "Join Geometry"
    # Links for join_geometry_014
    links.new(repeat_output.outputs[0], join_geometry_014.inputs[0])
    links.new(reroute_004.outputs[0], join_geometry_014.inputs[0])

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.label = ""
    merge_by_distance.location = (3740.0, 60.0)
    merge_by_distance.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance.inputs[1].default_value = True
    # Mode
    merge_by_distance.inputs[2].default_value = "All"
    # Distance
    merge_by_distance.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance
    links.new(join_geometry_014.outputs[0], merge_by_distance.inputs[0])
    links.new(merge_by_distance.outputs[0], join_geometry_013.inputs[0])

    join_geometry_015 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_015.name = "Join Geometry.015"
    join_geometry_015.label = ""
    join_geometry_015.location = (8880.0, 280.0)
    join_geometry_015.bl_label = "Join Geometry"
    # Links for join_geometry_015
    links.new(transform_geometry_002.outputs[0], join_geometry_015.inputs[0])
    links.new(merge_by_distance.outputs[0], join_geometry_015.inputs[0])

    join_geometry_016 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_016.name = "Join Geometry.016"
    join_geometry_016.label = ""
    join_geometry_016.location = (613.83349609375, -32.866668701171875)
    join_geometry_016.bl_label = "Join Geometry"
    # Links for join_geometry_016
    links.new(join_geometry_016.outputs[0], join_geometry_013.inputs[0])
    links.new(transform_geometry.outputs[0], join_geometry_016.inputs[0])
    links.new(transform_geometry_001.outputs[0], join_geometry_016.inputs[0])

    rotate_on_centre_3 = nodes.new("GeometryNodeGroup")
    rotate_on_centre_3.name = "Group.004"
    rotate_on_centre_3.label = ""
    rotate_on_centre_3.location = (73.83349609375, -272.8666687011719)
    rotate_on_centre_3.node_tree = create_rotate_on__centre_group()
    rotate_on_centre_3.bl_label = "Group"
    # Rotation
    rotate_on_centre_3.inputs[1].default_value = Euler((0.0, 0.19373153150081635, 0.0), 'XYZ')
    # Links for rotate_on_centre_3
    links.new(rotate_on_centre_3.outputs[0], transform_geometry_001.inputs[0])

    reroute_011 = nodes.new("NodeReroute")
    reroute_011.name = "Reroute.011"
    reroute_011.label = ""
    reroute_011.location = (33.83349609375, -172.86666870117188)
    reroute_011.bl_label = "Reroute"
    reroute_011.socket_idname = "NodeSocketGeometry"
    # Links for reroute_011
    links.new(reroute_011.outputs[0], rotate_on_centre_1.inputs[0])
    links.new(reroute_011.outputs[0], rotate_on_centre_3.inputs[0])

    join_geometry_017 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_017.name = "Join Geometry.017"
    join_geometry_017.label = ""
    join_geometry_017.location = (6260.0, -400.0)
    join_geometry_017.bl_label = "Join Geometry"
    # Links for join_geometry_017
    links.new(join_geometry_017.outputs[0], reroute_011.inputs[0])

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = ""
    frame_002.location = (6486.16650390625, -307.1333312988281)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    rivet = nodes.new("GeometryNodeGroup")
    rivet.name = "Group.006"
    rivet.label = ""
    rivet.location = (4360.0, -400.0)
    rivet.node_tree = create_rivet_group()
    rivet.bl_label = "Group"
    # Corners
    rivet.inputs[1].default_value = False
    # Offset
    rivet.inputs[2].default_value = 0.9399999976158142
    # Spacing
    rivet.inputs[3].default_value = 0.9399999976158142
    # Links for rivet
    links.new(rivet.outputs[0], join_geometry_017.inputs[0])
    links.new(separate_geometry.outputs[0], rivet.inputs[0])

    rivet_1 = nodes.new("GeometryNodeGroup")
    rivet_1.name = "Group.007"
    rivet_1.label = ""
    rivet_1.location = (4120.0, 300.0)
    rivet_1.node_tree = create_rivet_group()
    rivet_1.bl_label = "Group"
    # Corners
    rivet_1.inputs[1].default_value = False
    # Offset
    rivet_1.inputs[2].default_value = -1.0799999237060547
    # Spacing
    rivet_1.inputs[3].default_value = 0.9399999976158142
    # Links for rivet_1
    links.new(transform_geometry_002.outputs[0], rivet_1.inputs[0])

    join_geometry_018 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_018.name = "Join Geometry.018"
    join_geometry_018.label = ""
    join_geometry_018.location = (4280.0, 340.0)
    join_geometry_018.bl_label = "Join Geometry"
    # Links for join_geometry_018
    links.new(transform_geometry_002.outputs[0], join_geometry_018.inputs[0])
    links.new(rivet_1.outputs[0], join_geometry_018.inputs[0])
    links.new(join_geometry_018.outputs[0], join_geometry_013.inputs[0])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.name = "Group.005"
    pipes.label = ""
    pipes.location = (9320.0, 400.0)
    pipes.node_tree = create_pipes_group()
    pipes.bl_label = "Group"
    # Links for pipes
    links.new(pipes.outputs[0], join_geometry_013.inputs[0])
    links.new(join_geometry_015.outputs[0], pipes.inputs[0])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (12920.0, 20.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True
    # Links for set_shade_smooth
    links.new(join_geometry_013.outputs[0], set_shade_smooth.inputs[0])

    gold_decorations = nodes.new("GeometryNodeGroup")
    gold_decorations.name = "Group.008"
    gold_decorations.label = ""
    gold_decorations.location = (1469.0, -409.0)
    gold_decorations.node_tree = create_gold__decorations_group()
    gold_decorations.bl_label = "Group"
    # Seed
    gold_decorations.inputs[1].default_value = 58
    # Scale
    gold_decorations.inputs[2].default_value = 1.5
    # Count
    gold_decorations.inputs[3].default_value = 56
    # Links for gold_decorations

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.name = "Group.003"
    gold_on_band.label = ""
    gold_on_band.location = (1860.8330078125, -924.80029296875)
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.bl_label = "Group"
    # Density
    gold_on_band.inputs[1].default_value = 200000.0
    # W
    gold_on_band.inputs[2].default_value = 8.669999122619629
    # Seed
    gold_on_band.inputs[3].default_value = 1
    # Links for gold_on_band

    subdivide_mesh = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh.name = "Subdivide Mesh"
    subdivide_mesh.label = ""
    subdivide_mesh.location = (489.0, -409.0)
    subdivide_mesh.bl_label = "Subdivide Mesh"
    # Level
    subdivide_mesh.inputs[1].default_value = 1
    # Links for subdivide_mesh

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (809.0, -409.0)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Selection
    mesh_to_curve.inputs[1].default_value = True
    # Links for mesh_to_curve

    is_edge_boundary_1 = nodes.new("GeometryNodeGroup")
    is_edge_boundary_1.name = "Is Edge Boundary"
    is_edge_boundary_1.label = ""
    is_edge_boundary_1.location = (449.0, -509.0)
    is_edge_boundary_1.node_tree = create_is__edge__boundary_group()
    is_edge_boundary_1.bl_label = "Group"
    # Links for is_edge_boundary_1

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (649.0, -409.0)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "POINT"
    # Links for delete_geometry
    links.new(delete_geometry.outputs[0], mesh_to_curve.inputs[0])
    links.new(subdivide_mesh.outputs[0], delete_geometry.inputs[0])

    reroute_013 = nodes.new("NodeReroute")
    reroute_013.name = "Reroute.013"
    reroute_013.label = ""
    reroute_013.location = (249.0, -409.0)
    reroute_013.bl_label = "Reroute"
    reroute_013.socket_idname = "NodeSocketGeometry"
    # Links for reroute_013
    links.new(reroute_013.outputs[0], subdivide_mesh.inputs[0])
    links.new(flip_faces_005.outputs[0], reroute_013.inputs[0])

    sample_nearest_surface = nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.name = "Sample Nearest Surface"
    sample_nearest_surface.label = ""
    sample_nearest_surface.location = (309.0, -29.0)
    sample_nearest_surface.bl_label = "Sample Nearest Surface"
    sample_nearest_surface.data_type = "FLOAT_VECTOR"
    # Group ID
    sample_nearest_surface.inputs[2].default_value = 0
    # Sample Position
    sample_nearest_surface.inputs[3].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    sample_nearest_surface.inputs[4].default_value = 0
    # Links for sample_nearest_surface
    links.new(reroute_013.outputs[0], sample_nearest_surface.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.label = ""
    normal.location = (309.0, -249.0)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = False
    # Links for normal
    links.new(normal.outputs[0], sample_nearest_surface.inputs[1])

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (249.0, -489.0)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (29.0, -569.0)
    position.bl_label = "Position"
    # Links for position
    links.new(position.outputs[0], separate_x_y_z.inputs[0])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (249.0, -589.0)
    compare_003.bl_label = "Compare"
    compare_003.operation = "GREATER_THAN"
    compare_003.data_type = "FLOAT"
    compare_003.mode = "ELEMENT"
    # B
    compare_003.inputs[1].default_value = 0.0
    # A
    compare_003.inputs[2].default_value = 0
    # B
    compare_003.inputs[3].default_value = 0
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
    links.new(separate_x_y_z.outputs[1], compare_003.inputs[0])

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.label = ""
    boolean_math_003.location = (649.0, -529.0)
    boolean_math_003.bl_label = "Boolean Math"
    boolean_math_003.operation = "OR"
    # Links for boolean_math_003
    links.new(is_edge_boundary_1.outputs[0], boolean_math_003.inputs[0])
    links.new(boolean_math_003.outputs[0], delete_geometry.inputs[1])
    links.new(compare_003.outputs[0], boolean_math_003.inputs[1])

    set_curve_normal_001 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.name = "Set Curve Normal.001"
    set_curve_normal_001.label = ""
    set_curve_normal_001.location = (989.0, -409.0)
    set_curve_normal_001.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_001.inputs[1].default_value = True
    # Mode
    set_curve_normal_001.inputs[2].default_value = "Free"
    # Links for set_curve_normal_001
    links.new(mesh_to_curve.outputs[0], set_curve_normal_001.inputs[0])
    links.new(sample_nearest_surface.outputs[0], set_curve_normal_001.inputs[3])

    set_curve_tilt_003 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_003.name = "Set Curve Tilt.003"
    set_curve_tilt_003.label = ""
    set_curve_tilt_003.location = (1309.0, -409.0)
    set_curve_tilt_003.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_003.inputs[1].default_value = True
    # Tilt
    set_curve_tilt_003.inputs[2].default_value = -1.5707963705062866
    # Links for set_curve_tilt_003
    links.new(set_curve_tilt_003.outputs[0], gold_decorations.inputs[0])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    transform_geometry_003.label = ""
    transform_geometry_003.location = (2169.0, -469.0)
    transform_geometry_003.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_003.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_003.inputs[4].default_value = Vector((1.0, -1.0, 1.0))
    # Links for transform_geometry_003

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.name = "Flip Faces"
    flip_faces.label = ""
    flip_faces.location = (2329.0, -469.0)
    flip_faces.bl_label = "Flip Faces"
    # Selection
    flip_faces.inputs[1].default_value = True
    # Links for flip_faces
    links.new(transform_geometry_003.outputs[0], flip_faces.inputs[0])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (2509.0, -429.0)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(flip_faces.outputs[0], join_geometry.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = ""
    frame_001.location = (407.0, -35.80029296875)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (2633.8330078125, -669.0)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(join_geometry.outputs[0], join_geometry_001.inputs[0])
    links.new(gold_on_band.outputs[0], join_geometry_001.inputs[0])

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Gold"
    frame_003.location = (6404.0, 6804.80029296875)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (2813.8330078125, -569.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(join_geometry_001.outputs[0], store_named_attribute.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (1149.0, -409.0)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Position
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position
    links.new(set_position.outputs[0], set_curve_tilt_003.inputs[0])
    links.new(set_curve_normal_001.outputs[0], set_position.inputs[0])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (989.0, -529.0)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "SCALE"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 0.0020000000949949026
    # Links for vector_math_001
    links.new(vector_math_001.outputs[0], set_position.inputs[3])

    normal_003 = nodes.new("GeometryNodeInputNormal")
    normal_003.name = "Normal.003"
    normal_003.label = ""
    normal_003.location = (809.0, -549.0)
    normal_003.bl_label = "Normal"
    normal_003.legacy_corner_normals = False
    # Links for normal_003
    links.new(normal_003.outputs[0], vector_math_001.inputs[0])

    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.label = ""
    delete_geometry_001.location = (1829.0, -389.0)
    delete_geometry_001.bl_label = "Delete Geometry"
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "POINT"
    # Links for delete_geometry_001
    links.new(delete_geometry_001.outputs[0], transform_geometry_003.inputs[0])
    links.new(delete_geometry_001.outputs[0], join_geometry.inputs[0])
    links.new(gold_decorations.outputs[0], delete_geometry_001.inputs[0])

    raycast = nodes.new("GeometryNodeRaycast")
    raycast.name = "Raycast"
    raycast.label = ""
    raycast.location = (1409.0, -29.0)
    raycast.bl_label = "Raycast"
    raycast.data_type = "FLOAT"
    # Attribute
    raycast.inputs[1].default_value = 0.0
    # Interpolation
    raycast.inputs[2].default_value = "Interpolated"
    # Ray Length
    raycast.inputs[5].default_value = 0.10000000149011612
    # Links for raycast
    links.new(reroute_013.outputs[0], raycast.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (769.0, -49.0)
    position_001.bl_label = "Position"
    # Links for position_001

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (949.0, -69.0)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "MULTIPLY_ADD"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(sample_nearest_surface.outputs[0], vector_math_002.inputs[0])
    links.new(position_001.outputs[0], vector_math_002.inputs[2])
    links.new(vector_math_002.outputs[0], raycast.inputs[3])

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.label = ""
    vector_math_007.location = (1149.0, -229.0)
    vector_math_007.bl_label = "Vector Math"
    vector_math_007.operation = "SCALE"
    # Vector
    vector_math_007.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_007.inputs[3].default_value = -1.0
    # Links for vector_math_007
    links.new(sample_nearest_surface.outputs[0], vector_math_007.inputs[0])
    links.new(vector_math_007.outputs[0], raycast.inputs[4])

    boolean_math_004 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.name = "Boolean Math.004"
    boolean_math_004.label = ""
    boolean_math_004.location = (1609.0, -29.0)
    boolean_math_004.bl_label = "Boolean Math"
    boolean_math_004.operation = "NOT"
    # Boolean
    boolean_math_004.inputs[1].default_value = False
    # Links for boolean_math_004
    links.new(raycast.outputs[0], boolean_math_004.inputs[0])
    links.new(boolean_math_004.outputs[0], delete_geometry_001.inputs[1])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (3920.0, -620.0)
    compare_004.bl_label = "Compare"
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    # B
    compare_004.inputs[1].default_value = 0.375
    # A
    compare_004.inputs[2].default_value = 0
    # B
    compare_004.inputs[3].default_value = 0
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

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (189.0, -75.79998779296875)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Links for mesh_to_curve_001
    links.new(compare_004.outputs[0], mesh_to_curve_001.inputs[1])

    evaluate_on_domain = nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.name = "Evaluate on Domain"
    evaluate_on_domain.label = ""
    evaluate_on_domain.location = (3760.0, -620.0)
    evaluate_on_domain.bl_label = "Evaluate on Domain"
    evaluate_on_domain.domain = "POINT"
    evaluate_on_domain.data_type = "FLOAT"
    # Links for evaluate_on_domain
    links.new(evaluate_on_domain.outputs[0], compare_004.inputs[0])
    links.new(repeat_output.outputs[2], evaluate_on_domain.inputs[0])

    capture_attribute_005 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_005.name = "Capture Attribute.005"
    capture_attribute_005.label = ""
    capture_attribute_005.location = (29.0, -75.79998779296875)
    capture_attribute_005.bl_label = "Capture Attribute"
    capture_attribute_005.active_index = 0
    capture_attribute_005.domain = "POINT"
    # Links for capture_attribute_005
    links.new(capture_attribute_005.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(separate_geometry.outputs[0], capture_attribute_005.inputs[0])

    normal_004 = nodes.new("GeometryNodeInputNormal")
    normal_004.name = "Normal.004"
    normal_004.label = ""
    normal_004.location = (29.0, -195.79998779296875)
    normal_004.bl_label = "Normal"
    normal_004.legacy_corner_normals = False
    # Links for normal_004
    links.new(normal_004.outputs[0], capture_attribute_005.inputs[1])

    set_curve_normal_002 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_002.name = "Set Curve Normal.002"
    set_curve_normal_002.label = ""
    set_curve_normal_002.location = (349.0, -75.79998779296875)
    set_curve_normal_002.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_002.inputs[1].default_value = True
    # Mode
    set_curve_normal_002.inputs[2].default_value = "Free"
    # Links for set_curve_normal_002
    links.new(mesh_to_curve_001.outputs[0], set_curve_normal_002.inputs[0])
    links.new(capture_attribute_005.outputs[1], set_curve_normal_002.inputs[3])

    gold_decorations_1 = nodes.new("GeometryNodeGroup")
    gold_decorations_1.name = "Group.009"
    gold_decorations_1.label = ""
    gold_decorations_1.location = (849.0, -75.79998779296875)
    gold_decorations_1.node_tree = create_gold__decorations_group()
    gold_decorations_1.bl_label = "Group"
    # Seed
    gold_decorations_1.inputs[1].default_value = 65
    # Scale
    gold_decorations_1.inputs[2].default_value = 3.0
    # Count
    gold_decorations_1.inputs[3].default_value = 19
    # Links for gold_decorations_1

    set_curve_tilt_004 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_004.name = "Set Curve Tilt.004"
    set_curve_tilt_004.label = ""
    set_curve_tilt_004.location = (509.0, -75.79998779296875)
    set_curve_tilt_004.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_004.inputs[1].default_value = True
    # Tilt
    set_curve_tilt_004.inputs[2].default_value = -1.5707963705062866
    # Links for set_curve_tilt_004
    links.new(set_curve_normal_002.outputs[0], set_curve_tilt_004.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Gold"
    frame_004.location = (4191.0, -644.2000122070312)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    capture_attribute_006 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_006.name = "Capture Attribute.006"
    capture_attribute_006.label = ""
    capture_attribute_006.location = (4680.0, -260.0)
    capture_attribute_006.bl_label = "Capture Attribute"
    capture_attribute_006.active_index = 0
    capture_attribute_006.domain = "POINT"
    # Float
    capture_attribute_006.inputs[1].default_value = True
    # Links for capture_attribute_006
    links.new(capture_attribute_006.outputs[0], join_geometry_017.inputs[0])
    links.new(separate_geometry.outputs[0], capture_attribute_006.inputs[0])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.name = "Separate Geometry.001"
    separate_geometry_001.label = ""
    separate_geometry_001.location = (8540.0, 160.0)
    separate_geometry_001.bl_label = "Separate Geometry"
    separate_geometry_001.domain = "POINT"
    # Links for separate_geometry_001
    links.new(separate_geometry_001.outputs[0], join_geometry_015.inputs[0])
    links.new(join_geometry_016.outputs[0], separate_geometry_001.inputs[0])
    links.new(capture_attribute_006.outputs[1], separate_geometry_001.inputs[1])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    transform_geometry_004.label = ""
    transform_geometry_004.location = (669.0, -75.79998779296875)
    transform_geometry_004.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_004.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_004.inputs[2].default_value = Vector((-0.0020000000949949026, 0.0, -0.004999999888241291))
    # Rotation
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_004.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_004
    links.new(transform_geometry_004.outputs[0], gold_decorations_1.inputs[0])
    links.new(set_curve_tilt_004.outputs[0], transform_geometry_004.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (849.0, -295.79998779296875)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Count"
    # Count
    resample_curve_001.inputs[3].default_value = 15
    # Length
    resample_curve_001.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_001
    links.new(transform_geometry_004.outputs[0], resample_curve_001.inputs[0])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.label = ""
    instance_on_points_001.location = (1029.0, -295.79998779296875)
    instance_on_points_001.bl_label = "Instance on Points"
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Rotation
    instance_on_points_001.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_001.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_001
    links.new(resample_curve_001.outputs[0], instance_on_points_001.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    ico_sphere.label = ""
    ico_sphere.location = (849.0, -415.79998779296875)
    ico_sphere.bl_label = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.004999999888241291
    # Subdivisions
    ico_sphere.inputs[1].default_value = 2
    # Links for ico_sphere
    links.new(ico_sphere.outputs[0], instance_on_points_001.inputs[2])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.label = ""
    realize_instances_001.location = (1189.0, -295.79998779296875)
    realize_instances_001.bl_label = "Realize Instances"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0
    # Links for realize_instances_001
    links.new(instance_on_points_001.outputs[0], realize_instances_001.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.name = "Set Shade Smooth.001"
    set_shade_smooth_001.label = ""
    set_shade_smooth_001.location = (1349.0, -295.79998779296875)
    set_shade_smooth_001.bl_label = "Set Shade Smooth"
    set_shade_smooth_001.domain = "FACE"
    # Selection
    set_shade_smooth_001.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_001.inputs[2].default_value = True
    # Links for set_shade_smooth_001
    links.new(realize_instances_001.outputs[0], set_shade_smooth_001.inputs[0])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (1509.0, -295.79998779296875)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "ruby"
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001
    links.new(set_shade_smooth_001.outputs[0], store_named_attribute_001.inputs[0])

    boolean_math_005 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.name = "Boolean Math.005"
    boolean_math_005.label = ""
    boolean_math_005.location = (669.0, -415.79998779296875)
    boolean_math_005.bl_label = "Boolean Math"
    boolean_math_005.operation = "NOT"
    # Boolean
    boolean_math_005.inputs[1].default_value = False
    # Links for boolean_math_005
    links.new(boolean_math_005.outputs[0], instance_on_points_001.inputs[1])

    endpoint_selection_004 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_004.name = "Endpoint Selection.004"
    endpoint_selection_004.label = ""
    endpoint_selection_004.location = (489.0, -415.79998779296875)
    endpoint_selection_004.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection_004.inputs[0].default_value = 1
    # End Size
    endpoint_selection_004.inputs[1].default_value = 1
    # Links for endpoint_selection_004
    links.new(endpoint_selection_004.outputs[0], boolean_math_005.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (1029.0, -75.79998779296875)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_002.inputs[3].default_value = True
    # Links for store_named_attribute_002
    links.new(gold_decorations_1.outputs[0], store_named_attribute_002.inputs[0])

    instance_on_points_002 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.name = "Instance on Points.002"
    instance_on_points_002.label = ""
    instance_on_points_002.location = (313.8330078125, -35.80029296875)
    instance_on_points_002.bl_label = "Instance on Points"
    # Selection
    instance_on_points_002.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_002.inputs[3].default_value = False
    # Instance Index
    instance_on_points_002.inputs[4].default_value = 0
    # Rotation
    instance_on_points_002.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for instance_on_points_002

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.name = "Distribute Points on Faces"
    distribute_points_on_faces.label = ""
    distribute_points_on_faces.location = (113.83349609375, -35.80029296875)
    distribute_points_on_faces.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    # Selection
    distribute_points_on_faces.inputs[1].default_value = True
    # Distance Min
    distribute_points_on_faces.inputs[2].default_value = 0.0
    # Density Max
    distribute_points_on_faces.inputs[3].default_value = 10.0
    # Density
    distribute_points_on_faces.inputs[4].default_value = 20000.0
    # Density Factor
    distribute_points_on_faces.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces.inputs[6].default_value = 0
    # Links for distribute_points_on_faces
    links.new(distribute_points_on_faces.outputs[0], instance_on_points_002.inputs[0])

    ico_sphere_002 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_002.name = "Ico Sphere.002"
    ico_sphere_002.label = ""
    ico_sphere_002.location = (29.0, -255.80029296875)
    ico_sphere_002.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_002.inputs[0].default_value = 0.0010000000474974513
    # Subdivisions
    ico_sphere_002.inputs[1].default_value = 2
    # Links for ico_sphere_002
    links.new(ico_sphere_002.outputs[0], instance_on_points_002.inputs[2])

    realize_instances_002 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.name = "Realize Instances.002"
    realize_instances_002.label = ""
    realize_instances_002.location = (473.8330078125, -35.80029296875)
    realize_instances_002.bl_label = "Realize Instances"
    # Selection
    realize_instances_002.inputs[1].default_value = True
    # Realize All
    realize_instances_002.inputs[2].default_value = True
    # Depth
    realize_instances_002.inputs[3].default_value = 0
    # Links for realize_instances_002
    links.new(instance_on_points_002.outputs[0], realize_instances_002.inputs[0])

    set_shade_smooth_002 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_002.name = "Set Shade Smooth.002"
    set_shade_smooth_002.label = ""
    set_shade_smooth_002.location = (633.8330078125, -35.80029296875)
    set_shade_smooth_002.bl_label = "Set Shade Smooth"
    set_shade_smooth_002.domain = "FACE"
    # Selection
    set_shade_smooth_002.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_002.inputs[2].default_value = True
    # Links for set_shade_smooth_002
    links.new(realize_instances_002.outputs[0], set_shade_smooth_002.inputs[0])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (793.8330078125, -35.80029296875)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "ruby"
    # Value
    store_named_attribute_003.inputs[3].default_value = True
    # Links for store_named_attribute_003
    links.new(set_shade_smooth_002.outputs[0], store_named_attribute_003.inputs[0])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.label = ""
    random_value_001.location = (209.0, -295.80029296875)
    random_value_001.bl_label = "Random Value"
    random_value_001.data_type = "FLOAT"
    # Min
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_001.inputs[2].default_value = 1.0
    # Max
    random_value_001.inputs[3].default_value = 1.5
    # Min
    random_value_001.inputs[4].default_value = 0
    # Max
    random_value_001.inputs[5].default_value = 100
    # Probability
    random_value_001.inputs[6].default_value = 0.5
    # ID
    random_value_001.inputs[7].default_value = 0
    # Seed
    random_value_001.inputs[8].default_value = 0
    # Links for random_value_001
    links.new(random_value_001.outputs[1], instance_on_points_002.inputs[6])

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = "Extra Rubies"
    frame_005.location = (1647.0, -1289.0)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (2389.0, -415.79998779296875)
    store_named_attribute_004.bl_label = "Store Named Attribute"
    store_named_attribute_004.data_type = "FLOAT2"
    store_named_attribute_004.domain = "CORNER"
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute_004
    links.new(store_named_attribute_004.outputs[0], set_position_003.inputs[0])
    links.new(curve_to_mesh.outputs[0], store_named_attribute_004.inputs[0])

    spline_parameter_004 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_004.name = "Spline Parameter.004"
    spline_parameter_004.label = ""
    spline_parameter_004.location = (1229.0, -535.7999877929688)
    spline_parameter_004.bl_label = "Spline Parameter"
    # Links for spline_parameter_004
    links.new(spline_parameter_004.outputs[0], capture_attribute_001.inputs[3])
    links.new(spline_parameter_004.outputs[0], capture_attribute.inputs[2])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (2169.0, -575.7999877929688)
    combine_x_y_z.bl_label = "Combine XYZ"
    # Z
    combine_x_y_z.inputs[2].default_value = 0.0
    # Links for combine_x_y_z
    links.new(capture_attribute_001.outputs[3], combine_x_y_z.inputs[0])
    links.new(capture_attribute.outputs[2], combine_x_y_z.inputs[1])
    links.new(combine_x_y_z.outputs[0], store_named_attribute_004.inputs[3])

    delete_geometry_002 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.name = "Delete Geometry.002"
    delete_geometry_002.label = ""
    delete_geometry_002.location = (1787.0, -1113.800048828125)
    delete_geometry_002.bl_label = "Delete Geometry"
    delete_geometry_002.mode = "ALL"
    delete_geometry_002.domain = "FACE"
    # Links for delete_geometry_002
    links.new(transform_geometry_002.outputs[0], delete_geometry_002.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (1607.0, -1293.800048828125)
    position_002.bl_label = "Position"
    # Links for position_002

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (1607.0, -1353.800048828125)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001
    links.new(position_002.outputs[0], separate_x_y_z_001.inputs[0])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (1767.0, -1293.800048828125)
    compare_005.bl_label = "Compare"
    compare_005.operation = "GREATER_THAN"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    # B
    compare_005.inputs[1].default_value = 0.0
    # A
    compare_005.inputs[2].default_value = 0
    # B
    compare_005.inputs[3].default_value = 0
    # A
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_005.inputs[8].default_value = ""
    # B
    compare_005.inputs[9].default_value = ""
    # C
    compare_005.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_005.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_005.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_005
    links.new(separate_x_y_z_001.outputs[1], compare_005.inputs[0])
    links.new(compare_005.outputs[0], delete_geometry_002.inputs[1])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (1467.0, -1493.800048828125)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "FLOAT_VECTOR"
    # Name
    named_attribute.inputs[0].default_value = "UVMap"
    # Links for named_attribute

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.name = "Group.010"
    gem_in_holder.label = ""
    gem_in_holder.location = (229.0, -369.0)
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.bl_label = "Group"
    # Gem Radius
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder.inputs[2].default_value = True
    # Scale
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder.inputs[4].default_value = 20
    # Seed
    gem_in_holder.inputs[5].default_value = 15
    # Wings
    gem_in_holder.inputs[6].default_value = True
    # Array Count
    gem_in_holder.inputs[7].default_value = 4
    # Strand Count
    gem_in_holder.inputs[8].default_value = 5
    # Split
    gem_in_holder.inputs[9].default_value = 1.0
    # Seed
    gem_in_holder.inputs[10].default_value = 3.179999589920044
    # Links for gem_in_holder

    gem_in_holder_1 = nodes.new("GeometryNodeGroup")
    gem_in_holder_1.name = "Group.011"
    gem_in_holder_1.label = ""
    gem_in_holder_1.location = (229.0, -29.0)
    gem_in_holder_1.node_tree = create_gem_in__holder_group()
    gem_in_holder_1.bl_label = "Group"
    # Gem Radius
    gem_in_holder_1.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_1.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_1.inputs[2].default_value = False
    # Scale
    gem_in_holder_1.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_1.inputs[4].default_value = 20
    # Seed
    gem_in_holder_1.inputs[5].default_value = 10
    # Wings
    gem_in_holder_1.inputs[6].default_value = True
    # Strand Count
    gem_in_holder_1.inputs[8].default_value = 5
    # Split
    gem_in_holder_1.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder_1.inputs[10].default_value = 2.609999656677246
    # Links for gem_in_holder_1

    gem_in_holder_2 = nodes.new("GeometryNodeGroup")
    gem_in_holder_2.name = "Group.012"
    gem_in_holder_2.label = ""
    gem_in_holder_2.location = (29.0, -29.0)
    gem_in_holder_2.node_tree = create_gem_in__holder_group()
    gem_in_holder_2.bl_label = "Group"
    # Gem Radius
    gem_in_holder_2.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_2.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_2.inputs[2].default_value = True
    # Scale
    gem_in_holder_2.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_2.inputs[4].default_value = 20
    # Seed
    gem_in_holder_2.inputs[5].default_value = 15
    # Wings
    gem_in_holder_2.inputs[6].default_value = True
    # Array Count
    gem_in_holder_2.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_2.inputs[8].default_value = 10
    # Split
    gem_in_holder_2.inputs[9].default_value = 1.0
    # Seed
    gem_in_holder_2.inputs[10].default_value = 2.7799999713897705
    # Links for gem_in_holder_2

    instance_on_points_003 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.name = "Instance on Points.003"
    instance_on_points_003.label = ""
    instance_on_points_003.location = (709.0, -189.0)
    instance_on_points_003.bl_label = "Instance on Points"
    # Selection
    instance_on_points_003.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_003.inputs[3].default_value = False
    # Instance Index
    instance_on_points_003.inputs[4].default_value = 0
    # Scale
    instance_on_points_003.inputs[6].default_value = Vector((0.5, 0.5, 0.5))
    # Links for instance_on_points_003
    links.new(gem_in_holder.outputs[0], instance_on_points_003.inputs[2])

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (529.0, -189.0)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle.inputs[4].default_value = 0.029999999329447746
    # Links for curve_circle
    links.new(curve_circle.outputs[0], instance_on_points_003.inputs[0])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (709.0, -149.0)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002
    links.new(instance_on_points_003.outputs[0], join_geometry_002.inputs[0])
    links.new(gem_in_holder_1.outputs[0], join_geometry_002.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.label = ""
    transform_geometry_005.location = (269.0, -29.0)
    transform_geometry_005.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_005.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_005.inputs[2].default_value = Vector((-0.07999999821186066, 0.0, 0.0))
    # Rotation
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_005
    links.new(gem_in_holder_2.outputs[0], transform_geometry_005.inputs[0])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (1198.0, -558.0)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003
    links.new(transform_geometry_005.outputs[0], join_geometry_003.inputs[0])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.name = "Transform Geometry.006"
    transform_geometry_006.label = ""
    transform_geometry_006.location = (869.0, -149.0)
    transform_geometry_006.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_006.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_006.inputs[2].default_value = Vector((0.07999999821186066, 0.0, 0.0))
    # Rotation
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_006.inputs[4].default_value = Vector((0.699999988079071, 0.699999988079071, 0.699999988079071))
    # Links for transform_geometry_006
    links.new(transform_geometry_006.outputs[0], join_geometry_003.inputs[0])
    links.new(join_geometry_002.outputs[0], transform_geometry_006.inputs[0])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (529.0, -329.0)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent

    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.name = "Align Rotation to Vector.002"
    align_rotation_to_vector_002.label = ""
    align_rotation_to_vector_002.location = (529.0, -389.0)
    align_rotation_to_vector_002.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_002.axis = "X"
    align_rotation_to_vector_002.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_002.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_002.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_002
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_002.inputs[2])
    links.new(align_rotation_to_vector_002.outputs[0], instance_on_points_003.inputs[5])

    integer = nodes.new("FunctionNodeInputInt")
    integer.name = "Integer"
    integer.label = ""
    integer.location = (29.0, -149.0)
    integer.bl_label = "Integer"
    integer.integer = 5
    # Links for integer
    links.new(integer.outputs[0], gem_in_holder_1.inputs[7])
    links.new(integer.outputs[0], curve_circle.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = ""
    frame_006.location = (29.0, -29.0)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    frame_007 = nodes.new("NodeFrame")
    frame_007.name = "Frame.007"
    frame_007.label = ""
    frame_007.location = (629.0, -769.0)
    frame_007.bl_label = "Frame"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20
    # Links for frame_007

    frame_008 = nodes.new("NodeFrame")
    frame_008.name = "Frame.008"
    frame_008.label = ""
    frame_008.location = (29.0, -35.800048828125)
    frame_008.bl_label = "Frame"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20
    # Links for frame_008

    realize_instances_003 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.name = "Realize Instances.003"
    realize_instances_003.label = ""
    realize_instances_003.location = (1198.0, -618.0)
    realize_instances_003.bl_label = "Realize Instances"
    # Selection
    realize_instances_003.inputs[1].default_value = True
    # Realize All
    realize_instances_003.inputs[2].default_value = True
    # Depth
    realize_instances_003.inputs[3].default_value = 0
    # Links for realize_instances_003
    links.new(join_geometry_003.outputs[0], realize_instances_003.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    bounding_box.label = ""
    bounding_box.location = (1687.0, -653.800048828125)
    bounding_box.bl_label = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = False
    # Links for bounding_box
    links.new(realize_instances_003.outputs[0], bounding_box.inputs[0])

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (1687.0, -573.800048828125)
    position_003.bl_label = "Position"
    # Links for position_003

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (1867.0, -573.800048828125)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT_VECTOR"
    # Value
    map_range.inputs[0].default_value = 1.0
    # From Min
    map_range.inputs[1].default_value = 0.0
    # From Max
    map_range.inputs[2].default_value = 1.0
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0
    # Steps
    map_range.inputs[5].default_value = 4.0
    # To Min
    map_range.inputs[9].default_value = [0.009999999776482582, 0.05000000074505806, 0.009999999776482582]
    # To Max
    map_range.inputs[10].default_value = [0.9800000190734863, 0.949999988079071, 0.9990000128746033]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(position_003.outputs[0], map_range.inputs[6])
    links.new(bounding_box.outputs[1], map_range.inputs[7])
    links.new(bounding_box.outputs[2], map_range.inputs[8])

    sample_u_v_surface = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface.name = "Sample UV Surface"
    sample_u_v_surface.label = ""
    sample_u_v_surface.location = (2287.0, -913.800048828125)
    sample_u_v_surface.bl_label = "Sample UV Surface"
    sample_u_v_surface.data_type = "FLOAT_VECTOR"
    # Links for sample_u_v_surface
    links.new(delete_geometry_002.outputs[0], sample_u_v_surface.inputs[0])
    links.new(map_range.outputs[1], sample_u_v_surface.inputs[3])

    position_005 = nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"
    position_005.label = ""
    position_005.location = (2287.0, -853.800048828125)
    position_005.bl_label = "Position"
    # Links for position_005
    links.new(position_005.outputs[0], sample_u_v_surface.inputs[1])

    sample_u_v_surface_001 = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface_001.name = "Sample UV Surface.001"
    sample_u_v_surface_001.label = ""
    sample_u_v_surface_001.location = (2467.0, -993.800048828125)
    sample_u_v_surface_001.bl_label = "Sample UV Surface"
    sample_u_v_surface_001.data_type = "FLOAT_VECTOR"
    # Links for sample_u_v_surface_001
    links.new(delete_geometry_002.outputs[0], sample_u_v_surface_001.inputs[0])
    links.new(map_range.outputs[1], sample_u_v_surface_001.inputs[3])

    normal_005 = nodes.new("GeometryNodeInputNormal")
    normal_005.name = "Normal.005"
    normal_005.label = ""
    normal_005.location = (2467.0, -933.800048828125)
    normal_005.bl_label = "Normal"
    normal_005.legacy_corner_normals = False
    # Links for normal_005
    links.new(normal_005.outputs[0], sample_u_v_surface_001.inputs[1])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (2807.0, -593.800048828125)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Links for set_position_001
    links.new(realize_instances_003.outputs[0], set_position_001.inputs[0])
    links.new(sample_u_v_surface.outputs[0], set_position_001.inputs[2])

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_002.name = "Separate XYZ.002"
    separate_x_y_z_002.label = ""
    separate_x_y_z_002.location = (1627.0, -1493.800048828125)
    separate_x_y_z_002.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_002
    links.new(named_attribute.outputs[0], separate_x_y_z_002.inputs[0])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (2107.0, -1473.800048828125)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # Z
    combine_x_y_z_001.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_001
    links.new(combine_x_y_z_001.outputs[0], sample_u_v_surface.inputs[2])
    links.new(combine_x_y_z_001.outputs[0], sample_u_v_surface_001.inputs[2])
    links.new(separate_x_y_z_002.outputs[1], combine_x_y_z_001.inputs[1])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (1827.0, -1513.800048828125)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(float_curve.outputs[0], combine_x_y_z_001.inputs[0])
    links.new(separate_x_y_z_002.outputs[0], float_curve.inputs[1])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.label = ""
    vector_math_008.location = (2647.0, -933.800048828125)
    vector_math_008.bl_label = "Vector Math"
    vector_math_008.operation = "SCALE"
    # Vector
    vector_math_008.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_008
    links.new(sample_u_v_surface_001.outputs[0], vector_math_008.inputs[0])
    links.new(vector_math_008.outputs[0], set_position_001.inputs[3])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_003.name = "Separate XYZ.003"
    separate_x_y_z_003.label = ""
    separate_x_y_z_003.location = (2287.0, -693.800048828125)
    separate_x_y_z_003.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_003
    links.new(map_range.outputs[1], separate_x_y_z_003.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (2467.0, -693.800048828125)
    math.bl_label = "Math"
    math.operation = "MULTIPLY"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.009999999776482582
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(separate_x_y_z_003.outputs[2], math.inputs[0])
    links.new(math.outputs[0], vector_math_008.inputs[3])

    frame_009 = nodes.new("NodeFrame")
    frame_009.name = "Frame.009"
    frame_009.label = "Broaches"
    frame_009.location = (29.0, -3391.000244140625)
    frame_009.bl_label = "Frame"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20
    # Links for frame_009

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.name = "Transform Geometry.007"
    transform_geometry_007.label = ""
    transform_geometry_007.location = (3007.0, -673.800048828125)
    transform_geometry_007.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_007.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_007.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_007.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_007.inputs[4].default_value = Vector((1.0, -1.0, 1.0))
    # Links for transform_geometry_007
    links.new(set_position_001.outputs[0], transform_geometry_007.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.name = "Flip Faces.001"
    flip_faces_001.label = ""
    flip_faces_001.location = (3187.0, -673.800048828125)
    flip_faces_001.bl_label = "Flip Faces"
    # Selection
    flip_faces_001.inputs[1].default_value = True
    # Links for flip_faces_001
    links.new(transform_geometry_007.outputs[0], flip_faces_001.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (3367.0, -593.800048828125)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(flip_faces_001.outputs[0], join_geometry_004.inputs[0])
    links.new(set_position_001.outputs[0], join_geometry_004.inputs[0])

    gem_in_holder_3 = nodes.new("GeometryNodeGroup")
    gem_in_holder_3.name = "Group.013"
    gem_in_holder_3.label = ""
    gem_in_holder_3.location = (29.0, -29.0)
    gem_in_holder_3.node_tree = create_gem_in__holder_group()
    gem_in_holder_3.bl_label = "Group"
    # Gem Radius
    gem_in_holder_3.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_3.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_3.inputs[2].default_value = True
    # Scale
    gem_in_holder_3.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_3.inputs[4].default_value = 20
    # Seed
    gem_in_holder_3.inputs[5].default_value = 15
    # Wings
    gem_in_holder_3.inputs[6].default_value = True
    # Array Count
    gem_in_holder_3.inputs[7].default_value = 5
    # Strand Count
    gem_in_holder_3.inputs[8].default_value = 10
    # Split
    gem_in_holder_3.inputs[9].default_value = 0.004999999888241291
    # Seed
    gem_in_holder_3.inputs[10].default_value = 23.56599998474121
    # Links for gem_in_holder_3

    transform_geometry_008 = nodes.new("GeometryNodeTransform")
    transform_geometry_008.name = "Transform Geometry.008"
    transform_geometry_008.label = ""
    transform_geometry_008.location = (269.0, -29.0)
    transform_geometry_008.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_008.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_008.inputs[2].default_value = Vector((0.009999999776482582, 0.0, 0.0))
    # Rotation
    transform_geometry_008.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_008.inputs[4].default_value = Vector((1.2000000476837158, 1.2000000476837158, 1.2000000476837158))
    # Links for transform_geometry_008
    links.new(gem_in_holder_3.outputs[0], transform_geometry_008.inputs[0])
    links.new(transform_geometry_008.outputs[0], join_geometry_003.inputs[0])

    frame_010 = nodes.new("NodeFrame")
    frame_010.name = "Frame.010"
    frame_010.label = ""
    frame_010.location = (629.0, -1169.0)
    frame_010.bl_label = "Frame"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20
    # Links for frame_010

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (229.166015625, -115.80029296875)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Links for switch_001

    join_geometry_019 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_019.name = "Join Geometry.019"
    join_geometry_019.label = ""
    join_geometry_019.location = (29.166015625, -195.80029296875)
    join_geometry_019.bl_label = "Join Geometry"
    # Links for join_geometry_019
    links.new(join_geometry_004.outputs[0], join_geometry_019.inputs[0])
    links.new(store_named_attribute_003.outputs[0], join_geometry_019.inputs[0])
    links.new(store_named_attribute.outputs[0], join_geometry_019.inputs[0])
    links.new(join_geometry_019.outputs[0], switch_001.inputs[2])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (84.3330078125, -35.80029296875)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch_001.inputs[0])

    frame_011 = nodes.new("NodeFrame")
    frame_011.name = "Frame.011"
    frame_011.label = "Decor"
    frame_011.location = (5791.6669921875, -2229.0)
    frame_011.bl_label = "Frame"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20
    # Links for frame_011

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.label = ""
    switch_002.location = (1929.0, -115.79998779296875)
    switch_002.bl_label = "Switch"
    switch_002.input_type = "GEOMETRY"
    # Links for switch_002
    links.new(switch_002.outputs[0], join_geometry_017.inputs[0])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (1929.0, -35.79998779296875)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[0], switch_002.inputs[0])

    join_geometry_020 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_020.name = "Join Geometry.020"
    join_geometry_020.label = ""
    join_geometry_020.location = (1729.0, -115.79998779296875)
    join_geometry_020.bl_label = "Join Geometry"
    # Links for join_geometry_020
    links.new(store_named_attribute_002.outputs[0], join_geometry_020.inputs[0])
    links.new(store_named_attribute_001.outputs[0], join_geometry_020.inputs[0])
    links.new(join_geometry_020.outputs[0], switch_002.inputs[2])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.name = "Separate Geometry.002"
    separate_geometry_002.label = ""
    separate_geometry_002.location = (738.0, -29.0)
    separate_geometry_002.bl_label = "Separate Geometry"
    separate_geometry_002.domain = "POINT"
    # Links for separate_geometry_002
    links.new(repeat_output.outputs[0], separate_geometry_002.inputs[0])

    compare_006 = nodes.new("FunctionNodeCompare")
    compare_006.name = "Compare.006"
    compare_006.label = ""
    compare_006.location = (418.0, -29.0)
    compare_006.bl_label = "Compare"
    compare_006.operation = "EQUAL"
    compare_006.data_type = "FLOAT"
    compare_006.mode = "ELEMENT"
    # B
    compare_006.inputs[1].default_value = 0.4000000059604645
    # A
    compare_006.inputs[2].default_value = 0
    # B
    compare_006.inputs[3].default_value = 0
    # A
    compare_006.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_006.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_006.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_006.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_006.inputs[8].default_value = ""
    # B
    compare_006.inputs[9].default_value = ""
    # C
    compare_006.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_006.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_006.inputs[12].default_value = 0.3009999990463257
    # Links for compare_006
    links.new(repeat_output.outputs[2], compare_006.inputs[0])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.label = ""
    named_attribute_001.location = (58.0, -209.0)
    named_attribute_001.bl_label = "Named Attribute"
    named_attribute_001.data_type = "FLOAT_VECTOR"
    # Name
    named_attribute_001.inputs[0].default_value = "UVMap"
    # Links for named_attribute_001

    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_004.name = "Separate XYZ.004"
    separate_x_y_z_004.label = ""
    separate_x_y_z_004.location = (238.0, -209.0)
    separate_x_y_z_004.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_004
    links.new(named_attribute_001.outputs[0], separate_x_y_z_004.inputs[0])

    compare_007 = nodes.new("FunctionNodeCompare")
    compare_007.name = "Compare.007"
    compare_007.label = ""
    compare_007.location = (418.0, -209.0)
    compare_007.bl_label = "Compare"
    compare_007.operation = "EQUAL"
    compare_007.data_type = "FLOAT"
    compare_007.mode = "ELEMENT"
    # B
    compare_007.inputs[1].default_value = 0.0
    # A
    compare_007.inputs[2].default_value = 0
    # B
    compare_007.inputs[3].default_value = 0
    # A
    compare_007.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_007.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_007.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_007.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_007.inputs[8].default_value = ""
    # B
    compare_007.inputs[9].default_value = ""
    # C
    compare_007.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_007.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_007.inputs[12].default_value = 0.5199999809265137
    # Links for compare_007
    links.new(separate_x_y_z_004.outputs[0], compare_007.inputs[0])

    boolean_math_006 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_006.name = "Boolean Math.006"
    boolean_math_006.label = ""
    boolean_math_006.location = (578.0, -29.0)
    boolean_math_006.bl_label = "Boolean Math"
    boolean_math_006.operation = "AND"
    # Links for boolean_math_006
    links.new(compare_006.outputs[0], boolean_math_006.inputs[0])
    links.new(compare_007.outputs[0], boolean_math_006.inputs[1])
    links.new(boolean_math_006.outputs[0], separate_geometry_002.inputs[1])

    frame_012 = nodes.new("NodeFrame")
    frame_012.name = "Frame.012"
    frame_012.label = ""
    frame_012.location = (98.0, -1035.80029296875)
    frame_012.bl_label = "Frame"
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20
    # Links for frame_012

    gem_in_holder_4 = nodes.new("GeometryNodeGroup")
    gem_in_holder_4.name = "Gem in Holder.001"
    gem_in_holder_4.label = ""
    gem_in_holder_4.location = (949.0, -75.80029296875)
    gem_in_holder_4.node_tree = create_gem_in__holder_group()
    gem_in_holder_4.bl_label = "Group"
    # Gem Radius
    gem_in_holder_4.inputs[0].default_value = 0.009999990463256836
    # Gem Material
    gem_in_holder_4.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_4.inputs[2].default_value = False
    # Scale
    gem_in_holder_4.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_4.inputs[4].default_value = 20
    # Seed
    gem_in_holder_4.inputs[5].default_value = 10
    # Wings
    gem_in_holder_4.inputs[6].default_value = False
    # Array Count
    gem_in_holder_4.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_4.inputs[8].default_value = 10
    # Links for gem_in_holder_4

    position_006 = nodes.new("GeometryNodeInputPosition")
    position_006.name = "Position.006"
    position_006.label = ""
    position_006.location = (409.0, -255.80029296875)
    position_006.bl_label = "Position"
    # Links for position_006

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.name = "For Each Geometry Element Input.001"
    for_each_geometry_element_input_001.label = ""
    for_each_geometry_element_input_001.location = (569.0, -55.80029296875)
    for_each_geometry_element_input_001.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input_001.inputs[1].default_value = True
    # Links for for_each_geometry_element_input_001
    links.new(position_006.outputs[0], for_each_geometry_element_input_001.inputs[2])

    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.name = "For Each Geometry Element Output.001"
    for_each_geometry_element_output_001.label = ""
    for_each_geometry_element_output_001.location = (2109.0, -75.80029296875)
    for_each_geometry_element_output_001.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    # Links for for_each_geometry_element_output_001
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_019.inputs[0])

    transform_geometry_009 = nodes.new("GeometryNodeTransform")
    transform_geometry_009.name = "Transform Geometry.009"
    transform_geometry_009.label = ""
    transform_geometry_009.location = (1209.0, -75.80029296875)
    transform_geometry_009.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_009.inputs[1].default_value = "Components"
    # Scale
    transform_geometry_009.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_009
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_009.inputs[2])
    links.new(gem_in_holder_4.outputs[4], transform_geometry_009.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.name = "Rotate Rotation.002"
    rotate_rotation_002.label = ""
    rotate_rotation_002.location = (569.0, -315.80029296875)
    rotate_rotation_002.bl_label = "Rotate Rotation"
    rotate_rotation_002.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, 0.0, -1.3229594230651855), 'XYZ')
    # Links for rotate_rotation_002
    links.new(rotate_rotation_002.outputs[0], transform_geometry_009.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[3], rotate_rotation_002.inputs[0])

    frame_016 = nodes.new("NodeFrame")
    frame_016.name = "Frame.016"
    frame_016.label = "Random Wings"
    frame_016.location = (1287.0, -1849.0)
    frame_016.bl_label = "Frame"
    frame_016.text = None
    frame_016.shrink = True
    frame_016.label_size = 20
    # Links for frame_016

    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.name = "Random Value.007"
    random_value_007.label = ""
    random_value_007.location = (769.0, -75.80029296875)
    random_value_007.bl_label = "Random Value"
    random_value_007.data_type = "FLOAT"
    # Min
    random_value_007.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_007.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_007.inputs[2].default_value = 6.0
    # Max
    random_value_007.inputs[3].default_value = 8.0
    # Min
    random_value_007.inputs[4].default_value = 0
    # Max
    random_value_007.inputs[5].default_value = 100
    # Probability
    random_value_007.inputs[6].default_value = 0.5
    # Seed
    random_value_007.inputs[8].default_value = 48
    # Links for random_value_007
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_4.inputs[10])

    random_value_008 = nodes.new("FunctionNodeRandomValue")
    random_value_008.name = "Random Value.008"
    random_value_008.label = ""
    random_value_008.location = (769.0, -255.80029296875)
    random_value_008.bl_label = "Random Value"
    random_value_008.data_type = "FLOAT"
    # Min
    random_value_008.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_008.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_008.inputs[2].default_value = 0.0
    # Max
    random_value_008.inputs[3].default_value = 0.003000000026077032
    # Min
    random_value_008.inputs[4].default_value = 0
    # Max
    random_value_008.inputs[5].default_value = 100
    # Probability
    random_value_008.inputs[6].default_value = 0.5
    # Seed
    random_value_008.inputs[8].default_value = 10
    # Links for random_value_008
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_008.inputs[7])
    links.new(random_value_008.outputs[1], gem_in_holder_4.inputs[9])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (1589.0, -75.80029296875)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Offset
    set_position_002.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_002

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.label = ""
    geometry_proximity_001.location = (1589.0, -255.80029296875)
    geometry_proximity_001.bl_label = "Geometry Proximity"
    geometry_proximity_001.target_element = "FACES"
    # Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0
    # Links for geometry_proximity_001
    links.new(geometry_proximity_001.outputs[0], set_position_002.inputs[2])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (1749.0, -75.80029296875)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002
    links.new(set_position_002.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(gem_in_holder_4.outputs[1], curve_to_mesh_002.inputs[1])
    links.new(gem_in_holder_4.outputs[2], curve_to_mesh_002.inputs[2])

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.label = ""
    reroute_003.location = (716.0, -2084.80029296875)
    reroute_003.bl_label = "Reroute"
    reroute_003.socket_idname = "NodeSocketGeometry"
    # Links for reroute_003
    links.new(transform_geometry_002.outputs[0], reroute_003.inputs[0])
    links.new(reroute_003.outputs[0], geometry_proximity_001.inputs[0])

    reroute_012 = nodes.new("NodeReroute")
    reroute_012.name = "Reroute.012"
    reroute_012.label = ""
    reroute_012.location = (309.0, -75.80029296875)
    reroute_012.bl_label = "Reroute"
    reroute_012.socket_idname = "NodeSocketGeometry"
    # Links for reroute_012
    links.new(reroute_003.outputs[0], reroute_012.inputs[0])

    distribute_points_on_faces_001 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_001.name = "Distribute Points on Faces.001"
    distribute_points_on_faces_001.label = ""
    distribute_points_on_faces_001.location = (549.0, -35.80029296875)
    distribute_points_on_faces_001.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces_001.distribute_method = "POISSON"
    distribute_points_on_faces_001.use_legacy_normal = False
    # Distance Min
    distribute_points_on_faces_001.inputs[2].default_value = 0.009999999776482582
    # Density Max
    distribute_points_on_faces_001.inputs[3].default_value = 5000.0
    # Density
    distribute_points_on_faces_001.inputs[4].default_value = 500.0
    # Density Factor
    distribute_points_on_faces_001.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces_001.inputs[6].default_value = 0
    # Links for distribute_points_on_faces_001
    links.new(reroute_012.outputs[0], distribute_points_on_faces_001.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (29.0, -175.80029296875)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "POINTS"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity
    links.new(for_each_geometry_element_output_001.outputs[2], geometry_proximity.inputs[0])

    compare_008 = nodes.new("FunctionNodeCompare")
    compare_008.name = "Compare.008"
    compare_008.label = ""
    compare_008.location = (189.0, -175.80029296875)
    compare_008.bl_label = "Compare"
    compare_008.operation = "LESS_THAN"
    compare_008.data_type = "FLOAT"
    compare_008.mode = "ELEMENT"
    # B
    compare_008.inputs[1].default_value = 0.0020000000949949026
    # A
    compare_008.inputs[2].default_value = 0
    # B
    compare_008.inputs[3].default_value = 0
    # A
    compare_008.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_008.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_008.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_008.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_008.inputs[8].default_value = ""
    # B
    compare_008.inputs[9].default_value = ""
    # C
    compare_008.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_008.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_008.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_008
    links.new(geometry_proximity.outputs[1], compare_008.inputs[0])

    gem_in_holder_5 = nodes.new("GeometryNodeGroup")
    gem_in_holder_5.name = "Gem in Holder.002"
    gem_in_holder_5.label = ""
    gem_in_holder_5.location = (549.0, -455.80029296875)
    gem_in_holder_5.node_tree = create_gem_in__holder_group()
    gem_in_holder_5.bl_label = "Group"
    # Gem Radius
    gem_in_holder_5.inputs[0].default_value = 0.00800000037997961
    # Gem Material
    gem_in_holder_5.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_5.inputs[2].default_value = False
    # Scale
    gem_in_holder_5.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_5.inputs[4].default_value = 20
    # Seed
    gem_in_holder_5.inputs[5].default_value = 10
    # Wings
    gem_in_holder_5.inputs[6].default_value = False
    # Array Count
    gem_in_holder_5.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_5.inputs[8].default_value = 10
    # Split
    gem_in_holder_5.inputs[9].default_value = 0.0010000000474974513
    # Seed
    gem_in_holder_5.inputs[10].default_value = 6.6099958419799805
    # Links for gem_in_holder_5

    instance_on_points_004 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_004.name = "Instance on Points.004"
    instance_on_points_004.label = ""
    instance_on_points_004.location = (809.0, -75.80029296875)
    instance_on_points_004.bl_label = "Instance on Points"
    # Selection
    instance_on_points_004.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_004.inputs[3].default_value = False
    # Instance Index
    instance_on_points_004.inputs[4].default_value = 0
    # Links for instance_on_points_004
    links.new(distribute_points_on_faces_001.outputs[0], instance_on_points_004.inputs[0])
    links.new(distribute_points_on_faces_001.outputs[2], instance_on_points_004.inputs[5])

    random_value_010 = nodes.new("FunctionNodeRandomValue")
    random_value_010.name = "Random Value.010"
    random_value_010.label = ""
    random_value_010.location = (789.0, -275.80029296875)
    random_value_010.bl_label = "Random Value"
    random_value_010.data_type = "FLOAT"
    # Min
    random_value_010.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_010.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_010.inputs[2].default_value = 0.10000000894069672
    # Max
    random_value_010.inputs[3].default_value = 0.5
    # Min
    random_value_010.inputs[4].default_value = 0
    # Max
    random_value_010.inputs[5].default_value = 100
    # Probability
    random_value_010.inputs[6].default_value = 0.5
    # ID
    random_value_010.inputs[7].default_value = 0
    # Seed
    random_value_010.inputs[8].default_value = 0
    # Links for random_value_010
    links.new(random_value_010.outputs[1], instance_on_points_004.inputs[6])

    frame_017 = nodes.new("NodeFrame")
    frame_017.name = "Frame.017"
    frame_017.label = "Larger Jewels"
    frame_017.location = (3787.0, -2389.0)
    frame_017.bl_label = "Frame"
    frame_017.text = None
    frame_017.shrink = True
    frame_017.label_size = 20
    # Links for frame_017

    realize_instances_004 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_004.name = "Realize Instances.004"
    realize_instances_004.label = ""
    realize_instances_004.location = (1149.0, -75.80029296875)
    realize_instances_004.bl_label = "Realize Instances"
    # Selection
    realize_instances_004.inputs[1].default_value = True
    # Realize All
    realize_instances_004.inputs[2].default_value = True
    # Depth
    realize_instances_004.inputs[3].default_value = 0
    # Links for realize_instances_004

    transform_geometry_010 = nodes.new("GeometryNodeTransform")
    transform_geometry_010.name = "Transform Geometry.010"
    transform_geometry_010.label = ""
    transform_geometry_010.location = (789.0, -455.80029296875)
    transform_geometry_010.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_010.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_010.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    # Rotation
    transform_geometry_010.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_010.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_010
    links.new(transform_geometry_010.outputs[0], instance_on_points_004.inputs[2])
    links.new(gem_in_holder_5.outputs[0], transform_geometry_010.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.name = "Group.014"
    swap_attr.label = ""
    swap_attr.location = (1309.0, -75.80029296875)
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.bl_label = "Group"
    # Old
    swap_attr.inputs[2].default_value = "ruby"
    # New
    swap_attr.inputs[3].default_value = "saphire"
    # Links for swap_attr
    links.new(realize_instances_004.outputs[0], swap_attr.inputs[0])
    links.new(swap_attr.outputs[0], join_geometry_019.inputs[0])

    capture_attribute_008 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_008.name = "Capture Attribute.008"
    capture_attribute_008.label = ""
    capture_attribute_008.location = (989.0, -75.80029296875)
    capture_attribute_008.bl_label = "Capture Attribute"
    capture_attribute_008.active_index = 0
    capture_attribute_008.domain = "INSTANCE"
    # Links for capture_attribute_008
    links.new(capture_attribute_008.outputs[0], realize_instances_004.inputs[0])
    links.new(instance_on_points_004.outputs[0], capture_attribute_008.inputs[0])
    links.new(capture_attribute_008.outputs[1], swap_attr.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (949.0, -195.80029296875)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], capture_attribute_008.inputs[1])

    join_geometry_021 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_021.name = "Join Geometry.021"
    join_geometry_021.label = ""
    join_geometry_021.location = (13480.0, 0.0)
    join_geometry_021.bl_label = "Join Geometry"
    # Links for join_geometry_021
    links.new(join_geometry_021.outputs[0], rotate_on_centre.inputs[0])
    links.new(set_shade_smooth.outputs[0], join_geometry_021.inputs[0])
    links.new(switch_001.outputs[0], join_geometry_021.inputs[0])

    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.name = "Store Named Attribute.005"
    store_named_attribute_005.label = ""
    store_named_attribute_005.location = (1929.0, -75.80029296875)
    store_named_attribute_005.bl_label = "Store Named Attribute"
    store_named_attribute_005.data_type = "BOOLEAN"
    store_named_attribute_005.domain = "POINT"
    # Selection
    store_named_attribute_005.inputs[1].default_value = True
    # Name
    store_named_attribute_005.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_005.inputs[3].default_value = True
    # Links for store_named_attribute_005
    links.new(store_named_attribute_005.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute_005.inputs[0])

    distribute_points_on_faces_002 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_002.name = "Distribute Points on Faces.002"
    distribute_points_on_faces_002.label = ""
    distribute_points_on_faces_002.location = (29.0, -35.80029296875)
    distribute_points_on_faces_002.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces_002.distribute_method = "RANDOM"
    distribute_points_on_faces_002.use_legacy_normal = False
    # Selection
    distribute_points_on_faces_002.inputs[1].default_value = True
    # Distance Min
    distribute_points_on_faces_002.inputs[2].default_value = 0.0
    # Density Max
    distribute_points_on_faces_002.inputs[3].default_value = 10.0
    # Density
    distribute_points_on_faces_002.inputs[4].default_value = 8000.0
    # Density Factor
    distribute_points_on_faces_002.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces_002.inputs[6].default_value = 2
    # Links for distribute_points_on_faces_002
    links.new(distribute_points_on_faces_002.outputs[2], for_each_geometry_element_input_001.inputs[3])

    delete_geometry_003 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_003.name = "Delete Geometry.003"
    delete_geometry_003.label = ""
    delete_geometry_003.location = (269.0, -35.80029296875)
    delete_geometry_003.bl_label = "Delete Geometry"
    delete_geometry_003.mode = "ALL"
    delete_geometry_003.domain = "POINT"
    # Links for delete_geometry_003
    links.new(delete_geometry_003.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(distribute_points_on_faces_002.outputs[0], delete_geometry_003.inputs[0])

    geometry_proximity_002 = nodes.new("GeometryNodeProximity")
    geometry_proximity_002.name = "Geometry Proximity.002"
    geometry_proximity_002.label = ""
    geometry_proximity_002.location = (29.0, -315.80029296875)
    geometry_proximity_002.bl_label = "Geometry Proximity"
    geometry_proximity_002.target_element = "FACES"
    # Group ID
    geometry_proximity_002.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_002.inputs[3].default_value = 0
    # Links for geometry_proximity_002
    links.new(join_geometry_004.outputs[0], geometry_proximity_002.inputs[0])

    compare_009 = nodes.new("FunctionNodeCompare")
    compare_009.name = "Compare.009"
    compare_009.label = ""
    compare_009.location = (189.0, -315.80029296875)
    compare_009.bl_label = "Compare"
    compare_009.operation = "LESS_THAN"
    compare_009.data_type = "FLOAT"
    compare_009.mode = "ELEMENT"
    # B
    compare_009.inputs[1].default_value = 0.004999999888241291
    # A
    compare_009.inputs[2].default_value = 0
    # B
    compare_009.inputs[3].default_value = 0
    # A
    compare_009.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_009.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_009.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_009.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_009.inputs[8].default_value = ""
    # B
    compare_009.inputs[9].default_value = ""
    # C
    compare_009.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_009.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_009.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_009
    links.new(geometry_proximity_002.outputs[1], compare_009.inputs[0])
    links.new(compare_009.outputs[0], delete_geometry_003.inputs[1])

    delete_geometry_004 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_004.name = "Delete Geometry.004"
    delete_geometry_004.label = ""
    delete_geometry_004.location = (1389.0, -75.80029296875)
    delete_geometry_004.bl_label = "Delete Geometry"
    delete_geometry_004.mode = "ALL"
    delete_geometry_004.domain = "POINT"
    # Links for delete_geometry_004
    links.new(delete_geometry_004.outputs[0], set_position_002.inputs[0])
    links.new(transform_geometry_009.outputs[0], delete_geometry_004.inputs[0])

    geometry_proximity_003 = nodes.new("GeometryNodeProximity")
    geometry_proximity_003.name = "Geometry Proximity.003"
    geometry_proximity_003.label = ""
    geometry_proximity_003.location = (989.0, -515.80029296875)
    geometry_proximity_003.bl_label = "Geometry Proximity"
    geometry_proximity_003.target_element = "FACES"
    # Group ID
    geometry_proximity_003.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_003.inputs[3].default_value = 0
    # Links for geometry_proximity_003

    reroute_014 = nodes.new("NodeReroute")
    reroute_014.name = "Reroute.014"
    reroute_014.label = ""
    reroute_014.location = (1236.0, -2024.80029296875)
    reroute_014.bl_label = "Reroute"
    reroute_014.socket_idname = "NodeSocketGeometry"
    # Links for reroute_014
    links.new(reroute_014.outputs[0], distribute_points_on_faces_002.inputs[0])
    links.new(reroute_003.outputs[0], reroute_014.inputs[0])
    links.new(reroute_014.outputs[0], geometry_proximity_003.inputs[0])

    compare_010 = nodes.new("FunctionNodeCompare")
    compare_010.name = "Compare.010"
    compare_010.label = ""
    compare_010.location = (1149.0, -515.80029296875)
    compare_010.bl_label = "Compare"
    compare_010.operation = "GREATER_THAN"
    compare_010.data_type = "FLOAT"
    compare_010.mode = "ELEMENT"
    # B
    compare_010.inputs[1].default_value = 0.009999999776482582
    # A
    compare_010.inputs[2].default_value = 0
    # B
    compare_010.inputs[3].default_value = 0
    # A
    compare_010.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_010.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_010.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_010.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_010.inputs[8].default_value = ""
    # B
    compare_010.inputs[9].default_value = ""
    # C
    compare_010.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_010.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_010.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_010
    links.new(geometry_proximity_003.outputs[1], compare_010.inputs[0])
    links.new(compare_010.outputs[0], delete_geometry_004.inputs[1])

    separate_geometry_003 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_003.name = "Separate Geometry.003"
    separate_geometry_003.label = ""
    separate_geometry_003.location = (529.0, -35.80029296875)
    separate_geometry_003.bl_label = "Separate Geometry"
    separate_geometry_003.domain = "FACE"
    # Links for separate_geometry_003
    links.new(merge_by_distance_001.outputs[0], separate_geometry_003.inputs[0])

    separate_x_y_z_005 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_005.name = "Separate XYZ.005"
    separate_x_y_z_005.label = ""
    separate_x_y_z_005.location = (209.0, -35.80029296875)
    separate_x_y_z_005.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_005

    named_attribute_002 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.name = "Named Attribute.002"
    named_attribute_002.label = ""
    named_attribute_002.location = (29.0, -35.80029296875)
    named_attribute_002.bl_label = "Named Attribute"
    named_attribute_002.data_type = "FLOAT_VECTOR"
    # Name
    named_attribute_002.inputs[0].default_value = "UVMap"
    # Links for named_attribute_002
    links.new(named_attribute_002.outputs[0], separate_x_y_z_005.inputs[0])

    compare_011 = nodes.new("FunctionNodeCompare")
    compare_011.name = "Compare.011"
    compare_011.label = ""
    compare_011.location = (369.0, -35.80029296875)
    compare_011.bl_label = "Compare"
    compare_011.operation = "GREATER_THAN"
    compare_011.data_type = "FLOAT"
    compare_011.mode = "ELEMENT"
    # B
    compare_011.inputs[1].default_value = 0.8999999761581421
    # A
    compare_011.inputs[2].default_value = 0
    # B
    compare_011.inputs[3].default_value = 0
    # A
    compare_011.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_011.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_011.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_011.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_011.inputs[8].default_value = ""
    # B
    compare_011.inputs[9].default_value = ""
    # C
    compare_011.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_011.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_011.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_011
    links.new(separate_x_y_z_005.outputs[0], compare_011.inputs[0])
    links.new(compare_011.outputs[0], separate_geometry_003.inputs[1])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (1076.0, -1104.80029296875)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(separate_geometry_002.outputs[1], join_geometry_005.inputs[0])
    links.new(separate_geometry_003.outputs[0], join_geometry_005.inputs[0])

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.name = "Merge by Distance.002"
    merge_by_distance_002.label = ""
    merge_by_distance_002.location = (1256.0, -1084.80029296875)
    merge_by_distance_002.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance_002.inputs[1].default_value = True
    # Mode
    merge_by_distance_002.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_002
    links.new(merge_by_distance_002.outputs[0], gold_on_band.inputs[0])
    links.new(merge_by_distance_002.outputs[0], distribute_points_on_faces.inputs[0])
    links.new(join_geometry_005.outputs[0], merge_by_distance_002.inputs[0])

    frame_018 = nodes.new("NodeFrame")
    frame_018.name = "Frame.018"
    frame_018.label = "Curved"
    frame_018.location = (29.0, -393.19970703125)
    frame_018.bl_label = "Frame"
    frame_018.text = None
    frame_018.shrink = True
    frame_018.label_size = 20
    # Links for frame_018

    geometry_proximity_004 = nodes.new("GeometryNodeProximity")
    geometry_proximity_004.name = "Geometry Proximity.004"
    geometry_proximity_004.label = ""
    geometry_proximity_004.location = (29.0, -435.80029296875)
    geometry_proximity_004.bl_label = "Geometry Proximity"
    geometry_proximity_004.target_element = "POINTS"
    # Group ID
    geometry_proximity_004.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_004.inputs[3].default_value = 0
    # Links for geometry_proximity_004
    links.new(join_geometry_004.outputs[0], geometry_proximity_004.inputs[0])

    compare_012 = nodes.new("FunctionNodeCompare")
    compare_012.name = "Compare.012"
    compare_012.label = ""
    compare_012.location = (189.0, -435.80029296875)
    compare_012.bl_label = "Compare"
    compare_012.operation = "GREATER_THAN"
    compare_012.data_type = "FLOAT"
    compare_012.mode = "ELEMENT"
    # B
    compare_012.inputs[1].default_value = 0.003000000026077032
    # A
    compare_012.inputs[2].default_value = 0
    # B
    compare_012.inputs[3].default_value = 0
    # A
    compare_012.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_012.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_012.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_012.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_012.inputs[8].default_value = ""
    # B
    compare_012.inputs[9].default_value = ""
    # C
    compare_012.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_012.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_012.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_012
    links.new(geometry_proximity_004.outputs[1], compare_012.inputs[0])

    boolean_math_007 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_007.name = "Boolean Math.007"
    boolean_math_007.label = ""
    boolean_math_007.location = (349.0, -175.80029296875)
    boolean_math_007.bl_label = "Boolean Math"
    boolean_math_007.operation = "AND"
    # Links for boolean_math_007
    links.new(boolean_math_007.outputs[0], distribute_points_on_faces_001.inputs[1])
    links.new(compare_008.outputs[0], boolean_math_007.inputs[0])
    links.new(compare_012.outputs[0], boolean_math_007.inputs[1])

    # Parent assignments
    bézier_segment_004.parent = frame_014
    curve_to_mesh.parent = frame_014
    arc.parent = frame_014
    transform_geometry_012.parent = frame_014
    set_curve_tilt.parent = frame_014
    spline_parameter.parent = frame_014
    float_curve_003.parent = frame_014
    value_001.parent = frame_014
    vector_math_003.parent = frame_014
    resample_curve.parent = frame_014
    capture_attribute.parent = frame_014
    capture_attribute_001.parent = frame_014
    endpoint_selection.parent = frame_014
    instance_on_points.parent = frame_013
    arc_001.parent = frame_013
    align_rotation_to_vector.parent = frame_013
    set_curve_radius.parent = frame_014
    radius.parent = frame_014
    align_rotation_to_vector_001.parent = frame_013
    normal_001.parent = frame_013
    rotate_rotation.parent = frame_013
    transform_geometry_013.parent = frame_013
    set_position_003.parent = frame_014
    frame_013.parent = frame_014
    realize_instances.parent = frame_013
    sample_curve.parent = frame_013
    transform_geometry_015.parent = frame_014
    flip_faces_006.parent = frame_014
    join_geometry_012.parent = frame_014
    endpoint_selection_001.parent = frame_014
    curve_tangent_001.parent = frame_013
    set_position_004.parent = frame_014
    position_004.parent = frame_014
    vector_math_004.parent = frame_014
    merge_by_distance_001.parent = frame_014
    reroute.parent = frame_014
    reroute_001.parent = frame_014
    reroute_002.parent = frame_014
    mesh_to_curve_002.parent = frame_015
    is_edge_boundary.parent = frame_015
    curve_to_mesh_001.parent = frame_015
    curve_line.parent = frame_015
    set_curve_tilt_001.parent = frame_015
    flip_faces_005.parent = frame_015
    capture_attribute_002.parent = frame_015
    endpoint_selection_002.parent = frame_015
    boolean_math.parent = frame
    capture_attribute_003.parent = frame_015
    spline_parameter_001.parent = frame_015
    compare_001.parent = frame
    extrude_mesh.parent = frame
    repeat_input.parent = frame
    repeat_output.parent = frame
    vector_002.parent = frame
    set_curve_tilt_002.parent = frame_014
    curve_tilt.parent = frame_014
    math_003.parent = frame_014
    spline_parameter_002.parent = frame_014
    float_curve_004.parent = frame_014
    capture_attribute_004.parent = frame_015
    normal_002.parent = frame_015
    set_curve_normal.parent = frame_015
    blur_attribute.parent = frame_015
    endpoint_selection_003.parent = frame_015
    boolean_math_001.parent = frame
    math_004.parent = frame
    integer_001.parent = frame
    integer_math.parent = frame
    math_006.parent = frame
    math_007.parent = frame
    math_008.parent = frame
    vector_math_005.parent = frame
    float_curve_005.parent = frame
    vector_math_006.parent = frame
    reroute_005.parent = frame
    reroute_006.parent = frame
    reroute_007.parent = frame
    reroute_008.parent = frame
    reroute_009.parent = frame
    switch.parent = frame
    rotate_on_centre_1.parent = frame_002
    transform_geometry.parent = frame_002
    transform_geometry_001.parent = frame_002
    join_geometry_016.parent = frame_002
    rotate_on_centre_3.parent = frame_002
    reroute_011.parent = frame_002
    gold_decorations.parent = frame_001
    gold_on_band.parent = frame_003
    subdivide_mesh.parent = frame_001
    mesh_to_curve.parent = frame_001
    is_edge_boundary_1.parent = frame_001
    delete_geometry.parent = frame_001
    reroute_013.parent = frame_001
    sample_nearest_surface.parent = frame_001
    normal.parent = frame_001
    separate_x_y_z.parent = frame_001
    position.parent = frame_001
    compare_003.parent = frame_001
    boolean_math_003.parent = frame_001
    set_curve_normal_001.parent = frame_001
    set_curve_tilt_003.parent = frame_001
    transform_geometry_003.parent = frame_001
    flip_faces.parent = frame_001
    join_geometry.parent = frame_001
    frame_001.parent = frame_003
    join_geometry_001.parent = frame_001
    store_named_attribute.parent = frame_001
    set_position.parent = frame_001
    vector_math_001.parent = frame_001
    normal_003.parent = frame_001
    delete_geometry_001.parent = frame_001
    raycast.parent = frame_001
    position_001.parent = frame_001
    vector_math_002.parent = frame_001
    vector_math_007.parent = frame_001
    boolean_math_004.parent = frame_001
    mesh_to_curve_001.parent = frame_004
    capture_attribute_005.parent = frame_004
    normal_004.parent = frame_004
    set_curve_normal_002.parent = frame_004
    gold_decorations_1.parent = frame_004
    set_curve_tilt_004.parent = frame_004
    transform_geometry_004.parent = frame_004
    resample_curve_001.parent = frame_004
    instance_on_points_001.parent = frame_004
    ico_sphere.parent = frame_004
    realize_instances_001.parent = frame_004
    set_shade_smooth_001.parent = frame_004
    store_named_attribute_001.parent = frame_004
    boolean_math_005.parent = frame_004
    endpoint_selection_004.parent = frame_004
    store_named_attribute_002.parent = frame_004
    instance_on_points_002.parent = frame_005
    distribute_points_on_faces.parent = frame_005
    ico_sphere_002.parent = frame_005
    realize_instances_002.parent = frame_005
    set_shade_smooth_002.parent = frame_005
    store_named_attribute_003.parent = frame_005
    random_value_001.parent = frame_005
    frame_005.parent = frame_003
    store_named_attribute_004.parent = frame_014
    spline_parameter_004.parent = frame_014
    combine_x_y_z.parent = frame_014
    delete_geometry_002.parent = frame_009
    position_002.parent = frame_009
    separate_x_y_z_001.parent = frame_009
    compare_005.parent = frame_009
    named_attribute.parent = frame_009
    gem_in_holder.parent = frame_006
    gem_in_holder_1.parent = frame_006
    gem_in_holder_2.parent = frame_007
    instance_on_points_003.parent = frame_006
    curve_circle.parent = frame_006
    join_geometry_002.parent = frame_006
    transform_geometry_005.parent = frame_007
    join_geometry_003.parent = frame_008
    transform_geometry_006.parent = frame_006
    curve_tangent.parent = frame_006
    align_rotation_to_vector_002.parent = frame_006
    integer.parent = frame_006
    frame_006.parent = frame_008
    frame_007.parent = frame_008
    frame_008.parent = frame_009
    realize_instances_003.parent = frame_008
    bounding_box.parent = frame_009
    position_003.parent = frame_009
    map_range.parent = frame_009
    sample_u_v_surface.parent = frame_009
    position_005.parent = frame_009
    sample_u_v_surface_001.parent = frame_009
    normal_005.parent = frame_009
    set_position_001.parent = frame_009
    separate_x_y_z_002.parent = frame_009
    combine_x_y_z_001.parent = frame_009
    float_curve.parent = frame_009
    vector_math_008.parent = frame_009
    separate_x_y_z_003.parent = frame_009
    math.parent = frame_009
    frame_009.parent = frame_003
    transform_geometry_007.parent = frame_009
    flip_faces_001.parent = frame_009
    join_geometry_004.parent = frame_009
    gem_in_holder_3.parent = frame_010
    transform_geometry_008.parent = frame_010
    frame_010.parent = frame_008
    switch_001.parent = frame_011
    join_geometry_019.parent = frame_011
    group_input.parent = frame_011
    frame_011.parent = frame_003
    switch_002.parent = frame_004
    group_input_001.parent = frame_004
    join_geometry_020.parent = frame_004
    separate_geometry_002.parent = frame_012
    compare_006.parent = frame_012
    named_attribute_001.parent = frame_012
    separate_x_y_z_004.parent = frame_012
    compare_007.parent = frame_012
    boolean_math_006.parent = frame_012
    frame_012.parent = frame_003
    gem_in_holder_4.parent = frame_016
    position_006.parent = frame_016
    for_each_geometry_element_input_001.parent = frame_016
    for_each_geometry_element_output_001.parent = frame_016
    transform_geometry_009.parent = frame_016
    rotate_rotation_002.parent = frame_016
    frame_016.parent = frame_003
    random_value_007.parent = frame_016
    random_value_008.parent = frame_016
    set_position_002.parent = frame_016
    geometry_proximity_001.parent = frame_016
    curve_to_mesh_002.parent = frame_016
    reroute_003.parent = frame_003
    reroute_012.parent = frame_017
    distribute_points_on_faces_001.parent = frame_017
    geometry_proximity.parent = frame_017
    compare_008.parent = frame_017
    gem_in_holder_5.parent = frame_017
    instance_on_points_004.parent = frame_017
    random_value_010.parent = frame_017
    frame_017.parent = frame_003
    realize_instances_004.parent = frame_017
    transform_geometry_010.parent = frame_017
    swap_attr.parent = frame_017
    capture_attribute_008.parent = frame_017
    index.parent = frame_017
    store_named_attribute_005.parent = frame_016
    distribute_points_on_faces_002.parent = frame_016
    delete_geometry_003.parent = frame_016
    geometry_proximity_002.parent = frame_016
    compare_009.parent = frame_016
    delete_geometry_004.parent = frame_016
    geometry_proximity_003.parent = frame_016
    reroute_014.parent = frame_003
    compare_010.parent = frame_016
    separate_geometry_003.parent = frame_018
    separate_x_y_z_005.parent = frame_018
    named_attribute_002.parent = frame_018
    compare_011.parent = frame_018
    join_geometry_005.parent = frame_003
    merge_by_distance_002.parent = frame_003
    frame_018.parent = frame_012
    geometry_proximity_004.parent = frame_017
    compare_012.parent = frame_017
    boolean_math_007.parent = frame_017

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_space_/__res__switch_group():
    group_name = "Space / Res Switch"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Output", in_out="OUTPUT", socket_type="NodeSocketInt")
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Menu", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "Spacing"
    socket = group.interface.new_socket(name="Spacing", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Resolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-440.0, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (-80.0, 40.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    menu_switch_001 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_001.name = "Menu Switch.001"
    menu_switch_001.label = ""
    menu_switch_001.location = (-260.0, 40.0)
    menu_switch_001.bl_label = "Menu Switch"
    menu_switch_001.active_index = 1
    menu_switch_001.data_type = "INT"
    # Links for menu_switch_001
    links.new(group_input.outputs[0], menu_switch_001.inputs[0])
    links.new(group_input.outputs[1], menu_switch_001.inputs[1])
    links.new(group_input.outputs[2], menu_switch_001.inputs[2])
    links.new(menu_switch_001.outputs[0], group_output.inputs[0])

    # Parent assignments

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_bi-_rail__loft_group():
    group_name = "Bi-Rail Loft"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Interpolated Profiles", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="UVMap", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Rail Curve", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Rail Curve", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Profile Curves", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Smoothing", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = 0
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Menu", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "Spacing"
    socket = group.interface.new_socket(name="X Spacing", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.10000000149011612
    socket.min_value = 0.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Y Spacing", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.10000000149011612
    socket.min_value = 0.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="X Resolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 12
    socket.min_value = 2
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Y Resolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 12
    socket.min_value = 2
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Profile Blending Curve", in_out="INPUT", socket_type="NodeSocketClosure")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (3920.0, 620.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-4300.0, -140.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (-4140.0, -140.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(group_input.outputs[2], realize_instances.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (-1440.0, 340.0)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Count"
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (-1440.0, 200.0)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Count"
    # Length
    resample_curve_001.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_001

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (1549.0, -35.79999542236328)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position

    evaluate_at_index = nodes.new("GeometryNodeFieldAtIndex")
    evaluate_at_index.name = "Evaluate at Index"
    evaluate_at_index.label = ""
    evaluate_at_index.location = (529.0, -175.79998779296875)
    evaluate_at_index.bl_label = "Evaluate at Index"
    evaluate_at_index.domain = "POINT"
    evaluate_at_index.data_type = "FLOAT_VECTOR"
    # Links for evaluate_at_index

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (369.0, -175.79998779296875)
    position.bl_label = "Position"
    # Links for position
    links.new(position.outputs[0], evaluate_at_index.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (689.0, -175.79998779296875)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "MULTIPLY_ADD"
    # Vector
    vector_math.inputs[1].default_value = [-1.0, -1.0, -1.0]
    # Scale
    vector_math.inputs[3].default_value = -1.0
    # Links for vector_math
    links.new(position.outputs[0], vector_math.inputs[2])
    links.new(evaluate_at_index.outputs[0], vector_math.inputs[0])

    spline_length = nodes.new("GeometryNodeSplineLength")
    spline_length.name = "Spline Length"
    spline_length.label = ""
    spline_length.location = (29.0, -515.7999877929688)
    spline_length.bl_label = "Spline Length"
    # Links for spline_length

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (29.0, -375.79998779296875)
    index.bl_label = "Index"
    # Links for index

    spline_parameter = nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.label = ""
    spline_parameter.location = (29.0, -435.79998779296875)
    spline_parameter.bl_label = "Spline Parameter"
    # Links for spline_parameter

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (189.0, -375.79998779296875)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "SUBTRACT"
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(integer_math.outputs[0], evaluate_at_index.inputs[1])
    links.new(index.outputs[0], integer_math.inputs[0])
    links.new(spline_parameter.outputs[2], integer_math.inputs[1])

    integer_math_001 = nodes.new("FunctionNodeIntegerMath")
    integer_math_001.name = "Integer Math.001"
    integer_math_001.label = ""
    integer_math_001.location = (349.0, -415.79998779296875)
    integer_math_001.bl_label = "Integer Math"
    integer_math_001.operation = "ADD"
    # Value
    integer_math_001.inputs[2].default_value = 0
    # Links for integer_math_001
    links.new(integer_math.outputs[0], integer_math_001.inputs[0])

    integer_math_002 = nodes.new("FunctionNodeIntegerMath")
    integer_math_002.name = "Integer Math.002"
    integer_math_002.label = ""
    integer_math_002.location = (189.0, -515.7999877929688)
    integer_math_002.bl_label = "Integer Math"
    integer_math_002.operation = "SUBTRACT"
    # Value
    integer_math_002.inputs[1].default_value = 1
    # Value
    integer_math_002.inputs[2].default_value = 0
    # Links for integer_math_002
    links.new(spline_length.outputs[1], integer_math_002.inputs[0])
    links.new(integer_math_002.outputs[0], integer_math_001.inputs[1])

    rotate_vector = nodes.new("FunctionNodeRotateVector")
    rotate_vector.name = "Rotate Vector"
    rotate_vector.label = ""
    rotate_vector.location = (1109.0, -175.79998779296875)
    rotate_vector.bl_label = "Rotate Vector"
    # Links for rotate_vector
    links.new(vector_math.outputs[0], rotate_vector.inputs[0])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.label = ""
    align_rotation_to_vector.location = (949.0, -395.79998779296875)
    align_rotation_to_vector.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector

    evaluate_at_index_001 = nodes.new("GeometryNodeFieldAtIndex")
    evaluate_at_index_001.name = "Evaluate at Index.001"
    evaluate_at_index_001.label = ""
    evaluate_at_index_001.location = (529.0, -295.79998779296875)
    evaluate_at_index_001.bl_label = "Evaluate at Index"
    evaluate_at_index_001.domain = "POINT"
    evaluate_at_index_001.data_type = "FLOAT_VECTOR"
    # Links for evaluate_at_index_001
    links.new(integer_math_001.outputs[0], evaluate_at_index_001.inputs[1])
    links.new(position.outputs[0], evaluate_at_index_001.inputs[0])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (729.0, -395.79998779296875)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "SUBTRACT"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(evaluate_at_index.outputs[0], vector_math_001.inputs[1])
    links.new(evaluate_at_index_001.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], align_rotation_to_vector.inputs[2])

    invert_rotation = nodes.new("FunctionNodeInvertRotation")
    invert_rotation.name = "Invert Rotation"
    invert_rotation.label = ""
    invert_rotation.location = (1109.0, -395.79998779296875)
    invert_rotation.bl_label = "Invert Rotation"
    # Links for invert_rotation
    links.new(align_rotation_to_vector.outputs[0], invert_rotation.inputs[0])
    links.new(invert_rotation.outputs[0], rotate_vector.inputs[1])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (1349.0, -175.79998779296875)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [-1.0, -1.0, -1.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], set_position.inputs[2])
    links.new(rotate_vector.outputs[0], vector_math_002.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (949.0, -575.7999877929688)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "LENGTH"
    # Vector
    vector_math_003.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(vector_math_001.outputs[0], vector_math_003.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (1129.0, -575.7999877929688)
    math.bl_label = "Math"
    math.operation = "DIVIDE"
    math.use_clamp = False
    # Value
    math.inputs[0].default_value = 1.0
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(math.outputs[0], vector_math_002.inputs[3])
    links.new(vector_math_003.outputs[1], math.inputs[1])

    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.name = "Resample Curve.002"
    resample_curve_002.label = ""
    resample_curve_002.location = (-3260.0, -140.0)
    resample_curve_002.bl_label = "Resample Curve"
    resample_curve_002.keep_last_segment = True
    # Selection
    resample_curve_002.inputs[1].default_value = True
    # Mode
    resample_curve_002.inputs[2].default_value = "Evaluated"
    # Count
    resample_curve_002.inputs[3].default_value = 10
    # Length
    resample_curve_002.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_002
    links.new(resample_curve_002.outputs[0], set_position.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "Fix Transform"
    frame_001.location = (-3049.0, -84.20000457763672)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (-1220.0, -20.0)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "CURVE"
    # Links for separate_geometry
    links.new(set_position.outputs[0], separate_geometry.inputs[0])

    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.label = ""
    index_001.location = (-1220.0, -180.0)
    index_001.bl_label = "Index"
    # Links for index_001
    links.new(index_001.outputs[0], separate_geometry.inputs[1])

    duplicate_elements = nodes.new("GeometryNodeDuplicateElements")
    duplicate_elements.name = "Duplicate Elements"
    duplicate_elements.label = ""
    duplicate_elements.location = (-1020.0, 180.0)
    duplicate_elements.bl_label = "Duplicate Elements"
    duplicate_elements.domain = "SPLINE"
    # Selection
    duplicate_elements.inputs[1].default_value = True
    # Links for duplicate_elements
    links.new(separate_geometry.outputs[1], duplicate_elements.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (900.0, 120.0)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001
    links.new(duplicate_elements.outputs[0], set_position_001.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (49.0, -39.66666793823242)
    math_001.bl_label = "Math"
    math_001.operation = "DIVIDE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(duplicate_elements.outputs[1], math_001.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (-1080.0, 20.0)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketInt"
    # Links for reroute_001
    links.new(reroute_001.outputs[0], duplicate_elements.inputs[2])

    integer_math_003 = nodes.new("FunctionNodeIntegerMath")
    integer_math_003.name = "Integer Math.003"
    integer_math_003.label = ""
    integer_math_003.location = (29.0, -79.66666412353516)
    integer_math_003.bl_label = "Integer Math"
    integer_math_003.operation = "SUBTRACT"
    # Value
    integer_math_003.inputs[1].default_value = 1
    # Value
    integer_math_003.inputs[2].default_value = 0
    # Links for integer_math_003
    links.new(reroute_001.outputs[0], integer_math_003.inputs[0])
    links.new(integer_math_003.outputs[0], math_001.inputs[1])

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Duplicate Factor"
    frame_002.location = (-889.0, -0.3333333432674408)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (29.0, -195.8000030517578)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "CURVE"
    # Links for domain_size
    links.new(separate_geometry.outputs[0], domain_size.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (209.0, -35.80000305175781)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(domain_size.outputs[4], math_002.inputs[1])

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.label = ""
    sample_curve.location = (669.0, -215.8000030517578)
    sample_curve.bl_label = "Sample Curve"
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = False
    sample_curve.data_type = "FLOAT"
    # Value
    sample_curve.inputs[1].default_value = 0.0
    # Length
    sample_curve.inputs[3].default_value = 0.0
    # Links for sample_curve

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.label = ""
    spline_parameter_001.location = (489.0, -435.79998779296875)
    spline_parameter_001.bl_label = "Spline Parameter"
    # Links for spline_parameter_001
    links.new(spline_parameter_001.outputs[0], sample_curve.inputs[2])

    float_to_integer = nodes.new("FunctionNodeFloatToInt")
    float_to_integer.name = "Float to Integer"
    float_to_integer.label = ""
    float_to_integer.location = (429.0, -175.8000030517578)
    float_to_integer.bl_label = "Float to Integer"
    float_to_integer.rounding_mode = "FLOOR"
    # Links for float_to_integer
    links.new(float_to_integer.outputs[0], sample_curve.inputs[4])
    links.new(math_002.outputs[0], float_to_integer.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (429.0, -35.80000305175781)
    math_003.bl_label = "Math"
    math_003.operation = "FRACT"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 0.5
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_002.outputs[0], math_003.inputs[0])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (849.0, -95.80000305175781)
    mix.bl_label = "Mix"
    mix.data_type = "VECTOR"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    # Factor
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix.inputs[2].default_value = 0.0
    # B
    mix.inputs[3].default_value = 0.0
    # A
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix
    links.new(math_003.outputs[0], mix.inputs[0])
    links.new(sample_curve.outputs[1], mix.inputs[4])
    links.new(mix.outputs[1], set_position_001.inputs[2])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (569.0, -555.7999877929688)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], sample_curve.inputs[0])

    sample_curve_001 = nodes.new("GeometryNodeSampleCurve")
    sample_curve_001.name = "Sample Curve.001"
    sample_curve_001.label = ""
    sample_curve_001.location = (669.0, -495.79998779296875)
    sample_curve_001.bl_label = "Sample Curve"
    sample_curve_001.mode = "FACTOR"
    sample_curve_001.use_all_curves = False
    sample_curve_001.data_type = "FLOAT"
    # Value
    sample_curve_001.inputs[1].default_value = 0.0
    # Length
    sample_curve_001.inputs[3].default_value = 0.0
    # Links for sample_curve_001
    links.new(reroute_002.outputs[0], sample_curve_001.inputs[0])
    links.new(sample_curve_001.outputs[1], mix.inputs[5])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"
    spline_parameter_002.label = ""
    spline_parameter_002.location = (489.0, -715.7999877929688)
    spline_parameter_002.bl_label = "Spline Parameter"
    # Links for spline_parameter_002
    links.new(spline_parameter_002.outputs[0], sample_curve_001.inputs[2])

    integer_math_004 = nodes.new("FunctionNodeIntegerMath")
    integer_math_004.name = "Integer Math.004"
    integer_math_004.label = ""
    integer_math_004.location = (489.0, -675.7999877929688)
    integer_math_004.bl_label = "Integer Math"
    integer_math_004.operation = "ADD"
    # Value
    integer_math_004.inputs[1].default_value = 1
    # Value
    integer_math_004.inputs[2].default_value = 0
    # Links for integer_math_004
    links.new(integer_math_004.outputs[0], sample_curve_001.inputs[4])
    links.new(float_to_integer.outputs[0], integer_math_004.inputs[0])

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Spline Lerp"
    frame_003.location = (-189.0, -144.1999969482422)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.label = ""
    reroute_003.location = (89.0, -555.7999877929688)
    reroute_003.bl_label = "Reroute"
    reroute_003.socket_idname = "NodeSocketGeometry"
    # Links for reroute_003
    links.new(set_position.outputs[0], reroute_003.inputs[0])
    links.new(reroute_003.outputs[0], reroute_002.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (1460.0, 360.0)
    instance_on_points.bl_label = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = True
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Links for instance_on_points

    split_to_instances = nodes.new("GeometryNodeSplitToInstances")
    split_to_instances.name = "Split to Instances"
    split_to_instances.label = ""
    split_to_instances.location = (1060.0, 120.0)
    split_to_instances.bl_label = "Split to Instances"
    split_to_instances.domain = "CURVE"
    # Selection
    split_to_instances.inputs[1].default_value = True
    # Links for split_to_instances
    links.new(set_position_001.outputs[0], split_to_instances.inputs[0])
    links.new(duplicate_elements.outputs[1], split_to_instances.inputs[2])
    links.new(split_to_instances.outputs[0], instance_on_points.inputs[2])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (29.0, -95.7999267578125)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Links for sample_index
    links.new(resample_curve_001.outputs[0], sample_index.inputs[0])

    index_002 = nodes.new("GeometryNodeInputIndex")
    index_002.name = "Index.002"
    index_002.label = ""
    index_002.location = (29.0, -335.7999267578125)
    index_002.bl_label = "Index"
    # Links for index_002
    links.new(index_002.outputs[0], sample_index.inputs[2])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (29.0, -295.7999267578125)
    position_001.bl_label = "Position"
    # Links for position_001
    links.new(position_001.outputs[0], sample_index.inputs[1])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (189.0, -95.7999267578125)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "SUBTRACT"
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(position_001.outputs[0], vector_math_004.inputs[1])
    links.new(sample_index.outputs[0], vector_math_004.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (1049.0, -35.7999267578125)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "LENGTH"
    # Vector
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_005.inputs[3].default_value = 1.0
    # Links for vector_math_005
    links.new(vector_math_005.outputs[1], instance_on_points.inputs[6])
    links.new(vector_math_004.outputs[0], vector_math_005.inputs[0])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.label = ""
    align_rotation_to_vector_001.location = (1049.0, -155.7999267578125)
    align_rotation_to_vector_001.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_001.axis = "X"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_001.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_001
    links.new(vector_math_004.outputs[0], align_rotation_to_vector_001.inputs[2])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (249.0, -455.7999267578125)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (449.0, -395.7999267578125)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "CROSS_PRODUCT"
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006
    links.new(curve_tangent.outputs[0], vector_math_006.inputs[1])
    links.new(vector_math_004.outputs[0], vector_math_006.inputs[0])

    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.name = "Align Rotation to Vector.002"
    align_rotation_to_vector_002.label = ""
    align_rotation_to_vector_002.location = (1209.0, -155.7999267578125)
    align_rotation_to_vector_002.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_002.axis = "Y"
    align_rotation_to_vector_002.pivot_axis = "X"
    # Factor
    align_rotation_to_vector_002.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_002
    links.new(align_rotation_to_vector_002.outputs[0], instance_on_points.inputs[5])
    links.new(align_rotation_to_vector_001.outputs[0], align_rotation_to_vector_002.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Orient Splines"
    frame_004.location = (131.0, 1035.7999267578125)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.label = ""
    realize_instances_001.location = (1620.0, 360.0)
    realize_instances_001.bl_label = "Realize Instances"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0
    # Links for realize_instances_001
    links.new(instance_on_points.outputs[0], realize_instances_001.inputs[0])

    resample_curve_003 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.name = "Resample Curve.003"
    resample_curve_003.label = ""
    resample_curve_003.location = (2200.0, 360.0)
    resample_curve_003.bl_label = "Resample Curve"
    resample_curve_003.keep_last_segment = True
    # Selection
    resample_curve_003.inputs[1].default_value = True
    # Mode
    resample_curve_003.inputs[2].default_value = "Count"
    # Length
    resample_curve_003.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_003
    links.new(realize_instances_001.outputs[0], resample_curve_003.inputs[0])

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    grid.label = ""
    grid.location = (2380.0, 740.0)
    grid.bl_label = "Grid"
    # Size X
    grid.inputs[0].default_value = 1.0
    # Size Y
    grid.inputs[1].default_value = 1.0
    # Links for grid

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (3020.0, 780.0)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Offset
    set_position_002.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_002

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (2720.0, 420.0)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001
    links.new(resample_curve_003.outputs[0], sample_index_001.inputs[0])
    links.new(sample_index_001.outputs[0], set_position_002.inputs[2])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (2720.0, 220.0)
    position_002.bl_label = "Position"
    # Links for position_002
    links.new(position_002.outputs[0], sample_index_001.inputs[1])

    index_003 = nodes.new("GeometryNodeInputIndex")
    index_003.name = "Index.003"
    index_003.label = ""
    index_003.location = (2720.0, 160.0)
    index_003.bl_label = "Index"
    # Links for index_003
    links.new(index_003.outputs[0], sample_index_001.inputs[2])

    set_position_005 = nodes.new("GeometryNodeSetPosition")
    set_position_005.name = "Set Position.005"
    set_position_005.label = ""
    set_position_005.location = (3620.0, 680.0)
    set_position_005.bl_label = "Set Position"
    # Selection
    set_position_005.inputs[1].default_value = True
    # Offset
    set_position_005.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_005
    links.new(set_position_002.outputs[0], set_position_005.inputs[0])
    links.new(set_position_005.outputs[0], group_output.inputs[0])

    position_005 = nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"
    position_005.label = ""
    position_005.location = (3460.0, 600.0)
    position_005.bl_label = "Position"
    # Links for position_005

    blur_attribute = nodes.new("GeometryNodeBlurAttribute")
    blur_attribute.name = "Blur Attribute"
    blur_attribute.label = ""
    blur_attribute.location = (3620.0, 600.0)
    blur_attribute.bl_label = "Blur Attribute"
    blur_attribute.data_type = "FLOAT_VECTOR"
    # Links for blur_attribute
    links.new(blur_attribute.outputs[0], set_position_005.inputs[2])
    links.new(position_005.outputs[0], blur_attribute.inputs[0])

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Is Edge Boundary"
    is_edge_boundary.label = ""
    is_edge_boundary.location = (3460.0, 440.0)
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    is_edge_boundary.bl_label = "Group"
    # Links for is_edge_boundary

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (3460.0, 540.0)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "NOT"
    # Boolean
    boolean_math.inputs[1].default_value = False
    # Links for boolean_math
    links.new(is_edge_boundary.outputs[0], boolean_math.inputs[0])
    links.new(boolean_math.outputs[0], blur_attribute.inputs[2])

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.label = ""
    attribute_statistic.location = (1780.0, 40.0)
    attribute_statistic.bl_label = "Attribute Statistic"
    attribute_statistic.data_type = "FLOAT"
    attribute_statistic.domain = "CURVE"
    # Selection
    attribute_statistic.inputs[1].default_value = True
    # Links for attribute_statistic
    links.new(realize_instances_001.outputs[0], attribute_statistic.inputs[0])

    spline_length_001 = nodes.new("GeometryNodeSplineLength")
    spline_length_001.name = "Spline Length.001"
    spline_length_001.label = ""
    spline_length_001.location = (1620.0, -60.0)
    spline_length_001.bl_label = "Spline Length"
    # Links for spline_length_001
    links.new(spline_length_001.outputs[0], attribute_statistic.inputs[2])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (1940.0, 40.0)
    math_004.bl_label = "Math"
    math_004.operation = "DIVIDE"
    math_004.use_clamp = False
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(attribute_statistic.outputs[3], math_004.inputs[0])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (-2400.0, 240.0)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[0], resample_curve.inputs[0])
    links.new(group_input_001.outputs[1], resample_curve_001.inputs[0])

    curve_length = nodes.new("GeometryNodeCurveLength")
    curve_length.name = "Curve Length"
    curve_length.label = ""
    curve_length.location = (-2160.0, 480.0)
    curve_length.bl_label = "Curve Length"
    # Links for curve_length
    links.new(group_input_001.outputs[0], curve_length.inputs[0])

    curve_length_001 = nodes.new("GeometryNodeCurveLength")
    curve_length_001.name = "Curve Length.001"
    curve_length_001.label = ""
    curve_length_001.location = (-2160.0, 440.0)
    curve_length_001.bl_label = "Curve Length"
    # Links for curve_length_001
    links.new(group_input_001.outputs[1], curve_length_001.inputs[0])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (-2000.0, 460.0)
    math_005.bl_label = "Math"
    math_005.operation = "MINIMUM"
    math_005.use_clamp = False
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(curve_length.outputs[0], math_005.inputs[0])
    links.new(curve_length_001.outputs[0], math_005.inputs[1])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (-2000.0, 420.0)
    math_006.bl_label = "Math"
    math_006.operation = "DIVIDE"
    math_006.use_clamp = False
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(math_005.outputs[0], math_006.inputs[0])
    links.new(group_input_001.outputs[6], math_006.inputs[1])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (2860.0, 780.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "FLOAT2"
    store_named_attribute.domain = "CORNER"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute
    links.new(store_named_attribute.outputs[0], set_position_002.inputs[0])
    links.new(grid.outputs[0], store_named_attribute.inputs[0])

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (2540.0, 660.0)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(grid.outputs[1], separate_x_y_z.inputs[0])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (2700.0, 660.0)
    combine_x_y_z.bl_label = "Combine XYZ"
    # Z
    combine_x_y_z.inputs[2].default_value = 0.0
    # Links for combine_x_y_z
    links.new(separate_x_y_z.outputs[0], combine_x_y_z.inputs[1])
    links.new(separate_x_y_z.outputs[1], combine_x_y_z.inputs[0])
    links.new(combine_x_y_z.outputs[0], store_named_attribute.inputs[3])

    group_input_002 = nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.label = ""
    group_input_002.location = (3620.0, 480.0)
    group_input_002.bl_label = "Group Input"
    # Links for group_input_002
    links.new(group_input_002.outputs[3], blur_attribute.inputs[1])

    group_input_003 = nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.label = ""
    group_input_003.location = (1660.0, -180.0)
    group_input_003.bl_label = "Group Input"
    # Links for group_input_003
    links.new(group_input_003.outputs[5], math_004.inputs[1])

    space_/_res_switch = nodes.new("GeometryNodeGroup")
    space_/_res_switch.name = "Menu Switch.001"
    space_/_res_switch.label = ""
    space_/_res_switch.location = (2140.0, -120.0)
    space_/_res_switch.node_tree = create_space_/__res__switch_group()
    space_/_res_switch.bl_label = "Group"
    # Links for space_/_res_switch
    links.new(group_input_003.outputs[4], space_/_res_switch.inputs[0])
    links.new(group_input_003.outputs[7], space_/_res_switch.inputs[2])
    links.new(math_004.outputs[0], space_/_res_switch.inputs[1])
    links.new(space_/_res_switch.outputs[0], resample_curve_003.inputs[3])
    links.new(space_/_res_switch.outputs[0], grid.inputs[3])

    space_/_res_switch_1 = nodes.new("GeometryNodeGroup")
    space_/_res_switch_1.name = "Menu Switch.002"
    space_/_res_switch_1.label = ""
    space_/_res_switch_1.location = (-1720.0, 180.0)
    space_/_res_switch_1.node_tree = create_space_/__res__switch_group()
    space_/_res_switch_1.bl_label = "Group"
    # Links for space_/_res_switch_1
    links.new(space_/_res_switch_1.outputs[0], resample_curve.inputs[3])
    links.new(space_/_res_switch_1.outputs[0], resample_curve_001.inputs[3])
    links.new(space_/_res_switch_1.outputs[0], grid.inputs[2])
    links.new(space_/_res_switch_1.outputs[0], reroute_001.inputs[0])
    links.new(group_input_001.outputs[4], space_/_res_switch_1.inputs[0])
    links.new(math_006.outputs[0], space_/_res_switch_1.inputs[1])
    links.new(group_input_001.outputs[8], space_/_res_switch_1.inputs[2])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (3920.0, 480.0)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "FLOAT_VECTOR"
    # Name
    named_attribute.inputs[0].default_value = "UVMap"
    # Links for named_attribute
    links.new(named_attribute.outputs[0], group_output.inputs[2])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (2760.0, 40.0)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "FLOAT2"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute_001
    links.new(store_named_attribute_001.outputs[0], group_output.inputs[1])
    links.new(resample_curve_003.outputs[0], store_named_attribute_001.inputs[0])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (2580.0, -80.0)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # Z
    combine_x_y_z_001.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_001
    links.new(combine_x_y_z_001.outputs[0], store_named_attribute_001.inputs[3])

    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_003.name = "Spline Parameter.003"
    spline_parameter_003.label = ""
    spline_parameter_003.location = (2400.0, -80.0)
    spline_parameter_003.bl_label = "Spline Parameter"
    # Links for spline_parameter_003
    links.new(spline_parameter_003.outputs[0], combine_x_y_z_001.inputs[0])

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.label = ""
    capture_attribute.location = (1060.0, 260.0)
    capture_attribute.bl_label = "Capture Attribute"
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    # Links for capture_attribute
    links.new(capture_attribute.outputs[0], instance_on_points.inputs[0])
    links.new(resample_curve.outputs[0], capture_attribute.inputs[0])
    links.new(capture_attribute.outputs[1], combine_x_y_z_001.inputs[1])

    spline_parameter_004 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_004.name = "Spline Parameter.004"
    spline_parameter_004.label = ""
    spline_parameter_004.location = (900.0, 200.0)
    spline_parameter_004.bl_label = "Spline Parameter"
    # Links for spline_parameter_004
    links.new(spline_parameter_004.outputs[0], capture_attribute.inputs[1])

    field_average = nodes.new("GeometryNodeFieldAverage")
    field_average.name = "Field Average"
    field_average.label = ""
    field_average.location = (449.0, -535.7999267578125)
    field_average.bl_label = "Field Average"
    field_average.data_type = "FLOAT_VECTOR"
    field_average.domain = "POINT"
    # Group ID
    field_average.inputs[1].default_value = 0
    # Links for field_average
    links.new(vector_math_006.outputs[0], field_average.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (629.0, -455.7999267578125)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "VECTOR"
    compare.mode = "DIRECTION"
    # A
    compare.inputs[0].default_value = 0.0
    # B
    compare.inputs[1].default_value = 0.0
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.0
    # Epsilon
    compare.inputs[12].default_value = 1.5707963705062866
    # Links for compare
    links.new(vector_math_006.outputs[0], compare.inputs[4])
    links.new(field_average.outputs[0], compare.inputs[5])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (809.0, -455.7999267578125)
    switch.bl_label = "Switch"
    switch.input_type = "FLOAT"
    # False
    switch.inputs[1].default_value = -1.0
    # True
    switch.inputs[2].default_value = 1.0
    # Links for switch
    links.new(compare.outputs[0], switch.inputs[0])

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.label = ""
    vector_math_007.location = (1049.0, -315.7999267578125)
    vector_math_007.bl_label = "Vector Math"
    vector_math_007.operation = "SCALE"
    # Vector
    vector_math_007.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_007
    links.new(vector_math_007.outputs[0], align_rotation_to_vector_002.inputs[2])
    links.new(vector_math_006.outputs[0], vector_math_007.inputs[0])
    links.new(switch.outputs[0], vector_math_007.inputs[3])

    domain_size_001 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_001.name = "Domain Size.001"
    domain_size_001.label = ""
    domain_size_001.location = (-3780.0, 40.0)
    domain_size_001.bl_label = "Domain Size"
    domain_size_001.component = "CURVE"
    # Links for domain_size_001

    separate_components = nodes.new("GeometryNodeSeparateComponents")
    separate_components.name = "Separate Components"
    separate_components.label = ""
    separate_components.location = (-3980.0, -140.0)
    separate_components.bl_label = "Separate Components"
    # Links for separate_components
    links.new(realize_instances.outputs[0], separate_components.inputs[0])
    links.new(separate_components.outputs[1], domain_size_001.inputs[0])

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.label = ""
    curve_line.location = (-3660.0, -280.0)
    curve_line.bl_label = "Curve Line"
    curve_line.mode = "POINTS"
    # Start
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    # End
    curve_line.inputs[1].default_value = Vector((0.0, 0.0, 1.0))
    # Direction
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    # Length
    curve_line.inputs[3].default_value = 1.0
    # Links for curve_line

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (-3440.0, -120.0)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Links for switch_001
    links.new(switch_001.outputs[0], resample_curve_002.inputs[0])
    links.new(separate_components.outputs[1], switch_001.inputs[1])
    links.new(curve_line.outputs[0], switch_001.inputs[2])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (-3620.0, 40.0)
    compare_001.bl_label = "Compare"
    compare_001.operation = "EQUAL"
    compare_001.data_type = "INT"
    compare_001.mode = "ELEMENT"
    # A
    compare_001.inputs[0].default_value = 0.0
    # B
    compare_001.inputs[1].default_value = 0.0
    # B
    compare_001.inputs[3].default_value = 0
    # A
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_001.inputs[8].default_value = ""
    # B
    compare_001.inputs[9].default_value = ""
    # C
    compare_001.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_001.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_001.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_001
    links.new(domain_size_001.outputs[4], compare_001.inputs[2])
    links.new(compare_001.outputs[0], switch_001.inputs[0])

    group_input_004 = nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.label = ""
    group_input_004.location = (-520.0, -20.0)
    group_input_004.bl_label = "Group Input"
    # Links for group_input_004

    evaluate_closure = nodes.new("NodeEvaluateClosure")
    evaluate_closure.name = "Evaluate Closure"
    evaluate_closure.label = ""
    evaluate_closure.location = (-520.0, -100.0)
    evaluate_closure.bl_label = "Evaluate Closure"
    evaluate_closure.active_input_index = 0
    evaluate_closure.active_output_index = 0
    evaluate_closure.define_signature = False
    # Links for evaluate_closure
    links.new(math_001.outputs[0], evaluate_closure.inputs[1])
    links.new(group_input_004.outputs[9], evaluate_closure.inputs[0])
    links.new(evaluate_closure.outputs[0], math_002.inputs[0])

    # Parent assignments
    set_position.parent = frame_001
    evaluate_at_index.parent = frame_001
    position.parent = frame_001
    vector_math.parent = frame_001
    spline_length.parent = frame_001
    index.parent = frame_001
    spline_parameter.parent = frame_001
    integer_math.parent = frame_001
    integer_math_001.parent = frame_001
    integer_math_002.parent = frame_001
    rotate_vector.parent = frame_001
    align_rotation_to_vector.parent = frame_001
    evaluate_at_index_001.parent = frame_001
    vector_math_001.parent = frame_001
    invert_rotation.parent = frame_001
    vector_math_002.parent = frame_001
    vector_math_003.parent = frame_001
    math.parent = frame_001
    math_001.parent = frame_002
    integer_math_003.parent = frame_002
    domain_size.parent = frame_003
    math_002.parent = frame_003
    sample_curve.parent = frame_003
    spline_parameter_001.parent = frame_003
    float_to_integer.parent = frame_003
    math_003.parent = frame_003
    mix.parent = frame_003
    reroute_002.parent = frame_003
    sample_curve_001.parent = frame_003
    spline_parameter_002.parent = frame_003
    integer_math_004.parent = frame_003
    reroute_003.parent = frame_003
    sample_index.parent = frame_004
    index_002.parent = frame_004
    position_001.parent = frame_004
    vector_math_004.parent = frame_004
    vector_math_005.parent = frame_004
    align_rotation_to_vector_001.parent = frame_004
    curve_tangent.parent = frame_004
    vector_math_006.parent = frame_004
    align_rotation_to_vector_002.parent = frame_004
    field_average.parent = frame_004
    compare.parent = frame_004
    switch.parent = frame_004
    vector_math_007.parent = frame_004

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_sleeves_group():
    group_name = "Sleeves"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2600.0, 300.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (973.5, -35.699920654296875)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "FLOAT2"
    store_named_attribute.domain = "CORNER"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.name = "Transform Geometry.007"
    transform_geometry_007.label = ""
    transform_geometry_007.location = (1153.5, -35.699920654296875)
    transform_geometry_007.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_007.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_007.inputs[2].default_value = Vector((-0.25, 0.029999999329447746, 0.14999999105930328))
    # Rotation
    transform_geometry_007.inputs[3].default_value = Euler((0.06440264731645584, 0.36739179491996765, 0.0), 'XYZ')
    # Scale
    transform_geometry_007.inputs[4].default_value = Vector((1.0, 1.2899999618530273, 1.0))
    # Links for transform_geometry_007
    links.new(store_named_attribute.outputs[0], transform_geometry_007.inputs[0])

    cone = nodes.new("GeometryNodeMeshCone")
    cone.name = "Cone"
    cone.label = ""
    cone.location = (773.5, -35.699920654296875)
    cone.bl_label = "Cone"
    cone.fill_type = "NONE"
    # Vertices
    cone.inputs[0].default_value = 32
    # Side Segments
    cone.inputs[1].default_value = 26
    # Fill Segments
    cone.inputs[2].default_value = 1
    # Radius Top
    cone.inputs[3].default_value = 0.05000000074505806
    # Radius Bottom
    cone.inputs[4].default_value = 0.03999999910593033
    # Depth
    cone.inputs[5].default_value = 0.14000000059604645
    # Links for cone
    links.new(cone.outputs[0], store_named_attribute.inputs[0])
    links.new(cone.outputs[4], store_named_attribute.inputs[3])

    frame_011 = nodes.new("NodeFrame")
    frame_011.name = "Frame.011"
    frame_011.label = "Sleeve"
    frame_011.location = (-2049.0, 417.8000183105469)
    frame_011.bl_label = "Frame"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20
    # Links for frame_011

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (588.9998779296875, -437.8000183105469)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "FLOAT2"
    store_named_attribute_001.domain = "CORNER"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute_001

    transform_geometry_009 = nodes.new("GeometryNodeTransform")
    transform_geometry_009.name = "Transform Geometry.009"
    transform_geometry_009.label = ""
    transform_geometry_009.location = (1449.0, -437.8000183105469)
    transform_geometry_009.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_009.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_009.inputs[2].default_value = Vector((-0.28999999165534973, -0.04999999701976776, -0.010000007227063179))
    # Rotation
    transform_geometry_009.inputs[3].default_value = Euler((-0.47315871715545654, 0.3237585723400116, 0.2094395011663437), 'XYZ')
    # Scale
    transform_geometry_009.inputs[4].default_value = Vector((1.0, 1.2899999618530273, 1.0))
    # Links for transform_geometry_009

    cone_001 = nodes.new("GeometryNodeMeshCone")
    cone_001.name = "Cone.001"
    cone_001.label = ""
    cone_001.location = (388.9998779296875, -437.8000183105469)
    cone_001.bl_label = "Cone"
    cone_001.fill_type = "NONE"
    # Vertices
    cone_001.inputs[0].default_value = 32
    # Side Segments
    cone_001.inputs[1].default_value = 29
    # Fill Segments
    cone_001.inputs[2].default_value = 1
    # Radius Top
    cone_001.inputs[3].default_value = 0.03999999910593033
    # Radius Bottom
    cone_001.inputs[4].default_value = 0.029999999329447746
    # Links for cone_001
    links.new(cone_001.outputs[4], store_named_attribute_001.inputs[3])
    links.new(cone_001.outputs[0], store_named_attribute_001.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_009.name = "Join Geometry.009"
    join_geometry_009.label = ""
    join_geometry_009.location = (2153.5, -35.699920654296875)
    join_geometry_009.bl_label = "Join Geometry"
    # Links for join_geometry_009
    links.new(transform_geometry_009.outputs[0], join_geometry_009.inputs[0])
    links.new(transform_geometry_007.outputs[0], join_geometry_009.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1113.5, -455.6999206542969)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Position
    set_position_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_001
    links.new(set_position_001.outputs[0], transform_geometry_009.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (249.0, -937.800048828125)
    position_001.bl_label = "Position"
    # Links for position_001

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (409.0, -937.800048828125)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001
    links.new(position_001.outputs[0], separate_x_y_z_001.inputs[0])

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.label = ""
    map_range_001.location = (569.0, -937.800048828125)
    map_range_001.bl_label = "Map Range"
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT"
    # From Min
    map_range_001.inputs[1].default_value = -0.05000000074505806
    # From Max
    map_range_001.inputs[2].default_value = 0.050000011920928955
    # To Min
    map_range_001.inputs[3].default_value = 0.0
    # To Max
    map_range_001.inputs[4].default_value = 1.0
    # Steps
    map_range_001.inputs[5].default_value = 4.0
    # Vector
    map_range_001.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_001.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_001.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_001.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_001.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_001
    links.new(separate_x_y_z_001.outputs[1], map_range_001.inputs[0])

    float_curve_002 = nodes.new("ShaderNodeFloatCurve")
    float_curve_002.name = "Float Curve.002"
    float_curve_002.label = ""
    float_curve_002.location = (749.0, -937.800048828125)
    float_curve_002.bl_label = "Float Curve"
    # Factor
    float_curve_002.inputs[0].default_value = 1.0
    # Links for float_curve_002
    links.new(map_range_001.outputs[0], float_curve_002.inputs[1])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (1169.0, -937.800048828125)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # X
    combine_x_y_z_001.inputs[0].default_value = 0.0
    # Y
    combine_x_y_z_001.inputs[1].default_value = 0.0
    # Links for combine_x_y_z_001
    links.new(combine_x_y_z_001.outputs[0], set_position_001.inputs[3])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (1009.0, -937.800048828125)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 0.029999999329447746
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(float_curve_002.outputs[0], math_002.inputs[0])
    links.new(math_002.outputs[0], combine_x_y_z_001.inputs[2])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (89.0, -35.80000305175781)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Links for mesh_to_curve
    links.new(cone.outputs[2], mesh_to_curve.inputs[1])
    links.new(transform_geometry_007.outputs[0], mesh_to_curve.inputs[0])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (129.0, -175.8000030517578)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Links for mesh_to_curve_001
    links.new(transform_geometry_009.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(cone_001.outputs[1], mesh_to_curve_001.inputs[1])

    bi-_rail_loft = nodes.new("GeometryNodeGroup")
    bi-_rail_loft.name = "Bi-Rail Loft.002"
    bi-_rail_loft.label = ""
    bi-_rail_loft.location = (309.0, -35.80000305175781)
    bi-_rail_loft.node_tree = create_bi-_rail__loft_group()
    bi-_rail_loft.bl_label = "Group"
    # Smoothing
    bi-_rail_loft.inputs[3].default_value = 82
    # Menu
    bi-_rail_loft.inputs[4].default_value = "Resolution"
    # X Spacing
    bi-_rail_loft.inputs[5].default_value = 0.10000000149011612
    # Y Spacing
    bi-_rail_loft.inputs[6].default_value = 0.10000000149011612
    # X Resolution
    bi-_rail_loft.inputs[7].default_value = 23
    # Y Resolution
    bi-_rail_loft.inputs[8].default_value = 128
    # Links for bi-_rail_loft
    links.new(mesh_to_curve_001.outputs[0], bi-_rail_loft.inputs[1])
    links.new(mesh_to_curve.outputs[0], bi-_rail_loft.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.name = "Flip Faces.003"
    flip_faces_003.label = ""
    flip_faces_003.location = (569.0, -35.80000305175781)
    flip_faces_003.bl_label = "Flip Faces"
    # Selection
    flip_faces_003.inputs[1].default_value = True
    # Links for flip_faces_003
    links.new(bi-_rail_loft.outputs[0], flip_faces_003.inputs[0])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (749.0, -35.80000305175781)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Offset
    set_position_002.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_002
    links.new(flip_faces_003.outputs[0], set_position_002.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (189.0, -475.79998779296875)
    position_002.bl_label = "Position"
    # Links for position_002

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (349.0, -355.79998779296875)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "MULTIPLY_ADD"
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(position_002.outputs[0], vector_math.inputs[2])

    value = nodes.new("ShaderNodeValue")
    value.name = "Value"
    value.label = ""
    value.location = (189.0, -415.79998779296875)
    value.bl_label = "Value"
    # Links for value
    links.new(value.outputs[0], vector_math.inputs[1])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.label = ""
    normal.location = (189.0, -355.79998779296875)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = False
    # Links for normal
    links.new(normal.outputs[0], vector_math.inputs[0])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (509.0, -355.79998779296875)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "MULTIPLY_ADD"
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(vector_math.outputs[0], vector_math_001.inputs[2])
    links.new(vector_math_001.outputs[0], set_position_002.inputs[2])
    links.new(normal.outputs[0], vector_math_001.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (349.0, -535.7999877929688)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "3D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = False
    # W
    noise_texture.inputs[1].default_value = 0.0
    # Scale
    noise_texture.inputs[2].default_value = 13.209991455078125
    # Detail
    noise_texture.inputs[3].default_value = 0.4999999701976776
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Offset
    noise_texture.inputs[6].default_value = 0.0
    # Gain
    noise_texture.inputs[7].default_value = 1.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0
    # Links for noise_texture

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (29.0, -535.7999877929688)
    position_003.bl_label = "Position"
    # Links for position_003

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (189.0, -535.7999877929688)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "MULTIPLY"
    # Vector
    vector_math_002.inputs[1].default_value = [1.0, 1.0, 5.640000343322754]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], noise_texture.inputs[0])

    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.name = "Map Range.002"
    map_range_002.label = ""
    map_range_002.location = (509.0, -535.7999877929688)
    map_range_002.bl_label = "Map Range"
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    # From Min
    map_range_002.inputs[1].default_value = -1.0
    # From Max
    map_range_002.inputs[2].default_value = 1.0
    # To Min
    map_range_002.inputs[3].default_value = -0.0020000000949949026
    # To Max
    map_range_002.inputs[4].default_value = 0.0010000000474974513
    # Steps
    map_range_002.inputs[5].default_value = 4.0
    # Vector
    map_range_002.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_002.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_002.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_002.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_002.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_002.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_002
    links.new(noise_texture.outputs[0], map_range_002.inputs[0])
    links.new(map_range_002.outputs[0], vector_math_001.inputs[1])

    frame_012 = nodes.new("NodeFrame")
    frame_012.name = "Frame.012"
    frame_012.label = "Inner Sleeve"
    frame_012.location = (471.0, 175.8000030517578)
    frame_012.bl_label = "Frame"
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20
    # Links for frame_012

    rotate_vector = nodes.new("FunctionNodeRotateVector")
    rotate_vector.name = "Rotate Vector"
    rotate_vector.label = ""
    rotate_vector.location = (29.0, -595.7999877929688)
    rotate_vector.bl_label = "Rotate Vector"
    # Rotation
    rotate_vector.inputs[1].default_value = Euler((0.0, -0.42411497235298157, 0.0), 'XYZ')
    # Links for rotate_vector
    links.new(rotate_vector.outputs[0], vector_math_002.inputs[0])
    links.new(position_003.outputs[0], rotate_vector.inputs[0])

    join_geometry_015 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_015.name = "Join Geometry.015"
    join_geometry_015.label = ""
    join_geometry_015.location = (1920.0, 380.0)
    join_geometry_015.bl_label = "Join Geometry"
    # Links for join_geometry_015
    links.new(join_geometry_009.outputs[0], join_geometry_015.inputs[0])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.name = "Pipes"
    pipes.label = ""
    pipes.location = (1149.0, -235.79998779296875)
    pipes.node_tree = create_pipes_group()
    pipes.bl_label = "Group"
    # Links for pipes
    links.new(pipes.outputs[0], join_geometry_015.inputs[0])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (2300.0, 300.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True
    # Links for set_shade_smooth
    links.new(set_shade_smooth.outputs[0], group_output.inputs[0])
    links.new(join_geometry_015.outputs[0], set_shade_smooth.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (929.0, -35.80000305175781)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "fabric"
    # Value
    store_named_attribute_002.inputs[3].default_value = True
    # Links for store_named_attribute_002
    links.new(store_named_attribute_002.outputs[0], join_geometry_015.inputs[0])
    links.new(set_position_002.outputs[0], store_named_attribute_002.inputs[0])

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (768.9998779296875, -437.8000183105469)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry
    links.new(transform_geometry.outputs[0], set_position_001.inputs[0])
    links.new(store_named_attribute_001.outputs[0], transform_geometry.inputs[0])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (349.0, -737.800048828125)
    combine_x_y_z.bl_label = "Combine XYZ"
    # X
    combine_x_y_z.inputs[0].default_value = 0.0
    # Y
    combine_x_y_z.inputs[1].default_value = 0.0
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], transform_geometry.inputs[2])

    value_001 = nodes.new("ShaderNodeValue")
    value_001.name = "Value.001"
    value_001.label = ""
    value_001.location = (29.0, -637.800048828125)
    value_001.bl_label = "Value"
    # Links for value_001

    value_002 = nodes.new("ShaderNodeValue")
    value_002.name = "Value.002"
    value_002.label = "Longer"
    value_002.location = (29.0, -737.800048828125)
    value_002.bl_label = "Value"
    # Links for value_002

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (189.0, -637.800048828125)
    math.bl_label = "Math"
    math.operation = "ADD"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(math.outputs[0], cone_001.inputs[5])
    links.new(value_001.outputs[0], math.inputs[0])
    links.new(value_002.outputs[0], math.inputs[1])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (189.0, -677.800048828125)
    math_001.bl_label = "Math"
    math_001.operation = "MULTIPLY"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = -1.0
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(value_002.outputs[0], math_001.inputs[0])
    links.new(math_001.outputs[0], combine_x_y_z.inputs[2])

    join_geometry_016 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_016.name = "Join Geometry.016"
    join_geometry_016.label = ""
    join_geometry_016.location = (1400.0, 720.0)
    join_geometry_016.bl_label = "Join Geometry"
    # Links for join_geometry_016

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (1640.0, 640.0)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(switch.outputs[0], join_geometry_015.inputs[0])
    links.new(join_geometry_016.outputs[0], switch.inputs[2])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (1640.0, 700.0)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch.inputs[0])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.label = ""
    extrude_mesh.location = (729.0, -135.79998779296875)
    extrude_mesh.bl_label = "Extrude Mesh"
    extrude_mesh.mode = "FACES"
    # Offset
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.0020000000949949026
    # Individual
    extrude_mesh.inputs[4].default_value = False
    # Links for extrude_mesh
    links.new(join_geometry_009.outputs[0], extrude_mesh.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (29.0, -195.79998779296875)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "FLOAT_VECTOR"
    # Name
    named_attribute.inputs[0].default_value = "UVMap"
    # Links for named_attribute

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (189.0, -195.79998779296875)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(named_attribute.outputs[0], separate_x_y_z.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (349.0, -195.79998779296875)
    compare.bl_label = "Compare"
    compare.operation = "GREATER_THAN"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.7999999523162842
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513
    # Links for compare
    links.new(separate_x_y_z.outputs[1], compare.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (349.0, -35.79998779296875)
    compare_001.bl_label = "Compare"
    compare_001.operation = "LESS_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = 0.12000000476837158
    # A
    compare_001.inputs[2].default_value = 0
    # B
    compare_001.inputs[3].default_value = 0
    # A
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_001.inputs[8].default_value = ""
    # B
    compare_001.inputs[9].default_value = ""
    # C
    compare_001.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_001.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_001.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_001
    links.new(separate_x_y_z.outputs[1], compare_001.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (549.0, -115.79998779296875)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "OR"
    # Links for boolean_math
    links.new(compare_001.outputs[0], boolean_math.inputs[0])
    links.new(compare.outputs[0], boolean_math.inputs[1])
    links.new(boolean_math.outputs[0], extrude_mesh.inputs[1])

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (946.683837890625, -156.7991943359375)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "FACE"
    # Links for separate_geometry
    links.new(extrude_mesh.outputs[0], separate_geometry.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry.inputs[1])
    links.new(separate_geometry.outputs[0], pipes.inputs[0])

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.name = "Gold on Band"
    gold_on_band.label = ""
    gold_on_band.location = (1149.0, -55.79998779296875)
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.bl_label = "Group"
    # Density
    gold_on_band.inputs[1].default_value = 100000.0
    # W
    gold_on_band.inputs[2].default_value = 1.5699999332427979
    # Seed
    gold_on_band.inputs[3].default_value = 0
    # Links for gold_on_band
    links.new(separate_geometry.outputs[0], gold_on_band.inputs[0])
    links.new(gold_on_band.outputs[0], join_geometry_016.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Gold"
    frame.location = (-249.0, 875.7999877929688)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    # Parent assignments
    store_named_attribute.parent = frame_011
    transform_geometry_007.parent = frame_011
    cone.parent = frame_011
    store_named_attribute_001.parent = frame_011
    transform_geometry_009.parent = frame_011
    cone_001.parent = frame_011
    join_geometry_009.parent = frame_011
    set_position_001.parent = frame_011
    position_001.parent = frame_011
    separate_x_y_z_001.parent = frame_011
    map_range_001.parent = frame_011
    float_curve_002.parent = frame_011
    combine_x_y_z_001.parent = frame_011
    math_002.parent = frame_011
    mesh_to_curve.parent = frame_012
    mesh_to_curve_001.parent = frame_012
    bi-_rail_loft.parent = frame_012
    flip_faces_003.parent = frame_012
    set_position_002.parent = frame_012
    position_002.parent = frame_012
    vector_math.parent = frame_012
    value.parent = frame_012
    normal.parent = frame_012
    vector_math_001.parent = frame_012
    noise_texture.parent = frame_012
    position_003.parent = frame_012
    vector_math_002.parent = frame_012
    map_range_002.parent = frame_012
    rotate_vector.parent = frame_012
    pipes.parent = frame
    store_named_attribute_002.parent = frame_012
    transform_geometry.parent = frame_011
    combine_x_y_z.parent = frame_011
    value_001.parent = frame_011
    value_002.parent = frame_011
    math.parent = frame_011
    math_001.parent = frame_011
    extrude_mesh.parent = frame
    named_attribute.parent = frame
    separate_x_y_z.parent = frame
    compare.parent = frame
    compare_001.parent = frame
    boolean_math.parent = frame
    separate_geometry.parent = frame
    gold_on_band.parent = frame

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_join__splines_group():
    group_name = "Join Splines"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Curve", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (240.0, 80.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-720.0, 80.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (-400.0, 80.0)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "POINT"
    # Links for capture_attribute_001

    endpoint_selection_001 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_001.name = "Endpoint Selection.001"
    endpoint_selection_001.label = ""
    endpoint_selection_001.location = (-400.0, -40.0)
    endpoint_selection_001.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection_001.inputs[0].default_value = 1
    # End Size
    endpoint_selection_001.inputs[1].default_value = 1
    # Links for endpoint_selection_001
    links.new(endpoint_selection_001.outputs[0], capture_attribute_001.inputs[1])

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (-240.0, 80.0)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "EVALUATED"
    # Count
    curve_to_points.inputs[1].default_value = 10
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points
    links.new(capture_attribute_001.outputs[0], curve_to_points.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (-560.0, 80.0)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Evaluated"
    # Count
    resample_curve.inputs[3].default_value = 10
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve
    links.new(resample_curve.outputs[0], capture_attribute_001.inputs[0])
    links.new(group_input.outputs[0], resample_curve.inputs[0])

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.name = "Merge by Distance.002"
    merge_by_distance_002.label = ""
    merge_by_distance_002.location = (-80.0, 80.0)
    merge_by_distance_002.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_002.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_002
    links.new(curve_to_points.outputs[0], merge_by_distance_002.inputs[0])
    links.new(capture_attribute_001.outputs[1], merge_by_distance_002.inputs[1])

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    points_to_curves.label = ""
    points_to_curves.location = (80.0, 80.0)
    points_to_curves.bl_label = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0
    # Weight
    points_to_curves.inputs[2].default_value = 0.0
    # Links for points_to_curves
    links.new(merge_by_distance_002.outputs[0], points_to_curves.inputs[0])
    links.new(points_to_curves.outputs[0], group_output.inputs[0])

    # Parent assignments

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_neck_group():
    group_name = "Neck"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (12680.001953125, 400.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    quadratic_bézier_003 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_003.name = "Quadratic Bézier.003"
    quadratic_bézier_003.label = ""
    quadratic_bézier_003.location = (29.0, -35.79998779296875)
    quadratic_bézier_003.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_003.inputs[0].default_value = 40
    # Start
    quadratic_bézier_003.inputs[1].default_value = Vector((0.0, -0.13999998569488525, 0.3499999940395355))
    # Middle
    quadratic_bézier_003.inputs[2].default_value = Vector((0.0, -0.10000000149011612, 0.39500001072883606))
    # Links for quadratic_bézier_003

    bi-_rail_loft = nodes.new("GeometryNodeGroup")
    bi-_rail_loft.name = "Bi-Rail Loft.001"
    bi-_rail_loft.label = ""
    bi-_rail_loft.location = (1387.0, -631.5999145507812)
    bi-_rail_loft.node_tree = create_bi-_rail__loft_group()
    bi-_rail_loft.bl_label = "Group"
    # Smoothing
    bi-_rail_loft.inputs[3].default_value = 0
    # Menu
    bi-_rail_loft.inputs[4].default_value = "Resolution"
    # X Spacing
    bi-_rail_loft.inputs[5].default_value = 0.009999999776482582
    # Y Spacing
    bi-_rail_loft.inputs[6].default_value = 0.029999999329447746
    # X Resolution
    bi-_rail_loft.inputs[7].default_value = 42
    # Y Resolution
    bi-_rail_loft.inputs[8].default_value = 148
    # Links for bi-_rail_loft

    quadratic_bézier_004 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_004.name = "Quadratic Bézier.004"
    quadratic_bézier_004.label = ""
    quadratic_bézier_004.location = (189.0, -155.79998779296875)
    quadratic_bézier_004.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_004.inputs[0].default_value = 40
    # Middle
    quadratic_bézier_004.inputs[2].default_value = Vector((0.0, -0.07999999821186066, 0.4399999976158142))
    # End
    quadratic_bézier_004.inputs[3].default_value = Vector((0.0, -0.08999999612569809, 0.45000001788139343))
    # Links for quadratic_bézier_004

    join_splines = nodes.new("GeometryNodeGroup")
    join_splines.name = "Group.002"
    join_splines.label = ""
    join_splines.location = (369.0, -95.79998779296875)
    join_splines.node_tree = create_join__splines_group()
    join_splines.bl_label = "Group"
    # Links for join_splines

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (369.0, -35.79998779296875)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(quadratic_bézier_003.outputs[0], join_geometry_005.inputs[0])
    links.new(quadratic_bézier_004.outputs[0], join_geometry_005.inputs[0])
    links.new(join_geometry_005.outputs[0], join_splines.inputs[0])

    vector = nodes.new("FunctionNodeInputVector")
    vector.name = "Vector"
    vector.label = ""
    vector.location = (29.0, -295.79998779296875)
    vector.bl_label = "Vector"
    vector.vector = Vector((0.0, -0.08999999612569809, 0.42000001668930054))
    # Links for vector
    links.new(vector.outputs[0], quadratic_bézier_003.inputs[3])
    links.new(vector.outputs[0], quadratic_bézier_004.inputs[1])

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = "Centre Profile"
    frame_006.location = (29.0, -495.8000183105469)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    quadratic_bézier_006 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_006.name = "Quadratic Bézier.006"
    quadratic_bézier_006.label = ""
    quadratic_bézier_006.location = (29.0, -35.80000305175781)
    quadratic_bézier_006.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_006.inputs[0].default_value = 40
    # Start
    quadratic_bézier_006.inputs[1].default_value = Vector((-0.15000000596046448, 0.0, 0.429999977350235))
    # Middle
    quadratic_bézier_006.inputs[2].default_value = Vector((-0.10000000894069672, 0.0, 0.44999998807907104))
    # Links for quadratic_bézier_006

    quadratic_bézier_007 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_007.name = "Quadratic Bézier.007"
    quadratic_bézier_007.label = ""
    quadratic_bézier_007.location = (189.0, -155.8000030517578)
    quadratic_bézier_007.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_007.inputs[0].default_value = 40
    # Middle
    quadratic_bézier_007.inputs[2].default_value = Vector((-0.0650000050663948, 0.0, 0.4899999797344208))
    # End
    quadratic_bézier_007.inputs[3].default_value = Vector((-0.07500000298023224, 0.0, 0.5))
    # Links for quadratic_bézier_007

    join_splines_1 = nodes.new("GeometryNodeGroup")
    join_splines_1.name = "Group.003"
    join_splines_1.label = ""
    join_splines_1.location = (369.0, -95.80000305175781)
    join_splines_1.node_tree = create_join__splines_group()
    join_splines_1.bl_label = "Group"
    # Links for join_splines_1

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.label = ""
    join_geometry_006.location = (369.0, -35.80000305175781)
    join_geometry_006.bl_label = "Join Geometry"
    # Links for join_geometry_006
    links.new(join_geometry_006.outputs[0], join_splines_1.inputs[0])
    links.new(quadratic_bézier_006.outputs[0], join_geometry_006.inputs[0])
    links.new(quadratic_bézier_007.outputs[0], join_geometry_006.inputs[0])

    vector_001 = nodes.new("FunctionNodeInputVector")
    vector_001.name = "Vector.001"
    vector_001.label = ""
    vector_001.location = (29.0, -295.79998779296875)
    vector_001.bl_label = "Vector"
    vector_001.vector = Vector((-0.08500001579523087, 0.0, 0.4699999988079071))
    # Links for vector_001
    links.new(vector_001.outputs[0], quadratic_bézier_006.inputs[3])
    links.new(vector_001.outputs[0], quadratic_bézier_007.inputs[1])

    frame_007 = nodes.new("NodeFrame")
    frame_007.name = "Frame.007"
    frame_007.label = "Side Profile"
    frame_007.location = (29.0, -35.80000305175781)
    frame_007.bl_label = "Frame"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20
    # Links for frame_007

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_008.name = "Join Geometry.008"
    join_geometry_008.label = ""
    join_geometry_008.location = (778.0, -391.6000061035156)
    join_geometry_008.bl_label = "Join Geometry"
    # Links for join_geometry_008
    links.new(join_geometry_008.outputs[0], bi-_rail_loft.inputs[2])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    transform_geometry_002.label = ""
    transform_geometry_002.location = (549.0, -35.79998779296875)
    transform_geometry_002.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_002.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_002.inputs[2].default_value = Vector((0.0, -0.019999999552965164, 0.4800000488758087))
    # Rotation
    transform_geometry_002.inputs[3].default_value = Euler((0.4064871668815613, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_002
    links.new(transform_geometry_002.outputs[0], bi-_rail_loft.inputs[1])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    transform_geometry_003.label = ""
    transform_geometry_003.location = (549.0, -355.79998779296875)
    transform_geometry_003.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_003.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.3700000047683716))
    # Rotation
    transform_geometry_003.inputs[3].default_value = Euler((0.15620698034763336, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_003.inputs[4].default_value = Vector((1.2599999904632568, 1.0, 1.0))
    # Links for transform_geometry_003

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (189.0, -35.79998779296875)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle.inputs[4].default_value = 0.08000004291534424
    # Links for curve_circle

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.name = "Curve Circle.001"
    curve_circle_001.label = ""
    curve_circle_001.location = (189.0, -355.79998779296875)
    curve_circle_001.bl_label = "Curve Circle"
    curve_circle_001.mode = "RADIUS"
    # Point 1
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_001.inputs[4].default_value = 0.12999996542930603
    # Links for curve_circle_001

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (829.0, -395.79998779296875)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Position
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position
    links.new(transform_geometry_003.outputs[0], set_position.inputs[0])
    links.new(set_position.outputs[0], bi-_rail_loft.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (29.0, -715.7999877929688)
    position.bl_label = "Position"
    # Links for position

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (29.0, -775.7999877929688)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(position.outputs[0], separate_x_y_z.inputs[0])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (189.0, -715.7999877929688)
    map_range.bl_label = "Map Range"
    map_range.clamp = False
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    # From Min
    map_range.inputs[1].default_value = -0.14000000059604645
    # From Max
    map_range.inputs[2].default_value = 0.14000000059604645
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0
    # Steps
    map_range.inputs[5].default_value = 4.0
    # Vector
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(separate_x_y_z.outputs[1], map_range.inputs[0])

    frame_008 = nodes.new("NodeFrame")
    frame_008.name = "Frame.008"
    frame_008.label = "Profiles"
    frame_008.location = (29.0, -1119.9998779296875)
    frame_008.bl_label = "Frame"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20
    # Links for frame_008

    float_curve_001 = nodes.new("ShaderNodeFloatCurve")
    float_curve_001.name = "Float Curve.001"
    float_curve_001.label = ""
    float_curve_001.location = (349.0, -715.7999877929688)
    float_curve_001.bl_label = "Float Curve"
    # Factor
    float_curve_001.inputs[0].default_value = 1.0
    # Links for float_curve_001
    links.new(map_range.outputs[0], float_curve_001.inputs[1])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (649.0, -715.7999877929688)
    combine_x_y_z.bl_label = "Combine XYZ"
    # X
    combine_x_y_z.inputs[0].default_value = 0.0
    # Y
    combine_x_y_z.inputs[1].default_value = 0.0
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], set_position.inputs[3])
    links.new(float_curve_001.outputs[0], combine_x_y_z.inputs[2])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    transform_geometry_004.label = ""
    transform_geometry_004.location = (369.0, -355.79998779296875)
    transform_geometry_004.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_004.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    # Scale
    transform_geometry_004.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_004
    links.new(curve_circle_001.outputs[0], transform_geometry_004.inputs[0])
    links.new(transform_geometry_004.outputs[0], transform_geometry_003.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.label = ""
    transform_geometry_005.location = (369.0, -35.79998779296875)
    transform_geometry_005.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_005.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    # Scale
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_005
    links.new(transform_geometry_005.outputs[0], transform_geometry_002.inputs[0])
    links.new(curve_circle.outputs[0], transform_geometry_005.inputs[0])

    closure_input_001 = nodes.new("NodeClosureInput")
    closure_input_001.name = "Closure Input.001"
    closure_input_001.label = ""
    closure_input_001.location = (1167.0, -1051.599853515625)
    closure_input_001.bl_label = "Closure Input"
    # Links for closure_input_001

    closure_output_001 = nodes.new("NodeClosureOutput")
    closure_output_001.name = "Closure Output.001"
    closure_output_001.label = ""
    closure_output_001.location = (1647.0, -1051.599853515625)
    closure_output_001.bl_label = "Closure Output"
    closure_output_001.active_input_index = 0
    closure_output_001.active_output_index = 0
    closure_output_001.define_signature = False
    # Links for closure_output_001
    links.new(closure_output_001.outputs[0], bi-_rail_loft.inputs[9])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (1327.0, -1051.599853515625)
    math.bl_label = "Math"
    math.operation = "PINGPONG"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.25
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(closure_input_001.outputs[0], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (1487.0, -1051.599853515625)
    math_001.bl_label = "Math"
    math_001.operation = "MULTIPLY"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 4.0
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math_001.outputs[0], closure_output_001.inputs[0])
    links.new(math.outputs[0], math_001.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (529.0, -75.80000305175781)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_001.inputs[3].default_value = Euler((1.5446162223815918, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_001
    links.new(transform_geometry_001.outputs[0], join_geometry_008.inputs[0])
    links.new(join_splines_1.outputs[0], transform_geometry_001.inputs[0])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.name = "Transform Geometry.006"
    transform_geometry_006.label = ""
    transform_geometry_006.location = (529.0, -95.79998779296875)
    transform_geometry_006.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_006.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_006.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')
    # Scale
    transform_geometry_006.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_006
    links.new(transform_geometry_006.outputs[0], join_geometry_008.inputs[0])
    links.new(join_splines.outputs[0], transform_geometry_006.inputs[0])

    integer = nodes.new("FunctionNodeInputInt")
    integer.name = "Integer"
    integer.label = ""
    integer.location = (189.0, -215.79998779296875)
    integer.bl_label = "Integer"
    integer.integer = 73
    # Links for integer
    links.new(integer.outputs[0], curve_circle_001.inputs[0])
    links.new(integer.outputs[0], curve_circle.inputs[0])

    frame_009 = nodes.new("NodeFrame")
    frame_009.name = "Frame.009"
    frame_009.label = "Neck Rails"
    frame_009.location = (38.0, -35.7999267578125)
    frame_009.bl_label = "Frame"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20
    # Links for frame_009

    frame_010 = nodes.new("NodeFrame")
    frame_010.name = "Frame.010"
    frame_010.label = "Neck"
    frame_010.location = (-1287.0, 951.5999145507812)
    frame_010.bl_label = "Frame"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20
    # Links for frame_010

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (2840.0, -300.0)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "FACE"
    # Links for delete_geometry

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (2680.0, -460.0)
    position_001.bl_label = "Position"
    # Links for position_001

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (2680.0, -520.0)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001
    links.new(position_001.outputs[0], separate_x_y_z_001.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (2840.0, -460.0)
    compare.bl_label = "Compare"
    compare.operation = "GREATER_EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.0
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513
    # Links for compare
    links.new(separate_x_y_z_001.outputs[0], compare.inputs[0])
    links.new(compare.outputs[0], delete_geometry.inputs[1])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.name = "Pipes"
    pipes.label = ""
    pipes.location = (749.0, -95.80000305175781)
    pipes.node_tree = create_pipes_group()
    pipes.bl_label = "Group"
    # Links for pipes

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (2480.0, -320.0)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(join_geometry.outputs[0], delete_geometry.inputs[0])
    links.new(bi-_rail_loft.outputs[0], join_geometry.inputs[0])
    links.new(pipes.outputs[0], join_geometry.inputs[0])

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_002.name = "Separate XYZ.002"
    separate_x_y_z_002.label = ""
    separate_x_y_z_002.location = (29.0, -35.80000305175781)
    separate_x_y_z_002.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_002
    links.new(bi-_rail_loft.outputs[2], separate_x_y_z_002.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (189.0, -35.80000305175781)
    compare_001.bl_label = "Compare"
    compare_001.operation = "EQUAL"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = 0.8799999356269836
    # A
    compare_001.inputs[2].default_value = 0
    # B
    compare_001.inputs[3].default_value = 0
    # A
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_001.inputs[8].default_value = ""
    # B
    compare_001.inputs[9].default_value = ""
    # C
    compare_001.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_001.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_001.inputs[12].default_value = 0.02099999599158764
    # Links for compare_001
    links.new(separate_x_y_z_002.outputs[0], compare_001.inputs[0])

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (349.0, -35.80000305175781)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "POINT"
    # Links for separate_geometry
    links.new(bi-_rail_loft.outputs[0], separate_geometry.inputs[0])
    links.new(compare_001.outputs[0], separate_geometry.inputs[1])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (549.0, -75.80000305175781)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(join_geometry_001.outputs[0], pipes.inputs[0])
    links.new(bi-_rail_loft.outputs[0], join_geometry_001.inputs[0])
    links.new(separate_geometry.outputs[0], join_geometry_001.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Pipes"
    frame.location = (1351.0, -24.19999885559082)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    rivet = nodes.new("GeometryNodeGroup")
    rivet.name = "Rivet"
    rivet.label = ""
    rivet.location = (1520.0, -520.0)
    rivet.node_tree = create_rivet_group()
    rivet.bl_label = "Group"
    # Corners
    rivet.inputs[1].default_value = False
    # Offset
    rivet.inputs[2].default_value = -1.059999942779541
    # Spacing
    rivet.inputs[3].default_value = 0.9399999976158142
    # Links for rivet
    links.new(bi-_rail_loft.outputs[0], rivet.inputs[0])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (1700.0, -520.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(realize_instances.outputs[0], join_geometry.inputs[0])
    links.new(rivet.outputs[0], realize_instances.inputs[0])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (3080.0, -300.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True
    # Links for set_shade_smooth
    links.new(delete_geometry.outputs[0], set_shade_smooth.inputs[0])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (6677.9990234375, -3251.60009765625)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (6837.9990234375, -3251.60009765625)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(join_geometry_002.outputs[0], switch.inputs[2])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (6638.0, -3191.60009765625)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch.inputs[0])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    set_spline_cyclic.label = ""
    set_spline_cyclic.location = (458.0, -2031.60009765625)
    set_spline_cyclic.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = False
    # Links for set_spline_cyclic
    links.new(set_position.outputs[0], set_spline_cyclic.inputs[0])

    trim_curve = nodes.new("GeometryNodeTrimCurve")
    trim_curve.name = "Trim Curve"
    trim_curve.label = ""
    trim_curve.location = (29.0, -29.0)
    trim_curve.bl_label = "Trim Curve"
    trim_curve.mode = "FACTOR"
    # Selection
    trim_curve.inputs[1].default_value = True
    # Start
    trim_curve.inputs[2].default_value = 0.0
    # End
    trim_curve.inputs[3].default_value = 0.5074577331542969
    # Start
    trim_curve.inputs[4].default_value = 0.0
    # End
    trim_curve.inputs[5].default_value = 1.0
    # Links for trim_curve
    links.new(set_spline_cyclic.outputs[0], trim_curve.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (189.0, -29.0)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Count"
    # Count
    resample_curve_001.inputs[3].default_value = 47
    # Length
    resample_curve_001.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_001
    links.new(trim_curve.outputs[0], resample_curve_001.inputs[0])

    gold_decorations = nodes.new("GeometryNodeGroup")
    gold_decorations.name = "Group.006"
    gold_decorations.label = ""
    gold_decorations.location = (529.0, -29.0)
    gold_decorations.node_tree = create_gold__decorations_group()
    gold_decorations.bl_label = "Group"
    # Seed
    gold_decorations.inputs[1].default_value = 68
    # Scale
    gold_decorations.inputs[2].default_value = 2.6999993324279785
    # Count
    gold_decorations.inputs[3].default_value = 56
    # Links for gold_decorations
    links.new(gold_decorations.outputs[0], join_geometry_002.inputs[0])

    set_curve_normal = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal.name = "Set Curve Normal"
    set_curve_normal.label = ""
    set_curve_normal.location = (349.0, -29.0)
    set_curve_normal.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal.inputs[1].default_value = True
    # Mode
    set_curve_normal.inputs[2].default_value = "Free"
    # Links for set_curve_normal
    links.new(set_curve_normal.outputs[0], gold_decorations.inputs[0])
    links.new(resample_curve_001.outputs[0], set_curve_normal.inputs[0])

    sample_nearest_surface = nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.name = "Sample Nearest Surface"
    sample_nearest_surface.label = ""
    sample_nearest_surface.location = (438.0, -2291.60009765625)
    sample_nearest_surface.bl_label = "Sample Nearest Surface"
    sample_nearest_surface.data_type = "FLOAT_VECTOR"
    # Group ID
    sample_nearest_surface.inputs[2].default_value = 0
    # Sample Position
    sample_nearest_surface.inputs[3].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    sample_nearest_surface.inputs[4].default_value = 0
    # Links for sample_nearest_surface
    links.new(bi-_rail_loft.outputs[0], sample_nearest_surface.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.label = ""
    normal.location = (438.0, -2511.60009765625)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = False
    # Links for normal
    links.new(normal.outputs[0], sample_nearest_surface.inputs[1])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (189.0, -189.0)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "CROSS_PRODUCT"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(vector_math.outputs[0], set_curve_normal.inputs[3])
    links.new(sample_nearest_surface.outputs[0], vector_math.inputs[0])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (189.0, -329.0)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent
    links.new(curve_tangent.outputs[0], vector_math.inputs[1])

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = ""
    frame_005.location = (1309.0, -1702.60009765625)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.name = "Group.007"
    gold_on_band.label = ""
    gold_on_band.location = (1129.0, -335.800048828125)
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.bl_label = "Group"
    # Density
    gold_on_band.inputs[1].default_value = 100000.0
    # W
    gold_on_band.inputs[2].default_value = 8.669999122619629
    # Seed
    gold_on_band.inputs[3].default_value = 1
    # Links for gold_on_band

    frame_011 = nodes.new("NodeFrame")
    frame_011.name = "Frame.011"
    frame_011.label = "Gold"
    frame_011.location = (2422.0, 5711.60009765625)
    frame_011.bl_label = "Frame"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20
    # Links for frame_011

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.name = "Gem in Holder"
    gem_in_holder.label = ""
    gem_in_holder.location = (1249.0, -155.800048828125)
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.bl_label = "Group"
    # Gem Radius
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder.inputs[2].default_value = False
    # Scale
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    # Wings
    gem_in_holder.inputs[6].default_value = True
    # Links for gem_in_holder

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (389.0, -415.800048828125)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "COUNT"
    # Count
    curve_to_points.inputs[1].default_value = 8
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points

    for_each_geometry_element_input = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input.name = "For Each Geometry Element Input"
    for_each_geometry_element_input.label = ""
    for_each_geometry_element_input.location = (549.0, -415.800048828125)
    for_each_geometry_element_input.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input.inputs[1].default_value = True
    # Links for for_each_geometry_element_input
    links.new(curve_to_points.outputs[0], for_each_geometry_element_input.inputs[0])
    links.new(curve_to_points.outputs[3], for_each_geometry_element_input.inputs[2])

    for_each_geometry_element_output = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.name = "For Each Geometry Element Output"
    for_each_geometry_element_output.label = ""
    for_each_geometry_element_output.location = (2069.0, -475.800048828125)
    for_each_geometry_element_output.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output.active_input_index = 1
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = "POINT"
    for_each_geometry_element_output.inspection_index = 0
    # Links for for_each_geometry_element_output
    links.new(for_each_geometry_element_output.outputs[2], join_geometry_002.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (389.0, -615.800048828125)
    position_002.bl_label = "Position"
    # Links for position_002
    links.new(position_002.outputs[0], for_each_geometry_element_input.inputs[3])

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.name = "Transform Geometry.007"
    transform_geometry_007.label = ""
    transform_geometry_007.location = (1529.0, -475.800048828125)
    transform_geometry_007.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_007.inputs[1].default_value = "Components"
    # Links for transform_geometry_007
    links.new(gem_in_holder.outputs[0], transform_geometry_007.inputs[0])
    links.new(for_each_geometry_element_input.outputs[3], transform_geometry_007.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.name = "Rotate Rotation"
    rotate_rotation.label = ""
    rotate_rotation.location = (1189.0, -675.800048828125)
    rotate_rotation.bl_label = "Rotate Rotation"
    rotate_rotation.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation.inputs[1].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')
    # Links for rotate_rotation
    links.new(for_each_geometry_element_input.outputs[2], rotate_rotation.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (789.0, -395.800048828125)
    random_value.bl_label = "Random Value"
    random_value.data_type = "INT"
    # Min
    random_value.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value.inputs[2].default_value = 0.0
    # Max
    random_value.inputs[3].default_value = 1.0
    # Min
    random_value.inputs[4].default_value = 5
    # Max
    random_value.inputs[5].default_value = 7
    # Probability
    random_value.inputs[6].default_value = 0.5
    # Seed
    random_value.inputs[8].default_value = 0
    # Links for random_value
    links.new(for_each_geometry_element_input.outputs[0], random_value.inputs[7])
    links.new(random_value.outputs[2], gem_in_holder.inputs[7])

    transform_geometry_008 = nodes.new("GeometryNodeTransform")
    transform_geometry_008.name = "Transform Geometry.008"
    transform_geometry_008.label = ""
    transform_geometry_008.location = (1709.0, -475.800048828125)
    transform_geometry_008.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_008.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_008.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    # Rotation
    transform_geometry_008.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_008.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_008
    links.new(transform_geometry_007.outputs[0], transform_geometry_008.inputs[0])
    links.new(transform_geometry_008.outputs[0], for_each_geometry_element_output.inputs[1])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.label = ""
    random_value_001.location = (769.0, -615.800048828125)
    random_value_001.bl_label = "Random Value"
    random_value_001.data_type = "FLOAT"
    # Min
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_001.inputs[2].default_value = 0.3499999940395355
    # Max
    random_value_001.inputs[3].default_value = 0.75
    # Min
    random_value_001.inputs[4].default_value = 0
    # Max
    random_value_001.inputs[5].default_value = 100
    # Probability
    random_value_001.inputs[6].default_value = 0.5
    # Seed
    random_value_001.inputs[8].default_value = 0
    # Links for random_value_001
    links.new(for_each_geometry_element_input.outputs[0], random_value_001.inputs[7])
    links.new(random_value_001.outputs[1], transform_geometry_007.inputs[4])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (2329.0, -95.13330078125)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001

    random_value_002 = nodes.new("FunctionNodeRandomValue")
    random_value_002.name = "Random Value.002"
    random_value_002.label = ""
    random_value_002.location = (789.0, -215.800048828125)
    random_value_002.bl_label = "Random Value"
    random_value_002.data_type = "FLOAT"
    # Min
    random_value_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_002.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_002.inputs[2].default_value = 0.0
    # Max
    random_value_002.inputs[3].default_value = 100.0
    # Min
    random_value_002.inputs[4].default_value = 3
    # Max
    random_value_002.inputs[5].default_value = 7
    # Probability
    random_value_002.inputs[6].default_value = 0.5
    # Seed
    random_value_002.inputs[8].default_value = 24
    # Links for random_value_002
    links.new(for_each_geometry_element_input.outputs[0], random_value_002.inputs[7])
    links.new(random_value_002.outputs[1], gem_in_holder.inputs[10])

    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.name = "Rotate Rotation.001"
    rotate_rotation_001.label = ""
    rotate_rotation_001.location = (1349.0, -675.800048828125)
    rotate_rotation_001.bl_label = "Rotate Rotation"
    rotate_rotation_001.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_001.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
    # Links for rotate_rotation_001
    links.new(rotate_rotation_001.outputs[0], transform_geometry_007.inputs[3])
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])

    random_value_003 = nodes.new("FunctionNodeRandomValue")
    random_value_003.name = "Random Value.003"
    random_value_003.label = ""
    random_value_003.location = (789.0, -35.800048828125)
    random_value_003.bl_label = "Random Value"
    random_value_003.data_type = "FLOAT"
    # Min
    random_value_003.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_003.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_003.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_003.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_003.inputs[4].default_value = 3
    # Max
    random_value_003.inputs[5].default_value = 7
    # Probability
    random_value_003.inputs[6].default_value = 0.5
    # Seed
    random_value_003.inputs[8].default_value = 0
    # Links for random_value_003
    links.new(for_each_geometry_element_input.outputs[0], random_value_003.inputs[7])
    links.new(random_value_003.outputs[1], gem_in_holder.inputs[9])

    random_value_004 = nodes.new("FunctionNodeRandomValue")
    random_value_004.name = "Random Value.004"
    random_value_004.label = ""
    random_value_004.location = (1029.0, -255.800048828125)
    random_value_004.bl_label = "Random Value"
    random_value_004.data_type = "INT"
    # Min
    random_value_004.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_004.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_004.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_004.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_004.inputs[4].default_value = 0
    # Max
    random_value_004.inputs[5].default_value = 100
    # Probability
    random_value_004.inputs[6].default_value = 0.5
    # Seed
    random_value_004.inputs[8].default_value = 0
    # Links for random_value_004
    links.new(for_each_geometry_element_input.outputs[0], random_value_004.inputs[7])
    links.new(random_value_004.outputs[2], gem_in_holder.inputs[5])

    random_value_005 = nodes.new("FunctionNodeRandomValue")
    random_value_005.name = "Random Value.005"
    random_value_005.label = ""
    random_value_005.location = (1029.0, -75.800048828125)
    random_value_005.bl_label = "Random Value"
    random_value_005.data_type = "INT"
    # Min
    random_value_005.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_005.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_005.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_005.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_005.inputs[4].default_value = 6
    # Max
    random_value_005.inputs[5].default_value = 20
    # Probability
    random_value_005.inputs[6].default_value = 0.5
    # Seed
    random_value_005.inputs[8].default_value = 0
    # Links for random_value_005
    links.new(for_each_geometry_element_input.outputs[0], random_value_005.inputs[7])
    links.new(random_value_005.outputs[2], gem_in_holder.inputs[4])

    random_value_006 = nodes.new("FunctionNodeRandomValue")
    random_value_006.name = "Random Value.006"
    random_value_006.label = ""
    random_value_006.location = (1029.0, -435.800048828125)
    random_value_006.bl_label = "Random Value"
    random_value_006.data_type = "INT"
    # Min
    random_value_006.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_006.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_006.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_006.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_006.inputs[4].default_value = 5
    # Max
    random_value_006.inputs[5].default_value = 30
    # Probability
    random_value_006.inputs[6].default_value = 0.5
    # Seed
    random_value_006.inputs[8].default_value = 0
    # Links for random_value_006
    links.new(for_each_geometry_element_input.outputs[0], random_value_006.inputs[7])
    links.new(random_value_006.outputs[2], gem_in_holder.inputs[8])

    frame_012 = nodes.new("NodeFrame")
    frame_012.name = "Frame.012"
    frame_012.label = "Broaches"
    frame_012.location = (729.0, -2155.800048828125)
    frame_012.bl_label = "Frame"
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20
    # Links for frame_012

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.name = "Separate Geometry.001"
    separate_geometry_001.label = ""
    separate_geometry_001.location = (969.0, -335.800048828125)
    separate_geometry_001.bl_label = "Separate Geometry"
    separate_geometry_001.domain = "FACE"
    # Links for separate_geometry_001
    links.new(bi-_rail_loft.outputs[0], separate_geometry_001.inputs[0])
    links.new(separate_geometry_001.outputs[0], gold_on_band.inputs[0])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_003.name = "Separate XYZ.003"
    separate_x_y_z_003.label = ""
    separate_x_y_z_003.location = (29.0, -195.800048828125)
    separate_x_y_z_003.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_003
    links.new(bi-_rail_loft.outputs[2], separate_x_y_z_003.inputs[0])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.label = ""
    compare_002.location = (269.0, -35.800048828125)
    compare_002.bl_label = "Compare"
    compare_002.operation = "GREATER_THAN"
    compare_002.data_type = "FLOAT"
    compare_002.mode = "ELEMENT"
    # B
    compare_002.inputs[1].default_value = 0.8700000047683716
    # A
    compare_002.inputs[2].default_value = 0
    # B
    compare_002.inputs[3].default_value = 0
    # A
    compare_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_002.inputs[8].default_value = ""
    # B
    compare_002.inputs[9].default_value = ""
    # C
    compare_002.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_002.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_002.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_002
    links.new(separate_x_y_z_003.outputs[0], compare_002.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (12340.001953125, 360.0)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(join_geometry_004.outputs[0], group_output.inputs[0])
    links.new(set_shade_smooth.outputs[0], join_geometry_004.inputs[0])
    links.new(switch.outputs[0], join_geometry_004.inputs[0])

    trim_curve_001 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_001.name = "Trim Curve.001"
    trim_curve_001.label = ""
    trim_curve_001.location = (29.0, -415.800048828125)
    trim_curve_001.bl_label = "Trim Curve"
    trim_curve_001.mode = "FACTOR"
    # Selection
    trim_curve_001.inputs[1].default_value = True
    # Start
    trim_curve_001.inputs[2].default_value = 0.18784530460834503
    # End
    trim_curve_001.inputs[3].default_value = 0.46817636489868164
    # Start
    trim_curve_001.inputs[4].default_value = 0.0
    # End
    trim_curve_001.inputs[5].default_value = 1.0
    # Links for trim_curve_001
    links.new(set_spline_cyclic.outputs[0], trim_curve_001.inputs[0])

    set_curve_normal_001 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.name = "Set Curve Normal.001"
    set_curve_normal_001.label = ""
    set_curve_normal_001.location = (209.0, -395.800048828125)
    set_curve_normal_001.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_001.inputs[1].default_value = True
    # Mode
    set_curve_normal_001.inputs[2].default_value = "Free"
    # Links for set_curve_normal_001
    links.new(set_curve_normal_001.outputs[0], curve_to_points.inputs[0])
    links.new(trim_curve_001.outputs[0], set_curve_normal_001.inputs[0])
    links.new(sample_nearest_surface.outputs[0], set_curve_normal_001.inputs[3])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (269.0, -195.800048828125)
    compare_003.bl_label = "Compare"
    compare_003.operation = "LESS_THAN"
    compare_003.data_type = "FLOAT"
    compare_003.mode = "ELEMENT"
    # B
    compare_003.inputs[1].default_value = 0.25999999046325684
    # A
    compare_003.inputs[2].default_value = 0
    # B
    compare_003.inputs[3].default_value = 0
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
    links.new(separate_x_y_z_003.outputs[0], compare_003.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (429.0, -55.800048828125)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "OR"
    # Links for boolean_math
    links.new(compare_002.outputs[0], boolean_math.inputs[0])
    links.new(compare_003.outputs[0], boolean_math.inputs[1])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.label = ""
    boolean_math_001.location = (609.0, -215.800048828125)
    boolean_math_001.bl_label = "Boolean Math"
    boolean_math_001.operation = "OR"
    # Links for boolean_math_001
    links.new(boolean_math.outputs[0], boolean_math_001.inputs[0])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (269.0, -355.800048828125)
    compare_004.bl_label = "Compare"
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    # B
    compare_004.inputs[1].default_value = 0.5
    # A
    compare_004.inputs[2].default_value = 0
    # B
    compare_004.inputs[3].default_value = 0
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
    compare_004.inputs[12].default_value = 0.020999997854232788
    # Links for compare_004
    links.new(separate_x_y_z_003.outputs[1], compare_004.inputs[0])
    links.new(compare_004.outputs[0], boolean_math_001.inputs[1])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "On Band"
    frame_001.location = (29.0, -3255.800048828125)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.label = ""
    boolean_math_002.location = (789.0, -255.800048828125)
    boolean_math_002.bl_label = "Boolean Math"
    boolean_math_002.operation = "AND"
    # Links for boolean_math_002
    links.new(boolean_math_002.outputs[0], separate_geometry_001.inputs[1])
    links.new(boolean_math_001.outputs[0], boolean_math_002.inputs[0])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (269.0, -535.800048828125)
    compare_005.bl_label = "Compare"
    compare_005.operation = "LESS_THAN"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    # B
    compare_005.inputs[1].default_value = 0.5
    # A
    compare_005.inputs[2].default_value = 0
    # B
    compare_005.inputs[3].default_value = 0
    # A
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_005.inputs[8].default_value = ""
    # B
    compare_005.inputs[9].default_value = ""
    # C
    compare_005.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_005.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_005.inputs[12].default_value = 0.020999997854232788
    # Links for compare_005
    links.new(separate_x_y_z_003.outputs[1], compare_005.inputs[0])
    links.new(compare_005.outputs[0], boolean_math_002.inputs[1])

    gem_in_holder_1 = nodes.new("GeometryNodeGroup")
    gem_in_holder_1.name = "Gem in Holder.001"
    gem_in_holder_1.label = ""
    gem_in_holder_1.location = (1349.0, -75.13330078125)
    gem_in_holder_1.node_tree = create_gem_in__holder_group()
    gem_in_holder_1.bl_label = "Group"
    # Gem Radius
    gem_in_holder_1.inputs[0].default_value = 0.009999990463256836
    # Gem Material
    gem_in_holder_1.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_1.inputs[2].default_value = False
    # Scale
    gem_in_holder_1.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_1.inputs[4].default_value = 20
    # Seed
    gem_in_holder_1.inputs[5].default_value = 10
    # Wings
    gem_in_holder_1.inputs[6].default_value = False
    # Array Count
    gem_in_holder_1.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_1.inputs[8].default_value = 10
    # Links for gem_in_holder_1

    mesh_to_curve_002 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.name = "Mesh to Curve.002"
    mesh_to_curve_002.label = ""
    mesh_to_curve_002.location = (29.0, -55.13330078125)
    mesh_to_curve_002.bl_label = "Mesh to Curve"
    mesh_to_curve_002.mode = "EDGES"
    # Links for mesh_to_curve_002
    links.new(separate_geometry_001.outputs[0], mesh_to_curve_002.inputs[0])

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Is Edge Boundary"
    is_edge_boundary.label = ""
    is_edge_boundary.location = (29.0, -175.13330078125)
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    is_edge_boundary.bl_label = "Group"
    # Links for is_edge_boundary
    links.new(is_edge_boundary.outputs[0], mesh_to_curve_002.inputs[1])

    set_spline_cyclic_001 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_001.name = "Set Spline Cyclic.001"
    set_spline_cyclic_001.label = ""
    set_spline_cyclic_001.location = (349.0, -55.13330078125)
    set_spline_cyclic_001.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic_001.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic_001.inputs[2].default_value = False
    # Links for set_spline_cyclic_001

    trim_curve_004 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_004.name = "Trim Curve.004"
    trim_curve_004.label = ""
    trim_curve_004.location = (509.0, -55.13330078125)
    trim_curve_004.bl_label = "Trim Curve"
    trim_curve_004.mode = "FACTOR"
    # Selection
    trim_curve_004.inputs[1].default_value = True
    # Start
    trim_curve_004.inputs[2].default_value = 0.03867403417825699
    # End
    trim_curve_004.inputs[3].default_value = 0.4364641308784485
    # Start
    trim_curve_004.inputs[4].default_value = 0.0
    # End
    trim_curve_004.inputs[5].default_value = 1.0
    # Links for trim_curve_004
    links.new(set_spline_cyclic_001.outputs[0], trim_curve_004.inputs[0])

    curve_to_points_001 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.name = "Curve to Points.001"
    curve_to_points_001.label = ""
    curve_to_points_001.location = (669.0, -55.13330078125)
    curve_to_points_001.bl_label = "Curve to Points"
    curve_to_points_001.mode = "COUNT"
    # Count
    curve_to_points_001.inputs[1].default_value = 50
    # Length
    curve_to_points_001.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points_001
    links.new(trim_curve_004.outputs[0], curve_to_points_001.inputs[0])

    set_curve_normal_002 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_002.name = "Set Curve Normal.002"
    set_curve_normal_002.label = ""
    set_curve_normal_002.location = (189.0, -55.13330078125)
    set_curve_normal_002.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_002.inputs[1].default_value = True
    # Mode
    set_curve_normal_002.inputs[2].default_value = "Free"
    # Links for set_curve_normal_002
    links.new(set_curve_normal_002.outputs[0], set_spline_cyclic_001.inputs[0])
    links.new(mesh_to_curve_002.outputs[0], set_curve_normal_002.inputs[0])
    links.new(sample_nearest_surface.outputs[0], set_curve_normal_002.inputs[3])

    position_004 = nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"
    position_004.label = ""
    position_004.location = (669.0, -255.13330078125)
    position_004.bl_label = "Position"
    # Links for position_004

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.name = "For Each Geometry Element Input.001"
    for_each_geometry_element_input_001.label = ""
    for_each_geometry_element_input_001.location = (829.0, -55.13330078125)
    for_each_geometry_element_input_001.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input_001.inputs[1].default_value = True
    # Links for for_each_geometry_element_input_001
    links.new(curve_to_points_001.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(position_004.outputs[0], for_each_geometry_element_input_001.inputs[2])
    links.new(curve_to_points_001.outputs[3], for_each_geometry_element_input_001.inputs[3])

    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.name = "For Each Geometry Element Output.001"
    for_each_geometry_element_output_001.label = ""
    for_each_geometry_element_output_001.location = (2509.0, -75.13330078125)
    for_each_geometry_element_output_001.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    # Links for for_each_geometry_element_output_001
    links.new(store_named_attribute_001.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_002.inputs[0])

    transform_geometry_009 = nodes.new("GeometryNodeTransform")
    transform_geometry_009.name = "Transform Geometry.009"
    transform_geometry_009.label = ""
    transform_geometry_009.location = (1609.0, -75.13330078125)
    transform_geometry_009.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_009.inputs[1].default_value = "Components"
    # Scale
    transform_geometry_009.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_009
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_009.inputs[2])
    links.new(gem_in_holder_1.outputs[4], transform_geometry_009.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.name = "Rotate Rotation.002"
    rotate_rotation_002.label = ""
    rotate_rotation_002.location = (1009.0, -295.13330078125)
    rotate_rotation_002.bl_label = "Rotate Rotation"
    rotate_rotation_002.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, -1.5707963705062866, 0.0), 'XYZ')
    # Links for rotate_rotation_002
    links.new(rotate_rotation_002.outputs[0], transform_geometry_009.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[3], rotate_rotation_002.inputs[0])

    frame_014 = nodes.new("NodeFrame")
    frame_014.name = "Frame.014"
    frame_014.label = "Random Wings"
    frame_014.location = (1449.0, -3056.466796875)
    frame_014.bl_label = "Frame"
    frame_014.text = None
    frame_014.shrink = True
    frame_014.label_size = 20
    # Links for frame_014

    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.name = "Random Value.007"
    random_value_007.label = ""
    random_value_007.location = (1169.0, -55.13330078125)
    random_value_007.bl_label = "Random Value"
    random_value_007.data_type = "FLOAT"
    # Min
    random_value_007.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_007.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_007.inputs[2].default_value = 6.0
    # Max
    random_value_007.inputs[3].default_value = 7.0
    # Min
    random_value_007.inputs[4].default_value = 0
    # Max
    random_value_007.inputs[5].default_value = 100
    # Probability
    random_value_007.inputs[6].default_value = 0.5
    # Seed
    random_value_007.inputs[8].default_value = 33
    # Links for random_value_007
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_1.inputs[10])

    random_value_008 = nodes.new("FunctionNodeRandomValue")
    random_value_008.name = "Random Value.008"
    random_value_008.label = ""
    random_value_008.location = (1169.0, -235.13330078125)
    random_value_008.bl_label = "Random Value"
    random_value_008.data_type = "FLOAT"
    # Min
    random_value_008.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_008.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_008.inputs[2].default_value = 0.0
    # Max
    random_value_008.inputs[3].default_value = 0.003000000026077032
    # Min
    random_value_008.inputs[4].default_value = 0
    # Max
    random_value_008.inputs[5].default_value = 100
    # Probability
    random_value_008.inputs[6].default_value = 0.5
    # Seed
    random_value_008.inputs[8].default_value = 10
    # Links for random_value_008
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_008.inputs[7])
    links.new(random_value_008.outputs[1], gem_in_holder_1.inputs[9])

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.name = "Distribute Points on Faces"
    distribute_points_on_faces.label = ""
    distribute_points_on_faces.location = (209.0, -35.7999267578125)
    distribute_points_on_faces.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    # Selection
    distribute_points_on_faces.inputs[1].default_value = True
    # Distance Min
    distribute_points_on_faces.inputs[2].default_value = 0.0
    # Density Max
    distribute_points_on_faces.inputs[3].default_value = 10.0
    # Density
    distribute_points_on_faces.inputs[4].default_value = 5000.0
    # Density Factor
    distribute_points_on_faces.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces.inputs[6].default_value = 1
    # Links for distribute_points_on_faces
    links.new(separate_geometry_001.outputs[0], distribute_points_on_faces.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (509.0, -55.7999267578125)
    instance_on_points.bl_label = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Rotation
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for instance_on_points
    links.new(distribute_points_on_faces.outputs[0], instance_on_points.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    ico_sphere.label = ""
    ico_sphere.location = (29.0, -255.7999267578125)
    ico_sphere.bl_label = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.004000000189989805
    # Subdivisions
    ico_sphere.inputs[1].default_value = 2
    # Links for ico_sphere

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (689.0, -55.7999267578125)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "INSTANCE"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "ruby"
    # Links for store_named_attribute_002
    links.new(instance_on_points.outputs[0], store_named_attribute_002.inputs[0])

    random_value_009 = nodes.new("FunctionNodeRandomValue")
    random_value_009.name = "Random Value.009"
    random_value_009.label = ""
    random_value_009.location = (689.0, -215.7999267578125)
    random_value_009.bl_label = "Random Value"
    random_value_009.data_type = "BOOLEAN"
    # Min
    random_value_009.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_009.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_009.inputs[2].default_value = 0.0
    # Max
    random_value_009.inputs[3].default_value = 1.0
    # Min
    random_value_009.inputs[4].default_value = 0
    # Max
    random_value_009.inputs[5].default_value = 100
    # Probability
    random_value_009.inputs[6].default_value = 0.5
    # ID
    random_value_009.inputs[7].default_value = 0
    # Seed
    random_value_009.inputs[8].default_value = 0
    # Links for random_value_009
    links.new(random_value_009.outputs[3], store_named_attribute_002.inputs[3])

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.label = ""
    boolean_math_003.location = (869.0, -215.7999267578125)
    boolean_math_003.bl_label = "Boolean Math"
    boolean_math_003.operation = "NOT"
    # Boolean
    boolean_math_003.inputs[1].default_value = False
    # Links for boolean_math_003
    links.new(random_value_009.outputs[3], boolean_math_003.inputs[0])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (869.0, -55.7999267578125)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "INSTANCE"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "saphire"
    # Links for store_named_attribute_003
    links.new(store_named_attribute_002.outputs[0], store_named_attribute_003.inputs[0])
    links.new(boolean_math_003.outputs[0], store_named_attribute_003.inputs[3])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.label = ""
    realize_instances_001.location = (1029.0, -55.7999267578125)
    realize_instances_001.bl_label = "Realize Instances"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0
    # Links for realize_instances_001
    links.new(store_named_attribute_003.outputs[0], realize_instances_001.inputs[0])
    links.new(realize_instances_001.outputs[0], join_geometry_002.inputs[0])

    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.name = "Set Shade Smooth.003"
    set_shade_smooth_003.label = ""
    set_shade_smooth_003.location = (209.0, -255.7999267578125)
    set_shade_smooth_003.bl_label = "Set Shade Smooth"
    set_shade_smooth_003.domain = "FACE"
    # Selection
    set_shade_smooth_003.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_003.inputs[2].default_value = True
    # Links for set_shade_smooth_003
    links.new(set_shade_smooth_003.outputs[0], instance_on_points.inputs[2])
    links.new(ico_sphere.outputs[0], set_shade_smooth_003.inputs[0])

    frame_015 = nodes.new("NodeFrame")
    frame_015.name = "Frame.015"
    frame_015.label = "Random Jewels"
    frame_015.location = (2169.0, -3975.80029296875)
    frame_015.bl_label = "Frame"
    frame_015.text = None
    frame_015.shrink = True
    frame_015.label_size = 20
    # Links for frame_015

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (209.0, -75.7999267578125)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001
    links.new(bi-_rail_loft.outputs[0], reroute_001.inputs[0])

    distribute_points_on_faces_001 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_001.name = "Distribute Points on Faces.001"
    distribute_points_on_faces_001.label = ""
    distribute_points_on_faces_001.location = (409.0, -35.7999267578125)
    distribute_points_on_faces_001.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces_001.distribute_method = "POISSON"
    distribute_points_on_faces_001.use_legacy_normal = False
    # Distance Min
    distribute_points_on_faces_001.inputs[2].default_value = 0.009999999776482582
    # Density Max
    distribute_points_on_faces_001.inputs[3].default_value = 5000.0
    # Density
    distribute_points_on_faces_001.inputs[4].default_value = 500.0
    # Density Factor
    distribute_points_on_faces_001.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces_001.inputs[6].default_value = 0
    # Links for distribute_points_on_faces_001
    links.new(reroute_001.outputs[0], distribute_points_on_faces_001.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (29.0, -195.7999267578125)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "POINTS"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity
    links.new(for_each_geometry_element_output_001.outputs[2], geometry_proximity.inputs[0])

    compare_006 = nodes.new("FunctionNodeCompare")
    compare_006.name = "Compare.006"
    compare_006.label = ""
    compare_006.location = (249.0, -195.7999267578125)
    compare_006.bl_label = "Compare"
    compare_006.operation = "LESS_THAN"
    compare_006.data_type = "FLOAT"
    compare_006.mode = "ELEMENT"
    # B
    compare_006.inputs[1].default_value = 0.0010000000474974513
    # A
    compare_006.inputs[2].default_value = 0
    # B
    compare_006.inputs[3].default_value = 0
    # A
    compare_006.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_006.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_006.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_006.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_006.inputs[8].default_value = ""
    # B
    compare_006.inputs[9].default_value = ""
    # C
    compare_006.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_006.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_006.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_006
    links.new(geometry_proximity.outputs[1], compare_006.inputs[0])
    links.new(compare_006.outputs[0], distribute_points_on_faces_001.inputs[1])

    gem_in_holder_2 = nodes.new("GeometryNodeGroup")
    gem_in_holder_2.name = "Gem in Holder.002"
    gem_in_holder_2.label = ""
    gem_in_holder_2.location = (29.0, -415.7999267578125)
    gem_in_holder_2.node_tree = create_gem_in__holder_group()
    gem_in_holder_2.bl_label = "Group"
    # Gem Radius
    gem_in_holder_2.inputs[0].default_value = 0.009999990463256836
    # Gem Material
    gem_in_holder_2.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_2.inputs[2].default_value = False
    # Scale
    gem_in_holder_2.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_2.inputs[4].default_value = 20
    # Seed
    gem_in_holder_2.inputs[5].default_value = 10
    # Wings
    gem_in_holder_2.inputs[6].default_value = False
    # Array Count
    gem_in_holder_2.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_2.inputs[8].default_value = 10
    # Split
    gem_in_holder_2.inputs[9].default_value = 0.0010000000474974513
    # Seed
    gem_in_holder_2.inputs[10].default_value = 6.6099958419799805
    # Links for gem_in_holder_2

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.label = ""
    instance_on_points_001.location = (669.0, -75.7999267578125)
    instance_on_points_001.bl_label = "Instance on Points"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Links for instance_on_points_001
    links.new(distribute_points_on_faces_001.outputs[0], instance_on_points_001.inputs[0])
    links.new(distribute_points_on_faces_001.outputs[2], instance_on_points_001.inputs[5])

    random_value_010 = nodes.new("FunctionNodeRandomValue")
    random_value_010.name = "Random Value.010"
    random_value_010.label = ""
    random_value_010.location = (669.0, -315.7999267578125)
    random_value_010.bl_label = "Random Value"
    random_value_010.data_type = "FLOAT"
    # Min
    random_value_010.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_010.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_010.inputs[2].default_value = 0.10000000894069672
    # Max
    random_value_010.inputs[3].default_value = 0.4000000059604645
    # Min
    random_value_010.inputs[4].default_value = 0
    # Max
    random_value_010.inputs[5].default_value = 100
    # Probability
    random_value_010.inputs[6].default_value = 0.5
    # ID
    random_value_010.inputs[7].default_value = 0
    # Seed
    random_value_010.inputs[8].default_value = 0
    # Links for random_value_010
    links.new(random_value_010.outputs[1], instance_on_points_001.inputs[6])

    frame_016 = nodes.new("NodeFrame")
    frame_016.name = "Frame.016"
    frame_016.label = "Larger Jewels"
    frame_016.location = (4649.0, -3755.80029296875)
    frame_016.bl_label = "Frame"
    frame_016.text = None
    frame_016.shrink = True
    frame_016.label_size = 20
    # Links for frame_016

    realize_instances_002 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.name = "Realize Instances.002"
    realize_instances_002.label = ""
    realize_instances_002.location = (1009.0, -75.7999267578125)
    realize_instances_002.bl_label = "Realize Instances"
    # Selection
    realize_instances_002.inputs[1].default_value = True
    # Realize All
    realize_instances_002.inputs[2].default_value = True
    # Depth
    realize_instances_002.inputs[3].default_value = 0
    # Links for realize_instances_002

    transform_geometry_010 = nodes.new("GeometryNodeTransform")
    transform_geometry_010.name = "Transform Geometry.010"
    transform_geometry_010.label = ""
    transform_geometry_010.location = (269.0, -415.7999267578125)
    transform_geometry_010.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_010.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_010.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    # Rotation
    transform_geometry_010.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_010.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_010
    links.new(transform_geometry_010.outputs[0], instance_on_points_001.inputs[2])
    links.new(gem_in_holder_2.outputs[0], transform_geometry_010.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.name = "Group.005"
    swap_attr.label = ""
    swap_attr.location = (1169.0, -75.7999267578125)
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.bl_label = "Group"
    # Old
    swap_attr.inputs[2].default_value = "ruby"
    # New
    swap_attr.inputs[3].default_value = "saphire"
    # Links for swap_attr
    links.new(realize_instances_002.outputs[0], swap_attr.inputs[0])
    links.new(swap_attr.outputs[0], join_geometry_002.inputs[0])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (849.0, -75.7999267578125)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "INSTANCE"
    # Links for capture_attribute_001
    links.new(capture_attribute_001.outputs[0], realize_instances_002.inputs[0])
    links.new(instance_on_points_001.outputs[0], capture_attribute_001.inputs[0])
    links.new(capture_attribute_001.outputs[1], swap_attr.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (849.0, -195.7999267578125)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], capture_attribute_001.inputs[1])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1889.0, -75.13330078125)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001
    links.new(transform_geometry_009.outputs[0], set_position_001.inputs[0])

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.label = ""
    geometry_proximity_001.location = (1709.0, -275.13330078125)
    geometry_proximity_001.bl_label = "Geometry Proximity"
    geometry_proximity_001.target_element = "FACES"
    # Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0
    # Links for geometry_proximity_001
    links.new(bi-_rail_loft.outputs[0], geometry_proximity_001.inputs[0])
    links.new(geometry_proximity_001.outputs[0], set_position_001.inputs[2])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (2149.0, -95.13330078125)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh
    links.new(set_position_001.outputs[0], curve_to_mesh.inputs[0])
    links.new(gem_in_holder_1.outputs[1], curve_to_mesh.inputs[1])
    links.new(gem_in_holder_1.outputs[2], curve_to_mesh.inputs[2])
    links.new(curve_to_mesh.outputs[0], store_named_attribute_001.inputs[0])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.name = "Separate Geometry.002"
    separate_geometry_002.label = ""
    separate_geometry_002.location = (29.0, -29.0)
    separate_geometry_002.bl_label = "Separate Geometry"
    separate_geometry_002.domain = "CURVE"
    # Links for separate_geometry_002
    links.new(bi-_rail_loft.outputs[1], separate_geometry_002.inputs[0])

    compare_007 = nodes.new("FunctionNodeCompare")
    compare_007.name = "Compare.007"
    compare_007.label = ""
    compare_007.location = (29.0, -169.0)
    compare_007.bl_label = "Compare"
    compare_007.operation = "EQUAL"
    compare_007.data_type = "FLOAT"
    compare_007.mode = "ELEMENT"
    # B
    compare_007.inputs[1].default_value = 0.5
    # A
    compare_007.inputs[2].default_value = 0
    # B
    compare_007.inputs[3].default_value = 0
    # A
    compare_007.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_007.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_007.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_007.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_007.inputs[8].default_value = ""
    # B
    compare_007.inputs[9].default_value = ""
    # C
    compare_007.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_007.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_007.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_007
    links.new(compare_007.outputs[0], separate_geometry_002.inputs[1])

    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_004.name = "Separate XYZ.004"
    separate_x_y_z_004.label = ""
    separate_x_y_z_004.location = (29.0, -329.0)
    separate_x_y_z_004.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_004
    links.new(bi-_rail_loft.outputs[2], separate_x_y_z_004.inputs[0])
    links.new(separate_x_y_z_004.outputs[1], compare_007.inputs[0])

    trim_curve_002 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_002.name = "Trim Curve.002"
    trim_curve_002.label = ""
    trim_curve_002.location = (189.0, -29.0)
    trim_curve_002.bl_label = "Trim Curve"
    trim_curve_002.mode = "FACTOR"
    # Selection
    trim_curve_002.inputs[1].default_value = True
    # Start
    trim_curve_002.inputs[2].default_value = 0.0
    # End
    trim_curve_002.inputs[3].default_value = 0.8690060973167419
    # Start
    trim_curve_002.inputs[4].default_value = 0.0
    # End
    trim_curve_002.inputs[5].default_value = 1.0
    # Links for trim_curve_002
    links.new(separate_geometry_002.outputs[0], trim_curve_002.inputs[0])

    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.name = "Resample Curve.002"
    resample_curve_002.label = ""
    resample_curve_002.location = (349.0, -29.0)
    resample_curve_002.bl_label = "Resample Curve"
    resample_curve_002.keep_last_segment = True
    # Selection
    resample_curve_002.inputs[1].default_value = True
    # Mode
    resample_curve_002.inputs[2].default_value = "Count"
    # Count
    resample_curve_002.inputs[3].default_value = 47
    # Length
    resample_curve_002.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_002
    links.new(trim_curve_002.outputs[0], resample_curve_002.inputs[0])

    gold_decorations_1 = nodes.new("GeometryNodeGroup")
    gold_decorations_1.name = "Group.008"
    gold_decorations_1.label = ""
    gold_decorations_1.location = (869.0, -29.0)
    gold_decorations_1.node_tree = create_gold__decorations_group()
    gold_decorations_1.bl_label = "Group"
    # Seed
    gold_decorations_1.inputs[1].default_value = 75
    # Scale
    gold_decorations_1.inputs[2].default_value = 3.0999999046325684
    # Count
    gold_decorations_1.inputs[3].default_value = 6
    # Links for gold_decorations_1
    links.new(gold_decorations_1.outputs[0], join_geometry_002.inputs[0])

    set_curve_normal_003 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_003.name = "Set Curve Normal.003"
    set_curve_normal_003.label = ""
    set_curve_normal_003.location = (509.0, -29.0)
    set_curve_normal_003.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_003.inputs[1].default_value = True
    # Mode
    set_curve_normal_003.inputs[2].default_value = "Z Up"
    # Normal
    set_curve_normal_003.inputs[3].default_value = Vector((0.0, 0.0, 1.0))
    # Links for set_curve_normal_003
    links.new(resample_curve_002.outputs[0], set_curve_normal_003.inputs[0])

    frame_013 = nodes.new("NodeFrame")
    frame_013.name = "Frame.013"
    frame_013.label = ""
    frame_013.location = (1149.0, -1242.60009765625)
    frame_013.bl_label = "Frame"
    frame_013.text = None
    frame_013.shrink = True
    frame_013.label_size = 20
    # Links for frame_013

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (689.0, -49.0)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((0.0, -0.0010000000474974513, 0.0))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry
    links.new(transform_geometry.outputs[0], gold_decorations_1.inputs[0])
    links.new(set_curve_normal_003.outputs[0], transform_geometry.inputs[0])

    random_value_011 = nodes.new("FunctionNodeRandomValue")
    random_value_011.name = "Random Value.011"
    random_value_011.label = ""
    random_value_011.location = (509.0, -335.7999267578125)
    random_value_011.bl_label = "Random Value"
    random_value_011.data_type = "FLOAT"
    # Min
    random_value_011.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_011.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_011.inputs[2].default_value = 0.20000000298023224
    # Max
    random_value_011.inputs[3].default_value = 0.6000000238418579
    # Min
    random_value_011.inputs[4].default_value = 0
    # Max
    random_value_011.inputs[5].default_value = 100
    # Probability
    random_value_011.inputs[6].default_value = 0.5
    # ID
    random_value_011.inputs[7].default_value = 0
    # Seed
    random_value_011.inputs[8].default_value = 0
    # Links for random_value_011
    links.new(random_value_011.outputs[1], instance_on_points.inputs[6])

    trim_curve_003 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_003.name = "Trim Curve.003"
    trim_curve_003.label = ""
    trim_curve_003.location = (189.0, -29.0)
    trim_curve_003.bl_label = "Trim Curve"
    trim_curve_003.mode = "FACTOR"
    # Selection
    trim_curve_003.inputs[1].default_value = True
    # Start
    trim_curve_003.inputs[2].default_value = 0.10000000149011612
    # End
    trim_curve_003.inputs[3].default_value = 0.5
    # Start
    trim_curve_003.inputs[4].default_value = 0.0
    # End
    trim_curve_003.inputs[5].default_value = 1.0
    # Links for trim_curve_003

    resample_curve_003 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.name = "Resample Curve.003"
    resample_curve_003.label = ""
    resample_curve_003.location = (349.0, -29.0)
    resample_curve_003.bl_label = "Resample Curve"
    resample_curve_003.keep_last_segment = True
    # Selection
    resample_curve_003.inputs[1].default_value = True
    # Mode
    resample_curve_003.inputs[2].default_value = "Count"
    # Count
    resample_curve_003.inputs[3].default_value = 47
    # Length
    resample_curve_003.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_003
    links.new(trim_curve_003.outputs[0], resample_curve_003.inputs[0])

    gold_decorations_2 = nodes.new("GeometryNodeGroup")
    gold_decorations_2.name = "Group.009"
    gold_decorations_2.label = ""
    gold_decorations_2.location = (1029.0, -29.0)
    gold_decorations_2.node_tree = create_gold__decorations_group()
    gold_decorations_2.bl_label = "Group"
    # Seed
    gold_decorations_2.inputs[1].default_value = 78
    # Scale
    gold_decorations_2.inputs[2].default_value = 3.1999998092651367
    # Count
    gold_decorations_2.inputs[3].default_value = 13
    # Links for gold_decorations_2

    set_curve_normal_004 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_004.name = "Set Curve Normal.004"
    set_curve_normal_004.label = ""
    set_curve_normal_004.location = (509.0, -29.0)
    set_curve_normal_004.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_004.inputs[1].default_value = True
    # Mode
    set_curve_normal_004.inputs[2].default_value = "Free"
    # Links for set_curve_normal_004
    links.new(resample_curve_003.outputs[0], set_curve_normal_004.inputs[0])
    links.new(vector_math.outputs[0], set_curve_normal_004.inputs[3])

    frame_017 = nodes.new("NodeFrame")
    frame_017.name = "Frame.017"
    frame_017.label = ""
    frame_017.location = (1149.0, -622.60009765625)
    frame_017.bl_label = "Frame"
    frame_017.text = None
    frame_017.shrink = True
    frame_017.label_size = 20
    # Links for frame_017

    transform_geometry_011 = nodes.new("GeometryNodeTransform")
    transform_geometry_011.name = "Transform Geometry.011"
    transform_geometry_011.label = ""
    transform_geometry_011.location = (869.0, -29.0)
    transform_geometry_011.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_011.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_011.inputs[2].default_value = Vector((0.0, 0.0, -0.003000000026077032))
    # Rotation
    transform_geometry_011.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_011.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_011
    links.new(transform_geometry_011.outputs[0], gold_decorations_2.inputs[0])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (29.0, -29.0)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Selection
    mesh_to_curve.inputs[1].default_value = True
    # Links for mesh_to_curve
    links.new(separate_geometry.outputs[0], mesh_to_curve.inputs[0])
    links.new(mesh_to_curve.outputs[0], trim_curve_003.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    set_curve_tilt.label = ""
    set_curve_tilt.location = (689.0, -29.0)
    set_curve_tilt.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Tilt
    set_curve_tilt.inputs[2].default_value = -0.34819304943084717
    # Links for set_curve_tilt
    links.new(set_curve_tilt.outputs[0], transform_geometry_011.inputs[0])
    links.new(set_curve_normal_004.outputs[0], set_curve_tilt.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (4178.0, -3711.60009765625)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], join_geometry_002.inputs[0])
    links.new(gold_on_band.outputs[0], reroute_002.inputs[0])

    curve_circle_002 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_002.name = "Curve Circle.002"
    curve_circle_002.label = ""
    curve_circle_002.location = (1229.0, -35.7998046875)
    curve_circle_002.bl_label = "Curve Circle"
    curve_circle_002.mode = "RADIUS"
    # Resolution
    curve_circle_002.inputs[0].default_value = 64
    # Point 1
    curve_circle_002.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_002.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_002.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_002.inputs[4].default_value = 0.12999999523162842
    # Links for curve_circle_002

    transform_geometry_012 = nodes.new("GeometryNodeTransform")
    transform_geometry_012.name = "Transform Geometry.012"
    transform_geometry_012.label = ""
    transform_geometry_012.location = (1949.0, -395.7998046875)
    transform_geometry_012.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_012.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_012.inputs[2].default_value = Vector((0.009999999776482582, -0.03999999910593033, 0.46000000834465027))
    # Rotation
    transform_geometry_012.inputs[3].default_value = Euler((-0.027925267815589905, 0.0, 0.15533429384231567), 'XYZ')
    # Scale
    transform_geometry_012.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_012

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (1789.0, -395.7998046875)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Links for set_position_002
    links.new(curve_circle_002.outputs[0], set_position_002.inputs[0])
    links.new(set_position_002.outputs[0], transform_geometry_012.inputs[0])

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (629.0, -635.7998046875)
    position_003.bl_label = "Position"
    # Links for position_003

    separate_x_y_z_005 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_005.name = "Separate XYZ.005"
    separate_x_y_z_005.label = ""
    separate_x_y_z_005.location = (629.0, -695.7998046875)
    separate_x_y_z_005.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_005
    links.new(position_003.outputs[0], separate_x_y_z_005.inputs[0])

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.label = ""
    map_range_001.location = (789.0, -635.7998046875)
    map_range_001.bl_label = "Map Range"
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT"
    # From Min
    map_range_001.inputs[1].default_value = 0.12999999523162842
    # From Max
    map_range_001.inputs[2].default_value = -0.12999999523162842
    # To Min
    map_range_001.inputs[3].default_value = 0.0
    # To Max
    map_range_001.inputs[4].default_value = 1.0
    # Steps
    map_range_001.inputs[5].default_value = 4.0
    # Vector
    map_range_001.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_001.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_001.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_001.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_001.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_001
    links.new(separate_x_y_z_005.outputs[1], map_range_001.inputs[0])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (969.0, -635.7998046875)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(map_range_001.outputs[0], float_curve.inputs[1])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (1429.0, -675.7998046875)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = -0.29999998211860657
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (1589.0, -675.7998046875)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # X
    combine_x_y_z_001.inputs[0].default_value = 0.0
    # Links for combine_x_y_z_001
    links.new(combine_x_y_z_001.outputs[0], set_position_002.inputs[3])
    links.new(math_002.outputs[0], combine_x_y_z_001.inputs[2])

    position_005 = nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"
    position_005.label = ""
    position_005.location = (1069.0, -155.7998046875)
    position_005.bl_label = "Position"
    # Links for position_005

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (1229.0, -155.7998046875)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "MULTIPLY"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(position_005.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], set_position_002.inputs[2])

    combine_x_y_z_002 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_002.name = "Combine XYZ.002"
    combine_x_y_z_002.label = ""
    combine_x_y_z_002.location = (1229.0, -295.7998046875)
    combine_x_y_z_002.bl_label = "Combine XYZ"
    # Y
    combine_x_y_z_002.inputs[1].default_value = 1.0
    # Z
    combine_x_y_z_002.inputs[2].default_value = 1.0
    # Links for combine_x_y_z_002
    links.new(combine_x_y_z_002.outputs[0], vector_math_001.inputs[1])

    float_curve_002 = nodes.new("ShaderNodeFloatCurve")
    float_curve_002.name = "Float Curve.002"
    float_curve_002.label = ""
    float_curve_002.location = (969.0, -295.7998046875)
    float_curve_002.bl_label = "Float Curve"
    # Factor
    float_curve_002.inputs[0].default_value = 1.0
    # Links for float_curve_002
    links.new(map_range_001.outputs[0], float_curve_002.inputs[1])
    links.new(float_curve_002.outputs[0], combine_x_y_z_002.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (5618.0, -2771.5986328125)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "skip"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(store_named_attribute.outputs[0], join_geometry_002.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (2129.0, -395.7998046875)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Length"
    # Count
    resample_curve.inputs[3].default_value = 10
    # Length
    resample_curve.inputs[4].default_value = 0.014999999664723873
    # Links for resample_curve
    links.new(transform_geometry_012.outputs[0], resample_curve.inputs[0])

    instance_on_points_002 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.name = "Instance on Points.002"
    instance_on_points_002.label = ""
    instance_on_points_002.location = (3469.0, -535.7998046875)
    instance_on_points_002.bl_label = "Instance on Points"
    # Selection
    instance_on_points_002.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_002.inputs[3].default_value = False
    # Instance Index
    instance_on_points_002.inputs[4].default_value = 0
    # Scale
    instance_on_points_002.inputs[6].default_value = Vector((0.699999988079071, 0.699999988079071, 0.699999988079071))
    # Links for instance_on_points_002

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.label = ""
    align_rotation_to_vector.location = (29.0, -35.7998046875)
    align_rotation_to_vector.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector

    curve_tangent_001 = nodes.new("GeometryNodeInputTangent")
    curve_tangent_001.name = "Curve Tangent.001"
    curve_tangent_001.label = ""
    curve_tangent_001.location = (29.0, -195.7998046875)
    curve_tangent_001.bl_label = "Curve Tangent"
    # Links for curve_tangent_001
    links.new(curve_tangent_001.outputs[0], align_rotation_to_vector.inputs[2])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.label = ""
    align_rotation_to_vector_001.location = (189.0, -35.7998046875)
    align_rotation_to_vector_001.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_001.axis = "Y"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_001
    links.new(align_rotation_to_vector.outputs[0], align_rotation_to_vector_001.inputs[0])

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.name = "Normal.001"
    normal_001.label = ""
    normal_001.location = (189.0, -195.7998046875)
    normal_001.bl_label = "Normal"
    normal_001.legacy_corner_normals = False
    # Links for normal_001
    links.new(normal_001.outputs[0], align_rotation_to_vector_001.inputs[2])

    rotate_rotation_003 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_003.name = "Rotate Rotation.003"
    rotate_rotation_003.label = ""
    rotate_rotation_003.location = (349.0, -35.7998046875)
    rotate_rotation_003.bl_label = "Rotate Rotation"
    rotate_rotation_003.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_003.inputs[1].default_value = Euler((0.23108159005641937, 0.14137165248394012, 0.0), 'XYZ')
    # Links for rotate_rotation_003
    links.new(align_rotation_to_vector_001.outputs[0], rotate_rotation_003.inputs[0])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.label = ""
    spline_parameter.location = (1669.0, -55.7998046875)
    spline_parameter.bl_label = "Spline Parameter"
    # Links for spline_parameter

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (1849.0, -55.7998046875)
    math_003.bl_label = "Math"
    math_003.operation = "SUBTRACT"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 0.7400000095367432
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(spline_parameter.outputs[0], math_003.inputs[0])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (2029.0, -55.7998046875)
    math_004.bl_label = "Math"
    math_004.operation = "ABSOLUTE"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 0.7400000095367432
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(math_003.outputs[0], math_004.inputs[0])

    set_curve_tilt_002 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_002.name = "Set Curve Tilt.002"
    set_curve_tilt_002.label = ""
    set_curve_tilt_002.location = (2589.0, -395.7998046875)
    set_curve_tilt_002.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_002.inputs[1].default_value = True
    # Links for set_curve_tilt_002
    links.new(set_curve_tilt_002.outputs[0], instance_on_points_002.inputs[0])
    links.new(resample_curve.outputs[0], set_curve_tilt_002.inputs[0])

    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.name = "Map Range.002"
    map_range_002.label = ""
    map_range_002.location = (2229.0, -75.7998046875)
    map_range_002.bl_label = "Map Range"
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    # From Min
    map_range_002.inputs[1].default_value = 0.0
    # From Max
    map_range_002.inputs[2].default_value = 0.08000002801418304
    # To Min
    map_range_002.inputs[3].default_value = 0.6799999475479126
    # To Max
    map_range_002.inputs[4].default_value = 0.47999998927116394
    # Steps
    map_range_002.inputs[5].default_value = 4.0
    # Vector
    map_range_002.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_002.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_002.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_002.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_002.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_002.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_002
    links.new(math_004.outputs[0], map_range_002.inputs[0])
    links.new(map_range_002.outputs[0], set_curve_tilt_002.inputs[2])

    float_curve_003 = nodes.new("ShaderNodeFloatCurve")
    float_curve_003.name = "Float Curve.003"
    float_curve_003.label = ""
    float_curve_003.location = (269.0, -1115.7998046875)
    float_curve_003.bl_label = "Float Curve"
    # Factor
    float_curve_003.inputs[0].default_value = 1.0
    # Links for float_curve_003

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.label = ""
    spline_parameter_001.location = (29.0, -1355.7998046875)
    spline_parameter_001.bl_label = "Spline Parameter"
    # Links for spline_parameter_001
    links.new(spline_parameter_001.outputs[0], float_curve_003.inputs[1])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (609.0, -1095.7998046875)
    math_005.bl_label = "Math"
    math_005.operation = "MULTIPLY"
    math_005.use_clamp = False
    # Value
    math_005.inputs[1].default_value = 0.014999999664723873
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(float_curve_003.outputs[0], math_005.inputs[0])

    curve_circle_003 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.name = "Curve Circle.003"
    curve_circle_003.label = ""
    curve_circle_003.location = (29.0, -99.6669921875)
    curve_circle_003.bl_label = "Curve Circle"
    curve_circle_003.mode = "RADIUS"
    # Resolution
    curve_circle_003.inputs[0].default_value = 20
    # Point 1
    curve_circle_003.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_003.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_003.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_003.inputs[4].default_value = 0.014999999664723873
    # Links for curve_circle_003

    instance_on_points_003 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.name = "Instance on Points.003"
    instance_on_points_003.label = ""
    instance_on_points_003.location = (189.0, -99.6669921875)
    instance_on_points_003.bl_label = "Instance on Points"
    # Selection
    instance_on_points_003.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_003.inputs[3].default_value = False
    # Instance Index
    instance_on_points_003.inputs[4].default_value = 0
    # Rotation
    instance_on_points_003.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_003.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_003
    links.new(curve_circle_003.outputs[0], instance_on_points_003.inputs[0])

    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.name = "Ico Sphere.001"
    ico_sphere_001.label = ""
    ico_sphere_001.location = (29.0, -239.6669921875)
    ico_sphere_001.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_001.inputs[0].default_value = 0.0020000000949949026
    # Subdivisions
    ico_sphere_001.inputs[1].default_value = 1
    # Links for ico_sphere_001
    links.new(ico_sphere_001.outputs[0], instance_on_points_003.inputs[2])

    cylinder_001 = nodes.new("GeometryNodeMeshCylinder")
    cylinder_001.name = "Cylinder.001"
    cylinder_001.label = ""
    cylinder_001.location = (189.0, -39.6669921875)
    cylinder_001.bl_label = "Cylinder"
    cylinder_001.fill_type = "NGON"
    # Vertices
    cylinder_001.inputs[0].default_value = 10
    # Side Segments
    cylinder_001.inputs[1].default_value = 1
    # Fill Segments
    cylinder_001.inputs[2].default_value = 1
    # Radius
    cylinder_001.inputs[3].default_value = 0.014999999664723873
    # Depth
    cylinder_001.inputs[4].default_value = 0.0020000000949949026
    # Links for cylinder_001

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (1169.0, -39.6669921875)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003
    links.new(instance_on_points_003.outputs[0], join_geometry_003.inputs[0])
    links.new(cylinder_001.outputs[0], join_geometry_003.inputs[0])

    ico_sphere_002 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_002.name = "Ico Sphere.002"
    ico_sphere_002.label = ""
    ico_sphere_002.location = (349.0, -99.6669921875)
    ico_sphere_002.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_002.inputs[0].default_value = 0.012000000104308128
    # Subdivisions
    ico_sphere_002.inputs[1].default_value = 2
    # Links for ico_sphere_002

    transform_geometry_013 = nodes.new("GeometryNodeTransform")
    transform_geometry_013.name = "Transform Geometry.013"
    transform_geometry_013.label = ""
    transform_geometry_013.location = (749.0, -119.6669921875)
    transform_geometry_013.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_013.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_013.inputs[2].default_value = Vector((-0.006000000052154064, 0.0, 0.0010000000474974513))
    # Rotation
    transform_geometry_013.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_013.inputs[4].default_value = Vector((0.4699999988079071, 0.8600000143051147, 0.05000000074505806))
    # Links for transform_geometry_013
    links.new(transform_geometry_013.outputs[0], join_geometry_003.inputs[0])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    set_position_003.label = ""
    set_position_003.location = (569.0, -139.6669921875)
    set_position_003.bl_label = "Set Position"
    # Selection
    set_position_003.inputs[1].default_value = True
    # Position
    set_position_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_003
    links.new(set_position_003.outputs[0], transform_geometry_013.inputs[0])
    links.new(ico_sphere_002.outputs[0], set_position_003.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (569.0, -279.6669921875)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 0.004999999888241291
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], set_position_003.inputs[3])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (369.0, -279.6669921875)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = False
    # Vector
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # W
    noise_texture.inputs[1].default_value = 60.499996185302734
    # Scale
    noise_texture.inputs[2].default_value = 29.089996337890625
    # Detail
    noise_texture.inputs[3].default_value = 2.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Offset
    noise_texture.inputs[6].default_value = 0.0
    # Gain
    noise_texture.inputs[7].default_value = 1.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0
    # Links for noise_texture
    links.new(noise_texture.outputs[0], vector_math_002.inputs[0])

    transform_geometry_014 = nodes.new("GeometryNodeTransform")
    transform_geometry_014.name = "Transform Geometry.014"
    transform_geometry_014.label = ""
    transform_geometry_014.location = (909.0, -179.6669921875)
    transform_geometry_014.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_014.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_014.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_014.inputs[3].default_value = Euler((0.0, 0.0, 3.1415927410125732), 'XYZ')
    # Scale
    transform_geometry_014.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_014
    links.new(transform_geometry_013.outputs[0], transform_geometry_014.inputs[0])
    links.new(transform_geometry_014.outputs[0], join_geometry_003.inputs[0])

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Necklace Link"
    frame_002.location = (1700.0, -1016.1328125)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    rotate_rotation_004 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_004.name = "Rotate Rotation.004"
    rotate_rotation_004.label = ""
    rotate_rotation_004.location = (509.0, -35.7998046875)
    rotate_rotation_004.bl_label = "Rotate Rotation"
    rotate_rotation_004.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_004.inputs[1].default_value = Euler((3.1415927410125732, 0.0, 1.5707963705062866), 'XYZ')
    # Links for rotate_rotation_004
    links.new(rotate_rotation_003.outputs[0], rotate_rotation_004.inputs[0])
    links.new(rotate_rotation_004.outputs[0], instance_on_points_002.inputs[5])

    ico_sphere_003 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_003.name = "Ico Sphere.003"
    ico_sphere_003.label = ""
    ico_sphere_003.location = (29.0, -399.6669921875)
    ico_sphere_003.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_003.inputs[0].default_value = 0.004999999888241291
    # Subdivisions
    ico_sphere_003.inputs[1].default_value = 1
    # Links for ico_sphere_003
    links.new(ico_sphere_003.outputs[0], join_geometry_003.inputs[0])

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Align"
    frame_003.location = (2220.0, -680.0)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (1369.0, -39.6669921875)
    store_named_attribute_004.bl_label = "Store Named Attribute"
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_004.inputs[3].default_value = True
    # Links for store_named_attribute_004
    links.new(store_named_attribute_004.outputs[0], instance_on_points_002.inputs[2])
    links.new(join_geometry_003.outputs[0], store_named_attribute_004.inputs[0])

    cylinder_002 = nodes.new("GeometryNodeMeshCylinder")
    cylinder_002.name = "Cylinder.002"
    cylinder_002.label = ""
    cylinder_002.location = (29.0, -115.7998046875)
    cylinder_002.bl_label = "Cylinder"
    cylinder_002.fill_type = "NGON"
    # Vertices
    cylinder_002.inputs[0].default_value = 16
    # Side Segments
    cylinder_002.inputs[1].default_value = 1
    # Fill Segments
    cylinder_002.inputs[2].default_value = 1
    # Radius
    cylinder_002.inputs[3].default_value = 0.019999999552965164
    # Depth
    cylinder_002.inputs[4].default_value = 0.0020000000949949026
    # Links for cylinder_002

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (1249.0, -655.7998046875)
    math_006.bl_label = "Math"
    math_006.operation = "ADD"
    math_006.use_clamp = False
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(math_006.outputs[0], math_002.inputs[0])
    links.new(float_curve.outputs[0], math_006.inputs[0])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"
    spline_parameter_002.label = ""
    spline_parameter_002.location = (29.0, -935.7998046875)
    spline_parameter_002.bl_label = "Spline Parameter"
    # Links for spline_parameter_002

    float_curve_004 = nodes.new("ShaderNodeFloatCurve")
    float_curve_004.name = "Float Curve.004"
    float_curve_004.label = ""
    float_curve_004.location = (269.0, -795.7998046875)
    float_curve_004.bl_label = "Float Curve"
    # Factor
    float_curve_004.inputs[0].default_value = 1.0
    # Links for float_curve_004
    links.new(spline_parameter_002.outputs[0], float_curve_004.inputs[1])
    links.new(float_curve_004.outputs[0], math_006.inputs[1])

    set_position_004 = nodes.new("GeometryNodeSetPosition")
    set_position_004.name = "Set Position.004"
    set_position_004.label = ""
    set_position_004.location = (869.0, -155.7998046875)
    set_position_004.bl_label = "Set Position"
    # Selection
    set_position_004.inputs[1].default_value = True
    # Position
    set_position_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_004
    links.new(cylinder_002.outputs[0], set_position_004.inputs[0])

    position_006 = nodes.new("GeometryNodeInputPosition")
    position_006.name = "Position.006"
    position_006.label = ""
    position_006.location = (229.0, -215.7998046875)
    position_006.bl_label = "Position"
    # Links for position_006

    separate_x_y_z_006 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_006.name = "Separate XYZ.006"
    separate_x_y_z_006.label = ""
    separate_x_y_z_006.location = (229.0, -275.7998046875)
    separate_x_y_z_006.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_006
    links.new(position_006.outputs[0], separate_x_y_z_006.inputs[0])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.label = ""
    math_007.location = (389.0, -215.7998046875)
    math_007.bl_label = "Math"
    math_007.operation = "ABSOLUTE"
    math_007.use_clamp = False
    # Value
    math_007.inputs[1].default_value = 0.5
    # Value
    math_007.inputs[2].default_value = 0.5
    # Links for math_007
    links.new(separate_x_y_z_006.outputs[0], math_007.inputs[0])

    combine_x_y_z_003 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_003.name = "Combine XYZ.003"
    combine_x_y_z_003.label = ""
    combine_x_y_z_003.location = (709.0, -215.7998046875)
    combine_x_y_z_003.bl_label = "Combine XYZ"
    # X
    combine_x_y_z_003.inputs[0].default_value = 0.0
    # Z
    combine_x_y_z_003.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_003
    links.new(combine_x_y_z_003.outputs[0], set_position_004.inputs[3])

    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.name = "Map Range.003"
    map_range_003.label = ""
    map_range_003.location = (389.0, -355.7998046875)
    map_range_003.bl_label = "Map Range"
    map_range_003.clamp = True
    map_range_003.interpolation_type = "LINEAR"
    map_range_003.data_type = "FLOAT"
    # From Min
    map_range_003.inputs[1].default_value = -0.019999999552965164
    # From Max
    map_range_003.inputs[2].default_value = 0.019999999552965164
    # To Min
    map_range_003.inputs[3].default_value = 0.7999999523162842
    # To Max
    map_range_003.inputs[4].default_value = 0.19999998807907104
    # Steps
    map_range_003.inputs[5].default_value = 4.0
    # Vector
    map_range_003.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_003.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_003.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_003.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_003.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_003.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_003
    links.new(separate_x_y_z_006.outputs[1], map_range_003.inputs[0])

    math_008 = nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.label = ""
    math_008.location = (549.0, -215.7998046875)
    math_008.bl_label = "Math"
    math_008.operation = "MULTIPLY"
    math_008.use_clamp = False
    # Value
    math_008.inputs[2].default_value = 0.5
    # Links for math_008
    links.new(math_008.outputs[0], combine_x_y_z_003.inputs[1])
    links.new(math_007.outputs[0], math_008.inputs[0])
    links.new(map_range_003.outputs[0], math_008.inputs[1])

    boolean_math_004 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.name = "Boolean Math.004"
    boolean_math_004.label = ""
    boolean_math_004.location = (969.0, -495.7998046875)
    boolean_math_004.bl_label = "Boolean Math"
    boolean_math_004.operation = "AND"
    # Links for boolean_math_004
    links.new(cylinder_002.outputs[1], boolean_math_004.inputs[0])
    links.new(cylinder_002.outputs[2], boolean_math_004.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (1189.0, -375.7998046875)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Links for mesh_to_curve_001
    links.new(set_position_004.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(boolean_math_004.outputs[0], mesh_to_curve_001.inputs[1])

    ico_sphere_004 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_004.name = "Ico Sphere.004"
    ico_sphere_004.label = ""
    ico_sphere_004.location = (1189.0, -515.7998046875)
    ico_sphere_004.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_004.inputs[0].default_value = 0.0020000000949949026
    # Subdivisions
    ico_sphere_004.inputs[1].default_value = 1
    # Links for ico_sphere_004

    instance_on_points_004 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_004.name = "Instance on Points.004"
    instance_on_points_004.label = ""
    instance_on_points_004.location = (1369.0, -375.7998046875)
    instance_on_points_004.bl_label = "Instance on Points"
    # Selection
    instance_on_points_004.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_004.inputs[3].default_value = False
    # Instance Index
    instance_on_points_004.inputs[4].default_value = 0
    # Rotation
    instance_on_points_004.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_004.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_004
    links.new(mesh_to_curve_001.outputs[0], instance_on_points_004.inputs[0])
    links.new(ico_sphere_004.outputs[0], instance_on_points_004.inputs[2])

    transform_geometry_015 = nodes.new("GeometryNodeTransform")
    transform_geometry_015.name = "Transform Geometry.015"
    transform_geometry_015.label = ""
    transform_geometry_015.location = (1909.0, -495.7998046875)
    transform_geometry_015.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_015.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_015.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    # Rotation
    transform_geometry_015.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_015.inputs[4].default_value = Vector((2.0, 1.0, 0.30000001192092896))
    # Links for transform_geometry_015

    ico_sphere_005 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_005.name = "Ico Sphere.005"
    ico_sphere_005.label = ""
    ico_sphere_005.location = (1569.0, -495.7998046875)
    ico_sphere_005.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_005.inputs[0].default_value = 0.004999999888241291
    # Subdivisions
    ico_sphere_005.inputs[1].default_value = 2
    # Links for ico_sphere_005

    dual_mesh = nodes.new("GeometryNodeDualMesh")
    dual_mesh.name = "Dual Mesh"
    dual_mesh.label = ""
    dual_mesh.location = (1749.0, -495.7998046875)
    dual_mesh.bl_label = "Dual Mesh"
    # Keep Boundaries
    dual_mesh.inputs[1].default_value = False
    # Links for dual_mesh
    links.new(ico_sphere_005.outputs[0], dual_mesh.inputs[0])
    links.new(dual_mesh.outputs[0], transform_geometry_015.inputs[0])

    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_007.name = "Join Geometry.007"
    join_geometry_007.label = ""
    join_geometry_007.location = (2269.0, -315.7998046875)
    join_geometry_007.bl_label = "Join Geometry"
    # Links for join_geometry_007

    transform_geometry_016 = nodes.new("GeometryNodeTransform")
    transform_geometry_016.name = "Transform Geometry.016"
    transform_geometry_016.label = ""
    transform_geometry_016.location = (2109.0, -355.7998046875)
    transform_geometry_016.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_016.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_016.inputs[2].default_value = Vector((0.0, 0.003000000026077032, 0.0))
    # Rotation
    transform_geometry_016.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    # Scale
    transform_geometry_016.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_016
    links.new(transform_geometry_015.outputs[0], transform_geometry_016.inputs[0])
    links.new(transform_geometry_016.outputs[0], join_geometry_007.inputs[0])

    transform_geometry_017 = nodes.new("GeometryNodeTransform")
    transform_geometry_017.name = "Transform Geometry.017"
    transform_geometry_017.label = ""
    transform_geometry_017.location = (2109.0, -675.7998046875)
    transform_geometry_017.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_017.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_017.inputs[2].default_value = Vector((-0.009999999776482582, 0.009999999776482582, 0.0))
    # Rotation
    transform_geometry_017.inputs[3].default_value = Euler((0.0, 0.0, 1.0471975803375244), 'XYZ')
    # Scale
    transform_geometry_017.inputs[4].default_value = Vector((0.6000000238418579, 0.6000000238418579, 1.0))
    # Links for transform_geometry_017
    links.new(transform_geometry_015.outputs[0], transform_geometry_017.inputs[0])
    links.new(transform_geometry_017.outputs[0], join_geometry_007.inputs[0])

    transform_geometry_018 = nodes.new("GeometryNodeTransform")
    transform_geometry_018.name = "Transform Geometry.018"
    transform_geometry_018.label = ""
    transform_geometry_018.location = (2269.0, -675.7998046875)
    transform_geometry_018.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_018.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_018.inputs[2].default_value = Vector((0.009999999776482582, 0.009999999776482582, 0.0))
    # Rotation
    transform_geometry_018.inputs[3].default_value = Euler((0.0, 0.0, -1.0471975803375244), 'XYZ')
    # Scale
    transform_geometry_018.inputs[4].default_value = Vector((0.6000000238418579, 0.6000000238418579, 1.0))
    # Links for transform_geometry_018
    links.new(transform_geometry_015.outputs[0], transform_geometry_018.inputs[0])
    links.new(transform_geometry_018.outputs[0], join_geometry_007.inputs[0])

    transform_geometry_019 = nodes.new("GeometryNodeTransform")
    transform_geometry_019.name = "Transform Geometry.019"
    transform_geometry_019.label = ""
    transform_geometry_019.location = (2269.0, -355.7998046875)
    transform_geometry_019.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_019.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_019.inputs[2].default_value = Vector((0.0, -0.012000000104308128, 0.0))
    # Rotation
    transform_geometry_019.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    # Scale
    transform_geometry_019.inputs[4].default_value = Vector((0.30000001192092896, 0.6000000238418579, 1.0))
    # Links for transform_geometry_019
    links.new(transform_geometry_015.outputs[0], transform_geometry_019.inputs[0])
    links.new(transform_geometry_019.outputs[0], join_geometry_007.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_009.name = "Join Geometry.009"
    join_geometry_009.label = ""
    join_geometry_009.location = (1809.0, -95.7998046875)
    join_geometry_009.bl_label = "Join Geometry"
    # Links for join_geometry_009
    links.new(instance_on_points_004.outputs[0], join_geometry_009.inputs[0])
    links.new(set_position_004.outputs[0], join_geometry_009.inputs[0])

    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.name = "Store Named Attribute.005"
    store_named_attribute_005.label = ""
    store_named_attribute_005.location = (2889.0, -255.7998046875)
    store_named_attribute_005.bl_label = "Store Named Attribute"
    store_named_attribute_005.data_type = "BOOLEAN"
    store_named_attribute_005.domain = "POINT"
    # Selection
    store_named_attribute_005.inputs[1].default_value = True
    # Name
    store_named_attribute_005.inputs[2].default_value = "ruby"
    # Value
    store_named_attribute_005.inputs[3].default_value = True
    # Links for store_named_attribute_005

    join_geometry_010 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_010.name = "Join Geometry.010"
    join_geometry_010.label = ""
    join_geometry_010.location = (3109.0, -155.7998046875)
    join_geometry_010.bl_label = "Join Geometry"
    # Links for join_geometry_010
    links.new(store_named_attribute_005.outputs[0], join_geometry_010.inputs[0])

    store_named_attribute_006 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_006.name = "Store Named Attribute.006"
    store_named_attribute_006.label = ""
    store_named_attribute_006.location = (2889.0, -55.7998046875)
    store_named_attribute_006.bl_label = "Store Named Attribute"
    store_named_attribute_006.data_type = "BOOLEAN"
    store_named_attribute_006.domain = "POINT"
    # Selection
    store_named_attribute_006.inputs[1].default_value = True
    # Name
    store_named_attribute_006.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_006.inputs[3].default_value = True
    # Links for store_named_attribute_006
    links.new(store_named_attribute_006.outputs[0], join_geometry_010.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Pendant"
    frame_004.location = (640.0, -1760.0)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.label = ""
    sample_curve.location = (3509.0, -1515.7998046875)
    sample_curve.bl_label = "Sample Curve"
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = True
    sample_curve.data_type = "FLOAT"
    # Value
    sample_curve.inputs[1].default_value = 0.0
    # Factor
    sample_curve.inputs[2].default_value = 0.6780651807785034
    # Length
    sample_curve.inputs[3].default_value = 0.0
    # Curve Index
    sample_curve.inputs[4].default_value = 0
    # Links for sample_curve
    links.new(set_curve_tilt_002.outputs[0], sample_curve.inputs[0])

    transform_geometry_020 = nodes.new("GeometryNodeTransform")
    transform_geometry_020.name = "Transform Geometry.020"
    transform_geometry_020.label = ""
    transform_geometry_020.location = (3949.0, -1515.7998046875)
    transform_geometry_020.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_020.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_020.inputs[3].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_020.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_020
    links.new(join_geometry_010.outputs[0], transform_geometry_020.inputs[0])

    join_geometry_011 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_011.name = "Join Geometry.011"
    join_geometry_011.label = ""
    join_geometry_011.location = (4229.0, -1015.7998046875)
    join_geometry_011.bl_label = "Join Geometry"
    # Links for join_geometry_011
    links.new(transform_geometry_020.outputs[0], join_geometry_011.inputs[0])
    links.new(instance_on_points_002.outputs[0], join_geometry_011.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (3669.0, -1515.7998046875)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "ADD"
    # Vector
    vector_math_003.inputs[1].default_value = [0.0, -0.003000000026077032, -0.019999999552965164]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(vector_math_003.outputs[0], transform_geometry_020.inputs[2])
    links.new(sample_curve.outputs[1], vector_math_003.inputs[0])

    float_curve_005 = nodes.new("ShaderNodeFloatCurve")
    float_curve_005.name = "Float Curve.005"
    float_curve_005.label = ""
    float_curve_005.location = (229.0, -1455.7998046875)
    float_curve_005.bl_label = "Float Curve"
    # Factor
    float_curve_005.inputs[0].default_value = 1.0
    # Links for float_curve_005

    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_003.name = "Spline Parameter.003"
    spline_parameter_003.label = ""
    spline_parameter_003.location = (29.0, -1695.7998046875)
    spline_parameter_003.bl_label = "Spline Parameter"
    # Links for spline_parameter_003
    links.new(spline_parameter_003.outputs[0], float_curve_005.inputs[1])

    math_009 = nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.label = ""
    math_009.location = (609.0, -1435.7998046875)
    math_009.bl_label = "Math"
    math_009.operation = "MULTIPLY"
    math_009.use_clamp = False
    # Value
    math_009.inputs[1].default_value = -0.014999999664723873
    # Value
    math_009.inputs[2].default_value = 0.5
    # Links for math_009
    links.new(float_curve_005.outputs[0], math_009.inputs[0])

    math_010 = nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.label = ""
    math_010.location = (789.0, -1075.7998046875)
    math_010.bl_label = "Math"
    math_010.operation = "ADD"
    math_010.use_clamp = False
    # Value
    math_010.inputs[2].default_value = 0.5
    # Links for math_010
    links.new(math_010.outputs[0], combine_x_y_z_001.inputs[1])
    links.new(math_005.outputs[0], math_010.inputs[0])
    links.new(math_009.outputs[0], math_010.inputs[1])

    frame_018 = nodes.new("NodeFrame")
    frame_018.name = "Frame.018"
    frame_018.label = "Necklace 1"
    frame_018.location = (49.0, -35.798828125)
    frame_018.bl_label = "Frame"
    frame_018.text = None
    frame_018.shrink = True
    frame_018.label_size = 20
    # Links for frame_018

    curve_circle_004 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_004.name = "Curve Circle.004"
    curve_circle_004.label = ""
    curve_circle_004.location = (1229.0, -35.7998046875)
    curve_circle_004.bl_label = "Curve Circle"
    curve_circle_004.mode = "RADIUS"
    # Resolution
    curve_circle_004.inputs[0].default_value = 64
    # Point 1
    curve_circle_004.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_004.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_004.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_004.inputs[4].default_value = 0.12999999523162842
    # Links for curve_circle_004

    transform_geometry_021 = nodes.new("GeometryNodeTransform")
    transform_geometry_021.name = "Transform Geometry.021"
    transform_geometry_021.label = ""
    transform_geometry_021.location = (1949.0, -395.7998046875)
    transform_geometry_021.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_021.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_021.inputs[2].default_value = Vector((-0.009999999776482582, -0.03999999910593033, 0.46000000834465027))
    # Rotation
    transform_geometry_021.inputs[3].default_value = Euler((-0.027925267815589905, 0.0, -0.08691740036010742), 'XYZ')
    # Scale
    transform_geometry_021.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_021

    set_position_005 = nodes.new("GeometryNodeSetPosition")
    set_position_005.name = "Set Position.005"
    set_position_005.label = ""
    set_position_005.location = (1789.0, -395.7998046875)
    set_position_005.bl_label = "Set Position"
    # Selection
    set_position_005.inputs[1].default_value = True
    # Links for set_position_005
    links.new(curve_circle_004.outputs[0], set_position_005.inputs[0])
    links.new(set_position_005.outputs[0], transform_geometry_021.inputs[0])

    position_007 = nodes.new("GeometryNodeInputPosition")
    position_007.name = "Position.007"
    position_007.label = ""
    position_007.location = (629.0, -635.7998046875)
    position_007.bl_label = "Position"
    # Links for position_007

    separate_x_y_z_007 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_007.name = "Separate XYZ.007"
    separate_x_y_z_007.label = ""
    separate_x_y_z_007.location = (629.0, -695.7998046875)
    separate_x_y_z_007.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_007
    links.new(position_007.outputs[0], separate_x_y_z_007.inputs[0])

    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.name = "Map Range.004"
    map_range_004.label = ""
    map_range_004.location = (789.0, -635.7998046875)
    map_range_004.bl_label = "Map Range"
    map_range_004.clamp = True
    map_range_004.interpolation_type = "LINEAR"
    map_range_004.data_type = "FLOAT"
    # From Min
    map_range_004.inputs[1].default_value = 0.12999999523162842
    # From Max
    map_range_004.inputs[2].default_value = -0.12999999523162842
    # To Min
    map_range_004.inputs[3].default_value = 0.0
    # To Max
    map_range_004.inputs[4].default_value = 1.0
    # Steps
    map_range_004.inputs[5].default_value = 4.0
    # Vector
    map_range_004.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_004.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_004.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_004.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_004.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_004.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_004
    links.new(separate_x_y_z_007.outputs[1], map_range_004.inputs[0])

    float_curve_006 = nodes.new("ShaderNodeFloatCurve")
    float_curve_006.name = "Float Curve.006"
    float_curve_006.label = ""
    float_curve_006.location = (969.0, -635.7998046875)
    float_curve_006.bl_label = "Float Curve"
    # Factor
    float_curve_006.inputs[0].default_value = 1.0
    # Links for float_curve_006
    links.new(map_range_004.outputs[0], float_curve_006.inputs[1])

    math_011 = nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.label = ""
    math_011.location = (1409.0, -655.7998046875)
    math_011.bl_label = "Math"
    math_011.operation = "MULTIPLY"
    math_011.use_clamp = False
    # Value
    math_011.inputs[1].default_value = -0.19999998807907104
    # Value
    math_011.inputs[2].default_value = 0.5
    # Links for math_011

    combine_x_y_z_004 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_004.name = "Combine XYZ.004"
    combine_x_y_z_004.label = ""
    combine_x_y_z_004.location = (1589.0, -675.7998046875)
    combine_x_y_z_004.bl_label = "Combine XYZ"
    # X
    combine_x_y_z_004.inputs[0].default_value = 0.0
    # Links for combine_x_y_z_004
    links.new(combine_x_y_z_004.outputs[0], set_position_005.inputs[3])
    links.new(math_011.outputs[0], combine_x_y_z_004.inputs[2])

    position_008 = nodes.new("GeometryNodeInputPosition")
    position_008.name = "Position.008"
    position_008.label = ""
    position_008.location = (1069.0, -155.7998046875)
    position_008.bl_label = "Position"
    # Links for position_008

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (1229.0, -155.7998046875)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "MULTIPLY"
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(position_008.outputs[0], vector_math_004.inputs[0])
    links.new(vector_math_004.outputs[0], set_position_005.inputs[2])

    combine_x_y_z_005 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_005.name = "Combine XYZ.005"
    combine_x_y_z_005.label = ""
    combine_x_y_z_005.location = (1229.0, -295.7998046875)
    combine_x_y_z_005.bl_label = "Combine XYZ"
    # Y
    combine_x_y_z_005.inputs[1].default_value = 1.0
    # Z
    combine_x_y_z_005.inputs[2].default_value = 1.0
    # Links for combine_x_y_z_005
    links.new(combine_x_y_z_005.outputs[0], vector_math_004.inputs[1])

    float_curve_007 = nodes.new("ShaderNodeFloatCurve")
    float_curve_007.name = "Float Curve.007"
    float_curve_007.label = ""
    float_curve_007.location = (969.0, -295.7998046875)
    float_curve_007.bl_label = "Float Curve"
    # Factor
    float_curve_007.inputs[0].default_value = 1.0
    # Links for float_curve_007
    links.new(map_range_004.outputs[0], float_curve_007.inputs[1])
    links.new(float_curve_007.outputs[0], combine_x_y_z_005.inputs[0])

    resample_curve_004 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_004.name = "Resample Curve.004"
    resample_curve_004.label = ""
    resample_curve_004.location = (2129.0, -395.7998046875)
    resample_curve_004.bl_label = "Resample Curve"
    resample_curve_004.keep_last_segment = True
    # Selection
    resample_curve_004.inputs[1].default_value = True
    # Mode
    resample_curve_004.inputs[2].default_value = "Length"
    # Count
    resample_curve_004.inputs[3].default_value = 10
    # Length
    resample_curve_004.inputs[4].default_value = 0.013799999840557575
    # Links for resample_curve_004
    links.new(transform_geometry_021.outputs[0], resample_curve_004.inputs[0])

    instance_on_points_005 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_005.name = "Instance on Points.005"
    instance_on_points_005.label = ""
    instance_on_points_005.location = (3229.0, -555.7998046875)
    instance_on_points_005.bl_label = "Instance on Points"
    # Selection
    instance_on_points_005.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_005.inputs[3].default_value = False
    # Instance Index
    instance_on_points_005.inputs[4].default_value = 0
    # Scale
    instance_on_points_005.inputs[6].default_value = Vector((0.699999988079071, 0.699999988079071, 0.699999988079071))
    # Links for instance_on_points_005

    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.name = "Align Rotation to Vector.002"
    align_rotation_to_vector_002.label = ""
    align_rotation_to_vector_002.location = (29.0, -35.7998046875)
    align_rotation_to_vector_002.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_002.axis = "X"
    align_rotation_to_vector_002.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_002.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_002.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_002

    curve_tangent_002 = nodes.new("GeometryNodeInputTangent")
    curve_tangent_002.name = "Curve Tangent.002"
    curve_tangent_002.label = ""
    curve_tangent_002.location = (29.0, -195.7998046875)
    curve_tangent_002.bl_label = "Curve Tangent"
    # Links for curve_tangent_002
    links.new(curve_tangent_002.outputs[0], align_rotation_to_vector_002.inputs[2])

    align_rotation_to_vector_003 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_003.name = "Align Rotation to Vector.003"
    align_rotation_to_vector_003.label = ""
    align_rotation_to_vector_003.location = (189.0, -35.7998046875)
    align_rotation_to_vector_003.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_003.axis = "Y"
    align_rotation_to_vector_003.pivot_axis = "AUTO"
    # Factor
    align_rotation_to_vector_003.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_003
    links.new(align_rotation_to_vector_002.outputs[0], align_rotation_to_vector_003.inputs[0])

    normal_002 = nodes.new("GeometryNodeInputNormal")
    normal_002.name = "Normal.002"
    normal_002.label = ""
    normal_002.location = (189.0, -195.7998046875)
    normal_002.bl_label = "Normal"
    normal_002.legacy_corner_normals = False
    # Links for normal_002
    links.new(normal_002.outputs[0], align_rotation_to_vector_003.inputs[2])

    spline_parameter_004 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_004.name = "Spline Parameter.004"
    spline_parameter_004.label = ""
    spline_parameter_004.location = (1669.0, -55.7998046875)
    spline_parameter_004.bl_label = "Spline Parameter"
    # Links for spline_parameter_004

    math_012 = nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.label = ""
    math_012.location = (1849.0, -55.7998046875)
    math_012.bl_label = "Math"
    math_012.operation = "SUBTRACT"
    math_012.use_clamp = False
    # Value
    math_012.inputs[1].default_value = 0.7400000095367432
    # Value
    math_012.inputs[2].default_value = 0.5
    # Links for math_012
    links.new(spline_parameter_004.outputs[0], math_012.inputs[0])

    math_013 = nodes.new("ShaderNodeMath")
    math_013.name = "Math.013"
    math_013.label = ""
    math_013.location = (2029.0, -55.7998046875)
    math_013.bl_label = "Math"
    math_013.operation = "ABSOLUTE"
    math_013.use_clamp = False
    # Value
    math_013.inputs[1].default_value = 0.7400000095367432
    # Value
    math_013.inputs[2].default_value = 0.5
    # Links for math_013
    links.new(math_012.outputs[0], math_013.inputs[0])

    set_curve_tilt_003 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_003.name = "Set Curve Tilt.003"
    set_curve_tilt_003.label = ""
    set_curve_tilt_003.location = (2589.0, -395.7998046875)
    set_curve_tilt_003.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_003.inputs[1].default_value = True
    # Links for set_curve_tilt_003
    links.new(set_curve_tilt_003.outputs[0], instance_on_points_005.inputs[0])
    links.new(resample_curve_004.outputs[0], set_curve_tilt_003.inputs[0])

    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.name = "Map Range.005"
    map_range_005.label = ""
    map_range_005.location = (2229.0, -75.7998046875)
    map_range_005.bl_label = "Map Range"
    map_range_005.clamp = True
    map_range_005.interpolation_type = "LINEAR"
    map_range_005.data_type = "FLOAT"
    # From Min
    map_range_005.inputs[1].default_value = 0.0
    # From Max
    map_range_005.inputs[2].default_value = 0.08000002801418304
    # To Min
    map_range_005.inputs[3].default_value = 0.6799999475479126
    # To Max
    map_range_005.inputs[4].default_value = 0.47999998927116394
    # Steps
    map_range_005.inputs[5].default_value = 4.0
    # Vector
    map_range_005.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_005.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_005.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_005.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_005.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_005.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_005
    links.new(math_013.outputs[0], map_range_005.inputs[0])
    links.new(map_range_005.outputs[0], set_curve_tilt_003.inputs[2])

    float_curve_008 = nodes.new("ShaderNodeFloatCurve")
    float_curve_008.name = "Float Curve.008"
    float_curve_008.label = ""
    float_curve_008.location = (269.0, -1115.7998046875)
    float_curve_008.bl_label = "Float Curve"
    # Factor
    float_curve_008.inputs[0].default_value = 1.0
    # Links for float_curve_008

    spline_parameter_005 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_005.name = "Spline Parameter.005"
    spline_parameter_005.label = ""
    spline_parameter_005.location = (29.0, -1355.7998046875)
    spline_parameter_005.bl_label = "Spline Parameter"
    # Links for spline_parameter_005
    links.new(spline_parameter_005.outputs[0], float_curve_008.inputs[1])

    math_014 = nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.label = ""
    math_014.location = (609.0, -1095.7998046875)
    math_014.bl_label = "Math"
    math_014.operation = "MULTIPLY"
    math_014.use_clamp = False
    # Value
    math_014.inputs[1].default_value = 0.014999999664723873
    # Value
    math_014.inputs[2].default_value = 0.5
    # Links for math_014
    links.new(float_curve_008.outputs[0], math_014.inputs[0])

    frame_020 = nodes.new("NodeFrame")
    frame_020.name = "Frame.020"
    frame_020.label = "Align"
    frame_020.location = (2260.0, -520.0)
    frame_020.bl_label = "Frame"
    frame_020.text = None
    frame_020.shrink = True
    frame_020.label_size = 20
    # Links for frame_020

    math_015 = nodes.new("ShaderNodeMath")
    math_015.name = "Math.015"
    math_015.label = ""
    math_015.location = (1249.0, -655.7998046875)
    math_015.bl_label = "Math"
    math_015.operation = "ADD"
    math_015.use_clamp = False
    # Value
    math_015.inputs[2].default_value = 0.5
    # Links for math_015
    links.new(math_015.outputs[0], math_011.inputs[0])
    links.new(float_curve_006.outputs[0], math_015.inputs[0])

    spline_parameter_006 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_006.name = "Spline Parameter.006"
    spline_parameter_006.label = ""
    spline_parameter_006.location = (29.0, -935.7998046875)
    spline_parameter_006.bl_label = "Spline Parameter"
    # Links for spline_parameter_006

    float_curve_009 = nodes.new("ShaderNodeFloatCurve")
    float_curve_009.name = "Float Curve.009"
    float_curve_009.label = ""
    float_curve_009.location = (269.0, -795.7998046875)
    float_curve_009.bl_label = "Float Curve"
    # Factor
    float_curve_009.inputs[0].default_value = 1.0
    # Links for float_curve_009
    links.new(spline_parameter_006.outputs[0], float_curve_009.inputs[1])
    links.new(float_curve_009.outputs[0], math_015.inputs[1])

    float_curve_010 = nodes.new("ShaderNodeFloatCurve")
    float_curve_010.name = "Float Curve.010"
    float_curve_010.label = ""
    float_curve_010.location = (229.0, -1455.7998046875)
    float_curve_010.bl_label = "Float Curve"
    # Factor
    float_curve_010.inputs[0].default_value = 1.0
    # Links for float_curve_010

    spline_parameter_007 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_007.name = "Spline Parameter.007"
    spline_parameter_007.label = ""
    spline_parameter_007.location = (29.0, -1695.7998046875)
    spline_parameter_007.bl_label = "Spline Parameter"
    # Links for spline_parameter_007
    links.new(spline_parameter_007.outputs[0], float_curve_010.inputs[1])

    math_018 = nodes.new("ShaderNodeMath")
    math_018.name = "Math.018"
    math_018.label = ""
    math_018.location = (609.0, -1435.7998046875)
    math_018.bl_label = "Math"
    math_018.operation = "MULTIPLY"
    math_018.use_clamp = False
    # Value
    math_018.inputs[1].default_value = -0.014999999664723873
    # Value
    math_018.inputs[2].default_value = 0.5
    # Links for math_018
    links.new(float_curve_010.outputs[0], math_018.inputs[0])

    math_019 = nodes.new("ShaderNodeMath")
    math_019.name = "Math.019"
    math_019.label = ""
    math_019.location = (789.0, -1075.7998046875)
    math_019.bl_label = "Math"
    math_019.operation = "ADD"
    math_019.use_clamp = False
    # Value
    math_019.inputs[2].default_value = 0.5
    # Links for math_019
    links.new(math_019.outputs[0], combine_x_y_z_004.inputs[1])
    links.new(math_014.outputs[0], math_019.inputs[0])
    links.new(math_018.outputs[0], math_019.inputs[1])

    frame_022 = nodes.new("NodeFrame")
    frame_022.name = "Frame.022"
    frame_022.label = "Necklace 1"
    frame_022.location = (29.0, -3035.798828125)
    frame_022.bl_label = "Frame"
    frame_022.text = None
    frame_022.shrink = True
    frame_022.label_size = 20
    # Links for frame_022

    quadrilateral = nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
    quadrilateral.name = "Quadrilateral"
    quadrilateral.label = ""
    quadrilateral.location = (29.0, -35.7998046875)
    quadrilateral.bl_label = "Quadrilateral"
    quadrilateral.mode = "RECTANGLE"
    # Width
    quadrilateral.inputs[0].default_value = 0.02500000037252903
    # Height
    quadrilateral.inputs[1].default_value = 0.014999999664723873
    # Bottom Width
    quadrilateral.inputs[2].default_value = 4.0
    # Top Width
    quadrilateral.inputs[3].default_value = 2.0
    # Offset
    quadrilateral.inputs[4].default_value = 1.0
    # Bottom Height
    quadrilateral.inputs[5].default_value = 3.0
    # Top Height
    quadrilateral.inputs[6].default_value = 1.0
    # Point 1
    quadrilateral.inputs[7].default_value = Vector((-1.0, -1.0, 0.0))
    # Point 2
    quadrilateral.inputs[8].default_value = Vector((1.0, -1.0, 0.0))
    # Point 3
    quadrilateral.inputs[9].default_value = Vector((1.0, 1.0, 0.0))
    # Point 4
    quadrilateral.inputs[10].default_value = Vector((-1.0, 1.0, 0.0))
    # Links for quadrilateral

    fillet_curve = nodes.new("GeometryNodeFilletCurve")
    fillet_curve.name = "Fillet Curve"
    fillet_curve.label = ""
    fillet_curve.location = (349.0, -35.7998046875)
    fillet_curve.bl_label = "Fillet Curve"
    # Radius
    fillet_curve.inputs[1].default_value = 0.007000000216066837
    # Limit Radius
    fillet_curve.inputs[2].default_value = True
    # Mode
    fillet_curve.inputs[3].default_value = "Bézier"
    # Count
    fillet_curve.inputs[4].default_value = 1
    # Links for fillet_curve

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.label = ""
    set_spline_type.location = (189.0, -35.7998046875)
    set_spline_type.bl_label = "Set Spline Type"
    set_spline_type.spline_type = "BEZIER"
    # Selection
    set_spline_type.inputs[1].default_value = True
    # Links for set_spline_type
    links.new(set_spline_type.outputs[0], fillet_curve.inputs[0])
    links.new(quadrilateral.outputs[0], set_spline_type.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (509.0, -35.7998046875)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_001.inputs[2].default_value = 0.8519999980926514
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False
    # Links for curve_to_mesh_001
    links.new(fillet_curve.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(curve_to_mesh_001.outputs[0], instance_on_points_005.inputs[2])

    curve_circle_005 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_005.name = "Curve Circle.005"
    curve_circle_005.label = ""
    curve_circle_005.location = (349.0, -155.7998046875)
    curve_circle_005.bl_label = "Curve Circle"
    curve_circle_005.mode = "RADIUS"
    # Resolution
    curve_circle_005.inputs[0].default_value = 6
    # Point 1
    curve_circle_005.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_005.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_005.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_005.inputs[4].default_value = 0.003000000026077032
    # Links for curve_circle_005
    links.new(curve_circle_005.outputs[0], curve_to_mesh_001.inputs[1])

    frame_019 = nodes.new("NodeFrame")
    frame_019.name = "Frame.019"
    frame_019.label = "Link"
    frame_019.location = (2260.0, -980.0)
    frame_019.bl_label = "Frame"
    frame_019.text = None
    frame_019.shrink = True
    frame_019.label_size = 20
    # Links for frame_019

    rotate_rotation_006 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_006.name = "Rotate Rotation.006"
    rotate_rotation_006.label = ""
    rotate_rotation_006.location = (509.0, -35.7998046875)
    rotate_rotation_006.bl_label = "Rotate Rotation"
    rotate_rotation_006.rotation_space = "LOCAL"
    # Links for rotate_rotation_006
    links.new(rotate_rotation_006.outputs[0], instance_on_points_005.inputs[5])

    rotate_rotation_005 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_005.name = "Rotate Rotation.005"
    rotate_rotation_005.label = ""
    rotate_rotation_005.location = (349.0, -35.7998046875)
    rotate_rotation_005.bl_label = "Rotate Rotation"
    rotate_rotation_005.rotation_space = "LOCAL"
    # Links for rotate_rotation_005
    links.new(align_rotation_to_vector_003.outputs[0], rotate_rotation_005.inputs[0])
    links.new(rotate_rotation_005.outputs[0], rotate_rotation_006.inputs[0])

    random_value_012 = nodes.new("FunctionNodeRandomValue")
    random_value_012.name = "Random Value.012"
    random_value_012.label = ""
    random_value_012.location = (509.0, -135.7998046875)
    random_value_012.bl_label = "Random Value"
    random_value_012.data_type = "FLOAT_VECTOR"
    # Min
    random_value_012.inputs[0].default_value = [-0.29999998211860657, -0.09999999403953552, 0.0]
    # Max
    random_value_012.inputs[1].default_value = [0.2999999225139618, 0.09999999403953552, 0.0]
    # Min
    random_value_012.inputs[2].default_value = 0.0
    # Max
    random_value_012.inputs[3].default_value = 1.0
    # Min
    random_value_012.inputs[4].default_value = 0
    # Max
    random_value_012.inputs[5].default_value = 100
    # Probability
    random_value_012.inputs[6].default_value = 0.5
    # ID
    random_value_012.inputs[7].default_value = 0
    # Seed
    random_value_012.inputs[8].default_value = 3
    # Links for random_value_012
    links.new(random_value_012.outputs[0], rotate_rotation_006.inputs[1])

    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.label = ""
    index_001.location = (189.0, -275.7998046875)
    index_001.bl_label = "Index"
    # Links for index_001

    math_016 = nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.label = ""
    math_016.location = (189.0, -335.7998046875)
    math_016.bl_label = "Math"
    math_016.operation = "FLOORED_MODULO"
    math_016.use_clamp = False
    # Value
    math_016.inputs[1].default_value = 2.0
    # Value
    math_016.inputs[2].default_value = 0.5
    # Links for math_016
    links.new(index_001.outputs[0], math_016.inputs[0])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (349.0, -235.7998046875)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "FLOAT"
    # False
    switch_001.inputs[1].default_value = -0.3799999952316284
    # True
    switch_001.inputs[2].default_value = 0.5
    # Links for switch_001
    links.new(math_016.outputs[0], switch_001.inputs[0])

    combine_x_y_z_006 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_006.name = "Combine XYZ.006"
    combine_x_y_z_006.label = ""
    combine_x_y_z_006.location = (349.0, -155.7998046875)
    combine_x_y_z_006.bl_label = "Combine XYZ"
    # Y
    combine_x_y_z_006.inputs[1].default_value = 0.0
    # Z
    combine_x_y_z_006.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_006
    links.new(switch_001.outputs[0], combine_x_y_z_006.inputs[0])
    links.new(combine_x_y_z_006.outputs[0], rotate_rotation_005.inputs[1])

    join_geometry_012 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_012.name = "Join Geometry.012"
    join_geometry_012.label = ""
    join_geometry_012.location = (5258.0, -2831.5986328125)
    join_geometry_012.bl_label = "Join Geometry"
    # Links for join_geometry_012
    links.new(join_geometry_011.outputs[0], join_geometry_012.inputs[0])
    links.new(join_geometry_012.outputs[0], store_named_attribute.inputs[0])

    curve_circle_006 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_006.name = "Curve Circle.006"
    curve_circle_006.label = ""
    curve_circle_006.location = (29.0, -35.7998046875)
    curve_circle_006.bl_label = "Curve Circle"
    curve_circle_006.mode = "RADIUS"
    # Resolution
    curve_circle_006.inputs[0].default_value = 15
    # Point 1
    curve_circle_006.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_006.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_006.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_006.inputs[4].default_value = 0.009999999776482582
    # Links for curve_circle_006

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (289.0, -35.7998046875)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_002.inputs[2].default_value = 0.22200000286102295
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002
    links.new(curve_circle_006.outputs[0], curve_to_mesh_002.inputs[0])

    sample_curve_001 = nodes.new("GeometryNodeSampleCurve")
    sample_curve_001.name = "Sample Curve.001"
    sample_curve_001.label = ""
    sample_curve_001.location = (3089.0, -1175.7998046875)
    sample_curve_001.bl_label = "Sample Curve"
    sample_curve_001.mode = "FACTOR"
    sample_curve_001.use_all_curves = True
    sample_curve_001.data_type = "FLOAT"
    # Value
    sample_curve_001.inputs[1].default_value = 0.0
    # Factor
    sample_curve_001.inputs[2].default_value = 0.7185045480728149
    # Length
    sample_curve_001.inputs[3].default_value = 0.0
    # Curve Index
    sample_curve_001.inputs[4].default_value = 0
    # Links for sample_curve_001
    links.new(set_curve_tilt_003.outputs[0], sample_curve_001.inputs[0])

    transform_geometry_022 = nodes.new("GeometryNodeTransform")
    transform_geometry_022.name = "Transform Geometry.022"
    transform_geometry_022.label = ""
    transform_geometry_022.location = (3449.0, -1215.7998046875)
    transform_geometry_022.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_022.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_022.inputs[3].default_value = Euler((1.5707963705062866, 0.0, 0.34033918380737305), 'XYZ')
    # Scale
    transform_geometry_022.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_022
    links.new(curve_to_mesh_002.outputs[0], transform_geometry_022.inputs[0])

    join_geometry_013 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_013.name = "Join Geometry.013"
    join_geometry_013.label = ""
    join_geometry_013.location = (4109.0, -895.7998046875)
    join_geometry_013.bl_label = "Join Geometry"
    # Links for join_geometry_013
    links.new(instance_on_points_005.outputs[0], join_geometry_013.inputs[0])
    links.new(transform_geometry_022.outputs[0], join_geometry_013.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (3269.0, -1255.7998046875)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "ADD"
    # Vector
    vector_math_005.inputs[1].default_value = [0.0, 0.0, -0.012000000104308128]
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_005.inputs[3].default_value = 1.0
    # Links for vector_math_005
    links.new(vector_math_005.outputs[0], transform_geometry_022.inputs[2])
    links.new(sample_curve_001.outputs[1], vector_math_005.inputs[0])

    curve_circle_007 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_007.name = "Curve Circle.007"
    curve_circle_007.label = ""
    curve_circle_007.location = (29.0, -155.7998046875)
    curve_circle_007.bl_label = "Curve Circle"
    curve_circle_007.mode = "RADIUS"
    # Resolution
    curve_circle_007.inputs[0].default_value = 6
    # Point 1
    curve_circle_007.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_007.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_007.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_007.inputs[4].default_value = 0.009999999776482582
    # Links for curve_circle_007
    links.new(curve_circle_007.outputs[0], curve_to_mesh_002.inputs[1])

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.label = ""
    curve_line.location = (29.0, -555.7998046875)
    curve_line.bl_label = "Curve Line"
    curve_line.mode = "DIRECTION"
    # Start
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, -0.009999999776482582))
    # End
    curve_line.inputs[1].default_value = Vector((0.0, 0.0, 1.0))
    # Direction
    curve_line.inputs[2].default_value = [0.0, 0.0, -1.0]
    # Length
    curve_line.inputs[3].default_value = 0.05000000074505806
    # Links for curve_line

    transform_geometry_023 = nodes.new("GeometryNodeTransform")
    transform_geometry_023.name = "Transform Geometry.023"
    transform_geometry_023.label = ""
    transform_geometry_023.location = (4009.0, -1575.7998046875)
    transform_geometry_023.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_023.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_023.inputs[3].default_value = Euler((0.0, 0.06632250547409058, -0.6752678751945496), 'XYZ')
    # Scale
    transform_geometry_023.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_023
    links.new(transform_geometry_023.outputs[0], join_geometry_013.inputs[0])

    frame_021 = nodes.new("NodeFrame")
    frame_021.name = "Frame.021"
    frame_021.label = "Loop"
    frame_021.location = (2420.0, -1400.0)
    frame_021.bl_label = "Frame"
    frame_021.text = None
    frame_021.shrink = True
    frame_021.label_size = 20
    # Links for frame_021

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (3269.0, -1475.7998046875)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "ADD"
    # Vector
    vector_math_006.inputs[1].default_value = [0.0, 0.0, -0.017999999225139618]
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006
    links.new(vector_math_006.outputs[0], transform_geometry_023.inputs[2])
    links.new(vector_math_005.outputs[0], vector_math_006.inputs[0])

    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.name = "Curve to Mesh.003"
    curve_to_mesh_003.label = ""
    curve_to_mesh_003.location = (529.0, -535.7998046875)
    curve_to_mesh_003.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_003.inputs[3].default_value = True
    # Links for curve_to_mesh_003

    resample_curve_005 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_005.name = "Resample Curve.005"
    resample_curve_005.label = ""
    resample_curve_005.location = (209.0, -555.7998046875)
    resample_curve_005.bl_label = "Resample Curve"
    resample_curve_005.keep_last_segment = True
    # Selection
    resample_curve_005.inputs[1].default_value = True
    # Mode
    resample_curve_005.inputs[2].default_value = "Count"
    # Count
    resample_curve_005.inputs[3].default_value = 128
    # Length
    resample_curve_005.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_005
    links.new(resample_curve_005.outputs[0], curve_to_mesh_003.inputs[0])
    links.new(curve_line.outputs[0], resample_curve_005.inputs[0])

    curve_circle_008 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_008.name = "Curve Circle.008"
    curve_circle_008.label = ""
    curve_circle_008.location = (529.0, -675.7998046875)
    curve_circle_008.bl_label = "Curve Circle"
    curve_circle_008.mode = "RADIUS"
    # Resolution
    curve_circle_008.inputs[0].default_value = 32
    # Point 1
    curve_circle_008.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_008.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_008.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_008.inputs[4].default_value = 0.003000000026077032
    # Links for curve_circle_008
    links.new(curve_circle_008.outputs[0], curve_to_mesh_003.inputs[1])

    spline_parameter_008 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_008.name = "Spline Parameter.008"
    spline_parameter_008.label = ""
    spline_parameter_008.location = (29.0, -835.7998046875)
    spline_parameter_008.bl_label = "Spline Parameter"
    # Links for spline_parameter_008

    float_curve_011 = nodes.new("ShaderNodeFloatCurve")
    float_curve_011.name = "Float Curve.011"
    float_curve_011.label = ""
    float_curve_011.location = (209.0, -675.7998046875)
    float_curve_011.bl_label = "Float Curve"
    # Factor
    float_curve_011.inputs[0].default_value = 1.0
    # Links for float_curve_011
    links.new(spline_parameter_008.outputs[0], float_curve_011.inputs[1])
    links.new(float_curve_011.outputs[0], curve_to_mesh_003.inputs[2])

    curve_circle_009 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_009.name = "Curve Circle.009"
    curve_circle_009.label = ""
    curve_circle_009.location = (649.0, -35.7998046875)
    curve_circle_009.bl_label = "Curve Circle"
    curve_circle_009.mode = "RADIUS"
    # Resolution
    curve_circle_009.inputs[0].default_value = 12
    # Point 1
    curve_circle_009.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_009.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_009.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_009.inputs[4].default_value = 0.004000000189989805
    # Links for curve_circle_009

    curve_to_mesh_004 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_004.name = "Curve to Mesh.004"
    curve_to_mesh_004.label = ""
    curve_to_mesh_004.location = (829.0, -75.7998046875)
    curve_to_mesh_004.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_004.inputs[2].default_value = 0.800000011920929
    # Fill Caps
    curve_to_mesh_004.inputs[3].default_value = True
    # Links for curve_to_mesh_004
    links.new(curve_circle_009.outputs[0], curve_to_mesh_004.inputs[0])

    curve_circle_010 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_010.name = "Curve Circle.010"
    curve_circle_010.label = ""
    curve_circle_010.location = (649.0, -175.7998046875)
    curve_circle_010.bl_label = "Curve Circle"
    curve_circle_010.mode = "RADIUS"
    # Resolution
    curve_circle_010.inputs[0].default_value = 6
    # Point 1
    curve_circle_010.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_010.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_010.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_010.inputs[4].default_value = 0.0020000000949949026
    # Links for curve_circle_010
    links.new(curve_circle_010.outputs[0], curve_to_mesh_004.inputs[1])

    join_geometry_014 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_014.name = "Join Geometry.014"
    join_geometry_014.label = ""
    join_geometry_014.location = (2129.0, -255.7998046875)
    join_geometry_014.bl_label = "Join Geometry"
    # Links for join_geometry_014
    links.new(curve_to_mesh_003.outputs[0], join_geometry_014.inputs[0])
    links.new(join_geometry_014.outputs[0], transform_geometry_023.inputs[0])

    curve_circle_011 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_011.name = "Curve Circle.011"
    curve_circle_011.label = ""
    curve_circle_011.location = (649.0, -315.7998046875)
    curve_circle_011.bl_label = "Curve Circle"
    curve_circle_011.mode = "RADIUS"
    # Resolution
    curve_circle_011.inputs[0].default_value = 6
    # Point 1
    curve_circle_011.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_011.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_011.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_011.inputs[4].default_value = 0.00800000037997961
    # Links for curve_circle_011

    instance_on_points_006 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_006.name = "Instance on Points.006"
    instance_on_points_006.label = ""
    instance_on_points_006.location = (1009.0, -95.7998046875)
    instance_on_points_006.bl_label = "Instance on Points"
    # Selection
    instance_on_points_006.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_006.inputs[3].default_value = False
    # Instance Index
    instance_on_points_006.inputs[4].default_value = 0
    # Rotation
    instance_on_points_006.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_006.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_006
    links.new(curve_to_mesh_004.outputs[0], instance_on_points_006.inputs[2])
    links.new(curve_circle_011.outputs[0], instance_on_points_006.inputs[0])

    transform_geometry_024 = nodes.new("GeometryNodeTransform")
    transform_geometry_024.name = "Transform Geometry.024"
    transform_geometry_024.label = ""
    transform_geometry_024.location = (1189.0, -95.7998046875)
    transform_geometry_024.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_024.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_024.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_024.inputs[3].default_value = Euler((1.5707963705062866, 0.5235987901687622, 0.0), 'XYZ')
    # Scale
    transform_geometry_024.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_024
    links.new(instance_on_points_006.outputs[0], transform_geometry_024.inputs[0])
    links.new(transform_geometry_024.outputs[0], join_geometry_014.inputs[0])

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    grid.label = ""
    grid.location = (709.0, -635.7998046875)
    grid.bl_label = "Grid"
    # Size X
    grid.inputs[0].default_value = 0.014999999664723873
    # Size Y
    grid.inputs[1].default_value = 0.012000000104308128
    # Vertices X
    grid.inputs[2].default_value = 12
    # Vertices Y
    grid.inputs[3].default_value = 4
    # Links for grid

    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.label = ""
    delete_geometry_001.location = (889.0, -635.7998046875)
    delete_geometry_001.bl_label = "Delete Geometry"
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "FACE"
    # Links for delete_geometry_001
    links.new(grid.outputs[0], delete_geometry_001.inputs[0])

    random_value_013 = nodes.new("FunctionNodeRandomValue")
    random_value_013.name = "Random Value.013"
    random_value_013.label = ""
    random_value_013.location = (889.0, -755.7998046875)
    random_value_013.bl_label = "Random Value"
    random_value_013.data_type = "BOOLEAN"
    # Min
    random_value_013.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_013.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_013.inputs[2].default_value = 0.0
    # Max
    random_value_013.inputs[3].default_value = 1.0
    # Min
    random_value_013.inputs[4].default_value = 0
    # Max
    random_value_013.inputs[5].default_value = 100
    # Probability
    random_value_013.inputs[6].default_value = 0.2734806537628174
    # ID
    random_value_013.inputs[7].default_value = 0
    # Seed
    random_value_013.inputs[8].default_value = 78
    # Links for random_value_013
    links.new(random_value_013.outputs[3], delete_geometry_001.inputs[1])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.label = ""
    extrude_mesh.location = (1069.0, -635.7998046875)
    extrude_mesh.bl_label = "Extrude Mesh"
    extrude_mesh.mode = "FACES"
    # Selection
    extrude_mesh.inputs[1].default_value = True
    # Offset
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.003000000026077032
    # Individual
    extrude_mesh.inputs[4].default_value = False
    # Links for extrude_mesh
    links.new(delete_geometry_001.outputs[0], extrude_mesh.inputs[0])

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.name = "Flip Faces"
    flip_faces.label = ""
    flip_faces.location = (1069.0, -555.7998046875)
    flip_faces.bl_label = "Flip Faces"
    # Selection
    flip_faces.inputs[1].default_value = True
    # Links for flip_faces
    links.new(delete_geometry_001.outputs[0], flip_faces.inputs[0])

    join_geometry_015 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_015.name = "Join Geometry.015"
    join_geometry_015.label = ""
    join_geometry_015.location = (1229.0, -635.7998046875)
    join_geometry_015.bl_label = "Join Geometry"
    # Links for join_geometry_015
    links.new(extrude_mesh.outputs[0], join_geometry_015.inputs[0])
    links.new(flip_faces.outputs[0], join_geometry_015.inputs[0])

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.label = ""
    merge_by_distance.location = (1409.0, -635.7998046875)
    merge_by_distance.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance.inputs[1].default_value = True
    # Mode
    merge_by_distance.inputs[2].default_value = "All"
    # Distance
    merge_by_distance.inputs[3].default_value = 9.999999747378752e-05
    # Links for merge_by_distance
    links.new(join_geometry_015.outputs[0], merge_by_distance.inputs[0])

    transform_geometry_025 = nodes.new("GeometryNodeTransform")
    transform_geometry_025.name = "Transform Geometry.025"
    transform_geometry_025.label = ""
    transform_geometry_025.location = (1769.0, -575.7998046875)
    transform_geometry_025.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_025.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_025.inputs[2].default_value = Vector((0.006000000052154064, 0.001500000013038516, -0.04999999701976776))
    # Rotation
    transform_geometry_025.inputs[3].default_value = Euler((1.5707963705062866, -1.5707963705062866, 0.0), 'XYZ')
    # Scale
    transform_geometry_025.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_025
    links.new(transform_geometry_025.outputs[0], join_geometry_014.inputs[0])

    subdivision_surface = nodes.new("GeometryNodeSubdivisionSurface")
    subdivision_surface.name = "Subdivision Surface"
    subdivision_surface.label = ""
    subdivision_surface.location = (1589.0, -635.7998046875)
    subdivision_surface.bl_label = "Subdivision Surface"
    # Level
    subdivision_surface.inputs[1].default_value = 1
    # Edge Crease
    subdivision_surface.inputs[2].default_value = 0.8063265681266785
    # Vertex Crease
    subdivision_surface.inputs[3].default_value = 0.0
    # Limit Surface
    subdivision_surface.inputs[4].default_value = True
    # UV Smooth
    subdivision_surface.inputs[5].default_value = "Keep Boundaries"
    # Boundary Smooth
    subdivision_surface.inputs[6].default_value = "All"
    # Links for subdivision_surface
    links.new(subdivision_surface.outputs[0], transform_geometry_025.inputs[0])
    links.new(merge_by_distance.outputs[0], subdivision_surface.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.name = "Set Shade Smooth.001"
    set_shade_smooth_001.label = ""
    set_shade_smooth_001.location = (4309.0, -915.7998046875)
    set_shade_smooth_001.bl_label = "Set Shade Smooth"
    set_shade_smooth_001.domain = "FACE"
    # Selection
    set_shade_smooth_001.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_001.inputs[2].default_value = True
    # Links for set_shade_smooth_001
    links.new(join_geometry_013.outputs[0], set_shade_smooth_001.inputs[0])

    frame_023 = nodes.new("NodeFrame")
    frame_023.name = "Frame.023"
    frame_023.label = "Key"
    frame_023.location = (1520.0, -1820.0)
    frame_023.bl_label = "Frame"
    frame_023.text = None
    frame_023.shrink = True
    frame_023.label_size = 20
    # Links for frame_023

    store_named_attribute_007 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_007.name = "Store Named Attribute.007"
    store_named_attribute_007.label = ""
    store_named_attribute_007.location = (4469.0, -895.7998046875)
    store_named_attribute_007.bl_label = "Store Named Attribute"
    store_named_attribute_007.data_type = "BOOLEAN"
    store_named_attribute_007.domain = "POINT"
    # Selection
    store_named_attribute_007.inputs[1].default_value = True
    # Name
    store_named_attribute_007.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_007.inputs[3].default_value = True
    # Links for store_named_attribute_007
    links.new(store_named_attribute_007.outputs[0], join_geometry_012.inputs[0])
    links.new(set_shade_smooth_001.outputs[0], store_named_attribute_007.inputs[0])

    frame_024 = nodes.new("NodeFrame")
    frame_024.name = "Frame.024"
    frame_024.label = "Necklaces"
    frame_024.location = (1062.0, 14831.5986328125)
    frame_024.bl_label = "Frame"
    frame_024.text = None
    frame_024.shrink = True
    frame_024.label_size = 20
    # Links for frame_024

    ico_sphere_006 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_006.name = "Ico Sphere.006"
    ico_sphere_006.label = ""
    ico_sphere_006.location = (29.0, -1295.80029296875)
    ico_sphere_006.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_006.inputs[0].default_value = 0.029999999329447746
    # Subdivisions
    ico_sphere_006.inputs[1].default_value = 3
    # Links for ico_sphere_006

    transform_geometry_026 = nodes.new("GeometryNodeTransform")
    transform_geometry_026.name = "Transform Geometry.026"
    transform_geometry_026.label = ""
    transform_geometry_026.location = (209.0, -1295.80029296875)
    transform_geometry_026.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_026.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_026.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_026.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_026.inputs[4].default_value = Vector((1.0, 1.0, 0.5))
    # Links for transform_geometry_026
    links.new(ico_sphere_006.outputs[0], transform_geometry_026.inputs[0])

    instance_on_points_007 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_007.name = "Instance on Points.007"
    instance_on_points_007.label = ""
    instance_on_points_007.location = (389.0, -1195.80029296875)
    instance_on_points_007.bl_label = "Instance on Points"
    # Selection
    instance_on_points_007.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_007.inputs[3].default_value = False
    # Instance Index
    instance_on_points_007.inputs[4].default_value = 0
    # Rotation
    instance_on_points_007.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_007.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_007
    links.new(transform_geometry_026.outputs[0], instance_on_points_007.inputs[2])

    quadratic_bézier = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier.name = "Quadratic Bézier"
    quadratic_bézier.label = ""
    quadratic_bézier.location = (29.0, -975.80029296875)
    quadratic_bézier.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier.inputs[0].default_value = 16
    # Start
    quadratic_bézier.inputs[1].default_value = Vector((-0.019999999552965164, 0.0, 0.0))
    # Middle
    quadratic_bézier.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.009999999776482582))
    # End
    quadratic_bézier.inputs[3].default_value = Vector((0.019999999552965164, 0.0, 0.0))
    # Links for quadratic_bézier
    links.new(quadratic_bézier.outputs[0], instance_on_points_007.inputs[0])

    realize_instances_003 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.name = "Realize Instances.003"
    realize_instances_003.label = ""
    realize_instances_003.location = (569.0, -1195.80029296875)
    realize_instances_003.bl_label = "Realize Instances"
    # Selection
    realize_instances_003.inputs[1].default_value = True
    # Realize All
    realize_instances_003.inputs[2].default_value = True
    # Depth
    realize_instances_003.inputs[3].default_value = 0
    # Links for realize_instances_003
    links.new(instance_on_points_007.outputs[0], realize_instances_003.inputs[0])

    mesh_to_s_d_f_grid = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid.name = "Mesh to SDF Grid"
    mesh_to_s_d_f_grid.label = ""
    mesh_to_s_d_f_grid.location = (729.0, -1195.80029296875)
    mesh_to_s_d_f_grid.bl_label = "Mesh to SDF Grid"
    # Voxel Size
    mesh_to_s_d_f_grid.inputs[1].default_value = 0.009999999776482582
    # Band Width
    mesh_to_s_d_f_grid.inputs[2].default_value = 1
    # Links for mesh_to_s_d_f_grid
    links.new(realize_instances_003.outputs[0], mesh_to_s_d_f_grid.inputs[0])

    grid_to_mesh = nodes.new("GeometryNodeGridToMesh")
    grid_to_mesh.name = "Grid to Mesh"
    grid_to_mesh.label = ""
    grid_to_mesh.location = (1089.0, -1195.80029296875)
    grid_to_mesh.bl_label = "Grid to Mesh"
    # Threshold
    grid_to_mesh.inputs[1].default_value = 0.0
    # Adaptivity
    grid_to_mesh.inputs[2].default_value = 0.0
    # Links for grid_to_mesh

    dual_mesh_001 = nodes.new("GeometryNodeDualMesh")
    dual_mesh_001.name = "Dual Mesh.001"
    dual_mesh_001.label = ""
    dual_mesh_001.location = (1409.0, -1195.80029296875)
    dual_mesh_001.bl_label = "Dual Mesh"
    # Keep Boundaries
    dual_mesh_001.inputs[1].default_value = False
    # Links for dual_mesh_001

    triangulate = nodes.new("GeometryNodeTriangulate")
    triangulate.name = "Triangulate"
    triangulate.label = ""
    triangulate.location = (1249.0, -1195.80029296875)
    triangulate.bl_label = "Triangulate"
    # Selection
    triangulate.inputs[1].default_value = True
    # Quad Method
    triangulate.inputs[2].default_value = "Shortest Diagonal"
    # N-gon Method
    triangulate.inputs[3].default_value = "Beauty"
    # Links for triangulate
    links.new(triangulate.outputs[0], dual_mesh_001.inputs[0])
    links.new(grid_to_mesh.outputs[0], triangulate.inputs[0])

    s_d_f_grid_boolean = nodes.new("GeometryNodeSDFGridBoolean")
    s_d_f_grid_boolean.name = "SDF Grid Boolean"
    s_d_f_grid_boolean.label = ""
    s_d_f_grid_boolean.location = (909.0, -1195.80029296875)
    s_d_f_grid_boolean.bl_label = "SDF Grid Boolean"
    s_d_f_grid_boolean.operation = "INTERSECT"
    # Grid 1
    s_d_f_grid_boolean.inputs[0].default_value = 0.0
    # Links for s_d_f_grid_boolean
    links.new(s_d_f_grid_boolean.outputs[0], grid_to_mesh.inputs[0])
    links.new(mesh_to_s_d_f_grid.outputs[0], s_d_f_grid_boolean.inputs[1])

    cube = nodes.new("GeometryNodeMeshCube")
    cube.name = "Cube"
    cube.label = ""
    cube.location = (409.0, -1535.80029296875)
    cube.bl_label = "Cube"
    # Size
    cube.inputs[0].default_value = Vector((1.0, 1.0, 0.019999999552965164))
    # Vertices X
    cube.inputs[1].default_value = 2
    # Vertices Y
    cube.inputs[2].default_value = 2
    # Vertices Z
    cube.inputs[3].default_value = 2
    # Links for cube

    mesh_to_s_d_f_grid_001 = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid_001.name = "Mesh to SDF Grid.001"
    mesh_to_s_d_f_grid_001.label = ""
    mesh_to_s_d_f_grid_001.location = (769.0, -1355.80029296875)
    mesh_to_s_d_f_grid_001.bl_label = "Mesh to SDF Grid"
    # Voxel Size
    mesh_to_s_d_f_grid_001.inputs[1].default_value = 0.009999999776482582
    # Band Width
    mesh_to_s_d_f_grid_001.inputs[2].default_value = 1
    # Links for mesh_to_s_d_f_grid_001
    links.new(mesh_to_s_d_f_grid_001.outputs[0], s_d_f_grid_boolean.inputs[1])

    transform_geometry_027 = nodes.new("GeometryNodeTransform")
    transform_geometry_027.name = "Transform Geometry.027"
    transform_geometry_027.label = ""
    transform_geometry_027.location = (569.0, -1515.80029296875)
    transform_geometry_027.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_027.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_027.inputs[2].default_value = Vector((0.0, 0.0, 0.009999999776482582))
    # Rotation
    transform_geometry_027.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_027.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_027
    links.new(cube.outputs[0], transform_geometry_027.inputs[0])
    links.new(transform_geometry_027.outputs[0], mesh_to_s_d_f_grid_001.inputs[0])

    mesh_boolean = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean.name = "Mesh Boolean"
    mesh_boolean.label = ""
    mesh_boolean.location = (1589.0, -1195.80029296875)
    mesh_boolean.bl_label = "Mesh Boolean"
    mesh_boolean.operation = "DIFFERENCE"
    mesh_boolean.solver = "MANIFOLD"
    # Self Intersection
    mesh_boolean.inputs[2].default_value = False
    # Hole Tolerant
    mesh_boolean.inputs[3].default_value = False
    # Links for mesh_boolean
    links.new(dual_mesh_001.outputs[0], mesh_boolean.inputs[0])

    cube_001 = nodes.new("GeometryNodeMeshCube")
    cube_001.name = "Cube.001"
    cube_001.label = ""
    cube_001.location = (1249.0, -1335.80029296875)
    cube_001.bl_label = "Cube"
    # Size
    cube_001.inputs[0].default_value = Vector((1.0, 1.0, 1.0))
    # Vertices X
    cube_001.inputs[1].default_value = 2
    # Vertices Y
    cube_001.inputs[2].default_value = 2
    # Vertices Z
    cube_001.inputs[3].default_value = 2
    # Links for cube_001

    transform_geometry_028 = nodes.new("GeometryNodeTransform")
    transform_geometry_028.name = "Transform Geometry.028"
    transform_geometry_028.label = ""
    transform_geometry_028.location = (1409.0, -1335.80029296875)
    transform_geometry_028.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_028.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_028.inputs[2].default_value = Vector((0.5, 0.0, 0.0))
    # Rotation
    transform_geometry_028.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_028.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_028
    links.new(cube_001.outputs[0], transform_geometry_028.inputs[0])
    links.new(transform_geometry_028.outputs[0], mesh_boolean.inputs[1])

    delete_geometry_002 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.name = "Delete Geometry.002"
    delete_geometry_002.label = ""
    delete_geometry_002.location = (1769.0, -1195.80029296875)
    delete_geometry_002.bl_label = "Delete Geometry"
    delete_geometry_002.mode = "ALL"
    delete_geometry_002.domain = "FACE"
    # Links for delete_geometry_002
    links.new(mesh_boolean.outputs[0], delete_geometry_002.inputs[0])
    links.new(mesh_boolean.outputs[1], delete_geometry_002.inputs[1])

    mesh_boolean_001 = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean_001.name = "Mesh Boolean.001"
    mesh_boolean_001.label = ""
    mesh_boolean_001.location = (1449.0, -195.80029296875)
    mesh_boolean_001.bl_label = "Mesh Boolean"
    mesh_boolean_001.operation = "INTERSECT"
    mesh_boolean_001.solver = "MANIFOLD"
    # Self Intersection
    mesh_boolean_001.inputs[2].default_value = False
    # Hole Tolerant
    mesh_boolean_001.inputs[3].default_value = False
    # Links for mesh_boolean_001
    links.new(dual_mesh_001.outputs[0], mesh_boolean_001.inputs[1])

    cube_002 = nodes.new("GeometryNodeMeshCube")
    cube_002.name = "Cube.002"
    cube_002.label = ""
    cube_002.location = (1089.0, -55.80029296875)
    cube_002.bl_label = "Cube"
    # Size
    cube_002.inputs[0].default_value = Vector((1.0, 1.0, 0.0010000000474974513))
    # Vertices X
    cube_002.inputs[1].default_value = 2
    # Vertices Y
    cube_002.inputs[2].default_value = 2
    # Vertices Z
    cube_002.inputs[3].default_value = 2
    # Links for cube_002

    transform_geometry_029 = nodes.new("GeometryNodeTransform")
    transform_geometry_029.name = "Transform Geometry.029"
    transform_geometry_029.label = ""
    transform_geometry_029.location = (1249.0, -55.80029296875)
    transform_geometry_029.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_029.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_029.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    # Rotation
    transform_geometry_029.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_029.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_029
    links.new(cube_002.outputs[0], transform_geometry_029.inputs[0])
    links.new(transform_geometry_029.outputs[0], mesh_boolean_001.inputs[1])

    join_geometry_016 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_016.name = "Join Geometry.016"
    join_geometry_016.label = ""
    join_geometry_016.location = (5609.0, -795.80029296875)
    join_geometry_016.bl_label = "Join Geometry"
    # Links for join_geometry_016

    delete_geometry_003 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_003.name = "Delete Geometry.003"
    delete_geometry_003.label = ""
    delete_geometry_003.location = (1969.0, -175.80029296875)
    delete_geometry_003.bl_label = "Delete Geometry"
    delete_geometry_003.mode = "ALL"
    delete_geometry_003.domain = "POINT"
    # Links for delete_geometry_003
    links.new(mesh_boolean_001.outputs[0], delete_geometry_003.inputs[0])

    normal_003 = nodes.new("GeometryNodeInputNormal")
    normal_003.name = "Normal.003"
    normal_003.label = ""
    normal_003.location = (1629.0, -275.80029296875)
    normal_003.bl_label = "Normal"
    normal_003.legacy_corner_normals = False
    # Links for normal_003

    compare_008 = nodes.new("FunctionNodeCompare")
    compare_008.name = "Compare.008"
    compare_008.label = ""
    compare_008.location = (1789.0, -275.80029296875)
    compare_008.bl_label = "Compare"
    compare_008.operation = "EQUAL"
    compare_008.data_type = "VECTOR"
    compare_008.mode = "DIRECTION"
    # A
    compare_008.inputs[0].default_value = 0.0
    # B
    compare_008.inputs[1].default_value = 0.0
    # A
    compare_008.inputs[2].default_value = 0
    # B
    compare_008.inputs[3].default_value = 0
    # B
    compare_008.inputs[5].default_value = [0.0, 0.0, 1.0]
    # A
    compare_008.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_008.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_008.inputs[8].default_value = ""
    # B
    compare_008.inputs[9].default_value = ""
    # C
    compare_008.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_008.inputs[11].default_value = 0.0
    # Epsilon
    compare_008.inputs[12].default_value = 1.5707963705062866
    # Links for compare_008
    links.new(normal_003.outputs[0], compare_008.inputs[4])
    links.new(compare_008.outputs[0], delete_geometry_003.inputs[1])

    mesh_to_curve_003 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_003.name = "Mesh to Curve.003"
    mesh_to_curve_003.label = ""
    mesh_to_curve_003.location = (2129.0, -175.80029296875)
    mesh_to_curve_003.bl_label = "Mesh to Curve"
    mesh_to_curve_003.mode = "EDGES"
    # Selection
    mesh_to_curve_003.inputs[1].default_value = True
    # Links for mesh_to_curve_003
    links.new(delete_geometry_003.outputs[0], mesh_to_curve_003.inputs[0])

    resample_curve_006 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_006.name = "Resample Curve.006"
    resample_curve_006.label = ""
    resample_curve_006.location = (3809.0, -35.80029296875)
    resample_curve_006.bl_label = "Resample Curve"
    resample_curve_006.keep_last_segment = True
    # Selection
    resample_curve_006.inputs[1].default_value = True
    # Mode
    resample_curve_006.inputs[2].default_value = "Count"
    # Count
    resample_curve_006.inputs[3].default_value = 45
    # Length
    resample_curve_006.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_006

    set_spline_cyclic_002 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_002.name = "Set Spline Cyclic.002"
    set_spline_cyclic_002.label = ""
    set_spline_cyclic_002.location = (3649.0, -35.80029296875)
    set_spline_cyclic_002.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic_002.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic_002.inputs[2].default_value = True
    # Links for set_spline_cyclic_002
    links.new(set_spline_cyclic_002.outputs[0], resample_curve_006.inputs[0])

    curve_to_mesh_005 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_005.name = "Curve to Mesh.005"
    curve_to_mesh_005.label = ""
    curve_to_mesh_005.location = (3969.0, -35.80029296875)
    curve_to_mesh_005.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_005.inputs[2].default_value = 0.009999999776482582
    # Fill Caps
    curve_to_mesh_005.inputs[3].default_value = False
    # Links for curve_to_mesh_005
    links.new(curve_to_mesh_005.outputs[0], join_geometry_016.inputs[0])
    links.new(resample_curve_006.outputs[0], curve_to_mesh_005.inputs[0])

    gem_in_holder_3 = nodes.new("GeometryNodeGroup")
    gem_in_holder_3.name = "Gem in Holder.003"
    gem_in_holder_3.label = ""
    gem_in_holder_3.location = (3809.0, -155.80029296875)
    gem_in_holder_3.node_tree = create_gem_in__holder_group()
    gem_in_holder_3.bl_label = "Group"
    # Gem Radius
    gem_in_holder_3.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_3.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_3.inputs[2].default_value = False
    # Scale
    gem_in_holder_3.inputs[3].default_value = 0.004999995231628418
    # Count
    gem_in_holder_3.inputs[4].default_value = 6
    # Seed
    gem_in_holder_3.inputs[5].default_value = 41
    # Wings
    gem_in_holder_3.inputs[6].default_value = False
    # Array Count
    gem_in_holder_3.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_3.inputs[8].default_value = 10
    # Split
    gem_in_holder_3.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder_3.inputs[10].default_value = 3.3099989891052246
    # Links for gem_in_holder_3
    links.new(gem_in_holder_3.outputs[1], curve_to_mesh_005.inputs[1])

    trim_curve_005 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_005.name = "Trim Curve.005"
    trim_curve_005.label = ""
    trim_curve_005.location = (2289.0, -175.80029296875)
    trim_curve_005.bl_label = "Trim Curve"
    trim_curve_005.mode = "FACTOR"
    # Selection
    trim_curve_005.inputs[1].default_value = True
    # Start
    trim_curve_005.inputs[2].default_value = 0.010773210786283016
    # End
    trim_curve_005.inputs[3].default_value = 0.9906079769134521
    # Start
    trim_curve_005.inputs[4].default_value = 0.0
    # End
    trim_curve_005.inputs[5].default_value = 1.0
    # Links for trim_curve_005
    links.new(mesh_to_curve_003.outputs[0], trim_curve_005.inputs[0])

    instance_on_points_008 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_008.name = "Instance on Points.008"
    instance_on_points_008.label = ""
    instance_on_points_008.location = (4689.0, -655.80029296875)
    instance_on_points_008.bl_label = "Instance on Points"
    # Selection
    instance_on_points_008.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_008.inputs[3].default_value = False
    # Instance Index
    instance_on_points_008.inputs[4].default_value = 0
    # Links for instance_on_points_008

    resample_curve_007 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_007.name = "Resample Curve.007"
    resample_curve_007.label = ""
    resample_curve_007.location = (4529.0, -655.80029296875)
    resample_curve_007.bl_label = "Resample Curve"
    resample_curve_007.keep_last_segment = True
    # Selection
    resample_curve_007.inputs[1].default_value = True
    # Mode
    resample_curve_007.inputs[2].default_value = "Count"
    # Count
    resample_curve_007.inputs[3].default_value = 10
    # Length
    resample_curve_007.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_007
    links.new(resample_curve_007.outputs[0], instance_on_points_008.inputs[0])

    align_rotation_to_vector_004 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_004.name = "Align Rotation to Vector.004"
    align_rotation_to_vector_004.label = ""
    align_rotation_to_vector_004.location = (4529.0, -775.80029296875)
    align_rotation_to_vector_004.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_004.axis = "Y"
    align_rotation_to_vector_004.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_004.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_004.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_004
    links.new(align_rotation_to_vector_004.outputs[0], instance_on_points_008.inputs[5])

    curve_tangent_003 = nodes.new("GeometryNodeInputTangent")
    curve_tangent_003.name = "Curve Tangent.003"
    curve_tangent_003.label = ""
    curve_tangent_003.location = (4529.0, -935.80029296875)
    curve_tangent_003.bl_label = "Curve Tangent"
    # Links for curve_tangent_003
    links.new(curve_tangent_003.outputs[0], align_rotation_to_vector_004.inputs[2])

    realize_instances_004 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_004.name = "Realize Instances.004"
    realize_instances_004.label = ""
    realize_instances_004.location = (5029.0, -815.80029296875)
    realize_instances_004.bl_label = "Realize Instances"
    # Selection
    realize_instances_004.inputs[1].default_value = True
    # Realize All
    realize_instances_004.inputs[2].default_value = True
    # Depth
    realize_instances_004.inputs[3].default_value = 0
    # Links for realize_instances_004
    links.new(instance_on_points_008.outputs[0], realize_instances_004.inputs[0])

    transform_geometry_030 = nodes.new("GeometryNodeTransform")
    transform_geometry_030.name = "Transform Geometry.030"
    transform_geometry_030.label = ""
    transform_geometry_030.location = (1949.0, -1295.80029296875)
    transform_geometry_030.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_030.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_030.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_030.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_030.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    # Links for transform_geometry_030
    links.new(delete_geometry_002.outputs[0], transform_geometry_030.inputs[0])

    flip_faces_002 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.name = "Flip Faces.002"
    flip_faces_002.label = ""
    flip_faces_002.location = (2109.0, -1295.80029296875)
    flip_faces_002.bl_label = "Flip Faces"
    # Selection
    flip_faces_002.inputs[1].default_value = True
    # Links for flip_faces_002
    links.new(transform_geometry_030.outputs[0], flip_faces_002.inputs[0])

    join_geometry_018 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_018.name = "Join Geometry.018"
    join_geometry_018.label = ""
    join_geometry_018.location = (2269.0, -1235.80029296875)
    join_geometry_018.bl_label = "Join Geometry"
    # Links for join_geometry_018
    links.new(delete_geometry_002.outputs[0], join_geometry_018.inputs[0])
    links.new(flip_faces_002.outputs[0], join_geometry_018.inputs[0])

    merge_by_distance_001 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_001.name = "Merge by Distance.001"
    merge_by_distance_001.label = ""
    merge_by_distance_001.location = (2449.0, -1235.80029296875)
    merge_by_distance_001.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_001.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_001.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_001
    links.new(join_geometry_018.outputs[0], merge_by_distance_001.inputs[0])

    is_edge_boundary_1 = nodes.new("GeometryNodeGroup")
    is_edge_boundary_1.name = "Is Edge Boundary.001"
    is_edge_boundary_1.label = ""
    is_edge_boundary_1.location = (2269.0, -1315.80029296875)
    is_edge_boundary_1.node_tree = create_is__edge__boundary_group()
    is_edge_boundary_1.bl_label = "Group"
    # Links for is_edge_boundary_1
    links.new(is_edge_boundary_1.outputs[0], merge_by_distance_001.inputs[1])

    spline_parameter_009 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_009.name = "Spline Parameter.009"
    spline_parameter_009.label = ""
    spline_parameter_009.location = (3809.0, -1035.80029296875)
    spline_parameter_009.bl_label = "Spline Parameter"
    # Links for spline_parameter_009

    math_020 = nodes.new("ShaderNodeMath")
    math_020.name = "Math.020"
    math_020.label = ""
    math_020.location = (3969.0, -1035.80029296875)
    math_020.bl_label = "Math"
    math_020.operation = "MULTIPLY"
    math_020.use_clamp = False
    # Value
    math_020.inputs[1].default_value = 2.0
    # Value
    math_020.inputs[2].default_value = 0.5
    # Links for math_020
    links.new(spline_parameter_009.outputs[0], math_020.inputs[0])

    math_021 = nodes.new("ShaderNodeMath")
    math_021.name = "Math.021"
    math_021.label = ""
    math_021.location = (4129.0, -1035.80029296875)
    math_021.bl_label = "Math"
    math_021.operation = "PINGPONG"
    math_021.use_clamp = False
    # Value
    math_021.inputs[1].default_value = 1.0
    # Value
    math_021.inputs[2].default_value = 0.5
    # Links for math_021
    links.new(math_020.outputs[0], math_021.inputs[0])

    curve_to_points_002 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_002.name = "Curve to Points.002"
    curve_to_points_002.label = ""
    curve_to_points_002.location = (2449.0, -175.80029296875)
    curve_to_points_002.bl_label = "Curve to Points"
    curve_to_points_002.mode = "EVALUATED"
    # Count
    curve_to_points_002.inputs[1].default_value = 10
    # Length
    curve_to_points_002.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points_002
    links.new(trim_curve_005.outputs[0], curve_to_points_002.inputs[0])

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    points_to_curves.label = ""
    points_to_curves.location = (2609.0, -175.80029296875)
    points_to_curves.bl_label = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0
    # Links for points_to_curves
    links.new(curve_to_points_002.outputs[0], points_to_curves.inputs[0])
    links.new(points_to_curves.outputs[0], set_spline_cyclic_002.inputs[0])

    gradient_texture = nodes.new("ShaderNodeTexGradient")
    gradient_texture.name = "Gradient Texture"
    gradient_texture.label = ""
    gradient_texture.location = (2129.0, -355.80029296875)
    gradient_texture.bl_label = "Gradient Texture"
    gradient_texture.gradient_type = "RADIAL"
    # Vector
    gradient_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Links for gradient_texture

    math_022 = nodes.new("ShaderNodeMath")
    math_022.name = "Math.022"
    math_022.label = ""
    math_022.location = (2289.0, -355.80029296875)
    math_022.bl_label = "Math"
    math_022.operation = "ADD"
    math_022.use_clamp = False
    # Value
    math_022.inputs[1].default_value = 0.5
    # Value
    math_022.inputs[2].default_value = 0.5
    # Links for math_022
    links.new(gradient_texture.outputs[1], math_022.inputs[0])

    math_023 = nodes.new("ShaderNodeMath")
    math_023.name = "Math.023"
    math_023.label = ""
    math_023.location = (2449.0, -355.80029296875)
    math_023.bl_label = "Math"
    math_023.operation = "FRACT"
    math_023.use_clamp = False
    # Value
    math_023.inputs[1].default_value = 0.5
    # Value
    math_023.inputs[2].default_value = 0.5
    # Links for math_023
    links.new(math_023.outputs[0], points_to_curves.inputs[2])
    links.new(math_022.outputs[0], math_023.inputs[0])

    delete_geometry_004 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_004.name = "Delete Geometry.004"
    delete_geometry_004.label = ""
    delete_geometry_004.location = (3149.0, -335.80029296875)
    delete_geometry_004.bl_label = "Delete Geometry"
    delete_geometry_004.mode = "ALL"
    delete_geometry_004.domain = "POINT"
    # Links for delete_geometry_004
    links.new(delete_geometry_004.outputs[0], resample_curve_007.inputs[0])
    links.new(points_to_curves.outputs[0], delete_geometry_004.inputs[0])

    position_009 = nodes.new("GeometryNodeInputPosition")
    position_009.name = "Position.009"
    position_009.label = ""
    position_009.location = (2689.0, -415.80029296875)
    position_009.bl_label = "Position"
    # Links for position_009

    separate_x_y_z_008 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_008.name = "Separate XYZ.008"
    separate_x_y_z_008.label = ""
    separate_x_y_z_008.location = (2689.0, -475.80029296875)
    separate_x_y_z_008.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_008
    links.new(position_009.outputs[0], separate_x_y_z_008.inputs[0])

    compare_009 = nodes.new("FunctionNodeCompare")
    compare_009.name = "Compare.009"
    compare_009.label = ""
    compare_009.location = (2849.0, -415.80029296875)
    compare_009.bl_label = "Compare"
    compare_009.operation = "GREATER_THAN"
    compare_009.data_type = "FLOAT"
    compare_009.mode = "ELEMENT"
    # B
    compare_009.inputs[1].default_value = 0.0
    # A
    compare_009.inputs[2].default_value = 0
    # B
    compare_009.inputs[3].default_value = 0
    # A
    compare_009.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_009.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_009.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_009.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_009.inputs[8].default_value = ""
    # B
    compare_009.inputs[9].default_value = ""
    # C
    compare_009.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_009.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_009.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_009
    links.new(separate_x_y_z_008.outputs[0], compare_009.inputs[0])
    links.new(compare_009.outputs[0], delete_geometry_004.inputs[1])

    float_curve_012 = nodes.new("ShaderNodeFloatCurve")
    float_curve_012.name = "Float Curve.012"
    float_curve_012.label = ""
    float_curve_012.location = (4289.0, -1035.80029296875)
    float_curve_012.bl_label = "Float Curve"
    # Factor
    float_curve_012.inputs[0].default_value = 1.0
    # Links for float_curve_012
    links.new(math_021.outputs[0], float_curve_012.inputs[1])
    links.new(float_curve_012.outputs[0], instance_on_points_008.inputs[6])

    transform_geometry_031 = nodes.new("GeometryNodeTransform")
    transform_geometry_031.name = "Transform Geometry.031"
    transform_geometry_031.label = ""
    transform_geometry_031.location = (4869.0, -935.80029296875)
    transform_geometry_031.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_031.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_031.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_031.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_031.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    # Links for transform_geometry_031
    links.new(realize_instances_004.outputs[0], transform_geometry_031.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.name = "Flip Faces.003"
    flip_faces_003.label = ""
    flip_faces_003.location = (5029.0, -935.80029296875)
    flip_faces_003.bl_label = "Flip Faces"
    # Selection
    flip_faces_003.inputs[1].default_value = True
    # Links for flip_faces_003
    links.new(transform_geometry_031.outputs[0], flip_faces_003.inputs[0])

    join_geometry_019 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_019.name = "Join Geometry.019"
    join_geometry_019.label = ""
    join_geometry_019.location = (5229.0, -875.80029296875)
    join_geometry_019.bl_label = "Join Geometry"
    # Links for join_geometry_019
    links.new(join_geometry_019.outputs[0], join_geometry_016.inputs[0])
    links.new(flip_faces_003.outputs[0], join_geometry_019.inputs[0])
    links.new(realize_instances_004.outputs[0], join_geometry_019.inputs[0])

    gem_in_holder_4 = nodes.new("GeometryNodeGroup")
    gem_in_holder_4.name = "Gem in Holder.004"
    gem_in_holder_4.label = ""
    gem_in_holder_4.location = (3149.0, -495.80029296875)
    gem_in_holder_4.node_tree = create_gem_in__holder_group()
    gem_in_holder_4.bl_label = "Group"
    # Gem Radius
    gem_in_holder_4.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_4.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_4.inputs[2].default_value = False
    # Scale
    gem_in_holder_4.inputs[3].default_value = 0.004999995231628418
    # Count
    gem_in_holder_4.inputs[4].default_value = 6
    # Seed
    gem_in_holder_4.inputs[5].default_value = 41
    # Wings
    gem_in_holder_4.inputs[6].default_value = False
    # Array Count
    gem_in_holder_4.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_4.inputs[8].default_value = 10
    # Split
    gem_in_holder_4.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder_4.inputs[10].default_value = 3.3099989891052246
    # Links for gem_in_holder_4

    join_geometry_020 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_020.name = "Join Geometry.020"
    join_geometry_020.label = ""
    join_geometry_020.location = (4329.0, -735.80029296875)
    join_geometry_020.bl_label = "Join Geometry"
    # Links for join_geometry_020
    links.new(join_geometry_020.outputs[0], instance_on_points_008.inputs[2])
    links.new(gem_in_holder_4.outputs[3], join_geometry_020.inputs[0])

    gem_in_holder_5 = nodes.new("GeometryNodeGroup")
    gem_in_holder_5.name = "Gem in Holder.005"
    gem_in_holder_5.label = ""
    gem_in_holder_5.location = (3149.0, -595.80029296875)
    gem_in_holder_5.node_tree = create_gem_in__holder_group()
    gem_in_holder_5.bl_label = "Group"
    # Gem Radius
    gem_in_holder_5.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_5.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_5.inputs[2].default_value = False
    # Scale
    gem_in_holder_5.inputs[3].default_value = 0.004999995231628418
    # Count
    gem_in_holder_5.inputs[4].default_value = 6
    # Seed
    gem_in_holder_5.inputs[5].default_value = 41
    # Wings
    gem_in_holder_5.inputs[6].default_value = False
    # Array Count
    gem_in_holder_5.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_5.inputs[8].default_value = 10
    # Split
    gem_in_holder_5.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder_5.inputs[10].default_value = 5.109997272491455
    # Links for gem_in_holder_5

    transform_geometry_032 = nodes.new("GeometryNodeTransform")
    transform_geometry_032.name = "Transform Geometry.032"
    transform_geometry_032.label = ""
    transform_geometry_032.location = (3309.0, -675.80029296875)
    transform_geometry_032.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_032.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_032.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_032.inputs[3].default_value = Euler((0.0, 0.0, 0.01745329238474369), 'XYZ')
    # Scale
    transform_geometry_032.inputs[4].default_value = Vector((1.0, -1.0, 1.0))
    # Links for transform_geometry_032
    links.new(gem_in_holder_5.outputs[3], transform_geometry_032.inputs[0])

    join_geometry_021 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_021.name = "Join Geometry.021"
    join_geometry_021.label = ""
    join_geometry_021.location = (3309.0, -595.80029296875)
    join_geometry_021.bl_label = "Join Geometry"
    # Links for join_geometry_021
    links.new(join_geometry_021.outputs[0], join_geometry_020.inputs[0])
    links.new(gem_in_holder_5.outputs[3], join_geometry_021.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.name = "Flip Faces.001"
    flip_faces_001.label = ""
    flip_faces_001.location = (3309.0, -635.80029296875)
    flip_faces_001.bl_label = "Flip Faces"
    # Selection
    flip_faces_001.inputs[1].default_value = True
    # Links for flip_faces_001
    links.new(transform_geometry_032.outputs[0], flip_faces_001.inputs[0])
    links.new(flip_faces_001.outputs[0], join_geometry_021.inputs[0])

    gem_in_holder_6 = nodes.new("GeometryNodeGroup")
    gem_in_holder_6.name = "Gem in Holder.006"
    gem_in_holder_6.label = ""
    gem_in_holder_6.location = (3009.0, -775.80029296875)
    gem_in_holder_6.node_tree = create_gem_in__holder_group()
    gem_in_holder_6.bl_label = "Group"
    # Gem Radius
    gem_in_holder_6.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_6.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_6.inputs[2].default_value = False
    # Scale
    gem_in_holder_6.inputs[3].default_value = 0.004999995231628418
    # Count
    gem_in_holder_6.inputs[4].default_value = 6
    # Seed
    gem_in_holder_6.inputs[5].default_value = 41
    # Wings
    gem_in_holder_6.inputs[6].default_value = False
    # Array Count
    gem_in_holder_6.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_6.inputs[8].default_value = 6
    # Split
    gem_in_holder_6.inputs[9].default_value = 0.0010000000474974513
    # Seed
    gem_in_holder_6.inputs[10].default_value = 4.80999755859375
    # Links for gem_in_holder_6

    transform_geometry_033 = nodes.new("GeometryNodeTransform")
    transform_geometry_033.name = "Transform Geometry.033"
    transform_geometry_033.label = ""
    transform_geometry_033.location = (3169.0, -855.80029296875)
    transform_geometry_033.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_033.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_033.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_033.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_033.inputs[4].default_value = Vector((1.0, -1.0, 1.0))
    # Links for transform_geometry_033
    links.new(gem_in_holder_6.outputs[3], transform_geometry_033.inputs[0])

    join_geometry_022 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_022.name = "Join Geometry.022"
    join_geometry_022.label = ""
    join_geometry_022.location = (3329.0, -795.80029296875)
    join_geometry_022.bl_label = "Join Geometry"
    # Links for join_geometry_022
    links.new(gem_in_holder_6.outputs[3], join_geometry_022.inputs[0])

    flip_faces_004 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_004.name = "Flip Faces.004"
    flip_faces_004.label = ""
    flip_faces_004.location = (3329.0, -855.80029296875)
    flip_faces_004.bl_label = "Flip Faces"
    # Selection
    flip_faces_004.inputs[1].default_value = True
    # Links for flip_faces_004
    links.new(transform_geometry_033.outputs[0], flip_faces_004.inputs[0])
    links.new(flip_faces_004.outputs[0], join_geometry_022.inputs[0])

    transform_geometry_034 = nodes.new("GeometryNodeTransform")
    transform_geometry_034.name = "Transform Geometry.034"
    transform_geometry_034.label = ""
    transform_geometry_034.location = (3489.0, -795.80029296875)
    transform_geometry_034.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_034.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_034.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_034.inputs[3].default_value = Euler((0.0, -0.4363323152065277, 0.0), 'XYZ')
    # Scale
    transform_geometry_034.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_034
    links.new(transform_geometry_034.outputs[0], join_geometry_020.inputs[0])
    links.new(join_geometry_022.outputs[0], transform_geometry_034.inputs[0])

    join_geometry_017 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_017.name = "Join Geometry.017"
    join_geometry_017.label = ""
    join_geometry_017.location = (6009.0, -935.80029296875)
    join_geometry_017.bl_label = "Join Geometry"
    # Links for join_geometry_017

    store_named_attribute_008 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_008.name = "Store Named Attribute.008"
    store_named_attribute_008.label = ""
    store_named_attribute_008.location = (5789.0, -795.80029296875)
    store_named_attribute_008.bl_label = "Store Named Attribute"
    store_named_attribute_008.data_type = "BOOLEAN"
    store_named_attribute_008.domain = "POINT"
    # Selection
    store_named_attribute_008.inputs[1].default_value = True
    # Name
    store_named_attribute_008.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_008.inputs[3].default_value = True
    # Links for store_named_attribute_008
    links.new(join_geometry_016.outputs[0], store_named_attribute_008.inputs[0])
    links.new(store_named_attribute_008.outputs[0], join_geometry_017.inputs[0])

    store_named_attribute_009 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_009.name = "Store Named Attribute.009"
    store_named_attribute_009.label = ""
    store_named_attribute_009.location = (5789.0, -975.80029296875)
    store_named_attribute_009.bl_label = "Store Named Attribute"
    store_named_attribute_009.data_type = "BOOLEAN"
    store_named_attribute_009.domain = "POINT"
    # Selection
    store_named_attribute_009.inputs[1].default_value = True
    # Name
    store_named_attribute_009.inputs[2].default_value = "saphire"
    # Value
    store_named_attribute_009.inputs[3].default_value = True
    # Links for store_named_attribute_009
    links.new(merge_by_distance_001.outputs[0], store_named_attribute_009.inputs[0])
    links.new(store_named_attribute_009.outputs[0], join_geometry_017.inputs[0])

    gem_in_holder_7 = nodes.new("GeometryNodeGroup")
    gem_in_holder_7.name = "Gem in Holder.007"
    gem_in_holder_7.label = ""
    gem_in_holder_7.location = (389.0, -215.80029296875)
    gem_in_holder_7.node_tree = create_gem_in__holder_group()
    gem_in_holder_7.bl_label = "Group"
    # Gem Radius
    gem_in_holder_7.inputs[0].default_value = 0.006000000052154064
    # Gem Material
    gem_in_holder_7.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_7.inputs[2].default_value = False
    # Scale
    gem_in_holder_7.inputs[3].default_value = 0.004000000189989805
    # Count
    gem_in_holder_7.inputs[4].default_value = 6
    # Seed
    gem_in_holder_7.inputs[5].default_value = 41
    # Wings
    gem_in_holder_7.inputs[6].default_value = False
    # Array Count
    gem_in_holder_7.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_7.inputs[8].default_value = 3
    # Split
    gem_in_holder_7.inputs[9].default_value = 0.0010000000474974513
    # Seed
    gem_in_holder_7.inputs[10].default_value = 5.309997081756592
    # Links for gem_in_holder_7

    instance_on_points_009 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_009.name = "Instance on Points.009"
    instance_on_points_009.label = ""
    instance_on_points_009.location = (569.0, -155.80029296875)
    instance_on_points_009.bl_label = "Instance on Points"
    # Selection
    instance_on_points_009.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_009.inputs[3].default_value = False
    # Instance Index
    instance_on_points_009.inputs[4].default_value = 0
    # Rotation
    instance_on_points_009.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_009.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_009
    links.new(gem_in_holder_7.outputs[0], instance_on_points_009.inputs[2])
    links.new(instance_on_points_009.outputs[0], join_geometry_017.inputs[0])

    curve_circle_012 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_012.name = "Curve Circle.012"
    curve_circle_012.label = ""
    curve_circle_012.location = (29.0, -35.80029296875)
    curve_circle_012.bl_label = "Curve Circle"
    curve_circle_012.mode = "RADIUS"
    # Resolution
    curve_circle_012.inputs[0].default_value = 12
    # Point 1
    curve_circle_012.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_012.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_012.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_012.inputs[4].default_value = 0.05000000074505806
    # Links for curve_circle_012

    transform_geometry_035 = nodes.new("GeometryNodeTransform")
    transform_geometry_035.name = "Transform Geometry.035"
    transform_geometry_035.label = ""
    transform_geometry_035.location = (209.0, -35.80029296875)
    transform_geometry_035.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_035.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_035.inputs[2].default_value = Vector((0.0, 0.003000000026077032, 0.009999999776482582))
    # Rotation
    transform_geometry_035.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_035.inputs[4].default_value = Vector((1.4000000953674316, 0.8999999761581421, 1.0))
    # Links for transform_geometry_035
    links.new(transform_geometry_035.outputs[0], instance_on_points_009.inputs[0])
    links.new(curve_circle_012.outputs[0], transform_geometry_035.inputs[0])

    frame_025 = nodes.new("NodeFrame")
    frame_025.name = "Frame.025"
    frame_025.label = "Satalite Gems"
    frame_025.location = (5180.0, -1240.0)
    frame_025.bl_label = "Frame"
    frame_025.text = None
    frame_025.shrink = True
    frame_025.label_size = 20
    # Links for frame_025

    frame_026 = nodes.new("NodeFrame")
    frame_026.name = "Frame.026"
    frame_026.label = "Main Broach"
    frame_026.location = (991.0, 8155.80029296875)
    frame_026.bl_label = "Frame"
    frame_026.text = None
    frame_026.shrink = True
    frame_026.label_size = 20
    # Links for frame_026

    transform_geometry_036 = nodes.new("GeometryNodeTransform")
    transform_geometry_036.name = "Transform Geometry.036"
    transform_geometry_036.label = ""
    transform_geometry_036.location = (6189.0, -875.80029296875)
    transform_geometry_036.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_036.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_036.inputs[2].default_value = Vector((0.0, -0.12600000202655792, 0.36497700214385986))
    # Rotation
    transform_geometry_036.inputs[3].default_value = Euler((0.9428269863128662, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_036.inputs[4].default_value = Vector((0.4000000059604645, 0.4000000059604645, 0.4000000059604645))
    # Links for transform_geometry_036
    links.new(join_geometry_017.outputs[0], transform_geometry_036.inputs[0])

    instance_on_points_010 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_010.name = "Instance on Points.010"
    instance_on_points_010.label = ""
    instance_on_points_010.location = (749.0, -175.80029296875)
    instance_on_points_010.bl_label = "Instance on Points"
    # Selection
    instance_on_points_010.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_010.inputs[3].default_value = False
    # Instance Index
    instance_on_points_010.inputs[4].default_value = 0
    # Scale
    instance_on_points_010.inputs[6].default_value = Vector((0.6000000238418579, 0.6000000238418579, 0.6000000238418579))
    # Links for instance_on_points_010

    gem_in_holder_8 = nodes.new("GeometryNodeGroup")
    gem_in_holder_8.name = "Gem in Holder.008"
    gem_in_holder_8.label = ""
    gem_in_holder_8.location = (189.0, -175.80029296875)
    gem_in_holder_8.node_tree = create_gem_in__holder_group()
    gem_in_holder_8.bl_label = "Group"
    # Gem Radius
    gem_in_holder_8.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_8.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_8.inputs[2].default_value = True
    # Scale
    gem_in_holder_8.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_8.inputs[4].default_value = 20
    # Seed
    gem_in_holder_8.inputs[5].default_value = 10
    # Wings
    gem_in_holder_8.inputs[6].default_value = False
    # Array Count
    gem_in_holder_8.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_8.inputs[8].default_value = 10
    # Split
    gem_in_holder_8.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder_8.inputs[10].default_value = 2.5099997520446777
    # Links for gem_in_holder_8
    links.new(gem_in_holder_8.outputs[0], instance_on_points_010.inputs[2])

    realize_instances_005 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_005.name = "Realize Instances.005"
    realize_instances_005.label = ""
    realize_instances_005.location = (1109.0, -115.80029296875)
    realize_instances_005.bl_label = "Realize Instances"
    # Selection
    realize_instances_005.inputs[1].default_value = True
    # Realize All
    realize_instances_005.inputs[2].default_value = True
    # Depth
    realize_instances_005.inputs[3].default_value = 0
    # Links for realize_instances_005

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.name = "Capture Attribute.002"
    capture_attribute_002.label = ""
    capture_attribute_002.location = (929.0, -175.80029296875)
    capture_attribute_002.bl_label = "Capture Attribute"
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "INSTANCE"
    # Links for capture_attribute_002
    links.new(capture_attribute_002.outputs[0], realize_instances_005.inputs[0])
    links.new(instance_on_points_010.outputs[0], capture_attribute_002.inputs[0])

    index_002 = nodes.new("GeometryNodeInputIndex")
    index_002.name = "Index.002"
    index_002.label = ""
    index_002.location = (929.0, -295.80029296875)
    index_002.bl_label = "Index"
    # Links for index_002
    links.new(index_002.outputs[0], capture_attribute_002.inputs[1])

    resample_curve_008 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_008.name = "Resample Curve.008"
    resample_curve_008.label = ""
    resample_curve_008.location = (189.0, -35.80029296875)
    resample_curve_008.bl_label = "Resample Curve"
    resample_curve_008.keep_last_segment = True
    # Selection
    resample_curve_008.inputs[1].default_value = True
    # Mode
    resample_curve_008.inputs[2].default_value = "Count"
    # Count
    resample_curve_008.inputs[3].default_value = 10
    # Length
    resample_curve_008.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_008
    links.new(resample_curve_008.outputs[0], instance_on_points_010.inputs[0])

    align_rotation_to_vector_005 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_005.name = "Align Rotation to Vector.005"
    align_rotation_to_vector_005.label = ""
    align_rotation_to_vector_005.location = (369.0, -315.80029296875)
    align_rotation_to_vector_005.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_005.axis = "X"
    align_rotation_to_vector_005.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_005.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_005.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_005

    normal_004 = nodes.new("GeometryNodeInputNormal")
    normal_004.name = "Normal.004"
    normal_004.label = ""
    normal_004.location = (529.0, -475.80029296875)
    normal_004.bl_label = "Normal"
    normal_004.legacy_corner_normals = False
    # Links for normal_004

    align_rotation_to_vector_006 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_006.name = "Align Rotation to Vector.006"
    align_rotation_to_vector_006.label = ""
    align_rotation_to_vector_006.location = (529.0, -315.80029296875)
    align_rotation_to_vector_006.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_006.axis = "Y"
    align_rotation_to_vector_006.pivot_axis = "AUTO"
    # Factor
    align_rotation_to_vector_006.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_006
    links.new(align_rotation_to_vector_006.outputs[0], instance_on_points_010.inputs[5])
    links.new(align_rotation_to_vector_005.outputs[0], align_rotation_to_vector_006.inputs[0])
    links.new(normal_004.outputs[0], align_rotation_to_vector_006.inputs[2])

    curve_tangent_004 = nodes.new("GeometryNodeInputTangent")
    curve_tangent_004.name = "Curve Tangent.004"
    curve_tangent_004.label = ""
    curve_tangent_004.location = (369.0, -475.80029296875)
    curve_tangent_004.bl_label = "Curve Tangent"
    # Links for curve_tangent_004
    links.new(curve_tangent_004.outputs[0], align_rotation_to_vector_005.inputs[2])

    frame_027 = nodes.new("NodeFrame")
    frame_027.name = "Frame.027"
    frame_027.label = "Collar Gems"
    frame_027.location = (2489.0, -35.7998046875)
    frame_027.bl_label = "Frame"
    frame_027.text = None
    frame_027.shrink = True
    frame_027.label_size = 20
    # Links for frame_027

    trim_curve_006 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_006.name = "Trim Curve.006"
    trim_curve_006.label = ""
    trim_curve_006.location = (29.0, -35.80029296875)
    trim_curve_006.bl_label = "Trim Curve"
    trim_curve_006.mode = "FACTOR"
    # Selection
    trim_curve_006.inputs[1].default_value = True
    # Start
    trim_curve_006.inputs[2].default_value = 0.009999999776482582
    # End
    trim_curve_006.inputs[3].default_value = 0.940000057220459
    # Start
    trim_curve_006.inputs[4].default_value = 0.0
    # End
    trim_curve_006.inputs[5].default_value = 1.0
    # Links for trim_curve_006
    links.new(trim_curve_006.outputs[0], resample_curve_008.inputs[0])
    links.new(set_curve_tilt.outputs[0], trim_curve_006.inputs[0])

    gem_in_holder_9 = nodes.new("GeometryNodeGroup")
    gem_in_holder_9.name = "Gem in Holder.009"
    gem_in_holder_9.label = ""
    gem_in_holder_9.location = (1109.0, -155.80029296875)
    gem_in_holder_9.node_tree = create_gem_in__holder_group()
    gem_in_holder_9.bl_label = "Group"
    # Gem Radius
    gem_in_holder_9.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_9.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_9.inputs[2].default_value = False
    # Scale
    gem_in_holder_9.inputs[3].default_value = 0.004999999888241291
    # Wings
    gem_in_holder_9.inputs[6].default_value = True
    # Links for gem_in_holder_9

    curve_to_points_003 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_003.name = "Curve to Points.003"
    curve_to_points_003.label = ""
    curve_to_points_003.location = (189.0, -475.80029296875)
    curve_to_points_003.bl_label = "Curve to Points"
    curve_to_points_003.mode = "COUNT"
    # Count
    curve_to_points_003.inputs[1].default_value = 2
    # Length
    curve_to_points_003.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points_003

    for_each_geometry_element_input_002 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_002.name = "For Each Geometry Element Input.002"
    for_each_geometry_element_input_002.label = ""
    for_each_geometry_element_input_002.location = (409.0, -415.80029296875)
    for_each_geometry_element_input_002.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input_002.inputs[1].default_value = True
    # Links for for_each_geometry_element_input_002
    links.new(curve_to_points_003.outputs[0], for_each_geometry_element_input_002.inputs[0])
    links.new(curve_to_points_003.outputs[3], for_each_geometry_element_input_002.inputs[2])

    for_each_geometry_element_output_002 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_002.name = "For Each Geometry Element Output.002"
    for_each_geometry_element_output_002.label = ""
    for_each_geometry_element_output_002.location = (2029.0, -455.80029296875)
    for_each_geometry_element_output_002.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output_002.active_input_index = 1
    for_each_geometry_element_output_002.active_generation_index = 0
    for_each_geometry_element_output_002.active_main_index = 0
    for_each_geometry_element_output_002.domain = "POINT"
    for_each_geometry_element_output_002.inspection_index = 0
    # Links for for_each_geometry_element_output_002

    position_010 = nodes.new("GeometryNodeInputPosition")
    position_010.name = "Position.010"
    position_010.label = ""
    position_010.location = (189.0, -675.80029296875)
    position_010.bl_label = "Position"
    # Links for position_010
    links.new(position_010.outputs[0], for_each_geometry_element_input_002.inputs[3])

    transform_geometry_037 = nodes.new("GeometryNodeTransform")
    transform_geometry_037.name = "Transform Geometry.037"
    transform_geometry_037.label = ""
    transform_geometry_037.location = (1389.0, -475.80029296875)
    transform_geometry_037.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_037.inputs[1].default_value = "Components"
    # Links for transform_geometry_037
    links.new(gem_in_holder_9.outputs[0], transform_geometry_037.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[3], transform_geometry_037.inputs[2])

    rotate_rotation_007 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_007.name = "Rotate Rotation.007"
    rotate_rotation_007.label = ""
    rotate_rotation_007.location = (1049.0, -675.80029296875)
    rotate_rotation_007.bl_label = "Rotate Rotation"
    rotate_rotation_007.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_007.inputs[1].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')
    # Links for rotate_rotation_007
    links.new(for_each_geometry_element_input_002.outputs[2], rotate_rotation_007.inputs[0])

    random_value_014 = nodes.new("FunctionNodeRandomValue")
    random_value_014.name = "Random Value.014"
    random_value_014.label = ""
    random_value_014.location = (649.0, -395.80029296875)
    random_value_014.bl_label = "Random Value"
    random_value_014.data_type = "INT"
    # Min
    random_value_014.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_014.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_014.inputs[2].default_value = 0.0
    # Max
    random_value_014.inputs[3].default_value = 1.0
    # Min
    random_value_014.inputs[4].default_value = 5
    # Max
    random_value_014.inputs[5].default_value = 7
    # Probability
    random_value_014.inputs[6].default_value = 0.5
    # Seed
    random_value_014.inputs[8].default_value = 0
    # Links for random_value_014
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_014.inputs[7])
    links.new(random_value_014.outputs[2], gem_in_holder_9.inputs[7])

    transform_geometry_038 = nodes.new("GeometryNodeTransform")
    transform_geometry_038.name = "Transform Geometry.038"
    transform_geometry_038.label = ""
    transform_geometry_038.location = (1569.0, -475.80029296875)
    transform_geometry_038.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_038.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_038.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    # Rotation
    transform_geometry_038.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_038.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_038
    links.new(transform_geometry_037.outputs[0], transform_geometry_038.inputs[0])

    trim_curve_007 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_007.name = "Trim Curve.007"
    trim_curve_007.label = ""
    trim_curve_007.location = (29.0, -475.80029296875)
    trim_curve_007.bl_label = "Trim Curve"
    trim_curve_007.mode = "FACTOR"
    # Selection
    trim_curve_007.inputs[1].default_value = True
    # Start
    trim_curve_007.inputs[2].default_value = 0.4000000059604645
    # End
    trim_curve_007.inputs[3].default_value = 0.75
    # Start
    trim_curve_007.inputs[4].default_value = 0.0
    # End
    trim_curve_007.inputs[5].default_value = 1.0
    # Links for trim_curve_007
    links.new(trim_curve_007.outputs[0], curve_to_points_003.inputs[0])
    links.new(separate_geometry_002.outputs[0], trim_curve_007.inputs[0])

    random_value_015 = nodes.new("FunctionNodeRandomValue")
    random_value_015.name = "Random Value.015"
    random_value_015.label = ""
    random_value_015.location = (629.0, -615.80029296875)
    random_value_015.bl_label = "Random Value"
    random_value_015.data_type = "FLOAT"
    # Min
    random_value_015.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_015.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_015.inputs[2].default_value = 0.25
    # Max
    random_value_015.inputs[3].default_value = 0.550000011920929
    # Min
    random_value_015.inputs[4].default_value = 0
    # Max
    random_value_015.inputs[5].default_value = 100
    # Probability
    random_value_015.inputs[6].default_value = 0.5
    # Seed
    random_value_015.inputs[8].default_value = 0
    # Links for random_value_015
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_015.inputs[7])
    links.new(random_value_015.outputs[1], transform_geometry_037.inputs[4])

    store_named_attribute_010 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_010.name = "Store Named Attribute.010"
    store_named_attribute_010.label = ""
    store_named_attribute_010.location = (1809.0, -495.80029296875)
    store_named_attribute_010.bl_label = "Store Named Attribute"
    store_named_attribute_010.data_type = "BOOLEAN"
    store_named_attribute_010.domain = "POINT"
    # Selection
    store_named_attribute_010.inputs[1].default_value = True
    # Name
    store_named_attribute_010.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_010.inputs[3].default_value = True
    # Links for store_named_attribute_010
    links.new(store_named_attribute_010.outputs[0], for_each_geometry_element_output_002.inputs[1])
    links.new(transform_geometry_038.outputs[0], store_named_attribute_010.inputs[0])

    random_value_016 = nodes.new("FunctionNodeRandomValue")
    random_value_016.name = "Random Value.016"
    random_value_016.label = ""
    random_value_016.location = (649.0, -215.80029296875)
    random_value_016.bl_label = "Random Value"
    random_value_016.data_type = "FLOAT"
    # Min
    random_value_016.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_016.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_016.inputs[2].default_value = 0.0
    # Max
    random_value_016.inputs[3].default_value = 100.0
    # Min
    random_value_016.inputs[4].default_value = 3
    # Max
    random_value_016.inputs[5].default_value = 7
    # Probability
    random_value_016.inputs[6].default_value = 0.5
    # Seed
    random_value_016.inputs[8].default_value = 16
    # Links for random_value_016
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_016.inputs[7])
    links.new(random_value_016.outputs[1], gem_in_holder_9.inputs[10])

    rotate_rotation_008 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_008.name = "Rotate Rotation.008"
    rotate_rotation_008.label = ""
    rotate_rotation_008.location = (1209.0, -675.80029296875)
    rotate_rotation_008.bl_label = "Rotate Rotation"
    rotate_rotation_008.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_008.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
    # Links for rotate_rotation_008
    links.new(rotate_rotation_008.outputs[0], transform_geometry_037.inputs[3])
    links.new(rotate_rotation_007.outputs[0], rotate_rotation_008.inputs[0])

    random_value_017 = nodes.new("FunctionNodeRandomValue")
    random_value_017.name = "Random Value.017"
    random_value_017.label = ""
    random_value_017.location = (649.0, -35.80029296875)
    random_value_017.bl_label = "Random Value"
    random_value_017.data_type = "FLOAT"
    # Min
    random_value_017.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_017.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_017.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_017.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_017.inputs[4].default_value = 3
    # Max
    random_value_017.inputs[5].default_value = 7
    # Probability
    random_value_017.inputs[6].default_value = 0.5
    # Seed
    random_value_017.inputs[8].default_value = 0
    # Links for random_value_017
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_017.inputs[7])
    links.new(random_value_017.outputs[1], gem_in_holder_9.inputs[9])

    random_value_018 = nodes.new("FunctionNodeRandomValue")
    random_value_018.name = "Random Value.018"
    random_value_018.label = ""
    random_value_018.location = (889.0, -255.80029296875)
    random_value_018.bl_label = "Random Value"
    random_value_018.data_type = "INT"
    # Min
    random_value_018.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_018.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_018.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_018.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_018.inputs[4].default_value = 0
    # Max
    random_value_018.inputs[5].default_value = 100
    # Probability
    random_value_018.inputs[6].default_value = 0.5
    # Seed
    random_value_018.inputs[8].default_value = 0
    # Links for random_value_018
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_018.inputs[7])
    links.new(random_value_018.outputs[2], gem_in_holder_9.inputs[5])

    random_value_019 = nodes.new("FunctionNodeRandomValue")
    random_value_019.name = "Random Value.019"
    random_value_019.label = ""
    random_value_019.location = (889.0, -75.80029296875)
    random_value_019.bl_label = "Random Value"
    random_value_019.data_type = "INT"
    # Min
    random_value_019.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_019.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_019.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_019.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_019.inputs[4].default_value = 6
    # Max
    random_value_019.inputs[5].default_value = 20
    # Probability
    random_value_019.inputs[6].default_value = 0.5
    # Seed
    random_value_019.inputs[8].default_value = 0
    # Links for random_value_019
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_019.inputs[7])
    links.new(random_value_019.outputs[2], gem_in_holder_9.inputs[4])

    random_value_020 = nodes.new("FunctionNodeRandomValue")
    random_value_020.name = "Random Value.020"
    random_value_020.label = ""
    random_value_020.location = (889.0, -435.80029296875)
    random_value_020.bl_label = "Random Value"
    random_value_020.data_type = "INT"
    # Min
    random_value_020.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_020.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_020.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_020.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_020.inputs[4].default_value = 5
    # Max
    random_value_020.inputs[5].default_value = 30
    # Probability
    random_value_020.inputs[6].default_value = 0.5
    # Seed
    random_value_020.inputs[8].default_value = 0
    # Links for random_value_020
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_020.inputs[7])
    links.new(random_value_020.outputs[2], gem_in_holder_9.inputs[8])

    frame_028 = nodes.new("NodeFrame")
    frame_028.name = "Frame.028"
    frame_028.label = "Broaches"
    frame_028.location = (3029.0, -915.7998046875)
    frame_028.bl_label = "Frame"
    frame_028.text = None
    frame_028.shrink = True
    frame_028.label_size = 20
    # Links for frame_028

    store_named_attribute_011 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_011.name = "Store Named Attribute.011"
    store_named_attribute_011.label = ""
    store_named_attribute_011.location = (6369.0, -875.80029296875)
    store_named_attribute_011.bl_label = "Store Named Attribute"
    store_named_attribute_011.data_type = "BOOLEAN"
    store_named_attribute_011.domain = "POINT"
    # Selection
    store_named_attribute_011.inputs[1].default_value = True
    # Name
    store_named_attribute_011.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_011.inputs[3].default_value = True
    # Links for store_named_attribute_011
    links.new(store_named_attribute_011.outputs[0], join_geometry_002.inputs[0])
    links.new(transform_geometry_036.outputs[0], store_named_attribute_011.inputs[0])

    store_named_attribute_012 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_012.name = "Store Named Attribute.012"
    store_named_attribute_012.label = ""
    store_named_attribute_012.location = (2189.0, -455.80029296875)
    store_named_attribute_012.bl_label = "Store Named Attribute"
    store_named_attribute_012.data_type = "BOOLEAN"
    store_named_attribute_012.domain = "POINT"
    # Selection
    store_named_attribute_012.inputs[1].default_value = True
    # Name
    store_named_attribute_012.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_012.inputs[3].default_value = True
    # Links for store_named_attribute_012
    links.new(store_named_attribute_012.outputs[0], join_geometry_002.inputs[0])
    links.new(for_each_geometry_element_output_002.outputs[2], store_named_attribute_012.inputs[0])

    mesh_boolean_002 = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean_002.name = "Mesh Boolean.002"
    mesh_boolean_002.label = ""
    mesh_boolean_002.location = (1329.0, -49.0)
    mesh_boolean_002.bl_label = "Mesh Boolean"
    mesh_boolean_002.operation = "DIFFERENCE"
    mesh_boolean_002.solver = "FLOAT"
    # Self Intersection
    mesh_boolean_002.inputs[2].default_value = False
    # Hole Tolerant
    mesh_boolean_002.inputs[3].default_value = False
    # Links for mesh_boolean_002
    links.new(mesh_boolean_002.outputs[0], join_geometry_002.inputs[0])
    links.new(gold_decorations_2.outputs[0], mesh_boolean_002.inputs[0])

    ico_sphere_007 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_007.name = "Ico Sphere.007"
    ico_sphere_007.label = ""
    ico_sphere_007.location = (1029.0, -209.0)
    ico_sphere_007.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_007.inputs[0].default_value = 0.07800000160932541
    # Subdivisions
    ico_sphere_007.inputs[1].default_value = 3
    # Links for ico_sphere_007

    transform_geometry_039 = nodes.new("GeometryNodeTransform")
    transform_geometry_039.name = "Transform Geometry.039"
    transform_geometry_039.label = ""
    transform_geometry_039.location = (1189.0, -209.0)
    transform_geometry_039.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_039.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_039.inputs[2].default_value = Vector((0.0, -0.019999999552965164, 0.47999998927116394))
    # Rotation
    transform_geometry_039.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_039.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_039
    links.new(transform_geometry_039.outputs[0], mesh_boolean_002.inputs[1])
    links.new(ico_sphere_007.outputs[0], transform_geometry_039.inputs[0])

    store_named_attribute_013 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_013.name = "Store Named Attribute.013"
    store_named_attribute_013.label = ""
    store_named_attribute_013.location = (1449.0, -135.80029296875)
    store_named_attribute_013.bl_label = "Store Named Attribute"
    store_named_attribute_013.data_type = "BOOLEAN"
    store_named_attribute_013.domain = "POINT"
    # Name
    store_named_attribute_013.inputs[2].default_value = "saphire"
    # Value
    store_named_attribute_013.inputs[3].default_value = True
    # Links for store_named_attribute_013
    links.new(realize_instances_005.outputs[0], store_named_attribute_013.inputs[0])

    boolean_math_005 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.name = "Boolean Math.005"
    boolean_math_005.label = ""
    boolean_math_005.location = (1289.0, -255.80029296875)
    boolean_math_005.bl_label = "Boolean Math"
    boolean_math_005.operation = "AND"
    # Links for boolean_math_005
    links.new(boolean_math_005.outputs[0], store_named_attribute_013.inputs[1])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (1109.0, -415.80029296875)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "BOOLEAN"
    # Name
    named_attribute.inputs[0].default_value = "ruby"
    # Links for named_attribute
    links.new(named_attribute.outputs[0], boolean_math_005.inputs[1])

    store_named_attribute_014 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_014.name = "Store Named Attribute.014"
    store_named_attribute_014.label = ""
    store_named_attribute_014.location = (1609.0, -135.80029296875)
    store_named_attribute_014.bl_label = "Store Named Attribute"
    store_named_attribute_014.data_type = "BOOLEAN"
    store_named_attribute_014.domain = "POINT"
    # Name
    store_named_attribute_014.inputs[2].default_value = "ruby"
    # Value
    store_named_attribute_014.inputs[3].default_value = False
    # Links for store_named_attribute_014
    links.new(store_named_attribute_013.outputs[0], store_named_attribute_014.inputs[0])
    links.new(boolean_math_005.outputs[0], store_named_attribute_014.inputs[1])
    links.new(store_named_attribute_014.outputs[0], join_geometry_002.inputs[0])

    math_017 = nodes.new("ShaderNodeMath")
    math_017.name = "Math.017"
    math_017.label = ""
    math_017.location = (1109.0, -255.80029296875)
    math_017.bl_label = "Math"
    math_017.operation = "FLOORED_MODULO"
    math_017.use_clamp = False
    # Value
    math_017.inputs[1].default_value = 2.0
    # Value
    math_017.inputs[2].default_value = 0.5
    # Links for math_017
    links.new(math_017.outputs[0], boolean_math_005.inputs[0])
    links.new(capture_attribute_002.outputs[1], math_017.inputs[0])

    transform_geometry_040 = nodes.new("GeometryNodeTransform")
    transform_geometry_040.name = "Transform Geometry.040"
    transform_geometry_040.label = ""
    transform_geometry_040.location = (1209.0, -35.7998046875)
    transform_geometry_040.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_040.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_040.inputs[2].default_value = Vector((0.0, 0.0, 0.0007999999797903001))
    # Rotation
    transform_geometry_040.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_040.inputs[4].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))
    # Links for transform_geometry_040
    links.new(set_position_004.outputs[0], transform_geometry_040.inputs[0])
    links.new(transform_geometry_040.outputs[0], join_geometry_009.inputs[0])

    transform_geometry_041 = nodes.new("GeometryNodeTransform")
    transform_geometry_041.name = "Transform Geometry.041"
    transform_geometry_041.label = ""
    transform_geometry_041.location = (1409.0, -35.7998046875)
    transform_geometry_041.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_041.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_041.inputs[2].default_value = Vector((0.0, 0.0, 0.0007999999797903001))
    # Rotation
    transform_geometry_041.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_041.inputs[4].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))
    # Links for transform_geometry_041
    links.new(transform_geometry_040.outputs[0], transform_geometry_041.inputs[0])
    links.new(transform_geometry_041.outputs[0], join_geometry_009.inputs[0])

    scale_elements = nodes.new("GeometryNodeScaleElements")
    scale_elements.name = "Scale Elements"
    scale_elements.label = ""
    scale_elements.location = (2509.0, -155.7998046875)
    scale_elements.bl_label = "Scale Elements"
    scale_elements.domain = "FACE"
    # Selection
    scale_elements.inputs[1].default_value = True
    # Scale
    scale_elements.inputs[2].default_value = 1.2000000476837158
    # Center
    scale_elements.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Scale Mode
    scale_elements.inputs[4].default_value = "Uniform"
    # Axis
    scale_elements.inputs[5].default_value = [1.0, 0.0, 0.0]
    # Links for scale_elements
    links.new(join_geometry_007.outputs[0], scale_elements.inputs[0])

    transform_geometry_042 = nodes.new("GeometryNodeTransform")
    transform_geometry_042.name = "Transform Geometry.042"
    transform_geometry_042.label = ""
    transform_geometry_042.location = (2669.0, -155.7998046875)
    transform_geometry_042.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_042.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_042.inputs[2].default_value = Vector((0.0, 0.0, 0.0005000000237487257))
    # Rotation
    transform_geometry_042.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_042.inputs[4].default_value = Vector((1.0, 1.0, 0.7000000476837158))
    # Links for transform_geometry_042
    links.new(scale_elements.outputs[0], transform_geometry_042.inputs[0])

    join_geometry_023 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_023.name = "Join Geometry.023"
    join_geometry_023.label = ""
    join_geometry_023.location = (2669.0, -115.7998046875)
    join_geometry_023.bl_label = "Join Geometry"
    # Links for join_geometry_023
    links.new(join_geometry_023.outputs[0], store_named_attribute_006.inputs[0])
    links.new(join_geometry_009.outputs[0], join_geometry_023.inputs[0])
    links.new(transform_geometry_042.outputs[0], join_geometry_023.inputs[0])

    transform_geometry_043 = nodes.new("GeometryNodeTransform")
    transform_geometry_043.name = "Transform Geometry.043"
    transform_geometry_043.label = ""
    transform_geometry_043.location = (2669.0, -495.7998046875)
    transform_geometry_043.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_043.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_043.inputs[2].default_value = Vector((0.0, 0.0, 0.0005000000237487257))
    # Rotation
    transform_geometry_043.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_043.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_043
    links.new(transform_geometry_043.outputs[0], store_named_attribute_005.inputs[0])
    links.new(join_geometry_007.outputs[0], transform_geometry_043.inputs[0])

    # Parent assignments
    quadratic_bézier_003.parent = frame_006
    bi-_rail_loft.parent = frame_010
    quadratic_bézier_004.parent = frame_006
    join_splines.parent = frame_006
    join_geometry_005.parent = frame_006
    vector.parent = frame_006
    frame_006.parent = frame_008
    quadratic_bézier_006.parent = frame_007
    quadratic_bézier_007.parent = frame_007
    join_splines_1.parent = frame_007
    join_geometry_006.parent = frame_007
    vector_001.parent = frame_007
    frame_007.parent = frame_008
    join_geometry_008.parent = frame_008
    transform_geometry_002.parent = frame_009
    transform_geometry_003.parent = frame_009
    curve_circle.parent = frame_009
    curve_circle_001.parent = frame_009
    set_position.parent = frame_009
    position.parent = frame_009
    separate_x_y_z.parent = frame_009
    map_range.parent = frame_009
    frame_008.parent = frame_010
    float_curve_001.parent = frame_009
    combine_x_y_z.parent = frame_009
    transform_geometry_004.parent = frame_009
    transform_geometry_005.parent = frame_009
    closure_input_001.parent = frame_010
    closure_output_001.parent = frame_010
    math.parent = frame_010
    math_001.parent = frame_010
    transform_geometry_001.parent = frame_007
    transform_geometry_006.parent = frame_006
    integer.parent = frame_009
    frame_009.parent = frame_010
    pipes.parent = frame
    separate_x_y_z_002.parent = frame
    compare_001.parent = frame
    separate_geometry.parent = frame
    join_geometry_001.parent = frame
    join_geometry_002.parent = frame_011
    switch.parent = frame_011
    group_input.parent = frame_011
    set_spline_cyclic.parent = frame_011
    trim_curve.parent = frame_005
    resample_curve_001.parent = frame_005
    gold_decorations.parent = frame_005
    set_curve_normal.parent = frame_005
    sample_nearest_surface.parent = frame_011
    normal.parent = frame_011
    vector_math.parent = frame_005
    curve_tangent.parent = frame_005
    frame_005.parent = frame_011
    gold_on_band.parent = frame_001
    gem_in_holder.parent = frame_012
    curve_to_points.parent = frame_012
    for_each_geometry_element_input.parent = frame_012
    for_each_geometry_element_output.parent = frame_012
    position_002.parent = frame_012
    transform_geometry_007.parent = frame_012
    rotate_rotation.parent = frame_012
    random_value.parent = frame_012
    transform_geometry_008.parent = frame_012
    random_value_001.parent = frame_012
    store_named_attribute_001.parent = frame_014
    random_value_002.parent = frame_012
    rotate_rotation_001.parent = frame_012
    random_value_003.parent = frame_012
    random_value_004.parent = frame_012
    random_value_005.parent = frame_012
    random_value_006.parent = frame_012
    frame_012.parent = frame_011
    separate_geometry_001.parent = frame_001
    separate_x_y_z_003.parent = frame_001
    compare_002.parent = frame_001
    trim_curve_001.parent = frame_012
    set_curve_normal_001.parent = frame_012
    compare_003.parent = frame_001
    boolean_math.parent = frame_001
    boolean_math_001.parent = frame_001
    compare_004.parent = frame_001
    frame_001.parent = frame_011
    boolean_math_002.parent = frame_001
    compare_005.parent = frame_001
    gem_in_holder_1.parent = frame_014
    mesh_to_curve_002.parent = frame_014
    is_edge_boundary.parent = frame_014
    set_spline_cyclic_001.parent = frame_014
    trim_curve_004.parent = frame_014
    curve_to_points_001.parent = frame_014
    set_curve_normal_002.parent = frame_014
    position_004.parent = frame_014
    for_each_geometry_element_input_001.parent = frame_014
    for_each_geometry_element_output_001.parent = frame_014
    transform_geometry_009.parent = frame_014
    rotate_rotation_002.parent = frame_014
    frame_014.parent = frame_011
    random_value_007.parent = frame_014
    random_value_008.parent = frame_014
    distribute_points_on_faces.parent = frame_015
    instance_on_points.parent = frame_015
    ico_sphere.parent = frame_015
    store_named_attribute_002.parent = frame_015
    random_value_009.parent = frame_015
    boolean_math_003.parent = frame_015
    store_named_attribute_003.parent = frame_015
    realize_instances_001.parent = frame_015
    set_shade_smooth_003.parent = frame_015
    frame_015.parent = frame_011
    reroute_001.parent = frame_016
    distribute_points_on_faces_001.parent = frame_016
    geometry_proximity.parent = frame_016
    compare_006.parent = frame_016
    gem_in_holder_2.parent = frame_016
    instance_on_points_001.parent = frame_016
    random_value_010.parent = frame_016
    frame_016.parent = frame_011
    realize_instances_002.parent = frame_016
    transform_geometry_010.parent = frame_016
    swap_attr.parent = frame_016
    capture_attribute_001.parent = frame_016
    index.parent = frame_016
    set_position_001.parent = frame_014
    geometry_proximity_001.parent = frame_014
    curve_to_mesh.parent = frame_014
    separate_geometry_002.parent = frame_013
    compare_007.parent = frame_013
    separate_x_y_z_004.parent = frame_013
    trim_curve_002.parent = frame_013
    resample_curve_002.parent = frame_013
    gold_decorations_1.parent = frame_013
    set_curve_normal_003.parent = frame_013
    frame_013.parent = frame_011
    transform_geometry.parent = frame_013
    random_value_011.parent = frame_015
    trim_curve_003.parent = frame_017
    resample_curve_003.parent = frame_017
    gold_decorations_2.parent = frame_017
    set_curve_normal_004.parent = frame_017
    frame_017.parent = frame_011
    transform_geometry_011.parent = frame_017
    mesh_to_curve.parent = frame_017
    set_curve_tilt.parent = frame_017
    reroute_002.parent = frame_011
    curve_circle_002.parent = frame_018
    transform_geometry_012.parent = frame_018
    set_position_002.parent = frame_018
    position_003.parent = frame_018
    separate_x_y_z_005.parent = frame_018
    map_range_001.parent = frame_018
    float_curve.parent = frame_018
    math_002.parent = frame_018
    combine_x_y_z_001.parent = frame_018
    position_005.parent = frame_018
    vector_math_001.parent = frame_018
    combine_x_y_z_002.parent = frame_018
    float_curve_002.parent = frame_018
    store_named_attribute.parent = frame_024
    resample_curve.parent = frame_018
    instance_on_points_002.parent = frame_018
    align_rotation_to_vector.parent = frame_003
    curve_tangent_001.parent = frame_003
    align_rotation_to_vector_001.parent = frame_003
    normal_001.parent = frame_003
    rotate_rotation_003.parent = frame_003
    spline_parameter.parent = frame_018
    math_003.parent = frame_018
    math_004.parent = frame_018
    set_curve_tilt_002.parent = frame_018
    map_range_002.parent = frame_018
    float_curve_003.parent = frame_018
    spline_parameter_001.parent = frame_018
    math_005.parent = frame_018
    curve_circle_003.parent = frame_002
    instance_on_points_003.parent = frame_002
    ico_sphere_001.parent = frame_002
    cylinder_001.parent = frame_002
    join_geometry_003.parent = frame_002
    ico_sphere_002.parent = frame_002
    transform_geometry_013.parent = frame_002
    set_position_003.parent = frame_002
    vector_math_002.parent = frame_002
    noise_texture.parent = frame_002
    transform_geometry_014.parent = frame_002
    frame_002.parent = frame_018
    rotate_rotation_004.parent = frame_003
    ico_sphere_003.parent = frame_002
    frame_003.parent = frame_018
    store_named_attribute_004.parent = frame_002
    cylinder_002.parent = frame_004
    math_006.parent = frame_018
    spline_parameter_002.parent = frame_018
    float_curve_004.parent = frame_018
    set_position_004.parent = frame_004
    position_006.parent = frame_004
    separate_x_y_z_006.parent = frame_004
    math_007.parent = frame_004
    combine_x_y_z_003.parent = frame_004
    map_range_003.parent = frame_004
    math_008.parent = frame_004
    boolean_math_004.parent = frame_004
    mesh_to_curve_001.parent = frame_004
    ico_sphere_004.parent = frame_004
    instance_on_points_004.parent = frame_004
    transform_geometry_015.parent = frame_004
    ico_sphere_005.parent = frame_004
    dual_mesh.parent = frame_004
    join_geometry_007.parent = frame_004
    transform_geometry_016.parent = frame_004
    transform_geometry_017.parent = frame_004
    transform_geometry_018.parent = frame_004
    transform_geometry_019.parent = frame_004
    join_geometry_009.parent = frame_004
    store_named_attribute_005.parent = frame_004
    join_geometry_010.parent = frame_004
    store_named_attribute_006.parent = frame_004
    frame_004.parent = frame_018
    sample_curve.parent = frame_018
    transform_geometry_020.parent = frame_018
    join_geometry_011.parent = frame_018
    vector_math_003.parent = frame_018
    float_curve_005.parent = frame_018
    spline_parameter_003.parent = frame_018
    math_009.parent = frame_018
    math_010.parent = frame_018
    frame_018.parent = frame_024
    curve_circle_004.parent = frame_022
    transform_geometry_021.parent = frame_022
    set_position_005.parent = frame_022
    position_007.parent = frame_022
    separate_x_y_z_007.parent = frame_022
    map_range_004.parent = frame_022
    float_curve_006.parent = frame_022
    math_011.parent = frame_022
    combine_x_y_z_004.parent = frame_022
    position_008.parent = frame_022
    vector_math_004.parent = frame_022
    combine_x_y_z_005.parent = frame_022
    float_curve_007.parent = frame_022
    resample_curve_004.parent = frame_022
    instance_on_points_005.parent = frame_022
    align_rotation_to_vector_002.parent = frame_020
    curve_tangent_002.parent = frame_020
    align_rotation_to_vector_003.parent = frame_020
    normal_002.parent = frame_020
    spline_parameter_004.parent = frame_022
    math_012.parent = frame_022
    math_013.parent = frame_022
    set_curve_tilt_003.parent = frame_022
    map_range_005.parent = frame_022
    float_curve_008.parent = frame_022
    spline_parameter_005.parent = frame_022
    math_014.parent = frame_022
    frame_020.parent = frame_022
    math_015.parent = frame_022
    spline_parameter_006.parent = frame_022
    float_curve_009.parent = frame_022
    float_curve_010.parent = frame_022
    spline_parameter_007.parent = frame_022
    math_018.parent = frame_022
    math_019.parent = frame_022
    frame_022.parent = frame_024
    quadrilateral.parent = frame_019
    fillet_curve.parent = frame_019
    set_spline_type.parent = frame_019
    curve_to_mesh_001.parent = frame_019
    curve_circle_005.parent = frame_019
    frame_019.parent = frame_022
    rotate_rotation_006.parent = frame_020
    rotate_rotation_005.parent = frame_020
    random_value_012.parent = frame_020
    index_001.parent = frame_020
    math_016.parent = frame_020
    switch_001.parent = frame_020
    combine_x_y_z_006.parent = frame_020
    join_geometry_012.parent = frame_024
    curve_circle_006.parent = frame_021
    curve_to_mesh_002.parent = frame_021
    sample_curve_001.parent = frame_022
    transform_geometry_022.parent = frame_022
    join_geometry_013.parent = frame_022
    vector_math_005.parent = frame_022
    curve_circle_007.parent = frame_021
    curve_line.parent = frame_023
    transform_geometry_023.parent = frame_022
    frame_021.parent = frame_022
    vector_math_006.parent = frame_022
    curve_to_mesh_003.parent = frame_023
    resample_curve_005.parent = frame_023
    curve_circle_008.parent = frame_023
    spline_parameter_008.parent = frame_023
    float_curve_011.parent = frame_023
    curve_circle_009.parent = frame_023
    curve_to_mesh_004.parent = frame_023
    curve_circle_010.parent = frame_023
    join_geometry_014.parent = frame_023
    curve_circle_011.parent = frame_023
    instance_on_points_006.parent = frame_023
    transform_geometry_024.parent = frame_023
    grid.parent = frame_023
    delete_geometry_001.parent = frame_023
    random_value_013.parent = frame_023
    extrude_mesh.parent = frame_023
    flip_faces.parent = frame_023
    join_geometry_015.parent = frame_023
    merge_by_distance.parent = frame_023
    transform_geometry_025.parent = frame_023
    subdivision_surface.parent = frame_023
    set_shade_smooth_001.parent = frame_022
    frame_023.parent = frame_022
    store_named_attribute_007.parent = frame_022
    ico_sphere_006.parent = frame_026
    transform_geometry_026.parent = frame_026
    instance_on_points_007.parent = frame_026
    quadratic_bézier.parent = frame_026
    realize_instances_003.parent = frame_026
    mesh_to_s_d_f_grid.parent = frame_026
    grid_to_mesh.parent = frame_026
    dual_mesh_001.parent = frame_026
    triangulate.parent = frame_026
    s_d_f_grid_boolean.parent = frame_026
    cube.parent = frame_026
    mesh_to_s_d_f_grid_001.parent = frame_026
    transform_geometry_027.parent = frame_026
    mesh_boolean.parent = frame_026
    cube_001.parent = frame_026
    transform_geometry_028.parent = frame_026
    delete_geometry_002.parent = frame_026
    mesh_boolean_001.parent = frame_026
    cube_002.parent = frame_026
    transform_geometry_029.parent = frame_026
    join_geometry_016.parent = frame_026
    delete_geometry_003.parent = frame_026
    normal_003.parent = frame_026
    compare_008.parent = frame_026
    mesh_to_curve_003.parent = frame_026
    resample_curve_006.parent = frame_026
    set_spline_cyclic_002.parent = frame_026
    curve_to_mesh_005.parent = frame_026
    gem_in_holder_3.parent = frame_026
    trim_curve_005.parent = frame_026
    instance_on_points_008.parent = frame_026
    resample_curve_007.parent = frame_026
    align_rotation_to_vector_004.parent = frame_026
    curve_tangent_003.parent = frame_026
    realize_instances_004.parent = frame_026
    transform_geometry_030.parent = frame_026
    flip_faces_002.parent = frame_026
    join_geometry_018.parent = frame_026
    merge_by_distance_001.parent = frame_026
    is_edge_boundary_1.parent = frame_026
    spline_parameter_009.parent = frame_026
    math_020.parent = frame_026
    math_021.parent = frame_026
    curve_to_points_002.parent = frame_026
    points_to_curves.parent = frame_026
    gradient_texture.parent = frame_026
    math_022.parent = frame_026
    math_023.parent = frame_026
    delete_geometry_004.parent = frame_026
    position_009.parent = frame_026
    separate_x_y_z_008.parent = frame_026
    compare_009.parent = frame_026
    float_curve_012.parent = frame_026
    transform_geometry_031.parent = frame_026
    flip_faces_003.parent = frame_026
    join_geometry_019.parent = frame_026
    gem_in_holder_4.parent = frame_026
    join_geometry_020.parent = frame_026
    gem_in_holder_5.parent = frame_026
    transform_geometry_032.parent = frame_026
    join_geometry_021.parent = frame_026
    flip_faces_001.parent = frame_026
    gem_in_holder_6.parent = frame_026
    transform_geometry_033.parent = frame_026
    join_geometry_022.parent = frame_026
    flip_faces_004.parent = frame_026
    transform_geometry_034.parent = frame_026
    join_geometry_017.parent = frame_026
    store_named_attribute_008.parent = frame_026
    store_named_attribute_009.parent = frame_026
    gem_in_holder_7.parent = frame_025
    instance_on_points_009.parent = frame_025
    curve_circle_012.parent = frame_025
    transform_geometry_035.parent = frame_025
    frame_025.parent = frame_026
    transform_geometry_036.parent = frame_026
    instance_on_points_010.parent = frame_027
    gem_in_holder_8.parent = frame_027
    realize_instances_005.parent = frame_027
    capture_attribute_002.parent = frame_027
    index_002.parent = frame_027
    resample_curve_008.parent = frame_027
    align_rotation_to_vector_005.parent = frame_027
    normal_004.parent = frame_027
    align_rotation_to_vector_006.parent = frame_027
    curve_tangent_004.parent = frame_027
    frame_027.parent = frame_011
    trim_curve_006.parent = frame_027
    gem_in_holder_9.parent = frame_028
    curve_to_points_003.parent = frame_028
    for_each_geometry_element_input_002.parent = frame_028
    for_each_geometry_element_output_002.parent = frame_028
    position_010.parent = frame_028
    transform_geometry_037.parent = frame_028
    rotate_rotation_007.parent = frame_028
    random_value_014.parent = frame_028
    transform_geometry_038.parent = frame_028
    trim_curve_007.parent = frame_028
    random_value_015.parent = frame_028
    store_named_attribute_010.parent = frame_028
    random_value_016.parent = frame_028
    rotate_rotation_008.parent = frame_028
    random_value_017.parent = frame_028
    random_value_018.parent = frame_028
    random_value_019.parent = frame_028
    random_value_020.parent = frame_028
    frame_028.parent = frame_011
    store_named_attribute_011.parent = frame_026
    store_named_attribute_012.parent = frame_028
    mesh_boolean_002.parent = frame_017
    ico_sphere_007.parent = frame_017
    transform_geometry_039.parent = frame_017
    store_named_attribute_013.parent = frame_027
    boolean_math_005.parent = frame_027
    named_attribute.parent = frame_027
    store_named_attribute_014.parent = frame_027
    math_017.parent = frame_027
    transform_geometry_040.parent = frame_004
    transform_geometry_041.parent = frame_004
    scale_elements.parent = frame_004
    transform_geometry_042.parent = frame_004
    join_geometry_023.parent = frame_004
    transform_geometry_043.parent = frame_004

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_chest_group():
    group_name = "Chest"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (8900.0, -160.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    bi-_rail_loft = nodes.new("GeometryNodeGroup")
    bi-_rail_loft.name = "Bi-Rail Loft"
    bi-_rail_loft.label = ""
    bi-_rail_loft.location = (-1860.0, -400.0)
    bi-_rail_loft.node_tree = create_bi-_rail__loft_group()
    bi-_rail_loft.bl_label = "Group"
    # Smoothing
    bi-_rail_loft.inputs[3].default_value = 6
    # Menu
    bi-_rail_loft.inputs[4].default_value = "Resolution"
    # X Spacing
    bi-_rail_loft.inputs[5].default_value = 0.009999999776482582
    # Y Spacing
    bi-_rail_loft.inputs[6].default_value = 0.029999999329447746
    # X Resolution
    bi-_rail_loft.inputs[7].default_value = 14
    # Y Resolution
    bi-_rail_loft.inputs[8].default_value = 102
    # Links for bi-_rail_loft

    bézier_segment = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment.name = "Bézier Segment"
    bézier_segment.label = ""
    bézier_segment.location = (29.0, -35.800018310546875)
    bézier_segment.bl_label = "Bézier Segment"
    bézier_segment.mode = "POSITION"
    # Resolution
    bézier_segment.inputs[0].default_value = 200
    # Start
    bézier_segment.inputs[1].default_value = Vector((0.0, -0.14000000059604645, 0.07000000029802322))
    # Start Handle
    bézier_segment.inputs[2].default_value = Vector((0.0, -0.20000000298023224, 0.2800000011920929))
    # End Handle
    bézier_segment.inputs[3].default_value = Vector((0.0, -0.1600000113248825, 0.3100000023841858))
    # End
    bézier_segment.inputs[4].default_value = Vector((0.0, -0.08999998867511749, 0.4099999964237213))
    # Links for bézier_segment

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Centre Line"
    frame.location = (29.0, -35.800018310546875)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    bézier_segment_001 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_001.name = "Bézier Segment.001"
    bézier_segment_001.label = ""
    bézier_segment_001.location = (29.0, -35.79999542236328)
    bézier_segment_001.bl_label = "Bézier Segment"
    bézier_segment_001.mode = "OFFSET"
    # Resolution
    bézier_segment_001.inputs[0].default_value = 200
    # Start
    bézier_segment_001.inputs[1].default_value = Vector((-0.14999999105930328, 0.0, 0.07000000029802322))
    # Start Handle
    bézier_segment_001.inputs[2].default_value = Vector((-0.019999999552965164, 0.0, 0.05999999865889549))
    # End Handle
    bézier_segment_001.inputs[3].default_value = Vector((0.0, 0.0, -0.029999999329447746))
    # End
    bézier_segment_001.inputs[4].default_value = Vector((-0.17000000178813934, 0.0, 0.1899999976158142))
    # Links for bézier_segment_001

    bézier_segment_002 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_002.name = "Bézier Segment.002"
    bézier_segment_002.label = ""
    bézier_segment_002.location = (209.0, -95.79999542236328)
    bézier_segment_002.bl_label = "Bézier Segment"
    bézier_segment_002.mode = "OFFSET"
    # Resolution
    bézier_segment_002.inputs[0].default_value = 200
    # Start
    bézier_segment_002.inputs[1].default_value = Vector((-0.17000000178813934, 0.0, 0.1899999976158142))
    # Start Handle
    bézier_segment_002.inputs[2].default_value = Vector((0.05000000074505806, -0.20999999344348907, 0.030000001192092896))
    # End Handle
    bézier_segment_002.inputs[3].default_value = Vector((0.019999999552965164, -0.029999999329447746, -0.029999999329447746))
    # End
    bézier_segment_002.inputs[4].default_value = Vector((-0.11999998986721039, -0.06000000238418579, 0.4000000059604645))
    # Links for bézier_segment_002

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (589.0, -75.79999542236328)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(bézier_segment_002.outputs[0], join_geometry.inputs[0])
    links.new(bézier_segment_001.outputs[0], join_geometry.inputs[0])

    join_splines = nodes.new("GeometryNodeGroup")
    join_splines.name = "Group"
    join_splines.label = ""
    join_splines.location = (769.0, -55.79999542236328)
    join_splines.node_tree = create_join__splines_group()
    join_splines.bl_label = "Group"
    # Links for join_splines
    links.new(join_splines.outputs[0], bi-_rail_loft.inputs[1])
    links.new(join_geometry.outputs[0], join_splines.inputs[0])

    join_splines_1 = nodes.new("GeometryNodeGroup")
    join_splines_1.name = "Group.001"
    join_splines_1.label = ""
    join_splines_1.location = (618.0, -131.60003662109375)
    join_splines_1.node_tree = create_join__splines_group()
    join_splines_1.bl_label = "Group"
    # Links for join_splines_1
    links.new(bézier_segment.outputs[0], join_splines_1.inputs[0])
    links.new(join_splines_1.outputs[0], bi-_rail_loft.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "Outside"
    frame_001.location = (29.0, -651.6000366210938)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Centre"
    frame_002.location = (180.0, -35.79998779296875)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Rails"
    frame_003.location = (-3398.0, 567.4000244140625)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    quadratic_bézier = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier.name = "Quadratic Bézier"
    quadratic_bézier.label = ""
    quadratic_bézier.location = (29.0, -55.79998779296875)
    quadratic_bézier.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier.inputs[0].default_value = 40
    # Start
    quadratic_bézier.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier.inputs[2].default_value = Vector((0.0, -0.75, -0.12999999523162842))
    # End
    quadratic_bézier.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier

    quadratic_bézier_001 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_001.name = "Quadratic Bézier.001"
    quadratic_bézier_001.label = ""
    quadratic_bézier_001.location = (709.0, -235.79998779296875)
    quadratic_bézier_001.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_001.inputs[0].default_value = 40
    # Start
    quadratic_bézier_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier_001.inputs[2].default_value = Vector((0.0, -0.1599999964237213, 0.1899999976158142))
    # End
    quadratic_bézier_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier_001

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (889.0, -35.79998779296875)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002
    links.new(join_geometry_002.outputs[0], bi-_rail_loft.inputs[2])
    links.new(quadratic_bézier_001.outputs[0], join_geometry_002.inputs[0])
    links.new(quadratic_bézier.outputs[0], join_geometry_002.inputs[0])

    bézier_segment_003 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_003.name = "Bézier Segment.003"
    bézier_segment_003.label = ""
    bézier_segment_003.location = (369.0, -155.79998779296875)
    bézier_segment_003.bl_label = "Bézier Segment"
    bézier_segment_003.mode = "OFFSET"
    # Resolution
    bézier_segment_003.inputs[0].default_value = 200
    # Start
    bézier_segment_003.inputs[1].default_value = Vector((-0.11999999731779099, -0.05999999865889549, 0.4000000059604645))
    # Start Handle
    bézier_segment_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # End Handle
    bézier_segment_003.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # End
    bézier_segment_003.inputs[4].default_value = Vector((-0.09000000357627869, -0.05999999865889549, 0.41999998688697815))
    # Links for bézier_segment_003
    links.new(bézier_segment_003.outputs[0], join_geometry.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Profiles"
    frame_004.location = (-3369.0, -804.2000122070312)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    closure_input = nodes.new("NodeClosureInput")
    closure_input.name = "Closure Input"
    closure_input.label = ""
    closure_input.location = (-2220.0, -860.0)
    closure_input.bl_label = "Closure Input"
    # Links for closure_input

    closure_output = nodes.new("NodeClosureOutput")
    closure_output.name = "Closure Output"
    closure_output.label = ""
    closure_output.location = (-1760.0, -860.0)
    closure_output.bl_label = "Closure Output"
    closure_output.active_input_index = 0
    closure_output.active_output_index = 0
    closure_output.define_signature = False
    # Links for closure_output
    links.new(closure_output.outputs[0], bi-_rail_loft.inputs[9])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (-2040.0, -860.0)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(float_curve.outputs[0], closure_output.inputs[0])
    links.new(closure_input.outputs[0], float_curve.inputs[1])

    quadratic_bézier_005 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_005.name = "Quadratic Bézier.005"
    quadratic_bézier_005.label = ""
    quadratic_bézier_005.location = (549.0, -195.79998779296875)
    quadratic_bézier_005.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_005.inputs[0].default_value = 40
    # Start
    quadratic_bézier_005.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier_005.inputs[2].default_value = Vector((0.26999998092651367, -0.41999995708465576, 0.0))
    # End
    quadratic_bézier_005.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier_005
    links.new(quadratic_bézier_005.outputs[0], join_geometry_002.inputs[0])

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (-700.0, -1760.0)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(bi-_rail_loft.outputs[2], separate_x_y_z.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (-520.0, -1700.0)
    compare.bl_label = "Compare"
    compare.operation = "LESS_EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.85999995470047
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.3709999918937683
    # Links for compare
    links.new(separate_x_y_z.outputs[0], compare.inputs[0])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.label = ""
    extrude_mesh.location = (60.0, -1660.0)
    extrude_mesh.bl_label = "Extrude Mesh"
    extrude_mesh.mode = "FACES"
    # Offset
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.0010000000474974513
    # Individual
    extrude_mesh.inputs[4].default_value = False
    # Links for extrude_mesh

    pipes = nodes.new("GeometryNodeGroup")
    pipes.name = "Pipes"
    pipes.label = ""
    pipes.location = (640.0, -1820.0)
    pipes.node_tree = create_pipes_group()
    pipes.bl_label = "Group"
    # Links for pipes

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (480.0, -1820.0)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "FACE"
    # Links for separate_geometry
    links.new(separate_geometry.outputs[0], pipes.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry.inputs[1])
    links.new(extrude_mesh.outputs[0], separate_geometry.inputs[0])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (1680.0, -1460.0)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(pipes.outputs[0], join_geometry_001.inputs[0])
    links.new(extrude_mesh.outputs[0], join_geometry_001.inputs[0])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (360.0, -740.0)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Links for mesh_to_curve
    links.new(bi-_rail_loft.outputs[0], mesh_to_curve.inputs[0])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.label = ""
    compare_002.location = (360.0, -880.0)
    compare_002.bl_label = "Compare"
    compare_002.operation = "EQUAL"
    compare_002.data_type = "FLOAT"
    compare_002.mode = "ELEMENT"
    # B
    compare_002.inputs[1].default_value = 0.0
    # A
    compare_002.inputs[2].default_value = 0
    # B
    compare_002.inputs[3].default_value = 0
    # A
    compare_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_002.inputs[8].default_value = ""
    # B
    compare_002.inputs[9].default_value = ""
    # C
    compare_002.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_002.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_002.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_002
    links.new(separate_x_y_z.outputs[0], compare_002.inputs[0])
    links.new(compare_002.outputs[0], mesh_to_curve.inputs[1])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (920.0, -760.0)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh.inputs[2].default_value = 0.6599999666213989
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh

    quadrilateral = nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
    quadrilateral.name = "Quadrilateral"
    quadrilateral.label = ""
    quadrilateral.location = (240.0, -1020.0)
    quadrilateral.bl_label = "Quadrilateral"
    quadrilateral.mode = "RECTANGLE"
    # Width
    quadrilateral.inputs[0].default_value = 0.0430000014603138
    # Height
    quadrilateral.inputs[1].default_value = 0.006000000052154064
    # Bottom Width
    quadrilateral.inputs[2].default_value = 4.0
    # Top Width
    quadrilateral.inputs[3].default_value = 2.0
    # Offset
    quadrilateral.inputs[4].default_value = 1.0
    # Bottom Height
    quadrilateral.inputs[5].default_value = 3.0
    # Top Height
    quadrilateral.inputs[6].default_value = 1.0
    # Point 1
    quadrilateral.inputs[7].default_value = Vector((-1.0, -1.0, 0.0))
    # Point 2
    quadrilateral.inputs[8].default_value = Vector((1.0, -1.0, 0.0))
    # Point 3
    quadrilateral.inputs[9].default_value = Vector((1.0, 1.0, 0.0))
    # Point 4
    quadrilateral.inputs[10].default_value = Vector((-1.0, 1.0, 0.0))
    # Links for quadrilateral

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (1080.0, -760.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = False
    # Links for set_shade_smooth
    links.new(curve_to_mesh.outputs[0], set_shade_smooth.inputs[0])

    subdivide_curve = nodes.new("GeometryNodeSubdivideCurve")
    subdivide_curve.name = "Subdivide Curve"
    subdivide_curve.label = ""
    subdivide_curve.location = (400.0, -1020.0)
    subdivide_curve.bl_label = "Subdivide Curve"
    # Cuts
    subdivide_curve.inputs[1].default_value = 3
    # Links for subdivide_curve
    links.new(quadrilateral.outputs[0], subdivide_curve.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (560.0, -1020.0)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Position
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position
    links.new(subdivide_curve.outputs[0], set_position.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (-240.0, -1140.0)
    position.bl_label = "Position"
    # Links for position

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (-240.0, -1200.0)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001
    links.new(position.outputs[0], separate_x_y_z_001.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-80.0, -1140.0)
    math.bl_label = "Math"
    math.operation = "ABSOLUTE"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.5
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(separate_x_y_z_001.outputs[0], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (80.0, -1140.0)
    math_001.bl_label = "Math"
    math_001.operation = "DIVIDE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 0.0215000007301569
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math.outputs[0], math_001.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (240.0, -1140.0)
    math_002.bl_label = "Math"
    math_002.operation = "POWER"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 2.0
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(math_001.outputs[0], math_002.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (400.0, -1140.0)
    math_003.bl_label = "Math"
    math_003.operation = "MULTIPLY"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 0.0020000000949949026
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_002.outputs[0], math_003.inputs[0])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (560.0, -1140.0)
    combine_x_y_z.bl_label = "Combine XYZ"
    # X
    combine_x_y_z.inputs[0].default_value = 0.0
    # Z
    combine_x_y_z.inputs[2].default_value = 0.0
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], set_position.inputs[3])
    links.new(math_003.outputs[0], combine_x_y_z.inputs[1])

    fillet_curve = nodes.new("GeometryNodeFilletCurve")
    fillet_curve.name = "Fillet Curve"
    fillet_curve.label = ""
    fillet_curve.location = (720.0, -1020.0)
    fillet_curve.bl_label = "Fillet Curve"
    # Radius
    fillet_curve.inputs[1].default_value = 0.0010000000474974513
    # Limit Radius
    fillet_curve.inputs[2].default_value = True
    # Mode
    fillet_curve.inputs[3].default_value = "Bézier"
    # Count
    fillet_curve.inputs[4].default_value = 1
    # Links for fillet_curve
    links.new(fillet_curve.outputs[0], curve_to_mesh.inputs[1])
    links.new(set_position.outputs[0], fillet_curve.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    set_curve_tilt.label = ""
    set_curve_tilt.location = (760.0, -760.0)
    set_curve_tilt.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Tilt
    set_curve_tilt.inputs[2].default_value = 3.1415927410125732
    # Links for set_curve_tilt
    links.new(set_curve_tilt.outputs[0], curve_to_mesh.inputs[0])

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.label = ""
    boolean_math_003.location = (-120.0, -1780.0)
    boolean_math_003.bl_label = "Boolean Math"
    boolean_math_003.operation = "NOT"
    # Boolean
    boolean_math_003.inputs[1].default_value = False
    # Links for boolean_math_003
    links.new(boolean_math_003.outputs[0], extrude_mesh.inputs[1])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (440.0, -1620.0)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "OR"
    # Links for boolean_math
    links.new(extrude_mesh.outputs[1], boolean_math.inputs[0])
    links.new(extrude_mesh.outputs[2], boolean_math.inputs[1])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.name = "Separate Geometry.001"
    separate_geometry_001.label = ""
    separate_geometry_001.location = (640.0, -1500.0)
    separate_geometry_001.bl_label = "Separate Geometry"
    separate_geometry_001.domain = "FACE"
    # Links for separate_geometry_001
    links.new(extrude_mesh.outputs[0], separate_geometry_001.inputs[0])
    links.new(boolean_math.outputs[0], separate_geometry_001.inputs[1])

    rivet = nodes.new("GeometryNodeGroup")
    rivet.name = "Pipes.001"
    rivet.label = ""
    rivet.location = (1100.0, -1280.0)
    rivet.node_tree = create_rivet_group()
    rivet.bl_label = "Group"
    # Corners
    rivet.inputs[1].default_value = False
    # Offset
    rivet.inputs[2].default_value = -1.279999852180481
    # Spacing
    rivet.inputs[3].default_value = 0.9399999976158142
    # Links for rivet
    links.new(separate_geometry_001.outputs[1], rivet.inputs[0])
    links.new(rivet.outputs[0], join_geometry_001.inputs[0])

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (1360.0, -760.0)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "FACE"
    # Links for delete_geometry
    links.new(delete_geometry.outputs[0], join_geometry_001.inputs[0])
    links.new(set_shade_smooth.outputs[0], delete_geometry.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (1040.0, -980.0)
    position_001.bl_label = "Position"
    # Links for position_001

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_002.name = "Separate XYZ.002"
    separate_x_y_z_002.label = ""
    separate_x_y_z_002.location = (1040.0, -1040.0)
    separate_x_y_z_002.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_002
    links.new(position_001.outputs[0], separate_x_y_z_002.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (1200.0, -1040.0)
    compare_001.bl_label = "Compare"
    compare_001.operation = "GREATER_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = 0.0
    # A
    compare_001.inputs[2].default_value = 0
    # B
    compare_001.inputs[3].default_value = 0
    # A
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_001.inputs[8].default_value = ""
    # B
    compare_001.inputs[9].default_value = ""
    # C
    compare_001.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_001.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_001.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_001
    links.new(separate_x_y_z_002.outputs[0], compare_001.inputs[0])
    links.new(compare_001.outputs[0], delete_geometry.inputs[1])

    trim_curve = nodes.new("GeometryNodeTrimCurve")
    trim_curve.name = "Trim Curve"
    trim_curve.label = ""
    trim_curve.location = (580.0, -760.0)
    trim_curve.bl_label = "Trim Curve"
    trim_curve.mode = "FACTOR"
    # Selection
    trim_curve.inputs[1].default_value = True
    # Start
    trim_curve.inputs[2].default_value = 0.0
    # End
    trim_curve.inputs[3].default_value = 0.8569066524505615
    # Start
    trim_curve.inputs[4].default_value = 0.0
    # End
    trim_curve.inputs[5].default_value = 1.0
    # Links for trim_curve
    links.new(trim_curve.outputs[0], set_curve_tilt.inputs[0])
    links.new(mesh_to_curve.outputs[0], trim_curve.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.name = "Set Shade Smooth.001"
    set_shade_smooth_001.label = ""
    set_shade_smooth_001.location = (4540.0, -1500.0)
    set_shade_smooth_001.bl_label = "Set Shade Smooth"
    set_shade_smooth_001.domain = "EDGE"
    # Shade Smooth
    set_shade_smooth_001.inputs[2].default_value = False
    # Links for set_shade_smooth_001

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (4880.0, -1700.0)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.0))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, -0.7799999713897705, 1.0))
    # Links for transform_geometry
    links.new(set_shade_smooth_001.outputs[0], transform_geometry.inputs[0])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (5260.0, -1520.0)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003
    links.new(set_shade_smooth_001.outputs[0], join_geometry_003.inputs[0])

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.name = "Flip Faces"
    flip_faces.label = ""
    flip_faces.location = (5060.0, -1700.0)
    flip_faces.bl_label = "Flip Faces"
    # Selection
    flip_faces.inputs[1].default_value = True
    # Links for flip_faces
    links.new(flip_faces.outputs[0], join_geometry_003.inputs[0])
    links.new(transform_geometry.outputs[0], flip_faces.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (369.0, -29.0)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Count"
    # Count
    resample_curve.inputs[3].default_value = 47
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve

    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.label = ""
    delete_geometry_001.location = (909.0, -29.0)
    delete_geometry_001.bl_label = "Delete Geometry"
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "FACE"
    # Links for delete_geometry_001

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (909.0, -369.0)
    position_003.bl_label = "Position"
    # Links for position_003

    separate_x_y_z_005 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_005.name = "Separate XYZ.005"
    separate_x_y_z_005.label = ""
    separate_x_y_z_005.location = (909.0, -289.0)
    separate_x_y_z_005.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_005
    links.new(position_003.outputs[0], separate_x_y_z_005.inputs[0])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (909.0, -149.0)
    compare_003.bl_label = "Compare"
    compare_003.operation = "GREATER_THAN"
    compare_003.data_type = "FLOAT"
    compare_003.mode = "ELEMENT"
    # B
    compare_003.inputs[1].default_value = 0.0
    # A
    compare_003.inputs[2].default_value = 0
    # B
    compare_003.inputs[3].default_value = 0
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
    links.new(separate_x_y_z_005.outputs[0], compare_003.inputs[0])
    links.new(compare_003.outputs[0], delete_geometry_001.inputs[1])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (8600.0, -180.0)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(join_geometry_004.outputs[0], group_output.inputs[0])
    links.new(join_geometry_003.outputs[0], join_geometry_004.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (1658.0, -724.800048828125)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(delete_geometry_001.outputs[0], join_geometry_005.inputs[0])

    trim_curve_001 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_001.name = "Trim Curve.001"
    trim_curve_001.label = ""
    trim_curve_001.location = (209.0, -29.0)
    trim_curve_001.bl_label = "Trim Curve"
    trim_curve_001.mode = "FACTOR"
    # Selection
    trim_curve_001.inputs[1].default_value = True
    # Start
    trim_curve_001.inputs[2].default_value = 0.0
    # End
    trim_curve_001.inputs[3].default_value = 0.8784530162811279
    # Start
    trim_curve_001.inputs[4].default_value = 0.0
    # End
    trim_curve_001.inputs[5].default_value = 1.0
    # Links for trim_curve_001
    links.new(trim_curve_001.outputs[0], resample_curve.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (29.0, -29.0)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((0.0, -0.0020000000949949026, 0.0))
    # Rotation
    transform_geometry_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_001
    links.new(transform_geometry_001.outputs[0], trim_curve_001.inputs[0])
    links.new(join_splines_1.outputs[0], transform_geometry_001.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (1878.0, -704.800048828125)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(join_geometry_005.outputs[0], store_named_attribute.inputs[0])

    gold_decorations = nodes.new("GeometryNodeGroup")
    gold_decorations.name = "Group.003"
    gold_decorations.label = ""
    gold_decorations.location = (729.0, -29.0)
    gold_decorations.node_tree = create_gold__decorations_group()
    gold_decorations.bl_label = "Group"
    # Seed
    gold_decorations.inputs[1].default_value = 54
    # Scale
    gold_decorations.inputs[2].default_value = 4.0
    # Count
    gold_decorations.inputs[3].default_value = 20
    # Links for gold_decorations
    links.new(gold_decorations.outputs[0], delete_geometry_001.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (509.0, -29.0)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Count"
    # Count
    resample_curve_001.inputs[3].default_value = 47
    # Length
    resample_curve_001.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_001

    trim_curve_002 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_002.name = "Trim Curve.002"
    trim_curve_002.label = ""
    trim_curve_002.location = (349.0, -29.0)
    trim_curve_002.bl_label = "Trim Curve"
    trim_curve_002.mode = "FACTOR"
    # Selection
    trim_curve_002.inputs[1].default_value = True
    # Start
    trim_curve_002.inputs[2].default_value = 0.0
    # End
    trim_curve_002.inputs[3].default_value = 0.6187845468521118
    # Start
    trim_curve_002.inputs[4].default_value = 0.0
    # End
    trim_curve_002.inputs[5].default_value = 1.0
    # Links for trim_curve_002
    links.new(trim_curve_002.outputs[0], resample_curve_001.inputs[0])

    gold_decorations_1 = nodes.new("GeometryNodeGroup")
    gold_decorations_1.name = "Group.004"
    gold_decorations_1.label = ""
    gold_decorations_1.location = (849.0, -29.0)
    gold_decorations_1.node_tree = create_gold__decorations_group()
    gold_decorations_1.bl_label = "Group"
    # Seed
    gold_decorations_1.inputs[1].default_value = 58
    # Scale
    gold_decorations_1.inputs[2].default_value = 2.0
    # Count
    gold_decorations_1.inputs[3].default_value = 18
    # Links for gold_decorations_1
    links.new(gold_decorations_1.outputs[0], join_geometry_005.inputs[0])

    set_curve_normal = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal.name = "Set Curve Normal"
    set_curve_normal.label = ""
    set_curve_normal.location = (669.0, -29.0)
    set_curve_normal.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal.inputs[1].default_value = True
    # Mode
    set_curve_normal.inputs[2].default_value = "Free"
    # Links for set_curve_normal
    links.new(set_curve_normal.outputs[0], gold_decorations_1.inputs[0])
    links.new(resample_curve_001.outputs[0], set_curve_normal.inputs[0])

    sample_nearest_surface = nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.name = "Sample Nearest Surface"
    sample_nearest_surface.label = ""
    sample_nearest_surface.location = (309.0, -189.0)
    sample_nearest_surface.bl_label = "Sample Nearest Surface"
    sample_nearest_surface.data_type = "FLOAT_VECTOR"
    # Group ID
    sample_nearest_surface.inputs[2].default_value = 0
    # Sample Position
    sample_nearest_surface.inputs[3].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    sample_nearest_surface.inputs[4].default_value = 0
    # Links for sample_nearest_surface
    links.new(bi-_rail_loft.outputs[0], sample_nearest_surface.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.label = ""
    normal.location = (309.0, -409.0)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = False
    # Links for normal
    links.new(normal.outputs[0], sample_nearest_surface.inputs[1])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (469.0, -189.0)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "CROSS_PRODUCT"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(vector_math.outputs[0], set_curve_normal.inputs[3])
    links.new(sample_nearest_surface.outputs[0], vector_math.inputs[0])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (469.0, -329.0)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent
    links.new(curve_tangent.outputs[0], vector_math.inputs[1])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.name = "Separate Geometry.002"
    separate_geometry_002.label = ""
    separate_geometry_002.location = (29.0, -29.0)
    separate_geometry_002.bl_label = "Separate Geometry"
    separate_geometry_002.domain = "EDGE"
    # Links for separate_geometry_002
    links.new(separate_geometry_001.outputs[0], separate_geometry_002.inputs[0])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.label = ""
    boolean_math_001.location = (200.0, -1480.0)
    boolean_math_001.bl_label = "Boolean Math"
    boolean_math_001.operation = "AND"
    # Links for boolean_math_001
    links.new(boolean_math_001.outputs[0], separate_geometry_002.inputs[1])
    links.new(extrude_mesh.outputs[1], boolean_math_001.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (189.0, -29.0)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Selection
    mesh_to_curve_001.inputs[1].default_value = True
    # Links for mesh_to_curve_001
    links.new(separate_geometry_002.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(mesh_to_curve_001.outputs[0], trim_curve_002.inputs[0])

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = ""
    frame_005.location = (189.0, -515.800048828125)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = ""
    frame_006.location = (209.0, -35.800048828125)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    set_curve_tilt_001 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_001.name = "Set Curve Tilt.001"
    set_curve_tilt_001.label = ""
    set_curve_tilt_001.location = (549.0, -29.0)
    set_curve_tilt_001.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_001.inputs[1].default_value = True
    # Tilt
    set_curve_tilt_001.inputs[2].default_value = -0.16580626368522644
    # Links for set_curve_tilt_001
    links.new(set_curve_tilt_001.outputs[0], gold_decorations.inputs[0])
    links.new(resample_curve.outputs[0], set_curve_tilt_001.inputs[0])

    separate_geometry_003 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_003.name = "Separate Geometry.003"
    separate_geometry_003.label = ""
    separate_geometry_003.location = (438.0, -1184.800048828125)
    separate_geometry_003.bl_label = "Separate Geometry"
    separate_geometry_003.domain = "FACE"
    # Links for separate_geometry_003
    links.new(extrude_mesh.outputs[0], separate_geometry_003.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry_003.inputs[1])

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.name = "Group.002"
    gold_on_band.label = ""
    gold_on_band.location = (658.0, -1184.800048828125)
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.bl_label = "Group"
    # Density
    gold_on_band.inputs[1].default_value = 200000.0
    # W
    gold_on_band.inputs[2].default_value = 8.669999122619629
    # Seed
    gold_on_band.inputs[3].default_value = 1
    # Links for gold_on_band
    links.new(separate_geometry_003.outputs[0], gold_on_band.inputs[0])
    links.new(gold_on_band.outputs[0], join_geometry_005.inputs[0])

    frame_007 = nodes.new("NodeFrame")
    frame_007.name = "Frame.007"
    frame_007.label = "Gold"
    frame_007.location = (1942.0, 2584.800048828125)
    frame_007.bl_label = "Frame"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20
    # Links for frame_007

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (4138.0, -984.800048828125)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(switch.outputs[0], join_geometry_004.inputs[0])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (3858.0, -884.800048828125)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch.inputs[0])

    bézier_segment_004 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_004.name = "Bézier Segment.004"
    bézier_segment_004.label = ""
    bézier_segment_004.location = (229.0, -135.79998779296875)
    bézier_segment_004.bl_label = "Bézier Segment"
    bézier_segment_004.mode = "OFFSET"
    # Resolution
    bézier_segment_004.inputs[0].default_value = 16
    # Start
    bézier_segment_004.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Start Handle
    bézier_segment_004.inputs[2].default_value = Vector((1.0299999713897705, -0.6199999451637268, 0.0))
    # End Handle
    bézier_segment_004.inputs[3].default_value = Vector((-0.8299999833106995, -0.4300000071525574, 0.0))
    # End
    bézier_segment_004.inputs[4].default_value = Vector((1.0, 0.0, 0.0))
    # Links for bézier_segment_004
    links.new(bézier_segment_004.outputs[0], join_geometry_002.inputs[0])

    boolean_math_004 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.name = "Boolean Math.004"
    boolean_math_004.label = ""
    boolean_math_004.location = (-360.0, -1700.0)
    boolean_math_004.bl_label = "Boolean Math"
    boolean_math_004.operation = "AND"
    # Links for boolean_math_004
    links.new(boolean_math_004.outputs[0], boolean_math_003.inputs[0])
    links.new(boolean_math_004.outputs[0], boolean_math_001.inputs[0])
    links.new(compare.outputs[0], boolean_math_004.inputs[0])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (-520.0, -1860.0)
    compare_004.bl_label = "Compare"
    compare_004.operation = "GREATER_THAN"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    # B
    compare_004.inputs[1].default_value = 0.06999994814395905
    # A
    compare_004.inputs[2].default_value = 0
    # B
    compare_004.inputs[3].default_value = 0
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
    compare_004.inputs[12].default_value = 0.3709999918937683
    # Links for compare_004
    links.new(separate_x_y_z.outputs[1], compare_004.inputs[0])
    links.new(compare_004.outputs[0], boolean_math_004.inputs[1])

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.name = "Gem in Holder"
    gem_in_holder.label = ""
    gem_in_holder.location = (1109.0, -155.7999267578125)
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.bl_label = "Group"
    # Gem Radius
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder.inputs[2].default_value = False
    # Scale
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    # Wings
    gem_in_holder.inputs[6].default_value = True
    # Links for gem_in_holder

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (189.0, -475.7999267578125)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "COUNT"
    # Count
    curve_to_points.inputs[1].default_value = 10
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points

    for_each_geometry_element_input = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input.name = "For Each Geometry Element Input"
    for_each_geometry_element_input.label = ""
    for_each_geometry_element_input.location = (409.0, -415.7999267578125)
    for_each_geometry_element_input.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input.inputs[1].default_value = True
    # Links for for_each_geometry_element_input
    links.new(curve_to_points.outputs[0], for_each_geometry_element_input.inputs[0])
    links.new(curve_to_points.outputs[3], for_each_geometry_element_input.inputs[2])

    for_each_geometry_element_output = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.name = "For Each Geometry Element Output"
    for_each_geometry_element_output.label = ""
    for_each_geometry_element_output.location = (2029.0, -455.7999267578125)
    for_each_geometry_element_output.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output.active_input_index = 1
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = "POINT"
    for_each_geometry_element_output.inspection_index = 0
    # Links for for_each_geometry_element_output

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (189.0, -675.7999267578125)
    position_002.bl_label = "Position"
    # Links for position_002
    links.new(position_002.outputs[0], for_each_geometry_element_input.inputs[3])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    transform_geometry_002.label = ""
    transform_geometry_002.location = (1389.0, -475.7999267578125)
    transform_geometry_002.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_002.inputs[1].default_value = "Components"
    # Links for transform_geometry_002
    links.new(gem_in_holder.outputs[0], transform_geometry_002.inputs[0])
    links.new(for_each_geometry_element_input.outputs[3], transform_geometry_002.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.name = "Rotate Rotation"
    rotate_rotation.label = ""
    rotate_rotation.location = (1049.0, -675.7999267578125)
    rotate_rotation.bl_label = "Rotate Rotation"
    rotate_rotation.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation.inputs[1].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')
    # Links for rotate_rotation
    links.new(for_each_geometry_element_input.outputs[2], rotate_rotation.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (649.0, -395.7999267578125)
    random_value.bl_label = "Random Value"
    random_value.data_type = "INT"
    # Min
    random_value.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value.inputs[2].default_value = 0.0
    # Max
    random_value.inputs[3].default_value = 1.0
    # Min
    random_value.inputs[4].default_value = 5
    # Max
    random_value.inputs[5].default_value = 7
    # Probability
    random_value.inputs[6].default_value = 0.5
    # Seed
    random_value.inputs[8].default_value = 0
    # Links for random_value
    links.new(for_each_geometry_element_input.outputs[0], random_value.inputs[7])
    links.new(random_value.outputs[2], gem_in_holder.inputs[7])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    transform_geometry_003.label = ""
    transform_geometry_003.location = (1569.0, -475.7999267578125)
    transform_geometry_003.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_003.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_003.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    # Rotation
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_003.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_003
    links.new(transform_geometry_002.outputs[0], transform_geometry_003.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.label = ""
    join_geometry_006.location = (3878.0, -1064.800048828125)
    join_geometry_006.bl_label = "Join Geometry"
    # Links for join_geometry_006
    links.new(join_geometry_006.outputs[0], switch.inputs[2])
    links.new(store_named_attribute.outputs[0], join_geometry_006.inputs[0])
    links.new(for_each_geometry_element_output.outputs[2], join_geometry_006.inputs[0])

    trim_curve_003 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_003.name = "Trim Curve.003"
    trim_curve_003.label = ""
    trim_curve_003.location = (29.0, -475.7999267578125)
    trim_curve_003.bl_label = "Trim Curve"
    trim_curve_003.mode = "FACTOR"
    # Selection
    trim_curve_003.inputs[1].default_value = True
    # Start
    trim_curve_003.inputs[2].default_value = 0.04999999701976776
    # End
    trim_curve_003.inputs[3].default_value = 0.9000000953674316
    # Start
    trim_curve_003.inputs[4].default_value = 0.0
    # End
    trim_curve_003.inputs[5].default_value = 1.0
    # Links for trim_curve_003
    links.new(trim_curve_003.outputs[0], curve_to_points.inputs[0])
    links.new(set_curve_tilt.outputs[0], trim_curve_003.inputs[0])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.label = ""
    random_value_001.location = (629.0, -615.7999267578125)
    random_value_001.bl_label = "Random Value"
    random_value_001.data_type = "FLOAT"
    # Min
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_001.inputs[2].default_value = 0.25
    # Max
    random_value_001.inputs[3].default_value = 0.550000011920929
    # Min
    random_value_001.inputs[4].default_value = 0
    # Max
    random_value_001.inputs[5].default_value = 100
    # Probability
    random_value_001.inputs[6].default_value = 0.5
    # Seed
    random_value_001.inputs[8].default_value = 0
    # Links for random_value_001
    links.new(for_each_geometry_element_input.outputs[0], random_value_001.inputs[7])
    links.new(random_value_001.outputs[1], transform_geometry_002.inputs[4])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (1809.0, -495.7999267578125)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001
    links.new(store_named_attribute_001.outputs[0], for_each_geometry_element_output.inputs[1])
    links.new(transform_geometry_003.outputs[0], store_named_attribute_001.inputs[0])

    random_value_002 = nodes.new("FunctionNodeRandomValue")
    random_value_002.name = "Random Value.002"
    random_value_002.label = ""
    random_value_002.location = (649.0, -215.7999267578125)
    random_value_002.bl_label = "Random Value"
    random_value_002.data_type = "FLOAT"
    # Min
    random_value_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_002.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_002.inputs[2].default_value = 0.0
    # Max
    random_value_002.inputs[3].default_value = 100.0
    # Min
    random_value_002.inputs[4].default_value = 3
    # Max
    random_value_002.inputs[5].default_value = 7
    # Probability
    random_value_002.inputs[6].default_value = 0.5
    # Seed
    random_value_002.inputs[8].default_value = 13
    # Links for random_value_002
    links.new(for_each_geometry_element_input.outputs[0], random_value_002.inputs[7])
    links.new(random_value_002.outputs[1], gem_in_holder.inputs[10])

    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.name = "Rotate Rotation.001"
    rotate_rotation_001.label = ""
    rotate_rotation_001.location = (1209.0, -675.7999267578125)
    rotate_rotation_001.bl_label = "Rotate Rotation"
    rotate_rotation_001.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_001.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
    # Links for rotate_rotation_001
    links.new(rotate_rotation_001.outputs[0], transform_geometry_002.inputs[3])
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])

    random_value_003 = nodes.new("FunctionNodeRandomValue")
    random_value_003.name = "Random Value.003"
    random_value_003.label = ""
    random_value_003.location = (649.0, -35.7999267578125)
    random_value_003.bl_label = "Random Value"
    random_value_003.data_type = "FLOAT"
    # Min
    random_value_003.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_003.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_003.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_003.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_003.inputs[4].default_value = 3
    # Max
    random_value_003.inputs[5].default_value = 7
    # Probability
    random_value_003.inputs[6].default_value = 0.5
    # Seed
    random_value_003.inputs[8].default_value = 0
    # Links for random_value_003
    links.new(for_each_geometry_element_input.outputs[0], random_value_003.inputs[7])
    links.new(random_value_003.outputs[1], gem_in_holder.inputs[9])

    random_value_004 = nodes.new("FunctionNodeRandomValue")
    random_value_004.name = "Random Value.004"
    random_value_004.label = ""
    random_value_004.location = (889.0, -255.7999267578125)
    random_value_004.bl_label = "Random Value"
    random_value_004.data_type = "INT"
    # Min
    random_value_004.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_004.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_004.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_004.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_004.inputs[4].default_value = 0
    # Max
    random_value_004.inputs[5].default_value = 100
    # Probability
    random_value_004.inputs[6].default_value = 0.5
    # Seed
    random_value_004.inputs[8].default_value = 0
    # Links for random_value_004
    links.new(for_each_geometry_element_input.outputs[0], random_value_004.inputs[7])
    links.new(random_value_004.outputs[2], gem_in_holder.inputs[5])

    random_value_005 = nodes.new("FunctionNodeRandomValue")
    random_value_005.name = "Random Value.005"
    random_value_005.label = ""
    random_value_005.location = (889.0, -75.7999267578125)
    random_value_005.bl_label = "Random Value"
    random_value_005.data_type = "INT"
    # Min
    random_value_005.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_005.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_005.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_005.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_005.inputs[4].default_value = 6
    # Max
    random_value_005.inputs[5].default_value = 20
    # Probability
    random_value_005.inputs[6].default_value = 0.5
    # Seed
    random_value_005.inputs[8].default_value = 0
    # Links for random_value_005
    links.new(for_each_geometry_element_input.outputs[0], random_value_005.inputs[7])
    links.new(random_value_005.outputs[2], gem_in_holder.inputs[4])

    random_value_006 = nodes.new("FunctionNodeRandomValue")
    random_value_006.name = "Random Value.006"
    random_value_006.label = ""
    random_value_006.location = (889.0, -435.7999267578125)
    random_value_006.bl_label = "Random Value"
    random_value_006.data_type = "INT"
    # Min
    random_value_006.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_006.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_006.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_006.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_006.inputs[4].default_value = 5
    # Max
    random_value_006.inputs[5].default_value = 30
    # Probability
    random_value_006.inputs[6].default_value = 0.5
    # Seed
    random_value_006.inputs[8].default_value = 0
    # Links for random_value_006
    links.new(for_each_geometry_element_input.outputs[0], random_value_006.inputs[7])
    links.new(random_value_006.outputs[2], gem_in_holder.inputs[8])

    frame_008 = nodes.new("NodeFrame")
    frame_008.name = "Frame.008"
    frame_008.label = "Broaches"
    frame_008.location = (29.0, -1389.0001220703125)
    frame_008.bl_label = "Frame"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20
    # Links for frame_008

    set_shade_smooth_002 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_002.name = "Set Shade Smooth.002"
    set_shade_smooth_002.label = ""
    set_shade_smooth_002.location = (4380.0, -1500.0)
    set_shade_smooth_002.bl_label = "Set Shade Smooth"
    set_shade_smooth_002.domain = "FACE"
    # Selection
    set_shade_smooth_002.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_002.inputs[2].default_value = True
    # Links for set_shade_smooth_002
    links.new(set_shade_smooth_002.outputs[0], set_shade_smooth_001.inputs[0])
    links.new(join_geometry_001.outputs[0], set_shade_smooth_002.inputs[0])

    edge_angle = nodes.new("GeometryNodeInputMeshEdgeAngle")
    edge_angle.name = "Edge Angle"
    edge_angle.label = ""
    edge_angle.location = (4380.0, -1640.0)
    edge_angle.bl_label = "Edge Angle"
    # Links for edge_angle

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (4540.0, -1640.0)
    compare_005.bl_label = "Compare"
    compare_005.operation = "GREATER_THAN"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    # B
    compare_005.inputs[1].default_value = 1.0
    # A
    compare_005.inputs[2].default_value = 0
    # B
    compare_005.inputs[3].default_value = 0
    # A
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_005.inputs[8].default_value = ""
    # B
    compare_005.inputs[9].default_value = ""
    # C
    compare_005.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_005.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_005.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_005
    links.new(edge_angle.outputs[0], compare_005.inputs[0])
    links.new(compare_005.outputs[0], set_shade_smooth_001.inputs[1])

    gem_in_holder_1 = nodes.new("GeometryNodeGroup")
    gem_in_holder_1.name = "Gem in Holder.001"
    gem_in_holder_1.label = ""
    gem_in_holder_1.location = (1209.0, -75.13334655761719)
    gem_in_holder_1.node_tree = create_gem_in__holder_group()
    gem_in_holder_1.bl_label = "Group"
    # Gem Radius
    gem_in_holder_1.inputs[0].default_value = 0.009999990463256836
    # Gem Material
    gem_in_holder_1.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_1.inputs[2].default_value = False
    # Scale
    gem_in_holder_1.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_1.inputs[4].default_value = 20
    # Seed
    gem_in_holder_1.inputs[5].default_value = 10
    # Wings
    gem_in_holder_1.inputs[6].default_value = False
    # Array Count
    gem_in_holder_1.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_1.inputs[8].default_value = 10
    # Links for gem_in_holder_1

    mesh_to_curve_002 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.name = "Mesh to Curve.002"
    mesh_to_curve_002.label = ""
    mesh_to_curve_002.location = (29.0, -55.13334655761719)
    mesh_to_curve_002.bl_label = "Mesh to Curve"
    mesh_to_curve_002.mode = "EDGES"
    # Links for mesh_to_curve_002

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Is Edge Boundary"
    is_edge_boundary.label = ""
    is_edge_boundary.location = (29.0, -175.1333465576172)
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    is_edge_boundary.bl_label = "Group"
    # Links for is_edge_boundary
    links.new(is_edge_boundary.outputs[0], mesh_to_curve_002.inputs[1])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    set_spline_cyclic.label = ""
    set_spline_cyclic.location = (349.0, -55.13334655761719)
    set_spline_cyclic.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = False
    # Links for set_spline_cyclic

    trim_curve_004 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_004.name = "Trim Curve.004"
    trim_curve_004.label = ""
    trim_curve_004.location = (509.0, -55.13334655761719)
    trim_curve_004.bl_label = "Trim Curve"
    trim_curve_004.mode = "FACTOR"
    # Selection
    trim_curve_004.inputs[1].default_value = True
    # Start
    trim_curve_004.inputs[2].default_value = 0.6629834175109863
    # End
    trim_curve_004.inputs[3].default_value = 0.9834254384040833
    # Start
    trim_curve_004.inputs[4].default_value = 0.0
    # End
    trim_curve_004.inputs[5].default_value = 1.0
    # Links for trim_curve_004
    links.new(set_spline_cyclic.outputs[0], trim_curve_004.inputs[0])

    curve_to_points_001 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.name = "Curve to Points.001"
    curve_to_points_001.label = ""
    curve_to_points_001.location = (669.0, -55.13334655761719)
    curve_to_points_001.bl_label = "Curve to Points"
    curve_to_points_001.mode = "COUNT"
    # Count
    curve_to_points_001.inputs[1].default_value = 50
    # Length
    curve_to_points_001.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points_001
    links.new(trim_curve_004.outputs[0], curve_to_points_001.inputs[0])

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.label = ""
    capture_attribute.location = (-200.0, -1480.0)
    capture_attribute.bl_label = "Capture Attribute"
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    # Links for capture_attribute
    links.new(bi-_rail_loft.outputs[0], capture_attribute.inputs[0])
    links.new(capture_attribute.outputs[0], extrude_mesh.inputs[0])

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.name = "Normal.001"
    normal_001.label = ""
    normal_001.location = (-200.0, -1600.0)
    normal_001.bl_label = "Normal"
    normal_001.legacy_corner_normals = False
    # Links for normal_001
    links.new(normal_001.outputs[0], capture_attribute.inputs[1])

    set_curve_normal_001 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.name = "Set Curve Normal.001"
    set_curve_normal_001.label = ""
    set_curve_normal_001.location = (189.0, -55.13334655761719)
    set_curve_normal_001.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_001.inputs[1].default_value = True
    # Mode
    set_curve_normal_001.inputs[2].default_value = "Free"
    # Links for set_curve_normal_001
    links.new(set_curve_normal_001.outputs[0], set_spline_cyclic.inputs[0])
    links.new(mesh_to_curve_002.outputs[0], set_curve_normal_001.inputs[0])
    links.new(capture_attribute.outputs[1], set_curve_normal_001.inputs[3])

    position_004 = nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"
    position_004.label = ""
    position_004.location = (669.0, -255.1333465576172)
    position_004.bl_label = "Position"
    # Links for position_004

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.name = "For Each Geometry Element Input.001"
    for_each_geometry_element_input_001.label = ""
    for_each_geometry_element_input_001.location = (829.0, -55.13334655761719)
    for_each_geometry_element_input_001.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input_001.inputs[1].default_value = True
    # Links for for_each_geometry_element_input_001
    links.new(curve_to_points_001.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(position_004.outputs[0], for_each_geometry_element_input_001.inputs[2])
    links.new(curve_to_points_001.outputs[3], for_each_geometry_element_input_001.inputs[3])

    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.name = "For Each Geometry Element Output.001"
    for_each_geometry_element_output_001.label = ""
    for_each_geometry_element_output_001.location = (2169.0, -75.13334655761719)
    for_each_geometry_element_output_001.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    # Links for for_each_geometry_element_output_001
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_006.inputs[0])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    transform_geometry_004.label = ""
    transform_geometry_004.location = (1469.0, -75.13334655761719)
    transform_geometry_004.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_004.inputs[1].default_value = "Components"
    # Scale
    transform_geometry_004.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_004
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_004.inputs[2])
    links.new(gem_in_holder_1.outputs[4], transform_geometry_004.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.name = "Rotate Rotation.002"
    rotate_rotation_002.label = ""
    rotate_rotation_002.location = (869.0, -315.13336181640625)
    rotate_rotation_002.bl_label = "Rotate Rotation"
    rotate_rotation_002.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, -1.5707963705062866, 0.0), 'XYZ')
    # Links for rotate_rotation_002
    links.new(rotate_rotation_002.outputs[0], transform_geometry_004.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[3], rotate_rotation_002.inputs[0])

    frame_009 = nodes.new("NodeFrame")
    frame_009.name = "Frame.009"
    frame_009.label = "Random Wings"
    frame_009.location = (189.0, -2369.666748046875)
    frame_009.bl_label = "Frame"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20
    # Links for frame_009

    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.name = "Random Value.007"
    random_value_007.label = ""
    random_value_007.location = (1029.0, -75.13334655761719)
    random_value_007.bl_label = "Random Value"
    random_value_007.data_type = "FLOAT"
    # Min
    random_value_007.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_007.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_007.inputs[2].default_value = 6.0
    # Max
    random_value_007.inputs[3].default_value = 7.0
    # Min
    random_value_007.inputs[4].default_value = 0
    # Max
    random_value_007.inputs[5].default_value = 100
    # Probability
    random_value_007.inputs[6].default_value = 0.5
    # Seed
    random_value_007.inputs[8].default_value = 32
    # Links for random_value_007
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_1.inputs[10])

    random_value_008 = nodes.new("FunctionNodeRandomValue")
    random_value_008.name = "Random Value.008"
    random_value_008.label = ""
    random_value_008.location = (1029.0, -255.1333465576172)
    random_value_008.bl_label = "Random Value"
    random_value_008.data_type = "FLOAT"
    # Min
    random_value_008.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_008.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_008.inputs[2].default_value = 0.0
    # Max
    random_value_008.inputs[3].default_value = 0.003000000026077032
    # Min
    random_value_008.inputs[4].default_value = 0
    # Max
    random_value_008.inputs[5].default_value = 100
    # Probability
    random_value_008.inputs[6].default_value = 0.5
    # Seed
    random_value_008.inputs[8].default_value = 10
    # Links for random_value_008
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_008.inputs[7])
    links.new(random_value_008.outputs[1], gem_in_holder_1.inputs[9])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (38.0, -3284.800048828125)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(reroute.outputs[0], mesh_to_curve_002.inputs[0])
    links.new(separate_geometry.outputs[0], reroute.inputs[0])

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.name = "Distribute Points on Faces"
    distribute_points_on_faces.label = ""
    distribute_points_on_faces.location = (149.0, -35.79998779296875)
    distribute_points_on_faces.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    # Selection
    distribute_points_on_faces.inputs[1].default_value = True
    # Distance Min
    distribute_points_on_faces.inputs[2].default_value = 0.0
    # Density Max
    distribute_points_on_faces.inputs[3].default_value = 10.0
    # Density
    distribute_points_on_faces.inputs[4].default_value = 5000.0
    # Density Factor
    distribute_points_on_faces.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces.inputs[6].default_value = 0
    # Links for distribute_points_on_faces
    links.new(reroute.outputs[0], distribute_points_on_faces.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (509.0, -35.79998779296875)
    instance_on_points.bl_label = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Rotation
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points
    links.new(distribute_points_on_faces.outputs[0], instance_on_points.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    ico_sphere.label = ""
    ico_sphere.location = (29.0, -235.79998779296875)
    ico_sphere.bl_label = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.0020000000949949026
    # Subdivisions
    ico_sphere.inputs[1].default_value = 2
    # Links for ico_sphere

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (689.0, -35.79998779296875)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "INSTANCE"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "ruby"
    # Links for store_named_attribute_002
    links.new(instance_on_points.outputs[0], store_named_attribute_002.inputs[0])

    random_value_009 = nodes.new("FunctionNodeRandomValue")
    random_value_009.name = "Random Value.009"
    random_value_009.label = ""
    random_value_009.location = (689.0, -195.79998779296875)
    random_value_009.bl_label = "Random Value"
    random_value_009.data_type = "BOOLEAN"
    # Min
    random_value_009.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_009.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_009.inputs[2].default_value = 0.0
    # Max
    random_value_009.inputs[3].default_value = 1.0
    # Min
    random_value_009.inputs[4].default_value = 0
    # Max
    random_value_009.inputs[5].default_value = 100
    # Probability
    random_value_009.inputs[6].default_value = 0.5
    # ID
    random_value_009.inputs[7].default_value = 0
    # Seed
    random_value_009.inputs[8].default_value = 0
    # Links for random_value_009
    links.new(random_value_009.outputs[3], store_named_attribute_002.inputs[3])

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.label = ""
    boolean_math_002.location = (869.0, -195.79998779296875)
    boolean_math_002.bl_label = "Boolean Math"
    boolean_math_002.operation = "NOT"
    # Boolean
    boolean_math_002.inputs[1].default_value = False
    # Links for boolean_math_002
    links.new(random_value_009.outputs[3], boolean_math_002.inputs[0])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (869.0, -35.79998779296875)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "INSTANCE"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "saphire"
    # Links for store_named_attribute_003
    links.new(store_named_attribute_002.outputs[0], store_named_attribute_003.inputs[0])
    links.new(boolean_math_002.outputs[0], store_named_attribute_003.inputs[3])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (1029.0, -35.79998779296875)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(store_named_attribute_003.outputs[0], realize_instances.inputs[0])
    links.new(realize_instances.outputs[0], join_geometry_006.inputs[0])

    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.name = "Set Shade Smooth.003"
    set_shade_smooth_003.label = ""
    set_shade_smooth_003.location = (209.0, -235.79998779296875)
    set_shade_smooth_003.bl_label = "Set Shade Smooth"
    set_shade_smooth_003.domain = "FACE"
    # Selection
    set_shade_smooth_003.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_003.inputs[2].default_value = True
    # Links for set_shade_smooth_003
    links.new(set_shade_smooth_003.outputs[0], instance_on_points.inputs[2])
    links.new(ico_sphere.outputs[0], set_shade_smooth_003.inputs[0])

    frame_010 = nodes.new("NodeFrame")
    frame_010.name = "Frame.010"
    frame_010.label = "Random Jewels"
    frame_010.location = (629.0, -3209.0)
    frame_010.bl_label = "Frame"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20
    # Links for frame_010

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (69.0, -75.79999542236328)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001

    distribute_points_on_faces_001 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_001.name = "Distribute Points on Faces.001"
    distribute_points_on_faces_001.label = ""
    distribute_points_on_faces_001.location = (449.0, -35.79999542236328)
    distribute_points_on_faces_001.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces_001.distribute_method = "POISSON"
    distribute_points_on_faces_001.use_legacy_normal = False
    # Distance Min
    distribute_points_on_faces_001.inputs[2].default_value = 0.009999999776482582
    # Density Max
    distribute_points_on_faces_001.inputs[3].default_value = 5000.0
    # Density
    distribute_points_on_faces_001.inputs[4].default_value = 500.0
    # Density Factor
    distribute_points_on_faces_001.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces_001.inputs[6].default_value = 0
    # Links for distribute_points_on_faces_001
    links.new(reroute_001.outputs[0], distribute_points_on_faces_001.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (89.0, -195.79998779296875)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "POINTS"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity
    links.new(for_each_geometry_element_output_001.outputs[2], geometry_proximity.inputs[0])

    compare_006 = nodes.new("FunctionNodeCompare")
    compare_006.name = "Compare.006"
    compare_006.label = ""
    compare_006.location = (289.0, -195.79998779296875)
    compare_006.bl_label = "Compare"
    compare_006.operation = "LESS_THAN"
    compare_006.data_type = "FLOAT"
    compare_006.mode = "ELEMENT"
    # B
    compare_006.inputs[1].default_value = 0.006000000052154064
    # A
    compare_006.inputs[2].default_value = 0
    # B
    compare_006.inputs[3].default_value = 0
    # A
    compare_006.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_006.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_006.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_006.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_006.inputs[8].default_value = ""
    # B
    compare_006.inputs[9].default_value = ""
    # C
    compare_006.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_006.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_006.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_006
    links.new(geometry_proximity.outputs[1], compare_006.inputs[0])
    links.new(compare_006.outputs[0], distribute_points_on_faces_001.inputs[1])

    gem_in_holder_2 = nodes.new("GeometryNodeGroup")
    gem_in_holder_2.name = "Gem in Holder.002"
    gem_in_holder_2.label = ""
    gem_in_holder_2.location = (29.0, -435.79998779296875)
    gem_in_holder_2.node_tree = create_gem_in__holder_group()
    gem_in_holder_2.bl_label = "Group"
    # Gem Radius
    gem_in_holder_2.inputs[0].default_value = 0.009999990463256836
    # Gem Material
    gem_in_holder_2.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_2.inputs[2].default_value = False
    # Scale
    gem_in_holder_2.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_2.inputs[4].default_value = 20
    # Seed
    gem_in_holder_2.inputs[5].default_value = 10
    # Wings
    gem_in_holder_2.inputs[6].default_value = False
    # Array Count
    gem_in_holder_2.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_2.inputs[8].default_value = 10
    # Split
    gem_in_holder_2.inputs[9].default_value = 0.0010000000474974513
    # Seed
    gem_in_holder_2.inputs[10].default_value = 6.6099958419799805
    # Links for gem_in_holder_2

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.label = ""
    instance_on_points_001.location = (709.0, -75.79999542236328)
    instance_on_points_001.bl_label = "Instance on Points"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Links for instance_on_points_001
    links.new(distribute_points_on_faces_001.outputs[0], instance_on_points_001.inputs[0])
    links.new(distribute_points_on_faces_001.outputs[2], instance_on_points_001.inputs[5])

    random_value_010 = nodes.new("FunctionNodeRandomValue")
    random_value_010.name = "Random Value.010"
    random_value_010.label = ""
    random_value_010.location = (469.0, -415.79998779296875)
    random_value_010.bl_label = "Random Value"
    random_value_010.data_type = "FLOAT"
    # Min
    random_value_010.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_010.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_010.inputs[2].default_value = 0.20000000298023224
    # Max
    random_value_010.inputs[3].default_value = 0.5
    # Min
    random_value_010.inputs[4].default_value = 0
    # Max
    random_value_010.inputs[5].default_value = 100
    # Probability
    random_value_010.inputs[6].default_value = 0.5
    # ID
    random_value_010.inputs[7].default_value = 0
    # Seed
    random_value_010.inputs[8].default_value = 0
    # Links for random_value_010
    links.new(random_value_010.outputs[1], instance_on_points_001.inputs[6])

    frame_011 = nodes.new("NodeFrame")
    frame_011.name = "Frame.011"
    frame_011.label = "Larger Jewels"
    frame_011.location = (2669.0, -2649.0)
    frame_011.bl_label = "Frame"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20
    # Links for frame_011

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.label = ""
    realize_instances_001.location = (1049.0, -75.79999542236328)
    realize_instances_001.bl_label = "Realize Instances"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0
    # Links for realize_instances_001

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.label = ""
    transform_geometry_005.location = (269.0, -435.79998779296875)
    transform_geometry_005.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_005.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    # Rotation
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_005
    links.new(transform_geometry_005.outputs[0], instance_on_points_001.inputs[2])
    links.new(gem_in_holder_2.outputs[0], transform_geometry_005.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.name = "Group.005"
    swap_attr.label = ""
    swap_attr.location = (1209.0, -75.79999542236328)
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.bl_label = "Group"
    # Old
    swap_attr.inputs[2].default_value = "ruby"
    # New
    swap_attr.inputs[3].default_value = "saphire"
    # Links for swap_attr
    links.new(swap_attr.outputs[0], join_geometry_006.inputs[0])
    links.new(realize_instances_001.outputs[0], swap_attr.inputs[0])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (889.0, -75.79999542236328)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "INSTANCE"
    # Links for capture_attribute_001
    links.new(capture_attribute_001.outputs[0], realize_instances_001.inputs[0])
    links.new(instance_on_points_001.outputs[0], capture_attribute_001.inputs[0])
    links.new(capture_attribute_001.outputs[1], swap_attr.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (849.0, -195.79998779296875)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], capture_attribute_001.inputs[1])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1649.0, -75.13334655761719)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001
    links.new(transform_geometry_004.outputs[0], set_position_001.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (1498.0, -2964.800048828125)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], reroute_001.inputs[0])
    links.new(separate_geometry_001.outputs[1], reroute_002.inputs[0])

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.label = ""
    geometry_proximity_001.location = (1469.0, -295.13336181640625)
    geometry_proximity_001.bl_label = "Geometry Proximity"
    geometry_proximity_001.target_element = "FACES"
    # Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0
    # Links for geometry_proximity_001
    links.new(reroute_002.outputs[0], geometry_proximity_001.inputs[0])
    links.new(geometry_proximity_001.outputs[0], set_position_001.inputs[2])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (1809.0, -75.13334655761719)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False
    # Links for curve_to_mesh_001
    links.new(set_position_001.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(gem_in_holder_1.outputs[1], curve_to_mesh_001.inputs[1])
    links.new(gem_in_holder_1.outputs[2], curve_to_mesh_001.inputs[2])

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (1989.0, -75.13334655761719)
    store_named_attribute_004.bl_label = "Store Named Attribute"
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_004.inputs[3].default_value = True
    # Links for store_named_attribute_004
    links.new(store_named_attribute_004.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(curve_to_mesh_001.outputs[0], store_named_attribute_004.inputs[0])

    # Parent assignments
    bézier_segment.parent = frame
    frame.parent = frame_002
    bézier_segment_001.parent = frame_001
    bézier_segment_002.parent = frame_001
    join_geometry.parent = frame_001
    join_splines.parent = frame_001
    join_splines_1.parent = frame_002
    frame_001.parent = frame_003
    frame_002.parent = frame_003
    quadratic_bézier.parent = frame_004
    quadratic_bézier_001.parent = frame_004
    join_geometry_002.parent = frame_004
    bézier_segment_003.parent = frame_001
    quadratic_bézier_005.parent = frame_004
    resample_curve.parent = frame_006
    delete_geometry_001.parent = frame_006
    position_003.parent = frame_006
    separate_x_y_z_005.parent = frame_006
    compare_003.parent = frame_006
    join_geometry_005.parent = frame_007
    trim_curve_001.parent = frame_006
    transform_geometry_001.parent = frame_006
    store_named_attribute.parent = frame_007
    gold_decorations.parent = frame_006
    resample_curve_001.parent = frame_005
    trim_curve_002.parent = frame_005
    gold_decorations_1.parent = frame_005
    set_curve_normal.parent = frame_005
    sample_nearest_surface.parent = frame_005
    normal.parent = frame_005
    vector_math.parent = frame_005
    curve_tangent.parent = frame_005
    separate_geometry_002.parent = frame_005
    mesh_to_curve_001.parent = frame_005
    frame_005.parent = frame_007
    frame_006.parent = frame_007
    set_curve_tilt_001.parent = frame_006
    separate_geometry_003.parent = frame_007
    gold_on_band.parent = frame_007
    switch.parent = frame_007
    group_input.parent = frame_007
    bézier_segment_004.parent = frame_004
    gem_in_holder.parent = frame_008
    curve_to_points.parent = frame_008
    for_each_geometry_element_input.parent = frame_008
    for_each_geometry_element_output.parent = frame_008
    position_002.parent = frame_008
    transform_geometry_002.parent = frame_008
    rotate_rotation.parent = frame_008
    random_value.parent = frame_008
    transform_geometry_003.parent = frame_008
    join_geometry_006.parent = frame_007
    trim_curve_003.parent = frame_008
    random_value_001.parent = frame_008
    store_named_attribute_001.parent = frame_008
    random_value_002.parent = frame_008
    rotate_rotation_001.parent = frame_008
    random_value_003.parent = frame_008
    random_value_004.parent = frame_008
    random_value_005.parent = frame_008
    random_value_006.parent = frame_008
    frame_008.parent = frame_007
    gem_in_holder_1.parent = frame_009
    mesh_to_curve_002.parent = frame_009
    is_edge_boundary.parent = frame_009
    set_spline_cyclic.parent = frame_009
    trim_curve_004.parent = frame_009
    curve_to_points_001.parent = frame_009
    set_curve_normal_001.parent = frame_009
    position_004.parent = frame_009
    for_each_geometry_element_input_001.parent = frame_009
    for_each_geometry_element_output_001.parent = frame_009
    transform_geometry_004.parent = frame_009
    rotate_rotation_002.parent = frame_009
    frame_009.parent = frame_007
    random_value_007.parent = frame_009
    random_value_008.parent = frame_009
    reroute.parent = frame_007
    distribute_points_on_faces.parent = frame_010
    instance_on_points.parent = frame_010
    ico_sphere.parent = frame_010
    store_named_attribute_002.parent = frame_010
    random_value_009.parent = frame_010
    boolean_math_002.parent = frame_010
    store_named_attribute_003.parent = frame_010
    realize_instances.parent = frame_010
    set_shade_smooth_003.parent = frame_010
    frame_010.parent = frame_007
    reroute_001.parent = frame_011
    distribute_points_on_faces_001.parent = frame_011
    geometry_proximity.parent = frame_011
    compare_006.parent = frame_011
    gem_in_holder_2.parent = frame_011
    instance_on_points_001.parent = frame_011
    random_value_010.parent = frame_011
    frame_011.parent = frame_007
    realize_instances_001.parent = frame_011
    transform_geometry_005.parent = frame_011
    swap_attr.parent = frame_011
    capture_attribute_001.parent = frame_011
    index.parent = frame_011
    set_position_001.parent = frame_009
    reroute_002.parent = frame_007
    geometry_proximity_001.parent = frame_009
    curve_to_mesh_001.parent = frame_009
    store_named_attribute_004.parent = frame_009

    auto_layout_nodes(group)
    return group

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

    # Parent assignments

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_blocker_group():
    group_name = "Blocker"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1991.1298828125, -100.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (1511.1298828125, -100.0)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (1671.1298828125, -100.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True
    # Links for set_shade_smooth
    links.new(set_shade_smooth.outputs[0], group_output.inputs[0])
    links.new(join_geometry.outputs[0], set_shade_smooth.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (7331.1298828125, -712.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "blocker"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(store_named_attribute.outputs[0], join_geometry.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    ico_sphere.label = ""
    ico_sphere.location = (30.0, -276.0)
    ico_sphere.bl_label = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.1300000250339508
    # Subdivisions
    ico_sphere.inputs[1].default_value = 3
    # Links for ico_sphere

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (330.0, -376.0)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((-0.03999999910593033, 0.0, 0.25))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.2000000476837158))
    # Links for transform_geometry
    links.new(ico_sphere.outputs[0], transform_geometry.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "Chest"
    frame_001.location = (-1910.0, 696.0)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (330.0, -36.0)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((-0.10000000149011612, 0.019999999552965164, 0.33000001311302185))
    # Rotation
    transform_geometry_001.inputs[3].default_value = Euler((0.0, -0.13439033925533295, 0.18500488996505737), 'XYZ')
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0199999809265137, 0.8300000429153442, 0.8400001525878906))
    # Links for transform_geometry_001
    links.new(ico_sphere.outputs[0], transform_geometry_001.inputs[0])

    mesh_to_s_d_f_grid = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid.name = "Mesh to SDF Grid"
    mesh_to_s_d_f_grid.label = ""
    mesh_to_s_d_f_grid.location = (570.0, -436.0)
    mesh_to_s_d_f_grid.bl_label = "Mesh to SDF Grid"
    # Voxel Size
    mesh_to_s_d_f_grid.inputs[1].default_value = 0.004999999888241291
    # Band Width
    mesh_to_s_d_f_grid.inputs[2].default_value = 2
    # Links for mesh_to_s_d_f_grid
    links.new(transform_geometry.outputs[0], mesh_to_s_d_f_grid.inputs[0])

    mesh_to_s_d_f_grid_001 = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid_001.name = "Mesh to SDF Grid.001"
    mesh_to_s_d_f_grid_001.label = ""
    mesh_to_s_d_f_grid_001.location = (570.0, -296.0)
    mesh_to_s_d_f_grid_001.bl_label = "Mesh to SDF Grid"
    # Voxel Size
    mesh_to_s_d_f_grid_001.inputs[1].default_value = 0.004999999888241291
    # Band Width
    mesh_to_s_d_f_grid_001.inputs[2].default_value = 2
    # Links for mesh_to_s_d_f_grid_001
    links.new(transform_geometry_001.outputs[0], mesh_to_s_d_f_grid_001.inputs[0])

    s_d_f_grid_boolean = nodes.new("GeometryNodeSDFGridBoolean")
    s_d_f_grid_boolean.name = "SDF Grid Boolean"
    s_d_f_grid_boolean.label = ""
    s_d_f_grid_boolean.location = (730.0, -296.0)
    s_d_f_grid_boolean.bl_label = "SDF Grid Boolean"
    s_d_f_grid_boolean.operation = "UNION"
    # Grid 1
    s_d_f_grid_boolean.inputs[0].default_value = 0.0
    # Links for s_d_f_grid_boolean
    links.new(mesh_to_s_d_f_grid.outputs[0], s_d_f_grid_boolean.inputs[1])
    links.new(mesh_to_s_d_f_grid_001.outputs[0], s_d_f_grid_boolean.inputs[1])

    grid_to_mesh = nodes.new("GeometryNodeGridToMesh")
    grid_to_mesh.name = "Grid to Mesh"
    grid_to_mesh.label = ""
    grid_to_mesh.location = (1050.0, -296.0)
    grid_to_mesh.bl_label = "Grid to Mesh"
    # Threshold
    grid_to_mesh.inputs[1].default_value = 0.0
    # Adaptivity
    grid_to_mesh.inputs[2].default_value = 0.0
    # Links for grid_to_mesh

    s_d_f_grid_fillet = nodes.new("GeometryNodeSDFGridFillet")
    s_d_f_grid_fillet.name = "SDF Grid Fillet"
    s_d_f_grid_fillet.label = ""
    s_d_f_grid_fillet.location = (890.0, -296.0)
    s_d_f_grid_fillet.bl_label = "SDF Grid Fillet"
    # Iterations
    s_d_f_grid_fillet.inputs[1].default_value = 3
    # Links for s_d_f_grid_fillet
    links.new(s_d_f_grid_boolean.outputs[0], s_d_f_grid_fillet.inputs[0])
    links.new(s_d_f_grid_fillet.outputs[0], grid_to_mesh.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (1730.0, -276.0)
    instance_on_points.bl_label = "Instance on Points"
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Scale
    instance_on_points.inputs[6].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))
    # Links for instance_on_points
    links.new(grid_to_mesh.outputs[0], instance_on_points.inputs[0])

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.name = "Curve Circle.001"
    curve_circle_001.label = ""
    curve_circle_001.location = (870.0, -476.0)
    curve_circle_001.bl_label = "Curve Circle"
    curve_circle_001.mode = "RADIUS"
    # Resolution
    curve_circle_001.inputs[0].default_value = 9
    # Point 1
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_001.inputs[4].default_value = 0.004999999888241291
    # Links for curve_circle_001

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (1050.0, -476.0)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_001.inputs[2].default_value = 0.21000000834465027
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False
    # Links for curve_to_mesh_001
    links.new(curve_circle_001.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(curve_circle_001.outputs[0], curve_to_mesh_001.inputs[1])
    links.new(curve_to_mesh_001.outputs[0], instance_on_points.inputs[2])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (1370.0, -416.0)
    position_002.bl_label = "Position"
    # Links for position_002

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (1370.0, -476.0)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001
    links.new(position_002.outputs[0], separate_x_y_z_001.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (1530.0, -416.0)
    compare_001.bl_label = "Compare"
    compare_001.operation = "LESS_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = -0.09999999403953552
    # A
    compare_001.inputs[2].default_value = 0
    # B
    compare_001.inputs[3].default_value = 0
    # A
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_001.inputs[8].default_value = ""
    # B
    compare_001.inputs[9].default_value = ""
    # C
    compare_001.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_001.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_001.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_001
    links.new(separate_x_y_z_001.outputs[0], compare_001.inputs[0])
    links.new(compare_001.outputs[0], instance_on_points.inputs[1])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.label = ""
    align_rotation_to_vector.location = (1210.0, -616.0)
    align_rotation_to_vector.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector.axis = "Z"
    align_rotation_to_vector.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.name = "Normal.001"
    normal_001.label = ""
    normal_001.location = (1050.0, -616.0)
    normal_001.bl_label = "Normal"
    normal_001.legacy_corner_normals = False
    # Links for normal_001
    links.new(normal_001.outputs[0], align_rotation_to_vector.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.name = "Rotate Rotation"
    rotate_rotation.label = ""
    rotate_rotation.location = (1370.0, -616.0)
    rotate_rotation.bl_label = "Rotate Rotation"
    rotate_rotation.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation.inputs[1].default_value = Euler((-0.3707079291343689, 0.3525564670562744, 0.0), 'XYZ')
    # Links for rotate_rotation
    links.new(align_rotation_to_vector.outputs[0], rotate_rotation.inputs[0])

    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.name = "Rotate Rotation.001"
    rotate_rotation_001.label = ""
    rotate_rotation_001.location = (1550.0, -616.0)
    rotate_rotation_001.bl_label = "Rotate Rotation"
    rotate_rotation_001.rotation_space = "LOCAL"
    # Links for rotate_rotation_001
    links.new(rotate_rotation_001.outputs[0], instance_on_points.inputs[5])
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (1550.0, -736.0)
    random_value.bl_label = "Random Value"
    random_value.data_type = "FLOAT_VECTOR"
    # Min
    random_value.inputs[0].default_value = [-0.10000000149011612, -0.10000000149011612, -0.10000000149011612]
    # Max
    random_value.inputs[1].default_value = [0.10000000149011612, 0.10000000149011612, 0.10000000149011612]
    # Min
    random_value.inputs[2].default_value = 0.0
    # Max
    random_value.inputs[3].default_value = 1.0
    # Min
    random_value.inputs[4].default_value = 0
    # Max
    random_value.inputs[5].default_value = 100
    # Probability
    random_value.inputs[6].default_value = 0.5
    # ID
    random_value.inputs[7].default_value = 0
    # Seed
    random_value.inputs[8].default_value = 2
    # Links for random_value
    links.new(random_value.outputs[0], rotate_rotation_001.inputs[1])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (1890.0, -276.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(instance_on_points.outputs[0], realize_instances.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (2110.0, -156.0)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(switch.outputs[0], join_geometry.inputs[0])
    links.new(realize_instances.outputs[0], switch.inputs[2])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (590.0, -156.0)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002
    links.new(transform_geometry_001.outputs[0], join_geometry_002.inputs[0])
    links.new(transform_geometry.outputs[0], join_geometry_002.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (2010.0, -196.0)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(reroute.outputs[0], switch.inputs[1])
    links.new(join_geometry_002.outputs[0], reroute.inputs[0])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (2110.0, -96.0)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch.inputs[0])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (1170.0, -416.0)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002

    curve_circle_002 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_002.name = "Curve Circle.002"
    curve_circle_002.label = ""
    curve_circle_002.location = (470.0, -496.0)
    curve_circle_002.bl_label = "Curve Circle"
    curve_circle_002.mode = "RADIUS"
    # Resolution
    curve_circle_002.inputs[0].default_value = 105
    # Point 1
    curve_circle_002.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_002.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_002.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_002.inputs[4].default_value = 0.10000000149011612
    # Links for curve_circle_002

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.label = ""
    spline_parameter_001.location = (30.0, -596.0)
    spline_parameter_001.bl_label = "Spline Parameter"
    # Links for spline_parameter_001

    float_curve_001 = nodes.new("ShaderNodeFloatCurve")
    float_curve_001.name = "Float Curve.001"
    float_curve_001.label = ""
    float_curve_001.location = (190.0, -476.0)
    float_curve_001.bl_label = "Float Curve"
    # Factor
    float_curve_001.inputs[0].default_value = 1.0
    # Links for float_curve_001
    links.new(spline_parameter_001.outputs[0], float_curve_001.inputs[1])
    links.new(float_curve_001.outputs[0], curve_to_mesh_002.inputs[2])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (190.0, -256.0)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Count"
    # Count
    resample_curve_001.inputs[3].default_value = 34
    # Length
    resample_curve_001.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_001

    quadratic_bézier_001 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_001.name = "Quadratic Bézier.001"
    quadratic_bézier_001.label = ""
    quadratic_bézier_001.location = (30.0, -256.0)
    quadratic_bézier_001.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_001.inputs[0].default_value = 16
    # Start
    quadratic_bézier_001.inputs[1].default_value = Vector((0.0, -0.009999999776482582, 0.4000000059604645))
    # Middle
    quadratic_bézier_001.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.44999995827674866))
    # End
    quadratic_bézier_001.inputs[3].default_value = Vector((0.0, -0.04999999701976776, 0.5199999809265137))
    # Links for quadratic_bézier_001
    links.new(quadratic_bézier_001.outputs[0], resample_curve_001.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1041.1298828125, -36.0)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Position
    set_position_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_001

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (641.1298828125, -176.0)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 0.0020000000949949026
    # Links for vector_math_002

    noise_texture_001 = nodes.new("ShaderNodeTexNoise")
    noise_texture_001.name = "Noise Texture.001"
    noise_texture_001.label = ""
    noise_texture_001.location = (301.1298828125, -316.0)
    noise_texture_001.bl_label = "Noise Texture"
    noise_texture_001.noise_dimensions = "2D"
    noise_texture_001.noise_type = "FBM"
    noise_texture_001.normalize = False
    # W
    noise_texture_001.inputs[1].default_value = 0.0
    # Scale
    noise_texture_001.inputs[2].default_value = 5.669999599456787
    # Detail
    noise_texture_001.inputs[3].default_value = 0.0
    # Roughness
    noise_texture_001.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture_001.inputs[5].default_value = 2.0
    # Offset
    noise_texture_001.inputs[6].default_value = 0.0
    # Gain
    noise_texture_001.inputs[7].default_value = 1.0
    # Distortion
    noise_texture_001.inputs[8].default_value = 0.0
    # Links for noise_texture_001
    links.new(noise_texture_001.outputs[1], vector_math_002.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (141.12982177734375, -316.0)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "MULTIPLY"
    # Vector
    vector_math_003.inputs[1].default_value = [1.0, 2.5999999046325684, 24.950000762939453]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(vector_math_003.outputs[0], noise_texture_001.inputs[0])

    quadrilateral = nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
    quadrilateral.name = "Quadrilateral"
    quadrilateral.label = ""
    quadrilateral.location = (230.0, -732.0)
    quadrilateral.bl_label = "Quadrilateral"
    quadrilateral.mode = "RECTANGLE"
    # Width
    quadrilateral.inputs[0].default_value = 0.5
    # Height
    quadrilateral.inputs[1].default_value = 0.15000000596046448
    # Bottom Width
    quadrilateral.inputs[2].default_value = 4.0
    # Top Width
    quadrilateral.inputs[3].default_value = 2.0
    # Offset
    quadrilateral.inputs[4].default_value = 1.0
    # Bottom Height
    quadrilateral.inputs[5].default_value = 3.0
    # Top Height
    quadrilateral.inputs[6].default_value = 1.0
    # Point 1
    quadrilateral.inputs[7].default_value = Vector((-1.0, -1.0, 0.0))
    # Point 2
    quadrilateral.inputs[8].default_value = Vector((1.0, -1.0, 0.0))
    # Point 3
    quadrilateral.inputs[9].default_value = Vector((1.0, 1.0, 0.0))
    # Point 4
    quadrilateral.inputs[10].default_value = Vector((-1.0, 1.0, 0.0))
    # Links for quadrilateral

    fillet_curve = nodes.new("GeometryNodeFilletCurve")
    fillet_curve.name = "Fillet Curve"
    fillet_curve.label = ""
    fillet_curve.location = (550.0, -732.0)
    fillet_curve.bl_label = "Fillet Curve"
    # Limit Radius
    fillet_curve.inputs[2].default_value = False
    # Mode
    fillet_curve.inputs[3].default_value = "Bézier"
    # Count
    fillet_curve.inputs[4].default_value = 1
    # Links for fillet_curve

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.label = ""
    set_spline_type.location = (390.0, -732.0)
    set_spline_type.bl_label = "Set Spline Type"
    set_spline_type.spline_type = "BEZIER"
    # Selection
    set_spline_type.inputs[1].default_value = True
    # Links for set_spline_type
    links.new(set_spline_type.outputs[0], fillet_curve.inputs[0])
    links.new(quadrilateral.outputs[0], set_spline_type.inputs[0])

    index_switch = nodes.new("GeometryNodeIndexSwitch")
    index_switch.name = "Index Switch"
    index_switch.label = ""
    index_switch.location = (550.0, -852.0)
    index_switch.bl_label = "Index Switch"
    index_switch.data_type = "FLOAT"
    # 0
    index_switch.inputs[1].default_value = 0.09000000357627869
    # 1
    index_switch.inputs[2].default_value = 0.09000000357627869
    # Links for index_switch
    links.new(index_switch.outputs[0], fillet_curve.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (390.0, -852.0)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], index_switch.inputs[0])

    fill_curve = nodes.new("GeometryNodeFillCurve")
    fill_curve.name = "Fill Curve"
    fill_curve.label = ""
    fill_curve.location = (710.0, -732.0)
    fill_curve.bl_label = "Fill Curve"
    # Group ID
    fill_curve.inputs[1].default_value = 0
    # Mode
    fill_curve.inputs[2].default_value = "N-gons"
    # Links for fill_curve
    links.new(fillet_curve.outputs[0], fill_curve.inputs[0])

    extrude_mesh_002 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_002.name = "Extrude Mesh.002"
    extrude_mesh_002.label = ""
    extrude_mesh_002.location = (890.0, -732.0)
    extrude_mesh_002.bl_label = "Extrude Mesh"
    extrude_mesh_002.mode = "FACES"
    # Selection
    extrude_mesh_002.inputs[1].default_value = True
    # Offset
    extrude_mesh_002.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh_002.inputs[3].default_value = 0.009999999776482582
    # Individual
    extrude_mesh_002.inputs[4].default_value = False
    # Links for extrude_mesh_002
    links.new(fill_curve.outputs[0], extrude_mesh_002.inputs[0])

    flip_faces_002 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.name = "Flip Faces.002"
    flip_faces_002.label = ""
    flip_faces_002.location = (890.0, -632.0)
    flip_faces_002.bl_label = "Flip Faces"
    # Selection
    flip_faces_002.inputs[1].default_value = True
    # Links for flip_faces_002
    links.new(fill_curve.outputs[0], flip_faces_002.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (1070.0, -692.0)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(extrude_mesh_002.outputs[0], join_geometry_004.inputs[0])
    links.new(flip_faces_002.outputs[0], join_geometry_004.inputs[0])

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.name = "Merge by Distance.002"
    merge_by_distance_002.label = ""
    merge_by_distance_002.location = (1070.0, -732.0)
    merge_by_distance_002.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance_002.inputs[1].default_value = True
    # Mode
    merge_by_distance_002.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_002
    links.new(join_geometry_004.outputs[0], merge_by_distance_002.inputs[0])

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    grid.label = ""
    grid.location = (30.0, -332.0)
    grid.bl_label = "Grid"
    # Size X
    grid.inputs[0].default_value = 0.6000000238418579
    # Size Y
    grid.inputs[1].default_value = 0.30000001192092896
    # Vertices X
    grid.inputs[2].default_value = 13
    # Vertices Y
    grid.inputs[3].default_value = 7
    # Links for grid

    extrude_mesh_003 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_003.name = "Extrude Mesh.003"
    extrude_mesh_003.label = ""
    extrude_mesh_003.location = (210.0, -332.0)
    extrude_mesh_003.bl_label = "Extrude Mesh"
    extrude_mesh_003.mode = "FACES"
    # Selection
    extrude_mesh_003.inputs[1].default_value = True
    # Offset
    extrude_mesh_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh_003.inputs[3].default_value = 0.0
    # Individual
    extrude_mesh_003.inputs[4].default_value = True
    # Links for extrude_mesh_003
    links.new(grid.outputs[0], extrude_mesh_003.inputs[0])

    scale_elements = nodes.new("GeometryNodeScaleElements")
    scale_elements.name = "Scale Elements"
    scale_elements.label = ""
    scale_elements.location = (370.0, -332.0)
    scale_elements.bl_label = "Scale Elements"
    scale_elements.domain = "FACE"
    # Scale
    scale_elements.inputs[2].default_value = 0.0
    # Center
    scale_elements.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Scale Mode
    scale_elements.inputs[4].default_value = "Uniform"
    # Axis
    scale_elements.inputs[5].default_value = [1.0, 0.0, 0.0]
    # Links for scale_elements
    links.new(extrude_mesh_003.outputs[0], scale_elements.inputs[0])
    links.new(extrude_mesh_003.outputs[1], scale_elements.inputs[1])

    merge_by_distance_003 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_003.name = "Merge by Distance.003"
    merge_by_distance_003.label = ""
    merge_by_distance_003.location = (530.0, -332.0)
    merge_by_distance_003.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_003.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_003.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_003
    links.new(scale_elements.outputs[0], merge_by_distance_003.inputs[0])
    links.new(extrude_mesh_003.outputs[1], merge_by_distance_003.inputs[1])

    subdivide_mesh = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh.name = "Subdivide Mesh"
    subdivide_mesh.label = ""
    subdivide_mesh.location = (690.0, -332.0)
    subdivide_mesh.bl_label = "Subdivide Mesh"
    # Level
    subdivide_mesh.inputs[1].default_value = 3
    # Links for subdivide_mesh
    links.new(merge_by_distance_003.outputs[0], subdivide_mesh.inputs[0])

    mesh_boolean = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean.name = "Mesh Boolean"
    mesh_boolean.label = ""
    mesh_boolean.location = (1230.0, -332.0)
    mesh_boolean.bl_label = "Mesh Boolean"
    mesh_boolean.operation = "INTERSECT"
    mesh_boolean.solver = "MANIFOLD"
    # Self Intersection
    mesh_boolean.inputs[2].default_value = False
    # Hole Tolerant
    mesh_boolean.inputs[3].default_value = False
    # Links for mesh_boolean
    links.new(merge_by_distance_002.outputs[0], mesh_boolean.inputs[1])

    extrude_mesh_004 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_004.name = "Extrude Mesh.004"
    extrude_mesh_004.label = ""
    extrude_mesh_004.location = (870.0, -332.0)
    extrude_mesh_004.bl_label = "Extrude Mesh"
    extrude_mesh_004.mode = "FACES"
    # Selection
    extrude_mesh_004.inputs[1].default_value = True
    # Offset
    extrude_mesh_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh_004.inputs[3].default_value = 0.009999999776482582
    # Individual
    extrude_mesh_004.inputs[4].default_value = False
    # Links for extrude_mesh_004
    links.new(subdivide_mesh.outputs[0], extrude_mesh_004.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.name = "Flip Faces.003"
    flip_faces_003.label = ""
    flip_faces_003.location = (870.0, -232.0)
    flip_faces_003.bl_label = "Flip Faces"
    # Selection
    flip_faces_003.inputs[1].default_value = True
    # Links for flip_faces_003
    links.new(subdivide_mesh.outputs[0], flip_faces_003.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (1050.0, -292.0)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(extrude_mesh_004.outputs[0], join_geometry_005.inputs[0])
    links.new(flip_faces_003.outputs[0], join_geometry_005.inputs[0])

    merge_by_distance_004 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_004.name = "Merge by Distance.004"
    merge_by_distance_004.label = ""
    merge_by_distance_004.location = (1050.0, -332.0)
    merge_by_distance_004.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance_004.inputs[1].default_value = True
    # Mode
    merge_by_distance_004.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_004.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_004
    links.new(join_geometry_005.outputs[0], merge_by_distance_004.inputs[0])
    links.new(merge_by_distance_004.outputs[0], mesh_boolean.inputs[1])

    delete_geometry_002 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.name = "Delete Geometry.002"
    delete_geometry_002.label = ""
    delete_geometry_002.location = (1390.0, -332.0)
    delete_geometry_002.bl_label = "Delete Geometry"
    delete_geometry_002.mode = "ALL"
    delete_geometry_002.domain = "POINT"
    # Links for delete_geometry_002
    links.new(mesh_boolean.outputs[0], delete_geometry_002.inputs[0])
    links.new(extrude_mesh_004.outputs[1], delete_geometry_002.inputs[1])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (1230.0, -316.0)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Position
    set_position_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_002
    links.new(delete_geometry_002.outputs[0], set_position_002.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (30.0, -36.0)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "EDGES"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (690.0, -112.0)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "EDGE"
    # Links for separate_geometry
    links.new(merge_by_distance_003.outputs[0], separate_geometry.inputs[0])

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.label = ""
    geometry_proximity_001.location = (210.0, -112.0)
    geometry_proximity_001.bl_label = "Geometry Proximity"
    geometry_proximity_001.target_element = "EDGES"
    # Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0
    # Links for geometry_proximity_001
    links.new(grid.outputs[0], geometry_proximity_001.inputs[0])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (370.0, -112.0)
    compare_003.bl_label = "Compare"
    compare_003.operation = "GREATER_THAN"
    compare_003.data_type = "FLOAT"
    compare_003.mode = "ELEMENT"
    # B
    compare_003.inputs[1].default_value = 0.0
    # A
    compare_003.inputs[2].default_value = 0
    # B
    compare_003.inputs[3].default_value = 0
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
    links.new(geometry_proximity_001.outputs[1], compare_003.inputs[0])
    links.new(compare_003.outputs[0], separate_geometry.inputs[1])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (830.0, -36.0)
    combine_x_y_z.bl_label = "Combine XYZ"
    # X
    combine_x_y_z.inputs[0].default_value = 0.0
    # Y
    combine_x_y_z.inputs[1].default_value = 0.0
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], set_position_002.inputs[3])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (190.0, -36.0)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    # From Min
    map_range.inputs[1].default_value = 0.0
    # From Max
    map_range.inputs[2].default_value = 0.009999999776482582
    # To Min
    map_range.inputs[3].default_value = 1.0
    # To Max
    map_range.inputs[4].default_value = 0.0
    # Steps
    map_range.inputs[5].default_value = 4.0
    # Vector
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(geometry_proximity.outputs[1], map_range.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (350.0, -36.0)
    math_002.bl_label = "Math"
    math_002.operation = "POWER"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 2.0
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(map_range.outputs[0], math_002.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (670.0, -36.0)
    math_003.bl_label = "Math"
    math_003.operation = "MULTIPLY"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 0.0020000000949949026
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_003.outputs[0], combine_x_y_z.inputs[2])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (510.0, -36.0)
    math_004.bl_label = "Math"
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    # Value
    math_004.inputs[0].default_value = 1.0
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(math_004.outputs[0], math_003.inputs[0])
    links.new(math_002.outputs[0], math_004.inputs[1])

    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.name = "Curve to Mesh.003"
    curve_to_mesh_003.label = ""
    curve_to_mesh_003.location = (1530.0, -56.0)
    curve_to_mesh_003.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_003.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh_003.inputs[3].default_value = False
    # Links for curve_to_mesh_003

    curve_circle_003 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.name = "Curve Circle.003"
    curve_circle_003.label = ""
    curve_circle_003.location = (770.0, -196.0)
    curve_circle_003.bl_label = "Curve Circle"
    curve_circle_003.mode = "RADIUS"
    # Resolution
    curve_circle_003.inputs[0].default_value = 57
    # Point 1
    curve_circle_003.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_003.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_003.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_003.inputs[4].default_value = 0.004999999888241291
    # Links for curve_circle_003

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    transform_geometry_002.label = ""
    transform_geometry_002.location = (950.0, -196.0)
    transform_geometry_002.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_002.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_002.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_002.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 0.5, 1.0))
    # Links for transform_geometry_002
    links.new(curve_circle_003.outputs[0], transform_geometry_002.inputs[0])

    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.name = "Resample Curve.002"
    resample_curve_002.label = ""
    resample_curve_002.location = (1050.0, -36.0)
    resample_curve_002.bl_label = "Resample Curve"
    resample_curve_002.keep_last_segment = True
    # Selection
    resample_curve_002.inputs[1].default_value = True
    # Mode
    resample_curve_002.inputs[2].default_value = "Length"
    # Count
    resample_curve_002.inputs[3].default_value = 10
    # Length
    resample_curve_002.inputs[4].default_value = 0.009999999776482582
    # Links for resample_curve_002
    links.new(resample_curve_002.outputs[0], curve_to_mesh_003.inputs[0])
    links.new(fillet_curve.outputs[0], resample_curve_002.inputs[0])

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Piping"
    frame_002.location = (180.0, -1616.0)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Quilting"
    frame_003.location = (1560.0, -36.0)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    transform_geometry_003.label = ""
    transform_geometry_003.location = (3010.0, -412.0)
    transform_geometry_003.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_003.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_003.inputs[4].default_value = Vector((1.0, 1.0, -1.0))
    # Links for transform_geometry_003
    links.new(set_position_002.outputs[0], transform_geometry_003.inputs[0])

    flip_faces_004 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_004.name = "Flip Faces.004"
    flip_faces_004.label = ""
    flip_faces_004.location = (3010.0, -332.0)
    flip_faces_004.bl_label = "Flip Faces"
    # Selection
    flip_faces_004.inputs[1].default_value = True
    # Links for flip_faces_004
    links.new(set_position_002.outputs[0], flip_faces_004.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.label = ""
    join_geometry_006.location = (3210.0, -372.0)
    join_geometry_006.bl_label = "Join Geometry"
    # Links for join_geometry_006
    links.new(transform_geometry_003.outputs[0], join_geometry_006.inputs[0])
    links.new(flip_faces_004.outputs[0], join_geometry_006.inputs[0])

    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_007.name = "Join Geometry.007"
    join_geometry_007.label = ""
    join_geometry_007.location = (1130.0, -152.0)
    join_geometry_007.bl_label = "Join Geometry"
    # Links for join_geometry_007
    links.new(join_geometry_007.outputs[0], geometry_proximity.inputs[0])
    links.new(separate_geometry.outputs[0], join_geometry_007.inputs[0])
    links.new(fill_curve.outputs[0], join_geometry_007.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.name = "Set Shade Smooth.001"
    set_shade_smooth_001.label = ""
    set_shade_smooth_001.location = (3390.0, -332.0)
    set_shade_smooth_001.bl_label = "Set Shade Smooth"
    set_shade_smooth_001.domain = "FACE"
    # Selection
    set_shade_smooth_001.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_001.inputs[2].default_value = True
    # Links for set_shade_smooth_001
    links.new(join_geometry_006.outputs[0], set_shade_smooth_001.inputs[0])

    set_shade_smooth_002 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_002.name = "Set Shade Smooth.002"
    set_shade_smooth_002.label = ""
    set_shade_smooth_002.location = (3570.0, -332.0)
    set_shade_smooth_002.bl_label = "Set Shade Smooth"
    set_shade_smooth_002.domain = "EDGE"
    # Shade Smooth
    set_shade_smooth_002.inputs[2].default_value = False
    # Links for set_shade_smooth_002
    links.new(set_shade_smooth_001.outputs[0], set_shade_smooth_002.inputs[0])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (3390.0, -452.0)
    compare_004.bl_label = "Compare"
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    # B
    compare_004.inputs[1].default_value = 0.0
    # A
    compare_004.inputs[2].default_value = 0
    # B
    compare_004.inputs[3].default_value = 0
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
    links.new(geometry_proximity.outputs[1], compare_004.inputs[0])
    links.new(compare_004.outputs[0], set_shade_smooth_002.inputs[1])

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Gambeson Pattern"
    frame_004.location = (30.0, -920.0)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    sample_u_v_surface = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface.name = "Sample UV Surface"
    sample_u_v_surface.label = ""
    sample_u_v_surface.location = (4751.1298828125, -692.0)
    sample_u_v_surface.bl_label = "Sample UV Surface"
    sample_u_v_surface.data_type = "FLOAT_VECTOR"
    # Links for sample_u_v_surface

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.label = ""
    capture_attribute.location = (910.0, -576.0)
    capture_attribute.bl_label = "Capture Attribute"
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    # Links for capture_attribute
    links.new(capture_attribute.outputs[0], curve_to_mesh_002.inputs[1])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (910.0, -376.0)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "POINT"
    # Links for capture_attribute_001
    links.new(capture_attribute_001.outputs[0], curve_to_mesh_002.inputs[0])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"
    spline_parameter_002.label = ""
    spline_parameter_002.location = (450.0, -356.0)
    spline_parameter_002.bl_label = "Spline Parameter"
    # Links for spline_parameter_002
    links.new(spline_parameter_002.outputs[0], capture_attribute_001.inputs[1])
    links.new(spline_parameter_002.outputs[0], capture_attribute.inputs[1])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (1170.0, -576.0)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # Z
    combine_x_y_z_001.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_001
    links.new(capture_attribute_001.outputs[1], combine_x_y_z_001.inputs[1])
    links.new(capture_attribute.outputs[1], combine_x_y_z_001.inputs[0])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    set_spline_cyclic.label = ""
    set_spline_cyclic.location = (650.0, -516.0)
    set_spline_cyclic.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = False
    # Links for set_spline_cyclic
    links.new(set_spline_cyclic.outputs[0], capture_attribute.inputs[0])
    links.new(curve_circle_002.outputs[0], set_spline_cyclic.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    set_curve_tilt.label = ""
    set_curve_tilt.location = (650.0, -236.0)
    set_curve_tilt.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Tilt
    set_curve_tilt.inputs[2].default_value = -1.472708821296692
    # Links for set_curve_tilt
    links.new(set_curve_tilt.outputs[0], capture_attribute_001.inputs[0])
    links.new(resample_curve_001.outputs[0], set_curve_tilt.inputs[0])

    position_005 = nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"
    position_005.label = ""
    position_005.location = (4500.0, -652.0)
    position_005.bl_label = "Position"
    # Links for position_005
    links.new(position_005.outputs[0], sample_u_v_surface.inputs[1])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    set_position_003.label = ""
    set_position_003.location = (5631.1298828125, -892.0)
    set_position_003.bl_label = "Set Position"
    # Selection
    set_position_003.inputs[1].default_value = True
    # Links for set_position_003
    links.new(set_position_003.outputs[0], set_position_001.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    bounding_box.label = ""
    bounding_box.location = (281.1298828125, -96.0)
    bounding_box.bl_label = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = False
    # Links for bounding_box

    position_006 = nodes.new("GeometryNodeInputPosition")
    position_006.name = "Position.006"
    position_006.label = ""
    position_006.location = (30.0, -36.0)
    position_006.bl_label = "Position"
    # Links for position_006

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.label = ""
    map_range_001.location = (481.1298828125, -36.0)
    map_range_001.bl_label = "Map Range"
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT_VECTOR"
    # Value
    map_range_001.inputs[0].default_value = 1.0
    # From Min
    map_range_001.inputs[1].default_value = 0.0
    # From Max
    map_range_001.inputs[2].default_value = 1.0
    # To Min
    map_range_001.inputs[3].default_value = 0.0
    # To Max
    map_range_001.inputs[4].default_value = 1.0
    # Steps
    map_range_001.inputs[5].default_value = 4.0
    # To Min
    map_range_001.inputs[9].default_value = [0.009999999776482582, 0.009999999776482582, 0.009999999776482582]
    # To Max
    map_range_001.inputs[10].default_value = [0.9900000095367432, 0.9900000095367432, 0.9900000095367432]
    # Steps
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_001
    links.new(position_006.outputs[0], map_range_001.inputs[6])
    links.new(bounding_box.outputs[1], map_range_001.inputs[7])
    links.new(bounding_box.outputs[2], map_range_001.inputs[8])
    links.new(map_range_001.outputs[1], sample_u_v_surface.inputs[3])

    sample_u_v_surface_001 = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface_001.name = "Sample UV Surface.001"
    sample_u_v_surface_001.label = ""
    sample_u_v_surface_001.location = (4751.1298828125, -792.0)
    sample_u_v_surface_001.bl_label = "Sample UV Surface"
    sample_u_v_surface_001.data_type = "FLOAT_VECTOR"
    # Links for sample_u_v_surface_001
    links.new(map_range_001.outputs[1], sample_u_v_surface_001.inputs[3])

    normal_003 = nodes.new("GeometryNodeInputNormal")
    normal_003.name = "Normal.003"
    normal_003.label = ""
    normal_003.location = (4500.0, -752.0)
    normal_003.bl_label = "Normal"
    normal_003.legacy_corner_normals = False
    # Links for normal_003
    links.new(normal_003.outputs[0], sample_u_v_surface_001.inputs[1])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_003.name = "Separate XYZ.003"
    separate_x_y_z_003.label = ""
    separate_x_y_z_003.location = (30.0, -80.0)
    separate_x_y_z_003.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_003
    links.new(position_006.outputs[0], separate_x_y_z_003.inputs[0])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (441.1298828125, -40.0)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "SCALE"
    # Vector
    vector_math_004.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_004
    links.new(vector_math_004.outputs[0], set_position_003.inputs[3])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (190.0, -80.0)
    math_005.bl_label = "Math"
    math_005.operation = "MULTIPLY"
    math_005.use_clamp = False
    # Value
    math_005.inputs[1].default_value = 1.2499998807907104
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(separate_x_y_z_003.outputs[2], math_005.inputs[0])
    links.new(math_005.outputs[0], vector_math_004.inputs[3])

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.name = "Capture Attribute.002"
    capture_attribute_002.label = ""
    capture_attribute_002.location = (5091.1298828125, -952.0)
    capture_attribute_002.bl_label = "Capture Attribute"
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "POINT"
    # Links for capture_attribute_002
    links.new(sample_u_v_surface_001.outputs[0], capture_attribute_002.inputs[2])
    links.new(capture_attribute_002.outputs[2], vector_math_004.inputs[0])
    links.new(map_range_001.outputs[1], capture_attribute_002.inputs[3])
    links.new(capture_attribute_002.outputs[3], vector_math_003.inputs[0])
    links.new(sample_u_v_surface.outputs[0], capture_attribute_002.inputs[1])
    links.new(capture_attribute_002.outputs[1], set_position_003.inputs[2])

    noise_texture_002 = nodes.new("ShaderNodeTexNoise")
    noise_texture_002.name = "Noise Texture.002"
    noise_texture_002.label = ""
    noise_texture_002.location = (30.0, -656.0)
    noise_texture_002.bl_label = "Noise Texture"
    noise_texture_002.noise_dimensions = "4D"
    noise_texture_002.noise_type = "FBM"
    noise_texture_002.normalize = False
    # Vector
    noise_texture_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    # W
    noise_texture_002.inputs[1].default_value = 44.769989013671875
    # Scale
    noise_texture_002.inputs[2].default_value = 17.969999313354492
    # Detail
    noise_texture_002.inputs[3].default_value = 0.0
    # Roughness
    noise_texture_002.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture_002.inputs[5].default_value = 2.0
    # Offset
    noise_texture_002.inputs[6].default_value = 0.0
    # Gain
    noise_texture_002.inputs[7].default_value = 1.0
    # Distortion
    noise_texture_002.inputs[8].default_value = 0.0
    # Links for noise_texture_002

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (841.1298828125, -256.0)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "ADD"
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006
    links.new(vector_math_006.outputs[0], set_position_001.inputs[3])
    links.new(vector_math_002.outputs[0], vector_math_006.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (410.0, -536.0)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "SCALE"
    # Vector
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_005.inputs[3].default_value = 0.006000000052154064
    # Links for vector_math_005
    links.new(noise_texture_002.outputs[1], vector_math_005.inputs[0])
    links.new(vector_math_005.outputs[0], vector_math_006.inputs[1])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (7171.1298828125, -712.0)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001
    links.new(store_named_attribute_001.outputs[0], store_named_attribute.inputs[0])

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = "Thickness"
    frame_005.location = (4950.0, -1212.0)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (4420.0, -712.0)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketVector"
    # Links for reroute_001
    links.new(reroute_001.outputs[0], sample_u_v_surface.inputs[2])
    links.new(reroute_001.outputs[0], sample_u_v_surface_001.inputs[2])
    links.new(combine_x_y_z_001.outputs[0], reroute_001.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (4420.0, -672.0)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], sample_u_v_surface.inputs[0])
    links.new(reroute_002.outputs[0], sample_u_v_surface_001.inputs[0])
    links.new(curve_to_mesh_002.outputs[0], reroute_002.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = "UVMap"
    frame_006.location = (4130.0, -896.0)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    frame_007 = nodes.new("NodeFrame")
    frame_007.name = "Frame.007"
    frame_007.label = "General Collar Shape"
    frame_007.location = (2850.0, -36.0)
    frame_007.bl_label = "Frame"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20
    # Links for frame_007

    frame_008 = nodes.new("NodeFrame")
    frame_008.name = "Frame.008"
    frame_008.label = "Displacement"
    frame_008.location = (5730.0, -836.0)
    frame_008.bl_label = "Frame"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20
    # Links for frame_008

    frame_009 = nodes.new("NodeFrame")
    frame_009.name = "Frame.009"
    frame_009.label = "Collar"
    frame_009.location = (-6800.0, -428.0)
    frame_009.bl_label = "Frame"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20
    # Links for frame_009

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (5351.1298828125, -812.0)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "FLOAT2"
    store_named_attribute_002.domain = "CORNER"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute_002
    links.new(store_named_attribute_002.outputs[0], set_position_003.inputs[0])
    links.new(capture_attribute_002.outputs[0], store_named_attribute_002.inputs[0])
    links.new(capture_attribute_002.outputs[3], store_named_attribute_002.inputs[3])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (7011.1298828125, -712.0)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Links for switch_001
    links.new(switch_001.outputs[0], store_named_attribute_001.inputs[0])
    links.new(set_position_001.outputs[0], switch_001.inputs[2])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (6760.0, -632.0)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[0], switch_001.inputs[0])

    curve_to_mesh_004 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_004.name = "Curve to Mesh.004"
    curve_to_mesh_004.label = ""
    curve_to_mesh_004.location = (1170.0, -196.0)
    curve_to_mesh_004.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_004.inputs[3].default_value = False
    # Links for curve_to_mesh_004
    links.new(curve_to_mesh_004.outputs[0], switch_001.inputs[1])
    links.new(set_curve_tilt.outputs[0], curve_to_mesh_004.inputs[0])
    links.new(float_curve_001.outputs[0], curve_to_mesh_004.inputs[2])

    curve_circle_004 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_004.name = "Curve Circle.004"
    curve_circle_004.label = ""
    curve_circle_004.location = (710.0, -36.0)
    curve_circle_004.bl_label = "Curve Circle"
    curve_circle_004.mode = "RADIUS"
    # Resolution
    curve_circle_004.inputs[0].default_value = 24
    # Point 1
    curve_circle_004.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_004.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_004.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_004.inputs[4].default_value = 0.10000000149011612
    # Links for curve_circle_004

    set_spline_cyclic_001 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_001.name = "Set Spline Cyclic.001"
    set_spline_cyclic_001.label = ""
    set_spline_cyclic_001.location = (890.0, -56.0)
    set_spline_cyclic_001.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic_001.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic_001.inputs[2].default_value = False
    # Links for set_spline_cyclic_001
    links.new(curve_circle_004.outputs[0], set_spline_cyclic_001.inputs[0])
    links.new(set_spline_cyclic_001.outputs[0], curve_to_mesh_004.inputs[1])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (570.0, -56.0)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Selection
    mesh_to_curve.inputs[1].default_value = True
    # Links for mesh_to_curve

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (1190.0, -36.0)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Length"
    # Count
    resample_curve.inputs[3].default_value = 101
    # Length
    resample_curve.inputs[4].default_value = 0.003000000026077032
    # Links for resample_curve

    subdivide_mesh_001 = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh_001.name = "Subdivide Mesh.001"
    subdivide_mesh_001.label = ""
    subdivide_mesh_001.location = (30.0, -136.0)
    subdivide_mesh_001.bl_label = "Subdivide Mesh"
    # Level
    subdivide_mesh_001.inputs[1].default_value = 4
    # Links for subdivide_mesh_001
    links.new(separate_geometry.outputs[0], subdivide_mesh_001.inputs[0])

    geometry_proximity_002 = nodes.new("GeometryNodeProximity")
    geometry_proximity_002.name = "Geometry Proximity.002"
    geometry_proximity_002.label = ""
    geometry_proximity_002.location = (30.0, -216.0)
    geometry_proximity_002.bl_label = "Geometry Proximity"
    geometry_proximity_002.target_element = "FACES"
    # Group ID
    geometry_proximity_002.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_002.inputs[3].default_value = 0
    # Links for geometry_proximity_002
    links.new(fill_curve.outputs[0], geometry_proximity_002.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (190.0, -216.0)
    compare.bl_label = "Compare"
    compare.operation = "GREATER_THAN"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.0010000000474974513
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513
    # Links for compare
    links.new(geometry_proximity_002.outputs[1], compare.inputs[0])

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (410.0, -56.0)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "POINT"
    # Links for delete_geometry
    links.new(delete_geometry.outputs[0], mesh_to_curve.inputs[0])
    links.new(subdivide_mesh_001.outputs[0], delete_geometry.inputs[0])
    links.new(compare.outputs[0], delete_geometry.inputs[1])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.label = ""
    instance_on_points_001.location = (1390.0, -36.0)
    instance_on_points_001.bl_label = "Instance on Points"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Links for instance_on_points_001
    links.new(resample_curve.outputs[0], instance_on_points_001.inputs[0])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.label = ""
    align_rotation_to_vector_001.location = (1190.0, -156.0)
    align_rotation_to_vector_001.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_001.axis = "X"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_001.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_001
    links.new(align_rotation_to_vector_001.outputs[0], instance_on_points_001.inputs[5])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (1010.0, -196.0)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_001.inputs[2])

    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.name = "Ico Sphere.001"
    ico_sphere_001.label = ""
    ico_sphere_001.location = (990.0, -296.0)
    ico_sphere_001.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_001.inputs[0].default_value = 0.0007999999797903001
    # Subdivisions
    ico_sphere_001.inputs[1].default_value = 2
    # Links for ico_sphere_001

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    transform_geometry_004.label = ""
    transform_geometry_004.location = (1190.0, -316.0)
    transform_geometry_004.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_004.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_004.inputs[4].default_value = Vector((1.5, 0.5, 0.3199999928474426))
    # Links for transform_geometry_004
    links.new(transform_geometry_004.outputs[0], instance_on_points_001.inputs[2])
    links.new(ico_sphere_001.outputs[0], transform_geometry_004.inputs[0])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.label = ""
    realize_instances_001.location = (1570.0, -36.0)
    realize_instances_001.bl_label = "Realize Instances"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0
    # Links for realize_instances_001
    links.new(instance_on_points_001.outputs[0], realize_instances_001.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (1170.0, -196.0)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position
    links.new(transform_geometry_002.outputs[0], set_position.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (30.0, -536.0)
    position.bl_label = "Position"
    # Links for position

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (190.0, -536.0)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(position.outputs[0], separate_x_y_z.inputs[0])

    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.name = "Map Range.002"
    map_range_002.label = ""
    map_range_002.location = (350.0, -536.0)
    map_range_002.bl_label = "Map Range"
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    # From Min
    map_range_002.inputs[1].default_value = -0.004999999888241291
    # From Max
    map_range_002.inputs[2].default_value = 0.004999999888241291
    # To Min
    map_range_002.inputs[3].default_value = 0.0
    # To Max
    map_range_002.inputs[4].default_value = 1.0
    # Steps
    map_range_002.inputs[5].default_value = 4.0
    # Vector
    map_range_002.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_002.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_002.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_002.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_002.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_002.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_002
    links.new(separate_x_y_z.outputs[0], map_range_002.inputs[0])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (530.0, -536.0)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(map_range_002.outputs[0], float_curve.inputs[1])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (790.0, -536.0)
    math.bl_label = "Math"
    math.operation = "MULTIPLY"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(separate_x_y_z.outputs[1], math.inputs[0])
    links.new(float_curve.outputs[0], math.inputs[1])

    combine_x_y_z_002 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_002.name = "Combine XYZ.002"
    combine_x_y_z_002.label = ""
    combine_x_y_z_002.location = (950.0, -536.0)
    combine_x_y_z_002.bl_label = "Combine XYZ"
    # Links for combine_x_y_z_002
    links.new(separate_x_y_z.outputs[0], combine_x_y_z_002.inputs[0])
    links.new(math.outputs[0], combine_x_y_z_002.inputs[1])
    links.new(separate_x_y_z.outputs[2], combine_x_y_z_002.inputs[2])
    links.new(combine_x_y_z_002.outputs[0], set_position.inputs[2])

    capture_attribute_003 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.name = "Capture Attribute.003"
    capture_attribute_003.label = ""
    capture_attribute_003.location = (1350.0, -196.0)
    capture_attribute_003.bl_label = "Capture Attribute"
    capture_attribute_003.active_index = 0
    capture_attribute_003.domain = "POINT"
    # Links for capture_attribute_003
    links.new(capture_attribute_003.outputs[0], curve_to_mesh_003.inputs[1])
    links.new(set_position.outputs[0], capture_attribute_003.inputs[0])

    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.label = ""
    index_001.location = (1170.0, -396.0)
    index_001.bl_label = "Index"
    # Links for index_001

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.label = ""
    compare_002.location = (1350.0, -436.0)
    compare_002.bl_label = "Compare"
    compare_002.operation = "EQUAL"
    compare_002.data_type = "INT"
    compare_002.mode = "ELEMENT"
    # A
    compare_002.inputs[0].default_value = 0.0
    # B
    compare_002.inputs[1].default_value = 0.0
    # B
    compare_002.inputs[3].default_value = 39
    # A
    compare_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_002.inputs[8].default_value = ""
    # B
    compare_002.inputs[9].default_value = ""
    # C
    compare_002.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_002.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_002.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_002
    links.new(index_001.outputs[0], compare_002.inputs[2])
    links.new(compare_002.outputs[0], capture_attribute_003.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (1730.0, -96.0)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Links for mesh_to_curve_001
    links.new(curve_to_mesh_003.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(capture_attribute_003.outputs[1], mesh_to_curve_001.inputs[1])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (830.0, -76.0)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(mesh_to_curve_001.outputs[0], join_geometry_001.inputs[0])
    links.new(mesh_to_curve.outputs[0], join_geometry_001.inputs[0])
    links.new(join_geometry_001.outputs[0], resample_curve.inputs[0])

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_008.name = "Join Geometry.008"
    join_geometry_008.label = ""
    join_geometry_008.location = (3570.0, -1492.0)
    join_geometry_008.bl_label = "Join Geometry"
    # Links for join_geometry_008

    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.name = "Set Shade Smooth.003"
    set_shade_smooth_003.label = ""
    set_shade_smooth_003.location = (3390.0, -612.0)
    set_shade_smooth_003.bl_label = "Set Shade Smooth"
    set_shade_smooth_003.domain = "FACE"
    # Selection
    set_shade_smooth_003.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_003.inputs[2].default_value = True
    # Links for set_shade_smooth_003
    links.new(join_geometry_008.outputs[0], set_shade_smooth_003.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_009.name = "Join Geometry.009"
    join_geometry_009.label = ""
    join_geometry_009.location = (3750.0, -372.0)
    join_geometry_009.bl_label = "Join Geometry"
    # Links for join_geometry_009
    links.new(join_geometry_009.outputs[0], bounding_box.inputs[0])
    links.new(join_geometry_009.outputs[0], capture_attribute_002.inputs[0])
    links.new(set_shade_smooth_002.outputs[0], join_geometry_009.inputs[0])
    links.new(set_shade_smooth_003.outputs[0], join_geometry_009.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Stitching"
    frame.location = (1200.0, -876.0)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (1750.0, -36.0)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "stitching"
    # Value
    store_named_attribute_003.inputs[3].default_value = True
    # Links for store_named_attribute_003
    links.new(store_named_attribute_003.outputs[0], join_geometry_008.inputs[0])
    links.new(realize_instances_001.outputs[0], store_named_attribute_003.inputs[0])

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (3190.0, -1492.0)
    store_named_attribute_004.bl_label = "Store Named Attribute"
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "piping"
    # Value
    store_named_attribute_004.inputs[3].default_value = True
    # Links for store_named_attribute_004
    links.new(store_named_attribute_004.outputs[0], join_geometry_008.inputs[0])
    links.new(curve_to_mesh_003.outputs[0], store_named_attribute_004.inputs[0])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.label = ""
    random_value_001.location = (1390.0, -296.0)
    random_value_001.bl_label = "Random Value"
    random_value_001.data_type = "FLOAT_VECTOR"
    # Min
    random_value_001.inputs[0].default_value = [0.699999988079071, 0.699999988079071, 0.699999988079071]
    # Max
    random_value_001.inputs[1].default_value = [1.0, 1.5, 1.2999999523162842]
    # Min
    random_value_001.inputs[2].default_value = 0.0
    # Max
    random_value_001.inputs[3].default_value = 1.0
    # Min
    random_value_001.inputs[4].default_value = 0
    # Max
    random_value_001.inputs[5].default_value = 100
    # Probability
    random_value_001.inputs[6].default_value = 0.5
    # ID
    random_value_001.inputs[7].default_value = 0
    # Seed
    random_value_001.inputs[8].default_value = 0
    # Links for random_value_001
    links.new(random_value_001.outputs[0], instance_on_points_001.inputs[6])

    # Parent assignments
    store_named_attribute.parent = frame_009
    ico_sphere.parent = frame_001
    transform_geometry.parent = frame_001
    transform_geometry_001.parent = frame_001
    mesh_to_s_d_f_grid.parent = frame_001
    mesh_to_s_d_f_grid_001.parent = frame_001
    s_d_f_grid_boolean.parent = frame_001
    grid_to_mesh.parent = frame_001
    s_d_f_grid_fillet.parent = frame_001
    instance_on_points.parent = frame_001
    curve_circle_001.parent = frame_001
    curve_to_mesh_001.parent = frame_001
    position_002.parent = frame_001
    separate_x_y_z_001.parent = frame_001
    compare_001.parent = frame_001
    align_rotation_to_vector.parent = frame_001
    normal_001.parent = frame_001
    rotate_rotation.parent = frame_001
    rotate_rotation_001.parent = frame_001
    random_value.parent = frame_001
    realize_instances.parent = frame_001
    switch.parent = frame_001
    join_geometry_002.parent = frame_001
    reroute.parent = frame_001
    group_input.parent = frame_001
    curve_to_mesh_002.parent = frame_007
    curve_circle_002.parent = frame_007
    spline_parameter_001.parent = frame_007
    float_curve_001.parent = frame_007
    resample_curve_001.parent = frame_007
    quadratic_bézier_001.parent = frame_007
    set_position_001.parent = frame_008
    vector_math_002.parent = frame_008
    noise_texture_001.parent = frame_008
    vector_math_003.parent = frame_008
    quadrilateral.parent = frame_004
    fillet_curve.parent = frame_004
    set_spline_type.parent = frame_004
    index_switch.parent = frame_004
    index.parent = frame_004
    fill_curve.parent = frame_004
    extrude_mesh_002.parent = frame_004
    flip_faces_002.parent = frame_004
    join_geometry_004.parent = frame_004
    merge_by_distance_002.parent = frame_004
    grid.parent = frame_004
    extrude_mesh_003.parent = frame_004
    scale_elements.parent = frame_004
    merge_by_distance_003.parent = frame_004
    subdivide_mesh.parent = frame_004
    mesh_boolean.parent = frame_004
    extrude_mesh_004.parent = frame_004
    flip_faces_003.parent = frame_004
    join_geometry_005.parent = frame_004
    merge_by_distance_004.parent = frame_004
    delete_geometry_002.parent = frame_004
    set_position_002.parent = frame_003
    geometry_proximity.parent = frame_003
    separate_geometry.parent = frame_004
    geometry_proximity_001.parent = frame_004
    compare_003.parent = frame_004
    combine_x_y_z.parent = frame_003
    map_range.parent = frame_003
    math_002.parent = frame_003
    math_003.parent = frame_003
    math_004.parent = frame_003
    curve_to_mesh_003.parent = frame_002
    curve_circle_003.parent = frame_002
    transform_geometry_002.parent = frame_002
    resample_curve_002.parent = frame_002
    frame_002.parent = frame_004
    frame_003.parent = frame_004
    transform_geometry_003.parent = frame_004
    flip_faces_004.parent = frame_004
    join_geometry_006.parent = frame_004
    join_geometry_007.parent = frame_004
    set_shade_smooth_001.parent = frame_004
    set_shade_smooth_002.parent = frame_004
    compare_004.parent = frame_004
    frame_004.parent = frame_009
    sample_u_v_surface.parent = frame_009
    capture_attribute.parent = frame_007
    capture_attribute_001.parent = frame_007
    spline_parameter_002.parent = frame_007
    combine_x_y_z_001.parent = frame_007
    set_spline_cyclic.parent = frame_007
    set_curve_tilt.parent = frame_007
    position_005.parent = frame_009
    set_position_003.parent = frame_009
    bounding_box.parent = frame_006
    position_006.parent = frame_006
    map_range_001.parent = frame_006
    sample_u_v_surface_001.parent = frame_009
    normal_003.parent = frame_009
    separate_x_y_z_003.parent = frame_005
    vector_math_004.parent = frame_005
    math_005.parent = frame_005
    capture_attribute_002.parent = frame_009
    noise_texture_002.parent = frame_008
    vector_math_006.parent = frame_008
    vector_math_005.parent = frame_008
    store_named_attribute_001.parent = frame_009
    frame_005.parent = frame_009
    reroute_001.parent = frame_009
    reroute_002.parent = frame_009
    frame_006.parent = frame_009
    frame_007.parent = frame_009
    frame_008.parent = frame_009
    store_named_attribute_002.parent = frame_009
    switch_001.parent = frame_009
    group_input_001.parent = frame_009
    curve_to_mesh_004.parent = frame_007
    curve_circle_004.parent = frame_007
    set_spline_cyclic_001.parent = frame_007
    mesh_to_curve.parent = frame
    resample_curve.parent = frame
    subdivide_mesh_001.parent = frame
    geometry_proximity_002.parent = frame
    compare.parent = frame
    delete_geometry.parent = frame
    instance_on_points_001.parent = frame
    align_rotation_to_vector_001.parent = frame
    curve_tangent.parent = frame
    ico_sphere_001.parent = frame
    transform_geometry_004.parent = frame
    realize_instances_001.parent = frame
    set_position.parent = frame_002
    position.parent = frame_002
    separate_x_y_z.parent = frame_002
    map_range_002.parent = frame_002
    float_curve.parent = frame_002
    math.parent = frame_002
    combine_x_y_z_002.parent = frame_002
    capture_attribute_003.parent = frame_002
    index_001.parent = frame_002
    compare_002.parent = frame_002
    mesh_to_curve_001.parent = frame_002
    join_geometry_001.parent = frame
    join_geometry_008.parent = frame_004
    set_shade_smooth_003.parent = frame_004
    join_geometry_009.parent = frame_004
    frame.parent = frame_004
    store_named_attribute_003.parent = frame
    store_named_attribute_004.parent = frame_004
    random_value_001.parent = frame

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_waist_group():
    group_name = "Waist"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (10900.0, 640.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    bi-_rail_loft = nodes.new("GeometryNodeGroup")
    bi-_rail_loft.name = "Bi-Rail Loft"
    bi-_rail_loft.label = ""
    bi-_rail_loft.location = (-820.0, -1320.0)
    bi-_rail_loft.node_tree = create_bi-_rail__loft_group()
    bi-_rail_loft.bl_label = "Group"
    # Smoothing
    bi-_rail_loft.inputs[3].default_value = 0
    # Menu
    bi-_rail_loft.inputs[4].default_value = "Resolution"
    # X Spacing
    bi-_rail_loft.inputs[5].default_value = 0.009999999776482582
    # Y Spacing
    bi-_rail_loft.inputs[6].default_value = 0.029999999329447746
    # X Resolution
    bi-_rail_loft.inputs[7].default_value = 14
    # Y Resolution
    bi-_rail_loft.inputs[8].default_value = 9
    # Links for bi-_rail_loft

    bézier_segment = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment.name = "Bézier Segment"
    bézier_segment.label = ""
    bézier_segment.location = (29.0, -35.800018310546875)
    bézier_segment.bl_label = "Bézier Segment"
    bézier_segment.mode = "OFFSET"
    # Resolution
    bézier_segment.inputs[0].default_value = 200
    # Start
    bézier_segment.inputs[1].default_value = Vector((0.0, -0.14000000059604645, 0.07000000029802322))
    # Start Handle
    bézier_segment.inputs[2].default_value = Vector((0.0, 0.0, -0.019999999552965164))
    # End Handle
    bézier_segment.inputs[3].default_value = Vector((0.0, 0.0, 0.07999999821186066))
    # End
    bézier_segment.inputs[4].default_value = Vector((0.0, -0.18999998271465302, -0.049999989569187164))
    # Links for bézier_segment

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Centre Line"
    frame.location = (29.0, -35.79998779296875)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    bézier_segment_001 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_001.name = "Bézier Segment.001"
    bézier_segment_001.label = ""
    bézier_segment_001.location = (29.0, -35.79998779296875)
    bézier_segment_001.bl_label = "Bézier Segment"
    bézier_segment_001.mode = "OFFSET"
    # Resolution
    bézier_segment_001.inputs[0].default_value = 200
    # Start
    bézier_segment_001.inputs[1].default_value = Vector((-0.14999999105930328, 0.0, 0.07000000029802322))
    # Start Handle
    bézier_segment_001.inputs[2].default_value = Vector((0.0, 0.0, -0.029999999329447746))
    # End Handle
    bézier_segment_001.inputs[3].default_value = Vector((0.0, 0.0, 0.04999999701976776))
    # End
    bézier_segment_001.inputs[4].default_value = Vector((-0.1899999976158142, 0.0, -0.029999990016222))
    # Links for bézier_segment_001

    join_splines = nodes.new("GeometryNodeGroup")
    join_splines.name = "Group"
    join_splines.label = ""
    join_splines.location = (769.0, -55.79998779296875)
    join_splines.node_tree = create_join__splines_group()
    join_splines.bl_label = "Group"
    # Links for join_splines
    links.new(join_splines.outputs[0], bi-_rail_loft.inputs[1])

    join_splines_1 = nodes.new("GeometryNodeGroup")
    join_splines_1.name = "Group.001"
    join_splines_1.label = ""
    join_splines_1.location = (618.0, -131.60000610351562)
    join_splines_1.node_tree = create_join__splines_group()
    join_splines_1.bl_label = "Group"
    # Links for join_splines_1
    links.new(join_splines_1.outputs[0], bi-_rail_loft.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "Outside"
    frame_001.location = (29.0, -651.6000366210938)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Centre"
    frame_002.location = (180.0, -35.800018310546875)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Rails"
    frame_003.location = (-2358.0, -352.5999755859375)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    quadratic_bézier = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier.name = "Quadratic Bézier"
    quadratic_bézier.label = ""
    quadratic_bézier.location = (29.0, -55.7999267578125)
    quadratic_bézier.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier.inputs[0].default_value = 40
    # Start
    quadratic_bézier.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier.inputs[2].default_value = Vector((0.0, -0.6000000238418579, -0.1199999749660492))
    # End
    quadratic_bézier.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (889.0, -35.7999267578125)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002
    links.new(join_geometry_002.outputs[0], bi-_rail_loft.inputs[2])
    links.new(quadratic_bézier.outputs[0], join_geometry_002.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Profiles"
    frame_004.location = (-2329.0, -1724.2000732421875)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    quadratic_bézier_005 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_005.name = "Quadratic Bézier.005"
    quadratic_bézier_005.label = ""
    quadratic_bézier_005.location = (549.0, -175.7999267578125)
    quadratic_bézier_005.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_005.inputs[0].default_value = 40
    # Start
    quadratic_bézier_005.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier_005.inputs[2].default_value = Vector((-2.2351741790771484e-08, -0.7599999308586121, 0.25999999046325684))
    # End
    quadratic_bézier_005.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier_005
    links.new(quadratic_bézier_005.outputs[0], join_geometry_002.inputs[0])

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (9740.0, 240.0)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.0))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, -0.7799999713897705, 1.0))
    # Links for transform_geometry

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (10140.0, 320.0)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.name = "Flip Faces"
    flip_faces.label = ""
    flip_faces.location = (9920.0, 240.0)
    flip_faces.bl_label = "Flip Faces"
    # Selection
    flip_faces.inputs[1].default_value = True
    # Links for flip_faces
    links.new(flip_faces.outputs[0], join_geometry_003.inputs[0])
    links.new(transform_geometry.outputs[0], flip_faces.inputs[0])

    reverse_curve = nodes.new("GeometryNodeReverseCurve")
    reverse_curve.name = "Reverse Curve"
    reverse_curve.label = ""
    reverse_curve.location = (338.0, -91.60000610351562)
    reverse_curve.bl_label = "Reverse Curve"
    # Selection
    reverse_curve.inputs[1].default_value = True
    # Links for reverse_curve
    links.new(reverse_curve.outputs[0], join_splines_1.inputs[0])
    links.new(bézier_segment.outputs[0], reverse_curve.inputs[0])

    reverse_curve_001 = nodes.new("GeometryNodeReverseCurve")
    reverse_curve_001.name = "Reverse Curve.001"
    reverse_curve_001.label = ""
    reverse_curve_001.location = (529.0, -55.79998779296875)
    reverse_curve_001.bl_label = "Reverse Curve"
    # Selection
    reverse_curve_001.inputs[1].default_value = True
    # Links for reverse_curve_001
    links.new(reverse_curve_001.outputs[0], join_splines.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (249.0, -55.79998779296875)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.004999999888241291, 0.0))
    # Rotation
    transform_geometry_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_001
    links.new(transform_geometry_001.outputs[0], reverse_curve_001.inputs[0])
    links.new(bézier_segment_001.outputs[0], transform_geometry_001.inputs[0])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.name = "Pipes"
    pipes.label = ""
    pipes.location = (829.0, -35.79998779296875)
    pipes.node_tree = create_pipes_group()
    pipes.bl_label = "Group"
    # Links for pipes

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (1320.0, -1100.0)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(pipes.outputs[0], join_geometry_005.inputs[0])

    quadratic_bézier_006 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_006.name = "Quadratic Bézier.006"
    quadratic_bézier_006.label = ""
    quadratic_bézier_006.location = (309.0, -135.7999267578125)
    quadratic_bézier_006.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_006.inputs[0].default_value = 40
    # Start
    quadratic_bézier_006.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier_006.inputs[2].default_value = Vector((-0.18000002205371857, -0.6399999260902405, 0.31999996304512024))
    # End
    quadratic_bézier_006.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier_006
    links.new(quadratic_bézier_006.outputs[0], join_geometry_002.inputs[0])

    closure_input = nodes.new("NodeClosureInput")
    closure_input.name = "Closure Input"
    closure_input.label = ""
    closure_input.location = (-1140.0, -1780.0)
    closure_input.bl_label = "Closure Input"
    # Links for closure_input

    closure_output = nodes.new("NodeClosureOutput")
    closure_output.name = "Closure Output"
    closure_output.label = ""
    closure_output.location = (-680.0, -1780.0)
    closure_output.bl_label = "Closure Output"
    closure_output.active_input_index = 0
    closure_output.active_output_index = 0
    closure_output.define_signature = False
    # Links for closure_output
    links.new(closure_output.outputs[0], bi-_rail_loft.inputs[9])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (-960.0, -1800.0)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(float_curve.outputs[0], closure_output.inputs[0])
    links.new(closure_input.outputs[0], float_curve.inputs[1])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.label = ""
    extrude_mesh.location = (-60.0, -1300.0)
    extrude_mesh.bl_label = "Extrude Mesh"
    extrude_mesh.mode = "FACES"
    # Offset
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.0020000000949949026
    # Individual
    extrude_mesh.inputs[4].default_value = False
    # Links for extrude_mesh

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (-480.0, -1440.0)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(bi-_rail_loft.outputs[2], separate_x_y_z.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (-300.0, -1500.0)
    compare_001.bl_label = "Compare"
    compare_001.operation = "GREATER_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = 0.5999999642372131
    # A
    compare_001.inputs[2].default_value = 0
    # B
    compare_001.inputs[3].default_value = 0
    # A
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_001.inputs[8].default_value = ""
    # B
    compare_001.inputs[9].default_value = ""
    # C
    compare_001.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_001.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_001.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_001
    links.new(separate_x_y_z.outputs[1], compare_001.inputs[0])
    links.new(compare_001.outputs[0], extrude_mesh.inputs[1])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.name = "Separate Geometry.001"
    separate_geometry_001.label = ""
    separate_geometry_001.location = (320.0, -1280.0)
    separate_geometry_001.bl_label = "Separate Geometry"
    separate_geometry_001.domain = "FACE"
    # Links for separate_geometry_001
    links.new(separate_geometry_001.outputs[1], join_geometry_005.inputs[0])
    links.new(extrude_mesh.outputs[0], separate_geometry_001.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (140.0, -1380.0)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "OR"
    # Links for boolean_math
    links.new(boolean_math.outputs[0], separate_geometry_001.inputs[1])
    links.new(extrude_mesh.outputs[1], boolean_math.inputs[0])
    links.new(extrude_mesh.outputs[2], boolean_math.inputs[1])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (680.0, -1240.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(separate_geometry_001.outputs[0], store_named_attribute.inputs[0])
    links.new(store_named_attribute.outputs[0], join_geometry_005.inputs[0])

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.name = "Gold on Band"
    gold_on_band.label = ""
    gold_on_band.location = (478.0, -944.7999267578125)
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.bl_label = "Group"
    # Density
    gold_on_band.inputs[1].default_value = 100000.0
    # W
    gold_on_band.inputs[2].default_value = 1.5699999332427979
    # Seed
    gold_on_band.inputs[3].default_value = 1
    # Links for gold_on_band
    links.new(separate_geometry_001.outputs[0], gold_on_band.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.label = ""
    join_geometry_006.location = (2758.0, -764.7999267578125)
    join_geometry_006.bl_label = "Join Geometry"
    # Links for join_geometry_006
    links.new(gold_on_band.outputs[0], join_geometry_006.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (9840.0, 560.0)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(switch.outputs[0], join_geometry_003.inputs[0])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (9840.0, 620.0)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch.inputs[0])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.name = "Separate Geometry.002"
    separate_geometry_002.label = ""
    separate_geometry_002.location = (669.0, -35.79998779296875)
    separate_geometry_002.bl_label = "Separate Geometry"
    separate_geometry_002.domain = "EDGE"
    # Links for separate_geometry_002
    links.new(extrude_mesh.outputs[0], separate_geometry_002.inputs[0])
    links.new(separate_geometry_002.outputs[0], pipes.inputs[0])

    edge_vertices = nodes.new("GeometryNodeInputMeshEdgeVertices")
    edge_vertices.name = "Edge Vertices"
    edge_vertices.label = ""
    edge_vertices.location = (29.0, -35.79998779296875)
    edge_vertices.bl_label = "Edge Vertices"
    # Links for edge_vertices

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (189.0, -35.79998779296875)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "SUBTRACT"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(edge_vertices.outputs[3], vector_math.inputs[0])
    links.new(edge_vertices.outputs[2], vector_math.inputs[1])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.label = ""
    compare_002.location = (349.0, -35.79998779296875)
    compare_002.bl_label = "Compare"
    compare_002.operation = "EQUAL"
    compare_002.data_type = "VECTOR"
    compare_002.mode = "DIRECTION"
    # A
    compare_002.inputs[0].default_value = 0.0
    # B
    compare_002.inputs[1].default_value = 0.0
    # A
    compare_002.inputs[2].default_value = 0
    # B
    compare_002.inputs[3].default_value = 0
    # B
    compare_002.inputs[5].default_value = [0.0, 0.0, 1.0]
    # A
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_002.inputs[8].default_value = ""
    # B
    compare_002.inputs[9].default_value = ""
    # C
    compare_002.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_002.inputs[11].default_value = 1.5707963705062866
    # Epsilon
    compare_002.inputs[12].default_value = 0.3109999895095825
    # Links for compare_002
    links.new(vector_math.outputs[0], compare_002.inputs[4])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.label = ""
    boolean_math_001.location = (509.0, -35.79998779296875)
    boolean_math_001.bl_label = "Boolean Math"
    boolean_math_001.operation = "AND"
    # Links for boolean_math_001
    links.new(compare_002.outputs[0], boolean_math_001.inputs[0])
    links.new(boolean_math_001.outputs[0], separate_geometry_002.inputs[1])
    links.new(extrude_mesh.outputs[1], boolean_math_001.inputs[1])

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = "Pipes"
    frame_005.location = (-409.0, -884.2000122070312)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (1009.0, -189.0)
    instance_on_points.bl_label = "Instance on Points"
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Links for instance_on_points

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.name = "Gem in Holder"
    gem_in_holder.label = ""
    gem_in_holder.location = (169.0, -409.0)
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.bl_label = "Group"
    # Gem Radius
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder.inputs[2].default_value = True
    # Scale
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder.inputs[4].default_value = 20
    # Seed
    gem_in_holder.inputs[5].default_value = 10
    # Wings
    gem_in_holder.inputs[6].default_value = False
    # Array Count
    gem_in_holder.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder.inputs[8].default_value = 10
    # Split
    gem_in_holder.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder.inputs[10].default_value = 2.5099997520446777
    # Links for gem_in_holder
    links.new(gem_in_holder.outputs[0], instance_on_points.inputs[2])

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (189.0, -29.0)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.label = ""
    capture_attribute.location = (-380.0, -1320.0)
    capture_attribute.bl_label = "Capture Attribute"
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    # Links for capture_attribute
    links.new(capture_attribute.outputs[0], extrude_mesh.inputs[0])
    links.new(capture_attribute.outputs[1], separate_x_y_z_001.inputs[0])
    links.new(bi-_rail_loft.outputs[0], capture_attribute.inputs[0])
    links.new(bi-_rail_loft.outputs[2], capture_attribute.inputs[1])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (349.0, -29.0)
    compare.bl_label = "Compare"
    compare.operation = "GREATER_THAN"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.6800000071525574
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513
    # Links for compare
    links.new(separate_x_y_z_001.outputs[1], compare.inputs[0])
    links.new(compare.outputs[0], instance_on_points.inputs[1])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.label = ""
    align_rotation_to_vector.location = (549.0, -269.0)
    align_rotation_to_vector.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector.axis = "Z"
    align_rotation_to_vector.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector
    links.new(align_rotation_to_vector.outputs[0], instance_on_points.inputs[5])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (549.0, -409.0)
    random_value.bl_label = "Random Value"
    random_value.data_type = "FLOAT"
    # Min
    random_value.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value.inputs[2].default_value = -0.09999999403953552
    # Max
    random_value.inputs[3].default_value = 0.09999993443489075
    # Min
    random_value.inputs[4].default_value = 0
    # Max
    random_value.inputs[5].default_value = 100
    # Probability
    random_value.inputs[6].default_value = 0.5
    # ID
    random_value.inputs[7].default_value = 0
    # Seed
    random_value.inputs[8].default_value = 0
    # Links for random_value

    separate_geometry_003 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_003.name = "Separate Geometry.003"
    separate_geometry_003.label = ""
    separate_geometry_003.location = (29.0, -189.0)
    separate_geometry_003.bl_label = "Separate Geometry"
    separate_geometry_003.domain = "FACE"
    # Links for separate_geometry_003
    links.new(extrude_mesh.outputs[0], separate_geometry_003.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry_003.inputs[1])

    mesh_to_points = nodes.new("GeometryNodeMeshToPoints")
    mesh_to_points.name = "Mesh to Points"
    mesh_to_points.label = ""
    mesh_to_points.location = (349.0, -189.0)
    mesh_to_points.bl_label = "Mesh to Points"
    mesh_to_points.mode = "FACES"
    # Selection
    mesh_to_points.inputs[1].default_value = True
    # Position
    mesh_to_points.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Radius
    mesh_to_points.inputs[3].default_value = 0.05000000074505806
    # Links for mesh_to_points
    links.new(mesh_to_points.outputs[0], instance_on_points.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.label = ""
    normal.location = (189.0, -309.0)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = False
    # Links for normal

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (189.0, -189.0)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 1
    capture_attribute_001.domain = "FACE"
    # Links for capture_attribute_001
    links.new(capture_attribute_001.outputs[0], mesh_to_points.inputs[0])
    links.new(separate_geometry_003.outputs[0], capture_attribute_001.inputs[0])
    links.new(normal.outputs[0], capture_attribute_001.inputs[1])
    links.new(capture_attribute_001.outputs[1], align_rotation_to_vector.inputs[2])
    links.new(bi-_rail_loft.outputs[2], capture_attribute_001.inputs[2])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (1349.0, -169.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_002.name = "Separate XYZ.002"
    separate_x_y_z_002.label = ""
    separate_x_y_z_002.location = (409.0, -589.0)
    separate_x_y_z_002.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_002
    links.new(capture_attribute_001.outputs[2], separate_x_y_z_002.inputs[0])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (569.0, -589.0)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    # From Min
    map_range.inputs[1].default_value = 0.0
    # From Max
    map_range.inputs[2].default_value = 1.0
    # To Min
    map_range.inputs[3].default_value = 0.46000003814697266
    # To Max
    map_range.inputs[4].default_value = 0.28999999165534973
    # Steps
    map_range.inputs[5].default_value = 4.0
    # Vector
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(separate_x_y_z_002.outputs[0], map_range.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (789.0, -469.0)
    math.bl_label = "Math"
    math.operation = "ADD"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(map_range.outputs[0], math.inputs[0])
    links.new(random_value.outputs[1], math.inputs[1])
    links.new(math.outputs[0], instance_on_points.inputs[6])

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.name = "Capture Attribute.002"
    capture_attribute_002.label = ""
    capture_attribute_002.location = (1189.0, -189.0)
    capture_attribute_002.bl_label = "Capture Attribute"
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "INSTANCE"
    # Links for capture_attribute_002
    links.new(capture_attribute_002.outputs[0], realize_instances.inputs[0])
    links.new(instance_on_points.outputs[0], capture_attribute_002.inputs[0])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (1189.0, -309.0)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], capture_attribute_002.inputs[1])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (10720.0, 660.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True
    # Links for set_shade_smooth
    links.new(set_shade_smooth.outputs[0], group_output.inputs[0])
    links.new(join_geometry_003.outputs[0], set_shade_smooth.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = "Gold"
    frame_006.location = (1082.0, 1264.7999267578125)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (429.0, -35.7999267578125)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "FACE"
    # Links for delete_geometry
    links.new(join_geometry_005.outputs[0], delete_geometry.inputs[0])

    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_007.name = "Join Geometry.007"
    join_geometry_007.label = ""
    join_geometry_007.location = (9500.0, 320.0)
    join_geometry_007.bl_label = "Join Geometry"
    # Links for join_geometry_007
    links.new(join_geometry_007.outputs[0], transform_geometry.inputs[0])
    links.new(join_geometry_007.outputs[0], join_geometry_003.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (29.0, -195.7999267578125)
    position.bl_label = "Position"
    # Links for position

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_003.name = "Separate XYZ.003"
    separate_x_y_z_003.label = ""
    separate_x_y_z_003.location = (29.0, -255.7999267578125)
    separate_x_y_z_003.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_003
    links.new(position.outputs[0], separate_x_y_z_003.inputs[0])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (189.0, -255.7999267578125)
    compare_003.bl_label = "Compare"
    compare_003.operation = "EQUAL"
    compare_003.data_type = "FLOAT"
    compare_003.mode = "ELEMENT"
    # B
    compare_003.inputs[1].default_value = 0.0
    # A
    compare_003.inputs[2].default_value = 0
    # B
    compare_003.inputs[3].default_value = 0
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
    links.new(separate_x_y_z_003.outputs[0], compare_003.inputs[0])
    links.new(compare_003.outputs[0], delete_geometry.inputs[1])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (789.0, -55.7999267578125)
    set_position.bl_label = "Set Position"
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position
    links.new(set_position.outputs[0], join_geometry_007.inputs[0])
    links.new(delete_geometry.outputs[0], set_position.inputs[0])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (369.0, -255.7999267578125)
    compare_004.bl_label = "Compare"
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    # B
    compare_004.inputs[1].default_value = 0.0
    # A
    compare_004.inputs[2].default_value = 0
    # B
    compare_004.inputs[3].default_value = 0
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
    links.new(separate_x_y_z_003.outputs[0], compare_004.inputs[0])
    links.new(compare_004.outputs[0], set_position.inputs[1])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (569.0, -295.7999267578125)
    position_001.bl_label = "Position"
    # Links for position_001

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (789.0, -295.7999267578125)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "MULTIPLY"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 1.0, 1.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(position_001.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], set_position.inputs[2])

    frame_007 = nodes.new("NodeFrame")
    frame_007.name = "Frame.007"
    frame_007.label = "Merge Centre Line"
    frame_007.location = (1811.0, -1084.2000732421875)
    frame_007.bl_label = "Frame"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20
    # Links for frame_007

    separate_geometry_004 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_004.name = "Separate Geometry.004"
    separate_geometry_004.label = ""
    separate_geometry_004.location = (349.0, -35.800048828125)
    separate_geometry_004.bl_label = "Separate Geometry"
    separate_geometry_004.domain = "EDGE"
    # Links for separate_geometry_004
    links.new(separate_geometry_002.outputs[0], separate_geometry_004.inputs[0])

    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_004.name = "Separate XYZ.004"
    separate_x_y_z_004.label = ""
    separate_x_y_z_004.location = (29.0, -135.800048828125)
    separate_x_y_z_004.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_004
    links.new(capture_attribute.outputs[1], separate_x_y_z_004.inputs[0])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (189.0, -135.800048828125)
    compare_005.bl_label = "Compare"
    compare_005.operation = "EQUAL"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    # B
    compare_005.inputs[1].default_value = 0.8700000047683716
    # A
    compare_005.inputs[2].default_value = 0
    # B
    compare_005.inputs[3].default_value = 0
    # A
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_005.inputs[8].default_value = ""
    # B
    compare_005.inputs[9].default_value = ""
    # C
    compare_005.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_005.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_005.inputs[12].default_value = 0.09099999070167542
    # Links for compare_005
    links.new(separate_x_y_z_004.outputs[1], compare_005.inputs[0])
    links.new(compare_005.outputs[0], separate_geometry_004.inputs[1])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    transform_geometry_002.label = ""
    transform_geometry_002.location = (529.0, -95.800048828125)
    transform_geometry_002.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_002.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_002.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.0))
    # Rotation
    transform_geometry_002.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_002.inputs[4].default_value = Vector((1.0, -0.7799999713897705, 1.0))
    # Links for transform_geometry_002
    links.new(separate_geometry_004.outputs[0], transform_geometry_002.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (869.0, -35.800048828125)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(separate_geometry_004.outputs[0], join_geometry_004.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.name = "Flip Faces.001"
    flip_faces_001.label = ""
    flip_faces_001.location = (709.0, -95.800048828125)
    flip_faces_001.bl_label = "Flip Faces"
    # Selection
    flip_faces_001.inputs[1].default_value = True
    # Links for flip_faces_001
    links.new(flip_faces_001.outputs[0], join_geometry_004.inputs[0])
    links.new(transform_geometry_002.outputs[0], flip_faces_001.inputs[0])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    transform_geometry_003.label = ""
    transform_geometry_003.location = (1029.0, -115.800048828125)
    transform_geometry_003.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_003.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_003.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    # Links for transform_geometry_003
    links.new(join_geometry_004.outputs[0], transform_geometry_003.inputs[0])

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_008.name = "Join Geometry.008"
    join_geometry_008.label = ""
    join_geometry_008.location = (1369.0, -55.800048828125)
    join_geometry_008.bl_label = "Join Geometry"
    # Links for join_geometry_008
    links.new(join_geometry_004.outputs[0], join_geometry_008.inputs[0])

    flip_faces_002 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.name = "Flip Faces.002"
    flip_faces_002.label = ""
    flip_faces_002.location = (1209.0, -115.800048828125)
    flip_faces_002.bl_label = "Flip Faces"
    # Selection
    flip_faces_002.inputs[1].default_value = True
    # Links for flip_faces_002
    links.new(flip_faces_002.outputs[0], join_geometry_008.inputs[0])
    links.new(transform_geometry_003.outputs[0], flip_faces_002.inputs[0])

    mesh_to_points_001 = nodes.new("GeometryNodeMeshToPoints")
    mesh_to_points_001.name = "Mesh to Points.001"
    mesh_to_points_001.label = ""
    mesh_to_points_001.location = (1729.0, -55.800048828125)
    mesh_to_points_001.bl_label = "Mesh to Points"
    mesh_to_points_001.mode = "VERTICES"
    # Selection
    mesh_to_points_001.inputs[1].default_value = True
    # Position
    mesh_to_points_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Radius
    mesh_to_points_001.inputs[3].default_value = 0.05000000074505806
    # Links for mesh_to_points_001

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    points_to_curves.label = ""
    points_to_curves.location = (2109.0, -55.800048828125)
    points_to_curves.bl_label = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0
    # Links for points_to_curves
    links.new(mesh_to_points_001.outputs[0], points_to_curves.inputs[0])

    gradient_texture = nodes.new("ShaderNodeTexGradient")
    gradient_texture.name = "Gradient Texture"
    gradient_texture.label = ""
    gradient_texture.location = (1569.0, -235.800048828125)
    gradient_texture.bl_label = "Gradient Texture"
    gradient_texture.gradient_type = "RADIAL"
    # Vector
    gradient_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Links for gradient_texture

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.label = ""
    merge_by_distance.location = (1549.0, -55.800048828125)
    merge_by_distance.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance.inputs[1].default_value = True
    # Mode
    merge_by_distance.inputs[2].default_value = "All"
    # Distance
    merge_by_distance.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance
    links.new(merge_by_distance.outputs[0], mesh_to_points_001.inputs[0])
    links.new(join_geometry_008.outputs[0], merge_by_distance.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (2309.0, -55.800048828125)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Length"
    # Count
    resample_curve.inputs[3].default_value = 754
    # Length
    resample_curve.inputs[4].default_value = 0.0010000000474974513
    # Links for resample_curve
    links.new(points_to_curves.outputs[0], resample_curve.inputs[0])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    transform_geometry_004.label = ""
    transform_geometry_004.location = (2629.0, -35.800048828125)
    transform_geometry_004.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_004.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_004.inputs[3].default_value = Euler((0.01483529806137085, 0.03560471534729004, 0.0), 'XYZ')
    # Scale
    transform_geometry_004.inputs[4].default_value = Vector((1.059999942779541, 1.0199999809265137, 1.0))
    # Links for transform_geometry_004
    links.new(resample_curve.outputs[0], transform_geometry_004.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.label = ""
    transform_geometry_005.location = (2809.0, -375.800048828125)
    transform_geometry_005.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_005.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_005.inputs[3].default_value = Euler((-0.01151917316019535, -0.06230825185775757, 0.0), 'XYZ')
    # Scale
    transform_geometry_005.inputs[4].default_value = Vector((1.059999942779541, 1.0199999809265137, 1.0))
    # Links for transform_geometry_005

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (3029.0, -35.800048828125)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(transform_geometry_004.outputs[0], join_geometry.inputs[0])
    links.new(transform_geometry_005.outputs[0], join_geometry.inputs[0])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (5558.0, -355.800048828125)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (4678.0, -635.800048828125)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Resolution
    curve_circle.inputs[0].default_value = 3
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle.inputs[4].default_value = 0.0020000000949949026
    # Links for curve_circle

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (2629.0, -375.800048828125)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Position
    set_position_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_001
    links.new(set_position_001.outputs[0], transform_geometry_005.inputs[0])
    links.new(resample_curve.outputs[0], set_position_001.inputs[0])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.label = ""
    spline_parameter.location = (1989.0, -755.800048828125)
    spline_parameter.bl_label = "Spline Parameter"
    # Links for spline_parameter

    float_curve_001 = nodes.new("ShaderNodeFloatCurve")
    float_curve_001.name = "Float Curve.001"
    float_curve_001.label = ""
    float_curve_001.location = (1989.0, -435.800048828125)
    float_curve_001.bl_label = "Float Curve"
    # Factor
    float_curve_001.inputs[0].default_value = 1.0
    # Links for float_curve_001
    links.new(spline_parameter.outputs[0], float_curve_001.inputs[1])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (2249.0, -435.800048828125)
    combine_x_y_z.bl_label = "Combine XYZ"
    # X
    combine_x_y_z.inputs[0].default_value = 0.0
    # Z
    combine_x_y_z.inputs[2].default_value = 0.0
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], set_position_001.inputs[3])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (2249.0, -515.800048828125)
    math_001.bl_label = "Math"
    math_001.operation = "MULTIPLY"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = -0.009999999776482582
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(float_curve_001.outputs[0], math_001.inputs[0])
    links.new(math_001.outputs[0], combine_x_y_z.inputs[1])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (6938.0, -515.800048828125)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_003.inputs[3].default_value = True
    # Links for store_named_attribute_003

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.name = "Curve Circle.001"
    curve_circle_001.label = ""
    curve_circle_001.location = (29.0, -35.800048828125)
    curve_circle_001.bl_label = "Curve Circle"
    curve_circle_001.mode = "RADIUS"
    # Resolution
    curve_circle_001.inputs[0].default_value = 32
    # Point 1
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_001.inputs[4].default_value = 0.009999999776482582
    # Links for curve_circle_001

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (4378.0, -315.800048828125)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(join_geometry.outputs[0], join_geometry_001.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_009.name = "Join Geometry.009"
    join_geometry_009.label = ""
    join_geometry_009.location = (209.0, -55.800048828125)
    join_geometry_009.bl_label = "Join Geometry"
    # Links for join_geometry_009
    links.new(curve_circle_001.outputs[0], join_geometry_009.inputs[0])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.name = "Transform Geometry.006"
    transform_geometry_006.label = ""
    transform_geometry_006.location = (389.0, -35.800048828125)
    transform_geometry_006.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_006.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_006.inputs[2].default_value = Vector((0.0, -0.1550000011920929, 0.054999999701976776))
    # Rotation
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')
    # Scale
    transform_geometry_006.inputs[4].default_value = Vector((1.0, 0.800000011920929, 1.0))
    # Links for transform_geometry_006
    links.new(join_geometry_009.outputs[0], transform_geometry_006.inputs[0])

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.name = "Transform Geometry.007"
    transform_geometry_007.label = ""
    transform_geometry_007.location = (29.0, -175.800048828125)
    transform_geometry_007.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_007.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_007.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    # Rotation
    transform_geometry_007.inputs[3].default_value = Euler((0.4747295081615448, 0.7522368431091309, 0.8482299447059631), 'XYZ')
    # Scale
    transform_geometry_007.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_007
    links.new(curve_circle_001.outputs[0], transform_geometry_007.inputs[0])
    links.new(transform_geometry_007.outputs[0], join_geometry_009.inputs[0])

    frame_008 = nodes.new("NodeFrame")
    frame_008.name = "Frame.008"
    frame_008.label = "Knot"
    frame_008.location = (3329.0, -440.0)
    frame_008.bl_label = "Frame"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20
    # Links for frame_008

    frame_009 = nodes.new("NodeFrame")
    frame_009.name = "Frame.009"
    frame_009.label = "Waist Loops"
    frame_009.location = (29.0, -260.0)
    frame_009.bl_label = "Frame"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20
    # Links for frame_009

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (1749.0, -235.800048828125)
    math_002.bl_label = "Math"
    math_002.operation = "ADD"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 0.5
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(gradient_texture.outputs[1], math_002.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (1909.0, -235.800048828125)
    math_003.bl_label = "Math"
    math_003.operation = "FRACT"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 0.5
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_003.outputs[0], points_to_curves.inputs[2])
    links.new(math_002.outputs[0], math_003.inputs[0])

    bézier_segment_002 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_002.name = "Bézier Segment.002"
    bézier_segment_002.label = ""
    bézier_segment_002.location = (3958.0, -635.800048828125)
    bézier_segment_002.bl_label = "Bézier Segment"
    bézier_segment_002.mode = "OFFSET"
    # Resolution
    bézier_segment_002.inputs[0].default_value = 16
    # Start
    bézier_segment_002.inputs[1].default_value = Vector((0.0, -0.15800000727176666, 0.054999999701976776))
    # Start Handle
    bézier_segment_002.inputs[2].default_value = Vector((0.04999999701976776, 0.0, 0.0))
    # End Handle
    bézier_segment_002.inputs[3].default_value = Vector((-0.03999999910593033, 0.0, 0.05999999865889549))
    # End
    bézier_segment_002.inputs[4].default_value = Vector((0.03999999910593033, -0.18800000846385956, -0.06499999761581421))
    # Links for bézier_segment_002
    links.new(bézier_segment_002.outputs[0], join_geometry_001.inputs[0])

    bézier_segment_003 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_003.name = "Bézier Segment.003"
    bézier_segment_003.label = ""
    bézier_segment_003.location = (4118.0, -695.800048828125)
    bézier_segment_003.bl_label = "Bézier Segment"
    bézier_segment_003.mode = "OFFSET"
    # Resolution
    bézier_segment_003.inputs[0].default_value = 16
    # Start
    bézier_segment_003.inputs[1].default_value = Vector((0.0, -0.15800000727176666, 0.054999999701976776))
    # Start Handle
    bézier_segment_003.inputs[2].default_value = Vector((0.019999997690320015, -0.009999999776482582, 0.0))
    # End Handle
    bézier_segment_003.inputs[3].default_value = Vector((-0.009999999776482582, -0.009999999776482582, 0.05999999865889549))
    # End
    bézier_segment_003.inputs[4].default_value = Vector((0.009999999776482582, -0.18800000846385956, -0.06499999761581421))
    # Links for bézier_segment_003
    links.new(bézier_segment_003.outputs[0], join_geometry_001.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    set_curve_tilt.label = ""
    set_curve_tilt.location = (4738.0, -315.800048828125)
    set_curve_tilt.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Links for set_curve_tilt

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.label = ""
    spline_parameter_001.location = (4578.0, -435.800048828125)
    spline_parameter_001.bl_label = "Spline Parameter"
    # Links for spline_parameter_001

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (4738.0, -435.800048828125)
    math_004.bl_label = "Math"
    math_004.operation = "MULTIPLY"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 106.49999237060547
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(spline_parameter_001.outputs[1], math_004.inputs[0])
    links.new(math_004.outputs[0], set_curve_tilt.inputs[2])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.label = ""
    instance_on_points_001.location = (4878.0, -675.800048828125)
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
    links.new(curve_circle.outputs[0], instance_on_points_001.inputs[0])

    curve_circle_002 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_002.name = "Curve Circle.002"
    curve_circle_002.label = ""
    curve_circle_002.location = (4678.0, -755.800048828125)
    curve_circle_002.bl_label = "Curve Circle"
    curve_circle_002.mode = "RADIUS"
    # Resolution
    curve_circle_002.inputs[0].default_value = 8
    # Point 1
    curve_circle_002.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_002.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_002.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_002.inputs[4].default_value = 0.003000000026077032
    # Links for curve_circle_002
    links.new(curve_circle_002.outputs[0], instance_on_points_001.inputs[2])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.label = ""
    realize_instances_001.location = (5038.0, -675.800048828125)
    realize_instances_001.bl_label = "Realize Instances"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0
    # Links for realize_instances_001
    links.new(instance_on_points_001.outputs[0], realize_instances_001.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (4578.0, -315.800048828125)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Length"
    # Count
    resample_curve_001.inputs[3].default_value = 754
    # Length
    resample_curve_001.inputs[4].default_value = 0.0010000000474974513
    # Links for resample_curve_001
    links.new(resample_curve_001.outputs[0], set_curve_tilt.inputs[0])
    links.new(join_geometry_001.outputs[0], resample_curve_001.inputs[0])

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (7098.0, -515.800048828125)
    store_named_attribute_004.bl_label = "Store Named Attribute"
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "rope"
    # Value
    store_named_attribute_004.inputs[3].default_value = True
    # Links for store_named_attribute_004
    links.new(store_named_attribute_003.outputs[0], store_named_attribute_004.inputs[0])

    capture_attribute_003 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.name = "Capture Attribute.003"
    capture_attribute_003.label = ""
    capture_attribute_003.location = (5358.0, -515.800048828125)
    capture_attribute_003.bl_label = "Capture Attribute"
    capture_attribute_003.active_index = 0
    capture_attribute_003.domain = "POINT"
    # Links for capture_attribute_003
    links.new(capture_attribute_003.outputs[0], curve_to_mesh.inputs[1])
    links.new(realize_instances_001.outputs[0], capture_attribute_003.inputs[0])

    capture_attribute_004 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_004.name = "Capture Attribute.004"
    capture_attribute_004.label = ""
    capture_attribute_004.location = (5358.0, -375.800048828125)
    capture_attribute_004.bl_label = "Capture Attribute"
    capture_attribute_004.active_index = 0
    capture_attribute_004.domain = "POINT"
    # Links for capture_attribute_004
    links.new(capture_attribute_004.outputs[0], curve_to_mesh.inputs[0])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"
    spline_parameter_002.label = ""
    spline_parameter_002.location = (5358.0, -655.800048828125)
    spline_parameter_002.bl_label = "Spline Parameter"
    # Links for spline_parameter_002
    links.new(spline_parameter_002.outputs[1], capture_attribute_004.inputs[1])
    links.new(spline_parameter_002.outputs[1], capture_attribute_003.inputs[1])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (5558.0, -515.800048828125)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # Z
    combine_x_y_z_001.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_001
    links.new(capture_attribute_004.outputs[1], combine_x_y_z_001.inputs[0])
    links.new(capture_attribute_003.outputs[1], combine_x_y_z_001.inputs[1])

    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.name = "Store Named Attribute.005"
    store_named_attribute_005.label = ""
    store_named_attribute_005.location = (7258.0, -515.800048828125)
    store_named_attribute_005.bl_label = "Store Named Attribute"
    store_named_attribute_005.data_type = "FLOAT2"
    store_named_attribute_005.domain = "CORNER"
    # Selection
    store_named_attribute_005.inputs[1].default_value = True
    # Name
    store_named_attribute_005.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute_005
    links.new(store_named_attribute_004.outputs[0], store_named_attribute_005.inputs[0])
    links.new(combine_x_y_z_001.outputs[0], store_named_attribute_005.inputs[3])
    links.new(store_named_attribute_005.outputs[0], switch.inputs[2])

    frame_010 = nodes.new("NodeFrame")
    frame_010.name = "Frame.010"
    frame_010.label = "ROPE"
    frame_010.location = (762.0, 2875.800048828125)
    frame_010.bl_label = "Frame"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20
    # Links for frame_010

    instance_on_points_002 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.name = "Instance on Points.002"
    instance_on_points_002.label = ""
    instance_on_points_002.location = (5418.0, -995.800048828125)
    instance_on_points_002.bl_label = "Instance on Points"
    # Selection
    instance_on_points_002.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_002.inputs[3].default_value = False
    # Instance Index
    instance_on_points_002.inputs[4].default_value = 0
    # Scale
    instance_on_points_002.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_002

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.label = ""
    curve_line.location = (5238.0, -1055.800048828125)
    curve_line.bl_label = "Curve Line"
    curve_line.mode = "POINTS"
    # Start
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    # End
    curve_line.inputs[1].default_value = Vector((0.0, 0.0, 0.05000000074505806))
    # Direction
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    # Length
    curve_line.inputs[3].default_value = 1.0
    # Links for curve_line
    links.new(curve_line.outputs[0], instance_on_points_002.inputs[2])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.label = ""
    align_rotation_to_vector_001.location = (5418.0, -1275.800048828125)
    align_rotation_to_vector_001.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_001.axis = "Z"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_001.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_001
    links.new(align_rotation_to_vector_001.outputs[0], instance_on_points_002.inputs[5])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (5238.0, -1315.800048828125)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_001.inputs[2])

    realize_instances_002 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.name = "Realize Instances.002"
    realize_instances_002.label = ""
    realize_instances_002.location = (5598.0, -995.800048828125)
    realize_instances_002.bl_label = "Realize Instances"
    # Selection
    realize_instances_002.inputs[1].default_value = True
    # Realize All
    realize_instances_002.inputs[2].default_value = True
    # Depth
    realize_instances_002.inputs[3].default_value = 0
    # Links for realize_instances_002
    links.new(instance_on_points_002.outputs[0], realize_instances_002.inputs[0])

    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.name = "Resample Curve.002"
    resample_curve_002.label = ""
    resample_curve_002.location = (5758.0, -995.800048828125)
    resample_curve_002.bl_label = "Resample Curve"
    resample_curve_002.keep_last_segment = True
    # Selection
    resample_curve_002.inputs[1].default_value = True
    # Mode
    resample_curve_002.inputs[2].default_value = "Count"
    # Count
    resample_curve_002.inputs[3].default_value = 7
    # Length
    resample_curve_002.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_002
    links.new(realize_instances_002.outputs[0], resample_curve_002.inputs[0])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (5978.0, -1015.800048828125)
    set_position_002.bl_label = "Set Position"
    # Links for set_position_002
    links.new(resample_curve_002.outputs[0], set_position_002.inputs[0])

    endpoint_selection = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection.name = "Endpoint Selection"
    endpoint_selection.label = ""
    endpoint_selection.location = (5598.0, -1115.800048828125)
    endpoint_selection.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection.inputs[0].default_value = 1
    # End Size
    endpoint_selection.inputs[1].default_value = 0
    # Links for endpoint_selection

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.label = ""
    boolean_math_003.location = (5758.0, -1115.800048828125)
    boolean_math_003.bl_label = "Boolean Math"
    boolean_math_003.operation = "NOT"
    # Boolean
    boolean_math_003.inputs[1].default_value = False
    # Links for boolean_math_003
    links.new(boolean_math_003.outputs[0], set_position_002.inputs[1])
    links.new(endpoint_selection.outputs[0], boolean_math_003.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (5758.0, -1235.800048828125)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 0.006000000052154064
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], set_position_002.inputs[3])

    random_value_002 = nodes.new("FunctionNodeRandomValue")
    random_value_002.name = "Random Value.002"
    random_value_002.label = ""
    random_value_002.location = (5598.0, -1235.800048828125)
    random_value_002.bl_label = "Random Value"
    random_value_002.data_type = "FLOAT_VECTOR"
    # Min
    random_value_002.inputs[0].default_value = [-1.0, -1.0, -1.0]
    # Max
    random_value_002.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_002.inputs[2].default_value = 0.0
    # Max
    random_value_002.inputs[3].default_value = 1.0
    # Min
    random_value_002.inputs[4].default_value = 0
    # Max
    random_value_002.inputs[5].default_value = 100
    # Probability
    random_value_002.inputs[6].default_value = 0.5
    # ID
    random_value_002.inputs[7].default_value = 0
    # Seed
    random_value_002.inputs[8].default_value = 2
    # Links for random_value_002
    links.new(random_value_002.outputs[0], vector_math_002.inputs[0])

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.label = ""
    set_spline_type.location = (6138.0, -1015.800048828125)
    set_spline_type.bl_label = "Set Spline Type"
    set_spline_type.spline_type = "NURBS"
    # Selection
    set_spline_type.inputs[1].default_value = True
    # Links for set_spline_type
    links.new(set_position_002.outputs[0], set_spline_type.inputs[0])

    resample_curve_003 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.name = "Resample Curve.003"
    resample_curve_003.label = ""
    resample_curve_003.location = (6298.0, -1015.800048828125)
    resample_curve_003.bl_label = "Resample Curve"
    resample_curve_003.keep_last_segment = True
    # Selection
    resample_curve_003.inputs[1].default_value = True
    # Mode
    resample_curve_003.inputs[2].default_value = "Count"
    # Count
    resample_curve_003.inputs[3].default_value = 15
    # Length
    resample_curve_003.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_003
    links.new(set_spline_type.outputs[0], resample_curve_003.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (6458.0, -1015.800048828125)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_001.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = True
    # Links for curve_to_mesh_001
    links.new(resample_curve_003.outputs[0], curve_to_mesh_001.inputs[0])

    curve_circle_003 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.name = "Curve Circle.003"
    curve_circle_003.label = ""
    curve_circle_003.location = (6298.0, -1135.800048828125)
    curve_circle_003.bl_label = "Curve Circle"
    curve_circle_003.mode = "RADIUS"
    # Resolution
    curve_circle_003.inputs[0].default_value = 32
    # Point 1
    curve_circle_003.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_003.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_003.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_003.inputs[4].default_value = 9.999999747378752e-05
    # Links for curve_circle_003
    links.new(curve_circle_003.outputs[0], curve_to_mesh_001.inputs[1])

    join_geometry_011 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_011.name = "Join Geometry.011"
    join_geometry_011.label = ""
    join_geometry_011.location = (6698.0, -495.800048828125)
    join_geometry_011.bl_label = "Join Geometry"
    # Links for join_geometry_011
    links.new(curve_to_mesh_001.outputs[0], join_geometry_011.inputs[0])
    links.new(curve_to_mesh.outputs[0], join_geometry_011.inputs[0])
    links.new(join_geometry_011.outputs[0], store_named_attribute_003.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (5858.0, -675.800048828125)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "FACES"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity
    links.new(curve_to_mesh.outputs[0], geometry_proximity.inputs[0])
    links.new(geometry_proximity.outputs[0], set_position_002.inputs[2])

    join_geometry_012 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_012.name = "Join Geometry.012"
    join_geometry_012.label = ""
    join_geometry_012.location = (5078.0, -355.800048828125)
    join_geometry_012.bl_label = "Join Geometry"
    # Links for join_geometry_012
    links.new(join_geometry_012.outputs[0], capture_attribute_004.inputs[0])
    links.new(set_curve_tilt.outputs[0], join_geometry_012.inputs[0])

    set_curve_tilt_001 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_001.name = "Set Curve Tilt.001"
    set_curve_tilt_001.label = ""
    set_curve_tilt_001.location = (4738.0, -35.800048828125)
    set_curve_tilt_001.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_001.inputs[1].default_value = True
    # Links for set_curve_tilt_001
    links.new(set_curve_tilt_001.outputs[0], join_geometry_012.inputs[0])

    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_003.name = "Spline Parameter.003"
    spline_parameter_003.label = ""
    spline_parameter_003.location = (4578.0, -155.800048828125)
    spline_parameter_003.bl_label = "Spline Parameter"
    # Links for spline_parameter_003

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (4738.0, -155.800048828125)
    math_005.bl_label = "Math"
    math_005.operation = "MULTIPLY"
    math_005.use_clamp = False
    # Value
    math_005.inputs[1].default_value = 199.0999755859375
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(spline_parameter_003.outputs[1], math_005.inputs[0])
    links.new(math_005.outputs[0], set_curve_tilt_001.inputs[2])

    resample_curve_004 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_004.name = "Resample Curve.004"
    resample_curve_004.label = ""
    resample_curve_004.location = (4578.0, -35.800048828125)
    resample_curve_004.bl_label = "Resample Curve"
    resample_curve_004.keep_last_segment = True
    # Selection
    resample_curve_004.inputs[1].default_value = True
    # Mode
    resample_curve_004.inputs[2].default_value = "Length"
    # Count
    resample_curve_004.inputs[3].default_value = 754
    # Length
    resample_curve_004.inputs[4].default_value = 0.0010000000474974513
    # Links for resample_curve_004
    links.new(resample_curve_004.outputs[0], set_curve_tilt_001.inputs[0])
    links.new(transform_geometry_006.outputs[0], resample_curve_004.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.name = "Group.002"
    swap_attr.label = ""
    swap_attr.location = (1349.0, -289.0)
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.bl_label = "Group"
    # Old
    swap_attr.inputs[2].default_value = "ruby"
    # New
    swap_attr.inputs[3].default_value = "saphire"
    # Links for swap_attr
    links.new(swap_attr.outputs[0], join_geometry_006.inputs[0])
    links.new(realize_instances.outputs[0], swap_attr.inputs[0])
    links.new(capture_attribute_002.outputs[1], swap_attr.inputs[1])

    gem_in_holder_1 = nodes.new("GeometryNodeGroup")
    gem_in_holder_1.name = "Gem in Holder.001"
    gem_in_holder_1.label = ""
    gem_in_holder_1.location = (569.0, -75.13334655761719)
    gem_in_holder_1.node_tree = create_gem_in__holder_group()
    gem_in_holder_1.bl_label = "Group"
    # Gem Radius
    gem_in_holder_1.inputs[0].default_value = 0.009999990463256836
    # Gem Material
    gem_in_holder_1.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_1.inputs[2].default_value = False
    # Scale
    gem_in_holder_1.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_1.inputs[4].default_value = 20
    # Seed
    gem_in_holder_1.inputs[5].default_value = 10
    # Wings
    gem_in_holder_1.inputs[6].default_value = False
    # Array Count
    gem_in_holder_1.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_1.inputs[8].default_value = 10
    # Links for gem_in_holder_1

    position_004 = nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"
    position_004.label = ""
    position_004.location = (29.0, -255.1333465576172)
    position_004.bl_label = "Position"
    # Links for position_004

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.name = "For Each Geometry Element Input.001"
    for_each_geometry_element_input_001.label = ""
    for_each_geometry_element_input_001.location = (189.0, -55.13334655761719)
    for_each_geometry_element_input_001.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input_001.inputs[1].default_value = True
    # Rotation
    for_each_geometry_element_input_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for for_each_geometry_element_input_001
    links.new(position_004.outputs[0], for_each_geometry_element_input_001.inputs[2])

    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.name = "For Each Geometry Element Output.001"
    for_each_geometry_element_output_001.label = ""
    for_each_geometry_element_output_001.location = (1529.0, -75.13334655761719)
    for_each_geometry_element_output_001.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    # Links for for_each_geometry_element_output_001
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_006.inputs[0])

    transform_geometry_008 = nodes.new("GeometryNodeTransform")
    transform_geometry_008.name = "Transform Geometry.008"
    transform_geometry_008.label = ""
    transform_geometry_008.location = (829.0, -75.13334655761719)
    transform_geometry_008.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_008.inputs[1].default_value = "Components"
    # Scale
    transform_geometry_008.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_008
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_008.inputs[2])
    links.new(gem_in_holder_1.outputs[4], transform_geometry_008.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.name = "Rotate Rotation.002"
    rotate_rotation_002.label = ""
    rotate_rotation_002.location = (229.0, -315.13336181640625)
    rotate_rotation_002.bl_label = "Rotate Rotation"
    rotate_rotation_002.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, -1.5707963705062866, 0.0), 'XYZ')
    # Links for rotate_rotation_002
    links.new(rotate_rotation_002.outputs[0], transform_geometry_008.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[3], rotate_rotation_002.inputs[0])

    frame_011 = nodes.new("NodeFrame")
    frame_011.name = "Frame.011"
    frame_011.label = "Random Wings"
    frame_011.location = (729.0, -1029.6666259765625)
    frame_011.bl_label = "Frame"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20
    # Links for frame_011

    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.name = "Random Value.007"
    random_value_007.label = ""
    random_value_007.location = (389.0, -75.13334655761719)
    random_value_007.bl_label = "Random Value"
    random_value_007.data_type = "FLOAT"
    # Min
    random_value_007.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_007.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_007.inputs[2].default_value = 6.0
    # Max
    random_value_007.inputs[3].default_value = 7.0
    # Min
    random_value_007.inputs[4].default_value = 0
    # Max
    random_value_007.inputs[5].default_value = 100
    # Probability
    random_value_007.inputs[6].default_value = 0.5
    # Seed
    random_value_007.inputs[8].default_value = 32
    # Links for random_value_007
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_1.inputs[10])

    random_value_008 = nodes.new("FunctionNodeRandomValue")
    random_value_008.name = "Random Value.008"
    random_value_008.label = ""
    random_value_008.location = (389.0, -255.1333465576172)
    random_value_008.bl_label = "Random Value"
    random_value_008.data_type = "FLOAT"
    # Min
    random_value_008.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_008.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_008.inputs[2].default_value = 0.0
    # Max
    random_value_008.inputs[3].default_value = 0.003000000026077032
    # Min
    random_value_008.inputs[4].default_value = 0
    # Max
    random_value_008.inputs[5].default_value = 100
    # Probability
    random_value_008.inputs[6].default_value = 0.5
    # Seed
    random_value_008.inputs[8].default_value = 10
    # Links for random_value_008
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_008.inputs[7])
    links.new(random_value_008.outputs[1], gem_in_holder_1.inputs[9])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    set_position_003.label = ""
    set_position_003.location = (1009.0, -75.13334655761719)
    set_position_003.bl_label = "Set Position"
    # Selection
    set_position_003.inputs[1].default_value = True
    # Offset
    set_position_003.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_003
    links.new(transform_geometry_008.outputs[0], set_position_003.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (1398.0, -1624.7999267578125)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Links for reroute_002

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.label = ""
    geometry_proximity_001.location = (829.0, -295.13336181640625)
    geometry_proximity_001.bl_label = "Geometry Proximity"
    geometry_proximity_001.target_element = "FACES"
    # Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0
    # Links for geometry_proximity_001
    links.new(reroute_002.outputs[0], geometry_proximity_001.inputs[0])
    links.new(geometry_proximity_001.outputs[0], set_position_003.inputs[2])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (1169.0, -75.13334655761719)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002
    links.new(set_position_003.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(gem_in_holder_1.outputs[1], curve_to_mesh_002.inputs[1])
    links.new(gem_in_holder_1.outputs[2], curve_to_mesh_002.inputs[2])

    store_named_attribute_006 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_006.name = "Store Named Attribute.006"
    store_named_attribute_006.label = ""
    store_named_attribute_006.location = (1349.0, -75.13334655761719)
    store_named_attribute_006.bl_label = "Store Named Attribute"
    store_named_attribute_006.data_type = "BOOLEAN"
    store_named_attribute_006.domain = "POINT"
    # Selection
    store_named_attribute_006.inputs[1].default_value = True
    # Name
    store_named_attribute_006.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_006.inputs[3].default_value = True
    # Links for store_named_attribute_006
    links.new(store_named_attribute_006.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute_006.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (578.9881591796875, -1496.593994140625)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(reroute.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(separate_geometry_001.outputs[1], reroute.inputs[0])
    links.new(reroute.outputs[0], reroute_002.inputs[0])

    frame_012 = nodes.new("NodeFrame")
    frame_012.name = "Frame.012"
    frame_012.label = ""
    frame_012.location = (29.0, -35.7999267578125)
    frame_012.bl_label = "Frame"
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20
    # Links for frame_012

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (8595.9638671875, 854.44287109375)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001
    links.new(join_geometry_006.outputs[0], reroute_001.inputs[0])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (9180.0, 660.0)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Links for switch_001
    links.new(reroute_001.outputs[0], switch_001.inputs[2])
    links.new(switch_001.outputs[0], join_geometry_007.inputs[0])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (9180.0, 720.0)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[0], switch_001.inputs[0])

    resample_curve_005 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_005.name = "Resample Curve.005"
    resample_curve_005.label = ""
    resample_curve_005.location = (5238.0, -915.800048828125)
    resample_curve_005.bl_label = "Resample Curve"
    resample_curve_005.keep_last_segment = True
    # Selection
    resample_curve_005.inputs[1].default_value = True
    # Mode
    resample_curve_005.inputs[2].default_value = "Length"
    # Count
    resample_curve_005.inputs[3].default_value = 10
    # Length
    resample_curve_005.inputs[4].default_value = 0.004999999888241291
    # Links for resample_curve_005
    links.new(resample_curve_005.outputs[0], instance_on_points_002.inputs[0])
    links.new(set_curve_tilt.outputs[0], resample_curve_005.inputs[0])

    # Parent assignments
    bézier_segment.parent = frame
    frame.parent = frame_002
    bézier_segment_001.parent = frame_001
    join_splines.parent = frame_001
    join_splines_1.parent = frame_002
    frame_001.parent = frame_003
    frame_002.parent = frame_003
    quadratic_bézier.parent = frame_004
    join_geometry_002.parent = frame_004
    quadratic_bézier_005.parent = frame_004
    reverse_curve.parent = frame_002
    reverse_curve_001.parent = frame_001
    transform_geometry_001.parent = frame_001
    pipes.parent = frame_005
    quadratic_bézier_006.parent = frame_004
    gold_on_band.parent = frame_006
    join_geometry_006.parent = frame_006
    separate_geometry_002.parent = frame_005
    edge_vertices.parent = frame_005
    vector_math.parent = frame_005
    compare_002.parent = frame_005
    boolean_math_001.parent = frame_005
    instance_on_points.parent = frame_012
    gem_in_holder.parent = frame_012
    separate_x_y_z_001.parent = frame_012
    compare.parent = frame_012
    align_rotation_to_vector.parent = frame_012
    random_value.parent = frame_012
    separate_geometry_003.parent = frame_012
    mesh_to_points.parent = frame_012
    normal.parent = frame_012
    capture_attribute_001.parent = frame_012
    realize_instances.parent = frame_012
    separate_x_y_z_002.parent = frame_012
    map_range.parent = frame_012
    math.parent = frame_012
    capture_attribute_002.parent = frame_012
    index.parent = frame_012
    delete_geometry.parent = frame_007
    position.parent = frame_007
    separate_x_y_z_003.parent = frame_007
    compare_003.parent = frame_007
    set_position.parent = frame_007
    compare_004.parent = frame_007
    position_001.parent = frame_007
    vector_math_001.parent = frame_007
    separate_geometry_004.parent = frame_009
    separate_x_y_z_004.parent = frame_009
    compare_005.parent = frame_009
    transform_geometry_002.parent = frame_009
    join_geometry_004.parent = frame_009
    flip_faces_001.parent = frame_009
    transform_geometry_003.parent = frame_009
    join_geometry_008.parent = frame_009
    flip_faces_002.parent = frame_009
    mesh_to_points_001.parent = frame_009
    points_to_curves.parent = frame_009
    gradient_texture.parent = frame_009
    merge_by_distance.parent = frame_009
    resample_curve.parent = frame_009
    transform_geometry_004.parent = frame_009
    transform_geometry_005.parent = frame_009
    join_geometry.parent = frame_009
    curve_to_mesh.parent = frame_010
    curve_circle.parent = frame_010
    set_position_001.parent = frame_009
    spline_parameter.parent = frame_009
    float_curve_001.parent = frame_009
    combine_x_y_z.parent = frame_009
    math_001.parent = frame_009
    store_named_attribute_003.parent = frame_010
    curve_circle_001.parent = frame_008
    join_geometry_001.parent = frame_010
    join_geometry_009.parent = frame_008
    transform_geometry_006.parent = frame_008
    transform_geometry_007.parent = frame_008
    frame_008.parent = frame_010
    frame_009.parent = frame_010
    math_002.parent = frame_009
    math_003.parent = frame_009
    bézier_segment_002.parent = frame_010
    bézier_segment_003.parent = frame_010
    set_curve_tilt.parent = frame_010
    spline_parameter_001.parent = frame_010
    math_004.parent = frame_010
    instance_on_points_001.parent = frame_010
    curve_circle_002.parent = frame_010
    realize_instances_001.parent = frame_010
    resample_curve_001.parent = frame_010
    store_named_attribute_004.parent = frame_010
    capture_attribute_003.parent = frame_010
    capture_attribute_004.parent = frame_010
    spline_parameter_002.parent = frame_010
    combine_x_y_z_001.parent = frame_010
    store_named_attribute_005.parent = frame_010
    instance_on_points_002.parent = frame_010
    curve_line.parent = frame_010
    align_rotation_to_vector_001.parent = frame_010
    curve_tangent.parent = frame_010
    realize_instances_002.parent = frame_010
    resample_curve_002.parent = frame_010
    set_position_002.parent = frame_010
    endpoint_selection.parent = frame_010
    boolean_math_003.parent = frame_010
    vector_math_002.parent = frame_010
    random_value_002.parent = frame_010
    set_spline_type.parent = frame_010
    resample_curve_003.parent = frame_010
    curve_to_mesh_001.parent = frame_010
    curve_circle_003.parent = frame_010
    join_geometry_011.parent = frame_010
    geometry_proximity.parent = frame_010
    join_geometry_012.parent = frame_010
    set_curve_tilt_001.parent = frame_010
    spline_parameter_003.parent = frame_010
    math_005.parent = frame_010
    resample_curve_004.parent = frame_010
    swap_attr.parent = frame_012
    gem_in_holder_1.parent = frame_011
    position_004.parent = frame_011
    for_each_geometry_element_input_001.parent = frame_011
    for_each_geometry_element_output_001.parent = frame_011
    transform_geometry_008.parent = frame_011
    rotate_rotation_002.parent = frame_011
    frame_011.parent = frame_006
    random_value_007.parent = frame_011
    random_value_008.parent = frame_011
    set_position_003.parent = frame_011
    reroute_002.parent = frame_006
    geometry_proximity_001.parent = frame_011
    curve_to_mesh_002.parent = frame_011
    store_named_attribute_006.parent = frame_011
    reroute.parent = frame_006
    frame_012.parent = frame_006
    resample_curve_005.parent = frame_010

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_08__bejewelled_group():
    group_name = "08 Bejewelled"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (10880.0, -1300.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (9280.0, -1300.0)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004

    set_material = nodes.new("GeometryNodeSetMaterial")
    set_material.name = "Set Material"
    set_material.label = ""
    set_material.location = (9760.0, -1300.0)
    set_material.bl_label = "Set Material"
    # Selection
    set_material.inputs[1].default_value = True
    # Links for set_material

    shoulders = nodes.new("GeometryNodeGroup")
    shoulders.name = "Group.004"
    shoulders.label = ""
    shoulders.location = (9060.0, -1460.0)
    shoulders.node_tree = create_shoulders_group()
    shoulders.bl_label = "Group"
    # Decor
    shoulders.inputs[0].default_value = True
    # Links for shoulders
    links.new(shoulders.outputs[0], join_geometry_004.inputs[0])

    sleeves = nodes.new("GeometryNodeGroup")
    sleeves.name = "Group.005"
    sleeves.label = ""
    sleeves.location = (9060.0, -1360.0)
    sleeves.node_tree = create_sleeves_group()
    sleeves.bl_label = "Group"
    # Decor
    sleeves.inputs[0].default_value = True
    # Links for sleeves
    links.new(sleeves.outputs[0], join_geometry_004.inputs[0])

    neck = nodes.new("GeometryNodeGroup")
    neck.name = "Group.006"
    neck.label = ""
    neck.location = (9060.0, -1060.0)
    neck.node_tree = create_neck_group()
    neck.bl_label = "Group"
    # Decor
    neck.inputs[0].default_value = True
    # Links for neck
    links.new(neck.outputs[0], join_geometry_004.inputs[0])
    links.new(neck.outputs[0], group_output.inputs[0])

    chest = nodes.new("GeometryNodeGroup")
    chest.name = "Group.002"
    chest.label = ""
    chest.location = (9060.0, -1160.0)
    chest.node_tree = create_chest_group()
    chest.bl_label = "Group"
    # Decor
    chest.inputs[0].default_value = True
    # Links for chest
    links.new(chest.outputs[0], join_geometry_004.inputs[0])

    mirror = nodes.new("GeometryNodeGroup")
    mirror.name = "Group"
    mirror.label = ""
    mirror.location = (9600.0, -1300.0)
    mirror.node_tree = create_mirror_group()
    mirror.bl_label = "Group"
    # Links for mirror
    links.new(mirror.outputs[0], set_material.inputs[0])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (9440.0, -1300.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(realize_instances.outputs[0], mirror.inputs[0])
    links.new(join_geometry_004.outputs[0], realize_instances.inputs[0])

    set_material_001 = nodes.new("GeometryNodeSetMaterial")
    set_material_001.name = "Set Material.001"
    set_material_001.label = ""
    set_material_001.location = (9920.0, -1300.0)
    set_material_001.bl_label = "Set Material"
    # Links for set_material_001
    links.new(set_material.outputs[0], set_material_001.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (9920.0, -1400.0)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "BOOLEAN"
    # Name
    named_attribute.inputs[0].default_value = "gold"
    # Links for named_attribute
    links.new(named_attribute.outputs[0], set_material_001.inputs[1])

    set_material_002 = nodes.new("GeometryNodeSetMaterial")
    set_material_002.name = "Set Material.002"
    set_material_002.label = ""
    set_material_002.location = (10080.0, -1300.0)
    set_material_002.bl_label = "Set Material"
    # Links for set_material_002
    links.new(set_material_001.outputs[0], set_material_002.inputs[0])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.label = ""
    named_attribute_001.location = (10080.0, -1400.0)
    named_attribute_001.bl_label = "Named Attribute"
    named_attribute_001.data_type = "BOOLEAN"
    # Name
    named_attribute_001.inputs[0].default_value = "ruby"
    # Links for named_attribute_001
    links.new(named_attribute_001.outputs[0], set_material_002.inputs[1])

    set_material_003 = nodes.new("GeometryNodeSetMaterial")
    set_material_003.name = "Set Material.003"
    set_material_003.label = ""
    set_material_003.location = (10240.0, -1300.0)
    set_material_003.bl_label = "Set Material"
    # Links for set_material_003
    links.new(set_material_002.outputs[0], set_material_003.inputs[0])

    named_attribute_002 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.name = "Named Attribute.002"
    named_attribute_002.label = ""
    named_attribute_002.location = (10240.0, -1400.0)
    named_attribute_002.bl_label = "Named Attribute"
    named_attribute_002.data_type = "BOOLEAN"
    # Name
    named_attribute_002.inputs[0].default_value = "saphire"
    # Links for named_attribute_002
    links.new(named_attribute_002.outputs[0], set_material_003.inputs[1])

    set_material_004 = nodes.new("GeometryNodeSetMaterial")
    set_material_004.name = "Set Material.004"
    set_material_004.label = ""
    set_material_004.location = (10400.0, -1300.0)
    set_material_004.bl_label = "Set Material"
    # Links for set_material_004
    links.new(set_material_003.outputs[0], set_material_004.inputs[0])

    named_attribute_003 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003.name = "Named Attribute.003"
    named_attribute_003.label = ""
    named_attribute_003.location = (10400.0, -1400.0)
    named_attribute_003.bl_label = "Named Attribute"
    named_attribute_003.data_type = "BOOLEAN"
    # Name
    named_attribute_003.inputs[0].default_value = "fabric"
    # Links for named_attribute_003
    links.new(named_attribute_003.outputs[0], set_material_004.inputs[1])

    set_material_005 = nodes.new("GeometryNodeSetMaterial")
    set_material_005.name = "Set Material.005"
    set_material_005.label = ""
    set_material_005.location = (10560.0, -1300.0)
    set_material_005.bl_label = "Set Material"
    # Links for set_material_005
    links.new(set_material_004.outputs[0], set_material_005.inputs[0])

    named_attribute_004 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_004.name = "Named Attribute.004"
    named_attribute_004.label = ""
    named_attribute_004.location = (10560.0, -1400.0)
    named_attribute_004.bl_label = "Named Attribute"
    named_attribute_004.data_type = "BOOLEAN"
    # Name
    named_attribute_004.inputs[0].default_value = "blocker"
    # Links for named_attribute_004
    links.new(named_attribute_004.outputs[0], set_material_005.inputs[1])

    blocker = nodes.new("GeometryNodeGroup")
    blocker.name = "Group.001"
    blocker.label = ""
    blocker.location = (9060.0, -1560.0)
    blocker.node_tree = create_blocker_group()
    blocker.bl_label = "Group"
    # Decor
    blocker.inputs[0].default_value = False
    # Links for blocker
    links.new(blocker.outputs[0], join_geometry_004.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (-7403.833984375, 4101.759765625)
    instance_on_points.bl_label = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Rotation
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points

    waist = nodes.new("GeometryNodeGroup")
    waist.name = "Group.003"
    waist.label = ""
    waist.location = (9060.0, -1260.0)
    waist.node_tree = create_waist_group()
    waist.bl_label = "Group"
    # Decor
    waist.inputs[0].default_value = True
    # Links for waist
    links.new(waist.outputs[0], join_geometry_004.inputs[0])

    named_attribute_005 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_005.name = "Named Attribute.005"
    named_attribute_005.label = ""
    named_attribute_005.location = (9600.0, -1400.0)
    named_attribute_005.bl_label = "Named Attribute"
    named_attribute_005.data_type = "BOOLEAN"
    # Name
    named_attribute_005.inputs[0].default_value = "skip"
    # Links for named_attribute_005
    links.new(named_attribute_005.outputs[0], mirror.inputs[1])

    set_material_006 = nodes.new("GeometryNodeSetMaterial")
    set_material_006.name = "Set Material.006"
    set_material_006.label = ""
    set_material_006.location = (10720.0, -1300.0)
    set_material_006.bl_label = "Set Material"
    # Links for set_material_006
    links.new(set_material_005.outputs[0], set_material_006.inputs[0])

    named_attribute_006 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_006.name = "Named Attribute.006"
    named_attribute_006.label = ""
    named_attribute_006.location = (10720.0, -1400.0)
    named_attribute_006.bl_label = "Named Attribute"
    named_attribute_006.data_type = "BOOLEAN"
    # Name
    named_attribute_006.inputs[0].default_value = "rope"
    # Links for named_attribute_006
    links.new(named_attribute_006.outputs[0], set_material_006.inputs[1])

    # Parent assignments

    auto_layout_nodes(group)
    return group