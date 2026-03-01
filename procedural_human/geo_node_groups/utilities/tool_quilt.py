import math

from mathutils import Vector

from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.closures import create_float_curve_closure
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


def boolean_and(group, a, b):
    """Boolean AND of two boolean sockets."""
    n = group.nodes.new("FunctionNodeBooleanMath")
    n.operation = "AND"
    link_or_set(group, n.inputs[0], a)
    link_or_set(group, n.inputs[1], b)
    return n.outputs[0]


def boolean_not(group, a):
    """Boolean NOT of a boolean socket."""
    n = group.nodes.new("FunctionNodeBooleanMath")
    n.operation = "NOT"
    link_or_set(group, n.inputs[0], a)
    return n.outputs[0]


def field_at_index(group, domain, value, index):
    """Evaluate a field at a specific index.

    :param group: The node group.
    :param domain: Domain to evaluate in ("POINT", "EDGE", etc.).
    :param value: The field value to sample (socket).
    :param index: The index to evaluate at (socket).
    :returns: The sampled value output socket.
    """
    n = group.nodes.new("GeometryNodeFieldAtIndex")
    n.domain = domain
    link_or_set(group, n.inputs[0], value)
    link_or_set(group, n.inputs[1], index)
    return n.outputs[0]


def _build_closure_with_curve(nodes, links, label, points):
    """Create a closure zone with custom float curve control points.

    :param nodes: The node collection of the group.
    :param links: The link collection of the group.
    :param label: Label for the closure zone nodes.
    :param points: List of (x, y) tuples for the curve.
    :returns: FloatCurveClosure with the shaped curve.
    """
    closure = create_float_curve_closure(nodes, links, label, (0, 0))
    curve = closure.curve_node.mapping.curves[0]
    for i, (x, y) in enumerate(points):
        if i < 2:
            curve.points[i].location = (x, y)
        else:
            curve.points.new(x, y)
    closure.curve_node.mapping.update()
    return closure


