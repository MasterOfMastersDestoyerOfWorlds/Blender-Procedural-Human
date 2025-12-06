import bpy
import math
from procedural_human.utils.node_layout import auto_layout_nodes

def create_dual_radial_loft_group(name: str = "Dual Radial Loft"):
    """
    Creates a Geometry Node group for Spherical/Elliptical Lofting.
    
    Logic:
    Instead of linearly mixing positions (which creates flat/ruled surfaces),
    this uses Trigonometric Interpolation:
    
    X_final = Radius_Curve1 * cos(t * pi/2)
    Z_final = Radius_Curve2 * sin(t * pi/2)
    Y_final = Mix(Y1, Y2, t)
    
    This naturally forms spheres, ellipsoids, and bubble-like volumes
    from two orthogonal boundary loops.
    """
    group_name = name
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
    
    # --- Interface ---
    group.interface.new_socket(name="Curve X (Front)", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Curve Y (Side)", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Resolution V", in_out="INPUT", socket_type="NodeSocketInt").default_value = 64
    group.interface.new_socket(name="Resolution U", in_out="INPUT", socket_type="NodeSocketInt").default_value = 32
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    input_node = group.nodes.new("NodeGroupInput")
    output_node = group.nodes.new("NodeGroupOutput")

    # 1. Domain Generation (The Grid)
    # X = U (Curve Parameter), Y = V (Arc Interpolation 0-1)
    grid = group.nodes.new("GeometryNodeMeshGrid")
    grid.inputs["Size X"].default_value = 1.0
    grid.inputs["Size Y"].default_value = 1.0
    # Center grid at 0.5, 0.5 so UVs range 0-1
    # Actually Mesh Grid centers at 0. But we only need vertices, we will overwrite positions.
    # We rely on the internal UV mapping or position relative to corner?
    # Easier to just use Mesh Grid, then read Position X/Y as attributes if we offset it, 
    # but Mesh Grid generates -0.5 to 0.5 by default. 
    # Let's map it to 0-1 for easier math.
    
    group.links.new(input_node.outputs["Resolution U"], grid.inputs["Vertices X"])
    group.links.new(input_node.outputs["Resolution V"], grid.inputs["Vertices Y"])
    
    # Map Grid range (-0.5 to 0.5) to (0 to 1) for U/V calculations
    grid_pos = group.nodes.new("GeometryNodeInputPosition")
    
    map_range_u = group.nodes.new("ShaderNodeMapRange")
    map_range_u.label = "Map U (0-1)"
    map_range_u.inputs["From Min"].default_value = -0.5
    map_range_u.inputs["From Max"].default_value = 0.5
    map_range_u.inputs["To Min"].default_value = 0.0
    map_range_u.inputs["To Max"].default_value = 1.0
    
    map_range_v = group.nodes.new("ShaderNodeMapRange")
    map_range_v.label = "Map V (0-1)"
    map_range_v.inputs["From Min"].default_value = -0.5
    map_range_v.inputs["From Max"].default_value = 0.5
    map_range_v.inputs["To Min"].default_value = 0.0
    map_range_v.inputs["To Max"].default_value = 1.0
    
    sep_grid_pos = group.nodes.new("ShaderNodeSeparateXYZ")
    group.links.new(grid_pos.outputs["Position"], sep_grid_pos.inputs["Vector"])
    group.links.new(sep_grid_pos.outputs["X"], map_range_u.inputs["Value"])
    group.links.new(sep_grid_pos.outputs["Y"], map_range_v.inputs["Value"])

    u_param = map_range_u.outputs["Result"]
    v_param = map_range_v.outputs["Result"]

    # 2. Sample Curves
    # Curve X (Front) - Provides X radius and Y height
    sample_x = group.nodes.new("GeometryNodeSampleCurve")
    sample_x.data_type = 'FLOAT_VECTOR' # Position
    sample_x.mode = 'FACTOR'
    sample_x.use_all_curves = True
    group.links.new(input_node.outputs["Curve X (Front)"], sample_x.inputs["Curves"])
    group.links.new(u_param, sample_x.inputs["Factor"])
    
    # Curve Y (Side) - Provides Z radius (and Y height for blending)
    sample_y = group.nodes.new("GeometryNodeSampleCurve")
    sample_y.data_type = 'FLOAT_VECTOR'
    sample_y.mode = 'FACTOR'
    sample_y.use_all_curves = True
    group.links.new(input_node.outputs["Curve Y (Side)"], sample_y.inputs["Curves"])
    group.links.new(u_param, sample_y.inputs["Factor"])

    # Break Vectors
    sep_x = group.nodes.new("ShaderNodeSeparateXYZ")
    group.links.new(sample_x.outputs["Position"], sep_x.inputs["Vector"])
    
    sep_y = group.nodes.new("ShaderNodeSeparateXYZ")
    group.links.new(sample_y.outputs["Position"], sep_y.inputs["Vector"])

    # 3. Trigonometric Interpolation (The Bulge Math)
    # We rotate 90 degrees (pi/2) from Plane X (0 rad) to Plane Z (pi/2 rad)
    
    # Angle = V * (pi/2)
    angle_math = group.nodes.new("ShaderNodeMath")
    angle_math.operation = 'MULTIPLY'
    angle_math.inputs[1].default_value = 1.570796 # pi/2
    group.links.new(v_param, angle_math.inputs[0])
    theta = angle_math.outputs["Value"]
    
    # Cos(theta) -> Scale for X component
    cos_node = group.nodes.new("ShaderNodeMath")
    cos_node.operation = 'COSINE'
    group.links.new(theta, cos_node.inputs[0])
    
    # Sin(theta) -> Scale for Z component
    sin_node = group.nodes.new("ShaderNodeMath")
    sin_node.operation = 'SINE'
    group.links.new(theta, sin_node.inputs[0])
    
    # 4. Construct Final Coordinates
    
    # Final X = Radius_From_CurveX * Cos(theta)
    # We take X from Curve X as the radius.
    calc_x = group.nodes.new("ShaderNodeMath")
    calc_x.operation = 'MULTIPLY'
    group.links.new(sep_x.outputs["X"], calc_x.inputs[0])
    group.links.new(cos_node.outputs["Value"], calc_x.inputs[1])
    
    # Final Z = Radius_From_CurveY * Sin(theta)
    # We take Z (or X depending on orientation) from Curve Y. 
    # Usually side profiles are drawn in XY or ZY. 
    # If Curve Y is drawn in ZY, we take Z. If drawn in XY (local), we take X.
    # To be safe for "Side/Top" usually implying Z-depth, we'll take Z.
    # (If the user draws both curves in XY plane and rotates the object, they might need to verify this socket).
    # Assuming user follows "ZY plane" instruction from prompt:
    calc_z = group.nodes.new("ShaderNodeMath")
    calc_z.operation = 'MULTIPLY'
    group.links.new(sep_y.outputs["Z"], calc_z.inputs[0]) 
    group.links.new(sin_node.outputs["Value"], calc_z.inputs[1])
    
    # Final Y = Mix(CurveX_Y, CurveY_Y, V)
    # Linearly blends height to handle slight mismatches between the two curves
    mix_y = group.nodes.new("ShaderNodeMix")
    mix_y.data_type = 'FLOAT'
    group.links.new(v_param, mix_y.inputs["Factor"])
    group.links.new(sep_x.outputs["Y"], mix_y.inputs["A"])
    group.links.new(sep_y.outputs["Y"], mix_y.inputs["B"])
    
    # Combine
    comb_final = group.nodes.new("ShaderNodeCombineXYZ")
    group.links.new(calc_x.outputs["Value"], comb_final.inputs["X"])
    group.links.new(mix_y.outputs["Result"], comb_final.inputs["Y"])
    group.links.new(calc_z.outputs["Value"], comb_final.inputs["Z"])
    
    # 5. Output Geometry
    set_pos = group.nodes.new("GeometryNodeSetPosition")
    group.links.new(grid.outputs["Mesh"], set_pos.inputs["Geometry"])
    group.links.new(comb_final.outputs["Vector"], set_pos.inputs["Position"])
    
    # Optional: Merge by distance to seal the poles
    merge = group.nodes.new("GeometryNodeMergeByDistance")
    merge.inputs["Distance"].default_value = 0.001
    group.links.new(set_pos.outputs["Geometry"], merge.inputs["Geometry"])

    group.links.new(merge.outputs["Geometry"], output_node.inputs["Geometry"])
    
    # Auto Layout
    try:
        auto_layout_nodes(group)
    except Exception:
        pass # Fallback if utils not available in context
        
    return group