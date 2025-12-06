import bpy
import math
from mathutils import Vector, Color, Matrix
from procedural_human.utils.node_layout import auto_layout_nodes

def create_maletorso_loft_0_group_group():
    group_name = "MaleTorso_Loft_0_Group"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Curve X (Front)", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Curve Y (Side)", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Resolution V", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 64
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Resolution U", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 32
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(name="Height", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 1.0
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38

    # --- Nodes ---
    nodes = group.nodes
    node_0 = nodes.new("NodeGroupInput")
    node_0.name = "Group Input"
    node_0.label = ""
    node_0.location = (-1400.0, 75.0)
    node_0.location_absolute = (-1400.0, 75.0)
    node_0.warning_propagation = "ALL"
    node_0.use_custom_color = False
    node_0.show_options = True
    node_0.show_preview = False
    node_0.hide = False
    node_0.mute = False
    node_0.show_texture = False
    node_0.bl_idname = "NodeGroupInput"
    node_0.bl_label = "Group Input"
    node_0.bl_description = "Expose connected data from inside a node group as inputs to its interface"
    node_0.bl_icon = "NONE"
    node_0.bl_width_default = 140.0
    node_0.bl_width_min = 80.0
    node_0.bl_width_max = 400.0
    node_0.bl_height_default = 100.0
    node_0.bl_height_min = 30.0
    node_0.bl_height_max = 30.0

    node_1 = nodes.new("GeometryNodeCurveToMesh")
    node_1.name = "Curve to Mesh"
    node_1.label = ""
    node_1.location = (-1150.0, 375.0)
    node_1.location_absolute = (-1150.0, 375.0)
    node_1.warning_propagation = "ALL"
    node_1.use_custom_color = False
    node_1.show_options = True
    node_1.show_preview = False
    node_1.hide = False
    node_1.mute = False
    node_1.show_texture = False
    node_1.bl_idname = "GeometryNodeCurveToMesh"
    node_1.bl_label = "Curve to Mesh"
    node_1.bl_description = "Convert curves into a mesh, optionally with a custom profile shape defined by curves"
    node_1.bl_icon = "NONE"
    node_1.bl_width_default = 140.0
    node_1.bl_width_min = 100.0
    node_1.bl_width_max = 700.0
    node_1.bl_height_default = 100.0
    node_1.bl_height_min = 30.0
    node_1.bl_height_max = 30.0
    # Scale
    node_1.inputs[2].default_value = 1.0
    # Fill Caps
    node_1.inputs[3].default_value = False

    node_2 = nodes.new("GeometryNodeExtrudeMesh")
    node_2.name = "Extrude Mesh"
    node_2.label = ""
    node_2.location = (-900.0, 525.0)
    node_2.location_absolute = (-900.0, 525.0)
    node_2.warning_propagation = "ALL"
    node_2.use_custom_color = False
    node_2.show_options = True
    node_2.show_preview = False
    node_2.hide = False
    node_2.mute = False
    node_2.show_texture = False
    node_2.bl_idname = "GeometryNodeExtrudeMesh"
    node_2.bl_label = "Extrude Mesh"
    node_2.bl_description = "Generate new vertices, edges, or faces from selected elements and move them based on an offset while keeping them connected by their boundary"
    node_2.bl_icon = "NONE"
    node_2.bl_width_default = 140.0
    node_2.bl_width_min = 100.0
    node_2.bl_width_max = 700.0
    node_2.bl_height_default = 100.0
    node_2.bl_height_min = 30.0
    node_2.bl_height_max = 30.0
    node_2.mode = "EDGES"
    # Selection
    node_2.inputs[1].default_value = True
    # Offset
    node_2.inputs[2].default_value = (0.0, 1.0, 0.0)
    # Offset Scale
    node_2.inputs[3].default_value = 54.20000457763672
    # Individual
    node_2.inputs[4].default_value = True

    node_3 = nodes.new("GeometryNodeExtrudeMesh")
    node_3.name = "Extrude Mesh.001"
    node_3.label = ""
    node_3.location = (-902.9901733398438, 389.97705078125)
    node_3.location_absolute = (-902.9901733398438, 389.97705078125)
    node_3.warning_propagation = "ALL"
    node_3.use_custom_color = False
    node_3.show_options = True
    node_3.show_preview = False
    node_3.hide = False
    node_3.mute = False
    node_3.show_texture = False
    node_3.bl_idname = "GeometryNodeExtrudeMesh"
    node_3.bl_label = "Extrude Mesh"
    node_3.bl_description = "Generate new vertices, edges, or faces from selected elements and move them based on an offset while keeping them connected by their boundary"
    node_3.bl_icon = "NONE"
    node_3.bl_width_default = 140.0
    node_3.bl_width_min = 100.0
    node_3.bl_width_max = 700.0
    node_3.bl_height_default = 100.0
    node_3.bl_height_min = 30.0
    node_3.bl_height_max = 30.0
    node_3.mode = "EDGES"
    # Selection
    node_3.inputs[1].default_value = True
    # Offset
    node_3.inputs[2].default_value = (0.0, -1.0, 0.0)
    # Offset Scale
    node_3.inputs[3].default_value = 71.69999694824219
    # Individual
    node_3.inputs[4].default_value = True

    node_4 = nodes.new("GeometryNodeJoinGeometry")
    node_4.name = "Join Geometry"
    node_4.label = ""
    node_4.location = (-650.0, 450.0)
    node_4.location_absolute = (-650.0, 450.0)
    node_4.warning_propagation = "ALL"
    node_4.use_custom_color = False
    node_4.show_options = True
    node_4.show_preview = False
    node_4.hide = False
    node_4.mute = False
    node_4.show_texture = False
    node_4.bl_idname = "GeometryNodeJoinGeometry"
    node_4.bl_label = "Join Geometry"
    node_4.bl_description = "Merge separately generated geometries into a single one"
    node_4.bl_icon = "NONE"
    node_4.bl_width_default = 140.0
    node_4.bl_width_min = 100.0
    node_4.bl_width_max = 700.0
    node_4.bl_height_default = 100.0
    node_4.bl_height_min = 30.0
    node_4.bl_height_max = 30.0

    node_5 = nodes.new("GeometryNodeCurveToMesh")
    node_5.name = "Curve to Mesh.001"
    node_5.label = ""
    node_5.location = (-1158.9703369140625, 225.00003051757812)
    node_5.location_absolute = (-1158.9703369140625, 225.00003051757812)
    node_5.warning_propagation = "ALL"
    node_5.use_custom_color = False
    node_5.show_options = True
    node_5.show_preview = False
    node_5.hide = False
    node_5.mute = False
    node_5.show_texture = False
    node_5.bl_idname = "GeometryNodeCurveToMesh"
    node_5.bl_label = "Curve to Mesh"
    node_5.bl_description = "Convert curves into a mesh, optionally with a custom profile shape defined by curves"
    node_5.bl_icon = "NONE"
    node_5.bl_width_default = 140.0
    node_5.bl_width_min = 100.0
    node_5.bl_width_max = 700.0
    node_5.bl_height_default = 100.0
    node_5.bl_height_min = 30.0
    node_5.bl_height_max = 30.0
    # Scale
    node_5.inputs[2].default_value = 1.0
    # Fill Caps
    node_5.inputs[3].default_value = False

    node_6 = nodes.new("GeometryNodeExtrudeMesh")
    node_6.name = "Extrude Mesh.002"
    node_6.label = ""
    node_6.location = (-898.5049438476562, 242.97216796875)
    node_6.location_absolute = (-898.5049438476562, 242.97216796875)
    node_6.warning_propagation = "ALL"
    node_6.use_custom_color = False
    node_6.show_options = True
    node_6.show_preview = False
    node_6.hide = False
    node_6.mute = False
    node_6.show_texture = False
    node_6.bl_idname = "GeometryNodeExtrudeMesh"
    node_6.bl_label = "Extrude Mesh"
    node_6.bl_description = "Generate new vertices, edges, or faces from selected elements and move them based on an offset while keeping them connected by their boundary"
    node_6.bl_icon = "NONE"
    node_6.bl_width_default = 140.0
    node_6.bl_width_min = 100.0
    node_6.bl_width_max = 700.0
    node_6.bl_height_default = 100.0
    node_6.bl_height_min = 30.0
    node_6.bl_height_max = 30.0
    node_6.mode = "EDGES"
    # Selection
    node_6.inputs[1].default_value = True
    # Offset
    node_6.inputs[2].default_value = (1.0, 0.0, 0.0)
    # Offset Scale
    node_6.inputs[3].default_value = 20.000003814697266
    # Individual
    node_6.inputs[4].default_value = True

    node_7 = nodes.new("GeometryNodeExtrudeMesh")
    node_7.name = "Extrude Mesh.003"
    node_7.label = ""
    node_7.location = (-900.0, 75.0)
    node_7.location_absolute = (-900.0, 75.0)
    node_7.warning_propagation = "ALL"
    node_7.use_custom_color = False
    node_7.show_options = True
    node_7.show_preview = False
    node_7.hide = False
    node_7.mute = False
    node_7.show_texture = False
    node_7.bl_idname = "GeometryNodeExtrudeMesh"
    node_7.bl_label = "Extrude Mesh"
    node_7.bl_description = "Generate new vertices, edges, or faces from selected elements and move them based on an offset while keeping them connected by their boundary"
    node_7.bl_icon = "NONE"
    node_7.bl_width_default = 140.0
    node_7.bl_width_min = 100.0
    node_7.bl_width_max = 700.0
    node_7.bl_height_default = 100.0
    node_7.bl_height_min = 30.0
    node_7.bl_height_max = 30.0
    node_7.mode = "EDGES"
    # Selection
    node_7.inputs[1].default_value = True
    # Offset
    node_7.inputs[2].default_value = (-1.0, 0.0, 0.0)
    # Offset Scale
    node_7.inputs[3].default_value = 20.20000457763672
    # Individual
    node_7.inputs[4].default_value = True

    node_8 = nodes.new("GeometryNodeJoinGeometry")
    node_8.name = "Join Geometry.001"
    node_8.label = ""
    node_8.location = (-654.4851684570312, 274.5391845703125)
    node_8.location_absolute = (-654.4851684570312, 274.5391845703125)
    node_8.warning_propagation = "ALL"
    node_8.use_custom_color = False
    node_8.show_options = True
    node_8.show_preview = False
    node_8.hide = False
    node_8.mute = False
    node_8.show_texture = False
    node_8.bl_idname = "GeometryNodeJoinGeometry"
    node_8.bl_label = "Join Geometry"
    node_8.bl_description = "Merge separately generated geometries into a single one"
    node_8.bl_icon = "NONE"
    node_8.bl_width_default = 140.0
    node_8.bl_width_min = 100.0
    node_8.bl_width_max = 700.0
    node_8.bl_height_default = 100.0
    node_8.bl_height_min = 30.0
    node_8.bl_height_max = 30.0

    node_9 = nodes.new("GeometryNodeBoundBox")
    node_9.name = "Bounding Box"
    node_9.label = ""
    node_9.location = (-1150.0, 75.0)
    node_9.location_absolute = (-1150.0, 75.0)
    node_9.warning_propagation = "ALL"
    node_9.use_custom_color = False
    node_9.show_options = True
    node_9.show_preview = False
    node_9.hide = False
    node_9.mute = False
    node_9.show_texture = False
    node_9.bl_idname = "GeometryNodeBoundBox"
    node_9.bl_label = "Bounding Box"
    node_9.bl_description = "Calculate the limits of a geometry's positions and generate a box mesh with those dimensions"
    node_9.bl_icon = "NONE"
    node_9.bl_width_default = 140.0
    node_9.bl_width_min = 100.0
    node_9.bl_width_max = 700.0
    node_9.bl_height_default = 100.0
    node_9.bl_height_min = 30.0
    node_9.bl_height_max = 30.0
    # Use Radius
    node_9.inputs[1].default_value = True

    node_10 = nodes.new("ShaderNodeSeparateXYZ")
    node_10.name = "Separate XYZ"
    node_10.label = ""
    node_10.location = (-900.0, -75.0)
    node_10.location_absolute = (-900.0, -75.0)
    node_10.warning_propagation = "ALL"
    node_10.use_custom_color = False
    node_10.show_options = True
    node_10.show_preview = False
    node_10.hide = False
    node_10.mute = False
    node_10.show_texture = False
    node_10.bl_idname = "ShaderNodeSeparateXYZ"
    node_10.bl_label = "Separate XYZ"
    node_10.bl_description = "Split a vector into its X, Y, and Z components"
    node_10.bl_icon = "NONE"
    node_10.bl_width_default = 140.0
    node_10.bl_width_min = 100.0
    node_10.bl_width_max = 700.0
    node_10.bl_height_default = 100.0
    node_10.bl_height_min = 30.0
    node_10.bl_height_max = 30.0

    node_11 = nodes.new("GeometryNodeMeshLine")
    node_11.name = "Mesh Line"
    node_11.label = ""
    node_11.location = (-400.0, 450.0)
    node_11.location_absolute = (-400.0, 450.0)
    node_11.warning_propagation = "ALL"
    node_11.use_custom_color = False
    node_11.show_options = True
    node_11.show_preview = False
    node_11.hide = False
    node_11.mute = False
    node_11.show_texture = False
    node_11.bl_idname = "GeometryNodeMeshLine"
    node_11.bl_label = "Mesh Line"
    node_11.bl_description = "Generate vertices in a line and connect them with edges"
    node_11.bl_icon = "NONE"
    node_11.bl_width_default = 140.0
    node_11.bl_width_min = 100.0
    node_11.bl_width_max = 700.0
    node_11.bl_height_default = 100.0
    node_11.bl_height_min = 30.0
    node_11.bl_height_max = 30.0
    node_11.mode = "OFFSET"
    node_11.count_mode = "TOTAL"
    # Resolution
    node_11.inputs[1].default_value = 1.0

    node_12 = nodes.new("ShaderNodeCombineXYZ")
    node_12.name = "Combine XYZ"
    node_12.label = ""
    node_12.location = (-650.0, 150.0)
    node_12.location_absolute = (-650.0, 150.0)
    node_12.warning_propagation = "ALL"
    node_12.use_custom_color = False
    node_12.show_options = True
    node_12.show_preview = False
    node_12.hide = False
    node_12.mute = False
    node_12.show_texture = False
    node_12.bl_idname = "ShaderNodeCombineXYZ"
    node_12.bl_label = "Combine XYZ"
    node_12.bl_description = "Create a vector from X, Y, and Z components"
    node_12.bl_icon = "NONE"
    node_12.bl_width_default = 140.0
    node_12.bl_width_min = 100.0
    node_12.bl_width_max = 700.0
    node_12.bl_height_default = 100.0
    node_12.bl_height_min = 30.0
    node_12.bl_height_max = 30.0
    # X
    node_12.inputs[0].default_value = 0.0
    # Y
    node_12.inputs[1].default_value = 0.0

    node_13 = nodes.new("ShaderNodeCombineXYZ")
    node_13.name = "Combine XYZ.001"
    node_13.label = ""
    node_13.location = (-1150.0, -75.0)
    node_13.location_absolute = (-1150.0, -75.0)
    node_13.warning_propagation = "ALL"
    node_13.use_custom_color = False
    node_13.show_options = True
    node_13.show_preview = False
    node_13.hide = False
    node_13.mute = False
    node_13.show_texture = False
    node_13.bl_idname = "ShaderNodeCombineXYZ"
    node_13.bl_label = "Combine XYZ"
    node_13.bl_description = "Create a vector from X, Y, and Z components"
    node_13.bl_icon = "NONE"
    node_13.bl_width_default = 140.0
    node_13.bl_width_min = 100.0
    node_13.bl_width_max = 700.0
    node_13.bl_height_default = 100.0
    node_13.bl_height_min = 30.0
    node_13.bl_height_max = 30.0
    # X
    node_13.inputs[0].default_value = 0.0
    # Y
    node_13.inputs[1].default_value = 0.0

    node_14 = nodes.new("GeometryNodeMeshToCurve")
    node_14.name = "Mesh to Curve"
    node_14.label = ""
    node_14.location = (-900.0, -225.0)
    node_14.location_absolute = (-900.0, -225.0)
    node_14.warning_propagation = "ALL"
    node_14.use_custom_color = False
    node_14.show_options = True
    node_14.show_preview = False
    node_14.hide = False
    node_14.mute = False
    node_14.show_texture = False
    node_14.bl_idname = "GeometryNodeMeshToCurve"
    node_14.bl_label = "Mesh to Curve"
    node_14.bl_description = "Generate a curve from a mesh"
    node_14.bl_icon = "NONE"
    node_14.bl_width_default = 140.0
    node_14.bl_width_min = 100.0
    node_14.bl_width_max = 700.0
    node_14.bl_height_default = 100.0
    node_14.bl_height_min = 30.0
    node_14.bl_height_max = 30.0
    node_14.mode = "EDGES"
    # Selection
    node_14.inputs[1].default_value = True

    node_15 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    node_15.name = "Curve Circle"
    node_15.label = ""
    node_15.location = (-1152.9901123046875, -235.4837646484375)
    node_15.location_absolute = (-1152.9901123046875, -235.4837646484375)
    node_15.warning_propagation = "ALL"
    node_15.use_custom_color = False
    node_15.show_options = True
    node_15.show_preview = False
    node_15.hide = False
    node_15.mute = False
    node_15.show_texture = False
    node_15.bl_idname = "GeometryNodeCurvePrimitiveCircle"
    node_15.bl_label = "Curve Circle"
    node_15.bl_description = "Generate a poly spline circle"
    node_15.bl_icon = "NONE"
    node_15.bl_width_default = 140.0
    node_15.bl_width_min = 100.0
    node_15.bl_width_max = 700.0
    node_15.bl_height_default = 100.0
    node_15.bl_height_min = 30.0
    node_15.bl_height_max = 30.0
    node_15.mode = "RADIUS"
    # Point 1
    node_15.inputs[1].default_value = (-1.0, 0.0, 0.0)
    # Point 2
    node_15.inputs[2].default_value = (0.0, 1.0, 0.0)
    # Point 3
    node_15.inputs[3].default_value = (1.0, 0.0, 0.0)
    # Radius
    node_15.inputs[4].default_value = 1.0

    node_16 = nodes.new("GeometryNodeCurveToMesh")
    node_16.name = "Curve to Mesh.002"
    node_16.label = ""
    node_16.location = (-650.0, 0.0)
    node_16.location_absolute = (-650.0, 0.0)
    node_16.warning_propagation = "ALL"
    node_16.use_custom_color = False
    node_16.show_options = True
    node_16.show_preview = False
    node_16.hide = False
    node_16.mute = False
    node_16.show_texture = False
    node_16.bl_idname = "GeometryNodeCurveToMesh"
    node_16.bl_label = "Curve to Mesh"
    node_16.bl_description = "Convert curves into a mesh, optionally with a custom profile shape defined by curves"
    node_16.bl_icon = "NONE"
    node_16.bl_width_default = 140.0
    node_16.bl_width_min = 100.0
    node_16.bl_width_max = 700.0
    node_16.bl_height_default = 100.0
    node_16.bl_height_min = 30.0
    node_16.bl_height_max = 30.0
    # Scale
    node_16.inputs[2].default_value = 1.0
    # Fill Caps
    node_16.inputs[3].default_value = False

    node_17 = nodes.new("GeometryNodeInputPosition")
    node_17.name = "Position"
    node_17.label = ""
    node_17.location = (-1400.0, -75.0)
    node_17.location_absolute = (-1400.0, -75.0)
    node_17.warning_propagation = "ALL"
    node_17.use_custom_color = False
    node_17.show_options = True
    node_17.show_preview = False
    node_17.hide = False
    node_17.mute = False
    node_17.show_texture = False
    node_17.bl_idname = "GeometryNodeInputPosition"
    node_17.bl_label = "Position"
    node_17.bl_description = "Retrieve a vector indicating the location of each element"
    node_17.bl_icon = "NONE"
    node_17.bl_width_default = 140.0
    node_17.bl_width_min = 100.0
    node_17.bl_width_max = 700.0
    node_17.bl_height_default = 100.0
    node_17.bl_height_min = 30.0
    node_17.bl_height_max = 30.0

    node_18 = nodes.new("ShaderNodeSeparateXYZ")
    node_18.name = "Separate XYZ.001"
    node_18.label = ""
    node_18.location = (-1150.0, -375.0)
    node_18.location_absolute = (-1150.0, -375.0)
    node_18.warning_propagation = "ALL"
    node_18.use_custom_color = False
    node_18.show_options = True
    node_18.show_preview = False
    node_18.hide = False
    node_18.mute = False
    node_18.show_texture = False
    node_18.bl_idname = "ShaderNodeSeparateXYZ"
    node_18.bl_label = "Separate XYZ"
    node_18.bl_description = "Split a vector into its X, Y, and Z components"
    node_18.bl_icon = "NONE"
    node_18.bl_width_default = 140.0
    node_18.bl_width_min = 100.0
    node_18.bl_width_max = 700.0
    node_18.bl_height_default = 100.0
    node_18.bl_height_min = 30.0
    node_18.bl_height_max = 30.0

    node_19 = nodes.new("ShaderNodeCombineXYZ")
    node_19.name = "Combine XYZ.002"
    node_19.label = ""
    node_19.location = (-900.0, -375.0)
    node_19.location_absolute = (-900.0, -375.0)
    node_19.warning_propagation = "ALL"
    node_19.use_custom_color = False
    node_19.show_options = True
    node_19.show_preview = False
    node_19.hide = False
    node_19.mute = False
    node_19.show_texture = False
    node_19.bl_idname = "ShaderNodeCombineXYZ"
    node_19.bl_label = "Combine XYZ"
    node_19.bl_description = "Create a vector from X, Y, and Z components"
    node_19.bl_icon = "NONE"
    node_19.bl_width_default = 140.0
    node_19.bl_width_min = 100.0
    node_19.bl_width_max = 700.0
    node_19.bl_height_default = 100.0
    node_19.bl_height_min = 30.0
    node_19.bl_height_max = 30.0
    # X
    node_19.inputs[0].default_value = 0.0
    # Y
    node_19.inputs[1].default_value = -0.29999998211860657

    node_20 = nodes.new("GeometryNodeRaycast")
    node_20.name = "Raycast"
    node_20.label = "Measure Rx"
    node_20.location = (-400.0, 300.0)
    node_20.location_absolute = (-400.0, 300.0)
    node_20.warning_propagation = "ALL"
    node_20.use_custom_color = False
    node_20.show_options = True
    node_20.show_preview = False
    node_20.hide = False
    node_20.mute = False
    node_20.show_texture = False
    node_20.bl_idname = "GeometryNodeRaycast"
    node_20.bl_label = "Raycast"
    node_20.bl_description = "Cast rays from the context geometry onto a target geometry, and retrieve information from each hit point"
    node_20.bl_icon = "NONE"
    node_20.bl_width_default = 150.0
    node_20.bl_width_min = 120.0
    node_20.bl_width_max = 700.0
    node_20.bl_height_default = 100.0
    node_20.bl_height_min = 30.0
    node_20.bl_height_max = 30.0
    node_20.data_type = "FLOAT"
    # Attribute
    node_20.inputs[1].default_value = 0.0
    # Interpolation
    node_20.inputs[2].default_value = "Interpolated"
    # Ray Direction
    node_20.inputs[4].default_value = <bpy_float[3], NodeSocketVector.default_value>
    # Ray Length
    node_20.inputs[5].default_value = 1.0

    node_21 = nodes.new("GeometryNodeRaycast")
    node_21.name = "Raycast.001"
    node_21.label = "Measure Ry"
    node_21.location = (-102.48590087890625, 494.46612548828125)
    node_21.location_absolute = (-102.48590087890625, 494.46612548828125)
    node_21.warning_propagation = "ALL"
    node_21.use_custom_color = False
    node_21.show_options = True
    node_21.show_preview = False
    node_21.hide = False
    node_21.mute = False
    node_21.show_texture = False
    node_21.bl_idname = "GeometryNodeRaycast"
    node_21.bl_label = "Raycast"
    node_21.bl_description = "Cast rays from the context geometry onto a target geometry, and retrieve information from each hit point"
    node_21.bl_icon = "NONE"
    node_21.bl_width_default = 150.0
    node_21.bl_width_min = 120.0
    node_21.bl_width_max = 700.0
    node_21.bl_height_default = 100.0
    node_21.bl_height_min = 30.0
    node_21.bl_height_max = 30.0
    node_21.data_type = "FLOAT"
    # Attribute
    node_21.inputs[1].default_value = 0.0
    # Interpolation
    node_21.inputs[2].default_value = "Interpolated"
    # Ray Direction
    node_21.inputs[4].default_value = <bpy_float[3], NodeSocketVector.default_value>
    # Ray Length
    node_21.inputs[5].default_value = 1.0

    node_22 = nodes.new("ShaderNodeMath")
    node_22.name = "Math"
    node_22.label = ""
    node_22.location = (-900.0, -525.0)
    node_22.location_absolute = (-900.0, -525.0)
    node_22.warning_propagation = "ALL"
    node_22.use_custom_color = False
    node_22.show_options = True
    node_22.show_preview = False
    node_22.hide = False
    node_22.mute = False
    node_22.show_texture = False
    node_22.bl_idname = "ShaderNodeMath"
    node_22.bl_label = "Math"
    node_22.bl_description = "Perform math operations"
    node_22.bl_icon = "NONE"
    node_22.bl_width_default = 140.0
    node_22.bl_width_min = 100.0
    node_22.bl_width_max = 700.0
    node_22.bl_height_default = 100.0
    node_22.bl_height_min = 30.0
    node_22.bl_height_max = 30.0
    node_22.operation = "ARCTAN2"
    node_22.use_clamp = False
    # Value
    node_22.inputs[2].default_value = 0.5

    node_23 = nodes.new("ShaderNodeMath")
    node_23.name = "Math.001"
    node_23.label = ""
    node_23.location = (-650.0, -150.0)
    node_23.location_absolute = (-650.0, -150.0)
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
    node_23.operation = "COSINE"
    node_23.use_clamp = False
    # Value
    node_23.inputs[1].default_value = 0.5
    # Value
    node_23.inputs[2].default_value = 0.5

    node_24 = nodes.new("ShaderNodeMath")
    node_24.name = "Math.002"
    node_24.label = ""
    node_24.location = (-650.0, -300.0)
    node_24.location_absolute = (-650.0, -300.0)
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
    node_24.operation = "SINE"
    node_24.use_clamp = False
    # Value
    node_24.inputs[1].default_value = 0.5
    # Value
    node_24.inputs[2].default_value = 0.5

    node_25 = nodes.new("ShaderNodeMath")
    node_25.name = "Math.003"
    node_25.label = ""
    node_25.location = (-400.0, 0.0)
    node_25.location_absolute = (-400.0, 0.0)
    node_25.warning_propagation = "ALL"
    node_25.use_custom_color = False
    node_25.show_options = True
    node_25.show_preview = False
    node_25.hide = False
    node_25.mute = False
    node_25.show_texture = False
    node_25.bl_idname = "ShaderNodeMath"
    node_25.bl_label = "Math"
    node_25.bl_description = "Perform math operations"
    node_25.bl_icon = "NONE"
    node_25.bl_width_default = 140.0
    node_25.bl_width_min = 100.0
    node_25.bl_width_max = 700.0
    node_25.bl_height_default = 100.0
    node_25.bl_height_min = 30.0
    node_25.bl_height_max = 30.0
    node_25.operation = "MULTIPLY"
    node_25.use_clamp = False
    # Value
    node_25.inputs[2].default_value = 0.5

    node_26 = nodes.new("ShaderNodeMath")
    node_26.name = "Math.004"
    node_26.label = ""
    node_26.location = (-150.0, 150.0)
    node_26.location_absolute = (-150.0, 150.0)
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
    node_26.operation = "POWER"
    node_26.use_clamp = False
    # Value
    node_26.inputs[1].default_value = 2.0
    # Value
    node_26.inputs[2].default_value = 0.5

    node_27 = nodes.new("ShaderNodeMath")
    node_27.name = "Math.005"
    node_27.label = ""
    node_27.location = (-400.0, -150.0)
    node_27.location_absolute = (-400.0, -150.0)
    node_27.warning_propagation = "ALL"
    node_27.use_custom_color = False
    node_27.show_options = True
    node_27.show_preview = False
    node_27.hide = False
    node_27.mute = False
    node_27.show_texture = False
    node_27.bl_idname = "ShaderNodeMath"
    node_27.bl_label = "Math"
    node_27.bl_description = "Perform math operations"
    node_27.bl_icon = "NONE"
    node_27.bl_width_default = 140.0
    node_27.bl_width_min = 100.0
    node_27.bl_width_max = 700.0
    node_27.bl_height_default = 100.0
    node_27.bl_height_min = 30.0
    node_27.bl_height_max = 30.0
    node_27.operation = "MULTIPLY"
    node_27.use_clamp = False
    # Value
    node_27.inputs[2].default_value = 0.5

    node_28 = nodes.new("ShaderNodeMath")
    node_28.name = "Math.006"
    node_28.label = ""
    node_28.location = (-150.0, 0.0)
    node_28.location_absolute = (-150.0, 0.0)
    node_28.warning_propagation = "ALL"
    node_28.use_custom_color = False
    node_28.show_options = True
    node_28.show_preview = False
    node_28.hide = False
    node_28.mute = False
    node_28.show_texture = False
    node_28.bl_idname = "ShaderNodeMath"
    node_28.bl_label = "Math"
    node_28.bl_description = "Perform math operations"
    node_28.bl_icon = "NONE"
    node_28.bl_width_default = 140.0
    node_28.bl_width_min = 100.0
    node_28.bl_width_max = 700.0
    node_28.bl_height_default = 100.0
    node_28.bl_height_min = 30.0
    node_28.bl_height_max = 30.0
    node_28.operation = "POWER"
    node_28.use_clamp = False
    # Value
    node_28.inputs[1].default_value = 2.0
    # Value
    node_28.inputs[2].default_value = 0.5

    node_29 = nodes.new("ShaderNodeMath")
    node_29.name = "Math.007"
    node_29.label = ""
    node_29.location = (100.0, 150.0)
    node_29.location_absolute = (100.0, 150.0)
    node_29.warning_propagation = "ALL"
    node_29.use_custom_color = False
    node_29.show_options = True
    node_29.show_preview = False
    node_29.hide = False
    node_29.mute = False
    node_29.show_texture = False
    node_29.bl_idname = "ShaderNodeMath"
    node_29.bl_label = "Math"
    node_29.bl_description = "Perform math operations"
    node_29.bl_icon = "NONE"
    node_29.bl_width_default = 140.0
    node_29.bl_width_min = 100.0
    node_29.bl_width_max = 700.0
    node_29.bl_height_default = 100.0
    node_29.bl_height_min = 30.0
    node_29.bl_height_max = 30.0
    node_29.operation = "ADD"
    node_29.use_clamp = False
    # Value
    node_29.inputs[2].default_value = 0.5

    node_30 = nodes.new("ShaderNodeMath")
    node_30.name = "Math.008"
    node_30.label = ""
    node_30.location = (350.0, 0.0)
    node_30.location_absolute = (350.0, 0.0)
    node_30.warning_propagation = "ALL"
    node_30.use_custom_color = False
    node_30.show_options = True
    node_30.show_preview = False
    node_30.hide = False
    node_30.mute = False
    node_30.show_texture = False
    node_30.bl_idname = "ShaderNodeMath"
    node_30.bl_label = "Math"
    node_30.bl_description = "Perform math operations"
    node_30.bl_icon = "NONE"
    node_30.bl_width_default = 140.0
    node_30.bl_width_min = 100.0
    node_30.bl_width_max = 700.0
    node_30.bl_height_default = 100.0
    node_30.bl_height_min = 30.0
    node_30.bl_height_max = 30.0
    node_30.operation = "ADD"
    node_30.use_clamp = False
    # Value
    node_30.inputs[1].default_value = 0.0
    # Value
    node_30.inputs[2].default_value = 0.5

    node_31 = nodes.new("ShaderNodeMath")
    node_31.name = "Math.009"
    node_31.label = ""
    node_31.location = (600.0, 0.0)
    node_31.location_absolute = (600.0, 0.0)
    node_31.warning_propagation = "ALL"
    node_31.use_custom_color = False
    node_31.show_options = True
    node_31.show_preview = False
    node_31.hide = False
    node_31.mute = False
    node_31.show_texture = False
    node_31.bl_idname = "ShaderNodeMath"
    node_31.bl_label = "Math"
    node_31.bl_description = "Perform math operations"
    node_31.bl_icon = "NONE"
    node_31.bl_width_default = 140.0
    node_31.bl_width_min = 100.0
    node_31.bl_width_max = 700.0
    node_31.bl_height_default = 100.0
    node_31.bl_height_min = 30.0
    node_31.bl_height_max = 30.0
    node_31.operation = "SQRT"
    node_31.use_clamp = False
    # Value
    node_31.inputs[1].default_value = 0.5
    # Value
    node_31.inputs[2].default_value = 0.5

    node_32 = nodes.new("ShaderNodeMath")
    node_32.name = "Math.010"
    node_32.label = ""
    node_32.location = (-400.0, -300.0)
    node_32.location_absolute = (-400.0, -300.0)
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
    node_32.operation = "MULTIPLY"
    node_32.use_clamp = False
    # Value
    node_32.inputs[2].default_value = 0.5

    node_33 = nodes.new("ShaderNodeMath")
    node_33.name = "Math.011"
    node_33.label = ""
    node_33.location = (850.0, 0.0)
    node_33.location_absolute = (850.0, 0.0)
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
    node_33.operation = "DIVIDE"
    node_33.use_clamp = False
    # Value
    node_33.inputs[2].default_value = 0.5

    node_34 = nodes.new("ShaderNodeMath")
    node_34.name = "Math.012"
    node_34.label = ""
    node_34.location = (100.0, 0.0)
    node_34.location_absolute = (100.0, 0.0)
    node_34.warning_propagation = "ALL"
    node_34.use_custom_color = False
    node_34.show_options = True
    node_34.show_preview = False
    node_34.hide = False
    node_34.mute = False
    node_34.show_texture = False
    node_34.bl_idname = "ShaderNodeMath"
    node_34.bl_label = "Math"
    node_34.bl_description = "Perform math operations"
    node_34.bl_icon = "NONE"
    node_34.bl_width_default = 140.0
    node_34.bl_width_min = 100.0
    node_34.bl_width_max = 700.0
    node_34.bl_height_default = 100.0
    node_34.bl_height_min = 30.0
    node_34.bl_height_max = 30.0
    node_34.operation = "MULTIPLY"
    node_34.use_clamp = False
    # Value
    node_34.inputs[2].default_value = 0.5

    node_35 = nodes.new("ShaderNodeMath")
    node_35.name = "Math.013"
    node_35.label = ""
    node_35.location = (100.0, -150.0)
    node_35.location_absolute = (100.0, -150.0)
    node_35.warning_propagation = "ALL"
    node_35.use_custom_color = False
    node_35.show_options = True
    node_35.show_preview = False
    node_35.hide = False
    node_35.mute = False
    node_35.show_texture = False
    node_35.bl_idname = "ShaderNodeMath"
    node_35.bl_label = "Math"
    node_35.bl_description = "Perform math operations"
    node_35.bl_icon = "NONE"
    node_35.bl_width_default = 140.0
    node_35.bl_width_min = 100.0
    node_35.bl_width_max = 700.0
    node_35.bl_height_default = 100.0
    node_35.bl_height_min = 30.0
    node_35.bl_height_max = 30.0
    node_35.operation = "MULTIPLY"
    node_35.use_clamp = False
    # Value
    node_35.inputs[2].default_value = 0.5

    node_36 = nodes.new("ShaderNodeCombineXYZ")
    node_36.name = "Combine XYZ.003"
    node_36.label = ""
    node_36.location = (-150.0, -150.0)
    node_36.location_absolute = (-150.0, -150.0)
    node_36.warning_propagation = "ALL"
    node_36.use_custom_color = False
    node_36.show_options = True
    node_36.show_preview = False
    node_36.hide = False
    node_36.mute = False
    node_36.show_texture = False
    node_36.bl_idname = "ShaderNodeCombineXYZ"
    node_36.bl_label = "Combine XYZ"
    node_36.bl_description = "Create a vector from X, Y, and Z components"
    node_36.bl_icon = "NONE"
    node_36.bl_width_default = 140.0
    node_36.bl_width_min = 100.0
    node_36.bl_width_max = 700.0
    node_36.bl_height_default = 100.0
    node_36.bl_height_min = 30.0
    node_36.bl_height_max = 30.0

    node_37 = nodes.new("GeometryNodeSetPosition")
    node_37.name = "Set Position"
    node_37.label = ""
    node_37.location = (-650.0, -450.0)
    node_37.location_absolute = (-650.0, -450.0)
    node_37.warning_propagation = "ALL"
    node_37.use_custom_color = False
    node_37.show_options = True
    node_37.show_preview = False
    node_37.hide = False
    node_37.mute = False
    node_37.show_texture = False
    node_37.bl_idname = "GeometryNodeSetPosition"
    node_37.bl_label = "Set Position"
    node_37.bl_description = "Set the location of each point"
    node_37.bl_icon = "NONE"
    node_37.bl_width_default = 140.0
    node_37.bl_width_min = 100.0
    node_37.bl_width_max = 700.0
    node_37.bl_height_default = 100.0
    node_37.bl_height_min = 30.0
    node_37.bl_height_max = 30.0
    # Selection
    node_37.inputs[1].default_value = True
    # Offset
    node_37.inputs[3].default_value = (0.0, 0.0, 0.0)

    node_38 = nodes.new("GeometryNodeJoinGeometry")
    node_38.name = "Join Geometry.002"
    node_38.label = ""
    node_38.location = (-400.0, -450.0)
    node_38.location_absolute = (-400.0, -450.0)
    node_38.warning_propagation = "ALL"
    node_38.use_custom_color = False
    node_38.show_options = True
    node_38.show_preview = False
    node_38.hide = False
    node_38.mute = False
    node_38.show_texture = False
    node_38.bl_idname = "GeometryNodeJoinGeometry"
    node_38.bl_label = "Join Geometry"
    node_38.bl_description = "Merge separately generated geometries into a single one"
    node_38.bl_icon = "NONE"
    node_38.bl_width_default = 140.0
    node_38.bl_width_min = 100.0
    node_38.bl_width_max = 700.0
    node_38.bl_height_default = 100.0
    node_38.bl_height_min = 30.0
    node_38.bl_height_max = 30.0

    node_39 = nodes.new("NodeGroupOutput")
    node_39.name = "Group Output"
    node_39.label = ""
    node_39.location = (1100.0, 0.0)
    node_39.location_absolute = (1100.0, 0.0)
    node_39.warning_propagation = "ALL"
    node_39.use_custom_color = False
    node_39.show_options = True
    node_39.show_preview = False
    node_39.hide = False
    node_39.mute = False
    node_39.show_texture = False
    node_39.bl_idname = "NodeGroupOutput"
    node_39.bl_label = "Group Output"
    node_39.bl_description = "Output data from inside of a node group"
    node_39.bl_icon = "NONE"
    node_39.bl_width_default = 140.0
    node_39.bl_width_min = 80.0
    node_39.bl_width_max = 400.0
    node_39.bl_height_default = 100.0
    node_39.bl_height_min = 30.0
    node_39.bl_height_max = 30.0
    node_39.is_active_output = True

    # --- Links ---
    links = group.links
    links.new(node_0.outputs[1], node_1.inputs[0])
    links.new(node_1.outputs[0], node_2.inputs[0])
    links.new(node_1.outputs[0], node_3.inputs[0])
    links.new(node_2.outputs[0], node_4.inputs[0])
    links.new(node_3.outputs[0], node_4.inputs[0])
    links.new(node_0.outputs[2], node_5.inputs[0])
    links.new(node_5.outputs[0], node_6.inputs[0])
    links.new(node_5.outputs[0], node_7.inputs[0])
    links.new(node_6.outputs[0], node_8.inputs[0])
    links.new(node_7.outputs[0], node_8.inputs[0])
    links.new(node_0.outputs[0], node_9.inputs[0])
    links.new(node_9.outputs[2], node_10.inputs[0])
    links.new(node_10.outputs[2], node_12.inputs[2])
    links.new(node_12.outputs[0], node_11.inputs[2])
    links.new(node_0.outputs[5], node_13.inputs[2])
    links.new(node_13.outputs[0], node_11.inputs[3])
    links.new(node_0.outputs[3], node_11.inputs[0])
    links.new(node_11.outputs[0], node_14.inputs[0])
    links.new(node_0.outputs[4], node_15.inputs[0])
    links.new(node_14.outputs[0], node_16.inputs[0])
    links.new(node_15.outputs[0], node_16.inputs[1])
    links.new(node_17.outputs[0], node_18.inputs[0])
    links.new(node_18.outputs[2], node_19.inputs[2])
    links.new(node_4.outputs[0], node_20.inputs[0])
    links.new(node_19.outputs[0], node_20.inputs[3])
    links.new(node_8.outputs[0], node_21.inputs[0])
    links.new(node_19.outputs[0], node_21.inputs[3])
    links.new(node_18.outputs[1], node_22.inputs[0])
    links.new(node_18.outputs[0], node_22.inputs[1])
    links.new(node_22.outputs[0], node_23.inputs[0])
    links.new(node_22.outputs[0], node_24.inputs[0])
    links.new(node_21.outputs[3], node_25.inputs[0])
    links.new(node_23.outputs[0], node_25.inputs[1])
    links.new(node_25.outputs[0], node_26.inputs[0])
    links.new(node_20.outputs[3], node_27.inputs[0])
    links.new(node_24.outputs[0], node_27.inputs[1])
    links.new(node_27.outputs[0], node_28.inputs[0])
    links.new(node_26.outputs[0], node_29.inputs[0])
    links.new(node_28.outputs[0], node_29.inputs[1])
    links.new(node_29.outputs[0], node_30.inputs[0])
    links.new(node_30.outputs[0], node_31.inputs[0])
    links.new(node_20.outputs[3], node_32.inputs[0])
    links.new(node_21.outputs[3], node_32.inputs[1])
    links.new(node_32.outputs[0], node_33.inputs[0])
    links.new(node_31.outputs[0], node_33.inputs[1])
    links.new(node_33.outputs[0], node_34.inputs[0])
    links.new(node_23.outputs[0], node_34.inputs[1])
    links.new(node_33.outputs[0], node_35.inputs[0])
    links.new(node_24.outputs[0], node_35.inputs[1])
    links.new(node_34.outputs[0], node_36.inputs[0])
    links.new(node_35.outputs[0], node_36.inputs[1])
    links.new(node_18.outputs[2], node_36.inputs[2])
    links.new(node_16.outputs[0], node_37.inputs[0])
    links.new(node_36.outputs[0], node_37.inputs[2])
    links.new(node_0.outputs[0], node_38.inputs[0])
    links.new(node_37.outputs[0], node_38.inputs[0])
    links.new(node_38.outputs[0], node_39.inputs[0])

    auto_layout_nodes(group)
    return group