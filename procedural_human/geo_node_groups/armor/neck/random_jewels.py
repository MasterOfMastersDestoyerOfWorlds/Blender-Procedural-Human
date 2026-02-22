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
def create_neck_random_jewels_group():
    group_name = "Neck_random_jewels"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    distribute_points_on_faces.inputs[1].default_value = True
    distribute_points_on_faces.inputs[2].default_value = 0.0
    distribute_points_on_faces.inputs[3].default_value = 10.0
    distribute_points_on_faces.inputs[4].default_value = 5000.0
    distribute_points_on_faces.inputs[5].default_value = 1.0
    distribute_points_on_faces.inputs[6].default_value = 1


    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.inputs[1].default_value = True
    instance_on_points.inputs[3].default_value = False
    instance_on_points.inputs[4].default_value = 0
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')


    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.inputs[0].default_value = 0.004000000189989805
    ico_sphere.inputs[1].default_value = 2


    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "INSTANCE"
    store_named_attribute_002.inputs[1].default_value = True
    store_named_attribute_002.inputs[2].default_value = "ruby"


    random_value_009 = nodes.new("FunctionNodeRandomValue")
    random_value_009.data_type = "BOOLEAN"
    random_value_009.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_009.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_009.inputs[2].default_value = 0.0
    random_value_009.inputs[3].default_value = 1.0
    random_value_009.inputs[4].default_value = 0
    random_value_009.inputs[5].default_value = 100
    random_value_009.inputs[6].default_value = 0.5
    random_value_009.inputs[7].default_value = 0
    random_value_009.inputs[8].default_value = 0


    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.operation = "NOT"
    boolean_math_003.inputs[1].default_value = False


    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "INSTANCE"
    store_named_attribute_003.inputs[1].default_value = True
    store_named_attribute_003.inputs[2].default_value = "saphire"


    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.inputs[1].default_value = True
    realize_instances_001.inputs[2].default_value = True
    realize_instances_001.inputs[3].default_value = 0


    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.domain = "FACE"
    set_shade_smooth_003.inputs[1].default_value = True
    set_shade_smooth_003.inputs[2].default_value = True


    frame_015 = nodes.new("NodeFrame")
    frame_015.label = "Random Jewels"
    frame_015.text = None
    frame_015.shrink = True
    frame_015.label_size = 20


    random_value_011 = nodes.new("FunctionNodeRandomValue")
    random_value_011.data_type = "FLOAT"
    random_value_011.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_011.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_011.inputs[2].default_value = 0.20000000298023224
    random_value_011.inputs[3].default_value = 0.6000000238418579
    random_value_011.inputs[4].default_value = 0
    random_value_011.inputs[5].default_value = 100
    random_value_011.inputs[6].default_value = 0.5
    random_value_011.inputs[7].default_value = 0
    random_value_011.inputs[8].default_value = 0


    # Parent assignments
    boolean_math_003.parent = frame_015
    distribute_points_on_faces.parent = frame_015
    ico_sphere.parent = frame_015
    instance_on_points.parent = frame_015
    random_value_009.parent = frame_015
    random_value_011.parent = frame_015
    realize_instances_001.parent = frame_015
    set_shade_smooth_003.parent = frame_015
    store_named_attribute_002.parent = frame_015
    store_named_attribute_003.parent = frame_015

    # Internal links
    links.new(distribute_points_on_faces.outputs[0], instance_on_points.inputs[0])
    links.new(instance_on_points.outputs[0], store_named_attribute_002.inputs[0])
    links.new(random_value_009.outputs[3], store_named_attribute_002.inputs[3])
    links.new(random_value_009.outputs[3], boolean_math_003.inputs[0])
    links.new(store_named_attribute_002.outputs[0], store_named_attribute_003.inputs[0])
    links.new(boolean_math_003.outputs[0], store_named_attribute_003.inputs[3])
    links.new(store_named_attribute_003.outputs[0], realize_instances_001.inputs[0])
    links.new(set_shade_smooth_003.outputs[0], instance_on_points.inputs[2])
    links.new(ico_sphere.outputs[0], set_shade_smooth_003.inputs[0])
    links.new(random_value_011.outputs[1], instance_on_points.inputs[6])

    links.new(distribute_points_on_faces.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
