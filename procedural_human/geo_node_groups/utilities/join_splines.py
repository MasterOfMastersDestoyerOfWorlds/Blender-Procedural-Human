
@geo_node_group
def create_join__splines_group():
    group_name = "Join Splines"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Curve", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (240.0, 80.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-720.0, 80.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (-400.0, 80.0)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "POINT"
    # Links for capture_attribute_001

    endpoint_selection_001 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_001.name = "Endpoint Selection.001"
    endpoint_selection_001.label = ""
    endpoint_selection_001.location = (-400.0, -40.0)
    endpoint_selection_001.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection_001.inputs[0].default_value = 1
    # End Size
    endpoint_selection_001.inputs[1].default_value = 1
    # Links for endpoint_selection_001
    links.new(endpoint_selection_001.outputs[0], capture_attribute_001.inputs[1])

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (-240.0, 80.0)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "EVALUATED"
    # Count
    curve_to_points.inputs[1].default_value = 10
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points
    links.new(capture_attribute_001.outputs[0], curve_to_points.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (-560.0, 80.0)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Evaluated"
    # Count
    resample_curve.inputs[3].default_value = 10
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve
    links.new(resample_curve.outputs[0], capture_attribute_001.inputs[0])
    links.new(group_input.outputs[0], resample_curve.inputs[0])

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.name = "Merge by Distance.002"
    merge_by_distance_002.label = ""
    merge_by_distance_002.location = (-80.0, 80.0)
    merge_by_distance_002.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_002.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_002
    links.new(curve_to_points.outputs[0], merge_by_distance_002.inputs[0])
    links.new(capture_attribute_001.outputs[1], merge_by_distance_002.inputs[1])

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    points_to_curves.label = ""
    points_to_curves.location = (80.0, 80.0)
    points_to_curves.bl_label = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0
    # Weight
    points_to_curves.inputs[2].default_value = 0.0
    # Links for points_to_curves
    links.new(merge_by_distance_002.outputs[0], points_to_curves.inputs[0])
    links.new(points_to_curves.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group