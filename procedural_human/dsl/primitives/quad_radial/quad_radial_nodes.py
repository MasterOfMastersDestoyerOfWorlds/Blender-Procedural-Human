import bpy
import math

from procedural_human.utils.node_layout import auto_layout_nodes


def create_quad_profile_radial_group(suffix=None):
    """
    Creates a node group for radial geometry with 4 profiles (0°, 90°, 180°, 270°).
    Uses closure inputs for each quadrant profile.
    Interpolates between adjacent profiles based on angle.
    """
    group_name = "Radial Profile (Quad)"
    if suffix:
        group_name += f" {suffix}"

    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    group.interface.new_socket(
        name="Radius", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    group.interface.new_socket(
        name="Z Position", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    group.interface.new_socket(
        name="0° Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
    )
    group.interface.new_socket(
        name="90° Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
    )
    group.interface.new_socket(
        name="180° Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
    )
    group.interface.new_socket(
        name="270° Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
    )
    group.interface.new_socket(
        name="Segment Length", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    group.interface.new_socket(
        name="Position", in_out="OUTPUT", socket_type="NodeSocketVector"
    )

    input_node = group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"

    grid_pos = group.nodes.new("GeometryNodeInputPosition")
    grid_pos.label = "Grid Position"

    separate_grid = group.nodes.new("ShaderNodeSeparateXYZ")
    separate_grid.label = "Separate Grid Coords"
    group.links.new(grid_pos.outputs["Position"], separate_grid.inputs["Vector"])

    angle_param = group.nodes.new("ShaderNodeMath")
    angle_param.label = "Angle Param"
    angle_param.operation = "ADD"
    angle_param.inputs[1].default_value = 0.5
    group.links.new(separate_grid.outputs["X"], angle_param.inputs[0])

    length_param = group.nodes.new("ShaderNodeMath")
    length_param.label = "Length Param"
    length_param.operation = "ADD"
    length_param.inputs[1].default_value = 0.5
    group.links.new(separate_grid.outputs["Y"], length_param.inputs[0])

    angle_clamp = group.nodes.new("ShaderNodeClamp")
    angle_clamp.label = "Clamp Angle"
    angle_clamp.inputs["Value"].default_value = 1.0
    group.links.new(angle_param.outputs["Value"], angle_clamp.inputs["Value"])

    length_clamp = group.nodes.new("ShaderNodeClamp")
    length_clamp.label = "Clamp Length"
    length_clamp.inputs["Value"].default_value = 1.0
    group.links.new(length_param.outputs["Value"], length_clamp.inputs["Value"])

    theta_node = group.nodes.new("ShaderNodeMath")
    theta_node.label = "Angle θ"
    theta_node.operation = "MULTIPLY"
    theta_node.inputs[1].default_value = 2 * math.pi
    group.links.new(angle_clamp.outputs["Result"], theta_node.inputs[0])

    evaluate_0 = group.nodes.new("NodeEvaluateClosure")
    evaluate_0.label = "Evaluate 0° Curve"
    evaluate_0.define_signature = True
    evaluate_0.input_items.new(socket_type="FLOAT", name="Value")
    evaluate_0.output_items.new(socket_type="FLOAT", name="Value")
    group.links.new(input_node.outputs["0° Float Curve"], evaluate_0.inputs["Closure"])
    group.links.new(length_clamp.outputs["Result"], evaluate_0.inputs["Value"])

    evaluate_90 = group.nodes.new("NodeEvaluateClosure")
    evaluate_90.label = "Evaluate 90° Curve"
    evaluate_90.define_signature = True
    evaluate_90.input_items.new(socket_type="FLOAT", name="Value")
    evaluate_90.output_items.new(socket_type="FLOAT", name="Value")
    group.links.new(
        input_node.outputs["90° Float Curve"], evaluate_90.inputs["Closure"]
    )
    group.links.new(length_clamp.outputs["Result"], evaluate_90.inputs["Value"])

    evaluate_180 = group.nodes.new("NodeEvaluateClosure")
    evaluate_180.label = "Evaluate 180° Curve"
    evaluate_180.define_signature = True
    evaluate_180.input_items.new(socket_type="FLOAT", name="Value")
    evaluate_180.output_items.new(socket_type="FLOAT", name="Value")
    group.links.new(
        input_node.outputs["180° Float Curve"], evaluate_180.inputs["Closure"]
    )
    group.links.new(length_clamp.outputs["Result"], evaluate_180.inputs["Value"])

    evaluate_270 = group.nodes.new("NodeEvaluateClosure")
    evaluate_270.label = "Evaluate 270° Curve"
    evaluate_270.define_signature = True
    evaluate_270.input_items.new(socket_type="FLOAT", name="Value")
    evaluate_270.output_items.new(socket_type="FLOAT", name="Value")
    group.links.new(
        input_node.outputs["270° Float Curve"], evaluate_270.inputs["Closure"]
    )
    group.links.new(length_clamp.outputs["Result"], evaluate_270.inputs["Value"])

    cos_node = group.nodes.new("ShaderNodeMath")
    cos_node.operation = "COSINE"
    cos_node.label = "Cos(Theta)"
    group.links.new(theta_node.outputs["Value"], cos_node.inputs[0])

    sin_node = group.nodes.new("ShaderNodeMath")
    sin_node.operation = "SINE"
    sin_node.label = "Sin(Theta)"
    group.links.new(theta_node.outputs["Value"], sin_node.inputs[0])

    gt_zero_x = group.nodes.new("ShaderNodeMath")
    gt_zero_x.operation = "GREATER_THAN"
    gt_zero_x.label = "cos > 0"
    group.links.new(cos_node.outputs["Value"], gt_zero_x.inputs[0])

    mix_x = group.nodes.new("ShaderNodeMix")
    mix_x.data_type = "FLOAT"
    mix_x.label = "Mix X Profiles"
    group.links.new(gt_zero_x.outputs["Value"], mix_x.inputs["Factor"])
    group.links.new(evaluate_180.outputs["Value"], mix_x.inputs["A"])
    group.links.new(evaluate_0.outputs["Value"], mix_x.inputs["B"])

    gt_zero_y = group.nodes.new("ShaderNodeMath")
    gt_zero_y.operation = "GREATER_THAN"
    gt_zero_y.label = "sin > 0"
    group.links.new(sin_node.outputs["Value"], gt_zero_y.inputs[0])

    mix_y = group.nodes.new("ShaderNodeMix")
    mix_y.data_type = "FLOAT"
    mix_y.label = "Mix Y Profiles"
    group.links.new(gt_zero_y.outputs["Value"], mix_y.inputs["Factor"])
    group.links.new(evaluate_270.outputs["Value"], mix_y.inputs["A"])
    group.links.new(evaluate_90.outputs["Value"], mix_y.inputs["B"])

    x_mult = group.nodes.new("ShaderNodeMath")
    x_mult.label = "X * Cos"
    x_mult.operation = "MULTIPLY"
    group.links.new(mix_x.outputs["Result"], x_mult.inputs[0])
    group.links.new(cos_node.outputs["Value"], x_mult.inputs[1])

    x_sq = group.nodes.new("ShaderNodeMath")
    x_sq.label = "X²"
    x_sq.operation = "POWER"
    x_sq.inputs[1].default_value = 2.0
    group.links.new(x_mult.outputs["Value"], x_sq.inputs[0])

    y_mult = group.nodes.new("ShaderNodeMath")
    y_mult.label = "Y * Sin"
    y_mult.operation = "MULTIPLY"
    group.links.new(mix_y.outputs["Result"], y_mult.inputs[0])
    group.links.new(sin_node.outputs["Value"], y_mult.inputs[1])

    y_sq = group.nodes.new("ShaderNodeMath")
    y_sq.label = "Y²"
    y_sq.operation = "POWER"
    y_sq.inputs[1].default_value = 2.0
    group.links.new(y_mult.outputs["Value"], y_sq.inputs[0])

    add = group.nodes.new("ShaderNodeMath")
    add.label = "X² + Y²"
    add.operation = "ADD"
    group.links.new(x_sq.outputs["Value"], add.inputs[0])
    group.links.new(y_sq.outputs["Value"], add.inputs[1])

    sqrt = group.nodes.new("ShaderNodeMath")
    sqrt.label = "√(X² + Y²)"
    sqrt.operation = "SQRT"
    group.links.new(add.outputs["Value"], sqrt.inputs[0])

    final_mult = group.nodes.new("ShaderNodeMath")
    final_mult.label = "Scale by Radius"
    final_mult.operation = "MULTIPLY"
    group.links.new(sqrt.outputs["Value"], final_mult.inputs[0])
    group.links.new(input_node.outputs["Radius"], final_mult.inputs[1])

    z_offset = group.nodes.new("ShaderNodeMath")
    z_offset.label = "Length Offset"
    z_offset.operation = "MULTIPLY"
    group.links.new(length_clamp.outputs["Result"], z_offset.inputs[0])
    group.links.new(input_node.outputs["Segment Length"], z_offset.inputs[1])

    z_position = group.nodes.new("ShaderNodeMath")
    z_position.label = "Z Position"
    z_position.operation = "ADD"
    group.links.new(input_node.outputs["Z Position"], z_position.inputs[0])
    group.links.new(z_offset.outputs["Value"], z_position.inputs[1])

    cos_theta = group.nodes.new("ShaderNodeMath")
    cos_theta.label = "cos(θ) Final"
    cos_theta.operation = "COSINE"
    group.links.new(theta_node.outputs["Value"], cos_theta.inputs[0])

    sin_theta = group.nodes.new("ShaderNodeMath")
    sin_theta.label = "sin(θ) Final"
    sin_theta.operation = "SINE"
    group.links.new(theta_node.outputs["Value"], sin_theta.inputs[0])

    final_x = group.nodes.new("ShaderNodeMath")
    final_x.label = "Final X"
    final_x.operation = "MULTIPLY"
    group.links.new(final_mult.outputs["Value"], final_x.inputs[0])
    group.links.new(cos_theta.outputs["Value"], final_x.inputs[1])

    final_y = group.nodes.new("ShaderNodeMath")
    final_y.label = "Final Y"
    final_y.operation = "MULTIPLY"
    group.links.new(final_mult.outputs["Value"], final_y.inputs[0])
    group.links.new(sin_theta.outputs["Value"], final_y.inputs[1])

    final_pos = group.nodes.new("ShaderNodeCombineXYZ")
    final_pos.label = "Final Position"
    group.links.new(final_x.outputs["Value"], final_pos.inputs["X"])
    group.links.new(final_y.outputs["Value"], final_pos.inputs["Y"])
    group.links.new(z_position.outputs["Value"], final_pos.inputs["Z"])

    output_node = group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"
    group.links.new(final_pos.outputs["Vector"], output_node.inputs["Position"])

    auto_layout_nodes(group)
    return group
