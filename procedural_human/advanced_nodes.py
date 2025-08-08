"""
Advanced Geometry Nodes setup for Procedural Human Generator
This module contains functions to create complex node setups for human anatomy
"""


def create_advanced_torso_nodes(node_group):
    """Create advanced torso shaping with proper anatomical proportions"""

    # Add geometry socket to node group interface
    if "Geometry" not in [socket.name for socket in node_group.interface.items_tree]:
        node_group.interface.new_socket(
            name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
        )
        node_group.interface.new_socket(
            name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
        )

    # Input/Output nodes
    input_node = node_group.nodes.new("NodeGroupInput")
    output_node = node_group.nodes.new("NodeGroupOutput")

    # Position nodes
    input_node.location = (-800, 0)
    output_node.location = (800, 0)

    # Base geometry - start with cylinder
    cylinder = node_group.nodes.new("GeometryNodeMeshCylinder")
    cylinder.location = (-600, 0)
    cylinder.inputs["Vertices"].default_value = 16
    cylinder.inputs["Radius"].default_value = 0.4
    cylinder.inputs["Depth"].default_value = 1.2

    # Add subdivision for smoother surface
    subdiv = node_group.nodes.new("GeometryNodeSubdivisionSurface")
    subdiv.location = (-400, 0)
    subdiv.inputs["Level"].default_value = 2

    # Create height-based shaping
    position = node_group.nodes.new("GeometryNodeInputPosition")
    position.location = (-600, 200)

    # Separate XYZ to get height component
    separate_xyz = node_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.location = (-400, 200)

    # Normalize height (0 to 1)
    map_range = node_group.nodes.new("ShaderNodeMapRange")
    map_range.location = (-200, 200)
    map_range.inputs["From Min"].default_value = -0.6
    map_range.inputs["From Max"].default_value = 0.6
    map_range.inputs["To Min"].default_value = 0.0
    map_range.inputs["To Max"].default_value = 1.0

    # Map range for torso silhouette
    map_range_torso = node_group.nodes.new("ShaderNodeMapRange")
    map_range_torso.location = (0, 200)
    map_range_torso.inputs["From Min"].default_value = 0.0
    map_range_torso.inputs["From Max"].default_value = 1.0
    map_range_torso.inputs["To Min"].default_value = 0.8
    map_range_torso.inputs["To Max"].default_value = 1.2

    # Combine position with curve output
    combine_xyz = node_group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.location = (200, 200)

    # Set position node for final shaping
    set_position = node_group.nodes.new("GeometryNodeSetPosition")
    set_position.location = (400, 0)

    # Connect nodes
    node_group.links.new(cylinder.outputs["Mesh"], subdiv.inputs["Mesh"])
    node_group.links.new(subdiv.outputs["Mesh"], set_position.inputs["Geometry"])
    node_group.links.new(position.outputs["Position"], separate_xyz.inputs["Vector"])
    node_group.links.new(separate_xyz.outputs["Z"], map_range.inputs["Value"])
    node_group.links.new(map_range.outputs["Result"], map_range_torso.inputs["Value"])
    node_group.links.new(map_range_torso.outputs["Result"], combine_xyz.inputs["X"])
    node_group.links.new(combine_xyz.outputs["Vector"], set_position.inputs["Offset"])
    node_group.links.new(
        set_position.outputs["Geometry"], output_node.inputs["Geometry"]
    )

    return node_group


def create_advanced_limb_nodes(node_group, limb_type="arm"):
    """Create advanced limb shaping with muscle definition"""

    # Add geometry socket to node group interface
    if "Geometry" not in [socket.name for socket in node_group.interface.items_tree]:
        node_group.interface.new_socket(
            name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
        )
        node_group.interface.new_socket(
            name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
        )

    # Input/Output nodes
    input_node = node_group.nodes.new("NodeGroupInput")
    output_node = node_group.nodes.new("NodeGroupOutput")

    # Position nodes
    input_node.location = (-800, 0)
    output_node.location = (800, 0)

    # Base cylinder
    cylinder = node_group.nodes.new("GeometryNodeMeshCylinder")
    cylinder.location = (-600, 0)
    cylinder.inputs["Vertices"].default_value = 12
    cylinder.inputs["Radius"].default_value = 0.1
    cylinder.inputs["Depth"].default_value = 0.8

    # Add subdivision
    subdiv = node_group.nodes.new("GeometryNodeSubdivisionSurface")
    subdiv.location = (-400, 0)
    subdiv.inputs["Level"].default_value = 2

    # Position for height-based shaping
    position = node_group.nodes.new("GeometryNodeInputPosition")
    position.location = (-600, 200)

    # Separate XYZ
    separate_xyz = node_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.location = (-400, 200)

    # Map range for height
    map_range = node_group.nodes.new("ShaderNodeMapRange")
    map_range.location = (-200, 200)
    map_range.inputs["From Min"].default_value = -0.4
    map_range.inputs["From Max"].default_value = 0.4
    map_range.inputs["To Min"].default_value = 0.0
    map_range.inputs["To Max"].default_value = 1.0

    # Map range for muscle shape
    map_range_muscle = node_group.nodes.new("ShaderNodeMapRange")
    map_range_muscle.location = (0, 200)
    if limb_type == "arm":
        # Bicep/tricep shape
        map_range_muscle.inputs["From Min"].default_value = 0.0
        map_range_muscle.inputs["From Max"].default_value = 1.0
        map_range_muscle.inputs["To Min"].default_value = 0.8
        map_range_muscle.inputs["To Max"].default_value = 1.2
    else:
        # Thigh/calf shape
        map_range_muscle.inputs["From Min"].default_value = 0.0
        map_range_muscle.inputs["From Max"].default_value = 1.0
        map_range_muscle.inputs["To Min"].default_value = 1.0
        map_range_muscle.inputs["To Max"].default_value = 1.3

    # Combine XYZ
    combine_xyz = node_group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.location = (200, 200)

    # Set position
    set_position = node_group.nodes.new("GeometryNodeSetPosition")
    set_position.location = (400, 0)

    # Connect nodes
    node_group.links.new(cylinder.outputs["Mesh"], subdiv.inputs["Mesh"])
    node_group.links.new(subdiv.outputs["Mesh"], set_position.inputs["Geometry"])
    node_group.links.new(position.outputs["Position"], separate_xyz.inputs["Vector"])
    node_group.links.new(separate_xyz.outputs["Z"], map_range.inputs["Value"])
    node_group.links.new(map_range.outputs["Result"], map_range_muscle.inputs["Value"])
    node_group.links.new(map_range_muscle.outputs["Result"], combine_xyz.inputs["X"])
    node_group.links.new(combine_xyz.outputs["Vector"], set_position.inputs["Offset"])
    node_group.links.new(
        set_position.outputs["Geometry"], output_node.inputs["Geometry"]
    )

    return node_group


