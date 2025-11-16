"""
Finger Geometry Nodes setup for Procedural Human Generator
"""

import bpy


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


def _create_finger_segment_node_group(name, seg_length, seg_radius, length_axis):
    """
    Create a reusable node group for a finger segment
    
    Args:
        name: Name for the node group
        seg_length: Length of the segment
        seg_radius: Radius of the segment
        length_axis: Axis along which the finger extends (0=X, 1=Y, 2=Z)
    
    Returns:
        Node group for the finger segment
    """
    # Create node group
    segment_group = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    _setup_node_group_interface(segment_group)
    
    # Input/Output nodes
    input_node = segment_group.nodes.new("NodeGroupInput")
    input_node.label = "Input"
    input_node.location = (-400, 0)
    
    output_node = segment_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (200, 0)
    
    # Create cylinder
    cylinder = segment_group.nodes.new("GeometryNodeMeshCylinder")
    cylinder.label = "Segment Cylinder"
    cylinder.location = (-200, 0)
    cylinder.inputs["Vertices"].default_value = 16
    cylinder.inputs["Radius"].default_value = seg_radius
    cylinder.inputs["Depth"].default_value = seg_length
    
    # Rotate cylinder to align with length axis
    rotation = [0.0, 0.0, 0.0]
    if length_axis == 1:  # Y-axis
        rotation[0] = 1.5708  # 90 degrees in radians
    elif length_axis == 0:  # X-axis
        rotation[1] = -1.5708  # -90 degrees in radians
    # If length_axis == 2 (Z-axis), no rotation needed
    
    transform = segment_group.nodes.new("GeometryNodeTransform")
    transform.label = "Align Segment"
    transform.location = (0, 0)
    transform.inputs["Rotation"].default_value = tuple(rotation)
    
    # Connect nodes
    segment_group.links.new(cylinder.outputs["Mesh"], transform.inputs["Geometry"])
    segment_group.links.new(transform.outputs["Geometry"], output_node.inputs["Geometry"])
    
    return segment_group


