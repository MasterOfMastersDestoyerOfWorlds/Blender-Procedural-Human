import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.geo_node_groups.node_helpers import compare_op
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_blocker_collar_gambeson_pattern_stitching_group():
    group_name = "BlockerCollarGambesonPatternStitching"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Mesh", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    subdivide_mesh_001 = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh_001.inputs[1].default_value = 4

    geometry_proximity_002 = nodes.new("GeometryNodeProximity")
    geometry_proximity_002.target_element = "FACES"
    geometry_proximity_002.inputs[1].default_value = 0
    geometry_proximity_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_002.inputs[3].default_value = 0

    curve_tangent = nodes.new("GeometryNodeInputTangent")

    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.inputs[0].default_value = 0.0007999999797903001
    ico_sphere_001.inputs[1].default_value = 2

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.data_type = "FLOAT_VECTOR"
    random_value_001.inputs[0].default_value = [0.699999988079071, 0.699999988079071, 0.699999988079071]
    random_value_001.inputs[1].default_value = [1.0, 1.5, 1.2999999523162842]
    random_value_001.inputs[2].default_value = 0.0
    random_value_001.inputs[3].default_value = 1.0
    random_value_001.inputs[4].default_value = 0
    random_value_001.inputs[5].default_value = 100
    random_value_001.inputs[6].default_value = 0.5
    random_value_001.inputs[7].default_value = 0
    random_value_001.inputs[8].default_value = 0

    compare = compare_op(group, "GREATER_THAN", "FLOAT", geometry_proximity_002.outputs[1], 0.0010000000474974513)
    compare.node.inputs[10].default_value = 0.8999999761581421
    compare.node.inputs[11].default_value = 0.08726649731397629
    compare.node.inputs[12].default_value = 0.0010000000474974513

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.axis = "X"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    align_rotation_to_vector_001.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_001.inputs[2])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.inputs[1].default_value = "Components"
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_004.inputs[4].default_value = Vector((1.5, 0.5, 0.3199999928474426))
    links.new(ico_sphere_001.outputs[0], transform_geometry_004.inputs[0])

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "POINT"
    links.new(subdivide_mesh_001.outputs[0], delete_geometry.inputs[0])
    links.new(compare, delete_geometry.inputs[1])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.mode = "EDGES"
    mesh_to_curve.inputs[1].default_value = True
    links.new(delete_geometry.outputs[0], mesh_to_curve.inputs[0])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    links.new(mesh_to_curve.outputs[0], join_geometry_001.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Length"
    resample_curve.inputs[3].default_value = 101
    resample_curve.inputs[4].default_value = 0.003000000026077032
    links.new(join_geometry_001.outputs[0], resample_curve.inputs[0])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.inputs[1].default_value = True
    instance_on_points_001.inputs[3].default_value = False
    instance_on_points_001.inputs[4].default_value = 0
    links.new(resample_curve.outputs[0], instance_on_points_001.inputs[0])
    links.new(align_rotation_to_vector_001.outputs[0], instance_on_points_001.inputs[5])
    links.new(transform_geometry_004.outputs[0], instance_on_points_001.inputs[2])
    links.new(random_value_001.outputs[0], instance_on_points_001.inputs[6])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.inputs[1].default_value = True
    realize_instances_001.inputs[2].default_value = True
    realize_instances_001.inputs[3].default_value = 0
    links.new(instance_on_points_001.outputs[0], realize_instances_001.inputs[0])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    store_named_attribute_003.inputs[1].default_value = True
    store_named_attribute_003.inputs[2].default_value = "stitching"
    store_named_attribute_003.inputs[3].default_value = True
    links.new(realize_instances_001.outputs[0], store_named_attribute_003.inputs[0])

    links.new(group_input.outputs[0], subdivide_mesh_001.inputs[0])
    links.new(group_input.outputs[1], geometry_proximity_002.inputs[0])
    links.new(group_input.outputs[2], join_geometry_001.inputs[0])
    links.new(store_named_attribute_003.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group