import bpy
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group

@geo_node_group
def create_charrot_gregory_group():
    """
    Creates a Geometry Node group that generates an n-sided C0 Coons patch
    following Péter Salvi (2020) Eq. (1)–(7) from `charrot_gregory_equations.md`.

    Summary:
    - Define a regular n-gon parameter domain and compute Wachspress coordinates λ_i (Eq. 4)
    - Define ribbon parameters s_i, d_i (Eq. 5)
    - Build a Coons ribbon R_i(s_i, d_i) (Eq. 1) using C_{i-1}, C_i, C_{i+1} and C_i^{opp} (Eq. 2–3)
    - Blend S(p) = Σ_i R_i(s_i, d_i) * B_i(d_i) with B_i(d) = 1 - d^2 (Eq. 6–7)

    Implementation notes:
    - We store domain polygon coordinates per CORNER before subdivision and rely on interpolation.
    - We split edges so each face is an island (prevents attribute averaging across faces).
    - We sample edge curve data (endpoints + handle_start/handle_end) from the ORIGINAL mesh.
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

    def int_op(op, a, b):
        n = nodes.new("FunctionNodeIntegerMath")
        n.operation = op
        link_or_set(n.inputs[0], a)
        link_or_set(n.inputs[1], b)
        return n.outputs[0]

    def compare_int_less(a, b):
        c = nodes.new("FunctionNodeCompare")
        c.data_type = "INT"
        c.operation = "LESS_THAN"
        links.new(a, c.inputs["A"])
        links.new(b, c.inputs["B"])
        return c.outputs["Result"]

    def compare_float_less(a, b_val):
        c = nodes.new("FunctionNodeCompare")
        c.data_type = "FLOAT"
        c.operation = "LESS_THAN"
        links.new(a, c.inputs["A"])
        c.inputs["B"].default_value = float(b_val)
        return c.outputs["Result"]

    def bool_and(a, b):
        n = nodes.new("FunctionNodeBooleanMath")
        n.operation = "AND"
        links.new(a, n.inputs[0])
        links.new(b, n.inputs[1])
        return n.outputs["Boolean"]

    def bool_or(a, b):
        n = nodes.new("FunctionNodeBooleanMath")
        n.operation = "OR"
        links.new(a, n.inputs[0])
        links.new(b, n.inputs[1])
        return n.outputs["Boolean"]

    def bool_not(a):
        n = nodes.new("FunctionNodeBooleanMath")
        n.operation = "NOT"
        links.new(a, n.inputs[0])
        return n.outputs["Boolean"]

    def switch_int(sw, false_val, true_val):
        n = nodes.new("GeometryNodeSwitch")
        n.input_type = "INT"
        links.new(sw, n.inputs["Switch"])
        links.new(false_val, n.inputs["False"])
        links.new(true_val, n.inputs["True"])
        return n.outputs["Output"]

    def switch_vec(sw, false_val, true_val):
        n = nodes.new("GeometryNodeSwitch")
        n.input_type = "VECTOR"
        links.new(sw, n.inputs["Switch"])
        links.new(false_val, n.inputs["False"])
        links.new(true_val, n.inputs["True"])
        return n.outputs["Output"]

    def clamp01(x):
        return math_op("MINIMUM", 1.0, math_op("MAXIMUM", 0.0, x))

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
    orig_loop_start_field = get_attr("orig_loop_start", "INT")

    # --- 6.0 Determine max N across patches (repeat iterations) ---
    stat_N = create_node("GeometryNodeAttributeStatistic", {
        "Geometry": subdivided_geo, "Domain": "POINT", "Attribute": N_field
    })
    max_N = stat_N.outputs["Max"]

    # --- 7. Geometry sampling helpers (from original mesh) ---
    def sample_from_orig_corner(attr_name, dtype, corner_idx_val):
        s = create_node("GeometryNodeSampleIndex", {
            "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": dtype, "Index": corner_idx_val
        })
        attr = nodes.new("GeometryNodeInputNamedAttribute")
        attr.data_type = dtype
        attr.inputs["Name"].default_value = attr_name
        links.new(attr.outputs[0], s.inputs["Value"])
        return s.outputs[0]

    def mapped_index(idx):
        """Domain index -> mesh corner sort index (identity for now)."""
        # NOTE: The paper assumes consistent circular indexing. We keep the face's corner order.
        # If you need auto rotate/flip again, this is where to plug it in.
        return idx

    def corner_for_idx(idx):
        return int_op("ADD", orig_loop_start_field, mapped_index(idx))

    def edge_for_idx(idx):
        cidx = corner_for_idx(idx)
        e = sample_from_orig_corner("corner_edge_idx", "INT", cidx)
        d = sample_from_orig_corner("edge_is_forward", "BOOLEAN", cidx)
        return e, d

    def edge_control_points(edge_id, fwd):
        """Return cubic Bezier control points P0..P3 for edge curve C_i."""
        def edge_vertex_pos(which):
            # which: 0 -> Vertex Index 1, 1 -> Vertex Index 2
            s_edge = create_node("GeometryNodeSampleIndex", {
                "Geometry": orig_geo, "Domain": "EDGE", "Data Type": "INT", "Index": edge_id
            })
            ev = nodes.new("GeometryNodeInputMeshEdgeVertices")
            links.new(ev.outputs[which], s_edge.inputs["Value"])
            s_pos = create_node("GeometryNodeSampleIndex", {
                "Geometry": orig_geo, "Domain": "POINT", "Data Type": "FLOAT_VECTOR", "Index": s_edge.outputs[0]
            })
            links.new(nodes.new("GeometryNodeInputPosition").outputs[0], s_pos.inputs["Value"])
            return s_pos.outputs[0]

        def edge_handle_vec(prefix):
            def comp(c):
                s = create_node("GeometryNodeSampleIndex", {
                    "Geometry": orig_geo, "Domain": "EDGE", "Data Type": "FLOAT", "Index": edge_id
                })
                attr = nodes.new("GeometryNodeInputNamedAttribute")
                attr.data_type = "FLOAT"
                attr.inputs["Name"].default_value = f"{prefix}_{c}"
                links.new(attr.outputs[0], s.inputs["Value"])
                return s.outputs[0]
            comb = nodes.new("ShaderNodeCombineXYZ")
            links.new(comp("x"), comb.inputs[0])
            links.new(comp("y"), comb.inputs[1])
            links.new(comp("z"), comb.inputs[2])
            return comb.outputs[0]

        p_v1 = edge_vertex_pos(0)
        p_v2 = edge_vertex_pos(1)
        h_start = edge_handle_vec("handle_start")  # relative to v1
        h_end = edge_handle_vec("handle_end")      # relative to v2

        # Endpoint mix
        mix_p0 = nodes.new("ShaderNodeMix")
        mix_p0.data_type = "VECTOR"
        links.new(fwd, mix_p0.inputs["Factor"])
        links.new(p_v2, mix_p0.inputs["A"])
        links.new(p_v1, mix_p0.inputs["B"])
        P0 = mix_p0.outputs["Result"]

        mix_p3 = nodes.new("ShaderNodeMix")
        mix_p3.data_type = "VECTOR"
        links.new(fwd, mix_p3.inputs["Factor"])
        links.new(p_v1, mix_p3.inputs["A"])
        links.new(p_v2, mix_p3.inputs["B"])
        P3 = mix_p3.outputs["Result"]

        # Handles depend on direction
        p1_fwd = vec_math_op("ADD", p_v1, h_start)
        p1_bwd = vec_math_op("ADD", p_v2, h_end)
        mix_p1 = nodes.new("ShaderNodeMix")
        mix_p1.data_type = "VECTOR"
        links.new(fwd, mix_p1.inputs["Factor"])
        links.new(p1_bwd, mix_p1.inputs["A"])
        links.new(p1_fwd, mix_p1.inputs["B"])
        P1 = mix_p1.outputs["Result"]

        p2_fwd = vec_math_op("ADD", p_v2, h_end)
        p2_bwd = vec_math_op("ADD", p_v1, h_start)
        mix_p2 = nodes.new("ShaderNodeMix")
        mix_p2.data_type = "VECTOR"
        links.new(fwd, mix_p2.inputs["Factor"])
        links.new(p2_bwd, mix_p2.inputs["A"])
        links.new(p2_fwd, mix_p2.inputs["B"])
        P2 = mix_p2.outputs["Result"]

        return P0, P1, P2, P3

    def bezier_eval(P0, P1, P2, P3, t):
        omt = math_op("SUBTRACT", 1.0, t)
        c0 = math_op("POWER", omt, 3.0)
        c1 = math_op("MULTIPLY", math_op("MULTIPLY", 3.0, math_op("POWER", omt, 2.0)), t)
        c2 = math_op("MULTIPLY", math_op("MULTIPLY", 3.0, omt), math_op("POWER", t, 2.0))
        c3 = math_op("POWER", t, 3.0)
        return vec_math_op("ADD",
                           vec_math_op("ADD", vec_math_op("SCALE", P0, c0), vec_math_op("SCALE", P1, c1)),
                           vec_math_op("ADD", vec_math_op("SCALE", P2, c2), vec_math_op("SCALE", P3, c3)))

    def bezier_deriv(P0, P1, P2, P3, t):
        omt = math_op("SUBTRACT", 1.0, t)
        omt2 = math_op("POWER", omt, 2.0)
        t2 = math_op("POWER", t, 2.0)
        a0 = math_op("MULTIPLY", 3.0, omt2)
        a1 = math_op("MULTIPLY", 6.0, math_op("MULTIPLY", omt, t))
        a2 = math_op("MULTIPLY", 3.0, t2)
        d10 = vec_math_op("SUBTRACT", P1, P0)
        d21 = vec_math_op("SUBTRACT", P2, P1)
        d32 = vec_math_op("SUBTRACT", P3, P2)
        return vec_math_op("ADD",
                           vec_math_op("ADD", vec_math_op("SCALE", d10, a0), vec_math_op("SCALE", d21, a1)),
                           vec_math_op("SCALE", d32, a2))

    # --- 8. Domain distances D_i(p) to regular polygon edges ---
    def domain_edge_distance(i_idx):
        angle_step_local = math_op("DIVIDE", 6.283185307, N_field)
        angle_offset = math_op("DIVIDE", angle_step_local, 2.0)  # π/N

        theta0 = math_op("ADD", math_op("MULTIPLY", i_idx, angle_step_local), angle_offset)
        theta1 = math_op("ADD", math_op("MULTIPLY", math_op("ADD", i_idx, 1), angle_step_local), angle_offset)

        v0x = math_op("COSINE", theta0)
        v0y = math_op("SINE", theta0)
        v1x = math_op("COSINE", theta1)
        v1y = math_op("SINE", theta1)

        ex = math_op("SUBTRACT", v1x, v0x)
        ey = math_op("SUBTRACT", v1y, v0y)
        elen = math_op("SQRT", math_op("ADD", math_op("MULTIPLY", ex, ex), math_op("MULTIPLY", ey, ey)))

        px = math_op("SUBTRACT", domain_p_x, v0x)
        py = math_op("SUBTRACT", domain_p_y, v0y)
        cross2 = math_op("SUBTRACT", math_op("MULTIPLY", px, ey), math_op("MULTIPLY", py, ex))
        return math_op("DIVIDE", math_op("ABSOLUTE", cross2), elen)

    # --- 9. Repeat Zone A: logD_total = Σ log(D_i) ---
    repA_in = nodes.new("GeometryNodeRepeatInput")
    repA_out = nodes.new("GeometryNodeRepeatOutput")
    repA_in.pair_with_output(repA_out)
    repA_out.repeat_items.new("GEOMETRY", "Geometry")
    repA_out.repeat_items.new("FLOAT", "LogDTotal")
    repA_out.repeat_items.new("INT", "IterIdx")

    links.new(subdivided_geo, repA_in.inputs["Geometry"])
    links.new(max_N, repA_in.inputs["Iterations"])
    repA_in.inputs["LogDTotal"].default_value = 0.0
    repA_in.inputs["IterIdx"].default_value = 0

    A_geo = repA_in.outputs["Geometry"]
    A_log = repA_in.outputs["LogDTotal"]
    A_i = repA_in.outputs["IterIdx"]
    A_valid = compare_int_less(A_i, N_field)

    D_i = domain_edge_distance(A_i)
    D_i_clamp = math_op("MAXIMUM", D_i, 1.0e-8)
    add_log = math_op("ADD", A_log, math_op("LOGARITHM", D_i_clamp))

    A_log_mix = nodes.new("ShaderNodeMix")
    A_log_mix.data_type = "FLOAT"
    links.new(A_valid, A_log_mix.inputs["Factor"])
    links.new(A_log, A_log_mix.inputs["A"])
    links.new(add_log, A_log_mix.inputs["B"])

    links.new(A_geo, repA_out.inputs["Geometry"])
    links.new(A_log_mix.outputs["Result"], repA_out.inputs["LogDTotal"])
    links.new(int_op("ADD", A_i, 1), repA_out.inputs["IterIdx"])

    logD_total = repA_out.outputs["LogDTotal"]

    # --- 10. Repeat Zone B: SumW = Σ w_i where w_i = Π_{j≠i-1,i} D_j ---
    repB_in = nodes.new("GeometryNodeRepeatInput")
    repB_out = nodes.new("GeometryNodeRepeatOutput")
    repB_in.pair_with_output(repB_out)
    repB_out.repeat_items.new("GEOMETRY", "Geometry")
    repB_out.repeat_items.new("FLOAT", "SumW")
    repB_out.repeat_items.new("INT", "IterIdx")

    links.new(repA_out.outputs["Geometry"], repB_in.inputs["Geometry"])
    links.new(max_N, repB_in.inputs["Iterations"])
    repB_in.inputs["SumW"].default_value = 0.0
    repB_in.inputs["IterIdx"].default_value = 0

    B_geo = repB_in.outputs["Geometry"]
    B_sumw = repB_in.outputs["SumW"]
    B_i = repB_in.outputs["IterIdx"]
    B_valid = compare_int_less(B_i, N_field)

    B_im1 = int_op("MODULO", int_op("ADD", int_op("SUBTRACT", B_i, 1), N_field), N_field)
    D0 = domain_edge_distance(B_i)
    D1 = domain_edge_distance(B_im1)
    D0c = math_op("MAXIMUM", D0, 1.0e-8)
    D1c = math_op("MAXIMUM", D1, 1.0e-8)
    log_w = math_op("SUBTRACT", logD_total, math_op("ADD", math_op("LOGARITHM", D0c), math_op("LOGARITHM", D1c)))
    w_i = math_op("EXPONENT", log_w)
    sum_new = math_op("ADD", B_sumw, w_i)

    B_sum_mix = nodes.new("ShaderNodeMix")
    B_sum_mix.data_type = "FLOAT"
    links.new(B_valid, B_sum_mix.inputs["Factor"])
    links.new(B_sumw, B_sum_mix.inputs["A"])
    links.new(sum_new, B_sum_mix.inputs["B"])

    links.new(B_geo, repB_out.inputs["Geometry"])
    links.new(B_sum_mix.outputs["Result"], repB_out.inputs["SumW"])
    links.new(int_op("ADD", B_i, 1), repB_out.inputs["IterIdx"])

    sumW = repB_out.outputs["SumW"]

    # --- 11. Repeat Zone C: Accumulate surface S = Σ R_i(s_i,d_i) * B_i(d_i) ---
    # IMPORTANT: We also accumulate SumB = Σ B_i(d_i) and normalize S/SumB.
    # Without this, vertices can double-count (e.g. a quad corner contributing from 2 ribbons),
    # which matches the user-observed exact 2x scaling at cube corners.
    repC_in = nodes.new("GeometryNodeRepeatInput")
    repC_out = nodes.new("GeometryNodeRepeatOutput")
    repC_in.pair_with_output(repC_out)
    repC_out.repeat_items.new("GEOMETRY", "Geometry")
    repC_out.repeat_items.new("VECTOR", "SumS")
    repC_out.repeat_items.new("FLOAT", "SumB")
    repC_out.repeat_items.new("INT", "IterIdx")

    links.new(repB_out.outputs["Geometry"], repC_in.inputs["Geometry"])
    links.new(max_N, repC_in.inputs["Iterations"])
    repC_in.inputs["SumS"].default_value = (0, 0, 0)
    repC_in.inputs["SumB"].default_value = 0.0
    repC_in.inputs["IterIdx"].default_value = 0

    C_geo = repC_in.outputs["Geometry"]
    C_sumS = repC_in.outputs["SumS"]
    C_sumB = repC_in.outputs["SumB"]
    C_i = repC_in.outputs["IterIdx"]
    C_valid = compare_int_less(C_i, N_field)

    im1 = int_op("MODULO", int_op("ADD", int_op("SUBTRACT", C_i, 1), N_field), N_field)
    ip1 = int_op("MODULO", int_op("ADD", C_i, 1), N_field)
    im2 = int_op("MODULO", int_op("ADD", int_op("SUBTRACT", C_i, 2), N_field), N_field)
    ip2 = int_op("MODULO", int_op("ADD", C_i, 2), N_field)
    im3 = int_op("MODULO", int_op("ADD", int_op("SUBTRACT", C_i, 3), N_field), N_field)

    # Wachspress λ_i and λ_{i-1}
    Di = math_op("MAXIMUM", domain_edge_distance(C_i), 1.0e-8)
    Dim1 = math_op("MAXIMUM", domain_edge_distance(im1), 1.0e-8)
    Dim2 = math_op("MAXIMUM", domain_edge_distance(im2), 1.0e-8)

    log_w_i = math_op("SUBTRACT", logD_total, math_op("ADD", math_op("LOGARITHM", Di), math_op("LOGARITHM", Dim1)))
    wcur = math_op("EXPONENT", log_w_i)
    lam_i = math_op("DIVIDE", wcur, sumW)

    log_w_im1 = math_op("SUBTRACT", logD_total, math_op("ADD", math_op("LOGARITHM", Dim1), math_op("LOGARITHM", Dim2)))
    wprev = math_op("EXPONENT", log_w_im1)
    lam_im1 = math_op("DIVIDE", wprev, sumW)

    denom = math_op("MAXIMUM", math_op("ADD", lam_im1, lam_i), 1.0e-8)
    s_i = clamp01(math_op("DIVIDE", lam_i, denom))
    d_i = clamp01(math_op("SUBTRACT", 1.0, math_op("ADD", lam_im1, lam_i)))

    # Evaluate boundary curves (paper indexing):
    # - Ribbon index i uses (λ_{i-1}, λ_i) and is 0 on the side between vertices (i-1,i).
    # - Therefore C_i corresponds to the mesh edge between (i-1,i), which is our edge index (i-1).
    # With our edge_for_idx(k) = edge from vertex k -> k+1, this means:
    #   C_i      -> edge_for_idx(i-1) == edge_for_idx(im1)
    #   C_{i-1}  -> edge_for_idx(i-2) == edge_for_idx(im2)
    #   C_{i+1}  -> edge_for_idx(i)   == edge_for_idx(C_i)
    e_i, f_i = edge_for_idx(C_i)
    e_im1, f_im1 = edge_for_idx(im1)
    e_im2, f_im2 = edge_for_idx(im2)
    e_im3, f_im3 = edge_for_idx(im3)
    e_ip1, f_ip1 = edge_for_idx(ip1)

    # Control points for C_i, C_{i-1}, C_{i+1}
    C0, C1, C2, C3 = edge_control_points(e_im1, f_im1)       # C_i
    Cm10, Cm11, Cm12, Cm13 = edge_control_points(e_im2, f_im2)  # C_{i-1}
    Cp10, Cp11, Cp12, Cp13 = edge_control_points(e_i, f_i)      # C_{i+1}

    Ci_si = bezier_eval(C0, C1, C2, C3, s_i)
    Cim1_1md = bezier_eval(Cm10, Cm11, Cm12, Cm13, math_op("SUBTRACT", 1.0, d_i))
    Cip1_d = bezier_eval(Cp10, Cp11, Cp12, Cp13, d_i)

    # Build C_i^{opp} (Eq. 2–3)
    # For C_i^{opp}, we need derivatives of C_{i+2}(0) and C_{i-2}(1).
    # Under the same mapping:
    #   C_{i+2} -> edge_for_idx(i+1) == edge_for_idx(ip1)
    #   C_{i-2} -> edge_for_idx(i-3) == edge_for_idx(im3)
    Cp20, Cp21, Cp22, Cp23 = edge_control_points(e_ip1, f_ip1)   # C_{i+2}
    Cm20, Cm21, Cm22, Cm23 = edge_control_points(e_im3, f_im3)   # C_{i-2}

    d_ip2_0 = bezier_deriv(Cp20, Cp21, Cp22, Cp23, 0.0)  # C'_{i+2}(0)
    d_im2_1 = bezier_deriv(Cm20, Cm21, Cm22, Cm23, 1.0)  # C'_{i-2}(1)

    P0_opp = bezier_eval(Cp10, Cp11, Cp12, Cp13, 1.0)    # C_{i+1}(1)
    P3_opp = bezier_eval(Cm10, Cm11, Cm12, Cm13, 0.0)    # C_{i-1}(0)
    P1_opp = vec_math_op("ADD", P0_opp, vec_math_op("SCALE", d_ip2_0, (1.0 / 3.0)))
    P2_opp = vec_math_op("SUBTRACT", P3_opp, vec_math_op("SCALE", d_im2_1, (1.0 / 3.0)))

    Copp_1ms = bezier_eval(P0_opp, P1_opp, P2_opp, P3_opp, math_op("SUBTRACT", 1.0, s_i))

    # Coons ribbon R_i(s_i, d_i) (Eq. 1)
    termA = vec_math_op("SCALE", Ci_si, math_op("SUBTRACT", 1.0, d_i))
    termB = vec_math_op("SCALE", Copp_1ms, d_i)
    termC = vec_math_op("SCALE", Cim1_1md, math_op("SUBTRACT", 1.0, s_i))
    termD = vec_math_op("SCALE", Cip1_d, s_i)

    # Bilinear correction (Eq. 1 matrix term)
    Ci0 = bezier_eval(C0, C1, C2, C3, 0.0)
    Ci1 = bezier_eval(C0, C1, C2, C3, 1.0)
    Cim10 = bezier_eval(Cm10, Cm11, Cm12, Cm13, 0.0)
    Cip11 = bezier_eval(Cp10, Cp11, Cp12, Cp13, 1.0)

    # lerp along d
    l0 = vec_math_op("ADD", vec_math_op("SCALE", Ci0, math_op("SUBTRACT", 1.0, d_i)),
                     vec_math_op("SCALE", Cim10, d_i))
    l1 = vec_math_op("ADD", vec_math_op("SCALE", Ci1, math_op("SUBTRACT", 1.0, d_i)),
                     vec_math_op("SCALE", Cip11, d_i))
    bilinear = vec_math_op("ADD", vec_math_op("SCALE", l0, math_op("SUBTRACT", 1.0, s_i)),
                           vec_math_op("SCALE", l1, s_i))

    R_i = vec_math_op("SUBTRACT",
                      vec_math_op("ADD", vec_math_op("ADD", termA, termB), vec_math_op("ADD", termC, termD)),
                      bilinear)

    # Blend B_i(d_i) = (1 - d_i)^2  (matches `multisided_coon.md` / Salvi 2020)
    Bi = math_op("POWER", math_op("SUBTRACT", 1.0, d_i), 2.0)
    contrib = vec_math_op("SCALE", R_i, Bi)
    S_new = vec_math_op("ADD", C_sumS, contrib)
    B_new = math_op("ADD", C_sumB, Bi)

    S_mix = nodes.new("GeometryNodeSwitch")
    S_mix.input_type = "VECTOR"
    links.new(C_valid, S_mix.inputs["Switch"])
    links.new(C_sumS, S_mix.inputs["False"])
    links.new(S_new, S_mix.inputs["True"])

    B_mix = nodes.new("GeometryNodeSwitch")
    B_mix.input_type = "FLOAT"
    links.new(C_valid, B_mix.inputs["Switch"])
    links.new(C_sumB, B_mix.inputs["False"])
    links.new(B_new, B_mix.inputs["True"])

    links.new(C_geo, repC_out.inputs["Geometry"])
    links.new(S_mix.outputs["Output"], repC_out.inputs["SumS"])
    links.new(B_mix.outputs["Output"], repC_out.inputs["SumB"])
    links.new(int_op("ADD", C_i, 1), repC_out.inputs["IterIdx"])

    sumS = repC_out.outputs["SumS"]
    sumB = repC_out.outputs["SumB"]
    inv_sumB = math_op("DIVIDE", 1.0, math_op("MAXIMUM", sumB, 1.0e-8))
    final_pos = vec_math_op("SCALE", sumS, inv_sumB)
    
    set_pos = nodes.new("GeometryNodeSetPosition")
    links.new(repC_out.outputs["Geometry"], set_pos.inputs["Geometry"])
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
