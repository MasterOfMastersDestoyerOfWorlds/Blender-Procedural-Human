import bpy
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group

@geo_node_group
def create_coons_patch_group():
    group_name = "CoonsPatchGenerator"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    
    # --- Interface ---
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Subdivisions", in_out="INPUT", socket_type="NodeSocketInt").default_value = 4
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    
    # --- Helpers ---
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

    # --- 1. Inputs ---
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    
    # --- 2. Topology Analysis (Face Corners) ---
    # Goal: Identify if a corner is 0 (Bottom-Left), 1 (Bottom-Right), 2 (Top-Right), or 3 (Top-Left)
    
    # Get Current Corner Index
    corner_idx_node = nodes.new("GeometryNodeInputIndex") # Domain: Corner
    
    # Get Face Index of this Corner
    face_of_corner = nodes.new("GeometryNodeFaceOfCorner")
    links.new(corner_idx_node.outputs[0], face_of_corner.inputs["Corner Index"])
    face_idx = face_of_corner.outputs["Face Index"]
    
    # Get First Corner Index of this Face (Sort Index 0)
    # "Corners of Face" looks up the global Corner Index for a specific Sort Index (0 here)
    corners_lookup_0 = nodes.new("GeometryNodeCornersOfFace")
    links.new(face_idx, corners_lookup_0.inputs["Face Index"])
    corners_lookup_0.inputs["Sort Index"].default_value = 0
    first_corner_idx = corners_lookup_0.outputs["Corner Index"]
    
    # Calculate Sort Index: Current - Start
    sort_idx = create_math('SUBTRACT', corner_idx_node.outputs[0], first_corner_idx)
    
    # --- Store UV on Corners ---
    # U = (SortIdx == 1) or (SortIdx == 2)
    # V = (SortIdx == 2) or (SortIdx == 3)
    
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

    # --- 3. Identify Edge Indices per Corner ---
    # "Edges of Corner" gives the edge connected to this corner in the winding direction (Next Edge)
    edges_of_corner = nodes.new("GeometryNodeEdgesOfCorner")
    # Note: EdgesOfCorner inputs implicitly use Context Corner Index if not connected
    edge_idx_at_corner = edges_of_corner.outputs["Next Edge Index"]
    
    store_edge_indices = nodes.new("GeometryNodeStoreNamedAttribute")
    store_edge_indices.data_type = 'INT'
    store_edge_indices.domain = 'CORNER'
    store_edge_indices.inputs["Name"].default_value = "corner_edge_idx"
    links.new(store_uv.outputs[0], store_edge_indices.inputs[0])
    links.new(edge_idx_at_corner, store_edge_indices.inputs["Value"])
    
    # --- Determine Edge Direction ---
    # Compare Corner Vertex with Edge Vertex 0
    vertex_of_corner = nodes.new("GeometryNodeVertexOfCorner")
    # (Implicit input: Context Corner Index)
    
    # Evaluate Edge Vertex 0 at the specific Edge Index we just found
    sample_edge_vert0 = nodes.new("GeometryNodeSampleIndex")
    sample_edge_vert0.domain = 'EDGE'
    sample_edge_vert0.data_type = 'INT'
    links.new(store_edge_indices.outputs[0], sample_edge_vert0.inputs["Geometry"])
    links.new(edge_idx_at_corner, sample_edge_vert0.inputs["Index"])
    
    # If Corner Vertex == Vertex 2 (Index 1), then we are at the end, so Edge Direction is BACKWARD relative to face winding?
    # Actually, standard: Edge is V1->V2.
    # If Corner is V1, we are at start.
    # If Corner is V2, we are at end.
    
    # Let's check if Corner == Vertex Index 1 (the first vertex, index 0 in UI but maybe "Vertex Index 1" in API?)
    # The socket names are "Vertex Index 1" and "Vertex Index 2".
    
    # If Corner Vertex == Vertex 1 (Index 0), then we are at the start of the edge.
    # Winding order usually goes V0 -> V1.
    # If we are at V0, we traverse forward to V1.
    # If we are at V1, we traverse backward to V0.
    
    # We compare Corner Vert Index with Edge Vert Index 0.
    # If Equal -> We are at Start -> Forward (True)
    # If Not Equal -> We are at End (V1) -> Backward (False)
    
    edge_verts_node = nodes.new("GeometryNodeInputMeshEdgeVertices")
    # socket 0 is "Vertex Index 1" (start)
    links.new(edge_verts_node.outputs[0], sample_edge_vert0.inputs["Value"])
    
    is_at_start = create_math('COMPARE', vertex_of_corner.outputs["Vertex Index"], sample_edge_vert0.outputs[0])
    
    # BUT! The previous logic using COMPARE directly as boolean 0/1 might be tricky if not exact match (float vs int).
    # Using 'EQUAL' operation for integer comparison is safer if available, but COMPARE works for floats.
    # Vertex indices are INTs. Use 'EQUAL'.
    
    # Use 'EQUAL' for Integer comparison, which is safer for indices
    is_at_start_node = nodes.new("FunctionNodeCompare")
    is_at_start_node.data_type = 'INT'
    is_at_start_node.operation = 'EQUAL'

    # Compare the Corner Vertex Index
    links.new(vertex_of_corner.outputs["Vertex Index"], is_at_start_node.inputs["A"])

    # Against the Edge's First Vertex Index (Vertex Index 1)
    # We must ensure sample_edge_vert0 is sampling the correct edge
    links.new(sample_edge_vert0.outputs["Value"], is_at_start_node.inputs["B"]) 

    
    is_forward = is_at_start_node.outputs["Result"]
    
    store_direction = nodes.new("GeometryNodeStoreNamedAttribute")
    store_direction.data_type = 'BOOLEAN'
    store_direction.domain = 'CORNER'
    store_direction.inputs["Name"].default_value = "edge_is_forward"
    links.new(store_edge_indices.outputs[0], store_direction.inputs[0])
    links.new(is_forward, store_direction.inputs["Value"])
    # Store this Result
    links.new(is_at_start_node.outputs["Result"], store_direction.inputs["Value"])

    # --- 4. Capture Data to FACE Domain ---
    # We need E0 (Bottom), E1 (Right), E2 (Top), E3 (Left) available on the Face domain.
    # We do this by looking up the specific corners of the face (Sort Index 0, 1, 2, 3).
    
    # Sort Index mapping is crucial.
    # 0 -> Bottom Left
    # 1 -> Bottom Right
    # 2 -> Top Right
    # 3 -> Top Left
    
    # The edges connected to these corners:
    # Corner 0 connects to Edge 0 (Bottom) and Edge 3 (Left) usually.
    # But "Edges of Corner" gives the edge in the winding direction (Next Edge).
    # So Corner 0 -> Next Edge is Edge 0 (Bottom).
    # Corner 1 -> Next Edge is Edge 1 (Right).
    # Corner 2 -> Next Edge is Edge 2 (Top).
    # Corner 3 -> Next Edge is Edge 3 (Left).
    
    def get_data_from_corner_sort_id(geo_link, sort_id_val, attr_name, type='INT'):
        # 1. Get Face Index (Context: Face)
        face_idx_node = nodes.new("GeometryNodeInputIndex") 
        
        # 2. Get Corner Index for this Sort ID on this Face
        c_lookup = nodes.new("GeometryNodeCornersOfFace")
        links.new(face_idx_node.outputs[0], c_lookup.inputs["Face Index"])
        c_lookup.inputs["Sort Index"].default_value = sort_id_val
        target_corner = c_lookup.outputs["Corner Index"]
        
        # 3. Sample the attribute from that Corner
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

    # Store 4 Edge Indices and 4 Directions on the Face
    def store_face_attr(geo, name, val, type='INT'):
        s = nodes.new("GeometryNodeStoreNamedAttribute")
        s.domain = 'FACE'
        s.data_type = type
        s.inputs["Name"].default_value = name
        links.new(geo, s.inputs[0])
        links.new(val, s.inputs["Value"])
        return s.outputs[0]

    # Chain the stores
    geo = store_direction.outputs[0]
    
    # Edges
    geo = store_face_attr(geo, "e0", get_data_from_corner_sort_id(geo, 0, "corner_edge_idx"))
    geo = store_face_attr(geo, "e1", get_data_from_corner_sort_id(geo, 1, "corner_edge_idx"))
    geo = store_face_attr(geo, "e2", get_data_from_corner_sort_id(geo, 2, "corner_edge_idx"))
    geo = store_face_attr(geo, "e3", get_data_from_corner_sort_id(geo, 3, "corner_edge_idx"))
    
    # Directions
    geo = store_face_attr(geo, "d0", get_data_from_corner_sort_id(geo, 0, "edge_is_forward", 'BOOLEAN'), 'BOOLEAN')
    geo = store_face_attr(geo, "d1", get_data_from_corner_sort_id(geo, 1, "edge_is_forward", 'BOOLEAN'), 'BOOLEAN')
    geo = store_face_attr(geo, "d2", get_data_from_corner_sort_id(geo, 2, "edge_is_forward", 'BOOLEAN'), 'BOOLEAN')
    geo = store_face_attr(geo, "d3", get_data_from_corner_sort_id(geo, 3, "edge_is_forward", 'BOOLEAN'), 'BOOLEAN')
    
    # Store Source Face Index
    store_face_idx = nodes.new("GeometryNodeStoreNamedAttribute")
    store_face_idx.domain = 'FACE'
    store_face_idx.data_type = 'INT'
    store_face_idx.inputs["Name"].default_value = "src_face_index"
    links.new(geo, store_face_idx.inputs[0])
    links.new(nodes.new("GeometryNodeInputIndex").outputs[0], store_face_idx.inputs["Value"])
    
    geo = store_face_idx.outputs[0]
    
    # Keeping a reference to geometry with face attributes for later sampling
    geo_with_face_attrs = geo

    # --- 5. Generate Grid Geometry per Face ---
    # Replace Subdivide Mesh with Grid Instancing for clean topology per face
    
    # Create Grid Primitive
    grid = nodes.new("GeometryNodeMeshGrid")
    grid.inputs["Size X"].default_value = 1.0
    grid.inputs["Size Y"].default_value = 1.0
    links.new(group_input.outputs["Subdivisions"], grid.inputs["Vertices X"])
    links.new(group_input.outputs["Subdivisions"], grid.inputs["Vertices Y"])
    
    # Capture Attributes on Points before instancing
    # We need to ensure e0..e3, d0..d3 are available on the points for instancing
    # Mesh to Points (Face)
    mesh_to_points = nodes.new("GeometryNodeMeshToPoints")
    mesh_to_points.mode = 'FACES'
    links.new(geo, mesh_to_points.inputs["Mesh"])
    
    # Instance on Points
    instance = nodes.new("GeometryNodeInstanceOnPoints")
    links.new(mesh_to_points.outputs["Points"], instance.inputs["Points"])
    links.new(grid.outputs["Mesh"], instance.inputs["Instance"])
    
    # Realize Instances to get actual geometry
    realize = nodes.new("GeometryNodeRealizeInstances")
    links.new(instance.outputs["Instances"], realize.inputs["Geometry"])
    
    subdivided_geo = realize.outputs["Geometry"]
    
    # --- 6. UV Logic (From Grid Position) ---
    # Grid creates positions from -0.5 to 0.5. We map to 0..1
    pos_node = nodes.new("GeometryNodeInputPosition")
    
    # Separate XYZ
    sep_pos = nodes.new("ShaderNodeSeparateXYZ")
    links.new(pos_node.outputs[0], sep_pos.inputs[0])
    
    # Map -0.5..0.5 to 0..1: (val + 0.5)
    u_raw = create_math('ADD', sep_pos.outputs["X"], 0.5)
    v_raw = create_math('ADD', sep_pos.outputs["Y"], 0.5)
    
    # Smoother Step (6t^5 - 15t^4 + 10t^3)
    def smoother_step(val_node):
        s1 = create_math('SUBTRACT', create_math('MULTIPLY', val_node, 6.0), 15.0)
        s2 = create_math('ADD', create_math('MULTIPLY', val_node, s1), 10.0)
        t3 = create_math('POWER', val_node, 3.0)
        return create_math('MULTIPLY', t3, s2)

    u_smooth = smoother_step(u_raw)
    v_smooth = smoother_step(v_raw)

    # Function: Evaluate Bezier
    def eval_bezier_curve(geo_ref, edge_idx_field, is_fwd_field, t_field, original_geometry):
        # We need to handle the is_fwd_field carefully.
        # Logic Recap:
        # P0 = (is_fwd) ? Start : End
        # P3 = (is_fwd) ? End : Start
        # If is_fwd is True: Curve is Start->End. t=0 is Start. t=1 is End.
        # If is_fwd is False: Curve is End->Start. t=0 is End. t=1 is Start.
        
        # When we sample along an edge using "Sample Index", we don't have a concept of "Forward/Backward" built-in
        # unless we are sampling at specific t.
        # BUT, the curve logic below constructs P0..P3 based on this flag.
        
        # Helper to sample edge attribute by index
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
        
        # Helper to get vertex pos from edge
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

        p_start = get_vert_pos(0) # Vertex 1 (Index 0)
        p_end = get_vert_pos(1)   # Vertex 2 (Index 1)
        
        # Combine handles
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
        
        # Logic for orientation
        # If Forward (True): We want curve from V0 to V1.
        #   P0 = V0 (p_start)
        #   P3 = V1 (p_end)
        #   P1 = V0 + h_start
        #   P2 = V1 + h_end
        
        # If Backward (False): We want curve from V1 to V0.
        #   P0 = V1 (p_end)
        #   P3 = V0 (p_start)
        #   P1 = V1 + h_end
        #   P2 = V0 + h_start
        
        # MIX NODE: Factor 0 -> A, Factor 1 -> B.
        # Wait, Blender Mix Node: A is top (0), B is bottom (1).
        # Boolean True maps to 1. False maps to 0.
        
        # If is_fwd (1): We want P0=p_start. So p_start should be B. p_end should be A.
        #   Mix(0, p_end, p_start) -> p_end (Backward P0)
        #   Mix(1, p_end, p_start) -> p_start (Forward P0)
        # This matches current code:
        # links.new(p_end, mix_p0.inputs["A"])
        # links.new(p_start, mix_p0.inputs["B"])
        
        mix_p0 = nodes.new("ShaderNodeMix")
        mix_p0.data_type = 'VECTOR'
        links.new(is_fwd_field, mix_p0.inputs["Factor"])
        links.new(p_end, mix_p0.inputs["A"])
        links.new(p_start, mix_p0.inputs["B"])
        P0 = mix_p0.outputs["Result"]
        
        # P3: If Forward (1), want p_end. So p_end is B. p_start is A.
        mix_p3 = nodes.new("ShaderNodeMix")
        mix_p3.data_type = 'VECTOR'
        links.new(is_fwd_field, mix_p3.inputs["Factor"])
        links.new(p_start, mix_p3.inputs["A"])
        links.new(p_end, mix_p3.inputs["B"])
        P3 = mix_p3.outputs["Result"]
        
        # P1: If Forward (1), want p_start + h_start.
        #     If Backward (0), want p_end + h_end.
        p1_fwd = create_vec_math('ADD', p_start, h_start)
        p1_bwd = create_vec_math('ADD', p_end, h_end)
        mix_p1 = nodes.new("ShaderNodeMix")
        mix_p1.data_type = 'VECTOR'
        links.new(is_fwd_field, mix_p1.inputs["Factor"])
        links.new(p1_bwd, mix_p1.inputs["A"])
        links.new(p1_fwd, mix_p1.inputs["B"])
        P1 = mix_p1.outputs["Result"]
        
        # P2: If Forward (1), want p_end + h_end.
        #     If Backward (0), want p_start + h_start.
        p2_fwd = create_vec_math('ADD', p_end, h_end)
        p2_bwd = create_vec_math('ADD', p_start, h_start)
        mix_p2 = nodes.new("ShaderNodeMix")
        mix_p2.data_type = 'VECTOR'
        links.new(is_fwd_field, mix_p2.inputs["Factor"])
        links.new(p2_bwd, mix_p2.inputs["A"])
        links.new(p2_fwd, mix_p2.inputs["B"])
        P2 = mix_p2.outputs["Result"]
        
        # Bezier Calculation
        one_minus_t = create_math('SUBTRACT', 1.0, t_field)
        
        c0 = create_math('POWER', one_minus_t, 3.0)
        c1 = create_math('MULTIPLY', create_math('MULTIPLY', 3.0, create_math('POWER', one_minus_t, 2.0)), t_field)
        c2 = create_math('MULTIPLY', create_math('MULTIPLY', 3.0, one_minus_t), create_math('POWER', t_field, 2.0))
        c3 = create_math('POWER', t_field, 3.0)
        
        return create_vec_math('ADD', 
            create_vec_math('ADD', create_vec_math('SCALE', P0, c0), create_vec_math('SCALE', P1, c1)),
            create_vec_math('ADD', create_vec_math('SCALE', P2, c2), create_vec_math('SCALE', P3, c3))
        )

    # Helper to get stored face attributes (sampled from source geometry using src_face_index)
    def get_face_attr(name, type='INT'):
        # 1. Get src_face_index from current geometry (propagated from instance)
        get_src_idx = nodes.new("GeometryNodeInputNamedAttribute")
        get_src_idx.data_type = 'INT'
        get_src_idx.inputs["Name"].default_value = "src_face_index"
        
        # 2. Sample the attribute from geo_with_face_attrs at that index
        s = nodes.new("GeometryNodeSampleIndex")
        s.domain = 'FACE'
        s.data_type = type
        links.new(geo_with_face_attrs, s.inputs["Geometry"])
        links.new(get_src_idx.outputs[0], s.inputs["Index"])
        
        get_attr = nodes.new("GeometryNodeInputNamedAttribute")
        get_attr.data_type = type
        get_attr.inputs["Name"].default_value = name
        links.new(get_attr.outputs[0], s.inputs["Value"])
        
        return s.outputs[0]
        
    e0, d0 = get_face_attr("e0"), get_face_attr("d0", 'BOOLEAN')
    e1, d1 = get_face_attr("e1"), get_face_attr("d1", 'BOOLEAN')
    e2, d2 = get_face_attr("e2"), get_face_attr("e2", 'BOOLEAN') # Typo check: "d2"
    d2 = get_face_attr("d2", 'BOOLEAN') # Fix
    e3, d3 = get_face_attr("e3"), get_face_attr("d3", 'BOOLEAN')

    # Curves
    # Note: U is 0..1 (Left to Right), V is 0..1 (Bottom to Top)
    # c_bottom: V=0. Should use Edge 0 (Bottom). Edge 0 starts at Corner 0.
    # c_top: V=1. Should use Edge 2 (Top). Edge 2 starts at Corner 2.
    # c_right: U=1. Should use Edge 1 (Right). Edge 1 starts at Corner 1.
    # c_left: U=0. Should use Edge 3 (Left). Edge 3 starts at Corner 3.
    
    # Check orientation logic:
    # If edge is forward (V0->V1), T=0 is V0, T=1 is V1.
    # E0 (Bottom): V0 is Corner 0 (u=0, v=0), V1 is Corner 1 (u=1, v=0). 
    #   So T aligns with U.
    # E2 (Top): V0 is Corner 2 (u=1, v=1), V1 is Corner 3 (u=0, v=1).
    #   Wait! Winding order: 0->1->2->3.
    #   Edge 2 goes from Corner 2 to Corner 3.
    #   Corner 2 is (1,1). Corner 3 is (0,1).
    #   So Edge 2 travels from Right to Left (U=1 to U=0).
    #   So T=0 is Right, T=1 is Left.
    #   We want c_top(u). 
    #   If we sample at parameter (1-u):
    #     At u=0 (Left), param=1 (End of E2 = Corner 3 = Left). Correct.
    #     At u=1 (Right), param=0 (Start of E2 = Corner 2 = Right). Correct.
    
    # E1 (Right): V0 is Corner 1 (u=1, v=0), V1 is Corner 2 (u=1, v=1).
    #   So T aligns with V (0->1).
    #   We want c_right(v).
    #   Sample at v. Correct.
    
    # E3 (Left): V0 is Corner 3 (u=0, v=1), V1 is Corner 0 (u=0, v=0).
    #   Edge 3 travels Top to Bottom (V=1 to V=0).
    #   So T=0 is Top, T=1 is Bottom.
    #   We want c_left(v).
    #   If we sample at parameter (1-v):
    #     At v=0 (Bottom), param=1 (End of E3 = Corner 0 = Bottom). Correct.
    #     At v=1 (Top), param=0 (Start of E3 = Corner 3 = Top). Correct.
    
    # BUT, "Corners of Face" returns corners in CCW winding order.
    # 0 -> 1 -> 2 -> 3.
    # If the face is flipped or winding is different on sides, this breaks.
    # Sides of a cube: normals point out. Winding is CCW from outside.
    # 0->1 (Bottom), 1->2 (Right), 2->3 (Top), 3->0 (Left).
    # This assumption holds for any convex quad face.
    
    c_bottom = eval_bezier_curve(subdivided_geo, e0, d0, u_raw, group_input.outputs[0])
    c_top    = eval_bezier_curve(subdivided_geo, e2, d2, create_math('SUBTRACT', 1.0, u_raw), group_input.outputs[0])
    c_left   = eval_bezier_curve(subdivided_geo, e3, d3, create_math('SUBTRACT', 1.0, v_raw), group_input.outputs[0])
    c_right  = eval_bezier_curve(subdivided_geo, e1, d1, v_raw, group_input.outputs[0])
    
    # Corners (Bilinear Patch)
    # P00: u=0, v=0 (Bottom-Left) -> Corner 0. 
    #   Ideally use Corner 0 position directly.
    #   Using e0(0) (Start of Edge 0) -> Corner 0. Correct.
    
    # P10: u=1, v=0 (Bottom-Right) -> Corner 1.
    #   Using e0(1) (End of Edge 0) -> Corner 1. Correct.
    
    # P11: u=1, v=1 (Top-Right) -> Corner 2.
    #   Using e2(0) (Start of Edge 2) -> Corner 2.
    #   Wait, in our logic above (c_top), we established E2 goes R->L (2->3).
    #   So e2(0) is Corner 2 (Right). Correct.
    
    # P01: u=0, v=1 (Top-Left) -> Corner 3.
    #   Using e2(1) (End of Edge 2) -> Corner 3. Correct.
    
    # Previous code:
    # p00 = eval(e0, 0.0) -> Corner 0. OK.
    # p10 = eval(e0, 1.0) -> Corner 1. OK.
    # p01 = eval(e2, 1.0) -> Corner 3. OK. (0,1)
    # p11 = eval(e2, 0.0) -> Corner 2. OK. (1,1)
    
    p00 = eval_bezier_curve(subdivided_geo, e0, d0, 0.0, group_input.outputs[0])
    p10 = eval_bezier_curve(subdivided_geo, e0, d0, 1.0, group_input.outputs[0])
    p01 = eval_bezier_curve(subdivided_geo, e2, d2, 1.0, group_input.outputs[0])
    p11 = eval_bezier_curve(subdivided_geo, e2, d2, 0.0, group_input.outputs[0])
    
    # Lofts
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
    
    # Bilinear
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
    
    # Coons Sum: LU + LV - B
    final_pos = create_vec_math('SUBTRACT', 
        create_vec_math('ADD', loft_u.outputs["Result"], loft_v.outputs["Result"]), 
        bilinear.outputs["Result"]
    )
    
    # Output
    set_pos = nodes.new("GeometryNodeSetPosition")
    links.new(subdivided_geo, set_pos.inputs["Geometry"])
    links.new(final_pos, set_pos.inputs["Position"])
    
    # Weld Vertices (Merge by Distance) to close gaps
    merge = nodes.new("GeometryNodeMergeByDistance")
    links.new(set_pos.outputs[0], merge.inputs["Geometry"])
    merge.inputs["Distance"].default_value = 0.001
    
    set_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    links.new(merge.outputs[0], set_smooth.inputs[0])
    set_smooth.inputs["Shade Smooth"].default_value = True

    links.new(set_smooth.outputs[0], group_output.inputs[0])
    
    auto_layout_nodes(group)
    return group