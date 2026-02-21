import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
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

@geo_node_group
def create_neck_group():
    group_name = "Neck"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    quadratic_bézier_003 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_003.inputs[0].default_value = 40
    quadratic_bézier_003.inputs[1].default_value = Vector((0.0, -0.13999998569488525, 0.3499999940395355))
    quadratic_bézier_003.inputs[2].default_value = Vector((0.0, -0.10000000149011612, 0.39500001072883606))

    bi_rail_loft = nodes.new("GeometryNodeGroup")
    bi_rail_loft.node_tree = create_bi_rail_loft_group()
    bi_rail_loft.inputs[3].default_value = 0
    bi_rail_loft.inputs[5].default_value = 0.009999999776482582
    bi_rail_loft.inputs[6].default_value = 0.029999999329447746
    bi_rail_loft.inputs[7].default_value = 42
    bi_rail_loft.inputs[8].default_value = 148

    quadratic_bézier_004 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_004.inputs[0].default_value = 40
    quadratic_bézier_004.inputs[2].default_value = Vector((0.0, -0.07999999821186066, 0.4399999976158142))
    quadratic_bézier_004.inputs[3].default_value = Vector((0.0, -0.08999999612569809, 0.45000001788139343))

    join_splines = nodes.new("GeometryNodeGroup")
    join_splines.node_tree = create_join__splines_group()

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    links.new(quadratic_bézier_003.outputs[0], join_geometry_005.inputs[0])
    links.new(quadratic_bézier_004.outputs[0], join_geometry_005.inputs[0])
    links.new(join_geometry_005.outputs[0], join_splines.inputs[0])

    vector = nodes.new("FunctionNodeInputVector")
    vector.vector = Vector((0.0, -0.08999999612569809, 0.42000001668930054))
    links.new(vector.outputs[0], quadratic_bézier_003.inputs[3])
    links.new(vector.outputs[0], quadratic_bézier_004.inputs[1])

    frame_006 = nodes.new("NodeFrame")
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20

    quadratic_bézier_006 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_006.inputs[0].default_value = 40
    quadratic_bézier_006.inputs[1].default_value = Vector((-0.15000000596046448, 0.0, 0.429999977350235))
    quadratic_bézier_006.inputs[2].default_value = Vector((-0.10000000894069672, 0.0, 0.44999998807907104))

    quadratic_bézier_007 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_007.inputs[0].default_value = 40
    quadratic_bézier_007.inputs[2].default_value = Vector((-0.0650000050663948, 0.0, 0.4899999797344208))
    quadratic_bézier_007.inputs[3].default_value = Vector((-0.07500000298023224, 0.0, 0.5))

    join_splines_1 = nodes.new("GeometryNodeGroup")
    join_splines_1.node_tree = create_join__splines_group()

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_006.outputs[0], join_splines_1.inputs[0])
    links.new(quadratic_bézier_006.outputs[0], join_geometry_006.inputs[0])
    links.new(quadratic_bézier_007.outputs[0], join_geometry_006.inputs[0])

    vector_001 = nodes.new("FunctionNodeInputVector")
    vector_001.vector = Vector((-0.08500001579523087, 0.0, 0.4699999988079071))
    links.new(vector_001.outputs[0], quadratic_bézier_006.inputs[3])
    links.new(vector_001.outputs[0], quadratic_bézier_007.inputs[1])

    frame_007 = nodes.new("NodeFrame")
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_008.outputs[0], bi_rail_loft.inputs[2])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.inputs[1].default_value = "Components"
    transform_geometry_002.inputs[2].default_value = Vector((0.0, -0.019999999552965164, 0.4800000488758087))
    transform_geometry_002.inputs[3].default_value = Euler((0.4064871668815613, 0.0, 0.0), 'XYZ')
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_002.outputs[0], bi_rail_loft.inputs[1])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.inputs[1].default_value = "Components"
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.3700000047683716))
    transform_geometry_003.inputs[3].default_value = Euler((0.15620698034763336, 0.0, 0.0), 'XYZ')
    transform_geometry_003.inputs[4].default_value = Vector((1.2599999904632568, 1.0, 1.0))

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.mode = "RADIUS"
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle.inputs[4].default_value = 0.08000004291534424

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.mode = "RADIUS"
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_001.inputs[4].default_value = 0.12999996542930603

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.inputs[1].default_value = True
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(transform_geometry_003.outputs[0], set_position.inputs[0])
    links.new(set_position.outputs[0], bi_rail_loft.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position.outputs[0], separate_x_y_z.inputs[0])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.clamp = False
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    map_range.inputs[1].default_value = -0.14000000059604645
    map_range.inputs[2].default_value = 0.14000000059604645
    map_range.inputs[3].default_value = 0.0
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(separate_x_y_z.outputs[1], map_range.inputs[0])

    frame_008 = nodes.new("NodeFrame")
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20

    float_curve_001 = nodes.new("ShaderNodeFloatCurve")
    float_curve_001.inputs[0].default_value = 1.0
    links.new(map_range.outputs[0], float_curve_001.inputs[1])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.inputs[0].default_value = 0.0
    combine_x_y_z.inputs[1].default_value = 0.0
    links.new(combine_x_y_z.outputs[0], set_position.inputs[3])
    links.new(float_curve_001.outputs[0], combine_x_y_z.inputs[2])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.inputs[1].default_value = "Components"
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_004.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(curve_circle_001.outputs[0], transform_geometry_004.inputs[0])
    links.new(transform_geometry_004.outputs[0], transform_geometry_003.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.inputs[1].default_value = "Components"
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_005.outputs[0], transform_geometry_002.inputs[0])
    links.new(curve_circle.outputs[0], transform_geometry_005.inputs[0])

    closure_input_001 = nodes.new("NodeClosureInput")

    closure_output_001 = nodes.new("NodeClosureOutput")
    closure_output_001.active_input_index = 0
    closure_output_001.active_output_index = 0
    closure_output_001.define_signature = False
    links.new(closure_output_001.outputs[0], bi_rail_loft.inputs[9])

    math = nodes.new("ShaderNodeMath")
    math.operation = "PINGPONG"
    math.inputs[1].default_value = 0.25
    math.inputs[2].default_value = 0.5
    links.new(closure_input_001.outputs[0], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.operation = "MULTIPLY"
    math_001.inputs[1].default_value = 4.0
    math_001.inputs[2].default_value = 0.5
    links.new(math_001.outputs[0], closure_output_001.inputs[0])
    links.new(math.outputs[0], math_001.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.inputs[1].default_value = "Components"
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_001.inputs[3].default_value = Euler((1.5446162223815918, 0.0, 0.0), 'XYZ')
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_001.outputs[0], join_geometry_008.inputs[0])
    links.new(join_splines_1.outputs[0], transform_geometry_001.inputs[0])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.inputs[1].default_value = "Components"
    transform_geometry_006.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')
    transform_geometry_006.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_006.outputs[0], join_geometry_008.inputs[0])
    links.new(join_splines.outputs[0], transform_geometry_006.inputs[0])

    integer = nodes.new("FunctionNodeInputInt")
    integer.integer = 73
    links.new(integer.outputs[0], curve_circle_001.inputs[0])
    links.new(integer.outputs[0], curve_circle.inputs[0])

    frame_009 = nodes.new("NodeFrame")
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20

    frame_010 = nodes.new("NodeFrame")
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "FACE"

    position_001 = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_001.outputs[0], separate_x_y_z_001.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "GREATER_EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    compare.inputs[1].default_value = 0.0
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
    links.new(separate_x_y_z_001.outputs[0], compare.inputs[0])
    links.new(compare.outputs[0], delete_geometry.inputs[1])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.node_tree = create_pipes_group()

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry.outputs[0], delete_geometry.inputs[0])
    links.new(bi_rail_loft.outputs[0], join_geometry.inputs[0])
    links.new(pipes.outputs[0], join_geometry.inputs[0])

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(bi_rail_loft.outputs[2], separate_x_y_z_002.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.operation = "EQUAL"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    compare_001.inputs[1].default_value = 0.8799999356269836
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
    compare_001.inputs[12].default_value = 0.02099999599158764
    links.new(separate_x_y_z_002.outputs[0], compare_001.inputs[0])

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.domain = "POINT"
    links.new(bi_rail_loft.outputs[0], separate_geometry.inputs[0])
    links.new(compare_001.outputs[0], separate_geometry.inputs[1])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_001.outputs[0], pipes.inputs[0])
    links.new(bi_rail_loft.outputs[0], join_geometry_001.inputs[0])
    links.new(separate_geometry.outputs[0], join_geometry_001.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.text = None
    frame.shrink = True
    frame.label_size = 20

    rivet = nodes.new("GeometryNodeGroup")
    rivet.node_tree = create_rivet_group()
    rivet.inputs[1].default_value = False
    rivet.inputs[2].default_value = -1.059999942779541
    rivet.inputs[3].default_value = 0.9399999976158142
    links.new(bi_rail_loft.outputs[0], rivet.inputs[0])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.inputs[1].default_value = True
    realize_instances.inputs[2].default_value = True
    realize_instances.inputs[3].default_value = 0
    links.new(realize_instances.outputs[0], join_geometry.inputs[0])
    links.new(rivet.outputs[0], realize_instances.inputs[0])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.domain = "FACE"
    set_shade_smooth.inputs[1].default_value = True
    set_shade_smooth.inputs[2].default_value = True
    links.new(delete_geometry.outputs[0], set_shade_smooth.inputs[0])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "GEOMETRY"
    links.new(join_geometry_002.outputs[0], switch.inputs[2])

    group_input = nodes.new("NodeGroupInput")
    links.new(group_input.outputs[0], switch.inputs[0])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.inputs[1].default_value = True
    set_spline_cyclic.inputs[2].default_value = False
    links.new(set_position.outputs[0], set_spline_cyclic.inputs[0])

    trim_curve = nodes.new("GeometryNodeTrimCurve")
    trim_curve.mode = "FACTOR"
    trim_curve.inputs[1].default_value = True
    trim_curve.inputs[2].default_value = 0.0
    trim_curve.inputs[3].default_value = 0.5074577331542969
    trim_curve.inputs[4].default_value = 0.0
    trim_curve.inputs[5].default_value = 1.0
    links.new(set_spline_cyclic.outputs[0], trim_curve.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.keep_last_segment = True
    resample_curve_001.inputs[1].default_value = True
    resample_curve_001.inputs[2].default_value = "Count"
    resample_curve_001.inputs[3].default_value = 47
    resample_curve_001.inputs[4].default_value = 0.10000000149011612
    links.new(trim_curve.outputs[0], resample_curve_001.inputs[0])

    gold_decorations = nodes.new("GeometryNodeGroup")
    gold_decorations.node_tree = create_gold__decorations_group()
    gold_decorations.inputs[1].default_value = 68
    gold_decorations.inputs[2].default_value = 2.6999993324279785
    gold_decorations.inputs[3].default_value = 56
    links.new(gold_decorations.outputs[0], join_geometry_002.inputs[0])

    set_curve_normal = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal.inputs[1].default_value = True
    set_curve_normal.inputs[2].default_value = "Free"
    links.new(set_curve_normal.outputs[0], gold_decorations.inputs[0])
    links.new(resample_curve_001.outputs[0], set_curve_normal.inputs[0])

    sample_nearest_surface = nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.data_type = "FLOAT_VECTOR"
    sample_nearest_surface.inputs[2].default_value = 0
    sample_nearest_surface.inputs[3].default_value = [0.0, 0.0, 0.0]
    sample_nearest_surface.inputs[4].default_value = 0
    links.new(bi_rail_loft.outputs[0], sample_nearest_surface.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.legacy_corner_normals = False
    links.new(normal.outputs[0], sample_nearest_surface.inputs[1])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    vector_math = vec_math_op(
        group,
        "CROSS_PRODUCT",
        sample_nearest_surface.outputs[0],
        curve_tangent.outputs[0],
    )
    links.new(vector_math, set_curve_normal.inputs[3])

    frame_005 = nodes.new("NodeFrame")
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.inputs[1].default_value = 100000.0
    gold_on_band.inputs[2].default_value = 8.669999122619629
    gold_on_band.inputs[3].default_value = 1

    frame_011 = nodes.new("NodeFrame")
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
    links.new(curve_to_points.outputs[0], for_each_geometry_element_input.inputs[0])
    links.new(curve_to_points.outputs[3], for_each_geometry_element_input.inputs[2])

    for_each_geometry_element_output = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.active_input_index = 1
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = "POINT"
    for_each_geometry_element_output.inspection_index = 0
    links.new(for_each_geometry_element_output.outputs[2], join_geometry_002.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    links.new(position_002.outputs[0], for_each_geometry_element_input.inputs[2])

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.inputs[1].default_value = "Components"
    links.new(gem_in_holder.outputs[0], transform_geometry_007.inputs[0])
    links.new(for_each_geometry_element_input.outputs[2], transform_geometry_007.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.rotation_space = "LOCAL"
    rotate_rotation.inputs[1].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')
    links.new(for_each_geometry_element_input.outputs[2], rotate_rotation.inputs[0])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value.inputs[7])
    links.new(random_value.outputs[2], gem_in_holder.inputs[7])

    transform_geometry_008 = nodes.new("GeometryNodeTransform")
    transform_geometry_008.inputs[1].default_value = "Components"
    transform_geometry_008.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    transform_geometry_008.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_008.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_007.outputs[0], transform_geometry_008.inputs[0])
    links.new(transform_geometry_008.outputs[0], for_each_geometry_element_output.inputs[1])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value_001.inputs[7])
    links.new(random_value_001.outputs[1], transform_geometry_007.inputs[4])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value_002.inputs[7])
    links.new(random_value_002.outputs[1], gem_in_holder.inputs[10])

    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.rotation_space = "LOCAL"
    rotate_rotation_001.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
    links.new(rotate_rotation_001.outputs[0], transform_geometry_007.inputs[3])
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value_003.inputs[7])
    links.new(random_value_003.outputs[1], gem_in_holder.inputs[9])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value_004.inputs[7])
    links.new(random_value_004.outputs[2], gem_in_holder.inputs[5])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value_005.inputs[7])
    links.new(random_value_005.outputs[2], gem_in_holder.inputs[4])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value_006.inputs[7])
    links.new(random_value_006.outputs[2], gem_in_holder.inputs[8])

    frame_012 = nodes.new("NodeFrame")
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.domain = "FACE"
    links.new(bi_rail_loft.outputs[0], separate_geometry_001.inputs[0])
    links.new(separate_geometry_001.outputs[0], gold_on_band.inputs[0])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(bi_rail_loft.outputs[2], separate_x_y_z_003.inputs[0])

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
    links.new(separate_x_y_z_003.outputs[0], compare_002.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_004.outputs[0], group_output.inputs[0])
    links.new(set_shade_smooth.outputs[0], join_geometry_004.inputs[0])
    links.new(switch.outputs[0], join_geometry_004.inputs[0])

    trim_curve_001 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_001.mode = "FACTOR"
    trim_curve_001.inputs[1].default_value = True
    trim_curve_001.inputs[2].default_value = 0.18784530460834503
    trim_curve_001.inputs[3].default_value = 0.46817636489868164
    trim_curve_001.inputs[4].default_value = 0.0
    trim_curve_001.inputs[5].default_value = 1.0
    links.new(set_spline_cyclic.outputs[0], trim_curve_001.inputs[0])

    set_curve_normal_001 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.inputs[1].default_value = True
    set_curve_normal_001.inputs[2].default_value = "Free"
    links.new(set_curve_normal_001.outputs[0], curve_to_points.inputs[0])
    links.new(trim_curve_001.outputs[0], set_curve_normal_001.inputs[0])
    links.new(sample_nearest_surface.outputs[0], set_curve_normal_001.inputs[3])

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
    links.new(separate_x_y_z_003.outputs[0], compare_003.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "OR"
    links.new(compare_002.outputs[0], boolean_math.inputs[0])
    links.new(compare_003.outputs[0], boolean_math.inputs[1])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.operation = "OR"
    links.new(boolean_math.outputs[0], boolean_math_001.inputs[0])

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
    links.new(separate_x_y_z_003.outputs[1], compare_004.inputs[0])
    links.new(compare_004.outputs[0], boolean_math_001.inputs[1])

    frame_001 = nodes.new("NodeFrame")
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.operation = "AND"
    links.new(boolean_math_002.outputs[0], separate_geometry_001.inputs[1])
    links.new(boolean_math_001.outputs[0], boolean_math_002.inputs[0])

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
    links.new(separate_x_y_z_003.outputs[1], compare_005.inputs[0])
    links.new(compare_005.outputs[0], boolean_math_002.inputs[1])

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
    links.new(separate_geometry_001.outputs[0], mesh_to_curve_002.inputs[0])

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    links.new(is_edge_boundary.outputs[0], mesh_to_curve_002.inputs[1])

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
    links.new(set_spline_cyclic_001.outputs[0], trim_curve_004.inputs[0])

    curve_to_points_001 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.mode = "COUNT"
    curve_to_points_001.inputs[1].default_value = 50
    curve_to_points_001.inputs[2].default_value = 0.10000000149011612
    links.new(trim_curve_004.outputs[0], curve_to_points_001.inputs[0])

    set_curve_normal_002 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_002.inputs[1].default_value = True
    set_curve_normal_002.inputs[2].default_value = "Free"
    links.new(set_curve_normal_002.outputs[0], set_spline_cyclic_001.inputs[0])
    links.new(mesh_to_curve_002.outputs[0], set_curve_normal_002.inputs[0])
    links.new(sample_nearest_surface.outputs[0], set_curve_normal_002.inputs[3])

    position_004 = nodes.new("GeometryNodeInputPosition")

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.inputs[1].default_value = True
    links.new(curve_to_points_001.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(position_004.outputs[0], for_each_geometry_element_input_001.inputs[2])
    links.new(curve_to_points_001.outputs[3], for_each_geometry_element_input_001.inputs[2])

    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    links.new(store_named_attribute_001.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_002.inputs[0])

    transform_geometry_009 = nodes.new("GeometryNodeTransform")
    transform_geometry_009.inputs[1].default_value = "Components"
    transform_geometry_009.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_009.inputs[2])
    links.new(gem_in_holder_1.outputs[4], transform_geometry_009.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.rotation_space = "LOCAL"
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, -1.5707963705062866, 0.0), 'XYZ')
    links.new(rotate_rotation_002.outputs[0], transform_geometry_009.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[2], rotate_rotation_002.inputs[0])

    frame_014 = nodes.new("NodeFrame")
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
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_1.inputs[10])

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
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_008.inputs[7])
    links.new(random_value_008.outputs[1], gem_in_holder_1.inputs[9])

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    distribute_points_on_faces.inputs[1].default_value = True
    distribute_points_on_faces.inputs[2].default_value = 0.0
    distribute_points_on_faces.inputs[3].default_value = 10.0
    distribute_points_on_faces.inputs[4].default_value = 5000.0
    distribute_points_on_faces.inputs[5].default_value = 1.0
    distribute_points_on_faces.inputs[6].default_value = 1
    links.new(separate_geometry_001.outputs[0], distribute_points_on_faces.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.inputs[1].default_value = True
    instance_on_points.inputs[3].default_value = False
    instance_on_points.inputs[4].default_value = 0
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    links.new(distribute_points_on_faces.outputs[0], instance_on_points.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.inputs[0].default_value = 0.004000000189989805
    ico_sphere.inputs[1].default_value = 2

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "INSTANCE"
    store_named_attribute_002.inputs[1].default_value = True
    store_named_attribute_002.inputs[2].default_value = "ruby"
    links.new(instance_on_points.outputs[0], store_named_attribute_002.inputs[0])

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
    links.new(random_value_009.outputs[3], store_named_attribute_002.inputs[3])

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.operation = "NOT"
    boolean_math_003.inputs[1].default_value = False
    links.new(random_value_009.outputs[3], boolean_math_003.inputs[0])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "INSTANCE"
    store_named_attribute_003.inputs[1].default_value = True
    store_named_attribute_003.inputs[2].default_value = "saphire"
    links.new(store_named_attribute_002.outputs[0], store_named_attribute_003.inputs[0])
    links.new(boolean_math_003.outputs[0], store_named_attribute_003.inputs[3])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.inputs[1].default_value = True
    realize_instances_001.inputs[2].default_value = True
    realize_instances_001.inputs[3].default_value = 0
    links.new(store_named_attribute_003.outputs[0], realize_instances_001.inputs[0])
    links.new(realize_instances_001.outputs[0], join_geometry_002.inputs[0])

    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.domain = "FACE"
    set_shade_smooth_003.inputs[1].default_value = True
    set_shade_smooth_003.inputs[2].default_value = True
    links.new(set_shade_smooth_003.outputs[0], instance_on_points.inputs[2])
    links.new(ico_sphere.outputs[0], set_shade_smooth_003.inputs[0])

    frame_015 = nodes.new("NodeFrame")
    frame_015.text = None
    frame_015.shrink = True
    frame_015.label_size = 20

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketGeometry"
    links.new(bi_rail_loft.outputs[0], reroute_001.inputs[0])

    distribute_points_on_faces_001 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_001.distribute_method = "POISSON"
    distribute_points_on_faces_001.use_legacy_normal = False
    distribute_points_on_faces_001.inputs[2].default_value = 0.009999999776482582
    distribute_points_on_faces_001.inputs[3].default_value = 5000.0
    distribute_points_on_faces_001.inputs[4].default_value = 500.0
    distribute_points_on_faces_001.inputs[5].default_value = 1.0
    distribute_points_on_faces_001.inputs[6].default_value = 0
    links.new(reroute_001.outputs[0], distribute_points_on_faces_001.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.target_element = "POINTS"
    geometry_proximity.inputs[1].default_value = 0
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity.inputs[3].default_value = 0
    links.new(for_each_geometry_element_output_001.outputs[2], geometry_proximity.inputs[0])

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
    links.new(geometry_proximity.outputs[1], compare_006.inputs[0])
    links.new(compare_006.outputs[0], distribute_points_on_faces_001.inputs[1])

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
    links.new(distribute_points_on_faces_001.outputs[0], instance_on_points_001.inputs[0])
    links.new(distribute_points_on_faces_001.outputs[2], instance_on_points_001.inputs[5])

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
    links.new(random_value_010.outputs[1], instance_on_points_001.inputs[6])

    frame_016 = nodes.new("NodeFrame")
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
    links.new(transform_geometry_010.outputs[0], instance_on_points_001.inputs[2])
    links.new(gem_in_holder_2.outputs[0], transform_geometry_010.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.inputs[2].default_value = "ruby"
    swap_attr.inputs[3].default_value = "saphire"
    links.new(realize_instances_002.outputs[0], swap_attr.inputs[0])
    links.new(swap_attr.outputs[0], join_geometry_002.inputs[0])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "INSTANCE"
    links.new(capture_attribute_001.outputs[0], realize_instances_002.inputs[0])
    links.new(instance_on_points_001.outputs[0], capture_attribute_001.inputs[0])
    links.new(capture_attribute_001.outputs[1], swap_attr.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    links.new(index.outputs[0], capture_attribute_001.inputs[1])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[1].default_value = True
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(transform_geometry_009.outputs[0], set_position_001.inputs[0])

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.target_element = "FACES"
    geometry_proximity_001.inputs[1].default_value = 0
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_001.inputs[3].default_value = 0
    links.new(bi_rail_loft.outputs[0], geometry_proximity_001.inputs[0])
    links.new(geometry_proximity_001.outputs[0], set_position_001.inputs[2])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.inputs[3].default_value = False
    links.new(set_position_001.outputs[0], curve_to_mesh.inputs[0])
    links.new(gem_in_holder_1.outputs[1], curve_to_mesh.inputs[1])
    links.new(gem_in_holder_1.outputs[2], curve_to_mesh.inputs[2])
    links.new(curve_to_mesh.outputs[0], store_named_attribute_001.inputs[0])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.domain = "CURVE"
    links.new(bi_rail_loft.outputs[1], separate_geometry_002.inputs[0])

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
    links.new(compare_007.outputs[0], separate_geometry_002.inputs[1])

    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(bi_rail_loft.outputs[2], separate_x_y_z_004.inputs[0])
    links.new(separate_x_y_z_004.outputs[1], compare_007.inputs[0])

    trim_curve_002 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_002.mode = "FACTOR"
    trim_curve_002.inputs[1].default_value = True
    trim_curve_002.inputs[2].default_value = 0.0
    trim_curve_002.inputs[3].default_value = 0.8690060973167419
    trim_curve_002.inputs[4].default_value = 0.0
    trim_curve_002.inputs[5].default_value = 1.0
    links.new(separate_geometry_002.outputs[0], trim_curve_002.inputs[0])

    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.keep_last_segment = True
    resample_curve_002.inputs[1].default_value = True
    resample_curve_002.inputs[2].default_value = "Count"
    resample_curve_002.inputs[3].default_value = 47
    resample_curve_002.inputs[4].default_value = 0.10000000149011612
    links.new(trim_curve_002.outputs[0], resample_curve_002.inputs[0])

    gold_decorations_1 = nodes.new("GeometryNodeGroup")
    gold_decorations_1.node_tree = create_gold__decorations_group()
    gold_decorations_1.inputs[1].default_value = 75
    gold_decorations_1.inputs[2].default_value = 3.0999999046325684
    gold_decorations_1.inputs[3].default_value = 6
    links.new(gold_decorations_1.outputs[0], join_geometry_002.inputs[0])

    set_curve_normal_003 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_003.inputs[1].default_value = True
    set_curve_normal_003.inputs[2].default_value = "Z Up"
    set_curve_normal_003.inputs[3].default_value = Vector((0.0, 0.0, 1.0))
    links.new(resample_curve_002.outputs[0], set_curve_normal_003.inputs[0])

    frame_013 = nodes.new("NodeFrame")
    frame_013.text = None
    frame_013.shrink = True
    frame_013.label_size = 20

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.inputs[1].default_value = "Components"
    transform_geometry.inputs[2].default_value = Vector((0.0, -0.0010000000474974513, 0.0))
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry.outputs[0], gold_decorations_1.inputs[0])
    links.new(set_curve_normal_003.outputs[0], transform_geometry.inputs[0])

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
    links.new(random_value_011.outputs[1], instance_on_points.inputs[6])

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
    links.new(trim_curve_003.outputs[0], resample_curve_003.inputs[0])

    gold_decorations_2 = nodes.new("GeometryNodeGroup")
    gold_decorations_2.node_tree = create_gold__decorations_group()
    gold_decorations_2.inputs[1].default_value = 78
    gold_decorations_2.inputs[2].default_value = 3.1999998092651367
    gold_decorations_2.inputs[3].default_value = 13

    set_curve_normal_004 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_004.inputs[1].default_value = True
    set_curve_normal_004.inputs[2].default_value = "Free"
    links.new(resample_curve_003.outputs[0], set_curve_normal_004.inputs[0])
    links.new(vector_math, set_curve_normal_004.inputs[3])

    frame_017 = nodes.new("NodeFrame")
    frame_017.text = None
    frame_017.shrink = True
    frame_017.label_size = 20

    transform_geometry_011 = nodes.new("GeometryNodeTransform")
    transform_geometry_011.inputs[1].default_value = "Components"
    transform_geometry_011.inputs[2].default_value = Vector((0.0, 0.0, -0.003000000026077032))
    transform_geometry_011.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_011.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_011.outputs[0], gold_decorations_2.inputs[0])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.mode = "EDGES"
    mesh_to_curve.inputs[1].default_value = True
    links.new(separate_geometry.outputs[0], mesh_to_curve.inputs[0])
    links.new(mesh_to_curve.outputs[0], trim_curve_003.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.inputs[1].default_value = True
    set_curve_tilt.inputs[2].default_value = -0.34819304943084717
    links.new(set_curve_tilt.outputs[0], transform_geometry_011.inputs[0])
    links.new(set_curve_normal_004.outputs[0], set_curve_tilt.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.socket_idname = "NodeSocketGeometry"
    links.new(reroute_002.outputs[0], join_geometry_002.inputs[0])
    links.new(gold_on_band.outputs[0], reroute_002.inputs[0])

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
    links.new(curve_circle_002.outputs[0], set_position_002.inputs[0])
    links.new(set_position_002.outputs[0], transform_geometry_012.inputs[0])

    position_003 = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_005 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_003.outputs[0], separate_x_y_z_005.inputs[0])

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
    links.new(separate_x_y_z_005.outputs[1], map_range_001.inputs[0])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.inputs[0].default_value = 1.0
    links.new(map_range_001.outputs[0], float_curve.inputs[1])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.operation = "MULTIPLY"
    math_002.inputs[1].default_value = -0.29999998211860657
    math_002.inputs[2].default_value = 0.5

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.inputs[0].default_value = 0.0
    links.new(combine_x_y_z_001.outputs[0], set_position_002.inputs[3])
    links.new(math_002.outputs[0], combine_x_y_z_001.inputs[2])

    position_005 = nodes.new("GeometryNodeInputPosition")

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.operation = "MULTIPLY"
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[3].default_value = 1.0
    links.new(position_005.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], set_position_002.inputs[2])

    combine_x_y_z_002 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_002.inputs[1].default_value = 1.0
    combine_x_y_z_002.inputs[2].default_value = 1.0
    links.new(combine_x_y_z_002.outputs[0], vector_math_001.inputs[1])

    float_curve_002 = nodes.new("ShaderNodeFloatCurve")
    float_curve_002.inputs[0].default_value = 1.0
    links.new(map_range_001.outputs[0], float_curve_002.inputs[1])
    links.new(float_curve_002.outputs[0], combine_x_y_z_002.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "skip"
    store_named_attribute.inputs[3].default_value = True
    links.new(store_named_attribute.outputs[0], join_geometry_002.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Length"
    resample_curve.inputs[3].default_value = 10
    resample_curve.inputs[4].default_value = 0.014999999664723873
    links.new(transform_geometry_012.outputs[0], resample_curve.inputs[0])

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
    links.new(curve_tangent_001.outputs[0], align_rotation_to_vector.inputs[2])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.axis = "Y"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    links.new(align_rotation_to_vector.outputs[0], align_rotation_to_vector_001.inputs[0])

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.legacy_corner_normals = False
    links.new(normal_001.outputs[0], align_rotation_to_vector_001.inputs[2])

    rotate_rotation_003 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_003.rotation_space = "LOCAL"
    rotate_rotation_003.inputs[1].default_value = Euler((0.23108159005641937, 0.14137165248394012, 0.0), 'XYZ')
    links.new(align_rotation_to_vector_001.outputs[0], rotate_rotation_003.inputs[0])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")

    math_003 = nodes.new("ShaderNodeMath")
    math_003.operation = "SUBTRACT"
    math_003.inputs[1].default_value = 0.7400000095367432
    math_003.inputs[2].default_value = 0.5
    links.new(spline_parameter.outputs[0], math_003.inputs[0])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.operation = "ABSOLUTE"
    math_004.inputs[1].default_value = 0.7400000095367432
    math_004.inputs[2].default_value = 0.5
    links.new(math_003.outputs[0], math_004.inputs[0])

    set_curve_tilt_002 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_002.inputs[1].default_value = True
    links.new(set_curve_tilt_002.outputs[0], instance_on_points_002.inputs[0])
    links.new(resample_curve.outputs[0], set_curve_tilt_002.inputs[0])

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
    links.new(math_004.outputs[0], map_range_002.inputs[0])
    links.new(map_range_002.outputs[0], set_curve_tilt_002.inputs[2])

    float_curve_003 = nodes.new("ShaderNodeFloatCurve")
    float_curve_003.inputs[0].default_value = 1.0

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_001.outputs[0], float_curve_003.inputs[1])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.operation = "MULTIPLY"
    math_005.inputs[1].default_value = 0.014999999664723873
    math_005.inputs[2].default_value = 0.5
    links.new(float_curve_003.outputs[0], math_005.inputs[0])

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
    links.new(curve_circle_003.outputs[0], instance_on_points_003.inputs[0])

    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.inputs[0].default_value = 0.0020000000949949026
    ico_sphere_001.inputs[1].default_value = 1
    links.new(ico_sphere_001.outputs[0], instance_on_points_003.inputs[2])

    cylinder_001 = nodes.new("GeometryNodeMeshCylinder")
    cylinder_001.fill_type = "NGON"
    cylinder_001.inputs[0].default_value = 10
    cylinder_001.inputs[1].default_value = 1
    cylinder_001.inputs[2].default_value = 1
    cylinder_001.inputs[3].default_value = 0.014999999664723873
    cylinder_001.inputs[4].default_value = 0.0020000000949949026

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    links.new(instance_on_points_003.outputs[0], join_geometry_003.inputs[0])
    links.new(cylinder_001.outputs[0], join_geometry_003.inputs[0])

    ico_sphere_002 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_002.inputs[0].default_value = 0.012000000104308128
    ico_sphere_002.inputs[1].default_value = 2

    transform_geometry_013 = nodes.new("GeometryNodeTransform")
    transform_geometry_013.inputs[1].default_value = "Components"
    transform_geometry_013.inputs[2].default_value = Vector((-0.006000000052154064, 0.0, 0.0010000000474974513))
    transform_geometry_013.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_013.inputs[4].default_value = Vector((0.4699999988079071, 0.8600000143051147, 0.05000000074505806))
    links.new(transform_geometry_013.outputs[0], join_geometry_003.inputs[0])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.inputs[1].default_value = True
    set_position_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(set_position_003.outputs[0], transform_geometry_013.inputs[0])
    links.new(ico_sphere_002.outputs[0], set_position_003.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.operation = "SCALE"
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[3].default_value = 0.004999999888241291
    links.new(vector_math_002.outputs[0], set_position_003.inputs[3])

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
    links.new(noise_texture.outputs[0], vector_math_002.inputs[0])

    transform_geometry_014 = nodes.new("GeometryNodeTransform")
    transform_geometry_014.inputs[1].default_value = "Components"
    transform_geometry_014.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_014.inputs[3].default_value = Euler((0.0, 0.0, 3.1415927410125732), 'XYZ')
    transform_geometry_014.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_013.outputs[0], transform_geometry_014.inputs[0])
    links.new(transform_geometry_014.outputs[0], join_geometry_003.inputs[0])

    frame_002 = nodes.new("NodeFrame")
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20

    rotate_rotation_004 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_004.rotation_space = "LOCAL"
    rotate_rotation_004.inputs[1].default_value = Euler((3.1415927410125732, 0.0, 1.5707963705062866), 'XYZ')
    links.new(rotate_rotation_003.outputs[0], rotate_rotation_004.inputs[0])
    links.new(rotate_rotation_004.outputs[0], instance_on_points_002.inputs[5])

    ico_sphere_003 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_003.inputs[0].default_value = 0.004999999888241291
    ico_sphere_003.inputs[1].default_value = 1
    links.new(ico_sphere_003.outputs[0], join_geometry_003.inputs[0])

    frame_003 = nodes.new("NodeFrame")
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    store_named_attribute_004.inputs[1].default_value = True
    store_named_attribute_004.inputs[2].default_value = "gold"
    store_named_attribute_004.inputs[3].default_value = True
    links.new(store_named_attribute_004.outputs[0], instance_on_points_002.inputs[2])
    links.new(join_geometry_003.outputs[0], store_named_attribute_004.inputs[0])

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
    links.new(math_006.outputs[0], math_002.inputs[0])
    links.new(float_curve.outputs[0], math_006.inputs[0])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")

    float_curve_004 = nodes.new("ShaderNodeFloatCurve")
    float_curve_004.inputs[0].default_value = 1.0
    links.new(spline_parameter_002.outputs[0], float_curve_004.inputs[1])
    links.new(float_curve_004.outputs[0], math_006.inputs[1])

    set_position_004 = nodes.new("GeometryNodeSetPosition")
    set_position_004.inputs[1].default_value = True
    set_position_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(cylinder_002.outputs[0], set_position_004.inputs[0])

    position_006 = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_006 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_006.outputs[0], separate_x_y_z_006.inputs[0])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.operation = "ABSOLUTE"
    math_007.inputs[1].default_value = 0.5
    math_007.inputs[2].default_value = 0.5
    links.new(separate_x_y_z_006.outputs[0], math_007.inputs[0])

    combine_x_y_z_003 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_003.inputs[0].default_value = 0.0
    combine_x_y_z_003.inputs[2].default_value = 0.0
    links.new(combine_x_y_z_003.outputs[0], set_position_004.inputs[3])

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
    links.new(separate_x_y_z_006.outputs[1], map_range_003.inputs[0])

    math_008 = nodes.new("ShaderNodeMath")
    math_008.operation = "MULTIPLY"
    math_008.inputs[2].default_value = 0.5
    links.new(math_008.outputs[0], combine_x_y_z_003.inputs[1])
    links.new(math_007.outputs[0], math_008.inputs[0])
    links.new(map_range_003.outputs[0], math_008.inputs[1])

    boolean_math_004 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.operation = "AND"
    links.new(cylinder_002.outputs[1], boolean_math_004.inputs[0])
    links.new(cylinder_002.outputs[2], boolean_math_004.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.mode = "EDGES"
    links.new(set_position_004.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(boolean_math_004.outputs[0], mesh_to_curve_001.inputs[1])

    ico_sphere_004 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_004.inputs[0].default_value = 0.0020000000949949026
    ico_sphere_004.inputs[1].default_value = 1

    instance_on_points_004 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_004.inputs[1].default_value = True
    instance_on_points_004.inputs[3].default_value = False
    instance_on_points_004.inputs[4].default_value = 0
    instance_on_points_004.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_004.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    links.new(mesh_to_curve_001.outputs[0], instance_on_points_004.inputs[0])
    links.new(ico_sphere_004.outputs[0], instance_on_points_004.inputs[2])

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
    links.new(ico_sphere_005.outputs[0], dual_mesh.inputs[0])
    links.new(dual_mesh.outputs[0], transform_geometry_015.inputs[0])

    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")

    transform_geometry_016 = nodes.new("GeometryNodeTransform")
    transform_geometry_016.inputs[1].default_value = "Components"
    transform_geometry_016.inputs[2].default_value = Vector((0.0, 0.003000000026077032, 0.0))
    transform_geometry_016.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_016.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_015.outputs[0], transform_geometry_016.inputs[0])
    links.new(transform_geometry_016.outputs[0], join_geometry_007.inputs[0])

    transform_geometry_017 = nodes.new("GeometryNodeTransform")
    transform_geometry_017.inputs[1].default_value = "Components"
    transform_geometry_017.inputs[2].default_value = Vector((-0.009999999776482582, 0.009999999776482582, 0.0))
    transform_geometry_017.inputs[3].default_value = Euler((0.0, 0.0, 1.0471975803375244), 'XYZ')
    transform_geometry_017.inputs[4].default_value = Vector((0.6000000238418579, 0.6000000238418579, 1.0))
    links.new(transform_geometry_015.outputs[0], transform_geometry_017.inputs[0])
    links.new(transform_geometry_017.outputs[0], join_geometry_007.inputs[0])

    transform_geometry_018 = nodes.new("GeometryNodeTransform")
    transform_geometry_018.inputs[1].default_value = "Components"
    transform_geometry_018.inputs[2].default_value = Vector((0.009999999776482582, 0.009999999776482582, 0.0))
    transform_geometry_018.inputs[3].default_value = Euler((0.0, 0.0, -1.0471975803375244), 'XYZ')
    transform_geometry_018.inputs[4].default_value = Vector((0.6000000238418579, 0.6000000238418579, 1.0))
    links.new(transform_geometry_015.outputs[0], transform_geometry_018.inputs[0])
    links.new(transform_geometry_018.outputs[0], join_geometry_007.inputs[0])

    transform_geometry_019 = nodes.new("GeometryNodeTransform")
    transform_geometry_019.inputs[1].default_value = "Components"
    transform_geometry_019.inputs[2].default_value = Vector((0.0, -0.012000000104308128, 0.0))
    transform_geometry_019.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_019.inputs[4].default_value = Vector((0.30000001192092896, 0.6000000238418579, 1.0))
    links.new(transform_geometry_015.outputs[0], transform_geometry_019.inputs[0])
    links.new(transform_geometry_019.outputs[0], join_geometry_007.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    links.new(instance_on_points_004.outputs[0], join_geometry_009.inputs[0])
    links.new(set_position_004.outputs[0], join_geometry_009.inputs[0])

    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.data_type = "BOOLEAN"
    store_named_attribute_005.domain = "POINT"
    store_named_attribute_005.inputs[1].default_value = True
    store_named_attribute_005.inputs[2].default_value = "ruby"
    store_named_attribute_005.inputs[3].default_value = True

    join_geometry_010 = nodes.new("GeometryNodeJoinGeometry")
    links.new(store_named_attribute_005.outputs[0], join_geometry_010.inputs[0])

    store_named_attribute_006 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_006.data_type = "BOOLEAN"
    store_named_attribute_006.domain = "POINT"
    store_named_attribute_006.inputs[1].default_value = True
    store_named_attribute_006.inputs[2].default_value = "gold"
    store_named_attribute_006.inputs[3].default_value = True
    links.new(store_named_attribute_006.outputs[0], join_geometry_010.inputs[0])

    frame_004 = nodes.new("NodeFrame")
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
    links.new(set_curve_tilt_002.outputs[0], sample_curve.inputs[0])

    transform_geometry_020 = nodes.new("GeometryNodeTransform")
    transform_geometry_020.inputs[1].default_value = "Components"
    transform_geometry_020.inputs[3].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')
    transform_geometry_020.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(join_geometry_010.outputs[0], transform_geometry_020.inputs[0])

    join_geometry_011 = nodes.new("GeometryNodeJoinGeometry")
    links.new(transform_geometry_020.outputs[0], join_geometry_011.inputs[0])
    links.new(instance_on_points_002.outputs[0], join_geometry_011.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.operation = "ADD"
    vector_math_003.inputs[1].default_value = [0.0, -0.003000000026077032, -0.019999999552965164]
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_003.inputs[3].default_value = 1.0
    links.new(vector_math_003.outputs[0], transform_geometry_020.inputs[2])
    links.new(sample_curve.outputs[1], vector_math_003.inputs[0])

    float_curve_005 = nodes.new("ShaderNodeFloatCurve")
    float_curve_005.inputs[0].default_value = 1.0

    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_003.outputs[0], float_curve_005.inputs[1])

    math_009 = nodes.new("ShaderNodeMath")
    math_009.operation = "MULTIPLY"
    math_009.inputs[1].default_value = -0.014999999664723873
    math_009.inputs[2].default_value = 0.5
    links.new(float_curve_005.outputs[0], math_009.inputs[0])

    math_010 = nodes.new("ShaderNodeMath")
    math_010.operation = "ADD"
    math_010.inputs[2].default_value = 0.5
    links.new(math_010.outputs[0], combine_x_y_z_001.inputs[1])
    links.new(math_005.outputs[0], math_010.inputs[0])
    links.new(math_009.outputs[0], math_010.inputs[1])

    frame_018 = nodes.new("NodeFrame")
    frame_018.text = None
    frame_018.shrink = True
    frame_018.label_size = 20

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
    links.new(curve_circle_004.outputs[0], set_position_005.inputs[0])
    links.new(set_position_005.outputs[0], transform_geometry_021.inputs[0])

    position_007 = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_007 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_007.outputs[0], separate_x_y_z_007.inputs[0])

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
    links.new(separate_x_y_z_007.outputs[1], map_range_004.inputs[0])

    float_curve_006 = nodes.new("ShaderNodeFloatCurve")
    float_curve_006.inputs[0].default_value = 1.0
    links.new(map_range_004.outputs[0], float_curve_006.inputs[1])

    math_011 = nodes.new("ShaderNodeMath")
    math_011.operation = "MULTIPLY"
    math_011.inputs[1].default_value = -0.19999998807907104
    math_011.inputs[2].default_value = 0.5

    combine_x_y_z_004 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_004.inputs[0].default_value = 0.0
    links.new(combine_x_y_z_004.outputs[0], set_position_005.inputs[3])
    links.new(math_011.outputs[0], combine_x_y_z_004.inputs[2])

    position_008 = nodes.new("GeometryNodeInputPosition")

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.operation = "MULTIPLY"
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_004.inputs[3].default_value = 1.0
    links.new(position_008.outputs[0], vector_math_004.inputs[0])
    links.new(vector_math_004.outputs[0], set_position_005.inputs[2])

    combine_x_y_z_005 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_005.inputs[1].default_value = 1.0
    combine_x_y_z_005.inputs[2].default_value = 1.0
    links.new(combine_x_y_z_005.outputs[0], vector_math_004.inputs[1])

    float_curve_007 = nodes.new("ShaderNodeFloatCurve")
    float_curve_007.inputs[0].default_value = 1.0
    links.new(map_range_004.outputs[0], float_curve_007.inputs[1])
    links.new(float_curve_007.outputs[0], combine_x_y_z_005.inputs[0])

    resample_curve_004 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_004.keep_last_segment = True
    resample_curve_004.inputs[1].default_value = True
    resample_curve_004.inputs[2].default_value = "Length"
    resample_curve_004.inputs[3].default_value = 10
    resample_curve_004.inputs[4].default_value = 0.013799999840557575
    links.new(transform_geometry_021.outputs[0], resample_curve_004.inputs[0])

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
    links.new(curve_tangent_002.outputs[0], align_rotation_to_vector_002.inputs[2])

    align_rotation_to_vector_003 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_003.axis = "Y"
    align_rotation_to_vector_003.pivot_axis = "AUTO"
    align_rotation_to_vector_003.inputs[1].default_value = 1.0
    links.new(align_rotation_to_vector_002.outputs[0], align_rotation_to_vector_003.inputs[0])

    normal_002 = nodes.new("GeometryNodeInputNormal")
    normal_002.legacy_corner_normals = False
    links.new(normal_002.outputs[0], align_rotation_to_vector_003.inputs[2])

    spline_parameter_004 = nodes.new("GeometryNodeSplineParameter")

    math_012 = nodes.new("ShaderNodeMath")
    math_012.operation = "SUBTRACT"
    math_012.inputs[1].default_value = 0.7400000095367432
    math_012.inputs[2].default_value = 0.5
    links.new(spline_parameter_004.outputs[0], math_012.inputs[0])

    math_013 = nodes.new("ShaderNodeMath")
    math_013.operation = "ABSOLUTE"
    math_013.inputs[1].default_value = 0.7400000095367432
    math_013.inputs[2].default_value = 0.5
    links.new(math_012.outputs[0], math_013.inputs[0])

    set_curve_tilt_003 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_003.inputs[1].default_value = True
    links.new(set_curve_tilt_003.outputs[0], instance_on_points_005.inputs[0])
    links.new(resample_curve_004.outputs[0], set_curve_tilt_003.inputs[0])

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
    links.new(math_013.outputs[0], map_range_005.inputs[0])
    links.new(map_range_005.outputs[0], set_curve_tilt_003.inputs[2])

    float_curve_008 = nodes.new("ShaderNodeFloatCurve")
    float_curve_008.inputs[0].default_value = 1.0

    spline_parameter_005 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_005.outputs[0], float_curve_008.inputs[1])

    math_014 = nodes.new("ShaderNodeMath")
    math_014.operation = "MULTIPLY"
    math_014.inputs[1].default_value = 0.014999999664723873
    math_014.inputs[2].default_value = 0.5
    links.new(float_curve_008.outputs[0], math_014.inputs[0])

    frame_020 = nodes.new("NodeFrame")
    frame_020.text = None
    frame_020.shrink = True
    frame_020.label_size = 20

    math_015 = nodes.new("ShaderNodeMath")
    math_015.operation = "ADD"
    math_015.inputs[2].default_value = 0.5
    links.new(math_015.outputs[0], math_011.inputs[0])
    links.new(float_curve_006.outputs[0], math_015.inputs[0])

    spline_parameter_006 = nodes.new("GeometryNodeSplineParameter")

    float_curve_009 = nodes.new("ShaderNodeFloatCurve")
    float_curve_009.inputs[0].default_value = 1.0
    links.new(spline_parameter_006.outputs[0], float_curve_009.inputs[1])
    links.new(float_curve_009.outputs[0], math_015.inputs[1])

    float_curve_010 = nodes.new("ShaderNodeFloatCurve")
    float_curve_010.inputs[0].default_value = 1.0

    spline_parameter_007 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_007.outputs[0], float_curve_010.inputs[1])

    math_018 = nodes.new("ShaderNodeMath")
    math_018.operation = "MULTIPLY"
    math_018.inputs[1].default_value = -0.014999999664723873
    math_018.inputs[2].default_value = 0.5
    links.new(float_curve_010.outputs[0], math_018.inputs[0])

    math_019 = nodes.new("ShaderNodeMath")
    math_019.operation = "ADD"
    math_019.inputs[2].default_value = 0.5
    links.new(math_019.outputs[0], combine_x_y_z_004.inputs[1])
    links.new(math_014.outputs[0], math_019.inputs[0])
    links.new(math_018.outputs[0], math_019.inputs[1])

    frame_022 = nodes.new("NodeFrame")
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
    links.new(set_spline_type.outputs[0], fillet_curve.inputs[0])
    links.new(quadrilateral.outputs[0], set_spline_type.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.inputs[2].default_value = 0.8519999980926514
    curve_to_mesh_001.inputs[3].default_value = False
    links.new(fillet_curve.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(curve_to_mesh_001.outputs[0], instance_on_points_005.inputs[2])

    curve_circle_005 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_005.mode = "RADIUS"
    curve_circle_005.inputs[0].default_value = 6
    curve_circle_005.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_005.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_005.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_005.inputs[4].default_value = 0.003000000026077032
    links.new(curve_circle_005.outputs[0], curve_to_mesh_001.inputs[1])

    frame_019 = nodes.new("NodeFrame")
    frame_019.text = None
    frame_019.shrink = True
    frame_019.label_size = 20

    rotate_rotation_006 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_006.rotation_space = "LOCAL"
    links.new(rotate_rotation_006.outputs[0], instance_on_points_005.inputs[5])

    rotate_rotation_005 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_005.rotation_space = "LOCAL"
    links.new(align_rotation_to_vector_003.outputs[0], rotate_rotation_005.inputs[0])
    links.new(rotate_rotation_005.outputs[0], rotate_rotation_006.inputs[0])

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
    links.new(random_value_012.outputs[0], rotate_rotation_006.inputs[1])

    index_001 = nodes.new("GeometryNodeInputIndex")

    math_016 = nodes.new("ShaderNodeMath")
    math_016.operation = "FLOORED_MODULO"
    math_016.inputs[1].default_value = 2.0
    math_016.inputs[2].default_value = 0.5
    links.new(index_001.outputs[0], math_016.inputs[0])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "FLOAT"
    switch_001.inputs[1].default_value = -0.3799999952316284
    switch_001.inputs[2].default_value = 0.5
    links.new(math_016.outputs[0], switch_001.inputs[0])

    combine_x_y_z_006 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_006.inputs[1].default_value = 0.0
    combine_x_y_z_006.inputs[2].default_value = 0.0
    links.new(switch_001.outputs[0], combine_x_y_z_006.inputs[0])
    links.new(combine_x_y_z_006.outputs[0], rotate_rotation_005.inputs[1])

    join_geometry_012 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_011.outputs[0], join_geometry_012.inputs[0])
    links.new(join_geometry_012.outputs[0], store_named_attribute.inputs[0])

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
    links.new(curve_circle_006.outputs[0], curve_to_mesh_002.inputs[0])

    sample_curve_001 = nodes.new("GeometryNodeSampleCurve")
    sample_curve_001.mode = "FACTOR"
    sample_curve_001.use_all_curves = True
    sample_curve_001.data_type = "FLOAT"
    sample_curve_001.inputs[1].default_value = 0.0
    sample_curve_001.inputs[2].default_value = 0.7185045480728149
    sample_curve_001.inputs[3].default_value = 0.0
    sample_curve_001.inputs[4].default_value = 0
    links.new(set_curve_tilt_003.outputs[0], sample_curve_001.inputs[0])

    transform_geometry_022 = nodes.new("GeometryNodeTransform")
    transform_geometry_022.inputs[1].default_value = "Components"
    transform_geometry_022.inputs[3].default_value = Euler((1.5707963705062866, 0.0, 0.34033918380737305), 'XYZ')
    transform_geometry_022.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(curve_to_mesh_002.outputs[0], transform_geometry_022.inputs[0])

    join_geometry_013 = nodes.new("GeometryNodeJoinGeometry")
    links.new(instance_on_points_005.outputs[0], join_geometry_013.inputs[0])
    links.new(transform_geometry_022.outputs[0], join_geometry_013.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.operation = "ADD"
    vector_math_005.inputs[1].default_value = [0.0, 0.0, -0.012000000104308128]
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_005.inputs[3].default_value = 1.0
    links.new(vector_math_005.outputs[0], transform_geometry_022.inputs[2])
    links.new(sample_curve_001.outputs[1], vector_math_005.inputs[0])

    curve_circle_007 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_007.mode = "RADIUS"
    curve_circle_007.inputs[0].default_value = 6
    curve_circle_007.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_007.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_007.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_007.inputs[4].default_value = 0.009999999776482582
    links.new(curve_circle_007.outputs[0], curve_to_mesh_002.inputs[1])

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
    links.new(transform_geometry_023.outputs[0], join_geometry_013.inputs[0])

    frame_021 = nodes.new("NodeFrame")
    frame_021.text = None
    frame_021.shrink = True
    frame_021.label_size = 20

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.operation = "ADD"
    vector_math_006.inputs[1].default_value = [0.0, 0.0, -0.017999999225139618]
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_006.inputs[3].default_value = 1.0
    links.new(vector_math_006.outputs[0], transform_geometry_023.inputs[2])
    links.new(vector_math_005.outputs[0], vector_math_006.inputs[0])

    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.inputs[3].default_value = True

    resample_curve_005 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_005.keep_last_segment = True
    resample_curve_005.inputs[1].default_value = True
    resample_curve_005.inputs[2].default_value = "Count"
    resample_curve_005.inputs[3].default_value = 128
    resample_curve_005.inputs[4].default_value = 0.10000000149011612
    links.new(resample_curve_005.outputs[0], curve_to_mesh_003.inputs[0])
    links.new(curve_line.outputs[0], resample_curve_005.inputs[0])

    curve_circle_008 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_008.mode = "RADIUS"
    curve_circle_008.inputs[0].default_value = 32
    curve_circle_008.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_008.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_008.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_008.inputs[4].default_value = 0.003000000026077032
    links.new(curve_circle_008.outputs[0], curve_to_mesh_003.inputs[1])

    spline_parameter_008 = nodes.new("GeometryNodeSplineParameter")

    float_curve_011 = nodes.new("ShaderNodeFloatCurve")
    float_curve_011.inputs[0].default_value = 1.0
    links.new(spline_parameter_008.outputs[0], float_curve_011.inputs[1])
    links.new(float_curve_011.outputs[0], curve_to_mesh_003.inputs[2])

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
    links.new(curve_circle_009.outputs[0], curve_to_mesh_004.inputs[0])

    curve_circle_010 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_010.mode = "RADIUS"
    curve_circle_010.inputs[0].default_value = 6
    curve_circle_010.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_010.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_010.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_010.inputs[4].default_value = 0.0020000000949949026
    links.new(curve_circle_010.outputs[0], curve_to_mesh_004.inputs[1])

    join_geometry_014 = nodes.new("GeometryNodeJoinGeometry")
    links.new(curve_to_mesh_003.outputs[0], join_geometry_014.inputs[0])
    links.new(join_geometry_014.outputs[0], transform_geometry_023.inputs[0])

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
    links.new(curve_to_mesh_004.outputs[0], instance_on_points_006.inputs[2])
    links.new(curve_circle_011.outputs[0], instance_on_points_006.inputs[0])

    transform_geometry_024 = nodes.new("GeometryNodeTransform")
    transform_geometry_024.inputs[1].default_value = "Components"
    transform_geometry_024.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_024.inputs[3].default_value = Euler((1.5707963705062866, 0.5235987901687622, 0.0), 'XYZ')
    transform_geometry_024.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(instance_on_points_006.outputs[0], transform_geometry_024.inputs[0])
    links.new(transform_geometry_024.outputs[0], join_geometry_014.inputs[0])

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.inputs[0].default_value = 0.014999999664723873
    grid.inputs[1].default_value = 0.012000000104308128
    grid.inputs[2].default_value = 12
    grid.inputs[3].default_value = 4

    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "FACE"
    links.new(grid.outputs[0], delete_geometry_001.inputs[0])

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
    links.new(random_value_013.outputs[3], delete_geometry_001.inputs[1])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.mode = "FACES"
    extrude_mesh.inputs[1].default_value = True
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    extrude_mesh.inputs[3].default_value = 0.003000000026077032
    extrude_mesh.inputs[4].default_value = False
    links.new(delete_geometry_001.outputs[0], extrude_mesh.inputs[0])

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.inputs[1].default_value = True
    links.new(delete_geometry_001.outputs[0], flip_faces.inputs[0])

    join_geometry_015 = nodes.new("GeometryNodeJoinGeometry")
    links.new(extrude_mesh.outputs[0], join_geometry_015.inputs[0])
    links.new(flip_faces.outputs[0], join_geometry_015.inputs[0])

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.inputs[1].default_value = True
    merge_by_distance.inputs[2].default_value = "All"
    merge_by_distance.inputs[3].default_value = 9.999999747378752e-05
    links.new(join_geometry_015.outputs[0], merge_by_distance.inputs[0])

    transform_geometry_025 = nodes.new("GeometryNodeTransform")
    transform_geometry_025.inputs[1].default_value = "Components"
    transform_geometry_025.inputs[2].default_value = Vector((0.006000000052154064, 0.001500000013038516, -0.04999999701976776))
    transform_geometry_025.inputs[3].default_value = Euler((1.5707963705062866, -1.5707963705062866, 0.0), 'XYZ')
    transform_geometry_025.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_025.outputs[0], join_geometry_014.inputs[0])

    subdivision_surface = nodes.new("GeometryNodeSubdivisionSurface")
    subdivision_surface.inputs[1].default_value = 1
    subdivision_surface.inputs[2].default_value = 0.8063265681266785
    subdivision_surface.inputs[3].default_value = 0.0
    subdivision_surface.inputs[4].default_value = True
    subdivision_surface.inputs[5].default_value = "Keep Boundaries"
    subdivision_surface.inputs[6].default_value = "All"
    links.new(subdivision_surface.outputs[0], transform_geometry_025.inputs[0])
    links.new(merge_by_distance.outputs[0], subdivision_surface.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.domain = "FACE"
    set_shade_smooth_001.inputs[1].default_value = True
    set_shade_smooth_001.inputs[2].default_value = True
    links.new(join_geometry_013.outputs[0], set_shade_smooth_001.inputs[0])

    frame_023 = nodes.new("NodeFrame")
    frame_023.text = None
    frame_023.shrink = True
    frame_023.label_size = 20

    store_named_attribute_007 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_007.data_type = "BOOLEAN"
    store_named_attribute_007.domain = "POINT"
    store_named_attribute_007.inputs[1].default_value = True
    store_named_attribute_007.inputs[2].default_value = "gold"
    store_named_attribute_007.inputs[3].default_value = True
    links.new(store_named_attribute_007.outputs[0], join_geometry_012.inputs[0])
    links.new(set_shade_smooth_001.outputs[0], store_named_attribute_007.inputs[0])

    frame_024 = nodes.new("NodeFrame")
    frame_024.text = None
    frame_024.shrink = True
    frame_024.label_size = 20

    ico_sphere_006 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_006.inputs[0].default_value = 0.029999999329447746
    ico_sphere_006.inputs[1].default_value = 3

    transform_geometry_026 = nodes.new("GeometryNodeTransform")
    transform_geometry_026.inputs[1].default_value = "Components"
    transform_geometry_026.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_026.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_026.inputs[4].default_value = Vector((1.0, 1.0, 0.5))
    links.new(ico_sphere_006.outputs[0], transform_geometry_026.inputs[0])

    instance_on_points_007 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_007.inputs[1].default_value = True
    instance_on_points_007.inputs[3].default_value = False
    instance_on_points_007.inputs[4].default_value = 0
    instance_on_points_007.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_007.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_026.outputs[0], instance_on_points_007.inputs[2])

    quadratic_bézier = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier.inputs[0].default_value = 16
    quadratic_bézier.inputs[1].default_value = Vector((-0.019999999552965164, 0.0, 0.0))
    quadratic_bézier.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.009999999776482582))
    quadratic_bézier.inputs[3].default_value = Vector((0.019999999552965164, 0.0, 0.0))
    links.new(quadratic_bézier.outputs[0], instance_on_points_007.inputs[0])

    realize_instances_003 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.inputs[1].default_value = True
    realize_instances_003.inputs[2].default_value = True
    realize_instances_003.inputs[3].default_value = 0
    links.new(instance_on_points_007.outputs[0], realize_instances_003.inputs[0])

    mesh_to_s_d_f_grid = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid.inputs[1].default_value = 0.009999999776482582
    mesh_to_s_d_f_grid.inputs[2].default_value = 1
    links.new(realize_instances_003.outputs[0], mesh_to_s_d_f_grid.inputs[0])

    grid_to_mesh = nodes.new("GeometryNodeGridToMesh")
    grid_to_mesh.inputs[1].default_value = 0.0
    grid_to_mesh.inputs[2].default_value = 0.0

    dual_mesh_001 = nodes.new("GeometryNodeDualMesh")
    dual_mesh_001.inputs[1].default_value = False

    triangulate = nodes.new("GeometryNodeTriangulate")
    triangulate.inputs[1].default_value = True
    triangulate.inputs[2].default_value = "Shortest Diagonal"
    triangulate.inputs[3].default_value = "Beauty"
    links.new(triangulate.outputs[0], dual_mesh_001.inputs[0])
    links.new(grid_to_mesh.outputs[0], triangulate.inputs[0])

    s_d_f_grid_boolean = nodes.new("GeometryNodeSDFGridBoolean")
    s_d_f_grid_boolean.operation = "INTERSECT"
    s_d_f_grid_boolean.inputs[0].default_value = 0.0
    links.new(s_d_f_grid_boolean.outputs[0], grid_to_mesh.inputs[0])
    links.new(mesh_to_s_d_f_grid.outputs[0], s_d_f_grid_boolean.inputs[1])

    cube = nodes.new("GeometryNodeMeshCube")
    cube.inputs[0].default_value = Vector((1.0, 1.0, 0.019999999552965164))
    cube.inputs[1].default_value = 2
    cube.inputs[2].default_value = 2
    cube.inputs[3].default_value = 2

    mesh_to_s_d_f_grid_001 = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid_001.inputs[1].default_value = 0.009999999776482582
    mesh_to_s_d_f_grid_001.inputs[2].default_value = 1
    links.new(mesh_to_s_d_f_grid_001.outputs[0], s_d_f_grid_boolean.inputs[1])

    transform_geometry_027 = nodes.new("GeometryNodeTransform")
    transform_geometry_027.inputs[1].default_value = "Components"
    transform_geometry_027.inputs[2].default_value = Vector((0.0, 0.0, 0.009999999776482582))
    transform_geometry_027.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_027.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(cube.outputs[0], transform_geometry_027.inputs[0])
    links.new(transform_geometry_027.outputs[0], mesh_to_s_d_f_grid_001.inputs[0])

    mesh_boolean = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean.operation = "DIFFERENCE"
    mesh_boolean.solver = "MANIFOLD"
    mesh_boolean.inputs[2].default_value = False
    mesh_boolean.inputs[3].default_value = False
    links.new(dual_mesh_001.outputs[0], mesh_boolean.inputs[0])

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
    links.new(cube_001.outputs[0], transform_geometry_028.inputs[0])
    links.new(transform_geometry_028.outputs[0], mesh_boolean.inputs[1])

    delete_geometry_002 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.mode = "ALL"
    delete_geometry_002.domain = "FACE"
    links.new(mesh_boolean.outputs[0], delete_geometry_002.inputs[0])
    links.new(mesh_boolean.outputs[1], delete_geometry_002.inputs[1])

    mesh_boolean_001 = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean_001.operation = "INTERSECT"
    mesh_boolean_001.solver = "MANIFOLD"
    mesh_boolean_001.inputs[2].default_value = False
    mesh_boolean_001.inputs[3].default_value = False
    links.new(dual_mesh_001.outputs[0], mesh_boolean_001.inputs[1])

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
    links.new(cube_002.outputs[0], transform_geometry_029.inputs[0])
    links.new(transform_geometry_029.outputs[0], mesh_boolean_001.inputs[1])

    join_geometry_016 = nodes.new("GeometryNodeJoinGeometry")

    delete_geometry_003 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_003.mode = "ALL"
    delete_geometry_003.domain = "POINT"
    links.new(mesh_boolean_001.outputs[0], delete_geometry_003.inputs[0])

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
    links.new(normal_003.outputs[0], compare_008.inputs[4])
    links.new(compare_008.outputs[0], delete_geometry_003.inputs[1])

    mesh_to_curve_003 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_003.mode = "EDGES"
    mesh_to_curve_003.inputs[1].default_value = True
    links.new(delete_geometry_003.outputs[0], mesh_to_curve_003.inputs[0])

    resample_curve_006 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_006.keep_last_segment = True
    resample_curve_006.inputs[1].default_value = True
    resample_curve_006.inputs[2].default_value = "Count"
    resample_curve_006.inputs[3].default_value = 45
    resample_curve_006.inputs[4].default_value = 0.10000000149011612

    set_spline_cyclic_002 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_002.inputs[1].default_value = True
    set_spline_cyclic_002.inputs[2].default_value = True
    links.new(set_spline_cyclic_002.outputs[0], resample_curve_006.inputs[0])

    curve_to_mesh_005 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_005.inputs[2].default_value = 0.009999999776482582
    curve_to_mesh_005.inputs[3].default_value = False
    links.new(curve_to_mesh_005.outputs[0], join_geometry_016.inputs[0])
    links.new(resample_curve_006.outputs[0], curve_to_mesh_005.inputs[0])

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
    links.new(gem_in_holder_3.outputs[1], curve_to_mesh_005.inputs[1])

    trim_curve_005 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_005.mode = "FACTOR"
    trim_curve_005.inputs[1].default_value = True
    trim_curve_005.inputs[2].default_value = 0.010773210786283016
    trim_curve_005.inputs[3].default_value = 0.9906079769134521
    trim_curve_005.inputs[4].default_value = 0.0
    trim_curve_005.inputs[5].default_value = 1.0
    links.new(mesh_to_curve_003.outputs[0], trim_curve_005.inputs[0])

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
    links.new(resample_curve_007.outputs[0], instance_on_points_008.inputs[0])

    align_rotation_to_vector_004 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_004.axis = "Y"
    align_rotation_to_vector_004.pivot_axis = "AUTO"
    align_rotation_to_vector_004.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_004.inputs[1].default_value = 1.0
    links.new(align_rotation_to_vector_004.outputs[0], instance_on_points_008.inputs[5])

    curve_tangent_003 = nodes.new("GeometryNodeInputTangent")
    links.new(curve_tangent_003.outputs[0], align_rotation_to_vector_004.inputs[2])

    realize_instances_004 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_004.inputs[1].default_value = True
    realize_instances_004.inputs[2].default_value = True
    realize_instances_004.inputs[3].default_value = 0
    links.new(instance_on_points_008.outputs[0], realize_instances_004.inputs[0])

    transform_geometry_030 = nodes.new("GeometryNodeTransform")
    transform_geometry_030.inputs[1].default_value = "Components"
    transform_geometry_030.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_030.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_030.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    links.new(delete_geometry_002.outputs[0], transform_geometry_030.inputs[0])

    flip_faces_002 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.inputs[1].default_value = True
    links.new(transform_geometry_030.outputs[0], flip_faces_002.inputs[0])

    join_geometry_018 = nodes.new("GeometryNodeJoinGeometry")
    links.new(delete_geometry_002.outputs[0], join_geometry_018.inputs[0])
    links.new(flip_faces_002.outputs[0], join_geometry_018.inputs[0])

    merge_by_distance_001 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_001.inputs[2].default_value = "All"
    merge_by_distance_001.inputs[3].default_value = 0.0010000000474974513
    links.new(join_geometry_018.outputs[0], merge_by_distance_001.inputs[0])

    is_edge_boundary_1 = nodes.new("GeometryNodeGroup")
    is_edge_boundary_1.node_tree = create_is__edge__boundary_group()
    links.new(is_edge_boundary_1.outputs[0], merge_by_distance_001.inputs[1])

    spline_parameter_009 = nodes.new("GeometryNodeSplineParameter")

    math_020 = nodes.new("ShaderNodeMath")
    math_020.operation = "MULTIPLY"
    math_020.inputs[1].default_value = 2.0
    math_020.inputs[2].default_value = 0.5
    links.new(spline_parameter_009.outputs[0], math_020.inputs[0])

    math_021 = nodes.new("ShaderNodeMath")
    math_021.operation = "PINGPONG"
    math_021.inputs[1].default_value = 1.0
    math_021.inputs[2].default_value = 0.5
    links.new(math_020.outputs[0], math_021.inputs[0])

    curve_to_points_002 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_002.mode = "EVALUATED"
    curve_to_points_002.inputs[1].default_value = 10
    curve_to_points_002.inputs[2].default_value = 0.10000000149011612
    links.new(trim_curve_005.outputs[0], curve_to_points_002.inputs[0])

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.inputs[1].default_value = 0
    links.new(curve_to_points_002.outputs[0], points_to_curves.inputs[0])
    links.new(points_to_curves.outputs[0], set_spline_cyclic_002.inputs[0])

    gradient_texture = nodes.new("ShaderNodeTexGradient")
    gradient_texture.gradient_type = "RADIAL"
    gradient_texture.inputs[0].default_value = [0.0, 0.0, 0.0]

    math_022 = nodes.new("ShaderNodeMath")
    math_022.operation = "ADD"
    math_022.inputs[1].default_value = 0.5
    math_022.inputs[2].default_value = 0.5
    links.new(gradient_texture.outputs[1], math_022.inputs[0])

    math_023 = nodes.new("ShaderNodeMath")
    math_023.operation = "FRACT"
    math_023.inputs[1].default_value = 0.5
    math_023.inputs[2].default_value = 0.5
    links.new(math_023.outputs[0], points_to_curves.inputs[2])
    links.new(math_022.outputs[0], math_023.inputs[0])

    delete_geometry_004 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_004.mode = "ALL"
    delete_geometry_004.domain = "POINT"
    links.new(delete_geometry_004.outputs[0], resample_curve_007.inputs[0])
    links.new(points_to_curves.outputs[0], delete_geometry_004.inputs[0])

    position_009 = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_008 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_009.outputs[0], separate_x_y_z_008.inputs[0])

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
    links.new(separate_x_y_z_008.outputs[0], compare_009.inputs[0])
    links.new(compare_009.outputs[0], delete_geometry_004.inputs[1])

    float_curve_012 = nodes.new("ShaderNodeFloatCurve")
    float_curve_012.inputs[0].default_value = 1.0
    links.new(math_021.outputs[0], float_curve_012.inputs[1])
    links.new(float_curve_012.outputs[0], instance_on_points_008.inputs[6])

    transform_geometry_031 = nodes.new("GeometryNodeTransform")
    transform_geometry_031.inputs[1].default_value = "Components"
    transform_geometry_031.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_031.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_031.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    links.new(realize_instances_004.outputs[0], transform_geometry_031.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.inputs[1].default_value = True
    links.new(transform_geometry_031.outputs[0], flip_faces_003.inputs[0])

    join_geometry_019 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_019.outputs[0], join_geometry_016.inputs[0])
    links.new(flip_faces_003.outputs[0], join_geometry_019.inputs[0])
    links.new(realize_instances_004.outputs[0], join_geometry_019.inputs[0])

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
    links.new(join_geometry_020.outputs[0], instance_on_points_008.inputs[2])
    links.new(gem_in_holder_4.outputs[3], join_geometry_020.inputs[0])

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
    links.new(gem_in_holder_5.outputs[3], transform_geometry_032.inputs[0])

    join_geometry_021 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_021.outputs[0], join_geometry_020.inputs[0])
    links.new(gem_in_holder_5.outputs[3], join_geometry_021.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.inputs[1].default_value = True
    links.new(transform_geometry_032.outputs[0], flip_faces_001.inputs[0])
    links.new(flip_faces_001.outputs[0], join_geometry_021.inputs[0])

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
    links.new(gem_in_holder_6.outputs[3], transform_geometry_033.inputs[0])

    join_geometry_022 = nodes.new("GeometryNodeJoinGeometry")
    links.new(gem_in_holder_6.outputs[3], join_geometry_022.inputs[0])

    flip_faces_004 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_004.inputs[1].default_value = True
    links.new(transform_geometry_033.outputs[0], flip_faces_004.inputs[0])
    links.new(flip_faces_004.outputs[0], join_geometry_022.inputs[0])

    transform_geometry_034 = nodes.new("GeometryNodeTransform")
    transform_geometry_034.inputs[1].default_value = "Components"
    transform_geometry_034.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_034.inputs[3].default_value = Euler((0.0, -0.4363323152065277, 0.0), 'XYZ')
    transform_geometry_034.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_034.outputs[0], join_geometry_020.inputs[0])
    links.new(join_geometry_022.outputs[0], transform_geometry_034.inputs[0])

    join_geometry_017 = nodes.new("GeometryNodeJoinGeometry")

    store_named_attribute_008 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_008.data_type = "BOOLEAN"
    store_named_attribute_008.domain = "POINT"
    store_named_attribute_008.inputs[1].default_value = True
    store_named_attribute_008.inputs[2].default_value = "gold"
    store_named_attribute_008.inputs[3].default_value = True
    links.new(join_geometry_016.outputs[0], store_named_attribute_008.inputs[0])
    links.new(store_named_attribute_008.outputs[0], join_geometry_017.inputs[0])

    store_named_attribute_009 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_009.data_type = "BOOLEAN"
    store_named_attribute_009.domain = "POINT"
    store_named_attribute_009.inputs[1].default_value = True
    store_named_attribute_009.inputs[2].default_value = "saphire"
    store_named_attribute_009.inputs[3].default_value = True
    links.new(merge_by_distance_001.outputs[0], store_named_attribute_009.inputs[0])
    links.new(store_named_attribute_009.outputs[0], join_geometry_017.inputs[0])

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
    links.new(gem_in_holder_7.outputs[0], instance_on_points_009.inputs[2])
    links.new(instance_on_points_009.outputs[0], join_geometry_017.inputs[0])

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
    links.new(transform_geometry_035.outputs[0], instance_on_points_009.inputs[0])
    links.new(curve_circle_012.outputs[0], transform_geometry_035.inputs[0])

    frame_025 = nodes.new("NodeFrame")
    frame_025.text = None
    frame_025.shrink = True
    frame_025.label_size = 20

    frame_026 = nodes.new("NodeFrame")
    frame_026.text = None
    frame_026.shrink = True
    frame_026.label_size = 20

    transform_geometry_036 = nodes.new("GeometryNodeTransform")
    transform_geometry_036.inputs[1].default_value = "Components"
    transform_geometry_036.inputs[2].default_value = Vector((0.0, -0.12600000202655792, 0.36497700214385986))
    transform_geometry_036.inputs[3].default_value = Euler((0.9428269863128662, 0.0, 0.0), 'XYZ')
    transform_geometry_036.inputs[4].default_value = Vector((0.4000000059604645, 0.4000000059604645, 0.4000000059604645))
    links.new(join_geometry_017.outputs[0], transform_geometry_036.inputs[0])

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
    links.new(gem_in_holder_8.outputs[0], instance_on_points_010.inputs[2])

    realize_instances_005 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_005.inputs[1].default_value = True
    realize_instances_005.inputs[2].default_value = True
    realize_instances_005.inputs[3].default_value = 0

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "INSTANCE"
    links.new(capture_attribute_002.outputs[0], realize_instances_005.inputs[0])
    links.new(instance_on_points_010.outputs[0], capture_attribute_002.inputs[0])

    index_002 = nodes.new("GeometryNodeInputIndex")
    links.new(index_002.outputs[0], capture_attribute_002.inputs[1])

    resample_curve_008 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_008.keep_last_segment = True
    resample_curve_008.inputs[1].default_value = True
    resample_curve_008.inputs[2].default_value = "Count"
    resample_curve_008.inputs[3].default_value = 10
    resample_curve_008.inputs[4].default_value = 0.10000000149011612
    links.new(resample_curve_008.outputs[0], instance_on_points_010.inputs[0])

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
    links.new(align_rotation_to_vector_006.outputs[0], instance_on_points_010.inputs[5])
    links.new(align_rotation_to_vector_005.outputs[0], align_rotation_to_vector_006.inputs[0])
    links.new(normal_004.outputs[0], align_rotation_to_vector_006.inputs[2])

    curve_tangent_004 = nodes.new("GeometryNodeInputTangent")
    links.new(curve_tangent_004.outputs[0], align_rotation_to_vector_005.inputs[2])

    frame_027 = nodes.new("NodeFrame")
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
    links.new(trim_curve_006.outputs[0], resample_curve_008.inputs[0])
    links.new(set_curve_tilt.outputs[0], trim_curve_006.inputs[0])

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
    links.new(curve_to_points_003.outputs[0], for_each_geometry_element_input_002.inputs[0])
    links.new(curve_to_points_003.outputs[3], for_each_geometry_element_input_002.inputs[2])

    for_each_geometry_element_output_002 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_002.active_input_index = 1
    for_each_geometry_element_output_002.active_generation_index = 0
    for_each_geometry_element_output_002.active_main_index = 0
    for_each_geometry_element_output_002.domain = "POINT"
    for_each_geometry_element_output_002.inspection_index = 0

    position_010 = nodes.new("GeometryNodeInputPosition")
    links.new(position_010.outputs[0], for_each_geometry_element_input_002.inputs[2])

    transform_geometry_037 = nodes.new("GeometryNodeTransform")
    transform_geometry_037.inputs[1].default_value = "Components"
    links.new(gem_in_holder_9.outputs[0], transform_geometry_037.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[2], transform_geometry_037.inputs[2])

    rotate_rotation_007 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_007.rotation_space = "LOCAL"
    rotate_rotation_007.inputs[1].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')
    links.new(for_each_geometry_element_input_002.outputs[2], rotate_rotation_007.inputs[0])

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
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_014.inputs[7])
    links.new(random_value_014.outputs[2], gem_in_holder_9.inputs[7])

    transform_geometry_038 = nodes.new("GeometryNodeTransform")
    transform_geometry_038.inputs[1].default_value = "Components"
    transform_geometry_038.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    transform_geometry_038.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_038.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_037.outputs[0], transform_geometry_038.inputs[0])

    trim_curve_007 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_007.mode = "FACTOR"
    trim_curve_007.inputs[1].default_value = True
    trim_curve_007.inputs[2].default_value = 0.4000000059604645
    trim_curve_007.inputs[3].default_value = 0.75
    trim_curve_007.inputs[4].default_value = 0.0
    trim_curve_007.inputs[5].default_value = 1.0
    links.new(trim_curve_007.outputs[0], curve_to_points_003.inputs[0])
    links.new(separate_geometry_002.outputs[0], trim_curve_007.inputs[0])

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
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_015.inputs[7])
    links.new(random_value_015.outputs[1], transform_geometry_037.inputs[4])

    store_named_attribute_010 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_010.data_type = "BOOLEAN"
    store_named_attribute_010.domain = "POINT"
    store_named_attribute_010.inputs[1].default_value = True
    store_named_attribute_010.inputs[2].default_value = "skip"
    store_named_attribute_010.inputs[3].default_value = True
    links.new(store_named_attribute_010.outputs[0], for_each_geometry_element_output_002.inputs[1])
    links.new(transform_geometry_038.outputs[0], store_named_attribute_010.inputs[0])

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
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_016.inputs[7])
    links.new(random_value_016.outputs[1], gem_in_holder_9.inputs[10])

    rotate_rotation_008 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_008.rotation_space = "LOCAL"
    rotate_rotation_008.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
    links.new(rotate_rotation_008.outputs[0], transform_geometry_037.inputs[3])
    links.new(rotate_rotation_007.outputs[0], rotate_rotation_008.inputs[0])

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
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_017.inputs[7])
    links.new(random_value_017.outputs[1], gem_in_holder_9.inputs[9])

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
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_018.inputs[7])
    links.new(random_value_018.outputs[2], gem_in_holder_9.inputs[5])

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
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_019.inputs[7])
    links.new(random_value_019.outputs[2], gem_in_holder_9.inputs[4])

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
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_020.inputs[7])
    links.new(random_value_020.outputs[2], gem_in_holder_9.inputs[8])

    frame_028 = nodes.new("NodeFrame")
    frame_028.text = None
    frame_028.shrink = True
    frame_028.label_size = 20

    store_named_attribute_011 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_011.data_type = "BOOLEAN"
    store_named_attribute_011.domain = "POINT"
    store_named_attribute_011.inputs[1].default_value = True
    store_named_attribute_011.inputs[2].default_value = "skip"
    store_named_attribute_011.inputs[3].default_value = True
    links.new(store_named_attribute_011.outputs[0], join_geometry_002.inputs[0])
    links.new(transform_geometry_036.outputs[0], store_named_attribute_011.inputs[0])

    store_named_attribute_012 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_012.data_type = "BOOLEAN"
    store_named_attribute_012.domain = "POINT"
    store_named_attribute_012.inputs[1].default_value = True
    store_named_attribute_012.inputs[2].default_value = "skip"
    store_named_attribute_012.inputs[3].default_value = True
    links.new(store_named_attribute_012.outputs[0], join_geometry_002.inputs[0])
    links.new(for_each_geometry_element_output_002.outputs[2], store_named_attribute_012.inputs[0])

    mesh_boolean_002 = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean_002.operation = "DIFFERENCE"
    mesh_boolean_002.solver = "FLOAT"
    mesh_boolean_002.inputs[2].default_value = False
    mesh_boolean_002.inputs[3].default_value = False
    links.new(mesh_boolean_002.outputs[0], join_geometry_002.inputs[0])
    links.new(gold_decorations_2.outputs[0], mesh_boolean_002.inputs[0])

    ico_sphere_007 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_007.inputs[0].default_value = 0.07800000160932541
    ico_sphere_007.inputs[1].default_value = 3

    transform_geometry_039 = nodes.new("GeometryNodeTransform")
    transform_geometry_039.inputs[1].default_value = "Components"
    transform_geometry_039.inputs[2].default_value = Vector((0.0, -0.019999999552965164, 0.47999998927116394))
    transform_geometry_039.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_039.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_039.outputs[0], mesh_boolean_002.inputs[1])
    links.new(ico_sphere_007.outputs[0], transform_geometry_039.inputs[0])

    store_named_attribute_013 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_013.data_type = "BOOLEAN"
    store_named_attribute_013.domain = "POINT"
    store_named_attribute_013.inputs[2].default_value = "saphire"
    store_named_attribute_013.inputs[3].default_value = True
    links.new(realize_instances_005.outputs[0], store_named_attribute_013.inputs[0])

    boolean_math_005 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.operation = "AND"
    links.new(boolean_math_005.outputs[0], store_named_attribute_013.inputs[1])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.data_type = "BOOLEAN"
    named_attribute.inputs[0].default_value = "ruby"
    links.new(named_attribute.outputs[0], boolean_math_005.inputs[1])

    store_named_attribute_014 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_014.data_type = "BOOLEAN"
    store_named_attribute_014.domain = "POINT"
    store_named_attribute_014.inputs[2].default_value = "ruby"
    store_named_attribute_014.inputs[3].default_value = False
    links.new(store_named_attribute_013.outputs[0], store_named_attribute_014.inputs[0])
    links.new(boolean_math_005.outputs[0], store_named_attribute_014.inputs[1])
    links.new(store_named_attribute_014.outputs[0], join_geometry_002.inputs[0])

    math_017 = nodes.new("ShaderNodeMath")
    math_017.operation = "FLOORED_MODULO"
    math_017.inputs[1].default_value = 2.0
    math_017.inputs[2].default_value = 0.5
    links.new(math_017.outputs[0], boolean_math_005.inputs[0])
    links.new(capture_attribute_002.outputs[1], math_017.inputs[0])

    transform_geometry_040 = nodes.new("GeometryNodeTransform")
    transform_geometry_040.inputs[1].default_value = "Components"
    transform_geometry_040.inputs[2].default_value = Vector((0.0, 0.0, 0.0007999999797903001))
    transform_geometry_040.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_040.inputs[4].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))
    links.new(set_position_004.outputs[0], transform_geometry_040.inputs[0])
    links.new(transform_geometry_040.outputs[0], join_geometry_009.inputs[0])

    transform_geometry_041 = nodes.new("GeometryNodeTransform")
    transform_geometry_041.inputs[1].default_value = "Components"
    transform_geometry_041.inputs[2].default_value = Vector((0.0, 0.0, 0.0007999999797903001))
    transform_geometry_041.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_041.inputs[4].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))
    links.new(transform_geometry_040.outputs[0], transform_geometry_041.inputs[0])
    links.new(transform_geometry_041.outputs[0], join_geometry_009.inputs[0])

    scale_elements = nodes.new("GeometryNodeScaleElements")
    scale_elements.domain = "FACE"
    scale_elements.inputs[1].default_value = True
    scale_elements.inputs[2].default_value = 1.2000000476837158
    scale_elements.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    scale_elements.inputs[4].default_value = "Uniform"
    scale_elements.inputs[5].default_value = [1.0, 0.0, 0.0]
    links.new(join_geometry_007.outputs[0], scale_elements.inputs[0])

    transform_geometry_042 = nodes.new("GeometryNodeTransform")
    transform_geometry_042.inputs[1].default_value = "Components"
    transform_geometry_042.inputs[2].default_value = Vector((0.0, 0.0, 0.0005000000237487257))
    transform_geometry_042.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_042.inputs[4].default_value = Vector((1.0, 1.0, 0.7000000476837158))
    links.new(scale_elements.outputs[0], transform_geometry_042.inputs[0])

    join_geometry_023 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_023.outputs[0], store_named_attribute_006.inputs[0])
    links.new(join_geometry_009.outputs[0], join_geometry_023.inputs[0])
    links.new(transform_geometry_042.outputs[0], join_geometry_023.inputs[0])

    transform_geometry_043 = nodes.new("GeometryNodeTransform")
    transform_geometry_043.inputs[1].default_value = "Components"
    transform_geometry_043.inputs[2].default_value = Vector((0.0, 0.0, 0.0005000000237487257))
    transform_geometry_043.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_043.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_043.outputs[0], store_named_attribute_005.inputs[0])
    links.new(join_geometry_007.outputs[0], transform_geometry_043.inputs[0])

    auto_layout_nodes(group)
    return group
