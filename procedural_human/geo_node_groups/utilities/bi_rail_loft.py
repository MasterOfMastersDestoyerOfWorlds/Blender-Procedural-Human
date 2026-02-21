import bpy
from mathutils import Vector, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group
from procedural_human.geo_node_groups.utilities.space_switch import create_space_res_switch_group
from procedural_human.geo_node_groups.node_helpers import (
    combine_xyz,
    get_or_rebuild_node_group,
    math_op,
    separate_xyz,
)


@geo_node_group
def create_bi_rail_loft_group():
    group_name = "Bi-Rail Loft"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

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
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.inputs[1].default_value = True
    realize_instances.inputs[2].default_value = True
    realize_instances.inputs[3].default_value = 0
    links.new(group_input.outputs[2], realize_instances.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Count"
    resample_curve.inputs[4].default_value = 0.10000000149011612

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.keep_last_segment = True
    resample_curve_001.inputs[1].default_value = True
    resample_curve_001.inputs[2].default_value = "Count"
    resample_curve_001.inputs[4].default_value = 0.10000000149011612

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.inputs[1].default_value = True
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))

    evaluate_at_index = nodes.new("GeometryNodeFieldAtIndex")
    evaluate_at_index.domain = "POINT"
    evaluate_at_index.data_type = "FLOAT_VECTOR"

    position = nodes.new("GeometryNodeInputPosition")
    links.new(position.outputs[0], evaluate_at_index.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.operation = "MULTIPLY_ADD"
    vector_math.inputs[1].default_value = [-1.0, -1.0, -1.0]
    vector_math.inputs[3].default_value = -1.0
    links.new(position.outputs[0], vector_math.inputs[2])
    links.new(evaluate_at_index.outputs[0], vector_math.inputs[0])

    spline_length = nodes.new("GeometryNodeSplineLength")

    index = nodes.new("GeometryNodeInputIndex")

    spline_parameter = nodes.new("GeometryNodeSplineParameter")

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.operation = "SUBTRACT"
    integer_math.inputs[2].default_value = 0
    links.new(integer_math.outputs[0], evaluate_at_index.inputs[1])
    links.new(index.outputs[0], integer_math.inputs[0])
    links.new(spline_parameter.outputs[2], integer_math.inputs[1])

    integer_math_001 = nodes.new("FunctionNodeIntegerMath")
    integer_math_001.operation = "ADD"
    integer_math_001.inputs[2].default_value = 0
    links.new(integer_math.outputs[0], integer_math_001.inputs[0])

    integer_math_002 = nodes.new("FunctionNodeIntegerMath")
    integer_math_002.operation = "SUBTRACT"
    integer_math_002.inputs[1].default_value = 1
    integer_math_002.inputs[2].default_value = 0
    links.new(spline_length.outputs[1], integer_math_002.inputs[0])
    links.new(integer_math_002.outputs[0], integer_math_001.inputs[1])

    rotate_vector = nodes.new("FunctionNodeRotateVector")
    links.new(vector_math.outputs[0], rotate_vector.inputs[0])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector.inputs[1].default_value = 1.0

    evaluate_at_index_001 = nodes.new("GeometryNodeFieldAtIndex")
    evaluate_at_index_001.domain = "POINT"
    evaluate_at_index_001.data_type = "FLOAT_VECTOR"
    links.new(integer_math_001.outputs[0], evaluate_at_index_001.inputs[1])
    links.new(position.outputs[0], evaluate_at_index_001.inputs[0])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.operation = "SUBTRACT"
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[3].default_value = 1.0
    links.new(evaluate_at_index.outputs[0], vector_math_001.inputs[1])
    links.new(evaluate_at_index_001.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], align_rotation_to_vector.inputs[2])

    invert_rotation = nodes.new("FunctionNodeInvertRotation")
    links.new(align_rotation_to_vector.outputs[0], invert_rotation.inputs[0])
    links.new(invert_rotation.outputs[0], rotate_vector.inputs[1])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.operation = "SCALE"
    vector_math_002.inputs[1].default_value = [-1.0, -1.0, -1.0]
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(vector_math_002.outputs[0], set_position.inputs[2])
    links.new(rotate_vector.outputs[0], vector_math_002.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.operation = "LENGTH"
    vector_math_003.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_003.inputs[3].default_value = 1.0
    links.new(vector_math_001.outputs[0], vector_math_003.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.operation = "DIVIDE"
    math.inputs[0].default_value = 1.0
    math.inputs[2].default_value = 0.5
    links.new(math.outputs[0], vector_math_002.inputs[3])
    links.new(vector_math_003.outputs[1], math.inputs[1])

    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.keep_last_segment = True
    resample_curve_002.inputs[1].default_value = True
    resample_curve_002.inputs[2].default_value = "Evaluated"
    resample_curve_002.inputs[3].default_value = 10
    resample_curve_002.inputs[4].default_value = 0.10000000149011612
    links.new(resample_curve_002.outputs[0], set_position.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.domain = "CURVE"
    links.new(set_position.outputs[0], separate_geometry.inputs[0])

    index_001 = nodes.new("GeometryNodeInputIndex")
    links.new(index_001.outputs[0], separate_geometry.inputs[1])

    duplicate_elements = nodes.new("GeometryNodeDuplicateElements")
    duplicate_elements.domain = "SPLINE"
    duplicate_elements.inputs[1].default_value = True
    links.new(separate_geometry.outputs[1], duplicate_elements.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[1].default_value = True
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(duplicate_elements.outputs[0], set_position_001.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.operation = "DIVIDE"
    math_001.inputs[2].default_value = 0.5
    links.new(duplicate_elements.outputs[1], math_001.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketInt"
    links.new(reroute_001.outputs[0], duplicate_elements.inputs[2])

    integer_math_003 = nodes.new("FunctionNodeIntegerMath")
    integer_math_003.operation = "SUBTRACT"
    integer_math_003.inputs[1].default_value = 1
    integer_math_003.inputs[2].default_value = 0
    links.new(reroute_001.outputs[0], integer_math_003.inputs[0])
    links.new(integer_math_003.outputs[0], math_001.inputs[1])

    frame_002 = nodes.new("NodeFrame")
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.component = "CURVE"
    links.new(separate_geometry.outputs[0], domain_size.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.operation = "MULTIPLY"
    math_002.inputs[2].default_value = 0.5
    links.new(domain_size.outputs[4], math_002.inputs[1])

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = False
    sample_curve.data_type = "FLOAT"
    sample_curve.inputs[1].default_value = 0.0
    sample_curve.inputs[3].default_value = 0.0

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_001.outputs[0], sample_curve.inputs[2])

    float_to_integer = nodes.new("FunctionNodeFloatToInt")
    float_to_integer.rounding_mode = "FLOOR"
    links.new(float_to_integer.outputs[0], sample_curve.inputs[4])
    links.new(math_002.outputs[0], float_to_integer.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.operation = "FRACT"
    math_003.inputs[1].default_value = 0.5
    math_003.inputs[2].default_value = 0.5
    links.new(math_002.outputs[0], math_003.inputs[0])

    mix = nodes.new("ShaderNodeMix")
    mix.data_type = "VECTOR"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    mix.inputs[2].default_value = 0.0
    mix.inputs[3].default_value = 0.0
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    links.new(math_003.outputs[0], mix.inputs[0])
    links.new(sample_curve.outputs[1], mix.inputs[4])
    links.new(mix.outputs[1], set_position_001.inputs[2])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.socket_idname = "NodeSocketGeometry"
    links.new(reroute_002.outputs[0], sample_curve.inputs[0])

    sample_curve_001 = nodes.new("GeometryNodeSampleCurve")
    sample_curve_001.mode = "FACTOR"
    sample_curve_001.use_all_curves = False
    sample_curve_001.data_type = "FLOAT"
    sample_curve_001.inputs[1].default_value = 0.0
    sample_curve_001.inputs[3].default_value = 0.0
    links.new(reroute_002.outputs[0], sample_curve_001.inputs[0])
    links.new(sample_curve_001.outputs[1], mix.inputs[5])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_002.outputs[0], sample_curve_001.inputs[2])

    integer_math_004 = nodes.new("FunctionNodeIntegerMath")
    integer_math_004.operation = "ADD"
    integer_math_004.inputs[1].default_value = 1
    integer_math_004.inputs[2].default_value = 0
    links.new(integer_math_004.outputs[0], sample_curve_001.inputs[4])
    links.new(float_to_integer.outputs[0], integer_math_004.inputs[0])

    frame_003 = nodes.new("NodeFrame")
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.socket_idname = "NodeSocketGeometry"
    links.new(set_position.outputs[0], reroute_003.inputs[0])
    links.new(reroute_003.outputs[0], reroute_002.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.inputs[1].default_value = True
    instance_on_points.inputs[3].default_value = True
    instance_on_points.inputs[4].default_value = 0

    split_to_instances = nodes.new("GeometryNodeSplitToInstances")
    split_to_instances.domain = "CURVE"
    split_to_instances.inputs[1].default_value = True
    links.new(set_position_001.outputs[0], split_to_instances.inputs[0])
    links.new(duplicate_elements.outputs[1], split_to_instances.inputs[2])
    links.new(split_to_instances.outputs[0], instance_on_points.inputs[2])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    links.new(resample_curve_001.outputs[0], sample_index.inputs[0])

    index_002 = nodes.new("GeometryNodeInputIndex")
    links.new(index_002.outputs[0], sample_index.inputs[2])

    position_001 = nodes.new("GeometryNodeInputPosition")
    links.new(position_001.outputs[0], sample_index.inputs[1])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.operation = "SUBTRACT"
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_004.inputs[3].default_value = 1.0
    links.new(position_001.outputs[0], vector_math_004.inputs[1])
    links.new(sample_index.outputs[0], vector_math_004.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.operation = "LENGTH"
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_005.inputs[3].default_value = 1.0
    links.new(vector_math_005.outputs[1], instance_on_points.inputs[6])
    links.new(vector_math_004.outputs[0], vector_math_005.inputs[0])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.axis = "X"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    align_rotation_to_vector_001.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    links.new(vector_math_004.outputs[0], align_rotation_to_vector_001.inputs[2])

    curve_tangent = nodes.new("GeometryNodeInputTangent")

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.operation = "CROSS_PRODUCT"
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_006.inputs[3].default_value = 1.0
    links.new(curve_tangent.outputs[0], vector_math_006.inputs[1])
    links.new(vector_math_004.outputs[0], vector_math_006.inputs[0])

    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.axis = "Y"
    align_rotation_to_vector_002.pivot_axis = "X"
    align_rotation_to_vector_002.inputs[1].default_value = 1.0
    links.new(align_rotation_to_vector_002.outputs[0], instance_on_points.inputs[5])
    links.new(align_rotation_to_vector_001.outputs[0], align_rotation_to_vector_002.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.inputs[1].default_value = True
    realize_instances_001.inputs[2].default_value = True
    realize_instances_001.inputs[3].default_value = 0
    links.new(instance_on_points.outputs[0], realize_instances_001.inputs[0])

    resample_curve_003 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.keep_last_segment = True
    resample_curve_003.inputs[1].default_value = True
    resample_curve_003.inputs[2].default_value = "Count"
    resample_curve_003.inputs[4].default_value = 0.10000000149011612
    links.new(realize_instances_001.outputs[0], resample_curve_003.inputs[0])

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.inputs[0].default_value = 1.0
    grid.inputs[1].default_value = 1.0

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.inputs[1].default_value = True
    set_position_002.inputs[3].default_value = Vector((0.0, 0.0, 0.0))

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    links.new(resample_curve_003.outputs[0], sample_index_001.inputs[0])
    links.new(sample_index_001.outputs[0], set_position_002.inputs[2])

    position_002 = nodes.new("GeometryNodeInputPosition")
    links.new(position_002.outputs[0], sample_index_001.inputs[1])

    index_003 = nodes.new("GeometryNodeInputIndex")
    links.new(index_003.outputs[0], sample_index_001.inputs[2])

    set_position_005 = nodes.new("GeometryNodeSetPosition")
    set_position_005.inputs[1].default_value = True
    set_position_005.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(set_position_002.outputs[0], set_position_005.inputs[0])
    links.new(set_position_005.outputs[0], group_output.inputs[0])

    position_005 = nodes.new("GeometryNodeInputPosition")

    blur_attribute = nodes.new("GeometryNodeBlurAttribute")
    blur_attribute.data_type = "FLOAT_VECTOR"
    links.new(blur_attribute.outputs[0], set_position_005.inputs[2])
    links.new(position_005.outputs[0], blur_attribute.inputs[0])

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.node_tree = create_is__edge__boundary_group()

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "NOT"
    boolean_math.inputs[1].default_value = False
    links.new(is_edge_boundary.outputs[0], boolean_math.inputs[0])
    links.new(boolean_math.outputs[0], blur_attribute.inputs[2])

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.data_type = "FLOAT"
    attribute_statistic.domain = "CURVE"
    attribute_statistic.inputs[1].default_value = True
    links.new(realize_instances_001.outputs[0], attribute_statistic.inputs[0])

    spline_length_001 = nodes.new("GeometryNodeSplineLength")
    links.new(spline_length_001.outputs[0], attribute_statistic.inputs[2])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.operation = "DIVIDE"
    math_004.inputs[2].default_value = 0.5
    links.new(attribute_statistic.outputs[3], math_004.inputs[0])

    group_input_001 = nodes.new("NodeGroupInput")
    links.new(group_input_001.outputs[0], resample_curve.inputs[0])
    links.new(group_input_001.outputs[1], resample_curve_001.inputs[0])

    curve_length = nodes.new("GeometryNodeCurveLength")
    links.new(group_input_001.outputs[0], curve_length.inputs[0])

    curve_length_001 = nodes.new("GeometryNodeCurveLength")
    links.new(group_input_001.outputs[1], curve_length_001.inputs[0])

    min_curve_length = math_op(group, "MINIMUM", curve_length.outputs[0], curve_length_001.outputs[0])
    spacing_len = math_op(group, "DIVIDE", min_curve_length, group_input_001.outputs[6])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "FLOAT2"
    store_named_attribute.domain = "CORNER"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "UVMap"
    links.new(store_named_attribute.outputs[0], set_position_002.inputs[0])
    links.new(grid.outputs[0], store_named_attribute.inputs[0])

    uv_x, uv_y, _ = separate_xyz(group, grid.outputs[1])
    links.new(combine_xyz(group, uv_y, uv_x, 0.0), store_named_attribute.inputs[3])

    group_input_002 = nodes.new("NodeGroupInput")
    links.new(group_input_002.outputs[3], blur_attribute.inputs[1])

    group_input_003 = nodes.new("NodeGroupInput")
    links.new(group_input_003.outputs[5], math_004.inputs[1])

    links.new(group_input_003.outputs[7], resample_curve_003.inputs[3])
    links.new(group_input_003.outputs[7], grid.inputs[3])

    links.new(group_input_001.outputs[8], resample_curve.inputs[3])
    links.new(group_input_001.outputs[8], resample_curve_001.inputs[3])
    links.new(group_input_001.outputs[8], grid.inputs[2])
    links.new(group_input_001.outputs[8], reroute_001.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.data_type = "FLOAT_VECTOR"
    named_attribute.inputs[0].default_value = "UVMap"
    links.new(named_attribute.outputs[0], group_output.inputs[2])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.data_type = "FLOAT2"
    store_named_attribute_001.domain = "POINT"
    store_named_attribute_001.inputs[1].default_value = True
    store_named_attribute_001.inputs[2].default_value = "UVMap"
    links.new(store_named_attribute_001.outputs[0], group_output.inputs[1])
    links.new(resample_curve_003.outputs[0], store_named_attribute_001.inputs[0])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.inputs[2].default_value = 0.0
    links.new(combine_x_y_z_001.outputs[0], store_named_attribute_001.inputs[3])

    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_003.outputs[0], combine_x_y_z_001.inputs[0])

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    links.new(capture_attribute.outputs[0], instance_on_points.inputs[0])
    links.new(resample_curve.outputs[0], capture_attribute.inputs[0])
    links.new(capture_attribute.outputs[1], combine_x_y_z_001.inputs[1])

    spline_parameter_004 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_004.outputs[0], capture_attribute.inputs[1])

    field_average = nodes.new("GeometryNodeFieldAverage")
    field_average.data_type = "FLOAT_VECTOR"
    field_average.domain = "POINT"
    field_average.inputs[1].default_value = 0
    links.new(vector_math_006.outputs[0], field_average.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "EQUAL"
    compare.data_type = "VECTOR"
    compare.mode = "DIRECTION"
    compare.inputs[0].default_value = 0.0
    compare.inputs[1].default_value = 0.0
    compare.inputs[2].default_value = 0
    compare.inputs[3].default_value = 0
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[8].default_value = ""
    compare.inputs[9].default_value = ""
    compare.inputs[10].default_value = 0.8999999761581421
    compare.inputs[11].default_value = 0.0
    compare.inputs[12].default_value = 1.5707963705062866
    links.new(vector_math_006.outputs[0], compare.inputs[4])
    links.new(field_average.outputs[0], compare.inputs[5])

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "FLOAT"
    switch.inputs[1].default_value = -1.0
    switch.inputs[2].default_value = 1.0
    links.new(compare.outputs[0], switch.inputs[0])

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.operation = "SCALE"
    vector_math_007.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(vector_math_007.outputs[0], align_rotation_to_vector_002.inputs[2])
    links.new(vector_math_006.outputs[0], vector_math_007.inputs[0])
    links.new(switch.outputs[0], vector_math_007.inputs[3])

    domain_size_001 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_001.component = "CURVE"

    separate_components = nodes.new("GeometryNodeSeparateComponents")
    links.new(realize_instances.outputs[0], separate_components.inputs[0])
    links.new(separate_components.outputs[1], domain_size_001.inputs[0])

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.mode = "POINTS"
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    curve_line.inputs[1].default_value = Vector((0.0, 0.0, 1.0))
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    curve_line.inputs[3].default_value = 1.0

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "GEOMETRY"
    links.new(switch_001.outputs[0], resample_curve_002.inputs[0])
    links.new(separate_components.outputs[1], switch_001.inputs[1])
    links.new(curve_line.outputs[0], switch_001.inputs[2])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.operation = "EQUAL"
    compare_001.data_type = "INT"
    compare_001.mode = "ELEMENT"
    compare_001.inputs[0].default_value = 0.0
    compare_001.inputs[1].default_value = 0.0
    compare_001.inputs[3].default_value = 0
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[8].default_value = ""
    compare_001.inputs[9].default_value = ""
    compare_001.inputs[10].default_value = 0.8999999761581421
    compare_001.inputs[11].default_value = 0.08726649731397629
    compare_001.inputs[12].default_value = 0.0010000000474974513
    links.new(domain_size_001.outputs[4], compare_001.inputs[2])
    links.new(compare_001.outputs[0], switch_001.inputs[0])

    group_input_004 = nodes.new("NodeGroupInput")

    evaluate_closure = nodes.new("NodeEvaluateClosure")
    evaluate_closure.active_input_index = 0
    evaluate_closure.active_output_index = 0
    evaluate_closure.define_signature = False
    links.new(math_001.outputs[0], evaluate_closure.inputs[1])
    links.new(group_input_004.outputs[9], evaluate_closure.inputs[0])
    links.new(evaluate_closure.outputs[0], math_002.inputs[0])

    auto_layout_nodes(group)
    return group
