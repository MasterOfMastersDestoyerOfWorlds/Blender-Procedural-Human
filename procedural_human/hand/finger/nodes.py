"""
Finger Geometry Nodes setup for Procedural Human Generator
"""


def _setup_node_group_interface(node_group):
    """Helper function to setup node group interface with geometry sockets"""
    # Check existing sockets
    existing_sockets = [socket.name for socket in node_group.interface.items_tree]
    
    # Add input geometry socket if it doesn't exist
    if "Geometry" not in existing_sockets:
        try:
            node_group.interface.new_socket(
                name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
            )
        except Exception as e:
            print(f"Warning: Could not create input Geometry socket: {e}")
    
    # Add output geometry socket if it doesn't exist
    existing_sockets = [socket.name for socket in node_group.interface.items_tree]
    if "Geometry" not in existing_sockets or existing_sockets.count("Geometry") < 2:
        try:
            node_group.interface.new_socket(
                name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
            )
        except Exception as e:
            print(f"Warning: Could not create output Geometry socket: {e}")


def create_fingernail_nodes(node_group, nail_size=0.003):
    """Create fingernail geometry on fingertip surface"""
    _setup_node_group_interface(node_group)

    # Input/Output nodes
    input_node = node_group.nodes.new("NodeGroupInput")
    output_node = node_group.nodes.new("NodeGroupOutput")

    # Position nodes
    input_node.location = (-600, 0)
    output_node.location = (600, 0)

    # Get position for selecting top surface
    position = node_group.nodes.new("GeometryNodeInputPosition")
    position.location = (-600, 200)

    # Separate XYZ to get Z component
    separate_xyz = node_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.location = (-400, 200)

    # Get bounding box to find top
    bounding_box = node_group.nodes.new("GeometryNodeBoundBox")
    bounding_box.location = (-400, 0)

    # Get max Z from bounding box
    separate_bbox = node_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_bbox.location = (-200, 0)

    # Compare to find top face
    compare = node_group.nodes.new("FunctionNodeCompare")
    compare.location = (-200, 200)
    compare.operation = "GREATER_THAN"
    compare.inputs["Epsilon"].default_value = 0.001

    # Create nail geometry - flattened sphere
    nail_sphere = node_group.nodes.new("GeometryNodeMeshUVSphere")
    nail_sphere.location = (-200, -200)
    nail_sphere.inputs["Radius"].default_value = nail_size
    nail_sphere.inputs["Segments"].default_value = 16
    nail_sphere.inputs["Rings"].default_value = 8

    # Transform nail to top surface
    transform = node_group.nodes.new("GeometryNodeTransform")
    transform.location = (0, -200)
    transform.inputs["Scale"].default_value = (1.5, 1.0, 0.3)  # Flatten nail shape

    # Use geometry proximity to position nail on surface
    proximity = node_group.nodes.new("GeometryNodeProximity")
    proximity.location = (0, 0)
    proximity.target_element = "FACES"

    # Set position to move nail to surface
    set_position = node_group.nodes.new("GeometryNodeSetPosition")
    set_position.location = (200, -200)

    # Join nail with finger segment
    join = node_group.nodes.new("GeometryNodeJoinGeometry")
    join.location = (400, 0)

    # Connect nodes
    node_group.links.new(input_node.outputs["Geometry"], bounding_box.inputs["Geometry"])
    node_group.links.new(bounding_box.outputs["Bounding Box"], separate_bbox.inputs["Vector"])
    node_group.links.new(position.outputs["Position"], separate_xyz.inputs["Vector"])
    node_group.links.new(separate_xyz.outputs["Z"], compare.inputs[0])
    node_group.links.new(separate_bbox.outputs["Z"], compare.inputs[1])

    # Position nail on top
    node_group.links.new(input_node.outputs["Geometry"], proximity.inputs["Target"])
    node_group.links.new(transform.outputs["Geometry"], set_position.inputs["Geometry"])
    node_group.links.new(proximity.outputs["Position"], set_position.inputs["Position"])

    # Join everything
    node_group.links.new(nail_sphere.outputs["Mesh"], transform.inputs["Geometry"])
    node_group.links.new(input_node.outputs["Geometry"], join.inputs["Geometry"])
    node_group.links.new(set_position.outputs["Geometry"], join.inputs["Geometry"])
    node_group.links.new(join.outputs["Geometry"], output_node.inputs["Geometry"])

    return node_group


