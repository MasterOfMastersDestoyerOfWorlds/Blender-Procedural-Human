import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.shader_node_decorator import shader_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@shader_node_group
def create_steel_material_group():
    group_name = "SteelMaterial"
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
    principled_b_s_d_f.location = (1060.0, 100.0)
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
    # Thin Film IOR
    principled_b_s_d_f.inputs[30].default_value = 1.3300000429153442
    # Links for principled_b_s_d_f

    material_output = nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.label = ""
    material_output.location = (1420.0, 100.0)
    material_output.bl_label = "Material Output"
    material_output.is_active_output = True
    material_output.target = "ALL"
    # Displacement
    material_output.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Thickness
    material_output.inputs[3].default_value = 0.0
    # Links for material_output
    links.new(principled_b_s_d_f.outputs[0], material_output.inputs[0])

    geometry = nodes.new("ShaderNodeNewGeometry")
    geometry.name = "Geometry"
    geometry.label = ""
    geometry.location = (-1540.0, -160.0)
    geometry.bl_label = "Geometry"
    # Links for geometry

    ambient_occlusion = nodes.new("ShaderNodeAmbientOcclusion")
    ambient_occlusion.name = "Ambient Occlusion"
    ambient_occlusion.label = ""
    ambient_occlusion.location = (-1240.0, 80.0)
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
    math.location = (-1060.0, 80.0)
    math.bl_label = "Math"
    math.operation = "SUBTRACT"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(ambient_occlusion.outputs[1], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-880.0, 80.0)
    math_001.bl_label = "Math"
    math_001.operation = "POWER"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 5.0
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math.outputs[0], math_001.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (-1380.0, -160.0)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "3D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = True
    # W
    noise_texture.inputs[1].default_value = 0.0
    # Scale
    noise_texture.inputs[2].default_value = 30.0
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
    noise_texture.inputs[8].default_value = 0.23999999463558197
    # Links for noise_texture
    links.new(geometry.outputs[0], noise_texture.inputs[0])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (-1220.0, -160.0)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    # From Min
    map_range.inputs[1].default_value = 0.29999998211860657
    # From Max
    map_range.inputs[2].default_value = 0.6999999284744263
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 0.12999999523162842
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
    links.new(map_range.outputs[0], math.inputs[1])

    noise_texture_001 = nodes.new("ShaderNodeTexNoise")
    noise_texture_001.name = "Noise Texture.001"
    noise_texture_001.label = ""
    noise_texture_001.location = (-1020.0, -160.0)
    noise_texture_001.bl_label = "Noise Texture"
    noise_texture_001.noise_dimensions = "3D"
    noise_texture_001.noise_type = "FBM"
    noise_texture_001.normalize = True
    # W
    noise_texture_001.inputs[1].default_value = 0.0
    # Scale
    noise_texture_001.inputs[2].default_value = 300.0
    # Detail
    noise_texture_001.inputs[3].default_value = 14.999999046325684
    # Roughness
    noise_texture_001.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture_001.inputs[5].default_value = 2.0
    # Offset
    noise_texture_001.inputs[6].default_value = 0.0
    # Gain
    noise_texture_001.inputs[7].default_value = 1.0
    # Distortion
    noise_texture_001.inputs[8].default_value = 3.0
    # Links for noise_texture_001
    links.new(geometry.outputs[0], noise_texture_001.inputs[0])

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.label = ""
    map_range_001.location = (-860.0, -160.0)
    map_range_001.bl_label = "Map Range"
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT"
    # From Min
    map_range_001.inputs[1].default_value = 0.6499999761581421
    # From Max
    map_range_001.inputs[2].default_value = 0.6999999284744263
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
    links.new(noise_texture_001.outputs[0], map_range_001.inputs[0])

    noise_texture_002 = nodes.new("ShaderNodeTexNoise")
    noise_texture_002.name = "Noise Texture.002"
    noise_texture_002.label = ""
    noise_texture_002.location = (-1020.0, -460.0)
    noise_texture_002.bl_label = "Noise Texture"
    noise_texture_002.noise_dimensions = "3D"
    noise_texture_002.noise_type = "FBM"
    noise_texture_002.normalize = True
    # W
    noise_texture_002.inputs[1].default_value = 0.0
    # Scale
    noise_texture_002.inputs[2].default_value = 30.0
    # Detail
    noise_texture_002.inputs[3].default_value = 14.999999046325684
    # Roughness
    noise_texture_002.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture_002.inputs[5].default_value = 2.0
    # Offset
    noise_texture_002.inputs[6].default_value = 0.0
    # Gain
    noise_texture_002.inputs[7].default_value = 1.0
    # Distortion
    noise_texture_002.inputs[8].default_value = 1.0
    # Links for noise_texture_002

    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.name = "Map Range.002"
    map_range_002.label = ""
    map_range_002.location = (-860.0, -460.0)
    map_range_002.bl_label = "Map Range"
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    # From Min
    map_range_002.inputs[1].default_value = 0.3699999153614044
    # From Max
    map_range_002.inputs[2].default_value = 0.5699999928474426
    # To Min
    map_range_002.inputs[3].default_value = 164.0
    # To Max
    map_range_002.inputs[4].default_value = 180.0
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
    links.new(noise_texture_002.outputs[0], map_range_002.inputs[0])
    links.new(map_range_002.outputs[0], principled_b_s_d_f.inputs[29])

    mix = nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.label = ""
    mix.location = (40.0, 340.0)
    mix.bl_label = "Mix"
    mix.data_type = "RGBA"
    mix.factor_mode = "UNIFORM"
    mix.blend_type = "MIX"
    mix.clamp_factor = True
    mix.clamp_result = False
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
    mix.inputs[6].default_value = [0.03511274233460426, 0.03511274233460426, 0.03511274233460426, 1.0]
    # B
    mix.inputs[7].default_value = [0.10428895056247711, 0.10428895056247711, 0.10428895056247711, 1.0]
    # A
    mix.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix
    links.new(mix.outputs[2], principled_b_s_d_f.inputs[0])

    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.label = ""
    mix_001.location = (40.0, 80.0)
    mix_001.bl_label = "Mix"
    mix_001.data_type = "FLOAT"
    mix_001.factor_mode = "UNIFORM"
    mix_001.blend_type = "MIX"
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    # Factor
    mix_001.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_001.inputs[2].default_value = 0.800000011920929
    # B
    mix_001.inputs[3].default_value = 1.0
    # A
    mix_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_001.inputs[6].default_value = [0.07641182839870453, 0.07641182839870453, 0.07641182839870453, 1.0]
    # B
    mix_001.inputs[7].default_value = [0.13734933733940125, 0.13734933733940125, 0.13734933733940125, 1.0]
    # A
    mix_001.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_001.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_001
    links.new(mix_001.outputs[0], principled_b_s_d_f.inputs[1])

    mix_002 = nodes.new("ShaderNodeMix")
    mix_002.name = "Mix.002"
    mix_002.label = ""
    mix_002.location = (40.0, 20.0)
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
    mix_002.inputs[3].default_value = 0.10000002384185791
    # A
    mix_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_002.inputs[6].default_value = [0.07641182839870453, 0.07641182839870453, 0.07641182839870453, 1.0]
    # B
    mix_002.inputs[7].default_value = [0.13734933733940125, 0.13734933733940125, 0.13734933733940125, 1.0]
    # A
    mix_002.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_002.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_002
    links.new(mix_002.outputs[0], principled_b_s_d_f.inputs[2])

    bump = nodes.new("ShaderNodeBump")
    bump.name = "Bump"
    bump.label = ""
    bump.location = (-100.0, -200.0)
    bump.bl_label = "Bump"
    bump.invert = True
    # Strength
    bump.inputs[0].default_value = 1.0
    # Distance
    bump.inputs[1].default_value = 0.0010000000474974513
    # Filter Width
    bump.inputs[2].default_value = 5.999999523162842
    # Normal
    bump.inputs[4].default_value = [0.0, 0.0, 0.0]
    # Links for bump
    links.new(map_range_001.outputs[0], bump.inputs[3])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (-1260.0, -480.0)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "MULTIPLY"
    # Vector
    vector_math.inputs[1].default_value = [1.0, 1.0, 0.30000001192092896]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(vector_math.outputs[0], noise_texture_002.inputs[0])
    links.new(geometry.outputs[0], vector_math.inputs[0])

    voronoi_texture = nodes.new("ShaderNodeTexVoronoi")
    voronoi_texture.name = "Voronoi Texture"
    voronoi_texture.label = ""
    voronoi_texture.location = (-2240.0, 320.0)
    voronoi_texture.bl_label = "Voronoi Texture"
    voronoi_texture.voronoi_dimensions = "4D"
    voronoi_texture.distance = "EUCLIDEAN"
    voronoi_texture.feature = "DISTANCE_TO_EDGE"
    voronoi_texture.normalize = False
    # W
    voronoi_texture.inputs[1].default_value = 0.8199999928474426
    # Scale
    voronoi_texture.inputs[2].default_value = 5.0
    # Detail
    voronoi_texture.inputs[3].default_value = 0.0
    # Roughness
    voronoi_texture.inputs[4].default_value = 0.5
    # Lacunarity
    voronoi_texture.inputs[5].default_value = 2.0
    # Smoothness
    voronoi_texture.inputs[6].default_value = 1.0
    # Exponent
    voronoi_texture.inputs[7].default_value = 0.5
    # Randomness
    voronoi_texture.inputs[8].default_value = 1.0
    # Links for voronoi_texture

    geometry_001 = nodes.new("ShaderNodeNewGeometry")
    geometry_001.name = "Geometry.001"
    geometry_001.label = ""
    geometry_001.location = (-2560.0, 180.0)
    geometry_001.bl_label = "Geometry"
    # Links for geometry_001

    noise_texture_003 = nodes.new("ShaderNodeTexNoise")
    noise_texture_003.name = "Noise Texture.003"
    noise_texture_003.label = ""
    noise_texture_003.location = (-2560.0, 100.0)
    noise_texture_003.bl_label = "Noise Texture"
    noise_texture_003.noise_dimensions = "4D"
    noise_texture_003.noise_type = "FBM"
    noise_texture_003.normalize = True
    # W
    noise_texture_003.inputs[1].default_value = 5.369999885559082
    # Scale
    noise_texture_003.inputs[2].default_value = 5.509999752044678
    # Detail
    noise_texture_003.inputs[3].default_value = 3.1999998092651367
    # Roughness
    noise_texture_003.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture_003.inputs[5].default_value = 2.0
    # Offset
    noise_texture_003.inputs[6].default_value = 0.0
    # Gain
    noise_texture_003.inputs[7].default_value = 1.0
    # Distortion
    noise_texture_003.inputs[8].default_value = 0.23999999463558197
    # Links for noise_texture_003
    links.new(geometry_001.outputs[0], noise_texture_003.inputs[0])

    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.name = "Mix.003"
    mix_003.label = ""
    mix_003.location = (-2400.0, 320.0)
    mix_003.bl_label = "Mix"
    mix_003.data_type = "RGBA"
    mix_003.factor_mode = "UNIFORM"
    mix_003.blend_type = "LINEAR_LIGHT"
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    # Factor
    mix_003.inputs[0].default_value = 0.1077347993850708
    # Factor
    mix_003.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_003.inputs[2].default_value = 0.0
    # B
    mix_003.inputs[3].default_value = 0.0
    # A
    mix_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_003.inputs[8].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # B
    mix_003.inputs[9].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for mix_003
    links.new(mix_003.outputs[2], voronoi_texture.inputs[0])
    links.new(geometry_001.outputs[0], mix_003.inputs[6])
    links.new(noise_texture_003.outputs[1], mix_003.inputs[7])

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (-2400.0, 20.0)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(noise_texture_003.outputs[1], separate_x_y_z.inputs[0])

    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.name = "Map Range.003"
    map_range_003.label = ""
    map_range_003.location = (-2240.0, 20.0)
    map_range_003.bl_label = "Map Range"
    map_range_003.clamp = True
    map_range_003.interpolation_type = "LINEAR"
    map_range_003.data_type = "FLOAT"
    # From Min
    map_range_003.inputs[1].default_value = 0.47999998927116394
    # From Max
    map_range_003.inputs[2].default_value = 0.5799999237060547
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
    links.new(separate_x_y_z.outputs[1], map_range_003.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (-1900.0, 320.0)
    math_002.bl_label = "Math"
    math_002.operation = "MAXIMUM"
    math_002.use_clamp = True
    # Value
    math_002.inputs[2].default_value = 0.09000001102685928
    # Links for math_002
    links.new(map_range_003.outputs[0], math_002.inputs[1])

    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.name = "Map Range.004"
    map_range_004.label = ""
    map_range_004.location = (-2060.0, 320.0)
    map_range_004.bl_label = "Map Range"
    map_range_004.clamp = True
    map_range_004.interpolation_type = "LINEAR"
    map_range_004.data_type = "FLOAT"
    # From Min
    map_range_004.inputs[1].default_value = 0.0
    # From Max
    map_range_004.inputs[2].default_value = 0.11000001430511475
    # To Min
    map_range_004.inputs[3].default_value = 0.0
    # To Max
    map_range_004.inputs[4].default_value = 1.0
    # Steps
    map_range_004.inputs[5].default_value = 4.0
    # Vector
    map_range_004.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_004.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_004.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_004.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_004.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_004.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_004
    links.new(voronoi_texture.outputs[0], map_range_004.inputs[0])
    links.new(map_range_004.outputs[0], math_002.inputs[0])

    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.name = "Map Range.005"
    map_range_005.label = ""
    map_range_005.location = (-1740.0, 320.0)
    map_range_005.bl_label = "Map Range"
    map_range_005.clamp = True
    map_range_005.interpolation_type = "LINEAR"
    map_range_005.data_type = "FLOAT"
    # From Min
    map_range_005.inputs[1].default_value = 0.0010000000474974513
    # From Max
    map_range_005.inputs[2].default_value = 0.0020000000949949026
    # To Min
    map_range_005.inputs[3].default_value = 0.0
    # To Max
    map_range_005.inputs[4].default_value = 1.0
    # Steps
    map_range_005.inputs[5].default_value = 4.0
    # Vector
    map_range_005.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_005.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_005.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_005.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_005.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_005.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_005
    links.new(math_002.outputs[0], map_range_005.inputs[0])

    bump_001 = nodes.new("ShaderNodeBump")
    bump_001.name = "Bump.001"
    bump_001.label = ""
    bump_001.location = (460.0, -140.0)
    bump_001.bl_label = "Bump"
    bump_001.invert = False
    # Strength
    bump_001.inputs[0].default_value = 1.0
    # Distance
    bump_001.inputs[1].default_value = 0.004999999888241291
    # Filter Width
    bump_001.inputs[2].default_value = 5.999999523162842
    # Links for bump_001
    links.new(bump_001.outputs[0], principled_b_s_d_f.inputs[5])
    links.new(bump.outputs[0], bump_001.inputs[4])
    links.new(map_range_005.outputs[0], bump_001.inputs[3])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (-700.0, 300.0)
    math_003.bl_label = "Math"
    math_003.operation = "MULTIPLY"
    math_003.use_clamp = False
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_001.outputs[0], math_003.inputs[0])
    links.new(map_range_005.outputs[0], math_003.inputs[1])

    geometry_002 = nodes.new("ShaderNodeNewGeometry")
    geometry_002.name = "Geometry.002"
    geometry_002.label = ""
    geometry_002.location = (30.0, -310.0)
    geometry_002.bl_label = "Geometry"
    # Links for geometry_002

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (190.0, -310.0)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "DOT_PRODUCT"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, -0.25, 1.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(geometry_002.outputs[1], vector_math_001.inputs[0])

    map_range_006 = nodes.new("ShaderNodeMapRange")
    map_range_006.name = "Map Range.006"
    map_range_006.label = ""
    map_range_006.location = (350.0, -310.0)
    map_range_006.bl_label = "Map Range"
    map_range_006.clamp = True
    map_range_006.interpolation_type = "LINEAR"
    map_range_006.data_type = "FLOAT"
    # From Min
    map_range_006.inputs[1].default_value = 0.29999998211860657
    # From Max
    map_range_006.inputs[2].default_value = 0.5200000405311584
    # To Min
    map_range_006.inputs[3].default_value = 0.0
    # To Max
    map_range_006.inputs[4].default_value = 1.0
    # Steps
    map_range_006.inputs[5].default_value = 4.0
    # Vector
    map_range_006.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_006.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_006.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_006.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_006.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_006.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_006
    links.new(vector_math_001.outputs[1], map_range_006.inputs[0])

    noise_texture_004 = nodes.new("ShaderNodeTexNoise")
    noise_texture_004.name = "Noise Texture.004"
    noise_texture_004.label = ""
    noise_texture_004.location = (510.0, -30.0)
    noise_texture_004.bl_label = "Noise Texture"
    noise_texture_004.noise_dimensions = "3D"
    noise_texture_004.noise_type = "FBM"
    noise_texture_004.normalize = True
    # Vector
    noise_texture_004.inputs[0].default_value = [0.0, 0.0, 0.0]
    # W
    noise_texture_004.inputs[1].default_value = 0.0
    # Scale
    noise_texture_004.inputs[2].default_value = 1500.0
    # Detail
    noise_texture_004.inputs[3].default_value = 7.0
    # Roughness
    noise_texture_004.inputs[4].default_value = 1.0
    # Lacunarity
    noise_texture_004.inputs[5].default_value = 2.0
    # Offset
    noise_texture_004.inputs[6].default_value = 0.0
    # Gain
    noise_texture_004.inputs[7].default_value = 1.0
    # Distortion
    noise_texture_004.inputs[8].default_value = 0.0
    # Links for noise_texture_004

    map_range_007 = nodes.new("ShaderNodeMapRange")
    map_range_007.name = "Map Range.007"
    map_range_007.label = ""
    map_range_007.location = (870.0, -50.0)
    map_range_007.bl_label = "Map Range"
    map_range_007.clamp = True
    map_range_007.interpolation_type = "LINEAR"
    map_range_007.data_type = "FLOAT"
    # From Min
    map_range_007.inputs[1].default_value = 0.30000001192092896
    # From Max
    map_range_007.inputs[2].default_value = 0.3499999940395355
    # To Min
    map_range_007.inputs[3].default_value = 0.0
    # To Max
    map_range_007.inputs[4].default_value = 1.0
    # Steps
    map_range_007.inputs[5].default_value = 4.0
    # Vector
    map_range_007.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_007.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_007.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_007.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_007.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_007.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_007

    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.name = "Mix.004"
    mix_004.label = ""
    mix_004.location = (510.0, -310.0)
    mix_004.bl_label = "Mix"
    mix_004.data_type = "FLOAT"
    mix_004.factor_mode = "UNIFORM"
    mix_004.blend_type = "MIX"
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    # Factor
    mix_004.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_004.inputs[2].default_value = 0.14999999105930328
    # B
    mix_004.inputs[3].default_value = -0.09999999403953552
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
    links.new(map_range_006.outputs[0], mix_004.inputs[0])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (690.0, -50.0)
    math_004.bl_label = "Math"
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(math_004.outputs[0], map_range_007.inputs[0])
    links.new(noise_texture_004.outputs[0], math_004.inputs[0])
    links.new(mix_004.outputs[0], math_004.inputs[1])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = ""
    frame.location = (-1350.0, -770.0)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (-143.23765563964844, 129.0784149169922)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketFloat"
    # Links for reroute
    links.new(reroute.outputs[0], mix.inputs[0])
    links.new(reroute.outputs[0], mix_001.inputs[0])
    links.new(reroute.outputs[0], mix_002.inputs[0])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (-480.0, 260.0)
    math_006.bl_label = "Math"
    math_006.operation = "MULTIPLY"
    math_006.use_clamp = False
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(math_006.outputs[0], reroute.inputs[0])
    links.new(math_003.outputs[0], math_006.inputs[0])
    links.new(map_range_007.outputs[0], math_006.inputs[1])

    a_o_v_output = nodes.new("ShaderNodeOutputAOV")
    a_o_v_output.name = "AOV Output"
    a_o_v_output.label = ""
    a_o_v_output.location = (1420.0, -60.0)
    a_o_v_output.bl_label = "AOV Output"
    a_o_v_output.aov_name = "steel"
    # Color
    a_o_v_output.inputs[0].default_value = [0.0, 0.0, 0.0, 1.0]
    # Value
    a_o_v_output.inputs[1].default_value = 1.0
    # Links for a_o_v_output

    auto_layout_nodes(group)
    return group