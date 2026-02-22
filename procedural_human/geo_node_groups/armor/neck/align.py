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
def create_neck_align_group():
    group_name = "Neck_align"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Rotation", in_out="OUTPUT", socket_type="NodeSocketRotation")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector.inputs[1].default_value = 1.0


    curve_tangent_001 = nodes.new("GeometryNodeInputTangent")


    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.axis = "Y"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    align_rotation_to_vector_001.inputs[1].default_value = 1.0


    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.legacy_corner_normals = False


    rotate_rotation_003 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_003.rotation_space = "LOCAL"
    rotate_rotation_003.inputs[1].default_value = Euler((0.23108159005641937, 0.14137165248394012, 0.0), 'XYZ')


    rotate_rotation_004 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_004.rotation_space = "LOCAL"
    rotate_rotation_004.inputs[1].default_value = Euler((3.1415927410125732, 0.0, 1.5707963705062866), 'XYZ')


    frame_003 = nodes.new("NodeFrame")
    frame_003.label = "Align"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20


    # Parent assignments
    align_rotation_to_vector.parent = frame_003
    align_rotation_to_vector_001.parent = frame_003
    curve_tangent_001.parent = frame_003
    normal_001.parent = frame_003
    rotate_rotation_003.parent = frame_003
    rotate_rotation_004.parent = frame_003

    # Internal links
    links.new(curve_tangent_001.outputs[0], align_rotation_to_vector.inputs[2])
    links.new(align_rotation_to_vector.outputs[0], align_rotation_to_vector_001.inputs[0])
    links.new(normal_001.outputs[0], align_rotation_to_vector_001.inputs[2])
    links.new(align_rotation_to_vector_001.outputs[0], rotate_rotation_003.inputs[0])
    links.new(rotate_rotation_003.outputs[0], rotate_rotation_004.inputs[0])

    links.new(rotate_rotation_004.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
