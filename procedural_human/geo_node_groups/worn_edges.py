"""
Worn Edges Geometry Node Group

Creates worn/chipped edge details on geometry by detecting sharp edges
and applying noise-based displacement along those edges.

Based on Edge Damage technique from temp_0.py:
    1. Apply uniform edge offset: Position + Normal * Edge Offset
    2. Subdivide and smooth with Subdivision Surface
    3. Apply noise displacement: Position + Normal * Noise * Noise Strength
    4. Boolean intersect with original mesh to clip overhangs
"""

import bpy
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group


@geo_node_group
def create_worn_edges_group():
    """Creates a Geometry Node group that applies worn/chipped details to edges.
    
    Uses two-stage displacement following the Edge Damage pattern:
    1. Uniform edge offset along normals
    2. Ridged noise for irregular chipping
    
    :returns: The Worn Edges node group.
    """
    group_name = "WornEdges"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
    
    # --- Interface ---
    group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    
    subdiv_socket = group.interface.new_socket(name="Subdivisions", in_out='INPUT', socket_type='NodeSocketInt')
    subdiv_socket.default_value = 2
    subdiv_socket.min_value = 0 
    subdiv_socket.max_value = 6 
    
    edge_offset_socket = group.interface.new_socket(name="Edge Offset", in_out='INPUT', socket_type='NodeSocketFloat')
    edge_offset_socket.default_value = 0.05
    edge_offset_socket.min_value = -1.0
    edge_offset_socket.max_value = 1.0
    
    noise_scale_socket = group.interface.new_socket(name="Noise Scale", in_out='INPUT', socket_type='NodeSocketFloat')
    noise_scale_socket.default_value = 50.0
    noise_scale_socket.min_value = 0.1
    
    noise_strength_socket = group.interface.new_socket(name="Noise Strength", in_out='INPUT', socket_type='NodeSocketFloat')
    noise_strength_socket.default_value = 0.3
    noise_strength_socket.min_value = 0.0
    
    group.interface.new_socket(name="Mesh", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new("NodeGroupInput")
    output_node = nodes.new("NodeGroupOutput")

    # ===== Stage 1: Edge Offset Displacement =====
    # Position + Normal * Edge Offset
    
    normal_1 = nodes.new("GeometryNodeInputNormal")
    position_1 = nodes.new("GeometryNodeInputPosition")
    
    # Normal * Edge Offset
    vec_mult_1 = nodes.new("ShaderNodeVectorMath")
    vec_mult_1.operation = "MULTIPLY"
    links.new(normal_1.outputs["Normal"], vec_mult_1.inputs[0])
    links.new(input_node.outputs["Edge Offset"], vec_mult_1.inputs[1])
    
    # Position + (Normal * Edge Offset)
    vec_add_1 = nodes.new("ShaderNodeVectorMath")
    vec_add_1.operation = "ADD"
    links.new(position_1.outputs["Position"], vec_add_1.inputs[0])
    links.new(vec_mult_1.outputs[0], vec_add_1.inputs[1])
    
    # Set Position (edge offset)
    set_pos_1 = nodes.new("GeometryNodeSetPosition")
    links.new(input_node.outputs["Geometry"], set_pos_1.inputs["Geometry"])
    links.new(vec_add_1.outputs[0], set_pos_1.inputs["Position"])

    # ===== Subdivide and Smooth =====
    
    # Subdivide Mesh
    subdivide = nodes.new("GeometryNodeSubdivideMesh")
    links.new(set_pos_1.outputs["Geometry"], subdivide.inputs["Mesh"])
    links.new(input_node.outputs["Subdivisions"], subdivide.inputs["Level"])
    
    # Subdivision Surface (smoothing)
    subdiv_surface = nodes.new("GeometryNodeSubdivisionSurface")
    links.new(subdivide.outputs["Mesh"], subdiv_surface.inputs["Mesh"])
    subdiv_surface.inputs["Level"].default_value = 1
    subdiv_surface.inputs["Edge Crease"].default_value = 0.0
    subdiv_surface.inputs["Vertex Crease"].default_value = 0.0

    # ===== Stage 2: Noise Displacement =====
    # Position + Normal * Noise * Noise Strength
    
    # Ridged Multifractal noise for realistic chipping
    noise = nodes.new("ShaderNodeTexNoise")
    noise.noise_dimensions = '3D'
    noise.noise_type = 'RIDGED_MULTIFRACTAL'
    noise.normalize = False
    noise.inputs["Detail"].default_value = 1.0
    noise.inputs["Roughness"].default_value = 0.25
    noise.inputs["Lacunarity"].default_value = 2.0
    noise.inputs["Offset"].default_value = 0.0
    noise.inputs["Gain"].default_value = 1.0
    noise.inputs["Distortion"].default_value = 0.0
    links.new(input_node.outputs["Noise Scale"], noise.inputs["Scale"])
    
    normal_2 = nodes.new("GeometryNodeInputNormal")
    position_2 = nodes.new("GeometryNodeInputPosition")
    
    # Normal * Noise
    vec_mult_2 = nodes.new("ShaderNodeVectorMath")
    vec_mult_2.operation = "MULTIPLY"
    links.new(normal_2.outputs["Normal"], vec_mult_2.inputs[0])
    links.new(noise.outputs["Fac"], vec_mult_2.inputs[1])
    
    # (Normal * Noise) * Noise Strength
    vec_mult_3 = nodes.new("ShaderNodeVectorMath")
    vec_mult_3.operation = "MULTIPLY"
    links.new(vec_mult_2.outputs[0], vec_mult_3.inputs[0])
    links.new(input_node.outputs["Noise Strength"], vec_mult_3.inputs[1])
    
    # Position + (Normal * Noise * Noise Strength)
    vec_add_2 = nodes.new("ShaderNodeVectorMath")
    vec_add_2.operation = "ADD"
    links.new(position_2.outputs["Position"], vec_add_2.inputs[0])
    links.new(vec_mult_3.outputs[0], vec_add_2.inputs[1])
    
    # Set Position (noise displacement)
    set_pos_2 = nodes.new("GeometryNodeSetPosition")
    links.new(subdiv_surface.outputs["Mesh"], set_pos_2.inputs["Geometry"])
    links.new(vec_add_2.outputs[0], set_pos_2.inputs["Position"])

    # ===== Boolean Intersection =====
    # Clip against original mesh to remove overhanging geometry
    
    boolean = nodes.new("GeometryNodeMeshBoolean")
    boolean.operation = 'INTERSECT'
    boolean.solver = 'EXACT'
    boolean.inputs["Self Intersection"].default_value = False
    boolean.inputs["Hole Tolerant"].default_value = False
    # Blender 4.x: inputs[0] = Mesh 1, inputs[1] = Mesh 2
    links.new(set_pos_2.outputs["Geometry"], boolean.inputs[0])
    links.new(input_node.outputs["Geometry"], boolean.inputs[1])
    
    # Output
    links.new(boolean.outputs["Mesh"], output_node.inputs["Mesh"])
    
    auto_layout_nodes(group)
    return group
 