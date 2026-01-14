import bpy

# --- Helpers ---
def is_socket(obj):
    return isinstance(obj, bpy.types.NodeSocket) 

def link_or_set(group, socket_in, value):
    if is_socket(value):
        group.links.new(value, socket_in)
    elif isinstance(value, (int, float, bool, str)):
        socket_in.default_value = value 
    elif isinstance(value, (tuple, list)):
        socket_in.default_value = value

def create_node(group, type_name, inputs=None, **properties):
    node = group.nodes.new(type_name)
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
                link_or_set(group, node.inputs[k], v)
    return node

def math_op(group, op, a, b=None):
    n = group.nodes.new("ShaderNodeMath")
    n.operation = op
    link_or_set(group, n.inputs[0], a)
    if b is not None:
        link_or_set(group, n.inputs[1], b)
    return n.outputs[0]

def vec_math_op(group, op, a, b=None):
    n = group.nodes.new("ShaderNodeVectorMath")
    n.operation = op
    link_or_set(group, n.inputs[0], a)
    if b is not None:
        if op == 'SCALE':
            link_or_set(group, n.inputs[3], b)
        else:
            link_or_set(group, n.inputs[1], b)
    if op in ('DOT_PRODUCT', 'LENGTH', 'DISTANCE'):
        return n.outputs[1]
    return n.outputs[0]

def get_attr(group, name, dtype='INT'):
    n = group.nodes.new("GeometryNodeInputNamedAttribute")
    n.data_type = dtype
    n.inputs["Name"].default_value = name
    return n.outputs[0]

def int_op(group, op, a, b):
    n = group.nodes.new("FunctionNodeIntegerMath")
    n.operation = op
    link_or_set(group, n.inputs[0], a)
    link_or_set(group, n.inputs[1], b)
    return n.outputs[0]

def compare_int_less(group, a, b):
    c = group.nodes.new("FunctionNodeCompare")
    c.data_type = "INT"
    c.operation = "LESS_THAN"
    group.links.new(a, c.inputs["A"])
    group.links.new(b, c.inputs["B"])
    return c.outputs["Result"]

def compare_float_less(group, a, b_val):
    c = group.nodes.new("FunctionNodeCompare")
    c.data_type = "FLOAT"
    c.operation = "LESS_THAN"
    group.links.new(a, c.inputs["A"])
    c.inputs["B"].default_value = float(b_val)
    return c.outputs["Result"]

def bool_and(group, a, b):
    n = group.nodes.new("FunctionNodeBooleanMath")
    n.operation = "AND"
    group.links.new(a, n.inputs[0])
    group.links.new(b, n.inputs[1])
    return n.outputs["Boolean"]

def int_to_float(group, a):
    """Convert integer to float."""
    n = group.nodes.new("ShaderNodeMath")
    n.operation = "ADD"
    link_or_set(group, n.inputs[0], a)
    n.inputs[1].default_value = 0.0
    return n.outputs["Value"]

def switch_node(group, dtype, sw, false_val, true_val):
    """Generic switch for INT, FLOAT, or VECTOR types."""
    n = group.nodes.new("GeometryNodeSwitch")
    n.input_type = dtype
    group.links.new(sw, n.inputs["Switch"])
    link_or_set(group, n.inputs["False"], false_val)
    link_or_set(group, n.inputs["True"], true_val)
    return n.outputs["Output"]

def switch_int(group, sw, false_val, true_val):
    return switch_node(group, "INT", sw, false_val, true_val)

def switch_vec(group,sw, false_val, true_val):
    return switch_node(group, "VECTOR", sw, false_val, true_val)

def switch_float(group, sw, false_val, true_val):
    return switch_node(group, "FLOAT", sw, false_val, true_val)

def clamp01(group, x):
    return math_op(group, "MINIMUM", 1.0, math_op(group, "MAXIMUM", 0.0, x))

def smoother_step(group, t):
    """Quintic smoothstep: t^3 * (6t^2 - 15t + 10) for C2 continuity.
    Matches coon_patch.py's blending function."""
    # s1 = 6*t - 15
    s1 = math_op(group, "SUBTRACT", math_op(group, "MULTIPLY", t, 6.0), 15.0)
    # s2 = t * s1 + 10 = 6t^2 - 15t + 10
    s2 = math_op(group, "ADD", math_op(group, "MULTIPLY", t, s1), 10.0)
    # result = t^3 * s2
    t3 = math_op(group, "POWER", t, 3.0)
    return math_op(group, "MULTIPLY", t3, s2)

