"""
Worn Edges Geometry Node Group

Creates worn/chipped edge details on geometry by detecting sharp edges
and applying noise-based displacement along those edges.

Technique:
    1. Capture Edge Angle on the original low-poly mesh
    2. Subdivide to increase resolution
    3. Use Noise Texture mixed with edge angle to create a wear mask
    4. Displace vertices along normals based on the mask
"""

import bpy
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import (
    math_op, vec_math_op, create_node, link_or_set
)


@geo_node_group
def create_worn_edges_group():
    """Creates a Geometry Node group that applies worn/chipped details to sharp edges.
    
    The group takes low-poly geometry, subdivides it, and displaces vertices near
    sharp edges using noise to create a weathered, chipped appearance.
    
    :returns: The Worn Edges node group.
    """
    group_name = "WornEdges"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(name=group_name, type='GeometryNodeTree')
    
    # --- Interface ---
    group.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    
    subdiv_socket = group.interface.new_socket(name="Subdivisions", in_out='INPUT', socket_type='NodeSocketInt')
    subdiv_socket.default_value = 3
    subdiv_socket.min_value = 0
    subdiv_socket.max_value = 6
    
    wear_scale_socket = group.interface.new_socket(name="Wear Scale", in_out='INPUT', socket_type='NodeSocketFloat')
    wear_scale_socket.default_value = 10.0
    wear_scale_socket.min_value = 0.1
    
    wear_depth_socket = group.interface.new_socket(name="Wear Depth", in_out='INPUT', socket_type='NodeSocketFloat')
    wear_depth_socket.default_value = 0.05
    
    edge_thresh_socket = group.interface.new_socket(name="Edge Threshold", in_out='INPUT', socket_type='NodeSocketFloat')
    edge_thresh_socket.default_value = 1.0  # Radians, approx 57 degrees
    edge_thresh_socket.min_value = 0.0
    edge_thresh_socket.max_value = 3.14159
    
    group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new("NodeGroupInput")
    output_node = nodes.new("NodeGroupOutput")

    # 1. Capture Edge Angle on low-poly mesh before subdivision
    edge_angle = nodes.new("GeometryNodeInputMeshEdgeAngle")
    
    capture_attr = nodes.new("GeometryNodeCaptureAttribute")
    capture_attr.domain = 'POINT'  # Interpolate edge data to points
    links.new(input_node.outputs["Geometry"], capture_attr.inputs["Geometry"])
    # Blender 4.x: Use indexed socket access for Capture Attribute value
    links.new(edge_angle.outputs["Unsigned Angle"], capture_attr.inputs[0])
    
    # 2. Subdivide mesh to add resolution for displacement
    subdiv = create_node(group, "GeometryNodeSubdivideMesh", {
        "Mesh": capture_attr.outputs["Geometry"],
        "Level": input_node.outputs["Subdivisions"]
    })
    
    # 3. Create wear mask using noise
    position = nodes.new("GeometryNodeInputPosition")
    
    noise = nodes.new("ShaderNodeTexNoise")
    noise.noise_dimensions = '3D'
    links.new(position.outputs["Position"], noise.inputs["Vector"])
    link_or_set(group, noise.inputs["Scale"], input_node.outputs["Wear Scale"])
    noise.inputs["Roughness"].default_value = 0.7
    noise.inputs["Detail"].default_value = 4.0
    
    # Center noise around 0 by subtracting 0.5
    noise_centered = math_op(group, 'SUBTRACT', noise.outputs["Fac"], 0.5)
    
    # 4. Map edge angle to 0-1 range based on threshold
    # Edges sharper than threshold get full effect
    map_range = nodes.new("ShaderNodeMapRange")
    map_range.interpolation_type = 'LINEAR'
    map_range.inputs["From Min"].default_value = 0.0
    # Blender 4.x: Use indexed socket access for Capture Attribute output
    links.new(capture_attr.outputs[0], map_range.inputs["Value"])
    links.new(input_node.outputs["Edge Threshold"], map_range.inputs["From Max"])
    
    # 5. Combine noise with edge mask
    wear_mask = math_op(group, 'MULTIPLY', noise_centered, map_range.outputs["Result"])
    
    # 6. Create displacement vector along normal
    normal = nodes.new("GeometryNodeInputNormal")
    
    # Scale normal by wear mask
    displacement_dir = vec_math_op(group, 'SCALE', normal.outputs["Normal"], wear_mask)
    
    # Apply depth multiplier
    displacement = vec_math_op(group, 'SCALE', displacement_dir, input_node.outputs["Wear Depth"])
    
    # 7. Apply displacement
    set_pos = create_node(group, "GeometryNodeSetPosition", {
        "Geometry": subdiv.outputs["Mesh"],
        "Offset": displacement
    })
    
    # 8. Store wear factor as attribute for material use
    store_wear = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Geometry": set_pos.outputs["Geometry"],
        "Name": "wear_factor",
        "Domain": "POINT",
        "Data Type": "FLOAT"
    })
    # Remap wear mask to 0-1 for material
    wear_factor_abs = math_op(group, 'ABSOLUTE', wear_mask)
    links.new(wear_factor_abs, store_wear.inputs["Value"])
    
    # Output
    links.new(store_wear.outputs["Geometry"], output_node.inputs["Geometry"])
    
    auto_layout_nodes(group)
    return group
