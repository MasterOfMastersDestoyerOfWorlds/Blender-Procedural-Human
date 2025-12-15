import bpy
import math

from procedural_human.utils.node_layout import auto_layout_nodes


def create_dual_profile_radial_group(suffix=None):
    """
    Creates a node group for radial geometry with 2 profiles (X and Y).
    Uses angle-based interpolation:
    radius(θ) = sqrt((X(t)*cos(θ))² + (Y(t)*sin(θ))²)
    """
    group_name = "Radial Profile (Dual)"
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
        name="X Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
    )
    group.interface.new_socket(
        name="Y Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
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

    evaluate_x_curve = group.nodes.new("NodeEvaluateClosure")
    evaluate_x_curve.label = "Evaluate X Float Curve"
    evaluate_x_curve.define_signature = True
    evaluate_x_curve.input_items.new(socket_type="FLOAT", name="Value")
    evaluate_x_curve.output_items.new(socket_type="FLOAT", name="Value")
    group.links.new(
        input_node.outputs["X Float Curve"], evaluate_x_curve.inputs["Closure"]
    )
    group.links.new(length_clamp.outputs["Result"], evaluate_x_curve.inputs["Value"])

    evaluate_y_curve = group.nodes.new("NodeEvaluateClosure")
    evaluate_y_curve.label = "Evaluate Y Float Curve"
    evaluate_y_curve.define_signature = True
    evaluate_y_curve.input_items.new(socket_type="FLOAT", name="Value")
    evaluate_y_curve.output_items.new(socket_type="FLOAT", name="Value")
    group.links.new(
        input_node.outputs["Y Float Curve"], evaluate_y_curve.inputs["Closure"]
    )
    group.links.new(length_clamp.outputs["Result"], evaluate_y_curve.inputs["Value"])

    cos_node = group.nodes.new("ShaderNodeMath")
    cos_node.operation = "COSINE"
    cos_node.label = "Cos(Theta)"
    group.links.new(theta_node.outputs["Value"], cos_node.inputs[0])

    sin_node = group.nodes.new("ShaderNodeMath")
    sin_node.operation = "SINE"
    sin_node.label = "Sin(Theta)"
    group.links.new(theta_node.outputs["Value"], sin_node.inputs[0])

    x_mult = group.nodes.new("ShaderNodeMath")
    x_mult.label = "X * Cos"
    x_mult.operation = "MULTIPLY"
    group.links.new(evaluate_x_curve.outputs["Value"], x_mult.inputs[0])
    group.links.new(cos_node.outputs["Value"], x_mult.inputs[1])

    x_sq = group.nodes.new("ShaderNodeMath")
    x_sq.label = "X²"
    x_sq.operation = "POWER"
    x_sq.inputs[1].default_value = 2.0
    group.links.new(x_mult.outputs["Value"], x_sq.inputs[0])

    y_mult = group.nodes.new("ShaderNodeMath")
    y_mult.label = "Y * Sin"
    y_mult.operation = "MULTIPLY"
    group.links.new(evaluate_y_curve.outputs["Value"], y_mult.inputs[0])
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
    group.links.new(
        input_node.outputs["Segment Length"],
        z_offset.inputs[1],
    )

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