# tan(α/2) = sqrt((1 - cos(α)) / (1 + cos(α)))
def tan_half_angle(group, cos_a):
    # Clamp to avoid numerical issues
    cos_clamped = math_op(group, "MINIMUM", 0.9999, math_op(group, "MAXIMUM", -0.9999, cos_a))
    numer = math_op(group, "SUBTRACT", 1.0, cos_clamped)
    denom = math_op(group, "ADD", 1.0, cos_clamped)
    return math_op(group, "SQRT", math_op(group, "DIVIDE", numer, math_op(group, "MAXIMUM", denom, 1e-8)))

def sample_from_orig_corner(group, attr_name, dtype, corner_idx_val, prepared_geo):
    s = create_node(group,"GeometryNodeSampleIndex", {
        "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": dtype, "Index": corner_idx_val
    })
    attr = group.nodes.new("GeometryNodeInputNamedAttribute")
    attr.data_type = dtype
    attr.inputs["Name"].default_value = attr_name
    group.links.new(attr.outputs[0], s.inputs["Value"])
    return s.outputs[0]

def mapped_index(idx):
    """Identity mapping: domain vertex i == mesh corner i (within the face's corner order)."""
    return idx

def corner_for_idx(group,idx,orig_loop_start_field):
    return int_op(group, "ADD", orig_loop_start_field, mapped_index(idx))

def edge_for_idx(group, idx, orig_loop_start_field, prepared_geo):
    cidx = corner_for_idx(group, idx, orig_loop_start_field)
    e = sample_from_orig_corner(group, "corner_edge_idx", "INT", cidx, prepared_geo)
    d = sample_from_orig_corner(group, "edge_is_forward", "BOOLEAN", cidx, prepared_geo)
    return e, d

def edge_control_points(group, edge_id, fwd, orig_geo):
    """Return cubic Bezier control points P0..P3 for edge curve C_i."""
    def edge_vertex_pos(which):
        # which: 0 -> Vertex Index 1, 1 -> Vertex Index 2
        s_edge = create_node(group,"GeometryNodeSampleIndex", {
            "Geometry": orig_geo, "Domain": "EDGE", "Data Type": "INT", "Index": edge_id
        })
        ev = group.nodes.new("GeometryNodeInputMeshEdgeVertices")
        group.links.new(ev.outputs[which], s_edge.inputs["Value"])
        s_pos = create_node(group,"GeometryNodeSampleIndex", {
            "Geometry": orig_geo, "Domain": "POINT", "Data Type": "FLOAT_VECTOR", "Index": s_edge.outputs[0]
        })
        group.links.new(group.nodes.new("GeometryNodeInputPosition").outputs[0], s_pos.inputs["Value"])
        return s_pos.outputs[0]

    def edge_handle_vec(prefix):
        def comp(c):
            s = create_node(group,"GeometryNodeSampleIndex", {
                "Geometry": orig_geo, "Domain": "EDGE", "Data Type": "FLOAT", "Index": edge_id
            })
            attr = group.nodes.new("GeometryNodeInputNamedAttribute")
            attr.data_type = "FLOAT"
            attr.inputs["Name"].default_value = f"{prefix}_{c}"
            group.links.new(attr.outputs[0], s.inputs["Value"])
            return s.outputs[0]
        comb = group.nodes.new("ShaderNodeCombineXYZ")
        group.links.new(comp("x"), comb.inputs[0])
        group.links.new(comp("y"), comb.inputs[1])
        group.links.new(comp("z"), comb.inputs[2])
        return comb.outputs[0]

    p_v1 = edge_vertex_pos(0)
    p_v2 = edge_vertex_pos(1)
    h_start = edge_handle_vec("handle_start")  # relative to v1
    h_end = edge_handle_vec("handle_end")      # relative to v2

    # Endpoint mix
    mix_p0 = group.nodes.new("ShaderNodeMix")
    mix_p0.data_type = "VECTOR"
    group.links.new(fwd, mix_p0.inputs["Factor"])
    group.links.new(p_v2, mix_p0.inputs["A"])
    group.links.new(p_v1, mix_p0.inputs["B"])
    P0 = mix_p0.outputs["Result"]

    mix_p3 = group.nodes.new("ShaderNodeMix")
    mix_p3.data_type = "VECTOR"
    group.links.new(fwd, mix_p3.inputs["Factor"])
    group.links.new(p_v1, mix_p3.inputs["A"])
    group.links.new(p_v2, mix_p3.inputs["B"])
    P3 = mix_p3.outputs["Result"]

    # Handles depend on direction
    p1_fwd = vec_math_op(group, "ADD", p_v1, h_start)
    p1_bwd = vec_math_op(group, "ADD", p_v2, h_end)
    mix_p1 = group.nodes.new("ShaderNodeMix")
    mix_p1.data_type = "VECTOR"
    group.links.new(fwd, mix_p1.inputs["Factor"])
    group.links.new(p1_bwd, mix_p1.inputs["A"])
    group.links.new(p1_fwd, mix_p1.inputs["B"])
    P1 = mix_p1.outputs["Result"]

    p2_fwd = vec_math_op(group, "ADD", p_v2, h_end)
    p2_bwd = vec_math_op(group, "ADD", p_v1, h_start)
    mix_p2 = group.nodes.new("ShaderNodeMix")
    mix_p2.data_type = "VECTOR"
    group.links.new(fwd, mix_p2.inputs["Factor"])
    group.links.new(p2_bwd, mix_p2.inputs["A"])
    group.links.new(p2_fwd, mix_p2.inputs["B"])
    P2 = mix_p2.outputs["Result"]

    return P0, P1, P2, P3



