import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_loft__splines_group():
    group_name = "Loft Splines"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Splines", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Bezier/Catmull/Poly", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 0
    socket.min_value = 0
    socket.max_value = 2
    socket = group.interface.new_socket(name="Resample Count", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 10
    socket.min_value = 2
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Subdivide", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 2
    socket.min_value = 0
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Resample Splines", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = True
    socket = group.interface.new_socket(name="Cyclic Splines", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False
    socket = group.interface.new_socket(name="Cyclic Loft", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (-1622.518798828125, -123.54595184326172)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "FLOAT_VECTOR"
    store_named_attribute.domain = "CORNER"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "uv_map"
    # Links for store_named_attribute

    math_024 = nodes.new("ShaderNodeMath")
    math_024.name = "Math.024"
    math_024.label = ""
    math_024.location = (-2447.518798828125, -43.54595184326172)
    math_024.bl_label = "Math"
    math_024.operation = "MULTIPLY"
    math_024.use_clamp = False
    # Value
    math_024.inputs[2].default_value = 0.5
    # Links for math_024

    math_026 = nodes.new("ShaderNodeMath")
    math_026.name = "Math.026"
    math_026.label = ""
    math_026.location = (-2627.518798828125, -43.54595184326172)
    math_026.bl_label = "Math"
    math_026.operation = "MODULO"
    math_026.use_clamp = False
    # Value
    math_026.inputs[2].default_value = 0.5
    # Links for math_026
    links.new(math_026.outputs[0], math_024.inputs[0])

    duplicate_elements_001 = nodes.new("GeometryNodeDuplicateElements")
    duplicate_elements_001.name = "Duplicate Elements.001"
    duplicate_elements_001.label = ""
    duplicate_elements_001.location = (-2447.518798828125, 156.45404052734375)
    duplicate_elements_001.bl_label = "Duplicate Elements"
    duplicate_elements_001.domain = "SPLINE"
    # Selection
    duplicate_elements_001.inputs[1].default_value = True
    # Links for duplicate_elements_001

    resample_curve_003 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.name = "Resample Curve.003"
    resample_curve_003.label = ""
    resample_curve_003.location = (-2627.518798828125, 156.45404052734375)
    resample_curve_003.bl_label = "Resample Curve"
    resample_curve_003.keep_last_segment = False
    # Selection
    resample_curve_003.inputs[1].default_value = True
    # Mode
    resample_curve_003.inputs[2].default_value = "Count"
    # Length
    resample_curve_003.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_003
    links.new(resample_curve_003.outputs[0], duplicate_elements_001.inputs[0])

    math_025 = nodes.new("ShaderNodeMath")
    math_025.name = "Math.025"
    math_025.label = ""
    math_025.location = (-2267.518798828125, -43.54595184326172)
    math_025.bl_label = "Math"
    math_025.operation = "ADD"
    math_025.use_clamp = False
    # Value
    math_025.inputs[2].default_value = 0.5
    # Links for math_025
    links.new(math_024.outputs[0], math_025.inputs[0])
    links.new(duplicate_elements_001.outputs[1], math_025.inputs[1])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    set_position_003.label = ""
    set_position_003.location = (-1887.518798828125, 176.45404052734375)
    set_position_003.bl_label = "Set Position"
    # Selection
    set_position_003.inputs[1].default_value = True
    # Offset
    set_position_003.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_003
    links.new(duplicate_elements_001.outputs[0], set_position_003.inputs[0])

    switch_011 = nodes.new("GeometryNodeSwitch")
    switch_011.name = "Switch.011"
    switch_011.label = ""
    switch_011.location = (-1847.518798828125, -123.54595184326172)
    switch_011.bl_label = "Switch"
    switch_011.input_type = "INT"
    # Links for switch_011

    math_027 = nodes.new("ShaderNodeMath")
    math_027.name = "Math.027"
    math_027.label = ""
    math_027.location = (-2027.518798828125, -243.54595947265625)
    math_027.bl_label = "Math"
    math_027.operation = "ADD"
    math_027.use_clamp = False
    # Value
    math_027.inputs[1].default_value = 1.0
    # Value
    math_027.inputs[2].default_value = 0.5
    # Links for math_027
    links.new(math_027.outputs[0], switch_011.inputs[2])

    math_020 = nodes.new("ShaderNodeMath")
    math_020.name = "Math.020"
    math_020.label = ""
    math_020.location = (-2207.518798828125, -543.5459594726562)
    math_020.bl_label = "Math"
    math_020.operation = "SUBTRACT"
    math_020.use_clamp = False
    # Value
    math_020.inputs[2].default_value = 0.5
    # Links for math_020

    math_021 = nodes.new("ShaderNodeMath")
    math_021.name = "Math.021"
    math_021.label = ""
    math_021.location = (-2207.518798828125, -383.54595947265625)
    math_021.bl_label = "Math"
    math_021.operation = "ADD"
    math_021.use_clamp = False
    # Value
    math_021.inputs[1].default_value = 1.0
    # Value
    math_021.inputs[2].default_value = 0.5
    # Links for math_021

    math_022 = nodes.new("ShaderNodeMath")
    math_022.name = "Math.022"
    math_022.label = ""
    math_022.location = (-2027.518798828125, -443.54595947265625)
    math_022.bl_label = "Math"
    math_022.operation = "MULTIPLY"
    math_022.use_clamp = False
    # Value
    math_022.inputs[2].default_value = 0.5
    # Links for math_022
    links.new(math_021.outputs[0], math_022.inputs[0])
    links.new(math_020.outputs[0], math_022.inputs[1])

    math_023 = nodes.new("ShaderNodeMath")
    math_023.name = "Math.023"
    math_023.label = ""
    math_023.location = (-1847.518798828125, -443.54595947265625)
    math_023.bl_label = "Math"
    math_023.operation = "ADD"
    math_023.use_clamp = False
    # Value
    math_023.inputs[1].default_value = 1.0
    # Value
    math_023.inputs[2].default_value = 0.5
    # Links for math_023
    links.new(math_022.outputs[0], math_023.inputs[0])

    switch_003 = nodes.new("GeometryNodeSwitch")
    switch_003.name = "Switch.003"
    switch_003.label = ""
    switch_003.location = (-2387.518798828125, -543.5459594726562)
    switch_003.bl_label = "Switch"
    switch_003.input_type = "FLOAT"
    # False
    switch_003.inputs[1].default_value = 1.0
    # True
    switch_003.inputs[2].default_value = 0.0
    # Links for switch_003
    links.new(switch_003.outputs[0], math_020.inputs[1])

    grid_001 = nodes.new("GeometryNodeMeshGrid")
    grid_001.name = "Grid.001"
    grid_001.label = ""
    grid_001.location = (-1673.7686767578125, -261.3111877441406)
    grid_001.bl_label = "Grid"
    # Size X
    grid_001.inputs[0].default_value = 1.0
    # Size Y
    grid_001.inputs[1].default_value = 1.0
    # Links for grid_001
    links.new(math_023.outputs[0], grid_001.inputs[3])
    links.new(switch_011.outputs[0], grid_001.inputs[2])
    links.new(grid_001.outputs[0], store_named_attribute.inputs[0])
    links.new(grid_001.outputs[1], store_named_attribute.inputs[3])

    math_028 = nodes.new("ShaderNodeMath")
    math_028.name = "Math.028"
    math_028.label = ""
    math_028.location = (-1507.518798828125, -363.54595947265625)
    math_028.bl_label = "Math"
    math_028.operation = "DIVIDE"
    math_028.use_clamp = False
    # Value
    math_028.inputs[2].default_value = 0.5
    # Links for math_028
    links.new(math_023.outputs[0], math_028.inputs[1])

    math_029 = nodes.new("ShaderNodeMath")
    math_029.name = "Math.029"
    math_029.label = ""
    math_029.location = (-1507.518798828125, -523.5459594726562)
    math_029.bl_label = "Math"
    math_029.operation = "MODULO"
    math_029.use_clamp = False
    # Value
    math_029.inputs[2].default_value = 0.5
    # Links for math_029
    links.new(math_023.outputs[0], math_029.inputs[1])

    math_031 = nodes.new("ShaderNodeMath")
    math_031.name = "Math.031"
    math_031.label = ""
    math_031.location = (-1327.518798828125, -363.54595947265625)
    math_031.bl_label = "Math"
    math_031.operation = "FLOOR"
    math_031.use_clamp = False
    # Value
    math_031.inputs[1].default_value = 0.5
    # Value
    math_031.inputs[2].default_value = 0.5
    # Links for math_031
    links.new(math_028.outputs[0], math_031.inputs[0])

    math_032 = nodes.new("ShaderNodeMath")
    math_032.name = "Math.032"
    math_032.label = ""
    math_032.location = (-1147.518798828125, -363.54595947265625)
    math_032.bl_label = "Math"
    math_032.operation = "SUBTRACT"
    math_032.use_clamp = False
    # Value
    math_032.inputs[2].default_value = 0.5
    # Links for math_032
    links.new(math_031.outputs[0], math_032.inputs[1])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (-1327.518798828125, -523.5459594726562)
    compare_003.bl_label = "Compare"
    compare_003.operation = "EQUAL"
    compare_003.data_type = "INT"
    compare_003.mode = "ELEMENT"
    # A
    compare_003.inputs[0].default_value = 0.0
    # B
    compare_003.inputs[1].default_value = 0.0
    # A
    compare_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_003.inputs[6].default_value = [0.0, 0.0, 0.0, 0.0]
    # B
    compare_003.inputs[7].default_value = [0.0, 0.0, 0.0, 0.0]
    # A
    compare_003.inputs[8].default_value = ""
    # B
    compare_003.inputs[9].default_value = ""
    # C
    compare_003.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_003.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_003.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_003
    links.new(math_029.outputs[0], compare_003.inputs[2])

    math_033 = nodes.new("ShaderNodeMath")
    math_033.name = "Math.033"
    math_033.label = ""
    math_033.location = (-1147.518798828125, -523.5459594726562)
    math_033.bl_label = "Math"
    math_033.operation = "MULTIPLY"
    math_033.use_clamp = False
    # Value
    math_033.inputs[2].default_value = 0.5
    # Links for math_033
    links.new(math_031.outputs[0], math_033.inputs[0])

    switch_012 = nodes.new("GeometryNodeSwitch")
    switch_012.name = "Switch.012"
    switch_012.label = ""
    switch_012.location = (-967.518798828125, -363.54595947265625)
    switch_012.bl_label = "Switch"
    switch_012.input_type = "FLOAT"
    # Links for switch_012
    links.new(math_032.outputs[0], switch_012.inputs[1])
    links.new(math_033.outputs[0], switch_012.inputs[2])
    links.new(compare_003.outputs[0], switch_012.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (-2267.518798828125, 56.45404815673828)
    position_002.bl_label = "Position"
    # Links for position_002

    math_030 = nodes.new("ShaderNodeMath")
    math_030.name = "Math.030"
    math_030.label = ""
    math_030.location = (-1507.518798828125, -683.5459594726562)
    math_030.bl_label = "Math"
    math_030.operation = "SUBTRACT"
    math_030.use_clamp = False
    # Value
    math_030.inputs[1].default_value = 1.0
    # Value
    math_030.inputs[2].default_value = 0.5
    # Links for math_030
    links.new(math_023.outputs[0], math_030.inputs[0])
    links.new(math_030.outputs[0], compare_003.inputs[3])
    links.new(math_030.outputs[0], math_033.inputs[1])

    math_034 = nodes.new("ShaderNodeMath")
    math_034.name = "Math.034"
    math_034.label = ""
    math_034.location = (-1572.31591796875, -813.1153564453125)
    math_034.bl_label = "Math"
    math_034.operation = "MULTIPLY"
    math_034.use_clamp = False
    # Value
    math_034.inputs[2].default_value = 0.5
    # Links for math_034
    links.new(math_023.outputs[0], math_034.inputs[1])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (-1147.518798828125, -703.5459594726562)
    compare_004.bl_label = "Compare"
    compare_004.operation = "GREATER_EQUAL"
    compare_004.data_type = "INT"
    compare_004.mode = "ELEMENT"
    # A
    compare_004.inputs[0].default_value = 0.0
    # B
    compare_004.inputs[1].default_value = 0.0
    # A
    compare_004.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_004.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_004.inputs[6].default_value = [0.0, 0.0, 0.0, 0.0]
    # B
    compare_004.inputs[7].default_value = [0.0, 0.0, 0.0, 0.0]
    # A
    compare_004.inputs[8].default_value = ""
    # B
    compare_004.inputs[9].default_value = ""
    # C
    compare_004.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_004.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_004.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_004
    links.new(math_034.outputs[0], compare_004.inputs[3])

    math_035 = nodes.new("ShaderNodeMath")
    math_035.name = "Math.035"
    math_035.label = ""
    math_035.location = (-1147.518798828125, -883.5459594726562)
    math_035.bl_label = "Math"
    math_035.operation = "MODULO"
    math_035.use_clamp = False
    # Value
    math_035.inputs[2].default_value = 0.5
    # Links for math_035
    links.new(math_023.outputs[0], math_035.inputs[1])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.label = ""
    boolean_math_001.location = (-187.518798828125, -83.54595184326172)
    boolean_math_001.bl_label = "Boolean Math"
    boolean_math_001.operation = "AND"
    # Links for boolean_math_001

    switch_017 = nodes.new("GeometryNodeSwitch")
    switch_017.name = "Switch.017"
    switch_017.label = ""
    switch_017.location = (-55.6870002746582, 85.83245086669922)
    switch_017.bl_label = "Switch"
    switch_017.input_type = "INT"
    # Links for switch_017
    links.new(boolean_math_001.outputs[0], switch_017.inputs[0])

    switch_014 = nodes.new("GeometryNodeSwitch")
    switch_014.name = "Switch.014"
    switch_014.label = ""
    switch_014.location = (-367.518798828125, -83.54595184326172)
    switch_014.bl_label = "Switch"
    switch_014.input_type = "INT"
    # Links for switch_014
    links.new(switch_014.outputs[0], switch_017.inputs[1])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (-367.518798828125, -263.54595947265625)
    compare_005.bl_label = "Compare"
    compare_005.operation = "EQUAL"
    compare_005.data_type = "INT"
    compare_005.mode = "ELEMENT"
    # A
    compare_005.inputs[0].default_value = 0.0
    # B
    compare_005.inputs[1].default_value = 0.0
    # A
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_005.inputs[6].default_value = [0.0, 0.0, 0.0, 0.0]
    # B
    compare_005.inputs[7].default_value = [0.0, 0.0, 0.0, 0.0]
    # A
    compare_005.inputs[8].default_value = ""
    # B
    compare_005.inputs[9].default_value = ""
    # C
    compare_005.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_005.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_005.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_005

    switch_015 = nodes.new("GeometryNodeSwitch")
    switch_015.name = "Switch.015"
    switch_015.label = ""
    switch_015.location = (-187.518798828125, -243.54595947265625)
    switch_015.bl_label = "Switch"
    switch_015.input_type = "INT"
    # True
    switch_015.inputs[2].default_value = 0
    # Links for switch_015
    links.new(switch_014.outputs[0], switch_015.inputs[1])
    links.new(compare_005.outputs[0], switch_015.inputs[0])
    links.new(switch_015.outputs[0], switch_017.inputs[2])

    math_036 = nodes.new("ShaderNodeMath")
    math_036.name = "Math.036"
    math_036.label = ""
    math_036.location = (-547.518798828125, -423.54595947265625)
    math_036.bl_label = "Math"
    math_036.operation = "SUBTRACT"
    math_036.use_clamp = False
    # Value
    math_036.inputs[1].default_value = 1.0
    # Value
    math_036.inputs[2].default_value = 0.5
    # Links for math_036
    links.new(math_036.outputs[0], compare_005.inputs[3])

    math_037 = nodes.new("ShaderNodeMath")
    math_037.name = "Math.037"
    math_037.label = ""
    math_037.location = (-727.518798828125, -423.54595947265625)
    math_037.bl_label = "Math"
    math_037.operation = "MULTIPLY"
    math_037.use_clamp = False
    # Value
    math_037.inputs[2].default_value = 0.5
    # Links for math_037
    links.new(switch_011.outputs[0], math_037.inputs[0])
    links.new(math_023.outputs[0], math_037.inputs[1])
    links.new(math_037.outputs[0], math_036.inputs[0])

    switch_016 = nodes.new("GeometryNodeSwitch")
    switch_016.name = "Switch.016"
    switch_016.label = ""
    switch_016.location = (-730.2539672851562, -163.54595947265625)
    switch_016.bl_label = "Switch"
    switch_016.input_type = "INT"
    # Links for switch_016
    links.new(switch_012.outputs[0], switch_016.inputs[2])
    links.new(switch_016.outputs[0], switch_014.inputs[1])

    switch_013 = nodes.new("GeometryNodeSwitch")
    switch_013.name = "Switch.013"
    switch_013.label = ""
    switch_013.location = (-547.518798828125, -163.54595947265625)
    switch_013.bl_label = "Switch"
    switch_013.input_type = "INT"
    # Links for switch_013
    links.new(switch_016.outputs[0], switch_013.inputs[1])
    links.new(compare_004.outputs[0], switch_013.inputs[0])
    links.new(math_035.outputs[0], switch_013.inputs[2])
    links.new(switch_013.outputs[0], switch_014.inputs[2])

    set_spline_cyclic_002 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_002.name = "Set Spline Cyclic.002"
    set_spline_cyclic_002.label = ""
    set_spline_cyclic_002.location = (-1647.518798828125, 176.45404052734375)
    set_spline_cyclic_002.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic_002.inputs[1].default_value = True
    # Links for set_spline_cyclic_002
    links.new(set_position_003.outputs[0], set_spline_cyclic_002.inputs[0])

    math_019 = nodes.new("ShaderNodeMath")
    math_019.name = "Math.019"
    math_019.label = ""
    math_019.location = (-1647.518798828125, 356.45404052734375)
    math_019.bl_label = "Math"
    math_019.operation = "ADD"
    math_019.use_clamp = False
    # Value
    math_019.inputs[1].default_value = 1.0
    # Value
    math_019.inputs[2].default_value = 0.5
    # Links for math_019

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (372.481201171875, -103.54595184326172)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    # A
    compare.inputs[0].default_value = 0.0
    # B
    compare.inputs[1].default_value = 0.0
    # B
    compare.inputs[3].default_value = 1
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.0, 0.0, 0.0, 0.0]
    # B
    compare.inputs[7].default_value = [0.0, 0.0, 0.0, 0.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513
    # Links for compare

    edge_neighbors = nodes.new("GeometryNodeInputMeshEdgeNeighbors")
    edge_neighbors.name = "Edge Neighbors"
    edge_neighbors.label = ""
    edge_neighbors.location = (192.481201171875, -183.54595947265625)
    edge_neighbors.bl_label = "Edge Neighbors"
    # Links for edge_neighbors
    links.new(edge_neighbors.outputs[0], compare.inputs[2])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (372.481201171875, 136.45404052734375)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Offset
    set_position_002.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_002
    links.new(store_named_attribute.outputs[0], set_position_002.inputs[0])

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.label = ""
    merge_by_distance.location = (572.481201171875, -23.54595184326172)
    merge_by_distance.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance.inputs[2].default_value = "All"
    # Distance
    merge_by_distance.inputs[3].default_value = 9.999999747378752e-06
    # Links for merge_by_distance
    links.new(set_position_002.outputs[0], merge_by_distance.inputs[0])
    links.new(compare.outputs[0], merge_by_distance.inputs[1])

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (972.481201171875, 116.45404815673828)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (372.481201171875, -283.54595947265625)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "OR"
    # Links for boolean_math

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (772.481201171875, 116.45404815673828)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(boolean_math.outputs[0], switch.inputs[0])
    links.new(merge_by_distance.outputs[0], switch.inputs[2])
    links.new(set_position_002.outputs[0], switch.inputs[1])
    links.new(switch.outputs[0], group_output.inputs[0])

    switch_010 = nodes.new("GeometryNodeSwitch")
    switch_010.name = "Switch.010"
    switch_010.label = ""
    switch_010.location = (-687.518798828125, 456.45404052734375)
    switch_010.bl_label = "Switch"
    switch_010.input_type = "GEOMETRY"
    # Links for switch_010

    resample_curve_006 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_006.name = "Resample Curve.006"
    resample_curve_006.label = ""
    resample_curve_006.location = (-1067.518798828125, 276.45404052734375)
    resample_curve_006.bl_label = "Resample Curve"
    resample_curve_006.keep_last_segment = False
    # Selection
    resample_curve_006.inputs[1].default_value = True
    # Mode
    resample_curve_006.inputs[2].default_value = "Evaluated"
    # Count
    resample_curve_006.inputs[3].default_value = 10
    # Length
    resample_curve_006.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_006
    links.new(resample_curve_006.outputs[0], switch_010.inputs[2])

    set_spline_type_002 = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type_002.name = "Set Spline Type.002"
    set_spline_type_002.label = ""
    set_spline_type_002.location = (-1247.518798828125, 276.45404052734375)
    set_spline_type_002.bl_label = "Set Spline Type"
    set_spline_type_002.spline_type = "CATMULL_ROM"
    # Selection
    set_spline_type_002.inputs[1].default_value = True
    # Links for set_spline_type_002
    links.new(set_spline_type_002.outputs[0], resample_curve_006.inputs[0])

    set_spline_type_001 = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type_001.name = "Set Spline Type.001"
    set_spline_type_001.label = ""
    set_spline_type_001.location = (-1247.518798828125, 456.45404052734375)
    set_spline_type_001.bl_label = "Set Spline Type"
    set_spline_type_001.spline_type = "BEZIER"
    # Selection
    set_spline_type_001.inputs[1].default_value = True
    # Links for set_spline_type_001

    set_handle_type_001 = nodes.new("GeometryNodeCurveSetHandles")
    set_handle_type_001.name = "Set Handle Type.001"
    set_handle_type_001.label = ""
    set_handle_type_001.location = (-1067.518798828125, 456.45404052734375)
    set_handle_type_001.bl_label = "Set Handle Type"
    set_handle_type_001.handle_type = "AUTO"
    set_handle_type_001.mode = ['RIGHT', 'LEFT']
    # Selection
    set_handle_type_001.inputs[1].default_value = True
    # Links for set_handle_type_001
    links.new(set_spline_type_001.outputs[0], set_handle_type_001.inputs[0])

    resample_curve_005 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_005.name = "Resample Curve.005"
    resample_curve_005.label = ""
    resample_curve_005.location = (-887.518798828125, 456.45404052734375)
    resample_curve_005.bl_label = "Resample Curve"
    resample_curve_005.keep_last_segment = False
    # Selection
    resample_curve_005.inputs[1].default_value = True
    # Mode
    resample_curve_005.inputs[2].default_value = "Evaluated"
    # Count
    resample_curve_005.inputs[3].default_value = 10
    # Length
    resample_curve_005.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_005
    links.new(set_handle_type_001.outputs[0], resample_curve_005.inputs[0])
    links.new(resample_curve_005.outputs[0], switch_010.inputs[1])

    set_spline_resolution_001 = nodes.new("GeometryNodeSetSplineResolution")
    set_spline_resolution_001.name = "Set Spline Resolution.001"
    set_spline_resolution_001.label = ""
    set_spline_resolution_001.location = (-1427.518798828125, 296.45404052734375)
    set_spline_resolution_001.bl_label = "Set Spline Resolution"
    # Selection
    set_spline_resolution_001.inputs[1].default_value = True
    # Links for set_spline_resolution_001
    links.new(set_spline_cyclic_002.outputs[0], set_spline_resolution_001.inputs[0])
    links.new(set_spline_resolution_001.outputs[0], set_spline_type_001.inputs[0])
    links.new(math_019.outputs[0], set_spline_resolution_001.inputs[2])
    links.new(set_spline_resolution_001.outputs[0], set_spline_type_002.inputs[0])

    subdivide_curve_001 = nodes.new("GeometryNodeSubdivideCurve")
    subdivide_curve_001.name = "Subdivide Curve.001"
    subdivide_curve_001.label = ""
    subdivide_curve_001.location = (-1427.518798828125, 136.45404052734375)
    subdivide_curve_001.bl_label = "Subdivide Curve"
    # Links for subdivide_curve_001
    links.new(set_spline_cyclic_002.outputs[0], subdivide_curve_001.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-687.518798828125, 276.45404052734375)
    math.bl_label = "Math"
    math.operation = "SUBTRACT"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 1.0
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math

    switch_018 = nodes.new("GeometryNodeSwitch")
    switch_018.name = "Switch.018"
    switch_018.label = ""
    switch_018.location = (-447.518798828125, 316.45404052734375)
    switch_018.bl_label = "Switch"
    switch_018.input_type = "GEOMETRY"
    # Links for switch_018
    links.new(switch_010.outputs[0], switch_018.inputs[1])
    links.new(subdivide_curve_001.outputs[0], switch_018.inputs[2])
    links.new(math.outputs[0], switch_018.inputs[0])

    index_006 = nodes.new("GeometryNodeInputIndex")
    index_006.name = "Index.006"
    index_006.label = ""
    index_006.location = (-3039.521728515625, -216.7563934326172)
    index_006.bl_label = "Index"
    # Links for index_006
    links.new(index_006.outputs[0], math_026.inputs[0])
    links.new(index_006.outputs[0], math_028.inputs[0])
    links.new(index_006.outputs[0], math_032.inputs[0])
    links.new(index_006.outputs[0], math_029.inputs[0])
    links.new(index_006.outputs[0], compare_004.inputs[2])
    links.new(index_006.outputs[0], math_035.inputs[0])
    links.new(index_006.outputs[0], switch_016.inputs[1])
    links.new(index_006.outputs[0], compare_005.inputs[2])

    switch_002 = nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.label = ""
    switch_002.location = (-2764.609619140625, 422.72320556640625)
    switch_002.bl_label = "Switch"
    switch_002.input_type = "INT"
    # Links for switch_002
    links.new(switch_002.outputs[0], math_024.inputs[1])
    links.new(switch_002.outputs[0], duplicate_elements_001.inputs[2])
    links.new(switch_002.outputs[0], switch_011.inputs[1])
    links.new(switch_002.outputs[0], math_027.inputs[0])
    links.new(switch_002.outputs[0], math_034.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-3027.518798828125, 236.45404052734375)
    math_001.bl_label = "Math"
    math_001.operation = "DIVIDE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math_001.outputs[0], switch_002.inputs[1])

    domain_size_001 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_001.name = "Domain Size.001"
    domain_size_001.label = ""
    domain_size_001.location = (-3243.416015625, 113.71483612060547)
    domain_size_001.bl_label = "Domain Size"
    domain_size_001.component = "CURVE"
    # Links for domain_size_001
    links.new(domain_size_001.outputs[4], resample_curve_003.inputs[3])
    links.new(domain_size_001.outputs[4], math_026.inputs[1])
    links.new(domain_size_001.outputs[4], math_020.inputs[0])
    links.new(domain_size_001.outputs[0], math_001.inputs[0])
    links.new(domain_size_001.outputs[4], math_001.inputs[1])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (-3449.39990234375, 156.17262268066406)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Links for switch_001
    links.new(switch_001.outputs[0], domain_size_001.inputs[0])

    resample_curve_004 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_004.name = "Resample Curve.004"
    resample_curve_004.label = ""
    resample_curve_004.location = (-3636.158447265625, 246.63818359375)
    resample_curve_004.bl_label = "Resample Curve"
    resample_curve_004.keep_last_segment = False
    # Selection
    resample_curve_004.inputs[1].default_value = True
    # Mode
    resample_curve_004.inputs[2].default_value = "Count"
    # Length
    resample_curve_004.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_004
    links.new(resample_curve_004.outputs[0], switch_001.inputs[2])

    curve_line_001 = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line_001.name = "Curve Line.001"
    curve_line_001.label = ""
    curve_line_001.location = (-3627.518798828125, 36.45404815673828)
    curve_line_001.bl_label = "Curve Line"
    curve_line_001.mode = "POINTS"
    # Start
    curve_line_001.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    # End
    curve_line_001.inputs[1].default_value = Vector((0.0, 0.0, 1.0))
    # Direction
    curve_line_001.inputs[2].default_value = [0.0, 0.0, 1.0]
    # Length
    curve_line_001.inputs[3].default_value = 1.0
    # Links for curve_line_001
    links.new(curve_line_001.outputs[0], resample_curve_003.inputs[0])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-3947.518798828125, 276.45404052734375)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], resample_curve_004.inputs[0])
    links.new(group_input.outputs[2], resample_curve_004.inputs[3])
    links.new(group_input.outputs[3], subdivide_curve_001.inputs[1])
    links.new(group_input.outputs[3], math_021.inputs[0])
    links.new(group_input.outputs[3], math_019.inputs[0])
    links.new(group_input.outputs[6], set_spline_cyclic_002.inputs[2])
    links.new(group_input.outputs[6], switch_003.inputs[0])
    links.new(group_input.outputs[5], switch_011.inputs[0])
    links.new(group_input.outputs[6], switch_016.inputs[0])
    links.new(group_input.outputs[5], switch_014.inputs[0])
    links.new(group_input.outputs[5], boolean_math_001.inputs[0])
    links.new(group_input.outputs[6], boolean_math_001.inputs[1])
    links.new(group_input.outputs[1], switch_010.inputs[0])
    links.new(group_input.outputs[5], boolean_math.inputs[0])
    links.new(group_input.outputs[6], boolean_math.inputs[1])
    links.new(group_input.outputs[1], math.inputs[0])
    links.new(group_input.outputs[0], switch_001.inputs[1])
    links.new(group_input.outputs[4], switch_001.inputs[0])
    links.new(group_input.outputs[2], switch_002.inputs[2])
    links.new(group_input.outputs[4], switch_002.inputs[0])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (72.481201171875, -83.54595184326172)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = True
    # Links for sample_index
    links.new(switch_001.outputs[0], sample_index.inputs[0])
    links.new(position_002.outputs[0], sample_index.inputs[1])
    links.new(sample_index.outputs[0], set_position_003.inputs[2])
    links.new(math_025.outputs[0], sample_index.inputs[2])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (72.481201171875, -83.54595184326172)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = True
    # Links for sample_index_001
    links.new(position_002.outputs[0], sample_index_001.inputs[1])
    links.new(sample_index_001.outputs[0], set_position_002.inputs[2])
    links.new(switch_018.outputs[0], sample_index_001.inputs[0])
    links.new(switch_017.outputs[0], sample_index_001.inputs[2])

    viewer = nodes.new("GeometryNodeViewer")
    viewer.name = "Viewer"
    viewer.label = ""
    viewer.location = (-35.3814697265625, 378.11065673828125)
    viewer.bl_label = "Viewer"
    viewer.ui_shortcut = 0
    viewer.active_index = 0
    viewer.domain = "AUTO"
    # Links for viewer
    links.new(switch_018.outputs[0], viewer.inputs[0])

    auto_layout_nodes(group)
    return group