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
def create_neck_align_f022_group():
    group_name = "Neck_align_f022"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    curve_circle_004 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_004.mode = "RADIUS"
    curve_circle_004.inputs[0].default_value = 64
    curve_circle_004.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_004.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_004.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_004.inputs[4].default_value = 0.12999999523162842


    transform_geometry_021 = nodes.new("GeometryNodeTransform")
    transform_geometry_021.inputs[1].default_value = "Components"
    transform_geometry_021.inputs[2].default_value = Vector((-0.009999999776482582, -0.03999999910593033, 0.46000000834465027))
    transform_geometry_021.inputs[3].default_value = Euler((-0.027925267815589905, 0.0, -0.08691740036010742), 'XYZ')
    transform_geometry_021.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    set_position_005 = nodes.new("GeometryNodeSetPosition")
    set_position_005.inputs[1].default_value = True


    position_007 = nodes.new("GeometryNodeInputPosition")


    separate_x_y_z_007 = nodes.new("ShaderNodeSeparateXYZ")


    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.clamp = True
    map_range_004.interpolation_type = "LINEAR"
    map_range_004.data_type = "FLOAT"
    map_range_004.inputs[1].default_value = 0.12999999523162842
    map_range_004.inputs[2].default_value = -0.12999999523162842
    map_range_004.inputs[3].default_value = 0.0
    map_range_004.inputs[4].default_value = 1.0
    map_range_004.inputs[5].default_value = 4.0
    map_range_004.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range_004.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range_004.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range_004.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range_004.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range_004.inputs[11].default_value = [4.0, 4.0, 4.0]


    float_curve_006 = nodes.new("ShaderNodeFloatCurve")
    float_curve_006.inputs[0].default_value = 1.0


    math_011 = nodes.new("ShaderNodeMath")
    math_011.operation = "MULTIPLY"
    math_011.inputs[1].default_value = -0.19999998807907104
    math_011.inputs[2].default_value = 0.5


    combine_x_y_z_004 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_004.inputs[0].default_value = 0.0


    position_008 = nodes.new("GeometryNodeInputPosition")


    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.operation = "MULTIPLY"
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_004.inputs[3].default_value = 1.0


    combine_x_y_z_005 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_005.inputs[1].default_value = 1.0
    combine_x_y_z_005.inputs[2].default_value = 1.0


    float_curve_007 = nodes.new("ShaderNodeFloatCurve")
    float_curve_007.inputs[0].default_value = 1.0


    resample_curve_004 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_004.keep_last_segment = True
    resample_curve_004.inputs[1].default_value = True
    resample_curve_004.inputs[2].default_value = "Length"
    resample_curve_004.inputs[3].default_value = 10
    resample_curve_004.inputs[4].default_value = 0.013799999840557575


    instance_on_points_005 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_005.inputs[1].default_value = True
    instance_on_points_005.inputs[3].default_value = False
    instance_on_points_005.inputs[4].default_value = 0
    instance_on_points_005.inputs[6].default_value = Vector((0.699999988079071, 0.699999988079071, 0.699999988079071))


    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.axis = "X"
    align_rotation_to_vector_002.pivot_axis = "AUTO"
    align_rotation_to_vector_002.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_002.inputs[1].default_value = 1.0


    curve_tangent_002 = nodes.new("GeometryNodeInputTangent")


    align_rotation_to_vector_003 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_003.axis = "Y"
    align_rotation_to_vector_003.pivot_axis = "AUTO"
    align_rotation_to_vector_003.inputs[1].default_value = 1.0


    normal_002 = nodes.new("GeometryNodeInputNormal")
    normal_002.legacy_corner_normals = False


    spline_parameter_004 = nodes.new("GeometryNodeSplineParameter")


    math_012 = nodes.new("ShaderNodeMath")
    math_012.operation = "SUBTRACT"
    math_012.inputs[1].default_value = 0.7400000095367432
    math_012.inputs[2].default_value = 0.5


    math_013 = nodes.new("ShaderNodeMath")
    math_013.operation = "ABSOLUTE"
    math_013.inputs[1].default_value = 0.7400000095367432
    math_013.inputs[2].default_value = 0.5


    set_curve_tilt_003 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_003.inputs[1].default_value = True


    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.clamp = True
    map_range_005.interpolation_type = "LINEAR"
    map_range_005.data_type = "FLOAT"
    map_range_005.inputs[1].default_value = 0.0
    map_range_005.inputs[2].default_value = 0.08000002801418304
    map_range_005.inputs[3].default_value = 0.6799999475479126
    map_range_005.inputs[4].default_value = 0.47999998927116394
    map_range_005.inputs[5].default_value = 4.0
    map_range_005.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range_005.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range_005.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range_005.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range_005.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range_005.inputs[11].default_value = [4.0, 4.0, 4.0]


    float_curve_008 = nodes.new("ShaderNodeFloatCurve")
    float_curve_008.inputs[0].default_value = 1.0


    spline_parameter_005 = nodes.new("GeometryNodeSplineParameter")


    math_014 = nodes.new("ShaderNodeMath")
    math_014.operation = "MULTIPLY"
    math_014.inputs[1].default_value = 0.014999999664723873
    math_014.inputs[2].default_value = 0.5


    frame_020 = nodes.new("NodeFrame")
    frame_020.label = "Align"
    frame_020.text = None
    frame_020.shrink = True
    frame_020.label_size = 20


    math_015 = nodes.new("ShaderNodeMath")
    math_015.operation = "ADD"
    math_015.inputs[2].default_value = 0.5


    spline_parameter_006 = nodes.new("GeometryNodeSplineParameter")


    float_curve_009 = nodes.new("ShaderNodeFloatCurve")
    float_curve_009.inputs[0].default_value = 1.0


    float_curve_010 = nodes.new("ShaderNodeFloatCurve")
    float_curve_010.inputs[0].default_value = 1.0


    spline_parameter_007 = nodes.new("GeometryNodeSplineParameter")


    math_018 = nodes.new("ShaderNodeMath")
    math_018.operation = "MULTIPLY"
    math_018.inputs[1].default_value = -0.014999999664723873
    math_018.inputs[2].default_value = 0.5


    math_019 = nodes.new("ShaderNodeMath")
    math_019.operation = "ADD"
    math_019.inputs[2].default_value = 0.5


    frame_022 = nodes.new("NodeFrame")
    frame_022.label = "Necklace 1"
    frame_022.text = None
    frame_022.shrink = True
    frame_022.label_size = 20


    quadrilateral = nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
    quadrilateral.mode = "RECTANGLE"
    quadrilateral.inputs[0].default_value = 0.02500000037252903
    quadrilateral.inputs[1].default_value = 0.014999999664723873
    quadrilateral.inputs[2].default_value = 4.0
    quadrilateral.inputs[3].default_value = 2.0
    quadrilateral.inputs[4].default_value = 1.0
    quadrilateral.inputs[5].default_value = 3.0
    quadrilateral.inputs[6].default_value = 1.0
    quadrilateral.inputs[7].default_value = Vector((-1.0, -1.0, 0.0))
    quadrilateral.inputs[8].default_value = Vector((1.0, -1.0, 0.0))
    quadrilateral.inputs[9].default_value = Vector((1.0, 1.0, 0.0))
    quadrilateral.inputs[10].default_value = Vector((-1.0, 1.0, 0.0))


    fillet_curve = nodes.new("GeometryNodeFilletCurve")
    fillet_curve.inputs[1].default_value = 0.007000000216066837
    fillet_curve.inputs[2].default_value = True
    fillet_curve.inputs[3].default_value = "Bézier"
    fillet_curve.inputs[4].default_value = 1


    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.spline_type = "BEZIER"
    set_spline_type.inputs[1].default_value = True


    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.inputs[2].default_value = 0.8519999980926514
    curve_to_mesh_001.inputs[3].default_value = False


    curve_circle_005 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_005.mode = "RADIUS"
    curve_circle_005.inputs[0].default_value = 6
    curve_circle_005.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_005.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_005.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_005.inputs[4].default_value = 0.003000000026077032


    frame_019 = nodes.new("NodeFrame")
    frame_019.label = "Link"
    frame_019.text = None
    frame_019.shrink = True
    frame_019.label_size = 20


    rotate_rotation_006 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_006.rotation_space = "LOCAL"


    rotate_rotation_005 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_005.rotation_space = "LOCAL"


    random_value_012 = nodes.new("FunctionNodeRandomValue")
    random_value_012.data_type = "FLOAT_VECTOR"
    random_value_012.inputs[0].default_value = [-0.29999998211860657, -0.09999999403953552, 0.0]
    random_value_012.inputs[1].default_value = [0.2999999225139618, 0.09999999403953552, 0.0]
    random_value_012.inputs[2].default_value = 0.0
    random_value_012.inputs[3].default_value = 1.0
    random_value_012.inputs[4].default_value = 0
    random_value_012.inputs[5].default_value = 100
    random_value_012.inputs[6].default_value = 0.5
    random_value_012.inputs[7].default_value = 0
    random_value_012.inputs[8].default_value = 3


    index_001 = nodes.new("GeometryNodeInputIndex")


    math_016 = nodes.new("ShaderNodeMath")
    math_016.operation = "FLOORED_MODULO"
    math_016.inputs[1].default_value = 2.0
    math_016.inputs[2].default_value = 0.5


    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "FLOAT"
    switch_001.inputs[1].default_value = -0.3799999952316284
    switch_001.inputs[2].default_value = 0.5


    combine_x_y_z_006 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_006.inputs[1].default_value = 0.0
    combine_x_y_z_006.inputs[2].default_value = 0.0


    curve_circle_006 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_006.mode = "RADIUS"
    curve_circle_006.inputs[0].default_value = 15
    curve_circle_006.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_006.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_006.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_006.inputs[4].default_value = 0.009999999776482582


    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.inputs[2].default_value = 0.22200000286102295
    curve_to_mesh_002.inputs[3].default_value = False


    sample_curve_001 = nodes.new("GeometryNodeSampleCurve")
    sample_curve_001.mode = "FACTOR"
    sample_curve_001.use_all_curves = True
    sample_curve_001.data_type = "FLOAT"
    sample_curve_001.inputs[1].default_value = 0.0
    sample_curve_001.inputs[2].default_value = 0.7185045480728149
    sample_curve_001.inputs[3].default_value = 0.0
    sample_curve_001.inputs[4].default_value = 0


    transform_geometry_022 = nodes.new("GeometryNodeTransform")
    transform_geometry_022.inputs[1].default_value = "Components"
    transform_geometry_022.inputs[3].default_value = Euler((1.5707963705062866, 0.0, 0.34033918380737305), 'XYZ')
    transform_geometry_022.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    join_geometry_013 = nodes.new("GeometryNodeJoinGeometry")


    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.operation = "ADD"
    vector_math_005.inputs[1].default_value = [0.0, 0.0, -0.012000000104308128]
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_005.inputs[3].default_value = 1.0


    curve_circle_007 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_007.mode = "RADIUS"
    curve_circle_007.inputs[0].default_value = 6
    curve_circle_007.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_007.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_007.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_007.inputs[4].default_value = 0.009999999776482582


    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.mode = "DIRECTION"
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, -0.009999999776482582))
    curve_line.inputs[1].default_value = Vector((0.0, 0.0, 1.0))
    curve_line.inputs[2].default_value = [0.0, 0.0, -1.0]
    curve_line.inputs[3].default_value = 0.05000000074505806


    transform_geometry_023 = nodes.new("GeometryNodeTransform")
    transform_geometry_023.inputs[1].default_value = "Components"
    transform_geometry_023.inputs[3].default_value = Euler((0.0, 0.06632250547409058, -0.6752678751945496), 'XYZ')
    transform_geometry_023.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    frame_021 = nodes.new("NodeFrame")
    frame_021.label = "Loop"
    frame_021.text = None
    frame_021.shrink = True
    frame_021.label_size = 20


    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.operation = "ADD"
    vector_math_006.inputs[1].default_value = [0.0, 0.0, -0.017999999225139618]
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_006.inputs[3].default_value = 1.0


    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.inputs[3].default_value = True


    resample_curve_005 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_005.keep_last_segment = True
    resample_curve_005.inputs[1].default_value = True
    resample_curve_005.inputs[2].default_value = "Count"
    resample_curve_005.inputs[3].default_value = 128
    resample_curve_005.inputs[4].default_value = 0.10000000149011612


    curve_circle_008 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_008.mode = "RADIUS"
    curve_circle_008.inputs[0].default_value = 32
    curve_circle_008.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_008.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_008.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_008.inputs[4].default_value = 0.003000000026077032


    spline_parameter_008 = nodes.new("GeometryNodeSplineParameter")


    float_curve_011 = nodes.new("ShaderNodeFloatCurve")
    float_curve_011.inputs[0].default_value = 1.0


    curve_circle_009 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_009.mode = "RADIUS"
    curve_circle_009.inputs[0].default_value = 12
    curve_circle_009.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_009.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_009.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_009.inputs[4].default_value = 0.004000000189989805


    curve_to_mesh_004 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_004.inputs[2].default_value = 0.800000011920929
    curve_to_mesh_004.inputs[3].default_value = True


    curve_circle_010 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_010.mode = "RADIUS"
    curve_circle_010.inputs[0].default_value = 6
    curve_circle_010.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_010.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_010.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_010.inputs[4].default_value = 0.0020000000949949026


    join_geometry_014 = nodes.new("GeometryNodeJoinGeometry")


    curve_circle_011 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_011.mode = "RADIUS"
    curve_circle_011.inputs[0].default_value = 6
    curve_circle_011.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_011.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_011.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_011.inputs[4].default_value = 0.00800000037997961


    instance_on_points_006 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_006.inputs[1].default_value = True
    instance_on_points_006.inputs[3].default_value = False
    instance_on_points_006.inputs[4].default_value = 0
    instance_on_points_006.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_006.inputs[6].default_value = Vector((1.0, 1.0, 1.0))


    transform_geometry_024 = nodes.new("GeometryNodeTransform")
    transform_geometry_024.inputs[1].default_value = "Components"
    transform_geometry_024.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_024.inputs[3].default_value = Euler((1.5707963705062866, 0.5235987901687622, 0.0), 'XYZ')
    transform_geometry_024.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    grid = nodes.new("GeometryNodeMeshGrid")
    grid.inputs[0].default_value = 0.014999999664723873
    grid.inputs[1].default_value = 0.012000000104308128
    grid.inputs[2].default_value = 12
    grid.inputs[3].default_value = 4


    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "FACE"


    random_value_013 = nodes.new("FunctionNodeRandomValue")
    random_value_013.data_type = "BOOLEAN"
    random_value_013.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_013.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_013.inputs[2].default_value = 0.0
    random_value_013.inputs[3].default_value = 1.0
    random_value_013.inputs[4].default_value = 0
    random_value_013.inputs[5].default_value = 100
    random_value_013.inputs[6].default_value = 0.2734806537628174
    random_value_013.inputs[7].default_value = 0
    random_value_013.inputs[8].default_value = 78


    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.mode = "FACES"
    extrude_mesh.inputs[1].default_value = True
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    extrude_mesh.inputs[3].default_value = 0.003000000026077032
    extrude_mesh.inputs[4].default_value = False


    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.inputs[1].default_value = True


    join_geometry_015 = nodes.new("GeometryNodeJoinGeometry")


    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.inputs[1].default_value = True
    merge_by_distance.inputs[2].default_value = "All"
    merge_by_distance.inputs[3].default_value = 9.999999747378752e-05


    transform_geometry_025 = nodes.new("GeometryNodeTransform")
    transform_geometry_025.inputs[1].default_value = "Components"
    transform_geometry_025.inputs[2].default_value = Vector((0.006000000052154064, 0.001500000013038516, -0.04999999701976776))
    transform_geometry_025.inputs[3].default_value = Euler((1.5707963705062866, -1.5707963705062866, 0.0), 'XYZ')
    transform_geometry_025.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    subdivision_surface = nodes.new("GeometryNodeSubdivisionSurface")
    subdivision_surface.inputs[1].default_value = 1
    subdivision_surface.inputs[2].default_value = 0.8063265681266785
    subdivision_surface.inputs[3].default_value = 0.0
    subdivision_surface.inputs[4].default_value = True
    subdivision_surface.inputs[5].default_value = "Keep Boundaries"
    subdivision_surface.inputs[6].default_value = "All"


    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.domain = "FACE"
    set_shade_smooth_001.inputs[1].default_value = True
    set_shade_smooth_001.inputs[2].default_value = True


    frame_023 = nodes.new("NodeFrame")
    frame_023.label = "Key"
    frame_023.text = None
    frame_023.shrink = True
    frame_023.label_size = 20


    store_named_attribute_007 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_007.data_type = "BOOLEAN"
    store_named_attribute_007.domain = "POINT"
    store_named_attribute_007.inputs[1].default_value = True
    store_named_attribute_007.inputs[2].default_value = "gold"
    store_named_attribute_007.inputs[3].default_value = True


    # Parent assignments
    align_rotation_to_vector_002.parent = frame_020
    align_rotation_to_vector_003.parent = frame_020
    combine_x_y_z_004.parent = frame_022
    combine_x_y_z_005.parent = frame_022
    combine_x_y_z_006.parent = frame_020
    curve_circle_004.parent = frame_022
    curve_circle_005.parent = frame_019
    curve_circle_006.parent = frame_021
    curve_circle_007.parent = frame_021
    curve_circle_008.parent = frame_023
    curve_circle_009.parent = frame_023
    curve_circle_010.parent = frame_023
    curve_circle_011.parent = frame_023
    curve_line.parent = frame_023
    curve_tangent_002.parent = frame_020
    curve_to_mesh_001.parent = frame_019
    curve_to_mesh_002.parent = frame_021
    curve_to_mesh_003.parent = frame_023
    curve_to_mesh_004.parent = frame_023
    delete_geometry_001.parent = frame_023
    extrude_mesh.parent = frame_023
    fillet_curve.parent = frame_019
    flip_faces.parent = frame_023
    float_curve_006.parent = frame_022
    float_curve_007.parent = frame_022
    float_curve_008.parent = frame_022
    float_curve_009.parent = frame_022
    float_curve_010.parent = frame_022
    float_curve_011.parent = frame_023
    frame_019.parent = frame_022
    frame_020.parent = frame_022
    frame_021.parent = frame_022
    frame_023.parent = frame_022
    grid.parent = frame_023
    index_001.parent = frame_020
    instance_on_points_005.parent = frame_022
    instance_on_points_006.parent = frame_023
    join_geometry_013.parent = frame_022
    join_geometry_014.parent = frame_023
    join_geometry_015.parent = frame_023
    map_range_004.parent = frame_022
    map_range_005.parent = frame_022
    math_011.parent = frame_022
    math_012.parent = frame_022
    math_013.parent = frame_022
    math_014.parent = frame_022
    math_015.parent = frame_022
    math_016.parent = frame_020
    math_018.parent = frame_022
    math_019.parent = frame_022
    merge_by_distance.parent = frame_023
    normal_002.parent = frame_020
    position_007.parent = frame_022
    position_008.parent = frame_022
    quadrilateral.parent = frame_019
    random_value_012.parent = frame_020
    random_value_013.parent = frame_023
    resample_curve_004.parent = frame_022
    resample_curve_005.parent = frame_023
    rotate_rotation_005.parent = frame_020
    rotate_rotation_006.parent = frame_020
    sample_curve_001.parent = frame_022
    separate_x_y_z_007.parent = frame_022
    set_curve_tilt_003.parent = frame_022
    set_position_005.parent = frame_022
    set_shade_smooth_001.parent = frame_022
    set_spline_type.parent = frame_019
    spline_parameter_004.parent = frame_022
    spline_parameter_005.parent = frame_022
    spline_parameter_006.parent = frame_022
    spline_parameter_007.parent = frame_022
    spline_parameter_008.parent = frame_023
    store_named_attribute_007.parent = frame_022
    subdivision_surface.parent = frame_023
    switch_001.parent = frame_020
    transform_geometry_021.parent = frame_022
    transform_geometry_022.parent = frame_022
    transform_geometry_023.parent = frame_022
    transform_geometry_024.parent = frame_023
    transform_geometry_025.parent = frame_023
    vector_math_004.parent = frame_022
    vector_math_005.parent = frame_022
    vector_math_006.parent = frame_022

    # Internal links
    links.new(curve_circle_004.outputs[0], set_position_005.inputs[0])
    links.new(set_position_005.outputs[0], transform_geometry_021.inputs[0])
    links.new(position_007.outputs[0], separate_x_y_z_007.inputs[0])
    links.new(separate_x_y_z_007.outputs[1], map_range_004.inputs[0])
    links.new(map_range_004.outputs[0], float_curve_006.inputs[1])
    links.new(combine_x_y_z_004.outputs[0], set_position_005.inputs[3])
    links.new(math_011.outputs[0], combine_x_y_z_004.inputs[2])
    links.new(position_008.outputs[0], vector_math_004.inputs[0])
    links.new(vector_math_004.outputs[0], set_position_005.inputs[2])
    links.new(combine_x_y_z_005.outputs[0], vector_math_004.inputs[1])
    links.new(map_range_004.outputs[0], float_curve_007.inputs[1])
    links.new(float_curve_007.outputs[0], combine_x_y_z_005.inputs[0])
    links.new(transform_geometry_021.outputs[0], resample_curve_004.inputs[0])
    links.new(curve_tangent_002.outputs[0], align_rotation_to_vector_002.inputs[2])
    links.new(align_rotation_to_vector_002.outputs[0], align_rotation_to_vector_003.inputs[0])
    links.new(normal_002.outputs[0], align_rotation_to_vector_003.inputs[2])
    links.new(spline_parameter_004.outputs[0], math_012.inputs[0])
    links.new(math_012.outputs[0], math_013.inputs[0])
    links.new(set_curve_tilt_003.outputs[0], instance_on_points_005.inputs[0])
    links.new(resample_curve_004.outputs[0], set_curve_tilt_003.inputs[0])
    links.new(math_013.outputs[0], map_range_005.inputs[0])
    links.new(map_range_005.outputs[0], set_curve_tilt_003.inputs[2])
    links.new(spline_parameter_005.outputs[0], float_curve_008.inputs[1])
    links.new(float_curve_008.outputs[0], math_014.inputs[0])
    links.new(math_015.outputs[0], math_011.inputs[0])
    links.new(float_curve_006.outputs[0], math_015.inputs[0])
    links.new(spline_parameter_006.outputs[0], float_curve_009.inputs[1])
    links.new(float_curve_009.outputs[0], math_015.inputs[1])
    links.new(spline_parameter_007.outputs[0], float_curve_010.inputs[1])
    links.new(float_curve_010.outputs[0], math_018.inputs[0])
    links.new(math_019.outputs[0], combine_x_y_z_004.inputs[1])
    links.new(math_014.outputs[0], math_019.inputs[0])
    links.new(math_018.outputs[0], math_019.inputs[1])
    links.new(set_spline_type.outputs[0], fillet_curve.inputs[0])
    links.new(quadrilateral.outputs[0], set_spline_type.inputs[0])
    links.new(fillet_curve.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(curve_to_mesh_001.outputs[0], instance_on_points_005.inputs[2])
    links.new(curve_circle_005.outputs[0], curve_to_mesh_001.inputs[1])
    links.new(rotate_rotation_006.outputs[0], instance_on_points_005.inputs[5])
    links.new(align_rotation_to_vector_003.outputs[0], rotate_rotation_005.inputs[0])
    links.new(rotate_rotation_005.outputs[0], rotate_rotation_006.inputs[0])
    links.new(random_value_012.outputs[0], rotate_rotation_006.inputs[1])
    links.new(index_001.outputs[0], math_016.inputs[0])
    links.new(math_016.outputs[0], switch_001.inputs[0])
    links.new(switch_001.outputs[0], combine_x_y_z_006.inputs[0])
    links.new(combine_x_y_z_006.outputs[0], rotate_rotation_005.inputs[1])
    links.new(curve_circle_006.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(set_curve_tilt_003.outputs[0], sample_curve_001.inputs[0])
    links.new(curve_to_mesh_002.outputs[0], transform_geometry_022.inputs[0])
    links.new(instance_on_points_005.outputs[0], join_geometry_013.inputs[0])
    links.new(transform_geometry_022.outputs[0], join_geometry_013.inputs[0])
    links.new(vector_math_005.outputs[0], transform_geometry_022.inputs[2])
    links.new(sample_curve_001.outputs[1], vector_math_005.inputs[0])
    links.new(curve_circle_007.outputs[0], curve_to_mesh_002.inputs[1])
    links.new(transform_geometry_023.outputs[0], join_geometry_013.inputs[0])
    links.new(vector_math_006.outputs[0], transform_geometry_023.inputs[2])
    links.new(vector_math_005.outputs[0], vector_math_006.inputs[0])
    links.new(resample_curve_005.outputs[0], curve_to_mesh_003.inputs[0])
    links.new(curve_line.outputs[0], resample_curve_005.inputs[0])
    links.new(curve_circle_008.outputs[0], curve_to_mesh_003.inputs[1])
    links.new(spline_parameter_008.outputs[0], float_curve_011.inputs[1])
    links.new(float_curve_011.outputs[0], curve_to_mesh_003.inputs[2])
    links.new(curve_circle_009.outputs[0], curve_to_mesh_004.inputs[0])
    links.new(curve_circle_010.outputs[0], curve_to_mesh_004.inputs[1])
    links.new(curve_to_mesh_003.outputs[0], join_geometry_014.inputs[0])
    links.new(join_geometry_014.outputs[0], transform_geometry_023.inputs[0])
    links.new(curve_to_mesh_004.outputs[0], instance_on_points_006.inputs[2])
    links.new(curve_circle_011.outputs[0], instance_on_points_006.inputs[0])
    links.new(instance_on_points_006.outputs[0], transform_geometry_024.inputs[0])
    links.new(transform_geometry_024.outputs[0], join_geometry_014.inputs[0])
    links.new(grid.outputs[0], delete_geometry_001.inputs[0])
    links.new(random_value_013.outputs[3], delete_geometry_001.inputs[1])
    links.new(delete_geometry_001.outputs[0], extrude_mesh.inputs[0])
    links.new(delete_geometry_001.outputs[0], flip_faces.inputs[0])
    links.new(extrude_mesh.outputs[0], join_geometry_015.inputs[0])
    links.new(flip_faces.outputs[0], join_geometry_015.inputs[0])
    links.new(join_geometry_015.outputs[0], merge_by_distance.inputs[0])
    links.new(transform_geometry_025.outputs[0], join_geometry_014.inputs[0])
    links.new(subdivision_surface.outputs[0], transform_geometry_025.inputs[0])
    links.new(merge_by_distance.outputs[0], subdivision_surface.inputs[0])
    links.new(join_geometry_013.outputs[0], set_shade_smooth_001.inputs[0])
    links.new(set_shade_smooth_001.outputs[0], store_named_attribute_007.inputs[0])

    links.new(curve_circle_004.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
