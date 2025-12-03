"""
Geometry Node helpers for fingernail creation and attachment.
"""

import math
import bpy

from procedural_human.blender_const import NODE_WIDTH
from procedural_human.dsl.finger_segment_const import SEGMENT_SAMPLE_COUNT
from procedural_human.utils import setup_node_group_interface
from procedural_human.utils.node_layout import auto_layout_nodes


DEFAULT_NAIL_SIZE = 0.003
OFFSET_RATIO = 0.1


def create_fingernail_node_group(
    name,
    curl_direction,
    nail_width_ratio,
    attachment_position=0.8,
    wrap_amount=math.pi / 2,
    height_position=0.5,
    max_thickness=0.001,
):
    """
    Create a reusable node group for a fingernail/radial attachment.
    
    Uses Raycast to attach precisely to the mesh surface.
    Segment radius is determined automatically via raycast on input geometry
    at the specified attachment position along the segment.
    
    Args:
        name: Name for the node group
        curl_direction: Curl axis ("X", "Y", or "Z") - center of radial attachment
        nail_width_ratio: Width ratio of attachment relative to segment radius
        attachment_position: Position along segment (0-1) to sample radius
        wrap_amount: Angular coverage around curl axis in radians (0 to 2π)
        height_position: Position along segment length (0-1) for attach base point
        max_thickness: Maximum thickness in world units (meters)
    """
    nail_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    setup_node_group_interface(nail_group)

    width_socket = nail_group.interface.new_socket(
        name="Nail Width Ratio", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    width_socket.default_value = nail_width_ratio

    attach_pos_socket = nail_group.interface.new_socket(
        name="Attachment Position", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    attach_pos_socket.default_value = attachment_position
    attach_pos_socket.min_value = 0.0
    attach_pos_socket.max_value = 1.0

    wrap_socket = nail_group.interface.new_socket(
        name="Wrap Amount", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    wrap_socket.default_value = wrap_amount
    wrap_socket.min_value = 0.0
    wrap_socket.max_value = 2 * math.pi

    height_pos_socket = nail_group.interface.new_socket(
        name="Height Position", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    height_pos_socket.default_value = height_position
    height_pos_socket.min_value = 0.0
    height_pos_socket.max_value = 1.0

    # Max Thickness input (in world units)
    max_thickness_socket = nail_group.interface.new_socket(
        name="Max Thickness", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    max_thickness_socket.default_value = max_thickness
    max_thickness_socket.min_value = 0.0

    # Closure inputs for shaping
    nail_group.interface.new_socket(
        name="Angle Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
    )
    nail_group.interface.new_socket(
        name="Height Float Curve", in_out="INPUT", socket_type="NodeSocketClosure"
    )

    input_node = nail_group.nodes.new("NodeGroupInput")
    input_node.label = "Inputs"

    output_node = nail_group.nodes.new("NodeGroupOutput")
    output_node.label = "Output"

    # === Axis Configuration ===
    if curl_direction == "X":
        length_axis_vec = (0, 0, 1)
        curl_axis_vec = (1, 0, 0)
        side_axis_vec = (0, 1, 0)
        length_idx, curl_idx, side_idx = 2, 0, 1
    elif curl_direction == "Y":
        length_axis_vec = (0, 0, 1)
        curl_axis_vec = (0, 1, 0)
        side_axis_vec = (1, 0, 0)
        length_idx, curl_idx, side_idx = 2, 1, 0
    else:  # "Z"
        length_axis_vec = (0, 1, 0)
        curl_axis_vec = (0, 0, 1)
        side_axis_vec = (1, 0, 0)
        length_idx, curl_idx, side_idx = 1, 2, 0

    # === Bounding Box for Segment ===
    bounding_box = nail_group.nodes.new("GeometryNodeBoundBox")
    bounding_box.label = "Segment Bounds"
    nail_group.links.new(
        input_node.outputs["Geometry"], bounding_box.inputs["Geometry"]
    )

    sep_bbox = nail_group.nodes.new("ShaderNodeSeparateXYZ")
    sep_bbox.label = "Max XYZ"
    nail_group.links.new(bounding_box.outputs["Max"], sep_bbox.inputs["Vector"])

    sep_bbox_min = nail_group.nodes.new("ShaderNodeSeparateXYZ")
    sep_bbox_min.label = "Min XYZ"
    nail_group.links.new(bounding_box.outputs["Min"], sep_bbox_min.inputs["Vector"])

    # === Calculate sample Z position based on Attachment Position ===
    seg_length = nail_group.nodes.new("ShaderNodeMath")
    seg_length.label = "Segment Length"
    seg_length.operation = "SUBTRACT"
    nail_group.links.new(sep_bbox.outputs["Z"], seg_length.inputs[0])
    nail_group.links.new(sep_bbox_min.outputs["Z"], seg_length.inputs[1])

    sample_z = nail_group.nodes.new("ShaderNodeMath")
    sample_z.label = "Sample Z"
    sample_z.operation = "MULTIPLY_ADD"
    nail_group.links.new(seg_length.outputs["Value"], sample_z.inputs[0])
    nail_group.links.new(input_node.outputs["Attachment Position"], sample_z.inputs[1])
    nail_group.links.new(sep_bbox_min.outputs["Z"], sample_z.inputs[2])

    # === Raycast to measure segment radius ===
    radius_ray_origin = nail_group.nodes.new("ShaderNodeCombineXYZ")
    radius_ray_origin.label = "Radius Ray Origin"
    radius_ray_origin.inputs["X"].default_value = 100.0
    radius_ray_origin.inputs["Y"].default_value = 0.0
    nail_group.links.new(sample_z.outputs["Value"], radius_ray_origin.inputs["Z"])

    radius_raycast = nail_group.nodes.new("GeometryNodeRaycast")
    radius_raycast.label = "Measure Radius"
    radius_raycast.inputs["Ray Direction"].default_value = (-1.0, 0.0, 0.0)
    radius_raycast.inputs["Ray Length"].default_value = 200.0
    nail_group.links.new(
        input_node.outputs["Geometry"], radius_raycast.inputs["Target Geometry"]
    )
    nail_group.links.new(
        radius_ray_origin.outputs["Vector"], radius_raycast.inputs["Source Position"]
    )

    radius_hit_sep = nail_group.nodes.new("ShaderNodeSeparateXYZ")
    radius_hit_sep.label = "Hit Position"
    nail_group.links.new(
        radius_raycast.outputs["Hit Position"], radius_hit_sep.inputs["Vector"]
    )

    segment_radius = nail_group.nodes.new("ShaderNodeMath")
    segment_radius.label = "Segment Radius"
    segment_radius.operation = "ABSOLUTE"
    nail_group.links.new(radius_hit_sep.outputs["X"], segment_radius.inputs[0])

    # === Calculate dimensions ===
    # Width = segment_radius * width_ratio
    width_calc = nail_group.nodes.new("ShaderNodeMath")
    width_calc.label = "Nail Width"
    width_calc.operation = "MULTIPLY"
    nail_group.links.new(segment_radius.outputs["Value"], width_calc.inputs[0])
    nail_group.links.new(input_node.outputs["Nail Width Ratio"], width_calc.inputs[1])

    # Height = segment_radius * width_ratio (same as width for now)
    height_calc = nail_group.nodes.new("ShaderNodeMath")
    height_calc.label = "Nail Height"
    height_calc.operation = "MULTIPLY"
    nail_group.links.new(segment_radius.outputs["Value"], height_calc.inputs[0])
    nail_group.links.new(input_node.outputs["Nail Width Ratio"], height_calc.inputs[1])

    # === Target position for nail placement ===
    target_length_pos = nail_group.nodes.new("ShaderNodeMath")
    target_length_pos.label = "Target Length Pos"
    target_length_pos.operation = "SUBTRACT"
    nail_group.links.new(sample_z.outputs["Value"], target_length_pos.inputs[0])

    half_height = nail_group.nodes.new("ShaderNodeMath")
    half_height.label = "Half Height"
    half_height.operation = "MULTIPLY"
    half_height.inputs[1].default_value = 0.5
    nail_group.links.new(height_calc.outputs["Value"], half_height.inputs[0])

    nail_group.links.new(half_height.outputs["Value"], target_length_pos.inputs[1])

    base_pos_combine = nail_group.nodes.new("ShaderNodeCombineXYZ")
    base_pos_combine.label = "Base Position"
    if length_idx == 0:
        nail_group.links.new(
            target_length_pos.outputs["Value"], base_pos_combine.inputs["X"]
        )
    elif length_idx == 1:
        nail_group.links.new(
            target_length_pos.outputs["Value"], base_pos_combine.inputs["Y"]
        )
    elif length_idx == 2:
        nail_group.links.new(
            target_length_pos.outputs["Value"], base_pos_combine.inputs["Z"]
        )

    # === Raycast to find surface position ===
    offset_dist = nail_group.nodes.new("ShaderNodeMath")
    offset_dist.label = "Offset Distance"
    offset_dist.operation = "MULTIPLY"
    offset_dist.inputs[1].default_value = 2.0
    nail_group.links.new(segment_radius.outputs["Value"], offset_dist.inputs[0])

    offset_vec = nail_group.nodes.new("ShaderNodeCombineXYZ")
    offset_vec.label = "Curl Axis"
    offset_vec.inputs[0].default_value = curl_axis_vec[0]
    offset_vec.inputs[1].default_value = curl_axis_vec[1]
    offset_vec.inputs[2].default_value = curl_axis_vec[2]

    offset_scaled = nail_group.nodes.new("ShaderNodeVectorMath")
    offset_scaled.label = "Offset Scaled"
    offset_scaled.operation = "SCALE"
    nail_group.links.new(offset_vec.outputs["Vector"], offset_scaled.inputs[0])
    nail_group.links.new(offset_dist.outputs["Value"], offset_scaled.inputs[3])

    ray_start = nail_group.nodes.new("ShaderNodeVectorMath")
    ray_start.label = "Ray Start"
    ray_start.operation = "ADD"
    nail_group.links.new(base_pos_combine.outputs["Vector"], ray_start.inputs[0])
    nail_group.links.new(offset_scaled.outputs["Vector"], ray_start.inputs[1])

    ray_dir = nail_group.nodes.new("ShaderNodeVectorMath")
    ray_dir.label = "Ray Direction"
    ray_dir.operation = "SCALE"
    ray_dir.inputs[0].default_value = curl_axis_vec
    ray_dir.inputs[3].default_value = -1.0

    raycast = nail_group.nodes.new("GeometryNodeRaycast")
    raycast.label = "Surface Raycast"
    nail_group.links.new(
        input_node.outputs["Geometry"], raycast.inputs["Target Geometry"]
    )
    nail_group.links.new(ray_start.outputs["Vector"], raycast.inputs["Source Position"])
    nail_group.links.new(ray_dir.outputs["Vector"], raycast.inputs["Ray Direction"])

    # === Create Mesh Grid for angular wedge ===
    # Grid X = angle parameter (0 to wrap_amount), Grid Y = length parameter
    grid = nail_group.nodes.new("GeometryNodeMeshGrid")
    grid.label = "Attachment Grid"
    grid.inputs["Vertices X"].default_value = SEGMENT_SAMPLE_COUNT
    grid.inputs["Vertices Y"].default_value = SEGMENT_SAMPLE_COUNT
    grid.inputs["Size X"].default_value = 1.0
    grid.inputs["Size Y"].default_value = 1.0

    grid_pos = nail_group.nodes.new("GeometryNodeInputPosition")
    grid_pos.label = "Grid Position"

    sep_grid = nail_group.nodes.new("ShaderNodeSeparateXYZ")
    sep_grid.label = "Grid XY"
    nail_group.links.new(grid_pos.outputs["Position"], sep_grid.inputs["Vector"])

    # === Angle parameter: map grid X (-0.5 to 0.5) to angle (0 to wrap_amount) ===
    angle_param = nail_group.nodes.new("ShaderNodeMath")
    angle_param.label = "Angle Param 0-1"
    angle_param.operation = "ADD"
    angle_param.inputs[1].default_value = 0.5
    nail_group.links.new(sep_grid.outputs["X"], angle_param.inputs[0])

    angle_clamp = nail_group.nodes.new("ShaderNodeClamp")
    angle_clamp.label = "Clamp Angle"
    nail_group.links.new(angle_param.outputs["Value"], angle_clamp.inputs["Value"])

    # Evaluate Angle Float Curve to shape thickness based on angle
    evaluate_angle_curve = nail_group.nodes.new("NodeEvaluateClosure")
    evaluate_angle_curve.label = "Evaluate Angle Curve"
    evaluate_angle_curve.define_signature = True
    evaluate_angle_curve.input_items.new(socket_type='FLOAT', name="Value")
    evaluate_angle_curve.output_items.new(socket_type='FLOAT', name="Value")
    nail_group.links.new(
        input_node.outputs["Angle Float Curve"],
        evaluate_angle_curve.inputs["Closure"]
    )
    nail_group.links.new(angle_clamp.outputs["Result"], evaluate_angle_curve.inputs["Value"])

    # Map angle param to actual angle: angle = (param - 0.5) * wrap_amount
    # This centers the wrap around the curl axis
    angle_centered = nail_group.nodes.new("ShaderNodeMath")
    angle_centered.label = "Center Angle"
    angle_centered.operation = "SUBTRACT"
    angle_centered.inputs[1].default_value = 0.5
    nail_group.links.new(angle_clamp.outputs["Result"], angle_centered.inputs[0])

    angle_scaled = nail_group.nodes.new("ShaderNodeMath")
    angle_scaled.label = "Scale to Wrap"
    angle_scaled.operation = "MULTIPLY"
    nail_group.links.new(angle_centered.outputs["Value"], angle_scaled.inputs[0])
    nail_group.links.new(input_node.outputs["Wrap Amount"], angle_scaled.inputs[1])

    # === Length parameter: map grid Y to 0-1 ===
    length_param = nail_group.nodes.new("ShaderNodeMath")
    length_param.label = "Length Param 0-1"
    length_param.operation = "ADD"
    length_param.inputs[1].default_value = 0.5
    nail_group.links.new(sep_grid.outputs["Y"], length_param.inputs[0])

    length_clamp = nail_group.nodes.new("ShaderNodeClamp")
    length_clamp.label = "Clamp Length"
    nail_group.links.new(length_param.outputs["Value"], length_clamp.inputs["Value"])

    # === Evaluate Height Float Curve per-vertex (along nail height) ===
    # The height curve modulates thickness based on position along the nail's length
    evaluate_height_curve = nail_group.nodes.new("NodeEvaluateClosure")
    evaluate_height_curve.label = "Evaluate Height Curve"
    evaluate_height_curve.define_signature = True
    evaluate_height_curve.input_items.new(socket_type='FLOAT', name="Value")
    evaluate_height_curve.output_items.new(socket_type='FLOAT', name="Value")
    nail_group.links.new(
        input_node.outputs["Height Float Curve"],
        evaluate_height_curve.inputs["Closure"]
    )
    # Use length_clamp (grid Y parameter 0-1) for per-vertex evaluation
    nail_group.links.new(
        length_clamp.outputs["Result"],
        evaluate_height_curve.inputs["Value"]
    )

    # === Calculate radial position (wedge around curl axis) ===
    cos_angle = nail_group.nodes.new("ShaderNodeMath")
    cos_angle.label = "cos(angle)"
    cos_angle.operation = "COSINE"
    nail_group.links.new(angle_scaled.outputs["Value"], cos_angle.inputs[0])

    sin_angle = nail_group.nodes.new("ShaderNodeMath")
    sin_angle.label = "sin(angle)"
    sin_angle.operation = "SINE"
    nail_group.links.new(angle_scaled.outputs["Value"], sin_angle.inputs[0])

    # === Per-vertex thickness = max_thickness * height_curve(length) * angle_curve(angle) ===
    # Thickness modulated by height curve (per-vertex along nail length)
    thickness_from_height = nail_group.nodes.new("ShaderNodeMath")
    thickness_from_height.label = "Thickness from Height"
    thickness_from_height.operation = "MULTIPLY"
    nail_group.links.new(input_node.outputs["Max Thickness"], thickness_from_height.inputs[0])
    nail_group.links.new(evaluate_height_curve.outputs["Value"], thickness_from_height.inputs[1])

    # Final thickness modulated by angle curve
    thickness_modulated = nail_group.nodes.new("ShaderNodeMath")
    thickness_modulated.label = "Thickness Modulated"
    thickness_modulated.operation = "MULTIPLY"
    nail_group.links.new(thickness_from_height.outputs["Value"], thickness_modulated.inputs[0])
    nail_group.links.new(evaluate_angle_curve.outputs["Value"], thickness_modulated.inputs[1])

    # Radial distance = segment_radius + thickness * (1 + some offset)
    radial_offset = nail_group.nodes.new("ShaderNodeMath")
    radial_offset.label = "Radial Offset"
    radial_offset.operation = "MULTIPLY"
    radial_offset.inputs[1].default_value = OFFSET_RATIO
    nail_group.links.new(segment_radius.outputs["Value"], radial_offset.inputs[0])

    radial_dist = nail_group.nodes.new("ShaderNodeMath")
    radial_dist.label = "Radial Distance"
    radial_dist.operation = "ADD"
    nail_group.links.new(segment_radius.outputs["Value"], radial_dist.inputs[0])
    nail_group.links.new(radial_offset.outputs["Value"], radial_dist.inputs[1])

    # Add thickness modulation
    radial_with_thickness = nail_group.nodes.new("ShaderNodeMath")
    radial_with_thickness.label = "Radial + Thickness"
    radial_with_thickness.operation = "ADD"
    nail_group.links.new(radial_dist.outputs["Value"], radial_with_thickness.inputs[0])
    nail_group.links.new(thickness_modulated.outputs["Value"], radial_with_thickness.inputs[1])

    # === Calculate position for each grid point ===
    # The position is: (radial * cos(angle), radial * sin(angle), z_along_height)
    # But we need to map this to the correct axes based on curl direction
    
    # X component (based on side axis for curl direction)
    x_component = nail_group.nodes.new("ShaderNodeMath")
    x_component.label = "X Component"
    x_component.operation = "MULTIPLY"
    nail_group.links.new(radial_with_thickness.outputs["Value"], x_component.inputs[0])
    nail_group.links.new(cos_angle.outputs["Value"], x_component.inputs[1])

    # Y component (based on curl axis depth - the thickness direction)
    y_component = nail_group.nodes.new("ShaderNodeMath")
    y_component.label = "Y Component"  
    y_component.operation = "MULTIPLY"
    nail_group.links.new(radial_with_thickness.outputs["Value"], y_component.inputs[0])
    nail_group.links.new(sin_angle.outputs["Value"], y_component.inputs[1])

    # Z component (along length axis) = sample_z + length_param * height
    z_offset = nail_group.nodes.new("ShaderNodeMath")
    z_offset.label = "Z Offset"
    z_offset.operation = "MULTIPLY"
    nail_group.links.new(length_clamp.outputs["Result"], z_offset.inputs[0])
    nail_group.links.new(height_calc.outputs["Value"], z_offset.inputs[1])

    z_component = nail_group.nodes.new("ShaderNodeMath")
    z_component.label = "Z Component"
    z_component.operation = "ADD"
    nail_group.links.new(sample_z.outputs["Value"], z_component.inputs[0])
    nail_group.links.new(z_offset.outputs["Value"], z_component.inputs[1])

    # Combine into final position (map to correct axes based on curl direction)
    final_pos_combine = nail_group.nodes.new("ShaderNodeCombineXYZ")
    final_pos_combine.label = "Final Position"

    # Map components to axes based on curl direction:
    # curl_idx = thickness/depth direction (uses sin_angle component)
    # side_idx = width direction (uses cos_angle component)
    # length_idx = height direction (uses z_component)
    
    if curl_direction == "X":
        # curl=X, side=Y, length=Z
        nail_group.links.new(y_component.outputs["Value"], final_pos_combine.inputs["X"])
        nail_group.links.new(x_component.outputs["Value"], final_pos_combine.inputs["Y"])
        nail_group.links.new(z_component.outputs["Value"], final_pos_combine.inputs["Z"])
    elif curl_direction == "Y":
        # curl=Y, side=X, length=Z
        nail_group.links.new(x_component.outputs["Value"], final_pos_combine.inputs["X"])
        nail_group.links.new(y_component.outputs["Value"], final_pos_combine.inputs["Y"])
        nail_group.links.new(z_component.outputs["Value"], final_pos_combine.inputs["Z"])
    else:  # "Z"
        # curl=Z, side=X, length=Y
        nail_group.links.new(x_component.outputs["Value"], final_pos_combine.inputs["X"])
        nail_group.links.new(z_component.outputs["Value"], final_pos_combine.inputs["Y"])
        nail_group.links.new(y_component.outputs["Value"], final_pos_combine.inputs["Z"])

    # === Apply position to grid ===
    set_position = nail_group.nodes.new("GeometryNodeSetPosition")
    set_position.label = "Apply Position"
    nail_group.links.new(grid.outputs["Mesh"], set_position.inputs["Geometry"])
    nail_group.links.new(final_pos_combine.outputs["Vector"], set_position.inputs["Position"])

    # === Join with input geometry ===
    join_geo = nail_group.nodes.new("GeometryNodeJoinGeometry")
    join_geo.label = "Join Geometry"
    nail_group.links.new(input_node.outputs["Geometry"], join_geo.inputs["Geometry"])
    nail_group.links.new(set_position.outputs["Geometry"], join_geo.inputs["Geometry"])

    nail_group.links.new(join_geo.outputs["Geometry"], output_node.inputs["Geometry"])

    # Auto-layout all nodes based on their connections
    auto_layout_nodes(nail_group)

    return nail_group
