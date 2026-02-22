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
def create_neck_frame_013_group():
    group_name = "Neck_frame_013"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

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


    # Parent assignments
    compare_007.parent = frame_013
    gold_decorations_1.parent = frame_013
    resample_curve_002.parent = frame_013
    separate_geometry_002.parent = frame_013
    separate_x_y_z_004.parent = frame_013
    set_curve_normal_003.parent = frame_013
    transform_geometry.parent = frame_013
    trim_curve_002.parent = frame_013

    # Internal links
    links.new(compare_007.outputs[0], separate_geometry_002.inputs[1])
    links.new(separate_x_y_z_004.outputs[1], compare_007.inputs[0])
    links.new(separate_geometry_002.outputs[0], trim_curve_002.inputs[0])
    links.new(trim_curve_002.outputs[0], resample_curve_002.inputs[0])
    links.new(resample_curve_002.outputs[0], set_curve_normal_003.inputs[0])
    links.new(transform_geometry.outputs[0], gold_decorations_1.inputs[0])
    links.new(set_curve_normal_003.outputs[0], transform_geometry.inputs[0])

    links.new(separate_geometry_002.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
