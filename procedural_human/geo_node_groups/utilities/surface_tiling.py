"""Surface tiling primitives for quilting, masonry, herringbone, etc.

This module extracts common surface-tiling operations from tool_quilt.py into
reusable functions. These primitives form the foundation for any surface-tiling
pattern.
"""

from procedural_human.geo_node_groups.node_helpers import (
    combine_xyz,
    math_op,
    vec_math_op,
    switch_vec,
    compare_op,
)


def tangent_frame(group, face_normal, position):
    """Derive tangent frame (local_u, local_v) from face normal with singularity handling.

    Creates a local coordinate system on the surface using the face normal.
    Handles Z-aligned faces by using X as reference instead of Z to avoid
    numerical issues with cross product.

    :param group: The node group.
    :param face_normal: Face normal vector (socket or vector).
    :param position: Position vector (socket or vector).
    :returns: Tuple of (local_u, local_v) output sockets.
    """
    z_axis = combine_xyz(group, 0.0, 0.0, 1.0)
    x_axis = combine_xyz(group, 1.0, 0.0, 0.0)

    n_dot_z = vec_math_op(group, "DOT_PRODUCT", face_normal, z_axis)
    abs_n_dot_z = math_op(group, "ABSOLUTE", n_dot_z)
    is_z_aligned = compare_op(group, "GREATER_THAN", "FLOAT", abs_n_dot_z, 0.99)

    reference = switch_vec(group, is_z_aligned, z_axis, x_axis)

    t1_raw = vec_math_op(group, "CROSS_PRODUCT", face_normal, reference)
    t1 = vec_math_op(group, "NORMALIZE", t1_raw)
    t2 = vec_math_op(group, "CROSS_PRODUCT", face_normal, t1)

    local_u = vec_math_op(group, "DOT_PRODUCT", position, t1)
    local_v = vec_math_op(group, "DOT_PRODUCT", position, t2)

    return local_u, local_v


def axis_cell_dist(group, coord, scale, offset=0.0):
    """Compute normalized cell distance for one axis: 0 at seam, 1 at center.

    Uses FRACT-based grid math to compute distance from nearest seam.
    Optional offset allows for running bond patterns (e.g., masonry).

    :param group: The node group.
    :param coord: Coordinate value in face-local rotated space (socket).
    :param scale: Cell size for this axis (socket or float).
    :param offset: Optional offset for running bond patterns (default: 0.0).
    :returns: Output socket with distance 0..1.
    """
    divided = math_op(group, "DIVIDE", coord, scale)
    shifted = math_op(group, "ADD", divided, offset + 0.5)
    cell = math_op(group, "FRACT", shifted)
    mirror = math_op(group, "SUBTRACT", 1.0, cell)
    half = math_op(group, "MINIMUM", cell, mirror)
    return math_op(group, "MULTIPLY", half, 2.0)


def face_local_rotation(group, u, v, angle):
    """Apply rotation in the face-local tangent plane.

    Applies 2D rotation using cos/sin to local_u and local_v coordinates.

    :param group: The node group.
    :param u: Local u coordinate (socket).
    :param v: Local v coordinate (socket).
    :param angle: Rotation angle in radians (socket or float).
    :returns: Tuple of (rotated_u, rotated_v) output sockets.
    """
    cos_a = math_op(group, "COSINE", angle)
    sin_a = math_op(group, "SINE", angle)

    rotated_u = math_op(group, "SUBTRACT",
        math_op(group, "MULTIPLY", u, cos_a),
        math_op(group, "MULTIPLY", v, sin_a))
    rotated_v = math_op(group, "ADD",
        math_op(group, "MULTIPLY", u, sin_a),
        math_op(group, "MULTIPLY", v, cos_a))

    return rotated_u, rotated_v
