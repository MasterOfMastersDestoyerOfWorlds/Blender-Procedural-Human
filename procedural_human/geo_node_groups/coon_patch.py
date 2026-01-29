import bpy
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import (
    math_op, vec_math_op, get_attr, smoother_step, link_or_set, create_node
)


@geo_node_group
def create_coons_patch_group():
    group_name = "CoonsPatchGenerator"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Subdivisions", in_out="INPUT", socket_type="NodeSocketInt").default_value = 4
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links

    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    corner_idx_node = nodes.new("GeometryNodeInputIndex")
    face_of_corner = nodes.new("GeometryNodeFaceOfCorner")
    links.new(corner_idx_node.outputs[0], face_of_corner.inputs["Corner Index"])
    face_idx = face_of_corner.outputs["Face Index"]
    corners_lookup_0 = nodes.new("GeometryNodeCornersOfFace")
    links.new(face_idx, corners_lookup_0.inputs["Face Index"])
    corners_lookup_0.inputs["Sort Index"].default_value = 0
    first_corner_idx = corners_lookup_0.outputs["Corner Index"]
    sort_idx = math_op(group, 'SUBTRACT', corner_idx_node.outputs[0], first_corner_idx)

    op_eq1 = math_op(group, 'COMPARE', sort_idx, 1.0)
    op_eq2 = math_op(group, 'COMPARE', sort_idx, 2.0)
    op_eq3 = math_op(group, 'COMPARE', sort_idx, 3.0)

    u_val = math_op(group, 'ADD', op_eq1, op_eq2)
    v_val = math_op(group, 'ADD', op_eq2, op_eq3)

    uv_combine = nodes.new("ShaderNodeCombineXYZ")
    links.new(u_val, uv_combine.inputs[0])
    links.new(v_val, uv_combine.inputs[1])

    store_uv = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Geometry": group_input.outputs[0],
        "Name": "patch_uv",
        "Domain": "CORNER",
        "Data Type": "FLOAT_VECTOR",
        "Value": uv_combine.outputs[0]
    })

    edges_of_corner = nodes.new("GeometryNodeEdgesOfCorner")
    edge_idx_at_corner = edges_of_corner.outputs["Next Edge Index"]

    store_edge_indices = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Geometry": store_uv.outputs[0],
        "Name": "corner_edge_idx",
        "Domain": "CORNER",
        "Data Type": "INT",
        "Value": edge_idx_at_corner
    })

    vertex_of_corner = nodes.new("GeometryNodeVertexOfCorner")
    edge_verts_node = nodes.new("GeometryNodeInputMeshEdgeVertices")

    sample_edge_vert1 = create_node(group, "GeometryNodeSampleIndex", {
        "Geometry": store_edge_indices.outputs[0],
        "Domain": "EDGE",
        "Data Type": "INT",
        "Index": edge_idx_at_corner,
        "Value": edge_verts_node.outputs["Vertex Index 1"]
    })

    is_fwd_cmp = create_node(group, "FunctionNodeCompare", {
        "Data Type": "INT",
        "Operation": "EQUAL"
    })
    links.new(vertex_of_corner.outputs["Vertex Index"], is_fwd_cmp.inputs["A"])
    links.new(sample_edge_vert1.outputs[0], is_fwd_cmp.inputs["B"])
    is_forward = is_fwd_cmp.outputs["Result"]

    store_direction = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Geometry": store_edge_indices.outputs[0],
        "Name": "edge_is_forward",
        "Domain": "CORNER",
        "Data Type": "BOOLEAN",
        "Value": is_forward
    })

    def get_data_from_corner_sort_id(geo_link, sort_id_val, attr_name, dtype='INT'):
        face_idx_node_inner = nodes.new("GeometryNodeInputIndex")
        c_lookup = nodes.new("GeometryNodeCornersOfFace")
        links.new(face_idx_node_inner.outputs[0], c_lookup.inputs["Face Index"])
        c_lookup.inputs["Sort Index"].default_value = sort_id_val
        target_corner = c_lookup.outputs["Corner Index"]

        read_attr = nodes.new("GeometryNodeInputNamedAttribute")
        read_attr.data_type = dtype
        read_attr.inputs["Name"].default_value = attr_name

        samp = create_node(group, "GeometryNodeSampleIndex", {
            "Geometry": geo_link,
            "Domain": "CORNER",
            "Data Type": dtype,
            "Index": target_corner,
            "Value": read_attr.outputs[0]
        })
        return samp.outputs[0]

    def store_face_attr(geo, name, val, dtype='INT'):
        s = create_node(group, "GeometryNodeStoreNamedAttribute", {
            "Geometry": geo,
            "Name": name,
            "Domain": "FACE",
            "Data Type": dtype,
            "Value": val
        })
        return s.outputs[0]

    geo = store_direction.outputs[0]
    geo = store_face_attr(geo, "e0", get_data_from_corner_sort_id(geo, 0, "corner_edge_idx"))
    geo = store_face_attr(geo, "e1", get_data_from_corner_sort_id(geo, 1, "corner_edge_idx"))
    geo = store_face_attr(geo, "e2", get_data_from_corner_sort_id(geo, 2, "corner_edge_idx"))
    geo = store_face_attr(geo, "e3", get_data_from_corner_sort_id(geo, 3, "corner_edge_idx"))

    geo = store_face_attr(geo, "d0", get_data_from_corner_sort_id(geo, 0, "edge_is_forward", 'BOOLEAN'), 'BOOLEAN')
    geo = store_face_attr(geo, "d1", get_data_from_corner_sort_id(geo, 1, "edge_is_forward", 'BOOLEAN'), 'BOOLEAN')
    geo = store_face_attr(geo, "d2", get_data_from_corner_sort_id(geo, 2, "edge_is_forward", 'BOOLEAN'), 'BOOLEAN')
    geo = store_face_attr(geo, "d3", get_data_from_corner_sort_id(geo, 3, "edge_is_forward", 'BOOLEAN'), 'BOOLEAN')

    split_edges = create_node(group, "GeometryNodeSplitEdges", {"Mesh": geo})

    subdiv = create_node(group, "GeometryNodeSubdivideMesh", {
        "Mesh": split_edges.outputs[0],
        "Level": group_input.outputs["Subdivisions"]
    })
    subdivided_geo = subdiv.outputs[0]

    get_uv = nodes.new("GeometryNodeInputNamedAttribute")
    get_uv.data_type = 'FLOAT_VECTOR'
    get_uv.inputs["Name"].default_value = "patch_uv"
    sep_uv = nodes.new("ShaderNodeSeparateXYZ")
    links.new(get_uv.outputs[0], sep_uv.inputs[0])
    u_raw = sep_uv.outputs["X"]
    v_raw = sep_uv.outputs["Y"]

    u_smooth = smoother_step(group, u_raw)
    v_smooth = smoother_step(group, v_raw)

    def eval_bezier_curve(geo_ref, edge_idx_field, is_fwd_field, t_field, original_geometry):
        def sample_edge(attr_name, dtype='FLOAT_VECTOR'):
            inp = nodes.new("GeometryNodeInputNamedAttribute")
            inp.data_type = dtype
            inp.inputs["Name"].default_value = attr_name
            s = create_node(group, "GeometryNodeSampleIndex", {
                "Geometry": original_geometry,
                "Domain": "EDGE",
                "Data Type": dtype,
                "Index": edge_idx_field,
                "Value": inp.outputs[0]
            })
            return s.outputs[0]

        def get_vert_pos(v_socket_idx):
            ev = nodes.new("GeometryNodeInputMeshEdgeVertices")
            s_verts = create_node(group, "GeometryNodeSampleIndex", {
                "Geometry": original_geometry,
                "Domain": "EDGE",
                "Data Type": "INT",
                "Index": edge_idx_field,
                "Value": ev.outputs[v_socket_idx]
            })

            pos_node = nodes.new("GeometryNodeInputPosition")
            s_pos = create_node(group, "GeometryNodeSampleIndex", {
                "Geometry": original_geometry,
                "Domain": "POINT",
                "Data Type": "FLOAT_VECTOR",
                "Index": s_verts.outputs[0],
                "Value": pos_node.outputs[0]
            })
            return s_pos.outputs[0]

        p_start = get_vert_pos(0)
        p_end = get_vert_pos(1)

        def get_vec_handle(prefix):
            x = sample_edge(f"{prefix}_x", 'FLOAT')
            y = sample_edge(f"{prefix}_y", 'FLOAT')
            z = sample_edge(f"{prefix}_z", 'FLOAT')
            combine = nodes.new("ShaderNodeCombineXYZ")
            links.new(x, combine.inputs[0])
            links.new(y, combine.inputs[1])
            links.new(z, combine.inputs[2])
            return combine.outputs[0]

        h_start = get_vec_handle("handle_start")
        h_end = get_vec_handle("handle_end")

        mix_p0 = nodes.new("ShaderNodeMix")
        mix_p0.data_type = 'VECTOR'
        links.new(is_fwd_field, mix_p0.inputs["Factor"])
        links.new(p_end, mix_p0.inputs["A"])
        links.new(p_start, mix_p0.inputs["B"])
        P0 = mix_p0.outputs["Result"]

        mix_p3 = nodes.new("ShaderNodeMix")
        mix_p3.data_type = 'VECTOR'
        links.new(is_fwd_field, mix_p3.inputs["Factor"])
        links.new(p_start, mix_p3.inputs["A"])
        links.new(p_end, mix_p3.inputs["B"])
        P3 = mix_p3.outputs["Result"]

        p1_fwd = vec_math_op(group, 'ADD', p_start, h_start)
        p1_bwd = vec_math_op(group, 'ADD', p_end, h_end)
        mix_p1 = nodes.new("ShaderNodeMix")
        mix_p1.data_type = 'VECTOR'
        links.new(is_fwd_field, mix_p1.inputs["Factor"])
        links.new(p1_bwd, mix_p1.inputs["A"])
        links.new(p1_fwd, mix_p1.inputs["B"])
        P1 = mix_p1.outputs["Result"]

        p2_fwd = vec_math_op(group, 'ADD', p_end, h_end)
        p2_bwd = vec_math_op(group, 'ADD', p_start, h_start)
        mix_p2 = nodes.new("ShaderNodeMix")
        mix_p2.data_type = 'VECTOR'
        links.new(is_fwd_field, mix_p2.inputs["Factor"])
        links.new(p2_bwd, mix_p2.inputs["A"])
        links.new(p2_fwd, mix_p2.inputs["B"])
        P2 = mix_p2.outputs["Result"]

        one_minus_t = math_op(group, 'SUBTRACT', 1.0, t_field)
        c0 = math_op(group, 'POWER', one_minus_t, 3.0)
        c1 = math_op(group, 'MULTIPLY', math_op(group, 'MULTIPLY', 3.0, math_op(group, 'POWER', one_minus_t, 2.0)), t_field)
        c2 = math_op(group, 'MULTIPLY', math_op(group, 'MULTIPLY', 3.0, one_minus_t), math_op(group, 'POWER', t_field, 2.0))
        c3 = math_op(group, 'POWER', t_field, 3.0)

        return vec_math_op(group, 'ADD',
            vec_math_op(group, 'ADD', vec_math_op(group, 'SCALE', P0, c0), vec_math_op(group, 'SCALE', P1, c1)),
            vec_math_op(group, 'ADD', vec_math_op(group, 'SCALE', P2, c2), vec_math_op(group, 'SCALE', P3, c3))
        )

    e0, d0 = get_attr(group, "e0", "INT"), get_attr(group, "d0", 'BOOLEAN')
    e1, d1 = get_attr(group, "e1", "INT"), get_attr(group, "d1", 'BOOLEAN')
    e2, d2 = get_attr(group, "e2", "INT"), get_attr(group, "d2", 'BOOLEAN')
    e3, d3 = get_attr(group, "e3", "INT"), get_attr(group, "d3", 'BOOLEAN')

    c_bottom = eval_bezier_curve(subdivided_geo, e0, d0, u_raw, group_input.outputs[0])
    c_top = eval_bezier_curve(subdivided_geo, e2, d2, math_op(group, 'SUBTRACT', 1.0, u_raw), group_input.outputs[0])
    c_left = eval_bezier_curve(subdivided_geo, e3, d3, math_op(group, 'SUBTRACT', 1.0, v_raw), group_input.outputs[0])
    c_right = eval_bezier_curve(subdivided_geo, e1, d1, v_raw, group_input.outputs[0])

    p00 = eval_bezier_curve(subdivided_geo, e0, d0, 0.0, group_input.outputs[0])
    p10 = eval_bezier_curve(subdivided_geo, e0, d0, 1.0, group_input.outputs[0])
    p01 = eval_bezier_curve(subdivided_geo, e2, d2, 1.0, group_input.outputs[0])
    p11 = eval_bezier_curve(subdivided_geo, e2, d2, 0.0, group_input.outputs[0])

    loft_u = nodes.new("ShaderNodeMix")
    loft_u.data_type = 'VECTOR'
    links.new(v_smooth, loft_u.inputs["Factor"])
    links.new(c_bottom, loft_u.inputs["A"])
    links.new(c_top, loft_u.inputs["B"])

    loft_v = nodes.new("ShaderNodeMix")
    loft_v.data_type = 'VECTOR'
    links.new(u_smooth, loft_v.inputs["Factor"])
    links.new(c_left, loft_v.inputs["A"])
    links.new(c_right, loft_v.inputs["B"])

    mix_b1 = nodes.new("ShaderNodeMix")
    mix_b1.data_type = 'VECTOR'
    links.new(u_smooth, mix_b1.inputs["Factor"])
    links.new(p00, mix_b1.inputs["A"])
    links.new(p10, mix_b1.inputs["B"])

    mix_b2 = nodes.new("ShaderNodeMix")
    mix_b2.data_type = 'VECTOR'
    links.new(u_smooth, mix_b2.inputs["Factor"])
    links.new(p01, mix_b2.inputs["A"])
    links.new(p11, mix_b2.inputs["B"])

    bilinear = nodes.new("ShaderNodeMix")
    bilinear.data_type = 'VECTOR'
    links.new(v_smooth, bilinear.inputs["Factor"])
    links.new(mix_b1.outputs["Result"], bilinear.inputs["A"])
    links.new(mix_b2.outputs["Result"], bilinear.inputs["B"])

    final_pos = vec_math_op(group, 'SUBTRACT',
        vec_math_op(group, 'ADD', loft_u.outputs["Result"], loft_v.outputs["Result"]),
        bilinear.outputs["Result"]
    )

    set_pos = create_node(group, "GeometryNodeSetPosition", {
        "Geometry": subdivided_geo,
        "Position": final_pos
    })

    merge = create_node(group, "GeometryNodeMergeByDistance", {
        "Geometry": set_pos.outputs[0],
        "Distance": 0.001
    })

    set_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    links.new(merge.outputs[0], set_smooth.inputs[0])
    set_smooth.inputs["Shade Smooth"].default_value = True

    links.new(set_smooth.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
