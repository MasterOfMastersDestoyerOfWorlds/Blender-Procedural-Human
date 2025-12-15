import bpy
from procedural_human.utils.node_layout import auto_layout_nodes


def create_hex_profile_spheroid_group(suffix=None):
    """
    Creates a node group for spheroid geometry with 6 profiles (X+, X-, Y+, Y-, Z+, Z-).

    Uses 3D Root-Sum-Square interpolation (generalized Dual Radial technique):
    R = sqrt((Rx * nx)^2 + (Ry * ny)^2 + (Rz * nz)^2)

    Curve Inputs:
    - X Curves take distance from X-axis (sqrt(y^2+z^2)) as input [0-1]
    - Y Curves take distance from Y-axis (sqrt(x^2+z^2)) as input [0-1]
    - Z Curves take distance from Z-axis (sqrt(x^2+y^2)) as input [0-1]
    """
    group_name = "Radial Profile (Hex)"
    if suffix:
        group_name += f" {suffix}"

    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # Inputs
    group.interface.new_socket(
        name="Radius", in_out="INPUT", socket_type="NodeSocketFloat"
    ).default_value = 1.0

    # 6 Curve Inputs
    directions = ["X+", "X-", "Y+", "Y-", "Z+", "Z-"]
    for d in directions:
        group.interface.new_socket(
            name=f"{d} Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
        )

    group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    group.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )

    # --- Nodes ---
    input_node = group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"

    # Get Position and Normalize to get direction vector n
    pos_node = group.nodes.new("GeometryNodeInputPosition")

    normalize = group.nodes.new("ShaderNodeVectorMath")
    normalize.operation = "NORMALIZE"
    normalize.label = "Normal (n)"
    group.links.new(pos_node.outputs["Position"], normalize.inputs[0])

    sep_xyz = group.nodes.new("ShaderNodeSeparateXYZ")
    group.links.new(normalize.outputs["Vector"], sep_xyz.inputs["Vector"])

    # --- Calculate Input Parameters (Distance from Axes) ---
    # Input for X curves = sqrt(ny^2 + nz^2) aka length(ny, nz)
    # Since n is normalized, this is also sqrt(1 - nx^2)

    # Helper to create component math
    def create_axis_logic(
        axis_char, comp_node, pos_socket, neg_socket, param_input_x, param_input_y
    ):
        """
        Generates nodes for one axis (e.g., X).
        Returns the (Val * n_axis)^2 node.
        """
        # 1. Calculate Parameter (Length of other two components)
        # We construct a vector of the *other* two components to get length
        combine_perp = group.nodes.new("ShaderNodeCombineXYZ")
        combine_perp.label = f"Perp Plane {axis_char}"

        if axis_char == "X":
            group.links.new(param_input_x, combine_perp.inputs["Y"])  # ny
            group.links.new(param_input_y, combine_perp.inputs["Z"])  # nz
        elif axis_char == "Y":
            group.links.new(param_input_x, combine_perp.inputs["X"])  # nx
            group.links.new(param_input_y, combine_perp.inputs["Z"])  # nz
        else:  # Z
            group.links.new(param_input_x, combine_perp.inputs["X"])  # nx
            group.links.new(param_input_y, combine_perp.inputs["Y"])  # ny

        param_len = group.nodes.new("ShaderNodeVectorMath")
        param_len.operation = "LENGTH"
        group.links.new(combine_perp.outputs["Vector"], param_len.inputs[0])

        # 2. Evaluate both curves (Pos and Neg)
        eval_pos = group.nodes.new("NodeEvaluateClosure")
        eval_pos.label = f"Eval {axis_char}+"
        eval_pos.define_signature = True
        eval_pos.input_items.new(socket_type="FLOAT", name="Value")
        eval_pos.output_items.new(socket_type="FLOAT", name="Value")
        group.links.new(pos_socket, eval_pos.inputs["Closure"])
        group.links.new(param_len.outputs["Value"], eval_pos.inputs["Value"])

        eval_neg = group.nodes.new("NodeEvaluateClosure")
        eval_neg.label = f"Eval {axis_char}-"
        eval_neg.define_signature = True
        eval_neg.input_items.new(socket_type="FLOAT", name="Value")
        eval_neg.output_items.new(socket_type="FLOAT", name="Value")
        group.links.new(neg_socket, eval_neg.inputs["Closure"])
        group.links.new(param_len.outputs["Value"], eval_neg.inputs["Value"])

        # 3. Switch based on sign of component
        gt_zero = group.nodes.new("ShaderNodeMath")
        gt_zero.operation = "GREATER_THAN"
        group.links.new(comp_node, gt_zero.inputs[0])

        mix_val = group.nodes.new("ShaderNodeMix")
        mix_val.data_type = "FLOAT"
        mix_val.label = f"Mix {axis_char}"
        group.links.new(gt_zero.outputs["Value"], mix_val.inputs["Factor"])
        group.links.new(eval_neg.outputs["Value"], mix_val.inputs["A"])
        group.links.new(eval_pos.outputs["Value"], mix_val.inputs["B"])

        # 4. Multiply by component: (Val * n_axis)
        mult_comp = group.nodes.new("ShaderNodeMath")
        mult_comp.operation = "MULTIPLY"
        group.links.new(mix_val.outputs["Result"], mult_comp.inputs[0])
        group.links.new(comp_node, mult_comp.inputs[1])

        # 5. Square it: (Val * n_axis)^2
        sq_node = group.nodes.new("ShaderNodeMath")
        sq_node.operation = "POWER"
        sq_node.inputs[1].default_value = 2.0
        group.links.new(mult_comp.outputs["Value"], sq_node.inputs[0])

        return sq_node

    # Logic for X
    x_sq = create_axis_logic(
        "X",
        sep_xyz.outputs["X"],
        input_node.outputs["X+ Float Curve"],
        input_node.outputs["X- Float Curve"],
        sep_xyz.outputs["Y"],
        sep_xyz.outputs["Z"],
    )

    # Logic for Y
    y_sq = create_axis_logic(
        "Y",
        sep_xyz.outputs["Y"],
        input_node.outputs["Y+ Float Curve"],
        input_node.outputs["Y- Float Curve"],
        sep_xyz.outputs["X"],
        sep_xyz.outputs["Z"],
    )

    # Logic for Z
    z_sq = create_axis_logic(
        "Z",
        sep_xyz.outputs["Z"],
        input_node.outputs["Z+ Float Curve"],
        input_node.outputs["Z- Float Curve"],
        sep_xyz.outputs["X"],
        sep_xyz.outputs["Y"],
    )

    # --- Combine ---
    add_xy = group.nodes.new("ShaderNodeMath")
    add_xy.operation = "ADD"
    group.links.new(x_sq.outputs["Value"], add_xy.inputs[0])
    group.links.new(y_sq.outputs["Value"], add_xy.inputs[1])

    add_xyz = group.nodes.new("ShaderNodeMath")
    add_xyz.operation = "ADD"
    group.links.new(add_xy.outputs["Value"], add_xyz.inputs[0])
    group.links.new(z_sq.outputs["Value"], add_xyz.inputs[1])

    # Sqrt to get final R
    # R = sqrt( (Rx*nx)^2 + (Ry*ny)^2 + (Rz*nz)^2 )
    final_r = group.nodes.new("ShaderNodeMath")
    final_r.operation = "SQRT"
    group.links.new(add_xyz.outputs["Value"], final_r.inputs[0])

    # Apply Global Radius Scale
    scale_r = group.nodes.new("ShaderNodeMath")
    scale_r.operation = "MULTIPLY"
    group.links.new(final_r.outputs["Value"], scale_r.inputs[0])
    group.links.new(input_node.outputs["Radius"], scale_r.inputs[1])

    # Calculate Final Position: P = n * R
    scale_vec = group.nodes.new("ShaderNodeVectorMath")
    scale_vec.operation = "SCALE"
    group.links.new(normalize.outputs["Vector"], scale_vec.inputs[0])
    group.links.new(scale_r.outputs["Value"], scale_vec.inputs[3])

    # Set Position
    set_pos = group.nodes.new("GeometryNodeSetPosition")
    group.links.new(input_node.outputs["Geometry"], set_pos.inputs["Geometry"])
    group.links.new(scale_vec.outputs["Vector"], set_pos.inputs["Position"])

    # Output
    output_node = group.nodes.new("NodeGroupOutput")
    group.links.new(set_pos.outputs["Geometry"], output_node.inputs["Geometry"])

    auto_layout_nodes(group)
    return group
