import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.geo_node_groups.node_helpers import compare_op, separate_xyz
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_blocker_chest_group():
    group_name = "BlockerChest"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Output", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.inputs[0].default_value = 0.1300000250339508
    ico_sphere.inputs[1].default_value = 3

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.mode = "RADIUS"
    curve_circle_001.inputs[0].default_value = 9
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_001.inputs[4].default_value = 0.004999999888241291

    position_002 = nodes.new("GeometryNodeInputPosition")

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.legacy_corner_normals = False

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.data_type = "FLOAT_VECTOR"
    random_value.inputs[0].default_value = [-0.10000000149011612, -0.10000000149011612, -0.10000000149011612]
    random_value.inputs[1].default_value = [0.10000000149011612, 0.10000000149011612, 0.10000000149011612]
    random_value.inputs[2].default_value = 0.0
    random_value.inputs[3].default_value = 1.0
    random_value.inputs[4].default_value = 0
    random_value.inputs[5].default_value = 100
    random_value.inputs[6].default_value = 0.5
    random_value.inputs[7].default_value = 0
    random_value.inputs[8].default_value = 2

    group_input = nodes.new("NodeGroupInput")

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.inputs[1].default_value = "Components"
    transform_geometry.inputs[2].default_value = Vector((-0.03999999910593033, 0.0, 0.25))
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.2000000476837158))
    links.new(ico_sphere.outputs[0], transform_geometry.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.inputs[1].default_value = "Components"
    transform_geometry_001.inputs[2].default_value = Vector((-0.10000000149011612, 0.019999999552965164, 0.33000001311302185))
    transform_geometry_001.inputs[3].default_value = Euler((0.0, -0.13439033925533295, 0.18500488996505737), 'XYZ')
    transform_geometry_001.inputs[4].default_value = Vector((1.0199999809265137, 0.8300000429153442, 0.8400001525878906))
    links.new(ico_sphere.outputs[0], transform_geometry_001.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.inputs[2].default_value = 0.21000000834465027
    curve_to_mesh_001.inputs[3].default_value = False
    links.new(curve_circle_001.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(curve_circle_001.outputs[0], curve_to_mesh_001.inputs[1])

    separate_x_y_z_001_x, _, _ = separate_xyz(group, position_002.outputs[0])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.axis = "Z"
    align_rotation_to_vector.pivot_axis = "AUTO"
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector.inputs[1].default_value = 1.0
    links.new(normal_001.outputs[0], align_rotation_to_vector.inputs[2])

    mesh_to_s_d_f_grid = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid.inputs[1].default_value = 0.004999999888241291
    mesh_to_s_d_f_grid.inputs[2].default_value = 2
    links.new(transform_geometry.outputs[0], mesh_to_s_d_f_grid.inputs[0])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    links.new(transform_geometry_001.outputs[0], join_geometry_002.inputs[0])
    links.new(transform_geometry.outputs[0], join_geometry_002.inputs[0])

    mesh_to_s_d_f_grid_001 = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid_001.inputs[1].default_value = 0.004999999888241291
    mesh_to_s_d_f_grid_001.inputs[2].default_value = 2
    links.new(transform_geometry_001.outputs[0], mesh_to_s_d_f_grid_001.inputs[0])

    compare_001 = compare_op(group, "LESS_THAN", "FLOAT", separate_x_y_z_001_x, -0.09999999403953552)
    compare_001.node.inputs[10].default_value = 0.8999999761581421
    compare_001.node.inputs[11].default_value = 0.08726649731397629
    compare_001.node.inputs[12].default_value = 0.0010000000474974513

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.rotation_space = "LOCAL"
    rotate_rotation.inputs[1].default_value = Euler((-0.3707079291343689, 0.3525564670562744, 0.0), 'XYZ')
    links.new(align_rotation_to_vector.outputs[0], rotate_rotation.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.socket_idname = "NodeSocketGeometry"
    links.new(join_geometry_002.outputs[0], reroute.inputs[0])

    s_d_f_grid_boolean = nodes.new("GeometryNodeSDFGridBoolean")
    s_d_f_grid_boolean.operation = "UNION"
    s_d_f_grid_boolean.inputs[0].default_value = 0.0
    links.new(mesh_to_s_d_f_grid.outputs[0], s_d_f_grid_boolean.inputs[1])
    links.new(mesh_to_s_d_f_grid_001.outputs[0], s_d_f_grid_boolean.inputs[1])

    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.rotation_space = "LOCAL"
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])
    links.new(random_value.outputs[0], rotate_rotation_001.inputs[1])

    s_d_f_grid_fillet = nodes.new("GeometryNodeSDFGridFillet")
    s_d_f_grid_fillet.inputs[1].default_value = 3
    links.new(s_d_f_grid_boolean.outputs[0], s_d_f_grid_fillet.inputs[0])

    grid_to_mesh = nodes.new("GeometryNodeGridToMesh")
    grid_to_mesh.inputs[1].default_value = 0.0
    grid_to_mesh.inputs[2].default_value = 0.0
    links.new(s_d_f_grid_fillet.outputs[0], grid_to_mesh.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.inputs[3].default_value = False
    instance_on_points.inputs[4].default_value = 0
    instance_on_points.inputs[6].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))
    links.new(grid_to_mesh.outputs[0], instance_on_points.inputs[0])
    links.new(curve_to_mesh_001.outputs[0], instance_on_points.inputs[2])
    links.new(compare_001, instance_on_points.inputs[1])
    links.new(rotate_rotation_001.outputs[0], instance_on_points.inputs[5])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.inputs[1].default_value = True
    realize_instances.inputs[2].default_value = True
    realize_instances.inputs[3].default_value = 0
    links.new(instance_on_points.outputs[0], realize_instances.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    links.new(realize_instances.outputs[0], switch.inputs[2])
    links.new(reroute.outputs[0], switch.inputs[1])
    links.new(group_input.outputs[0], switch.inputs[0])

    links.new(switch.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group