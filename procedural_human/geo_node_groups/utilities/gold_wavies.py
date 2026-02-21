import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes

@geo_node_group
def create_gold__wavies_group():
    group_name = "Gold Wavies"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Instances", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1500.0, 300.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.label = ""
    curve_line.location = (-620.0, 220.0)
    curve_line.bl_label = "Curve Line"
    curve_line.mode = "POINTS"
    # Start
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    # End
    curve_line.inputs[1].default_value = Vector((0.009999999776482582, 0.0, 0.0))
    # Direction
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    # Length
    curve_line.inputs[3].default_value = 1.0
    # Links for curve_line

    points_to_vertices = nodes.new("GeometryNodePointsToVertices")
    points_to_vertices.name = "Points to Vertices"
    points_to_vertices.label = ""
    points_to_vertices.location = (-300.0, 220.0)
    points_to_vertices.bl_label = "Points to Vertices"
    # Selection
    points_to_vertices.inputs[1].default_value = True
    # Links for points_to_vertices

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (-460.0, 220.0)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "COUNT"
    # Count
    curve_to_points.inputs[1].default_value = 18
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points
    links.new(curve_to_points.outputs[0], points_to_vertices.inputs[0])
    links.new(curve_line.outputs[0], curve_to_points.inputs[0])

    extrude_mesh_001 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.name = "Extrude Mesh.001"
    extrude_mesh_001.label = ""
    extrude_mesh_001.location = (100.0, 220.0)
    extrude_mesh_001.bl_label = "Extrude Mesh"
    extrude_mesh_001.mode = "VERTICES"
    # Offset Scale
    extrude_mesh_001.inputs[3].default_value = 0.0010000000474974513
    # Individual
    extrude_mesh_001.inputs[4].default_value = True
    # Links for extrude_mesh_001

    repeat_input = nodes.new("GeometryNodeRepeatInput")
    repeat_input.name = "Repeat Input"
    repeat_input.label = ""
    repeat_input.location = (-120.0, 220.0)
    repeat_input.bl_label = "Repeat Input"
    # Iterations
    repeat_input.inputs[0].default_value = 50
    # Top
    repeat_input.inputs[2].default_value = True
    # Links for repeat_input
    links.new(points_to_vertices.outputs[0], repeat_input.inputs[1])
    links.new(repeat_input.outputs[2], extrude_mesh_001.inputs[1])
    links.new(repeat_input.outputs[1], extrude_mesh_001.inputs[0])

    repeat_output = nodes.new("GeometryNodeRepeatOutput")
    repeat_output.name = "Repeat Output"
    repeat_output.label = ""
    repeat_output.location = (260.0, 220.0)
    repeat_output.bl_label = "Repeat Output"
    repeat_output.active_index = 1
    repeat_output.inspection_index = 0
    # Links for repeat_output
    links.new(extrude_mesh_001.outputs[1], repeat_output.inputs[1])
    links.new(extrude_mesh_001.outputs[0], repeat_output.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (-300.0, 60.0)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = True
    # Vector
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Scale
    noise_texture.inputs[2].default_value = 104.69999694824219
    # Detail
    noise_texture.inputs[3].default_value = 0.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Offset
    noise_texture.inputs[6].default_value = 0.0
    # Gain
    noise_texture.inputs[7].default_value = 1.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0
    # Links for noise_texture

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (-120.0, 60.0)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT_VECTOR"
    # Value
    map_range.inputs[0].default_value = 1.0
    # From Min
    map_range.inputs[1].default_value = 0.0
    # From Max
    map_range.inputs[2].default_value = 1.0
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0
    # Steps
    map_range.inputs[5].default_value = 4.0
    # From Min
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range.inputs[9].default_value = [-1.0, -1.0, 0.0]
    # To Max
    map_range.inputs[10].default_value = [1.0, 1.0, 0.05000000074505806]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(map_range.outputs[1], extrude_mesh_001.inputs[2])
    links.new(noise_texture.outputs[1], map_range.inputs[6])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (420.0, 220.0)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Selection
    mesh_to_curve_001.inputs[1].default_value = True
    # Links for mesh_to_curve_001
    links.new(repeat_output.outputs[0], mesh_to_curve_001.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (780.0, 200.0)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False
    # Links for curve_to_mesh_001

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (780.0, 60.0)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Resolution
    curve_circle.inputs[0].default_value = 6
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle.inputs[4].default_value = 0.0003000000142492354
    # Links for curve_circle
    links.new(curve_circle.outputs[0], curve_to_mesh_001.inputs[1])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.label = ""
    spline_parameter.location = (420.0, -40.0)
    spline_parameter.bl_label = "Spline Parameter"
    # Links for spline_parameter

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (420.0, 100.0)
    math_004.bl_label = "Math"
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    # Value
    math_004.inputs[0].default_value = 1.0
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(spline_parameter.outputs[0], math_004.inputs[1])
    links.new(math_004.outputs[0], curve_to_mesh_001.inputs[2])

    repeat_input_001 = nodes.new("GeometryNodeRepeatInput")
    repeat_input_001.name = "Repeat Input.001"
    repeat_input_001.label = ""
    repeat_input_001.location = (-1080.0, 360.0)
    repeat_input_001.bl_label = "Repeat Input"
    # Iterations
    repeat_input_001.inputs[0].default_value = 20
    # Links for repeat_input_001

    repeat_output_001 = nodes.new("GeometryNodeRepeatOutput")
    repeat_output_001.name = "Repeat Output.001"
    repeat_output_001.label = ""
    repeat_output_001.location = (1320.0, 300.0)
    repeat_output_001.bl_label = "Repeat Output"
    repeat_output_001.active_index = 0
    repeat_output_001.inspection_index = 19
    # Links for repeat_output_001
    links.new(repeat_output_001.outputs[0], group_output.inputs[0])

    index_switch = nodes.new("GeometryNodeIndexSwitch")
    index_switch.name = "Index Switch"
    index_switch.label = ""
    index_switch.location = (-900.0, 360.0)
    index_switch.bl_label = "Index Switch"
    index_switch.data_type = "FLOAT"
    # 0
    index_switch.inputs[1].default_value = 1.5700000524520874
    # 1
    index_switch.inputs[2].default_value = 0.3499999940395355
    # 2
    index_switch.inputs[3].default_value = 1.0099999904632568
    # 3
    index_switch.inputs[4].default_value = 1.2999999523162842
    # 4
    index_switch.inputs[5].default_value = 1.2999999523162842
    # 5
    index_switch.inputs[6].default_value = 2.569999933242798
    # 6
    index_switch.inputs[7].default_value = 3.6499998569488525
    # 7
    index_switch.inputs[8].default_value = 4.029999732971191
    # 8
    index_switch.inputs[9].default_value = 4.599999904632568
    # 9
    index_switch.inputs[10].default_value = 6.239999771118164
    # 10
    index_switch.inputs[11].default_value = 10.100000381469727
    # 11
    index_switch.inputs[12].default_value = 10.270000457763672
    # 12
    index_switch.inputs[13].default_value = 10.369999885559082
    # 13
    index_switch.inputs[14].default_value = 10.670000076293945
    # 14
    index_switch.inputs[15].default_value = 10.720000267028809
    # 15
    index_switch.inputs[16].default_value = 10.890000343322754
    # 16
    index_switch.inputs[17].default_value = 11.130000114440918
    # 17
    index_switch.inputs[18].default_value = 11.289999961853027
    # 18
    index_switch.inputs[19].default_value = 11.390000343322754
    # 19
    index_switch.inputs[20].default_value = 11.800000190734863
    # Links for index_switch
    links.new(repeat_input_001.outputs[0], index_switch.inputs[0])
    links.new(index_switch.outputs[0], noise_texture.inputs[1])

    geometry_to_instance = nodes.new("GeometryNodeGeometryToInstance")
    geometry_to_instance.name = "Geometry to Instance"
    geometry_to_instance.label = ""
    geometry_to_instance.location = (940.0, 200.0)
    geometry_to_instance.bl_label = "Geometry to Instance"
    # Links for geometry_to_instance
    links.new(curve_to_mesh_001.outputs[0], geometry_to_instance.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.label = ""
    join_geometry_006.location = (1140.0, 300.0)
    join_geometry_006.bl_label = "Join Geometry"
    # Links for join_geometry_006
    links.new(join_geometry_006.outputs[0], repeat_output_001.inputs[0])
    links.new(repeat_input_001.outputs[1], join_geometry_006.inputs[0])
    links.new(geometry_to_instance.outputs[0], join_geometry_006.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (600.0, 200.0)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Count"
    # Count
    resample_curve.inputs[3].default_value = 30
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve
    links.new(resample_curve.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(mesh_to_curve_001.outputs[0], resample_curve.inputs[0])

    auto_layout_nodes(group)
    return group
