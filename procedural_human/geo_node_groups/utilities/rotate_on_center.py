import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group

@geo_node_group
def create_rotate_on__centre_group():
    group_name = "Rotate on Centre"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Rotation", in_out="INPUT", socket_type="NodeSocketRotation")
    socket.default_value = Euler((0.0, 0.0, 0.0), 'XYZ')

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    transform_geometry_014 = nodes.new("GeometryNodeTransform")
    transform_geometry_014.inputs[1].default_value = "Components"
    transform_geometry_014.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_014.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(group_input.outputs[1], transform_geometry_014.inputs[3])

    transform_geometry_016 = nodes.new("GeometryNodeTransform")
    transform_geometry_016.inputs[1].default_value = "Components"
    transform_geometry_016.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_016.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_016.outputs[0], transform_geometry_014.inputs[0])
    links.new(group_input.outputs[0], transform_geometry_016.inputs[0])

    transform_geometry_017 = nodes.new("GeometryNodeTransform")
    transform_geometry_017.inputs[1].default_value = "Components"
    transform_geometry_017.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_017.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_014.outputs[0], transform_geometry_017.inputs[0])
    links.new(transform_geometry_017.outputs[0], group_output.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.inputs[1].default_value = True
    links.new(group_input.outputs[0], bounding_box.inputs[0])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.operation = "SCALE"
    vector_math_008.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_008.inputs[3].default_value = -1.0
    links.new(vector_math_008.outputs[0], transform_geometry_016.inputs[2])

    mix = nodes.new("ShaderNodeMix")
    mix.data_type = "VECTOR"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.inputs[0].default_value = 0.5
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    mix.inputs[2].default_value = 0.0
    mix.inputs[3].default_value = 0.0
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    links.new(bounding_box.outputs[1], mix.inputs[4])
    links.new(mix.outputs[1], vector_math_008.inputs[0])
    links.new(bounding_box.outputs[2], mix.inputs[5])
    links.new(mix.outputs[1], transform_geometry_017.inputs[2])

    auto_layout_nodes(group)
    return group
