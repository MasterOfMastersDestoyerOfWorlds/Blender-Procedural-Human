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
def create_neck_link_group():
    group_name = "Neck_link"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

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


    # Parent assignments
    curve_circle_005.parent = frame_019
    curve_to_mesh_001.parent = frame_019
    fillet_curve.parent = frame_019
    quadrilateral.parent = frame_019
    set_spline_type.parent = frame_019

    # Internal links
    links.new(set_spline_type.outputs[0], fillet_curve.inputs[0])
    links.new(quadrilateral.outputs[0], set_spline_type.inputs[0])
    links.new(fillet_curve.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(curve_circle_005.outputs[0], curve_to_mesh_001.inputs[1])

    links.new(quadrilateral.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
