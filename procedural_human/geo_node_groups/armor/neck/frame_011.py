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
def create_neck_frame_011_group():
    group_name = "Neck_frame_011"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")


    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "GEOMETRY"


    group_input = nodes.new("NodeGroupInput")


    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.inputs[1].default_value = True
    set_spline_cyclic.inputs[2].default_value = False


    trim_curve = nodes.new("GeometryNodeTrimCurve")
    trim_curve.mode = "FACTOR"
    trim_curve.inputs[1].default_value = True
    trim_curve.inputs[2].default_value = 0.0
    trim_curve.inputs[3].default_value = 0.5074577331542969
    trim_curve.inputs[4].default_value = 0.0
    trim_curve.inputs[5].default_value = 1.0


    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.keep_last_segment = True
    resample_curve_001.inputs[1].default_value = True
    resample_curve_001.inputs[2].default_value = "Count"
    resample_curve_001.inputs[3].default_value = 47
    resample_curve_001.inputs[4].default_value = 0.10000000149011612


    gold_decorations = nodes.new("GeometryNodeGroup")
    gold_decorations.node_tree = create_gold__decorations_group()
    gold_decorations.inputs[1].default_value = 68
    gold_decorations.inputs[2].default_value = 2.6999993324279785
    gold_decorations.inputs[3].default_value = 56


    set_curve_normal = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal.inputs[1].default_value = True
    set_curve_normal.inputs[2].default_value = "Free"


    sample_nearest_surface = nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.data_type = "FLOAT_VECTOR"
    sample_nearest_surface.inputs[2].default_value = 0
    sample_nearest_surface.inputs[3].default_value = [0.0, 0.0, 0.0]
    sample_nearest_surface.inputs[4].default_value = 0


    normal = nodes.new("GeometryNodeInputNormal")
    normal.legacy_corner_normals = False


    curve_tangent = nodes.new("GeometryNodeInputTangent")
    vector_math = vec_math_op(
        group,
        "CROSS_PRODUCT",
        sample_nearest_surface.outputs[0],
        curve_tangent.outputs[0],
    )


    frame_005 = nodes.new("NodeFrame")
    frame_005.label = ""
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20


    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.inputs[1].default_value = 100000.0
    gold_on_band.inputs[2].default_value = 8.669999122619629
    gold_on_band.inputs[3].default_value = 1


    frame_011 = nodes.new("NodeFrame")
    frame_011.label = "Gold"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20


    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    gem_in_holder.inputs[1].default_value = "ruby"
    gem_in_holder.inputs[2].default_value = False
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    gem_in_holder.inputs[6].default_value = True


    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.mode = "COUNT"
    curve_to_points.inputs[1].default_value = 8
    curve_to_points.inputs[2].default_value = 0.10000000149011612


    for_each_geometry_element_input = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input.inputs[1].default_value = True


    for_each_geometry_element_output = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.input_items.new("ROTATION", "Rotation")
    for_each_geometry_element_input.pair_with_output(for_each_geometry_element_output)
    for_each_geometry_element_output.active_input_index = 1
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = "POINT"
    for_each_geometry_element_output.inspection_index = 0


    position_002 = nodes.new("GeometryNodeInputPosition")


    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.inputs[1].default_value = "Components"


    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.rotation_space = "LOCAL"
    rotate_rotation.inputs[1].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')


    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.data_type = "INT"
    random_value.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value.inputs[2].default_value = 0.0
    random_value.inputs[3].default_value = 1.0
    random_value.inputs[4].default_value = 5
    random_value.inputs[5].default_value = 7
    random_value.inputs[6].default_value = 0.5
    random_value.inputs[8].default_value = 0


    transform_geometry_008 = nodes.new("GeometryNodeTransform")
    transform_geometry_008.inputs[1].default_value = "Components"
    transform_geometry_008.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    transform_geometry_008.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_008.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.data_type = "FLOAT"
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_001.inputs[2].default_value = 0.3499999940395355
    random_value_001.inputs[3].default_value = 0.75
    random_value_001.inputs[4].default_value = 0
    random_value_001.inputs[5].default_value = 100
    random_value_001.inputs[6].default_value = 0.5
    random_value_001.inputs[8].default_value = 0


    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    store_named_attribute_001.inputs[1].default_value = True
    store_named_attribute_001.inputs[2].default_value = "gold"
    store_named_attribute_001.inputs[3].default_value = True


    random_value_002 = nodes.new("FunctionNodeRandomValue")
    random_value_002.data_type = "FLOAT"
    random_value_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_002.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_002.inputs[2].default_value = 0.0
    random_value_002.inputs[3].default_value = 100.0
    random_value_002.inputs[4].default_value = 3
    random_value_002.inputs[5].default_value = 7
    random_value_002.inputs[6].default_value = 0.5
    random_value_002.inputs[8].default_value = 24


    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.rotation_space = "LOCAL"
    rotate_rotation_001.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')


    random_value_003 = nodes.new("FunctionNodeRandomValue")
    random_value_003.data_type = "FLOAT"
    random_value_003.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_003.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_003.inputs[2].default_value = 0.0010000000474974513
    random_value_003.inputs[3].default_value = 0.004999999888241291
    random_value_003.inputs[4].default_value = 3
    random_value_003.inputs[5].default_value = 7
    random_value_003.inputs[6].default_value = 0.5
    random_value_003.inputs[8].default_value = 0


    random_value_004 = nodes.new("FunctionNodeRandomValue")
    random_value_004.data_type = "INT"
    random_value_004.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_004.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_004.inputs[2].default_value = 0.0010000000474974513
    random_value_004.inputs[3].default_value = 0.004999999888241291
    random_value_004.inputs[4].default_value = 0
    random_value_004.inputs[5].default_value = 100
    random_value_004.inputs[6].default_value = 0.5
    random_value_004.inputs[8].default_value = 0


    random_value_005 = nodes.new("FunctionNodeRandomValue")
    random_value_005.data_type = "INT"
    random_value_005.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_005.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_005.inputs[2].default_value = 0.0010000000474974513
    random_value_005.inputs[3].default_value = 0.004999999888241291
    random_value_005.inputs[4].default_value = 6
    random_value_005.inputs[5].default_value = 20
    random_value_005.inputs[6].default_value = 0.5
    random_value_005.inputs[8].default_value = 0


    random_value_006 = nodes.new("FunctionNodeRandomValue")
    random_value_006.data_type = "INT"
    random_value_006.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_006.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_006.inputs[2].default_value = 0.0010000000474974513
    random_value_006.inputs[3].default_value = 0.004999999888241291
    random_value_006.inputs[4].default_value = 5
    random_value_006.inputs[5].default_value = 30
    random_value_006.inputs[6].default_value = 0.5
    random_value_006.inputs[8].default_value = 0


    frame_012 = nodes.new("NodeFrame")
    frame_012.label = "Broaches"
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20


    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.domain = "FACE"


    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")


    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.operation = "GREATER_THAN"
    compare_002.data_type = "FLOAT"
    compare_002.mode = "ELEMENT"
    compare_002.inputs[1].default_value = 0.8700000047683716
    compare_002.inputs[2].default_value = 0
    compare_002.inputs[3].default_value = 0
    compare_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[8].default_value = ""
    compare_002.inputs[9].default_value = ""
    compare_002.inputs[10].default_value = 0.8999999761581421
    compare_002.inputs[11].default_value = 0.08726649731397629
    compare_002.inputs[12].default_value = 0.0010000000474974513


    trim_curve_001 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_001.mode = "FACTOR"
    trim_curve_001.inputs[1].default_value = True
    trim_curve_001.inputs[2].default_value = 0.18784530460834503
    trim_curve_001.inputs[3].default_value = 0.46817636489868164
    trim_curve_001.inputs[4].default_value = 0.0
    trim_curve_001.inputs[5].default_value = 1.0


    set_curve_normal_001 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.inputs[1].default_value = True
    set_curve_normal_001.inputs[2].default_value = "Free"


    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.operation = "LESS_THAN"
    compare_003.data_type = "FLOAT"
    compare_003.mode = "ELEMENT"
    compare_003.inputs[1].default_value = 0.25999999046325684
    compare_003.inputs[2].default_value = 0
    compare_003.inputs[3].default_value = 0
    compare_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_003.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_003.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_003.inputs[8].default_value = ""
    compare_003.inputs[9].default_value = ""
    compare_003.inputs[10].default_value = 0.8999999761581421
    compare_003.inputs[11].default_value = 0.08726649731397629
    compare_003.inputs[12].default_value = 0.0010000000474974513


    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "OR"


    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.operation = "OR"


    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    compare_004.inputs[1].default_value = 0.5
    compare_004.inputs[2].default_value = 0
    compare_004.inputs[3].default_value = 0
    compare_004.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_004.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_004.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_004.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_004.inputs[8].default_value = ""
    compare_004.inputs[9].default_value = ""
    compare_004.inputs[10].default_value = 0.8999999761581421
    compare_004.inputs[11].default_value = 0.08726649731397629
    compare_004.inputs[12].default_value = 0.020999997854232788


    frame_001 = nodes.new("NodeFrame")
    frame_001.label = "On Band"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20


    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.operation = "AND"


    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.operation = "LESS_THAN"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    compare_005.inputs[1].default_value = 0.5
    compare_005.inputs[2].default_value = 0
    compare_005.inputs[3].default_value = 0
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_005.inputs[8].default_value = ""
    compare_005.inputs[9].default_value = ""
    compare_005.inputs[10].default_value = 0.8999999761581421
    compare_005.inputs[11].default_value = 0.08726649731397629
    compare_005.inputs[12].default_value = 0.020999997854232788


    gem_in_holder_1 = nodes.new("GeometryNodeGroup")
    gem_in_holder_1.node_tree = create_gem_in__holder_group()
    gem_in_holder_1.inputs[0].default_value = 0.009999990463256836
    gem_in_holder_1.inputs[1].default_value = "ruby"
    gem_in_holder_1.inputs[2].default_value = False
    gem_in_holder_1.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_1.inputs[4].default_value = 20
    gem_in_holder_1.inputs[5].default_value = 10
    gem_in_holder_1.inputs[6].default_value = False
    gem_in_holder_1.inputs[7].default_value = 6
    gem_in_holder_1.inputs[8].default_value = 10


    mesh_to_curve_002 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.mode = "EDGES"


    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.node_tree = create_is__edge__boundary_group()


    set_spline_cyclic_001 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_001.inputs[1].default_value = True
    set_spline_cyclic_001.inputs[2].default_value = False


    trim_curve_004 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_004.mode = "FACTOR"
    trim_curve_004.inputs[1].default_value = True
    trim_curve_004.inputs[2].default_value = 0.03867403417825699
    trim_curve_004.inputs[3].default_value = 0.4364641308784485
    trim_curve_004.inputs[4].default_value = 0.0
    trim_curve_004.inputs[5].default_value = 1.0


    curve_to_points_001 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.mode = "COUNT"
    curve_to_points_001.inputs[1].default_value = 50
    curve_to_points_001.inputs[2].default_value = 0.10000000149011612


    set_curve_normal_002 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_002.inputs[1].default_value = True
    set_curve_normal_002.inputs[2].default_value = "Free"


    position_004 = nodes.new("GeometryNodeInputPosition")


    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.inputs[1].default_value = True


    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.input_items.new("ROTATION", "Rotation")
    for_each_geometry_element_input_001.pair_with_output(for_each_geometry_element_output_001)
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0


    transform_geometry_009 = nodes.new("GeometryNodeTransform")
    transform_geometry_009.inputs[1].default_value = "Components"
    transform_geometry_009.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.rotation_space = "LOCAL"
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, -1.5707963705062866, 0.0), 'XYZ')


    frame_014 = nodes.new("NodeFrame")
    frame_014.label = "Random Wings"
    frame_014.text = None
    frame_014.shrink = True
    frame_014.label_size = 20


    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.data_type = "FLOAT"
    random_value_007.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_007.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_007.inputs[2].default_value = 6.0
    random_value_007.inputs[3].default_value = 7.0
    random_value_007.inputs[4].default_value = 0
    random_value_007.inputs[5].default_value = 100
    random_value_007.inputs[6].default_value = 0.5
    random_value_007.inputs[8].default_value = 33


    random_value_008 = nodes.new("FunctionNodeRandomValue")
    random_value_008.data_type = "FLOAT"
    random_value_008.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_008.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_008.inputs[2].default_value = 0.0
    random_value_008.inputs[3].default_value = 0.003000000026077032
    random_value_008.inputs[4].default_value = 0
    random_value_008.inputs[5].default_value = 100
    random_value_008.inputs[6].default_value = 0.5
    random_value_008.inputs[8].default_value = 10


    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    distribute_points_on_faces.inputs[1].default_value = True
    distribute_points_on_faces.inputs[2].default_value = 0.0
    distribute_points_on_faces.inputs[3].default_value = 10.0
    distribute_points_on_faces.inputs[4].default_value = 5000.0
    distribute_points_on_faces.inputs[5].default_value = 1.0
    distribute_points_on_faces.inputs[6].default_value = 1


    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.inputs[1].default_value = True
    instance_on_points.inputs[3].default_value = False
    instance_on_points.inputs[4].default_value = 0
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')


    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.inputs[0].default_value = 0.004000000189989805
    ico_sphere.inputs[1].default_value = 2


    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "INSTANCE"
    store_named_attribute_002.inputs[1].default_value = True
    store_named_attribute_002.inputs[2].default_value = "ruby"


    random_value_009 = nodes.new("FunctionNodeRandomValue")
    random_value_009.data_type = "BOOLEAN"
    random_value_009.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_009.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_009.inputs[2].default_value = 0.0
    random_value_009.inputs[3].default_value = 1.0
    random_value_009.inputs[4].default_value = 0
    random_value_009.inputs[5].default_value = 100
    random_value_009.inputs[6].default_value = 0.5
    random_value_009.inputs[7].default_value = 0
    random_value_009.inputs[8].default_value = 0


    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.operation = "NOT"
    boolean_math_003.inputs[1].default_value = False


    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "INSTANCE"
    store_named_attribute_003.inputs[1].default_value = True
    store_named_attribute_003.inputs[2].default_value = "saphire"


    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.inputs[1].default_value = True
    realize_instances_001.inputs[2].default_value = True
    realize_instances_001.inputs[3].default_value = 0


    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.domain = "FACE"
    set_shade_smooth_003.inputs[1].default_value = True
    set_shade_smooth_003.inputs[2].default_value = True


    frame_015 = nodes.new("NodeFrame")
    frame_015.label = "Random Jewels"
    frame_015.text = None
    frame_015.shrink = True
    frame_015.label_size = 20


    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketGeometry"


    distribute_points_on_faces_001 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_001.distribute_method = "POISSON"
    distribute_points_on_faces_001.use_legacy_normal = False
    distribute_points_on_faces_001.inputs[2].default_value = 0.009999999776482582
    distribute_points_on_faces_001.inputs[3].default_value = 5000.0
    distribute_points_on_faces_001.inputs[4].default_value = 500.0
    distribute_points_on_faces_001.inputs[5].default_value = 1.0
    distribute_points_on_faces_001.inputs[6].default_value = 0


    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.target_element = "POINTS"
    geometry_proximity.inputs[1].default_value = 0
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity.inputs[3].default_value = 0


    compare_006 = nodes.new("FunctionNodeCompare")
    compare_006.operation = "LESS_THAN"
    compare_006.data_type = "FLOAT"
    compare_006.mode = "ELEMENT"
    compare_006.inputs[1].default_value = 0.0010000000474974513
    compare_006.inputs[2].default_value = 0
    compare_006.inputs[3].default_value = 0
    compare_006.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_006.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_006.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_006.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_006.inputs[8].default_value = ""
    compare_006.inputs[9].default_value = ""
    compare_006.inputs[10].default_value = 0.8999999761581421
    compare_006.inputs[11].default_value = 0.08726649731397629
    compare_006.inputs[12].default_value = 0.0010000000474974513


    gem_in_holder_2 = nodes.new("GeometryNodeGroup")
    gem_in_holder_2.node_tree = create_gem_in__holder_group()
    gem_in_holder_2.inputs[0].default_value = 0.009999990463256836
    gem_in_holder_2.inputs[1].default_value = "ruby"
    gem_in_holder_2.inputs[2].default_value = False
    gem_in_holder_2.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_2.inputs[4].default_value = 20
    gem_in_holder_2.inputs[5].default_value = 10
    gem_in_holder_2.inputs[6].default_value = False
    gem_in_holder_2.inputs[7].default_value = 6
    gem_in_holder_2.inputs[8].default_value = 10
    gem_in_holder_2.inputs[9].default_value = 0.0010000000474974513
    gem_in_holder_2.inputs[10].default_value = 6.6099958419799805


    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.inputs[1].default_value = True
    instance_on_points_001.inputs[3].default_value = False
    instance_on_points_001.inputs[4].default_value = 0


    random_value_010 = nodes.new("FunctionNodeRandomValue")
    random_value_010.data_type = "FLOAT"
    random_value_010.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_010.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_010.inputs[2].default_value = 0.10000000894069672
    random_value_010.inputs[3].default_value = 0.4000000059604645
    random_value_010.inputs[4].default_value = 0
    random_value_010.inputs[5].default_value = 100
    random_value_010.inputs[6].default_value = 0.5
    random_value_010.inputs[7].default_value = 0
    random_value_010.inputs[8].default_value = 0


    frame_016 = nodes.new("NodeFrame")
    frame_016.label = "Larger Jewels"
    frame_016.text = None
    frame_016.shrink = True
    frame_016.label_size = 20


    realize_instances_002 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.inputs[1].default_value = True
    realize_instances_002.inputs[2].default_value = True
    realize_instances_002.inputs[3].default_value = 0


    transform_geometry_010 = nodes.new("GeometryNodeTransform")
    transform_geometry_010.inputs[1].default_value = "Components"
    transform_geometry_010.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    transform_geometry_010.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_010.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.inputs[2].default_value = "ruby"
    swap_attr.inputs[3].default_value = "saphire"


    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.capture_items.new("INT", "Value")
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "INSTANCE"


    index = nodes.new("GeometryNodeInputIndex")


    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[1].default_value = True
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))


    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.target_element = "FACES"
    geometry_proximity_001.inputs[1].default_value = 0
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_001.inputs[3].default_value = 0


    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.inputs[3].default_value = False


    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.domain = "CURVE"


    compare_007 = nodes.new("FunctionNodeCompare")
    compare_007.operation = "EQUAL"
    compare_007.data_type = "FLOAT"
    compare_007.mode = "ELEMENT"
    compare_007.inputs[1].default_value = 0.5
    compare_007.inputs[2].default_value = 0
    compare_007.inputs[3].default_value = 0
    compare_007.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_007.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_007.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_007.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_007.inputs[8].default_value = ""
    compare_007.inputs[9].default_value = ""
    compare_007.inputs[10].default_value = 0.8999999761581421
    compare_007.inputs[11].default_value = 0.08726649731397629
    compare_007.inputs[12].default_value = 0.0010000000474974513


    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")


    trim_curve_002 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_002.mode = "FACTOR"
    trim_curve_002.inputs[1].default_value = True
    trim_curve_002.inputs[2].default_value = 0.0
    trim_curve_002.inputs[3].default_value = 0.8690060973167419
    trim_curve_002.inputs[4].default_value = 0.0
    trim_curve_002.inputs[5].default_value = 1.0


    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.keep_last_segment = True
    resample_curve_002.inputs[1].default_value = True
    resample_curve_002.inputs[2].default_value = "Count"
    resample_curve_002.inputs[3].default_value = 47
    resample_curve_002.inputs[4].default_value = 0.10000000149011612


    gold_decorations_1 = nodes.new("GeometryNodeGroup")
    gold_decorations_1.node_tree = create_gold__decorations_group()
    gold_decorations_1.inputs[1].default_value = 75
    gold_decorations_1.inputs[2].default_value = 3.0999999046325684
    gold_decorations_1.inputs[3].default_value = 6


    set_curve_normal_003 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_003.inputs[1].default_value = True
    set_curve_normal_003.inputs[2].default_value = "Z Up"
    set_curve_normal_003.inputs[3].default_value = Vector((0.0, 0.0, 1.0))


    frame_013 = nodes.new("NodeFrame")
    frame_013.label = ""
    frame_013.text = None
    frame_013.shrink = True
    frame_013.label_size = 20


    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.inputs[1].default_value = "Components"
    transform_geometry.inputs[2].default_value = Vector((0.0, -0.0010000000474974513, 0.0))
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    random_value_011 = nodes.new("FunctionNodeRandomValue")
    random_value_011.data_type = "FLOAT"
    random_value_011.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_011.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_011.inputs[2].default_value = 0.20000000298023224
    random_value_011.inputs[3].default_value = 0.6000000238418579
    random_value_011.inputs[4].default_value = 0
    random_value_011.inputs[5].default_value = 100
    random_value_011.inputs[6].default_value = 0.5
    random_value_011.inputs[7].default_value = 0
    random_value_011.inputs[8].default_value = 0


    trim_curve_003 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_003.mode = "FACTOR"
    trim_curve_003.inputs[1].default_value = True
    trim_curve_003.inputs[2].default_value = 0.10000000149011612
    trim_curve_003.inputs[3].default_value = 0.5
    trim_curve_003.inputs[4].default_value = 0.0
    trim_curve_003.inputs[5].default_value = 1.0


    resample_curve_003 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.keep_last_segment = True
    resample_curve_003.inputs[1].default_value = True
    resample_curve_003.inputs[2].default_value = "Count"
    resample_curve_003.inputs[3].default_value = 47
    resample_curve_003.inputs[4].default_value = 0.10000000149011612


    gold_decorations_2 = nodes.new("GeometryNodeGroup")
    gold_decorations_2.node_tree = create_gold__decorations_group()
    gold_decorations_2.inputs[1].default_value = 78
    gold_decorations_2.inputs[2].default_value = 3.1999998092651367
    gold_decorations_2.inputs[3].default_value = 13


    set_curve_normal_004 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_004.inputs[1].default_value = True
    set_curve_normal_004.inputs[2].default_value = "Free"


    frame_017 = nodes.new("NodeFrame")
    frame_017.label = ""
    frame_017.text = None
    frame_017.shrink = True
    frame_017.label_size = 20


    transform_geometry_011 = nodes.new("GeometryNodeTransform")
    transform_geometry_011.inputs[1].default_value = "Components"
    transform_geometry_011.inputs[2].default_value = Vector((0.0, 0.0, -0.003000000026077032))
    transform_geometry_011.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_011.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.mode = "EDGES"
    mesh_to_curve.inputs[1].default_value = True


    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.inputs[1].default_value = True
    set_curve_tilt.inputs[2].default_value = -0.34819304943084717


    reroute_002 = nodes.new("NodeReroute")
    reroute_002.socket_idname = "NodeSocketGeometry"


    instance_on_points_010 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_010.inputs[1].default_value = True
    instance_on_points_010.inputs[3].default_value = False
    instance_on_points_010.inputs[4].default_value = 0
    instance_on_points_010.inputs[6].default_value = Vector((0.6000000238418579, 0.6000000238418579, 0.6000000238418579))


    gem_in_holder_8 = nodes.new("GeometryNodeGroup")
    gem_in_holder_8.node_tree = create_gem_in__holder_group()
    gem_in_holder_8.inputs[0].default_value = 0.009999999776482582
    gem_in_holder_8.inputs[1].default_value = "ruby"
    gem_in_holder_8.inputs[2].default_value = True
    gem_in_holder_8.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_8.inputs[4].default_value = 20
    gem_in_holder_8.inputs[5].default_value = 10
    gem_in_holder_8.inputs[6].default_value = False
    gem_in_holder_8.inputs[7].default_value = 6
    gem_in_holder_8.inputs[8].default_value = 10
    gem_in_holder_8.inputs[9].default_value = 0.0020000000949949026
    gem_in_holder_8.inputs[10].default_value = 2.5099997520446777


    realize_instances_005 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_005.inputs[1].default_value = True
    realize_instances_005.inputs[2].default_value = True
    realize_instances_005.inputs[3].default_value = 0


    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.capture_items.new("INT", "Value")
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "INSTANCE"


    index_002 = nodes.new("GeometryNodeInputIndex")


    resample_curve_008 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_008.keep_last_segment = True
    resample_curve_008.inputs[1].default_value = True
    resample_curve_008.inputs[2].default_value = "Count"
    resample_curve_008.inputs[3].default_value = 10
    resample_curve_008.inputs[4].default_value = 0.10000000149011612


    align_rotation_to_vector_005 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_005.axis = "X"
    align_rotation_to_vector_005.pivot_axis = "AUTO"
    align_rotation_to_vector_005.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_005.inputs[1].default_value = 1.0


    normal_004 = nodes.new("GeometryNodeInputNormal")
    normal_004.legacy_corner_normals = False


    align_rotation_to_vector_006 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_006.axis = "Y"
    align_rotation_to_vector_006.pivot_axis = "AUTO"
    align_rotation_to_vector_006.inputs[1].default_value = 1.0


    curve_tangent_004 = nodes.new("GeometryNodeInputTangent")


    frame_027 = nodes.new("NodeFrame")
    frame_027.label = "Collar Gems"
    frame_027.text = None
    frame_027.shrink = True
    frame_027.label_size = 20


    trim_curve_006 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_006.mode = "FACTOR"
    trim_curve_006.inputs[1].default_value = True
    trim_curve_006.inputs[2].default_value = 0.009999999776482582
    trim_curve_006.inputs[3].default_value = 0.940000057220459
    trim_curve_006.inputs[4].default_value = 0.0
    trim_curve_006.inputs[5].default_value = 1.0


    gem_in_holder_9 = nodes.new("GeometryNodeGroup")
    gem_in_holder_9.node_tree = create_gem_in__holder_group()
    gem_in_holder_9.inputs[0].default_value = 0.009999999776482582
    gem_in_holder_9.inputs[1].default_value = "ruby"
    gem_in_holder_9.inputs[2].default_value = False
    gem_in_holder_9.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_9.inputs[6].default_value = True


    curve_to_points_003 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_003.mode = "COUNT"
    curve_to_points_003.inputs[1].default_value = 2
    curve_to_points_003.inputs[2].default_value = 0.10000000149011612


    for_each_geometry_element_input_002 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_002.inputs[1].default_value = True


    for_each_geometry_element_output_002 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_002.input_items.new("ROTATION", "Rotation")
    for_each_geometry_element_input_002.pair_with_output(for_each_geometry_element_output_002)
    for_each_geometry_element_output_002.active_input_index = 1
    for_each_geometry_element_output_002.active_generation_index = 0
    for_each_geometry_element_output_002.active_main_index = 0
    for_each_geometry_element_output_002.domain = "POINT"
    for_each_geometry_element_output_002.inspection_index = 0


    position_010 = nodes.new("GeometryNodeInputPosition")


    transform_geometry_037 = nodes.new("GeometryNodeTransform")
    transform_geometry_037.inputs[1].default_value = "Components"


    rotate_rotation_007 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_007.rotation_space = "LOCAL"
    rotate_rotation_007.inputs[1].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')


    random_value_014 = nodes.new("FunctionNodeRandomValue")
    random_value_014.data_type = "INT"
    random_value_014.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_014.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_014.inputs[2].default_value = 0.0
    random_value_014.inputs[3].default_value = 1.0
    random_value_014.inputs[4].default_value = 5
    random_value_014.inputs[5].default_value = 7
    random_value_014.inputs[6].default_value = 0.5
    random_value_014.inputs[8].default_value = 0


    transform_geometry_038 = nodes.new("GeometryNodeTransform")
    transform_geometry_038.inputs[1].default_value = "Components"
    transform_geometry_038.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    transform_geometry_038.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_038.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    trim_curve_007 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_007.mode = "FACTOR"
    trim_curve_007.inputs[1].default_value = True
    trim_curve_007.inputs[2].default_value = 0.4000000059604645
    trim_curve_007.inputs[3].default_value = 0.75
    trim_curve_007.inputs[4].default_value = 0.0
    trim_curve_007.inputs[5].default_value = 1.0


    random_value_015 = nodes.new("FunctionNodeRandomValue")
    random_value_015.data_type = "FLOAT"
    random_value_015.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_015.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_015.inputs[2].default_value = 0.25
    random_value_015.inputs[3].default_value = 0.550000011920929
    random_value_015.inputs[4].default_value = 0
    random_value_015.inputs[5].default_value = 100
    random_value_015.inputs[6].default_value = 0.5
    random_value_015.inputs[8].default_value = 0


    store_named_attribute_010 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_010.data_type = "BOOLEAN"
    store_named_attribute_010.domain = "POINT"
    store_named_attribute_010.inputs[1].default_value = True
    store_named_attribute_010.inputs[2].default_value = "skip"
    store_named_attribute_010.inputs[3].default_value = True


    random_value_016 = nodes.new("FunctionNodeRandomValue")
    random_value_016.data_type = "FLOAT"
    random_value_016.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_016.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_016.inputs[2].default_value = 0.0
    random_value_016.inputs[3].default_value = 100.0
    random_value_016.inputs[4].default_value = 3
    random_value_016.inputs[5].default_value = 7
    random_value_016.inputs[6].default_value = 0.5
    random_value_016.inputs[8].default_value = 16


    rotate_rotation_008 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_008.rotation_space = "LOCAL"
    rotate_rotation_008.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')


    random_value_017 = nodes.new("FunctionNodeRandomValue")
    random_value_017.data_type = "FLOAT"
    random_value_017.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_017.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_017.inputs[2].default_value = 0.0010000000474974513
    random_value_017.inputs[3].default_value = 0.004999999888241291
    random_value_017.inputs[4].default_value = 3
    random_value_017.inputs[5].default_value = 7
    random_value_017.inputs[6].default_value = 0.5
    random_value_017.inputs[8].default_value = 0


    random_value_018 = nodes.new("FunctionNodeRandomValue")
    random_value_018.data_type = "INT"
    random_value_018.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_018.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_018.inputs[2].default_value = 0.0010000000474974513
    random_value_018.inputs[3].default_value = 0.004999999888241291
    random_value_018.inputs[4].default_value = 0
    random_value_018.inputs[5].default_value = 100
    random_value_018.inputs[6].default_value = 0.5
    random_value_018.inputs[8].default_value = 0


    random_value_019 = nodes.new("FunctionNodeRandomValue")
    random_value_019.data_type = "INT"
    random_value_019.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_019.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_019.inputs[2].default_value = 0.0010000000474974513
    random_value_019.inputs[3].default_value = 0.004999999888241291
    random_value_019.inputs[4].default_value = 6
    random_value_019.inputs[5].default_value = 20
    random_value_019.inputs[6].default_value = 0.5
    random_value_019.inputs[8].default_value = 0


    random_value_020 = nodes.new("FunctionNodeRandomValue")
    random_value_020.data_type = "INT"
    random_value_020.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_020.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_020.inputs[2].default_value = 0.0010000000474974513
    random_value_020.inputs[3].default_value = 0.004999999888241291
    random_value_020.inputs[4].default_value = 5
    random_value_020.inputs[5].default_value = 30
    random_value_020.inputs[6].default_value = 0.5
    random_value_020.inputs[8].default_value = 0


    frame_028 = nodes.new("NodeFrame")
    frame_028.label = "Broaches"
    frame_028.text = None
    frame_028.shrink = True
    frame_028.label_size = 20


    store_named_attribute_012 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_012.data_type = "BOOLEAN"
    store_named_attribute_012.domain = "POINT"
    store_named_attribute_012.inputs[1].default_value = True
    store_named_attribute_012.inputs[2].default_value = "skip"
    store_named_attribute_012.inputs[3].default_value = True


    mesh_boolean_002 = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean_002.operation = "DIFFERENCE"
    mesh_boolean_002.solver = "FLOAT"
    mesh_boolean_002.inputs[2].default_value = False
    mesh_boolean_002.inputs[3].default_value = False


    ico_sphere_007 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_007.inputs[0].default_value = 0.07800000160932541
    ico_sphere_007.inputs[1].default_value = 3


    transform_geometry_039 = nodes.new("GeometryNodeTransform")
    transform_geometry_039.inputs[1].default_value = "Components"
    transform_geometry_039.inputs[2].default_value = Vector((0.0, -0.019999999552965164, 0.47999998927116394))
    transform_geometry_039.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_039.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    store_named_attribute_013 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_013.data_type = "BOOLEAN"
    store_named_attribute_013.domain = "POINT"
    store_named_attribute_013.inputs[2].default_value = "saphire"
    store_named_attribute_013.inputs[3].default_value = True


    boolean_math_005 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.operation = "AND"


    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.data_type = "BOOLEAN"
    named_attribute.inputs[0].default_value = "ruby"


    store_named_attribute_014 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_014.data_type = "BOOLEAN"
    store_named_attribute_014.domain = "POINT"
    store_named_attribute_014.inputs[2].default_value = "ruby"
    store_named_attribute_014.inputs[3].default_value = False


    math_017 = nodes.new("ShaderNodeMath")
    math_017.operation = "FLOORED_MODULO"
    math_017.inputs[1].default_value = 2.0
    math_017.inputs[2].default_value = 0.5


    # Parent assignments
    align_rotation_to_vector_005.parent = frame_027
    align_rotation_to_vector_006.parent = frame_027
    boolean_math.parent = frame_001
    boolean_math_001.parent = frame_001
    boolean_math_002.parent = frame_001
    boolean_math_003.parent = frame_015
    boolean_math_005.parent = frame_027
    capture_attribute_001.parent = frame_016
    capture_attribute_002.parent = frame_027
    compare_002.parent = frame_001
    compare_003.parent = frame_001
    compare_004.parent = frame_001
    compare_005.parent = frame_001
    compare_006.parent = frame_016
    compare_007.parent = frame_013
    curve_tangent.parent = frame_005
    curve_tangent_004.parent = frame_027
    curve_to_mesh.parent = frame_014
    curve_to_points.parent = frame_012
    curve_to_points_001.parent = frame_014
    curve_to_points_003.parent = frame_028
    distribute_points_on_faces.parent = frame_015
    distribute_points_on_faces_001.parent = frame_016
    for_each_geometry_element_input.parent = frame_012
    for_each_geometry_element_input_001.parent = frame_014
    for_each_geometry_element_input_002.parent = frame_028
    for_each_geometry_element_output.parent = frame_012
    for_each_geometry_element_output_001.parent = frame_014
    for_each_geometry_element_output_002.parent = frame_028
    frame_001.parent = frame_011
    frame_005.parent = frame_011
    frame_012.parent = frame_011
    frame_013.parent = frame_011
    frame_014.parent = frame_011
    frame_015.parent = frame_011
    frame_016.parent = frame_011
    frame_017.parent = frame_011
    frame_027.parent = frame_011
    frame_028.parent = frame_011
    gem_in_holder.parent = frame_012
    gem_in_holder_1.parent = frame_014
    gem_in_holder_2.parent = frame_016
    gem_in_holder_8.parent = frame_027
    gem_in_holder_9.parent = frame_028
    geometry_proximity.parent = frame_016
    geometry_proximity_001.parent = frame_014
    gold_decorations.parent = frame_005
    gold_decorations_1.parent = frame_013
    gold_decorations_2.parent = frame_017
    gold_on_band.parent = frame_001
    group_input.parent = frame_011
    ico_sphere.parent = frame_015
    ico_sphere_007.parent = frame_017
    index.parent = frame_016
    index_002.parent = frame_027
    instance_on_points.parent = frame_015
    instance_on_points_001.parent = frame_016
    instance_on_points_010.parent = frame_027
    is_edge_boundary.parent = frame_014
    join_geometry_002.parent = frame_011
    math_017.parent = frame_027
    mesh_boolean_002.parent = frame_017
    mesh_to_curve.parent = frame_017
    mesh_to_curve_002.parent = frame_014
    named_attribute.parent = frame_027
    normal.parent = frame_011
    normal_004.parent = frame_027
    position_002.parent = frame_012
    position_004.parent = frame_014
    position_010.parent = frame_028
    random_value.parent = frame_012
    random_value_001.parent = frame_012
    random_value_002.parent = frame_012
    random_value_003.parent = frame_012
    random_value_004.parent = frame_012
    random_value_005.parent = frame_012
    random_value_006.parent = frame_012
    random_value_007.parent = frame_014
    random_value_008.parent = frame_014
    random_value_009.parent = frame_015
    random_value_010.parent = frame_016
    random_value_011.parent = frame_015
    random_value_014.parent = frame_028
    random_value_015.parent = frame_028
    random_value_016.parent = frame_028
    random_value_017.parent = frame_028
    random_value_018.parent = frame_028
    random_value_019.parent = frame_028
    random_value_020.parent = frame_028
    realize_instances_001.parent = frame_015
    realize_instances_002.parent = frame_016
    realize_instances_005.parent = frame_027
    reroute_001.parent = frame_016
    reroute_002.parent = frame_011
    resample_curve_001.parent = frame_005
    resample_curve_002.parent = frame_013
    resample_curve_003.parent = frame_017
    resample_curve_008.parent = frame_027
    rotate_rotation.parent = frame_012
    rotate_rotation_001.parent = frame_012
    rotate_rotation_002.parent = frame_014
    rotate_rotation_007.parent = frame_028
    rotate_rotation_008.parent = frame_028
    sample_nearest_surface.parent = frame_011
    separate_geometry_001.parent = frame_001
    separate_geometry_002.parent = frame_013
    separate_x_y_z_003.parent = frame_001
    separate_x_y_z_004.parent = frame_013
    set_curve_normal.parent = frame_005
    set_curve_normal_001.parent = frame_012
    set_curve_normal_002.parent = frame_014
    set_curve_normal_003.parent = frame_013
    set_curve_normal_004.parent = frame_017
    set_curve_tilt.parent = frame_017
    set_position_001.parent = frame_014
    set_shade_smooth_003.parent = frame_015
    set_spline_cyclic.parent = frame_011
    set_spline_cyclic_001.parent = frame_014
    store_named_attribute_001.parent = frame_014
    store_named_attribute_002.parent = frame_015
    store_named_attribute_003.parent = frame_015
    store_named_attribute_010.parent = frame_028
    store_named_attribute_012.parent = frame_028
    store_named_attribute_013.parent = frame_027
    store_named_attribute_014.parent = frame_027
    swap_attr.parent = frame_016
    switch.parent = frame_011
    transform_geometry.parent = frame_013
    transform_geometry_007.parent = frame_012
    transform_geometry_008.parent = frame_012
    transform_geometry_009.parent = frame_014
    transform_geometry_010.parent = frame_016
    transform_geometry_011.parent = frame_017
    transform_geometry_037.parent = frame_028
    transform_geometry_038.parent = frame_028
    transform_geometry_039.parent = frame_017
    trim_curve.parent = frame_005
    trim_curve_001.parent = frame_012
    trim_curve_002.parent = frame_013
    trim_curve_003.parent = frame_017
    trim_curve_004.parent = frame_014
    trim_curve_006.parent = frame_027
    trim_curve_007.parent = frame_028

    # Internal links
    links.new(join_geometry_002.outputs[0], switch.inputs[2])
    links.new(group_input.outputs[0], switch.inputs[0])
    links.new(set_spline_cyclic.outputs[0], trim_curve.inputs[0])
    links.new(trim_curve.outputs[0], resample_curve_001.inputs[0])
    links.new(gold_decorations.outputs[0], join_geometry_002.inputs[0])
    links.new(set_curve_normal.outputs[0], gold_decorations.inputs[0])
    links.new(resample_curve_001.outputs[0], set_curve_normal.inputs[0])
    links.new(normal.outputs[0], sample_nearest_surface.inputs[1])
    links.new(curve_to_points.outputs[0], for_each_geometry_element_input.inputs[0])
    links.new(curve_to_points.outputs[3], for_each_geometry_element_input.inputs[2])
    links.new(for_each_geometry_element_output.outputs[2], join_geometry_002.inputs[0])
    links.new(position_002.outputs[0], for_each_geometry_element_input.inputs[2])
    links.new(gem_in_holder.outputs[0], transform_geometry_007.inputs[0])
    links.new(for_each_geometry_element_input.outputs[2], transform_geometry_007.inputs[2])
    links.new(for_each_geometry_element_input.outputs[2], rotate_rotation.inputs[0])
    links.new(for_each_geometry_element_input.outputs[0], random_value.inputs[7])
    links.new(random_value.outputs[2], gem_in_holder.inputs[7])
    links.new(transform_geometry_007.outputs[0], transform_geometry_008.inputs[0])
    links.new(transform_geometry_008.outputs[0], for_each_geometry_element_output.inputs[1])
    links.new(for_each_geometry_element_input.outputs[0], random_value_001.inputs[7])
    links.new(random_value_001.outputs[1], transform_geometry_007.inputs[4])
    links.new(for_each_geometry_element_input.outputs[0], random_value_002.inputs[7])
    links.new(random_value_002.outputs[1], gem_in_holder.inputs[10])
    links.new(rotate_rotation_001.outputs[0], transform_geometry_007.inputs[3])
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])
    links.new(for_each_geometry_element_input.outputs[0], random_value_003.inputs[7])
    links.new(random_value_003.outputs[1], gem_in_holder.inputs[9])
    links.new(for_each_geometry_element_input.outputs[0], random_value_004.inputs[7])
    links.new(random_value_004.outputs[2], gem_in_holder.inputs[5])
    links.new(for_each_geometry_element_input.outputs[0], random_value_005.inputs[7])
    links.new(random_value_005.outputs[2], gem_in_holder.inputs[4])
    links.new(for_each_geometry_element_input.outputs[0], random_value_006.inputs[7])
    links.new(random_value_006.outputs[2], gem_in_holder.inputs[8])
    links.new(separate_geometry_001.outputs[0], gold_on_band.inputs[0])
    links.new(separate_x_y_z_003.outputs[0], compare_002.inputs[0])
    links.new(set_spline_cyclic.outputs[0], trim_curve_001.inputs[0])
    links.new(set_curve_normal_001.outputs[0], curve_to_points.inputs[0])
    links.new(trim_curve_001.outputs[0], set_curve_normal_001.inputs[0])
    links.new(sample_nearest_surface.outputs[0], set_curve_normal_001.inputs[3])
    links.new(separate_x_y_z_003.outputs[0], compare_003.inputs[0])
    links.new(compare_002.outputs[0], boolean_math.inputs[0])
    links.new(compare_003.outputs[0], boolean_math.inputs[1])
    links.new(boolean_math.outputs[0], boolean_math_001.inputs[0])
    links.new(separate_x_y_z_003.outputs[1], compare_004.inputs[0])
    links.new(compare_004.outputs[0], boolean_math_001.inputs[1])
    links.new(boolean_math_002.outputs[0], separate_geometry_001.inputs[1])
    links.new(boolean_math_001.outputs[0], boolean_math_002.inputs[0])
    links.new(separate_x_y_z_003.outputs[1], compare_005.inputs[0])
    links.new(compare_005.outputs[0], boolean_math_002.inputs[1])
    links.new(separate_geometry_001.outputs[0], mesh_to_curve_002.inputs[0])
    links.new(is_edge_boundary.outputs[0], mesh_to_curve_002.inputs[1])
    links.new(set_spline_cyclic_001.outputs[0], trim_curve_004.inputs[0])
    links.new(trim_curve_004.outputs[0], curve_to_points_001.inputs[0])
    links.new(set_curve_normal_002.outputs[0], set_spline_cyclic_001.inputs[0])
    links.new(mesh_to_curve_002.outputs[0], set_curve_normal_002.inputs[0])
    links.new(sample_nearest_surface.outputs[0], set_curve_normal_002.inputs[3])
    links.new(curve_to_points_001.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(position_004.outputs[0], for_each_geometry_element_input_001.inputs[2])
    links.new(curve_to_points_001.outputs[3], for_each_geometry_element_input_001.inputs[2])
    links.new(store_named_attribute_001.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_002.inputs[0])
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_009.inputs[2])
    links.new(gem_in_holder_1.outputs[4], transform_geometry_009.inputs[0])
    links.new(rotate_rotation_002.outputs[0], transform_geometry_009.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[2], rotate_rotation_002.inputs[0])
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_1.inputs[10])
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_008.inputs[7])
    links.new(random_value_008.outputs[1], gem_in_holder_1.inputs[9])
    links.new(separate_geometry_001.outputs[0], distribute_points_on_faces.inputs[0])
    links.new(distribute_points_on_faces.outputs[0], instance_on_points.inputs[0])
    links.new(instance_on_points.outputs[0], store_named_attribute_002.inputs[0])
    links.new(random_value_009.outputs[3], store_named_attribute_002.inputs[3])
    links.new(random_value_009.outputs[3], boolean_math_003.inputs[0])
    links.new(store_named_attribute_002.outputs[0], store_named_attribute_003.inputs[0])
    links.new(boolean_math_003.outputs[0], store_named_attribute_003.inputs[3])
    links.new(store_named_attribute_003.outputs[0], realize_instances_001.inputs[0])
    links.new(realize_instances_001.outputs[0], join_geometry_002.inputs[0])
    links.new(set_shade_smooth_003.outputs[0], instance_on_points.inputs[2])
    links.new(ico_sphere.outputs[0], set_shade_smooth_003.inputs[0])
    links.new(reroute_001.outputs[0], distribute_points_on_faces_001.inputs[0])
    links.new(for_each_geometry_element_output_001.outputs[2], geometry_proximity.inputs[0])
    links.new(geometry_proximity.outputs[1], compare_006.inputs[0])
    links.new(compare_006.outputs[0], distribute_points_on_faces_001.inputs[1])
    links.new(distribute_points_on_faces_001.outputs[0], instance_on_points_001.inputs[0])
    links.new(distribute_points_on_faces_001.outputs[2], instance_on_points_001.inputs[5])
    links.new(random_value_010.outputs[1], instance_on_points_001.inputs[6])
    links.new(transform_geometry_010.outputs[0], instance_on_points_001.inputs[2])
    links.new(gem_in_holder_2.outputs[0], transform_geometry_010.inputs[0])
    links.new(realize_instances_002.outputs[0], swap_attr.inputs[0])
    links.new(swap_attr.outputs[0], join_geometry_002.inputs[0])
    links.new(capture_attribute_001.outputs[0], realize_instances_002.inputs[0])
    links.new(instance_on_points_001.outputs[0], capture_attribute_001.inputs[0])
    links.new(capture_attribute_001.outputs[1], swap_attr.inputs[1])
    links.new(index.outputs[0], capture_attribute_001.inputs[1])
    links.new(transform_geometry_009.outputs[0], set_position_001.inputs[0])
    links.new(geometry_proximity_001.outputs[0], set_position_001.inputs[2])
    links.new(set_position_001.outputs[0], curve_to_mesh.inputs[0])
    links.new(gem_in_holder_1.outputs[1], curve_to_mesh.inputs[1])
    links.new(gem_in_holder_1.outputs[2], curve_to_mesh.inputs[2])
    links.new(curve_to_mesh.outputs[0], store_named_attribute_001.inputs[0])
    links.new(compare_007.outputs[0], separate_geometry_002.inputs[1])
    links.new(separate_x_y_z_004.outputs[1], compare_007.inputs[0])
    links.new(separate_geometry_002.outputs[0], trim_curve_002.inputs[0])
    links.new(trim_curve_002.outputs[0], resample_curve_002.inputs[0])
    links.new(gold_decorations_1.outputs[0], join_geometry_002.inputs[0])
    links.new(resample_curve_002.outputs[0], set_curve_normal_003.inputs[0])
    links.new(transform_geometry.outputs[0], gold_decorations_1.inputs[0])
    links.new(set_curve_normal_003.outputs[0], transform_geometry.inputs[0])
    links.new(random_value_011.outputs[1], instance_on_points.inputs[6])
    links.new(trim_curve_003.outputs[0], resample_curve_003.inputs[0])
    links.new(resample_curve_003.outputs[0], set_curve_normal_004.inputs[0])
    links.new(transform_geometry_011.outputs[0], gold_decorations_2.inputs[0])
    links.new(mesh_to_curve.outputs[0], trim_curve_003.inputs[0])
    links.new(set_curve_tilt.outputs[0], transform_geometry_011.inputs[0])
    links.new(set_curve_normal_004.outputs[0], set_curve_tilt.inputs[0])
    links.new(reroute_002.outputs[0], join_geometry_002.inputs[0])
    links.new(gold_on_band.outputs[0], reroute_002.inputs[0])
    links.new(gem_in_holder_8.outputs[0], instance_on_points_010.inputs[2])
    links.new(capture_attribute_002.outputs[0], realize_instances_005.inputs[0])
    links.new(instance_on_points_010.outputs[0], capture_attribute_002.inputs[0])
    links.new(index_002.outputs[0], capture_attribute_002.inputs[1])
    links.new(resample_curve_008.outputs[0], instance_on_points_010.inputs[0])
    links.new(align_rotation_to_vector_006.outputs[0], instance_on_points_010.inputs[5])
    links.new(align_rotation_to_vector_005.outputs[0], align_rotation_to_vector_006.inputs[0])
    links.new(normal_004.outputs[0], align_rotation_to_vector_006.inputs[2])
    links.new(curve_tangent_004.outputs[0], align_rotation_to_vector_005.inputs[2])
    links.new(trim_curve_006.outputs[0], resample_curve_008.inputs[0])
    links.new(set_curve_tilt.outputs[0], trim_curve_006.inputs[0])
    links.new(curve_to_points_003.outputs[0], for_each_geometry_element_input_002.inputs[0])
    links.new(curve_to_points_003.outputs[3], for_each_geometry_element_input_002.inputs[2])
    links.new(position_010.outputs[0], for_each_geometry_element_input_002.inputs[2])
    links.new(gem_in_holder_9.outputs[0], transform_geometry_037.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[2], transform_geometry_037.inputs[2])
    links.new(for_each_geometry_element_input_002.outputs[2], rotate_rotation_007.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_014.inputs[7])
    links.new(random_value_014.outputs[2], gem_in_holder_9.inputs[7])
    links.new(transform_geometry_037.outputs[0], transform_geometry_038.inputs[0])
    links.new(trim_curve_007.outputs[0], curve_to_points_003.inputs[0])
    links.new(separate_geometry_002.outputs[0], trim_curve_007.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_015.inputs[7])
    links.new(random_value_015.outputs[1], transform_geometry_037.inputs[4])
    links.new(store_named_attribute_010.outputs[0], for_each_geometry_element_output_002.inputs[1])
    links.new(transform_geometry_038.outputs[0], store_named_attribute_010.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_016.inputs[7])
    links.new(random_value_016.outputs[1], gem_in_holder_9.inputs[10])
    links.new(rotate_rotation_008.outputs[0], transform_geometry_037.inputs[3])
    links.new(rotate_rotation_007.outputs[0], rotate_rotation_008.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_017.inputs[7])
    links.new(random_value_017.outputs[1], gem_in_holder_9.inputs[9])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_018.inputs[7])
    links.new(random_value_018.outputs[2], gem_in_holder_9.inputs[5])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_019.inputs[7])
    links.new(random_value_019.outputs[2], gem_in_holder_9.inputs[4])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_020.inputs[7])
    links.new(random_value_020.outputs[2], gem_in_holder_9.inputs[8])
    links.new(store_named_attribute_012.outputs[0], join_geometry_002.inputs[0])
    links.new(for_each_geometry_element_output_002.outputs[2], store_named_attribute_012.inputs[0])
    links.new(mesh_boolean_002.outputs[0], join_geometry_002.inputs[0])
    links.new(gold_decorations_2.outputs[0], mesh_boolean_002.inputs[0])
    links.new(transform_geometry_039.outputs[0], mesh_boolean_002.inputs[1])
    links.new(ico_sphere_007.outputs[0], transform_geometry_039.inputs[0])
    links.new(realize_instances_005.outputs[0], store_named_attribute_013.inputs[0])
    links.new(boolean_math_005.outputs[0], store_named_attribute_013.inputs[1])
    links.new(named_attribute.outputs[0], boolean_math_005.inputs[1])
    links.new(store_named_attribute_013.outputs[0], store_named_attribute_014.inputs[0])
    links.new(boolean_math_005.outputs[0], store_named_attribute_014.inputs[1])
    links.new(store_named_attribute_014.outputs[0], join_geometry_002.inputs[0])
    links.new(math_017.outputs[0], boolean_math_005.inputs[0])
    links.new(capture_attribute_002.outputs[1], math_017.inputs[0])

    links.new(join_geometry_002.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
