"""
Finger Geometry Nodes setup for Procedural Human Generator
"""

import bpy
from procedural_human.hand.finger_segment.finger_types import (
    FingerType,
    ensure_finger_type,
)
from procedural_human.hand.finger_segment.finger_nail.finger_nail_nodes import (
    attach_fingernail_to_distal_segment,
)
from procedural_human.utils import setup_node_group_interface





def _create_finger_segment_node_group(
    name,
    seg_length,
    seg_radius,
    length_axis,
    segment_ratio,
):
    """
    Create a reusable node group for a finger segment
    
    Args:
        name: Name for the node group
        seg_length: Length of the segment
        seg_radius: Radius of the segment
        length_axis: Axis along which the finger extends (0=X, 1=Y, 2=Z)
        segment_ratio: Fraction of total finger length represented by this segment
    
    Returns:
        Node group for the finger segment
    """
    # Create node group
    segment_group = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    setup_node_group_interface(segment_group)
    
    # Create exposed sockets for proportions
    length_socket = segment_group.interface.new_socket(
        name="Segment Length", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    length_socket.default_value = seg_length

    radius_socket = segment_group.interface.new_socket(
        name="Segment Radius", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    radius_socket.default_value = seg_radius

    ratio_socket = segment_group.interface.new_socket(
        name="Segment Ratio", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    ratio_socket.default_value = segment_ratio

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
    segment_group.links.new(
        input_node.outputs["Segment Radius"], cylinder.inputs["Radius"]
    )
    segment_group.links.new(
        input_node.outputs["Segment Length"], cylinder.inputs["Depth"]
    )
    
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
    segment_group.links.new(
        transform.outputs["Geometry"], output_node.inputs["Geometry"]
    )
    
    return segment_group




def create_finger_nodes(
    node_group,
    num_segments=3,
    segment_lengths=None,
    radius=0.007,
    nail_size=0.003,
    taper_factor=0.15,
    curl_direction="Y",
    finger_type=FingerType.INDEX,
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
    setup_node_group_interface(node_group)
    finger_type = ensure_finger_type(finger_type)

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
        segment_ratio = (seg_length / total_length) if total_length > 0 else 0.0
        
        # Get segment name
        if num_segments == 2:
            seg_name = "Proximal" if seg_idx == 0 else "Distal"
        else:
            seg_name = segment_names[seg_idx] if seg_idx < len(segment_names) else f"Segment {seg_idx}"
        
        # Create custom node group for this segment
        segment_group = _create_finger_segment_node_group(
            f"{finger_type.value}_{seg_name}_Segment_Group",
            seg_length,
            seg_radius,
            length_axis,
            segment_ratio,
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

    # Attach fingernail to distal segment via helper in the fingernail module
    distal_seg_name, distal_transform, distal_idx = segment_node_instances[-1]
    distal_seg_length = segment_lengths[-1]
    nail_instance = attach_fingernail_to_distal_segment(
        node_group=node_group,
        distal_transform_node=distal_transform,
        curl_direction=curl_direction,
        distal_seg_length=distal_seg_length,
        num_segments=num_segments,
        taper_factor=taper_factor,
        finger_type=finger_type,
        nail_size=nail_size,
    )
    
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

