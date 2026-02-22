import bpy
from procedural_human.decorators.geo_node_decorator import geo_node_group
from mathutils import Euler, Vector
from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group
from procedural_human.geo_node_groups.utilities.gem_in_holder import create_gem_in__holder_group
from procedural_human.geo_node_groups.utilities.gold_decorations import create_gold__decorations_group
from procedural_human.geo_node_groups.utilities.gold_on_band import create_gold_on__band_group
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group
from procedural_human.geo_node_groups.utilities.join_splines import create_join__splines_group
from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group
from procedural_human.geo_node_groups.utilities.rivet import create_rivet_group
from procedural_human.geo_node_groups.utilities.swap_attr import create_swap__attr_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, vec_math_op
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_neck_random_wings_group():
    group_name = "Neck_random_wings"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    store_named_attribute_001.inputs[1].default_value = True
    store_named_attribute_001.inputs[2].default_value = "gold"
    store_named_attribute_001.inputs[3].default_value = True


    gem_in_holder_1 = nodes.new("GeometryNodeGroup")
    gem_in_holder_1.node_tree = create_gem_in__holder_group()
    gem_in_holder_1.inputs[0].default_value = 0.009999990463256836
    gem_in_holder_1.inputs[1].default_value = "ruby"
    gem_in_holder_1.inputs[2].default_value = False
    gem_in_holder_1.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_1.inputs[4].default_value = 20
    gem_in_holder_1.inputs[5].default_value = 10
    gem_in_holder_1.inputs[6].default_value = False
    gem_in_holder_1.inputs[7].default_value = 6
    gem_in_holder_1.inputs[8].default_value = 10


    mesh_to_curve_002 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.mode = "EDGES"


    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.node_tree = create_is__edge__boundary_group()


    set_spline_cyclic_001 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_001.inputs[1].default_value = True
    set_spline_cyclic_001.inputs[2].default_value = False


    trim_curve_004 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_004.mode = "FACTOR"
    trim_curve_004.inputs[1].default_value = True
    trim_curve_004.inputs[2].default_value = 0.03867403417825699
    trim_curve_004.inputs[3].default_value = 0.4364641308784485
    trim_curve_004.inputs[4].default_value = 0.0
    trim_curve_004.inputs[5].default_value = 1.0


    curve_to_points_001 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.mode = "COUNT"
    curve_to_points_001.inputs[1].default_value = 50
    curve_to_points_001.inputs[2].default_value = 0.10000000149011612


    set_curve_normal_002 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_002.inputs[1].default_value = True
    set_curve_normal_002.inputs[2].default_value = "Free"


    position_004 = nodes.new("GeometryNodeInputPosition")


    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.inputs[1].default_value = True


    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.input_items.new("ROTATION", "Rotation")
    for_each_geometry_element_input_001.pair_with_output(for_each_geometry_element_output_001)
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0


    transform_geometry_009 = nodes.new("GeometryNodeTransform")
    transform_geometry_009.inputs[1].default_value = "Components"
    transform_geometry_009.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.rotation_space = "LOCAL"
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, -1.5707963705062866, 0.0), 'XYZ')


    frame_014 = nodes.new("NodeFrame")
    frame_014.label = "Random Wings"
    frame_014.text = None
    frame_014.shrink = True
    frame_014.label_size = 20


    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.data_type = "FLOAT"
    random_value_007.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_007.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_007.inputs[2].default_value = 6.0
    random_value_007.inputs[3].default_value = 7.0
    random_value_007.inputs[4].default_value = 0
    random_value_007.inputs[5].default_value = 100
    random_value_007.inputs[6].default_value = 0.5
    random_value_007.inputs[8].default_value = 33


    random_value_008 = nodes.new("FunctionNodeRandomValue")
    random_value_008.data_type = "FLOAT"
    random_value_008.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_008.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_008.inputs[2].default_value = 0.0
    random_value_008.inputs[3].default_value = 0.003000000026077032
    random_value_008.inputs[4].default_value = 0
    random_value_008.inputs[5].default_value = 100
    random_value_008.inputs[6].default_value = 0.5
    random_value_008.inputs[8].default_value = 10


    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[1].default_value = True
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))


    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.target_element = "FACES"
    geometry_proximity_001.inputs[1].default_value = 0
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_001.inputs[3].default_value = 0


    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.inputs[3].default_value = False


    # Parent assignments
    curve_to_mesh.parent = frame_014
    curve_to_points_001.parent = frame_014
    for_each_geometry_element_input_001.parent = frame_014
    for_each_geometry_element_output_001.parent = frame_014
    gem_in_holder_1.parent = frame_014
    geometry_proximity_001.parent = frame_014
    is_edge_boundary.parent = frame_014
    mesh_to_curve_002.parent = frame_014
    position_004.parent = frame_014
    random_value_007.parent = frame_014
    random_value_008.parent = frame_014
    rotate_rotation_002.parent = frame_014
    set_curve_normal_002.parent = frame_014
    set_position_001.parent = frame_014
    set_spline_cyclic_001.parent = frame_014
    store_named_attribute_001.parent = frame_014
    transform_geometry_009.parent = frame_014
    trim_curve_004.parent = frame_014

    # Internal links
    links.new(is_edge_boundary.outputs[0], mesh_to_curve_002.inputs[1])
    links.new(set_spline_cyclic_001.outputs[0], trim_curve_004.inputs[0])
    links.new(trim_curve_004.outputs[0], curve_to_points_001.inputs[0])
    links.new(set_curve_normal_002.outputs[0], set_spline_cyclic_001.inputs[0])
    links.new(mesh_to_curve_002.outputs[0], set_curve_normal_002.inputs[0])
    links.new(curve_to_points_001.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(position_004.outputs[0], for_each_geometry_element_input_001.inputs[2])
    links.new(curve_to_points_001.outputs[3], for_each_geometry_element_input_001.inputs[2])
    links.new(store_named_attribute_001.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_009.inputs[2])
    links.new(gem_in_holder_1.outputs[4], transform_geometry_009.inputs[0])
    links.new(rotate_rotation_002.outputs[0], transform_geometry_009.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[2], rotate_rotation_002.inputs[0])
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_1.inputs[10])
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_008.inputs[7])
    links.new(random_value_008.outputs[1], gem_in_holder_1.inputs[9])
    links.new(transform_geometry_009.outputs[0], set_position_001.inputs[0])
    links.new(geometry_proximity_001.outputs[0], set_position_001.inputs[2])
    links.new(set_position_001.outputs[0], curve_to_mesh.inputs[0])
    links.new(gem_in_holder_1.outputs[1], curve_to_mesh.inputs[1])
    links.new(gem_in_holder_1.outputs[2], curve_to_mesh.inputs[2])
    links.new(curve_to_mesh.outputs[0], store_named_attribute_001.inputs[0])

    links.new(for_each_geometry_element_output_001.outputs[2], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
