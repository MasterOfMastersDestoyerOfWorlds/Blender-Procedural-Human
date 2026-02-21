import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group
from procedural_human.geo_node_groups.utilities.join_splines import create_join__splines_group
from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group

@geo_node_group
def create_waist_group():
    group_name = "Waist"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (10900.0, 640.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    bi_rail_loft = nodes.new("GeometryNodeGroup")
    bi_rail_loft.name = "Bi-Rail Loft"
    bi_rail_loft.label = ""
    bi_rail_loft.location = (-820.0, -1320.0)
    bi_rail_loft.node_tree = create_bi_rail_loft_group()
    bi_rail_loft.bl_label = "Group"
    # Smoothing
    bi_rail_loft.inputs[3].default_value = 0
    # Menu
    bi_rail_loft.inputs[4].default_value = "Resolution"
    # X Spacing
    bi_rail_loft.inputs[5].default_value = 0.009999999776482582
    # Y Spacing
    bi_rail_loft.inputs[6].default_value = 0.029999999329447746
    # X Resolution
    bi_rail_loft.inputs[7].default_value = 14
    # Y Resolution
    bi_rail_loft.inputs[8].default_value = 9
    # Links for bi_rail_loft

    bézier_segment = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment.name = "Bézier Segment"
    bézier_segment.label = ""
    bézier_segment.location = (29.0, -35.800018310546875)
    bézier_segment.bl_label = "Bézier Segment"
    bézier_segment.mode = "OFFSET"
    # Resolution
    bézier_segment.inputs[0].default_value = 200
    # Start
    bézier_segment.inputs[1].default_value = Vector((0.0, -0.14000000059604645, 0.07000000029802322))
    # Start Handle
    bézier_segment.inputs[2].default_value = Vector((0.0, 0.0, -0.019999999552965164))
    # End Handle
    bézier_segment.inputs[3].default_value = Vector((0.0, 0.0, 0.07999999821186066))
    # End
    bézier_segment.inputs[4].default_value = Vector((0.0, -0.18999998271465302, -0.049999989569187164))
    # Links for bézier_segment

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Centre Line"
    frame.location = (29.0, -35.79998779296875)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    bézier_segment_001 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_001.name = "Bézier Segment.001"
    bézier_segment_001.label = ""
    bézier_segment_001.location = (29.0, -35.79998779296875)
    bézier_segment_001.bl_label = "Bézier Segment"
    bézier_segment_001.mode = "OFFSET"
    # Resolution
    bézier_segment_001.inputs[0].default_value = 200
    # Start
    bézier_segment_001.inputs[1].default_value = Vector((-0.14999999105930328, 0.0, 0.07000000029802322))
    # Start Handle
    bézier_segment_001.inputs[2].default_value = Vector((0.0, 0.0, -0.029999999329447746))
    # End Handle
    bézier_segment_001.inputs[3].default_value = Vector((0.0, 0.0, 0.04999999701976776))
    # End
    bézier_segment_001.inputs[4].default_value = Vector((-0.1899999976158142, 0.0, -0.029999990016222))
    # Links for bézier_segment_001

    join_splines = nodes.new("GeometryNodeGroup")
    join_splines.name = "Group"
    join_splines.label = ""
    join_splines.location = (769.0, -55.79998779296875)
    join_splines.node_tree = create_join__splines_group()
    join_splines.bl_label = "Group"
    # Links for join_splines
    links.new(join_splines.outputs[0], bi_rail_loft.inputs[1])

    join_splines_1 = nodes.new("GeometryNodeGroup")
    join_splines_1.name = "Group.001"
    join_splines_1.label = ""
    join_splines_1.location = (618.0, -131.60000610351562)
    join_splines_1.node_tree = create_join__splines_group()
    join_splines_1.bl_label = "Group"
    # Links for join_splines_1
    links.new(join_splines_1.outputs[0], bi_rail_loft.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "Outside"
    frame_001.location = (29.0, -651.6000366210938)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Centre"
    frame_002.location = (180.0, -35.800018310546875)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Rails"
    frame_003.location = (-2358.0, -352.5999755859375)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    quadratic_bézier = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier.name = "Quadratic Bézier"
    quadratic_bézier.label = ""
    quadratic_bézier.location = (29.0, -55.7999267578125)
    quadratic_bézier.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier.inputs[0].default_value = 40
    # Start
    quadratic_bézier.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier.inputs[2].default_value = Vector((0.0, -0.6000000238418579, -0.1199999749660492))
    # End
    quadratic_bézier.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (889.0, -35.7999267578125)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002
    links.new(join_geometry_002.outputs[0], bi_rail_loft.inputs[2])
    links.new(quadratic_bézier.outputs[0], join_geometry_002.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Profiles"
    frame_004.location = (-2329.0, -1724.2000732421875)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    quadratic_bézier_005 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_005.name = "Quadratic Bézier.005"
    quadratic_bézier_005.label = ""
    quadratic_bézier_005.location = (549.0, -175.7999267578125)
    quadratic_bézier_005.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_005.inputs[0].default_value = 40
    # Start
    quadratic_bézier_005.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier_005.inputs[2].default_value = Vector((-2.2351741790771484e-08, -0.7599999308586121, 0.25999999046325684))
    # End
    quadratic_bézier_005.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier_005
    links.new(quadratic_bézier_005.outputs[0], join_geometry_002.inputs[0])

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (9740.0, 240.0)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.0))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, -0.7799999713897705, 1.0))
    # Links for transform_geometry

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (10140.0, 320.0)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.name = "Flip Faces"
    flip_faces.label = ""
    flip_faces.location = (9920.0, 240.0)
    flip_faces.bl_label = "Flip Faces"
    # Selection
    flip_faces.inputs[1].default_value = True
    # Links for flip_faces
    links.new(flip_faces.outputs[0], join_geometry_003.inputs[0])
    links.new(transform_geometry.outputs[0], flip_faces.inputs[0])

    reverse_curve = nodes.new("GeometryNodeReverseCurve")
    reverse_curve.name = "Reverse Curve"
    reverse_curve.label = ""
    reverse_curve.location = (338.0, -91.60000610351562)
    reverse_curve.bl_label = "Reverse Curve"
    # Selection
    reverse_curve.inputs[1].default_value = True
    # Links for reverse_curve
    links.new(reverse_curve.outputs[0], join_splines_1.inputs[0])
    links.new(bézier_segment.outputs[0], reverse_curve.inputs[0])

    reverse_curve_001 = nodes.new("GeometryNodeReverseCurve")
    reverse_curve_001.name = "Reverse Curve.001"
    reverse_curve_001.label = ""
    reverse_curve_001.location = (529.0, -55.79998779296875)
    reverse_curve_001.bl_label = "Reverse Curve"
    # Selection
    reverse_curve_001.inputs[1].default_value = True
    # Links for reverse_curve_001
    links.new(reverse_curve_001.outputs[0], join_splines.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (249.0, -55.79998779296875)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.004999999888241291, 0.0))
    # Rotation
    transform_geometry_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_001
    links.new(transform_geometry_001.outputs[0], reverse_curve_001.inputs[0])
    links.new(bézier_segment_001.outputs[0], transform_geometry_001.inputs[0])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.name = "Pipes"
    pipes.label = ""
    pipes.location = (829.0, -35.79998779296875)
    pipes.node_tree = create_pipes_group()
    pipes.bl_label = "Group"
    # Links for pipes

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (1320.0, -1100.0)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(pipes.outputs[0], join_geometry_005.inputs[0])

    quadratic_bézier_006 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_006.name = "Quadratic Bézier.006"
    quadratic_bézier_006.label = ""
    quadratic_bézier_006.location = (309.0, -135.7999267578125)
    quadratic_bézier_006.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_006.inputs[0].default_value = 40
    # Start
    quadratic_bézier_006.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier_006.inputs[2].default_value = Vector((-0.18000002205371857, -0.6399999260902405, 0.31999996304512024))
    # End
    quadratic_bézier_006.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier_006
    links.new(quadratic_bézier_006.outputs[0], join_geometry_002.inputs[0])

    closure_input = nodes.new("NodeClosureInput")
    closure_input.name = "Closure Input"
    closure_input.label = ""
    closure_input.location = (-1140.0, -1780.0)
    closure_input.bl_label = "Closure Input"
    # Links for closure_input

    closure_output = nodes.new("NodeClosureOutput")
    closure_output.name = "Closure Output"
    closure_output.label = ""
    closure_output.location = (-680.0, -1780.0)
    closure_output.bl_label = "Closure Output"
    closure_output.active_input_index = 0
    closure_output.active_output_index = 0
    closure_output.define_signature = False
    # Links for closure_output
    links.new(closure_output.outputs[0], bi_rail_loft.inputs[9])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (-960.0, -1800.0)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(float_curve.outputs[0], closure_output.inputs[0])
    links.new(closure_input.outputs[0], float_curve.inputs[1])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.label = ""
    extrude_mesh.location = (-60.0, -1300.0)
    extrude_mesh.bl_label = "Extrude Mesh"
    extrude_mesh.mode = "FACES"
    # Offset
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.0020000000949949026
    # Individual
    extrude_mesh.inputs[4].default_value = False
    # Links for extrude_mesh

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (-480.0, -1440.0)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(bi_rail_loft.outputs[2], separate_x_y_z.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (-300.0, -1500.0)
    compare_001.bl_label = "Compare"
    compare_001.operation = "GREATER_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = 0.5999999642372131
    # A
    compare_001.inputs[2].default_value = 0
    # B
    compare_001.inputs[3].default_value = 0
    # A
    compare_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_001.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_001.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_001.inputs[8].default_value = ""
    # B
    compare_001.inputs[9].default_value = ""
    # C
    compare_001.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_001.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_001.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_001
    links.new(separate_x_y_z.outputs[1], compare_001.inputs[0])
    links.new(compare_001.outputs[0], extrude_mesh.inputs[1])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.name = "Separate Geometry.001"
    separate_geometry_001.label = ""
    separate_geometry_001.location = (320.0, -1280.0)
    separate_geometry_001.bl_label = "Separate Geometry"
    separate_geometry_001.domain = "FACE"
    # Links for separate_geometry_001
    links.new(separate_geometry_001.outputs[1], join_geometry_005.inputs[0])
    links.new(extrude_mesh.outputs[0], separate_geometry_001.inputs[0])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (140.0, -1380.0)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "OR"
    # Links for boolean_math
    links.new(boolean_math.outputs[0], separate_geometry_001.inputs[1])
    links.new(extrude_mesh.outputs[1], boolean_math.inputs[0])
    links.new(extrude_mesh.outputs[2], boolean_math.inputs[1])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (680.0, -1240.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(separate_geometry_001.outputs[0], store_named_attribute.inputs[0])
    links.new(store_named_attribute.outputs[0], join_geometry_005.inputs[0])

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.name = "Gold on Band"
    gold_on_band.label = ""
    gold_on_band.location = (478.0, -944.7999267578125)
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.bl_label = "Group"
    # Density
    gold_on_band.inputs[1].default_value = 100000.0
    # W
    gold_on_band.inputs[2].default_value = 1.5699999332427979
    # Seed
    gold_on_band.inputs[3].default_value = 1
    # Links for gold_on_band
    links.new(separate_geometry_001.outputs[0], gold_on_band.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.label = ""
    join_geometry_006.location = (2758.0, -764.7999267578125)
    join_geometry_006.bl_label = "Join Geometry"
    # Links for join_geometry_006
    links.new(gold_on_band.outputs[0], join_geometry_006.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (9840.0, 560.0)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(switch.outputs[0], join_geometry_003.inputs[0])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (9840.0, 620.0)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch.inputs[0])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.name = "Separate Geometry.002"
    separate_geometry_002.label = ""
    separate_geometry_002.location = (669.0, -35.79998779296875)
    separate_geometry_002.bl_label = "Separate Geometry"
    separate_geometry_002.domain = "EDGE"
    # Links for separate_geometry_002
    links.new(extrude_mesh.outputs[0], separate_geometry_002.inputs[0])
    links.new(separate_geometry_002.outputs[0], pipes.inputs[0])

    edge_vertices = nodes.new("GeometryNodeInputMeshEdgeVertices")
    edge_vertices.name = "Edge Vertices"
    edge_vertices.label = ""
    edge_vertices.location = (29.0, -35.79998779296875)
    edge_vertices.bl_label = "Edge Vertices"
    # Links for edge_vertices

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (189.0, -35.79998779296875)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "SUBTRACT"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(edge_vertices.outputs[3], vector_math.inputs[0])
    links.new(edge_vertices.outputs[2], vector_math.inputs[1])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.label = ""
    compare_002.location = (349.0, -35.79998779296875)
    compare_002.bl_label = "Compare"
    compare_002.operation = "EQUAL"
    compare_002.data_type = "VECTOR"
    compare_002.mode = "DIRECTION"
    # A
    compare_002.inputs[0].default_value = 0.0
    # B
    compare_002.inputs[1].default_value = 0.0
    # A
    compare_002.inputs[2].default_value = 0
    # B
    compare_002.inputs[3].default_value = 0
    # B
    compare_002.inputs[5].default_value = [0.0, 0.0, 1.0]
    # A
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_002.inputs[8].default_value = ""
    # B
    compare_002.inputs[9].default_value = ""
    # C
    compare_002.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_002.inputs[11].default_value = 1.5707963705062866
    # Epsilon
    compare_002.inputs[12].default_value = 0.3109999895095825
    # Links for compare_002
    links.new(vector_math.outputs[0], compare_002.inputs[4])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.label = ""
    boolean_math_001.location = (509.0, -35.79998779296875)
    boolean_math_001.bl_label = "Boolean Math"
    boolean_math_001.operation = "AND"
    # Links for boolean_math_001
    links.new(compare_002.outputs[0], boolean_math_001.inputs[0])
    links.new(boolean_math_001.outputs[0], separate_geometry_002.inputs[1])
    links.new(extrude_mesh.outputs[1], boolean_math_001.inputs[1])

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = "Pipes"
    frame_005.location = (-409.0, -884.2000122070312)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (1009.0, -189.0)
    instance_on_points.bl_label = "Instance on Points"
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Links for instance_on_points

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.name = "Gem in Holder"
    gem_in_holder.label = ""
    gem_in_holder.location = (169.0, -409.0)
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.bl_label = "Group"
    # Gem Radius
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder.inputs[2].default_value = True
    # Scale
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder.inputs[4].default_value = 20
    # Seed
    gem_in_holder.inputs[5].default_value = 10
    # Wings
    gem_in_holder.inputs[6].default_value = False
    # Array Count
    gem_in_holder.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder.inputs[8].default_value = 10
    # Split
    gem_in_holder.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder.inputs[10].default_value = 2.5099997520446777
    # Links for gem_in_holder
    links.new(gem_in_holder.outputs[0], instance_on_points.inputs[2])

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (189.0, -29.0)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.label = ""
    capture_attribute.location = (-380.0, -1320.0)
    capture_attribute.bl_label = "Capture Attribute"
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    # Links for capture_attribute
    links.new(capture_attribute.outputs[0], extrude_mesh.inputs[0])
    links.new(capture_attribute.outputs[1], separate_x_y_z_001.inputs[0])
    links.new(bi_rail_loft.outputs[0], capture_attribute.inputs[0])
    links.new(bi_rail_loft.outputs[2], capture_attribute.inputs[1])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (349.0, -29.0)
    compare.bl_label = "Compare"
    compare.operation = "GREATER_THAN"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.6800000071525574
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare.inputs[8].default_value = ""
    # B
    compare.inputs[9].default_value = ""
    # C
    compare.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513
    # Links for compare
    links.new(separate_x_y_z_001.outputs[1], compare.inputs[0])
    links.new(compare.outputs[0], instance_on_points.inputs[1])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.label = ""
    align_rotation_to_vector.location = (549.0, -269.0)
    align_rotation_to_vector.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector.axis = "Z"
    align_rotation_to_vector.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector
    links.new(align_rotation_to_vector.outputs[0], instance_on_points.inputs[5])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (549.0, -409.0)
    random_value.bl_label = "Random Value"
    random_value.data_type = "FLOAT"
    # Min
    random_value.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value.inputs[2].default_value = -0.09999999403953552
    # Max
    random_value.inputs[3].default_value = 0.09999993443489075
    # Min
    random_value.inputs[4].default_value = 0
    # Max
    random_value.inputs[5].default_value = 100
    # Probability
    random_value.inputs[6].default_value = 0.5
    # ID
    random_value.inputs[7].default_value = 0
    # Seed
    random_value.inputs[8].default_value = 0
    # Links for random_value

    separate_geometry_003 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_003.name = "Separate Geometry.003"
    separate_geometry_003.label = ""
    separate_geometry_003.location = (29.0, -189.0)
    separate_geometry_003.bl_label = "Separate Geometry"
    separate_geometry_003.domain = "FACE"
    # Links for separate_geometry_003
    links.new(extrude_mesh.outputs[0], separate_geometry_003.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry_003.inputs[1])

    mesh_to_points = nodes.new("GeometryNodeMeshToPoints")
    mesh_to_points.name = "Mesh to Points"
    mesh_to_points.label = ""
    mesh_to_points.location = (349.0, -189.0)
    mesh_to_points.bl_label = "Mesh to Points"
    mesh_to_points.mode = "FACES"
    # Selection
    mesh_to_points.inputs[1].default_value = True
    # Position
    mesh_to_points.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Radius
    mesh_to_points.inputs[3].default_value = 0.05000000074505806
    # Links for mesh_to_points
    links.new(mesh_to_points.outputs[0], instance_on_points.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.label = ""
    normal.location = (189.0, -309.0)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = False
    # Links for normal

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (189.0, -189.0)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 1
    capture_attribute_001.domain = "FACE"
    # Links for capture_attribute_001
    links.new(capture_attribute_001.outputs[0], mesh_to_points.inputs[0])
    links.new(separate_geometry_003.outputs[0], capture_attribute_001.inputs[0])
    links.new(normal.outputs[0], capture_attribute_001.inputs[1])
    links.new(capture_attribute_001.outputs[1], align_rotation_to_vector.inputs[2])
    links.new(bi_rail_loft.outputs[2], capture_attribute_001.inputs[2])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (1349.0, -169.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_002.name = "Separate XYZ.002"
    separate_x_y_z_002.label = ""
    separate_x_y_z_002.location = (409.0, -589.0)
    separate_x_y_z_002.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_002
    links.new(capture_attribute_001.outputs[2], separate_x_y_z_002.inputs[0])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (569.0, -589.0)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    # From Min
    map_range.inputs[1].default_value = 0.0
    # From Max
    map_range.inputs[2].default_value = 1.0
    # To Min
    map_range.inputs[3].default_value = 0.46000003814697266
    # To Max
    map_range.inputs[4].default_value = 0.28999999165534973
    # Steps
    map_range.inputs[5].default_value = 4.0
    # Vector
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range
    links.new(separate_x_y_z_002.outputs[0], map_range.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (789.0, -469.0)
    math.bl_label = "Math"
    math.operation = "ADD"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(map_range.outputs[0], math.inputs[0])
    links.new(random_value.outputs[1], math.inputs[1])
    links.new(math.outputs[0], instance_on_points.inputs[6])

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.name = "Capture Attribute.002"
    capture_attribute_002.label = ""
    capture_attribute_002.location = (1189.0, -189.0)
    capture_attribute_002.bl_label = "Capture Attribute"
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "INSTANCE"
    # Links for capture_attribute_002
    links.new(capture_attribute_002.outputs[0], realize_instances.inputs[0])
    links.new(instance_on_points.outputs[0], capture_attribute_002.inputs[0])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (1189.0, -309.0)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], capture_attribute_002.inputs[1])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (10720.0, 660.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True
    # Links for set_shade_smooth
    links.new(set_shade_smooth.outputs[0], group_output.inputs[0])
    links.new(join_geometry_003.outputs[0], set_shade_smooth.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = "Gold"
    frame_006.location = (1082.0, 1264.7999267578125)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (429.0, -35.7999267578125)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "FACE"
    # Links for delete_geometry
    links.new(join_geometry_005.outputs[0], delete_geometry.inputs[0])

    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_007.name = "Join Geometry.007"
    join_geometry_007.label = ""
    join_geometry_007.location = (9500.0, 320.0)
    join_geometry_007.bl_label = "Join Geometry"
    # Links for join_geometry_007
    links.new(join_geometry_007.outputs[0], transform_geometry.inputs[0])
    links.new(join_geometry_007.outputs[0], join_geometry_003.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (29.0, -195.7999267578125)
    position.bl_label = "Position"
    # Links for position

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_003.name = "Separate XYZ.003"
    separate_x_y_z_003.label = ""
    separate_x_y_z_003.location = (29.0, -255.7999267578125)
    separate_x_y_z_003.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_003
    links.new(position.outputs[0], separate_x_y_z_003.inputs[0])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (189.0, -255.7999267578125)
    compare_003.bl_label = "Compare"
    compare_003.operation = "EQUAL"
    compare_003.data_type = "FLOAT"
    compare_003.mode = "ELEMENT"
    # B
    compare_003.inputs[1].default_value = 0.0
    # A
    compare_003.inputs[2].default_value = 0
    # B
    compare_003.inputs[3].default_value = 0
    # A
    compare_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_003.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_003.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_003.inputs[8].default_value = ""
    # B
    compare_003.inputs[9].default_value = ""
    # C
    compare_003.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_003.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_003.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_003
    links.new(separate_x_y_z_003.outputs[0], compare_003.inputs[0])
    links.new(compare_003.outputs[0], delete_geometry.inputs[1])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (789.0, -55.7999267578125)
    set_position.bl_label = "Set Position"
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position
    links.new(set_position.outputs[0], join_geometry_007.inputs[0])
    links.new(delete_geometry.outputs[0], set_position.inputs[0])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (369.0, -255.7999267578125)
    compare_004.bl_label = "Compare"
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    # B
    compare_004.inputs[1].default_value = 0.0
    # A
    compare_004.inputs[2].default_value = 0
    # B
    compare_004.inputs[3].default_value = 0
    # A
    compare_004.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_004.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_004.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_004.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_004.inputs[8].default_value = ""
    # B
    compare_004.inputs[9].default_value = ""
    # C
    compare_004.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_004.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_004.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_004
    links.new(separate_x_y_z_003.outputs[0], compare_004.inputs[0])
    links.new(compare_004.outputs[0], set_position.inputs[1])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (569.0, -295.7999267578125)
    position_001.bl_label = "Position"
    # Links for position_001

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (789.0, -295.7999267578125)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "MULTIPLY"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 1.0, 1.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(position_001.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], set_position.inputs[2])

    frame_007 = nodes.new("NodeFrame")
    frame_007.name = "Frame.007"
    frame_007.label = "Merge Centre Line"
    frame_007.location = (1811.0, -1084.2000732421875)
    frame_007.bl_label = "Frame"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20
    # Links for frame_007

    separate_geometry_004 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_004.name = "Separate Geometry.004"
    separate_geometry_004.label = ""
    separate_geometry_004.location = (349.0, -35.800048828125)
    separate_geometry_004.bl_label = "Separate Geometry"
    separate_geometry_004.domain = "EDGE"
    # Links for separate_geometry_004
    links.new(separate_geometry_002.outputs[0], separate_geometry_004.inputs[0])

    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_004.name = "Separate XYZ.004"
    separate_x_y_z_004.label = ""
    separate_x_y_z_004.location = (29.0, -135.800048828125)
    separate_x_y_z_004.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_004
    links.new(capture_attribute.outputs[1], separate_x_y_z_004.inputs[0])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (189.0, -135.800048828125)
    compare_005.bl_label = "Compare"
    compare_005.operation = "EQUAL"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    # B
    compare_005.inputs[1].default_value = 0.8700000047683716
    # A
    compare_005.inputs[2].default_value = 0
    # B
    compare_005.inputs[3].default_value = 0
    # A
    compare_005.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_005.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_005.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_005.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_005.inputs[8].default_value = ""
    # B
    compare_005.inputs[9].default_value = ""
    # C
    compare_005.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_005.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_005.inputs[12].default_value = 0.09099999070167542
    # Links for compare_005
    links.new(separate_x_y_z_004.outputs[1], compare_005.inputs[0])
    links.new(compare_005.outputs[0], separate_geometry_004.inputs[1])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    transform_geometry_002.label = ""
    transform_geometry_002.location = (529.0, -95.800048828125)
    transform_geometry_002.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_002.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_002.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.0))
    # Rotation
    transform_geometry_002.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_002.inputs[4].default_value = Vector((1.0, -0.7799999713897705, 1.0))
    # Links for transform_geometry_002
    links.new(separate_geometry_004.outputs[0], transform_geometry_002.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (869.0, -35.800048828125)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(separate_geometry_004.outputs[0], join_geometry_004.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.name = "Flip Faces.001"
    flip_faces_001.label = ""
    flip_faces_001.location = (709.0, -95.800048828125)
    flip_faces_001.bl_label = "Flip Faces"
    # Selection
    flip_faces_001.inputs[1].default_value = True
    # Links for flip_faces_001
    links.new(flip_faces_001.outputs[0], join_geometry_004.inputs[0])
    links.new(transform_geometry_002.outputs[0], flip_faces_001.inputs[0])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    transform_geometry_003.label = ""
    transform_geometry_003.location = (1029.0, -115.800048828125)
    transform_geometry_003.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_003.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_003.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    # Links for transform_geometry_003
    links.new(join_geometry_004.outputs[0], transform_geometry_003.inputs[0])

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_008.name = "Join Geometry.008"
    join_geometry_008.label = ""
    join_geometry_008.location = (1369.0, -55.800048828125)
    join_geometry_008.bl_label = "Join Geometry"
    # Links for join_geometry_008
    links.new(join_geometry_004.outputs[0], join_geometry_008.inputs[0])

    flip_faces_002 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.name = "Flip Faces.002"
    flip_faces_002.label = ""
    flip_faces_002.location = (1209.0, -115.800048828125)
    flip_faces_002.bl_label = "Flip Faces"
    # Selection
    flip_faces_002.inputs[1].default_value = True
    # Links for flip_faces_002
    links.new(flip_faces_002.outputs[0], join_geometry_008.inputs[0])
    links.new(transform_geometry_003.outputs[0], flip_faces_002.inputs[0])

    mesh_to_points_001 = nodes.new("GeometryNodeMeshToPoints")
    mesh_to_points_001.name = "Mesh to Points.001"
    mesh_to_points_001.label = ""
    mesh_to_points_001.location = (1729.0, -55.800048828125)
    mesh_to_points_001.bl_label = "Mesh to Points"
    mesh_to_points_001.mode = "VERTICES"
    # Selection
    mesh_to_points_001.inputs[1].default_value = True
    # Position
    mesh_to_points_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Radius
    mesh_to_points_001.inputs[3].default_value = 0.05000000074505806
    # Links for mesh_to_points_001

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    points_to_curves.label = ""
    points_to_curves.location = (2109.0, -55.800048828125)
    points_to_curves.bl_label = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0
    # Links for points_to_curves
    links.new(mesh_to_points_001.outputs[0], points_to_curves.inputs[0])

    gradient_texture = nodes.new("ShaderNodeTexGradient")
    gradient_texture.name = "Gradient Texture"
    gradient_texture.label = ""
    gradient_texture.location = (1569.0, -235.800048828125)
    gradient_texture.bl_label = "Gradient Texture"
    gradient_texture.gradient_type = "RADIAL"
    # Vector
    gradient_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Links for gradient_texture

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.label = ""
    merge_by_distance.location = (1549.0, -55.800048828125)
    merge_by_distance.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance.inputs[1].default_value = True
    # Mode
    merge_by_distance.inputs[2].default_value = "All"
    # Distance
    merge_by_distance.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance
    links.new(merge_by_distance.outputs[0], mesh_to_points_001.inputs[0])
    links.new(join_geometry_008.outputs[0], merge_by_distance.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (2309.0, -55.800048828125)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Length"
    # Count
    resample_curve.inputs[3].default_value = 754
    # Length
    resample_curve.inputs[4].default_value = 0.0010000000474974513
    # Links for resample_curve
    links.new(points_to_curves.outputs[0], resample_curve.inputs[0])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    transform_geometry_004.label = ""
    transform_geometry_004.location = (2629.0, -35.800048828125)
    transform_geometry_004.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_004.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_004.inputs[3].default_value = Euler((0.01483529806137085, 0.03560471534729004, 0.0), 'XYZ')
    # Scale
    transform_geometry_004.inputs[4].default_value = Vector((1.059999942779541, 1.0199999809265137, 1.0))
    # Links for transform_geometry_004
    links.new(resample_curve.outputs[0], transform_geometry_004.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.label = ""
    transform_geometry_005.location = (2809.0, -375.800048828125)
    transform_geometry_005.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_005.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_005.inputs[3].default_value = Euler((-0.01151917316019535, -0.06230825185775757, 0.0), 'XYZ')
    # Scale
    transform_geometry_005.inputs[4].default_value = Vector((1.059999942779541, 1.0199999809265137, 1.0))
    # Links for transform_geometry_005

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (3029.0, -35.800048828125)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(transform_geometry_004.outputs[0], join_geometry.inputs[0])
    links.new(transform_geometry_005.outputs[0], join_geometry.inputs[0])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (5558.0, -355.800048828125)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (4678.0, -635.800048828125)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Resolution
    curve_circle.inputs[0].default_value = 3
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle.inputs[4].default_value = 0.0020000000949949026
    # Links for curve_circle

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (2629.0, -375.800048828125)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Position
    set_position_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_001
    links.new(set_position_001.outputs[0], transform_geometry_005.inputs[0])
    links.new(resample_curve.outputs[0], set_position_001.inputs[0])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.label = ""
    spline_parameter.location = (1989.0, -755.800048828125)
    spline_parameter.bl_label = "Spline Parameter"
    # Links for spline_parameter

    float_curve_001 = nodes.new("ShaderNodeFloatCurve")
    float_curve_001.name = "Float Curve.001"
    float_curve_001.label = ""
    float_curve_001.location = (1989.0, -435.800048828125)
    float_curve_001.bl_label = "Float Curve"
    # Factor
    float_curve_001.inputs[0].default_value = 1.0
    # Links for float_curve_001
    links.new(spline_parameter.outputs[0], float_curve_001.inputs[1])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (2249.0, -435.800048828125)
    combine_x_y_z.bl_label = "Combine XYZ"
    # X
    combine_x_y_z.inputs[0].default_value = 0.0
    # Z
    combine_x_y_z.inputs[2].default_value = 0.0
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], set_position_001.inputs[3])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (2249.0, -515.800048828125)
    math_001.bl_label = "Math"
    math_001.operation = "MULTIPLY"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = -0.009999999776482582
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(float_curve_001.outputs[0], math_001.inputs[0])
    links.new(math_001.outputs[0], combine_x_y_z.inputs[1])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (6938.0, -515.800048828125)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_003.inputs[3].default_value = True
    # Links for store_named_attribute_003

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.name = "Curve Circle.001"
    curve_circle_001.label = ""
    curve_circle_001.location = (29.0, -35.800048828125)
    curve_circle_001.bl_label = "Curve Circle"
    curve_circle_001.mode = "RADIUS"
    # Resolution
    curve_circle_001.inputs[0].default_value = 32
    # Point 1
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_001.inputs[4].default_value = 0.009999999776482582
    # Links for curve_circle_001

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (4378.0, -315.800048828125)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(join_geometry.outputs[0], join_geometry_001.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_009.name = "Join Geometry.009"
    join_geometry_009.label = ""
    join_geometry_009.location = (209.0, -55.800048828125)
    join_geometry_009.bl_label = "Join Geometry"
    # Links for join_geometry_009
    links.new(curve_circle_001.outputs[0], join_geometry_009.inputs[0])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.name = "Transform Geometry.006"
    transform_geometry_006.label = ""
    transform_geometry_006.location = (389.0, -35.800048828125)
    transform_geometry_006.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_006.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_006.inputs[2].default_value = Vector((0.0, -0.1550000011920929, 0.054999999701976776))
    # Rotation
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')
    # Scale
    transform_geometry_006.inputs[4].default_value = Vector((1.0, 0.800000011920929, 1.0))
    # Links for transform_geometry_006
    links.new(join_geometry_009.outputs[0], transform_geometry_006.inputs[0])

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.name = "Transform Geometry.007"
    transform_geometry_007.label = ""
    transform_geometry_007.location = (29.0, -175.800048828125)
    transform_geometry_007.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_007.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_007.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    # Rotation
    transform_geometry_007.inputs[3].default_value = Euler((0.4747295081615448, 0.7522368431091309, 0.8482299447059631), 'XYZ')
    # Scale
    transform_geometry_007.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_007
    links.new(curve_circle_001.outputs[0], transform_geometry_007.inputs[0])
    links.new(transform_geometry_007.outputs[0], join_geometry_009.inputs[0])

    frame_008 = nodes.new("NodeFrame")
    frame_008.name = "Frame.008"
    frame_008.label = "Knot"
    frame_008.location = (3329.0, -440.0)
    frame_008.bl_label = "Frame"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20
    # Links for frame_008

    frame_009 = nodes.new("NodeFrame")
    frame_009.name = "Frame.009"
    frame_009.label = "Waist Loops"
    frame_009.location = (29.0, -260.0)
    frame_009.bl_label = "Frame"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20
    # Links for frame_009

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (1749.0, -235.800048828125)
    math_002.bl_label = "Math"
    math_002.operation = "ADD"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 0.5
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(gradient_texture.outputs[1], math_002.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (1909.0, -235.800048828125)
    math_003.bl_label = "Math"
    math_003.operation = "FRACT"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 0.5
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_003.outputs[0], points_to_curves.inputs[2])
    links.new(math_002.outputs[0], math_003.inputs[0])

    bézier_segment_002 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_002.name = "Bézier Segment.002"
    bézier_segment_002.label = ""
    bézier_segment_002.location = (3958.0, -635.800048828125)
    bézier_segment_002.bl_label = "Bézier Segment"
    bézier_segment_002.mode = "OFFSET"
    # Resolution
    bézier_segment_002.inputs[0].default_value = 16
    # Start
    bézier_segment_002.inputs[1].default_value = Vector((0.0, -0.15800000727176666, 0.054999999701976776))
    # Start Handle
    bézier_segment_002.inputs[2].default_value = Vector((0.04999999701976776, 0.0, 0.0))
    # End Handle
    bézier_segment_002.inputs[3].default_value = Vector((-0.03999999910593033, 0.0, 0.05999999865889549))
    # End
    bézier_segment_002.inputs[4].default_value = Vector((0.03999999910593033, -0.18800000846385956, -0.06499999761581421))
    # Links for bézier_segment_002
    links.new(bézier_segment_002.outputs[0], join_geometry_001.inputs[0])

    bézier_segment_003 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_003.name = "Bézier Segment.003"
    bézier_segment_003.label = ""
    bézier_segment_003.location = (4118.0, -695.800048828125)
    bézier_segment_003.bl_label = "Bézier Segment"
    bézier_segment_003.mode = "OFFSET"
    # Resolution
    bézier_segment_003.inputs[0].default_value = 16
    # Start
    bézier_segment_003.inputs[1].default_value = Vector((0.0, -0.15800000727176666, 0.054999999701976776))
    # Start Handle
    bézier_segment_003.inputs[2].default_value = Vector((0.019999997690320015, -0.009999999776482582, 0.0))
    # End Handle
    bézier_segment_003.inputs[3].default_value = Vector((-0.009999999776482582, -0.009999999776482582, 0.05999999865889549))
    # End
    bézier_segment_003.inputs[4].default_value = Vector((0.009999999776482582, -0.18800000846385956, -0.06499999761581421))
    # Links for bézier_segment_003
    links.new(bézier_segment_003.outputs[0], join_geometry_001.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    set_curve_tilt.label = ""
    set_curve_tilt.location = (4738.0, -315.800048828125)
    set_curve_tilt.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Links for set_curve_tilt

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.label = ""
    spline_parameter_001.location = (4578.0, -435.800048828125)
    spline_parameter_001.bl_label = "Spline Parameter"
    # Links for spline_parameter_001

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (4738.0, -435.800048828125)
    math_004.bl_label = "Math"
    math_004.operation = "MULTIPLY"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 106.49999237060547
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(spline_parameter_001.outputs[1], math_004.inputs[0])
    links.new(math_004.outputs[0], set_curve_tilt.inputs[2])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.label = ""
    instance_on_points_001.location = (4878.0, -675.800048828125)
    instance_on_points_001.bl_label = "Instance on Points"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Rotation
    instance_on_points_001.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_001.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_001
    links.new(curve_circle.outputs[0], instance_on_points_001.inputs[0])

    curve_circle_002 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_002.name = "Curve Circle.002"
    curve_circle_002.label = ""
    curve_circle_002.location = (4678.0, -755.800048828125)
    curve_circle_002.bl_label = "Curve Circle"
    curve_circle_002.mode = "RADIUS"
    # Resolution
    curve_circle_002.inputs[0].default_value = 8
    # Point 1
    curve_circle_002.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_002.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_002.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_002.inputs[4].default_value = 0.003000000026077032
    # Links for curve_circle_002
    links.new(curve_circle_002.outputs[0], instance_on_points_001.inputs[2])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.label = ""
    realize_instances_001.location = (5038.0, -675.800048828125)
    realize_instances_001.bl_label = "Realize Instances"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0
    # Links for realize_instances_001
    links.new(instance_on_points_001.outputs[0], realize_instances_001.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (4578.0, -315.800048828125)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Length"
    # Count
    resample_curve_001.inputs[3].default_value = 754
    # Length
    resample_curve_001.inputs[4].default_value = 0.0010000000474974513
    # Links for resample_curve_001
    links.new(resample_curve_001.outputs[0], set_curve_tilt.inputs[0])
    links.new(join_geometry_001.outputs[0], resample_curve_001.inputs[0])

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (7098.0, -515.800048828125)
    store_named_attribute_004.bl_label = "Store Named Attribute"
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "rope"
    # Value
    store_named_attribute_004.inputs[3].default_value = True
    # Links for store_named_attribute_004
    links.new(store_named_attribute_003.outputs[0], store_named_attribute_004.inputs[0])

    capture_attribute_003 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.name = "Capture Attribute.003"
    capture_attribute_003.label = ""
    capture_attribute_003.location = (5358.0, -515.800048828125)
    capture_attribute_003.bl_label = "Capture Attribute"
    capture_attribute_003.active_index = 0
    capture_attribute_003.domain = "POINT"
    # Links for capture_attribute_003
    links.new(capture_attribute_003.outputs[0], curve_to_mesh.inputs[1])
    links.new(realize_instances_001.outputs[0], capture_attribute_003.inputs[0])

    capture_attribute_004 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_004.name = "Capture Attribute.004"
    capture_attribute_004.label = ""
    capture_attribute_004.location = (5358.0, -375.800048828125)
    capture_attribute_004.bl_label = "Capture Attribute"
    capture_attribute_004.active_index = 0
    capture_attribute_004.domain = "POINT"
    # Links for capture_attribute_004
    links.new(capture_attribute_004.outputs[0], curve_to_mesh.inputs[0])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"
    spline_parameter_002.label = ""
    spline_parameter_002.location = (5358.0, -655.800048828125)
    spline_parameter_002.bl_label = "Spline Parameter"
    # Links for spline_parameter_002
    links.new(spline_parameter_002.outputs[1], capture_attribute_004.inputs[1])
    links.new(spline_parameter_002.outputs[1], capture_attribute_003.inputs[1])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (5558.0, -515.800048828125)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # Z
    combine_x_y_z_001.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_001
    links.new(capture_attribute_004.outputs[1], combine_x_y_z_001.inputs[0])
    links.new(capture_attribute_003.outputs[1], combine_x_y_z_001.inputs[1])

    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.name = "Store Named Attribute.005"
    store_named_attribute_005.label = ""
    store_named_attribute_005.location = (7258.0, -515.800048828125)
    store_named_attribute_005.bl_label = "Store Named Attribute"
    store_named_attribute_005.data_type = "FLOAT2"
    store_named_attribute_005.domain = "CORNER"
    # Selection
    store_named_attribute_005.inputs[1].default_value = True
    # Name
    store_named_attribute_005.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute_005
    links.new(store_named_attribute_004.outputs[0], store_named_attribute_005.inputs[0])
    links.new(combine_x_y_z_001.outputs[0], store_named_attribute_005.inputs[3])
    links.new(store_named_attribute_005.outputs[0], switch.inputs[2])

    frame_010 = nodes.new("NodeFrame")
    frame_010.name = "Frame.010"
    frame_010.label = "ROPE"
    frame_010.location = (762.0, 2875.800048828125)
    frame_010.bl_label = "Frame"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20
    # Links for frame_010

    instance_on_points_002 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.name = "Instance on Points.002"
    instance_on_points_002.label = ""
    instance_on_points_002.location = (5418.0, -995.800048828125)
    instance_on_points_002.bl_label = "Instance on Points"
    # Selection
    instance_on_points_002.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_002.inputs[3].default_value = False
    # Instance Index
    instance_on_points_002.inputs[4].default_value = 0
    # Scale
    instance_on_points_002.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_002

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.label = ""
    curve_line.location = (5238.0, -1055.800048828125)
    curve_line.bl_label = "Curve Line"
    curve_line.mode = "POINTS"
    # Start
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, 0.0))
    # End
    curve_line.inputs[1].default_value = Vector((0.0, 0.0, 0.05000000074505806))
    # Direction
    curve_line.inputs[2].default_value = [0.0, 0.0, 1.0]
    # Length
    curve_line.inputs[3].default_value = 1.0
    # Links for curve_line
    links.new(curve_line.outputs[0], instance_on_points_002.inputs[2])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.label = ""
    align_rotation_to_vector_001.location = (5418.0, -1275.800048828125)
    align_rotation_to_vector_001.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_001.axis = "Z"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_001.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_001
    links.new(align_rotation_to_vector_001.outputs[0], instance_on_points_002.inputs[5])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (5238.0, -1315.800048828125)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_001.inputs[2])

    realize_instances_002 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.name = "Realize Instances.002"
    realize_instances_002.label = ""
    realize_instances_002.location = (5598.0, -995.800048828125)
    realize_instances_002.bl_label = "Realize Instances"
    # Selection
    realize_instances_002.inputs[1].default_value = True
    # Realize All
    realize_instances_002.inputs[2].default_value = True
    # Depth
    realize_instances_002.inputs[3].default_value = 0
    # Links for realize_instances_002
    links.new(instance_on_points_002.outputs[0], realize_instances_002.inputs[0])

    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.name = "Resample Curve.002"
    resample_curve_002.label = ""
    resample_curve_002.location = (5758.0, -995.800048828125)
    resample_curve_002.bl_label = "Resample Curve"
    resample_curve_002.keep_last_segment = True
    # Selection
    resample_curve_002.inputs[1].default_value = True
    # Mode
    resample_curve_002.inputs[2].default_value = "Count"
    # Count
    resample_curve_002.inputs[3].default_value = 7
    # Length
    resample_curve_002.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_002
    links.new(realize_instances_002.outputs[0], resample_curve_002.inputs[0])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (5978.0, -1015.800048828125)
    set_position_002.bl_label = "Set Position"
    # Links for set_position_002
    links.new(resample_curve_002.outputs[0], set_position_002.inputs[0])

    endpoint_selection = nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection.name = "Endpoint Selection"
    endpoint_selection.label = ""
    endpoint_selection.location = (5598.0, -1115.800048828125)
    endpoint_selection.bl_label = "Endpoint Selection"
    # Start Size
    endpoint_selection.inputs[0].default_value = 1
    # End Size
    endpoint_selection.inputs[1].default_value = 0
    # Links for endpoint_selection

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.label = ""
    boolean_math_003.location = (5758.0, -1115.800048828125)
    boolean_math_003.bl_label = "Boolean Math"
    boolean_math_003.operation = "NOT"
    # Boolean
    boolean_math_003.inputs[1].default_value = False
    # Links for boolean_math_003
    links.new(boolean_math_003.outputs[0], set_position_002.inputs[1])
    links.new(endpoint_selection.outputs[0], boolean_math_003.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (5758.0, -1235.800048828125)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 0.006000000052154064
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], set_position_002.inputs[3])

    random_value_002 = nodes.new("FunctionNodeRandomValue")
    random_value_002.name = "Random Value.002"
    random_value_002.label = ""
    random_value_002.location = (5598.0, -1235.800048828125)
    random_value_002.bl_label = "Random Value"
    random_value_002.data_type = "FLOAT_VECTOR"
    # Min
    random_value_002.inputs[0].default_value = [-1.0, -1.0, -1.0]
    # Max
    random_value_002.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_002.inputs[2].default_value = 0.0
    # Max
    random_value_002.inputs[3].default_value = 1.0
    # Min
    random_value_002.inputs[4].default_value = 0
    # Max
    random_value_002.inputs[5].default_value = 100
    # Probability
    random_value_002.inputs[6].default_value = 0.5
    # ID
    random_value_002.inputs[7].default_value = 0
    # Seed
    random_value_002.inputs[8].default_value = 2
    # Links for random_value_002
    links.new(random_value_002.outputs[0], vector_math_002.inputs[0])

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.label = ""
    set_spline_type.location = (6138.0, -1015.800048828125)
    set_spline_type.bl_label = "Set Spline Type"
    set_spline_type.spline_type = "NURBS"
    # Selection
    set_spline_type.inputs[1].default_value = True
    # Links for set_spline_type
    links.new(set_position_002.outputs[0], set_spline_type.inputs[0])

    resample_curve_003 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.name = "Resample Curve.003"
    resample_curve_003.label = ""
    resample_curve_003.location = (6298.0, -1015.800048828125)
    resample_curve_003.bl_label = "Resample Curve"
    resample_curve_003.keep_last_segment = True
    # Selection
    resample_curve_003.inputs[1].default_value = True
    # Mode
    resample_curve_003.inputs[2].default_value = "Count"
    # Count
    resample_curve_003.inputs[3].default_value = 15
    # Length
    resample_curve_003.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_003
    links.new(set_spline_type.outputs[0], resample_curve_003.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (6458.0, -1015.800048828125)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_001.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = True
    # Links for curve_to_mesh_001
    links.new(resample_curve_003.outputs[0], curve_to_mesh_001.inputs[0])

    curve_circle_003 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.name = "Curve Circle.003"
    curve_circle_003.label = ""
    curve_circle_003.location = (6298.0, -1135.800048828125)
    curve_circle_003.bl_label = "Curve Circle"
    curve_circle_003.mode = "RADIUS"
    # Resolution
    curve_circle_003.inputs[0].default_value = 32
    # Point 1
    curve_circle_003.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_003.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_003.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_003.inputs[4].default_value = 9.999999747378752e-05
    # Links for curve_circle_003
    links.new(curve_circle_003.outputs[0], curve_to_mesh_001.inputs[1])

    join_geometry_011 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_011.name = "Join Geometry.011"
    join_geometry_011.label = ""
    join_geometry_011.location = (6698.0, -495.800048828125)
    join_geometry_011.bl_label = "Join Geometry"
    # Links for join_geometry_011
    links.new(curve_to_mesh_001.outputs[0], join_geometry_011.inputs[0])
    links.new(curve_to_mesh.outputs[0], join_geometry_011.inputs[0])
    links.new(join_geometry_011.outputs[0], store_named_attribute_003.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (5858.0, -675.800048828125)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "FACES"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity
    links.new(curve_to_mesh.outputs[0], geometry_proximity.inputs[0])
    links.new(geometry_proximity.outputs[0], set_position_002.inputs[2])

    join_geometry_012 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_012.name = "Join Geometry.012"
    join_geometry_012.label = ""
    join_geometry_012.location = (5078.0, -355.800048828125)
    join_geometry_012.bl_label = "Join Geometry"
    # Links for join_geometry_012
    links.new(join_geometry_012.outputs[0], capture_attribute_004.inputs[0])
    links.new(set_curve_tilt.outputs[0], join_geometry_012.inputs[0])

    set_curve_tilt_001 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_001.name = "Set Curve Tilt.001"
    set_curve_tilt_001.label = ""
    set_curve_tilt_001.location = (4738.0, -35.800048828125)
    set_curve_tilt_001.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_001.inputs[1].default_value = True
    # Links for set_curve_tilt_001
    links.new(set_curve_tilt_001.outputs[0], join_geometry_012.inputs[0])

    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_003.name = "Spline Parameter.003"
    spline_parameter_003.label = ""
    spline_parameter_003.location = (4578.0, -155.800048828125)
    spline_parameter_003.bl_label = "Spline Parameter"
    # Links for spline_parameter_003

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (4738.0, -155.800048828125)
    math_005.bl_label = "Math"
    math_005.operation = "MULTIPLY"
    math_005.use_clamp = False
    # Value
    math_005.inputs[1].default_value = 199.0999755859375
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(spline_parameter_003.outputs[1], math_005.inputs[0])
    links.new(math_005.outputs[0], set_curve_tilt_001.inputs[2])

    resample_curve_004 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_004.name = "Resample Curve.004"
    resample_curve_004.label = ""
    resample_curve_004.location = (4578.0, -35.800048828125)
    resample_curve_004.bl_label = "Resample Curve"
    resample_curve_004.keep_last_segment = True
    # Selection
    resample_curve_004.inputs[1].default_value = True
    # Mode
    resample_curve_004.inputs[2].default_value = "Length"
    # Count
    resample_curve_004.inputs[3].default_value = 754
    # Length
    resample_curve_004.inputs[4].default_value = 0.0010000000474974513
    # Links for resample_curve_004
    links.new(resample_curve_004.outputs[0], set_curve_tilt_001.inputs[0])
    links.new(transform_geometry_006.outputs[0], resample_curve_004.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.name = "Group.002"
    swap_attr.label = ""
    swap_attr.location = (1349.0, -289.0)
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.bl_label = "Group"
    # Old
    swap_attr.inputs[2].default_value = "ruby"
    # New
    swap_attr.inputs[3].default_value = "saphire"
    # Links for swap_attr
    links.new(swap_attr.outputs[0], join_geometry_006.inputs[0])
    links.new(realize_instances.outputs[0], swap_attr.inputs[0])
    links.new(capture_attribute_002.outputs[1], swap_attr.inputs[1])

    gem_in_holder_1 = nodes.new("GeometryNodeGroup")
    gem_in_holder_1.name = "Gem in Holder.001"
    gem_in_holder_1.label = ""
    gem_in_holder_1.location = (569.0, -75.13334655761719)
    gem_in_holder_1.node_tree = create_gem_in__holder_group()
    gem_in_holder_1.bl_label = "Group"
    # Gem Radius
    gem_in_holder_1.inputs[0].default_value = 0.009999990463256836
    # Gem Material
    gem_in_holder_1.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_1.inputs[2].default_value = False
    # Scale
    gem_in_holder_1.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_1.inputs[4].default_value = 20
    # Seed
    gem_in_holder_1.inputs[5].default_value = 10
    # Wings
    gem_in_holder_1.inputs[6].default_value = False
    # Array Count
    gem_in_holder_1.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_1.inputs[8].default_value = 10
    # Links for gem_in_holder_1

    position_004 = nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"
    position_004.label = ""
    position_004.location = (29.0, -255.1333465576172)
    position_004.bl_label = "Position"
    # Links for position_004

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.name = "For Each Geometry Element Input.001"
    for_each_geometry_element_input_001.label = ""
    for_each_geometry_element_input_001.location = (189.0, -55.13334655761719)
    for_each_geometry_element_input_001.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input_001.inputs[1].default_value = True
    # Rotation
    for_each_geometry_element_input_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for for_each_geometry_element_input_001
    links.new(position_004.outputs[0], for_each_geometry_element_input_001.inputs[2])

    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.name = "For Each Geometry Element Output.001"
    for_each_geometry_element_output_001.label = ""
    for_each_geometry_element_output_001.location = (1529.0, -75.13334655761719)
    for_each_geometry_element_output_001.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    # Links for for_each_geometry_element_output_001
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_006.inputs[0])

    transform_geometry_008 = nodes.new("GeometryNodeTransform")
    transform_geometry_008.name = "Transform Geometry.008"
    transform_geometry_008.label = ""
    transform_geometry_008.location = (829.0, -75.13334655761719)
    transform_geometry_008.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_008.inputs[1].default_value = "Components"
    # Scale
    transform_geometry_008.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_008
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_008.inputs[2])
    links.new(gem_in_holder_1.outputs[4], transform_geometry_008.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.name = "Rotate Rotation.002"
    rotate_rotation_002.label = ""
    rotate_rotation_002.location = (229.0, -315.13336181640625)
    rotate_rotation_002.bl_label = "Rotate Rotation"
    rotate_rotation_002.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, -1.5707963705062866, 0.0), 'XYZ')
    # Links for rotate_rotation_002
    links.new(rotate_rotation_002.outputs[0], transform_geometry_008.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[3], rotate_rotation_002.inputs[0])

    frame_011 = nodes.new("NodeFrame")
    frame_011.name = "Frame.011"
    frame_011.label = "Random Wings"
    frame_011.location = (729.0, -1029.6666259765625)
    frame_011.bl_label = "Frame"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20
    # Links for frame_011

    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.name = "Random Value.007"
    random_value_007.label = ""
    random_value_007.location = (389.0, -75.13334655761719)
    random_value_007.bl_label = "Random Value"
    random_value_007.data_type = "FLOAT"
    # Min
    random_value_007.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_007.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_007.inputs[2].default_value = 6.0
    # Max
    random_value_007.inputs[3].default_value = 7.0
    # Min
    random_value_007.inputs[4].default_value = 0
    # Max
    random_value_007.inputs[5].default_value = 100
    # Probability
    random_value_007.inputs[6].default_value = 0.5
    # Seed
    random_value_007.inputs[8].default_value = 32
    # Links for random_value_007
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_1.inputs[10])

    random_value_008 = nodes.new("FunctionNodeRandomValue")
    random_value_008.name = "Random Value.008"
    random_value_008.label = ""
    random_value_008.location = (389.0, -255.1333465576172)
    random_value_008.bl_label = "Random Value"
    random_value_008.data_type = "FLOAT"
    # Min
    random_value_008.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_008.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_008.inputs[2].default_value = 0.0
    # Max
    random_value_008.inputs[3].default_value = 0.003000000026077032
    # Min
    random_value_008.inputs[4].default_value = 0
    # Max
    random_value_008.inputs[5].default_value = 100
    # Probability
    random_value_008.inputs[6].default_value = 0.5
    # Seed
    random_value_008.inputs[8].default_value = 10
    # Links for random_value_008
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_008.inputs[7])
    links.new(random_value_008.outputs[1], gem_in_holder_1.inputs[9])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    set_position_003.label = ""
    set_position_003.location = (1009.0, -75.13334655761719)
    set_position_003.bl_label = "Set Position"
    # Selection
    set_position_003.inputs[1].default_value = True
    # Offset
    set_position_003.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_003
    links.new(transform_geometry_008.outputs[0], set_position_003.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (1398.0, -1624.7999267578125)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Links for reroute_002

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.label = ""
    geometry_proximity_001.location = (829.0, -295.13336181640625)
    geometry_proximity_001.bl_label = "Geometry Proximity"
    geometry_proximity_001.target_element = "FACES"
    # Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0
    # Links for geometry_proximity_001
    links.new(reroute_002.outputs[0], geometry_proximity_001.inputs[0])
    links.new(geometry_proximity_001.outputs[0], set_position_003.inputs[2])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (1169.0, -75.13334655761719)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002
    links.new(set_position_003.outputs[0], curve_to_mesh_002.inputs[0])
    links.new(gem_in_holder_1.outputs[1], curve_to_mesh_002.inputs[1])
    links.new(gem_in_holder_1.outputs[2], curve_to_mesh_002.inputs[2])

    store_named_attribute_006 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_006.name = "Store Named Attribute.006"
    store_named_attribute_006.label = ""
    store_named_attribute_006.location = (1349.0, -75.13334655761719)
    store_named_attribute_006.bl_label = "Store Named Attribute"
    store_named_attribute_006.data_type = "BOOLEAN"
    store_named_attribute_006.domain = "POINT"
    # Selection
    store_named_attribute_006.inputs[1].default_value = True
    # Name
    store_named_attribute_006.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_006.inputs[3].default_value = True
    # Links for store_named_attribute_006
    links.new(store_named_attribute_006.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(curve_to_mesh_002.outputs[0], store_named_attribute_006.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (578.9881591796875, -1496.593994140625)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(reroute.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(separate_geometry_001.outputs[1], reroute.inputs[0])
    links.new(reroute.outputs[0], reroute_002.inputs[0])

    frame_012 = nodes.new("NodeFrame")
    frame_012.name = "Frame.012"
    frame_012.label = ""
    frame_012.location = (29.0, -35.7999267578125)
    frame_012.bl_label = "Frame"
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20
    # Links for frame_012

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (8595.9638671875, 854.44287109375)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001
    links.new(join_geometry_006.outputs[0], reroute_001.inputs[0])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (9180.0, 660.0)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Links for switch_001
    links.new(reroute_001.outputs[0], switch_001.inputs[2])
    links.new(switch_001.outputs[0], join_geometry_007.inputs[0])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (9180.0, 720.0)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[0], switch_001.inputs[0])

    resample_curve_005 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_005.name = "Resample Curve.005"
    resample_curve_005.label = ""
    resample_curve_005.location = (5238.0, -915.800048828125)
    resample_curve_005.bl_label = "Resample Curve"
    resample_curve_005.keep_last_segment = True
    # Selection
    resample_curve_005.inputs[1].default_value = True
    # Mode
    resample_curve_005.inputs[2].default_value = "Length"
    # Count
    resample_curve_005.inputs[3].default_value = 10
    # Length
    resample_curve_005.inputs[4].default_value = 0.004999999888241291
    # Links for resample_curve_005
    links.new(resample_curve_005.outputs[0], instance_on_points_002.inputs[0])
    links.new(set_curve_tilt.outputs[0], resample_curve_005.inputs[0])

    auto_layout_nodes(group)
    return group
