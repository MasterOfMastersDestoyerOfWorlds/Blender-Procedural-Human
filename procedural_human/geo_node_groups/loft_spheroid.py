"""
Loft Spheroid geometry node groups for procedural mesh generation.
Moved from tmp/temp_25.py - contains the LoftSpheriod node group and its dependencies.
"""
import bpy
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import create_node, link_or_set, vec_math_op, math_op, get_or_rebuild_node_group

def get_bundled_node_group(name: str):
    """
    Get a bundled Blender node group by name.
    These are node groups from Blender's Essentials asset library.
    
    Args:
        name: Name of the bundled node group (e.g., "Array")
    
    Returns:
        The node group, or None if not found
    """
    if name in bpy.data.node_groups:
        return bpy.data.node_groups[name]
    import os
    blender_version = bpy.app.version_string.split()[0]
    possible_paths = [
        os.path.join(os.path.dirname(bpy.app.binary_path), blender_version, "datafiles", "assets", "geometry_nodes", "essentials.blend"),
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
    return None

def create_array_group():
    """
    Get or create the Array node group.
    This is a bundled Blender asset from the Essentials library.
    """
    existing = get_bundled_node_group("Array")
    if existing:
        return existing
    return None

@geo_node_group
def create_set_axis_group():
    group_name = "SetAxis"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Object", in_out="INPUT", socket_type="NodeSocketObject")
    socket.default_value = None
    socket = group.interface.new_socket(name="Name", in_out="INPUT", socket_type="NodeSocketString")
    socket.default_value = "axis+"
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    store_named_attribute_001.inputs[3].default_value = True
    links.new(group_input.outputs[0], store_named_attribute_001.inputs[0])
    links.new(store_named_attribute_001.outputs[0], group_output.inputs[0])
    links.new(group_input.outputs[2], store_named_attribute_001.inputs[2])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.operation = "DISTANCE"
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math.inputs[3].default_value = 1.0

    position = nodes.new("GeometryNodeInputPosition")

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    links.new(sample_index_002.outputs[0], vector_math.inputs[0])
    links.new(position.outputs[0], sample_index_002.inputs[1])
    links.new(group_input.outputs[0], sample_index_002.inputs[0])

    index_003 = nodes.new("GeometryNodeInputIndex")
    links.new(index_003.outputs[0], sample_index_002.inputs[2])

    object_info = nodes.new("GeometryNodeObjectInfo")
    object_info.transform_space = "ORIGINAL"
    object_info.inputs[1].default_value = False
    links.new(object_info.outputs[1], vector_math.inputs[1])
    links.new(group_input.outputs[1], object_info.inputs[0])

    compare_007 = nodes.new("FunctionNodeCompare")
    compare_007.operation = "LESS_EQUAL"
    compare_007.data_type = "FLOAT"
    compare_007.mode = "ELEMENT"
    compare_007.inputs[1].default_value = 0.009999999776482582
    compare_007.inputs[2].default_value = 0
    compare_007.inputs[3].default_value = 0
    compare_007.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_007.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_007.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_007.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_007.inputs[8].default_value = ""
    compare_007.inputs[9].default_value = ""
    compare_007.inputs[10].default_value = 0.8999999761581421
    compare_007.inputs[11].default_value = 0.08726649731397629
    compare_007.inputs[12].default_value = 0.0010000000474974513
    links.new(vector_math.outputs[1], compare_007.inputs[0])
    links.new(compare_007.outputs[0], store_named_attribute_001.inputs[1])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_weld__curves_group():
    group_name = "Weld Curves"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")

    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.component = "CURVE"

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.mode = "POINTS"
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    curve_line.inputs[1].default_value = Vector((0.0, 0.0, 1.0))
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    curve_line.inputs[3].default_value = 1.0

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = False
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Count"
    resample_curve.inputs[4].default_value = 0.10000000149011612
    links.new(domain_size.outputs[0], resample_curve.inputs[3])
    links.new(curve_line.outputs[0], resample_curve.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.socket_idname = "NodeSocketGeometry"
    links.new(resample_curve.outputs[0], reroute_002.inputs[0])

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.spline_type = "BEZIER"
    set_spline_type.inputs[1].default_value = True
    links.new(reroute_002.outputs[0], set_spline_type.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.inputs[1].default_value = True
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketGeometry"
    links.new(set_position.outputs[0], reroute_001.inputs[0])

    set_handle_positions = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions.mode = "LEFT"
    set_handle_positions.inputs[1].default_value = True
    set_handle_positions.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(reroute_001.outputs[0], set_handle_positions.inputs[0])

    set_handle_positions_001 = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions_001.mode = "RIGHT"
    set_handle_positions_001.inputs[1].default_value = True
    set_handle_positions_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(set_handle_positions.outputs[0], set_handle_positions_001.inputs[0])

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.socket_idname = "NodeSocketInt"

    position = nodes.new("GeometryNodeInputPosition")

    curve_handle_positions = nodes.new("GeometryNodeInputCurveHandlePositions")
    curve_handle_positions.inputs[0].default_value = False

    reroute_004 = nodes.new("NodeReroute")
    reroute_004.socket_idname = "NodeSocketGeometry"

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    links.new(reroute_004.outputs[0], sample_index.inputs[0])
    links.new(sample_index.outputs[0], set_position.inputs[2])
    links.new(position.outputs[0], sample_index.inputs[1])
    links.new(reroute_003.outputs[0], sample_index.inputs[2])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "GEOMETRY"
    links.new(set_spline_type.outputs[0], switch_001.inputs[2])
    links.new(reroute_002.outputs[0], switch_001.inputs[1])
    links.new(switch_001.outputs[0], set_position.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.socket_idname = "NodeSocketGeometry"
    links.new(reroute.outputs[0], domain_size.inputs[0])
    links.new(reroute.outputs[0], reroute_004.inputs[0])
    links.new(group_input.outputs[0], reroute.inputs[0])

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.data_type = "FLOAT"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    links.new(group_input.outputs[0], sample_index_005.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    compare.inputs[1].default_value = 2.0
    compare.inputs[3].default_value = 2
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare.inputs[6].default_value = [0.0, 0.0, 0.0, 0.0]
    compare.inputs[7].default_value = [0.0, 0.0, 0.0, 0.0]
    compare.inputs[8].default_value = ""
    compare.inputs[9].default_value = ""
    compare.inputs[10].default_value = 0.8999999761581421
    compare.inputs[11].default_value = 0.08726649731397629
    compare.inputs[12].default_value = 0.0010000000474974513
    links.new(sample_index_005.outputs[0], compare.inputs[2])

    integer = nodes.new("FunctionNodeInputInt")
    integer.integer = 0
    links.new(integer.outputs[0], sample_index_005.inputs[2])

    reroute_005 = nodes.new("NodeReroute")
    reroute_005.socket_idname = "NodeSocketBool"
    links.new(reroute_005.outputs[0], switch_001.inputs[0])
    links.new(compare.outputs[0], reroute_005.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.data_type = "INT"
    named_attribute.inputs[0].default_value = "curve_type"
    links.new(named_attribute.outputs[0], sample_index_005.inputs[1])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    links.new(reroute_004.outputs[0], sample_index_001.inputs[0])
    links.new(curve_handle_positions.outputs[0], sample_index_001.inputs[1])
    links.new(sample_index_001.outputs[0], set_handle_positions.inputs[2])
    links.new(reroute_003.outputs[0], sample_index_001.inputs[2])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    links.new(reroute_003.outputs[0], sample_index_002.inputs[2])
    links.new(curve_handle_positions.outputs[1], sample_index_002.inputs[1])
    links.new(reroute_004.outputs[0], sample_index_002.inputs[0])
    links.new(sample_index_002.outputs[0], set_handle_positions_001.inputs[2])

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.data_type = "FLOAT"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    links.new(reroute_003.outputs[0], sample_index_003.inputs[2])

    curve_tilt = nodes.new("GeometryNodeInputCurveTilt")
    links.new(curve_tilt.outputs[0], sample_index_003.inputs[1])

    radius = nodes.new("GeometryNodeInputRadius")

    reroute_006 = nodes.new("NodeReroute")
    reroute_006.socket_idname = "NodeSocketGeometry"
    links.new(reroute_006.outputs[0], sample_index_003.inputs[0])
    links.new(reroute_004.outputs[0], reroute_006.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.inputs[1].default_value = True
    links.new(sample_index_003.outputs[0], set_curve_tilt.inputs[2])

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "GEOMETRY"
    links.new(reroute_001.outputs[0], switch.inputs[1])
    links.new(set_handle_positions_001.outputs[0], switch.inputs[2])
    links.new(switch.outputs[0], set_curve_tilt.inputs[0])
    links.new(reroute_005.outputs[0], switch.inputs[0])

    set_curve_radius = nodes.new("GeometryNodeSetCurveRadius")
    set_curve_radius.inputs[1].default_value = True
    links.new(set_curve_tilt.outputs[0], set_curve_radius.inputs[0])
    links.new(set_curve_radius.outputs[0], group_output.inputs[0])

    sample_index_004 = nodes.new("GeometryNodeSampleIndex")
    sample_index_004.data_type = "FLOAT"
    sample_index_004.domain = "POINT"
    sample_index_004.clamp = False
    links.new(reroute_003.outputs[0], sample_index_004.inputs[2])
    links.new(reroute_006.outputs[0], sample_index_004.inputs[0])
    links.new(radius.outputs[0], sample_index_004.inputs[1])
    links.new(sample_index_004.outputs[0], set_curve_radius.inputs[2])

    viewer = nodes.new("GeometryNodeViewer")
    viewer.ui_shortcut = 0
    viewer.active_index = 0
    viewer.domain = "AUTO"
    links.new(set_curve_radius.outputs[0], viewer.inputs[0])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.data_type = "FLOAT"
    named_attribute_001.inputs[0].default_value = ""

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.operation = "FLOORED_MODULO"
    integer_math.inputs[2].default_value = 0
    links.new(domain_size.outputs[0], integer_math.inputs[1])
    links.new(group_input.outputs[1], integer_math.inputs[0])
    links.new(integer_math.outputs[0], reroute_003.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_split_curves_about_axis_group():
    group_name = "SplitCurvesAboutAxis"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
    socket = group.interface.new_socket(name="CurvePos", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveNeg", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Curve", in_out="INPUT", socket_type="NodeSocketGeometry")
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = False
    sample_curve.data_type = "FLOAT"
    sample_curve.inputs[1].default_value = 0.0
    sample_curve.inputs[2].default_value = 0.0
    sample_curve.inputs[3].default_value = 0.0
    sample_curve.inputs[4].default_value = 0

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.data_type = "BOOLEAN"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    links.new(group_input.outputs[0], sample_index_002.inputs[0])

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.data_type = "FLOAT"
    attribute_statistic.domain = "POINT"
    links.new(sample_index_002.outputs[0], attribute_statistic.inputs[1])
    links.new(group_input.outputs[0], attribute_statistic.inputs[0])

    index_003 = nodes.new("GeometryNodeInputIndex")
    links.new(index_003.outputs[0], attribute_statistic.inputs[2])
    links.new(index_003.outputs[0], sample_index_002.inputs[2])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.data_type = "BOOLEAN"
    named_attribute.inputs[0].default_value = "axis+"
    links.new(named_attribute.outputs[0], sample_index_002.inputs[1])

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.data_type = "BOOLEAN"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    links.new(group_input.outputs[0], sample_index_003.inputs[0])

    attribute_statistic_001 = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_001.data_type = "FLOAT"
    attribute_statistic_001.domain = "POINT"
    links.new(sample_index_003.outputs[0], attribute_statistic_001.inputs[1])
    links.new(group_input.outputs[0], attribute_statistic_001.inputs[0])

    index_005 = nodes.new("GeometryNodeInputIndex")
    links.new(index_005.outputs[0], attribute_statistic_001.inputs[2])
    links.new(index_005.outputs[0], sample_index_003.inputs[2])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.data_type = "BOOLEAN"
    named_attribute_001.inputs[0].default_value = "axis-"
    links.new(named_attribute_001.outputs[0], sample_index_003.inputs[1])

    separate_geometry_004 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_004.domain = "POINT"
    links.new(group_input.outputs[0], separate_geometry_004.inputs[0])

    compare_007 = nodes.new("FunctionNodeCompare")
    compare_007.operation = "GREATER_EQUAL"
    compare_007.data_type = "INT"
    compare_007.mode = "ELEMENT"
    compare_007.inputs[0].default_value = 0.0
    compare_007.inputs[1].default_value = 0.0
    compare_007.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_007.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_007.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_007.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_007.inputs[8].default_value = ""
    compare_007.inputs[9].default_value = ""
    compare_007.inputs[10].default_value = 0.8999999761581421
    compare_007.inputs[11].default_value = 0.08726649731397629
    compare_007.inputs[12].default_value = 0.0010000000474974513
    links.new(index_003.outputs[0], compare_007.inputs[2])

    compare_008 = nodes.new("FunctionNodeCompare")
    compare_008.operation = "LESS_EQUAL"
    compare_008.data_type = "INT"
    compare_008.mode = "ELEMENT"
    compare_008.inputs[0].default_value = 0.0
    compare_008.inputs[1].default_value = 0.0
    compare_008.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_008.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_008.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_008.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_008.inputs[8].default_value = ""
    compare_008.inputs[9].default_value = ""
    compare_008.inputs[10].default_value = 0.8999999761581421
    compare_008.inputs[11].default_value = 0.08726649731397629
    compare_008.inputs[12].default_value = 0.0010000000474974513
    links.new(index_003.outputs[0], compare_008.inputs[2])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "AND"
    links.new(compare_007.outputs[0], boolean_math.inputs[0])
    links.new(compare_008.outputs[0], boolean_math.inputs[1])
    links.new(boolean_math.outputs[0], separate_geometry_004.inputs[1])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.inputs[1].default_value = True
    set_spline_cyclic.inputs[2].default_value = False
    links.new(separate_geometry_004.outputs[0], set_spline_cyclic.inputs[0])
    links.new(set_spline_cyclic.outputs[0], group_output.inputs[1])

    compare_009 = nodes.new("FunctionNodeCompare")
    compare_009.operation = "LESS_EQUAL"
    compare_009.data_type = "INT"
    compare_009.mode = "ELEMENT"
    compare_009.inputs[0].default_value = 0.0
    compare_009.inputs[1].default_value = 0.0
    compare_009.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_009.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_009.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_009.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_009.inputs[8].default_value = ""
    compare_009.inputs[9].default_value = ""
    compare_009.inputs[10].default_value = 0.8999999761581421
    compare_009.inputs[11].default_value = 0.08726649731397629
    compare_009.inputs[12].default_value = 0.0010000000474974513
    links.new(index_003.outputs[0], compare_009.inputs[2])

    compare_010 = nodes.new("FunctionNodeCompare")
    compare_010.operation = "GREATER_EQUAL"
    compare_010.data_type = "INT"
    compare_010.mode = "ELEMENT"
    compare_010.inputs[0].default_value = 0.0
    compare_010.inputs[1].default_value = 0.0
    compare_010.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_010.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_010.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_010.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_010.inputs[8].default_value = ""
    compare_010.inputs[9].default_value = ""
    compare_010.inputs[10].default_value = 0.8999999761581421
    compare_010.inputs[11].default_value = 0.08726649731397629
    compare_010.inputs[12].default_value = 0.0010000000474974513
    links.new(index_003.outputs[0], compare_010.inputs[2])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.operation = "OR"
    links.new(compare_009.outputs[0], boolean_math_001.inputs[0])
    links.new(compare_010.outputs[0], boolean_math_001.inputs[1])

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.socket_idname = "NodeSocketGeometry"
    links.new(group_input.outputs[0], reroute_003.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "INT"
    links.new(attribute_statistic_001.outputs[3], switch.inputs[2])
    links.new(attribute_statistic.outputs[4], switch.inputs[1])
    links.new(switch.outputs[0], compare_010.inputs[3])
    links.new(switch.outputs[0], compare_008.inputs[3])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "GREATER_THAN"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    compare.inputs[2].default_value = 0
    compare.inputs[3].default_value = 0
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[8].default_value = ""
    compare.inputs[9].default_value = ""
    compare.inputs[10].default_value = 0.8999999761581421
    compare.inputs[11].default_value = 0.08726649731397629
    compare.inputs[12].default_value = 0.0010000000474974513
    links.new(attribute_statistic_001.outputs[3], compare.inputs[0])
    links.new(attribute_statistic.outputs[4], compare.inputs[1])
    links.new(compare.outputs[0], switch.inputs[0])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "INT"
    links.new(compare.outputs[0], switch_001.inputs[0])
    links.new(attribute_statistic.outputs[4], switch_001.inputs[2])
    links.new(attribute_statistic_001.outputs[3], switch_001.inputs[1])
    links.new(switch_001.outputs[0], compare_009.inputs[3])
    links.new(switch_001.outputs[0], compare_007.inputs[3])

    separate_geometry_005 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_005.domain = "POINT"
    links.new(boolean_math_001.outputs[0], separate_geometry_005.inputs[1])
    links.new(group_input.outputs[0], separate_geometry_005.inputs[0])

    set_spline_cyclic_002 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_002.inputs[1].default_value = True
    set_spline_cyclic_002.inputs[2].default_value = False
    links.new(separate_geometry_005.outputs[0], set_spline_cyclic_002.inputs[0])

    weld_curves = nodes.new("GeometryNodeGroup")
    weld_curves.node_tree = create_weld__curves_group()
    links.new(set_spline_cyclic_002.outputs[0], weld_curves.inputs[0])
    links.new(weld_curves.outputs[0], group_output.inputs[0])

    index_007 = nodes.new("GeometryNodeInputIndex")

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.operation = "ADD"
    integer_math.inputs[2].default_value = 0
    links.new(integer_math.outputs[0], weld_curves.inputs[1])
    links.new(index_007.outputs[0], integer_math.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.operation = "SUBTRACT"
    math.use_clamp = False
    math.inputs[1].default_value = 1.0
    math.inputs[2].default_value = 0.5
    links.new(attribute_statistic_001.outputs[3], math.inputs[0])
    links.new(math.outputs[0], integer_math.inputs[1])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_get_axis_group():
    group_name = "GetAxis"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
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
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.data_type = "FLOAT"
    attribute_statistic.domain = "POINT"
    attribute_statistic.inputs[1].default_value = True
    links.new(group_input.outputs[0], attribute_statistic.inputs[0])

    attribute_statistic_001 = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_001.data_type = "FLOAT"
    attribute_statistic_001.domain = "POINT"
    links.new(group_input.outputs[0], attribute_statistic_001.inputs[0])
    links.new(attribute_statistic_001.outputs[3], group_output.inputs[0])
    links.new(attribute_statistic_001.outputs[4], group_output.inputs[1])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    compare.inputs[2].default_value = 0
    compare.inputs[3].default_value = 0
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[8].default_value = ""
    compare.inputs[9].default_value = ""
    compare.inputs[10].default_value = 0.8999999761581421
    compare.inputs[11].default_value = 0.08726649731397629
    compare.inputs[12].default_value = 0.0010000000474974513
    links.new(attribute_statistic.outputs[3], compare.inputs[1])
    links.new(compare.outputs[0], attribute_statistic_001.inputs[1])

    index_003 = nodes.new("GeometryNodeInputIndex")
    links.new(index_003.outputs[0], attribute_statistic_001.inputs[2])

    position = nodes.new("GeometryNodeInputPosition")

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    links.new(position.outputs[0], sample_index.inputs[1])
    links.new(group_input.outputs[1], sample_index.inputs[0])
    links.new(index_003.outputs[0], sample_index.inputs[2])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    links.new(position.outputs[0], sample_index_001.inputs[1])
    links.new(index_003.outputs[0], sample_index_001.inputs[2])
    links.new(group_input.outputs[0], sample_index_001.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.operation = "DISTANCE"
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math.inputs[3].default_value = 1.0
    links.new(sample_index_001.outputs[0], vector_math.inputs[0])
    links.new(sample_index.outputs[0], vector_math.inputs[1])
    links.new(vector_math.outputs[1], attribute_statistic.inputs[2])
    links.new(vector_math.outputs[1], compare.inputs[0])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    links.new(position.outputs[0], sample_index_002.inputs[1])
    links.new(group_input.outputs[0], sample_index_002.inputs[0])
    links.new(sample_index_002.outputs[0], group_output.inputs[2])
    links.new(attribute_statistic_001.outputs[3], sample_index_002.inputs[2])

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.data_type = "FLOAT_VECTOR"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    links.new(attribute_statistic_001.outputs[4], sample_index_003.inputs[2])
    links.new(group_input.outputs[0], sample_index_003.inputs[0])
    links.new(sample_index_003.outputs[0], group_output.inputs[3])
    links.new(position.outputs[0], sample_index_003.inputs[1])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.operation = "SUBTRACT"
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[3].default_value = 1.0
    links.new(sample_index_002.outputs[0], vector_math_001.inputs[0])
    links.new(sample_index_003.outputs[0], vector_math_001.inputs[1])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.operation = "NORMALIZE"
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[3].default_value = 1.0
    links.new(vector_math_002.outputs[0], group_output.inputs[4])
    links.new(vector_math_001.outputs[0], vector_math_002.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_orient_curve_group():
    group_name = "OrientCurve"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
    socket = group.interface.new_socket(name="CurveA", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveB", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveA", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="CurveB", in_out="INPUT", socket_type="NodeSocketGeometry")
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")
    links.new(group_input.outputs[0], group_output.inputs[0])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    sample_index_001.inputs[2].default_value = 0
    links.new(group_input.outputs[0], sample_index_001.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")
    links.new(position_001.outputs[0], sample_index_001.inputs[1])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "NOT_EQUAL"
    compare.data_type = "VECTOR"
    compare.mode = "ELEMENT"
    compare.inputs[0].default_value = 0.0
    compare.inputs[1].default_value = 0.0
    compare.inputs[2].default_value = 0
    compare.inputs[3].default_value = 0
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[8].default_value = ""
    compare.inputs[9].default_value = ""
    compare.inputs[10].default_value = 0.8999999761581421
    compare.inputs[11].default_value = 0.08726649731397629
    compare.inputs[12].default_value = 0.0010000000474974513
    links.new(sample_index_001.outputs[0], compare.inputs[4])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    sample_index_002.inputs[2].default_value = 0
    links.new(position_001.outputs[0], sample_index_002.inputs[1])
    links.new(sample_index_002.outputs[0], compare.inputs[5])
    links.new(group_input.outputs[1], sample_index_002.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "GEOMETRY"
    links.new(compare.outputs[0], switch.inputs[0])
    links.new(group_input.outputs[1], switch.inputs[1])
    links.new(switch.outputs[0], group_output.inputs[1])

    reverse_curve = nodes.new("GeometryNodeReverseCurve")
    reverse_curve.inputs[1].default_value = True
    links.new(reverse_curve.outputs[0], switch.inputs[2])
    links.new(group_input.outputs[1], reverse_curve.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_loft_curve_parts_group():
    group_name = "LoftCurveParts"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Vertices Y", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 3
    socket.min_value = 2
    socket.max_value = 1000
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketGeometry"

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.inputs[0].default_value = 1.0
    grid.inputs[1].default_value = 1.0
    links.new(group_input.outputs[1], grid.inputs[3]) 

    domain_size_002 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_002.component = "CURVE"
    links.new(reroute_001.outputs[0], domain_size_002.inputs[0])
    links.new(domain_size_002.outputs[4], grid.inputs[2])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False

    position_001 = nodes.new("GeometryNodeInputPosition")
    links.new(position_001.outputs[0], sample_index_001.inputs[1])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.inputs[1].default_value = True
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(grid.outputs[0], set_position.inputs[0])
    links.new(set_position.outputs[0], group_output.inputs[0])
    links.new(sample_index_001.outputs[0], set_position.inputs[2])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.inputs[2].default_value = 1.0
    curve_to_mesh.inputs[3].default_value = False
    links.new(curve_to_mesh.outputs[0], sample_index_001.inputs[0])
    links.new(reroute_001.outputs[0], curve_to_mesh.inputs[0])

    index_002 = nodes.new("GeometryNodeInputIndex")
    links.new(index_002.outputs[0], sample_index_001.inputs[2])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Count"
    resample_curve.inputs[4].default_value = 0.10000000149011612
    links.new(resample_curve.outputs[0], reroute_001.inputs[0])
    links.new(group_input.outputs[0], resample_curve.inputs[0])
    links.new(group_input.outputs[1], resample_curve.inputs[3])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create__axis_alignment_switch_group():
    group_name = ".axis_alignment_switch"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
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
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    menu_switch_007 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_007.active_index = 2
    menu_switch_007.data_type = "INT"
    menu_switch_007.inputs[1].default_value = 0
    menu_switch_007.inputs[2].default_value = 1
    menu_switch_007.inputs[3].default_value = 2
    links.new(group_input.outputs[0], menu_switch_007.inputs[0])

    menu_switch_008 = nodes.new("GeometryNodeMenuSwitch")
    menu_switch_008.active_index = 2
    menu_switch_008.data_type = "INT"
    menu_switch_008.inputs[1].default_value = 0
    menu_switch_008.inputs[2].default_value = 1
    menu_switch_008.inputs[3].default_value = 2
    links.new(group_input.outputs[1], menu_switch_008.inputs[0])

    axes_to_rotation_004 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_004.primary_axis = "X"
    axes_to_rotation_004.secondary_axis = "Y"

    axes_to_rotation_005 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_005.primary_axis = "X"
    axes_to_rotation_005.secondary_axis = "Z"

    index_switch_012 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_012.data_type = "ROTATION"
    links.new(menu_switch_007.outputs[0], index_switch_012.inputs[0])

    index_switch_013 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_013.data_type = "ROTATION"
    index_switch_013.inputs[1].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    links.new(axes_to_rotation_004.outputs[0], index_switch_013.inputs[2])
    links.new(axes_to_rotation_005.outputs[0], index_switch_013.inputs[3])
    links.new(index_switch_013.outputs[0], index_switch_012.inputs[1])

    index_switch_014 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_014.data_type = "ROTATION"
    index_switch_014.inputs[2].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    links.new(index_switch_014.outputs[0], index_switch_012.inputs[2])

    index_switch_015 = nodes.new("GeometryNodeIndexSwitch")
    index_switch_015.data_type = "ROTATION"
    index_switch_015.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    links.new(index_switch_015.outputs[0], index_switch_012.inputs[3])

    reroute_056 = nodes.new("NodeReroute")
    reroute_056.socket_idname = "NodeSocketInt"
    links.new(reroute_056.outputs[0], index_switch_014.inputs[0])
    links.new(reroute_056.outputs[0], index_switch_013.inputs[0])
    links.new(menu_switch_008.outputs[0], reroute_056.inputs[0])
    links.new(reroute_056.outputs[0], index_switch_015.inputs[0])

    axes_to_rotation_006 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_006.primary_axis = "Y"
    axes_to_rotation_006.secondary_axis = "X"
    links.new(axes_to_rotation_006.outputs[0], index_switch_014.inputs[1])

    axes_to_rotation_007 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_007.primary_axis = "Y"
    axes_to_rotation_007.secondary_axis = "Z"
    links.new(axes_to_rotation_007.outputs[0], index_switch_014.inputs[3])

    axes_to_rotation_008 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_008.primary_axis = "Z"
    axes_to_rotation_008.secondary_axis = "X"
    links.new(axes_to_rotation_008.outputs[0], index_switch_015.inputs[1])

    axes_to_rotation_009 = nodes.new("FunctionNodeAxesToRotation")
    axes_to_rotation_009.primary_axis = "Z"
    axes_to_rotation_009.secondary_axis = "Y"
    links.new(axes_to_rotation_009.outputs[0], index_switch_015.inputs[2])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.operation = "EQUAL"
    compare_005.data_type = "INT"
    compare_005.mode = "ELEMENT"
    compare_005.inputs[0].default_value = 0.0
    compare_005.inputs[1].default_value = 0.0
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_005.inputs[8].default_value = ""
    compare_005.inputs[9].default_value = ""
    compare_005.inputs[10].default_value = 0.8999999761581421
    compare_005.inputs[11].default_value = 0.08726649731397629
    compare_005.inputs[12].default_value = 0.0010000000474974513
    links.new(menu_switch_008.outputs[0], compare_005.inputs[3])
    links.new(menu_switch_007.outputs[0], compare_005.inputs[2])

    reroute_059 = nodes.new("NodeReroute")
    reroute_059.socket_idname = "NodeSocketVector"
    links.new(reroute_059.outputs[0], axes_to_rotation_005.inputs[0])
    links.new(reroute_059.outputs[0], axes_to_rotation_004.inputs[0])
    links.new(reroute_059.outputs[0], axes_to_rotation_008.inputs[0])
    links.new(reroute_059.outputs[0], axes_to_rotation_009.inputs[0])
    links.new(reroute_059.outputs[0], axes_to_rotation_006.inputs[0])
    links.new(reroute_059.outputs[0], axes_to_rotation_007.inputs[0])
    links.new(group_input.outputs[2], reroute_059.inputs[0])

    reroute_060 = nodes.new("NodeReroute")
    reroute_060.socket_idname = "NodeSocketVector"
    links.new(reroute_060.outputs[0], axes_to_rotation_006.inputs[1])
    links.new(reroute_060.outputs[0], axes_to_rotation_009.inputs[1])
    links.new(reroute_060.outputs[0], axes_to_rotation_007.inputs[1])
    links.new(reroute_060.outputs[0], axes_to_rotation_008.inputs[1])
    links.new(reroute_060.outputs[0], axes_to_rotation_005.inputs[1])
    links.new(reroute_060.outputs[0], axes_to_rotation_004.inputs[1])
    links.new(group_input.outputs[3], reroute_060.inputs[0])

    warning_002 = nodes.new("GeometryNodeWarning")
    warning_002.warning_type = "WARNING"
    warning_002.inputs[1].default_value = "Equal Axes"
    links.new(compare_005.outputs[0], warning_002.inputs[0])

    switch_028 = nodes.new("GeometryNodeSwitch")
    switch_028.input_type = "ROTATION"
    switch_028.inputs[2].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    links.new(index_switch_012.outputs[0], switch_028.inputs[1])
    links.new(warning_002.outputs[0], switch_028.inputs[0])
    links.new(switch_028.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_debug_handles_group():
    group_name = "DebugHandles"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
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
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    mesh_line = nodes.new("GeometryNodeMeshLine")
    mesh_line.mode = "END_POINTS"
    mesh_line.count_mode = "TOTAL"
    mesh_line.inputs[0].default_value = 10
    mesh_line.inputs[1].default_value = 1.0

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.data_type = "FLOAT_VECTOR"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    links.new(sample_index_005.outputs[0], mesh_line.inputs[2])
    links.new(group_input.outputs[0], sample_index_005.inputs[0])

    sample_index_006 = nodes.new("GeometryNodeSampleIndex")
    sample_index_006.data_type = "FLOAT_VECTOR"
    sample_index_006.domain = "POINT"
    sample_index_006.clamp = False
    links.new(sample_index_006.outputs[0], mesh_line.inputs[3])
    links.new(group_input.outputs[0], sample_index_006.inputs[0])

    curve_handle_positions = nodes.new("GeometryNodeInputCurveHandlePositions")
    curve_handle_positions.inputs[0].default_value = True
    links.new(curve_handle_positions.outputs[1], sample_index_006.inputs[1])
    links.new(curve_handle_positions.outputs[0], sample_index_005.inputs[1])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.inputs[1].default_value = True
    set_position_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(mesh_line.outputs[0], set_position_002.inputs[0])

    sample_index_011 = nodes.new("GeometryNodeSampleIndex")
    sample_index_011.data_type = "FLOAT_VECTOR"
    sample_index_011.domain = "POINT"
    sample_index_011.clamp = False
    links.new(sample_index_011.outputs[0], set_position_002.inputs[3])
    links.new(group_input.outputs[0], sample_index_011.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    links.new(position_002.outputs[0], sample_index_011.inputs[1])

    mesh_line_001 = nodes.new("GeometryNodeMeshLine")
    mesh_line_001.mode = "OFFSET"
    mesh_line_001.count_mode = "TOTAL"
    mesh_line_001.inputs[0].default_value = 2
    mesh_line_001.inputs[1].default_value = 1.0
    mesh_line_001.inputs[3].default_value = Vector((0.0, 0.0, 1.0))

    sample_index_012 = nodes.new("GeometryNodeSampleIndex")
    sample_index_012.data_type = "FLOAT_VECTOR"
    sample_index_012.domain = "POINT"
    sample_index_012.clamp = False
    links.new(sample_index_012.outputs[0], mesh_line_001.inputs[2])
    links.new(group_input.outputs[0], sample_index_012.inputs[0])
    links.new(group_input.outputs[2], sample_index_012.inputs[1])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    links.new(mesh_line_001.outputs[0], join_geometry.inputs[0])
    links.new(set_position_002.outputs[0], join_geometry.inputs[0])
    links.new(join_geometry.outputs[0], group_output.inputs[0])

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.component = "CURVE"
    links.new(group_input.outputs[0], domain_size.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.operation = "SUBTRACT"
    math.use_clamp = False
    math.inputs[1].default_value = 1.0
    math.inputs[2].default_value = 0.5
    links.new(domain_size.outputs[4], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.operation = "SUBTRACT"
    math_001.use_clamp = False
    math_001.inputs[2].default_value = 0.5
    links.new(math.outputs[0], math_001.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    math_002.inputs[1].default_value = 2.0
    math_002.inputs[2].default_value = 0.5
    links.new(math_001.outputs[0], math_002.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "INT"
    links.new(switch.outputs[0], sample_index_012.inputs[2])
    links.new(group_input.outputs[1], switch.inputs[2])
    links.new(switch.outputs[0], sample_index_011.inputs[2])
    links.new(switch.outputs[0], sample_index_006.inputs[2])
    links.new(switch.outputs[0], sample_index_005.inputs[2])
    links.new(group_input.outputs[3], switch.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.operation = "DIVIDE"
    math_003.use_clamp = False
    math_003.inputs[1].default_value = 2.0
    math_003.inputs[2].default_value = 0.5
    links.new(group_input.outputs[1], math_003.inputs[0])
    links.new(math_003.outputs[0], math_001.inputs[1])

    domain_size_001 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_001.component = "CURVE"
    links.new(group_input.outputs[0], domain_size_001.inputs[0])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    math_004.inputs[1].default_value = 1.0
    math_004.inputs[2].default_value = 0.5
    links.new(domain_size_001.outputs[4], math_004.inputs[0])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.operation = "SUBTRACT"
    math_005.use_clamp = False
    math_005.inputs[2].default_value = 0.5
    links.new(math_004.outputs[0], math_005.inputs[0])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.operation = "MULTIPLY"
    math_006.use_clamp = False
    math_006.inputs[1].default_value = 2.0
    math_006.inputs[2].default_value = 0.5
    links.new(math_005.outputs[0], math_006.inputs[0])

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.operation = "ADD"
    integer_math.inputs[2].default_value = 0
    links.new(math_006.outputs[0], integer_math.inputs[0])
    links.new(integer_math.outputs[0], switch.inputs[1])

    integer_math_004 = nodes.new("FunctionNodeIntegerMath")
    integer_math_004.operation = "MODULO"
    integer_math_004.inputs[1].default_value = 2
    integer_math_004.inputs[2].default_value = 0
    links.new(integer_math_004.outputs[0], integer_math.inputs[1])
    links.new(group_input.outputs[1], integer_math_004.inputs[0])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.operation = "DIVIDE"
    math_007.use_clamp = False
    math_007.inputs[1].default_value = 2.0
    math_007.inputs[2].default_value = 0.5
    links.new(math_007.outputs[0], math_005.inputs[1])
    links.new(group_input.outputs[1], math_007.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_set_handles_group():
    group_name = "SetHandles"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
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
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    index_002 = nodes.new("GeometryNodeInputIndex")

    math_001 = nodes.new("ShaderNodeMath")
    math_001.operation = "DIVIDE"
    math_001.use_clamp = False
    math_001.inputs[1].default_value = 2.0
    math_001.inputs[2].default_value = 0.5
    links.new(index_002.outputs[0], math_001.inputs[0])

    sample_index_009 = nodes.new("GeometryNodeSampleIndex")
    sample_index_009.data_type = "FLOAT_VECTOR"
    sample_index_009.domain = "POINT"
    sample_index_009.clamp = False
    links.new(math_001.outputs[0], sample_index_009.inputs[2])
    links.new(group_input.outputs[0], sample_index_009.inputs[0])
    links.new(sample_index_009.outputs[0], group_output.inputs[2])

    position_001 = nodes.new("GeometryNodeInputPosition")
    links.new(position_001.outputs[0], sample_index_009.inputs[1])

    sample_index_010 = nodes.new("GeometryNodeSampleIndex")
    sample_index_010.data_type = "FLOAT_VECTOR"
    sample_index_010.domain = "POINT"
    sample_index_010.clamp = False
    links.new(math_001.outputs[0], sample_index_010.inputs[2])
    links.new(position_001.outputs[0], sample_index_010.inputs[1])
    links.new(group_input.outputs[3], sample_index_010.inputs[0])
    links.new(sample_index_010.outputs[0], group_output.inputs[3])

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.operation = "ADD"
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_006.inputs[3].default_value = 1.0
    links.new(sample_index_009.outputs[0], vector_math_006.inputs[0])
    links.new(sample_index_010.outputs[0], vector_math_006.inputs[1])

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.operation = "SCALE"
    vector_math_007.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(vector_math_006.outputs[0], vector_math_007.inputs[0])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.operation = "DISTANCE"
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_008.inputs[3].default_value = 1.0
    links.new(vector_math_008.outputs[1], vector_math_007.inputs[3])
    links.new(sample_index_009.outputs[0], vector_math_008.inputs[0])
    links.new(sample_index_010.outputs[0], vector_math_008.inputs[1])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.operation = "SCALE"
    vector_math.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math.inputs[3].default_value = 0.5
    links.new(vector_math_006.outputs[0], vector_math.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.socket_idname = "NodeSocketVector"
    links.new(reroute.outputs[0], group_output.inputs[0])
    links.new(reroute.outputs[0], group_output.inputs[1])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.operation = "ADD"
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[3].default_value = 1.0
    links.new(vector_math_001.outputs[0], reroute.inputs[0])
    links.new(vector_math.outputs[0], vector_math_001.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.operation = "SCALE"
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[3].default_value = 0.19999992847442627
    links.new(vector_math_002.outputs[0], vector_math_001.inputs[1])
    links.new(vector_math_007.outputs[0], vector_math_002.inputs[0])

    sample_index_011 = nodes.new("GeometryNodeSampleIndex")
    sample_index_011.data_type = "FLOAT_VECTOR"
    sample_index_011.domain = "POINT"
    sample_index_011.clamp = False
    links.new(math_001.outputs[0], sample_index_011.inputs[2])
    links.new(group_input.outputs[3], sample_index_011.inputs[0])
    links.new(group_input.outputs[5], sample_index_011.inputs[1])

    sample_index_012 = nodes.new("GeometryNodeSampleIndex")
    sample_index_012.data_type = "FLOAT_VECTOR"
    sample_index_012.domain = "POINT"
    sample_index_012.clamp = False
    links.new(math_001.outputs[0], sample_index_012.inputs[2])
    links.new(group_input.outputs[0], sample_index_012.inputs[0])
    links.new(group_input.outputs[2], sample_index_012.inputs[1])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.operation = "ADD"
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_003.inputs[3].default_value = 1.0
    links.new(sample_index_009.outputs[0], vector_math_003.inputs[1])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.operation = "ADD"
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_004.inputs[3].default_value = 1.0
    links.new(sample_index_010.outputs[0], vector_math_004.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.operation = "NORMALIZE"
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_005.inputs[3].default_value = 1.0
    links.new(sample_index_012.outputs[0], vector_math_005.inputs[0])

    vector_math_009 = nodes.new("ShaderNodeVectorMath")
    vector_math_009.operation = "NORMALIZE"
    vector_math_009.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_009.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_009.inputs[3].default_value = 1.0
    links.new(sample_index_011.outputs[0], vector_math_009.inputs[0])

    vector_math_010 = nodes.new("ShaderNodeVectorMath")
    vector_math_010.operation = "DOT_PRODUCT"
    vector_math_010.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_010.inputs[3].default_value = 1.0
    links.new(vector_math_005.outputs[0], vector_math_010.inputs[0])
    links.new(sample_index_010.outputs[0], vector_math_010.inputs[1])

    math = nodes.new("ShaderNodeMath")
    math.operation = "SIGN"
    math.use_clamp = False
    math.inputs[1].default_value = 0.5
    math.inputs[2].default_value = 0.5
    links.new(vector_math_010.outputs[1], math.inputs[0])

    vector_math_011 = nodes.new("ShaderNodeVectorMath")
    vector_math_011.operation = "SCALE"
    vector_math_011.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_011.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(vector_math_005.outputs[0], vector_math_011.inputs[0])
    links.new(math.outputs[0], vector_math_011.inputs[3])
    links.new(vector_math_011.outputs[0], vector_math_003.inputs[0])

    vector_math_012 = nodes.new("ShaderNodeVectorMath")
    vector_math_012.operation = "DOT_PRODUCT"
    vector_math_012.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_012.inputs[3].default_value = 1.0
    links.new(sample_index_009.outputs[0], vector_math_012.inputs[0])
    links.new(vector_math_009.outputs[0], vector_math_012.inputs[1])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.operation = "SIGN"
    math_002.use_clamp = False
    math_002.inputs[1].default_value = 0.5
    math_002.inputs[2].default_value = 0.5
    links.new(vector_math_012.outputs[1], math_002.inputs[0])

    vector_math_013 = nodes.new("ShaderNodeVectorMath")
    vector_math_013.operation = "SCALE"
    vector_math_013.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_013.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(math_002.outputs[0], vector_math_013.inputs[3])
    links.new(vector_math_009.outputs[0], vector_math_013.inputs[0])
    links.new(vector_math_013.outputs[0], vector_math_004.inputs[1])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_curve_rib_cage_group():
    group_name = "CurveRibCage"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
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
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    integer = nodes.new("FunctionNodeInputInt")
    integer.integer = 200

    integer_003 = nodes.new("FunctionNodeInputInt")
    integer_003.integer = 50

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.socket_idname = "NodeSocketInt"
    links.new(group_input.outputs[3], reroute_002.inputs[0])

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.socket_idname = "NodeSocketInt"
    links.new(group_input.outputs[4], reroute_003.inputs[0])

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.mode = "COUNT"
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    links.new(reroute_002.outputs[0], curve_to_points.inputs[1])
    links.new(group_input.outputs[1], curve_to_points.inputs[0])

    curve_to_points_001 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.mode = "COUNT"
    curve_to_points_001.inputs[2].default_value = 0.10000000149011612
    links.new(reroute_002.outputs[0], curve_to_points_001.inputs[1])
    links.new(group_input.outputs[0], curve_to_points_001.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.inputs[1].default_value = True
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))

    array = nodes.new("GeometryNodeGroup")
    array.node_tree = create_array_group()
    array.inputs[1].default_value = "Line"
    array.inputs[2].default_value = "Count"
    array.inputs[4].default_value = 1.0
    array.inputs[5].default_value = 0.7853981852531433
    array.inputs[6].default_value = True
    array.inputs[7].default_value = "Relative"
    array.inputs[8].default_value = "Inputs"
    array.inputs[9].default_value = Vector((1.0, 0.0, 0.0))
    array.inputs[10].default_value = Vector((0.0, 0.0, 0.0))
    array.inputs[11].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    array.inputs[12].default_value = Vector((1.0, 1.0, 1.0))
    array.inputs[13].default_value = "Z"
    array.inputs[14].default_value = "Full"
    array.inputs[15].default_value = 3.1415927410125732
    array.inputs[16].default_value = 0.0
    array.inputs[19].default_value = True
    array.inputs[20].default_value = True
    array.inputs[21].default_value = True
    array.inputs[22].default_value = "X"
    array.inputs[23].default_value = "Z"
    array.inputs[24].default_value = False
    array.inputs[25].default_value = Vector((0.0, 0.0, 0.0))
    array.inputs[26].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    array.inputs[27].default_value = "Uniform"
    array.inputs[28].default_value = Vector((0.0, 0.0, 0.0))
    array.inputs[29].default_value = 0.0
    array.inputs[30].default_value = [0.0, 0.0, 0.0]
    array.inputs[31].default_value = True
    array.inputs[32].default_value = False
    array.inputs[33].default_value = 0
    array.inputs[34].default_value = False
    array.inputs[35].default_value = 0.0010000000474974513
    links.new(array.outputs[0], set_position.inputs[0])
    links.new(reroute_002.outputs[0], array.inputs[3])

    index = nodes.new("GeometryNodeInputIndex")

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(set_position.outputs[0], set_position_001.inputs[0])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.data_type = "INT"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    links.new(array.outputs[0], sample_index_002.inputs[0])

    index_001 = nodes.new("GeometryNodeInputIndex")
    links.new(index_001.outputs[0], sample_index_002.inputs[2])
    links.new(index_001.outputs[0], sample_index_002.inputs[1])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    compare.inputs[0].default_value = 0.0
    compare.inputs[1].default_value = 0.0
    compare.inputs[3].default_value = 0
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[8].default_value = ""
    compare.inputs[9].default_value = ""
    compare.inputs[10].default_value = 0.8999999761581421
    compare.inputs[11].default_value = 0.08726649731397629
    compare.inputs[12].default_value = 0.0010000000474974513

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.operation = "MODULO"
    integer_math.inputs[1].default_value = 2
    integer_math.inputs[2].default_value = 0
    links.new(integer_math.outputs[0], compare.inputs[2])
    links.new(sample_index_002.outputs[0], integer_math.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "NOT"
    boolean_math.inputs[1].default_value = False
    links.new(compare.outputs[0], boolean_math.inputs[0])
    links.new(boolean_math.outputs[0], set_position_001.inputs[1])

    set_handle_positions = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions.mode = "LEFT"
    set_handle_positions.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(boolean_math.outputs[0], set_handle_positions.inputs[1])

    set_handle_positions_001 = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions_001.mode = "RIGHT"
    set_handle_positions_001.inputs[1].default_value = True
    set_handle_positions_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(set_handle_positions_001.outputs[0], set_handle_positions.inputs[0])
    links.new(set_position_001.outputs[0], set_handle_positions_001.inputs[0])

    sample_index_007 = nodes.new("GeometryNodeSampleIndex")
    sample_index_007.data_type = "FLOAT_VECTOR"
    sample_index_007.domain = "POINT"
    sample_index_007.clamp = False
    sample_index_007.inputs[1].default_value = [0.0, 0.0, 0.0]
    sample_index_007.inputs[2].default_value = 0

    sample_index_008 = nodes.new("GeometryNodeSampleIndex")
    sample_index_008.data_type = "FLOAT_VECTOR"
    sample_index_008.domain = "POINT"
    sample_index_008.clamp = False
    sample_index_008.inputs[1].default_value = [0.0, 0.0, 0.0]
    sample_index_008.inputs[2].default_value = 0

    reroute = nodes.new("NodeReroute")
    reroute.socket_idname = "NodeSocketGeometry"
    links.new(curve_to_points_001.outputs[0], reroute.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketVector"
    links.new(curve_to_points_001.outputs[1], reroute_001.inputs[0])

    reroute_004 = nodes.new("NodeReroute")
    reroute_004.socket_idname = "NodeSocketGeometry"
    links.new(curve_to_points.outputs[0], reroute_004.inputs[0])

    reroute_005 = nodes.new("NodeReroute")
    reroute_005.socket_idname = "NodeSocketVector"
    links.new(curve_to_points.outputs[1], reroute_005.inputs[0])

    debug_handles = nodes.new("GeometryNodeGroup")
    debug_handles.node_tree = create_debug_handles_group()
    debug_handles.inputs[1].default_value = 14
    debug_handles.inputs[2].default_value = [0.0, 0.0, 0.0]
    debug_handles.inputs[3].default_value = False
    links.new(set_handle_positions.outputs[0], debug_handles.inputs[0])

    set_handles = nodes.new("GeometryNodeGroup")
    set_handles.node_tree = create_set_handles_group()
    links.new(reroute.outputs[0], set_handles.inputs[3])
    links.new(reroute_005.outputs[0], set_handles.inputs[1])
    links.new(reroute_001.outputs[0], set_handles.inputs[4])
    links.new(reroute_004.outputs[0], set_handles.inputs[0])
    links.new(set_handles.outputs[0], set_handle_positions_001.inputs[2])
    links.new(set_handles.outputs[1], set_handle_positions.inputs[2])
    links.new(set_handles.outputs[2], set_position.inputs[2])
    links.new(set_handles.outputs[3], set_position_001.inputs[2])

    reroute_006 = nodes.new("NodeReroute")
    reroute_006.socket_idname = "NodeSocketVector"
    links.new(curve_to_points_001.outputs[2], reroute_006.inputs[0])
    links.new(reroute_006.outputs[0], set_handles.inputs[5])

    reroute_007 = nodes.new("NodeReroute")
    reroute_007.socket_idname = "NodeSocketVector"
    links.new(curve_to_points.outputs[2], reroute_007.inputs[0])
    links.new(reroute_007.outputs[0], set_handles.inputs[2])

    integer_math_001 = nodes.new("FunctionNodeIntegerMath")
    integer_math_001.operation = "DIVIDE"
    integer_math_001.inputs[1].default_value = 2
    integer_math_001.inputs[2].default_value = 0
    links.new(index.outputs[0], integer_math_001.inputs[0])

    bézier_segment = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment.mode = "POSITION"
    bézier_segment.inputs[0].default_value = 16
    bézier_segment.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    bézier_segment.inputs[2].default_value = Vector((-0.5, 0.5, 0.0))
    bézier_segment.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    bézier_segment.inputs[4].default_value = Vector((1.0, 0.0, 0.0))

    set_handle_type_002 = nodes.new("GeometryNodeCurveSetHandles")
    set_handle_type_002.handle_type = "ALIGN"
    set_handle_type_002.mode = ['LEFT', 'RIGHT']
    set_handle_type_002.inputs[1].default_value = True
    links.new(set_handle_type_002.outputs[0], array.inputs[0])
    links.new(bézier_segment.outputs[0], set_handle_type_002.inputs[0])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry.outputs[0], group_output.inputs[0])
    links.new(set_handle_positions.outputs[0], join_geometry.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_get_position_and_handles_group():
    group_name = "GetPositionAndHandles"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
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
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    index = nodes.new("GeometryNodeInputIndex")

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.data_type = "FLOAT_VECTOR"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    links.new(sample_index_003.outputs[0], group_output.inputs[1])

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.data_type = "FLOAT_VECTOR"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    links.new(sample_index_005.outputs[0], group_output.inputs[2])

    index_001 = nodes.new("GeometryNodeInputIndex")

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.component = "CURVE"
    links.new(group_input.outputs[0], domain_size.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.operation = "SUBTRACT"
    math.use_clamp = False
    math.inputs[1].default_value = 1.0
    math.inputs[2].default_value = 0.5
    links.new(domain_size.outputs[4], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.operation = "SUBTRACT"
    math_001.use_clamp = False
    math_001.inputs[2].default_value = 0.5
    links.new(math.outputs[0], math_001.inputs[0])

    evaluate_on_domain = nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.domain = "CURVE"
    evaluate_on_domain.data_type = "INT"
    links.new(index_001.outputs[0], evaluate_on_domain.inputs[0])
    links.new(evaluate_on_domain.outputs[0], math_001.inputs[1])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    math_002.inputs[1].default_value = 2.0
    math_002.inputs[2].default_value = 0.5
    links.new(math_001.outputs[0], math_002.inputs[0])

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.operation = "ADD"
    integer_math.inputs[2].default_value = 0
    links.new(math_002.outputs[0], integer_math.inputs[0])
    links.new(integer_math.outputs[0], sample_index_005.inputs[2])
    links.new(integer_math.outputs[0], sample_index_003.inputs[2])

    sample_index_004 = nodes.new("GeometryNodeSampleIndex")
    sample_index_004.data_type = "FLOAT_VECTOR"
    sample_index_004.domain = "POINT"
    sample_index_004.clamp = False
    links.new(integer_math.outputs[0], sample_index_004.inputs[2])
    links.new(sample_index_004.outputs[0], group_output.inputs[0])

    integer_math_004 = nodes.new("FunctionNodeIntegerMath")
    integer_math_004.operation = "MODULO"
    integer_math_004.inputs[1].default_value = 2
    integer_math_004.inputs[2].default_value = 0
    links.new(index_001.outputs[0], integer_math_004.inputs[0])
    links.new(integer_math_004.outputs[0], integer_math.inputs[1])

    sample_index_008 = nodes.new("GeometryNodeSampleIndex")
    sample_index_008.data_type = "FLOAT_VECTOR"
    sample_index_008.domain = "POINT"
    sample_index_008.clamp = False
    links.new(index.outputs[0], sample_index_008.inputs[2])
    links.new(sample_index_008.outputs[0], group_output.inputs[5])

    sample_index_009 = nodes.new("GeometryNodeSampleIndex")
    sample_index_009.data_type = "FLOAT_VECTOR"
    sample_index_009.domain = "POINT"
    sample_index_009.clamp = False
    links.new(index.outputs[0], sample_index_009.inputs[2])
    links.new(sample_index_009.outputs[0], group_output.inputs[4])

    sample_index_010 = nodes.new("GeometryNodeSampleIndex")
    sample_index_010.data_type = "FLOAT_VECTOR"
    sample_index_010.domain = "POINT"
    sample_index_010.clamp = False
    links.new(index.outputs[0], sample_index_010.inputs[2])
    links.new(sample_index_010.outputs[0], group_output.inputs[3])

    reroute = nodes.new("NodeReroute")
    reroute.socket_idname = "NodeSocketGeometry"
    links.new(reroute.outputs[0], sample_index_010.inputs[0])
    links.new(reroute.outputs[0], sample_index_005.inputs[0])
    links.new(reroute.outputs[0], sample_index_009.inputs[0])
    links.new(reroute.outputs[0], sample_index_004.inputs[0])
    links.new(reroute.outputs[0], sample_index_003.inputs[0])
    links.new(reroute.outputs[0], sample_index_008.inputs[0])
    links.new(group_input.outputs[0], reroute.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    links.new(position_002.outputs[0], sample_index_008.inputs[1])
    links.new(position_002.outputs[0], sample_index_003.inputs[1])

    curve_handle_positions_001 = nodes.new("GeometryNodeInputCurveHandlePositions")
    curve_handle_positions_001.inputs[0].default_value = False
    links.new(curve_handle_positions_001.outputs[0], sample_index_004.inputs[1])
    links.new(curve_handle_positions_001.outputs[1], sample_index_009.inputs[1])
    links.new(curve_handle_positions_001.outputs[0], sample_index_010.inputs[1])
    links.new(curve_handle_positions_001.outputs[1], sample_index_005.inputs[1])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_align_handles_group():
    group_name = "AlignHandles"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    separate_components_001 = nodes.new("GeometryNodeSeparateComponents")
    links.new(group_input.outputs[0], separate_components_001.inputs[0])

    separate_components_002 = nodes.new("GeometryNodeSeparateComponents")
    links.new(group_input.outputs[1], separate_components_002.inputs[0])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry.outputs[0], group_output.inputs[0])
    links.new(separate_components_001.outputs[0], join_geometry.inputs[0])

    set_handle_positions = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions.mode = "LEFT"
    set_handle_positions.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(separate_components_001.outputs[1], set_handle_positions.inputs[0])
    links.new(set_handle_positions.outputs[0], join_geometry.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "EQUAL"
    compare.data_type = "VECTOR"
    compare.mode = "ELEMENT"
    compare.inputs[0].default_value = 0.0
    compare.inputs[1].default_value = 0.0
    compare.inputs[2].default_value = 0
    compare.inputs[3].default_value = 0
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[8].default_value = ""
    compare.inputs[9].default_value = ""
    compare.inputs[10].default_value = 0.8999999761581421
    compare.inputs[11].default_value = 0.08726649731397629
    compare.inputs[12].default_value = 0.0010000000474974513
    links.new(compare.outputs[0], set_handle_positions.inputs[1])

    debug_handles = nodes.new("GeometryNodeGroup")
    debug_handles.node_tree = create_debug_handles_group()
    debug_handles.inputs[1].default_value = 2
    debug_handles.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(set_handle_positions.outputs[0], debug_handles.inputs[0])

    mix = nodes.new("ShaderNodeMix")
    mix.data_type = "VECTOR"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[0].default_value = 0.5
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    mix.inputs[2].default_value = 0.0
    mix.inputs[3].default_value = 0.0
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    links.new(mix.outputs[1], set_handle_positions.inputs[2])

    position_001 = nodes.new("GeometryNodeInputPosition")

    sample_index_006 = nodes.new("GeometryNodeSampleIndex")
    sample_index_006.data_type = "FLOAT_VECTOR"
    sample_index_006.domain = "POINT"
    sample_index_006.clamp = False
    sample_index_006.inputs[2].default_value = 0
    links.new(position_001.outputs[0], sample_index_006.inputs[1])
    links.new(separate_components_001.outputs[1], sample_index_006.inputs[0])

    sample_index_007 = nodes.new("GeometryNodeSampleIndex")
    sample_index_007.data_type = "FLOAT_VECTOR"
    sample_index_007.domain = "POINT"
    sample_index_007.clamp = False
    sample_index_007.inputs[2].default_value = 0
    links.new(position_001.outputs[0], sample_index_007.inputs[1])
    links.new(separate_components_002.outputs[1], sample_index_007.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.operation = "EQUAL"
    compare_001.data_type = "VECTOR"
    compare_001.mode = "ELEMENT"
    compare_001.inputs[0].default_value = 0.0
    compare_001.inputs[1].default_value = 0.0
    compare_001.inputs[2].default_value = 0
    compare_001.inputs[3].default_value = 0
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[8].default_value = ""
    compare_001.inputs[9].default_value = ""
    compare_001.inputs[10].default_value = 0.8999999761581421
    compare_001.inputs[11].default_value = 0.08726649731397629
    compare_001.inputs[12].default_value = 0.0010000000474974513
    links.new(sample_index_006.outputs[0], compare_001.inputs[4])
    links.new(sample_index_007.outputs[0], compare_001.inputs[5])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "NOT"
    boolean_math.inputs[1].default_value = False
    links.new(compare_001.outputs[0], boolean_math.inputs[0])
    links.new(boolean_math.outputs[0], debug_handles.inputs[3])

    set_handle_positions_001 = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions_001.mode = "LEFT"
    set_handle_positions_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(separate_components_002.outputs[1], set_handle_positions_001.inputs[0])
    links.new(compare.outputs[0], set_handle_positions_001.inputs[1])

    debug_handles_1 = nodes.new("GeometryNodeGroup")
    debug_handles_1.node_tree = create_debug_handles_group()
    debug_handles_1.inputs[1].default_value = 2
    debug_handles_1.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(set_handle_positions_001.outputs[0], debug_handles_1.inputs[0])
    links.new(boolean_math.outputs[0], debug_handles_1.inputs[3])

    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.data_type = "VECTOR"
    mix_001.factor_mode = "UNIFORM"
    mix_001.blend_type = "MIX"
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.inputs[0].default_value = 0.5
    mix_001.inputs[1].default_value = [0.5, 0.5, 0.5]
    mix_001.inputs[2].default_value = 0.0
    mix_001.inputs[3].default_value = 0.0
    mix_001.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    mix_001.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    mix_001.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    mix_001.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    links.new(mix_001.outputs[1], set_handle_positions_001.inputs[2])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_001.outputs[0], group_output.inputs[1])
    links.new(set_handle_positions_001.outputs[0], join_geometry_001.inputs[0])
    links.new(separate_components_002.outputs[0], join_geometry_001.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "VECTOR"
    links.new(switch.outputs[0], mix_001.inputs[4])
    links.new(compare_001.outputs[0], switch.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketGeometry"
    links.new(separate_components_001.outputs[1], reroute_001.inputs[0])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "VECTOR"
    links.new(compare_001.outputs[0], switch_001.inputs[0])
    links.new(switch_001.outputs[0], mix.inputs[5])

    get_position_and_handles = nodes.new("GeometryNodeGroup")
    get_position_and_handles.node_tree = create_get_position_and_handles_group()
    links.new(get_position_and_handles.outputs[3], mix_001.inputs[5])
    links.new(get_position_and_handles.outputs[2], switch_001.inputs[1])
    links.new(separate_components_002.outputs[1], get_position_and_handles.inputs[0])
    links.new(get_position_and_handles.outputs[4], switch_001.inputs[2])

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.input_type = "VECTOR"
    links.new(get_position_and_handles.outputs[1], switch_002.inputs[1])
    links.new(get_position_and_handles.outputs[5], switch_002.inputs[2])
    links.new(compare_001.outputs[0], switch_002.inputs[0])
    links.new(switch_002.outputs[0], compare.inputs[4])

    get_position_and_handles_1 = nodes.new("GeometryNodeGroup")
    get_position_and_handles_1.node_tree = create_get_position_and_handles_group()
    links.new(reroute_001.outputs[0], get_position_and_handles_1.inputs[0])
    links.new(get_position_and_handles_1.outputs[3], mix.inputs[4])
    links.new(get_position_and_handles_1.outputs[4], switch.inputs[2])
    links.new(get_position_and_handles_1.outputs[2], switch.inputs[1])
    links.new(get_position_and_handles_1.outputs[5], compare.inputs[5])

    switch_003 = nodes.new("GeometryNodeSwitch")
    switch_003.input_type = "VECTOR"
    links.new(get_position_and_handles_1.outputs[1], switch_003.inputs[1])
    links.new(get_position_and_handles_1.outputs[5], switch_003.inputs[2])
    links.new(compare_001.outputs[0], switch_003.inputs[0])

    auto_layout_nodes(group)
    return group

@geo_node_group
def create_loft_spheriod_group():
    group_name = "LoftSpheriod"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
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
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.domain = "CURVE"

    math_005 = nodes.new("ShaderNodeMath")
    math_005.operation = "GREATER_THAN"
    math_005.use_clamp = False
    math_005.inputs[1].default_value = 5.960464477539063e-08
    math_005.inputs[2].default_value = 0.5
    links.new(math_005.outputs[0], separate_geometry.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    links.new(index.outputs[0], math_005.inputs[0])

    viewer = nodes.new("GeometryNodeViewer")
    viewer.ui_shortcut = 0
    viewer.active_index = 0
    viewer.domain = "AUTO"

    set_axis = nodes.new("GeometryNodeGroup")
    set_axis.node_tree = create_set_axis_group()
    set_axis.inputs[2].default_value = "axis+"
    links.new(group_input.outputs[0], set_axis.inputs[0])

    set_axis_1 = nodes.new("GeometryNodeGroup")
    set_axis_1.node_tree = create_set_axis_group()
    set_axis_1.inputs[2].default_value = "axis-"
    links.new(set_axis.outputs[0], set_axis_1.inputs[0])
    links.new(set_axis_1.outputs[0], viewer.inputs[0])
    links.new(set_axis_1.outputs[0], separate_geometry.inputs[0])

    viewer_001 = nodes.new("GeometryNodeViewer")
    viewer_001.ui_shortcut = 0
    viewer_001.active_index = 0
    viewer_001.domain = "AUTO"
    links.new(separate_geometry.outputs[1], viewer_001.inputs[0])

    split_curves_about_axis = nodes.new("GeometryNodeGroup")
    split_curves_about_axis.node_tree = create_split_curves_about_axis_group()
    links.new(separate_geometry.outputs[0], split_curves_about_axis.inputs[0])

    split_curves_about_axis_1 = nodes.new("GeometryNodeGroup")
    split_curves_about_axis_1.node_tree = create_split_curves_about_axis_group()
    links.new(separate_geometry.outputs[1], split_curves_about_axis_1.inputs[0])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    links.new(split_curves_about_axis.outputs[0], join_geometry.inputs[0])
    links.new(split_curves_about_axis_1.outputs[1], join_geometry.inputs[0])
    links.new(split_curves_about_axis.outputs[1], join_geometry.inputs[0])
    links.new(split_curves_about_axis_1.outputs[0], join_geometry.inputs[0])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    sample_index.inputs[2].default_value = 0
    links.new(set_axis_1.outputs[0], sample_index.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")
    links.new(position.outputs[0], sample_index.inputs[1])

    get_axis = nodes.new("GeometryNodeGroup")
    get_axis.node_tree = create_get_axis_group()
    links.new(separate_geometry.outputs[1], get_axis.inputs[1])
    links.new(separate_geometry.outputs[0], get_axis.inputs[0])

    orient_curve = nodes.new("GeometryNodeGroup")
    orient_curve.node_tree = create_orient_curve_group()
    links.new(split_curves_about_axis.outputs[0], orient_curve.inputs[0])
    links.new(split_curves_about_axis_1.outputs[1], orient_curve.inputs[1])

    orient_curve_1 = nodes.new("GeometryNodeGroup")
    orient_curve_1.node_tree = create_orient_curve_group()
    links.new(split_curves_about_axis_1.outputs[0], orient_curve_1.inputs[1])
    links.new(split_curves_about_axis.outputs[1], orient_curve_1.inputs[0])

    orient_curve_2 = nodes.new("GeometryNodeGroup")
    orient_curve_2.node_tree = create_orient_curve_group()
    links.new(split_curves_about_axis.outputs[1], orient_curve_2.inputs[0])
    links.new(split_curves_about_axis_1.outputs[1], orient_curve_2.inputs[1])

    orient_curve_3 = nodes.new("GeometryNodeGroup")
    orient_curve_3.node_tree = create_orient_curve_group()
    links.new(split_curves_about_axis.outputs[0], orient_curve_3.inputs[0])
    links.new(split_curves_about_axis_1.outputs[0], orient_curve_3.inputs[1])

    integer_math_003 = nodes.new("FunctionNodeIntegerMath")
    integer_math_003.operation = "DIVIDE_CEIL"
    integer_math_003.inputs[1].default_value = 4
    integer_math_003.inputs[2].default_value = 0
    links.new(group_input.outputs[1], integer_math_003.inputs[0])

    viewer_004 = nodes.new("GeometryNodeViewer")
    viewer_004.ui_shortcut = 0
    viewer_004.active_index = 0
    viewer_004.domain = "AUTO"
    links.new(split_curves_about_axis.outputs[0], viewer_004.inputs[0])

    loft_curve_parts = nodes.new("GeometryNodeGroup")
    loft_curve_parts.node_tree = create_loft_curve_parts_group()
    links.new(group_input.outputs[1], loft_curve_parts.inputs[1])

    loft_curve_parts_1 = nodes.new("GeometryNodeGroup")
    loft_curve_parts_1.node_tree = create_loft_curve_parts_group()
    loft_curve_parts_1.inputs[1].default_value = 3

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "GEOMETRY"
    switch.inputs[0].default_value = True

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "GEOMETRY"
    switch_001.inputs[0].default_value = True

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.input_type = "GEOMETRY"
    switch_002.inputs[0].default_value = True

    switch_003 = nodes.new("GeometryNodeSwitch")
    switch_003.input_type = "GEOMETRY"
    switch_003.inputs[0].default_value = True

    curve_rib_cage = nodes.new("GeometryNodeGroup")
    curve_rib_cage.node_tree = create_curve_rib_cage_group()
    links.new(orient_curve.outputs[0], curve_rib_cage.inputs[0])
    links.new(integer_math_003.outputs[0], curve_rib_cage.inputs[4])
    links.new(curve_rib_cage.outputs[0], switch_003.inputs[2])
    links.new(get_axis.outputs[4], curve_rib_cage.inputs[5])
    links.new(orient_curve.outputs[1], curve_rib_cage.inputs[1])
    links.new(group_input.outputs[2], curve_rib_cage.inputs[2])
    links.new(group_input.outputs[3], curve_rib_cage.inputs[3])

    curve_rib_cage_1 = nodes.new("GeometryNodeGroup")
    curve_rib_cage_1.node_tree = create_curve_rib_cage_group()
    links.new(curve_rib_cage_1.outputs[0], switch.inputs[2])
    links.new(orient_curve_1.outputs[0], curve_rib_cage_1.inputs[0])
    links.new(orient_curve_1.outputs[1], curve_rib_cage_1.inputs[1])
    links.new(get_axis.outputs[4], curve_rib_cage_1.inputs[5])
    links.new(integer_math_003.outputs[0], curve_rib_cage_1.inputs[4])
    links.new(group_input.outputs[3], curve_rib_cage_1.inputs[2])
    links.new(group_input.outputs[3], curve_rib_cage_1.inputs[3])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")

    curve_rib_cage_2 = nodes.new("GeometryNodeGroup")
    curve_rib_cage_2.node_tree = create_curve_rib_cage_group()
    curve_rib_cage_2.inputs[2].default_value = 200
    links.new(curve_rib_cage_2.outputs[0], switch_001.inputs[2])
    links.new(orient_curve_2.outputs[0], curve_rib_cage_2.inputs[0])
    links.new(get_axis.outputs[4], curve_rib_cage_2.inputs[5])
    links.new(orient_curve_2.outputs[1], curve_rib_cage_2.inputs[1])
    links.new(group_input.outputs[2], curve_rib_cage_2.inputs[4])
    links.new(group_input.outputs[3], curve_rib_cage_2.inputs[3])

    curve_rib_cage_3 = nodes.new("GeometryNodeGroup")
    curve_rib_cage_3.node_tree = create_curve_rib_cage_group()
    links.new(integer_math_003.outputs[0], curve_rib_cage_3.inputs[2])
    links.new(curve_rib_cage_3.outputs[0], switch_002.inputs[2])
    links.new(orient_curve_3.outputs[0], curve_rib_cage_3.inputs[0])
    links.new(orient_curve_3.outputs[1], curve_rib_cage_3.inputs[1])
    links.new(get_axis.outputs[4], curve_rib_cage_3.inputs[5])
    links.new(group_input.outputs[2], curve_rib_cage_3.inputs[4])
    links.new(group_input.outputs[3], curve_rib_cage_3.inputs[3])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    links.new(loft_curve_parts.outputs[0], join_geometry_002.inputs[0])
    links.new(group_input.outputs[0], join_geometry_002.inputs[0])
    links.new(join_geometry_002.outputs[0], group_output.inputs[0])

    separate_components = nodes.new("GeometryNodeSeparateComponents")
    links.new(join_geometry_001.outputs[0], separate_components.inputs[0])
    links.new(separate_components.outputs[1], loft_curve_parts.inputs[0])
    links.new(separate_components.outputs[0], join_geometry_002.inputs[0])

    align_handles = nodes.new("GeometryNodeGroup")
    align_handles.node_tree = create_align_handles_group()
    links.new(align_handles.outputs[0], join_geometry_001.inputs[0])
    links.new(switch.outputs[0], align_handles.inputs[1])

    align_handles_1 = nodes.new("GeometryNodeGroup")
    align_handles_1.node_tree = create_align_handles_group()
    links.new(align_handles_1.outputs[1], join_geometry_001.inputs[0])
    links.new(align_handles.outputs[1], align_handles_1.inputs[1])
    links.new(align_handles_1.outputs[0], join_geometry_001.inputs[0])

    align_handles_2 = nodes.new("GeometryNodeGroup")
    align_handles_2.node_tree = create_align_handles_group()
    links.new(align_handles_2.outputs[1], align_handles.inputs[0])
    links.new(switch_003.outputs[0], align_handles_2.inputs[0])
    links.new(switch_002.outputs[0], align_handles_2.inputs[1])

    align_handles_3 = nodes.new("GeometryNodeGroup")
    align_handles_3.node_tree = create_align_handles_group()
    links.new(align_handles_2.outputs[0], align_handles_3.inputs[0])
    links.new(align_handles_3.outputs[1], align_handles_1.inputs[0])
    links.new(align_handles_3.outputs[0], join_geometry_001.inputs[0])
    links.new(switch_001.outputs[0], align_handles_3.inputs[1])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.inputs[2].default_value = 1.0
    curve_to_mesh.inputs[3].default_value = False
    links.new(separate_components.outputs[1], curve_to_mesh.inputs[0])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    links.new(switch.outputs[0], join_geometry_003.inputs[0])
    links.new(switch_003.outputs[0], join_geometry_003.inputs[0])
    links.new(switch_001.outputs[0], join_geometry_003.inputs[0])
    links.new(switch_002.outputs[0], join_geometry_003.inputs[0])

    auto_layout_nodes(group)
    return group

