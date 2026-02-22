import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group

@geo_node_group
def create_gold_on__band_group():
    group_name = "Gold on Band"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

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
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    distribute_points_on_faces.inputs[1].default_value = True
    distribute_points_on_faces.inputs[2].default_value = 0.0
    distribute_points_on_faces.inputs[3].default_value = 10.0
    distribute_points_on_faces.inputs[5].default_value = 1.0
    links.new(group_input.outputs[0], distribute_points_on_faces.inputs[0])
    links.new(group_input.outputs[1], distribute_points_on_faces.inputs[4])
    links.new(group_input.outputs[3], distribute_points_on_faces.inputs[6])

    points_to_vertices = nodes.new("GeometryNodePointsToVertices")
    points_to_vertices.inputs[1].default_value = True
    links.new(distribute_points_on_faces.outputs[0], points_to_vertices.inputs[0])

    extrude_mesh_001 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.mode = "VERTICES"
    extrude_mesh_001.inputs[3].default_value = 0.0020000000949949026
    extrude_mesh_001.inputs[4].default_value = True
    
    repeat_output = nodes.new("GeometryNodeRepeatOutput")
    repeat_output.active_index = 1
    repeat_output.inspection_index = 0
    repeat_output.repeat_items.new("BOOLEAN", "Top")

    repeat_input = nodes.new("GeometryNodeRepeatInput")
    repeat_input.pair_with_output(repeat_output)
    repeat_input.inputs[2].default_value = True
    repeat_input.inputs[0].default_value = 100
    links.new(repeat_input.outputs[2], extrude_mesh_001.inputs[1])
    links.new(repeat_input.outputs[1], extrude_mesh_001.inputs[0])
    links.new(points_to_vertices.outputs[0], repeat_input.inputs[1])

    links.new(extrude_mesh_001.outputs[0], repeat_output.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = True
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    noise_texture.inputs[2].default_value = 39.5
    noise_texture.inputs[3].default_value = 0.0
    noise_texture.inputs[4].default_value = 0.5
    noise_texture.inputs[5].default_value = 2.0
    noise_texture.inputs[6].default_value = 0.0
    noise_texture.inputs[7].default_value = 1.0
    noise_texture.inputs[8].default_value = 0.0
    links.new(group_input.outputs[2], noise_texture.inputs[1])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT_VECTOR"
    map_range.inputs[0].default_value = 1.0
    map_range.inputs[1].default_value = 0.0
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[3].default_value = 0.0
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[9].default_value = [-1.0, -1.0, -1.0]
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(noise_texture.outputs[1], map_range.inputs[6])

    mesh_to_curve_002 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.mode = "EDGES"
    mesh_to_curve_002.inputs[1].default_value = True
    links.new(repeat_output.outputs[0], mesh_to_curve_002.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.inputs[3].default_value = False
    links.new(mesh_to_curve_002.outputs[0], curve_to_mesh_001.inputs[0])

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.mode = "RADIUS"
    curve_circle.inputs[0].default_value = 6
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle.inputs[4].default_value = 0.0010000000474974513
    links.new(curve_circle.outputs[0], curve_to_mesh_001.inputs[1])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")

    math_004 = nodes.new("ShaderNodeMath")
    math_004.operation = "SUBTRACT"
    math_004.inputs[0].default_value = 1.0
    math_004.inputs[2].default_value = 0.5
    links.new(math_004.outputs[0], curve_to_mesh_001.inputs[2])
    links.new(spline_parameter.outputs[0], math_004.inputs[1])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.operation = "CROSS_PRODUCT"
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math.inputs[3].default_value = 1.0
    links.new(map_range.outputs[1], vector_math.inputs[0])
    links.new(distribute_points_on_faces.outputs[1], vector_math.inputs[1])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.operation = "NORMALIZE"
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[3].default_value = 1.0
    links.new(vector_math_001.outputs[0], extrude_mesh_001.inputs[2])
    links.new(vector_math.outputs[0], vector_math_001.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.target_element = "FACES"
    geometry_proximity.inputs[1].default_value = 0
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity.inputs[3].default_value = 0

    group_input_001 = nodes.new("NodeGroupInput")
    links.new(group_input_001.outputs[0], geometry_proximity.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "LESS_EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    compare.inputs[1].default_value = 0.0010000000474974513
    compare.inputs[2].default_value = 0
    compare.inputs[3].default_value = 0
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[8].default_value = ""
    compare.inputs[9].default_value = ""
    compare.inputs[10].default_value = 0.8999999761581421
    compare.inputs[11].default_value = 0.08726649731397629
    compare.inputs[12].default_value = 0.0010000000474974513
    links.new(geometry_proximity.outputs[1], compare.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "AND"
    links.new(boolean_math.outputs[0], repeat_output.inputs[1])
    links.new(extrude_mesh_001.outputs[1], boolean_math.inputs[0])
    links.new(compare.outputs[0], boolean_math.inputs[1])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "gold"
    store_named_attribute.inputs[3].default_value = True
    links.new(store_named_attribute.outputs[0], group_output.inputs[0])
    links.new(curve_to_mesh_001.outputs[0], store_named_attribute.inputs[0])

    auto_layout_nodes(group)
    return group
