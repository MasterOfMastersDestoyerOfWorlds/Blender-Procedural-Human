import bpy

# --- Helpers ---
def is_socket(obj):
    """Check if an object is a Blender node socket.
    
    :param obj: Object to check.
    :returns: True if obj is a NodeSocket instance, False otherwise.
    """
    return isinstance(obj, bpy.types.NodeSocket) 

def link_or_set(group, socket_in, value):
    """Link a socket to another socket, or set a default value.
    
    If value is a socket, creates a link. Otherwise, sets the default value.
    
    :param group: The node group to create links in.
    :param socket_in: The input socket to link to or set value for.
    :param value: Either a NodeSocket to link, or a primitive value (int, float, bool, str, tuple, list) to set as default.
    """
    if is_socket(value):
        group.links.new(value, socket_in)
    elif isinstance(value, (int, float, bool, str)):
        socket_in.default_value = value 
    elif isinstance(value, (tuple, list)):
        socket_in.default_value = value

def create_node(group, type_name, inputs=None, **properties):
    """Create a new node in the node group and configure it.
    
    :param group: The node group to add the node to.
    :param type_name: The type name of the node to create (e.g., "ShaderNodeMath").
    :param inputs: Optional dictionary of input socket names to values.
    :param properties: Additional properties to set on the node.
    :returns: The created node.
    """
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
    """Create a math operation node.
    
    :param group: The node group to add the node to.
    :param op: The math operation (e.g., "ADD", "SUBTRACT", "MULTIPLY", "DIVIDE", "POWER", "COSINE", "SINE", "SQRT", "ABSOLUTE").
    :param a: First operand (socket or value).
    :param b: Optional second operand (socket or value). Required for binary operations.
    :returns: The output socket of the math node.
    """
    n = group.nodes.new("ShaderNodeMath")
    n.operation = op
    link_or_set(group, n.inputs[0], a)
    if b is not None:
        link_or_set(group, n.inputs[1], b)
    return n.outputs[0]

def vec_math_op(group, op, a, b=None):
    """Create a vector math operation node.
    
    :param group: The node group to add the node to.
    :param op: The vector math operation (e.g., "ADD", "SUBTRACT", "SCALE", "DOT_PRODUCT", "LENGTH", "DISTANCE").
    :param a: First operand (socket or value).
    :param b: Optional second operand (socket or value). For SCALE, this is the scale factor.
    :returns: The output socket. For DOT_PRODUCT, LENGTH, and DISTANCE, returns the scalar output (outputs[1]). Otherwise returns the vector output (outputs[0]).
    """
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
    """Get a named attribute from the geometry.
    
    :param group: The node group to add the node to.
    :param name: The name of the attribute to retrieve.
    :param dtype: The data type of the attribute. Defaults to 'INT'. Options: 'INT', 'FLOAT', 'FLOAT_VECTOR', 'BOOLEAN', etc.
    :returns: The output socket containing the attribute value.
    """
    n = group.nodes.new("GeometryNodeInputNamedAttribute")
    n.data_type = dtype
    n.inputs["Name"].default_value = name
    return n.outputs[0]

def int_op(group, op, a, b):
    """Create an integer math operation node.
    
    :param group: The node group to add the node to.
    :param op: The integer math operation (e.g., "ADD", "SUBTRACT", "MULTIPLY", "DIVIDE", "MODULO").
    :param a: First operand (socket or integer value).
    :param b: Second operand (socket or integer value).
    :returns: The output socket of the integer math node.
    """
    n = group.nodes.new("FunctionNodeIntegerMath")
    n.operation = op
    link_or_set(group, n.inputs[0], a)
    link_or_set(group, n.inputs[1], b)
    return n.outputs[0]

def compare_int_less(group, a, b):
    """Compare two integer values (a < b).
    
    :param group: The node group to add the node to.
    :param a: First integer value (socket or integer).
    :param b: Second integer value (socket or integer).
    :returns: Boolean output socket, True if a < b, False otherwise.
    """
    c = group.nodes.new("FunctionNodeCompare")
    c.data_type = "INT"
    c.operation = "LESS_THAN"
    group.links.new(a, c.inputs["A"])
    group.links.new(b, c.inputs["B"])
    return c.outputs["Result"]

