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
    
    # --- 2. STORE CORNER POSITIONS ---
    vert_of_corner = nodes.new("GeometryNodeVertexOfCorner")
    links.new(corner_idx, vert_of_corner.inputs["Corner Index"])
    
    sample_corner_pos = create_node(group,"GeometryNodeSampleIndex", {
        "Geometry": orig_geo, "Domain": "POINT", "Data Type": "FLOAT_VECTOR",
        "Index": vert_of_corner.outputs["Vertex Index"]
    })
    pos_node = nodes.new("GeometryNodeInputPosition")
    links.new(pos_node.outputs[0], sample_corner_pos.inputs["Value"])
    corner_pos = sample_corner_pos.outputs[0]

    store_corner_pos = create_node(group,"GeometryNodeStoreNamedAttribute", {
        "Name": "corner_pos", "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Value": corner_pos
    })
    links.new(orig_geo, store_corner_pos.inputs[0])
    
    
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
    links.new(store_corner_pos.outputs[0], store_loop_start.inputs[0])

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
    
    # --- 4.2 COMPUTE AND STORE FACE WINDING (before split/subdivide) ---
    # The domain polygon vertices are arranged CCW. If the mesh face's corners wind CW,
    # we need to flip the domain vertex order to prevent a "twisted" mapping.
    # Compute winding per-face BEFORE split, so it propagates through subdivision.
    
    # Get face corner positions using corners_of_face
    cof_winding = nodes.new("GeometryNodeCornersOfFace")
    face_idx_node = nodes.new("GeometryNodeInputIndex")  # In FACE context, this is face index
    links.new(face_idx_node.outputs[0], cof_winding.inputs["Face Index"])

    wc0 = sample_face_corner_pos(group, face_idx_node, prepared_geo, 0)
    wc1 = sample_face_corner_pos(group, face_idx_node, prepared_geo, 1)
    wc2 = sample_face_corner_pos(group, face_idx_node, prepared_geo, 2)
    wc3 = sample_face_corner_pos(group, face_idx_node, prepared_geo, 3) 
    
    # Compute cross product of two edges to get face normal direction
    edge01_w = vec_math_op(group, "SUBTRACT", wc1, wc0)
    edge02_w = vec_math_op(group, "SUBTRACT", wc2, wc0)
    face_normal_w = vec_math_op(group, "CROSS_PRODUCT", edge01_w, edge02_w)
    
    # Compute face center
    fc_01 = vec_math_op(group, "ADD", wc0, wc1)
    fc_012 = vec_math_op(group, "ADD", fc_01, wc2)
    fc_sum = vec_math_op(group, "ADD", fc_012, wc3)
    face_center_w = vec_math_op(group, "SCALE", fc_sum, 0.25)
    
    # Dot product of face_center and face_normal
    # For a cube centered at origin: if dot < 0, face normal points inward (CW winding)
    center_dot_w = vec_math_op(group, "DOT_PRODUCT", face_center_w, face_normal_w)
    
    flip_cmp = nodes.new("FunctionNodeCompare")
    flip_cmp.data_type = "FLOAT"
    flip_cmp.operation = "LESS_THAN"
    links.new(center_dot_w, flip_cmp.inputs["A"])
    flip_cmp.inputs["B"].default_value = 0.0
    face_flip_domain = flip_cmp.outputs["Result"]
    
    # Store flip_domain on FACE domain (will propagate through split/subdivide)
    store_flip = create_node(group,"GeometryNodeStoreNamedAttribute", {
        "Name": "face_flip_domain", "Domain": "FACE", "Data Type": "BOOLEAN",
        "Value": face_flip_domain
    })
    links.new(prepared_geo, store_flip.inputs[0])
    prepared_geo_with_flip = store_flip.outputs[0]
    
