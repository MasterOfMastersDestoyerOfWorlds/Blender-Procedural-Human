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
def create_neck_frame_005_group():
    group_name = "Neck_frame_005"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

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


    # Parent assignments
    curve_tangent.parent = frame_005
    gold_decorations.parent = frame_005
    normal.parent = frame_005
    resample_curve_001.parent = frame_005
    sample_nearest_surface.parent = frame_005
    set_curve_normal.parent = frame_005
    trim_curve.parent = frame_005

    # Internal links
    links.new(trim_curve.outputs[0], resample_curve_001.inputs[0])
    links.new(set_curve_normal.outputs[0], gold_decorations.inputs[0])
    links.new(resample_curve_001.outputs[0], set_curve_normal.inputs[0])
    links.new(normal.outputs[0], sample_nearest_surface.inputs[1])
    links.new(vector_math, set_curve_normal.inputs[3])

    links.new(trim_curve.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