def compare_float_less(group, a, b_val):
    """Compare a float value to a constant (a < b_val).
    
    :param group: The node group to add the node to.
    :param a: Float value to compare (socket or float).
    :param b_val: Constant float value to compare against.
    :returns: Boolean output socket, True if a < b_val, False otherwise.
    """
    c = group.nodes.new("FunctionNodeCompare")
    c.data_type = "FLOAT"
    c.operation = "LESS_THAN"
    group.links.new(a, c.inputs["A"])
    c.inputs["B"].default_value = float(b_val)
    return c.outputs["Result"]

def bool_and(group, a, b):
    """Perform boolean AND operation on two boolean values.
    
    :param group: The node group to add the node to.
    :param a: First boolean value (socket or bool).
    :param b: Second boolean value (socket or bool).
    :returns: Boolean output socket, True if both a and b are True, False otherwise.
    """
    n = group.nodes.new("FunctionNodeBooleanMath")
    n.operation = "AND"
    group.links.new(a, n.inputs[0])
    group.links.new(b, n.inputs[1])
    return n.outputs["Boolean"]

def int_to_float(group, a):
    """Convert integer to float.
    
    :param group: The node group to add the node to.
    :param a: Integer value to convert (socket or integer).
    :returns: Float output socket with the converted value.
    """
    n = group.nodes.new("ShaderNodeMath")
    n.operation = "ADD"
    link_or_set(group, n.inputs[0], a)
    n.inputs[1].default_value = 0.0
    return n.outputs["Value"]

def switch_node(group, dtype, sw, false_val, true_val):
    """Generic switch for INT, FLOAT, or VECTOR types.
    
    :param group: The node group to add the node to.
    :param dtype: The data type for the switch ("INT", "FLOAT", or "VECTOR").
    :param sw: Boolean switch value (socket or bool). If True, returns true_val; if False, returns false_val.
    :param false_val: Value to return when switch is False (socket or value matching dtype).
    :param true_val: Value to return when switch is True (socket or value matching dtype).
    :returns: Output socket with the selected value based on the switch.
    """
    n = group.nodes.new("GeometryNodeSwitch")
    n.input_type = dtype
    group.links.new(sw, n.inputs["Switch"])
    link_or_set(group, n.inputs["False"], false_val)
    link_or_set(group, n.inputs["True"], true_val)
    return n.outputs["Output"]

def switch_int(group, sw, false_val, true_val):
    """Switch node for integer type.
    
    :param group: The node group to add the node to.
    :param sw: Boolean switch value (socket or bool).
    :param false_val: Integer value to return when switch is False (socket or int).
    :param true_val: Integer value to return when switch is True (socket or int).
    :returns: Output socket with the selected integer value.
    """
    return switch_node(group, "INT", sw, false_val, true_val)

def switch_vec(group,sw, false_val, true_val):
    """Switch node for vector type.
    
    :param group: The node group to add the node to.
    :param sw: Boolean switch value (socket or bool).
    :param false_val: Vector value to return when switch is False (socket or tuple/list).
    :param true_val: Vector value to return when switch is True (socket or tuple/list).
    :returns: Output socket with the selected vector value.
    """
    return switch_node(group, "VECTOR", sw, false_val, true_val)

def switch_float(group, sw, false_val, true_val):
    """Switch node for float type.
    
    :param group: The node group to add the node to.
    :param sw: Boolean switch value (socket or bool).
    :param false_val: Float value to return when switch is False (socket or float).
    :param true_val: Float value to return when switch is True (socket or float).
    :returns: Output socket with the selected float value.
    """
    return switch_node(group, "FLOAT", sw, false_val, true_val)

def clamp01(group, x):
    """Clamp a value between 0.0 and 1.0.
    
    :param group: The node group to add the node to.
    :param x: Value to clamp (socket or float).
    :returns: Output socket with the clamped value.
    """
    return math_op(group, "MINIMUM", 1.0, math_op(group, "MAXIMUM", 0.0, x))

