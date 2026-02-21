import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, math_op, vec_math_op

@geo_node_group
def create_rivet_group():
    group_name = "Rivet"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Corners", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False
    socket = group.interface.new_socket(name="Offset", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.9399999976158142
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Spacing", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.9399999976158142
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    capture_attribute_005 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_005.active_index = 0
    capture_attribute_005.domain = "POINT"
    links.new(group_input.outputs[0], capture_attribute_005.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.legacy_corner_normals = False
    links.new(normal.outputs[0], capture_attribute_005.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.mode = "EDGES"
    links.new(capture_attribute_005.outputs[0], mesh_to_curve_001.inputs[0])

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.node_tree = create_is__edge__boundary_group()

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.inputs[1].default_value = True
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]

    curve_tangent_002 = nodes.new("GeometryNodeInputTangent")
    tangent_cross = vec_math_op(group, "CROSS_PRODUCT", capture_attribute_005.outputs[1], curve_tangent_002.outputs[0])
    tangent_normalized = vec_math_op(group, "NORMALIZE", tangent_cross)

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.keep_last_segment = True
    resample_curve_001.inputs[1].default_value = True
    resample_curve_001.inputs[2].default_value = "Length"
    resample_curve_001.inputs[3].default_value = 59
    links.new(resample_curve_001.outputs[0], set_position.inputs[0])
    links.new(mesh_to_curve_001.outputs[0], resample_curve_001.inputs[0])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.inputs[1].default_value = True
    instance_on_points_001.inputs[3].default_value = False
    instance_on_points_001.inputs[4].default_value = 0
    instance_on_points_001.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_001.inputs[6].default_value = Vector((1.0, 1.0, 1.0))

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.inputs[0].default_value = 0.0010000000474974513
    ico_sphere.inputs[1].default_value = 3
    links.new(ico_sphere.outputs[0], instance_on_points_001.inputs[2])

    vertex_neighbors = nodes.new("GeometryNodeInputMeshVertexNeighbors")

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.operation = "EQUAL"
    compare_003.data_type = "INT"
    compare_003.mode = "ELEMENT"
    compare_003.inputs[0].default_value = 0.0
    compare_003.inputs[1].default_value = 0.0
    compare_003.inputs[3].default_value = 2
    compare_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_003.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_003.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_003.inputs[8].default_value = ""
    compare_003.inputs[9].default_value = ""
    compare_003.inputs[10].default_value = 0.8999999761581421
    compare_003.inputs[11].default_value = 0.08726649731397629
    compare_003.inputs[12].default_value = 0.0010000000474974513
    links.new(vertex_neighbors.outputs[1], compare_003.inputs[2])

    evaluate_on_domain = nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.domain = "POINT"
    evaluate_on_domain.data_type = "BOOLEAN"
    links.new(compare_003.outputs[0], evaluate_on_domain.inputs[0])

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.operation = "AND"
    links.new(boolean_math_003.outputs[0], mesh_to_curve_001.inputs[1])
    links.new(is_edge_boundary.outputs[0], boolean_math_003.inputs[0])

    curve_of_point = nodes.new("GeometryNodeCurveOfPoint")
    curve_of_point.inputs[0].default_value = 0

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.operation = "GREATER_EQUAL"
    compare_004.data_type = "INT"
    compare_004.mode = "ELEMENT"
    compare_004.inputs[0].default_value = 0.0
    compare_004.inputs[1].default_value = 0.0
    compare_004.inputs[3].default_value = 1
    compare_004.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_004.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_004.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_004.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_004.inputs[8].default_value = ""
    compare_004.inputs[9].default_value = ""
    compare_004.inputs[10].default_value = 0.8999999761581421
    compare_004.inputs[11].default_value = 0.08726649731397629
    compare_004.inputs[12].default_value = 0.0010000000474974513

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "INT"
    switch_001.inputs[1].default_value = 1
    switch_001.inputs[2].default_value = -1
    links.new(compare_004.outputs[0], switch_001.inputs[0])
    tangent_scaled = vec_math_op(group, "SCALE", tangent_normalized, switch_001.outputs[0])

    links.new(math_op(group, "FLOORED_MODULO", curve_of_point.outputs[0], 2.0), compare_004.inputs[2])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.operation = "MULTIPLY"
    math_001.inputs[1].default_value = 0.009999999776482582
    math_001.inputs[2].default_value = 0.5
    links.new(vec_math_op(group, "SCALE", tangent_scaled, math_001.outputs[0]), set_position.inputs[3])

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "BOOLEAN"
    switch.inputs[1].default_value = True
    links.new(switch.outputs[0], boolean_math_003.inputs[1])
    links.new(group_input.outputs[1], switch.inputs[0])
    links.new(evaluate_on_domain.outputs[0], switch.inputs[2])

    group_input_001 = nodes.new("NodeGroupInput")
    links.new(group_input_001.outputs[2], math_001.inputs[0])

    links.new(
        math_op(group, "MULTIPLY", group_input_001.outputs[3], 0.009999999776482582),
        resample_curve_001.inputs[4],
    )

    group_input_002 = nodes.new("NodeGroupInput")

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.target_element = "FACES"
    geometry_proximity.inputs[1].default_value = 0
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity.inputs[3].default_value = 0
    links.new(group_input_002.outputs[0], geometry_proximity.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[1].default_value = True
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(set_position_001.outputs[0], instance_on_points_001.inputs[0])
    links.new(set_position.outputs[0], set_position_001.inputs[0])
    links.new(geometry_proximity.outputs[0], set_position_001.inputs[2])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.inputs[1].default_value = True
    realize_instances.inputs[2].default_value = True
    realize_instances.inputs[3].default_value = 0
    links.new(realize_instances.outputs[0], group_output.inputs[0])
    links.new(instance_on_points_001.outputs[0], realize_instances.inputs[0])

    auto_layout_nodes(group)
    return group
