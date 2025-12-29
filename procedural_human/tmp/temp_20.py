import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_angle_between_vectors_group():
    group_name = "AngleBetweenVectors"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Value", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Vector", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Vector", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (478.046630859375, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-488.046630859375, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (-200.63522338867188, 143.54544067382812)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "DOT_PRODUCT"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(group_input.outputs[0], vector_math_001.inputs[0])
    links.new(group_input.outputs[1], vector_math_001.inputs[1])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (288.046630859375, -39.432464599609375)
    math.bl_label = "Math"
    math.operation = "ARCCOSINE"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.5
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(math.outputs[0], group_output.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (102.18690490722656, 20.129806518554688)
    math_001.bl_label = "Math"
    math_001.operation = "DIVIDE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(vector_math_001.outputs[1], math_001.inputs[0])
    links.new(math_001.outputs[0], math.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (-288.046630859375, -143.54544067382812)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "LENGTH"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(group_input.outputs[0], vector_math_002.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (-101.26889038085938, -65.54901123046875)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(vector_math_002.outputs[1], math_002.inputs[0])
    links.new(math_002.outputs[0], math_001.inputs[1])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (-284.23486328125, -27.069671630859375)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "LENGTH"
    # Vector
    vector_math_003.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(vector_math_003.outputs[1], math_002.inputs[1])
    links.new(group_input.outputs[1], vector_math_003.inputs[0])

    auto_layout_nodes(group)
    return group

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
    group_input.location = (-368.0382080078125, -17.875732421875)
    group_input.bl_label = "Group Input"
    # Links for group_input

    separate_components_001 = nodes.new("GeometryNodeSeparateComponents")
    separate_components_001.name = "Separate Components.001"
    separate_components_001.label = ""
    separate_components_001.location = (-86.11442565917969, 145.46966552734375)
    separate_components_001.bl_label = "Separate Components"
    # Links for separate_components_001
    links.new(group_input.outputs[0], separate_components_001.inputs[0])

    separate_components_002 = nodes.new("GeometryNodeSeparateComponents")
    separate_components_002.name = "Separate Components.002"
    separate_components_002.label = ""
    separate_components_002.location = (-81.93426513671875, -79.224365234375)
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
    links.new(separate_components_001.outputs[0], join_geometry.inputs[0])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (135.58949279785156, 84.00625610351562)
    index.bl_label = "Index"
    # Links for index

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (408.59051513671875, 280.3372802734375)
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
    curve_handle_positions.location = (128.78846740722656, 284.07177734375)
    curve_handle_positions.bl_label = "Curve Handle Positions"
    # Relative
    curve_handle_positions.inputs[0].default_value = False
    # Links for curve_handle_positions
    links.new(curve_handle_positions.outputs[0], sample_index.inputs[1])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (458.13885498046875, -110.66964721679688)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001
    links.new(index.outputs[0], sample_index_001.inputs[2])
    links.new(separate_components_002.outputs[1], sample_index_001.inputs[0])
    links.new(curve_handle_positions.outputs[0], sample_index_001.inputs[1])

    angle_between_vectors = nodes.new("GeometryNodeGroup")
    angle_between_vectors.name = "AngleBetweenVectors"
    angle_between_vectors.label = ""
    angle_between_vectors.location = (673.341064453125, 249.59117126464844)
    angle_between_vectors.node_tree = create_angle_between_vectors_group()
    angle_between_vectors.bl_label = "Group"
    # Links for angle_between_vectors
    links.new(sample_index.outputs[0], angle_between_vectors.inputs[0])
    links.new(sample_index_001.outputs[0], angle_between_vectors.inputs[1])

    vector_rotate = nodes.new("ShaderNodeVectorRotate")
    vector_rotate.name = "Vector Rotate"
    vector_rotate.label = ""
    vector_rotate.location = (1047.3057861328125, 347.06927490234375)
    vector_rotate.bl_label = "Vector Rotate"
    vector_rotate.rotation_type = "AXIS_ANGLE"
    vector_rotate.invert = False
    # Rotation
    vector_rotate.inputs[4].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for vector_rotate
    links.new(sample_index.outputs[0], vector_rotate.inputs[0])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.label = ""
    sample_index_002.location = (415.76385498046875, 536.0023193359375)
    sample_index_002.bl_label = "Sample Index"
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    # Links for sample_index_002
    links.new(separate_components_001.outputs[1], sample_index_002.inputs[0])
    links.new(index.outputs[0], sample_index_002.inputs[2])
    links.new(sample_index_002.outputs[0], vector_rotate.inputs[1])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (129.16574096679688, 433.15863037109375)
    position.bl_label = "Position"
    # Links for position
    links.new(position.outputs[0], sample_index_002.inputs[1])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (828.7347412109375, 207.27243041992188)
    math.bl_label = "Math"
    math.operation = "DIVIDE"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 2.0
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(angle_between_vectors.outputs[0], math.inputs[0])
    links.new(math.outputs[0], vector_rotate.inputs[3])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (785.7593383789062, -89.51475524902344)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "CROSS_PRODUCT"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(vector_math.outputs[0], vector_rotate.inputs[2])
    links.new(sample_index_001.outputs[0], vector_math.inputs[1])
    links.new(sample_index.outputs[0], vector_math.inputs[0])

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
    links.new(vector_rotate.outputs[0], set_handle_positions.inputs[2])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (1089.6671142578125, -165.71905517578125)
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
    sample_index_003.location = (460.7041015625, -354.23822021484375)
    sample_index_003.bl_label = "Sample Index"
    sample_index_003.data_type = "FLOAT_VECTOR"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    # Links for sample_index_003
    links.new(position.outputs[0], sample_index_003.inputs[1])
    links.new(index.outputs[0], sample_index_003.inputs[2])
    links.new(separate_components_002.outputs[1], sample_index_003.inputs[0])
    links.new(sample_index_003.outputs[0], compare.inputs[4])

    debug_handles = nodes.new("GeometryNodeGroup")
    debug_handles.name = "Group.001"
    debug_handles.label = ""
    debug_handles.location = (1514.2930908203125, 313.65655517578125)
    debug_handles.node_tree = create_debug_handles_group()
    debug_handles.bl_label = "Group"
    # Index
    debug_handles.inputs[1].default_value = 9
    # Value
    debug_handles.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for debug_handles
    links.new(set_handle_positions.outputs[0], debug_handles.inputs[0])
    links.new(debug_handles.outputs[0], join_geometry.inputs[0])

    auto_layout_nodes(group)
    return group