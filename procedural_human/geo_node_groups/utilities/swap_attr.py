import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group

@geo_node_group
def create_swap__attr_group():
    group_name = "Swap Attr"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="ID", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Old", in_out="INPUT", socket_type="NodeSocketString")
    socket.default_value = "ruby"
    socket = group.interface.new_socket(name="New", in_out="INPUT", socket_type="NodeSocketString")
    socket.default_value = "saphire"

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    store_named_attribute_001.inputs[3].default_value = True
    links.new(group_input.outputs[0], store_named_attribute_001.inputs[0])
    links.new(group_input.outputs[3], store_named_attribute_001.inputs[2])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.data_type = "BOOLEAN"
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_001.inputs[2].default_value = 0.0
    random_value_001.inputs[3].default_value = 1.0
    random_value_001.inputs[4].default_value = 0
    random_value_001.inputs[5].default_value = 100
    random_value_001.inputs[6].default_value = 0.5
    random_value_001.inputs[8].default_value = 0
    links.new(group_input.outputs[1], random_value_001.inputs[7])

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.operation = "AND"
    links.new(boolean_math_002.outputs[0], store_named_attribute_001.inputs[1])
    links.new(random_value_001.outputs[3], boolean_math_002.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.data_type = "BOOLEAN"
    links.new(named_attribute.outputs[0], boolean_math_002.inputs[1])
    links.new(group_input.outputs[2], named_attribute.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    store_named_attribute_002.inputs[3].default_value = False
    links.new(store_named_attribute_001.outputs[0], store_named_attribute_002.inputs[0])
    links.new(boolean_math_002.outputs[0], store_named_attribute_002.inputs[1])
    links.new(store_named_attribute_002.outputs[0], group_output.inputs[0])
    links.new(group_input.outputs[2], store_named_attribute_002.inputs[2])

    auto_layout_nodes(group)
    return group
