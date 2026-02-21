import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.shader_node_decorator import shader_node_group


@shader_node_group
def create_fabric_material_group():
    group_name = "FabricMaterial"
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
    material_output.location = (200.0, 100.0)
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
    principled_b_s_d_f.location = (-200.0, 120.0)
    principled_b_s_d_f.bl_label = "Principled BSDF"
    principled_b_s_d_f.distribution = "MULTI_GGX"
    principled_b_s_d_f.subsurface_method = "RANDOM_WALK"
    # Base Color
    principled_b_s_d_f.inputs[0].default_value = [0.08027029037475586, 0.0009848610498011112, 0.010410563088953495, 1.0]
    # Metallic
    principled_b_s_d_f.inputs[1].default_value = 0.0
    # Roughness
    principled_b_s_d_f.inputs[2].default_value = 1.0
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
    principled_b_s_d_f.inputs[13].default_value = 0.7145015001296997
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

    voronoi_texture = nodes.new("ShaderNodeTexVoronoi")
    voronoi_texture.name = "Voronoi Texture"
    voronoi_texture.label = ""
    voronoi_texture.location = (-620.0, 80.0)
    voronoi_texture.bl_label = "Voronoi Texture"
    voronoi_texture.voronoi_dimensions = "3D"
    voronoi_texture.distance = "EUCLIDEAN"
    voronoi_texture.feature = "F1"
    voronoi_texture.normalize = False
    # W
    voronoi_texture.inputs[1].default_value = 0.0
    # Scale
    voronoi_texture.inputs[2].default_value = 500.0
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
    voronoi_texture.inputs[8].default_value = 0.0
    # Links for voronoi_texture

    geometry = nodes.new("ShaderNodeNewGeometry")
    geometry.name = "Geometry"
    geometry.label = ""
    geometry.location = (-860.0, -80.0)
    geometry.bl_label = "Geometry"
    # Links for geometry
    links.new(geometry.outputs[0], voronoi_texture.inputs[0])

    bump = nodes.new("ShaderNodeBump")
    bump.name = "Bump"
    bump.label = ""
    bump.location = (-420.0, 0.0)
    bump.bl_label = "Bump"
    bump.invert = True
    # Strength
    bump.inputs[0].default_value = 1.0
    # Distance
    bump.inputs[1].default_value = 0.0010000000474974513
    # Filter Width
    bump.inputs[2].default_value = 0.10000000149011612
    # Normal
    bump.inputs[4].default_value = [0.0, 0.0, 0.0]
    # Links for bump
    links.new(voronoi_texture.outputs[0], bump.inputs[3])
    links.new(bump.outputs[0], principled_b_s_d_f.inputs[5])

    auto_layout_nodes(group)
    return group