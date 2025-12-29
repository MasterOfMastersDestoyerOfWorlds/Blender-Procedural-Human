import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_rotate_cyclic_curve_group():
    group_name = "RotateCyclicCurve"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Curve", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Curve", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Count", in_out="INPUT", socket_type="NodeSocketInt"
    )
    socket.default_value = 16
    socket.min_value = 2 
    socket.max_value = 100000
    socket = group.interface.new_socket(
        name="Axis", in_out="INPUT", socket_type="NodeSocketVector"
    )
    socket.default_value = [0.0, 1.0, 0.0]
    socket.min_value = -1.0
    socket.max_value = 1.0
    socket = group.interface.new_socket(
        name="Center", in_out="INPUT", socket_type="NodeSocketVector"
    )
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Angle", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    socket.default_value = 0.5026547908782959
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = "re"
    group_output.location = (906.801025390625, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-887.198974609375, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    viewer = nodes.new("GeometryNodeViewer")
    viewer.name = "Viewer"
    viewer.label = ""
    viewer.location = (1374.9971923828125, -165.81289672851562)
    viewer.bl_label = "Viewer"
    viewer.ui_shortcut = 0
    viewer.active_index = 0
    viewer.domain = "AUTO"
    # Links for viewer

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (798.1805419921875, -183.06088256835938)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001

    vector_rotate = nodes.new("ShaderNodeVectorRotate")
    vector_rotate.name = "Vector Rotate"
    vector_rotate.label = "re"
    vector_rotate.location = (308.85302734375, -35.797454833984375)
    vector_rotate.bl_label = "Vector Rotate"
    vector_rotate.rotation_type = "AXIS_ANGLE"
    vector_rotate.invert = False
    # Rotation
    vector_rotate.inputs[4].default_value = Euler((0.0, 0.0, 0.0), "XYZ")
    # Links for vector_rotate
    links.new(vector_rotate.outputs[0], set_position_001.inputs[2])
    links.new(group_input.outputs[2], vector_rotate.inputs[2])
    links.new(group_input.outputs[3], vector_rotate.inputs[1])
    links.new(group_input.outputs[4], vector_rotate.inputs[3])

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (513.981689453125, -249.37582397460938)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "COUNT"
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points
    links.new(curve_to_points.outputs[0], set_position_001.inputs[0])
    links.new(group_input.outputs[0], curve_to_points.inputs[0])
    links.new(group_input.outputs[1], curve_to_points.inputs[1])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (30.323974609375, -237.89010620117188)
    position_001.bl_label = "Position"
    # Links for position_001
    links.new(position_001.outputs[0], vector_rotate.inputs[0])

    points_to_curves = nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    points_to_curves.label = ""
    points_to_curves.location = (1014.511474609375, -152.83877563476562)
    points_to_curves.bl_label = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0
    # Weight
    points_to_curves.inputs[2].default_value = 0.0
    # Links for points_to_curves
    links.new(set_position_001.outputs[0], points_to_curves.inputs[0])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    set_spline_cyclic.label = ""
    set_spline_cyclic.location = (1194.599365234375, -150.70260620117188)
    set_spline_cyclic.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = True
    # Links for set_spline_cyclic
    links.new(points_to_curves.outputs[0], set_spline_cyclic.inputs[0])
    links.new(set_spline_cyclic.outputs[0], group_output.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Rotate Cyclic Curve"
    frame.location = (-587.0, 200.0)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_sample_curve_distances_group():
    group_name = "SampleCurveDistances"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Value", in_out="OUTPUT", socket_type="NodeSocketVector"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Value", in_out="OUTPUT", socket_type="NodeSocketFloat"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Curve", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Index", in_out="INPUT", socket_type="NodeSocketInt"
    )
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(
        name="Count", in_out="INPUT", socket_type="NodeSocketInt"
    )
    socket.default_value = 64
    socket.min_value = 2
    socket.max_value = 100000

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (853.70068359375, 140.80035400390625)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-703.9666748046875, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    curve_to_points = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.label = ""
    curve_to_points.location = (-279.7032775878906, 201.56521606445312)
    curve_to_points.bl_label = "Curve to Points"
    curve_to_points.mode = "COUNT"
    # Length
    curve_to_points.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points
    links.new(group_input.outputs[0], curve_to_points.inputs[0])
    links.new(group_input.outputs[2], curve_to_points.inputs[1])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (-94.98046875, -176.63214111328125)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "DISTANCE"
    # Vector
    vector_math.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(vector_math.outputs[1], group_output.inputs[2])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (-369.3836669921875, -109.30762481689453)
    position_002.bl_label = "Position"
    # Links for position_002
    links.new(position_002.outputs[0], vector_math.inputs[0])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (-99.20317840576172, -12.244603157043457)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "NORMALIZE"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(position_002.outputs[0], vector_math_001.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (271.75421142578125, 157.68020629882812)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001
    links.new(curve_to_points.outputs[0], set_position_001.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (207.74887084960938, -20.179344177246094)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_002
    links.new(vector_math.outputs[1], vector_math_002.inputs[3])
    links.new(vector_math_002.outputs[0], set_position_001.inputs[2])
    links.new(vector_math_001.outputs[0], vector_math_002.inputs[0])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (500.01690673828125, 84.99751281738281)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Links for sample_index
    links.new(curve_to_points.outputs[0], sample_index.inputs[0])
    links.new(group_input.outputs[1], sample_index.inputs[2])
    links.new(sample_index.outputs[0], group_output.inputs[0])
    links.new(vector_math_002.outputs[0], sample_index.inputs[1])

    vector = nodes.new("FunctionNodeInputVector")
    vector.name = "Vector"
    vector.label = ""
    vector.location = (-440.4152526855469, -193.17086791992188)
    vector.bl_label = "Vector"
    vector.vector = Vector((0.0, 0.0, 0.0))
    # Links for vector

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (-81.5783920288086, 356.9877624511719)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "POINTCLOUD"
    # Links for domain_size
    links.new(curve_to_points.outputs[0], domain_size.inputs[0])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (-178.65699768066406, 422.7564697265625)
    index.bl_label = "Index"
    # Links for index

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (136.92100524902344, 455.71826171875)
    math.bl_label = "Math"
    math.operation = "DIVIDE"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(domain_size.outputs[0], math.inputs[1])
    links.new(index.outputs[0], math.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (389.52740478515625, 405.97601318359375)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "FLOAT"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "t"
    # Links for store_named_attribute
    links.new(curve_to_points.outputs[0], store_named_attribute.inputs[0])
    links.new(math.outputs[0], store_named_attribute.inputs[3])
    links.new(store_named_attribute.outputs[0], group_output.inputs[1])

    viewer = nodes.new("GeometryNodeViewer")
    viewer.name = "Viewer"
    viewer.label = ""
    viewer.location = (692.1257934570312, 376.59674072265625)
    viewer.bl_label = "Viewer"
    viewer.ui_shortcut = 0
    viewer.active_index = 0
    viewer.domain = "AUTO"
    # Links for viewer
    links.new(store_named_attribute.outputs[0], viewer.inputs[0])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_get_center_curve_group():
    group_name = "GetCenterCurve"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Result", in_out="OUTPUT", socket_type="NodeSocketVector"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (300.5806884765625, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-310.580810546875, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    bounding_box.label = ""
    bounding_box.location = (-110.580810546875, -43.05302429199219)
    bounding_box.bl_label = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = True
    # Links for bounding_box
    links.new(group_input.outputs[0], bounding_box.inputs[0])

    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.label = ""
    mix_001.location = (110.5806884765625, 43.05303955078125)
    mix_001.bl_label = "Mix"
    mix_001.data_type = "VECTOR"
    mix_001.factor_mode = "UNIFORM"
    mix_001.blend_type = "MIX"
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    # Factor
    mix_001.inputs[0].default_value = 0.5
    # Factor
    mix_001.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_001.inputs[2].default_value = 0.0
    # B
    mix_001.inputs[3].default_value = 0.0
    # A
    mix_001.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_001.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_001.inputs[8].default_value = Euler((0.0, 0.0, 0.0), "XYZ")
    # B
    mix_001.inputs[9].default_value = Euler((0.0, 0.0, 0.0), "XYZ")
    # Links for mix_001
    links.new(bounding_box.outputs[2], mix_001.inputs[5])
    links.new(bounding_box.outputs[1], mix_001.inputs[4])
    links.new(mix_001.outputs[1], group_output.inputs[0])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_closest_index_points_group():
    group_name = "ClosestIndexPoints"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Min", in_out="OUTPUT", socket_type="NodeSocketInt"
    )
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (875.7348022460938, -64.79780578613281)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-480.4573974609375, -33.79435729980469)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[1], group_output.inputs[1])

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.label = ""
    attribute_statistic.location = (88.55728149414062, 159.94671630859375)
    attribute_statistic.bl_label = "Attribute Statistic"
    attribute_statistic.data_type = "FLOAT"
    attribute_statistic.domain = "POINT"
    # Selection
    attribute_statistic.inputs[1].default_value = True
    # Links for attribute_statistic
    links.new(group_input.outputs[1], attribute_statistic.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (-176.77639770507812, -142.14071655273438)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "POINTS"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity
    links.new(geometry_proximity.outputs[1], attribute_statistic.inputs[2])
    links.new(group_input.outputs[0], geometry_proximity.inputs[0])

    viewer_001 = nodes.new("GeometryNodeViewer")
    viewer_001.name = "Viewer.001"
    viewer_001.label = ""
    viewer_001.location = (898.151611328125, 103.5215072631836)
    viewer_001.bl_label = "Viewer"
    viewer_001.ui_shortcut = 0
    viewer_001.active_index = 0
    viewer_001.domain = "AUTO"
    # Links for viewer_001

    attribute_statistic_001 = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_001.name = "Attribute Statistic.001"
    attribute_statistic_001.label = ""
    attribute_statistic_001.location = (478.6709899902344, 160.69068908691406)
    attribute_statistic_001.bl_label = "Attribute Statistic"
    attribute_statistic_001.data_type = "FLOAT"
    attribute_statistic_001.domain = "POINT"
    # Links for attribute_statistic_001
    links.new(group_input.outputs[1], attribute_statistic_001.inputs[0])
    links.new(attribute_statistic_001.outputs[3], viewer_001.inputs[0])
    links.new(attribute_statistic_001.outputs[3], group_output.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (357.97802734375, -170.44155883789062)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # A
    compare.inputs[2].default_value = 0
    # B
    compare.inputs[3].default_value = 0
    # A
    compare.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    compare.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    compare.inputs[6].default_value = [
        0.800000011920929,
        0.800000011920929,
        0.800000011920929,
        1.0,
    ]
    # B
    compare.inputs[7].default_value = [
        0.800000011920929,
        0.800000011920929,
        0.800000011920929,
        1.0,
    ]
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
    links.new(compare.outputs[0], attribute_statistic_001.inputs[1])
    links.new(attribute_statistic.outputs[3], compare.inputs[1])
    links.new(geometry_proximity.outputs[1], compare.inputs[0])

    index_003 = nodes.new("GeometryNodeInputIndex")
    index_003.name = "Index.003"
    index_003.label = ""
    index_003.location = (245.71279907226562, 101.55435180664062)
    index_003.bl_label = "Index"
    # Links for index_003
    links.new(index_003.outputs[0], attribute_statistic_001.inputs[2])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_get_index_offset_group():
    group_name = "GetIndexOffset"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Min", in_out="OUTPUT", socket_type="NodeSocketInt"
    )
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(
        name="Index Offset", in_out="OUTPUT", socket_type="NodeSocketInt"
    )
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Min", in_out="OUTPUT", socket_type="NodeSocketInt"
    )
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(
        name="Index Offset", in_out="OUTPUT", socket_type="NodeSocketInt"
    )
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Value", in_out="INPUT", socket_type="NodeSocketInt"
    )
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (451.0545654296875, -14.581380844116211)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-714.971435546875, -40.50383758544922)
    group_input.bl_label = "Group Input"
    # Links for group_input

    closest_index_points = nodes.new("GeometryNodeGroup")
    closest_index_points.name = "Group.002"
    closest_index_points.label = ""
    closest_index_points.location = (-366.0711669921875, 75.27714538574219)
    closest_index_points.node_tree = create_closest_index_points_group()
    closest_index_points.bl_label = "Group"
    # Links for closest_index_points
    links.new(group_input.outputs[1], closest_index_points.inputs[1])
    links.new(group_input.outputs[0], closest_index_points.inputs[0])
    links.new(closest_index_points.outputs[1], group_output.inputs[0])
    links.new(closest_index_points.outputs[0], group_output.inputs[1])

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (-12.075698852539062, -157.56106567382812)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "POINTCLOUD"
    # Links for domain_size
    links.new(group_input.outputs[1], domain_size.inputs[0])

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (-10.634254455566406, -266.283203125)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "SUBTRACT"
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(group_input.outputs[2], integer_math.inputs[0])

    integer_math_001 = nodes.new("FunctionNodeIntegerMath")
    integer_math_001.name = "Integer Math.001"
    integer_math_001.label = ""
    integer_math_001.location = (191.51043701171875, -183.6558380126953)
    integer_math_001.bl_label = "Integer Math"
    integer_math_001.operation = "FLOORED_MODULO"
    # Value
    integer_math_001.inputs[2].default_value = 0
    # Links for integer_math_001
    links.new(domain_size.outputs[0], integer_math_001.inputs[1])
    links.new(integer_math.outputs[0], integer_math_001.inputs[0])
    links.new(integer_math_001.outputs[0], group_output.inputs[5])

    closest_index_points_1 = nodes.new("GeometryNodeGroup")
    closest_index_points_1.name = "Group.006"
    closest_index_points_1.label = ""
    closest_index_points_1.location = (-502.394287109375, -223.20584106445312)
    closest_index_points_1.node_tree = create_closest_index_points_group()
    closest_index_points_1.bl_label = "Group"
    # Links for closest_index_points_1
    links.new(group_input.outputs[1], closest_index_points_1.inputs[0])
    links.new(group_input.outputs[0], closest_index_points_1.inputs[1])
    links.new(closest_index_points_1.outputs[0], group_output.inputs[4])
    links.new(closest_index_points_1.outputs[1], group_output.inputs[3])
    links.new(closest_index_points_1.outputs[0], integer_math.inputs[1])

    domain_size_001 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_001.name = "Domain Size.001"
    domain_size_001.label = ""
    domain_size_001.location = (-30.79648208618164, 259.3493347167969)
    domain_size_001.bl_label = "Domain Size"
    domain_size_001.component = "POINTCLOUD"
    # Links for domain_size_001
    links.new(closest_index_points.outputs[1], domain_size_001.inputs[0])

    integer_math_002 = nodes.new("FunctionNodeIntegerMath")
    integer_math_002.name = "Integer Math.002"
    integer_math_002.label = ""
    integer_math_002.location = (-29.355037689208984, 150.627197265625)
    integer_math_002.bl_label = "Integer Math"
    integer_math_002.operation = "SUBTRACT"
    # Value
    integer_math_002.inputs[2].default_value = 0
    # Links for integer_math_002
    links.new(group_input.outputs[2], integer_math_002.inputs[0])
    links.new(closest_index_points.outputs[0], integer_math_002.inputs[1])

    integer_math_003 = nodes.new("FunctionNodeIntegerMath")
    integer_math_003.name = "Integer Math.003"
    integer_math_003.label = ""
    integer_math_003.location = (172.78965759277344, 233.2545623779297)
    integer_math_003.bl_label = "Integer Math"
    integer_math_003.operation = "FLOORED_MODULO"
    # Value
    integer_math_003.inputs[2].default_value = 0
    # Links for integer_math_003
    links.new(domain_size_001.outputs[0], integer_math_003.inputs[1])
    links.new(integer_math_002.outputs[0], integer_math_003.inputs[0])
    links.new(integer_math_003.outputs[0], group_output.inputs[2])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_morph_curve_to_curve_group():
    group_name = "MorphCurveToCurve"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Scale", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    socket.default_value = 1.0
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(
        name="Index", in_out="INPUT", socket_type="NodeSocketInt"
    )
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(
        name="Normal", in_out="INPUT", socket_type="NodeSocketVector"
    )
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (872.06103515625, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-882.06103515625, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    set_position_004 = nodes.new("GeometryNodeSetPosition")
    set_position_004.name = "Set Position.004"
    set_position_004.label = ""
    set_position_004.location = (682.06103515625, 221.8826904296875)
    set_position_004.bl_label = "Set Position"
    # Selection
    set_position_004.inputs[1].default_value = True
    # Offset
    set_position_004.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_004
    links.new(group_input.outputs[0], set_position_004.inputs[0])
    links.new(set_position_004.outputs[0], group_output.inputs[0])

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (-774.0696411132812, -212.8158416748047)
    position_003.bl_label = "Position"
    # Links for position_003

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (-543.3536376953125, -156.01107788085938)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "NORMALIZE"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(position_003.outputs[0], vector_math_001.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (-111.69979858398438, 230.81773376464844)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_002
    links.new(group_input.outputs[1], vector_math_002.inputs[3])

    vector_rotate_001 = nodes.new("ShaderNodeVectorRotate")
    vector_rotate_001.name = "Vector Rotate.001"
    vector_rotate_001.label = ""
    vector_rotate_001.location = (322.24505615234375, 177.58984375)
    vector_rotate_001.bl_label = "Vector Rotate"
    vector_rotate_001.rotation_type = "AXIS_ANGLE"
    vector_rotate_001.invert = False
    # Center
    vector_rotate_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Axis
    vector_rotate_001.inputs[2].default_value = [0.0, 1.0, 0.0]
    # Angle
    vector_rotate_001.inputs[3].default_value = 0.0
    # Rotation
    vector_rotate_001.inputs[4].default_value = Euler((0.0, 0.0, 0.0), "XYZ")
    # Links for vector_rotate_001
    links.new(vector_rotate_001.outputs[0], set_position_004.inputs[2])

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.name = "Sample Index.005"
    sample_index_005.label = ""
    sample_index_005.location = (-53.836883544921875, 49.65673828125)
    sample_index_005.bl_label = "Sample Index"
    sample_index_005.data_type = "FLOAT_VECTOR"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    # Links for sample_index_005
    links.new(sample_index_005.outputs[0], vector_rotate_001.inputs[0])
    links.new(group_input.outputs[0], sample_index_005.inputs[0])
    links.new(group_input.outputs[2], sample_index_005.inputs[2])
    links.new(vector_math_002.outputs[0], sample_index_005.inputs[1])

    sample_index_006 = nodes.new("GeometryNodeSampleIndex")
    sample_index_006.name = "Sample Index.006"
    sample_index_006.label = ""
    sample_index_006.location = (-356.5566711425781, -31.397838592529297)
    sample_index_006.bl_label = "Sample Index"
    sample_index_006.data_type = "FLOAT_VECTOR"
    sample_index_006.domain = "POINT"
    sample_index_006.clamp = False
    # Links for sample_index_006
    links.new(vector_math_001.outputs[0], sample_index_006.inputs[1])
    links.new(sample_index_006.outputs[0], vector_math_002.inputs[0])
    links.new(group_input.outputs[0], sample_index_006.inputs[0])
    links.new(group_input.outputs[2], sample_index_006.inputs[2])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_loop_normal_vector_group():
    group_name = "LoopNormalVector"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Vector", in_out="OUTPUT", socket_type="NodeSocketVector"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Index", in_out="INPUT", socket_type="NodeSocketInt"
    )
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1839.8212890625, 428.323486328125)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-484.7840270996094, 94.83818054199219)
    group_input.bl_label = "Group Input"
    # Links for group_input

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (32.85664367675781, -177.16058349609375)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "ADD"
    # Value
    integer_math.inputs[1].default_value = 1
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math
    links.new(group_input.outputs[0], integer_math.inputs[0])

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (234.97552490234375, -36.091949462890625)
    position_003.bl_label = "Position"
    # Links for position_003

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (438.3837585449219, -40.103485107421875)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Links for sample_index
    links.new(position_003.outputs[0], sample_index.inputs[1])

    integer_math_001 = nodes.new("FunctionNodeIntegerMath")
    integer_math_001.name = "Integer Math.001"
    integer_math_001.label = ""
    integer_math_001.location = (226.43252563476562, -139.78411865234375)
    integer_math_001.bl_label = "Integer Math"
    integer_math_001.operation = "MODULO"
    # Value
    integer_math_001.inputs[2].default_value = 0
    # Links for integer_math_001
    links.new(integer_math.outputs[0], integer_math_001.inputs[0])
    links.new(integer_math_001.outputs[0], sample_index.inputs[2])

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (29.741722106933594, -73.76312255859375)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "POINTCLOUD"
    # Links for domain_size
    links.new(domain_size.outputs[0], integer_math_001.inputs[1])
    links.new(group_input.outputs[1], domain_size.inputs[0])

    position_004 = nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"
    position_004.label = ""
    position_004.location = (29.751815795898438, -113.363037109375)
    position_004.bl_label = "Position"
    # Links for position_004

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (262.7493591308594, -35.527587890625)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001
    links.new(position_004.outputs[0], sample_index_001.inputs[1])
    links.new(group_input.outputs[0], sample_index_001.inputs[2])
    links.new(group_input.outputs[1], sample_index_001.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (663.7770385742188, -144.79534912109375)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "SUBTRACT"
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(sample_index_001.outputs[0], vector_math.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "i+1"
    frame.location = (30.0, -332.0)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "i"
    frame_001.location = (169.0, -36.0)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "e[i]"
    frame_002.location = (-84.0, 776.0)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (1050.1224365234375, 371.6311950683594)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "CROSS_PRODUCT"
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(vector_math.outputs[0], vector_math_002.inputs[0])

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.label = ""
    attribute_statistic.location = (1246.830078125, 657.2858276367188)
    attribute_statistic.bl_label = "Attribute Statistic"
    attribute_statistic.data_type = "FLOAT_VECTOR"
    attribute_statistic.domain = "POINT"
    # Selection
    attribute_statistic.inputs[1].default_value = True
    # Links for attribute_statistic
    links.new(vector_math_002.outputs[0], attribute_statistic.inputs[2])
    links.new(group_input.outputs[1], attribute_statistic.inputs[0])

    attribute_statistic_001 = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_001.name = "Attribute Statistic.001"
    attribute_statistic_001.label = ""
    attribute_statistic_001.location = (247.00067138671875, 47.819068908691406)
    attribute_statistic_001.bl_label = "Attribute Statistic"
    attribute_statistic_001.data_type = "FLOAT_VECTOR"
    attribute_statistic_001.domain = "POINT"
    # Selection
    attribute_statistic_001.inputs[1].default_value = True
    # Links for attribute_statistic_001
    links.new(group_input.outputs[1], attribute_statistic_001.inputs[0])
    links.new(attribute_statistic_001.outputs[0], vector_math.inputs[1])

    position_005 = nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"
    position_005.label = ""
    position_005.location = (-141.09368896484375, -180.7404327392578)
    position_005.bl_label = "Position"
    # Links for position_005
    links.new(position_005.outputs[0], attribute_statistic_001.inputs[2])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (800.6077270507812, -424.5738220214844)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "SUBTRACT"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(vector_math_001.outputs[0], vector_math_002.inputs[1])
    links.new(sample_index.outputs[0], vector_math_001.inputs[0])
    links.new(attribute_statistic_001.outputs[0], vector_math_001.inputs[1])

    vector_math_012 = nodes.new("ShaderNodeVectorMath")
    vector_math_012.name = "Vector Math.012"
    vector_math_012.label = ""
    vector_math_012.location = (1512.6114501953125, 505.3103332519531)
    vector_math_012.bl_label = "Vector Math"
    vector_math_012.operation = "NORMALIZE"
    # Vector
    vector_math_012.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_012.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_012.inputs[3].default_value = 1.0
    # Links for vector_math_012
    links.new(vector_math_012.outputs[0], group_output.inputs[0])
    links.new(attribute_statistic.outputs[4], vector_math_012.inputs[0])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_perpendicular_vectors_group():
    group_name = "PerpendicularVectors"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Center", in_out="OUTPUT", socket_type="NodeSocketVector"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="U", in_out="OUTPUT", socket_type="NodeSocketVector"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="V", in_out="OUTPUT", socket_type="NodeSocketVector"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Normal", in_out="INPUT", socket_type="NodeSocketVector"
    )
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (751.6455688476562, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-731.3544311523438, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (29.5478515625, -36.42059326171875)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "CROSS_PRODUCT"
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006
    links.new(group_input.outputs[0], vector_math_006.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "V"
    frame_001.location = (264.0, -346.0)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    position_004 = nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"
    position_004.label = ""
    position_004.location = (29.58050537109375, -375.744140625)
    position_004.bl_label = "Position"
    # Links for position_004

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.label = ""
    attribute_statistic.location = (277.29510498046875, -325.97039794921875)
    attribute_statistic.bl_label = "Attribute Statistic"
    attribute_statistic.data_type = "FLOAT_VECTOR"
    attribute_statistic.domain = "POINT"
    # Selection
    attribute_statistic.inputs[1].default_value = True
    # Links for attribute_statistic
    links.new(position_004.outputs[0], attribute_statistic.inputs[2])
    links.new(group_input.outputs[1], attribute_statistic.inputs[0])
    links.new(attribute_statistic.outputs[0], group_output.inputs[0])

    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.label = ""
    sample_index.location = (206.79583740234375, -36.42279052734375)
    sample_index.bl_label = "Sample Index"
    sample_index.data_type = "FLOAT_VECTOR"
    sample_index.domain = "POINT"
    sample_index.clamp = False
    # Index
    sample_index.inputs[2].default_value = 0
    # Links for sample_index
    links.new(position_004.outputs[0], sample_index.inputs[1])
    links.new(group_input.outputs[1], sample_index.inputs[0])

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Uraw"
    frame_002.location = (30.0, -36.0)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    vector_math_014 = nodes.new("ShaderNodeVectorMath")
    vector_math_014.name = "Vector Math.014"
    vector_math_014.label = ""
    vector_math_014.location = (444.80450439453125, -186.4271240234375)
    vector_math_014.bl_label = "Vector Math"
    vector_math_014.operation = "SUBTRACT"
    # Vector
    vector_math_014.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_014.inputs[3].default_value = 1.0
    # Links for vector_math_014
    links.new(attribute_statistic.outputs[0], vector_math_014.inputs[1])
    links.new(sample_index.outputs[0], vector_math_014.inputs[0])

    vector_math_015 = nodes.new("ShaderNodeVectorMath")
    vector_math_015.name = "Vector Math.015"
    vector_math_015.label = ""
    vector_math_015.location = (804.020263671875, -165.089111328125)
    vector_math_015.bl_label = "Vector Math"
    vector_math_015.operation = "SUBTRACT"
    # Vector
    vector_math_015.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_015.inputs[3].default_value = 1.0
    # Links for vector_math_015
    links.new(vector_math_014.outputs[0], vector_math_015.inputs[0])

    vector_math_016 = nodes.new("ShaderNodeVectorMath")
    vector_math_016.name = "Vector Math.016"
    vector_math_016.label = ""
    vector_math_016.location = (1035.5938720703125, -193.7757568359375)
    vector_math_016.bl_label = "Vector Math"
    vector_math_016.operation = "NORMALIZE"
    # Vector
    vector_math_016.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_016.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_016.inputs[3].default_value = 1.0
    # Links for vector_math_016
    links.new(vector_math_015.outputs[0], vector_math_016.inputs[0])
    links.new(vector_math_016.outputs[0], vector_math_006.inputs[1])
    links.new(vector_math_016.outputs[0], group_output.inputs[1])

    vector_math_017 = nodes.new("ShaderNodeVectorMath")
    vector_math_017.name = "Vector Math.017"
    vector_math_017.label = ""
    vector_math_017.location = (709.3302001953125, -377.52154541015625)
    vector_math_017.bl_label = "Vector Math"
    vector_math_017.operation = "DOT_PRODUCT"
    # Vector
    vector_math_017.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_017.inputs[3].default_value = 1.0
    # Links for vector_math_017
    links.new(vector_math_014.outputs[0], vector_math_017.inputs[0])
    links.new(group_input.outputs[0], vector_math_017.inputs[1])

    vector_math_018 = nodes.new("ShaderNodeVectorMath")
    vector_math_018.name = "Vector Math.018"
    vector_math_018.label = ""
    vector_math_018.location = (856.9280395507812, -361.20245361328125)
    vector_math_018.bl_label = "Vector Math"
    vector_math_018.operation = "SCALE"
    # Vector
    vector_math_018.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_018.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_018
    links.new(vector_math_018.outputs[0], vector_math_015.inputs[1])
    links.new(vector_math_017.outputs[1], vector_math_018.inputs[3])
    links.new(group_input.outputs[0], vector_math_018.inputs[0])

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "U"
    frame_003.location = (-531.0, 405.0)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    vector_math_019 = nodes.new("ShaderNodeVectorMath")
    vector_math_019.name = "Vector Math.019"
    vector_math_019.label = ""
    vector_math_019.location = (267.35443115234375, -58.34832763671875)
    vector_math_019.bl_label = "Vector Math"
    vector_math_019.operation = "NORMALIZE"
    # Vector
    vector_math_019.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_019.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_019.inputs[3].default_value = 1.0
    # Links for vector_math_019
    links.new(vector_math_006.outputs[0], vector_math_019.inputs[0])
    links.new(vector_math_019.outputs[0], group_output.inputs[2])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_vector_angles_group():
    group_name = "VectorAngles"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Normal", in_out="OUTPUT", socket_type="NodeSocketVector"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Inclination", in_out="OUTPUT", socket_type="NodeSocketFloat"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Asimuth", in_out="OUTPUT", socket_type="NodeSocketFloat"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="u", in_out="OUTPUT", socket_type="NodeSocketVector"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="v", in_out="OUTPUT", socket_type="NodeSocketVector"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="length", in_out="OUTPUT", socket_type="NodeSocketFloat"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="center", in_out="OUTPUT", socket_type="NodeSocketVector"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Index", in_out="INPUT", socket_type="NodeSocketInt"
    )
    socket.default_value = 159
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1315.0655517578125, -287.92340087890625)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-1297.44482421875, 119.60213470458984)
    group_input.bl_label = "Group Input"
    # Links for group_input

    position_003 = nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    position_003.label = ""
    position_003.location = (-949.1030883789062, -198.9227294921875)
    position_003.bl_label = "Position"
    # Links for position_003

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.name = "Sample Index.005"
    sample_index_005.label = ""
    sample_index_005.location = (-769.1713256835938, -115.09825897216797)
    sample_index_005.bl_label = "Sample Index"
    sample_index_005.data_type = "FLOAT_VECTOR"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    # Links for sample_index_005
    links.new(position_003.outputs[0], sample_index_005.inputs[1])
    links.new(group_input.outputs[0], sample_index_005.inputs[0])
    links.new(group_input.outputs[1], sample_index_005.inputs[2])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (-325.8828125, 107.03775024414062)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "DOT_PRODUCT"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(sample_index_005.outputs[0], vector_math_001.inputs[1])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (162.79904174804688, -75.94014739990234)
    math.bl_label = "Math"
    math.operation = "ARCCOSINE"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.5
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(math.outputs[0], group_output.inputs[1])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-23.060680389404297, -16.37787628173828)
    math_001.bl_label = "Math"
    math_001.operation = "DIVIDE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math_001.outputs[0], math.inputs[0])
    links.new(vector_math_001.outputs[1], math_001.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (-413.2942199707031, -180.05311584472656)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "LENGTH"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (-226.5164794921875, -102.05669403076172)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(vector_math_002.outputs[1], math_002.inputs[0])
    links.new(math_002.outputs[0], math_001.inputs[1])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (-409.4824523925781, -63.577354431152344)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "LENGTH"
    # Vector
    vector_math_003.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(vector_math_003.outputs[1], math_002.inputs[1])
    links.new(sample_index_005.outputs[0], vector_math_003.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (-441.00006103515625, -466.3115234375)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketVector"
    # Links for reroute

    vector_math_007 = nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.label = ""
    vector_math_007.location = (-82.20596313476562, -1099.1424560546875)
    vector_math_007.bl_label = "Vector Math"
    vector_math_007.operation = "SUBTRACT"
    # Vector
    vector_math_007.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_007.inputs[3].default_value = 1.0
    # Links for vector_math_007

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (-463.0, -881.9312744140625)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketVector"
    # Links for reroute_001
    links.new(reroute_001.outputs[0], vector_math_007.inputs[0])
    links.new(sample_index_005.outputs[0], reroute_001.inputs[0])

    vector_math_008 = nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.label = ""
    vector_math_008.location = (-411.4500427246094, -1089.5032958984375)
    vector_math_008.bl_label = "Vector Math"
    vector_math_008.operation = "DOT_PRODUCT"
    # Vector
    vector_math_008.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_008.inputs[3].default_value = 1.0
    # Links for vector_math_008
    links.new(reroute_001.outputs[0], vector_math_008.inputs[0])
    links.new(reroute.outputs[0], vector_math_008.inputs[1])

    vector_math_009 = nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.label = ""
    vector_math_009.location = (-263.1983947753906, -1050.4158935546875)
    vector_math_009.bl_label = "Vector Math"
    vector_math_009.operation = "SCALE"
    # Vector
    vector_math_009.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_009.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_009
    links.new(vector_math_008.outputs[1], vector_math_009.inputs[3])
    links.new(reroute.outputs[0], vector_math_009.inputs[0])
    links.new(vector_math_009.outputs[0], vector_math_007.inputs[1])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (1095.6085205078125, -505.3965148925781)
    math_004.bl_label = "Math"
    math_004.operation = "ARCTAN2"
    math_004.use_clamp = False
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(math_004.outputs[0], group_output.inputs[2])

    vector_math_010 = nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.label = ""
    vector_math_010.location = (872.9500122070312, -592.1559448242188)
    vector_math_010.bl_label = "Vector Math"
    vector_math_010.operation = "DOT_PRODUCT"
    # Vector
    vector_math_010.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_010.inputs[3].default_value = 1.0
    # Links for vector_math_010
    links.new(vector_math_007.outputs[0], vector_math_010.inputs[0])
    links.new(vector_math_010.outputs[1], math_004.inputs[0])

    vector_math_011 = nodes.new("ShaderNodeVectorMath")
    vector_math_011.name = "Vector Math.011"
    vector_math_011.label = ""
    vector_math_011.location = (872.9500122070312, -792.66650390625)
    vector_math_011.bl_label = "Vector Math"
    vector_math_011.operation = "DOT_PRODUCT"
    # Vector
    vector_math_011.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_011.inputs[3].default_value = 1.0
    # Links for vector_math_011
    links.new(vector_math_007.outputs[0], vector_math_011.inputs[0])
    links.new(vector_math_011.outputs[1], math_004.inputs[1])

    loop_normal_vector = nodes.new("GeometryNodeGroup")
    loop_normal_vector.name = "Group.003"
    loop_normal_vector.label = ""
    loop_normal_vector.location = (-955.8082275390625, 322.36871337890625)
    loop_normal_vector.node_tree = create_loop_normal_vector_group()
    loop_normal_vector.bl_label = "Group"
    # Links for loop_normal_vector
    links.new(loop_normal_vector.outputs[0], group_output.inputs[0])
    links.new(loop_normal_vector.outputs[0], vector_math_001.inputs[0])
    links.new(loop_normal_vector.outputs[0], vector_math_002.inputs[0])
    links.new(loop_normal_vector.outputs[0], reroute.inputs[0])
    links.new(group_input.outputs[0], loop_normal_vector.inputs[1])
    links.new(group_input.outputs[1], loop_normal_vector.inputs[0])

    vector_math_012 = nodes.new("ShaderNodeVectorMath")
    vector_math_012.name = "Vector Math.012"
    vector_math_012.label = ""
    vector_math_012.location = (203.12255859375, 230.5105438232422)
    vector_math_012.bl_label = "Vector Math"
    vector_math_012.operation = "LENGTH"
    # Vector
    vector_math_012.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_012.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_012.inputs[3].default_value = 1.0
    # Links for vector_math_012
    links.new(sample_index_005.outputs[0], vector_math_012.inputs[0])
    links.new(vector_math_012.outputs[1], group_output.inputs[5])

    perpendicular_vectors = nodes.new("GeometryNodeGroup")
    perpendicular_vectors.name = "Group"
    perpendicular_vectors.label = ""
    perpendicular_vectors.location = (168.35443115234375, -630.3483276367188)
    perpendicular_vectors.node_tree = create_perpendicular_vectors_group()
    perpendicular_vectors.bl_label = "Group"
    # Links for perpendicular_vectors
    links.new(perpendicular_vectors.outputs[1], vector_math_011.inputs[1])
    links.new(perpendicular_vectors.outputs[0], group_output.inputs[6])
    links.new(perpendicular_vectors.outputs[2], vector_math_010.inputs[1])
    links.new(group_input.outputs[0], perpendicular_vectors.inputs[1])
    links.new(reroute.outputs[0], perpendicular_vectors.inputs[0])
    links.new(perpendicular_vectors.outputs[1], group_output.inputs[3])
    links.new(perpendicular_vectors.outputs[2], group_output.inputs[4])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_construct_vector_group():
    group_name = "ConstructVector"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Vector", in_out="OUTPUT", socket_type="NodeSocketVector"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Normal", in_out="INPUT", socket_type="NodeSocketVector"
    )
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(
        name="Inclination", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    socket.default_value = 0.5
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(
        name="Azimuth", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    socket.default_value = 0.5
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(
        name="u", in_out="INPUT", socket_type="NodeSocketVector"
    )
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(
        name="v", in_out="INPUT", socket_type="NodeSocketVector"
    )
    socket.default_value = [0.0, 0.0, 0.0]
    socket.min_value = -10000.0
    socket.max_value = 10000.0
    socket = group.interface.new_socket(
        name="length", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    socket.default_value = 1.0
    socket.min_value = -10000.0
    socket.max_value = 10000.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (649.7435913085938, -8.821724891662598)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-984.1678466796875, -15.879104614257812)
    group_input.bl_label = "Group Input"
    # Links for group_input

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-558.4098510742188, 291.6924743652344)
    math.bl_label = "Math"
    math.operation = "COSINE"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 0.5
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(group_input.outputs[2], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-558.409912109375, 156.14988708496094)
    math_001.bl_label = "Math"
    math_001.operation = "SINE"
    math_001.use_clamp = False
    # Value
    math_001.inputs[1].default_value = 0.5
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(group_input.outputs[1], math_001.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (-348.3465576171875, 249.7794952392578)
    math_002.bl_label = "Math"
    math_002.operation = "MULTIPLY"
    math_002.use_clamp = False
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(math_001.outputs[0], math_002.inputs[0])
    links.new(math.outputs[0], math_002.inputs[1])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (-181.99456787109375, 174.4263153076172)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "SCALE"
    # Vector
    vector_math_001.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_001
    links.new(math_002.outputs[0], vector_math_001.inputs[3])
    links.new(group_input.outputs[3], vector_math_001.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (14.837173461914062, 109.81389617919922)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "ADD"
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 1.0
    # Links for vector_math_002
    links.new(vector_math_001.outputs[0], vector_math_002.inputs[0])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (-565.5341796875, 6.339285850524902)
    math_004.bl_label = "Math"
    math_004.operation = "SINE"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 0.5
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(group_input.outputs[1], math_004.inputs[0])

    math_006 = nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.label = ""
    math_006.location = (-560.1909790039062, -139.90406799316406)
    math_006.bl_label = "Math"
    math_006.operation = "SINE"
    math_006.use_clamp = False
    # Value
    math_006.inputs[1].default_value = 0.5
    # Value
    math_006.inputs[2].default_value = 0.5
    # Links for math_006
    links.new(group_input.outputs[2], math_006.inputs[0])

    math_007 = nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.label = ""
    math_007.location = (-372.5569152832031, -56.62147903442383)
    math_007.bl_label = "Math"
    math_007.operation = "MULTIPLY"
    math_007.use_clamp = False
    # Value
    math_007.inputs[2].default_value = 0.5
    # Links for math_007
    links.new(math_006.outputs[0], math_007.inputs[0])
    links.new(math_004.outputs[0], math_007.inputs[1])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (-198.8205108642578, -47.08412551879883)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "SCALE"
    # Vector
    vector_math_003.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_003
    links.new(math_007.outputs[0], vector_math_003.inputs[3])
    links.new(vector_math_003.outputs[0], vector_math_002.inputs[1])
    links.new(group_input.outputs[4], vector_math_003.inputs[0])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (231.5659942626953, 44.80907440185547)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "ADD"
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(vector_math_002.outputs[0], vector_math_004.inputs[0])

    math_008 = nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.label = ""
    math_008.location = (-574.3892211914062, -377.2076721191406)
    math_008.bl_label = "Math"
    math_008.operation = "COSINE"
    math_008.use_clamp = False
    # Value
    math_008.inputs[1].default_value = 0.5
    # Value
    math_008.inputs[2].default_value = 0.5
    # Links for math_008
    links.new(group_input.outputs[1], math_008.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (-321.3338317871094, -336.8251953125)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "SCALE"
    # Vector
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_005
    links.new(math_008.outputs[0], vector_math_005.inputs[3])
    links.new(vector_math_005.outputs[0], vector_math_004.inputs[1])
    links.new(group_input.outputs[0], vector_math_005.inputs[0])

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (459.74359130859375, 73.97240447998047)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "SCALE"
    # Vector
    vector_math_006.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_006
    links.new(vector_math_004.outputs[0], vector_math_006.inputs[0])
    links.new(group_input.outputs[5], vector_math_006.inputs[3])
    links.new(vector_math_006.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_tri_line_group():
    group_name = "TriLine"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Offset", in_out="INPUT", socket_type="NodeSocketVector"
    )
    socket.default_value = [0.0, 0.0, 1.0]
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Offset", in_out="INPUT", socket_type="NodeSocketVector"
    )
    socket.default_value = [0.0, 0.0, 1.0]
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Offset", in_out="INPUT", socket_type="NodeSocketVector"
    )
    socket.default_value = [0.0, 0.0, 1.0]
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (337.2384033203125, 0.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-347.23828125, 0.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    mesh_line = nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.label = ""
    mesh_line.location = (-85.5181884765625, -15.899749755859375)
    mesh_line.bl_label = "Mesh Line"
    mesh_line.mode = "OFFSET"
    mesh_line.count_mode = "TOTAL"
    # Count
    mesh_line.inputs[0].default_value = 10
    # Resolution
    mesh_line.inputs[1].default_value = 1.0
    # Start Location
    mesh_line.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Links for mesh_line
    links.new(group_input.outputs[0], mesh_line.inputs[3])

    mesh_line_001 = nodes.new("GeometryNodeMeshLine")
    mesh_line_001.name = "Mesh Line.001"
    mesh_line_001.label = ""
    mesh_line_001.location = (-89.0450439453125, -250.8613739013672)
    mesh_line_001.bl_label = "Mesh Line"
    mesh_line_001.mode = "OFFSET"
    mesh_line_001.count_mode = "TOTAL"
    # Count
    mesh_line_001.inputs[0].default_value = 10
    # Resolution
    mesh_line_001.inputs[1].default_value = 1.0
    # Start Location
    mesh_line_001.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Links for mesh_line_001
    links.new(group_input.outputs[1], mesh_line_001.inputs[3])

    mesh_line_002 = nodes.new("GeometryNodeMeshLine")
    mesh_line_002.name = "Mesh Line.002"
    mesh_line_002.label = ""
    mesh_line_002.location = (-147.23828125, 250.86135864257812)
    mesh_line_002.bl_label = "Mesh Line"
    mesh_line_002.mode = "OFFSET"
    mesh_line_002.count_mode = "TOTAL"
    # Count
    mesh_line_002.inputs[0].default_value = 10
    # Resolution
    mesh_line_002.inputs[1].default_value = 1.0
    # Start Location
    mesh_line_002.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Links for mesh_line_002
    links.new(group_input.outputs[2], mesh_line_002.inputs[3])

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (147.2384033203125, -14.810882568359375)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry
    links.new(mesh_line.outputs[0], join_geometry.inputs[0])
    links.new(mesh_line_001.outputs[0], join_geometry.inputs[0])
    links.new(mesh_line_002.outputs[0], join_geometry.inputs[0])
    links.new(join_geometry.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_node_group_group():
    group_name = "NodeGroup"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Result", in_out="OUTPUT", socket_type="NodeSocketFloat"
    )
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Factor", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    socket.default_value = 0.5
    socket.min_value = 0.0
    socket.max_value = 1.0
    socket = group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Value", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    socket.default_value = 0.0
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Index", in_out="INPUT", socket_type="NodeSocketInt"
    )
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Value", in_out="INPUT", socket_type="NodeSocketFloat"
    )
    socket.default_value = 0.0
    socket.min_value = -3.4028234663852886e38
    socket.max_value = 3.4028234663852886e38
    socket = group.interface.new_socket(
        name="Index", in_out="INPUT", socket_type="NodeSocketInt"
    )
    socket.default_value = 0
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (265.5225830078125, 6.492884159088135)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-588.9310913085938, 4.869663238525391)
    group_input.bl_label = "Group Input"
    # Links for group_input

    mix_003 = nodes.new("ShaderNodeMix")
    mix_003.name = "Mix.003"
    mix_003.label = ""
    mix_003.location = (75.52255249023438, 30.14333724975586)
    mix_003.bl_label = "Mix"
    mix_003.data_type = "FLOAT"
    mix_003.factor_mode = "UNIFORM"
    mix_003.blend_type = "MIX"
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    # Factor
    mix_003.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_003.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_003.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_003.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_003.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_003.inputs[8].default_value = Euler((0.0, 0.0, 0.0), "XYZ")
    # B
    mix_003.inputs[9].default_value = Euler((0.0, 0.0, 0.0), "XYZ")
    # Links for mix_003
    links.new(group_input.outputs[0], mix_003.inputs[0])
    links.new(mix_003.outputs[0], group_output.inputs[0])

    sample_index_005 = nodes.new("GeometryNodeSampleIndex")
    sample_index_005.name = "Sample Index.005"
    sample_index_005.label = ""
    sample_index_005.location = (50.895599365234375, 237.23135375976562)
    sample_index_005.bl_label = "Sample Index"
    sample_index_005.data_type = "FLOAT"
    sample_index_005.domain = "POINT"
    sample_index_005.clamp = False
    # Links for sample_index_005
    links.new(group_input.outputs[1], sample_index_005.inputs[0])
    links.new(group_input.outputs[2], sample_index_005.inputs[1])
    links.new(sample_index_005.outputs[0], mix_003.inputs[2])

    sample_index_006 = nodes.new("GeometryNodeSampleIndex")
    sample_index_006.name = "Sample Index.006"
    sample_index_006.label = ""
    sample_index_006.location = (-249.58685302734375, -83.22563934326172)
    sample_index_006.bl_label = "Sample Index"
    sample_index_006.data_type = "FLOAT"
    sample_index_006.domain = "POINT"
    sample_index_006.clamp = False
    # Links for sample_index_006
    links.new(group_input.outputs[6], sample_index_006.inputs[2])
    links.new(group_input.outputs[4], sample_index_006.inputs[0])
    links.new(group_input.outputs[5], sample_index_006.inputs[1])
    links.new(sample_index_006.outputs[0], mix_003.inputs[3])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-336.81927490234375, 20.383298873901367)
    math.bl_label = "Math"
    math.operation = "ADD"
    math.use_clamp = False
    # Value
    math.inputs[1].default_value = 40.10000228881836
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(group_input.outputs[3], math.inputs[0])

    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.label = ""
    math_001.location = (-139.95248413085938, 123.16204833984375)
    math_001.bl_label = "Math"
    math_001.operation = "FLOORED_MODULO"
    math_001.use_clamp = False
    # Value
    math_001.inputs[2].default_value = 0.5
    # Links for math_001
    links.new(math.outputs[0], math_001.inputs[0])
    links.new(math_001.outputs[0], sample_index_005.inputs[2])

    mix_offset_index = nodes.new("GeometryNodeAttributeDomainSize")
    mix_offset_index.name = "MixOffsetIndex"
    mix_offset_index.label = ""
    mix_offset_index.location = (-359.97015380859375, 160.91741943359375)
    mix_offset_index.bl_label = "Domain Size"
    mix_offset_index.component = "POINTCLOUD"
    # Links for mix_offset_index
    links.new(mix_offset_index.outputs[0], math_001.inputs[1])
    links.new(group_input.outputs[1], mix_offset_index.inputs[0])

    auto_layout_nodes(group)
    return group


