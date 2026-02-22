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
def create_neck_align_f020_group():
    group_name = "Neck_align_f020"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Rotation", in_out="OUTPUT", socket_type="NodeSocketRotation")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.axis = "X"
    align_rotation_to_vector_002.pivot_axis = "AUTO"
    align_rotation_to_vector_002.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_002.inputs[1].default_value = 1.0


    curve_tangent_002 = nodes.new("GeometryNodeInputTangent")


    align_rotation_to_vector_003 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_003.axis = "Y"
    align_rotation_to_vector_003.pivot_axis = "AUTO"
    align_rotation_to_vector_003.inputs[1].default_value = 1.0


    normal_002 = nodes.new("GeometryNodeInputNormal")
    normal_002.legacy_corner_normals = False


    frame_020 = nodes.new("NodeFrame")
    frame_020.label = "Align"
    frame_020.text = None
    frame_020.shrink = True
    frame_020.label_size = 20


    rotate_rotation_006 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_006.rotation_space = "LOCAL"


    rotate_rotation_005 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_005.rotation_space = "LOCAL"


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


    index_001 = nodes.new("GeometryNodeInputIndex")


    math_016 = nodes.new("ShaderNodeMath")
    math_016.operation = "FLOORED_MODULO"
    math_016.inputs[1].default_value = 2.0
    math_016.inputs[2].default_value = 0.5


    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "FLOAT"
    switch_001.inputs[1].default_value = -0.3799999952316284
    switch_001.inputs[2].default_value = 0.5


    combine_x_y_z_006 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_006.inputs[1].default_value = 0.0
    combine_x_y_z_006.inputs[2].default_value = 0.0


    # Parent assignments
    align_rotation_to_vector_002.parent = frame_020
    align_rotation_to_vector_003.parent = frame_020
    combine_x_y_z_006.parent = frame_020
    curve_tangent_002.parent = frame_020
    index_001.parent = frame_020
    math_016.parent = frame_020
    normal_002.parent = frame_020
    random_value_012.parent = frame_020
    rotate_rotation_005.parent = frame_020
    rotate_rotation_006.parent = frame_020
    switch_001.parent = frame_020

    # Internal links
    links.new(curve_tangent_002.outputs[0], align_rotation_to_vector_002.inputs[2])
    links.new(align_rotation_to_vector_002.outputs[0], align_rotation_to_vector_003.inputs[0])
    links.new(normal_002.outputs[0], align_rotation_to_vector_003.inputs[2])
    links.new(align_rotation_to_vector_003.outputs[0], rotate_rotation_005.inputs[0])
    links.new(rotate_rotation_005.outputs[0], rotate_rotation_006.inputs[0])
    links.new(random_value_012.outputs[0], rotate_rotation_006.inputs[1])
    links.new(index_001.outputs[0], math_016.inputs[0])
    links.new(math_016.outputs[0], switch_001.inputs[0])
    links.new(switch_001.outputs[0], combine_x_y_z_006.inputs[0])
    links.new(combine_x_y_z_006.outputs[0], rotate_rotation_005.inputs[1])

    links.new(rotate_rotation_006.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