# --- 5. SPLIT & SUBDIVIDE ---
    split = create_node(group,"GeometryNodeSplitEdges", {"Mesh": prepared_geo_with_flip})
    
    subdiv = create_node(group,"GeometryNodeSubdivideMesh", {
        "Mesh": split.outputs[0],
        "Level": group_input.outputs["Subdivisions"]
    })
    subdivided_geo = subdiv.outputs[0]
    
    # --- 6. COMPUTE DOMAIN POSITION USING MEAN VALUE COORDINATES ---
    # FIX: Instead of interpolating pre-stored domain positions (which doesn't work),
    # we compute domain_pos at each point using generalized barycentric coordinates.
    # 
    # For each point P after subdivision:
    # 1. Get the N corner positions C_0, ..., C_{N-1} from original geometry
    # 2. Compute mean value coordinates λ_i of P w.r.t. C_i
    # 3. Compute domain_pos = Σ λ_i × domain_corner_i
    #    where domain_corner_i = (cos((i+0.5)*2π/N), sin((i+0.5)*2π/N))
    
    N_field = get_attr(group, "poly_N", "INT")
    orig_loop_start_field = get_attr(group, "orig_loop_start", "INT")
    
    # Get current point position
    current_pos = nodes.new("GeometryNodeInputPosition").outputs[0]

    # --- 6.0 Determine max N across patches (repeat iterations) ---
    stat_N_temp = create_node(group,"GeometryNodeAttributeStatistic", {
        "Geometry": subdivided_geo, "Domain": "POINT", "Attribute": N_field
    })
    max_N_for_bary = stat_N_temp.outputs["Max"]
    
    # --- 6.1 COMPUTE MEAN VALUE COORDINATES ---
    # Repeat Zone to compute sum of weights and weighted domain position
    # Mean value coordinates: w_i = (tan(α_{i-1}/2) + tan(α_i/2)) / |P - C_i|
    # where α_i is the angle at P subtended by edge (C_i, C_{i+1})
    
    repMV_in = nodes.new("GeometryNodeRepeatInput")
    repMV_out = nodes.new("GeometryNodeRepeatOutput")
    repMV_in.pair_with_output(repMV_out)
    
    repMV_out.repeat_items.new("GEOMETRY", "Geometry")
    repMV_out.repeat_items.new("FLOAT", "SumW")  # Sum of weights
    repMV_out.repeat_items.new("VECTOR", "SumDomain")  # Weighted sum of domain positions
    repMV_out.repeat_items.new("INT", "IterIdx")
    
    links.new(subdivided_geo, repMV_in.inputs["Geometry"])
    links.new(max_N_for_bary, repMV_in.inputs["Iterations"])
    repMV_in.inputs["SumW"].default_value = 0.0
    repMV_in.inputs["SumDomain"].default_value = (0.0, 0.0, 0.0)
    repMV_in.inputs["IterIdx"].default_value = 0
    
    MV_geo = repMV_in.outputs["Geometry"]
    MV_sumW = repMV_in.outputs["SumW"]
    MV_sumDomain = repMV_in.outputs["SumDomain"]
    MV_i = repMV_in.outputs["IterIdx"]
    
    # Check if this iteration is valid for this face
    MV_valid = compare_int_less(group, MV_i, N_field)
    
    # Get corner index for this iteration
    MV_corner_idx = int_op(group, "ADD", orig_loop_start_field, MV_i)
    
    # Sample corner position from original geometry
    sample_corner_i = create_node(group,"GeometryNodeSampleIndex", {
        "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Index": MV_corner_idx
    })
    corner_pos_attr = nodes.new("GeometryNodeInputNamedAttribute")
    corner_pos_attr.data_type = "FLOAT_VECTOR"
    corner_pos_attr.inputs["Name"].default_value = "corner_pos"
    links.new(corner_pos_attr.outputs[0], sample_corner_i.inputs["Value"])
    corner_i_pos = sample_corner_i.outputs[0]
    
    # Get next corner position
    MV_ip1 = int_op(group, "MODULO", int_op(group, "ADD", MV_i, 1), N_field)
    MV_corner_ip1 = int_op(group, "ADD", orig_loop_start_field, MV_ip1)
    sample_corner_ip1 = create_node(group,"GeometryNodeSampleIndex", {
        "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Index": MV_corner_ip1
    })
    links.new(corner_pos_attr.outputs[0], sample_corner_ip1.inputs["Value"])
    corner_ip1_pos = sample_corner_ip1.outputs[0]
    
    # Get previous corner position
    MV_im1 = int_op(group, "MODULO", int_op(group, "ADD", int_op(group, "SUBTRACT", MV_i, 1), N_field), N_field)
    MV_corner_im1 = int_op(group, "ADD", orig_loop_start_field, MV_im1)
    sample_corner_im1 = create_node(group,"GeometryNodeSampleIndex", {
        "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Index": MV_corner_im1
    })
    links.new(corner_pos_attr.outputs[0], sample_corner_im1.inputs["Value"])
    corner_im1_pos = sample_corner_im1.outputs[0]
    
    # Compute vectors from current point to corners
    v_to_i = vec_math_op(group, "SUBTRACT", corner_i_pos, current_pos)
    v_to_ip1 = vec_math_op(group, "SUBTRACT", corner_ip1_pos, current_pos)
    v_to_im1 = vec_math_op(group, "SUBTRACT", corner_im1_pos, current_pos)
    
    # Distance to corner i
    dist_i = vec_math_op(group, "LENGTH", v_to_i)
    dist_i_safe = math_op(group, "MAXIMUM", dist_i, 1e-8)
    
    # Compute angle α_i at P subtended by edge (C_i, C_{i+1})
    # cos(α_i) = dot(v_to_i, v_to_ip1) / (|v_to_i| * |v_to_ip1|)
    dot_i_ip1 = vec_math_op(group,  "DOT_PRODUCT", v_to_i, v_to_ip1)
    dist_ip1 = vec_math_op(group, "LENGTH", v_to_ip1)
    cos_alpha_i = math_op(group, "DIVIDE", dot_i_ip1, 
                          math_op(group, "MAXIMUM", math_op(group, "MULTIPLY", dist_i, dist_ip1), 1e-8))

    
    # Compute angle α_{i-1} at P subtended by edge (C_{i-1}, C_i)
    dot_im1_i = vec_math_op(group, "DOT_PRODUCT", v_to_im1, v_to_i)
    dist_im1 = vec_math_op(group, "LENGTH", v_to_im1)
    cos_alpha_im1 = math_op(group, "DIVIDE", dot_im1_i,
                            math_op(group, "MAXIMUM", math_op(group, "MULTIPLY", dist_im1, dist_i), 1e-8))
    
    tan_half_i = tan_half_angle(group, cos_alpha_i)
    tan_half_im1 = tan_half_angle(group, cos_alpha_im1)
    
    # Mean value weight: w_i = (tan(α_{i-1}/2) + tan(α_i/2)) / |P - C_i|
    weight_i = math_op(group, "DIVIDE", 
                       math_op(group, "ADD", tan_half_im1, tan_half_i),
                       dist_i_safe)
    
    # Compute domain position for corner i
    # theta_i = (i + 0.5) * 2π / N + π
    # If flip_domain is true, we negate the angle to reverse the vertex order (CW instead of CCW)
    N_float = int_to_float(group, N_field)
    i_float = int_to_float(group, MV_i)
    
    # Base angle (CCW order)
    angle_step = math_op(group, "DIVIDE", 6.283185307, N_float)
    base_angle = math_op(group, "MULTIPLY", math_op(group, "ADD", i_float, 0.5), angle_step)
    theta_ccw = math_op(group, "ADD", base_angle, 3.14159265)
    
    # Flipped angle (CW order) - negate the base angle before adding offset
    theta_cw = math_op(group, "SUBTRACT", 3.14159265, base_angle)
    
    # Select based on flip_domain
    theta_i = theta_ccw
    
    domain_corner_x = math_op(group, "COSINE", theta_i)
    domain_corner_y = math_op(group, "SINE", theta_i)
    
    # Weighted domain position contribution
    domain_contrib = nodes.new("ShaderNodeCombineXYZ")
    links.new(math_op(group, "MULTIPLY", weight_i, domain_corner_x), domain_contrib.inputs["X"])
    links.new(math_op(group, "MULTIPLY", weight_i, domain_corner_y), domain_contrib.inputs["Y"])
    
    # Accumulate (only if valid)
    new_sumW = switch_float(group, MV_valid, MV_sumW, math_op(group, "ADD", MV_sumW, weight_i))
    new_sumDomain = switch_vec(group, MV_valid, MV_sumDomain, 
                               vec_math_op(group, "ADD", MV_sumDomain, domain_contrib.outputs[0]))
    
    # Output from repeat
    links.new(MV_geo, repMV_out.inputs["Geometry"])
    links.new(new_sumW, repMV_out.inputs["SumW"])
    links.new(new_sumDomain, repMV_out.inputs["SumDomain"])
    links.new(int_op(group, "ADD", MV_i, 1), repMV_out.inputs["IterIdx"])
    
    # Normalize to get final domain position
    final_sumW = repMV_out.outputs["SumW"]
    final_sumDomain = repMV_out.outputs["SumDomain"]
    inv_sumW = math_op(group, "DIVIDE", 1.0, math_op(group, "MAXIMUM", final_sumW, 1e-8))
    domain_pos_vec = vec_math_op(group, "SCALE", final_sumDomain, inv_sumW)
    
    sep_domain_final = nodes.new("ShaderNodeSeparateXYZ")
    links.new(domain_pos_vec, sep_domain_final.inputs[0])
    domain_p_x = sep_domain_final.outputs["X"]
    domain_p_y = sep_domain_final.outputs["Y"]

    # --- 6.2 Determine max N across patches (repeat iterations) ---
    stat_N = create_node(group,"GeometryNodeAttributeStatistic", {
        "Geometry": subdivided_geo, "Domain": "POINT", "Attribute": N_field
    })
    max_N = stat_N.outputs["Max"]


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
    A_valid = compare_int_less(group, A_i, N_field)

    D_i = domain_edge_distance(group, A_i, N_field, domain_p_x, domain_p_y)
    D_i_clamp = math_op(group, "MAXIMUM", D_i, 1.0e-8)
    # FIX: Explicitly use base e (2.718281828) for natural log - Blender defaults to base 2!
    add_log = math_op(group, "ADD", A_log, math_op(group, "LOGARITHM", D_i_clamp, 2.718281828))

    A_log_final = switch_float(group, A_valid, A_log, add_log)

    links.new(A_geo, repA_out.inputs["Geometry"])
    links.new(A_log_final, repA_out.inputs["LogDTotal"])
    links.new(int_op(group, "ADD", A_i, 1), repA_out.inputs["IterIdx"])

    logD_total = repA_out.outputs["LogDTotal"]

    # --- 10. Repeat Zone B: SumW = Σ w_i where w_i excludes D_i and D_{i+1} ---
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
    B_valid = compare_int_less(group, B_i, N_field)
    B_ip1 = int_op(group, "MODULO", int_op(group, "ADD", B_i, 1), N_field)
    D0 = domain_edge_distance(group, B_i, N_field, domain_p_x, domain_p_y)   # Edge i (ends at vertex i)
    D1 = domain_edge_distance(group, B_ip1, N_field, domain_p_x, domain_p_y) # Edge i+1 (starts at vertex i) 
    
    D0c = math_op(group, "MAXIMUM", D0, 1.0e-8)
    D1c = math_op(group, "MAXIMUM", D1, 1.0e-8)
    log_w = math_op(group, "SUBTRACT", logD_total, math_op(group, "ADD", math_op(group, "LOGARITHM", D0c, 2.718281828), math_op(group, "LOGARITHM", D1c, 2.718281828)))
    w_i = math_op(group, "EXPONENT", log_w)
    sum_new = math_op(group, "ADD", B_sumw, w_i)
    B_sum_final = switch_float(group, B_valid, B_sumw, sum_new)

    links.new(B_geo, repB_out.inputs["Geometry"])
    links.new(B_sum_final, repB_out.inputs["SumW"])
    links.new(int_op(group, "ADD", B_i, 1), repB_out.inputs["IterIdx"])
    
    sumW = repB_out.outputs["SumW"]

    # --- 11. Repeat Zone C: Accumulate surface S = Σ R_i(s_i,d_i) * B_i(d_i) ---
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
    C_valid = compare_int_less(group, C_i, N_field)

    im1 = int_op(group, "MODULO", int_op(group, "ADD", int_op(group, "SUBTRACT", C_i, 1), N_field), N_field)
    ip1 = int_op(group, "MODULO", int_op(group, "ADD", C_i, 1), N_field)
    im2 = int_op(group, "MODULO", int_op(group, "ADD", int_op(group, "SUBTRACT", C_i, 2), N_field), N_field)
    ip2 = int_op(group, "MODULO", int_op(group, "ADD", C_i, 2), N_field)

    # Wachspress λ_i for vertex i: excludes edges i and (i+1) meeting at vertex i
    Di = math_op(group, "MAXIMUM", domain_edge_distance(group, C_i, N_field, domain_p_x, domain_p_y), 1.0e-8)
    Dip1 = math_op(group, "MAXIMUM", domain_edge_distance(group, ip1, N_field, domain_p_x, domain_p_y), 1.0e-8)
    
    log_w_i = math_op(group, "SUBTRACT", logD_total, math_op(group, "ADD", math_op(group, "LOGARITHM", Di, 2.718281828), math_op(group, "LOGARITHM", Dip1, 2.718281828)))
    wcur = math_op(group, "EXPONENT", log_w_i)
    lam_i = math_op(group, "DIVIDE", wcur, sumW)
 
    # Wachspress λ_{i-1} for vertex (i-1): excludes edges (i-1) and i meeting at vertex (i-1)
    Dim1 = math_op(group, "MAXIMUM", domain_edge_distance(group, im1, N_field, domain_p_x, domain_p_y), 1.0e-8)

    log_w_im1 = math_op(group, "SUBTRACT", logD_total, math_op(group, "ADD", math_op(group, "LOGARITHM", Dim1, 2.718281828), math_op(group, "LOGARITHM", Di, 2.718281828)))
    wprev = math_op(group, "EXPONENT", log_w_im1)
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
    C0, C1, C2, C3 = edge_control_points(group, e_i, f_i, orig_geo)              # C_i
    Cm10, Cm11, Cm12, Cm13 = edge_control_points(group, e_im1, f_im1, orig_geo)  # C_{i-1}
    Cp10, Cp11, Cp12, Cp13 = edge_control_points(group, e_ip1, f_ip1, orig_geo)  # C_{i+1}

    Ci_si = bezier_eval(group, C0, C1, C2, C3, s_i)
    Cim1_1md = bezier_eval(group, Cm10, Cm11, Cm12, Cm13, math_op(group, "SUBTRACT", 1.0, d_i))
    Cip1_d = bezier_eval(group, Cp10, Cp11, Cp12, Cp13, d_i)

    # Build C_i^{opp} (Eq. 2–3)
    e_ip2, f_ip2 = edge_for_idx(group, ip2, orig_loop_start_field, prepared_geo) # C_{i+2}
    e_im2, f_im2 = edge_for_idx(group, im2, orig_loop_start_field, prepared_geo) # C_{i-2}

    Cp20, Cp21, Cp22, Cp23 = edge_control_points(group, e_ip2, f_ip2, orig_geo)   # C_{i+2}
    Cm20, Cm21, Cm22, Cm23 = edge_control_points(group, e_im2, f_im2, orig_geo)   # C_{i-2}

    d_ip2_0 = bezier_deriv(group, Cp20, Cp21, Cp22, Cp23, 0.0)  # C'_{i+2}(0)
    d_im2_1 = bezier_deriv(group, Cm20, Cm21, Cm22, Cm23, 1.0)  # C'_{i-2}(1)

    P0_opp = bezier_eval(group, Cp10, Cp11, Cp12, Cp13, 1.0)    # C_{i+1}(1)
    P3_opp = bezier_eval(group, Cm10, Cm11, Cm12, Cm13, 0.0)    # C_{i-1}(0)
    P1_opp = vec_math_op(group, "ADD", P0_opp, vec_math_op(group, "SCALE", d_ip2_0, (1.0 / 3.0)))
    P2_opp = vec_math_op(group, "SUBTRACT", P3_opp, vec_math_op(group, "SCALE", d_im2_1, (1.0 / 3.0)))

    Copp_1ms = bezier_eval(group, P0_opp, P1_opp, P2_opp, P3_opp, math_op(group, "SUBTRACT", 1.0, s_i))

    # Coons ribbon R_i(s_i, d_i) (Eq. 1)
    termA = vec_math_op(group, "SCALE", Ci_si, math_op(group, "SUBTRACT", 1.0, d_i))
    termB = vec_math_op(group, "SCALE", Copp_1ms, d_i)
    termC = vec_math_op(group, "SCALE", Cim1_1md, math_op(group, "SUBTRACT", 1.0, s_i))
    termD = vec_math_op(group, "SCALE", Cip1_d, s_i)

    # Bilinear correction (Eq. 1 matrix term)
    Ci0 = bezier_eval(group, C0, C1, C2, C3, 0.0)
    Ci1 = bezier_eval(group, C0, C1, C2, C3, 1.0)
    Cim10 = bezier_eval(group, Cm10, Cm11, Cm12, Cm13, 0.0)
    Cip11 = bezier_eval(group, Cp10, Cp11, Cp12, Cp13, 1.0)

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
