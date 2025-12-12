import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes

def create_nodegroup_group():
    group_name = "NodeGroup"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Result", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Factor", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.5
    socket.min_value = 0.0
    socket.max_value = 1.0
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Value", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Value", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (265.5225830078125, 6.492884159088135)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-588.9310913085938, 4.869663238525391)
    group_input.bl_label = "Group Input"
    # Links for group_input

    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.name = "Mix.003"
    mix_003.label = ""
    mix_003.location = (75.52255249023438, 30.14333724975586)
    mix_003.bl_label = "Mix"
    mix_003.data_type = "FLOAT"
    mix_003.factor_mode = "UNIFORM"
    mix_003.blend_type = "MIX"
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    # Factor
    mix_003.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_003.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_003.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_003.inputs[8].default_value = <Euler (x=0.0000, y=0.0000, z=0.0000), order='XYZ'>
    # B
    mix_003.inputs[9].default_value = <Euler (x=0.0000, y=0.0000, z=0.0000), order='XYZ'>
    # Links for mix_003
    links.new(group_input.outputs[0], mix_003.inputs[0])
    links.new(mix_003.outputs[0], group_output.inputs[0])

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.name = "Sample Index.005"
    sample_index_005.label = ""
    sample_index_005.location = (50.895599365234375, 237.23135375976562)
    sample_index_005.bl_label = "Sample Index"
    sample_index_005.data_type = "FLOAT"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    # Links for sample_index_005
    links.new(group_input.outputs[1], sample_index_005.inputs[0])
    links.new(group_input.outputs[2], sample_index_005.inputs[1])
    links.new(sample_index_005.outputs[0], mix_003.inputs[2])

    sample_index_006 = nodes.new("GeometryNodeSampleIndex")
    sample_index_006.name = "Sample Index.006"
    sample_index_006.label = ""
    sample_index_006.location = (-249.58685302734375, -83.22563934326172)
    sample_index_006.bl_label = "Sample Index"
    sample_index_006.data_type = "FLOAT"
    sample_index_006.domain = "POINT"
    sample_index_006.clamp = False
    # Links for sample_index_006
    links.new(group_input.outputs[6], sample_index_006.inputs[2])
    links.new(group_input.outputs[4], sample_index_006.inputs[0])
    links.new(group_input.outputs[5], sample_index_006.inputs[1])
    links.new(sample_index_006.outputs[0], mix_003.inputs[3])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-336.81927490234375, 20.383298873901367)
    math.bl_label = "Math"
    math.operation = "ADD"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 40.10000228881836
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(group_input.outputs[3], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-139.95248413085938, 123.16204833984375)
    math_001.bl_label = "Math"
    math_001.operation = "FLOORED_MODULO"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math.outputs[0], math_001.inputs[0])
    links.new(math_001.outputs[0], sample_index_005.inputs[2])

    mix_offset_index = nodes.new("GeometryNodeAttributeDomainSize")
    mix_offset_index.name = "MixOffsetIndex"
    mix_offset_index.label = ""
    mix_offset_index.location = (-359.97015380859375, 160.91741943359375)
    mix_offset_index.bl_label = "Domain Size"
    mix_offset_index.component = "POINTCLOUD"
    # Links for mix_offset_index
    links.new(mix_offset_index.outputs[0], math_001.inputs[1])
    links.new(group_input.outputs[1], mix_offset_index.inputs[0])

    auto_layout_nodes(group)
    return group