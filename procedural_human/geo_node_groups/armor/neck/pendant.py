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
def create_neck_pendant_group():
    group_name = "Neck_pendant"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    cylinder_002 = nodes.new("GeometryNodeMeshCylinder")
    cylinder_002.fill_type = "NGON"
    cylinder_002.inputs[0].default_value = 16
    cylinder_002.inputs[1].default_value = 1
    cylinder_002.inputs[2].default_value = 1
    cylinder_002.inputs[3].default_value = 0.019999999552965164
    cylinder_002.inputs[4].default_value = 0.0020000000949949026


    set_position_004 = nodes.new("GeometryNodeSetPosition")
    set_position_004.inputs[1].default_value = True
    set_position_004.inputs[2].default_value = [0.0, 0.0, 0.0]


    position_006 = nodes.new("GeometryNodeInputPosition")


    separate_x_y_z_006 = nodes.new("ShaderNodeSeparateXYZ")


    math_007 = nodes.new("ShaderNodeMath")
    math_007.operation = "ABSOLUTE"
    math_007.inputs[1].default_value = 0.5
    math_007.inputs[2].default_value = 0.5


    combine_x_y_z_003 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_003.inputs[0].default_value = 0.0
    combine_x_y_z_003.inputs[2].default_value = 0.0


    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.clamp = True
    map_range_003.interpolation_type = "LINEAR"
    map_range_003.data_type = "FLOAT"
    map_range_003.inputs[1].default_value = -0.019999999552965164
    map_range_003.inputs[2].default_value = 0.019999999552965164
    map_range_003.inputs[3].default_value = 0.7999999523162842
    map_range_003.inputs[4].default_value = 0.19999998807907104
    map_range_003.inputs[5].default_value = 4.0
    map_range_003.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range_003.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range_003.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range_003.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range_003.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range_003.inputs[11].default_value = [4.0, 4.0, 4.0]


    math_008 = nodes.new("ShaderNodeMath")
    math_008.operation = "MULTIPLY"
    math_008.inputs[2].default_value = 0.5


    boolean_math_004 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.operation = "AND"


    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.mode = "EDGES"


    ico_sphere_004 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_004.inputs[0].default_value = 0.0020000000949949026
    ico_sphere_004.inputs[1].default_value = 1


    instance_on_points_004 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_004.inputs[1].default_value = True
    instance_on_points_004.inputs[3].default_value = False
    instance_on_points_004.inputs[4].default_value = 0
    instance_on_points_004.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_004.inputs[6].default_value = Vector((1.0, 1.0, 1.0))


    transform_geometry_015 = nodes.new("GeometryNodeTransform")
    transform_geometry_015.inputs[1].default_value = "Components"
    transform_geometry_015.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    transform_geometry_015.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_015.inputs[4].default_value = Vector((2.0, 1.0, 0.30000001192092896))


    ico_sphere_005 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_005.inputs[0].default_value = 0.004999999888241291
    ico_sphere_005.inputs[1].default_value = 2


    dual_mesh = nodes.new("GeometryNodeDualMesh")
    dual_mesh.inputs[1].default_value = False


    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")


    transform_geometry_016 = nodes.new("GeometryNodeTransform")
    transform_geometry_016.inputs[1].default_value = "Components"
    transform_geometry_016.inputs[2].default_value = Vector((0.0, 0.003000000026077032, 0.0))
    transform_geometry_016.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_016.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    transform_geometry_017 = nodes.new("GeometryNodeTransform")
    transform_geometry_017.inputs[1].default_value = "Components"
    transform_geometry_017.inputs[2].default_value = Vector((-0.009999999776482582, 0.009999999776482582, 0.0))
    transform_geometry_017.inputs[3].default_value = Euler((0.0, 0.0, 1.0471975803375244), 'XYZ')
    transform_geometry_017.inputs[4].default_value = Vector((0.6000000238418579, 0.6000000238418579, 1.0))


    transform_geometry_018 = nodes.new("GeometryNodeTransform")
    transform_geometry_018.inputs[1].default_value = "Components"
    transform_geometry_018.inputs[2].default_value = Vector((0.009999999776482582, 0.009999999776482582, 0.0))
    transform_geometry_018.inputs[3].default_value = Euler((0.0, 0.0, -1.0471975803375244), 'XYZ')
    transform_geometry_018.inputs[4].default_value = Vector((0.6000000238418579, 0.6000000238418579, 1.0))


    transform_geometry_019 = nodes.new("GeometryNodeTransform")
    transform_geometry_019.inputs[1].default_value = "Components"
    transform_geometry_019.inputs[2].default_value = Vector((0.0, -0.012000000104308128, 0.0))
    transform_geometry_019.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    transform_geometry_019.inputs[4].default_value = Vector((0.30000001192092896, 0.6000000238418579, 1.0))


    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")


    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.data_type = "BOOLEAN"
    store_named_attribute_005.domain = "POINT"
    store_named_attribute_005.inputs[1].default_value = True
    store_named_attribute_005.inputs[2].default_value = "ruby"
    store_named_attribute_005.inputs[3].default_value = True


    join_geometry_010 = nodes.new("GeometryNodeJoinGeometry")


    store_named_attribute_006 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_006.data_type = "BOOLEAN"
    store_named_attribute_006.domain = "POINT"
    store_named_attribute_006.inputs[1].default_value = True
    store_named_attribute_006.inputs[2].default_value = "gold"
    store_named_attribute_006.inputs[3].default_value = True


    frame_004 = nodes.new("NodeFrame")
    frame_004.label = "Pendant"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20


    transform_geometry_040 = nodes.new("GeometryNodeTransform")
    transform_geometry_040.inputs[1].default_value = "Components"
    transform_geometry_040.inputs[2].default_value = Vector((0.0, 0.0, 0.0007999999797903001))
    transform_geometry_040.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_040.inputs[4].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))


    transform_geometry_041 = nodes.new("GeometryNodeTransform")
    transform_geometry_041.inputs[1].default_value = "Components"
    transform_geometry_041.inputs[2].default_value = Vector((0.0, 0.0, 0.0007999999797903001))
    transform_geometry_041.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_041.inputs[4].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))


    scale_elements = nodes.new("GeometryNodeScaleElements")
    scale_elements.domain = "FACE"
    scale_elements.inputs[1].default_value = True
    scale_elements.inputs[2].default_value = 1.2000000476837158
    scale_elements.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    scale_elements.inputs[4].default_value = "Uniform"
    scale_elements.inputs[5].default_value = [1.0, 0.0, 0.0]


    transform_geometry_042 = nodes.new("GeometryNodeTransform")
    transform_geometry_042.inputs[1].default_value = "Components"
    transform_geometry_042.inputs[2].default_value = Vector((0.0, 0.0, 0.0005000000237487257))
    transform_geometry_042.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_042.inputs[4].default_value = Vector((1.0, 1.0, 0.7000000476837158))


    join_geometry_023 = nodes.new("GeometryNodeJoinGeometry")


    transform_geometry_043 = nodes.new("GeometryNodeTransform")
    transform_geometry_043.inputs[1].default_value = "Components"
    transform_geometry_043.inputs[2].default_value = Vector((0.0, 0.0, 0.0005000000237487257))
    transform_geometry_043.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_043.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    # Parent assignments
    boolean_math_004.parent = frame_004
    combine_x_y_z_003.parent = frame_004
    cylinder_002.parent = frame_004
    dual_mesh.parent = frame_004
    ico_sphere_004.parent = frame_004
    ico_sphere_005.parent = frame_004
    instance_on_points_004.parent = frame_004
    join_geometry_007.parent = frame_004
    join_geometry_009.parent = frame_004
    join_geometry_010.parent = frame_004
    join_geometry_023.parent = frame_004
    map_range_003.parent = frame_004
    math_007.parent = frame_004
    math_008.parent = frame_004
    mesh_to_curve_001.parent = frame_004
    position_006.parent = frame_004
    scale_elements.parent = frame_004
    separate_x_y_z_006.parent = frame_004
    set_position_004.parent = frame_004
    store_named_attribute_005.parent = frame_004
    store_named_attribute_006.parent = frame_004
    transform_geometry_015.parent = frame_004
    transform_geometry_016.parent = frame_004
    transform_geometry_017.parent = frame_004
    transform_geometry_018.parent = frame_004
    transform_geometry_019.parent = frame_004
    transform_geometry_040.parent = frame_004
    transform_geometry_041.parent = frame_004
    transform_geometry_042.parent = frame_004
    transform_geometry_043.parent = frame_004

    # Internal links
    links.new(cylinder_002.outputs[0], set_position_004.inputs[0])
    links.new(position_006.outputs[0], separate_x_y_z_006.inputs[0])
    links.new(separate_x_y_z_006.outputs[0], math_007.inputs[0])
    links.new(combine_x_y_z_003.outputs[0], set_position_004.inputs[3])
    links.new(separate_x_y_z_006.outputs[1], map_range_003.inputs[0])
    links.new(math_008.outputs[0], combine_x_y_z_003.inputs[1])
    links.new(math_007.outputs[0], math_008.inputs[0])
    links.new(map_range_003.outputs[0], math_008.inputs[1])
    links.new(cylinder_002.outputs[1], boolean_math_004.inputs[0])
    links.new(cylinder_002.outputs[2], boolean_math_004.inputs[1])
    links.new(set_position_004.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(boolean_math_004.outputs[0], mesh_to_curve_001.inputs[1])
    links.new(mesh_to_curve_001.outputs[0], instance_on_points_004.inputs[0])
    links.new(ico_sphere_004.outputs[0], instance_on_points_004.inputs[2])
    links.new(ico_sphere_005.outputs[0], dual_mesh.inputs[0])
    links.new(dual_mesh.outputs[0], transform_geometry_015.inputs[0])
    links.new(transform_geometry_015.outputs[0], transform_geometry_016.inputs[0])
    links.new(transform_geometry_016.outputs[0], join_geometry_007.inputs[0])
    links.new(transform_geometry_015.outputs[0], transform_geometry_017.inputs[0])
    links.new(transform_geometry_017.outputs[0], join_geometry_007.inputs[0])
    links.new(transform_geometry_015.outputs[0], transform_geometry_018.inputs[0])
    links.new(transform_geometry_018.outputs[0], join_geometry_007.inputs[0])
    links.new(transform_geometry_015.outputs[0], transform_geometry_019.inputs[0])
    links.new(transform_geometry_019.outputs[0], join_geometry_007.inputs[0])
    links.new(instance_on_points_004.outputs[0], join_geometry_009.inputs[0])
    links.new(set_position_004.outputs[0], join_geometry_009.inputs[0])
    links.new(store_named_attribute_005.outputs[0], join_geometry_010.inputs[0])
    links.new(store_named_attribute_006.outputs[0], join_geometry_010.inputs[0])
    links.new(set_position_004.outputs[0], transform_geometry_040.inputs[0])
    links.new(transform_geometry_040.outputs[0], join_geometry_009.inputs[0])
    links.new(transform_geometry_040.outputs[0], transform_geometry_041.inputs[0])
    links.new(transform_geometry_041.outputs[0], join_geometry_009.inputs[0])
    links.new(join_geometry_007.outputs[0], scale_elements.inputs[0])
    links.new(scale_elements.outputs[0], transform_geometry_042.inputs[0])
    links.new(join_geometry_023.outputs[0], store_named_attribute_006.inputs[0])
    links.new(join_geometry_009.outputs[0], join_geometry_023.inputs[0])
    links.new(transform_geometry_042.outputs[0], join_geometry_023.inputs[0])
    links.new(transform_geometry_043.outputs[0], store_named_attribute_005.inputs[0])
    links.new(join_geometry_007.outputs[0], transform_geometry_043.inputs[0])

    links.new(cylinder_002.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