def create_finger_nodes(
    node_group,
    num_segments=3,
    segment_lengths=None,
    radius=0.007,
    nail_size=0.003,
    taper_factor=0.15,
    curl_direction="Y",
):
    """
    Create complete finger geometry with variable segments and fingernail
    
    Args:
        node_group: Geometry node group to populate
        num_segments: Number of segments (2 or 3)
        segment_lengths: List of segment lengths in blender units
        radius: Base finger radius
        nail_size: Fingernail size
        taper_factor: How much radius decreases per segment
        curl_direction: Curl direction axis ("X", "Y", or "Z")
    """
    _setup_node_group_interface(node_group)

    # Input/Output nodes
    input_node = node_group.nodes.new("NodeGroupInput")
    output_node = node_group.nodes.new("NodeGroupOutput")

    # Position nodes
    input_node.location = (-1000, 0)
    output_node.location = (2000, 0)

    # Determine axis mapping based on curl direction
    # Default: Z is up (finger length), Y is curl direction (forward/back)
    if curl_direction == "X":
        length_axis = 2  # Z
        curl_axis = 0  # X
        side_axis = 1  # Y
    elif curl_direction == "Y":
        length_axis = 2  # Z
        curl_axis = 1  # Y
        side_axis = 0  # X
    else:  # Z
        length_axis = 1  # Y
        curl_axis = 2  # Z
        side_axis = 0  # X

    # Calculate segment lengths if not provided
    if segment_lengths is None:
        total_length = 1.0
        segment_lengths = [total_length / num_segments] * num_segments
    else:
        total_length = sum(segment_lengths)

    # Create segments dynamically
    segment_outputs = []
    cumulative_length = 0.0

    for seg_idx in range(num_segments):
        seg_length = segment_lengths[seg_idx]
        seg_radius = radius * (1.0 - seg_idx * taper_factor)
        
        # Create cylinder for segment
        cylinder = node_group.nodes.new("GeometryNodeMeshCylinder")
        cylinder.location = (-800, 200 - seg_idx * 200)
        cylinder.inputs["Vertices"].default_value = 16
        cylinder.inputs["Radius"].default_value = seg_radius
        cylinder.inputs["Depth"].default_value = seg_length

        # Transform to position segment
        transform = node_group.nodes.new("GeometryNodeTransform")
        transform.location = (-600, 200 - seg_idx * 200)
        
        # Position along length axis (Z by default)
        translation = [0.0, 0.0, 0.0]
        translation[length_axis] = cumulative_length + seg_length / 2
        transform.inputs["Translation"].default_value = tuple(translation)

        segment_outputs.append(transform.outputs["Geometry"])
        node_group.links.new(cylinder.outputs["Mesh"], transform.inputs["Geometry"])
        
        cumulative_length += seg_length

    # Join all segments
    join_segments = node_group.nodes.new("GeometryNodeJoinGeometry")
    join_segments.location = (-400, 0)

    for seg_output in segment_outputs:
        node_group.links.new(seg_output, join_segments.inputs["Geometry"])
    
    # For now, connect segments directly to output to test
    # We'll add nail later once basic geometry works
    test_output = join_segments.outputs["Geometry"]

    # Get distal segment (last segment) for nail placement
    # Use bounding box to find top of finger
    bounding_box = node_group.nodes.new("GeometryNodeBoundBox")
    bounding_box.location = (-200, 0)

    separate_bbox_max = node_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_bbox_max.location = (0, 0)
    
    separate_bbox_min = node_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_bbox_min.location = (0, -200)

    # Create nail geometry - flattened sphere
    nail_sphere = node_group.nodes.new("GeometryNodeMeshUVSphere")
    nail_sphere.location = (200, 0)
    nail_sphere.inputs["Radius"].default_value = nail_size
    nail_sphere.inputs["Segments"].default_value = 16
    nail_sphere.inputs["Rings"].default_value = 8

    # Transform nail - flatten it and position on side of distal segment
    transform_nail = node_group.nodes.new("GeometryNodeTransform")
    transform_nail.location = (400, 0)
    transform_nail.inputs["Scale"].default_value = (1.5, 1.0, 0.3)  # Flatten nail
    
    # Calculate nail position: center on length axis, negative curl axis
    # Get center of finger bounding box
    math_add_length = node_group.nodes.new("ShaderNodeMath")
    math_add_length.location = (200, -200)
    math_add_length.operation = "ADD"
    
    math_multiply_length = node_group.nodes.new("ShaderNodeMath")
    math_multiply_length.location = (400, -200)
    math_multiply_length.operation = "MULTIPLY"
    math_multiply_length.inputs[1].default_value = 0.5
    
    # Get negative curl axis value
    math_negate_curl = node_group.nodes.new("ShaderNodeMath")
    math_negate_curl.location = (400, -400)
    math_negate_curl.operation = "MULTIPLY"
    math_negate_curl.inputs[1].default_value = -1.0
    
    # Combine nail position
    combine_nail_pos = node_group.nodes.new("ShaderNodeCombineXYZ")
    combine_nail_pos.location = (600, -200)
    
    # Position nail transform
    transform_nail_pos = node_group.nodes.new("GeometryNodeTransform")
    transform_nail_pos.location = (800, 0)

    # Join nail with finger segments
    join_all = node_group.nodes.new("GeometryNodeJoinGeometry")
    join_all.location = (1800, 0)

    # Connect nodes - segments and bounding box
    node_group.links.new(join_segments.outputs["Geometry"], bounding_box.inputs["Geometry"])
    node_group.links.new(bounding_box.outputs["Max"], separate_bbox_max.inputs["Vector"])
    node_group.links.new(bounding_box.outputs["Min"], separate_bbox_min.inputs["Vector"])
    
    # Calculate nail position
    # Get length axis center (for positioning nail along finger)
    length_max = separate_bbox_max.outputs["X"] if length_axis == 0 else (separate_bbox_max.outputs["Y"] if length_axis == 1 else separate_bbox_max.outputs["Z"])
    length_min = separate_bbox_min.outputs["X"] if length_axis == 0 else (separate_bbox_min.outputs["Y"] if length_axis == 1 else separate_bbox_min.outputs["Z"])
    
    node_group.links.new(length_max, math_add_length.inputs[0])
    node_group.links.new(length_min, math_add_length.inputs[1])
    node_group.links.new(math_add_length.outputs["Value"], math_multiply_length.inputs[0])
    
    # Get curl axis for negative positioning
    curl_max = separate_bbox_max.outputs["X"] if curl_axis == 0 else (separate_bbox_max.outputs["Y"] if curl_axis == 1 else separate_bbox_max.outputs["Z"])
    node_group.links.new(curl_max, math_negate_curl.inputs[0])
    
    # Combine nail position - set each axis appropriately
    # Side axis: center (0)
    # Length axis: center of finger (from bounding box)
    # Curl axis: negative side (opposite curl direction)
    axis_inputs = {
        0: combine_nail_pos.inputs["X"],
        1: combine_nail_pos.inputs["Y"],
        2: combine_nail_pos.inputs["Z"]
    }
    
    # Set side axis to 0 (center)
    axis_inputs[side_axis].default_value = 0.0
    
    # Connect length axis to center calculation
    node_group.links.new(math_multiply_length.outputs["Value"], axis_inputs[length_axis])
    
    # Connect curl axis to negative value
    node_group.links.new(math_negate_curl.outputs["Value"], axis_inputs[curl_axis])

    # Connect nail
    node_group.links.new(nail_sphere.outputs["Mesh"], transform_nail.inputs["Geometry"])
    node_group.links.new(transform_nail.outputs["Geometry"], transform_nail_pos.inputs["Geometry"])
    node_group.links.new(combine_nail_pos.outputs["Vector"], transform_nail_pos.inputs["Translation"])

    # Join everything - segments and nail
    node_group.links.new(join_segments.outputs["Geometry"], join_all.inputs["Geometry"])
    node_group.links.new(transform_nail_pos.outputs["Geometry"], join_all.inputs["Geometry"])
    
    # Ensure output is connected
    # The output node should have a Geometry input from the interface setup
    try:
        node_group.links.new(join_all.outputs["Geometry"], output_node.inputs["Geometry"])
    except KeyError:
        # If Geometry socket doesn't exist, check what sockets are available
        available_inputs = [inp.name for inp in output_node.inputs]
        print(f"Available output node inputs: {available_inputs}")
        raise RuntimeError(f"Output node does not have 'Geometry' socket. Available: {available_inputs}")

    return node_group

