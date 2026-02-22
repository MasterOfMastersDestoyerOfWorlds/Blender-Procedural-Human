import bpy
from procedural_human.decorators.geo_node_decorator import geo_node_group
from mathutils import Euler, Vector
from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group
from procedural_human.geo_node_groups.utilities.gem_in_holder import create_gem_in__holder_group
from procedural_human.geo_node_groups.utilities.gold_decorations import create_gold__decorations_group
from procedural_human.geo_node_groups.utilities.gold_on_band import create_gold_on__band_group
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group
from procedural_human.geo_node_groups.utilities.join_splines import create_join__splines_group
from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group
from procedural_human.geo_node_groups.utilities.rivet import create_rivet_group
from procedural_human.geo_node_groups.utilities.swap_attr import create_swap__attr_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, vec_math_op
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_neck_necklace_link_f018_group():
    group_name = "Neck_necklace_link_f018"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    curve_circle_002 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_002.mode = "RADIUS"
    curve_circle_002.inputs[0].default_value = 64
    curve_circle_002.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_002.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_002.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_002.inputs[4].default_value = 0.12999999523162842


    transform_geometry_012 = nodes.new("GeometryNodeTransform")
    transform_geometry_012.inputs[1].default_value = "Components"
    transform_geometry_012.inputs[2].default_value = Vector((0.009999999776482582, -0.03999999910593033, 0.46000000834465027))
    transform_geometry_012.inputs[3].default_value = Euler((-0.027925267815589905, 0.0, 0.15533429384231567), 'XYZ')
    transform_geometry_012.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.inputs[1].default_value = True


    position_003 = nodes.new("GeometryNodeInputPosition")


    separate_x_y_z_005 = nodes.new("ShaderNodeSeparateXYZ")


    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT"
    map_range_001.inputs[1].default_value = 0.12999999523162842
    map_range_001.inputs[2].default_value = -0.12999999523162842
    map_range_001.inputs[3].default_value = 0.0
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range_001.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range_001.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range_001.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range_001.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]


    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.inputs[0].default_value = 1.0


    math_002 = nodes.new("ShaderNodeMath")
    math_002.operation = "MULTIPLY"
    math_002.inputs[1].default_value = -0.29999998211860657
    math_002.inputs[2].default_value = 0.5


    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.inputs[0].default_value = 0.0


    position_005 = nodes.new("GeometryNodeInputPosition")


    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.operation = "MULTIPLY"
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[3].default_value = 1.0


    combine_x_y_z_002 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_002.inputs[1].default_value = 1.0
    combine_x_y_z_002.inputs[2].default_value = 1.0


    float_curve_002 = nodes.new("ShaderNodeFloatCurve")
    float_curve_002.inputs[0].default_value = 1.0


    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Length"
    resample_curve.inputs[3].default_value = 10
    resample_curve.inputs[4].default_value = 0.014999999664723873


    instance_on_points_002 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.inputs[1].default_value = True
    instance_on_points_002.inputs[3].default_value = False
    instance_on_points_002.inputs[4].default_value = 0
    instance_on_points_002.inputs[6].default_value = Vector((0.699999988079071, 0.699999988079071, 0.699999988079071))


    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector.inputs[1].default_value = 1.0


    curve_tangent_001 = nodes.new("GeometryNodeInputTangent")


    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.axis = "Y"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    align_rotation_to_vector_001.inputs[1].default_value = 1.0


    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.legacy_corner_normals = False


    rotate_rotation_003 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_003.rotation_space = "LOCAL"
    rotate_rotation_003.inputs[1].default_value = Euler((0.23108159005641937, 0.14137165248394012, 0.0), 'XYZ')


    spline_parameter = nodes.new("GeometryNodeSplineParameter")


    math_003 = nodes.new("ShaderNodeMath")
    math_003.operation = "SUBTRACT"
    math_003.inputs[1].default_value = 0.7400000095367432
    math_003.inputs[2].default_value = 0.5


    math_004 = nodes.new("ShaderNodeMath")
    math_004.operation = "ABSOLUTE"
    math_004.inputs[1].default_value = 0.7400000095367432
    math_004.inputs[2].default_value = 0.5


    set_curve_tilt_002 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_002.inputs[1].default_value = True


    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    map_range_002.inputs[1].default_value = 0.0
    map_range_002.inputs[2].default_value = 0.08000002801418304
    map_range_002.inputs[3].default_value = 0.6799999475479126
    map_range_002.inputs[4].default_value = 0.47999998927116394
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range_002.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range_002.inputs[11].default_value = [4.0, 4.0, 4.0]


    float_curve_003 = nodes.new("ShaderNodeFloatCurve")
    float_curve_003.inputs[0].default_value = 1.0


    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")


    math_005 = nodes.new("ShaderNodeMath")
    math_005.operation = "MULTIPLY"
    math_005.inputs[1].default_value = 0.014999999664723873
    math_005.inputs[2].default_value = 0.5


    curve_circle_003 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.mode = "RADIUS"
    curve_circle_003.inputs[0].default_value = 20
    curve_circle_003.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_003.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_003.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_003.inputs[4].default_value = 0.014999999664723873


    instance_on_points_003 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.inputs[1].default_value = True
    instance_on_points_003.inputs[3].default_value = False
    instance_on_points_003.inputs[4].default_value = 0
    instance_on_points_003.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_003.inputs[6].default_value = Vector((1.0, 1.0, 1.0))


    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.inputs[0].default_value = 0.0020000000949949026
    ico_sphere_001.inputs[1].default_value = 1


    cylinder_001 = nodes.new("GeometryNodeMeshCylinder")
    cylinder_001.fill_type = "NGON"
    cylinder_001.inputs[0].default_value = 10
    cylinder_001.inputs[1].default_value = 1
    cylinder_001.inputs[2].default_value = 1
    cylinder_001.inputs[3].default_value = 0.014999999664723873
    cylinder_001.inputs[4].default_value = 0.0020000000949949026


    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")


    ico_sphere_002 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_002.inputs[0].default_value = 0.012000000104308128
    ico_sphere_002.inputs[1].default_value = 2


    transform_geometry_013 = nodes.new("GeometryNodeTransform")
    transform_geometry_013.inputs[1].default_value = "Components"
    transform_geometry_013.inputs[2].default_value = Vector((-0.006000000052154064, 0.0, 0.0010000000474974513))
    transform_geometry_013.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_013.inputs[4].default_value = Vector((0.4699999988079071, 0.8600000143051147, 0.05000000074505806))


    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.inputs[1].default_value = True
    set_position_003.inputs[2].default_value = [0.0, 0.0, 0.0]


    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.operation = "SCALE"
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[3].default_value = 0.004999999888241291


    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = False
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    noise_texture.inputs[1].default_value = 60.499996185302734
    noise_texture.inputs[2].default_value = 29.089996337890625
    noise_texture.inputs[3].default_value = 2.0
    noise_texture.inputs[4].default_value = 0.5
    noise_texture.inputs[5].default_value = 2.0
    noise_texture.inputs[6].default_value = 0.0
    noise_texture.inputs[7].default_value = 1.0
    noise_texture.inputs[8].default_value = 0.0


    transform_geometry_014 = nodes.new("GeometryNodeTransform")
    transform_geometry_014.inputs[1].default_value = "Components"
    transform_geometry_014.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_014.inputs[3].default_value = Euler((0.0, 0.0, 3.1415927410125732), 'XYZ')
    transform_geometry_014.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    frame_002 = nodes.new("NodeFrame")
    frame_002.label = "Necklace Link"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20


    rotate_rotation_004 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_004.rotation_space = "LOCAL"
    rotate_rotation_004.inputs[1].default_value = Euler((3.1415927410125732, 0.0, 1.5707963705062866), 'XYZ')


    ico_sphere_003 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_003.inputs[0].default_value = 0.004999999888241291
    ico_sphere_003.inputs[1].default_value = 1


    frame_003 = nodes.new("NodeFrame")
    frame_003.label = "Align"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20


    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    store_named_attribute_004.inputs[1].default_value = True
    store_named_attribute_004.inputs[2].default_value = "gold"
    store_named_attribute_004.inputs[3].default_value = True


    cylinder_002 = nodes.new("GeometryNodeMeshCylinder")
    cylinder_002.fill_type = "NGON"
    cylinder_002.inputs[0].default_value = 16
    cylinder_002.inputs[1].default_value = 1
    cylinder_002.inputs[2].default_value = 1
    cylinder_002.inputs[3].default_value = 0.019999999552965164
    cylinder_002.inputs[4].default_value = 0.0020000000949949026


    math_006 = nodes.new("ShaderNodeMath")
    math_006.operation = "ADD"
    math_006.inputs[2].default_value = 0.5


    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")


    float_curve_004 = nodes.new("ShaderNodeFloatCurve")
    float_curve_004.inputs[0].default_value = 1.0


    set_position_004 = nodes.new("GeometryNodeSetPosition")
    set_position_004.inputs[1].default_value = True
    set_position_004.inputs[2].default_value = [0.0, 0.0, 0.0]


    position_006 = nodes.new("GeometryNodeInputPosition")


    separate_x_y_z_006 = nodes.new("ShaderNodeSeparateXYZ")


    math_007 = nodes.new("ShaderNodeMath")
    math_007.operation = "ABSOLUTE"
    math_007.inputs[1].default_value = 0.5
    math_007.inputs[2].default_value = 0.5


    combine_x_y_z_003 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_003.inputs[0].default_value = 0.0
    combine_x_y_z_003.inputs[2].default_value = 0.0


    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.clamp = True
    map_range_003.interpolation_type = "LINEAR"
    map_range_003.data_type = "FLOAT"
    map_range_003.inputs[1].default_value = -0.019999999552965164
    map_range_003.inputs[2].default_value = 0.019999999552965164
    map_range_003.inputs[3].default_value = 0.7999999523162842
    map_range_003.inputs[4].default_value = 0.19999998807907104
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range_003.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range_003.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range_003.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range_003.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range_003.inputs[11].default_value = [4.0, 4.0, 4.0]


    math_008 = nodes.new("ShaderNodeMath")
    math_008.operation = "MULTIPLY"
    math_008.inputs[2].default_value = 0.5


    boolean_math_004 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.operation = "AND"


    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.mode = "EDGES"


    ico_sphere_004 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_004.inputs[0].default_value = 0.0020000000949949026
    ico_sphere_004.inputs[1].default_value = 1


    instance_on_points_004 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_004.inputs[1].default_value = True
    instance_on_points_004.inputs[3].default_value = False
    instance_on_points_004.inputs[4].default_value = 0
    instance_on_points_004.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_004.inputs[6].default_value = Vector((1.0, 1.0, 1.0))


    transform_geometry_015 = nodes.new("GeometryNodeTransform")
    transform_geometry_015.inputs[1].default_value = "Components"
    transform_geometry_015.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    transform_geometry_015.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_015.inputs[4].default_value = Vector((2.0, 1.0, 0.30000001192092896))


    ico_sphere_005 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_005.inputs[0].default_value = 0.004999999888241291
    ico_sphere_005.inputs[1].default_value = 2


    dual_mesh = nodes.new("GeometryNodeDualMesh")
    dual_mesh.inputs[1].default_value = False


    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")


    transform_geometry_016 = nodes.new("GeometryNodeTransform")
    transform_geometry_016.inputs[1].default_value = "Components"
    transform_geometry_016.inputs[2].default_value = Vector((0.0, 0.003000000026077032, 0.0))
    transform_geometry_016.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_016.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    transform_geometry_017 = nodes.new("GeometryNodeTransform")
    transform_geometry_017.inputs[1].default_value = "Components"
    transform_geometry_017.inputs[2].default_value = Vector((-0.009999999776482582, 0.009999999776482582, 0.0))
    transform_geometry_017.inputs[3].default_value = Euler((0.0, 0.0, 1.0471975803375244), 'XYZ')
    transform_geometry_017.inputs[4].default_value = Vector((0.6000000238418579, 0.6000000238418579, 1.0))


    transform_geometry_018 = nodes.new("GeometryNodeTransform")
    transform_geometry_018.inputs[1].default_value = "Components"
    transform_geometry_018.inputs[2].default_value = Vector((0.009999999776482582, 0.009999999776482582, 0.0))
    transform_geometry_018.inputs[3].default_value = Euler((0.0, 0.0, -1.0471975803375244), 'XYZ')
    transform_geometry_018.inputs[4].default_value = Vector((0.6000000238418579, 0.6000000238418579, 1.0))


    transform_geometry_019 = nodes.new("GeometryNodeTransform")
    transform_geometry_019.inputs[1].default_value = "Components"
    transform_geometry_019.inputs[2].default_value = Vector((0.0, -0.012000000104308128, 0.0))
    transform_geometry_019.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_019.inputs[4].default_value = Vector((0.30000001192092896, 0.6000000238418579, 1.0))


    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")


    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.data_type = "BOOLEAN"
    store_named_attribute_005.domain = "POINT"
    store_named_attribute_005.inputs[1].default_value = True
    store_named_attribute_005.inputs[2].default_value = "ruby"
    store_named_attribute_005.inputs[3].default_value = True


    join_geometry_010 = nodes.new("GeometryNodeJoinGeometry")


    store_named_attribute_006 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_006.data_type = "BOOLEAN"
    store_named_attribute_006.domain = "POINT"
    store_named_attribute_006.inputs[1].default_value = True
    store_named_attribute_006.inputs[2].default_value = "gold"
    store_named_attribute_006.inputs[3].default_value = True


    frame_004 = nodes.new("NodeFrame")
    frame_004.label = "Pendant"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20


    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = True
    sample_curve.data_type = "FLOAT"
    sample_curve.inputs[1].default_value = 0.0
    sample_curve.inputs[2].default_value = 0.6780651807785034
    sample_curve.inputs[3].default_value = 0.0
    sample_curve.inputs[4].default_value = 0


    transform_geometry_020 = nodes.new("GeometryNodeTransform")
    transform_geometry_020.inputs[1].default_value = "Components"
    transform_geometry_020.inputs[3].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')
    transform_geometry_020.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    join_geometry_011 = nodes.new("GeometryNodeJoinGeometry")


    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.operation = "ADD"
    vector_math_003.inputs[1].default_value = [0.0, -0.003000000026077032, -0.019999999552965164]
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_003.inputs[3].default_value = 1.0


    float_curve_005 = nodes.new("ShaderNodeFloatCurve")
    float_curve_005.inputs[0].default_value = 1.0


    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")


    math_009 = nodes.new("ShaderNodeMath")
    math_009.operation = "MULTIPLY"
    math_009.inputs[1].default_value = -0.014999999664723873
    math_009.inputs[2].default_value = 0.5


    math_010 = nodes.new("ShaderNodeMath")
    math_010.operation = "ADD"
    math_010.inputs[2].default_value = 0.5


    frame_018 = nodes.new("NodeFrame")
    frame_018.label = "Necklace 1"
    frame_018.text = None
    frame_018.shrink = True
    frame_018.label_size = 20


    transform_geometry_040 = nodes.new("GeometryNodeTransform")
    transform_geometry_040.inputs[1].default_value = "Components"
    transform_geometry_040.inputs[2].default_value = Vector((0.0, 0.0, 0.0007999999797903001))
    transform_geometry_040.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_040.inputs[4].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))


    transform_geometry_041 = nodes.new("GeometryNodeTransform")
    transform_geometry_041.inputs[1].default_value = "Components"
    transform_geometry_041.inputs[2].default_value = Vector((0.0, 0.0, 0.0007999999797903001))
    transform_geometry_041.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_041.inputs[4].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))


    scale_elements = nodes.new("GeometryNodeScaleElements")
    scale_elements.domain = "FACE"
    scale_elements.inputs[1].default_value = True
    scale_elements.inputs[2].default_value = 1.2000000476837158
    scale_elements.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    scale_elements.inputs[4].default_value = "Uniform"
    scale_elements.inputs[5].default_value = [1.0, 0.0, 0.0]


    transform_geometry_042 = nodes.new("GeometryNodeTransform")
    transform_geometry_042.inputs[1].default_value = "Components"
    transform_geometry_042.inputs[2].default_value = Vector((0.0, 0.0, 0.0005000000237487257))
    transform_geometry_042.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_042.inputs[4].default_value = Vector((1.0, 1.0, 0.7000000476837158))


    join_geometry_023 = nodes.new("GeometryNodeJoinGeometry")


    transform_geometry_043 = nodes.new("GeometryNodeTransform")
    transform_geometry_043.inputs[1].default_value = "Components"
    transform_geometry_043.inputs[2].default_value = Vector((0.0, 0.0, 0.0005000000237487257))
    transform_geometry_043.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_043.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    # Parent assignments
    align_rotation_to_vector.parent = frame_003
    align_rotation_to_vector_001.parent = frame_003
    boolean_math_004.parent = frame_004
    combine_x_y_z_001.parent = frame_018
    combine_x_y_z_002.parent = frame_018
    combine_x_y_z_003.parent = frame_004
    curve_circle_002.parent = frame_018
    curve_circle_003.parent = frame_002
    curve_tangent_001.parent = frame_003
    cylinder_001.parent = frame_002
    cylinder_002.parent = frame_004
    dual_mesh.parent = frame_004
    float_curve.parent = frame_018
    float_curve_002.parent = frame_018
    float_curve_003.parent = frame_018
    float_curve_004.parent = frame_018
    float_curve_005.parent = frame_018
    frame_002.parent = frame_018
    frame_003.parent = frame_018
    frame_004.parent = frame_018
    ico_sphere_001.parent = frame_002
    ico_sphere_002.parent = frame_002
    ico_sphere_003.parent = frame_002
    ico_sphere_004.parent = frame_004
    ico_sphere_005.parent = frame_004
    instance_on_points_002.parent = frame_018
    instance_on_points_003.parent = frame_002
    instance_on_points_004.parent = frame_004
    join_geometry_003.parent = frame_002
    join_geometry_007.parent = frame_004
    join_geometry_009.parent = frame_004
    join_geometry_010.parent = frame_004
    join_geometry_011.parent = frame_018
    join_geometry_023.parent = frame_004
    map_range_001.parent = frame_018
    map_range_002.parent = frame_018
    map_range_003.parent = frame_004
    math_002.parent = frame_018
    math_003.parent = frame_018
    math_004.parent = frame_018
    math_005.parent = frame_018
    math_006.parent = frame_018
    math_007.parent = frame_004
    math_008.parent = frame_004
    math_009.parent = frame_018
    math_010.parent = frame_018
    mesh_to_curve_001.parent = frame_004
    noise_texture.parent = frame_002
    normal_001.parent = frame_003
    position_003.parent = frame_018
    position_005.parent = frame_018
    position_006.parent = frame_004
    resample_curve.parent = frame_018
    rotate_rotation_003.parent = frame_003
    rotate_rotation_004.parent = frame_003
    sample_curve.parent = frame_018
    scale_elements.parent = frame_004
    separate_x_y_z_005.parent = frame_018
    separate_x_y_z_006.parent = frame_004
    set_curve_tilt_002.parent = frame_018
    set_position_002.parent = frame_018
    set_position_003.parent = frame_002
    set_position_004.parent = frame_004
    spline_parameter.parent = frame_018
    spline_parameter_001.parent = frame_018
    spline_parameter_002.parent = frame_018
    spline_parameter_003.parent = frame_018
    store_named_attribute_004.parent = frame_002
    store_named_attribute_005.parent = frame_004
    store_named_attribute_006.parent = frame_004
    transform_geometry_012.parent = frame_018
    transform_geometry_013.parent = frame_002
    transform_geometry_014.parent = frame_002
    transform_geometry_015.parent = frame_004
    transform_geometry_016.parent = frame_004
    transform_geometry_017.parent = frame_004
    transform_geometry_018.parent = frame_004
    transform_geometry_019.parent = frame_004
    transform_geometry_020.parent = frame_018
    transform_geometry_040.parent = frame_004
    transform_geometry_041.parent = frame_004
    transform_geometry_042.parent = frame_004
    transform_geometry_043.parent = frame_004
    vector_math_001.parent = frame_018
    vector_math_002.parent = frame_002
    vector_math_003.parent = frame_018

    # Internal links
    links.new(curve_circle_002.outputs[0], set_position_002.inputs[0])
    links.new(set_position_002.outputs[0], transform_geometry_012.inputs[0])
    links.new(position_003.outputs[0], separate_x_y_z_005.inputs[0])
    links.new(separate_x_y_z_005.outputs[1], map_range_001.inputs[0])
    links.new(map_range_001.outputs[0], float_curve.inputs[1])
    links.new(combine_x_y_z_001.outputs[0], set_position_002.inputs[3])
    links.new(math_002.outputs[0], combine_x_y_z_001.inputs[2])
    links.new(position_005.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], set_position_002.inputs[2])
    links.new(combine_x_y_z_002.outputs[0], vector_math_001.inputs[1])
    links.new(map_range_001.outputs[0], float_curve_002.inputs[1])
    links.new(float_curve_002.outputs[0], combine_x_y_z_002.inputs[0])
    links.new(transform_geometry_012.outputs[0], resample_curve.inputs[0])
    links.new(curve_tangent_001.outputs[0], align_rotation_to_vector.inputs[2])
    links.new(align_rotation_to_vector.outputs[0], align_rotation_to_vector_001.inputs[0])
    links.new(normal_001.outputs[0], align_rotation_to_vector_001.inputs[2])
    links.new(align_rotation_to_vector_001.outputs[0], rotate_rotation_003.inputs[0])
    links.new(spline_parameter.outputs[0], math_003.inputs[0])
    links.new(math_003.outputs[0], math_004.inputs[0])
    links.new(set_curve_tilt_002.outputs[0], instance_on_points_002.inputs[0])
    links.new(resample_curve.outputs[0], set_curve_tilt_002.inputs[0])
    links.new(math_004.outputs[0], map_range_002.inputs[0])
    links.new(map_range_002.outputs[0], set_curve_tilt_002.inputs[2])
    links.new(spline_parameter_001.outputs[0], float_curve_003.inputs[1])
    links.new(float_curve_003.outputs[0], math_005.inputs[0])
    links.new(curve_circle_003.outputs[0], instance_on_points_003.inputs[0])
    links.new(ico_sphere_001.outputs[0], instance_on_points_003.inputs[2])
    links.new(instance_on_points_003.outputs[0], join_geometry_003.inputs[0])
    links.new(cylinder_001.outputs[0], join_geometry_003.inputs[0])
    links.new(transform_geometry_013.outputs[0], join_geometry_003.inputs[0])
    links.new(set_position_003.outputs[0], transform_geometry_013.inputs[0])
    links.new(ico_sphere_002.outputs[0], set_position_003.inputs[0])
    links.new(vector_math_002.outputs[0], set_position_003.inputs[3])
    links.new(noise_texture.outputs[0], vector_math_002.inputs[0])
    links.new(transform_geometry_013.outputs[0], transform_geometry_014.inputs[0])
    links.new(transform_geometry_014.outputs[0], join_geometry_003.inputs[0])
    links.new(rotate_rotation_003.outputs[0], rotate_rotation_004.inputs[0])
    links.new(rotate_rotation_004.outputs[0], instance_on_points_002.inputs[5])
    links.new(ico_sphere_003.outputs[0], join_geometry_003.inputs[0])
    links.new(store_named_attribute_004.outputs[0], instance_on_points_002.inputs[2])
    links.new(join_geometry_003.outputs[0], store_named_attribute_004.inputs[0])
    links.new(math_006.outputs[0], math_002.inputs[0])
    links.new(float_curve.outputs[0], math_006.inputs[0])
    links.new(spline_parameter_002.outputs[0], float_curve_004.inputs[1])
    links.new(float_curve_004.outputs[0], math_006.inputs[1])
    links.new(cylinder_002.outputs[0], set_position_004.inputs[0])
    links.new(position_006.outputs[0], separate_x_y_z_006.inputs[0])
    links.new(separate_x_y_z_006.outputs[0], math_007.inputs[0])
    links.new(combine_x_y_z_003.outputs[0], set_position_004.inputs[3])
    links.new(separate_x_y_z_006.outputs[1], map_range_003.inputs[0])
    links.new(math_008.outputs[0], combine_x_y_z_003.inputs[1])
    links.new(math_007.outputs[0], math_008.inputs[0])
    links.new(map_range_003.outputs[0], math_008.inputs[1])
    links.new(cylinder_002.outputs[1], boolean_math_004.inputs[0])
    links.new(cylinder_002.outputs[2], boolean_math_004.inputs[1])
    links.new(set_position_004.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(boolean_math_004.outputs[0], mesh_to_curve_001.inputs[1])
    links.new(mesh_to_curve_001.outputs[0], instance_on_points_004.inputs[0])
    links.new(ico_sphere_004.outputs[0], instance_on_points_004.inputs[2])
    links.new(ico_sphere_005.outputs[0], dual_mesh.inputs[0])
    links.new(dual_mesh.outputs[0], transform_geometry_015.inputs[0])
    links.new(transform_geometry_015.outputs[0], transform_geometry_016.inputs[0])
    links.new(transform_geometry_016.outputs[0], join_geometry_007.inputs[0])
    links.new(transform_geometry_015.outputs[0], transform_geometry_017.inputs[0])
    links.new(transform_geometry_017.outputs[0], join_geometry_007.inputs[0])
    links.new(transform_geometry_015.outputs[0], transform_geometry_018.inputs[0])
    links.new(transform_geometry_018.outputs[0], join_geometry_007.inputs[0])
    links.new(transform_geometry_015.outputs[0], transform_geometry_019.inputs[0])
    links.new(transform_geometry_019.outputs[0], join_geometry_007.inputs[0])
    links.new(instance_on_points_004.outputs[0], join_geometry_009.inputs[0])
    links.new(set_position_004.outputs[0], join_geometry_009.inputs[0])
    links.new(store_named_attribute_005.outputs[0], join_geometry_010.inputs[0])
    links.new(store_named_attribute_006.outputs[0], join_geometry_010.inputs[0])
    links.new(set_curve_tilt_002.outputs[0], sample_curve.inputs[0])
    links.new(join_geometry_010.outputs[0], transform_geometry_020.inputs[0])
    links.new(transform_geometry_020.outputs[0], join_geometry_011.inputs[0])
    links.new(instance_on_points_002.outputs[0], join_geometry_011.inputs[0])
    links.new(vector_math_003.outputs[0], transform_geometry_020.inputs[2])
    links.new(sample_curve.outputs[1], vector_math_003.inputs[0])
    links.new(spline_parameter_003.outputs[0], float_curve_005.inputs[1])
    links.new(float_curve_005.outputs[0], math_009.inputs[0])
    links.new(math_010.outputs[0], combine_x_y_z_001.inputs[1])
    links.new(math_005.outputs[0], math_010.inputs[0])
    links.new(math_009.outputs[0], math_010.inputs[1])
    links.new(set_position_004.outputs[0], transform_geometry_040.inputs[0])
    links.new(transform_geometry_040.outputs[0], join_geometry_009.inputs[0])
    links.new(transform_geometry_040.outputs[0], transform_geometry_041.inputs[0])
    links.new(transform_geometry_041.outputs[0], join_geometry_009.inputs[0])
    links.new(join_geometry_007.outputs[0], scale_elements.inputs[0])
    links.new(scale_elements.outputs[0], transform_geometry_042.inputs[0])
    links.new(join_geometry_023.outputs[0], store_named_attribute_006.inputs[0])
    links.new(join_geometry_009.outputs[0], join_geometry_023.inputs[0])
    links.new(transform_geometry_042.outputs[0], join_geometry_023.inputs[0])
    links.new(transform_geometry_043.outputs[0], store_named_attribute_005.inputs[0])
    links.new(join_geometry_007.outputs[0], transform_geometry_043.inputs[0])

    links.new(curve_circle_002.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
