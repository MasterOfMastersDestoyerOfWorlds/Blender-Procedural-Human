import bpy
from procedural_human.hand.finger.finger_segment.finger_segment_properties import FingerSegmentProperties
from procedural_human.utils import setup_node_group_interface


def create_finger_segment_node_group(
    name,
    start_ratio,
    segment_ratio,
    seg_radius,
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
    segment_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    setup_node_group_interface(segment_group)

    # Additional input sockets for ratios and radius
    start_socket = segment_group.interface.new_socket(
        name=FingerSegmentProperties.START_RATIO.value, in_out="INPUT", socket_type="NodeSocketFloat"
    )
    start_socket.default_value = start_ratio

    ratio_socket = segment_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_RATIO.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    ratio_socket.default_value = segment_ratio

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
    input_node.location = (-600, 0)

    output_node = segment_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (500, 0)

    # Trim curve to isolate this segment
    trim_curve = segment_group.nodes.new("GeometryNodeTrimCurve")
    trim_curve.label = "Segment Span"
    trim_curve.location = (-200, 0)
    trim_curve.mode = "FACTOR"
    segment_group.links.new(input_node.outputs["Geometry"], trim_curve.inputs["Curve"])
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.START_RATIO.value], trim_curve.inputs["Start"]
    )

    end_math = segment_group.nodes.new("ShaderNodeMath")
    end_math.label = "End Ratio"
    end_math.location = (-350, -150)
    end_math.operation = "ADD"
    segment_group.links.new(input_node.outputs[FingerSegmentProperties.START_RATIO.value], end_math.inputs[0])
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RATIO.value],
        end_math.inputs[1],
    )
    segment_group.links.new(end_math.outputs["Value"], trim_curve.inputs["End"])

    # Profile circle for cylinder
    curve_circle = segment_group.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.label = "Segment Profile"
    curve_circle.location = (-200, -250)
    curve_circle.inputs["Resolution"].default_value = 16
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        curve_circle.inputs["Radius"],
    )

    # Convert trimmed curve to mesh using profile
    curve_to_mesh = segment_group.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.label = "Segment Mesh"
    curve_to_mesh.location = (200, 0)
    curve_to_mesh.inputs["Fill Caps"].default_value = True
    segment_group.links.new(trim_curve.outputs["Curve"], curve_to_mesh.inputs["Curve"])
    segment_group.links.new(
        curve_circle.outputs["Curve"], curve_to_mesh.inputs["Profile Curve"]
    )

    segment_group.links.new(
        curve_to_mesh.outputs["Mesh"], output_node.inputs["Geometry"]
    )
    segment_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        output_node.inputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
    )

    return segment_group
