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
def create_neck_collar_gems_group():
    group_name = "Neck_collar_gems"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    instance_on_points_010 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_010.inputs[1].default_value = True
    instance_on_points_010.inputs[3].default_value = False
    instance_on_points_010.inputs[4].default_value = 0
    instance_on_points_010.inputs[6].default_value = Vector((0.6000000238418579, 0.6000000238418579, 0.6000000238418579))


    gem_in_holder_8 = nodes.new("GeometryNodeGroup")
    gem_in_holder_8.node_tree = create_gem_in__holder_group()
    gem_in_holder_8.inputs[0].default_value = 0.009999999776482582
    gem_in_holder_8.inputs[1].default_value = "ruby"
    gem_in_holder_8.inputs[2].default_value = True
    gem_in_holder_8.inputs[3].default_value = 0.004999999888241291
    gem_in_holder_8.inputs[4].default_value = 20
    gem_in_holder_8.inputs[5].default_value = 10
    gem_in_holder_8.inputs[6].default_value = False
    gem_in_holder_8.inputs[7].default_value = 6
    gem_in_holder_8.inputs[8].default_value = 10
    gem_in_holder_8.inputs[9].default_value = 0.0020000000949949026
    gem_in_holder_8.inputs[10].default_value = 2.5099997520446777


    realize_instances_005 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_005.inputs[1].default_value = True
    realize_instances_005.inputs[2].default_value = True
    realize_instances_005.inputs[3].default_value = 0


    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.capture_items.new("INT", "Value")
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "INSTANCE"


    index_002 = nodes.new("GeometryNodeInputIndex")


    resample_curve_008 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_008.keep_last_segment = True
    resample_curve_008.inputs[1].default_value = True
    resample_curve_008.inputs[2].default_value = "Count"
    resample_curve_008.inputs[3].default_value = 10
    resample_curve_008.inputs[4].default_value = 0.10000000149011612


    align_rotation_to_vector_005 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_005.axis = "X"
    align_rotation_to_vector_005.pivot_axis = "AUTO"
    align_rotation_to_vector_005.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_005.inputs[1].default_value = 1.0


    normal_004 = nodes.new("GeometryNodeInputNormal")
    normal_004.legacy_corner_normals = False


    align_rotation_to_vector_006 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_006.axis = "Y"
    align_rotation_to_vector_006.pivot_axis = "AUTO"
    align_rotation_to_vector_006.inputs[1].default_value = 1.0


    curve_tangent_004 = nodes.new("GeometryNodeInputTangent")


    frame_027 = nodes.new("NodeFrame")
    frame_027.label = "Collar Gems"
    frame_027.text = None
    frame_027.shrink = True
    frame_027.label_size = 20


    trim_curve_006 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_006.mode = "FACTOR"
    trim_curve_006.inputs[1].default_value = True
    trim_curve_006.inputs[2].default_value = 0.009999999776482582
    trim_curve_006.inputs[3].default_value = 0.940000057220459
    trim_curve_006.inputs[4].default_value = 0.0
    trim_curve_006.inputs[5].default_value = 1.0


    store_named_attribute_013 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_013.data_type = "BOOLEAN"
    store_named_attribute_013.domain = "POINT"
    store_named_attribute_013.inputs[2].default_value = "saphire"
    store_named_attribute_013.inputs[3].default_value = True


    boolean_math_005 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.operation = "AND"


    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.data_type = "BOOLEAN"
    named_attribute.inputs[0].default_value = "ruby"


    store_named_attribute_014 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_014.data_type = "BOOLEAN"
    store_named_attribute_014.domain = "POINT"
    store_named_attribute_014.inputs[2].default_value = "ruby"
    store_named_attribute_014.inputs[3].default_value = False


    math_017 = nodes.new("ShaderNodeMath")
    math_017.operation = "FLOORED_MODULO"
    math_017.inputs[1].default_value = 2.0
    math_017.inputs[2].default_value = 0.5


    # Parent assignments
    align_rotation_to_vector_005.parent = frame_027
    align_rotation_to_vector_006.parent = frame_027
    boolean_math_005.parent = frame_027
    capture_attribute_002.parent = frame_027
    curve_tangent_004.parent = frame_027
    gem_in_holder_8.parent = frame_027
    index_002.parent = frame_027
    instance_on_points_010.parent = frame_027
    math_017.parent = frame_027
    named_attribute.parent = frame_027
    normal_004.parent = frame_027
    realize_instances_005.parent = frame_027
    resample_curve_008.parent = frame_027
    store_named_attribute_013.parent = frame_027
    store_named_attribute_014.parent = frame_027
    trim_curve_006.parent = frame_027

    # Internal links
    links.new(gem_in_holder_8.outputs[0], instance_on_points_010.inputs[2])
    links.new(capture_attribute_002.outputs[0], realize_instances_005.inputs[0])
    links.new(instance_on_points_010.outputs[0], capture_attribute_002.inputs[0])
    links.new(index_002.outputs[0], capture_attribute_002.inputs[1])
    links.new(resample_curve_008.outputs[0], instance_on_points_010.inputs[0])
    links.new(align_rotation_to_vector_006.outputs[0], instance_on_points_010.inputs[5])
    links.new(align_rotation_to_vector_005.outputs[0], align_rotation_to_vector_006.inputs[0])
    links.new(normal_004.outputs[0], align_rotation_to_vector_006.inputs[2])
    links.new(curve_tangent_004.outputs[0], align_rotation_to_vector_005.inputs[2])
    links.new(trim_curve_006.outputs[0], resample_curve_008.inputs[0])
    links.new(realize_instances_005.outputs[0], store_named_attribute_013.inputs[0])
    links.new(boolean_math_005.outputs[0], store_named_attribute_013.inputs[1])
    links.new(named_attribute.outputs[0], boolean_math_005.inputs[1])
    links.new(store_named_attribute_013.outputs[0], store_named_attribute_014.inputs[0])
    links.new(boolean_math_005.outputs[0], store_named_attribute_014.inputs[1])
    links.new(math_017.outputs[0], boolean_math_005.inputs[0])
    links.new(capture_attribute_002.outputs[1], math_017.inputs[0])

    links.new(instance_on_points_010.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
