import bpy
from mathutils import Vector, Euler

from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.closures import create_flat_float_curve_closure
from procedural_human.geo_node_groups.node_helpers import (
    get_or_rebuild_node_group,
    link_or_set,
    math_op,
    vec_math_op,
    set_position,
    separate_xyz,
    combine_xyz,
    compare_op,
    switch_node,
    resample_curve,
)
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_quilting_group():
    group_name = "Quilting"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    sock = group.interface.new_socket(name="Scale X", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = 0.1
    sock.min_value = 0.001
    sock = group.interface.new_socket(name="Scale Y", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = 0.1
    sock.min_value = 0.001
    sock = group.interface.new_socket(name="Depth", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = 0.02
    sock = group.interface.new_socket(name="Rotation", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = 0.0
    sock.subtype = "ANGLE"
    sock = group.interface.new_socket(name="Subdivisions", in_out="INPUT", socket_type="NodeSocketInt")
    sock.default_value = 3
    sock.min_value = 0
    sock.max_value = 6
    group.interface.new_socket(name="Stitches", in_out="INPUT", socket_type="NodeSocketBool")
    sock = group.interface.new_socket(name="Stitch Size", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = 0.003

    nodes = group.nodes
    links = group.links

    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    # [0]=Geometry, [1]=ScaleX, [2]=ScaleY, [3]=Depth, [4]=Rotation,
    # [5]=Subdivisions, [6]=Stitches, [7]=StitchSize
    scale_x_sock = group_input.outputs[1]
    scale_y_sock = group_input.outputs[2]
    depth_sock = group_input.outputs[3]
    rotation_sock = group_input.outputs[4]

    subdivide = nodes.new("GeometryNodeSubdivideMesh")
    links.new(group_input.outputs[0], subdivide.inputs[0])
    links.new(group_input.outputs[5], subdivide.inputs[1])

    # === Generate internal grid from bounding box ===
    bbox = nodes.new("GeometryNodeBoundBox")
    bbox.inputs[1].default_value = True
    links.new(subdivide.outputs[0], bbox.inputs[0])

    min_x, min_y, min_z = separate_xyz(group, bbox.outputs[1])
    max_x, max_y, max_z = separate_xyz(group, bbox.outputs[2])

    width = math_op(group, "SUBTRACT", max_x, min_x)
    height = math_op(group, "SUBTRACT", max_y, min_y)
    center_x = math_op(group, "MULTIPLY", math_op(group, "ADD", min_x, max_x), 0.5)
    center_y = math_op(group, "MULTIPLY", math_op(group, "ADD", min_y, max_y), 0.5)

    # Grid resolution: enough cells to cover bbox + padding for rotation overshoot
    cells_x = math_op(group, "ADD",
        math_op(group, "FLOOR", math_op(group, "DIVIDE", width, scale_x_sock)), 6.0)
    cells_y = math_op(group, "ADD",
        math_op(group, "FLOOR", math_op(group, "DIVIDE", height, scale_y_sock)), 6.0)

    grid_size_x = math_op(group, "MULTIPLY", cells_x, scale_x_sock)
    grid_size_y = math_op(group, "MULTIPLY", cells_y, scale_y_sock)

    verts_x = math_op(group, "ADD", cells_x, 1.0)
    verts_y = math_op(group, "ADD", cells_y, 1.0)

    grid = nodes.new("GeometryNodeMeshGrid")
    link_or_set(group, grid.inputs[0], grid_size_x)
    link_or_set(group, grid.inputs[1], grid_size_y)
    link_or_set(group, grid.inputs[2], verts_x)
    link_or_set(group, grid.inputs[3], verts_y)

    delete_faces = nodes.new("GeometryNodeDeleteGeometry")
    delete_faces.domain = "FACE"
    delete_faces.mode = "ONLY_FACE"
    links.new(grid.outputs[0], delete_faces.inputs[0])
    delete_faces.inputs[1].default_value = True

    # Transform grid: rotate around Z, then translate to bbox center at bbox top
    grid_position = combine_xyz(group, center_x, center_y, max_z)

    axis_to_rot = nodes.new("FunctionNodeAxisAngleToRotation")
    axis_to_rot.inputs[0].default_value = Vector((0, 0, 1))
    links.new(rotation_sock, axis_to_rot.inputs[1])

    grid_transform = nodes.new("GeometryNodeTransform")
    grid_transform.inputs[1].default_value = "Components"
    links.new(delete_faces.outputs[0], grid_transform.inputs[0])
    link_or_set(group, grid_transform.inputs[2], grid_position)
    links.new(axis_to_rot.outputs[0], grid_transform.inputs[3])

    # === Proximity: distance from surface vertices to grid edges ===
    proximity = nodes.new("GeometryNodeProximity")
    proximity.target_element = "EDGES"
    links.new(grid_transform.outputs[0], proximity.inputs[0])

    # Normalize distance: [0, half_min_scale] → [0, 1] where 0=seam, 1=center
    half_min_scale = math_op(group, "MULTIPLY",
        math_op(group, "MINIMUM", scale_x_sock, scale_y_sock), 0.5)

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.clamp = True
    link_or_set(group, map_range.inputs[0], proximity.outputs[1])
    link_or_set(group, map_range.inputs[1], 0.0)
    link_or_set(group, map_range.inputs[2], half_min_scale)
    link_or_set(group, map_range.inputs[3], 0.0)
    link_or_set(group, map_range.inputs[4], 1.0)

    # Capture normalized distance for reuse in stitching
    capture = nodes.new("GeometryNodeCaptureAttribute")
    capture.active_index = 0
    capture.domain = "POINT"
    capture.capture_items.new("FLOAT", "Distance")
    links.new(subdivide.outputs[0], capture.inputs[0])
    links.new(map_range.outputs[0], capture.inputs[1])

    # === Pillow profile: puff = 1 - (1 - dist)^2 ===
    captured_dist = capture.outputs[1]
    inv_dist = math_op(group, "SUBTRACT", 1.0, captured_dist)
    inv_sq = math_op(group, "POWER", inv_dist, 2.0)
    puff = math_op(group, "SUBTRACT", 1.0, inv_sq)

    # === Internal depth curve closure ===
    # Flat at y=0: closure_eval=0, depth_multiplier=1-0=1 → full pillow.
    # User shapes the curve to reduce depth at specific distances from seam.
    depth_closure = create_flat_float_curve_closure(
        nodes, links, "Depth Profile", (0, 0), value=0.0)

    evaluate_closure = nodes.new("NodeEvaluateClosure")
    evaluate_closure.input_items.new("FLOAT", "Value")
    evaluate_closure.output_items.new("FLOAT", "Value")
    evaluate_closure.active_input_index = 0
    evaluate_closure.active_output_index = 0
    evaluate_closure.define_signature = False
    links.new(depth_closure.output_socket, evaluate_closure.inputs[0])
    links.new(captured_dist, evaluate_closure.inputs[1])

    depth_multiplier = math_op(group, "SUBTRACT", 1.0, evaluate_closure.outputs[0])
    displacement = math_op(group, "MULTIPLY",
        math_op(group, "MULTIPLY", puff, depth_multiplier), depth_sock)

    normal = nodes.new("GeometryNodeInputNormal")
    offset_vec = vec_math_op(group, "SCALE", normal.outputs[0], displacement)

    quilted = set_position(group, capture.outputs[0], True, None, offset_vec)

    # === Stitching (optional) ===
    far_sel = compare_op(group, "GREATER_THAN", "FLOAT", captured_dist, 0.08)

    delete_geo = nodes.new("GeometryNodeDeleteGeometry")
    delete_geo.mode = "ALL"
    delete_geo.domain = "POINT"
    links.new(quilted, delete_geo.inputs[0])
    links.new(far_sel, delete_geo.inputs[1])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.mode = "EDGES"
    mesh_to_curve.inputs[1].default_value = True
    links.new(delete_geo.outputs[0], mesh_to_curve.inputs[0])

    stitch_size_sock = group_input.outputs[7]
    stitch_spacing = math_op(group, "MULTIPLY", stitch_size_sock, 3.0)
    stitch_curves = resample_curve(
        group, True, mesh_to_curve.outputs[0], True, "Length", 10, stitch_spacing)

    ico = nodes.new("GeometryNodeMeshIcoSphere")
    ico.inputs[0].default_value = 1.0
    ico.inputs[1].default_value = 2

    stitch_shape = nodes.new("GeometryNodeTransform")
    stitch_shape.inputs[1].default_value = "Components"
    stitch_shape.inputs[4].default_value = Vector((1.5, 0.5, 0.32))
    links.new(ico.outputs[0], stitch_shape.inputs[0])

    tangent = nodes.new("GeometryNodeInputTangent")
    align_rot = nodes.new("FunctionNodeAlignRotationToVector")
    align_rot.axis = "X"
    align_rot.pivot_axis = "AUTO"
    align_rot.inputs[1].default_value = 1.0
    links.new(tangent.outputs[0], align_rot.inputs[2])

    instance_pts = nodes.new("GeometryNodeInstanceOnPoints")
    instance_pts.inputs[1].default_value = True
    instance_pts.inputs[3].default_value = False
    instance_pts.inputs[4].default_value = 0
    links.new(stitch_curves, instance_pts.inputs[0])
    links.new(stitch_shape.outputs[0], instance_pts.inputs[2])
    links.new(align_rot.outputs[0], instance_pts.inputs[5])

    stitch_scale = combine_xyz(group, stitch_size_sock, stitch_size_sock, stitch_size_sock)
    links.new(stitch_scale, instance_pts.inputs[6])

    realize = nodes.new("GeometryNodeRealizeInstances")
    realize.inputs[1].default_value = True
    realize.inputs[2].default_value = True
    realize.inputs[3].default_value = 0
    links.new(instance_pts.outputs[0], realize.inputs[0])

    join_geo = nodes.new("GeometryNodeJoinGeometry")
    links.new(realize.outputs[0], join_geo.inputs[0])
    links.new(quilted, join_geo.inputs[0])

    result = switch_node(group, "GEOMETRY",
        group_input.outputs[6], quilted, join_geo.outputs[0])

    links.new(result, group_output.inputs[0])

    auto_layout_nodes(group)
    return group
