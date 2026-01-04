"""
Loft Spheroid geometry node groups for procedural mesh generation.
Moved from tmp/temp_25.py - contains the LoftSpheriod node group and its dependencies.
"""
import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


def get_bundled_node_group(name: str):
    """
    Get a bundled Blender node group by name.
    These are node groups from Blender's Essentials asset library.
    
    Args:
        name: Name of the bundled node group (e.g., "Array")
    
    Returns:
        The node group, or None if not found
    """
    # First check if it already exists in bpy.data
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    
    # Try to load from Blender's bundled assets
    # The Essentials library path varies by OS
    import os
    blender_version = bpy.app.version_string.split()[0]
    
    # Common bundled asset paths
    possible_paths = [
        # Windows
        os.path.join(os.path.dirname(bpy.app.binary_path), blender_version, "datafiles", "assets", "geometry_nodes", "essentials.blend"),
        # Fallback - try script directory  
        os.path.join(bpy.utils.resource_path('LOCAL'), "datafiles", "assets", "geometry_nodes", "essentials.blend"),
    ]
    
    for blend_path in possible_paths:
        if os.path.exists(blend_path):
            try:
                with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
                    if name in data_from.node_groups:
                        data_to.node_groups = [name]
                if name in bpy.data.node_groups:
                    return bpy.data.node_groups[name]
            except Exception:
                continue
    
    # If we still can't find it, return None and let the caller handle it
    return None


