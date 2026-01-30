import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_edge__damage_group():
    group_name = "Edge Damage"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    displacement = nodes.new("NodeFrame")
    displacement.name = "Displacement"
    displacement.label = "Displacement"
    displacement.location = (440.0, 356.24078369140625)
    displacement.bl_label = "Frame"
    displacement.text = None
    displacement.shrink = True
    displacement.label_size = 20
    # Links for displacement

    edge_mask = nodes.new("NodeFrame")
    edge_mask.name = "Edge Mask"
    edge_mask.label = "Edge Mask"
    edge_mask.location = (-634.0, 350.0)
    edge_mask.bl_label = "Frame"
    edge_mask.text = None
    edge_mask.shrink = True
    edge_mask.label_size = 20
    # Links for edge_mask

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (1333.634765625, 306.16107177734375)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Offset
    set_position_002.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_002

    set_material = nodes.new("GeometryNodeSetMaterial")
    set_material.name = "Set Material"
    set_material.label = ""
    set_material.location = (1500.9774169921875, 302.95452880859375)
    set_material.bl_label = "Set Material"
    # Selection
    set_material.inputs[1].default_value = True
    # Links for set_material
    links.new(set_position_002.outputs[0], set_material.inputs[0])

    mesh_boolean = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean.name = "Mesh Boolean"
    mesh_boolean.label = ""
    mesh_boolean.location = (1662.586669921875, 454.41864013671875)
    mesh_boolean.bl_label = "Mesh Boolean"
    mesh_boolean.operation = "INTERSECT"
    mesh_boolean.solver = "EXACT"
    # Self Intersection
    mesh_boolean.inputs[2].default_value = False
    # Hole Tolerant
    mesh_boolean.inputs[3].default_value = False
    # Links for mesh_boolean
    links.new(set_material.outputs[0], mesh_boolean.inputs[1])

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1826.3115234375, 429.3497314453125)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output
    links.new(mesh_boolean.outputs[0], group_output.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (360.79913330078125, -76.08053588867188)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "MULTIPLY"
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_005.inputs[3].default_value = 1.0
    # Links for vector_math_005

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.label = ""
    vector_math_007.location = (541.62158203125, -168.92913818359375)
    vector_math_007.bl_label = "Vector Math"
    vector_math_007.operation = "MULTIPLY"
    # Vector
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_007.inputs[3].default_value = 1.0
    # Links for vector_math_007
    links.new(vector_math_005.outputs[0], vector_math_007.inputs[0])

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (709.64404296875, -74.24087524414062)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "ADD"
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006
    links.new(vector_math_006.outputs[0], set_position_002.inputs[2])
    links.new(vector_math_007.outputs[0], vector_math_006.inputs[1])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (543.2315673828125, -87.04019165039062)
    position_002.bl_label = "Position"
    # Links for position_002
    links.new(position_002.outputs[0], vector_math_006.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (37.017578125, -44.4234619140625)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (837.599853515625, -41.0)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001
    links.new(reroute.outputs[0], reroute_001.inputs[0])
    links.new(reroute_001.outputs[0], set_position_002.inputs[0])

    normal_002 = nodes.new("GeometryNodeInputNormal")
    normal_002.name = "Normal.002"
    normal_002.label = ""
    normal_002.location = (186.5849609375, -52.5479736328125)
    normal_002.bl_label = "Normal"
    normal_002.legacy_corner_normals = True
    # Links for normal_002
    links.new(normal_002.outputs[0], vector_math_005.inputs[0])

    noise_strength = nodes.new("ShaderNodeValue")
    noise_strength.name = "Noise Strength"
    noise_strength.label = "Noise Strength"
    noise_strength.location = (363.1832275390625, -278.787841796875)
    noise_strength.bl_label = "Value"
    # Links for noise_strength
    links.new(noise_strength.outputs[0], vector_math_007.inputs[1])

    musgrave_texture_002 = nodes.new("ShaderNodeTexNoise")
    musgrave_texture_002.name = "Musgrave Texture.002"
    musgrave_texture_002.label = ""
    musgrave_texture_002.location = (185.91204833984375, -107.90447998046875)
    musgrave_texture_002.bl_label = "Noise Texture"
    musgrave_texture_002.noise_dimensions = "3D"
    musgrave_texture_002.noise_type = "RIDGED_MULTIFRACTAL"
    musgrave_texture_002.normalize = False
    # Vector
    musgrave_texture_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    # W
    musgrave_texture_002.inputs[1].default_value = 0.0
    # Detail
    musgrave_texture_002.inputs[3].default_value = 1.0
    # Roughness
    musgrave_texture_002.inputs[4].default_value = 0.25
    # Lacunarity
    musgrave_texture_002.inputs[5].default_value = 2.0
    # Offset
    musgrave_texture_002.inputs[6].default_value = 0.0
    # Gain
    musgrave_texture_002.inputs[7].default_value = 1.0
    # Distortion
    musgrave_texture_002.inputs[8].default_value = 0.0
    # Links for musgrave_texture_002
    links.new(musgrave_texture_002.outputs[0], vector_math_005.inputs[1])

    subdivision_surface_001 = nodes.new("GeometryNodeSubdivisionSurface")
    subdivision_surface_001.name = "Subdivision Surface.001"
    subdivision_surface_001.label = ""
    subdivision_surface_001.location = (881.878662109375, -35.53021240234375)
    subdivision_surface_001.bl_label = "Subdivision Surface"
    # Level
    subdivision_surface_001.inputs[1].default_value = 1
    # Edge Crease
    subdivision_surface_001.inputs[2].default_value = 0.0
    # Vertex Crease
    subdivision_surface_001.inputs[3].default_value = 0.0
    # Limit Surface
    subdivision_surface_001.inputs[4].default_value = False
    # UV Smooth
    subdivision_surface_001.inputs[5].default_value = "Keep Boundaries"
    # Boundary Smooth
    subdivision_surface_001.inputs[6].default_value = "All"
    # Links for subdivision_surface_001
    links.new(subdivision_surface_001.outputs[0], reroute.inputs[0])

    edge_offset = nodes.new("ShaderNodeValue")
    edge_offset.name = "Edge Offset"
    edge_offset.label = "Edge Offset"
    edge_offset.location = (30.46038818359375, -258.6700134277344)
    edge_offset.bl_label = "Value"
    # Links for edge_offset

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (546.5501098632812, -60.568084716796875)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position

    subdivide_mesh = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh.name = "Subdivide Mesh"
    subdivide_mesh.label = ""
    subdivide_mesh.location = (715.5108642578125, -88.53390502929688)
    subdivide_mesh.bl_label = "Subdivide Mesh"
    # Links for subdivide_mesh
    links.new(subdivide_mesh.outputs[0], subdivision_surface_001.inputs[0])
    links.new(set_position.outputs[0], subdivide_mesh.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.label = ""
    normal.location = (30.41864013671875, -181.0032958984375)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = True
    # Links for normal

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (217.27001953125, -206.274169921875)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "MULTIPLY"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(normal.outputs[0], vector_math.inputs[0])
    links.new(edge_offset.outputs[0], vector_math.inputs[1])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (214.748046875, -138.260986328125)
    position.bl_label = "Position"
    # Links for position

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (391.88665771484375, -162.267333984375)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "ADD"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(position.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math.outputs[0], vector_math_001.inputs[1])
    links.new(vector_math_001.outputs[0], set_position.inputs[2])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-784.0969848632812, 394.5766296386719)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], set_position.inputs[0])
    links.new(group_input.outputs[0], mesh_boolean.inputs[1])

    integer = nodes.new("FunctionNodeInputInt")
    integer.name = "Integer"
    integer.label = ""
    integer.location = (543.368896484375, -278.7611389160156)
    integer.bl_label = "Integer"
    integer.integer = 2
    # Links for integer

    noise_scale = nodes.new("ShaderNodeValue")
    noise_scale.name = "Noise Scale"
    noise_scale.label = "Noise Scale"
    noise_scale.location = (29.98760986328125, -214.2939910888672)
    noise_scale.bl_label = "Value"
    # Links for noise_scale
    links.new(noise_scale.outputs[0], musgrave_texture_002.inputs[2])

    clamp = nodes.new("ShaderNodeClamp")
    clamp.name = "Clamp"
    clamp.label = ""
    clamp.location = (690.5108642578125, -88.53390502929688)
    clamp.bl_label = "Clamp"
    clamp.clamp_type = "MINMAX"
    # Min
    clamp.inputs[1].default_value = 0.0
    # Max
    clamp.inputs[2].default_value = 11.0
    # Links for clamp
    links.new(integer.outputs[0], clamp.inputs[0])
    links.new(clamp.outputs[0], subdivide_mesh.inputs[1])

    auto_layout_nodes(group)
    return group