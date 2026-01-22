import bpy
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group

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
    def create_math(op, inp1, inp2=None):
        node = nodes.new("ShaderNodeMath")
        node.operation = op
        if isinstance(inp1, str): links.new(nodes.get(inp1).outputs[0], node.inputs[0])
        elif isinstance(inp1, (float, int)): node.inputs[0].default_value = inp1
        else: links.new(inp1, node.inputs[0])
        if inp2 is not None:
            if isinstance(inp2, (float, int)): node.inputs[1].default_value = inp2
            else: links.new(inp2, node.inputs[1])
        return node.outputs[0]

    def create_vec_math(op, inp1, inp2=None):
        node = nodes.new("ShaderNodeVectorMath")
        node.operation = op
        if isinstance(inp1, tuple): node.inputs[0].default_value = inp1
        else: links.new(inp1, node.inputs[0])
        
        if inp2 is not None:
            if op == 'SCALE':
                if isinstance(inp2, (float, int)): node.inputs[3].default_value = inp2
                else: links.new(inp2, node.inputs[3])
            else:
                if isinstance(inp2, tuple): node.inputs[1].default_value = inp2
                else: links.new(inp2, node.inputs[1])
        return node.outputs[0]
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    corner_idx_node = nodes.new("GeometryNodeInputIndex") # Domain: Corner
    face_of_corner = nodes.new("GeometryNodeFaceOfCorner")
    links.new(corner_idx_node.outputs[0], face_of_corner.inputs["Corner Index"])
    face_idx = face_of_corner.outputs["Face Index"]
    corners_lookup_0 = nodes.new("GeometryNodeCornersOfFace")
    links.new(face_idx, corners_lookup_0.inputs["Face Index"])
    corners_lookup_0.inputs["Sort Index"].default_value = 0
    first_corner_idx = corners_lookup_0.outputs["Corner Index"]
    sort_idx = create_math('SUBTRACT', corner_idx_node.outputs[0], first_corner_idx)
    
    op_eq1 = create_math('COMPARE', sort_idx, 1.0)
    op_eq2 = create_math('COMPARE', sort_idx, 2.0)
    op_eq3 = create_math('COMPARE', sort_idx, 3.0)
    
    u_val = create_math('ADD', op_eq1, op_eq2)
    v_val = create_math('ADD', op_eq2, op_eq3)
    
    uv_combine = nodes.new("ShaderNodeCombineXYZ")
    links.new(u_val, uv_combine.inputs[0])
    links.new(v_val, uv_combine.inputs[1])
    
    store_uv = nodes.new("GeometryNodeStoreNamedAttribute")
    store_uv.data_type = 'FLOAT_VECTOR'
    store_uv.domain = 'CORNER'
    store_uv.inputs["Name"].default_value = "patch_uv"
    links.new(group_input.outputs[0], store_uv.inputs[0])
    links.new(uv_combine.outputs[0], store_uv.inputs["Value"])
    edges_of_corner = nodes.new("GeometryNodeEdgesOfCorner")
    edge_idx_at_corner = edges_of_corner.outputs["Next Edge Index"]
    
    store_edge_indices = nodes.new("GeometryNodeStoreNamedAttribute")
    store_edge_indices.data_type = 'INT'
    store_edge_indices.domain = 'CORNER'
    store_edge_indices.inputs["Name"].default_value = "corner_edge_idx"
    links.new(store_uv.outputs[0], store_edge_indices.inputs[0])
    links.new(edge_idx_at_corner, store_edge_indices.inputs["Value"])
    vertex_of_corner = nodes.new("GeometryNodeVertexOfCorner")
    sample_edge_vert1 = nodes.new("GeometryNodeSampleIndex")
    sample_edge_vert1.domain = 'EDGE'
    sample_edge_vert1.data_type = 'INT'
    links.new(store_edge_indices.outputs[0], sample_edge_vert1.inputs["Geometry"])
    links.new(edge_idx_at_corner, sample_edge_vert1.inputs["Index"])
    
    edge_verts_node = nodes.new("GeometryNodeInputMeshEdgeVertices")
    links.new(edge_verts_node.outputs["Vertex Index 1"], sample_edge_vert1.inputs["Value"])
    is_fwd_cmp = nodes.new("FunctionNodeCompare")
    is_fwd_cmp.data_type = 'INT'
    is_fwd_cmp.operation = 'EQUAL'
    links.new(vertex_of_corner.outputs["Vertex Index"], is_fwd_cmp.inputs["A"])
    links.new(sample_edge_vert1.outputs[0], is_fwd_cmp.inputs["B"])
    is_forward = is_fwd_cmp.outputs["Result"]
    
    store_direction = nodes.new("GeometryNodeStoreNamedAttribute")
    store_direction.data_type = 'BOOLEAN'
    store_direction.domain = 'CORNER'
    store_direction.inputs["Name"].default_value = "edge_is_forward"
    links.new(store_edge_indices.outputs[0], store_direction.inputs[0])
    links.new(is_forward, store_direction.inputs["Value"])
    
    def get_data_from_corner_sort_id(geo_link, sort_id_val, attr_name, type='INT'):
        face_idx_node = nodes.new("GeometryNodeInputIndex") 
        
        c_lookup = nodes.new("GeometryNodeCornersOfFace")
        links.new(face_idx_node.outputs[0], c_lookup.inputs["Face Index"])
        c_lookup.inputs["Sort Index"].default_value = sort_id_val
        target_corner = c_lookup.outputs["Corner Index"]
        
        samp = nodes.new("GeometryNodeSampleIndex")
        samp.domain = 'CORNER'
        samp.data_type = type
        links.new(geo_link, samp.inputs["Geometry"])
        links.new(target_corner, samp.inputs["Index"])
        
        read_attr = nodes.new("GeometryNodeInputNamedAttribute")
        read_attr.data_type = type
        read_attr.inputs["Name"].default_value = attr_name
        
        links.new(read_attr.outputs[0], samp.inputs["Value"])
        return samp.outputs[0]

    def store_face_attr(geo, name, val, type='INT'):
        s = nodes.new("GeometryNodeStoreNamedAttribute")
        s.domain = 'FACE'
        s.data_type = type
        s.inputs["Name"].default_value = name
        links.new(geo, s.inputs[0])
        links.new(val, s.inputs["Value"])
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
    split_edges = nodes.new("GeometryNodeSplitEdges")
    links.new(geo, split_edges.inputs["Mesh"])
    
    subdiv = nodes.new("GeometryNodeSubdivideMesh")
    links.new(split_edges.outputs[0], subdiv.inputs[0])
    links.new(group_input.outputs["Subdivisions"], subdiv.inputs["Level"])
    subdivided_geo = subdiv.outputs[0]
    
    get_uv = nodes.new("GeometryNodeInputNamedAttribute")
    get_uv.data_type = 'FLOAT_VECTOR'
    get_uv.inputs["Name"].default_value = "patch_uv"
    sep_uv = nodes.new("ShaderNodeSeparateXYZ")
    links.new(get_uv.outputs[0], sep_uv.inputs[0])
    u_raw = sep_uv.outputs["X"]
    v_raw = sep_uv.outputs["Y"]
    
    def smoother_step(val_node):
        s1 = create_math('SUBTRACT', create_math('MULTIPLY', val_node, 6.0), 15.0)
        s2 = create_math('ADD', create_math('MULTIPLY', val_node, s1), 10.0)
        t3 = create_math('POWER', val_node, 3.0)
        return create_math('MULTIPLY', t3, s2)

    u_smooth = smoother_step(u_raw)
    v_smooth = smoother_step(v_raw)

    def eval_bezier_curve(geo_ref, edge_idx_field, is_fwd_field, t_field, original_geometry):
        
        def sample_edge(attr_name, type='FLOAT_VECTOR'):
            s = nodes.new("GeometryNodeSampleIndex")
            s.domain = 'EDGE'
            s.data_type = type
            links.new(original_geometry, s.inputs["Geometry"])
            links.new(edge_idx_field, s.inputs["Index"])
            inp = nodes.new("GeometryNodeInputNamedAttribute")
            inp.data_type = type
            inp.inputs["Name"].default_value = attr_name
            links.new(inp.outputs[0], s.inputs["Value"])
            return s.outputs[0]
        
        def get_vert_pos(v_socket_idx):
            s_verts = nodes.new("GeometryNodeSampleIndex")
            s_verts.domain = 'EDGE'
            s_verts.data_type = 'INT'
            links.new(original_geometry, s_verts.inputs["Geometry"])
            links.new(edge_idx_field, s_verts.inputs["Index"])
            ev = nodes.new("GeometryNodeInputMeshEdgeVertices")
            links.new(ev.outputs[v_socket_idx], s_verts.inputs["Value"])
            
            s_pos = nodes.new("GeometryNodeSampleIndex")
            s_pos.domain = 'POINT'
            s_pos.data_type = 'FLOAT_VECTOR'
            links.new(original_geometry, s_pos.inputs["Geometry"])
            links.new(s_verts.outputs[0], s_pos.inputs["Index"])
            links.new(nodes.new("GeometryNodeInputPosition").outputs[0], s_pos.inputs["Value"])
            return s_pos.outputs[0]

        p_start = get_vert_pos(0) # Vertex 1
        p_end = get_vert_pos(1)   # Vertex 2
        
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
        
        p1_fwd = create_vec_math('ADD', p_start, h_start)
        p1_bwd = create_vec_math('ADD', p_end, h_end)
        mix_p1 = nodes.new("ShaderNodeMix")
        mix_p1.data_type = 'VECTOR'
        links.new(is_fwd_field, mix_p1.inputs["Factor"])
        links.new(p1_bwd, mix_p1.inputs["A"])
        links.new(p1_fwd, mix_p1.inputs["B"])
        P1 = mix_p1.outputs["Result"]
        
        p2_fwd = create_vec_math('ADD', p_end, h_end)
        p2_bwd = create_vec_math('ADD', p_start, h_start)
        mix_p2 = nodes.new("ShaderNodeMix")
        mix_p2.data_type = 'VECTOR'
        links.new(is_fwd_field, mix_p2.inputs["Factor"])
        links.new(p2_bwd, mix_p2.inputs["A"])
        links.new(p2_fwd, mix_p2.inputs["B"])
        P2 = mix_p2.outputs["Result"]
        
        one_minus_t = create_math('SUBTRACT', 1.0, t_field)
        c0 = create_math('POWER', one_minus_t, 3.0)
        c1 = create_math('MULTIPLY', create_math('MULTIPLY', 3.0, create_math('POWER', one_minus_t, 2.0)), t_field)
        c2 = create_math('MULTIPLY', create_math('MULTIPLY', 3.0, one_minus_t), create_math('POWER', t_field, 2.0))
        c3 = create_math('POWER', t_field, 3.0)
        
        return create_vec_math('ADD', 
            create_vec_math('ADD', create_vec_math('SCALE', P0, c0), create_vec_math('SCALE', P1, c1)),
            create_vec_math('ADD', create_vec_math('SCALE', P2, c2), create_vec_math('SCALE', P3, c3))
        )

    def get_face_attr(name, type='INT'):
        node = nodes.new("GeometryNodeInputNamedAttribute")
        node.data_type = type
        node.inputs["Name"].default_value = name
        return node.outputs[0]
        
    e0, d0 = get_face_attr("e0"), get_face_attr("d0", 'BOOLEAN')
    e1, d1 = get_face_attr("e1"), get_face_attr("d1", 'BOOLEAN')
    e2, d2 = get_face_attr("e2"), get_face_attr("e2", 'BOOLEAN') # Typo check: "d2"
    d2 = get_face_attr("d2", 'BOOLEAN') 
    e3, d3 = get_face_attr("e3"), get_face_attr("d3", 'BOOLEAN')

    c_bottom = eval_bezier_curve(subdivided_geo, e0, d0, u_raw, group_input.outputs[0])
    c_top    = eval_bezier_curve(subdivided_geo, e2, d2, create_math('SUBTRACT', 1.0, u_raw), group_input.outputs[0])
    c_left   = eval_bezier_curve(subdivided_geo, e3, d3, create_math('SUBTRACT', 1.0, v_raw), group_input.outputs[0])
    c_right  = eval_bezier_curve(subdivided_geo, e1, d1, v_raw, group_input.outputs[0])
    
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
    
    final_pos = create_vec_math('SUBTRACT', 
        create_vec_math('ADD', loft_u.outputs["Result"], loft_v.outputs["Result"]), 
        bilinear.outputs["Result"]
    )
    
    set_pos = nodes.new("GeometryNodeSetPosition")
    links.new(subdivided_geo, set_pos.inputs["Geometry"])
    links.new(final_pos, set_pos.inputs["Position"])
    merge = nodes.new("GeometryNodeMergeByDistance")
    links.new(set_pos.outputs[0], merge.inputs["Geometry"])
    merge.inputs["Distance"].default_value = 0.001
    
    set_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    links.new(merge.outputs[0], set_smooth.inputs[0])
    set_smooth.inputs["Shade Smooth"].default_value = True

    links.new(set_smooth.outputs[0], group_output.inputs[0])
    
    auto_layout_nodes(group)
    return group