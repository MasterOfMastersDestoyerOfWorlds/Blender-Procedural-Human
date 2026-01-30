import bpy
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import (
    get_or_rebuild_node_group, math_op, vec_math_op, get_attr, link_or_set, create_node,
    int_op, compare_int_less, compare_float_less, bool_and, int_to_float, switch_node,
    switch_int, switch_vec, switch_float, clamp01, smoother_step, tan_half_angle,
    sample_from_orig_corner, mapped_index, corner_for_idx, edge_for_idx,
    edge_control_points_node, bezier_eval_node, bezier_deriv_node,
    sample_face_corner_pos, domain_edge_distance_node
)
from procedural_human.geo_node_groups.cache_bezier import *

@geo_node_group
def create_charrot_gregory_group():
    group_name = "CoonNGonPatchGenerator"     
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Subdivisions", in_out="INPUT", socket_type="NodeSocketInt").default_value = 4
    group.interface.new_socket(name="Merge By Distance", in_out="INPUT", socket_type="NodeSocketBool").default_value = True
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
  
    nodes = group.nodes    
    links = group.links  
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    raw_geo = group_input.outputs["Geometry"]  
    orig_geo = precompute_edge_data_node(group, raw_geo)

    corner_idx = nodes.new("GeometryNodeInputIndex").outputs[0]
    face_of_corner = nodes.new("GeometryNodeFaceOfCorner")
    links.new(corner_idx, face_of_corner.inputs["Corner Index"])
    face_idx = face_of_corner.outputs["Face Index"]
    face_idx_node = nodes.new("GeometryNodeInputIndex")
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
        "Geometry": orig_geo, "Domain": "EDGE", "Data Type": "INT",
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
        "Value": 1, "Group ID": face_idx, "Domain": "CORNER"
    })
    local_i = math_op(group, "SUBTRACT", accum_idx.outputs["Trailing"], 1)
    
    N_field = get_attr(group, "poly_N", "INT")
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
    
    store_uv = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Name": "domain_uv_interp", "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Value": uv_vec.outputs[0]
    })
    links.new(prepared_geo, store_uv.inputs[0])
    geo_with_uv = store_uv.outputs[0]
    split = create_node(group,"GeometryNodeSplitEdges", {"Mesh": geo_with_uv})
    subdiv = create_node(group,"GeometryNodeSubdivideMesh", {
        "Mesh": split.outputs[0],
        "Level": group_input.outputs["Subdivisions"]
    })
    subdivided_geo = subdiv.outputs[0]
    domain_uv_node = nodes.new("GeometryNodeInputNamedAttribute")
    domain_uv_node.data_type = "FLOAT_VECTOR"
    domain_uv_node.inputs["Name"].default_value = "domain_uv_interp"
    sep_uv = nodes.new("ShaderNodeSeparateXYZ")
    links.new(domain_uv_node.outputs[0], sep_uv.inputs[0])
    domain_p_x = sep_uv.outputs["X"]
    domain_p_y = sep_uv.outputs["Y"]

    stat_N = create_node(group,"GeometryNodeAttributeStatistic", {
        "Geometry": subdivided_geo, "Domain": "POINT", "Attribute": N_field
    })
    max_N = stat_N.outputs["Max"]
    repB_in = nodes.new("GeometryNodeRepeatInput")
    repB_out = nodes.new("GeometryNodeRepeatOutput")
    repB_in.pair_with_output(repB_out)
    repB_out.repeat_items.new("GEOMETRY", "Geometry")
    repB_out.repeat_items.new("FLOAT", "SumW")
    repB_out.repeat_items.new("INT", "IterIdx")
    repB_out.repeat_items.new("FLOAT", "PrevDist") 

    links.new(subdivided_geo, repB_in.inputs["Geometry"]) 
    links.new(max_N, repB_in.inputs["Iterations"])
    repB_in.inputs["SumW"].default_value = 0.0
    repB_in.inputs["IterIdx"].default_value = 0
    init_D0 = domain_edge_distance_node(group, 0, N_field, domain_p_x, domain_p_y)
    links.new(init_D0, repB_in.inputs["PrevDist"])

    B_geo = repB_in.outputs["Geometry"]
    B_sumw = repB_in.outputs["SumW"]
    B_i = repB_in.outputs["IterIdx"]
    B_prev_D = repB_in.outputs["PrevDist"]
    
    B_valid = compare_int_less(group, B_i, N_field)
    B_ip1 = int_op(group, "MODULO", int_op(group, "ADD", B_i, 1), N_field)
    
    D0 = B_prev_D
    D1 = domain_edge_distance_node(group, B_ip1, N_field, domain_p_x, domain_p_y)
    D0_safe = math_op(group, "MAXIMUM", D0, 1e-8)
    D1_safe = math_op(group, "MAXIMUM", D1, 1e-8)
    denom = math_op(group, "MULTIPLY", D0_safe, D1_safe)
    w_i = math_op(group, "DIVIDE", 1.0, denom)
    
    sum_new = math_op(group, "ADD", B_sumw, w_i)
    B_sum_final = switch_float(group, B_valid, B_sumw, sum_new)

    links.new(B_geo, repB_out.inputs["Geometry"])
    links.new(B_sum_final, repB_out.inputs["SumW"])
    links.new(int_op(group, "ADD", B_i, 1), repB_out.inputs["IterIdx"])
    links.new(D1, repB_out.inputs["PrevDist"]) # Pass D1 as next D0
    
    sumW = repB_out.outputs["SumW"]
    orig_loop_start_field = get_attr(group, "orig_loop_start", "INT")
    repC_in = nodes.new("GeometryNodeRepeatInput")
    repC_out = nodes.new("GeometryNodeRepeatOutput")
    repC_in.pair_with_output(repC_out)
    repC_out.repeat_items.new("GEOMETRY", "Geometry")
    repC_out.repeat_items.new("VECTOR", "SumS")
    repC_out.repeat_items.new("FLOAT", "SumB")
    repC_out.repeat_items.new("INT", "IterIdx")
    repC_out.repeat_items.new("FLOAT", "Dist_i")

    links.new(repB_out.outputs["Geometry"], repC_in.inputs["Geometry"])
    links.new(max_N, repC_in.inputs["Iterations"])
    repC_in.inputs["SumS"].default_value = (0, 0, 0)
    repC_in.inputs["SumB"].default_value = 0.0
    repC_in.inputs["IterIdx"].default_value = 0
    init_C_D0 = domain_edge_distance_node(group, 0, N_field, domain_p_x, domain_p_y)
    links.new(init_C_D0, repC_in.inputs["Dist_i"])

    C_geo = repC_in.outputs["Geometry"]
    C_sumS = repC_in.outputs["SumS"]
    C_sumB = repC_in.outputs["SumB"]
    C_i = repC_in.outputs["IterIdx"]
    C_Di = repC_in.outputs["Dist_i"]
    
    C_valid = compare_int_less(group, C_i, N_field)
    im1 = int_op(group, "MODULO", int_op(group, "ADD", int_op(group, "SUBTRACT", C_i, 1), N_field), N_field)
    ip1 = int_op(group, "MODULO", int_op(group, "ADD", C_i, 1), N_field)
    im2 = int_op(group, "MODULO", int_op(group, "ADD", int_op(group, "SUBTRACT", C_i, 2), N_field), N_field)
    ip2 = int_op(group, "MODULO", int_op(group, "ADD", C_i, 2), N_field)
    
    Di = math_op(group, "MAXIMUM", C_Di, 1.0e-8)
    D_ip1_raw = domain_edge_distance_node(group, ip1, N_field, domain_p_x, domain_p_y)
    Dip1 = math_op(group, "MAXIMUM", D_ip1_raw, 1.0e-8)
    
    wcur = math_op(group, "DIVIDE", 1.0, math_op(group, "MULTIPLY", Di, Dip1))
    lam_i = math_op(group, "DIVIDE", wcur, sumW)
    
    Dim1 = math_op(group, "MAXIMUM", domain_edge_distance_node(group, im1, N_field, domain_p_x, domain_p_y), 1.0e-8)
    wprev = math_op(group, "DIVIDE", 1.0, math_op(group, "MULTIPLY", Dim1, Di))
    lam_im1 = math_op(group, "DIVIDE", wprev, sumW)

    denom = math_op(group, "MAXIMUM", math_op(group, "ADD", lam_im1, lam_i), 1.0e-8)
    s_i_raw = clamp01(group, math_op(group, "DIVIDE", lam_i, denom))
    d_i_raw = clamp01(group, math_op(group, "SUBTRACT", 1.0, math_op(group, "ADD", lam_im1, lam_i)))
    s_i = smoother_step(group, s_i_raw)
    d_i = smoother_step(group, d_i_raw)
    
    def get_edge_data(idx):
        e, f = edge_for_idx(group, idx, orig_loop_start_field, prepared_geo)
        return sample_cached_bezier_node(group, e, f, orig_geo)

    C0, C1, C2, C3 = get_edge_data(C_i)              # C_i
    Cm10, Cm11, Cm12, Cm13 = get_edge_data(im1)      # C_{i-1}
    Cp10, Cp11, Cp12, Cp13 = get_edge_data(ip1)      # C_{i+1}

    Ci_si = bezier_eval_node(group, C0, C1, C2, C3, s_i)
    Cim1_1md = bezier_eval_node(group, Cm10, Cm11, Cm12, Cm13, math_op(group, "SUBTRACT", 1.0, d_i))
    Cip1_d = bezier_eval_node(group, Cp10, Cp11, Cp12, Cp13, d_i)
    Cp20, Cp21, Cp22, Cp23 = get_edge_data(ip2)   # C_{i+2}
    Cm20, Cm21, Cm22, Cm23 = get_edge_data(im2)   # C_{i-2}
    tan_ip2 = vec_math_op(group, "SUBTRACT", Cp21, Cp20)
    tan_im2 = vec_math_op(group, "SUBTRACT", Cm23, Cm22)
    P0_opp = Cp13 # C_{i+1}(1) is P3 of C_{i+1}
    P3_opp = Cm10 # C_{i-1}(0) is P0 of C_{i-1}
    
    P1_opp = vec_math_op(group, "ADD", P0_opp, tan_ip2)
    P2_opp = vec_math_op(group, "SUBTRACT", P3_opp, tan_im2)

    Copp_1ms = bezier_eval_node(group, P0_opp, P1_opp, P2_opp, P3_opp, math_op(group, "SUBTRACT", 1.0, s_i))
    termA = vec_math_op(group, "SCALE", Ci_si, math_op(group, "SUBTRACT", 1.0, d_i))
    termB = vec_math_op(group, "SCALE", Copp_1ms, d_i)
    termC = vec_math_op(group, "SCALE", Cim1_1md, math_op(group, "SUBTRACT", 1.0, s_i))
    termD = vec_math_op(group, "SCALE", Cip1_d, s_i)
    Ci0 = C0
    Ci1 = C3
    Cim10 = Cm10
    Cip11 = Cp13

    l0 = vec_math_op(group, "ADD", vec_math_op(group, "SCALE", Ci0, math_op(group, "SUBTRACT", 1.0, d_i)),
                     vec_math_op(group, "SCALE", Cim10, d_i))
    l1 = vec_math_op(group, "ADD", vec_math_op(group, "SCALE", Ci1, math_op(group, "SUBTRACT", 1.0, d_i)),
                     vec_math_op(group, "SCALE", Cip11, d_i))
    bilinear = vec_math_op(group, "ADD", vec_math_op(group, "SCALE", l0, math_op(group, "SUBTRACT", 1.0, s_i)),
                           vec_math_op(group, "SCALE", l1, s_i))

    R_i = vec_math_op(group, "SUBTRACT",
                      vec_math_op(group, "ADD", vec_math_op(group, "ADD", termA, termB), vec_math_op(group, "ADD", termC, termD)),
                      bilinear)

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
    links.new(D_ip1_raw, repC_out.inputs["Dist_i"]) # Pass calculated D_{i+1} to next loop

    sumS = repC_out.outputs["SumS"]
    sumB = repC_out.outputs["SumB"]
    inv_sumB = math_op(group, "DIVIDE", 1.0, math_op(group, "MAXIMUM", sumB, 1.0e-8))
    final_pos_raw = vec_math_op(group, "SCALE", sumS, inv_sumB)
    
    set_pos = nodes.new("GeometryNodeSetPosition")
    links.new(repC_out.outputs["Geometry"], set_pos.inputs["Geometry"])
    links.new(final_pos_raw, set_pos.inputs["Position"])

    merge = create_node(group,"GeometryNodeMergeByDistance", {
        "Geometry": set_pos.outputs[0], "Distance": 0.0001
    })

    geom_after_merge = switch_node(group, "GEOMETRY",
                                   group_input.outputs["Merge By Distance"],
                                   set_pos.outputs[0],
                                   merge.outputs[0])
    
    set_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    links.new(geom_after_merge, set_smooth.inputs[0])
    set_smooth.inputs["Shade Smooth"].default_value = True
    
    links.new(set_smooth.outputs[0], group_output.inputs[0])
    
    auto_layout_nodes(group)
    return group