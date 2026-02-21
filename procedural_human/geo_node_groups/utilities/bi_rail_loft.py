import bpy
from mathutils import Vector, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_bi_rail_loft_group():
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

    space_res_switch = nodes.new("GeometryNodeGroup")
    space_res_switch.name = "Menu Switch.001"
    space_res_switch.label = ""
    space_res_switch.location = (2140.0, -120.0)
    space_res_switch.node_tree = create_space_res_switch_group()
    space_res_switch.bl_label = "Group"
    # Links for space_res_switch
    links.new(group_input_003.outputs[4], space_res_switch.inputs[0])
    links.new(group_input_003.outputs[7], space_res_switch.inputs[2])
    links.new(math_004.outputs[0], space_res_switch.inputs[1])
    links.new(space_res_switch.outputs[0], resample_curve_003.inputs[3])
    links.new(space_res_switch.outputs[0], grid.inputs[3])

    space_res_switch_1 = nodes.new("GeometryNodeGroup")
    space_res_switch_1.name = "Menu Switch.002"
    space_res_switch_1.label = ""
    space_res_switch_1.location = (-1720.0, 180.0)
    space_res_switch_1.node_tree = create_space_res_switch_group()
    space_res_switch_1.bl_label = "Group"
    # Links for space_res_switch_1
    links.new(space_res_switch_1.outputs[0], resample_curve.inputs[3])
    links.new(space_res_switch_1.outputs[0], resample_curve_001.inputs[3])
    links.new(space_res_switch_1.outputs[0], grid.inputs[2])
    links.new(space_res_switch_1.outputs[0], reroute_001.inputs[0])
    links.new(group_input_001.outputs[4], space_res_switch_1.inputs[0])
    links.new(math_006.outputs[0], space_res_switch_1.inputs[1])
    links.new(group_input_001.outputs[8], space_res_switch_1.inputs[2])

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

    auto_layout_nodes(group)
    return group
