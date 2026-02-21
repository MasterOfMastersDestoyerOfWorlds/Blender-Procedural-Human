import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.shader_node_decorator import shader_node_group


@shader_node_group
def create_gold_material_group():
    group_name = "GoldMaterial"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")

    # --- Interface ---

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    principled_b_s_d_f = nodes.new("ShaderNodeBsdfPrincipled")
    principled_b_s_d_f.name = "Principled BSDF"
    principled_b_s_d_f.label = ""
    principled_b_s_d_f.location = (-200.0, 100.0)
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
    principled_b_s_d_f.inputs[13].default_value = 0.5
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

    material_output = nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.label = ""
    material_output.location = (200.0, 100.0)
    material_output.bl_label = "Material Output"
    material_output.is_active_output = True
    material_output.target = "ALL"
    # Displacement
    material_output.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Thickness
    material_output.inputs[3].default_value = 0.0
    # Links for material_output
    links.new(principled_b_s_d_f.outputs[0], material_output.inputs[0])

    ambient_occlusion = nodes.new("ShaderNodeAmbientOcclusion")
    ambient_occlusion.name = "Ambient Occlusion"
    ambient_occlusion.label = ""
    ambient_occlusion.location = (-1920.0, 40.0)
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
    math.location = (-1380.0, 40.0)
    math.bl_label = "Math"
    math.operation = "POWER"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 4.5
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (-920.0, -20.0)
    mix.bl_label = "Mix"
    mix.data_type = "FLOAT"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
    # Factor
    mix.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix.inputs[2].default_value = 0.4000000059604645
    # B
    mix.inputs[3].default_value = 1.0
    # A
    mix.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix
    links.new(mix.outputs[0], principled_b_s_d_f.inputs[1])

    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.label = ""
    mix_001.location = (-740.0, 280.0)
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
    mix_001.inputs[3].default_value = 1.0
    # A
    mix_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_001.inputs[6].default_value = [0.058471061289310455, 0.027111006900668144, 0.001040724921040237, 1.0]
    # A
    mix_001.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_001.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_001
    links.new(mix_001.outputs[2], principled_b_s_d_f.inputs[0])

    mix_002 = nodes.new("ShaderNodeMix")
    mix_002.name = "Mix.002"
    mix_002.label = ""
    mix_002.location = (-920.0, -200.0)
    mix_002.bl_label = "Mix"
    mix_002.data_type = "FLOAT"
    mix_002.factor_mode = "UNIFORM"
    mix_002.blend_type = "MIX"
    mix_002.clamp_factor = True
    mix_002.clamp_result = False
    # Factor
    mix_002.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_002.inputs[2].default_value = 0.4000000059604645
    # B
    mix_002.inputs[3].default_value = 0.05000000074505806
    # A
    mix_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_002.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_002.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_002.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_002.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_002

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (-1760.0, -420.0)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "3D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = True
    # W
    noise_texture.inputs[1].default_value = 0.0
    # Scale
    noise_texture.inputs[2].default_value = 612.5999755859375
    # Detail
    noise_texture.inputs[3].default_value = 2.0
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

    geometry = nodes.new("ShaderNodeNewGeometry")
    geometry.name = "Geometry"
    geometry.label = ""
    geometry.location = (-1920.0, -420.0)
    geometry.bl_label = "Geometry"
    # Links for geometry
    links.new(geometry.outputs[0], noise_texture.inputs[0])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (-920.0, -400.0)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    # From Min
    map_range.inputs[1].default_value = 0.19999998807907104
    # From Max
    map_range.inputs[2].default_value = 0.7999999523162842
    # To Min
    map_range.inputs[3].default_value = 1.0
    # To Max
    map_range.inputs[4].default_value = 1.0
    # Steps
    map_range.inputs[5].default_value = 4.0
    # Vector
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(noise_texture.outputs[0], map_range.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-740.0, -200.0)
    math_001.bl_label = "Math"
    math_001.operation = "DIVIDE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(mix_002.outputs[0], math_001.inputs[0])
    links.new(math_001.outputs[0], principled_b_s_d_f.inputs[2])
    links.new(map_range.outputs[0], math_001.inputs[1])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (-1040.0, -60.0)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketFloat"
    # Links for reroute
    links.new(reroute.outputs[0], mix.inputs[0])
    links.new(reroute.outputs[0], mix_001.inputs[0])
    links.new(reroute.outputs[0], mix_002.inputs[0])

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.label = ""
    map_range_001.location = (-1220.0, 40.0)
    map_range_001.bl_label = "Map Range"
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT"
    # From Min
    map_range_001.inputs[1].default_value = 0.29999998211860657
    # From Max
    map_range_001.inputs[2].default_value = 0.5999999046325684
    # To Min
    map_range_001.inputs[3].default_value = 0.0
    # To Max
    map_range_001.inputs[4].default_value = 1.0
    # Steps
    map_range_001.inputs[5].default_value = 4.0
    # Vector
    map_range_001.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_001.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_001.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_001.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_001.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_001
    links.new(map_range_001.outputs[0], reroute.inputs[0])
    links.new(math.outputs[0], map_range_001.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (-1620.0, 40.0)
    math_002.bl_label = "Math"
    math_002.operation = "SUBTRACT"
    math_002.use_clamp = False
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(math_002.outputs[0], math.inputs[0])
    links.new(ambient_occlusion.outputs[1], math_002.inputs[0])

    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.name = "Map Range.002"
    map_range_002.label = ""
    map_range_002.location = (-1760.0, -120.0)
    map_range_002.bl_label = "Map Range"
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    # From Min
    map_range_002.inputs[1].default_value = 0.19999998807907104
    # From Max
    map_range_002.inputs[2].default_value = 0.7999999523162842
    # To Min
    map_range_002.inputs[3].default_value = 0.0
    # To Max
    map_range_002.inputs[4].default_value = 0.09999999403953552
    # Steps
    map_range_002.inputs[5].default_value = 4.0
    # Vector
    map_range_002.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_002.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_002.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_002.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_002.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_002.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_002
    links.new(noise_texture.outputs[0], map_range_002.inputs[0])
    links.new(map_range_002.outputs[0], math_002.inputs[1])

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (-980.0, -720.0)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(noise_texture.outputs[1], separate_x_y_z.inputs[0])

    bump = nodes.new("ShaderNodeBump")
    bump.name = "Bump"
    bump.label = ""
    bump.location = (-460.0, -700.0)
    bump.bl_label = "Bump"
    bump.invert = True
    # Strength
    bump.inputs[0].default_value = 1.0
    # Distance
    bump.inputs[1].default_value = 9.999999747378752e-05
    # Filter Width
    bump.inputs[2].default_value = 0.10000000149011612
    # Normal
    bump.inputs[4].default_value = [0.0, 0.0, 0.0]
    # Links for bump
    links.new(bump.outputs[0], principled_b_s_d_f.inputs[5])

    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.name = "Map Range.003"
    map_range_003.label = ""
    map_range_003.location = (-800.0, -700.0)
    map_range_003.bl_label = "Map Range"
    map_range_003.clamp = True
    map_range_003.interpolation_type = "LINEAR"
    map_range_003.data_type = "FLOAT"
    # From Min
    map_range_003.inputs[1].default_value = 0.4999999701976776
    # From Max
    map_range_003.inputs[2].default_value = 0.7999999523162842
    # To Min
    map_range_003.inputs[3].default_value = 0.0
    # To Max
    map_range_003.inputs[4].default_value = 1.0
    # Steps
    map_range_003.inputs[5].default_value = 4.0
    # Vector
    map_range_003.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_003.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_003.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_003.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_003.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_003.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_003
    links.new(map_range_003.outputs[0], bump.inputs[3])
    links.new(separate_x_y_z.outputs[1], map_range_003.inputs[0])

    color_001 = nodes.new("ShaderNodeRGB")
    color_001.name = "Color.001"
    color_001.label = ""
    color_001.location = (-1240.0, 280.0)
    color_001.bl_label = "Color"
    # Links for color_001
    links.new(color_001.outputs[0], mix_001.inputs[7])

    a_o_v_output = nodes.new("ShaderNodeOutputAOV")
    a_o_v_output.name = "AOV Output"
    a_o_v_output.label = ""
    a_o_v_output.location = (200.0, -60.0)
    a_o_v_output.bl_label = "AOV Output"
    a_o_v_output.aov_name = "gold"
    # Color
    a_o_v_output.inputs[0].default_value = [0.0, 0.0, 0.0, 1.0]
    # Value
    a_o_v_output.inputs[1].default_value = 1.0
    # Links for a_o_v_output

    auto_layout_nodes(group)
    return group