import bpy
import math
from mathutils import Vector, Color, Matrix
from procedural_human.utils.node_layout import auto_layout_nodes

def create_loft_splines_group():
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
    node_0 = nodes.new("GeometryNodeStoreNamedAttribute")
    node_0.name = "Store Named Attribute"
    node_0.label = ""
    node_0.location = (-1695.0, -40.0)
    node_0.location_absolute = (-1695.0, -40.0)
    node_0.warning_propagation = "ALL"
    node_0.use_custom_color = False
    node_0.show_options = True
    node_0.show_preview = False
    node_0.hide = False
    node_0.mute = False
    node_0.show_texture = False
    node_0.bl_idname = "GeometryNodeStoreNamedAttribute"
    node_0.bl_label = "Store Named Attribute"
    node_0.bl_description = "Store the result of a field on a geometry as an attribute with the specified name"
    node_0.bl_icon = "NONE"
    node_0.bl_width_default = 140.0
    node_0.bl_width_min = 100.0
    node_0.bl_width_max = 700.0
    node_0.bl_height_default = 100.0
    node_0.bl_height_min = 30.0
    node_0.bl_height_max = 30.0
    node_0.data_type = "FLOAT_VECTOR"
    node_0.domain = "CORNER"
    # Selection
    node_0.inputs[1].default_value = True
    # Name
    node_0.inputs[2].default_value = "uv_map"

    node_1 = nodes.new("ShaderNodeMath")
    node_1.name = "Math.024"
    node_1.label = ""
    node_1.location = (-2520.0, 40.0)
    node_1.location_absolute = (-2520.0, 40.0)
    node_1.warning_propagation = "ALL"
    node_1.use_custom_color = False
    node_1.show_options = True
    node_1.show_preview = False
    node_1.hide = False
    node_1.mute = False
    node_1.show_texture = False
    node_1.bl_idname = "ShaderNodeMath"
    node_1.bl_label = "Math"
    node_1.bl_description = "Perform math operations"
    node_1.bl_icon = "NONE"
    node_1.bl_width_default = 140.0
    node_1.bl_width_min = 100.0
    node_1.bl_width_max = 700.0
    node_1.bl_height_default = 100.0
    node_1.bl_height_min = 30.0
    node_1.bl_height_max = 30.0
    node_1.operation = "MULTIPLY"
    node_1.use_clamp = False
    # Value
    node_1.inputs[2].default_value = 0.5

    node_2 = nodes.new("ShaderNodeMath")
    node_2.name = "Math.026"
    node_2.label = ""
    node_2.location = (-2700.0, 40.0)
    node_2.location_absolute = (-2700.0, 40.0)
    node_2.warning_propagation = "ALL"
    node_2.use_custom_color = False
    node_2.show_options = True
    node_2.show_preview = False
    node_2.hide = False
    node_2.mute = False
    node_2.show_texture = False
    node_2.bl_idname = "ShaderNodeMath"
    node_2.bl_label = "Math"
    node_2.bl_description = "Perform math operations"
    node_2.bl_icon = "NONE"
    node_2.bl_width_default = 140.0
    node_2.bl_width_min = 100.0
    node_2.bl_width_max = 700.0
    node_2.bl_height_default = 100.0
    node_2.bl_height_min = 30.0
    node_2.bl_height_max = 30.0
    node_2.operation = "MODULO"
    node_2.use_clamp = False
    # Value
    node_2.inputs[2].default_value = 0.5

    node_3 = nodes.new("GeometryNodeDuplicateElements")
    node_3.name = "Duplicate Elements.001"
    node_3.label = ""
    node_3.location = (-2520.0, 240.0)
    node_3.location_absolute = (-2520.0, 240.0)
    node_3.warning_propagation = "ALL"
    node_3.use_custom_color = False
    node_3.show_options = True
    node_3.show_preview = False
    node_3.hide = False
    node_3.mute = False
    node_3.show_texture = False
    node_3.bl_idname = "GeometryNodeDuplicateElements"
    node_3.bl_label = "Duplicate Elements"
    node_3.bl_description = "Generate an arbitrary number copies of each selected input element"
    node_3.bl_icon = "NONE"
    node_3.bl_width_default = 140.0
    node_3.bl_width_min = 100.0
    node_3.bl_width_max = 700.0
    node_3.bl_height_default = 100.0
    node_3.bl_height_min = 30.0
    node_3.bl_height_max = 30.0
    node_3.domain = "SPLINE"
    # Selection
    node_3.inputs[1].default_value = True

    node_4 = nodes.new("GeometryNodeResampleCurve")
    node_4.name = "Resample Curve.003"
    node_4.label = ""
    node_4.location = (-2700.0, 240.0)
    node_4.location_absolute = (-2700.0, 240.0)
    node_4.warning_propagation = "ALL"
    node_4.use_custom_color = False
    node_4.show_options = True
    node_4.show_preview = False
    node_4.hide = False
    node_4.mute = False
    node_4.show_texture = False
    node_4.bl_idname = "GeometryNodeResampleCurve"
    node_4.bl_label = "Resample Curve"
    node_4.bl_description = "Generate a poly spline for each input spline"
    node_4.bl_icon = "NONE"
    node_4.bl_width_default = 140.0
    node_4.bl_width_min = 100.0
    node_4.bl_width_max = 700.0
    node_4.bl_height_default = 100.0
    node_4.bl_height_min = 30.0
    node_4.bl_height_max = 30.0
    node_4.keep_last_segment = False
    # Selection
    node_4.inputs[1].default_value = True
    # Mode
    node_4.inputs[2].default_value = "Count"
    # Length
    node_4.inputs[4].default_value = 0.10000000149011612

    node_5 = nodes.new("ShaderNodeMath")
    node_5.name = "Math.025"
    node_5.label = ""
    node_5.location = (-2340.0, 40.0)
    node_5.location_absolute = (-2340.0, 40.0)
    node_5.warning_propagation = "ALL"
    node_5.use_custom_color = False
    node_5.show_options = True
    node_5.show_preview = False
    node_5.hide = False
    node_5.mute = False
    node_5.show_texture = False
    node_5.bl_idname = "ShaderNodeMath"
    node_5.bl_label = "Math"
    node_5.bl_description = "Perform math operations"
    node_5.bl_icon = "NONE"
    node_5.bl_width_default = 140.0
    node_5.bl_width_min = 100.0
    node_5.bl_width_max = 700.0
    node_5.bl_height_default = 100.0
    node_5.bl_height_min = 30.0
    node_5.bl_height_max = 30.0
    node_5.operation = "ADD"
    node_5.use_clamp = False
    # Value
    node_5.inputs[2].default_value = 0.5

    node_6 = nodes.new("GeometryNodeSetPosition")
    node_6.name = "Set Position.003"
    node_6.label = ""
    node_6.location = (-1960.0, 260.0)
    node_6.location_absolute = (-1960.0, 260.0)
    node_6.warning_propagation = "ALL"
    node_6.use_custom_color = False
    node_6.show_options = True
    node_6.show_preview = False
    node_6.hide = False
    node_6.mute = False
    node_6.show_texture = False
    node_6.bl_idname = "GeometryNodeSetPosition"
    node_6.bl_label = "Set Position"
    node_6.bl_description = "Set the location of each point"
    node_6.bl_icon = "NONE"
    node_6.bl_width_default = 140.0
    node_6.bl_width_min = 100.0
    node_6.bl_width_max = 700.0
    node_6.bl_height_default = 100.0
    node_6.bl_height_min = 30.0
    node_6.bl_height_max = 30.0
    # Selection
    node_6.inputs[1].default_value = True
    # Offset
    node_6.inputs[3].default_value = (0.0, 0.0, 0.0)

    node_7 = nodes.new("GeometryNodeSwitch")
    node_7.name = "Switch.011"
    node_7.label = ""
    node_7.location = (-1920.0, -40.0)
    node_7.location_absolute = (-1920.0, -40.0)
    node_7.warning_propagation = "ALL"
    node_7.use_custom_color = False
    node_7.show_options = True
    node_7.show_preview = False
    node_7.hide = False
    node_7.mute = False
    node_7.show_texture = False
    node_7.bl_idname = "GeometryNodeSwitch"
    node_7.bl_label = "Switch"
    node_7.bl_description = "Switch between two inputs"
    node_7.bl_icon = "NONE"
    node_7.bl_width_default = 140.0
    node_7.bl_width_min = 100.0
    node_7.bl_width_max = 700.0
    node_7.bl_height_default = 100.0
    node_7.bl_height_min = 30.0
    node_7.bl_height_max = 30.0
    node_7.input_type = "INT"

    node_8 = nodes.new("ShaderNodeMath")
    node_8.name = "Math.027"
    node_8.label = ""
    node_8.location = (-2100.0, -160.0)
    node_8.location_absolute = (-2100.0, -160.0)
    node_8.warning_propagation = "ALL"
    node_8.use_custom_color = False
    node_8.show_options = True
    node_8.show_preview = False
    node_8.hide = False
    node_8.mute = False
    node_8.show_texture = False
    node_8.bl_idname = "ShaderNodeMath"
    node_8.bl_label = "Math"
    node_8.bl_description = "Perform math operations"
    node_8.bl_icon = "NONE"
    node_8.bl_width_default = 140.0
    node_8.bl_width_min = 100.0
    node_8.bl_width_max = 700.0
    node_8.bl_height_default = 100.0
    node_8.bl_height_min = 30.0
    node_8.bl_height_max = 30.0
    node_8.operation = "ADD"
    node_8.use_clamp = False
    # Value
    node_8.inputs[1].default_value = 1.0
    # Value
    node_8.inputs[2].default_value = 0.5

    node_9 = nodes.new("ShaderNodeMath")
    node_9.name = "Math.020"
    node_9.label = ""
    node_9.location = (-2280.0, -460.0)
    node_9.location_absolute = (-2280.0, -460.0)
    node_9.warning_propagation = "ALL"
    node_9.use_custom_color = False
    node_9.show_options = True
    node_9.show_preview = False
    node_9.hide = False
    node_9.mute = False
    node_9.show_texture = False
    node_9.bl_idname = "ShaderNodeMath"
    node_9.bl_label = "Math"
    node_9.bl_description = "Perform math operations"
    node_9.bl_icon = "NONE"
    node_9.bl_width_default = 140.0
    node_9.bl_width_min = 100.0
    node_9.bl_width_max = 700.0
    node_9.bl_height_default = 100.0
    node_9.bl_height_min = 30.0
    node_9.bl_height_max = 30.0
    node_9.operation = "SUBTRACT"
    node_9.use_clamp = False
    # Value
    node_9.inputs[2].default_value = 0.5

    node_10 = nodes.new("ShaderNodeMath")
    node_10.name = "Math.021"
    node_10.label = ""
    node_10.location = (-2280.0, -300.0)
    node_10.location_absolute = (-2280.0, -300.0)
    node_10.warning_propagation = "ALL"
    node_10.use_custom_color = False
    node_10.show_options = True
    node_10.show_preview = False
    node_10.hide = False
    node_10.mute = False
    node_10.show_texture = False
    node_10.bl_idname = "ShaderNodeMath"
    node_10.bl_label = "Math"
    node_10.bl_description = "Perform math operations"
    node_10.bl_icon = "NONE"
    node_10.bl_width_default = 140.0
    node_10.bl_width_min = 100.0
    node_10.bl_width_max = 700.0
    node_10.bl_height_default = 100.0
    node_10.bl_height_min = 30.0
    node_10.bl_height_max = 30.0
    node_10.operation = "ADD"
    node_10.use_clamp = False
    # Value
    node_10.inputs[1].default_value = 1.0
    # Value
    node_10.inputs[2].default_value = 0.5

    node_11 = nodes.new("ShaderNodeMath")
    node_11.name = "Math.022"
    node_11.label = ""
    node_11.location = (-2100.0, -360.0)
    node_11.location_absolute = (-2100.0, -360.0)
    node_11.warning_propagation = "ALL"
    node_11.use_custom_color = False
    node_11.show_options = True
    node_11.show_preview = False
    node_11.hide = False
    node_11.mute = False
    node_11.show_texture = False
    node_11.bl_idname = "ShaderNodeMath"
    node_11.bl_label = "Math"
    node_11.bl_description = "Perform math operations"
    node_11.bl_icon = "NONE"
    node_11.bl_width_default = 140.0
    node_11.bl_width_min = 100.0
    node_11.bl_width_max = 700.0
    node_11.bl_height_default = 100.0
    node_11.bl_height_min = 30.0
    node_11.bl_height_max = 30.0
    node_11.operation = "MULTIPLY"
    node_11.use_clamp = False
    # Value
    node_11.inputs[2].default_value = 0.5

    node_12 = nodes.new("ShaderNodeMath")
    node_12.name = "Math.023"
    node_12.label = ""
    node_12.location = (-1920.0, -360.0)
    node_12.location_absolute = (-1920.0, -360.0)
    node_12.warning_propagation = "ALL"
    node_12.use_custom_color = False
    node_12.show_options = True
    node_12.show_preview = False
    node_12.hide = False
    node_12.mute = False
    node_12.show_texture = False
    node_12.bl_idname = "ShaderNodeMath"
    node_12.bl_label = "Math"
    node_12.bl_description = "Perform math operations"
    node_12.bl_icon = "NONE"
    node_12.bl_width_default = 140.0
    node_12.bl_width_min = 100.0
    node_12.bl_width_max = 700.0
    node_12.bl_height_default = 100.0
    node_12.bl_height_min = 30.0
    node_12.bl_height_max = 30.0
    node_12.operation = "ADD"
    node_12.use_clamp = False
    # Value
    node_12.inputs[1].default_value = 1.0
    # Value
    node_12.inputs[2].default_value = 0.5

    node_13 = nodes.new("GeometryNodeSwitch")
    node_13.name = "Switch.003"
    node_13.label = ""
    node_13.location = (-2460.0, -460.0)
    node_13.location_absolute = (-2460.0, -460.0)
    node_13.warning_propagation = "ALL"
    node_13.use_custom_color = False
    node_13.show_options = True
    node_13.show_preview = False
    node_13.hide = False
    node_13.mute = False
    node_13.show_texture = False
    node_13.bl_idname = "GeometryNodeSwitch"
    node_13.bl_label = "Switch"
    node_13.bl_description = "Switch between two inputs"
    node_13.bl_icon = "NONE"
    node_13.bl_width_default = 140.0
    node_13.bl_width_min = 100.0
    node_13.bl_width_max = 700.0
    node_13.bl_height_default = 100.0
    node_13.bl_height_min = 30.0
    node_13.bl_height_max = 30.0
    node_13.input_type = "FLOAT"
    # False
    node_13.inputs[1].default_value = 1.0
    # True
    node_13.inputs[2].default_value = 0.0

    node_14 = nodes.new("GeometryNodeMeshGrid")
    node_14.name = "Grid.001"
    node_14.label = ""
    node_14.location = (-1720.0, -40.0)
    node_14.location_absolute = (-1720.0, -40.0)
    node_14.warning_propagation = "ALL"
    node_14.use_custom_color = False
    node_14.show_options = True
    node_14.show_preview = False
    node_14.hide = False
    node_14.mute = False
    node_14.show_texture = False
    node_14.bl_idname = "GeometryNodeMeshGrid"
    node_14.bl_label = "Grid"
    node_14.bl_description = "Generate a planar mesh on the XY plane"
    node_14.bl_icon = "NONE"
    node_14.bl_width_default = 140.0
    node_14.bl_width_min = 100.0
    node_14.bl_width_max = 700.0
    node_14.bl_height_default = 100.0
    node_14.bl_height_min = 30.0
    node_14.bl_height_max = 30.0
    # Size X
    node_14.inputs[0].default_value = 1.0
    # Size Y
    node_14.inputs[1].default_value = 1.0

    node_15 = nodes.new("ShaderNodeMath")
    node_15.name = "Math.028"
    node_15.label = ""
    node_15.location = (-1580.0, -280.0)
    node_15.location_absolute = (-1580.0, -280.0)
    node_15.warning_propagation = "ALL"
    node_15.use_custom_color = False
    node_15.show_options = True
    node_15.show_preview = False
    node_15.hide = False
    node_15.mute = False
    node_15.show_texture = False
    node_15.bl_idname = "ShaderNodeMath"
    node_15.bl_label = "Math"
    node_15.bl_description = "Perform math operations"
    node_15.bl_icon = "NONE"
    node_15.bl_width_default = 140.0
    node_15.bl_width_min = 100.0
    node_15.bl_width_max = 700.0
    node_15.bl_height_default = 100.0
    node_15.bl_height_min = 30.0
    node_15.bl_height_max = 30.0
    node_15.operation = "DIVIDE"
    node_15.use_clamp = False
    # Value
    node_15.inputs[2].default_value = 0.5

    node_16 = nodes.new("ShaderNodeMath")
    node_16.name = "Math.029"
    node_16.label = ""
    node_16.location = (-1580.0, -440.0)
    node_16.location_absolute = (-1580.0, -440.0)
    node_16.warning_propagation = "ALL"
    node_16.use_custom_color = False
    node_16.show_options = True
    node_16.show_preview = False
    node_16.hide = False
    node_16.mute = False
    node_16.show_texture = False
    node_16.bl_idname = "ShaderNodeMath"
    node_16.bl_label = "Math"
    node_16.bl_description = "Perform math operations"
    node_16.bl_icon = "NONE"
    node_16.bl_width_default = 140.0
    node_16.bl_width_min = 100.0
    node_16.bl_width_max = 700.0
    node_16.bl_height_default = 100.0
    node_16.bl_height_min = 30.0
    node_16.bl_height_max = 30.0
    node_16.operation = "MODULO"
    node_16.use_clamp = False
    # Value
    node_16.inputs[2].default_value = 0.5

    node_17 = nodes.new("ShaderNodeMath")
    node_17.name = "Math.031"
    node_17.label = ""
    node_17.location = (-1400.0, -280.0)
    node_17.location_absolute = (-1400.0, -280.0)
    node_17.warning_propagation = "ALL"
    node_17.use_custom_color = False
    node_17.show_options = True
    node_17.show_preview = False
    node_17.hide = False
    node_17.mute = False
    node_17.show_texture = False
    node_17.bl_idname = "ShaderNodeMath"
    node_17.bl_label = "Math"
    node_17.bl_description = "Perform math operations"
    node_17.bl_icon = "NONE"
    node_17.bl_width_default = 140.0
    node_17.bl_width_min = 100.0
    node_17.bl_width_max = 700.0
    node_17.bl_height_default = 100.0
    node_17.bl_height_min = 30.0
    node_17.bl_height_max = 30.0
    node_17.operation = "FLOOR"
    node_17.use_clamp = False
    # Value
    node_17.inputs[1].default_value = 0.5
    # Value
    node_17.inputs[2].default_value = 0.5

    node_18 = nodes.new("ShaderNodeMath")
    node_18.name = "Math.032"
    node_18.label = ""
    node_18.location = (-1220.0, -280.0)
    node_18.location_absolute = (-1220.0, -280.0)
    node_18.warning_propagation = "ALL"
    node_18.use_custom_color = False
    node_18.show_options = True
    node_18.show_preview = False
    node_18.hide = False
    node_18.mute = False
    node_18.show_texture = False
    node_18.bl_idname = "ShaderNodeMath"
    node_18.bl_label = "Math"
    node_18.bl_description = "Perform math operations"
    node_18.bl_icon = "NONE"
    node_18.bl_width_default = 140.0
    node_18.bl_width_min = 100.0
    node_18.bl_width_max = 700.0
    node_18.bl_height_default = 100.0
    node_18.bl_height_min = 30.0
    node_18.bl_height_max = 30.0
    node_18.operation = "SUBTRACT"
    node_18.use_clamp = False
    # Value
    node_18.inputs[2].default_value = 0.5

    node_19 = nodes.new("FunctionNodeCompare")
    node_19.name = "Compare.003"
    node_19.label = ""
    node_19.location = (-1400.0, -440.0)
    node_19.location_absolute = (-1400.0, -440.0)
    node_19.warning_propagation = "ALL"
    node_19.use_custom_color = False
    node_19.show_options = True
    node_19.show_preview = False
    node_19.hide = False
    node_19.mute = False
    node_19.show_texture = False
    node_19.bl_idname = "FunctionNodeCompare"
    node_19.bl_label = "Compare"
    node_19.bl_description = "Perform a comparison operation on the two given inputs"
    node_19.bl_icon = "NONE"
    node_19.bl_width_default = 140.0
    node_19.bl_width_min = 100.0
    node_19.bl_width_max = 700.0
    node_19.bl_height_default = 100.0
    node_19.bl_height_min = 30.0
    node_19.bl_height_max = 30.0
    node_19.operation = "EQUAL"
    node_19.data_type = "INT"
    node_19.mode = "ELEMENT"
    # A
    node_19.inputs[0].default_value = 0.0
    # B
    node_19.inputs[1].default_value = 0.0
    # A
    node_19.inputs[4].default_value = <bpy_float[3], NodeSocketVector.default_value>
    # B
    node_19.inputs[5].default_value = <bpy_float[3], NodeSocketVector.default_value>
    # A
    node_19.inputs[6].default_value = <bpy_float[4], NodeSocketColor.default_value>
    # B
    node_19.inputs[7].default_value = <bpy_float[4], NodeSocketColor.default_value>
    # A
    node_19.inputs[8].default_value = ""
    # B
    node_19.inputs[9].default_value = ""
    # C
    node_19.inputs[10].default_value = 0.8999999761581421
    # Angle
    node_19.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    node_19.inputs[12].default_value = 0.0010000000474974513

    node_20 = nodes.new("ShaderNodeMath")
    node_20.name = "Math.033"
    node_20.label = ""
    node_20.location = (-1220.0, -440.0)
    node_20.location_absolute = (-1220.0, -440.0)
    node_20.warning_propagation = "ALL"
    node_20.use_custom_color = False
    node_20.show_options = True
    node_20.show_preview = False
    node_20.hide = False
    node_20.mute = False
    node_20.show_texture = False
    node_20.bl_idname = "ShaderNodeMath"
    node_20.bl_label = "Math"
    node_20.bl_description = "Perform math operations"
    node_20.bl_icon = "NONE"
    node_20.bl_width_default = 140.0
    node_20.bl_width_min = 100.0
    node_20.bl_width_max = 700.0
    node_20.bl_height_default = 100.0
    node_20.bl_height_min = 30.0
    node_20.bl_height_max = 30.0
    node_20.operation = "MULTIPLY"
    node_20.use_clamp = False
    # Value
    node_20.inputs[2].default_value = 0.5

    node_21 = nodes.new("GeometryNodeSwitch")
    node_21.name = "Switch.012"
    node_21.label = ""
    node_21.location = (-1040.0, -280.0)
    node_21.location_absolute = (-1040.0, -280.0)
    node_21.warning_propagation = "ALL"
    node_21.use_custom_color = False
    node_21.show_options = True
    node_21.show_preview = False
    node_21.hide = False
    node_21.mute = False
    node_21.show_texture = False
    node_21.bl_idname = "GeometryNodeSwitch"
    node_21.bl_label = "Switch"
    node_21.bl_description = "Switch between two inputs"
    node_21.bl_icon = "NONE"
    node_21.bl_width_default = 140.0
    node_21.bl_width_min = 100.0
    node_21.bl_width_max = 700.0
    node_21.bl_height_default = 100.0
    node_21.bl_height_min = 30.0
    node_21.bl_height_max = 30.0
    node_21.input_type = "FLOAT"

    node_22 = nodes.new("GeometryNodeInputPosition")
    node_22.name = "Position.002"
    node_22.label = ""
    node_22.location = (-2340.0, 140.0)
    node_22.location_absolute = (-2340.0, 140.0)
    node_22.warning_propagation = "ALL"
    node_22.use_custom_color = False
    node_22.show_options = True
    node_22.show_preview = False
    node_22.hide = False
    node_22.mute = False
    node_22.show_texture = False
    node_22.bl_idname = "GeometryNodeInputPosition"
    node_22.bl_label = "Position"
    node_22.bl_description = "Retrieve a vector indicating the location of each element"
    node_22.bl_icon = "NONE"
    node_22.bl_width_default = 140.0
    node_22.bl_width_min = 100.0
    node_22.bl_width_max = 700.0
    node_22.bl_height_default = 100.0
    node_22.bl_height_min = 30.0
    node_22.bl_height_max = 30.0

    node_23 = nodes.new("ShaderNodeMath")
    node_23.name = "Math.030"
    node_23.label = ""
    node_23.location = (-1580.0, -600.0)
    node_23.location_absolute = (-1580.0, -600.0)
    node_23.warning_propagation = "ALL"
    node_23.use_custom_color = False
    node_23.show_options = True
    node_23.show_preview = False
    node_23.hide = False
    node_23.mute = False
    node_23.show_texture = False
    node_23.bl_idname = "ShaderNodeMath"
    node_23.bl_label = "Math"
    node_23.bl_description = "Perform math operations"
    node_23.bl_icon = "NONE"
    node_23.bl_width_default = 140.0
    node_23.bl_width_min = 100.0
    node_23.bl_width_max = 700.0
    node_23.bl_height_default = 100.0
    node_23.bl_height_min = 30.0
    node_23.bl_height_max = 30.0
    node_23.operation = "SUBTRACT"
    node_23.use_clamp = False
    # Value
    node_23.inputs[1].default_value = 1.0
    # Value
    node_23.inputs[2].default_value = 0.5

    node_24 = nodes.new("ShaderNodeMath")
    node_24.name = "Math.034"
    node_24.label = ""
    node_24.location = (-1400.0, -620.0)
    node_24.location_absolute = (-1400.0, -620.0)
    node_24.warning_propagation = "ALL"
    node_24.use_custom_color = False
    node_24.show_options = True
    node_24.show_preview = False
    node_24.hide = False
    node_24.mute = False
    node_24.show_texture = False
    node_24.bl_idname = "ShaderNodeMath"
    node_24.bl_label = "Math"
    node_24.bl_description = "Perform math operations"
    node_24.bl_icon = "NONE"
    node_24.bl_width_default = 140.0
    node_24.bl_width_min = 100.0
    node_24.bl_width_max = 700.0
    node_24.bl_height_default = 100.0
    node_24.bl_height_min = 30.0
    node_24.bl_height_max = 30.0
    node_24.operation = "MULTIPLY"
    node_24.use_clamp = False
    # Value
    node_24.inputs[2].default_value = 0.5

    node_25 = nodes.new("FunctionNodeCompare")
    node_25.name = "Compare.004"
    node_25.label = ""
    node_25.location = (-1220.0, -620.0)
    node_25.location_absolute = (-1220.0, -620.0)
    node_25.warning_propagation = "ALL"
    node_25.use_custom_color = False
    node_25.show_options = True
    node_25.show_preview = False
    node_25.hide = False
    node_25.mute = False
    node_25.show_texture = False
    node_25.bl_idname = "FunctionNodeCompare"
    node_25.bl_label = "Compare"
    node_25.bl_description = "Perform a comparison operation on the two given inputs"
    node_25.bl_icon = "NONE"
    node_25.bl_width_default = 140.0
    node_25.bl_width_min = 100.0
    node_25.bl_width_max = 700.0
    node_25.bl_height_default = 100.0
    node_25.bl_height_min = 30.0
    node_25.bl_height_max = 30.0
    node_25.operation = "GREATER_EQUAL"
    node_25.data_type = "INT"
    node_25.mode = "ELEMENT"
    # A
    node_25.inputs[0].default_value = 0.0
    # B
    node_25.inputs[1].default_value = 0.0
    # A
    node_25.inputs[4].default_value = <bpy_float[3], NodeSocketVector.default_value>
    # B
    node_25.inputs[5].default_value = <bpy_float[3], NodeSocketVector.default_value>
    # A
    node_25.inputs[6].default_value = <bpy_float[4], NodeSocketColor.default_value>
    # B
    node_25.inputs[7].default_value = <bpy_float[4], NodeSocketColor.default_value>
    # A
    node_25.inputs[8].default_value = ""
    # B
    node_25.inputs[9].default_value = ""
    # C
    node_25.inputs[10].default_value = 0.8999999761581421
    # Angle
    node_25.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    node_25.inputs[12].default_value = 0.0010000000474974513

    node_26 = nodes.new("ShaderNodeMath")
    node_26.name = "Math.035"
    node_26.label = ""
    node_26.location = (-1220.0, -800.0)
    node_26.location_absolute = (-1220.0, -800.0)
    node_26.warning_propagation = "ALL"
    node_26.use_custom_color = False
    node_26.show_options = True
    node_26.show_preview = False
    node_26.hide = False
    node_26.mute = False
    node_26.show_texture = False
    node_26.bl_idname = "ShaderNodeMath"
    node_26.bl_label = "Math"
    node_26.bl_description = "Perform math operations"
    node_26.bl_icon = "NONE"
    node_26.bl_width_default = 140.0
    node_26.bl_width_min = 100.0
    node_26.bl_width_max = 700.0
    node_26.bl_height_default = 100.0
    node_26.bl_height_min = 30.0
    node_26.bl_height_max = 30.0
    node_26.operation = "MODULO"
    node_26.use_clamp = False
    # Value
    node_26.inputs[2].default_value = 0.5

    node_27 = nodes.new("FunctionNodeBooleanMath")
    node_27.name = "Boolean Math.001"
    node_27.label = ""
    node_27.location = (-260.0, 0.0)
    node_27.location_absolute = (-260.0, 0.0)
    node_27.warning_propagation = "ALL"
    node_27.use_custom_color = False
    node_27.show_options = True
    node_27.show_preview = False
    node_27.hide = False
    node_27.mute = False
    node_27.show_texture = False
    node_27.bl_idname = "FunctionNodeBooleanMath"
    node_27.bl_label = "Boolean Math"
    node_27.bl_description = "Perform a logical operation on the given boolean inputs"
    node_27.bl_icon = "NONE"
    node_27.bl_width_default = 140.0
    node_27.bl_width_min = 100.0
    node_27.bl_width_max = 700.0
    node_27.bl_height_default = 100.0
    node_27.bl_height_min = 30.0
    node_27.bl_height_max = 30.0
    node_27.operation = "AND"

    node_28 = nodes.new("GeometryNodeSwitch")
    node_28.name = "Switch.017"
    node_28.label = ""
    node_28.location = (-80.0, 0.0)
    node_28.location_absolute = (-80.0, 0.0)
    node_28.warning_propagation = "ALL"
    node_28.use_custom_color = False
    node_28.show_options = True
    node_28.show_preview = False
    node_28.hide = False
    node_28.mute = False
    node_28.show_texture = False
    node_28.bl_idname = "GeometryNodeSwitch"
    node_28.bl_label = "Switch"
    node_28.bl_description = "Switch between two inputs"
    node_28.bl_icon = "NONE"
    node_28.bl_width_default = 140.0
    node_28.bl_width_min = 100.0
    node_28.bl_width_max = 700.0
    node_28.bl_height_default = 100.0
    node_28.bl_height_min = 30.0
    node_28.bl_height_max = 30.0
    node_28.input_type = "INT"

    node_29 = nodes.new("GeometryNodeSwitch")
    node_29.name = "Switch.014"
    node_29.label = ""
    node_29.location = (-440.0, 0.0)
    node_29.location_absolute = (-440.0, 0.0)
    node_29.warning_propagation = "ALL"
    node_29.use_custom_color = False
    node_29.show_options = True
    node_29.show_preview = False
    node_29.hide = False
    node_29.mute = False
    node_29.show_texture = False
    node_29.bl_idname = "GeometryNodeSwitch"
    node_29.bl_label = "Switch"
    node_29.bl_description = "Switch between two inputs"
    node_29.bl_icon = "NONE"
    node_29.bl_width_default = 140.0
    node_29.bl_width_min = 100.0
    node_29.bl_width_max = 700.0
    node_29.bl_height_default = 100.0
    node_29.bl_height_min = 30.0
    node_29.bl_height_max = 30.0
    node_29.input_type = "INT"

    node_30 = nodes.new("FunctionNodeCompare")
    node_30.name = "Compare.005"
    node_30.label = ""
    node_30.location = (-440.0, -180.0)
    node_30.location_absolute = (-440.0, -180.0)
    node_30.warning_propagation = "ALL"
    node_30.use_custom_color = False
    node_30.show_options = True
    node_30.show_preview = False
    node_30.hide = False
    node_30.mute = False
    node_30.show_texture = False
    node_30.bl_idname = "FunctionNodeCompare"
    node_30.bl_label = "Compare"
    node_30.bl_description = "Perform a comparison operation on the two given inputs"
    node_30.bl_icon = "NONE"
    node_30.bl_width_default = 140.0
    node_30.bl_width_min = 100.0
    node_30.bl_width_max = 700.0
    node_30.bl_height_default = 100.0
    node_30.bl_height_min = 30.0
    node_30.bl_height_max = 30.0
    node_30.operation = "EQUAL"
    node_30.data_type = "INT"
    node_30.mode = "ELEMENT"
    # A
    node_30.inputs[0].default_value = 0.0
    # B
    node_30.inputs[1].default_value = 0.0
    # A
    node_30.inputs[4].default_value = <bpy_float[3], NodeSocketVector.default_value>
    # B
    node_30.inputs[5].default_value = <bpy_float[3], NodeSocketVector.default_value>
    # A
    node_30.inputs[6].default_value = <bpy_float[4], NodeSocketColor.default_value>
    # B
    node_30.inputs[7].default_value = <bpy_float[4], NodeSocketColor.default_value>
    # A
    node_30.inputs[8].default_value = ""
    # B
    node_30.inputs[9].default_value = ""
    # C
    node_30.inputs[10].default_value = 0.8999999761581421
    # Angle
    node_30.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    node_30.inputs[12].default_value = 0.0010000000474974513

    node_31 = nodes.new("GeometryNodeSwitch")
    node_31.name = "Switch.015"
    node_31.label = ""
    node_31.location = (-260.0, -160.0)
    node_31.location_absolute = (-260.0, -160.0)
    node_31.warning_propagation = "ALL"
    node_31.use_custom_color = False
    node_31.show_options = True
    node_31.show_preview = False
    node_31.hide = False
    node_31.mute = False
    node_31.show_texture = False
    node_31.bl_idname = "GeometryNodeSwitch"
    node_31.bl_label = "Switch"
    node_31.bl_description = "Switch between two inputs"
    node_31.bl_icon = "NONE"
    node_31.bl_width_default = 140.0
    node_31.bl_width_min = 100.0
    node_31.bl_width_max = 700.0
    node_31.bl_height_default = 100.0
    node_31.bl_height_min = 30.0
    node_31.bl_height_max = 30.0
    node_31.input_type = "INT"
    # True
    node_31.inputs[2].default_value = 0

    node_32 = nodes.new("ShaderNodeMath")
    node_32.name = "Math.036"
    node_32.label = ""
    node_32.location = (-620.0, -340.0)
    node_32.location_absolute = (-620.0, -340.0)
    node_32.warning_propagation = "ALL"
    node_32.use_custom_color = False
    node_32.show_options = True
    node_32.show_preview = False
    node_32.hide = False
    node_32.mute = False
    node_32.show_texture = False
    node_32.bl_idname = "ShaderNodeMath"
    node_32.bl_label = "Math"
    node_32.bl_description = "Perform math operations"
    node_32.bl_icon = "NONE"
    node_32.bl_width_default = 140.0
    node_32.bl_width_min = 100.0
    node_32.bl_width_max = 700.0
    node_32.bl_height_default = 100.0
    node_32.bl_height_min = 30.0
    node_32.bl_height_max = 30.0
    node_32.operation = "SUBTRACT"
    node_32.use_clamp = False
    # Value
    node_32.inputs[1].default_value = 1.0
    # Value
    node_32.inputs[2].default_value = 0.5

    node_33 = nodes.new("ShaderNodeMath")
    node_33.name = "Math.037"
    node_33.label = ""
    node_33.location = (-800.0, -340.0)
    node_33.location_absolute = (-800.0, -340.0)
    node_33.warning_propagation = "ALL"
    node_33.use_custom_color = False
    node_33.show_options = True
    node_33.show_preview = False
    node_33.hide = False
    node_33.mute = False
    node_33.show_texture = False
    node_33.bl_idname = "ShaderNodeMath"
    node_33.bl_label = "Math"
    node_33.bl_description = "Perform math operations"
    node_33.bl_icon = "NONE"
    node_33.bl_width_default = 140.0
    node_33.bl_width_min = 100.0
    node_33.bl_width_max = 700.0
    node_33.bl_height_default = 100.0
    node_33.bl_height_min = 30.0
    node_33.bl_height_max = 30.0
    node_33.operation = "MULTIPLY"
    node_33.use_clamp = False
    # Value
    node_33.inputs[2].default_value = 0.5

    node_34 = nodes.new("GeometryNodeSwitch")
    node_34.name = "Switch.016"
    node_34.label = ""
    node_34.location = (-800.0, -80.0)
    node_34.location_absolute = (-800.0, -80.0)
    node_34.warning_propagation = "ALL"
    node_34.use_custom_color = False
    node_34.show_options = True
    node_34.show_preview = False
    node_34.hide = False
    node_34.mute = False
    node_34.show_texture = False
    node_34.bl_idname = "GeometryNodeSwitch"
    node_34.bl_label = "Switch"
    node_34.bl_description = "Switch between two inputs"
    node_34.bl_icon = "NONE"
    node_34.bl_width_default = 140.0
    node_34.bl_width_min = 100.0
    node_34.bl_width_max = 700.0
    node_34.bl_height_default = 100.0
    node_34.bl_height_min = 30.0
    node_34.bl_height_max = 30.0
    node_34.input_type = "INT"

    node_35 = nodes.new("GeometryNodeSwitch")
    node_35.name = "Switch.013"
    node_35.label = ""
    node_35.location = (-620.0, -80.0)
    node_35.location_absolute = (-620.0, -80.0)
    node_35.warning_propagation = "ALL"
    node_35.use_custom_color = False
    node_35.show_options = True
    node_35.show_preview = False
    node_35.hide = False
    node_35.mute = False
    node_35.show_texture = False
    node_35.bl_idname = "GeometryNodeSwitch"
    node_35.bl_label = "Switch"
    node_35.bl_description = "Switch between two inputs"
    node_35.bl_icon = "NONE"
    node_35.bl_width_default = 140.0
    node_35.bl_width_min = 100.0
    node_35.bl_width_max = 700.0
    node_35.bl_height_default = 100.0
    node_35.bl_height_min = 30.0
    node_35.bl_height_max = 30.0
    node_35.input_type = "INT"

    node_36 = nodes.new("GeometryNodeSetSplineCyclic")
    node_36.name = "Set Spline Cyclic.002"
    node_36.label = ""
    node_36.location = (-1720.0, 260.0)
    node_36.location_absolute = (-1720.0, 260.0)
    node_36.warning_propagation = "ALL"
    node_36.use_custom_color = False
    node_36.show_options = True
    node_36.show_preview = False
    node_36.hide = False
    node_36.mute = False
    node_36.show_texture = False
    node_36.bl_idname = "GeometryNodeSetSplineCyclic"
    node_36.bl_label = "Set Spline Cyclic"
    node_36.bl_description = "Control whether each spline loops back on itself by changing the \"cyclic\" attribute"
    node_36.bl_icon = "NONE"
    node_36.bl_width_default = 140.0
    node_36.bl_width_min = 100.0
    node_36.bl_width_max = 700.0
    node_36.bl_height_default = 100.0
    node_36.bl_height_min = 30.0
    node_36.bl_height_max = 30.0
    # Selection
    node_36.inputs[1].default_value = True

    node_37 = nodes.new("ShaderNodeMath")
    node_37.name = "Math.019"
    node_37.label = ""
    node_37.location = (-1720.0, 440.0)
    node_37.location_absolute = (-1720.0, 440.0)
    node_37.warning_propagation = "ALL"
    node_37.use_custom_color = False
    node_37.show_options = True
    node_37.show_preview = False
    node_37.hide = False
    node_37.mute = False
    node_37.show_texture = False
    node_37.bl_idname = "ShaderNodeMath"
    node_37.bl_label = "Math"
    node_37.bl_description = "Perform math operations"
    node_37.bl_icon = "NONE"
    node_37.bl_width_default = 140.0
    node_37.bl_width_min = 100.0
    node_37.bl_width_max = 700.0
    node_37.bl_height_default = 100.0
    node_37.bl_height_min = 30.0
    node_37.bl_height_max = 30.0
    node_37.operation = "ADD"
    node_37.use_clamp = False
    # Value
    node_37.inputs[1].default_value = 1.0
    # Value
    node_37.inputs[2].default_value = 0.5

    node_38 = nodes.new("FunctionNodeCompare")
    node_38.name = "Compare"
    node_38.label = ""
    node_38.location = (300.0, -20.0)
    node_38.location_absolute = (300.0, -20.0)
    node_38.warning_propagation = "ALL"
    node_38.use_custom_color = False
    node_38.show_options = True
    node_38.show_preview = False
    node_38.hide = False
    node_38.mute = False
    node_38.show_texture = False
    node_38.bl_idname = "FunctionNodeCompare"
    node_38.bl_label = "Compare"
    node_38.bl_description = "Perform a comparison operation on the two given inputs"
    node_38.bl_icon = "NONE"
    node_38.bl_width_default = 140.0
    node_38.bl_width_min = 100.0
    node_38.bl_width_max = 700.0
    node_38.bl_height_default = 100.0
    node_38.bl_height_min = 30.0
    node_38.bl_height_max = 30.0
    node_38.operation = "EQUAL"
    node_38.data_type = "INT"
    node_38.mode = "ELEMENT"
    # A
    node_38.inputs[0].default_value = 0.0
    # B
    node_38.inputs[1].default_value = 0.0
    # B
    node_38.inputs[3].default_value = 1
    # A
    node_38.inputs[4].default_value = <bpy_float[3], NodeSocketVector.default_value>
    # B
    node_38.inputs[5].default_value = <bpy_float[3], NodeSocketVector.default_value>
    # A
    node_38.inputs[6].default_value = <bpy_float[4], NodeSocketColor.default_value>
    # B
    node_38.inputs[7].default_value = <bpy_float[4], NodeSocketColor.default_value>
    # A
    node_38.inputs[8].default_value = ""
    # B
    node_38.inputs[9].default_value = ""
    # C
    node_38.inputs[10].default_value = 0.8999999761581421
    # Angle
    node_38.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    node_38.inputs[12].default_value = 0.0010000000474974513

    node_39 = nodes.new("GeometryNodeInputMeshEdgeNeighbors")
    node_39.name = "Edge Neighbors"
    node_39.label = ""
    node_39.location = (120.0, -100.0)
    node_39.location_absolute = (120.0, -100.0)
    node_39.warning_propagation = "ALL"
    node_39.use_custom_color = False
    node_39.show_options = True
    node_39.show_preview = False
    node_39.hide = False
    node_39.mute = False
    node_39.show_texture = False
    node_39.bl_idname = "GeometryNodeInputMeshEdgeNeighbors"
    node_39.bl_label = "Edge Neighbors"
    node_39.bl_description = "Retrieve the number of faces that use each edge as one of their sides"
    node_39.bl_icon = "NONE"
    node_39.bl_width_default = 140.0
    node_39.bl_width_min = 100.0
    node_39.bl_width_max = 700.0
    node_39.bl_height_default = 100.0
    node_39.bl_height_min = 30.0
    node_39.bl_height_max = 30.0

    node_40 = nodes.new("GeometryNodeSetPosition")
    node_40.name = "Set Position.002"
    node_40.label = ""
    node_40.location = (300.0, 220.0)
    node_40.location_absolute = (300.0, 220.0)
    node_40.warning_propagation = "ALL"
    node_40.use_custom_color = False
    node_40.show_options = True
    node_40.show_preview = False
    node_40.hide = False
    node_40.mute = False
    node_40.show_texture = False
    node_40.bl_idname = "GeometryNodeSetPosition"
    node_40.bl_label = "Set Position"
    node_40.bl_description = "Set the location of each point"
    node_40.bl_icon = "NONE"
    node_40.bl_width_default = 140.0
    node_40.bl_width_min = 100.0
    node_40.bl_width_max = 700.0
    node_40.bl_height_default = 100.0
    node_40.bl_height_min = 30.0
    node_40.bl_height_max = 30.0
    # Selection
    node_40.inputs[1].default_value = True
    # Offset
    node_40.inputs[3].default_value = (0.0, 0.0, 0.0)

    node_41 = nodes.new("GeometryNodeMergeByDistance")
    node_41.name = "Merge by Distance"
    node_41.label = ""
    node_41.location = (500.0, 60.0)
    node_41.location_absolute = (500.0, 60.0)
    node_41.warning_propagation = "ALL"
    node_41.use_custom_color = False
    node_41.show_options = True
    node_41.show_preview = False
    node_41.hide = False
    node_41.mute = False
    node_41.show_texture = False
    node_41.bl_idname = "GeometryNodeMergeByDistance"
    node_41.bl_label = "Merge by Distance"
    node_41.bl_description = "Merge vertices or points within a given distance"
    node_41.bl_icon = "NONE"
    node_41.bl_width_default = 140.0
    node_41.bl_width_min = 100.0
    node_41.bl_width_max = 700.0
    node_41.bl_height_default = 100.0
    node_41.bl_height_min = 30.0
    node_41.bl_height_max = 30.0
    # Mode
    node_41.inputs[2].default_value = "All"
    # Distance
    node_41.inputs[3].default_value = 9.999999747378752e-06

    node_42 = nodes.new("NodeGroupOutput")
    node_42.name = "Group Output"
    node_42.label = ""
    node_42.location = (900.0, 200.0)
    node_42.location_absolute = (900.0, 200.0)
    node_42.warning_propagation = "ALL"
    node_42.use_custom_color = False
    node_42.show_options = True
    node_42.show_preview = False
    node_42.hide = False
    node_42.mute = False
    node_42.show_texture = False
    node_42.bl_idname = "NodeGroupOutput"
    node_42.bl_label = "Group Output"
    node_42.bl_description = "Output data from inside of a node group"
    node_42.bl_icon = "NONE"
    node_42.bl_width_default = 140.0
    node_42.bl_width_min = 80.0
    node_42.bl_width_max = 400.0
    node_42.bl_height_default = 100.0
    node_42.bl_height_min = 30.0
    node_42.bl_height_max = 30.0
    node_42.is_active_output = True

    node_43 = nodes.new("FunctionNodeBooleanMath")
    node_43.name = "Boolean Math"
    node_43.label = ""
    node_43.location = (300.0, -200.0)
    node_43.location_absolute = (300.0, -200.0)
    node_43.warning_propagation = "ALL"
    node_43.use_custom_color = False
    node_43.show_options = True
    node_43.show_preview = False
    node_43.hide = False
    node_43.mute = False
    node_43.show_texture = False
    node_43.bl_idname = "FunctionNodeBooleanMath"
    node_43.bl_label = "Boolean Math"
    node_43.bl_description = "Perform a logical operation on the given boolean inputs"
    node_43.bl_icon = "NONE"
    node_43.bl_width_default = 140.0
    node_43.bl_width_min = 100.0
    node_43.bl_width_max = 700.0
    node_43.bl_height_default = 100.0
    node_43.bl_height_min = 30.0
    node_43.bl_height_max = 30.0
    node_43.operation = "OR"

    node_44 = nodes.new("GeometryNodeSwitch")
    node_44.name = "Switch"
    node_44.label = ""
    node_44.location = (700.0, 200.0)
    node_44.location_absolute = (700.0, 200.0)
    node_44.warning_propagation = "ALL"
    node_44.use_custom_color = False
    node_44.show_options = True
    node_44.show_preview = False
    node_44.hide = False
    node_44.mute = False
    node_44.show_texture = False
    node_44.bl_idname = "GeometryNodeSwitch"
    node_44.bl_label = "Switch"
    node_44.bl_description = "Switch between two inputs"
    node_44.bl_icon = "NONE"
    node_44.bl_width_default = 140.0
    node_44.bl_width_min = 100.0
    node_44.bl_width_max = 700.0
    node_44.bl_height_default = 100.0
    node_44.bl_height_min = 30.0
    node_44.bl_height_max = 30.0
    node_44.input_type = "GEOMETRY"

    node_45 = nodes.new("GeometryNodeSwitch")
    node_45.name = "Switch.010"
    node_45.label = ""
    node_45.location = (-760.0, 540.0)
    node_45.location_absolute = (-760.0, 540.0)
    node_45.warning_propagation = "ALL"
    node_45.use_custom_color = False
    node_45.show_options = True
    node_45.show_preview = False
    node_45.hide = False
    node_45.mute = False
    node_45.show_texture = False
    node_45.bl_idname = "GeometryNodeSwitch"
    node_45.bl_label = "Switch"
    node_45.bl_description = "Switch between two inputs"
    node_45.bl_icon = "NONE"
    node_45.bl_width_default = 140.0
    node_45.bl_width_min = 100.0
    node_45.bl_width_max = 700.0
    node_45.bl_height_default = 100.0
    node_45.bl_height_min = 30.0
    node_45.bl_height_max = 30.0
    node_45.input_type = "GEOMETRY"

    node_46 = nodes.new("GeometryNodeResampleCurve")
    node_46.name = "Resample Curve.006"
    node_46.label = ""
    node_46.location = (-1140.0, 360.0)
    node_46.location_absolute = (-1140.0, 360.0)
    node_46.warning_propagation = "ALL"
    node_46.use_custom_color = False
    node_46.show_options = True
    node_46.show_preview = False
    node_46.hide = False
    node_46.mute = False
    node_46.show_texture = False
    node_46.bl_idname = "GeometryNodeResampleCurve"
    node_46.bl_label = "Resample Curve"
    node_46.bl_description = "Generate a poly spline for each input spline"
    node_46.bl_icon = "NONE"
    node_46.bl_width_default = 140.0
    node_46.bl_width_min = 100.0
    node_46.bl_width_max = 700.0
    node_46.bl_height_default = 100.0
    node_46.bl_height_min = 30.0
    node_46.bl_height_max = 30.0
    node_46.keep_last_segment = False
    # Selection
    node_46.inputs[1].default_value = True
    # Mode
    node_46.inputs[2].default_value = "Evaluated"
    # Count
    node_46.inputs[3].default_value = 10
    # Length
    node_46.inputs[4].default_value = 0.10000000149011612

    node_47 = nodes.new("GeometryNodeCurveSplineType")
    node_47.name = "Set Spline Type.002"
    node_47.label = ""
    node_47.location = (-1320.0, 360.0)
    node_47.location_absolute = (-1320.0, 360.0)
    node_47.warning_propagation = "ALL"
    node_47.use_custom_color = False
    node_47.show_options = True
    node_47.show_preview = False
    node_47.hide = False
    node_47.mute = False
    node_47.show_texture = False
    node_47.bl_idname = "GeometryNodeCurveSplineType"
    node_47.bl_label = "Set Spline Type"
    node_47.bl_description = "Change the type of curves"
    node_47.bl_icon = "NONE"
    node_47.bl_width_default = 140.0
    node_47.bl_width_min = 100.0
    node_47.bl_width_max = 700.0
    node_47.bl_height_default = 100.0
    node_47.bl_height_min = 30.0
    node_47.bl_height_max = 30.0
    node_47.spline_type = "CATMULL_ROM"
    # Selection
    node_47.inputs[1].default_value = True

    node_48 = nodes.new("GeometryNodeCurveSplineType")
    node_48.name = "Set Spline Type.001"
    node_48.label = ""
    node_48.location = (-1320.0, 540.0)
    node_48.location_absolute = (-1320.0, 540.0)
    node_48.warning_propagation = "ALL"
    node_48.use_custom_color = False
    node_48.show_options = True
    node_48.show_preview = False
    node_48.hide = False
    node_48.mute = False
    node_48.show_texture = False
    node_48.bl_idname = "GeometryNodeCurveSplineType"
    node_48.bl_label = "Set Spline Type"
    node_48.bl_description = "Change the type of curves"
    node_48.bl_icon = "NONE"
    node_48.bl_width_default = 140.0
    node_48.bl_width_min = 100.0
    node_48.bl_width_max = 700.0
    node_48.bl_height_default = 100.0
    node_48.bl_height_min = 30.0
    node_48.bl_height_max = 30.0
    node_48.spline_type = "BEZIER"
    # Selection
    node_48.inputs[1].default_value = True

    node_49 = nodes.new("GeometryNodeCurveSetHandles")
    node_49.name = "Set Handle Type.001"
    node_49.label = ""
    node_49.location = (-1140.0, 540.0)
    node_49.location_absolute = (-1140.0, 540.0)
    node_49.warning_propagation = "ALL"
    node_49.use_custom_color = False
    node_49.show_options = True
    node_49.show_preview = False
    node_49.hide = False
    node_49.mute = False
    node_49.show_texture = False
    node_49.bl_idname = "GeometryNodeCurveSetHandles"
    node_49.bl_label = "Set Handle Type"
    node_49.bl_description = "Set the handle type for the control points of a Bézier curve"
    node_49.bl_icon = "NONE"
    node_49.bl_width_default = 140.0
    node_49.bl_width_min = 100.0
    node_49.bl_width_max = 700.0
    node_49.bl_height_default = 100.0
    node_49.bl_height_min = 30.0
    node_49.bl_height_max = 30.0
    node_49.handle_type = "AUTO"
    # Selection
    node_49.inputs[1].default_value = True

    node_50 = nodes.new("GeometryNodeResampleCurve")
    node_50.name = "Resample Curve.005"
    node_50.label = ""
    node_50.location = (-960.0, 540.0)
    node_50.location_absolute = (-960.0, 540.0)
    node_50.warning_propagation = "ALL"
    node_50.use_custom_color = False
    node_50.show_options = True
    node_50.show_preview = False
    node_50.hide = False
    node_50.mute = False
    node_50.show_texture = False
    node_50.bl_idname = "GeometryNodeResampleCurve"
    node_50.bl_label = "Resample Curve"
    node_50.bl_description = "Generate a poly spline for each input spline"
    node_50.bl_icon = "NONE"
    node_50.bl_width_default = 140.0
    node_50.bl_width_min = 100.0
    node_50.bl_width_max = 700.0
    node_50.bl_height_default = 100.0
    node_50.bl_height_min = 30.0
    node_50.bl_height_max = 30.0
    node_50.keep_last_segment = False
    # Selection
    node_50.inputs[1].default_value = True
    # Mode
    node_50.inputs[2].default_value = "Evaluated"
    # Count
    node_50.inputs[3].default_value = 10
    # Length
    node_50.inputs[4].default_value = 0.10000000149011612

    node_51 = nodes.new("GeometryNodeSetSplineResolution")
    node_51.name = "Set Spline Resolution.001"
    node_51.label = ""
    node_51.location = (-1500.0, 380.0)
    node_51.location_absolute = (-1500.0, 380.0)
    node_51.warning_propagation = "ALL"
    node_51.use_custom_color = False
    node_51.show_options = True
    node_51.show_preview = False
    node_51.hide = False
    node_51.mute = False
    node_51.show_texture = False
    node_51.bl_idname = "GeometryNodeSetSplineResolution"
    node_51.bl_label = "Set Spline Resolution"
    node_51.bl_description = "Control how many evaluated points should be generated on every curve segment"
    node_51.bl_icon = "NONE"
    node_51.bl_width_default = 140.0
    node_51.bl_width_min = 100.0
    node_51.bl_width_max = 700.0
    node_51.bl_height_default = 100.0
    node_51.bl_height_min = 30.0
    node_51.bl_height_max = 30.0
    # Selection
    node_51.inputs[1].default_value = True

    node_52 = nodes.new("GeometryNodeSubdivideCurve")
    node_52.name = "Subdivide Curve.001"
    node_52.label = ""
    node_52.location = (-1500.0, 220.0)
    node_52.location_absolute = (-1500.0, 220.0)
    node_52.warning_propagation = "ALL"
    node_52.use_custom_color = False
    node_52.show_options = True
    node_52.show_preview = False
    node_52.hide = False
    node_52.mute = False
    node_52.show_texture = False
    node_52.bl_idname = "GeometryNodeSubdivideCurve"
    node_52.bl_label = "Subdivide Curve"
    node_52.bl_description = "Dividing each curve segment into a specified number of pieces"
    node_52.bl_icon = "NONE"
    node_52.bl_width_default = 140.0
    node_52.bl_width_min = 100.0
    node_52.bl_width_max = 700.0
    node_52.bl_height_default = 100.0
    node_52.bl_height_min = 30.0
    node_52.bl_height_max = 30.0

    node_53 = nodes.new("ShaderNodeMath")
    node_53.name = "Math"
    node_53.label = ""
    node_53.location = (-760.0, 360.0)
    node_53.location_absolute = (-760.0, 360.0)
    node_53.warning_propagation = "ALL"
    node_53.use_custom_color = False
    node_53.show_options = True
    node_53.show_preview = False
    node_53.hide = False
    node_53.mute = False
    node_53.show_texture = False
    node_53.bl_idname = "ShaderNodeMath"
    node_53.bl_label = "Math"
    node_53.bl_description = "Perform math operations"
    node_53.bl_icon = "NONE"
    node_53.bl_width_default = 140.0
    node_53.bl_width_min = 100.0
    node_53.bl_width_max = 700.0
    node_53.bl_height_default = 100.0
    node_53.bl_height_min = 30.0
    node_53.bl_height_max = 30.0
    node_53.operation = "SUBTRACT"
    node_53.use_clamp = False
    # Value
    node_53.inputs[1].default_value = 1.0
    # Value
    node_53.inputs[2].default_value = 0.5

    node_54 = nodes.new("GeometryNodeSwitch")
    node_54.name = "Switch.018"
    node_54.label = ""
    node_54.location = (-520.0, 400.0)
    node_54.location_absolute = (-520.0, 400.0)
    node_54.warning_propagation = "ALL"
    node_54.use_custom_color = False
    node_54.show_options = True
    node_54.show_preview = False
    node_54.hide = False
    node_54.mute = False
    node_54.show_texture = False
    node_54.bl_idname = "GeometryNodeSwitch"
    node_54.bl_label = "Switch"
    node_54.bl_description = "Switch between two inputs"
    node_54.bl_icon = "NONE"
    node_54.bl_width_default = 140.0
    node_54.bl_width_min = 100.0
    node_54.bl_width_max = 700.0
    node_54.bl_height_default = 100.0
    node_54.bl_height_min = 30.0
    node_54.bl_height_max = 30.0
    node_54.input_type = "GEOMETRY"

    node_55 = nodes.new("GeometryNodeInputIndex")
    node_55.name = "Index.006"
    node_55.label = ""
    node_55.location = (-2920.0, -80.0)
    node_55.location_absolute = (-2920.0, -80.0)
    node_55.warning_propagation = "ALL"
    node_55.use_custom_color = False
    node_55.show_options = True
    node_55.show_preview = False
    node_55.hide = False
    node_55.mute = False
    node_55.show_texture = False
    node_55.bl_idname = "GeometryNodeInputIndex"
    node_55.bl_label = "Index"
    node_55.bl_description = "Retrieve an integer value indicating the position of each element in the list, starting at zero"
    node_55.bl_icon = "NONE"
    node_55.bl_width_default = 140.0
    node_55.bl_width_min = 100.0
    node_55.bl_width_max = 700.0
    node_55.bl_height_default = 100.0
    node_55.bl_height_min = 30.0
    node_55.bl_height_max = 30.0

    node_56 = nodes.new("GeometryNodeSwitch")
    node_56.name = "Switch.002"
    node_56.label = ""
    node_56.location = (-2900.0, 320.0)
    node_56.location_absolute = (-2900.0, 320.0)
    node_56.warning_propagation = "ALL"
    node_56.use_custom_color = False
    node_56.show_options = True
    node_56.show_preview = False
    node_56.hide = False
    node_56.mute = False
    node_56.show_texture = False
    node_56.bl_idname = "GeometryNodeSwitch"
    node_56.bl_label = "Switch"
    node_56.bl_description = "Switch between two inputs"
    node_56.bl_icon = "NONE"
    node_56.bl_width_default = 140.0
    node_56.bl_width_min = 100.0
    node_56.bl_width_max = 700.0
    node_56.bl_height_default = 100.0
    node_56.bl_height_min = 30.0
    node_56.bl_height_max = 30.0
    node_56.input_type = "INT"

    node_57 = nodes.new("ShaderNodeMath")
    node_57.name = "Math.001"
    node_57.label = ""
    node_57.location = (-3100.0, 320.0)
    node_57.location_absolute = (-3100.0, 320.0)
    node_57.warning_propagation = "ALL"
    node_57.use_custom_color = False
    node_57.show_options = True
    node_57.show_preview = False
    node_57.hide = False
    node_57.mute = False
    node_57.show_texture = False
    node_57.bl_idname = "ShaderNodeMath"
    node_57.bl_label = "Math"
    node_57.bl_description = "Perform math operations"
    node_57.bl_icon = "NONE"
    node_57.bl_width_default = 140.0
    node_57.bl_width_min = 100.0
    node_57.bl_width_max = 700.0
    node_57.bl_height_default = 100.0
    node_57.bl_height_min = 30.0
    node_57.bl_height_max = 30.0
    node_57.operation = "DIVIDE"
    node_57.use_clamp = False
    # Value
    node_57.inputs[2].default_value = 0.5

    node_58 = nodes.new("GeometryNodeAttributeDomainSize")
    node_58.name = "Domain Size.001"
    node_58.label = ""
    node_58.location = (-3320.0, 200.0)
    node_58.location_absolute = (-3320.0, 200.0)
    node_58.warning_propagation = "ALL"
    node_58.use_custom_color = False
    node_58.show_options = True
    node_58.show_preview = False
    node_58.hide = False
    node_58.mute = False
    node_58.show_texture = False
    node_58.bl_idname = "GeometryNodeAttributeDomainSize"
    node_58.bl_label = "Domain Size"
    node_58.bl_description = "Retrieve the number of elements in a geometry for each attribute domain"
    node_58.bl_icon = "NONE"
    node_58.bl_width_default = 140.0
    node_58.bl_width_min = 100.0
    node_58.bl_width_max = 700.0
    node_58.bl_height_default = 100.0
    node_58.bl_height_min = 30.0
    node_58.bl_height_max = 30.0
    node_58.component = "CURVE"

    node_59 = nodes.new("GeometryNodeSwitch")
    node_59.name = "Switch.001"
    node_59.label = ""
    node_59.location = (-3500.0, 200.0)
    node_59.location_absolute = (-3500.0, 200.0)
    node_59.warning_propagation = "ALL"
    node_59.use_custom_color = False
    node_59.show_options = True
    node_59.show_preview = False
    node_59.hide = False
    node_59.mute = False
    node_59.show_texture = False
    node_59.bl_idname = "GeometryNodeSwitch"
    node_59.bl_label = "Switch"
    node_59.bl_description = "Switch between two inputs"
    node_59.bl_icon = "NONE"
    node_59.bl_width_default = 140.0
    node_59.bl_width_min = 100.0
    node_59.bl_width_max = 700.0
    node_59.bl_height_default = 100.0
    node_59.bl_height_min = 30.0
    node_59.bl_height_max = 30.0
    node_59.input_type = "GEOMETRY"

    node_60 = nodes.new("GeometryNodeResampleCurve")
    node_60.name = "Resample Curve.004"
    node_60.label = ""
    node_60.location = (-3700.0, 280.0)
    node_60.location_absolute = (-3700.0, 280.0)
    node_60.warning_propagation = "ALL"
    node_60.use_custom_color = False
    node_60.show_options = True
    node_60.show_preview = False
    node_60.hide = False
    node_60.mute = False
    node_60.show_texture = False
    node_60.bl_idname = "GeometryNodeResampleCurve"
    node_60.bl_label = "Resample Curve"
    node_60.bl_description = "Generate a poly spline for each input spline"
    node_60.bl_icon = "NONE"
    node_60.bl_width_default = 140.0
    node_60.bl_width_min = 100.0
    node_60.bl_width_max = 700.0
    node_60.bl_height_default = 100.0
    node_60.bl_height_min = 30.0
    node_60.bl_height_max = 30.0
    node_60.keep_last_segment = False
    # Selection
    node_60.inputs[1].default_value = True
    # Mode
    node_60.inputs[2].default_value = "Count"
    # Length
    node_60.inputs[4].default_value = 0.10000000149011612

    node_61 = nodes.new("GeometryNodeCurvePrimitiveLine")
    node_61.name = "Curve Line.001"
    node_61.label = ""
    node_61.location = (-3700.0, 120.0)
    node_61.location_absolute = (-3700.0, 120.0)
    node_61.warning_propagation = "ALL"
    node_61.use_custom_color = False
    node_61.show_options = True
    node_61.show_preview = False
    node_61.hide = False
    node_61.mute = False
    node_61.show_texture = False
    node_61.bl_idname = "GeometryNodeCurvePrimitiveLine"
    node_61.bl_label = "Curve Line"
    node_61.bl_description = "Generate a poly spline line with two points"
    node_61.bl_icon = "NONE"
    node_61.bl_width_default = 140.0
    node_61.bl_width_min = 100.0
    node_61.bl_width_max = 700.0
    node_61.bl_height_default = 100.0
    node_61.bl_height_min = 30.0
    node_61.bl_height_max = 30.0
    node_61.mode = "POINTS"
    # Start
    node_61.inputs[0].default_value = (0.0, 0.0, 0.0)
    # End
    node_61.inputs[1].default_value = (0.0, 0.0, 1.0)
    # Direction
    node_61.inputs[2].default_value = <bpy_float[3], NodeSocketVector.default_value>
    # Length
    node_61.inputs[3].default_value = 1.0

    node_62 = nodes.new("NodeGroupInput")
    node_62.name = "Group Input"
    node_62.label = ""
    node_62.location = (-4020.0, 360.0)
    node_62.location_absolute = (-4020.0, 360.0)
    node_62.warning_propagation = "ALL"
    node_62.use_custom_color = False
    node_62.show_options = True
    node_62.show_preview = False
    node_62.hide = False
    node_62.mute = False
    node_62.show_texture = False
    node_62.bl_idname = "NodeGroupInput"
    node_62.bl_label = "Group Input"
    node_62.bl_description = "Expose connected data from inside a node group as inputs to its interface"
    node_62.bl_icon = "NONE"
    node_62.bl_width_default = 140.0
    node_62.bl_width_min = 80.0
    node_62.bl_width_max = 400.0
    node_62.bl_height_default = 100.0
    node_62.bl_height_min = 30.0
    node_62.bl_height_max = 30.0

    node_63 = nodes.new("GeometryNodeSampleIndex")
    node_63.name = "Sample Index"
    node_63.label = ""
    node_63.location = (0.0, 0.0)
    node_63.location_absolute = (0.0, 0.0)
    node_63.warning_propagation = "ALL"
    node_63.use_custom_color = False
    node_63.show_options = True
    node_63.show_preview = False
    node_63.hide = False
    node_63.mute = False
    node_63.show_texture = False
    node_63.bl_idname = "GeometryNodeSampleIndex"
    node_63.bl_label = "Sample Index"
    node_63.bl_description = "Retrieve values from specific geometry elements"
    node_63.bl_icon = "NONE"
    node_63.bl_width_default = 140.0
    node_63.bl_width_min = 100.0
    node_63.bl_width_max = 700.0
    node_63.bl_height_default = 100.0
    node_63.bl_height_min = 30.0
    node_63.bl_height_max = 30.0
    node_63.data_type = "FLOAT_VECTOR"
    node_63.domain = "POINT"
    node_63.clamp = True

    node_64 = nodes.new("GeometryNodeSampleIndex")
    node_64.name = "Sample Index.001"
    node_64.label = ""
    node_64.location = (0.0, 0.0)
    node_64.location_absolute = (0.0, 0.0)
    node_64.warning_propagation = "ALL"
    node_64.use_custom_color = False
    node_64.show_options = True
    node_64.show_preview = False
    node_64.hide = False
    node_64.mute = False
    node_64.show_texture = False
    node_64.bl_idname = "GeometryNodeSampleIndex"
    node_64.bl_label = "Sample Index"
    node_64.bl_description = "Retrieve values from specific geometry elements"
    node_64.bl_icon = "NONE"
    node_64.bl_width_default = 140.0
    node_64.bl_width_min = 100.0
    node_64.bl_width_max = 700.0
    node_64.bl_height_default = 100.0
    node_64.bl_height_min = 30.0
    node_64.bl_height_max = 30.0
    node_64.data_type = "FLOAT_VECTOR"
    node_64.domain = "POINT"
    node_64.clamp = True

    # --- Links ---
    links = group.links
    links.new(node_62.outputs[0], node_60.inputs[0])
    links.new(node_4.outputs[0], node_3.inputs[0])
    links.new(node_62.outputs[2], node_60.inputs[3])
    links.new(node_59.outputs[0], node_63.inputs[0])
    links.new(node_22.outputs[0], node_63.inputs[1])
    links.new(node_3.outputs[0], node_6.inputs[0])
    links.new(node_63.outputs[0], node_6.inputs[2])
    links.new(node_59.outputs[0], node_58.inputs[0])
    links.new(node_58.outputs[4], node_4.inputs[3])
    links.new(node_2.outputs[0], node_1.inputs[0])
    links.new(node_5.outputs[0], node_63.inputs[2])
    links.new(node_55.outputs[0], node_2.inputs[0])
    links.new(node_1.outputs[0], node_5.inputs[0])
    links.new(node_3.outputs[1], node_5.inputs[1])
    links.new(node_56.outputs[0], node_1.inputs[1])
    links.new(node_56.outputs[0], node_3.inputs[2])
    links.new(node_58.outputs[4], node_2.inputs[1])
    links.new(node_48.outputs[0], node_49.inputs[0])
    links.new(node_36.outputs[0], node_52.inputs[0])
    links.new(node_22.outputs[0], node_64.inputs[1])
    links.new(node_62.outputs[3], node_52.inputs[1])
    links.new(node_0.outputs[0], node_40.inputs[0])
    links.new(node_64.outputs[0], node_40.inputs[2])
    links.new(node_58.outputs[4], node_9.inputs[0])
    links.new(node_62.outputs[3], node_10.inputs[0])
    links.new(node_10.outputs[0], node_11.inputs[0])
    links.new(node_9.outputs[0], node_11.inputs[1])
    links.new(node_11.outputs[0], node_12.inputs[0])
    links.new(node_36.outputs[0], node_51.inputs[0])
    links.new(node_51.outputs[0], node_48.inputs[0])
    links.new(node_49.outputs[0], node_50.inputs[0])
    links.new(node_62.outputs[3], node_37.inputs[0])
    links.new(node_37.outputs[0], node_51.inputs[2])
    links.new(node_50.outputs[0], node_45.inputs[1])
    links.new(node_54.outputs[0], node_64.inputs[0])
    links.new(node_6.outputs[0], node_36.inputs[0])
    links.new(node_55.outputs[0], node_15.inputs[0])
    links.new(node_15.outputs[0], node_17.inputs[0])
    links.new(node_12.outputs[0], node_15.inputs[1])
    links.new(node_55.outputs[0], node_18.inputs[0])
    links.new(node_17.outputs[0], node_18.inputs[1])
    links.new(node_55.outputs[0], node_16.inputs[0])
    links.new(node_12.outputs[0], node_16.inputs[1])
    links.new(node_16.outputs[0], node_19.inputs[2])
    links.new(node_12.outputs[0], node_23.inputs[0])
    links.new(node_23.outputs[0], node_19.inputs[3])
    links.new(node_17.outputs[0], node_20.inputs[0])
    links.new(node_23.outputs[0], node_20.inputs[1])
    links.new(node_18.outputs[0], node_21.inputs[1])
    links.new(node_20.outputs[0], node_21.inputs[2])
    links.new(node_19.outputs[0], node_21.inputs[0])
    links.new(node_62.outputs[6], node_36.inputs[2])
    links.new(node_62.outputs[6], node_13.inputs[0])
    links.new(node_13.outputs[0], node_9.inputs[1])
    links.new(node_12.outputs[0], node_14.inputs[3])
    links.new(node_56.outputs[0], node_7.inputs[1])
    links.new(node_56.outputs[0], node_8.inputs[0])
    links.new(node_8.outputs[0], node_7.inputs[2])
    links.new(node_7.outputs[0], node_14.inputs[2])
    links.new(node_56.outputs[0], node_24.inputs[0])
    links.new(node_12.outputs[0], node_24.inputs[1])
    links.new(node_55.outputs[0], node_25.inputs[2])
    links.new(node_24.outputs[0], node_25.inputs[3])
    links.new(node_55.outputs[0], node_26.inputs[0])
    links.new(node_12.outputs[0], node_26.inputs[1])
    links.new(node_62.outputs[5], node_7.inputs[0])
    links.new(node_55.outputs[0], node_34.inputs[1])
    links.new(node_21.outputs[0], node_34.inputs[2])
    links.new(node_62.outputs[6], node_34.inputs[0])
    links.new(node_34.outputs[0], node_35.inputs[1])
    links.new(node_25.outputs[0], node_35.inputs[0])
    links.new(node_26.outputs[0], node_35.inputs[2])
    links.new(node_34.outputs[0], node_29.inputs[1])
    links.new(node_35.outputs[0], node_29.inputs[2])
    links.new(node_62.outputs[5], node_29.inputs[0])
    links.new(node_55.outputs[0], node_30.inputs[2])
    links.new(node_29.outputs[0], node_31.inputs[1])
    links.new(node_30.outputs[0], node_31.inputs[0])
    links.new(node_7.outputs[0], node_33.inputs[0])
    links.new(node_12.outputs[0], node_33.inputs[1])
    links.new(node_33.outputs[0], node_32.inputs[0])
    links.new(node_32.outputs[0], node_30.inputs[3])
    links.new(node_62.outputs[5], node_27.inputs[0])
    links.new(node_62.outputs[6], node_27.inputs[1])
    links.new(node_29.outputs[0], node_28.inputs[1])
    links.new(node_31.outputs[0], node_28.inputs[2])
    links.new(node_28.outputs[0], node_64.inputs[2])
    links.new(node_27.outputs[0], node_28.inputs[0])
    links.new(node_62.outputs[1], node_45.inputs[0])
    links.new(node_61.outputs[0], node_4.inputs[0])
    links.new(node_62.outputs[5], node_43.inputs[0])
    links.new(node_62.outputs[6], node_43.inputs[1])
    links.new(node_43.outputs[0], node_44.inputs[0])
    links.new(node_40.outputs[0], node_41.inputs[0])
    links.new(node_39.outputs[0], node_38.inputs[2])
    links.new(node_38.outputs[0], node_41.inputs[1])
    links.new(node_41.outputs[0], node_44.inputs[2])
    links.new(node_40.outputs[0], node_44.inputs[1])
    links.new(node_44.outputs[0], node_42.inputs[0])
    links.new(node_51.outputs[0], node_47.inputs[0])
    links.new(node_47.outputs[0], node_46.inputs[0])
    links.new(node_46.outputs[0], node_45.inputs[2])
    links.new(node_45.outputs[0], node_54.inputs[1])
    links.new(node_52.outputs[0], node_54.inputs[2])
    links.new(node_62.outputs[1], node_53.inputs[0])
    links.new(node_53.outputs[0], node_54.inputs[0])
    links.new(node_60.outputs[0], node_59.inputs[2])
    links.new(node_62.outputs[0], node_59.inputs[1])
    links.new(node_62.outputs[4], node_59.inputs[0])
    links.new(node_62.outputs[2], node_56.inputs[2])
    links.new(node_62.outputs[4], node_56.inputs[0])
    links.new(node_57.outputs[0], node_56.inputs[1])
    links.new(node_58.outputs[0], node_57.inputs[0])
    links.new(node_58.outputs[4], node_57.inputs[1])
    links.new(node_14.outputs[0], node_0.inputs[0])
    links.new(node_14.outputs[1], node_0.inputs[3])

    auto_layout_nodes(group)
    return group