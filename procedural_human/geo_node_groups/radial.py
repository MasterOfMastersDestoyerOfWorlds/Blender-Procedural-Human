import bpy
import math


def create_single_profile_radial_group():
    """
    Creates a node group for radial geometry with a single profile curve.
    """
    group_name = "Radial Profile (Single)"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    group.interface.new_socket(name="Factor", in_out="INPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket(name="Radius", in_out="INPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket(name="Offset", in_out="OUTPUT", socket_type="NodeSocketFloat")

    input_node = group.nodes.new("NodeGroupInput")
    input_node.location = (-400, 0)

    float_curve = group.nodes.new("ShaderNodeFloatCurve")
    float_curve.location = (-200, 0)
    
    group.links.new(input_node.outputs["Factor"], float_curve.inputs["Value"])
    
    mult = group.nodes.new("ShaderNodeMath")
    mult.operation = "MULTIPLY"
    mult.location = (0, 0)
    
    group.links.new(float_curve.outputs["Value"], mult.inputs[0])
    group.links.new(input_node.outputs["Radius"], mult.inputs[1])
    
    output_node = group.nodes.new("NodeGroupOutput")
    output_node.location = (200, 0)
    
    group.links.new(mult.outputs["Value"], output_node.inputs["Offset"])
    
    return group


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
    group.interface.new_socket(name="Factor", in_out="INPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket(name="Angle", in_out="INPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket(name="Radius", in_out="INPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket(name="Offset", in_out="OUTPUT", socket_type="NodeSocketFloat")

    input_node = group.nodes.new("NodeGroupInput")
    input_node.location = (-800, 0)

    
    x_curve = group.nodes.new("ShaderNodeFloatCurve")
    x_curve.label = "X Profile"
    x_curve.location = (-500, 100)
    group.links.new(input_node.outputs["Factor"], x_curve.inputs["Value"])

    
    y_curve = group.nodes.new("ShaderNodeFloatCurve")
    y_curve.label = "Y Profile"
    y_curve.location = (-500, -100)
    group.links.new(input_node.outputs["Factor"], y_curve.inputs["Value"])

    
    cos_node = group.nodes.new("ShaderNodeMath")
    cos_node.operation = "COSINE"
    cos_node.label = "Cos(Theta)"
    cos_node.location = (-500, 300)
    group.links.new(input_node.outputs["Angle"], cos_node.inputs[0])

    
    sin_node = group.nodes.new("ShaderNodeMath")
    sin_node.operation = "SINE"
    sin_node.label = "Sin(Theta)"
    sin_node.location = (-500, -300)
    group.links.new(input_node.outputs["Angle"], sin_node.inputs[0])

    
    x_mult = group.nodes.new("ShaderNodeMath")
    x_mult.operation = "MULTIPLY"
    x_mult.location = (-300, 200)
    group.links.new(x_curve.outputs["Value"], x_mult.inputs[0])
    group.links.new(cos_node.outputs["Value"], x_mult.inputs[1])

    x_sq = group.nodes.new("ShaderNodeMath")
    x_sq.operation = "POWER"
    x_sq.inputs[1].default_value = 2.0
    x_sq.location = (-100, 200)
    group.links.new(x_mult.outputs["Value"], x_sq.inputs[0])

    
    y_mult = group.nodes.new("ShaderNodeMath")
    y_mult.operation = "MULTIPLY"
    y_mult.location = (-300, -200)
    group.links.new(y_curve.outputs["Value"], y_mult.inputs[0])
    group.links.new(sin_node.outputs["Value"], y_mult.inputs[1])

    y_sq = group.nodes.new("ShaderNodeMath")
    y_sq.operation = "POWER"
    y_sq.inputs[1].default_value = 2.0
    y_sq.location = (-100, -200)
    group.links.new(y_mult.outputs["Value"], y_sq.inputs[0])

    
    add = group.nodes.new("ShaderNodeMath")
    add.operation = "ADD"
    add.location = (100, 0)
    group.links.new(x_sq.outputs["Value"], add.inputs[0])
    group.links.new(y_sq.outputs["Value"], add.inputs[1])

    sqrt = group.nodes.new("ShaderNodeMath")
    sqrt.operation = "SQRT"
    sqrt.location = (300, 0)
    group.links.new(add.outputs["Value"], sqrt.inputs[0])

    
    final_mult = group.nodes.new("ShaderNodeMath")
    final_mult.operation = "MULTIPLY"
    final_mult.location = (500, 0)
    group.links.new(sqrt.outputs["Value"], final_mult.inputs[0])
    group.links.new(input_node.outputs["Radius"], final_mult.inputs[1])

    output_node = group.nodes.new("NodeGroupOutput")
    output_node.location = (700, 0)
    group.links.new(final_mult.outputs["Value"], output_node.inputs["Offset"])

    return group


def create_quad_profile_radial_group():
    """
    Creates a node group for radial geometry with 4 profiles (0, 90, 180, 270).
    Interpolates between adjacent profiles.
    """
    group_name = "Radial Profile (Quad)"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    group.interface.new_socket(name="Factor", in_out="INPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket(name="Angle", in_out="INPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket(name="Radius", in_out="INPUT", socket_type="NodeSocketFloat")
    group.interface.new_socket(name="Offset", in_out="OUTPUT", socket_type="NodeSocketFloat")

    input_node = group.nodes.new("NodeGroupInput")
    input_node.location = (-1000, 0)

    
    profiles = []
    labels = ["0 (+X)", "90 (+Y)", "180 (-X)", "270 (-Y)"]
    for i in range(4):
        curve = group.nodes.new("ShaderNodeFloatCurve")
        curve.label = labels[i]
        curve.location = (-600, 400 - i * 200)
        group.links.new(input_node.outputs["Factor"], curve.inputs["Value"])
        profiles.append(curve)

    
    
    
    
    cos_node = group.nodes.new("ShaderNodeMath")
    cos_node.operation = "COSINE"
    cos_node.location = (-800, 200)
    group.links.new(input_node.outputs["Angle"], cos_node.inputs[0])
    
    
    sin_node = group.nodes.new("ShaderNodeMath")
    sin_node.operation = "SINE"
    sin_node.location = (-800, -200)
    group.links.new(input_node.outputs["Angle"], sin_node.inputs[0])

    
    
    gt_zero_x = group.nodes.new("ShaderNodeMath")
    gt_zero_x.operation = "GREATER_THAN"
    gt_zero_x.location = (-400, 300)
    group.links.new(cos_node.outputs["Value"], gt_zero_x.inputs[0])
    
    mix_x = group.nodes.new("ShaderNodeMix")
    mix_x.data_type = "FLOAT"
    mix_x.label = "Mix X Profiles"
    mix_x.location = (-200, 300)
    group.links.new(gt_zero_x.outputs["Value"], mix_x.inputs["Factor"])
    group.links.new(profiles[2].outputs["Value"], mix_x.inputs[4]) 
    group.links.new(profiles[0].outputs["Value"], mix_x.inputs[5]) 
    
    
    
    gt_zero_y = group.nodes.new("ShaderNodeMath")
    gt_zero_y.operation = "GREATER_THAN"
    gt_zero_y.location = (-400, -100)
    group.links.new(sin_node.outputs["Value"], gt_zero_y.inputs[0])
    
    mix_y = group.nodes.new("ShaderNodeMix")
    mix_y.data_type = "FLOAT"
    mix_y.label = "Mix Y Profiles"
    mix_y.location = (-200, -100)
    group.links.new(gt_zero_y.outputs["Value"], mix_y.inputs["Factor"])
    group.links.new(profiles[3].outputs["Value"], mix_y.inputs[4]) 
    group.links.new(profiles[1].outputs["Value"], mix_y.inputs[5]) 

    
    
    
    x_mult = group.nodes.new("ShaderNodeMath")
    x_mult.operation = "MULTIPLY"
    x_mult.location = (0, 200)
    group.links.new(mix_x.outputs["Result"], x_mult.inputs[0])
    group.links.new(cos_node.outputs["Value"], x_mult.inputs[1])
    
    x_sq = group.nodes.new("ShaderNodeMath")
    x_sq.operation = "POWER"
    x_sq.inputs[1].default_value = 2.0
    x_sq.location = (200, 200)
    group.links.new(x_mult.outputs["Value"], x_sq.inputs[0])
    
    
    y_mult = group.nodes.new("ShaderNodeMath")
    y_mult.operation = "MULTIPLY"
    y_mult.location = (0, -200)
    group.links.new(mix_y.outputs["Result"], y_mult.inputs[0])
    group.links.new(sin_node.outputs["Value"], y_mult.inputs[1])
    
    y_sq = group.nodes.new("ShaderNodeMath")
    y_sq.operation = "POWER"
    y_sq.inputs[1].default_value = 2.0
    y_sq.location = (200, -200)
    group.links.new(y_mult.outputs["Value"], y_sq.inputs[0])
    
    
    add = group.nodes.new("ShaderNodeMath")
    add.operation = "ADD"
    add.location = (400, 0)
    group.links.new(x_sq.outputs["Value"], add.inputs[0])
    group.links.new(y_sq.outputs["Value"], add.inputs[1])
    
    sqrt = group.nodes.new("ShaderNodeMath")
    sqrt.operation = "SQRT"
    sqrt.location = (600, 0)
    group.links.new(add.outputs["Value"], sqrt.inputs[0])
    
    
    final_mult = group.nodes.new("ShaderNodeMath")
    final_mult.operation = "MULTIPLY"
    final_mult.location = (800, 0)
    group.links.new(sqrt.outputs["Value"], final_mult.inputs[0])
    group.links.new(input_node.outputs["Radius"], final_mult.inputs[1])
    
    output_node = group.nodes.new("NodeGroupOutput")
    output_node.location = (1000, 0)
    group.links.new(final_mult.outputs["Value"], output_node.inputs["Offset"])

    return group

