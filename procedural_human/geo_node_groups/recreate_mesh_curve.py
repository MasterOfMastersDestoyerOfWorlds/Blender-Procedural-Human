import bpy
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import (
    get_attr, create_node, vec_math_op, link_or_set, get_or_rebuild_node_group
)


@geo_node_group
def create_recreate_curves_from_mesh_group():
    group_name = "RecreateCurvesFromMesh"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links

    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    # Get handle attributes and combine into vectors
    start_x = get_attr(group, "FLOAT", "handle_start_x")
    start_y = get_attr(group, "FLOAT", "handle_start_y")
    start_z = get_attr(group, "FLOAT", "handle_start_z")

    combine_start_offset = nodes.new("ShaderNodeCombineXYZ")
    links.new(start_x, combine_start_offset.inputs[0])
    links.new(start_y, combine_start_offset.inputs[1])
    links.new(start_z, combine_start_offset.inputs[2])

    end_x = get_attr(group, "FLOAT", "handle_end_x")
    end_y = get_attr(group, "FLOAT", "handle_end_y")
    end_z = get_attr(group, "FLOAT", "handle_end_z")

    combine_end_offset = nodes.new("ShaderNodeCombineXYZ")
    links.new(end_x, combine_end_offset.inputs[0])
    links.new(end_y, combine_end_offset.inputs[1])
    links.new(end_z, combine_end_offset.inputs[2])

    # For each edge, create a bezier curve
    for_each_input = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_input.inputs[1].default_value = True
    links.new(group_input.outputs[0], for_each_input.inputs[0])

    for_each_output = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_output.domain = "EDGE"
    for_each_output.inspection_index = 0
    for_each_input.pair_with_output(for_each_output)

    # Get edge vertex positions
    edge_vertices = nodes.new("GeometryNodeInputMeshEdgeVertices")

    # Sample position at vertex 1 (start)
    sample_pos_start = create_node(group, "GeometryNodeSampleIndex", {
        "Geometry": for_each_input.outputs[1],
        "Domain": "EDGE",
        "Data Type": "FLOAT_VECTOR",
        "Value": edge_vertices.outputs[2],  # Position 1
        "Index": 0
    })

    # Sample position at vertex 2 (end)
    sample_pos_end = create_node(group, "GeometryNodeSampleIndex", {
        "Geometry": for_each_input.outputs[1],
        "Domain": "EDGE",
        "Data Type": "FLOAT_VECTOR",
        "Value": edge_vertices.outputs[3],  # Position 2
        "Index": 0
    })

    # Create curve line from start to end
    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.mode = "POINTS"
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    curve_line.inputs[3].default_value = 1.0
    links.new(sample_pos_start.outputs[0], curve_line.inputs[0])
    links.new(sample_pos_end.outputs[0], curve_line.inputs[1])

    # Sample handle offsets
    sample_start_offset = create_node(group, "GeometryNodeSampleIndex", {
        "Geometry": for_each_input.outputs[1],
        "Domain": "EDGE",
        "Data Type": "FLOAT_VECTOR",
        "Value": combine_start_offset.outputs[0],
        "Index": 0
    })

    sample_end_offset = create_node(group, "GeometryNodeSampleIndex", {
        "Geometry": for_each_input.outputs[1],
        "Domain": "EDGE",
        "Data Type": "FLOAT_VECTOR",
        "Value": combine_end_offset.outputs[0],
        "Index": 0
    })

    # Set spline type to Bezier
    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.spline_type = "BEZIER"
    set_spline_type.inputs[1].default_value = True
    links.new(curve_line.outputs[0], set_spline_type.inputs[0])

    # Set handle type to Free
    set_handle_type = nodes.new("GeometryNodeCurveSetHandles")
    set_handle_type.handle_type = "FREE"
    set_handle_type.mode = {'LEFT', 'RIGHT'}
    set_handle_type.inputs[1].default_value = True
    links.new(set_spline_type.outputs[0], set_handle_type.inputs[0])

    # Endpoint selections
    endpoint_start = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_start.inputs[0].default_value = 1  # Start count
    endpoint_start.inputs[1].default_value = 0  # End count

    endpoint_end = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_end.inputs[0].default_value = 0  # Start count
    endpoint_end.inputs[1].default_value = 1  # End count

    # Calculate handle positions (position + offset)
    handle_pos_start = vec_math_op(group, "ADD", sample_pos_start.outputs[0], sample_start_offset.outputs[0])
    handle_pos_end = vec_math_op(group, "ADD", sample_pos_end.outputs[0], sample_end_offset.outputs[0])

    # Set handle positions for start point (right handle)
    set_handle_pos_right = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_pos_right.mode = "RIGHT"
    set_handle_pos_right.inputs[3].default_value = (0.0, 0.0, 0.0)
    links.new(set_handle_type.outputs[0], set_handle_pos_right.inputs[0])
    links.new(endpoint_start.outputs[0], set_handle_pos_right.inputs[1])
    links.new(handle_pos_start, set_handle_pos_right.inputs[2])

    # Set handle positions for end point (left handle)
    set_handle_pos_left = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_pos_left.mode = "LEFT"
    set_handle_pos_left.inputs[3].default_value = (0.0, 0.0, 0.0)
    links.new(set_handle_pos_right.outputs[0], set_handle_pos_left.inputs[0])
    links.new(endpoint_end.outputs[0], set_handle_pos_left.inputs[1])
    links.new(handle_pos_end, set_handle_pos_left.inputs[2])

    # Connect to for-each output
    links.new(set_handle_pos_left.outputs[0], for_each_output.inputs[1])

    # Convert curves to mesh
    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.inputs[2].default_value = 1.0
    curve_to_mesh.inputs[3].default_value = False
    links.new(for_each_output.outputs[2], curve_to_mesh.inputs[0])
    links.new(curve_to_mesh.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
