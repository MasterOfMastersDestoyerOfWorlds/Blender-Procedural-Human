import bpy
import math
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group

@geo_node_group
def create_charrot_gregory_group():
    """
    Creates a Geometry Node group that generates Charrot-Gregory patches 
    for arbitrary N-gons using Repeat Zones (Blender 4.0+).
    
    Key insight: Store domain polygon coordinates on corners BEFORE subdivision.
    Subdivision naturally interpolates these, giving correct parametric coords
    that map face edges to domain polygon edges.
    
    CRITICAL: Sample edge/direction info from ORIGINAL geometry, not split geometry.
    Corner indices change after SplitEdges!
    """
    group_name = "CharrotGregoryPatchGenerator"
    if group_name in bpy.data.node_groups:
        bpy.data.node_groups.remove(bpy.data.node_groups[group_name])

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    
    # --- Interface ---
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Subdivisions", in_out="INPUT", socket_type="NodeSocketInt").default_value = 4
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    
    # --- Helpers ---
    def is_socket(obj):
        return isinstance(obj, bpy.types.NodeSocket)

    def link_or_set(socket_in, value):
        if is_socket(value):
            links.new(value, socket_in)
        elif isinstance(value, (int, float, bool, str)):
            socket_in.default_value = value
        elif isinstance(value, (tuple, list)):
            socket_in.default_value = value

    def create_node(type_name, inputs=None, **properties):
        node = nodes.new(type_name)
        if inputs:
            for k, v in inputs.items():
                k_prop = k.lower().replace(" ", "_")
                if hasattr(node, k_prop):
                    try:
                        setattr(node, k_prop, v)
                    except Exception:
                        pass
                elif hasattr(node, k):
                    try:
                        setattr(node, k, v)
                    except Exception:
                        pass
            for k, v in inputs.items():
                if k in node.inputs:
                    link_or_set(node.inputs[k], v)
        return node

    def math_op(op, a, b=None):
        n = nodes.new("ShaderNodeMath")
        n.operation = op
        link_or_set(n.inputs[0], a)
        if b is not None:
            link_or_set(n.inputs[1], b)
        return n.outputs[0]

    def vec_math_op(op, a, b=None):
        n = nodes.new("ShaderNodeVectorMath")
        n.operation = op
        link_or_set(n.inputs[0], a)
        if b is not None:
            if op == 'SCALE':
                link_or_set(n.inputs[3], b)
            else:
                link_or_set(n.inputs[1], b)
        if op in ('DOT_PRODUCT', 'LENGTH', 'DISTANCE'):
            return n.outputs[1]
        return n.outputs[0]

    def get_attr(name, dtype='INT'):
        n = nodes.new("GeometryNodeInputNamedAttribute")
        n.data_type = dtype
        n.inputs["Name"].default_value = name
        return n.outputs[0]

    # --- 1. INPUTS & TOPOLOGY ---
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    orig_geo = group_input.outputs["Geometry"]
    
    # Get corner index (evaluated in CORNER domain)
    corner_idx = nodes.new("GeometryNodeInputIndex").outputs[0]
    
    # Get face of this corner
    face_of_corner = nodes.new("GeometryNodeFaceOfCorner")
    links.new(corner_idx, face_of_corner.inputs["Corner Index"])
    face_idx = face_of_corner.outputs["Face Index"]
    
    # Get first corner of face (sort index 0)
    corners_of_face = nodes.new("GeometryNodeCornersOfFace")
    links.new(face_idx, corners_of_face.inputs["Face Index"])
    corners_of_face.inputs["Sort Index"].default_value = 0
    first_corner = corners_of_face.outputs["Corner Index"]
    
    # Compute sort index (0, 1, 2, ..., N-1) for this corner within face
    sort_idx = math_op('SUBTRACT', corner_idx, first_corner)
    
    # Count corners per face (N)
    accum_N = create_node("GeometryNodeAccumulateField", {
        "Value": 1, "Group ID": face_idx, "Domain": "CORNER"
    })
    N_total = accum_N.outputs["Total"]
    
    # --- 2. STORE DOMAIN POLYGON COORDINATES ON CORNERS ---
    # Each corner i gets domain position (cos(2πi/N + π/N), sin(2πi/N + π/N))
    # Rotating by π/N aligns the edges of N=4 (square) to the axes, fixing "cross pattern" artifacts.
    
    # angle_step = 2π / N
    angle_step = math_op('DIVIDE', 6.283185307, N_total)
    
    # theta = sort_idx * angle_step + angle_step / 2
    theta = math_op('ADD', 
        math_op('MULTIPLY', sort_idx, angle_step),
        math_op('DIVIDE', angle_step, 2.0)
    )
    
    # domain_pos = (cos(θ), sin(θ), 0)
    domain_x = math_op('COSINE', theta)
    domain_y = math_op('SINE', theta)
    
    domain_pos_combine = nodes.new("ShaderNodeCombineXYZ")
    links.new(domain_x, domain_pos_combine.inputs["X"])
    links.new(domain_y, domain_pos_combine.inputs["Y"])
    
    # Store domain position on CORNER domain
    store_domain_pos = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "domain_pos", "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Value": domain_pos_combine.outputs[0]
    })
    links.new(orig_geo, store_domain_pos.inputs[0])
    
    # --- 3. STORE FACE INDEX ON FACE DOMAIN ---
    # This propagates through split/subdivide so we can look up original corners
    face_idx_node = nodes.new("GeometryNodeInputIndex")  # In FACE context this gives face index
    
    store_face_idx = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "orig_face_idx", "Domain": "FACE", "Data Type": "INT",
        "Value": face_idx_node.outputs[0]
    })
    links.new(store_domain_pos.outputs[0], store_face_idx.inputs[0])

    # Store original loop start ("first corner") per face.
    # This is stable for looking up per-face corners later even after subdiv/split,
    # and avoids using CornersOfFace with face indices from a different geometry.
    corners_of_face_for_store = nodes.new("GeometryNodeCornersOfFace")
    links.new(face_idx_node.outputs[0], corners_of_face_for_store.inputs["Face Index"])
    corners_of_face_for_store.inputs["Sort Index"].default_value = 0

    store_loop_start = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "orig_loop_start", "Domain": "FACE", "Data Type": "INT",
        "Value": corners_of_face_for_store.outputs["Corner Index"]
    })
    links.new(store_face_idx.outputs[0], store_loop_start.inputs[0])
    
    # Store N on face domain
    store_N = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "poly_N", "Domain": "FACE", "Data Type": "INT",
        "Value": N_total
    })
    links.new(store_loop_start.outputs[0], store_N.inputs[0])
    
    # --- 4. STORE EDGE INFO ON CORNERS (for sampling from original geo) ---
    edges_of_corner = nodes.new("GeometryNodeEdgesOfCorner")
    links.new(corner_idx, edges_of_corner.inputs["Corner Index"])
    
    store_edge_idx = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "corner_edge_idx", "Domain": "CORNER", "Data Type": "INT",
        "Value": edges_of_corner.outputs["Next Edge Index"]
    })
    links.new(store_N.outputs[0], store_edge_idx.inputs[0])
    
    # Determine edge direction
    vertex_of_corner = nodes.new("GeometryNodeVertexOfCorner")
    links.new(corner_idx, vertex_of_corner.inputs["Corner Index"])
    
    edge_verts = nodes.new("GeometryNodeInputMeshEdgeVertices")
    
    # Sample edge's first vertex at the edge index
    sample_edge_v1 = create_node("GeometryNodeSampleIndex", {
        "Geometry": store_edge_idx.outputs[0],
        "Domain": "EDGE", "Data Type": "INT",
        "Index": edges_of_corner.outputs["Next Edge Index"]
    })
    links.new(edge_verts.outputs["Vertex Index 1"], sample_edge_v1.inputs["Value"])
    
    is_fwd_cmp = create_node("FunctionNodeCompare", {"Data Type": "INT", "Operation": "EQUAL"})
    links.new(vertex_of_corner.outputs["Vertex Index"], is_fwd_cmp.inputs["A"])
    links.new(sample_edge_v1.outputs[0], is_fwd_cmp.inputs["B"])
    
    store_is_fwd = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "edge_is_forward", "Domain": "CORNER", "Data Type": "BOOLEAN",
        "Value": is_fwd_cmp.outputs["Result"]
    })
    links.new(store_edge_idx.outputs[0], store_is_fwd.inputs[0])
    
    prepared_geo = store_is_fwd.outputs[0]
    
    # --- 5. SPLIT & SUBDIVIDE ---
    split = create_node("GeometryNodeSplitEdges", {"Mesh": prepared_geo})
    
    subdiv = create_node("GeometryNodeSubdivideMesh", {
        "Mesh": split.outputs[0],
        "Level": group_input.outputs["Subdivisions"]
    })
    subdivided_geo = subdiv.outputs[0]
    
    # --- 6. READ INTERPOLATED DOMAIN POSITION ---
    domain_p_attr = get_attr("domain_pos", "FLOAT_VECTOR")
    
    sep_domain = nodes.new("ShaderNodeSeparateXYZ")
    links.new(domain_p_attr, sep_domain.inputs[0])
    domain_p_x = sep_domain.outputs["X"]
    domain_p_y = sep_domain.outputs["Y"]
    
    N_field = get_attr("poly_N", "INT")
    orig_face_idx_field = get_attr("orig_face_idx", "INT")
    orig_loop_start_field = get_attr("orig_loop_start", "INT")
    
    # --- 7. REPEAT ZONE 1: Compute LogSum of all λ ---
    stat_N = create_node("GeometryNodeAttributeStatistic", {
        "Geometry": subdivided_geo, "Domain": "POINT", "Attribute": N_field
    })
    max_N = stat_N.outputs["Max"]
    
    rep_1_in = nodes.new("GeometryNodeRepeatInput")
    rep_1_out = nodes.new("GeometryNodeRepeatOutput")
    rep_1_in.pair_with_output(rep_1_out)
    
    rep_1_out.repeat_items.new("GEOMETRY", "Geometry")
    rep_1_out.repeat_items.new("FLOAT", "LogSum")
    rep_1_out.repeat_items.new("INT", "IterIdx")
    
    links.new(subdivided_geo, rep_1_in.inputs["Geometry"])
    links.new(max_N, rep_1_in.inputs["Iterations"])
    rep_1_in.inputs["LogSum"].default_value = 0.0
    rep_1_in.inputs["IterIdx"].default_value = 0
    
    loop_geo = rep_1_in.outputs["Geometry"]
    loop_log = rep_1_in.outputs["LogSum"]
    loop_iter = rep_1_in.outputs["IterIdx"]
    
    valid_iter = math_op('LESS_THAN', loop_iter, N_field)
    
    def calc_lambda(idx_node):
        """
        Compute perpendicular distance from domain point to edge idx_node.
        Edge i goes from vertex i to vertex i+1 of the regular N-gon.
        """
        # Match the same domain rotation used for domain_pos: + (π/N) == + (angle_step/2)
        angle_step_local = math_op('DIVIDE', 6.283185307, N_field)
        angle_offset = math_op('DIVIDE', angle_step_local, 2.0)

        # Vertex i at angle (2πi/N + π/N)
        theta_i = math_op(
            'ADD',
            math_op('MULTIPLY', idx_node, angle_step_local),
            angle_offset,
        )
        v_i_x = math_op('COSINE', theta_i)
        v_i_y = math_op('SINE', theta_i)
        
        # Vertex i+1
        idx_next = math_op('ADD', idx_node, 1)
        theta_next = math_op(
            'ADD',
            math_op('MULTIPLY', idx_next, angle_step_local),
            angle_offset,
        )
        v_next_x = math_op('COSINE', theta_next)
        v_next_y = math_op('SINE', theta_next)
        
        # Edge vector
        edge_x = math_op('SUBTRACT', v_next_x, v_i_x)
        edge_y = math_op('SUBTRACT', v_next_y, v_i_y)
        edge_len = math_op('SQRT', math_op('ADD', 
            math_op('MULTIPLY', edge_x, edge_x),
            math_op('MULTIPLY', edge_y, edge_y)
        ))
        
        # Vector from vertex i to domain point
        pv_x = math_op('SUBTRACT', domain_p_x, v_i_x)
        pv_y = math_op('SUBTRACT', domain_p_y, v_i_y)
        
        # 2D cross product (signed area)
        cross_2d = math_op('SUBTRACT',
            math_op('MULTIPLY', pv_x, edge_y),
            math_op('MULTIPLY', pv_y, edge_x)
        )
        
        # Perpendicular distance = |cross| / |edge|
        perp_dist = math_op('DIVIDE', math_op('ABSOLUTE', cross_2d), edge_len)
        
        return math_op('MAXIMUM', perp_dist, 0.0001)
    
    lam_val = calc_lambda(loop_iter)
    new_log_sum = math_op('ADD', loop_log, math_op('LOGARITHM', lam_val))
    
    final_log_mix = nodes.new("ShaderNodeMix")
    final_log_mix.data_type = 'FLOAT'
    links.new(valid_iter, final_log_mix.inputs["Factor"])
    links.new(loop_log, final_log_mix.inputs["A"])
    links.new(new_log_sum, final_log_mix.inputs["B"])
    
    next_iter = math_op('ADD', loop_iter, 1)
    
    links.new(loop_geo, rep_1_out.inputs["Geometry"])
    links.new(final_log_mix.outputs["Result"], rep_1_out.inputs["LogSum"])
    links.new(next_iter, rep_1_out.inputs["IterIdx"])
    
    # --- 8. REPEAT ZONE 2: Compute weighted positions ---
    total_log_sum = rep_1_out.outputs["LogSum"]
    
    rep_2_in = nodes.new("GeometryNodeRepeatInput")
    rep_2_out = nodes.new("GeometryNodeRepeatOutput")
    rep_2_in.pair_with_output(rep_2_out)
    
    rep_2_out.repeat_items.new("GEOMETRY", "Geometry")
    rep_2_out.repeat_items.new("VECTOR", "WeightedPos")
    rep_2_out.repeat_items.new("FLOAT", "TotalWeight")
    rep_2_out.repeat_items.new("INT", "IterIdx")
    
    links.new(rep_1_out.outputs["Geometry"], rep_2_in.inputs["Geometry"])
    links.new(max_N, rep_2_in.inputs["Iterations"])
    rep_2_in.inputs["WeightedPos"].default_value = (0, 0, 0)
    rep_2_in.inputs["TotalWeight"].default_value = 0.0
    rep_2_in.inputs["IterIdx"].default_value = 0
    
    l2_geo = rep_2_in.outputs["Geometry"]
    l2_wpos = rep_2_in.outputs["WeightedPos"]
    l2_wgt = rep_2_in.outputs["TotalWeight"]
    l2_iter = rep_2_in.outputs["IterIdx"]
    
    valid_2 = math_op('LESS_THAN', l2_iter, N_field)
    
    # λ_i (distance to edge i, which is AFTER vertex i)
    lam_curr = calc_lambda(l2_iter)
    # λ_{i-1} (distance to edge i-1, which is BEFORE vertex i)
    idx_prev = math_op('MODULO', math_op('ADD', math_op('SUBTRACT', l2_iter, 1), N_field), N_field)
    lam_prev = calc_lambda(idx_prev)
    # λ_{i+1} (distance to edge i+1, which is AFTER vertex i+1)
    idx_next = math_op('MODULO', math_op('ADD', l2_iter, 1), N_field)
    lam_next = calc_lambda(idx_next)
    # λ_{i-2} (distance to edge i-2, needed for s_{i-1})
    idx_prev_prev = math_op('MODULO', math_op('ADD', math_op('SUBTRACT', l2_iter, 2), N_field), N_field)
    lam_prev_prev = calc_lambda(idx_prev_prev)
    
    # Weight Λ_i = Π{λ_j : j ≠ i-1 AND j ≠ i} = exp(logsum - log(λ_i) - log(λ_{i-1}))
    log_local = math_op('ADD', math_op('LOGARITHM', lam_curr), math_op('LOGARITHM', lam_prev))
    weight_i = math_op('EXPONENT', math_op('SUBTRACT', total_log_sum, log_local))
    
    # Sampling weight s_i varies along edge i using adjacent edges
    # s_i = d_{i-1} / (d_{i-1} + d_{i+1})
    s_val = math_op('DIVIDE', lam_prev, math_op('ADD', lam_prev, lam_next))

    # Sampling weight s_{i-1} varies along edge i-1
    # s_{i-1} = d_{i-2} / (d_{i-2} + d_i)
    s_prev = math_op('DIVIDE', lam_prev_prev, math_op('ADD', lam_prev_prev, lam_curr))
    
    # --- Stable per-face corner addressing ---
    # Do NOT use CornersOfFace here: it operates on the current (subdivided) geometry.
    # Instead, we stored each original face's loop start (first corner index) as an attribute.
    # Corners for a face are contiguous in the corner/loop array: corner = loop_start + sort_index.
    corner_i = math_op('ADD', orig_loop_start_field, l2_iter)
    corner_prev = math_op('ADD', orig_loop_start_field, idx_prev)
    
    def sample_from_orig_corner(attr_name, dtype, corner_idx_val):
        """Sample an attribute from the original geometry at a specific corner."""
        s = create_node("GeometryNodeSampleIndex", {
            "Geometry": prepared_geo,  # Use geometry BEFORE split
            "Domain": "CORNER", 
            "Data Type": dtype,
            "Index": corner_idx_val
        })
        attr = nodes.new("GeometryNodeInputNamedAttribute")
        attr.data_type = dtype
        attr.inputs["Name"].default_value = attr_name
        links.new(attr.outputs[0], s.inputs["Value"])
        return s.outputs[0]
    
    edge_idx_i = sample_from_orig_corner("corner_edge_idx", "INT", corner_i)
    is_fwd_i = sample_from_orig_corner("edge_is_forward", "BOOLEAN", corner_i)
    edge_idx_prev = sample_from_orig_corner("corner_edge_idx", "INT", corner_prev)
    is_fwd_prev = sample_from_orig_corner("edge_is_forward", "BOOLEAN", corner_prev)
    
    # --- Bezier evaluation (sample from ORIGINAL geometry) ---
    def eval_bezier(edge_id, fwd, t_val):
        def get_vert_pos(v_output_idx):
            # Sample which vertex index from the edge
            s_edge = create_node("GeometryNodeSampleIndex", {
                "Geometry": orig_geo, "Domain": "EDGE", "Data Type": "INT", "Index": edge_id
            })
            ev = nodes.new("GeometryNodeInputMeshEdgeVertices")
            links.new(ev.outputs[v_output_idx], s_edge.inputs["Value"])
            
            # Sample position at that vertex
            s_pos = create_node("GeometryNodeSampleIndex", {
                "Geometry": orig_geo, "Domain": "POINT", "Data Type": "FLOAT_VECTOR",
                "Index": s_edge.outputs[0]
            })
            links.new(nodes.new("GeometryNodeInputPosition").outputs[0], s_pos.inputs["Value"])
            return s_pos.outputs[0]
        
        # Edge vertices: output 0 = "Vertex Index 1", output 1 = "Vertex Index 2"
        p_v1 = get_vert_pos(0)  # Vertex Index 1
        p_v2 = get_vert_pos(1)  # Vertex Index 2
        
        def get_handle(prefix):
            def sample_handle_component(comp):
                s = create_node("GeometryNodeSampleIndex", {
                    "Geometry": orig_geo, "Domain": "EDGE", "Data Type": "FLOAT", "Index": edge_id
                })
                attr = nodes.new("GeometryNodeInputNamedAttribute")
                attr.data_type = 'FLOAT'
                attr.inputs["Name"].default_value = f"{prefix}_{comp}"
                links.new(attr.outputs[0], s.inputs["Value"])
                return s.outputs[0]
            
            c = nodes.new("ShaderNodeCombineXYZ")
            links.new(sample_handle_component("x"), c.inputs[0])
            links.new(sample_handle_component("y"), c.inputs[1])
            links.new(sample_handle_component("z"), c.inputs[2])
            return c.outputs[0]
        
        h_start = get_handle("handle_start")
        h_end = get_handle("handle_end")
        
        # P0, P3: endpoints (swapped based on direction)
        # fwd=True: P0=p_v1, P3=p_v2
        # fwd=False: P0=p_v2, P3=p_v1
        mix_p0 = nodes.new("ShaderNodeMix")
        mix_p0.data_type = 'VECTOR'
        links.new(fwd, mix_p0.inputs["Factor"])
        links.new(p_v2, mix_p0.inputs["A"])  # fwd=False
        links.new(p_v1, mix_p0.inputs["B"])  # fwd=True
        P0 = mix_p0.outputs["Result"]
        
        mix_p3 = nodes.new("ShaderNodeMix")
        mix_p3.data_type = 'VECTOR'
        links.new(fwd, mix_p3.inputs["Factor"])
        links.new(p_v1, mix_p3.inputs["A"])  # fwd=False
        links.new(p_v2, mix_p3.inputs["B"])  # fwd=True
        P3 = mix_p3.outputs["Result"]
        
        # P1 = P0 + handle_at_P0
        # P2 = P3 + handle_at_P3 (negated for incoming)
        # handle_start is relative to v1, handle_end is relative to v2
        p1_fwd = vec_math_op('ADD', p_v1, h_start)  # fwd: P1 near v1
        p1_bwd = vec_math_op('ADD', p_v2, h_end)    # bwd: P1 near v2
        mix_p1 = nodes.new("ShaderNodeMix")
        mix_p1.data_type = 'VECTOR'
        links.new(fwd, mix_p1.inputs["Factor"])
        links.new(p1_bwd, mix_p1.inputs["A"])
        links.new(p1_fwd, mix_p1.inputs["B"])
        P1 = mix_p1.outputs["Result"]
        
        # For P2 we need the handle near P3
        p2_fwd = vec_math_op('ADD', p_v2, h_end)    # fwd: P2 near v2
        p2_bwd = vec_math_op('ADD', p_v1, h_start)  # bwd: P2 near v1
        mix_p2 = nodes.new("ShaderNodeMix")
        mix_p2.data_type = 'VECTOR'
        links.new(fwd, mix_p2.inputs["Factor"])
        links.new(p2_bwd, mix_p2.inputs["A"])
        links.new(p2_fwd, mix_p2.inputs["B"])
        P2 = mix_p2.outputs["Result"]
        
        # Cubic Bezier: B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
        omt = math_op('SUBTRACT', 1.0, t_val)
        c0 = math_op('POWER', omt, 3.0)
        c1 = math_op('MULTIPLY', math_op('MULTIPLY', 3.0, math_op('POWER', omt, 2.0)), t_val)
        c2 = math_op('MULTIPLY', math_op('MULTIPLY', 3.0, omt), math_op('POWER', t_val, 2.0))
        c3 = math_op('POWER', t_val, 3.0)
        
        t1 = vec_math_op('SCALE', P0, c0)
        t2 = vec_math_op('SCALE', P1, c1)
        t3 = vec_math_op('SCALE', P2, c2)
        t4 = vec_math_op('SCALE', P3, c3)
        return vec_math_op('ADD', vec_math_op('ADD', t1, t2), vec_math_op('ADD', t3, t4))
    
    # c_i(s_i): point on curve i (edge leaving vertex i)
    c_i_pos = eval_bezier(edge_idx_i, is_fwd_i, s_val)
    # c_{i-1}(s_{i-1}): point on curve i-1 (edge arriving at vertex i)
    # We use s_{i-1} directly because it parameterizes edge i-1 from vertex i-1 to i.
    # So at vertex i (this corner), s_{i-1} -> 1.
    c_prev_pos = eval_bezier(edge_idx_prev, is_fwd_prev, s_prev)
    # p_i: corner vertex (curve i at t=0)
    p_corner = eval_bezier(edge_idx_i, is_fwd_i, 0.0)
    
    # r_i = c_i(s_i) + c_{i-1}(s_{i-1}) - p_i
    r_i = vec_math_op('SUBTRACT', vec_math_op('ADD', c_i_pos, c_prev_pos), p_corner)
    
    # Accumulate w_i * r_i
    w_r_i = vec_math_op('SCALE', r_i, weight_i)
    new_wpos = vec_math_op('ADD', l2_wpos, w_r_i)
    new_wgt = math_op('ADD', l2_wgt, weight_i)
    
    # Mix based on valid iteration
    final_wpos_mix = nodes.new("ShaderNodeMix")
    final_wpos_mix.data_type = 'VECTOR'
    links.new(valid_2, final_wpos_mix.inputs["Factor"])
    links.new(l2_wpos, final_wpos_mix.inputs["A"])
    links.new(new_wpos, final_wpos_mix.inputs["B"])
    
    final_wgt_mix = nodes.new("ShaderNodeMix")
    final_wgt_mix.data_type = 'FLOAT'
    links.new(valid_2, final_wgt_mix.inputs["Factor"])
    links.new(l2_wgt, final_wgt_mix.inputs["A"])
    links.new(new_wgt, final_wgt_mix.inputs["B"])
    
    next_iter2 = math_op('ADD', l2_iter, 1)
    
    links.new(l2_geo, rep_2_out.inputs["Geometry"])
    links.new(final_wpos_mix.outputs["Result"], rep_2_out.inputs["WeightedPos"])
    links.new(final_wgt_mix.outputs["Result"], rep_2_out.inputs["TotalWeight"])
    links.new(next_iter2, rep_2_out.inputs["IterIdx"])
    
    # --- 9. FINAL OUTPUT ---
    # Q = Σ(w_i * r_i) / Σ(w_i)
    final_pos = vec_math_op('SCALE', rep_2_out.outputs["WeightedPos"],
                           math_op('DIVIDE', 1.0, rep_2_out.outputs["TotalWeight"]))
    
    set_pos = nodes.new("GeometryNodeSetPosition")
    links.new(rep_2_out.outputs["Geometry"], set_pos.inputs["Geometry"])
    links.new(final_pos, set_pos.inputs["Position"])
    
    # Merge vertices back together
    merge = create_node("GeometryNodeMergeByDistance", {
        "Geometry": set_pos.outputs[0], "Distance": 0.0001
    })
    
    # Smooth shading
    set_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    links.new(merge.outputs[0], set_smooth.inputs[0])
    set_smooth.inputs["Shade Smooth"].default_value = True
    
    links.new(set_smooth.outputs[0], group_output.inputs[0])
    
    auto_layout_nodes(group)
    return group
