import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_debug_handles_group():
    group_name = "DebugHandles"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 1
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Value", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1022.678466796875, -87.68763732910156)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-759.2931518554688, 15.13492202758789)
    group_input.bl_label = "Group Input"
    # Links for group_input

    mesh_line = nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.label = ""
    mesh_line.location = (212.28326416015625, -135.93734741210938)
    mesh_line.bl_label = "Mesh Line"
    mesh_line.mode = "END_POINTS"
    mesh_line.count_mode = "TOTAL"
    # Count
    mesh_line.inputs[0].default_value = 10
    # Resolution
    mesh_line.inputs[1].default_value = 1.0
    # Links for mesh_line

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.name = "Sample Index.005"
    sample_index_005.label = ""
    sample_index_005.location = (-166.04278564453125, 112.57162475585938)
    sample_index_005.bl_label = "Sample Index"
    sample_index_005.data_type = "FLOAT_VECTOR"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    # Links for sample_index_005
    links.new(sample_index_005.outputs[0], mesh_line.inputs[2])
    links.new(group_input.outputs[0], sample_index_005.inputs[0])
    links.new(group_input.outputs[1], sample_index_005.inputs[2])

    sample_index_006 = nodes.new("GeometryNodeSampleIndex")
    sample_index_006.name = "Sample Index.006"
    sample_index_006.label = ""
    sample_index_006.location = (15.213069915771484, 198.64065551757812)
    sample_index_006.bl_label = "Sample Index"
    sample_index_006.data_type = "FLOAT_VECTOR"
    sample_index_006.domain = "POINT"
    sample_index_006.clamp = False
    # Links for sample_index_006
    links.new(sample_index_006.outputs[0], mesh_line.inputs[3])
    links.new(group_input.outputs[0], sample_index_006.inputs[0])
    links.new(group_input.outputs[1], sample_index_006.inputs[2])

    curve_handle_positions = nodes.new("GeometryNodeInputCurveHandlePositions")
    curve_handle_positions.name = "Curve Handle Positions"
    curve_handle_positions.label = ""
    curve_handle_positions.location = (-559.2931518554688, 281.7010803222656)
    curve_handle_positions.bl_label = "Curve Handle Positions"
    # Relative
    curve_handle_positions.inputs[0].default_value = True
    # Links for curve_handle_positions
    links.new(curve_handle_positions.outputs[1], sample_index_006.inputs[1])
    links.new(curve_handle_positions.outputs[0], sample_index_005.inputs[1])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (392.31256103515625, -342.2837829589844)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Position
    set_position_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_002
    links.new(mesh_line.outputs[0], set_position_002.inputs[0])

    sample_index_011 = nodes.new("GeometryNodeSampleIndex")
    sample_index_011.name = "Sample Index.011"
    sample_index_011.label = ""
    sample_index_011.location = (336.81134033203125, 127.37490844726562)
    sample_index_011.bl_label = "Sample Index"
    sample_index_011.data_type = "FLOAT_VECTOR"
    sample_index_011.domain = "POINT"
    sample_index_011.clamp = False
    # Links for sample_index_011
    links.new(sample_index_011.outputs[0], set_position_002.inputs[3])
    links.new(group_input.outputs[0], sample_index_011.inputs[0])
    links.new(group_input.outputs[1], sample_index_011.inputs[2])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (144.09576416015625, 372.5536193847656)
    position_002.bl_label = "Position"
    # Links for position_002
    links.new(position_002.outputs[0], sample_index_011.inputs[1])

    mesh_line_001 = nodes.new("GeometryNodeMeshLine")
    mesh_line_001.name = "Mesh Line.001"
    mesh_line_001.label = ""
    mesh_line_001.location = (639.0037231445312, -0.6247215270996094)
    mesh_line_001.bl_label = "Mesh Line"
    mesh_line_001.mode = "OFFSET"
    mesh_line_001.count_mode = "TOTAL"
    # Count
    mesh_line_001.inputs[0].default_value = 2
    # Resolution
    mesh_line_001.inputs[1].default_value = 1.0
    # Offset
    mesh_line_001.inputs[3].default_value = Vector((0.0, 0.0, 1.0))
    # Links for mesh_line_001

    sample_index_012 = nodes.new("GeometryNodeSampleIndex")
    sample_index_012.name = "Sample Index.012"
    sample_index_012.label = ""
    sample_index_012.location = (454.96881103515625, -97.14944458007812)
    sample_index_012.bl_label = "Sample Index"
    sample_index_012.data_type = "FLOAT_VECTOR"
    sample_index_012.domain = "POINT"
    sample_index_012.clamp = False
    # Links for sample_index_012
    links.new(sample_index_012.outputs[0], mesh_line_001.inputs[2])
    links.new(group_input.outputs[0], sample_index_012.inputs[0])
    links.new(group_input.outputs[1], sample_index_012.inputs[2])
    links.new(group_input.outputs[2], sample_index_012.inputs[1])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (827.9381103515625, -77.44023132324219)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(mesh_line_001.outputs[0], join_geometry.inputs[0])
    links.new(set_position_002.outputs[0], join_geometry.inputs[0])
    links.new(join_geometry.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_align_handles_group():
    group_name = "AlignHandles"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1683.2965087890625, 8.261022567749023)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1744.117919921875, -11.170132637023926)
    group_input.bl_label = "Group Input"
    # Links for group_input

    separate_components_001 = nodes.new("GeometryNodeSeparateComponents")
    separate_components_001.name = "Separate Components.001"
    separate_components_001.label = ""
    separate_components_001.location = (-1462.194091796875, 152.17526245117188)
    separate_components_001.bl_label = "Separate Components"
    # Links for separate_components_001
    links.new(group_input.outputs[0], separate_components_001.inputs[0])

    separate_components_002 = nodes.new("GeometryNodeSeparateComponents")
    separate_components_002.name = "Separate Components.002"
    separate_components_002.label = ""
    separate_components_002.location = (-1458.0140380859375, -72.51876831054688)
    separate_components_002.bl_label = "Separate Components"
    # Links for separate_components_002
    links.new(group_input.outputs[1], separate_components_002.inputs[0])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (1491.3441162109375, -9.0211181640625)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(join_geometry.outputs[0], group_output.inputs[0])
    links.new(separate_components_002.outputs[0], join_geometry.inputs[0])
    links.new(separate_components_001.outputs[0], join_geometry.inputs[0])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (-494.2066650390625, -378.6239318847656)
    index.bl_label = "Index"
    # Links for index

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (175.2965087890625, 258.2102966308594)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Links for sample_index
    links.new(separate_components_001.outputs[1], sample_index.inputs[0])
    links.new(index.outputs[0], sample_index.inputs[2])

    curve_handle_positions = nodes.new("GeometryNodeInputCurveHandlePositions")
    curve_handle_positions.name = "Curve Handle Positions"
    curve_handle_positions.label = ""
    curve_handle_positions.location = (-211.00820922851562, 347.25439453125)
    curve_handle_positions.bl_label = "Curve Handle Positions"
    # Relative
    curve_handle_positions.inputs[0].default_value = False
    # Links for curve_handle_positions
    links.new(curve_handle_positions.outputs[0], sample_index.inputs[1])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.label = ""
    sample_index_002.location = (176.241455078125, 546.1041259765625)
    sample_index_002.bl_label = "Sample Index"
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    # Links for sample_index_002
    links.new(separate_components_001.outputs[1], sample_index_002.inputs[0])
    links.new(index.outputs[0], sample_index_002.inputs[2])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (-228.091064453125, 457.77337646484375)
    position.bl_label = "Position"
    # Links for position
    links.new(position.outputs[0], sample_index_002.inputs[1])

    set_handle_positions = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions.name = "Set Handle Positions"
    set_handle_positions.label = ""
    set_handle_positions.location = (1308.53173828125, 466.7369384765625)
    set_handle_positions.bl_label = "Set Handle Positions"
    set_handle_positions.mode = "LEFT"
    # Offset
    set_handle_positions.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_handle_positions
    links.new(separate_components_001.outputs[1], set_handle_positions.inputs[0])
    links.new(set_handle_positions.outputs[0], join_geometry.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (977.3076782226562, 237.22573852539062)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "VECTOR"
    compare.mode = "ELEMENT"
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
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513
    # Links for compare
    links.new(sample_index_002.outputs[0], compare.inputs[5])
    links.new(compare.outputs[0], set_handle_positions.inputs[1])

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.name = "Sample Index.003"
    sample_index_003.label = ""
    sample_index_003.location = (199.87777709960938, -309.401123046875)
    sample_index_003.bl_label = "Sample Index"
    sample_index_003.data_type = "FLOAT_VECTOR"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    # Links for sample_index_003
    links.new(position.outputs[0], sample_index_003.inputs[1])
    links.new(separate_components_002.outputs[1], sample_index_003.inputs[0])
    links.new(sample_index_003.outputs[0], compare.inputs[4])

    debug_handles = nodes.new("GeometryNodeGroup")
    debug_handles.name = "Group.001"
    debug_handles.label = ""
    debug_handles.location = (1514.2930908203125, 313.65655517578125)
    debug_handles.node_tree = create_debug_handles_group()
    debug_handles.bl_label = "Group"
    # Index
    debug_handles.inputs[1].default_value = 14
    # Value
    debug_handles.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for debug_handles
    links.new(set_handle_positions.outputs[0], debug_handles.inputs[0])
    links.new(debug_handles.outputs[0], join_geometry.inputs[0])

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.name = "Sample Index.005"
    sample_index_005.label = ""
    sample_index_005.location = (186.2352294921875, -568.8812866210938)
    sample_index_005.bl_label = "Sample Index"
    sample_index_005.data_type = "FLOAT_VECTOR"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    # Links for sample_index_005
    links.new(curve_handle_positions.outputs[1], sample_index_005.inputs[1])
    links.new(separate_components_002.outputs[1], sample_index_005.inputs[0])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (879.8364868164062, 674.670166015625)
    mix.bl_label = "Mix"
    mix.data_type = "VECTOR"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    # Factor
    mix.inputs[0].default_value = 0.5
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
    links.new(sample_index.outputs[0], mix.inputs[4])
    links.new(mix.outputs[1], set_handle_positions.inputs[2])
    links.new(sample_index_005.outputs[0], mix.inputs[5])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (-811.7499389648438, 575.3111572265625)
    position_001.bl_label = "Position"
    # Links for position_001

    sample_index_006 = nodes.new("GeometryNodeSampleIndex")
    sample_index_006.name = "Sample Index.006"
    sample_index_006.label = ""
    sample_index_006.location = (-514.5317993164062, 743.6423950195312)
    sample_index_006.bl_label = "Sample Index"
    sample_index_006.data_type = "FLOAT_VECTOR"
    sample_index_006.domain = "POINT"
    sample_index_006.clamp = False
    # Index
    sample_index_006.inputs[2].default_value = 0
    # Links for sample_index_006
    links.new(position_001.outputs[0], sample_index_006.inputs[1])
    links.new(separate_components_001.outputs[1], sample_index_006.inputs[0])

    sample_index_007 = nodes.new("GeometryNodeSampleIndex")
    sample_index_007.name = "Sample Index.007"
    sample_index_007.label = ""
    sample_index_007.location = (-517.8861694335938, 1004.9937744140625)
    sample_index_007.bl_label = "Sample Index"
    sample_index_007.data_type = "FLOAT_VECTOR"
    sample_index_007.domain = "POINT"
    sample_index_007.clamp = False
    # Index
    sample_index_007.inputs[2].default_value = 0
    # Links for sample_index_007
    links.new(position_001.outputs[0], sample_index_007.inputs[1])
    links.new(separate_components_002.outputs[1], sample_index_007.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (-248.7480926513672, 948.2908935546875)
    compare_001.bl_label = "Compare"
    compare_001.operation = "EQUAL"
    compare_001.data_type = "VECTOR"
    compare_001.mode = "ELEMENT"
    # A
    compare_001.inputs[0].default_value = 0.0
    # B
    compare_001.inputs[1].default_value = 0.0
    # A
    compare_001.inputs[2].default_value = 0
    # B
    compare_001.inputs[3].default_value = 0
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
    links.new(sample_index_006.outputs[0], compare_001.inputs[4])
    links.new(sample_index_007.outputs[0], compare_001.inputs[5])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (-33.31646728515625, -649.8456420898438)
    switch.bl_label = "Switch"
    switch.input_type = "INT"
    # Links for switch
    links.new(index.outputs[0], switch.inputs[2])
    links.new(switch.outputs[0], sample_index_005.inputs[2])
    links.new(switch.outputs[0], sample_index_003.inputs[2])
    links.new(compare_001.outputs[0], switch.inputs[0])

    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.label = ""
    index_001.location = (-531.1052856445312, -608.6661376953125)
    index_001.bl_label = "Index"
    # Links for index_001

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (-777.4346923828125, -485.34515380859375)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "CURVE"
    # Links for domain_size
    links.new(separate_components_002.outputs[1], domain_size.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-611.4735717773438, -466.7501525878906)
    math.bl_label = "Math"
    math.operation = "SUBTRACT"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 1.0
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(domain_size.outputs[0], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-314.92510986328125, -627.7711181640625)
    math_001.bl_label = "Math"
    math_001.operation = "SUBTRACT"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math.outputs[0], math_001.inputs[0])
    links.new(index.outputs[0], math_001.inputs[1])
    links.new(math_001.outputs[0], switch.inputs[1])

    auto_layout_nodes(group)
    return group