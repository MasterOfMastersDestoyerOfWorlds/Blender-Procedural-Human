import bpy
import math
from procedural_human.utils.node_layout import auto_layout_nodes

def create_dual_radial_loft_group(name: str = "Dual Radial Loft"):
    """
    Creates a node group for Dual Radial Surface Synthesis via Curve Lofting.
    
    Implements the algorithm:
    1. Ribbon Generation: Extrudes input curves (X-profile and Y-profile) to create raycast targets.
    2. Raycasting: Scans the ribbons from the central axis to determine Rx(z) and Ry(z).
    3. Elliptical Synthesis: Fuses Rx and Ry using the polar ellipse equation.
    
    Input Curves must be:
    - X Profile: Lying on the XZ plane (Y=0).
    - Y Profile: Lying on the YZ plane (X=0).
    """
    group_name = name
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    
    # --- Interface ---
    # Geometry input for chaining (stacking)
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    
    group.interface.new_socket(name="Curve X (Front)", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Curve Y (Side)", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Resolution V", in_out="INPUT", socket_type="NodeSocketInt").default_value = 64
    group.interface.new_socket(name="Resolution U", in_out="INPUT", socket_type="NodeSocketInt").default_value = 32
    # Height control is derived from curve bounding box in a real scenario, 
    # but here we provide explicit control or default to 1.0
    group.interface.new_socket(name="Height", in_out="INPUT", socket_type="NodeSocketFloat").default_value = 1.0
    
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    input_node = group.nodes.new("NodeGroupInput")
    
    # =================================================================================
    # Phase I: Ribbon Generation (The Targets)
    # =================================================================================
    
    # -- Ribbon X (Extrude along Y) --
    # Ensure Curve to Mesh first (in case it's just a wire)
    c2m_x = group.nodes.new("GeometryNodeCurveToMesh")
    group.links.new(input_node.outputs["Curve X (Front)"], c2m_x.inputs["Curve"])
    
    extrude_x_pos = group.nodes.new("GeometryNodeExtrudeMesh")
    extrude_x_pos.inputs["Offset Scale"].default_value = 100.0
    extrude_x_pos.inputs["Offset"].default_value = (0, 1, 0) # Extrude +Y
    group.links.new(c2m_x.outputs["Mesh"], extrude_x_pos.inputs["Mesh"])
    
    extrude_x_neg = group.nodes.new("GeometryNodeExtrudeMesh")
    extrude_x_neg.inputs["Offset Scale"].default_value = 100.0
    extrude_x_neg.inputs["Offset"].default_value = (0, -1, 0) # Extrude -Y
    group.links.new(c2m_x.outputs["Mesh"], extrude_x_neg.inputs["Mesh"])
    
    join_ribbon_x = group.nodes.new("GeometryNodeJoinGeometry")
    group.links.new(extrude_x_pos.outputs["Mesh"], join_ribbon_x.inputs["Geometry"])
    group.links.new(extrude_x_neg.outputs["Mesh"], join_ribbon_x.inputs["Geometry"])
    
    # -- Ribbon Y (Extrude along X) --
    c2m_y = group.nodes.new("GeometryNodeCurveToMesh")
    group.links.new(input_node.outputs["Curve Y (Side)"], c2m_y.inputs["Curve"])
    
    extrude_y_pos = group.nodes.new("GeometryNodeExtrudeMesh")
    extrude_y_pos.inputs["Offset Scale"].default_value = 100.0
    extrude_y_pos.inputs["Offset"].default_value = (1, 0, 0) # Extrude +X
    group.links.new(c2m_y.outputs["Mesh"], extrude_y_pos.inputs["Mesh"])
    
    extrude_y_neg = group.nodes.new("GeometryNodeExtrudeMesh")
    extrude_y_neg.inputs["Offset Scale"].default_value = 100.0
    extrude_y_neg.inputs["Offset"].default_value = (-1, 0, 0) # Extrude -X
    group.links.new(c2m_y.outputs["Mesh"], extrude_y_neg.inputs["Mesh"])
    
    join_ribbon_y = group.nodes.new("GeometryNodeJoinGeometry")
    group.links.new(extrude_y_pos.outputs["Mesh"], join_ribbon_y.inputs["Geometry"])
    group.links.new(extrude_y_neg.outputs["Mesh"], join_ribbon_y.inputs["Geometry"])

    # =================================================================================
    # Phase II: Base Topology Generation (The Canvas)
    # =================================================================================
    
    # Stacking Logic (Find Top of Previous Geometry)
    bbox = group.nodes.new("GeometryNodeBoundBox")
    group.links.new(input_node.outputs["Geometry"], bbox.inputs["Geometry"])
    
    sep_max = group.nodes.new("ShaderNodeSeparateXYZ")
    group.links.new(bbox.outputs["Max"], sep_max.inputs["Vector"])
    offset_z = sep_max.outputs["Z"] # This determines the start Z
    
    # Create Spine Line
    spine = group.nodes.new("GeometryNodeMeshLine")
    # spine.mode = 'END_POINTS' - Removed to avoid socket issues
    # Using Default 'OFFSET' mode which is robust
    
    # Start Location = (0, 0, offset_z)
    start_loc = group.nodes.new("ShaderNodeCombineXYZ")
    group.links.new(offset_z, start_loc.inputs["Z"])
    group.links.new(start_loc.outputs["Vector"], spine.inputs["Start Location"])
    
    # Offset = (0, 0, Height)
    offset_vec = group.nodes.new("ShaderNodeCombineXYZ")
    group.links.new(input_node.outputs["Height"], offset_vec.inputs["Z"])
    group.links.new(offset_vec.outputs["Vector"], spine.inputs["Offset"])
    
    group.links.new(input_node.outputs["Resolution V"], spine.inputs["Count"])
    
    # Create Cylinder (Loft Source)
    spine_to_curve = group.nodes.new("GeometryNodeMeshToCurve")
    group.links.new(spine.outputs["Mesh"], spine_to_curve.inputs["Mesh"])
    
    profile_circle = group.nodes.new("GeometryNodeCurvePrimitiveCircle")
    profile_circle.inputs["Radius"].default_value = 1.0 # Unit radius for easy math
    group.links.new(input_node.outputs["Resolution U"], profile_circle.inputs["Resolution"])
    
    cylinder = group.nodes.new("GeometryNodeCurveToMesh")
    group.links.new(spine_to_curve.outputs["Curve"], cylinder.inputs["Curve"])
    group.links.new(profile_circle.outputs["Curve"], cylinder.inputs["Profile Curve"])
    
    # =================================================================================
    # Phase III: The Interrogation Engine (Raycasting)
    # =================================================================================
    
    # We need to perform calculations on the Cylinder's points
    # 1. Get Current Position
    pos = group.nodes.new("GeometryNodeInputPosition")
    sep_pos = group.nodes.new("ShaderNodeSeparateXYZ")
    group.links.new(pos.outputs["Position"], sep_pos.inputs["Vector"])
    
    # 2. Define Ray Source (Center of spine at current Z)
    ray_source = group.nodes.new("ShaderNodeCombineXYZ")
    group.links.new(sep_pos.outputs["Z"], ray_source.inputs["Z"]) # (0, 0, z)
    
    # 3. Raycast X (Direction 1,0,0)
    ray_x = group.nodes.new("GeometryNodeRaycast")
    ray_x.label = "Measure Rx"
    ray_x.inputs["Ray Direction"].default_value = (1, 0, 0)
    group.links.new(join_ribbon_x.outputs["Geometry"], ray_x.inputs["Target Geometry"])
    group.links.new(ray_source.outputs["Vector"], ray_x.inputs["Source Position"])
    
    # 4. Raycast Y (Direction 0,1,0)
    ray_y = group.nodes.new("GeometryNodeRaycast")
    ray_y.label = "Measure Ry"
    ray_y.inputs["Ray Direction"].default_value = (0, 1, 0)
    group.links.new(join_ribbon_y.outputs["Geometry"], ray_y.inputs["Target Geometry"])
    group.links.new(ray_source.outputs["Vector"], ray_y.inputs["Source Position"])
    
    # 5. Extract Distances (Rx, Ry)
    # Use Hit Distance. If not hit, we might want 0 or keep 1. Let's assume 0 for silhouette fidelity.
    rx = ray_x.outputs["Hit Distance"]
    ry = ray_y.outputs["Hit Distance"]

    # =================================================================================
    # Phase IV: Elliptical Synthesis
    # Formula: R = (Rx * Ry) / sqrt( (Ry * cos t)^2 + (Rx * sin t)^2 )
    # =================================================================================
    
    # Calculate Theta (Angle)
    theta = group.nodes.new("ShaderNodeMath")
    theta.operation = 'ARCTAN2'
    group.links.new(sep_pos.outputs["Y"], theta.inputs[0])
    group.links.new(sep_pos.outputs["X"], theta.inputs[1])
    
    cos_t = group.nodes.new("ShaderNodeMath")
    cos_t.operation = 'COSINE'
    group.links.new(theta.outputs["Value"], cos_t.inputs[0])
    
    sin_t = group.nodes.new("ShaderNodeMath")
    sin_t.operation = 'SINE'
    group.links.new(theta.outputs["Value"], sin_t.inputs[0])
    
    # Denominator Term A: (Ry * cos t)^2
    term_a_mult = group.nodes.new("ShaderNodeMath")
    term_a_mult.operation = 'MULTIPLY'
    group.links.new(ry, term_a_mult.inputs[0])
    group.links.new(cos_t.outputs["Value"], term_a_mult.inputs[1])
    
    term_a_sq = group.nodes.new("ShaderNodeMath")
    term_a_sq.operation = 'POWER'
    term_a_sq.inputs[1].default_value = 2.0
    group.links.new(term_a_mult.outputs["Value"], term_a_sq.inputs[0])
    
    # Denominator Term B: (Rx * sin t)^2
    term_b_mult = group.nodes.new("ShaderNodeMath")
    term_b_mult.operation = 'MULTIPLY'
    group.links.new(rx, term_b_mult.inputs[0])
    group.links.new(sin_t.outputs["Value"], term_b_mult.inputs[1])
    
    term_b_sq = group.nodes.new("ShaderNodeMath")
    term_b_sq.operation = 'POWER'
    term_b_sq.inputs[1].default_value = 2.0
    group.links.new(term_b_mult.outputs["Value"], term_b_sq.inputs[0])
    
    # Denominator Sqrt
    denom_add = group.nodes.new("ShaderNodeMath")
    denom_add.operation = 'ADD'
    group.links.new(term_a_sq.outputs["Value"], denom_add.inputs[0])
    group.links.new(term_b_sq.outputs["Value"], denom_add.inputs[1])
    
    # Safety: Add Epsilon to prevent div by zero
    denom_safe = group.nodes.new("ShaderNodeMath")
    denom_safe.operation = 'ADD'
    denom_safe.inputs[1].default_value = 0.0001
    group.links.new(denom_add.outputs["Value"], denom_safe.inputs[0])
    
    denom_sqrt = group.nodes.new("ShaderNodeMath")
    denom_sqrt.operation = 'SQRT'
    group.links.new(denom_safe.outputs["Value"], denom_sqrt.inputs[0])
    
    # Numerator: Rx * Ry
    num_mult = group.nodes.new("ShaderNodeMath")
    num_mult.operation = 'MULTIPLY'
    group.links.new(rx, num_mult.inputs[0])
    group.links.new(ry, num_mult.inputs[1])
    
    # Final Radius R
    final_r = group.nodes.new("ShaderNodeMath")
    final_r.operation = 'DIVIDE'
    group.links.new(num_mult.outputs["Value"], final_r.inputs[0])
    group.links.new(denom_sqrt.outputs["Value"], final_r.inputs[1])
    
    # =================================================================================
    # Phase V: Apply Deformation
    # =================================================================================
    
    # Calculate New Position Vector
    # X = R * cos t
    new_x = group.nodes.new("ShaderNodeMath")
    new_x.operation = 'MULTIPLY'
    group.links.new(final_r.outputs["Value"], new_x.inputs[0])
    group.links.new(cos_t.outputs["Value"], new_x.inputs[1])
    
    # Y = R * sin t
    new_y = group.nodes.new("ShaderNodeMath")
    new_y.operation = 'MULTIPLY'
    group.links.new(final_r.outputs["Value"], new_y.inputs[0])
    group.links.new(sin_t.outputs["Value"], new_y.inputs[1])
    
    new_pos = group.nodes.new("ShaderNodeCombineXYZ")
    group.links.new(new_x.outputs["Value"], new_pos.inputs["X"])
    group.links.new(new_y.outputs["Value"], new_pos.inputs["Y"])
    group.links.new(sep_pos.outputs["Z"], new_pos.inputs["Z"]) # Keep original Z (which includes offset_z)
    
    set_pos = group.nodes.new("GeometryNodeSetPosition")
    group.links.new(cylinder.outputs["Mesh"], set_pos.inputs["Geometry"])
    group.links.new(new_pos.outputs["Vector"], set_pos.inputs["Position"])
    
    # Join with Previous Geometry
    join_output = group.nodes.new("GeometryNodeJoinGeometry")
    group.links.new(input_node.outputs["Geometry"], join_output.inputs["Geometry"])
    group.links.new(set_pos.outputs["Geometry"], join_output.inputs["Geometry"])
    
    # Output 
    output_node = group.nodes.new("NodeGroupOutput")
    group.links.new(join_output.outputs["Geometry"], output_node.inputs["Geometry"])
    
    auto_layout_nodes(group)
    return group
