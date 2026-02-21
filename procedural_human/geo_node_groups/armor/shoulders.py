import bpy
from mathutils import Vector, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group

@geo_node_group
def create_shoulders_group():
    group_name = "Shoulders"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (13900.0, 40.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    bézier_segment_004 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_004.name = "Bézier Segment.004"
    bézier_segment_004.label = ""
    bézier_segment_004.location = (249.0, -415.79998779296875)
    bézier_segment_004.bl_label = "Bézier Segment"
    bézier_segment_004.mode = "OFFSET"
    # Resolution
    bézier_segment_004.inputs[0].default_value = 16
    # Start
    bézier_segment_004.inputs[1].default_value = Vector((-0.23098699748516083, 0.009999999776482582, 0.39754199981689453))
    # Start Handle
    bézier_segment_004.inputs[2].default_value = Vector((0.0, -0.10000000149011612, 0.0))
    # End Handle
    bézier_segment_004.inputs[3].default_value = Vector((-0.05999999865889549, 0.029999999329447746, 0.019999999552965164))
    # End
    bézier_segment_004.inputs[4].default_value = Vector((-0.10215499997138977, -0.13706600666046143, 0.31426501274108887))
    # Links for bézier_segment_004

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (1969.0, -435.79998779296875)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh

    arc = nodes.new("GeometryNodeCurveArc")
    arc.name = "Arc"
    arc.label = ""
    arc.location = (1229.0, -735.7999877929688)
    arc.bl_label = "Arc"
    arc.mode = "RADIUS"
    # Resolution
    arc.inputs[0].default_value = 24
    # Start
    arc.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    arc.inputs[2].default_value = Vector((0.0, 2.0, 0.0))
    # End
    arc.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Start Angle
    arc.inputs[5].default_value = 1.3089969158172607
    # Sweep Angle
    arc.inputs[6].default_value = 0.5235987901687622
    # Offset Angle
    arc.inputs[7].default_value = 0.0
    # Connect Center
    arc.inputs[8].default_value = False
    # Invert Arc
    arc.inputs[9].default_value = False
    # Links for arc

    transform_geometry_012 = nodes.new("GeometryNodeTransform")
    transform_geometry_012.name = "Transform Geometry.012"
    transform_geometry_012.label = ""
    transform_geometry_012.location = (1389.0, -735.7999877929688)
    transform_geometry_012.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_012.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_012.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_012.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_012
    links.new(arc.outputs[0], transform_geometry_012.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    set_curve_tilt.label = ""
    set_curve_tilt.location = (409.0, -415.79998779296875)
    set_curve_tilt.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Tilt
    set_curve_tilt.inputs[2].default_value = -2.0682151317596436
    # Links for set_curve_tilt
    links.new(bézier_segment_004.outputs[0], set_curve_tilt.inputs[0])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.label = ""
    spline_parameter.location = (769.0, -575.7999877929688)
    spline_parameter.bl_label = "Spline Parameter"
    # Links for spline_parameter

    float_curve_003 = nodes.new("ShaderNodeFloatCurve")
    float_curve_003.name = "Float Curve.003"
    float_curve_003.label = ""
    float_curve_003.location = (769.0, -635.7999877929688)
    float_curve_003.bl_label = "Float Curve"
    # Factor
    float_curve_003.inputs[0].default_value = 1.0
    # Links for float_curve_003
    links.new(spline_parameter.outputs[0], float_curve_003.inputs[1])

    value_001 = nodes.new("ShaderNodeValue")
    value_001.name = "Value.001"
    value_001.label = ""
    value_001.location = (1229.0, -955.7999877929688)
    value_001.bl_label = "Value"
    # Links for value_001
    links.new(value_001.outputs[0], arc.inputs[4])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (1389.0, -995.7999877929688)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "SCALE"
    # Vector
    vector_math_003.inputs[0].default_value = [0.0, -0.9799999594688416, 0.0]
    # Vector
    vector_math_003.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_003
    links.new(value_001.outputs[0], vector_math_003.inputs[3])
    links.new(vector_math_003.outputs[0], transform_geometry_012.inputs[2])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (589.0, -415.79998779296875)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Count"
    # Count
    resample_curve.inputs[3].default_value = 16
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve
    links.new(set_curve_tilt.outputs[0], resample_curve.inputs[0])

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.label = ""
    capture_attribute.location = (1549.0, -735.7999877929688)
    capture_attribute.bl_label = "Capture Attribute"
    capture_attribute.active_index = 1
    capture_attribute.domain = "POINT"
    # Links for capture_attribute
    links.new(capture_attribute.outputs[0], curve_to_mesh.inputs[1])
    links.new(transform_geometry_012.outputs[0], capture_attribute.inputs[0])
    links.new(spline_parameter.outputs[0], capture_attribute.inputs[1])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (1769.0, -435.79998779296875)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 2
    capture_attribute_001.domain = "POINT"
    # Links for capture_attribute_001
    links.new(capture_attribute_001.outputs[0], curve_to_mesh.inputs[0])

    endpoint_selection = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection.name = "Endpoint Selection"
    endpoint_selection.label = ""
    endpoint_selection.location = (1389.0, -435.79998779296875)
    endpoint_selection.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection.inputs[0].default_value = 0
    # End Size
    endpoint_selection.inputs[1].default_value = 1
    # Links for endpoint_selection
    links.new(endpoint_selection.outputs[0], capture_attribute_001.inputs[1])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (789.0, -55.79999923706055)
    instance_on_points.bl_label = "Instance on Points"
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Scale
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points
    links.new(endpoint_selection.outputs[0], instance_on_points.inputs[1])

    arc_001 = nodes.new("GeometryNodeCurveArc")
    arc_001.name = "Arc.001"
    arc_001.label = ""
    arc_001.location = (369.0, -35.79999923706055)
    arc_001.bl_label = "Arc"
    arc_001.mode = "RADIUS"
    # Resolution
    arc_001.inputs[0].default_value = 32
    # Start
    arc_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    arc_001.inputs[2].default_value = Vector((0.0, 2.0, 0.0))
    # End
    arc_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    arc_001.inputs[4].default_value = 0.04000002145767212
    # Start Angle
    arc_001.inputs[5].default_value = 0.0
    # Sweep Angle
    arc_001.inputs[6].default_value = 3.1415927410125732
    # Offset Angle
    arc_001.inputs[7].default_value = 0.0
    # Connect Center
    arc_001.inputs[8].default_value = False
    # Invert Arc
    arc_001.inputs[9].default_value = False
    # Links for arc_001

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.label = ""
    align_rotation_to_vector.location = (209.0, -375.79998779296875)
    align_rotation_to_vector.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector

    set_curve_radius = nodes.new("GeometryNodeSetCurveRadius")
    set_curve_radius.name = "Set Curve Radius"
    set_curve_radius.label = ""
    set_curve_radius.location = (1149.0, -415.79998779296875)
    set_curve_radius.bl_label = "Set Curve Radius"
    # Selection
    set_curve_radius.inputs[1].default_value = True
    # Links for set_curve_radius
    links.new(set_curve_radius.outputs[0], capture_attribute_001.inputs[0])
    links.new(set_curve_radius.outputs[0], instance_on_points.inputs[0])
    links.new(float_curve_003.outputs[0], set_curve_radius.inputs[2])

    radius = nodes.new("GeometryNodeInputRadius")
    radius.name = "Radius"
    radius.label = ""
    radius.location = (1969.0, -575.7999877929688)
    radius.bl_label = "Radius"
    # Links for radius
    links.new(radius.outputs[0], curve_to_mesh.inputs[2])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.label = ""
    align_rotation_to_vector_001.location = (389.0, -375.79998779296875)
    align_rotation_to_vector_001.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_001.axis = "Y"
    align_rotation_to_vector_001.pivot_axis = "X"
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_001
    links.new(align_rotation_to_vector.outputs[0], align_rotation_to_vector_001.inputs[0])

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.name = "Normal.001"
    normal_001.label = ""
    normal_001.location = (29.0, -455.79998779296875)
    normal_001.bl_label = "Normal"
    normal_001.legacy_corner_normals = False
    # Links for normal_001
    links.new(normal_001.outputs[0], align_rotation_to_vector.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.name = "Rotate Rotation"
    rotate_rotation.label = ""
    rotate_rotation.location = (549.0, -395.79998779296875)
    rotate_rotation.bl_label = "Rotate Rotation"
    rotate_rotation.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation.inputs[1].default_value = Euler((-0.12514010071754456, 0.0, 0.0), 'XYZ')
    # Links for rotate_rotation
    links.new(rotate_rotation.outputs[0], instance_on_points.inputs[5])
    links.new(align_rotation_to_vector_001.outputs[0], rotate_rotation.inputs[0])

    transform_geometry_013 = nodes.new("GeometryNodeTransform")
    transform_geometry_013.name = "Transform Geometry.013"
    transform_geometry_013.label = ""
    transform_geometry_013.location = (549.0, -35.79999923706055)
    transform_geometry_013.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_013.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_013.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    # Rotation
    transform_geometry_013.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_013.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_013
    links.new(transform_geometry_013.outputs[0], instance_on_points.inputs[2])
    links.new(arc_001.outputs[0], transform_geometry_013.inputs[0])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    set_position_003.label = ""
    set_position_003.location = (3169.0, -495.79998779296875)
    set_position_003.bl_label = "Set Position"
    # Offset
    set_position_003.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_003
    links.new(capture_attribute_001.outputs[1], set_position_003.inputs[1])

    frame_013 = nodes.new("NodeFrame")
    frame_013.name = "Frame.013"
    frame_013.label = "End curve"
    frame_013.location = (1720.0, -820.0)
    frame_013.bl_label = "Frame"
    frame_013.text = None
    frame_013.shrink = True
    frame_013.label_size = 20
    # Links for frame_013

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (949.0, -55.79999923706055)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(instance_on_points.outputs[0], realize_instances.inputs[0])

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.label = ""
    sample_curve.location = (1109.0, -55.79999923706055)
    sample_curve.bl_label = "Sample Curve"
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = True
    sample_curve.data_type = "FLOAT"
    # Value
    sample_curve.inputs[1].default_value = 0.0
    # Length
    sample_curve.inputs[3].default_value = 0.0
    # Curve Index
    sample_curve.inputs[4].default_value = 0
    # Links for sample_curve
    links.new(realize_instances.outputs[0], sample_curve.inputs[0])
    links.new(sample_curve.outputs[1], set_position_003.inputs[2])
    links.new(capture_attribute.outputs[1], sample_curve.inputs[2])

    transform_geometry_015 = nodes.new("GeometryNodeTransform")
    transform_geometry_015.name = "Transform Geometry.015"
    transform_geometry_015.label = ""
    transform_geometry_015.location = (3809.0, -555.7999877929688)
    transform_geometry_015.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_015.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_015.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_015.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_015.inputs[4].default_value = Vector((1.0, -1.0, 1.0))
    # Links for transform_geometry_015

    flip_faces_006 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_006.name = "Flip Faces.006"
    flip_faces_006.label = ""
    flip_faces_006.location = (3969.0, -555.7999877929688)
    flip_faces_006.bl_label = "Flip Faces"
    # Selection
    flip_faces_006.inputs[1].default_value = True
    # Links for flip_faces_006
    links.new(transform_geometry_015.outputs[0], flip_faces_006.inputs[0])

    join_geometry_012 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_012.name = "Join Geometry.012"
    join_geometry_012.label = ""
    join_geometry_012.location = (4129.0, -495.79998779296875)
    join_geometry_012.bl_label = "Join Geometry"
    # Links for join_geometry_012
    links.new(flip_faces_006.outputs[0], join_geometry_012.inputs[0])

    endpoint_selection_001 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_001.name = "Endpoint Selection.001"
    endpoint_selection_001.label = ""
    endpoint_selection_001.location = (1389.0, -595.7999877929688)
    endpoint_selection_001.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection_001.inputs[0].default_value = 1
    # End Size
    endpoint_selection_001.inputs[1].default_value = 0
    # Links for endpoint_selection_001
    links.new(endpoint_selection_001.outputs[0], capture_attribute_001.inputs[2])

    curve_tangent_001 = nodes.new("GeometryNodeInputTangent")
    curve_tangent_001.name = "Curve Tangent.001"
    curve_tangent_001.label = ""
    curve_tangent_001.location = (209.0, -515.7999877929688)
    curve_tangent_001.bl_label = "Curve Tangent"
    # Links for curve_tangent_001
    links.new(curve_tangent_001.outputs[0], align_rotation_to_vector_001.inputs[2])

    set_position_004 = nodes.new("GeometryNodeSetPosition")
    set_position_004.name = "Set Position.004"
    set_position_004.label = ""
    set_position_004.location = (3589.0, -495.79998779296875)
    set_position_004.bl_label = "Set Position"
    # Offset
    set_position_004.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_004
    links.new(set_position_004.outputs[0], transform_geometry_015.inputs[0])
    links.new(set_position_004.outputs[0], join_geometry_012.inputs[0])
    links.new(set_position_003.outputs[0], set_position_004.inputs[0])

    position_004 = nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"
    position_004.label = ""
    position_004.location = (3329.0, -595.7999877929688)
    position_004.bl_label = "Position"
    # Links for position_004

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (3329.0, -655.7999877929688)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "MULTIPLY"
    # Vector
    vector_math_004.inputs[1].default_value = [1.0, 0.0, 1.0]
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(position_004.outputs[0], vector_math_004.inputs[0])
    links.new(vector_math_004.outputs[0], set_position_004.inputs[2])

    merge_by_distance_001 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_001.name = "Merge by Distance.001"
    merge_by_distance_001.label = ""
    merge_by_distance_001.location = (4309.0, -495.79998779296875)
    merge_by_distance_001.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_001.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_001.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_001
    links.new(join_geometry_012.outputs[0], merge_by_distance_001.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (3509.0, -555.7999877929688)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketBool"
    # Links for reroute
    links.new(reroute.outputs[0], set_position_004.inputs[1])
    links.new(capture_attribute_001.outputs[2], reroute.inputs[0])

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (4269.0, -435.79998779296875)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketBool"
    # Links for reroute_001
    links.new(reroute_001.outputs[0], merge_by_distance_001.inputs[1])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (3529.0, -435.79998779296875)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketBool"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], reroute_001.inputs[0])
    links.new(reroute.outputs[0], reroute_002.inputs[0])

    mesh_to_curve_002 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.name = "Mesh to Curve.002"
    mesh_to_curve_002.label = ""
    mesh_to_curve_002.location = (209.0, -35.800018310546875)
    mesh_to_curve_002.bl_label = "Mesh to Curve"
    mesh_to_curve_002.mode = "EDGES"
    # Links for mesh_to_curve_002

    frame_014 = nodes.new("NodeFrame")
    frame_014.name = "Frame.014"
    frame_014.label = "Shoulder Cover"
    frame_014.location = (-5249.0, 875.7999877929688)
    frame_014.bl_label = "Frame"
    frame_014.text = None
    frame_014.shrink = True
    frame_014.label_size = 20
    # Links for frame_014

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Is Edge Boundary.001"
    is_edge_boundary.label = ""
    is_edge_boundary.location = (209.0, -175.80001831054688)
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    is_edge_boundary.bl_label = "Group"
    # Links for is_edge_boundary
    links.new(is_edge_boundary.outputs[0], mesh_to_curve_002.inputs[1])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (1209.0, -35.800018310546875)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_001.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False
    # Links for curve_to_mesh_001

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.label = ""
    curve_line.location = (809.0, -355.8000183105469)
    curve_line.bl_label = "Curve Line"
    curve_line.mode = "POINTS"
    # Start
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    # End
    curve_line.inputs[1].default_value = Vector((0.019999999552965164, 0.0, 0.0))
    # Direction
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    # Length
    curve_line.inputs[3].default_value = 1.0
    # Links for curve_line

    set_curve_tilt_001 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_001.name = "Set Curve Tilt.001"
    set_curve_tilt_001.label = ""
    set_curve_tilt_001.location = (769.0, -35.800018310546875)
    set_curve_tilt_001.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_001.inputs[1].default_value = True
    # Tilt
    set_curve_tilt_001.inputs[2].default_value = -7.752577304840088
    # Links for set_curve_tilt_001

    flip_faces_005 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_005.name = "Flip Faces.005"
    flip_faces_005.label = ""
    flip_faces_005.location = (1369.0, -35.800018310546875)
    flip_faces_005.bl_label = "Flip Faces"
    # Selection
    flip_faces_005.inputs[1].default_value = True
    # Links for flip_faces_005
    links.new(curve_to_mesh_001.outputs[0], flip_faces_005.inputs[0])

    frame_015 = nodes.new("NodeFrame")
    frame_015.name = "Frame.015"
    frame_015.label = "Outer Band"
    frame_015.location = (-729.0, 275.8000183105469)
    frame_015.bl_label = "Frame"
    frame_015.text = None
    frame_015.shrink = True
    frame_015.label_size = 20
    # Links for frame_015

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.name = "Capture Attribute.002"
    capture_attribute_002.label = ""
    capture_attribute_002.location = (989.0, -355.8000183105469)
    capture_attribute_002.bl_label = "Capture Attribute"
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "POINT"
    # Links for capture_attribute_002
    links.new(capture_attribute_002.outputs[0], curve_to_mesh_001.inputs[1])
    links.new(curve_line.outputs[0], capture_attribute_002.inputs[0])

    endpoint_selection_002 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_002.name = "Endpoint Selection.002"
    endpoint_selection_002.label = ""
    endpoint_selection_002.location = (989.0, -475.8000183105469)
    endpoint_selection_002.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection_002.inputs[0].default_value = 0
    # End Size
    endpoint_selection_002.inputs[1].default_value = 1
    # Links for endpoint_selection_002
    links.new(endpoint_selection_002.outputs[0], capture_attribute_002.inputs[1])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (473.83331298828125, -335.79998779296875)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "AND"
    # Links for boolean_math

    capture_attribute_003 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.name = "Capture Attribute.003"
    capture_attribute_003.label = ""
    capture_attribute_003.location = (989.0, -35.800018310546875)
    capture_attribute_003.bl_label = "Capture Attribute"
    capture_attribute_003.active_index = 1
    capture_attribute_003.domain = "POINT"
    # Links for capture_attribute_003
    links.new(capture_attribute_003.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(set_curve_tilt_001.outputs[0], capture_attribute_003.inputs[0])

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.label = ""
    spline_parameter_001.location = (989.0, -175.80001831054688)
    spline_parameter_001.bl_label = "Spline Parameter"
    # Links for spline_parameter_001
    links.new(spline_parameter_001.outputs[0], capture_attribute_003.inputs[1])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (113.83331298828125, -455.79998779296875)
    compare_001.bl_label = "Compare"
    compare_001.operation = "EQUAL"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = 0.5
    # A
    compare_001.inputs[2].default_value = 0
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
    compare_001.inputs[12].default_value = 0.1210000067949295
    # Links for compare_001

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.label = ""
    extrude_mesh.location = (1853.833251953125, -115.79999542236328)
    extrude_mesh.bl_label = "Extrude Mesh"
    extrude_mesh.mode = "EDGES"
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.07000000029802322
    # Individual
    extrude_mesh.inputs[4].default_value = True
    # Links for extrude_mesh

    repeat_input = nodes.new("GeometryNodeRepeatInput")
    repeat_input.name = "Repeat Input"
    repeat_input.label = ""
    repeat_input.location = (673.8333129882812, -175.79998779296875)
    repeat_input.bl_label = "Repeat Input"
    # Value
    repeat_input.inputs[3].default_value = 0.0
    # Links for repeat_input
    links.new(flip_faces_005.outputs[0], repeat_input.inputs[1])
    links.new(repeat_input.outputs[1], extrude_mesh.inputs[0])
    links.new(boolean_math.outputs[0], repeat_input.inputs[2])
    links.new(repeat_input.outputs[2], extrude_mesh.inputs[1])

    repeat_output = nodes.new("GeometryNodeRepeatOutput")
    repeat_output.name = "Repeat Output"
    repeat_output.label = ""
    repeat_output.location = (2233.833251953125, -135.79998779296875)
    repeat_output.bl_label = "Repeat Output"
    repeat_output.active_index = 2
    repeat_output.inspection_index = 0
    # Links for repeat_output
    links.new(extrude_mesh.outputs[0], repeat_output.inputs[0])
    links.new(extrude_mesh.outputs[1], repeat_output.inputs[1])

    vector_002 = nodes.new("FunctionNodeInputVector")
    vector_002.name = "Vector.002"
    vector_002.label = ""
    vector_002.location = (1213.833251953125, -375.79998779296875)
    vector_002.bl_label = "Vector"
    vector_002.vector = Vector((-0.03999999910593033, 0.0, -0.14999999105930328))
    # Links for vector_002

    set_curve_tilt_002 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_002.name = "Set Curve Tilt.002"
    set_curve_tilt_002.label = ""
    set_curve_tilt_002.location = (769.0, -415.79998779296875)
    set_curve_tilt_002.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_002.inputs[1].default_value = True
    # Links for set_curve_tilt_002
    links.new(set_curve_tilt_002.outputs[0], set_curve_radius.inputs[0])
    links.new(resample_curve.outputs[0], set_curve_tilt_002.inputs[0])

    curve_tilt = nodes.new("GeometryNodeInputCurveTilt")
    curve_tilt.name = "Curve Tilt"
    curve_tilt.label = ""
    curve_tilt.location = (389.0, -175.79998779296875)
    curve_tilt.bl_label = "Curve Tilt"
    # Links for curve_tilt

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (569.0, -155.79998779296875)
    math_003.bl_label = "Math"
    math_003.operation = "SUBTRACT"
    math_003.use_clamp = False
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(curve_tilt.outputs[0], math_003.inputs[0])
    links.new(math_003.outputs[0], set_curve_tilt_002.inputs[2])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"
    spline_parameter_002.label = ""
    spline_parameter_002.location = (29.0, -35.79998779296875)
    spline_parameter_002.bl_label = "Spline Parameter"
    # Links for spline_parameter_002

    float_curve_004 = nodes.new("ShaderNodeFloatCurve")
    float_curve_004.name = "Float Curve.004"
    float_curve_004.label = ""
    float_curve_004.location = (29.0, -95.79998779296875)
    float_curve_004.bl_label = "Float Curve"
    # Factor
    float_curve_004.inputs[0].default_value = 1.0
    # Links for float_curve_004
    links.new(spline_parameter_002.outputs[0], float_curve_004.inputs[1])
    links.new(float_curve_004.outputs[0], math_003.inputs[1])

    capture_attribute_004 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_004.name = "Capture Attribute.004"
    capture_attribute_004.label = ""
    capture_attribute_004.location = (29.0, -55.800018310546875)
    capture_attribute_004.bl_label = "Capture Attribute"
    capture_attribute_004.active_index = 0
    capture_attribute_004.domain = "POINT"
    # Links for capture_attribute_004
    links.new(merge_by_distance_001.outputs[0], capture_attribute_004.inputs[0])
    links.new(capture_attribute_004.outputs[0], mesh_to_curve_002.inputs[0])

    normal_002 = nodes.new("GeometryNodeInputNormal")
    normal_002.name = "Normal.002"
    normal_002.label = ""
    normal_002.location = (29.0, -315.8000183105469)
    normal_002.bl_label = "Normal"
    normal_002.legacy_corner_normals = False
    # Links for normal_002

    set_curve_normal = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal.name = "Set Curve Normal"
    set_curve_normal.label = ""
    set_curve_normal.location = (469.0, -55.800018310546875)
    set_curve_normal.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal.inputs[1].default_value = True
    # Mode
    set_curve_normal.inputs[2].default_value = "Free"
    # Links for set_curve_normal
    links.new(mesh_to_curve_002.outputs[0], set_curve_normal.inputs[0])
    links.new(capture_attribute_004.outputs[1], set_curve_normal.inputs[3])
    links.new(set_curve_normal.outputs[0], set_curve_tilt_001.inputs[0])

    blur_attribute = nodes.new("GeometryNodeBlurAttribute")
    blur_attribute.name = "Blur Attribute"
    blur_attribute.label = ""
    blur_attribute.location = (29.0, -195.80001831054688)
    blur_attribute.bl_label = "Blur Attribute"
    blur_attribute.data_type = "FLOAT_VECTOR"
    # Iterations
    blur_attribute.inputs[1].default_value = 5
    # Weight
    blur_attribute.inputs[2].default_value = 1.0
    # Links for blur_attribute
    links.new(blur_attribute.outputs[0], capture_attribute_004.inputs[1])
    links.new(normal_002.outputs[0], blur_attribute.inputs[0])

    endpoint_selection_003 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_003.name = "Endpoint Selection.003"
    endpoint_selection_003.label = ""
    endpoint_selection_003.location = (989.0, -235.80001831054688)
    endpoint_selection_003.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection_003.inputs[0].default_value = 1
    # End Size
    endpoint_selection_003.inputs[1].default_value = 1
    # Links for endpoint_selection_003
    links.new(endpoint_selection_003.outputs[0], capture_attribute_003.inputs[2])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.label = ""
    boolean_math_001.location = (293.83331298828125, -455.79998779296875)
    boolean_math_001.bl_label = "Boolean Math"
    boolean_math_001.operation = "NIMPLY"
    # Links for boolean_math_001
    links.new(compare_001.outputs[0], boolean_math_001.inputs[0])
    links.new(boolean_math_001.outputs[0], boolean_math.inputs[1])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (873.8333129882812, -875.7999877929688)
    math_004.bl_label = "Math"
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 0.5
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004

    integer_001 = nodes.new("FunctionNodeInputInt")
    integer_001.name = "Integer.001"
    integer_001.label = ""
    integer_001.location = (673.8333129882812, -35.79999542236328)
    integer_001.bl_label = "Integer"
    integer_001.integer = 9
    # Links for integer_001
    links.new(integer_001.outputs[0], repeat_input.inputs[0])

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (673.8333129882812, -95.79999542236328)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "SUBTRACT"
    # Value
    integer_math.inputs[1].default_value = 1
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(integer_001.outputs[0], integer_math.inputs[0])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (673.8333129882812, -135.79998779296875)
    math_006.bl_label = "Math"
    math_006.operation = "DIVIDE"
    math_006.use_clamp = False
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(repeat_input.outputs[0], math_006.inputs[0])
    links.new(integer_math.outputs[0], math_006.inputs[1])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.label = ""
    math_007.location = (1053.833251953125, -875.7999877929688)
    math_007.bl_label = "Math"
    math_007.operation = "SIGN"
    math_007.use_clamp = False
    # Value
    math_007.inputs[1].default_value = 11.59999942779541
    # Value
    math_007.inputs[2].default_value = 0.5
    # Links for math_007
    links.new(math_004.outputs[0], math_007.inputs[0])

    math_008 = nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.label = ""
    math_008.location = (1213.833251953125, -595.7999877929688)
    math_008.bl_label = "Math"
    math_008.operation = "MULTIPLY"
    math_008.use_clamp = False
    # Value
    math_008.inputs[2].default_value = 0.5
    # Links for math_008
    links.new(math_007.outputs[0], math_008.inputs[1])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (1633.833251953125, -375.79998779296875)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "MULTIPLY_ADD"
    # Vector
    vector_math_005.inputs[0].default_value = [0.0, 0.09000000357627869, 0.0]
    # Scale
    vector_math_005.inputs[3].default_value = 1.0
    # Links for vector_math_005
    links.new(math_008.outputs[0], vector_math_005.inputs[1])
    links.new(vector_math_005.outputs[0], extrude_mesh.inputs[2])

    float_curve_005 = nodes.new("ShaderNodeFloatCurve")
    float_curve_005.name = "Float Curve.005"
    float_curve_005.label = ""
    float_curve_005.location = (953.8333129882812, -555.7999877929688)
    float_curve_005.bl_label = "Float Curve"
    # Factor
    float_curve_005.inputs[0].default_value = 1.0
    # Links for float_curve_005
    links.new(math_006.outputs[0], float_curve_005.inputs[1])
    links.new(float_curve_005.outputs[0], math_008.inputs[0])

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (1413.833251953125, -375.79998779296875)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "MULTIPLY_ADD"
    # Vector
    vector_math_006.inputs[0].default_value = [0.0, -0.003000000026077032, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006
    links.new(vector_math_006.outputs[0], vector_math_005.inputs[2])
    links.new(vector_002.outputs[0], vector_math_006.inputs[2])
    links.new(math_007.outputs[0], vector_math_006.inputs[1])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Arm Extension"
    frame.location = (946.1666870117188, -104.20000457763672)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    reroute_005 = nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.label = ""
    reroute_005.location = (233.83331298828125, -395.79998779296875)
    reroute_005.bl_label = "Reroute"
    reroute_005.socket_idname = "NodeSocketBool"
    # Links for reroute_005
    links.new(reroute_005.outputs[0], boolean_math_001.inputs[1])
    links.new(capture_attribute_003.outputs[2], reroute_005.inputs[0])

    reroute_006 = nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.label = ""
    reroute_006.location = (33.83331298828125, -455.79998779296875)
    reroute_006.bl_label = "Reroute"
    reroute_006.socket_idname = "NodeSocketFloat"
    # Links for reroute_006
    links.new(reroute_006.outputs[0], compare_001.inputs[0])
    links.new(capture_attribute_003.outputs[1], reroute_006.inputs[0])

    reroute_007 = nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    reroute_007.label = ""
    reroute_007.location = (313.83331298828125, -255.79998779296875)
    reroute_007.bl_label = "Reroute"
    reroute_007.socket_idname = "NodeSocketBool"
    # Links for reroute_007
    links.new(reroute_007.outputs[0], boolean_math.inputs[0])
    links.new(capture_attribute_002.outputs[1], reroute_007.inputs[0])

    reroute_008 = nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    reroute_008.label = ""
    reroute_008.location = (93.83331298828125, -855.7999877929688)
    reroute_008.bl_label = "Reroute"
    reroute_008.socket_idname = "NodeSocketFloat"
    # Links for reroute_008
    links.new(reroute_006.outputs[0], reroute_008.inputs[0])

    reroute_009 = nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    reroute_009.label = ""
    reroute_009.location = (833.8333129882812, -875.7999877929688)
    reroute_009.bl_label = "Reroute"
    reroute_009.socket_idname = "NodeSocketFloat"
    # Links for reroute_009
    links.new(reroute_009.outputs[0], math_004.inputs[0])
    links.new(reroute_008.outputs[0], reroute_009.inputs[0])

    reroute_010 = nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    reroute_010.label = ""
    reroute_010.location = (3460.0, -560.0)
    reroute_010.bl_label = "Reroute"
    reroute_010.socket_idname = "NodeSocketFloat"
    # Links for reroute_010
    links.new(reroute_006.outputs[0], reroute_010.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (3520.0, -540.0)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.5
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
    compare.inputs[12].default_value = 0.10100000351667404
    # Links for compare
    links.new(reroute_010.outputs[0], compare.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (2053.833251953125, -195.79998779296875)
    switch.bl_label = "Switch"
    switch.input_type = "FLOAT"
    # Links for switch
    links.new(extrude_mesh.outputs[1], switch.inputs[0])
    links.new(switch.outputs[0], repeat_output.inputs[2])
    links.new(repeat_input.outputs[3], switch.inputs[1])
    links.new(math_006.outputs[0], switch.inputs[2])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.label = ""
    compare_002.location = (3520.0, -320.0)
    compare_002.bl_label = "Compare"
    compare_002.operation = "EQUAL"
    compare_002.data_type = "FLOAT"
    compare_002.mode = "ELEMENT"
    # B
    compare_002.inputs[1].default_value = 0.36000001430511475
    # A
    compare_002.inputs[2].default_value = 0
    # B
    compare_002.inputs[3].default_value = 0
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
    compare_002.inputs[12].default_value = 0.3409999907016754
    # Links for compare_002
    links.new(repeat_output.outputs[2], compare_002.inputs[0])

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.label = ""
    boolean_math_002.location = (3720.0, -360.0)
    boolean_math_002.bl_label = "Boolean Math"
    boolean_math_002.operation = "AND"
    # Links for boolean_math_002
    links.new(compare_002.outputs[0], boolean_math_002.inputs[0])
    links.new(compare.outputs[0], boolean_math_002.inputs[1])

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (3900.0, -240.0)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "FACE"
    # Links for separate_geometry
    links.new(repeat_output.outputs[0], separate_geometry.inputs[0])
    links.new(boolean_math_002.outputs[0], separate_geometry.inputs[1])

    rotate_on_centre = nodes.new("GeometryNodeGroup")
    rotate_on_centre.name = "Group"
    rotate_on_centre.label = ""
    rotate_on_centre.location = (13680.0, 80.0)
    rotate_on_centre.node_tree = create_rotate_on__centre_group()
    rotate_on_centre.bl_label = "Group"
    # Rotation
    rotate_on_centre.inputs[1].default_value = Euler((0.10437069833278656, 0.0, -0.04712388664484024), 'XYZ')
    # Links for rotate_on_centre
    links.new(rotate_on_centre.outputs[0], group_output.inputs[0])

    rotate_on_centre_1 = nodes.new("GeometryNodeGroup")
    rotate_on_centre_1.name = "Group.001"
    rotate_on_centre_1.label = ""
    rotate_on_centre_1.location = (73.83349609375, -92.86666870117188)
    rotate_on_centre_1.node_tree = create_rotate_on__centre_group()
    rotate_on_centre_1.bl_label = "Group"
    # Rotation
    rotate_on_centre_1.inputs[1].default_value = Euler((0.0, 0.2042035013437271, 0.0), 'XYZ')
    # Links for rotate_on_centre_1

    join_geometry_013 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_013.name = "Join Geometry.013"
    join_geometry_013.label = ""
    join_geometry_013.location = (12720.0, 0.0)
    join_geometry_013.bl_label = "Join Geometry"
    # Links for join_geometry_013

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (253.83349609375, -92.86666870117188)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((-0.006000000052154064, 0.0, -0.004999999888241291))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, 0.9800000190734863, 1.0))
    # Links for transform_geometry
    links.new(rotate_on_centre_1.outputs[0], transform_geometry.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (433.83349609375, -132.86666870117188)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.0, 0.019999999552965164))
    # Rotation
    transform_geometry_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0099999904632568, 0.9800000190734863, 1.0))
    # Links for transform_geometry_001

    reroute_004 = nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.label = ""
    reroute_004.location = (3200.0, 260.0)
    reroute_004.bl_label = "Reroute"
    reroute_004.socket_idname = "NodeSocketGeometry"
    # Links for reroute_004
    links.new(merge_by_distance_001.outputs[0], reroute_004.inputs[0])

    rotate_on_centre_2 = nodes.new("GeometryNodeGroup")
    rotate_on_centre_2.name = "Group.002"
    rotate_on_centre_2.label = ""
    rotate_on_centre_2.location = (3360.0, 460.0)
    rotate_on_centre_2.node_tree = create_rotate_on__centre_group()
    rotate_on_centre_2.bl_label = "Group"
    # Rotation
    rotate_on_centre_2.inputs[1].default_value = Euler((0.0, 0.02635446935892105, 0.0), 'XYZ')
    # Links for rotate_on_centre_2
    links.new(reroute_004.outputs[0], rotate_on_centre_2.inputs[0])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    transform_geometry_002.label = ""
    transform_geometry_002.location = (3520.0, 460.0)
    transform_geometry_002.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_002.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_002.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_002
    links.new(rotate_on_centre_2.outputs[0], transform_geometry_002.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (3520.0, 420.0)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "SCALE"
    # Vector
    vector_math.inputs[0].default_value = [-0.5799999833106995, 0.0, 0.19999998807907104]
    # Vector
    vector_math.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 0.009999999776482582
    # Links for vector_math
    links.new(vector_math.outputs[0], transform_geometry_002.inputs[2])

    join_geometry_014 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_014.name = "Join Geometry.014"
    join_geometry_014.label = ""
    join_geometry_014.location = (3560.0, 40.0)
    join_geometry_014.bl_label = "Join Geometry"
    # Links for join_geometry_014
    links.new(repeat_output.outputs[0], join_geometry_014.inputs[0])
    links.new(reroute_004.outputs[0], join_geometry_014.inputs[0])

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.label = ""
    merge_by_distance.location = (3740.0, 60.0)
    merge_by_distance.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance.inputs[1].default_value = True
    # Mode
    merge_by_distance.inputs[2].default_value = "All"
    # Distance
    merge_by_distance.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance
    links.new(join_geometry_014.outputs[0], merge_by_distance.inputs[0])
    links.new(merge_by_distance.outputs[0], join_geometry_013.inputs[0])

    join_geometry_015 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_015.name = "Join Geometry.015"
    join_geometry_015.label = ""
    join_geometry_015.location = (8880.0, 280.0)
    join_geometry_015.bl_label = "Join Geometry"
    # Links for join_geometry_015
    links.new(transform_geometry_002.outputs[0], join_geometry_015.inputs[0])
    links.new(merge_by_distance.outputs[0], join_geometry_015.inputs[0])

    join_geometry_016 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_016.name = "Join Geometry.016"
    join_geometry_016.label = ""
    join_geometry_016.location = (613.83349609375, -32.866668701171875)
    join_geometry_016.bl_label = "Join Geometry"
    # Links for join_geometry_016
    links.new(join_geometry_016.outputs[0], join_geometry_013.inputs[0])
    links.new(transform_geometry.outputs[0], join_geometry_016.inputs[0])
    links.new(transform_geometry_001.outputs[0], join_geometry_016.inputs[0])

    rotate_on_centre_3 = nodes.new("GeometryNodeGroup")
    rotate_on_centre_3.name = "Group.004"
    rotate_on_centre_3.label = ""
    rotate_on_centre_3.location = (73.83349609375, -272.8666687011719)
    rotate_on_centre_3.node_tree = create_rotate_on__centre_group()
    rotate_on_centre_3.bl_label = "Group"
    # Rotation
    rotate_on_centre_3.inputs[1].default_value = Euler((0.0, 0.19373153150081635, 0.0), 'XYZ')
    # Links for rotate_on_centre_3
    links.new(rotate_on_centre_3.outputs[0], transform_geometry_001.inputs[0])

    reroute_011 = nodes.new("NodeReroute")
    reroute_011.name = "Reroute.011"
    reroute_011.label = ""
    reroute_011.location = (33.83349609375, -172.86666870117188)
    reroute_011.bl_label = "Reroute"
    reroute_011.socket_idname = "NodeSocketGeometry"
    # Links for reroute_011
    links.new(reroute_011.outputs[0], rotate_on_centre_1.inputs[0])
    links.new(reroute_011.outputs[0], rotate_on_centre_3.inputs[0])

    join_geometry_017 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_017.name = "Join Geometry.017"
    join_geometry_017.label = ""
    join_geometry_017.location = (6260.0, -400.0)
    join_geometry_017.bl_label = "Join Geometry"
    # Links for join_geometry_017
    links.new(join_geometry_017.outputs[0], reroute_011.inputs[0])

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = ""
    frame_002.location = (6486.16650390625, -307.1333312988281)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    rivet = nodes.new("GeometryNodeGroup")
    rivet.name = "Group.006"
    rivet.label = ""
    rivet.location = (4360.0, -400.0)
    rivet.node_tree = create_rivet_group()
    rivet.bl_label = "Group"
    # Corners
    rivet.inputs[1].default_value = False
    # Offset
    rivet.inputs[2].default_value = 0.9399999976158142
    # Spacing
    rivet.inputs[3].default_value = 0.9399999976158142
    # Links for rivet
    links.new(rivet.outputs[0], join_geometry_017.inputs[0])
    links.new(separate_geometry.outputs[0], rivet.inputs[0])

    rivet_1 = nodes.new("GeometryNodeGroup")
    rivet_1.name = "Group.007"
    rivet_1.label = ""
    rivet_1.location = (4120.0, 300.0)
    rivet_1.node_tree = create_rivet_group()
    rivet_1.bl_label = "Group"
    # Corners
    rivet_1.inputs[1].default_value = False
    # Offset
    rivet_1.inputs[2].default_value = -1.0799999237060547
    # Spacing
    rivet_1.inputs[3].default_value = 0.9399999976158142
    # Links for rivet_1
    links.new(transform_geometry_002.outputs[0], rivet_1.inputs[0])

    join_geometry_018 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_018.name = "Join Geometry.018"
    join_geometry_018.label = ""
    join_geometry_018.location = (4280.0, 340.0)
    join_geometry_018.bl_label = "Join Geometry"
    # Links for join_geometry_018
    links.new(transform_geometry_002.outputs[0], join_geometry_018.inputs[0])
    links.new(rivet_1.outputs[0], join_geometry_018.inputs[0])
    links.new(join_geometry_018.outputs[0], join_geometry_013.inputs[0])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.name = "Group.005"
    pipes.label = ""
    pipes.location = (9320.0, 400.0)
    pipes.node_tree = create_pipes_group()
    pipes.bl_label = "Group"
    # Links for pipes
    links.new(pipes.outputs[0], join_geometry_013.inputs[0])
    links.new(join_geometry_015.outputs[0], pipes.inputs[0])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (12920.0, 20.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True
    # Links for set_shade_smooth
    links.new(join_geometry_013.outputs[0], set_shade_smooth.inputs[0])

    gold_decorations = nodes.new("GeometryNodeGroup")
    gold_decorations.name = "Group.008"
    gold_decorations.label = ""
    gold_decorations.location = (1469.0, -409.0)
    gold_decorations.node_tree = create_gold__decorations_group()
    gold_decorations.bl_label = "Group"
    # Seed
    gold_decorations.inputs[1].default_value = 58
    # Scale
    gold_decorations.inputs[2].default_value = 1.5
    # Count
    gold_decorations.inputs[3].default_value = 56
    # Links for gold_decorations

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.name = "Group.003"
    gold_on_band.label = ""
    gold_on_band.location = (1860.8330078125, -924.80029296875)
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.bl_label = "Group"
    # Density
    gold_on_band.inputs[1].default_value = 200000.0
    # W
    gold_on_band.inputs[2].default_value = 8.669999122619629
    # Seed
    gold_on_band.inputs[3].default_value = 1
    # Links for gold_on_band

    subdivide_mesh = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh.name = "Subdivide Mesh"
    subdivide_mesh.label = ""
    subdivide_mesh.location = (489.0, -409.0)
    subdivide_mesh.bl_label = "Subdivide Mesh"
    # Level
    subdivide_mesh.inputs[1].default_value = 1
    # Links for subdivide_mesh

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (809.0, -409.0)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Selection
    mesh_to_curve.inputs[1].default_value = True
    # Links for mesh_to_curve

    is_edge_boundary_1 = nodes.new("GeometryNodeGroup")
    is_edge_boundary_1.name = "Is Edge Boundary"
    is_edge_boundary_1.label = ""
    is_edge_boundary_1.location = (449.0, -509.0)
    is_edge_boundary_1.node_tree = create_is__edge__boundary_group()
    is_edge_boundary_1.bl_label = "Group"
    # Links for is_edge_boundary_1

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (649.0, -409.0)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "POINT"
    # Links for delete_geometry
    links.new(delete_geometry.outputs[0], mesh_to_curve.inputs[0])
    links.new(subdivide_mesh.outputs[0], delete_geometry.inputs[0])

    reroute_013 = nodes.new("NodeReroute")
    reroute_013.name = "Reroute.013"
    reroute_013.label = ""
    reroute_013.location = (249.0, -409.0)
    reroute_013.bl_label = "Reroute"
    reroute_013.socket_idname = "NodeSocketGeometry"
    # Links for reroute_013
    links.new(reroute_013.outputs[0], subdivide_mesh.inputs[0])
    links.new(flip_faces_005.outputs[0], reroute_013.inputs[0])

    sample_nearest_surface = nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.name = "Sample Nearest Surface"
    sample_nearest_surface.label = ""
    sample_nearest_surface.location = (309.0, -29.0)
    sample_nearest_surface.bl_label = "Sample Nearest Surface"
    sample_nearest_surface.data_type = "FLOAT_VECTOR"
    # Group ID
    sample_nearest_surface.inputs[2].default_value = 0
    # Sample Position
    sample_nearest_surface.inputs[3].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    sample_nearest_surface.inputs[4].default_value = 0
    # Links for sample_nearest_surface
    links.new(reroute_013.outputs[0], sample_nearest_surface.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.label = ""
    normal.location = (309.0, -249.0)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = False
    # Links for normal
    links.new(normal.outputs[0], sample_nearest_surface.inputs[1])

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (249.0, -489.0)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (29.0, -569.0)
    position.bl_label = "Position"
    # Links for position
    links.new(position.outputs[0], separate_x_y_z.inputs[0])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (249.0, -589.0)
    compare_003.bl_label = "Compare"
    compare_003.operation = "GREATER_THAN"
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
    compare_003.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_003
    links.new(separate_x_y_z.outputs[1], compare_003.inputs[0])

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.label = ""
    boolean_math_003.location = (649.0, -529.0)
    boolean_math_003.bl_label = "Boolean Math"
    boolean_math_003.operation = "OR"
    # Links for boolean_math_003
    links.new(is_edge_boundary_1.outputs[0], boolean_math_003.inputs[0])
    links.new(boolean_math_003.outputs[0], delete_geometry.inputs[1])
    links.new(compare_003.outputs[0], boolean_math_003.inputs[1])

    set_curve_normal_001 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.name = "Set Curve Normal.001"
    set_curve_normal_001.label = ""
    set_curve_normal_001.location = (989.0, -409.0)
    set_curve_normal_001.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_001.inputs[1].default_value = True
    # Mode
    set_curve_normal_001.inputs[2].default_value = "Free"
    # Links for set_curve_normal_001
    links.new(mesh_to_curve.outputs[0], set_curve_normal_001.inputs[0])
    links.new(sample_nearest_surface.outputs[0], set_curve_normal_001.inputs[3])

    set_curve_tilt_003 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_003.name = "Set Curve Tilt.003"
    set_curve_tilt_003.label = ""
    set_curve_tilt_003.location = (1309.0, -409.0)
    set_curve_tilt_003.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_003.inputs[1].default_value = True
    # Tilt
    set_curve_tilt_003.inputs[2].default_value = -1.5707963705062866
    # Links for set_curve_tilt_003
    links.new(set_curve_tilt_003.outputs[0], gold_decorations.inputs[0])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    transform_geometry_003.label = ""
    transform_geometry_003.location = (2169.0, -469.0)
    transform_geometry_003.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_003.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_003.inputs[4].default_value = Vector((1.0, -1.0, 1.0))
    # Links for transform_geometry_003

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.name = "Flip Faces"
    flip_faces.label = ""
    flip_faces.location = (2329.0, -469.0)
    flip_faces.bl_label = "Flip Faces"
    # Selection
    flip_faces.inputs[1].default_value = True
    # Links for flip_faces
    links.new(transform_geometry_003.outputs[0], flip_faces.inputs[0])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (2509.0, -429.0)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(flip_faces.outputs[0], join_geometry.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = ""
    frame_001.location = (407.0, -35.80029296875)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (2633.8330078125, -669.0)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(join_geometry.outputs[0], join_geometry_001.inputs[0])
    links.new(gold_on_band.outputs[0], join_geometry_001.inputs[0])

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Gold"
    frame_003.location = (6404.0, 6804.80029296875)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (2813.8330078125, -569.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(join_geometry_001.outputs[0], store_named_attribute.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (1149.0, -409.0)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Position
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position
    links.new(set_position.outputs[0], set_curve_tilt_003.inputs[0])
    links.new(set_curve_normal_001.outputs[0], set_position.inputs[0])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (989.0, -529.0)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "SCALE"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 0.0020000000949949026
    # Links for vector_math_001
    links.new(vector_math_001.outputs[0], set_position.inputs[3])

    normal_003 = nodes.new("GeometryNodeInputNormal")
    normal_003.name = "Normal.003"
    normal_003.label = ""
    normal_003.location = (809.0, -549.0)
    normal_003.bl_label = "Normal"
    normal_003.legacy_corner_normals = False
    # Links for normal_003
    links.new(normal_003.outputs[0], vector_math_001.inputs[0])

    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.label = ""
    delete_geometry_001.location = (1829.0, -389.0)
    delete_geometry_001.bl_label = "Delete Geometry"
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "POINT"
    # Links for delete_geometry_001
    links.new(delete_geometry_001.outputs[0], transform_geometry_003.inputs[0])
    links.new(delete_geometry_001.outputs[0], join_geometry.inputs[0])
    links.new(gold_decorations.outputs[0], delete_geometry_001.inputs[0])

    raycast = nodes.new("GeometryNodeRaycast")
    raycast.name = "Raycast"
    raycast.label = ""
    raycast.location = (1409.0, -29.0)
    raycast.bl_label = "Raycast"
    raycast.data_type = "FLOAT"
    # Attribute
    raycast.inputs[1].default_value = 0.0
    # Interpolation
    raycast.inputs[2].default_value = "Interpolated"
    # Ray Length
    raycast.inputs[5].default_value = 0.10000000149011612
    # Links for raycast
    links.new(reroute_013.outputs[0], raycast.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (769.0, -49.0)
    position_001.bl_label = "Position"
    # Links for position_001

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (949.0, -69.0)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "MULTIPLY_ADD"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0010000000474974513, 0.0010000000474974513, 0.0010000000474974513]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(sample_nearest_surface.outputs[0], vector_math_002.inputs[0])
    links.new(position_001.outputs[0], vector_math_002.inputs[2])
    links.new(vector_math_002.outputs[0], raycast.inputs[3])

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.label = ""
    vector_math_007.location = (1149.0, -229.0)
    vector_math_007.bl_label = "Vector Math"
    vector_math_007.operation = "SCALE"
    # Vector
    vector_math_007.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_007.inputs[3].default_value = -1.0
    # Links for vector_math_007
    links.new(sample_nearest_surface.outputs[0], vector_math_007.inputs[0])
    links.new(vector_math_007.outputs[0], raycast.inputs[4])

    boolean_math_004 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.name = "Boolean Math.004"
    boolean_math_004.label = ""
    boolean_math_004.location = (1609.0, -29.0)
    boolean_math_004.bl_label = "Boolean Math"
    boolean_math_004.operation = "NOT"
    # Boolean
    boolean_math_004.inputs[1].default_value = False
    # Links for boolean_math_004
    links.new(raycast.outputs[0], boolean_math_004.inputs[0])
    links.new(boolean_math_004.outputs[0], delete_geometry_001.inputs[1])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (3920.0, -620.0)
    compare_004.bl_label = "Compare"
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    # B
    compare_004.inputs[1].default_value = 0.375
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
    compare_004.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_004

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (189.0, -75.79998779296875)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Links for mesh_to_curve_001
    links.new(compare_004.outputs[0], mesh_to_curve_001.inputs[1])

    evaluate_on_domain = nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.name = "Evaluate on Domain"
    evaluate_on_domain.label = ""
    evaluate_on_domain.location = (3760.0, -620.0)
    evaluate_on_domain.bl_label = "Evaluate on Domain"
    evaluate_on_domain.domain = "POINT"
    evaluate_on_domain.data_type = "FLOAT"
    # Links for evaluate_on_domain
    links.new(evaluate_on_domain.outputs[0], compare_004.inputs[0])
    links.new(repeat_output.outputs[2], evaluate_on_domain.inputs[0])

    capture_attribute_005 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_005.name = "Capture Attribute.005"
    capture_attribute_005.label = ""
    capture_attribute_005.location = (29.0, -75.79998779296875)
    capture_attribute_005.bl_label = "Capture Attribute"
    capture_attribute_005.active_index = 0
    capture_attribute_005.domain = "POINT"
    # Links for capture_attribute_005
    links.new(capture_attribute_005.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(separate_geometry.outputs[0], capture_attribute_005.inputs[0])

    normal_004 = nodes.new("GeometryNodeInputNormal")
    normal_004.name = "Normal.004"
    normal_004.label = ""
    normal_004.location = (29.0, -195.79998779296875)
    normal_004.bl_label = "Normal"
    normal_004.legacy_corner_normals = False
    # Links for normal_004
    links.new(normal_004.outputs[0], capture_attribute_005.inputs[1])

    set_curve_normal_002 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_002.name = "Set Curve Normal.002"
    set_curve_normal_002.label = ""
    set_curve_normal_002.location = (349.0, -75.79998779296875)
    set_curve_normal_002.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_002.inputs[1].default_value = True
    # Mode
    set_curve_normal_002.inputs[2].default_value = "Free"
    # Links for set_curve_normal_002
    links.new(mesh_to_curve_001.outputs[0], set_curve_normal_002.inputs[0])
    links.new(capture_attribute_005.outputs[1], set_curve_normal_002.inputs[3])

    gold_decorations_1 = nodes.new("GeometryNodeGroup")
    gold_decorations_1.name = "Group.009"
    gold_decorations_1.label = ""
    gold_decorations_1.location = (849.0, -75.79998779296875)
    gold_decorations_1.node_tree = create_gold__decorations_group()
    gold_decorations_1.bl_label = "Group"
    # Seed
    gold_decorations_1.inputs[1].default_value = 65
    # Scale
    gold_decorations_1.inputs[2].default_value = 3.0
    # Count
    gold_decorations_1.inputs[3].default_value = 19
    # Links for gold_decorations_1

    set_curve_tilt_004 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_004.name = "Set Curve Tilt.004"
    set_curve_tilt_004.label = ""
    set_curve_tilt_004.location = (509.0, -75.79998779296875)
    set_curve_tilt_004.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_004.inputs[1].default_value = True
    # Tilt
    set_curve_tilt_004.inputs[2].default_value = -1.5707963705062866
    # Links for set_curve_tilt_004
    links.new(set_curve_normal_002.outputs[0], set_curve_tilt_004.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Gold"
    frame_004.location = (4191.0, -644.2000122070312)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    capture_attribute_006 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_006.name = "Capture Attribute.006"
    capture_attribute_006.label = ""
    capture_attribute_006.location = (4680.0, -260.0)
    capture_attribute_006.bl_label = "Capture Attribute"
    capture_attribute_006.active_index = 0
    capture_attribute_006.domain = "POINT"
    # Float
    capture_attribute_006.inputs[1].default_value = True
    # Links for capture_attribute_006
    links.new(capture_attribute_006.outputs[0], join_geometry_017.inputs[0])
    links.new(separate_geometry.outputs[0], capture_attribute_006.inputs[0])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.name = "Separate Geometry.001"
    separate_geometry_001.label = ""
    separate_geometry_001.location = (8540.0, 160.0)
    separate_geometry_001.bl_label = "Separate Geometry"
    separate_geometry_001.domain = "POINT"
    # Links for separate_geometry_001
    links.new(separate_geometry_001.outputs[0], join_geometry_015.inputs[0])
    links.new(join_geometry_016.outputs[0], separate_geometry_001.inputs[0])
    links.new(capture_attribute_006.outputs[1], separate_geometry_001.inputs[1])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    transform_geometry_004.label = ""
    transform_geometry_004.location = (669.0, -75.79998779296875)
    transform_geometry_004.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_004.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_004.inputs[2].default_value = Vector((-0.0020000000949949026, 0.0, -0.004999999888241291))
    # Rotation
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_004.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_004
    links.new(transform_geometry_004.outputs[0], gold_decorations_1.inputs[0])
    links.new(set_curve_tilt_004.outputs[0], transform_geometry_004.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (849.0, -295.79998779296875)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Count"
    # Count
    resample_curve_001.inputs[3].default_value = 15
    # Length
    resample_curve_001.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_001
    links.new(transform_geometry_004.outputs[0], resample_curve_001.inputs[0])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.label = ""
    instance_on_points_001.location = (1029.0, -295.79998779296875)
    instance_on_points_001.bl_label = "Instance on Points"
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Rotation
    instance_on_points_001.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_001.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_001
    links.new(resample_curve_001.outputs[0], instance_on_points_001.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    ico_sphere.label = ""
    ico_sphere.location = (849.0, -415.79998779296875)
    ico_sphere.bl_label = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.004999999888241291
    # Subdivisions
    ico_sphere.inputs[1].default_value = 2
    # Links for ico_sphere
    links.new(ico_sphere.outputs[0], instance_on_points_001.inputs[2])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.label = ""
    realize_instances_001.location = (1189.0, -295.79998779296875)
    realize_instances_001.bl_label = "Realize Instances"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0
    # Links for realize_instances_001
    links.new(instance_on_points_001.outputs[0], realize_instances_001.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.name = "Set Shade Smooth.001"
    set_shade_smooth_001.label = ""
    set_shade_smooth_001.location = (1349.0, -295.79998779296875)
    set_shade_smooth_001.bl_label = "Set Shade Smooth"
    set_shade_smooth_001.domain = "FACE"
    # Selection
    set_shade_smooth_001.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_001.inputs[2].default_value = True
    # Links for set_shade_smooth_001
    links.new(realize_instances_001.outputs[0], set_shade_smooth_001.inputs[0])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (1509.0, -295.79998779296875)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "ruby"
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001
    links.new(set_shade_smooth_001.outputs[0], store_named_attribute_001.inputs[0])

    boolean_math_005 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.name = "Boolean Math.005"
    boolean_math_005.label = ""
    boolean_math_005.location = (669.0, -415.79998779296875)
    boolean_math_005.bl_label = "Boolean Math"
    boolean_math_005.operation = "NOT"
    # Boolean
    boolean_math_005.inputs[1].default_value = False
    # Links for boolean_math_005
    links.new(boolean_math_005.outputs[0], instance_on_points_001.inputs[1])

    endpoint_selection_004 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_004.name = "Endpoint Selection.004"
    endpoint_selection_004.label = ""
    endpoint_selection_004.location = (489.0, -415.79998779296875)
    endpoint_selection_004.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection_004.inputs[0].default_value = 1
    # End Size
    endpoint_selection_004.inputs[1].default_value = 1
    # Links for endpoint_selection_004
    links.new(endpoint_selection_004.outputs[0], boolean_math_005.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (1029.0, -75.79998779296875)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_002.inputs[3].default_value = True
    # Links for store_named_attribute_002
    links.new(gold_decorations_1.outputs[0], store_named_attribute_002.inputs[0])

    instance_on_points_002 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.name = "Instance on Points.002"
    instance_on_points_002.label = ""
    instance_on_points_002.location = (313.8330078125, -35.80029296875)
    instance_on_points_002.bl_label = "Instance on Points"
    # Selection
    instance_on_points_002.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_002.inputs[3].default_value = False
    # Instance Index
    instance_on_points_002.inputs[4].default_value = 0
    # Rotation
    instance_on_points_002.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for instance_on_points_002

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.name = "Distribute Points on Faces"
    distribute_points_on_faces.label = ""
    distribute_points_on_faces.location = (113.83349609375, -35.80029296875)
    distribute_points_on_faces.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    # Selection
    distribute_points_on_faces.inputs[1].default_value = True
    # Distance Min
    distribute_points_on_faces.inputs[2].default_value = 0.0
    # Density Max
    distribute_points_on_faces.inputs[3].default_value = 10.0
    # Density
    distribute_points_on_faces.inputs[4].default_value = 20000.0
    # Density Factor
    distribute_points_on_faces.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces.inputs[6].default_value = 0
    # Links for distribute_points_on_faces
    links.new(distribute_points_on_faces.outputs[0], instance_on_points_002.inputs[0])

    ico_sphere_002 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_002.name = "Ico Sphere.002"
    ico_sphere_002.label = ""
    ico_sphere_002.location = (29.0, -255.80029296875)
    ico_sphere_002.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_002.inputs[0].default_value = 0.0010000000474974513
    # Subdivisions
    ico_sphere_002.inputs[1].default_value = 2
    # Links for ico_sphere_002
    links.new(ico_sphere_002.outputs[0], instance_on_points_002.inputs[2])

    realize_instances_002 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.name = "Realize Instances.002"
    realize_instances_002.label = ""
    realize_instances_002.location = (473.8330078125, -35.80029296875)
    realize_instances_002.bl_label = "Realize Instances"
    # Selection
    realize_instances_002.inputs[1].default_value = True
    # Realize All
    realize_instances_002.inputs[2].default_value = True
    # Depth
    realize_instances_002.inputs[3].default_value = 0
    # Links for realize_instances_002
    links.new(instance_on_points_002.outputs[0], realize_instances_002.inputs[0])

    set_shade_smooth_002 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_002.name = "Set Shade Smooth.002"
    set_shade_smooth_002.label = ""
    set_shade_smooth_002.location = (633.8330078125, -35.80029296875)
    set_shade_smooth_002.bl_label = "Set Shade Smooth"
    set_shade_smooth_002.domain = "FACE"
    # Selection
    set_shade_smooth_002.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_002.inputs[2].default_value = True
    # Links for set_shade_smooth_002
    links.new(realize_instances_002.outputs[0], set_shade_smooth_002.inputs[0])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (793.8330078125, -35.80029296875)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "ruby"
    # Value
    store_named_attribute_003.inputs[3].default_value = True
    # Links for store_named_attribute_003
    links.new(set_shade_smooth_002.outputs[0], store_named_attribute_003.inputs[0])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.label = ""
    random_value_001.location = (209.0, -295.80029296875)
    random_value_001.bl_label = "Random Value"
    random_value_001.data_type = "FLOAT"
    # Min
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_001.inputs[2].default_value = 1.0
    # Max
    random_value_001.inputs[3].default_value = 1.5
    # Min
    random_value_001.inputs[4].default_value = 0
    # Max
    random_value_001.inputs[5].default_value = 100
    # Probability
    random_value_001.inputs[6].default_value = 0.5
    # ID
    random_value_001.inputs[7].default_value = 0
    # Seed
    random_value_001.inputs[8].default_value = 0
    # Links for random_value_001
    links.new(random_value_001.outputs[1], instance_on_points_002.inputs[6])

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = "Extra Rubies"
    frame_005.location = (1647.0, -1289.0)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (2389.0, -415.79998779296875)
    store_named_attribute_004.bl_label = "Store Named Attribute"
    store_named_attribute_004.data_type = "FLOAT2"
    store_named_attribute_004.domain = "CORNER"
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute_004
    links.new(store_named_attribute_004.outputs[0], set_position_003.inputs[0])
    links.new(curve_to_mesh.outputs[0], store_named_attribute_004.inputs[0])

    spline_parameter_004 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_004.name = "Spline Parameter.004"
    spline_parameter_004.label = ""
    spline_parameter_004.location = (1229.0, -535.7999877929688)
    spline_parameter_004.bl_label = "Spline Parameter"
    # Links for spline_parameter_004
    links.new(spline_parameter_004.outputs[0], capture_attribute_001.inputs[3])
    links.new(spline_parameter_004.outputs[0], capture_attribute.inputs[2])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (2169.0, -575.7999877929688)
    combine_x_y_z.bl_label = "Combine XYZ"
    # Z
    combine_x_y_z.inputs[2].default_value = 0.0
    # Links for combine_x_y_z
    links.new(capture_attribute_001.outputs[3], combine_x_y_z.inputs[0])
    links.new(capture_attribute.outputs[2], combine_x_y_z.inputs[1])
    links.new(combine_x_y_z.outputs[0], store_named_attribute_004.inputs[3])

    delete_geometry_002 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.name = "Delete Geometry.002"
    delete_geometry_002.label = ""
    delete_geometry_002.location = (1787.0, -1113.800048828125)
    delete_geometry_002.bl_label = "Delete Geometry"
    delete_geometry_002.mode = "ALL"
    delete_geometry_002.domain = "FACE"
    # Links for delete_geometry_002
    links.new(transform_geometry_002.outputs[0], delete_geometry_002.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (1607.0, -1293.800048828125)
    position_002.bl_label = "Position"
    # Links for position_002

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (1607.0, -1353.800048828125)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001
    links.new(position_002.outputs[0], separate_x_y_z_001.inputs[0])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (1767.0, -1293.800048828125)
    compare_005.bl_label = "Compare"
    compare_005.operation = "GREATER_THAN"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    # B
    compare_005.inputs[1].default_value = 0.0
    # A
    compare_005.inputs[2].default_value = 0
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
    links.new(separate_x_y_z_001.outputs[1], compare_005.inputs[0])
    links.new(compare_005.outputs[0], delete_geometry_002.inputs[1])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (1467.0, -1493.800048828125)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "FLOAT_VECTOR"
    # Name
    named_attribute.inputs[0].default_value = "UVMap"
    # Links for named_attribute

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.name = "Group.010"
    gem_in_holder.label = ""
    gem_in_holder.location = (229.0, -369.0)
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.bl_label = "Group"
    # Gem Radius
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder.inputs[2].default_value = True
    # Scale
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder.inputs[4].default_value = 20
    # Seed
    gem_in_holder.inputs[5].default_value = 15
    # Wings
    gem_in_holder.inputs[6].default_value = True
    # Array Count
    gem_in_holder.inputs[7].default_value = 4
    # Strand Count
    gem_in_holder.inputs[8].default_value = 5
    # Split
    gem_in_holder.inputs[9].default_value = 1.0
    # Seed
    gem_in_holder.inputs[10].default_value = 3.179999589920044
    # Links for gem_in_holder

    gem_in_holder_1 = nodes.new("GeometryNodeGroup")
    gem_in_holder_1.name = "Group.011"
    gem_in_holder_1.label = ""
    gem_in_holder_1.location = (229.0, -29.0)
    gem_in_holder_1.node_tree = create_gem_in__holder_group()
    gem_in_holder_1.bl_label = "Group"
    # Gem Radius
    gem_in_holder_1.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_1.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_1.inputs[2].default_value = False
    # Scale
    gem_in_holder_1.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_1.inputs[4].default_value = 20
    # Seed
    gem_in_holder_1.inputs[5].default_value = 10
    # Wings
    gem_in_holder_1.inputs[6].default_value = True
    # Strand Count
    gem_in_holder_1.inputs[8].default_value = 5
    # Split
    gem_in_holder_1.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder_1.inputs[10].default_value = 2.609999656677246
    # Links for gem_in_holder_1

    gem_in_holder_2 = nodes.new("GeometryNodeGroup")
    gem_in_holder_2.name = "Group.012"
    gem_in_holder_2.label = ""
    gem_in_holder_2.location = (29.0, -29.0)
    gem_in_holder_2.node_tree = create_gem_in__holder_group()
    gem_in_holder_2.bl_label = "Group"
    # Gem Radius
    gem_in_holder_2.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_2.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_2.inputs[2].default_value = True
    # Scale
    gem_in_holder_2.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_2.inputs[4].default_value = 20
    # Seed
    gem_in_holder_2.inputs[5].default_value = 15
    # Wings
    gem_in_holder_2.inputs[6].default_value = True
    # Array Count
    gem_in_holder_2.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_2.inputs[8].default_value = 10
    # Split
    gem_in_holder_2.inputs[9].default_value = 1.0
    # Seed
    gem_in_holder_2.inputs[10].default_value = 2.7799999713897705
    # Links for gem_in_holder_2

    instance_on_points_003 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.name = "Instance on Points.003"
    instance_on_points_003.label = ""
    instance_on_points_003.location = (709.0, -189.0)
    instance_on_points_003.bl_label = "Instance on Points"
    # Selection
    instance_on_points_003.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_003.inputs[3].default_value = False
    # Instance Index
    instance_on_points_003.inputs[4].default_value = 0
    # Scale
    instance_on_points_003.inputs[6].default_value = Vector((0.5, 0.5, 0.5))
    # Links for instance_on_points_003
    links.new(gem_in_holder.outputs[0], instance_on_points_003.inputs[2])

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (529.0, -189.0)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle.inputs[4].default_value = 0.029999999329447746
    # Links for curve_circle
    links.new(curve_circle.outputs[0], instance_on_points_003.inputs[0])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (709.0, -149.0)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002
    links.new(instance_on_points_003.outputs[0], join_geometry_002.inputs[0])
    links.new(gem_in_holder_1.outputs[0], join_geometry_002.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.label = ""
    transform_geometry_005.location = (269.0, -29.0)
    transform_geometry_005.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_005.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_005.inputs[2].default_value = Vector((-0.07999999821186066, 0.0, 0.0))
    # Rotation
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_005
    links.new(gem_in_holder_2.outputs[0], transform_geometry_005.inputs[0])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (1198.0, -558.0)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003
    links.new(transform_geometry_005.outputs[0], join_geometry_003.inputs[0])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.name = "Transform Geometry.006"
    transform_geometry_006.label = ""
    transform_geometry_006.location = (869.0, -149.0)
    transform_geometry_006.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_006.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_006.inputs[2].default_value = Vector((0.07999999821186066, 0.0, 0.0))
    # Rotation
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_006.inputs[4].default_value = Vector((0.699999988079071, 0.699999988079071, 0.699999988079071))
    # Links for transform_geometry_006
    links.new(transform_geometry_006.outputs[0], join_geometry_003.inputs[0])
    links.new(join_geometry_002.outputs[0], transform_geometry_006.inputs[0])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (529.0, -329.0)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent

    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.name = "Align Rotation to Vector.002"
    align_rotation_to_vector_002.label = ""
    align_rotation_to_vector_002.location = (529.0, -389.0)
    align_rotation_to_vector_002.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_002.axis = "X"
    align_rotation_to_vector_002.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_002.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_002.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_002
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_002.inputs[2])
    links.new(align_rotation_to_vector_002.outputs[0], instance_on_points_003.inputs[5])

    integer = nodes.new("FunctionNodeInputInt")
    integer.name = "Integer"
    integer.label = ""
    integer.location = (29.0, -149.0)
    integer.bl_label = "Integer"
    integer.integer = 5
    # Links for integer
    links.new(integer.outputs[0], gem_in_holder_1.inputs[7])
    links.new(integer.outputs[0], curve_circle.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = ""
    frame_006.location = (29.0, -29.0)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    frame_007 = nodes.new("NodeFrame")
    frame_007.name = "Frame.007"
    frame_007.label = ""
    frame_007.location = (629.0, -769.0)
    frame_007.bl_label = "Frame"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20
    # Links for frame_007

    frame_008 = nodes.new("NodeFrame")
    frame_008.name = "Frame.008"
    frame_008.label = ""
    frame_008.location = (29.0, -35.800048828125)
    frame_008.bl_label = "Frame"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20
    # Links for frame_008

    realize_instances_003 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.name = "Realize Instances.003"
    realize_instances_003.label = ""
    realize_instances_003.location = (1198.0, -618.0)
    realize_instances_003.bl_label = "Realize Instances"
    # Selection
    realize_instances_003.inputs[1].default_value = True
    # Realize All
    realize_instances_003.inputs[2].default_value = True
    # Depth
    realize_instances_003.inputs[3].default_value = 0
    # Links for realize_instances_003
    links.new(join_geometry_003.outputs[0], realize_instances_003.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    bounding_box.label = ""
    bounding_box.location = (1687.0, -653.800048828125)
    bounding_box.bl_label = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = False
    # Links for bounding_box
    links.new(realize_instances_003.outputs[0], bounding_box.inputs[0])

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (1687.0, -573.800048828125)
    position_003.bl_label = "Position"
    # Links for position_003

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (1867.0, -573.800048828125)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT_VECTOR"
    # Value
    map_range.inputs[0].default_value = 1.0
    # From Min
    map_range.inputs[1].default_value = 0.0
    # From Max
    map_range.inputs[2].default_value = 1.0
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0
    # Steps
    map_range.inputs[5].default_value = 4.0
    # To Min
    map_range.inputs[9].default_value = [0.009999999776482582, 0.05000000074505806, 0.009999999776482582]
    # To Max
    map_range.inputs[10].default_value = [0.9800000190734863, 0.949999988079071, 0.9990000128746033]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(position_003.outputs[0], map_range.inputs[6])
    links.new(bounding_box.outputs[1], map_range.inputs[7])
    links.new(bounding_box.outputs[2], map_range.inputs[8])

    sample_u_v_surface = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface.name = "Sample UV Surface"
    sample_u_v_surface.label = ""
    sample_u_v_surface.location = (2287.0, -913.800048828125)
    sample_u_v_surface.bl_label = "Sample UV Surface"
    sample_u_v_surface.data_type = "FLOAT_VECTOR"
    # Links for sample_u_v_surface
    links.new(delete_geometry_002.outputs[0], sample_u_v_surface.inputs[0])
    links.new(map_range.outputs[1], sample_u_v_surface.inputs[3])

    position_005 = nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"
    position_005.label = ""
    position_005.location = (2287.0, -853.800048828125)
    position_005.bl_label = "Position"
    # Links for position_005
    links.new(position_005.outputs[0], sample_u_v_surface.inputs[1])

    sample_u_v_surface_001 = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface_001.name = "Sample UV Surface.001"
    sample_u_v_surface_001.label = ""
    sample_u_v_surface_001.location = (2467.0, -993.800048828125)
    sample_u_v_surface_001.bl_label = "Sample UV Surface"
    sample_u_v_surface_001.data_type = "FLOAT_VECTOR"
    # Links for sample_u_v_surface_001
    links.new(delete_geometry_002.outputs[0], sample_u_v_surface_001.inputs[0])
    links.new(map_range.outputs[1], sample_u_v_surface_001.inputs[3])

    normal_005 = nodes.new("GeometryNodeInputNormal")
    normal_005.name = "Normal.005"
    normal_005.label = ""
    normal_005.location = (2467.0, -933.800048828125)
    normal_005.bl_label = "Normal"
    normal_005.legacy_corner_normals = False
    # Links for normal_005
    links.new(normal_005.outputs[0], sample_u_v_surface_001.inputs[1])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (2807.0, -593.800048828125)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Links for set_position_001
    links.new(realize_instances_003.outputs[0], set_position_001.inputs[0])
    links.new(sample_u_v_surface.outputs[0], set_position_001.inputs[2])

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_002.name = "Separate XYZ.002"
    separate_x_y_z_002.label = ""
    separate_x_y_z_002.location = (1627.0, -1493.800048828125)
    separate_x_y_z_002.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_002
    links.new(named_attribute.outputs[0], separate_x_y_z_002.inputs[0])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (2107.0, -1473.800048828125)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # Z
    combine_x_y_z_001.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_001
    links.new(combine_x_y_z_001.outputs[0], sample_u_v_surface.inputs[2])
    links.new(combine_x_y_z_001.outputs[0], sample_u_v_surface_001.inputs[2])
    links.new(separate_x_y_z_002.outputs[1], combine_x_y_z_001.inputs[1])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (1827.0, -1513.800048828125)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(float_curve.outputs[0], combine_x_y_z_001.inputs[0])
    links.new(separate_x_y_z_002.outputs[0], float_curve.inputs[1])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.label = ""
    vector_math_008.location = (2647.0, -933.800048828125)
    vector_math_008.bl_label = "Vector Math"
    vector_math_008.operation = "SCALE"
    # Vector
    vector_math_008.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_008
    links.new(sample_u_v_surface_001.outputs[0], vector_math_008.inputs[0])
    links.new(vector_math_008.outputs[0], set_position_001.inputs[3])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_003.name = "Separate XYZ.003"
    separate_x_y_z_003.label = ""
    separate_x_y_z_003.location = (2287.0, -693.800048828125)
    separate_x_y_z_003.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_003
    links.new(map_range.outputs[1], separate_x_y_z_003.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (2467.0, -693.800048828125)
    math.bl_label = "Math"
    math.operation = "MULTIPLY"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.009999999776482582
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(separate_x_y_z_003.outputs[2], math.inputs[0])
    links.new(math.outputs[0], vector_math_008.inputs[3])

    frame_009 = nodes.new("NodeFrame")
    frame_009.name = "Frame.009"
    frame_009.label = "Broaches"
    frame_009.location = (29.0, -3391.000244140625)
    frame_009.bl_label = "Frame"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20
    # Links for frame_009

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.name = "Transform Geometry.007"
    transform_geometry_007.label = ""
    transform_geometry_007.location = (3007.0, -673.800048828125)
    transform_geometry_007.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_007.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_007.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_007.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_007.inputs[4].default_value = Vector((1.0, -1.0, 1.0))
    # Links for transform_geometry_007
    links.new(set_position_001.outputs[0], transform_geometry_007.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.name = "Flip Faces.001"
    flip_faces_001.label = ""
    flip_faces_001.location = (3187.0, -673.800048828125)
    flip_faces_001.bl_label = "Flip Faces"
    # Selection
    flip_faces_001.inputs[1].default_value = True
    # Links for flip_faces_001
    links.new(transform_geometry_007.outputs[0], flip_faces_001.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (3367.0, -593.800048828125)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(flip_faces_001.outputs[0], join_geometry_004.inputs[0])
    links.new(set_position_001.outputs[0], join_geometry_004.inputs[0])

    gem_in_holder_3 = nodes.new("GeometryNodeGroup")
    gem_in_holder_3.name = "Group.013"
    gem_in_holder_3.label = ""
    gem_in_holder_3.location = (29.0, -29.0)
    gem_in_holder_3.node_tree = create_gem_in__holder_group()
    gem_in_holder_3.bl_label = "Group"
    # Gem Radius
    gem_in_holder_3.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_3.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_3.inputs[2].default_value = True
    # Scale
    gem_in_holder_3.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_3.inputs[4].default_value = 20
    # Seed
    gem_in_holder_3.inputs[5].default_value = 15
    # Wings
    gem_in_holder_3.inputs[6].default_value = True
    # Array Count
    gem_in_holder_3.inputs[7].default_value = 5
    # Strand Count
    gem_in_holder_3.inputs[8].default_value = 10
    # Split
    gem_in_holder_3.inputs[9].default_value = 0.004999999888241291
    # Seed
    gem_in_holder_3.inputs[10].default_value = 23.56599998474121
    # Links for gem_in_holder_3

    transform_geometry_008 = nodes.new("GeometryNodeTransform")
    transform_geometry_008.name = "Transform Geometry.008"
    transform_geometry_008.label = ""
    transform_geometry_008.location = (269.0, -29.0)
    transform_geometry_008.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_008.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_008.inputs[2].default_value = Vector((0.009999999776482582, 0.0, 0.0))
    # Rotation
    transform_geometry_008.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_008.inputs[4].default_value = Vector((1.2000000476837158, 1.2000000476837158, 1.2000000476837158))
    # Links for transform_geometry_008
    links.new(gem_in_holder_3.outputs[0], transform_geometry_008.inputs[0])
    links.new(transform_geometry_008.outputs[0], join_geometry_003.inputs[0])

    frame_010 = nodes.new("NodeFrame")
    frame_010.name = "Frame.010"
    frame_010.label = ""
    frame_010.location = (629.0, -1169.0)
    frame_010.bl_label = "Frame"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20
    # Links for frame_010

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (229.166015625, -115.80029296875)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Links for switch_001

    join_geometry_019 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_019.name = "Join Geometry.019"
    join_geometry_019.label = ""
    join_geometry_019.location = (29.166015625, -195.80029296875)
    join_geometry_019.bl_label = "Join Geometry"
    # Links for join_geometry_019
    links.new(join_geometry_004.outputs[0], join_geometry_019.inputs[0])
    links.new(store_named_attribute_003.outputs[0], join_geometry_019.inputs[0])
    links.new(store_named_attribute.outputs[0], join_geometry_019.inputs[0])
    links.new(join_geometry_019.outputs[0], switch_001.inputs[2])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (84.3330078125, -35.80029296875)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch_001.inputs[0])

    frame_011 = nodes.new("NodeFrame")
    frame_011.name = "Frame.011"
    frame_011.label = "Decor"
    frame_011.location = (5791.6669921875, -2229.0)
    frame_011.bl_label = "Frame"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20
    # Links for frame_011

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.label = ""
    switch_002.location = (1929.0, -115.79998779296875)
    switch_002.bl_label = "Switch"
    switch_002.input_type = "GEOMETRY"
    # Links for switch_002
    links.new(switch_002.outputs[0], join_geometry_017.inputs[0])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (1929.0, -35.79998779296875)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[0], switch_002.inputs[0])

    join_geometry_020 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_020.name = "Join Geometry.020"
    join_geometry_020.label = ""
    join_geometry_020.location = (1729.0, -115.79998779296875)
    join_geometry_020.bl_label = "Join Geometry"
    # Links for join_geometry_020
    links.new(store_named_attribute_002.outputs[0], join_geometry_020.inputs[0])
    links.new(store_named_attribute_001.outputs[0], join_geometry_020.inputs[0])
    links.new(join_geometry_020.outputs[0], switch_002.inputs[2])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.name = "Separate Geometry.002"
    separate_geometry_002.label = ""
    separate_geometry_002.location = (738.0, -29.0)
    separate_geometry_002.bl_label = "Separate Geometry"
    separate_geometry_002.domain = "POINT"
    # Links for separate_geometry_002
    links.new(repeat_output.outputs[0], separate_geometry_002.inputs[0])

    compare_006 = nodes.new("FunctionNodeCompare")
    compare_006.name = "Compare.006"
    compare_006.label = ""
    compare_006.location = (418.0, -29.0)
    compare_006.bl_label = "Compare"
    compare_006.operation = "EQUAL"
    compare_006.data_type = "FLOAT"
    compare_006.mode = "ELEMENT"
    # B
    compare_006.inputs[1].default_value = 0.4000000059604645
    # A
    compare_006.inputs[2].default_value = 0
    # B
    compare_006.inputs[3].default_value = 0
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
    compare_006.inputs[12].default_value = 0.3009999990463257
    # Links for compare_006
    links.new(repeat_output.outputs[2], compare_006.inputs[0])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.label = ""
    named_attribute_001.location = (58.0, -209.0)
    named_attribute_001.bl_label = "Named Attribute"
    named_attribute_001.data_type = "FLOAT_VECTOR"
    # Name
    named_attribute_001.inputs[0].default_value = "UVMap"
    # Links for named_attribute_001

    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_004.name = "Separate XYZ.004"
    separate_x_y_z_004.label = ""
    separate_x_y_z_004.location = (238.0, -209.0)
    separate_x_y_z_004.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_004
    links.new(named_attribute_001.outputs[0], separate_x_y_z_004.inputs[0])

    compare_007 = nodes.new("FunctionNodeCompare")
    compare_007.name = "Compare.007"
    compare_007.label = ""
    compare_007.location = (418.0, -209.0)
    compare_007.bl_label = "Compare"
    compare_007.operation = "EQUAL"
    compare_007.data_type = "FLOAT"
    compare_007.mode = "ELEMENT"
    # B
    compare_007.inputs[1].default_value = 0.0
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
    compare_007.inputs[12].default_value = 0.5199999809265137
    # Links for compare_007
    links.new(separate_x_y_z_004.outputs[0], compare_007.inputs[0])

    boolean_math_006 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_006.name = "Boolean Math.006"
    boolean_math_006.label = ""
    boolean_math_006.location = (578.0, -29.0)
    boolean_math_006.bl_label = "Boolean Math"
    boolean_math_006.operation = "AND"
    # Links for boolean_math_006
    links.new(compare_006.outputs[0], boolean_math_006.inputs[0])
    links.new(compare_007.outputs[0], boolean_math_006.inputs[1])
    links.new(boolean_math_006.outputs[0], separate_geometry_002.inputs[1])

    frame_012 = nodes.new("NodeFrame")
    frame_012.name = "Frame.012"
    frame_012.label = ""
    frame_012.location = (98.0, -1035.80029296875)
    frame_012.bl_label = "Frame"
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20
    # Links for frame_012

    gem_in_holder_4 = nodes.new("GeometryNodeGroup")
    gem_in_holder_4.name = "Gem in Holder.001"
    gem_in_holder_4.label = ""
    gem_in_holder_4.location = (949.0, -75.80029296875)
    gem_in_holder_4.node_tree = create_gem_in__holder_group()
    gem_in_holder_4.bl_label = "Group"
    # Gem Radius
    gem_in_holder_4.inputs[0].default_value = 0.009999990463256836
    # Gem Material
    gem_in_holder_4.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_4.inputs[2].default_value = False
    # Scale
    gem_in_holder_4.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_4.inputs[4].default_value = 20
    # Seed
    gem_in_holder_4.inputs[5].default_value = 10
    # Wings
    gem_in_holder_4.inputs[6].default_value = False
    # Array Count
    gem_in_holder_4.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_4.inputs[8].default_value = 10
    # Links for gem_in_holder_4

    position_006 = nodes.new("GeometryNodeInputPosition")
    position_006.name = "Position.006"
    position_006.label = ""
    position_006.location = (409.0, -255.80029296875)
    position_006.bl_label = "Position"
    # Links for position_006

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.name = "For Each Geometry Element Input.001"
    for_each_geometry_element_input_001.label = ""
    for_each_geometry_element_input_001.location = (569.0, -55.80029296875)
    for_each_geometry_element_input_001.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input_001.inputs[1].default_value = True
    # Links for for_each_geometry_element_input_001
    links.new(position_006.outputs[0], for_each_geometry_element_input_001.inputs[2])

    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.name = "For Each Geometry Element Output.001"
    for_each_geometry_element_output_001.label = ""
    for_each_geometry_element_output_001.location = (2109.0, -75.80029296875)
    for_each_geometry_element_output_001.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    # Links for for_each_geometry_element_output_001
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_019.inputs[0])

    transform_geometry_009 = nodes.new("GeometryNodeTransform")
    transform_geometry_009.name = "Transform Geometry.009"
    transform_geometry_009.label = ""
    transform_geometry_009.location = (1209.0, -75.80029296875)
    transform_geometry_009.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_009.inputs[1].default_value = "Components"
    # Scale
    transform_geometry_009.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_009
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_009.inputs[2])
    links.new(gem_in_holder_4.outputs[4], transform_geometry_009.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.name = "Rotate Rotation.002"
    rotate_rotation_002.label = ""
    rotate_rotation_002.location = (569.0, -315.80029296875)
    rotate_rotation_002.bl_label = "Rotate Rotation"
    rotate_rotation_002.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, 0.0, -1.3229594230651855), 'XYZ')
    # Links for rotate_rotation_002
    links.new(rotate_rotation_002.outputs[0], transform_geometry_009.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[3], rotate_rotation_002.inputs[0])

    frame_016 = nodes.new("NodeFrame")
    frame_016.name = "Frame.016"
    frame_016.label = "Random Wings"
    frame_016.location = (1287.0, -1849.0)
    frame_016.bl_label = "Frame"
    frame_016.text = None
    frame_016.shrink = True
    frame_016.label_size = 20
    # Links for frame_016

    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.name = "Random Value.007"
    random_value_007.label = ""
    random_value_007.location = (769.0, -75.80029296875)
    random_value_007.bl_label = "Random Value"
    random_value_007.data_type = "FLOAT"
    # Min
    random_value_007.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_007.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_007.inputs[2].default_value = 6.0
    # Max
    random_value_007.inputs[3].default_value = 8.0
    # Min
    random_value_007.inputs[4].default_value = 0
    # Max
    random_value_007.inputs[5].default_value = 100
    # Probability
    random_value_007.inputs[6].default_value = 0.5
    # Seed
    random_value_007.inputs[8].default_value = 48
    # Links for random_value_007
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_4.inputs[10])

    random_value_008 = nodes.new("FunctionNodeRandomValue")
    random_value_008.name = "Random Value.008"
    random_value_008.label = ""
    random_value_008.location = (769.0, -255.80029296875)
    random_value_008.bl_label = "Random Value"
    random_value_008.data_type = "FLOAT"
    # Min
    random_value_008.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_008.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_008.inputs[2].default_value = 0.0
    # Max
    random_value_008.inputs[3].default_value = 0.003000000026077032
    # Min
    random_value_008.inputs[4].default_value = 0
    # Max
    random_value_008.inputs[5].default_value = 100
    # Probability
    random_value_008.inputs[6].default_value = 0.5
    # Seed
    random_value_008.inputs[8].default_value = 10
    # Links for random_value_008
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_008.inputs[7])
    links.new(random_value_008.outputs[1], gem_in_holder_4.inputs[9])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (1589.0, -75.80029296875)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Offset
    set_position_002.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_002

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.label = ""
    geometry_proximity_001.location = (1589.0, -255.80029296875)
    geometry_proximity_001.bl_label = "Geometry Proximity"
    geometry_proximity_001.target_element = "FACES"
    # Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0
    # Links for geometry_proximity_001
    links.new(geometry_proximity_001.outputs[0], set_position_002.inputs[2])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (1749.0, -75.80029296875)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002
    links.new(set_position_002.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(gem_in_holder_4.outputs[1], curve_to_mesh_002.inputs[1])
    links.new(gem_in_holder_4.outputs[2], curve_to_mesh_002.inputs[2])

    reroute_003 = nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.label = ""
    reroute_003.location = (716.0, -2084.80029296875)
    reroute_003.bl_label = "Reroute"
    reroute_003.socket_idname = "NodeSocketGeometry"
    # Links for reroute_003
    links.new(transform_geometry_002.outputs[0], reroute_003.inputs[0])
    links.new(reroute_003.outputs[0], geometry_proximity_001.inputs[0])

    reroute_012 = nodes.new("NodeReroute")
    reroute_012.name = "Reroute.012"
    reroute_012.label = ""
    reroute_012.location = (309.0, -75.80029296875)
    reroute_012.bl_label = "Reroute"
    reroute_012.socket_idname = "NodeSocketGeometry"
    # Links for reroute_012
    links.new(reroute_003.outputs[0], reroute_012.inputs[0])

    distribute_points_on_faces_001 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_001.name = "Distribute Points on Faces.001"
    distribute_points_on_faces_001.label = ""
    distribute_points_on_faces_001.location = (549.0, -35.80029296875)
    distribute_points_on_faces_001.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces_001.distribute_method = "POISSON"
    distribute_points_on_faces_001.use_legacy_normal = False
    # Distance Min
    distribute_points_on_faces_001.inputs[2].default_value = 0.009999999776482582
    # Density Max
    distribute_points_on_faces_001.inputs[3].default_value = 5000.0
    # Density
    distribute_points_on_faces_001.inputs[4].default_value = 500.0
    # Density Factor
    distribute_points_on_faces_001.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces_001.inputs[6].default_value = 0
    # Links for distribute_points_on_faces_001
    links.new(reroute_012.outputs[0], distribute_points_on_faces_001.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (29.0, -175.80029296875)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "POINTS"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity
    links.new(for_each_geometry_element_output_001.outputs[2], geometry_proximity.inputs[0])

    compare_008 = nodes.new("FunctionNodeCompare")
    compare_008.name = "Compare.008"
    compare_008.label = ""
    compare_008.location = (189.0, -175.80029296875)
    compare_008.bl_label = "Compare"
    compare_008.operation = "LESS_THAN"
    compare_008.data_type = "FLOAT"
    compare_008.mode = "ELEMENT"
    # B
    compare_008.inputs[1].default_value = 0.0020000000949949026
    # A
    compare_008.inputs[2].default_value = 0
    # B
    compare_008.inputs[3].default_value = 0
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
    links.new(geometry_proximity.outputs[1], compare_008.inputs[0])

    gem_in_holder_5 = nodes.new("GeometryNodeGroup")
    gem_in_holder_5.name = "Gem in Holder.002"
    gem_in_holder_5.label = ""
    gem_in_holder_5.location = (549.0, -455.80029296875)
    gem_in_holder_5.node_tree = create_gem_in__holder_group()
    gem_in_holder_5.bl_label = "Group"
    # Gem Radius
    gem_in_holder_5.inputs[0].default_value = 0.00800000037997961
    # Gem Material
    gem_in_holder_5.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_5.inputs[2].default_value = False
    # Scale
    gem_in_holder_5.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_5.inputs[4].default_value = 20
    # Seed
    gem_in_holder_5.inputs[5].default_value = 10
    # Wings
    gem_in_holder_5.inputs[6].default_value = False
    # Array Count
    gem_in_holder_5.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_5.inputs[8].default_value = 10
    # Split
    gem_in_holder_5.inputs[9].default_value = 0.0010000000474974513
    # Seed
    gem_in_holder_5.inputs[10].default_value = 6.6099958419799805
    # Links for gem_in_holder_5

    instance_on_points_004 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_004.name = "Instance on Points.004"
    instance_on_points_004.label = ""
    instance_on_points_004.location = (809.0, -75.80029296875)
    instance_on_points_004.bl_label = "Instance on Points"
    # Selection
    instance_on_points_004.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_004.inputs[3].default_value = False
    # Instance Index
    instance_on_points_004.inputs[4].default_value = 0
    # Links for instance_on_points_004
    links.new(distribute_points_on_faces_001.outputs[0], instance_on_points_004.inputs[0])
    links.new(distribute_points_on_faces_001.outputs[2], instance_on_points_004.inputs[5])

    random_value_010 = nodes.new("FunctionNodeRandomValue")
    random_value_010.name = "Random Value.010"
    random_value_010.label = ""
    random_value_010.location = (789.0, -275.80029296875)
    random_value_010.bl_label = "Random Value"
    random_value_010.data_type = "FLOAT"
    # Min
    random_value_010.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_010.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_010.inputs[2].default_value = 0.10000000894069672
    # Max
    random_value_010.inputs[3].default_value = 0.5
    # Min
    random_value_010.inputs[4].default_value = 0
    # Max
    random_value_010.inputs[5].default_value = 100
    # Probability
    random_value_010.inputs[6].default_value = 0.5
    # ID
    random_value_010.inputs[7].default_value = 0
    # Seed
    random_value_010.inputs[8].default_value = 0
    # Links for random_value_010
    links.new(random_value_010.outputs[1], instance_on_points_004.inputs[6])

    frame_017 = nodes.new("NodeFrame")
    frame_017.name = "Frame.017"
    frame_017.label = "Larger Jewels"
    frame_017.location = (3787.0, -2389.0)
    frame_017.bl_label = "Frame"
    frame_017.text = None
    frame_017.shrink = True
    frame_017.label_size = 20
    # Links for frame_017

    realize_instances_004 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_004.name = "Realize Instances.004"
    realize_instances_004.label = ""
    realize_instances_004.location = (1149.0, -75.80029296875)
    realize_instances_004.bl_label = "Realize Instances"
    # Selection
    realize_instances_004.inputs[1].default_value = True
    # Realize All
    realize_instances_004.inputs[2].default_value = True
    # Depth
    realize_instances_004.inputs[3].default_value = 0
    # Links for realize_instances_004

    transform_geometry_010 = nodes.new("GeometryNodeTransform")
    transform_geometry_010.name = "Transform Geometry.010"
    transform_geometry_010.label = ""
    transform_geometry_010.location = (789.0, -455.80029296875)
    transform_geometry_010.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_010.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_010.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    # Rotation
    transform_geometry_010.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_010.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_010
    links.new(transform_geometry_010.outputs[0], instance_on_points_004.inputs[2])
    links.new(gem_in_holder_5.outputs[0], transform_geometry_010.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.name = "Group.014"
    swap_attr.label = ""
    swap_attr.location = (1309.0, -75.80029296875)
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.bl_label = "Group"
    # Old
    swap_attr.inputs[2].default_value = "ruby"
    # New
    swap_attr.inputs[3].default_value = "saphire"
    # Links for swap_attr
    links.new(realize_instances_004.outputs[0], swap_attr.inputs[0])
    links.new(swap_attr.outputs[0], join_geometry_019.inputs[0])

    capture_attribute_008 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_008.name = "Capture Attribute.008"
    capture_attribute_008.label = ""
    capture_attribute_008.location = (989.0, -75.80029296875)
    capture_attribute_008.bl_label = "Capture Attribute"
    capture_attribute_008.active_index = 0
    capture_attribute_008.domain = "INSTANCE"
    # Links for capture_attribute_008
    links.new(capture_attribute_008.outputs[0], realize_instances_004.inputs[0])
    links.new(instance_on_points_004.outputs[0], capture_attribute_008.inputs[0])
    links.new(capture_attribute_008.outputs[1], swap_attr.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (949.0, -195.80029296875)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], capture_attribute_008.inputs[1])

    join_geometry_021 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_021.name = "Join Geometry.021"
    join_geometry_021.label = ""
    join_geometry_021.location = (13480.0, 0.0)
    join_geometry_021.bl_label = "Join Geometry"
    # Links for join_geometry_021
    links.new(join_geometry_021.outputs[0], rotate_on_centre.inputs[0])
    links.new(set_shade_smooth.outputs[0], join_geometry_021.inputs[0])
    links.new(switch_001.outputs[0], join_geometry_021.inputs[0])

    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.name = "Store Named Attribute.005"
    store_named_attribute_005.label = ""
    store_named_attribute_005.location = (1929.0, -75.80029296875)
    store_named_attribute_005.bl_label = "Store Named Attribute"
    store_named_attribute_005.data_type = "BOOLEAN"
    store_named_attribute_005.domain = "POINT"
    # Selection
    store_named_attribute_005.inputs[1].default_value = True
    # Name
    store_named_attribute_005.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_005.inputs[3].default_value = True
    # Links for store_named_attribute_005
    links.new(store_named_attribute_005.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute_005.inputs[0])

    distribute_points_on_faces_002 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_002.name = "Distribute Points on Faces.002"
    distribute_points_on_faces_002.label = ""
    distribute_points_on_faces_002.location = (29.0, -35.80029296875)
    distribute_points_on_faces_002.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces_002.distribute_method = "RANDOM"
    distribute_points_on_faces_002.use_legacy_normal = False
    # Selection
    distribute_points_on_faces_002.inputs[1].default_value = True
    # Distance Min
    distribute_points_on_faces_002.inputs[2].default_value = 0.0
    # Density Max
    distribute_points_on_faces_002.inputs[3].default_value = 10.0
    # Density
    distribute_points_on_faces_002.inputs[4].default_value = 8000.0
    # Density Factor
    distribute_points_on_faces_002.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces_002.inputs[6].default_value = 2
    # Links for distribute_points_on_faces_002
    links.new(distribute_points_on_faces_002.outputs[2], for_each_geometry_element_input_001.inputs[3])

    delete_geometry_003 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_003.name = "Delete Geometry.003"
    delete_geometry_003.label = ""
    delete_geometry_003.location = (269.0, -35.80029296875)
    delete_geometry_003.bl_label = "Delete Geometry"
    delete_geometry_003.mode = "ALL"
    delete_geometry_003.domain = "POINT"
    # Links for delete_geometry_003
    links.new(delete_geometry_003.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(distribute_points_on_faces_002.outputs[0], delete_geometry_003.inputs[0])

    geometry_proximity_002 = nodes.new("GeometryNodeProximity")
    geometry_proximity_002.name = "Geometry Proximity.002"
    geometry_proximity_002.label = ""
    geometry_proximity_002.location = (29.0, -315.80029296875)
    geometry_proximity_002.bl_label = "Geometry Proximity"
    geometry_proximity_002.target_element = "FACES"
    # Group ID
    geometry_proximity_002.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_002.inputs[3].default_value = 0
    # Links for geometry_proximity_002
    links.new(join_geometry_004.outputs[0], geometry_proximity_002.inputs[0])

    compare_009 = nodes.new("FunctionNodeCompare")
    compare_009.name = "Compare.009"
    compare_009.label = ""
    compare_009.location = (189.0, -315.80029296875)
    compare_009.bl_label = "Compare"
    compare_009.operation = "LESS_THAN"
    compare_009.data_type = "FLOAT"
    compare_009.mode = "ELEMENT"
    # B
    compare_009.inputs[1].default_value = 0.004999999888241291
    # A
    compare_009.inputs[2].default_value = 0
    # B
    compare_009.inputs[3].default_value = 0
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
    links.new(geometry_proximity_002.outputs[1], compare_009.inputs[0])
    links.new(compare_009.outputs[0], delete_geometry_003.inputs[1])

    delete_geometry_004 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_004.name = "Delete Geometry.004"
    delete_geometry_004.label = ""
    delete_geometry_004.location = (1389.0, -75.80029296875)
    delete_geometry_004.bl_label = "Delete Geometry"
    delete_geometry_004.mode = "ALL"
    delete_geometry_004.domain = "POINT"
    # Links for delete_geometry_004
    links.new(delete_geometry_004.outputs[0], set_position_002.inputs[0])
    links.new(transform_geometry_009.outputs[0], delete_geometry_004.inputs[0])

    geometry_proximity_003 = nodes.new("GeometryNodeProximity")
    geometry_proximity_003.name = "Geometry Proximity.003"
    geometry_proximity_003.label = ""
    geometry_proximity_003.location = (989.0, -515.80029296875)
    geometry_proximity_003.bl_label = "Geometry Proximity"
    geometry_proximity_003.target_element = "FACES"
    # Group ID
    geometry_proximity_003.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_003.inputs[3].default_value = 0
    # Links for geometry_proximity_003

    reroute_014 = nodes.new("NodeReroute")
    reroute_014.name = "Reroute.014"
    reroute_014.label = ""
    reroute_014.location = (1236.0, -2024.80029296875)
    reroute_014.bl_label = "Reroute"
    reroute_014.socket_idname = "NodeSocketGeometry"
    # Links for reroute_014
    links.new(reroute_014.outputs[0], distribute_points_on_faces_002.inputs[0])
    links.new(reroute_003.outputs[0], reroute_014.inputs[0])
    links.new(reroute_014.outputs[0], geometry_proximity_003.inputs[0])

    compare_010 = nodes.new("FunctionNodeCompare")
    compare_010.name = "Compare.010"
    compare_010.label = ""
    compare_010.location = (1149.0, -515.80029296875)
    compare_010.bl_label = "Compare"
    compare_010.operation = "GREATER_THAN"
    compare_010.data_type = "FLOAT"
    compare_010.mode = "ELEMENT"
    # B
    compare_010.inputs[1].default_value = 0.009999999776482582
    # A
    compare_010.inputs[2].default_value = 0
    # B
    compare_010.inputs[3].default_value = 0
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
    links.new(geometry_proximity_003.outputs[1], compare_010.inputs[0])
    links.new(compare_010.outputs[0], delete_geometry_004.inputs[1])

    separate_geometry_003 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_003.name = "Separate Geometry.003"
    separate_geometry_003.label = ""
    separate_geometry_003.location = (529.0, -35.80029296875)
    separate_geometry_003.bl_label = "Separate Geometry"
    separate_geometry_003.domain = "FACE"
    # Links for separate_geometry_003
    links.new(merge_by_distance_001.outputs[0], separate_geometry_003.inputs[0])

    separate_x_y_z_005 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_005.name = "Separate XYZ.005"
    separate_x_y_z_005.label = ""
    separate_x_y_z_005.location = (209.0, -35.80029296875)
    separate_x_y_z_005.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_005

    named_attribute_002 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.name = "Named Attribute.002"
    named_attribute_002.label = ""
    named_attribute_002.location = (29.0, -35.80029296875)
    named_attribute_002.bl_label = "Named Attribute"
    named_attribute_002.data_type = "FLOAT_VECTOR"
    # Name
    named_attribute_002.inputs[0].default_value = "UVMap"
    # Links for named_attribute_002
    links.new(named_attribute_002.outputs[0], separate_x_y_z_005.inputs[0])

    compare_011 = nodes.new("FunctionNodeCompare")
    compare_011.name = "Compare.011"
    compare_011.label = ""
    compare_011.location = (369.0, -35.80029296875)
    compare_011.bl_label = "Compare"
    compare_011.operation = "GREATER_THAN"
    compare_011.data_type = "FLOAT"
    compare_011.mode = "ELEMENT"
    # B
    compare_011.inputs[1].default_value = 0.8999999761581421
    # A
    compare_011.inputs[2].default_value = 0
    # B
    compare_011.inputs[3].default_value = 0
    # A
    compare_011.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_011.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_011.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_011.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_011.inputs[8].default_value = ""
    # B
    compare_011.inputs[9].default_value = ""
    # C
    compare_011.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_011.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_011.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_011
    links.new(separate_x_y_z_005.outputs[0], compare_011.inputs[0])
    links.new(compare_011.outputs[0], separate_geometry_003.inputs[1])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (1076.0, -1104.80029296875)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(separate_geometry_002.outputs[1], join_geometry_005.inputs[0])
    links.new(separate_geometry_003.outputs[0], join_geometry_005.inputs[0])

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.name = "Merge by Distance.002"
    merge_by_distance_002.label = ""
    merge_by_distance_002.location = (1256.0, -1084.80029296875)
    merge_by_distance_002.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance_002.inputs[1].default_value = True
    # Mode
    merge_by_distance_002.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_002
    links.new(merge_by_distance_002.outputs[0], gold_on_band.inputs[0])
    links.new(merge_by_distance_002.outputs[0], distribute_points_on_faces.inputs[0])
    links.new(join_geometry_005.outputs[0], merge_by_distance_002.inputs[0])

    frame_018 = nodes.new("NodeFrame")
    frame_018.name = "Frame.018"
    frame_018.label = "Curved"
    frame_018.location = (29.0, -393.19970703125)
    frame_018.bl_label = "Frame"
    frame_018.text = None
    frame_018.shrink = True
    frame_018.label_size = 20
    # Links for frame_018

    geometry_proximity_004 = nodes.new("GeometryNodeProximity")
    geometry_proximity_004.name = "Geometry Proximity.004"
    geometry_proximity_004.label = ""
    geometry_proximity_004.location = (29.0, -435.80029296875)
    geometry_proximity_004.bl_label = "Geometry Proximity"
    geometry_proximity_004.target_element = "POINTS"
    # Group ID
    geometry_proximity_004.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_004.inputs[3].default_value = 0
    # Links for geometry_proximity_004
    links.new(join_geometry_004.outputs[0], geometry_proximity_004.inputs[0])

    compare_012 = nodes.new("FunctionNodeCompare")
    compare_012.name = "Compare.012"
    compare_012.label = ""
    compare_012.location = (189.0, -435.80029296875)
    compare_012.bl_label = "Compare"
    compare_012.operation = "GREATER_THAN"
    compare_012.data_type = "FLOAT"
    compare_012.mode = "ELEMENT"
    # B
    compare_012.inputs[1].default_value = 0.003000000026077032
    # A
    compare_012.inputs[2].default_value = 0
    # B
    compare_012.inputs[3].default_value = 0
    # A
    compare_012.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_012.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_012.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_012.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_012.inputs[8].default_value = ""
    # B
    compare_012.inputs[9].default_value = ""
    # C
    compare_012.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_012.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_012.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_012
    links.new(geometry_proximity_004.outputs[1], compare_012.inputs[0])

    boolean_math_007 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_007.name = "Boolean Math.007"
    boolean_math_007.label = ""
    boolean_math_007.location = (349.0, -175.80029296875)
    boolean_math_007.bl_label = "Boolean Math"
    boolean_math_007.operation = "AND"
    # Links for boolean_math_007
    links.new(boolean_math_007.outputs[0], distribute_points_on_faces_001.inputs[1])
    links.new(compare_008.outputs[0], boolean_math_007.inputs[0])
    links.new(compare_012.outputs[0], boolean_math_007.inputs[1])

    auto_layout_nodes(group)
    return group
