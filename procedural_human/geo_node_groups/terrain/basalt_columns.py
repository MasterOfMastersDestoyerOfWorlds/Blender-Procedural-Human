"""
Basalt Columns Geometry Node Group

Generates hexagonal basalt rock columns similar to those found at
Stuðlagil Canyon and Reynisfjara Beach in Iceland.

Technique:
    1. Create a Grid primitive
    2. Triangulate to create uniform triangles
    3. Apply Dual Mesh to convert triangles to hexagons
    4. Split Edges to separate columns
    5. Scale Elements to create gaps between columns
    6. Extrude with random height per column
"""

import bpy
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import (
    math_op, vec_math_op, create_node, link_or_set, get_or_rebuild_node_group
)


@geo_node_group
def create_basalt_columns_group():
    """Creates a Geometry Node group that generates hexagonal basalt columns.
    
    The group creates a field of hexagonal columns with varying heights,
    simulating the natural columnar jointing found in cooled basaltic lava.
    
    :returns: The Basalt Columns node group.
    """
    group_name = "BasaltColumns"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group
    
    # --- Interface ---
    size_x_socket = group.interface.new_socket(name="Size X", in_out='INPUT', socket_type='NodeSocketFloat')
    size_x_socket.default_value = 10.0
    size_x_socket.min_value = 0.1
    
    size_y_socket = group.interface.new_socket(name="Size Y", in_out='INPUT', socket_type='NodeSocketFloat')
    size_y_socket.default_value = 10.0
    size_y_socket.min_value = 0.1
    
    resolution_socket = group.interface.new_socket(name="Resolution", in_out='INPUT', socket_type='NodeSocketInt')
    resolution_socket.default_value = 20
    resolution_socket.min_value = 3
    resolution_socket.max_value = 100
    
    min_height_socket = group.interface.new_socket(name="Min Height", in_out='INPUT', socket_type='NodeSocketFloat')
    min_height_socket.default_value = 0.5
    min_height_socket.min_value = 0.0
    
    max_height_socket = group.interface.new_socket(name="Max Height", in_out='INPUT', socket_type='NodeSocketFloat')
    max_height_socket.default_value = 3.0
    max_height_socket.min_value = 0.0
    
    crack_width_socket = group.interface.new_socket(name="Crack Width", in_out='INPUT', socket_type='NodeSocketFloat')
    crack_width_socket.default_value = 0.95
    crack_width_socket.min_value = 0.5
    crack_width_socket.max_value = 1.0
    crack_width_socket.subtype = 'FACTOR'
    
    seed_socket = group.interface.new_socket(name="Seed", in_out='INPUT', socket_type='NodeSocketInt')
    seed_socket.default_value = 0
    
    top_roughness_socket = group.interface.new_socket(name="Top Roughness", in_out='INPUT', socket_type='NodeSocketFloat')
    top_roughness_socket.default_value = 0.1
    top_roughness_socket.min_value = 0.0
    top_roughness_socket.max_value = 1.0
    top_roughness_socket.subtype = 'FACTOR'
    
    group.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    
    input_node = nodes.new("NodeGroupInput")
    output_node = nodes.new("NodeGroupOutput")

    # 1. Create base grid
    grid = nodes.new("GeometryNodeMeshGrid")
    links.new(input_node.outputs["Size X"], grid.inputs["Size X"])
    links.new(input_node.outputs["Size Y"], grid.inputs["Size Y"])
    links.new(input_node.outputs["Resolution"], grid.inputs["Vertices X"])
    links.new(input_node.outputs["Resolution"], grid.inputs["Vertices Y"])
    
    # 2. Triangulate to create uniform triangle mesh
    triangulate = create_node(group, "GeometryNodeTriangulate", {
        "Mesh": grid.outputs["Mesh"]
    })
    
    # 3. Dual Mesh converts triangles to hexagons
    dual_mesh = create_node(group, "GeometryNodeDualMesh", {
        "Mesh": triangulate.outputs["Mesh"]
    })
    
    # 4. Split edges so each hexagon becomes separate island
    split_edges = create_node(group, "GeometryNodeSplitEdges", {
        "Mesh": dual_mesh.outputs["Dual Mesh"]
    })
    
    # 5. Scale elements to create gaps between columns
    scale_elements = create_node(group, "GeometryNodeScaleElements", {
        "Geometry": split_edges.outputs["Mesh"],
        "Scale": input_node.outputs["Crack Width"]
    })
    scale_elements.domain = 'FACE'
    
    # 6. Store face index before extrusion for per-column randomization
    face_index = nodes.new("GeometryNodeInputIndex")
    
    store_column_id = create_node(group, "GeometryNodeStoreNamedAttribute", {
        "Geometry": scale_elements.outputs["Geometry"],
        "Name": "column_id",
        "Domain": "FACE",
        "Data Type": "INT",
        "Value": face_index.outputs["Index"]
    })
    
    # 7. Generate random height per column using face index as seed
    random_height = nodes.new("FunctionNodeRandomValue")
    random_height.data_type = 'FLOAT'
    links.new(input_node.outputs["Min Height"], random_height.inputs["Min"])
    links.new(input_node.outputs["Max Height"], random_height.inputs["Max"])
    links.new(input_node.outputs["Seed"], random_height.inputs["Seed"])
    # Use face index as ID for per-face randomization
    links.new(face_index.outputs["Index"], random_height.inputs["ID"])
    
    # 8. Extrude faces upward with random height
    extrude = nodes.new("GeometryNodeExtrudeMesh")
    extrude.mode = 'FACES'
    links.new(store_column_id.outputs["Geometry"], extrude.inputs["Mesh"])
    links.new(random_height.outputs["Value"], extrude.inputs["Offset Scale"])
    extrude.inputs["Individual"].default_value = True
    
    # 9. Add roughness to top faces using noise displacement
    # Get selection of top faces (extruded faces)
    top_selection = extrude.outputs["Top"]
    
    # Position for noise
    position = nodes.new("GeometryNodeInputPosition")
    
    # Noise for top surface roughness
    noise = nodes.new("ShaderNodeTexNoise")
    noise.noise_dimensions = '3D'
    links.new(position.outputs["Position"], noise.inputs["Vector"])
    noise.inputs["Scale"].default_value = 5.0
    noise.inputs["Roughness"].default_value = 0.6
    noise.inputs["Detail"].default_value = 3.0
    
    # Center noise and scale by roughness parameter
    noise_centered = math_op(group, 'SUBTRACT', noise.outputs["Fac"], 0.5)
    noise_scaled = math_op(group, 'MULTIPLY', noise_centered, input_node.outputs["Top Roughness"])
    
    # Displacement vector (only Z direction for tops)
    normal = nodes.new("GeometryNodeInputNormal")
    displacement = vec_math_op(group, 'SCALE', normal.outputs["Normal"], noise_scaled)
    
    # Apply displacement only to top faces
    set_pos = create_node(group, "GeometryNodeSetPosition", {
        "Geometry": extrude.outputs["Mesh"],
        "Selection": top_selection,
        "Offset": displacement
    })
    
    # 10. Set smooth shading on sides, flat on tops
    # Invert top selection for sides
    not_top = nodes.new("FunctionNodeBooleanMath")
    not_top.operation = 'NOT'
    links.new(top_selection, not_top.inputs[0])
    
    set_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    links.new(set_pos.outputs["Geometry"], set_smooth.inputs["Geometry"])
    links.new(not_top.outputs["Boolean"], set_smooth.inputs["Selection"])
    set_smooth.inputs["Shade Smooth"].default_value = True
    
    # Output
    links.new(set_smooth.outputs["Geometry"], output_node.inputs["Geometry"])
    
    auto_layout_nodes(group)
    return group
