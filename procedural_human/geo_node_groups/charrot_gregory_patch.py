import bpy
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import *

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
    group_name = "CoonNGonPatchGenerator"     
    if group_name in bpy.data.node_groups:
        bpy.data.node_groups.remove(bpy.data.node_groups[group_name])

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    
    # --- Interface ---
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Subdivisions", in_out="INPUT", socket_type="NodeSocketInt").default_value = 4
    # Default OFF: merging breaks per-face attribute consistency (orig_loop_start/poly_N)
    # and can create "star" connectivity when multiple face-islands collapse together.
    group.interface.new_socket(name="Merge By Distance", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
  
    nodes = group.nodes    
    links = group.links  

    # --- 1. INPUTS & TOPOLOGY ---
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    orig_geo = group_input.outputs["Geometry"]  

    corner_idx = nodes.new("GeometryNodeInputIndex").outputs[0]
    face_of_corner = nodes.new("GeometryNodeFaceOfCorner")
    links.new(corner_idx, face_of_corner.inputs["Corner Index"])
    face_idx = face_of_corner.outputs["Face Index"]
    
    # --- 3. STORE FACE INDEX ON FACE DOMAIN ---
    # This propagates through split/subdivide so we can look up original corners
    face_idx_node = nodes.new("GeometryNodeInputIndex")  # In FACE context this gives face index

    # Store original loop start ("first corner") per face.
    # This is stable for looking up per-face corners later even after subdiv/split,
    # and avoids using CornersOfFace with face indices from a different geometry.
    corners_of_face = nodes.new("GeometryNodeCornersOfFace")
    links.new(face_idx_node.outputs[0], corners_of_face.inputs["Face Index"])
    corners_of_face.inputs["Sort Index"].default_value = 0

    store_loop_start = create_node(group,"GeometryNodeStoreNamedAttribute", {
        "Name": "orig_loop_start", "Domain": "FACE", "Data Type": "INT",
        "Value": corners_of_face.outputs["Corner Index"]
    })
    links.new(orig_geo, store_loop_start.inputs[0])

    accum_N = create_node(group, "GeometryNodeAccumulateField", {
        "Value": 1, "Group ID": face_idx, "Domain": "CORNER"
    })
    N_total = accum_N.outputs["Total"]
    store_N = create_node(group,"GeometryNodeStoreNamedAttribute", {
        "Name": "poly_N", "Domain": "FACE", "Data Type": "INT",
        "Value": N_total
    })
    links.new(store_loop_start.outputs[0], store_N.inputs[0])

    # --- 4. STORE EDGE INFO ON CORNERS ---
    edges_of_corner = nodes.new("GeometryNodeEdgesOfCorner")
    links.new(corner_idx, edges_of_corner.inputs["Corner Index"])
    
    store_edge_idx = create_node(group,"GeometryNodeStoreNamedAttribute", {
        "Name": "corner_edge_idx", "Domain": "CORNER", "Data Type": "INT",
        "Value": edges_of_corner.outputs["Previous Edge Index"]
    })
    links.new(store_N.outputs[0], store_edge_idx.inputs[0])
    
    vertex_of_corner = nodes.new("GeometryNodeVertexOfCorner")
    links.new(corner_idx, vertex_of_corner.inputs["Corner Index"])
    edge_verts = nodes.new("GeometryNodeInputMeshEdgeVertices")
    sample_edge_v1 = create_node(group,"GeometryNodeSampleIndex", {
        "Geometry": orig_geo,
        "Domain": "EDGE", "Data Type": "INT",
        "Index": edges_of_corner.outputs["Previous Edge Index"]
    })
    links.new(edge_verts.outputs["Vertex Index 2"], sample_edge_v1.inputs["Value"])
    is_fwd_cmp = create_node(group,"FunctionNodeCompare", {"Data Type": "INT", "Operation": "EQUAL"})
    links.new(vertex_of_corner.outputs["Vertex Index"], is_fwd_cmp.inputs["A"])
    links.new(sample_edge_v1.outputs[0], is_fwd_cmp.inputs["B"])
    store_is_fwd = create_node(group,"GeometryNodeStoreNamedAttribute", {
        "Name": "edge_is_forward", "Domain": "CORNER", "Data Type": "BOOLEAN",
        "Value": is_fwd_cmp.outputs["Result"]
    })
    links.new(store_edge_idx.outputs[0], store_is_fwd.inputs[0])
    prepared_geo = store_is_fwd.outputs[0]
    
    
    accum_idx = create_node(group, "GeometryNodeAccumulateField", {
        "Value": 1, 
        "Group ID": face_idx, 
        "Domain": "CORNER"
    })
    local_i = math_op(group, "SUBTRACT", accum_idx.outputs["Trailing"], 1)
    
    # 2. Calculate Angle theta (Matches paper/original code logic)
    # theta_i = (i + 0.5) * 2π / N + π
    N_field = get_attr(group, "poly_N", "INT") # This must be available on Corner domain
    # Note: Ensure poly_N is stored on CORNER or reachable. 
    # In previous code it was FACE. Let's sample it or use the accum total from before.
    N_val = accum_idx.outputs["Total"] 

    two_pi = 6.283185307
    angle_step = math_op(group, "DIVIDE", two_pi, int_to_float(group, N_val))
    i_float = int_to_float(group, local_i)
    base_angle = math_op(group, "MULTIPLY", math_op(group, "ADD", i_float, 0.5), angle_step)
    theta_i = math_op(group, "ADD", base_angle, 3.14159265)
    
    uv_x = math_op(group, "COSINE", theta_i)
    uv_y = math_op(group, "SINE", theta_i)
    
    uv_vec = nodes.new("ShaderNodeCombineXYZ")
    links.new(uv_x, uv_vec.inputs["X"])
    links.new(uv_y, uv_vec.inputs["Y"])
    
    # 3. Store as attribute to be interpolated
    store_uv = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Name": "domain_uv_interp", "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Value": uv_vec.outputs[0]
    })
    links.new(prepared_geo, store_uv.inputs[0])
    geo_with_uv = store_uv.outputs[0]

    # --- 5. SPLIT & SUBDIVIDE ---
    split = create_node(group,"GeometryNodeSplitEdges", {"Mesh": geo_with_uv})
    subdiv = create_node(group,"GeometryNodeSubdivideMesh", {
        "Mesh": split.outputs[0],
        "Level": group_input.outputs["Subdivisions"]
    })
    subdivided_geo = subdiv.outputs[0]

    # --- RETRIEVE INTERPOLATED DOMAIN POS ---
    # This replaces the entire Mean Value Coordinate Repeat Zone
    domain_uv_node = nodes.new("GeometryNodeInputNamedAttribute")
    domain_uv_node.data_type = "FLOAT_VECTOR"
    domain_uv_node.inputs["Name"].default_value = "domain_uv_interp"
    
    sep_uv = nodes.new("ShaderNodeSeparateXYZ")
    links.new(domain_uv_node.outputs[0], sep_uv.inputs[0])
    domain_p_x = sep_uv.outputs["X"]
    domain_p_y = sep_uv.outputs["Y"]

    # Calculate Max N for loop iterations
    stat_N = create_node(group,"GeometryNodeAttributeStatistic", {
        "Geometry": subdivided_geo, "Domain": "POINT", "Attribute": N_field
    })
    max_N = stat_N.outputs["Max"]
    
   # --- Loop B: Sum Weights ---
    repB_in = nodes.new("GeometryNodeRepeatInput")
    repB_out = nodes.new("GeometryNodeRepeatOutput")
    repB_in.pair_with_output(repB_out)
    repB_out.repeat_items.new("GEOMETRY", "Geometry")
    repB_out.repeat_items.new("FLOAT", "SumW")
    repB_out.repeat_items.new("INT", "IterIdx")

    links.new(subdivided_geo, repB_in.inputs["Geometry"]) # Skipped Loop A geometry
    links.new(max_N, repB_in.inputs["Iterations"])
    repB_in.inputs["SumW"].default_value = 0.0
    repB_in.inputs["IterIdx"].default_value = 0

    B_geo = repB_in.outputs["Geometry"]
    B_sumw = repB_in.outputs["SumW"]
    B_i = repB_in.outputs["IterIdx"]
    
    B_valid = compare_int_less(group, B_i, N_field)
    B_ip1 = int_op(group, "MODULO", int_op(group, "ADD", B_i, 1), N_field)
    
    D0 = domain_edge_distance_node(group, B_i, N_field, domain_p_x, domain_p_y)
    D1 = domain_edge_distance_node(group, B_ip1, N_field, domain_p_x, domain_p_y)
    
    # w_i = 1.0 / (D0 * D1)
    # Clamp distances to avoid division by zero
    D0_safe = math_op(group, "MAXIMUM", D0, 1e-8)
    D1_safe = math_op(group, "MAXIMUM", D1, 1e-8)
    denom = math_op(group, "MULTIPLY", D0_safe, D1_safe)
    w_i = math_op(group, "DIVIDE", 1.0, denom)
    
    sum_new = math_op(group, "ADD", B_sumw, w_i)
    B_sum_final = switch_float(group, B_valid, B_sumw, sum_new)

    links.new(B_geo, repB_out.inputs["Geometry"])
    links.new(B_sum_final, repB_out.inputs["SumW"])
    links.new(int_op(group, "ADD", B_i, 1), repB_out.inputs["IterIdx"])
    
    sumW = repB_out.outputs["SumW"]

    orig_loop_start_field = get_attr(group, "orig_loop_start", "INT")

    # --- 11. Repeat Zone C: Accumulate surface S = Σ R_i(s_i,d_i) * B_i(d_i) ---
    repC_in = nodes.new("GeometryNodeRepeatInput")
    repC_out = nodes.new("GeometryNodeRepeatOutput")
    repC_in.pair_with_output(repC_out)
    repC_out.repeat_items.new("GEOMETRY", "Geometry")
    repC_out.repeat_items.new("VECTOR", "SumS")
    repC_out.repeat_items.new("FLOAT", "SumB") # Note: This SumB is for blending function B_i, distinct from SumW
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
    C_valid = compare_int_less(group, C_i, N_field)

    im1 = int_op(group, "MODULO", int_op(group, "ADD", int_op(group, "SUBTRACT", C_i, 1), N_field), N_field)
    ip1 = int_op(group, "MODULO", int_op(group, "ADD", C_i, 1), N_field)
    im2 = int_op(group, "MODULO", int_op(group, "ADD", int_op(group, "SUBTRACT", C_i, 2), N_field), N_field)
    ip2 = int_op(group, "MODULO", int_op(group, "ADD", C_i, 2), N_field)
    Di = math_op(group, "MAXIMUM", domain_edge_distance_node(group, C_i, N_field, domain_p_x, domain_p_y), 1.0e-8)
    Dip1 = math_op(group, "MAXIMUM", domain_edge_distance_node(group, ip1, N_field, domain_p_x, domain_p_y), 1.0e-8)
    wcur = math_op(group, "DIVIDE", 1.0, math_op(group, "MULTIPLY", Di, Dip1))
    lam_i = math_op(group, "DIVIDE", wcur, sumW)
    Dim1 = math_op(group, "MAXIMUM", domain_edge_distance_node(group, im1, N_field, domain_p_x, domain_p_y), 1.0e-8)
    wprev = math_op(group, "DIVIDE", 1.0, math_op(group, "MULTIPLY", Dim1, Di))
    lam_im1 = math_op(group, "DIVIDE", wprev, sumW)

    denom = math_op(group, "MAXIMUM", math_op(group, "ADD", lam_im1, lam_i), 1.0e-8)
    
    # Raw s_i, d_i from Wachspress coordinates
    s_i_raw = clamp01(group, math_op(group, "DIVIDE", lam_i, denom))
    d_i_raw = clamp01(group, math_op(group, "SUBTRACT", 1.0, math_op(group, "ADD", lam_im1, lam_i)))
    
    s_i = smoother_step(group, s_i_raw)
    d_i = smoother_step(group, d_i_raw)

    # Evaluate boundary curves (paper indexing) with *incoming-edge* semantics:
    # We stored `corner_edge_idx` as EdgesOfCorner.Previous Edge Index, i.e. the incoming edge at corner i,
    # which is exactly the side between vertices (i-1, i). Therefore:
    #   C_i      -> edge_for_idx(i)
    #   C_{i-1}  -> edge_for_idx(i-1)
    #   C_{i+1}  -> edge_for_idx(i+1)
    # and for opp curve derivatives:
    #   C'_{i+2}(0) -> edge_for_idx(i+2)
    #   C'_{i-2}(1) -> edge_for_idx(i-2)
    e_i, f_i = edge_for_idx(group, C_i, orig_loop_start_field, prepared_geo)     # C_i 
    e_im1, f_im1 = edge_for_idx(group, im1, orig_loop_start_field, prepared_geo) # C_{i-1}
    e_ip1, f_ip1 = edge_for_idx(group, ip1, orig_loop_start_field, prepared_geo) # C_{i+1}

    # Control points for C_i, C_{i-1}, C_{i+1}
    C0, C1, C2, C3 = edge_control_points_node(group, e_i, f_i, orig_geo)              # C_i
    Cm10, Cm11, Cm12, Cm13 = edge_control_points_node(group, e_im1, f_im1, orig_geo)  # C_{i-1}
    Cp10, Cp11, Cp12, Cp13 = edge_control_points_node(group, e_ip1, f_ip1, orig_geo)  # C_{i+1}

    Ci_si = bezier_eval_node(group, C0, C1, C2, C3, s_i)
    Cim1_1md = bezier_eval_node(group, Cm10, Cm11, Cm12, Cm13, math_op(group, "SUBTRACT", 1.0, d_i))
    Cip1_d = bezier_eval_node(group, Cp10, Cp11, Cp12, Cp13, d_i)

    # Build C_i^{opp} (Eq. 2–3)
    e_ip2, f_ip2 = edge_for_idx(group, ip2, orig_loop_start_field, prepared_geo) # C_{i+2}
    e_im2, f_im2 = edge_for_idx(group, im2, orig_loop_start_field, prepared_geo) # C_{i-2}

    Cp20, Cp21, Cp22, Cp23 = edge_control_points_node(group, e_ip2, f_ip2, orig_geo)   # C_{i+2}
    Cm20, Cm21, Cm22, Cm23 = edge_control_points_node(group, e_im2, f_im2, orig_geo)   # C_{i-2}

    d_ip2_0 = bezier_deriv(group, Cp20, Cp21, Cp22, Cp23, 0.0)  # C'_{i+2}(0)
    d_im2_1 = bezier_deriv(group, Cm20, Cm21, Cm22, Cm23, 1.0)  # C'_{i-2}(1)

    P0_opp = bezier_eval_node(group, Cp10, Cp11, Cp12, Cp13, 1.0)    # C_{i+1}(1)
    P3_opp = bezier_eval_node(group, Cm10, Cm11, Cm12, Cm13, 0.0)    # C_{i-1}(0)
    P1_opp = vec_math_op(group, "ADD", P0_opp, vec_math_op(group, "SCALE", d_ip2_0, (1.0 / 3.0)))
    P2_opp = vec_math_op(group, "SUBTRACT", P3_opp, vec_math_op(group, "SCALE", d_im2_1, (1.0 / 3.0)))

    Copp_1ms = bezier_eval_node(group, P0_opp, P1_opp, P2_opp, P3_opp, math_op(group, "SUBTRACT", 1.0, s_i))

    # Coons ribbon R_i(s_i, d_i) (Eq. 1)
    termA = vec_math_op(group, "SCALE", Ci_si, math_op(group, "SUBTRACT", 1.0, d_i))
    termB = vec_math_op(group, "SCALE", Copp_1ms, d_i)
    termC = vec_math_op(group, "SCALE", Cim1_1md, math_op(group, "SUBTRACT", 1.0, s_i))
    termD = vec_math_op(group, "SCALE", Cip1_d, s_i)

    # Bilinear correction (Eq. 1 matrix term)
    Ci0 = bezier_eval_node(group, C0, C1, C2, C3, 0.0)
    Ci1 = bezier_eval_node(group, C0, C1, C2, C3, 1.0)
    Cim10 = bezier_eval_node(group, Cm10, Cm11, Cm12, Cm13, 0.0)
    Cip11 = bezier_eval_node(group, Cp10, Cp11, Cp12, Cp13, 1.0)

    # lerp along d
    l0 = vec_math_op(group, "ADD", vec_math_op(group, "SCALE", Ci0, math_op(group, "SUBTRACT", 1.0, d_i)),
                     vec_math_op(group, "SCALE", Cim10, d_i))
    l1 = vec_math_op(group, "ADD", vec_math_op(group, "SCALE", Ci1, math_op(group, "SUBTRACT", 1.0, d_i)),
                     vec_math_op(group, "SCALE", Cip11, d_i))
    bilinear = vec_math_op(group, "ADD", vec_math_op(group, "SCALE", l0, math_op(group, "SUBTRACT", 1.0, s_i)),
                           vec_math_op(group, "SCALE", l1, s_i))

    R_i = vec_math_op(group, "SUBTRACT",
                      vec_math_op(group, "ADD", vec_math_op(group, "ADD", termA, termB), vec_math_op(group, "ADD", termC, termD)),
                      bilinear)

    # Blend B_i(d_i) = (1 - d_i)^2  (matches `multisided_coon.md` / Salvi 2020)
    Bi = math_op(group, "POWER", math_op(group, "SUBTRACT", 1.0, d_i), 2.0)
    contrib = vec_math_op(group, "SCALE", R_i, Bi)
    S_new = vec_math_op(group, "ADD", C_sumS, contrib)
    B_new = math_op(group, "ADD", C_sumB, Bi)

    S_final = switch_vec(group, C_valid, C_sumS, S_new)
    B_final = switch_float(group, C_valid, C_sumB, B_new)

    links.new(C_geo, repC_out.inputs["Geometry"])
    links.new(S_final, repC_out.inputs["SumS"])
    links.new(B_final, repC_out.inputs["SumB"])
    links.new(int_op(group, "ADD", C_i, 1), repC_out.inputs["IterIdx"])

    sumS = repC_out.outputs["SumS"]
    sumB = repC_out.outputs["SumB"]
    inv_sumB = math_op(group, "DIVIDE", 1.0, math_op(group, "MAXIMUM", sumB, 1.0e-8))
    final_pos_raw = vec_math_op(group, "SCALE", sumS, inv_sumB)
    
    set_pos = nodes.new("GeometryNodeSetPosition")
    links.new(repC_out.outputs["Geometry"], set_pos.inputs["Geometry"])
    links.new(final_pos_raw, set_pos.inputs["Position"])


    # Optional: merge vertices back together.
    # NOTE: During debugging, disabling this avoids averaging attributes/positions at shared corners.
    merge = create_node(group,"GeometryNodeMergeByDistance", {
        "Geometry": set_pos.outputs[0], "Distance": 0.0001
    })

    geom_after_merge = switch_node(group, "GEOMETRY",
                                   group_input.outputs["Merge By Distance"],
                                   set_pos.outputs[0],
                                   merge.outputs[0])
    
    # Smooth shading
    set_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    links.new(geom_after_merge, set_smooth.inputs[0])
    set_smooth.inputs["Shade Smooth"].default_value = True
    
    links.new(set_smooth.outputs[0], group_output.inputs[0])
    
    auto_layout_nodes(group)
    return group
