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
def create_neck_centre_profile_f010_group():
    group_name = "Neck_centre_profile_f010"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

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
    bi_rail_loft.inputs[4].default_value = "Resolution"
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


    vector = nodes.new("FunctionNodeInputVector")
    vector.vector = Vector((0.0, -0.08999999612569809, 0.42000001668930054))


    frame_006 = nodes.new("NodeFrame")
    frame_006.label = "Centre Profile"
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


    vector_001 = nodes.new("FunctionNodeInputVector")
    vector_001.vector = Vector((-0.08500001579523087, 0.0, 0.4699999988079071))


    frame_007 = nodes.new("NodeFrame")
    frame_007.label = "Side Profile"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20


    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")


    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.inputs[1].default_value = "Components"
    transform_geometry_002.inputs[2].default_value = Vector((0.0, -0.019999999552965164, 0.4800000488758087))
    transform_geometry_002.inputs[3].default_value = Euler((0.4064871668815613, 0.0, 0.0), 'XYZ')
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


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


    position = nodes.new("GeometryNodeInputPosition")


    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")


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


    frame_008 = nodes.new("NodeFrame")
    frame_008.label = "Profiles"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20


    float_curve_001 = nodes.new("ShaderNodeFloatCurve")
    float_curve_001.inputs[0].default_value = 1.0


    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.inputs[0].default_value = 0.0
    combine_x_y_z.inputs[1].default_value = 0.0


    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.inputs[1].default_value = "Components"
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_004.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.inputs[1].default_value = "Components"
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    closure_output_001 = nodes.new("NodeClosureOutput")
    closure_output_001.input_items.new("FLOAT", "Value")
    closure_output_001.output_items.new("FLOAT", "Value")
    closure_output_001.active_input_index = 0
    closure_output_001.active_output_index = 0
    closure_output_001.define_signature = False


    closure_input_001 = nodes.new("NodeClosureInput")
    closure_input_001.pair_with_output(closure_output_001)


    math = nodes.new("ShaderNodeMath")
    math.operation = "PINGPONG"
    math.inputs[1].default_value = 0.25
    math.inputs[2].default_value = 0.5


    math_001 = nodes.new("ShaderNodeMath")
    math_001.operation = "MULTIPLY"
    math_001.inputs[1].default_value = 4.0
    math_001.inputs[2].default_value = 0.5


    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.inputs[1].default_value = "Components"
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_001.inputs[3].default_value = Euler((1.5446162223815918, 0.0, 0.0), 'XYZ')
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.inputs[1].default_value = "Components"
    transform_geometry_006.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')
    transform_geometry_006.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    integer = nodes.new("FunctionNodeInputInt")
    integer.integer = 73


    frame_009 = nodes.new("NodeFrame")
    frame_009.label = "Neck Rails"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20


    frame_010 = nodes.new("NodeFrame")
    frame_010.label = "Neck"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20


    # Parent assignments
    bi_rail_loft.parent = frame_010
    closure_input_001.parent = frame_010
    closure_output_001.parent = frame_010
    combine_x_y_z.parent = frame_009
    curve_circle.parent = frame_009
    curve_circle_001.parent = frame_009
    float_curve_001.parent = frame_009
    frame_006.parent = frame_008
    frame_007.parent = frame_008
    frame_008.parent = frame_010
    frame_009.parent = frame_010
    integer.parent = frame_009
    join_geometry_005.parent = frame_006
    join_geometry_006.parent = frame_007
    join_geometry_008.parent = frame_008
    join_splines.parent = frame_006
    join_splines_1.parent = frame_007
    map_range.parent = frame_009
    math.parent = frame_010
    math_001.parent = frame_010
    position.parent = frame_009
    quadratic_bézier_003.parent = frame_006
    quadratic_bézier_004.parent = frame_006
    quadratic_bézier_006.parent = frame_007
    quadratic_bézier_007.parent = frame_007
    separate_x_y_z.parent = frame_009
    set_position.parent = frame_009
    transform_geometry_001.parent = frame_007
    transform_geometry_002.parent = frame_009
    transform_geometry_003.parent = frame_009
    transform_geometry_004.parent = frame_009
    transform_geometry_005.parent = frame_009
    transform_geometry_006.parent = frame_006
    vector.parent = frame_006
    vector_001.parent = frame_007

    # Internal links
    links.new(quadratic_bézier_003.outputs[0], join_geometry_005.inputs[0])
    links.new(quadratic_bézier_004.outputs[0], join_geometry_005.inputs[0])
    links.new(join_geometry_005.outputs[0], join_splines.inputs[0])
    links.new(vector.outputs[0], quadratic_bézier_003.inputs[3])
    links.new(vector.outputs[0], quadratic_bézier_004.inputs[1])
    links.new(join_geometry_006.outputs[0], join_splines_1.inputs[0])
    links.new(quadratic_bézier_006.outputs[0], join_geometry_006.inputs[0])
    links.new(quadratic_bézier_007.outputs[0], join_geometry_006.inputs[0])
    links.new(vector_001.outputs[0], quadratic_bézier_006.inputs[3])
    links.new(vector_001.outputs[0], quadratic_bézier_007.inputs[1])
    links.new(join_geometry_008.outputs[0], bi_rail_loft.inputs[2])
    links.new(transform_geometry_002.outputs[0], bi_rail_loft.inputs[1])
    links.new(transform_geometry_003.outputs[0], set_position.inputs[0])
    links.new(set_position.outputs[0], bi_rail_loft.inputs[0])
    links.new(position.outputs[0], separate_x_y_z.inputs[0])
    links.new(separate_x_y_z.outputs[1], map_range.inputs[0])
    links.new(map_range.outputs[0], float_curve_001.inputs[1])
    links.new(combine_x_y_z.outputs[0], set_position.inputs[3])
    links.new(float_curve_001.outputs[0], combine_x_y_z.inputs[2])
    links.new(curve_circle_001.outputs[0], transform_geometry_004.inputs[0])
    links.new(transform_geometry_004.outputs[0], transform_geometry_003.inputs[0])
    links.new(transform_geometry_005.outputs[0], transform_geometry_002.inputs[0])
    links.new(curve_circle.outputs[0], transform_geometry_005.inputs[0])
    links.new(closure_output_001.outputs[0], bi_rail_loft.inputs[9])
    links.new(closure_input_001.outputs[0], math.inputs[0])
    links.new(math_001.outputs[0], closure_output_001.inputs[0])
    links.new(math.outputs[0], math_001.inputs[0])
    links.new(transform_geometry_001.outputs[0], join_geometry_008.inputs[0])
    links.new(join_splines_1.outputs[0], transform_geometry_001.inputs[0])
    links.new(transform_geometry_006.outputs[0], join_geometry_008.inputs[0])
    links.new(join_splines.outputs[0], transform_geometry_006.inputs[0])
    links.new(integer.outputs[0], curve_circle_001.inputs[0])
    links.new(integer.outputs[0], curve_circle.inputs[0])

    links.new(quadratic_bézier_003.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