def smoother_step(group, t):
    """Quintic smoothstep: t^3 * (6t^2 - 15t + 10) for C2 continuity.
    Matches coon_patch.py's blending function.
    
    :param group: The node group to add the node to.
    :param t: Input parameter (socket or float).
    :returns: Output socket with the smoothstep value.
    """
    # s1 = 6*t - 15
    s1 = math_op(group, "SUBTRACT", math_op(group, "MULTIPLY", t, 6.0), 15.0)
    # s2 = t * s1 + 10 = 6t^2 - 15t + 10
    s2 = math_op(group, "ADD", math_op(group, "MULTIPLY", t, s1), 10.0)
    # result = t^3 * s2
    t3 = math_op(group, "POWER", t, 3.0)
    return math_op(group, "MULTIPLY", t3, s2)

# tan(α/2) = sqrt((1 - cos(α)) / (1 + cos(α)))
def tan_half_angle(group, cos_a):
    """Calculate tan(α/2) from cos(α).
    
    :param group: The node group to add the node to.
    :param cos_a: Cosine of the angle (socket or float). Clamped to avoid numerical issues.
    :returns: Output socket with tan(α/2).
    """
    # Clamp to avoid numerical issues
    cos_clamped = math_op(group, "MINIMUM", 0.9999, math_op(group, "MAXIMUM", -0.9999, cos_a))
    numer = math_op(group, "SUBTRACT", 1.0, cos_clamped)
    denom = math_op(group, "ADD", 1.0, cos_clamped)
    return math_op(group, "SQRT", math_op(group, "DIVIDE", numer, math_op(group, "MAXIMUM", denom, 1e-8)))

def sample_from_orig_corner(group, attr_name, dtype, corner_idx_val, prepared_geo):
    """Sample a named attribute from a corner in the prepared geometry.
    
    :param group: The node group to add the node to.
    :param attr_name: Name of the attribute to sample.
    :param dtype: Data type of the attribute (e.g., "INT", "FLOAT", "FLOAT_VECTOR", "BOOLEAN").
    :param corner_idx_val: Corner index to sample from (socket or int).
    :param prepared_geo: Geometry to sample from (socket or geometry).
    :returns: Output socket with the sampled attribute value.
    """
    s = create_node(group,"GeometryNodeSampleIndex", {
        "Geometry": prepared_geo, "Domain": "CORNER", "Data Type": dtype, "Index": corner_idx_val
    })
    attr = group.nodes.new("GeometryNodeInputNamedAttribute")
    attr.data_type = dtype
    attr.inputs["Name"].default_value = attr_name
    group.links.new(attr.outputs[0], s.inputs["Value"])
    return s.outputs[0]

def mapped_index(idx):
    """Identity mapping: domain vertex i == mesh corner i (within the face's corner order).
    
    :param idx: Index value.
    :returns: The same index value (identity mapping).
    """
    return idx

def corner_for_idx(group,idx,orig_loop_start_field):
    """Calculate the corner index for a given domain index.
    
    :param group: The node group to add the node to.
    :param idx: Domain index (socket or int).
    :param orig_loop_start_field: Original loop start field (socket or int).
    :returns: Output socket with the corner index.
    """
    return int_op(group, "ADD", orig_loop_start_field, mapped_index(idx))

def edge_for_idx(group, idx, orig_loop_start_field, prepared_geo):
    """Get the edge index and forward direction for a given domain index.
    
    :param group: The node group to add the node to.
    :param idx: Domain index (socket or int).
    :param orig_loop_start_field: Original loop start field (socket or int).
    :param prepared_geo: Geometry to sample from (socket or geometry).
    :returns: Tuple of (edge_index, forward_direction) output sockets.
    """
    cidx = corner_for_idx(group, idx, orig_loop_start_field)
    e = sample_from_orig_corner(group, "corner_edge_idx", "INT", cidx, prepared_geo)
    d = sample_from_orig_corner(group, "edge_is_forward", "BOOLEAN", cidx, prepared_geo)
    return e, d