def create_array_group():
    """
    Get or create the Array node group.
    This is a bundled Blender asset from the Essentials library.
    """
    existing = get_bundled_node_group("Array")
    if existing:
        return existing
    
    # If the bundled asset isn't available, return None
    # The calling code should handle this gracefully
    return None


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
    group_output.location = (1387.547607421875, 23.529390335083008)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-829.52099609375, -36.41956329345703)
    group_input.bl_label = "Group Input"
    # Links for group_input

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (-262.0, 30.0992431640625)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    grid.label = ""
    grid.location = (221.0078582763672, 116.20465087890625)
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
    domain_size_002.location = (-245.50221252441406, 235.4501495361328)
    domain_size_002.bl_label = "Domain Size"
    domain_size_002.component = "CURVE"
    # Links for domain_size_002
    links.new(reroute_001.outputs[0], domain_size_002.inputs[0])
    links.new(domain_size_002.outputs[4], grid.inputs[2])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (335.1291809082031, -203.06390380859375)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (-266.4889831542969, -316.2491455078125)
    position_001.bl_label = "Position"
    # Links for position_001
    links.new(position_001.outputs[0], sample_index_001.inputs[1])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (897.1658935546875, 109.17431640625)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position
    links.new(grid.outputs[0], set_position.inputs[0])
    links.new(set_position.outputs[0], group_output.inputs[0])
    links.new(sample_index_001.outputs[0], set_position.inputs[2])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (-252.08665466308594, -122.1737060546875)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh
    links.new(curve_to_mesh.outputs[0], sample_index_001.inputs[0])
    links.new(reroute_001.outputs[0], curve_to_mesh.inputs[0])

    index_002 = nodes.new("GeometryNodeInputIndex")
    index_002.name = "Index.002"
    index_002.label = ""
    index_002.location = (-173.16062927246094, -439.4073486328125)
    index_002.bl_label = "Index"
    # Links for index_002
    links.new(index_002.outputs[0], sample_index_001.inputs[2])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (-447.0, 50.06106948852539)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Count"
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve
    links.new(resample_curve.outputs[0], reroute_001.inputs[0])
    links.new(group_input.outputs[0], resample_curve.inputs[0])
    links.new(group_input.outputs[1], resample_curve.inputs[3])

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
    socket = group.interface.new_socket(name="Switch", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

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
    group_input.location = (-1186.8115234375, 13.849903106689453)
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

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (-904.0509033203125, -177.74118041992188)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "CURVE"
    # Links for domain_size
    links.new(group_input.outputs[0], domain_size.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-729.0030517578125, -179.614990234375)
    math.bl_label = "Math"
    math.operation = "SUBTRACT"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 1.0
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(domain_size.outputs[4], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-506.8645935058594, -373.4737243652344)
    math_001.bl_label = "Math"
    math_001.operation = "SUBTRACT"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math.outputs[0], math_001.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (-298.08953857421875, -407.2438659667969)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 2.0
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(math_001.outputs[0], math_002.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (-19.613996505737305, -285.5209655761719)
    switch.bl_label = "Switch"
    switch.input_type = "INT"
    # Links for switch
    links.new(switch.outputs[0], sample_index_012.inputs[2])
    links.new(group_input.outputs[1], switch.inputs[2])
    links.new(switch.outputs[0], sample_index_011.inputs[2])
    links.new(switch.outputs[0], sample_index_006.inputs[2])
    links.new(switch.outputs[0], sample_index_005.inputs[2])
    links.new(group_input.outputs[3], switch.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (-699.6692504882812, -505.7955017089844)
    math_003.bl_label = "Math"
    math_003.operation = "DIVIDE"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 2.0
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(group_input.outputs[1], math_003.inputs[0])
    links.new(math_003.outputs[0], math_001.inputs[1])

    domain_size_001 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_001.name = "Domain Size.001"
    domain_size_001.label = ""
    domain_size_001.location = (-899.22998046875, -680.1869506835938)
    domain_size_001.bl_label = "Domain Size"
    domain_size_001.component = "CURVE"
    # Links for domain_size_001
    links.new(group_input.outputs[0], domain_size_001.inputs[0])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (-724.1820678710938, -682.0607299804688)
    math_004.bl_label = "Math"
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 1.0
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(domain_size_001.outputs[4], math_004.inputs[0])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (-385.6071472167969, -851.0418090820312)
    math_005.bl_label = "Math"
    math_005.operation = "SUBTRACT"
    math_005.use_clamp = False
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(math_004.outputs[0], math_005.inputs[0])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (-217.19674682617188, -940.7866821289062)
    math_006.bl_label = "Math"
    math_006.operation = "MULTIPLY"
    math_006.use_clamp = False
    # Value
    math_006.inputs[1].default_value = 2.0
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(math_005.outputs[0], math_006.inputs[0])

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (-29.646026611328125, -1031.6082763671875)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "ADD"
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(math_006.outputs[0], integer_math.inputs[0])
    links.new(integer_math.outputs[0], switch.inputs[1])

    integer_math_004 = nodes.new("FunctionNodeIntegerMath")
    integer_math_004.name = "Integer Math.004"
    integer_math_004.label = ""
    integer_math_004.location = (-731.1800537109375, -1082.71435546875)
    integer_math_004.bl_label = "Integer Math"
    integer_math_004.operation = "MODULO"
    # Value
    integer_math_004.inputs[1].default_value = 2
    # Value
    integer_math_004.inputs[2].default_value = 0
    # Links for integer_math_004
    links.new(integer_math_004.outputs[0], integer_math.inputs[1])
    links.new(group_input.outputs[1], integer_math_004.inputs[0])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.label = ""
    math_007.location = (-820.0, -902.9105224609375)
    math_007.bl_label = "Math"
    math_007.operation = "DIVIDE"
    math_007.use_clamp = False
    # Value
    math_007.inputs[1].default_value = 2.0
    # Value
    math_007.inputs[2].default_value = 0.5
    # Links for math_007
    links.new(math_007.outputs[0], math_005.inputs[1])
    links.new(group_input.outputs[1], math_007.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_set_handles_group():
    group_name = "SetHandles"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="HandleA", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="HandleB", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="PositionA", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="PositionB", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="CurveA", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="TangentA", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="NormalA", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="CurveB", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="TangentB", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="NormalB", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1185.1075439453125, 119.63382720947266)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1161.087158203125, -14.222005844116211)
    group_input.bl_label = "Group Input"
    # Links for group_input

    index_002 = nodes.new("GeometryNodeInputIndex")
    index_002.name = "Index.002"
    index_002.label = ""
    index_002.location = (-1099.22021484375, 162.25738525390625)
    index_002.bl_label = "Index"
    # Links for index_002

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-876.4878540039062, 248.62969970703125)
    math_001.bl_label = "Math"
    math_001.operation = "DIVIDE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 2.0
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(index_002.outputs[0], math_001.inputs[0])

    sample_index_009 = nodes.new("GeometryNodeSampleIndex")
    sample_index_009.name = "Sample Index.009"
    sample_index_009.label = ""
    sample_index_009.location = (-363.1686096191406, 64.17465209960938)
    sample_index_009.bl_label = "Sample Index"
    sample_index_009.data_type = "FLOAT_VECTOR"
    sample_index_009.domain = "POINT"
    sample_index_009.clamp = False
    # Links for sample_index_009
    links.new(math_001.outputs[0], sample_index_009.inputs[2])
    links.new(group_input.outputs[0], sample_index_009.inputs[0])
    links.new(sample_index_009.outputs[0], group_output.inputs[2])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (-707.1697998046875, -91.63800048828125)
    position_001.bl_label = "Position"
    # Links for position_001
    links.new(position_001.outputs[0], sample_index_009.inputs[1])

    sample_index_010 = nodes.new("GeometryNodeSampleIndex")
    sample_index_010.name = "Sample Index.010"
    sample_index_010.label = ""
    sample_index_010.location = (-365.93695068359375, -146.77980041503906)
    sample_index_010.bl_label = "Sample Index"
    sample_index_010.data_type = "FLOAT_VECTOR"
    sample_index_010.domain = "POINT"
    sample_index_010.clamp = False
    # Links for sample_index_010
    links.new(math_001.outputs[0], sample_index_010.inputs[2])
    links.new(position_001.outputs[0], sample_index_010.inputs[1])
    links.new(group_input.outputs[3], sample_index_010.inputs[0])
    links.new(sample_index_010.outputs[0], group_output.inputs[3])

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (87.67414855957031, 116.74725341796875)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "ADD"
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006
    links.new(sample_index_009.outputs[0], vector_math_006.inputs[0])
    links.new(sample_index_010.outputs[0], vector_math_006.inputs[1])

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.label = ""
    vector_math_007.location = (491.18865966796875, 50.70146179199219)
    vector_math_007.bl_label = "Vector Math"
    vector_math_007.operation = "SCALE"
    # Vector
    vector_math_007.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_007
    links.new(vector_math_006.outputs[0], vector_math_007.inputs[0])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.label = ""
    vector_math_008.location = (278.6622619628906, -52.563232421875)
    vector_math_008.bl_label = "Vector Math"
    vector_math_008.operation = "DISTANCE"
    # Vector
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_008.inputs[3].default_value = 1.0
    # Links for vector_math_008
    links.new(vector_math_008.outputs[1], vector_math_007.inputs[3])
    links.new(sample_index_009.outputs[0], vector_math_008.inputs[0])
    links.new(sample_index_010.outputs[0], vector_math_008.inputs[1])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (286.9575500488281, 295.33734130859375)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "SCALE"
    # Vector
    vector_math.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 0.5
    # Links for vector_math
    links.new(vector_math_006.outputs[0], vector_math.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (1099.70166015625, 187.13038635253906)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketVector"
    # Links for reroute
    links.new(reroute.outputs[0], group_output.inputs[0])
    links.new(reroute.outputs[0], group_output.inputs[1])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (850.54638671875, 306.03070068359375)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "ADD"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(vector_math_001.outputs[0], reroute.inputs[0])
    links.new(vector_math.outputs[0], vector_math_001.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (671.0, 144.48333740234375)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 0.19999992847442627
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], vector_math_001.inputs[1])
    links.new(vector_math_007.outputs[0], vector_math_002.inputs[0])

    sample_index_011 = nodes.new("GeometryNodeSampleIndex")
    sample_index_011.name = "Sample Index.011"
    sample_index_011.label = ""
    sample_index_011.location = (-346.8516845703125, -610.5057373046875)
    sample_index_011.bl_label = "Sample Index"
    sample_index_011.data_type = "FLOAT_VECTOR"
    sample_index_011.domain = "POINT"
    sample_index_011.clamp = False
    # Links for sample_index_011
    links.new(math_001.outputs[0], sample_index_011.inputs[2])
    links.new(group_input.outputs[3], sample_index_011.inputs[0])
    links.new(group_input.outputs[5], sample_index_011.inputs[1])

    sample_index_012 = nodes.new("GeometryNodeSampleIndex")
    sample_index_012.name = "Sample Index.012"
    sample_index_012.label = ""
    sample_index_012.location = (-355.0589294433594, -379.0880432128906)
    sample_index_012.bl_label = "Sample Index"
    sample_index_012.data_type = "FLOAT_VECTOR"
    sample_index_012.domain = "POINT"
    sample_index_012.clamp = False
    # Links for sample_index_012
    links.new(math_001.outputs[0], sample_index_012.inputs[2])
    links.new(group_input.outputs[0], sample_index_012.inputs[0])
    links.new(group_input.outputs[2], sample_index_012.inputs[1])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (732.5552368164062, -145.2587890625)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "ADD"
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(sample_index_009.outputs[0], vector_math_003.inputs[1])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (635.5346069335938, -485.6574401855469)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "ADD"
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(sample_index_010.outputs[0], vector_math_004.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (-153.94729614257812, -301.81842041015625)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "NORMALIZE"
    # Vector
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_005.inputs[3].default_value = 1.0
    # Links for vector_math_005
    links.new(sample_index_012.outputs[0], vector_math_005.inputs[0])

    vector_math_009 = nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.label = ""
    vector_math_009.location = (-131.3297882080078, -634.953369140625)
    vector_math_009.bl_label = "Vector Math"
    vector_math_009.operation = "NORMALIZE"
    # Vector
    vector_math_009.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_009.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_009.inputs[3].default_value = 1.0
    # Links for vector_math_009
    links.new(sample_index_011.outputs[0], vector_math_009.inputs[0])

    vector_math_010 = nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.label = ""
    vector_math_010.location = (88.80683135986328, -174.81814575195312)
    vector_math_010.bl_label = "Vector Math"
    vector_math_010.operation = "DOT_PRODUCT"
    # Vector
    vector_math_010.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_010.inputs[3].default_value = 1.0
    # Links for vector_math_010
    links.new(vector_math_005.outputs[0], vector_math_010.inputs[0])
    links.new(sample_index_010.outputs[0], vector_math_010.inputs[1])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (313.7152404785156, -220.23715209960938)
    math.bl_label = "Math"
    math.operation = "SIGN"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.5
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(vector_math_010.outputs[1], math.inputs[0])

    vector_math_011 = nodes.new("ShaderNodeVectorMath")
    vector_math_011.name = "Vector Math.011"
    vector_math_011.label = ""
    vector_math_011.location = (529.8158569335938, -197.86407470703125)
    vector_math_011.bl_label = "Vector Math"
    vector_math_011.operation = "SCALE"
    # Vector
    vector_math_011.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_011.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_011
    links.new(vector_math_005.outputs[0], vector_math_011.inputs[0])
    links.new(math.outputs[0], vector_math_011.inputs[3])
    links.new(vector_math_011.outputs[0], vector_math_003.inputs[0])

    vector_math_012 = nodes.new("ShaderNodeVectorMath")
    vector_math_012.name = "Vector Math.012"
    vector_math_012.label = ""
    vector_math_012.location = (122.03595733642578, -550.6720581054688)
    vector_math_012.bl_label = "Vector Math"
    vector_math_012.operation = "DOT_PRODUCT"
    # Vector
    vector_math_012.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_012.inputs[3].default_value = 1.0
    # Links for vector_math_012
    links.new(sample_index_009.outputs[0], vector_math_012.inputs[0])
    links.new(vector_math_009.outputs[0], vector_math_012.inputs[1])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (343.5240173339844, -697.6522216796875)
    math_002.bl_label = "Math"
    math_002.operation = "SIGN"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 0.5
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(vector_math_012.outputs[1], math_002.inputs[0])

    vector_math_013 = nodes.new("ShaderNodeVectorMath")
    vector_math_013.name = "Vector Math.013"
    vector_math_013.label = ""
    vector_math_013.location = (545.0252075195312, -647.3753662109375)
    vector_math_013.bl_label = "Vector Math"
    vector_math_013.operation = "SCALE"
    # Vector
    vector_math_013.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_013.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_013
    links.new(math_002.outputs[0], vector_math_013.inputs[3])
    links.new(vector_math_009.outputs[0], vector_math_013.inputs[0])
    links.new(vector_math_013.outputs[0], vector_math_004.inputs[1])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_curve_rib_cage_group():
    group_name = "CurveRibCage"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveA", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveB", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveResolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 200
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Radial Resolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="MaxResolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
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
    group_output.location = (2903.184326171875, 199.82162475585938)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1839.8890380859375, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    integer = nodes.new("FunctionNodeInputInt")
    integer.name = "Integer"
    integer.label = "Resolution"
    integer.location = (-1639.8890380859375, 107.2135009765625)
    integer.bl_label = "Integer"
    integer.integer = 200
    # Links for integer

    integer_003 = nodes.new("FunctionNodeInputInt")
    integer_003.name = "Integer.003"
    integer_003.label = ""
    integer_003.location = (-1656.304443359375, -235.44937133789062)
    integer_003.bl_label = "Integer"
    integer_003.integer = 50
    # Links for integer_003

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (-1408.2342529296875, 86.822265625)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketInt"
    # Links for reroute_002
    links.new(group_input.outputs[3], reroute_002.inputs[0])

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.label = ""
    reroute_003.location = (-1415.2530517578125, -12.4205322265625)
    reroute_003.bl_label = "Reroute"
    reroute_003.socket_idname = "NodeSocketInt"
    # Links for reroute_003
    links.new(group_input.outputs[4], reroute_003.inputs[0])

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (-1217.8558349609375, 421.913330078125)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "COUNT"
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points
    links.new(reroute_002.outputs[0], curve_to_points.inputs[1])
    links.new(group_input.outputs[1], curve_to_points.inputs[0])

    curve_to_points_001 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.name = "Curve to Points.001"
    curve_to_points_001.label = ""
    curve_to_points_001.location = (-1180.1820068359375, 155.034912109375)
    curve_to_points_001.bl_label = "Curve to Points"
    curve_to_points_001.mode = "COUNT"
    # Length
    curve_to_points_001.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points_001
    links.new(reroute_002.outputs[0], curve_to_points_001.inputs[1])
    links.new(group_input.outputs[0], curve_to_points_001.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (829.149169921875, 559.6358642578125)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position

    array = nodes.new("GeometryNodeGroup")
    array.name = "Group"
    array.label = ""
    array.location = (-273.0000305175781, 209.8246307373047)
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
    array.inputs[20].default_value = True
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
    links.new(array.outputs[0], set_position.inputs[0])
    links.new(reroute_002.outputs[0], array.inputs[3])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (-1354.190185546875, 585.2673950195312)
    index.bl_label = "Index"
    # Links for index

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1418.1240234375, 560.9843139648438)
    set_position_001.bl_label = "Set Position"
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001
    links.new(set_position.outputs[0], set_position_001.inputs[0])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.label = ""
    sample_index_002.location = (125.06501007080078, -38.159156799316406)
    sample_index_002.bl_label = "Sample Index"
    sample_index_002.data_type = "INT"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    # Links for sample_index_002
    links.new(array.outputs[0], sample_index_002.inputs[0])

    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.label = ""
    index_001.location = (-65.76254272460938, -227.00503540039062)
    index_001.bl_label = "Index"
    # Links for index_001
    links.new(index_001.outputs[0], sample_index_002.inputs[2])
    links.new(index_001.outputs[0], sample_index_002.inputs[1])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (482.5027160644531, -66.42317199707031)
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

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (303.0, -101.26826477050781)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "MODULO"
    # Value
    integer_math.inputs[1].default_value = 2
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(integer_math.outputs[0], compare.inputs[2])
    links.new(sample_index_002.outputs[0], integer_math.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (667.40771484375, -83.35041046142578)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "NOT"
    # Boolean
    boolean_math.inputs[1].default_value = False
    # Links for boolean_math
    links.new(compare.outputs[0], boolean_math.inputs[0])
    links.new(boolean_math.outputs[0], set_position_001.inputs[1])

    set_handle_positions = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions.name = "Set Handle Positions"
    set_handle_positions.label = ""
    set_handle_positions.location = (2300.10595703125, 556.7994384765625)
    set_handle_positions.bl_label = "Set Handle Positions"
    set_handle_positions.mode = "LEFT"
    # Offset
    set_handle_positions.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_handle_positions
    links.new(boolean_math.outputs[0], set_handle_positions.inputs[1])

    set_handle_positions_001 = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions_001.name = "Set Handle Positions.001"
    set_handle_positions_001.label = ""
    set_handle_positions_001.location = (1787.247802734375, 582.4185180664062)
    set_handle_positions_001.bl_label = "Set Handle Positions"
    set_handle_positions_001.mode = "RIGHT"
    # Selection
    set_handle_positions_001.inputs[1].default_value = True
    # Offset
    set_handle_positions_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_handle_positions_001
    links.new(set_handle_positions_001.outputs[0], set_handle_positions.inputs[0])
    links.new(set_position_001.outputs[0], set_handle_positions_001.inputs[0])

    sample_index_007 = nodes.new("GeometryNodeSampleIndex")
    sample_index_007.name = "Sample Index.007"
    sample_index_007.label = ""
    sample_index_007.location = (3675.80859375, 815.5343627929688)
    sample_index_007.bl_label = "Sample Index"
    sample_index_007.data_type = "FLOAT_VECTOR"
    sample_index_007.domain = "POINT"
    sample_index_007.clamp = False
    # Value
    sample_index_007.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Index
    sample_index_007.inputs[2].default_value = 0
    # Links for sample_index_007

    sample_index_008 = nodes.new("GeometryNodeSampleIndex")
    sample_index_008.name = "Sample Index.008"
    sample_index_008.label = ""
    sample_index_008.location = (3685.39697265625, 1044.4698486328125)
    sample_index_008.bl_label = "Sample Index"
    sample_index_008.data_type = "FLOAT_VECTOR"
    sample_index_008.domain = "POINT"
    sample_index_008.clamp = False
    # Value
    sample_index_008.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Index
    sample_index_008.inputs[2].default_value = 0
    # Links for sample_index_008

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (63.43391418457031, 772.19189453125)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(curve_to_points_001.outputs[0], reroute.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (67.85675811767578, 737.757568359375)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketVector"
    # Links for reroute_001
    links.new(curve_to_points_001.outputs[1], reroute_001.inputs[0])

    reroute_004 = nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.label = ""
    reroute_004.location = (57.05168151855469, 951.3240966796875)
    reroute_004.bl_label = "Reroute"
    reroute_004.socket_idname = "NodeSocketGeometry"
    # Links for reroute_004
    links.new(curve_to_points.outputs[0], reroute_004.inputs[0])

    reroute_005 = nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.label = ""
    reroute_005.location = (64.10752868652344, 926.9064331054688)
    reroute_005.bl_label = "Reroute"
    reroute_005.socket_idname = "NodeSocketVector"
    # Links for reroute_005
    links.new(curve_to_points.outputs[1], reroute_005.inputs[0])

    debug_handles = nodes.new("GeometryNodeGroup")
    debug_handles.name = "Group.001"
    debug_handles.label = ""
    debug_handles.location = (2627.62158203125, 694.8394775390625)
    debug_handles.node_tree = create_debug_handles_group()
    debug_handles.bl_label = "Group"
    # Index
    debug_handles.inputs[1].default_value = 14
    # Value
    debug_handles.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Switch
    debug_handles.inputs[3].default_value = False
    # Links for debug_handles
    links.new(set_handle_positions.outputs[0], debug_handles.inputs[0])

    set_handles = nodes.new("GeometryNodeGroup")
    set_handles.name = "Group.002"
    set_handles.label = ""
    set_handles.location = (231.06597900390625, 991.0908203125)
    set_handles.node_tree = create_set_handles_group()
    set_handles.bl_label = "Group"
    # Links for set_handles
    links.new(reroute.outputs[0], set_handles.inputs[3])
    links.new(reroute_005.outputs[0], set_handles.inputs[1])
    links.new(reroute_001.outputs[0], set_handles.inputs[4])
    links.new(reroute_004.outputs[0], set_handles.inputs[0])
    links.new(set_handles.outputs[0], set_handle_positions_001.inputs[2])
    links.new(set_handles.outputs[1], set_handle_positions.inputs[2])
    links.new(set_handles.outputs[2], set_position.inputs[2])
    links.new(set_handles.outputs[3], set_position_001.inputs[2])

    reroute_006 = nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.label = ""
    reroute_006.location = (67.7335205078125, 712.9395751953125)
    reroute_006.bl_label = "Reroute"
    reroute_006.socket_idname = "NodeSocketVector"
    # Links for reroute_006
    links.new(curve_to_points_001.outputs[2], reroute_006.inputs[0])
    links.new(reroute_006.outputs[0], set_handles.inputs[5])

    reroute_007 = nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    reroute_007.label = ""
    reroute_007.location = (64.7851791381836, 893.8403930664062)
    reroute_007.bl_label = "Reroute"
    reroute_007.socket_idname = "NodeSocketVector"
    # Links for reroute_007
    links.new(curve_to_points.outputs[2], reroute_007.inputs[0])
    links.new(reroute_007.outputs[0], set_handles.inputs[2])

    integer_math_001 = nodes.new("FunctionNodeIntegerMath")
    integer_math_001.name = "Integer Math.001"
    integer_math_001.label = ""
    integer_math_001.location = (-1174.0, 615.14111328125)
    integer_math_001.bl_label = "Integer Math"
    integer_math_001.operation = "DIVIDE"
    # Value
    integer_math_001.inputs[1].default_value = 2
    # Value
    integer_math_001.inputs[2].default_value = 0
    # Links for integer_math_001
    links.new(index.outputs[0], integer_math_001.inputs[0])

    bézier_segment = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment.name = "Bézier Segment"
    bézier_segment.label = ""
    bézier_segment.location = (-692.7023315429688, 43.52708435058594)
    bézier_segment.bl_label = "Bézier Segment"
    bézier_segment.mode = "POSITION"
    # Resolution
    bézier_segment.inputs[0].default_value = 16
    # Start
    bézier_segment.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Start Handle
    bézier_segment.inputs[2].default_value = Vector((-0.5, 0.5, 0.0))
    # End Handle
    bézier_segment.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # End
    bézier_segment.inputs[4].default_value = Vector((1.0, 0.0, 0.0))
    # Links for bézier_segment

    set_handle_type_002 = nodes.new("GeometryNodeCurveSetHandles")
    set_handle_type_002.name = "Set Handle Type.002"
    set_handle_type_002.label = ""
    set_handle_type_002.location = (-513.0, 77.51834106445312)
    set_handle_type_002.bl_label = "Set Handle Type"
    set_handle_type_002.handle_type = "ALIGN"
    set_handle_type_002.mode = ['LEFT', 'RIGHT']
    # Selection
    set_handle_type_002.inputs[1].default_value = True
    # Links for set_handle_type_002
    links.new(set_handle_type_002.outputs[0], array.inputs[0])
    links.new(bézier_segment.outputs[0], set_handle_type_002.inputs[0])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (2697.66845703125, 366.85833740234375)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(join_geometry.outputs[0], group_output.inputs[0])
    links.new(set_handle_positions.outputs[0], join_geometry.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_get_position_and_handles_group():
    group_name = "GetPositionAndHandles"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Left Inv", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Position Inv", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Right Inv", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Left", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Right", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Postiion", in_out="OUTPUT", socket_type="NodeSocketVector")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1048.3564453125, 24.619173049926758)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-964.946044921875, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (125.09759521484375, -636.548583984375)
    index.bl_label = "Index"
    # Links for index

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.name = "Sample Index.003"
    sample_index_003.label = "Position B Inv"
    sample_index_003.location = (758.8583374023438, 329.375)
    sample_index_003.bl_label = "Sample Index"
    sample_index_003.data_type = "FLOAT_VECTOR"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    # Links for sample_index_003
    links.new(sample_index_003.outputs[0], group_output.inputs[1])

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.name = "Sample Index.005"
    sample_index_005.label = "Right B Inv"
    sample_index_005.location = (751.6654052734375, 120.30117797851562)
    sample_index_005.bl_label = "Sample Index"
    sample_index_005.data_type = "FLOAT_VECTOR"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    # Links for sample_index_005
    links.new(sample_index_005.outputs[0], group_output.inputs[2])

    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.label = ""
    index_001.location = (-764.946044921875, -139.975830078125)
    index_001.bl_label = "Index"
    # Links for index_001

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (-691.083984375, 100.5946044921875)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "CURVE"
    # Links for domain_size
    links.new(group_input.outputs[0], domain_size.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-516.0360107421875, 98.72076416015625)
    math.bl_label = "Math"
    math.operation = "SUBTRACT"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 1.0
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(domain_size.outputs[4], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-328.5074462890625, -48.64935302734375)
    math_001.bl_label = "Math"
    math_001.operation = "SUBTRACT"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math.outputs[0], math_001.inputs[0])

    evaluate_on_domain = nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.name = "Evaluate on Domain"
    evaluate_on_domain.label = ""
    evaluate_on_domain.location = (-582.481201171875, -92.24609375)
    evaluate_on_domain.bl_label = "Evaluate on Domain"
    evaluate_on_domain.domain = "CURVE"
    evaluate_on_domain.data_type = "INT"
    # Links for evaluate_on_domain
    links.new(index_001.outputs[0], evaluate_on_domain.inputs[0])
    links.new(evaluate_on_domain.outputs[0], math_001.inputs[1])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (-160.0970458984375, -138.39422607421875)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 2.0
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(math_001.outputs[0], math_002.inputs[0])

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (65.55516052246094, 487.19842529296875)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "ADD"
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(math_002.outputs[0], integer_math.inputs[0])
    links.new(integer_math.outputs[0], sample_index_005.inputs[2])
    links.new(integer_math.outputs[0], sample_index_003.inputs[2])

    sample_index_004 = nodes.new("GeometryNodeSampleIndex")
    sample_index_004.name = "Sample Index.004"
    sample_index_004.label = "Left B Inv"
    sample_index_004.location = (764.946044921875, 551.9163818359375)
    sample_index_004.bl_label = "Sample Index"
    sample_index_004.data_type = "FLOAT_VECTOR"
    sample_index_004.domain = "POINT"
    sample_index_004.clamp = False
    # Links for sample_index_004
    links.new(integer_math.outputs[0], sample_index_004.inputs[2])
    links.new(sample_index_004.outputs[0], group_output.inputs[0])

    integer_math_004 = nodes.new("FunctionNodeIntegerMath")
    integer_math_004.name = "Integer Math.004"
    integer_math_004.label = ""
    integer_math_004.location = (-548.3275146484375, -246.1148681640625)
    integer_math_004.bl_label = "Integer Math"
    integer_math_004.operation = "MODULO"
    # Value
    integer_math_004.inputs[1].default_value = 2
    # Value
    integer_math_004.inputs[2].default_value = 0
    # Links for integer_math_004
    links.new(index_001.outputs[0], integer_math_004.inputs[0])
    links.new(integer_math_004.outputs[0], integer_math.inputs[1])

    sample_index_008 = nodes.new("GeometryNodeSampleIndex")
    sample_index_008.name = "Sample Index.008"
    sample_index_008.label = "Position B"
    sample_index_008.location = (738.2950439453125, -335.4423828125)
    sample_index_008.bl_label = "Sample Index"
    sample_index_008.data_type = "FLOAT_VECTOR"
    sample_index_008.domain = "POINT"
    sample_index_008.clamp = False
    # Links for sample_index_008
    links.new(index.outputs[0], sample_index_008.inputs[2])
    links.new(sample_index_008.outputs[0], group_output.inputs[5])

    sample_index_009 = nodes.new("GeometryNodeSampleIndex")
    sample_index_009.name = "Sample Index.009"
    sample_index_009.label = "Right B"
    sample_index_009.location = (747.080078125, -551.9163818359375)
    sample_index_009.bl_label = "Sample Index"
    sample_index_009.data_type = "FLOAT_VECTOR"
    sample_index_009.domain = "POINT"
    sample_index_009.clamp = False
    # Links for sample_index_009
    links.new(index.outputs[0], sample_index_009.inputs[2])
    links.new(sample_index_009.outputs[0], group_output.inputs[4])

    sample_index_010 = nodes.new("GeometryNodeSampleIndex")
    sample_index_010.name = "Sample Index.010"
    sample_index_010.label = "Left B"
    sample_index_010.location = (757.4880981445312, -121.73974609375)
    sample_index_010.bl_label = "Sample Index"
    sample_index_010.data_type = "FLOAT_VECTOR"
    sample_index_010.domain = "POINT"
    sample_index_010.clamp = False
    # Links for sample_index_010
    links.new(index.outputs[0], sample_index_010.inputs[2])
    links.new(sample_index_010.outputs[0], group_output.inputs[3])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (46.4398193359375, 93.0948486328125)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(reroute.outputs[0], sample_index_010.inputs[0])
    links.new(reroute.outputs[0], sample_index_005.inputs[0])
    links.new(reroute.outputs[0], sample_index_009.inputs[0])
    links.new(reroute.outputs[0], sample_index_004.inputs[0])
    links.new(reroute.outputs[0], sample_index_003.inputs[0])
    links.new(reroute.outputs[0], sample_index_008.inputs[0])
    links.new(group_input.outputs[0], reroute.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (117.39013671875, -499.133056640625)
    position_002.bl_label = "Position"
    # Links for position_002
    links.new(position_002.outputs[0], sample_index_008.inputs[1])
    links.new(position_002.outputs[0], sample_index_003.inputs[1])

    curve_handle_positions_001 = nodes.new("GeometryNodeInputCurveHandlePositions")
    curve_handle_positions_001.name = "Curve Handle Positions.001"
    curve_handle_positions_001.label = ""
    curve_handle_positions_001.location = (205.35855102539062, -291.5831298828125)
    curve_handle_positions_001.bl_label = "Curve Handle Positions"
    # Relative
    curve_handle_positions_001.inputs[0].default_value = False
    # Links for curve_handle_positions_001
    links.new(curve_handle_positions_001.outputs[0], sample_index_004.inputs[1])
    links.new(curve_handle_positions_001.outputs[1], sample_index_009.inputs[1])
    links.new(curve_handle_positions_001.outputs[0], sample_index_010.inputs[1])
    links.new(curve_handle_positions_001.outputs[1], sample_index_005.inputs[1])

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
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2220.334228515625, -25.85662269592285)
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
    join_geometry.location = (1986.4351806640625, 20.717426300048828)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(join_geometry.outputs[0], group_output.inputs[0])
    links.new(separate_components_001.outputs[0], join_geometry.inputs[0])

    set_handle_positions = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions.name = "Set Handle Positions"
    set_handle_positions.label = ""
    set_handle_positions.location = (1452.5316162109375, 466.7369384765625)
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
    compare.location = (1124.1785888671875, -89.12350463867188)
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
    links.new(compare.outputs[0], set_handle_positions.inputs[1])

    debug_handles = nodes.new("GeometryNodeGroup")
    debug_handles.name = "Group.001"
    debug_handles.label = ""
    debug_handles.location = (1658.29296875, 313.65655517578125)
    debug_handles.node_tree = create_debug_handles_group()
    debug_handles.bl_label = "Group"
    # Index
    debug_handles.inputs[1].default_value = 2
    # Value
    debug_handles.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for debug_handles
    links.new(set_handle_positions.outputs[0], debug_handles.inputs[0])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (1023.8364868164062, 674.670166015625)
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
    links.new(mix.outputs[1], set_handle_positions.inputs[2])

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

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (1405.96826171875, 79.9457015991211)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "NOT"
    # Boolean
    boolean_math.inputs[1].default_value = False
    # Links for boolean_math
    links.new(compare_001.outputs[0], boolean_math.inputs[0])
    links.new(boolean_math.outputs[0], debug_handles.inputs[3])

    set_handle_positions_001 = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions_001.name = "Set Handle Positions.001"
    set_handle_positions_001.label = ""
    set_handle_positions_001.location = (1464.9913330078125, -279.5343017578125)
    set_handle_positions_001.bl_label = "Set Handle Positions"
    set_handle_positions_001.mode = "LEFT"
    # Offset
    set_handle_positions_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_handle_positions_001
    links.new(separate_components_002.outputs[1], set_handle_positions_001.inputs[0])
    links.new(compare.outputs[0], set_handle_positions_001.inputs[1])

    debug_handles_1 = nodes.new("GeometryNodeGroup")
    debug_handles_1.name = "Group.002"
    debug_handles_1.label = "Handle B"
    debug_handles_1.location = (1740.105224609375, -297.04949951171875)
    debug_handles_1.node_tree = create_debug_handles_group()
    debug_handles_1.bl_label = "Group"
    # Index
    debug_handles_1.inputs[1].default_value = 2
    # Value
    debug_handles_1.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for debug_handles_1
    links.new(set_handle_positions_001.outputs[0], debug_handles_1.inputs[0])
    links.new(boolean_math.outputs[0], debug_handles_1.inputs[3])

    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.label = ""
    mix_001.location = (1170.73828125, -591.6215209960938)
    mix_001.bl_label = "Mix"
    mix_001.data_type = "VECTOR"
    mix_001.factor_mode = "UNIFORM"
    mix_001.blend_type = "MIX"
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    # Factor
    mix_001.inputs[0].default_value = 0.5
    # Factor
    mix_001.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_001.inputs[2].default_value = 0.0
    # B
    mix_001.inputs[3].default_value = 0.0
    # A
    mix_001.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_001.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_001.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_001.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_001
    links.new(mix_001.outputs[1], set_handle_positions_001.inputs[2])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (2008.0052490234375, -179.67501831054688)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(join_geometry_001.outputs[0], group_output.inputs[1])
    links.new(set_handle_positions_001.outputs[0], join_geometry_001.inputs[0])
    links.new(separate_components_002.outputs[0], join_geometry_001.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (879.3078002929688, -472.99078369140625)
    switch.bl_label = "Switch"
    switch.input_type = "VECTOR"
    # Links for switch
    links.new(switch.outputs[0], mix_001.inputs[4])
    links.new(compare_001.outputs[0], switch.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (-332.0032958984375, 325.2765808105469)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001
    links.new(separate_components_001.outputs[1], reroute_001.inputs[0])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (695.0316162109375, 852.5718383789062)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "VECTOR"
    # Links for switch_001
    links.new(compare_001.outputs[0], switch_001.inputs[0])
    links.new(switch_001.outputs[0], mix.inputs[5])

    get_position_and_handles = nodes.new("GeometryNodeGroup")
    get_position_and_handles.name = "Group"
    get_position_and_handles.label = ""
    get_position_and_handles.location = (145.87744140625, -330.1246032714844)
    get_position_and_handles.node_tree = create_get_position_and_handles_group()
    get_position_and_handles.bl_label = "Group"
    # Links for get_position_and_handles
    links.new(get_position_and_handles.outputs[3], mix_001.inputs[5])
    links.new(get_position_and_handles.outputs[2], switch_001.inputs[1])
    links.new(separate_components_002.outputs[1], get_position_and_handles.inputs[0])
    links.new(get_position_and_handles.outputs[4], switch_001.inputs[2])

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.label = ""
    switch_002.location = (866.603515625, -313.0365905761719)
    switch_002.bl_label = "Switch"
    switch_002.input_type = "VECTOR"
    # Links for switch_002
    links.new(get_position_and_handles.outputs[1], switch_002.inputs[1])
    links.new(get_position_and_handles.outputs[5], switch_002.inputs[2])
    links.new(compare_001.outputs[0], switch_002.inputs[0])
    links.new(switch_002.outputs[0], compare.inputs[4])

    get_position_and_handles_1 = nodes.new("GeometryNodeGroup")
    get_position_and_handles_1.name = "Group.003"
    get_position_and_handles_1.label = ""
    get_position_and_handles_1.location = (1.009063720703125, 531.7056884765625)
    get_position_and_handles_1.node_tree = create_get_position_and_handles_group()
    get_position_and_handles_1.bl_label = "Group"
    # Links for get_position_and_handles_1
    links.new(reroute_001.outputs[0], get_position_and_handles_1.inputs[0])
    links.new(get_position_and_handles_1.outputs[3], mix.inputs[4])
    links.new(get_position_and_handles_1.outputs[4], switch.inputs[2])
    links.new(get_position_and_handles_1.outputs[2], switch.inputs[1])
    links.new(get_position_and_handles_1.outputs[5], compare.inputs[5])

    switch_003 = nodes.new("GeometryNodeSwitch")
    switch_003.name = "Switch.003"
    switch_003.label = ""
    switch_003.location = (603.6848754882812, 319.7162780761719)
    switch_003.bl_label = "Switch"
    switch_003.input_type = "VECTOR"
    # Links for switch_003
    links.new(get_position_and_handles_1.outputs[1], switch_003.inputs[1])
    links.new(get_position_and_handles_1.outputs[5], switch_003.inputs[2])
    links.new(compare_001.outputs[0], switch_003.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_loft_spheriod_group():
    group_name = "LoftSpheriod"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Value", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="CurveResolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 200
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Radial Resolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2067.265625, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-2077.265380859375, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (-1310.141357421875, 347.8206787109375)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "CURVE"
    # Links for separate_geometry

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (-1260.673095703125, 62.5552978515625)
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
    index.location = (-1477.432861328125, 24.95831298828125)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], math_005.inputs[0])

    viewer = nodes.new("GeometryNodeViewer")
    viewer.name = "Viewer"
    viewer.label = ""
    viewer.location = (-1084.2939453125, -229.27688598632812)
    viewer.bl_label = "Viewer"
    viewer.ui_shortcut = 0
    viewer.active_index = 0
    viewer.domain = "AUTO"
    # Links for viewer

    set_axis = nodes.new("GeometryNodeGroup")
    set_axis.name = "Group.001"
    set_axis.label = ""
    set_axis.location = (-1877.265380859375, -427.7810974121094)
    set_axis.node_tree = create_set_axis_group()
    set_axis.bl_label = "Group"
    # Name
    set_axis.inputs[2].default_value = "axis+"
    # Links for set_axis
    links.new(group_input.outputs[0], set_axis.inputs[0])

    set_axis_1 = nodes.new("GeometryNodeGroup")
    set_axis_1.name = "Group.002"
    set_axis_1.label = ""
    set_axis_1.location = (-1670.775634765625, -266.4662780761719)
    set_axis_1.node_tree = create_set_axis_group()
    set_axis_1.bl_label = "Group"
    # Name
    set_axis_1.inputs[2].default_value = "axis-"
    # Links for set_axis_1
    links.new(set_axis.outputs[0], set_axis_1.inputs[0])
    links.new(set_axis_1.outputs[0], viewer.inputs[0])
    links.new(set_axis_1.outputs[0], separate_geometry.inputs[0])

    viewer_001 = nodes.new("GeometryNodeViewer")
    viewer_001.name = "Viewer.001"
    viewer_001.label = ""
    viewer_001.location = (-1050.574951171875, 202.72491455078125)
    viewer_001.bl_label = "Viewer"
    viewer_001.ui_shortcut = 0
    viewer_001.active_index = 0
    viewer_001.domain = "AUTO"
    # Links for viewer_001
    links.new(separate_geometry.outputs[1], viewer_001.inputs[0])

    split_curves_about_axis = nodes.new("GeometryNodeGroup")
    split_curves_about_axis.name = "Group.003"
    split_curves_about_axis.label = ""
    split_curves_about_axis.location = (-833.828125, 427.2255859375)
    split_curves_about_axis.node_tree = create_split_curves_about_axis_group()
    split_curves_about_axis.bl_label = "Group"
    # Links for split_curves_about_axis
    links.new(separate_geometry.outputs[0], split_curves_about_axis.inputs[0])

    split_curves_about_axis_1 = nodes.new("GeometryNodeGroup")
    split_curves_about_axis_1.name = "SplitCurvesAboutAxis"
    split_curves_about_axis_1.label = ""
    split_curves_about_axis_1.location = (-838.374755859375, 264.2379150390625)
    split_curves_about_axis_1.node_tree = create_split_curves_about_axis_group()
    split_curves_about_axis_1.bl_label = "Group"
    # Links for split_curves_about_axis_1
    links.new(separate_geometry.outputs[1], split_curves_about_axis_1.inputs[0])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (-272.06591796875, 460.7904052734375)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(split_curves_about_axis.outputs[0], join_geometry.inputs[0])
    links.new(split_curves_about_axis_1.outputs[1], join_geometry.inputs[0])
    links.new(split_curves_about_axis.outputs[1], join_geometry.inputs[0])
    links.new(split_curves_about_axis_1.outputs[0], join_geometry.inputs[0])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (-1315.76953125, -422.73199462890625)
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
    position.location = (-1604.45458984375, -588.0914916992188)
    position.bl_label = "Position"
    # Links for position
    links.new(position.outputs[0], sample_index.inputs[1])

    get_axis = nodes.new("GeometryNodeGroup")
    get_axis.name = "Group.004"
    get_axis.label = ""
    get_axis.location = (-1090.255859375, 539.30419921875)
    get_axis.node_tree = create_get_axis_group()
    get_axis.bl_label = "Group"
    # Links for get_axis
    links.new(separate_geometry.outputs[1], get_axis.inputs[1])
    links.new(separate_geometry.outputs[0], get_axis.inputs[0])

    orient_curve = nodes.new("GeometryNodeGroup")
    orient_curve.name = "Group.005"
    orient_curve.label = ""
    orient_curve.location = (-446.660400390625, 251.6153564453125)
    orient_curve.node_tree = create_orient_curve_group()
    orient_curve.bl_label = "Group"
    # Links for orient_curve
    links.new(split_curves_about_axis.outputs[0], orient_curve.inputs[0])
    links.new(split_curves_about_axis_1.outputs[1], orient_curve.inputs[1])

    orient_curve_1 = nodes.new("GeometryNodeGroup")
    orient_curve_1.name = "Group.008"
    orient_curve_1.label = ""
    orient_curve_1.location = (-450.034912109375, -144.38726806640625)
    orient_curve_1.node_tree = create_orient_curve_group()
    orient_curve_1.bl_label = "Group"
    # Links for orient_curve_1
    links.new(split_curves_about_axis_1.outputs[0], orient_curve_1.inputs[1])
    links.new(split_curves_about_axis.outputs[1], orient_curve_1.inputs[0])

    orient_curve_2 = nodes.new("GeometryNodeGroup")
    orient_curve_2.name = "Group.010"
    orient_curve_2.label = ""
    orient_curve_2.location = (-460.482421875, 65.53424072265625)
    orient_curve_2.node_tree = create_orient_curve_group()
    orient_curve_2.bl_label = "Group"
    # Links for orient_curve_2
    links.new(split_curves_about_axis.outputs[1], orient_curve_2.inputs[0])
    links.new(split_curves_about_axis_1.outputs[1], orient_curve_2.inputs[1])

    orient_curve_3 = nodes.new("GeometryNodeGroup")
    orient_curve_3.name = "Group.012"
    orient_curve_3.label = ""
    orient_curve_3.location = (-457.2618408203125, -361.70751953125)
    orient_curve_3.node_tree = create_orient_curve_group()
    orient_curve_3.bl_label = "Group"
    # Links for orient_curve_3
    links.new(split_curves_about_axis.outputs[0], orient_curve_3.inputs[0])
    links.new(split_curves_about_axis_1.outputs[0], orient_curve_3.inputs[1])

    integer_math_003 = nodes.new("FunctionNodeIntegerMath")
    integer_math_003.name = "Integer Math.003"
    integer_math_003.label = ""
    integer_math_003.location = (-992.8583984375, -107.34674072265625)
    integer_math_003.bl_label = "Integer Math"
    integer_math_003.operation = "DIVIDE_CEIL"
    # Value
    integer_math_003.inputs[1].default_value = 4
    # Value
    integer_math_003.inputs[2].default_value = 0
    # Links for integer_math_003
    links.new(group_input.outputs[1], integer_math_003.inputs[0])

    viewer_004 = nodes.new("GeometryNodeViewer")
    viewer_004.name = "Viewer.004"
    viewer_004.label = ""
    viewer_004.location = (-337.9136962890625, 578.904052734375)
    viewer_004.bl_label = "Viewer"
    viewer_004.ui_shortcut = 0
    viewer_004.active_index = 0
    viewer_004.domain = "AUTO"
    # Links for viewer_004
    links.new(split_curves_about_axis.outputs[0], viewer_004.inputs[0])

    loft_curve_parts = nodes.new("GeometryNodeGroup")
    loft_curve_parts.name = "Group.013"
    loft_curve_parts.label = ""
    loft_curve_parts.location = (1780.077392578125, 53.3594970703125)
    loft_curve_parts.node_tree = create_loft_curve_parts_group()
    loft_curve_parts.bl_label = "Group"
    # Links for loft_curve_parts
    links.new(group_input.outputs[1], loft_curve_parts.inputs[1])

    loft_curve_parts_1 = nodes.new("GeometryNodeGroup")
    loft_curve_parts_1.name = "Group.015"
    loft_curve_parts_1.label = ""
    loft_curve_parts_1.location = (1755.7967529296875, -302.8563232421875)
    loft_curve_parts_1.node_tree = create_loft_curve_parts_group()
    loft_curve_parts_1.bl_label = "Group"
    # Vertices Y
    loft_curve_parts_1.inputs[1].default_value = 3
    # Links for loft_curve_parts_1

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (517.7208251953125, -399.0810241699219)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Switch
    switch.inputs[0].default_value = True
    # Links for switch

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (515.8461303710938, 65.640625)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Switch
    switch_001.inputs[0].default_value = True
    # Links for switch_001

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.label = ""
    switch_002.location = (519.3490600585938, -243.988037109375)
    switch_002.bl_label = "Switch"
    switch_002.input_type = "GEOMETRY"
    # Switch
    switch_002.inputs[0].default_value = True
    # Links for switch_002

    switch_003 = nodes.new("GeometryNodeSwitch")
    switch_003.name = "Switch.003"
    switch_003.label = ""
    switch_003.location = (512.4342041015625, -86.969970703125)
    switch_003.bl_label = "Switch"
    switch_003.input_type = "GEOMETRY"
    # Switch
    switch_003.inputs[0].default_value = True
    # Links for switch_003

    curve_rib_cage = nodes.new("GeometryNodeGroup")
    curve_rib_cage.name = "Group"
    curve_rib_cage.label = ""
    curve_rib_cage.location = (-139.23486328125, 354.98583984375)
    curve_rib_cage.node_tree = create_curve_rib_cage_group()
    curve_rib_cage.bl_label = "Group"
    # Links for curve_rib_cage
    links.new(orient_curve.outputs[0], curve_rib_cage.inputs[0])
    links.new(integer_math_003.outputs[0], curve_rib_cage.inputs[4])
    links.new(curve_rib_cage.outputs[0], switch_003.inputs[2])
    links.new(get_axis.outputs[4], curve_rib_cage.inputs[5])
    links.new(orient_curve.outputs[1], curve_rib_cage.inputs[1])
    links.new(group_input.outputs[2], curve_rib_cage.inputs[2])
    links.new(group_input.outputs[3], curve_rib_cage.inputs[3])

    curve_rib_cage_1 = nodes.new("GeometryNodeGroup")
    curve_rib_cage_1.name = "Group.006"
    curve_rib_cage_1.label = ""
    curve_rib_cage_1.location = (-147.656494140625, -171.15997314453125)
    curve_rib_cage_1.node_tree = create_curve_rib_cage_group()
    curve_rib_cage_1.bl_label = "Group"
    # Links for curve_rib_cage_1
    links.new(curve_rib_cage_1.outputs[0], switch.inputs[2])
    links.new(orient_curve_1.outputs[0], curve_rib_cage_1.inputs[0])
    links.new(orient_curve_1.outputs[1], curve_rib_cage_1.inputs[1])
    links.new(get_axis.outputs[4], curve_rib_cage_1.inputs[5])
    links.new(integer_math_003.outputs[0], curve_rib_cage_1.inputs[4])
    links.new(group_input.outputs[3], curve_rib_cage_1.inputs[2])
    links.new(group_input.outputs[3], curve_rib_cage_1.inputs[3])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (1319.568359375, 6.187744140625)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001

    curve_rib_cage_2 = nodes.new("GeometryNodeGroup")
    curve_rib_cage_2.name = "Group.007"
    curve_rib_cage_2.label = ""
    curve_rib_cage_2.location = (-136.952392578125, 162.30877685546875)
    curve_rib_cage_2.node_tree = create_curve_rib_cage_group()
    curve_rib_cage_2.bl_label = "Group"
    # CurveResolution
    curve_rib_cage_2.inputs[2].default_value = 200
    # Links for curve_rib_cage_2
    links.new(curve_rib_cage_2.outputs[0], switch_001.inputs[2])
    links.new(orient_curve_2.outputs[0], curve_rib_cage_2.inputs[0])
    links.new(get_axis.outputs[4], curve_rib_cage_2.inputs[5])
    links.new(orient_curve_2.outputs[1], curve_rib_cage_2.inputs[1])
    links.new(group_input.outputs[2], curve_rib_cage_2.inputs[4])
    links.new(group_input.outputs[3], curve_rib_cage_2.inputs[3])

    curve_rib_cage_3 = nodes.new("GeometryNodeGroup")
    curve_rib_cage_3.name = "Group.009"
    curve_rib_cage_3.label = ""
    curve_rib_cage_3.location = (-147.3289794921875, -390.40728759765625)
    curve_rib_cage_3.node_tree = create_curve_rib_cage_group()
    curve_rib_cage_3.bl_label = "Group"
    # Links for curve_rib_cage_3
    links.new(integer_math_003.outputs[0], curve_rib_cage_3.inputs[2])
    links.new(curve_rib_cage_3.outputs[0], switch_002.inputs[2])
    links.new(orient_curve_3.outputs[0], curve_rib_cage_3.inputs[0])
    links.new(orient_curve_3.outputs[1], curve_rib_cage_3.inputs[1])
    links.new(get_axis.outputs[4], curve_rib_cage_3.inputs[5])
    links.new(group_input.outputs[2], curve_rib_cage_3.inputs[4])
    links.new(group_input.outputs[3], curve_rib_cage_3.inputs[3])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (1877.2655029296875, 588.091552734375)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002
    links.new(loft_curve_parts.outputs[0], join_geometry_002.inputs[0])
    links.new(group_input.outputs[0], join_geometry_002.inputs[0])
    links.new(join_geometry_002.outputs[0], group_output.inputs[0])

    separate_components = nodes.new("GeometryNodeSeparateComponents")
    separate_components.name = "Separate Components"
    separate_components.label = ""
    separate_components.location = (1326.482421875, 468.34814453125)
    separate_components.bl_label = "Separate Components"
    # Links for separate_components
    links.new(join_geometry_001.outputs[0], separate_components.inputs[0])
    links.new(separate_components.outputs[1], loft_curve_parts.inputs[0])
    links.new(separate_components.outputs[0], join_geometry_002.inputs[0])

    align_handles = nodes.new("GeometryNodeGroup")
    align_handles.name = "Group.021"
    align_handles.label = ""
    align_handles.location = (951.8352661132812, -247.0377197265625)
    align_handles.node_tree = create_align_handles_group()
    align_handles.bl_label = "Group"
    # Links for align_handles
    links.new(align_handles.outputs[0], join_geometry_001.inputs[0])
    links.new(switch.outputs[0], align_handles.inputs[1])

    align_handles_1 = nodes.new("GeometryNodeGroup")
    align_handles_1.name = "Group.025"
    align_handles_1.label = ""
    align_handles_1.location = (1229.7374267578125, -203.523193359375)
    align_handles_1.node_tree = create_align_handles_group()
    align_handles_1.bl_label = "Group"
    # Links for align_handles_1
    links.new(align_handles_1.outputs[1], join_geometry_001.inputs[0])
    links.new(align_handles.outputs[1], align_handles_1.inputs[1])
    links.new(align_handles_1.outputs[0], join_geometry_001.inputs[0])

    align_handles_2 = nodes.new("GeometryNodeGroup")
    align_handles_2.name = "Group.027"
    align_handles_2.label = ""
    align_handles_2.location = (715.73388671875, -214.32705688476562)
    align_handles_2.node_tree = create_align_handles_group()
    align_handles_2.bl_label = "Group"
    # Links for align_handles_2
    links.new(align_handles_2.outputs[1], align_handles.inputs[0])
    links.new(switch_003.outputs[0], align_handles_2.inputs[0])
    links.new(switch_002.outputs[0], align_handles_2.inputs[1])

    align_handles_3 = nodes.new("GeometryNodeGroup")
    align_handles_3.name = "Group.028"
    align_handles_3.label = ""
    align_handles_3.location = (969.6356201171875, -17.4246826171875)
    align_handles_3.node_tree = create_align_handles_group()
    align_handles_3.bl_label = "Group"
    # Links for align_handles_3
    links.new(align_handles_2.outputs[0], align_handles_3.inputs[0])
    links.new(align_handles_3.outputs[1], align_handles_1.inputs[0])
    links.new(align_handles_3.outputs[0], join_geometry_001.inputs[0])
    links.new(switch_001.outputs[0], align_handles_3.inputs[1])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (1645.718994140625, 449.803955078125)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh
    links.new(separate_components.outputs[1], curve_to_mesh.inputs[0])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (1113.176025390625, 114.134765625)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003
    links.new(switch.outputs[0], join_geometry_003.inputs[0])
    links.new(switch_003.outputs[0], join_geometry_003.inputs[0])
    links.new(switch_001.outputs[0], join_geometry_003.inputs[0])
    links.new(switch_002.outputs[0], join_geometry_003.inputs[0])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_recreate_curves_from_mesh_group():
    """
    Recreate Bezier curves from a mesh with handle attributes stored on edges.
    
    The mesh has per-edge attributes: handle_start_x/y/z (for edge.verts[0])
    and handle_end_x/y/z (for edge.verts[1]).
    
    Strategy:
    1. Capture handle vectors from edge domain BEFORE mesh-to-curve conversion
    2. Convert mesh edges to Bezier curves
    3. Use captured values (now on curve points) to set handle positions
    """
    group_name = "RecreateCurvesFromMesh"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    
    # Input/Output
    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.location = (-1200.0, 0.0)

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.location = (1400.0, 0.0)
    group_output.is_active_output = True

    # ============================================================
    # STEP 1: Read handle attributes from mesh edges (BEFORE conversion)
    # ============================================================
    
    # --- Named Attributes for handle_start (x, y, z) ---
    named_attr_start_x = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_start_x.name = "Named Attr Start X"
    named_attr_start_x.location = (-1000.0, 400.0)
    named_attr_start_x.data_type = "FLOAT"
    named_attr_start_x.inputs[0].default_value = "handle_start_x"

    named_attr_start_y = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_start_y.name = "Named Attr Start Y"
    named_attr_start_y.location = (-1000.0, 300.0)
    named_attr_start_y.data_type = "FLOAT"
    named_attr_start_y.inputs[0].default_value = "handle_start_y"

    named_attr_start_z = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_start_z.name = "Named Attr Start Z"
    named_attr_start_z.location = (-1000.0, 200.0)
    named_attr_start_z.data_type = "FLOAT"
    named_attr_start_z.inputs[0].default_value = "handle_start_z"

    # Combine handle_start into vector
    combine_start = nodes.new("ShaderNodeCombineXYZ")
    combine_start.name = "Combine Start"
    combine_start.location = (-800.0, 300.0)
    links.new(named_attr_start_x.outputs[0], combine_start.inputs[0])
    links.new(named_attr_start_y.outputs[0], combine_start.inputs[1])
    links.new(named_attr_start_z.outputs[0], combine_start.inputs[2])

    # --- Named Attributes for handle_end (x, y, z) ---
    named_attr_end_x = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_end_x.name = "Named Attr End X"
    named_attr_end_x.location = (-1000.0, -100.0)
    named_attr_end_x.data_type = "FLOAT"
    named_attr_end_x.inputs[0].default_value = "handle_end_x"

    named_attr_end_y = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_end_y.name = "Named Attr End Y"
    named_attr_end_y.location = (-1000.0, -200.0)
    named_attr_end_y.data_type = "FLOAT"
    named_attr_end_y.inputs[0].default_value = "handle_end_y"

    named_attr_end_z = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_end_z.name = "Named Attr End Z"
    named_attr_end_z.location = (-1000.0, -300.0)
    named_attr_end_z.data_type = "FLOAT"
    named_attr_end_z.inputs[0].default_value = "handle_end_z"

    # Combine handle_end into vector
    combine_end = nodes.new("ShaderNodeCombineXYZ")
    combine_end.name = "Combine End"
    combine_end.location = (-800.0, -200.0)
    links.new(named_attr_end_x.outputs[0], combine_end.inputs[0])
    links.new(named_attr_end_y.outputs[0], combine_end.inputs[1])
    links.new(named_attr_end_z.outputs[0], combine_end.inputs[2])

    # ============================================================
    # STEP 2: Capture handle vectors on EDGE domain before conversion
    # This preserves the data through the mesh-to-curve conversion
    # ============================================================
    
    # Capture handle_start vector
    # In Blender 4.x, we need to add capture_items to define the data type
    capture_start = nodes.new("GeometryNodeCaptureAttribute")
    capture_start.name = "Capture Start"
    capture_start.location = (-600.0, 200.0)
    capture_start.domain = "EDGE"
    # Add a capture item for vector data (enum is 'VECTOR' not 'FLOAT_VECTOR')
    capture_start.capture_items.new('VECTOR', "HandleStart")
    # inputs[0]=Geometry, inputs[1]=Value (vector); outputs[0]=Geometry, outputs[1]=Attribute
    links.new(group_input.outputs[0], capture_start.inputs[0])  # Geometry
    links.new(combine_start.outputs[0], capture_start.inputs[1])  # Value (vector)
    
    # Capture handle_end vector (chained from capture_start)
    capture_end = nodes.new("GeometryNodeCaptureAttribute")
    capture_end.name = "Capture End"
    capture_end.location = (-400.0, 100.0)
    capture_end.domain = "EDGE"
    # Add a capture item for vector data (enum is 'VECTOR' not 'FLOAT_VECTOR')
    capture_end.capture_items.new('VECTOR', "HandleEnd")
    links.new(capture_start.outputs[0], capture_end.inputs[0])  # Geometry from previous capture
    links.new(combine_end.outputs[0], capture_end.inputs[1])  # Value (vector)

    # ============================================================
    # STEP 3: Convert mesh edges to Bezier curves
    # The captured attributes will transfer to curve points
    # ============================================================
    
    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.location = (-200.0, 0.0)
    mesh_to_curve.mode = "EDGES"
    mesh_to_curve.inputs[1].default_value = True  # Selection
    links.new(capture_end.outputs[0], mesh_to_curve.inputs[0])

    # Set Spline Type to BEZIER
    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.location = (0.0, 0.0)
    set_spline_type.spline_type = "BEZIER"
    set_spline_type.inputs[1].default_value = True
    links.new(mesh_to_curve.outputs[0], set_spline_type.inputs[0])

    # Set Handle Type to FREE (so we can set positions manually)
    set_handle_type = nodes.new("GeometryNodeCurveSetHandles")
    set_handle_type.name = "Set Handle Type"
    set_handle_type.location = (200.0, 0.0)
    set_handle_type.handle_type = "FREE"
    set_handle_type.mode = {'LEFT', 'RIGHT'}
    set_handle_type.inputs[1].default_value = True
    links.new(set_spline_type.outputs[0], set_handle_type.inputs[0])

    # ============================================================
    # STEP 4: Select first/last points of each spline
    # ============================================================
    
    # Endpoint Selection for FIRST point (start_size=1, end_size=0)
    endpoint_first = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_first.name = "Endpoint First"
    endpoint_first.location = (400.0, 200.0)
    endpoint_first.inputs[0].default_value = 1  # start_size
    endpoint_first.inputs[1].default_value = 0  # end_size

    # Endpoint Selection for LAST point (start_size=0, end_size=1)
    endpoint_last = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_last.name = "Endpoint Last"
    endpoint_last.location = (400.0, -200.0)
    endpoint_last.inputs[0].default_value = 0  # start_size
    endpoint_last.inputs[1].default_value = 1  # end_size

    # ============================================================
    # STEP 5: Set handle positions using captured values
    # - First point's RIGHT handle = handle_start (pointing toward 2nd point)
    # - Last point's LEFT handle = handle_end (pointing toward 1st point)
    # ============================================================
    
    # Set Handle Positions for FIRST point (handle_start → RIGHT handle)
    set_handle_first = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_first.name = "Set Handle First"
    set_handle_first.location = (700.0, 100.0)
    set_handle_first.mode = "RIGHT"
    set_handle_first.inputs[3].default_value = Vector((0.0, 0.0, 0.0))  # Offset
    links.new(set_handle_type.outputs[0], set_handle_first.inputs[0])  # Curve
    links.new(endpoint_first.outputs[0], set_handle_first.inputs[1])  # Selection
    links.new(capture_start.outputs[1], set_handle_first.inputs[2])  # Position = captured handle_start

    # Set Handle Positions for LAST point (handle_end → LEFT handle)
    set_handle_last = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_last.name = "Set Handle Last"
    set_handle_last.location = (1000.0, 0.0)
    set_handle_last.mode = "LEFT"
    set_handle_last.inputs[3].default_value = Vector((0.0, 0.0, 0.0))  # Offset
    links.new(set_handle_first.outputs[0], set_handle_last.inputs[0])  # Curve (chained)
    links.new(endpoint_last.outputs[0], set_handle_last.inputs[1])  # Selection
    links.new(capture_end.outputs[1], set_handle_last.inputs[2])  # Position = captured handle_end

    # --- Final output ---
    links.new(set_handle_last.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group