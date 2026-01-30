"""
Worn Edges Geometry Node Group

Creates worn/chipped edge details on geometry by detecting sharp edges
and applying noise-based displacement along those edges.

Technique:
    1. Capture Edge Angle on the original low-poly mesh
    2. Apply uniform edge offset along normals (Stage 1)
    3. Subdivide and smooth with Subdivision Surface
    4. Apply noise-based displacement for irregular edges (Stage 2)
    5. Optionally clip against original mesh with Boolean intersection 
"""

import bpy
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import (
    math_op, vec_math_op, create_node, link_or_set, get_or_rebuild_node_group
)


@geo_node_group
def create_worn_edges_group():
    """Creates a Geometry Node group that applies worn/chipped details to sharp edges.
    
    Uses two-stage displacement:
    1. Uniform edge offset creates the base chip shape
    2. Ridged noise adds irregular variation
    
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
    
    edge_thresh_socket = group.interface.new_socket(name="Edge Threshold", in_out='INPUT', socket_type='NodeSocketFloat')
    edge_thresh_socket.default_value = 1.0  # Radians, approx 57 degrees
    edge_thresh_socket.min_value = 0.0
    edge_thresh_socket.max_value = 3.14159
    
    edge_offset_socket = group.interface.new_socket(name="Edge Offset", in_out='INPUT', socket_type='NodeSocketFloat')
    edge_offset_socket.default_value = 0.02
    edge_offset_socket.min_value = 0.0
    
    noise_scale_socket = group.interface.new_socket(name="Noise Scale", in_out='INPUT', socket_type='NodeSocketFloat')
    noise_scale_socket.default_value = 10.0
    noise_scale_socket.min_value = 0.1
    
    noise_strength_socket = group.interface.new_socket(name="Noise Strength", in_out='INPUT', socket_type='NodeSocketFloat')
    noise_strength_socket.default_value = 0.5
    noise_strength_socket.min_value = 0.0
    
    use_boolean_socket = group.interface.new_socket(name="Use Boolean", in_out='INPUT', socket_type='NodeSocketBool')
    use_boolean_socket.default_value = False
    
    group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new("NodeGroupInput")
    output_node = nodes.new("NodeGroupOutput")

    # 1. Capture Edge Angle on low-poly mesh before any modifications
    edge_angle = nodes.new("GeometryNodeInputMeshEdgeAngle")
    
    capture_attr = nodes.new("GeometryNodeCaptureAttribute")
    capture_attr.domain = 'POINT'  # Interpolate edge data to points
    links.new(input_node.outputs["Geometry"], capture_attr.inputs["Geometry"])
    # Blender 4.x: Value socket is at index 1 (index 0 is Geometry)
    links.new(edge_angle.outputs["Unsigned Angle"], capture_attr.inputs[1])
    
    # 2. Create edge mask from captured angle
    # Map edge angle to 0-1 range based on threshold
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.interpolation_type = 'LINEAR'
    map_range.inputs["From Min"].default_value = 0.0
    # Blender 4.x: Captured value is at outputs[1] (outputs[0] is Geometry)
    links.new(capture_attr.outputs[1], map_range.inputs["Value"])
    links.new(input_node.outputs["Edge Threshold"], map_range.inputs["From Max"])
    
    edge_mask = map_range.outputs["Result"]
    
    # 3. Stage 1: Apply uniform edge offset along normals
    normal = nodes.new("GeometryNodeInputNormal")
    
    # Scale edge offset by edge mask (only displace near sharp edges)
    edge_offset_scaled = math_op(group, 'MULTIPLY', edge_mask, input_node.outputs["Edge Offset"])
    edge_offset_vec = vec_math_op(group, 'SCALE', normal.outputs["Normal"], edge_offset_scaled)
    
    # Negate to push inward (chips go into the surface)
    edge_offset_neg = vec_math_op(group, 'SCALE', edge_offset_vec, -1.0)
    
    offset_geo = create_node(group, "GeometryNodeSetPosition", {
        "Geometry": capture_attr.outputs["Geometry"],
        "Offset": edge_offset_neg
    })
    
    # 4. Subdivide mesh to add resolution for displacement
    subdiv = create_node(group, "GeometryNodeSubdivideMesh", {
        "Mesh": offset_geo.outputs["Geometry"],
        "Level": input_node.outputs["Subdivisions"]
    })
    
    # 5. Subdivision Surface for smoother results
    subdiv_surface = nodes.new("GeometryNodeSubdivisionSurface")
    links.new(subdiv.outputs["Mesh"], subdiv_surface.inputs["Mesh"])
    subdiv_surface.inputs["Level"].default_value = 1
    subdiv_surface.inputs["Edge Crease"].default_value = 0.0
    subdiv_surface.inputs["Vertex Crease"].default_value = 0.0
    
    # 6. Stage 2: Apply noise-based displacement for irregular edges
    position = nodes.new("GeometryNodeInputPosition")
    
    # Use Ridged Multifractal noise for more realistic chipping
    noise = nodes.new("ShaderNodeTexNoise")
    noise.noise_dimensions = '3D'
    noise.noise_type = 'RIDGED_MULTIFRACTAL'
    links.new(position.outputs["Position"], noise.inputs["Vector"])
    link_or_set(group, noise.inputs["Scale"], input_node.outputs["Noise Scale"])
    noise.inputs["Roughness"].default_value = 0.25
    noise.inputs["Detail"].default_value = 1.0
    noise.inputs["Lacunarity"].default_value = 2.0
    
    # Center noise around 0 by subtracting 0.5
    noise_centered = math_op(group, 'SUBTRACT', noise.outputs["Fac"], 0.5)
    
    # Scale noise by strength and edge mask
    noise_masked = math_op(group, 'MULTIPLY', noise_centered, edge_mask)
    noise_scaled = math_op(group, 'MULTIPLY', noise_masked, input_node.outputs["Noise Strength"])
    
    # Get normal after subdivision for accurate displacement direction
    normal_post = nodes.new("GeometryNodeInputNormal")
    
    # Create noise displacement vector
    noise_displacement = vec_math_op(group, 'SCALE', normal_post.outputs["Normal"], noise_scaled)
    
    # Negate to push inward
    noise_displacement_neg = vec_math_op(group, 'SCALE', noise_displacement, -1.0)
    
    # Apply noise displacement
    set_pos_noise = create_node(group, "GeometryNodeSetPosition", {
        "Geometry": subdiv_surface.outputs["Mesh"],
        "Offset": noise_displacement_neg
    })
    
    # 7. Store wear factor as attribute for material use
    store_wear = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Geometry": set_pos_noise.outputs["Geometry"],
        "Name": "wear_factor",
        "Domain": "POINT",
        "Data Type": "FLOAT"
    })
    # Store edge mask as wear factor (0-1 range)
    links.new(edge_mask, store_wear.inputs["Value"])
    
    # 8. Optional Boolean intersection to clip against original mesh
    boolean = nodes.new("GeometryNodeMeshBoolean")
    boolean.operation = 'INTERSECT'
    boolean.solver = 'EXACT'
    # Blender 4.x: Boolean uses indexed inputs - inputs[0] is Mesh 1, inputs[1] is Mesh 2
    links.new(store_wear.outputs["Geometry"], boolean.inputs[0])
    links.new(input_node.outputs["Geometry"], boolean.inputs[1])
    boolean.inputs["Self Intersection"].default_value = False
    boolean.inputs["Hole Tolerant"].default_value = False
    
    # 9. Switch between boolean and non-boolean output
    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = 'GEOMETRY'
    links.new(input_node.outputs["Use Boolean"], switch.inputs["Switch"])
    links.new(store_wear.outputs["Geometry"], switch.inputs["False"])
    links.new(boolean.outputs["Mesh"], switch.inputs["True"])
    
    # Output
    links.new(switch.outputs["Output"], output_node.inputs["Geometry"])
    
    auto_layout_nodes(group)
    return group