def create_advanced_head_nodes(node_group):
    """Create advanced head shaping with facial features"""

    # Add geometry socket to node group interface
    if "Geometry" not in [socket.name for socket in node_group.interface.items_tree]:
        node_group.interface.new_socket(
            name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
        )
        node_group.interface.new_socket(
            name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
        )

    # Input/Output nodes
    input_node = node_group.nodes.new("NodeGroupInput")
    output_node = node_group.nodes.new("NodeGroupOutput")

    # Position nodes
    input_node.location = (-800, 0)
    output_node.location = (800, 0)

    # Base sphere
    sphere = node_group.nodes.new(
        "GeometryNodeMeshUVSphere"
    )  # Changed from MeshSphere to MeshUVSphere
    sphere.location = (-600, 0)
    sphere.inputs["Radius"].default_value = 0.3
    sphere.inputs["Segments"].default_value = 16
    sphere.inputs["Rings"].default_value = 8

    # Add subdivision
    subdiv = node_group.nodes.new("GeometryNodeSubdivisionSurface")
    subdiv.location = (-400, 0)
    subdiv.inputs["Level"].default_value = 2

    # Position for feature displacement
    position = node_group.nodes.new("GeometryNodeInputPosition")
    position.location = (-600, 200)

    # Separate XYZ
    separate_xyz = node_group.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.location = (-400, 200)

    # Noise texture for facial features
    noise = node_group.nodes.new("ShaderNodeTexNoise")
    noise.location = (-200, 200)
    noise.inputs["Scale"].default_value = 20.0
    noise.inputs["Detail"].default_value = 2.0

    # Set position for displacement
    displace = node_group.nodes.new(
        "GeometryNodeSetPosition"
    )  # Changed from Displace to SetPosition
    displace.location = (0, 0)

    # Vector math for displacement
    vector_math = node_group.nodes.new("ShaderNodeVectorMath")
    vector_math.location = (-100, 100)
    vector_math.operation = "MULTIPLY"
    vector_math.inputs[1].default_value = (0.02, 0.02, 0.02)  # Scale factor

    # Set position for final shaping
    set_position = node_group.nodes.new("GeometryNodeSetPosition")
    set_position.location = (200, 0)

    # Connect nodes
    node_group.links.new(sphere.outputs["Mesh"], subdiv.inputs["Mesh"])
    node_group.links.new(subdiv.outputs["Mesh"], displace.inputs["Geometry"])
    node_group.links.new(position.outputs["Position"], separate_xyz.inputs["Vector"])
    node_group.links.new(
        noise.outputs["Color"], vector_math.inputs[0]
    )  # Connect noise to vector math
    node_group.links.new(
        vector_math.outputs[0], displace.inputs["Offset"]
    )  # Vector math to displacement
    node_group.links.new(displace.outputs["Geometry"], set_position.inputs["Geometry"])
    node_group.links.new(
        set_position.outputs["Geometry"], output_node.inputs["Geometry"]
    )

    return node_group


def create_hand_nodes(node_group):
    """Create hand with separate objects approach - fallback to simple geometry"""

    # Add geometry socket to node group interface
    if "Geometry" not in [socket.name for socket in node_group.interface.items_tree]:
        node_group.interface.new_socket(
            name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
        )
        node_group.interface.new_socket(
            name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
        )

    # Input/Output nodes
    input_node = node_group.nodes.new("NodeGroupInput")
    output_node = node_group.nodes.new("NodeGroupOutput")

    # Position nodes
    input_node.location = (-400, 0)
    output_node.location = (400, 0)

    # Simple subdivision for smoother palm
    subdiv = node_group.nodes.new("GeometryNodeSubdivisionSurface")
    subdiv.location = (0, 0)
    subdiv.inputs["Level"].default_value = 2

    # Smooth shading
    smooth = node_group.nodes.new("GeometryNodeSetShadeSmooth")
    smooth.location = (200, 0)

    # Connect nodes - just enhance the palm since fingers are separate objects now
    node_group.links.new(input_node.outputs["Geometry"], subdiv.inputs["Mesh"])
    node_group.links.new(subdiv.outputs["Mesh"], smooth.inputs["Geometry"])
    node_group.links.new(smooth.outputs["Geometry"], output_node.inputs["Geometry"])

    return node_group


# End of file
