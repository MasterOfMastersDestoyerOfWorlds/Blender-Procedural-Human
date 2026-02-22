import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.gem_in_holder import create_gem_in__holder_group
from procedural_human.geo_node_groups.utilities.gold_on_band import create_gold_on__band_group
from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group
from procedural_human.geo_node_groups.utilities.join_splines import create_join__splines_group
from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group
from procedural_human.geo_node_groups.utilities.swap_attr import create_swap__attr_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, math_op, vec_math_op

@geo_node_group
def create_waist_group():
    group_name = "Waist"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    bi_rail_loft = nodes.new("GeometryNodeGroup")
    bi_rail_loft.node_tree = create_bi_rail_loft_group()
    bi_rail_loft.inputs[4].default_value = "Resolution"
    bi_rail_loft.inputs[3].default_value = 0
    bi_rail_loft.inputs[5].default_value = 0.009999999776482582
    bi_rail_loft.inputs[6].default_value = 0.029999999329447746
    bi_rail_loft.inputs[7].default_value = 14
    bi_rail_loft.inputs[8].default_value = 9

    bézier_segment = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment.mode = "OFFSET"
    bézier_segment.inputs[0].default_value = 200
    bézier_segment.inputs[1].default_value = Vector((0.0, -0.14000000059604645, 0.07000000029802322))
    bézier_segment.inputs[2].default_value = Vector((0.0, 0.0, -0.019999999552965164))
    bézier_segment.inputs[3].default_value = Vector((0.0, 0.0, 0.07999999821186066))
    bézier_segment.inputs[4].default_value = Vector((0.0, -0.18999998271465302, -0.049999989569187164))

    frame = nodes.new("NodeFrame")
    frame.label = "Centre Line"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20

    bézier_segment_001 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_001.mode = "OFFSET"
    bézier_segment_001.inputs[0].default_value = 200
    bézier_segment_001.inputs[1].default_value = Vector((-0.14999999105930328, 0.0, 0.07000000029802322))
    bézier_segment_001.inputs[2].default_value = Vector((0.0, 0.0, -0.029999999329447746))
    bézier_segment_001.inputs[3].default_value = Vector((0.0, 0.0, 0.04999999701976776))
    bézier_segment_001.inputs[4].default_value = Vector((-0.1899999976158142, 0.0, -0.029999990016222))

    join_splines = nodes.new("GeometryNodeGroup")
    join_splines.node_tree = create_join__splines_group()
    links.new(join_splines.outputs[0], bi_rail_loft.inputs[1])

    join_splines_1 = nodes.new("GeometryNodeGroup")
    join_splines_1.node_tree = create_join__splines_group()
    links.new(join_splines_1.outputs[0], bi_rail_loft.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.label = "Outside"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20

    frame_002 = nodes.new("NodeFrame")
    frame_002.label = "Centre"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20

    frame_003 = nodes.new("NodeFrame")
    frame_003.label = "Rails"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20

    quadratic_bézier = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier.inputs[0].default_value = 40
    quadratic_bézier.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    quadratic_bézier.inputs[2].default_value = Vector((0.0, -0.6000000238418579, -0.1199999749660492))
    quadratic_bézier.inputs[3].default_value = Vector((1.0, 0.0, 0.0))

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_002.outputs[0], bi_rail_loft.inputs[2])
    links.new(quadratic_bézier.outputs[0], join_geometry_002.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.label = "Profiles"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20

    quadratic_bézier_005 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_005.inputs[0].default_value = 40
    quadratic_bézier_005.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    quadratic_bézier_005.inputs[2].default_value = Vector((-2.2351741790771484e-08, -0.7599999308586121, 0.25999999046325684))
    quadratic_bézier_005.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    links.new(quadratic_bézier_005.outputs[0], join_geometry_002.inputs[0])

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.inputs[1].default_value = "Components"
    transform_geometry.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.0))
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry.inputs[4].default_value = Vector((1.0, -0.7799999713897705, 1.0))

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.inputs[1].default_value = True
    links.new(flip_faces.outputs[0], join_geometry_003.inputs[0])
    links.new(transform_geometry.outputs[0], flip_faces.inputs[0])

    reverse_curve = nodes.new("GeometryNodeReverseCurve")
    reverse_curve.inputs[1].default_value = True
    links.new(reverse_curve.outputs[0], join_splines_1.inputs[0])
    links.new(bézier_segment.outputs[0], reverse_curve.inputs[0])

    reverse_curve_001 = nodes.new("GeometryNodeReverseCurve")
    reverse_curve_001.inputs[1].default_value = True
    links.new(reverse_curve_001.outputs[0], join_splines.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.inputs[1].default_value = "Components"
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.004999999888241291, 0.0))
    transform_geometry_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_001.outputs[0], reverse_curve_001.inputs[0])
    links.new(bézier_segment_001.outputs[0], transform_geometry_001.inputs[0])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.node_tree = create_pipes_group()

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    links.new(pipes.outputs[0], join_geometry_005.inputs[0])

    quadratic_bézier_006 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_006.inputs[0].default_value = 40
    quadratic_bézier_006.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    quadratic_bézier_006.inputs[2].default_value = Vector((-0.18000002205371857, -0.6399999260902405, 0.31999996304512024))
    quadratic_bézier_006.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    links.new(quadratic_bézier_006.outputs[0], join_geometry_002.inputs[0])

    closure_output = nodes.new("NodeClosureOutput")
    closure_output.input_items.new("FLOAT", "Value")
    closure_output.output_items.new("FLOAT", "Value")
    closure_output.active_input_index = 0
    closure_output.active_output_index = 0
    closure_output.define_signature = False

    closure_input = nodes.new("NodeClosureInput")
    closure_input.pair_with_output(closure_output)
    links.new(closure_output.outputs[0], bi_rail_loft.inputs[9])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.inputs[0].default_value = 1.0
    links.new(float_curve.outputs[0], closure_output.inputs[0])
    links.new(closure_input.outputs[0], float_curve.inputs[1])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.mode = "FACES"
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    extrude_mesh.inputs[3].default_value = 0.0020000000949949026
    extrude_mesh.inputs[4].default_value = False

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    links.new(bi_rail_loft.outputs[2], separate_x_y_z.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.operation = "GREATER_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    compare_001.inputs[1].default_value = 0.5999999642372131
    compare_001.inputs[2].default_value = 0
    compare_001.inputs[3].default_value = 0
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_001.inputs[8].default_value = ""
    compare_001.inputs[9].default_value = ""
    compare_001.inputs[10].default_value = 0.8999999761581421
    compare_001.inputs[11].default_value = 0.08726649731397629
    compare_001.inputs[12].default_value = 0.0010000000474974513
    links.new(separate_x_y_z.outputs[1], compare_001.inputs[0])
    links.new(compare_001.outputs[0], extrude_mesh.inputs[1])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.domain = "FACE"
    links.new(separate_geometry_001.outputs[1], join_geometry_005.inputs[0])
    links.new(extrude_mesh.outputs[0], separate_geometry_001.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "OR"
    links.new(boolean_math.outputs[0], separate_geometry_001.inputs[1])
    links.new(extrude_mesh.outputs[1], boolean_math.inputs[0])
    links.new(extrude_mesh.outputs[2], boolean_math.inputs[1])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "gold"
    store_named_attribute.inputs[3].default_value = True
    links.new(separate_geometry_001.outputs[0], store_named_attribute.inputs[0])
    links.new(store_named_attribute.outputs[0], join_geometry_005.inputs[0])

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.inputs[1].default_value = 100000.0
    gold_on_band.inputs[2].default_value = 1.5699999332427979
    gold_on_band.inputs[3].default_value = 1
    links.new(separate_geometry_001.outputs[0], gold_on_band.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    links.new(gold_on_band.outputs[0], join_geometry_006.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "GEOMETRY"
    links.new(switch.outputs[0], join_geometry_003.inputs[0])

    group_input = nodes.new("NodeGroupInput")
    links.new(group_input.outputs[0], switch.inputs[0])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.domain = "EDGE"
    links.new(extrude_mesh.outputs[0], separate_geometry_002.inputs[0])
    links.new(separate_geometry_002.outputs[0], pipes.inputs[0])

    edge_vertices = nodes.new("GeometryNodeInputMeshEdgeVertices")

    edge_delta = vec_math_op(group, "SUBTRACT", edge_vertices.outputs[3], edge_vertices.outputs[2])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.operation = "EQUAL"
    compare_002.data_type = "VECTOR"
    compare_002.mode = "DIRECTION"
    compare_002.inputs[0].default_value = 0.0
    compare_002.inputs[1].default_value = 0.0
    compare_002.inputs[2].default_value = 0
    compare_002.inputs[3].default_value = 0
    compare_002.inputs[5].default_value = [0.0, 0.0, 1.0]
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[8].default_value = ""
    compare_002.inputs[9].default_value = ""
    compare_002.inputs[10].default_value = 0.8999999761581421
    compare_002.inputs[11].default_value = 1.5707963705062866
    compare_002.inputs[12].default_value = 0.3109999895095825
    links.new(edge_delta, compare_002.inputs[4])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.operation = "AND"
    links.new(compare_002.outputs[0], boolean_math_001.inputs[0])
    links.new(boolean_math_001.outputs[0], separate_geometry_002.inputs[1])
    links.new(extrude_mesh.outputs[1], boolean_math_001.inputs[1])

    frame_005 = nodes.new("NodeFrame")
    frame_005.label = "Pipes"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.inputs[3].default_value = False
    instance_on_points.inputs[4].default_value = 0

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    gem_in_holder.inputs[1].default_value = "ruby"
    gem_in_holder.inputs[2].default_value = True
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    gem_in_holder.inputs[4].default_value = 20
    gem_in_holder.inputs[5].default_value = 10
    gem_in_holder.inputs[6].default_value = False
    gem_in_holder.inputs[7].default_value = 6
    gem_in_holder.inputs[8].default_value = 10
    gem_in_holder.inputs[9].default_value = 0.0020000000949949026
    gem_in_holder.inputs[10].default_value = 2.5099997520446777
    links.new(gem_in_holder.outputs[0], instance_on_points.inputs[2])

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.capture_items.new("VECTOR", "Value")
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    links.new(capture_attribute.outputs[0], extrude_mesh.inputs[0])
    links.new(capture_attribute.outputs[1], separate_x_y_z_001.inputs[0])
    links.new(bi_rail_loft.outputs[0], capture_attribute.inputs[0])
    links.new(bi_rail_loft.outputs[2], capture_attribute.inputs[1])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "GREATER_THAN"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    compare.inputs[1].default_value = 0.6800000071525574
    compare.inputs[2].default_value = 0
    compare.inputs[3].default_value = 0
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare.inputs[8].default_value = ""
    compare.inputs[9].default_value = ""
    compare.inputs[10].default_value = 0.8999999761581421
    compare.inputs[11].default_value = 0.08726649731397629
    compare.inputs[12].default_value = 0.0010000000474974513
    links.new(separate_x_y_z_001.outputs[1], compare.inputs[0])
    links.new(compare.outputs[0], instance_on_points.inputs[1])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.axis = "Z"
    align_rotation_to_vector.pivot_axis = "AUTO"
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector.inputs[1].default_value = 1.0
    links.new(align_rotation_to_vector.outputs[0], instance_on_points.inputs[5])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.data_type = "FLOAT"
    random_value.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value.inputs[2].default_value = -0.09999999403953552
    random_value.inputs[3].default_value = 0.09999993443489075
    random_value.inputs[4].default_value = 0
    random_value.inputs[5].default_value = 100
    random_value.inputs[6].default_value = 0.5
    random_value.inputs[7].default_value = 0
    random_value.inputs[8].default_value = 0

    separate_geometry_003 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_003.domain = "FACE"
    links.new(extrude_mesh.outputs[0], separate_geometry_003.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry_003.inputs[1])

    mesh_to_points = nodes.new("GeometryNodeMeshToPoints")
    mesh_to_points.mode = "FACES"
    mesh_to_points.inputs[1].default_value = True
    mesh_to_points.inputs[2].default_value = [0.0, 0.0, 0.0]
    mesh_to_points.inputs[3].default_value = 0.05000000074505806
    links.new(mesh_to_points.outputs[0], instance_on_points.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.legacy_corner_normals = False

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.capture_items.new("VECTOR", "Value")
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "FACE"
    links.new(capture_attribute_001.outputs[0], mesh_to_points.inputs[0])
    links.new(separate_geometry_003.outputs[0], capture_attribute_001.inputs[0])
    links.new(normal.outputs[0], capture_attribute_001.inputs[1])
    links.new(capture_attribute_001.outputs[1], align_rotation_to_vector.inputs[2])
    links.new(bi_rail_loft.outputs[2], capture_attribute_001.inputs[1])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.inputs[1].default_value = True
    realize_instances.inputs[2].default_value = True
    realize_instances.inputs[3].default_value = 0

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(capture_attribute_001.outputs[1], separate_x_y_z_002.inputs[0])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    map_range.inputs[1].default_value = 0.0
    map_range.inputs[2].default_value = 1.0
    map_range.inputs[3].default_value = 0.46000003814697266
    map_range.inputs[4].default_value = 0.28999999165534973
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(separate_x_y_z_002.outputs[0], map_range.inputs[0])

    random_scale = math_op(group, "ADD", map_range.outputs[0], random_value.outputs[1])
    links.new(random_scale, instance_on_points.inputs[6])

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.capture_items.new("INT", "Value")
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "INSTANCE"
    links.new(capture_attribute_002.outputs[0], realize_instances.inputs[0])
    links.new(instance_on_points.outputs[0], capture_attribute_002.inputs[0])

    index = nodes.new("GeometryNodeInputIndex")
    links.new(index.outputs[0], capture_attribute_002.inputs[1])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.domain = "FACE"
    set_shade_smooth.inputs[1].default_value = True
    set_shade_smooth.inputs[2].default_value = True
    links.new(set_shade_smooth.outputs[0], group_output.inputs[0])
    links.new(join_geometry_003.outputs[0], set_shade_smooth.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.label = "Gold"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "FACE"
    links.new(join_geometry_005.outputs[0], delete_geometry.inputs[0])

    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_007.outputs[0], transform_geometry.inputs[0])
    links.new(join_geometry_007.outputs[0], join_geometry_003.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position.outputs[0], separate_x_y_z_003.inputs[0])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.operation = "EQUAL"
    compare_003.data_type = "FLOAT"
    compare_003.mode = "ELEMENT"
    compare_003.inputs[1].default_value = 0.0
    compare_003.inputs[2].default_value = 0
    compare_003.inputs[3].default_value = 0
    compare_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_003.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_003.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_003.inputs[8].default_value = ""
    compare_003.inputs[9].default_value = ""
    compare_003.inputs[10].default_value = 0.8999999761581421
    compare_003.inputs[11].default_value = 0.08726649731397629
    compare_003.inputs[12].default_value = 0.0010000000474974513
    links.new(separate_x_y_z_003.outputs[0], compare_003.inputs[0])
    links.new(compare_003.outputs[0], delete_geometry.inputs[1])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(set_position.outputs[0], join_geometry_007.inputs[0])
    links.new(delete_geometry.outputs[0], set_position.inputs[0])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    compare_004.inputs[1].default_value = 0.0
    compare_004.inputs[2].default_value = 0
    compare_004.inputs[3].default_value = 0
    compare_004.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_004.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_004.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_004.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_004.inputs[8].default_value = ""
    compare_004.inputs[9].default_value = ""
    compare_004.inputs[10].default_value = 0.8999999761581421
    compare_004.inputs[11].default_value = 0.08726649731397629
    compare_004.inputs[12].default_value = 0.0010000000474974513
    links.new(separate_x_y_z_003.outputs[0], compare_004.inputs[0])
    links.new(compare_004.outputs[0], set_position.inputs[1])

    position_001 = nodes.new("GeometryNodeInputPosition")

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.operation = "MULTIPLY"
    vector_math_001.inputs[1].default_value = [0.0, 1.0, 1.0]
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_001.inputs[3].default_value = 1.0
    links.new(position_001.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], set_position.inputs[2])

    frame_007 = nodes.new("NodeFrame")
    frame_007.label = "Merge Centre Line"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20

    separate_geometry_004 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_004.domain = "EDGE"
    links.new(separate_geometry_002.outputs[0], separate_geometry_004.inputs[0])

    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(capture_attribute.outputs[1], separate_x_y_z_004.inputs[0])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.operation = "EQUAL"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    compare_005.inputs[1].default_value = 0.8700000047683716
    compare_005.inputs[2].default_value = 0
    compare_005.inputs[3].default_value = 0
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_005.inputs[8].default_value = ""
    compare_005.inputs[9].default_value = ""
    compare_005.inputs[10].default_value = 0.8999999761581421
    compare_005.inputs[11].default_value = 0.08726649731397629
    compare_005.inputs[12].default_value = 0.09099999070167542
    links.new(separate_x_y_z_004.outputs[1], compare_005.inputs[0])
    links.new(compare_005.outputs[0], separate_geometry_004.inputs[1])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.inputs[1].default_value = "Components"
    transform_geometry_002.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.0))
    transform_geometry_002.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_002.inputs[4].default_value = Vector((1.0, -0.7799999713897705, 1.0))
    links.new(separate_geometry_004.outputs[0], transform_geometry_002.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    links.new(separate_geometry_004.outputs[0], join_geometry_004.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.inputs[1].default_value = True
    links.new(flip_faces_001.outputs[0], join_geometry_004.inputs[0])
    links.new(transform_geometry_002.outputs[0], flip_faces_001.inputs[0])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.inputs[1].default_value = "Components"
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_003.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    links.new(join_geometry_004.outputs[0], transform_geometry_003.inputs[0])

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_004.outputs[0], join_geometry_008.inputs[0])

    flip_faces_002 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.inputs[1].default_value = True
    links.new(flip_faces_002.outputs[0], join_geometry_008.inputs[0])
    links.new(transform_geometry_003.outputs[0], flip_faces_002.inputs[0])

    mesh_to_points_001 = nodes.new("GeometryNodeMeshToPoints")
    mesh_to_points_001.mode = "VERTICES"
    mesh_to_points_001.inputs[1].default_value = True
    mesh_to_points_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    mesh_to_points_001.inputs[3].default_value = 0.05000000074505806

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.inputs[1].default_value = 0
    links.new(mesh_to_points_001.outputs[0], points_to_curves.inputs[0])

    gradient_texture = nodes.new("ShaderNodeTexGradient")
    gradient_texture.gradient_type = "RADIAL"
    gradient_texture.inputs[0].default_value = [0.0, 0.0, 0.0]

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.inputs[1].default_value = True
    merge_by_distance.inputs[2].default_value = "All"
    merge_by_distance.inputs[3].default_value = 0.0010000000474974513
    links.new(merge_by_distance.outputs[0], mesh_to_points_001.inputs[0])
    links.new(join_geometry_008.outputs[0], merge_by_distance.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Length"
    resample_curve.inputs[3].default_value = 754
    resample_curve.inputs[4].default_value = 0.0010000000474974513
    links.new(points_to_curves.outputs[0], resample_curve.inputs[0])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.inputs[1].default_value = "Components"
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_004.inputs[3].default_value = Euler((0.01483529806137085, 0.03560471534729004, 0.0), 'XYZ')
    transform_geometry_004.inputs[4].default_value = Vector((1.059999942779541, 1.0199999809265137, 1.0))
    links.new(resample_curve.outputs[0], transform_geometry_004.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.inputs[1].default_value = "Components"
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_005.inputs[3].default_value = Euler((-0.01151917316019535, -0.06230825185775757, 0.0), 'XYZ')
    transform_geometry_005.inputs[4].default_value = Vector((1.059999942779541, 1.0199999809265137, 1.0))

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    links.new(transform_geometry_004.outputs[0], join_geometry.inputs[0])
    links.new(transform_geometry_005.outputs[0], join_geometry.inputs[0])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.inputs[2].default_value = 1.0
    curve_to_mesh.inputs[3].default_value = False

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.mode = "RADIUS"
    curve_circle.inputs[0].default_value = 3
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle.inputs[4].default_value = 0.0020000000949949026

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[1].default_value = True
    set_position_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(set_position_001.outputs[0], transform_geometry_005.inputs[0])
    links.new(resample_curve.outputs[0], set_position_001.inputs[0])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")

    float_curve_001 = nodes.new("ShaderNodeFloatCurve")
    float_curve_001.inputs[0].default_value = 1.0
    links.new(spline_parameter.outputs[0], float_curve_001.inputs[1])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.inputs[0].default_value = 0.0
    combine_x_y_z.inputs[2].default_value = 0.0
    links.new(combine_x_y_z.outputs[0], set_position_001.inputs[3])

    links.new(
        math_op(group, "MULTIPLY", float_curve_001.outputs[0], -0.009999999776482582),
        combine_x_y_z.inputs[1],
    )

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    store_named_attribute_003.inputs[1].default_value = True
    store_named_attribute_003.inputs[2].default_value = "skip"
    store_named_attribute_003.inputs[3].default_value = True

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.mode = "RADIUS"
    curve_circle_001.inputs[0].default_value = 32
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_001.inputs[4].default_value = 0.009999999776482582

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry.outputs[0], join_geometry_001.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    links.new(curve_circle_001.outputs[0], join_geometry_009.inputs[0])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.inputs[1].default_value = "Components"
    transform_geometry_006.inputs[2].default_value = Vector((0.0, -0.1550000011920929, 0.054999999701976776))
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')
    transform_geometry_006.inputs[4].default_value = Vector((1.0, 0.800000011920929, 1.0))
    links.new(join_geometry_009.outputs[0], transform_geometry_006.inputs[0])

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.inputs[1].default_value = "Components"
    transform_geometry_007.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    transform_geometry_007.inputs[3].default_value = Euler((0.4747295081615448, 0.7522368431091309, 0.8482299447059631), 'XYZ')
    transform_geometry_007.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(curve_circle_001.outputs[0], transform_geometry_007.inputs[0])
    links.new(transform_geometry_007.outputs[0], join_geometry_009.inputs[0])

    frame_008 = nodes.new("NodeFrame")
    frame_008.label = "Knot"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20

    frame_009 = nodes.new("NodeFrame")
    frame_009.label = "Waist Loops"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20

    math_002 = nodes.new("ShaderNodeMath")
    math_002.operation = "ADD"
    math_002.inputs[1].default_value = 0.5
    math_002.inputs[2].default_value = 0.5
    links.new(gradient_texture.outputs[1], math_002.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.operation = "FRACT"
    math_003.inputs[1].default_value = 0.5
    math_003.inputs[2].default_value = 0.5
    links.new(math_003.outputs[0], points_to_curves.inputs[2])
    links.new(math_002.outputs[0], math_003.inputs[0])

    bézier_segment_002 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_002.mode = "OFFSET"
    bézier_segment_002.inputs[0].default_value = 16
    bézier_segment_002.inputs[1].default_value = Vector((0.0, -0.15800000727176666, 0.054999999701976776))
    bézier_segment_002.inputs[2].default_value = Vector((0.04999999701976776, 0.0, 0.0))
    bézier_segment_002.inputs[3].default_value = Vector((-0.03999999910593033, 0.0, 0.05999999865889549))
    bézier_segment_002.inputs[4].default_value = Vector((0.03999999910593033, -0.18800000846385956, -0.06499999761581421))
    links.new(bézier_segment_002.outputs[0], join_geometry_001.inputs[0])

    bézier_segment_003 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_003.mode = "OFFSET"
    bézier_segment_003.inputs[0].default_value = 16
    bézier_segment_003.inputs[1].default_value = Vector((0.0, -0.15800000727176666, 0.054999999701976776))
    bézier_segment_003.inputs[2].default_value = Vector((0.019999997690320015, -0.009999999776482582, 0.0))
    bézier_segment_003.inputs[3].default_value = Vector((-0.009999999776482582, -0.009999999776482582, 0.05999999865889549))
    bézier_segment_003.inputs[4].default_value = Vector((0.009999999776482582, -0.18800000846385956, -0.06499999761581421))
    links.new(bézier_segment_003.outputs[0], join_geometry_001.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.inputs[1].default_value = True

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")

    math_004 = nodes.new("ShaderNodeMath")
    math_004.operation = "MULTIPLY"
    math_004.inputs[1].default_value = 106.49999237060547
    math_004.inputs[2].default_value = 0.5
    links.new(spline_parameter_001.outputs[1], math_004.inputs[0])
    links.new(math_004.outputs[0], set_curve_tilt.inputs[2])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.inputs[1].default_value = True
    instance_on_points_001.inputs[3].default_value = False
    instance_on_points_001.inputs[4].default_value = 0
    instance_on_points_001.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_001.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    links.new(curve_circle.outputs[0], instance_on_points_001.inputs[0])

    curve_circle_002 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_002.mode = "RADIUS"
    curve_circle_002.inputs[0].default_value = 8
    curve_circle_002.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_002.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_002.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_002.inputs[4].default_value = 0.003000000026077032
    links.new(curve_circle_002.outputs[0], instance_on_points_001.inputs[2])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.inputs[1].default_value = True
    realize_instances_001.inputs[2].default_value = True
    realize_instances_001.inputs[3].default_value = 0
    links.new(instance_on_points_001.outputs[0], realize_instances_001.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.keep_last_segment = True
    resample_curve_001.inputs[1].default_value = True
    resample_curve_001.inputs[2].default_value = "Length"
    resample_curve_001.inputs[3].default_value = 754
    resample_curve_001.inputs[4].default_value = 0.0010000000474974513
    links.new(resample_curve_001.outputs[0], set_curve_tilt.inputs[0])
    links.new(join_geometry_001.outputs[0], resample_curve_001.inputs[0])

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    store_named_attribute_004.inputs[1].default_value = True
    store_named_attribute_004.inputs[2].default_value = "rope"
    store_named_attribute_004.inputs[3].default_value = True
    links.new(store_named_attribute_003.outputs[0], store_named_attribute_004.inputs[0])

    capture_attribute_003 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.capture_items.new("FLOAT", "Value")
    capture_attribute_003.active_index = 0
    capture_attribute_003.domain = "POINT"
    links.new(capture_attribute_003.outputs[0], curve_to_mesh.inputs[1])
    links.new(realize_instances_001.outputs[0], capture_attribute_003.inputs[0])

    capture_attribute_004 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_004.capture_items.new("FLOAT", "Value")
    capture_attribute_004.active_index = 0
    capture_attribute_004.domain = "POINT"
    links.new(capture_attribute_004.outputs[0], curve_to_mesh.inputs[0])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_002.outputs[1], capture_attribute_004.inputs[1])
    links.new(spline_parameter_002.outputs[1], capture_attribute_003.inputs[1])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.inputs[2].default_value = 0.0
    links.new(capture_attribute_004.outputs[1], combine_x_y_z_001.inputs[0])
    links.new(capture_attribute_003.outputs[1], combine_x_y_z_001.inputs[1])

    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.data_type = "FLOAT2"
    store_named_attribute_005.domain = "CORNER"
    store_named_attribute_005.inputs[1].default_value = True
    store_named_attribute_005.inputs[2].default_value = "UVMap"
    links.new(store_named_attribute_004.outputs[0], store_named_attribute_005.inputs[0])
    links.new(combine_x_y_z_001.outputs[0], store_named_attribute_005.inputs[3])
    links.new(store_named_attribute_005.outputs[0], switch.inputs[2])

    frame_010 = nodes.new("NodeFrame")
    frame_010.label = "ROPE"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20

    instance_on_points_002 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.inputs[1].default_value = True
    instance_on_points_002.inputs[3].default_value = False
    instance_on_points_002.inputs[4].default_value = 0
    instance_on_points_002.inputs[6].default_value = Vector((1.0, 1.0, 1.0))

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.mode = "POINTS"
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    curve_line.inputs[1].default_value = Vector((0.0, 0.0, 0.05000000074505806))
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    curve_line.inputs[3].default_value = 1.0
    links.new(curve_line.outputs[0], instance_on_points_002.inputs[2])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.axis = "Z"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    align_rotation_to_vector_001.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    links.new(align_rotation_to_vector_001.outputs[0], instance_on_points_002.inputs[5])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_001.inputs[2])

    realize_instances_002 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.inputs[1].default_value = True
    realize_instances_002.inputs[2].default_value = True
    realize_instances_002.inputs[3].default_value = 0
    links.new(instance_on_points_002.outputs[0], realize_instances_002.inputs[0])

    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.keep_last_segment = True
    resample_curve_002.inputs[1].default_value = True
    resample_curve_002.inputs[2].default_value = "Count"
    resample_curve_002.inputs[3].default_value = 7
    resample_curve_002.inputs[4].default_value = 0.10000000149011612
    links.new(realize_instances_002.outputs[0], resample_curve_002.inputs[0])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    links.new(resample_curve_002.outputs[0], set_position_002.inputs[0])

    endpoint_selection = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection.inputs[0].default_value = 1
    endpoint_selection.inputs[1].default_value = 0

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.operation = "NOT"
    boolean_math_003.inputs[1].default_value = False
    links.new(boolean_math_003.outputs[0], set_position_002.inputs[1])
    links.new(endpoint_selection.outputs[0], boolean_math_003.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.operation = "SCALE"
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[3].default_value = 0.006000000052154064
    links.new(vector_math_002.outputs[0], set_position_002.inputs[3])

    random_value_002 = nodes.new("FunctionNodeRandomValue")
    random_value_002.data_type = "FLOAT_VECTOR"
    random_value_002.inputs[0].default_value = [-1.0, -1.0, -1.0]
    random_value_002.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_002.inputs[2].default_value = 0.0
    random_value_002.inputs[3].default_value = 1.0
    random_value_002.inputs[4].default_value = 0
    random_value_002.inputs[5].default_value = 100
    random_value_002.inputs[6].default_value = 0.5
    random_value_002.inputs[7].default_value = 0
    random_value_002.inputs[8].default_value = 2
    links.new(random_value_002.outputs[0], vector_math_002.inputs[0])

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.spline_type = "NURBS"
    set_spline_type.inputs[1].default_value = True
    links.new(set_position_002.outputs[0], set_spline_type.inputs[0])

    resample_curve_003 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.keep_last_segment = True
    resample_curve_003.inputs[1].default_value = True
    resample_curve_003.inputs[2].default_value = "Count"
    resample_curve_003.inputs[3].default_value = 15
    resample_curve_003.inputs[4].default_value = 0.10000000149011612
    links.new(set_spline_type.outputs[0], resample_curve_003.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.inputs[2].default_value = 1.0
    curve_to_mesh_001.inputs[3].default_value = True
    links.new(resample_curve_003.outputs[0], curve_to_mesh_001.inputs[0])

    curve_circle_003 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.mode = "RADIUS"
    curve_circle_003.inputs[0].default_value = 32
    curve_circle_003.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_003.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_003.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_003.inputs[4].default_value = 9.999999747378752e-05
    links.new(curve_circle_003.outputs[0], curve_to_mesh_001.inputs[1])

    join_geometry_011 = nodes.new("GeometryNodeJoinGeometry")
    links.new(curve_to_mesh_001.outputs[0], join_geometry_011.inputs[0])
    links.new(curve_to_mesh.outputs[0], join_geometry_011.inputs[0])
    links.new(join_geometry_011.outputs[0], store_named_attribute_003.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.target_element = "FACES"
    geometry_proximity.inputs[1].default_value = 0
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity.inputs[3].default_value = 0
    links.new(curve_to_mesh.outputs[0], geometry_proximity.inputs[0])
    links.new(geometry_proximity.outputs[0], set_position_002.inputs[2])

    join_geometry_012 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_012.outputs[0], capture_attribute_004.inputs[0])
    links.new(set_curve_tilt.outputs[0], join_geometry_012.inputs[0])

    set_curve_tilt_001 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_001.inputs[1].default_value = True
    links.new(set_curve_tilt_001.outputs[0], join_geometry_012.inputs[0])

    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")

    math_005 = nodes.new("ShaderNodeMath")
    math_005.operation = "MULTIPLY"
    math_005.inputs[1].default_value = 199.0999755859375
    math_005.inputs[2].default_value = 0.5
    links.new(spline_parameter_003.outputs[1], math_005.inputs[0])
    links.new(math_005.outputs[0], set_curve_tilt_001.inputs[2])

    resample_curve_004 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_004.keep_last_segment = True
    resample_curve_004.inputs[1].default_value = True
    resample_curve_004.inputs[2].default_value = "Length"
    resample_curve_004.inputs[3].default_value = 754
    resample_curve_004.inputs[4].default_value = 0.0010000000474974513
    links.new(resample_curve_004.outputs[0], set_curve_tilt_001.inputs[0])
    links.new(transform_geometry_006.outputs[0], resample_curve_004.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.inputs[2].default_value = "ruby"
    swap_attr.inputs[3].default_value = "saphire"
    links.new(swap_attr.outputs[0], join_geometry_006.inputs[0])
    links.new(realize_instances.outputs[0], swap_attr.inputs[0])
    links.new(capture_attribute_002.outputs[1], swap_attr.inputs[1])

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

    position_004 = nodes.new("GeometryNodeInputPosition")

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.inputs[1].default_value = True

    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.input_items.new("VECTOR", "Vector")
    for_each_geometry_element_output_001.input_items.new("ROTATION", "Rotation 2")
    for_each_geometry_element_input_001.pair_with_output(for_each_geometry_element_output_001)
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_input_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    links.new(position_004.outputs[0], for_each_geometry_element_input_001.inputs[2])
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_006.inputs[0])

    transform_geometry_008 = nodes.new("GeometryNodeTransform")
    transform_geometry_008.inputs[1].default_value = "Components"
    transform_geometry_008.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_008.inputs[2])
    links.new(gem_in_holder_1.outputs[4], transform_geometry_008.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.rotation_space = "LOCAL"
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, -1.5707963705062866, 0.0), 'XYZ')
    links.new(rotate_rotation_002.outputs[0], transform_geometry_008.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[2], rotate_rotation_002.inputs[0])

    frame_011 = nodes.new("NodeFrame")
    frame_011.label = "Random Wings"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20

    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.data_type = "FLOAT"
    random_value_007.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_007.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_007.inputs[2].default_value = 6.0
    random_value_007.inputs[3].default_value = 7.0
    random_value_007.inputs[4].default_value = 0
    random_value_007.inputs[5].default_value = 100
    random_value_007.inputs[6].default_value = 0.5
    random_value_007.inputs[8].default_value = 32
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_1.inputs[10])

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
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_008.inputs[7])
    links.new(random_value_008.outputs[1], gem_in_holder_1.inputs[9])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.inputs[1].default_value = True
    set_position_003.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(transform_geometry_008.outputs[0], set_position_003.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.socket_idname = "NodeSocketGeometry"

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.target_element = "FACES"
    geometry_proximity_001.inputs[1].default_value = 0
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_001.inputs[3].default_value = 0
    links.new(reroute_002.outputs[0], geometry_proximity_001.inputs[0])
    links.new(geometry_proximity_001.outputs[0], set_position_003.inputs[2])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.inputs[3].default_value = False
    links.new(set_position_003.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(gem_in_holder_1.outputs[1], curve_to_mesh_002.inputs[1])
    links.new(gem_in_holder_1.outputs[2], curve_to_mesh_002.inputs[2])

    store_named_attribute_006 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_006.data_type = "BOOLEAN"
    store_named_attribute_006.domain = "POINT"
    store_named_attribute_006.inputs[1].default_value = True
    store_named_attribute_006.inputs[2].default_value = "gold"
    store_named_attribute_006.inputs[3].default_value = True
    links.new(store_named_attribute_006.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute_006.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.socket_idname = "NodeSocketGeometry"
    links.new(reroute.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(separate_geometry_001.outputs[1], reroute.inputs[0])
    links.new(reroute.outputs[0], reroute_002.inputs[0])

    frame_012 = nodes.new("NodeFrame")
    frame_012.label = ""
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketGeometry"
    links.new(join_geometry_006.outputs[0], reroute_001.inputs[0])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "GEOMETRY"
    links.new(reroute_001.outputs[0], switch_001.inputs[2])
    links.new(switch_001.outputs[0], join_geometry_007.inputs[0])

    group_input_001 = nodes.new("NodeGroupInput")
    links.new(group_input_001.outputs[0], switch_001.inputs[0])

    resample_curve_005 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_005.keep_last_segment = True
    resample_curve_005.inputs[1].default_value = True
    resample_curve_005.inputs[2].default_value = "Length"
    resample_curve_005.inputs[3].default_value = 10
    resample_curve_005.inputs[4].default_value = 0.004999999888241291
    links.new(resample_curve_005.outputs[0], instance_on_points_002.inputs[0])
    links.new(set_curve_tilt.outputs[0], resample_curve_005.inputs[0])

    auto_layout_nodes(group)
    return group