def _create_fingernail_node_group(name, nail_radius, curl_direction, distal_seg_radius):
    """
    Create a reusable node group for a fingernail
    
    Args:
        name: Name for the node group
        nail_radius: Radius of the nail
        curl_direction: Curl direction axis ("X", "Y", or "Z")
        distal_seg_radius: Radius of the distal segment (for positioning)
    
    Returns:
        Node group for the fingernail
    """
    # Create node group
    nail_group = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    _setup_node_group_interface(nail_group)
    
    # Input/Output nodes (expects distal segment geometry as input)
    input_node = nail_group.nodes.new("NodeGroupInput")
    input_node.label = "Distal Segment Input"
    input_node.location = (-800, 0)
    
    output_node = nail_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (1000, 0)
    
    # Get bounding box of distal segment
    bounding_box = nail_group.nodes.new("GeometryNodeBoundBox")
    bounding_box.label = "Distal Bounds"
    bounding_box.location = (-600, 0)
    
    separate_bbox_max = nail_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_bbox_max.label = "Get Max XYZ"
    separate_bbox_max.location = (-400, 0)
    
    # Create nail sphere
    nail_sphere = nail_group.nodes.new("GeometryNodeMeshUVSphere")
    nail_sphere.label = "Nail Sphere"
    nail_sphere.location = (-600, -300)
    nail_sphere.inputs["Radius"].default_value = nail_radius
    nail_sphere.inputs["Segments"].default_value = 16
    nail_sphere.inputs["Rings"].default_value = 8
    
    # Determine scale based on curl direction
    scale = [1.5, 1.0, 1.0]
    if curl_direction == "Y":
        scale = [1.5, 0.3, 1.0]  # X=wide, Y=thin (curl), Z=normal (length)
    elif curl_direction == "X":
        scale = [0.3, 1.5, 1.0]  # X=thin (curl), Y=wide, Z=normal (length)
    else:  # Z
        scale = [1.5, 1.0, 0.3]  # X=wide, Y=normal (length), Z=thin (curl)
    
    # Flatten nail
    flatten_nail = nail_group.nodes.new("GeometryNodeTransform")
    flatten_nail.label = "Flatten Nail"
    flatten_nail.location = (-400, -300)
    flatten_nail.inputs["Scale"].default_value = tuple(scale)
    flatten_nail.inputs["Rotation"].default_value = (0.0, 0.0, 0.0)
    
    # Calculate nail position (at tip of distal segment, centered, on opposite side of curl)
    # Determine axis mapping
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
    
    # Get max value for length axis (top of distal segment)
    length_max_output = separate_bbox_max.outputs["X"] if length_axis == 0 else (separate_bbox_max.outputs["Y"] if length_axis == 1 else separate_bbox_max.outputs["Z"])
    
    # Get max value for curl axis (opposite side of curl)
    curl_max_output = separate_bbox_max.outputs["X"] if curl_axis == 0 else (separate_bbox_max.outputs["Y"] if curl_axis == 1 else separate_bbox_max.outputs["Z"])
    
    # Add offset to curl axis to place nail on surface
    math_offset_curl = nail_group.nodes.new("ShaderNodeMath")
    math_offset_curl.label = "Offset to Surface"
    math_offset_curl.location = (-200, -100)
    math_offset_curl.operation = "ADD"
    math_offset_curl.inputs[1].default_value = distal_seg_radius * 0.1
    
    # Combine position (length at max, side at 0 center, curl at max + offset)
    combine_pos = nail_group.nodes.new("ShaderNodeCombineXYZ")
    combine_pos.label = "Nail Position"
    combine_pos.location = (0, -200)
    
    # Set axis values
    axis_inputs = {0: combine_pos.inputs["X"], 1: combine_pos.inputs["Y"], 2: combine_pos.inputs["Z"]}
    nail_group.links.new(length_max_output, axis_inputs[length_axis])
    axis_inputs[side_axis].default_value = 0.0  # Center on side axis
    nail_group.links.new(math_offset_curl.outputs["Value"], axis_inputs[curl_axis])
    
    # Position nail
    position_nail = nail_group.nodes.new("GeometryNodeTransform")
    position_nail.label = "Place on Distal"
    position_nail.location = (200, -300)
    
    # Join distal segment + nail
    join_nail = nail_group.nodes.new("GeometryNodeJoinGeometry")
    join_nail.label = "Join Distal + Nail"
    join_nail.location = (600, 0)
    
    # Connect nodes
    nail_group.links.new(input_node.outputs["Geometry"], bounding_box.inputs["Geometry"])
    nail_group.links.new(bounding_box.outputs["Max"], separate_bbox_max.inputs["Vector"])
    nail_group.links.new(curl_max_output, math_offset_curl.inputs[0])
    nail_group.links.new(nail_sphere.outputs["Mesh"], flatten_nail.inputs["Geometry"])
    nail_group.links.new(flatten_nail.outputs["Geometry"], position_nail.inputs["Geometry"])
    nail_group.links.new(combine_pos.outputs["Vector"], position_nail.inputs["Translation"])
    nail_group.links.new(input_node.outputs["Geometry"], join_nail.inputs["Geometry"])
    nail_group.links.new(position_nail.outputs["Geometry"], join_nail.inputs["Geometry"])
    nail_group.links.new(join_nail.outputs["Geometry"], output_node.inputs["Geometry"])
    
    return nail_group


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
    input_node.label = "Input"
    output_node = node_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"

    # Position nodes
    input_node.location = (-1000, 0)
    output_node.location = (1200, 0)

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

    # Calculate segment radii and create custom node groups
    segment_names = ["Proximal", "Middle", "Distal"]
    segment_node_instances = []
    cumulative_length = 0.0

    for seg_idx in range(num_segments):
        seg_length = segment_lengths[seg_idx]
        # Radius should be ~1/2 of segment length, with taper applied
        base_radius = seg_length * 0.5
        seg_radius = base_radius * (1.0 - seg_idx * taper_factor)
        
        # Get segment name
        if num_segments == 2:
            seg_name = "Proximal" if seg_idx == 0 else "Distal"
        else:
            seg_name = segment_names[seg_idx] if seg_idx < len(segment_names) else f"Segment {seg_idx}"
        
        # Create custom node group for this segment
        segment_group = _create_finger_segment_node_group(
            f"{seg_name}_Segment_Group",
            seg_length,
            seg_radius,
            length_axis
        )
        
        # Create instance of the custom node group
        segment_instance = node_group.nodes.new("GeometryNodeGroup")
        segment_instance.node_tree = segment_group
        segment_instance.label = f"{seg_name} Segment"
        segment_instance.location = (-800, 200 - seg_idx * 300)
        
        # Position the segment along the finger
        transform = node_group.nodes.new("GeometryNodeTransform")
        transform.label = f"Position {seg_name}"
        transform.location = (-600, 200 - seg_idx * 300)
        
        # Position along length axis - segments should be tip-to-tail
        translation = [0.0, 0.0, 0.0]
        translation[length_axis] = cumulative_length + seg_length / 2
        transform.inputs["Translation"].default_value = tuple(translation)
        
        # Connect segment instance to transform
        node_group.links.new(segment_instance.outputs["Geometry"], transform.inputs["Geometry"])
        
        segment_node_instances.append((seg_name, transform, seg_idx))
        cumulative_length += seg_length

    # Calculate distal segment radius for nail
    distal_seg_length = segment_lengths[-1]
    distal_seg_radius = (distal_seg_length * 0.5) * (1.0 - (num_segments - 1) * taper_factor)
    nail_radius = distal_seg_radius / 3.0
    
    # Create fingernail node group
    nail_group = _create_fingernail_node_group(
        "Fingernail_Group",
        nail_radius,
        curl_direction,
        distal_seg_radius
    )
    
    # Create instance of the fingernail node group
    # Apply it to the distal segment (last segment)
    nail_instance = node_group.nodes.new("GeometryNodeGroup")
    nail_instance.node_tree = nail_group
    nail_instance.label = "Add Fingernail to Distal"
    nail_instance.location = (-400, 200 - (num_segments - 1) * 300)
    
    # Connect distal segment output to nail node group
    distal_seg_name, distal_transform, distal_idx = segment_node_instances[-1]
    node_group.links.new(distal_transform.outputs["Geometry"], nail_instance.inputs["Geometry"])
    
    # Join ALL segments (proximal, middle, distal+nail) - THIS IS THE FINAL OPERATION
    join_all = node_group.nodes.new("GeometryNodeJoinGeometry")
    join_all.label = "Join All Finger Parts (FINAL)"
    join_all.location = (0, 0)
    
    # Connect all segment outputs to final join
    for idx, (seg_name, transform, seg_idx) in enumerate(segment_node_instances):
        if idx == len(segment_node_instances) - 1:
            # Last segment (distal) - use the nail instance output instead
            node_group.links.new(nail_instance.outputs["Geometry"], join_all.inputs["Geometry"])
        else:
            # Other segments (proximal, middle)
            node_group.links.new(transform.outputs["Geometry"], join_all.inputs["Geometry"])
    
    # Connect final join to output
    node_group.links.new(join_all.outputs["Geometry"], output_node.inputs["Geometry"])
    
    return node_group

