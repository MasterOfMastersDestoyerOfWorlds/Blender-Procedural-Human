import math

import bpy

from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import (
    math_op, vec_math_op, create_node, link_or_set, get_or_rebuild_node_group
)


@geo_node_group
def create_segmentation_depth_loft_group():
    group_name = "Segmentation Depth Loft"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    socket = group.interface.new_socket(name="Resolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 1000
    socket.min_value = 2
    socket.max_value = 1000

    socket = group.interface.new_socket(name="SegmentationMask", in_out="INPUT", socket_type="NodeSocketImage")
    socket.default_value = None

    socket = group.interface.new_socket(name="DepthMask", in_out="INPUT", socket_type="NodeSocketImage")
    socket.default_value = None

    socket = group.interface.new_socket(name="OutlineMergeDistance", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.004
    socket.min_value = 0.0

    socket = group.interface.new_socket(name="MergeDistance", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.001
    socket.min_value = 0.0

    nodes = group.nodes
    links = group.links

    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    # --- Mask sampling ---
    position = nodes.new("GeometryNodeInputPosition")
    uv_offset = vec_math_op(group, "ADD", position.outputs[0], (0.5, 0.5, 0.0))

    image_texture = nodes.new("GeometryNodeImageTexture")
    image_texture.interpolation = "Linear"
    image_texture.extension = "REPEAT"
    image_texture.inputs[2].default_value = 0
    links.new(group_input.outputs[2], image_texture.inputs[0])  # SegmentationMask
    links.new(uv_offset, image_texture.inputs[1])

    separate_color = nodes.new("FunctionNodeSeparateColor")
    separate_color.mode = "RGB"
    links.new(image_texture.outputs[0], separate_color.inputs[0])

    # --- Grid creation ---
    grid = create_node(group, "GeometryNodeMeshGrid", {
        "Size X": 1.0,
        "Size Y": 1.0,
        "Vertices X": group_input.outputs[1],  # Resolution
        "Vertices Y": group_input.outputs[1]
    })

    # --- Delete points outside mask ---
    alpha_check = math_op(group, "LESS_THAN", separate_color.outputs[3], 0.1)

    delete_outside = create_node(group, "GeometryNodeDeleteGeometry", {
        "Geometry": grid.outputs[0],
        "Selection": alpha_check
    })
    delete_outside.mode = "ALL"
    delete_outside.domain = "POINT"

    # --- Delete interior edges ---
    edge_neighbors = nodes.new("GeometryNodeInputMeshEdgeNeighbors")

    compare_edge = create_node(group, "FunctionNodeCompare", {
        "Operation": "NOT_EQUAL",
        "Data Type": "INT"
    })
    compare_edge.mode = "ELEMENT"
    compare_edge.inputs[3].default_value = 1
    links.new(edge_neighbors.outputs[0], compare_edge.inputs[2])

    delete_interior = create_node(group, "GeometryNodeDeleteGeometry", {
        "Geometry": delete_outside.outputs[0],
        "Selection": compare_edge.outputs[0]
    })
    delete_interior.mode = "ALL"
    delete_interior.domain = "EDGE"

    # --- Mesh to curve and fill ---
    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.mode = "EDGES"
    mesh_to_curve.inputs[1].default_value = True
    links.new(delete_interior.outputs[0], mesh_to_curve.inputs[0])

    fill_curve = nodes.new("GeometryNodeFillCurve")
    fill_curve.inputs[1].default_value = 0
    fill_curve.inputs[2].default_value = "Triangles"
    links.new(mesh_to_curve.outputs[0], fill_curve.inputs[0])

    # --- Merge by distance (outline) ---
    merge_outline = create_node(group, "GeometryNodeMergeByDistance", {
        "Geometry": fill_curve.outputs[0],
        "Distance": group_input.outputs[4]  # OutlineMergeDistance
    })
    merge_outline.inputs[1].default_value = True
    merge_outline.inputs[2].default_value = "All"

    # --- Depth sampling ---
    position_depth = nodes.new("GeometryNodeInputPosition")
    uv_offset_depth = vec_math_op(group, "ADD", position_depth.outputs[0], (0.5, 0.5, 0.0))

    image_texture_depth = nodes.new("GeometryNodeImageTexture")
    image_texture_depth.interpolation = "Linear"
    image_texture_depth.extension = "REPEAT"
    image_texture_depth.inputs[2].default_value = 0
    links.new(group_input.outputs[3], image_texture_depth.inputs[0])  # DepthMask
    links.new(uv_offset_depth, image_texture_depth.inputs[1])

    separate_color_depth = nodes.new("FunctionNodeSeparateColor")
    separate_color_depth.mode = "RGB"
    links.new(image_texture_depth.outputs[0], separate_color_depth.inputs[0])

    # --- Average RGB for depth ---
    rgb_sum = math_op(group, "ADD",
        math_op(group, "ADD", separate_color_depth.outputs[0], separate_color_depth.outputs[1]),
        separate_color_depth.outputs[2]
    )
    depth_avg = math_op(group, "DIVIDE", rgb_sum, 3.0)
    depth_scaled = math_op(group, "MULTIPLY", depth_avg, 0.5)

    # --- Create Z offset vector ---
    combine_z = nodes.new("ShaderNodeCombineXYZ")
    combine_z.inputs[0].default_value = 0.0
    combine_z.inputs[1].default_value = 0.0
    links.new(depth_scaled, combine_z.inputs[2])

    # --- Set position (front mesh) ---
    set_pos_front = create_node(group, "GeometryNodeSetPosition", {
        "Geometry": merge_outline.outputs[0],
        "Offset": combine_z.outputs[0]
    })
    set_pos_front.inputs[1].default_value = True

    # --- Duplicate front for attribute statistic ---
    duplicate = create_node(group, "GeometryNodeDuplicateElements", {
        "Geometry": set_pos_front.outputs[0],
        "Amount": 1
    })
    duplicate.domain = "FACE"
    duplicate.inputs[1].default_value = True

    # --- Find max Z ---
    position_stat = nodes.new("GeometryNodeInputPosition")
    separate_stat = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_stat.outputs[0], separate_stat.inputs[0])

    attr_stat = create_node(group, "GeometryNodeAttributeStatistic", {
        "Geometry": duplicate.outputs[0],
        "Attribute": separate_stat.outputs[2]  # Z
    })
    attr_stat.data_type = "FLOAT"
    attr_stat.domain = "POINT"
    attr_stat.inputs[1].default_value = True

    # --- Extrude mesh ---
    vector_zero = nodes.new("FunctionNodeInputVector")
    vector_zero.vector = (0.0, 0.0, 0.0)

    extrude = create_node(group, "GeometryNodeExtrudeMesh", {
        "Mesh": set_pos_front.outputs[0],
        "Offset": vector_zero.outputs[0],
        "Offset Scale": 1.0
    })
    extrude.mode = "FACES"
    extrude.inputs[1].default_value = True
    extrude.inputs[4].default_value = False

    # --- Scale elements (invert Z on extruded faces) ---
    scale_invert = create_node(group, "GeometryNodeScaleElements", {
        "Geometry": extrude.outputs[0],
        "Selection": extrude.outputs[1],
        "Scale": -1.0,
        "Center": vector_zero.outputs[0]
    })
    scale_invert.domain = "FACE"
    scale_invert.inputs[4].default_value = "Single Axis"
    scale_invert.inputs[5].default_value = [0.0, 0.0, 1.0]

    # --- Offset back half by 2*maxZ ---
    max_z_scaled = vec_math_op(group, "SCALE", attr_stat.outputs[4], 2.0)

    combine_offset = nodes.new("ShaderNodeCombineXYZ")
    combine_offset.inputs[0].default_value = 0.0
    combine_offset.inputs[1].default_value = 0.0
    links.new(max_z_scaled, combine_offset.inputs[2])

    set_pos_back = create_node(group, "GeometryNodeSetPosition", {
        "Geometry": scale_invert.outputs[0],
        "Selection": extrude.outputs[1],
        "Offset": combine_offset.outputs[0]
    })

    # --- Join front and back ---
    join_geo = nodes.new("GeometryNodeJoinGeometry")
    links.new(duplicate.outputs[0], join_geo.inputs[0])
    links.new(set_pos_back.outputs[0], join_geo.inputs[0])

    # --- Final merge by distance ---
    merge_final = create_node(group, "GeometryNodeMergeByDistance", {
        "Geometry": join_geo.outputs[0],
        "Distance": group_input.outputs[5]  # MergeDistance
    })
    merge_final.inputs[1].default_value = True
    merge_final.inputs[2].default_value = "All"

    # --- Geometry to Instance ---
    geo_to_instance = nodes.new("GeometryNodeGeometryToInstance")
    links.new(merge_final.outputs[0], geo_to_instance.inputs[0])

    # --- Rotate Instances (X 90 degrees) ---
    rotate = create_node(group, "GeometryNodeRotateInstances", {
        "Instances": geo_to_instance.outputs[0],
        "Rotation": [math.radians(90), 0.0, 0.0],
        "Pivot Point": [0.0, 0.0, 0.0]
    })
    rotate.inputs[1].default_value = True
    rotate.inputs[4].default_value = True

    # --- Image aspect ratio scaling ---
    image_info = nodes.new("GeometryNodeImageInfo")
    image_info.inputs[1].default_value = 0
    links.new(group_input.outputs[2], image_info.inputs[0])  # SegmentationMask

    aspect_ratio = math_op(group, "DIVIDE", image_info.outputs[0], image_info.outputs[1])

    scale_aspect = create_node(group, "GeometryNodeScaleElements", {
        "Geometry": rotate.outputs[0],
        "Scale": aspect_ratio
    })
    scale_aspect.domain = "FACE"
    scale_aspect.inputs[1].default_value = True
    scale_aspect.inputs[3].default_value = [0.0, 0.0, 0.0]
    scale_aspect.inputs[4].default_value = "Single Axis"
    scale_aspect.inputs[5].default_value = [1.0, 0.0, 0.0]

    links.new(scale_aspect.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
