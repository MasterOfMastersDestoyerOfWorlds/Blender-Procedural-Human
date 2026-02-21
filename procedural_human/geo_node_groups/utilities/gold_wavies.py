import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group

@geo_node_group
def create_gold__wavies_group():
    group_name = "Gold Wavies"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Instances", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.mode = "POINTS"
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    curve_line.inputs[1].default_value = Vector((0.009999999776482582, 0.0, 0.0))
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    curve_line.inputs[3].default_value = 1.0

    points_to_vertices = nodes.new("GeometryNodePointsToVertices")
    points_to_vertices.inputs[1].default_value = True

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.mode = "COUNT"
    curve_to_points.inputs[1].default_value = 18
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    links.new(curve_to_points.outputs[0], points_to_vertices.inputs[0])
    links.new(curve_line.outputs[0], curve_to_points.inputs[0])

    extrude_mesh_001 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.mode = "VERTICES"
    extrude_mesh_001.inputs[3].default_value = 0.0010000000474974513
    extrude_mesh_001.inputs[4].default_value = True

    repeat_input = nodes.new("GeometryNodeRepeatInput")
    repeat_input.inputs[0].default_value = 50
    links.new(points_to_vertices.outputs[0], repeat_input.inputs[1])
    links.new(repeat_input.outputs[1], extrude_mesh_001.inputs[0])

    repeat_output = nodes.new("GeometryNodeRepeatOutput")
    repeat_output.active_index = 1
    repeat_output.inspection_index = 0
    links.new(extrude_mesh_001.outputs[1], repeat_output.inputs[1])
    links.new(extrude_mesh_001.outputs[0], repeat_output.inputs[0])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = True
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    noise_texture.inputs[2].default_value = 104.69999694824219
    noise_texture.inputs[3].default_value = 0.0
    noise_texture.inputs[4].default_value = 0.5
    noise_texture.inputs[5].default_value = 2.0
    noise_texture.inputs[6].default_value = 0.0
    noise_texture.inputs[7].default_value = 1.0
    noise_texture.inputs[8].default_value = 0.0

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT_VECTOR"
    map_range.inputs[0].default_value = 1.0
    map_range.inputs[1].default_value = 0.0
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[3].default_value = 0.0
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[9].default_value = [-1.0, -1.0, 0.0]
    map_range.inputs[10].default_value = [1.0, 1.0, 0.05000000074505806]
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(map_range.outputs[1], extrude_mesh_001.inputs[2])
    links.new(noise_texture.outputs[1], map_range.inputs[6])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.mode = "EDGES"
    mesh_to_curve_001.inputs[1].default_value = True
    links.new(repeat_output.outputs[0], mesh_to_curve_001.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.inputs[3].default_value = False

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.mode = "RADIUS"
    curve_circle.inputs[0].default_value = 6
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle.inputs[4].default_value = 0.0003000000142492354
    links.new(curve_circle.outputs[0], curve_to_mesh_001.inputs[1])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")

    math_004 = nodes.new("ShaderNodeMath")
    math_004.operation = "SUBTRACT"
    math_004.inputs[0].default_value = 1.0
    math_004.inputs[2].default_value = 0.5
    links.new(spline_parameter.outputs[0], math_004.inputs[1])
    links.new(math_004.outputs[0], curve_to_mesh_001.inputs[2])

    repeat_input_001 = nodes.new("GeometryNodeRepeatInput")
    repeat_input_001.inputs[0].default_value = 20

    repeat_output_001 = nodes.new("GeometryNodeRepeatOutput")
    repeat_output_001.active_index = 0
    repeat_output_001.inspection_index = 19
    links.new(repeat_output_001.outputs[0], group_output.inputs[0])

    index_switch = nodes.new("GeometryNodeIndexSwitch")
    index_switch.data_type = "FLOAT"
    index_switch.inputs[1].default_value = 1.5700000524520874
    index_switch.inputs[2].default_value = 0.3499999940395355
    links.new(repeat_input_001.outputs[0], index_switch.inputs[0])
    links.new(index_switch.outputs[0], noise_texture.inputs[1])

    geometry_to_instance = nodes.new("GeometryNodeGeometryToInstance")
    links.new(curve_to_mesh_001.outputs[0], geometry_to_instance.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_006.outputs[0], repeat_output_001.inputs[0])
    links.new(repeat_input_001.outputs[1], join_geometry_006.inputs[0])
    links.new(geometry_to_instance.outputs[0], join_geometry_006.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Count"
    resample_curve.inputs[3].default_value = 30
    resample_curve.inputs[4].default_value = 0.10000000149011612
    links.new(resample_curve.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(mesh_to_curve_001.outputs[0], resample_curve.inputs[0])

    auto_layout_nodes(group)
    return group
