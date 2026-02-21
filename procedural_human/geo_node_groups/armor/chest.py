import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group
from procedural_human.geo_node_groups.utilities.join_splines import create_join__splines_group
from procedural_human.geo_node_groups.utilities.gold_decorations import create_gold_decorations_group


@geo_node_group
def create_chest_group():
    group_name = "Chest"
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
    group_output.location = (8900.0, -160.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    bi_rail_loft = nodes.new("GeometryNodeGroup")
    bi_rail_loft.name = "Bi-Rail Loft"
    bi_rail_loft.label = ""
    bi_rail_loft.location = (-1860.0, -400.0)
    bi_rail_loft.node_tree = create_bi_rail_loft_group()
    bi_rail_loft.bl_label = "Group"
    # Smoothing
    bi_rail_loft.inputs[3].default_value = 6
    # Menu
    bi_rail_loft.inputs[4].default_value = "Resolution"
    # X Spacing
    bi_rail_loft.inputs[5].default_value = 0.009999999776482582
    # Y Spacing
    bi_rail_loft.inputs[6].default_value = 0.029999999329447746
    # X Resolution
    bi_rail_loft.inputs[7].default_value = 14
    # Y Resolution
    bi_rail_loft.inputs[8].default_value = 102
    # Links for bi_rail_loft

    bézier_segment = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment.name = "Bézier Segment"
    bézier_segment.label = ""
    bézier_segment.location = (29.0, -35.800018310546875)
    bézier_segment.bl_label = "Bézier Segment"
    bézier_segment.mode = "POSITION"
    # Resolution
    bézier_segment.inputs[0].default_value = 200
    # Start
    bézier_segment.inputs[1].default_value = Vector((0.0, -0.14000000059604645, 0.07000000029802322))
    # Start Handle
    bézier_segment.inputs[2].default_value = Vector((0.0, -0.20000000298023224, 0.2800000011920929))
    # End Handle
    bézier_segment.inputs[3].default_value = Vector((0.0, -0.1600000113248825, 0.3100000023841858))
    # End
    bézier_segment.inputs[4].default_value = Vector((0.0, -0.08999998867511749, 0.4099999964237213))
    # Links for bézier_segment

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Centre Line"
    frame.location = (29.0, -35.800018310546875)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    bézier_segment_001 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_001.name = "Bézier Segment.001"
    bézier_segment_001.label = ""
    bézier_segment_001.location = (29.0, -35.79999542236328)
    bézier_segment_001.bl_label = "Bézier Segment"
    bézier_segment_001.mode = "OFFSET"
    # Resolution
    bézier_segment_001.inputs[0].default_value = 200
    # Start
    bézier_segment_001.inputs[1].default_value = Vector((-0.14999999105930328, 0.0, 0.07000000029802322))
    # Start Handle
    bézier_segment_001.inputs[2].default_value = Vector((-0.019999999552965164, 0.0, 0.05999999865889549))
    # End Handle
    bézier_segment_001.inputs[3].default_value = Vector((0.0, 0.0, -0.029999999329447746))
    # End
    bézier_segment_001.inputs[4].default_value = Vector((-0.17000000178813934, 0.0, 0.1899999976158142))
    # Links for bézier_segment_001

    bézier_segment_002 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_002.name = "Bézier Segment.002"
    bézier_segment_002.label = ""
    bézier_segment_002.location = (209.0, -95.79999542236328)
    bézier_segment_002.bl_label = "Bézier Segment"
    bézier_segment_002.mode = "OFFSET"
    # Resolution
    bézier_segment_002.inputs[0].default_value = 200
    # Start
    bézier_segment_002.inputs[1].default_value = Vector((-0.17000000178813934, 0.0, 0.1899999976158142))
    # Start Handle
    bézier_segment_002.inputs[2].default_value = Vector((0.05000000074505806, -0.20999999344348907, 0.030000001192092896))
    # End Handle
    bézier_segment_002.inputs[3].default_value = Vector((0.019999999552965164, -0.029999999329447746, -0.029999999329447746))
    # End
    bézier_segment_002.inputs[4].default_value = Vector((-0.11999998986721039, -0.06000000238418579, 0.4000000059604645))
    # Links for bézier_segment_002

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (589.0, -75.79999542236328)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(bézier_segment_002.outputs[0], join_geometry.inputs[0])
    links.new(bézier_segment_001.outputs[0], join_geometry.inputs[0])

    join_splines = nodes.new("GeometryNodeGroup")
    join_splines.name = "Group"
    join_splines.label = ""
    join_splines.location = (769.0, -55.79999542236328)
    join_splines.node_tree = create_join__splines_group()
    join_splines.bl_label = "Group"
    # Links for join_splines
    links.new(join_splines.outputs[0], bi_rail_loft.inputs[1])
    links.new(join_geometry.outputs[0], join_splines.inputs[0])

    join_splines_1 = nodes.new("GeometryNodeGroup")
    join_splines_1.name = "Group.001"
    join_splines_1.label = ""
    join_splines_1.location = (618.0, -131.60003662109375)
    join_splines_1.node_tree = create_join__splines_group()
    join_splines_1.bl_label = "Group"
    # Links for join_splines_1
    links.new(bézier_segment.outputs[0], join_splines_1.inputs[0])
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
    frame_002.location = (180.0, -35.79998779296875)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Rails"
    frame_003.location = (-3398.0, 567.4000244140625)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    quadratic_bézier = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier.name = "Quadratic Bézier"
    quadratic_bézier.label = ""
    quadratic_bézier.location = (29.0, -55.79998779296875)
    quadratic_bézier.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier.inputs[0].default_value = 40
    # Start
    quadratic_bézier.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier.inputs[2].default_value = Vector((0.0, -0.75, -0.12999999523162842))
    # End
    quadratic_bézier.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier

    quadratic_bézier_001 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_001.name = "Quadratic Bézier.001"
    quadratic_bézier_001.label = ""
    quadratic_bézier_001.location = (709.0, -235.79998779296875)
    quadratic_bézier_001.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_001.inputs[0].default_value = 40
    # Start
    quadratic_bézier_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier_001.inputs[2].default_value = Vector((0.0, -0.1599999964237213, 0.1899999976158142))
    # End
    quadratic_bézier_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier_001

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (889.0, -35.79998779296875)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002
    links.new(join_geometry_002.outputs[0], bi_rail_loft.inputs[2])
    links.new(quadratic_bézier_001.outputs[0], join_geometry_002.inputs[0])
    links.new(quadratic_bézier.outputs[0], join_geometry_002.inputs[0])

    bézier_segment_003 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_003.name = "Bézier Segment.003"
    bézier_segment_003.label = ""
    bézier_segment_003.location = (369.0, -155.79998779296875)
    bézier_segment_003.bl_label = "Bézier Segment"
    bézier_segment_003.mode = "OFFSET"
    # Resolution
    bézier_segment_003.inputs[0].default_value = 200
    # Start
    bézier_segment_003.inputs[1].default_value = Vector((-0.11999999731779099, -0.05999999865889549, 0.4000000059604645))
    # Start Handle
    bézier_segment_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # End Handle
    bézier_segment_003.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # End
    bézier_segment_003.inputs[4].default_value = Vector((-0.09000000357627869, -0.05999999865889549, 0.41999998688697815))
    # Links for bézier_segment_003
    links.new(bézier_segment_003.outputs[0], join_geometry.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Profiles"
    frame_004.location = (-3369.0, -804.2000122070312)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    closure_input = nodes.new("NodeClosureInput")
    closure_input.name = "Closure Input"
    closure_input.label = ""
    closure_input.location = (-2220.0, -860.0)
    closure_input.bl_label = "Closure Input"
    # Links for closure_input

    closure_output = nodes.new("NodeClosureOutput")
    closure_output.name = "Closure Output"
    closure_output.label = ""
    closure_output.location = (-1760.0, -860.0)
    closure_output.bl_label = "Closure Output"
    closure_output.active_input_index = 0
    closure_output.active_output_index = 0
    closure_output.define_signature = False
    # Links for closure_output
    links.new(closure_output.outputs[0], bi_rail_loft.inputs[9])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (-2040.0, -860.0)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(float_curve.outputs[0], closure_output.inputs[0])
    links.new(closure_input.outputs[0], float_curve.inputs[1])

    quadratic_bézier_005 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_005.name = "Quadratic Bézier.005"
    quadratic_bézier_005.label = ""
    quadratic_bézier_005.location = (549.0, -195.79998779296875)
    quadratic_bézier_005.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_005.inputs[0].default_value = 40
    # Start
    quadratic_bézier_005.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Middle
    quadratic_bézier_005.inputs[2].default_value = Vector((0.26999998092651367, -0.41999995708465576, 0.0))
    # End
    quadratic_bézier_005.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Links for quadratic_bézier_005
    links.new(quadratic_bézier_005.outputs[0], join_geometry_002.inputs[0])

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (-700.0, -1760.0)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(bi_rail_loft.outputs[2], separate_x_y_z.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (-520.0, -1700.0)
    compare.bl_label = "Compare"
    compare.operation = "LESS_EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.85999995470047
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
    compare.inputs[12].default_value = 0.3709999918937683
    # Links for compare
    links.new(separate_x_y_z.outputs[0], compare.inputs[0])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.label = ""
    extrude_mesh.location = (60.0, -1660.0)
    extrude_mesh.bl_label = "Extrude Mesh"
    extrude_mesh.mode = "FACES"
    # Offset
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.0010000000474974513
    # Individual
    extrude_mesh.inputs[4].default_value = False
    # Links for extrude_mesh

    pipes = nodes.new("GeometryNodeGroup")
    pipes.name = "Pipes"
    pipes.label = ""
    pipes.location = (640.0, -1820.0)
    pipes.node_tree = create_pipes_group()
    pipes.bl_label = "Group"
    # Links for pipes

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (480.0, -1820.0)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "FACE"
    # Links for separate_geometry
    links.new(separate_geometry.outputs[0], pipes.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry.inputs[1])
    links.new(extrude_mesh.outputs[0], separate_geometry.inputs[0])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (1680.0, -1460.0)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(pipes.outputs[0], join_geometry_001.inputs[0])
    links.new(extrude_mesh.outputs[0], join_geometry_001.inputs[0])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (360.0, -740.0)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Links for mesh_to_curve
    links.new(bi_rail_loft.outputs[0], mesh_to_curve.inputs[0])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.label = ""
    compare_002.location = (360.0, -880.0)
    compare_002.bl_label = "Compare"
    compare_002.operation = "EQUAL"
    compare_002.data_type = "FLOAT"
    compare_002.mode = "ELEMENT"
    # B
    compare_002.inputs[1].default_value = 0.0
    # A
    compare_002.inputs[2].default_value = 0
    # B
    compare_002.inputs[3].default_value = 0
    # A
    compare_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_002.inputs[5].default_value = [0.0, 0.0, 0.0]
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
    compare_002.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_002.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_002
    links.new(separate_x_y_z.outputs[0], compare_002.inputs[0])
    links.new(compare_002.outputs[0], mesh_to_curve.inputs[1])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (920.0, -760.0)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh.inputs[2].default_value = 0.6599999666213989
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh

    quadrilateral = nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
    quadrilateral.name = "Quadrilateral"
    quadrilateral.label = ""
    quadrilateral.location = (240.0, -1020.0)
    quadrilateral.bl_label = "Quadrilateral"
    quadrilateral.mode = "RECTANGLE"
    # Width
    quadrilateral.inputs[0].default_value = 0.0430000014603138
    # Height
    quadrilateral.inputs[1].default_value = 0.006000000052154064
    # Bottom Width
    quadrilateral.inputs[2].default_value = 4.0
    # Top Width
    quadrilateral.inputs[3].default_value = 2.0
    # Offset
    quadrilateral.inputs[4].default_value = 1.0
    # Bottom Height
    quadrilateral.inputs[5].default_value = 3.0
    # Top Height
    quadrilateral.inputs[6].default_value = 1.0
    # Point 1
    quadrilateral.inputs[7].default_value = Vector((-1.0, -1.0, 0.0))
    # Point 2
    quadrilateral.inputs[8].default_value = Vector((1.0, -1.0, 0.0))
    # Point 3
    quadrilateral.inputs[9].default_value = Vector((1.0, 1.0, 0.0))
    # Point 4
    quadrilateral.inputs[10].default_value = Vector((-1.0, 1.0, 0.0))
    # Links for quadrilateral

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (1080.0, -760.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = False
    # Links for set_shade_smooth
    links.new(curve_to_mesh.outputs[0], set_shade_smooth.inputs[0])

    subdivide_curve = nodes.new("GeometryNodeSubdivideCurve")
    subdivide_curve.name = "Subdivide Curve"
    subdivide_curve.label = ""
    subdivide_curve.location = (400.0, -1020.0)
    subdivide_curve.bl_label = "Subdivide Curve"
    # Cuts
    subdivide_curve.inputs[1].default_value = 3
    # Links for subdivide_curve
    links.new(quadrilateral.outputs[0], subdivide_curve.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (560.0, -1020.0)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Position
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position
    links.new(subdivide_curve.outputs[0], set_position.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (-240.0, -1140.0)
    position.bl_label = "Position"
    # Links for position

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (-240.0, -1200.0)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001
    links.new(position.outputs[0], separate_x_y_z_001.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-80.0, -1140.0)
    math.bl_label = "Math"
    math.operation = "ABSOLUTE"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.5
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(separate_x_y_z_001.outputs[0], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (80.0, -1140.0)
    math_001.bl_label = "Math"
    math_001.operation = "DIVIDE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 0.0215000007301569
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math.outputs[0], math_001.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (240.0, -1140.0)
    math_002.bl_label = "Math"
    math_002.operation = "POWER"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 2.0
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(math_001.outputs[0], math_002.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (400.0, -1140.0)
    math_003.bl_label = "Math"
    math_003.operation = "MULTIPLY"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 0.0020000000949949026
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_002.outputs[0], math_003.inputs[0])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (560.0, -1140.0)
    combine_x_y_z.bl_label = "Combine XYZ"
    # X
    combine_x_y_z.inputs[0].default_value = 0.0
    # Z
    combine_x_y_z.inputs[2].default_value = 0.0
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], set_position.inputs[3])
    links.new(math_003.outputs[0], combine_x_y_z.inputs[1])

    fillet_curve = nodes.new("GeometryNodeFilletCurve")
    fillet_curve.name = "Fillet Curve"
    fillet_curve.label = ""
    fillet_curve.location = (720.0, -1020.0)
    fillet_curve.bl_label = "Fillet Curve"
    # Radius
    fillet_curve.inputs[1].default_value = 0.0010000000474974513
    # Limit Radius
    fillet_curve.inputs[2].default_value = True
    # Mode
    fillet_curve.inputs[3].default_value = "Bézier"
    # Count
    fillet_curve.inputs[4].default_value = 1
    # Links for fillet_curve
    links.new(fillet_curve.outputs[0], curve_to_mesh.inputs[1])
    links.new(set_position.outputs[0], fillet_curve.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    set_curve_tilt.label = ""
    set_curve_tilt.location = (760.0, -760.0)
    set_curve_tilt.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Tilt
    set_curve_tilt.inputs[2].default_value = 3.1415927410125732
    # Links for set_curve_tilt
    links.new(set_curve_tilt.outputs[0], curve_to_mesh.inputs[0])

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.label = ""
    boolean_math_003.location = (-120.0, -1780.0)
    boolean_math_003.bl_label = "Boolean Math"
    boolean_math_003.operation = "NOT"
    # Boolean
    boolean_math_003.inputs[1].default_value = False
    # Links for boolean_math_003
    links.new(boolean_math_003.outputs[0], extrude_mesh.inputs[1])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (440.0, -1620.0)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "OR"
    # Links for boolean_math
    links.new(extrude_mesh.outputs[1], boolean_math.inputs[0])
    links.new(extrude_mesh.outputs[2], boolean_math.inputs[1])

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.name = "Separate Geometry.001"
    separate_geometry_001.label = ""
    separate_geometry_001.location = (640.0, -1500.0)
    separate_geometry_001.bl_label = "Separate Geometry"
    separate_geometry_001.domain = "FACE"
    # Links for separate_geometry_001
    links.new(extrude_mesh.outputs[0], separate_geometry_001.inputs[0])
    links.new(boolean_math.outputs[0], separate_geometry_001.inputs[1])

    rivet = nodes.new("GeometryNodeGroup")
    rivet.name = "Pipes.001"
    rivet.label = ""
    rivet.location = (1100.0, -1280.0)
    rivet.node_tree = create_rivet_group()
    rivet.bl_label = "Group"
    # Corners
    rivet.inputs[1].default_value = False
    # Offset
    rivet.inputs[2].default_value = -1.279999852180481
    # Spacing
    rivet.inputs[3].default_value = 0.9399999976158142
    # Links for rivet
    links.new(separate_geometry_001.outputs[1], rivet.inputs[0])
    links.new(rivet.outputs[0], join_geometry_001.inputs[0])

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (1360.0, -760.0)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "FACE"
    # Links for delete_geometry
    links.new(delete_geometry.outputs[0], join_geometry_001.inputs[0])
    links.new(set_shade_smooth.outputs[0], delete_geometry.inputs[0])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (1040.0, -980.0)
    position_001.bl_label = "Position"
    # Links for position_001

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_002.name = "Separate XYZ.002"
    separate_x_y_z_002.label = ""
    separate_x_y_z_002.location = (1040.0, -1040.0)
    separate_x_y_z_002.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_002
    links.new(position_001.outputs[0], separate_x_y_z_002.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (1200.0, -1040.0)
    compare_001.bl_label = "Compare"
    compare_001.operation = "GREATER_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = 0.0
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
    links.new(separate_x_y_z_002.outputs[0], compare_001.inputs[0])
    links.new(compare_001.outputs[0], delete_geometry.inputs[1])

    trim_curve = nodes.new("GeometryNodeTrimCurve")
    trim_curve.name = "Trim Curve"
    trim_curve.label = ""
    trim_curve.location = (580.0, -760.0)
    trim_curve.bl_label = "Trim Curve"
    trim_curve.mode = "FACTOR"
    # Selection
    trim_curve.inputs[1].default_value = True
    # Start
    trim_curve.inputs[2].default_value = 0.0
    # End
    trim_curve.inputs[3].default_value = 0.8569066524505615
    # Start
    trim_curve.inputs[4].default_value = 0.0
    # End
    trim_curve.inputs[5].default_value = 1.0
    # Links for trim_curve
    links.new(trim_curve.outputs[0], set_curve_tilt.inputs[0])
    links.new(mesh_to_curve.outputs[0], trim_curve.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.name = "Set Shade Smooth.001"
    set_shade_smooth_001.label = ""
    set_shade_smooth_001.location = (4540.0, -1500.0)
    set_shade_smooth_001.bl_label = "Set Shade Smooth"
    set_shade_smooth_001.domain = "EDGE"
    # Shade Smooth
    set_shade_smooth_001.inputs[2].default_value = False
    # Links for set_shade_smooth_001

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (4880.0, -1700.0)
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
    links.new(set_shade_smooth_001.outputs[0], transform_geometry.inputs[0])

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (5260.0, -1520.0)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003
    links.new(set_shade_smooth_001.outputs[0], join_geometry_003.inputs[0])

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.name = "Flip Faces"
    flip_faces.label = ""
    flip_faces.location = (5060.0, -1700.0)
    flip_faces.bl_label = "Flip Faces"
    # Selection
    flip_faces.inputs[1].default_value = True
    # Links for flip_faces
    links.new(flip_faces.outputs[0], join_geometry_003.inputs[0])
    links.new(transform_geometry.outputs[0], flip_faces.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (369.0, -29.0)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Count"
    # Count
    resample_curve.inputs[3].default_value = 47
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve

    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.label = ""
    delete_geometry_001.location = (909.0, -29.0)
    delete_geometry_001.bl_label = "Delete Geometry"
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "FACE"
    # Links for delete_geometry_001

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (909.0, -369.0)
    position_003.bl_label = "Position"
    # Links for position_003

    separate_x_y_z_005 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_005.name = "Separate XYZ.005"
    separate_x_y_z_005.label = ""
    separate_x_y_z_005.location = (909.0, -289.0)
    separate_x_y_z_005.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_005
    links.new(position_003.outputs[0], separate_x_y_z_005.inputs[0])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (909.0, -149.0)
    compare_003.bl_label = "Compare"
    compare_003.operation = "GREATER_THAN"
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
    links.new(separate_x_y_z_005.outputs[0], compare_003.inputs[0])
    links.new(compare_003.outputs[0], delete_geometry_001.inputs[1])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (8600.0, -180.0)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(join_geometry_004.outputs[0], group_output.inputs[0])
    links.new(join_geometry_003.outputs[0], join_geometry_004.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (1658.0, -724.800048828125)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(delete_geometry_001.outputs[0], join_geometry_005.inputs[0])

    trim_curve_001 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_001.name = "Trim Curve.001"
    trim_curve_001.label = ""
    trim_curve_001.location = (209.0, -29.0)
    trim_curve_001.bl_label = "Trim Curve"
    trim_curve_001.mode = "FACTOR"
    # Selection
    trim_curve_001.inputs[1].default_value = True
    # Start
    trim_curve_001.inputs[2].default_value = 0.0
    # End
    trim_curve_001.inputs[3].default_value = 0.8784530162811279
    # Start
    trim_curve_001.inputs[4].default_value = 0.0
    # End
    trim_curve_001.inputs[5].default_value = 1.0
    # Links for trim_curve_001
    links.new(trim_curve_001.outputs[0], resample_curve.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (29.0, -29.0)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((0.0, -0.0020000000949949026, 0.0))
    # Rotation
    transform_geometry_001.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_001
    links.new(transform_geometry_001.outputs[0], trim_curve_001.inputs[0])
    links.new(join_splines_1.outputs[0], transform_geometry_001.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (1878.0, -704.800048828125)
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
    links.new(join_geometry_005.outputs[0], store_named_attribute.inputs[0])

    gold_decorations = nodes.new("GeometryNodeGroup")
    gold_decorations.name = "Group.003"
    gold_decorations.label = ""
    gold_decorations.location = (729.0, -29.0)
    gold_decorations.node_tree = create_gold__decorations_group()
    gold_decorations.bl_label = "Group"
    # Seed
    gold_decorations.inputs[1].default_value = 54
    # Scale
    gold_decorations.inputs[2].default_value = 4.0
    # Count
    gold_decorations.inputs[3].default_value = 20
    # Links for gold_decorations
    links.new(gold_decorations.outputs[0], delete_geometry_001.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (509.0, -29.0)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Count"
    # Count
    resample_curve_001.inputs[3].default_value = 47
    # Length
    resample_curve_001.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_001

    trim_curve_002 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_002.name = "Trim Curve.002"
    trim_curve_002.label = ""
    trim_curve_002.location = (349.0, -29.0)
    trim_curve_002.bl_label = "Trim Curve"
    trim_curve_002.mode = "FACTOR"
    # Selection
    trim_curve_002.inputs[1].default_value = True
    # Start
    trim_curve_002.inputs[2].default_value = 0.0
    # End
    trim_curve_002.inputs[3].default_value = 0.6187845468521118
    # Start
    trim_curve_002.inputs[4].default_value = 0.0
    # End
    trim_curve_002.inputs[5].default_value = 1.0
    # Links for trim_curve_002
    links.new(trim_curve_002.outputs[0], resample_curve_001.inputs[0])

    gold_decorations_1 = nodes.new("GeometryNodeGroup")
    gold_decorations_1.name = "Group.004"
    gold_decorations_1.label = ""
    gold_decorations_1.location = (849.0, -29.0)
    gold_decorations_1.node_tree = create_gold__decorations_group()
    gold_decorations_1.bl_label = "Group"
    # Seed
    gold_decorations_1.inputs[1].default_value = 58
    # Scale
    gold_decorations_1.inputs[2].default_value = 2.0
    # Count
    gold_decorations_1.inputs[3].default_value = 18
    # Links for gold_decorations_1
    links.new(gold_decorations_1.outputs[0], join_geometry_005.inputs[0])

    set_curve_normal = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal.name = "Set Curve Normal"
    set_curve_normal.label = ""
    set_curve_normal.location = (669.0, -29.0)
    set_curve_normal.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal.inputs[1].default_value = True
    # Mode
    set_curve_normal.inputs[2].default_value = "Free"
    # Links for set_curve_normal
    links.new(set_curve_normal.outputs[0], gold_decorations_1.inputs[0])
    links.new(resample_curve_001.outputs[0], set_curve_normal.inputs[0])

    sample_nearest_surface = nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.name = "Sample Nearest Surface"
    sample_nearest_surface.label = ""
    sample_nearest_surface.location = (309.0, -189.0)
    sample_nearest_surface.bl_label = "Sample Nearest Surface"
    sample_nearest_surface.data_type = "FLOAT_VECTOR"
    # Group ID
    sample_nearest_surface.inputs[2].default_value = 0
    # Sample Position
    sample_nearest_surface.inputs[3].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    sample_nearest_surface.inputs[4].default_value = 0
    # Links for sample_nearest_surface
    links.new(bi_rail_loft.outputs[0], sample_nearest_surface.inputs[0])

    normal = nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.label = ""
    normal.location = (309.0, -409.0)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = False
    # Links for normal
    links.new(normal.outputs[0], sample_nearest_surface.inputs[1])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (469.0, -189.0)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "CROSS_PRODUCT"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(vector_math.outputs[0], set_curve_normal.inputs[3])
    links.new(sample_nearest_surface.outputs[0], vector_math.inputs[0])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (469.0, -329.0)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent
    links.new(curve_tangent.outputs[0], vector_math.inputs[1])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.name = "Separate Geometry.002"
    separate_geometry_002.label = ""
    separate_geometry_002.location = (29.0, -29.0)
    separate_geometry_002.bl_label = "Separate Geometry"
    separate_geometry_002.domain = "EDGE"
    # Links for separate_geometry_002
    links.new(separate_geometry_001.outputs[0], separate_geometry_002.inputs[0])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.label = ""
    boolean_math_001.location = (200.0, -1480.0)
    boolean_math_001.bl_label = "Boolean Math"
    boolean_math_001.operation = "AND"
    # Links for boolean_math_001
    links.new(boolean_math_001.outputs[0], separate_geometry_002.inputs[1])
    links.new(extrude_mesh.outputs[1], boolean_math_001.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (189.0, -29.0)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Selection
    mesh_to_curve_001.inputs[1].default_value = True
    # Links for mesh_to_curve_001
    links.new(separate_geometry_002.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(mesh_to_curve_001.outputs[0], trim_curve_002.inputs[0])

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = ""
    frame_005.location = (189.0, -515.800048828125)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = ""
    frame_006.location = (209.0, -35.800048828125)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    set_curve_tilt_001 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_001.name = "Set Curve Tilt.001"
    set_curve_tilt_001.label = ""
    set_curve_tilt_001.location = (549.0, -29.0)
    set_curve_tilt_001.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_001.inputs[1].default_value = True
    # Tilt
    set_curve_tilt_001.inputs[2].default_value = -0.16580626368522644
    # Links for set_curve_tilt_001
    links.new(set_curve_tilt_001.outputs[0], gold_decorations.inputs[0])
    links.new(resample_curve.outputs[0], set_curve_tilt_001.inputs[0])

    separate_geometry_003 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_003.name = "Separate Geometry.003"
    separate_geometry_003.label = ""
    separate_geometry_003.location = (438.0, -1184.800048828125)
    separate_geometry_003.bl_label = "Separate Geometry"
    separate_geometry_003.domain = "FACE"
    # Links for separate_geometry_003
    links.new(extrude_mesh.outputs[0], separate_geometry_003.inputs[0])
    links.new(extrude_mesh.outputs[1], separate_geometry_003.inputs[1])

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.name = "Group.002"
    gold_on_band.label = ""
    gold_on_band.location = (658.0, -1184.800048828125)
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.bl_label = "Group"
    # Density
    gold_on_band.inputs[1].default_value = 200000.0
    # W
    gold_on_band.inputs[2].default_value = 8.669999122619629
    # Seed
    gold_on_band.inputs[3].default_value = 1
    # Links for gold_on_band
    links.new(separate_geometry_003.outputs[0], gold_on_band.inputs[0])
    links.new(gold_on_band.outputs[0], join_geometry_005.inputs[0])

    frame_007 = nodes.new("NodeFrame")
    frame_007.name = "Frame.007"
    frame_007.label = "Gold"
    frame_007.location = (1942.0, 2584.800048828125)
    frame_007.bl_label = "Frame"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20
    # Links for frame_007

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (4138.0, -984.800048828125)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(switch.outputs[0], join_geometry_004.inputs[0])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (3858.0, -884.800048828125)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch.inputs[0])

    bézier_segment_004 = nodes.new("GeometryNodeCurvePrimitiveBezierSegment")
    bézier_segment_004.name = "Bézier Segment.004"
    bézier_segment_004.label = ""
    bézier_segment_004.location = (229.0, -135.79998779296875)
    bézier_segment_004.bl_label = "Bézier Segment"
    bézier_segment_004.mode = "OFFSET"
    # Resolution
    bézier_segment_004.inputs[0].default_value = 16
    # Start
    bézier_segment_004.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Start Handle
    bézier_segment_004.inputs[2].default_value = Vector((1.0299999713897705, -0.6199999451637268, 0.0))
    # End Handle
    bézier_segment_004.inputs[3].default_value = Vector((-0.8299999833106995, -0.4300000071525574, 0.0))
    # End
    bézier_segment_004.inputs[4].default_value = Vector((1.0, 0.0, 0.0))
    # Links for bézier_segment_004
    links.new(bézier_segment_004.outputs[0], join_geometry_002.inputs[0])

    boolean_math_004 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.name = "Boolean Math.004"
    boolean_math_004.label = ""
    boolean_math_004.location = (-360.0, -1700.0)
    boolean_math_004.bl_label = "Boolean Math"
    boolean_math_004.operation = "AND"
    # Links for boolean_math_004
    links.new(boolean_math_004.outputs[0], boolean_math_003.inputs[0])
    links.new(boolean_math_004.outputs[0], boolean_math_001.inputs[0])
    links.new(compare.outputs[0], boolean_math_004.inputs[0])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (-520.0, -1860.0)
    compare_004.bl_label = "Compare"
    compare_004.operation = "GREATER_THAN"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    # B
    compare_004.inputs[1].default_value = 0.06999994814395905
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
    compare_004.inputs[12].default_value = 0.3709999918937683
    # Links for compare_004
    links.new(separate_x_y_z.outputs[1], compare_004.inputs[0])
    links.new(compare_004.outputs[0], boolean_math_004.inputs[1])

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.name = "Gem in Holder"
    gem_in_holder.label = ""
    gem_in_holder.location = (1109.0, -155.7999267578125)
    gem_in_holder.node_tree = create_gem_in__holder_group()
    gem_in_holder.bl_label = "Group"
    # Gem Radius
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder.inputs[2].default_value = False
    # Scale
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    # Wings
    gem_in_holder.inputs[6].default_value = True
    # Links for gem_in_holder

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (189.0, -475.7999267578125)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "COUNT"
    # Count
    curve_to_points.inputs[1].default_value = 10
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points

    for_each_geometry_element_input = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input.name = "For Each Geometry Element Input"
    for_each_geometry_element_input.label = ""
    for_each_geometry_element_input.location = (409.0, -415.7999267578125)
    for_each_geometry_element_input.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input.inputs[1].default_value = True
    # Links for for_each_geometry_element_input
    links.new(curve_to_points.outputs[0], for_each_geometry_element_input.inputs[0])
    links.new(curve_to_points.outputs[3], for_each_geometry_element_input.inputs[2])

    for_each_geometry_element_output = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.name = "For Each Geometry Element Output"
    for_each_geometry_element_output.label = ""
    for_each_geometry_element_output.location = (2029.0, -455.7999267578125)
    for_each_geometry_element_output.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output.active_input_index = 1
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = "POINT"
    for_each_geometry_element_output.inspection_index = 0
    # Links for for_each_geometry_element_output

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (189.0, -675.7999267578125)
    position_002.bl_label = "Position"
    # Links for position_002
    links.new(position_002.outputs[0], for_each_geometry_element_input.inputs[3])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    transform_geometry_002.label = ""
    transform_geometry_002.location = (1389.0, -475.7999267578125)
    transform_geometry_002.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_002.inputs[1].default_value = "Components"
    # Links for transform_geometry_002
    links.new(gem_in_holder.outputs[0], transform_geometry_002.inputs[0])
    links.new(for_each_geometry_element_input.outputs[3], transform_geometry_002.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.name = "Rotate Rotation"
    rotate_rotation.label = ""
    rotate_rotation.location = (1049.0, -675.7999267578125)
    rotate_rotation.bl_label = "Rotate Rotation"
    rotate_rotation.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation.inputs[1].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')
    # Links for rotate_rotation
    links.new(for_each_geometry_element_input.outputs[2], rotate_rotation.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (649.0, -395.7999267578125)
    random_value.bl_label = "Random Value"
    random_value.data_type = "INT"
    # Min
    random_value.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value.inputs[2].default_value = 0.0
    # Max
    random_value.inputs[3].default_value = 1.0
    # Min
    random_value.inputs[4].default_value = 5
    # Max
    random_value.inputs[5].default_value = 7
    # Probability
    random_value.inputs[6].default_value = 0.5
    # Seed
    random_value.inputs[8].default_value = 0
    # Links for random_value
    links.new(for_each_geometry_element_input.outputs[0], random_value.inputs[7])
    links.new(random_value.outputs[2], gem_in_holder.inputs[7])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    transform_geometry_003.label = ""
    transform_geometry_003.location = (1569.0, -475.7999267578125)
    transform_geometry_003.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_003.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_003.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    # Rotation
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_003.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_003
    links.new(transform_geometry_002.outputs[0], transform_geometry_003.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.label = ""
    join_geometry_006.location = (3878.0, -1064.800048828125)
    join_geometry_006.bl_label = "Join Geometry"
    # Links for join_geometry_006
    links.new(join_geometry_006.outputs[0], switch.inputs[2])
    links.new(store_named_attribute.outputs[0], join_geometry_006.inputs[0])
    links.new(for_each_geometry_element_output.outputs[2], join_geometry_006.inputs[0])

    trim_curve_003 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_003.name = "Trim Curve.003"
    trim_curve_003.label = ""
    trim_curve_003.location = (29.0, -475.7999267578125)
    trim_curve_003.bl_label = "Trim Curve"
    trim_curve_003.mode = "FACTOR"
    # Selection
    trim_curve_003.inputs[1].default_value = True
    # Start
    trim_curve_003.inputs[2].default_value = 0.04999999701976776
    # End
    trim_curve_003.inputs[3].default_value = 0.9000000953674316
    # Start
    trim_curve_003.inputs[4].default_value = 0.0
    # End
    trim_curve_003.inputs[5].default_value = 1.0
    # Links for trim_curve_003
    links.new(trim_curve_003.outputs[0], curve_to_points.inputs[0])
    links.new(set_curve_tilt.outputs[0], trim_curve_003.inputs[0])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.label = ""
    random_value_001.location = (629.0, -615.7999267578125)
    random_value_001.bl_label = "Random Value"
    random_value_001.data_type = "FLOAT"
    # Min
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_001.inputs[2].default_value = 0.25
    # Max
    random_value_001.inputs[3].default_value = 0.550000011920929
    # Min
    random_value_001.inputs[4].default_value = 0
    # Max
    random_value_001.inputs[5].default_value = 100
    # Probability
    random_value_001.inputs[6].default_value = 0.5
    # Seed
    random_value_001.inputs[8].default_value = 0
    # Links for random_value_001
    links.new(for_each_geometry_element_input.outputs[0], random_value_001.inputs[7])
    links.new(random_value_001.outputs[1], transform_geometry_002.inputs[4])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (1809.0, -495.7999267578125)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001
    links.new(store_named_attribute_001.outputs[0], for_each_geometry_element_output.inputs[1])
    links.new(transform_geometry_003.outputs[0], store_named_attribute_001.inputs[0])

    random_value_002 = nodes.new("FunctionNodeRandomValue")
    random_value_002.name = "Random Value.002"
    random_value_002.label = ""
    random_value_002.location = (649.0, -215.7999267578125)
    random_value_002.bl_label = "Random Value"
    random_value_002.data_type = "FLOAT"
    # Min
    random_value_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_002.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_002.inputs[2].default_value = 0.0
    # Max
    random_value_002.inputs[3].default_value = 100.0
    # Min
    random_value_002.inputs[4].default_value = 3
    # Max
    random_value_002.inputs[5].default_value = 7
    # Probability
    random_value_002.inputs[6].default_value = 0.5
    # Seed
    random_value_002.inputs[8].default_value = 13
    # Links for random_value_002
    links.new(for_each_geometry_element_input.outputs[0], random_value_002.inputs[7])
    links.new(random_value_002.outputs[1], gem_in_holder.inputs[10])

    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.name = "Rotate Rotation.001"
    rotate_rotation_001.label = ""
    rotate_rotation_001.location = (1209.0, -675.7999267578125)
    rotate_rotation_001.bl_label = "Rotate Rotation"
    rotate_rotation_001.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_001.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
    # Links for rotate_rotation_001
    links.new(rotate_rotation_001.outputs[0], transform_geometry_002.inputs[3])
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])

    random_value_003 = nodes.new("FunctionNodeRandomValue")
    random_value_003.name = "Random Value.003"
    random_value_003.label = ""
    random_value_003.location = (649.0, -35.7999267578125)
    random_value_003.bl_label = "Random Value"
    random_value_003.data_type = "FLOAT"
    # Min
    random_value_003.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_003.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_003.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_003.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_003.inputs[4].default_value = 3
    # Max
    random_value_003.inputs[5].default_value = 7
    # Probability
    random_value_003.inputs[6].default_value = 0.5
    # Seed
    random_value_003.inputs[8].default_value = 0
    # Links for random_value_003
    links.new(for_each_geometry_element_input.outputs[0], random_value_003.inputs[7])
    links.new(random_value_003.outputs[1], gem_in_holder.inputs[9])

    random_value_004 = nodes.new("FunctionNodeRandomValue")
    random_value_004.name = "Random Value.004"
    random_value_004.label = ""
    random_value_004.location = (889.0, -255.7999267578125)
    random_value_004.bl_label = "Random Value"
    random_value_004.data_type = "INT"
    # Min
    random_value_004.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_004.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_004.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_004.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_004.inputs[4].default_value = 0
    # Max
    random_value_004.inputs[5].default_value = 100
    # Probability
    random_value_004.inputs[6].default_value = 0.5
    # Seed
    random_value_004.inputs[8].default_value = 0
    # Links for random_value_004
    links.new(for_each_geometry_element_input.outputs[0], random_value_004.inputs[7])
    links.new(random_value_004.outputs[2], gem_in_holder.inputs[5])

    random_value_005 = nodes.new("FunctionNodeRandomValue")
    random_value_005.name = "Random Value.005"
    random_value_005.label = ""
    random_value_005.location = (889.0, -75.7999267578125)
    random_value_005.bl_label = "Random Value"
    random_value_005.data_type = "INT"
    # Min
    random_value_005.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_005.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_005.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_005.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_005.inputs[4].default_value = 6
    # Max
    random_value_005.inputs[5].default_value = 20
    # Probability
    random_value_005.inputs[6].default_value = 0.5
    # Seed
    random_value_005.inputs[8].default_value = 0
    # Links for random_value_005
    links.new(for_each_geometry_element_input.outputs[0], random_value_005.inputs[7])
    links.new(random_value_005.outputs[2], gem_in_holder.inputs[4])

    random_value_006 = nodes.new("FunctionNodeRandomValue")
    random_value_006.name = "Random Value.006"
    random_value_006.label = ""
    random_value_006.location = (889.0, -435.7999267578125)
    random_value_006.bl_label = "Random Value"
    random_value_006.data_type = "INT"
    # Min
    random_value_006.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_006.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_006.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_006.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_006.inputs[4].default_value = 5
    # Max
    random_value_006.inputs[5].default_value = 30
    # Probability
    random_value_006.inputs[6].default_value = 0.5
    # Seed
    random_value_006.inputs[8].default_value = 0
    # Links for random_value_006
    links.new(for_each_geometry_element_input.outputs[0], random_value_006.inputs[7])
    links.new(random_value_006.outputs[2], gem_in_holder.inputs[8])

    frame_008 = nodes.new("NodeFrame")
    frame_008.name = "Frame.008"
    frame_008.label = "Broaches"
    frame_008.location = (29.0, -1389.0001220703125)
    frame_008.bl_label = "Frame"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20
    # Links for frame_008

    set_shade_smooth_002 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_002.name = "Set Shade Smooth.002"
    set_shade_smooth_002.label = ""
    set_shade_smooth_002.location = (4380.0, -1500.0)
    set_shade_smooth_002.bl_label = "Set Shade Smooth"
    set_shade_smooth_002.domain = "FACE"
    # Selection
    set_shade_smooth_002.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_002.inputs[2].default_value = True
    # Links for set_shade_smooth_002
    links.new(set_shade_smooth_002.outputs[0], set_shade_smooth_001.inputs[0])
    links.new(join_geometry_001.outputs[0], set_shade_smooth_002.inputs[0])

    edge_angle = nodes.new("GeometryNodeInputMeshEdgeAngle")
    edge_angle.name = "Edge Angle"
    edge_angle.label = ""
    edge_angle.location = (4380.0, -1640.0)
    edge_angle.bl_label = "Edge Angle"
    # Links for edge_angle

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (4540.0, -1640.0)
    compare_005.bl_label = "Compare"
    compare_005.operation = "GREATER_THAN"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    # B
    compare_005.inputs[1].default_value = 1.0
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
    compare_005.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_005
    links.new(edge_angle.outputs[0], compare_005.inputs[0])
    links.new(compare_005.outputs[0], set_shade_smooth_001.inputs[1])

    gem_in_holder_1 = nodes.new("GeometryNodeGroup")
    gem_in_holder_1.name = "Gem in Holder.001"
    gem_in_holder_1.label = ""
    gem_in_holder_1.location = (1209.0, -75.13334655761719)
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

    mesh_to_curve_002 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.name = "Mesh to Curve.002"
    mesh_to_curve_002.label = ""
    mesh_to_curve_002.location = (29.0, -55.13334655761719)
    mesh_to_curve_002.bl_label = "Mesh to Curve"
    mesh_to_curve_002.mode = "EDGES"
    # Links for mesh_to_curve_002

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Is Edge Boundary"
    is_edge_boundary.label = ""
    is_edge_boundary.location = (29.0, -175.1333465576172)
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    is_edge_boundary.bl_label = "Group"
    # Links for is_edge_boundary
    links.new(is_edge_boundary.outputs[0], mesh_to_curve_002.inputs[1])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    set_spline_cyclic.label = ""
    set_spline_cyclic.location = (349.0, -55.13334655761719)
    set_spline_cyclic.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = False
    # Links for set_spline_cyclic

    trim_curve_004 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_004.name = "Trim Curve.004"
    trim_curve_004.label = ""
    trim_curve_004.location = (509.0, -55.13334655761719)
    trim_curve_004.bl_label = "Trim Curve"
    trim_curve_004.mode = "FACTOR"
    # Selection
    trim_curve_004.inputs[1].default_value = True
    # Start
    trim_curve_004.inputs[2].default_value = 0.6629834175109863
    # End
    trim_curve_004.inputs[3].default_value = 0.9834254384040833
    # Start
    trim_curve_004.inputs[4].default_value = 0.0
    # End
    trim_curve_004.inputs[5].default_value = 1.0
    # Links for trim_curve_004
    links.new(set_spline_cyclic.outputs[0], trim_curve_004.inputs[0])

    curve_to_points_001 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.name = "Curve to Points.001"
    curve_to_points_001.label = ""
    curve_to_points_001.location = (669.0, -55.13334655761719)
    curve_to_points_001.bl_label = "Curve to Points"
    curve_to_points_001.mode = "COUNT"
    # Count
    curve_to_points_001.inputs[1].default_value = 50
    # Length
    curve_to_points_001.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points_001
    links.new(trim_curve_004.outputs[0], curve_to_points_001.inputs[0])

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.label = ""
    capture_attribute.location = (-200.0, -1480.0)
    capture_attribute.bl_label = "Capture Attribute"
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    # Links for capture_attribute
    links.new(bi_rail_loft.outputs[0], capture_attribute.inputs[0])
    links.new(capture_attribute.outputs[0], extrude_mesh.inputs[0])

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.name = "Normal.001"
    normal_001.label = ""
    normal_001.location = (-200.0, -1600.0)
    normal_001.bl_label = "Normal"
    normal_001.legacy_corner_normals = False
    # Links for normal_001
    links.new(normal_001.outputs[0], capture_attribute.inputs[1])

    set_curve_normal_001 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.name = "Set Curve Normal.001"
    set_curve_normal_001.label = ""
    set_curve_normal_001.location = (189.0, -55.13334655761719)
    set_curve_normal_001.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_001.inputs[1].default_value = True
    # Mode
    set_curve_normal_001.inputs[2].default_value = "Free"
    # Links for set_curve_normal_001
    links.new(set_curve_normal_001.outputs[0], set_spline_cyclic.inputs[0])
    links.new(mesh_to_curve_002.outputs[0], set_curve_normal_001.inputs[0])
    links.new(capture_attribute.outputs[1], set_curve_normal_001.inputs[3])

    position_004 = nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"
    position_004.label = ""
    position_004.location = (669.0, -255.1333465576172)
    position_004.bl_label = "Position"
    # Links for position_004

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.name = "For Each Geometry Element Input.001"
    for_each_geometry_element_input_001.label = ""
    for_each_geometry_element_input_001.location = (829.0, -55.13334655761719)
    for_each_geometry_element_input_001.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input_001.inputs[1].default_value = True
    # Links for for_each_geometry_element_input_001
    links.new(curve_to_points_001.outputs[0], for_each_geometry_element_input_001.inputs[0])
    links.new(position_004.outputs[0], for_each_geometry_element_input_001.inputs[2])
    links.new(curve_to_points_001.outputs[3], for_each_geometry_element_input_001.inputs[3])

    for_each_geometry_element_output_001 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.name = "For Each Geometry Element Output.001"
    for_each_geometry_element_output_001.label = ""
    for_each_geometry_element_output_001.location = (2169.0, -75.13334655761719)
    for_each_geometry_element_output_001.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    # Links for for_each_geometry_element_output_001
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_006.inputs[0])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    transform_geometry_004.label = ""
    transform_geometry_004.location = (1469.0, -75.13334655761719)
    transform_geometry_004.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_004.inputs[1].default_value = "Components"
    # Scale
    transform_geometry_004.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_004
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_004.inputs[2])
    links.new(gem_in_holder_1.outputs[4], transform_geometry_004.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.name = "Rotate Rotation.002"
    rotate_rotation_002.label = ""
    rotate_rotation_002.location = (869.0, -315.13336181640625)
    rotate_rotation_002.bl_label = "Rotate Rotation"
    rotate_rotation_002.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, -1.5707963705062866, 0.0), 'XYZ')
    # Links for rotate_rotation_002
    links.new(rotate_rotation_002.outputs[0], transform_geometry_004.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[3], rotate_rotation_002.inputs[0])

    frame_009 = nodes.new("NodeFrame")
    frame_009.name = "Frame.009"
    frame_009.label = "Random Wings"
    frame_009.location = (189.0, -2369.666748046875)
    frame_009.bl_label = "Frame"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20
    # Links for frame_009

    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.name = "Random Value.007"
    random_value_007.label = ""
    random_value_007.location = (1029.0, -75.13334655761719)
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
    random_value_008.location = (1029.0, -255.1333465576172)
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

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (38.0, -3284.800048828125)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(reroute.outputs[0], mesh_to_curve_002.inputs[0])
    links.new(separate_geometry.outputs[0], reroute.inputs[0])

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.name = "Distribute Points on Faces"
    distribute_points_on_faces.label = ""
    distribute_points_on_faces.location = (149.0, -35.79998779296875)
    distribute_points_on_faces.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces.distribute_method = "RANDOM"
    distribute_points_on_faces.use_legacy_normal = False
    # Selection
    distribute_points_on_faces.inputs[1].default_value = True
    # Distance Min
    distribute_points_on_faces.inputs[2].default_value = 0.0
    # Density Max
    distribute_points_on_faces.inputs[3].default_value = 10.0
    # Density
    distribute_points_on_faces.inputs[4].default_value = 5000.0
    # Density Factor
    distribute_points_on_faces.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces.inputs[6].default_value = 0
    # Links for distribute_points_on_faces
    links.new(reroute.outputs[0], distribute_points_on_faces.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (509.0, -35.79998779296875)
    instance_on_points.bl_label = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Rotation
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points
    links.new(distribute_points_on_faces.outputs[0], instance_on_points.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    ico_sphere.label = ""
    ico_sphere.location = (29.0, -235.79998779296875)
    ico_sphere.bl_label = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.0020000000949949026
    # Subdivisions
    ico_sphere.inputs[1].default_value = 2
    # Links for ico_sphere

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (689.0, -35.79998779296875)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "BOOLEAN"
    store_named_attribute_002.domain = "INSTANCE"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "ruby"
    # Links for store_named_attribute_002
    links.new(instance_on_points.outputs[0], store_named_attribute_002.inputs[0])

    random_value_009 = nodes.new("FunctionNodeRandomValue")
    random_value_009.name = "Random Value.009"
    random_value_009.label = ""
    random_value_009.location = (689.0, -195.79998779296875)
    random_value_009.bl_label = "Random Value"
    random_value_009.data_type = "BOOLEAN"
    # Min
    random_value_009.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_009.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_009.inputs[2].default_value = 0.0
    # Max
    random_value_009.inputs[3].default_value = 1.0
    # Min
    random_value_009.inputs[4].default_value = 0
    # Max
    random_value_009.inputs[5].default_value = 100
    # Probability
    random_value_009.inputs[6].default_value = 0.5
    # ID
    random_value_009.inputs[7].default_value = 0
    # Seed
    random_value_009.inputs[8].default_value = 0
    # Links for random_value_009
    links.new(random_value_009.outputs[3], store_named_attribute_002.inputs[3])

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.label = ""
    boolean_math_002.location = (869.0, -195.79998779296875)
    boolean_math_002.bl_label = "Boolean Math"
    boolean_math_002.operation = "NOT"
    # Boolean
    boolean_math_002.inputs[1].default_value = False
    # Links for boolean_math_002
    links.new(random_value_009.outputs[3], boolean_math_002.inputs[0])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (869.0, -35.79998779296875)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "INSTANCE"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "saphire"
    # Links for store_named_attribute_003
    links.new(store_named_attribute_002.outputs[0], store_named_attribute_003.inputs[0])
    links.new(boolean_math_002.outputs[0], store_named_attribute_003.inputs[3])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (1029.0, -35.79998779296875)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(store_named_attribute_003.outputs[0], realize_instances.inputs[0])
    links.new(realize_instances.outputs[0], join_geometry_006.inputs[0])

    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.name = "Set Shade Smooth.003"
    set_shade_smooth_003.label = ""
    set_shade_smooth_003.location = (209.0, -235.79998779296875)
    set_shade_smooth_003.bl_label = "Set Shade Smooth"
    set_shade_smooth_003.domain = "FACE"
    # Selection
    set_shade_smooth_003.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_003.inputs[2].default_value = True
    # Links for set_shade_smooth_003
    links.new(set_shade_smooth_003.outputs[0], instance_on_points.inputs[2])
    links.new(ico_sphere.outputs[0], set_shade_smooth_003.inputs[0])

    frame_010 = nodes.new("NodeFrame")
    frame_010.name = "Frame.010"
    frame_010.label = "Random Jewels"
    frame_010.location = (629.0, -3209.0)
    frame_010.bl_label = "Frame"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20
    # Links for frame_010

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (69.0, -75.79999542236328)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001

    distribute_points_on_faces_001 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_001.name = "Distribute Points on Faces.001"
    distribute_points_on_faces_001.label = ""
    distribute_points_on_faces_001.location = (449.0, -35.79999542236328)
    distribute_points_on_faces_001.bl_label = "Distribute Points on Faces"
    distribute_points_on_faces_001.distribute_method = "POISSON"
    distribute_points_on_faces_001.use_legacy_normal = False
    # Distance Min
    distribute_points_on_faces_001.inputs[2].default_value = 0.009999999776482582
    # Density Max
    distribute_points_on_faces_001.inputs[3].default_value = 5000.0
    # Density
    distribute_points_on_faces_001.inputs[4].default_value = 500.0
    # Density Factor
    distribute_points_on_faces_001.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces_001.inputs[6].default_value = 0
    # Links for distribute_points_on_faces_001
    links.new(reroute_001.outputs[0], distribute_points_on_faces_001.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (89.0, -195.79998779296875)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "POINTS"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity
    links.new(for_each_geometry_element_output_001.outputs[2], geometry_proximity.inputs[0])

    compare_006 = nodes.new("FunctionNodeCompare")
    compare_006.name = "Compare.006"
    compare_006.label = ""
    compare_006.location = (289.0, -195.79998779296875)
    compare_006.bl_label = "Compare"
    compare_006.operation = "LESS_THAN"
    compare_006.data_type = "FLOAT"
    compare_006.mode = "ELEMENT"
    # B
    compare_006.inputs[1].default_value = 0.006000000052154064
    # A
    compare_006.inputs[2].default_value = 0
    # B
    compare_006.inputs[3].default_value = 0
    # A
    compare_006.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_006.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_006.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_006.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_006.inputs[8].default_value = ""
    # B
    compare_006.inputs[9].default_value = ""
    # C
    compare_006.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_006.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_006.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_006
    links.new(geometry_proximity.outputs[1], compare_006.inputs[0])
    links.new(compare_006.outputs[0], distribute_points_on_faces_001.inputs[1])

    gem_in_holder_2 = nodes.new("GeometryNodeGroup")
    gem_in_holder_2.name = "Gem in Holder.002"
    gem_in_holder_2.label = ""
    gem_in_holder_2.location = (29.0, -435.79998779296875)
    gem_in_holder_2.node_tree = create_gem_in__holder_group()
    gem_in_holder_2.bl_label = "Group"
    # Gem Radius
    gem_in_holder_2.inputs[0].default_value = 0.009999990463256836
    # Gem Material
    gem_in_holder_2.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_2.inputs[2].default_value = False
    # Scale
    gem_in_holder_2.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_2.inputs[4].default_value = 20
    # Seed
    gem_in_holder_2.inputs[5].default_value = 10
    # Wings
    gem_in_holder_2.inputs[6].default_value = False
    # Array Count
    gem_in_holder_2.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_2.inputs[8].default_value = 10
    # Split
    gem_in_holder_2.inputs[9].default_value = 0.0010000000474974513
    # Seed
    gem_in_holder_2.inputs[10].default_value = 6.6099958419799805
    # Links for gem_in_holder_2

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.label = ""
    instance_on_points_001.location = (709.0, -75.79999542236328)
    instance_on_points_001.bl_label = "Instance on Points"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Links for instance_on_points_001
    links.new(distribute_points_on_faces_001.outputs[0], instance_on_points_001.inputs[0])
    links.new(distribute_points_on_faces_001.outputs[2], instance_on_points_001.inputs[5])

    random_value_010 = nodes.new("FunctionNodeRandomValue")
    random_value_010.name = "Random Value.010"
    random_value_010.label = ""
    random_value_010.location = (469.0, -415.79998779296875)
    random_value_010.bl_label = "Random Value"
    random_value_010.data_type = "FLOAT"
    # Min
    random_value_010.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_010.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_010.inputs[2].default_value = 0.20000000298023224
    # Max
    random_value_010.inputs[3].default_value = 0.5
    # Min
    random_value_010.inputs[4].default_value = 0
    # Max
    random_value_010.inputs[5].default_value = 100
    # Probability
    random_value_010.inputs[6].default_value = 0.5
    # ID
    random_value_010.inputs[7].default_value = 0
    # Seed
    random_value_010.inputs[8].default_value = 0
    # Links for random_value_010
    links.new(random_value_010.outputs[1], instance_on_points_001.inputs[6])

    frame_011 = nodes.new("NodeFrame")
    frame_011.name = "Frame.011"
    frame_011.label = "Larger Jewels"
    frame_011.location = (2669.0, -2649.0)
    frame_011.bl_label = "Frame"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20
    # Links for frame_011

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.label = ""
    realize_instances_001.location = (1049.0, -75.79999542236328)
    realize_instances_001.bl_label = "Realize Instances"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0
    # Links for realize_instances_001

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.label = ""
    transform_geometry_005.location = (269.0, -435.79998779296875)
    transform_geometry_005.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_005.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    # Rotation
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_005
    links.new(transform_geometry_005.outputs[0], instance_on_points_001.inputs[2])
    links.new(gem_in_holder_2.outputs[0], transform_geometry_005.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.name = "Group.005"
    swap_attr.label = ""
    swap_attr.location = (1209.0, -75.79999542236328)
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.bl_label = "Group"
    # Old
    swap_attr.inputs[2].default_value = "ruby"
    # New
    swap_attr.inputs[3].default_value = "saphire"
    # Links for swap_attr
    links.new(swap_attr.outputs[0], join_geometry_006.inputs[0])
    links.new(realize_instances_001.outputs[0], swap_attr.inputs[0])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (889.0, -75.79999542236328)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "INSTANCE"
    # Links for capture_attribute_001
    links.new(capture_attribute_001.outputs[0], realize_instances_001.inputs[0])
    links.new(instance_on_points_001.outputs[0], capture_attribute_001.inputs[0])
    links.new(capture_attribute_001.outputs[1], swap_attr.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (849.0, -195.79998779296875)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], capture_attribute_001.inputs[1])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1649.0, -75.13334655761719)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001
    links.new(transform_geometry_004.outputs[0], set_position_001.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (1498.0, -2964.800048828125)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], reroute_001.inputs[0])
    links.new(separate_geometry_001.outputs[1], reroute_002.inputs[0])

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.label = ""
    geometry_proximity_001.location = (1469.0, -295.13336181640625)
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
    links.new(geometry_proximity_001.outputs[0], set_position_001.inputs[2])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (1809.0, -75.13334655761719)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False
    # Links for curve_to_mesh_001
    links.new(set_position_001.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(gem_in_holder_1.outputs[1], curve_to_mesh_001.inputs[1])
    links.new(gem_in_holder_1.outputs[2], curve_to_mesh_001.inputs[2])

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (1989.0, -75.13334655761719)
    store_named_attribute_004.bl_label = "Store Named Attribute"
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_004.inputs[3].default_value = True
    # Links for store_named_attribute_004
    links.new(store_named_attribute_004.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(curve_to_mesh_001.outputs[0], store_named_attribute_004.inputs[0])

    auto_layout_nodes(group)
    return group
