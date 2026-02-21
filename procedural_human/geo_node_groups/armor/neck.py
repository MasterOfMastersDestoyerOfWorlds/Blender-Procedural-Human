import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group
from procedural_human.geo_node_groups.utilities.join_splines import create_join__splines_group

@geo_node_group
def create_neck_group():
    group_name = "Neck"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Mesh", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Decor", in_out="INPUT", socket_type="NodeSocketBool")
    socket.default_value = False

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (12680.001953125, 400.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    quadratic_bézier_003 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_003.name = "Quadratic Bézier.003"
    quadratic_bézier_003.label = ""
    quadratic_bézier_003.location = (29.0, -35.79998779296875)
    quadratic_bézier_003.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_003.inputs[0].default_value = 40
    # Start
    quadratic_bézier_003.inputs[1].default_value = Vector((0.0, -0.13999998569488525, 0.3499999940395355))
    # Middle
    quadratic_bézier_003.inputs[2].default_value = Vector((0.0, -0.10000000149011612, 0.39500001072883606))
    # Links for quadratic_bézier_003

    bi_rail_loft = nodes.new("GeometryNodeGroup")
    bi_rail_loft.name = "Bi-Rail Loft.001"
    bi_rail_loft.label = ""
    bi_rail_loft.location = (1387.0, -631.5999145507812)
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
    bi_rail_loft.inputs[7].default_value = 42
    # Y Resolution
    bi_rail_loft.inputs[8].default_value = 148
    # Links for bi_rail_loft

    quadratic_bézier_004 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_004.name = "Quadratic Bézier.004"
    quadratic_bézier_004.label = ""
    quadratic_bézier_004.location = (189.0, -155.79998779296875)
    quadratic_bézier_004.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_004.inputs[0].default_value = 40
    # Middle
    quadratic_bézier_004.inputs[2].default_value = Vector((0.0, -0.07999999821186066, 0.4399999976158142))
    # End
    quadratic_bézier_004.inputs[3].default_value = Vector((0.0, -0.08999999612569809, 0.45000001788139343))
    # Links for quadratic_bézier_004

    join_splines = nodes.new("GeometryNodeGroup")
    join_splines.name = "Group.002"
    join_splines.label = ""
    join_splines.location = (369.0, -95.79998779296875)
    join_splines.node_tree = create_join__splines_group()
    join_splines.bl_label = "Group"
    # Links for join_splines

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (369.0, -35.79998779296875)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(quadratic_bézier_003.outputs[0], join_geometry_005.inputs[0])
    links.new(quadratic_bézier_004.outputs[0], join_geometry_005.inputs[0])
    links.new(join_geometry_005.outputs[0], join_splines.inputs[0])

    vector = nodes.new("FunctionNodeInputVector")
    vector.name = "Vector"
    vector.label = ""
    vector.location = (29.0, -295.79998779296875)
    vector.bl_label = "Vector"
    vector.vector = Vector((0.0, -0.08999999612569809, 0.42000001668930054))
    # Links for vector
    links.new(vector.outputs[0], quadratic_bézier_003.inputs[3])
    links.new(vector.outputs[0], quadratic_bézier_004.inputs[1])

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = "Centre Profile"
    frame_006.location = (29.0, -495.8000183105469)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    quadratic_bézier_006 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_006.name = "Quadratic Bézier.006"
    quadratic_bézier_006.label = ""
    quadratic_bézier_006.location = (29.0, -35.80000305175781)
    quadratic_bézier_006.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_006.inputs[0].default_value = 40
    # Start
    quadratic_bézier_006.inputs[1].default_value = Vector((-0.15000000596046448, 0.0, 0.429999977350235))
    # Middle
    quadratic_bézier_006.inputs[2].default_value = Vector((-0.10000000894069672, 0.0, 0.44999998807907104))
    # Links for quadratic_bézier_006

    quadratic_bézier_007 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_007.name = "Quadratic Bézier.007"
    quadratic_bézier_007.label = ""
    quadratic_bézier_007.location = (189.0, -155.8000030517578)
    quadratic_bézier_007.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_007.inputs[0].default_value = 40
    # Middle
    quadratic_bézier_007.inputs[2].default_value = Vector((-0.0650000050663948, 0.0, 0.4899999797344208))
    # End
    quadratic_bézier_007.inputs[3].default_value = Vector((-0.07500000298023224, 0.0, 0.5))
    # Links for quadratic_bézier_007

    join_splines_1 = nodes.new("GeometryNodeGroup")
    join_splines_1.name = "Group.003"
    join_splines_1.label = ""
    join_splines_1.location = (369.0, -95.80000305175781)
    join_splines_1.node_tree = create_join__splines_group()
    join_splines_1.bl_label = "Group"
    # Links for join_splines_1

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.label = ""
    join_geometry_006.location = (369.0, -35.80000305175781)
    join_geometry_006.bl_label = "Join Geometry"
    # Links for join_geometry_006
    links.new(join_geometry_006.outputs[0], join_splines_1.inputs[0])
    links.new(quadratic_bézier_006.outputs[0], join_geometry_006.inputs[0])
    links.new(quadratic_bézier_007.outputs[0], join_geometry_006.inputs[0])

    vector_001 = nodes.new("FunctionNodeInputVector")
    vector_001.name = "Vector.001"
    vector_001.label = ""
    vector_001.location = (29.0, -295.79998779296875)
    vector_001.bl_label = "Vector"
    vector_001.vector = Vector((-0.08500001579523087, 0.0, 0.4699999988079071))
    # Links for vector_001
    links.new(vector_001.outputs[0], quadratic_bézier_006.inputs[3])
    links.new(vector_001.outputs[0], quadratic_bézier_007.inputs[1])

    frame_007 = nodes.new("NodeFrame")
    frame_007.name = "Frame.007"
    frame_007.label = "Side Profile"
    frame_007.location = (29.0, -35.80000305175781)
    frame_007.bl_label = "Frame"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20
    # Links for frame_007

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_008.name = "Join Geometry.008"
    join_geometry_008.label = ""
    join_geometry_008.location = (778.0, -391.6000061035156)
    join_geometry_008.bl_label = "Join Geometry"
    # Links for join_geometry_008
    links.new(join_geometry_008.outputs[0], bi_rail_loft.inputs[2])

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    transform_geometry_002.label = ""
    transform_geometry_002.location = (549.0, -35.79998779296875)
    transform_geometry_002.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_002.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_002.inputs[2].default_value = Vector((0.0, -0.019999999552965164, 0.4800000488758087))
    # Rotation
    transform_geometry_002.inputs[3].default_value = Euler((0.4064871668815613, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_002
    links.new(transform_geometry_002.outputs[0], bi_rail_loft.inputs[1])

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    transform_geometry_003.label = ""
    transform_geometry_003.location = (549.0, -355.79998779296875)
    transform_geometry_003.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_003.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.3700000047683716))
    # Rotation
    transform_geometry_003.inputs[3].default_value = Euler((0.15620698034763336, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_003.inputs[4].default_value = Vector((1.2599999904632568, 1.0, 1.0))
    # Links for transform_geometry_003

    curve_circle = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.label = ""
    curve_circle.location = (189.0, -35.79998779296875)
    curve_circle.bl_label = "Curve Circle"
    curve_circle.mode = "RADIUS"
    # Point 1
    curve_circle.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle.inputs[4].default_value = 0.08000004291534424
    # Links for curve_circle

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.name = "Curve Circle.001"
    curve_circle_001.label = ""
    curve_circle_001.location = (189.0, -355.79998779296875)
    curve_circle_001.bl_label = "Curve Circle"
    curve_circle_001.mode = "RADIUS"
    # Point 1
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_001.inputs[4].default_value = 0.12999996542930603
    # Links for curve_circle_001

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (829.0, -395.79998779296875)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Position
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position
    links.new(transform_geometry_003.outputs[0], set_position.inputs[0])
    links.new(set_position.outputs[0], bi_rail_loft.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (29.0, -715.7999877929688)
    position.bl_label = "Position"
    # Links for position

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (29.0, -775.7999877929688)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(position.outputs[0], separate_x_y_z.inputs[0])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (189.0, -715.7999877929688)
    map_range.bl_label = "Map Range"
    map_range.clamp = False
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    # From Min
    map_range.inputs[1].default_value = -0.14000000059604645
    # From Max
    map_range.inputs[2].default_value = 0.14000000059604645
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0
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
    links.new(separate_x_y_z.outputs[1], map_range.inputs[0])

    frame_008 = nodes.new("NodeFrame")
    frame_008.name = "Frame.008"
    frame_008.label = "Profiles"
    frame_008.location = (29.0, -1119.9998779296875)
    frame_008.bl_label = "Frame"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20
    # Links for frame_008

    float_curve_001 = nodes.new("ShaderNodeFloatCurve")
    float_curve_001.name = "Float Curve.001"
    float_curve_001.label = ""
    float_curve_001.location = (349.0, -715.7999877929688)
    float_curve_001.bl_label = "Float Curve"
    # Factor
    float_curve_001.inputs[0].default_value = 1.0
    # Links for float_curve_001
    links.new(map_range.outputs[0], float_curve_001.inputs[1])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (649.0, -715.7999877929688)
    combine_x_y_z.bl_label = "Combine XYZ"
    # X
    combine_x_y_z.inputs[0].default_value = 0.0
    # Y
    combine_x_y_z.inputs[1].default_value = 0.0
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], set_position.inputs[3])
    links.new(float_curve_001.outputs[0], combine_x_y_z.inputs[2])

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    transform_geometry_004.label = ""
    transform_geometry_004.location = (369.0, -355.79998779296875)
    transform_geometry_004.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_004.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    # Scale
    transform_geometry_004.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_004
    links.new(curve_circle_001.outputs[0], transform_geometry_004.inputs[0])
    links.new(transform_geometry_004.outputs[0], transform_geometry_003.inputs[0])

    transform_geometry_005 = nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.label = ""
    transform_geometry_005.location = (369.0, -35.79998779296875)
    transform_geometry_005.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_005.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_005.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_005.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    # Scale
    transform_geometry_005.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_005
    links.new(transform_geometry_005.outputs[0], transform_geometry_002.inputs[0])
    links.new(curve_circle.outputs[0], transform_geometry_005.inputs[0])

    closure_input_001 = nodes.new("NodeClosureInput")
    closure_input_001.name = "Closure Input.001"
    closure_input_001.label = ""
    closure_input_001.location = (1167.0, -1051.599853515625)
    closure_input_001.bl_label = "Closure Input"
    # Links for closure_input_001

    closure_output_001 = nodes.new("NodeClosureOutput")
    closure_output_001.name = "Closure Output.001"
    closure_output_001.label = ""
    closure_output_001.location = (1647.0, -1051.599853515625)
    closure_output_001.bl_label = "Closure Output"
    closure_output_001.active_input_index = 0
    closure_output_001.active_output_index = 0
    closure_output_001.define_signature = False
    # Links for closure_output_001
    links.new(closure_output_001.outputs[0], bi_rail_loft.inputs[9])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (1327.0, -1051.599853515625)
    math.bl_label = "Math"
    math.operation = "PINGPONG"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.25
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(closure_input_001.outputs[0], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (1487.0, -1051.599853515625)
    math_001.bl_label = "Math"
    math_001.operation = "MULTIPLY"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 4.0
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math_001.outputs[0], closure_output_001.inputs[0])
    links.new(math.outputs[0], math_001.inputs[0])

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (529.0, -75.80000305175781)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_001.inputs[3].default_value = Euler((1.5446162223815918, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_001
    links.new(transform_geometry_001.outputs[0], join_geometry_008.inputs[0])
    links.new(join_splines_1.outputs[0], transform_geometry_001.inputs[0])

    transform_geometry_006 = nodes.new("GeometryNodeTransform")
    transform_geometry_006.name = "Transform Geometry.006"
    transform_geometry_006.label = ""
    transform_geometry_006.location = (529.0, -95.79998779296875)
    transform_geometry_006.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_006.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_006.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_006.inputs[3].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')
    # Scale
    transform_geometry_006.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_006
    links.new(transform_geometry_006.outputs[0], join_geometry_008.inputs[0])
    links.new(join_splines.outputs[0], transform_geometry_006.inputs[0])

    integer = nodes.new("FunctionNodeInputInt")
    integer.name = "Integer"
    integer.label = ""
    integer.location = (189.0, -215.79998779296875)
    integer.bl_label = "Integer"
    integer.integer = 73
    # Links for integer
    links.new(integer.outputs[0], curve_circle_001.inputs[0])
    links.new(integer.outputs[0], curve_circle.inputs[0])

    frame_009 = nodes.new("NodeFrame")
    frame_009.name = "Frame.009"
    frame_009.label = "Neck Rails"
    frame_009.location = (38.0, -35.7999267578125)
    frame_009.bl_label = "Frame"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20
    # Links for frame_009

    frame_010 = nodes.new("NodeFrame")
    frame_010.name = "Frame.010"
    frame_010.label = "Neck"
    frame_010.location = (-1287.0, 951.5999145507812)
    frame_010.bl_label = "Frame"
    frame_010.text = None
    frame_010.shrink = True
    frame_010.label_size = 20
    # Links for frame_010

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (2840.0, -300.0)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "FACE"
    # Links for delete_geometry

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (2680.0, -460.0)
    position_001.bl_label = "Position"
    # Links for position_001

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (2680.0, -520.0)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001
    links.new(position_001.outputs[0], separate_x_y_z_001.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (2840.0, -460.0)
    compare.bl_label = "Compare"
    compare.operation = "GREATER_EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.0
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
    links.new(separate_x_y_z_001.outputs[0], compare.inputs[0])
    links.new(compare.outputs[0], delete_geometry.inputs[1])

    pipes = nodes.new("GeometryNodeGroup")
    pipes.name = "Pipes"
    pipes.label = ""
    pipes.location = (749.0, -95.80000305175781)
    pipes.node_tree = create_pipes_group()
    pipes.bl_label = "Group"
    # Links for pipes

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (2480.0, -320.0)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(join_geometry.outputs[0], delete_geometry.inputs[0])
    links.new(bi_rail_loft.outputs[0], join_geometry.inputs[0])
    links.new(pipes.outputs[0], join_geometry.inputs[0])

    separate_x_y_z_002 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_002.name = "Separate XYZ.002"
    separate_x_y_z_002.label = ""
    separate_x_y_z_002.location = (29.0, -35.80000305175781)
    separate_x_y_z_002.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_002
    links.new(bi_rail_loft.outputs[2], separate_x_y_z_002.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (189.0, -35.80000305175781)
    compare_001.bl_label = "Compare"
    compare_001.operation = "EQUAL"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = 0.8799999356269836
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
    compare_001.inputs[12].default_value = 0.02099999599158764
    # Links for compare_001
    links.new(separate_x_y_z_002.outputs[0], compare_001.inputs[0])

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (349.0, -35.80000305175781)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "POINT"
    # Links for separate_geometry
    links.new(bi_rail_loft.outputs[0], separate_geometry.inputs[0])
    links.new(compare_001.outputs[0], separate_geometry.inputs[1])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (549.0, -75.80000305175781)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(join_geometry_001.outputs[0], pipes.inputs[0])
    links.new(bi_rail_loft.outputs[0], join_geometry_001.inputs[0])
    links.new(separate_geometry.outputs[0], join_geometry_001.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Pipes"
    frame.location = (1351.0, -24.19999885559082)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    rivet = nodes.new("GeometryNodeGroup")
    rivet.name = "Rivet"
    rivet.label = ""
    rivet.location = (1520.0, -520.0)
    rivet.node_tree = create_rivet_group()
    rivet.bl_label = "Group"
    # Corners
    rivet.inputs[1].default_value = False
    # Offset
    rivet.inputs[2].default_value = -1.059999942779541
    # Spacing
    rivet.inputs[3].default_value = 0.9399999976158142
    # Links for rivet
    links.new(bi_rail_loft.outputs[0], rivet.inputs[0])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (1700.0, -520.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(realize_instances.outputs[0], join_geometry.inputs[0])
    links.new(rivet.outputs[0], realize_instances.inputs[0])

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (3080.0, -300.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True
    # Links for set_shade_smooth
    links.new(delete_geometry.outputs[0], set_shade_smooth.inputs[0])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (6677.9990234375, -3251.60009765625)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (6837.9990234375, -3251.60009765625)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(join_geometry_002.outputs[0], switch.inputs[2])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (6638.0, -3191.60009765625)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch.inputs[0])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    set_spline_cyclic.label = ""
    set_spline_cyclic.location = (458.0, -2031.60009765625)
    set_spline_cyclic.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = False
    # Links for set_spline_cyclic
    links.new(set_position.outputs[0], set_spline_cyclic.inputs[0])

    trim_curve = nodes.new("GeometryNodeTrimCurve")
    trim_curve.name = "Trim Curve"
    trim_curve.label = ""
    trim_curve.location = (29.0, -29.0)
    trim_curve.bl_label = "Trim Curve"
    trim_curve.mode = "FACTOR"
    # Selection
    trim_curve.inputs[1].default_value = True
    # Start
    trim_curve.inputs[2].default_value = 0.0
    # End
    trim_curve.inputs[3].default_value = 0.5074577331542969
    # Start
    trim_curve.inputs[4].default_value = 0.0
    # End
    trim_curve.inputs[5].default_value = 1.0
    # Links for trim_curve
    links.new(set_spline_cyclic.outputs[0], trim_curve.inputs[0])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (189.0, -29.0)
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
    links.new(trim_curve.outputs[0], resample_curve_001.inputs[0])

    gold_decorations = nodes.new("GeometryNodeGroup")
    gold_decorations.name = "Group.006"
    gold_decorations.label = ""
    gold_decorations.location = (529.0, -29.0)
    gold_decorations.node_tree = create_gold__decorations_group()
    gold_decorations.bl_label = "Group"
    # Seed
    gold_decorations.inputs[1].default_value = 68
    # Scale
    gold_decorations.inputs[2].default_value = 2.6999993324279785
    # Count
    gold_decorations.inputs[3].default_value = 56
    # Links for gold_decorations
    links.new(gold_decorations.outputs[0], join_geometry_002.inputs[0])

    set_curve_normal = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal.name = "Set Curve Normal"
    set_curve_normal.label = ""
    set_curve_normal.location = (349.0, -29.0)
    set_curve_normal.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal.inputs[1].default_value = True
    # Mode
    set_curve_normal.inputs[2].default_value = "Free"
    # Links for set_curve_normal
    links.new(set_curve_normal.outputs[0], gold_decorations.inputs[0])
    links.new(resample_curve_001.outputs[0], set_curve_normal.inputs[0])

    sample_nearest_surface = nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.name = "Sample Nearest Surface"
    sample_nearest_surface.label = ""
    sample_nearest_surface.location = (438.0, -2291.60009765625)
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
    normal.location = (438.0, -2511.60009765625)
    normal.bl_label = "Normal"
    normal.legacy_corner_normals = False
    # Links for normal
    links.new(normal.outputs[0], sample_nearest_surface.inputs[1])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (189.0, -189.0)
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
    curve_tangent.location = (189.0, -329.0)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent
    links.new(curve_tangent.outputs[0], vector_math.inputs[1])

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = ""
    frame_005.location = (1309.0, -1702.60009765625)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    gold_on_band = nodes.new("GeometryNodeGroup")
    gold_on_band.name = "Group.007"
    gold_on_band.label = ""
    gold_on_band.location = (1129.0, -335.800048828125)
    gold_on_band.node_tree = create_gold_on__band_group()
    gold_on_band.bl_label = "Group"
    # Density
    gold_on_band.inputs[1].default_value = 100000.0
    # W
    gold_on_band.inputs[2].default_value = 8.669999122619629
    # Seed
    gold_on_band.inputs[3].default_value = 1
    # Links for gold_on_band

    frame_011 = nodes.new("NodeFrame")
    frame_011.name = "Frame.011"
    frame_011.label = "Gold"
    frame_011.location = (2422.0, 5711.60009765625)
    frame_011.bl_label = "Frame"
    frame_011.text = None
    frame_011.shrink = True
    frame_011.label_size = 20
    # Links for frame_011

    gem_in_holder = nodes.new("GeometryNodeGroup")
    gem_in_holder.name = "Gem in Holder"
    gem_in_holder.label = ""
    gem_in_holder.location = (1249.0, -155.800048828125)
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
    curve_to_points.location = (389.0, -415.800048828125)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "COUNT"
    # Count
    curve_to_points.inputs[1].default_value = 8
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points

    for_each_geometry_element_input = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input.name = "For Each Geometry Element Input"
    for_each_geometry_element_input.label = ""
    for_each_geometry_element_input.location = (549.0, -415.800048828125)
    for_each_geometry_element_input.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input.inputs[1].default_value = True
    # Links for for_each_geometry_element_input
    links.new(curve_to_points.outputs[0], for_each_geometry_element_input.inputs[0])
    links.new(curve_to_points.outputs[3], for_each_geometry_element_input.inputs[2])

    for_each_geometry_element_output = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.name = "For Each Geometry Element Output"
    for_each_geometry_element_output.label = ""
    for_each_geometry_element_output.location = (2069.0, -475.800048828125)
    for_each_geometry_element_output.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output.active_input_index = 1
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = "POINT"
    for_each_geometry_element_output.inspection_index = 0
    # Links for for_each_geometry_element_output
    links.new(for_each_geometry_element_output.outputs[2], join_geometry_002.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (389.0, -615.800048828125)
    position_002.bl_label = "Position"
    # Links for position_002
    links.new(position_002.outputs[0], for_each_geometry_element_input.inputs[3])

    transform_geometry_007 = nodes.new("GeometryNodeTransform")
    transform_geometry_007.name = "Transform Geometry.007"
    transform_geometry_007.label = ""
    transform_geometry_007.location = (1529.0, -475.800048828125)
    transform_geometry_007.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_007.inputs[1].default_value = "Components"
    # Links for transform_geometry_007
    links.new(gem_in_holder.outputs[0], transform_geometry_007.inputs[0])
    links.new(for_each_geometry_element_input.outputs[3], transform_geometry_007.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.name = "Rotate Rotation"
    rotate_rotation.label = ""
    rotate_rotation.location = (1189.0, -675.800048828125)
    rotate_rotation.bl_label = "Rotate Rotation"
    rotate_rotation.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation.inputs[1].default_value = Euler((0.0, 1.5707963705062866, 0.0), 'XYZ')
    # Links for rotate_rotation
    links.new(for_each_geometry_element_input.outputs[2], rotate_rotation.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (789.0, -395.800048828125)
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

    transform_geometry_008 = nodes.new("GeometryNodeTransform")
    transform_geometry_008.name = "Transform Geometry.008"
    transform_geometry_008.label = ""
    transform_geometry_008.location = (1709.0, -475.800048828125)
    transform_geometry_008.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_008.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_008.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    # Rotation
    transform_geometry_008.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_008.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_008
    links.new(transform_geometry_007.outputs[0], transform_geometry_008.inputs[0])
    links.new(transform_geometry_008.outputs[0], for_each_geometry_element_output.inputs[1])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.label = ""
    random_value_001.location = (769.0, -615.800048828125)
    random_value_001.bl_label = "Random Value"
    random_value_001.data_type = "FLOAT"
    # Min
    random_value_001.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_001.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_001.inputs[2].default_value = 0.3499999940395355
    # Max
    random_value_001.inputs[3].default_value = 0.75
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
    links.new(random_value_001.outputs[1], transform_geometry_007.inputs[4])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (2329.0, -95.13330078125)
    store_named_attribute_001.bl_label = "Store Named Attribute"
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_001.inputs[3].default_value = True
    # Links for store_named_attribute_001

    random_value_002 = nodes.new("FunctionNodeRandomValue")
    random_value_002.name = "Random Value.002"
    random_value_002.label = ""
    random_value_002.location = (789.0, -215.800048828125)
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
    random_value_002.inputs[8].default_value = 24
    # Links for random_value_002
    links.new(for_each_geometry_element_input.outputs[0], random_value_002.inputs[7])
    links.new(random_value_002.outputs[1], gem_in_holder.inputs[10])

    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.name = "Rotate Rotation.001"
    rotate_rotation_001.label = ""
    rotate_rotation_001.location = (1349.0, -675.800048828125)
    rotate_rotation_001.bl_label = "Rotate Rotation"
    rotate_rotation_001.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_001.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
    # Links for rotate_rotation_001
    links.new(rotate_rotation_001.outputs[0], transform_geometry_007.inputs[3])
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])

    random_value_003 = nodes.new("FunctionNodeRandomValue")
    random_value_003.name = "Random Value.003"
    random_value_003.label = ""
    random_value_003.location = (789.0, -35.800048828125)
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
    random_value_004.location = (1029.0, -255.800048828125)
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
    random_value_005.location = (1029.0, -75.800048828125)
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
    random_value_006.location = (1029.0, -435.800048828125)
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

    frame_012 = nodes.new("NodeFrame")
    frame_012.name = "Frame.012"
    frame_012.label = "Broaches"
    frame_012.location = (729.0, -2155.800048828125)
    frame_012.bl_label = "Frame"
    frame_012.text = None
    frame_012.shrink = True
    frame_012.label_size = 20
    # Links for frame_012

    separate_geometry_001 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.name = "Separate Geometry.001"
    separate_geometry_001.label = ""
    separate_geometry_001.location = (969.0, -335.800048828125)
    separate_geometry_001.bl_label = "Separate Geometry"
    separate_geometry_001.domain = "FACE"
    # Links for separate_geometry_001
    links.new(bi_rail_loft.outputs[0], separate_geometry_001.inputs[0])
    links.new(separate_geometry_001.outputs[0], gold_on_band.inputs[0])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_003.name = "Separate XYZ.003"
    separate_x_y_z_003.label = ""
    separate_x_y_z_003.location = (29.0, -195.800048828125)
    separate_x_y_z_003.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_003
    links.new(bi_rail_loft.outputs[2], separate_x_y_z_003.inputs[0])

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.label = ""
    compare_002.location = (269.0, -35.800048828125)
    compare_002.bl_label = "Compare"
    compare_002.operation = "GREATER_THAN"
    compare_002.data_type = "FLOAT"
    compare_002.mode = "ELEMENT"
    # B
    compare_002.inputs[1].default_value = 0.8700000047683716
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
    links.new(separate_x_y_z_003.outputs[0], compare_002.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (12340.001953125, 360.0)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(join_geometry_004.outputs[0], group_output.inputs[0])
    links.new(set_shade_smooth.outputs[0], join_geometry_004.inputs[0])
    links.new(switch.outputs[0], join_geometry_004.inputs[0])

    trim_curve_001 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_001.name = "Trim Curve.001"
    trim_curve_001.label = ""
    trim_curve_001.location = (29.0, -415.800048828125)
    trim_curve_001.bl_label = "Trim Curve"
    trim_curve_001.mode = "FACTOR"
    # Selection
    trim_curve_001.inputs[1].default_value = True
    # Start
    trim_curve_001.inputs[2].default_value = 0.18784530460834503
    # End
    trim_curve_001.inputs[3].default_value = 0.46817636489868164
    # Start
    trim_curve_001.inputs[4].default_value = 0.0
    # End
    trim_curve_001.inputs[5].default_value = 1.0
    # Links for trim_curve_001
    links.new(set_spline_cyclic.outputs[0], trim_curve_001.inputs[0])

    set_curve_normal_001 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.name = "Set Curve Normal.001"
    set_curve_normal_001.label = ""
    set_curve_normal_001.location = (209.0, -395.800048828125)
    set_curve_normal_001.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_001.inputs[1].default_value = True
    # Mode
    set_curve_normal_001.inputs[2].default_value = "Free"
    # Links for set_curve_normal_001
    links.new(set_curve_normal_001.outputs[0], curve_to_points.inputs[0])
    links.new(trim_curve_001.outputs[0], set_curve_normal_001.inputs[0])
    links.new(sample_nearest_surface.outputs[0], set_curve_normal_001.inputs[3])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (269.0, -195.800048828125)
    compare_003.bl_label = "Compare"
    compare_003.operation = "LESS_THAN"
    compare_003.data_type = "FLOAT"
    compare_003.mode = "ELEMENT"
    # B
    compare_003.inputs[1].default_value = 0.25999999046325684
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

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (429.0, -55.800048828125)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "OR"
    # Links for boolean_math
    links.new(compare_002.outputs[0], boolean_math.inputs[0])
    links.new(compare_003.outputs[0], boolean_math.inputs[1])

    boolean_math_001 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.label = ""
    boolean_math_001.location = (609.0, -215.800048828125)
    boolean_math_001.bl_label = "Boolean Math"
    boolean_math_001.operation = "OR"
    # Links for boolean_math_001
    links.new(boolean_math.outputs[0], boolean_math_001.inputs[0])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (269.0, -355.800048828125)
    compare_004.bl_label = "Compare"
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    # B
    compare_004.inputs[1].default_value = 0.5
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
    compare_004.inputs[12].default_value = 0.020999997854232788
    # Links for compare_004
    links.new(separate_x_y_z_003.outputs[1], compare_004.inputs[0])
    links.new(compare_004.outputs[0], boolean_math_001.inputs[1])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "On Band"
    frame_001.location = (29.0, -3255.800048828125)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    boolean_math_002 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.label = ""
    boolean_math_002.location = (789.0, -255.800048828125)
    boolean_math_002.bl_label = "Boolean Math"
    boolean_math_002.operation = "AND"
    # Links for boolean_math_002
    links.new(boolean_math_002.outputs[0], separate_geometry_001.inputs[1])
    links.new(boolean_math_001.outputs[0], boolean_math_002.inputs[0])

    compare_005 = nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.label = ""
    compare_005.location = (269.0, -535.800048828125)
    compare_005.bl_label = "Compare"
    compare_005.operation = "LESS_THAN"
    compare_005.data_type = "FLOAT"
    compare_005.mode = "ELEMENT"
    # B
    compare_005.inputs[1].default_value = 0.5
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
    compare_005.inputs[12].default_value = 0.020999997854232788
    # Links for compare_005
    links.new(separate_x_y_z_003.outputs[1], compare_005.inputs[0])
    links.new(compare_005.outputs[0], boolean_math_002.inputs[1])

    gem_in_holder_1 = nodes.new("GeometryNodeGroup")
    gem_in_holder_1.name = "Gem in Holder.001"
    gem_in_holder_1.label = ""
    gem_in_holder_1.location = (1349.0, -75.13330078125)
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
    mesh_to_curve_002.location = (29.0, -55.13330078125)
    mesh_to_curve_002.bl_label = "Mesh to Curve"
    mesh_to_curve_002.mode = "EDGES"
    # Links for mesh_to_curve_002
    links.new(separate_geometry_001.outputs[0], mesh_to_curve_002.inputs[0])

    is_edge_boundary = nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Is Edge Boundary"
    is_edge_boundary.label = ""
    is_edge_boundary.location = (29.0, -175.13330078125)
    is_edge_boundary.node_tree = create_is__edge__boundary_group()
    is_edge_boundary.bl_label = "Group"
    # Links for is_edge_boundary
    links.new(is_edge_boundary.outputs[0], mesh_to_curve_002.inputs[1])

    set_spline_cyclic_001 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_001.name = "Set Spline Cyclic.001"
    set_spline_cyclic_001.label = ""
    set_spline_cyclic_001.location = (349.0, -55.13330078125)
    set_spline_cyclic_001.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic_001.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic_001.inputs[2].default_value = False
    # Links for set_spline_cyclic_001

    trim_curve_004 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_004.name = "Trim Curve.004"
    trim_curve_004.label = ""
    trim_curve_004.location = (509.0, -55.13330078125)
    trim_curve_004.bl_label = "Trim Curve"
    trim_curve_004.mode = "FACTOR"
    # Selection
    trim_curve_004.inputs[1].default_value = True
    # Start
    trim_curve_004.inputs[2].default_value = 0.03867403417825699
    # End
    trim_curve_004.inputs[3].default_value = 0.4364641308784485
    # Start
    trim_curve_004.inputs[4].default_value = 0.0
    # End
    trim_curve_004.inputs[5].default_value = 1.0
    # Links for trim_curve_004
    links.new(set_spline_cyclic_001.outputs[0], trim_curve_004.inputs[0])

    curve_to_points_001 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.name = "Curve to Points.001"
    curve_to_points_001.label = ""
    curve_to_points_001.location = (669.0, -55.13330078125)
    curve_to_points_001.bl_label = "Curve to Points"
    curve_to_points_001.mode = "COUNT"
    # Count
    curve_to_points_001.inputs[1].default_value = 50
    # Length
    curve_to_points_001.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points_001
    links.new(trim_curve_004.outputs[0], curve_to_points_001.inputs[0])

    set_curve_normal_002 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_002.name = "Set Curve Normal.002"
    set_curve_normal_002.label = ""
    set_curve_normal_002.location = (189.0, -55.13330078125)
    set_curve_normal_002.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_002.inputs[1].default_value = True
    # Mode
    set_curve_normal_002.inputs[2].default_value = "Free"
    # Links for set_curve_normal_002
    links.new(set_curve_normal_002.outputs[0], set_spline_cyclic_001.inputs[0])
    links.new(mesh_to_curve_002.outputs[0], set_curve_normal_002.inputs[0])
    links.new(sample_nearest_surface.outputs[0], set_curve_normal_002.inputs[3])

    position_004 = nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"
    position_004.label = ""
    position_004.location = (669.0, -255.13330078125)
    position_004.bl_label = "Position"
    # Links for position_004

    for_each_geometry_element_input_001 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.name = "For Each Geometry Element Input.001"
    for_each_geometry_element_input_001.label = ""
    for_each_geometry_element_input_001.location = (829.0, -55.13330078125)
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
    for_each_geometry_element_output_001.location = (2509.0, -75.13330078125)
    for_each_geometry_element_output_001.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = "POINT"
    for_each_geometry_element_output_001.inspection_index = 0
    # Links for for_each_geometry_element_output_001
    links.new(store_named_attribute_001.outputs[0], for_each_geometry_element_output_001.inputs[1])
    links.new(for_each_geometry_element_output_001.outputs[2], join_geometry_002.inputs[0])

    transform_geometry_009 = nodes.new("GeometryNodeTransform")
    transform_geometry_009.name = "Transform Geometry.009"
    transform_geometry_009.label = ""
    transform_geometry_009.location = (1609.0, -75.13330078125)
    transform_geometry_009.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_009.inputs[1].default_value = "Components"
    # Scale
    transform_geometry_009.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_009
    links.new(for_each_geometry_element_input_001.outputs[2], transform_geometry_009.inputs[2])
    links.new(gem_in_holder_1.outputs[4], transform_geometry_009.inputs[0])

    rotate_rotation_002 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.name = "Rotate Rotation.002"
    rotate_rotation_002.label = ""
    rotate_rotation_002.location = (1009.0, -295.13330078125)
    rotate_rotation_002.bl_label = "Rotate Rotation"
    rotate_rotation_002.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_002.inputs[1].default_value = Euler((0.0, -1.5707963705062866, 0.0), 'XYZ')
    # Links for rotate_rotation_002
    links.new(rotate_rotation_002.outputs[0], transform_geometry_009.inputs[3])
    links.new(for_each_geometry_element_input_001.outputs[3], rotate_rotation_002.inputs[0])

    frame_014 = nodes.new("NodeFrame")
    frame_014.name = "Frame.014"
    frame_014.label = "Random Wings"
    frame_014.location = (1449.0, -3056.466796875)
    frame_014.bl_label = "Frame"
    frame_014.text = None
    frame_014.shrink = True
    frame_014.label_size = 20
    # Links for frame_014

    random_value_007 = nodes.new("FunctionNodeRandomValue")
    random_value_007.name = "Random Value.007"
    random_value_007.label = ""
    random_value_007.location = (1169.0, -55.13330078125)
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
    random_value_007.inputs[8].default_value = 33
    # Links for random_value_007
    links.new(for_each_geometry_element_input_001.outputs[0], random_value_007.inputs[7])
    links.new(random_value_007.outputs[1], gem_in_holder_1.inputs[10])

    random_value_008 = nodes.new("FunctionNodeRandomValue")
    random_value_008.name = "Random Value.008"
    random_value_008.label = ""
    random_value_008.location = (1169.0, -235.13330078125)
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

    distribute_points_on_faces = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.name = "Distribute Points on Faces"
    distribute_points_on_faces.label = ""
    distribute_points_on_faces.location = (209.0, -35.7999267578125)
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
    distribute_points_on_faces.inputs[6].default_value = 1
    # Links for distribute_points_on_faces
    links.new(separate_geometry_001.outputs[0], distribute_points_on_faces.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (509.0, -55.7999267578125)
    instance_on_points.bl_label = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Rotation
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Links for instance_on_points
    links.new(distribute_points_on_faces.outputs[0], instance_on_points.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    ico_sphere.label = ""
    ico_sphere.location = (29.0, -255.7999267578125)
    ico_sphere.bl_label = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.004000000189989805
    # Subdivisions
    ico_sphere.inputs[1].default_value = 2
    # Links for ico_sphere

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (689.0, -55.7999267578125)
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
    random_value_009.location = (689.0, -215.7999267578125)
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

    boolean_math_003 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.label = ""
    boolean_math_003.location = (869.0, -215.7999267578125)
    boolean_math_003.bl_label = "Boolean Math"
    boolean_math_003.operation = "NOT"
    # Boolean
    boolean_math_003.inputs[1].default_value = False
    # Links for boolean_math_003
    links.new(random_value_009.outputs[3], boolean_math_003.inputs[0])

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (869.0, -55.7999267578125)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "INSTANCE"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "saphire"
    # Links for store_named_attribute_003
    links.new(store_named_attribute_002.outputs[0], store_named_attribute_003.inputs[0])
    links.new(boolean_math_003.outputs[0], store_named_attribute_003.inputs[3])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.label = ""
    realize_instances_001.location = (1029.0, -55.7999267578125)
    realize_instances_001.bl_label = "Realize Instances"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0
    # Links for realize_instances_001
    links.new(store_named_attribute_003.outputs[0], realize_instances_001.inputs[0])
    links.new(realize_instances_001.outputs[0], join_geometry_002.inputs[0])

    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.name = "Set Shade Smooth.003"
    set_shade_smooth_003.label = ""
    set_shade_smooth_003.location = (209.0, -255.7999267578125)
    set_shade_smooth_003.bl_label = "Set Shade Smooth"
    set_shade_smooth_003.domain = "FACE"
    # Selection
    set_shade_smooth_003.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_003.inputs[2].default_value = True
    # Links for set_shade_smooth_003
    links.new(set_shade_smooth_003.outputs[0], instance_on_points.inputs[2])
    links.new(ico_sphere.outputs[0], set_shade_smooth_003.inputs[0])

    frame_015 = nodes.new("NodeFrame")
    frame_015.name = "Frame.015"
    frame_015.label = "Random Jewels"
    frame_015.location = (2169.0, -3975.80029296875)
    frame_015.bl_label = "Frame"
    frame_015.text = None
    frame_015.shrink = True
    frame_015.label_size = 20
    # Links for frame_015

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (209.0, -75.7999267578125)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001
    links.new(bi_rail_loft.outputs[0], reroute_001.inputs[0])

    distribute_points_on_faces_001 = nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_001.name = "Distribute Points on Faces.001"
    distribute_points_on_faces_001.label = ""
    distribute_points_on_faces_001.location = (409.0, -35.7999267578125)
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
    geometry_proximity.location = (29.0, -195.7999267578125)
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
    compare_006.location = (249.0, -195.7999267578125)
    compare_006.bl_label = "Compare"
    compare_006.operation = "LESS_THAN"
    compare_006.data_type = "FLOAT"
    compare_006.mode = "ELEMENT"
    # B
    compare_006.inputs[1].default_value = 0.0010000000474974513
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
    gem_in_holder_2.location = (29.0, -415.7999267578125)
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
    instance_on_points_001.location = (669.0, -75.7999267578125)
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
    random_value_010.location = (669.0, -315.7999267578125)
    random_value_010.bl_label = "Random Value"
    random_value_010.data_type = "FLOAT"
    # Min
    random_value_010.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_010.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_010.inputs[2].default_value = 0.10000000894069672
    # Max
    random_value_010.inputs[3].default_value = 0.4000000059604645
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

    frame_016 = nodes.new("NodeFrame")
    frame_016.name = "Frame.016"
    frame_016.label = "Larger Jewels"
    frame_016.location = (4649.0, -3755.80029296875)
    frame_016.bl_label = "Frame"
    frame_016.text = None
    frame_016.shrink = True
    frame_016.label_size = 20
    # Links for frame_016

    realize_instances_002 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.name = "Realize Instances.002"
    realize_instances_002.label = ""
    realize_instances_002.location = (1009.0, -75.7999267578125)
    realize_instances_002.bl_label = "Realize Instances"
    # Selection
    realize_instances_002.inputs[1].default_value = True
    # Realize All
    realize_instances_002.inputs[2].default_value = True
    # Depth
    realize_instances_002.inputs[3].default_value = 0
    # Links for realize_instances_002

    transform_geometry_010 = nodes.new("GeometryNodeTransform")
    transform_geometry_010.name = "Transform Geometry.010"
    transform_geometry_010.label = ""
    transform_geometry_010.location = (269.0, -415.7999267578125)
    transform_geometry_010.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_010.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_010.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    # Rotation
    transform_geometry_010.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_010.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_010
    links.new(transform_geometry_010.outputs[0], instance_on_points_001.inputs[2])
    links.new(gem_in_holder_2.outputs[0], transform_geometry_010.inputs[0])

    swap_attr = nodes.new("GeometryNodeGroup")
    swap_attr.name = "Group.005"
    swap_attr.label = ""
    swap_attr.location = (1169.0, -75.7999267578125)
    swap_attr.node_tree = create_swap__attr_group()
    swap_attr.bl_label = "Group"
    # Old
    swap_attr.inputs[2].default_value = "ruby"
    # New
    swap_attr.inputs[3].default_value = "saphire"
    # Links for swap_attr
    links.new(realize_instances_002.outputs[0], swap_attr.inputs[0])
    links.new(swap_attr.outputs[0], join_geometry_002.inputs[0])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (849.0, -75.7999267578125)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "INSTANCE"
    # Links for capture_attribute_001
    links.new(capture_attribute_001.outputs[0], realize_instances_002.inputs[0])
    links.new(instance_on_points_001.outputs[0], capture_attribute_001.inputs[0])
    links.new(capture_attribute_001.outputs[1], swap_attr.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (849.0, -195.7999267578125)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], capture_attribute_001.inputs[1])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1889.0, -75.13330078125)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001
    links.new(transform_geometry_009.outputs[0], set_position_001.inputs[0])

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.label = ""
    geometry_proximity_001.location = (1709.0, -275.13330078125)
    geometry_proximity_001.bl_label = "Geometry Proximity"
    geometry_proximity_001.target_element = "FACES"
    # Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0
    # Links for geometry_proximity_001
    links.new(bi_rail_loft.outputs[0], geometry_proximity_001.inputs[0])
    links.new(geometry_proximity_001.outputs[0], set_position_001.inputs[2])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (2149.0, -95.13330078125)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh
    links.new(set_position_001.outputs[0], curve_to_mesh.inputs[0])
    links.new(gem_in_holder_1.outputs[1], curve_to_mesh.inputs[1])
    links.new(gem_in_holder_1.outputs[2], curve_to_mesh.inputs[2])
    links.new(curve_to_mesh.outputs[0], store_named_attribute_001.inputs[0])

    separate_geometry_002 = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.name = "Separate Geometry.002"
    separate_geometry_002.label = ""
    separate_geometry_002.location = (29.0, -29.0)
    separate_geometry_002.bl_label = "Separate Geometry"
    separate_geometry_002.domain = "CURVE"
    # Links for separate_geometry_002
    links.new(bi_rail_loft.outputs[1], separate_geometry_002.inputs[0])

    compare_007 = nodes.new("FunctionNodeCompare")
    compare_007.name = "Compare.007"
    compare_007.label = ""
    compare_007.location = (29.0, -169.0)
    compare_007.bl_label = "Compare"
    compare_007.operation = "EQUAL"
    compare_007.data_type = "FLOAT"
    compare_007.mode = "ELEMENT"
    # B
    compare_007.inputs[1].default_value = 0.5
    # A
    compare_007.inputs[2].default_value = 0
    # B
    compare_007.inputs[3].default_value = 0
    # A
    compare_007.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_007.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_007.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_007.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_007.inputs[8].default_value = ""
    # B
    compare_007.inputs[9].default_value = ""
    # C
    compare_007.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_007.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_007.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_007
    links.new(compare_007.outputs[0], separate_geometry_002.inputs[1])

    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_004.name = "Separate XYZ.004"
    separate_x_y_z_004.label = ""
    separate_x_y_z_004.location = (29.0, -329.0)
    separate_x_y_z_004.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_004
    links.new(bi_rail_loft.outputs[2], separate_x_y_z_004.inputs[0])
    links.new(separate_x_y_z_004.outputs[1], compare_007.inputs[0])

    trim_curve_002 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_002.name = "Trim Curve.002"
    trim_curve_002.label = ""
    trim_curve_002.location = (189.0, -29.0)
    trim_curve_002.bl_label = "Trim Curve"
    trim_curve_002.mode = "FACTOR"
    # Selection
    trim_curve_002.inputs[1].default_value = True
    # Start
    trim_curve_002.inputs[2].default_value = 0.0
    # End
    trim_curve_002.inputs[3].default_value = 0.8690060973167419
    # Start
    trim_curve_002.inputs[4].default_value = 0.0
    # End
    trim_curve_002.inputs[5].default_value = 1.0
    # Links for trim_curve_002
    links.new(separate_geometry_002.outputs[0], trim_curve_002.inputs[0])

    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.name = "Resample Curve.002"
    resample_curve_002.label = ""
    resample_curve_002.location = (349.0, -29.0)
    resample_curve_002.bl_label = "Resample Curve"
    resample_curve_002.keep_last_segment = True
    # Selection
    resample_curve_002.inputs[1].default_value = True
    # Mode
    resample_curve_002.inputs[2].default_value = "Count"
    # Count
    resample_curve_002.inputs[3].default_value = 47
    # Length
    resample_curve_002.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_002
    links.new(trim_curve_002.outputs[0], resample_curve_002.inputs[0])

    gold_decorations_1 = nodes.new("GeometryNodeGroup")
    gold_decorations_1.name = "Group.008"
    gold_decorations_1.label = ""
    gold_decorations_1.location = (869.0, -29.0)
    gold_decorations_1.node_tree = create_gold__decorations_group()
    gold_decorations_1.bl_label = "Group"
    # Seed
    gold_decorations_1.inputs[1].default_value = 75
    # Scale
    gold_decorations_1.inputs[2].default_value = 3.0999999046325684
    # Count
    gold_decorations_1.inputs[3].default_value = 6
    # Links for gold_decorations_1
    links.new(gold_decorations_1.outputs[0], join_geometry_002.inputs[0])

    set_curve_normal_003 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_003.name = "Set Curve Normal.003"
    set_curve_normal_003.label = ""
    set_curve_normal_003.location = (509.0, -29.0)
    set_curve_normal_003.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_003.inputs[1].default_value = True
    # Mode
    set_curve_normal_003.inputs[2].default_value = "Z Up"
    # Normal
    set_curve_normal_003.inputs[3].default_value = Vector((0.0, 0.0, 1.0))
    # Links for set_curve_normal_003
    links.new(resample_curve_002.outputs[0], set_curve_normal_003.inputs[0])

    frame_013 = nodes.new("NodeFrame")
    frame_013.name = "Frame.013"
    frame_013.label = ""
    frame_013.location = (1149.0, -1242.60009765625)
    frame_013.bl_label = "Frame"
    frame_013.text = None
    frame_013.shrink = True
    frame_013.label_size = 20
    # Links for frame_013

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (689.0, -49.0)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((0.0, -0.0010000000474974513, 0.0))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry
    links.new(transform_geometry.outputs[0], gold_decorations_1.inputs[0])
    links.new(set_curve_normal_003.outputs[0], transform_geometry.inputs[0])

    random_value_011 = nodes.new("FunctionNodeRandomValue")
    random_value_011.name = "Random Value.011"
    random_value_011.label = ""
    random_value_011.location = (509.0, -335.7999267578125)
    random_value_011.bl_label = "Random Value"
    random_value_011.data_type = "FLOAT"
    # Min
    random_value_011.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_011.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_011.inputs[2].default_value = 0.20000000298023224
    # Max
    random_value_011.inputs[3].default_value = 0.6000000238418579
    # Min
    random_value_011.inputs[4].default_value = 0
    # Max
    random_value_011.inputs[5].default_value = 100
    # Probability
    random_value_011.inputs[6].default_value = 0.5
    # ID
    random_value_011.inputs[7].default_value = 0
    # Seed
    random_value_011.inputs[8].default_value = 0
    # Links for random_value_011
    links.new(random_value_011.outputs[1], instance_on_points.inputs[6])

    trim_curve_003 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_003.name = "Trim Curve.003"
    trim_curve_003.label = ""
    trim_curve_003.location = (189.0, -29.0)
    trim_curve_003.bl_label = "Trim Curve"
    trim_curve_003.mode = "FACTOR"
    # Selection
    trim_curve_003.inputs[1].default_value = True
    # Start
    trim_curve_003.inputs[2].default_value = 0.10000000149011612
    # End
    trim_curve_003.inputs[3].default_value = 0.5
    # Start
    trim_curve_003.inputs[4].default_value = 0.0
    # End
    trim_curve_003.inputs[5].default_value = 1.0
    # Links for trim_curve_003

    resample_curve_003 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.name = "Resample Curve.003"
    resample_curve_003.label = ""
    resample_curve_003.location = (349.0, -29.0)
    resample_curve_003.bl_label = "Resample Curve"
    resample_curve_003.keep_last_segment = True
    # Selection
    resample_curve_003.inputs[1].default_value = True
    # Mode
    resample_curve_003.inputs[2].default_value = "Count"
    # Count
    resample_curve_003.inputs[3].default_value = 47
    # Length
    resample_curve_003.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_003
    links.new(trim_curve_003.outputs[0], resample_curve_003.inputs[0])

    gold_decorations_2 = nodes.new("GeometryNodeGroup")
    gold_decorations_2.name = "Group.009"
    gold_decorations_2.label = ""
    gold_decorations_2.location = (1029.0, -29.0)
    gold_decorations_2.node_tree = create_gold__decorations_group()
    gold_decorations_2.bl_label = "Group"
    # Seed
    gold_decorations_2.inputs[1].default_value = 78
    # Scale
    gold_decorations_2.inputs[2].default_value = 3.1999998092651367
    # Count
    gold_decorations_2.inputs[3].default_value = 13
    # Links for gold_decorations_2

    set_curve_normal_004 = nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_004.name = "Set Curve Normal.004"
    set_curve_normal_004.label = ""
    set_curve_normal_004.location = (509.0, -29.0)
    set_curve_normal_004.bl_label = "Set Curve Normal"
    # Selection
    set_curve_normal_004.inputs[1].default_value = True
    # Mode
    set_curve_normal_004.inputs[2].default_value = "Free"
    # Links for set_curve_normal_004
    links.new(resample_curve_003.outputs[0], set_curve_normal_004.inputs[0])
    links.new(vector_math.outputs[0], set_curve_normal_004.inputs[3])

    frame_017 = nodes.new("NodeFrame")
    frame_017.name = "Frame.017"
    frame_017.label = ""
    frame_017.location = (1149.0, -622.60009765625)
    frame_017.bl_label = "Frame"
    frame_017.text = None
    frame_017.shrink = True
    frame_017.label_size = 20
    # Links for frame_017

    transform_geometry_011 = nodes.new("GeometryNodeTransform")
    transform_geometry_011.name = "Transform Geometry.011"
    transform_geometry_011.label = ""
    transform_geometry_011.location = (869.0, -29.0)
    transform_geometry_011.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_011.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_011.inputs[2].default_value = Vector((0.0, 0.0, -0.003000000026077032))
    # Rotation
    transform_geometry_011.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_011.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_011
    links.new(transform_geometry_011.outputs[0], gold_decorations_2.inputs[0])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (29.0, -29.0)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Selection
    mesh_to_curve.inputs[1].default_value = True
    # Links for mesh_to_curve
    links.new(separate_geometry.outputs[0], mesh_to_curve.inputs[0])
    links.new(mesh_to_curve.outputs[0], trim_curve_003.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    set_curve_tilt.label = ""
    set_curve_tilt.location = (689.0, -29.0)
    set_curve_tilt.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Tilt
    set_curve_tilt.inputs[2].default_value = -0.34819304943084717
    # Links for set_curve_tilt
    links.new(set_curve_tilt.outputs[0], transform_geometry_011.inputs[0])
    links.new(set_curve_normal_004.outputs[0], set_curve_tilt.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (4178.0, -3711.60009765625)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], join_geometry_002.inputs[0])
    links.new(gold_on_band.outputs[0], reroute_002.inputs[0])

    curve_circle_002 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_002.name = "Curve Circle.002"
    curve_circle_002.label = ""
    curve_circle_002.location = (1229.0, -35.7998046875)
    curve_circle_002.bl_label = "Curve Circle"
    curve_circle_002.mode = "RADIUS"
    # Resolution
    curve_circle_002.inputs[0].default_value = 64
    # Point 1
    curve_circle_002.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_002.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_002.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_002.inputs[4].default_value = 0.12999999523162842
    # Links for curve_circle_002

    transform_geometry_012 = nodes.new("GeometryNodeTransform")
    transform_geometry_012.name = "Transform Geometry.012"
    transform_geometry_012.label = ""
    transform_geometry_012.location = (1949.0, -395.7998046875)
    transform_geometry_012.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_012.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_012.inputs[2].default_value = Vector((0.009999999776482582, -0.03999999910593033, 0.46000000834465027))
    # Rotation
    transform_geometry_012.inputs[3].default_value = Euler((-0.027925267815589905, 0.0, 0.15533429384231567), 'XYZ')
    # Scale
    transform_geometry_012.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_012

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (1789.0, -395.7998046875)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Links for set_position_002
    links.new(curve_circle_002.outputs[0], set_position_002.inputs[0])
    links.new(set_position_002.outputs[0], transform_geometry_012.inputs[0])

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (629.0, -635.7998046875)
    position_003.bl_label = "Position"
    # Links for position_003

    separate_x_y_z_005 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_005.name = "Separate XYZ.005"
    separate_x_y_z_005.label = ""
    separate_x_y_z_005.location = (629.0, -695.7998046875)
    separate_x_y_z_005.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_005
    links.new(position_003.outputs[0], separate_x_y_z_005.inputs[0])

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.label = ""
    map_range_001.location = (789.0, -635.7998046875)
    map_range_001.bl_label = "Map Range"
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT"
    # From Min
    map_range_001.inputs[1].default_value = 0.12999999523162842
    # From Max
    map_range_001.inputs[2].default_value = -0.12999999523162842
    # To Min
    map_range_001.inputs[3].default_value = 0.0
    # To Max
    map_range_001.inputs[4].default_value = 1.0
    # Steps
    map_range_001.inputs[5].default_value = 4.0
    # Vector
    map_range_001.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_001.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_001.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_001.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_001.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_001
    links.new(separate_x_y_z_005.outputs[1], map_range_001.inputs[0])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (969.0, -635.7998046875)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(map_range_001.outputs[0], float_curve.inputs[1])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (1429.0, -675.7998046875)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = -0.29999998211860657
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (1589.0, -675.7998046875)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # X
    combine_x_y_z_001.inputs[0].default_value = 0.0
    # Links for combine_x_y_z_001
    links.new(combine_x_y_z_001.outputs[0], set_position_002.inputs[3])
    links.new(math_002.outputs[0], combine_x_y_z_001.inputs[2])

    position_005 = nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"
    position_005.label = ""
    position_005.location = (1069.0, -155.7998046875)
    position_005.bl_label = "Position"
    # Links for position_005

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (1229.0, -155.7998046875)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "MULTIPLY"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(position_005.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], set_position_002.inputs[2])

    combine_x_y_z_002 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_002.name = "Combine XYZ.002"
    combine_x_y_z_002.label = ""
    combine_x_y_z_002.location = (1229.0, -295.7998046875)
    combine_x_y_z_002.bl_label = "Combine XYZ"
    # Y
    combine_x_y_z_002.inputs[1].default_value = 1.0
    # Z
    combine_x_y_z_002.inputs[2].default_value = 1.0
    # Links for combine_x_y_z_002
    links.new(combine_x_y_z_002.outputs[0], vector_math_001.inputs[1])

    float_curve_002 = nodes.new("ShaderNodeFloatCurve")
    float_curve_002.name = "Float Curve.002"
    float_curve_002.label = ""
    float_curve_002.location = (969.0, -295.7998046875)
    float_curve_002.bl_label = "Float Curve"
    # Factor
    float_curve_002.inputs[0].default_value = 1.0
    # Links for float_curve_002
    links.new(map_range_001.outputs[0], float_curve_002.inputs[1])
    links.new(float_curve_002.outputs[0], combine_x_y_z_002.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (5618.0, -2771.5986328125)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "skip"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(store_named_attribute.outputs[0], join_geometry_002.inputs[0])

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (2129.0, -395.7998046875)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Length"
    # Count
    resample_curve.inputs[3].default_value = 10
    # Length
    resample_curve.inputs[4].default_value = 0.014999999664723873
    # Links for resample_curve
    links.new(transform_geometry_012.outputs[0], resample_curve.inputs[0])

    instance_on_points_002 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.name = "Instance on Points.002"
    instance_on_points_002.label = ""
    instance_on_points_002.location = (3469.0, -535.7998046875)
    instance_on_points_002.bl_label = "Instance on Points"
    # Selection
    instance_on_points_002.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_002.inputs[3].default_value = False
    # Instance Index
    instance_on_points_002.inputs[4].default_value = 0
    # Scale
    instance_on_points_002.inputs[6].default_value = Vector((0.699999988079071, 0.699999988079071, 0.699999988079071))
    # Links for instance_on_points_002

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.label = ""
    align_rotation_to_vector.location = (29.0, -35.7998046875)
    align_rotation_to_vector.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector.axis = "X"
    align_rotation_to_vector.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector

    curve_tangent_001 = nodes.new("GeometryNodeInputTangent")
    curve_tangent_001.name = "Curve Tangent.001"
    curve_tangent_001.label = ""
    curve_tangent_001.location = (29.0, -195.7998046875)
    curve_tangent_001.bl_label = "Curve Tangent"
    # Links for curve_tangent_001
    links.new(curve_tangent_001.outputs[0], align_rotation_to_vector.inputs[2])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.label = ""
    align_rotation_to_vector_001.location = (189.0, -35.7998046875)
    align_rotation_to_vector_001.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_001.axis = "Y"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_001
    links.new(align_rotation_to_vector.outputs[0], align_rotation_to_vector_001.inputs[0])

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.name = "Normal.001"
    normal_001.label = ""
    normal_001.location = (189.0, -195.7998046875)
    normal_001.bl_label = "Normal"
    normal_001.legacy_corner_normals = False
    # Links for normal_001
    links.new(normal_001.outputs[0], align_rotation_to_vector_001.inputs[2])

    rotate_rotation_003 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_003.name = "Rotate Rotation.003"
    rotate_rotation_003.label = ""
    rotate_rotation_003.location = (349.0, -35.7998046875)
    rotate_rotation_003.bl_label = "Rotate Rotation"
    rotate_rotation_003.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_003.inputs[1].default_value = Euler((0.23108159005641937, 0.14137165248394012, 0.0), 'XYZ')
    # Links for rotate_rotation_003
    links.new(align_rotation_to_vector_001.outputs[0], rotate_rotation_003.inputs[0])

    spline_parameter = nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.label = ""
    spline_parameter.location = (1669.0, -55.7998046875)
    spline_parameter.bl_label = "Spline Parameter"
    # Links for spline_parameter

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (1849.0, -55.7998046875)
    math_003.bl_label = "Math"
    math_003.operation = "SUBTRACT"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 0.7400000095367432
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(spline_parameter.outputs[0], math_003.inputs[0])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (2029.0, -55.7998046875)
    math_004.bl_label = "Math"
    math_004.operation = "ABSOLUTE"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 0.7400000095367432
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(math_003.outputs[0], math_004.inputs[0])

    set_curve_tilt_002 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_002.name = "Set Curve Tilt.002"
    set_curve_tilt_002.label = ""
    set_curve_tilt_002.location = (2589.0, -395.7998046875)
    set_curve_tilt_002.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_002.inputs[1].default_value = True
    # Links for set_curve_tilt_002
    links.new(set_curve_tilt_002.outputs[0], instance_on_points_002.inputs[0])
    links.new(resample_curve.outputs[0], set_curve_tilt_002.inputs[0])

    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.name = "Map Range.002"
    map_range_002.label = ""
    map_range_002.location = (2229.0, -75.7998046875)
    map_range_002.bl_label = "Map Range"
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    # From Min
    map_range_002.inputs[1].default_value = 0.0
    # From Max
    map_range_002.inputs[2].default_value = 0.08000002801418304
    # To Min
    map_range_002.inputs[3].default_value = 0.6799999475479126
    # To Max
    map_range_002.inputs[4].default_value = 0.47999998927116394
    # Steps
    map_range_002.inputs[5].default_value = 4.0
    # Vector
    map_range_002.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_002.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_002.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_002.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_002.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_002.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_002
    links.new(math_004.outputs[0], map_range_002.inputs[0])
    links.new(map_range_002.outputs[0], set_curve_tilt_002.inputs[2])

    float_curve_003 = nodes.new("ShaderNodeFloatCurve")
    float_curve_003.name = "Float Curve.003"
    float_curve_003.label = ""
    float_curve_003.location = (269.0, -1115.7998046875)
    float_curve_003.bl_label = "Float Curve"
    # Factor
    float_curve_003.inputs[0].default_value = 1.0
    # Links for float_curve_003

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.label = ""
    spline_parameter_001.location = (29.0, -1355.7998046875)
    spline_parameter_001.bl_label = "Spline Parameter"
    # Links for spline_parameter_001
    links.new(spline_parameter_001.outputs[0], float_curve_003.inputs[1])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (609.0, -1095.7998046875)
    math_005.bl_label = "Math"
    math_005.operation = "MULTIPLY"
    math_005.use_clamp = False
    # Value
    math_005.inputs[1].default_value = 0.014999999664723873
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(float_curve_003.outputs[0], math_005.inputs[0])

    curve_circle_003 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.name = "Curve Circle.003"
    curve_circle_003.label = ""
    curve_circle_003.location = (29.0, -99.6669921875)
    curve_circle_003.bl_label = "Curve Circle"
    curve_circle_003.mode = "RADIUS"
    # Resolution
    curve_circle_003.inputs[0].default_value = 20
    # Point 1
    curve_circle_003.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_003.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_003.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_003.inputs[4].default_value = 0.014999999664723873
    # Links for curve_circle_003

    instance_on_points_003 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.name = "Instance on Points.003"
    instance_on_points_003.label = ""
    instance_on_points_003.location = (189.0, -99.6669921875)
    instance_on_points_003.bl_label = "Instance on Points"
    # Selection
    instance_on_points_003.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_003.inputs[3].default_value = False
    # Instance Index
    instance_on_points_003.inputs[4].default_value = 0
    # Rotation
    instance_on_points_003.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_003.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_003
    links.new(curve_circle_003.outputs[0], instance_on_points_003.inputs[0])

    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.name = "Ico Sphere.001"
    ico_sphere_001.label = ""
    ico_sphere_001.location = (29.0, -239.6669921875)
    ico_sphere_001.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_001.inputs[0].default_value = 0.0020000000949949026
    # Subdivisions
    ico_sphere_001.inputs[1].default_value = 1
    # Links for ico_sphere_001
    links.new(ico_sphere_001.outputs[0], instance_on_points_003.inputs[2])

    cylinder_001 = nodes.new("GeometryNodeMeshCylinder")
    cylinder_001.name = "Cylinder.001"
    cylinder_001.label = ""
    cylinder_001.location = (189.0, -39.6669921875)
    cylinder_001.bl_label = "Cylinder"
    cylinder_001.fill_type = "NGON"
    # Vertices
    cylinder_001.inputs[0].default_value = 10
    # Side Segments
    cylinder_001.inputs[1].default_value = 1
    # Fill Segments
    cylinder_001.inputs[2].default_value = 1
    # Radius
    cylinder_001.inputs[3].default_value = 0.014999999664723873
    # Depth
    cylinder_001.inputs[4].default_value = 0.0020000000949949026
    # Links for cylinder_001

    join_geometry_003 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.label = ""
    join_geometry_003.location = (1169.0, -39.6669921875)
    join_geometry_003.bl_label = "Join Geometry"
    # Links for join_geometry_003
    links.new(instance_on_points_003.outputs[0], join_geometry_003.inputs[0])
    links.new(cylinder_001.outputs[0], join_geometry_003.inputs[0])

    ico_sphere_002 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_002.name = "Ico Sphere.002"
    ico_sphere_002.label = ""
    ico_sphere_002.location = (349.0, -99.6669921875)
    ico_sphere_002.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_002.inputs[0].default_value = 0.012000000104308128
    # Subdivisions
    ico_sphere_002.inputs[1].default_value = 2
    # Links for ico_sphere_002

    transform_geometry_013 = nodes.new("GeometryNodeTransform")
    transform_geometry_013.name = "Transform Geometry.013"
    transform_geometry_013.label = ""
    transform_geometry_013.location = (749.0, -119.6669921875)
    transform_geometry_013.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_013.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_013.inputs[2].default_value = Vector((-0.006000000052154064, 0.0, 0.0010000000474974513))
    # Rotation
    transform_geometry_013.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_013.inputs[4].default_value = Vector((0.4699999988079071, 0.8600000143051147, 0.05000000074505806))
    # Links for transform_geometry_013
    links.new(transform_geometry_013.outputs[0], join_geometry_003.inputs[0])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    set_position_003.label = ""
    set_position_003.location = (569.0, -139.6669921875)
    set_position_003.bl_label = "Set Position"
    # Selection
    set_position_003.inputs[1].default_value = True
    # Position
    set_position_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_003
    links.new(set_position_003.outputs[0], transform_geometry_013.inputs[0])
    links.new(ico_sphere_002.outputs[0], set_position_003.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (569.0, -279.6669921875)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 0.004999999888241291
    # Links for vector_math_002
    links.new(vector_math_002.outputs[0], set_position_003.inputs[3])

    noise_texture = nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.label = ""
    noise_texture.location = (369.0, -279.6669921875)
    noise_texture.bl_label = "Noise Texture"
    noise_texture.noise_dimensions = "4D"
    noise_texture.noise_type = "FBM"
    noise_texture.normalize = False
    # Vector
    noise_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # W
    noise_texture.inputs[1].default_value = 60.499996185302734
    # Scale
    noise_texture.inputs[2].default_value = 29.089996337890625
    # Detail
    noise_texture.inputs[3].default_value = 2.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Offset
    noise_texture.inputs[6].default_value = 0.0
    # Gain
    noise_texture.inputs[7].default_value = 1.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0
    # Links for noise_texture
    links.new(noise_texture.outputs[0], vector_math_002.inputs[0])

    transform_geometry_014 = nodes.new("GeometryNodeTransform")
    transform_geometry_014.name = "Transform Geometry.014"
    transform_geometry_014.label = ""
    transform_geometry_014.location = (909.0, -179.6669921875)
    transform_geometry_014.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_014.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_014.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_014.inputs[3].default_value = Euler((0.0, 0.0, 3.1415927410125732), 'XYZ')
    # Scale
    transform_geometry_014.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_014
    links.new(transform_geometry_013.outputs[0], transform_geometry_014.inputs[0])
    links.new(transform_geometry_014.outputs[0], join_geometry_003.inputs[0])

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Necklace Link"
    frame_002.location = (1700.0, -1016.1328125)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    rotate_rotation_004 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_004.name = "Rotate Rotation.004"
    rotate_rotation_004.label = ""
    rotate_rotation_004.location = (509.0, -35.7998046875)
    rotate_rotation_004.bl_label = "Rotate Rotation"
    rotate_rotation_004.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_004.inputs[1].default_value = Euler((3.1415927410125732, 0.0, 1.5707963705062866), 'XYZ')
    # Links for rotate_rotation_004
    links.new(rotate_rotation_003.outputs[0], rotate_rotation_004.inputs[0])
    links.new(rotate_rotation_004.outputs[0], instance_on_points_002.inputs[5])

    ico_sphere_003 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_003.name = "Ico Sphere.003"
    ico_sphere_003.label = ""
    ico_sphere_003.location = (29.0, -399.6669921875)
    ico_sphere_003.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_003.inputs[0].default_value = 0.004999999888241291
    # Subdivisions
    ico_sphere_003.inputs[1].default_value = 1
    # Links for ico_sphere_003
    links.new(ico_sphere_003.outputs[0], join_geometry_003.inputs[0])

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Align"
    frame_003.location = (2220.0, -680.0)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (1369.0, -39.6669921875)
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
    links.new(store_named_attribute_004.outputs[0], instance_on_points_002.inputs[2])
    links.new(join_geometry_003.outputs[0], store_named_attribute_004.inputs[0])

    cylinder_002 = nodes.new("GeometryNodeMeshCylinder")
    cylinder_002.name = "Cylinder.002"
    cylinder_002.label = ""
    cylinder_002.location = (29.0, -115.7998046875)
    cylinder_002.bl_label = "Cylinder"
    cylinder_002.fill_type = "NGON"
    # Vertices
    cylinder_002.inputs[0].default_value = 16
    # Side Segments
    cylinder_002.inputs[1].default_value = 1
    # Fill Segments
    cylinder_002.inputs[2].default_value = 1
    # Radius
    cylinder_002.inputs[3].default_value = 0.019999999552965164
    # Depth
    cylinder_002.inputs[4].default_value = 0.0020000000949949026
    # Links for cylinder_002

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (1249.0, -655.7998046875)
    math_006.bl_label = "Math"
    math_006.operation = "ADD"
    math_006.use_clamp = False
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(math_006.outputs[0], math_002.inputs[0])
    links.new(float_curve.outputs[0], math_006.inputs[0])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"
    spline_parameter_002.label = ""
    spline_parameter_002.location = (29.0, -935.7998046875)
    spline_parameter_002.bl_label = "Spline Parameter"
    # Links for spline_parameter_002

    float_curve_004 = nodes.new("ShaderNodeFloatCurve")
    float_curve_004.name = "Float Curve.004"
    float_curve_004.label = ""
    float_curve_004.location = (269.0, -795.7998046875)
    float_curve_004.bl_label = "Float Curve"
    # Factor
    float_curve_004.inputs[0].default_value = 1.0
    # Links for float_curve_004
    links.new(spline_parameter_002.outputs[0], float_curve_004.inputs[1])
    links.new(float_curve_004.outputs[0], math_006.inputs[1])

    set_position_004 = nodes.new("GeometryNodeSetPosition")
    set_position_004.name = "Set Position.004"
    set_position_004.label = ""
    set_position_004.location = (869.0, -155.7998046875)
    set_position_004.bl_label = "Set Position"
    # Selection
    set_position_004.inputs[1].default_value = True
    # Position
    set_position_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_004
    links.new(cylinder_002.outputs[0], set_position_004.inputs[0])

    position_006 = nodes.new("GeometryNodeInputPosition")
    position_006.name = "Position.006"
    position_006.label = ""
    position_006.location = (229.0, -215.7998046875)
    position_006.bl_label = "Position"
    # Links for position_006

    separate_x_y_z_006 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_006.name = "Separate XYZ.006"
    separate_x_y_z_006.label = ""
    separate_x_y_z_006.location = (229.0, -275.7998046875)
    separate_x_y_z_006.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_006
    links.new(position_006.outputs[0], separate_x_y_z_006.inputs[0])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.label = ""
    math_007.location = (389.0, -215.7998046875)
    math_007.bl_label = "Math"
    math_007.operation = "ABSOLUTE"
    math_007.use_clamp = False
    # Value
    math_007.inputs[1].default_value = 0.5
    # Value
    math_007.inputs[2].default_value = 0.5
    # Links for math_007
    links.new(separate_x_y_z_006.outputs[0], math_007.inputs[0])

    combine_x_y_z_003 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_003.name = "Combine XYZ.003"
    combine_x_y_z_003.label = ""
    combine_x_y_z_003.location = (709.0, -215.7998046875)
    combine_x_y_z_003.bl_label = "Combine XYZ"
    # X
    combine_x_y_z_003.inputs[0].default_value = 0.0
    # Z
    combine_x_y_z_003.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_003
    links.new(combine_x_y_z_003.outputs[0], set_position_004.inputs[3])

    map_range_003 = nodes.new("ShaderNodeMapRange")
    map_range_003.name = "Map Range.003"
    map_range_003.label = ""
    map_range_003.location = (389.0, -355.7998046875)
    map_range_003.bl_label = "Map Range"
    map_range_003.clamp = True
    map_range_003.interpolation_type = "LINEAR"
    map_range_003.data_type = "FLOAT"
    # From Min
    map_range_003.inputs[1].default_value = -0.019999999552965164
    # From Max
    map_range_003.inputs[2].default_value = 0.019999999552965164
    # To Min
    map_range_003.inputs[3].default_value = 0.7999999523162842
    # To Max
    map_range_003.inputs[4].default_value = 0.19999998807907104
    # Steps
    map_range_003.inputs[5].default_value = 4.0
    # Vector
    map_range_003.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_003.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_003.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_003.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_003.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_003.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_003
    links.new(separate_x_y_z_006.outputs[1], map_range_003.inputs[0])

    math_008 = nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.label = ""
    math_008.location = (549.0, -215.7998046875)
    math_008.bl_label = "Math"
    math_008.operation = "MULTIPLY"
    math_008.use_clamp = False
    # Value
    math_008.inputs[2].default_value = 0.5
    # Links for math_008
    links.new(math_008.outputs[0], combine_x_y_z_003.inputs[1])
    links.new(math_007.outputs[0], math_008.inputs[0])
    links.new(map_range_003.outputs[0], math_008.inputs[1])

    boolean_math_004 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.name = "Boolean Math.004"
    boolean_math_004.label = ""
    boolean_math_004.location = (969.0, -495.7998046875)
    boolean_math_004.bl_label = "Boolean Math"
    boolean_math_004.operation = "AND"
    # Links for boolean_math_004
    links.new(cylinder_002.outputs[1], boolean_math_004.inputs[0])
    links.new(cylinder_002.outputs[2], boolean_math_004.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (1189.0, -375.7998046875)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Links for mesh_to_curve_001
    links.new(set_position_004.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(boolean_math_004.outputs[0], mesh_to_curve_001.inputs[1])

    ico_sphere_004 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_004.name = "Ico Sphere.004"
    ico_sphere_004.label = ""
    ico_sphere_004.location = (1189.0, -515.7998046875)
    ico_sphere_004.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_004.inputs[0].default_value = 0.0020000000949949026
    # Subdivisions
    ico_sphere_004.inputs[1].default_value = 1
    # Links for ico_sphere_004

    instance_on_points_004 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_004.name = "Instance on Points.004"
    instance_on_points_004.label = ""
    instance_on_points_004.location = (1369.0, -375.7998046875)
    instance_on_points_004.bl_label = "Instance on Points"
    # Selection
    instance_on_points_004.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_004.inputs[3].default_value = False
    # Instance Index
    instance_on_points_004.inputs[4].default_value = 0
    # Rotation
    instance_on_points_004.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_004.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_004
    links.new(mesh_to_curve_001.outputs[0], instance_on_points_004.inputs[0])
    links.new(ico_sphere_004.outputs[0], instance_on_points_004.inputs[2])

    transform_geometry_015 = nodes.new("GeometryNodeTransform")
    transform_geometry_015.name = "Transform Geometry.015"
    transform_geometry_015.label = ""
    transform_geometry_015.location = (1909.0, -495.7998046875)
    transform_geometry_015.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_015.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_015.inputs[2].default_value = Vector((0.0, 0.0, 0.0020000000949949026))
    # Rotation
    transform_geometry_015.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_015.inputs[4].default_value = Vector((2.0, 1.0, 0.30000001192092896))
    # Links for transform_geometry_015

    ico_sphere_005 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_005.name = "Ico Sphere.005"
    ico_sphere_005.label = ""
    ico_sphere_005.location = (1569.0, -495.7998046875)
    ico_sphere_005.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_005.inputs[0].default_value = 0.004999999888241291
    # Subdivisions
    ico_sphere_005.inputs[1].default_value = 2
    # Links for ico_sphere_005

    dual_mesh = nodes.new("GeometryNodeDualMesh")
    dual_mesh.name = "Dual Mesh"
    dual_mesh.label = ""
    dual_mesh.location = (1749.0, -495.7998046875)
    dual_mesh.bl_label = "Dual Mesh"
    # Keep Boundaries
    dual_mesh.inputs[1].default_value = False
    # Links for dual_mesh
    links.new(ico_sphere_005.outputs[0], dual_mesh.inputs[0])
    links.new(dual_mesh.outputs[0], transform_geometry_015.inputs[0])

    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_007.name = "Join Geometry.007"
    join_geometry_007.label = ""
    join_geometry_007.location = (2269.0, -315.7998046875)
    join_geometry_007.bl_label = "Join Geometry"
    # Links for join_geometry_007

    transform_geometry_016 = nodes.new("GeometryNodeTransform")
    transform_geometry_016.name = "Transform Geometry.016"
    transform_geometry_016.label = ""
    transform_geometry_016.location = (2109.0, -355.7998046875)
    transform_geometry_016.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_016.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_016.inputs[2].default_value = Vector((0.0, 0.003000000026077032, 0.0))
    # Rotation
    transform_geometry_016.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    # Scale
    transform_geometry_016.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_016
    links.new(transform_geometry_015.outputs[0], transform_geometry_016.inputs[0])
    links.new(transform_geometry_016.outputs[0], join_geometry_007.inputs[0])

    transform_geometry_017 = nodes.new("GeometryNodeTransform")
    transform_geometry_017.name = "Transform Geometry.017"
    transform_geometry_017.label = ""
    transform_geometry_017.location = (2109.0, -675.7998046875)
    transform_geometry_017.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_017.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_017.inputs[2].default_value = Vector((-0.009999999776482582, 0.009999999776482582, 0.0))
    # Rotation
    transform_geometry_017.inputs[3].default_value = Euler((0.0, 0.0, 1.0471975803375244), 'XYZ')
    # Scale
    transform_geometry_017.inputs[4].default_value = Vector((0.6000000238418579, 0.6000000238418579, 1.0))
    # Links for transform_geometry_017
    links.new(transform_geometry_015.outputs[0], transform_geometry_017.inputs[0])
    links.new(transform_geometry_017.outputs[0], join_geometry_007.inputs[0])

    transform_geometry_018 = nodes.new("GeometryNodeTransform")
    transform_geometry_018.name = "Transform Geometry.018"
    transform_geometry_018.label = ""
    transform_geometry_018.location = (2269.0, -675.7998046875)
    transform_geometry_018.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_018.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_018.inputs[2].default_value = Vector((0.009999999776482582, 0.009999999776482582, 0.0))
    # Rotation
    transform_geometry_018.inputs[3].default_value = Euler((0.0, 0.0, -1.0471975803375244), 'XYZ')
    # Scale
    transform_geometry_018.inputs[4].default_value = Vector((0.6000000238418579, 0.6000000238418579, 1.0))
    # Links for transform_geometry_018
    links.new(transform_geometry_015.outputs[0], transform_geometry_018.inputs[0])
    links.new(transform_geometry_018.outputs[0], join_geometry_007.inputs[0])

    transform_geometry_019 = nodes.new("GeometryNodeTransform")
    transform_geometry_019.name = "Transform Geometry.019"
    transform_geometry_019.label = ""
    transform_geometry_019.location = (2269.0, -355.7998046875)
    transform_geometry_019.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_019.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_019.inputs[2].default_value = Vector((0.0, -0.012000000104308128, 0.0))
    # Rotation
    transform_geometry_019.inputs[3].default_value = Euler((0.0, 0.0, 1.5707963705062866), 'XYZ')
    # Scale
    transform_geometry_019.inputs[4].default_value = Vector((0.30000001192092896, 0.6000000238418579, 1.0))
    # Links for transform_geometry_019
    links.new(transform_geometry_015.outputs[0], transform_geometry_019.inputs[0])
    links.new(transform_geometry_019.outputs[0], join_geometry_007.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_009.name = "Join Geometry.009"
    join_geometry_009.label = ""
    join_geometry_009.location = (1809.0, -95.7998046875)
    join_geometry_009.bl_label = "Join Geometry"
    # Links for join_geometry_009
    links.new(instance_on_points_004.outputs[0], join_geometry_009.inputs[0])
    links.new(set_position_004.outputs[0], join_geometry_009.inputs[0])

    store_named_attribute_005 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.name = "Store Named Attribute.005"
    store_named_attribute_005.label = ""
    store_named_attribute_005.location = (2889.0, -255.7998046875)
    store_named_attribute_005.bl_label = "Store Named Attribute"
    store_named_attribute_005.data_type = "BOOLEAN"
    store_named_attribute_005.domain = "POINT"
    # Selection
    store_named_attribute_005.inputs[1].default_value = True
    # Name
    store_named_attribute_005.inputs[2].default_value = "ruby"
    # Value
    store_named_attribute_005.inputs[3].default_value = True
    # Links for store_named_attribute_005

    join_geometry_010 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_010.name = "Join Geometry.010"
    join_geometry_010.label = ""
    join_geometry_010.location = (3109.0, -155.7998046875)
    join_geometry_010.bl_label = "Join Geometry"
    # Links for join_geometry_010
    links.new(store_named_attribute_005.outputs[0], join_geometry_010.inputs[0])

    store_named_attribute_006 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_006.name = "Store Named Attribute.006"
    store_named_attribute_006.label = ""
    store_named_attribute_006.location = (2889.0, -55.7998046875)
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
    links.new(store_named_attribute_006.outputs[0], join_geometry_010.inputs[0])

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Pendant"
    frame_004.location = (640.0, -1760.0)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.label = ""
    sample_curve.location = (3509.0, -1515.7998046875)
    sample_curve.bl_label = "Sample Curve"
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = True
    sample_curve.data_type = "FLOAT"
    # Value
    sample_curve.inputs[1].default_value = 0.0
    # Factor
    sample_curve.inputs[2].default_value = 0.6780651807785034
    # Length
    sample_curve.inputs[3].default_value = 0.0
    # Curve Index
    sample_curve.inputs[4].default_value = 0
    # Links for sample_curve
    links.new(set_curve_tilt_002.outputs[0], sample_curve.inputs[0])

    transform_geometry_020 = nodes.new("GeometryNodeTransform")
    transform_geometry_020.name = "Transform Geometry.020"
    transform_geometry_020.label = ""
    transform_geometry_020.location = (3949.0, -1515.7998046875)
    transform_geometry_020.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_020.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_020.inputs[3].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_020.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_020
    links.new(join_geometry_010.outputs[0], transform_geometry_020.inputs[0])

    join_geometry_011 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_011.name = "Join Geometry.011"
    join_geometry_011.label = ""
    join_geometry_011.location = (4229.0, -1015.7998046875)
    join_geometry_011.bl_label = "Join Geometry"
    # Links for join_geometry_011
    links.new(transform_geometry_020.outputs[0], join_geometry_011.inputs[0])
    links.new(instance_on_points_002.outputs[0], join_geometry_011.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (3669.0, -1515.7998046875)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "ADD"
    # Vector
    vector_math_003.inputs[1].default_value = [0.0, -0.003000000026077032, -0.019999999552965164]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(vector_math_003.outputs[0], transform_geometry_020.inputs[2])
    links.new(sample_curve.outputs[1], vector_math_003.inputs[0])

    float_curve_005 = nodes.new("ShaderNodeFloatCurve")
    float_curve_005.name = "Float Curve.005"
    float_curve_005.label = ""
    float_curve_005.location = (229.0, -1455.7998046875)
    float_curve_005.bl_label = "Float Curve"
    # Factor
    float_curve_005.inputs[0].default_value = 1.0
    # Links for float_curve_005

    spline_parameter_003 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_003.name = "Spline Parameter.003"
    spline_parameter_003.label = ""
    spline_parameter_003.location = (29.0, -1695.7998046875)
    spline_parameter_003.bl_label = "Spline Parameter"
    # Links for spline_parameter_003
    links.new(spline_parameter_003.outputs[0], float_curve_005.inputs[1])

    math_009 = nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.label = ""
    math_009.location = (609.0, -1435.7998046875)
    math_009.bl_label = "Math"
    math_009.operation = "MULTIPLY"
    math_009.use_clamp = False
    # Value
    math_009.inputs[1].default_value = -0.014999999664723873
    # Value
    math_009.inputs[2].default_value = 0.5
    # Links for math_009
    links.new(float_curve_005.outputs[0], math_009.inputs[0])

    math_010 = nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.label = ""
    math_010.location = (789.0, -1075.7998046875)
    math_010.bl_label = "Math"
    math_010.operation = "ADD"
    math_010.use_clamp = False
    # Value
    math_010.inputs[2].default_value = 0.5
    # Links for math_010
    links.new(math_010.outputs[0], combine_x_y_z_001.inputs[1])
    links.new(math_005.outputs[0], math_010.inputs[0])
    links.new(math_009.outputs[0], math_010.inputs[1])

    frame_018 = nodes.new("NodeFrame")
    frame_018.name = "Frame.018"
    frame_018.label = "Necklace 1"
    frame_018.location = (49.0, -35.798828125)
    frame_018.bl_label = "Frame"
    frame_018.text = None
    frame_018.shrink = True
    frame_018.label_size = 20
    # Links for frame_018

    curve_circle_004 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_004.name = "Curve Circle.004"
    curve_circle_004.label = ""
    curve_circle_004.location = (1229.0, -35.7998046875)
    curve_circle_004.bl_label = "Curve Circle"
    curve_circle_004.mode = "RADIUS"
    # Resolution
    curve_circle_004.inputs[0].default_value = 64
    # Point 1
    curve_circle_004.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_004.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_004.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_004.inputs[4].default_value = 0.12999999523162842
    # Links for curve_circle_004

    transform_geometry_021 = nodes.new("GeometryNodeTransform")
    transform_geometry_021.name = "Transform Geometry.021"
    transform_geometry_021.label = ""
    transform_geometry_021.location = (1949.0, -395.7998046875)
    transform_geometry_021.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_021.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_021.inputs[2].default_value = Vector((-0.009999999776482582, -0.03999999910593033, 0.46000000834465027))
    # Rotation
    transform_geometry_021.inputs[3].default_value = Euler((-0.027925267815589905, 0.0, -0.08691740036010742), 'XYZ')
    # Scale
    transform_geometry_021.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_021

    set_position_005 = nodes.new("GeometryNodeSetPosition")
    set_position_005.name = "Set Position.005"
    set_position_005.label = ""
    set_position_005.location = (1789.0, -395.7998046875)
    set_position_005.bl_label = "Set Position"
    # Selection
    set_position_005.inputs[1].default_value = True
    # Links for set_position_005
    links.new(curve_circle_004.outputs[0], set_position_005.inputs[0])
    links.new(set_position_005.outputs[0], transform_geometry_021.inputs[0])

    position_007 = nodes.new("GeometryNodeInputPosition")
    position_007.name = "Position.007"
    position_007.label = ""
    position_007.location = (629.0, -635.7998046875)
    position_007.bl_label = "Position"
    # Links for position_007

    separate_x_y_z_007 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_007.name = "Separate XYZ.007"
    separate_x_y_z_007.label = ""
    separate_x_y_z_007.location = (629.0, -695.7998046875)
    separate_x_y_z_007.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_007
    links.new(position_007.outputs[0], separate_x_y_z_007.inputs[0])

    map_range_004 = nodes.new("ShaderNodeMapRange")
    map_range_004.name = "Map Range.004"
    map_range_004.label = ""
    map_range_004.location = (789.0, -635.7998046875)
    map_range_004.bl_label = "Map Range"
    map_range_004.clamp = True
    map_range_004.interpolation_type = "LINEAR"
    map_range_004.data_type = "FLOAT"
    # From Min
    map_range_004.inputs[1].default_value = 0.12999999523162842
    # From Max
    map_range_004.inputs[2].default_value = -0.12999999523162842
    # To Min
    map_range_004.inputs[3].default_value = 0.0
    # To Max
    map_range_004.inputs[4].default_value = 1.0
    # Steps
    map_range_004.inputs[5].default_value = 4.0
    # Vector
    map_range_004.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_004.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_004.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_004.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_004.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_004.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_004
    links.new(separate_x_y_z_007.outputs[1], map_range_004.inputs[0])

    float_curve_006 = nodes.new("ShaderNodeFloatCurve")
    float_curve_006.name = "Float Curve.006"
    float_curve_006.label = ""
    float_curve_006.location = (969.0, -635.7998046875)
    float_curve_006.bl_label = "Float Curve"
    # Factor
    float_curve_006.inputs[0].default_value = 1.0
    # Links for float_curve_006
    links.new(map_range_004.outputs[0], float_curve_006.inputs[1])

    math_011 = nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.label = ""
    math_011.location = (1409.0, -655.7998046875)
    math_011.bl_label = "Math"
    math_011.operation = "MULTIPLY"
    math_011.use_clamp = False
    # Value
    math_011.inputs[1].default_value = -0.19999998807907104
    # Value
    math_011.inputs[2].default_value = 0.5
    # Links for math_011

    combine_x_y_z_004 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_004.name = "Combine XYZ.004"
    combine_x_y_z_004.label = ""
    combine_x_y_z_004.location = (1589.0, -675.7998046875)
    combine_x_y_z_004.bl_label = "Combine XYZ"
    # X
    combine_x_y_z_004.inputs[0].default_value = 0.0
    # Links for combine_x_y_z_004
    links.new(combine_x_y_z_004.outputs[0], set_position_005.inputs[3])
    links.new(math_011.outputs[0], combine_x_y_z_004.inputs[2])

    position_008 = nodes.new("GeometryNodeInputPosition")
    position_008.name = "Position.008"
    position_008.label = ""
    position_008.location = (1069.0, -155.7998046875)
    position_008.bl_label = "Position"
    # Links for position_008

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (1229.0, -155.7998046875)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "MULTIPLY"
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(position_008.outputs[0], vector_math_004.inputs[0])
    links.new(vector_math_004.outputs[0], set_position_005.inputs[2])

    combine_x_y_z_005 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_005.name = "Combine XYZ.005"
    combine_x_y_z_005.label = ""
    combine_x_y_z_005.location = (1229.0, -295.7998046875)
    combine_x_y_z_005.bl_label = "Combine XYZ"
    # Y
    combine_x_y_z_005.inputs[1].default_value = 1.0
    # Z
    combine_x_y_z_005.inputs[2].default_value = 1.0
    # Links for combine_x_y_z_005
    links.new(combine_x_y_z_005.outputs[0], vector_math_004.inputs[1])

    float_curve_007 = nodes.new("ShaderNodeFloatCurve")
    float_curve_007.name = "Float Curve.007"
    float_curve_007.label = ""
    float_curve_007.location = (969.0, -295.7998046875)
    float_curve_007.bl_label = "Float Curve"
    # Factor
    float_curve_007.inputs[0].default_value = 1.0
    # Links for float_curve_007
    links.new(map_range_004.outputs[0], float_curve_007.inputs[1])
    links.new(float_curve_007.outputs[0], combine_x_y_z_005.inputs[0])

    resample_curve_004 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_004.name = "Resample Curve.004"
    resample_curve_004.label = ""
    resample_curve_004.location = (2129.0, -395.7998046875)
    resample_curve_004.bl_label = "Resample Curve"
    resample_curve_004.keep_last_segment = True
    # Selection
    resample_curve_004.inputs[1].default_value = True
    # Mode
    resample_curve_004.inputs[2].default_value = "Length"
    # Count
    resample_curve_004.inputs[3].default_value = 10
    # Length
    resample_curve_004.inputs[4].default_value = 0.013799999840557575
    # Links for resample_curve_004
    links.new(transform_geometry_021.outputs[0], resample_curve_004.inputs[0])

    instance_on_points_005 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_005.name = "Instance on Points.005"
    instance_on_points_005.label = ""
    instance_on_points_005.location = (3229.0, -555.7998046875)
    instance_on_points_005.bl_label = "Instance on Points"
    # Selection
    instance_on_points_005.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_005.inputs[3].default_value = False
    # Instance Index
    instance_on_points_005.inputs[4].default_value = 0
    # Scale
    instance_on_points_005.inputs[6].default_value = Vector((0.699999988079071, 0.699999988079071, 0.699999988079071))
    # Links for instance_on_points_005

    align_rotation_to_vector_002 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.name = "Align Rotation to Vector.002"
    align_rotation_to_vector_002.label = ""
    align_rotation_to_vector_002.location = (29.0, -35.7998046875)
    align_rotation_to_vector_002.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_002.axis = "X"
    align_rotation_to_vector_002.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_002.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_002.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_002

    curve_tangent_002 = nodes.new("GeometryNodeInputTangent")
    curve_tangent_002.name = "Curve Tangent.002"
    curve_tangent_002.label = ""
    curve_tangent_002.location = (29.0, -195.7998046875)
    curve_tangent_002.bl_label = "Curve Tangent"
    # Links for curve_tangent_002
    links.new(curve_tangent_002.outputs[0], align_rotation_to_vector_002.inputs[2])

    align_rotation_to_vector_003 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_003.name = "Align Rotation to Vector.003"
    align_rotation_to_vector_003.label = ""
    align_rotation_to_vector_003.location = (189.0, -35.7998046875)
    align_rotation_to_vector_003.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_003.axis = "Y"
    align_rotation_to_vector_003.pivot_axis = "AUTO"
    # Factor
    align_rotation_to_vector_003.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_003
    links.new(align_rotation_to_vector_002.outputs[0], align_rotation_to_vector_003.inputs[0])

    normal_002 = nodes.new("GeometryNodeInputNormal")
    normal_002.name = "Normal.002"
    normal_002.label = ""
    normal_002.location = (189.0, -195.7998046875)
    normal_002.bl_label = "Normal"
    normal_002.legacy_corner_normals = False
    # Links for normal_002
    links.new(normal_002.outputs[0], align_rotation_to_vector_003.inputs[2])

    spline_parameter_004 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_004.name = "Spline Parameter.004"
    spline_parameter_004.label = ""
    spline_parameter_004.location = (1669.0, -55.7998046875)
    spline_parameter_004.bl_label = "Spline Parameter"
    # Links for spline_parameter_004

    math_012 = nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.label = ""
    math_012.location = (1849.0, -55.7998046875)
    math_012.bl_label = "Math"
    math_012.operation = "SUBTRACT"
    math_012.use_clamp = False
    # Value
    math_012.inputs[1].default_value = 0.7400000095367432
    # Value
    math_012.inputs[2].default_value = 0.5
    # Links for math_012
    links.new(spline_parameter_004.outputs[0], math_012.inputs[0])

    math_013 = nodes.new("ShaderNodeMath")
    math_013.name = "Math.013"
    math_013.label = ""
    math_013.location = (2029.0, -55.7998046875)
    math_013.bl_label = "Math"
    math_013.operation = "ABSOLUTE"
    math_013.use_clamp = False
    # Value
    math_013.inputs[1].default_value = 0.7400000095367432
    # Value
    math_013.inputs[2].default_value = 0.5
    # Links for math_013
    links.new(math_012.outputs[0], math_013.inputs[0])

    set_curve_tilt_003 = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_003.name = "Set Curve Tilt.003"
    set_curve_tilt_003.label = ""
    set_curve_tilt_003.location = (2589.0, -395.7998046875)
    set_curve_tilt_003.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt_003.inputs[1].default_value = True
    # Links for set_curve_tilt_003
    links.new(set_curve_tilt_003.outputs[0], instance_on_points_005.inputs[0])
    links.new(resample_curve_004.outputs[0], set_curve_tilt_003.inputs[0])

    map_range_005 = nodes.new("ShaderNodeMapRange")
    map_range_005.name = "Map Range.005"
    map_range_005.label = ""
    map_range_005.location = (2229.0, -75.7998046875)
    map_range_005.bl_label = "Map Range"
    map_range_005.clamp = True
    map_range_005.interpolation_type = "LINEAR"
    map_range_005.data_type = "FLOAT"
    # From Min
    map_range_005.inputs[1].default_value = 0.0
    # From Max
    map_range_005.inputs[2].default_value = 0.08000002801418304
    # To Min
    map_range_005.inputs[3].default_value = 0.6799999475479126
    # To Max
    map_range_005.inputs[4].default_value = 0.47999998927116394
    # Steps
    map_range_005.inputs[5].default_value = 4.0
    # Vector
    map_range_005.inputs[6].default_value = [0.0, 0.0, 0.0]
    # From Min
    map_range_005.inputs[7].default_value = [0.0, 0.0, 0.0]
    # From Max
    map_range_005.inputs[8].default_value = [1.0, 1.0, 1.0]
    # To Min
    map_range_005.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_005.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_005.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_005
    links.new(math_013.outputs[0], map_range_005.inputs[0])
    links.new(map_range_005.outputs[0], set_curve_tilt_003.inputs[2])

    float_curve_008 = nodes.new("ShaderNodeFloatCurve")
    float_curve_008.name = "Float Curve.008"
    float_curve_008.label = ""
    float_curve_008.location = (269.0, -1115.7998046875)
    float_curve_008.bl_label = "Float Curve"
    # Factor
    float_curve_008.inputs[0].default_value = 1.0
    # Links for float_curve_008

    spline_parameter_005 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_005.name = "Spline Parameter.005"
    spline_parameter_005.label = ""
    spline_parameter_005.location = (29.0, -1355.7998046875)
    spline_parameter_005.bl_label = "Spline Parameter"
    # Links for spline_parameter_005
    links.new(spline_parameter_005.outputs[0], float_curve_008.inputs[1])

    math_014 = nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.label = ""
    math_014.location = (609.0, -1095.7998046875)
    math_014.bl_label = "Math"
    math_014.operation = "MULTIPLY"
    math_014.use_clamp = False
    # Value
    math_014.inputs[1].default_value = 0.014999999664723873
    # Value
    math_014.inputs[2].default_value = 0.5
    # Links for math_014
    links.new(float_curve_008.outputs[0], math_014.inputs[0])

    frame_020 = nodes.new("NodeFrame")
    frame_020.name = "Frame.020"
    frame_020.label = "Align"
    frame_020.location = (2260.0, -520.0)
    frame_020.bl_label = "Frame"
    frame_020.text = None
    frame_020.shrink = True
    frame_020.label_size = 20
    # Links for frame_020

    math_015 = nodes.new("ShaderNodeMath")
    math_015.name = "Math.015"
    math_015.label = ""
    math_015.location = (1249.0, -655.7998046875)
    math_015.bl_label = "Math"
    math_015.operation = "ADD"
    math_015.use_clamp = False
    # Value
    math_015.inputs[2].default_value = 0.5
    # Links for math_015
    links.new(math_015.outputs[0], math_011.inputs[0])
    links.new(float_curve_006.outputs[0], math_015.inputs[0])

    spline_parameter_006 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_006.name = "Spline Parameter.006"
    spline_parameter_006.label = ""
    spline_parameter_006.location = (29.0, -935.7998046875)
    spline_parameter_006.bl_label = "Spline Parameter"
    # Links for spline_parameter_006

    float_curve_009 = nodes.new("ShaderNodeFloatCurve")
    float_curve_009.name = "Float Curve.009"
    float_curve_009.label = ""
    float_curve_009.location = (269.0, -795.7998046875)
    float_curve_009.bl_label = "Float Curve"
    # Factor
    float_curve_009.inputs[0].default_value = 1.0
    # Links for float_curve_009
    links.new(spline_parameter_006.outputs[0], float_curve_009.inputs[1])
    links.new(float_curve_009.outputs[0], math_015.inputs[1])

    float_curve_010 = nodes.new("ShaderNodeFloatCurve")
    float_curve_010.name = "Float Curve.010"
    float_curve_010.label = ""
    float_curve_010.location = (229.0, -1455.7998046875)
    float_curve_010.bl_label = "Float Curve"
    # Factor
    float_curve_010.inputs[0].default_value = 1.0
    # Links for float_curve_010

    spline_parameter_007 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_007.name = "Spline Parameter.007"
    spline_parameter_007.label = ""
    spline_parameter_007.location = (29.0, -1695.7998046875)
    spline_parameter_007.bl_label = "Spline Parameter"
    # Links for spline_parameter_007
    links.new(spline_parameter_007.outputs[0], float_curve_010.inputs[1])

    math_018 = nodes.new("ShaderNodeMath")
    math_018.name = "Math.018"
    math_018.label = ""
    math_018.location = (609.0, -1435.7998046875)
    math_018.bl_label = "Math"
    math_018.operation = "MULTIPLY"
    math_018.use_clamp = False
    # Value
    math_018.inputs[1].default_value = -0.014999999664723873
    # Value
    math_018.inputs[2].default_value = 0.5
    # Links for math_018
    links.new(float_curve_010.outputs[0], math_018.inputs[0])

    math_019 = nodes.new("ShaderNodeMath")
    math_019.name = "Math.019"
    math_019.label = ""
    math_019.location = (789.0, -1075.7998046875)
    math_019.bl_label = "Math"
    math_019.operation = "ADD"
    math_019.use_clamp = False
    # Value
    math_019.inputs[2].default_value = 0.5
    # Links for math_019
    links.new(math_019.outputs[0], combine_x_y_z_004.inputs[1])
    links.new(math_014.outputs[0], math_019.inputs[0])
    links.new(math_018.outputs[0], math_019.inputs[1])

    frame_022 = nodes.new("NodeFrame")
    frame_022.name = "Frame.022"
    frame_022.label = "Necklace 1"
    frame_022.location = (29.0, -3035.798828125)
    frame_022.bl_label = "Frame"
    frame_022.text = None
    frame_022.shrink = True
    frame_022.label_size = 20
    # Links for frame_022

    quadrilateral = nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
    quadrilateral.name = "Quadrilateral"
    quadrilateral.label = ""
    quadrilateral.location = (29.0, -35.7998046875)
    quadrilateral.bl_label = "Quadrilateral"
    quadrilateral.mode = "RECTANGLE"
    # Width
    quadrilateral.inputs[0].default_value = 0.02500000037252903
    # Height
    quadrilateral.inputs[1].default_value = 0.014999999664723873
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

    fillet_curve = nodes.new("GeometryNodeFilletCurve")
    fillet_curve.name = "Fillet Curve"
    fillet_curve.label = ""
    fillet_curve.location = (349.0, -35.7998046875)
    fillet_curve.bl_label = "Fillet Curve"
    # Radius
    fillet_curve.inputs[1].default_value = 0.007000000216066837
    # Limit Radius
    fillet_curve.inputs[2].default_value = True
    # Mode
    fillet_curve.inputs[3].default_value = "Bézier"
    # Count
    fillet_curve.inputs[4].default_value = 1
    # Links for fillet_curve

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.label = ""
    set_spline_type.location = (189.0, -35.7998046875)
    set_spline_type.bl_label = "Set Spline Type"
    set_spline_type.spline_type = "BEZIER"
    # Selection
    set_spline_type.inputs[1].default_value = True
    # Links for set_spline_type
    links.new(set_spline_type.outputs[0], fillet_curve.inputs[0])
    links.new(quadrilateral.outputs[0], set_spline_type.inputs[0])

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (509.0, -35.7998046875)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_001.inputs[2].default_value = 0.8519999980926514
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False
    # Links for curve_to_mesh_001
    links.new(fillet_curve.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(curve_to_mesh_001.outputs[0], instance_on_points_005.inputs[2])

    curve_circle_005 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_005.name = "Curve Circle.005"
    curve_circle_005.label = ""
    curve_circle_005.location = (349.0, -155.7998046875)
    curve_circle_005.bl_label = "Curve Circle"
    curve_circle_005.mode = "RADIUS"
    # Resolution
    curve_circle_005.inputs[0].default_value = 6
    # Point 1
    curve_circle_005.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_005.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_005.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_005.inputs[4].default_value = 0.003000000026077032
    # Links for curve_circle_005
    links.new(curve_circle_005.outputs[0], curve_to_mesh_001.inputs[1])

    frame_019 = nodes.new("NodeFrame")
    frame_019.name = "Frame.019"
    frame_019.label = "Link"
    frame_019.location = (2260.0, -980.0)
    frame_019.bl_label = "Frame"
    frame_019.text = None
    frame_019.shrink = True
    frame_019.label_size = 20
    # Links for frame_019

    rotate_rotation_006 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_006.name = "Rotate Rotation.006"
    rotate_rotation_006.label = ""
    rotate_rotation_006.location = (509.0, -35.7998046875)
    rotate_rotation_006.bl_label = "Rotate Rotation"
    rotate_rotation_006.rotation_space = "LOCAL"
    # Links for rotate_rotation_006
    links.new(rotate_rotation_006.outputs[0], instance_on_points_005.inputs[5])

    rotate_rotation_005 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_005.name = "Rotate Rotation.005"
    rotate_rotation_005.label = ""
    rotate_rotation_005.location = (349.0, -35.7998046875)
    rotate_rotation_005.bl_label = "Rotate Rotation"
    rotate_rotation_005.rotation_space = "LOCAL"
    # Links for rotate_rotation_005
    links.new(align_rotation_to_vector_003.outputs[0], rotate_rotation_005.inputs[0])
    links.new(rotate_rotation_005.outputs[0], rotate_rotation_006.inputs[0])

    random_value_012 = nodes.new("FunctionNodeRandomValue")
    random_value_012.name = "Random Value.012"
    random_value_012.label = ""
    random_value_012.location = (509.0, -135.7998046875)
    random_value_012.bl_label = "Random Value"
    random_value_012.data_type = "FLOAT_VECTOR"
    # Min
    random_value_012.inputs[0].default_value = [-0.29999998211860657, -0.09999999403953552, 0.0]
    # Max
    random_value_012.inputs[1].default_value = [0.2999999225139618, 0.09999999403953552, 0.0]
    # Min
    random_value_012.inputs[2].default_value = 0.0
    # Max
    random_value_012.inputs[3].default_value = 1.0
    # Min
    random_value_012.inputs[4].default_value = 0
    # Max
    random_value_012.inputs[5].default_value = 100
    # Probability
    random_value_012.inputs[6].default_value = 0.5
    # ID
    random_value_012.inputs[7].default_value = 0
    # Seed
    random_value_012.inputs[8].default_value = 3
    # Links for random_value_012
    links.new(random_value_012.outputs[0], rotate_rotation_006.inputs[1])

    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.label = ""
    index_001.location = (189.0, -275.7998046875)
    index_001.bl_label = "Index"
    # Links for index_001

    math_016 = nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.label = ""
    math_016.location = (189.0, -335.7998046875)
    math_016.bl_label = "Math"
    math_016.operation = "FLOORED_MODULO"
    math_016.use_clamp = False
    # Value
    math_016.inputs[1].default_value = 2.0
    # Value
    math_016.inputs[2].default_value = 0.5
    # Links for math_016
    links.new(index_001.outputs[0], math_016.inputs[0])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (349.0, -235.7998046875)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "FLOAT"
    # False
    switch_001.inputs[1].default_value = -0.3799999952316284
    # True
    switch_001.inputs[2].default_value = 0.5
    # Links for switch_001
    links.new(math_016.outputs[0], switch_001.inputs[0])

    combine_x_y_z_006 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_006.name = "Combine XYZ.006"
    combine_x_y_z_006.label = ""
    combine_x_y_z_006.location = (349.0, -155.7998046875)
    combine_x_y_z_006.bl_label = "Combine XYZ"
    # Y
    combine_x_y_z_006.inputs[1].default_value = 0.0
    # Z
    combine_x_y_z_006.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_006
    links.new(switch_001.outputs[0], combine_x_y_z_006.inputs[0])
    links.new(combine_x_y_z_006.outputs[0], rotate_rotation_005.inputs[1])

    join_geometry_012 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_012.name = "Join Geometry.012"
    join_geometry_012.label = ""
    join_geometry_012.location = (5258.0, -2831.5986328125)
    join_geometry_012.bl_label = "Join Geometry"
    # Links for join_geometry_012
    links.new(join_geometry_011.outputs[0], join_geometry_012.inputs[0])
    links.new(join_geometry_012.outputs[0], store_named_attribute.inputs[0])

    curve_circle_006 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_006.name = "Curve Circle.006"
    curve_circle_006.label = ""
    curve_circle_006.location = (29.0, -35.7998046875)
    curve_circle_006.bl_label = "Curve Circle"
    curve_circle_006.mode = "RADIUS"
    # Resolution
    curve_circle_006.inputs[0].default_value = 15
    # Point 1
    curve_circle_006.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_006.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_006.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_006.inputs[4].default_value = 0.009999999776482582
    # Links for curve_circle_006

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (289.0, -35.7998046875)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_002.inputs[2].default_value = 0.22200000286102295
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002
    links.new(curve_circle_006.outputs[0], curve_to_mesh_002.inputs[0])

    sample_curve_001 = nodes.new("GeometryNodeSampleCurve")
    sample_curve_001.name = "Sample Curve.001"
    sample_curve_001.label = ""
    sample_curve_001.location = (3089.0, -1175.7998046875)
    sample_curve_001.bl_label = "Sample Curve"
    sample_curve_001.mode = "FACTOR"
    sample_curve_001.use_all_curves = True
    sample_curve_001.data_type = "FLOAT"
    # Value
    sample_curve_001.inputs[1].default_value = 0.0
    # Factor
    sample_curve_001.inputs[2].default_value = 0.7185045480728149
    # Length
    sample_curve_001.inputs[3].default_value = 0.0
    # Curve Index
    sample_curve_001.inputs[4].default_value = 0
    # Links for sample_curve_001
    links.new(set_curve_tilt_003.outputs[0], sample_curve_001.inputs[0])

    transform_geometry_022 = nodes.new("GeometryNodeTransform")
    transform_geometry_022.name = "Transform Geometry.022"
    transform_geometry_022.label = ""
    transform_geometry_022.location = (3449.0, -1215.7998046875)
    transform_geometry_022.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_022.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_022.inputs[3].default_value = Euler((1.5707963705062866, 0.0, 0.34033918380737305), 'XYZ')
    # Scale
    transform_geometry_022.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_022
    links.new(curve_to_mesh_002.outputs[0], transform_geometry_022.inputs[0])

    join_geometry_013 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_013.name = "Join Geometry.013"
    join_geometry_013.label = ""
    join_geometry_013.location = (4109.0, -895.7998046875)
    join_geometry_013.bl_label = "Join Geometry"
    # Links for join_geometry_013
    links.new(instance_on_points_005.outputs[0], join_geometry_013.inputs[0])
    links.new(transform_geometry_022.outputs[0], join_geometry_013.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (3269.0, -1255.7998046875)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "ADD"
    # Vector
    vector_math_005.inputs[1].default_value = [0.0, 0.0, -0.012000000104308128]
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_005.inputs[3].default_value = 1.0
    # Links for vector_math_005
    links.new(vector_math_005.outputs[0], transform_geometry_022.inputs[2])
    links.new(sample_curve_001.outputs[1], vector_math_005.inputs[0])

    curve_circle_007 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_007.name = "Curve Circle.007"
    curve_circle_007.label = ""
    curve_circle_007.location = (29.0, -155.7998046875)
    curve_circle_007.bl_label = "Curve Circle"
    curve_circle_007.mode = "RADIUS"
    # Resolution
    curve_circle_007.inputs[0].default_value = 6
    # Point 1
    curve_circle_007.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_007.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_007.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_007.inputs[4].default_value = 0.009999999776482582
    # Links for curve_circle_007
    links.new(curve_circle_007.outputs[0], curve_to_mesh_002.inputs[1])

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.label = ""
    curve_line.location = (29.0, -555.7998046875)
    curve_line.bl_label = "Curve Line"
    curve_line.mode = "DIRECTION"
    # Start
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, -0.009999999776482582))
    # End
    curve_line.inputs[1].default_value = Vector((0.0, 0.0, 1.0))
    # Direction
    curve_line.inputs[2].default_value = [0.0, 0.0, -1.0]
    # Length
    curve_line.inputs[3].default_value = 0.05000000074505806
    # Links for curve_line

    transform_geometry_023 = nodes.new("GeometryNodeTransform")
    transform_geometry_023.name = "Transform Geometry.023"
    transform_geometry_023.label = ""
    transform_geometry_023.location = (4009.0, -1575.7998046875)
    transform_geometry_023.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_023.inputs[1].default_value = "Components"
    # Rotation
    transform_geometry_023.inputs[3].default_value = Euler((0.0, 0.06632250547409058, -0.6752678751945496), 'XYZ')
    # Scale
    transform_geometry_023.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_023
    links.new(transform_geometry_023.outputs[0], join_geometry_013.inputs[0])

    frame_021 = nodes.new("NodeFrame")
    frame_021.name = "Frame.021"
    frame_021.label = "Loop"
    frame_021.location = (2420.0, -1400.0)
    frame_021.bl_label = "Frame"
    frame_021.text = None
    frame_021.shrink = True
    frame_021.label_size = 20
    # Links for frame_021

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (3269.0, -1475.7998046875)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "ADD"
    # Vector
    vector_math_006.inputs[1].default_value = [0.0, 0.0, -0.017999999225139618]
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006
    links.new(vector_math_006.outputs[0], transform_geometry_023.inputs[2])
    links.new(vector_math_005.outputs[0], vector_math_006.inputs[0])

    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.name = "Curve to Mesh.003"
    curve_to_mesh_003.label = ""
    curve_to_mesh_003.location = (529.0, -535.7998046875)
    curve_to_mesh_003.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_003.inputs[3].default_value = True
    # Links for curve_to_mesh_003

    resample_curve_005 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_005.name = "Resample Curve.005"
    resample_curve_005.label = ""
    resample_curve_005.location = (209.0, -555.7998046875)
    resample_curve_005.bl_label = "Resample Curve"
    resample_curve_005.keep_last_segment = True
    # Selection
    resample_curve_005.inputs[1].default_value = True
    # Mode
    resample_curve_005.inputs[2].default_value = "Count"
    # Count
    resample_curve_005.inputs[3].default_value = 128
    # Length
    resample_curve_005.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_005
    links.new(resample_curve_005.outputs[0], curve_to_mesh_003.inputs[0])
    links.new(curve_line.outputs[0], resample_curve_005.inputs[0])

    curve_circle_008 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_008.name = "Curve Circle.008"
    curve_circle_008.label = ""
    curve_circle_008.location = (529.0, -675.7998046875)
    curve_circle_008.bl_label = "Curve Circle"
    curve_circle_008.mode = "RADIUS"
    # Resolution
    curve_circle_008.inputs[0].default_value = 32
    # Point 1
    curve_circle_008.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_008.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_008.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_008.inputs[4].default_value = 0.003000000026077032
    # Links for curve_circle_008
    links.new(curve_circle_008.outputs[0], curve_to_mesh_003.inputs[1])

    spline_parameter_008 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_008.name = "Spline Parameter.008"
    spline_parameter_008.label = ""
    spline_parameter_008.location = (29.0, -835.7998046875)
    spline_parameter_008.bl_label = "Spline Parameter"
    # Links for spline_parameter_008

    float_curve_011 = nodes.new("ShaderNodeFloatCurve")
    float_curve_011.name = "Float Curve.011"
    float_curve_011.label = ""
    float_curve_011.location = (209.0, -675.7998046875)
    float_curve_011.bl_label = "Float Curve"
    # Factor
    float_curve_011.inputs[0].default_value = 1.0
    # Links for float_curve_011
    links.new(spline_parameter_008.outputs[0], float_curve_011.inputs[1])
    links.new(float_curve_011.outputs[0], curve_to_mesh_003.inputs[2])

    curve_circle_009 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_009.name = "Curve Circle.009"
    curve_circle_009.label = ""
    curve_circle_009.location = (649.0, -35.7998046875)
    curve_circle_009.bl_label = "Curve Circle"
    curve_circle_009.mode = "RADIUS"
    # Resolution
    curve_circle_009.inputs[0].default_value = 12
    # Point 1
    curve_circle_009.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_009.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_009.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_009.inputs[4].default_value = 0.004000000189989805
    # Links for curve_circle_009

    curve_to_mesh_004 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_004.name = "Curve to Mesh.004"
    curve_to_mesh_004.label = ""
    curve_to_mesh_004.location = (829.0, -75.7998046875)
    curve_to_mesh_004.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_004.inputs[2].default_value = 0.800000011920929
    # Fill Caps
    curve_to_mesh_004.inputs[3].default_value = True
    # Links for curve_to_mesh_004
    links.new(curve_circle_009.outputs[0], curve_to_mesh_004.inputs[0])

    curve_circle_010 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_010.name = "Curve Circle.010"
    curve_circle_010.label = ""
    curve_circle_010.location = (649.0, -175.7998046875)
    curve_circle_010.bl_label = "Curve Circle"
    curve_circle_010.mode = "RADIUS"
    # Resolution
    curve_circle_010.inputs[0].default_value = 6
    # Point 1
    curve_circle_010.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_010.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_010.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_010.inputs[4].default_value = 0.0020000000949949026
    # Links for curve_circle_010
    links.new(curve_circle_010.outputs[0], curve_to_mesh_004.inputs[1])

    join_geometry_014 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_014.name = "Join Geometry.014"
    join_geometry_014.label = ""
    join_geometry_014.location = (2129.0, -255.7998046875)
    join_geometry_014.bl_label = "Join Geometry"
    # Links for join_geometry_014
    links.new(curve_to_mesh_003.outputs[0], join_geometry_014.inputs[0])
    links.new(join_geometry_014.outputs[0], transform_geometry_023.inputs[0])

    curve_circle_011 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_011.name = "Curve Circle.011"
    curve_circle_011.label = ""
    curve_circle_011.location = (649.0, -315.7998046875)
    curve_circle_011.bl_label = "Curve Circle"
    curve_circle_011.mode = "RADIUS"
    # Resolution
    curve_circle_011.inputs[0].default_value = 6
    # Point 1
    curve_circle_011.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_011.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_011.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_011.inputs[4].default_value = 0.00800000037997961
    # Links for curve_circle_011

    instance_on_points_006 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_006.name = "Instance on Points.006"
    instance_on_points_006.label = ""
    instance_on_points_006.location = (1009.0, -95.7998046875)
    instance_on_points_006.bl_label = "Instance on Points"
    # Selection
    instance_on_points_006.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_006.inputs[3].default_value = False
    # Instance Index
    instance_on_points_006.inputs[4].default_value = 0
    # Rotation
    instance_on_points_006.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_006.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_006
    links.new(curve_to_mesh_004.outputs[0], instance_on_points_006.inputs[2])
    links.new(curve_circle_011.outputs[0], instance_on_points_006.inputs[0])

    transform_geometry_024 = nodes.new("GeometryNodeTransform")
    transform_geometry_024.name = "Transform Geometry.024"
    transform_geometry_024.label = ""
    transform_geometry_024.location = (1189.0, -95.7998046875)
    transform_geometry_024.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_024.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_024.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_024.inputs[3].default_value = Euler((1.5707963705062866, 0.5235987901687622, 0.0), 'XYZ')
    # Scale
    transform_geometry_024.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_024
    links.new(instance_on_points_006.outputs[0], transform_geometry_024.inputs[0])
    links.new(transform_geometry_024.outputs[0], join_geometry_014.inputs[0])

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    grid.label = ""
    grid.location = (709.0, -635.7998046875)
    grid.bl_label = "Grid"
    # Size X
    grid.inputs[0].default_value = 0.014999999664723873
    # Size Y
    grid.inputs[1].default_value = 0.012000000104308128
    # Vertices X
    grid.inputs[2].default_value = 12
    # Vertices Y
    grid.inputs[3].default_value = 4
    # Links for grid

    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.label = ""
    delete_geometry_001.location = (889.0, -635.7998046875)
    delete_geometry_001.bl_label = "Delete Geometry"
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "FACE"
    # Links for delete_geometry_001
    links.new(grid.outputs[0], delete_geometry_001.inputs[0])

    random_value_013 = nodes.new("FunctionNodeRandomValue")
    random_value_013.name = "Random Value.013"
    random_value_013.label = ""
    random_value_013.location = (889.0, -755.7998046875)
    random_value_013.bl_label = "Random Value"
    random_value_013.data_type = "BOOLEAN"
    # Min
    random_value_013.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_013.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_013.inputs[2].default_value = 0.0
    # Max
    random_value_013.inputs[3].default_value = 1.0
    # Min
    random_value_013.inputs[4].default_value = 0
    # Max
    random_value_013.inputs[5].default_value = 100
    # Probability
    random_value_013.inputs[6].default_value = 0.2734806537628174
    # ID
    random_value_013.inputs[7].default_value = 0
    # Seed
    random_value_013.inputs[8].default_value = 78
    # Links for random_value_013
    links.new(random_value_013.outputs[3], delete_geometry_001.inputs[1])

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.label = ""
    extrude_mesh.location = (1069.0, -635.7998046875)
    extrude_mesh.bl_label = "Extrude Mesh"
    extrude_mesh.mode = "FACES"
    # Selection
    extrude_mesh.inputs[1].default_value = True
    # Offset
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.003000000026077032
    # Individual
    extrude_mesh.inputs[4].default_value = False
    # Links for extrude_mesh
    links.new(delete_geometry_001.outputs[0], extrude_mesh.inputs[0])

    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.name = "Flip Faces"
    flip_faces.label = ""
    flip_faces.location = (1069.0, -555.7998046875)
    flip_faces.bl_label = "Flip Faces"
    # Selection
    flip_faces.inputs[1].default_value = True
    # Links for flip_faces
    links.new(delete_geometry_001.outputs[0], flip_faces.inputs[0])

    join_geometry_015 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_015.name = "Join Geometry.015"
    join_geometry_015.label = ""
    join_geometry_015.location = (1229.0, -635.7998046875)
    join_geometry_015.bl_label = "Join Geometry"
    # Links for join_geometry_015
    links.new(extrude_mesh.outputs[0], join_geometry_015.inputs[0])
    links.new(flip_faces.outputs[0], join_geometry_015.inputs[0])

    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.label = ""
    merge_by_distance.location = (1409.0, -635.7998046875)
    merge_by_distance.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance.inputs[1].default_value = True
    # Mode
    merge_by_distance.inputs[2].default_value = "All"
    # Distance
    merge_by_distance.inputs[3].default_value = 9.999999747378752e-05
    # Links for merge_by_distance
    links.new(join_geometry_015.outputs[0], merge_by_distance.inputs[0])

    transform_geometry_025 = nodes.new("GeometryNodeTransform")
    transform_geometry_025.name = "Transform Geometry.025"
    transform_geometry_025.label = ""
    transform_geometry_025.location = (1769.0, -575.7998046875)
    transform_geometry_025.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_025.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_025.inputs[2].default_value = Vector((0.006000000052154064, 0.001500000013038516, -0.04999999701976776))
    # Rotation
    transform_geometry_025.inputs[3].default_value = Euler((1.5707963705062866, -1.5707963705062866, 0.0), 'XYZ')
    # Scale
    transform_geometry_025.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_025
    links.new(transform_geometry_025.outputs[0], join_geometry_014.inputs[0])

    subdivision_surface = nodes.new("GeometryNodeSubdivisionSurface")
    subdivision_surface.name = "Subdivision Surface"
    subdivision_surface.label = ""
    subdivision_surface.location = (1589.0, -635.7998046875)
    subdivision_surface.bl_label = "Subdivision Surface"
    # Level
    subdivision_surface.inputs[1].default_value = 1
    # Edge Crease
    subdivision_surface.inputs[2].default_value = 0.8063265681266785
    # Vertex Crease
    subdivision_surface.inputs[3].default_value = 0.0
    # Limit Surface
    subdivision_surface.inputs[4].default_value = True
    # UV Smooth
    subdivision_surface.inputs[5].default_value = "Keep Boundaries"
    # Boundary Smooth
    subdivision_surface.inputs[6].default_value = "All"
    # Links for subdivision_surface
    links.new(subdivision_surface.outputs[0], transform_geometry_025.inputs[0])
    links.new(merge_by_distance.outputs[0], subdivision_surface.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.name = "Set Shade Smooth.001"
    set_shade_smooth_001.label = ""
    set_shade_smooth_001.location = (4309.0, -915.7998046875)
    set_shade_smooth_001.bl_label = "Set Shade Smooth"
    set_shade_smooth_001.domain = "FACE"
    # Selection
    set_shade_smooth_001.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_001.inputs[2].default_value = True
    # Links for set_shade_smooth_001
    links.new(join_geometry_013.outputs[0], set_shade_smooth_001.inputs[0])

    frame_023 = nodes.new("NodeFrame")
    frame_023.name = "Frame.023"
    frame_023.label = "Key"
    frame_023.location = (1520.0, -1820.0)
    frame_023.bl_label = "Frame"
    frame_023.text = None
    frame_023.shrink = True
    frame_023.label_size = 20
    # Links for frame_023

    store_named_attribute_007 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_007.name = "Store Named Attribute.007"
    store_named_attribute_007.label = ""
    store_named_attribute_007.location = (4469.0, -895.7998046875)
    store_named_attribute_007.bl_label = "Store Named Attribute"
    store_named_attribute_007.data_type = "BOOLEAN"
    store_named_attribute_007.domain = "POINT"
    # Selection
    store_named_attribute_007.inputs[1].default_value = True
    # Name
    store_named_attribute_007.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_007.inputs[3].default_value = True
    # Links for store_named_attribute_007
    links.new(store_named_attribute_007.outputs[0], join_geometry_012.inputs[0])
    links.new(set_shade_smooth_001.outputs[0], store_named_attribute_007.inputs[0])

    frame_024 = nodes.new("NodeFrame")
    frame_024.name = "Frame.024"
    frame_024.label = "Necklaces"
    frame_024.location = (1062.0, 14831.5986328125)
    frame_024.bl_label = "Frame"
    frame_024.text = None
    frame_024.shrink = True
    frame_024.label_size = 20
    # Links for frame_024

    ico_sphere_006 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_006.name = "Ico Sphere.006"
    ico_sphere_006.label = ""
    ico_sphere_006.location = (29.0, -1295.80029296875)
    ico_sphere_006.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_006.inputs[0].default_value = 0.029999999329447746
    # Subdivisions
    ico_sphere_006.inputs[1].default_value = 3
    # Links for ico_sphere_006

    transform_geometry_026 = nodes.new("GeometryNodeTransform")
    transform_geometry_026.name = "Transform Geometry.026"
    transform_geometry_026.label = ""
    transform_geometry_026.location = (209.0, -1295.80029296875)
    transform_geometry_026.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_026.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_026.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_026.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_026.inputs[4].default_value = Vector((1.0, 1.0, 0.5))
    # Links for transform_geometry_026
    links.new(ico_sphere_006.outputs[0], transform_geometry_026.inputs[0])

    instance_on_points_007 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_007.name = "Instance on Points.007"
    instance_on_points_007.label = ""
    instance_on_points_007.location = (389.0, -1195.80029296875)
    instance_on_points_007.bl_label = "Instance on Points"
    # Selection
    instance_on_points_007.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_007.inputs[3].default_value = False
    # Instance Index
    instance_on_points_007.inputs[4].default_value = 0
    # Rotation
    instance_on_points_007.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_007.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_007
    links.new(transform_geometry_026.outputs[0], instance_on_points_007.inputs[2])

    quadratic_bézier = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier.name = "Quadratic Bézier"
    quadratic_bézier.label = ""
    quadratic_bézier.location = (29.0, -975.80029296875)
    quadratic_bézier.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier.inputs[0].default_value = 16
    # Start
    quadratic_bézier.inputs[1].default_value = Vector((-0.019999999552965164, 0.0, 0.0))
    # Middle
    quadratic_bézier.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.009999999776482582))
    # End
    quadratic_bézier.inputs[3].default_value = Vector((0.019999999552965164, 0.0, 0.0))
    # Links for quadratic_bézier
    links.new(quadratic_bézier.outputs[0], instance_on_points_007.inputs[0])

    realize_instances_003 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.name = "Realize Instances.003"
    realize_instances_003.label = ""
    realize_instances_003.location = (569.0, -1195.80029296875)
    realize_instances_003.bl_label = "Realize Instances"
    # Selection
    realize_instances_003.inputs[1].default_value = True
    # Realize All
    realize_instances_003.inputs[2].default_value = True
    # Depth
    realize_instances_003.inputs[3].default_value = 0
    # Links for realize_instances_003
    links.new(instance_on_points_007.outputs[0], realize_instances_003.inputs[0])

    mesh_to_s_d_f_grid = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid.name = "Mesh to SDF Grid"
    mesh_to_s_d_f_grid.label = ""
    mesh_to_s_d_f_grid.location = (729.0, -1195.80029296875)
    mesh_to_s_d_f_grid.bl_label = "Mesh to SDF Grid"
    # Voxel Size
    mesh_to_s_d_f_grid.inputs[1].default_value = 0.009999999776482582
    # Band Width
    mesh_to_s_d_f_grid.inputs[2].default_value = 1
    # Links for mesh_to_s_d_f_grid
    links.new(realize_instances_003.outputs[0], mesh_to_s_d_f_grid.inputs[0])

    grid_to_mesh = nodes.new("GeometryNodeGridToMesh")
    grid_to_mesh.name = "Grid to Mesh"
    grid_to_mesh.label = ""
    grid_to_mesh.location = (1089.0, -1195.80029296875)
    grid_to_mesh.bl_label = "Grid to Mesh"
    # Threshold
    grid_to_mesh.inputs[1].default_value = 0.0
    # Adaptivity
    grid_to_mesh.inputs[2].default_value = 0.0
    # Links for grid_to_mesh

    dual_mesh_001 = nodes.new("GeometryNodeDualMesh")
    dual_mesh_001.name = "Dual Mesh.001"
    dual_mesh_001.label = ""
    dual_mesh_001.location = (1409.0, -1195.80029296875)
    dual_mesh_001.bl_label = "Dual Mesh"
    # Keep Boundaries
    dual_mesh_001.inputs[1].default_value = False
    # Links for dual_mesh_001

    triangulate = nodes.new("GeometryNodeTriangulate")
    triangulate.name = "Triangulate"
    triangulate.label = ""
    triangulate.location = (1249.0, -1195.80029296875)
    triangulate.bl_label = "Triangulate"
    # Selection
    triangulate.inputs[1].default_value = True
    # Quad Method
    triangulate.inputs[2].default_value = "Shortest Diagonal"
    # N-gon Method
    triangulate.inputs[3].default_value = "Beauty"
    # Links for triangulate
    links.new(triangulate.outputs[0], dual_mesh_001.inputs[0])
    links.new(grid_to_mesh.outputs[0], triangulate.inputs[0])

    s_d_f_grid_boolean = nodes.new("GeometryNodeSDFGridBoolean")
    s_d_f_grid_boolean.name = "SDF Grid Boolean"
    s_d_f_grid_boolean.label = ""
    s_d_f_grid_boolean.location = (909.0, -1195.80029296875)
    s_d_f_grid_boolean.bl_label = "SDF Grid Boolean"
    s_d_f_grid_boolean.operation = "INTERSECT"
    # Grid 1
    s_d_f_grid_boolean.inputs[0].default_value = 0.0
    # Links for s_d_f_grid_boolean
    links.new(s_d_f_grid_boolean.outputs[0], grid_to_mesh.inputs[0])
    links.new(mesh_to_s_d_f_grid.outputs[0], s_d_f_grid_boolean.inputs[1])

    cube = nodes.new("GeometryNodeMeshCube")
    cube.name = "Cube"
    cube.label = ""
    cube.location = (409.0, -1535.80029296875)
    cube.bl_label = "Cube"
    # Size
    cube.inputs[0].default_value = Vector((1.0, 1.0, 0.019999999552965164))
    # Vertices X
    cube.inputs[1].default_value = 2
    # Vertices Y
    cube.inputs[2].default_value = 2
    # Vertices Z
    cube.inputs[3].default_value = 2
    # Links for cube

    mesh_to_s_d_f_grid_001 = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid_001.name = "Mesh to SDF Grid.001"
    mesh_to_s_d_f_grid_001.label = ""
    mesh_to_s_d_f_grid_001.location = (769.0, -1355.80029296875)
    mesh_to_s_d_f_grid_001.bl_label = "Mesh to SDF Grid"
    # Voxel Size
    mesh_to_s_d_f_grid_001.inputs[1].default_value = 0.009999999776482582
    # Band Width
    mesh_to_s_d_f_grid_001.inputs[2].default_value = 1
    # Links for mesh_to_s_d_f_grid_001
    links.new(mesh_to_s_d_f_grid_001.outputs[0], s_d_f_grid_boolean.inputs[1])

    transform_geometry_027 = nodes.new("GeometryNodeTransform")
    transform_geometry_027.name = "Transform Geometry.027"
    transform_geometry_027.label = ""
    transform_geometry_027.location = (569.0, -1515.80029296875)
    transform_geometry_027.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_027.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_027.inputs[2].default_value = Vector((0.0, 0.0, 0.009999999776482582))
    # Rotation
    transform_geometry_027.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_027.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_027
    links.new(cube.outputs[0], transform_geometry_027.inputs[0])
    links.new(transform_geometry_027.outputs[0], mesh_to_s_d_f_grid_001.inputs[0])

    mesh_boolean = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean.name = "Mesh Boolean"
    mesh_boolean.label = ""
    mesh_boolean.location = (1589.0, -1195.80029296875)
    mesh_boolean.bl_label = "Mesh Boolean"
    mesh_boolean.operation = "DIFFERENCE"
    mesh_boolean.solver = "MANIFOLD"
    # Self Intersection
    mesh_boolean.inputs[2].default_value = False
    # Hole Tolerant
    mesh_boolean.inputs[3].default_value = False
    # Links for mesh_boolean
    links.new(dual_mesh_001.outputs[0], mesh_boolean.inputs[0])

    cube_001 = nodes.new("GeometryNodeMeshCube")
    cube_001.name = "Cube.001"
    cube_001.label = ""
    cube_001.location = (1249.0, -1335.80029296875)
    cube_001.bl_label = "Cube"
    # Size
    cube_001.inputs[0].default_value = Vector((1.0, 1.0, 1.0))
    # Vertices X
    cube_001.inputs[1].default_value = 2
    # Vertices Y
    cube_001.inputs[2].default_value = 2
    # Vertices Z
    cube_001.inputs[3].default_value = 2
    # Links for cube_001

    transform_geometry_028 = nodes.new("GeometryNodeTransform")
    transform_geometry_028.name = "Transform Geometry.028"
    transform_geometry_028.label = ""
    transform_geometry_028.location = (1409.0, -1335.80029296875)
    transform_geometry_028.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_028.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_028.inputs[2].default_value = Vector((0.5, 0.0, 0.0))
    # Rotation
    transform_geometry_028.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_028.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_028
    links.new(cube_001.outputs[0], transform_geometry_028.inputs[0])
    links.new(transform_geometry_028.outputs[0], mesh_boolean.inputs[1])

    delete_geometry_002 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.name = "Delete Geometry.002"
    delete_geometry_002.label = ""
    delete_geometry_002.location = (1769.0, -1195.80029296875)
    delete_geometry_002.bl_label = "Delete Geometry"
    delete_geometry_002.mode = "ALL"
    delete_geometry_002.domain = "FACE"
    # Links for delete_geometry_002
    links.new(mesh_boolean.outputs[0], delete_geometry_002.inputs[0])
    links.new(mesh_boolean.outputs[1], delete_geometry_002.inputs[1])

    mesh_boolean_001 = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean_001.name = "Mesh Boolean.001"
    mesh_boolean_001.label = ""
    mesh_boolean_001.location = (1449.0, -195.80029296875)
    mesh_boolean_001.bl_label = "Mesh Boolean"
    mesh_boolean_001.operation = "INTERSECT"
    mesh_boolean_001.solver = "MANIFOLD"
    # Self Intersection
    mesh_boolean_001.inputs[2].default_value = False
    # Hole Tolerant
    mesh_boolean_001.inputs[3].default_value = False
    # Links for mesh_boolean_001
    links.new(dual_mesh_001.outputs[0], mesh_boolean_001.inputs[1])

    cube_002 = nodes.new("GeometryNodeMeshCube")
    cube_002.name = "Cube.002"
    cube_002.label = ""
    cube_002.location = (1089.0, -55.80029296875)
    cube_002.bl_label = "Cube"
    # Size
    cube_002.inputs[0].default_value = Vector((1.0, 1.0, 0.0010000000474974513))
    # Vertices X
    cube_002.inputs[1].default_value = 2
    # Vertices Y
    cube_002.inputs[2].default_value = 2
    # Vertices Z
    cube_002.inputs[3].default_value = 2
    # Links for cube_002

    transform_geometry_029 = nodes.new("GeometryNodeTransform")
    transform_geometry_029.name = "Transform Geometry.029"
    transform_geometry_029.label = ""
    transform_geometry_029.location = (1249.0, -55.80029296875)
    transform_geometry_029.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_029.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_029.inputs[2].default_value = Vector((0.0, 0.0, 0.004000000189989805))
    # Rotation
    transform_geometry_029.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_029.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_029
    links.new(cube_002.outputs[0], transform_geometry_029.inputs[0])
    links.new(transform_geometry_029.outputs[0], mesh_boolean_001.inputs[1])

    join_geometry_016 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_016.name = "Join Geometry.016"
    join_geometry_016.label = ""
    join_geometry_016.location = (5609.0, -795.80029296875)
    join_geometry_016.bl_label = "Join Geometry"
    # Links for join_geometry_016

    delete_geometry_003 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_003.name = "Delete Geometry.003"
    delete_geometry_003.label = ""
    delete_geometry_003.location = (1969.0, -175.80029296875)
    delete_geometry_003.bl_label = "Delete Geometry"
    delete_geometry_003.mode = "ALL"
    delete_geometry_003.domain = "POINT"
    # Links for delete_geometry_003
    links.new(mesh_boolean_001.outputs[0], delete_geometry_003.inputs[0])

    normal_003 = nodes.new("GeometryNodeInputNormal")
    normal_003.name = "Normal.003"
    normal_003.label = ""
    normal_003.location = (1629.0, -275.80029296875)
    normal_003.bl_label = "Normal"
    normal_003.legacy_corner_normals = False
    # Links for normal_003

    compare_008 = nodes.new("FunctionNodeCompare")
    compare_008.name = "Compare.008"
    compare_008.label = ""
    compare_008.location = (1789.0, -275.80029296875)
    compare_008.bl_label = "Compare"
    compare_008.operation = "EQUAL"
    compare_008.data_type = "VECTOR"
    compare_008.mode = "DIRECTION"
    # A
    compare_008.inputs[0].default_value = 0.0
    # B
    compare_008.inputs[1].default_value = 0.0
    # A
    compare_008.inputs[2].default_value = 0
    # B
    compare_008.inputs[3].default_value = 0
    # B
    compare_008.inputs[5].default_value = [0.0, 0.0, 1.0]
    # A
    compare_008.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_008.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_008.inputs[8].default_value = ""
    # B
    compare_008.inputs[9].default_value = ""
    # C
    compare_008.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_008.inputs[11].default_value = 0.0
    # Epsilon
    compare_008.inputs[12].default_value = 1.5707963705062866
    # Links for compare_008
    links.new(normal_003.outputs[0], compare_008.inputs[4])
    links.new(compare_008.outputs[0], delete_geometry_003.inputs[1])

    mesh_to_curve_003 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_003.name = "Mesh to Curve.003"
    mesh_to_curve_003.label = ""
    mesh_to_curve_003.location = (2129.0, -175.80029296875)
    mesh_to_curve_003.bl_label = "Mesh to Curve"
    mesh_to_curve_003.mode = "EDGES"
    # Selection
    mesh_to_curve_003.inputs[1].default_value = True
    # Links for mesh_to_curve_003
    links.new(delete_geometry_003.outputs[0], mesh_to_curve_003.inputs[0])

    resample_curve_006 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_006.name = "Resample Curve.006"
    resample_curve_006.label = ""
    resample_curve_006.location = (3809.0, -35.80029296875)
    resample_curve_006.bl_label = "Resample Curve"
    resample_curve_006.keep_last_segment = True
    # Selection
    resample_curve_006.inputs[1].default_value = True
    # Mode
    resample_curve_006.inputs[2].default_value = "Count"
    # Count
    resample_curve_006.inputs[3].default_value = 45
    # Length
    resample_curve_006.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_006

    set_spline_cyclic_002 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_002.name = "Set Spline Cyclic.002"
    set_spline_cyclic_002.label = ""
    set_spline_cyclic_002.location = (3649.0, -35.80029296875)
    set_spline_cyclic_002.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic_002.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic_002.inputs[2].default_value = True
    # Links for set_spline_cyclic_002
    links.new(set_spline_cyclic_002.outputs[0], resample_curve_006.inputs[0])

    curve_to_mesh_005 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_005.name = "Curve to Mesh.005"
    curve_to_mesh_005.label = ""
    curve_to_mesh_005.location = (3969.0, -35.80029296875)
    curve_to_mesh_005.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_005.inputs[2].default_value = 0.009999999776482582
    # Fill Caps
    curve_to_mesh_005.inputs[3].default_value = False
    # Links for curve_to_mesh_005
    links.new(curve_to_mesh_005.outputs[0], join_geometry_016.inputs[0])
    links.new(resample_curve_006.outputs[0], curve_to_mesh_005.inputs[0])

    gem_in_holder_3 = nodes.new("GeometryNodeGroup")
    gem_in_holder_3.name = "Gem in Holder.003"
    gem_in_holder_3.label = ""
    gem_in_holder_3.location = (3809.0, -155.80029296875)
    gem_in_holder_3.node_tree = create_gem_in__holder_group()
    gem_in_holder_3.bl_label = "Group"
    # Gem Radius
    gem_in_holder_3.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_3.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_3.inputs[2].default_value = False
    # Scale
    gem_in_holder_3.inputs[3].default_value = 0.004999995231628418
    # Count
    gem_in_holder_3.inputs[4].default_value = 6
    # Seed
    gem_in_holder_3.inputs[5].default_value = 41
    # Wings
    gem_in_holder_3.inputs[6].default_value = False
    # Array Count
    gem_in_holder_3.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_3.inputs[8].default_value = 10
    # Split
    gem_in_holder_3.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder_3.inputs[10].default_value = 3.3099989891052246
    # Links for gem_in_holder_3
    links.new(gem_in_holder_3.outputs[1], curve_to_mesh_005.inputs[1])

    trim_curve_005 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_005.name = "Trim Curve.005"
    trim_curve_005.label = ""
    trim_curve_005.location = (2289.0, -175.80029296875)
    trim_curve_005.bl_label = "Trim Curve"
    trim_curve_005.mode = "FACTOR"
    # Selection
    trim_curve_005.inputs[1].default_value = True
    # Start
    trim_curve_005.inputs[2].default_value = 0.010773210786283016
    # End
    trim_curve_005.inputs[3].default_value = 0.9906079769134521
    # Start
    trim_curve_005.inputs[4].default_value = 0.0
    # End
    trim_curve_005.inputs[5].default_value = 1.0
    # Links for trim_curve_005
    links.new(mesh_to_curve_003.outputs[0], trim_curve_005.inputs[0])

    instance_on_points_008 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_008.name = "Instance on Points.008"
    instance_on_points_008.label = ""
    instance_on_points_008.location = (4689.0, -655.80029296875)
    instance_on_points_008.bl_label = "Instance on Points"
    # Selection
    instance_on_points_008.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_008.inputs[3].default_value = False
    # Instance Index
    instance_on_points_008.inputs[4].default_value = 0
    # Links for instance_on_points_008

    resample_curve_007 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_007.name = "Resample Curve.007"
    resample_curve_007.label = ""
    resample_curve_007.location = (4529.0, -655.80029296875)
    resample_curve_007.bl_label = "Resample Curve"
    resample_curve_007.keep_last_segment = True
    # Selection
    resample_curve_007.inputs[1].default_value = True
    # Mode
    resample_curve_007.inputs[2].default_value = "Count"
    # Count
    resample_curve_007.inputs[3].default_value = 10
    # Length
    resample_curve_007.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_007
    links.new(resample_curve_007.outputs[0], instance_on_points_008.inputs[0])

    align_rotation_to_vector_004 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_004.name = "Align Rotation to Vector.004"
    align_rotation_to_vector_004.label = ""
    align_rotation_to_vector_004.location = (4529.0, -775.80029296875)
    align_rotation_to_vector_004.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_004.axis = "Y"
    align_rotation_to_vector_004.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_004.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_004.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_004
    links.new(align_rotation_to_vector_004.outputs[0], instance_on_points_008.inputs[5])

    curve_tangent_003 = nodes.new("GeometryNodeInputTangent")
    curve_tangent_003.name = "Curve Tangent.003"
    curve_tangent_003.label = ""
    curve_tangent_003.location = (4529.0, -935.80029296875)
    curve_tangent_003.bl_label = "Curve Tangent"
    # Links for curve_tangent_003
    links.new(curve_tangent_003.outputs[0], align_rotation_to_vector_004.inputs[2])

    realize_instances_004 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_004.name = "Realize Instances.004"
    realize_instances_004.label = ""
    realize_instances_004.location = (5029.0, -815.80029296875)
    realize_instances_004.bl_label = "Realize Instances"
    # Selection
    realize_instances_004.inputs[1].default_value = True
    # Realize All
    realize_instances_004.inputs[2].default_value = True
    # Depth
    realize_instances_004.inputs[3].default_value = 0
    # Links for realize_instances_004
    links.new(instance_on_points_008.outputs[0], realize_instances_004.inputs[0])

    transform_geometry_030 = nodes.new("GeometryNodeTransform")
    transform_geometry_030.name = "Transform Geometry.030"
    transform_geometry_030.label = ""
    transform_geometry_030.location = (1949.0, -1295.80029296875)
    transform_geometry_030.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_030.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_030.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_030.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_030.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    # Links for transform_geometry_030
    links.new(delete_geometry_002.outputs[0], transform_geometry_030.inputs[0])

    flip_faces_002 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.name = "Flip Faces.002"
    flip_faces_002.label = ""
    flip_faces_002.location = (2109.0, -1295.80029296875)
    flip_faces_002.bl_label = "Flip Faces"
    # Selection
    flip_faces_002.inputs[1].default_value = True
    # Links for flip_faces_002
    links.new(transform_geometry_030.outputs[0], flip_faces_002.inputs[0])

    join_geometry_018 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_018.name = "Join Geometry.018"
    join_geometry_018.label = ""
    join_geometry_018.location = (2269.0, -1235.80029296875)
    join_geometry_018.bl_label = "Join Geometry"
    # Links for join_geometry_018
    links.new(delete_geometry_002.outputs[0], join_geometry_018.inputs[0])
    links.new(flip_faces_002.outputs[0], join_geometry_018.inputs[0])

    merge_by_distance_001 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_001.name = "Merge by Distance.001"
    merge_by_distance_001.label = ""
    merge_by_distance_001.location = (2449.0, -1235.80029296875)
    merge_by_distance_001.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_001.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_001.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_001
    links.new(join_geometry_018.outputs[0], merge_by_distance_001.inputs[0])

    is_edge_boundary_1 = nodes.new("GeometryNodeGroup")
    is_edge_boundary_1.name = "Is Edge Boundary.001"
    is_edge_boundary_1.label = ""
    is_edge_boundary_1.location = (2269.0, -1315.80029296875)
    is_edge_boundary_1.node_tree = create_is__edge__boundary_group()
    is_edge_boundary_1.bl_label = "Group"
    # Links for is_edge_boundary_1
    links.new(is_edge_boundary_1.outputs[0], merge_by_distance_001.inputs[1])

    spline_parameter_009 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_009.name = "Spline Parameter.009"
    spline_parameter_009.label = ""
    spline_parameter_009.location = (3809.0, -1035.80029296875)
    spline_parameter_009.bl_label = "Spline Parameter"
    # Links for spline_parameter_009

    math_020 = nodes.new("ShaderNodeMath")
    math_020.name = "Math.020"
    math_020.label = ""
    math_020.location = (3969.0, -1035.80029296875)
    math_020.bl_label = "Math"
    math_020.operation = "MULTIPLY"
    math_020.use_clamp = False
    # Value
    math_020.inputs[1].default_value = 2.0
    # Value
    math_020.inputs[2].default_value = 0.5
    # Links for math_020
    links.new(spline_parameter_009.outputs[0], math_020.inputs[0])

    math_021 = nodes.new("ShaderNodeMath")
    math_021.name = "Math.021"
    math_021.label = ""
    math_021.location = (4129.0, -1035.80029296875)
    math_021.bl_label = "Math"
    math_021.operation = "PINGPONG"
    math_021.use_clamp = False
    # Value
    math_021.inputs[1].default_value = 1.0
    # Value
    math_021.inputs[2].default_value = 0.5
    # Links for math_021
    links.new(math_020.outputs[0], math_021.inputs[0])

    curve_to_points_002 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_002.name = "Curve to Points.002"
    curve_to_points_002.label = ""
    curve_to_points_002.location = (2449.0, -175.80029296875)
    curve_to_points_002.bl_label = "Curve to Points"
    curve_to_points_002.mode = "EVALUATED"
    # Count
    curve_to_points_002.inputs[1].default_value = 10
    # Length
    curve_to_points_002.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points_002
    links.new(trim_curve_005.outputs[0], curve_to_points_002.inputs[0])

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    points_to_curves.label = ""
    points_to_curves.location = (2609.0, -175.80029296875)
    points_to_curves.bl_label = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0
    # Links for points_to_curves
    links.new(curve_to_points_002.outputs[0], points_to_curves.inputs[0])
    links.new(points_to_curves.outputs[0], set_spline_cyclic_002.inputs[0])

    gradient_texture = nodes.new("ShaderNodeTexGradient")
    gradient_texture.name = "Gradient Texture"
    gradient_texture.label = ""
    gradient_texture.location = (2129.0, -355.80029296875)
    gradient_texture.bl_label = "Gradient Texture"
    gradient_texture.gradient_type = "RADIAL"
    # Vector
    gradient_texture.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Links for gradient_texture

    math_022 = nodes.new("ShaderNodeMath")
    math_022.name = "Math.022"
    math_022.label = ""
    math_022.location = (2289.0, -355.80029296875)
    math_022.bl_label = "Math"
    math_022.operation = "ADD"
    math_022.use_clamp = False
    # Value
    math_022.inputs[1].default_value = 0.5
    # Value
    math_022.inputs[2].default_value = 0.5
    # Links for math_022
    links.new(gradient_texture.outputs[1], math_022.inputs[0])

    math_023 = nodes.new("ShaderNodeMath")
    math_023.name = "Math.023"
    math_023.label = ""
    math_023.location = (2449.0, -355.80029296875)
    math_023.bl_label = "Math"
    math_023.operation = "FRACT"
    math_023.use_clamp = False
    # Value
    math_023.inputs[1].default_value = 0.5
    # Value
    math_023.inputs[2].default_value = 0.5
    # Links for math_023
    links.new(math_023.outputs[0], points_to_curves.inputs[2])
    links.new(math_022.outputs[0], math_023.inputs[0])

    delete_geometry_004 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_004.name = "Delete Geometry.004"
    delete_geometry_004.label = ""
    delete_geometry_004.location = (3149.0, -335.80029296875)
    delete_geometry_004.bl_label = "Delete Geometry"
    delete_geometry_004.mode = "ALL"
    delete_geometry_004.domain = "POINT"
    # Links for delete_geometry_004
    links.new(delete_geometry_004.outputs[0], resample_curve_007.inputs[0])
    links.new(points_to_curves.outputs[0], delete_geometry_004.inputs[0])

    position_009 = nodes.new("GeometryNodeInputPosition")
    position_009.name = "Position.009"
    position_009.label = ""
    position_009.location = (2689.0, -415.80029296875)
    position_009.bl_label = "Position"
    # Links for position_009

    separate_x_y_z_008 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_008.name = "Separate XYZ.008"
    separate_x_y_z_008.label = ""
    separate_x_y_z_008.location = (2689.0, -475.80029296875)
    separate_x_y_z_008.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_008
    links.new(position_009.outputs[0], separate_x_y_z_008.inputs[0])

    compare_009 = nodes.new("FunctionNodeCompare")
    compare_009.name = "Compare.009"
    compare_009.label = ""
    compare_009.location = (2849.0, -415.80029296875)
    compare_009.bl_label = "Compare"
    compare_009.operation = "GREATER_THAN"
    compare_009.data_type = "FLOAT"
    compare_009.mode = "ELEMENT"
    # B
    compare_009.inputs[1].default_value = 0.0
    # A
    compare_009.inputs[2].default_value = 0
    # B
    compare_009.inputs[3].default_value = 0
    # A
    compare_009.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare_009.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare_009.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # B
    compare_009.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    # A
    compare_009.inputs[8].default_value = ""
    # B
    compare_009.inputs[9].default_value = ""
    # C
    compare_009.inputs[10].default_value = 0.8999999761581421
    # Angle
    compare_009.inputs[11].default_value = 0.08726649731397629
    # Epsilon
    compare_009.inputs[12].default_value = 0.0010000000474974513
    # Links for compare_009
    links.new(separate_x_y_z_008.outputs[0], compare_009.inputs[0])
    links.new(compare_009.outputs[0], delete_geometry_004.inputs[1])

    float_curve_012 = nodes.new("ShaderNodeFloatCurve")
    float_curve_012.name = "Float Curve.012"
    float_curve_012.label = ""
    float_curve_012.location = (4289.0, -1035.80029296875)
    float_curve_012.bl_label = "Float Curve"
    # Factor
    float_curve_012.inputs[0].default_value = 1.0
    # Links for float_curve_012
    links.new(math_021.outputs[0], float_curve_012.inputs[1])
    links.new(float_curve_012.outputs[0], instance_on_points_008.inputs[6])

    transform_geometry_031 = nodes.new("GeometryNodeTransform")
    transform_geometry_031.name = "Transform Geometry.031"
    transform_geometry_031.label = ""
    transform_geometry_031.location = (4869.0, -935.80029296875)
    transform_geometry_031.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_031.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_031.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_031.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_031.inputs[4].default_value = Vector((-1.0, 1.0, 1.0))
    # Links for transform_geometry_031
    links.new(realize_instances_004.outputs[0], transform_geometry_031.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.name = "Flip Faces.003"
    flip_faces_003.label = ""
    flip_faces_003.location = (5029.0, -935.80029296875)
    flip_faces_003.bl_label = "Flip Faces"
    # Selection
    flip_faces_003.inputs[1].default_value = True
    # Links for flip_faces_003
    links.new(transform_geometry_031.outputs[0], flip_faces_003.inputs[0])

    join_geometry_019 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_019.name = "Join Geometry.019"
    join_geometry_019.label = ""
    join_geometry_019.location = (5229.0, -875.80029296875)
    join_geometry_019.bl_label = "Join Geometry"
    # Links for join_geometry_019
    links.new(join_geometry_019.outputs[0], join_geometry_016.inputs[0])
    links.new(flip_faces_003.outputs[0], join_geometry_019.inputs[0])
    links.new(realize_instances_004.outputs[0], join_geometry_019.inputs[0])

    gem_in_holder_4 = nodes.new("GeometryNodeGroup")
    gem_in_holder_4.name = "Gem in Holder.004"
    gem_in_holder_4.label = ""
    gem_in_holder_4.location = (3149.0, -495.80029296875)
    gem_in_holder_4.node_tree = create_gem_in__holder_group()
    gem_in_holder_4.bl_label = "Group"
    # Gem Radius
    gem_in_holder_4.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_4.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_4.inputs[2].default_value = False
    # Scale
    gem_in_holder_4.inputs[3].default_value = 0.004999995231628418
    # Count
    gem_in_holder_4.inputs[4].default_value = 6
    # Seed
    gem_in_holder_4.inputs[5].default_value = 41
    # Wings
    gem_in_holder_4.inputs[6].default_value = False
    # Array Count
    gem_in_holder_4.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_4.inputs[8].default_value = 10
    # Split
    gem_in_holder_4.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder_4.inputs[10].default_value = 3.3099989891052246
    # Links for gem_in_holder_4

    join_geometry_020 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_020.name = "Join Geometry.020"
    join_geometry_020.label = ""
    join_geometry_020.location = (4329.0, -735.80029296875)
    join_geometry_020.bl_label = "Join Geometry"
    # Links for join_geometry_020
    links.new(join_geometry_020.outputs[0], instance_on_points_008.inputs[2])
    links.new(gem_in_holder_4.outputs[3], join_geometry_020.inputs[0])

    gem_in_holder_5 = nodes.new("GeometryNodeGroup")
    gem_in_holder_5.name = "Gem in Holder.005"
    gem_in_holder_5.label = ""
    gem_in_holder_5.location = (3149.0, -595.80029296875)
    gem_in_holder_5.node_tree = create_gem_in__holder_group()
    gem_in_holder_5.bl_label = "Group"
    # Gem Radius
    gem_in_holder_5.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_5.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_5.inputs[2].default_value = False
    # Scale
    gem_in_holder_5.inputs[3].default_value = 0.004999995231628418
    # Count
    gem_in_holder_5.inputs[4].default_value = 6
    # Seed
    gem_in_holder_5.inputs[5].default_value = 41
    # Wings
    gem_in_holder_5.inputs[6].default_value = False
    # Array Count
    gem_in_holder_5.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_5.inputs[8].default_value = 10
    # Split
    gem_in_holder_5.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder_5.inputs[10].default_value = 5.109997272491455
    # Links for gem_in_holder_5

    transform_geometry_032 = nodes.new("GeometryNodeTransform")
    transform_geometry_032.name = "Transform Geometry.032"
    transform_geometry_032.label = ""
    transform_geometry_032.location = (3309.0, -675.80029296875)
    transform_geometry_032.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_032.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_032.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_032.inputs[3].default_value = Euler((0.0, 0.0, 0.01745329238474369), 'XYZ')
    # Scale
    transform_geometry_032.inputs[4].default_value = Vector((1.0, -1.0, 1.0))
    # Links for transform_geometry_032
    links.new(gem_in_holder_5.outputs[3], transform_geometry_032.inputs[0])

    join_geometry_021 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_021.name = "Join Geometry.021"
    join_geometry_021.label = ""
    join_geometry_021.location = (3309.0, -595.80029296875)
    join_geometry_021.bl_label = "Join Geometry"
    # Links for join_geometry_021
    links.new(join_geometry_021.outputs[0], join_geometry_020.inputs[0])
    links.new(gem_in_holder_5.outputs[3], join_geometry_021.inputs[0])

    flip_faces_001 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.name = "Flip Faces.001"
    flip_faces_001.label = ""
    flip_faces_001.location = (3309.0, -635.80029296875)
    flip_faces_001.bl_label = "Flip Faces"
    # Selection
    flip_faces_001.inputs[1].default_value = True
    # Links for flip_faces_001
    links.new(transform_geometry_032.outputs[0], flip_faces_001.inputs[0])
    links.new(flip_faces_001.outputs[0], join_geometry_021.inputs[0])

    gem_in_holder_6 = nodes.new("GeometryNodeGroup")
    gem_in_holder_6.name = "Gem in Holder.006"
    gem_in_holder_6.label = ""
    gem_in_holder_6.location = (3009.0, -775.80029296875)
    gem_in_holder_6.node_tree = create_gem_in__holder_group()
    gem_in_holder_6.bl_label = "Group"
    # Gem Radius
    gem_in_holder_6.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_6.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_6.inputs[2].default_value = False
    # Scale
    gem_in_holder_6.inputs[3].default_value = 0.004999995231628418
    # Count
    gem_in_holder_6.inputs[4].default_value = 6
    # Seed
    gem_in_holder_6.inputs[5].default_value = 41
    # Wings
    gem_in_holder_6.inputs[6].default_value = False
    # Array Count
    gem_in_holder_6.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_6.inputs[8].default_value = 6
    # Split
    gem_in_holder_6.inputs[9].default_value = 0.0010000000474974513
    # Seed
    gem_in_holder_6.inputs[10].default_value = 4.80999755859375
    # Links for gem_in_holder_6

    transform_geometry_033 = nodes.new("GeometryNodeTransform")
    transform_geometry_033.name = "Transform Geometry.033"
    transform_geometry_033.label = ""
    transform_geometry_033.location = (3169.0, -855.80029296875)
    transform_geometry_033.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_033.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_033.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_033.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_033.inputs[4].default_value = Vector((1.0, -1.0, 1.0))
    # Links for transform_geometry_033
    links.new(gem_in_holder_6.outputs[3], transform_geometry_033.inputs[0])

    join_geometry_022 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_022.name = "Join Geometry.022"
    join_geometry_022.label = ""
    join_geometry_022.location = (3329.0, -795.80029296875)
    join_geometry_022.bl_label = "Join Geometry"
    # Links for join_geometry_022
    links.new(gem_in_holder_6.outputs[3], join_geometry_022.inputs[0])

    flip_faces_004 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_004.name = "Flip Faces.004"
    flip_faces_004.label = ""
    flip_faces_004.location = (3329.0, -855.80029296875)
    flip_faces_004.bl_label = "Flip Faces"
    # Selection
    flip_faces_004.inputs[1].default_value = True
    # Links for flip_faces_004
    links.new(transform_geometry_033.outputs[0], flip_faces_004.inputs[0])
    links.new(flip_faces_004.outputs[0], join_geometry_022.inputs[0])

    transform_geometry_034 = nodes.new("GeometryNodeTransform")
    transform_geometry_034.name = "Transform Geometry.034"
    transform_geometry_034.label = ""
    transform_geometry_034.location = (3489.0, -795.80029296875)
    transform_geometry_034.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_034.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_034.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_034.inputs[3].default_value = Euler((0.0, -0.4363323152065277, 0.0), 'XYZ')
    # Scale
    transform_geometry_034.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_034
    links.new(transform_geometry_034.outputs[0], join_geometry_020.inputs[0])
    links.new(join_geometry_022.outputs[0], transform_geometry_034.inputs[0])

    join_geometry_017 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_017.name = "Join Geometry.017"
    join_geometry_017.label = ""
    join_geometry_017.location = (6009.0, -935.80029296875)
    join_geometry_017.bl_label = "Join Geometry"
    # Links for join_geometry_017

    store_named_attribute_008 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_008.name = "Store Named Attribute.008"
    store_named_attribute_008.label = ""
    store_named_attribute_008.location = (5789.0, -795.80029296875)
    store_named_attribute_008.bl_label = "Store Named Attribute"
    store_named_attribute_008.data_type = "BOOLEAN"
    store_named_attribute_008.domain = "POINT"
    # Selection
    store_named_attribute_008.inputs[1].default_value = True
    # Name
    store_named_attribute_008.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_008.inputs[3].default_value = True
    # Links for store_named_attribute_008
    links.new(join_geometry_016.outputs[0], store_named_attribute_008.inputs[0])
    links.new(store_named_attribute_008.outputs[0], join_geometry_017.inputs[0])

    store_named_attribute_009 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_009.name = "Store Named Attribute.009"
    store_named_attribute_009.label = ""
    store_named_attribute_009.location = (5789.0, -975.80029296875)
    store_named_attribute_009.bl_label = "Store Named Attribute"
    store_named_attribute_009.data_type = "BOOLEAN"
    store_named_attribute_009.domain = "POINT"
    # Selection
    store_named_attribute_009.inputs[1].default_value = True
    # Name
    store_named_attribute_009.inputs[2].default_value = "saphire"
    # Value
    store_named_attribute_009.inputs[3].default_value = True
    # Links for store_named_attribute_009
    links.new(merge_by_distance_001.outputs[0], store_named_attribute_009.inputs[0])
    links.new(store_named_attribute_009.outputs[0], join_geometry_017.inputs[0])

    gem_in_holder_7 = nodes.new("GeometryNodeGroup")
    gem_in_holder_7.name = "Gem in Holder.007"
    gem_in_holder_7.label = ""
    gem_in_holder_7.location = (389.0, -215.80029296875)
    gem_in_holder_7.node_tree = create_gem_in__holder_group()
    gem_in_holder_7.bl_label = "Group"
    # Gem Radius
    gem_in_holder_7.inputs[0].default_value = 0.006000000052154064
    # Gem Material
    gem_in_holder_7.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_7.inputs[2].default_value = False
    # Scale
    gem_in_holder_7.inputs[3].default_value = 0.004000000189989805
    # Count
    gem_in_holder_7.inputs[4].default_value = 6
    # Seed
    gem_in_holder_7.inputs[5].default_value = 41
    # Wings
    gem_in_holder_7.inputs[6].default_value = False
    # Array Count
    gem_in_holder_7.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_7.inputs[8].default_value = 3
    # Split
    gem_in_holder_7.inputs[9].default_value = 0.0010000000474974513
    # Seed
    gem_in_holder_7.inputs[10].default_value = 5.309997081756592
    # Links for gem_in_holder_7

    instance_on_points_009 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_009.name = "Instance on Points.009"
    instance_on_points_009.label = ""
    instance_on_points_009.location = (569.0, -155.80029296875)
    instance_on_points_009.bl_label = "Instance on Points"
    # Selection
    instance_on_points_009.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_009.inputs[3].default_value = False
    # Instance Index
    instance_on_points_009.inputs[4].default_value = 0
    # Rotation
    instance_on_points_009.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points_009.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points_009
    links.new(gem_in_holder_7.outputs[0], instance_on_points_009.inputs[2])
    links.new(instance_on_points_009.outputs[0], join_geometry_017.inputs[0])

    curve_circle_012 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_012.name = "Curve Circle.012"
    curve_circle_012.label = ""
    curve_circle_012.location = (29.0, -35.80029296875)
    curve_circle_012.bl_label = "Curve Circle"
    curve_circle_012.mode = "RADIUS"
    # Resolution
    curve_circle_012.inputs[0].default_value = 12
    # Point 1
    curve_circle_012.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_012.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_012.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_012.inputs[4].default_value = 0.05000000074505806
    # Links for curve_circle_012

    transform_geometry_035 = nodes.new("GeometryNodeTransform")
    transform_geometry_035.name = "Transform Geometry.035"
    transform_geometry_035.label = ""
    transform_geometry_035.location = (209.0, -35.80029296875)
    transform_geometry_035.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_035.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_035.inputs[2].default_value = Vector((0.0, 0.003000000026077032, 0.009999999776482582))
    # Rotation
    transform_geometry_035.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_035.inputs[4].default_value = Vector((1.4000000953674316, 0.8999999761581421, 1.0))
    # Links for transform_geometry_035
    links.new(transform_geometry_035.outputs[0], instance_on_points_009.inputs[0])
    links.new(curve_circle_012.outputs[0], transform_geometry_035.inputs[0])

    frame_025 = nodes.new("NodeFrame")
    frame_025.name = "Frame.025"
    frame_025.label = "Satalite Gems"
    frame_025.location = (5180.0, -1240.0)
    frame_025.bl_label = "Frame"
    frame_025.text = None
    frame_025.shrink = True
    frame_025.label_size = 20
    # Links for frame_025

    frame_026 = nodes.new("NodeFrame")
    frame_026.name = "Frame.026"
    frame_026.label = "Main Broach"
    frame_026.location = (991.0, 8155.80029296875)
    frame_026.bl_label = "Frame"
    frame_026.text = None
    frame_026.shrink = True
    frame_026.label_size = 20
    # Links for frame_026

    transform_geometry_036 = nodes.new("GeometryNodeTransform")
    transform_geometry_036.name = "Transform Geometry.036"
    transform_geometry_036.label = ""
    transform_geometry_036.location = (6189.0, -875.80029296875)
    transform_geometry_036.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_036.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_036.inputs[2].default_value = Vector((0.0, -0.12600000202655792, 0.36497700214385986))
    # Rotation
    transform_geometry_036.inputs[3].default_value = Euler((0.9428269863128662, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_036.inputs[4].default_value = Vector((0.4000000059604645, 0.4000000059604645, 0.4000000059604645))
    # Links for transform_geometry_036
    links.new(join_geometry_017.outputs[0], transform_geometry_036.inputs[0])

    instance_on_points_010 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_010.name = "Instance on Points.010"
    instance_on_points_010.label = ""
    instance_on_points_010.location = (749.0, -175.80029296875)
    instance_on_points_010.bl_label = "Instance on Points"
    # Selection
    instance_on_points_010.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_010.inputs[3].default_value = False
    # Instance Index
    instance_on_points_010.inputs[4].default_value = 0
    # Scale
    instance_on_points_010.inputs[6].default_value = Vector((0.6000000238418579, 0.6000000238418579, 0.6000000238418579))
    # Links for instance_on_points_010

    gem_in_holder_8 = nodes.new("GeometryNodeGroup")
    gem_in_holder_8.name = "Gem in Holder.008"
    gem_in_holder_8.label = ""
    gem_in_holder_8.location = (189.0, -175.80029296875)
    gem_in_holder_8.node_tree = create_gem_in__holder_group()
    gem_in_holder_8.bl_label = "Group"
    # Gem Radius
    gem_in_holder_8.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_8.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_8.inputs[2].default_value = True
    # Scale
    gem_in_holder_8.inputs[3].default_value = 0.004999999888241291
    # Count
    gem_in_holder_8.inputs[4].default_value = 20
    # Seed
    gem_in_holder_8.inputs[5].default_value = 10
    # Wings
    gem_in_holder_8.inputs[6].default_value = False
    # Array Count
    gem_in_holder_8.inputs[7].default_value = 6
    # Strand Count
    gem_in_holder_8.inputs[8].default_value = 10
    # Split
    gem_in_holder_8.inputs[9].default_value = 0.0020000000949949026
    # Seed
    gem_in_holder_8.inputs[10].default_value = 2.5099997520446777
    # Links for gem_in_holder_8
    links.new(gem_in_holder_8.outputs[0], instance_on_points_010.inputs[2])

    realize_instances_005 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_005.name = "Realize Instances.005"
    realize_instances_005.label = ""
    realize_instances_005.location = (1109.0, -115.80029296875)
    realize_instances_005.bl_label = "Realize Instances"
    # Selection
    realize_instances_005.inputs[1].default_value = True
    # Realize All
    realize_instances_005.inputs[2].default_value = True
    # Depth
    realize_instances_005.inputs[3].default_value = 0
    # Links for realize_instances_005

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.name = "Capture Attribute.002"
    capture_attribute_002.label = ""
    capture_attribute_002.location = (929.0, -175.80029296875)
    capture_attribute_002.bl_label = "Capture Attribute"
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "INSTANCE"
    # Links for capture_attribute_002
    links.new(capture_attribute_002.outputs[0], realize_instances_005.inputs[0])
    links.new(instance_on_points_010.outputs[0], capture_attribute_002.inputs[0])

    index_002 = nodes.new("GeometryNodeInputIndex")
    index_002.name = "Index.002"
    index_002.label = ""
    index_002.location = (929.0, -295.80029296875)
    index_002.bl_label = "Index"
    # Links for index_002
    links.new(index_002.outputs[0], capture_attribute_002.inputs[1])

    resample_curve_008 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_008.name = "Resample Curve.008"
    resample_curve_008.label = ""
    resample_curve_008.location = (189.0, -35.80029296875)
    resample_curve_008.bl_label = "Resample Curve"
    resample_curve_008.keep_last_segment = True
    # Selection
    resample_curve_008.inputs[1].default_value = True
    # Mode
    resample_curve_008.inputs[2].default_value = "Count"
    # Count
    resample_curve_008.inputs[3].default_value = 10
    # Length
    resample_curve_008.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_008
    links.new(resample_curve_008.outputs[0], instance_on_points_010.inputs[0])

    align_rotation_to_vector_005 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_005.name = "Align Rotation to Vector.005"
    align_rotation_to_vector_005.label = ""
    align_rotation_to_vector_005.location = (369.0, -315.80029296875)
    align_rotation_to_vector_005.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_005.axis = "X"
    align_rotation_to_vector_005.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_005.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_005.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_005

    normal_004 = nodes.new("GeometryNodeInputNormal")
    normal_004.name = "Normal.004"
    normal_004.label = ""
    normal_004.location = (529.0, -475.80029296875)
    normal_004.bl_label = "Normal"
    normal_004.legacy_corner_normals = False
    # Links for normal_004

    align_rotation_to_vector_006 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_006.name = "Align Rotation to Vector.006"
    align_rotation_to_vector_006.label = ""
    align_rotation_to_vector_006.location = (529.0, -315.80029296875)
    align_rotation_to_vector_006.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_006.axis = "Y"
    align_rotation_to_vector_006.pivot_axis = "AUTO"
    # Factor
    align_rotation_to_vector_006.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_006
    links.new(align_rotation_to_vector_006.outputs[0], instance_on_points_010.inputs[5])
    links.new(align_rotation_to_vector_005.outputs[0], align_rotation_to_vector_006.inputs[0])
    links.new(normal_004.outputs[0], align_rotation_to_vector_006.inputs[2])

    curve_tangent_004 = nodes.new("GeometryNodeInputTangent")
    curve_tangent_004.name = "Curve Tangent.004"
    curve_tangent_004.label = ""
    curve_tangent_004.location = (369.0, -475.80029296875)
    curve_tangent_004.bl_label = "Curve Tangent"
    # Links for curve_tangent_004
    links.new(curve_tangent_004.outputs[0], align_rotation_to_vector_005.inputs[2])

    frame_027 = nodes.new("NodeFrame")
    frame_027.name = "Frame.027"
    frame_027.label = "Collar Gems"
    frame_027.location = (2489.0, -35.7998046875)
    frame_027.bl_label = "Frame"
    frame_027.text = None
    frame_027.shrink = True
    frame_027.label_size = 20
    # Links for frame_027

    trim_curve_006 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_006.name = "Trim Curve.006"
    trim_curve_006.label = ""
    trim_curve_006.location = (29.0, -35.80029296875)
    trim_curve_006.bl_label = "Trim Curve"
    trim_curve_006.mode = "FACTOR"
    # Selection
    trim_curve_006.inputs[1].default_value = True
    # Start
    trim_curve_006.inputs[2].default_value = 0.009999999776482582
    # End
    trim_curve_006.inputs[3].default_value = 0.940000057220459
    # Start
    trim_curve_006.inputs[4].default_value = 0.0
    # End
    trim_curve_006.inputs[5].default_value = 1.0
    # Links for trim_curve_006
    links.new(trim_curve_006.outputs[0], resample_curve_008.inputs[0])
    links.new(set_curve_tilt.outputs[0], trim_curve_006.inputs[0])

    gem_in_holder_9 = nodes.new("GeometryNodeGroup")
    gem_in_holder_9.name = "Gem in Holder.009"
    gem_in_holder_9.label = ""
    gem_in_holder_9.location = (1109.0, -155.80029296875)
    gem_in_holder_9.node_tree = create_gem_in__holder_group()
    gem_in_holder_9.bl_label = "Group"
    # Gem Radius
    gem_in_holder_9.inputs[0].default_value = 0.009999999776482582
    # Gem Material
    gem_in_holder_9.inputs[1].default_value = "ruby"
    # Gem Dual Mesh
    gem_in_holder_9.inputs[2].default_value = False
    # Scale
    gem_in_holder_9.inputs[3].default_value = 0.004999999888241291
    # Wings
    gem_in_holder_9.inputs[6].default_value = True
    # Links for gem_in_holder_9

    curve_to_points_003 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_003.name = "Curve to Points.003"
    curve_to_points_003.label = ""
    curve_to_points_003.location = (189.0, -475.80029296875)
    curve_to_points_003.bl_label = "Curve to Points"
    curve_to_points_003.mode = "COUNT"
    # Count
    curve_to_points_003.inputs[1].default_value = 2
    # Length
    curve_to_points_003.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points_003

    for_each_geometry_element_input_002 = nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_002.name = "For Each Geometry Element Input.002"
    for_each_geometry_element_input_002.label = ""
    for_each_geometry_element_input_002.location = (409.0, -415.80029296875)
    for_each_geometry_element_input_002.bl_label = "For Each Geometry Element Input"
    # Selection
    for_each_geometry_element_input_002.inputs[1].default_value = True
    # Links for for_each_geometry_element_input_002
    links.new(curve_to_points_003.outputs[0], for_each_geometry_element_input_002.inputs[0])
    links.new(curve_to_points_003.outputs[3], for_each_geometry_element_input_002.inputs[2])

    for_each_geometry_element_output_002 = nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_002.name = "For Each Geometry Element Output.002"
    for_each_geometry_element_output_002.label = ""
    for_each_geometry_element_output_002.location = (2029.0, -455.80029296875)
    for_each_geometry_element_output_002.bl_label = "For Each Geometry Element Output"
    for_each_geometry_element_output_002.active_input_index = 1
    for_each_geometry_element_output_002.active_generation_index = 0
    for_each_geometry_element_output_002.active_main_index = 0
    for_each_geometry_element_output_002.domain = "POINT"
    for_each_geometry_element_output_002.inspection_index = 0
    # Links for for_each_geometry_element_output_002

    position_010 = nodes.new("GeometryNodeInputPosition")
    position_010.name = "Position.010"
    position_010.label = ""
    position_010.location = (189.0, -675.80029296875)
    position_010.bl_label = "Position"
    # Links for position_010
    links.new(position_010.outputs[0], for_each_geometry_element_input_002.inputs[3])

    transform_geometry_037 = nodes.new("GeometryNodeTransform")
    transform_geometry_037.name = "Transform Geometry.037"
    transform_geometry_037.label = ""
    transform_geometry_037.location = (1389.0, -475.80029296875)
    transform_geometry_037.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_037.inputs[1].default_value = "Components"
    # Links for transform_geometry_037
    links.new(gem_in_holder_9.outputs[0], transform_geometry_037.inputs[0])
    links.new(for_each_geometry_element_input_002.outputs[3], transform_geometry_037.inputs[2])

    rotate_rotation_007 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_007.name = "Rotate Rotation.007"
    rotate_rotation_007.label = ""
    rotate_rotation_007.location = (1049.0, -675.80029296875)
    rotate_rotation_007.bl_label = "Rotate Rotation"
    rotate_rotation_007.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_007.inputs[1].default_value = Euler((1.5707963705062866, 0.0, 0.0), 'XYZ')
    # Links for rotate_rotation_007
    links.new(for_each_geometry_element_input_002.outputs[2], rotate_rotation_007.inputs[0])

    random_value_014 = nodes.new("FunctionNodeRandomValue")
    random_value_014.name = "Random Value.014"
    random_value_014.label = ""
    random_value_014.location = (649.0, -395.80029296875)
    random_value_014.bl_label = "Random Value"
    random_value_014.data_type = "INT"
    # Min
    random_value_014.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_014.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_014.inputs[2].default_value = 0.0
    # Max
    random_value_014.inputs[3].default_value = 1.0
    # Min
    random_value_014.inputs[4].default_value = 5
    # Max
    random_value_014.inputs[5].default_value = 7
    # Probability
    random_value_014.inputs[6].default_value = 0.5
    # Seed
    random_value_014.inputs[8].default_value = 0
    # Links for random_value_014
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_014.inputs[7])
    links.new(random_value_014.outputs[2], gem_in_holder_9.inputs[7])

    transform_geometry_038 = nodes.new("GeometryNodeTransform")
    transform_geometry_038.name = "Transform Geometry.038"
    transform_geometry_038.label = ""
    transform_geometry_038.location = (1569.0, -475.80029296875)
    transform_geometry_038.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_038.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_038.inputs[2].default_value = Vector((0.0, -0.004999999888241291, 0.0))
    # Rotation
    transform_geometry_038.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_038.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_038
    links.new(transform_geometry_037.outputs[0], transform_geometry_038.inputs[0])

    trim_curve_007 = nodes.new("GeometryNodeTrimCurve")
    trim_curve_007.name = "Trim Curve.007"
    trim_curve_007.label = ""
    trim_curve_007.location = (29.0, -475.80029296875)
    trim_curve_007.bl_label = "Trim Curve"
    trim_curve_007.mode = "FACTOR"
    # Selection
    trim_curve_007.inputs[1].default_value = True
    # Start
    trim_curve_007.inputs[2].default_value = 0.4000000059604645
    # End
    trim_curve_007.inputs[3].default_value = 0.75
    # Start
    trim_curve_007.inputs[4].default_value = 0.0
    # End
    trim_curve_007.inputs[5].default_value = 1.0
    # Links for trim_curve_007
    links.new(trim_curve_007.outputs[0], curve_to_points_003.inputs[0])
    links.new(separate_geometry_002.outputs[0], trim_curve_007.inputs[0])

    random_value_015 = nodes.new("FunctionNodeRandomValue")
    random_value_015.name = "Random Value.015"
    random_value_015.label = ""
    random_value_015.location = (629.0, -615.80029296875)
    random_value_015.bl_label = "Random Value"
    random_value_015.data_type = "FLOAT"
    # Min
    random_value_015.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_015.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_015.inputs[2].default_value = 0.25
    # Max
    random_value_015.inputs[3].default_value = 0.550000011920929
    # Min
    random_value_015.inputs[4].default_value = 0
    # Max
    random_value_015.inputs[5].default_value = 100
    # Probability
    random_value_015.inputs[6].default_value = 0.5
    # Seed
    random_value_015.inputs[8].default_value = 0
    # Links for random_value_015
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_015.inputs[7])
    links.new(random_value_015.outputs[1], transform_geometry_037.inputs[4])

    store_named_attribute_010 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_010.name = "Store Named Attribute.010"
    store_named_attribute_010.label = ""
    store_named_attribute_010.location = (1809.0, -495.80029296875)
    store_named_attribute_010.bl_label = "Store Named Attribute"
    store_named_attribute_010.data_type = "BOOLEAN"
    store_named_attribute_010.domain = "POINT"
    # Selection
    store_named_attribute_010.inputs[1].default_value = True
    # Name
    store_named_attribute_010.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_010.inputs[3].default_value = True
    # Links for store_named_attribute_010
    links.new(store_named_attribute_010.outputs[0], for_each_geometry_element_output_002.inputs[1])
    links.new(transform_geometry_038.outputs[0], store_named_attribute_010.inputs[0])

    random_value_016 = nodes.new("FunctionNodeRandomValue")
    random_value_016.name = "Random Value.016"
    random_value_016.label = ""
    random_value_016.location = (649.0, -215.80029296875)
    random_value_016.bl_label = "Random Value"
    random_value_016.data_type = "FLOAT"
    # Min
    random_value_016.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_016.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_016.inputs[2].default_value = 0.0
    # Max
    random_value_016.inputs[3].default_value = 100.0
    # Min
    random_value_016.inputs[4].default_value = 3
    # Max
    random_value_016.inputs[5].default_value = 7
    # Probability
    random_value_016.inputs[6].default_value = 0.5
    # Seed
    random_value_016.inputs[8].default_value = 16
    # Links for random_value_016
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_016.inputs[7])
    links.new(random_value_016.outputs[1], gem_in_holder_9.inputs[10])

    rotate_rotation_008 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_008.name = "Rotate Rotation.008"
    rotate_rotation_008.label = ""
    rotate_rotation_008.location = (1209.0, -675.80029296875)
    rotate_rotation_008.bl_label = "Rotate Rotation"
    rotate_rotation_008.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation_008.inputs[1].default_value = Euler((0.0, 0.0, -1.5707963705062866), 'XYZ')
    # Links for rotate_rotation_008
    links.new(rotate_rotation_008.outputs[0], transform_geometry_037.inputs[3])
    links.new(rotate_rotation_007.outputs[0], rotate_rotation_008.inputs[0])

    random_value_017 = nodes.new("FunctionNodeRandomValue")
    random_value_017.name = "Random Value.017"
    random_value_017.label = ""
    random_value_017.location = (649.0, -35.80029296875)
    random_value_017.bl_label = "Random Value"
    random_value_017.data_type = "FLOAT"
    # Min
    random_value_017.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_017.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_017.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_017.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_017.inputs[4].default_value = 3
    # Max
    random_value_017.inputs[5].default_value = 7
    # Probability
    random_value_017.inputs[6].default_value = 0.5
    # Seed
    random_value_017.inputs[8].default_value = 0
    # Links for random_value_017
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_017.inputs[7])
    links.new(random_value_017.outputs[1], gem_in_holder_9.inputs[9])

    random_value_018 = nodes.new("FunctionNodeRandomValue")
    random_value_018.name = "Random Value.018"
    random_value_018.label = ""
    random_value_018.location = (889.0, -255.80029296875)
    random_value_018.bl_label = "Random Value"
    random_value_018.data_type = "INT"
    # Min
    random_value_018.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_018.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_018.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_018.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_018.inputs[4].default_value = 0
    # Max
    random_value_018.inputs[5].default_value = 100
    # Probability
    random_value_018.inputs[6].default_value = 0.5
    # Seed
    random_value_018.inputs[8].default_value = 0
    # Links for random_value_018
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_018.inputs[7])
    links.new(random_value_018.outputs[2], gem_in_holder_9.inputs[5])

    random_value_019 = nodes.new("FunctionNodeRandomValue")
    random_value_019.name = "Random Value.019"
    random_value_019.label = ""
    random_value_019.location = (889.0, -75.80029296875)
    random_value_019.bl_label = "Random Value"
    random_value_019.data_type = "INT"
    # Min
    random_value_019.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_019.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_019.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_019.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_019.inputs[4].default_value = 6
    # Max
    random_value_019.inputs[5].default_value = 20
    # Probability
    random_value_019.inputs[6].default_value = 0.5
    # Seed
    random_value_019.inputs[8].default_value = 0
    # Links for random_value_019
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_019.inputs[7])
    links.new(random_value_019.outputs[2], gem_in_holder_9.inputs[4])

    random_value_020 = nodes.new("FunctionNodeRandomValue")
    random_value_020.name = "Random Value.020"
    random_value_020.label = ""
    random_value_020.location = (889.0, -435.80029296875)
    random_value_020.bl_label = "Random Value"
    random_value_020.data_type = "INT"
    # Min
    random_value_020.inputs[0].default_value = [0.0, 0.0, 0.0]
    # Max
    random_value_020.inputs[1].default_value = [1.0, 1.0, 1.0]
    # Min
    random_value_020.inputs[2].default_value = 0.0010000000474974513
    # Max
    random_value_020.inputs[3].default_value = 0.004999999888241291
    # Min
    random_value_020.inputs[4].default_value = 5
    # Max
    random_value_020.inputs[5].default_value = 30
    # Probability
    random_value_020.inputs[6].default_value = 0.5
    # Seed
    random_value_020.inputs[8].default_value = 0
    # Links for random_value_020
    links.new(for_each_geometry_element_input_002.outputs[0], random_value_020.inputs[7])
    links.new(random_value_020.outputs[2], gem_in_holder_9.inputs[8])

    frame_028 = nodes.new("NodeFrame")
    frame_028.name = "Frame.028"
    frame_028.label = "Broaches"
    frame_028.location = (3029.0, -915.7998046875)
    frame_028.bl_label = "Frame"
    frame_028.text = None
    frame_028.shrink = True
    frame_028.label_size = 20
    # Links for frame_028

    store_named_attribute_011 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_011.name = "Store Named Attribute.011"
    store_named_attribute_011.label = ""
    store_named_attribute_011.location = (6369.0, -875.80029296875)
    store_named_attribute_011.bl_label = "Store Named Attribute"
    store_named_attribute_011.data_type = "BOOLEAN"
    store_named_attribute_011.domain = "POINT"
    # Selection
    store_named_attribute_011.inputs[1].default_value = True
    # Name
    store_named_attribute_011.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_011.inputs[3].default_value = True
    # Links for store_named_attribute_011
    links.new(store_named_attribute_011.outputs[0], join_geometry_002.inputs[0])
    links.new(transform_geometry_036.outputs[0], store_named_attribute_011.inputs[0])

    store_named_attribute_012 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_012.name = "Store Named Attribute.012"
    store_named_attribute_012.label = ""
    store_named_attribute_012.location = (2189.0, -455.80029296875)
    store_named_attribute_012.bl_label = "Store Named Attribute"
    store_named_attribute_012.data_type = "BOOLEAN"
    store_named_attribute_012.domain = "POINT"
    # Selection
    store_named_attribute_012.inputs[1].default_value = True
    # Name
    store_named_attribute_012.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_012.inputs[3].default_value = True
    # Links for store_named_attribute_012
    links.new(store_named_attribute_012.outputs[0], join_geometry_002.inputs[0])
    links.new(for_each_geometry_element_output_002.outputs[2], store_named_attribute_012.inputs[0])

    mesh_boolean_002 = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean_002.name = "Mesh Boolean.002"
    mesh_boolean_002.label = ""
    mesh_boolean_002.location = (1329.0, -49.0)
    mesh_boolean_002.bl_label = "Mesh Boolean"
    mesh_boolean_002.operation = "DIFFERENCE"
    mesh_boolean_002.solver = "FLOAT"
    # Self Intersection
    mesh_boolean_002.inputs[2].default_value = False
    # Hole Tolerant
    mesh_boolean_002.inputs[3].default_value = False
    # Links for mesh_boolean_002
    links.new(mesh_boolean_002.outputs[0], join_geometry_002.inputs[0])
    links.new(gold_decorations_2.outputs[0], mesh_boolean_002.inputs[0])

    ico_sphere_007 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_007.name = "Ico Sphere.007"
    ico_sphere_007.label = ""
    ico_sphere_007.location = (1029.0, -209.0)
    ico_sphere_007.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_007.inputs[0].default_value = 0.07800000160932541
    # Subdivisions
    ico_sphere_007.inputs[1].default_value = 3
    # Links for ico_sphere_007

    transform_geometry_039 = nodes.new("GeometryNodeTransform")
    transform_geometry_039.name = "Transform Geometry.039"
    transform_geometry_039.label = ""
    transform_geometry_039.location = (1189.0, -209.0)
    transform_geometry_039.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_039.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_039.inputs[2].default_value = Vector((0.0, -0.019999999552965164, 0.47999998927116394))
    # Rotation
    transform_geometry_039.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_039.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_039
    links.new(transform_geometry_039.outputs[0], mesh_boolean_002.inputs[1])
    links.new(ico_sphere_007.outputs[0], transform_geometry_039.inputs[0])

    store_named_attribute_013 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_013.name = "Store Named Attribute.013"
    store_named_attribute_013.label = ""
    store_named_attribute_013.location = (1449.0, -135.80029296875)
    store_named_attribute_013.bl_label = "Store Named Attribute"
    store_named_attribute_013.data_type = "BOOLEAN"
    store_named_attribute_013.domain = "POINT"
    # Name
    store_named_attribute_013.inputs[2].default_value = "saphire"
    # Value
    store_named_attribute_013.inputs[3].default_value = True
    # Links for store_named_attribute_013
    links.new(realize_instances_005.outputs[0], store_named_attribute_013.inputs[0])

    boolean_math_005 = nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.name = "Boolean Math.005"
    boolean_math_005.label = ""
    boolean_math_005.location = (1289.0, -255.80029296875)
    boolean_math_005.bl_label = "Boolean Math"
    boolean_math_005.operation = "AND"
    # Links for boolean_math_005
    links.new(boolean_math_005.outputs[0], store_named_attribute_013.inputs[1])

    named_attribute = nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.label = ""
    named_attribute.location = (1109.0, -415.80029296875)
    named_attribute.bl_label = "Named Attribute"
    named_attribute.data_type = "BOOLEAN"
    # Name
    named_attribute.inputs[0].default_value = "ruby"
    # Links for named_attribute
    links.new(named_attribute.outputs[0], boolean_math_005.inputs[1])

    store_named_attribute_014 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_014.name = "Store Named Attribute.014"
    store_named_attribute_014.label = ""
    store_named_attribute_014.location = (1609.0, -135.80029296875)
    store_named_attribute_014.bl_label = "Store Named Attribute"
    store_named_attribute_014.data_type = "BOOLEAN"
    store_named_attribute_014.domain = "POINT"
    # Name
    store_named_attribute_014.inputs[2].default_value = "ruby"
    # Value
    store_named_attribute_014.inputs[3].default_value = False
    # Links for store_named_attribute_014
    links.new(store_named_attribute_013.outputs[0], store_named_attribute_014.inputs[0])
    links.new(boolean_math_005.outputs[0], store_named_attribute_014.inputs[1])
    links.new(store_named_attribute_014.outputs[0], join_geometry_002.inputs[0])

    math_017 = nodes.new("ShaderNodeMath")
    math_017.name = "Math.017"
    math_017.label = ""
    math_017.location = (1109.0, -255.80029296875)
    math_017.bl_label = "Math"
    math_017.operation = "FLOORED_MODULO"
    math_017.use_clamp = False
    # Value
    math_017.inputs[1].default_value = 2.0
    # Value
    math_017.inputs[2].default_value = 0.5
    # Links for math_017
    links.new(math_017.outputs[0], boolean_math_005.inputs[0])
    links.new(capture_attribute_002.outputs[1], math_017.inputs[0])

    transform_geometry_040 = nodes.new("GeometryNodeTransform")
    transform_geometry_040.name = "Transform Geometry.040"
    transform_geometry_040.label = ""
    transform_geometry_040.location = (1209.0, -35.7998046875)
    transform_geometry_040.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_040.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_040.inputs[2].default_value = Vector((0.0, 0.0, 0.0007999999797903001))
    # Rotation
    transform_geometry_040.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_040.inputs[4].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))
    # Links for transform_geometry_040
    links.new(set_position_004.outputs[0], transform_geometry_040.inputs[0])
    links.new(transform_geometry_040.outputs[0], join_geometry_009.inputs[0])

    transform_geometry_041 = nodes.new("GeometryNodeTransform")
    transform_geometry_041.name = "Transform Geometry.041"
    transform_geometry_041.label = ""
    transform_geometry_041.location = (1409.0, -35.7998046875)
    transform_geometry_041.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_041.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_041.inputs[2].default_value = Vector((0.0, 0.0, 0.0007999999797903001))
    # Rotation
    transform_geometry_041.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_041.inputs[4].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))
    # Links for transform_geometry_041
    links.new(transform_geometry_040.outputs[0], transform_geometry_041.inputs[0])
    links.new(transform_geometry_041.outputs[0], join_geometry_009.inputs[0])

    scale_elements = nodes.new("GeometryNodeScaleElements")
    scale_elements.name = "Scale Elements"
    scale_elements.label = ""
    scale_elements.location = (2509.0, -155.7998046875)
    scale_elements.bl_label = "Scale Elements"
    scale_elements.domain = "FACE"
    # Selection
    scale_elements.inputs[1].default_value = True
    # Scale
    scale_elements.inputs[2].default_value = 1.2000000476837158
    # Center
    scale_elements.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Scale Mode
    scale_elements.inputs[4].default_value = "Uniform"
    # Axis
    scale_elements.inputs[5].default_value = [1.0, 0.0, 0.0]
    # Links for scale_elements
    links.new(join_geometry_007.outputs[0], scale_elements.inputs[0])

    transform_geometry_042 = nodes.new("GeometryNodeTransform")
    transform_geometry_042.name = "Transform Geometry.042"
    transform_geometry_042.label = ""
    transform_geometry_042.location = (2669.0, -155.7998046875)
    transform_geometry_042.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_042.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_042.inputs[2].default_value = Vector((0.0, 0.0, 0.0005000000237487257))
    # Rotation
    transform_geometry_042.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_042.inputs[4].default_value = Vector((1.0, 1.0, 0.7000000476837158))
    # Links for transform_geometry_042
    links.new(scale_elements.outputs[0], transform_geometry_042.inputs[0])

    join_geometry_023 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_023.name = "Join Geometry.023"
    join_geometry_023.label = ""
    join_geometry_023.location = (2669.0, -115.7998046875)
    join_geometry_023.bl_label = "Join Geometry"
    # Links for join_geometry_023
    links.new(join_geometry_023.outputs[0], store_named_attribute_006.inputs[0])
    links.new(join_geometry_009.outputs[0], join_geometry_023.inputs[0])
    links.new(transform_geometry_042.outputs[0], join_geometry_023.inputs[0])

    transform_geometry_043 = nodes.new("GeometryNodeTransform")
    transform_geometry_043.name = "Transform Geometry.043"
    transform_geometry_043.label = ""
    transform_geometry_043.location = (2669.0, -495.7998046875)
    transform_geometry_043.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_043.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_043.inputs[2].default_value = Vector((0.0, 0.0, 0.0005000000237487257))
    # Rotation
    transform_geometry_043.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_043.inputs[4].default_value = Vector((1.0, 1.0, 1.0))
    # Links for transform_geometry_043
    links.new(transform_geometry_043.outputs[0], store_named_attribute_005.inputs[0])
    links.new(join_geometry_007.outputs[0], transform_geometry_043.inputs[0])

    auto_layout_nodes(group)
    return group
