Plan Overview

We will implement two new procedural geometry node groups in the procedural_human/geo_node_groups package. These groups will be defined as Python modules that generate the node trees programmatically using the bpy API.

1. worn_edges.py

    Goal: Convert low-poly geometry into high-resolution worn/chipped details.

    Technique:

        Capture Data: Capture the Edge Angle of the original low-poly mesh to identify sharp corners.

        Subdivide: Apply Subdivide Mesh (Catmull-Clark) to increase resolution.

        Displace: Use a Noise Texture mixed with the captured edge angle to displace vertices only near the original sharp edges, creating a chipped effect.

2. basalt_columns.py

    Goal: Generate hexagonal basalt rock columns.

    Technique:

        Base Grid: Start with a Grid primitive.

        Hex Conversion: Use Triangulate followed by Dual Mesh to convert the grid into a honeycomb/hexagonal pattern.

        Separation: Use Split Edges and Scale Elements to create physical gaps between columns.

        Extrusion: Use Extrude Mesh with a Random Value driving the height to create the stepped rock formation.

Step 1: Create worn_edges.py

Create a new file: procedural_human/geo_node_groups/worn_edges.py
Python

import bpy
from ..utils.node_layout import layout_nodes

def create_worn_edges_group():
    """
    Creates a Geometry Node group that takes low-poly geometry, subdivides it,
    and applies worn/chipped details to the sharp edges.
    """
    group_name = "Worn Edges"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    ng = bpy.data.node_groups.new(name=group_name, type='GeometryNodeTree')
    
    # --- Interfaces ---
    # Input
    ng.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    subdiv_socket = ng.interface.new_socket(name="Subdivisions", in_out='INPUT', socket_type='NodeSocketInt')
    subdiv_socket.default_value = 3
    subdiv_socket.min_value = 0
    subdiv_socket.max_value = 6
    
    wear_scale_socket = ng.interface.new_socket(name="Wear Scale", in_out='INPUT', socket_type='NodeSocketFloat')
    wear_scale_socket.default_value = 10.0
    
    wear_depth_socket = ng.interface.new_socket(name="Wear Depth", in_out='INPUT', socket_type='NodeSocketFloat')
    wear_depth_socket.default_value = 0.05
    
    edge_thresh_socket = ng.interface.new_socket(name="Edge Threshold", in_out='INPUT', socket_type='NodeSocketFloat')
    edge_thresh_socket.default_value = 1.0  # Radians, approx 57 degrees

    # Output
    ng.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    # --- Nodes ---
    input_node = ng.nodes.new("NodeGroupInput")
    output_node = ng.nodes.new("NodeGroupOutput")

    # 1. Capture Edge Info on Low Poly
    edge_angle = ng.nodes.new("GeometryNodeInputMeshEdgeAngle")
    capture_attr = ng.nodes.new("GeometryNodeCaptureAttribute")
    capture_attr.domain = 'POINT'  # Interpolate edge data to points
    
    # 2. Subdivide
    subdiv = ng.nodes.new("GeometryNodeSubdivideMesh")
    
    # 3. Create Wear Mask (Noise * Edge Angle)
    noise = ng.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Roughness"].default_value = 0.7
    noise.inputs["Detail"].default_value = 4.0
    
    # Subtract 0.5 from noise to center it
    math_sub = ng.nodes.new("ShaderNodeMath")
    math_sub.operation = 'SUBTRACT'
    math_sub.inputs[1].default_value = 0.5
    
    # Map Range for Edge Angle (Sharpen the selection)
    map_range = ng.nodes.new("ShaderNodeMapRange")
    map_range.inputs["From Min"].default_value = 0.0
    # Connect Threshold to From Max
    
    math_mult_mask = ng.nodes.new("ShaderNodeMath")
    math_mult_mask.operation = 'MULTIPLY'
    
    # 4. Displace
    normal = ng.nodes.new("GeometryNodeInputNormal")
    vec_math_scale = ng.nodes.new("ShaderNodeVectorMath")
    vec_math_scale.operation = 'SCALE'
    
    vec_math_depth = ng.nodes.new("ShaderNodeVectorMath")
    vec_math_depth.operation = 'SCALE'
    
    set_pos = ng.nodes.new("GeometryNodeSetPosition")

    # --- Links ---
    links = ng.links
    
    # Capture Attribute Flow
    links.new(input_node.outputs["Geometry"], capture_attr.inputs["Geometry"])
    links.new(edge_angle.outputs["Unsigned Angle"], capture_attr.inputs["Value"])
    
    # Subdivide Flow
    links.new(capture_attr.outputs["Geometry"], subdiv.inputs["Mesh"])
    links.new(input_node.outputs["Subdivisions"], subdiv.inputs["Level"])
    
    # Noise Logic
    links.new(input_node.outputs["Wear Scale"], noise.inputs["Scale"])
    links.new(noise.outputs["Fac"], math_sub.inputs[0])
    
    # Mask Logic (Edge Angle -> Map Range)
    links.new(capture_attr.outputs["Attribute"], map_range.inputs["Value"])
    links.new(input_node.outputs["Edge Threshold"], map_range.inputs["From Max"])
    
    # Combine Noise + Mask
    links.new(math_sub.outputs["Value"], math_mult_mask.inputs[0])
    links.new(map_range.outputs["Result"], math_mult_mask.inputs[1])
    
    # Displacement Vector Logic
    links.new(normal.outputs["Vector"], vec_math_scale.inputs["Vector"])
    links.new(math_mult_mask.outputs["Value"], vec_math_scale.inputs["Scale"])
    
    # Apply Depth Strength
    links.new(vec_math_scale.outputs["Vector"], vec_math_depth.inputs["Vector"])
    links.new(input_node.outputs["Wear Depth"], vec_math_depth.inputs["Scale"])
    
    # Set Position
    links.new(subdiv.outputs["Mesh"], set_pos.inputs["Geometry"])
    links.new(vec_math_depth.outputs["Vector"], set_pos.inputs["Offset"])
    
    # Output
    links.new(set_pos.outputs["Geometry"], output_node.inputs["Geometry"])
    
    # Layout (Optional if you have the utility)
    layout_nodes(ng)
    
    return ng

