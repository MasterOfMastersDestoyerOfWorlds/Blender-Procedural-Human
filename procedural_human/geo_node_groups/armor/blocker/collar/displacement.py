import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.geo_node_groups.node_helpers import math_op, set_position, vec_math_op
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_blocker_collar_displacement_group():
    group_name = "BlockerCollarDisplacement"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Vector", in_out="INPUT", socket_type="NodeSocketVector")

    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    vector_math_003 = vec_math_op(group, "MULTIPLY", [0.0, 0.0, 0.0], [1.0, 2.5999999046325684, 24.950000762939453])
    vector_math_003.node.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_003.node.inputs[3].default_value = 1.0

    noise_texture_002 = nodes.new("ShaderNodeTexNoise")
    noise_texture_002.noise_dimensions = "4D"
    noise_texture_002.noise_type = "FBM"
    noise_texture_002.normalize = False
    noise_texture_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    noise_texture_002.inputs[1].default_value = 44.769989013671875
    noise_texture_002.inputs[2].default_value = 17.969999313354492
    noise_texture_002.inputs[3].default_value = 0.0
    noise_texture_002.inputs[4].default_value = 0.5
    noise_texture_002.inputs[5].default_value = 2.0
    noise_texture_002.inputs[6].default_value = 0.0
    noise_texture_002.inputs[7].default_value = 1.0
    noise_texture_002.inputs[8].default_value = 0.0

    noise_texture_001 = nodes.new("ShaderNodeTexNoise")
    noise_texture_001.noise_dimensions = "2D"
    noise_texture_001.noise_type = "FBM"
    noise_texture_001.normalize = False
    noise_texture_001.inputs[1].default_value = 0.0
    noise_texture_001.inputs[2].default_value = 5.669999599456787
    noise_texture_001.inputs[3].default_value = 0.0
    noise_texture_001.inputs[4].default_value = 0.5
    noise_texture_001.inputs[5].default_value = 2.0
    noise_texture_001.inputs[6].default_value = 0.0
    noise_texture_001.inputs[7].default_value = 1.0
    noise_texture_001.inputs[8].default_value = 0.0
    links.new(vector_math_003, noise_texture_001.inputs[0])

    vector_math_005 = vec_math_op(group, "SCALE", noise_texture_002.outputs[1], 0.006000000052154064)
    vector_math_005.node.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_005.node.inputs[2].default_value = [0.0, 0.0, 0.0]

    vector_math_002 = vec_math_op(group, "SCALE", noise_texture_001.outputs[1], 0.0020000000949949026)
    vector_math_002.node.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_002.node.inputs[2].default_value = [0.0, 0.0, 0.0]

    vector_math_006 = vec_math_op(group, "ADD", vector_math_002, vector_math_005)
    vector_math_006.node.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_006.node.inputs[3].default_value = 1.0

    set_position_001 = set_position(group, None, True, [0.0, 0.0, 0.0], vector_math_006)

    links.new(group_input.outputs[0], set_position_001.node.inputs[0])
    links.new(group_input.outputs[1], vector_math_003.node.inputs[0])
    links.new(set_position_001, group_output.inputs[0])

    auto_layout_nodes(group)
    return group