@geo_node_group
def create_male_torso__loft_0__group_group():
    group_name = "MaleTorso_Loft_0_Group"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Curve X (Front)", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Curve Y (Side)", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    socket = group.interface.new_socket(
        name="Resolution V", in_out="INPUT", socket_type="NodeSocketInt"
    )
    socket.default_value = 64
    socket.min_value = -2147483648
    socket.max_value = 2147483647
    socket = group.interface.new_socket(
        name="Resolution U", in_out="INPUT", socket_type="NodeSocketInt"
    )
    socket.default_value = 32
    socket.min_value = -2147483648
    socket.max_value = 2147483647

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-2933.60400390625, -284.1351013183594)
    group_input.bl_label = "Group Input"
    # Links for group_input

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1317.19140625, 806.7011108398438)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (-2479.11328125, 203.23561096191406)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "CURVE"
    # Links for separate_geometry
    links.new(group_input.outputs[0], separate_geometry.inputs[0])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (-2429.645263671875, -82.02975463867188)
    math_005.bl_label = "Math"
    math_005.operation = "GREATER_THAN"
    math_005.use_clamp = False
    # Value
    math_005.inputs[1].default_value = 5.960464477539063e-08
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(math_005.outputs[0], separate_geometry.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (-2643.1640625, 45.95417022705078)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], math_005.inputs[0])

    duplicate_elements = nodes.new("GeometryNodeDuplicateElements")
    duplicate_elements.name = "Duplicate Elements"
    duplicate_elements.label = ""
    duplicate_elements.location = (-2018.183837890625, 486.8221740722656)
    duplicate_elements.bl_label = "Duplicate Elements"
    duplicate_elements.domain = "SPLINE"
    # Selection
    duplicate_elements.inputs[1].default_value = True
    # Amount
    duplicate_elements.inputs[2].default_value = 1
    # Links for duplicate_elements
    links.new(separate_geometry.outputs[1], duplicate_elements.inputs[0])

    rotate_cyclic_curve = nodes.new("GeometryNodeGroup")
    rotate_cyclic_curve.name = "Group"
    rotate_cyclic_curve.label = ""
    rotate_cyclic_curve.location = (-958.9896240234375, 1129.1314697265625)
    rotate_cyclic_curve.node_tree = create_rotate_cyclic_curve_group()
    rotate_cyclic_curve.bl_label = "Group"
    # Axis
    rotate_cyclic_curve.inputs[2].default_value = [0.0, 1.0, 0.0]
    # Center
    rotate_cyclic_curve.inputs[3].default_value = [0.0, 0.0, 0.0]
    # Angle
    rotate_cyclic_curve.inputs[4].default_value = 0.0
    # Links for rotate_cyclic_curve
    links.new(duplicate_elements.outputs[0], rotate_cyclic_curve.inputs[0])
    links.new(group_input.outputs[2], rotate_cyclic_curve.inputs[1])

    curve_to_points_002 = nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_002.name = "Curve to Points.002"
    curve_to_points_002.label = ""
    curve_to_points_002.location = (-476.92755126953125, 1113.7088623046875)
    curve_to_points_002.bl_label = "Curve to Points"
    curve_to_points_002.mode = "COUNT"
    # Length
    curve_to_points_002.inputs[2].default_value = 0.10000000149011612
    # Links for curve_to_points_002
    links.new(rotate_cyclic_curve.outputs[0], curve_to_points_002.inputs[0])

    mix_001 = nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.label = ""
    mix_001.location = (586.9482421875, 926.5385131835938)
    mix_001.bl_label = "Mix"
    mix_001.data_type = "FLOAT"
    mix_001.factor_mode = "UNIFORM"
    mix_001.blend_type = "MIX"
    mix_001.clamp_factor = False
    mix_001.clamp_result = False
    # Factor
    mix_001.inputs[0].default_value = 0.0
    # Factor
    mix_001.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_001.inputs[4].default_value = [0.0, 0.0, 0.0]
    # B
    mix_001.inputs[5].default_value = [0.0, 0.0, 0.0]
    # A
    mix_001.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_001.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_001.inputs[8].default_value = Euler((0.0, 0.0, 0.0), "XYZ")
    # B
    mix_001.inputs[9].default_value = Euler((0.0, 0.0, 0.0), "XYZ")
    # Links for mix_001

    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.label = ""
    index_001.location = (-897.94140625, 620.3433837890625)
    index_001.bl_label = "Index"
    # Links for index_001

    sample_curve_distances = nodes.new("GeometryNodeGroup")
    sample_curve_distances.name = "Group.004"
    sample_curve_distances.label = ""
    sample_curve_distances.location = (-726.5615234375, 502.611572265625)
    sample_curve_distances.node_tree = create_sample_curve_distances_group()
    sample_curve_distances.bl_label = "Group"
    # Links for sample_curve_distances
    links.new(index_001.outputs[0], sample_curve_distances.inputs[1])
    links.new(separate_geometry.outputs[1], sample_curve_distances.inputs[0])

    sample_curve_distances_1 = nodes.new("GeometryNodeGroup")
    sample_curve_distances_1.name = "Group.005"
    sample_curve_distances_1.label = ""
    sample_curve_distances_1.location = (-585.4951171875, 729.9744873046875)
    sample_curve_distances_1.node_tree = create_sample_curve_distances_group()
    sample_curve_distances_1.bl_label = "Group"
    # Links for sample_curve_distances_1
    links.new(separate_geometry.outputs[0], sample_curve_distances_1.inputs[0])
    links.new(index_001.outputs[0], sample_curve_distances_1.inputs[1])

    get_center_curve = nodes.new("GeometryNodeGroup")
    get_center_curve.name = "Group.001"
    get_center_curve.label = ""
    get_center_curve.location = (-1588.4923095703125, 786.5953979492188)
    get_center_curve.node_tree = create_get_center_curve_group()
    get_center_curve.bl_label = "Group"
    # Links for get_center_curve
    links.new(duplicate_elements.outputs[0], get_center_curve.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (623.0247192382812, 699.7493286132812)
    position_002.bl_label = "Position"
    # Links for position_002

    get_index_offset = nodes.new("GeometryNodeGroup")
    get_index_offset.name = "Group.007"
    get_index_offset.label = ""
    get_index_offset.location = (-348.3952941894531, 165.63031005859375)
    get_index_offset.node_tree = create_get_index_offset_group()
    get_index_offset.bl_label = "Group"
    # Links for get_index_offset
    links.new(sample_curve_distances.outputs[1], get_index_offset.inputs[1])
    links.new(sample_curve_distances_1.outputs[1], get_index_offset.inputs[0])
    links.new(index_001.outputs[0], get_index_offset.inputs[2])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (323.2083740234375, 806.2218627929688)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001
    links.new(get_index_offset.outputs[0], sample_index_001.inputs[0])
    links.new(sample_index_001.outputs[0], mix_001.inputs[2])
    links.new(get_index_offset.outputs[2], sample_index_001.inputs[2])

    sample_index_003 = nodes.new("GeometryNodeSampleIndex")
    sample_index_003.name = "Sample Index.003"
    sample_index_003.label = ""
    sample_index_003.location = (6.234428405761719, 582.8724365234375)
    sample_index_003.bl_label = "Sample Index"
    sample_index_003.data_type = "FLOAT"
    sample_index_003.domain = "POINT"
    sample_index_003.clamp = False
    # Links for sample_index_003
    links.new(sample_curve_distances.outputs[2], sample_index_003.inputs[1])
    links.new(get_index_offset.outputs[3], sample_index_003.inputs[0])
    links.new(get_index_offset.outputs[5], sample_index_003.inputs[2])

    integer = nodes.new("FunctionNodeInputInt")
    integer.name = "Integer"
    integer.label = ""
    integer.location = (-1035.6302490234375, 755.3663330078125)
    integer.bl_label = "Integer"
    integer.integer = 200
    # Links for integer
    links.new(integer.outputs[0], sample_curve_distances_1.inputs[2])
    links.new(integer.outputs[0], sample_curve_distances.inputs[2])
    links.new(integer.outputs[0], curve_to_points_002.inputs[1])

    morph_curve_to_curve = nodes.new("GeometryNodeGroup")
    morph_curve_to_curve.name = "Group.002"
    morph_curve_to_curve.label = ""
    morph_curve_to_curve.location = (752.0720825195312, 1127.622314453125)
    morph_curve_to_curve.node_tree = create_morph_curve_to_curve_group()
    morph_curve_to_curve.bl_label = "Group"
    # Normal
    morph_curve_to_curve.inputs[3].default_value = [0.0, 0.0, 0.0]
    # Links for morph_curve_to_curve
    links.new(mix_001.outputs[0], morph_curve_to_curve.inputs[1])
    links.new(get_index_offset.outputs[2], morph_curve_to_curve.inputs[2])
    links.new(get_index_offset.outputs[0], morph_curve_to_curve.inputs[0])

    sample_index_004 = nodes.new("GeometryNodeSampleIndex")
    sample_index_004.name = "Sample Index.004"
    sample_index_004.label = ""
    sample_index_004.location = (486.5193176269531, 544.322509765625)
    sample_index_004.bl_label = "Sample Index"
    sample_index_004.data_type = "FLOAT"
    sample_index_004.domain = "POINT"
    sample_index_004.clamp = False
    # Links for sample_index_004
    links.new(get_index_offset.outputs[5], sample_index_004.inputs[2])
    links.new(get_index_offset.outputs[3], sample_index_004.inputs[0])
    links.new(sample_index_004.outputs[0], mix_001.inputs[3])

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (9.348089218139648, 361.38043212890625)
    position_001.bl_label = "Position"
    # Links for position_001

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (206.1245880126953, 412.07244873046875)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "LENGTH"
    # Vector
    vector_math.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math.inputs[3].default_value = 1.0
    # Links for vector_math
    links.new(vector_math.outputs[1], sample_index_004.inputs[1])
    links.new(position_001.outputs[0], vector_math.inputs[0])
    links.new(vector_math.outputs[1], sample_index_001.inputs[1])

    vector_angles = nodes.new("GeometryNodeGroup")
    vector_angles.name = "Group.008"
    vector_angles.label = ""
    vector_angles.location = (28.650938034057617, -114.20536804199219)
    vector_angles.node_tree = create_vector_angles_group()
    vector_angles.bl_label = "Group"
    # Links for vector_angles
    links.new(get_index_offset.outputs[5], vector_angles.inputs[1])
    links.new(get_index_offset.outputs[3], vector_angles.inputs[0])

    viewer_001 = nodes.new("GeometryNodeViewer")
    viewer_001.name = "Viewer.001"
    viewer_001.label = ""
    viewer_001.location = (1074.338134765625, 1035.04345703125)
    viewer_001.bl_label = "Viewer"
    viewer_001.ui_shortcut = 0
    viewer_001.active_index = 0
    viewer_001.domain = "AUTO"
    # Links for viewer_001
    links.new(morph_curve_to_curve.outputs[0], viewer_001.inputs[0])

    construct_vector = nodes.new("GeometryNodeGroup")
    construct_vector.name = "Group.006"
    construct_vector.label = ""
    construct_vector.location = (854.6863403320312, 128.50543212890625)
    construct_vector.node_tree = create_construct_vector_group()
    construct_vector.bl_label = "Group"
    # Links for construct_vector
    links.new(vector_angles.outputs[0], construct_vector.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (972.3775634765625, 739.5772705078125)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position
    links.new(construct_vector.outputs[0], set_position.inputs[2])
    links.new(sample_curve_distances_1.outputs[1], set_position.inputs[0])
    links.new(set_position.outputs[0], group_output.inputs[0])

    viewer = nodes.new("GeometryNodeViewer")
    viewer.name = "Viewer"
    viewer.label = ""
    viewer.location = (1298.373046875, 575.7996215820312)
    viewer.bl_label = "Viewer"
    viewer.ui_shortcut = 0
    viewer.active_index = 0
    viewer.domain = "AUTO"
    # Links for viewer
    links.new(set_position.outputs[0], viewer.inputs[0])

    viewer_002 = nodes.new("GeometryNodeViewer")
    viewer_002.name = "Viewer.002"
    viewer_002.label = ""
    viewer_002.location = (1614.1627197265625, 283.785400390625)
    viewer_002.bl_label = "Viewer"
    viewer_002.ui_shortcut = 0
    viewer_002.active_index = 0
    viewer_002.domain = "AUTO"
    # Links for viewer_002

    vector_angles_1 = nodes.new("GeometryNodeGroup")
    vector_angles_1.name = "VectorAngles"
    vector_angles_1.label = ""
    vector_angles_1.location = (98.1412353515625, 239.17434692382812)
    vector_angles_1.node_tree = create_vector_angles_group()
    vector_angles_1.bl_label = "Group"
    # Links for vector_angles_1
    links.new(get_index_offset.outputs[2], vector_angles_1.inputs[1])
    links.new(get_index_offset.outputs[0], vector_angles_1.inputs[0])

    value = nodes.new("ShaderNodeValue")
    value.name = "Value"
    value.label = ""
    value.location = (-266.37615966796875, -303.3360290527344)
    value.bl_label = "Value"
    # Links for value

    mix_004 = nodes.new("ShaderNodeMix")
    mix_004.name = "Mix.004"
    mix_004.label = ""
    mix_004.location = (253.12193298339844, -491.7706298828125)
    mix_004.bl_label = "Mix"
    mix_004.data_type = "VECTOR"
    mix_004.factor_mode = "UNIFORM"
    mix_004.blend_type = "MIX"
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    # Factor
    mix_004.inputs[1].default_value = [0.5, 0.5, 0.5]
    # A
    mix_004.inputs[2].default_value = 0.0
    # B
    mix_004.inputs[3].default_value = 0.0
    # A
    mix_004.inputs[6].default_value = [0.5, 0.5, 0.5, 1.0]
    # B
    mix_004.inputs[7].default_value = [0.5, 0.5, 0.5, 1.0]
    # A
    mix_004.inputs[8].default_value = Euler((0.0, 0.0, 0.0), "XYZ")
    # B
    mix_004.inputs[9].default_value = Euler((0.0, 0.0, 0.0), "XYZ")
    # Links for mix_004
    links.new(vector_angles.outputs[0], mix_004.inputs[4])
    links.new(vector_angles_1.outputs[0], mix_004.inputs[5])
    links.new(value.outputs[0], mix_004.inputs[0])

    perpendicular_vectors = nodes.new("GeometryNodeGroup")
    perpendicular_vectors.name = "PerpendicularVectors"
    perpendicular_vectors.label = ""
    perpendicular_vectors.location = (534.8549194335938, -511.94525146484375)
    perpendicular_vectors.node_tree = create_perpendicular_vectors_group()
    perpendicular_vectors.bl_label = "Group"
    # Links for perpendicular_vectors
    links.new(get_index_offset.outputs[0], perpendicular_vectors.inputs[1])
    links.new(perpendicular_vectors.outputs[1], construct_vector.inputs[3])
    links.new(perpendicular_vectors.outputs[2], construct_vector.inputs[4])
    links.new(vector_angles.outputs[0], perpendicular_vectors.inputs[0])

    tri_line = nodes.new("GeometryNodeGroup")
    tri_line.name = "Group.003"
    tri_line.label = ""
    tri_line.location = (1154.7657470703125, 210.84188842773438)
    tri_line.node_tree = create_tri_line_group()
    tri_line.bl_label = "Group"
    # Links for tri_line
    links.new(vector_angles.outputs[4], tri_line.inputs[1])
    links.new(vector_angles.outputs[3], tri_line.inputs[0])
    links.new(vector_angles.outputs[0], tri_line.inputs[2])

    tri_line_1 = nodes.new("GeometryNodeGroup")
    tri_line_1.name = "Group.009"
    tri_line_1.label = ""
    tri_line_1.location = (1140.1817626953125, 29.05059814453125)
    tri_line_1.node_tree = create_tri_line_group()
    tri_line_1.bl_label = "Group"
    # Links for tri_line_1
    links.new(perpendicular_vectors.outputs[2], tri_line_1.inputs[2])
    links.new(perpendicular_vectors.outputs[1], tri_line_1.inputs[1])
    links.new(tri_line_1.outputs[0], viewer_002.inputs[0])
    links.new(vector_angles.outputs[0], tri_line_1.inputs[0])

    node_group = nodes.new("GeometryNodeGroup")
    node_group.name = "Group.010"
    node_group.label = ""
    node_group.location = (495.1964416503906, 302.04534912109375)
    node_group.node_tree = create_node_group_group()
    node_group.bl_label = "Group"
    # Links for node_group
    links.new(node_group.outputs[0], construct_vector.inputs[1])
    links.new(value.outputs[0], node_group.inputs[0])
    links.new(get_index_offset.outputs[3], node_group.inputs[4])
    links.new(get_index_offset.outputs[0], node_group.inputs[1])
    links.new(vector_angles.outputs[1], node_group.inputs[5])
    links.new(vector_angles_1.outputs[1], node_group.inputs[2])
    links.new(get_index_offset.outputs[5], node_group.inputs[6])
    links.new(get_index_offset.outputs[2], node_group.inputs[3])

    node_group_1 = nodes.new("GeometryNodeGroup")
    node_group_1.name = "Group.011"
    node_group_1.label = ""
    node_group_1.location = (478.33740234375, 54.81170654296875)
    node_group_1.node_tree = create_node_group_group()
    node_group_1.bl_label = "Group"
    # Links for node_group_1
    links.new(value.outputs[0], node_group_1.inputs[0])
    links.new(vector_angles_1.outputs[2], node_group_1.inputs[2])
    links.new(get_index_offset.outputs[0], node_group_1.inputs[1])
    links.new(get_index_offset.outputs[2], node_group_1.inputs[3])
    links.new(get_index_offset.outputs[3], node_group_1.inputs[4])
    links.new(get_index_offset.outputs[5], node_group_1.inputs[6])
    links.new(vector_angles.outputs[2], node_group_1.inputs[5])
    links.new(node_group_1.outputs[0], construct_vector.inputs[2])

    node_group_2 = nodes.new("GeometryNodeGroup")
    node_group_2.name = "Group.012"
    node_group_2.label = ""
    node_group_2.location = (468.9720764160156, -242.9362030029297)
    node_group_2.node_tree = create_node_group_group()
    node_group_2.bl_label = "Group"
    # Links for node_group_2
    links.new(value.outputs[0], node_group_2.inputs[0])
    links.new(node_group_2.outputs[0], construct_vector.inputs[5])
    links.new(get_index_offset.outputs[0], node_group_2.inputs[1])
    links.new(get_index_offset.outputs[2], node_group_2.inputs[3])
    links.new(vector_angles_1.outputs[5], node_group_2.inputs[2])
    links.new(get_index_offset.outputs[3], node_group_2.inputs[4])
    links.new(get_index_offset.outputs[5], node_group_2.inputs[6])
    links.new(vector_angles.outputs[5], node_group_2.inputs[5])

    auto_layout_nodes(group)
    return group
