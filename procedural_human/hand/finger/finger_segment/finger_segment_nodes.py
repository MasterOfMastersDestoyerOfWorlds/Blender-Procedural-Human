import bpy
from procedural_human.hand.finger.finger_segment.finger_segment_properties import FingerSegmentProperties
from procedural_human.utils import setup_node_group_interface


def create_finger_segment_node_group(
    name,
    segment_length,
    seg_radius,
):
    """
    Create a reusable node group for a finger segment that extends from input geometry
    
    Each segment:
    - Takes input geometry (previous segment or starting axis)
    - Extracts the endpoint position
    - Creates a new curve extending from that point by segment_length
    - Converts to mesh and joins with input
    
    Args:
        name: Name for the node group
        segment_length: Length of the segment in Blender units
        seg_radius: Radius of the segment
        
    Returns:
        Node group for the finger segment
    """
    # Create node group
    segment_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    setup_node_group_interface(segment_group)
    
    # Additional input sockets for length and radius
    length_socket = segment_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_LENGTH.value, in_out="INPUT", socket_type="NodeSocketFloat"
    )
    length_socket.default_value = segment_length
    
    radius_socket = segment_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_RADIUS.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    radius_socket.default_value = seg_radius
    
    radius_output = segment_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_RADIUS.value,
        in_out="OUTPUT",
        socket_type="NodeSocketFloat",
    )
    
    # Input/Output nodes
    input_node = segment_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"
    input_node.location = (-800, 0)
    
    output_node = segment_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (800, 0)
    
    # Get bounding box of input geometry to find endpoint
    bbox_node = segment_group.nodes.new("GeometryNodeBoundBox")
    bbox_node.label = "Find Endpoint"
    bbox_node.location = (-600, 200)
    segment_group.links.new(input_node.outputs["Geometry"], bbox_node.inputs["Geometry"])
    
    # Extract max Z coordinate (endpoint)
    separate_xyz = segment_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.label = "Extract Z"
    separate_xyz.location = (-400, 200)
    segment_group.links.new(bbox_node.outputs["Max"], separate_xyz.inputs["Vector"])
    
    # Create end point for new segment: start at endpoint Z, extend by segment_length
    add_length = segment_group.nodes.new("ShaderNodeMath")
    add_length.label = "End Z = Start Z + Length"
    add_length.location = (-200, 200)
    add_length.operation = "ADD"
    segment_group.links.new(separate_xyz.outputs["Z"], add_length.inputs[0])
    segment_group.links.new(input_node.outputs[FingerSegmentProperties.SEGMENT_LENGTH.value], add_length.inputs[1])
    
    # Combine XYZ for end point (X=0, Y=0, Z=start_z + length)
    combine_end = segment_group.nodes.new("ShaderNodeCombineXYZ")
    combine_end.label = "End Point"
    combine_end.location = (0, 200)
    combine_end.inputs["X"].default_value = 0.0
    combine_end.inputs["Y"].default_value = 0.0
    segment_group.links.new(add_length.outputs["Value"], combine_end.inputs["Z"])
    
    # Combine XYZ for start point (X=0, Y=0, Z=previous_end_z)
    combine_start = segment_group.nodes.new("ShaderNodeCombineXYZ")
    combine_start.label = "Start Point"
    combine_start.location = (0, 0)
    combine_start.inputs["X"].default_value = 0.0
    combine_start.inputs["Y"].default_value = 0.0
    segment_group.links.new(separate_xyz.outputs["Z"], combine_start.inputs["Z"])
    
    # Create line curve for this segment
    line_curve = segment_group.nodes.new("GeometryNodeCurvePrimitiveLine")
    line_curve.label = "Segment Curve"
    line_curve.location = (200, 100)
    segment_group.links.new(combine_start.outputs["Vector"], line_curve.inputs["Start"])
    segment_group.links.new(combine_end.outputs["Vector"], line_curve.inputs["End"])
    
    # Profile circle for cylinder
    curve_circle = segment_group.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.label = "Segment Profile"
    curve_circle.location = (200, -100)
    curve_circle.inputs["Resolution"].default_value = 16
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        curve_circle.inputs["Radius"],
    )
    
    # Convert curve to mesh using profile
    curve_to_mesh = segment_group.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.label = "Segment Mesh"
    curve_to_mesh.location = (400, 100)
    curve_to_mesh.inputs["Fill Caps"].default_value = True
    segment_group.links.new(line_curve.outputs["Curve"], curve_to_mesh.inputs["Curve"])
    segment_group.links.new(
        curve_circle.outputs["Curve"], curve_to_mesh.inputs["Profile Curve"]
    )
    
    # Join with input geometry (previous segments)
    join_geo = segment_group.nodes.new("GeometryNodeJoinGeometry")
    join_geo.label = "Join With Previous"
    join_geo.location = (600, 0)
    segment_group.links.new(input_node.outputs["Geometry"], join_geo.inputs["Geometry"])
    segment_group.links.new(curve_to_mesh.outputs["Mesh"], join_geo.inputs["Geometry"])
    
    # Output
    segment_group.links.new(
        join_geo.outputs["Geometry"], output_node.inputs["Geometry"]
    )
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        output_node.inputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
    )
    
    return segment_group
