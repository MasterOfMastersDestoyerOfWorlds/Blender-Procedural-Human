import bpy
import math
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group

@geo_node_group
def create_charrot_gregory_group():
    """
    Creates a Geometry Node group that generates Charrot-Gregory patches 
    for arbitrary N-gons using Repeat Zones (Blender 4.0+).
    """
    group_name = "CharrotGregoryPatchGenerator"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    
    # --- Interface ---
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Subdivisions", in_out="INPUT", socket_type="NodeSocketInt").default_value = 4
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    
    # --- Robust Helpers ---
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
        """Creates a node, sets properties, and links inputs."""
        node = nodes.new(type_name)
        
        # Set Properties (Attribute Domain, Data Type, Math Operation, etc.)
        # We handle this first so sockets (like Attribute Type) update correctly
        if inputs:
            # Separate properties from socket inputs
            # Properties usually match snake_case attributes on the node
            for k, v in inputs.items():
                k_prop = k.lower().replace(" ", "_")
                if hasattr(node, k_prop):
                    try:
                        setattr(node, k_prop, v)
                    except Exception:
                        pass # Might be read-only or invalid
                elif hasattr(node, k): # Try direct name (e.g. 'operation')
                     try:
                        setattr(node, k, v)
                     except Exception:
                        pass

        # Link Inputs
        if inputs:
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
        # Operations that return scalar values use output index 1 ("Value")
        if op in ('DOT_PRODUCT', 'LENGTH', 'DISTANCE'):
            return n.outputs[1]  # "Value" output (scalar)
        return n.outputs[0]  # "Vector" output

    def get_attr(name, type='INT'):
        n = nodes.new("GeometryNodeInputNamedAttribute")
        n.data_type = type
        n.inputs["Name"].default_value = name
        return n.outputs[0]

    # --- 1. PRE-PROCESSING (Topology Capture) ---
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    
    corner_idx = nodes.new("GeometryNodeInputIndex").outputs[0] 
    edges_of_corner = nodes.new("GeometryNodeEdgesOfCorner")
    links.new(corner_idx, edges_of_corner.inputs["Corner Index"])
    
    store_orig_edge = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "orig_edge_idx", 
        "Domain": "CORNER", 
        "Data Type": "INT",
        "Value": edges_of_corner.outputs["Next Edge Index"]
    })
    links.new(group_input.outputs["Geometry"], store_orig_edge.inputs[0])
    
    vertex_of_corner = nodes.new("GeometryNodeVertexOfCorner")
    links.new(corner_idx, vertex_of_corner.inputs["Corner Index"])
    
    sample_edge_v1 = create_node("GeometryNodeSampleIndex", {
        "Geometry": store_orig_edge.outputs[0], 
        "Domain": "EDGE", 
        "Data Type": "INT",
        "Index": edges_of_corner.outputs["Next Edge Index"]
    })
    edge_verts = nodes.new("GeometryNodeInputMeshEdgeVertices")
    links.new(edge_verts.outputs["Vertex Index 1"], sample_edge_v1.inputs["Value"])
    
    is_fwd_cmp = create_node("FunctionNodeCompare", {"Data Type": "INT", "Operation": "EQUAL"})
    links.new(vertex_of_corner.outputs["Vertex Index"], is_fwd_cmp.inputs["A"])
    links.new(sample_edge_v1.outputs[0], is_fwd_cmp.inputs["B"])
    
    store_is_fwd = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "orig_edge_fwd", "Domain": "CORNER", "Data Type": "BOOLEAN",
        "Value": is_fwd_cmp.outputs["Result"]
    })
    links.new(store_orig_edge.outputs[0], store_is_fwd.inputs[0])

    face_of_corner = nodes.new("GeometryNodeFaceOfCorner")
    links.new(corner_idx, face_of_corner.inputs["Corner Index"])
    
    accum_N = create_node("GeometryNodeAccumulateField", {
        "Value": 1, "Group ID": face_of_corner.outputs["Face Index"], "Domain": "CORNER" 
    })
    
    store_N = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "poly_N", "Domain": "FACE", "Data Type": "INT",
        "Value": accum_N.outputs["Total"]
    })
    links.new(store_is_fwd.outputs[0], store_N.inputs[0])
    
    corners_of_face = nodes.new("GeometryNodeCornersOfFace")
    links.new(face_of_corner.outputs["Face Index"], corners_of_face.inputs["Face Index"])
    corners_of_face.inputs["Sort Index"].default_value = 0
    
    sort_idx = math_op('SUBTRACT', corner_idx, corners_of_face.outputs["Corner Index"])
    store_sort = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "corner_sort_idx", "Domain": "CORNER", "Data Type": "INT",
        "Value": sort_idx
    })
    links.new(store_N.outputs[0], store_sort.inputs[0])

    # Store Base Corner Index (for looking up corners later)
    c_lookup_0 = nodes.new("GeometryNodeCornersOfFace")
    links.new(face_of_corner.outputs["Face Index"], c_lookup_0.inputs["Face Index"])
    c_lookup_0.inputs["Sort Index"].default_value = 0
    
    store_base_corner = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "base_corner_idx", "Domain": "FACE", "Data Type": "INT",
        "Value": c_lookup_0.outputs["Corner Index"]
    })
    links.new(store_sort.outputs[0], store_base_corner.inputs[0])

    # --- 1b. STORE FACE TANGENT (before split/subdivide) ---
    # We need a consistent tangent direction per face for the domain mapping.
    # Compute tangent from the first edge of each face (corner 0 -> corner 1 direction).
    
    # Get first corner's vertex position
    vert_of_c0 = nodes.new("GeometryNodeVertexOfCorner")
    links.new(c_lookup_0.outputs["Corner Index"], vert_of_c0.inputs["Corner Index"])
    
    pos_for_tangent = nodes.new("GeometryNodeInputPosition").outputs[0]
    sample_pos_c0 = create_node("GeometryNodeSampleIndex", {
        "Geometry": store_base_corner.outputs[0], "Domain": "POINT", "Data Type": "FLOAT_VECTOR",
        "Index": vert_of_c0.outputs["Vertex Index"]
    })
    links.new(pos_for_tangent, sample_pos_c0.inputs["Value"])
    
    # Get second corner (sort index 1)
    c_lookup_1 = nodes.new("GeometryNodeCornersOfFace")
    links.new(face_of_corner.outputs["Face Index"], c_lookup_1.inputs["Face Index"])
    c_lookup_1.inputs["Sort Index"].default_value = 1
    
    vert_of_c1 = nodes.new("GeometryNodeVertexOfCorner")
    links.new(c_lookup_1.outputs["Corner Index"], vert_of_c1.inputs["Corner Index"])
    
    sample_pos_c1 = create_node("GeometryNodeSampleIndex", {
        "Geometry": store_base_corner.outputs[0], "Domain": "POINT", "Data Type": "FLOAT_VECTOR",
        "Index": vert_of_c1.outputs["Vertex Index"]
    })
    links.new(pos_for_tangent, sample_pos_c1.inputs["Value"])
    
    # Tangent = normalize(pos_c1 - pos_c0) - direction along first edge
    edge1_vec = vec_math_op('SUBTRACT', sample_pos_c1.outputs[0], sample_pos_c0.outputs[0])
    face_tangent = vec_math_op('NORMALIZE', edge1_vec)
    
    # Store face tangent as a FACE attribute (will be inherited by subdivided points)
    store_tangent = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "face_tangent", "Domain": "FACE", "Data Type": "FLOAT_VECTOR",
        "Value": face_tangent
    })
    links.new(store_base_corner.outputs[0], store_tangent.inputs[0])

    # --- 1c. STORE FACE NORMAL (computed from edge cross product, not vertex normals) ---
    # GeometryNodeInputNormal gives smooth vertex normals, which are incorrect for our needs.
    # We compute the true face normal from cross(edge1, edge2) where edge1 and edge2 are
    # two edges of the face emanating from corner 0.
    
    # Get third corner (sort index 2) to form second edge
    c_lookup_2 = nodes.new("GeometryNodeCornersOfFace")
    links.new(face_of_corner.outputs["Face Index"], c_lookup_2.inputs["Face Index"])
    c_lookup_2.inputs["Sort Index"].default_value = 2
    
    vert_of_c2 = nodes.new("GeometryNodeVertexOfCorner")
    links.new(c_lookup_2.outputs["Corner Index"], vert_of_c2.inputs["Corner Index"])
    
    sample_pos_c2 = create_node("GeometryNodeSampleIndex", {
        "Geometry": store_tangent.outputs[0], "Domain": "POINT", "Data Type": "FLOAT_VECTOR",
        "Index": vert_of_c2.outputs["Vertex Index"]
    })
    links.new(pos_for_tangent, sample_pos_c2.inputs["Value"])
    
    # edge2 = c2 - c0 (second edge from corner 0)
    edge2_vec = vec_math_op('SUBTRACT', sample_pos_c2.outputs[0], sample_pos_c0.outputs[0])
    
    # Face normal = normalize(cross(edge1, edge2))
    # This gives a consistent face normal regardless of smooth shading
    face_normal_cross = vec_math_op('CROSS_PRODUCT', edge1_vec, edge2_vec)
    face_normal_computed = vec_math_op('NORMALIZE', face_normal_cross)
    
    # Store face normal as a FACE attribute
    store_normal = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "face_normal", "Domain": "FACE", "Data Type": "FLOAT_VECTOR",
        "Value": face_normal_computed
    })
    links.new(store_tangent.outputs[0], store_normal.inputs[0])

    # --- 1d. STORE ORIGINAL FACE CENTER AND MAX RADIUS (before split/subdivide) ---
    # CRITICAL: After subdivision, each original face becomes many small sub-faces.
    # AttributeStatistic on subdivided geometry gives per-sub-face values, which is WRONG.
    # We need the ORIGINAL face center and max radius for the domain mapping to work.
    
    pos_for_center = nodes.new("GeometryNodeInputPosition").outputs[0]
    
    # Compute original face center (mean of face vertices)
    orig_face_stat = create_node("GeometryNodeAttributeStatistic", {
        "Geometry": store_normal.outputs[0], "Domain": "FACE", "Attribute": pos_for_center
    })
    orig_face_center = orig_face_stat.outputs["Mean"]
    
    store_face_center = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "orig_face_center", "Domain": "FACE", "Data Type": "FLOAT_VECTOR",
        "Value": orig_face_center
    })
    links.new(store_normal.outputs[0], store_face_center.inputs[0])
    
    # Compute distance from each vertex to face center, then get max per face
    rel_to_center = vec_math_op('SUBTRACT', pos_for_center, orig_face_center)
    dist_to_center = vec_math_op('LENGTH', rel_to_center)
    
    orig_dist_stat = create_node("GeometryNodeAttributeStatistic", {
        "Geometry": store_face_center.outputs[0], "Domain": "FACE", "Attribute": dist_to_center
    })
    orig_max_dist = orig_dist_stat.outputs["Max"]
    
    store_max_dist = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "orig_max_dist", "Domain": "FACE", "Data Type": "FLOAT",
        "Value": orig_max_dist
    })
    links.new(store_face_center.outputs[0], store_max_dist.inputs[0])

    # --- 2. SPLIT & SUBDIVIDE ---
    split = create_node("GeometryNodeSplitEdges", {"Mesh": store_max_dist.outputs[0]})
    split_geo = split.outputs[0] # Keep reference to split (un-subdivided) mesh
    
    subdiv = create_node("GeometryNodeSubdivideMesh", {
        "Mesh": split_geo, 
        "Level": group_input.outputs["Subdivisions"]
    })
    subdivided_geo = subdiv.outputs[0]
    
    # --- 3. DOMAIN MAPPING (Face-Local Coordinates) ---
    # This section maps each point on the subdivided mesh to a 2D parametric domain
    # using the face's local coordinate system (tangent, bitangent from normal).
    # This correctly handles faces of ANY orientation, not just XY-aligned faces.
    
    pos_input = nodes.new("GeometryNodeInputPosition").outputs[0]
    
    # Get face center (mean position of face vertices)
    face_stat = create_node("GeometryNodeAttributeStatistic", {
        "Geometry": subdivided_geo, "Domain": "FACE", "Attribute": pos_input
    })
    face_center = face_stat.outputs["Mean"]
    
    # Retrieve stored face attributes (computed before subdivision from actual face geometry)
    # These are correct for any face orientation, unlike GeometryNodeInputNormal which
    # returns smooth vertex normals that can point in wrong directions.
    tangent = get_attr("face_tangent", "FLOAT_VECTOR")
    face_normal = get_attr("face_normal", "FLOAT_VECTOR")
    
    # Bitangent = normalize(normal x tangent)
    # This gives us the second axis of our local 2D coordinate system
    bitangent = vec_math_op('NORMALIZE', vec_math_op('CROSS_PRODUCT', face_normal, tangent))
    
    # Re-orthogonalize tangent to ensure it's perpendicular to normal
    # tangent_ortho = normalize(bitangent x normal)
    tangent_ortho = vec_math_op('NORMALIZE', vec_math_op('CROSS_PRODUCT', bitangent, face_normal))
    
    # Vector from face center to current point
    rel_vec = vec_math_op('SUBTRACT', pos_input, face_center)
    
    # Project to local 2D coordinates using dot products
    local_x = vec_math_op('DOT_PRODUCT', rel_vec, tangent_ortho)
    local_y = vec_math_op('DOT_PRODUCT', rel_vec, bitangent)
    
    # Get N (number of sides) early - needed for angle offset
    N_field = get_attr("poly_N", "INT")
    
    # Compute angle in local face space
    angle_raw = math_op('ARCTAN2', local_y, local_x)
    
    # CRITICAL FIX: Add pi/N offset to align face corners with domain polygon vertices.
    # The domain polygon has vertex 0 at angle 0 (position (1,0)).
    # But our local X-axis points along edge 0 (from corner 0 to corner 1), not toward corner 0.
    # In a regular N-gon, the angle from center to vertex 0 differs from the edge 0 direction
    # by approximately pi/N. Adding this offset ensures corner 0 maps to domain vertex 0.
    angle_offset = math_op('DIVIDE', 3.14159265, N_field)  # pi/N
    angle = math_op('ADD', angle_raw, angle_offset)
    
    # Compute normalized distance (radial distance in the 2D domain)
    len_vec = vec_math_op('LENGTH', rel_vec)
    dist_stat = create_node("GeometryNodeAttributeStatistic", {
        "Geometry": subdivided_geo, "Domain": "FACE", "Attribute": len_vec
    })
    norm_dist = math_op('DIVIDE', len_vec, math_op('MAXIMUM', dist_stat.outputs["Max"], 0.001))
    
    # Create domain point in 2D polar coordinates (for the Charrot-Gregory algorithm)
    cos_a = math_op('COSINE', angle)
    sin_a = math_op('SINE', angle)
    
    domain_p = nodes.new("ShaderNodeCombineXYZ")
    links.new(math_op('MULTIPLY', cos_a, norm_dist), domain_p.inputs["X"])
    links.new(math_op('MULTIPLY', sin_a, norm_dist), domain_p.inputs["Y"])
    domain_p_vec = domain_p.outputs[0]
    
    # --- 4. REPEAT ZONE 1: LogSum ---
    stat_N = create_node("GeometryNodeAttributeStatistic", {
        "Geometry": subdivided_geo, "Domain": "POINT", "Attribute": N_field
    })
    max_N = stat_N.outputs["Max"]
    
    # Create and Pair Repeat Nodes
    rep_1_in = nodes.new("GeometryNodeRepeatInput")
    rep_1_out = nodes.new("GeometryNodeRepeatOutput")
    rep_1_in.pair_with_output(rep_1_out)
    
    # Define Repeat Items (on Output Node)
    rep_1_out.repeat_items.new("GEOMETRY", "Geometry")
    rep_1_out.repeat_items.new("FLOAT", "LogSum")
    rep_1_out.repeat_items.new("INT", "IterIdx")
    
    # Link External Inputs
    links.new(subdivided_geo, rep_1_in.inputs["Geometry"])
    links.new(max_N, rep_1_in.inputs["Iterations"])
    rep_1_in.inputs["LogSum"].default_value = 0.0
    rep_1_in.inputs["IterIdx"].default_value = 0
    
    # Internal Logic 1
    loop_geo = rep_1_in.outputs["Geometry"]
    loop_log = rep_1_in.outputs["LogSum"]
    loop_iter = rep_1_in.outputs["IterIdx"]
    
    valid_iter = math_op('LESS_THAN', loop_iter, N_field)
    
    def calc_lambda(idx_node):
        """
        Compute perpendicular distance from domain point to the INFINITE LINE 
        containing edge idx_node of the domain polygon.
        
        According to Charrot-Gregory algorithm (Section 2.3), lambda_i is the 
        orthogonal distance to the line containing edge i, NOT the clamped 
        distance to the line segment.
        
        Formula: distance = |cross(p - v0, edge_dir)| / |edge|
        In 2D: cross gives scalar = (px-v0x)*(v1y-v0y) - (py-v0y)*(v1x-v0x)
        """
        # Domain polygon vertex i at angle 2*pi*i/N
        theta = math_op('MULTIPLY', 6.283185, math_op('DIVIDE', idx_node, N_field))
        v_curr = nodes.new("ShaderNodeCombineXYZ")
        links.new(math_op('COSINE', theta), v_curr.inputs["X"])
        links.new(math_op('SINE', theta), v_curr.inputs["Y"])
        
        # Domain polygon vertex i+1
        idx_next = math_op('ADD', idx_node, 1)
        theta_next = math_op('MULTIPLY', 6.283185, math_op('DIVIDE', idx_next, N_field))
        v_next = nodes.new("ShaderNodeCombineXYZ")
        links.new(math_op('COSINE', theta_next), v_next.inputs["X"])
        links.new(math_op('SINE', theta_next), v_next.inputs["Y"])
        
        # Edge vector and length
        edge_vec = vec_math_op('SUBTRACT', v_next.outputs[0], v_curr.outputs[0])
        edge_len = vec_math_op('LENGTH', edge_vec)
        
        # Vector from edge start to point
        p_sub_v = vec_math_op('SUBTRACT', domain_p_vec, v_curr.outputs[0])
        
        # Separate X and Y components for 2D cross product
        sep_edge = nodes.new("ShaderNodeSeparateXYZ")
        links.new(edge_vec, sep_edge.inputs[0])
        edge_x = sep_edge.outputs["X"]
        edge_y = sep_edge.outputs["Y"]
        
        sep_pv = nodes.new("ShaderNodeSeparateXYZ")
        links.new(p_sub_v, sep_pv.inputs[0])
        pv_x = sep_pv.outputs["X"]
        pv_y = sep_pv.outputs["Y"]
        
        # 2D cross product: (p-v0).x * edge.y - (p-v0).y * edge.x
        cross_2d = math_op('SUBTRACT', 
            math_op('MULTIPLY', pv_x, edge_y),
            math_op('MULTIPLY', pv_y, edge_x)
        )
        
        # Perpendicular distance = |cross| / |edge|
        perp_dist = math_op('DIVIDE', math_op('ABSOLUTE', cross_2d), edge_len)
        
        # Clamp to small positive value to avoid division by zero in weights
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

    # --- 5. REPEAT ZONE 2: Positions ---
    total_log_sum = rep_1_out.outputs["LogSum"]
    
    rep_2_in = nodes.new("GeometryNodeRepeatInput")
    rep_2_out = nodes.new("GeometryNodeRepeatOutput")
    rep_2_in.pair_with_output(rep_2_out)
    
    # Define Items
    rep_2_out.repeat_items.new("GEOMETRY", "Geometry")
    rep_2_out.repeat_items.new("VECTOR", "WeightedPos")
    rep_2_out.repeat_items.new("FLOAT", "TotalWeight")
    rep_2_out.repeat_items.new("INT", "IterIdx")
    
    # Inputs
    links.new(rep_1_out.outputs["Geometry"], rep_2_in.inputs["Geometry"])
    links.new(max_N, rep_2_in.inputs["Iterations"])
    rep_2_in.inputs["WeightedPos"].default_value = (0,0,0)
    rep_2_in.inputs["TotalWeight"].default_value = 0.0
    rep_2_in.inputs["IterIdx"].default_value = 0
    
    # Internal Logic 2
    l2_geo = rep_2_in.outputs["Geometry"]
    l2_wpos = rep_2_in.outputs["WeightedPos"]
    l2_wgt = rep_2_in.outputs["TotalWeight"]
    l2_iter = rep_2_in.outputs["IterIdx"]
    
    valid_2 = math_op('LESS_THAN', l2_iter, N_field)
    
    lam_curr = calc_lambda(l2_iter)
    idx_prev = math_op('MODULO', math_op('ADD', math_op('ADD', l2_iter, N_field), -1), N_field)
    lam_prev = calc_lambda(idx_prev)
    
    log_sum_local = math_op('ADD', math_op('LOGARITHM', lam_curr), math_op('LOGARITHM', lam_prev))
    weight_i = math_op('EXPONENT', math_op('SUBTRACT', total_log_sum, log_sum_local))
    s_val = math_op('DIVIDE', lam_curr, math_op('ADD', lam_curr, lam_prev))
    
    # Sample Corner Attributes from Split Geo (RefGeo)
    # RefGeo is 'split_geo', which is available in the group (same tree)
    base_corner_field = get_attr("base_corner_idx", "INT")
    target_corner_idx = math_op('ADD', base_corner_field, l2_iter)
    
    def sample_corner_attr(name, type, idx_val):
        s = create_node("GeometryNodeSampleIndex", {
            "Geometry": split_geo, "Domain": "CORNER", "Data Type": type,
            "Index": idx_val
        })
        attr = nodes.new("GeometryNodeInputNamedAttribute")
        attr.data_type = type
        attr.inputs["Name"].default_value = name
        links.new(attr.outputs[0], s.inputs["Value"])
        return s.outputs[0]
        
    edge_idx = sample_corner_attr("orig_edge_idx", "INT", target_corner_idx)
    is_fwd = sample_corner_attr("orig_edge_fwd", "BOOLEAN", target_corner_idx)
    
    target_corner_prev = math_op('ADD', base_corner_field, idx_prev)
    edge_idx_prev = sample_corner_attr("orig_edge_idx", "INT", target_corner_prev)
    is_fwd_prev = sample_corner_attr("orig_edge_fwd", "BOOLEAN", target_corner_prev)

    # Bezier Eval
    orig_geo_input = group_input.outputs["Geometry"]
    
    def eval_bezier(edge_id, fwd, t_val):
        # Sample from Original Geo
        def get_pt(idx, v_sock):
            s_edge = create_node("GeometryNodeSampleIndex", {
                "Geometry": orig_geo_input, "Domain": "EDGE", "Data Type": "INT", "Index": idx
            })
            ev = nodes.new("GeometryNodeInputMeshEdgeVertices")
            links.new(ev.outputs[v_sock], s_edge.inputs["Value"])
            s_pos = create_node("GeometryNodeSampleIndex", {
                "Geometry": orig_geo_input, "Domain": "POINT", "Data Type": "FLOAT_VECTOR", "Index": s_edge.outputs[0]
            })
            links.new(nodes.new("GeometryNodeInputPosition").outputs[0], s_pos.inputs["Value"])
            return s_pos.outputs[0]

        p_start = get_pt(edge_id, 0)
        p_end = get_pt(edge_id, 1)
        
        def get_h(prefix):
            x = create_node("GeometryNodeSampleIndex", {
                "Geometry": orig_geo_input, "Domain": "EDGE", "Data Type": "FLOAT", "Index": edge_id
            })
            links.new(get_attr(f"{prefix}_x", 'FLOAT'), x.inputs["Value"])
            y = create_node("GeometryNodeSampleIndex", {
                "Geometry": orig_geo_input, "Domain": "EDGE", "Data Type": "FLOAT", "Index": edge_id
            })
            links.new(get_attr(f"{prefix}_y", 'FLOAT'), y.inputs["Value"])
            z = create_node("GeometryNodeSampleIndex", {
                "Geometry": orig_geo_input, "Domain": "EDGE", "Data Type": "FLOAT", "Index": edge_id
            })
            links.new(get_attr(f"{prefix}_z", 'FLOAT'), z.inputs["Value"])
            
            c = nodes.new("ShaderNodeCombineXYZ")
            links.new(x.outputs[0], c.inputs[0])
            links.new(y.outputs[0], c.inputs[1])
            links.new(z.outputs[0], c.inputs[2])
            return c.outputs[0]
            
        h_start = get_h("handle_start")
        h_end = get_h("handle_end")
        
        mix_p0 = nodes.new("ShaderNodeMix")
        mix_p0.data_type = 'VECTOR'
        links.new(fwd, mix_p0.inputs["Factor"])
        links.new(p_end, mix_p0.inputs["A"])
        links.new(p_start, mix_p0.inputs["B"])
        P0 = mix_p0.outputs["Result"]
        
        mix_p3 = nodes.new("ShaderNodeMix")
        mix_p3.data_type = 'VECTOR'
        links.new(fwd, mix_p3.inputs["Factor"])
        links.new(p_start, mix_p3.inputs["A"])
        links.new(p_end, mix_p3.inputs["B"])
        P3 = mix_p3.outputs["Result"]
        
        p1_fwd = vec_math_op('ADD', p_start, h_start)
        p1_bwd = vec_math_op('ADD', p_end, h_end)
        mix_p1 = nodes.new("ShaderNodeMix")
        mix_p1.data_type = 'VECTOR'
        links.new(fwd, mix_p1.inputs["Factor"])
        links.new(p1_bwd, mix_p1.inputs["A"])
        links.new(p1_fwd, mix_p1.inputs["B"])
        P1 = mix_p1.outputs["Result"]

        p2_fwd = vec_math_op('ADD', p_end, h_end)
        p2_bwd = vec_math_op('ADD', p_start, h_start)
        mix_p2 = nodes.new("ShaderNodeMix")
        mix_p2.data_type = 'VECTOR'
        links.new(fwd, mix_p2.inputs["Factor"])
        links.new(p2_bwd, mix_p2.inputs["A"])
        links.new(p2_fwd, mix_p2.inputs["B"])
        P2 = mix_p2.outputs["Result"]
        
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

    c_curr_pos = eval_bezier(edge_idx, is_fwd, math_op('SUBTRACT', 1.0, s_val))
    c_prev_pos = eval_bezier(edge_idx_prev, is_fwd_prev, s_val)
    p_corner = eval_bezier(edge_idx, is_fwd, 0.0)
    
    r_i = vec_math_op('SUBTRACT', vec_math_op('ADD', c_curr_pos, c_prev_pos), p_corner)
    
    w_pos_accum = vec_math_op('SCALE', r_i, weight_i)
    new_wpos = vec_math_op('ADD', l2_wpos, w_pos_accum)
    new_wgt = math_op('ADD', l2_wgt, weight_i)
    
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

    # --- FINAL OUTPUT ---
    final_pos = vec_math_op('DIVIDE', rep_2_out.outputs["WeightedPos"], rep_2_out.outputs["TotalWeight"])
    
    set_pos = nodes.new("GeometryNodeSetPosition")
    links.new(rep_2_out.outputs["Geometry"], set_pos.inputs["Geometry"])
    links.new(final_pos, set_pos.inputs["Position"])
    
    merge = create_node("GeometryNodeMergeByDistance", {
        "Geometry": set_pos.outputs[0], "Distance": 0.0001
    })
    
    links.new(merge.outputs[0], group_output.inputs[0])
    
    auto_layout_nodes(group)
    return group