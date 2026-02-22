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
def create_neck_larger_jewels_group():
    group_name = "Neck_larger_jewels"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketGeometry"


    distribute_points_on_faces_001 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_001.distribute_method = "POISSON"
    distribute_points_on_faces_001.use_legacy_normal = False
    distribute_points_on_faces_001.inputs[2].default_value = 0.009999999776482582
    distribute_points_on_faces_001.inputs[3].default_value = 5000.0
    distribute_points_on_faces_001.inputs[4].default_value = 500.0
    distribute_points_on_faces_001.inputs[5].default_value = 1.0
    distribute_points_on_faces_001.inputs[6].default_value = 0


    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.target_element = "POINTS"
    geometry_proximity.inputs[1].default_value = 0
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity.inputs[3].default_value = 0


    compare_006 = nodes.new("FunctionNodeCompare")
    compare_006.operation = "LESS_THAN"
    compare_006.data_type = "FLOAT"
    compare_006.mode = "ELEMENT"
    compare_006.inputs[1].default_value = 0.0010000000474974513
    compare_006.inputs[2].default_value = 0
    compare_006.inputs[3].default_value = 0
    compare_006.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_006.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_006.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_006.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_006.inputs[8].default_value = ""
    compare_006.inputs[9].default_value = ""
    compare_006.inputs[10].default_value = 0.8999999761581421
    compare_006.inputs[11].default_value = 0.08726649731397629
    compare_006.inputs[12].default_value = 0.0010000000474974513


    gem_in_holder_2 = nodes.new("GeometryNodeGroup")
    gem_in_holder_2.node_tree = create_gem_in__holder_group()
    gem_in_holder_2.inputs[0].default_value = 0.009999990463256836
    gem_in_holder_2.inputs[1].default_value = "ruby"
    gem_in_holder_2.inputs[2].default_value = False
    gem_in_holder_2.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_2.inputs[4].default_value = 20
    gem_in_holder_2.inputs[5].default_value = 10
    gem_in_holder_2.inputs[6].default_value = False
    gem_in_holder_2.inputs[7].default_value = 6
    gem_in_holder_2.inputs[8].default_value = 10
    gem_in_holder_2.inputs[9].default_value = 0.0010000000474974513
    gem_in_holder_2.inputs[10].default_value = 6.6099958419799805


    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.inputs[1].default_value = True
    instance_on_points_001.inputs[3].default_value = False
    instance_on_points_001.inputs[4].default_value = 0


    random_value_010 = nodes.new("FunctionNodeRandomValue")
    random_value_010.data_type = "FLOAT"
    random_value_010.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_010.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_010.inputs[2].default_value = 0.10000000894069672
    random_value_010.inputs[3].default_value = 0.4000000059604645
    random_value_010.inputs[4].default_value = 0
    random_value_010.inputs[5].default_value = 100
    random_value_010.inputs[6].default_value = 0.5
    random_value_010.inputs[7].default_value = 0
    random_value_010.inputs[8].default_value = 0


    frame_016 = nodes.new("NodeFrame")
    frame_016.label = "Larger Jewels"
    frame_016.text = None
    frame_016.shrink = True
    frame_016.label_size = 20


    realize_instances_002 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.inputs[1].default_value = True
    realize_instances_002.inputs[2].default_value = True
    realize_instances_002.inputs[3].default_value = 0


    transform_geometry_010 = nodes.new("GeometryNodeTransform")
    transform_geometry_010.inputs[1].default_value = "Components"
    transform_geometry_010.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    transform_geometry_010.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_010.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.inputs[2].default_value = "ruby"
    swap_attr.inputs[3].default_value = "saphire"


    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.capture_items.new("INT", "Value")
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "INSTANCE"


    index = nodes.new("GeometryNodeInputIndex")


    # Parent assignments
    capture_attribute_001.parent = frame_016
    compare_006.parent = frame_016
    distribute_points_on_faces_001.parent = frame_016
    gem_in_holder_2.parent = frame_016
    geometry_proximity.parent = frame_016
    index.parent = frame_016
    instance_on_points_001.parent = frame_016
    random_value_010.parent = frame_016
    realize_instances_002.parent = frame_016
    reroute_001.parent = frame_016
    swap_attr.parent = frame_016
    transform_geometry_010.parent = frame_016

    # Internal links
    links.new(reroute_001.outputs[0], distribute_points_on_faces_001.inputs[0])
    links.new(geometry_proximity.outputs[1], compare_006.inputs[0])
    links.new(compare_006.outputs[0], distribute_points_on_faces_001.inputs[1])
    links.new(distribute_points_on_faces_001.outputs[0], instance_on_points_001.inputs[0])
    links.new(distribute_points_on_faces_001.outputs[2], instance_on_points_001.inputs[5])
    links.new(random_value_010.outputs[1], instance_on_points_001.inputs[6])
    links.new(transform_geometry_010.outputs[0], instance_on_points_001.inputs[2])
    links.new(gem_in_holder_2.outputs[0], transform_geometry_010.inputs[0])
    links.new(realize_instances_002.outputs[0], swap_attr.inputs[0])
    links.new(capture_attribute_001.outputs[0], realize_instances_002.inputs[0])
    links.new(instance_on_points_001.outputs[0], capture_attribute_001.inputs[0])
    links.new(capture_attribute_001.outputs[1], swap_attr.inputs[1])
    links.new(index.outputs[0], capture_attribute_001.inputs[1])

    links.new(reroute_001.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
