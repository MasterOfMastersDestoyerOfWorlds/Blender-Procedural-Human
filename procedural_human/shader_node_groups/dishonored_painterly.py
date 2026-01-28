import bpy
from procedural_human.decorators.shader_node_decorator import shader_node_group
from procedural_human.shader_node_groups.shader_helpers import (
    link_or_set, create_node, math_op, vec_math_op, mix_color, mix_shader
)
from procedural_human.utils.node_layout import auto_layout_nodes

@shader_node_group
def create_dishonored_painterly_group():
    group_name = "DishonoredPainterly" 
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]
    
    group = bpy.data.node_groups.new(group_name, "ShaderNodeTree")
    interface = group.interface
    
    # --- INPUTS ---
    interface.new_socket(name="Base Color", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.1, 0.4, 0.5, 1.0)
    interface.new_socket(name="Shadow Color", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.05, 0.1, 0.2, 1.0)
    interface.new_socket(name="Highlight Color", in_out="INPUT", socket_type="NodeSocketColor").default_value = (0.9, 0.8, 0.6, 1.0)
    
    # New Input: Fixed Light Direction (Controls where the "paint" sits)
    interface.new_socket(name="Light Direction", in_out="INPUT", socket_type="NodeSocketVector").default_value = (0.5, 0.5, 1.0)
    
    interface.new_socket(name="Brush Scale", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 50.0
    interface.new_socket(name="Distortion Strength", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.5
    interface.new_socket(name="Edge Threshold", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 0.4
    interface.new_socket(name="Vector Snap", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 5.0
    
    # New Input: Geometry Wear (Controls how much the mesh shape affects the paint)
    interface.new_socket(name="Geometry Wear", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    
    interface.new_socket(name="Normal", in_out="INPUT", socket_type="NodeSocketVector")
    interface.new_socket(name="BSDF", in_out="OUTPUT", socket_type="NodeSocketShader")
    
    nodes = group.nodes
    input_node = nodes.new("NodeGroupInput")
    output_node = nodes.new("NodeGroupOutput")
    
    # Unpack Inputs
    base_color = input_node.outputs["Base Color"]
    shadow_color = input_node.outputs["Shadow Color"]
    highlight_color = input_node.outputs["Highlight Color"]
    light_dir = input_node.outputs["Light Direction"]
    brush_scale = input_node.outputs["Brush Scale"]
    distortion_str = input_node.outputs["Distortion Strength"]
    edge_thresh = input_node.outputs["Edge Threshold"]
    vec_snap = input_node.outputs["Vector Snap"]
    geo_wear = input_node.outputs["Geometry Wear"]
    input_normal = input_node.outputs["Normal"]
    
    geometry_node = create_node(group, "ShaderNodeNewGeometry")
    
    # --- PHASE 0: Coordinate Jitter (Unchanged) ---
    tex_coord = create_node(group, "ShaderNodeTexCoord")
    object_coords = tex_coord.outputs["Object"]
    
    jitter_noise = create_node(group, "ShaderNodeTexNoise")
    jitter_noise.noise_dimensions = '3D'
    link_or_set(group, jitter_noise.inputs["Vector"], object_coords)
    link_or_set(group, jitter_noise.inputs["Scale"], 2.0)
    
    jittered_coords = mix_color(group, "MIX", 0.02, object_coords, jitter_noise.outputs["Color"])
    
    # --- PHASE 1: Planar Core (Fixed: Lighting Vector) ---
    
    # 1. Snap Normal Logic (Existing logic preserved)
    div_node = create_node(group, "ShaderNodeMath")
    div_node.operation = 'DIVIDE'
    link_or_set(group, div_node.inputs[0], 1.0)
    link_or_set(group, div_node.inputs[1], vec_snap)
    snap_increment = div_node.outputs[0]
    
    world_to_obj = create_node(group, "ShaderNodeVectorTransform")
    world_to_obj.vector_type = 'NORMAL'
    world_to_obj.convert_from = 'WORLD'
    world_to_obj.convert_to = 'OBJECT'
    link_or_set(group, world_to_obj.inputs["Vector"], input_normal)
    
    vec_snap_node = create_node(group, "ShaderNodeVectorMath")
    vec_snap_node.operation = 'SNAP'
    link_or_set(group, vec_snap_node.inputs[0], world_to_obj.outputs["Vector"])
    link_or_set(group, vec_snap_node.inputs[1], snap_increment)
    
    obj_to_world = create_node(group, "ShaderNodeVectorTransform")
    obj_to_world.vector_type = 'NORMAL'
    obj_to_world.convert_from = 'OBJECT'
    obj_to_world.convert_to = 'WORLD'
    link_or_set(group, obj_to_world.inputs["Vector"], vec_snap_node.outputs["Vector"])
    snapped_normal_world = obj_to_world.outputs["Vector"]
    
    # 2. Replaced Layer Weight with DOT PRODUCT (Normal . Light Direction)
    dot_product = vec_math_op(group, "DOT_PRODUCT", snapped_normal_world, light_dir)
    
    # Map range from -1..1 to 0..1
    add_one = math_op(group, "ADD", dot_product, 1.0)
    lighting_factor = math_op(group, "DIVIDE", add_one, 2.0)
    
    # --- PHASE 1.5: Geometry Wear (Pointiness) ---
    pointiness = geometry_node.outputs["Pointiness"]
    
    # Contrast stretch the pointiness
    ramp = create_node(group, "ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = 'LINEAR'
    ramp.color_ramp.elements[0].position = 0.45
    ramp.color_ramp.elements[1].position = 0.55
    link_or_set(group, ramp.inputs["Fac"], pointiness)
    
    # FIXED: Use "Color" output instead of "Fac"
    wear_mask = ramp.outputs["Color"]
    
    # Mix the Lighting Factor with the Wear Mask
    modified_lighting = mix_color(group, "OVERLAY", geo_wear, lighting_factor, wear_mask)

    # --- Color Logic ---
    is_mid_or_high = math_op(group, "GREATER_THAN", modified_lighting, 0.4)
    is_high = math_op(group, "GREATER_THAN", modified_lighting, 0.65)
    
    mix_dark_mid = mix_color(group, "MIX", is_mid_or_high, shadow_color, base_color)
    planar_color = mix_color(group, "MIX", is_high, mix_dark_mid, highlight_color)
    
    planar_bsdf_node = create_node(group, "ShaderNodeBsdfDiffuse")
    link_or_set(group, planar_bsdf_node.inputs["Color"], planar_color)
    planar_bsdf = planar_bsdf_node.outputs["BSDF"]
    
    # --- PHASE 2: Distortion Engine (Brush Strokes) ---
    mapping = create_node(group, "ShaderNodeMapping")
    link_or_set(group, mapping.inputs["Vector"], object_coords)
    link_or_set(group, mapping.inputs["Scale"], (1.0, 0.05, 1.0))
    
    brush_noise = create_node(group, "ShaderNodeTexNoise")
    link_or_set(group, brush_noise.inputs["Vector"], mapping.outputs["Vector"])
    link_or_set(group, brush_noise.inputs["Scale"], brush_scale)
    link_or_set(group, brush_noise.inputs["Detail"], 10.0)
    noise_fac = brush_noise.outputs["Fac"]
    
    distorted_lighting = mix_color(group, "LINEAR_LIGHT", distortion_str, modified_lighting, noise_fac)
    
    edge_mask = math_op(group, "LESS_THAN", distorted_lighting, edge_thresh)
    
    # --- PHASE 3: Integration ---
    ink_bsdf_node = create_node(group, "ShaderNodeBsdfDiffuse")
    link_or_set(group, ink_bsdf_node.inputs["Color"], (0.05, 0.05, 0.05, 1.0))
    ink_bsdf = ink_bsdf_node.outputs["BSDF"]
    
    final_shader = mix_shader(group, edge_mask, planar_bsdf, ink_bsdf)
    
    link_or_set(group, output_node.inputs["BSDF"], final_shader)
    
    auto_layout_nodes(group) 
    return group 