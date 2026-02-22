import bpy
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group

@geo_node_group
def create_join__splines_group():
    group_name = "Join Splines"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Curve", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.capture_items.new("BOOLEAN", "Value")
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "POINT"

    endpoint_selection_001 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_001.inputs[0].default_value = 1
    endpoint_selection_001.inputs[1].default_value = 1
    links.new(endpoint_selection_001.outputs[0], capture_attribute_001.inputs[1])

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.mode = "EVALUATED"
    curve_to_points.inputs[1].default_value = 10
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    links.new(capture_attribute_001.outputs[0], curve_to_points.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Evaluated"
    resample_curve.inputs[3].default_value = 10
    resample_curve.inputs[4].default_value = 0.10000000149011612
    links.new(resample_curve.outputs[0], capture_attribute_001.inputs[0])
    links.new(group_input.outputs[0], resample_curve.inputs[0])

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.inputs[2].default_value = "All"
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    links.new(curve_to_points.outputs[0], merge_by_distance_002.inputs[0])
    links.new(capture_attribute_001.outputs[1], merge_by_distance_002.inputs[1])

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.inputs[1].default_value = 0
    points_to_curves.inputs[2].default_value = 0.0
    links.new(merge_by_distance_002.outputs[0], points_to_curves.inputs[0])
    links.new(points_to_curves.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group