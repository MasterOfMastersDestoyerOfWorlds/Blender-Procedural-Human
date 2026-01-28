import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_segmentation_depth_loft_group():
    group_name = "Segmentation Depth Loft"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Resolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 1000
    socket.min_value = 2
    socket.max_value = 1000
    socket = group.interface.new_socket(name="Value", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.5
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-948.8731689453125, -179.5188446044922)
    group_input.bl_label = "Group Input"
    # Links for group_input

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1477.839111328125, 14.664697647094727)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    image = nodes.new("GeometryNodeInputImage")
    image.name = "Image"
    image.label = ""
    image.location = (-626.608642578125, 146.37478637695312)
    image.bl_label = "Image"
    image.image = <bpy_struct, Image("Debug_Masks_Img") at 0x0000029BF28EAB08>
    # Links for image

    image_texture = nodes.new("GeometryNodeImageTexture")
    image_texture.name = "Image Texture"
    image_texture.label = ""
    image_texture.location = (-337.65728759765625, 211.69757080078125)
    image_texture.bl_label = "Image Texture"
    image_texture.interpolation = "Linear"
    image_texture.extension = "REPEAT"
    # Frame
    image_texture.inputs[2].default_value = 0
    # Links for image_texture
    links.new(image.outputs[0], image_texture.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (-789.1710815429688, 30.515771865844727)
    position.bl_label = "Position"
    # Links for position

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    grid.label = ""
    grid.location = (211.7303466796875, 252.71046447753906)
    grid.bl_label = "Grid"
    # Size X
    grid.inputs[0].default_value = 1.0
    # Size Y
    grid.inputs[1].default_value = 1.0
    # Links for grid

    separate_color = nodes.new("FunctionNodeSeparateColor")
    separate_color.name = "Separate Color"
    separate_color.label = ""
    separate_color.location = (-69.69364166259766, 168.030517578125)
    separate_color.bl_label = "Separate Color"
    separate_color.mode = "RGB"
    # Links for separate_color
    links.new(image_texture.outputs[0], separate_color.inputs[0])

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (475.2337341308594, 231.86721801757812)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "POINT"
    # Links for delete_geometry
    links.new(grid.outputs[0], delete_geometry.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (76.43373107910156, -21.930744171142578)
    math.bl_label = "Math"
    math.operation = "LESS_THAN"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.10000000149011612
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(separate_color.outputs[3], math.inputs[0])
    links.new(math.outputs[0], delete_geometry.inputs[1])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (-596.0537109375, 72.81655883789062)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "ADD"
    # Vector
    vector_math.inputs[1].default_value = [0.5, 0.5, 0.0]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(position.outputs[0], vector_math.inputs[0])
    links.new(vector_math.outputs[0], image_texture.inputs[1])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (-602.8243408203125, -207.2234344482422)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketInt"
    # Links for reroute
    links.new(reroute.outputs[0], grid.inputs[2])
    links.new(group_input.outputs[1], reroute.inputs[0])
    links.new(reroute.outputs[0], grid.inputs[3])

    image_001 = nodes.new("GeometryNodeInputImage")
    image_001.name = "Image.001"
    image_001.label = ""
    image_001.location = (-668.6317138671875, -300.5017395019531)
    image_001.bl_label = "Image"
    image_001.image = <bpy_struct, Image("local_008_Tigre_(1724)_mg_5065_img") at 0x0000029A1DD39D08>
    # Links for image_001

    image_texture_001 = nodes.new("GeometryNodeImageTexture")
    image_texture_001.name = "Image Texture.001"
    image_texture_001.label = ""
    image_texture_001.location = (-339.10552978515625, -340.381103515625)
    image_texture_001.bl_label = "Image Texture"
    image_texture_001.interpolation = "Linear"
    image_texture_001.extension = "REPEAT"
    # Frame
    image_texture_001.inputs[2].default_value = 0
    # Links for image_texture_001
    links.new(image_001.outputs[0], image_texture_001.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (-831.1941528320312, -416.3607482910156)
    position_001.bl_label = "Position"
    # Links for position_001

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (-638.0767822265625, -374.0599670410156)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "ADD"
    # Vector
    vector_math_001.inputs[1].default_value = [0.5, 0.5, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(position_001.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], image_texture_001.inputs[1])

    separate_color_001 = nodes.new("FunctionNodeSeparateColor")
    separate_color_001.name = "Separate Color.001"
    separate_color_001.label = ""
    separate_color_001.location = (-463.2501525878906, -608.1563110351562)
    separate_color_001.bl_label = "Separate Color"
    separate_color_001.mode = "RGB"
    # Links for separate_color_001
    links.new(image_texture_001.outputs[0], separate_color_001.inputs[0])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (668.0772705078125, -84.010009765625)
    combine_x_y_z.bl_label = "Combine XYZ"
    # X
    combine_x_y_z.inputs[0].default_value = 0.0
    # Y
    combine_x_y_z.inputs[1].default_value = 0.0
    # Links for combine_x_y_z

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (497.2205505371094, -147.44219970703125)
    math_001.bl_label = "Math"
    math_001.operation = "MULTIPLY"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(group_input.outputs[2], math_001.inputs[1])
    links.new(math_001.outputs[0], combine_x_y_z.inputs[2])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (1181.41455078125, 33.786346435546875)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Position
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position
    links.new(set_position.outputs[0], group_output.inputs[0])
    links.new(combine_x_y_z.outputs[0], set_position.inputs[3])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (10.109603881835938, -522.9320678710938)
    math_002.bl_label = "Math"
    math_002.operation = "ADD"
    math_002.use_clamp = False
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(separate_color_001.outputs[0], math_002.inputs[0])
    links.new(separate_color_001.outputs[1], math_002.inputs[1])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (137.40257263183594, -643.7979125976562)
    math_003.bl_label = "Math"
    math_003.operation = "ADD"
    math_003.use_clamp = False
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(separate_color_001.outputs[2], math_003.inputs[0])
    links.new(math_002.outputs[0], math_003.inputs[1])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (316.9999694824219, -511.74017333984375)
    math_004.bl_label = "Math"
    math_004.operation = "DIVIDE"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 3.0
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(math_004.outputs[0], math_001.inputs[0])
    links.new(math_003.outputs[0], math_004.inputs[0])

    edge_neighbors = nodes.new("GeometryNodeInputMeshEdgeNeighbors")
    edge_neighbors.name = "Edge Neighbors"
    edge_neighbors.label = ""
    edge_neighbors.location = (440.1933288574219, 356.98333740234375)
    edge_neighbors.bl_label = "Edge Neighbors"
    # Links for edge_neighbors

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (759.6516723632812, 327.6960754394531)
    compare.bl_label = "Compare"
    compare.operation = "NOT_EQUAL"
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
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
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
    links.new(edge_neighbors.outputs[0], compare.inputs[2])

    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.label = ""
    delete_geometry_001.location = (641.482421875, 138.6962432861328)
    delete_geometry_001.bl_label = "Delete Geometry"
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "EDGE"
    # Links for delete_geometry_001
    links.new(compare.outputs[0], delete_geometry_001.inputs[1])
    links.new(delete_geometry.outputs[0], delete_geometry_001.inputs[0])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (821.0001220703125, 112.18274688720703)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Selection
    mesh_to_curve.inputs[1].default_value = True
    # Links for mesh_to_curve
    links.new(delete_geometry_001.outputs[0], mesh_to_curve.inputs[0])

    fill_curve = nodes.new("GeometryNodeFillCurve")
    fill_curve.name = "Fill Curve"
    fill_curve.label = ""
    fill_curve.location = (1001.0, 113.56812286376953)
    fill_curve.bl_label = "Fill Curve"
    # Group ID
    fill_curve.inputs[1].default_value = 0
    # Mode
    fill_curve.inputs[2].default_value = "Triangles"
    # Links for fill_curve
    links.new(fill_curve.outputs[0], set_position.inputs[0])
    links.new(mesh_to_curve.outputs[0], fill_curve.inputs[0])

    auto_layout_nodes(group)
    return group