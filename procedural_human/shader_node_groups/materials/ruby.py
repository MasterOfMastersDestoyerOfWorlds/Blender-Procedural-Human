import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.shader_node_decorator import shader_node_group


@shader_node_group
def create_ruby_material_group():
    group_name = "RubyMaterial"
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

    glass_b_s_d_f = nodes.new("ShaderNodeBsdfGlass")
    glass_b_s_d_f.name = "Glass BSDF"
    glass_b_s_d_f.label = ""
    glass_b_s_d_f.location = (-180.0, 100.0)
    glass_b_s_d_f.bl_label = "Glass BSDF"
    glass_b_s_d_f.distribution = "MULTI_GGX"
    # Color
    glass_b_s_d_f.inputs[0].default_value = [0.7221790552139282, 0.009354429319500923, 0.009354429319500923, 1.0]
    # Roughness
    glass_b_s_d_f.inputs[1].default_value = 0.10000000149011612
    # IOR
    glass_b_s_d_f.inputs[2].default_value = 1.5
    # Normal
    glass_b_s_d_f.inputs[3].default_value = [0.0, 0.0, 0.0]
    # Weight
    glass_b_s_d_f.inputs[4].default_value = 0.0
    # Thin Film Thickness
    glass_b_s_d_f.inputs[5].default_value = 0.0
    # Thin Film IOR
    glass_b_s_d_f.inputs[6].default_value = 1.3300000429153442
    # Links for glass_b_s_d_f
    links.new(glass_b_s_d_f.outputs[0], material_output.inputs[0])

    a_o_v_output = nodes.new("ShaderNodeOutputAOV")
    a_o_v_output.name = "AOV Output"
    a_o_v_output.label = ""
    a_o_v_output.location = (200.0, -60.0)
    a_o_v_output.bl_label = "AOV Output"
    a_o_v_output.aov_name = "gem"
    # Color
    a_o_v_output.inputs[0].default_value = [0.0, 0.0, 0.0, 1.0]
    # Value
    a_o_v_output.inputs[1].default_value = 1.0
    # Links for a_o_v_output

    auto_layout_nodes(group)
    return group