import bpy
from procedural_human.decorators.geo_node_decorator import geo_node_group
from mathutils import Euler, Vector
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, vec_math_op, create_float_curve
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_neck_neck_rails_group():
    group_name = "Neck_neck_rails"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Rail Curve A", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Rail Curve B", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.inputs[1].default_value = "Components"
    transform_geometry_002.inputs[2].default_value = Vector((0.0, -0.019999999552965164, 0.4800000488758087))
    transform_geometry_002.inputs[3].default_value = Euler((0.4064871668815613, 0.0, 0.0), 'XYZ')
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.inputs[1].default_value = "Components"
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.3700000047683716))
    transform_geometry_003.inputs[3].default_value = Euler((0.15620698034763336, 0.0, 0.0), 'XYZ')
    transform_geometry_003.inputs[4].default_value = Vector((1.2599999904632568, 1.0, 1.0))


    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.mode = "RADIUS"
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle.inputs[4].default_value = 0.08000004291534424


    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.mode = "RADIUS"
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_001.inputs[4].default_value = 0.12999996542930603


    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.inputs[1].default_value = True
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]


    position = nodes.new("GeometryNodeInputPosition")


    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")


    map_range = nodes.new("ShaderNodeMapRange")
    map_range.clamp = False
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    map_range.inputs[1].default_value = -0.14000000059604645
    map_range.inputs[2].default_value = 0.14000000059604645
    map_range.inputs[3].default_value = 0.0
    map_range.inputs[4].default_value = 1.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]


    float_curve_001 = create_float_curve(group, map_range.outputs[0],
        [(0.0, 0.0), (0.645, 0.058), (1.0, 0.0)])


    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.inputs[0].default_value = 0.0
    combine_x_y_z.inputs[1].default_value = 0.0


    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.inputs[1].default_value = "Components"
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_004.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.inputs[1].default_value = "Components"
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    integer = nodes.new("FunctionNodeInputInt")
    integer.integer = 73


    frame_009 = nodes.new("NodeFrame")
    frame_009.label = "Neck Rails"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20


    # Parent assignments
    combine_x_y_z.parent = frame_009
    curve_circle.parent = frame_009
    curve_circle_001.parent = frame_009
    float_curve_001.node.parent = frame_009
    integer.parent = frame_009
    map_range.parent = frame_009
    position.parent = frame_009
    separate_x_y_z.parent = frame_009
    set_position.parent = frame_009
    transform_geometry_002.parent = frame_009
    transform_geometry_003.parent = frame_009
    transform_geometry_004.parent = frame_009
    transform_geometry_005.parent = frame_009

    # Internal links
    links.new(transform_geometry_003.outputs[0], set_position.inputs[0])
    links.new(position.outputs[0], separate_x_y_z.inputs[0])
    links.new(separate_x_y_z.outputs[1], map_range.inputs[0])
    links.new(combine_x_y_z.outputs[0], set_position.inputs[3])
    links.new(float_curve_001, combine_x_y_z.inputs[2])
    links.new(curve_circle_001.outputs[0], transform_geometry_004.inputs[0])
    links.new(transform_geometry_004.outputs[0], transform_geometry_003.inputs[0])
    links.new(transform_geometry_005.outputs[0], transform_geometry_002.inputs[0])
    links.new(curve_circle.outputs[0], transform_geometry_005.inputs[0])
    links.new(integer.outputs[0], curve_circle_001.inputs[0])
    links.new(integer.outputs[0], curve_circle.inputs[0])

    links.new(set_position.outputs[0], group_output.inputs[0])
    links.new(transform_geometry_002.outputs[0], group_output.inputs[1])

    auto_layout_nodes(group)
    return group
