import bpy

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
    :param value: Either a NodeSocket to link, or a primitive value to set as default.
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
    :param type_name: The type name of the node to create.
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
    
    for k, v in properties.items():
        if hasattr(node, k):
            setattr(node, k, v)
            
    return node

def math_op(group, op, a, b=None):
    """Create a math operation node.
    
    :param group: The node group to add the node to.
    :param op: The math operation.
    :param a: First operand (socket or value).
    :param b: Optional second operand.
    :returns: The output socket.
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
    :param op: The vector math operation.
    :param a: First operand (socket or value).
    :param b: Optional second operand. For SCALE, this is the scale factor.
    :returns: Value socket for DOT_PRODUCT/LENGTH/DISTANCE, Vector socket otherwise.
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

def mix_color(group, blend_type, factor, a, b):
    """Create a Mix Color node.
    
    In Blender 4.0 ShaderNodeMix, RGBA inputs are at indices 6 (A) and 7 (B).
    """
    n = group.nodes.new("ShaderNodeMix")
    n.data_type = 'RGBA' 
    n.blend_type = blend_type
    link_or_set(group, n.inputs[0], factor)
    link_or_set(group, n.inputs[6], a)
    link_or_set(group, n.inputs[7], b)
    return n.outputs[2]

def mix_shader(group, factor, shader1, shader2):
    """Create a Mix Shader node."""
    n = group.nodes.new("ShaderNodeMixShader")
    link_or_set(group, n.inputs["Fac"], factor)
    link_or_set(group, n.inputs[1], shader1)
    link_or_set(group, n.inputs[2], shader2)
    return n.outputs[0]

def add_shader(group, shader1, shader2):
    """Create an Add Shader node."""
    n = group.nodes.new("ShaderNodeAddShader")
    link_or_set(group, n.inputs[0], shader1)
    link_or_set(group, n.inputs[1], shader2)
    return n.outputs[0]

def fresnel_schlick_factor(group, normal=None):
    """Compute Schlick Fresnel factor: (1 - cos(theta))^5.
    
    Uses Layer Weight Facing output as the base (1 - N.V).
    
    :param group: The node group to add nodes to.
    :param normal: Optional custom normal vector.
    :returns: Output socket with the Fresnel factor for mixing between F0 and F90.
    """
    layer_weight = create_node(group, "ShaderNodeLayerWeight", {"Blend": 0.5})
    if normal is not None:
        link_or_set(group, layer_weight.inputs["Normal"], normal)
    facing = layer_weight.outputs["Facing"]
    return math_op(group, "POWER", facing, 5.0)
