import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_store_attributes_on_points_group():
    group_name = "StoreAttributesOnPoints"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Curve", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Value", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Value", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (952.5218505859375, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-962.5218505859375, 0.0)
    group_input.bl_label = "Group Input"

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (-396.429443359375, -119.66419982910156)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "COUNT"
    curve_to_points.inputs[1].default_value = 1
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    links.new(group_input.outputs[0], curve_to_points.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (-123.23245239257812, 14.101547241210938)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "FLOAT_VECTOR"
    store_named_attribute.domain = "POINT"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "handle_left"
    links.new(curve_to_points.outputs[0], store_named_attribute.inputs[0])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (-514.1650390625, 97.05918884277344)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    links.new(sample_index.outputs[0], store_named_attribute.inputs[3])
    links.new(group_input.outputs[0], sample_index.inputs[0])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (-745.1072387695312, -20.25994873046875)
    index.bl_label = "Index"
    links.new(index.outputs[0], sample_index.inputs[2])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (-762.5218505859375, 112.67343139648438)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "FLOAT_VECTOR"
    named_attribute.inputs[0].default_value = "handle_left"
    links.new(named_attribute.outputs[0], sample_index.inputs[1])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (162.3988037109375, 252.705078125)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "FLOAT_VECTOR"
    store_named_attribute_001.domain = "POINT"
    store_named_attribute_001.inputs[1].default_value = True
    store_named_attribute_001.inputs[2].default_value = "handle_right"
    links.new(store_named_attribute.outputs[0], store_named_attribute_001.inputs[0])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (-228.5337371826172, 335.6627197265625)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    links.new(index.outputs[0], sample_index_001.inputs[2])
    links.new(sample_index_001.outputs[0], store_named_attribute_001.inputs[3])
    links.new(group_input.outputs[0], sample_index_001.inputs[0])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.label = ""
    named_attribute_001.location = (-476.89056396484375, 351.2769470214844)
    named_attribute_001.bl_label = "Named Attribute"
    named_attribute_001.data_type = "FLOAT_VECTOR"
    named_attribute_001.inputs[0].default_value = "handle_right"
    links.new(named_attribute_001.outputs[0], sample_index_001.inputs[1])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.label = ""
    sample_index_002.location = (243.86834716796875, -129.6185302734375)
    sample_index_002.bl_label = "Sample Index"
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    links.new(index.outputs[0], sample_index_002.inputs[2])
    links.new(group_input.outputs[1], sample_index_002.inputs[1])
    links.new(group_input.outputs[0], sample_index_002.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (454.944580078125, -9.592620849609375)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "FLOAT_VECTOR"
    store_named_attribute_002.domain = "POINT"
    store_named_attribute_002.inputs[1].default_value = True
    store_named_attribute_002.inputs[2].default_value = "handle_start"
    links.new(store_named_attribute_001.outputs[0], store_named_attribute_002.inputs[0])
    links.new(sample_index_002.outputs[0], store_named_attribute_002.inputs[3])

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.name = "Sample Index.003"
    sample_index_003.label = ""
    sample_index_003.location = (370.9483642578125, -351.27691650390625)
    sample_index_003.bl_label = "Sample Index"
    sample_index_003.data_type = "FLOAT_VECTOR"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    links.new(index.outputs[0], sample_index_003.inputs[2])
    links.new(group_input.outputs[0], sample_index_003.inputs[0])
    links.new(group_input.outputs[2], sample_index_003.inputs[1])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (582.0245971679688, -231.2510223388672)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "FLOAT_VECTOR"
    store_named_attribute_003.domain = "POINT"
    store_named_attribute_003.inputs[1].default_value = True
    store_named_attribute_003.inputs[2].default_value = "handle_end"
    links.new(sample_index_003.outputs[0], store_named_attribute_003.inputs[3])
    links.new(store_named_attribute_002.outputs[0], store_named_attribute_003.inputs[0])

    store_attributes_on_points = nodes.new("GeometryNodePointsToVertices")
    store_attributes_on_points.name = "StoreAttributesOnPoints"
    store_attributes_on_points.label = ""
    store_attributes_on_points.location = (762.5218505859375, -222.0064697265625)
    store_attributes_on_points.bl_label = "Points to Vertices"
    store_attributes_on_points.inputs[1].default_value = True
    links.new(store_named_attribute_003.outputs[0], store_attributes_on_points.inputs[0])
    links.new(store_attributes_on_points.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group