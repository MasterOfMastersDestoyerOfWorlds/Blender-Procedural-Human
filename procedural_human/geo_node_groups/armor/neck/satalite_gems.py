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
def create_neck_satalite_gems_group():
    group_name = "Neck_satalite_gems"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

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


    # Parent assignments
    curve_circle_012.parent = frame_025
    gem_in_holder_7.parent = frame_025
    instance_on_points_009.parent = frame_025
    transform_geometry_035.parent = frame_025

    # Internal links
    links.new(gem_in_holder_7.outputs[0], instance_on_points_009.inputs[2])
    links.new(transform_geometry_035.outputs[0], instance_on_points_009.inputs[0])
    links.new(curve_circle_012.outputs[0], transform_geometry_035.inputs[0])

    links.new(gem_in_holder_7.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
