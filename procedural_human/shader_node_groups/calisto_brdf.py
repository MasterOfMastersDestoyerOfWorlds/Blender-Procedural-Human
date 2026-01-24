import bpy
from procedural_human.decorators.shader_node_decorator import shader_node_group
from procedural_human.shader_node_groups.shader_helpers import (
    link_or_set, create_node, math_op, mix_color, mix_shader, add_shader
)
from procedural_human.utils.node_layout import auto_layout_nodes

@shader_node_group
def create_calisto_brdf_group():
    """Calisto BRDF shader for photorealistic skin rendering.

    Implements the production-grade shader model from "The Callisto Protocol"
    as documented in Jimenez's GDC 2023 presentation, featuring:
    
    1. Subsurface Scattering (Random Walk) - replaces Lambertian diffuse
    2. Translucent BSDF - for thin geometry transmission (ears, nostrils)
    3. Sheen BSDF - for retroreflection/peach fuzz
    4. Dual Specular Lobe - skin + oil layers with proper Fresnel layering
    5. Explicit artistic controls over physical correctness

    Note: For optimal results, set the object's Shadow Terminator Offset
    to 0.1-0.15 in Object Properties > Shading.
    """
    group_name = "CalistoBRDF"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")
    interface = group.interface
    
    interface.new_socket(name="Base Color", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.8, 0.6, 0.5, 1.0)
    interface.new_socket(name="Roughness", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.4
    interface.new_socket(name="Normal", in_out="INPUT", socket_type="NodeSocketVector")
    
    interface.new_socket(name="Subsurface Radius", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.4, 0.15, 0.1)
    interface.new_socket(name="Subsurface Scale", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.01
    
    interface.new_socket(name="Diffuse Fresnel Intensity", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.4
    interface.new_socket(name="Diffuse Fresnel Tint", in_out="INPUT", socket_type="NodeSocketColor").default_value = (1.0, 0.94, 0.94, 1.0)
    
    interface.new_socket(name="Thickness", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.0
    interface.new_socket(name="Transmission Weight", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.3
    interface.new_socket(name="Transmission Tint", in_out="INPUT", socket_type="NodeSocketColor").default_value = (1.0, 0.2, 0.1, 1.0)
    
    interface.new_socket(name="Retroreflection Intensity", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.15
    interface.new_socket(name="Retroreflection Roughness", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.8
    
    interface.new_socket(name="Coat Roughness Scale", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.5
    interface.new_socket(name="Coat Intensity", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.3
    
    interface.new_socket(name="BSDF", in_out="OUTPUT", socket_type="NodeSocketShader")
    
    nodes = group.nodes
    input_node = nodes.new("NodeGroupInput")
    output_node = nodes.new("NodeGroupOutput")
    
    base_color = input_node.outputs["Base Color"]
    roughness = input_node.outputs["Roughness"] 
    normal = input_node.outputs["Normal"]
    
    subsurface_radius = input_node.outputs["Subsurface Radius"]
    subsurface_scale = input_node.outputs["Subsurface Scale"]
    
    diff_fresnel_int = input_node.outputs["Diffuse Fresnel Intensity"]
    diff_fresnel_tint = input_node.outputs["Diffuse Fresnel Tint"]
    
    thickness = input_node.outputs["Thickness"]
    transmission_weight = input_node.outputs["Transmission Weight"]
    transmission_tint = input_node.outputs["Transmission Tint"]
    
    retro_int = input_node.outputs["Retroreflection Intensity"]
    retro_rough = input_node.outputs["Retroreflection Roughness"]
    
    coat_scale = input_node.outputs["Coat Roughness Scale"]
    coat_int = input_node.outputs["Coat Intensity"]
    
    layer_weight = create_node(group, "ShaderNodeLayerWeight", {"Blend": 0.5})
    link_or_set(group, layer_weight.inputs["Normal"], normal)
    facing = layer_weight.outputs["Facing"]
    
    edge_mod_color = mix_color(group, "MULTIPLY", 1.0, diff_fresnel_tint, diff_fresnel_int)
    color_modulator = mix_color(group, "MIX", facing, (1.0, 1.0, 1.0, 1.0), edge_mod_color)
    final_sss_color = mix_color(group, "MULTIPLY", 1.0, base_color, color_modulator)
    
    sss_bsdf = create_node(group, "ShaderNodeSubsurfaceScattering")
    sss_bsdf.falloff = 'RANDOM_WALK'
    link_or_set(group, sss_bsdf.inputs["Color"], final_sss_color)
    link_or_set(group, sss_bsdf.inputs["Radius"], subsurface_radius)
    link_or_set(group, sss_bsdf.inputs["Scale"], subsurface_scale)
    link_or_set(group, sss_bsdf.inputs["Normal"], normal)
    
    translucent_color = mix_color(group, "MULTIPLY", 1.0, base_color, transmission_tint)
    
    translucent_bsdf = create_node(group, "ShaderNodeBsdfTranslucent")
    link_or_set(group, translucent_bsdf.inputs["Color"], translucent_color)
    link_or_set(group, translucent_bsdf.inputs["Normal"], normal)
    
    inv_thickness = math_op(group, "SUBTRACT", 1.0, thickness)
    transmission_factor = math_op(group, "MULTIPLY", inv_thickness, transmission_weight)
    sss_plus_trans = mix_shader(group, transmission_factor, sss_bsdf.outputs[0], translucent_bsdf.outputs[0])
    
    sheen_bsdf = create_node(group, "ShaderNodeBsdfSheen")
    sheen_bsdf.distribution = 'MICROFIBER'
    retro_color = mix_color(group, "MULTIPLY", 1.0, base_color, retro_int)
    link_or_set(group, sheen_bsdf.inputs["Color"], retro_color)
    link_or_set(group, sheen_bsdf.inputs["Roughness"], retro_rough)
    link_or_set(group, sheen_bsdf.inputs["Normal"], normal)
    
    base_plus_retro = add_shader(group, sss_plus_trans, sheen_bsdf.outputs[0])
    
    spec_base = create_node(group, "ShaderNodeBsdfGlossy")
    link_or_set(group, spec_base.inputs["Roughness"], roughness)
    link_or_set(group, spec_base.inputs["Normal"], normal)
    
    spec_coat = create_node(group, "ShaderNodeBsdfGlossy")
    coat_roughness = math_op(group, "MULTIPLY", roughness, coat_scale)
    link_or_set(group, spec_coat.inputs["Roughness"], coat_roughness)
    link_or_set(group, spec_coat.inputs["Normal"], normal)
    
    coat_fresnel = create_node(group, "ShaderNodeFresnel")
    coat_fresnel.inputs["IOR"].default_value = 1.4
    link_or_set(group, coat_fresnel.inputs["Normal"], normal)
    
    coat_factor = math_op(group, "MULTIPLY", coat_fresnel.outputs["Fac"], coat_int)
    dual_specular = mix_shader(group, coat_factor, spec_base.outputs[0], spec_coat.outputs[0])
    
    fresnel_mix = create_node(group, "ShaderNodeFresnel")
    fresnel_mix.inputs["IOR"].default_value = 1.45
    link_or_set(group, fresnel_mix.inputs["Normal"], normal)
    
    final_shader = mix_shader(group, fresnel_mix.outputs["Fac"], base_plus_retro, dual_specular)
    
    link_or_set(group, output_node.inputs["BSDF"], final_shader)
    auto_layout_nodes(group)
    return group
