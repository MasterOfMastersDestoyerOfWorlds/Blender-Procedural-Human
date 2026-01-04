import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_geometry__nodes_group():
    group_name = "Geometry Nodes"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-340.0, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1312.0313720703125, 165.38958740234375)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (93.580810546875, 245.31854248046875)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "EDGE"
    sample_index.clamp = False
    # Links for sample_index
    links.new(group_input.outputs[0], sample_index.inputs[0])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (-368.3036804199219, 97.93629455566406)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], sample_index.inputs[2])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (57.69679260253906, 0.19861602783203125)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Selection
    mesh_to_curve.inputs[1].default_value = True
    # Links for mesh_to_curve
    links.new(group_input.outputs[0], mesh_to_curve.inputs[0])

    set_handle_type = nodes.new("GeometryNodeCurveSetHandles")
    set_handle_type.name = "Set Handle Type"
    set_handle_type.label = ""
    set_handle_type.location = (454.1979675292969, 49.76668167114258)
    set_handle_type.bl_label = "Set Handle Type"
    set_handle_type.handle_type = "AUTO"
    set_handle_type.mode = ['LEFT', 'RIGHT']
    # Selection
    set_handle_type.inputs[1].default_value = True
    # Links for set_handle_type

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.label = ""
    set_spline_type.location = (268.021240234375, 12.223613739013672)
    set_spline_type.bl_label = "Set Spline Type"
    set_spline_type.spline_type = "BEZIER"
    # Selection
    set_spline_type.inputs[1].default_value = True
    # Links for set_spline_type
    links.new(set_spline_type.outputs[0], set_handle_type.inputs[0])
    links.new(mesh_to_curve.outputs[0], set_spline_type.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (-501.530517578125, 857.6549072265625)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "FLOAT"
    # Name
    named_attribute.inputs[0].default_value = "handle_start_x"
    # Links for named_attribute

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (-181.70184326171875, 699.489990234375)
    combine_x_y_z.bl_label = "Combine XYZ"
    # Links for combine_x_y_z
    links.new(named_attribute.outputs[0], combine_x_y_z.inputs[0])
    links.new(combine_x_y_z.outputs[0], sample_index.inputs[1])

    named_attribute_001 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.label = ""
    named_attribute_001.location = (-501.530517578125, 857.6549072265625)
    named_attribute_001.bl_label = "Named Attribute"
    named_attribute_001.data_type = "FLOAT"
    # Name
    named_attribute_001.inputs[0].default_value = "handle_start_x"
    # Links for named_attribute_001

    named_attribute_002 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.name = "Named Attribute.002"
    named_attribute_002.label = ""
    named_attribute_002.location = (-511.38116455078125, 717.31005859375)
    named_attribute_002.bl_label = "Named Attribute"
    named_attribute_002.data_type = "FLOAT"
    # Name
    named_attribute_002.inputs[0].default_value = "handle_start_y"
    # Links for named_attribute_002
    links.new(named_attribute_002.outputs[0], combine_x_y_z.inputs[1])

    named_attribute_003 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003.name = "Named Attribute.003"
    named_attribute_003.label = ""
    named_attribute_003.location = (-538.7440795898438, 578.0616455078125)
    named_attribute_003.bl_label = "Named Attribute"
    named_attribute_003.data_type = "FLOAT"
    # Name
    named_attribute_003.inputs[0].default_value = "handle_start_z"
    # Links for named_attribute_003
    links.new(named_attribute_003.outputs[0], combine_x_y_z.inputs[2])

    set_handle_positions = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions.name = "Set Handle Positions"
    set_handle_positions.label = ""
    set_handle_positions.location = (673.8821411132812, 232.444091796875)
    set_handle_positions.bl_label = "Set Handle Positions"
    set_handle_positions.mode = "LEFT"
    # Selection
    set_handle_positions.inputs[1].default_value = True
    # Offset
    set_handle_positions.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_handle_positions
    links.new(set_handle_type.outputs[0], set_handle_positions.inputs[0])
    links.new(sample_index.outputs[0], set_handle_positions.inputs[2])

    named_attribute_004 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_004.name = "Named Attribute.004"
    named_attribute_004.label = ""
    named_attribute_004.location = (-636.0852661132812, 454.7774658203125)
    named_attribute_004.bl_label = "Named Attribute"
    named_attribute_004.data_type = "FLOAT"
    # Name
    named_attribute_004.inputs[0].default_value = "handle_start_x"
    # Links for named_attribute_004

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (-316.256591796875, 296.612548828125)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # Links for combine_x_y_z_001
    links.new(named_attribute_004.outputs[0], combine_x_y_z_001.inputs[0])

    named_attribute_005 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_005.name = "Named Attribute.005"
    named_attribute_005.label = ""
    named_attribute_005.location = (-636.0852661132812, 454.7774658203125)
    named_attribute_005.bl_label = "Named Attribute"
    named_attribute_005.data_type = "FLOAT"
    # Name
    named_attribute_005.inputs[0].default_value = "handle_end_x"
    # Links for named_attribute_005

    named_attribute_006 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_006.name = "Named Attribute.006"
    named_attribute_006.label = ""
    named_attribute_006.location = (-645.9359130859375, 314.4326171875)
    named_attribute_006.bl_label = "Named Attribute"
    named_attribute_006.data_type = "FLOAT"
    # Name
    named_attribute_006.inputs[0].default_value = "handle_end_y"
    # Links for named_attribute_006
    links.new(named_attribute_006.outputs[0], combine_x_y_z_001.inputs[1])

    named_attribute_007 = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_007.name = "Named Attribute.007"
    named_attribute_007.label = ""
    named_attribute_007.location = (-673.298828125, 175.1842041015625)
    named_attribute_007.bl_label = "Named Attribute"
    named_attribute_007.data_type = "FLOAT"
    # Name
    named_attribute_007.inputs[0].default_value = "handle_end_z"
    # Links for named_attribute_007
    links.new(named_attribute_007.outputs[0], combine_x_y_z_001.inputs[2])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (101.05607604980469, 490.9389953613281)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "EDGE"
    sample_index_001.clamp = False
    # Links for sample_index_001
    links.new(group_input.outputs[0], sample_index_001.inputs[0])
    links.new(combine_x_y_z_001.outputs[0], sample_index_001.inputs[1])
    links.new(index.outputs[0], sample_index_001.inputs[2])

    set_handle_positions_001 = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions_001.name = "Set Handle Positions.001"
    set_handle_positions_001.label = ""
    set_handle_positions_001.location = (989.3448486328125, 253.25967407226562)
    set_handle_positions_001.bl_label = "Set Handle Positions"
    set_handle_positions_001.mode = "RIGHT"
    # Selection
    set_handle_positions_001.inputs[1].default_value = True
    # Offset
    set_handle_positions_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_handle_positions_001
    links.new(set_handle_positions_001.outputs[0], group_output.inputs[0])
    links.new(set_handle_positions.outputs[0], set_handle_positions_001.inputs[0])
    links.new(sample_index_001.outputs[0], set_handle_positions_001.inputs[2])

    auto_layout_nodes(group)
    return group