def get_edge_control_points_group():
    """Creates or retrieves a singleton Node Group that calculates cubic Bezier control points for an edge.
    
    The node group samples vertex positions and handle vectors from the geometry, then computes
    the four control points (P0, P1, P2, P3) for a cubic Bezier curve representing the edge.
    The control points are direction-dependent, mixing forward and backward configurations based
    on the edge direction flag.
    
    :returns: The node group for calculating edge control points.
    """
    group_name = "Math_EdgeControlPoints"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    
    ng = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    ng.interface.new_socket("edge_id", in_out="INPUT", socket_type="NodeSocketInt")
    ng.interface.new_socket("fwd", in_out="INPUT", socket_type="NodeSocketBool")
    ng.interface.new_socket("orig_geo", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("P0", in_out="OUTPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P1", in_out="OUTPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P2", in_out="OUTPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P3", in_out="OUTPUT", socket_type="NodeSocketVector")
    
    # Internal Logic
    in_node = ng.nodes.new("NodeGroupInput")
    out_node = ng.nodes.new("NodeGroupOutput")
    
    # Helper function to get vertex position (which: 0 -> Vertex Index 1, 1 -> Vertex Index 2)
    def edge_vertex_pos(which):
        s_edge = create_node(ng, "GeometryNodeSampleIndex", {
            "Geometry": in_node.outputs["orig_geo"], "Domain": "EDGE", "Data Type": "INT", "Index": in_node.outputs["edge_id"]
        })
        ev = ng.nodes.new("GeometryNodeInputMeshEdgeVertices")
        ng.links.new(ev.outputs[which], s_edge.inputs["Value"])
        s_pos = create_node(ng, "GeometryNodeSampleIndex", {
            "Geometry": in_node.outputs["orig_geo"], "Domain": "POINT", "Data Type": "FLOAT_VECTOR", "Index": s_edge.outputs[0]
        })
        ng.links.new(ng.nodes.new("GeometryNodeInputPosition").outputs[0], s_pos.inputs["Value"])
        return s_pos.outputs[0]
    
    # Helper function to get handle vector
    def edge_handle_vec(prefix):
        def comp(c):
            s = create_node(ng, "GeometryNodeSampleIndex", {
                "Geometry": in_node.outputs["orig_geo"], "Domain": "EDGE", "Data Type": "FLOAT", "Index": in_node.outputs["edge_id"]
            })
            attr = ng.nodes.new("GeometryNodeInputNamedAttribute")
            attr.data_type = "FLOAT"
            attr.inputs["Name"].default_value = f"{prefix}_{c}"
            ng.links.new(attr.outputs[0], s.inputs["Value"])
            return s.outputs[0]
        comb = ng.nodes.new("ShaderNodeCombineXYZ")
        ng.links.new(comp("x"), comb.inputs[0])
        ng.links.new(comp("y"), comb.inputs[1])
        ng.links.new(comp("z"), comb.inputs[2])
        return comb.outputs[0]
    
    p_v1 = edge_vertex_pos(0)
    p_v2 = edge_vertex_pos(1)
    h_start = edge_handle_vec("handle_start")  # relative to v1
    h_end = edge_handle_vec("handle_end")      # relative to v2

    # Endpoint mix
    mix_p0 = ng.nodes.new("ShaderNodeMix")
    mix_p0.data_type = "VECTOR"
    ng.links.new(in_node.outputs["fwd"], mix_p0.inputs["Factor"])
    ng.links.new(p_v2, mix_p0.inputs["A"])
    ng.links.new(p_v1, mix_p0.inputs["B"])
    P0 = mix_p0.outputs["Result"]

    mix_p3 = ng.nodes.new("ShaderNodeMix")
    mix_p3.data_type = "VECTOR"
    ng.links.new(in_node.outputs["fwd"], mix_p3.inputs["Factor"])
    ng.links.new(p_v1, mix_p3.inputs["A"])
    ng.links.new(p_v2, mix_p3.inputs["B"])
    P3 = mix_p3.outputs["Result"]

    # Handles depend on direction
    p1_fwd = vec_math_op(ng, "ADD", p_v1, h_start)
    p1_bwd = vec_math_op(ng, "ADD", p_v2, h_end)
    mix_p1 = ng.nodes.new("ShaderNodeMix")
    mix_p1.data_type = "VECTOR"
    ng.links.new(in_node.outputs["fwd"], mix_p1.inputs["Factor"])
    ng.links.new(p1_bwd, mix_p1.inputs["A"])
    ng.links.new(p1_fwd, mix_p1.inputs["B"])
    P1 = mix_p1.outputs["Result"]

    p2_fwd = vec_math_op(ng, "ADD", p_v2, h_end)
    p2_bwd = vec_math_op(ng, "ADD", p_v1, h_start)
    mix_p2 = ng.nodes.new("ShaderNodeMix")
    mix_p2.data_type = "VECTOR"
    ng.links.new(in_node.outputs["fwd"], mix_p2.inputs["Factor"])
    ng.links.new(p2_bwd, mix_p2.inputs["A"])
    ng.links.new(p2_fwd, mix_p2.inputs["B"])
    P2 = mix_p2.outputs["Result"]
    
    ng.links.new(P0, out_node.inputs["P0"])
    ng.links.new(P1, out_node.inputs["P1"])
    ng.links.new(P2, out_node.inputs["P2"])
    ng.links.new(P3, out_node.inputs["P3"])
    return ng

def edge_control_points_node(group, edge_id, fwd, orig_geo):
    """Instantiates the edge control points node group to compute cubic Bezier control points for an edge.
    
    :param group: The node group to add the node to.
    :param edge_id: Edge index (socket or int).
    :param fwd: Forward direction boolean (socket or bool).
    :param orig_geo: Original geometry (socket or geometry).
    :returns: Tuple of (P0, P1, P2, P3) control point output sockets.
    """
    ecp = get_edge_control_points_group()
    n = group.nodes.new("GeometryNodeGroup")
    n.node_tree = ecp
    
    link_or_set(group, n.inputs["edge_id"], edge_id)
    link_or_set(group, n.inputs["fwd"], fwd)
    link_or_set(group, n.inputs["orig_geo"], orig_geo)
    return n.outputs["P0"], n.outputs["P1"], n.outputs["P2"], n.outputs["P3"]



def get_bezier_eval_group():
    """Creates or retrieves a singleton Node Group that evaluates a cubic Bezier curve at parameter t.
    
    The node group implements the standard cubic Bezier evaluation formula:
    B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃
    
    where P₀, P₁, P₂, P₃ are the four control points and t is the parameter in [0, 1].
    
    :returns: The node group for evaluating cubic Bezier curves.
    """
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
    """Instantiates the Bezier evaluation node group to compute a point on a cubic Bezier curve.
    
    :param group: The node group to add the node to.
    :param P0: First control point (socket or vector).
    :param P1: Second control point (socket or vector).
    :param P2: Third control point (socket or vector).
    :param P3: Fourth control point (socket or vector).
    :param t: Parameter value along the curve (socket or float).
    :returns: Output socket with the evaluated point on the Bezier curve.
    """
    bg = get_bezier_eval_group()
    n = group.nodes.new("GeometryNodeGroup")
    n.node_tree = bg
    
    link_or_set(group, n.inputs["P0"], P0)
    link_or_set(group, n.inputs["P1"], P1)
    link_or_set(group, n.inputs["P2"], P2)
    link_or_set(group, n.inputs["P3"], P3)
    link_or_set(group, n.inputs["t"], t)
    return n.outputs["Result"]

def get_bezier_deriv_group():
    """Creates or retrieves a singleton Node Group that calculates the derivative of a cubic Bezier curve at parameter t.
    
    The node group implements the derivative formula for a cubic Bezier curve:
    B'(t) = 3(1-t)²(P₁-P₀) + 6(1-t)t(P₂-P₁) + 3t²(P₃-P₂)
    
    where P₀, P₁, P₂, P₃ are the four control points and t is the parameter in [0, 1].
    The derivative represents the tangent vector (direction and speed) along the curve.
    
    :returns: The node group for calculating Bezier curve derivatives.
    """
    group_name = "Math_BezierDeriv"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    
    ng = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    ng.interface.new_socket("P0", in_out="INPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P1", in_out="INPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P2", in_out="INPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("P3", in_out="INPUT", socket_type="NodeSocketVector")
    ng.interface.new_socket("t", in_out="INPUT", socket_type="NodeSocketFloat")
    ng.interface.new_socket("Result", in_out="OUTPUT", socket_type="NodeSocketVector")
    
    # Internal Logic
    in_node = ng.nodes.new("NodeGroupInput")
    out_node = ng.nodes.new("NodeGroupOutput")
    
    omt = math_op(ng, "SUBTRACT", 1.0, in_node.outputs["t"])
    omt2 = math_op(ng, "POWER", omt, 2.0)
    t2 = math_op(ng, "POWER", in_node.outputs["t"], 2.0)
    a0 = math_op(ng, "MULTIPLY", 3.0, omt2)
    a1 = math_op(ng, "MULTIPLY", 6.0, math_op(ng, "MULTIPLY", omt, in_node.outputs["t"]))
    a2 = math_op(ng, "MULTIPLY", 3.0, t2)
    d10 = vec_math_op(ng, "SUBTRACT", in_node.outputs["P1"], in_node.outputs["P0"])
    d21 = vec_math_op(ng, "SUBTRACT", in_node.outputs["P2"], in_node.outputs["P1"])
    d32 = vec_math_op(ng, "SUBTRACT", in_node.outputs["P3"], in_node.outputs["P2"])
    result = vec_math_op(ng, "ADD",
                        vec_math_op(ng, "ADD", vec_math_op(ng, "SCALE", d10, a0), vec_math_op(ng, "SCALE", d21, a1)),
                        vec_math_op(ng, "SCALE", d32, a2))
    
    ng.links.new(result, out_node.inputs["Result"])
    return ng

def bezier_deriv_node(group, P0, P1, P2, P3, t):
    """Instantiates the Bezier derivative node group to compute the derivative vector at parameter t.
    
    :param group: The node group to add the node to.
    :param P0: First control point (socket or vector).
    :param P1: Second control point (socket or vector).
    :param P2: Third control point (socket or vector).
    :param P3: Fourth control point (socket or vector).
    :param t: Parameter value along the curve (socket or float).
    :returns: Output socket with the derivative vector at parameter t.
    """
    bd = get_bezier_deriv_group()
    n = group.nodes.new("GeometryNodeGroup")
    n.node_tree = bd
    
    link_or_set(group, n.inputs["P0"], P0)
    link_or_set(group, n.inputs["P1"], P1)
    link_or_set(group, n.inputs["P2"], P2)
    link_or_set(group, n.inputs["P3"], P3)
    link_or_set(group, n.inputs["t"], t)
    return n.outputs["Result"]
    
def sample_face_corner_pos(group, face_idx_node, prepared_geo, sort_index):
    """Sample corner position at a specific sort index for a face.
    
    :param group: The node group to add the node to.
    :param face_idx_node: Face index node (socket or int).
    :param prepared_geo: Geometry to sample from (socket or geometry).
    :param sort_index: Sort index of the corner within the face (0, 1, 2, or 3).
    :returns: Output socket with the corner position vector.
    """
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

def get_domain_edge_distance_group():
    """Creates or retrieves a singleton Node Group that calculates the perpendicular distance from a point to an edge in a regular N-sided polygon domain.
    
    The node group computes the distance from a point (domain_p_x, domain_p_y) to edge i_idx
    in a regular N-sided polygon. It uses the same angle calculation as mean-value coordinates
    to ensure domain edge positions match the computed domain coordinates. The distance is
    calculated using the cross product method for point-to-line distance.
    
    :returns: The node group for calculating domain edge distances.
    """
    group_name = "Math_DomainEdgeDistance"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    
    ng = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    ng.interface.new_socket("i_idx", in_out="INPUT", socket_type="NodeSocketInt")
    ng.interface.new_socket("N_field", in_out="INPUT", socket_type="NodeSocketInt")
    ng.interface.new_socket("domain_p_x", in_out="INPUT", socket_type="NodeSocketFloat")
    ng.interface.new_socket("domain_p_y", in_out="INPUT", socket_type="NodeSocketFloat")
    ng.interface.new_socket("Result", in_out="OUTPUT", socket_type="NodeSocketFloat")
    
    # Internal Logic
    in_node = ng.nodes.new("NodeGroupInput")
    out_node = ng.nodes.new("NodeGroupOutput")
    
    # Must use the same flip_domain logic as in mean-value coordinates
    # to ensure domain edge positions match the computed domain_p_x/y.
    angle_step_local = math_op(ng, "DIVIDE", 6.283185307, in_node.outputs["N_field"])
    
    i_float_local = int_to_float(ng, in_node.outputs["i_idx"])
    i_prev = int_op(ng, "MODULO", int_op(ng, "ADD", int_op(ng, "SUBTRACT", in_node.outputs["i_idx"], 1), in_node.outputs["N_field"]), in_node.outputs["N_field"])
    i_prev_float = int_to_float(ng, i_prev)
    
    # CCW angles (same formula as in mean-value coords)
    base_angle_prev = math_op(ng, "MULTIPLY", math_op(ng, "ADD", i_prev_float, 0.5), angle_step_local)
    theta0_ccw = math_op(ng, "ADD", base_angle_prev, 3.14159265)
    theta0 = theta0_ccw
    
    base_angle_i = math_op(ng, "MULTIPLY", math_op(ng, "ADD", i_float_local, 0.5), angle_step_local)
    theta1_ccw = math_op(ng, "ADD", base_angle_i, 3.14159265)
    theta1 = theta1_ccw

    v0x = math_op(ng, "COSINE", theta0)
    v0y = math_op(ng, "SINE", theta0)
    v1x = math_op(ng, "COSINE", theta1)
    v1y = math_op(ng, "SINE", theta1)

    ex = math_op(ng, "SUBTRACT", v1x, v0x)
    ey = math_op(ng, "SUBTRACT", v1y, v0y)
    elen = math_op(ng, "SQRT", math_op(ng, "ADD", math_op(ng, "MULTIPLY", ex, ex), math_op(ng, "MULTIPLY", ey, ey)))

    px = math_op(ng, "SUBTRACT", in_node.outputs["domain_p_x"], v0x)
    py = math_op(ng, "SUBTRACT", in_node.outputs["domain_p_y"], v0y)
    cross2 = math_op(ng, "SUBTRACT", math_op(ng, "MULTIPLY", px, ey), math_op(ng, "MULTIPLY", py, ex))
    result = math_op(ng, "DIVIDE", math_op(ng, "ABSOLUTE", cross2), elen)
    
    ng.links.new(result, out_node.inputs["Result"])
    return ng

def domain_edge_distance_node(group, i_idx, N_field, domain_p_x, domain_p_y):
    """Instantiates the domain edge distance node group to compute the perpendicular distance from a point to an edge.
    
    :param group: The node group to add the node to.
    :param i_idx: Edge index (socket or int).
    :param N_field: Number of edges/vertices in the domain (socket or int).
    :param domain_p_x: X coordinate of the domain point (socket or float).
    :param domain_p_y: Y coordinate of the domain point (socket or float).
    :returns: Output socket with the distance from the point to the edge.
    """
    dg = get_domain_edge_distance_group()
    n = group.nodes.new("GeometryNodeGroup")
    n.node_tree = dg
    
    link_or_set(group, n.inputs["i_idx"], i_idx)
    link_or_set(group, n.inputs["N_field"], N_field)
    link_or_set(group, n.inputs["domain_p_x"], domain_p_x)
    link_or_set(group, n.inputs["domain_p_y"], domain_p_y)
    return n.outputs["Result"]

