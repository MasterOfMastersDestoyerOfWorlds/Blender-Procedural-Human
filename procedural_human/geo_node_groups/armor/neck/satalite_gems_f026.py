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
def create_neck_satalite_gems_f026_group():
    group_name = "Neck_satalite_gems_f026"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    ico_sphere_006 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_006.inputs[0].default_value = 0.029999999329447746
    ico_sphere_006.inputs[1].default_value = 3


    transform_geometry_026 = nodes.new("GeometryNodeTransform")
    transform_geometry_026.inputs[1].default_value = "Components"
    transform_geometry_026.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_026.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_026.inputs[4].default_value = Vector((1.0, 1.0, 0.5))


    instance_on_points_007 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_007.inputs[1].default_value = True
    instance_on_points_007.inputs[3].default_value = False
    instance_on_points_007.inputs[4].default_value = 0
    instance_on_points_007.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_007.inputs[6].default_value = Vector((1.0, 1.0, 1.0))


    quadratic_bézier = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier.inputs[0].default_value = 16
    quadratic_bézier.inputs[1].default_value = Vector((-0.019999999552965164, 0.0, 0.0))
    quadratic_bézier.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.009999999776482582))
    quadratic_bézier.inputs[3].default_value = Vector((0.019999999552965164, 0.0, 0.0))


    realize_instances_003 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.inputs[1].default_value = True
    realize_instances_003.inputs[2].default_value = True
    realize_instances_003.inputs[3].default_value = 0


    mesh_to_s_d_f_grid = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid.inputs[1].default_value = 0.009999999776482582
    mesh_to_s_d_f_grid.inputs[2].default_value = 1


    grid_to_mesh = nodes.new("GeometryNodeGridToMesh")
    grid_to_mesh.inputs[1].default_value = 0.0
    grid_to_mesh.inputs[2].default_value = 0.0


    dual_mesh_001 = nodes.new("GeometryNodeDualMesh")
    dual_mesh_001.inputs[1].default_value = False


    triangulate = nodes.new("GeometryNodeTriangulate")
    triangulate.inputs[1].default_value = True
    triangulate.inputs[2].default_value = "Shortest Diagonal"
    triangulate.inputs[3].default_value = "Beauty"


    s_d_f_grid_boolean = nodes.new("GeometryNodeSDFGridBoolean")
    s_d_f_grid_boolean.operation = "INTERSECT"
    s_d_f_grid_boolean.inputs[0].default_value = 0.0


    cube = nodes.new("GeometryNodeMeshCube")
    cube.inputs[0].default_value = Vector((1.0, 1.0, 0.019999999552965164))
    cube.inputs[1].default_value = 2
    cube.inputs[2].default_value = 2
    cube.inputs[3].default_value = 2


    mesh_to_s_d_f_grid_001 = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid_001.inputs[1].default_value = 0.009999999776482582
    mesh_to_s_d_f_grid_001.inputs[2].default_value = 1


    transform_geometry_027 = nodes.new("GeometryNodeTransform")
    transform_geometry_027.inputs[1].default_value = "Components"
    transform_geometry_027.inputs[2].default_value = Vector((0.0, 0.0, 0.009999999776482582))
    transform_geometry_027.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_027.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    mesh_boolean = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean.operation = "DIFFERENCE"
    mesh_boolean.solver = "MANIFOLD"
    mesh_boolean.inputs[2].default_value = False
    mesh_boolean.inputs[3].default_value = False


    cube_001 = nodes.new("GeometryNodeMeshCube")
    cube_001.inputs[0].default_value = Vector((1.0, 1.0, 1.0))
    cube_001.inputs[1].default_value = 2
    cube_001.inputs[2].default_value = 2
    cube_001.inputs[3].default_value = 2


    transform_geometry_028 = nodes.new("GeometryNodeTransform")
    transform_geometry_028.inputs[1].default_value = "Components"
    transform_geometry_028.inputs[2].default_value = Vector((0.5, 0.0, 0.0))
    transform_geometry_028.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_028.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    delete_geometry_002 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.mode = "ALL"
    delete_geometry_002.domain = "FACE"


    mesh_boolean_001 = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean_001.operation = "INTERSECT"
    mesh_boolean_001.solver = "MANIFOLD"
    mesh_boolean_001.inputs[2].default_value = False
    mesh_boolean_001.inputs[3].default_value = False


    cube_002 = nodes.new("GeometryNodeMeshCube")
    cube_002.inputs[0].default_value = Vector((1.0, 1.0, 0.0010000000474974513))
    cube_002.inputs[1].default_value = 2
    cube_002.inputs[2].default_value = 2
    cube_002.inputs[3].default_value = 2


    transform_geometry_029 = nodes.new("GeometryNodeTransform")
    transform_geometry_029.inputs[1].default_value = "Components"
    transform_geometry_029.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    transform_geometry_029.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_029.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    join_geometry_016 = nodes.new("GeometryNodeJoinGeometry")


    delete_geometry_003 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_003.mode = "ALL"
    delete_geometry_003.domain = "POINT"


    normal_003 = nodes.new("GeometryNodeInputNormal")
    normal_003.legacy_corner_normals = False


    compare_008 = nodes.new("FunctionNodeCompare")
    compare_008.operation = "EQUAL"
    compare_008.data_type = "VECTOR"
    compare_008.mode = "DIRECTION"
    compare_008.inputs[0].default_value = 0.0
    compare_008.inputs[1].default_value = 0.0
    compare_008.inputs[2].default_value = 0
    compare_008.inputs[3].default_value = 0
    compare_008.inputs[5].default_value = [0.0, 0.0, 1.0]
    compare_008.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_008.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_008.inputs[8].default_value = ""
    compare_008.inputs[9].default_value = ""
    compare_008.inputs[10].default_value = 0.8999999761581421
    compare_008.inputs[11].default_value = 0.0
    compare_008.inputs[12].default_value = 1.5707963705062866


    mesh_to_curve_003 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_003.mode = "EDGES"
    mesh_to_curve_003.inputs[1].default_value = True


    resample_curve_006 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_006.keep_last_segment = True
    resample_curve_006.inputs[1].default_value = True
    resample_curve_006.inputs[2].default_value = "Count"
    resample_curve_006.inputs[3].default_value = 45
    resample_curve_006.inputs[4].default_value = 0.10000000149011612


    set_spline_cyclic_002 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_002.inputs[1].default_value = True
    set_spline_cyclic_002.inputs[2].default_value = True


    curve_to_mesh_005 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_005.inputs[2].default_value = 0.009999999776482582
    curve_to_mesh_005.inputs[3].default_value = False


    gem_in_holder_3 = nodes.new("GeometryNodeGroup")
    gem_in_holder_3.node_tree = create_gem_in__holder_group()
    gem_in_holder_3.inputs[0].default_value = 0.009999999776482582
    gem_in_holder_3.inputs[1].default_value = "ruby"
    gem_in_holder_3.inputs[2].default_value = False
    gem_in_holder_3.inputs[3].default_value = 0.004999995231628418
    gem_in_holder_3.inputs[4].default_value = 6
    gem_in_holder_3.inputs[5].default_value = 41
    gem_in_holder_3.inputs[6].default_value = False
    gem_in_holder_3.inputs[7].default_value = 6
    gem_in_holder_3.inputs[8].default_value = 10
    gem_in_holder_3.inputs[9].default_value = 0.0020000000949949026
    gem_in_holder_3.inputs[10].default_value = 3.3099989891052246


    trim_curve_005 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_005.mode = "FACTOR"
    trim_curve_005.inputs[1].default_value = True
    trim_curve_005.inputs[2].default_value = 0.010773210786283016
    trim_curve_005.inputs[3].default_value = 0.9906079769134521
    trim_curve_005.inputs[4].default_value = 0.0
    trim_curve_005.inputs[5].default_value = 1.0


    instance_on_points_008 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_008.inputs[1].default_value = True
    instance_on_points_008.inputs[3].default_value = False
    instance_on_points_008.inputs[4].default_value = 0


    resample_curve_007 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_007.keep_last_segment = True
    resample_curve_007.inputs[1].default_value = True
    resample_curve_007.inputs[2].default_value = "Count"
    resample_curve_007.inputs[3].default_value = 10
    resample_curve_007.inputs[4].default_value = 0.10000000149011612


    align_rotation_to_vector_004 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_004.axis = "Y"
    align_rotation_to_vector_004.pivot_axis = "AUTO"
    align_rotation_to_vector_004.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_004.inputs[1].default_value = 1.0


    curve_tangent_003 = nodes.new("GeometryNodeInputTangent")


    realize_instances_004 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_004.inputs[1].default_value = True
    realize_instances_004.inputs[2].default_value = True
    realize_instances_004.inputs[3].default_value = 0


    transform_geometry_030 = nodes.new("GeometryNodeTransform")
    transform_geometry_030.inputs[1].default_value = "Components"
    transform_geometry_030.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_030.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_030.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))


    flip_faces_002 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.inputs[1].default_value = True


    join_geometry_018 = nodes.new("GeometryNodeJoinGeometry")


    merge_by_distance_001 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_001.inputs[2].default_value = "All"
    merge_by_distance_001.inputs[3].default_value = 0.0010000000474974513


    is_edge_boundary_1 = nodes.new("GeometryNodeGroup")
    is_edge_boundary_1.node_tree = create_is__edge__boundary_group()


    spline_parameter_009 = nodes.new("GeometryNodeSplineParameter")


    math_020 = nodes.new("ShaderNodeMath")
    math_020.operation = "MULTIPLY"
    math_020.inputs[1].default_value = 2.0
    math_020.inputs[2].default_value = 0.5


    math_021 = nodes.new("ShaderNodeMath")
    math_021.operation = "PINGPONG"
    math_021.inputs[1].default_value = 1.0
    math_021.inputs[2].default_value = 0.5


    curve_to_points_002 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_002.mode = "EVALUATED"
    curve_to_points_002.inputs[1].default_value = 10
    curve_to_points_002.inputs[2].default_value = 0.10000000149011612


    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.inputs[1].default_value = 0


    gradient_texture = nodes.new("ShaderNodeTexGradient")
    gradient_texture.gradient_type = "RADIAL"
    gradient_texture.inputs[0].default_value = [0.0, 0.0, 0.0]


    math_022 = nodes.new("ShaderNodeMath")
    math_022.operation = "ADD"
    math_022.inputs[1].default_value = 0.5
    math_022.inputs[2].default_value = 0.5


    math_023 = nodes.new("ShaderNodeMath")
    math_023.operation = "FRACT"
    math_023.inputs[1].default_value = 0.5
    math_023.inputs[2].default_value = 0.5


    delete_geometry_004 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_004.mode = "ALL"
    delete_geometry_004.domain = "POINT"


    position_009 = nodes.new("GeometryNodeInputPosition")


    separate_x_y_z_008 = nodes.new("ShaderNodeSeparateXYZ")


    compare_009 = nodes.new("FunctionNodeCompare")
    compare_009.operation = "GREATER_THAN"
    compare_009.data_type = "FLOAT"
    compare_009.mode = "ELEMENT"
    compare_009.inputs[1].default_value = 0.0
    compare_009.inputs[2].default_value = 0
    compare_009.inputs[3].default_value = 0
    compare_009.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_009.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_009.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_009.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_009.inputs[8].default_value = ""
    compare_009.inputs[9].default_value = ""
    compare_009.inputs[10].default_value = 0.8999999761581421
    compare_009.inputs[11].default_value = 0.08726649731397629
    compare_009.inputs[12].default_value = 0.0010000000474974513


    float_curve_012 = nodes.new("ShaderNodeFloatCurve")
    float_curve_012.inputs[0].default_value = 1.0


    transform_geometry_031 = nodes.new("GeometryNodeTransform")
    transform_geometry_031.inputs[1].default_value = "Components"
    transform_geometry_031.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_031.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_031.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))


    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.inputs[1].default_value = True


    join_geometry_019 = nodes.new("GeometryNodeJoinGeometry")


    gem_in_holder_4 = nodes.new("GeometryNodeGroup")
    gem_in_holder_4.node_tree = create_gem_in__holder_group()
    gem_in_holder_4.inputs[0].default_value = 0.009999999776482582
    gem_in_holder_4.inputs[1].default_value = "ruby"
    gem_in_holder_4.inputs[2].default_value = False
    gem_in_holder_4.inputs[3].default_value = 0.004999995231628418
    gem_in_holder_4.inputs[4].default_value = 6
    gem_in_holder_4.inputs[5].default_value = 41
    gem_in_holder_4.inputs[6].default_value = False
    gem_in_holder_4.inputs[7].default_value = 6
    gem_in_holder_4.inputs[8].default_value = 10
    gem_in_holder_4.inputs[9].default_value = 0.0020000000949949026
    gem_in_holder_4.inputs[10].default_value = 3.3099989891052246


    join_geometry_020 = nodes.new("GeometryNodeJoinGeometry")


    gem_in_holder_5 = nodes.new("GeometryNodeGroup")
    gem_in_holder_5.node_tree = create_gem_in__holder_group()
    gem_in_holder_5.inputs[0].default_value = 0.009999999776482582
    gem_in_holder_5.inputs[1].default_value = "ruby"
    gem_in_holder_5.inputs[2].default_value = False
    gem_in_holder_5.inputs[3].default_value = 0.004999995231628418
    gem_in_holder_5.inputs[4].default_value = 6
    gem_in_holder_5.inputs[5].default_value = 41
    gem_in_holder_5.inputs[6].default_value = False
    gem_in_holder_5.inputs[7].default_value = 6
    gem_in_holder_5.inputs[8].default_value = 10
    gem_in_holder_5.inputs[9].default_value = 0.0020000000949949026
    gem_in_holder_5.inputs[10].default_value = 5.109997272491455


    transform_geometry_032 = nodes.new("GeometryNodeTransform")
    transform_geometry_032.inputs[1].default_value = "Components"
    transform_geometry_032.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_032.inputs[3].default_value = Euler((0.0, 0.0, 0.01745329238474369), 'XYZ')
    transform_geometry_032.inputs[4].default_value = Vector((1.0, -1.0, 1.0))


    join_geometry_021 = nodes.new("GeometryNodeJoinGeometry")


    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.inputs[1].default_value = True


    gem_in_holder_6 = nodes.new("GeometryNodeGroup")
    gem_in_holder_6.node_tree = create_gem_in__holder_group()
    gem_in_holder_6.inputs[0].default_value = 0.009999999776482582
    gem_in_holder_6.inputs[1].default_value = "ruby"
    gem_in_holder_6.inputs[2].default_value = False
    gem_in_holder_6.inputs[3].default_value = 0.004999995231628418
    gem_in_holder_6.inputs[4].default_value = 6
    gem_in_holder_6.inputs[5].default_value = 41
    gem_in_holder_6.inputs[6].default_value = False
    gem_in_holder_6.inputs[7].default_value = 6
    gem_in_holder_6.inputs[8].default_value = 6
    gem_in_holder_6.inputs[9].default_value = 0.0010000000474974513
    gem_in_holder_6.inputs[10].default_value = 4.80999755859375


    transform_geometry_033 = nodes.new("GeometryNodeTransform")
    transform_geometry_033.inputs[1].default_value = "Components"
    transform_geometry_033.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_033.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_033.inputs[4].default_value = Vector((1.0, -1.0, 1.0))


    join_geometry_022 = nodes.new("GeometryNodeJoinGeometry")


    flip_faces_004 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_004.inputs[1].default_value = True


    transform_geometry_034 = nodes.new("GeometryNodeTransform")
    transform_geometry_034.inputs[1].default_value = "Components"
    transform_geometry_034.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_034.inputs[3].default_value = Euler((0.0, -0.4363323152065277, 0.0), 'XYZ')
    transform_geometry_034.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    join_geometry_017 = nodes.new("GeometryNodeJoinGeometry")


    store_named_attribute_008 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_008.data_type = "BOOLEAN"
    store_named_attribute_008.domain = "POINT"
    store_named_attribute_008.inputs[1].default_value = True
    store_named_attribute_008.inputs[2].default_value = "gold"
    store_named_attribute_008.inputs[3].default_value = True


    store_named_attribute_009 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_009.data_type = "BOOLEAN"
    store_named_attribute_009.domain = "POINT"
    store_named_attribute_009.inputs[1].default_value = True
    store_named_attribute_009.inputs[2].default_value = "saphire"
    store_named_attribute_009.inputs[3].default_value = True


    gem_in_holder_7 = nodes.new("GeometryNodeGroup")
    gem_in_holder_7.node_tree = create_gem_in__holder_group()
    gem_in_holder_7.inputs[0].default_value = 0.006000000052154064
    gem_in_holder_7.inputs[1].default_value = "ruby"
    gem_in_holder_7.inputs[2].default_value = False
    gem_in_holder_7.inputs[3].default_value = 0.004000000189989805
    gem_in_holder_7.inputs[4].default_value = 6
    gem_in_holder_7.inputs[5].default_value = 41
    gem_in_holder_7.inputs[6].default_value = False
    gem_in_holder_7.inputs[7].default_value = 6
    gem_in_holder_7.inputs[8].default_value = 3
    gem_in_holder_7.inputs[9].default_value = 0.0010000000474974513
    gem_in_holder_7.inputs[10].default_value = 5.309997081756592


    instance_on_points_009 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_009.inputs[1].default_value = True
    instance_on_points_009.inputs[3].default_value = False
    instance_on_points_009.inputs[4].default_value = 0
    instance_on_points_009.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_009.inputs[6].default_value = Vector((1.0, 1.0, 1.0))


    curve_circle_012 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_012.mode = "RADIUS"
    curve_circle_012.inputs[0].default_value = 12
    curve_circle_012.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_012.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_012.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_012.inputs[4].default_value = 0.05000000074505806


    transform_geometry_035 = nodes.new("GeometryNodeTransform")
    transform_geometry_035.inputs[1].default_value = "Components"
    transform_geometry_035.inputs[2].default_value = Vector((0.0, 0.003000000026077032, 0.009999999776482582))
    transform_geometry_035.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_035.inputs[4].default_value = Vector((1.4000000953674316, 0.8999999761581421, 1.0))


    frame_025 = nodes.new("NodeFrame")
    frame_025.label = "Satalite Gems"
    frame_025.text = None
    frame_025.shrink = True
    frame_025.label_size = 20


    frame_026 = nodes.new("NodeFrame")
    frame_026.label = "Main Broach"
    frame_026.text = None
    frame_026.shrink = True
    frame_026.label_size = 20


    transform_geometry_036 = nodes.new("GeometryNodeTransform")
    transform_geometry_036.inputs[1].default_value = "Components"
    transform_geometry_036.inputs[2].default_value = Vector((0.0, -0.12600000202655792, 0.36497700214385986))
    transform_geometry_036.inputs[3].default_value = Euler((0.9428269863128662, 0.0, 0.0), 'XYZ')
    transform_geometry_036.inputs[4].default_value = Vector((0.4000000059604645, 0.4000000059604645, 0.4000000059604645))


    store_named_attribute_011 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_011.data_type = "BOOLEAN"
    store_named_attribute_011.domain = "POINT"
    store_named_attribute_011.inputs[1].default_value = True
    store_named_attribute_011.inputs[2].default_value = "skip"
    store_named_attribute_011.inputs[3].default_value = True


    # Parent assignments
    align_rotation_to_vector_004.parent = frame_026
    compare_008.parent = frame_026
    compare_009.parent = frame_026
    cube.parent = frame_026
    cube_001.parent = frame_026
    cube_002.parent = frame_026
    curve_circle_012.parent = frame_025
    curve_tangent_003.parent = frame_026
    curve_to_mesh_005.parent = frame_026
    curve_to_points_002.parent = frame_026
    delete_geometry_002.parent = frame_026
    delete_geometry_003.parent = frame_026
    delete_geometry_004.parent = frame_026
    dual_mesh_001.parent = frame_026
    flip_faces_001.parent = frame_026
    flip_faces_002.parent = frame_026
    flip_faces_003.parent = frame_026
    flip_faces_004.parent = frame_026
    float_curve_012.parent = frame_026
    frame_025.parent = frame_026
    gem_in_holder_3.parent = frame_026
    gem_in_holder_4.parent = frame_026
    gem_in_holder_5.parent = frame_026
    gem_in_holder_6.parent = frame_026
    gem_in_holder_7.parent = frame_025
    gradient_texture.parent = frame_026
    grid_to_mesh.parent = frame_026
    ico_sphere_006.parent = frame_026
    instance_on_points_007.parent = frame_026
    instance_on_points_008.parent = frame_026
    instance_on_points_009.parent = frame_025
    is_edge_boundary_1.parent = frame_026
    join_geometry_016.parent = frame_026
    join_geometry_017.parent = frame_026
    join_geometry_018.parent = frame_026
    join_geometry_019.parent = frame_026
    join_geometry_020.parent = frame_026
    join_geometry_021.parent = frame_026
    join_geometry_022.parent = frame_026
    math_020.parent = frame_026
    math_021.parent = frame_026
    math_022.parent = frame_026
    math_023.parent = frame_026
    merge_by_distance_001.parent = frame_026
    mesh_boolean.parent = frame_026
    mesh_boolean_001.parent = frame_026
    mesh_to_curve_003.parent = frame_026
    mesh_to_s_d_f_grid.parent = frame_026
    mesh_to_s_d_f_grid_001.parent = frame_026
    normal_003.parent = frame_026
    points_to_curves.parent = frame_026
    position_009.parent = frame_026
    quadratic_bézier.parent = frame_026
    realize_instances_003.parent = frame_026
    realize_instances_004.parent = frame_026
    resample_curve_006.parent = frame_026
    resample_curve_007.parent = frame_026
    s_d_f_grid_boolean.parent = frame_026
    separate_x_y_z_008.parent = frame_026
    set_spline_cyclic_002.parent = frame_026
    spline_parameter_009.parent = frame_026
    store_named_attribute_008.parent = frame_026
    store_named_attribute_009.parent = frame_026
    store_named_attribute_011.parent = frame_026
    transform_geometry_026.parent = frame_026
    transform_geometry_027.parent = frame_026
    transform_geometry_028.parent = frame_026
    transform_geometry_029.parent = frame_026
    transform_geometry_030.parent = frame_026
    transform_geometry_031.parent = frame_026
    transform_geometry_032.parent = frame_026
    transform_geometry_033.parent = frame_026
    transform_geometry_034.parent = frame_026
    transform_geometry_035.parent = frame_025
    transform_geometry_036.parent = frame_026
    triangulate.parent = frame_026
    trim_curve_005.parent = frame_026

    # Internal links
    links.new(ico_sphere_006.outputs[0], transform_geometry_026.inputs[0])
    links.new(transform_geometry_026.outputs[0], instance_on_points_007.inputs[2])
    links.new(quadratic_bézier.outputs[0], instance_on_points_007.inputs[0])
    links.new(instance_on_points_007.outputs[0], realize_instances_003.inputs[0])
    links.new(realize_instances_003.outputs[0], mesh_to_s_d_f_grid.inputs[0])
    links.new(triangulate.outputs[0], dual_mesh_001.inputs[0])
    links.new(grid_to_mesh.outputs[0], triangulate.inputs[0])
    links.new(s_d_f_grid_boolean.outputs[0], grid_to_mesh.inputs[0])
    links.new(mesh_to_s_d_f_grid.outputs[0], s_d_f_grid_boolean.inputs[1])
    links.new(mesh_to_s_d_f_grid_001.outputs[0], s_d_f_grid_boolean.inputs[1])
    links.new(cube.outputs[0], transform_geometry_027.inputs[0])
    links.new(transform_geometry_027.outputs[0], mesh_to_s_d_f_grid_001.inputs[0])
    links.new(dual_mesh_001.outputs[0], mesh_boolean.inputs[0])
    links.new(cube_001.outputs[0], transform_geometry_028.inputs[0])
    links.new(transform_geometry_028.outputs[0], mesh_boolean.inputs[1])
    links.new(mesh_boolean.outputs[0], delete_geometry_002.inputs[0])
    links.new(mesh_boolean.outputs[1], delete_geometry_002.inputs[1])
    links.new(dual_mesh_001.outputs[0], mesh_boolean_001.inputs[1])
    links.new(cube_002.outputs[0], transform_geometry_029.inputs[0])
    links.new(transform_geometry_029.outputs[0], mesh_boolean_001.inputs[1])
    links.new(mesh_boolean_001.outputs[0], delete_geometry_003.inputs[0])
    links.new(normal_003.outputs[0], compare_008.inputs[4])
    links.new(compare_008.outputs[0], delete_geometry_003.inputs[1])
    links.new(delete_geometry_003.outputs[0], mesh_to_curve_003.inputs[0])
    links.new(set_spline_cyclic_002.outputs[0], resample_curve_006.inputs[0])
    links.new(curve_to_mesh_005.outputs[0], join_geometry_016.inputs[0])
    links.new(resample_curve_006.outputs[0], curve_to_mesh_005.inputs[0])
    links.new(gem_in_holder_3.outputs[1], curve_to_mesh_005.inputs[1])
    links.new(mesh_to_curve_003.outputs[0], trim_curve_005.inputs[0])
    links.new(resample_curve_007.outputs[0], instance_on_points_008.inputs[0])
    links.new(align_rotation_to_vector_004.outputs[0], instance_on_points_008.inputs[5])
    links.new(curve_tangent_003.outputs[0], align_rotation_to_vector_004.inputs[2])
    links.new(instance_on_points_008.outputs[0], realize_instances_004.inputs[0])
    links.new(delete_geometry_002.outputs[0], transform_geometry_030.inputs[0])
    links.new(transform_geometry_030.outputs[0], flip_faces_002.inputs[0])
    links.new(delete_geometry_002.outputs[0], join_geometry_018.inputs[0])
    links.new(flip_faces_002.outputs[0], join_geometry_018.inputs[0])
    links.new(join_geometry_018.outputs[0], merge_by_distance_001.inputs[0])
    links.new(is_edge_boundary_1.outputs[0], merge_by_distance_001.inputs[1])
    links.new(spline_parameter_009.outputs[0], math_020.inputs[0])
    links.new(math_020.outputs[0], math_021.inputs[0])
    links.new(trim_curve_005.outputs[0], curve_to_points_002.inputs[0])
    links.new(curve_to_points_002.outputs[0], points_to_curves.inputs[0])
    links.new(points_to_curves.outputs[0], set_spline_cyclic_002.inputs[0])
    links.new(gradient_texture.outputs[1], math_022.inputs[0])
    links.new(math_023.outputs[0], points_to_curves.inputs[2])
    links.new(math_022.outputs[0], math_023.inputs[0])
    links.new(delete_geometry_004.outputs[0], resample_curve_007.inputs[0])
    links.new(points_to_curves.outputs[0], delete_geometry_004.inputs[0])
    links.new(position_009.outputs[0], separate_x_y_z_008.inputs[0])
    links.new(separate_x_y_z_008.outputs[0], compare_009.inputs[0])
    links.new(compare_009.outputs[0], delete_geometry_004.inputs[1])
    links.new(math_021.outputs[0], float_curve_012.inputs[1])
    links.new(float_curve_012.outputs[0], instance_on_points_008.inputs[6])
    links.new(realize_instances_004.outputs[0], transform_geometry_031.inputs[0])
    links.new(transform_geometry_031.outputs[0], flip_faces_003.inputs[0])
    links.new(join_geometry_019.outputs[0], join_geometry_016.inputs[0])
    links.new(flip_faces_003.outputs[0], join_geometry_019.inputs[0])
    links.new(realize_instances_004.outputs[0], join_geometry_019.inputs[0])
    links.new(join_geometry_020.outputs[0], instance_on_points_008.inputs[2])
    links.new(gem_in_holder_4.outputs[3], join_geometry_020.inputs[0])
    links.new(gem_in_holder_5.outputs[3], transform_geometry_032.inputs[0])
    links.new(join_geometry_021.outputs[0], join_geometry_020.inputs[0])
    links.new(gem_in_holder_5.outputs[3], join_geometry_021.inputs[0])
    links.new(transform_geometry_032.outputs[0], flip_faces_001.inputs[0])
    links.new(flip_faces_001.outputs[0], join_geometry_021.inputs[0])
    links.new(gem_in_holder_6.outputs[3], transform_geometry_033.inputs[0])
    links.new(gem_in_holder_6.outputs[3], join_geometry_022.inputs[0])
    links.new(transform_geometry_033.outputs[0], flip_faces_004.inputs[0])
    links.new(flip_faces_004.outputs[0], join_geometry_022.inputs[0])
    links.new(transform_geometry_034.outputs[0], join_geometry_020.inputs[0])
    links.new(join_geometry_022.outputs[0], transform_geometry_034.inputs[0])
    links.new(join_geometry_016.outputs[0], store_named_attribute_008.inputs[0])
    links.new(store_named_attribute_008.outputs[0], join_geometry_017.inputs[0])
    links.new(merge_by_distance_001.outputs[0], store_named_attribute_009.inputs[0])
    links.new(store_named_attribute_009.outputs[0], join_geometry_017.inputs[0])
    links.new(gem_in_holder_7.outputs[0], instance_on_points_009.inputs[2])
    links.new(instance_on_points_009.outputs[0], join_geometry_017.inputs[0])
    links.new(transform_geometry_035.outputs[0], instance_on_points_009.inputs[0])
    links.new(curve_circle_012.outputs[0], transform_geometry_035.inputs[0])
    links.new(join_geometry_017.outputs[0], transform_geometry_036.inputs[0])
    links.new(transform_geometry_036.outputs[0], store_named_attribute_011.inputs[0])

    links.new(ico_sphere_006.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
