import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group
from procedural_human.geo_node_groups.utilities.rivet import create_rivet_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group
from procedural_human.geo_node_groups.utilities.gem_in_holder import create_gem_in__holder_group
from procedural_human.geo_node_groups.utilities.join_splines import create_join__splines_group
from procedural_human.geo_node_groups.utilities.gold_on_band import create_gold_on__band_group
from procedural_human.geo_node_groups.utilities.gold_decorations import create_gold__decorations_group
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group
from procedural_human.geo_node_groups.utilities.swap_attr import create_swap__attr_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, vec_math_op


@geo_node_group
def create_chest_group():
    group_name = "Chest"
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
    bi_rail_loft.inputs[3].default_value = 6
    bi_rail_loft.inputs[5].default_value = 0.009999999776482582
    bi_rail_loft.inputs[6].default_value = 0.029999999329447746
    bi_rail_loft.inputs[7].default_value = 14
    bi_rail_loft.inputs[8].default_value = 102

    bézier_segment = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment.mode = "POSITION"
    bézier_segment.inputs[0].default_value = 200
    bézier_segment.inputs[1].default_value = Vector((0.0, -0.14000000059604645, 0.07000000029802322))
    bézier_segment.inputs[2].default_value = Vector((0.0, -0.20000000298023224, 0.2800000011920929))
    bézier_segment.inputs[3].default_value = Vector((0.0, -0.1600000113248825, 0.3100000023841858))
    bézier_segment.inputs[4].default_value = Vector((0.0, -0.08999998867511749, 0.4099999964237213))

    frame = nodes.new("NodeFrame")
    frame.label = "Centre Line"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20

    bézier_segment_001 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_001.mode = "OFFSET"
    bézier_segment_001.inputs[0].default_value = 200
    bézier_segment_001.inputs[1].default_value = Vector((-0.14999999105930328, 0.0, 0.07000000029802322))
    bézier_segment_001.inputs[2].default_value = Vector((-0.019999999552965164, 0.0, 0.05999999865889549))
    bézier_segment_001.inputs[3].default_value = Vector((0.0, 0.0, -0.029999999329447746))
    bézier_segment_001.inputs[4].default_value = Vector((-0.17000000178813934, 0.0, 0.1899999976158142))

    bézier_segment_002 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_002.mode = "OFFSET"
    bézier_segment_002.inputs[0].default_value = 200
    bézier_segment_002.inputs[1].default_value = Vector((-0.17000000178813934, 0.0, 0.1899999976158142))
    bézier_segment_002.inputs[2].default_value = Vector((0.05000000074505806, -0.20999999344348907, 0.030000001192092896))
    bézier_segment_002.inputs[3].default_value = Vector((0.019999999552965164, -0.029999999329447746, -0.029999999329447746))
    bézier_segment_002.inputs[4].default_value = Vector((-0.11999998986721039, -0.06000000238418579, 0.4000000059604645))

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    links.new(bézier_segment_002.outputs[0], join_geometry.inputs[0])
    links.new(bézier_segment_001.outputs[0], join_geometry.inputs[0])

    join_splines = nodes.new("GeometryNodeGroup")
    join_splines.node_tree = create_join__splines_group()
    links.new(join_splines.outputs[0], bi_rail_loft.inputs[1])
    links.new(join_geometry.outputs[0], join_splines.inputs[0])

    join_splines_1 = nodes.new("GeometryNodeGroup")
    join_splines_1.node_tree = create_join__splines_group()
    links.new(bézier_segment.outputs[0], join_splines_1.inputs[0])
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
    quadratic_bézier.inputs[2].default_value = Vector((0.0, -0.75, -0.12999999523162842))
    quadratic_bézier.inputs[3].default_value = Vector((1.0, 0.0, 0.0))

    quadratic_bézier_001 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_001.inputs[0].default_value = 40
    quadratic_bézier_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    quadratic_bézier_001.inputs[2].default_value = Vector((0.0, -0.1599999964237213, 0.1899999976158142))
    quadratic_bézier_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_002.outputs[0], bi_rail_loft.inputs[2])
    links.new(quadratic_bézier_001.outputs[0], join_geometry_002.inputs[0])
    links.new(quadratic_bézier.outputs[0], join_geometry_002.inputs[0])

    bézier_segment_003 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_003.mode = "OFFSET"
    bézier_segment_003.inputs[0].default_value = 200
    bézier_segment_003.inputs[1].default_value = Vector((-0.11999999731779099, -0.05999999865889549, 0.4000000059604645))
    bézier_segment_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    bézier_segment_003.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    bézier_segment_003.inputs[4].default_value = Vector((-0.09000000357627869, -0.05999999865889549, 0.41999998688697815))
    links.new(bézier_segment_003.outputs[0], join_geometry.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.label = "Profiles"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20

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

    quadratic_bézier_005 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_005.inputs[0].default_value = 40
    quadratic_bézier_005.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    quadratic_bézier_005.inputs[2].default_value = Vector((0.26999998092651367, -0.41999995708465576, 0.0))
    quadratic_bézier_005.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    links.new(quadratic_bézier_005.outputs[0], join_geometry_002.inputs[0])

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    links.new(bi_rail_loft.outputs[2], separate_x_y_z.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "LESS_EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    compare.inputs[1].default_value = 0.85999995470047
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
    compare.inputs[12].default_value = 0.3709999918937683
    links.new(separate_x_y_z.outputs[0], compare.inputs[0])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.mode = "FACES"
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    extrude_mesh.inputs[3].default_value = 0.0010000000474974513
    extrude_mesh.inputs[4].default_value = False

    pipes = nodes.new("GeometryNodeGroup")
    pipes.node_tree = create_pipes_group()

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.domain = "FACE"
    links.new(separate_geometry.outputs[0], pipes.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry.inputs[1])
    links.new(extrude_mesh.outputs[0], separate_geometry.inputs[0])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    links.new(pipes.outputs[0], join_geometry_001.inputs[0])
    links.new(extrude_mesh.outputs[0], join_geometry_001.inputs[0])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.mode = "EDGES"
    links.new(bi_rail_loft.outputs[0], mesh_to_curve.inputs[0])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.operation = "EQUAL"
    compare_002.data_type = "FLOAT"
    compare_002.mode = "ELEMENT"
    compare_002.inputs[1].default_value = 0.0
    compare_002.inputs[2].default_value = 0
    compare_002.inputs[3].default_value = 0
    compare_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[8].default_value = ""
    compare_002.inputs[9].default_value = ""
    compare_002.inputs[10].default_value = 0.8999999761581421
    compare_002.inputs[11].default_value = 0.08726649731397629
    compare_002.inputs[12].default_value = 0.0010000000474974513
    links.new(separate_x_y_z.outputs[0], compare_002.inputs[0])
    links.new(compare_002.outputs[0], mesh_to_curve.inputs[1])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.inputs[2].default_value = 0.6599999666213989
    curve_to_mesh.inputs[3].default_value = False

    quadrilateral = nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
    quadrilateral.mode = "RECTANGLE"
    quadrilateral.inputs[0].default_value = 0.0430000014603138
    quadrilateral.inputs[1].default_value = 0.006000000052154064
    quadrilateral.inputs[2].default_value = 4.0
    quadrilateral.inputs[3].default_value = 2.0
    quadrilateral.inputs[4].default_value = 1.0
    quadrilateral.inputs[5].default_value = 3.0
    quadrilateral.inputs[6].default_value = 1.0
    quadrilateral.inputs[7].default_value = Vector((-1.0, -1.0, 0.0))
    quadrilateral.inputs[8].default_value = Vector((1.0, -1.0, 0.0))
    quadrilateral.inputs[9].default_value = Vector((1.0, 1.0, 0.0))
    quadrilateral.inputs[10].default_value = Vector((-1.0, 1.0, 0.0))

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.domain = "FACE"
    set_shade_smooth.inputs[1].default_value = True
    set_shade_smooth.inputs[2].default_value = False
    links.new(curve_to_mesh.outputs[0], set_shade_smooth.inputs[0])

    subdivide_curve = nodes.new("GeometryNodeSubdivideCurve")
    subdivide_curve.inputs[1].default_value = 3
    links.new(quadrilateral.outputs[0], subdivide_curve.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.inputs[1].default_value = True
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(subdivide_curve.outputs[0], set_position.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position.outputs[0], separate_x_y_z_001.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.operation = "ABSOLUTE"
    math.inputs[1].default_value = 0.5
    math.inputs[2].default_value = 0.5
    links.new(separate_x_y_z_001.outputs[0], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.operation = "DIVIDE"
    math_001.inputs[1].default_value = 0.0215000007301569
    math_001.inputs[2].default_value = 0.5
    links.new(math.outputs[0], math_001.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.operation = "POWER"
    math_002.inputs[1].default_value = 2.0
    math_002.inputs[2].default_value = 0.5
    links.new(math_001.outputs[0], math_002.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.operation = "MULTIPLY"
    math_003.inputs[1].default_value = 0.0020000000949949026
    math_003.inputs[2].default_value = 0.5
    links.new(math_002.outputs[0], math_003.inputs[0])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.inputs[0].default_value = 0.0
    combine_x_y_z.inputs[2].default_value = 0.0
    links.new(combine_x_y_z.outputs[0], set_position.inputs[3])
    links.new(math_003.outputs[0], combine_x_y_z.inputs[1])

    fillet_curve = nodes.new("GeometryNodeFilletCurve")
    fillet_curve.inputs[1].default_value = 0.0010000000474974513
    fillet_curve.inputs[2].default_value = True
    fillet_curve.inputs[3].default_value = "Bézier"
    fillet_curve.inputs[4].default_value = 1
    links.new(fillet_curve.outputs[0], curve_to_mesh.inputs[1])
    links.new(set_position.outputs[0], fillet_curve.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.inputs[1].default_value = True
    set_curve_tilt.inputs[2].default_value = 3.1415927410125732
    links.new(set_curve_tilt.outputs[0], curve_to_mesh.inputs[0])

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.operation = "NOT"
    boolean_math_003.inputs[1].default_value = False
    links.new(boolean_math_003.outputs[0], extrude_mesh.inputs[1])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.operation = "OR"
    links.new(extrude_mesh.outputs[1], boolean_math.inputs[0])
    links.new(extrude_mesh.outputs[2], boolean_math.inputs[1])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.domain = "FACE"
    links.new(extrude_mesh.outputs[0], separate_geometry_001.inputs[0])
    links.new(boolean_math.outputs[0], separate_geometry_001.inputs[1])

    rivet = nodes.new("GeometryNodeGroup")
    rivet.node_tree = create_rivet_group()
    rivet.inputs[1].default_value = False
    rivet.inputs[2].default_value = -1.279999852180481
    rivet.inputs[3].default_value = 0.9399999976158142
    links.new(separate_geometry_001.outputs[1], rivet.inputs[0])
    links.new(rivet.outputs[0], join_geometry_001.inputs[0])

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "FACE"
    links.new(delete_geometry.outputs[0], join_geometry_001.inputs[0])
    links.new(set_shade_smooth.outputs[0], delete_geometry.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_001.outputs[0], separate_x_y_z_002.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.operation = "GREATER_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    compare_001.inputs[1].default_value = 0.0
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
    links.new(separate_x_y_z_002.outputs[0], compare_001.inputs[0])
    links.new(compare_001.outputs[0], delete_geometry.inputs[1])

    trim_curve = nodes.new("GeometryNodeTrimCurve")
    trim_curve.mode = "FACTOR"
    trim_curve.inputs[1].default_value = True
    trim_curve.inputs[2].default_value = 0.0
    trim_curve.inputs[3].default_value = 0.8569066524505615
    trim_curve.inputs[4].default_value = 0.0
    trim_curve.inputs[5].default_value = 1.0
    links.new(trim_curve.outputs[0], set_curve_tilt.inputs[0])
    links.new(mesh_to_curve.outputs[0], trim_curve.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.domain = "EDGE"
    set_shade_smooth_001.inputs[2].default_value = False

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.inputs[1].default_value = "Components"
    transform_geometry.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.0))
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry.inputs[4].default_value = Vector((1.0, -0.7799999713897705, 1.0))
    links.new(set_shade_smooth_001.outputs[0], transform_geometry.inputs[0])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    links.new(set_shade_smooth_001.outputs[0], join_geometry_003.inputs[0])

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.inputs[1].default_value = True
    links.new(flip_faces.outputs[0], join_geometry_003.inputs[0])
    links.new(transform_geometry.outputs[0], flip_faces.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Count"
    resample_curve.inputs[3].default_value = 47
    resample_curve.inputs[4].default_value = 0.10000000149011612

    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "FACE"

    position_003 = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_005 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_003.outputs[0], separate_x_y_z_005.inputs[0])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.operation = "GREATER_THAN"
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
    links.new(separate_x_y_z_005.outputs[0], compare_003.inputs[0])
    links.new(compare_003.outputs[0], delete_geometry_001.inputs[1])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_004.outputs[0], group_output.inputs[0])
    links.new(join_geometry_003.outputs[0], join_geometry_004.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    links.new(delete_geometry_001.outputs[0], join_geometry_005.inputs[0])

    trim_curve_001 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_001.mode = "FACTOR"
    trim_curve_001.inputs[1].default_value = True
    trim_curve_001.inputs[2].default_value = 0.0
    trim_curve_001.inputs[3].default_value = 0.8784530162811279
    trim_curve_001.inputs[4].default_value = 0.0
    trim_curve_001.inputs[5].default_value = 1.0
    links.new(trim_curve_001.outputs[0], resample_curve.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.inputs[1].default_value = "Components"
    transform_geometry_001.inputs[2].default_value = Vector((0.0, -0.0020000000949949026, 0.0))
    transform_geometry_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_001.outputs[0], trim_curve_001.inputs[0])
    links.new(join_splines_1.outputs[0], transform_geometry_001.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "gold"
    store_named_attribute.inputs[3].default_value = True
    links.new(join_geometry_005.outputs[0], store_named_attribute.inputs[0])

    gold_decorations = nodes.new("GeometryNodeGroup")
    gold_decorations.node_tree = create_gold__decorations_group()
    gold_decorations.inputs[1].default_value = 54
    gold_decorations.inputs[2].default_value = 4.0
    gold_decorations.inputs[3].default_value = 20
    links.new(gold_decorations.outputs[0], delete_geometry_001.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.keep_last_segment = True
    resample_curve_001.inputs[1].default_value = True
    resample_curve_001.inputs[2].default_value = "Count"
    resample_curve_001.inputs[3].default_value = 47
    resample_curve_001.inputs[4].default_value = 0.10000000149011612

    trim_curve_002 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_002.mode = "FACTOR"
    trim_curve_002.inputs[1].default_value = True
    trim_curve_002.inputs[2].default_value = 0.0
    trim_curve_002.inputs[3].default_value = 0.6187845468521118
    trim_curve_002.inputs[4].default_value = 0.0
    trim_curve_002.inputs[5].default_value = 1.0
    links.new(trim_curve_002.outputs[0], resample_curve_001.inputs[0])

    gold_decorations_1 = nodes.new("GeometryNodeGroup")
    gold_decorations_1.node_tree = create_gold__decorations_group()
    gold_decorations_1.inputs[1].default_value = 58
    gold_decorations_1.inputs[2].default_value = 2.0
    gold_decorations_1.inputs[3].default_value = 18
    links.new(gold_decorations_1.outputs[0], join_geometry_005.inputs[0])

    set_curve_normal = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal.inputs[1].default_value = True
    set_curve_normal.inputs[2].default_value = "Free"
    links.new(set_curve_normal.outputs[0], gold_decorations_1.inputs[0])
    links.new(resample_curve_001.outputs[0], set_curve_normal.inputs[0])

    sample_nearest_surface = nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.data_type = "FLOAT_VECTOR"
    sample_nearest_surface.inputs[2].default_value = 0
    sample_nearest_surface.inputs[3].default_value = [0.0, 0.0, 0.0]
    sample_nearest_surface.inputs[4].default_value = 0
    links.new(bi_rail_loft.outputs[0], sample_nearest_surface.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.legacy_corner_normals = False
    links.new(normal.outputs[0], sample_nearest_surface.inputs[1])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_normal = vec_math_op(
        group,
        "CROSS_PRODUCT",
        sample_nearest_surface.outputs[0],
        curve_tangent.outputs[0],
    )
    links.new(curve_normal, set_curve_normal.inputs[3])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.domain = "EDGE"
    links.new(separate_geometry_001.outputs[0], separate_geometry_002.inputs[0])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.operation = "AND"
    links.new(boolean_math_001.outputs[0], separate_geometry_002.inputs[1])
    links.new(extrude_mesh.outputs[1], boolean_math_001.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.mode = "EDGES"
    mesh_to_curve_001.inputs[1].default_value = True
    links.new(separate_geometry_002.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(mesh_to_curve_001.outputs[0], trim_curve_002.inputs[0])

    frame_005 = nodes.new("NodeFrame")
    frame_005.label = ""
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20

    frame_006 = nodes.new("NodeFrame")
    frame_006.label = ""
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20

    set_curve_tilt_001 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_001.inputs[1].default_value = True
    set_curve_tilt_001.inputs[2].default_value = -0.16580626368522644
    links.new(set_curve_tilt_001.outputs[0], gold_decorations.inputs[0])
    links.new(resample_curve.outputs[0], set_curve_tilt_001.inputs[0])

    separate_geometry_003 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_003.domain = "FACE"
    links.new(extrude_mesh.outputs[0], separate_geometry_003.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry_003.inputs[1])

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.inputs[1].default_value = 200000.0
    gold_on_band.inputs[2].default_value = 8.669999122619629
    gold_on_band.inputs[3].default_value = 1
    links.new(separate_geometry_003.outputs[0], gold_on_band.inputs[0])
    links.new(gold_on_band.outputs[0], join_geometry_005.inputs[0])

    frame_007 = nodes.new("NodeFrame")
    frame_007.label = "Gold"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "GEOMETRY"
    links.new(switch.outputs[0], join_geometry_004.inputs[0])

    group_input = nodes.new("NodeGroupInput")
    links.new(group_input.outputs[0], switch.inputs[0])

    bézier_segment_004 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_004.mode = "OFFSET"
    bézier_segment_004.inputs[0].default_value = 16
    bézier_segment_004.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    bézier_segment_004.inputs[2].default_value = Vector((1.0299999713897705, -0.6199999451637268, 0.0))
    bézier_segment_004.inputs[3].default_value = Vector((-0.8299999833106995, -0.4300000071525574, 0.0))
    bézier_segment_004.inputs[4].default_value = Vector((1.0, 0.0, 0.0))
    links.new(bézier_segment_004.outputs[0], join_geometry_002.inputs[0])

    boolean_math_004 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.operation = "AND"
    links.new(boolean_math_004.outputs[0], boolean_math_003.inputs[0])
    links.new(boolean_math_004.outputs[0], boolean_math_001.inputs[0])
    links.new(compare.outputs[0], boolean_math_004.inputs[0])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.operation = "GREATER_THAN"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    compare_004.inputs[1].default_value = 0.06999994814395905
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
    compare_004.inputs[12].default_value = 0.3709999918937683
    links.new(separate_x_y_z.outputs[1], compare_004.inputs[0])
    links.new(compare_004.outputs[0], boolean_math_004.inputs[1])

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    gem_in_holder.inputs[1].default_value = "ruby"
    gem_in_holder.inputs[2].default_value = False
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    gem_in_holder.inputs[6].default_value = True

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.mode = "COUNT"
    curve_to_points.inputs[1].default_value = 10
    curve_to_points.inputs[2].default_value = 0.10000000149011612

    for_each_geometry_element_input = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input.inputs[1].default_value = True
    links.new(curve_to_points.outputs[0], for_each_geometry_element_input.inputs[0])

    for_each_geometry_element_output = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.input_items.new("ROTATION", "Rotation")
    for_each_geometry_element_input.pair_with_output(for_each_geometry_element_output)
    for_each_geometry_element_output.active_input_index = 1
    links.new(curve_to_points.outputs[3], for_each_geometry_element_input.inputs[2])
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = "POINT"
    for_each_geometry_element_output.inspection_index = 0

    position_002 = nodes.new("GeometryNodeInputPosition")
    links.new(position_002.outputs[0], for_each_geometry_element_input.inputs[2])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.inputs[1].default_value = "Components"
    links.new(gem_in_holder.outputs[0], transform_geometry_002.inputs[0])
    links.new(for_each_geometry_element_input.outputs[2], transform_geometry_002.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.rotation_space = "LOCAL"
    rotate_rotation.inputs[1].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')
    links.new(for_each_geometry_element_input.outputs[2], rotate_rotation.inputs[0])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value.inputs[7])
    links.new(random_value.outputs[2], gem_in_holder.inputs[7])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.inputs[1].default_value = "Components"
    transform_geometry_003.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_003.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_002.outputs[0], transform_geometry_003.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_006.outputs[0], switch.inputs[2])
    links.new(store_named_attribute.outputs[0], join_geometry_006.inputs[0])
    links.new(for_each_geometry_element_output.outputs[2], join_geometry_006.inputs[0])

    trim_curve_003 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_003.mode = "FACTOR"
    trim_curve_003.inputs[1].default_value = True
    trim_curve_003.inputs[2].default_value = 0.04999999701976776
    trim_curve_003.inputs[3].default_value = 0.9000000953674316
    trim_curve_003.inputs[4].default_value = 0.0
    trim_curve_003.inputs[5].default_value = 1.0
    links.new(trim_curve_003.outputs[0], curve_to_points.inputs[0])
    links.new(set_curve_tilt.outputs[0], trim_curve_003.inputs[0])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.data_type = "FLOAT"
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_001.inputs[2].default_value = 0.25
    random_value_001.inputs[3].default_value = 0.550000011920929
    random_value_001.inputs[4].default_value = 0
    random_value_001.inputs[5].default_value = 100
    random_value_001.inputs[6].default_value = 0.5
    random_value_001.inputs[8].default_value = 0
    links.new(for_each_geometry_element_input.outputs[0], random_value_001.inputs[7])
    links.new(random_value_001.outputs[1], transform_geometry_002.inputs[4])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    store_named_attribute_001.inputs[1].default_value = True
    store_named_attribute_001.inputs[2].default_value = "skip"
    store_named_attribute_001.inputs[3].default_value = True
    links.new(store_named_attribute_001.outputs[0], for_each_geometry_element_output.inputs[1])
    links.new(transform_geometry_003.outputs[0], store_named_attribute_001.inputs[0])

    random_value_002 = nodes.new("FunctionNodeRandomValue")
    random_value_002.data_type = "FLOAT"
    random_value_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_002.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_002.inputs[2].default_value = 0.0
    random_value_002.inputs[3].default_value = 100.0
    random_value_002.inputs[4].default_value = 3
    random_value_002.inputs[5].default_value = 7
    random_value_002.inputs[6].default_value = 0.5
    random_value_002.inputs[8].default_value = 13
    links.new(for_each_geometry_element_input.outputs[0], random_value_002.inputs[7])
    links.new(random_value_002.outputs[1], gem_in_holder.inputs[10])

    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.rotation_space = "LOCAL"
    rotate_rotation_001.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
    links.new(rotate_rotation_001.outputs[0], transform_geometry_002.inputs[3])
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value_003.inputs[7])
    links.new(random_value_003.outputs[1], gem_in_holder.inputs[9])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value_004.inputs[7])
    links.new(random_value_004.outputs[2], gem_in_holder.inputs[5])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value_005.inputs[7])
    links.new(random_value_005.outputs[2], gem_in_holder.inputs[4])

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
    links.new(for_each_geometry_element_input.outputs[0], random_value_006.inputs[7])
    links.new(random_value_006.outputs[2], gem_in_holder.inputs[8])

    frame_008 = nodes.new("NodeFrame")
    frame_008.label = "Broaches"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20

    set_shade_smooth_002 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_002.domain = "FACE"
    set_shade_smooth_002.inputs[1].default_value = True
    set_shade_smooth_002.inputs[2].default_value = True
    links.new(set_shade_smooth_002.outputs[0], set_shade_smooth_001.inputs[0])
    links.new(join_geometry_001.outputs[0], set_shade_smooth_002.inputs[0])

    edge_angle = nodes.new("GeometryNodeInputMeshEdgeAngle")

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.operation = "GREATER_THAN"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    compare_005.inputs[1].default_value = 1.0
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
    compare_005.inputs[12].default_value = 0.0010000000474974513
    links.new(edge_angle.outputs[0], compare_005.inputs[0])
    links.new(compare_005.outputs[0], set_shade_smooth_001.inputs[1])

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
    links.new(is_edge_boundary.outputs[0], mesh_to_curve_002.inputs[1])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.inputs[1].default_value = True
    set_spline_cyclic.inputs[2].default_value = False

    trim_curve_004 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_004.mode = "FACTOR"
    trim_curve_004.inputs[1].default_value = True
    trim_curve_004.inputs[2].default_value = 0.6629834175109863
    trim_curve_004.inputs[3].default_value = 0.9834254384040833
    trim_curve_004.inputs[4].default_value = 0.0
    trim_curve_004.inputs[5].default_value = 1.0
    links.new(set_spline_cyclic.outputs[0], trim_curve_004.inputs[0])

    curve_to_points_001 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.mode = "COUNT"
    curve_to_points_001.inputs[1].default_value = 50
    curve_to_points_001.inputs[2].default_value = 0.10000000149011612
    links.new(trim_curve_004.outputs[0], curve_to_points_001.inputs[0])

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.capture_items.new("VECTOR", "Value")
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    links.new(bi_rail_loft.outputs[0], capture_attribute.inputs[0])
    links.new(capture_attribute.outputs[0], extrude_mesh.inputs[0])

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.legacy_corner_normals = False
    links.new(normal_001.outputs[0], capture_attribute.inputs[1])

    set_curve_normal_001 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.inputs[1].default_value = True
    set_curve_normal_001.inputs[2].default_value = "Free"
    links.new(set_curve_normal_001.outputs[0], set_spline_cyclic.inputs[0])
    links.new(mesh_to_curve_002.outputs[0], set_curve_normal_001.inputs[0])
    links.new(capture_attribute.outputs[1], set_curve_normal_001.inputs[3])

    position_004 = nodes.new("GeometryNodeInputPosition")

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.inputs[1].default_value = True
    links.new(curve_to_points_001.outputs[0], for_each_geometry_element_input_001.inputs[0])

    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.input_items.new("ROTATION", "Rotation")
    for_each_geometry_element_input_001.pair_with_output(for_each_geometry_element_output_001)
    for_each_geometry_element_output_001.active_input_index = 1
    links.new(position_004.outputs[0], for_each_geometry_element_input_001.inputs[2])
    links.new(curve_to_points_001.outputs[3], for_each_geometry_element_input_001.inputs[2])
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_006.inputs[0])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.inputs[1].default_value = "Components"
    transform_geometry_004.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_004.inputs[2])
    links.new(gem_in_holder_1.outputs[4], transform_geometry_004.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.rotation_space = "LOCAL"
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, -1.5707963705062866, 0.0), 'XYZ')
    links.new(rotate_rotation_002.outputs[0], transform_geometry_004.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[2], rotate_rotation_002.inputs[0])

    frame_009 = nodes.new("NodeFrame")
    frame_009.label = "Random Wings"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20

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

    reroute = nodes.new("NodeReroute")
    reroute.socket_idname = "NodeSocketGeometry"
    links.new(reroute.outputs[0], mesh_to_curve_002.inputs[0])
    links.new(separate_geometry.outputs[0], reroute.inputs[0])

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    distribute_points_on_faces.inputs[1].default_value = True
    distribute_points_on_faces.inputs[2].default_value = 0.0
    distribute_points_on_faces.inputs[3].default_value = 10.0
    distribute_points_on_faces.inputs[4].default_value = 5000.0
    distribute_points_on_faces.inputs[5].default_value = 1.0
    distribute_points_on_faces.inputs[6].default_value = 0
    links.new(reroute.outputs[0], distribute_points_on_faces.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.inputs[1].default_value = True
    instance_on_points.inputs[3].default_value = False
    instance_on_points.inputs[4].default_value = 0
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    links.new(distribute_points_on_faces.outputs[0], instance_on_points.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.inputs[0].default_value = 0.0020000000949949026
    ico_sphere.inputs[1].default_value = 2

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "INSTANCE"
    store_named_attribute_002.inputs[1].default_value = True
    store_named_attribute_002.inputs[2].default_value = "ruby"
    links.new(instance_on_points.outputs[0], store_named_attribute_002.inputs[0])

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
    links.new(random_value_009.outputs[3], store_named_attribute_002.inputs[3])

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.operation = "NOT"
    boolean_math_002.inputs[1].default_value = False
    links.new(random_value_009.outputs[3], boolean_math_002.inputs[0])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "INSTANCE"
    store_named_attribute_003.inputs[1].default_value = True
    store_named_attribute_003.inputs[2].default_value = "saphire"
    links.new(store_named_attribute_002.outputs[0], store_named_attribute_003.inputs[0])
    links.new(boolean_math_002.outputs[0], store_named_attribute_003.inputs[3])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.inputs[1].default_value = True
    realize_instances.inputs[2].default_value = True
    realize_instances.inputs[3].default_value = 0
    links.new(store_named_attribute_003.outputs[0], realize_instances.inputs[0])
    links.new(realize_instances.outputs[0], join_geometry_006.inputs[0])

    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.domain = "FACE"
    set_shade_smooth_003.inputs[1].default_value = True
    set_shade_smooth_003.inputs[2].default_value = True
    links.new(set_shade_smooth_003.outputs[0], instance_on_points.inputs[2])
    links.new(ico_sphere.outputs[0], set_shade_smooth_003.inputs[0])

    frame_010 = nodes.new("NodeFrame")
    frame_010.label = "Random Jewels"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20

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
    links.new(reroute_001.outputs[0], distribute_points_on_faces_001.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.target_element = "POINTS"
    geometry_proximity.inputs[1].default_value = 0
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity.inputs[3].default_value = 0
    links.new(for_each_geometry_element_output_001.outputs[2], geometry_proximity.inputs[0])

    compare_006 = nodes.new("FunctionNodeCompare")
    compare_006.operation = "LESS_THAN"
    compare_006.data_type = "FLOAT"
    compare_006.mode = "ELEMENT"
    compare_006.inputs[1].default_value = 0.006000000052154064
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
    links.new(geometry_proximity.outputs[1], compare_006.inputs[0])
    links.new(compare_006.outputs[0], distribute_points_on_faces_001.inputs[1])

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
    links.new(distribute_points_on_faces_001.outputs[0], instance_on_points_001.inputs[0])
    links.new(distribute_points_on_faces_001.outputs[2], instance_on_points_001.inputs[5])

    random_value_010 = nodes.new("FunctionNodeRandomValue")
    random_value_010.data_type = "FLOAT"
    random_value_010.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_010.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_010.inputs[2].default_value = 0.20000000298023224
    random_value_010.inputs[3].default_value = 0.5
    random_value_010.inputs[4].default_value = 0
    random_value_010.inputs[5].default_value = 100
    random_value_010.inputs[6].default_value = 0.5
    random_value_010.inputs[7].default_value = 0
    random_value_010.inputs[8].default_value = 0
    links.new(random_value_010.outputs[1], instance_on_points_001.inputs[6])

    frame_011 = nodes.new("NodeFrame")
    frame_011.label = "Larger Jewels"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.inputs[1].default_value = True
    realize_instances_001.inputs[2].default_value = True
    realize_instances_001.inputs[3].default_value = 0

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.inputs[1].default_value = "Components"
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    links.new(transform_geometry_005.outputs[0], instance_on_points_001.inputs[2])
    links.new(gem_in_holder_2.outputs[0], transform_geometry_005.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.inputs[2].default_value = "ruby"
    swap_attr.inputs[3].default_value = "saphire"
    links.new(swap_attr.outputs[0], join_geometry_006.inputs[0])
    links.new(realize_instances_001.outputs[0], swap_attr.inputs[0])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.capture_items.new("INT", "Value")
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "INSTANCE"
    links.new(capture_attribute_001.outputs[0], realize_instances_001.inputs[0])
    links.new(instance_on_points_001.outputs[0], capture_attribute_001.inputs[0])
    links.new(capture_attribute_001.outputs[1], swap_attr.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    links.new(index.outputs[0], capture_attribute_001.inputs[1])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[1].default_value = True
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(transform_geometry_004.outputs[0], set_position_001.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.socket_idname = "NodeSocketGeometry"
    links.new(reroute_002.outputs[0], reroute_001.inputs[0])
    links.new(separate_geometry_001.outputs[1], reroute_002.inputs[0])

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.target_element = "FACES"
    geometry_proximity_001.inputs[1].default_value = 0
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_001.inputs[3].default_value = 0
    links.new(reroute_002.outputs[0], geometry_proximity_001.inputs[0])
    links.new(geometry_proximity_001.outputs[0], set_position_001.inputs[2])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.inputs[3].default_value = False
    links.new(set_position_001.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(gem_in_holder_1.outputs[1], curve_to_mesh_001.inputs[1])
    links.new(gem_in_holder_1.outputs[2], curve_to_mesh_001.inputs[2])

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    store_named_attribute_004.inputs[1].default_value = True
    store_named_attribute_004.inputs[2].default_value = "gold"
    store_named_attribute_004.inputs[3].default_value = True
    links.new(store_named_attribute_004.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(curve_to_mesh_001.outputs[0], store_named_attribute_004.inputs[0])

    auto_layout_nodes(group)
    return group
