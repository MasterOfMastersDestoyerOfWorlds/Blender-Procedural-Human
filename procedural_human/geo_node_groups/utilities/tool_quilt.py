import bpy
from mathutils import Vector, Euler

from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import (
    get_or_rebuild_node_group,
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
    sock = group.interface.new_socket(name="Scale", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = 0.1
    sock.min_value = 0.001
    sock = group.interface.new_socket(name="Depth", in_out="INPUT", socket_type="NodeSocketFloat")
    sock.default_value = 0.02
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

    # outputs[0]=Geometry, [1]=Scale, [2]=Depth, [3]=Subdivisions, [4]=Stitches, [5]=StitchSize
    scale_sock = group_input.outputs[1]
    depth_sock = group_input.outputs[2]

    subdivide = nodes.new("GeometryNodeSubdivideMesh")
    links.new(group_input.outputs[0], subdivide.inputs[0])
    links.new(group_input.outputs[3], subdivide.inputs[1])

    # === 3-axis procedural distance field ===
    # FRACT(pos/scale + 0.5) → cell position [0,1), half-scale offset prevents
    # axis-aligned faces from landing on grid planes.
    # MIN(cell, 1-cell)*2 → normalized distance to nearest cell boundary [0=seam, 1=center]
    position = nodes.new("GeometryNodeInputPosition")
    pos_x, pos_y, pos_z = separate_xyz(group, position.outputs[0])

    def axis_cell_dist(pos_component):
        cell = math_op(group, "FRACT",
            math_op(group, "ADD", math_op(group, "DIVIDE", pos_component, scale_sock), 0.5))
        return math_op(group, "MULTIPLY",
            math_op(group, "MINIMUM", cell, math_op(group, "SUBTRACT", 1.0, cell)),
            2.0)

    norm_x = axis_cell_dist(pos_x)
    norm_y = axis_cell_dist(pos_y)
    norm_z = axis_cell_dist(pos_z)

    dist = math_op(group, "MINIMUM", norm_x, math_op(group, "MINIMUM", norm_y, norm_z))

    capture = nodes.new("GeometryNodeCaptureAttribute")
    capture.active_index = 0
    capture.domain = "POINT"
    capture.capture_items.new("FLOAT", "Distance")
    links.new(subdivide.outputs[0], capture.inputs[0])
    links.new(dist, capture.inputs[1])

    # === Displacement: puff = 1 - (1 - dist)^2 ===
    # Rounded pillow profile: rises quickly from seam, flattens at center
    captured_dist = capture.outputs[1]
    inv_dist = math_op(group, "SUBTRACT", 1.0, captured_dist)
    inv_sq = math_op(group, "POWER", inv_dist, 2.0)
    puff = math_op(group, "SUBTRACT", 1.0, inv_sq)

    displacement = math_op(group, "MULTIPLY", puff, depth_sock)

    normal = nodes.new("GeometryNodeInputNormal")
    offset_vec = vec_math_op(group, "SCALE", normal.outputs[0], displacement)

    quilted = set_position(group, capture.outputs[0], True, None, offset_vec)

    # === Stitching (optional) ===
    # Keep only vertices near seams, convert to curves, instance stitch geometry
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

    stitch_size_sock = group_input.outputs[5]
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
        group_input.outputs[4], quilted, join_geo.outputs[0])

    links.new(result, group_output.inputs[0])

    auto_layout_nodes(group)
    return group
