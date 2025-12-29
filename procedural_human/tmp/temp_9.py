import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_mix_angle_grouped_group():
    group_name = "MixAngleGrouped"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Result", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="CurveA", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Factor", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.5
    socket.min_value = -3.4028234663852886e+38 
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="CurveA", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="AngleA", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="CurveB", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="AngleB", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Switch", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1412.225830078125, -35.85774612426758)
    group_input.bl_label = "Group Input"
    # Links for group_input

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (587.7741088867188, -35.85774612426758)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output
    links.new(group_input.outputs[1], group_output.inputs[1])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = "Sample AngleA[0]"
    sample_index.location = (-1160.479248046875, 170.98989868164062)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Links for sample_index
    links.new(group_input.outputs[3], sample_index.inputs[2])
    links.new(group_input.outputs[2], sample_index.inputs[1])
    links.new(group_input.outputs[1], sample_index.inputs[0])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = "Sample AngleB[0]"
    sample_index_001.location = (-1162.225830078125, -35.85774612426758)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001
    links.new(group_input.outputs[6], sample_index_001.inputs[2])
    links.new(group_input.outputs[5], sample_index_001.inputs[1])
    links.new(group_input.outputs[4], sample_index_001.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-912.2258911132812, 114.14225769042969)
    math.bl_label = "Math"
    math.operation = "SUBTRACT"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(sample_index_001.outputs[0], math.inputs[0])
    links.new(sample_index.outputs[0], math.inputs[1])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-662.2258911132812, 39.14225387573242)
    math_001.bl_label = "Math"
    math_001.operation = "ADD"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 3.1415927410125732
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math.outputs[0], math_001.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (-412.2258605957031, 39.14225387573242)
    math_002.bl_label = "Math"
    math_002.operation = "FLOORED_MODULO"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 6.2831854820251465
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(math_001.outputs[0], math_002.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = "Ref Delta"
    math_003.location = (-162.2258758544922, 39.14225387573242)
    math_003.bl_label = "Math"
    math_003.operation = "SUBTRACT"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 3.1415927410125732
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_002.outputs[0], math_003.inputs[0])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = "Raw Delta"
    math_004.location = (-1150.8731689453125, -282.0614929199219)
    math_004.bl_label = "Math"
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(group_input.outputs[6], math_004.inputs[0])
    links.new(group_input.outputs[3], math_004.inputs[1])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (87.77412414550781, 39.14225387573242)
    math_005.bl_label = "Math"
    math_005.operation = "SUBTRACT"
    math_005.use_clamp = False
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(math_004.outputs[0], math_005.inputs[0])
    links.new(math_003.outputs[0], math_005.inputs[1])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (-662.2258911132812, -110.85774230957031)
    math_006.bl_label = "Math"
    math_006.operation = "ADD"
    math_006.use_clamp = False
    # Value
    math_006.inputs[1].default_value = 3.1415927410125732
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(math_005.outputs[0], math_006.inputs[0])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.label = ""
    math_007.location = (-412.2258605957031, -110.85774230957031)
    math_007.bl_label = "Math"
    math_007.operation = "FLOORED_MODULO"
    math_007.use_clamp = False
    # Value
    math_007.inputs[1].default_value = 6.2831854820251465
    # Value
    math_007.inputs[2].default_value = 0.5
    # Links for math_007
    links.new(math_006.outputs[0], math_007.inputs[0])

    math_008 = nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.label = ""
    math_008.location = (-162.2258758544922, -110.85774230957031)
    math_008.bl_label = "Math"
    math_008.operation = "SUBTRACT"
    math_008.use_clamp = False
    # Value
    math_008.inputs[1].default_value = 3.1415927410125732
    # Value
    math_008.inputs[2].default_value = 0.5
    # Links for math_008
    links.new(math_007.outputs[0], math_008.inputs[0])

    math_009 = nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.label = "Aligned Delta"
    math_009.location = (87.77412414550781, -110.85774230957031)
    math_009.bl_label = "Math"
    math_009.operation = "ADD"
    math_009.use_clamp = False
    # Value
    math_009.inputs[2].default_value = 0.5
    # Links for math_009
    links.new(math_003.outputs[0], math_009.inputs[0])
    links.new(math_008.outputs[0], math_009.inputs[1])

    math_010 = nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.label = ""
    math_010.location = (319.5939636230469, -215.63510131835938)
    math_010.bl_label = "Math"
    math_010.operation = "MULTIPLY"
    math_010.use_clamp = False
    # Value
    math_010.inputs[2].default_value = 0.5
    # Links for math_010
    links.new(math_009.outputs[0], math_010.inputs[0])
    links.new(group_input.outputs[0], math_010.inputs[1])

    math_011 = nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.label = ""
    math_011.location = (-935.651611328125, -115.947509765625)
    math_011.bl_label = "Math"
    math_011.operation = "ADD"
    math_011.use_clamp = False
    # Value
    math_011.inputs[2].default_value = 0.5
    # Links for math_011
    links.new(group_input.outputs[3], math_011.inputs[0])
    links.new(math_010.outputs[0], math_011.inputs[1])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (-687.6624145507812, -250.5767059326172)
    switch.bl_label = "Switch"
    switch.input_type = "FLOAT"
    # Links for switch
    links.new(math_011.outputs[0], switch.inputs[1])
    links.new(math_011.outputs[0], switch.inputs[2])
    links.new(switch.outputs[0], group_output.inputs[0])
    links.new(group_input.outputs[7], switch.inputs[0])

    auto_layout_nodes(group)
    return group