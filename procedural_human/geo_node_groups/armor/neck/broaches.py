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
def create_neck_broaches_group():
    group_name = "Neck_broaches"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    gem_in_holder.inputs[1].default_value = "ruby"
    gem_in_holder.inputs[2].default_value = False
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    gem_in_holder.inputs[6].default_value = True


    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.mode = "COUNT"
    curve_to_points.inputs[1].default_value = 8
    curve_to_points.inputs[2].default_value = 0.10000000149011612


    for_each_geometry_element_input = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input.inputs[1].default_value = True


    for_each_geometry_element_output = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.input_items.new("ROTATION", "Rotation")
    for_each_geometry_element_input.pair_with_output(for_each_geometry_element_output)
    for_each_geometry_element_output.active_input_index = 1
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = "POINT"
    for_each_geometry_element_output.inspection_index = 0


    position_002 = nodes.new("GeometryNodeInputPosition")


    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.inputs[1].default_value = "Components"


    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.rotation_space = "LOCAL"
    rotate_rotation.inputs[1].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')


    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.data_type = "INT"
    random_value.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value.inputs[2].default_value = 0.0
    random_value.inputs[3].default_value = 1.0
    random_value.inputs[4].default_value = 5
    random_value.inputs[5].default_value = 7
    random_value.inputs[6].default_value = 0.5
    random_value.inputs[8].default_value = 0


    transform_geometry_008 = nodes.new("GeometryNodeTransform")
    transform_geometry_008.inputs[1].default_value = "Components"
    transform_geometry_008.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    transform_geometry_008.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_008.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.data_type = "FLOAT"
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_001.inputs[2].default_value = 0.3499999940395355
    random_value_001.inputs[3].default_value = 0.75
    random_value_001.inputs[4].default_value = 0
    random_value_001.inputs[5].default_value = 100
    random_value_001.inputs[6].default_value = 0.5
    random_value_001.inputs[8].default_value = 0


    random_value_002 = nodes.new("FunctionNodeRandomValue")
    random_value_002.data_type = "FLOAT"
    random_value_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_002.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_002.inputs[2].default_value = 0.0
    random_value_002.inputs[3].default_value = 100.0
    random_value_002.inputs[4].default_value = 3
    random_value_002.inputs[5].default_value = 7
    random_value_002.inputs[6].default_value = 0.5
    random_value_002.inputs[8].default_value = 24


    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.rotation_space = "LOCAL"
    rotate_rotation_001.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')


    random_value_003 = nodes.new("FunctionNodeRandomValue")
    random_value_003.data_type = "FLOAT"
    random_value_003.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_003.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_003.inputs[2].default_value = 0.0010000000474974513
    random_value_003.inputs[3].default_value = 0.004999999888241291
    random_value_003.inputs[4].default_value = 3
    random_value_003.inputs[5].default_value = 7
    random_value_003.inputs[6].default_value = 0.5
    random_value_003.inputs[8].default_value = 0


    random_value_004 = nodes.new("FunctionNodeRandomValue")
    random_value_004.data_type = "INT"
    random_value_004.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_004.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_004.inputs[2].default_value = 0.0010000000474974513
    random_value_004.inputs[3].default_value = 0.004999999888241291
    random_value_004.inputs[4].default_value = 0
    random_value_004.inputs[5].default_value = 100
    random_value_004.inputs[6].default_value = 0.5
    random_value_004.inputs[8].default_value = 0


    random_value_005 = nodes.new("FunctionNodeRandomValue")
    random_value_005.data_type = "INT"
    random_value_005.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_005.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_005.inputs[2].default_value = 0.0010000000474974513
    random_value_005.inputs[3].default_value = 0.004999999888241291
    random_value_005.inputs[4].default_value = 6
    random_value_005.inputs[5].default_value = 20
    random_value_005.inputs[6].default_value = 0.5
    random_value_005.inputs[8].default_value = 0


    random_value_006 = nodes.new("FunctionNodeRandomValue")
    random_value_006.data_type = "INT"
    random_value_006.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_006.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_006.inputs[2].default_value = 0.0010000000474974513
    random_value_006.inputs[3].default_value = 0.004999999888241291
    random_value_006.inputs[4].default_value = 5
    random_value_006.inputs[5].default_value = 30
    random_value_006.inputs[6].default_value = 0.5
    random_value_006.inputs[8].default_value = 0


    frame_012 = nodes.new("NodeFrame")
    frame_012.label = "Broaches"
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20


    trim_curve_001 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_001.mode = "FACTOR"
    trim_curve_001.inputs[1].default_value = True
    trim_curve_001.inputs[2].default_value = 0.18784530460834503
    trim_curve_001.inputs[3].default_value = 0.46817636489868164
    trim_curve_001.inputs[4].default_value = 0.0
    trim_curve_001.inputs[5].default_value = 1.0


    set_curve_normal_001 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.inputs[1].default_value = True
    set_curve_normal_001.inputs[2].default_value = "Free"


    # Parent assignments
    curve_to_points.parent = frame_012
    for_each_geometry_element_input.parent = frame_012
    for_each_geometry_element_output.parent = frame_012
    gem_in_holder.parent = frame_012
    position_002.parent = frame_012
    random_value.parent = frame_012
    random_value_001.parent = frame_012
    random_value_002.parent = frame_012
    random_value_003.parent = frame_012
    random_value_004.parent = frame_012
    random_value_005.parent = frame_012
    random_value_006.parent = frame_012
    rotate_rotation.parent = frame_012
    rotate_rotation_001.parent = frame_012
    set_curve_normal_001.parent = frame_012
    transform_geometry_007.parent = frame_012
    transform_geometry_008.parent = frame_012
    trim_curve_001.parent = frame_012

    # Internal links
    links.new(curve_to_points.outputs[0], for_each_geometry_element_input.inputs[0])
    links.new(curve_to_points.outputs[3], for_each_geometry_element_input.inputs[2])
    links.new(position_002.outputs[0], for_each_geometry_element_input.inputs[2])
    links.new(gem_in_holder.outputs[0], transform_geometry_007.inputs[0])
    links.new(for_each_geometry_element_input.outputs[2], transform_geometry_007.inputs[2])
    links.new(for_each_geometry_element_input.outputs[2], rotate_rotation.inputs[0])
    links.new(for_each_geometry_element_input.outputs[0], random_value.inputs[7])
    links.new(random_value.outputs[2], gem_in_holder.inputs[7])
    links.new(transform_geometry_007.outputs[0], transform_geometry_008.inputs[0])
    links.new(transform_geometry_008.outputs[0], for_each_geometry_element_output.inputs[1])
    links.new(for_each_geometry_element_input.outputs[0], random_value_001.inputs[7])
    links.new(random_value_001.outputs[1], transform_geometry_007.inputs[4])
    links.new(for_each_geometry_element_input.outputs[0], random_value_002.inputs[7])
    links.new(random_value_002.outputs[1], gem_in_holder.inputs[10])
    links.new(rotate_rotation_001.outputs[0], transform_geometry_007.inputs[3])
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])
    links.new(for_each_geometry_element_input.outputs[0], random_value_003.inputs[7])
    links.new(random_value_003.outputs[1], gem_in_holder.inputs[9])
    links.new(for_each_geometry_element_input.outputs[0], random_value_004.inputs[7])
    links.new(random_value_004.outputs[2], gem_in_holder.inputs[5])
    links.new(for_each_geometry_element_input.outputs[0], random_value_005.inputs[7])
    links.new(random_value_005.outputs[2], gem_in_holder.inputs[4])
    links.new(for_each_geometry_element_input.outputs[0], random_value_006.inputs[7])
    links.new(random_value_006.outputs[2], gem_in_holder.inputs[8])
    links.new(set_curve_normal_001.outputs[0], curve_to_points.inputs[0])
    links.new(trim_curve_001.outputs[0], set_curve_normal_001.inputs[0])

    links.new(for_each_geometry_element_output.outputs[2], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
