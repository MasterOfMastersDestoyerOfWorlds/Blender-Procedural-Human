import bpy
import math
from procedural_human.utils.node_layout import auto_layout_nodes


def create_dual_radial_loft_group(name: str = "Dual Radial Loft"):
    """
    Creates a node group for 'Elliptical Revolution' from two loops.

    Fixes the 'Missing Quadrants' issue by decoupling the curve position
    from the radial quadrant.

    Logic:
    1. Sample Curve 1 to get the X-profile (and Y-height).
    2. Sample Curve 2 to get the Z-profile (and Y-height).
    3. Revolve this combined profile 360 degrees (Tau).

    Math:
    Angle = Grid.Y * 2*Pi
    X_pos = Curve1.X * cos(Angle)
    Z_pos = Curve2.Z * sin(Angle)
    Y_pos = Average(Curve1.Y, Curve2.Y)
    """
    group_name = name
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    group.interface.new_socket(
        name="Curve X (Front)", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    group.interface.new_socket(
        name="Curve Y (Side)", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    group.interface.new_socket(
        name="Resolution V", in_out="INPUT", socket_type="NodeSocketInt"
    ).default_value = 64
    group.interface.new_socket(
        name="Resolution U", in_out="INPUT", socket_type="NodeSocketInt"
    ).default_value = 32
    group.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )
    input_node = group.nodes.new("NodeGroupInput")
    output_node = group.nodes.new("NodeGroupOutput")
    grid = group.nodes.new("GeometryNodeMeshGrid")
    grid.inputs["Size X"].default_value = 1.0
    grid.inputs["Size Y"].default_value = 1.0

    group.links.new(input_node.outputs["Resolution U"], grid.inputs["Vertices X"])
    group.links.new(input_node.outputs["Resolution V"], grid.inputs["Vertices Y"])
    grid_pos = group.nodes.new("GeometryNodeInputPosition")
    sep_grid = group.nodes.new("ShaderNodeSeparateXYZ")
    group.links.new(grid_pos.outputs["Position"], sep_grid.inputs["Vector"])

    map_u = group.nodes.new("ShaderNodeMapRange")
    map_u.label = "Map U (Curve)"
    map_u.inputs["From Min"].default_value = -0.5
    map_u.inputs["From Max"].default_value = 0.5
    map_u.inputs["To Min"].default_value = 0.0
    map_u.inputs["To Max"].default_value = 1.0
    group.links.new(sep_grid.outputs["X"], map_u.inputs["Value"])

    map_v = group.nodes.new("ShaderNodeMapRange")
    map_v.label = "Map V (Revolution)"
    map_v.inputs["From Min"].default_value = -0.5
    map_v.inputs["From Max"].default_value = 0.5
    map_v.inputs["To Min"].default_value = 0.0
    map_v.inputs["To Max"].default_value = 1.0
    group.links.new(sep_grid.outputs["Y"], map_v.inputs["Value"])

    u_param = map_u.outputs["Result"]
    v_param = map_v.outputs["Result"]
    sample_1 = group.nodes.new("GeometryNodeSampleCurve")
    sample_1.data_type = "FLOAT_VECTOR"
    sample_1.mode = "FACTOR"
    sample_1.use_all_curves = True
    group.links.new(input_node.outputs["Curve X (Front)"], sample_1.inputs["Curves"])
    group.links.new(u_param, sample_1.inputs["Factor"])
    sample_2 = group.nodes.new("GeometryNodeSampleCurve")
    sample_2.data_type = "FLOAT_VECTOR"
    sample_2.mode = "FACTOR"
    sample_2.use_all_curves = True
    group.links.new(input_node.outputs["Curve Y (Side)"], sample_2.inputs["Curves"])
    group.links.new(u_param, sample_2.inputs["Factor"])
    sep_1 = group.nodes.new("ShaderNodeSeparateXYZ")
    group.links.new(sample_1.outputs["Position"], sep_1.inputs["Vector"])

    sep_2 = group.nodes.new("ShaderNodeSeparateXYZ")
    group.links.new(sample_2.outputs["Position"], sep_2.inputs["Vector"])

    tau_node = group.nodes.new("ShaderNodeMath")
    tau_node.operation = "MULTIPLY"
    tau_node.inputs[1].default_value = 6.283185  # 2 * Pi
    group.links.new(v_param, tau_node.inputs[0])
    theta = tau_node.outputs["Value"]

    cos_t = group.nodes.new("ShaderNodeMath")
    cos_t.operation = "COSINE"
    group.links.new(theta, cos_t.inputs[0])

    sin_t = group.nodes.new("ShaderNodeMath")
    sin_t.operation = "SINE"
    group.links.new(theta, sin_t.inputs[0])
    final_x = group.nodes.new("ShaderNodeMath")
    final_x.operation = "MULTIPLY"
    group.links.new(sep_1.outputs["X"], final_x.inputs[0])
    group.links.new(cos_t.outputs["Value"], final_x.inputs[1])
    final_z = group.nodes.new("ShaderNodeMath")
    final_z.operation = "MULTIPLY"
    group.links.new(sep_2.outputs["Z"], final_z.inputs[0])
    group.links.new(sin_t.outputs["Value"], final_z.inputs[1])
    mix_y = group.nodes.new("ShaderNodeMix")
    mix_y.data_type = "FLOAT"
    mix_y.inputs["Factor"].default_value = 0.5
    group.links.new(sep_1.outputs["Y"], mix_y.inputs["A"])
    group.links.new(sep_2.outputs["Y"], mix_y.inputs["B"])
    combine = group.nodes.new("ShaderNodeCombineXYZ")
    group.links.new(final_x.outputs["Value"], combine.inputs["X"])
    group.links.new(mix_y.outputs["Result"], combine.inputs["Y"])
    group.links.new(final_z.outputs["Value"], combine.inputs["Z"])
    set_pos = group.nodes.new("GeometryNodeSetPosition")
    group.links.new(grid.outputs["Mesh"], set_pos.inputs["Geometry"])
    group.links.new(combine.outputs["Vector"], set_pos.inputs["Position"])
    merge = group.nodes.new("GeometryNodeMergeByDistance")
    merge.inputs["Distance"].default_value = 0.001
    group.links.new(set_pos.outputs["Geometry"], merge.inputs["Geometry"])
    normals = group.nodes.new("GeometryNodeSetShadeSmooth")

    group.links.new(merge.outputs["Geometry"], normals.inputs["Geometry"])
    group.links.new(normals.outputs["Geometry"], output_node.inputs["Geometry"])
    try:
        auto_layout_nodes(group)
    except Exception:
        pass

    return group
