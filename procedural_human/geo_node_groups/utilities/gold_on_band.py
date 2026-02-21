import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes

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

    auto_layout_nodes(group)
    return group
