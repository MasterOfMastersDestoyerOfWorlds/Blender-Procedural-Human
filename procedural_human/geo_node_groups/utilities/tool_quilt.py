import math

import bpy
from mathutils import Vector

from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.closures import create_flat_float_curve_closure
from procedural_human.geo_node_groups.node_helpers import (
    get_or_rebuild_node_group,
    link_or_set,
    math_op,
    vec_math_op,
    set_position,
    combine_xyz,
    compare_op,
    switch_node,
    switch_float,
    switch_vec,
    resample_curve,
)
from procedural_human.utils.node_layout import auto_layout_nodes


def axis_cell_dist(group, coord, scale):
    """Compute normalized cell distance for one axis: 0 at seam, 1 at center.

    :param group: The node group.
    :param coord: Coordinate value in face-local rotated space (socket).
    :param scale: Cell size for this axis (socket or float).
    :returns: Output socket with distance 0..1.
    """
    divided = math_op(group, "DIVIDE", coord, scale)
    shifted = math_op(group, "ADD", divided, 0.5)
    cell = math_op(group, "FRACT", shifted)
    mirror = math_op(group, "SUBTRACT", 1.0, cell)
    half = math_op(group, "MINIMUM", cell, mirror)
    return math_op(group, "MULTIPLY", half, 2.0)


