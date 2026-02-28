import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.geo_node_groups.node_helpers import combine_xyz, compare_op, create_float_curve, curve_circle, math_op, resample_curve, separate_xyz, set_position
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_blocker_collar_gambeson_pattern_piping_group():
    group_name = "BlockerCollarGambesonPatternPiping"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Curve", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Curve", in_out="INPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    curve_circle_003 = curve_circle(group, "RADIUS", 57, 0.004999999888241291)
    curve_circle_003.node.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_003.node.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_003.node.inputs[3].default_value = Vector((1.0, 0.0, 0.0))

    resample_curve_002 = resample_curve(group, True, None, True, "Length", 10, 0.009999999776482582)

    position = nodes.new("GeometryNodeInputPosition")

    index_001 = nodes.new("GeometryNodeInputIndex")

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.inputs[1].default_value = "Components"
    transform_geometry_002.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_002.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 0.5, 1.0))
    links.new(curve_circle_003, transform_geometry_002.inputs[0])

    separate_x_y_z_x, separate_x_y_z_y, separate_x_y_z_z = separate_xyz(group, position.outputs[0])

    compare_002 = compare_op(group, "EQUAL", "INT", 0.0, 0.0)
    compare_002.node.inputs[10].default_value = 0.8999999761581421
    compare_002.node.inputs[11].default_value = 0.08726649731397629
    compare_002.node.inputs[12].default_value = 0.0010000000474974513
    links.new(index_001.outputs[0], compare_002.node.inputs[2])

    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    map_range_002.inputs[1].default_value = -0.004999999888241291
    map_range_002.inputs[2].default_value = 0.004999999888241291
    map_range_002.inputs[3].default_value = 0.0
    map_range_002.inputs[4].default_value = 1.0
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range_002.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range_002.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(separate_x_y_z_x, map_range_002.inputs[0])

    float_curve = create_float_curve(group, map_range_002.outputs[0], [
        (0.0, 0.0),
        (0.16918471455574036, 0.04741369187831879),
        (0.22054383158683777, 1.0),
        (0.2765861451625824, 0.3771551549434662, 'VECTOR'),
        (0.41087615489959717, 1.0),
        (1.0, 1.0),
    ])

    math = math_op(group, "MULTIPLY", separate_x_y_z_y, float_curve)
    math.node.inputs[2].default_value = 0.5

    combine_x_y_z_002 = combine_xyz(group, separate_x_y_z_x, math, separate_x_y_z_z)

    set_position_000 = set_position(group, transform_geometry_002.outputs[0], True, combine_x_y_z_002, Vector((0.0, 0.0, 0.0)))

    capture_attribute_003 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.active_index = 0
    capture_attribute_003.domain = "POINT"
    capture_attribute_003.capture_items.new("BOOLEAN", "Result")
    links.new(set_position_000, capture_attribute_003.inputs[0])
    links.new(compare_002, capture_attribute_003.inputs[1])

    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.inputs[2].default_value = 1.0
    curve_to_mesh_003.inputs[3].default_value = False
    links.new(resample_curve_002, curve_to_mesh_003.inputs[0])
    links.new(capture_attribute_003.outputs[0], curve_to_mesh_003.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.mode = "EDGES"
    links.new(curve_to_mesh_003.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(capture_attribute_003.outputs[1], mesh_to_curve_001.inputs[1])

    links.new(group_input.outputs[0], resample_curve_002.node.inputs[0])
    links.new(mesh_to_curve_001.outputs[0], group_output.inputs[0])
    links.new(curve_to_mesh_003.outputs[0], group_output.inputs[1])

    auto_layout_nodes(group)
    return group