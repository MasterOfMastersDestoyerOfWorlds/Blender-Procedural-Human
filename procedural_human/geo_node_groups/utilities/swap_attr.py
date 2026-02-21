import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes

@geo_node_group
def create_swap__attr_group():
    group_name = "Swap Attr"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

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
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (430.0, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-440.0, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (80.0, 140.0)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001
    links.new(group_input.outputs[0], store_named_attribute_001.inputs[0])
    links.new(group_input.outputs[3], store_named_attribute_001.inputs[2])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.label = ""
    random_value_001.location = (-240.0, 20.0)
    random_value_001.bl_label = "Random Value"
    random_value_001.data_type = "BOOLEAN"
    # Min
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_001.inputs[2].default_value = 0.0
    # Max
    random_value_001.inputs[3].default_value = 1.0
    # Min
    random_value_001.inputs[4].default_value = 0
    # Max
    random_value_001.inputs[5].default_value = 100
    # Probability
    random_value_001.inputs[6].default_value = 0.5
    # Seed
    random_value_001.inputs[8].default_value = 0
    # Links for random_value_001
    links.new(group_input.outputs[1], random_value_001.inputs[7])

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.label = ""
    boolean_math_002.location = (-80.0, 20.0)
    boolean_math_002.bl_label = "Boolean Math"
    boolean_math_002.operation = "AND"
    # Links for boolean_math_002
    links.new(boolean_math_002.outputs[0], store_named_attribute_001.inputs[1])
    links.new(random_value_001.outputs[3], boolean_math_002.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (-240.0, -140.0)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "BOOLEAN"
    # Links for named_attribute
    links.new(named_attribute.outputs[0], boolean_math_002.inputs[1])
    links.new(group_input.outputs[2], named_attribute.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (240.0, 140.0)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    # Value
    store_named_attribute_002.inputs[3].default_value = False
    # Links for store_named_attribute_002
    links.new(store_named_attribute_001.outputs[0], store_named_attribute_002.inputs[0])
    links.new(boolean_math_002.outputs[0], store_named_attribute_002.inputs[1])
    links.new(store_named_attribute_002.outputs[0], group_output.inputs[0])
    links.new(group_input.outputs[2], store_named_attribute_002.inputs[2])

    auto_layout_nodes(group)
    return group
