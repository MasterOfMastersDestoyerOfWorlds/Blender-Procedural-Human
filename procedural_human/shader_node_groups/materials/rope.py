import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.shader_node_decorator import shader_node_group


@shader_node_group
def create_rope_material_group():
    group_name = "RopeMaterial"
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
    material_output.location = (260.0, 100.0)
    material_output.bl_label = "Material Output"
    material_output.is_active_output = True
    material_output.target = "ALL"
    # Displacement
    material_output.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Thickness
    material_output.inputs[3].default_value = 0.0
    # Links for material_output

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (-460.0, 120.0)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "3D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = True
    # W
    noise_texture.inputs[1].default_value = 0.0
    # Scale
    noise_texture.inputs[2].default_value = 500.0
    # Detail
    noise_texture.inputs[3].default_value = 0.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Offset
    noise_texture.inputs[6].default_value = 0.0
    # Gain
    noise_texture.inputs[7].default_value = 1.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0
    # Links for noise_texture

    attribute = nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.label = ""
    attribute.location = (-800.0, 120.0)
    attribute.bl_label = "Attribute"
    attribute.attribute_type = "GEOMETRY"
    attribute.attribute_name = "UVMap"
    # Links for attribute

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (-620.0, 120.0)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "MULTIPLY"
    # Vector
    vector_math.inputs[1].default_value = [0.10000000149011612, 1.0, 0.0]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(vector_math.outputs[0], noise_texture.inputs[0])
    links.new(attribute.outputs[1], vector_math.inputs[0])

    bump = nodes.new("ShaderNodeBump")
    bump.name = "Bump"
    bump.label = ""
    bump.location = (-280.0, 120.0)
    bump.bl_label = "Bump"
    bump.invert = False
    # Strength
    bump.inputs[0].default_value = 1.0
    # Distance
    bump.inputs[1].default_value = 0.0010000000474974513
    # Filter Width
    bump.inputs[2].default_value = 0.10000000149011612
    # Normal
    bump.inputs[4].default_value = [0.0, 0.0, 0.0]
    # Links for bump
    links.new(noise_texture.outputs[0], bump.inputs[3])

    principled_b_s_d_f = nodes.new("ShaderNodeBsdfPrincipled")
    principled_b_s_d_f.name = "Principled BSDF"
    principled_b_s_d_f.label = ""
    principled_b_s_d_f.location = (-40.0, 240.0)
    principled_b_s_d_f.bl_label = "Principled BSDF"
    principled_b_s_d_f.distribution = "MULTI_GGX"
    principled_b_s_d_f.subsurface_method = "RANDOM_WALK"
    # Metallic
    principled_b_s_d_f.inputs[1].default_value = 0.0
    # Roughness
    principled_b_s_d_f.inputs[2].default_value = 0.5558912754058838
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
    principled_b_s_d_f.inputs[13].default_value = 0.12990936636924744
    # Specular Tint
    principled_b_s_d_f.inputs[14].default_value = [0.42307132482528687, 0.05193892866373062, 0.05193892866373062, 1.0]
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
    principled_b_s_d_f.inputs[24].default_value = 1.0
    # Sheen Roughness
    principled_b_s_d_f.inputs[25].default_value = 0.2522658407688141
    # Sheen Tint
    principled_b_s_d_f.inputs[26].default_value = [0.02875443920493126, 0.003672473132610321, 0.000569276453461498, 1.0]
    # Emission Color
    principled_b_s_d_f.inputs[27].default_value = [1.0, 1.0, 1.0, 1.0]
    # Emission Strength
    principled_b_s_d_f.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_b_s_d_f.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_b_s_d_f.inputs[30].default_value = 1.3300000429153442
    # Links for principled_b_s_d_f
    links.new(bump.outputs[0], principled_b_s_d_f.inputs[5])
    links.new(principled_b_s_d_f.outputs[0], material_output.inputs[0])

    noise_texture_001 = nodes.new("ShaderNodeTexNoise")
    noise_texture_001.name = "Noise Texture.001"
    noise_texture_001.label = ""
    noise_texture_001.location = (-580.0, 420.0)
    noise_texture_001.bl_label = "Noise Texture"
    noise_texture_001.noise_dimensions = "3D"
    noise_texture_001.noise_type = "FBM"
    noise_texture_001.normalize = True
    # W
    noise_texture_001.inputs[1].default_value = 0.0
    # Scale
    noise_texture_001.inputs[2].default_value = 100.0
    # Detail
    noise_texture_001.inputs[3].default_value = 2.0
    # Roughness
    noise_texture_001.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture_001.inputs[5].default_value = 2.0
    # Offset
    noise_texture_001.inputs[6].default_value = 0.0
    # Gain
    noise_texture_001.inputs[7].default_value = 1.0
    # Distortion
    noise_texture_001.inputs[8].default_value = 0.0
    # Links for noise_texture_001
    links.new(attribute.outputs[1], noise_texture_001.inputs[0])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (-380.0, 440.0)
    mix.bl_label = "Mix"
    mix.data_type = "RGBA"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "OVERLAY"
    mix.clamp_factor = True
    mix.clamp_result = False
    # Factor
    mix.inputs[0].default_value = 0.0883978009223938
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
    mix.inputs[6].default_value = [0.0942532867193222, 0.0, 0.0, 1.0]
    # A
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix
    links.new(noise_texture_001.outputs[0], mix.inputs[7])

    ambient_occlusion = nodes.new("ShaderNodeAmbientOcclusion")
    ambient_occlusion.name = "Ambient Occlusion"
    ambient_occlusion.label = ""
    ambient_occlusion.location = (-780.0, 580.0)
    ambient_occlusion.bl_label = "Ambient Occlusion"
    ambient_occlusion.samples = 16
    ambient_occlusion.inside = False
    ambient_occlusion.only_local = False
    # Color
    ambient_occlusion.inputs[0].default_value = [1.0, 1.0, 1.0, 1.0]
    # Distance
    ambient_occlusion.inputs[1].default_value = 1.0
    # Normal
    ambient_occlusion.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for ambient_occlusion

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-600.0, 580.0)
    math.bl_label = "Math"
    math.operation = "POWER"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 3.0
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(ambient_occlusion.outputs[1], math.inputs[0])

    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.label = ""
    mix_001.location = (-200.00001525878906, 420.0)
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
    # A
    mix_001.inputs[6].default_value = [0.04062913730740547, 0.010317648760974407, 0.00479144835844636, 1.0]
    # A
    mix_001.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_001.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_001
    links.new(mix_001.outputs[2], principled_b_s_d_f.inputs[0])
    links.new(math.outputs[0], mix_001.inputs[0])
    links.new(mix.outputs[2], mix_001.inputs[7])

    auto_layout_nodes(group)
    return group