import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group



@geo_node_group
def create_recreate_curves_from_mesh_group():
    group_name = "RecreateCurvesFromMesh"
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
    group_input.location = (-2083.287109375, 782.2153930664062)
    group_input.bl_label = "Group Input"
    # Links for group_input

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (-166.3363037109375, 1094.60888671875)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    named_attr_start_x = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_start_x.name = "Named Attr Start X"
    named_attr_start_x.label = ""
    named_attr_start_x.location = (-2386.742919921875, 1024.169921875)
    named_attr_start_x.bl_label = "Named Attribute"
    named_attr_start_x.data_type = "FLOAT"
    # Name
    named_attr_start_x.inputs[0].default_value = "handle_start_x"
    # Links for named_attr_start_x

    named_attr_start_y = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_start_y.name = "Named Attr Start Y"
    named_attr_start_y.label = ""
    named_attr_start_y.location = (-2386.742919921875, 874.169921875)
    named_attr_start_y.bl_label = "Named Attribute"
    named_attr_start_y.data_type = "FLOAT"
    # Name
    named_attr_start_y.inputs[0].default_value = "handle_start_y"
    # Links for named_attr_start_y

    named_attr_start_z = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_start_z.name = "Named Attr Start Z"
    named_attr_start_z.label = ""
    named_attr_start_z.location = (-2386.742919921875, 724.169921875)
    named_attr_start_z.bl_label = "Named Attribute"
    named_attr_start_z.data_type = "FLOAT"
    # Name
    named_attr_start_z.inputs[0].default_value = "handle_start_z"
    # Links for named_attr_start_z

    combine_start_offset = nodes.new("ShaderNodeCombineXYZ")
    combine_start_offset.name = "Combine Start Offset"
    combine_start_offset.label = ""
    combine_start_offset.location = (-2136.742919921875, 574.169921875)
    combine_start_offset.bl_label = "Combine XYZ"
    # Links for combine_start_offset
    links.new(named_attr_start_x.outputs[0], combine_start_offset.inputs[0])
    links.new(named_attr_start_y.outputs[0], combine_start_offset.inputs[1])
    links.new(named_attr_start_z.outputs[0], combine_start_offset.inputs[2])

    named_attr_end_x = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_end_x.name = "Named Attr End X"
    named_attr_end_x.label = ""
    named_attr_end_x.location = (-2386.742919921875, 574.169921875)
    named_attr_end_x.bl_label = "Named Attribute"
    named_attr_end_x.data_type = "FLOAT"
    # Name
    named_attr_end_x.inputs[0].default_value = "handle_end_x"
    # Links for named_attr_end_x

    named_attr_end_y = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_end_y.name = "Named Attr End Y"
    named_attr_end_y.label = ""
    named_attr_end_y.location = (-2386.742919921875, 424.169921875)
    named_attr_end_y.bl_label = "Named Attribute"
    named_attr_end_y.data_type = "FLOAT"
    # Name
    named_attr_end_y.inputs[0].default_value = "handle_end_y"
    # Links for named_attr_end_y

    named_attr_end_z = nodes.new("GeometryNodeInputNamedAttribute")
    named_attr_end_z.name = "Named Attr End Z"
    named_attr_end_z.label = ""
    named_attr_end_z.location = (-2386.742919921875, 274.169921875)
    named_attr_end_z.bl_label = "Named Attribute"
    named_attr_end_z.data_type = "FLOAT"
    # Name
    named_attr_end_z.inputs[0].default_value = "handle_end_z"
    # Links for named_attr_end_z

    combine_end_offset = nodes.new("ShaderNodeCombineXYZ")
    combine_end_offset.name = "Combine End Offset"
    combine_end_offset.label = ""
    combine_end_offset.location = (-2136.742919921875, 424.169921875)
    combine_end_offset.bl_label = "Combine XYZ"
    # Links for combine_end_offset
    links.new(named_attr_end_x.outputs[0], combine_end_offset.inputs[0])
    links.new(named_attr_end_y.outputs[0], combine_end_offset.inputs[1])
    links.new(named_attr_end_z.outputs[0], combine_end_offset.inputs[2])

    for_each_geometry_element_input = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input.name = "For Each Geometry Element Input"
    for_each_geometry_element_input.label = ""
    for_each_geometry_element_input.location = (-1770.4730224609375, 976.4089965820312)
    for_each_geometry_element_input.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input.inputs[1].default_value = True
    # Links for for_each_geometry_element_input
    links.new(group_input.outputs[0], for_each_geometry_element_input.inputs[0])

    for_each_geometry_element_output = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.name = "For Each Geometry Element Output"
    for_each_geometry_element_output.label = ""
    for_each_geometry_element_output.location = (-587.4566650390625, 1044.0587158203125)
    for_each_geometry_element_output.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output.active_input_index = 0
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = "EDGE"
    for_each_geometry_element_output.inspection_index = 0
    # Links for for_each_geometry_element_output
    for_each_geometry_element_input.pair_with_output(for_each_geometry_element_output)


    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.label = ""
    curve_line.location = (-1379.283935546875, 1283.69921875)
    curve_line.bl_label = "Curve Line"
    curve_line.mode = "POINTS"
    # Direction
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    # Length
    curve_line.inputs[3].default_value = 1.0
    # Links for curve_line

    edge_vertices_001 = nodes.new("GeometryNodeInputMeshEdgeVertices")
    edge_vertices_001.name = "Edge Vertices.001"
    edge_vertices_001.label = ""
    edge_vertices_001.location = (-2004.4859619140625, 1168.3634033203125)
    edge_vertices_001.bl_label = "Edge Vertices"
    # Links for edge_vertices_001

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.name = "Sample Index.003"
    sample_index_003.label = ""
    sample_index_003.location = (-1553.5643310546875, 1196.6053466796875)
    sample_index_003.bl_label = "Sample Index"
    sample_index_003.data_type = "FLOAT_VECTOR"
    sample_index_003.domain = "EDGE"
    sample_index_003.clamp = False
    # Index
    sample_index_003.inputs[2].default_value = 0
    # Links for sample_index_003
    links.new(for_each_geometry_element_input.outputs[1], sample_index_003.inputs[0])
    links.new(sample_index_003.outputs[0], curve_line.inputs[1])
    links.new(edge_vertices_001.outputs[3], sample_index_003.inputs[1])

    sample_index_004 = nodes.new("GeometryNodeSampleIndex")
    sample_index_004.name = "Sample Index.004"
    sample_index_004.label = ""
    sample_index_004.location = (-1643.486083984375, 1453.2906494140625)
    sample_index_004.bl_label = "Sample Index"
    sample_index_004.data_type = "FLOAT_VECTOR"
    sample_index_004.domain = "EDGE"
    sample_index_004.clamp = False
    # Index
    sample_index_004.inputs[2].default_value = 0
    # Links for sample_index_004
    links.new(for_each_geometry_element_input.outputs[1], sample_index_004.inputs[0])
    links.new(sample_index_004.outputs[0], curve_line.inputs[0])
    links.new(edge_vertices_001.outputs[2], sample_index_004.inputs[1])

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.name = "Sample Index.005"
    sample_index_005.label = ""
    sample_index_005.location = (-1288.8336181640625, 1066.10009765625)
    sample_index_005.bl_label = "Sample Index"
    sample_index_005.data_type = "FLOAT_VECTOR"
    sample_index_005.domain = "EDGE"
    sample_index_005.clamp = False
    # Index
    sample_index_005.inputs[2].default_value = 0
    # Links for sample_index_005
    links.new(for_each_geometry_element_input.outputs[1], sample_index_005.inputs[0])
    links.new(combine_start_offset.outputs[0], sample_index_005.inputs[1])

    set_spline_type_003 = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type_003.name = "Set Spline Type.003"
    set_spline_type_003.label = ""
    set_spline_type_003.location = (-1164.2056884765625, 1216.109130859375)
    set_spline_type_003.bl_label = "Set Spline Type"
    set_spline_type_003.spline_type = "BEZIER"
    # Selection
    set_spline_type_003.inputs[1].default_value = True
    # Links for set_spline_type_003
    links.new(curve_line.outputs[0], set_spline_type_003.inputs[0])

    set_handle_type_001 = nodes.new("GeometryNodeCurveSetHandles")
    set_handle_type_001.name = "Set Handle Type.001"
    set_handle_type_001.label = ""
    set_handle_type_001.location = (-1010.8772583007812, 1244.3740234375)
    set_handle_type_001.bl_label = "Set Handle Type"
    set_handle_type_001.handle_type = "FREE"
    set_handle_type_001.mode = {'LEFT', 'RIGHT'}
    # Selection
    set_handle_type_001.inputs[1].default_value = True
    # Links for set_handle_type_001
    links.new(set_spline_type_003.outputs[0], set_handle_type_001.inputs[0])

    set_handle_positions = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions.name = "Set Handle Positions"
    set_handle_positions.label = ""
    set_handle_positions.location = (-767.9992065429688, 1110.37744140625)
    set_handle_positions.bl_label = "Set Handle Positions"
    set_handle_positions.mode = "RIGHT"
    # Offset
    set_handle_positions.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_handle_positions
    links.new(set_handle_type_001.outputs[0], set_handle_positions.inputs[0])

    endpoint_first_001 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_first_001.name = "Endpoint First.001"
    endpoint_first_001.label = ""
    endpoint_first_001.location = (-993.0531616210938, 953.380859375)
    endpoint_first_001.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_first_001.inputs[0].default_value = 0
    # End Size
    endpoint_first_001.inputs[1].default_value = 1
    # Links for endpoint_first_001

    endpoint_first_002 = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_first_002.name = "Endpoint First.002"
    endpoint_first_002.label = ""
    endpoint_first_002.location = (-1028.62548828125, 1374.5029296875)
    endpoint_first_002.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_first_002.inputs[0].default_value = 1
    # End Size
    endpoint_first_002.inputs[1].default_value = 0
    # Links for endpoint_first_002
    links.new(endpoint_first_002.outputs[0], set_handle_positions.inputs[1])

    sample_index_006 = nodes.new("GeometryNodeSampleIndex")
    sample_index_006.name = "Sample Index.006"
    sample_index_006.label = ""
    sample_index_006.location = (-1147.238037109375, 845.4776000976562)
    sample_index_006.bl_label = "Sample Index"
    sample_index_006.data_type = "FLOAT_VECTOR"
    sample_index_006.domain = "EDGE"
    sample_index_006.clamp = False
    # Index
    sample_index_006.inputs[2].default_value = 0
    # Links for sample_index_006
    links.new(for_each_geometry_element_input.outputs[1], sample_index_006.inputs[0])
    links.new(combine_end_offset.outputs[0], sample_index_006.inputs[1])

    set_handle_positions_001 = nodes.new("GeometryNodeSetCurveHandlePositions")
    set_handle_positions_001.name = "Set Handle Positions.001"
    set_handle_positions_001.label = ""
    set_handle_positions_001.location = (-752.3320922851562, 932.4335327148438)
    set_handle_positions_001.bl_label = "Set Handle Positions"
    set_handle_positions_001.mode = "LEFT"
    # Offset
    set_handle_positions_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_handle_positions_001
    links.new(set_handle_positions.outputs[0], set_handle_positions_001.inputs[0])
    links.new(set_handle_positions_001.outputs[0], for_each_geometry_element_output.inputs[1])
    links.new(endpoint_first_001.outputs[0], set_handle_positions_001.inputs[1])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (-352.2510986328125, 1064.26220703125)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh
    links.new(for_each_geometry_element_output.outputs[2], curve_to_mesh.inputs[0])
    links.new(curve_to_mesh.outputs[0], group_output.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (-1014.80810546875, 1111.758544921875)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "ADD"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(sample_index_004.outputs[0], vector_math.inputs[0])
    links.new(sample_index_005.outputs[0], vector_math.inputs[1])
    links.new(vector_math.outputs[0], set_handle_positions.inputs[2])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (-965.1981201171875, 846.1195678710938)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "ADD"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(sample_index_006.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], set_handle_positions_001.inputs[2])
    links.new(sample_index_003.outputs[0], vector_math_001.inputs[1])

    auto_layout_nodes(group)
    return group