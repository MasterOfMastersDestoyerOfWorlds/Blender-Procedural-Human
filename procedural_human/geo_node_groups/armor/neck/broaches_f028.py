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
def create_neck_broaches_f028_group():
    group_name = "Neck_broaches_f028"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    gem_in_holder_9 = nodes.new("GeometryNodeGroup")
    gem_in_holder_9.node_tree = create_gem_in__holder_group()
    gem_in_holder_9.inputs[0].default_value = 0.009999999776482582
    gem_in_holder_9.inputs[1].default_value = "ruby"
    gem_in_holder_9.inputs[2].default_value = False
    gem_in_holder_9.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_9.inputs[6].default_value = True


    curve_to_points_003 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_003.mode = "COUNT"
    curve_to_points_003.inputs[1].default_value = 2
    curve_to_points_003.inputs[2].default_value = 0.10000000149011612


    for_each_geometry_element_input_002 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_002.inputs[1].default_value = True


    for_each_geometry_element_output_002 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_002.input_items.new("ROTATION", "Rotation")
    for_each_geometry_element_input_002.pair_with_output(for_each_geometry_element_output_002)
    for_each_geometry_element_output_002.active_input_index = 1
    for_each_geometry_element_output_002.active_generation_index = 0
    for_each_geometry_element_output_002.active_main_index = 0
    for_each_geometry_element_output_002.domain = "POINT"
    for_each_geometry_element_output_002.inspection_index = 0


    position_010 = nodes.new("GeometryNodeInputPosition")


    transform_geometry_037 = nodes.new("GeometryNodeTransform")
    transform_geometry_037.inputs[1].default_value = "Components"


    rotate_rotation_007 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_007.rotation_space = "LOCAL"
    rotate_rotation_007.inputs[1].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')


    random_value_014 = nodes.new("FunctionNodeRandomValue")
    random_value_014.data_type = "INT"
    random_value_014.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_014.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_014.inputs[2].default_value = 0.0
    random_value_014.inputs[3].default_value = 1.0
    random_value_014.inputs[4].default_value = 5
    random_value_014.inputs[5].default_value = 7
    random_value_014.inputs[6].default_value = 0.5
    random_value_014.inputs[8].default_value = 0


    transform_geometry_038 = nodes.new("GeometryNodeTransform")
    transform_geometry_038.inputs[1].default_value = "Components"
    transform_geometry_038.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    transform_geometry_038.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_038.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    trim_curve_007 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_007.mode = "FACTOR"
    trim_curve_007.inputs[1].default_value = True
    trim_curve_007.inputs[2].default_value = 0.4000000059604645
    trim_curve_007.inputs[3].default_value = 0.75
    trim_curve_007.inputs[4].default_value = 0.0
    trim_curve_007.inputs[5].default_value = 1.0


    random_value_015 = nodes.new("FunctionNodeRandomValue")
    random_value_015.data_type = "FLOAT"
    random_value_015.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_015.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_015.inputs[2].default_value = 0.25
    random_value_015.inputs[3].default_value = 0.550000011920929
    random_value_015.inputs[4].default_value = 0
    random_value_015.inputs[5].default_value = 100
    random_value_015.inputs[6].default_value = 0.5
    random_value_015.inputs[8].default_value = 0


    store_named_attribute_010 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_010.data_type = "BOOLEAN"
    store_named_attribute_010.domain = "POINT"
    store_named_attribute_010.inputs[1].default_value = True
    store_named_attribute_010.inputs[2].default_value = "skip"
    store_named_attribute_010.inputs[3].default_value = True


    random_value_016 = nodes.new("FunctionNodeRandomValue")
    random_value_016.data_type = "FLOAT"
    random_value_016.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_016.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_016.inputs[2].default_value = 0.0
    random_value_016.inputs[3].default_value = 100.0
    random_value_016.inputs[4].default_value = 3
    random_value_016.inputs[5].default_value = 7
    random_value_016.inputs[6].default_value = 0.5
    random_value_016.inputs[8].default_value = 16


    rotate_rotation_008 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_008.rotation_space = "LOCAL"
    rotate_rotation_008.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')


    random_value_017 = nodes.new("FunctionNodeRandomValue")
    random_value_017.data_type = "FLOAT"
    random_value_017.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_017.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_017.inputs[2].default_value = 0.0010000000474974513
    random_value_017.inputs[3].default_value = 0.004999999888241291
    random_value_017.inputs[4].default_value = 3
    random_value_017.inputs[5].default_value = 7
    random_value_017.inputs[6].default_value = 0.5
    random_value_017.inputs[8].default_value = 0


    random_value_018 = nodes.new("FunctionNodeRandomValue")
    random_value_018.data_type = "INT"
    random_value_018.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_018.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_018.inputs[2].default_value = 0.0010000000474974513
    random_value_018.inputs[3].default_value = 0.004999999888241291
    random_value_018.inputs[4].default_value = 0
    random_value_018.inputs[5].default_value = 100
    random_value_018.inputs[6].default_value = 0.5
    random_value_018.inputs[8].default_value = 0


    random_value_019 = nodes.new("FunctionNodeRandomValue")
    random_value_019.data_type = "INT"
    random_value_019.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_019.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_019.inputs[2].default_value = 0.0010000000474974513
    random_value_019.inputs[3].default_value = 0.004999999888241291
    random_value_019.inputs[4].default_value = 6
    random_value_019.inputs[5].default_value = 20
    random_value_019.inputs[6].default_value = 0.5
    random_value_019.inputs[8].default_value = 0


    random_value_020 = nodes.new("FunctionNodeRandomValue")
    random_value_020.data_type = "INT"
    random_value_020.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_020.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_020.inputs[2].default_value = 0.0010000000474974513
    random_value_020.inputs[3].default_value = 0.004999999888241291
    random_value_020.inputs[4].default_value = 5
    random_value_020.inputs[5].default_value = 30
    random_value_020.inputs[6].default_value = 0.5
    random_value_020.inputs[8].default_value = 0


    frame_028 = nodes.new("NodeFrame")
    frame_028.label = "Broaches"
    frame_028.text = None
    frame_028.shrink = True
    frame_028.label_size = 20


    store_named_attribute_012 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_012.data_type = "BOOLEAN"
    store_named_attribute_012.domain = "POINT"
    store_named_attribute_012.inputs[1].default_value = True
    store_named_attribute_012.inputs[2].default_value = "skip"
    store_named_attribute_012.inputs[3].default_value = True


    # Parent assignments
    curve_to_points_003.parent = frame_028
    for_each_geometry_element_input_002.parent = frame_028
    for_each_geometry_element_output_002.parent = frame_028
    gem_in_holder_9.parent = frame_028
    position_010.parent = frame_028
    random_value_014.parent = frame_028
    random_value_015.parent = frame_028
    random_value_016.parent = frame_028
    random_value_017.parent = frame_028
    random_value_018.parent = frame_028
    random_value_019.parent = frame_028
    random_value_020.parent = frame_028
    rotate_rotation_007.parent = frame_028
    rotate_rotation_008.parent = frame_028
    store_named_attribute_010.parent = frame_028
    store_named_attribute_012.parent = frame_028
    transform_geometry_037.parent = frame_028
    transform_geometry_038.parent = frame_028
    trim_curve_007.parent = frame_028

    # Internal links
    links.new(curve_to_points_003.outputs[0], for_each_geometry_element_input_002.inputs[0])
    links.new(curve_to_points_003.outputs[3], for_each_geometry_element_input_002.inputs[2])
    links.new(position_010.outputs[0], for_each_geometry_element_input_002.inputs[2])
    links.new(gem_in_holder_9.outputs[0], transform_geometry_037.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[2], transform_geometry_037.inputs[2])
    links.new(for_each_geometry_element_input_002.outputs[2], rotate_rotation_007.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_014.inputs[7])
    links.new(random_value_014.outputs[2], gem_in_holder_9.inputs[7])
    links.new(transform_geometry_037.outputs[0], transform_geometry_038.inputs[0])
    links.new(trim_curve_007.outputs[0], curve_to_points_003.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_015.inputs[7])
    links.new(random_value_015.outputs[1], transform_geometry_037.inputs[4])
    links.new(store_named_attribute_010.outputs[0], for_each_geometry_element_output_002.inputs[1])
    links.new(transform_geometry_038.outputs[0], store_named_attribute_010.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_016.inputs[7])
    links.new(random_value_016.outputs[1], gem_in_holder_9.inputs[10])
    links.new(rotate_rotation_008.outputs[0], transform_geometry_037.inputs[3])
    links.new(rotate_rotation_007.outputs[0], rotate_rotation_008.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_017.inputs[7])
    links.new(random_value_017.outputs[1], gem_in_holder_9.inputs[9])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_018.inputs[7])
    links.new(random_value_018.outputs[2], gem_in_holder_9.inputs[5])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_019.inputs[7])
    links.new(random_value_019.outputs[2], gem_in_holder_9.inputs[4])
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_020.inputs[7])
    links.new(random_value_020.outputs[2], gem_in_holder_9.inputs[8])
    links.new(for_each_geometry_element_output_002.outputs[2], store_named_attribute_012.inputs[0])

    links.new(store_named_attribute_012.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
