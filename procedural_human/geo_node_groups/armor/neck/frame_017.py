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
def create_neck_frame_017_group():
    group_name = "Neck_frame_017"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

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


    # Parent assignments
    gold_decorations_2.parent = frame_017
    ico_sphere_007.parent = frame_017
    mesh_boolean_002.parent = frame_017
    mesh_to_curve.parent = frame_017
    resample_curve_003.parent = frame_017
    set_curve_normal_004.parent = frame_017
    set_curve_tilt.parent = frame_017
    transform_geometry_011.parent = frame_017
    transform_geometry_039.parent = frame_017
    trim_curve_003.parent = frame_017

    # Internal links
    links.new(trim_curve_003.outputs[0], resample_curve_003.inputs[0])
    links.new(resample_curve_003.outputs[0], set_curve_normal_004.inputs[0])
    links.new(transform_geometry_011.outputs[0], gold_decorations_2.inputs[0])
    links.new(mesh_to_curve.outputs[0], trim_curve_003.inputs[0])
    links.new(set_curve_tilt.outputs[0], transform_geometry_011.inputs[0])
    links.new(set_curve_normal_004.outputs[0], set_curve_tilt.inputs[0])
    links.new(gold_decorations_2.outputs[0], mesh_boolean_002.inputs[0])
    links.new(transform_geometry_039.outputs[0], mesh_boolean_002.inputs[1])
    links.new(ico_sphere_007.outputs[0], transform_geometry_039.inputs[0])

    links.new(trim_curve_003.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
