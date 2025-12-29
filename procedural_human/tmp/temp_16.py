import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_construct_vector_group():
    group_name = "ConstructVector"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Vector", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Normal", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Inclination", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.5
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Azimuth", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.5
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="u", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="v", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="length", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 1.0
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Factor", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.5
    socket.min_value = 0.0
    socket.max_value = 1.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (649.7435913085938, -8.821724891662598)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1256.1810302734375, -61.06705093383789)
    group_input.bl_label = "Group Input"
    # Links for group_input

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-645.156005859375, 153.03457641601562)
    math.bl_label = "Math"
    math.operation = "COSINE"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.5
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(group_input.outputs[2], math.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (-348.3465576171875, 249.7794952392578)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(math.outputs[0], math_002.inputs[1])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (-181.99456787109375, 174.4263153076172)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "SCALE"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_001
    links.new(math_002.outputs[0], vector_math_001.inputs[3])
    links.new(group_input.outputs[3], vector_math_001.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (14.837173461914062, 109.81389617919922)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "ADD"
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(vector_math_001.outputs[0], vector_math_002.inputs[0])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (-607.515869140625, 392.5959777832031)
    math_004.bl_label = "Math"
    math_004.operation = "SINE"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 0.5
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(group_input.outputs[1], math_004.inputs[0])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (-615.67919921875, -181.97836303710938)
    math_006.bl_label = "Math"
    math_006.operation = "SINE"
    math_006.use_clamp = False
    # Value
    math_006.inputs[1].default_value = 0.5
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(group_input.outputs[2], math_006.inputs[0])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.label = ""
    math_007.location = (-372.5569152832031, -56.62147903442383)
    math_007.bl_label = "Math"
    math_007.operation = "MULTIPLY"
    math_007.use_clamp = False
    # Value
    math_007.inputs[2].default_value = 0.5
    # Links for math_007
    links.new(math_006.outputs[0], math_007.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (-198.8205108642578, -47.08412551879883)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "SCALE"
    # Vector
    vector_math_003.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_003
    links.new(math_007.outputs[0], vector_math_003.inputs[3])
    links.new(vector_math_003.outputs[0], vector_math_002.inputs[1])
    links.new(group_input.outputs[4], vector_math_003.inputs[0])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (231.5659942626953, 44.80907440185547)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "ADD"
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(vector_math_002.outputs[0], vector_math_004.inputs[0])

    math_008 = nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.label = ""
    math_008.location = (-608.7670288085938, 664.8692626953125)
    math_008.bl_label = "Math"
    math_008.operation = "COSINE"
    math_008.use_clamp = False
    # Value
    math_008.inputs[1].default_value = 0.5
    # Value
    math_008.inputs[2].default_value = 0.5
    # Links for math_008
    links.new(group_input.outputs[1], math_008.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (-321.3338317871094, -336.8251953125)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "SCALE"
    # Vector
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_005
    links.new(vector_math_005.outputs[0], vector_math_004.inputs[1])
    links.new(group_input.outputs[0], vector_math_005.inputs[0])

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (459.74359130859375, 73.97240447998047)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "SCALE"
    # Vector
    vector_math_006.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_006
    links.new(vector_math_004.outputs[0], vector_math_006.inputs[0])
    links.new(group_input.outputs[5], vector_math_006.inputs[3])
    links.new(vector_math_006.outputs[0], group_output.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (-917.6014404296875, -488.59307861328125)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "FLOAT"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "length"
    # Links for store_named_attribute
    links.new(group_input.outputs[5], store_named_attribute.inputs[3])
    links.new(group_input.outputs[6], store_named_attribute.inputs[0])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (-653.3214111328125, -547.9818725585938)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "FLOAT"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "azimuth"
    # Links for store_named_attribute_001
    links.new(group_input.outputs[2], store_named_attribute_001.inputs[3])
    links.new(store_named_attribute.outputs[0], store_named_attribute_001.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (-300.0876770019531, -509.24896240234375)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "FLOAT"
    store_named_attribute_002.domain = "POINT"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "inclination"
    # Links for store_named_attribute_002
    links.new(store_named_attribute_002.outputs[0], group_output.inputs[1])
    links.new(store_named_attribute_001.outputs[0], store_named_attribute_002.inputs[0])
    links.new(group_input.outputs[1], store_named_attribute_002.inputs[3])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (-600.677490234375, 804.3973388671875)
    math_003.bl_label = "Math"
    math_003.operation = "COSH"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 0.5
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (-604.7570190429688, 522.3834228515625)
    math_005.bl_label = "Math"
    math_005.operation = "SINH"
    math_005.use_clamp = False
    # Value
    math_005.inputs[1].default_value = 0.5
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (-1030.930908203125, 599.92041015625)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    # From Min
    map_range.inputs[1].default_value = -1.0
    # From Max
    map_range.inputs[2].default_value = 1.0
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
    links.new(group_input.outputs[7], map_range.inputs[0])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (-393.9388427734375, 769.8325805664062)
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
    links.new(mix.outputs[0], vector_math_005.inputs[3])
    links.new(map_range.outputs[0], mix.inputs[0])
    links.new(math_008.outputs[0], mix.inputs[3])
    links.new(math_003.outputs[0], mix.inputs[2])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-781.0, 725.5538940429688)
    math_001.bl_label = "Math"
    math_001.operation = "SUBTRACT"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 1.5707963705062866
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math_001.outputs[0], math_003.inputs[0])
    links.new(group_input.outputs[1], math_001.inputs[0])
    links.new(math_001.outputs[0], math_005.inputs[0])

    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.label = ""
    mix_001.location = (-425.28973388671875, 545.6399536132812)
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
    links.new(mix_001.outputs[0], math_002.inputs[0])
    links.new(mix_001.outputs[0], math_007.inputs[1])
    links.new(map_range.outputs[0], mix_001.inputs[0])
    links.new(math_005.outputs[0], mix_001.inputs[2])
    links.new(math_004.outputs[0], mix_001.inputs[3])

    auto_layout_nodes(group)
    return group