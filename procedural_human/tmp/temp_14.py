import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_set_axis_group():
    group_name = "SetAxis"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Object", in_out="INPUT", socket_type="NodeSocketObject")
    socket.default_value = None
    socket = group.interface.new_socket(name="Name", in_out="INPUT", socket_type="NodeSocketString")
    socket.default_value = "axis+"

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (531.546142578125, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-541.546142578125, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (341.546142578125, 228.27078247070312)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001
    links.new(group_input.outputs[0], store_named_attribute_001.inputs[0])
    links.new(store_named_attribute_001.outputs[0], group_output.inputs[0])
    links.new(group_input.outputs[2], store_named_attribute_001.inputs[2])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (109.4755859375, 72.13540649414062)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "DISTANCE"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (-310.908447265625, 68.18743896484375)
    position.bl_label = "Position"
    # Links for position

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.label = ""
    sample_index_002.location = (-98.68994140625, 62.368072509765625)
    sample_index_002.bl_label = "Sample Index"
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    # Links for sample_index_002
    links.new(sample_index_002.outputs[0], vector_math.inputs[0])
    links.new(position.outputs[0], sample_index_002.inputs[1])
    links.new(group_input.outputs[0], sample_index_002.inputs[0])

    index_003 = nodes.new("GeometryNodeInputIndex")
    index_003.name = "Index.003"
    index_003.label = ""
    index_003.location = (-341.546142578125, -54.582550048828125)
    index_003.bl_label = "Index"
    # Links for index_003
    links.new(index_003.outputs[0], sample_index_002.inputs[2])

    object_info = nodes.new("GeometryNodeObjectInfo")
    object_info.name = "Object Info"
    object_info.label = ""
    object_info.location = (-82.888916015625, -178.52932739257812)
    object_info.bl_label = "Object Info"
    object_info.transform_space = "ORIGINAL"
    # As Instance
    object_info.inputs[1].default_value = False
    # Links for object_info
    links.new(object_info.outputs[1], vector_math.inputs[1])
    links.new(group_input.outputs[1], object_info.inputs[0])

    compare_007 = nodes.new("FunctionNodeCompare")
    compare_007.name = "Compare.007"
    compare_007.label = ""
    compare_007.location = (341.071044921875, -23.027130126953125)
    compare_007.bl_label = "Compare"
    compare_007.operation = "LESS_EQUAL"
    compare_007.data_type = "FLOAT"
    compare_007.mode = "ELEMENT"
    # B
    compare_007.inputs[1].default_value = 0.009999999776482582
    # A
    compare_007.inputs[2].default_value = 0
    # B
    compare_007.inputs[3].default_value = 0
    # A
    compare_007.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_007.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_007.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_007.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_007.inputs[8].default_value = ""
    # B
    compare_007.inputs[9].default_value = ""
    # C
    compare_007.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_007.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_007.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_007
    links.new(vector_math.outputs[1], compare_007.inputs[0])
    links.new(compare_007.outputs[0], store_named_attribute_001.inputs[1])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_weld__curves_group():
    group_name = "Weld Curves"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-653.830322265625, 108.69551086425781)
    group_input.bl_label = "Group Input"
    # Links for group_input

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2572.89404296875, 185.03811645507812)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (-140.27325439453125, 215.8501434326172)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "CURVE"
    # Links for domain_size

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.label = ""
    curve_line.location = (-302.34368896484375, 369.2785949707031)
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

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (76.75601196289062, 323.91796875)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = False
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Count"
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve
    links.new(domain_size.outputs[0], resample_curve.inputs[3])
    links.new(curve_line.outputs[0], resample_curve.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (260.81622314453125, 311.53399658203125)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Links for reroute_002
    links.new(resample_curve.outputs[0], reroute_002.inputs[0])

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.label = ""
    set_spline_type.location = (332.2375793457031, 290.21929931640625)
    set_spline_type.bl_label = "Set Spline Type"
    set_spline_type.spline_type = "BEZIER"
    # Selection
    set_spline_type.inputs[1].default_value = True
    # Links for set_spline_type
    links.new(reroute_002.outputs[0], set_spline_type.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (1189.354248046875, 188.57846069335938)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (1400.536376953125, 148.94627380371094)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001
    links.new(set_position.outputs[0], reroute_001.inputs[0])

    set_handle_positions = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions.name = "Set Handle Positions"
    set_handle_positions.label = ""
    set_handle_positions.location = (1460.0745849609375, 121.97119903564453)
    set_handle_positions.bl_label = "Set Handle Positions"
    set_handle_positions.mode = "LEFT"
    # Selection
    set_handle_positions.inputs[1].default_value = True
    # Offset
    set_handle_positions.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_handle_positions
    links.new(reroute_001.outputs[0], set_handle_positions.inputs[0])

    set_handle_positions_001 = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions_001.name = "Set Handle Positions.001"
    set_handle_positions_001.label = ""
    set_handle_positions_001.location = (1676.925048828125, 123.46479034423828)
    set_handle_positions_001.bl_label = "Set Handle Positions"
    set_handle_positions_001.mode = "RIGHT"
    # Selection
    set_handle_positions_001.inputs[1].default_value = True
    # Offset
    set_handle_positions_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_handle_positions_001
    links.new(set_handle_positions.outputs[0], set_handle_positions_001.inputs[0])

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.label = ""
    reroute_003.location = (188.863037109375, -100.882568359375)
    reroute_003.bl_label = "Reroute"
    reroute_003.socket_idname = "NodeSocketInt"
    # Links for reroute_003

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (-2.48687744140625, -13.6173095703125)
    position.bl_label = "Position"
    # Links for position

    curve_handle_positions = nodes.new("GeometryNodeInputCurveHandlePositions")
    curve_handle_positions.name = "Curve Handle Positions"
    curve_handle_positions.label = ""
    curve_handle_positions.location = (-3.63714599609375, -137.64468383789062)
    curve_handle_positions.bl_label = "Curve Handle Positions"
    # Relative
    curve_handle_positions.inputs[0].default_value = False
    # Links for curve_handle_positions

    reroute_004 = nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.label = ""
    reroute_004.location = (208.11392211914062, 30.921554565429688)
    reroute_004.bl_label = "Reroute"
    reroute_004.socket_idname = "NodeSocketGeometry"
    # Links for reroute_004

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (521.3038940429688, 135.3823699951172)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Links for sample_index
    links.new(reroute_004.outputs[0], sample_index.inputs[0])
    links.new(sample_index.outputs[0], set_position.inputs[2])
    links.new(position.outputs[0], sample_index.inputs[1])
    links.new(reroute_003.outputs[0], sample_index.inputs[2])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (987.7000122070312, 424.0278015136719)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Links for switch_001
    links.new(set_spline_type.outputs[0], switch_001.inputs[2])
    links.new(reroute_002.outputs[0], switch_001.inputs[1])
    links.new(switch_001.outputs[0], set_position.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (-206.071533203125, 49.907501220703125)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(reroute.outputs[0], domain_size.inputs[0])
    links.new(reroute.outputs[0], reroute_004.inputs[0])
    links.new(group_input.outputs[0], reroute.inputs[0])

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.name = "Sample Index.005"
    sample_index_005.label = ""
    sample_index_005.location = (361.031494140625, 681.4527587890625)
    sample_index_005.bl_label = "Sample Index"
    sample_index_005.data_type = "FLOAT"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    # Links for sample_index_005
    links.new(group_input.outputs[0], sample_index_005.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (588.638671875, 581.53173828125)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 2.0
    # B
    compare.inputs[3].default_value = 2
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.0, 0.0, 0.0, 0.0]
    # B
    compare.inputs[7].default_value = [0.0, 0.0, 0.0, 0.0]
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
    links.new(sample_index_005.outputs[0], compare.inputs[2])

    integer = nodes.new("FunctionNodeInputInt")
    integer.name = "Integer"
    integer.label = ""
    integer.location = (143.29940795898438, 511.2506103515625)
    integer.bl_label = "Integer"
    integer.integer = 0
    # Links for integer
    links.new(integer.outputs[0], sample_index_005.inputs[2])

    reroute_005 = nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.label = ""
    reroute_005.location = (785.169921875, 533.813720703125)
    reroute_005.bl_label = "Reroute"
    reroute_005.socket_idname = "NodeSocketBool"
    # Links for reroute_005
    links.new(reroute_005.outputs[0], switch_001.inputs[0])
    links.new(compare.outputs[0], reroute_005.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (144.30368041992188, 647.0281982421875)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "INT"
    # Name
    named_attribute.inputs[0].default_value = "curve_type"
    # Links for named_attribute
    links.new(named_attribute.outputs[0], sample_index_005.inputs[1])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (734.1484985351562, -0.188079833984375)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001
    links.new(reroute_004.outputs[0], sample_index_001.inputs[0])
    links.new(curve_handle_positions.outputs[0], sample_index_001.inputs[1])
    links.new(sample_index_001.outputs[0], set_handle_positions.inputs[2])
    links.new(reroute_003.outputs[0], sample_index_001.inputs[2])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.label = ""
    sample_index_002.location = (891.290283203125, -131.73471069335938)
    sample_index_002.bl_label = "Sample Index"
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    # Links for sample_index_002
    links.new(reroute_003.outputs[0], sample_index_002.inputs[2])
    links.new(curve_handle_positions.outputs[1], sample_index_002.inputs[1])
    links.new(reroute_004.outputs[0], sample_index_002.inputs[0])
    links.new(sample_index_002.outputs[0], set_handle_positions_001.inputs[2])

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.name = "Sample Index.003"
    sample_index_003.label = ""
    sample_index_003.location = (1197.531982421875, -217.16851806640625)
    sample_index_003.bl_label = "Sample Index"
    sample_index_003.data_type = "FLOAT"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    # Links for sample_index_003
    links.new(reroute_003.outputs[0], sample_index_003.inputs[2])

    curve_tilt = nodes.new("GeometryNodeInputCurveTilt")
    curve_tilt.name = "Curve Tilt"
    curve_tilt.label = ""
    curve_tilt.location = (991.5816650390625, -459.4078674316406)
    curve_tilt.bl_label = "Curve Tilt"
    # Links for curve_tilt
    links.new(curve_tilt.outputs[0], sample_index_003.inputs[1])

    radius = nodes.new("GeometryNodeInputRadius")
    radius.name = "Radius"
    radius.label = ""
    radius.location = (1002.8818359375, -526.7122802734375)
    radius.bl_label = "Radius"
    # Links for radius

    reroute_006 = nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.label = ""
    reroute_006.location = (761.84619140625, -412.3727111816406)
    reroute_006.bl_label = "Reroute"
    reroute_006.socket_idname = "NodeSocketGeometry"
    # Links for reroute_006
    links.new(reroute_006.outputs[0], sample_index_003.inputs[0])
    links.new(reroute_004.outputs[0], reroute_006.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    set_curve_tilt.label = ""
    set_curve_tilt.location = (2121.820556640625, 181.59811401367188)
    set_curve_tilt.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Links for set_curve_tilt
    links.new(sample_index_003.outputs[0], set_curve_tilt.inputs[2])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (1901.7294921875, 233.9946746826172)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(reroute_001.outputs[0], switch.inputs[1])
    links.new(set_handle_positions_001.outputs[0], switch.inputs[2])
    links.new(switch.outputs[0], set_curve_tilt.inputs[0])
    links.new(reroute_005.outputs[0], switch.inputs[0])

    set_curve_radius = nodes.new("GeometryNodeSetCurveRadius")
    set_curve_radius.name = "Set Curve Radius"
    set_curve_radius.label = ""
    set_curve_radius.location = (2324.908447265625, 174.50189208984375)
    set_curve_radius.bl_label = "Set Curve Radius"
    # Selection
    set_curve_radius.inputs[1].default_value = True
    # Links for set_curve_radius
    links.new(set_curve_tilt.outputs[0], set_curve_radius.inputs[0])
    links.new(set_curve_radius.outputs[0], group_output.inputs[0])

    sample_index_004 = nodes.new("GeometryNodeSampleIndex")
    sample_index_004.name = "Sample Index.004"
    sample_index_004.label = ""
    sample_index_004.location = (1369.5079345703125, -319.2707824707031)
    sample_index_004.bl_label = "Sample Index"
    sample_index_004.data_type = "FLOAT"
    sample_index_004.domain = "POINT"
    sample_index_004.clamp = False
    # Links for sample_index_004
    links.new(reroute_003.outputs[0], sample_index_004.inputs[2])
    links.new(reroute_006.outputs[0], sample_index_004.inputs[0])
    links.new(radius.outputs[0], sample_index_004.inputs[1])
    links.new(sample_index_004.outputs[0], set_curve_radius.inputs[2])

    viewer = nodes.new("GeometryNodeViewer")
    viewer.name = "Viewer"
    viewer.label = ""
    viewer.location = (2529.70654296875, 320.0043640136719)
    viewer.bl_label = "Viewer"
    viewer.ui_shortcut = 0
    viewer.active_index = 0
    viewer.domain = "AUTO"
    # Links for viewer
    links.new(set_curve_radius.outputs[0], viewer.inputs[0])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.label = ""
    named_attribute_001.location = (1870.690185546875, -346.57037353515625)
    named_attribute_001.bl_label = "Named Attribute"
    named_attribute_001.data_type = "FLOAT"
    # Name
    named_attribute_001.inputs[0].default_value = ""
    # Links for named_attribute_001

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (-212.94300842285156, -30.48084259033203)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "FLOORED_MODULO"
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(domain_size.outputs[0], integer_math.inputs[1])
    links.new(group_input.outputs[1], integer_math.inputs[0])
    links.new(integer_math.outputs[0], reroute_003.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_split_curves_about_axis_group():
    group_name = "SplitCurvesAboutAxis"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="CurvePos", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveNeg", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Curve", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2280.7548828125, -23.62287139892578)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1781.9263916015625, -278.87664794921875)
    group_input.bl_label = "Group Input"
    # Links for group_input

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.label = ""
    sample_curve.location = (-1581.9263916015625, -611.0350952148438)
    sample_curve.bl_label = "Sample Curve"
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = False
    sample_curve.data_type = "FLOAT"
    # Value
    sample_curve.inputs[1].default_value = 0.0
    # Factor
    sample_curve.inputs[2].default_value = 0.0
    # Length
    sample_curve.inputs[3].default_value = 0.0
    # Curve Index
    sample_curve.inputs[4].default_value = 0
    # Links for sample_curve

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.label = ""
    sample_index_002.location = (-1063.2467041015625, -1110.57568359375)
    sample_index_002.bl_label = "Sample Index"
    sample_index_002.data_type = "BOOLEAN"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    # Links for sample_index_002
    links.new(group_input.outputs[0], sample_index_002.inputs[0])

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.label = ""
    attribute_statistic.location = (-835.2241821289062, -889.5979614257812)
    attribute_statistic.bl_label = "Attribute Statistic"
    attribute_statistic.data_type = "FLOAT"
    attribute_statistic.domain = "POINT"
    # Links for attribute_statistic
    links.new(sample_index_002.outputs[0], attribute_statistic.inputs[1])
    links.new(group_input.outputs[0], attribute_statistic.inputs[0])

    index_003 = nodes.new("GeometryNodeInputIndex")
    index_003.name = "Index.003"
    index_003.label = ""
    index_003.location = (-1267.5443115234375, -1118.6982421875)
    index_003.bl_label = "Index"
    # Links for index_003
    links.new(index_003.outputs[0], attribute_statistic.inputs[2])
    links.new(index_003.outputs[0], sample_index_002.inputs[2])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (-1242.7745361328125, -1201.525390625)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "BOOLEAN"
    # Name
    named_attribute.inputs[0].default_value = "axis+"
    # Links for named_attribute
    links.new(named_attribute.outputs[0], sample_index_002.inputs[1])

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.name = "Sample Index.003"
    sample_index_003.label = ""
    sample_index_003.location = (-1119.7774658203125, -641.3611450195312)
    sample_index_003.bl_label = "Sample Index"
    sample_index_003.data_type = "BOOLEAN"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    # Links for sample_index_003
    links.new(group_input.outputs[0], sample_index_003.inputs[0])

    attribute_statistic_001 = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_001.name = "Attribute Statistic.001"
    attribute_statistic_001.label = ""
    attribute_statistic_001.location = (-1274.658447265625, -320.7618408203125)
    attribute_statistic_001.bl_label = "Attribute Statistic"
    attribute_statistic_001.data_type = "FLOAT"
    attribute_statistic_001.domain = "POINT"
    # Links for attribute_statistic_001
    links.new(sample_index_003.outputs[0], attribute_statistic_001.inputs[1])
    links.new(group_input.outputs[0], attribute_statistic_001.inputs[0])

    index_005 = nodes.new("GeometryNodeInputIndex")
    index_005.name = "Index.005"
    index_005.label = ""
    index_005.location = (-1324.0750732421875, -649.4838256835938)
    index_005.bl_label = "Index"
    # Links for index_005
    links.new(index_005.outputs[0], attribute_statistic_001.inputs[2])
    links.new(index_005.outputs[0], sample_index_003.inputs[2])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.label = ""
    named_attribute_001.location = (-1299.3052978515625, -732.3109741210938)
    named_attribute_001.bl_label = "Named Attribute"
    named_attribute_001.data_type = "BOOLEAN"
    # Name
    named_attribute_001.inputs[0].default_value = "axis-"
    # Links for named_attribute_001
    links.new(named_attribute_001.outputs[0], sample_index_003.inputs[1])

    separate_geometry_004 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_004.name = "Separate Geometry.004"
    separate_geometry_004.label = ""
    separate_geometry_004.location = (-224.56927490234375, -668.0817260742188)
    separate_geometry_004.bl_label = "Separate Geometry"
    separate_geometry_004.domain = "POINT"
    # Links for separate_geometry_004
    links.new(group_input.outputs[0], separate_geometry_004.inputs[0])

    compare_007 = nodes.new("FunctionNodeCompare")
    compare_007.name = "Compare.007"
    compare_007.label = ""
    compare_007.location = (-345.50994873046875, -1075.327392578125)
    compare_007.bl_label = "Compare"
    compare_007.operation = "GREATER_EQUAL"
    compare_007.data_type = "INT"
    compare_007.mode = "ELEMENT"
    # A
    compare_007.inputs[0].default_value = 0.0
    # B
    compare_007.inputs[1].default_value = 0.0
    # A
    compare_007.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_007.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_007.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_007.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_007.inputs[8].default_value = ""
    # B
    compare_007.inputs[9].default_value = ""
    # C
    compare_007.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_007.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_007.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_007
    links.new(index_003.outputs[0], compare_007.inputs[2])

    compare_008 = nodes.new("FunctionNodeCompare")
    compare_008.name = "Compare.008"
    compare_008.label = ""
    compare_008.location = (-381.44268798828125, -876.8381958007812)
    compare_008.bl_label = "Compare"
    compare_008.operation = "LESS_EQUAL"
    compare_008.data_type = "INT"
    compare_008.mode = "ELEMENT"
    # A
    compare_008.inputs[0].default_value = 0.0
    # B
    compare_008.inputs[1].default_value = 0.0
    # A
    compare_008.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_008.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_008.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_008.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_008.inputs[8].default_value = ""
    # B
    compare_008.inputs[9].default_value = ""
    # C
    compare_008.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_008.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_008.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_008
    links.new(index_003.outputs[0], compare_008.inputs[2])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (-151.47003173828125, -920.1058959960938)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "AND"
    # Links for boolean_math
    links.new(compare_007.outputs[0], boolean_math.inputs[0])
    links.new(compare_008.outputs[0], boolean_math.inputs[1])
    links.new(boolean_math.outputs[0], separate_geometry_004.inputs[1])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    set_spline_cyclic.label = ""
    set_spline_cyclic.location = (5.892765045166016, -611.6832885742188)
    set_spline_cyclic.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = False
    # Links for set_spline_cyclic
    links.new(separate_geometry_004.outputs[0], set_spline_cyclic.inputs[0])
    links.new(set_spline_cyclic.outputs[0], group_output.inputs[1])

    compare_009 = nodes.new("FunctionNodeCompare")
    compare_009.name = "Compare.009"
    compare_009.label = ""
    compare_009.location = (-516.8703002929688, -629.4653930664062)
    compare_009.bl_label = "Compare"
    compare_009.operation = "LESS_EQUAL"
    compare_009.data_type = "INT"
    compare_009.mode = "ELEMENT"
    # A
    compare_009.inputs[0].default_value = 0.0
    # B
    compare_009.inputs[1].default_value = 0.0
    # A
    compare_009.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_009.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_009.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_009.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_009.inputs[8].default_value = ""
    # B
    compare_009.inputs[9].default_value = ""
    # C
    compare_009.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_009.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_009.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_009
    links.new(index_003.outputs[0], compare_009.inputs[2])

    compare_010 = nodes.new("FunctionNodeCompare")
    compare_010.name = "Compare.010"
    compare_010.label = ""
    compare_010.location = (-506.2520446777344, -515.840576171875)
    compare_010.bl_label = "Compare"
    compare_010.operation = "GREATER_EQUAL"
    compare_010.data_type = "INT"
    compare_010.mode = "ELEMENT"
    # A
    compare_010.inputs[0].default_value = 0.0
    # B
    compare_010.inputs[1].default_value = 0.0
    # A
    compare_010.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_010.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_010.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_010.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_010.inputs[8].default_value = ""
    # B
    compare_010.inputs[9].default_value = ""
    # C
    compare_010.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_010.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_010.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_010
    links.new(index_003.outputs[0], compare_010.inputs[2])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.label = ""
    boolean_math_001.location = (-208.5948486328125, -361.4840393066406)
    boolean_math_001.bl_label = "Boolean Math"
    boolean_math_001.operation = "OR"
    # Links for boolean_math_001
    links.new(compare_009.outputs[0], boolean_math_001.inputs[0])
    links.new(compare_010.outputs[0], boolean_math_001.inputs[1])

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.label = ""
    reroute_003.location = (-884.3948364257812, -247.64447021484375)
    reroute_003.bl_label = "Reroute"
    reroute_003.socket_idname = "NodeSocketGeometry"
    # Links for reroute_003
    links.new(group_input.outputs[0], reroute_003.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (-507.3822937011719, -164.89926147460938)
    switch.bl_label = "Switch"
    switch.input_type = "INT"
    # Links for switch
    links.new(attribute_statistic_001.outputs[3], switch.inputs[2])
    links.new(attribute_statistic.outputs[4], switch.inputs[1])
    links.new(switch.outputs[0], compare_010.inputs[3])
    links.new(switch.outputs[0], compare_008.inputs[3])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (-676.6411743164062, -296.2898864746094)
    compare.bl_label = "Compare"
    compare.operation = "GREATER_THAN"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
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
    links.new(attribute_statistic_001.outputs[3], compare.inputs[0])
    links.new(attribute_statistic.outputs[4], compare.inputs[1])
    links.new(compare.outputs[0], switch.inputs[0])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (-496.5869140625, -348.44281005859375)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "INT"
    # Links for switch_001
    links.new(compare.outputs[0], switch_001.inputs[0])
    links.new(attribute_statistic.outputs[4], switch_001.inputs[2])
    links.new(attribute_statistic_001.outputs[3], switch_001.inputs[1])
    links.new(switch_001.outputs[0], compare_009.inputs[3])
    links.new(switch_001.outputs[0], compare_007.inputs[3])

    separate_geometry_005 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_005.name = "Separate Geometry.005"
    separate_geometry_005.label = ""
    separate_geometry_005.location = (97.76614379882812, -219.24166870117188)
    separate_geometry_005.bl_label = "Separate Geometry"
    separate_geometry_005.domain = "POINT"
    # Links for separate_geometry_005
    links.new(boolean_math_001.outputs[0], separate_geometry_005.inputs[1])
    links.new(group_input.outputs[0], separate_geometry_005.inputs[0])

    set_spline_cyclic_002 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_002.name = "Set Spline Cyclic.002"
    set_spline_cyclic_002.label = ""
    set_spline_cyclic_002.location = (328.2281799316406, -162.84323120117188)
    set_spline_cyclic_002.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic_002.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic_002.inputs[2].default_value = False
    # Links for set_spline_cyclic_002
    links.new(separate_geometry_005.outputs[0], set_spline_cyclic_002.inputs[0])

    weld_curves = nodes.new("GeometryNodeGroup")
    weld_curves.name = "Weld Curves.001"
    weld_curves.label = ""
    weld_curves.location = (713.2869262695312, -94.5709228515625)
    weld_curves.node_tree = create_weld__curves_group()
    weld_curves.bl_label = "Group"
    # Links for weld_curves
    links.new(set_spline_cyclic_002.outputs[0], weld_curves.inputs[0])
    links.new(weld_curves.outputs[0], group_output.inputs[0])

    index_007 = nodes.new("GeometryNodeInputIndex")
    index_007.name = "Index.007"
    index_007.label = ""
    index_007.location = (270.3264465332031, -289.97662353515625)
    index_007.bl_label = "Index"
    # Links for index_007

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (533.0, -238.42868041992188)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "ADD"
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(integer_math.outputs[0], weld_curves.inputs[1])
    links.new(index_007.outputs[0], integer_math.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (307.05712890625, -400.28125)
    math.bl_label = "Math"
    math.operation = "SUBTRACT"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 1.0
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(attribute_statistic_001.outputs[3], math.inputs[0])
    links.new(math.outputs[0], integer_math.inputs[1])

    auto_layout_nodes(group)
    return group

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
def create_perp_vectors_simple_group():
    group_name = "PerpVectorsSimple"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="U", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="V", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="U", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Normal", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (751.6455688476562, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-731.3544311523438, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], group_output.inputs[0])

    vector_math_013 = nodes.new("ShaderNodeVectorMath")
    vector_math_013.name = "Vector Math.013"
    vector_math_013.label = ""
    vector_math_013.location = (29.57269287109375, -35.83811950683594)
    vector_math_013.bl_label = "Vector Math"
    vector_math_013.operation = "CROSS_PRODUCT"
    # Vector
    vector_math_013.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_013.inputs[3].default_value = 1.0
    # Links for vector_math_013
    links.new(group_input.outputs[0], vector_math_013.inputs[0])
    links.new(group_input.outputs[1], vector_math_013.inputs[1])

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "V"
    frame_002.location = (-86.0, -142.0)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    vector_math_020 = nodes.new("ShaderNodeVectorMath")
    vector_math_020.name = "Vector Math.020"
    vector_math_020.label = ""
    vector_math_020.location = (267.3792724609375, -52.05003356933594)
    vector_math_020.bl_label = "Vector Math"
    vector_math_020.operation = "NORMALIZE"
    # Vector
    vector_math_020.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_020.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_020.inputs[3].default_value = 1.0
    # Links for vector_math_020
    links.new(vector_math_013.outputs[0], vector_math_020.inputs[0])
    links.new(vector_math_020.outputs[0], group_output.inputs[1])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_spherical_coords_group():
    group_name = "SphericalCoords"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Normal", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Inclination", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Asimuth", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="u", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="v", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="length", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="center", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 159
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Normal", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="U", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1249.538818359375, -257.2055358886719)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1297.44482421875, 119.60213470458984)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[2], group_output.inputs[0])

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (-960.4971923828125, -228.26548767089844)
    position_003.bl_label = "Position"
    # Links for position_003

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.name = "Sample Index.005"
    sample_index_005.label = ""
    sample_index_005.location = (-697.5897827148438, -91.59891510009766)
    sample_index_005.bl_label = "Sample Index"
    sample_index_005.data_type = "FLOAT_VECTOR"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    # Links for sample_index_005
    links.new(position_003.outputs[0], sample_index_005.inputs[1])
    links.new(group_input.outputs[0], sample_index_005.inputs[0])
    links.new(group_input.outputs[1], sample_index_005.inputs[2])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (-441.00006103515625, -466.3115234375)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketVector"
    # Links for reroute
    links.new(group_input.outputs[2], reroute.inputs[0])

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.label = ""
    vector_math_007.location = (-82.20596313476562, -1099.1424560546875)
    vector_math_007.bl_label = "Vector Math"
    vector_math_007.operation = "SUBTRACT"
    # Vector
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_007.inputs[3].default_value = 1.0
    # Links for vector_math_007

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (-463.0, -881.9312744140625)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketVector"
    # Links for reroute_001
    links.new(reroute_001.outputs[0], vector_math_007.inputs[0])
    links.new(sample_index_005.outputs[0], reroute_001.inputs[0])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.label = ""
    vector_math_008.location = (-411.4500427246094, -1089.5032958984375)
    vector_math_008.bl_label = "Vector Math"
    vector_math_008.operation = "DOT_PRODUCT"
    # Vector
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_008.inputs[3].default_value = 1.0
    # Links for vector_math_008
    links.new(reroute_001.outputs[0], vector_math_008.inputs[0])
    links.new(reroute.outputs[0], vector_math_008.inputs[1])

    vector_math_009 = nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.label = ""
    vector_math_009.location = (-263.1983947753906, -1050.4158935546875)
    vector_math_009.bl_label = "Vector Math"
    vector_math_009.operation = "SCALE"
    # Vector
    vector_math_009.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_009.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_009
    links.new(vector_math_008.outputs[1], vector_math_009.inputs[3])
    links.new(reroute.outputs[0], vector_math_009.inputs[0])
    links.new(vector_math_009.outputs[0], vector_math_007.inputs[1])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (1038.8651123046875, -507.9796142578125)
    math_004.bl_label = "Math"
    math_004.operation = "ARCTAN2"
    math_004.use_clamp = False
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(math_004.outputs[0], group_output.inputs[2])

    vector_math_010 = nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.label = ""
    vector_math_010.location = (814.1676025390625, -549.8902587890625)
    vector_math_010.bl_label = "Vector Math"
    vector_math_010.operation = "DOT_PRODUCT"
    # Vector
    vector_math_010.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_010.inputs[3].default_value = 1.0
    # Links for vector_math_010
    links.new(vector_math_007.outputs[0], vector_math_010.inputs[0])
    links.new(vector_math_010.outputs[1], math_004.inputs[0])

    vector_math_011 = nodes.new("ShaderNodeVectorMath")
    vector_math_011.name = "Vector Math.011"
    vector_math_011.label = ""
    vector_math_011.location = (811.153076171875, -744.36279296875)
    vector_math_011.bl_label = "Vector Math"
    vector_math_011.operation = "DOT_PRODUCT"
    # Vector
    vector_math_011.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_011.inputs[3].default_value = 1.0
    # Links for vector_math_011
    links.new(vector_math_007.outputs[0], vector_math_011.inputs[0])
    links.new(vector_math_011.outputs[1], math_004.inputs[1])
    links.new(group_input.outputs[3], vector_math_011.inputs[1])

    vector_math_012 = nodes.new("ShaderNodeVectorMath")
    vector_math_012.name = "Vector Math.012"
    vector_math_012.label = ""
    vector_math_012.location = (203.12255859375, 230.5105438232422)
    vector_math_012.bl_label = "Vector Math"
    vector_math_012.operation = "LENGTH"
    # Vector
    vector_math_012.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_012.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_012.inputs[3].default_value = 1.0
    # Links for vector_math_012
    links.new(sample_index_005.outputs[0], vector_math_012.inputs[0])
    links.new(vector_math_012.outputs[1], group_output.inputs[5])

    angle_between_vectors = nodes.new("GeometryNodeGroup")
    angle_between_vectors.name = "Group.001"
    angle_between_vectors.label = ""
    angle_between_vectors.location = (2.06182861328125, 48.78794860839844)
    angle_between_vectors.node_tree = create_angle_between_vectors_group()
    angle_between_vectors.bl_label = "Group"
    # Links for angle_between_vectors
    links.new(angle_between_vectors.outputs[0], group_output.inputs[1])
    links.new(sample_index_005.outputs[0], angle_between_vectors.inputs[1])
    links.new(group_input.outputs[2], angle_between_vectors.inputs[0])

    perp_vectors_simple = nodes.new("GeometryNodeGroup")
    perp_vectors_simple.name = "Group"
    perp_vectors_simple.label = ""
    perp_vectors_simple.location = (218.59158325195312, -405.6551208496094)
    perp_vectors_simple.node_tree = create_perp_vectors_simple_group()
    perp_vectors_simple.bl_label = "Group"
    # Links for perp_vectors_simple
    links.new(perp_vectors_simple.outputs[1], group_output.inputs[6])
    links.new(group_input.outputs[3], perp_vectors_simple.inputs[0])
    links.new(perp_vectors_simple.outputs[0], group_output.inputs[3])
    links.new(reroute.outputs[0], perp_vectors_simple.inputs[1])
    links.new(perp_vectors_simple.outputs[1], vector_math_010.inputs[1])
    links.new(perp_vectors_simple.outputs[1], group_output.inputs[4])

    auto_layout_nodes(group)
    return group

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
    math.location = (-554.2284545898438, 256.79571533203125)
    math.bl_label = "Math"
    math.operation = "COSINE"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.5
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(group_input.outputs[2], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-572.3478393554688, 144.98292541503906)
    math_001.bl_label = "Math"
    math_001.operation = "SINE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 0.5
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(group_input.outputs[1], math_001.inputs[0])

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
    links.new(math_001.outputs[0], math_002.inputs[0])
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
    math_004.location = (-565.5341796875, -4.827675819396973)
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
    math_006.location = (-576.91650390625, -131.52883911132812)
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
    links.new(math_004.outputs[0], math_007.inputs[1])

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
    math_008.location = (-535.3630981445312, -312.9976806640625)
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
    links.new(math_008.outputs[0], vector_math_005.inputs[3])
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

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_mix_sample_group():
    group_name = "MixSample"
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
    socket = group.interface.new_socket(name="CurveA", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Value", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="CurveB", in_out="INPUT", socket_type="NodeSocketGeometry")
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
    group_output.location = (721.3746337890625, 102.26183319091797)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-588.9310913085938, 4.869663238525391)
    group_input.bl_label = "Group Input"
    # Links for group_input

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

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-137.375732421875, 112.83964538574219)
    math_001.bl_label = "Math"
    math_001.operation = "FLOORED_MODULO"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(group_input.outputs[3], math_001.inputs[0])
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

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (429.01739501953125, 86.00204467773438)
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
    links.new(sample_index_005.outputs[0], mix.inputs[2])
    links.new(sample_index_006.outputs[0], mix.inputs[3])
    links.new(mix.outputs[0], group_output.inputs[0])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (138.5199737548828, -139.73809814453125)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(float_curve.outputs[0], mix.inputs[0])
    links.new(group_input.outputs[0], float_curve.inputs[1])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_closest_index_points_group():
    group_name = "ClosestIndexPoints"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Min", in_out="OUTPUT", socket_type="NodeSocketInt")
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="CurveA", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveA", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveB", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (-400.0, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1400.0, 75.0)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], group_output.inputs[1])

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.label = ""
    attribute_statistic.location = (-900.0, -150.0)
    attribute_statistic.bl_label = "Attribute Statistic"
    attribute_statistic.data_type = "FLOAT"
    attribute_statistic.domain = "POINT"
    # Selection
    attribute_statistic.inputs[1].default_value = True
    # Links for attribute_statistic
    links.new(group_input.outputs[0], attribute_statistic.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (-1137.111083984375, -23.234716415405273)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "POINTS"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity
    links.new(geometry_proximity.outputs[1], attribute_statistic.inputs[2])
    links.new(group_input.outputs[1], geometry_proximity.inputs[0])

    attribute_statistic_001 = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_001.name = "Attribute Statistic.001"
    attribute_statistic_001.label = ""
    attribute_statistic_001.location = (-650.0, 0.0)
    attribute_statistic_001.bl_label = "Attribute Statistic"
    attribute_statistic_001.data_type = "FLOAT"
    attribute_statistic_001.domain = "POINT"
    # Links for attribute_statistic_001
    links.new(group_input.outputs[0], attribute_statistic_001.inputs[0])
    links.new(attribute_statistic_001.outputs[3], group_output.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (-895.8106079101562, 69.92700958251953)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
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
    links.new(compare.outputs[0], attribute_statistic_001.inputs[1])
    links.new(attribute_statistic.outputs[3], compare.inputs[1])
    links.new(geometry_proximity.outputs[1], compare.inputs[0])

    index_003 = nodes.new("GeometryNodeInputIndex")
    index_003.name = "Index.003"
    index_003.label = ""
    index_003.location = (-1400.0, -75.0)
    index_003.bl_label = "Index"
    # Links for index_003
    links.new(index_003.outputs[0], attribute_statistic_001.inputs[2])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_get_index_offset_group():
    group_name = "GetIndexOffset"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="CurveA", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Offset Value", in_out="OUTPUT", socket_type="NodeSocketInt")
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Index Offset", in_out="OUTPUT", socket_type="NodeSocketInt")
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="CurveB", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="OffsetValue", in_out="OUTPUT", socket_type="NodeSocketInt")
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Index Offset", in_out="OUTPUT", socket_type="NodeSocketInt")
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="CurveA", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveB", in_out="INPUT", socket_type="NodeSocketGeometry")
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
    group_output.location = (128.305908203125, 18.488861083984375)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1399.0743408203125, 46.935203552246094)
    group_input.bl_label = "Group Input"
    # Links for group_input

    closest_index_points = nodes.new("GeometryNodeGroup")
    closest_index_points.name = "Group.002"
    closest_index_points.label = ""
    closest_index_points.location = (-1085.91845703125, 213.71585083007812)
    closest_index_points.node_tree = create_closest_index_points_group()
    closest_index_points.bl_label = "Group"
    # Links for closest_index_points
    links.new(group_input.outputs[0], closest_index_points.inputs[0])
    links.new(group_input.outputs[1], closest_index_points.inputs[1])
    links.new(closest_index_points.outputs[0], group_output.inputs[1])

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (-882.800537109375, -169.34527587890625)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "POINTCLOUD"
    # Links for domain_size
    links.new(group_input.outputs[0], domain_size.inputs[0])

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (-890.2810668945312, -42.27594757080078)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "SUBTRACT"
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(group_input.outputs[2], integer_math.inputs[0])

    integer_math_001 = nodes.new("FunctionNodeIntegerMath")
    integer_math_001.name = "Integer Math.001"
    integer_math_001.label = ""
    integer_math_001.location = (-564.529541015625, -128.26463317871094)
    integer_math_001.bl_label = "Integer Math"
    integer_math_001.operation = "FLOORED_MODULO"
    # Value
    integer_math_001.inputs[2].default_value = 0
    # Links for integer_math_001
    links.new(domain_size.outputs[0], integer_math_001.inputs[1])
    links.new(integer_math.outputs[0], integer_math_001.inputs[0])
    links.new(integer_math_001.outputs[0], group_output.inputs[5])

    closest_index_points_1 = nodes.new("GeometryNodeGroup")
    closest_index_points_1.name = "Group.006"
    closest_index_points_1.label = ""
    closest_index_points_1.location = (-1075.632568359375, -26.593198776245117)
    closest_index_points_1.node_tree = create_closest_index_points_group()
    closest_index_points_1.bl_label = "Group"
    # Links for closest_index_points_1
    links.new(group_input.outputs[0], closest_index_points_1.inputs[1])
    links.new(group_input.outputs[1], closest_index_points_1.inputs[0])
    links.new(closest_index_points_1.outputs[0], group_output.inputs[4])
    links.new(closest_index_points_1.outputs[1], group_output.inputs[3])
    links.new(closest_index_points_1.outputs[0], integer_math.inputs[1])

    domain_size_001 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_001.name = "Domain Size.001"
    domain_size_001.label = ""
    domain_size_001.location = (-803.3027954101562, 250.52816772460938)
    domain_size_001.bl_label = "Domain Size"
    domain_size_001.component = "POINTCLOUD"
    # Links for domain_size_001
    links.new(closest_index_points.outputs[1], domain_size_001.inputs[0])

    integer_math_002 = nodes.new("FunctionNodeIntegerMath")
    integer_math_002.name = "Integer Math.002"
    integer_math_002.label = ""
    integer_math_002.location = (-882.12451171875, 116.77193450927734)
    integer_math_002.bl_label = "Integer Math"
    integer_math_002.operation = "SUBTRACT"
    # Value
    integer_math_002.inputs[2].default_value = 0
    # Links for integer_math_002
    links.new(group_input.outputs[2], integer_math_002.inputs[0])
    links.new(closest_index_points.outputs[0], integer_math_002.inputs[1])

    integer_math_003 = nodes.new("FunctionNodeIntegerMath")
    integer_math_003.name = "Integer Math.003"
    integer_math_003.label = ""
    integer_math_003.location = (-554.7694091796875, 53.024009704589844)
    integer_math_003.bl_label = "Integer Math"
    integer_math_003.operation = "FLOORED_MODULO"
    # Value
    integer_math_003.inputs[2].default_value = 0
    # Links for integer_math_003
    links.new(domain_size_001.outputs[0], integer_math_003.inputs[1])
    links.new(integer_math_002.outputs[0], integer_math_003.inputs[0])
    links.new(integer_math_003.outputs[0], group_output.inputs[2])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (-187.963134765625, 360.31927490234375)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "INT"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "indexA"
    # Links for store_named_attribute
    links.new(integer_math_003.outputs[0], store_named_attribute.inputs[3])
    links.new(closest_index_points.outputs[1], store_named_attribute.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (430.8806457519531, -155.7249298095703)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "INT"
    store_named_attribute_002.domain = "POINT"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "indexB"
    # Links for store_named_attribute_002
    links.new(integer_math_001.outputs[0], store_named_attribute_002.inputs[3])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (-189.99737548828125, 180.73336791992188)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "INT"
    store_named_attribute_003.domain = "POINT"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "offsetA"
    # Links for store_named_attribute_003
    links.new(closest_index_points.outputs[0], store_named_attribute_003.inputs[3])
    links.new(store_named_attribute.outputs[0], store_named_attribute_003.inputs[0])
    links.new(store_named_attribute_003.outputs[0], store_named_attribute_002.inputs[0])

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (411.34515380859375, -405.65093994140625)
    store_named_attribute_004.bl_label = "Store Named Attribute"
    store_named_attribute_004.data_type = "INT"
    store_named_attribute_004.domain = "POINT"
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "offsetB"
    # Links for store_named_attribute_004
    links.new(store_named_attribute_002.outputs[0], store_named_attribute_004.inputs[0])
    links.new(store_named_attribute_004.outputs[0], group_output.inputs[0])
    links.new(closest_index_points_1.outputs[0], store_named_attribute_004.inputs[3])

    auto_layout_nodes(group)
    return group

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
    math.location = (-923.9249267578125, -271.87628173828125)
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
    links.new(math.outputs[0], math_001.inputs[0])

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
    math_003.location = (44.973960876464844, -109.38308715820312)
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
    links.new(store_named_attribute_001.outputs[0], group_output.inputs[1])

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
    links.new(math_009.outputs[0], group_output.inputs[0])

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

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_rotate_modulo_group():
    group_name = "RotateModulo"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Normal", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="AngleRotated", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Angle", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Axis", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 1.0, 0.0]
    socket.min_value = -1.0
    socket.max_value = 1.0
    socket = group.interface.new_socket(name="NormalA", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="NormalB", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Factor", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.5
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Center", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (917.6239013671875, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-927.6239013671875, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    vector_rotate = nodes.new("ShaderNodeVectorRotate")
    vector_rotate.name = "Vector Rotate"
    vector_rotate.label = ""
    vector_rotate.location = (476.7568664550781, 254.47760009765625)
    vector_rotate.bl_label = "Vector Rotate"
    vector_rotate.rotation_type = "AXIS_ANGLE"
    vector_rotate.invert = False
    # Rotation
    vector_rotate.inputs[4].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for vector_rotate
    links.new(group_input.outputs[1], vector_rotate.inputs[2])
    links.new(group_input.outputs[2], vector_rotate.inputs[0])
    links.new(vector_rotate.outputs[0], group_output.inputs[0])
    links.new(group_input.outputs[5], vector_rotate.inputs[1])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (194.0428009033203, -414.29925537109375)
    math_003.bl_label = "Math"
    math_003.operation = "MULTIPLY"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 6.2831854820251465
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (-984.9898681640625, -925.7344360351562)
    math_004.bl_label = "Math"
    math_004.operation = "FLOORED_MODULO"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 4.0
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(group_input.outputs[4], math_004.inputs[0])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (228.7541961669922, -705.5700073242188)
    math_005.bl_label = "Math"
    math_005.operation = "DIVIDE"
    math_005.use_clamp = False
    # Value
    math_005.inputs[1].default_value = 4.0
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(math_004.outputs[0], math_005.inputs[0])
    links.new(math_005.outputs[0], math_003.inputs[0])

    math_008 = nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.label = ""
    math_008.location = (-413.06512451171875, -631.7705078125)
    math_008.bl_label = "Math"
    math_008.operation = "DIVIDE"
    math_008.use_clamp = False
    # Value
    math_008.inputs[1].default_value = 2.0
    # Value
    math_008.inputs[2].default_value = 0.5
    # Links for math_008

    math_009 = nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.label = ""
    math_009.location = (-226.07379150390625, -626.710693359375)
    math_009.bl_label = "Math"
    math_009.operation = "TRUNC"
    math_009.use_clamp = False
    # Value
    math_009.inputs[1].default_value = 0.5
    # Value
    math_009.inputs[2].default_value = 0.5
    # Links for math_009
    links.new(math_008.outputs[0], math_009.inputs[0])

    math_010 = nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.label = ""
    math_010.location = (-484.9452819824219, -1066.0108642578125)
    math_010.bl_label = "Math"
    math_010.operation = "ADD"
    math_010.use_clamp = False
    # Value
    math_010.inputs[1].default_value = 1.0
    # Value
    math_010.inputs[2].default_value = 0.5
    # Links for math_010

    math_011 = nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.label = ""
    math_011.location = (-293.2920837402344, -1078.250732421875)
    math_011.bl_label = "Math"
    math_011.operation = "DIVIDE"
    math_011.use_clamp = False
    # Value
    math_011.inputs[1].default_value = 2.0
    # Value
    math_011.inputs[2].default_value = 0.5
    # Links for math_011
    links.new(math_010.outputs[0], math_011.inputs[0])

    math_012 = nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.label = ""
    math_012.location = (-598.1597290039062, -648.6722412109375)
    math_012.bl_label = "Math"
    math_012.operation = "TRUNC"
    math_012.use_clamp = False
    # Value
    math_012.inputs[1].default_value = 0.5
    # Value
    math_012.inputs[2].default_value = 0.5
    # Links for math_012
    links.new(math_012.outputs[0], math_008.inputs[0])
    links.new(math_004.outputs[0], math_012.inputs[0])

    math_013 = nodes.new("ShaderNodeMath")
    math_013.name = "Math.013"
    math_013.label = ""
    math_013.location = (-873.312255859375, -1357.3724365234375)
    math_013.bl_label = "Math"
    math_013.operation = "TRUNC"
    math_013.use_clamp = False
    # Value
    math_013.inputs[1].default_value = 0.5
    # Value
    math_013.inputs[2].default_value = 0.5
    # Links for math_013
    links.new(math_004.outputs[0], math_013.inputs[0])

    math_014 = nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.label = ""
    math_014.location = (-26.745006561279297, -596.6319580078125)
    math_014.bl_label = "Math"
    math_014.operation = "MULTIPLY"
    math_014.use_clamp = False
    # Value
    math_014.inputs[2].default_value = 0.5
    # Links for math_014
    links.new(math_009.outputs[0], math_014.inputs[1])

    math_015 = nodes.new("ShaderNodeMath")
    math_015.name = "Math.015"
    math_015.label = ""
    math_015.location = (90.86752319335938, -1015.5218505859375)
    math_015.bl_label = "Math"
    math_015.operation = "MULTIPLY"
    math_015.use_clamp = False
    # Value
    math_015.inputs[2].default_value = 0.5
    # Links for math_015
    links.new(group_input.outputs[0], math_015.inputs[0])

    math_016 = nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.label = ""
    math_016.location = (-223.9788818359375, -884.0120239257812)
    math_016.bl_label = "Math"
    math_016.operation = "SUBTRACT"
    math_016.use_clamp = False
    # Value
    math_016.inputs[0].default_value = 3.1415927410125732
    # Value
    math_016.inputs[2].default_value = 0.5
    # Links for math_016
    links.new(math_016.outputs[0], math_014.inputs[0])
    links.new(group_input.outputs[0], math_016.inputs[1])

    math_017 = nodes.new("ShaderNodeMath")
    math_017.name = "Math.017"
    math_017.label = ""
    math_017.location = (313.25555419921875, -898.5160522460938)
    math_017.bl_label = "Math"
    math_017.operation = "ADD"
    math_017.use_clamp = False
    # Value
    math_017.inputs[2].default_value = 0.5
    # Links for math_017
    links.new(math_015.outputs[0], math_017.inputs[0])
    links.new(math_014.outputs[0], math_017.inputs[1])

    integer_math_001 = nodes.new("FunctionNodeIntegerMath")
    integer_math_001.name = "Integer Math.001"
    integer_math_001.label = ""
    integer_math_001.location = (-667.899658203125, -1349.813232421875)
    integer_math_001.bl_label = "Integer Math"
    integer_math_001.operation = "MODULO"
    # Value
    integer_math_001.inputs[1].default_value = 2
    # Value
    integer_math_001.inputs[2].default_value = 0
    # Links for integer_math_001
    links.new(math_013.outputs[0], integer_math_001.inputs[0])

    math_018 = nodes.new("ShaderNodeMath")
    math_018.name = "Math.018"
    math_018.label = ""
    math_018.location = (-117.0, -1121.912841796875)
    math_018.bl_label = "Math"
    math_018.operation = "TRUNC"
    math_018.use_clamp = False
    # Value
    math_018.inputs[1].default_value = 0.5
    # Value
    math_018.inputs[2].default_value = 0.5
    # Links for math_018
    links.new(math_018.outputs[0], math_015.inputs[1])
    links.new(math_011.outputs[0], math_018.inputs[0])

    math_019 = nodes.new("ShaderNodeMath")
    math_019.name = "Math.019"
    math_019.label = ""
    math_019.location = (-677.8359985351562, -1037.0626220703125)
    math_019.bl_label = "Math"
    math_019.operation = "TRUNC"
    math_019.use_clamp = False
    # Value
    math_019.inputs[1].default_value = 0.5
    # Value
    math_019.inputs[2].default_value = 0.5
    # Links for math_019
    links.new(math_019.outputs[0], math_010.inputs[0])
    links.new(math_004.outputs[0], math_019.inputs[0])

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.label = ""
    switch_002.location = (101.2281494140625, -1253.0750732421875)
    switch_002.bl_label = "Switch"
    switch_002.input_type = "FLOAT"
    # Links for switch_002
    links.new(math_016.outputs[0], switch_002.inputs[1])
    links.new(group_input.outputs[0], switch_002.inputs[2])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (-460.3631896972656, -1288.61083984375)
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
    links.new(integer_math_001.outputs[0], compare_001.inputs[2])
    links.new(compare_001.outputs[0], switch_002.inputs[0])

    math_020 = nodes.new("ShaderNodeMath")
    math_020.name = "Math.020"
    math_020.label = ""
    math_020.location = (472.70361328125, -740.770263671875)
    math_020.bl_label = "Math"
    math_020.operation = "ADD"
    math_020.use_clamp = False
    # Value
    math_020.inputs[2].default_value = 0.5
    # Links for math_020
    links.new(math_017.outputs[0], math_020.inputs[1])
    links.new(math_020.outputs[0], vector_rotate.inputs[3])
    links.new(math_020.outputs[0], group_output.inputs[1])

    math_021 = nodes.new("ShaderNodeMath")
    math_021.name = "Math.021"
    math_021.label = ""
    math_021.location = (384.40118408203125, -1242.1575927734375)
    math_021.bl_label = "Math"
    math_021.operation = "MULTIPLY"
    math_021.use_clamp = False
    # Value
    math_021.inputs[2].default_value = 0.5
    # Links for math_021
    links.new(switch_002.outputs[0], math_021.inputs[0])
    links.new(math_021.outputs[0], math_020.inputs[0])

    math_022 = nodes.new("ShaderNodeMath")
    math_022.name = "Math.022"
    math_022.label = ""
    math_022.location = (-573.7567138671875, -1593.11669921875)
    math_022.bl_label = "Math"
    math_022.operation = "FLOORED_MODULO"
    math_022.use_clamp = False
    # Value
    math_022.inputs[1].default_value = 1.0
    # Value
    math_022.inputs[2].default_value = 0.5
    # Links for math_022
    links.new(math_004.outputs[0], math_022.inputs[0])
    links.new(math_022.outputs[0], math_021.inputs[1])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_tri_line_group():
    group_name = "TriLine"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Offset", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 1.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Offset", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 1.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Offset", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 1.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Offset", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 1.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (337.2384033203125, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-347.23828125, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    mesh_line = nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.label = ""
    mesh_line.location = (-169.26904296875, 494.29180908203125)
    mesh_line.bl_label = "Mesh Line"
    mesh_line.mode = "OFFSET"
    mesh_line.count_mode = "TOTAL"
    # Count
    mesh_line.inputs[0].default_value = 2
    # Resolution
    mesh_line.inputs[1].default_value = 1.0
    # Start Location
    mesh_line.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Links for mesh_line
    links.new(group_input.outputs[0], mesh_line.inputs[3])

    mesh_line_001 = nodes.new("GeometryNodeMeshLine")
    mesh_line_001.name = "Mesh Line.001"
    mesh_line_001.label = ""
    mesh_line_001.location = (-153.2540283203125, 249.5457305908203)
    mesh_line_001.bl_label = "Mesh Line"
    mesh_line_001.mode = "OFFSET"
    mesh_line_001.count_mode = "TOTAL"
    # Count
    mesh_line_001.inputs[0].default_value = 2
    # Resolution
    mesh_line_001.inputs[1].default_value = 1.0
    # Start Location
    mesh_line_001.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Links for mesh_line_001
    links.new(group_input.outputs[1], mesh_line_001.inputs[3])

    mesh_line_002 = nodes.new("GeometryNodeMeshLine")
    mesh_line_002.name = "Mesh Line.002"
    mesh_line_002.label = ""
    mesh_line_002.location = (-124.90472412109375, -3.535533905029297)
    mesh_line_002.bl_label = "Mesh Line"
    mesh_line_002.mode = "OFFSET"
    mesh_line_002.count_mode = "TOTAL"
    # Count
    mesh_line_002.inputs[0].default_value = 2
    # Resolution
    mesh_line_002.inputs[1].default_value = 1.0
    # Start Location
    mesh_line_002.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Links for mesh_line_002
    links.new(group_input.outputs[2], mesh_line_002.inputs[3])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (147.2384033203125, -14.810882568359375)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(mesh_line.outputs[0], join_geometry.inputs[0])
    links.new(mesh_line_001.outputs[0], join_geometry.inputs[0])
    links.new(mesh_line_002.outputs[0], join_geometry.inputs[0])
    links.new(join_geometry.outputs[0], group_output.inputs[0])

    mesh_line_003 = nodes.new("GeometryNodeMeshLine")
    mesh_line_003.name = "Mesh Line.003"
    mesh_line_003.label = ""
    mesh_line_003.location = (-84.55441284179688, -482.3179931640625)
    mesh_line_003.bl_label = "Mesh Line"
    mesh_line_003.mode = "OFFSET"
    mesh_line_003.count_mode = "TOTAL"
    # Count
    mesh_line_003.inputs[0].default_value = 2
    # Resolution
    mesh_line_003.inputs[1].default_value = 1.0
    # Start Location
    mesh_line_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Links for mesh_line_003
    links.new(group_input.outputs[3], mesh_line_003.inputs[3])
    links.new(mesh_line_003.outputs[0], join_geometry.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_find_angle_about_axis_group():
    group_name = "FindAngleAboutAxis"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="AxisAngle", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="NormalA", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="NormalB", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Axis", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Axis", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2242.950439453125, 125.25481414794922)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-509.5579833984375, -13.273642539978027)
    group_input.bl_label = "Group Input"
    # Links for group_input

    attribute_statistic_001 = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_001.name = "Attribute Statistic.001"
    attribute_statistic_001.label = "V2"
    attribute_statistic_001.location = (-64.8912353515625, -57.447349548339844)
    attribute_statistic_001.bl_label = "Attribute Statistic"
    attribute_statistic_001.data_type = "FLOAT_VECTOR"
    attribute_statistic_001.domain = "POINT"
    # Selection
    attribute_statistic_001.inputs[1].default_value = True
    # Links for attribute_statistic_001
    links.new(group_input.outputs[0], attribute_statistic_001.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (-299.7730712890625, -338.1766052246094)
    position_002.bl_label = "Position"
    # Links for position_002
    links.new(position_002.outputs[0], attribute_statistic_001.inputs[2])

    attribute_statistic_002 = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_002.name = "Attribute Statistic.002"
    attribute_statistic_002.label = "V1"
    attribute_statistic_002.location = (-74.6761474609375, 311.6293029785156)
    attribute_statistic_002.bl_label = "Attribute Statistic"
    attribute_statistic_002.data_type = "FLOAT_VECTOR"
    attribute_statistic_002.domain = "POINT"
    # Selection
    attribute_statistic_002.inputs[1].default_value = True
    # Links for attribute_statistic_002
    links.new(group_input.outputs[1], attribute_statistic_002.inputs[0])

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (-309.5579833984375, 30.900001525878906)
    position_003.bl_label = "Position"
    # Links for position_003
    links.new(position_003.outputs[0], attribute_statistic_002.inputs[2])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (152.9683837890625, -196.3247528076172)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "CROSS_PRODUCT"
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(attribute_statistic_001.outputs[0], vector_math_003.inputs[1])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (260.2647399902344, 272.6657409667969)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "DOT_PRODUCT"
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(attribute_statistic_002.outputs[0], vector_math_004.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (375.1629333496094, -91.8990478515625)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "DOT_PRODUCT"
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_005.inputs[3].default_value = 1.0
    # Links for vector_math_005
    links.new(attribute_statistic_001.outputs[0], vector_math_005.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (593.291015625, -126.66676330566406)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "SCALE"
    # Vector
    vector_math.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math
    links.new(vector_math_005.outputs[1], vector_math.inputs[3])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (562.3072509765625, 298.6588134765625)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "SCALE"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_001
    links.new(vector_math_004.outputs[1], vector_math_001.inputs[3])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (816.63232421875, 416.5107421875)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SUBTRACT"
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(attribute_statistic_002.outputs[0], vector_math_002.inputs[0])
    links.new(vector_math_001.outputs[0], vector_math_002.inputs[1])

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (888.9278564453125, -76.03976440429688)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "SUBTRACT"
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006
    links.new(attribute_statistic_001.outputs[0], vector_math_006.inputs[0])
    links.new(vector_math.outputs[0], vector_math_006.inputs[1])

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.label = ""
    vector_math_007.location = (1043.435302734375, 288.263916015625)
    vector_math_007.bl_label = "Vector Math"
    vector_math_007.operation = "NORMALIZE"
    # Vector
    vector_math_007.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_007.inputs[3].default_value = 1.0
    # Links for vector_math_007
    links.new(vector_math_002.outputs[0], vector_math_007.inputs[0])
    links.new(vector_math_007.outputs[0], group_output.inputs[1])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.label = ""
    vector_math_008.location = (1111.8577880859375, 68.49073791503906)
    vector_math_008.bl_label = "Vector Math"
    vector_math_008.operation = "NORMALIZE"
    # Vector
    vector_math_008.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_008.inputs[3].default_value = 1.0
    # Links for vector_math_008
    links.new(vector_math_006.outputs[0], vector_math_008.inputs[0])
    links.new(vector_math_008.outputs[0], group_output.inputs[2])

    vector_math_009 = nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.label = ""
    vector_math_009.location = (1317.5867919921875, 432.9709167480469)
    vector_math_009.bl_label = "Vector Math"
    vector_math_009.operation = "DOT_PRODUCT"
    # Vector
    vector_math_009.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_009.inputs[3].default_value = 1.0
    # Links for vector_math_009
    links.new(vector_math_007.outputs[0], vector_math_009.inputs[0])
    links.new(vector_math_008.outputs[0], vector_math_009.inputs[1])

    vector_math_010 = nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.label = ""
    vector_math_010.location = (1386.00927734375, 100.72518920898438)
    vector_math_010.bl_label = "Vector Math"
    vector_math_010.operation = "CROSS_PRODUCT"
    # Vector
    vector_math_010.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_010.inputs[3].default_value = 1.0
    # Links for vector_math_010
    links.new(vector_math_007.outputs[0], vector_math_010.inputs[0])
    links.new(vector_math_008.outputs[0], vector_math_010.inputs[1])

    vector_math_011 = nodes.new("ShaderNodeVectorMath")
    vector_math_011.name = "Vector Math.011"
    vector_math_011.label = ""
    vector_math_011.location = (1608.6024169921875, 18.707992553710938)
    vector_math_011.bl_label = "Vector Math"
    vector_math_011.operation = "DOT_PRODUCT"
    # Vector
    vector_math_011.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_011.inputs[3].default_value = 1.0
    # Links for vector_math_011
    links.new(vector_math_010.outputs[0], vector_math_011.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (1823.076171875, 245.01296997070312)
    math.bl_label = "Math"
    math.operation = "ARCTAN2"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(vector_math_011.outputs[1], math.inputs[0])
    links.new(vector_math_009.outputs[1], math.inputs[1])
    links.new(math.outputs[0], group_output.inputs[0])

    vector_math_012 = nodes.new("ShaderNodeVectorMath")
    vector_math_012.name = "Vector Math.012"
    vector_math_012.label = ""
    vector_math_012.location = (-391.00341796875, -181.34669494628906)
    vector_math_012.bl_label = "Vector Math"
    vector_math_012.operation = "NORMALIZE"
    # Vector
    vector_math_012.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_012.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_012.inputs[3].default_value = 1.0
    # Links for vector_math_012
    links.new(group_input.outputs[2], vector_math_012.inputs[0])
    links.new(vector_math_012.outputs[0], vector_math_003.inputs[0])
    links.new(vector_math_012.outputs[0], vector_math_005.inputs[1])
    links.new(vector_math_012.outputs[0], vector_math.inputs[0])
    links.new(vector_math_012.outputs[0], vector_math_004.inputs[1])
    links.new(vector_math_012.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_012.outputs[0], vector_math_011.inputs[1])
    links.new(vector_math_012.outputs[0], group_output.inputs[3])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_rotate_and_mix_curves_spherical_group():
    group_name = "RotateAndMixCurvesSpherical"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveA", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveB", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Index", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Factor", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.5
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="CommonAxis", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-2027.872314453125, -102.11109161376953)
    group_input.bl_label = "Group Input"
    # Links for group_input

    spherical_coords = nodes.new("GeometryNodeGroup")
    spherical_coords.name = "Group.008"
    spherical_coords.label = "SphericalB"
    spherical_coords.location = (-338.5374450683594, 68.12154388427734)
    spherical_coords.node_tree = create_spherical_coords_group()
    spherical_coords.bl_label = "Group"
    # Links for spherical_coords

    construct_vector = nodes.new("GeometryNodeGroup")
    construct_vector.name = "Group.006"
    construct_vector.label = ""
    construct_vector.location = (1215.45068359375, 313.8856201171875)
    construct_vector.node_tree = create_construct_vector_group()
    construct_vector.bl_label = "Group"
    # Links for construct_vector

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (1658.168701171875, 401.20806884765625)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position
    links.new(construct_vector.outputs[1], set_position.inputs[0])
    links.new(construct_vector.outputs[0], set_position.inputs[2])

    spherical_coords_1 = nodes.new("GeometryNodeGroup")
    spherical_coords_1.name = "VectorAngles"
    spherical_coords_1.label = "SphericalA"
    spherical_coords_1.location = (-376.0134582519531, 466.6144714355469)
    spherical_coords_1.node_tree = create_spherical_coords_group()
    spherical_coords_1.bl_label = "Group"
    # Links for spherical_coords_1

    mix_sample = nodes.new("GeometryNodeGroup")
    mix_sample.name = "Group.012"
    mix_sample.label = ""
    mix_sample.location = (256.9674377441406, 74.91156768798828)
    mix_sample.node_tree = create_mix_sample_group()
    mix_sample.bl_label = "Group"
    # Links for mix_sample
    links.new(spherical_coords.outputs[5], mix_sample.inputs[5])
    links.new(spherical_coords_1.outputs[5], mix_sample.inputs[2])
    links.new(mix_sample.outputs[0], construct_vector.inputs[5])

    perp_vectors_simple = nodes.new("GeometryNodeGroup")
    perp_vectors_simple.name = "Group.002"
    perp_vectors_simple.label = ""
    perp_vectors_simple.location = (164.22769165039062, -214.4324951171875)
    perp_vectors_simple.node_tree = create_perp_vectors_simple_group()
    perp_vectors_simple.bl_label = "Group"
    # Links for perp_vectors_simple
    links.new(perp_vectors_simple.outputs[1], construct_vector.inputs[4])
    links.new(perp_vectors_simple.outputs[0], construct_vector.inputs[3])

    get_index_offset = nodes.new("GeometryNodeGroup")
    get_index_offset.name = "GetIndexOffset"
    get_index_offset.label = ""
    get_index_offset.location = (-1114.658203125, 257.0685729980469)
    get_index_offset.node_tree = create_get_index_offset_group()
    get_index_offset.bl_label = "Group"
    # Links for get_index_offset
    links.new(get_index_offset.outputs[0], spherical_coords_1.inputs[0])
    links.new(get_index_offset.outputs[0], mix_sample.inputs[1])
    links.new(get_index_offset.outputs[3], mix_sample.inputs[4])
    links.new(get_index_offset.outputs[5], spherical_coords.inputs[1])
    links.new(get_index_offset.outputs[2], spherical_coords_1.inputs[1])
    links.new(get_index_offset.outputs[3], spherical_coords.inputs[0])
    links.new(get_index_offset.outputs[5], mix_sample.inputs[6])
    links.new(get_index_offset.outputs[2], mix_sample.inputs[3])
    links.new(group_input.outputs[0], get_index_offset.inputs[0])
    links.new(group_input.outputs[2], get_index_offset.inputs[2])
    links.new(group_input.outputs[1], get_index_offset.inputs[1])

    mix_angle = nodes.new("GeometryNodeGroup")
    mix_angle.name = "MixAngle"
    mix_angle.label = ""
    mix_angle.location = (298.398681640625, 406.36962890625)
    mix_angle.node_tree = create_mix_angle_group()
    mix_angle.bl_label = "Group"
    # Links for mix_angle
    links.new(get_index_offset.outputs[2], mix_angle.inputs[3])
    links.new(spherical_coords_1.outputs[2], mix_angle.inputs[2])
    links.new(mix_angle.outputs[1], construct_vector.inputs[6])
    links.new(mix_angle.outputs[0], construct_vector.inputs[2])
    links.new(get_index_offset.outputs[3], mix_angle.inputs[4])
    links.new(get_index_offset.outputs[5], mix_angle.inputs[6])
    links.new(get_index_offset.outputs[0], mix_angle.inputs[1])
    links.new(spherical_coords.outputs[2], mix_angle.inputs[5])

    mix_angle_1 = nodes.new("GeometryNodeGroup")
    mix_angle_1.name = "MixAngle.001"
    mix_angle_1.label = ""
    mix_angle_1.location = (239.1171875, 775.544921875)
    mix_angle_1.node_tree = create_mix_angle_group()
    mix_angle_1.bl_label = "Group"
    # Links for mix_angle_1
    links.new(get_index_offset.outputs[2], mix_angle_1.inputs[3])
    links.new(get_index_offset.outputs[5], mix_angle_1.inputs[6])
    links.new(get_index_offset.outputs[0], mix_angle_1.inputs[1])
    links.new(get_index_offset.outputs[3], mix_angle_1.inputs[4])
    links.new(spherical_coords_1.outputs[1], mix_angle_1.inputs[2])
    links.new(mix_angle_1.outputs[0], construct_vector.inputs[1])
    links.new(spherical_coords.outputs[1], mix_angle_1.inputs[5])

    rotate_modulo = nodes.new("GeometryNodeGroup")
    rotate_modulo.name = "Group.011"
    rotate_modulo.label = ""
    rotate_modulo.location = (-356.638671875, -576.537841796875)
    rotate_modulo.node_tree = create_rotate_modulo_group()
    rotate_modulo.bl_label = "Group"
    # Center
    rotate_modulo.inputs[5].default_value = [0.0, 0.0, 0.0]
    # Links for rotate_modulo
    links.new(rotate_modulo.outputs[0], construct_vector.inputs[0])
    links.new(rotate_modulo.outputs[0], perp_vectors_simple.inputs[1])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-1096.5289306640625, -522.4593505859375)
    math.bl_label = "Math"
    math.operation = "PINGPONG"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 1.0
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(math.outputs[0], mix_angle.inputs[0])
    links.new(math.outputs[0], mix_angle_1.inputs[0])
    links.new(math.outputs[0], mix_sample.inputs[0])

    tri_line = nodes.new("GeometryNodeGroup")
    tri_line.name = "TriLine"
    tri_line.label = ""
    tri_line.location = (874.246337890625, -321.6324462890625)
    tri_line.node_tree = create_tri_line_group()
    tri_line.bl_label = "Group"
    # Links for tri_line
    links.new(rotate_modulo.outputs[0], tri_line.inputs[0])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (1836.0140380859375, 87.6494140625)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(tri_line.outputs[0], join_geometry_001.inputs[0])
    links.new(set_position.outputs[0], join_geometry_001.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (-1744.55322265625, -447.71405029296875)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketFloat"
    # Links for reroute
    links.new(reroute.outputs[0], rotate_modulo.inputs[4])
    links.new(reroute.outputs[0], math.inputs[0])
    links.new(group_input.outputs[3], reroute.inputs[0])

    find_angle_about_axis = nodes.new("GeometryNodeGroup")
    find_angle_about_axis.name = "Group.001"
    find_angle_about_axis.label = ""
    find_angle_about_axis.location = (-1078.385009765625, -138.2272186279297)
    find_angle_about_axis.node_tree = create_find_angle_about_axis_group()
    find_angle_about_axis.bl_label = "Group"
    # Links for find_angle_about_axis
    links.new(group_input.outputs[1], find_angle_about_axis.inputs[0])
    links.new(group_input.outputs[4], find_angle_about_axis.inputs[2])
    links.new(group_input.outputs[0], find_angle_about_axis.inputs[1])
    links.new(find_angle_about_axis.outputs[0], rotate_modulo.inputs[0])
    links.new(find_angle_about_axis.outputs[1], rotate_modulo.inputs[2])
    links.new(find_angle_about_axis.outputs[1], spherical_coords_1.inputs[2])
    links.new(find_angle_about_axis.outputs[2], rotate_modulo.inputs[3])
    links.new(find_angle_about_axis.outputs[2], spherical_coords.inputs[2])
    links.new(find_angle_about_axis.outputs[1], tri_line.inputs[1])
    links.new(find_angle_about_axis.outputs[2], tri_line.inputs[2])
    links.new(find_angle_about_axis.outputs[3], rotate_modulo.inputs[1])
    links.new(find_angle_about_axis.outputs[3], tri_line.inputs[3])
    links.new(find_angle_about_axis.outputs[3], spherical_coords.inputs[3])
    links.new(find_angle_about_axis.outputs[3], spherical_coords_1.inputs[3])
    links.new(find_angle_about_axis.outputs[3], perp_vectors_simple.inputs[0])

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2174.226318359375, 53.16731262207031)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output
    links.new(set_position.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create__axis_alignment_switch_group():
    group_name = ".axis_alignment_switch"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Output", in_out="OUTPUT", socket_type="NodeSocketRotation")
    socket = group.interface.new_socket(name="Menu", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "X"
    socket = group.interface.new_socket(name="Menu", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "X"
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1060.0, 120.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1066.653076171875, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    menu_switch_007 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_007.name = "Menu Switch.007"
    menu_switch_007.label = ""
    menu_switch_007.location = (-862.7600708007812, 144.72216796875)
    menu_switch_007.bl_label = "Menu Switch"
    menu_switch_007.active_index = 2
    menu_switch_007.data_type = "INT"
    # X
    menu_switch_007.inputs[1].default_value = 0
    # Y
    menu_switch_007.inputs[2].default_value = 1
    # Z
    menu_switch_007.inputs[3].default_value = 2
    # Links for menu_switch_007
    links.new(group_input.outputs[0], menu_switch_007.inputs[0])

    menu_switch_008 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_008.name = "Menu Switch.008"
    menu_switch_008.label = ""
    menu_switch_008.location = (-866.6530151367188, -137.067138671875)
    menu_switch_008.bl_label = "Menu Switch"
    menu_switch_008.active_index = 2
    menu_switch_008.data_type = "INT"
    # X
    menu_switch_008.inputs[1].default_value = 0
    # Y
    menu_switch_008.inputs[2].default_value = 1
    # Z
    menu_switch_008.inputs[3].default_value = 2
    # Links for menu_switch_008
    links.new(group_input.outputs[1], menu_switch_008.inputs[0])

    axes_to_rotation_004 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_004.name = "Axes to Rotation.004"
    axes_to_rotation_004.label = ""
    axes_to_rotation_004.location = (-200.0, 0.0)
    axes_to_rotation_004.bl_label = "Axes to Rotation"
    axes_to_rotation_004.primary_axis = "X"
    axes_to_rotation_004.secondary_axis = "Y"
    # Links for axes_to_rotation_004

    axes_to_rotation_005 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_005.name = "Axes to Rotation.005"
    axes_to_rotation_005.label = ""
    axes_to_rotation_005.location = (-200.0, -160.0)
    axes_to_rotation_005.bl_label = "Axes to Rotation"
    axes_to_rotation_005.primary_axis = "X"
    axes_to_rotation_005.secondary_axis = "Z"
    # Links for axes_to_rotation_005

    index_switch_012 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_012.name = "Index Switch.012"
    index_switch_012.label = ""
    index_switch_012.location = (660.0, 60.0)
    index_switch_012.bl_label = "Index Switch"
    index_switch_012.data_type = "ROTATION"
    # Links for index_switch_012
    links.new(menu_switch_007.outputs[0], index_switch_012.inputs[0])

    index_switch_013 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_013.name = "Index Switch.013"
    index_switch_013.label = ""
    index_switch_013.location = (440.0, -60.0)
    index_switch_013.bl_label = "Index Switch"
    index_switch_013.data_type = "ROTATION"
    # 0
    index_switch_013.inputs[1].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for index_switch_013
    links.new(axes_to_rotation_004.outputs[0], index_switch_013.inputs[2])
    links.new(axes_to_rotation_005.outputs[0], index_switch_013.inputs[3])
    links.new(index_switch_013.outputs[0], index_switch_012.inputs[1])

    index_switch_014 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_014.name = "Index Switch.014"
    index_switch_014.label = ""
    index_switch_014.location = (440.0, -140.0)
    index_switch_014.bl_label = "Index Switch"
    index_switch_014.data_type = "ROTATION"
    # 1
    index_switch_014.inputs[2].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for index_switch_014
    links.new(index_switch_014.outputs[0], index_switch_012.inputs[2])

    index_switch_015 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_015.name = "Index Switch.015"
    index_switch_015.label = ""
    index_switch_015.location = (440.0, -220.00001525878906)
    index_switch_015.bl_label = "Index Switch"
    index_switch_015.data_type = "ROTATION"
    # 2
    index_switch_015.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for index_switch_015
    links.new(index_switch_015.outputs[0], index_switch_012.inputs[3])

    reroute_056 = nodes.new("NodeReroute")
    reroute_056.name = "Reroute.056"
    reroute_056.label = ""
    reroute_056.location = (320.0, -140.00001525878906)
    reroute_056.bl_label = "Reroute"
    reroute_056.socket_idname = "NodeSocketInt"
    # Links for reroute_056
    links.new(reroute_056.outputs[0], index_switch_014.inputs[0])
    links.new(reroute_056.outputs[0], index_switch_013.inputs[0])
    links.new(menu_switch_008.outputs[0], reroute_056.inputs[0])
    links.new(reroute_056.outputs[0], index_switch_015.inputs[0])

    axes_to_rotation_006 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_006.name = "Axes to Rotation.006"
    axes_to_rotation_006.label = ""
    axes_to_rotation_006.location = (-20.0, -240.0)
    axes_to_rotation_006.bl_label = "Axes to Rotation"
    axes_to_rotation_006.primary_axis = "Y"
    axes_to_rotation_006.secondary_axis = "X"
    # Links for axes_to_rotation_006
    links.new(axes_to_rotation_006.outputs[0], index_switch_014.inputs[1])

    axes_to_rotation_007 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_007.name = "Axes to Rotation.007"
    axes_to_rotation_007.label = ""
    axes_to_rotation_007.location = (-20.0, -400.0)
    axes_to_rotation_007.bl_label = "Axes to Rotation"
    axes_to_rotation_007.primary_axis = "Y"
    axes_to_rotation_007.secondary_axis = "Z"
    # Links for axes_to_rotation_007
    links.new(axes_to_rotation_007.outputs[0], index_switch_014.inputs[3])

    axes_to_rotation_008 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_008.name = "Axes to Rotation.008"
    axes_to_rotation_008.label = ""
    axes_to_rotation_008.location = (160.0, -480.0)
    axes_to_rotation_008.bl_label = "Axes to Rotation"
    axes_to_rotation_008.primary_axis = "Z"
    axes_to_rotation_008.secondary_axis = "X"
    # Links for axes_to_rotation_008
    links.new(axes_to_rotation_008.outputs[0], index_switch_015.inputs[1])

    axes_to_rotation_009 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_009.name = "Axes to Rotation.009"
    axes_to_rotation_009.label = ""
    axes_to_rotation_009.location = (160.0, -640.0)
    axes_to_rotation_009.bl_label = "Axes to Rotation"
    axes_to_rotation_009.primary_axis = "Z"
    axes_to_rotation_009.secondary_axis = "Y"
    # Links for axes_to_rotation_009
    links.new(axes_to_rotation_009.outputs[0], index_switch_015.inputs[2])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (-400.0, 259.9999694824219)
    compare_005.bl_label = "Compare"
    compare_005.operation = "EQUAL"
    compare_005.data_type = "INT"
    compare_005.mode = "ELEMENT"
    # A
    compare_005.inputs[0].default_value = 0.0
    # B
    compare_005.inputs[1].default_value = 0.0
    # A
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_005.inputs[8].default_value = ""
    # B
    compare_005.inputs[9].default_value = ""
    # C
    compare_005.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_005.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_005.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_005
    links.new(menu_switch_008.outputs[0], compare_005.inputs[3])
    links.new(menu_switch_007.outputs[0], compare_005.inputs[2])

    reroute_059 = nodes.new("NodeReroute")
    reroute_059.name = "Reroute.059"
    reroute_059.label = ""
    reroute_059.location = (-306.47357177734375, -159.8908233642578)
    reroute_059.bl_label = "Reroute"
    reroute_059.socket_idname = "NodeSocketVector"
    # Links for reroute_059
    links.new(reroute_059.outputs[0], axes_to_rotation_005.inputs[0])
    links.new(reroute_059.outputs[0], axes_to_rotation_004.inputs[0])
    links.new(reroute_059.outputs[0], axes_to_rotation_008.inputs[0])
    links.new(reroute_059.outputs[0], axes_to_rotation_009.inputs[0])
    links.new(reroute_059.outputs[0], axes_to_rotation_006.inputs[0])
    links.new(reroute_059.outputs[0], axes_to_rotation_007.inputs[0])
    links.new(group_input.outputs[2], reroute_059.inputs[0])

    reroute_060 = nodes.new("NodeReroute")
    reroute_060.name = "Reroute.060"
    reroute_060.label = ""
    reroute_060.location = (-313.8742980957031, -198.2582550048828)
    reroute_060.bl_label = "Reroute"
    reroute_060.socket_idname = "NodeSocketVector"
    # Links for reroute_060
    links.new(reroute_060.outputs[0], axes_to_rotation_006.inputs[1])
    links.new(reroute_060.outputs[0], axes_to_rotation_009.inputs[1])
    links.new(reroute_060.outputs[0], axes_to_rotation_007.inputs[1])
    links.new(reroute_060.outputs[0], axes_to_rotation_008.inputs[1])
    links.new(reroute_060.outputs[0], axes_to_rotation_005.inputs[1])
    links.new(reroute_060.outputs[0], axes_to_rotation_004.inputs[1])
    links.new(group_input.outputs[3], reroute_060.inputs[0])

    warning_002 = nodes.new("GeometryNodeWarning")
    warning_002.name = "Warning.002"
    warning_002.label = ""
    warning_002.location = (-220.0, 259.9999694824219)
    warning_002.bl_label = "Warning"
    warning_002.warning_type = "WARNING"
    # Message
    warning_002.inputs[1].default_value = "Equal Axes"
    # Links for warning_002
    links.new(compare_005.outputs[0], warning_002.inputs[0])

    switch_028 = nodes.new("GeometryNodeSwitch")
    switch_028.name = "Switch.028"
    switch_028.label = ""
    switch_028.location = (860.0, 160.00001525878906)
    switch_028.bl_label = "Switch"
    switch_028.input_type = "ROTATION"
    # True
    switch_028.inputs[2].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for switch_028
    links.new(index_switch_012.outputs[0], switch_028.inputs[1])
    links.new(warning_002.outputs[0], switch_028.inputs[0])
    links.new(switch_028.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_randomize__transforms_group():
    group_name = "Randomize Transforms"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Instances", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Instances", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Selection", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = True
    socket = group.interface.new_socket(name="Local Space", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = True
    socket = group.interface.new_socket(name="Offset", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Rotation", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Scale Axes", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "Uniform"
    socket = group.interface.new_socket(name="Scale", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = 0.0
    socket.max_value = 1.0
    socket = group.interface.new_socket(name="Scale", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    socket.min_value = 0.0
    socket.max_value = 1.0
    socket = group.interface.new_socket(name="Flipping", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = 0.0
    socket.max_value = 1.0
    socket = group.interface.new_socket(name="Seed", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1484.562255859375, 64.49579620361328)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-340.0, 200.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    rotate_instances = nodes.new("GeometryNodeRotateInstances")
    rotate_instances.name = "Rotate Instances"
    rotate_instances.label = ""
    rotate_instances.location = (636.3701782226562, 180.06201171875)
    rotate_instances.bl_label = "Rotate Instances"
    # Links for rotate_instances
    links.new(group_input.outputs[0], rotate_instances.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (-140.88572692871094, -18.094011306762695)
    random_value.bl_label = "Random Value"
    random_value.data_type = "FLOAT_VECTOR"
    # Min
    random_value.inputs[2].default_value = 0.0
    # Max
    random_value.inputs[3].default_value = 1.0
    # Min
    random_value.inputs[4].default_value = 0
    # Max
    random_value.inputs[5].default_value = 100
    # Probability
    random_value.inputs[6].default_value = 0.5
    # ID
    random_value.inputs[7].default_value = 0
    # Links for random_value
    links.new(random_value.outputs[0], rotate_instances.inputs[2])

    scale_instances = nodes.new("GeometryNodeScaleInstances")
    scale_instances.name = "Scale Instances"
    scale_instances.label = ""
    scale_instances.location = (1283.676513671875, 86.40182495117188)
    scale_instances.bl_label = "Scale Instances"
    # Links for scale_instances
    links.new(scale_instances.outputs[0], group_output.inputs[0])

    group_input_021 = nodes.new("NodeGroupInput")
    group_input_021.name = "Group Input.021"
    group_input_021.label = ""
    group_input_021.location = (-540.0, -59.999996185302734)
    group_input_021.bl_label = "Group Input"
    # Links for group_input_021

    vector_math_010 = nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.label = ""
    vector_math_010.location = (-340.8857116699219, 21.905988693237305)
    vector_math_010.bl_label = "Vector Math"
    vector_math_010.operation = "SCALE"
    # Vector
    vector_math_010.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_010.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_010.inputs[3].default_value = -0.5
    # Links for vector_math_010
    links.new(vector_math_010.outputs[0], random_value.inputs[0])
    links.new(group_input_021.outputs[4], vector_math_010.inputs[0])

    vector_math_011 = nodes.new("ShaderNodeVectorMath")
    vector_math_011.name = "Vector Math.011"
    vector_math_011.label = ""
    vector_math_011.location = (-340.8857116699219, -98.09397888183594)
    vector_math_011.bl_label = "Vector Math"
    vector_math_011.operation = "SCALE"
    # Vector
    vector_math_011.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_011.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_011.inputs[3].default_value = 0.5
    # Links for vector_math_011
    links.new(vector_math_011.outputs[0], random_value.inputs[1])
    links.new(group_input_021.outputs[4], vector_math_011.inputs[0])

    group_input_024 = nodes.new("NodeGroupInput")
    group_input_024.name = "Group Input.024"
    group_input_024.label = ""
    group_input_024.location = (-733.5711669921875, -304.7391662597656)
    group_input_024.bl_label = "Group Input"
    # Links for group_input_024

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (525.50341796875, 103.64305877685547)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketBool"
    # Links for reroute
    links.new(reroute.outputs[0], rotate_instances.inputs[1])
    links.new(group_input.outputs[1], reroute.inputs[0])

    random_value_005 = nodes.new("FunctionNodeRandomValue")
    random_value_005.name = "Random Value.005"
    random_value_005.label = ""
    random_value_005.location = (690.5350952148438, -35.71200180053711)
    random_value_005.bl_label = "Random Value"
    random_value_005.data_type = "FLOAT_VECTOR"
    # Min
    random_value_005.inputs[0].default_value = [-1.0, -1.0, -1.0]
    # Max
    random_value_005.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_005.inputs[2].default_value = 0.0
    # Max
    random_value_005.inputs[3].default_value = 1.0
    # Min
    random_value_005.inputs[4].default_value = 0
    # Max
    random_value_005.inputs[5].default_value = 100
    # Probability
    random_value_005.inputs[6].default_value = 0.5
    # ID
    random_value_005.inputs[7].default_value = 0
    # Links for random_value_005

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (886.31298828125, -78.50513458251953)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "MULTIPLY"
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(random_value_005.outputs[0], vector_math_004.inputs[0])

    random_value_008 = nodes.new("FunctionNodeRandomValue")
    random_value_008.name = "Random Value.008"
    random_value_008.label = ""
    random_value_008.location = (501.5194396972656, -612.4253540039062)
    random_value_008.bl_label = "Random Value"
    random_value_008.data_type = "FLOAT_VECTOR"
    # Min
    random_value_008.inputs[2].default_value = 0.0
    # Max
    random_value_008.inputs[3].default_value = 1.0
    # Min
    random_value_008.inputs[4].default_value = 0
    # Max
    random_value_008.inputs[5].default_value = 100
    # Probability
    random_value_008.inputs[6].default_value = 0.5
    # ID
    random_value_008.inputs[7].default_value = 0
    # Links for random_value_008

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (273.23504638671875, -568.8362426757812)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "SUBTRACT"
    # Vector
    vector_math_001.inputs[0].default_value = [1.0, 1.0, 1.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(vector_math_001.outputs[0], random_value_008.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (273.23504638671875, -742.564453125)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SUBTRACT"
    # Vector
    vector_math_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], random_value_008.inputs[1])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (700.1310424804688, -628.0283203125)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "SIGN"
    # Vector
    vector_math_003.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(random_value_008.outputs[0], vector_math_003.inputs[0])

    translate_instances = nodes.new("GeometryNodeTranslateInstances")
    translate_instances.name = "Translate Instances"
    translate_instances.label = ""
    translate_instances.location = (1067.9522705078125, 125.88878631591797)
    translate_instances.bl_label = "Translate Instances"
    # Links for translate_instances
    links.new(vector_math_004.outputs[0], translate_instances.inputs[2])
    links.new(rotate_instances.outputs[0], translate_instances.inputs[0])
    links.new(translate_instances.outputs[0], scale_instances.inputs[0])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (688.6309814453125, -327.3764953613281)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[3], vector_math_004.inputs[1])

    hash_value_004 = nodes.new("FunctionNodeHashValue")
    hash_value_004.name = "Hash Value.004"
    hash_value_004.label = ""
    hash_value_004.location = (-360.4606018066406, -300.5281066894531)
    hash_value_004.bl_label = "Hash Value"
    hash_value_004.data_type = "INT"
    # Seed
    hash_value_004.inputs[1].default_value = 76836728
    # Links for hash_value_004

    hash_value_007 = nodes.new("FunctionNodeHashValue")
    hash_value_007.name = "Hash Value.007"
    hash_value_007.label = ""
    hash_value_007.location = (-552.2808227539062, -299.7030029296875)
    hash_value_007.bl_label = "Hash Value"
    hash_value_007.data_type = "INT"
    # Seed
    hash_value_007.inputs[1].default_value = 465656096
    # Links for hash_value_007
    links.new(hash_value_007.outputs[0], hash_value_004.inputs[0])
    links.new(group_input_024.outputs[9], hash_value_007.inputs[0])
    links.new(hash_value_007.outputs[0], random_value.inputs[8])

    menu_switch_007 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_007.name = "Menu Switch.007"
    menu_switch_007.label = ""
    menu_switch_007.location = (-102.30133056640625, -238.5729217529297)
    menu_switch_007.bl_label = "Menu Switch"
    menu_switch_007.active_index = 0
    menu_switch_007.data_type = "INT"
    # Uniform
    menu_switch_007.inputs[1].default_value = 0
    # Axes
    menu_switch_007.inputs[2].default_value = 1
    # Links for menu_switch_007

    group_input_002 = nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.label = ""
    group_input_002.location = (-347.74072265625, -478.95428466796875)
    group_input_002.bl_label = "Group Input"
    # Links for group_input_002
    links.new(group_input_002.outputs[5], menu_switch_007.inputs[0])

    random_value_004 = nodes.new("FunctionNodeRandomValue")
    random_value_004.name = "Random Value.004"
    random_value_004.label = ""
    random_value_004.location = (-100.10758972167969, -392.4493408203125)
    random_value_004.bl_label = "Random Value"
    random_value_004.data_type = "FLOAT_VECTOR"
    # Min
    random_value_004.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Min
    random_value_004.inputs[2].default_value = 0.0
    # Max
    random_value_004.inputs[3].default_value = 1.0
    # Min
    random_value_004.inputs[4].default_value = 0
    # Max
    random_value_004.inputs[5].default_value = 100
    # Probability
    random_value_004.inputs[6].default_value = 0.5
    # ID
    random_value_004.inputs[7].default_value = 0
    # Links for random_value_004
    links.new(group_input_002.outputs[6], random_value_004.inputs[1])

    index_switch_013 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_013.name = "Index Switch.013"
    index_switch_013.label = ""
    index_switch_013.location = (95.5732421875, -483.0869140625)
    index_switch_013.bl_label = "Index Switch"
    index_switch_013.data_type = "VECTOR"
    # Links for index_switch_013
    links.new(random_value_004.outputs[0], index_switch_013.inputs[2])
    links.new(menu_switch_007.outputs[0], index_switch_013.inputs[0])

    random_value_006 = nodes.new("FunctionNodeRandomValue")
    random_value_006.name = "Random Value.006"
    random_value_006.label = ""
    random_value_006.location = (-101.00652313232422, -626.0848999023438)
    random_value_006.bl_label = "Random Value"
    random_value_006.data_type = "FLOAT"
    # Min
    random_value_006.inputs[0].default_value = [1.0, 1.0, 1.0]
    # Max
    random_value_006.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_006.inputs[2].default_value = 0.0
    # Min
    random_value_006.inputs[4].default_value = 0
    # Max
    random_value_006.inputs[5].default_value = 100
    # Probability
    random_value_006.inputs[6].default_value = 0.5
    # ID
    random_value_006.inputs[7].default_value = 0
    # Links for random_value_006
    links.new(random_value_006.outputs[1], index_switch_013.inputs[1])
    links.new(group_input_002.outputs[7], random_value_006.inputs[3])

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.label = ""
    vector_math_007.location = (391.00775146484375, -336.8423156738281)
    vector_math_007.bl_label = "Vector Math"
    vector_math_007.operation = "SUBTRACT"
    # Vector
    vector_math_007.inputs[0].default_value = [1.0, 1.0, 1.0]
    # Vector
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_007.inputs[3].default_value = 1.0
    # Links for vector_math_007
    links.new(index_switch_013.outputs[0], vector_math_007.inputs[1])

    hash_value_005 = nodes.new("FunctionNodeHashValue")
    hash_value_005.name = "Hash Value.005"
    hash_value_005.label = ""
    hash_value_005.location = (279.8762512207031, -927.60595703125)
    hash_value_005.bl_label = "Hash Value"
    hash_value_005.data_type = "INT"
    # Seed
    hash_value_005.inputs[1].default_value = 76881592
    # Links for hash_value_005
    links.new(hash_value_004.outputs[0], hash_value_005.inputs[0])
    links.new(hash_value_005.outputs[0], random_value_008.inputs[8])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (908.0314331054688, -383.67779541015625)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "MULTIPLY"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(vector_math_007.outputs[0], vector_math.inputs[0])
    links.new(vector_math_003.outputs[0], vector_math.inputs[1])
    links.new(vector_math.outputs[0], scale_instances.inputs[2])

    group_input_003 = nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.label = ""
    group_input_003.location = (94.17984008789062, -777.11328125)
    group_input_003.bl_label = "Group Input"
    # Links for group_input_003
    links.new(group_input_003.outputs[8], vector_math_001.inputs[1])
    links.new(group_input_003.outputs[8], vector_math_002.inputs[1])

    group_input_004 = nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.label = ""
    group_input_004.location = (-125.71966552734375, 76.91018676757812)
    group_input_004.bl_label = "Group Input"
    # Links for group_input_004

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (96.38915252685547, -39.84272384643555)
    position.bl_label = "Position"
    # Links for position

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (289.1990966796875, 5.122333526611328)
    switch.bl_label = "Switch"
    switch.input_type = "VECTOR"
    # True
    switch.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for switch
    links.new(position.outputs[0], switch.inputs[1])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (562.7689208984375, -44.361087799072266)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketVector"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], scale_instances.inputs[3])
    links.new(reroute_002.outputs[0], rotate_instances.inputs[3])
    links.new(switch.outputs[0], reroute_002.inputs[0])

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.label = ""
    reroute_003.location = (229.7098846435547, 49.052734375)
    reroute_003.bl_label = "Reroute"
    reroute_003.socket_idname = "NodeSocketBool"
    # Links for reroute_003
    links.new(reroute_003.outputs[0], rotate_instances.inputs[4])
    links.new(reroute_003.outputs[0], switch.inputs[0])
    links.new(group_input_004.outputs[2], reroute_003.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (1014.8703002929688, -7.643285274505615)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketBool"
    # Links for reroute_001
    links.new(reroute_001.outputs[0], translate_instances.inputs[3])
    links.new(reroute_001.outputs[0], scale_instances.inputs[4])
    links.new(reroute_003.outputs[0], reroute_001.inputs[0])

    reroute_004 = nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.label = ""
    reroute_004.location = (986.0343627929688, 40.63087463378906)
    reroute_004.bl_label = "Reroute"
    reroute_004.socket_idname = "NodeSocketBool"
    # Links for reroute_004
    links.new(reroute_004.outputs[0], scale_instances.inputs[1])
    links.new(reroute_004.outputs[0], translate_instances.inputs[1])
    links.new(reroute.outputs[0], reroute_004.inputs[0])

    reroute_005 = nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.label = ""
    reroute_005.location = (-166.58203125, -660.3865356445312)
    reroute_005.bl_label = "Reroute"
    reroute_005.socket_idname = "NodeSocketInt"
    # Links for reroute_005
    links.new(reroute_005.outputs[0], random_value_004.inputs[8])
    links.new(reroute_005.outputs[0], random_value_006.inputs[8])
    links.new(hash_value_004.outputs[0], reroute_005.inputs[0])

    hash_value_006 = nodes.new("FunctionNodeHashValue")
    hash_value_006.name = "Hash Value.006"
    hash_value_006.label = ""
    hash_value_006.location = (503.361083984375, -160.2587127685547)
    hash_value_006.bl_label = "Hash Value"
    hash_value_006.data_type = "INT"
    # Seed
    hash_value_006.inputs[1].default_value = 587641147
    # Links for hash_value_006
    links.new(hash_value_006.outputs[0], random_value_005.inputs[8])

    reroute_006 = nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.label = ""
    reroute_006.location = (-125.02754211425781, -221.0699462890625)
    reroute_006.bl_label = "Reroute"
    reroute_006.socket_idname = "NodeSocketInt"
    # Links for reroute_006
    links.new(reroute_006.outputs[0], hash_value_006.inputs[0])
    links.new(hash_value_004.outputs[0], reroute_006.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_array_group():
    group_name = "Array"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Shape", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "Line"
    socket = group.interface.new_socket(name="Count Method", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "Count"
    socket = group.interface.new_socket(name="Count", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 3
    socket.min_value = 1
    socket.max_value = 10000
    socket = group.interface.new_socket(name="Distance", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 1.0
    socket.min_value = 0.009999999776482582
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Angular Distance", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.7853981852531433
    socket.min_value = 0.01745329238474369
    socket.max_value = 6.2831854820251465
    socket = group.interface.new_socket(name="Per Curve", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = True
    socket = group.interface.new_socket(name="Offset Method", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "Relative"
    socket = group.interface.new_socket(name="Transform Reference", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "Inputs"
    socket = group.interface.new_socket(name="Translation", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [1.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Offset", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [1.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Rotation", in_out="INPUT", socket_type="NodeSocketRotation")
    socket.default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    socket = group.interface.new_socket(name="Scale", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [1.0, 1.0, 1.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Central Axis", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "Z"
    socket = group.interface.new_socket(name="Circle Segment", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "Full"
    socket = group.interface.new_socket(name="Sweep Angle", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 3.1415927410125732
    socket.min_value = 0.0
    socket.max_value = 6.2831854820251465
    socket = group.interface.new_socket(name="Radius", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    socket.min_value = 0.0
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Transform Object", in_out="INPUT", socket_type="NodeSocketObject")
    socket.default_value = None
    socket = group.interface.new_socket(name="Curve Object", in_out="INPUT", socket_type="NodeSocketObject")
    socket.default_value = None
    socket = group.interface.new_socket(name="Relative Space", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = True
    socket = group.interface.new_socket(name="Realize Instances", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = True
    socket = group.interface.new_socket(name="Align Rotation", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = True
    socket = group.interface.new_socket(name="Forward Axis", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "X"
    socket = group.interface.new_socket(name="Up Axis", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "Z"
    socket = group.interface.new_socket(name="Randomize", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False
    socket = group.interface.new_socket(name="Randomize Offset", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Randomize Rotation", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Randomize Scale Axes", in_out="INPUT", socket_type="NodeSocketMenu")
    socket.default_value = "Uniform"
    socket = group.interface.new_socket(name="Randomize Scale", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = 0.0
    socket.max_value = 1.0
    socket = group.interface.new_socket(name="Randomize Scale", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    socket.min_value = 0.0
    socket.max_value = 1.0
    socket = group.interface.new_socket(name="Randomize Flipping", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = 0.0
    socket.max_value = 1.0
    socket = group.interface.new_socket(name="Exclude First", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = True
    socket = group.interface.new_socket(name="Exclude Last", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False
    socket = group.interface.new_socket(name="Seed", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -10000
    socket.max_value = 10000
    socket = group.interface.new_socket(name="Merge", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False
    socket = group.interface.new_socket(name="Merge Distance", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0010000000474974513
    socket.min_value = 0.0
    socket.max_value = 3.4028234663852886e+38

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (4305.51513671875, -102.88172912597656)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1992.76708984375, 1426.221435546875)
    group_input.bl_label = "Group Input"
    # Links for group_input

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (1328.13818359375, -331.7998046875)
    instance_on_points.bl_label = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Links for instance_on_points

    menu_switch = nodes.new("GeometryNodeMenuSwitch")
    menu_switch.name = "Menu Switch"
    menu_switch.label = ""
    menu_switch.location = (-1812.76708984375, 1446.2215576171875)
    menu_switch.bl_label = "Menu Switch"
    menu_switch.active_index = 3
    menu_switch.data_type = "INT"
    # Line
    menu_switch.inputs[1].default_value = 0
    # Circle
    menu_switch.inputs[2].default_value = 1
    # Curve
    menu_switch.inputs[3].default_value = 2
    # Transform
    menu_switch.inputs[4].default_value = 3
    # Links for menu_switch
    links.new(group_input.outputs[1], menu_switch.inputs[0])

    linear_gizmo = nodes.new("GeometryNodeGizmoLinear")
    linear_gizmo.name = "Linear Gizmo"
    linear_gizmo.label = ""
    linear_gizmo.location = (1949.2880859375, -200.800048828125)
    linear_gizmo.bl_label = "Linear Gizmo"
    linear_gizmo.color_id = "PRIMARY"
    linear_gizmo.draw_style = "CROSS"
    # Links for linear_gizmo

    group_input_003 = nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.label = ""
    group_input_003.location = (189.28759765625, -240.7999267578125)
    group_input_003.bl_label = "Group Input"
    # Links for group_input_003

    group_input_004 = nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.label = ""
    group_input_004.location = (1829.353515625, -108.47506713867188)
    group_input_004.bl_label = "Group Input"
    # Links for group_input_004

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (-1541.0103759765625, 582.3410034179688)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(instance_on_points.outputs[0], join_geometry.inputs[0])

    group_input_005 = nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    group_input_005.label = ""
    group_input_005.location = (1135.771484375, -374.8709716796875)
    group_input_005.bl_label = "Group Input"
    # Links for group_input_005
    links.new(group_input_005.outputs[0], instance_on_points.inputs[2])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (1189.28759765625, -520.800048828125)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "SCALE"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_001

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (509.28759765625, -380.800048828125)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "SUBTRACT"
    # Value
    integer_math.inputs[1].default_value = 1
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(integer_math.outputs[0], vector_math_001.inputs[3])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (-5021.7060546875, 556.4208374023438)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(linear_gizmo.outputs[0], join_geometry_001.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (1569.28759765625, -120.7999267578125)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "LENGTH"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (1749.28759765625, -140.79998779296875)
    math.bl_label = "Math"
    math.operation = "MULTIPLY"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(math.outputs[0], linear_gizmo.inputs[0])
    links.new(vector_math_002.outputs[1], math.inputs[1])

    group_input_006 = nodes.new("NodeGroupInput")
    group_input_006.name = "Group Input.006"
    group_input_006.label = ""
    group_input_006.location = (29.2880859375, -980.7999267578125)
    group_input_006.bl_label = "Group Input"
    # Links for group_input_006

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (1069.287109375, -460.7999267578125)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketVector"
    # Links for reroute_001
    links.new(reroute_001.outputs[0], vector_math_001.inputs[0])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (1309.353271484375, -388.47503662109375)
    index.bl_label = "Index"
    # Links for index

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (1639.645263671875, -385.30572509765625)
    math_001.bl_label = "Math"
    math_001.operation = "DIVIDE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (1819.645263671875, -505.30572509765625)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002

    combine_x_y_z_002 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_002.name = "Combine XYZ.002"
    combine_x_y_z_002.label = ""
    combine_x_y_z_002.location = (2271.2333984375, -660.5481567382812)
    combine_x_y_z_002.bl_label = "Combine XYZ"
    # X
    combine_x_y_z_002.inputs[0].default_value = 0.0
    # Y
    combine_x_y_z_002.inputs[1].default_value = 0.0
    # Links for combine_x_y_z_002

    menu_switch_001 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_001.name = "Menu Switch.001"
    menu_switch_001.label = ""
    menu_switch_001.location = (2489.353515625, -288.47509765625)
    menu_switch_001.bl_label = "Menu Switch"
    menu_switch_001.active_index = 2
    menu_switch_001.data_type = "INT"
    # X
    menu_switch_001.inputs[1].default_value = 0
    # Y
    menu_switch_001.inputs[2].default_value = 1
    # Z
    menu_switch_001.inputs[3].default_value = 2
    # Links for menu_switch_001

    group_input_009 = nodes.new("NodeGroupInput")
    group_input_009.name = "Group Input.009"
    group_input_009.label = ""
    group_input_009.location = (2309.353515625, -308.47509765625)
    group_input_009.bl_label = "Group Input"
    # Links for group_input_009
    links.new(group_input_009.outputs[13], menu_switch_001.inputs[0])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (3280.726806640625, -256.74468994140625)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "ROTATION"
    # False
    switch_001.inputs[1].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for switch_001

    group_input_010 = nodes.new("NodeGroupInput")
    group_input_010.name = "Group Input.010"
    group_input_010.label = ""
    group_input_010.location = (3096.409912109375, -265.6080627441406)
    group_input_010.bl_label = "Group Input"
    # Links for group_input_010
    links.new(group_input_010.outputs[21], switch_001.inputs[0])

    index_switch_005 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_005.name = "Index Switch.005"
    index_switch_005.label = ""
    index_switch_005.location = (2669.353515625, -308.47509765625)
    index_switch_005.bl_label = "Index Switch"
    index_switch_005.data_type = "ROTATION"
    # 0
    index_switch_005.inputs[1].default_value = Euler((1.5707963705062866, 0.0, 1.5707963705062866), 'XYZ')
    # 1
    index_switch_005.inputs[2].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')
    # 2
    index_switch_005.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for index_switch_005
    links.new(menu_switch_001.outputs[0], index_switch_005.inputs[0])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (1054.6474609375, -179.83447265625)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002

    dial_gizmo = nodes.new("GeometryNodeGizmoDial")
    dial_gizmo.name = "Dial Gizmo"
    dial_gizmo.label = ""
    dial_gizmo.location = (229.48681640625, -195.97222900390625)
    dial_gizmo.bl_label = "Dial Gizmo"
    dial_gizmo.color_id = "SECONDARY"
    # Position
    dial_gizmo.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Up
    dial_gizmo.inputs[2].default_value = Vector((0.0, 0.0, 1.0))
    # Screen Space
    dial_gizmo.inputs[3].default_value = True
    # Radius
    dial_gizmo.inputs[4].default_value = 1.0
    # Links for dial_gizmo

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (3429.353515625, -748.4749755859375)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Matrix"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_001

    points = nodes.new("GeometryNodePoints")
    points.name = "Points"
    points.label = ""
    points.location = (495.592041015625, -65.1995849609375)
    points.bl_label = "Points"
    # Position
    points.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Radius
    points.inputs[2].default_value = 0.10000000149011612
    # Links for points

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (714.3642578125, -75.9864501953125)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position
    links.new(points.outputs[0], set_position.inputs[0])
    links.new(set_position.outputs[0], instance_on_points.inputs[0])

    group_input_014 = nodes.new("NodeGroupInput")
    group_input_014.name = "Group Input.014"
    group_input_014.label = ""
    group_input_014.location = (29.592529296875, -95.6815185546875)
    group_input_014.bl_label = "Group Input"
    # Links for group_input_014

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (2671.933837890625, -88.45763397216797)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001

    combine_x_y_z_003 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_003.name = "Combine XYZ.003"
    combine_x_y_z_003.label = ""
    combine_x_y_z_003.location = (2009.353515625, -108.47506713867188)
    combine_x_y_z_003.bl_label = "Combine XYZ"
    # X
    combine_x_y_z_003.inputs[0].default_value = 0.0
    # Z
    combine_x_y_z_003.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_003
    links.new(group_input_004.outputs[16], combine_x_y_z_003.inputs[1])

    rotate_vector = nodes.new("FunctionNodeRotateVector")
    rotate_vector.name = "Rotate Vector"
    rotate_vector.label = ""
    rotate_vector.location = (2489.353515625, -128.47508239746094)
    rotate_vector.bl_label = "Rotate Vector"
    # Links for rotate_vector
    links.new(combine_x_y_z_003.outputs[0], rotate_vector.inputs[0])
    links.new(rotate_vector.outputs[0], set_position_001.inputs[2])

    combine_x_y_z_004 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_004.name = "Combine XYZ.004"
    combine_x_y_z_004.label = ""
    combine_x_y_z_004.location = (2309.353515625, -188.47509765625)
    combine_x_y_z_004.bl_label = "Combine XYZ"
    # X
    combine_x_y_z_004.inputs[0].default_value = 0.0
    # Y
    combine_x_y_z_004.inputs[1].default_value = 0.0
    # Links for combine_x_y_z_004
    links.new(combine_x_y_z_004.outputs[0], rotate_vector.inputs[1])

    linear_gizmo_001 = nodes.new("GeometryNodeGizmoLinear")
    linear_gizmo_001.name = "Linear Gizmo.001"
    linear_gizmo_001.label = ""
    linear_gizmo_001.location = (789.4873046875, -235.97247314453125)
    linear_gizmo_001.bl_label = "Linear Gizmo"
    linear_gizmo_001.color_id = "PRIMARY"
    linear_gizmo_001.draw_style = "BOX"
    # Direction
    linear_gizmo_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Links for linear_gizmo_001
    links.new(linear_gizmo_001.outputs[0], join_geometry_002.inputs[0])

    group_input_015 = nodes.new("NodeGroupInput")
    group_input_015.name = "Group Input.015"
    group_input_015.label = ""
    group_input_015.location = (429.4873046875, -295.97235107421875)
    group_input_015.bl_label = "Group Input"
    # Links for group_input_015
    links.new(group_input_015.outputs[16], linear_gizmo_001.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (609.4873046875, -355.97222900390625)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "SCALE"
    # Vector
    vector_math.inputs[0].default_value = [0.0, 1.0, 0.0]
    # Vector
    vector_math.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math
    links.new(vector_math.outputs[0], linear_gizmo_001.inputs[1])
    links.new(group_input_015.outputs[16], vector_math.inputs[3])

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.label = ""
    switch_002.location = (1569.28759765625, -820.7999267578125)
    switch_002.bl_label = "Switch"
    switch_002.input_type = "GEOMETRY"
    # Links for switch_002
    links.new(switch_002.outputs[0], join_geometry_001.inputs[0])

    transform_gizmo_001 = nodes.new("GeometryNodeGizmoTransform")
    transform_gizmo_001.name = "Transform Gizmo.001"
    transform_gizmo_001.label = ""
    transform_gizmo_001.location = (1309.28759765625, -960.7999877929688)
    transform_gizmo_001.bl_label = "Transform Gizmo"
    transform_gizmo_001.use_translation_x = True
    transform_gizmo_001.use_translation_y = True
    transform_gizmo_001.use_translation_z = True
    transform_gizmo_001.use_rotation_x = True
    transform_gizmo_001.use_rotation_y = True
    transform_gizmo_001.use_rotation_z = True
    transform_gizmo_001.use_scale_x = True
    transform_gizmo_001.use_scale_y = True
    transform_gizmo_001.use_scale_z = True
    # Links for transform_gizmo_001
    links.new(transform_gizmo_001.outputs[0], switch_002.inputs[2])

    combine_transform_003 = nodes.new("FunctionNodeCombineTransform")
    combine_transform_003.name = "Combine Transform.003"
    combine_transform_003.label = ""
    combine_transform_003.location = (929.28759765625, -980.7999267578125)
    combine_transform_003.bl_label = "Combine Transform"
    # Links for combine_transform_003
    links.new(combine_transform_003.outputs[0], transform_gizmo_001.inputs[0])
    links.new(group_input_006.outputs[12], combine_transform_003.inputs[2])
    links.new(group_input_006.outputs[9], combine_transform_003.inputs[0])

    reroute_010 = nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    reroute_010.label = ""
    reroute_010.location = (2870.410400390625, -310.6069030761719)
    reroute_010.bl_label = "Reroute"
    reroute_010.socket_idname = "NodeSocketRotation"
    # Links for reroute_010
    links.new(index_switch_005.outputs[0], reroute_010.inputs[0])

    menu_switch_002 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_002.name = "Menu Switch.002"
    menu_switch_002.label = ""
    menu_switch_002.location = (-8170.66455078125, 1089.81591796875)
    menu_switch_002.bl_label = "Menu Switch"
    menu_switch_002.active_index = 0
    menu_switch_002.data_type = "INT"
    # Relative
    menu_switch_002.inputs[1].default_value = 0
    # Offset
    menu_switch_002.inputs[2].default_value = 1
    # Endpoint
    menu_switch_002.inputs[3].default_value = 2
    # Links for menu_switch_002

    index_switch_006 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_006.name = "Index Switch.006"
    index_switch_006.label = ""
    index_switch_006.location = (294.3642578125, -155.9864501953125)
    index_switch_006.bl_label = "Index Switch"
    index_switch_006.data_type = "VECTOR"
    # Links for index_switch_006

    index_switch_007 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_007.name = "Index Switch.007"
    index_switch_007.label = ""
    index_switch_007.location = (509.2724609375, -175.81060791015625)
    index_switch_007.bl_label = "Index Switch"
    index_switch_007.data_type = "ROTATION"
    # Links for index_switch_007

    reroute_008 = nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    reroute_008.label = ""
    reroute_008.location = (789.28759765625, -960.7999877929688)
    reroute_008.bl_label = "Reroute"
    reroute_008.socket_idname = "NodeSocketRotation"
    # Links for reroute_008
    links.new(reroute_008.outputs[0], combine_transform_003.inputs[1])
    links.new(group_input_006.outputs[11], reroute_008.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (889.287109375, -320.79998779296875)
    math_003.bl_label = "Math"
    math_003.operation = "DIVIDE"
    math_003.use_clamp = False
    # Value
    math_003.inputs[0].default_value = 1.0
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(integer_math.outputs[0], math_003.inputs[1])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.label = ""
    vector_math_008.location = (94.36376953125, -195.98663330078125)
    vector_math_008.bl_label = "Vector Math"
    vector_math_008.operation = "SCALE"
    # Vector
    vector_math_008.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_008
    links.new(vector_math_008.outputs[0], index_switch_006.inputs[3])

    reroute_011 = nodes.new("NodeReroute")
    reroute_011.name = "Reroute.011"
    reroute_011.label = ""
    reroute_011.location = (-7828.64013671875, 979.9938354492188)
    reroute_011.bl_label = "Reroute"
    reroute_011.socket_idname = "NodeSocketInt"
    # Links for reroute_011
    links.new(menu_switch_002.outputs[0], reroute_011.inputs[0])

    group_input_016 = nodes.new("NodeGroupInput")
    group_input_016.name = "Group Input.016"
    group_input_016.label = ""
    group_input_016.location = (-8370.6650390625, 1069.81591796875)
    group_input_016.bl_label = "Group Input"
    # Links for group_input_016
    links.new(group_input_016.outputs[7], menu_switch_002.inputs[0])

    index_switch_008 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_008.name = "Index Switch.008"
    index_switch_008.label = ""
    index_switch_008.location = (1429.287109375, -400.800048828125)
    index_switch_008.bl_label = "Index Switch"
    index_switch_008.data_type = "VECTOR"
    # Links for index_switch_008
    links.new(index_switch_008.outputs[0], linear_gizmo.inputs[1])
    links.new(reroute_001.outputs[0], index_switch_008.inputs[3])

    reroute_009 = nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    reroute_009.label = ""
    reroute_009.location = (1189.28759765625, -40.800048828125)
    reroute_009.bl_label = "Reroute"
    reroute_009.socket_idname = "NodeSocketInt"
    # Links for reroute_009
    links.new(reroute_009.outputs[0], index_switch_008.inputs[0])
    links.new(reroute_011.outputs[0], reroute_009.inputs[0])

    index_switch_010 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_010.name = "Index Switch.010"
    index_switch_010.label = ""
    index_switch_010.location = (1369.28759765625, -100.79998779296875)
    index_switch_010.bl_label = "Index Switch"
    index_switch_010.data_type = "VECTOR"
    # Links for index_switch_010
    links.new(index_switch_010.outputs[0], vector_math_002.inputs[0])
    links.new(reroute_009.outputs[0], index_switch_010.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (1169.28759765625, -220.79998779296875)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "SCALE"
    # Vector
    vector_math_003.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_003
    links.new(reroute_001.outputs[0], vector_math_003.inputs[0])
    links.new(math_003.outputs[0], vector_math_003.inputs[3])
    links.new(vector_math_003.outputs[0], index_switch_010.inputs[3])

    index_switch_009 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_009.name = "Index Switch.009"
    index_switch_009.label = ""
    index_switch_009.location = (-589.9928588867188, -190.98963928222656)
    index_switch_009.bl_label = "Index Switch"
    index_switch_009.data_type = "GEOMETRY"
    # Links for index_switch_009
    links.new(join_geometry.outputs[0], index_switch_009.inputs[1])
    links.new(menu_switch.outputs[0], index_switch_009.inputs[0])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.label = ""
    instance_on_points_001.location = (3474.302734375, -85.87173461914062)
    instance_on_points_001.bl_label = "Instance on Points"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Scale
    instance_on_points_001.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_001
    links.new(switch_001.outputs[0], instance_on_points_001.inputs[5])

    group_input_017 = nodes.new("NodeGroupInput")
    group_input_017.name = "Group Input.017"
    group_input_017.label = ""
    group_input_017.location = (3241.68505859375, -167.60052490234375)
    group_input_017.bl_label = "Group Input"
    # Links for group_input_017
    links.new(group_input_017.outputs[0], instance_on_points_001.inputs[2])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (-1072.75537109375, -270.18414306640625)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003
    links.new(instance_on_points_001.outputs[0], join_geometry_003.inputs[0])
    links.new(transform_geometry_001.outputs[0], join_geometry_003.inputs[0])
    links.new(join_geometry_003.outputs[0], index_switch_009.inputs[2])

    points_002 = nodes.new("GeometryNodePoints")
    points_002.name = "Points.002"
    points_002.label = ""
    points_002.location = (2490.489990234375, -75.7423095703125)
    points_002.bl_label = "Points"
    # Position
    points_002.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Radius
    points_002.inputs[2].default_value = 0.10000000149011612
    # Links for points_002
    links.new(points_002.outputs[0], set_position_001.inputs[0])

    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.label = ""
    index_001.location = (529.2724609375, -35.810546875)
    index_001.bl_label = "Index"
    # Links for index_001

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = "Circle Instances"
    frame_006.location = (-4842.10888671875, 98.29090881347656)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    frame_007 = nodes.new("NodeFrame")
    frame_007.name = "Frame.007"
    frame_007.label = "Line Instances"
    frame_007.location = (-3147.119384765625, 1184.0726318359375)
    frame_007.bl_label = "Frame"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20
    # Links for frame_007

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (34.363525390625, -193.23370361328125)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketInt"
    # Links for reroute_002
    links.new(reroute_009.outputs[0], reroute_002.inputs[0])

    index_switch_011 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_011.name = "Index Switch.011"
    index_switch_011.label = ""
    index_switch_011.location = (709.59228515625, -195.68154907226562)
    index_switch_011.bl_label = "Index Switch"
    index_switch_011.data_type = "VECTOR"
    # Links for index_switch_011

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.label = ""
    reroute_003.location = (34.364013671875, -594.2567749023438)
    reroute_003.bl_label = "Reroute"
    reroute_003.socket_idname = "NodeSocketFloat"
    # Links for reroute_003
    links.new(reroute_003.outputs[0], vector_math_008.inputs[3])
    links.new(math_003.outputs[0], reroute_003.inputs[0])

    reroute_007 = nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    reroute_007.label = ""
    reroute_007.location = (409.28759765625, -300.7999267578125)
    reroute_007.bl_label = "Reroute"
    reroute_007.socket_idname = "NodeSocketInt"
    # Links for reroute_007
    links.new(reroute_007.outputs[0], integer_math.inputs[0])
    links.new(reroute_007.outputs[0], math.inputs[0])
    links.new(group_input_003.outputs[3], reroute_007.inputs[0])

    index_002 = nodes.new("GeometryNodeInputIndex")
    index_002.name = "Index.002"
    index_002.label = ""
    index_002.location = (549.59228515625, -35.681427001953125)
    index_002.bl_label = "Index"
    # Links for index_002

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (729.592529296875, -35.681427001953125)
    math_004.bl_label = "Math"
    math_004.operation = "DIVIDE"
    math_004.use_clamp = False
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(index_002.outputs[0], math_004.inputs[0])

    integer_math_001 = nodes.new("FunctionNodeIntegerMath")
    integer_math_001.name = "Integer Math.001"
    integer_math_001.label = ""
    integer_math_001.location = (269.592529296875, -55.6815185546875)
    integer_math_001.bl_label = "Integer Math"
    integer_math_001.operation = "SUBTRACT"
    # Value
    integer_math_001.inputs[1].default_value = 1
    # Value
    integer_math_001.inputs[2].default_value = 0
    # Links for integer_math_001
    links.new(integer_math_001.outputs[0], math_004.inputs[1])
    links.new(group_input_014.outputs[3], integer_math_001.inputs[0])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (909.592529296875, -35.681427001953125)
    mix.bl_label = "Mix"
    mix.data_type = "VECTOR"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = False
    mix.clamp_result = False
    # Factor
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix.inputs[2].default_value = 0.0
    # B
    mix.inputs[3].default_value = 0.0
    # A
    mix.inputs[4].default_value = [1.0, 1.0, 1.0]
    # A
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix
    links.new(math_004.outputs[0], mix.inputs[0])
    links.new(mix.outputs[1], instance_on_points.inputs[6])
    links.new(index_switch_011.outputs[0], mix.inputs[5])

    reroute_005 = nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.label = ""
    reroute_005.location = (34.363525390625, -155.9864501953125)
    reroute_005.bl_label = "Reroute"
    reroute_005.socket_idname = "NodeSocketInt"
    # Links for reroute_005
    links.new(reroute_005.outputs[0], index_switch_006.inputs[0])
    links.new(reroute_002.outputs[0], reroute_005.inputs[0])

    reroute_012 = nodes.new("NodeReroute")
    reroute_012.name = "Reroute.012"
    reroute_012.label = ""
    reroute_012.location = (174.364013671875, -634.2567749023438)
    reroute_012.bl_label = "Reroute"
    reroute_012.socket_idname = "NodeSocketInt"
    # Links for reroute_012
    links.new(reroute_002.outputs[0], reroute_012.inputs[0])

    group_input_021 = nodes.new("NodeGroupInput")
    group_input_021.name = "Group Input.021"
    group_input_021.label = ""
    group_input_021.location = (909.6446533203125, -336.0386962890625)
    group_input_021.bl_label = "Group Input"
    # Links for group_input_021

    switch_003 = nodes.new("GeometryNodeSwitch")
    switch_003.name = "Switch.003"
    switch_003.label = ""
    switch_003.location = (1449.6446533203125, -36.03870391845703)
    switch_003.bl_label = "Switch"
    switch_003.input_type = "GEOMETRY"
    # Links for switch_003

    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.label = ""
    mix_001.location = (489.59228515625, -115.6815185546875)
    mix_001.bl_label = "Mix"
    mix_001.data_type = "VECTOR"
    mix_001.factor_mode = "UNIFORM"
    mix_001.blend_type = "MIX"
    mix_001.clamp_factor = False
    mix_001.clamp_result = False
    # Factor
    mix_001.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_001.inputs[2].default_value = 0.0
    # B
    mix_001.inputs[3].default_value = 0.0
    # A
    mix_001.inputs[4].default_value = [1.0, 1.0, 1.0]
    # A
    mix_001.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_001.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_001.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_001.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_001
    links.new(integer_math_001.outputs[0], mix_001.inputs[0])

    group_input_022 = nodes.new("NodeGroupInput")
    group_input_022.name = "Group Input.022"
    group_input_022.label = ""
    group_input_022.location = (1209.6446533203125, -36.03870391845703)
    group_input_022.bl_label = "Group Input"
    # Links for group_input_022
    links.new(group_input_022.outputs[24], switch_003.inputs[0])

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (-7452.75634765625, 189.8158416748047)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "MULTIPLY"
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006

    group_input_025 = nodes.new("NodeGroupInput")
    group_input_025.name = "Group Input.025"
    group_input_025.label = ""
    group_input_025.location = (-8292.755859375, 109.81584167480469)
    group_input_025.bl_label = "Group Input"
    # Links for group_input_025

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    bounding_box.label = ""
    bounding_box.location = (-7932.75634765625, 109.81584167480469)
    bounding_box.bl_label = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = True
    # Links for bounding_box

    vector_math_009 = nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.label = ""
    vector_math_009.location = (-7752.75634765625, 109.81584167480469)
    vector_math_009.bl_label = "Vector Math"
    vector_math_009.operation = "SUBTRACT"
    # Vector
    vector_math_009.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_009.inputs[3].default_value = 1.0
    # Links for vector_math_009
    links.new(bounding_box.outputs[2], vector_math_009.inputs[0])
    links.new(bounding_box.outputs[1], vector_math_009.inputs[1])
    links.new(vector_math_009.outputs[0], vector_math_006.inputs[1])

    reroute_014 = nodes.new("NodeReroute")
    reroute_014.name = "Reroute.014"
    reroute_014.label = ""
    reroute_014.location = (1169.28759765625, -920.7999267578125)
    reroute_014.bl_label = "Reroute"
    reroute_014.socket_idname = "NodeSocketVector"
    # Links for reroute_014
    links.new(reroute_014.outputs[0], transform_gizmo_001.inputs[1])

    reroute_015 = nodes.new("NodeReroute")
    reroute_015.name = "Reroute.015"
    reroute_015.label = ""
    reroute_015.location = (34.363525390625, -195.98663330078125)
    reroute_015.bl_label = "Reroute"
    reroute_015.socket_idname = "NodeSocketVector"
    # Links for reroute_015
    links.new(reroute_015.outputs[0], vector_math_008.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (629.28759765625, -740.7999267578125)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketVector"
    # Links for reroute
    links.new(reroute.outputs[0], reroute_001.inputs[0])
    links.new(reroute.outputs[0], reroute_014.inputs[0])

    reroute_016 = nodes.new("NodeReroute")
    reroute_016.name = "Reroute.016"
    reroute_016.label = ""
    reroute_016.location = (1329.28759765625, -220.79998779296875)
    reroute_016.bl_label = "Reroute"
    reroute_016.socket_idname = "NodeSocketVector"
    # Links for reroute_016
    links.new(reroute_016.outputs[0], index_switch_010.inputs[2])
    links.new(reroute_016.outputs[0], index_switch_010.inputs[1])
    links.new(reroute_001.outputs[0], reroute_016.inputs[0])

    reroute_017 = nodes.new("NodeReroute")
    reroute_017.name = "Reroute.017"
    reroute_017.label = ""
    reroute_017.location = (1409.287109375, -500.79998779296875)
    reroute_017.bl_label = "Reroute"
    reroute_017.socket_idname = "NodeSocketVector"
    # Links for reroute_017
    links.new(reroute_017.outputs[0], index_switch_008.inputs[2])
    links.new(reroute_017.outputs[0], index_switch_008.inputs[1])
    links.new(vector_math_001.outputs[0], reroute_017.inputs[0])

    reroute_018 = nodes.new("NodeReroute")
    reroute_018.name = "Reroute.018"
    reroute_018.label = ""
    reroute_018.location = (254.36376953125, -175.98638916015625)
    reroute_018.bl_label = "Reroute"
    reroute_018.socket_idname = "NodeSocketVector"
    # Links for reroute_018
    links.new(reroute_018.outputs[0], index_switch_006.inputs[2])
    links.new(reroute_018.outputs[0], index_switch_006.inputs[1])
    links.new(reroute_015.outputs[0], reroute_018.inputs[0])

    group_input_027 = nodes.new("NodeGroupInput")
    group_input_027.name = "Group Input.027"
    group_input_027.label = ""
    group_input_027.location = (-7632.75634765625, 209.8158416748047)
    group_input_027.bl_label = "Group Input"
    # Links for group_input_027
    links.new(group_input_027.outputs[10], vector_math_006.inputs[0])

    transform_gizmo_002 = nodes.new("GeometryNodeGizmoTransform")
    transform_gizmo_002.name = "Transform Gizmo.002"
    transform_gizmo_002.label = ""
    transform_gizmo_002.location = (1289.28759765625, -740.7999267578125)
    transform_gizmo_002.bl_label = "Transform Gizmo"
    transform_gizmo_002.use_translation_x = True
    transform_gizmo_002.use_translation_y = True
    transform_gizmo_002.use_translation_z = True
    transform_gizmo_002.use_rotation_x = True
    transform_gizmo_002.use_rotation_y = True
    transform_gizmo_002.use_rotation_z = True
    transform_gizmo_002.use_scale_x = True
    transform_gizmo_002.use_scale_y = True
    transform_gizmo_002.use_scale_z = True
    # Links for transform_gizmo_002
    links.new(reroute_014.outputs[0], transform_gizmo_002.inputs[1])
    links.new(transform_gizmo_002.outputs[0], switch_002.inputs[1])

    combine_transform_004 = nodes.new("FunctionNodeCombineTransform")
    combine_transform_004.name = "Combine Transform.004"
    combine_transform_004.label = ""
    combine_transform_004.location = (929.28759765625, -780.7999877929688)
    combine_transform_004.bl_label = "Combine Transform"
    # Links for combine_transform_004
    links.new(combine_transform_004.outputs[0], transform_gizmo_002.inputs[0])
    links.new(reroute_008.outputs[0], combine_transform_004.inputs[1])
    links.new(group_input_006.outputs[12], combine_transform_004.inputs[2])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (369.28759765625, -680.7999267578125)
    switch.bl_label = "Switch"
    switch.input_type = "VECTOR"
    # Links for switch
    links.new(switch.outputs[0], reroute.inputs[0])
    links.new(group_input_006.outputs[9], switch.inputs[2])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (89.2880859375, -560.7999267578125)
    compare.bl_label = "Compare"
    compare.operation = "NOT_EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    # A
    compare.inputs[0].default_value = 0.0
    # B
    compare.inputs[1].default_value = 0.0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
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
    links.new(reroute_011.outputs[0], compare.inputs[2])
    links.new(compare.outputs[0], switch.inputs[0])
    links.new(compare.outputs[0], switch_002.inputs[0])

    switch_004 = nodes.new("GeometryNodeSwitch")
    switch_004.name = "Switch.004"
    switch_004.label = ""
    switch_004.location = (409.64453125, -136.03866577148438)
    switch_004.bl_label = "Switch"
    switch_004.input_type = "BOOLEAN"
    # False
    switch_004.inputs[1].default_value = True
    # Links for switch_004

    index_003 = nodes.new("GeometryNodeInputIndex")
    index_003.name = "Index.003"
    index_003.label = ""
    index_003.location = (29.644775390625, -336.0386962890625)
    index_003.bl_label = "Index"
    # Links for index_003

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (209.644775390625, -256.0386657714844)
    compare_001.bl_label = "Compare"
    compare_001.operation = "NOT_EQUAL"
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
    links.new(index_003.outputs[0], compare_001.inputs[2])
    links.new(compare_001.outputs[0], switch_004.inputs[2])

    reroute_021 = nodes.new("NodeReroute")
    reroute_021.name = "Reroute.021"
    reroute_021.label = ""
    reroute_021.location = (669.5927734375, -195.68154907226562)
    reroute_021.bl_label = "Reroute"
    reroute_021.socket_idname = "NodeSocketVector"
    # Links for reroute_021
    links.new(reroute_021.outputs[0], index_switch_011.inputs[2])
    links.new(reroute_021.outputs[0], index_switch_011.inputs[1])
    links.new(mix_001.outputs[1], reroute_021.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (-1417.39501953125, -3029.669677734375)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(join_geometry_004.outputs[0], index_switch_009.inputs[4])

    instance_on_points_002 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.name = "Instance on Points.002"
    instance_on_points_002.label = ""
    instance_on_points_002.location = (869.560546875, -55.749755859375)
    instance_on_points_002.bl_label = "Instance on Points"
    # Selection
    instance_on_points_002.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_002.inputs[3].default_value = False
    # Instance Index
    instance_on_points_002.inputs[4].default_value = 0
    # Rotation
    instance_on_points_002.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_002.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_002

    set_instance_transform = nodes.new("GeometryNodeSetInstanceTransform")
    set_instance_transform.name = "Set Instance Transform"
    set_instance_transform.label = ""
    set_instance_transform.location = (1049.560546875, -135.75)
    set_instance_transform.bl_label = "Set Instance Transform"
    # Selection
    set_instance_transform.inputs[1].default_value = True
    # Links for set_instance_transform
    links.new(set_instance_transform.outputs[0], join_geometry_004.inputs[0])
    links.new(instance_on_points_002.outputs[0], set_instance_transform.inputs[0])

    points_003 = nodes.new("GeometryNodePoints")
    points_003.name = "Points.003"
    points_003.label = ""
    points_003.location = (669.56005859375, -35.749267578125)
    points_003.bl_label = "Points"
    # Position
    points_003.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Radius
    points_003.inputs[2].default_value = 0.10000000149011612
    # Links for points_003
    links.new(points_003.outputs[0], instance_on_points_002.inputs[0])

    group_input_026 = nodes.new("NodeGroupInput")
    group_input_026.name = "Group Input.026"
    group_input_026.label = ""
    group_input_026.location = (489.56005859375, -35.749267578125)
    group_input_026.bl_label = "Group Input"
    # Links for group_input_026
    links.new(group_input_026.outputs[3], points_003.inputs[0])

    group_input_028 = nodes.new("NodeGroupInput")
    group_input_028.name = "Group Input.028"
    group_input_028.label = ""
    group_input_028.location = (669.56005859375, -135.75)
    group_input_028.bl_label = "Group Input"
    # Links for group_input_028
    links.new(group_input_028.outputs[0], instance_on_points_002.inputs[2])

    accumulate_field = nodes.new("GeometryNodeAccumulateField")
    accumulate_field.name = "Accumulate Field"
    accumulate_field.label = ""
    accumulate_field.location = (849.56005859375, -235.749755859375)
    accumulate_field.bl_label = "Accumulate Field"
    accumulate_field.data_type = "TRANSFORM"
    accumulate_field.domain = "INSTANCE"
    # Group ID
    accumulate_field.inputs[1].default_value = 0
    # Links for accumulate_field
    links.new(accumulate_field.outputs[1], set_instance_transform.inputs[2])

    group_input_029 = nodes.new("NodeGroupInput")
    group_input_029.name = "Group Input.029"
    group_input_029.label = ""
    group_input_029.location = (230.154296875, -419.82080078125)
    group_input_029.bl_label = "Group Input"
    # Links for group_input_029

    combine_transform = nodes.new("FunctionNodeCombineTransform")
    combine_transform.name = "Combine Transform"
    combine_transform.label = ""
    combine_transform.location = (449.560546875, -375.749267578125)
    combine_transform.bl_label = "Combine Transform"
    # Links for combine_transform
    links.new(group_input_029.outputs[9], combine_transform.inputs[0])
    links.new(group_input_029.outputs[11], combine_transform.inputs[1])
    links.new(group_input_029.outputs[12], combine_transform.inputs[2])

    transform_gizmo_003 = nodes.new("GeometryNodeGizmoTransform")
    transform_gizmo_003.name = "Transform Gizmo.003"
    transform_gizmo_003.label = ""
    transform_gizmo_003.location = (669.56005859375, -515.75)
    transform_gizmo_003.bl_label = "Transform Gizmo"
    transform_gizmo_003.use_translation_x = True
    transform_gizmo_003.use_translation_y = True
    transform_gizmo_003.use_translation_z = True
    transform_gizmo_003.use_rotation_x = True
    transform_gizmo_003.use_rotation_y = True
    transform_gizmo_003.use_rotation_z = True
    transform_gizmo_003.use_scale_x = True
    transform_gizmo_003.use_scale_y = True
    transform_gizmo_003.use_scale_z = True
    # Links for transform_gizmo_003
    links.new(combine_transform.outputs[0], transform_gizmo_003.inputs[0])
    links.new(group_input_029.outputs[9], transform_gizmo_003.inputs[1])
    links.new(group_input_029.outputs[11], transform_gizmo_003.inputs[2])

    object_info = nodes.new("GeometryNodeObjectInfo")
    object_info.name = "Object Info"
    object_info.label = ""
    object_info.location = (249.560546875, -795.750244140625)
    object_info.bl_label = "Object Info"
    object_info.transform_space = "RELATIVE"
    # As Instance
    object_info.inputs[1].default_value = False
    # Links for object_info

    group_input_002 = nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.label = ""
    group_input_002.location = (29.56005859375, -795.750244140625)
    group_input_002.bl_label = "Group Input"
    # Links for group_input_002
    links.new(group_input_002.outputs[17], object_info.inputs[0])

    switch_005 = nodes.new("GeometryNodeSwitch")
    switch_005.name = "Switch.005"
    switch_005.label = ""
    switch_005.location = (449.560546875, -615.750244140625)
    switch_005.bl_label = "Switch"
    switch_005.input_type = "MATRIX"
    # Links for switch_005
    links.new(object_info.outputs[0], switch_005.inputs[2])

    object_info_001 = nodes.new("GeometryNodeObjectInfo")
    object_info_001.name = "Object Info.001"
    object_info_001.label = ""
    object_info_001.location = (249.560546875, -675.75)
    object_info_001.bl_label = "Object Info"
    object_info_001.transform_space = "ORIGINAL"
    # As Instance
    object_info_001.inputs[1].default_value = False
    # Links for object_info_001
    links.new(group_input_002.outputs[17], object_info_001.inputs[0])
    links.new(object_info_001.outputs[0], switch_005.inputs[1])

    frame_010 = nodes.new("NodeFrame")
    frame_010.name = "Frame.010"
    frame_010.label = "Transform Instances"
    frame_010.location = (-4342.9091796875, -2650.363525390625)
    frame_010.bl_label = "Frame"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20
    # Links for frame_010

    reroute_022 = nodes.new("NodeReroute")
    reroute_022.name = "Reroute.022"
    reroute_022.label = ""
    reroute_022.location = (54.364501953125, -994.2567749023438)
    reroute_022.bl_label = "Reroute"
    reroute_022.socket_idname = "NodeSocketGeometry"
    # Links for reroute_022
    links.new(join_geometry_001.outputs[0], reroute_022.inputs[0])

    reroute_023 = nodes.new("NodeReroute")
    reroute_023.name = "Reroute.023"
    reroute_023.label = ""
    reroute_023.location = (1414.3641357421875, -994.2567749023438)
    reroute_023.bl_label = "Reroute"
    reroute_023.socket_idname = "NodeSocketGeometry"
    # Links for reroute_023
    links.new(reroute_023.outputs[0], join_geometry.inputs[0])
    links.new(reroute_022.outputs[0], reroute_023.inputs[0])

    reroute_024 = nodes.new("NodeReroute")
    reroute_024.name = "Reroute.024"
    reroute_024.label = ""
    reroute_024.location = (102.44140625, -845.3056030273438)
    reroute_024.bl_label = "Reroute"
    reroute_024.socket_idname = "NodeSocketGeometry"
    # Links for reroute_024
    links.new(join_geometry_002.outputs[0], reroute_024.inputs[0])

    reroute_025 = nodes.new("NodeReroute")
    reroute_025.name = "Reroute.025"
    reroute_025.label = ""
    reroute_025.location = (3151.15673828125, -843.53369140625)
    reroute_025.bl_label = "Reroute"
    reroute_025.socket_idname = "NodeSocketGeometry"
    # Links for reroute_025
    links.new(reroute_024.outputs[0], reroute_025.inputs[0])
    links.new(reroute_025.outputs[0], transform_geometry_001.inputs[0])

    menu_switch_003 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_003.name = "Menu Switch.003"
    menu_switch_003.label = ""
    menu_switch_003.location = (450.153564453125, -219.821044921875)
    menu_switch_003.bl_label = "Menu Switch"
    menu_switch_003.active_index = 1
    menu_switch_003.data_type = "INT"
    # Inputs
    menu_switch_003.inputs[1].default_value = 0
    # Object
    menu_switch_003.inputs[2].default_value = 1
    # Links for menu_switch_003

    index_switch = nodes.new("GeometryNodeIndexSwitch")
    index_switch.name = "Index Switch"
    index_switch.label = ""
    index_switch.location = (669.56005859375, -295.75)
    index_switch.bl_label = "Index Switch"
    index_switch.data_type = "MATRIX"
    # Links for index_switch
    links.new(switch_005.outputs[0], index_switch.inputs[2])
    links.new(combine_transform.outputs[0], index_switch.inputs[1])
    links.new(index_switch.outputs[0], accumulate_field.inputs[0])

    index_switch_001 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_001.name = "Index Switch.001"
    index_switch_001.label = ""
    index_switch_001.location = (849.56005859375, -475.75)
    index_switch_001.bl_label = "Index Switch"
    index_switch_001.data_type = "GEOMETRY"
    # Links for index_switch_001
    links.new(transform_gizmo_003.outputs[0], index_switch_001.inputs[1])

    group_input_032 = nodes.new("NodeGroupInput")
    group_input_032.name = "Group Input.032"
    group_input_032.label = ""
    group_input_032.location = (249.560546875, -215.749267578125)
    group_input_032.bl_label = "Group Input"
    # Links for group_input_032
    links.new(group_input_032.outputs[8], menu_switch_003.inputs[0])

    group_input_033 = nodes.new("NodeGroupInput")
    group_input_033.name = "Group Input.033"
    group_input_033.label = ""
    group_input_033.location = (249.560546875, -615.750244140625)
    group_input_033.bl_label = "Group Input"
    # Links for group_input_033
    links.new(group_input_033.outputs[19], switch_005.inputs[0])

    reroute_026 = nodes.new("NodeReroute")
    reroute_026.name = "Reroute.026"
    reroute_026.label = ""
    reroute_026.location = (629.560546875, -295.75)
    reroute_026.bl_label = "Reroute"
    reroute_026.socket_idname = "NodeSocketInt"
    # Links for reroute_026
    links.new(reroute_026.outputs[0], index_switch.inputs[0])
    links.new(reroute_026.outputs[0], index_switch_001.inputs[0])
    links.new(menu_switch_003.outputs[0], reroute_026.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (2649.56005859375, -515.75)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(join_geometry_005.outputs[0], join_geometry_004.inputs[0])
    links.new(index_switch_001.outputs[0], join_geometry_005.inputs[0])

    group_input_034 = nodes.new("NodeGroupInput")
    group_input_034.name = "Group Input.034"
    group_input_034.label = ""
    group_input_034.location = (989.560546875, -695.74951171875)
    group_input_034.bl_label = "Group Input"
    # Links for group_input_034

    linear_gizmo_002 = nodes.new("GeometryNodeGizmoLinear")
    linear_gizmo_002.name = "Linear Gizmo.002"
    linear_gizmo_002.label = ""
    linear_gizmo_002.location = (2489.56005859375, -615.750244140625)
    linear_gizmo_002.bl_label = "Linear Gizmo"
    linear_gizmo_002.color_id = "PRIMARY"
    linear_gizmo_002.draw_style = "CROSS"
    # Links for linear_gizmo_002
    links.new(linear_gizmo_002.outputs[0], join_geometry_005.inputs[0])

    instance_transform = nodes.new("GeometryNodeInstanceTransform")
    instance_transform.name = "Instance Transform"
    instance_transform.label = ""
    instance_transform.location = (1189.559814453125, -775.749267578125)
    instance_transform.bl_label = "Instance Transform"
    # Links for instance_transform

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (1369.559814453125, -735.749755859375)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT4X4"
    sample_index.domain = "INSTANCE"
    sample_index.clamp = False
    # Links for sample_index
    links.new(set_instance_transform.outputs[0], sample_index.inputs[0])
    links.new(instance_transform.outputs[0], sample_index.inputs[1])

    integer_math_002 = nodes.new("FunctionNodeIntegerMath")
    integer_math_002.name = "Integer Math.002"
    integer_math_002.label = ""
    integer_math_002.location = (1189.559814453125, -835.75)
    integer_math_002.bl_label = "Integer Math"
    integer_math_002.operation = "SUBTRACT"
    # Value
    integer_math_002.inputs[1].default_value = 1
    # Value
    integer_math_002.inputs[2].default_value = 0
    # Links for integer_math_002
    links.new(group_input_034.outputs[3], integer_math_002.inputs[0])
    links.new(integer_math_002.outputs[0], sample_index.inputs[2])

    separate_transform_001 = nodes.new("FunctionNodeSeparateTransform")
    separate_transform_001.name = "Separate Transform.001"
    separate_transform_001.label = ""
    separate_transform_001.location = (1549.559814453125, -735.749755859375)
    separate_transform_001.bl_label = "Separate Transform"
    # Links for separate_transform_001
    links.new(sample_index.outputs[0], separate_transform_001.inputs[0])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (2280.40380859375, -634.5087890625)
    math_005.bl_label = "Math"
    math_005.operation = "MULTIPLY"
    math_005.use_clamp = False
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(group_input_034.outputs[3], math_005.inputs[0])
    links.new(math_005.outputs[0], linear_gizmo_002.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (2109.416259765625, -772.04638671875)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "LENGTH"
    # Vector
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_005.inputs[3].default_value = 1.0
    # Links for vector_math_005
    links.new(vector_math_005.outputs[1], math_005.inputs[1])

    separate_transform_002 = nodes.new("FunctionNodeSeparateTransform")
    separate_transform_002.name = "Separate Transform.002"
    separate_transform_002.label = ""
    separate_transform_002.location = (850.154296875, -359.820556640625)
    separate_transform_002.bl_label = "Separate Transform"
    # Links for separate_transform_002
    links.new(index_switch.outputs[0], separate_transform_002.inputs[0])

    transform_point = nodes.new("FunctionNodeTransformPoint")
    transform_point.name = "Transform Point"
    transform_point.label = ""
    transform_point.location = (1929.56005859375, -775.749267578125)
    transform_point.bl_label = "Transform Point"
    # Links for transform_point
    links.new(separate_transform_002.outputs[0], transform_point.inputs[0])
    links.new(transform_point.outputs[0], vector_math_005.inputs[0])

    combine_transform_001 = nodes.new("FunctionNodeCombineTransform")
    combine_transform_001.name = "Combine Transform.001"
    combine_transform_001.label = ""
    combine_transform_001.location = (1749.559814453125, -775.749267578125)
    combine_transform_001.bl_label = "Combine Transform"
    # Translation
    combine_transform_001.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    # Links for combine_transform_001
    links.new(separate_transform_001.outputs[1], combine_transform_001.inputs[1])
    links.new(separate_transform_001.outputs[2], combine_transform_001.inputs[2])
    links.new(combine_transform_001.outputs[0], transform_point.inputs[1])

    reroute_027 = nodes.new("NodeReroute")
    reroute_027.name = "Reroute.027"
    reroute_027.label = ""
    reroute_027.location = (2449.56005859375, -755.749267578125)
    reroute_027.bl_label = "Reroute"
    reroute_027.socket_idname = "NodeSocketVectorTranslation"
    # Links for reroute_027
    links.new(reroute_027.outputs[0], linear_gizmo_002.inputs[1])
    links.new(reroute_027.outputs[0], linear_gizmo_002.inputs[2])
    links.new(separate_transform_001.outputs[0], reroute_027.inputs[0])

    object_info_003 = nodes.new("GeometryNodeObjectInfo")
    object_info_003.name = "Object Info.003"
    object_info_003.label = ""
    object_info_003.location = (229.36083984375, -457.500244140625)
    object_info_003.bl_label = "Object Info"
    object_info_003.transform_space = "RELATIVE"
    # As Instance
    object_info_003.inputs[1].default_value = False
    # Links for object_info_003

    object_info_004 = nodes.new("GeometryNodeObjectInfo")
    object_info_004.name = "Object Info.004"
    object_info_004.label = ""
    object_info_004.location = (229.36083984375, -337.50048828125)
    object_info_004.bl_label = "Object Info"
    object_info_004.transform_space = "ORIGINAL"
    # As Instance
    object_info_004.inputs[1].default_value = False
    # Links for object_info_004

    group_input_036 = nodes.new("NodeGroupInput")
    group_input_036.name = "Group Input.036"
    group_input_036.label = ""
    group_input_036.location = (229.36083984375, -277.500244140625)
    group_input_036.bl_label = "Group Input"
    # Links for group_input_036

    group_input_035 = nodes.new("NodeGroupInput")
    group_input_035.name = "Group Input.035"
    group_input_035.label = ""
    group_input_035.location = (29.36083984375, -457.500244140625)
    group_input_035.bl_label = "Group Input"
    # Links for group_input_035
    links.new(group_input_035.outputs[18], object_info_003.inputs[0])
    links.new(group_input_035.outputs[18], object_info_004.inputs[0])

    switch_006 = nodes.new("GeometryNodeSwitch")
    switch_006.name = "Switch.006"
    switch_006.label = ""
    switch_006.location = (429.361328125, -317.5003662109375)
    switch_006.bl_label = "Switch"
    switch_006.input_type = "GEOMETRY"
    # Links for switch_006
    links.new(object_info_004.outputs[4], switch_006.inputs[1])
    links.new(object_info_003.outputs[4], switch_006.inputs[2])
    links.new(group_input_036.outputs[19], switch_006.inputs[0])

    group_input_039 = nodes.new("NodeGroupInput")
    group_input_039.name = "Group Input.039"
    group_input_039.label = ""
    group_input_039.location = (1638.698486328125, -625.3056030273438)
    group_input_039.bl_label = "Group Input"
    # Links for group_input_039
    links.new(group_input_039.outputs[15], math_002.inputs[1])

    group_input_040 = nodes.new("NodeGroupInput")
    group_input_040.name = "Group Input.040"
    group_input_040.label = ""
    group_input_040.location = (29.48779296875, -235.97247314453125)
    group_input_040.bl_label = "Group Input"
    # Links for group_input_040
    links.new(group_input_040.outputs[15], dial_gizmo.inputs[0])

    group_input_041 = nodes.new("NodeGroupInput")
    group_input_041.name = "Group Input.041"
    group_input_041.label = ""
    group_input_041.location = (429.4873046875, -575.9722900390625)
    group_input_041.bl_label = "Group Input"
    # Links for group_input_041

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (-8112.75634765625, 109.81584167480469)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(realize_instances.outputs[0], bounding_box.inputs[0])
    links.new(group_input_025.outputs[0], realize_instances.inputs[0])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (1639.645263671875, -505.30572509765625)
    math_006.bl_label = "Math"
    math_006.operation = "DIVIDE"
    math_006.use_clamp = False
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(math_006.outputs[0], math_002.inputs[0])

    integer_math_003 = nodes.new("FunctionNodeIntegerMath")
    integer_math_003.name = "Integer Math.003"
    integer_math_003.label = ""
    integer_math_003.location = (1459.646240234375, -505.30572509765625)
    integer_math_003.bl_label = "Integer Math"
    integer_math_003.operation = "SUBTRACT"
    # Value
    integer_math_003.inputs[1].default_value = 1
    # Value
    integer_math_003.inputs[2].default_value = 0
    # Links for integer_math_003
    links.new(integer_math_003.outputs[0], math_006.inputs[1])

    reroute_028 = nodes.new("NodeReroute")
    reroute_028.name = "Reroute.028"
    reroute_028.label = ""
    reroute_028.location = (1558.697998046875, -445.30560302734375)
    reroute_028.bl_label = "Reroute"
    reroute_028.socket_idname = "NodeSocketInt"
    # Links for reroute_028
    links.new(reroute_028.outputs[0], math_001.inputs[0])
    links.new(reroute_028.outputs[0], math_006.inputs[0])
    links.new(index.outputs[0], reroute_028.inputs[0])

    reroute_029 = nodes.new("NodeReroute")
    reroute_029.name = "Reroute.029"
    reroute_029.label = ""
    reroute_029.location = (1419.64599609375, -485.3056640625)
    reroute_029.bl_label = "Reroute"
    reroute_029.socket_idname = "NodeSocketInt"
    # Links for reroute_029
    links.new(reroute_029.outputs[0], math_001.inputs[1])
    links.new(reroute_029.outputs[0], integer_math_003.inputs[0])

    group_input_042 = nodes.new("NodeGroupInput")
    group_input_042.name = "Group Input.042"
    group_input_042.label = ""
    group_input_042.location = (29.35400390625, -68.47505187988281)
    group_input_042.bl_label = "Group Input"
    # Links for group_input_042

    reroute_030 = nodes.new("NodeReroute")
    reroute_030.name = "Reroute.030"
    reroute_030.label = ""
    reroute_030.location = (2219.6455078125, -465.3056640625)
    reroute_030.bl_label = "Reroute"
    reroute_030.socket_idname = "NodeSocketFloat"
    # Links for reroute_030
    links.new(reroute_030.outputs[0], combine_x_y_z_002.inputs[2])
    links.new(reroute_030.outputs[0], combine_x_y_z_004.inputs[2])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.label = ""
    math_007.location = (1819.645263671875, -385.30572509765625)
    math_007.bl_label = "Math"
    math_007.operation = "MULTIPLY"
    math_007.use_clamp = False
    # Value
    math_007.inputs[1].default_value = 6.2831854820251465
    # Value
    math_007.inputs[2].default_value = 0.5
    # Links for math_007
    links.new(math_001.outputs[0], math_007.inputs[0])

    group_input_043 = nodes.new("NodeGroupInput")
    group_input_043.name = "Group Input.043"
    group_input_043.label = ""
    group_input_043.location = (-7684.82958984375, -522.7241821289062)
    group_input_043.bl_label = "Group Input"
    # Links for group_input_043

    menu_switch_006 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_006.name = "Menu Switch.006"
    menu_switch_006.label = ""
    menu_switch_006.location = (-7504.82958984375, -502.7243957519531)
    menu_switch_006.bl_label = "Menu Switch"
    menu_switch_006.active_index = 1
    menu_switch_006.data_type = "INT"
    # Full
    menu_switch_006.inputs[1].default_value = 0
    # Arc
    menu_switch_006.inputs[2].default_value = 1
    # Links for menu_switch_006
    links.new(group_input_043.outputs[14], menu_switch_006.inputs[0])

    index_switch_002 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_002.name = "Index Switch.002"
    index_switch_002.label = ""
    index_switch_002.location = (2039.6455078125, -405.30560302734375)
    index_switch_002.bl_label = "Index Switch"
    index_switch_002.data_type = "FLOAT"
    # Links for index_switch_002
    links.new(index_switch_002.outputs[0], reroute_030.inputs[0])
    links.new(math_007.outputs[0], index_switch_002.inputs[1])
    links.new(math_002.outputs[0], index_switch_002.inputs[2])

    reroute_031 = nodes.new("NodeReroute")
    reroute_031.name = "Reroute.031"
    reroute_031.label = ""
    reroute_031.location = (50.162109375, -345.3056640625)
    reroute_031.bl_label = "Reroute"
    reroute_031.socket_idname = "NodeSocketInt"
    # Links for reroute_031
    links.new(menu_switch_006.outputs[0], reroute_031.inputs[0])

    reroute_032 = nodes.new("NodeReroute")
    reroute_032.name = "Reroute.032"
    reroute_032.label = ""
    reroute_032.location = (1958.69873046875, -345.3056640625)
    reroute_032.bl_label = "Reroute"
    reroute_032.socket_idname = "NodeSocketInt"
    # Links for reroute_032
    links.new(reroute_032.outputs[0], index_switch_002.inputs[0])

    switch_007 = nodes.new("GeometryNodeSwitch")
    switch_007.name = "Switch.007"
    switch_007.label = ""
    switch_007.location = (469.48779296875, -35.97222900390625)
    switch_007.bl_label = "Switch"
    switch_007.input_type = "GEOMETRY"
    # Links for switch_007
    links.new(switch_007.outputs[0], join_geometry_002.inputs[0])
    links.new(dial_gizmo.outputs[0], switch_007.inputs[2])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.label = ""
    compare_002.location = (229.48681640625, -35.97222900390625)
    compare_002.bl_label = "Compare"
    compare_002.operation = "EQUAL"
    compare_002.data_type = "INT"
    compare_002.mode = "ELEMENT"
    # A
    compare_002.inputs[0].default_value = 0.0
    # B
    compare_002.inputs[1].default_value = 0.0
    # B
    compare_002.inputs[3].default_value = 1
    # A
    compare_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_002.inputs[8].default_value = ""
    # B
    compare_002.inputs[9].default_value = ""
    # C
    compare_002.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_002.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_002.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_002
    links.new(menu_switch_006.outputs[0], compare_002.inputs[2])
    links.new(compare_002.outputs[0], switch_007.inputs[0])

    linear_gizmo_003 = nodes.new("GeometryNodeGizmoLinear")
    linear_gizmo_003.name = "Linear Gizmo.003"
    linear_gizmo_003.label = ""
    linear_gizmo_003.location = (613.0185546875, -576.5751953125)
    linear_gizmo_003.bl_label = "Linear Gizmo"
    linear_gizmo_003.color_id = "PRIMARY"
    linear_gizmo_003.draw_style = "CROSS"
    # Position
    linear_gizmo_003.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Direction
    linear_gizmo_003.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Links for linear_gizmo_003
    links.new(group_input_041.outputs[3], linear_gizmo_003.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "Circle Gizmos"
    frame_001.location = (-7284.87255859375, -615.5999755859375)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    switch_008 = nodes.new("GeometryNodeSwitch")
    switch_008.name = "Switch.008"
    switch_008.label = ""
    switch_008.location = (671.03662109375, -135.67507934570312)
    switch_008.bl_label = "Switch"
    switch_008.input_type = "GEOMETRY"
    # Links for switch_008

    reroute_033 = nodes.new("NodeReroute")
    reroute_033.name = "Reroute.033"
    reroute_033.label = ""
    reroute_033.location = (34.363525390625, -116.88704681396484)
    reroute_033.bl_label = "Reroute"
    reroute_033.socket_idname = "NodeSocketGeometry"
    # Links for reroute_033
    links.new(switch_003.outputs[0], reroute_033.inputs[0])

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.label = ""
    merge_by_distance.location = (471.03662109375, -315.675048828125)
    merge_by_distance.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance.inputs[1].default_value = True
    # Mode
    merge_by_distance.inputs[2].default_value = "All"
    # Links for merge_by_distance
    links.new(merge_by_distance.outputs[0], switch_008.inputs[2])

    vector_math_015 = nodes.new("ShaderNodeVectorMath")
    vector_math_015.name = "Vector Math.015"
    vector_math_015.label = ""
    vector_math_015.location = (494.36376953125, -135.98663330078125)
    vector_math_015.bl_label = "Vector Math"
    vector_math_015.operation = "SCALE"
    # Vector
    vector_math_015.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_015.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_015
    links.new(index_switch_006.outputs[0], vector_math_015.inputs[0])
    links.new(vector_math_015.outputs[0], set_position.inputs[2])

    index_004 = nodes.new("GeometryNodeInputIndex")
    index_004.name = "Index.004"
    index_004.label = ""
    index_004.location = (294.3642578125, -215.986572265625)
    index_004.bl_label = "Index"
    # Links for index_004
    links.new(index_004.outputs[0], vector_math_015.inputs[3])

    group_input_045 = nodes.new("NodeGroupInput")
    group_input_045.name = "Group Input.045"
    group_input_045.label = ""
    group_input_045.location = (191.036376953125, -195.675048828125)
    group_input_045.bl_label = "Group Input"
    # Links for group_input_045
    links.new(group_input_045.outputs[35], merge_by_distance.inputs[3])
    links.new(group_input_045.outputs[34], switch_008.inputs[0])

    spline_length = nodes.new("GeometryNodeSplineLength")
    spline_length.name = "Spline Length"
    spline_length.label = ""
    spline_length.location = (59.95361328125, -294.50537109375)
    spline_length.bl_label = "Spline Length"
    # Links for spline_length

    math_008 = nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.label = ""
    math_008.location = (279.953125, -294.50537109375)
    math_008.bl_label = "Math"
    math_008.operation = "DIVIDE"
    math_008.use_clamp = False
    # Value
    math_008.inputs[2].default_value = 0.5
    # Links for math_008
    links.new(spline_length.outputs[0], math_008.inputs[0])

    reroute_034 = nodes.new("NodeReroute")
    reroute_034.name = "Reroute.034"
    reroute_034.label = ""
    reroute_034.location = (219.95361328125, -434.505615234375)
    reroute_034.bl_label = "Reroute"
    reroute_034.socket_idname = "NodeSocketFloatDistance"
    # Links for reroute_034
    links.new(reroute_034.outputs[0], math_008.inputs[1])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (899.953369140625, -214.505615234375)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 1
    capture_attribute_001.domain = "CURVE"
    # Links for capture_attribute_001

    group_input_037 = nodes.new("NodeGroupInput")
    group_input_037.name = "Group Input.037"
    group_input_037.label = ""
    group_input_037.location = (51.16162109375, -35.69580078125)
    group_input_037.bl_label = "Group Input"
    # Links for group_input_037

    instance_on_points_004 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_004.name = "Instance on Points.004"
    instance_on_points_004.label = ""
    instance_on_points_004.location = (3284.55322265625, -166.92138671875)
    instance_on_points_004.bl_label = "Instance on Points"
    # Selection
    instance_on_points_004.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_004.inputs[3].default_value = False
    # Instance Index
    instance_on_points_004.inputs[4].default_value = 0
    # Scale
    instance_on_points_004.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_004

    group_input_047 = nodes.new("NodeGroupInput")
    group_input_047.name = "Group Input.047"
    group_input_047.label = ""
    group_input_047.location = (3083.17529296875, -276.582763671875)
    group_input_047.bl_label = "Group Input"
    # Links for group_input_047
    links.new(group_input_047.outputs[0], instance_on_points_004.inputs[2])

    switch_011 = nodes.new("GeometryNodeSwitch")
    switch_011.name = "Switch.011"
    switch_011.label = ""
    switch_011.location = (3082.611328125, -344.1962890625)
    switch_011.bl_label = "Switch"
    switch_011.input_type = "ROTATION"
    # False
    switch_011.inputs[1].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for switch_011
    links.new(switch_011.outputs[0], instance_on_points_004.inputs[5])

    sample_curve_002 = nodes.new("GeometryNodeSampleCurve")
    sample_curve_002.name = "Sample Curve.002"
    sample_curve_002.label = ""
    sample_curve_002.location = (2107.026611328125, -331.82080078125)
    sample_curve_002.bl_label = "Sample Curve"
    sample_curve_002.mode = "LENGTH"
    sample_curve_002.use_all_curves = False
    sample_curve_002.data_type = "FLOAT"
    # Value
    sample_curve_002.inputs[1].default_value = 0.0
    # Factor
    sample_curve_002.inputs[2].default_value = 0.0
    # Links for sample_curve_002

    points_004 = nodes.new("GeometryNodePoints")
    points_004.name = "Points.004"
    points_004.label = ""
    points_004.location = (1567.026611328125, -151.8204345703125)
    points_004.bl_label = "Points"
    # Position
    points_004.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Radius
    points_004.inputs[2].default_value = 0.10000000149011612
    # Links for points_004

    accumulate_field_002 = nodes.new("GeometryNodeAccumulateField")
    accumulate_field_002.name = "Accumulate Field.002"
    accumulate_field_002.label = ""
    accumulate_field_002.location = (1159.953369140625, -134.5059814453125)
    accumulate_field_002.bl_label = "Accumulate Field"
    accumulate_field_002.data_type = "INT"
    accumulate_field_002.domain = "CURVE"
    # Group ID
    accumulate_field_002.inputs[1].default_value = 0
    # Links for accumulate_field_002
    links.new(capture_attribute_001.outputs[1], accumulate_field_002.inputs[0])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (1379.9541015625, -134.5059814453125)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "INT"
    sample_index_001.domain = "CURVE"
    sample_index_001.clamp = False
    # Index
    sample_index_001.inputs[2].default_value = 0
    # Links for sample_index_001
    links.new(capture_attribute_001.outputs[0], sample_index_001.inputs[0])
    links.new(accumulate_field_002.outputs[2], sample_index_001.inputs[1])
    links.new(sample_index_001.outputs[0], points_004.inputs[0])

    resample_curve_003 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.name = "Resample Curve.003"
    resample_curve_003.label = ""
    resample_curve_003.location = (1159.953369140625, -294.50537109375)
    resample_curve_003.bl_label = "Resample Curve"
    resample_curve_003.keep_last_segment = True
    # Selection
    resample_curve_003.inputs[1].default_value = True
    # Mode
    resample_curve_003.inputs[2].default_value = "Count"
    # Length
    resample_curve_003.inputs[4].default_value = 3.669999837875366
    # Links for resample_curve_003
    links.new(capture_attribute_001.outputs[0], resample_curve_003.inputs[0])
    links.new(capture_attribute_001.outputs[1], resample_curve_003.inputs[3])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.label = ""
    sample_index_002.location = (1427.02685546875, -451.8203125)
    sample_index_002.bl_label = "Sample Index"
    sample_index_002.data_type = "INT"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    # Links for sample_index_002
    links.new(capture_attribute_001.outputs[2], sample_index_002.inputs[1])

    capture_attribute_003 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.name = "Capture Attribute.003"
    capture_attribute_003.label = ""
    capture_attribute_003.location = (1747.026611328125, -131.8203125)
    capture_attribute_003.bl_label = "Capture Attribute"
    capture_attribute_003.active_index = 1
    capture_attribute_003.domain = "POINT"
    # Links for capture_attribute_003
    links.new(points_004.outputs[0], capture_attribute_003.inputs[0])
    links.new(sample_index_002.outputs[0], capture_attribute_003.inputs[1])
    links.new(capture_attribute_003.outputs[1], sample_curve_002.inputs[4])

    index_006 = nodes.new("GeometryNodeInputIndex")
    index_006.name = "Index.006"
    index_006.label = ""
    index_006.location = (1219.95361328125, -554.505859375)
    index_006.bl_label = "Index"
    # Links for index_006
    links.new(index_006.outputs[0], sample_index_002.inputs[2])

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.name = "Sample Index.003"
    sample_index_003.label = ""
    sample_index_003.location = (1427.02685546875, -511.8203125)
    sample_index_003.bl_label = "Sample Index"
    sample_index_003.data_type = "INT"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    # Links for sample_index_003
    links.new(index_006.outputs[0], sample_index_003.inputs[2])
    links.new(sample_index_003.outputs[0], capture_attribute_003.inputs[2])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.label = ""
    spline_parameter.location = (1219.95361328125, -494.506103515625)
    spline_parameter.bl_label = "Spline Parameter"
    # Links for spline_parameter
    links.new(spline_parameter.outputs[2], sample_index_003.inputs[1])

    math_014 = nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.label = ""
    math_014.location = (1927.026611328125, -291.8206787109375)
    math_014.bl_label = "Math"
    math_014.operation = "MULTIPLY"
    math_014.use_clamp = False
    # Value
    math_014.inputs[2].default_value = 0.5
    # Links for math_014
    links.new(capture_attribute_003.outputs[2], math_014.inputs[0])
    links.new(reroute_034.outputs[0], math_014.inputs[1])
    links.new(math_014.outputs[0], sample_curve_002.inputs[3])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    set_position_003.label = ""
    set_position_003.location = (2907.0263671875, -171.8204345703125)
    set_position_003.bl_label = "Set Position"
    # Selection
    set_position_003.inputs[1].default_value = True
    # Offset
    set_position_003.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_003

    capture_attribute_004 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_004.name = "Capture Attribute.004"
    capture_attribute_004.label = ""
    capture_attribute_004.location = (2501.07666015625, -154.5260009765625)
    capture_attribute_004.bl_label = "Capture Attribute"
    capture_attribute_004.active_index = 2
    capture_attribute_004.domain = "POINT"
    # Links for capture_attribute_004
    links.new(capture_attribute_004.outputs[1], set_position_003.inputs[2])

    index_007 = nodes.new("GeometryNodeInputIndex")
    index_007.name = "Index.007"
    index_007.label = ""
    index_007.location = (639.953125, -454.505615234375)
    index_007.bl_label = "Index"
    # Links for index_007
    links.new(index_007.outputs[0], capture_attribute_001.inputs[2])

    switch_009 = nodes.new("GeometryNodeSwitch")
    switch_009.name = "Switch.009"
    switch_009.label = ""
    switch_009.location = (4509.68115234375, -308.689453125)
    switch_009.bl_label = "Switch"
    switch_009.input_type = "GEOMETRY"
    # Links for switch_009
    links.new(instance_on_points_004.outputs[0], switch_009.inputs[2])

    instance_on_points_005 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_005.name = "Instance on Points.005"
    instance_on_points_005.label = ""
    instance_on_points_005.location = (2610.251953125, -132.2110595703125)
    instance_on_points_005.bl_label = "Instance on Points"
    # Selection
    instance_on_points_005.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_005.inputs[3].default_value = False
    # Instance Index
    instance_on_points_005.inputs[4].default_value = 0
    # Scale
    instance_on_points_005.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_005
    links.new(instance_on_points_005.outputs[0], switch_009.inputs[1])

    switch_012 = nodes.new("GeometryNodeSwitch")
    switch_012.name = "Switch.012"
    switch_012.label = ""
    switch_012.location = (2380.07275390625, -256.181884765625)
    switch_012.bl_label = "Switch"
    switch_012.input_type = "ROTATION"
    # False
    switch_012.inputs[1].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for switch_012
    links.new(switch_012.outputs[0], instance_on_points_005.inputs[5])

    menu_switch_005 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_005.name = "Menu Switch.005"
    menu_switch_005.label = ""
    menu_switch_005.location = (-7352.75537109375, -230.1841278076172)
    menu_switch_005.bl_label = "Menu Switch"
    menu_switch_005.active_index = 1
    menu_switch_005.data_type = "INT"
    # Count
    menu_switch_005.inputs[1].default_value = 0
    # Distance
    menu_switch_005.inputs[2].default_value = 1
    # Links for menu_switch_005

    group_input_038 = nodes.new("NodeGroupInput")
    group_input_038.name = "Group Input.038"
    group_input_038.label = ""
    group_input_038.location = (-7552.755859375, -270.18414306640625)
    group_input_038.bl_label = "Group Input"
    # Links for group_input_038
    links.new(group_input_038.outputs[2], menu_switch_005.inputs[0])

    group_input_046 = nodes.new("NodeGroupInput")
    group_input_046.name = "Group Input.046"
    group_input_046.label = ""
    group_input_046.location = (39.95361328125, -434.505615234375)
    group_input_046.bl_label = "Group Input"
    # Links for group_input_046
    links.new(group_input_046.outputs[4], reroute_034.inputs[0])

    float_to_integer = nodes.new("FunctionNodeFloatToInt")
    float_to_integer.name = "Float to Integer"
    float_to_integer.label = ""
    float_to_integer.location = (459.953125, -294.50537109375)
    float_to_integer.bl_label = "Float to Integer"
    float_to_integer.rounding_mode = "FLOOR"
    # Links for float_to_integer
    links.new(math_008.outputs[0], float_to_integer.inputs[0])

    integer_math_004 = nodes.new("FunctionNodeIntegerMath")
    integer_math_004.name = "Integer Math.004"
    integer_math_004.label = ""
    integer_math_004.location = (639.953125, -294.50537109375)
    integer_math_004.bl_label = "Integer Math"
    integer_math_004.operation = "ADD"
    # Value
    integer_math_004.inputs[1].default_value = 1
    # Value
    integer_math_004.inputs[2].default_value = 0
    # Links for integer_math_004
    links.new(integer_math_004.outputs[0], capture_attribute_001.inputs[1])
    links.new(float_to_integer.outputs[0], integer_math_004.inputs[0])

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Curve Instances"
    frame_002.location = (-5909.01806640625, -1047.92724609375)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = "Count Method"
    frame_005.location = (1508.9453125, -35.890869140625)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    reroute_035 = nodes.new("NodeReroute")
    reroute_035.name = "Reroute.035"
    reroute_035.label = ""
    reroute_035.location = (759.95361328125, -214.505615234375)
    reroute_035.bl_label = "Reroute"
    reroute_035.socket_idname = "NodeSocketGeometry"
    # Links for reroute_035
    links.new(reroute_035.outputs[0], capture_attribute_001.inputs[0])

    frame_012 = nodes.new("NodeFrame")
    frame_012.name = "Frame.012"
    frame_012.label = "Distance Method"
    frame_012.location = (989.236328125, -690.436279296875)
    frame_012.bl_label = "Frame"
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20
    # Links for frame_012

    frame_013 = nodes.new("NodeFrame")
    frame_013.name = "Frame.013"
    frame_013.label = "Randomization"
    frame_013.location = (1077.5999755859375, -94.14545440673828)
    frame_013.bl_label = "Frame"
    frame_013.text = None
    frame_013.shrink = True
    frame_013.label_size = 20
    # Links for frame_013

    reroute_036 = nodes.new("NodeReroute")
    reroute_036.name = "Reroute.036"
    reroute_036.label = ""
    reroute_036.location = (249.28759765625, -880.7999267578125)
    reroute_036.bl_label = "Reroute"
    reroute_036.socket_idname = "NodeSocketVector"
    # Links for reroute_036
    links.new(reroute_036.outputs[0], combine_transform_004.inputs[0])
    links.new(reroute_036.outputs[0], switch.inputs[1])
    links.new(vector_math_006.outputs[0], reroute_036.inputs[0])

    sample_curve_003 = nodes.new("GeometryNodeSampleCurve")
    sample_curve_003.name = "Sample Curve.003"
    sample_curve_003.label = ""
    sample_curve_003.location = (1320.07275390625, -316.181884765625)
    sample_curve_003.bl_label = "Sample Curve"
    sample_curve_003.mode = "FACTOR"
    sample_curve_003.use_all_curves = False
    sample_curve_003.data_type = "FLOAT"
    # Value
    sample_curve_003.inputs[1].default_value = 0.0
    # Length
    sample_curve_003.inputs[3].default_value = 0.0
    # Links for sample_curve_003

    points_005 = nodes.new("GeometryNodePoints")
    points_005.name = "Points.005"
    points_005.label = ""
    points_005.location = (1514.44287109375, -117.3359375)
    points_005.bl_label = "Points"
    # Position
    points_005.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Radius
    points_005.inputs[2].default_value = 0.10000000149011612
    # Links for points_005

    integer_math_005 = nodes.new("FunctionNodeIntegerMath")
    integer_math_005.name = "Integer Math.005"
    integer_math_005.label = ""
    integer_math_005.location = (554.442626953125, -157.3359375)
    integer_math_005.bl_label = "Integer Math"
    integer_math_005.operation = "MULTIPLY"
    # Value
    integer_math_005.inputs[2].default_value = 0
    # Links for integer_math_005
    links.new(group_input_037.outputs[3], integer_math_005.inputs[0])

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (354.442626953125, -237.3359375)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "CURVE"
    # Links for domain_size
    links.new(domain_size.outputs[4], integer_math_005.inputs[1])

    switch_010 = nodes.new("GeometryNodeSwitch")
    switch_010.name = "Switch.010"
    switch_010.label = ""
    switch_010.location = (734.442626953125, -57.3359375)
    switch_010.bl_label = "Switch"
    switch_010.input_type = "INT"
    # Links for switch_010
    links.new(switch_010.outputs[0], points_005.inputs[0])
    links.new(integer_math_005.outputs[0], switch_010.inputs[2])
    links.new(group_input_037.outputs[3], switch_010.inputs[1])

    group_input_051 = nodes.new("NodeGroupInput")
    group_input_051.name = "Group Input.051"
    group_input_051.label = ""
    group_input_051.location = (554.442626953125, -37.3358154296875)
    group_input_051.bl_label = "Group Input"
    # Links for group_input_051
    links.new(group_input_051.outputs[6], switch_010.inputs[0])

    reroute_037 = nodes.new("NodeReroute")
    reroute_037.name = "Reroute.037"
    reroute_037.label = ""
    reroute_037.location = (314.44287109375, -337.3359375)
    reroute_037.bl_label = "Reroute"
    reroute_037.socket_idname = "NodeSocketGeometry"
    # Links for reroute_037
    links.new(reroute_037.outputs[0], domain_size.inputs[0])

    integer_math_006 = nodes.new("FunctionNodeIntegerMath")
    integer_math_006.name = "Integer Math.006"
    integer_math_006.label = ""
    integer_math_006.location = (780.072509765625, -476.181884765625)
    integer_math_006.bl_label = "Integer Math"
    integer_math_006.operation = "SUBTRACT"
    # Value
    integer_math_006.inputs[2].default_value = 0
    # Links for integer_math_006

    switch_013 = nodes.new("GeometryNodeSwitch")
    switch_013.name = "Switch.013"
    switch_013.label = ""
    switch_013.location = (1520.73779296875, -236.24755859375)
    switch_013.bl_label = "Switch"
    switch_013.input_type = "VECTOR"
    # Links for switch_013
    links.new(sample_curve_003.outputs[2], switch_013.inputs[2])

    switch_014 = nodes.new("GeometryNodeSwitch")
    switch_014.name = "Switch.014"
    switch_014.label = ""
    switch_014.location = (1520.73779296875, -296.2476806640625)
    switch_014.bl_label = "Switch"
    switch_014.input_type = "VECTOR"
    # Links for switch_014
    links.new(sample_curve_003.outputs[3], switch_014.inputs[2])

    index_005 = nodes.new("GeometryNodeInputIndex")
    index_005.name = "Index.005"
    index_005.label = ""
    index_005.location = (29.615234375, -396.935302734375)
    index_005.bl_label = "Index"
    # Links for index_005

    integer_math_008 = nodes.new("FunctionNodeIntegerMath")
    integer_math_008.name = "Integer Math.008"
    integer_math_008.label = ""
    integer_math_008.location = (700.07275390625, -396.1820068359375)
    integer_math_008.bl_label = "Integer Math"
    integer_math_008.operation = "MULTIPLY"
    # Value
    integer_math_008.inputs[2].default_value = 0
    # Links for integer_math_008

    integer_math_009 = nodes.new("FunctionNodeIntegerMath")
    integer_math_009.name = "Integer Math.009"
    integer_math_009.label = ""
    integer_math_009.location = (860.07275390625, -376.181884765625)
    integer_math_009.bl_label = "Integer Math"
    integer_math_009.operation = "SUBTRACT"
    # Value
    integer_math_009.inputs[2].default_value = 0
    # Links for integer_math_009
    links.new(integer_math_008.outputs[0], integer_math_009.inputs[1])

    math_009 = nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.label = ""
    math_009.location = (1060.07275390625, -436.181884765625)
    math_009.bl_label = "Math"
    math_009.operation = "DIVIDE"
    math_009.use_clamp = False
    # Value
    math_009.inputs[2].default_value = 0.5
    # Links for math_009
    links.new(integer_math_009.outputs[0], math_009.inputs[0])
    links.new(integer_math_006.outputs[0], math_009.inputs[1])
    links.new(math_009.outputs[0], sample_curve_003.inputs[2])

    integer_math_007 = nodes.new("FunctionNodeIntegerMath")
    integer_math_007.name = "Integer Math.007"
    integer_math_007.label = ""
    integer_math_007.location = (229.61474609375, -496.935302734375)
    integer_math_007.bl_label = "Integer Math"
    integer_math_007.operation = "DIVIDE"
    # Value
    integer_math_007.inputs[2].default_value = 0
    # Links for integer_math_007
    links.new(group_input_037.outputs[3], integer_math_007.inputs[1])

    reroute_040 = nodes.new("NodeReroute")
    reroute_040.name = "Reroute.040"
    reroute_040.label = ""
    reroute_040.location = (435.6806640625, -524.5430908203125)
    reroute_040.bl_label = "Reroute"
    reroute_040.socket_idname = "NodeSocketInt"
    # Links for reroute_040
    links.new(integer_math_007.outputs[0], reroute_040.inputs[0])

    switch_015 = nodes.new("GeometryNodeSwitch")
    switch_015.name = "Switch.015"
    switch_015.label = ""
    switch_015.location = (1520.73779296875, -176.24755859375)
    switch_015.bl_label = "Switch"
    switch_015.input_type = "VECTOR"
    # Links for switch_015
    links.new(sample_curve_003.outputs[1], switch_015.inputs[2])

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.name = "Capture Attribute.002"
    capture_attribute_002.label = ""
    capture_attribute_002.location = (1719.375244140625, -129.591064453125)
    capture_attribute_002.bl_label = "Capture Attribute"
    capture_attribute_002.active_index = 2
    capture_attribute_002.domain = "POINT"
    # Links for capture_attribute_002
    links.new(points_005.outputs[0], capture_attribute_002.inputs[0])
    links.new(switch_015.outputs[0], capture_attribute_002.inputs[1])
    links.new(switch_013.outputs[0], capture_attribute_002.inputs[2])
    links.new(switch_014.outputs[0], capture_attribute_002.inputs[3])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (2146.62841796875, -58.0604248046875)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Offset
    set_position_002.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_002
    links.new(set_position_002.outputs[0], instance_on_points_005.inputs[0])
    links.new(capture_attribute_002.outputs[1], set_position_002.inputs[2])

    reroute_039 = nodes.new("NodeReroute")
    reroute_039.name = "Reroute.039"
    reroute_039.label = ""
    reroute_039.location = (209.615234375, -456.935302734375)
    reroute_039.bl_label = "Reroute"
    reroute_039.socket_idname = "NodeSocketInt"
    # Links for reroute_039
    links.new(reroute_039.outputs[0], integer_math_007.inputs[0])
    links.new(index_005.outputs[0], reroute_039.inputs[0])

    reroute_041 = nodes.new("NodeReroute")
    reroute_041.name = "Reroute.041"
    reroute_041.label = ""
    reroute_041.location = (534.442626953125, -337.3359375)
    reroute_041.bl_label = "Reroute"
    reroute_041.socket_idname = "NodeSocketInt"
    # Links for reroute_041
    links.new(reroute_041.outputs[0], integer_math_006.inputs[0])
    links.new(reroute_041.outputs[0], integer_math_008.inputs[1])
    links.new(group_input_037.outputs[3], reroute_041.inputs[0])

    sample_curve_004 = nodes.new("GeometryNodeSampleCurve")
    sample_curve_004.name = "Sample Curve.004"
    sample_curve_004.label = ""
    sample_curve_004.location = (1320.07275390625, -256.181884765625)
    sample_curve_004.bl_label = "Sample Curve"
    sample_curve_004.mode = "FACTOR"
    sample_curve_004.use_all_curves = True
    sample_curve_004.data_type = "FLOAT"
    # Value
    sample_curve_004.inputs[1].default_value = 0.0
    # Length
    sample_curve_004.inputs[3].default_value = 0.0
    # Curve Index
    sample_curve_004.inputs[4].default_value = 0
    # Links for sample_curve_004
    links.new(sample_curve_004.outputs[1], switch_015.inputs[1])
    links.new(sample_curve_004.outputs[2], switch_013.inputs[1])
    links.new(sample_curve_004.outputs[3], switch_014.inputs[1])

    math_010 = nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.label = ""
    math_010.location = (985.111083984375, -222.6348876953125)
    math_010.bl_label = "Math"
    math_010.operation = "DIVIDE"
    math_010.use_clamp = False
    # Value
    math_010.inputs[2].default_value = 0.5
    # Links for math_010
    links.new(math_010.outputs[0], sample_curve_004.inputs[2])

    reroute_042 = nodes.new("NodeReroute")
    reroute_042.name = "Reroute.042"
    reroute_042.label = ""
    reroute_042.location = (1220.07275390625, -296.181884765625)
    reroute_042.bl_label = "Reroute"
    reroute_042.socket_idname = "NodeSocketGeometry"
    # Links for reroute_042
    links.new(reroute_042.outputs[0], sample_curve_003.inputs[0])
    links.new(reroute_042.outputs[0], sample_curve_004.inputs[0])
    links.new(reroute_037.outputs[0], reroute_042.inputs[0])

    is_spline_cyclic = nodes.new("GeometryNodeInputSplineCyclic")
    is_spline_cyclic.name = "Is Spline Cyclic"
    is_spline_cyclic.label = ""
    is_spline_cyclic.location = (29.2958984375, -142.549072265625)
    is_spline_cyclic.bl_label = "Is Spline Cyclic"
    # Links for is_spline_cyclic

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (214.10986328125, -115.9173583984375)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "NOT"
    # Boolean
    boolean_math.inputs[1].default_value = False
    # Links for boolean_math
    links.new(is_spline_cyclic.outputs[0], boolean_math.inputs[0])

    sample_index_004 = nodes.new("GeometryNodeSampleIndex")
    sample_index_004.name = "Sample Index.004"
    sample_index_004.label = ""
    sample_index_004.location = (560.072998046875, -476.181884765625)
    sample_index_004.bl_label = "Sample Index"
    sample_index_004.data_type = "INT"
    sample_index_004.domain = "CURVE"
    sample_index_004.clamp = False
    # Links for sample_index_004
    links.new(boolean_math.outputs[0], sample_index_004.inputs[1])
    links.new(reroute_040.outputs[0], sample_index_004.inputs[2])
    links.new(reroute_037.outputs[0], sample_index_004.inputs[0])
    links.new(sample_index_004.outputs[0], integer_math_006.inputs[1])

    integer_math_010 = nodes.new("FunctionNodeIntegerMath")
    integer_math_010.name = "Integer Math.010"
    integer_math_010.label = ""
    integer_math_010.location = (748.2001953125, -221.6033935546875)
    integer_math_010.bl_label = "Integer Math"
    integer_math_010.operation = "SUBTRACT"
    # Value
    integer_math_010.inputs[1].default_value = 1
    # Value
    integer_math_010.inputs[2].default_value = 0
    # Links for integer_math_010
    links.new(reroute_041.outputs[0], integer_math_010.inputs[0])
    links.new(integer_math_010.outputs[0], math_010.inputs[1])

    reroute_044 = nodes.new("NodeReroute")
    reroute_044.name = "Reroute.044"
    reroute_044.label = ""
    reroute_044.location = (1414.452392578125, -152.4134521484375)
    reroute_044.bl_label = "Reroute"
    reroute_044.socket_idname = "NodeSocketBool"
    # Links for reroute_044
    links.new(reroute_044.outputs[0], switch_013.inputs[0])
    links.new(reroute_044.outputs[0], switch_014.inputs[0])
    links.new(reroute_044.outputs[0], switch_015.inputs[0])
    links.new(group_input_051.outputs[6], reroute_044.inputs[0])

    set_i_d = nodes.new("GeometryNodeSetID")
    set_i_d.name = "Set ID"
    set_i_d.label = ""
    set_i_d.location = (1939.334228515625, -74.266845703125)
    set_i_d.bl_label = "Set ID"
    # Selection
    set_i_d.inputs[1].default_value = True
    # Links for set_i_d
    links.new(set_i_d.outputs[0], set_position_002.inputs[0])
    links.new(capture_attribute_002.outputs[0], set_i_d.inputs[0])

    hash_value_001 = nodes.new("FunctionNodeHashValue")
    hash_value_001.name = "Hash Value.001"
    hash_value_001.label = ""
    hash_value_001.location = (1320.07275390625, -516.1820068359375)
    hash_value_001.bl_label = "Hash Value"
    hash_value_001.data_type = "INT"
    # Links for hash_value_001
    links.new(integer_math_009.outputs[0], hash_value_001.inputs[1])

    switch_016 = nodes.new("GeometryNodeSwitch")
    switch_016.name = "Switch.016"
    switch_016.label = ""
    switch_016.location = (1717.404296875, -363.6923828125)
    switch_016.bl_label = "Switch"
    switch_016.input_type = "INT"
    # Links for switch_016
    links.new(switch_016.outputs[0], set_i_d.inputs[2])
    links.new(reroute_044.outputs[0], switch_016.inputs[0])

    hash_value_002 = nodes.new("FunctionNodeHashValue")
    hash_value_002.name = "Hash Value.002"
    hash_value_002.label = ""
    hash_value_002.location = (1520.07275390625, -416.181884765625)
    hash_value_002.bl_label = "Hash Value"
    hash_value_002.data_type = "INT"
    # Links for hash_value_002
    links.new(hash_value_002.outputs[0], switch_016.inputs[1])

    index_008 = nodes.new("GeometryNodeInputIndex")
    index_008.name = "Index.008"
    index_008.label = ""
    index_008.location = (1320.07275390625, -396.181884765625)
    index_008.bl_label = "Index"
    # Links for index_008
    links.new(index_008.outputs[0], hash_value_002.inputs[0])

    hash_value_003 = nodes.new("FunctionNodeHashValue")
    hash_value_003.name = "Hash Value.003"
    hash_value_003.label = ""
    hash_value_003.location = (1520.07275390625, -516.1820068359375)
    hash_value_003.bl_label = "Hash Value"
    hash_value_003.data_type = "INT"
    # Links for hash_value_003
    links.new(hash_value_003.outputs[0], switch_016.inputs[2])
    links.new(hash_value_001.outputs[0], hash_value_003.inputs[0])

    group_input_052 = nodes.new("NodeGroupInput")
    group_input_052.name = "Group Input.052"
    group_input_052.label = ""
    group_input_052.location = (1320.07275390625, -456.181884765625)
    group_input_052.bl_label = "Group Input"
    # Links for group_input_052
    links.new(group_input_052.outputs[33], hash_value_003.inputs[1])
    links.new(group_input_052.outputs[33], hash_value_002.inputs[1])

    reroute_046 = nodes.new("NodeReroute")
    reroute_046.name = "Reroute.046"
    reroute_046.label = ""
    reroute_046.location = (-5650.98291015625, -962.7913818359375)
    reroute_046.bl_label = "Reroute"
    reroute_046.socket_idname = "NodeSocketInt"
    # Links for reroute_046

    reroute_047 = nodes.new("NodeReroute")
    reroute_047.name = "Reroute.047"
    reroute_047.label = ""
    reroute_047.location = (-1620.0, -959.9999389648438)
    reroute_047.bl_label = "Reroute"
    reroute_047.socket_idname = "NodeSocketInt"
    # Links for reroute_047
    links.new(reroute_047.outputs[0], switch_009.inputs[0])
    links.new(reroute_046.outputs[0], reroute_047.inputs[0])

    reroute_048 = nodes.new("NodeReroute")
    reroute_048.name = "Reroute.048"
    reroute_048.label = ""
    reroute_048.location = (-6012.755859375, -270.18414306640625)
    reroute_048.bl_label = "Reroute"
    reroute_048.socket_idname = "NodeSocketInt"
    # Links for reroute_048
    links.new(reroute_048.outputs[0], reroute_046.inputs[0])

    reroute_049 = nodes.new("NodeReroute")
    reroute_049.name = "Reroute.049"
    reroute_049.label = ""
    reroute_049.location = (64.29736328125, -57.92025375366211)
    reroute_049.bl_label = "Reroute"
    reroute_049.socket_idname = "NodeSocketInt"
    # Links for reroute_049
    links.new(reroute_048.outputs[0], reroute_049.inputs[0])

    switch_017 = nodes.new("GeometryNodeSwitch")
    switch_017.name = "Switch.017"
    switch_017.label = ""
    switch_017.location = (1122.8994140625, -35.7423210144043)
    switch_017.bl_label = "Switch"
    switch_017.input_type = "INT"
    # Links for switch_017
    links.new(group_input_042.outputs[3], switch_017.inputs[1])
    links.new(switch_017.outputs[0], points_002.inputs[0])
    links.new(switch_017.outputs[0], reroute_029.inputs[0])

    float_to_integer_001 = nodes.new("FunctionNodeFloatToInt")
    float_to_integer_001.name = "Float to Integer.001"
    float_to_integer_001.label = ""
    float_to_integer_001.location = (563.81103515625, -172.04275512695312)
    float_to_integer_001.bl_label = "Float to Integer"
    float_to_integer_001.rounding_mode = "FLOOR"
    # Links for float_to_integer_001

    switch_018 = nodes.new("GeometryNodeSwitch")
    switch_018.name = "Switch.018"
    switch_018.label = ""
    switch_018.location = (813.0185546875, -596.5751953125)
    switch_018.bl_label = "Switch"
    switch_018.input_type = "GEOMETRY"
    # Links for switch_018
    links.new(switch_018.outputs[0], join_geometry_002.inputs[0])
    links.new(linear_gizmo_003.outputs[0], switch_018.inputs[1])

    group_input_055 = nodes.new("NodeGroupInput")
    group_input_055.name = "Group Input.055"
    group_input_055.label = ""
    group_input_055.location = (425.87646484375, -935.1279296875)
    group_input_055.bl_label = "Group Input"
    # Links for group_input_055

    reroute_050 = nodes.new("NodeReroute")
    reroute_050.name = "Reroute.050"
    reroute_050.label = ""
    reroute_050.location = (-6832.755859375, -270.18414306640625)
    reroute_050.bl_label = "Reroute"
    reroute_050.socket_idname = "NodeSocketInt"
    # Links for reroute_050
    links.new(reroute_050.outputs[0], reroute_048.inputs[0])
    links.new(reroute_050.outputs[0], switch_018.inputs[0])
    links.new(menu_switch_005.outputs[0], reroute_050.inputs[0])

    math_011 = nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.label = ""
    math_011.location = (396.67626953125, -208.47506713867188)
    math_011.bl_label = "Math"
    math_011.operation = "DIVIDE"
    math_011.use_clamp = False
    # Value
    math_011.inputs[2].default_value = 0.5
    # Links for math_011
    links.new(group_input_042.outputs[5], math_011.inputs[1])

    index_switch_003 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_003.name = "Index Switch.003"
    index_switch_003.label = ""
    index_switch_003.location = (236.6767578125, -168.47506713867188)
    index_switch_003.bl_label = "Index Switch"
    index_switch_003.data_type = "FLOAT"
    # 0
    index_switch_003.inputs[1].default_value = 6.2831854820251465
    # Links for index_switch_003
    links.new(group_input_042.outputs[15], index_switch_003.inputs[2])
    links.new(index_switch_003.outputs[0], math_011.inputs[0])
    links.new(reroute_031.outputs[0], index_switch_003.inputs[0])

    math_012 = nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.label = ""
    math_012.location = (396.67626953125, -248.47506713867188)
    math_012.bl_label = "Math"
    math_012.operation = "ABSOLUTE"
    math_012.use_clamp = False
    # Value
    math_012.inputs[1].default_value = 0.5
    # Value
    math_012.inputs[2].default_value = 0.5
    # Links for math_012
    links.new(math_011.outputs[0], math_012.inputs[0])

    math_013 = nodes.new("ShaderNodeMath")
    math_013.name = "Math.013"
    math_013.label = ""
    math_013.location = (396.67626953125, -288.4750671386719)
    math_013.bl_label = "Math"
    math_013.operation = "MAXIMUM"
    math_013.use_clamp = False
    # Value
    math_013.inputs[1].default_value = 1.0
    # Value
    math_013.inputs[2].default_value = 0.5
    # Links for math_013
    links.new(math_013.outputs[0], float_to_integer_001.inputs[0])
    links.new(math_012.outputs[0], math_013.inputs[0])

    group_input_057 = nodes.new("NodeGroupInput")
    group_input_057.name = "Group Input.057"
    group_input_057.label = ""
    group_input_057.location = (1748.5869140625, -57.6375732421875)
    group_input_057.bl_label = "Group Input"
    # Links for group_input_057

    sample_curve_005 = nodes.new("GeometryNodeSampleCurve")
    sample_curve_005.name = "Sample Curve.005"
    sample_curve_005.label = ""
    sample_curve_005.location = (2107.026611328125, -391.820556640625)
    sample_curve_005.bl_label = "Sample Curve"
    sample_curve_005.mode = "LENGTH"
    sample_curve_005.use_all_curves = True
    sample_curve_005.data_type = "FLOAT"
    # Value
    sample_curve_005.inputs[1].default_value = 0.0
    # Factor
    sample_curve_005.inputs[2].default_value = 0.0
    # Curve Index
    sample_curve_005.inputs[4].default_value = 0
    # Links for sample_curve_005

    switch_019 = nodes.new("GeometryNodeSwitch")
    switch_019.name = "Switch.019"
    switch_019.label = ""
    switch_019.location = (2319.734375, -253.1563720703125)
    switch_019.bl_label = "Switch"
    switch_019.input_type = "VECTOR"
    # Links for switch_019
    links.new(sample_curve_002.outputs[1], switch_019.inputs[2])
    links.new(switch_019.outputs[0], capture_attribute_004.inputs[1])
    links.new(sample_curve_005.outputs[1], switch_019.inputs[1])

    switch_020 = nodes.new("GeometryNodeSwitch")
    switch_020.name = "Switch.020"
    switch_020.label = ""
    switch_020.location = (2318.2158203125, -298.7169189453125)
    switch_020.bl_label = "Switch"
    switch_020.input_type = "VECTOR"
    # Links for switch_020
    links.new(switch_020.outputs[0], capture_attribute_004.inputs[2])
    links.new(sample_curve_002.outputs[2], switch_020.inputs[2])
    links.new(sample_curve_005.outputs[2], switch_020.inputs[1])

    switch_021 = nodes.new("GeometryNodeSwitch")
    switch_021.name = "Switch.021"
    switch_021.label = ""
    switch_021.location = (2317.83642578125, -354.14892578125)
    switch_021.bl_label = "Switch"
    switch_021.input_type = "VECTOR"
    # Links for switch_021
    links.new(switch_021.outputs[0], capture_attribute_004.inputs[3])
    links.new(sample_curve_002.outputs[3], switch_021.inputs[2])
    links.new(sample_curve_005.outputs[3], switch_021.inputs[1])

    switch_022 = nodes.new("GeometryNodeSwitch")
    switch_022.name = "Switch.022"
    switch_022.label = ""
    switch_022.location = (2107.026123046875, -91.820556640625)
    switch_022.bl_label = "Switch"
    switch_022.input_type = "GEOMETRY"
    # Links for switch_022
    links.new(switch_022.outputs[0], capture_attribute_004.inputs[0])
    links.new(capture_attribute_003.outputs[0], switch_022.inputs[2])
    links.new(points_004.outputs[0], switch_022.inputs[1])

    reroute_051 = nodes.new("NodeReroute")
    reroute_051.name = "Reroute.051"
    reroute_051.label = ""
    reroute_051.location = (2087.0263671875, -131.8203125)
    reroute_051.bl_label = "Reroute"
    reroute_051.socket_idname = "NodeSocketBool"
    # Links for reroute_051
    links.new(group_input_057.outputs[6], reroute_051.inputs[0])
    links.new(reroute_051.outputs[0], switch_022.inputs[0])

    index_009 = nodes.new("GeometryNodeInputIndex")
    index_009.name = "Index.009"
    index_009.label = ""
    index_009.location = (1567.026611328125, -371.820556640625)
    index_009.bl_label = "Index"
    # Links for index_009

    math_015 = nodes.new("ShaderNodeMath")
    math_015.name = "Math.015"
    math_015.label = ""
    math_015.location = (1927.026123046875, -431.8203125)
    math_015.bl_label = "Math"
    math_015.operation = "MULTIPLY"
    math_015.use_clamp = False
    # Value
    math_015.inputs[2].default_value = 0.5
    # Links for math_015
    links.new(math_015.outputs[0], sample_curve_005.inputs[3])

    math_016 = nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.label = ""
    math_016.location = (1747.026123046875, -411.820556640625)
    math_016.bl_label = "Math"
    math_016.operation = "DIVIDE"
    math_016.use_clamp = False
    # Value
    math_016.inputs[2].default_value = 0.5
    # Links for math_016
    links.new(math_016.outputs[0], math_015.inputs[0])
    links.new(index_009.outputs[0], math_016.inputs[0])

    math_017 = nodes.new("ShaderNodeMath")
    math_017.name = "Math.017"
    math_017.label = ""
    math_017.location = (590.22802734375, -546.045654296875)
    math_017.bl_label = "Math"
    math_017.operation = "DIVIDE"
    math_017.use_clamp = False
    # Value
    math_017.inputs[2].default_value = 0.5
    # Links for math_017
    links.new(reroute_034.outputs[0], math_017.inputs[1])

    float_to_integer_002 = nodes.new("FunctionNodeFloatToInt")
    float_to_integer_002.name = "Float to Integer.002"
    float_to_integer_002.label = ""
    float_to_integer_002.location = (770.228515625, -546.045654296875)
    float_to_integer_002.bl_label = "Float to Integer"
    float_to_integer_002.rounding_mode = "FLOOR"
    # Links for float_to_integer_002
    links.new(math_017.outputs[0], float_to_integer_002.inputs[0])

    integer_math_011 = nodes.new("FunctionNodeIntegerMath")
    integer_math_011.name = "Integer Math.011"
    integer_math_011.label = ""
    integer_math_011.location = (950.228271484375, -546.045654296875)
    integer_math_011.bl_label = "Integer Math"
    integer_math_011.operation = "ADD"
    # Value
    integer_math_011.inputs[1].default_value = 1
    # Value
    integer_math_011.inputs[2].default_value = 0
    # Links for integer_math_011
    links.new(float_to_integer_002.outputs[0], integer_math_011.inputs[0])
    links.new(integer_math_011.outputs[0], math_016.inputs[1])

    curve_length = nodes.new("GeometryNodeCurveLength")
    curve_length.name = "Curve Length"
    curve_length.label = ""
    curve_length.location = (420.41943359375, -559.545654296875)
    curve_length.bl_label = "Curve Length"
    # Links for curve_length
    links.new(curve_length.outputs[0], math_017.inputs[0])
    links.new(curve_length.outputs[0], math_015.inputs[1])

    reroute_052 = nodes.new("NodeReroute")
    reroute_052.name = "Reroute.052"
    reroute_052.label = ""
    reroute_052.location = (2266.09619140625, -186.986572265625)
    reroute_052.bl_label = "Reroute"
    reroute_052.socket_idname = "NodeSocketBool"
    # Links for reroute_052
    links.new(reroute_052.outputs[0], switch_019.inputs[0])
    links.new(reroute_052.outputs[0], switch_020.inputs[0])
    links.new(reroute_052.outputs[0], switch_021.inputs[0])
    links.new(reroute_051.outputs[0], reroute_052.inputs[0])

    set_i_d_001 = nodes.new("GeometryNodeSetID")
    set_i_d_001.name = "Set ID.001"
    set_i_d_001.label = ""
    set_i_d_001.location = (2721.126708984375, -141.3544921875)
    set_i_d_001.bl_label = "Set ID"
    # Selection
    set_i_d_001.inputs[1].default_value = True
    # Links for set_i_d_001
    links.new(set_i_d_001.outputs[0], set_position_003.inputs[0])
    links.new(capture_attribute_004.outputs[0], set_i_d_001.inputs[0])

    reroute_053 = nodes.new("NodeReroute")
    reroute_053.name = "Reroute.053"
    reroute_053.label = ""
    reroute_053.location = (2047.0263671875, -371.820556640625)
    reroute_053.bl_label = "Reroute"
    reroute_053.socket_idname = "NodeSocketGeometry"
    # Links for reroute_053
    links.new(reroute_053.outputs[0], sample_curve_002.inputs[0])
    links.new(reroute_053.outputs[0], sample_curve_005.inputs[0])
    links.new(reroute_035.outputs[0], reroute_053.inputs[0])

    reroute_054 = nodes.new("NodeReroute")
    reroute_054.name = "Reroute.054"
    reroute_054.label = ""
    reroute_054.location = (1387.026611328125, -491.82080078125)
    reroute_054.bl_label = "Reroute"
    reroute_054.socket_idname = "NodeSocketGeometry"
    # Links for reroute_054
    links.new(reroute_054.outputs[0], sample_index_002.inputs[0])
    links.new(reroute_054.outputs[0], sample_index_003.inputs[0])
    links.new(resample_curve_003.outputs[0], reroute_054.inputs[0])

    switch_023 = nodes.new("GeometryNodeSwitch")
    switch_023.name = "Switch.023"
    switch_023.label = ""
    switch_023.location = (2510.8427734375, -499.998779296875)
    switch_023.bl_label = "Switch"
    switch_023.input_type = "INT"
    # Links for switch_023
    links.new(reroute_051.outputs[0], switch_023.inputs[0])
    links.new(switch_023.outputs[0], set_i_d_001.inputs[2])

    hash_value_004 = nodes.new("FunctionNodeHashValue")
    hash_value_004.name = "Hash Value.004"
    hash_value_004.label = ""
    hash_value_004.location = (2287.026611328125, -511.82080078125)
    hash_value_004.bl_label = "Hash Value"
    hash_value_004.data_type = "INT"
    # Links for hash_value_004
    links.new(hash_value_004.outputs[0], switch_023.inputs[1])

    index_010 = nodes.new("GeometryNodeInputIndex")
    index_010.name = "Index.010"
    index_010.label = ""
    index_010.location = (2087.02685546875, -491.82080078125)
    index_010.bl_label = "Index"
    # Links for index_010
    links.new(index_010.outputs[0], hash_value_004.inputs[0])

    group_input_058 = nodes.new("NodeGroupInput")
    group_input_058.name = "Group Input.058"
    group_input_058.label = ""
    group_input_058.location = (2087.02685546875, -531.820556640625)
    group_input_058.bl_label = "Group Input"
    # Links for group_input_058
    links.new(group_input_058.outputs[33], hash_value_004.inputs[1])

    hash_value_005 = nodes.new("FunctionNodeHashValue")
    hash_value_005.name = "Hash Value.005"
    hash_value_005.label = ""
    hash_value_005.location = (2287.026611328125, -571.820556640625)
    hash_value_005.bl_label = "Hash Value"
    hash_value_005.data_type = "INT"
    # Links for hash_value_005
    links.new(hash_value_005.outputs[0], switch_023.inputs[2])
    links.new(group_input_058.outputs[33], hash_value_005.inputs[1])

    hash_value_006 = nodes.new("FunctionNodeHashValue")
    hash_value_006.name = "Hash Value.006"
    hash_value_006.label = ""
    hash_value_006.location = (2087.0263671875, -591.820556640625)
    hash_value_006.bl_label = "Hash Value"
    hash_value_006.data_type = "INT"
    # Links for hash_value_006
    links.new(hash_value_006.outputs[0], hash_value_005.inputs[0])
    links.new(capture_attribute_003.outputs[2], hash_value_006.inputs[1])
    links.new(capture_attribute_003.outputs[1], hash_value_006.inputs[0])

    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.name = "Mix.003"
    mix_003.label = ""
    mix_003.location = (289.2724609375, -175.81060791015625)
    mix_003.bl_label = "Mix"
    mix_003.data_type = "ROTATION"
    mix_003.factor_mode = "UNIFORM"
    mix_003.blend_type = "MIX"
    mix_003.clamp_factor = False
    mix_003.clamp_result = False
    # Factor
    mix_003.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_003.inputs[2].default_value = 0.0
    # B
    mix_003.inputs[3].default_value = 0.0
    # A
    mix_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_003.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_003.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_003.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_003
    links.new(reroute_003.outputs[0], mix_003.inputs[0])
    links.new(mix_003.outputs[3], index_switch_007.inputs[3])

    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.name = "Mix.004"
    mix_004.label = ""
    mix_004.location = (729.2724609375, -35.810546875)
    mix_004.bl_label = "Mix"
    mix_004.data_type = "ROTATION"
    mix_004.factor_mode = "UNIFORM"
    mix_004.blend_type = "MIX"
    mix_004.clamp_factor = False
    mix_004.clamp_result = False
    # Factor
    mix_004.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_004.inputs[2].default_value = 0.0
    # B
    mix_004.inputs[3].default_value = 0.0
    # A
    mix_004.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_004.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_004.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_004.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_004.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_004
    links.new(index_001.outputs[0], mix_004.inputs[0])
    links.new(index_switch_007.outputs[0], mix_004.inputs[9])
    links.new(mix_004.outputs[3], instance_on_points.inputs[5])

    reroute_019 = nodes.new("NodeReroute")
    reroute_019.name = "Reroute.019"
    reroute_019.label = ""
    reroute_019.location = (469.2724609375, -175.81060791015625)
    reroute_019.bl_label = "Reroute"
    reroute_019.socket_idname = "NodeSocketRotation"
    # Links for reroute_019
    links.new(reroute_019.outputs[0], index_switch_007.inputs[2])
    links.new(reroute_019.outputs[0], index_switch_007.inputs[1])

    warning = nodes.new("GeometryNodeWarning")
    warning.name = "Warning"
    warning.label = ""
    warning.location = (409.353515625, -68.47505187988281)
    warning.bl_label = "Warning"
    warning.warning_type = "ERROR"
    # Message
    warning.inputs[1].default_value = "Invalid Distance"
    # Links for warning

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (243.62939453125, -120.98324584960938)
    compare_003.bl_label = "Compare"
    compare_003.operation = "EQUAL"
    compare_003.data_type = "FLOAT"
    compare_003.mode = "ELEMENT"
    # B
    compare_003.inputs[1].default_value = 0.0
    # A
    compare_003.inputs[2].default_value = 0
    # B
    compare_003.inputs[3].default_value = 0
    # A
    compare_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_003.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_003.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_003.inputs[8].default_value = ""
    # B
    compare_003.inputs[9].default_value = ""
    # C
    compare_003.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_003.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_003.inputs[12].default_value = 0.0
    # Links for compare_003
    links.new(compare_003.outputs[0], warning.inputs[0])
    links.new(group_input_042.outputs[5], compare_003.inputs[0])

    warning_001 = nodes.new("GeometryNodeWarning")
    warning_001.name = "Warning.001"
    warning_001.label = ""
    warning_001.location = (2904.4208984375, -36.030029296875)
    warning_001.bl_label = "Warning"
    warning_001.warning_type = "ERROR"
    # Message
    warning_001.inputs[1].default_value = "Invalid Distance"
    # Links for warning_001

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (2718.51513671875, -65.7818603515625)
    compare_004.bl_label = "Compare"
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    # B
    compare_004.inputs[1].default_value = 0.0
    # A
    compare_004.inputs[2].default_value = 0
    # B
    compare_004.inputs[3].default_value = 0
    # A
    compare_004.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_004.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_004.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_004.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_004.inputs[8].default_value = ""
    # B
    compare_004.inputs[9].default_value = ""
    # C
    compare_004.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_004.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_004.inputs[12].default_value = 0.0
    # Links for compare_004
    links.new(compare_004.outputs[0], warning_001.inputs[0])

    switch_025 = nodes.new("GeometryNodeSwitch")
    switch_025.name = "Switch.025"
    switch_025.label = ""
    switch_025.location = (3087.251953125, -112.782470703125)
    switch_025.bl_label = "Switch"
    switch_025.input_type = "GEOMETRY"
    # Links for switch_025
    links.new(switch_025.outputs[0], instance_on_points_004.inputs[0])
    links.new(set_position_003.outputs[0], switch_025.inputs[1])
    links.new(warning_001.outputs[0], switch_025.inputs[0])

    points_007 = nodes.new("GeometryNodePoints")
    points_007.name = "Points.007"
    points_007.label = ""
    points_007.location = (2906.32275390625, -265.9876708984375)
    points_007.bl_label = "Points"
    # Count
    points_007.inputs[0].default_value = 1
    # Position
    points_007.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Radius
    points_007.inputs[2].default_value = 0.10000000149011612
    # Links for points_007
    links.new(points_007.outputs[0], switch_025.inputs[2])

    group_input_059 = nodes.new("NodeGroupInput")
    group_input_059.name = "Group Input.059"
    group_input_059.label = ""
    group_input_059.location = (2537.467041015625, -35.7509765625)
    group_input_059.bl_label = "Group Input"
    # Links for group_input_059
    links.new(group_input_059.outputs[4], compare_004.inputs[0])

    switch_024 = nodes.new("GeometryNodeSwitch")
    switch_024.name = "Switch.024"
    switch_024.label = ""
    switch_024.location = (921.7265625, -88.84176635742188)
    switch_024.bl_label = "Switch"
    switch_024.input_type = "INT"
    # True
    switch_024.inputs[2].default_value = 1
    # Links for switch_024
    links.new(switch_024.outputs[0], switch_017.inputs[2])
    links.new(warning.outputs[0], switch_024.inputs[0])

    realize_instances_002 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.name = "Realize Instances.002"
    realize_instances_002.label = ""
    realize_instances_002.location = (191.036376953125, -275.6751403808594)
    realize_instances_002.bl_label = "Realize Instances"
    # Selection
    realize_instances_002.inputs[1].default_value = True
    # Realize All
    realize_instances_002.inputs[2].default_value = True
    # Depth
    realize_instances_002.inputs[3].default_value = 0
    # Links for realize_instances_002
    links.new(reroute_033.outputs[0], realize_instances_002.inputs[0])

    switch_026 = nodes.new("GeometryNodeSwitch")
    switch_026.name = "Switch.026"
    switch_026.label = ""
    switch_026.location = (871.03662109375, -35.67506408691406)
    switch_026.bl_label = "Switch"
    switch_026.input_type = "GEOMETRY"
    # Links for switch_026
    links.new(switch_026.outputs[0], group_output.inputs[0])
    links.new(reroute_033.outputs[0], switch_026.inputs[1])
    links.new(switch_008.outputs[0], switch_026.inputs[2])

    group_input_018 = nodes.new("NodeGroupInput")
    group_input_018.name = "Group Input.018"
    group_input_018.label = ""
    group_input_018.location = (631.036376953125, -35.67506408691406)
    group_input_018.bl_label = "Group Input"
    # Links for group_input_018
    links.new(group_input_018.outputs[20], switch_026.inputs[0])

    group_input_011 = nodes.new("NodeGroupInput")
    group_input_011.name = "Group Input.011"
    group_input_011.label = ""
    group_input_011.location = (2687.026611328125, -411.820556640625)
    group_input_011.bl_label = "Group Input"
    # Links for group_input_011
    links.new(group_input_011.outputs[21], switch_011.inputs[0])

    _axis_alignment_switch = nodes.new("GeometryNodeGroup")
    _axis_alignment_switch.name = "Group"
    _axis_alignment_switch.label = ""
    _axis_alignment_switch.location = (2887.0263671875, -451.820556640625)
    _axis_alignment_switch.node_tree = create__axis_alignment_switch_group()
    _axis_alignment_switch.bl_label = "Group"
    # Links for _axis_alignment_switch
    links.new(_axis_alignment_switch.outputs[0], switch_011.inputs[2])
    links.new(group_input_011.outputs[22], _axis_alignment_switch.inputs[0])
    links.new(capture_attribute_004.outputs[2], _axis_alignment_switch.inputs[2])
    links.new(capture_attribute_004.outputs[3], _axis_alignment_switch.inputs[3])
    links.new(group_input_011.outputs[23], _axis_alignment_switch.inputs[1])

    group_input_062 = nodes.new("NodeGroupInput")
    group_input_062.name = "Group Input.062"
    group_input_062.label = ""
    group_input_062.location = (1900.07275390625, -376.181884765625)
    group_input_062.bl_label = "Group Input"
    # Links for group_input_062
    links.new(group_input_062.outputs[0], instance_on_points_005.inputs[2])
    links.new(group_input_062.outputs[21], switch_012.inputs[0])

    _axis_alignment_switch_1 = nodes.new("GeometryNodeGroup")
    _axis_alignment_switch_1.name = "Group.001"
    _axis_alignment_switch_1.label = ""
    _axis_alignment_switch_1.location = (2180.072509765625, -396.181884765625)
    _axis_alignment_switch_1.node_tree = create__axis_alignment_switch_group()
    _axis_alignment_switch_1.bl_label = "Group"
    # Links for _axis_alignment_switch_1
    links.new(group_input_062.outputs[22], _axis_alignment_switch_1.inputs[0])
    links.new(group_input_062.outputs[23], _axis_alignment_switch_1.inputs[1])
    links.new(capture_attribute_002.outputs[2], _axis_alignment_switch_1.inputs[2])
    links.new(capture_attribute_002.outputs[3], _axis_alignment_switch_1.inputs[3])
    links.new(_axis_alignment_switch_1.outputs[0], switch_012.inputs[2])

    _axis_alignment_switch_2 = nodes.new("GeometryNodeGroup")
    _axis_alignment_switch_2.name = "Group.002"
    _axis_alignment_switch_2.label = ""
    _axis_alignment_switch_2.location = (2887.72705078125, -504.0140380859375)
    _axis_alignment_switch_2.node_tree = create__axis_alignment_switch_group()
    _axis_alignment_switch_2.bl_label = "Group"
    # Links for _axis_alignment_switch_2

    transform_direction = nodes.new("FunctionNodeTransformDirection")
    transform_direction.name = "Transform Direction"
    transform_direction.label = ""
    transform_direction.location = (2674.33984375, -664.3065795898438)
    transform_direction.bl_label = "Transform Direction"
    # Direction
    transform_direction.inputs[0].default_value = Vector((0.0, 0.0, 1.0))
    # Links for transform_direction
    links.new(transform_direction.outputs[0], _axis_alignment_switch_2.inputs[3])

    transform_direction_001 = nodes.new("FunctionNodeTransformDirection")
    transform_direction_001.name = "Transform Direction.001"
    transform_direction_001.label = ""
    transform_direction_001.location = (2674.33984375, -524.306640625)
    transform_direction_001.bl_label = "Transform Direction"
    # Direction
    transform_direction_001.inputs[0].default_value = Vector((1.0, 0.0, 0.0))
    # Links for transform_direction_001
    links.new(transform_direction_001.outputs[0], _axis_alignment_switch_2.inputs[2])

    group_input_067 = nodes.new("NodeGroupInput")
    group_input_067.name = "Group Input.067"
    group_input_067.label = ""
    group_input_067.location = (2678.154052734375, -385.1923828125)
    group_input_067.bl_label = "Group Input"
    # Links for group_input_067
    links.new(group_input_067.outputs[22], _axis_alignment_switch_2.inputs[0])

    group_input_068 = nodes.new("NodeGroupInput")
    group_input_068.name = "Group Input.068"
    group_input_068.label = ""
    group_input_068.location = (2675.8564453125, -454.10113525390625)
    group_input_068.bl_label = "Group Input"
    # Links for group_input_068
    links.new(group_input_068.outputs[23], _axis_alignment_switch_2.inputs[1])

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (2979.9833984375, -92.75325775146484)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Matrix"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry
    links.new(transform_geometry.outputs[0], instance_on_points_001.inputs[0])
    links.new(set_position_001.outputs[0], transform_geometry.inputs[0])
    links.new(reroute_010.outputs[0], transform_geometry.inputs[5])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.name = "Rotate Rotation"
    rotate_rotation.label = ""
    rotate_rotation.location = (3109.353515625, -368.47503662109375)
    rotate_rotation.bl_label = "Rotate Rotation"
    rotate_rotation.rotation_space = "GLOBAL"
    # Links for rotate_rotation
    links.new(_axis_alignment_switch_2.outputs[0], rotate_rotation.inputs[0])
    links.new(rotate_rotation.outputs[0], switch_001.inputs[2])

    reroute_006 = nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.label = ""
    reroute_006.location = (2631.29931640625, -704.178466796875)
    reroute_006.bl_label = "Reroute"
    reroute_006.socket_idname = "NodeSocketMatrix"
    # Links for reroute_006
    links.new(reroute_006.outputs[0], transform_direction.inputs[1])
    links.new(reroute_006.outputs[0], transform_direction_001.inputs[1])

    combine_transform_005 = nodes.new("FunctionNodeCombineTransform")
    combine_transform_005.name = "Combine Transform.005"
    combine_transform_005.label = ""
    combine_transform_005.location = (2459.06640625, -655.9279174804688)
    combine_transform_005.bl_label = "Combine Transform"
    # Translation
    combine_transform_005.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    # Scale
    combine_transform_005.inputs[2].default_value = Vector((1.0, 1.0, 1.0))
    # Links for combine_transform_005
    links.new(combine_x_y_z_002.outputs[0], combine_transform_005.inputs[1])
    links.new(combine_transform_005.outputs[0], reroute_006.inputs[0])

    reroute_004 = nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.label = ""
    reroute_004.location = (1339.11376953125, -365.7755126953125)
    reroute_004.bl_label = "Reroute"
    reroute_004.socket_idname = "NodeSocketGeometry"
    # Links for reroute_004
    links.new(reroute_004.outputs[0], reroute_035.inputs[0])
    links.new(reroute_004.outputs[0], reroute_037.inputs[0])
    links.new(reroute_004.outputs[0], curve_length.inputs[0])

    switch_027 = nodes.new("GeometryNodeSwitch")
    switch_027.name = "Switch.027"
    switch_027.label = ""
    switch_027.location = (1145.58642578125, -243.45068359375)
    switch_027.bl_label = "Switch"
    switch_027.input_type = "GEOMETRY"
    # Links for switch_027
    links.new(switch_027.outputs[0], reroute_004.inputs[0])
    links.new(switch_006.outputs[0], switch_027.inputs[1])

    domain_size_001 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_001.name = "Domain Size.001"
    domain_size_001.label = ""
    domain_size_001.location = (626.458984375, -232.1055908203125)
    domain_size_001.bl_label = "Domain Size"
    domain_size_001.component = "CURVE"
    # Links for domain_size_001
    links.new(switch_006.outputs[0], domain_size_001.inputs[0])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (792.6455078125, -204.3087158203125)
    compare_005.bl_label = "Compare"
    compare_005.operation = "EQUAL"
    compare_005.data_type = "INT"
    compare_005.mode = "ELEMENT"
    # A
    compare_005.inputs[0].default_value = 0.0
    # B
    compare_005.inputs[1].default_value = 0.0
    # B
    compare_005.inputs[3].default_value = 0
    # A
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_005.inputs[8].default_value = ""
    # B
    compare_005.inputs[9].default_value = ""
    # C
    compare_005.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_005.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_005.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_005
    links.new(domain_size_001.outputs[4], compare_005.inputs[2])

    warning_002 = nodes.new("GeometryNodeWarning")
    warning_002.name = "Warning.002"
    warning_002.label = ""
    warning_002.location = (961.55419921875, -203.19677734375)
    warning_002.bl_label = "Warning"
    warning_002.warning_type = "ERROR"
    # Message
    warning_002.inputs[1].default_value = "No Curve Selected"
    # Links for warning_002
    links.new(compare_005.outputs[0], warning_002.inputs[0])
    links.new(warning_002.outputs[0], switch_027.inputs[0])

    randomize_transforms = nodes.new("GeometryNodeGroup")
    randomize_transforms.name = "Randomize Instance Transforms"
    randomize_transforms.label = ""
    randomize_transforms.location = (1109.6446533203125, -216.03863525390625)
    randomize_transforms.node_tree = create_randomize__transforms_group()
    randomize_transforms.bl_label = "Group"
    # Local Space
    randomize_transforms.inputs[2].default_value = True
    # Links for randomize_transforms
    links.new(randomize_transforms.outputs[0], switch_003.inputs[2])
    links.new(group_input_021.outputs[27], randomize_transforms.inputs[5])
    links.new(group_input_021.outputs[26], randomize_transforms.inputs[4])
    links.new(group_input_021.outputs[28], randomize_transforms.inputs[6])
    links.new(group_input_021.outputs[29], randomize_transforms.inputs[7])
    links.new(group_input_021.outputs[33], randomize_transforms.inputs[9])
    links.new(group_input_021.outputs[25], randomize_transforms.inputs[3])
    links.new(group_input_021.outputs[30], randomize_transforms.inputs[8])

    reroute_056 = nodes.new("NodeReroute")
    reroute_056.name = "Reroute.056"
    reroute_056.label = ""
    reroute_056.location = (1009.6446533203125, -116.03865814208984)
    reroute_056.bl_label = "Reroute"
    reroute_056.socket_idname = "NodeSocketGeometry"
    # Links for reroute_056
    links.new(reroute_056.outputs[0], switch_003.inputs[1])
    links.new(reroute_056.outputs[0], randomize_transforms.inputs[0])

    compare_006 = nodes.new("FunctionNodeCompare")
    compare_006.name = "Compare.006"
    compare_006.label = ""
    compare_006.location = (409.64453125, -356.0386962890625)
    compare_006.bl_label = "Compare"
    compare_006.operation = "NOT_EQUAL"
    compare_006.data_type = "INT"
    compare_006.mode = "ELEMENT"
    # A
    compare_006.inputs[0].default_value = 0.0
    # B
    compare_006.inputs[1].default_value = 0.0
    # A
    compare_006.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_006.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_006.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_006.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_006.inputs[8].default_value = ""
    # B
    compare_006.inputs[9].default_value = ""
    # C
    compare_006.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_006.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_006.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_006
    links.new(index_003.outputs[0], compare_006.inputs[2])

    switch_028 = nodes.new("GeometryNodeSwitch")
    switch_028.name = "Switch.028"
    switch_028.label = ""
    switch_028.location = (789.64453125, -176.0386962890625)
    switch_028.bl_label = "Switch"
    switch_028.input_type = "BOOLEAN"
    # Links for switch_028
    links.new(switch_028.outputs[0], randomize_transforms.inputs[1])
    links.new(switch_004.outputs[0], switch_028.inputs[1])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.label = ""
    boolean_math_001.location = (609.64453125, -256.0387268066406)
    boolean_math_001.bl_label = "Boolean Math"
    boolean_math_001.operation = "AND"
    # Links for boolean_math_001
    links.new(switch_004.outputs[0], boolean_math_001.inputs[0])
    links.new(compare_006.outputs[0], boolean_math_001.inputs[1])
    links.new(boolean_math_001.outputs[0], switch_028.inputs[2])

    group_input_070 = nodes.new("NodeGroupInput")
    group_input_070.name = "Group Input.070"
    group_input_070.label = ""
    group_input_070.location = (189.6446533203125, -156.03875732421875)
    group_input_070.bl_label = "Group Input"
    # Links for group_input_070
    links.new(group_input_070.outputs[31], switch_004.inputs[0])
    links.new(group_input_070.outputs[32], switch_028.inputs[0])

    domain_size_002 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_002.name = "Domain Size.002"
    domain_size_002.label = ""
    domain_size_002.location = (49.64453125, -456.03875732421875)
    domain_size_002.bl_label = "Domain Size"
    domain_size_002.component = "INSTANCES"
    # Links for domain_size_002

    integer_math_012 = nodes.new("FunctionNodeIntegerMath")
    integer_math_012.name = "Integer Math.012"
    integer_math_012.label = ""
    integer_math_012.location = (229.64453125, -436.03863525390625)
    integer_math_012.bl_label = "Integer Math"
    integer_math_012.operation = "SUBTRACT"
    # Value
    integer_math_012.inputs[1].default_value = 1
    # Value
    integer_math_012.inputs[2].default_value = 0
    # Links for integer_math_012
    links.new(domain_size_002.outputs[5], integer_math_012.inputs[0])
    links.new(integer_math_012.outputs[0], compare_006.inputs[3])

    reroute_013 = nodes.new("NodeReroute")
    reroute_013.name = "Reroute.013"
    reroute_013.label = ""
    reroute_013.location = (967.2447509765625, -210.18417358398438)
    reroute_013.bl_label = "Reroute"
    reroute_013.socket_idname = "NodeSocketGeometry"
    # Links for reroute_013
    links.new(reroute_013.outputs[0], reroute_056.inputs[0])
    links.new(reroute_013.outputs[0], domain_size_002.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (29.87474822998047, -175.72549438476562)
    random_value.bl_label = "Random Value"
    random_value.data_type = "FLOAT_VECTOR"
    # Min
    random_value.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value.inputs[2].default_value = 0.0
    # Max
    random_value.inputs[3].default_value = 1.0
    # Min
    random_value.inputs[4].default_value = 0
    # Max
    random_value.inputs[5].default_value = 100
    # Probability
    random_value.inputs[6].default_value = 0.5
    # ID
    random_value.inputs[7].default_value = 0
    # Links for random_value

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (449.8747863769531, -55.72554016113281)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "FLOAT_VECTOR"
    store_named_attribute.domain = "INSTANCE"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "instance_random"
    # Links for store_named_attribute

    group_input_071 = nodes.new("NodeGroupInput")
    group_input_071.name = "Group Input.071"
    group_input_071.label = ""
    group_input_071.location = (-492.75537109375, -570.1841430664062)
    group_input_071.bl_label = "Group Input"
    # Links for group_input_071

    hash_value = nodes.new("FunctionNodeHashValue")
    hash_value.name = "Hash Value"
    hash_value.label = ""
    hash_value.location = (-292.75531005859375, -550.1842041015625)
    hash_value.bl_label = "Hash Value"
    hash_value.data_type = "INT"
    # Seed
    hash_value.inputs[1].default_value = 1000
    # Links for hash_value
    links.new(hash_value.outputs[0], random_value.inputs[8])
    links.new(group_input_071.outputs[33], hash_value.inputs[0])

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.label = ""
    capture_attribute.location = (258.0067138671875, -76.19324493408203)
    capture_attribute.bl_label = "Capture Attribute"
    capture_attribute.active_index = 1
    capture_attribute.domain = "INSTANCE"
    # Links for capture_attribute
    links.new(capture_attribute.outputs[0], store_named_attribute.inputs[0])
    links.new(index_switch_009.outputs[0], capture_attribute.inputs[0])
    links.new(random_value.outputs[0], capture_attribute.inputs[1])
    links.new(capture_attribute.outputs[1], store_named_attribute.inputs[3])

    index_011 = nodes.new("GeometryNodeInputIndex")
    index_011.name = "Index.011"
    index_011.label = ""
    index_011.location = (29.4859561920166, -482.1629333496094)
    index_011.bl_label = "Index"
    # Links for index_011
    links.new(index_011.outputs[0], capture_attribute.inputs[2])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (649.8748168945312, -55.72554016113281)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "INT"
    store_named_attribute_001.domain = "INSTANCE"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "instance_index"
    # Links for store_named_attribute_001
    links.new(store_named_attribute_001.outputs[0], reroute_013.inputs[0])
    links.new(store_named_attribute.outputs[0], store_named_attribute_001.inputs[0])
    links.new(capture_attribute.outputs[2], store_named_attribute_001.inputs[3])

    integer_math_013 = nodes.new("FunctionNodeIntegerMath")
    integer_math_013.name = "Integer Math.013"
    integer_math_013.label = ""
    integer_math_013.location = (736.6767578125, -148.47503662109375)
    integer_math_013.bl_label = "Integer Math"
    integer_math_013.operation = "ADD"
    # Value
    integer_math_013.inputs[2].default_value = 0
    # Links for integer_math_013
    links.new(integer_math_013.outputs[0], switch_024.inputs[1])
    links.new(float_to_integer_001.outputs[0], integer_math_013.inputs[0])

    reroute_020 = nodes.new("NodeReroute")
    reroute_020.name = "Reroute.020"
    reroute_020.label = ""
    reroute_020.location = (629.35302734375, -348.4750671386719)
    reroute_020.bl_label = "Reroute"
    reroute_020.socket_idname = "NodeSocketInt"
    # Links for reroute_020
    links.new(reroute_020.outputs[0], reroute_032.inputs[0])
    links.new(reroute_020.outputs[0], integer_math_013.inputs[1])
    links.new(reroute_031.outputs[0], reroute_020.inputs[0])

    dial_gizmo_001 = nodes.new("GeometryNodeGizmoDial")
    dial_gizmo_001.name = "Dial Gizmo.001"
    dial_gizmo_001.label = ""
    dial_gizmo_001.location = (620.177734375, -895.154296875)
    dial_gizmo_001.bl_label = "Dial Gizmo"
    dial_gizmo_001.color_id = "PRIMARY"
    # Position
    dial_gizmo_001.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Up
    dial_gizmo_001.inputs[2].default_value = Vector((0.0, 0.0, 1.0))
    # Screen Space
    dial_gizmo_001.inputs[3].default_value = True
    # Radius
    dial_gizmo_001.inputs[4].default_value = 0.800000011920929
    # Links for dial_gizmo_001
    links.new(group_input_055.outputs[5], dial_gizmo_001.inputs[0])
    links.new(dial_gizmo_001.outputs[0], switch_018.inputs[2])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.label = ""
    join_geometry_006.location = (-1130.233154296875, -1395.0440673828125)
    join_geometry_006.bl_label = "Join Geometry"
    # Links for join_geometry_006
    links.new(join_geometry_006.outputs[0], index_switch_009.inputs[3])
    links.new(switch_009.outputs[0], join_geometry_006.inputs[0])

    group_input_072 = nodes.new("NodeGroupInput")
    group_input_072.name = "Group Input.072"
    group_input_072.label = ""
    group_input_072.location = (249.2861328125, -35.802734375)
    group_input_072.bl_label = "Group Input"
    # Links for group_input_072

    linear_gizmo_004 = nodes.new("GeometryNodeGizmoLinear")
    linear_gizmo_004.name = "Linear Gizmo.004"
    linear_gizmo_004.label = ""
    linear_gizmo_004.location = (429.2861328125, -35.802734375)
    linear_gizmo_004.bl_label = "Linear Gizmo"
    linear_gizmo_004.color_id = "PRIMARY"
    linear_gizmo_004.draw_style = "CROSS"
    # Links for linear_gizmo_004
    links.new(group_input_072.outputs[3], linear_gizmo_004.inputs[0])

    reroute_043 = nodes.new("NodeReroute")
    reroute_043.name = "Reroute.043"
    reroute_043.label = ""
    reroute_043.location = (-1438.2030029296875, -2505.44482421875)
    reroute_043.bl_label = "Reroute"
    reroute_043.socket_idname = "NodeSocketGeometry"
    # Links for reroute_043
    links.new(reroute_043.outputs[0], join_geometry_006.inputs[0])

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.label = ""
    sample_curve.location = (249.2861328125, -135.802490234375)
    sample_curve.bl_label = "Sample Curve"
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = False
    sample_curve.data_type = "FLOAT"
    # Value
    sample_curve.inputs[1].default_value = 0.0
    # Factor
    sample_curve.inputs[2].default_value = 0.0
    # Length
    sample_curve.inputs[3].default_value = 0.0
    # Curve Index
    sample_curve.inputs[4].default_value = 0
    # Links for sample_curve
    links.new(sample_curve.outputs[1], linear_gizmo_004.inputs[1])
    links.new(sample_curve.outputs[2], linear_gizmo_004.inputs[2])

    group_input_073 = nodes.new("NodeGroupInput")
    group_input_073.name = "Group Input.073"
    group_input_073.label = ""
    group_input_073.location = (29.28662109375, -395.802734375)
    group_input_073.bl_label = "Group Input"
    # Links for group_input_073

    switch_029 = nodes.new("GeometryNodeSwitch")
    switch_029.name = "Switch.029"
    switch_029.label = ""
    switch_029.location = (-4085.4697265625, -2468.026123046875)
    switch_029.bl_label = "Switch"
    switch_029.input_type = "GEOMETRY"
    # Links for switch_029
    links.new(switch_029.outputs[0], reroute_043.inputs[0])
    links.new(linear_gizmo_004.outputs[0], switch_029.inputs[1])

    reroute_055 = nodes.new("NodeReroute")
    reroute_055.name = "Reroute.055"
    reroute_055.label = ""
    reroute_055.location = (-5106.22216796875, -2493.9140625)
    reroute_055.bl_label = "Reroute"
    reroute_055.socket_idname = "NodeSocketInt"
    # Links for reroute_055
    links.new(reroute_055.outputs[0], switch_029.inputs[0])
    links.new(reroute_046.outputs[0], reroute_055.inputs[0])

    linear_gizmo_005 = nodes.new("GeometryNodeGizmoLinear")
    linear_gizmo_005.name = "Linear Gizmo.005"
    linear_gizmo_005.label = ""
    linear_gizmo_005.location = (429.2861328125, -235.802734375)
    linear_gizmo_005.bl_label = "Linear Gizmo"
    linear_gizmo_005.color_id = "PRIMARY"
    linear_gizmo_005.draw_style = "CROSS"
    # Links for linear_gizmo_005
    links.new(group_input_073.outputs[4], linear_gizmo_005.inputs[0])
    links.new(linear_gizmo_005.outputs[0], switch_029.inputs[2])

    sample_curve_001 = nodes.new("GeometryNodeSampleCurve")
    sample_curve_001.name = "Sample Curve.001"
    sample_curve_001.label = ""
    sample_curve_001.location = (269.28564453125, -375.802734375)
    sample_curve_001.bl_label = "Sample Curve"
    sample_curve_001.mode = "LENGTH"
    sample_curve_001.use_all_curves = False
    sample_curve_001.data_type = "FLOAT"
    # Value
    sample_curve_001.inputs[1].default_value = 0.0
    # Factor
    sample_curve_001.inputs[2].default_value = 0.0
    # Curve Index
    sample_curve_001.inputs[4].default_value = 0
    # Links for sample_curve_001
    links.new(sample_curve_001.outputs[1], linear_gizmo_005.inputs[1])
    links.new(sample_curve_001.outputs[2], linear_gizmo_005.inputs[2])
    links.new(group_input_073.outputs[4], sample_curve_001.inputs[3])

    reroute_058 = nodes.new("NodeReroute")
    reroute_058.name = "Reroute.058"
    reroute_058.label = ""
    reroute_058.location = (953.4921875, -691.0145263671875)
    reroute_058.bl_label = "Reroute"
    reroute_058.socket_idname = "NodeSocketGeometry"
    # Links for reroute_058
    links.new(switch_006.outputs[0], reroute_058.inputs[0])

    reroute_059 = nodes.new("NodeReroute")
    reroute_059.name = "Reroute.059"
    reroute_059.label = ""
    reroute_059.location = (51.146484375, -189.2490234375)
    reroute_059.bl_label = "Reroute"
    reroute_059.socket_idname = "NodeSocketGeometry"
    # Links for reroute_059
    links.new(reroute_059.outputs[0], sample_curve.inputs[0])
    links.new(reroute_059.outputs[0], sample_curve_001.inputs[0])
    links.new(reroute_058.outputs[0], reroute_059.inputs[0])

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Curve Gizmos"
    frame_003.location = (-5010.54541015625, -2538.218017578125)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    reroute_060 = nodes.new("NodeReroute")
    reroute_060.name = "Reroute.060"
    reroute_060.label = ""
    reroute_060.location = (1066.25341796875, -59.30420684814453)
    reroute_060.bl_label = "Reroute"
    reroute_060.socket_idname = "NodeSocketInt"
    # Links for reroute_060
    links.new(reroute_060.outputs[0], switch_017.inputs[0])
    links.new(reroute_049.outputs[0], reroute_060.inputs[0])

    reroute_057 = nodes.new("NodeReroute")
    reroute_057.name = "Reroute.057"
    reroute_057.label = ""
    reroute_057.location = (1169.28759765625, -960.7999877929688)
    reroute_057.bl_label = "Reroute"
    reroute_057.socket_idname = "NodeSocketRotation"
    # Links for reroute_057
    links.new(reroute_057.outputs[0], transform_gizmo_001.inputs[2])
    links.new(reroute_057.outputs[0], transform_gizmo_002.inputs[2])
    links.new(reroute_008.outputs[0], reroute_057.inputs[0])

    reroute_061 = nodes.new("NodeReroute")
    reroute_061.name = "Reroute.061"
    reroute_061.label = ""
    reroute_061.location = (369.592529296875, -195.68154907226562)
    reroute_061.bl_label = "Reroute"
    reroute_061.socket_idname = "NodeSocketVectorXYZ"
    # Links for reroute_061
    links.new(reroute_061.outputs[0], mix_001.inputs[5])
    links.new(reroute_061.outputs[0], index_switch_011.inputs[3])
    links.new(group_input_014.outputs[12], reroute_061.inputs[0])

    group_input_019 = nodes.new("NodeGroupInput")
    group_input_019.name = "Group Input.019"
    group_input_019.label = ""
    group_input_019.location = (294.3642578125, -35.986572265625)
    group_input_019.bl_label = "Group Input"
    # Links for group_input_019
    links.new(group_input_019.outputs[3], points.inputs[0])

    reroute_063 = nodes.new("NodeReroute")
    reroute_063.name = "Reroute.063"
    reroute_063.label = ""
    reroute_063.location = (614.364013671875, -634.2567749023438)
    reroute_063.bl_label = "Reroute"
    reroute_063.socket_idname = "NodeSocketInt"
    # Links for reroute_063
    links.new(reroute_063.outputs[0], index_switch_011.inputs[0])
    links.new(reroute_063.outputs[0], index_switch_007.inputs[0])
    links.new(reroute_012.outputs[0], reroute_063.inputs[0])

    reroute_064 = nodes.new("NodeReroute")
    reroute_064.name = "Reroute.064"
    reroute_064.label = ""
    reroute_064.location = (229.2724609375, -135.81060791015625)
    reroute_064.bl_label = "Reroute"
    reroute_064.socket_idname = "NodeSocketRotation"
    # Links for reroute_064
    links.new(reroute_064.outputs[0], mix_003.inputs[9])
    links.new(reroute_064.outputs[0], reroute_019.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Line Gismoz"
    frame.location = (-7244.29052734375, 1023.6468505859375)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Merge Instances"
    frame_004.location = (2956.2080078125, -74.50908660888672)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    frame_008 = nodes.new("NodeFrame")
    frame_008.name = "Frame.008"
    frame_008.label = "Store Info"
    frame_008.location = (-57.818180084228516, -71.09090423583984)
    frame_008.bl_label = "Frame"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20
    # Links for frame_008

    reroute_065 = nodes.new("NodeReroute")
    reroute_065.name = "Reroute.065"
    reroute_065.label = ""
    reroute_065.location = (411.03662109375, -315.675048828125)
    reroute_065.bl_label = "Reroute"
    reroute_065.socket_idname = "NodeSocketGeometry"
    # Links for reroute_065
    links.new(reroute_065.outputs[0], merge_by_distance.inputs[0])
    links.new(reroute_065.outputs[0], switch_008.inputs[1])
    links.new(realize_instances_002.outputs[0], reroute_065.inputs[0])

    group_input_020 = nodes.new("NodeGroupInput")
    group_input_020.name = "Group Input.020"
    group_input_020.label = ""
    group_input_020.location = (29.2724609375, -95.8106689453125)
    group_input_020.bl_label = "Group Input"
    # Links for group_input_020
    links.new(group_input_020.outputs[11], reroute_064.inputs[0])

    frame_009 = nodes.new("NodeFrame")
    frame_009.name = "Frame.009"
    frame_009.label = "Scale"
    frame_009.location = (115.91943359375, -643.3090209960938)
    frame_009.bl_label = "Frame"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20
    # Links for frame_009

    frame_011 = nodes.new("NodeFrame")
    frame_011.name = "Frame.011"
    frame_011.label = "Position"
    frame_011.location = (202.371337890625, -35.890869140625)
    frame_011.bl_label = "Frame"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20
    # Links for frame_011

    frame_014 = nodes.new("NodeFrame")
    frame_014.name = "Frame.014"
    frame_014.label = "Rotation"
    frame_014.location = (194.028564453125, -377.5635986328125)
    frame_014.bl_label = "Frame"
    frame_014.text = None
    frame_014.shrink = True
    frame_014.label_size = 20
    # Links for frame_014

    reroute_062 = nodes.new("NodeReroute")
    reroute_062.name = "Reroute.062"
    reroute_062.label = ""
    reroute_062.location = (3069.353515625, -508.47503662109375)
    reroute_062.bl_label = "Reroute"
    reroute_062.socket_idname = "NodeSocketRotation"
    # Links for reroute_062
    links.new(reroute_062.outputs[0], transform_geometry_001.inputs[5])
    links.new(reroute_062.outputs[0], rotate_rotation.inputs[1])
    links.new(reroute_010.outputs[0], reroute_062.inputs[0])

    reroute_066 = nodes.new("NodeReroute")
    reroute_066.name = "Reroute.066"
    reroute_066.label = ""
    reroute_066.location = (1779.20166015625, -451.20733642578125)
    reroute_066.bl_label = "Reroute"
    reroute_066.socket_idname = "NodeSocketVector"
    # Links for reroute_066
    links.new(reroute_066.outputs[0], linear_gizmo.inputs[2])
    links.new(reroute_001.outputs[0], reroute_066.inputs[0])
    links.new(reroute_066.outputs[0], reroute_015.inputs[0])

    reroute_038 = nodes.new("NodeReroute")
    reroute_038.name = "Reroute.038"
    reroute_038.label = ""
    reroute_038.location = (960.072509765625, -456.181884765625)
    reroute_038.bl_label = "Reroute"
    reroute_038.socket_idname = "NodeSocketInt"
    # Links for reroute_038
    links.new(reroute_038.outputs[0], sample_curve_003.inputs[4])
    links.new(reroute_038.outputs[0], hash_value_001.inputs[0])

    reroute_045 = nodes.new("NodeReroute")
    reroute_045.name = "Reroute.045"
    reroute_045.label = ""
    reroute_045.location = (580.07275390625, -456.181884765625)
    reroute_045.bl_label = "Reroute"
    reroute_045.socket_idname = "NodeSocketInt"
    # Links for reroute_045
    links.new(reroute_045.outputs[0], reroute_038.inputs[0])
    links.new(reroute_045.outputs[0], integer_math_008.inputs[0])
    links.new(reroute_040.outputs[0], reroute_045.inputs[0])

    reroute_067 = nodes.new("NodeReroute")
    reroute_067.name = "Reroute.067"
    reroute_067.label = ""
    reroute_067.location = (760.072265625, -356.181884765625)
    reroute_067.bl_label = "Reroute"
    reroute_067.socket_idname = "NodeSocketInt"
    # Links for reroute_067
    links.new(reroute_067.outputs[0], integer_math_009.inputs[0])
    links.new(reroute_067.outputs[0], math_010.inputs[0])
    links.new(reroute_039.outputs[0], reroute_067.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_curve_rot_curve_group():
    group_name = "CurveRotCurve"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Viewer", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Curve", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Curve", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="RadialResolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="CurveResolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="MaxResolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 200
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="CommonAxis", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1987.56591796875, -93.78033447265625)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1697.4375, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    integer = nodes.new("FunctionNodeInputInt")
    integer.name = "Integer"
    integer.label = "Resolution"
    integer.location = (-1497.4375, 81.73336791992188)
    integer.bl_label = "Integer"
    integer.integer = 200
    # Links for integer

    rotate_and_mix_curves_spherical = nodes.new("GeometryNodeGroup")
    rotate_and_mix_curves_spherical.name = "Group.013"
    rotate_and_mix_curves_spherical.label = ""
    rotate_and_mix_curves_spherical.location = (916.282470703125, 217.06454467773438)
    rotate_and_mix_curves_spherical.node_tree = create_rotate_and_mix_curves_spherical_group()
    rotate_and_mix_curves_spherical.bl_label = "Group"
    # Links for rotate_and_mix_curves_spherical
    links.new(group_input.outputs[5], rotate_and_mix_curves_spherical.inputs[4])

    array = nodes.new("GeometryNodeGroup")
    array.name = "Array"
    array.label = ""
    array.location = (-343.26629638671875, 116.6800537109375)
    array.node_tree = create_array_group()
    array.bl_label = "Group"
    # Shape
    array.inputs[1].default_value = "Line"
    # Count Method
    array.inputs[2].default_value = "Count"
    # Distance
    array.inputs[4].default_value = 1.0
    # Angular Distance
    array.inputs[5].default_value = 0.7853981852531433
    # Per Curve
    array.inputs[6].default_value = True
    # Offset Method
    array.inputs[7].default_value = "Relative"
    # Transform Reference
    array.inputs[8].default_value = "Inputs"
    # Translation
    array.inputs[9].default_value = Vector((1.0, 0.0, 0.0))
    # Offset
    array.inputs[10].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    array.inputs[11].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    array.inputs[12].default_value = Vector((1.0, 1.0, 1.0))
    # Central Axis
    array.inputs[13].default_value = "Z"
    # Circle Segment
    array.inputs[14].default_value = "Full"
    # Sweep Angle
    array.inputs[15].default_value = 3.1415927410125732
    # Radius
    array.inputs[16].default_value = 0.0
    # Relative Space
    array.inputs[19].default_value = True
    # Realize Instances
    array.inputs[20].default_value = False
    # Align Rotation
    array.inputs[21].default_value = True
    # Forward Axis
    array.inputs[22].default_value = "X"
    # Up Axis
    array.inputs[23].default_value = "Z"
    # Randomize
    array.inputs[24].default_value = False
    # Randomize Offset
    array.inputs[25].default_value = Vector((0.0, 0.0, 0.0))
    # Randomize Rotation
    array.inputs[26].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Randomize Scale Axes
    array.inputs[27].default_value = "Uniform"
    # Randomize Scale
    array.inputs[28].default_value = Vector((0.0, 0.0, 0.0))
    # Randomize Scale
    array.inputs[29].default_value = 0.0
    # Randomize Flipping
    array.inputs[30].default_value = [0.0, 0.0, 0.0]
    # Exclude First
    array.inputs[31].default_value = True
    # Exclude Last
    array.inputs[32].default_value = False
    # Seed
    array.inputs[33].default_value = 0
    # Merge
    array.inputs[34].default_value = False
    # Merge Distance
    array.inputs[35].default_value = 0.0010000000474974513
    # Links for array

    for_each_geometry_element_input = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input.name = "For Each Geometry Element Input"
    for_each_geometry_element_input.label = ""
    for_each_geometry_element_input.location = (-100.9344482421875, 185.35916137695312)
    for_each_geometry_element_input.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input.inputs[1].default_value = True
    # Links for for_each_geometry_element_input
    links.new(array.outputs[0], for_each_geometry_element_input.inputs[0])

    for_each_geometry_element_output = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.name = "For Each Geometry Element Output"
    for_each_geometry_element_output.label = ""
    for_each_geometry_element_output.location = (1497.4375, 196.72348022460938)
    for_each_geometry_element_output.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output.active_input_index = 0
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = "INSTANCE"
    for_each_geometry_element_output.inspection_index = 0
    # Links for for_each_geometry_element_output
    links.new(for_each_geometry_element_output.outputs[2], group_output.inputs[0])

    set_i_d = nodes.new("GeometryNodeSetID")
    set_i_d.name = "Set ID"
    set_i_d.label = ""
    set_i_d.location = (-631.3878173828125, 4.195404052734375)
    set_i_d.bl_label = "Set ID"
    # Selection
    set_i_d.inputs[1].default_value = True
    # Links for set_i_d

    integer_001 = nodes.new("FunctionNodeInputInt")
    integer_001.name = "Integer.001"
    integer_001.label = ""
    integer_001.location = (-791.35986328125, -93.02761840820312)
    integer_001.bl_label = "Integer"
    integer_001.integer = 1
    # Links for integer_001
    links.new(integer_001.outputs[0], set_i_d.inputs[2])

    set_i_d_001 = nodes.new("GeometryNodeSetID")
    set_i_d_001.name = "Set ID.001"
    set_i_d_001.label = ""
    set_i_d_001.location = (-624.912109375, 236.28732299804688)
    set_i_d_001.bl_label = "Set ID"
    # Selection
    set_i_d_001.inputs[1].default_value = True
    # Links for set_i_d_001

    integer_002 = nodes.new("FunctionNodeInputInt")
    integer_002.name = "Integer.002"
    integer_002.label = ""
    integer_002.location = (-827.4935302734375, 199.17074584960938)
    integer_002.bl_label = "Integer"
    integer_002.integer = 0
    # Links for integer_002
    links.new(integer_002.outputs[0], set_i_d_001.inputs[2])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (-539.7406005859375, 103.16818237304688)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(set_i_d_001.outputs[0], join_geometry.inputs[0])
    links.new(set_i_d.outputs[0], join_geometry.inputs[0])
    links.new(join_geometry.outputs[0], array.inputs[0])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.name = "Separate Geometry.001"
    separate_geometry_001.label = ""
    separate_geometry_001.location = (378.94476318359375, 199.10952758789062)
    separate_geometry_001.bl_label = "Separate Geometry"
    separate_geometry_001.domain = "POINT"
    # Links for separate_geometry_001
    links.new(separate_geometry_001.outputs[0], rotate_and_mix_curves_spherical.inputs[0])
    links.new(separate_geometry_001.outputs[1], rotate_and_mix_curves_spherical.inputs[1])

    i_d = nodes.new("GeometryNodeInputID")
    i_d.name = "ID"
    i_d.label = ""
    i_d.location = (-28.7838134765625, -137.00949096679688)
    i_d.bl_label = "ID"
    # Links for i_d

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (175.2350616455078, -118.32120513916016)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "INT"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Links for sample_index
    links.new(i_d.outputs[0], sample_index.inputs[1])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (410.58831787109375, -30.744903564453125)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    # A
    compare.inputs[0].default_value = 0.0
    # B
    compare.inputs[1].default_value = 0.0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
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
    links.new(sample_index.outputs[0], compare.inputs[2])
    links.new(compare.outputs[0], separate_geometry_001.inputs[1])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (70.38412475585938, 55.29754638671875)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(realize_instances.outputs[0], sample_index.inputs[0])
    links.new(for_each_geometry_element_input.outputs[1], realize_instances.inputs[0])
    links.new(realize_instances.outputs[0], separate_geometry_001.inputs[0])

    index_002 = nodes.new("GeometryNodeInputIndex")
    index_002.name = "Index.002"
    index_002.label = ""
    index_002.location = (-58.38916015625, -214.83999633789062)
    index_002.bl_label = "Index"
    # Links for index_002
    links.new(index_002.outputs[0], sample_index.inputs[2])
    links.new(index_002.outputs[0], rotate_and_mix_curves_spherical.inputs[2])

    integer_003 = nodes.new("FunctionNodeInputInt")
    integer_003.name = "Integer.003"
    integer_003.label = ""
    integer_003.location = (-1496.6368408203125, -99.1761703491211)
    integer_003.bl_label = "Integer"
    integer_003.integer = 50
    # Links for integer_003

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (737.6185913085938, -139.45150756835938)
    math_001.bl_label = "Math"
    math_001.operation = "DIVIDE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(for_each_geometry_element_input.outputs[0], math_001.inputs[0])
    links.new(math_001.outputs[0], rotate_and_mix_curves_spherical.inputs[3])

    geometry_to_instance = nodes.new("GeometryNodeGeometryToInstance")
    geometry_to_instance.name = "Geometry to Instance"
    geometry_to_instance.label = ""
    geometry_to_instance.location = (1090.9283447265625, 14.555145263671875)
    geometry_to_instance.bl_label = "Geometry to Instance"
    # Links for geometry_to_instance
    links.new(geometry_to_instance.outputs[0], for_each_geometry_element_output.inputs[1])
    links.new(rotate_and_mix_curves_spherical.outputs[0], geometry_to_instance.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (-288.951416015625, -429.4346008300781)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketInt"
    # Links for reroute
    links.new(reroute.outputs[0], array.inputs[3])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (-861.0582275390625, -284.5886535644531)
    compare_005.bl_label = "Compare"
    compare_005.operation = "GREATER_THAN"
    compare_005.data_type = "INT"
    compare_005.mode = "ELEMENT"
    # A
    compare_005.inputs[0].default_value = 0.0
    # B
    compare_005.inputs[1].default_value = 0.0
    # A
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_005.inputs[8].default_value = ""
    # B
    compare_005.inputs[9].default_value = ""
    # C
    compare_005.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_005.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_005.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_005
    links.new(group_input.outputs[4], compare_005.inputs[3])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (-566.685302734375, -284.8795471191406)
    switch.bl_label = "Switch"
    switch.input_type = "INT"
    # Links for switch
    links.new(compare_005.outputs[0], switch.inputs[0])
    links.new(switch.outputs[0], reroute.inputs[0])
    links.new(group_input.outputs[4], switch.inputs[2])

    integer_math_006 = nodes.new("FunctionNodeIntegerMath")
    integer_math_006.name = "Integer Math.006"
    integer_math_006.label = ""
    integer_math_006.location = (365.0740966796875, -447.3934020996094)
    integer_math_006.bl_label = "Integer Math"
    integer_math_006.operation = "SUBTRACT"
    # Value
    integer_math_006.inputs[1].default_value = 1
    # Value
    integer_math_006.inputs[2].default_value = 0
    # Links for integer_math_006
    links.new(reroute.outputs[0], integer_math_006.inputs[0])
    links.new(integer_math_006.outputs[0], math_001.inputs[1])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (-1265.78271484375, 61.342132568359375)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketInt"
    # Links for reroute_001
    links.new(group_input.outputs[3], reroute_001.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (-1272.8016357421875, -37.900665283203125)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketInt"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], compare_005.inputs[2])
    links.new(reroute_002.outputs[0], switch.inputs[1])
    links.new(group_input.outputs[2], reroute_002.inputs[0])

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (-1075.404541015625, 396.4331970214844)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "COUNT"
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points
    links.new(group_input.outputs[1], curve_to_points.inputs[0])
    links.new(reroute_001.outputs[0], curve_to_points.inputs[1])
    links.new(curve_to_points.outputs[0], set_i_d_001.inputs[0])

    curve_to_points_001 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.name = "Curve to Points.001"
    curve_to_points_001.label = ""
    curve_to_points_001.location = (-1037.73046875, 129.55474853515625)
    curve_to_points_001.bl_label = "Curve to Points"
    curve_to_points_001.mode = "COUNT"
    # Length
    curve_to_points_001.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points_001
    links.new(group_input.outputs[0], curve_to_points_001.inputs[0])
    links.new(curve_to_points_001.outputs[0], set_i_d.inputs[0])
    links.new(reroute_001.outputs[0], curve_to_points_001.inputs[1])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (1679.3056640625, -144.93875122070312)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(group_input.outputs[0], join_geometry_001.inputs[0])
    links.new(group_input.outputs[1], join_geometry_001.inputs[0])
    links.new(for_each_geometry_element_output.outputs[2], join_geometry_001.inputs[0])

    set_point_radius = nodes.new("GeometryNodeSetPointRadius")
    set_point_radius.name = "Set Point Radius"
    set_point_radius.label = ""
    set_point_radius.location = (1782.3404541015625, -285.6394958496094)
    set_point_radius.bl_label = "Set Point Radius"
    # Selection
    set_point_radius.inputs[1].default_value = True
    # Radius
    set_point_radius.inputs[2].default_value = 0.009999999776482582
    # Links for set_point_radius
    links.new(join_geometry_001.outputs[0], set_point_radius.inputs[0])
    links.new(set_point_radius.outputs[0], group_output.inputs[1])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_get_axis_group():
    group_name = "GetAxis"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Min", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Max", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Axis-", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Axis+", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Axis", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1329.6693115234375, -109.89600372314453)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-510.5210876464844, 41.84991455078125)
    group_input.bl_label = "Group Input"
    # Links for group_input

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.label = ""
    attribute_statistic.location = (110.9979248046875, -47.66653060913086)
    attribute_statistic.bl_label = "Attribute Statistic"
    attribute_statistic.data_type = "FLOAT"
    attribute_statistic.domain = "POINT"
    # Selection
    attribute_statistic.inputs[1].default_value = True
    # Links for attribute_statistic
    links.new(group_input.outputs[0], attribute_statistic.inputs[0])

    attribute_statistic_001 = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_001.name = "Attribute Statistic.001"
    attribute_statistic_001.label = ""
    attribute_statistic_001.location = (450.7173767089844, 116.67169952392578)
    attribute_statistic_001.bl_label = "Attribute Statistic"
    attribute_statistic_001.data_type = "FLOAT"
    attribute_statistic_001.domain = "POINT"
    # Links for attribute_statistic_001
    links.new(group_input.outputs[0], attribute_statistic_001.inputs[0])
    links.new(attribute_statistic_001.outputs[3], group_output.inputs[0])
    links.new(attribute_statistic_001.outputs[4], group_output.inputs[1])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (273.19451904296875, 103.14662170410156)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
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
    links.new(attribute_statistic.outputs[3], compare.inputs[1])
    links.new(compare.outputs[0], attribute_statistic_001.inputs[1])

    index_003 = nodes.new("GeometryNodeInputIndex")
    index_003.name = "Index.003"
    index_003.label = ""
    index_003.location = (-294.9983825683594, 127.65331268310547)
    index_003.bl_label = "Index"
    # Links for index_003
    links.new(index_003.outputs[0], attribute_statistic_001.inputs[2])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (-428.8205261230469, -303.5053405761719)
    position.bl_label = "Position"
    # Links for position

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (-150.57200622558594, -303.66998291015625)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Links for sample_index
    links.new(position.outputs[0], sample_index.inputs[1])
    links.new(group_input.outputs[1], sample_index.inputs[0])
    links.new(index_003.outputs[0], sample_index.inputs[2])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (-147.74578857421875, -523.8267211914062)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001
    links.new(position.outputs[0], sample_index_001.inputs[1])
    links.new(index_003.outputs[0], sample_index_001.inputs[2])
    links.new(group_input.outputs[0], sample_index_001.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (33.23517608642578, -389.9391784667969)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "DISTANCE"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(sample_index_001.outputs[0], vector_math.inputs[0])
    links.new(sample_index.outputs[0], vector_math.inputs[1])
    links.new(vector_math.outputs[1], attribute_statistic.inputs[2])
    links.new(vector_math.outputs[1], compare.inputs[0])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.label = ""
    sample_index_002.location = (757.2284545898438, -137.4542236328125)
    sample_index_002.bl_label = "Sample Index"
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    # Links for sample_index_002
    links.new(position.outputs[0], sample_index_002.inputs[1])
    links.new(group_input.outputs[0], sample_index_002.inputs[0])
    links.new(sample_index_002.outputs[0], group_output.inputs[2])
    links.new(attribute_statistic_001.outputs[3], sample_index_002.inputs[2])

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.name = "Sample Index.003"
    sample_index_003.label = ""
    sample_index_003.location = (762.39208984375, -341.701171875)
    sample_index_003.bl_label = "Sample Index"
    sample_index_003.data_type = "FLOAT_VECTOR"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    # Links for sample_index_003
    links.new(attribute_statistic_001.outputs[4], sample_index_003.inputs[2])
    links.new(group_input.outputs[0], sample_index_003.inputs[0])
    links.new(sample_index_003.outputs[0], group_output.inputs[3])
    links.new(position.outputs[0], sample_index_003.inputs[1])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (970.4724731445312, -347.58306884765625)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "SUBTRACT"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(sample_index_002.outputs[0], vector_math_001.inputs[0])
    links.new(sample_index_003.outputs[0], vector_math_001.inputs[1])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (1149.999755859375, -308.7816162109375)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "NORMALIZE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], group_output.inputs[4])
    links.new(vector_math_001.outputs[0], vector_math_002.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_orient_curve_group():
    group_name = "OrientCurve"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="CurveA", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveB", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveA", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveB", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (571.7957763671875, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-581.7958984375, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], group_output.inputs[0])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (-179.1143798828125, 227.1519775390625)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Index
    sample_index_001.inputs[2].default_value = 0
    # Links for sample_index_001
    links.new(group_input.outputs[0], sample_index_001.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (-381.7958984375, -227.152099609375)
    position_001.bl_label = "Position"
    # Links for position_001
    links.new(position_001.outputs[0], sample_index_001.inputs[1])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (146.5411376953125, -42.9473876953125)
    compare.bl_label = "Compare"
    compare.operation = "NOT_EQUAL"
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
    links.new(sample_index_001.outputs[0], compare.inputs[4])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.label = ""
    sample_index_002.location = (-102.673583984375, -187.876220703125)
    sample_index_002.bl_label = "Sample Index"
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    # Index
    sample_index_002.inputs[2].default_value = 0
    # Links for sample_index_002
    links.new(position_001.outputs[0], sample_index_002.inputs[1])
    links.new(sample_index_002.outputs[0], compare.inputs[5])
    links.new(group_input.outputs[1], sample_index_002.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (381.7957763671875, -41.7064208984375)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(compare.outputs[0], switch.inputs[0])
    links.new(group_input.outputs[1], switch.inputs[1])
    links.new(switch.outputs[0], group_output.inputs[1])

    reverse_curve = nodes.new("GeometryNodeReverseCurve")
    reverse_curve.name = "Reverse Curve"
    reverse_curve.label = ""
    reverse_curve.location = (201.9752197265625, -181.6446533203125)
    reverse_curve.bl_label = "Reverse Curve"
    # Selection
    reverse_curve.inputs[1].default_value = True
    # Links for reverse_curve
    links.new(reverse_curve.outputs[0], switch.inputs[2])
    links.new(group_input.outputs[1], reverse_curve.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_loft_curve_parts_group():
    group_name = "LoftCurveParts"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Vertices Y", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 3
    socket.min_value = 2
    socket.max_value = 1000

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (584.2906494140625, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-594.2906494140625, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (-394.2906494140625, 30.0992431640625)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001
    links.new(group_input.outputs[0], reroute_001.inputs[0])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (-238.3514404296875, 51.01025390625)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(reroute_001.outputs[0], realize_instances.inputs[0])

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    grid.label = ""
    grid.location = (88.71722412109375, 116.20465087890625)
    grid.bl_label = "Grid"
    # Size X
    grid.inputs[0].default_value = 1.0
    # Size Y
    grid.inputs[1].default_value = 1.0
    # Links for grid
    links.new(group_input.outputs[1], grid.inputs[3])

    domain_size_002 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_002.name = "Domain Size.002"
    domain_size_002.label = ""
    domain_size_002.location = (-288.0189208984375, 261.626708984375)
    domain_size_002.bl_label = "Domain Size"
    domain_size_002.component = "INSTANCES"
    # Links for domain_size_002
    links.new(reroute_001.outputs[0], domain_size_002.inputs[0])
    links.new(domain_size_002.outputs[5], grid.inputs[2])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (137.4525146484375, -111.19189453125)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001
    links.new(realize_instances.outputs[0], sample_index_001.inputs[0])

    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.label = ""
    index_001.location = (-222.239501953125, -261.626708984375)
    index_001.bl_label = "Index"
    # Links for index_001
    links.new(index_001.outputs[0], sample_index_001.inputs[2])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (-213.8746337890625, -152.73162841796875)
    position_001.bl_label = "Position"
    # Links for position_001
    links.new(position_001.outputs[0], sample_index_001.inputs[1])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (394.2906494140625, 109.17431640625)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position
    links.new(sample_index_001.outputs[0], set_position.inputs[2])
    links.new(grid.outputs[0], set_position.inputs[0])
    links.new(set_position.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_geometry__nodes_group():
    group_name = "Geometry Nodes"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="RadialResolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 40
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="CurveResolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 96
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="MaxResolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 200
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (-3367.731689453125, 592.5940551757812)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (-2631.60498046875, 1072.0203857421875)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "CURVE"
    # Links for separate_geometry

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (-2582.13671875, 786.7550048828125)
    math_005.bl_label = "Math"
    math_005.operation = "GREATER_THAN"
    math_005.use_clamp = False
    # Value
    math_005.inputs[1].default_value = 5.960464477539063e-08
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(math_005.outputs[0], separate_geometry.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (-2798.896484375, 749.1580200195312)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], math_005.inputs[0])

    group_output_002 = nodes.new("NodeGroupOutput")
    group_output_002.name = "Group Output.002"
    group_output_002.label = ""
    group_output_002.location = (-434.3013610839844, 938.523681640625)
    group_output_002.bl_label = "Group Output"
    group_output_002.is_active_output = False
    # Links for group_output_002

    set_point_radius = nodes.new("GeometryNodeSetPointRadius")
    set_point_radius.name = "Set Point Radius"
    set_point_radius.label = ""
    set_point_radius.location = (-693.1724243164062, 933.380615234375)
    set_point_radius.bl_label = "Set Point Radius"
    # Selection
    set_point_radius.inputs[1].default_value = True
    # Radius
    set_point_radius.inputs[2].default_value = 0.009999999776482582
    # Links for set_point_radius

    viewer = nodes.new("GeometryNodeViewer")
    viewer.name = "Viewer"
    viewer.label = ""
    viewer.location = (-2405.757568359375, 494.9228210449219)
    viewer.bl_label = "Viewer"
    viewer.ui_shortcut = 0
    viewer.active_index = 0
    viewer.domain = "AUTO"
    # Links for viewer

    set_axis = nodes.new("GeometryNodeGroup")
    set_axis.name = "Group.001"
    set_axis.label = ""
    set_axis.location = (-3198.72900390625, 296.4186096191406)
    set_axis.node_tree = create_set_axis_group()
    set_axis.bl_label = "Group"
    # Name
    set_axis.inputs[2].default_value = "axis+"
    # Links for set_axis
    links.new(group_input_001.outputs[0], set_axis.inputs[0])

    set_axis_1 = nodes.new("GeometryNodeGroup")
    set_axis_1.name = "Group.002"
    set_axis_1.label = ""
    set_axis_1.location = (-2992.2392578125, 457.7334289550781)
    set_axis_1.node_tree = create_set_axis_group()
    set_axis_1.bl_label = "Group"
    # Name
    set_axis_1.inputs[2].default_value = "axis-"
    # Links for set_axis_1
    links.new(set_axis_1.outputs[0], separate_geometry.inputs[0])
    links.new(set_axis.outputs[0], set_axis_1.inputs[0])
    links.new(set_axis_1.outputs[0], viewer.inputs[0])

    viewer_001 = nodes.new("GeometryNodeViewer")
    viewer_001.name = "Viewer.001"
    viewer_001.label = ""
    viewer_001.location = (-2372.03857421875, 926.9246215820312)
    viewer_001.bl_label = "Viewer"
    viewer_001.ui_shortcut = 0
    viewer_001.active_index = 0
    viewer_001.domain = "AUTO"
    # Links for viewer_001
    links.new(separate_geometry.outputs[1], viewer_001.inputs[0])

    split_curves_about_axis = nodes.new("GeometryNodeGroup")
    split_curves_about_axis.name = "Group.003"
    split_curves_about_axis.label = ""
    split_curves_about_axis.location = (-2155.291748046875, 1151.42529296875)
    split_curves_about_axis.node_tree = create_split_curves_about_axis_group()
    split_curves_about_axis.bl_label = "Group"
    # Links for split_curves_about_axis
    links.new(separate_geometry.outputs[0], split_curves_about_axis.inputs[0])

    split_curves_about_axis_1 = nodes.new("GeometryNodeGroup")
    split_curves_about_axis_1.name = "SplitCurvesAboutAxis"
    split_curves_about_axis_1.label = ""
    split_curves_about_axis_1.location = (-2159.83837890625, 988.4376220703125)
    split_curves_about_axis_1.node_tree = create_split_curves_about_axis_group()
    split_curves_about_axis_1.bl_label = "Group"
    # Links for split_curves_about_axis_1
    links.new(separate_geometry.outputs[1], split_curves_about_axis_1.inputs[0])

    curve_rot_curve = nodes.new("GeometryNodeGroup")
    curve_rot_curve.name = "Group.006"
    curve_rot_curve.label = ""
    curve_rot_curve.location = (-1437.7447509765625, 1075.944091796875)
    curve_rot_curve.node_tree = create_curve_rot_curve_group()
    curve_rot_curve.bl_label = "Group"
    # Links for curve_rot_curve
    links.new(group_input_001.outputs[2], curve_rot_curve.inputs[3])
    links.new(curve_rot_curve.outputs[1], set_point_radius.inputs[0])
    links.new(group_input_001.outputs[3], curve_rot_curve.inputs[4])

    viewer_002 = nodes.new("GeometryNodeViewer")
    viewer_002.name = "Viewer.002"
    viewer_002.label = ""
    viewer_002.location = (-759.1332397460938, 1253.18701171875)
    viewer_002.bl_label = "Viewer"
    viewer_002.ui_shortcut = 0
    viewer_002.active_index = 0
    viewer_002.domain = "AUTO"
    # Links for viewer_002

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (-1593.529541015625, 1184.9901123046875)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(split_curves_about_axis_1.outputs[0], join_geometry.inputs[0])
    links.new(split_curves_about_axis.outputs[1], join_geometry.inputs[0])
    links.new(split_curves_about_axis.outputs[0], join_geometry.inputs[0])
    links.new(split_curves_about_axis_1.outputs[1], join_geometry.inputs[0])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (-2637.233154296875, 301.46771240234375)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Index
    sample_index.inputs[2].default_value = 0
    # Links for sample_index
    links.new(set_axis_1.outputs[0], sample_index.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (-2925.918212890625, 136.1082000732422)
    position.bl_label = "Position"
    # Links for position
    links.new(position.outputs[0], sample_index.inputs[1])

    get_axis = nodes.new("GeometryNodeGroup")
    get_axis.name = "Group.004"
    get_axis.label = ""
    get_axis.location = (-2411.719482421875, 1263.50390625)
    get_axis.node_tree = create_get_axis_group()
    get_axis.bl_label = "Group"
    # Links for get_axis
    links.new(separate_geometry.outputs[0], get_axis.inputs[0])
    links.new(separate_geometry.outputs[1], get_axis.inputs[1])
    links.new(get_axis.outputs[4], curve_rot_curve.inputs[5])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (-728.5403442382812, 1021.7056274414062)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002
    links.new(join_geometry.outputs[0], join_geometry_002.inputs[0])

    orient_curve = nodes.new("GeometryNodeGroup")
    orient_curve.name = "Group.005"
    orient_curve.label = ""
    orient_curve.location = (-1768.1240234375, 975.8150634765625)
    orient_curve.node_tree = create_orient_curve_group()
    orient_curve.bl_label = "Group"
    # Links for orient_curve
    links.new(orient_curve.outputs[1], curve_rot_curve.inputs[1])
    links.new(orient_curve.outputs[0], curve_rot_curve.inputs[0])
    links.new(split_curves_about_axis.outputs[0], orient_curve.inputs[0])
    links.new(split_curves_about_axis_1.outputs[1], orient_curve.inputs[1])

    curve_rot_curve_1 = nodes.new("GeometryNodeGroup")
    curve_rot_curve_1.name = "Group.007"
    curve_rot_curve_1.label = ""
    curve_rot_curve_1.location = (-1445.49267578125, 823.7884521484375)
    curve_rot_curve_1.node_tree = create_curve_rot_curve_group()
    curve_rot_curve_1.bl_label = "Group"
    # Links for curve_rot_curve_1
    links.new(get_axis.outputs[4], curve_rot_curve_1.inputs[5])
    links.new(group_input_001.outputs[2], curve_rot_curve_1.inputs[3])
    links.new(group_input_001.outputs[3], curve_rot_curve_1.inputs[4])

    orient_curve_1 = nodes.new("GeometryNodeGroup")
    orient_curve_1.name = "Group.008"
    orient_curve_1.label = ""
    orient_curve_1.location = (-1784.8468017578125, 794.0038452148438)
    orient_curve_1.node_tree = create_orient_curve_group()
    orient_curve_1.bl_label = "Group"
    # Links for orient_curve_1
    links.new(orient_curve_1.outputs[0], curve_rot_curve_1.inputs[0])
    links.new(orient_curve_1.outputs[1], curve_rot_curve_1.inputs[1])
    links.new(split_curves_about_axis.outputs[1], orient_curve_1.inputs[0])
    links.new(split_curves_about_axis_1.outputs[0], orient_curve_1.inputs[1])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (-1082.7420654296875, 859.3226318359375)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003
    links.new(curve_rot_curve.outputs[0], join_geometry_003.inputs[0])
    links.new(join_geometry_003.outputs[0], join_geometry_002.inputs[0])
    links.new(curve_rot_curve_1.outputs[0], join_geometry_003.inputs[0])

    curve_rot_curve_2 = nodes.new("GeometryNodeGroup")
    curve_rot_curve_2.name = "Group.009"
    curve_rot_curve_2.label = ""
    curve_rot_curve_2.location = (-1440.7147216796875, 565.4176635742188)
    curve_rot_curve_2.node_tree = create_curve_rot_curve_group()
    curve_rot_curve_2.bl_label = "Group"
    # Links for curve_rot_curve_2
    links.new(get_axis.outputs[4], curve_rot_curve_2.inputs[5])
    links.new(group_input_001.outputs[2], curve_rot_curve_2.inputs[3])
    links.new(group_input_001.outputs[3], curve_rot_curve_2.inputs[4])

    orient_curve_2 = nodes.new("GeometryNodeGroup")
    orient_curve_2.name = "Group.010"
    orient_curve_2.label = ""
    orient_curve_2.location = (-1751.2510986328125, 604.123291015625)
    orient_curve_2.node_tree = create_orient_curve_group()
    orient_curve_2.bl_label = "Group"
    # Links for orient_curve_2
    links.new(split_curves_about_axis.outputs[1], orient_curve_2.inputs[0])
    links.new(split_curves_about_axis_1.outputs[1], orient_curve_2.inputs[1])
    links.new(orient_curve_2.outputs[0], curve_rot_curve_2.inputs[0])
    links.new(orient_curve_2.outputs[1], curve_rot_curve_2.inputs[1])

    curve_rot_curve_3 = nodes.new("GeometryNodeGroup")
    curve_rot_curve_3.name = "Group.011"
    curve_rot_curve_3.label = ""
    curve_rot_curve_3.location = (-1468.1890869140625, 323.78656005859375)
    curve_rot_curve_3.node_tree = create_curve_rot_curve_group()
    curve_rot_curve_3.bl_label = "Group"
    # Links for curve_rot_curve_3
    links.new(get_axis.outputs[4], curve_rot_curve_3.inputs[5])
    links.new(group_input_001.outputs[2], curve_rot_curve_3.inputs[3])
    links.new(group_input_001.outputs[3], curve_rot_curve_3.inputs[4])

    orient_curve_3 = nodes.new("GeometryNodeGroup")
    orient_curve_3.name = "Group.012"
    orient_curve_3.label = ""
    orient_curve_3.location = (-1778.7254638671875, 362.4921875)
    orient_curve_3.node_tree = create_orient_curve_group()
    orient_curve_3.bl_label = "Group"
    # Links for orient_curve_3
    links.new(orient_curve_3.outputs[1], curve_rot_curve_3.inputs[1])
    links.new(orient_curve_3.outputs[0], curve_rot_curve_3.inputs[0])
    links.new(split_curves_about_axis_1.outputs[0], orient_curve_3.inputs[1])
    links.new(split_curves_about_axis.outputs[0], orient_curve_3.inputs[0])

    integer_math_003 = nodes.new("FunctionNodeIntegerMath")
    integer_math_003.name = "Integer Math.003"
    integer_math_003.label = ""
    integer_math_003.location = (-2437.26416015625, 654.5900268554688)
    integer_math_003.bl_label = "Integer Math"
    integer_math_003.operation = "DIVIDE_CEIL"
    # Value
    integer_math_003.inputs[1].default_value = 4
    # Value
    integer_math_003.inputs[2].default_value = 0
    # Links for integer_math_003
    links.new(integer_math_003.outputs[0], curve_rot_curve_1.inputs[2])
    links.new(group_input_001.outputs[1], integer_math_003.inputs[0])
    links.new(integer_math_003.outputs[0], curve_rot_curve.inputs[2])
    links.new(integer_math_003.outputs[0], curve_rot_curve_2.inputs[2])
    links.new(integer_math_003.outputs[0], curve_rot_curve_3.inputs[2])

    separate_components_004 = nodes.new("GeometryNodeSeparateComponents")
    separate_components_004.name = "Separate Components.004"
    separate_components_004.label = ""
    separate_components_004.location = (-1013.687744140625, 1514.2679443359375)
    separate_components_004.bl_label = "Separate Components"
    # Links for separate_components_004

    viewer_003 = nodes.new("GeometryNodeViewer")
    viewer_003.name = "Viewer.003"
    viewer_003.label = ""
    viewer_003.location = (-806.904296875, 1413.6922607421875)
    viewer_003.bl_label = "Viewer"
    viewer_003.ui_shortcut = 0
    viewer_003.active_index = 0
    viewer_003.domain = "AUTO"
    # Links for viewer_003
    links.new(separate_components_004.outputs[1], viewer_003.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (-1066.7183837890625, 1172.1756591796875)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(curve_rot_curve.outputs[1], reroute.inputs[0])
    links.new(reroute.outputs[0], separate_components_004.inputs[0])

    viewer_004 = nodes.new("GeometryNodeViewer")
    viewer_004.name = "Viewer.004"
    viewer_004.label = ""
    viewer_004.location = (-1659.3773193359375, 1303.103759765625)
    viewer_004.bl_label = "Viewer"
    viewer_004.ui_shortcut = 0
    viewer_004.active_index = 0
    viewer_004.domain = "AUTO"
    # Links for viewer_004
    links.new(split_curves_about_axis.outputs[0], viewer_004.inputs[0])

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (916.1948852539062, 749.3281860351562)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    loft_curve_parts = nodes.new("GeometryNodeGroup")
    loft_curve_parts.name = "Group.013"
    loft_curve_parts.label = ""
    loft_curve_parts.location = (89.80441284179688, 763.7989501953125)
    loft_curve_parts.node_tree = create_loft_curve_parts_group()
    loft_curve_parts.bl_label = "Group"
    # Links for loft_curve_parts
    links.new(curve_rot_curve_1.outputs[0], loft_curve_parts.inputs[0])

    loft_curve_parts_1 = nodes.new("GeometryNodeGroup")
    loft_curve_parts_1.name = "Group.014"
    loft_curve_parts_1.label = ""
    loft_curve_parts_1.location = (67.15608978271484, 580.848876953125)
    loft_curve_parts_1.node_tree = create_loft_curve_parts_group()
    loft_curve_parts_1.bl_label = "Group"
    # Links for loft_curve_parts_1
    links.new(curve_rot_curve_2.outputs[0], loft_curve_parts_1.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (-279.53741455078125, 648.5192260742188)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketInt"
    # Links for reroute_001
    links.new(reroute_001.outputs[0], loft_curve_parts.inputs[1])
    links.new(group_input_001.outputs[2], reroute_001.inputs[0])
    links.new(reroute_001.outputs[0], loft_curve_parts_1.inputs[1])

    loft_curve_parts_2 = nodes.new("GeometryNodeGroup")
    loft_curve_parts_2.name = "Group.015"
    loft_curve_parts_2.label = ""
    loft_curve_parts_2.location = (65.52377319335938, 407.5830993652344)
    loft_curve_parts_2.node_tree = create_loft_curve_parts_group()
    loft_curve_parts_2.bl_label = "Group"
    # Links for loft_curve_parts_2
    links.new(reroute_001.outputs[0], loft_curve_parts_2.inputs[1])
    links.new(curve_rot_curve_3.outputs[0], loft_curve_parts_2.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (368.56805419921875, 735.681884765625)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(loft_curve_parts.outputs[0], join_geometry_004.inputs[0])
    links.new(loft_curve_parts_1.outputs[0], join_geometry_004.inputs[0])
    links.new(loft_curve_parts_2.outputs[0], join_geometry_004.inputs[0])

    loft_curve_parts_3 = nodes.new("GeometryNodeGroup")
    loft_curve_parts_3.name = "Group.016"
    loft_curve_parts_3.label = ""
    loft_curve_parts_3.location = (94.62529754638672, 935.177978515625)
    loft_curve_parts_3.node_tree = create_loft_curve_parts_group()
    loft_curve_parts_3.bl_label = "Group"
    # Links for loft_curve_parts_3
    links.new(reroute_001.outputs[0], loft_curve_parts_3.inputs[1])
    links.new(loft_curve_parts_3.outputs[0], join_geometry_004.inputs[0])
    links.new(curve_rot_curve.outputs[0], loft_curve_parts_3.inputs[0])

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.label = ""
    merge_by_distance.location = (556.3425903320312, 736.9313354492188)
    merge_by_distance.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance.inputs[1].default_value = True
    # Mode
    merge_by_distance.inputs[2].default_value = "All"
    # Distance
    merge_by_distance.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance
    links.new(join_geometry_004.outputs[0], merge_by_distance.inputs[0])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (736.3272094726562, 759.3602294921875)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = False
    # Links for set_shade_smooth
    links.new(set_shade_smooth.outputs[0], group_output.inputs[0])
    links.new(merge_by_distance.outputs[0], set_shade_smooth.inputs[0])

    viewer_005 = nodes.new("GeometryNodeViewer")
    viewer_005.name = "Viewer.005"
    viewer_005.label = ""
    viewer_005.location = (-1182.601806640625, 747.2337036132812)
    viewer_005.bl_label = "Viewer"
    viewer_005.ui_shortcut = 0
    viewer_005.active_index = 0
    viewer_005.domain = "AUTO"
    # Links for viewer_005
    links.new(curve_rot_curve_2.outputs[1], viewer_005.inputs[0])

    auto_layout_nodes(group)
    return group