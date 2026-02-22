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
def create_neck_necklace_link_group():
    group_name = "Neck_necklace_link"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    curve_circle_003 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.mode = "RADIUS"
    curve_circle_003.inputs[0].default_value = 20
    curve_circle_003.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_003.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_003.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_003.inputs[4].default_value = 0.014999999664723873


    instance_on_points_003 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.inputs[1].default_value = True
    instance_on_points_003.inputs[3].default_value = False
    instance_on_points_003.inputs[4].default_value = 0
    instance_on_points_003.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_003.inputs[6].default_value = Vector((1.0, 1.0, 1.0))


    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.inputs[0].default_value = 0.0020000000949949026
    ico_sphere_001.inputs[1].default_value = 1


    cylinder_001 = nodes.new("GeometryNodeMeshCylinder")
    cylinder_001.fill_type = "NGON"
    cylinder_001.inputs[0].default_value = 10
    cylinder_001.inputs[1].default_value = 1
    cylinder_001.inputs[2].default_value = 1
    cylinder_001.inputs[3].default_value = 0.014999999664723873
    cylinder_001.inputs[4].default_value = 0.0020000000949949026


    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")


    ico_sphere_002 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_002.inputs[0].default_value = 0.012000000104308128
    ico_sphere_002.inputs[1].default_value = 2


    transform_geometry_013 = nodes.new("GeometryNodeTransform")
    transform_geometry_013.inputs[1].default_value = "Components"
    transform_geometry_013.inputs[2].default_value = Vector((-0.006000000052154064, 0.0, 0.0010000000474974513))
    transform_geometry_013.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_013.inputs[4].default_value = Vector((0.4699999988079071, 0.8600000143051147, 0.05000000074505806))


    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.inputs[1].default_value = True
    set_position_003.inputs[2].default_value = [0.0, 0.0, 0.0]


    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.operation = "SCALE"
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[3].default_value = 0.004999999888241291


    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = False
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    noise_texture.inputs[1].default_value = 60.499996185302734
    noise_texture.inputs[2].default_value = 29.089996337890625
    noise_texture.inputs[3].default_value = 2.0
    noise_texture.inputs[4].default_value = 0.5
    noise_texture.inputs[5].default_value = 2.0
    noise_texture.inputs[6].default_value = 0.0
    noise_texture.inputs[7].default_value = 1.0
    noise_texture.inputs[8].default_value = 0.0


    transform_geometry_014 = nodes.new("GeometryNodeTransform")
    transform_geometry_014.inputs[1].default_value = "Components"
    transform_geometry_014.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_014.inputs[3].default_value = Euler((0.0, 0.0, 3.1415927410125732), 'XYZ')
    transform_geometry_014.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    frame_002 = nodes.new("NodeFrame")
    frame_002.label = "Necklace Link"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20


    ico_sphere_003 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_003.inputs[0].default_value = 0.004999999888241291
    ico_sphere_003.inputs[1].default_value = 1


    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    store_named_attribute_004.inputs[1].default_value = True
    store_named_attribute_004.inputs[2].default_value = "gold"
    store_named_attribute_004.inputs[3].default_value = True


    # Parent assignments
    curve_circle_003.parent = frame_002
    cylinder_001.parent = frame_002
    ico_sphere_001.parent = frame_002
    ico_sphere_002.parent = frame_002
    ico_sphere_003.parent = frame_002
    instance_on_points_003.parent = frame_002
    join_geometry_003.parent = frame_002
    noise_texture.parent = frame_002
    set_position_003.parent = frame_002
    store_named_attribute_004.parent = frame_002
    transform_geometry_013.parent = frame_002
    transform_geometry_014.parent = frame_002
    vector_math_002.parent = frame_002

    # Internal links
    links.new(curve_circle_003.outputs[0], instance_on_points_003.inputs[0])
    links.new(ico_sphere_001.outputs[0], instance_on_points_003.inputs[2])
    links.new(instance_on_points_003.outputs[0], join_geometry_003.inputs[0])
    links.new(cylinder_001.outputs[0], join_geometry_003.inputs[0])
    links.new(transform_geometry_013.outputs[0], join_geometry_003.inputs[0])
    links.new(set_position_003.outputs[0], transform_geometry_013.inputs[0])
    links.new(ico_sphere_002.outputs[0], set_position_003.inputs[0])
    links.new(vector_math_002.outputs[0], set_position_003.inputs[3])
    links.new(noise_texture.outputs[0], vector_math_002.inputs[0])
    links.new(transform_geometry_013.outputs[0], transform_geometry_014.inputs[0])
    links.new(transform_geometry_014.outputs[0], join_geometry_003.inputs[0])
    links.new(ico_sphere_003.outputs[0], join_geometry_003.inputs[0])
    links.new(join_geometry_003.outputs[0], store_named_attribute_004.inputs[0])

    links.new(curve_circle_003.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
