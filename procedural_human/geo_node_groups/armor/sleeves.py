import bpy
from mathutils import Vector, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.utilities.bi_rail import create_bi_rail_loft_group
from procedural_human.geo_node_groups.utilities.space_res_switch import create_space_res_switch_group
from procedural_human.geo_node_groups.utilities.gold_on_band import create_gold_on_band_group

@geo_node_group
def create_sleeves_group():
    group_name = "Sleeves"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2600.0, 300.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (973.5, -35.699920654296875)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "FLOAT2"
    store_named_attribute.domain = "CORNER"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.name = "Transform Geometry.007"
    transform_geometry_007.label = ""
    transform_geometry_007.location = (1153.5, -35.699920654296875)
    transform_geometry_007.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_007.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_007.inputs[2].default_value = Vector((-0.25, 0.029999999329447746, 0.14999999105930328))
    # Rotation
    transform_geometry_007.inputs[3].default_value = Euler((0.06440264731645584, 0.36739179491996765, 0.0), 'XYZ')
    # Scale
    transform_geometry_007.inputs[4].default_value = Vector((1.0, 1.2899999618530273, 1.0))
    # Links for transform_geometry_007
    links.new(store_named_attribute.outputs[0], transform_geometry_007.inputs[0])

    cone = nodes.new("GeometryNodeMeshCone")
    cone.name = "Cone"
    cone.label = ""
    cone.location = (773.5, -35.699920654296875)
    cone.bl_label = "Cone"
    cone.fill_type = "NONE"
    # Vertices
    cone.inputs[0].default_value = 32
    # Side Segments
    cone.inputs[1].default_value = 26
    # Fill Segments
    cone.inputs[2].default_value = 1
    # Radius Top
    cone.inputs[3].default_value = 0.05000000074505806
    # Radius Bottom
    cone.inputs[4].default_value = 0.03999999910593033
    # Depth
    cone.inputs[5].default_value = 0.14000000059604645
    # Links for cone
    links.new(cone.outputs[0], store_named_attribute.inputs[0])
    links.new(cone.outputs[4], store_named_attribute.inputs[3])

    frame_011 = nodes.new("NodeFrame")
    frame_011.name = "Frame.011"
    frame_011.label = "Sleeve"
    frame_011.location = (-2049.0, 417.8000183105469)
    frame_011.bl_label = "Frame"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20
    # Links for frame_011

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (588.9998779296875, -437.8000183105469)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "FLOAT2"
    store_named_attribute_001.domain = "CORNER"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute_001

    transform_geometry_009 = nodes.new("GeometryNodeTransform")
    transform_geometry_009.name = "Transform Geometry.009"
    transform_geometry_009.label = ""
    transform_geometry_009.location = (1449.0, -437.8000183105469)
    transform_geometry_009.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_009.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_009.inputs[2].default_value = Vector((-0.28999999165534973, -0.04999999701976776, -0.010000007227063179))
    # Rotation
    transform_geometry_009.inputs[3].default_value = Euler((-0.47315871715545654, 0.3237585723400116, 0.2094395011663437), 'XYZ')
    # Scale
    transform_geometry_009.inputs[4].default_value = Vector((1.0, 1.2899999618530273, 1.0))
    # Links for transform_geometry_009

    cone_001 = nodes.new("GeometryNodeMeshCone")
    cone_001.name = "Cone.001"
    cone_001.label = ""
    cone_001.location = (388.9998779296875, -437.8000183105469)
    cone_001.bl_label = "Cone"
    cone_001.fill_type = "NONE"
    # Vertices
    cone_001.inputs[0].default_value = 32
    # Side Segments
    cone_001.inputs[1].default_value = 29
    # Fill Segments
    cone_001.inputs[2].default_value = 1
    # Radius Top
    cone_001.inputs[3].default_value = 0.03999999910593033
    # Radius Bottom
    cone_001.inputs[4].default_value = 0.029999999329447746
    # Links for cone_001
    links.new(cone_001.outputs[4], store_named_attribute_001.inputs[3])
    links.new(cone_001.outputs[0], store_named_attribute_001.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_009.name = "Join Geometry.009"
    join_geometry_009.label = ""
    join_geometry_009.location = (2153.5, -35.699920654296875)
    join_geometry_009.bl_label = "Join Geometry"
    # Links for join_geometry_009
    links.new(transform_geometry_009.outputs[0], join_geometry_009.inputs[0])
    links.new(transform_geometry_007.outputs[0], join_geometry_009.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1113.5, -455.6999206542969)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Position
    set_position_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_001
    links.new(set_position_001.outputs[0], transform_geometry_009.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (249.0, -937.800048828125)
    position_001.bl_label = "Position"
    # Links for position_001

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (409.0, -937.800048828125)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001
    links.new(position_001.outputs[0], separate_x_y_z_001.inputs[0])

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.label = ""
    map_range_001.location = (569.0, -937.800048828125)
    map_range_001.bl_label = "Map Range"
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT"
    # From Min
    map_range_001.inputs[1].default_value = -0.05000000074505806
    # From Max
    map_range_001.inputs[2].default_value = 0.050000011920928955
    # To Min
    map_range_001.inputs[3].default_value = 0.0
    # To Max
    map_range_001.inputs[4].default_value = 1.0
    # Steps
    map_range_001.inputs[5].default_value = 4.0
    # Vector
    map_range_001.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_001.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_001.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_001.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_001.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_001
    links.new(separate_x_y_z_001.outputs[1], map_range_001.inputs[0])

    float_curve_002 = nodes.new("ShaderNodeFloatCurve")
    float_curve_002.name = "Float Curve.002"
    float_curve_002.label = ""
    float_curve_002.location = (749.0, -937.800048828125)
    float_curve_002.bl_label = "Float Curve"
    # Factor
    float_curve_002.inputs[0].default_value = 1.0
    # Links for float_curve_002
    links.new(map_range_001.outputs[0], float_curve_002.inputs[1])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (1169.0, -937.800048828125)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # X
    combine_x_y_z_001.inputs[0].default_value = 0.0
    # Y
    combine_x_y_z_001.inputs[1].default_value = 0.0
    # Links for combine_x_y_z_001
    links.new(combine_x_y_z_001.outputs[0], set_position_001.inputs[3])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (1009.0, -937.800048828125)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 0.029999999329447746
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(float_curve_002.outputs[0], math_002.inputs[0])
    links.new(math_002.outputs[0], combine_x_y_z_001.inputs[2])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (89.0, -35.80000305175781)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Links for mesh_to_curve
    links.new(cone.outputs[2], mesh_to_curve.inputs[1])
    links.new(transform_geometry_007.outputs[0], mesh_to_curve.inputs[0])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (129.0, -175.8000030517578)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Links for mesh_to_curve_001
    links.new(transform_geometry_009.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(cone_001.outputs[1], mesh_to_curve_001.inputs[1])

    bi_rail_loft = nodes.new("GeometryNodeGroup")
    bi_rail_loft.name = "Bi-Rail Loft.002"
    bi_rail_loft.label = ""
    bi_rail_loft.location = (309.0, -35.80000305175781)
    bi_rail_loft.node_tree = create_bi_rail_loft_group()
    bi_rail_loft.bl_label = "Group"
    # Smoothing
    bi_rail_loft.inputs[3].default_value = 82
    # Menu
    bi_rail_loft.inputs[4].default_value = "Resolution"
    # X Spacing
    bi_rail_loft.inputs[5].default_value = 0.10000000149011612
    # Y Spacing
    bi_rail_loft.inputs[6].default_value = 0.10000000149011612
    # X Resolution
    bi_rail_loft.inputs[7].default_value = 23
    # Y Resolution
    bi_rail_loft.inputs[8].default_value = 128
    # Links for bi_rail_loft
    links.new(mesh_to_curve_001.outputs[0], bi_rail_loft.inputs[1])
    links.new(mesh_to_curve.outputs[0], bi_rail_loft.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.name = "Flip Faces.003"
    flip_faces_003.label = ""
    flip_faces_003.location = (569.0, -35.80000305175781)
    flip_faces_003.bl_label = "Flip Faces"
    # Selection
    flip_faces_003.inputs[1].default_value = True
    # Links for flip_faces_003
    links.new(bi_rail_loft.outputs[0], flip_faces_003.inputs[0])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (749.0, -35.80000305175781)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Offset
    set_position_002.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_002
    links.new(flip_faces_003.outputs[0], set_position_002.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (189.0, -475.79998779296875)
    position_002.bl_label = "Position"
    # Links for position_002

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (349.0, -355.79998779296875)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "MULTIPLY_ADD"
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(position_002.outputs[0], vector_math.inputs[2])

    value = nodes.new("ShaderNodeValue")
    value.name = "Value"
    value.label = ""
    value.location = (189.0, -415.79998779296875)
    value.bl_label = "Value"
    # Links for value
    links.new(value.outputs[0], vector_math.inputs[1])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.label = ""
    normal.location = (189.0, -355.79998779296875)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = False
    # Links for normal
    links.new(normal.outputs[0], vector_math.inputs[0])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (509.0, -355.79998779296875)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "MULTIPLY_ADD"
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(vector_math.outputs[0], vector_math_001.inputs[2])
    links.new(vector_math_001.outputs[0], set_position_002.inputs[2])
    links.new(normal.outputs[0], vector_math_001.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (349.0, -535.7999877929688)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "3D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = False
    # W
    noise_texture.inputs[1].default_value = 0.0
    # Scale
    noise_texture.inputs[2].default_value = 13.209991455078125
    # Detail
    noise_texture.inputs[3].default_value = 0.4999999701976776
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Offset
    noise_texture.inputs[6].default_value = 0.0
    # Gain
    noise_texture.inputs[7].default_value = 1.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0
    # Links for noise_texture

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (29.0, -535.7999877929688)
    position_003.bl_label = "Position"
    # Links for position_003

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (189.0, -535.7999877929688)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "MULTIPLY"
    # Vector
    vector_math_002.inputs[1].default_value = [1.0, 1.0, 5.640000343322754]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], noise_texture.inputs[0])

    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.name = "Map Range.002"
    map_range_002.label = ""
    map_range_002.location = (509.0, -535.7999877929688)
    map_range_002.bl_label = "Map Range"
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    # From Min
    map_range_002.inputs[1].default_value = -1.0
    # From Max
    map_range_002.inputs[2].default_value = 1.0
    # To Min
    map_range_002.inputs[3].default_value = -0.0020000000949949026
    # To Max
    map_range_002.inputs[4].default_value = 0.0010000000474974513
    # Steps
    map_range_002.inputs[5].default_value = 4.0
    # Vector
    map_range_002.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_002.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_002.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_002.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_002.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_002.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_002
    links.new(noise_texture.outputs[0], map_range_002.inputs[0])
    links.new(map_range_002.outputs[0], vector_math_001.inputs[1])

    frame_012 = nodes.new("NodeFrame")
    frame_012.name = "Frame.012"
    frame_012.label = "Inner Sleeve"
    frame_012.location = (471.0, 175.8000030517578)
    frame_012.bl_label = "Frame"
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20
    # Links for frame_012

    rotate_vector = nodes.new("FunctionNodeRotateVector")
    rotate_vector.name = "Rotate Vector"
    rotate_vector.label = ""
    rotate_vector.location = (29.0, -595.7999877929688)
    rotate_vector.bl_label = "Rotate Vector"
    # Rotation
    rotate_vector.inputs[1].default_value = Euler((0.0, -0.42411497235298157, 0.0), 'XYZ')
    # Links for rotate_vector
    links.new(rotate_vector.outputs[0], vector_math_002.inputs[0])
    links.new(position_003.outputs[0], rotate_vector.inputs[0])

    join_geometry_015 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_015.name = "Join Geometry.015"
    join_geometry_015.label = ""
    join_geometry_015.location = (1920.0, 380.0)
    join_geometry_015.bl_label = "Join Geometry"
    # Links for join_geometry_015
    links.new(join_geometry_009.outputs[0], join_geometry_015.inputs[0])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.name = "Pipes"
    pipes.label = ""
    pipes.location = (1149.0, -235.79998779296875)
    pipes.node_tree = create_pipes_group()
    pipes.bl_label = "Group"
    # Links for pipes
    links.new(pipes.outputs[0], join_geometry_015.inputs[0])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (2300.0, 300.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True
    # Links for set_shade_smooth
    links.new(set_shade_smooth.outputs[0], group_output.inputs[0])
    links.new(join_geometry_015.outputs[0], set_shade_smooth.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (929.0, -35.80000305175781)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "fabric"
    # Value
    store_named_attribute_002.inputs[3].default_value = True
    # Links for store_named_attribute_002
    links.new(store_named_attribute_002.outputs[0], join_geometry_015.inputs[0])
    links.new(set_position_002.outputs[0], store_named_attribute_002.inputs[0])

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (768.9998779296875, -437.8000183105469)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry
    links.new(transform_geometry.outputs[0], set_position_001.inputs[0])
    links.new(store_named_attribute_001.outputs[0], transform_geometry.inputs[0])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (349.0, -737.800048828125)
    combine_x_y_z.bl_label = "Combine XYZ"
    # X
    combine_x_y_z.inputs[0].default_value = 0.0
    # Y
    combine_x_y_z.inputs[1].default_value = 0.0
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], transform_geometry.inputs[2])

    value_001 = nodes.new("ShaderNodeValue")
    value_001.name = "Value.001"
    value_001.label = ""
    value_001.location = (29.0, -637.800048828125)
    value_001.bl_label = "Value"
    # Links for value_001

    value_002 = nodes.new("ShaderNodeValue")
    value_002.name = "Value.002"
    value_002.label = "Longer"
    value_002.location = (29.0, -737.800048828125)
    value_002.bl_label = "Value"
    # Links for value_002

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (189.0, -637.800048828125)
    math.bl_label = "Math"
    math.operation = "ADD"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(math.outputs[0], cone_001.inputs[5])
    links.new(value_001.outputs[0], math.inputs[0])
    links.new(value_002.outputs[0], math.inputs[1])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (189.0, -677.800048828125)
    math_001.bl_label = "Math"
    math_001.operation = "MULTIPLY"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = -1.0
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(value_002.outputs[0], math_001.inputs[0])
    links.new(math_001.outputs[0], combine_x_y_z.inputs[2])

    join_geometry_016 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_016.name = "Join Geometry.016"
    join_geometry_016.label = ""
    join_geometry_016.location = (1400.0, 720.0)
    join_geometry_016.bl_label = "Join Geometry"
    # Links for join_geometry_016

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (1640.0, 640.0)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(switch.outputs[0], join_geometry_015.inputs[0])
    links.new(join_geometry_016.outputs[0], switch.inputs[2])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (1640.0, 700.0)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch.inputs[0])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.label = ""
    extrude_mesh.location = (729.0, -135.79998779296875)
    extrude_mesh.bl_label = "Extrude Mesh"
    extrude_mesh.mode = "FACES"
    # Offset
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.0020000000949949026
    # Individual
    extrude_mesh.inputs[4].default_value = False
    # Links for extrude_mesh
    links.new(join_geometry_009.outputs[0], extrude_mesh.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (29.0, -195.79998779296875)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "FLOAT_VECTOR"
    # Name
    named_attribute.inputs[0].default_value = "UVMap"
    # Links for named_attribute

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (189.0, -195.79998779296875)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(named_attribute.outputs[0], separate_x_y_z.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (349.0, -195.79998779296875)
    compare.bl_label = "Compare"
    compare.operation = "GREATER_THAN"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.7999999523162842
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
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
    links.new(separate_x_y_z.outputs[1], compare.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (349.0, -35.79998779296875)
    compare_001.bl_label = "Compare"
    compare_001.operation = "LESS_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = 0.12000000476837158
    # A
    compare_001.inputs[2].default_value = 0
    # B
    compare_001.inputs[3].default_value = 0
    # A
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_001.inputs[8].default_value = ""
    # B
    compare_001.inputs[9].default_value = ""
    # C
    compare_001.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_001.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_001.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_001
    links.new(separate_x_y_z.outputs[1], compare_001.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (549.0, -115.79998779296875)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "OR"
    # Links for boolean_math
    links.new(compare_001.outputs[0], boolean_math.inputs[0])
    links.new(compare.outputs[0], boolean_math.inputs[1])
    links.new(boolean_math.outputs[0], extrude_mesh.inputs[1])

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (946.683837890625, -156.7991943359375)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "FACE"
    # Links for separate_geometry
    links.new(extrude_mesh.outputs[0], separate_geometry.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry.inputs[1])
    links.new(separate_geometry.outputs[0], pipes.inputs[0])

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.name = "Gold on Band"
    gold_on_band.label = ""
    gold_on_band.location = (1149.0, -55.79998779296875)
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.bl_label = "Group"
    # Density
    gold_on_band.inputs[1].default_value = 100000.0
    # W
    gold_on_band.inputs[2].default_value = 1.5699999332427979
    # Seed
    gold_on_band.inputs[3].default_value = 0
    # Links for gold_on_band
    links.new(separate_geometry.outputs[0], gold_on_band.inputs[0])
    links.new(gold_on_band.outputs[0], join_geometry_016.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Gold"
    frame.location = (-249.0, 875.7999877929688)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    auto_layout_nodes(group)
    return group