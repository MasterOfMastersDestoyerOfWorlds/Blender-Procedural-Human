import bpy
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)


def create_float_curve_profile_node_group(
    axis_name,
    parent_input_node,
    parent_node_group,
    length_clamp_node,
    angle_param_node,
    segment_length,
    segment_type,
):
    """
    Creates a node group that uses a Float Curve to define the profile offset.
    Replaces the geometry-based profile lookup.
    """

    group_name = f"{axis_name} Float Curve Profile"

    # Create new node group
    profile_group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    profile_group.interface.new_socket(
        name="Length Clamp", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    profile_group.interface.new_socket(
        name="Sin Theta", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    profile_group.interface.new_socket(
        name=FingerSegmentProperties.SEGMENT_RADIUS.value,
        in_out="INPUT",
        socket_type="NodeSocketFloat",
    )
    # Kept for compatibility, but essentially unused logic-wise
    profile_group.interface.new_socket(
        name="Y Profile", in_out="INPUT", socket_type="NodeSocketGeometry"
    )

    profile_group.interface.new_socket(
        name="Offset", in_out="OUTPUT", socket_type="NodeSocketFloat"
    )
    profile_group.interface.new_socket(
        name="Point Count", in_out="OUTPUT", socket_type="NodeSocketInt"
    )
    profile_group.interface.new_socket(
        name="Y Profile", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )

    # --- Nodes ---
    input_node = profile_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"
    input_node.location = (-800, 0)

    # Float Curve Node
    float_curve = profile_group.nodes.new("ShaderNodeFloatCurve")
    float_curve.label = f"{axis_name} Profile Shape"
    float_curve.location = (-400, 0)
    
    # By default, ShaderNodeFloatCurve has points at (0,0) and (1,1). 
    # We might want a default shape (e.g. flat 1.0 or bell curve), 
    # but keeping default linear 0-1 or Flat 1 might be safer. 
    # Assuming user will edit this curve. Let's set it to a reasonable default if possible,
    # or leave it linear. The original implementation sampled a curve which often had height ~1.
    # Let's set the curve to be flat at 1.0 so it's visible immediately.
    # Accessing curve points: node.mapping.curves[0].points
    curve_points = float_curve.mapping.curves[0].points
    # Reset to two points at y=1
    curve_points[0].location = (0.0, 1.0)
    curve_points[1].location = (1.0, 1.0)
    # Add a middle point for shaping
    # curve_points.new(0.5, 1.0) 
    
    profile_group.links.new(
        input_node.outputs["Length Clamp"], float_curve.inputs["Value"]
    )

    # Math: FloatCurve * Radius
    mult_radius = profile_group.nodes.new("ShaderNodeMath")
    mult_radius.label = "Scale by Radius"
    mult_radius.location = (-200, 0)
    mult_radius.operation = "MULTIPLY"
    
    profile_group.links.new(float_curve.outputs["Value"], mult_radius.inputs[0])
    profile_group.links.new(
        input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        mult_radius.inputs[1]
    )

    # Math: Result * Sin/Cos Theta
    final_mult = profile_group.nodes.new("ShaderNodeMath")
    final_mult.label = "Apply Angle Factor"
    final_mult.location = (0, 0)
    final_mult.operation = "MULTIPLY"

    profile_group.links.new(mult_radius.outputs["Value"], final_mult.inputs[0])
    profile_group.links.new(input_node.outputs["Sin Theta"], final_mult.inputs[1])

    # Output Node
    output_node = profile_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    output_node.location = (200, 0)

    profile_group.links.new(final_mult.outputs["Value"], output_node.inputs["Offset"])
    
    # Pass through geometry
    profile_group.links.new(
        input_node.outputs["Y Profile"], output_node.inputs["Y Profile"]
    )

    # Point Count - return 0 (integer) so logic falls back to Sample Count input elsewhere if Max is used
    # or just 0.
    zero_int = profile_group.nodes.new("FunctionNodeInputInt")
    zero_int.integer = 0
    zero_int.location = (0, -200)
    profile_group.links.new(zero_int.outputs["Integer"], output_node.inputs["Point Count"])

    # --- Instantiation in Parent ---
    profile_instance = parent_node_group.nodes.new("GeometryNodeGroup")
    profile_instance.node_tree = profile_group
    profile_instance.label = group_name
    
    # We don't know exactly where to place it, so (0,0) or similar. 
    # The caller usually sets location, but we can try to offset if needed.
    profile_instance.location = (0, 0) 

    # Connect Parent Inputs
    parent_node_group.links.new(
        length_clamp_node.outputs["Result"],
        profile_instance.inputs["Length Clamp"],
    )
    parent_node_group.links.new(
        parent_input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        profile_instance.inputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
    )
    parent_node_group.links.new(
        angle_param_node.outputs["Value"],
        profile_instance.inputs["Sin Theta"],
    )
    
    # Y Profile input on the instance is left unconnected (will be None/Empty geometry), 
    # which is fine since we just pass it through.

    return profile_instance


