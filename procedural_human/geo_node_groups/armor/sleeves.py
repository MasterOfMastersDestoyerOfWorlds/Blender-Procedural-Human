import bpy
from mathutils import Vector, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group
from procedural_human.geo_node_groups.utilities.gold_on_band import create_gold_on__band_group
from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group
from procedural_human.geo_node_groups.utilities.space_switch import create_space_res_switch_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group

@geo_node_group
def create_sleeves_group():
    group_name = "Sleeves"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "FLOAT2"
    store_named_attribute.domain = "CORNER"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "UVMap"

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.inputs[1].default_value = "Components"
    transform_geometry_007.inputs[2].default_value = Vector((-0.25, 0.029999999329447746, 0.14999999105930328))
    transform_geometry_007.inputs[3].default_value = Euler((0.06440264731645584, 0.36739179491996765, 0.0), 'XYZ')
    transform_geometry_007.inputs[4].default_value = Vector((1.0, 1.2899999618530273, 1.0))
    links.new(store_named_attribute.outputs[0], transform_geometry_007.inputs[0])

    cone = nodes.new("GeometryNodeMeshCone")
    cone.fill_type = "NONE"
    cone.inputs[0].default_value = 32
    cone.inputs[1].default_value = 26
    cone.inputs[2].default_value = 1
    cone.inputs[3].default_value = 0.05000000074505806
    cone.inputs[4].default_value = 0.03999999910593033
    cone.inputs[5].default_value = 0.14000000059604645
    links.new(cone.outputs[0], store_named_attribute.inputs[0])
    links.new(cone.outputs[4], store_named_attribute.inputs[3])

    frame_011 = nodes.new("NodeFrame")
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.data_type = "FLOAT2"
    store_named_attribute_001.domain = "CORNER"
    store_named_attribute_001.inputs[1].default_value = True
    store_named_attribute_001.inputs[2].default_value = "UVMap"

    transform_geometry_009 = nodes.new("GeometryNodeTransform")
    transform_geometry_009.inputs[1].default_value = "Components"
    transform_geometry_009.inputs[2].default_value = Vector((-0.28999999165534973, -0.04999999701976776, -0.010000007227063179))
    transform_geometry_009.inputs[3].default_value = Euler((-0.47315871715545654, 0.3237585723400116, 0.2094395011663437), 'XYZ')
    transform_geometry_009.inputs[4].default_value = Vector((1.0, 1.2899999618530273, 1.0))

    cone_001 = nodes.new("GeometryNodeMeshCone")
    cone_001.fill_type = "NONE"
    cone_001.inputs[0].default_value = 32
    cone_001.inputs[1].default_value = 29
    cone_001.inputs[2].default_value = 1
    cone_001.inputs[3].default_value = 0.03999999910593033
    cone_001.inputs[4].default_value = 0.029999999329447746
    links.new(cone_001.outputs[4], store_named_attribute_001.inputs[3])
    links.new(cone_001.outputs[0], store_named_attribute_001.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    links.new(transform_geometry_009.outputs[0], join_geometry_009.inputs[0])
    links.new(transform_geometry_007.outputs[0], join_geometry_009.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[1].default_value = True
    set_position_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(set_position_001.outputs[0], transform_geometry_009.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_001.outputs[0], separate_x_y_z_001.inputs[0])

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT"
    map_range_001.inputs[1].default_value = -0.05000000074505806
    map_range_001.inputs[2].default_value = 0.050000011920928955
    map_range_001.inputs[3].default_value = 0.0
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range_001.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range_001.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range_001.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range_001.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(separate_x_y_z_001.outputs[1], map_range_001.inputs[0])

    float_curve_002 = nodes.new("ShaderNodeFloatCurve")
    float_curve_002.inputs[0].default_value = 1.0
    links.new(map_range_001.outputs[0], float_curve_002.inputs[1])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.inputs[0].default_value = 0.0
    combine_x_y_z_001.inputs[1].default_value = 0.0
    links.new(combine_x_y_z_001.outputs[0], set_position_001.inputs[3])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.operation = "MULTIPLY"
    math_002.inputs[1].default_value = 0.029999999329447746
    math_002.inputs[2].default_value = 0.5
    links.new(float_curve_002.outputs[0], math_002.inputs[0])
    links.new(math_002.outputs[0], combine_x_y_z_001.inputs[2])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.mode = "EDGES"
    links.new(cone.outputs[2], mesh_to_curve.inputs[1])
    links.new(transform_geometry_007.outputs[0], mesh_to_curve.inputs[0])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.mode = "EDGES"
    links.new(transform_geometry_009.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(cone_001.outputs[1], mesh_to_curve_001.inputs[1])

    bi_rail_loft = nodes.new("GeometryNodeGroup")
    bi_rail_loft.node_tree = create_bi_rail_loft_group()
    bi_rail_loft.inputs[4].default_value = "Resolution"
    bi_rail_loft.inputs[3].default_value = 82
    bi_rail_loft.inputs[5].default_value = 0.10000000149011612
    bi_rail_loft.inputs[6].default_value = 0.10000000149011612
    bi_rail_loft.inputs[7].default_value = 23
    bi_rail_loft.inputs[8].default_value = 128
    links.new(mesh_to_curve_001.outputs[0], bi_rail_loft.inputs[1])
    links.new(mesh_to_curve.outputs[0], bi_rail_loft.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.inputs[1].default_value = True
    links.new(bi_rail_loft.outputs[0], flip_faces_003.inputs[0])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.inputs[1].default_value = True
    set_position_002.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(flip_faces_003.outputs[0], set_position_002.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.operation = "MULTIPLY_ADD"
    vector_math.inputs[3].default_value = 1.0
    links.new(position_002.outputs[0], vector_math.inputs[2])

    value = nodes.new("ShaderNodeValue")
    links.new(value.outputs[0], vector_math.inputs[1])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.legacy_corner_normals = False
    links.new(normal.outputs[0], vector_math.inputs[0])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.operation = "MULTIPLY_ADD"
    vector_math_001.inputs[3].default_value = 1.0
    links.new(vector_math.outputs[0], vector_math_001.inputs[2])
    links.new(vector_math_001.outputs[0], set_position_002.inputs[2])
    links.new(normal.outputs[0], vector_math_001.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.noise_dimensions = "3D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = False
    noise_texture.inputs[1].default_value = 0.0
    noise_texture.inputs[2].default_value = 13.209991455078125
    noise_texture.inputs[3].default_value = 0.4999999701976776
    noise_texture.inputs[4].default_value = 0.5
    noise_texture.inputs[5].default_value = 2.0
    noise_texture.inputs[6].default_value = 0.0
    noise_texture.inputs[7].default_value = 1.0
    noise_texture.inputs[8].default_value = 0.0

    position_003 = nodes.new("GeometryNodeInputPosition")

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.operation = "MULTIPLY"
    vector_math_002.inputs[1].default_value = [1.0, 1.0, 5.640000343322754]
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[3].default_value = 1.0
    links.new(vector_math_002.outputs[0], noise_texture.inputs[0])

    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    map_range_002.inputs[1].default_value = -1.0
    map_range_002.inputs[2].default_value = 1.0
    map_range_002.inputs[3].default_value = -0.0020000000949949026
    map_range_002.inputs[4].default_value = 0.0010000000474974513
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range_002.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range_002.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(noise_texture.outputs[0], map_range_002.inputs[0])
    links.new(map_range_002.outputs[0], vector_math_001.inputs[1])

    frame_012 = nodes.new("NodeFrame")
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20

    rotate_vector = nodes.new("FunctionNodeRotateVector")
    rotate_vector.inputs[1].default_value = Euler((0.0, -0.42411497235298157, 0.0), 'XYZ')
    links.new(rotate_vector.outputs[0], vector_math_002.inputs[0])
    links.new(position_003.outputs[0], rotate_vector.inputs[0])

    join_geometry_015 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_009.outputs[0], join_geometry_015.inputs[0])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.node_tree = create_pipes_group()
    links.new(pipes.outputs[0], join_geometry_015.inputs[0])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.domain = "FACE"
    set_shade_smooth.inputs[1].default_value = True
    set_shade_smooth.inputs[2].default_value = True
    links.new(set_shade_smooth.outputs[0], group_output.inputs[0])
    links.new(join_geometry_015.outputs[0], set_shade_smooth.inputs[0])

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "POINT"
    store_named_attribute_002.inputs[1].default_value = True
    store_named_attribute_002.inputs[2].default_value = "fabric"
    store_named_attribute_002.inputs[3].default_value = True
    links.new(store_named_attribute_002.outputs[0], join_geometry_015.inputs[0])
    links.new(set_position_002.outputs[0], store_named_attribute_002.inputs[0])

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.inputs[1].default_value = "Components"
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry.outputs[0], set_position_001.inputs[0])
    links.new(store_named_attribute_001.outputs[0], transform_geometry.inputs[0])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.inputs[0].default_value = 0.0
    combine_x_y_z.inputs[1].default_value = 0.0
    links.new(combine_x_y_z.outputs[0], transform_geometry.inputs[2])

    value_001 = nodes.new("ShaderNodeValue")

    value_002 = nodes.new("ShaderNodeValue")

    math = nodes.new("ShaderNodeMath")
    math.operation = "ADD"
    math.inputs[2].default_value = 0.5
    links.new(math.outputs[0], cone_001.inputs[5])
    links.new(value_001.outputs[0], math.inputs[0])
    links.new(value_002.outputs[0], math.inputs[1])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.operation = "MULTIPLY"
    math_001.inputs[1].default_value = -1.0
    math_001.inputs[2].default_value = 0.5
    links.new(value_002.outputs[0], math_001.inputs[0])
    links.new(math_001.outputs[0], combine_x_y_z.inputs[2])

    join_geometry_016 = nodes.new("GeometryNodeJoinGeometry")

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "GEOMETRY"
    links.new(switch.outputs[0], join_geometry_015.inputs[0])
    links.new(join_geometry_016.outputs[0], switch.inputs[2])

    group_input = nodes.new("NodeGroupInput")
    links.new(group_input.outputs[0], switch.inputs[0])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.mode = "FACES"
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    extrude_mesh.inputs[3].default_value = 0.0020000000949949026
    extrude_mesh.inputs[4].default_value = False
    links.new(join_geometry_009.outputs[0], extrude_mesh.inputs[0])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.data_type = "FLOAT_VECTOR"
    named_attribute.inputs[0].default_value = "UVMap"

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    links.new(named_attribute.outputs[0], separate_x_y_z.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "GREATER_THAN"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    compare.inputs[1].default_value = 0.7999999523162842
    compare.inputs[2].default_value = 0
    compare.inputs[3].default_value = 0
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[8].default_value = ""
    compare.inputs[9].default_value = ""
    compare.inputs[10].default_value = 0.8999999761581421
    compare.inputs[11].default_value = 0.08726649731397629
    compare.inputs[12].default_value = 0.0010000000474974513
    links.new(separate_x_y_z.outputs[1], compare.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.operation = "LESS_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    compare_001.inputs[1].default_value = 0.12000000476837158
    compare_001.inputs[2].default_value = 0
    compare_001.inputs[3].default_value = 0
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[8].default_value = ""
    compare_001.inputs[9].default_value = ""
    compare_001.inputs[10].default_value = 0.8999999761581421
    compare_001.inputs[11].default_value = 0.08726649731397629
    compare_001.inputs[12].default_value = 0.0010000000474974513
    links.new(separate_x_y_z.outputs[1], compare_001.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "OR"
    links.new(compare_001.outputs[0], boolean_math.inputs[0])
    links.new(compare.outputs[0], boolean_math.inputs[1])
    links.new(boolean_math.outputs[0], extrude_mesh.inputs[1])

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.domain = "FACE"
    links.new(extrude_mesh.outputs[0], separate_geometry.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry.inputs[1])
    links.new(separate_geometry.outputs[0], pipes.inputs[0])

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.inputs[1].default_value = 100000.0
    gold_on_band.inputs[2].default_value = 1.5699999332427979
    gold_on_band.inputs[3].default_value = 0
    links.new(separate_geometry.outputs[0], gold_on_band.inputs[0])
    links.new(gold_on_band.outputs[0], join_geometry_016.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.text = None
    frame.shrink = True
    frame.label_size = 20

    auto_layout_nodes(group)
    return group