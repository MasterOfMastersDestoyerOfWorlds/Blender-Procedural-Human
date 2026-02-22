import bpy
from mathutils import Vector, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.utilities.gem_in_holder import create_gem_in__holder_group
from procedural_human.geo_node_groups.utilities.gold_decorations import create_gold__decorations_group
from procedural_human.geo_node_groups.utilities.gold_on_band import create_gold_on__band_group
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group
from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group
from procedural_human.geo_node_groups.utilities.rivet import create_rivet_group
from procedural_human.geo_node_groups.utilities.rotate_on_center import create_rotate_on__centre_group
from procedural_human.geo_node_groups.utilities.swap_attr import create_swap__attr_group
from procedural_human.geo_node_groups.node_helpers import (
    compare_op,
    get_or_rebuild_node_group,
    separate_xyz,
)

@geo_node_group
def create_shoulders_group():
    group_name = "Shoulders"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    bézier_segment_004 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_004.mode = "OFFSET"
    bézier_segment_004.inputs[0].default_value = 16
    bézier_segment_004.inputs[1].default_value = Vector((-0.23098699748516083, 0.009999999776482582, 0.39754199981689453))
    bézier_segment_004.inputs[2].default_value = Vector((0.0, -0.10000000149011612, 0.0))
    bézier_segment_004.inputs[3].default_value = Vector((-0.05999999865889549, 0.029999999329447746, 0.019999999552965164))
    bézier_segment_004.inputs[4].default_value = Vector((-0.10215499997138977, -0.13706600666046143, 0.31426501274108887))

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.inputs[3].default_value = False

    arc = nodes.new("GeometryNodeCurveArc")
    arc.mode = "RADIUS"
    arc.inputs[0].default_value = 24
    arc.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    arc.inputs[2].default_value = Vector((0.0, 2.0, 0.0))
    arc.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    arc.inputs[5].default_value = 1.3089969158172607
    arc.inputs[6].default_value = 0.5235987901687622
    arc.inputs[7].default_value = 0.0
    arc.inputs[8].default_value = False
    arc.inputs[9].default_value = False

    transform_geometry_012 = nodes.new("GeometryNodeTransform")
    transform_geometry_012.inputs[1].default_value = "Components"
    transform_geometry_012.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_012.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(arc.outputs[0], transform_geometry_012.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.inputs[1].default_value = True
    set_curve_tilt.inputs[2].default_value = -2.0682151317596436
    links.new(bézier_segment_004.outputs[0], set_curve_tilt.inputs[0])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")

    float_curve_003 = nodes.new("ShaderNodeFloatCurve")
    float_curve_003.inputs[0].default_value = 1.0
    links.new(spline_parameter.outputs[0], float_curve_003.inputs[1])

    value_001 = nodes.new("ShaderNodeValue")
    links.new(value_001.outputs[0], arc.inputs[4])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.operation = "SCALE"
    vector_math_003.inputs[0].default_value = [0.0, -0.9799999594688416, 0.0]
    vector_math_003.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(value_001.outputs[0], vector_math_003.inputs[3])
    links.new(vector_math_003.outputs[0], transform_geometry_012.inputs[2])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Count"
    resample_curve.inputs[3].default_value = 16
    resample_curve.inputs[4].default_value = 0.10000000149011612
    links.new(set_curve_tilt.outputs[0], resample_curve.inputs[0])

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.active_index = 1
    capture_attribute.domain = "POINT"
    links.new(capture_attribute.outputs[0], curve_to_mesh.inputs[1])
    links.new(transform_geometry_012.outputs[0], capture_attribute.inputs[0])
    links.new(spline_parameter.outputs[0], capture_attribute.inputs[1])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.active_index = 2
    capture_attribute_001.domain = "POINT"
    links.new(capture_attribute_001.outputs[0], curve_to_mesh.inputs[0])

    endpoint_selection = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection.inputs[0].default_value = 0
    endpoint_selection.inputs[1].default_value = 1
    links.new(endpoint_selection.outputs[0], capture_attribute_001.inputs[1])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.inputs[3].default_value = False
    instance_on_points.inputs[4].default_value = 0
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    links.new(endpoint_selection.outputs[0], instance_on_points.inputs[1])

    arc_001 = nodes.new("GeometryNodeCurveArc")
    arc_001.mode = "RADIUS"
    arc_001.inputs[0].default_value = 32
    arc_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    arc_001.inputs[2].default_value = Vector((0.0, 2.0, 0.0))
    arc_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    arc_001.inputs[4].default_value = 0.04000002145767212
    arc_001.inputs[5].default_value = 0.0
    arc_001.inputs[6].default_value = 3.1415927410125732
    arc_001.inputs[7].default_value = 0.0
    arc_001.inputs[8].default_value = False
    arc_001.inputs[9].default_value = False

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector.inputs[1].default_value = 1.0

    set_curve_radius = nodes.new("GeometryNodeSetCurveRadius")
    set_curve_radius.inputs[1].default_value = True
    links.new(set_curve_radius.outputs[0], capture_attribute_001.inputs[0])
    links.new(set_curve_radius.outputs[0], instance_on_points.inputs[0])
    links.new(float_curve_003.outputs[0], set_curve_radius.inputs[2])

    radius = nodes.new("GeometryNodeInputRadius")
    links.new(radius.outputs[0], curve_to_mesh.inputs[2])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.axis = "Y"
    align_rotation_to_vector_001.pivot_axis = "X"
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    links.new(align_rotation_to_vector.outputs[0], align_rotation_to_vector_001.inputs[0])

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.legacy_corner_normals = False
    links.new(normal_001.outputs[0], align_rotation_to_vector.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.rotation_space = "LOCAL"
    rotate_rotation.inputs[1].default_value = Euler((-0.12514010071754456, 0.0, 0.0), 'XYZ')
    links.new(rotate_rotation.outputs[0], instance_on_points.inputs[5])
    links.new(align_rotation_to_vector_001.outputs[0], rotate_rotation.inputs[0])

    transform_geometry_013 = nodes.new("GeometryNodeTransform")
    transform_geometry_013.inputs[1].default_value = "Components"
    transform_geometry_013.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    transform_geometry_013.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_013.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_013.outputs[0], instance_on_points.inputs[2])
    links.new(arc_001.outputs[0], transform_geometry_013.inputs[0])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(capture_attribute_001.outputs[1], set_position_003.inputs[1])

    frame_013 = nodes.new("NodeFrame")
    frame_013.text = None
    frame_013.shrink = True
    frame_013.label_size = 20

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.inputs[1].default_value = True
    realize_instances.inputs[2].default_value = True
    realize_instances.inputs[3].default_value = 0
    links.new(instance_on_points.outputs[0], realize_instances.inputs[0])

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = True
    sample_curve.data_type = "FLOAT"
    sample_curve.inputs[1].default_value = 0.0
    sample_curve.inputs[3].default_value = 0.0
    sample_curve.inputs[4].default_value = 0
    links.new(realize_instances.outputs[0], sample_curve.inputs[0])
    links.new(sample_curve.outputs[1], set_position_003.inputs[2])
    links.new(capture_attribute.outputs[1], sample_curve.inputs[2])

    transform_geometry_015 = nodes.new("GeometryNodeTransform")
    transform_geometry_015.inputs[1].default_value = "Components"
    transform_geometry_015.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_015.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_015.inputs[4].default_value = Vector((1.0, -1.0, 1.0))

    flip_faces_006 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_006.inputs[1].default_value = True
    links.new(transform_geometry_015.outputs[0], flip_faces_006.inputs[0])

    join_geometry_012 = nodes.new("GeometryNodeJoinGeometry")
    links.new(flip_faces_006.outputs[0], join_geometry_012.inputs[0])

    endpoint_selection_001 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_001.inputs[0].default_value = 1
    endpoint_selection_001.inputs[1].default_value = 0
    links.new(endpoint_selection_001.outputs[0], capture_attribute_001.inputs[1])

    curve_tangent_001 = nodes.new("GeometryNodeInputTangent")
    links.new(curve_tangent_001.outputs[0], align_rotation_to_vector_001.inputs[2])

    set_position_004 = nodes.new("GeometryNodeSetPosition")
    set_position_004.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(set_position_004.outputs[0], transform_geometry_015.inputs[0])
    links.new(set_position_004.outputs[0], join_geometry_012.inputs[0])
    links.new(set_position_003.outputs[0], set_position_004.inputs[0])

    position_004 = nodes.new("GeometryNodeInputPosition")

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.operation = "MULTIPLY"
    vector_math_004.inputs[1].default_value = [1.0, 0.0, 1.0]
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_004.inputs[3].default_value = 1.0
    links.new(position_004.outputs[0], vector_math_004.inputs[0])
    links.new(vector_math_004.outputs[0], set_position_004.inputs[2])

    merge_by_distance_001 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_001.inputs[2].default_value = "All"
    merge_by_distance_001.inputs[3].default_value = 0.0010000000474974513
    links.new(join_geometry_012.outputs[0], merge_by_distance_001.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.socket_idname = "NodeSocketBool"
    links.new(reroute.outputs[0], set_position_004.inputs[1])
    links.new(capture_attribute_001.outputs[1], reroute.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketBool"
    links.new(reroute_001.outputs[0], merge_by_distance_001.inputs[1])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.socket_idname = "NodeSocketBool"
    links.new(reroute_002.outputs[0], reroute_001.inputs[0])
    links.new(reroute.outputs[0], reroute_002.inputs[0])

    mesh_to_curve_002 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.mode = "EDGES"

    frame_014 = nodes.new("NodeFrame")
    frame_014.text = None
    frame_014.shrink = True
    frame_014.label_size = 20

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    links.new(is_edge_boundary.outputs[0], mesh_to_curve_002.inputs[1])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.inputs[2].default_value = 1.0
    curve_to_mesh_001.inputs[3].default_value = False

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.mode = "POINTS"
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    curve_line.inputs[1].default_value = Vector((0.019999999552965164, 0.0, 0.0))
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    curve_line.inputs[3].default_value = 1.0

    set_curve_tilt_001 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_001.inputs[1].default_value = True
    set_curve_tilt_001.inputs[2].default_value = -7.752577304840088

    flip_faces_005 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_005.inputs[1].default_value = True
    links.new(curve_to_mesh_001.outputs[0], flip_faces_005.inputs[0])

    frame_015 = nodes.new("NodeFrame")
    frame_015.text = None
    frame_015.shrink = True
    frame_015.label_size = 20

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "POINT"
    links.new(capture_attribute_002.outputs[0], curve_to_mesh_001.inputs[1])
    links.new(curve_line.outputs[0], capture_attribute_002.inputs[0])

    endpoint_selection_002 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_002.inputs[0].default_value = 0
    endpoint_selection_002.inputs[1].default_value = 1
    links.new(endpoint_selection_002.outputs[0], capture_attribute_002.inputs[1])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "AND"

    capture_attribute_003 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.active_index = 1
    capture_attribute_003.domain = "POINT"
    links.new(capture_attribute_003.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(set_curve_tilt_001.outputs[0], capture_attribute_003.inputs[0])

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_001.outputs[0], capture_attribute_003.inputs[1])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.operation = "EQUAL"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    compare_001.inputs[1].default_value = 0.5
    compare_001.inputs[2].default_value = 0
    compare_001.inputs[3].default_value = 0
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[8].default_value = ""
    compare_001.inputs[9].default_value = ""
    compare_001.inputs[10].default_value = 0.8999999761581421
    compare_001.inputs[11].default_value = 0.08726649731397629
    compare_001.inputs[12].default_value = 0.1210000067949295

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.mode = "EDGES"
    extrude_mesh.inputs[3].default_value = 0.07000000029802322
    repeat_input = nodes.new("GeometryNodeRepeatInput") 
    repeat_input.inputs[3].default_value = 0.0
    extrude_mesh.inputs[4].default_value = True

    links.new(boolean_math.outputs[0], repeat_input.inputs[2])
    links.new(repeat_input.outputs[2], extrude_mesh.inputs[1])
    links.new(flip_faces_005.outputs[0], repeat_input.inputs[1])
    links.new(repeat_input.outputs[1], extrude_mesh.inputs[0])

    repeat_output = nodes.new("GeometryNodeRepeatOutput")
    repeat_output.active_index = 2
    repeat_output.inspection_index = 0
    links.new(extrude_mesh.outputs[0], repeat_output.inputs[0])
    links.new(extrude_mesh.outputs[1], repeat_output.inputs[1])

    vector_002 = nodes.new("FunctionNodeInputVector")
    vector_002.vector = Vector((-0.03999999910593033, 0.0, -0.14999999105930328))

    set_curve_tilt_002 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_002.inputs[1].default_value = True
    links.new(set_curve_tilt_002.outputs[0], set_curve_radius.inputs[0])
    links.new(resample_curve.outputs[0], set_curve_tilt_002.inputs[0])

    curve_tilt = nodes.new("GeometryNodeInputCurveTilt")

    math_003 = nodes.new("ShaderNodeMath")
    math_003.operation = "SUBTRACT"
    math_003.inputs[2].default_value = 0.5
    links.new(curve_tilt.outputs[0], math_003.inputs[0])
    links.new(math_003.outputs[0], set_curve_tilt_002.inputs[2])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")

    float_curve_004 = nodes.new("ShaderNodeFloatCurve")
    float_curve_004.inputs[0].default_value = 1.0
    links.new(spline_parameter_002.outputs[0], float_curve_004.inputs[1])
    links.new(float_curve_004.outputs[0], math_003.inputs[1])

    capture_attribute_004 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_004.active_index = 0
    capture_attribute_004.domain = "POINT"
    links.new(merge_by_distance_001.outputs[0], capture_attribute_004.inputs[0])
    links.new(capture_attribute_004.outputs[0], mesh_to_curve_002.inputs[0])

    normal_002 = nodes.new("GeometryNodeInputNormal")
    normal_002.legacy_corner_normals = False

    set_curve_normal = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal.inputs[1].default_value = True
    set_curve_normal.inputs[2].default_value = "Free"
    links.new(mesh_to_curve_002.outputs[0], set_curve_normal.inputs[0])
    links.new(capture_attribute_004.outputs[1], set_curve_normal.inputs[3])
    links.new(set_curve_normal.outputs[0], set_curve_tilt_001.inputs[0])

    blur_attribute = nodes.new("GeometryNodeBlurAttribute")
    blur_attribute.data_type = "FLOAT_VECTOR"
    blur_attribute.inputs[1].default_value = 5
    blur_attribute.inputs[2].default_value = 1.0
    links.new(blur_attribute.outputs[0], capture_attribute_004.inputs[1])
    links.new(normal_002.outputs[0], blur_attribute.inputs[0])

    endpoint_selection_003 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_003.inputs[0].default_value = 1
    endpoint_selection_003.inputs[1].default_value = 1
    links.new(endpoint_selection_003.outputs[0], capture_attribute_003.inputs[1])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.operation = "NIMPLY"
    links.new(compare_001.outputs[0], boolean_math_001.inputs[0])
    links.new(boolean_math_001.outputs[0], boolean_math.inputs[1])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.operation = "SUBTRACT"
    math_004.inputs[1].default_value = 0.5
    math_004.inputs[2].default_value = 0.5

    integer_001 = nodes.new("FunctionNodeInputInt")
    integer_001.integer = 9
    links.new(integer_001.outputs[0], repeat_input.inputs[0])

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.operation = "SUBTRACT"
    integer_math.inputs[1].default_value = 1
    integer_math.inputs[2].default_value = 0
    links.new(integer_001.outputs[0], integer_math.inputs[0])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.operation = "DIVIDE"
    math_006.inputs[2].default_value = 0.5
    links.new(repeat_input.outputs[0], math_006.inputs[0])
    links.new(integer_math.outputs[0], math_006.inputs[1])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.operation = "SIGN"
    math_007.inputs[1].default_value = 11.59999942779541
    math_007.inputs[2].default_value = 0.5
    links.new(math_004.outputs[0], math_007.inputs[0])

    math_008 = nodes.new("ShaderNodeMath")
    math_008.operation = "MULTIPLY"
    math_008.inputs[2].default_value = 0.5
    links.new(math_007.outputs[0], math_008.inputs[1])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.operation = "MULTIPLY_ADD"
    vector_math_005.inputs[0].default_value = [0.0, 0.09000000357627869, 0.0]
    vector_math_005.inputs[3].default_value = 1.0
    links.new(math_008.outputs[0], vector_math_005.inputs[1])
    links.new(vector_math_005.outputs[0], extrude_mesh.inputs[2])

    float_curve_005 = nodes.new("ShaderNodeFloatCurve")
    float_curve_005.inputs[0].default_value = 1.0
    links.new(math_006.outputs[0], float_curve_005.inputs[1])
    links.new(float_curve_005.outputs[0], math_008.inputs[0])

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.operation = "MULTIPLY_ADD"
    vector_math_006.inputs[0].default_value = [0.0, -0.003000000026077032, 0.0]
    vector_math_006.inputs[3].default_value = 1.0
    links.new(vector_math_006.outputs[0], vector_math_005.inputs[2])
    links.new(vector_002.outputs[0], vector_math_006.inputs[2])
    links.new(math_007.outputs[0], vector_math_006.inputs[1])

    frame = nodes.new("NodeFrame")
    frame.text = None
    frame.shrink = True
    frame.label_size = 20

    reroute_005 = nodes.new("NodeReroute")
    reroute_005.socket_idname = "NodeSocketBool"
    links.new(reroute_005.outputs[0], boolean_math_001.inputs[1])
    links.new(capture_attribute_003.outputs[1], reroute_005.inputs[0])

    reroute_006 = nodes.new("NodeReroute")
    reroute_006.socket_idname = "NodeSocketFloat"
    links.new(reroute_006.outputs[0], compare_001.inputs[0])
    links.new(capture_attribute_003.outputs[1], reroute_006.inputs[0])

    reroute_007 = nodes.new("NodeReroute")
    reroute_007.socket_idname = "NodeSocketBool"
    links.new(reroute_007.outputs[0], boolean_math.inputs[0])
    links.new(capture_attribute_002.outputs[1], reroute_007.inputs[0])

    reroute_008 = nodes.new("NodeReroute")
    reroute_008.socket_idname = "NodeSocketFloat"
    links.new(reroute_006.outputs[0], reroute_008.inputs[0])

    reroute_009 = nodes.new("NodeReroute")
    reroute_009.socket_idname = "NodeSocketFloat"
    links.new(reroute_009.outputs[0], math_004.inputs[0])
    links.new(reroute_008.outputs[0], reroute_009.inputs[0])

    reroute_010 = nodes.new("NodeReroute")
    reroute_010.socket_idname = "NodeSocketFloat"
    links.new(reroute_006.outputs[0], reroute_010.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    compare.inputs[1].default_value = 0.5
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
    compare.inputs[12].default_value = 0.10100000351667404
    links.new(reroute_010.outputs[0], compare.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "FLOAT"
    links.new(extrude_mesh.outputs[1], switch.inputs[0])
    links.new(switch.outputs[0], repeat_output.inputs[1])
    links.new(repeat_input.outputs[3], switch.inputs[1])
    links.new(math_006.outputs[0], switch.inputs[2])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.operation = "EQUAL"
    compare_002.data_type = "FLOAT"
    compare_002.mode = "ELEMENT"
    compare_002.inputs[1].default_value = 0.36000001430511475
    compare_002.inputs[2].default_value = 0
    compare_002.inputs[3].default_value = 0
    compare_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[8].default_value = ""
    compare_002.inputs[9].default_value = ""
    compare_002.inputs[10].default_value = 0.8999999761581421
    compare_002.inputs[11].default_value = 0.08726649731397629
    compare_002.inputs[12].default_value = 0.3409999907016754
    links.new(repeat_output.outputs[1], compare_002.inputs[0])

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.operation = "AND"
    links.new(compare_002.outputs[0], boolean_math_002.inputs[0])
    links.new(compare.outputs[0], boolean_math_002.inputs[1])

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.domain = "FACE"
    links.new(repeat_output.outputs[0], separate_geometry.inputs[0])
    links.new(boolean_math_002.outputs[0], separate_geometry.inputs[1])

    rotate_on_centre = nodes.new("GeometryNodeGroup")
    rotate_on_centre.node_tree = create_rotate_on__centre_group()
    rotate_on_centre.inputs[1].default_value = Euler((0.10437069833278656, 0.0, -0.04712388664484024), 'XYZ')
    links.new(rotate_on_centre.outputs[0], group_output.inputs[0])

    rotate_on_centre_1 = nodes.new("GeometryNodeGroup")
    rotate_on_centre_1.node_tree = create_rotate_on__centre_group()
    rotate_on_centre_1.inputs[1].default_value = Euler((0.0, 0.2042035013437271, 0.0), 'XYZ')

    join_geometry_013 = nodes.new("GeometryNodeJoinGeometry")

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.inputs[1].default_value = "Components"
    transform_geometry.inputs[2].default_value = Vector((-0.006000000052154064, 0.0, -0.004999999888241291))
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry.inputs[4].default_value = Vector((1.0, 0.9800000190734863, 1.0))
    links.new(rotate_on_centre_1.outputs[0], transform_geometry.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.inputs[1].default_value = "Components"
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.0, 0.019999999552965164))
    transform_geometry_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_001.inputs[4].default_value = Vector((1.0099999904632568, 0.9800000190734863, 1.0))

    reroute_004 = nodes.new("NodeReroute")
    reroute_004.socket_idname = "NodeSocketGeometry"
    links.new(merge_by_distance_001.outputs[0], reroute_004.inputs[0])

    rotate_on_centre_2 = nodes.new("GeometryNodeGroup")
    rotate_on_centre_2.node_tree = create_rotate_on__centre_group()
    rotate_on_centre_2.inputs[1].default_value = Euler((0.0, 0.02635446935892105, 0.0), 'XYZ')
    links.new(reroute_004.outputs[0], rotate_on_centre_2.inputs[0])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.inputs[1].default_value = "Components"
    transform_geometry_002.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(rotate_on_centre_2.outputs[0], transform_geometry_002.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.operation = "SCALE"
    vector_math.inputs[0].default_value = [-0.5799999833106995, 0.0, 0.19999998807907104]
    vector_math.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math.inputs[3].default_value = 0.009999999776482582
    links.new(vector_math.outputs[0], transform_geometry_002.inputs[2])

    join_geometry_014 = nodes.new("GeometryNodeJoinGeometry")
    links.new(repeat_output.outputs[0], join_geometry_014.inputs[0])
    links.new(reroute_004.outputs[0], join_geometry_014.inputs[0])

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.inputs[1].default_value = True
    merge_by_distance.inputs[2].default_value = "All"
    merge_by_distance.inputs[3].default_value = 0.0010000000474974513
    links.new(join_geometry_014.outputs[0], merge_by_distance.inputs[0])
    links.new(merge_by_distance.outputs[0], join_geometry_013.inputs[0])

    join_geometry_015 = nodes.new("GeometryNodeJoinGeometry")
    links.new(transform_geometry_002.outputs[0], join_geometry_015.inputs[0])
    links.new(merge_by_distance.outputs[0], join_geometry_015.inputs[0])

    join_geometry_016 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_016.outputs[0], join_geometry_013.inputs[0])
    links.new(transform_geometry.outputs[0], join_geometry_016.inputs[0])
    links.new(transform_geometry_001.outputs[0], join_geometry_016.inputs[0])

    rotate_on_centre_3 = nodes.new("GeometryNodeGroup")
    rotate_on_centre_3.node_tree = create_rotate_on__centre_group()
    rotate_on_centre_3.inputs[1].default_value = Euler((0.0, 0.19373153150081635, 0.0), 'XYZ')
    links.new(rotate_on_centre_3.outputs[0], transform_geometry_001.inputs[0])

    reroute_011 = nodes.new("NodeReroute")
    reroute_011.socket_idname = "NodeSocketGeometry"
    links.new(reroute_011.outputs[0], rotate_on_centre_1.inputs[0])
    links.new(reroute_011.outputs[0], rotate_on_centre_3.inputs[0])

    join_geometry_017 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_017.outputs[0], reroute_011.inputs[0])

    frame_002 = nodes.new("NodeFrame")
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20

    rivet = nodes.new("GeometryNodeGroup")
    rivet.node_tree = create_rivet_group()
    rivet.inputs[1].default_value = False
    rivet.inputs[2].default_value = 0.9399999976158142
    rivet.inputs[3].default_value = 0.9399999976158142
    links.new(rivet.outputs[0], join_geometry_017.inputs[0])
    links.new(separate_geometry.outputs[0], rivet.inputs[0])

    rivet_1 = nodes.new("GeometryNodeGroup")
    rivet_1.node_tree = create_rivet_group()
    rivet_1.inputs[1].default_value = False
    rivet_1.inputs[2].default_value = -1.0799999237060547
    rivet_1.inputs[3].default_value = 0.9399999976158142
    links.new(transform_geometry_002.outputs[0], rivet_1.inputs[0])

    join_geometry_018 = nodes.new("GeometryNodeJoinGeometry")
    links.new(transform_geometry_002.outputs[0], join_geometry_018.inputs[0])
    links.new(rivet_1.outputs[0], join_geometry_018.inputs[0])
    links.new(join_geometry_018.outputs[0], join_geometry_013.inputs[0])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.node_tree = create_pipes_group()
    links.new(pipes.outputs[0], join_geometry_013.inputs[0])
    links.new(join_geometry_015.outputs[0], pipes.inputs[0])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.domain = "FACE"
    set_shade_smooth.inputs[1].default_value = True
    set_shade_smooth.inputs[2].default_value = True
    links.new(join_geometry_013.outputs[0], set_shade_smooth.inputs[0])

    gold_decorations = nodes.new("GeometryNodeGroup")
    gold_decorations.node_tree = create_gold__decorations_group()
    gold_decorations.inputs[1].default_value = 58
    gold_decorations.inputs[2].default_value = 1.5
    gold_decorations.inputs[3].default_value = 56

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.inputs[1].default_value = 200000.0
    gold_on_band.inputs[2].default_value = 8.669999122619629
    gold_on_band.inputs[3].default_value = 1

    subdivide_mesh = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh.inputs[1].default_value = 1

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.mode = "EDGES"
    mesh_to_curve.inputs[1].default_value = True

    is_edge_boundary_1 = nodes.new("GeometryNodeGroup")
    is_edge_boundary_1.node_tree = create_is__edge__boundary_group()

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "POINT"
    links.new(delete_geometry.outputs[0], mesh_to_curve.inputs[0])
    links.new(subdivide_mesh.outputs[0], delete_geometry.inputs[0])

    reroute_013 = nodes.new("NodeReroute")
    reroute_013.socket_idname = "NodeSocketGeometry"
    links.new(reroute_013.outputs[0], subdivide_mesh.inputs[0])
    links.new(flip_faces_005.outputs[0], reroute_013.inputs[0])

    sample_nearest_surface = nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.data_type = "FLOAT_VECTOR"
    sample_nearest_surface.inputs[2].default_value = 0
    sample_nearest_surface.inputs[3].default_value = [0.0, 0.0, 0.0]
    sample_nearest_surface.inputs[4].default_value = 0
    links.new(reroute_013.outputs[0], sample_nearest_surface.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.legacy_corner_normals = False
    links.new(normal.outputs[0], sample_nearest_surface.inputs[1])

    position = nodes.new("GeometryNodeInputPosition")
    _, pos_y, _ = separate_xyz(group, position.outputs[0])
    y_above_center = compare_op(group, "GREATER_THAN", "FLOAT", pos_y, 0.0)

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.operation = "OR"
    links.new(is_edge_boundary_1.outputs[0], boolean_math_003.inputs[0])
    links.new(boolean_math_003.outputs[0], delete_geometry.inputs[1])
    links.new(y_above_center, boolean_math_003.inputs[1])

    set_curve_normal_001 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.inputs[1].default_value = True
    set_curve_normal_001.inputs[2].default_value = "Free"
    links.new(mesh_to_curve.outputs[0], set_curve_normal_001.inputs[0])
    links.new(sample_nearest_surface.outputs[0], set_curve_normal_001.inputs[3])

    set_curve_tilt_003 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_003.inputs[1].default_value = True
    set_curve_tilt_003.inputs[2].default_value = -1.5707963705062866
    links.new(set_curve_tilt_003.outputs[0], gold_decorations.inputs[0])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.inputs[1].default_value = "Components"
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_003.inputs[4].default_value = Vector((1.0, -1.0, 1.0))

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.inputs[1].default_value = True
    links.new(transform_geometry_003.outputs[0], flip_faces.inputs[0])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    links.new(flip_faces.outputs[0], join_geometry.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry.outputs[0], join_geometry_001.inputs[0])
    links.new(gold_on_band.outputs[0], join_geometry_001.inputs[0])

    frame_003 = nodes.new("NodeFrame")
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "gold"
    store_named_attribute.inputs[3].default_value = True
    links.new(join_geometry_001.outputs[0], store_named_attribute.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.inputs[1].default_value = True
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(set_position.outputs[0], set_curve_tilt_003.inputs[0])
    links.new(set_curve_normal_001.outputs[0], set_position.inputs[0])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.operation = "SCALE"
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[3].default_value = 0.0020000000949949026
    links.new(vector_math_001.outputs[0], set_position.inputs[3])

    normal_003 = nodes.new("GeometryNodeInputNormal")
    normal_003.legacy_corner_normals = False
    links.new(normal_003.outputs[0], vector_math_001.inputs[0])

    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "POINT"
    links.new(delete_geometry_001.outputs[0], transform_geometry_003.inputs[0])
    links.new(delete_geometry_001.outputs[0], join_geometry.inputs[0])
    links.new(gold_decorations.outputs[0], delete_geometry_001.inputs[0])

    raycast = nodes.new("GeometryNodeRaycast")
    raycast.data_type = "FLOAT"
    raycast.inputs[1].default_value = 0.0
    raycast.inputs[2].default_value = "Interpolated"
    raycast.inputs[5].default_value = 0.10000000149011612
    links.new(reroute_013.outputs[0], raycast.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.operation = "MULTIPLY_ADD"
    vector_math_002.inputs[1].default_value = [0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513]
    vector_math_002.inputs[3].default_value = 1.0
    links.new(sample_nearest_surface.outputs[0], vector_math_002.inputs[0])
    links.new(position_001.outputs[0], vector_math_002.inputs[2])
    links.new(vector_math_002.outputs[0], raycast.inputs[3])

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.operation = "SCALE"
    vector_math_007.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_007.inputs[3].default_value = -1.0
    links.new(sample_nearest_surface.outputs[0], vector_math_007.inputs[0])
    links.new(vector_math_007.outputs[0], raycast.inputs[4])

    boolean_math_004 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.operation = "NOT"
    boolean_math_004.inputs[1].default_value = False
    links.new(raycast.outputs[0], boolean_math_004.inputs[0])
    links.new(boolean_math_004.outputs[0], delete_geometry_001.inputs[1])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    compare_004.inputs[1].default_value = 0.375
    compare_004.inputs[2].default_value = 0
    compare_004.inputs[3].default_value = 0
    compare_004.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_004.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_004.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_004.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_004.inputs[8].default_value = ""
    compare_004.inputs[9].default_value = ""
    compare_004.inputs[10].default_value = 0.8999999761581421
    compare_004.inputs[11].default_value = 0.08726649731397629
    compare_004.inputs[12].default_value = 0.0010000000474974513

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.mode = "EDGES"
    links.new(compare_004.outputs[0], mesh_to_curve_001.inputs[1])

    evaluate_on_domain = nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.domain = "POINT"
    evaluate_on_domain.data_type = "FLOAT"
    links.new(evaluate_on_domain.outputs[0], compare_004.inputs[0])
    links.new(repeat_output.outputs[1], evaluate_on_domain.inputs[0])

    capture_attribute_005 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_005.active_index = 0
    capture_attribute_005.domain = "POINT"
    links.new(capture_attribute_005.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(separate_geometry.outputs[0], capture_attribute_005.inputs[0])

    normal_004 = nodes.new("GeometryNodeInputNormal")
    normal_004.legacy_corner_normals = False
    links.new(normal_004.outputs[0], capture_attribute_005.inputs[1])

    set_curve_normal_002 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_002.inputs[1].default_value = True
    set_curve_normal_002.inputs[2].default_value = "Free"
    links.new(mesh_to_curve_001.outputs[0], set_curve_normal_002.inputs[0])
    links.new(capture_attribute_005.outputs[1], set_curve_normal_002.inputs[3])

    gold_decorations_1 = nodes.new("GeometryNodeGroup")
    gold_decorations_1.node_tree = create_gold__decorations_group()
    gold_decorations_1.inputs[1].default_value = 65
    gold_decorations_1.inputs[2].default_value = 3.0
    gold_decorations_1.inputs[3].default_value = 19

    set_curve_tilt_004 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_004.inputs[1].default_value = True
    set_curve_tilt_004.inputs[2].default_value = -1.5707963705062866
    links.new(set_curve_normal_002.outputs[0], set_curve_tilt_004.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20

    capture_attribute_006 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_006.active_index = 0
    capture_attribute_006.domain = "POINT"
    capture_attribute_006.inputs[1].default_value = True
    links.new(capture_attribute_006.outputs[0], join_geometry_017.inputs[0])
    links.new(separate_geometry.outputs[0], capture_attribute_006.inputs[0])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.domain = "POINT"
    links.new(separate_geometry_001.outputs[0], join_geometry_015.inputs[0])
    links.new(join_geometry_016.outputs[0], separate_geometry_001.inputs[0])
    links.new(capture_attribute_006.outputs[1], separate_geometry_001.inputs[1])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.inputs[1].default_value = "Components"
    transform_geometry_004.inputs[2].default_value = Vector((-0.0020000000949949026, 0.0, -0.004999999888241291))
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_004.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_004.outputs[0], gold_decorations_1.inputs[0])
    links.new(set_curve_tilt_004.outputs[0], transform_geometry_004.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.keep_last_segment = True
    resample_curve_001.inputs[1].default_value = True
    resample_curve_001.inputs[2].default_value = "Count"
    resample_curve_001.inputs[3].default_value = 15
    resample_curve_001.inputs[4].default_value = 0.10000000149011612
    links.new(transform_geometry_004.outputs[0], resample_curve_001.inputs[0])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.inputs[3].default_value = False
    instance_on_points_001.inputs[4].default_value = 0
    instance_on_points_001.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_001.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    links.new(resample_curve_001.outputs[0], instance_on_points_001.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.inputs[0].default_value = 0.004999999888241291
    ico_sphere.inputs[1].default_value = 2
    links.new(ico_sphere.outputs[0], instance_on_points_001.inputs[2])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.inputs[1].default_value = True
    realize_instances_001.inputs[2].default_value = True
    realize_instances_001.inputs[3].default_value = 0
    links.new(instance_on_points_001.outputs[0], realize_instances_001.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.domain = "FACE"
    set_shade_smooth_001.inputs[1].default_value = True
    set_shade_smooth_001.inputs[2].default_value = True
    links.new(realize_instances_001.outputs[0], set_shade_smooth_001.inputs[0])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    store_named_attribute_001.inputs[1].default_value = True
    store_named_attribute_001.inputs[2].default_value = "ruby"
    store_named_attribute_001.inputs[3].default_value = True
    links.new(set_shade_smooth_001.outputs[0], store_named_attribute_001.inputs[0])

    boolean_math_005 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.operation = "NOT"
    boolean_math_005.inputs[1].default_value = False
    links.new(boolean_math_005.outputs[0], instance_on_points_001.inputs[1])

    endpoint_selection_004 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_004.inputs[0].default_value = 1
    endpoint_selection_004.inputs[1].default_value = 1
    links.new(endpoint_selection_004.outputs[0], boolean_math_005.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    store_named_attribute_002.inputs[1].default_value = True
    store_named_attribute_002.inputs[2].default_value = "gold"
    store_named_attribute_002.inputs[3].default_value = True
    links.new(gold_decorations_1.outputs[0], store_named_attribute_002.inputs[0])

    instance_on_points_002 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.inputs[1].default_value = True
    instance_on_points_002.inputs[3].default_value = False
    instance_on_points_002.inputs[4].default_value = 0
    instance_on_points_002.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    distribute_points_on_faces.inputs[1].default_value = True
    distribute_points_on_faces.inputs[2].default_value = 0.0
    distribute_points_on_faces.inputs[3].default_value = 10.0
    distribute_points_on_faces.inputs[4].default_value = 20000.0
    distribute_points_on_faces.inputs[5].default_value = 1.0
    distribute_points_on_faces.inputs[6].default_value = 0
    links.new(distribute_points_on_faces.outputs[0], instance_on_points_002.inputs[0])

    ico_sphere_002 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_002.inputs[0].default_value = 0.0010000000474974513
    ico_sphere_002.inputs[1].default_value = 2
    links.new(ico_sphere_002.outputs[0], instance_on_points_002.inputs[2])

    realize_instances_002 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.inputs[1].default_value = True
    realize_instances_002.inputs[2].default_value = True
    realize_instances_002.inputs[3].default_value = 0
    links.new(instance_on_points_002.outputs[0], realize_instances_002.inputs[0])

    set_shade_smooth_002 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_002.domain = "FACE"
    set_shade_smooth_002.inputs[1].default_value = True
    set_shade_smooth_002.inputs[2].default_value = True
    links.new(realize_instances_002.outputs[0], set_shade_smooth_002.inputs[0])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    store_named_attribute_003.inputs[1].default_value = True
    store_named_attribute_003.inputs[2].default_value = "ruby"
    store_named_attribute_003.inputs[3].default_value = True
    links.new(set_shade_smooth_002.outputs[0], store_named_attribute_003.inputs[0])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.data_type = "FLOAT"
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_001.inputs[2].default_value = 1.0
    random_value_001.inputs[3].default_value = 1.5
    random_value_001.inputs[4].default_value = 0
    random_value_001.inputs[5].default_value = 100
    random_value_001.inputs[6].default_value = 0.5
    random_value_001.inputs[7].default_value = 0
    random_value_001.inputs[8].default_value = 0
    links.new(random_value_001.outputs[1], instance_on_points_002.inputs[6])

    frame_005 = nodes.new("NodeFrame")
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.data_type = "FLOAT2"
    store_named_attribute_004.domain = "CORNER"
    store_named_attribute_004.inputs[1].default_value = True
    store_named_attribute_004.inputs[2].default_value = "UVMap"
    links.new(store_named_attribute_004.outputs[0], set_position_003.inputs[0])
    links.new(curve_to_mesh.outputs[0], store_named_attribute_004.inputs[0])

    spline_parameter_004 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_004.outputs[0], capture_attribute_001.inputs[1])
    links.new(spline_parameter_004.outputs[0], capture_attribute.inputs[1])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.inputs[2].default_value = 0.0
    links.new(capture_attribute_001.outputs[1], combine_x_y_z.inputs[0])
    links.new(capture_attribute.outputs[1], combine_x_y_z.inputs[1])
    links.new(combine_x_y_z.outputs[0], store_named_attribute_004.inputs[3])

    delete_geometry_002 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.mode = "ALL"
    delete_geometry_002.domain = "FACE"
    links.new(transform_geometry_002.outputs[0], delete_geometry_002.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_002.outputs[0], separate_x_y_z_001.inputs[0])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.operation = "GREATER_THAN"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    compare_005.inputs[1].default_value = 0.0
    compare_005.inputs[2].default_value = 0
    compare_005.inputs[3].default_value = 0
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_005.inputs[8].default_value = ""
    compare_005.inputs[9].default_value = ""
    compare_005.inputs[10].default_value = 0.8999999761581421
    compare_005.inputs[11].default_value = 0.08726649731397629
    compare_005.inputs[12].default_value = 0.0010000000474974513
    links.new(separate_x_y_z_001.outputs[1], compare_005.inputs[0])
    links.new(compare_005.outputs[0], delete_geometry_002.inputs[1])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.data_type = "FLOAT_VECTOR"
    named_attribute.inputs[0].default_value = "UVMap"

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    gem_in_holder.inputs[1].default_value = "ruby"
    gem_in_holder.inputs[2].default_value = True
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    gem_in_holder.inputs[4].default_value = 20
    gem_in_holder.inputs[5].default_value = 15
    gem_in_holder.inputs[6].default_value = True
    gem_in_holder.inputs[7].default_value = 4
    gem_in_holder.inputs[8].default_value = 5
    gem_in_holder.inputs[9].default_value = 1.0
    gem_in_holder.inputs[10].default_value = 3.179999589920044

    gem_in_holder_1 = nodes.new("GeometryNodeGroup")
    gem_in_holder_1.node_tree = create_gem_in__holder_group()
    gem_in_holder_1.inputs[0].default_value = 0.009999999776482582
    gem_in_holder_1.inputs[1].default_value = "ruby"
    gem_in_holder_1.inputs[2].default_value = False
    gem_in_holder_1.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_1.inputs[4].default_value = 20
    gem_in_holder_1.inputs[5].default_value = 10
    gem_in_holder_1.inputs[6].default_value = True
    gem_in_holder_1.inputs[8].default_value = 5
    gem_in_holder_1.inputs[9].default_value = 0.0020000000949949026
    gem_in_holder_1.inputs[10].default_value = 2.609999656677246

    gem_in_holder_2 = nodes.new("GeometryNodeGroup")
    gem_in_holder_2.node_tree = create_gem_in__holder_group()
    gem_in_holder_2.inputs[0].default_value = 0.009999999776482582
    gem_in_holder_2.inputs[1].default_value = "ruby"
    gem_in_holder_2.inputs[2].default_value = True
    gem_in_holder_2.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_2.inputs[4].default_value = 20
    gem_in_holder_2.inputs[5].default_value = 15
    gem_in_holder_2.inputs[6].default_value = True
    gem_in_holder_2.inputs[7].default_value = 6
    gem_in_holder_2.inputs[8].default_value = 10
    gem_in_holder_2.inputs[9].default_value = 1.0
    gem_in_holder_2.inputs[10].default_value = 2.7799999713897705

    instance_on_points_003 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.inputs[1].default_value = True
    instance_on_points_003.inputs[3].default_value = False
    instance_on_points_003.inputs[4].default_value = 0
    instance_on_points_003.inputs[6].default_value = Vector((0.5, 0.5, 0.5))
    links.new(gem_in_holder.outputs[0], instance_on_points_003.inputs[2])

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.mode = "RADIUS"
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle.inputs[4].default_value = 0.029999999329447746
    links.new(curve_circle.outputs[0], instance_on_points_003.inputs[0])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    links.new(instance_on_points_003.outputs[0], join_geometry_002.inputs[0])
    links.new(gem_in_holder_1.outputs[0], join_geometry_002.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.inputs[1].default_value = "Components"
    transform_geometry_005.inputs[2].default_value = Vector((-0.07999999821186066, 0.0, 0.0))
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(gem_in_holder_2.outputs[0], transform_geometry_005.inputs[0])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    links.new(transform_geometry_005.outputs[0], join_geometry_003.inputs[0])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.inputs[1].default_value = "Components"
    transform_geometry_006.inputs[2].default_value = Vector((0.07999999821186066, 0.0, 0.0))
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_006.inputs[4].default_value = Vector((0.699999988079071, 0.699999988079071, 0.699999988079071))
    links.new(transform_geometry_006.outputs[0], join_geometry_003.inputs[0])
    links.new(join_geometry_002.outputs[0], transform_geometry_006.inputs[0])

    curve_tangent = nodes.new("GeometryNodeInputTangent")

    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.axis = "X"
    align_rotation_to_vector_002.pivot_axis = "AUTO"
    align_rotation_to_vector_002.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_002.inputs[1].default_value = 1.0
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_002.inputs[2])
    links.new(align_rotation_to_vector_002.outputs[0], instance_on_points_003.inputs[5])

    integer = nodes.new("FunctionNodeInputInt")
    integer.integer = 5
    links.new(integer.outputs[0], gem_in_holder_1.inputs[7])
    links.new(integer.outputs[0], curve_circle.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20

    frame_007 = nodes.new("NodeFrame")
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20

    frame_008 = nodes.new("NodeFrame")
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20

    realize_instances_003 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.inputs[1].default_value = True
    realize_instances_003.inputs[2].default_value = True
    realize_instances_003.inputs[3].default_value = 0
    links.new(join_geometry_003.outputs[0], realize_instances_003.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.inputs[1].default_value = False
    links.new(realize_instances_003.outputs[0], bounding_box.inputs[0])

    position_003 = nodes.new("GeometryNodeInputPosition")

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT_VECTOR"
    map_range.inputs[0].default_value = 1.0
    map_range.inputs[1].default_value = 0.0
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[3].default_value = 0.0
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[9].default_value = [0.009999999776482582, 0.05000000074505806, 0.009999999776482582]
    map_range.inputs[10].default_value = [0.9800000190734863, 0.949999988079071, 0.9990000128746033]
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(position_003.outputs[0], map_range.inputs[6])
    links.new(bounding_box.outputs[1], map_range.inputs[7])
    links.new(bounding_box.outputs[2], map_range.inputs[8])

    sample_u_v_surface = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface.data_type = "FLOAT_VECTOR"
    links.new(delete_geometry_002.outputs[0], sample_u_v_surface.inputs[0])
    links.new(map_range.outputs[1], sample_u_v_surface.inputs[3])

    position_005 = nodes.new("GeometryNodeInputPosition")
    links.new(position_005.outputs[0], sample_u_v_surface.inputs[1])

    sample_u_v_surface_001 = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface_001.data_type = "FLOAT_VECTOR"
    links.new(delete_geometry_002.outputs[0], sample_u_v_surface_001.inputs[0])
    links.new(map_range.outputs[1], sample_u_v_surface_001.inputs[3])

    normal_005 = nodes.new("GeometryNodeInputNormal")
    normal_005.legacy_corner_normals = False
    links.new(normal_005.outputs[0], sample_u_v_surface_001.inputs[1])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[1].default_value = True
    links.new(realize_instances_003.outputs[0], set_position_001.inputs[0])
    links.new(sample_u_v_surface.outputs[0], set_position_001.inputs[2])

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(named_attribute.outputs[0], separate_x_y_z_002.inputs[0])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.inputs[2].default_value = 0.0
    links.new(combine_x_y_z_001.outputs[0], sample_u_v_surface.inputs[2])
    links.new(combine_x_y_z_001.outputs[0], sample_u_v_surface_001.inputs[2])
    links.new(separate_x_y_z_002.outputs[1], combine_x_y_z_001.inputs[1])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.inputs[0].default_value = 1.0
    links.new(float_curve.outputs[0], combine_x_y_z_001.inputs[0])
    links.new(separate_x_y_z_002.outputs[0], float_curve.inputs[1])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.operation = "SCALE"
    vector_math_008.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(sample_u_v_surface_001.outputs[0], vector_math_008.inputs[0])
    links.new(vector_math_008.outputs[0], set_position_001.inputs[3])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(map_range.outputs[1], separate_x_y_z_003.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.operation = "MULTIPLY"
    math.inputs[1].default_value = 0.009999999776482582
    math.inputs[2].default_value = 0.5
    links.new(separate_x_y_z_003.outputs[2], math.inputs[0])
    links.new(math.outputs[0], vector_math_008.inputs[3])

    frame_009 = nodes.new("NodeFrame")
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.inputs[1].default_value = "Components"
    transform_geometry_007.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_007.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_007.inputs[4].default_value = Vector((1.0, -1.0, 1.0))
    links.new(set_position_001.outputs[0], transform_geometry_007.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.inputs[1].default_value = True
    links.new(transform_geometry_007.outputs[0], flip_faces_001.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    links.new(flip_faces_001.outputs[0], join_geometry_004.inputs[0])
    links.new(set_position_001.outputs[0], join_geometry_004.inputs[0])

    gem_in_holder_3 = nodes.new("GeometryNodeGroup")
    gem_in_holder_3.node_tree = create_gem_in__holder_group()
    gem_in_holder_3.inputs[0].default_value = 0.009999999776482582
    gem_in_holder_3.inputs[1].default_value = "ruby"
    gem_in_holder_3.inputs[2].default_value = True
    gem_in_holder_3.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_3.inputs[4].default_value = 20
    gem_in_holder_3.inputs[5].default_value = 15
    gem_in_holder_3.inputs[6].default_value = True
    gem_in_holder_3.inputs[7].default_value = 5
    gem_in_holder_3.inputs[8].default_value = 10
    gem_in_holder_3.inputs[9].default_value = 0.004999999888241291
    gem_in_holder_3.inputs[10].default_value = 23.56599998474121

    transform_geometry_008 = nodes.new("GeometryNodeTransform")
    transform_geometry_008.inputs[1].default_value = "Components"
    transform_geometry_008.inputs[2].default_value = Vector((0.009999999776482582, 0.0, 0.0))
    transform_geometry_008.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_008.inputs[4].default_value = Vector((1.2000000476837158, 1.2000000476837158, 1.2000000476837158))
    links.new(gem_in_holder_3.outputs[0], transform_geometry_008.inputs[0])
    links.new(transform_geometry_008.outputs[0], join_geometry_003.inputs[0])

    frame_010 = nodes.new("NodeFrame")
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "GEOMETRY"

    join_geometry_019 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_004.outputs[0], join_geometry_019.inputs[0])
    links.new(store_named_attribute_003.outputs[0], join_geometry_019.inputs[0])
    links.new(store_named_attribute.outputs[0], join_geometry_019.inputs[0])
    links.new(join_geometry_019.outputs[0], switch_001.inputs[2])

    group_input = nodes.new("NodeGroupInput")
    links.new(group_input.outputs[0], switch_001.inputs[0])

    frame_011 = nodes.new("NodeFrame")
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.input_type = "GEOMETRY"
    links.new(switch_002.outputs[0], join_geometry_017.inputs[0])

    group_input_001 = nodes.new("NodeGroupInput")
    links.new(group_input_001.outputs[0], switch_002.inputs[0])

    join_geometry_020 = nodes.new("GeometryNodeJoinGeometry")
    links.new(store_named_attribute_002.outputs[0], join_geometry_020.inputs[0])
    links.new(store_named_attribute_001.outputs[0], join_geometry_020.inputs[0])
    links.new(join_geometry_020.outputs[0], switch_002.inputs[2])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.domain = "POINT"
    links.new(repeat_output.outputs[0], separate_geometry_002.inputs[0])

    compare_006 = nodes.new("FunctionNodeCompare")
    compare_006.operation = "EQUAL"
    compare_006.data_type = "FLOAT"
    compare_006.mode = "ELEMENT"
    compare_006.inputs[1].default_value = 0.4000000059604645
    compare_006.inputs[2].default_value = 0
    compare_006.inputs[3].default_value = 0
    compare_006.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_006.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_006.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_006.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_006.inputs[8].default_value = ""
    compare_006.inputs[9].default_value = ""
    compare_006.inputs[10].default_value = 0.8999999761581421
    compare_006.inputs[11].default_value = 0.08726649731397629
    compare_006.inputs[12].default_value = 0.3009999990463257
    links.new(repeat_output.outputs[1], compare_006.inputs[0])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.data_type = "FLOAT_VECTOR"
    named_attribute_001.inputs[0].default_value = "UVMap"

    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(named_attribute_001.outputs[0], separate_x_y_z_004.inputs[0])

    compare_007 = nodes.new("FunctionNodeCompare")
    compare_007.operation = "EQUAL"
    compare_007.data_type = "FLOAT"
    compare_007.mode = "ELEMENT"
    compare_007.inputs[1].default_value = 0.0
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
    compare_007.inputs[12].default_value = 0.5199999809265137
    links.new(separate_x_y_z_004.outputs[0], compare_007.inputs[0])

    boolean_math_006 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_006.operation = "AND"
    links.new(compare_006.outputs[0], boolean_math_006.inputs[0])
    links.new(compare_007.outputs[0], boolean_math_006.inputs[1])
    links.new(boolean_math_006.outputs[0], separate_geometry_002.inputs[1])

    frame_012 = nodes.new("NodeFrame")
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20

    gem_in_holder_4 = nodes.new("GeometryNodeGroup")
    gem_in_holder_4.node_tree = create_gem_in__holder_group()
    gem_in_holder_4.inputs[0].default_value = 0.009999990463256836
    gem_in_holder_4.inputs[1].default_value = "ruby"
    gem_in_holder_4.inputs[2].default_value = False
    gem_in_holder_4.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_4.inputs[4].default_value = 20
    gem_in_holder_4.inputs[5].default_value = 10
    gem_in_holder_4.inputs[6].default_value = False
    gem_in_holder_4.inputs[7].default_value = 6
    gem_in_holder_4.inputs[8].default_value = 10

    position_006 = nodes.new("GeometryNodeInputPosition")

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.inputs[1].default_value = True
    links.new(position_006.outputs[0], for_each_geometry_element_input_001.inputs[2])

    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_019.inputs[0])

    transform_geometry_009 = nodes.new("GeometryNodeTransform")
    transform_geometry_009.inputs[1].default_value = "Components"
    transform_geometry_009.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_009.inputs[2])
    links.new(gem_in_holder_4.outputs[4], transform_geometry_009.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.rotation_space = "LOCAL"
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, 0.0, -1.3229594230651855), 'XYZ')
    links.new(rotate_rotation_002.outputs[0], transform_geometry_009.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[2], rotate_rotation_002.inputs[0])

    frame_016 = nodes.new("NodeFrame")
    frame_016.text = None
    frame_016.shrink = True
    frame_016.label_size = 20

    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.data_type = "FLOAT"
    random_value_007.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_007.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_007.inputs[2].default_value = 6.0
    random_value_007.inputs[3].default_value = 8.0
    random_value_007.inputs[4].default_value = 0
    random_value_007.inputs[5].default_value = 100
    random_value_007.inputs[6].default_value = 0.5
    random_value_007.inputs[8].default_value = 48
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_4.inputs[10])

    random_value_008 = nodes.new("FunctionNodeRandomValue")
    random_value_008.data_type = "FLOAT"
    random_value_008.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_008.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_008.inputs[2].default_value = 0.0
    random_value_008.inputs[3].default_value = 0.003000000026077032
    random_value_008.inputs[4].default_value = 0
    random_value_008.inputs[5].default_value = 100
    random_value_008.inputs[6].default_value = 0.5
    random_value_008.inputs[8].default_value = 10
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_008.inputs[7])
    links.new(random_value_008.outputs[1], gem_in_holder_4.inputs[9])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.inputs[1].default_value = True
    set_position_002.inputs[3].default_value = Vector((0.0, 0.0, 0.0))

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.target_element = "FACES"
    geometry_proximity_001.inputs[1].default_value = 0
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_001.inputs[3].default_value = 0
    links.new(geometry_proximity_001.outputs[0], set_position_002.inputs[2])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.inputs[3].default_value = False
    links.new(set_position_002.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(gem_in_holder_4.outputs[1], curve_to_mesh_002.inputs[1])
    links.new(gem_in_holder_4.outputs[2], curve_to_mesh_002.inputs[2])

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.socket_idname = "NodeSocketGeometry"
    links.new(transform_geometry_002.outputs[0], reroute_003.inputs[0])
    links.new(reroute_003.outputs[0], geometry_proximity_001.inputs[0])

    reroute_012 = nodes.new("NodeReroute")
    reroute_012.socket_idname = "NodeSocketGeometry"
    links.new(reroute_003.outputs[0], reroute_012.inputs[0])

    distribute_points_on_faces_001 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_001.distribute_method = "POISSON"
    distribute_points_on_faces_001.use_legacy_normal = False
    distribute_points_on_faces_001.inputs[2].default_value = 0.009999999776482582
    distribute_points_on_faces_001.inputs[3].default_value = 5000.0
    distribute_points_on_faces_001.inputs[4].default_value = 500.0
    distribute_points_on_faces_001.inputs[5].default_value = 1.0
    distribute_points_on_faces_001.inputs[6].default_value = 0
    links.new(reroute_012.outputs[0], distribute_points_on_faces_001.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.target_element = "POINTS"
    geometry_proximity.inputs[1].default_value = 0
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity.inputs[3].default_value = 0
    links.new(for_each_geometry_element_output_001.outputs[2], geometry_proximity.inputs[0])

    compare_008 = nodes.new("FunctionNodeCompare")
    compare_008.operation = "LESS_THAN"
    compare_008.data_type = "FLOAT"
    compare_008.mode = "ELEMENT"
    compare_008.inputs[1].default_value = 0.0020000000949949026
    compare_008.inputs[2].default_value = 0
    compare_008.inputs[3].default_value = 0
    compare_008.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_008.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_008.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_008.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_008.inputs[8].default_value = ""
    compare_008.inputs[9].default_value = ""
    compare_008.inputs[10].default_value = 0.8999999761581421
    compare_008.inputs[11].default_value = 0.08726649731397629
    compare_008.inputs[12].default_value = 0.0010000000474974513
    links.new(geometry_proximity.outputs[1], compare_008.inputs[0])

    gem_in_holder_5 = nodes.new("GeometryNodeGroup")
    gem_in_holder_5.node_tree = create_gem_in__holder_group()
    gem_in_holder_5.inputs[0].default_value = 0.00800000037997961
    gem_in_holder_5.inputs[1].default_value = "ruby"
    gem_in_holder_5.inputs[2].default_value = False
    gem_in_holder_5.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_5.inputs[4].default_value = 20
    gem_in_holder_5.inputs[5].default_value = 10
    gem_in_holder_5.inputs[6].default_value = False
    gem_in_holder_5.inputs[7].default_value = 6
    gem_in_holder_5.inputs[8].default_value = 10
    gem_in_holder_5.inputs[9].default_value = 0.0010000000474974513
    gem_in_holder_5.inputs[10].default_value = 6.6099958419799805

    instance_on_points_004 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_004.inputs[1].default_value = True
    instance_on_points_004.inputs[3].default_value = False
    instance_on_points_004.inputs[4].default_value = 0
    links.new(distribute_points_on_faces_001.outputs[0], instance_on_points_004.inputs[0])
    links.new(distribute_points_on_faces_001.outputs[2], instance_on_points_004.inputs[5])

    random_value_010 = nodes.new("FunctionNodeRandomValue")
    random_value_010.data_type = "FLOAT"
    random_value_010.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_010.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_010.inputs[2].default_value = 0.10000000894069672
    random_value_010.inputs[3].default_value = 0.5
    random_value_010.inputs[4].default_value = 0
    random_value_010.inputs[5].default_value = 100
    random_value_010.inputs[6].default_value = 0.5
    random_value_010.inputs[7].default_value = 0
    random_value_010.inputs[8].default_value = 0
    links.new(random_value_010.outputs[1], instance_on_points_004.inputs[6])

    frame_017 = nodes.new("NodeFrame")
    frame_017.text = None
    frame_017.shrink = True
    frame_017.label_size = 20

    realize_instances_004 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_004.inputs[1].default_value = True
    realize_instances_004.inputs[2].default_value = True
    realize_instances_004.inputs[3].default_value = 0

    transform_geometry_010 = nodes.new("GeometryNodeTransform")
    transform_geometry_010.inputs[1].default_value = "Components"
    transform_geometry_010.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    transform_geometry_010.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_010.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_010.outputs[0], instance_on_points_004.inputs[2])
    links.new(gem_in_holder_5.outputs[0], transform_geometry_010.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.inputs[2].default_value = "ruby"
    swap_attr.inputs[3].default_value = "saphire"
    links.new(realize_instances_004.outputs[0], swap_attr.inputs[0])
    links.new(swap_attr.outputs[0], join_geometry_019.inputs[0])

    capture_attribute_008 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_008.active_index = 0
    capture_attribute_008.domain = "INSTANCE"
    links.new(capture_attribute_008.outputs[0], realize_instances_004.inputs[0])
    links.new(instance_on_points_004.outputs[0], capture_attribute_008.inputs[0])
    links.new(capture_attribute_008.outputs[1], swap_attr.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    links.new(index.outputs[0], capture_attribute_008.inputs[1])

    join_geometry_021 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_021.outputs[0], rotate_on_centre.inputs[0])
    links.new(set_shade_smooth.outputs[0], join_geometry_021.inputs[0])
    links.new(switch_001.outputs[0], join_geometry_021.inputs[0])

    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.data_type = "BOOLEAN"
    store_named_attribute_005.domain = "POINT"
    store_named_attribute_005.inputs[1].default_value = True
    store_named_attribute_005.inputs[2].default_value = "gold"
    store_named_attribute_005.inputs[3].default_value = True
    links.new(store_named_attribute_005.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute_005.inputs[0])

    distribute_points_on_faces_002 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_002.distribute_method = "RANDOM"
    distribute_points_on_faces_002.use_legacy_normal = False
    distribute_points_on_faces_002.inputs[1].default_value = True
    distribute_points_on_faces_002.inputs[2].default_value = 0.0
    distribute_points_on_faces_002.inputs[3].default_value = 10.0
    distribute_points_on_faces_002.inputs[4].default_value = 8000.0
    distribute_points_on_faces_002.inputs[5].default_value = 1.0
    distribute_points_on_faces_002.inputs[6].default_value = 2
    links.new(distribute_points_on_faces_002.outputs[2], for_each_geometry_element_input_001.inputs[2])

    delete_geometry_003 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_003.mode = "ALL"
    delete_geometry_003.domain = "POINT"
    links.new(delete_geometry_003.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(distribute_points_on_faces_002.outputs[0], delete_geometry_003.inputs[0])

    geometry_proximity_002 = nodes.new("GeometryNodeProximity")
    geometry_proximity_002.target_element = "FACES"
    geometry_proximity_002.inputs[1].default_value = 0
    geometry_proximity_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_002.inputs[3].default_value = 0
    links.new(join_geometry_004.outputs[0], geometry_proximity_002.inputs[0])

    compare_009 = nodes.new("FunctionNodeCompare")
    compare_009.operation = "LESS_THAN"
    compare_009.data_type = "FLOAT"
    compare_009.mode = "ELEMENT"
    compare_009.inputs[1].default_value = 0.004999999888241291
    compare_009.inputs[2].default_value = 0
    compare_009.inputs[3].default_value = 0
    compare_009.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_009.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_009.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_009.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_009.inputs[8].default_value = ""
    compare_009.inputs[9].default_value = ""
    compare_009.inputs[10].default_value = 0.8999999761581421
    compare_009.inputs[11].default_value = 0.08726649731397629
    compare_009.inputs[12].default_value = 0.0010000000474974513
    links.new(geometry_proximity_002.outputs[1], compare_009.inputs[0])
    links.new(compare_009.outputs[0], delete_geometry_003.inputs[1])

    delete_geometry_004 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_004.mode = "ALL"
    delete_geometry_004.domain = "POINT"
    links.new(delete_geometry_004.outputs[0], set_position_002.inputs[0])
    links.new(transform_geometry_009.outputs[0], delete_geometry_004.inputs[0])

    geometry_proximity_003 = nodes.new("GeometryNodeProximity")
    geometry_proximity_003.target_element = "FACES"
    geometry_proximity_003.inputs[1].default_value = 0
    geometry_proximity_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_003.inputs[3].default_value = 0

    reroute_014 = nodes.new("NodeReroute")
    reroute_014.socket_idname = "NodeSocketGeometry"
    links.new(reroute_014.outputs[0], distribute_points_on_faces_002.inputs[0])
    links.new(reroute_003.outputs[0], reroute_014.inputs[0])
    links.new(reroute_014.outputs[0], geometry_proximity_003.inputs[0])

    compare_010 = nodes.new("FunctionNodeCompare")
    compare_010.operation = "GREATER_THAN"
    compare_010.data_type = "FLOAT"
    compare_010.mode = "ELEMENT"
    compare_010.inputs[1].default_value = 0.009999999776482582
    compare_010.inputs[2].default_value = 0
    compare_010.inputs[3].default_value = 0
    compare_010.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_010.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_010.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_010.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_010.inputs[8].default_value = ""
    compare_010.inputs[9].default_value = ""
    compare_010.inputs[10].default_value = 0.8999999761581421
    compare_010.inputs[11].default_value = 0.08726649731397629
    compare_010.inputs[12].default_value = 0.0010000000474974513
    links.new(geometry_proximity_003.outputs[1], compare_010.inputs[0])
    links.new(compare_010.outputs[0], delete_geometry_004.inputs[1])

    separate_geometry_003 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_003.domain = "FACE"
    links.new(merge_by_distance_001.outputs[0], separate_geometry_003.inputs[0])

    separate_x_y_z_005 = nodes.new("ShaderNodeSeparateXYZ")

    named_attribute_002 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.data_type = "FLOAT_VECTOR"
    named_attribute_002.inputs[0].default_value = "UVMap"
    links.new(named_attribute_002.outputs[0], separate_x_y_z_005.inputs[0])

    compare_011 = nodes.new("FunctionNodeCompare")
    compare_011.operation = "GREATER_THAN"
    compare_011.data_type = "FLOAT"
    compare_011.mode = "ELEMENT"
    compare_011.inputs[1].default_value = 0.8999999761581421
    compare_011.inputs[2].default_value = 0
    compare_011.inputs[3].default_value = 0
    compare_011.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_011.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_011.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_011.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_011.inputs[8].default_value = ""
    compare_011.inputs[9].default_value = ""
    compare_011.inputs[10].default_value = 0.8999999761581421
    compare_011.inputs[11].default_value = 0.08726649731397629
    compare_011.inputs[12].default_value = 0.0010000000474974513
    links.new(separate_x_y_z_005.outputs[0], compare_011.inputs[0])
    links.new(compare_011.outputs[0], separate_geometry_003.inputs[1])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    links.new(separate_geometry_002.outputs[1], join_geometry_005.inputs[0])
    links.new(separate_geometry_003.outputs[0], join_geometry_005.inputs[0])

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.inputs[1].default_value = True
    merge_by_distance_002.inputs[2].default_value = "All"
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    links.new(merge_by_distance_002.outputs[0], gold_on_band.inputs[0])
    links.new(merge_by_distance_002.outputs[0], distribute_points_on_faces.inputs[0])
    links.new(join_geometry_005.outputs[0], merge_by_distance_002.inputs[0])

    frame_018 = nodes.new("NodeFrame")
    frame_018.text = None
    frame_018.shrink = True
    frame_018.label_size = 20

    geometry_proximity_004 = nodes.new("GeometryNodeProximity")
    geometry_proximity_004.target_element = "POINTS"
    geometry_proximity_004.inputs[1].default_value = 0
    geometry_proximity_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_004.inputs[3].default_value = 0
    links.new(join_geometry_004.outputs[0], geometry_proximity_004.inputs[0])

    compare_012 = nodes.new("FunctionNodeCompare")
    compare_012.operation = "GREATER_THAN"
    compare_012.data_type = "FLOAT"
    compare_012.mode = "ELEMENT"
    compare_012.inputs[1].default_value = 0.003000000026077032
    compare_012.inputs[2].default_value = 0
    compare_012.inputs[3].default_value = 0
    compare_012.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_012.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_012.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_012.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_012.inputs[8].default_value = ""
    compare_012.inputs[9].default_value = ""
    compare_012.inputs[10].default_value = 0.8999999761581421
    compare_012.inputs[11].default_value = 0.08726649731397629
    compare_012.inputs[12].default_value = 0.0010000000474974513
    links.new(geometry_proximity_004.outputs[1], compare_012.inputs[0])

    boolean_math_007 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_007.operation = "AND"
    links.new(boolean_math_007.outputs[0], distribute_points_on_faces_001.inputs[1])
    links.new(compare_008.outputs[0], boolean_math_007.inputs[0])
    links.new(compare_012.outputs[0], boolean_math_007.inputs[1])

    auto_layout_nodes(group)
    return group
