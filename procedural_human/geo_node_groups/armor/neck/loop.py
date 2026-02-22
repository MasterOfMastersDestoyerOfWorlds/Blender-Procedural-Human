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
def create_neck_loop_group():
    group_name = "Neck_loop"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

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


    curve_circle_007 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_007.mode = "RADIUS"
    curve_circle_007.inputs[0].default_value = 6
    curve_circle_007.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_007.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_007.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_007.inputs[4].default_value = 0.009999999776482582


    frame_021 = nodes.new("NodeFrame")
    frame_021.label = "Loop"
    frame_021.text = None
    frame_021.shrink = True
    frame_021.label_size = 20


    # Parent assignments
    curve_circle_006.parent = frame_021
    curve_circle_007.parent = frame_021
    curve_to_mesh_002.parent = frame_021

    # Internal links
    links.new(curve_circle_006.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(curve_circle_007.outputs[0], curve_to_mesh_002.inputs[1])

    links.new(curve_circle_006.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
