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
    group_name = "CoonNGonPatchGenerator"     
    if group_name in bpy.data.node_groups:
        bpy.data.node_groups.remove(bpy.data.node_groups[group_name])

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    
    # --- Interface ---
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Subdivisions", in_out="INPUT", socket_type="NodeSocketInt").default_value = 4
    # Default OFF: merging breaks per-face attribute consistency (orig_loop_start/poly_N)
    # and can create "star" connectivity when multiple face-islands collapse together.
    group.interface.new_socket(name="Merge By Distance", in_out="INPUT", socket_type="NodeSocketBool").default_value = False
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

    def int_to_float(a):
        """Convert integer to float."""
        n = nodes.new("ShaderNodeMath")
        n.operation = "ADD"
        link_or_set(n.inputs[0], a)
        n.inputs[1].default_value = 0.0
        return n.outputs["Value"]

    def compare_int_eq(a, b):
        """Compare two integers for equality."""
        c = nodes.new("FunctionNodeCompare")
        c.data_type = "INT"
        c.operation = "EQUAL"
        link_or_set(c.inputs["A"], a)
        link_or_set(c.inputs["B"], b)
        return c.outputs["Result"]

    def switch_node(dtype, sw, false_val, true_val):
        """Generic switch for INT, FLOAT, or VECTOR types."""
        n = nodes.new("GeometryNodeSwitch")
        n.input_type = dtype
        links.new(sw, n.inputs["Switch"])
        link_or_set(n.inputs["False"], false_val)
        link_or_set(n.inputs["True"], true_val)
        return n.outputs["Output"]

    def switch_int(sw, false_val, true_val):
        return switch_node("INT", sw, false_val, true_val)

    def switch_vec(sw, false_val, true_val):
        return switch_node("VECTOR", sw, false_val, true_val)

    def switch_float(sw, false_val, true_val):
        return switch_node("FLOAT", sw, false_val, true_val)

    def clamp01(x):
        return math_op("MINIMUM", 1.0, math_op("MAXIMUM", 0.0, x))

    def smoother_step(t):
        """Quintic smoothstep: t^3 * (6t^2 - 15t + 10) for C2 continuity.
        Matches coon_patch.py's blending function."""
        # s1 = 6*t - 15
        s1 = math_op("SUBTRACT", math_op("MULTIPLY", t, 6.0), 15.0)
        # s2 = t * s1 + 10 = 6t^2 - 15t + 10
        s2 = math_op("ADD", math_op("MULTIPLY", t, s1), 10.0)
        # result = t^3 * s2
        t3 = math_op("POWER", t, 3.0)
        return math_op("MULTIPLY", t3, s2)

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
    
    # --- 2. STORE CORNER POSITIONS FOR BARYCENTRIC COMPUTATION ---
    # FIX: Don't store domain_pos or UV on corners - they don't interpolate correctly for N-gons.
    # Instead, we'll compute domain_pos at runtime using generalized barycentric coordinates.
    # Store corner 3D positions so we can compute barycentric coords later.
    
    # Get the vertex position at this corner
    vert_of_corner = nodes.new("GeometryNodeVertexOfCorner")
    links.new(corner_idx, vert_of_corner.inputs["Corner Index"])
    
    sample_corner_pos = create_node("GeometryNodeSampleIndex", {
        "Geometry": orig_geo, "Domain": "POINT", "Data Type": "FLOAT_VECTOR",
        "Index": vert_of_corner.outputs["Vertex Index"]
    })
    pos_node = nodes.new("GeometryNodeInputPosition")
    links.new(pos_node.outputs[0], sample_corner_pos.inputs["Value"])
    corner_pos = sample_corner_pos.outputs[0]
    
    # Store corner position on CORNER domain
    store_corner_pos = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "corner_pos", "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Value": corner_pos
    })
    links.new(orig_geo, store_corner_pos.inputs[0])
    
    # Also store the sort_idx for each corner (needed for domain position calculation)
    sort_idx_float = int_to_float(sort_idx)
    store_sort_idx = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "corner_sort_idx", "Domain": "CORNER", "Data Type": "FLOAT",
        "Value": sort_idx_float
    })
    links.new(store_corner_pos.outputs[0], store_sort_idx.inputs[0])
    
    # --- 3. STORE FACE INDEX ON FACE DOMAIN ---
    # This propagates through split/subdivide so we can look up original corners
    face_idx_node = nodes.new("GeometryNodeInputIndex")  # In FACE context this gives face index
    
    store_face_idx = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "orig_face_idx", "Domain": "FACE", "Data Type": "INT",
        "Value": face_idx_node.outputs[0]
    })
    links.new(store_sort_idx.outputs[0], store_face_idx.inputs[0])

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
    # --- 4. STORE EDGE INFO ON CORNERS ---
    edges_of_corner = nodes.new("GeometryNodeEdgesOfCorner")
    links.new(corner_idx, edges_of_corner.inputs["Corner Index"])
    
    store_edge_idx = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "corner_edge_idx", "Domain": "CORNER", "Data Type": "INT",
        # Store the *incoming* edge at this corner.
        # This matches the paper's convention where side i is between vertices (i-1, i).
        "Value": edges_of_corner.outputs["Previous Edge Index"]
    })
    links.new(store_N.outputs[0], store_edge_idx.inputs[0])
    
    # Determine edge direction
    vertex_of_corner = nodes.new("GeometryNodeVertexOfCorner")
    links.new(corner_idx, vertex_of_corner.inputs["Corner Index"])
    
    edge_verts = nodes.new("GeometryNodeInputMeshEdgeVertices")

    # --- 4.1 DEBUG: verify corner_edge_idx is incident to corner vertex ---
    # Store the corner's vertex index
    store_corner_vert_idx = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "corner_vertex_idx", "Domain": "CORNER", "Data Type": "INT",
        "Value": vertex_of_corner.outputs["Vertex Index"]
    })
    links.new(store_edge_idx.outputs[0], store_corner_vert_idx.inputs[0])

    # Sample the two endpoint vertex indices of the stored edge
    sample_edge_v_idx1 = create_node("GeometryNodeSampleIndex", {
        "Geometry": store_corner_vert_idx.outputs[0],
        "Domain": "EDGE", "Data Type": "INT",
        "Index": edges_of_corner.outputs["Previous Edge Index"]
    })
    links.new(edge_verts.outputs["Vertex Index 1"], sample_edge_v_idx1.inputs["Value"])

    sample_edge_v_idx2 = create_node("GeometryNodeSampleIndex", {
        "Geometry": store_corner_vert_idx.outputs[0],
        "Domain": "EDGE", "Data Type": "INT",
        "Index": edges_of_corner.outputs["Previous Edge Index"]
    })
    links.new(edge_verts.outputs["Vertex Index 2"], sample_edge_v_idx2.inputs["Value"])

    store_corner_edge_v1 = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "corner_edge_v1", "Domain": "CORNER", "Data Type": "INT",
        "Value": sample_edge_v_idx1.outputs[0]
    })
    links.new(store_corner_vert_idx.outputs[0], store_corner_edge_v1.inputs[0])

    store_corner_edge_v2 = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "corner_edge_v2", "Domain": "CORNER", "Data Type": "INT",
        "Value": sample_edge_v_idx2.outputs[0]
    })
    links.new(store_corner_edge_v1.outputs[0], store_corner_edge_v2.inputs[0])
    
    # Determine direction for the stored incoming edge.
    # We want C_i(0)=vertex(i-1) and C_i(1)=vertex(i), i.e. the curve should end at this corner.
    sample_edge_v1 = create_node("GeometryNodeSampleIndex", {
        "Geometry": store_corner_edge_v2.outputs[0],
        "Domain": "EDGE", "Data Type": "INT",
        "Index": edges_of_corner.outputs["Previous Edge Index"]
    })
    # For an incoming edge, the corner vertex is the *end* of the edge in our convention,
    # so compare against "Vertex Index 2" to decide whether the stored (v1->v2) direction
    # already ends at this corner.
    links.new(edge_verts.outputs["Vertex Index 2"], sample_edge_v1.inputs["Value"])
    
    is_fwd_cmp = create_node("FunctionNodeCompare", {"Data Type": "INT", "Operation": "EQUAL"})
    links.new(vertex_of_corner.outputs["Vertex Index"], is_fwd_cmp.inputs["A"])
    links.new(sample_edge_v1.outputs[0], is_fwd_cmp.inputs["B"])
    
    store_is_fwd = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "edge_is_forward", "Domain": "CORNER", "Data Type": "BOOLEAN",
        "Value": is_fwd_cmp.outputs["Result"]
    })
    links.new(store_corner_edge_v2.outputs[0], store_is_fwd.inputs[0])

    prepared_geo = store_is_fwd.outputs[0]
    
    # --- 4.2 COMPUTE AND STORE FACE WINDING (before split/subdivide) ---
    # The domain polygon vertices are arranged CCW. If the mesh face's corners wind CW,
    # we need to flip the domain vertex order to prevent a "twisted" mapping.
    # Compute winding per-face BEFORE split, so it propagates through subdivision.
    
    # Get face corner positions using corners_of_face
    cof_winding = nodes.new("GeometryNodeCornersOfFace")
    face_idx_node = nodes.new("GeometryNodeInputIndex")  # In FACE context, this is face index
    links.new(face_idx_node.outputs[0], cof_winding.inputs["Face Index"])
    
    # Sample corner_pos at corners 0, 1, 2, 3 of each face
    def sample_face_corner_pos(sort_index):
        # Get the corner index for this face at the given sort position
        cof_corner = nodes.new("GeometryNodeCornersOfFace")
        links.new(face_idx_node.outputs[0], cof_corner.inputs["Face Index"])
        cof_corner.inputs["Weights"].default_value = 0.0
        cof_corner.inputs["Sort Index"].default_value = sort_index
        corner_at_sort = cof_corner.outputs["Corner Index"]
        
        # Sample the corner_pos at that corner index
        sample = create_node("GeometryNodeSampleIndex", {
            "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
            "Index": corner_at_sort
        })
        # Get the corner_pos attribute from prepared_geo
        corner_pos_attr_w = nodes.new("GeometryNodeInputNamedAttribute")
        corner_pos_attr_w.data_type = "FLOAT_VECTOR"
        corner_pos_attr_w.inputs["Name"].default_value = "corner_pos"
        links.new(corner_pos_attr_w.outputs[0], sample.inputs["Value"])
        return sample.outputs[0] 

    wc0 = sample_face_corner_pos(0)
    wc1 = sample_face_corner_pos(1)
    wc2 = sample_face_corner_pos(2)
    wc3 = sample_face_corner_pos(3) 
    
    # Compute cross product of two edges to get face normal direction
    edge01_w = vec_math_op("SUBTRACT", wc1, wc0)
    edge02_w = vec_math_op("SUBTRACT", wc2, wc0)
    face_normal_w = vec_math_op("CROSS_PRODUCT", edge01_w, edge02_w)
    
    # Compute face center
    fc_01 = vec_math_op("ADD", wc0, wc1)
    fc_012 = vec_math_op("ADD", fc_01, wc2)
    fc_sum = vec_math_op("ADD", fc_012, wc3)
    face_center_w = vec_math_op("SCALE", fc_sum, 0.25)
    
    # Dot product of face_center and face_normal
    # For a cube centered at origin: if dot < 0, face normal points inward (CW winding)
    center_dot_w = vec_math_op("DOT_PRODUCT", face_center_w, face_normal_w)
    
    flip_cmp = nodes.new("FunctionNodeCompare")
    flip_cmp.data_type = "FLOAT"
    flip_cmp.operation = "LESS_THAN"
    links.new(center_dot_w, flip_cmp.inputs["A"])
    flip_cmp.inputs["B"].default_value = 0.0
    face_flip_domain = flip_cmp.outputs["Result"]
    
    # Store flip_domain on FACE domain (will propagate through split/subdivide)
    store_flip = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "face_flip_domain", "Domain": "FACE", "Data Type": "BOOLEAN",
        "Value": face_flip_domain
    })
    links.new(prepared_geo, store_flip.inputs[0])
    prepared_geo_with_flip = store_flip.outputs[0]
    
