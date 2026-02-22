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
def create_neck_centre_profile_f008_group():
    group_name = "Neck_centre_profile_f008"
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


    frame_008 = nodes.new("NodeFrame")
    frame_008.label = "Profiles"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20


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


    # Parent assignments
    frame_006.parent = frame_008
    frame_007.parent = frame_008
    join_geometry_005.parent = frame_006
    join_geometry_006.parent = frame_007
    join_geometry_008.parent = frame_008
    join_splines.parent = frame_006
    join_splines_1.parent = frame_007
    quadratic_bézier_003.parent = frame_006
    quadratic_bézier_004.parent = frame_006
    quadratic_bézier_006.parent = frame_007
    quadratic_bézier_007.parent = frame_007
    transform_geometry_001.parent = frame_007
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
    links.new(transform_geometry_001.outputs[0], join_geometry_008.inputs[0])
    links.new(join_splines_1.outputs[0], transform_geometry_001.inputs[0])
    links.new(transform_geometry_006.outputs[0], join_geometry_008.inputs[0])
    links.new(join_splines.outputs[0], transform_geometry_006.inputs[0])

    links.new(quadratic_bézier_003.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