def _evaluate_closure(group, closure_socket, input_socket):
    """Create a NodeEvaluateClosure wired to a closure and input value.

    :returns: The float output socket of the evaluation.
    """
    ev = group.nodes.new("NodeEvaluateClosure")
    ev.input_items.new("FLOAT", "Value")
    ev.output_items.new("FLOAT", "Value")
    ev.active_input_index = 0
    ev.active_output_index = 0
    ev.define_signature = False
    link_or_set(group, ev.inputs[0], closure_socket)
    link_or_set(group, ev.inputs[1], input_socket)
    return ev.outputs[0]


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
    group.interface.new_socket(name="Custom Depth Profile", in_out="INPUT", socket_type="NodeSocketBool")
    group.interface.new_socket(name="Edge Profile", in_out="INPUT", socket_type="NodeSocketClosure")
    group.interface.new_socket(name="Custom Edge Profile", in_out="INPUT", socket_type="NodeSocketBool")
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
    # [5]=DepthProfile, [6]=CustomDepthProfile, [7]=EdgeProfile, [8]=CustomEdgeProfile,
    # [9]=Subdivisions, [10]=Stitches, [11]=StitchSize
    scale_x_sock = group_input.outputs[1]
    scale_y_sock = group_input.outputs[2]
    depth_sock = group_input.outputs[3]
    rotation_sock = group_input.outputs[4]
    depth_profile_sock = group_input.outputs[5]
    custom_depth_toggle = group_input.outputs[6]
    edge_profile_sock = group_input.outputs[7]
    custom_edge_toggle = group_input.outputs[8]

    subdivide = nodes.new("GeometryNodeSubdivideMesh")
    links.new(group_input.outputs[0], subdivide.inputs[0])
    links.new(group_input.outputs[9], subdivide.inputs[1])

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

    # === Position along nearest edge ===
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

    # === Depth Profile ===
    # Internal default: concave pillow (0,0) → (0.42,0.54) → (1,0.78)
    depth_default = _build_closure_with_curve(nodes, links, "Depth Profile Default", [
        (0.0, 0.0),
        (1.0, 0.775),
        (0.423, 0.537),
    ])
    profile_internal = _evaluate_closure(
        group, depth_default.output_socket, captured_dist)
    profile_external = _evaluate_closure(
        group, depth_profile_sock, captured_dist)
    profile = switch_float(group, custom_depth_toggle,
        profile_internal, profile_external)

    # === Edge Profile ===
    # Internal default: V-shape — deep at corners, shallow at mid-edge
    # (0.005,1) → (0.5,0.51) → (1,1)
    edge_default = _build_closure_with_curve(nodes, links, "Edge Profile Default", [
        (0.005, 1.0),
        (1.0, 1.0),
        (0.505, 0.512),
    ])
    edge_internal = _evaluate_closure(
        group, edge_default.output_socket, captured_pos_along)
    edge_external = _evaluate_closure(
        group, edge_profile_sock, captured_pos_along)
    edge_factor = switch_float(group, custom_edge_toggle,
        edge_internal, edge_external)

    # === Displacement ===
    # edge_factor controls trench floor: 1 = deepest trench, 0 = no trench
    # displacement = depth * (1 - (1 - profile) * edge_factor)
    # At seam (profile=0): displacement = depth * (1 - edge_factor)
    # At center (profile=1): displacement = depth (always full height)
    inv_profile = math_op(group, "SUBTRACT", 1.0, profile)
    trench_factor = math_op(group, "MULTIPLY", inv_profile, edge_factor)
    blend = math_op(group, "SUBTRACT", 1.0, trench_factor)
    displacement = math_op(group, "MULTIPLY", depth_sock, blend)

    normal_for_offset = nodes.new("GeometryNodeInputNormal")
    offset_vec = vec_math_op(group, "SCALE", normal_for_offset.outputs[0], displacement)

    quilted = set_position(group, capture.outputs[0], True, None, offset_vec)

    # === Stitching via shortest path between cell corners ===
    # Adaptive thresholds: capture ~1-2 vertex rows per seam regardless of scale/subdivision
    bbox = nodes.new("GeometryNodeBoundBox")
    links.new(subdivide.outputs[0], bbox.inputs[0])
    y_axis = combine_xyz(group, 0.0, 1.0, 0.0)
    min_bx = math_op(group, "ABSOLUTE",
        vec_math_op(group, "DOT_PRODUCT", bbox.outputs[1], x_axis))
    min_by = math_op(group, "ABSOLUTE",
        vec_math_op(group, "DOT_PRODUCT", bbox.outputs[1], y_axis))
    min_bz = math_op(group, "ABSOLUTE",
        vec_math_op(group, "DOT_PRODUCT", bbox.outputs[1], z_axis))
    max_bx = math_op(group, "ABSOLUTE",
        vec_math_op(group, "DOT_PRODUCT", bbox.outputs[2], x_axis))
    max_by = math_op(group, "ABSOLUTE",
        vec_math_op(group, "DOT_PRODUCT", bbox.outputs[2], y_axis))
    max_bz = math_op(group, "ABSOLUTE",
        vec_math_op(group, "DOT_PRODUCT", bbox.outputs[2], z_axis))
    bbox_w = math_op(group, "ADD", min_bx, max_bx)
    bbox_h = math_op(group, "ADD", min_by, max_by)
    bbox_d = math_op(group, "ADD", min_bz, max_bz)
    max_dim = math_op(group, "MAXIMUM", bbox_w, math_op(group, "MAXIMUM", bbox_h, bbox_d))

    subdiv_power = math_op(group, "POWER", 2.0, group_input.outputs[9])
    vert_spacing = math_op(group, "DIVIDE", max_dim, subdiv_power)
    min_scale = math_op(group, "MINIMUM", scale_x_sock, scale_y_sock)
    norm_spacing = math_op(group, "MULTIPLY",
        math_op(group, "DIVIDE", vert_spacing, min_scale), 2.0)
    seam_thresh = math_op(group, "MULTIPLY", norm_spacing, 1.2)

    # Corner vertices: both dist_x and dist_y within adaptive threshold
    is_corner_x = compare_op(group, "LESS_THAN", "FLOAT", dist_x, seam_thresh)
    is_corner_y = compare_op(group, "LESS_THAN", "FLOAT", dist_y, seam_thresh)
    is_corner = boolean_and(group, is_corner_x, is_corner_y)

    on_seam = compare_op(group, "LESS_THAN", "FLOAT", dist, seam_thresh)
    start_verts = boolean_and(group, on_seam, boolean_not(group, is_corner))

    # Shortest paths toward nearest corner, edge cost = dist so paths prefer seam edges
    edge_cost = math_op(group, "ADD", dist, 0.001)
    shortest = nodes.new("GeometryNodeInputShortestEdgePaths")
    links.new(is_corner, shortest.inputs[0])
    links.new(edge_cost, shortest.inputs[1])

    paths_sel = nodes.new("GeometryNodeEdgePathsToSelection")
    links.new(start_verts, paths_sel.inputs[0])
    links.new(shortest.outputs[0], paths_sel.inputs[1])

    # Filter: keep edges where both endpoints are near seams (edge domain via FieldAtIndex)
    edge_verts = nodes.new("GeometryNodeInputMeshEdgeVertices")
    dist_v1 = field_at_index(group, "POINT", captured_dist, edge_verts.outputs[0])
    dist_v2 = field_at_index(group, "POINT", captured_dist, edge_verts.outputs[1])
    v1_near = compare_op(group, "LESS_THAN", "FLOAT", dist_v1, seam_thresh)
    v2_near = compare_op(group, "LESS_THAN", "FLOAT", dist_v2, seam_thresh)
    both_near = boolean_and(group, v1_near, v2_near)

    stitch_edge_sel = boolean_and(group, paths_sel.outputs[0], both_near)

    inv_stitch = boolean_not(group, stitch_edge_sel)
    delete_edges = nodes.new("GeometryNodeDeleteGeometry")
    delete_edges.mode = "ALL"
    delete_edges.domain = "EDGE"
    links.new(quilted, delete_edges.inputs[0])
    links.new(inv_stitch, delete_edges.inputs[1])

    merge_dist = math_op(group, "MULTIPLY", vert_spacing, 3.0)
    merge = nodes.new("GeometryNodeMergeByDistance")
    links.new(delete_edges.outputs[0], merge.inputs[0])
    merge.inputs[1].default_value = True
    merge.inputs[2].default_value = "All"
    link_or_set(group, merge.inputs[3], merge_dist)

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.inputs[1].default_value = True
    links.new(merge.outputs[0], mesh_to_curve.inputs[0])

    stitch_size_sock = group_input.outputs[11]
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
        group_input.outputs[10], quilted, join_geo.outputs[0])

    links.new(result, group_output.inputs[0])

    auto_layout_nodes(group)
    return group
