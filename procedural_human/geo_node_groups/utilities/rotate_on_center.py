import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector

@geo_node_group
def create_rotate_on__centre_group():
    group_name = "Rotate on Centre"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Rotation", in_out="INPUT", socket_type="NodeSocketRotation")
    socket.default_value = Euler((0.0, 0.0, 0.0), 'XYZ')

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (655.9169921875, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-636.91650390625, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    transform_geometry_014 = nodes.new("GeometryNodeTransform")
    transform_geometry_014.name = "Transform Geometry.014"
    transform_geometry_014.label = ""
    transform_geometry_014.location = (276.9169921875, 22.100006103515625)
    transform_geometry_014.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_014.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_014.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Scale
    transform_geometry_014.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_014
    links.new(group_input.outputs[1], transform_geometry_014.inputs[3])

    transform_geometry_016 = nodes.new("GeometryNodeTransform")
    transform_geometry_016.name = "Transform Geometry.016"
    transform_geometry_016.label = ""
    transform_geometry_016.location = (116.9169921875, 22.100006103515625)
    transform_geometry_016.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_016.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_016.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_016.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_016
    links.new(transform_geometry_016.outputs[0], transform_geometry_014.inputs[0])
    links.new(group_input.outputs[0], transform_geometry_016.inputs[0])

    transform_geometry_017 = nodes.new("GeometryNodeTransform")
    transform_geometry_017.name = "Transform Geometry.017"
    transform_geometry_017.label = ""
    transform_geometry_017.location = (436.9169921875, 22.100006103515625)
    transform_geometry_017.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_017.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_017.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_017.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_017
    links.new(transform_geometry_014.outputs[0], transform_geometry_017.inputs[0])
    links.new(transform_geometry_017.outputs[0], group_output.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    bounding_box.label = ""
    bounding_box.location = (-363.0830078125, -57.899993896484375)
    bounding_box.bl_label = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = True
    # Links for bounding_box
    links.new(group_input.outputs[0], bounding_box.inputs[0])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.label = ""
    vector_math_008.location = (-43.0830078125, -57.899993896484375)
    vector_math_008.bl_label = "Vector Math"
    vector_math_008.operation = "SCALE"
    # Vector
    vector_math_008.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_008.inputs[3].default_value = -1.0
    # Links for vector_math_008
    links.new(vector_math_008.outputs[0], transform_geometry_016.inputs[2])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (-203.0830078125, -57.899993896484375)
    mix.bl_label = "Mix"
    mix.data_type = "VECTOR"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    # Factor
    mix.inputs[0].default_value = 0.5
    # Factor
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix.inputs[2].default_value = 0.0
    # B
    mix.inputs[3].default_value = 0.0
    # A
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix
    links.new(bounding_box.outputs[1], mix.inputs[4])
    links.new(mix.outputs[1], vector_math_008.inputs[0])
    links.new(bounding_box.outputs[2], mix.inputs[5])
    links.new(mix.outputs[1], transform_geometry_017.inputs[2])

    auto_layout_nodes(group)
    return group
