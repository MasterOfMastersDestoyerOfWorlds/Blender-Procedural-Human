import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_get_curvature_group():
    group_name = "GetCurvature"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Value", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
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
    group_output.location = (428.2508850097656, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-438.2508850097656, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (5.087127685546875, -184.75274658203125)
    math_001.bl_label = "Math"
    math_001.operation = "COSINE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 0.5
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (30.887298583984375, -10.357521057128906)
    math_002.bl_label = "Math"
    math_002.operation = "COSINE"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 0.5
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (238.25088500976562, -64.94317626953125)
    math_003.bl_label = "Math"
    math_003.operation = "MULTIPLY"
    math_003.use_clamp = False
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_001.outputs[0], math_003.inputs[1])
    links.new(math_002.outputs[0], math_003.inputs[0])
    links.new(math_003.outputs[0], group_output.inputs[0])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (-238.25088500976562, 184.75274658203125)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Links for sample_index
    links.new(sample_index.outputs[0], math_002.inputs[0])
    links.new(group_input.outputs[2], sample_index.inputs[2])
    links.new(group_input.outputs[1], sample_index.inputs[1])
    links.new(group_input.outputs[0], sample_index.inputs[0])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (-192.19253540039062, -49.258819580078125)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001
    links.new(sample_index_001.outputs[0], math_001.inputs[0])
    links.new(group_input.outputs[3], sample_index_001.inputs[0])
    links.new(group_input.outputs[4], sample_index_001.inputs[1])
    links.new(group_input.outputs[5], sample_index_001.inputs[2])

    auto_layout_nodes(group)
    return group