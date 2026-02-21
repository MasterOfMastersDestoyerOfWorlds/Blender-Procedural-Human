import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.shader_node_decorator import shader_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@shader_node_group
def create_voronoi__texture_group():
    group_name = "Voronoi Texture"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Distance", in_out="OUTPUT", socket_type="NodeSocketFloat")
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Color", in_out="OUTPUT", socket_type="NodeSocketColor")
    socket = group.interface.new_socket(name="Vector", in_out="INPUT", socket_type="NodeSocketVector")
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e+38
    socket.max_value = 3.4028234663852886e+38
    socket = group.interface.new_socket(name="Scale", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 500.0
    socket.min_value = -1000.0
    socket.max_value = 1000.0
    socket = group.interface.new_socket(name="Detail", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    socket.min_value = 0.0
    socket.max_value = 15.0
    socket = group.interface.new_socket(name="Roughness", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.5
    socket.min_value = 0.0
    socket.max_value = 1.0
    socket = group.interface.new_socket(name="Lacunarity", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 2.0
    socket.min_value = 0.0
    socket.max_value = 1000.0
    socket = group.interface.new_socket(name="Randomness", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.0
    socket.min_value = 0.0
    socket.max_value = 1.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-440.0, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (300.0, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    voronoi_texture = nodes.new("ShaderNodeTexVoronoi")
    voronoi_texture.name = "Voronoi Texture"
    voronoi_texture.label = ""
    voronoi_texture.location = (-77.5, 0.0)
    voronoi_texture.bl_label = "Voronoi Texture"
    voronoi_texture.voronoi_dimensions = "3D"
    voronoi_texture.distance = "EUCLIDEAN"
    voronoi_texture.feature = "DISTANCE_TO_EDGE"
    voronoi_texture.normalize = False
    # W
    voronoi_texture.inputs[1].default_value = 0.0
    # Smoothness
    voronoi_texture.inputs[6].default_value = 1.0
    # Exponent
    voronoi_texture.inputs[7].default_value = 0.5
    # Links for voronoi_texture
    links.new(group_input.outputs[0], voronoi_texture.inputs[0])
    links.new(group_input.outputs[1], voronoi_texture.inputs[2])
    links.new(group_input.outputs[2], voronoi_texture.inputs[3])
    links.new(group_input.outputs[3], voronoi_texture.inputs[4])
    links.new(group_input.outputs[4], voronoi_texture.inputs[5])
    links.new(group_input.outputs[5], voronoi_texture.inputs[8])
    links.new(voronoi_texture.outputs[0], group_output.inputs[0])

    voronoi_texture_001 = nodes.new("ShaderNodeTexVoronoi")
    voronoi_texture_001.name = "Voronoi Texture.001"
    voronoi_texture_001.label = ""
    voronoi_texture_001.location = (-80.0, 320.0)
    voronoi_texture_001.bl_label = "Voronoi Texture"
    voronoi_texture_001.voronoi_dimensions = "3D"
    voronoi_texture_001.distance = "EUCLIDEAN"
    voronoi_texture_001.feature = "F1"
    voronoi_texture_001.normalize = False
    # W
    voronoi_texture_001.inputs[1].default_value = 0.0
    # Smoothness
    voronoi_texture_001.inputs[6].default_value = 1.0
    # Exponent
    voronoi_texture_001.inputs[7].default_value = 0.5
    # Links for voronoi_texture_001
    links.new(group_input.outputs[0], voronoi_texture_001.inputs[0])
    links.new(group_input.outputs[1], voronoi_texture_001.inputs[2])
    links.new(group_input.outputs[2], voronoi_texture_001.inputs[3])
    links.new(group_input.outputs[3], voronoi_texture_001.inputs[4])
    links.new(group_input.outputs[4], voronoi_texture_001.inputs[5])
    links.new(group_input.outputs[5], voronoi_texture_001.inputs[8])
    links.new(voronoi_texture_001.outputs[1], group_output.inputs[1])

    auto_layout_nodes(group)
    return group

@shader_node_group
def create_gambeson_material_group():
    group_name = "GambesonMaterial"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    # --- Interface ---

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    material_output = nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.label = ""
    material_output.location = (315.0, 100.0)
    material_output.bl_label = "Material Output"
    material_output.is_active_output = True
    material_output.target = "ALL"
    # Displacement
    material_output.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Thickness
    material_output.inputs[3].default_value = 0.0
    # Links for material_output

    principled_b_s_d_f = nodes.new("ShaderNodeBsdfPrincipled")
    principled_b_s_d_f.name = "Principled BSDF"
    principled_b_s_d_f.label = ""
    principled_b_s_d_f.location = (20.0, 200.0)
    principled_b_s_d_f.bl_label = "Principled BSDF"
    principled_b_s_d_f.distribution = "MULTI_GGX"
    principled_b_s_d_f.subsurface_method = "RANDOM_WALK"
    # IOR
    principled_b_s_d_f.inputs[3].default_value = 1.5
    # Alpha
    principled_b_s_d_f.inputs[4].default_value = 1.0
    # Weight
    principled_b_s_d_f.inputs[6].default_value = 0.0
    # Diffuse Roughness
    principled_b_s_d_f.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_b_s_d_f.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_b_s_d_f.inputs[9].default_value = [1.0, 0.20000000298023224, 0.10000000149011612]
    # Subsurface Scale
    principled_b_s_d_f.inputs[10].default_value = 0.05000000074505806
    # Subsurface IOR
    principled_b_s_d_f.inputs[11].default_value = 1.399999976158142
    # Subsurface Anisotropy
    principled_b_s_d_f.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_b_s_d_f.inputs[13].default_value = 0.06797581911087036
    # Specular Tint
    principled_b_s_d_f.inputs[14].default_value = [1.0, 1.0, 1.0, 1.0]
    # Anisotropic
    principled_b_s_d_f.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_b_s_d_f.inputs[16].default_value = 0.0
    # Tangent
    principled_b_s_d_f.inputs[17].default_value = [0.0, 0.0, 0.0]
    # Transmission Weight
    principled_b_s_d_f.inputs[18].default_value = 0.0
    # Coat Weight
    principled_b_s_d_f.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_b_s_d_f.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_b_s_d_f.inputs[21].default_value = 1.5
    # Coat Tint
    principled_b_s_d_f.inputs[22].default_value = [1.0, 1.0, 1.0, 1.0]
    # Coat Normal
    principled_b_s_d_f.inputs[23].default_value = [0.0, 0.0, 0.0]
    # Sheen Weight
    principled_b_s_d_f.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_b_s_d_f.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_b_s_d_f.inputs[26].default_value = [1.0, 1.0, 1.0, 1.0]
    # Emission Color
    principled_b_s_d_f.inputs[27].default_value = [1.0, 1.0, 1.0, 1.0]
    # Emission Strength
    principled_b_s_d_f.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_b_s_d_f.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_b_s_d_f.inputs[30].default_value = 1.3300000429153442
    # Links for principled_b_s_d_f
    links.new(principled_b_s_d_f.outputs[0], material_output.inputs[0])

    texture_coordinate = nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.label = ""
    texture_coordinate.location = (-2040.0, -200.0)
    texture_coordinate.bl_label = "Texture Coordinate"
    texture_coordinate.object = None
    texture_coordinate.from_instancer = False
    # Links for texture_coordinate

    mapping = nodes.new("ShaderNodeMapping")
    mapping.name = "Mapping"
    mapping.label = ""
    mapping.location = (-1880.0, -200.0)
    mapping.bl_label = "Mapping"
    mapping.vector_type = "POINT"
    # Location
    mapping.inputs[1].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    mapping.inputs[2].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    mapping.inputs[3].default_value = Vector((1.0, 0.5, 1.0))
    # Links for mapping
    links.new(texture_coordinate.outputs[2], mapping.inputs[0])

    bump = nodes.new("ShaderNodeBump")
    bump.name = "Bump"
    bump.label = ""
    bump.location = (-1080.0, -140.0)
    bump.bl_label = "Bump"
    bump.invert = True
    # Strength
    bump.inputs[0].default_value = 1.0
    # Distance
    bump.inputs[1].default_value = 0.0003000000142492354
    # Filter Width
    bump.inputs[2].default_value = 0.10000000149011612
    # Normal
    bump.inputs[4].default_value = [0.0, 0.0, 0.0]
    # Links for bump
    links.new(bump.outputs[0], principled_b_s_d_f.inputs[5])

    ambient_occlusion = nodes.new("ShaderNodeAmbientOcclusion")
    ambient_occlusion.name = "Ambient Occlusion"
    ambient_occlusion.label = ""
    ambient_occlusion.location = (-940.0, 160.0)
    ambient_occlusion.bl_label = "Ambient Occlusion"
    ambient_occlusion.samples = 16
    ambient_occlusion.inside = False
    ambient_occlusion.only_local = False
    # Color
    ambient_occlusion.inputs[0].default_value = [1.0, 1.0, 1.0, 1.0]
    # Distance
    ambient_occlusion.inputs[1].default_value = 1.0
    # Links for ambient_occlusion
    links.new(bump.outputs[0], ambient_occlusion.inputs[2])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-760.0, 160.0)
    math.bl_label = "Math"
    math.operation = "POWER"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 3.0
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(ambient_occlusion.outputs[1], math.inputs[0])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (-420.0, 160.0)
    mix.bl_label = "Mix"
    mix.data_type = "RGBA"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MULTIPLY"
    mix.clamp_factor = True
    mix.clamp_result = False
    # Factor
    mix.inputs[0].default_value = 0.8080110549926758
    # Factor
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix.inputs[2].default_value = 0.0
    # B
    mix.inputs[3].default_value = 0.0
    # A
    mix.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix
    links.new(mix.outputs[2], principled_b_s_d_f.inputs[0])
    links.new(math.outputs[0], mix.inputs[7])

    attribute = nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.label = ""
    attribute.location = (-900.0, 660.0)
    attribute.bl_label = "Attribute"
    attribute.attribute_type = "GEOMETRY"
    attribute.attribute_name = "stitching"
    # Links for attribute

    attribute_001 = nodes.new("ShaderNodeAttribute")
    attribute_001.name = "Attribute.001"
    attribute_001.label = ""
    attribute_001.location = (-720.0, 660.0)
    attribute_001.bl_label = "Attribute"
    attribute_001.attribute_type = "GEOMETRY"
    attribute_001.attribute_name = "piping"
    # Links for attribute_001

    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.label = ""
    mix_001.location = (-720.0, 540.0)
    mix_001.bl_label = "Mix"
    mix_001.data_type = "RGBA"
    mix_001.factor_mode = "UNIFORM"
    mix_001.blend_type = "MIX"
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    # Factor
    mix_001.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_001.inputs[2].default_value = 0.0
    # B
    mix_001.inputs[3].default_value = 0.0
    # A
    mix_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # B
    mix_001.inputs[7].default_value = [0.03267429769039154, 0.005270657129585743, 0.005270657129585743, 1.0]
    # A
    mix_001.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_001.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_001
    links.new(mix_001.outputs[2], mix.inputs[6])
    links.new(attribute_001.outputs[2], mix_001.inputs[0])

    mix_002 = nodes.new("ShaderNodeMix")
    mix_002.name = "Mix.002"
    mix_002.label = ""
    mix_002.location = (-900.0, 540.0)
    mix_002.bl_label = "Mix"
    mix_002.data_type = "RGBA"
    mix_002.factor_mode = "UNIFORM"
    mix_002.blend_type = "MIX"
    mix_002.clamp_factor = True
    mix_002.clamp_result = False
    # Factor
    mix_002.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_002.inputs[2].default_value = 0.0
    # B
    mix_002.inputs[3].default_value = 0.0
    # A
    mix_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    # B
    mix_002.inputs[7].default_value = [0.5569925904273987, 0.39231517910957336, 0.05043492466211319, 1.0]
    # A
    mix_002.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_002.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_002
    links.new(mix_002.outputs[2], mix_001.inputs[6])
    links.new(attribute.outputs[2], mix_002.inputs[0])

    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.name = "Mix.003"
    mix_003.label = ""
    mix_003.location = (-320.0, 540.0)
    mix_003.bl_label = "Mix"
    mix_003.data_type = "FLOAT"
    mix_003.factor_mode = "UNIFORM"
    mix_003.blend_type = "MIX"
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    # Factor
    mix_003.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_003.inputs[2].default_value = 0.0
    # B
    mix_003.inputs[3].default_value = 1.0
    # A
    mix_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_003.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_003.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_003.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_003.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_003
    links.new(mix_003.outputs[0], principled_b_s_d_f.inputs[1])

    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.name = "Mix.004"
    mix_004.label = ""
    mix_004.location = (-320.0, 360.0)
    mix_004.bl_label = "Mix"
    mix_004.data_type = "FLOAT"
    mix_004.factor_mode = "UNIFORM"
    mix_004.blend_type = "MIX"
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    # Factor
    mix_004.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_004.inputs[2].default_value = 1.0
    # B
    mix_004.inputs[3].default_value = 0.6000000238418579
    # A
    mix_004.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_004.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_004.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_004.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_004.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_004.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_004
    links.new(mix_004.outputs[0], principled_b_s_d_f.inputs[2])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (-395.488037109375, 393.509521484375)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketFloat"
    # Links for reroute
    links.new(reroute.outputs[0], mix_004.inputs[0])
    links.new(reroute.outputs[0], mix_003.inputs[0])
    links.new(attribute.outputs[2], reroute.inputs[0])

    voronoi_texture = nodes.new("ShaderNodeGroup")
    voronoi_texture.name = "Voronoi Texture"
    voronoi_texture.label = ""
    voronoi_texture.location = (-1600.0, -140.0)
    voronoi_texture.node_tree = create_voronoi__texture_group()
    voronoi_texture.bl_label = "Group"
    # Scale
    voronoi_texture.inputs[1].default_value = 500.0
    # Detail
    voronoi_texture.inputs[2].default_value = 0.0
    # Roughness
    voronoi_texture.inputs[3].default_value = 0.5
    # Lacunarity
    voronoi_texture.inputs[4].default_value = 2.0
    # Randomness
    voronoi_texture.inputs[5].default_value = 0.0
    # Links for voronoi_texture
    links.new(mapping.outputs[0], voronoi_texture.inputs[0])
    links.new(voronoi_texture.outputs[0], bump.inputs[3])

    mix_005 = nodes.new("ShaderNodeMix")
    mix_005.name = "Mix.005"
    mix_005.label = ""
    mix_005.location = (-1200.0, 380.0)
    mix_005.bl_label = "Mix"
    mix_005.data_type = "RGBA"
    mix_005.factor_mode = "UNIFORM"
    mix_005.blend_type = "MULTIPLY"
    mix_005.clamp_factor = True
    mix_005.clamp_result = False
    # Factor
    mix_005.inputs[0].default_value = 0.20000000298023224
    # Factor
    mix_005.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_005.inputs[2].default_value = 0.0
    # B
    mix_005.inputs[3].default_value = 0.0
    # A
    mix_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_005.inputs[6].default_value = [0.05520150810480118, 0.02380118891596794, 0.01722710393369198, 1.0]
    # A
    mix_005.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_005.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_005
    links.new(mix_005.outputs[2], mix_002.inputs[6])
    links.new(voronoi_texture.outputs[1], mix_005.inputs[7])

    auto_layout_nodes(group)
    return group