# --- 5. SPLIT & SUBDIVIDE ---
    split = create_node("GeometryNodeSplitEdges", {"Mesh": prepared_geo_with_flip})
    
    store_crease = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "crease",
        "Domain": "EDGE",
        "Data Type": "FLOAT",
        "Value": 1.0
    })
    links.new(split.outputs[0], store_crease.inputs[0])
    
    subdiv = create_node("GeometryNodeSubdivideMesh", {
        "Mesh": store_crease.outputs[0],
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
    
    N_field = get_attr("poly_N", "INT")
    orig_loop_start_field = get_attr("orig_loop_start", "INT")
    
    # Get current point position
    current_pos = nodes.new("GeometryNodeInputPosition").outputs[0]

    # --- 6.0 Determine max N across patches (repeat iterations) ---
    stat_N_temp = create_node("GeometryNodeAttributeStatistic", {
        "Geometry": subdivided_geo, "Domain": "POINT", "Attribute": N_field
    })
    max_N_for_bary = stat_N_temp.outputs["Max"]
    
    # --- 6.0b READ FACE WINDING (stored before split/subdivide) ---
    # The flip_domain attribute was computed per-face before split and stored on FACE domain.
    # After subdivision, it propagates to each point from its face.
    flip_domain_attr = nodes.new("GeometryNodeInputNamedAttribute")
    flip_domain_attr.data_type = "BOOLEAN"
    flip_domain_attr.inputs["Name"].default_value = "face_flip_domain"
    flip_domain = flip_domain_attr.outputs[0]
    
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
    MV_valid = compare_int_less(MV_i, N_field)
    
    # Get corner index for this iteration
    MV_corner_idx = int_op("ADD", orig_loop_start_field, MV_i)
    
    # Sample corner position from original geometry
    sample_corner_i = create_node("GeometryNodeSampleIndex", {
        "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Index": MV_corner_idx
    })
    corner_pos_attr = nodes.new("GeometryNodeInputNamedAttribute")
    corner_pos_attr.data_type = "FLOAT_VECTOR"
    corner_pos_attr.inputs["Name"].default_value = "corner_pos"
    links.new(corner_pos_attr.outputs[0], sample_corner_i.inputs["Value"])
    corner_i_pos = sample_corner_i.outputs[0]
    
    # Get next corner position
    MV_ip1 = int_op("MODULO", int_op("ADD", MV_i, 1), N_field)
    MV_corner_ip1 = int_op("ADD", orig_loop_start_field, MV_ip1)
    sample_corner_ip1 = create_node("GeometryNodeSampleIndex", {
        "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Index": MV_corner_ip1
    })
    links.new(corner_pos_attr.outputs[0], sample_corner_ip1.inputs["Value"])
    corner_ip1_pos = sample_corner_ip1.outputs[0]
    
    # Get previous corner position
    MV_im1 = int_op("MODULO", int_op("ADD", int_op("SUBTRACT", MV_i, 1), N_field), N_field)
    MV_corner_im1 = int_op("ADD", orig_loop_start_field, MV_im1)
    sample_corner_im1 = create_node("GeometryNodeSampleIndex", {
        "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Index": MV_corner_im1
    })
    links.new(corner_pos_attr.outputs[0], sample_corner_im1.inputs["Value"])
    corner_im1_pos = sample_corner_im1.outputs[0]
    
    # Compute vectors from current point to corners
    v_to_i = vec_math_op("SUBTRACT", corner_i_pos, current_pos)
    v_to_ip1 = vec_math_op("SUBTRACT", corner_ip1_pos, current_pos)
    v_to_im1 = vec_math_op("SUBTRACT", corner_im1_pos, current_pos)
    
    # Distance to corner i
    dist_i = vec_math_op("LENGTH", v_to_i)
    dist_i_safe = math_op("MAXIMUM", dist_i, 1e-8)
    
    # Compute angle α_i at P subtended by edge (C_i, C_{i+1})
    # cos(α_i) = dot(v_to_i, v_to_ip1) / (|v_to_i| * |v_to_ip1|)
    dot_i_ip1 = vec_math_op("DOT_PRODUCT", v_to_i, v_to_ip1)
    dist_ip1 = vec_math_op("LENGTH", v_to_ip1)
    cos_alpha_i = math_op("DIVIDE", dot_i_ip1, 
                          math_op("MAXIMUM", math_op("MULTIPLY", dist_i, dist_ip1), 1e-8))
    # NOTE: Don't do "shift + clamp01" here. clamp01 clamps to [0,1] and would force cos into [-1,0],
    # which breaks mean value coordinates and causes boundary points to map to the wrong domain location.
    # tan_half_angle() already clamps cos to a safe range.
    
    # Compute angle α_{i-1} at P subtended by edge (C_{i-1}, C_i)
    dot_im1_i = vec_math_op("DOT_PRODUCT", v_to_im1, v_to_i)
    dist_im1 = vec_math_op("LENGTH", v_to_im1)
    cos_alpha_im1 = math_op("DIVIDE", dot_im1_i,
                            math_op("MAXIMUM", math_op("MULTIPLY", dist_im1, dist_i), 1e-8))
    
    # tan(α/2) = sqrt((1 - cos(α)) / (1 + cos(α)))
    def tan_half_angle(cos_a):
        # Clamp to avoid numerical issues
        cos_clamped = math_op("MINIMUM", 0.9999, math_op("MAXIMUM", -0.9999, cos_a))
        numer = math_op("SUBTRACT", 1.0, cos_clamped)
        denom = math_op("ADD", 1.0, cos_clamped)
        return math_op("SQRT", math_op("DIVIDE", numer, math_op("MAXIMUM", denom, 1e-8)))
    
    tan_half_i = tan_half_angle(cos_alpha_i)
    tan_half_im1 = tan_half_angle(cos_alpha_im1)
    
    # Mean value weight: w_i = (tan(α_{i-1}/2) + tan(α_i/2)) / |P - C_i|
    weight_i = math_op("DIVIDE", 
                       math_op("ADD", tan_half_im1, tan_half_i),
                       dist_i_safe)
    
    # Compute domain position for corner i
    # theta_i = (i + 0.5) * 2π / N + π
    # If flip_domain is true, we negate the angle to reverse the vertex order (CW instead of CCW)
    N_float = int_to_float(N_field)
    i_float = int_to_float(MV_i)
    
    # Base angle (CCW order)
    angle_step = math_op("DIVIDE", 6.283185307, N_float)
    base_angle = math_op("MULTIPLY", math_op("ADD", i_float, 0.5), angle_step)
    theta_ccw = math_op("ADD", base_angle, 3.14159265)
    
    # Flipped angle (CW order) - negate the base angle before adding offset
    theta_cw = math_op("SUBTRACT", 3.14159265, base_angle)
    
    # Select based on flip_domain
    theta_i = switch_float(flip_domain, theta_ccw, theta_cw)
    
    domain_corner_x = math_op("COSINE", theta_i)
    domain_corner_y = math_op("SINE", theta_i)
    
    # Weighted domain position contribution
    domain_contrib = nodes.new("ShaderNodeCombineXYZ")
    links.new(math_op("MULTIPLY", weight_i, domain_corner_x), domain_contrib.inputs["X"])
    links.new(math_op("MULTIPLY", weight_i, domain_corner_y), domain_contrib.inputs["Y"])
    
    # Accumulate (only if valid)
    new_sumW = switch_float(MV_valid, MV_sumW, math_op("ADD", MV_sumW, weight_i))
    new_sumDomain = switch_vec(MV_valid, MV_sumDomain, 
                               vec_math_op("ADD", MV_sumDomain, domain_contrib.outputs[0]))
    
    # Output from repeat
    links.new(MV_geo, repMV_out.inputs["Geometry"])
    links.new(new_sumW, repMV_out.inputs["SumW"])
    links.new(new_sumDomain, repMV_out.inputs["SumDomain"])
    links.new(int_op("ADD", MV_i, 1), repMV_out.inputs["IterIdx"])
    
    # Normalize to get final domain position
    final_sumW = repMV_out.outputs["SumW"]
    final_sumDomain = repMV_out.outputs["SumDomain"]
    inv_sumW = math_op("DIVIDE", 1.0, math_op("MAXIMUM", final_sumW, 1e-8))
    domain_pos_vec = vec_math_op("SCALE", final_sumDomain, inv_sumW)
    
    sep_domain_final = nodes.new("ShaderNodeSeparateXYZ")
    links.new(domain_pos_vec, sep_domain_final.inputs[0])
    domain_p_x = sep_domain_final.outputs["X"]
    domain_p_y = sep_domain_final.outputs["Y"]

    # --- 6.2 Determine max N across patches (repeat iterations) ---
    stat_N = create_node("GeometryNodeAttributeStatistic", {
        "Geometry": subdivided_geo, "Domain": "POINT", "Attribute": N_field
    })
    max_N = stat_N.outputs["Max"]

    # --- 6.1 DOMAIN INDEXING ---
    # IMPORTANT:
    # `domain_pos` (and later D_i distances) are already defined using the *face's corner order*
    # (corner i ↔ domain vertex i). Therefore edge index i corresponds to the mesh side between
    # corners (i-1, i), i.e. the incoming edge at corner i.
    #
    # Any extra "alignment" (shifts/flips) here will scramble which mesh edge is treated as side i
    # and can produce self-intersecting ("star") boundary loops.
    # (No shift applied; identity mapping below.)

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
        """Identity mapping: domain vertex i == mesh corner i (within the face's corner order)."""
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
        # Must use the same flip_domain logic as in mean-value coordinates
        # to ensure domain edge positions match the computed domain_p_x/y.
        angle_step_local = math_op("DIVIDE", 6.283185307, N_field)
        
        i_float_local = int_to_float(i_idx)
        i_prev = int_op("MODULO", int_op("ADD", int_op("SUBTRACT", i_idx, 1), N_field), N_field)
        i_prev_float = int_to_float(i_prev)
        
        # CCW angles (same formula as in mean-value coords)
        base_angle_prev = math_op("MULTIPLY", math_op("ADD", i_prev_float, 0.5), angle_step_local)
        theta0_ccw = math_op("ADD", base_angle_prev, 3.14159265)
        theta0_cw = math_op("SUBTRACT", 3.14159265, base_angle_prev)
        theta0 = switch_float(flip_domain, theta0_ccw, theta0_cw)
        
        base_angle_i = math_op("MULTIPLY", math_op("ADD", i_float_local, 0.5), angle_step_local)
        theta1_ccw = math_op("ADD", base_angle_i, 3.14159265)
        theta1_cw = math_op("SUBTRACT", 3.14159265, base_angle_i)
        theta1 = switch_float(flip_domain, theta1_ccw, theta1_cw)

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
    # FIX: Explicitly use base e (2.718281828) for natural log - Blender defaults to base 2!
    add_log = math_op("ADD", A_log, math_op("LOGARITHM", D_i_clamp, 2.718281828))

    A_log_final = switch_float(A_valid, A_log, add_log)

    links.new(A_geo, repA_out.inputs["Geometry"])
    links.new(A_log_final, repA_out.inputs["LogDTotal"])
    links.new(int_op("ADD", A_i, 1), repA_out.inputs["IterIdx"])

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
    B_valid = compare_int_less(B_i, N_field)
    # FIX: For vertex i, Wachspress weight w_i excludes D_i and D_{i+1} (the two edges meeting at vertex i)
    # In the code's convention, edge j connects vertex (j-1) to vertex j.
    # So vertex i is at the END of edge i, and at the START of edge (i+1).
    B_ip1 = int_op("MODULO", int_op("ADD", B_i, 1), N_field)
    D0 = domain_edge_distance(B_i)   # Edge i (ends at vertex i)
    D1 = domain_edge_distance(B_ip1) # Edge i+1 (starts at vertex i) 
    
    D0c = math_op("MAXIMUM", D0, 1.0e-8)
    D1c = math_op("MAXIMUM", D1, 1.0e-8)
    
    # log_w = LogTotal - (LogD_In + LogD_Out)
    # FIX: Explicitly use base e for natural log
    log_w = math_op("SUBTRACT", logD_total, math_op("ADD", math_op("LOGARITHM", D0c, 2.718281828), math_op("LOGARITHM", D1c, 2.718281828)))
    
    w_i = math_op("EXPONENT", log_w)
    sum_new = math_op("ADD", B_sumw, w_i)
    B_sum_final = switch_float(B_valid, B_sumw, sum_new)

    links.new(B_geo, repB_out.inputs["Geometry"])
    links.new(B_sum_final, repB_out.inputs["SumW"])
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

    # Wachspress λ_i for vertex i: excludes edges i and (i+1) meeting at vertex i
    Di = math_op("MAXIMUM", domain_edge_distance(C_i), 1.0e-8)
    Dip1 = math_op("MAXIMUM", domain_edge_distance(ip1), 1.0e-8)
    
    # FIX: Explicitly use base e for natural log
    log_w_i = math_op("SUBTRACT", logD_total, math_op("ADD", math_op("LOGARITHM", Di, 2.718281828), math_op("LOGARITHM", Dip1, 2.718281828)))
    wcur = math_op("EXPONENT", log_w_i)
    lam_i = math_op("DIVIDE", wcur, sumW)
 
    # Wachspress λ_{i-1} for vertex (i-1): excludes edges (i-1) and i meeting at vertex (i-1)
    Dim1 = math_op("MAXIMUM", domain_edge_distance(im1), 1.0e-8)

    # FIX: Explicitly use base e for natural log
    log_w_im1 = math_op("SUBTRACT", logD_total, math_op("ADD", math_op("LOGARITHM", Dim1, 2.718281828), math_op("LOGARITHM", Di, 2.718281828)))
    wprev = math_op("EXPONENT", log_w_im1)
    lam_im1 = math_op("DIVIDE", wprev, sumW)
    denom = math_op("MAXIMUM", math_op("ADD", lam_im1, lam_i), 1.0e-8)
    
    # Raw s_i, d_i from Wachspress coordinates
    s_i_raw = clamp01(math_op("DIVIDE", lam_i, denom))
    d_i_raw = clamp01(math_op("SUBTRACT", 1.0, math_op("ADD", lam_im1, lam_i)))
    
    # FIX: Apply quintic smoothstep for C2 continuity (matches coon_patch.py)
    s_i = smoother_step(s_i_raw)
    d_i = smoother_step(d_i_raw)

    # Evaluate boundary curves (paper indexing) with *incoming-edge* semantics:
    # We stored `corner_edge_idx` as EdgesOfCorner.Previous Edge Index, i.e. the incoming edge at corner i,
    # which is exactly the side between vertices (i-1, i). Therefore:
    #   C_i      -> edge_for_idx(i)
    #   C_{i-1}  -> edge_for_idx(i-1)
    #   C_{i+1}  -> edge_for_idx(i+1)
    # and for opp curve derivatives:
    #   C'_{i+2}(0) -> edge_for_idx(i+2)
    #   C'_{i-2}(1) -> edge_for_idx(i-2)
    e_i, f_i = edge_for_idx(C_i)     # C_i 
    e_im1, f_im1 = edge_for_idx(im1) # C_{i-1}
    e_ip1, f_ip1 = edge_for_idx(ip1) # C_{i+1}

    # Control points for C_i, C_{i-1}, C_{i+1}
    C0, C1, C2, C3 = edge_control_points(e_i, f_i)              # C_i
    Cm10, Cm11, Cm12, Cm13 = edge_control_points(e_im1, f_im1)  # C_{i-1}
    Cp10, Cp11, Cp12, Cp13 = edge_control_points(e_ip1, f_ip1)  # C_{i+1}

    Ci_si = bezier_eval(C0, C1, C2, C3, s_i)
    Cim1_1md = bezier_eval(Cm10, Cm11, Cm12, Cm13, math_op("SUBTRACT", 1.0, d_i))
    Cip1_d = bezier_eval(Cp10, Cp11, Cp12, Cp13, d_i)

    # Build C_i^{opp} (Eq. 2–3)
    e_ip2, f_ip2 = edge_for_idx(ip2) # C_{i+2}
    e_im2, f_im2 = edge_for_idx(im2) # C_{i-2}

    Cp20, Cp21, Cp22, Cp23 = edge_control_points(e_ip2, f_ip2)   # C_{i+2}
    Cm20, Cm21, Cm22, Cm23 = edge_control_points(e_im2, f_im2)   # C_{i-2}

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

    S_final = switch_vec(C_valid, C_sumS, S_new)
    B_final = switch_float(C_valid, C_sumB, B_new)

    links.new(C_geo, repC_out.inputs["Geometry"])
    links.new(S_final, repC_out.inputs["SumS"])
    links.new(B_final, repC_out.inputs["SumB"])
    links.new(int_op("ADD", C_i, 1), repC_out.inputs["IterIdx"])

    sumS = repC_out.outputs["SumS"]
    sumB = repC_out.outputs["SumB"]
    inv_sumB = math_op("DIVIDE", 1.0, math_op("MAXIMUM", sumB, 1.0e-8))
    final_pos_raw = vec_math_op("SCALE", sumS, inv_sumB)

    # --- 12. Exact boundary/vertex snap in domain ---
    # Wachspress + eps clamps make exact 0/1 boundaries numerically fuzzy (especially at vertices).
    # For Subdivisions=0, every point is a corner and must land exactly on a mesh vertex.
    # We enforce this by snapping points whose domain position is on (or very near) a domain edge
    # to the corresponding boundary curve evaluation.

    # Find closest domain edge index (min distance) for this point
    repE_in = nodes.new("GeometryNodeRepeatInput")
    repE_out = nodes.new("GeometryNodeRepeatOutput")
    repE_in.pair_with_output(repE_out)

    repE_out.repeat_items.new("GEOMETRY", "Geometry")
    repE_out.repeat_items.new("FLOAT", "MinD")
    repE_out.repeat_items.new("INT", "MinIdx")
    repE_out.repeat_items.new("INT", "IterIdx")

    links.new(repC_out.outputs["Geometry"], repE_in.inputs["Geometry"])
    links.new(max_N, repE_in.inputs["Iterations"])
    repE_in.inputs["MinD"].default_value = 1.0e20
    repE_in.inputs["MinIdx"].default_value = 0
    repE_in.inputs["IterIdx"].default_value = 0

    E_geo = repE_in.outputs["Geometry"]
    E_minD = repE_in.outputs["MinD"]
    E_minIdx = repE_in.outputs["MinIdx"]
    E_i = repE_in.outputs["IterIdx"]
    E_valid = compare_int_less(E_i, N_field)

    D_edge = domain_edge_distance(E_i)

    better = nodes.new("FunctionNodeCompare")
    better.data_type = "FLOAT"
    better.operation = "LESS_THAN"
    links.new(D_edge, better.inputs["A"])
    links.new(E_minD, better.inputs["B"])

    take = bool_and(E_valid, better.outputs["Result"])

    minD_final = switch_float(take, E_minD, D_edge)
    minIdx_final = switch_int(take, E_minIdx, E_i)

    links.new(E_geo, repE_out.inputs["Geometry"])
    links.new(minD_final, repE_out.inputs["MinD"])
    links.new(minIdx_final, repE_out.inputs["MinIdx"])
    links.new(int_op("ADD", E_i, 1), repE_out.inputs["IterIdx"])

    minD = repE_out.outputs["MinD"]
    minIdx = repE_out.outputs["MinIdx"]

    on_edge = compare_float_less(minD, 1.0e-6)

    # --- 12.1 Exact vertex snap (fixes vertex ambiguity) ---
    # At a domain vertex, TWO domain edges have distance 0, so the "closest edge" choice is ambiguous.
    # Relying on t_edge to become exactly 0/1 can flip to the opposite endpoint due to tiny numeric drift.
    # Instead: detect when we're at/near a domain vertex and snap directly to the corresponding mesh corner.
    repV_in = nodes.new("GeometryNodeRepeatInput")
    repV_out = nodes.new("GeometryNodeRepeatOutput")
    repV_in.pair_with_output(repV_out)

    repV_out.repeat_items.new("GEOMETRY", "Geometry")
    repV_out.repeat_items.new("FLOAT", "MinDV")
    repV_out.repeat_items.new("INT", "MinVIdx")
    repV_out.repeat_items.new("INT", "IterIdx")

    links.new(repC_out.outputs["Geometry"], repV_in.inputs["Geometry"])
    links.new(max_N, repV_in.inputs["Iterations"])
    repV_in.inputs["MinDV"].default_value = 1.0e20
    repV_in.inputs["MinVIdx"].default_value = 0
    repV_in.inputs["IterIdx"].default_value = 0

    V_geo = repV_in.outputs["Geometry"]
    V_minDV = repV_in.outputs["MinDV"]
    V_minVIdx = repV_in.outputs["MinVIdx"]
    V_i = repV_in.outputs["IterIdx"]
    V_valid = compare_int_less(V_i, N_field)

    # Domain vertex position for index V_i (same convention as domain_pos construction)
    # Must use flip_domain to match the mean-value coordinate computation
    v_angle_step = math_op("DIVIDE", 6.283185307, int_to_float(N_field))
    v_base_angle = math_op("MULTIPLY", math_op("ADD", int_to_float(V_i), 0.5), v_angle_step)
    v_theta_ccw = math_op("ADD", v_base_angle, 3.14159265)
    v_theta_cw = math_op("SUBTRACT", 3.14159265, v_base_angle)
    v_theta = switch_float(flip_domain, v_theta_ccw, v_theta_cw)
    vpx = math_op("COSINE", v_theta)
    vpy = math_op("SINE", v_theta)

    dxv = math_op("SUBTRACT", domain_p_x, vpx)
    dyv = math_op("SUBTRACT", domain_p_y, vpy)
    dv = math_op("SQRT", math_op("ADD", math_op("MULTIPLY", dxv, dxv), math_op("MULTIPLY", dyv, dyv)))

    v_better = nodes.new("FunctionNodeCompare")
    v_better.data_type = "FLOAT"
    v_better.operation = "LESS_THAN"
    links.new(dv, v_better.inputs["A"])
    links.new(V_minDV, v_better.inputs["B"])

    v_take = bool_and(V_valid, v_better.outputs["Result"])
    v_minDV_final = switch_float(v_take, V_minDV, dv)
    v_minVIdx_final = switch_int(v_take, V_minVIdx, V_i)

    links.new(V_geo, repV_out.inputs["Geometry"])
    links.new(v_minDV_final, repV_out.inputs["MinDV"])
    links.new(v_minVIdx_final, repV_out.inputs["MinVIdx"])
    links.new(int_op("ADD", V_i, 1), repV_out.inputs["IterIdx"])

    minDV = repV_out.outputs["MinDV"]
    minVIdx = repV_out.outputs["MinVIdx"]
    on_vertex = compare_float_less(minDV, 1.0e-5)

    # Compute parameter t along domain edge
    # Must use flip_domain to match domain_pos computation
    e_angle_step = math_op("DIVIDE", 6.283185307, N_field)
    
    minIdx_prev = int_op("MODULO", int_op("ADD", int_op("SUBTRACT", minIdx, 1), N_field), N_field)
    minIdx_prev_f = int_to_float(minIdx_prev)
    minIdx_f = int_to_float(minIdx)
    
    # theta for vertex at minIdx_prev
    e_base0 = math_op("MULTIPLY", math_op("ADD", minIdx_prev_f, 0.5), e_angle_step)
    e_theta0_ccw = math_op("ADD", e_base0, 3.14159265)
    e_theta0_cw = math_op("SUBTRACT", 3.14159265, e_base0)
    theta0 = switch_float(flip_domain, e_theta0_ccw, e_theta0_cw)
    
    # theta for vertex at minIdx
    e_base1 = math_op("MULTIPLY", math_op("ADD", minIdx_f, 0.5), e_angle_step)
    e_theta1_ccw = math_op("ADD", e_base1, 3.14159265)
    e_theta1_cw = math_op("SUBTRACT", 3.14159265, e_base1)
    theta1 = switch_float(flip_domain, e_theta1_ccw, e_theta1_cw)

    vx0 = math_op("COSINE", theta0)
    vy0 = math_op("SINE", theta0)
    vx1 = math_op("COSINE", theta1)
    vy1 = math_op("SINE", theta1)

    ex = math_op("SUBTRACT", vx1, vx0)
    ey = math_op("SUBTRACT", vy1, vy0)
    px = math_op("SUBTRACT", domain_p_x, vx0)
    py = math_op("SUBTRACT", domain_p_y, vy0)

    dot_pe = math_op("ADD", math_op("MULTIPLY", px, ex), math_op("MULTIPLY", py, ey))
    dot_ee = math_op("ADD", math_op("MULTIPLY", ex, ex), math_op("MULTIPLY", ey, ey))
    t_edge = clamp01(math_op("DIVIDE", dot_pe, math_op("MAXIMUM", dot_ee, 1.0e-8)))

    # Map domain edge minIdx (between vertices minIdx-1 -> minIdx) to corresponding mesh edge curve.
    # We stored incoming edges at corners, so edge_for_idx(i) is exactly the edge between (i-1, i).
    edge_id, edge_fwd = edge_for_idx(minIdx)
    P0e, P1e, P2e, P3e = edge_control_points(edge_id, edge_fwd)
    edge_pos = bezier_eval(P0e, P1e, P2e, P3e, t_edge)

    # If on a domain edge, snap to that boundary curve.
    final_pos_edge = switch_vec(on_edge, final_pos_raw, edge_pos)

    # If on a domain vertex, snap to the exact mesh corner position (overrides edge snap).
    corner_attr = nodes.new("GeometryNodeInputNamedAttribute")
    corner_attr.data_type = "FLOAT_VECTOR"
    corner_attr.inputs["Name"].default_value = "corner_pos"
    corner_corner_idx = corner_for_idx(minVIdx)
    sample_corner_vpos = create_node("GeometryNodeSampleIndex", {
        "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Index": corner_corner_idx
    })
    links.new(corner_attr.outputs[0], sample_corner_vpos.inputs["Value"])
    corner_vpos = sample_corner_vpos.outputs[0]

    final_pos = switch_vec(on_vertex, final_pos_edge, corner_vpos)
    
    set_pos = nodes.new("GeometryNodeSetPosition")
    links.new(repC_out.outputs["Geometry"], set_pos.inputs["Geometry"])
    links.new(final_pos, set_pos.inputs["Position"])
    
    # --- 13. DEBUG ATTRIBUTES ---
    # Store debug values for inspection in Blender spreadsheet
    geo_with_debug = set_pos.outputs[0]

    # debug_point_index: point index in the output mesh (lets us correlate with edge vertex indices)
    point_index = nodes.new("GeometryNodeInputIndex").outputs[0]
    store_debug_point_index = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_point_index", "Domain": "POINT", "Data Type": "INT",
        "Value": point_index
    })
    links.new(geo_with_debug, store_debug_point_index.inputs[0])
    geo_with_debug = store_debug_point_index.outputs[0]

    # debug_orig_loop_start / debug_poly_N: verify per-face constants aren't getting mixed on points
    store_debug_loop_start = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_orig_loop_start", "Domain": "POINT", "Data Type": "INT",
        "Value": orig_loop_start_field
    })
    links.new(geo_with_debug, store_debug_loop_start.inputs[0])
    geo_with_debug = store_debug_loop_start.outputs[0]

    store_debug_poly_n = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_poly_N", "Domain": "POINT", "Data Type": "INT",
        "Value": N_field
    })
    links.new(geo_with_debug, store_debug_poly_n.inputs[0])
    geo_with_debug = store_debug_poly_n.outputs[0]

    # debug_edge_id: which original mesh edge we snapped to (when on_edge)
    store_debug_edge_id = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_edge_id", "Domain": "POINT", "Data Type": "INT",
        "Value": edge_id
    })
    links.new(geo_with_debug, store_debug_edge_id.inputs[0])
    geo_with_debug = store_debug_edge_id.outputs[0]

    # debug_edge_fwd: whether edge control points are evaluated forward
    edge_fwd_int = switch_int(edge_fwd, 0, 1)
    store_debug_edge_fwd = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_edge_fwd", "Domain": "POINT", "Data Type": "INT",
        "Value": edge_fwd_int
    })
    links.new(geo_with_debug, store_debug_edge_fwd.inputs[0])
    geo_with_debug = store_debug_edge_fwd.outputs[0]

    # debug_t_edge: parameter along chosen domain edge (0..1)
    store_debug_t_edge = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_t_edge", "Domain": "POINT", "Data Type": "FLOAT",
        "Value": t_edge
    })
    links.new(geo_with_debug, store_debug_t_edge.inputs[0])
    geo_with_debug = store_debug_t_edge.outputs[0]

    # debug_on_edge: whether the edge snap path was used
    store_debug_on_edge = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_on_edge", "Domain": "POINT", "Data Type": "BOOLEAN",
        "Value": on_edge
    })
    links.new(geo_with_debug, store_debug_on_edge.inputs[0])
    geo_with_debug = store_debug_on_edge.outputs[0]
    
    # debug_flip_domain: whether the face required domain flip (CW winding)
    store_debug_flip = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_flip_domain", "Domain": "POINT", "Data Type": "BOOLEAN",
        "Value": flip_domain
    })
    links.new(geo_with_debug, store_debug_flip.inputs[0])
    geo_with_debug = store_debug_flip.outputs[0]
    
    # debug_sumB: Sum of blending weights (should be ~1 for interior points)
    store_debug_sumB = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_sumB", "Domain": "POINT", "Data Type": "FLOAT",
        "Value": sumB
    })
    links.new(geo_with_debug, store_debug_sumB.inputs[0])
    geo_with_debug = store_debug_sumB.outputs[0]
    
    # debug_minD: Minimum distance to domain edge (0 = on boundary)
    store_debug_minD = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_minD", "Domain": "POINT", "Data Type": "FLOAT",
        "Value": minD
    })
    links.new(geo_with_debug, store_debug_minD.inputs[0])
    geo_with_debug = store_debug_minD.outputs[0]
    
    # debug_minIdx: Index of closest domain edge
    store_debug_minIdx = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_minIdx", "Domain": "POINT", "Data Type": "INT",
        "Value": minIdx
    })
    links.new(geo_with_debug, store_debug_minIdx.inputs[0])
    geo_with_debug = store_debug_minIdx.outputs[0]
    
    # debug_domain_x: Computed domain X coordinate (from mean value coords)
    store_debug_domain_x = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_domain_x", "Domain": "POINT", "Data Type": "FLOAT",
        "Value": domain_p_x
    })
    links.new(geo_with_debug, store_debug_domain_x.inputs[0])
    geo_with_debug = store_debug_domain_x.outputs[0]
    
    # debug_domain_y: Computed domain Y coordinate (from mean value coords)
    store_debug_domain_y = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_domain_y", "Domain": "POINT", "Data Type": "FLOAT",
        "Value": domain_p_y
    })
    links.new(geo_with_debug, store_debug_domain_y.inputs[0])
    geo_with_debug = store_debug_domain_y.outputs[0]
    
    # debug_orig_face_idx: Which original face this point belongs to
    store_debug_face = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_orig_face_idx", "Domain": "POINT", "Data Type": "INT",
        "Value": get_attr("orig_face_idx", "INT")
    })
    links.new(geo_with_debug, store_debug_face.inputs[0])
    geo_with_debug = store_debug_face.outputs[0]
    
    # Optional: merge vertices back together.
    # NOTE: During debugging, disabling this avoids averaging attributes/positions at shared corners.
    merge = create_node("GeometryNodeMergeByDistance", {
        "Geometry": geo_with_debug, "Distance": 0.0001
    })

    geom_after_merge = switch_node("GEOMETRY",
                                   group_input.outputs["Merge By Distance"],
                                   geo_with_debug,
                                   merge.outputs[0])
    
    # Smooth shading
    set_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    links.new(geom_after_merge, set_smooth.inputs[0])
    set_smooth.inputs["Shade Smooth"].default_value = True

    # Final point index (after optional merge). This matches indices used by exported EDGE spreadsheets.
    out_point_index = nodes.new("GeometryNodeInputIndex").outputs[0]
    store_debug_out_point_index = create_node("GeometryNodeStoreNamedAttribute", {
        "Name": "debug_out_point_index", "Domain": "POINT", "Data Type": "INT",
        "Value": out_point_index
    })
    links.new(set_smooth.outputs[0], store_debug_out_point_index.inputs[0])
    
    links.new(store_debug_out_point_index.outputs[0], group_output.inputs[0])
    
    auto_layout_nodes(group)
    return group
