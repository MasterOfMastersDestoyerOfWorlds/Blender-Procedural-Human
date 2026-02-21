import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.gold_wavies import create_gold__wavies_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, separate_xyz, vec_math_op

@geo_node_group
def create_gold__decorations_group():
    group_name = "Gold Decorations"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Curves", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Seed", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 30
    socket.min_value = -10000
    socket.max_value = 10000
    socket = group.interface.new_socket(name="Scale", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 4.049999713897705
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(name="Count", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 18
    socket.min_value = 1
    socket.max_value = 10000

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    group_input = nodes.new("NodeGroupInput")

    mesh_line = nodes.new("GeometryNodeMeshLine")
    mesh_line.mode = "OFFSET"
    mesh_line.count_mode = "TOTAL"
    mesh_line.inputs[1].default_value = 1.0
    mesh_line.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    mesh_line.inputs[3].default_value = Vector((0.004999999888241291, 0.0, 0.0))

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.inputs[1].default_value = True
    instance_on_points.inputs[3].default_value = True
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    links.new(mesh_line.outputs[0], instance_on_points.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.data_type = "INT"
    random_value.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value.inputs[2].default_value = 0.0
    random_value.inputs[3].default_value = 1.0
    random_value.inputs[4].default_value = 0
    random_value.inputs[6].default_value = 0.5
    random_value.inputs[7].default_value = 0
    links.new(random_value.outputs[2], instance_on_points.inputs[4])

    scale_instances_001 = nodes.new("GeometryNodeScaleInstances")
    scale_instances_001.inputs[1].default_value = True
    scale_instances_001.inputs[2].default_value = Vector((1.0, -1.0, 1.0))
    scale_instances_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    scale_instances_001.inputs[4].default_value = True
    links.new(instance_on_points.outputs[0], scale_instances_001.inputs[0])

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    links.new(instance_on_points.outputs[0], join_geometry_008.inputs[0])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.inputs[1].default_value = True
    realize_instances.inputs[2].default_value = True
    realize_instances.inputs[3].default_value = 0
    links.new(join_geometry_008.outputs[0], realize_instances.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.inputs[1].default_value = True
    links.new(scale_instances_001.outputs[0], flip_faces_003.inputs[0])
    links.new(flip_faces_003.outputs[0], join_geometry_008.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.inputs[1].default_value = True
    links.new(realize_instances.outputs[0], bounding_box.inputs[0])

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = True
    sample_curve.data_type = "FLOAT"
    sample_curve.inputs[1].default_value = 0.0
    sample_curve.inputs[3].default_value = 0.0
    sample_curve.inputs[4].default_value = 0
    links.new(group_input.outputs[0], sample_curve.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT_VECTOR"
    map_range_001.inputs[0].default_value = 1.0
    map_range_001.inputs[1].default_value = 0.0
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[3].default_value = 0.0
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range_001.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(position_002.outputs[0], map_range_001.inputs[6])
    links.new(bounding_box.outputs[1], map_range_001.inputs[7])
    links.new(bounding_box.outputs[2], map_range_001.inputs[8])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(map_range_001.outputs[1], separate_x_y_z_003.inputs[0])
    links.new(separate_x_y_z_003.outputs[0], sample_curve.inputs[2])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[1].default_value = True
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(realize_instances.outputs[0], set_position_001.inputs[0])

    scaled_position = vec_math_op(group, "SCALE", position_002.outputs[0], group_input.outputs[2])
    _, scaled_y, scaled_z = separate_xyz(group, scaled_position)
    tangential_offset = vec_math_op(group, "SCALE", sample_curve.outputs[3], scaled_y)
    normal_cross = vec_math_op(group, "CROSS_PRODUCT", sample_curve.outputs[2], sample_curve.outputs[3])
    normal_offset = vec_math_op(group, "SCALE", normal_cross, scaled_z)
    base_offset = vec_math_op(group, "ADD", sample_curve.outputs[1], tangential_offset)
    links.new(vec_math_op(group, "ADD", base_offset, normal_offset), set_position_001.inputs[2])

    gold_wavies = nodes.new("GeometryNodeGroup")
    gold_wavies.node_tree = create_gold__wavies_group()
    links.new(gold_wavies.outputs[0], instance_on_points.inputs[2])

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.component = "INSTANCES"
    links.new(gold_wavies.outputs[0], domain_size.inputs[0])
    links.new(domain_size.outputs[5], random_value.inputs[5])

    group_input_001 = nodes.new("NodeGroupInput")
    links.new(group_input_001.outputs[1], random_value.inputs[8])
    links.new(group_input_001.outputs[3], mesh_line.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "gold"
    store_named_attribute.inputs[3].default_value = True
    links.new(store_named_attribute.outputs[0], group_output.inputs[0])
    links.new(set_position_001.outputs[0], store_named_attribute.inputs[0])

    auto_layout_nodes(group)
    return group