@geo_node_group
def create_quilting_group():
    group_name = "Quilting"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    sock = group.interface.new_socket(name="Scale X", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = 0.3
    sock.min_value = 0.001
    sock = group.interface.new_socket(name="Scale Y", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = 0.3
    sock.min_value = 0.001
    sock = group.interface.new_socket(name="Depth", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = 0.05
    sock = group.interface.new_socket(name="Rotation", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = math.radians(75)
    sock.subtype = "ANGLE"
    group.interface.new_socket(name="Depth Profile", in_out="INPUT", socket_type="NodeSocketClosure")
    sock = group.interface.new_socket(name="Subdivisions", in_out="INPUT", socket_type="NodeSocketInt")
    sock.default_value = 9
    sock.min_value = 0
    sock.max_value = 10
    group.interface.new_socket(name="Stitches", in_out="INPUT", socket_type="NodeSocketBool")
    sock = group.interface.new_socket(name="Stitch Size", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = 0.003

    nodes = group.nodes
    links = group.links

    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    # [0]=Geometry, [1]=ScaleX, [2]=ScaleY, [3]=Depth, [4]=Rotation,
    # [5]=DepthProfile(Closure), [6]=Subdivisions, [7]=Stitches, [8]=StitchSize
    scale_x_sock = group_input.outputs[1]
    scale_y_sock = group_input.outputs[2]
    depth_sock = group_input.outputs[3]
    rotation_sock = group_input.outputs[4]
    closure_sock = group_input.outputs[5]

    subdivide = nodes.new("GeometryNodeSubdivideMesh")
    links.new(group_input.outputs[0], subdivide.inputs[0])
    links.new(group_input.outputs[6], subdivide.inputs[1])

    # === Face-normal tangent frame ===
    face_normal = nodes.new("GeometryNodeInputNormal")
    position = nodes.new("GeometryNodeInputPosition")

    z_axis = combine_xyz(group, 0.0, 0.0, 1.0)
    x_axis = combine_xyz(group, 1.0, 0.0, 0.0)

    n_dot_z = vec_math_op(group, "DOT_PRODUCT", face_normal.outputs[0], z_axis)
    abs_n_dot_z = math_op(group, "ABSOLUTE", n_dot_z)
    is_z_aligned = compare_op(group, "GREATER_THAN", "FLOAT", abs_n_dot_z, 0.99)

    reference = switch_vec(group, is_z_aligned, z_axis, x_axis)

    t1_raw = vec_math_op(group, "CROSS_PRODUCT", face_normal.outputs[0], reference)
    t1 = vec_math_op(group, "NORMALIZE", t1_raw)
    t2 = vec_math_op(group, "CROSS_PRODUCT", face_normal.outputs[0], t1)

    local_u = vec_math_op(group, "DOT_PRODUCT", position.outputs[0], t1)
    local_v = vec_math_op(group, "DOT_PRODUCT", position.outputs[0], t2)

    # === Apply rotation in tangent plane ===
    cos_a = math_op(group, "COSINE", rotation_sock)
    sin_a = math_op(group, "SINE", rotation_sock)

    rotated_u = math_op(group, "SUBTRACT",
        math_op(group, "MULTIPLY", local_u, cos_a),
        math_op(group, "MULTIPLY", local_v, sin_a))
    rotated_v = math_op(group, "ADD",
        math_op(group, "MULTIPLY", local_u, sin_a),
        math_op(group, "MULTIPLY", local_v, cos_a))

    # === FRACT-based cell distance ===
    dist_x = axis_cell_dist(group, rotated_u, scale_x_sock)
    dist_y = axis_cell_dist(group, rotated_v, scale_y_sock)
    dist = math_op(group, "MINIMUM", dist_x, dist_y)

    # === Position along nearest edge (for edge profile closure) ===
    cell_x_frac = math_op(group, "FRACT",
        math_op(group, "ADD", math_op(group, "DIVIDE", rotated_u, scale_x_sock), 0.5))
    cell_y_frac = math_op(group, "FRACT",
        math_op(group, "ADD", math_op(group, "DIVIDE", rotated_v, scale_y_sock), 0.5))

    seam_dist_x = math_op(group, "MINIMUM", cell_x_frac,
        math_op(group, "SUBTRACT", 1.0, cell_x_frac))
    seam_dist_y = math_op(group, "MINIMUM", cell_y_frac,
        math_op(group, "SUBTRACT", 1.0, cell_y_frac))

    nearest_is_vertical = compare_op(group, "LESS_THAN", "FLOAT", seam_dist_x, seam_dist_y)
    pos_along = switch_float(group, nearest_is_vertical, cell_x_frac, cell_y_frac)

    # === Capture dist and pos_along for reuse ===
    capture = nodes.new("GeometryNodeCaptureAttribute")
    capture.active_index = 0
    capture.domain = "POINT"
    capture.capture_items.new("FLOAT", "Distance")
    capture.capture_items.new("FLOAT", "PosAlong")
    links.new(subdivide.outputs[0], capture.inputs[0])
    links.new(dist, capture.inputs[1])
    links.new(pos_along, capture.inputs[2])

    captured_dist = capture.outputs[1]
    captured_pos_along = capture.outputs[2]

    # === Radial profile via group input closure ===
    # Unconnected (identity): profile = dist → linear pillow
    # Connected with curve: profile = curve(dist) → custom shape
    evaluate_closure = nodes.new("NodeEvaluateClosure")
    evaluate_closure.input_items.new("FLOAT", "Value")
    evaluate_closure.output_items.new("FLOAT", "Value")
    evaluate_closure.active_input_index = 0
    evaluate_closure.active_output_index = 0
    evaluate_closure.define_signature = False
    links.new(closure_sock, evaluate_closure.inputs[0])
    links.new(captured_dist, evaluate_closure.inputs[1])

    profile = evaluate_closure.outputs[0]

    # === Edge profile via internal closure ===
    # Flat at y=1: edge_factor=1 everywhere → no modulation along seam.
    # User shapes curve: e.g. deep at corners (0,1 → 1.0), shallow at mid-edge (0.5 → 0.7)
    edge_closure = create_flat_float_curve_closure(
        nodes, links, "Edge Profile", (0, 0), value=1.0)

    eval_edge = nodes.new("NodeEvaluateClosure")
    eval_edge.input_items.new("FLOAT", "Value")
    eval_edge.output_items.new("FLOAT", "Value")
    eval_edge.active_input_index = 0
    eval_edge.active_output_index = 0
    eval_edge.define_signature = False
    links.new(edge_closure.output_socket, eval_edge.inputs[0])
    links.new(captured_pos_along, eval_edge.inputs[1])

    edge_factor = eval_edge.outputs[0]

    # === Final displacement ===
    # displacement = profile * edge_factor * depth, along face normal
    displacement = math_op(group, "MULTIPLY",
        math_op(group, "MULTIPLY", profile, edge_factor), depth_sock)

    normal_for_offset = nodes.new("GeometryNodeInputNormal")
    offset_vec = vec_math_op(group, "SCALE", normal_for_offset.outputs[0], displacement)

    quilted = set_position(group, capture.outputs[0], True, None, offset_vec)

    # === Stitching (optional) ===
    # Tight threshold to keep only vertices very close to seams
    far_sel = compare_op(group, "GREATER_THAN", "FLOAT", captured_dist, 0.02)

    delete_geo = nodes.new("GeometryNodeDeleteGeometry")
    delete_geo.mode = "ALL"
    delete_geo.domain = "POINT"
    links.new(quilted, delete_geo.inputs[0])
    links.new(far_sel, delete_geo.inputs[1])

    # Merge nearby vertices to collapse parallel edge rows into single lines
    merge = nodes.new("GeometryNodeMergeByDistance")
    links.new(delete_geo.outputs[0], merge.inputs[0])
    merge.inputs[1].default_value = True
    merge.inputs[2].default_value = "All"
    merge.inputs[3].default_value = 0.005

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.inputs[1].default_value = True
    links.new(merge.outputs[0], mesh_to_curve.inputs[0])

    stitch_size_sock = group_input.outputs[8]
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
        group_input.outputs[7], quilted, join_geo.outputs[0])

    links.new(result, group_output.inputs[0])

    auto_layout_nodes(group)
    return group