Step 2: Create basalt_columns.py

Create a new file: procedural_human/geo_node_groups/basalt_columns.py
Python

import bpy
from ..utils.node_layout import layout_nodes

def create_basalt_columns_group():
    """
    Creates a procedural basalt column generator using Dual Mesh logic.
    """
    group_name = "Basalt Columns"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    ng = bpy.data.node_groups.new(name=group_name, type='GeometryNodeTree')

    # --- Interfaces ---
    ng.interface.new_socket(name="Size X", in_out='INPUT', socket_type='NodeSocketFloat').default_value = 10.0
    ng.interface.new_socket(name="Size Y", in_out='INPUT', socket_type='NodeSocketFloat').default_value = 10.0
    ng.interface.new_socket(name="Resolution", in_out='INPUT', socket_type='NodeSocketInt').default_value = 20
    
    ng.interface.new_socket(name="Min Height", in_out='INPUT', socket_type='NodeSocketFloat').default_value = 0.5
    ng.interface.new_socket(name="Max Height", in_out='INPUT', socket_type='NodeSocketFloat').default_value = 3.0
    ng.interface.new_socket(name="Crack Width", in_out='INPUT', socket_type='NodeSocketFloat').default_value = 0.95 # Scale elements
    
    ng.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    # --- Nodes ---
    input_node = ng.nodes.new("NodeGroupInput")
    output_node = ng.nodes.new("NodeGroupOutput")

    # 1. Base Grid
    grid = ng.nodes.new("GeometryNodeMeshGrid")
    
    # 2. Convert to Hexagons (Dual Mesh method)
    triangulate = ng.nodes.new("GeometryNodeTriangulate")
    dual_mesh = ng.nodes.new("GeometryNodeDualMesh")
    
    # 3. Separate Columns
    split_edges = ng.nodes.new("GeometryNodeSplitEdges")
    
    # 4. Create Gaps
    scale_elements = ng.nodes.new("GeometryNodeScaleElements")
    
    # 5. Extrude Heights
    extrude = ng.nodes.new("GeometryNodeExtrudeMesh")
    extrude.inputs["Individual"].default_value = False # We want solid columns, not shells
    
    # Random Height Logic
    random_val = ng.nodes.new("FunctionNodeRandomValue")
    random_val.data_type = 'FLOAT'
    
    # We apply randomness to the "Offset Scale" of the extrusion
    # But Extrude Mesh "Offset Scale" is uniform. 
    # To randomize height per island, we need to scale the "Offset" vector.
    # Simpler way: Use 'Offset Scale' input of Extrude Mesh. It accepts fields!
    
    # 6. Cap the bottom (Optional, but Extrude leaves bottom open usually if not careful)
    # The grid is flat. Extruding up leaves a hole at Z=0. 
    # For basalt, we often want closed meshes. 
    # We can use "Join Geometry" with the original base, but Flip Faces is needed.
    # Simpler for now: Just extrude.
    
    # --- Links ---
    links = ng.links
    
    # Grid Setup
    links.new(input_node.outputs["Size X"], grid.inputs["Size X"])
    links.new(input_node.outputs["Size Y"], grid.inputs["Size Y"])
    # Map Resolution to Vertices X and Y
    links.new(input_node.outputs["Resolution"], grid.inputs["Vertices X"])
    links.new(input_node.outputs["Resolution"], grid.inputs["Vertices Y"])
    
    # Hex Logic
    links.new(grid.outputs["Mesh"], triangulate.inputs["Mesh"])
    links.new(triangulate.outputs["Mesh"], dual_mesh.inputs["Mesh"])
    
    # Split & Gap
    links.new(dual_mesh.outputs["Mesh"], split_edges.inputs["Mesh"])
    links.new(split_edges.outputs["Mesh"], scale_elements.inputs["Geometry"])
    links.new(input_node.outputs["Crack Width"], scale_elements.inputs["Scale"])
    
    # Extrude Logic
    links.new(scale_elements.outputs["Geometry"], extrude.inputs["Mesh"])
    
    # Height Randomization
    links.new(input_node.outputs["Min Height"], random_val.inputs["Min"])
    links.new(input_node.outputs["Max Height"], random_val.inputs["Max"])
    links.new(random_val.outputs["Value"], extrude.inputs["Offset Scale"])
    
    # Output
    links.new(extrude.outputs["Mesh"], output_node.inputs["Geometry"])

    layout_nodes(ng)
    return ng

Step 3: Update __init__.py

Modify procedural_human/geo_node_groups/__init__.py to include the new modules.
Python

from .worn_edges import create_worn_edges_group
from .basalt_columns import create_basalt_columns_group

# Add to your registration list or simply export them
__all__ = [
    # ... existing exports ...
    "create_worn_edges_group",
    "create_basalt_columns_group"
]

Relevance of Video

The selected video demonstrates a very similar technique for creating "worn edges" procedurally using noise and edge detection, which directly validates the approach used in the worn_edges.py plan (masking displacement on sharp edges).

Procedural Edge Wear With Geometry Nodes
Procedural Edge Wear With Geometry Nodes - YouTube
El3ctroNam Studios · 5.8K views