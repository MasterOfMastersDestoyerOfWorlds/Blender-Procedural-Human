import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.geo_node_groups.node_helpers import combine_xyz, create_float_curve, curve_circle, resample_curve
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_blocker_collar_general_collar_shape_group():
    group_name = "BlockerCollarGeneralCollarShape"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Vector", in_out="OUTPUT", socket_type="NodeSocketVector")
    group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    curve_circle_002 = curve_circle(group, "RADIUS", 105, 0.10000000149011612)
    curve_circle_002.node.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_002.node.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_002.node.inputs[3].default_value = Vector((1.0, 0.0, 0.0))

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")

    quadratic_bézier_001 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_001.inputs[0].default_value = 16
    quadratic_bézier_001.inputs[1].default_value = Vector((0.0, -0.009999999776482582, 0.4000000059604645))
    quadratic_bézier_001.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.44999995827674866))
    quadratic_bézier_001.inputs[3].default_value = Vector((0.0, -0.04999999701976776, 0.5199999809265137))

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")

    curve_circle_004 = curve_circle(group, "RADIUS", 24, 0.10000000149011612)
    curve_circle_004.node.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_004.node.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_004.node.inputs[3].default_value = Vector((1.0, 0.0, 0.0))

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.inputs[1].default_value = True
    set_spline_cyclic.inputs[2].default_value = False
    links.new(curve_circle_002, set_spline_cyclic.inputs[0])

    float_curve_001 = create_float_curve(group, spline_parameter_001.outputs[0], [
        (0.0, 0.7650688290596008),
        (0.46223577857017517, 0.6594827175140381),
        (0.8187312483787537, 0.7587241530418396),
        (1.0, 0.7294828295707703),
    ])

    resample_curve_001 = resample_curve(group, True, quadratic_bézier_001.outputs[0], True, "Count", 34, 0.10000000149011612)

    set_spline_cyclic_001 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_001.inputs[1].default_value = True
    set_spline_cyclic_001.inputs[2].default_value = False
    links.new(curve_circle_004, set_spline_cyclic_001.inputs[0])

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    capture_attribute.capture_items.new("FLOAT", "Factor")
    links.new(set_spline_cyclic.outputs[0], capture_attribute.inputs[0])
    links.new(spline_parameter_002.outputs[0], capture_attribute.inputs[1])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.inputs[1].default_value = True
    set_curve_tilt.inputs[2].default_value = -1.472708821296692
    links.new(resample_curve_001, set_curve_tilt.inputs[0])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "POINT"
    capture_attribute_001.capture_items.new("FLOAT", "Factor")
    links.new(set_curve_tilt.outputs[0], capture_attribute_001.inputs[0])
    links.new(spline_parameter_002.outputs[0], capture_attribute_001.inputs[1])

    curve_to_mesh_004 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_004.inputs[3].default_value = False
    links.new(set_spline_cyclic_001.outputs[0], curve_to_mesh_004.inputs[1])
    links.new(set_curve_tilt.outputs[0], curve_to_mesh_004.inputs[0])
    links.new(float_curve_001, curve_to_mesh_004.inputs[2])

    combine_x_y_z_001 = combine_xyz(group, capture_attribute.outputs[1], capture_attribute_001.outputs[1], 0.0)

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.inputs[3].default_value = False
    links.new(capture_attribute_001.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(capture_attribute.outputs[0], curve_to_mesh_002.inputs[1])
    links.new(float_curve_001, curve_to_mesh_002.inputs[2])

    links.new(combine_x_y_z_001, group_output.inputs[0])
    links.new(curve_to_mesh_002.outputs[0], group_output.inputs[1])
    links.new(curve_to_mesh_004.outputs[0], group_output.inputs[2])

    auto_layout_nodes(group)
    return group