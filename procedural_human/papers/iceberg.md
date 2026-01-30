Based on your existing codebase, specifically the pattern in node_helpers.py and loft_spheroid.py, here is a plan to implement a procedural iceberg generator.
1. New File Structure

Create a new file procedural_human/geo_node_groups/iceberg.py. This keeps the "Iceberg" logic isolated but utilizes your shared node_helpers.
2. Geometry Strategy

Icebergs are distinct from the smooth, lofted shapes in your current loft_spheroid.py. They require jagged, crystalline displacement.

    Base Mesh: An Ico Sphere or highly subdivided Cube is better than a Grid to allow for full 3D rotation/floating.

    Displacement: Use Voronoi Texture (Distance Edge) or F1 subtracted from F2 to create sharp ridges (crystalline look).

    Waterline: Use Set Position to flatten the bottom or a Boolean (if computationally affordable) to "cut" the submerged part flat if desired.

3. Implementation Plan using node_helpers.py

You will define a function create_iceberg_group() decorated with @geo_node_group (if you have that decorator available, otherwise just the function).
Inputs to define:

    Seed (Int)

    Scale (Float) - Overall size of the iceberg chunks.

    Detail (Float) - Strength of the noise.

    Water Level (Float) - Where to flatten the base.

Step-by-Step Logic (mapped to your helpers):

    Base Geometry:

        Use create_node(group, "GeometryNodeMeshIcoSphere", {"Radius": 1.0, "Subdivisions": 5}).

    Jagged Displacement (The "Ice" Look):

        Create a ShaderNodeTexVoronoi.

        Use math_op to manipulate the texture output (e.g., SUBTRACT offset to center it).

        Use vec_math_op(group, "SCALE", normal, displacement_strength) to calculate the offset vector.

        Apply with create_node(group, "GeometryNodeSetPosition", {"Offset": offset_vector}).

    Flatten Bottom:

        Get the Position node.

        Use compare_float_less(group, z_component, water_level).

        Use switch_vec (from your helpers) to switch between the original position and a flattened position (Z = water_level) based on the comparison.

        Apply via Set Position.

    Material Attributes:

        Calculate "Snow" coverage: vec_math_op("DOT_PRODUCT", normal, (0,0,1)).

        Use create_node(group, "GeometryNodeStoreNamedAttribute", ...) to store this as "snow_factor" for the shader to use.

4. Code Draft (for iceberg.py)

Here is how the code would look using your specific node_helpers.py syntax:
Python

import bpy
from procedural_human.geo_node_groups.node_helpers import (
    create_node, math_op, vec_math_op, link_or_set, 
    get_attr, compare_float_less, switch_vec
)

def create_iceberg_group():
    group_name = "ProceduralIceberg"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    # Define Inputs
    group.interface.new_socket("Seed", in_out="INPUT", socket_type="NodeSocketInt")
    group.interface.new_socket("Scale", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    group.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    # Nodes
    in_node = group.nodes.new("NodeGroupInput")
    out_node = group.nodes.new("NodeGroupOutput")
    
    # 1. Base Geometry (Ico Sphere for uniform displacement)
    ico = create_node(group, "GeometryNodeMeshIcoSphere", {"Radius": 2.0, "Subdivisions": 5})
    
    # 2. Generate Voronoi Noise (Jagged Edges)
    # We need 4D noise to use the Seed
    voronoi = create_node(group, "ShaderNodeTexVoronoi", {"Feature": "DISTANCE_TO_EDGE", "Dimensions": "4D"})
    link_or_set(group, voronoi.inputs["W"], in_node.outputs["Seed"])
    link_or_set(group, voronoi.inputs["Scale"], 2.0)
    
    # 3. Displace along Normal
    # Get Normal and Scale it by Voronoi output
    normal = create_node(group, "GeometryNodeInputNormal").outputs[0]
    
    # Invert Voronoi for "peaks" vs "cracks"
    # (Distance to edge is 0 at edge, so we might want to invert or map range)
    disp_strength = math_op(group, "MULTIPLY", voronoi.outputs["Distance"], in_node.outputs["Scale"])
    offset_vec = vec_math_op(group, "SCALE", normal, disp_strength)
    
    set_pos_disp = create_node(group, "GeometryNodeSetPosition", {"Geometry": ico.outputs["Mesh"], "Offset": offset_vec})
    
    # 4. Flatten Bottom (Simple waterline cut)
    # Get current position
    pos_node = create_node(group, "GeometryNodeInputPosition")
    sep_xyz = create_node(group, "ShaderNodeSeparateXYZ", {"Vector": pos_node.outputs[0]})
    
    # If Z < -0.5, Flatten to -0.5
    water_level = -0.5
    is_underwater = compare_float_less(group, sep_xyz.outputs["Z"], water_level)
    
    # Construct flattened vector (X, Y, water_level)
    flat_pos = create_node(group, "ShaderNodeCombineXYZ", {
        "X": sep_xyz.outputs["X"], 
        "Y": sep_xyz.outputs["Y"], 
        "Z": water_level
    })
    
    # Switch position based on underwater check
    final_pos_vec = switch_vec(group, is_underwater, pos_node.outputs[0], flat_pos.outputs[0])
    
    set_pos_flat = create_node(group, "GeometryNodeSetPosition", {
        "Geometry": set_pos_disp.outputs["Geometry"], 
        "Position": final_pos_vec
    })

    # 5. Output
    link_or_set(group, out_node.inputs["Geometry"], set_pos_flat.outputs["Geometry"])
    
    return group

5. Integration

To make this available in your addon/tool:

    Save the code above into procedural_human/geo_node_groups/iceberg.py.

    Import create_iceberg_group in your main operator or menu file.

    Assign an Ice Material (High transmission, high roughness, subsurface scattering) to the output geometry.

Reference for Voronoi-based iceberg workflow: Voronoi Glaciers Reddit Thread.

Relevant Video Tutorial: Polar Landscape with Icebergs and Ocean - Blender Geometry Nodes Tutorial This video covers the specific workflow of using noise displacement on a subdivided mesh to create the jagged iceberg look, which directly informs the node structure planned above.