def get_bezier_eval_group():
    """Creates or retrieves a singleton Node Group for Bezier Evaluation."""
    group_name = "Math_BezierEval"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    
    ng = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    ng.interface.new_socket("P0", in_out="INPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P1", in_out="INPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P2", in_out="INPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P3", in_out="INPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("t", in_out="INPUT", socket_type="NodeSocketFloat")
    ng.interface.new_socket("Result", in_out="OUTPUT", socket_type="NodeSocketVector")
    
    # Internal Logic (Your original bezier_eval logic goes here)
    in_node = ng.nodes.new("NodeGroupInput")
    out_node = ng.nodes.new("NodeGroupOutput")
    
    omt = math_op(ng, "SUBTRACT", 1.0, in_node.outputs["t"])
    c0 = math_op(ng,"POWER", omt, 3.0)
    c1 = math_op(ng,"MULTIPLY", math_op(ng,"MULTIPLY", 3.0, math_op(ng,"POWER", omt, 2.0)), in_node.outputs["t"])
    c2 = math_op(ng,"MULTIPLY", math_op(ng,"MULTIPLY", 3.0, omt), math_op(ng,"POWER", in_node.outputs["t"], 2.0))
    c3 = math_op(ng, "POWER", in_node.outputs["t"], 3.0)
    result_vec = vec_math_op(ng, "ADD",
                        vec_math_op(ng, "ADD", vec_math_op(ng, "SCALE", in_node.outputs["P0"], c0), vec_math_op(ng, "SCALE", in_node.outputs["P1"], c1)),
                        vec_math_op(ng, "ADD", vec_math_op(ng, "SCALE", in_node.outputs["P2"], c2), vec_math_op(ng, "SCALE", in_node.outputs["P3"], c3)))
    
    ng.links.new(result_vec, out_node.inputs["Result"])
    return ng

def bezier_eval_node(group, P0, P1, P2, P3, t):
    """Instantiates the Node Group instead of raw math."""
    bg = get_bezier_eval_group()
    n = group.nodes.new("GeometryNodeGroup")
    n.node_tree = bg
    
    link_or_set(group, n.inputs["P0"], P0)
    link_or_set(group, n.inputs["P1"], P1)
    link_or_set(group, n.inputs["P2"], P2)
    link_or_set(group, n.inputs["P3"], P3)
    link_or_set(group, n.inputs["t"], t)
    return n.outputs["Result"]

def bezier_deriv(group, P0, P1, P2, P3, t):
    omt = math_op(group, "SUBTRACT", 1.0, t)
    omt2 = math_op(group, "POWER", omt, 2.0)
    t2 = math_op(group, "POWER", t, 2.0)
    a0 = math_op(group, "MULTIPLY", 3.0, omt2)
    a1 = math_op(group, "MULTIPLY", 6.0, math_op(group, "MULTIPLY", omt, t))
    a2 = math_op(group, "MULTIPLY", 3.0, t2)
    d10 = vec_math_op(group, "SUBTRACT", P1, P0)
    d21 = vec_math_op(group, "SUBTRACT", P2, P1)
    d32 = vec_math_op(group, "SUBTRACT", P3, P2)
    return vec_math_op(group, "ADD",
                        vec_math_op(group, "ADD", vec_math_op(group, "SCALE", d10, a0), vec_math_op(group, "SCALE", d21, a1)),
                        vec_math_op(group, "SCALE", d32, a2))
    
# Sample corner_pos at corners 0, 1, 2, 3 of each face
def sample_face_corner_pos(group, face_idx_node, prepared_geo, sort_index):
    # Get the corner index for this face at the given sort position
    cof_corner = group.nodes.new("GeometryNodeCornersOfFace")
    group.links.new(face_idx_node.outputs[0], cof_corner.inputs["Face Index"])
    cof_corner.inputs["Weights"].default_value = 0.0
    cof_corner.inputs["Sort Index"].default_value = sort_index
    corner_at_sort = cof_corner.outputs["Corner Index"]
    
    # Sample the corner_pos at that corner index
    sample = create_node(group,"GeometryNodeSampleIndex", {
        "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": "FLOAT_VECTOR",
        "Index": corner_at_sort
    })
    # Get the corner_pos attribute from prepared_geo
    corner_pos_attr_w = group.nodes.new("GeometryNodeInputNamedAttribute")
    corner_pos_attr_w.data_type = "FLOAT_VECTOR"
    corner_pos_attr_w.inputs["Name"].default_value = "corner_pos"
    group.links.new(corner_pos_attr_w.outputs[0], sample.inputs["Value"])
    return sample.outputs[0] 

def domain_edge_distance(group, i_idx, N_field, domain_p_x, domain_p_y):
    # Must use the same flip_domain logic as in mean-value coordinates
    # to ensure domain edge positions match the computed domain_p_x/y.
    angle_step_local = math_op(group, "DIVIDE", 6.283185307, N_field)
    
    i_float_local = int_to_float(group, i_idx)
    i_prev = int_op(group, "MODULO", int_op(group, "ADD", int_op(group, "SUBTRACT", i_idx, 1), N_field), N_field)
    i_prev_float = int_to_float(group, i_prev)
    
    # CCW angles (same formula as in mean-value coords)
    base_angle_prev = math_op(group, "MULTIPLY", math_op(group, "ADD", i_prev_float, 0.5), angle_step_local)
    theta0_ccw = math_op(group, "ADD", base_angle_prev, 3.14159265)
    theta0 = theta0_ccw
    
    base_angle_i = math_op(group, "MULTIPLY", math_op(group, "ADD", i_float_local, 0.5), angle_step_local)
    theta1_ccw = math_op(group, "ADD", base_angle_i, 3.14159265)
    theta1 = theta1_ccw

    v0x = math_op(group, "COSINE", theta0)
    v0y = math_op(group, "SINE", theta0)
    v1x = math_op(group, "COSINE", theta1)
    v1y = math_op(group, "SINE", theta1)

    ex = math_op(group, "SUBTRACT", v1x, v0x)
    ey = math_op(group, "SUBTRACT", v1y, v0y)
    elen = math_op(group, "SQRT", math_op(group, "ADD", math_op(group, "MULTIPLY", ex, ex), math_op(group, "MULTIPLY", ey, ey)))

    px = math_op(group, "SUBTRACT", domain_p_x, v0x)
    py = math_op(group, "SUBTRACT", domain_p_y, v0y)
    cross2 = math_op(group, "SUBTRACT", math_op(group, "MULTIPLY", px, ey), math_op(group, "MULTIPLY", py, ex))
    return math_op(group, "DIVIDE", math_op(group, "ABSOLUTE", cross2), elen)