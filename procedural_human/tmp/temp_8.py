import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_mix_angle_group():
    group_name = "MixAngle"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Result", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="CurveA", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Factor", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.5
    socket.min_value = 0.0
    socket.max_value = 1.0
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
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (954.6058349609375, 20.5975341796875)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1882.045166015625, 42.7957878112793)
    group_input.bl_label = "Group Input"
    # Links for group_input

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-1279.3902587890625, -520.3563232421875)
    math.bl_label = "Math"
    math.operation = "SUBTRACT"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-543.8701782226562, -164.4372100830078)
    math_001.bl_label = "Math"
    math_001.operation = "ADD"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 3.1415927410125732
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (-368.0755920410156, -116.69608306884766)
    math_002.bl_label = "Math"
    math_002.operation = "FLOORED_MODULO"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 6.2831854820251465
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(math_001.outputs[0], math_002.inputs[0])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (-149.05108642578125, -111.53486633300781)
    math_004.bl_label = "Math"
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 3.1415927410125732
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(math_002.outputs[0], math_004.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (59.28801727294922, -96.24229431152344)
    math_003.bl_label = "Math"
    math_003.operation = "MULTIPLY"
    math_003.use_clamp = False
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_004.outputs[0], math_003.inputs[0])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (-677.885009765625, 46.519989013671875)
    math_005.bl_label = "Math"
    math_005.operation = "ADD"
    math_005.use_clamp = True
    # Value
    math_005.inputs[1].default_value = 0.0
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(math_005.outputs[0], math_003.inputs[1])
    links.new(group_input.outputs[0], math_005.inputs[0])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (235.92349243164062, 67.64781951904297)
    math_006.bl_label = "Math"
    math_006.operation = "ADD"
    math_006.use_clamp = False
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(math_003.outputs[0], math_006.inputs[0])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (-1463.1798095703125, 182.95172119140625)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Links for sample_index
    links.new(group_input.outputs[2], sample_index.inputs[1])
    links.new(sample_index.outputs[0], math_006.inputs[1])
    links.new(sample_index.outputs[0], math.inputs[1])
    links.new(group_input.outputs[1], sample_index.inputs[0])
    links.new(group_input.outputs[3], sample_index.inputs[2])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (-1446.77587890625, -99.33316802978516)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001
    links.new(group_input.outputs[5], sample_index_001.inputs[1])
    links.new(group_input.outputs[4], sample_index_001.inputs[0])
    links.new(sample_index_001.outputs[0], math.inputs[0])
    links.new(group_input.outputs[6], sample_index_001.inputs[2])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (-682.1146850585938, -458.2689514160156)
    switch.bl_label = "Switch"
    switch.input_type = "FLOAT"
    # Switch
    switch.inputs[0].default_value = False
    # Links for switch
    links.new(switch.outputs[0], math_001.inputs[0])
    links.new(math.outputs[0], switch.inputs[2])
    links.new(math.outputs[0], switch.inputs[1])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (-1647.0853271484375, -835.358154296875)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "FLOAT"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "AngleA"
    # Links for store_named_attribute
    links.new(group_input.outputs[1], store_named_attribute.inputs[0])
    links.new(sample_index.outputs[0], store_named_attribute.inputs[3])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (-1321.3853759765625, -835.5430908203125)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "FLOAT"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "AngleB"
    # Links for store_named_attribute_001
    links.new(store_named_attribute.outputs[0], store_named_attribute_001.inputs[0])
    links.new(sample_index_001.outputs[0], store_named_attribute_001.inputs[3])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (-119.56083679199219, -844.861572265625)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "FLOAT"
    store_named_attribute_002.domain = "POINT"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "ree2"
    # Links for store_named_attribute_002
    links.new(store_named_attribute_002.outputs[0], group_output.inputs[1])
    links.new(math_002.outputs[0], store_named_attribute_002.inputs[3])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (-451.2740173339844, -856.4972534179688)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "FLOAT"
    store_named_attribute_003.domain = "POINT"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "sub"
    # Links for store_named_attribute_003
    links.new(store_named_attribute_003.outputs[0], store_named_attribute_002.inputs[0])
    links.new(switch.outputs[0], store_named_attribute_003.inputs[3])

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (-990.6939697265625, -924.33154296875)
    store_named_attribute_004.bl_label = "Store Named Attribute"
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "negativeQuad"
    # Links for store_named_attribute_004
    links.new(store_named_attribute_004.outputs[0], store_named_attribute_003.inputs[0])
    links.new(store_named_attribute_001.outputs[0], store_named_attribute_004.inputs[0])
    links.new(group_input.outputs[7], store_named_attribute_004.inputs[3])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.label = ""
    math_007.location = (455.4095458984375, 248.90057373046875)
    math_007.bl_label = "Math"
    math_007.operation = "ADD"
    math_007.use_clamp = False
    # Value
    math_007.inputs[1].default_value = 3.1415927410125732
    # Value
    math_007.inputs[2].default_value = 0.5
    # Links for math_007
    links.new(math_006.outputs[0], math_007.inputs[0])

    math_008 = nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.label = ""
    math_008.location = (678.4512329101562, 212.67776489257812)
    math_008.bl_label = "Math"
    math_008.operation = "FLOORED_MODULO"
    math_008.use_clamp = False
    # Value
    math_008.inputs[1].default_value = 6.2831854820251465
    # Value
    math_008.inputs[2].default_value = 0.5
    # Links for math_008
    links.new(math_007.outputs[0], math_008.inputs[0])

    math_009 = nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.label = ""
    math_009.location = (880.3944091796875, 202.11270141601562)
    math_009.bl_label = "Math"
    math_009.operation = "SUBTRACT"
    math_009.use_clamp = False
    # Value
    math_009.inputs[1].default_value = 3.1415927410125732
    # Value
    math_009.inputs[2].default_value = 0.5
    # Links for math_009
    links.new(math_008.outputs[0], math_009.inputs[0])

    math_010 = nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.label = ""
    math_010.location = (-966.7532958984375, 818.9998168945312)
    math_010.bl_label = "Math"
    math_010.operation = "SINE"
    math_010.use_clamp = False
    # Value
    math_010.inputs[1].default_value = 0.5
    # Value
    math_010.inputs[2].default_value = 0.5
    # Links for math_010
    links.new(sample_index.outputs[0], math_010.inputs[0])

    math_011 = nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.label = ""
    math_011.location = (-972.7816772460938, 628.8234252929688)
    math_011.bl_label = "Math"
    math_011.operation = "COSINE"
    math_011.use_clamp = False
    # Value
    math_011.inputs[1].default_value = 0.5
    # Value
    math_011.inputs[2].default_value = 0.5
    # Links for math_011
    links.new(sample_index.outputs[0], math_011.inputs[0])

    math_012 = nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.label = ""
    math_012.location = (-993.8812255859375, 399.1414794921875)
    math_012.bl_label = "Math"
    math_012.operation = "SINE"
    math_012.use_clamp = False
    # Value
    math_012.inputs[1].default_value = 0.5
    # Value
    math_012.inputs[2].default_value = 0.5
    # Links for math_012
    links.new(sample_index_001.outputs[0], math_012.inputs[0])

    math_013 = nodes.new("ShaderNodeMath")
    math_013.name = "Math.013"
    math_013.label = ""
    math_013.location = (-992.3790893554688, 254.84425354003906)
    math_013.bl_label = "Math"
    math_013.operation = "COSINE"
    math_013.use_clamp = False
    # Value
    math_013.inputs[1].default_value = 0.5
    # Value
    math_013.inputs[2].default_value = 0.5
    # Links for math_013
    links.new(sample_index_001.outputs[0], math_013.inputs[0])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (-602.0673828125, 716.2296752929688)
    mix.bl_label = "Mix"
    mix.data_type = "FLOAT"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    # Factor
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix
    links.new(math_010.outputs[0], mix.inputs[2])
    links.new(math_012.outputs[0], mix.inputs[3])
    links.new(group_input.outputs[0], mix.inputs[0])

    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.label = ""
    mix_001.location = (-608.0957641601562, 408.32476806640625)
    mix_001.bl_label = "Mix"
    mix_001.data_type = "FLOAT"
    mix_001.factor_mode = "UNIFORM"
    mix_001.blend_type = "MIX"
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    # Factor
    mix_001.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_001.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_001.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_001.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_001.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_001
    links.new(math_011.outputs[0], mix_001.inputs[2])
    links.new(math_013.outputs[0], mix_001.inputs[3])
    links.new(group_input.outputs[0], mix_001.inputs[0])

    math_014 = nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.label = ""
    math_014.location = (-305.0365295410156, 511.1552734375)
    math_014.bl_label = "Math"
    math_014.operation = "ARCTAN2"
    math_014.use_clamp = False
    # Value
    math_014.inputs[2].default_value = 0.5
    # Links for math_014
    links.new(mix_001.outputs[0], math_014.inputs[1])
    links.new(mix.outputs[0], math_014.inputs[0])
    links.new(math_014.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
@geo_node_group
def create_mix_angle_group():
    group_name = "MixAngleGrouped2"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Result", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    
    socket = group.interface.new_socket(name="CurveA", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    
    socket = group.interface.new_socket(name="Factor", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.5
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    
    socket = group.interface.new_socket(name="CurveA", in_out="INPUT", socket_type="NodeSocketGeometry")
    
    socket = group.interface.new_socket(name="AngleA", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    
    socket = group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0 # Not used for logic, but kept for interface compatibility
    
    socket = group.interface.new_socket(name="CurveB", in_out="INPUT", socket_type="NodeSocketGeometry")
    
    socket = group.interface.new_socket(name="AngleB", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    
    socket = group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    
    socket = group.interface.new_socket(name="Switch", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    
    # Define Inputs
    group_input = nodes.new("NodeGroupInput")
    group_input.location = (-1400, 0)
    
    # Input Indices:
    # 0: Factor
    # 1: CurveA
    # 2: AngleA
    # 3: IndexA
    # 4: CurveB
    # 5: AngleB
    # 6: IndexB
    # 7: Switch

    group_output = nodes.new("NodeGroupOutput")
    group_output.location = (1200, 0)

    # --- 1. Get Reference Angles at Index 0 (The "Leader") ---
    
    # Constant Integer 0 for sampling the anchor
    int_zero = nodes.new("FunctionNodeInputInt")
    int_zero.integer = 0
    int_zero.location = (-1200, 300)

    # Sample AngleA at Index 0
    sample_a0 = nodes.new("GeometryNodeSampleIndex")
    sample_a0.label = "Sample AngleA[0]"
    sample_a0.data_type = "FLOAT"
    sample_a0.location = (-1000, 200)
    links.new(group_input.outputs[1], sample_a0.inputs[0]) # CurveA Geometry
    links.new(int_zero.outputs[0], sample_a0.inputs[1])    # Index (0)
    links.new(group_input.outputs[2], sample_a0.inputs[2]) # AngleA Value

    # Sample AngleB at Index 0
    sample_b0 = nodes.new("GeometryNodeSampleIndex")
    sample_b0.label = "Sample AngleB[0]"
    sample_b0.data_type = "FLOAT"
    sample_b0.location = (-1000, 0)
    links.new(group_input.outputs[4], sample_b0.inputs[0]) # CurveB Geometry
    links.new(int_zero.outputs[0], sample_b0.inputs[1])    # Index (0)
    links.new(group_input.outputs[5], sample_b0.inputs[2]) # AngleB Value

    # --- 2. Calculate Reference Delta (The "Global Direction") ---
    # Logic: Shortest path from A0 to B0.
    # RefDelta = ((B0 - A0 + pi) % 2pi) - pi
    
    # B0 - A0
    sub_ref = nodes.new("ShaderNodeMath")
    sub_ref.operation = "SUBTRACT"
    sub_ref.location = (-800, 100)
    links.new(sample_b0.outputs[0], sub_ref.inputs[0])
    links.new(sample_a0.outputs[0], sub_ref.inputs[1])

    # + Pi
    add_pi_ref = nodes.new("ShaderNodeMath")
    add_pi_ref.operation = "ADD"
    add_pi_ref.location = (-600, 100)
    add_pi_ref.inputs[1].default_value = math.pi
    links.new(sub_ref.outputs[0], add_pi_ref.inputs[0])

    # % 2Pi
    mod_ref = nodes.new("ShaderNodeMath")
    mod_ref.operation = "FLOORED_MODULO"
    mod_ref.location = (-400, 100)
    mod_ref.inputs[1].default_value = math.pi * 2
    links.new(add_pi_ref.outputs[0], mod_ref.inputs[0])

    # - Pi
    ref_delta = nodes.new("ShaderNodeMath")
    ref_delta.label = "Ref Delta"
    ref_delta.operation = "SUBTRACT"
    ref_delta.location = (-200, 100)
    ref_delta.inputs[1].default_value = math.pi
    links.new(mod_ref.outputs[0], ref_delta.inputs[0])

    # --- 3. Calculate Raw Delta for every point ---
    # Logic: RawDelta = AngleB - AngleA
    
    sub_raw = nodes.new("ShaderNodeMath")
    sub_raw.label = "Raw Delta"
    sub_raw.operation = "SUBTRACT"
    sub_raw.location = (-800, -200)
    links.new(group_input.outputs[5], sub_raw.inputs[0]) # AngleB
    links.new(group_input.outputs[2], sub_raw.inputs[1]) # AngleA

    # --- 4. Align Local Delta to Reference Delta ---
    # We want RawDelta to be within +-pi of RefDelta.
    # Formula: FinalDelta = RefDelta + ((RawDelta - RefDelta + pi) % 2pi - pi)
    
    # RawDelta - RefDelta
    diff_from_ref = nodes.new("ShaderNodeMath")
    diff_from_ref.operation = "SUBTRACT"
    diff_from_ref.location = (-200, -100)
    links.new(sub_raw.outputs[0], diff_from_ref.inputs[0])
    links.new(ref_delta.outputs[0], diff_from_ref.inputs[1])

    # Wrap the difference to [-pi, pi]
    # (x + pi)
    add_pi_local = nodes.new("ShaderNodeMath")
    add_pi_local.operation = "ADD"
    add_pi_local.location = (0, -100)
    add_pi_local.inputs[1].default_value = math.pi
    links.new(diff_from_ref.outputs[0], add_pi_local.inputs[0])

    # % 2pi
    mod_local = nodes.new("ShaderNodeMath")
    mod_local.operation = "FLOORED_MODULO"
    mod_local.location = (200, -100)
    mod_local.inputs[1].default_value = math.pi * 2
    links.new(add_pi_local.outputs[0], mod_local.inputs[0])

    # - pi
    wrap_local = nodes.new("ShaderNodeMath")
    wrap_local.operation = "SUBTRACT"
    wrap_local.location = (400, -100)
    wrap_local.inputs[1].default_value = math.pi
    links.new(mod_local.outputs[0], wrap_local.inputs[0])

    # Reconstruct the aligned delta: RefDelta + WrappedDiff
    final_delta = nodes.new("ShaderNodeMath")
    final_delta.label = "Aligned Delta"
    final_delta.operation = "ADD"
    final_delta.location = (600, 0)
    links.new(ref_delta.outputs[0], final_delta.inputs[0])
    links.new(wrap_local.outputs[0], final_delta.inputs[1])

    # --- 5. Apply Factor and Output ---
    # Result = AngleA + (AlignedDelta * Factor)
    
    # AlignedDelta * Factor
    scale_delta = nodes.new("ShaderNodeMath")
    scale_delta.operation = "MULTIPLY"
    scale_delta.location = (800, 0)
    links.new(final_delta.outputs[0], scale_delta.inputs[0])
    links.new(group_input.outputs[0], scale_delta.inputs[1]) # Factor

    # AngleA + ScaledDelta
    final_add = nodes.new("ShaderNodeMath")
    final_add.operation = "ADD"
    final_add.location = (1000, 0)
    links.new(group_input.outputs[2], final_add.inputs[0]) # AngleA
    links.new(scale_delta.outputs[0], final_add.inputs[1])

    # Outputs
    links.new(final_add.outputs[0], group_output.inputs[0]) # Result
    links.new(group_input.outputs[1], group_output.inputs[1]) # CurveA Pass-through

    auto_layout_nodes(group)
    return group