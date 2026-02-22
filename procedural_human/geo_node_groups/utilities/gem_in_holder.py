import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import (
    combine_xyz,
    get_or_rebuild_node_group,
    math_op,
    separate_xyz,
)

@geo_node_group
def create_gem_in__holder_group():
    group_name = "Gem in Holder"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

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
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.inputs[1].default_value = 2

    dual_mesh = nodes.new("GeometryNodeDualMesh")
    dual_mesh.inputs[1].default_value = False
    links.new(ico_sphere_001.outputs[0], dual_mesh.inputs[0])

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.mode = "RADIUS"
    curve_circle.inputs[0].default_value = 24
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    links.new(group_input.outputs[0], curve_circle.inputs[4])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.inputs[3].default_value = False
    links.new(curve_circle.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(group_input.outputs[3], curve_to_mesh_002.inputs[2])

    points = nodes.new("GeometryNodePoints")
    points.inputs[2].default_value = 0.10000000149011612
    links.new(group_input.outputs[4], points.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.data_type = "FLOAT_VECTOR"
    random_value.inputs[0].default_value = [-0.5, -1.0, 0.0]
    random_value.inputs[1].default_value = [0.5, 1.0, 0.0]
    random_value.inputs[2].default_value = 0.0
    random_value.inputs[3].default_value = 1.0
    random_value.inputs[4].default_value = 0
    random_value.inputs[5].default_value = 100
    random_value.inputs[6].default_value = 0.5
    random_value.inputs[7].default_value = 0
    links.new(random_value.outputs[0], points.inputs[1])
    links.new(group_input.outputs[5], random_value.inputs[8])

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.inputs[1].default_value = 0
    links.new(points.outputs[0], points_to_curves.inputs[0])

    gradient_texture = nodes.new("ShaderNodeTexGradient")
    gradient_texture.gradient_type = "RADIAL"
    gradient_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    links.new(gradient_texture.outputs[1], points_to_curves.inputs[2])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.inputs[1].default_value = True
    set_spline_cyclic.inputs[2].default_value = True
    links.new(points_to_curves.outputs[0], set_spline_cyclic.inputs[0])

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.spline_type = "NURBS"
    set_spline_type.inputs[1].default_value = True
    links.new(set_spline_cyclic.outputs[0], set_spline_type.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.inputs[1].default_value = "Components"
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 0.6000000238418579))

    points_to_vertices = nodes.new("GeometryNodePointsToVertices")
    points_to_vertices.inputs[1].default_value = True

    extrude_mesh_001 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.mode = "VERTICES"
    extrude_mesh_001.inputs[3].default_value = 0.0020000000949949026
    extrude_mesh_001.inputs[4].default_value = True
    
    repeat_output_001 = nodes.new("GeometryNodeRepeatOutput")
    repeat_output_001.active_index = 2
    repeat_output_001.inspection_index = 0
    repeat_output_001.repeat_items.new("BOOLEAN", "Top")
    repeat_output_001.repeat_items.new("VECTOR", "Value")

    repeat_input_001 = nodes.new("GeometryNodeRepeatInput")
    repeat_input_001.pair_with_output(repeat_output_001)
    repeat_input_001.inputs[2].default_value = True
    repeat_input_001.inputs[3].default_value = [0.0, 0.0, 0.0]
    repeat_input_001.inputs[0].default_value = 60
    links.new(repeat_input_001.outputs[2], extrude_mesh_001.inputs[1])
    links.new(repeat_input_001.outputs[1], extrude_mesh_001.inputs[0])
    links.new(points_to_vertices.outputs[0], repeat_input_001.inputs[1])

    links.new(extrude_mesh_001.outputs[1], repeat_output_001.inputs[1])
    links.new(extrude_mesh_001.outputs[0], repeat_output_001.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = False
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    noise_texture.inputs[2].default_value = 30.0
    noise_texture.inputs[3].default_value = 0.0
    noise_texture.inputs[4].default_value = 0.5
    noise_texture.inputs[5].default_value = 2.0
    noise_texture.inputs[6].default_value = 0.0
    noise_texture.inputs[7].default_value = 1.0
    noise_texture.inputs[8].default_value = 0.0

    mesh_to_curve_003 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_003.mode = "EDGES"
    mesh_to_curve_003.inputs[1].default_value = True
    links.new(repeat_output_001.outputs[0], mesh_to_curve_003.inputs[0])

    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.inputs[3].default_value = False

    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.inputs[0].default_value = 1.0
    links.new(spline_parameter_003.outputs[0], float_curve.inputs[1])

    profile_scale = math_op(group, "MULTIPLY", float_curve.outputs[0], 0.004999999888241291)
    links.new(profile_scale, curve_to_mesh_003.inputs[2])
    links.new(profile_scale, group_output.inputs[2])

    points_001 = nodes.new("GeometryNodePoints")
    points_001.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    points_001.inputs[2].default_value = 0.10000000149011612

    index = nodes.new("GeometryNodeInputIndex")

    capture_attribute_007 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_007.capture_items.new("INT", "Value")
    capture_attribute_007.active_index = 0
    capture_attribute_007.domain = "POINT"
    links.new(capture_attribute_007.outputs[0], points_to_vertices.inputs[0])
    links.new(points_001.outputs[0], capture_attribute_007.inputs[0])
    links.new(index.outputs[0], capture_attribute_007.inputs[1])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.operation = "MULTIPLY_ADD"
    links.new(capture_attribute_007.outputs[1], math_001.inputs[0])
    links.new(math_001.outputs[0], noise_texture.inputs[1])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.inputs[1].default_value = "Components"
    transform_geometry_006.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_006.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    links.new(curve_to_mesh_003.outputs[0], transform_geometry_006.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.inputs[1].default_value = True
    links.new(transform_geometry_006.outputs[0], flip_faces_001.inputs[0])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    links.new(flip_faces_001.outputs[0], join_geometry_003.inputs[0])
    links.new(curve_to_mesh_003.outputs[0], join_geometry_003.inputs[0])

    instance_on_points_003 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.inputs[1].default_value = True
    instance_on_points_003.inputs[3].default_value = False
    instance_on_points_003.inputs[4].default_value = 0
    instance_on_points_003.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    links.new(join_geometry_003.outputs[0], instance_on_points_003.inputs[2])

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.mode = "RADIUS"
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_001.inputs[4].default_value = 9.999999747378752e-05
    links.new(curve_circle_001.outputs[0], instance_on_points_003.inputs[0])

    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.axis = "X"
    align_rotation_to_vector_002.pivot_axis = "AUTO"
    align_rotation_to_vector_002.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_002.inputs[1].default_value = 1.0
    links.new(align_rotation_to_vector_002.outputs[0], instance_on_points_003.inputs[5])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_002.inputs[2])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")

    realize_instances_003 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.inputs[1].default_value = True
    realize_instances_003.inputs[2].default_value = True
    realize_instances_003.inputs[3].default_value = 0
    links.new(instance_on_points_003.outputs[0], realize_instances_003.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "GEOMETRY"
    links.new(switch.outputs[0], transform_geometry_005.inputs[0])
    links.new(dual_mesh.outputs[0], switch.inputs[2])
    links.new(ico_sphere_001.outputs[0], switch.inputs[1])

    group_input_001 = nodes.new("NodeGroupInput")
    links.new(group_input_001.outputs[0], ico_sphere_001.inputs[0])
    links.new(group_input_001.outputs[2], switch.inputs[0])

    group_input_002 = nodes.new("NodeGroupInput")
    links.new(group_input_002.outputs[8], points_001.inputs[0])
    links.new(group_input_002.outputs[9], math_001.inputs[1])
    links.new(group_input_002.outputs[10], math_001.inputs[2])

    group_input_003 = nodes.new("NodeGroupInput")
    links.new(group_input_003.outputs[7], curve_circle_001.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.text = None
    frame.shrink = True
    frame.label_size = 20

    frame_001 = nodes.new("NodeFrame")
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20

    frame_002 = nodes.new("NodeFrame")
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20

    frame_003 = nodes.new("NodeFrame")
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20

    frame_004 = nodes.new("NodeFrame")
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20

    frame_005 = nodes.new("NodeFrame")
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "gold"
    store_named_attribute.inputs[3].default_value = True
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    links.new(store_named_attribute.outputs[0], join_geometry_005.inputs[0])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    store_named_attribute_001.inputs[1].default_value = True
    store_named_attribute_001.inputs[3].default_value = True
    links.new(transform_geometry_005.outputs[0], store_named_attribute_001.inputs[0])
    links.new(store_named_attribute_001.outputs[0], join_geometry_005.inputs[0])
    links.new(group_input_001.outputs[1], store_named_attribute_001.inputs[2])

    mix = nodes.new("ShaderNodeMix")
    mix.data_type = "VECTOR"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    mix.inputs[2].default_value = 0.0
    mix.inputs[3].default_value = 0.0
    mix.inputs[4].default_value = [1.0, 1.0, 0.0]
    mix.inputs[5].default_value = [1.0, 1.0, 1.0]
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.operation = "MULTIPLY"
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math.inputs[3].default_value = 1.0
    links.new(vector_math.outputs[0], extrude_mesh_001.inputs[2])
    links.new(mix.outputs[1], vector_math.inputs[1])

    position = nodes.new("GeometryNodeInputPosition")

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.operation = "LENGTH"
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[3].default_value = 1.0
    links.new(position.outputs[0], vector_math_001.inputs[0])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    map_range.inputs[2].default_value = 0.05000000074505806
    map_range.inputs[3].default_value = 0.0
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(vector_math_001.outputs[1], map_range.inputs[0])
    links.new(map_range.outputs[0], mix.inputs[0])

    group_input_004 = nodes.new("NodeGroupInput")
    links.new(group_input_004.outputs[0], map_range.inputs[1])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    store_named_attribute_002.inputs[1].default_value = True
    store_named_attribute_002.inputs[2].default_value = "gold"
    store_named_attribute_002.inputs[3].default_value = True
    links.new(realize_instances_003.outputs[0], store_named_attribute_002.inputs[0])
    links.new(store_named_attribute_002.outputs[0], join_geometry_004.inputs[0])

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.inputs[1].default_value = "Components"
    transform_geometry.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(join_geometry_005.outputs[0], transform_geometry.inputs[0])
    links.new(transform_geometry.outputs[0], join_geometry_004.inputs[0])

    noise_x, noise_y, noise_z = separate_xyz(group, noise_texture.outputs[1])
    links.new(combine_xyz(group, noise_x, noise_y, math_op(group, "ABSOLUTE", noise_z)), vector_math.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Count"
    resample_curve.inputs[3].default_value = 12
    resample_curve.inputs[4].default_value = 0.10000000149011612
    links.new(resample_curve.outputs[0], curve_to_mesh_002.inputs[1])
    links.new(set_spline_type.outputs[0], resample_curve.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.keep_last_segment = True
    resample_curve_001.inputs[1].default_value = True
    resample_curve_001.inputs[2].default_value = "Length"
    resample_curve_001.inputs[3].default_value = 10
    resample_curve_001.inputs[4].default_value = 0.0007999999797903001
    links.new(resample_curve_001.outputs[0], curve_to_mesh_003.inputs[0])
    links.new(mesh_to_curve_003.outputs[0], resample_curve_001.inputs[0])
    links.new(resample_curve_001.outputs[0], group_output.inputs[4])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "GEOMETRY"
    links.new(switch_001.outputs[0], group_output.inputs[0])
    links.new(join_geometry_004.outputs[0], switch_001.inputs[2])
    links.new(join_geometry_005.outputs[0], switch_001.inputs[1])

    group_input_005 = nodes.new("NodeGroupInput")
    links.new(group_input_005.outputs[6], switch_001.inputs[0])

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.input_type = "VECTOR"
    switch_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(repeat_input_001.outputs[0], switch_002.inputs[0])
    links.new(vector_math.outputs[0], switch_002.inputs[1])

    evaluate_at_index = nodes.new("GeometryNodeFieldAtIndex")
    evaluate_at_index.domain = "POINT"
    evaluate_at_index.data_type = "FLOAT_VECTOR"
    evaluate_at_index.inputs[1].default_value = 0
    links.new(switch_002.outputs[0], evaluate_at_index.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.operation = "ADD"
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[3].default_value = 1.0
    links.new(vector_math_002.outputs[0], repeat_output_001.inputs[1])
    links.new(evaluate_at_index.outputs[0], vector_math_002.inputs[0])
    links.new(repeat_input_001.outputs[1], vector_math_002.inputs[1])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.inputs[1].default_value = "Components"
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(curve_to_mesh_003.outputs[0], transform_geometry_001.inputs[0])

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.data_type = "FLOAT_VECTOR"
    attribute_statistic.domain = "POINT"
    attribute_statistic.inputs[1].default_value = True
    links.new(repeat_output_001.outputs[0], attribute_statistic.inputs[0])
    links.new(repeat_output_001.outputs[1], attribute_statistic.inputs[2])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector.inputs[1].default_value = 1.0
    links.new(attribute_statistic.outputs[3], align_rotation_to_vector.inputs[2])

    invert_rotation = nodes.new("FunctionNodeInvertRotation")
    links.new(invert_rotation.outputs[0], transform_geometry_001.inputs[3])
    links.new(align_rotation_to_vector.outputs[0], invert_rotation.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    store_named_attribute_003.inputs[1].default_value = True
    store_named_attribute_003.inputs[2].default_value = "gold"
    store_named_attribute_003.inputs[3].default_value = True
    links.new(store_named_attribute_003.outputs[0], group_output.inputs[3])
    links.new(transform_geometry_001.outputs[0], store_named_attribute_003.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.socket_idname = "NodeSocketGeometry"
    links.new(reroute.outputs[0], curve_to_mesh_003.inputs[1])
    links.new(resample_curve.outputs[0], reroute.inputs[0])
    links.new(reroute.outputs[0], group_output.inputs[1])

    auto_layout_nodes(group)
    return group
