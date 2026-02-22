import bpy
import mathutils
import os
import typing


def is_edge_boundary_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Is Edge Boundary node group"""
    is_edge_boundary_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Is Edge Boundary")

    is_edge_boundary_1.color_tag = 'INPUT'
    is_edge_boundary_1.description = ""
    is_edge_boundary_1.default_group_node_width = 140
    is_edge_boundary_1.show_modifier_manage_panel = True

    # is_edge_boundary_1 interface

    # Socket Is Edge Boundary
    is_edge_boundary_socket = is_edge_boundary_1.interface.new_socket(name="Is Edge Boundary", in_out='OUTPUT', socket_type='NodeSocketBool')
    is_edge_boundary_socket.default_value = False
    is_edge_boundary_socket.attribute_domain = 'POINT'
    is_edge_boundary_socket.description = "Selection of edges that are part of the boundary of a mesh surface"
    is_edge_boundary_socket.default_input = 'VALUE'
    is_edge_boundary_socket.structure_type = 'AUTO'

    # Initialize is_edge_boundary_1 nodes

    # Node Group Output
    group_output = is_edge_boundary_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Edge Neighbors
    edge_neighbors = is_edge_boundary_1.nodes.new("GeometryNodeInputMeshEdgeNeighbors")
    edge_neighbors.name = "Edge Neighbors"

    # Node Compare
    compare = is_edge_boundary_1.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'INT'
    compare.mode = 'ELEMENT'
    compare.operation = 'EQUAL'
    # B_INT
    compare.inputs[3].default_value = 1

    # Node Evaluate on Domain
    evaluate_on_domain = is_edge_boundary_1.nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.name = "Evaluate on Domain"
    evaluate_on_domain.data_type = 'BOOLEAN'
    evaluate_on_domain.domain = 'EDGE'

    # Set locations
    is_edge_boundary_1.nodes["Group Output"].location = (320.0, 0.0)
    is_edge_boundary_1.nodes["Edge Neighbors"].location = (-279.9999694824219, 0.0)
    is_edge_boundary_1.nodes["Compare"].location = (-80.0, 0.0)
    is_edge_boundary_1.nodes["Evaluate on Domain"].location = (119.99999237060547, 0.0)

    # Set dimensions
    is_edge_boundary_1.nodes["Group Output"].width  = 140.0
    is_edge_boundary_1.nodes["Group Output"].height = 100.0

    is_edge_boundary_1.nodes["Edge Neighbors"].width  = 140.0
    is_edge_boundary_1.nodes["Edge Neighbors"].height = 100.0

    is_edge_boundary_1.nodes["Compare"].width  = 140.0
    is_edge_boundary_1.nodes["Compare"].height = 100.0

    is_edge_boundary_1.nodes["Evaluate on Domain"].width  = 140.0
    is_edge_boundary_1.nodes["Evaluate on Domain"].height = 100.0


    # Initialize is_edge_boundary_1 links

    # edge_neighbors.Face Count -> compare.A
    is_edge_boundary_1.links.new(
        is_edge_boundary_1.nodes["Edge Neighbors"].outputs[0],
        is_edge_boundary_1.nodes["Compare"].inputs[2]
    )
    # evaluate_on_domain.Value -> group_output.Is Edge Boundary
    is_edge_boundary_1.links.new(
        is_edge_boundary_1.nodes["Evaluate on Domain"].outputs[0],
        is_edge_boundary_1.nodes["Group Output"].inputs[0]
    )
    # compare.Result -> evaluate_on_domain.Value
    is_edge_boundary_1.links.new(
        is_edge_boundary_1.nodes["Compare"].outputs[0],
        is_edge_boundary_1.nodes["Evaluate on Domain"].inputs[0]
    )

    return is_edge_boundary_1


def space___res_switch_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Space / Res Switch node group"""
    space___res_switch_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Space / Res Switch")

    space___res_switch_1.color_tag = 'CONVERTER'
    space___res_switch_1.description = ""
    space___res_switch_1.default_group_node_width = 140
    space___res_switch_1.show_modifier_manage_panel = True

    # space___res_switch_1 interface

    # Socket Output
    output_socket = space___res_switch_1.interface.new_socket(name="Output", in_out='OUTPUT', socket_type='NodeSocketInt')
    output_socket.default_value = 0
    output_socket.min_value = -2147483648
    output_socket.max_value = 2147483647
    output_socket.subtype = 'NONE'
    output_socket.attribute_domain = 'POINT'
    output_socket.default_input = 'VALUE'
    output_socket.structure_type = 'AUTO'

    # Socket Menu
    menu_socket = space___res_switch_1.interface.new_socket(name="Menu", in_out='INPUT', socket_type='NodeSocketMenu')
    menu_socket.attribute_domain = 'POINT'
    menu_socket.default_input = 'VALUE'
    menu_socket.structure_type = 'AUTO'
    menu_socket.optional_label = True

    # Socket Spacing
    spacing_socket = space___res_switch_1.interface.new_socket(name="Spacing", in_out='INPUT', socket_type='NodeSocketInt')
    spacing_socket.default_value = 0
    spacing_socket.min_value = -2147483648
    spacing_socket.max_value = 2147483647
    spacing_socket.subtype = 'NONE'
    spacing_socket.attribute_domain = 'POINT'
    spacing_socket.description = "Becomes the output value if it is chosen by the menu input"
    spacing_socket.default_input = 'VALUE'
    spacing_socket.structure_type = 'AUTO'

    # Socket Resolution
    resolution_socket = space___res_switch_1.interface.new_socket(name="Resolution", in_out='INPUT', socket_type='NodeSocketInt')
    resolution_socket.default_value = 0
    resolution_socket.min_value = -2147483648
    resolution_socket.max_value = 2147483647
    resolution_socket.subtype = 'NONE'
    resolution_socket.attribute_domain = 'POINT'
    resolution_socket.description = "Becomes the output value if it is chosen by the menu input"
    resolution_socket.default_input = 'VALUE'
    resolution_socket.structure_type = 'AUTO'

    # Initialize space___res_switch_1 nodes

    # Node Group Input
    group_input = space___res_switch_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Group Output
    group_output = space___res_switch_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Menu Switch.001
    menu_switch_001 = space___res_switch_1.nodes.new("GeometryNodeMenuSwitch")
    menu_switch_001.name = "Menu Switch.001"
    menu_switch_001.active_index = 1
    menu_switch_001.data_type = 'INT'
    menu_switch_001.enum_items.clear()
    menu_switch_001.enum_items.new("Spacing")
    menu_switch_001.enum_items[0].description = ""
    menu_switch_001.enum_items.new("Resolution")
    menu_switch_001.enum_items[1].description = ""

    # Set locations
    space___res_switch_1.nodes["Group Input"].location = (-440.0, 0.0)
    space___res_switch_1.nodes["Group Output"].location = (-80.0, 40.0)
    space___res_switch_1.nodes["Menu Switch.001"].location = (-260.0, 40.0)

    # Set dimensions
    space___res_switch_1.nodes["Group Input"].width  = 140.0
    space___res_switch_1.nodes["Group Input"].height = 100.0

    space___res_switch_1.nodes["Group Output"].width  = 140.0
    space___res_switch_1.nodes["Group Output"].height = 100.0

    space___res_switch_1.nodes["Menu Switch.001"].width  = 140.0
    space___res_switch_1.nodes["Menu Switch.001"].height = 100.0


    # Initialize space___res_switch_1 links

    # group_input.Menu -> menu_switch_001.Menu
    space___res_switch_1.links.new(
        space___res_switch_1.nodes["Group Input"].outputs[0],
        space___res_switch_1.nodes["Menu Switch.001"].inputs[0]
    )
    # group_input.Spacing -> menu_switch_001.Spacing
    space___res_switch_1.links.new(
        space___res_switch_1.nodes["Group Input"].outputs[1],
        space___res_switch_1.nodes["Menu Switch.001"].inputs[1]
    )
    # group_input.Resolution -> menu_switch_001.Resolution
    space___res_switch_1.links.new(
        space___res_switch_1.nodes["Group Input"].outputs[2],
        space___res_switch_1.nodes["Menu Switch.001"].inputs[2]
    )
    # menu_switch_001.Output -> group_output.Output
    space___res_switch_1.links.new(
        space___res_switch_1.nodes["Menu Switch.001"].outputs[0],
        space___res_switch_1.nodes["Group Output"].inputs[0]
    )
    menu_socket.default_value = 'Spacing'

    return space___res_switch_1


def bi_rail_loft_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Bi-Rail Loft node group"""
    bi_rail_loft_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Bi-Rail Loft")

    bi_rail_loft_1.color_tag = 'GEOMETRY'
    bi_rail_loft_1.description = ""
    bi_rail_loft_1.default_group_node_width = 140
    bi_rail_loft_1.show_modifier_manage_panel = True

    # bi_rail_loft_1 interface

    # Socket Mesh
    mesh_socket = bi_rail_loft_1.interface.new_socket(name="Mesh", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    mesh_socket.attribute_domain = 'POINT'
    mesh_socket.default_input = 'VALUE'
    mesh_socket.structure_type = 'AUTO'

    # Socket Interpolated Profiles
    interpolated_profiles_socket = bi_rail_loft_1.interface.new_socket(name="Interpolated Profiles", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    interpolated_profiles_socket.attribute_domain = 'POINT'
    interpolated_profiles_socket.default_input = 'VALUE'
    interpolated_profiles_socket.structure_type = 'AUTO'

    # Socket UVMap
    uvmap_socket = bi_rail_loft_1.interface.new_socket(name="UVMap", in_out='OUTPUT', socket_type='NodeSocketVector')
    uvmap_socket.default_value = (0.0, 0.0, 0.0)
    uvmap_socket.min_value = -3.4028234663852886e+38
    uvmap_socket.max_value = 3.4028234663852886e+38
    uvmap_socket.subtype = 'NONE'
    uvmap_socket.attribute_domain = 'POINT'
    uvmap_socket.default_input = 'VALUE'
    uvmap_socket.structure_type = 'AUTO'

    # Socket Rail Curve
    rail_curve_socket = bi_rail_loft_1.interface.new_socket(name="Rail Curve", in_out='INPUT', socket_type='NodeSocketGeometry')
    rail_curve_socket.attribute_domain = 'POINT'
    rail_curve_socket.default_input = 'VALUE'
    rail_curve_socket.structure_type = 'AUTO'

    # Socket Rail Curve
    rail_curve_socket_1 = bi_rail_loft_1.interface.new_socket(name="Rail Curve", in_out='INPUT', socket_type='NodeSocketGeometry')
    rail_curve_socket_1.attribute_domain = 'POINT'
    rail_curve_socket_1.default_input = 'VALUE'
    rail_curve_socket_1.structure_type = 'AUTO'

    # Socket Profile Curves
    profile_curves_socket = bi_rail_loft_1.interface.new_socket(name="Profile Curves", in_out='INPUT', socket_type='NodeSocketGeometry')
    profile_curves_socket.attribute_domain = 'POINT'
    profile_curves_socket.default_input = 'VALUE'
    profile_curves_socket.structure_type = 'AUTO'

    # Socket Smoothing
    smoothing_socket = bi_rail_loft_1.interface.new_socket(name="Smoothing", in_out='INPUT', socket_type='NodeSocketInt')
    smoothing_socket.default_value = 0
    smoothing_socket.min_value = 0
    smoothing_socket.max_value = 2147483647
    smoothing_socket.subtype = 'NONE'
    smoothing_socket.attribute_domain = 'POINT'
    smoothing_socket.description = "How many times to blur the values for all elements"
    smoothing_socket.default_input = 'VALUE'
    smoothing_socket.structure_type = 'AUTO'

    # Socket Menu
    menu_socket = bi_rail_loft_1.interface.new_socket(name="Menu", in_out='INPUT', socket_type='NodeSocketMenu')
    menu_socket.attribute_domain = 'POINT'
    menu_socket.force_non_field = True
    menu_socket.default_input = 'VALUE'
    menu_socket.menu_expanded = True
    menu_socket.structure_type = 'SINGLE'
    menu_socket.optional_label = True

    # Socket X Spacing
    x_spacing_socket = bi_rail_loft_1.interface.new_socket(name="X Spacing", in_out='INPUT', socket_type='NodeSocketFloat')
    x_spacing_socket.default_value = 0.10000000149011612
    x_spacing_socket.min_value = 0.0
    x_spacing_socket.max_value = 10000.0
    x_spacing_socket.subtype = 'DISTANCE'
    x_spacing_socket.attribute_domain = 'POINT'
    x_spacing_socket.force_non_field = True
    x_spacing_socket.default_input = 'VALUE'
    x_spacing_socket.structure_type = 'SINGLE'

    # Socket Y Spacing
    y_spacing_socket = bi_rail_loft_1.interface.new_socket(name="Y Spacing", in_out='INPUT', socket_type='NodeSocketFloat')
    y_spacing_socket.default_value = 0.10000000149011612
    y_spacing_socket.min_value = 0.0
    y_spacing_socket.max_value = 10000.0
    y_spacing_socket.subtype = 'DISTANCE'
    y_spacing_socket.attribute_domain = 'POINT'
    y_spacing_socket.force_non_field = True
    y_spacing_socket.default_input = 'VALUE'
    y_spacing_socket.structure_type = 'SINGLE'

    # Socket X Resolution
    x_resolution_socket = bi_rail_loft_1.interface.new_socket(name="X Resolution", in_out='INPUT', socket_type='NodeSocketInt')
    x_resolution_socket.default_value = 12
    x_resolution_socket.min_value = 2
    x_resolution_socket.max_value = 2147483647
    x_resolution_socket.subtype = 'NONE'
    x_resolution_socket.attribute_domain = 'POINT'
    x_resolution_socket.force_non_field = True
    x_resolution_socket.description = "Becomes the output value if it is chosen by the menu input"
    x_resolution_socket.default_input = 'VALUE'
    x_resolution_socket.structure_type = 'SINGLE'

    # Socket Y Resolution
    y_resolution_socket = bi_rail_loft_1.interface.new_socket(name="Y Resolution", in_out='INPUT', socket_type='NodeSocketInt')
    y_resolution_socket.default_value = 12
    y_resolution_socket.min_value = 2
    y_resolution_socket.max_value = 2147483647
    y_resolution_socket.subtype = 'NONE'
    y_resolution_socket.attribute_domain = 'POINT'
    y_resolution_socket.force_non_field = True
    y_resolution_socket.description = "Becomes the output value if it is chosen by the menu input"
    y_resolution_socket.default_input = 'VALUE'
    y_resolution_socket.structure_type = 'SINGLE'

    # Socket Profile Blending Curve
    profile_blending_curve_socket = bi_rail_loft_1.interface.new_socket(name="Profile Blending Curve", in_out='INPUT', socket_type='NodeSocketClosure')
    profile_blending_curve_socket.attribute_domain = 'POINT'
    profile_blending_curve_socket.default_input = 'VALUE'
    profile_blending_curve_socket.structure_type = 'AUTO'

    # Initialize bi_rail_loft_1 nodes

    # Node Group Output
    group_output = bi_rail_loft_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = bi_rail_loft_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[0].hide = True
    group_input.outputs[1].hide = True
    group_input.outputs[3].hide = True
    group_input.outputs[4].hide = True
    group_input.outputs[5].hide = True
    group_input.outputs[6].hide = True
    group_input.outputs[7].hide = True
    group_input.outputs[8].hide = True
    group_input.outputs[9].hide = True
    group_input.outputs[10].hide = True

    # Node Realize Instances
    realize_instances = bi_rail_loft_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0

    # Node Resample Curve
    resample_curve = bi_rail_loft_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = 'Count'
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612

    # Node Resample Curve.001
    resample_curve_001 = bi_rail_loft_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = 'Count'
    # Length
    resample_curve_001.inputs[4].default_value = 0.10000000149011612

    # Node Set Position
    set_position = bi_rail_loft_1.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Evaluate at Index
    evaluate_at_index = bi_rail_loft_1.nodes.new("GeometryNodeFieldAtIndex")
    evaluate_at_index.name = "Evaluate at Index"
    evaluate_at_index.data_type = 'FLOAT_VECTOR'
    evaluate_at_index.domain = 'POINT'

    # Node Position
    position = bi_rail_loft_1.nodes.new("GeometryNodeInputPosition")
    position.name = "Position"

    # Node Vector Math
    vector_math = bi_rail_loft_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'MULTIPLY_ADD'
    # Vector_001
    vector_math.inputs[1].default_value = (-1.0, -1.0, -1.0)

    # Node Spline Length
    spline_length = bi_rail_loft_1.nodes.new("GeometryNodeSplineLength")
    spline_length.name = "Spline Length"
    spline_length.outputs[0].hide = True

    # Node Index
    index = bi_rail_loft_1.nodes.new("GeometryNodeInputIndex")
    index.name = "Index"

    # Node Spline Parameter
    spline_parameter = bi_rail_loft_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.outputs[0].hide = True
    spline_parameter.outputs[1].hide = True

    # Node Integer Math
    integer_math = bi_rail_loft_1.nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.operation = 'SUBTRACT'

    # Node Integer Math.001
    integer_math_001 = bi_rail_loft_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_001.name = "Integer Math.001"
    integer_math_001.operation = 'ADD'

    # Node Integer Math.002
    integer_math_002 = bi_rail_loft_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_002.name = "Integer Math.002"
    integer_math_002.operation = 'SUBTRACT'
    # Value_001
    integer_math_002.inputs[1].default_value = 1

    # Node Rotate Vector
    rotate_vector = bi_rail_loft_1.nodes.new("FunctionNodeRotateVector")
    rotate_vector.name = "Rotate Vector"

    # Node Align Rotation to Vector
    align_rotation_to_vector = bi_rail_loft_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.axis = 'X'
    align_rotation_to_vector.pivot_axis = 'AUTO'
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0

    # Node Evaluate at Index.001
    evaluate_at_index_001 = bi_rail_loft_1.nodes.new("GeometryNodeFieldAtIndex")
    evaluate_at_index_001.name = "Evaluate at Index.001"
    evaluate_at_index_001.data_type = 'FLOAT_VECTOR'
    evaluate_at_index_001.domain = 'POINT'

    # Node Vector Math.001
    vector_math_001 = bi_rail_loft_1.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'SUBTRACT'

    # Node Invert Rotation
    invert_rotation = bi_rail_loft_1.nodes.new("FunctionNodeInvertRotation")
    invert_rotation.name = "Invert Rotation"

    # Node Vector Math.002
    vector_math_002 = bi_rail_loft_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'SCALE'

    # Node Vector Math.003
    vector_math_003 = bi_rail_loft_1.nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.operation = 'LENGTH'

    # Node Math
    math = bi_rail_loft_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'DIVIDE'
    math.use_clamp = False
    # Value
    math.inputs[0].default_value = 1.0

    # Node Resample Curve.002
    resample_curve_002 = bi_rail_loft_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.name = "Resample Curve.002"
    resample_curve_002.keep_last_segment = True
    # Selection
    resample_curve_002.inputs[1].default_value = True
    # Mode
    resample_curve_002.inputs[2].default_value = 'Evaluated'
    # Count
    resample_curve_002.inputs[3].default_value = 10
    # Length
    resample_curve_002.inputs[4].default_value = 0.10000000149011612

    # Node Frame.001
    frame_001 = bi_rail_loft_1.nodes.new("NodeFrame")
    frame_001.label = "Fix Transform"
    frame_001.name = "Frame.001"
    frame_001.label_size = 20
    frame_001.shrink = True

    # Node Separate Geometry
    separate_geometry = bi_rail_loft_1.nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.domain = 'CURVE'

    # Node Index.001
    index_001 = bi_rail_loft_1.nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"

    # Node Duplicate Elements
    duplicate_elements = bi_rail_loft_1.nodes.new("GeometryNodeDuplicateElements")
    duplicate_elements.name = "Duplicate Elements"
    duplicate_elements.domain = 'SPLINE'
    # Selection
    duplicate_elements.inputs[1].default_value = True

    # Node Set Position.001
    set_position_001 = bi_rail_loft_1.nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Math.001
    math_001 = bi_rail_loft_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.hide = True
    math_001.operation = 'DIVIDE'
    math_001.use_clamp = False

    # Node Reroute.001
    reroute_001 = bi_rail_loft_1.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.socket_idname = "NodeSocketInt"
    # Node Integer Math.003
    integer_math_003 = bi_rail_loft_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_003.name = "Integer Math.003"
    integer_math_003.hide = True
    integer_math_003.operation = 'SUBTRACT'
    # Value_001
    integer_math_003.inputs[1].default_value = 1

    # Node Frame.002
    frame_002 = bi_rail_loft_1.nodes.new("NodeFrame")
    frame_002.label = "Duplicate Factor"
    frame_002.name = "Frame.002"
    frame_002.label_size = 20
    frame_002.shrink = True

    # Node Domain Size
    domain_size = bi_rail_loft_1.nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.component = 'CURVE'
    domain_size.outputs[0].hide = True
    domain_size.outputs[1].hide = True
    domain_size.outputs[2].hide = True
    domain_size.outputs[3].hide = True
    domain_size.outputs[5].hide = True
    domain_size.outputs[6].hide = True

    # Node Math.002
    math_002 = bi_rail_loft_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False

    # Node Sample Curve
    sample_curve = bi_rail_loft_1.nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.data_type = 'FLOAT'
    sample_curve.mode = 'FACTOR'
    sample_curve.use_all_curves = False
    # Value
    sample_curve.inputs[1].default_value = 0.0

    # Node Spline Parameter.001
    spline_parameter_001 = bi_rail_loft_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.outputs[1].hide = True
    spline_parameter_001.outputs[2].hide = True

    # Node Float to Integer
    float_to_integer = bi_rail_loft_1.nodes.new("FunctionNodeFloatToInt")
    float_to_integer.name = "Float to Integer"
    float_to_integer.rounding_mode = 'FLOOR'

    # Node Math.003
    math_003 = bi_rail_loft_1.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'FRACT'
    math_003.use_clamp = False

    # Node Mix
    mix = bi_rail_loft_1.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'VECTOR'
    mix.factor_mode = 'UNIFORM'

    # Node Reroute.002
    reroute_002 = bi_rail_loft_1.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Node Sample Curve.001
    sample_curve_001 = bi_rail_loft_1.nodes.new("GeometryNodeSampleCurve")
    sample_curve_001.name = "Sample Curve.001"
    sample_curve_001.data_type = 'FLOAT'
    sample_curve_001.mode = 'FACTOR'
    sample_curve_001.use_all_curves = False
    # Value
    sample_curve_001.inputs[1].default_value = 0.0

    # Node Spline Parameter.002
    spline_parameter_002 = bi_rail_loft_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"
    spline_parameter_002.outputs[1].hide = True
    spline_parameter_002.outputs[2].hide = True

    # Node Integer Math.004
    integer_math_004 = bi_rail_loft_1.nodes.new("FunctionNodeIntegerMath")
    integer_math_004.name = "Integer Math.004"
    integer_math_004.hide = True
    integer_math_004.operation = 'ADD'
    # Value_001
    integer_math_004.inputs[1].default_value = 1

    # Node Frame.003
    frame_003 = bi_rail_loft_1.nodes.new("NodeFrame")
    frame_003.label = "Spline Lerp"
    frame_003.name = "Frame.003"
    frame_003.label_size = 20
    frame_003.shrink = True

    # Node Reroute.003
    reroute_003 = bi_rail_loft_1.nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.socket_idname = "NodeSocketGeometry"
    # Node Instance on Points
    instance_on_points = bi_rail_loft_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = True
    # Instance Index
    instance_on_points.inputs[4].default_value = 0

    # Node Split to Instances
    split_to_instances = bi_rail_loft_1.nodes.new("GeometryNodeSplitToInstances")
    split_to_instances.name = "Split to Instances"
    split_to_instances.domain = 'CURVE'
    # Selection
    split_to_instances.inputs[1].default_value = True

    # Node Sample Index
    sample_index = bi_rail_loft_1.nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.clamp = False
    sample_index.data_type = 'FLOAT_VECTOR'
    sample_index.domain = 'POINT'

    # Node Index.002
    index_002 = bi_rail_loft_1.nodes.new("GeometryNodeInputIndex")
    index_002.name = "Index.002"
    index_002.hide = True

    # Node Position.001
    position_001 = bi_rail_loft_1.nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.hide = True

    # Node Vector Math.004
    vector_math_004 = bi_rail_loft_1.nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.operation = 'SUBTRACT'

    # Node Vector Math.005
    vector_math_005 = bi_rail_loft_1.nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.operation = 'LENGTH'

    # Node Align Rotation to Vector.001
    align_rotation_to_vector_001 = bi_rail_loft_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.axis = 'X'
    align_rotation_to_vector_001.pivot_axis = 'AUTO'
    # Rotation
    align_rotation_to_vector_001.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0

    # Node Curve Tangent
    curve_tangent = bi_rail_loft_1.nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"

    # Node Vector Math.006
    vector_math_006 = bi_rail_loft_1.nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.operation = 'CROSS_PRODUCT'

    # Node Align Rotation to Vector.002
    align_rotation_to_vector_002 = bi_rail_loft_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.name = "Align Rotation to Vector.002"
    align_rotation_to_vector_002.axis = 'Y'
    align_rotation_to_vector_002.pivot_axis = 'X'
    # Factor
    align_rotation_to_vector_002.inputs[1].default_value = 1.0

    # Node Frame.004
    frame_004 = bi_rail_loft_1.nodes.new("NodeFrame")
    frame_004.label = "Orient Splines"
    frame_004.name = "Frame.004"
    frame_004.label_size = 20
    frame_004.shrink = True

    # Node Realize Instances.001
    realize_instances_001 = bi_rail_loft_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0

    # Node Resample Curve.003
    resample_curve_003 = bi_rail_loft_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.name = "Resample Curve.003"
    resample_curve_003.keep_last_segment = True
    # Selection
    resample_curve_003.inputs[1].default_value = True
    # Mode
    resample_curve_003.inputs[2].default_value = 'Count'
    # Length
    resample_curve_003.inputs[4].default_value = 0.10000000149011612

    # Node Grid
    grid = bi_rail_loft_1.nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    # Size X
    grid.inputs[0].default_value = 1.0
    # Size Y
    grid.inputs[1].default_value = 1.0

    # Node Set Position.002
    set_position_002 = bi_rail_loft_1.nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Offset
    set_position_002.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Sample Index.001
    sample_index_001 = bi_rail_loft_1.nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.clamp = False
    sample_index_001.data_type = 'FLOAT_VECTOR'
    sample_index_001.domain = 'POINT'

    # Node Position.002
    position_002 = bi_rail_loft_1.nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"

    # Node Index.003
    index_003 = bi_rail_loft_1.nodes.new("GeometryNodeInputIndex")
    index_003.name = "Index.003"

    # Node Set Position.005
    set_position_005 = bi_rail_loft_1.nodes.new("GeometryNodeSetPosition")
    set_position_005.name = "Set Position.005"
    set_position_005.inputs[1].hide = True
    set_position_005.inputs[3].hide = True
    # Selection
    set_position_005.inputs[1].default_value = True
    # Offset
    set_position_005.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Position.005
    position_005 = bi_rail_loft_1.nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"

    # Node Blur Attribute
    blur_attribute = bi_rail_loft_1.nodes.new("GeometryNodeBlurAttribute")
    blur_attribute.name = "Blur Attribute"
    blur_attribute.data_type = 'FLOAT_VECTOR'

    # Node Is Edge Boundary
    is_edge_boundary = bi_rail_loft_1.nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Is Edge Boundary"
    is_edge_boundary.node_tree = bpy.data.node_groups[node_tree_names[is_edge_boundary_1_node_group]]

    # Node Boolean Math
    boolean_math = bi_rail_loft_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.operation = 'NOT'

    # Node Attribute Statistic
    attribute_statistic = bi_rail_loft_1.nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.data_type = 'FLOAT'
    attribute_statistic.domain = 'CURVE'
    attribute_statistic.inputs[1].hide = True
    attribute_statistic.outputs[0].hide = True
    attribute_statistic.outputs[1].hide = True
    attribute_statistic.outputs[2].hide = True
    attribute_statistic.outputs[4].hide = True
    attribute_statistic.outputs[5].hide = True
    attribute_statistic.outputs[6].hide = True
    attribute_statistic.outputs[7].hide = True
    # Selection
    attribute_statistic.inputs[1].default_value = True

    # Node Spline Length.001
    spline_length_001 = bi_rail_loft_1.nodes.new("GeometryNodeSplineLength")
    spline_length_001.name = "Spline Length.001"
    spline_length_001.outputs[1].hide = True

    # Node Math.004
    math_004 = bi_rail_loft_1.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'DIVIDE'
    math_004.use_clamp = False

    # Node Group Input.001
    group_input_001 = bi_rail_loft_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[3].hide = True
    group_input_001.outputs[5].hide = True
    group_input_001.outputs[7].hide = True
    group_input_001.outputs[9].hide = True
    group_input_001.outputs[10].hide = True

    # Node Curve Length
    curve_length = bi_rail_loft_1.nodes.new("GeometryNodeCurveLength")
    curve_length.name = "Curve Length"
    curve_length.hide = True

    # Node Curve Length.001
    curve_length_001 = bi_rail_loft_1.nodes.new("GeometryNodeCurveLength")
    curve_length_001.name = "Curve Length.001"
    curve_length_001.hide = True

    # Node Math.005
    math_005 = bi_rail_loft_1.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.hide = True
    math_005.operation = 'MINIMUM'
    math_005.use_clamp = False

    # Node Math.006
    math_006 = bi_rail_loft_1.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'DIVIDE'
    math_006.use_clamp = False

    # Node Store Named Attribute
    store_named_attribute = bi_rail_loft_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'FLOAT2'
    store_named_attribute.domain = 'CORNER'
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "UVMap"

    # Node Separate XYZ
    separate_xyz = bi_rail_loft_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"

    # Node Combine XYZ
    combine_xyz = bi_rail_loft_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    # Z
    combine_xyz.inputs[2].default_value = 0.0

    # Node Group Input.002
    group_input_002 = bi_rail_loft_1.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[0].hide = True
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[2].hide = True
    group_input_002.outputs[4].hide = True
    group_input_002.outputs[5].hide = True
    group_input_002.outputs[6].hide = True
    group_input_002.outputs[7].hide = True
    group_input_002.outputs[8].hide = True
    group_input_002.outputs[9].hide = True
    group_input_002.outputs[10].hide = True

    # Node Group Input.003
    group_input_003 = bi_rail_loft_1.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.outputs[0].hide = True
    group_input_003.outputs[1].hide = True
    group_input_003.outputs[2].hide = True
    group_input_003.outputs[3].hide = True
    group_input_003.outputs[6].hide = True
    group_input_003.outputs[8].hide = True
    group_input_003.outputs[9].hide = True
    group_input_003.outputs[10].hide = True

    # Node Menu Switch.001
    menu_switch_001 = bi_rail_loft_1.nodes.new("GeometryNodeGroup")
    menu_switch_001.name = "Menu Switch.001"
    menu_switch_001.node_tree = bpy.data.node_groups[node_tree_names[space___res_switch_1_node_group]]

    # Node Menu Switch.002
    menu_switch_002 = bi_rail_loft_1.nodes.new("GeometryNodeGroup")
    menu_switch_002.name = "Menu Switch.002"
    menu_switch_002.node_tree = bpy.data.node_groups[node_tree_names[space___res_switch_1_node_group]]

    # Node Named Attribute
    named_attribute = bi_rail_loft_1.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.data_type = 'FLOAT_VECTOR'
    # Name
    named_attribute.inputs[0].default_value = "UVMap"

    # Node Store Named Attribute.001
    store_named_attribute_001 = bi_rail_loft_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.data_type = 'FLOAT2'
    store_named_attribute_001.domain = 'POINT'
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "UVMap"

    # Node Combine XYZ.001
    combine_xyz_001 = bi_rail_loft_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_001.name = "Combine XYZ.001"
    # Z
    combine_xyz_001.inputs[2].default_value = 0.0

    # Node Spline Parameter.003
    spline_parameter_003 = bi_rail_loft_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_003.name = "Spline Parameter.003"
    spline_parameter_003.outputs[1].hide = True
    spline_parameter_003.outputs[2].hide = True

    # Node Capture Attribute
    capture_attribute = bi_rail_loft_1.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.active_index = 0
    capture_attribute.capture_items.clear()
    capture_attribute.capture_items.new('FLOAT', "Factor")
    capture_attribute.capture_items["Factor"].data_type = 'FLOAT'
    capture_attribute.domain = 'POINT'

    # Node Spline Parameter.004
    spline_parameter_004 = bi_rail_loft_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_004.name = "Spline Parameter.004"
    spline_parameter_004.outputs[1].hide = True
    spline_parameter_004.outputs[2].hide = True

    # Node Field Average
    field_average = bi_rail_loft_1.nodes.new("GeometryNodeFieldAverage")
    field_average.name = "Field Average"
    field_average.data_type = 'FLOAT_VECTOR'
    field_average.domain = 'POINT'
    # Group Index
    field_average.inputs[1].default_value = 0

    # Node Compare
    compare = bi_rail_loft_1.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'VECTOR'
    compare.mode = 'DIRECTION'
    compare.operation = 'EQUAL'
    # Angle
    compare.inputs[11].default_value = 0.0
    # Epsilon
    compare.inputs[12].default_value = 1.5707963705062866

    # Node Switch
    switch = bi_rail_loft_1.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'FLOAT'
    # False
    switch.inputs[1].default_value = -1.0
    # True
    switch.inputs[2].default_value = 1.0

    # Node Vector Math.007
    vector_math_007 = bi_rail_loft_1.nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.operation = 'SCALE'

    # Node Domain Size.001
    domain_size_001 = bi_rail_loft_1.nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_001.name = "Domain Size.001"
    domain_size_001.component = 'CURVE'

    # Node Separate Components
    separate_components = bi_rail_loft_1.nodes.new("GeometryNodeSeparateComponents")
    separate_components.name = "Separate Components"
    separate_components.outputs[0].hide = True
    separate_components.outputs[2].hide = True
    separate_components.outputs[3].hide = True
    separate_components.outputs[4].hide = True
    separate_components.outputs[5].hide = True

    # Node Curve Line
    curve_line = bi_rail_loft_1.nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.mode = 'POINTS'
    # Start
    curve_line.inputs[0].default_value = (0.0, 0.0, 0.0)
    # End
    curve_line.inputs[1].default_value = (0.0, 0.0, 1.0)

    # Node Switch.001
    switch_001 = bi_rail_loft_1.nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.input_type = 'GEOMETRY'

    # Node Compare.001
    compare_001 = bi_rail_loft_1.nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.data_type = 'INT'
    compare_001.mode = 'ELEMENT'
    compare_001.operation = 'EQUAL'
    # B_INT
    compare_001.inputs[3].default_value = 0

    # Node Group Input.004
    group_input_004 = bi_rail_loft_1.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.outputs[0].hide = True
    group_input_004.outputs[1].hide = True
    group_input_004.outputs[2].hide = True
    group_input_004.outputs[3].hide = True
    group_input_004.outputs[4].hide = True
    group_input_004.outputs[5].hide = True
    group_input_004.outputs[6].hide = True
    group_input_004.outputs[7].hide = True
    group_input_004.outputs[8].hide = True
    group_input_004.outputs[10].hide = True

    # Node Evaluate Closure
    evaluate_closure = bi_rail_loft_1.nodes.new("NodeEvaluateClosure")
    evaluate_closure.name = "Evaluate Closure"
    evaluate_closure.active_input_index = 0
    evaluate_closure.active_output_index = 0
    evaluate_closure.define_signature = False
    evaluate_closure.input_items.clear()
    evaluate_closure.input_items.new('FLOAT', "Factor")
    evaluate_closure.input_items[0].structure_type = 'AUTO'
    evaluate_closure.output_items.clear()
    evaluate_closure.output_items.new('FLOAT', "Factor")
    evaluate_closure.output_items[0].structure_type = 'AUTO'

    # Set parents
    bi_rail_loft_1.nodes["Set Position"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Evaluate at Index"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Position"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Vector Math"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Spline Length"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Index"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Spline Parameter"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Integer Math"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Integer Math.001"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Integer Math.002"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Rotate Vector"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Align Rotation to Vector"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Evaluate at Index.001"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Vector Math.001"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Invert Rotation"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Vector Math.002"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Vector Math.003"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Math"].parent = bi_rail_loft_1.nodes["Frame.001"]
    bi_rail_loft_1.nodes["Math.001"].parent = bi_rail_loft_1.nodes["Frame.002"]
    bi_rail_loft_1.nodes["Integer Math.003"].parent = bi_rail_loft_1.nodes["Frame.002"]
    bi_rail_loft_1.nodes["Domain Size"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Math.002"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Sample Curve"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Spline Parameter.001"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Float to Integer"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Math.003"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Mix"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Reroute.002"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Sample Curve.001"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Spline Parameter.002"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Integer Math.004"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Reroute.003"].parent = bi_rail_loft_1.nodes["Frame.003"]
    bi_rail_loft_1.nodes["Sample Index"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Index.002"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Position.001"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Vector Math.004"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Vector Math.005"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Align Rotation to Vector.001"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Curve Tangent"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Vector Math.006"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Align Rotation to Vector.002"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Field Average"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Compare"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Switch"].parent = bi_rail_loft_1.nodes["Frame.004"]
    bi_rail_loft_1.nodes["Vector Math.007"].parent = bi_rail_loft_1.nodes["Frame.004"]

    # Set locations
    bi_rail_loft_1.nodes["Group Output"].location = (3920.0, 620.0)
    bi_rail_loft_1.nodes["Group Input"].location = (-4300.0, -140.0)
    bi_rail_loft_1.nodes["Realize Instances"].location = (-4140.0, -140.0)
    bi_rail_loft_1.nodes["Resample Curve"].location = (-1440.0, 340.0)
    bi_rail_loft_1.nodes["Resample Curve.001"].location = (-1440.0, 200.0)
    bi_rail_loft_1.nodes["Set Position"].location = (1549.0, -35.79999542236328)
    bi_rail_loft_1.nodes["Evaluate at Index"].location = (529.0, -175.79998779296875)
    bi_rail_loft_1.nodes["Position"].location = (369.0, -175.79998779296875)
    bi_rail_loft_1.nodes["Vector Math"].location = (689.0, -175.79998779296875)
    bi_rail_loft_1.nodes["Spline Length"].location = (29.0, -515.7999877929688)
    bi_rail_loft_1.nodes["Index"].location = (29.0, -375.79998779296875)
    bi_rail_loft_1.nodes["Spline Parameter"].location = (29.0, -435.79998779296875)
    bi_rail_loft_1.nodes["Integer Math"].location = (189.0, -375.79998779296875)
    bi_rail_loft_1.nodes["Integer Math.001"].location = (349.0, -415.79998779296875)
    bi_rail_loft_1.nodes["Integer Math.002"].location = (189.0, -515.7999877929688)
    bi_rail_loft_1.nodes["Rotate Vector"].location = (1109.0, -175.79998779296875)
    bi_rail_loft_1.nodes["Align Rotation to Vector"].location = (949.0, -395.79998779296875)
    bi_rail_loft_1.nodes["Evaluate at Index.001"].location = (529.0, -295.79998779296875)
    bi_rail_loft_1.nodes["Vector Math.001"].location = (729.0, -395.79998779296875)
    bi_rail_loft_1.nodes["Invert Rotation"].location = (1109.0, -395.79998779296875)
    bi_rail_loft_1.nodes["Vector Math.002"].location = (1349.0, -175.79998779296875)
    bi_rail_loft_1.nodes["Vector Math.003"].location = (949.0, -575.7999877929688)
    bi_rail_loft_1.nodes["Math"].location = (1129.0, -575.7999877929688)
    bi_rail_loft_1.nodes["Resample Curve.002"].location = (-3260.0, -140.0)
    bi_rail_loft_1.nodes["Frame.001"].location = (-3049.0, -84.20000457763672)
    bi_rail_loft_1.nodes["Separate Geometry"].location = (-1220.0, -20.0)
    bi_rail_loft_1.nodes["Index.001"].location = (-1220.0, -180.0)
    bi_rail_loft_1.nodes["Duplicate Elements"].location = (-1020.0, 180.0)
    bi_rail_loft_1.nodes["Set Position.001"].location = (900.0, 120.0)
    bi_rail_loft_1.nodes["Math.001"].location = (49.0, -39.66666793823242)
    bi_rail_loft_1.nodes["Reroute.001"].location = (-1080.0, 20.0)
    bi_rail_loft_1.nodes["Integer Math.003"].location = (29.0, -79.66666412353516)
    bi_rail_loft_1.nodes["Frame.002"].location = (-889.0, -0.3333333432674408)
    bi_rail_loft_1.nodes["Domain Size"].location = (29.0, -195.8000030517578)
    bi_rail_loft_1.nodes["Math.002"].location = (209.0, -35.80000305175781)
    bi_rail_loft_1.nodes["Sample Curve"].location = (669.0, -215.8000030517578)
    bi_rail_loft_1.nodes["Spline Parameter.001"].location = (489.0, -435.79998779296875)
    bi_rail_loft_1.nodes["Float to Integer"].location = (429.0, -175.8000030517578)
    bi_rail_loft_1.nodes["Math.003"].location = (429.0, -35.80000305175781)
    bi_rail_loft_1.nodes["Mix"].location = (849.0, -95.80000305175781)
    bi_rail_loft_1.nodes["Reroute.002"].location = (569.0, -555.7999877929688)
    bi_rail_loft_1.nodes["Sample Curve.001"].location = (669.0, -495.79998779296875)
    bi_rail_loft_1.nodes["Spline Parameter.002"].location = (489.0, -715.7999877929688)
    bi_rail_loft_1.nodes["Integer Math.004"].location = (489.0, -675.7999877929688)
    bi_rail_loft_1.nodes["Frame.003"].location = (-189.0, -144.1999969482422)
    bi_rail_loft_1.nodes["Reroute.003"].location = (89.0, -555.7999877929688)
    bi_rail_loft_1.nodes["Instance on Points"].location = (1460.0, 360.0)
    bi_rail_loft_1.nodes["Split to Instances"].location = (1060.0, 120.0)
    bi_rail_loft_1.nodes["Sample Index"].location = (29.0, -95.7999267578125)
    bi_rail_loft_1.nodes["Index.002"].location = (29.0, -335.7999267578125)
    bi_rail_loft_1.nodes["Position.001"].location = (29.0, -295.7999267578125)
    bi_rail_loft_1.nodes["Vector Math.004"].location = (189.0, -95.7999267578125)
    bi_rail_loft_1.nodes["Vector Math.005"].location = (1049.0, -35.7999267578125)
    bi_rail_loft_1.nodes["Align Rotation to Vector.001"].location = (1049.0, -155.7999267578125)
    bi_rail_loft_1.nodes["Curve Tangent"].location = (249.0, -455.7999267578125)
    bi_rail_loft_1.nodes["Vector Math.006"].location = (449.0, -395.7999267578125)
    bi_rail_loft_1.nodes["Align Rotation to Vector.002"].location = (1209.0, -155.7999267578125)
    bi_rail_loft_1.nodes["Frame.004"].location = (131.0, 1035.7999267578125)
    bi_rail_loft_1.nodes["Realize Instances.001"].location = (1620.0, 360.0)
    bi_rail_loft_1.nodes["Resample Curve.003"].location = (2200.0, 360.0)
    bi_rail_loft_1.nodes["Grid"].location = (2380.0, 740.0)
    bi_rail_loft_1.nodes["Set Position.002"].location = (3020.0, 780.0)
    bi_rail_loft_1.nodes["Sample Index.001"].location = (2720.0, 420.0)
    bi_rail_loft_1.nodes["Position.002"].location = (2720.0, 220.0)
    bi_rail_loft_1.nodes["Index.003"].location = (2720.0, 160.0)
    bi_rail_loft_1.nodes["Set Position.005"].location = (3620.0, 680.0)
    bi_rail_loft_1.nodes["Position.005"].location = (3460.0, 600.0)
    bi_rail_loft_1.nodes["Blur Attribute"].location = (3620.0, 600.0)
    bi_rail_loft_1.nodes["Is Edge Boundary"].location = (3460.0, 440.0)
    bi_rail_loft_1.nodes["Boolean Math"].location = (3460.0, 540.0)
    bi_rail_loft_1.nodes["Attribute Statistic"].location = (1780.0, 40.0)
    bi_rail_loft_1.nodes["Spline Length.001"].location = (1620.0, -60.0)
    bi_rail_loft_1.nodes["Math.004"].location = (1940.0, 40.0)
    bi_rail_loft_1.nodes["Group Input.001"].location = (-2400.0, 240.0)
    bi_rail_loft_1.nodes["Curve Length"].location = (-2160.0, 480.0)
    bi_rail_loft_1.nodes["Curve Length.001"].location = (-2160.0, 440.0)
    bi_rail_loft_1.nodes["Math.005"].location = (-2000.0, 460.0)
    bi_rail_loft_1.nodes["Math.006"].location = (-2000.0, 420.0)
    bi_rail_loft_1.nodes["Store Named Attribute"].location = (2860.0, 780.0)
    bi_rail_loft_1.nodes["Separate XYZ"].location = (2540.0, 660.0)
    bi_rail_loft_1.nodes["Combine XYZ"].location = (2700.0, 660.0)
    bi_rail_loft_1.nodes["Group Input.002"].location = (3620.0, 480.0)
    bi_rail_loft_1.nodes["Group Input.003"].location = (1660.0, -180.0)
    bi_rail_loft_1.nodes["Menu Switch.001"].location = (2140.0, -120.0)
    bi_rail_loft_1.nodes["Menu Switch.002"].location = (-1720.0, 180.0)
    bi_rail_loft_1.nodes["Named Attribute"].location = (3920.0, 480.0)
    bi_rail_loft_1.nodes["Store Named Attribute.001"].location = (2760.0, 40.0)
    bi_rail_loft_1.nodes["Combine XYZ.001"].location = (2580.0, -80.0)
    bi_rail_loft_1.nodes["Spline Parameter.003"].location = (2400.0, -80.0)
    bi_rail_loft_1.nodes["Capture Attribute"].location = (1060.0, 260.0)
    bi_rail_loft_1.nodes["Spline Parameter.004"].location = (900.0, 200.0)
    bi_rail_loft_1.nodes["Field Average"].location = (449.0, -535.7999267578125)
    bi_rail_loft_1.nodes["Compare"].location = (629.0, -455.7999267578125)
    bi_rail_loft_1.nodes["Switch"].location = (809.0, -455.7999267578125)
    bi_rail_loft_1.nodes["Vector Math.007"].location = (1049.0, -315.7999267578125)
    bi_rail_loft_1.nodes["Domain Size.001"].location = (-3780.0, 40.0)
    bi_rail_loft_1.nodes["Separate Components"].location = (-3980.0, -140.0)
    bi_rail_loft_1.nodes["Curve Line"].location = (-3660.0, -280.0)
    bi_rail_loft_1.nodes["Switch.001"].location = (-3440.0, -120.0)
    bi_rail_loft_1.nodes["Compare.001"].location = (-3620.0, 40.0)
    bi_rail_loft_1.nodes["Group Input.004"].location = (-520.0, -20.0)
    bi_rail_loft_1.nodes["Evaluate Closure"].location = (-520.0, -100.0)

    # Set dimensions
    bi_rail_loft_1.nodes["Group Output"].width  = 140.0
    bi_rail_loft_1.nodes["Group Output"].height = 100.0

    bi_rail_loft_1.nodes["Group Input"].width  = 140.0
    bi_rail_loft_1.nodes["Group Input"].height = 100.0

    bi_rail_loft_1.nodes["Realize Instances"].width  = 140.0
    bi_rail_loft_1.nodes["Realize Instances"].height = 100.0

    bi_rail_loft_1.nodes["Resample Curve"].width  = 140.0
    bi_rail_loft_1.nodes["Resample Curve"].height = 100.0

    bi_rail_loft_1.nodes["Resample Curve.001"].width  = 140.0
    bi_rail_loft_1.nodes["Resample Curve.001"].height = 100.0

    bi_rail_loft_1.nodes["Set Position"].width  = 140.0
    bi_rail_loft_1.nodes["Set Position"].height = 100.0

    bi_rail_loft_1.nodes["Evaluate at Index"].width  = 140.0
    bi_rail_loft_1.nodes["Evaluate at Index"].height = 100.0

    bi_rail_loft_1.nodes["Position"].width  = 140.0
    bi_rail_loft_1.nodes["Position"].height = 100.0

    bi_rail_loft_1.nodes["Vector Math"].width  = 140.0
    bi_rail_loft_1.nodes["Vector Math"].height = 100.0

    bi_rail_loft_1.nodes["Spline Length"].width  = 140.0
    bi_rail_loft_1.nodes["Spline Length"].height = 100.0

    bi_rail_loft_1.nodes["Index"].width  = 140.0
    bi_rail_loft_1.nodes["Index"].height = 100.0

    bi_rail_loft_1.nodes["Spline Parameter"].width  = 140.0
    bi_rail_loft_1.nodes["Spline Parameter"].height = 100.0

    bi_rail_loft_1.nodes["Integer Math"].width  = 140.0
    bi_rail_loft_1.nodes["Integer Math"].height = 100.0

    bi_rail_loft_1.nodes["Integer Math.001"].width  = 140.0
    bi_rail_loft_1.nodes["Integer Math.001"].height = 100.0

    bi_rail_loft_1.nodes["Integer Math.002"].width  = 140.0
    bi_rail_loft_1.nodes["Integer Math.002"].height = 100.0

    bi_rail_loft_1.nodes["Rotate Vector"].width  = 140.0
    bi_rail_loft_1.nodes["Rotate Vector"].height = 100.0

    bi_rail_loft_1.nodes["Align Rotation to Vector"].width  = 140.0
    bi_rail_loft_1.nodes["Align Rotation to Vector"].height = 100.0

    bi_rail_loft_1.nodes["Evaluate at Index.001"].width  = 140.0
    bi_rail_loft_1.nodes["Evaluate at Index.001"].height = 100.0

    bi_rail_loft_1.nodes["Vector Math.001"].width  = 140.0
    bi_rail_loft_1.nodes["Vector Math.001"].height = 100.0

    bi_rail_loft_1.nodes["Invert Rotation"].width  = 140.0
    bi_rail_loft_1.nodes["Invert Rotation"].height = 100.0

    bi_rail_loft_1.nodes["Vector Math.002"].width  = 140.0
    bi_rail_loft_1.nodes["Vector Math.002"].height = 100.0

    bi_rail_loft_1.nodes["Vector Math.003"].width  = 140.0
    bi_rail_loft_1.nodes["Vector Math.003"].height = 100.0

    bi_rail_loft_1.nodes["Math"].width  = 140.0
    bi_rail_loft_1.nodes["Math"].height = 100.0

    bi_rail_loft_1.nodes["Resample Curve.002"].width  = 140.0
    bi_rail_loft_1.nodes["Resample Curve.002"].height = 100.0

    bi_rail_loft_1.nodes["Frame.001"].width  = 1718.0
    bi_rail_loft_1.nodes["Frame.001"].height = 746.13330078125

    bi_rail_loft_1.nodes["Separate Geometry"].width  = 140.0
    bi_rail_loft_1.nodes["Separate Geometry"].height = 100.0

    bi_rail_loft_1.nodes["Index.001"].width  = 140.0
    bi_rail_loft_1.nodes["Index.001"].height = 100.0

    bi_rail_loft_1.nodes["Duplicate Elements"].width  = 140.0
    bi_rail_loft_1.nodes["Duplicate Elements"].height = 100.0

    bi_rail_loft_1.nodes["Set Position.001"].width  = 140.0
    bi_rail_loft_1.nodes["Set Position.001"].height = 100.0

    bi_rail_loft_1.nodes["Math.001"].width  = 140.0
    bi_rail_loft_1.nodes["Math.001"].height = 100.0

    bi_rail_loft_1.nodes["Reroute.001"].width  = 14.5
    bi_rail_loft_1.nodes["Reroute.001"].height = 100.0

    bi_rail_loft_1.nodes["Integer Math.003"].width  = 140.0
    bi_rail_loft_1.nodes["Integer Math.003"].height = 100.0

    bi_rail_loft_1.nodes["Frame.002"].width  = 218.0
    bi_rail_loft_1.nodes["Frame.002"].height = 131.86666870117188

    bi_rail_loft_1.nodes["Domain Size"].width  = 140.0
    bi_rail_loft_1.nodes["Domain Size"].height = 100.0

    bi_rail_loft_1.nodes["Math.002"].width  = 140.0
    bi_rail_loft_1.nodes["Math.002"].height = 100.0

    bi_rail_loft_1.nodes["Sample Curve"].width  = 140.0
    bi_rail_loft_1.nodes["Sample Curve"].height = 100.0

    bi_rail_loft_1.nodes["Spline Parameter.001"].width  = 140.0
    bi_rail_loft_1.nodes["Spline Parameter.001"].height = 100.0

    bi_rail_loft_1.nodes["Float to Integer"].width  = 140.0
    bi_rail_loft_1.nodes["Float to Integer"].height = 100.0

    bi_rail_loft_1.nodes["Math.003"].width  = 140.0
    bi_rail_loft_1.nodes["Math.003"].height = 100.0

    bi_rail_loft_1.nodes["Mix"].width  = 140.0
    bi_rail_loft_1.nodes["Mix"].height = 100.0

    bi_rail_loft_1.nodes["Reroute.002"].width  = 14.5
    bi_rail_loft_1.nodes["Reroute.002"].height = 100.0

    bi_rail_loft_1.nodes["Sample Curve.001"].width  = 140.0
    bi_rail_loft_1.nodes["Sample Curve.001"].height = 100.0

    bi_rail_loft_1.nodes["Spline Parameter.002"].width  = 140.0
    bi_rail_loft_1.nodes["Spline Parameter.002"].height = 100.0

    bi_rail_loft_1.nodes["Integer Math.004"].width  = 140.0
    bi_rail_loft_1.nodes["Integer Math.004"].height = 100.0

    bi_rail_loft_1.nodes["Frame.003"].width  = 1018.0
    bi_rail_loft_1.nodes["Frame.003"].height = 794.13330078125

    bi_rail_loft_1.nodes["Reroute.003"].width  = 14.5
    bi_rail_loft_1.nodes["Reroute.003"].height = 100.0

    bi_rail_loft_1.nodes["Instance on Points"].width  = 140.0
    bi_rail_loft_1.nodes["Instance on Points"].height = 100.0

    bi_rail_loft_1.nodes["Split to Instances"].width  = 140.0
    bi_rail_loft_1.nodes["Split to Instances"].height = 100.0

    bi_rail_loft_1.nodes["Sample Index"].width  = 140.0
    bi_rail_loft_1.nodes["Sample Index"].height = 100.0

    bi_rail_loft_1.nodes["Index.002"].width  = 140.0
    bi_rail_loft_1.nodes["Index.002"].height = 100.0

    bi_rail_loft_1.nodes["Position.001"].width  = 140.0
    bi_rail_loft_1.nodes["Position.001"].height = 100.0

    bi_rail_loft_1.nodes["Vector Math.004"].width  = 140.0
    bi_rail_loft_1.nodes["Vector Math.004"].height = 100.0

    bi_rail_loft_1.nodes["Vector Math.005"].width  = 140.0
    bi_rail_loft_1.nodes["Vector Math.005"].height = 100.0

    bi_rail_loft_1.nodes["Align Rotation to Vector.001"].width  = 140.0
    bi_rail_loft_1.nodes["Align Rotation to Vector.001"].height = 100.0

    bi_rail_loft_1.nodes["Curve Tangent"].width  = 140.0
    bi_rail_loft_1.nodes["Curve Tangent"].height = 100.0

    bi_rail_loft_1.nodes["Vector Math.006"].width  = 140.0
    bi_rail_loft_1.nodes["Vector Math.006"].height = 100.0

    bi_rail_loft_1.nodes["Align Rotation to Vector.002"].width  = 140.0
    bi_rail_loft_1.nodes["Align Rotation to Vector.002"].height = 100.0

    bi_rail_loft_1.nodes["Frame.004"].width  = 1378.0
    bi_rail_loft_1.nodes["Frame.004"].height = 726.7999267578125

    bi_rail_loft_1.nodes["Realize Instances.001"].width  = 140.0
    bi_rail_loft_1.nodes["Realize Instances.001"].height = 100.0

    bi_rail_loft_1.nodes["Resample Curve.003"].width  = 140.0
    bi_rail_loft_1.nodes["Resample Curve.003"].height = 100.0

    bi_rail_loft_1.nodes["Grid"].width  = 140.0
    bi_rail_loft_1.nodes["Grid"].height = 100.0

    bi_rail_loft_1.nodes["Set Position.002"].width  = 140.0
    bi_rail_loft_1.nodes["Set Position.002"].height = 100.0

    bi_rail_loft_1.nodes["Sample Index.001"].width  = 140.0
    bi_rail_loft_1.nodes["Sample Index.001"].height = 100.0

    bi_rail_loft_1.nodes["Position.002"].width  = 140.0
    bi_rail_loft_1.nodes["Position.002"].height = 100.0

    bi_rail_loft_1.nodes["Index.003"].width  = 140.0
    bi_rail_loft_1.nodes["Index.003"].height = 100.0

    bi_rail_loft_1.nodes["Set Position.005"].width  = 140.0
    bi_rail_loft_1.nodes["Set Position.005"].height = 100.0

    bi_rail_loft_1.nodes["Position.005"].width  = 140.0
    bi_rail_loft_1.nodes["Position.005"].height = 100.0

    bi_rail_loft_1.nodes["Blur Attribute"].width  = 140.0
    bi_rail_loft_1.nodes["Blur Attribute"].height = 100.0

    bi_rail_loft_1.nodes["Is Edge Boundary"].width  = 140.0
    bi_rail_loft_1.nodes["Is Edge Boundary"].height = 100.0

    bi_rail_loft_1.nodes["Boolean Math"].width  = 140.0
    bi_rail_loft_1.nodes["Boolean Math"].height = 100.0

    bi_rail_loft_1.nodes["Attribute Statistic"].width  = 140.0
    bi_rail_loft_1.nodes["Attribute Statistic"].height = 100.0

    bi_rail_loft_1.nodes["Spline Length.001"].width  = 140.0
    bi_rail_loft_1.nodes["Spline Length.001"].height = 100.0

    bi_rail_loft_1.nodes["Math.004"].width  = 140.0
    bi_rail_loft_1.nodes["Math.004"].height = 100.0

    bi_rail_loft_1.nodes["Group Input.001"].width  = 140.0
    bi_rail_loft_1.nodes["Group Input.001"].height = 100.0

    bi_rail_loft_1.nodes["Curve Length"].width  = 140.0
    bi_rail_loft_1.nodes["Curve Length"].height = 100.0

    bi_rail_loft_1.nodes["Curve Length.001"].width  = 140.0
    bi_rail_loft_1.nodes["Curve Length.001"].height = 100.0

    bi_rail_loft_1.nodes["Math.005"].width  = 140.0
    bi_rail_loft_1.nodes["Math.005"].height = 100.0

    bi_rail_loft_1.nodes["Math.006"].width  = 140.0
    bi_rail_loft_1.nodes["Math.006"].height = 100.0

    bi_rail_loft_1.nodes["Store Named Attribute"].width  = 140.0
    bi_rail_loft_1.nodes["Store Named Attribute"].height = 100.0

    bi_rail_loft_1.nodes["Separate XYZ"].width  = 140.0
    bi_rail_loft_1.nodes["Separate XYZ"].height = 100.0

    bi_rail_loft_1.nodes["Combine XYZ"].width  = 140.0
    bi_rail_loft_1.nodes["Combine XYZ"].height = 100.0

    bi_rail_loft_1.nodes["Group Input.002"].width  = 140.0
    bi_rail_loft_1.nodes["Group Input.002"].height = 100.0

    bi_rail_loft_1.nodes["Group Input.003"].width  = 140.0
    bi_rail_loft_1.nodes["Group Input.003"].height = 100.0

    bi_rail_loft_1.nodes["Menu Switch.001"].width  = 140.0
    bi_rail_loft_1.nodes["Menu Switch.001"].height = 100.0

    bi_rail_loft_1.nodes["Menu Switch.002"].width  = 140.0
    bi_rail_loft_1.nodes["Menu Switch.002"].height = 100.0

    bi_rail_loft_1.nodes["Named Attribute"].width  = 140.0
    bi_rail_loft_1.nodes["Named Attribute"].height = 100.0

    bi_rail_loft_1.nodes["Store Named Attribute.001"].width  = 140.0
    bi_rail_loft_1.nodes["Store Named Attribute.001"].height = 100.0

    bi_rail_loft_1.nodes["Combine XYZ.001"].width  = 140.0
    bi_rail_loft_1.nodes["Combine XYZ.001"].height = 100.0

    bi_rail_loft_1.nodes["Spline Parameter.003"].width  = 140.0
    bi_rail_loft_1.nodes["Spline Parameter.003"].height = 100.0

    bi_rail_loft_1.nodes["Capture Attribute"].width  = 140.0
    bi_rail_loft_1.nodes["Capture Attribute"].height = 100.0

    bi_rail_loft_1.nodes["Spline Parameter.004"].width  = 140.0
    bi_rail_loft_1.nodes["Spline Parameter.004"].height = 100.0

    bi_rail_loft_1.nodes["Field Average"].width  = 140.0
    bi_rail_loft_1.nodes["Field Average"].height = 100.0

    bi_rail_loft_1.nodes["Compare"].width  = 140.0
    bi_rail_loft_1.nodes["Compare"].height = 100.0

    bi_rail_loft_1.nodes["Switch"].width  = 140.0
    bi_rail_loft_1.nodes["Switch"].height = 100.0

    bi_rail_loft_1.nodes["Vector Math.007"].width  = 140.0
    bi_rail_loft_1.nodes["Vector Math.007"].height = 100.0

    bi_rail_loft_1.nodes["Domain Size.001"].width  = 140.0
    bi_rail_loft_1.nodes["Domain Size.001"].height = 100.0

    bi_rail_loft_1.nodes["Separate Components"].width  = 140.0
    bi_rail_loft_1.nodes["Separate Components"].height = 100.0

    bi_rail_loft_1.nodes["Curve Line"].width  = 140.0
    bi_rail_loft_1.nodes["Curve Line"].height = 100.0

    bi_rail_loft_1.nodes["Switch.001"].width  = 140.0
    bi_rail_loft_1.nodes["Switch.001"].height = 100.0

    bi_rail_loft_1.nodes["Compare.001"].width  = 140.0
    bi_rail_loft_1.nodes["Compare.001"].height = 100.0

    bi_rail_loft_1.nodes["Group Input.004"].width  = 140.0
    bi_rail_loft_1.nodes["Group Input.004"].height = 100.0

    bi_rail_loft_1.nodes["Evaluate Closure"].width  = 140.0
    bi_rail_loft_1.nodes["Evaluate Closure"].height = 100.0


    # Initialize bi_rail_loft_1 links

    # spline_length_001.Length -> attribute_statistic.Attribute
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Spline Length.001"].outputs[0],
        bi_rail_loft_1.nodes["Attribute Statistic"].inputs[2]
    )
    # vector_math.Vector -> rotate_vector.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math"].outputs[0],
        bi_rail_loft_1.nodes["Rotate Vector"].inputs[0]
    )
    # integer_math.Value -> evaluate_at_index.Index
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Integer Math"].outputs[0],
        bi_rail_loft_1.nodes["Evaluate at Index"].inputs[1]
    )
    # capture_attribute.Geometry -> instance_on_points.Points
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Capture Attribute"].outputs[0],
        bi_rail_loft_1.nodes["Instance on Points"].inputs[0]
    )
    # blur_attribute.Value -> set_position_005.Position
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Blur Attribute"].outputs[0],
        bi_rail_loft_1.nodes["Set Position.005"].inputs[2]
    )
    # reroute_001.Output -> integer_math_003.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Reroute.001"].outputs[0],
        bi_rail_loft_1.nodes["Integer Math.003"].inputs[0]
    )
    # group_input_001.Rail Curve -> resample_curve.Curve
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.001"].outputs[0],
        bi_rail_loft_1.nodes["Resample Curve"].inputs[0]
    )
    # integer_math_004.Value -> sample_curve_001.Curve Index
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Integer Math.004"].outputs[0],
        bi_rail_loft_1.nodes["Sample Curve.001"].inputs[4]
    )
    # index_003.Index -> sample_index_001.Index
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Index.003"].outputs[0],
        bi_rail_loft_1.nodes["Sample Index.001"].inputs[2]
    )
    # vector_math_002.Vector -> set_position.Position
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.002"].outputs[0],
        bi_rail_loft_1.nodes["Set Position"].inputs[2]
    )
    # position_002.Position -> sample_index_001.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Position.002"].outputs[0],
        bi_rail_loft_1.nodes["Sample Index.001"].inputs[1]
    )
    # duplicate_elements.Geometry -> set_position_001.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Duplicate Elements"].outputs[0],
        bi_rail_loft_1.nodes["Set Position.001"].inputs[0]
    )
    # attribute_statistic.Min -> math_004.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Attribute Statistic"].outputs[3],
        bi_rail_loft_1.nodes["Math.004"].inputs[0]
    )
    # integer_math_003.Value -> math_001.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Integer Math.003"].outputs[0],
        bi_rail_loft_1.nodes["Math.001"].inputs[1]
    )
    # resample_curve_003.Curve -> sample_index_001.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Resample Curve.003"].outputs[0],
        bi_rail_loft_1.nodes["Sample Index.001"].inputs[0]
    )
    # vector_math_005.Value -> instance_on_points.Scale
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.005"].outputs[1],
        bi_rail_loft_1.nodes["Instance on Points"].inputs[6]
    )
    # set_position_001.Geometry -> split_to_instances.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Set Position.001"].outputs[0],
        bi_rail_loft_1.nodes["Split to Instances"].inputs[0]
    )
    # group_input_001.Rail Curve -> resample_curve_001.Curve
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.001"].outputs[1],
        bi_rail_loft_1.nodes["Resample Curve.001"].inputs[0]
    )
    # rotate_vector.Vector -> vector_math_002.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Rotate Vector"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.002"].inputs[0]
    )
    # menu_switch_002.Output -> resample_curve.Count
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Menu Switch.002"].outputs[0],
        bi_rail_loft_1.nodes["Resample Curve"].inputs[3]
    )
    # sample_index_001.Value -> set_position_002.Position
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Sample Index.001"].outputs[0],
        bi_rail_loft_1.nodes["Set Position.002"].inputs[2]
    )
    # reroute_002.Output -> sample_curve.Curves
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Reroute.002"].outputs[0],
        bi_rail_loft_1.nodes["Sample Curve"].inputs[0]
    )
    # menu_switch_002.Output -> resample_curve_001.Count
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Menu Switch.002"].outputs[0],
        bi_rail_loft_1.nodes["Resample Curve.001"].inputs[3]
    )
    # align_rotation_to_vector_002.Rotation -> instance_on_points.Rotation
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Align Rotation to Vector.002"].outputs[0],
        bi_rail_loft_1.nodes["Instance on Points"].inputs[5]
    )
    # align_rotation_to_vector.Rotation -> invert_rotation.Rotation
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Align Rotation to Vector"].outputs[0],
        bi_rail_loft_1.nodes["Invert Rotation"].inputs[0]
    )
    # vector_math_004.Vector -> align_rotation_to_vector_001.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.004"].outputs[0],
        bi_rail_loft_1.nodes["Align Rotation to Vector.001"].inputs[2]
    )
    # reroute_002.Output -> sample_curve_001.Curves
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Reroute.002"].outputs[0],
        bi_rail_loft_1.nodes["Sample Curve.001"].inputs[0]
    )
    # separate_geometry.Selection -> domain_size.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Separate Geometry"].outputs[0],
        bi_rail_loft_1.nodes["Domain Size"].inputs[0]
    )
    # vector_math_007.Vector -> align_rotation_to_vector_002.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.007"].outputs[0],
        bi_rail_loft_1.nodes["Align Rotation to Vector.002"].inputs[2]
    )
    # set_position_002.Geometry -> set_position_005.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Set Position.002"].outputs[0],
        bi_rail_loft_1.nodes["Set Position.005"].inputs[0]
    )
    # resample_curve_002.Curve -> set_position.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Resample Curve.002"].outputs[0],
        bi_rail_loft_1.nodes["Set Position"].inputs[0]
    )
    # position.Position -> vector_math.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Position"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math"].inputs[2]
    )
    # float_to_integer.Integer -> integer_math_004.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Float to Integer"].outputs[0],
        bi_rail_loft_1.nodes["Integer Math.004"].inputs[0]
    )
    # set_position.Geometry -> reroute_003.Input
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Set Position"].outputs[0],
        bi_rail_loft_1.nodes["Reroute.003"].inputs[0]
    )
    # index.Index -> integer_math.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Index"].outputs[0],
        bi_rail_loft_1.nodes["Integer Math"].inputs[0]
    )
    # math.Value -> vector_math_002.Scale
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Math"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.002"].inputs[3]
    )
    # float_to_integer.Integer -> sample_curve.Curve Index
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Float to Integer"].outputs[0],
        bi_rail_loft_1.nodes["Sample Curve"].inputs[4]
    )
    # integer_math_001.Value -> evaluate_at_index_001.Index
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Integer Math.001"].outputs[0],
        bi_rail_loft_1.nodes["Evaluate at Index.001"].inputs[1]
    )
    # reroute_003.Output -> reroute_002.Input
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Reroute.003"].outputs[0],
        bi_rail_loft_1.nodes["Reroute.002"].inputs[0]
    )
    # evaluate_at_index.Value -> vector_math_001.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Evaluate at Index"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.001"].inputs[1]
    )
    # position_001.Position -> sample_index.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Position.001"].outputs[0],
        bi_rail_loft_1.nodes["Sample Index"].inputs[1]
    )
    # vector_math_004.Vector -> vector_math_005.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.004"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.005"].inputs[0]
    )
    # position.Position -> evaluate_at_index_001.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Position"].outputs[0],
        bi_rail_loft_1.nodes["Evaluate at Index.001"].inputs[0]
    )
    # store_named_attribute.Geometry -> set_position_002.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Store Named Attribute"].outputs[0],
        bi_rail_loft_1.nodes["Set Position.002"].inputs[0]
    )
    # menu_switch_002.Output -> grid.Vertices X
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Menu Switch.002"].outputs[0],
        bi_rail_loft_1.nodes["Grid"].inputs[2]
    )
    # duplicate_elements.Duplicate Index -> math_001.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Duplicate Elements"].outputs[1],
        bi_rail_loft_1.nodes["Math.001"].inputs[0]
    )
    # menu_switch_002.Output -> reroute_001.Input
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Menu Switch.002"].outputs[0],
        bi_rail_loft_1.nodes["Reroute.001"].inputs[0]
    )
    # duplicate_elements.Duplicate Index -> split_to_instances.Group ID
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Duplicate Elements"].outputs[1],
        bi_rail_loft_1.nodes["Split to Instances"].inputs[2]
    )
    # separate_geometry.Inverted -> duplicate_elements.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Separate Geometry"].outputs[1],
        bi_rail_loft_1.nodes["Duplicate Elements"].inputs[0]
    )
    # is_edge_boundary.Is Edge Boundary -> boolean_math.Boolean
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Is Edge Boundary"].outputs[0],
        bi_rail_loft_1.nodes["Boolean Math"].inputs[0]
    )
    # position.Position -> evaluate_at_index.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Position"].outputs[0],
        bi_rail_loft_1.nodes["Evaluate at Index"].inputs[0]
    )
    # instance_on_points.Instances -> realize_instances_001.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Instance on Points"].outputs[0],
        bi_rail_loft_1.nodes["Realize Instances.001"].inputs[0]
    )
    # align_rotation_to_vector_001.Rotation -> align_rotation_to_vector_002.Rotation
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Align Rotation to Vector.001"].outputs[0],
        bi_rail_loft_1.nodes["Align Rotation to Vector.002"].inputs[0]
    )
    # invert_rotation.Rotation -> rotate_vector.Rotation
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Invert Rotation"].outputs[0],
        bi_rail_loft_1.nodes["Rotate Vector"].inputs[1]
    )
    # boolean_math.Boolean -> blur_attribute.Weight
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Boolean Math"].outputs[0],
        bi_rail_loft_1.nodes["Blur Attribute"].inputs[2]
    )
    # index_001.Index -> separate_geometry.Selection
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Index.001"].outputs[0],
        bi_rail_loft_1.nodes["Separate Geometry"].inputs[1]
    )
    # spline_parameter_002.Factor -> sample_curve_001.Factor
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Spline Parameter.002"].outputs[0],
        bi_rail_loft_1.nodes["Sample Curve.001"].inputs[2]
    )
    # spline_parameter_001.Factor -> sample_curve.Factor
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Spline Parameter.001"].outputs[0],
        bi_rail_loft_1.nodes["Sample Curve"].inputs[2]
    )
    # evaluate_at_index_001.Value -> vector_math_001.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Evaluate at Index.001"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.001"].inputs[0]
    )
    # math_003.Value -> mix.Factor
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Math.003"].outputs[0],
        bi_rail_loft_1.nodes["Mix"].inputs[0]
    )
    # index_002.Index -> sample_index.Index
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Index.002"].outputs[0],
        bi_rail_loft_1.nodes["Sample Index"].inputs[2]
    )
    # vector_math_003.Value -> math.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.003"].outputs[1],
        bi_rail_loft_1.nodes["Math"].inputs[1]
    )
    # sample_curve.Position -> mix.A
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Sample Curve"].outputs[1],
        bi_rail_loft_1.nodes["Mix"].inputs[4]
    )
    # evaluate_at_index.Value -> vector_math.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Evaluate at Index"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math"].inputs[0]
    )
    # realize_instances_001.Geometry -> resample_curve_003.Curve
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Realize Instances.001"].outputs[0],
        bi_rail_loft_1.nodes["Resample Curve.003"].inputs[0]
    )
    # spline_length.Point Count -> integer_math_002.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Spline Length"].outputs[1],
        bi_rail_loft_1.nodes["Integer Math.002"].inputs[0]
    )
    # math_002.Value -> float_to_integer.Float
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Math.002"].outputs[0],
        bi_rail_loft_1.nodes["Float to Integer"].inputs[0]
    )
    # position_005.Position -> blur_attribute.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Position.005"].outputs[0],
        bi_rail_loft_1.nodes["Blur Attribute"].inputs[0]
    )
    # integer_math_002.Value -> integer_math_001.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Integer Math.002"].outputs[0],
        bi_rail_loft_1.nodes["Integer Math.001"].inputs[1]
    )
    # spline_parameter.Index -> integer_math.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Spline Parameter"].outputs[2],
        bi_rail_loft_1.nodes["Integer Math"].inputs[1]
    )
    # vector_math_001.Vector -> vector_math_003.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.001"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.003"].inputs[0]
    )
    # realize_instances_001.Geometry -> attribute_statistic.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Realize Instances.001"].outputs[0],
        bi_rail_loft_1.nodes["Attribute Statistic"].inputs[0]
    )
    # math_002.Value -> math_003.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Math.002"].outputs[0],
        bi_rail_loft_1.nodes["Math.003"].inputs[0]
    )
    # set_position.Geometry -> separate_geometry.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Set Position"].outputs[0],
        bi_rail_loft_1.nodes["Separate Geometry"].inputs[0]
    )
    # curve_tangent.Tangent -> vector_math_006.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Curve Tangent"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.006"].inputs[1]
    )
    # reroute_001.Output -> duplicate_elements.Amount
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Reroute.001"].outputs[0],
        bi_rail_loft_1.nodes["Duplicate Elements"].inputs[2]
    )
    # mix.Result -> set_position_001.Position
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Mix"].outputs[1],
        bi_rail_loft_1.nodes["Set Position.001"].inputs[2]
    )
    # vector_math_001.Vector -> align_rotation_to_vector.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.001"].outputs[0],
        bi_rail_loft_1.nodes["Align Rotation to Vector"].inputs[2]
    )
    # integer_math.Value -> integer_math_001.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Integer Math"].outputs[0],
        bi_rail_loft_1.nodes["Integer Math.001"].inputs[0]
    )
    # group_input.Profile Curves -> realize_instances.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input"].outputs[2],
        bi_rail_loft_1.nodes["Realize Instances"].inputs[0]
    )
    # domain_size.Spline Count -> math_002.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Domain Size"].outputs[4],
        bi_rail_loft_1.nodes["Math.002"].inputs[1]
    )
    # sample_curve_001.Position -> mix.B
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Sample Curve.001"].outputs[1],
        bi_rail_loft_1.nodes["Mix"].inputs[5]
    )
    # split_to_instances.Instances -> instance_on_points.Instance
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Split to Instances"].outputs[0],
        bi_rail_loft_1.nodes["Instance on Points"].inputs[2]
    )
    # vector_math_004.Vector -> vector_math_006.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.004"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.006"].inputs[0]
    )
    # position_001.Position -> vector_math_004.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Position.001"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.004"].inputs[1]
    )
    # group_input_001.Rail Curve -> curve_length.Curve
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.001"].outputs[0],
        bi_rail_loft_1.nodes["Curve Length"].inputs[0]
    )
    # group_input_001.Rail Curve -> curve_length_001.Curve
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.001"].outputs[1],
        bi_rail_loft_1.nodes["Curve Length.001"].inputs[0]
    )
    # curve_length.Length -> math_005.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Curve Length"].outputs[0],
        bi_rail_loft_1.nodes["Math.005"].inputs[0]
    )
    # curve_length_001.Length -> math_005.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Curve Length.001"].outputs[0],
        bi_rail_loft_1.nodes["Math.005"].inputs[1]
    )
    # math_005.Value -> math_006.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Math.005"].outputs[0],
        bi_rail_loft_1.nodes["Math.006"].inputs[0]
    )
    # group_input_001.Y Spacing -> math_006.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.001"].outputs[6],
        bi_rail_loft_1.nodes["Math.006"].inputs[1]
    )
    # set_position_005.Geometry -> group_output.Mesh
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Set Position.005"].outputs[0],
        bi_rail_loft_1.nodes["Group Output"].inputs[0]
    )
    # grid.Mesh -> store_named_attribute.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Grid"].outputs[0],
        bi_rail_loft_1.nodes["Store Named Attribute"].inputs[0]
    )
    # grid.UV Map -> separate_xyz.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Grid"].outputs[1],
        bi_rail_loft_1.nodes["Separate XYZ"].inputs[0]
    )
    # separate_xyz.X -> combine_xyz.Y
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Separate XYZ"].outputs[0],
        bi_rail_loft_1.nodes["Combine XYZ"].inputs[1]
    )
    # separate_xyz.Y -> combine_xyz.X
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Separate XYZ"].outputs[1],
        bi_rail_loft_1.nodes["Combine XYZ"].inputs[0]
    )
    # combine_xyz.Vector -> store_named_attribute.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Combine XYZ"].outputs[0],
        bi_rail_loft_1.nodes["Store Named Attribute"].inputs[3]
    )
    # group_input_002.Smoothing -> blur_attribute.Iterations
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.002"].outputs[3],
        bi_rail_loft_1.nodes["Blur Attribute"].inputs[1]
    )
    # group_input_003.Menu -> menu_switch_001.Menu
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.003"].outputs[4],
        bi_rail_loft_1.nodes["Menu Switch.001"].inputs[0]
    )
    # group_input_001.Menu -> menu_switch_002.Menu
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.001"].outputs[4],
        bi_rail_loft_1.nodes["Menu Switch.002"].inputs[0]
    )
    # math_006.Value -> menu_switch_002.Spacing
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Math.006"].outputs[0],
        bi_rail_loft_1.nodes["Menu Switch.002"].inputs[1]
    )
    # group_input_003.X Resolution -> menu_switch_001.Resolution
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.003"].outputs[7],
        bi_rail_loft_1.nodes["Menu Switch.001"].inputs[2]
    )
    # group_input_003.X Spacing -> math_004.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.003"].outputs[5],
        bi_rail_loft_1.nodes["Math.004"].inputs[1]
    )
    # math_004.Value -> menu_switch_001.Spacing
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Math.004"].outputs[0],
        bi_rail_loft_1.nodes["Menu Switch.001"].inputs[1]
    )
    # menu_switch_001.Output -> resample_curve_003.Count
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Menu Switch.001"].outputs[0],
        bi_rail_loft_1.nodes["Resample Curve.003"].inputs[3]
    )
    # menu_switch_001.Output -> grid.Vertices Y
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Menu Switch.001"].outputs[0],
        bi_rail_loft_1.nodes["Grid"].inputs[3]
    )
    # group_input_001.Y Resolution -> menu_switch_002.Resolution
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.001"].outputs[8],
        bi_rail_loft_1.nodes["Menu Switch.002"].inputs[2]
    )
    # resample_curve_001.Curve -> sample_index.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Resample Curve.001"].outputs[0],
        bi_rail_loft_1.nodes["Sample Index"].inputs[0]
    )
    # sample_index.Value -> vector_math_004.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Sample Index"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.004"].inputs[0]
    )
    # store_named_attribute_001.Geometry -> group_output.Interpolated Profiles
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Store Named Attribute.001"].outputs[0],
        bi_rail_loft_1.nodes["Group Output"].inputs[1]
    )
    # named_attribute.Attribute -> group_output.UVMap
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Named Attribute"].outputs[0],
        bi_rail_loft_1.nodes["Group Output"].inputs[2]
    )
    # resample_curve_003.Curve -> store_named_attribute_001.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Resample Curve.003"].outputs[0],
        bi_rail_loft_1.nodes["Store Named Attribute.001"].inputs[0]
    )
    # combine_xyz_001.Vector -> store_named_attribute_001.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Combine XYZ.001"].outputs[0],
        bi_rail_loft_1.nodes["Store Named Attribute.001"].inputs[3]
    )
    # spline_parameter_003.Factor -> combine_xyz_001.X
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Spline Parameter.003"].outputs[0],
        bi_rail_loft_1.nodes["Combine XYZ.001"].inputs[0]
    )
    # resample_curve.Curve -> capture_attribute.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Resample Curve"].outputs[0],
        bi_rail_loft_1.nodes["Capture Attribute"].inputs[0]
    )
    # spline_parameter_004.Factor -> capture_attribute.Factor
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Spline Parameter.004"].outputs[0],
        bi_rail_loft_1.nodes["Capture Attribute"].inputs[1]
    )
    # capture_attribute.Factor -> combine_xyz_001.Y
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Capture Attribute"].outputs[1],
        bi_rail_loft_1.nodes["Combine XYZ.001"].inputs[1]
    )
    # vector_math_006.Vector -> field_average.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.006"].outputs[0],
        bi_rail_loft_1.nodes["Field Average"].inputs[0]
    )
    # vector_math_006.Vector -> compare.A
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.006"].outputs[0],
        bi_rail_loft_1.nodes["Compare"].inputs[4]
    )
    # field_average.Mean -> compare.B
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Field Average"].outputs[0],
        bi_rail_loft_1.nodes["Compare"].inputs[5]
    )
    # compare.Result -> switch.Switch
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Compare"].outputs[0],
        bi_rail_loft_1.nodes["Switch"].inputs[0]
    )
    # vector_math_006.Vector -> vector_math_007.Vector
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Vector Math.006"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.007"].inputs[0]
    )
    # switch.Output -> vector_math_007.Scale
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Switch"].outputs[0],
        bi_rail_loft_1.nodes["Vector Math.007"].inputs[3]
    )
    # realize_instances.Geometry -> separate_components.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Realize Instances"].outputs[0],
        bi_rail_loft_1.nodes["Separate Components"].inputs[0]
    )
    # switch_001.Output -> resample_curve_002.Curve
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Switch.001"].outputs[0],
        bi_rail_loft_1.nodes["Resample Curve.002"].inputs[0]
    )
    # separate_components.Curve -> domain_size_001.Geometry
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Separate Components"].outputs[1],
        bi_rail_loft_1.nodes["Domain Size.001"].inputs[0]
    )
    # separate_components.Curve -> switch_001.False
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Separate Components"].outputs[1],
        bi_rail_loft_1.nodes["Switch.001"].inputs[1]
    )
    # curve_line.Curve -> switch_001.True
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Curve Line"].outputs[0],
        bi_rail_loft_1.nodes["Switch.001"].inputs[2]
    )
    # domain_size_001.Spline Count -> compare_001.A
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Domain Size.001"].outputs[4],
        bi_rail_loft_1.nodes["Compare.001"].inputs[2]
    )
    # compare_001.Result -> switch_001.Switch
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Compare.001"].outputs[0],
        bi_rail_loft_1.nodes["Switch.001"].inputs[0]
    )
    # math_001.Value -> evaluate_closure.Factor
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Math.001"].outputs[0],
        bi_rail_loft_1.nodes["Evaluate Closure"].inputs[1]
    )
    # group_input_004.Profile Blending Curve -> evaluate_closure.Closure
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Group Input.004"].outputs[9],
        bi_rail_loft_1.nodes["Evaluate Closure"].inputs[0]
    )
    # evaluate_closure.Factor -> math_002.Value
    bi_rail_loft_1.links.new(
        bi_rail_loft_1.nodes["Evaluate Closure"].outputs[0],
        bi_rail_loft_1.nodes["Math.002"].inputs[0]
    )
    menu_socket.default_value = 'Spacing'

    return bi_rail_loft_1


def join_splines_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Join Splines node group"""
    join_splines_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Join Splines")

    join_splines_1.color_tag = 'GEOMETRY'
    join_splines_1.description = ""
    join_splines_1.default_group_node_width = 140
    join_splines_1.show_modifier_manage_panel = True

    # join_splines_1 interface

    # Socket Curve
    curve_socket = join_splines_1.interface.new_socket(name="Curve", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    curve_socket.attribute_domain = 'POINT'
    curve_socket.default_input = 'VALUE'
    curve_socket.structure_type = 'AUTO'

    # Socket Geometry
    geometry_socket = join_splines_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.description = "Geometry to evaluate the given fields and store the resulting attributes on. All geometry types except volumes are supported"
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Initialize join_splines_1 nodes

    # Node Group Output
    group_output = join_splines_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = join_splines_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Capture Attribute.001
    capture_attribute_001 = join_splines_1.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.active_index = 0
    capture_attribute_001.capture_items.clear()
    capture_attribute_001.capture_items.new('FLOAT', "Selection")
    capture_attribute_001.capture_items["Selection"].data_type = 'BOOLEAN'
    capture_attribute_001.domain = 'POINT'

    # Node Endpoint Selection.001
    endpoint_selection_001 = join_splines_1.nodes.new("GeometryNodeCurveEndpointSelection")
    endpoint_selection_001.name = "Endpoint Selection.001"
    # Start Size
    endpoint_selection_001.inputs[0].default_value = 1
    # End Size
    endpoint_selection_001.inputs[1].default_value = 1

    # Node Curve to Points
    curve_to_points = join_splines_1.nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.mode = 'EVALUATED'

    # Node Resample Curve
    resample_curve = join_splines_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = 'Evaluated'
    # Count
    resample_curve.inputs[3].default_value = 10
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612

    # Node Merge by Distance.002
    merge_by_distance_002 = join_splines_1.nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.name = "Merge by Distance.002"
    # Mode
    merge_by_distance_002.inputs[2].default_value = 'All'
    # Distance
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513

    # Node Points to Curves
    points_to_curves = join_splines_1.nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0
    # Weight
    points_to_curves.inputs[2].default_value = 0.0

    # Set locations
    join_splines_1.nodes["Group Output"].location = (240.0, 80.0)
    join_splines_1.nodes["Group Input"].location = (-720.0, 80.0)
    join_splines_1.nodes["Capture Attribute.001"].location = (-400.0, 80.0)
    join_splines_1.nodes["Endpoint Selection.001"].location = (-400.0, -40.0)
    join_splines_1.nodes["Curve to Points"].location = (-240.0, 80.0)
    join_splines_1.nodes["Resample Curve"].location = (-560.0, 80.0)
    join_splines_1.nodes["Merge by Distance.002"].location = (-80.0, 80.0)
    join_splines_1.nodes["Points to Curves"].location = (80.0, 80.0)

    # Set dimensions
    join_splines_1.nodes["Group Output"].width  = 140.0
    join_splines_1.nodes["Group Output"].height = 100.0

    join_splines_1.nodes["Group Input"].width  = 140.0
    join_splines_1.nodes["Group Input"].height = 100.0

    join_splines_1.nodes["Capture Attribute.001"].width  = 140.0
    join_splines_1.nodes["Capture Attribute.001"].height = 100.0

    join_splines_1.nodes["Endpoint Selection.001"].width  = 140.0
    join_splines_1.nodes["Endpoint Selection.001"].height = 100.0

    join_splines_1.nodes["Curve to Points"].width  = 140.0
    join_splines_1.nodes["Curve to Points"].height = 100.0

    join_splines_1.nodes["Resample Curve"].width  = 140.0
    join_splines_1.nodes["Resample Curve"].height = 100.0

    join_splines_1.nodes["Merge by Distance.002"].width  = 140.0
    join_splines_1.nodes["Merge by Distance.002"].height = 100.0

    join_splines_1.nodes["Points to Curves"].width  = 140.0
    join_splines_1.nodes["Points to Curves"].height = 100.0


    # Initialize join_splines_1 links

    # endpoint_selection_001.Selection -> capture_attribute_001.Selection
    join_splines_1.links.new(
        join_splines_1.nodes["Endpoint Selection.001"].outputs[0],
        join_splines_1.nodes["Capture Attribute.001"].inputs[1]
    )
    # resample_curve.Curve -> capture_attribute_001.Geometry
    join_splines_1.links.new(
        join_splines_1.nodes["Resample Curve"].outputs[0],
        join_splines_1.nodes["Capture Attribute.001"].inputs[0]
    )
    # capture_attribute_001.Geometry -> curve_to_points.Curve
    join_splines_1.links.new(
        join_splines_1.nodes["Capture Attribute.001"].outputs[0],
        join_splines_1.nodes["Curve to Points"].inputs[0]
    )
    # group_input.Geometry -> resample_curve.Curve
    join_splines_1.links.new(
        join_splines_1.nodes["Group Input"].outputs[0],
        join_splines_1.nodes["Resample Curve"].inputs[0]
    )
    # curve_to_points.Points -> merge_by_distance_002.Geometry
    join_splines_1.links.new(
        join_splines_1.nodes["Curve to Points"].outputs[0],
        join_splines_1.nodes["Merge by Distance.002"].inputs[0]
    )
    # capture_attribute_001.Selection -> merge_by_distance_002.Selection
    join_splines_1.links.new(
        join_splines_1.nodes["Capture Attribute.001"].outputs[1],
        join_splines_1.nodes["Merge by Distance.002"].inputs[1]
    )
    # merge_by_distance_002.Geometry -> points_to_curves.Points
    join_splines_1.links.new(
        join_splines_1.nodes["Merge by Distance.002"].outputs[0],
        join_splines_1.nodes["Points to Curves"].inputs[0]
    )
    # points_to_curves.Curves -> group_output.Curve
    join_splines_1.links.new(
        join_splines_1.nodes["Points to Curves"].outputs[0],
        join_splines_1.nodes["Group Output"].inputs[0]
    )

    return join_splines_1


def pipes_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Pipes node group"""
    pipes_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Pipes")

    pipes_1.color_tag = 'GEOMETRY'
    pipes_1.description = ""
    pipes_1.default_group_node_width = 140
    pipes_1.show_modifier_manage_panel = True

    # pipes_1 interface

    # Socket Mesh
    mesh_socket = pipes_1.interface.new_socket(name="Mesh", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    mesh_socket.attribute_domain = 'POINT'
    mesh_socket.default_input = 'VALUE'
    mesh_socket.structure_type = 'AUTO'

    # Socket Mesh
    mesh_socket_1 = pipes_1.interface.new_socket(name="Mesh", in_out='INPUT', socket_type='NodeSocketGeometry')
    mesh_socket_1.attribute_domain = 'POINT'
    mesh_socket_1.description = "Mesh to convert to curves"
    mesh_socket_1.default_input = 'VALUE'
    mesh_socket_1.structure_type = 'AUTO'

    # Initialize pipes_1 nodes

    # Node Group Output
    group_output = pipes_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = pipes_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Mesh to Curve
    mesh_to_curve = pipes_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.mode = 'EDGES'

    # Node Group.003
    group_003 = pipes_1.nodes.new("GeometryNodeGroup")
    group_003.name = "Group.003"
    group_003.node_tree = bpy.data.node_groups[node_tree_names[is_edge_boundary_1_node_group]]

    # Node Curve to Mesh.002
    curve_to_mesh_002 = pipes_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    # Scale
    curve_to_mesh_002.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False

    # Node Curve Circle
    curve_circle = pipes_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.mode = 'RADIUS'
    # Resolution
    curve_circle.inputs[0].default_value = 10
    # Radius
    curve_circle.inputs[4].default_value = 0.0020000000949949026

    # Node Store Named Attribute
    store_named_attribute = pipes_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'BOOLEAN'
    store_named_attribute.domain = 'POINT'
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True

    # Node Edge Neighbors
    edge_neighbors = pipes_1.nodes.new("GeometryNodeInputMeshEdgeNeighbors")
    edge_neighbors.name = "Edge Neighbors"

    # Node Boolean Math
    boolean_math = pipes_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.operation = 'OR'

    # Node Compare
    compare = pipes_1.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'INT'
    compare.mode = 'ELEMENT'
    compare.operation = 'EQUAL'
    # B_INT
    compare.inputs[3].default_value = 0

    # Set locations
    pipes_1.nodes["Group Output"].location = (520.0, 60.0)
    pipes_1.nodes["Group Input"].location = (-200.0, 80.0)
    pipes_1.nodes["Mesh to Curve"].location = (40.0, 60.0)
    pipes_1.nodes["Group.003"].location = (-380.0, -140.0)
    pipes_1.nodes["Curve to Mesh.002"].location = (200.0, 60.0)
    pipes_1.nodes["Curve Circle"].location = (200.0, -80.0)
    pipes_1.nodes["Store Named Attribute"].location = (360.0, 60.0)
    pipes_1.nodes["Edge Neighbors"].location = (-380.0, -240.0)
    pipes_1.nodes["Boolean Math"].location = (-200.0, -100.0)
    pipes_1.nodes["Compare"].location = (-200.0, -240.0)

    # Set dimensions
    pipes_1.nodes["Group Output"].width  = 140.0
    pipes_1.nodes["Group Output"].height = 100.0

    pipes_1.nodes["Group Input"].width  = 140.0
    pipes_1.nodes["Group Input"].height = 100.0

    pipes_1.nodes["Mesh to Curve"].width  = 140.0
    pipes_1.nodes["Mesh to Curve"].height = 100.0

    pipes_1.nodes["Group.003"].width  = 140.0
    pipes_1.nodes["Group.003"].height = 100.0

    pipes_1.nodes["Curve to Mesh.002"].width  = 140.0
    pipes_1.nodes["Curve to Mesh.002"].height = 100.0

    pipes_1.nodes["Curve Circle"].width  = 140.0
    pipes_1.nodes["Curve Circle"].height = 100.0

    pipes_1.nodes["Store Named Attribute"].width  = 140.0
    pipes_1.nodes["Store Named Attribute"].height = 100.0

    pipes_1.nodes["Edge Neighbors"].width  = 140.0
    pipes_1.nodes["Edge Neighbors"].height = 100.0

    pipes_1.nodes["Boolean Math"].width  = 140.0
    pipes_1.nodes["Boolean Math"].height = 100.0

    pipes_1.nodes["Compare"].width  = 140.0
    pipes_1.nodes["Compare"].height = 100.0


    # Initialize pipes_1 links

    # boolean_math.Boolean -> mesh_to_curve.Selection
    pipes_1.links.new(
        pipes_1.nodes["Boolean Math"].outputs[0],
        pipes_1.nodes["Mesh to Curve"].inputs[1]
    )
    # curve_circle.Curve -> curve_to_mesh_002.Profile Curve
    pipes_1.links.new(
        pipes_1.nodes["Curve Circle"].outputs[0],
        pipes_1.nodes["Curve to Mesh.002"].inputs[1]
    )
    # mesh_to_curve.Curve -> curve_to_mesh_002.Curve
    pipes_1.links.new(
        pipes_1.nodes["Mesh to Curve"].outputs[0],
        pipes_1.nodes["Curve to Mesh.002"].inputs[0]
    )
    # group_input.Mesh -> mesh_to_curve.Mesh
    pipes_1.links.new(
        pipes_1.nodes["Group Input"].outputs[0],
        pipes_1.nodes["Mesh to Curve"].inputs[0]
    )
    # store_named_attribute.Geometry -> group_output.Mesh
    pipes_1.links.new(
        pipes_1.nodes["Store Named Attribute"].outputs[0],
        pipes_1.nodes["Group Output"].inputs[0]
    )
    # curve_to_mesh_002.Mesh -> store_named_attribute.Geometry
    pipes_1.links.new(
        pipes_1.nodes["Curve to Mesh.002"].outputs[0],
        pipes_1.nodes["Store Named Attribute"].inputs[0]
    )
    # group_003.Is Edge Boundary -> boolean_math.Boolean
    pipes_1.links.new(
        pipes_1.nodes["Group.003"].outputs[0],
        pipes_1.nodes["Boolean Math"].inputs[0]
    )
    # edge_neighbors.Face Count -> compare.A
    pipes_1.links.new(
        pipes_1.nodes["Edge Neighbors"].outputs[0],
        pipes_1.nodes["Compare"].inputs[2]
    )
    # compare.Result -> boolean_math.Boolean
    pipes_1.links.new(
        pipes_1.nodes["Compare"].outputs[0],
        pipes_1.nodes["Boolean Math"].inputs[1]
    )

    return pipes_1


def rivet_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Rivet node group"""
    rivet_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Rivet")

    rivet_1.color_tag = 'NONE'
    rivet_1.description = ""
    rivet_1.default_group_node_width = 140
    rivet_1.show_modifier_manage_panel = True

    # rivet_1 interface

    # Socket Mesh
    mesh_socket = rivet_1.interface.new_socket(name="Mesh", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    mesh_socket.attribute_domain = 'POINT'
    mesh_socket.default_input = 'VALUE'
    mesh_socket.structure_type = 'AUTO'

    # Socket Geometry
    geometry_socket = rivet_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.description = "Geometry to evaluate the given fields and store the resulting attributes on. All geometry types except volumes are supported"
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Corners
    corners_socket = rivet_1.interface.new_socket(name="Corners", in_out='INPUT', socket_type='NodeSocketBool')
    corners_socket.default_value = False
    corners_socket.attribute_domain = 'POINT'
    corners_socket.default_input = 'VALUE'
    corners_socket.structure_type = 'AUTO'

    # Socket Offset
    offset_socket = rivet_1.interface.new_socket(name="Offset", in_out='INPUT', socket_type='NodeSocketFloat')
    offset_socket.default_value = 0.9399999976158142
    offset_socket.min_value = -10000.0
    offset_socket.max_value = 10000.0
    offset_socket.subtype = 'NONE'
    offset_socket.attribute_domain = 'POINT'
    offset_socket.default_input = 'VALUE'
    offset_socket.structure_type = 'AUTO'

    # Socket Spacing
    spacing_socket = rivet_1.interface.new_socket(name="Spacing", in_out='INPUT', socket_type='NodeSocketFloat')
    spacing_socket.default_value = 0.9399999976158142
    spacing_socket.min_value = -10000.0
    spacing_socket.max_value = 10000.0
    spacing_socket.subtype = 'NONE'
    spacing_socket.attribute_domain = 'POINT'
    spacing_socket.default_input = 'VALUE'
    spacing_socket.structure_type = 'AUTO'

    # Initialize rivet_1 nodes

    # Node Group Output
    group_output = rivet_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = rivet_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Capture Attribute.005
    capture_attribute_005 = rivet_1.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_005.name = "Capture Attribute.005"
    capture_attribute_005.active_index = 0
    capture_attribute_005.capture_items.clear()
    capture_attribute_005.capture_items.new('FLOAT', "Normal")
    capture_attribute_005.capture_items["Normal"].data_type = 'FLOAT_VECTOR'
    capture_attribute_005.domain = 'POINT'

    # Node Normal
    normal = rivet_1.nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.legacy_corner_normals = False
    normal.outputs[1].hide = True

    # Node Mesh to Curve.001
    mesh_to_curve_001 = rivet_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.mode = 'EDGES'

    # Node Group.005
    group_005 = rivet_1.nodes.new("GeometryNodeGroup")
    group_005.name = "Group.005"
    group_005.node_tree = bpy.data.node_groups[node_tree_names[is_edge_boundary_1_node_group]]

    # Node Set Position
    set_position = rivet_1.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.inputs[1].hide = True
    set_position.inputs[2].hide = True
    # Selection
    set_position.inputs[1].default_value = True
    # Position
    set_position.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Vector Math.001
    vector_math_001 = rivet_1.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'NORMALIZE'

    # Node Vector Math.002
    vector_math_002 = rivet_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'SCALE'

    # Node Vector Math.007
    vector_math_007 = rivet_1.nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.operation = 'CROSS_PRODUCT'

    # Node Curve Tangent.002
    curve_tangent_002 = rivet_1.nodes.new("GeometryNodeInputTangent")
    curve_tangent_002.name = "Curve Tangent.002"

    # Node Resample Curve.001
    resample_curve_001 = rivet_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = 'Length'
    # Count
    resample_curve_001.inputs[3].default_value = 59

    # Node Instance on Points.001
    instance_on_points_001 = rivet_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.inputs[1].hide = True
    instance_on_points_001.inputs[3].hide = True
    instance_on_points_001.inputs[4].hide = True
    instance_on_points_001.inputs[5].hide = True
    instance_on_points_001.inputs[6].hide = True
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Rotation
    instance_on_points_001.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points_001.inputs[6].default_value = (1.0, 1.0, 1.0)

    # Node Ico Sphere
    ico_sphere = rivet_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.0010000000474974513
    # Subdivisions
    ico_sphere.inputs[1].default_value = 3

    # Node Vertex Neighbors
    vertex_neighbors = rivet_1.nodes.new("GeometryNodeInputMeshVertexNeighbors")
    vertex_neighbors.name = "Vertex Neighbors"

    # Node Compare.003
    compare_003 = rivet_1.nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.data_type = 'INT'
    compare_003.mode = 'ELEMENT'
    compare_003.operation = 'EQUAL'
    # B_INT
    compare_003.inputs[3].default_value = 2

    # Node Evaluate on Domain
    evaluate_on_domain = rivet_1.nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.name = "Evaluate on Domain"
    evaluate_on_domain.data_type = 'BOOLEAN'
    evaluate_on_domain.domain = 'POINT'

    # Node Boolean Math.003
    boolean_math_003 = rivet_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.hide = True
    boolean_math_003.operation = 'AND'

    # Node Curve of Point
    curve_of_point = rivet_1.nodes.new("GeometryNodeCurveOfPoint")
    curve_of_point.name = "Curve of Point"
    curve_of_point.inputs[0].hide = True
    curve_of_point.outputs[1].hide = True
    # Point Index
    curve_of_point.inputs[0].default_value = 0

    # Node Compare.004
    compare_004 = rivet_1.nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.data_type = 'INT'
    compare_004.mode = 'ELEMENT'
    compare_004.operation = 'GREATER_EQUAL'
    # B_INT
    compare_004.inputs[3].default_value = 1

    # Node Vector Math.008
    vector_math_008 = rivet_1.nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.operation = 'SCALE'

    # Node Switch.001
    switch_001 = rivet_1.nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.input_type = 'INT'
    # False
    switch_001.inputs[1].default_value = 1
    # True
    switch_001.inputs[2].default_value = -1

    # Node Math
    math = rivet_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'FLOORED_MODULO'
    math.use_clamp = False
    # Value_001
    math.inputs[1].default_value = 2.0

    # Node Math.001
    math_001 = rivet_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    # Value_001
    math_001.inputs[1].default_value = 0.009999999776482582

    # Node Switch
    switch = rivet_1.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'BOOLEAN'
    # False
    switch.inputs[1].default_value = True

    # Node Group Input.001
    group_input_001 = rivet_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"

    # Node Math.002
    math_002 = rivet_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    # Value_001
    math_002.inputs[1].default_value = 0.009999999776482582

    # Node Group Input.002
    group_input_002 = rivet_1.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[2].hide = True
    group_input_002.outputs[3].hide = True
    group_input_002.outputs[4].hide = True

    # Node Geometry Proximity
    geometry_proximity = rivet_1.nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.target_element = 'FACES'
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Source Position
    geometry_proximity.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0

    # Node Set Position.001
    set_position_001 = rivet_1.nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Realize Instances
    realize_instances = rivet_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0

    # Set locations
    rivet_1.nodes["Group Output"].location = (1539.9998779296875, 160.0)
    rivet_1.nodes["Group Input"].location = (-820.0, 240.0)
    rivet_1.nodes["Capture Attribute.005"].location = (-660.0, 240.0)
    rivet_1.nodes["Normal"].location = (-660.0, 120.0)
    rivet_1.nodes["Mesh to Curve.001"].location = (-260.0, 240.0)
    rivet_1.nodes["Group.005"].location = (-840.0, 60.0)
    rivet_1.nodes["Set Position"].location = (700.0, 320.0)
    rivet_1.nodes["Vector Math.001"].location = (340.0, 40.0)
    rivet_1.nodes["Vector Math.002"].location = (500.0, 40.0)
    rivet_1.nodes["Vector Math.007"].location = (180.0, 40.0)
    rivet_1.nodes["Curve Tangent.002"].location = (-160.0, -200.0)
    rivet_1.nodes["Resample Curve.001"].location = (520.0, 320.0)
    rivet_1.nodes["Instance on Points.001"].location = (1180.0, 380.0)
    rivet_1.nodes["Ico Sphere"].location = (1180.0, 280.0)
    rivet_1.nodes["Vertex Neighbors"].location = (-1160.0, -100.0)
    rivet_1.nodes["Compare.003"].location = (-1000.0, -100.0)
    rivet_1.nodes["Evaluate on Domain"].location = (-840.0, -100.0)
    rivet_1.nodes["Boolean Math.003"].location = (-480.0, -60.0)
    rivet_1.nodes["Curve of Point"].location = (-460.0, -340.0)
    rivet_1.nodes["Compare.004"].location = (-140.0, -340.0)
    rivet_1.nodes["Vector Math.008"].location = (20.0, -200.0)
    rivet_1.nodes["Switch.001"].location = (20.0, -340.0)
    rivet_1.nodes["Math"].location = (-300.0, -340.0)
    rivet_1.nodes["Math.001"].location = (500.0, -100.0)
    rivet_1.nodes["Switch"].location = (-660.0, -80.0)
    rivet_1.nodes["Group Input.001"].location = (260.0, -120.0)
    rivet_1.nodes["Math.002"].location = (340.0, 200.0)
    rivet_1.nodes["Group Input.002"].location = (520.0, 560.0)
    rivet_1.nodes["Geometry Proximity"].location = (740.0, 560.0)
    rivet_1.nodes["Set Position.001"].location = (1000.0, 380.0)
    rivet_1.nodes["Realize Instances"].location = (1340.0, 360.0)

    # Set dimensions
    rivet_1.nodes["Group Output"].width  = 140.0
    rivet_1.nodes["Group Output"].height = 100.0

    rivet_1.nodes["Group Input"].width  = 140.0
    rivet_1.nodes["Group Input"].height = 100.0

    rivet_1.nodes["Capture Attribute.005"].width  = 140.0
    rivet_1.nodes["Capture Attribute.005"].height = 100.0

    rivet_1.nodes["Normal"].width  = 140.0
    rivet_1.nodes["Normal"].height = 100.0

    rivet_1.nodes["Mesh to Curve.001"].width  = 140.0
    rivet_1.nodes["Mesh to Curve.001"].height = 100.0

    rivet_1.nodes["Group.005"].width  = 140.0
    rivet_1.nodes["Group.005"].height = 100.0

    rivet_1.nodes["Set Position"].width  = 140.0
    rivet_1.nodes["Set Position"].height = 100.0

    rivet_1.nodes["Vector Math.001"].width  = 140.0
    rivet_1.nodes["Vector Math.001"].height = 100.0

    rivet_1.nodes["Vector Math.002"].width  = 140.0
    rivet_1.nodes["Vector Math.002"].height = 100.0

    rivet_1.nodes["Vector Math.007"].width  = 140.0
    rivet_1.nodes["Vector Math.007"].height = 100.0

    rivet_1.nodes["Curve Tangent.002"].width  = 140.0
    rivet_1.nodes["Curve Tangent.002"].height = 100.0

    rivet_1.nodes["Resample Curve.001"].width  = 140.0
    rivet_1.nodes["Resample Curve.001"].height = 100.0

    rivet_1.nodes["Instance on Points.001"].width  = 140.0
    rivet_1.nodes["Instance on Points.001"].height = 100.0

    rivet_1.nodes["Ico Sphere"].width  = 140.0
    rivet_1.nodes["Ico Sphere"].height = 100.0

    rivet_1.nodes["Vertex Neighbors"].width  = 140.0
    rivet_1.nodes["Vertex Neighbors"].height = 100.0

    rivet_1.nodes["Compare.003"].width  = 140.0
    rivet_1.nodes["Compare.003"].height = 100.0

    rivet_1.nodes["Evaluate on Domain"].width  = 140.0
    rivet_1.nodes["Evaluate on Domain"].height = 100.0

    rivet_1.nodes["Boolean Math.003"].width  = 140.0
    rivet_1.nodes["Boolean Math.003"].height = 100.0

    rivet_1.nodes["Curve of Point"].width  = 140.0
    rivet_1.nodes["Curve of Point"].height = 100.0

    rivet_1.nodes["Compare.004"].width  = 140.0
    rivet_1.nodes["Compare.004"].height = 100.0

    rivet_1.nodes["Vector Math.008"].width  = 140.0
    rivet_1.nodes["Vector Math.008"].height = 100.0

    rivet_1.nodes["Switch.001"].width  = 140.0
    rivet_1.nodes["Switch.001"].height = 100.0

    rivet_1.nodes["Math"].width  = 140.0
    rivet_1.nodes["Math"].height = 100.0

    rivet_1.nodes["Math.001"].width  = 140.0
    rivet_1.nodes["Math.001"].height = 100.0

    rivet_1.nodes["Switch"].width  = 140.0
    rivet_1.nodes["Switch"].height = 100.0

    rivet_1.nodes["Group Input.001"].width  = 140.0
    rivet_1.nodes["Group Input.001"].height = 100.0

    rivet_1.nodes["Math.002"].width  = 140.0
    rivet_1.nodes["Math.002"].height = 100.0

    rivet_1.nodes["Group Input.002"].width  = 140.0
    rivet_1.nodes["Group Input.002"].height = 100.0

    rivet_1.nodes["Geometry Proximity"].width  = 140.0
    rivet_1.nodes["Geometry Proximity"].height = 100.0

    rivet_1.nodes["Set Position.001"].width  = 140.0
    rivet_1.nodes["Set Position.001"].height = 100.0

    rivet_1.nodes["Realize Instances"].width  = 140.0
    rivet_1.nodes["Realize Instances"].height = 100.0


    # Initialize rivet_1 links

    # curve_tangent_002.Tangent -> vector_math_008.Vector
    rivet_1.links.new(
        rivet_1.nodes["Curve Tangent.002"].outputs[0],
        rivet_1.nodes["Vector Math.008"].inputs[0]
    )
    # capture_attribute_005.Geometry -> mesh_to_curve_001.Mesh
    rivet_1.links.new(
        rivet_1.nodes["Capture Attribute.005"].outputs[0],
        rivet_1.nodes["Mesh to Curve.001"].inputs[0]
    )
    # vector_math_007.Vector -> vector_math_001.Vector
    rivet_1.links.new(
        rivet_1.nodes["Vector Math.007"].outputs[0],
        rivet_1.nodes["Vector Math.001"].inputs[0]
    )
    # vertex_neighbors.Face Count -> compare_003.A
    rivet_1.links.new(
        rivet_1.nodes["Vertex Neighbors"].outputs[1],
        rivet_1.nodes["Compare.003"].inputs[2]
    )
    # switch_001.Output -> vector_math_008.Scale
    rivet_1.links.new(
        rivet_1.nodes["Switch.001"].outputs[0],
        rivet_1.nodes["Vector Math.008"].inputs[3]
    )
    # math_001.Value -> vector_math_002.Scale
    rivet_1.links.new(
        rivet_1.nodes["Math.001"].outputs[0],
        rivet_1.nodes["Vector Math.002"].inputs[3]
    )
    # resample_curve_001.Curve -> set_position.Geometry
    rivet_1.links.new(
        rivet_1.nodes["Resample Curve.001"].outputs[0],
        rivet_1.nodes["Set Position"].inputs[0]
    )
    # vector_math_008.Vector -> vector_math_007.Vector
    rivet_1.links.new(
        rivet_1.nodes["Vector Math.008"].outputs[0],
        rivet_1.nodes["Vector Math.007"].inputs[1]
    )
    # set_position_001.Geometry -> instance_on_points_001.Points
    rivet_1.links.new(
        rivet_1.nodes["Set Position.001"].outputs[0],
        rivet_1.nodes["Instance on Points.001"].inputs[0]
    )
    # boolean_math_003.Boolean -> mesh_to_curve_001.Selection
    rivet_1.links.new(
        rivet_1.nodes["Boolean Math.003"].outputs[0],
        rivet_1.nodes["Mesh to Curve.001"].inputs[1]
    )
    # capture_attribute_005.Normal -> vector_math_007.Vector
    rivet_1.links.new(
        rivet_1.nodes["Capture Attribute.005"].outputs[1],
        rivet_1.nodes["Vector Math.007"].inputs[0]
    )
    # group_005.Is Edge Boundary -> boolean_math_003.Boolean
    rivet_1.links.new(
        rivet_1.nodes["Group.005"].outputs[0],
        rivet_1.nodes["Boolean Math.003"].inputs[0]
    )
    # ico_sphere.Mesh -> instance_on_points_001.Instance
    rivet_1.links.new(
        rivet_1.nodes["Ico Sphere"].outputs[0],
        rivet_1.nodes["Instance on Points.001"].inputs[2]
    )
    # mesh_to_curve_001.Curve -> resample_curve_001.Curve
    rivet_1.links.new(
        rivet_1.nodes["Mesh to Curve.001"].outputs[0],
        rivet_1.nodes["Resample Curve.001"].inputs[0]
    )
    # compare_003.Result -> evaluate_on_domain.Value
    rivet_1.links.new(
        rivet_1.nodes["Compare.003"].outputs[0],
        rivet_1.nodes["Evaluate on Domain"].inputs[0]
    )
    # switch.Output -> boolean_math_003.Boolean
    rivet_1.links.new(
        rivet_1.nodes["Switch"].outputs[0],
        rivet_1.nodes["Boolean Math.003"].inputs[1]
    )
    # compare_004.Result -> switch_001.Switch
    rivet_1.links.new(
        rivet_1.nodes["Compare.004"].outputs[0],
        rivet_1.nodes["Switch.001"].inputs[0]
    )
    # vector_math_002.Vector -> set_position.Offset
    rivet_1.links.new(
        rivet_1.nodes["Vector Math.002"].outputs[0],
        rivet_1.nodes["Set Position"].inputs[3]
    )
    # curve_of_point.Curve Index -> math.Value
    rivet_1.links.new(
        rivet_1.nodes["Curve of Point"].outputs[0],
        rivet_1.nodes["Math"].inputs[0]
    )
    # vector_math_001.Vector -> vector_math_002.Vector
    rivet_1.links.new(
        rivet_1.nodes["Vector Math.001"].outputs[0],
        rivet_1.nodes["Vector Math.002"].inputs[0]
    )
    # math.Value -> compare_004.A
    rivet_1.links.new(
        rivet_1.nodes["Math"].outputs[0],
        rivet_1.nodes["Compare.004"].inputs[2]
    )
    # normal.Normal -> capture_attribute_005.Normal
    rivet_1.links.new(
        rivet_1.nodes["Normal"].outputs[0],
        rivet_1.nodes["Capture Attribute.005"].inputs[1]
    )
    # group_input.Geometry -> capture_attribute_005.Geometry
    rivet_1.links.new(
        rivet_1.nodes["Group Input"].outputs[0],
        rivet_1.nodes["Capture Attribute.005"].inputs[0]
    )
    # realize_instances.Geometry -> group_output.Mesh
    rivet_1.links.new(
        rivet_1.nodes["Realize Instances"].outputs[0],
        rivet_1.nodes["Group Output"].inputs[0]
    )
    # group_input.Corners -> switch.Switch
    rivet_1.links.new(
        rivet_1.nodes["Group Input"].outputs[1],
        rivet_1.nodes["Switch"].inputs[0]
    )
    # group_input_001.Offset -> math_001.Value
    rivet_1.links.new(
        rivet_1.nodes["Group Input.001"].outputs[2],
        rivet_1.nodes["Math.001"].inputs[0]
    )
    # math_002.Value -> resample_curve_001.Length
    rivet_1.links.new(
        rivet_1.nodes["Math.002"].outputs[0],
        rivet_1.nodes["Resample Curve.001"].inputs[4]
    )
    # group_input_001.Spacing -> math_002.Value
    rivet_1.links.new(
        rivet_1.nodes["Group Input.001"].outputs[3],
        rivet_1.nodes["Math.002"].inputs[0]
    )
    # evaluate_on_domain.Value -> switch.True
    rivet_1.links.new(
        rivet_1.nodes["Evaluate on Domain"].outputs[0],
        rivet_1.nodes["Switch"].inputs[2]
    )
    # group_input_002.Geometry -> geometry_proximity.Geometry
    rivet_1.links.new(
        rivet_1.nodes["Group Input.002"].outputs[0],
        rivet_1.nodes["Geometry Proximity"].inputs[0]
    )
    # set_position.Geometry -> set_position_001.Geometry
    rivet_1.links.new(
        rivet_1.nodes["Set Position"].outputs[0],
        rivet_1.nodes["Set Position.001"].inputs[0]
    )
    # geometry_proximity.Position -> set_position_001.Position
    rivet_1.links.new(
        rivet_1.nodes["Geometry Proximity"].outputs[0],
        rivet_1.nodes["Set Position.001"].inputs[2]
    )
    # instance_on_points_001.Instances -> realize_instances.Geometry
    rivet_1.links.new(
        rivet_1.nodes["Instance on Points.001"].outputs[0],
        rivet_1.nodes["Realize Instances"].inputs[0]
    )

    return rivet_1


def gold_wavies_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Gold Wavies node group"""
    gold_wavies_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Gold Wavies")

    gold_wavies_1.color_tag = 'GEOMETRY'
    gold_wavies_1.description = ""
    gold_wavies_1.default_group_node_width = 140
    gold_wavies_1.show_modifier_manage_panel = True

    # gold_wavies_1 interface

    # Socket Instances
    instances_socket = gold_wavies_1.interface.new_socket(name="Instances", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    instances_socket.attribute_domain = 'POINT'
    instances_socket.default_input = 'VALUE'
    instances_socket.structure_type = 'AUTO'

    # Initialize gold_wavies_1 nodes

    # Node Group Output
    group_output = gold_wavies_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Curve Line
    curve_line = gold_wavies_1.nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.mode = 'POINTS'
    # Start
    curve_line.inputs[0].default_value = (0.0, 0.0, 0.0)
    # End
    curve_line.inputs[1].default_value = (0.009999999776482582, 0.0, 0.0)

    # Node Points to Vertices
    points_to_vertices = gold_wavies_1.nodes.new("GeometryNodePointsToVertices")
    points_to_vertices.name = "Points to Vertices"
    # Selection
    points_to_vertices.inputs[1].default_value = True

    # Node Curve to Points
    curve_to_points = gold_wavies_1.nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.mode = 'COUNT'
    # Count
    curve_to_points.inputs[1].default_value = 18

    # Node Extrude Mesh.001
    extrude_mesh_001 = gold_wavies_1.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.name = "Extrude Mesh.001"
    extrude_mesh_001.mode = 'VERTICES'
    # Offset Scale
    extrude_mesh_001.inputs[3].default_value = 0.0010000000474974513

    # Node Repeat Input
    repeat_input = gold_wavies_1.nodes.new("GeometryNodeRepeatInput")
    repeat_input.name = "Repeat Input"
    # Node Repeat Output
    repeat_output = gold_wavies_1.nodes.new("GeometryNodeRepeatOutput")
    repeat_output.name = "Repeat Output"
    repeat_output.active_index = 1
    repeat_output.inspection_index = 0
    repeat_output.repeat_items.clear()
    # Create item "Geometry"
    repeat_output.repeat_items.new('GEOMETRY', "Geometry")
    # Create item "Top"
    repeat_output.repeat_items.new('BOOLEAN', "Top")

    # Node Noise Texture
    noise_texture = gold_wavies_1.nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.noise_dimensions = '4D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    # Vector
    noise_texture.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Scale
    noise_texture.inputs[2].default_value = 104.69999694824219
    # Detail
    noise_texture.inputs[3].default_value = 0.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0

    # Node Map Range
    map_range = gold_wavies_1.nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.clamp = True
    map_range.data_type = 'FLOAT_VECTOR'
    map_range.interpolation_type = 'LINEAR'
    # From_Min_FLOAT3
    map_range.inputs[7].default_value = (0.0, 0.0, 0.0)
    # From_Max_FLOAT3
    map_range.inputs[8].default_value = (1.0, 1.0, 1.0)
    # To_Min_FLOAT3
    map_range.inputs[9].default_value = (-1.0, -1.0, 0.0)
    # To_Max_FLOAT3
    map_range.inputs[10].default_value = (1.0, 1.0, 0.05000000074505806)

    # Node Mesh to Curve.001
    mesh_to_curve_001 = gold_wavies_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.mode = 'EDGES'
    # Selection
    mesh_to_curve_001.inputs[1].default_value = True

    # Node Curve to Mesh.001
    curve_to_mesh_001 = gold_wavies_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False

    # Node Curve Circle
    curve_circle = gold_wavies_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.mode = 'RADIUS'
    # Resolution
    curve_circle.inputs[0].default_value = 6
    # Radius
    curve_circle.inputs[4].default_value = 0.0003000000142492354

    # Node Spline Parameter
    spline_parameter = gold_wavies_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.outputs[1].hide = True
    spline_parameter.outputs[2].hide = True

    # Node Math.004
    math_004 = gold_wavies_1.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'SUBTRACT'
    math_004.use_clamp = False
    # Value
    math_004.inputs[0].default_value = 1.0

    # Node Repeat Input.001
    repeat_input_001 = gold_wavies_1.nodes.new("GeometryNodeRepeatInput")
    repeat_input_001.name = "Repeat Input.001"
    # Node Repeat Output.001
    repeat_output_001 = gold_wavies_1.nodes.new("GeometryNodeRepeatOutput")
    repeat_output_001.name = "Repeat Output.001"
    repeat_output_001.active_index = 0
    repeat_output_001.inspection_index = 19
    repeat_output_001.repeat_items.clear()
    # Create item "Geometry"
    repeat_output_001.repeat_items.new('GEOMETRY', "Geometry")

    # Node Index Switch
    index_switch = gold_wavies_1.nodes.new("GeometryNodeIndexSwitch")
    index_switch.name = "Index Switch"
    index_switch.data_type = 'FLOAT'
    index_switch.index_switch_items.clear()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    # Item_0
    index_switch.inputs[1].default_value = 1.5700000524520874
    # Item_1
    index_switch.inputs[2].default_value = 0.3499999940395355
    # Item_2
    index_switch.inputs[3].default_value = 1.0099999904632568
    # Item_3
    index_switch.inputs[4].default_value = 1.2999999523162842
    # Item_4
    index_switch.inputs[5].default_value = 1.2999999523162842
    # Item_5
    index_switch.inputs[6].default_value = 2.569999933242798
    # Item_6
    index_switch.inputs[7].default_value = 3.6499998569488525
    # Item_7
    index_switch.inputs[8].default_value = 4.029999732971191
    # Item_8
    index_switch.inputs[9].default_value = 4.599999904632568
    # Item_9
    index_switch.inputs[10].default_value = 6.239999771118164
    # Item_10
    index_switch.inputs[11].default_value = 10.100000381469727
    # Item_11
    index_switch.inputs[12].default_value = 10.270000457763672
    # Item_12
    index_switch.inputs[13].default_value = 10.369999885559082
    # Item_13
    index_switch.inputs[14].default_value = 10.670000076293945
    # Item_14
    index_switch.inputs[15].default_value = 10.720000267028809
    # Item_15
    index_switch.inputs[16].default_value = 10.890000343322754
    # Item_16
    index_switch.inputs[17].default_value = 11.130000114440918
    # Item_17
    index_switch.inputs[18].default_value = 11.289999961853027
    # Item_18
    index_switch.inputs[19].default_value = 11.390000343322754
    # Item_19
    index_switch.inputs[20].default_value = 11.800000190734863

    # Node Geometry to Instance
    geometry_to_instance = gold_wavies_1.nodes.new("GeometryNodeGeometryToInstance")
    geometry_to_instance.name = "Geometry to Instance"

    # Node Join Geometry.006
    join_geometry_006 = gold_wavies_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"

    # Node Resample Curve
    resample_curve = gold_wavies_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = 'Count'
    # Count
    resample_curve.inputs[3].default_value = 30
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612

    # Process zone input Repeat Input
    repeat_input.pair_with_output(repeat_output)
    # Iterations
    repeat_input.inputs[0].default_value = 50
    # Item_1
    repeat_input.inputs[2].default_value = True


    # Process zone input Repeat Input.001
    repeat_input_001.pair_with_output(repeat_output_001)
    # Iterations
    repeat_input_001.inputs[0].default_value = 20



    # Set locations
    gold_wavies_1.nodes["Group Output"].location = (1500.0, 300.0)
    gold_wavies_1.nodes["Curve Line"].location = (-620.0, 220.0)
    gold_wavies_1.nodes["Points to Vertices"].location = (-300.0, 220.0)
    gold_wavies_1.nodes["Curve to Points"].location = (-460.0, 220.0)
    gold_wavies_1.nodes["Extrude Mesh.001"].location = (100.0, 220.0)
    gold_wavies_1.nodes["Repeat Input"].location = (-120.0, 220.0)
    gold_wavies_1.nodes["Repeat Output"].location = (260.0, 220.0)
    gold_wavies_1.nodes["Noise Texture"].location = (-300.0, 60.0)
    gold_wavies_1.nodes["Map Range"].location = (-120.0, 60.0)
    gold_wavies_1.nodes["Mesh to Curve.001"].location = (420.0, 220.0)
    gold_wavies_1.nodes["Curve to Mesh.001"].location = (780.0, 200.0)
    gold_wavies_1.nodes["Curve Circle"].location = (780.0, 60.0)
    gold_wavies_1.nodes["Spline Parameter"].location = (420.0, -40.0)
    gold_wavies_1.nodes["Math.004"].location = (420.0, 100.0)
    gold_wavies_1.nodes["Repeat Input.001"].location = (-1080.0, 360.0)
    gold_wavies_1.nodes["Repeat Output.001"].location = (1320.0, 300.0)
    gold_wavies_1.nodes["Index Switch"].location = (-900.0, 360.0)
    gold_wavies_1.nodes["Geometry to Instance"].location = (940.0, 200.0)
    gold_wavies_1.nodes["Join Geometry.006"].location = (1140.0, 300.0)
    gold_wavies_1.nodes["Resample Curve"].location = (600.0, 200.0)

    # Set dimensions
    gold_wavies_1.nodes["Group Output"].width  = 140.0
    gold_wavies_1.nodes["Group Output"].height = 100.0

    gold_wavies_1.nodes["Curve Line"].width  = 140.0
    gold_wavies_1.nodes["Curve Line"].height = 100.0

    gold_wavies_1.nodes["Points to Vertices"].width  = 140.0
    gold_wavies_1.nodes["Points to Vertices"].height = 100.0

    gold_wavies_1.nodes["Curve to Points"].width  = 140.0
    gold_wavies_1.nodes["Curve to Points"].height = 100.0

    gold_wavies_1.nodes["Extrude Mesh.001"].width  = 140.0
    gold_wavies_1.nodes["Extrude Mesh.001"].height = 100.0

    gold_wavies_1.nodes["Repeat Input"].width  = 140.0
    gold_wavies_1.nodes["Repeat Input"].height = 100.0

    gold_wavies_1.nodes["Repeat Output"].width  = 140.0
    gold_wavies_1.nodes["Repeat Output"].height = 100.0

    gold_wavies_1.nodes["Noise Texture"].width  = 145.0
    gold_wavies_1.nodes["Noise Texture"].height = 100.0

    gold_wavies_1.nodes["Map Range"].width  = 140.0
    gold_wavies_1.nodes["Map Range"].height = 100.0

    gold_wavies_1.nodes["Mesh to Curve.001"].width  = 140.0
    gold_wavies_1.nodes["Mesh to Curve.001"].height = 100.0

    gold_wavies_1.nodes["Curve to Mesh.001"].width  = 140.0
    gold_wavies_1.nodes["Curve to Mesh.001"].height = 100.0

    gold_wavies_1.nodes["Curve Circle"].width  = 140.0
    gold_wavies_1.nodes["Curve Circle"].height = 100.0

    gold_wavies_1.nodes["Spline Parameter"].width  = 140.0
    gold_wavies_1.nodes["Spline Parameter"].height = 100.0

    gold_wavies_1.nodes["Math.004"].width  = 140.0
    gold_wavies_1.nodes["Math.004"].height = 100.0

    gold_wavies_1.nodes["Repeat Input.001"].width  = 140.0
    gold_wavies_1.nodes["Repeat Input.001"].height = 100.0

    gold_wavies_1.nodes["Repeat Output.001"].width  = 140.0
    gold_wavies_1.nodes["Repeat Output.001"].height = 100.0

    gold_wavies_1.nodes["Index Switch"].width  = 140.0
    gold_wavies_1.nodes["Index Switch"].height = 100.0

    gold_wavies_1.nodes["Geometry to Instance"].width  = 160.0
    gold_wavies_1.nodes["Geometry to Instance"].height = 100.0

    gold_wavies_1.nodes["Join Geometry.006"].width  = 140.0
    gold_wavies_1.nodes["Join Geometry.006"].height = 100.0

    gold_wavies_1.nodes["Resample Curve"].width  = 140.0
    gold_wavies_1.nodes["Resample Curve"].height = 100.0


    # Initialize gold_wavies_1 links

    # join_geometry_006.Geometry -> repeat_output_001.Geometry
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Join Geometry.006"].outputs[0],
        gold_wavies_1.nodes["Repeat Output.001"].inputs[0]
    )
    # curve_to_points.Points -> points_to_vertices.Points
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Curve to Points"].outputs[0],
        gold_wavies_1.nodes["Points to Vertices"].inputs[0]
    )
    # repeat_input_001.Iteration -> index_switch.Index
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Repeat Input.001"].outputs[0],
        gold_wavies_1.nodes["Index Switch"].inputs[0]
    )
    # resample_curve.Curve -> curve_to_mesh_001.Curve
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Resample Curve"].outputs[0],
        gold_wavies_1.nodes["Curve to Mesh.001"].inputs[0]
    )
    # curve_circle.Curve -> curve_to_mesh_001.Profile Curve
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Curve Circle"].outputs[0],
        gold_wavies_1.nodes["Curve to Mesh.001"].inputs[1]
    )
    # points_to_vertices.Mesh -> repeat_input.Geometry
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Points to Vertices"].outputs[0],
        gold_wavies_1.nodes["Repeat Input"].inputs[1]
    )
    # curve_line.Curve -> curve_to_points.Curve
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Curve Line"].outputs[0],
        gold_wavies_1.nodes["Curve to Points"].inputs[0]
    )
    # geometry_to_instance.Instances -> join_geometry_006.Geometry
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Geometry to Instance"].outputs[0],
        gold_wavies_1.nodes["Join Geometry.006"].inputs[0]
    )
    # extrude_mesh_001.Top -> repeat_output.Top
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Extrude Mesh.001"].outputs[1],
        gold_wavies_1.nodes["Repeat Output"].inputs[1]
    )
    # extrude_mesh_001.Mesh -> repeat_output.Geometry
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Extrude Mesh.001"].outputs[0],
        gold_wavies_1.nodes["Repeat Output"].inputs[0]
    )
    # map_range.Vector -> extrude_mesh_001.Offset
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Map Range"].outputs[1],
        gold_wavies_1.nodes["Extrude Mesh.001"].inputs[2]
    )
    # spline_parameter.Factor -> math_004.Value
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Spline Parameter"].outputs[0],
        gold_wavies_1.nodes["Math.004"].inputs[1]
    )
    # repeat_output.Geometry -> mesh_to_curve_001.Mesh
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Repeat Output"].outputs[0],
        gold_wavies_1.nodes["Mesh to Curve.001"].inputs[0]
    )
    # curve_to_mesh_001.Mesh -> geometry_to_instance.Geometry
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Curve to Mesh.001"].outputs[0],
        gold_wavies_1.nodes["Geometry to Instance"].inputs[0]
    )
    # noise_texture.Color -> map_range.Vector
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Noise Texture"].outputs[1],
        gold_wavies_1.nodes["Map Range"].inputs[6]
    )
    # repeat_input.Top -> extrude_mesh_001.Selection
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Repeat Input"].outputs[2],
        gold_wavies_1.nodes["Extrude Mesh.001"].inputs[1]
    )
    # math_004.Value -> curve_to_mesh_001.Scale
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Math.004"].outputs[0],
        gold_wavies_1.nodes["Curve to Mesh.001"].inputs[2]
    )
    # index_switch.Output -> noise_texture.W
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Index Switch"].outputs[0],
        gold_wavies_1.nodes["Noise Texture"].inputs[1]
    )
    # repeat_input.Geometry -> extrude_mesh_001.Mesh
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Repeat Input"].outputs[1],
        gold_wavies_1.nodes["Extrude Mesh.001"].inputs[0]
    )
    # repeat_output_001.Geometry -> group_output.Instances
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Repeat Output.001"].outputs[0],
        gold_wavies_1.nodes["Group Output"].inputs[0]
    )
    # mesh_to_curve_001.Curve -> resample_curve.Curve
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Mesh to Curve.001"].outputs[0],
        gold_wavies_1.nodes["Resample Curve"].inputs[0]
    )
    # repeat_input_001.Geometry -> join_geometry_006.Geometry
    gold_wavies_1.links.new(
        gold_wavies_1.nodes["Repeat Input.001"].outputs[1],
        gold_wavies_1.nodes["Join Geometry.006"].inputs[0]
    )

    return gold_wavies_1


def gold_decorations_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Gold Decorations node group"""
    gold_decorations_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Gold Decorations")

    gold_decorations_1.color_tag = 'GEOMETRY'
    gold_decorations_1.description = ""
    gold_decorations_1.default_group_node_width = 140
    gold_decorations_1.show_modifier_manage_panel = True

    # gold_decorations_1 interface

    # Socket Geometry
    geometry_socket = gold_decorations_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Curves
    curves_socket = gold_decorations_1.interface.new_socket(name="Curves", in_out='INPUT', socket_type='NodeSocketGeometry')
    curves_socket.attribute_domain = 'POINT'
    curves_socket.description = "Curves to sample positions on"
    curves_socket.default_input = 'VALUE'
    curves_socket.structure_type = 'AUTO'

    # Socket Seed
    seed_socket = gold_decorations_1.interface.new_socket(name="Seed", in_out='INPUT', socket_type='NodeSocketInt')
    seed_socket.default_value = 30
    seed_socket.min_value = -10000
    seed_socket.max_value = 10000
    seed_socket.subtype = 'NONE'
    seed_socket.attribute_domain = 'POINT'
    seed_socket.default_input = 'VALUE'
    seed_socket.structure_type = 'AUTO'

    # Socket Scale
    scale_socket = gold_decorations_1.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat')
    scale_socket.default_value = 4.049999713897705
    scale_socket.min_value = -10000.0
    scale_socket.max_value = 10000.0
    scale_socket.subtype = 'NONE'
    scale_socket.attribute_domain = 'POINT'
    scale_socket.default_input = 'VALUE'
    scale_socket.structure_type = 'AUTO'

    # Socket Count
    count_socket = gold_decorations_1.interface.new_socket(name="Count", in_out='INPUT', socket_type='NodeSocketInt')
    count_socket.default_value = 18
    count_socket.min_value = 1
    count_socket.max_value = 10000
    count_socket.subtype = 'NONE'
    count_socket.attribute_domain = 'POINT'
    count_socket.description = "Number of vertices on the line"
    count_socket.default_input = 'VALUE'
    count_socket.structure_type = 'AUTO'

    # Initialize gold_decorations_1 nodes

    # Node Group Output
    group_output = gold_decorations_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = gold_decorations_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[1].hide = True
    group_input.outputs[3].hide = True
    group_input.outputs[4].hide = True

    # Node Mesh Line
    mesh_line = gold_decorations_1.nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.count_mode = 'TOTAL'
    mesh_line.mode = 'OFFSET'
    # Start Location
    mesh_line.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset
    mesh_line.inputs[3].default_value = (0.004999999888241291, 0.0, 0.0)

    # Node Instance on Points
    instance_on_points = gold_decorations_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = True
    # Rotation
    instance_on_points.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points.inputs[6].default_value = (1.0, 1.0, 1.0)

    # Node Random Value
    random_value = gold_decorations_1.nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.data_type = 'INT'
    # Min_002
    random_value.inputs[4].default_value = 0
    # ID
    random_value.inputs[7].default_value = 0

    # Node Scale Instances.001
    scale_instances_001 = gold_decorations_1.nodes.new("GeometryNodeScaleInstances")
    scale_instances_001.name = "Scale Instances.001"
    # Selection
    scale_instances_001.inputs[1].default_value = True
    # Scale
    scale_instances_001.inputs[2].default_value = (1.0, -1.0, 1.0)
    # Center
    scale_instances_001.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Local Space
    scale_instances_001.inputs[4].default_value = True

    # Node Join Geometry.008
    join_geometry_008 = gold_decorations_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_008.name = "Join Geometry.008"

    # Node Realize Instances
    realize_instances = gold_decorations_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0

    # Node Flip Faces.003
    flip_faces_003 = gold_decorations_1.nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.name = "Flip Faces.003"
    # Selection
    flip_faces_003.inputs[1].default_value = True

    # Node Bounding Box
    bounding_box = gold_decorations_1.nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = True

    # Node Sample Curve
    sample_curve = gold_decorations_1.nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.data_type = 'FLOAT'
    sample_curve.mode = 'FACTOR'
    sample_curve.use_all_curves = True
    # Value
    sample_curve.inputs[1].default_value = 0.0

    # Node Position.002
    position_002 = gold_decorations_1.nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"

    # Node Map Range.001
    map_range_001 = gold_decorations_1.nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.clamp = True
    map_range_001.data_type = 'FLOAT_VECTOR'
    map_range_001.interpolation_type = 'LINEAR'
    # To_Min_FLOAT3
    map_range_001.inputs[9].default_value = (0.0, 0.0, 0.0)
    # To_Max_FLOAT3
    map_range_001.inputs[10].default_value = (1.0, 1.0, 1.0)

    # Node Separate XYZ.003
    separate_xyz_003 = gold_decorations_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_003.name = "Separate XYZ.003"
    separate_xyz_003.outputs[1].hide = True
    separate_xyz_003.outputs[2].hide = True

    # Node Set Position.001
    set_position_001 = gold_decorations_1.nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Vector Math.003
    vector_math_003 = gold_decorations_1.nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.operation = 'ADD'

    # Node Vector Math
    vector_math = gold_decorations_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'SCALE'

    # Node Separate XYZ.004
    separate_xyz_004 = gold_decorations_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_004.name = "Separate XYZ.004"
    separate_xyz_004.outputs[0].hide = True

    # Node Vector Math.001
    vector_math_001 = gold_decorations_1.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'CROSS_PRODUCT'

    # Node Vector Math.002
    vector_math_002 = gold_decorations_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'SCALE'

    # Node Vector Math.004
    vector_math_004 = gold_decorations_1.nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.operation = 'ADD'

    # Node Vector Math.005
    vector_math_005 = gold_decorations_1.nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.operation = 'SCALE'

    # Node Group.002
    group_002 = gold_decorations_1.nodes.new("GeometryNodeGroup")
    group_002.name = "Group.002"
    group_002.node_tree = bpy.data.node_groups[node_tree_names[gold_wavies_1_node_group]]

    # Node Domain Size
    domain_size = gold_decorations_1.nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.component = 'INSTANCES'

    # Node Group Input.001
    group_input_001 = gold_decorations_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[0].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[4].hide = True

    # Node Store Named Attribute
    store_named_attribute = gold_decorations_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'BOOLEAN'
    store_named_attribute.domain = 'POINT'
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True

    # Set locations
    gold_decorations_1.nodes["Group Output"].location = (2080.0, 200.0)
    gold_decorations_1.nodes["Group Input"].location = (280.0, -340.0)
    gold_decorations_1.nodes["Mesh Line"].location = (-1140.0, 220.0)
    gold_decorations_1.nodes["Instance on Points"].location = (-960.0, 220.0)
    gold_decorations_1.nodes["Random Value"].location = (-960.0, -100.0)
    gold_decorations_1.nodes["Scale Instances.001"].location = (-780.0, 160.0)
    gold_decorations_1.nodes["Join Geometry.008"].location = (-440.0, 220.0)
    gold_decorations_1.nodes["Realize Instances"].location = (-260.0, 220.0)
    gold_decorations_1.nodes["Flip Faces.003"].location = (-620.0, 160.0)
    gold_decorations_1.nodes["Bounding Box"].location = (-80.0, -80.0)
    gold_decorations_1.nodes["Sample Curve"].location = (480.0, -80.0)
    gold_decorations_1.nodes["Position.002"].location = (-80.0, -20.0)
    gold_decorations_1.nodes["Map Range.001"].location = (100.0, -20.0)
    gold_decorations_1.nodes["Separate XYZ.003"].location = (280.0, -20.0)
    gold_decorations_1.nodes["Set Position.001"].location = (1280.0, 220.0)
    gold_decorations_1.nodes["Vector Math.003"].location = (900.0, 40.0)
    gold_decorations_1.nodes["Vector Math"].location = (720.0, -160.0)
    gold_decorations_1.nodes["Separate XYZ.004"].location = (720.0, -440.0)
    gold_decorations_1.nodes["Vector Math.001"].location = (720.0, -300.0)
    gold_decorations_1.nodes["Vector Math.002"].location = (880.0, -300.0)
    gold_decorations_1.nodes["Vector Math.004"].location = (1080.0, 40.0)
    gold_decorations_1.nodes["Vector Math.005"].location = (500.0, -380.0)
    gold_decorations_1.nodes["Group.002"].location = (-1320.0, 20.0)
    gold_decorations_1.nodes["Domain Size"].location = (-1320.0, -40.0)
    gold_decorations_1.nodes["Group Input.001"].location = (-1160.0, -200.0)
    gold_decorations_1.nodes["Store Named Attribute"].location = (1500.0, 220.0)

    # Set dimensions
    gold_decorations_1.nodes["Group Output"].width  = 140.0
    gold_decorations_1.nodes["Group Output"].height = 100.0

    gold_decorations_1.nodes["Group Input"].width  = 140.0
    gold_decorations_1.nodes["Group Input"].height = 100.0

    gold_decorations_1.nodes["Mesh Line"].width  = 140.0
    gold_decorations_1.nodes["Mesh Line"].height = 100.0

    gold_decorations_1.nodes["Instance on Points"].width  = 140.0
    gold_decorations_1.nodes["Instance on Points"].height = 100.0

    gold_decorations_1.nodes["Random Value"].width  = 140.0
    gold_decorations_1.nodes["Random Value"].height = 100.0

    gold_decorations_1.nodes["Scale Instances.001"].width  = 140.0
    gold_decorations_1.nodes["Scale Instances.001"].height = 100.0

    gold_decorations_1.nodes["Join Geometry.008"].width  = 140.0
    gold_decorations_1.nodes["Join Geometry.008"].height = 100.0

    gold_decorations_1.nodes["Realize Instances"].width  = 140.0
    gold_decorations_1.nodes["Realize Instances"].height = 100.0

    gold_decorations_1.nodes["Flip Faces.003"].width  = 140.0
    gold_decorations_1.nodes["Flip Faces.003"].height = 100.0

    gold_decorations_1.nodes["Bounding Box"].width  = 140.0
    gold_decorations_1.nodes["Bounding Box"].height = 100.0

    gold_decorations_1.nodes["Sample Curve"].width  = 140.0
    gold_decorations_1.nodes["Sample Curve"].height = 100.0

    gold_decorations_1.nodes["Position.002"].width  = 140.0
    gold_decorations_1.nodes["Position.002"].height = 100.0

    gold_decorations_1.nodes["Map Range.001"].width  = 140.0
    gold_decorations_1.nodes["Map Range.001"].height = 100.0

    gold_decorations_1.nodes["Separate XYZ.003"].width  = 140.0
    gold_decorations_1.nodes["Separate XYZ.003"].height = 100.0

    gold_decorations_1.nodes["Set Position.001"].width  = 140.0
    gold_decorations_1.nodes["Set Position.001"].height = 100.0

    gold_decorations_1.nodes["Vector Math.003"].width  = 140.0
    gold_decorations_1.nodes["Vector Math.003"].height = 100.0

    gold_decorations_1.nodes["Vector Math"].width  = 140.0
    gold_decorations_1.nodes["Vector Math"].height = 100.0

    gold_decorations_1.nodes["Separate XYZ.004"].width  = 140.0
    gold_decorations_1.nodes["Separate XYZ.004"].height = 100.0

    gold_decorations_1.nodes["Vector Math.001"].width  = 140.0
    gold_decorations_1.nodes["Vector Math.001"].height = 100.0

    gold_decorations_1.nodes["Vector Math.002"].width  = 140.0
    gold_decorations_1.nodes["Vector Math.002"].height = 100.0

    gold_decorations_1.nodes["Vector Math.004"].width  = 140.0
    gold_decorations_1.nodes["Vector Math.004"].height = 100.0

    gold_decorations_1.nodes["Vector Math.005"].width  = 140.0
    gold_decorations_1.nodes["Vector Math.005"].height = 100.0

    gold_decorations_1.nodes["Group.002"].width  = 140.0
    gold_decorations_1.nodes["Group.002"].height = 100.0

    gold_decorations_1.nodes["Domain Size"].width  = 140.0
    gold_decorations_1.nodes["Domain Size"].height = 100.0

    gold_decorations_1.nodes["Group Input.001"].width  = 140.0
    gold_decorations_1.nodes["Group Input.001"].height = 100.0

    gold_decorations_1.nodes["Store Named Attribute"].width  = 140.0
    gold_decorations_1.nodes["Store Named Attribute"].height = 100.0


    # Initialize gold_decorations_1 links

    # random_value.Value -> instance_on_points.Instance Index
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Random Value"].outputs[2],
        gold_decorations_1.nodes["Instance on Points"].inputs[4]
    )
    # vector_math_003.Vector -> vector_math_004.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Vector Math.003"].outputs[0],
        gold_decorations_1.nodes["Vector Math.004"].inputs[0]
    )
    # join_geometry_008.Geometry -> realize_instances.Geometry
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Join Geometry.008"].outputs[0],
        gold_decorations_1.nodes["Realize Instances"].inputs[0]
    )
    # vector_math_004.Vector -> set_position_001.Position
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Vector Math.004"].outputs[0],
        gold_decorations_1.nodes["Set Position.001"].inputs[2]
    )
    # position_002.Position -> map_range_001.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Position.002"].outputs[0],
        gold_decorations_1.nodes["Map Range.001"].inputs[6]
    )
    # mesh_line.Mesh -> instance_on_points.Points
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Mesh Line"].outputs[0],
        gold_decorations_1.nodes["Instance on Points"].inputs[0]
    )
    # vector_math_001.Vector -> vector_math_002.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Vector Math.001"].outputs[0],
        gold_decorations_1.nodes["Vector Math.002"].inputs[0]
    )
    # group_002.Instances -> instance_on_points.Instance
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Group.002"].outputs[0],
        gold_decorations_1.nodes["Instance on Points"].inputs[2]
    )
    # realize_instances.Geometry -> set_position_001.Geometry
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Realize Instances"].outputs[0],
        gold_decorations_1.nodes["Set Position.001"].inputs[0]
    )
    # bounding_box.Min -> map_range_001.From Min
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Bounding Box"].outputs[1],
        gold_decorations_1.nodes["Map Range.001"].inputs[7]
    )
    # map_range_001.Vector -> separate_xyz_003.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Map Range.001"].outputs[1],
        gold_decorations_1.nodes["Separate XYZ.003"].inputs[0]
    )
    # vector_math.Vector -> vector_math_003.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Vector Math"].outputs[0],
        gold_decorations_1.nodes["Vector Math.003"].inputs[1]
    )
    # group_002.Instances -> domain_size.Geometry
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Group.002"].outputs[0],
        gold_decorations_1.nodes["Domain Size"].inputs[0]
    )
    # sample_curve.Normal -> vector_math.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Sample Curve"].outputs[3],
        gold_decorations_1.nodes["Vector Math"].inputs[0]
    )
    # vector_math_005.Vector -> separate_xyz_004.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Vector Math.005"].outputs[0],
        gold_decorations_1.nodes["Separate XYZ.004"].inputs[0]
    )
    # sample_curve.Position -> vector_math_003.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Sample Curve"].outputs[1],
        gold_decorations_1.nodes["Vector Math.003"].inputs[0]
    )
    # separate_xyz_003.X -> sample_curve.Factor
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Separate XYZ.003"].outputs[0],
        gold_decorations_1.nodes["Sample Curve"].inputs[2]
    )
    # vector_math_002.Vector -> vector_math_004.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Vector Math.002"].outputs[0],
        gold_decorations_1.nodes["Vector Math.004"].inputs[1]
    )
    # scale_instances_001.Instances -> flip_faces_003.Mesh
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Scale Instances.001"].outputs[0],
        gold_decorations_1.nodes["Flip Faces.003"].inputs[0]
    )
    # sample_curve.Normal -> vector_math_001.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Sample Curve"].outputs[3],
        gold_decorations_1.nodes["Vector Math.001"].inputs[1]
    )
    # instance_on_points.Instances -> join_geometry_008.Geometry
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Instance on Points"].outputs[0],
        gold_decorations_1.nodes["Join Geometry.008"].inputs[0]
    )
    # separate_xyz_004.Y -> vector_math.Scale
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Separate XYZ.004"].outputs[1],
        gold_decorations_1.nodes["Vector Math"].inputs[3]
    )
    # separate_xyz_004.Z -> vector_math_002.Scale
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Separate XYZ.004"].outputs[2],
        gold_decorations_1.nodes["Vector Math.002"].inputs[3]
    )
    # realize_instances.Geometry -> bounding_box.Geometry
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Realize Instances"].outputs[0],
        gold_decorations_1.nodes["Bounding Box"].inputs[0]
    )
    # bounding_box.Max -> map_range_001.From Max
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Bounding Box"].outputs[2],
        gold_decorations_1.nodes["Map Range.001"].inputs[8]
    )
    # sample_curve.Tangent -> vector_math_001.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Sample Curve"].outputs[2],
        gold_decorations_1.nodes["Vector Math.001"].inputs[0]
    )
    # position_002.Position -> vector_math_005.Vector
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Position.002"].outputs[0],
        gold_decorations_1.nodes["Vector Math.005"].inputs[0]
    )
    # instance_on_points.Instances -> scale_instances_001.Instances
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Instance on Points"].outputs[0],
        gold_decorations_1.nodes["Scale Instances.001"].inputs[0]
    )
    # domain_size.Instance Count -> random_value.Max
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Domain Size"].outputs[5],
        gold_decorations_1.nodes["Random Value"].inputs[5]
    )
    # group_input.Curves -> sample_curve.Curves
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Group Input"].outputs[0],
        gold_decorations_1.nodes["Sample Curve"].inputs[0]
    )
    # store_named_attribute.Geometry -> group_output.Geometry
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Store Named Attribute"].outputs[0],
        gold_decorations_1.nodes["Group Output"].inputs[0]
    )
    # group_input_001.Seed -> random_value.Seed
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Group Input.001"].outputs[1],
        gold_decorations_1.nodes["Random Value"].inputs[8]
    )
    # group_input.Scale -> vector_math_005.Scale
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Group Input"].outputs[2],
        gold_decorations_1.nodes["Vector Math.005"].inputs[3]
    )
    # group_input_001.Count -> mesh_line.Count
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Group Input.001"].outputs[3],
        gold_decorations_1.nodes["Mesh Line"].inputs[0]
    )
    # set_position_001.Geometry -> store_named_attribute.Geometry
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Set Position.001"].outputs[0],
        gold_decorations_1.nodes["Store Named Attribute"].inputs[0]
    )
    # flip_faces_003.Mesh -> join_geometry_008.Geometry
    gold_decorations_1.links.new(
        gold_decorations_1.nodes["Flip Faces.003"].outputs[0],
        gold_decorations_1.nodes["Join Geometry.008"].inputs[0]
    )

    return gold_decorations_1


def gold_on_band_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Gold on Band node group"""
    gold_on_band_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Gold on Band")

    gold_on_band_1.color_tag = 'GEOMETRY'
    gold_on_band_1.description = ""
    gold_on_band_1.default_group_node_width = 140
    gold_on_band_1.show_modifier_manage_panel = True

    # gold_on_band_1 interface

    # Socket Mesh
    mesh_socket = gold_on_band_1.interface.new_socket(name="Mesh", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    mesh_socket.attribute_domain = 'POINT'
    mesh_socket.default_input = 'VALUE'
    mesh_socket.structure_type = 'AUTO'

    # Socket Mesh
    mesh_socket_1 = gold_on_band_1.interface.new_socket(name="Mesh", in_out='INPUT', socket_type='NodeSocketGeometry')
    mesh_socket_1.attribute_domain = 'POINT'
    mesh_socket_1.description = "Mesh on whose faces to distribute points on"
    mesh_socket_1.default_input = 'VALUE'
    mesh_socket_1.structure_type = 'AUTO'

    # Socket Density
    density_socket = gold_on_band_1.interface.new_socket(name="Density", in_out='INPUT', socket_type='NodeSocketFloat')
    density_socket.default_value = 1000.0
    density_socket.min_value = 0.0
    density_socket.max_value = 3.4028234663852886e+38
    density_socket.subtype = 'NONE'
    density_socket.attribute_domain = 'POINT'
    density_socket.default_input = 'VALUE'
    density_socket.structure_type = 'AUTO'

    # Socket W
    w_socket = gold_on_band_1.interface.new_socket(name="W", in_out='INPUT', socket_type='NodeSocketFloat')
    w_socket.default_value = 1.5699999332427979
    w_socket.min_value = -1000.0
    w_socket.max_value = 1000.0
    w_socket.subtype = 'NONE'
    w_socket.attribute_domain = 'POINT'
    w_socket.default_input = 'VALUE'
    w_socket.structure_type = 'AUTO'

    # Socket Seed
    seed_socket = gold_on_band_1.interface.new_socket(name="Seed", in_out='INPUT', socket_type='NodeSocketInt')
    seed_socket.default_value = 0
    seed_socket.min_value = -2147483648
    seed_socket.max_value = 2147483647
    seed_socket.subtype = 'NONE'
    seed_socket.attribute_domain = 'POINT'
    seed_socket.default_input = 'VALUE'
    seed_socket.structure_type = 'AUTO'

    # Initialize gold_on_band_1 nodes

    # Node Group Output
    group_output = gold_on_band_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = gold_on_band_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Distribute Points on Faces
    distribute_points_on_faces = gold_on_band_1.nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.name = "Distribute Points on Faces"
    distribute_points_on_faces.distribute_method = 'RANDOM'
    distribute_points_on_faces.use_legacy_normal = False
    # Selection
    distribute_points_on_faces.inputs[1].default_value = True

    # Node Points to Vertices
    points_to_vertices = gold_on_band_1.nodes.new("GeometryNodePointsToVertices")
    points_to_vertices.name = "Points to Vertices"
    # Selection
    points_to_vertices.inputs[1].default_value = True

    # Node Extrude Mesh.001
    extrude_mesh_001 = gold_on_band_1.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.name = "Extrude Mesh.001"
    extrude_mesh_001.mode = 'VERTICES'
    # Offset Scale
    extrude_mesh_001.inputs[3].default_value = 0.0020000000949949026

    # Node Repeat Input
    repeat_input = gold_on_band_1.nodes.new("GeometryNodeRepeatInput")
    repeat_input.name = "Repeat Input"
    # Node Repeat Output
    repeat_output = gold_on_band_1.nodes.new("GeometryNodeRepeatOutput")
    repeat_output.name = "Repeat Output"
    repeat_output.active_index = 1
    repeat_output.inspection_index = 0
    repeat_output.repeat_items.clear()
    # Create item "Geometry"
    repeat_output.repeat_items.new('GEOMETRY', "Geometry")
    # Create item "Top"
    repeat_output.repeat_items.new('BOOLEAN', "Top")

    # Node Noise Texture
    noise_texture = gold_on_band_1.nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.noise_dimensions = '4D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    # Vector
    noise_texture.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Scale
    noise_texture.inputs[2].default_value = 39.5
    # Detail
    noise_texture.inputs[3].default_value = 0.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0

    # Node Map Range
    map_range = gold_on_band_1.nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.clamp = True
    map_range.data_type = 'FLOAT_VECTOR'
    map_range.interpolation_type = 'LINEAR'
    # From_Min_FLOAT3
    map_range.inputs[7].default_value = (0.0, 0.0, 0.0)
    # From_Max_FLOAT3
    map_range.inputs[8].default_value = (1.0, 1.0, 1.0)
    # To_Min_FLOAT3
    map_range.inputs[9].default_value = (-1.0, -1.0, -1.0)
    # To_Max_FLOAT3
    map_range.inputs[10].default_value = (1.0, 1.0, 1.0)

    # Node Mesh to Curve.002
    mesh_to_curve_002 = gold_on_band_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.name = "Mesh to Curve.002"
    mesh_to_curve_002.mode = 'EDGES'
    # Selection
    mesh_to_curve_002.inputs[1].default_value = True

    # Node Curve to Mesh.001
    curve_to_mesh_001 = gold_on_band_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False

    # Node Curve Circle
    curve_circle = gold_on_band_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.mode = 'RADIUS'
    # Resolution
    curve_circle.inputs[0].default_value = 6
    # Radius
    curve_circle.inputs[4].default_value = 0.0010000000474974513

    # Node Spline Parameter
    spline_parameter = gold_on_band_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"
    spline_parameter.outputs[1].hide = True
    spline_parameter.outputs[2].hide = True

    # Node Math.004
    math_004 = gold_on_band_1.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'SUBTRACT'
    math_004.use_clamp = False
    # Value
    math_004.inputs[0].default_value = 1.0

    # Node Vector Math
    vector_math = gold_on_band_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'CROSS_PRODUCT'

    # Node Vector Math.001
    vector_math_001 = gold_on_band_1.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'NORMALIZE'

    # Node Geometry Proximity
    geometry_proximity = gold_on_band_1.nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.target_element = 'FACES'
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Source Position
    geometry_proximity.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0

    # Node Group Input.001
    group_input_001 = gold_on_band_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[1].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[3].hide = True
    group_input_001.outputs[4].hide = True

    # Node Compare
    compare = gold_on_band_1.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'FLOAT'
    compare.mode = 'ELEMENT'
    compare.operation = 'LESS_EQUAL'
    # B
    compare.inputs[1].default_value = 0.0010000000474974513

    # Node Boolean Math
    boolean_math = gold_on_band_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.operation = 'AND'

    # Node Store Named Attribute
    store_named_attribute = gold_on_band_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'BOOLEAN'
    store_named_attribute.domain = 'POINT'
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True

    # Process zone input Repeat Input
    repeat_input.pair_with_output(repeat_output)
    # Iterations
    repeat_input.inputs[0].default_value = 100
    # Item_1
    repeat_input.inputs[2].default_value = True



    # Set locations
    gold_on_band_1.nodes["Group Output"].location = (1200.0, 80.0)
    gold_on_band_1.nodes["Group Input"].location = (-1423.4365234375, -77.9857406616211)
    gold_on_band_1.nodes["Distribute Points on Faces"].location = (-1203.4364013671875, 102.0142593383789)
    gold_on_band_1.nodes["Points to Vertices"].location = (-1003.4364624023438, 102.0142593383789)
    gold_on_band_1.nodes["Extrude Mesh.001"].location = (-483.4364318847656, 102.0142593383789)
    gold_on_band_1.nodes["Repeat Input"].location = (-833.4364624023438, 102.0142593383789)
    gold_on_band_1.nodes["Repeat Output"].location = (196.5635528564453, 102.0142593383789)
    gold_on_band_1.nodes["Noise Texture"].location = (-1183.4364013671875, -137.98573303222656)
    gold_on_band_1.nodes["Map Range"].location = (-1003.4364624023438, -137.98573303222656)
    gold_on_band_1.nodes["Mesh to Curve.002"].location = (440.0, 80.0)
    gold_on_band_1.nodes["Curve to Mesh.001"].location = (600.0, 80.0)
    gold_on_band_1.nodes["Curve Circle"].location = (420.0, -60.0)
    gold_on_band_1.nodes["Spline Parameter"].location = (600.0, -200.0)
    gold_on_band_1.nodes["Math.004"].location = (600.0, -60.0)
    gold_on_band_1.nodes["Vector Math"].location = (-843.4364624023438, -137.98573303222656)
    gold_on_band_1.nodes["Vector Math.001"].location = (-683.4364624023438, -137.98573303222656)
    gold_on_band_1.nodes["Geometry Proximity"].location = (-203.4364471435547, -117.9857406616211)
    gold_on_band_1.nodes["Group Input.001"].location = (-363.4364318847656, -117.9857406616211)
    gold_on_band_1.nodes["Compare"].location = (-23.43644142150879, -117.9857406616211)
    gold_on_band_1.nodes["Boolean Math"].location = (-23.43644142150879, 22.01426124572754)
    gold_on_band_1.nodes["Store Named Attribute"].location = (780.0, 80.0)

    # Set dimensions
    gold_on_band_1.nodes["Group Output"].width  = 140.0
    gold_on_band_1.nodes["Group Output"].height = 100.0

    gold_on_band_1.nodes["Group Input"].width  = 140.0
    gold_on_band_1.nodes["Group Input"].height = 100.0

    gold_on_band_1.nodes["Distribute Points on Faces"].width  = 170.0
    gold_on_band_1.nodes["Distribute Points on Faces"].height = 100.0

    gold_on_band_1.nodes["Points to Vertices"].width  = 140.0
    gold_on_band_1.nodes["Points to Vertices"].height = 100.0

    gold_on_band_1.nodes["Extrude Mesh.001"].width  = 140.0
    gold_on_band_1.nodes["Extrude Mesh.001"].height = 100.0

    gold_on_band_1.nodes["Repeat Input"].width  = 140.0
    gold_on_band_1.nodes["Repeat Input"].height = 100.0

    gold_on_band_1.nodes["Repeat Output"].width  = 140.0
    gold_on_band_1.nodes["Repeat Output"].height = 100.0

    gold_on_band_1.nodes["Noise Texture"].width  = 145.0
    gold_on_band_1.nodes["Noise Texture"].height = 100.0

    gold_on_band_1.nodes["Map Range"].width  = 140.0
    gold_on_band_1.nodes["Map Range"].height = 100.0

    gold_on_band_1.nodes["Mesh to Curve.002"].width  = 140.0
    gold_on_band_1.nodes["Mesh to Curve.002"].height = 100.0

    gold_on_band_1.nodes["Curve to Mesh.001"].width  = 140.0
    gold_on_band_1.nodes["Curve to Mesh.001"].height = 100.0

    gold_on_band_1.nodes["Curve Circle"].width  = 140.0
    gold_on_band_1.nodes["Curve Circle"].height = 100.0

    gold_on_band_1.nodes["Spline Parameter"].width  = 140.0
    gold_on_band_1.nodes["Spline Parameter"].height = 100.0

    gold_on_band_1.nodes["Math.004"].width  = 140.0
    gold_on_band_1.nodes["Math.004"].height = 100.0

    gold_on_band_1.nodes["Vector Math"].width  = 140.0
    gold_on_band_1.nodes["Vector Math"].height = 100.0

    gold_on_band_1.nodes["Vector Math.001"].width  = 140.0
    gold_on_band_1.nodes["Vector Math.001"].height = 100.0

    gold_on_band_1.nodes["Geometry Proximity"].width  = 140.0
    gold_on_band_1.nodes["Geometry Proximity"].height = 100.0

    gold_on_band_1.nodes["Group Input.001"].width  = 140.0
    gold_on_band_1.nodes["Group Input.001"].height = 100.0

    gold_on_band_1.nodes["Compare"].width  = 140.0
    gold_on_band_1.nodes["Compare"].height = 100.0

    gold_on_band_1.nodes["Boolean Math"].width  = 140.0
    gold_on_band_1.nodes["Boolean Math"].height = 100.0

    gold_on_band_1.nodes["Store Named Attribute"].width  = 140.0
    gold_on_band_1.nodes["Store Named Attribute"].height = 100.0


    # Initialize gold_on_band_1 links

    # noise_texture.Color -> map_range.Vector
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Noise Texture"].outputs[1],
        gold_on_band_1.nodes["Map Range"].inputs[6]
    )
    # math_004.Value -> curve_to_mesh_001.Scale
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Math.004"].outputs[0],
        gold_on_band_1.nodes["Curve to Mesh.001"].inputs[2]
    )
    # repeat_input.Top -> extrude_mesh_001.Selection
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Repeat Input"].outputs[2],
        gold_on_band_1.nodes["Extrude Mesh.001"].inputs[1]
    )
    # boolean_math.Boolean -> repeat_output.Top
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Boolean Math"].outputs[0],
        gold_on_band_1.nodes["Repeat Output"].inputs[1]
    )
    # extrude_mesh_001.Mesh -> repeat_output.Geometry
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Extrude Mesh.001"].outputs[0],
        gold_on_band_1.nodes["Repeat Output"].inputs[0]
    )
    # repeat_input.Geometry -> extrude_mesh_001.Mesh
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Repeat Input"].outputs[1],
        gold_on_band_1.nodes["Extrude Mesh.001"].inputs[0]
    )
    # spline_parameter.Factor -> math_004.Value
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Spline Parameter"].outputs[0],
        gold_on_band_1.nodes["Math.004"].inputs[1]
    )
    # mesh_to_curve_002.Curve -> curve_to_mesh_001.Curve
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Mesh to Curve.002"].outputs[0],
        gold_on_band_1.nodes["Curve to Mesh.001"].inputs[0]
    )
    # distribute_points_on_faces.Points -> points_to_vertices.Points
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Distribute Points on Faces"].outputs[0],
        gold_on_band_1.nodes["Points to Vertices"].inputs[0]
    )
    # curve_circle.Curve -> curve_to_mesh_001.Profile Curve
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Curve Circle"].outputs[0],
        gold_on_band_1.nodes["Curve to Mesh.001"].inputs[1]
    )
    # points_to_vertices.Mesh -> repeat_input.Geometry
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Points to Vertices"].outputs[0],
        gold_on_band_1.nodes["Repeat Input"].inputs[1]
    )
    # vector_math_001.Vector -> extrude_mesh_001.Offset
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Vector Math.001"].outputs[0],
        gold_on_band_1.nodes["Extrude Mesh.001"].inputs[2]
    )
    # repeat_output.Geometry -> mesh_to_curve_002.Mesh
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Repeat Output"].outputs[0],
        gold_on_band_1.nodes["Mesh to Curve.002"].inputs[0]
    )
    # group_input.Mesh -> distribute_points_on_faces.Mesh
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Group Input"].outputs[0],
        gold_on_band_1.nodes["Distribute Points on Faces"].inputs[0]
    )
    # group_input.Density -> distribute_points_on_faces.Density
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Group Input"].outputs[1],
        gold_on_band_1.nodes["Distribute Points on Faces"].inputs[4]
    )
    # group_input.W -> noise_texture.W
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Group Input"].outputs[2],
        gold_on_band_1.nodes["Noise Texture"].inputs[1]
    )
    # map_range.Vector -> vector_math.Vector
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Map Range"].outputs[1],
        gold_on_band_1.nodes["Vector Math"].inputs[0]
    )
    # distribute_points_on_faces.Normal -> vector_math.Vector
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Distribute Points on Faces"].outputs[1],
        gold_on_band_1.nodes["Vector Math"].inputs[1]
    )
    # group_input.Seed -> distribute_points_on_faces.Seed
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Group Input"].outputs[3],
        gold_on_band_1.nodes["Distribute Points on Faces"].inputs[6]
    )
    # vector_math.Vector -> vector_math_001.Vector
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Vector Math"].outputs[0],
        gold_on_band_1.nodes["Vector Math.001"].inputs[0]
    )
    # group_input_001.Mesh -> geometry_proximity.Geometry
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Group Input.001"].outputs[0],
        gold_on_band_1.nodes["Geometry Proximity"].inputs[0]
    )
    # geometry_proximity.Distance -> compare.A
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Geometry Proximity"].outputs[1],
        gold_on_band_1.nodes["Compare"].inputs[0]
    )
    # extrude_mesh_001.Top -> boolean_math.Boolean
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Extrude Mesh.001"].outputs[1],
        gold_on_band_1.nodes["Boolean Math"].inputs[0]
    )
    # compare.Result -> boolean_math.Boolean
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Compare"].outputs[0],
        gold_on_band_1.nodes["Boolean Math"].inputs[1]
    )
    # store_named_attribute.Geometry -> group_output.Mesh
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Store Named Attribute"].outputs[0],
        gold_on_band_1.nodes["Group Output"].inputs[0]
    )
    # curve_to_mesh_001.Mesh -> store_named_attribute.Geometry
    gold_on_band_1.links.new(
        gold_on_band_1.nodes["Curve to Mesh.001"].outputs[0],
        gold_on_band_1.nodes["Store Named Attribute"].inputs[0]
    )

    return gold_on_band_1


def gem_in_holder_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Gem in Holder node group"""
    gem_in_holder_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Gem in Holder")

    gem_in_holder_1.color_tag = 'GEOMETRY'
    gem_in_holder_1.description = ""
    gem_in_holder_1.default_group_node_width = 140
    gem_in_holder_1.show_modifier_manage_panel = True

    # gem_in_holder_1 interface

    # Socket Geometry
    geometry_socket = gem_in_holder_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Gem Radius
    gem_radius_socket = gem_in_holder_1.interface.new_socket(name="Gem Radius", in_out='INPUT', socket_type='NodeSocketFloat')
    gem_radius_socket.default_value = 0.009999999776482582
    gem_radius_socket.min_value = 0.0
    gem_radius_socket.max_value = 3.4028234663852886e+38
    gem_radius_socket.subtype = 'DISTANCE'
    gem_radius_socket.attribute_domain = 'POINT'
    gem_radius_socket.description = "Distance of the points from the origin"
    gem_radius_socket.default_input = 'VALUE'
    gem_radius_socket.structure_type = 'AUTO'

    # Socket Gem Material
    gem_material_socket = gem_in_holder_1.interface.new_socket(name="Gem Material", in_out='INPUT', socket_type='NodeSocketString')
    gem_material_socket.default_value = "ruby"
    gem_material_socket.subtype = 'NONE'
    gem_material_socket.attribute_domain = 'POINT'
    gem_material_socket.default_input = 'VALUE'
    gem_material_socket.structure_type = 'AUTO'
    gem_material_socket.optional_label = True

    # Socket Gem Dual Mesh
    gem_dual_mesh_socket = gem_in_holder_1.interface.new_socket(name="Gem Dual Mesh", in_out='INPUT', socket_type='NodeSocketBool')
    gem_dual_mesh_socket.default_value = False
    gem_dual_mesh_socket.attribute_domain = 'POINT'
    gem_dual_mesh_socket.default_input = 'VALUE'
    gem_dual_mesh_socket.structure_type = 'AUTO'

    # Panel Profile
    profile_panel = gem_in_holder_1.interface.new_panel("Profile")
    # Socket Profile Curve
    profile_curve_socket = gem_in_holder_1.interface.new_socket(name="Profile Curve", in_out='OUTPUT', socket_type='NodeSocketGeometry', parent = profile_panel)
    profile_curve_socket.attribute_domain = 'POINT'
    profile_curve_socket.default_input = 'VALUE'
    profile_curve_socket.structure_type = 'AUTO'

    # Socket Profile Scale
    profile_scale_socket = gem_in_holder_1.interface.new_socket(name="Profile Scale", in_out='OUTPUT', socket_type='NodeSocketFloat', parent = profile_panel)
    profile_scale_socket.default_value = 0.0
    profile_scale_socket.min_value = -3.4028234663852886e+38
    profile_scale_socket.max_value = 3.4028234663852886e+38
    profile_scale_socket.subtype = 'NONE'
    profile_scale_socket.attribute_domain = 'POINT'
    profile_scale_socket.default_input = 'VALUE'
    profile_scale_socket.structure_type = 'AUTO'

    # Socket Scale
    scale_socket = gem_in_holder_1.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat', parent = profile_panel)
    scale_socket.default_value = 0.004999999888241291
    scale_socket.min_value = 0.0
    scale_socket.max_value = 3.4028234663852886e+38
    scale_socket.subtype = 'NONE'
    scale_socket.attribute_domain = 'POINT'
    scale_socket.description = "Scale of the profile at each point"
    scale_socket.default_input = 'VALUE'
    scale_socket.structure_type = 'AUTO'

    # Socket Count
    count_socket = gem_in_holder_1.interface.new_socket(name="Count", in_out='INPUT', socket_type='NodeSocketInt', parent = profile_panel)
    count_socket.default_value = 20
    count_socket.min_value = 0
    count_socket.max_value = 2147483647
    count_socket.subtype = 'NONE'
    count_socket.attribute_domain = 'POINT'
    count_socket.description = "The number of points to create"
    count_socket.default_input = 'VALUE'
    count_socket.structure_type = 'AUTO'

    # Socket Seed
    seed_socket = gem_in_holder_1.interface.new_socket(name="Seed", in_out='INPUT', socket_type='NodeSocketInt', parent = profile_panel)
    seed_socket.default_value = 10
    seed_socket.min_value = -10000
    seed_socket.max_value = 10000
    seed_socket.subtype = 'NONE'
    seed_socket.attribute_domain = 'POINT'
    seed_socket.default_input = 'VALUE'
    seed_socket.structure_type = 'AUTO'


    # Panel Wings
    wings_panel = gem_in_holder_1.interface.new_panel("Wings")
    # Socket Wings
    wings_socket = gem_in_holder_1.interface.new_socket(name="Wings", in_out='INPUT', socket_type='NodeSocketBool', parent = wings_panel)
    wings_socket.default_value = False
    wings_socket.attribute_domain = 'POINT'
    wings_socket.default_input = 'VALUE'
    wings_socket.is_panel_toggle = True
    wings_socket.structure_type = 'AUTO'

    # Socket Wing
    wing_socket = gem_in_holder_1.interface.new_socket(name="Wing", in_out='OUTPUT', socket_type='NodeSocketGeometry', parent = wings_panel)
    wing_socket.attribute_domain = 'POINT'
    wing_socket.default_input = 'VALUE'
    wing_socket.structure_type = 'AUTO'

    # Socket Wing Curve
    wing_curve_socket = gem_in_holder_1.interface.new_socket(name="Wing Curve", in_out='OUTPUT', socket_type='NodeSocketGeometry', parent = wings_panel)
    wing_curve_socket.attribute_domain = 'POINT'
    wing_curve_socket.default_input = 'VALUE'
    wing_curve_socket.structure_type = 'AUTO'

    # Socket Array Count
    array_count_socket = gem_in_holder_1.interface.new_socket(name="Array Count", in_out='INPUT', socket_type='NodeSocketInt', parent = wings_panel)
    array_count_socket.default_value = 6
    array_count_socket.min_value = 3
    array_count_socket.max_value = 512
    array_count_socket.subtype = 'NONE'
    array_count_socket.attribute_domain = 'POINT'
    array_count_socket.description = "Number of points on the circle"
    array_count_socket.default_input = 'VALUE'
    array_count_socket.structure_type = 'AUTO'

    # Socket Strand Count
    strand_count_socket = gem_in_holder_1.interface.new_socket(name="Strand Count", in_out='INPUT', socket_type='NodeSocketInt', parent = wings_panel)
    strand_count_socket.default_value = 10
    strand_count_socket.min_value = 0
    strand_count_socket.max_value = 2147483647
    strand_count_socket.subtype = 'NONE'
    strand_count_socket.attribute_domain = 'POINT'
    strand_count_socket.description = "The number of points to create"
    strand_count_socket.default_input = 'VALUE'
    strand_count_socket.structure_type = 'AUTO'

    # Socket Split
    split_socket = gem_in_holder_1.interface.new_socket(name="Split", in_out='INPUT', socket_type='NodeSocketFloat', parent = wings_panel)
    split_socket.default_value = 0.0020000000949949026
    split_socket.min_value = -10000.0
    split_socket.max_value = 10000.0
    split_socket.subtype = 'NONE'
    split_socket.attribute_domain = 'POINT'
    split_socket.default_input = 'VALUE'
    split_socket.structure_type = 'AUTO'

    # Socket Seed
    seed_socket_1 = gem_in_holder_1.interface.new_socket(name="Seed", in_out='INPUT', socket_type='NodeSocketFloat', parent = wings_panel)
    seed_socket_1.default_value = 2.5099997520446777
    seed_socket_1.min_value = -10000.0
    seed_socket_1.max_value = 10000.0
    seed_socket_1.subtype = 'NONE'
    seed_socket_1.attribute_domain = 'POINT'
    seed_socket_1.default_input = 'VALUE'
    seed_socket_1.structure_type = 'AUTO'


    # Initialize gem_in_holder_1 nodes

    # Node Group Output
    group_output = gem_in_holder_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = gem_in_holder_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[1].hide = True
    group_input.outputs[2].hide = True
    group_input.outputs[6].hide = True
    group_input.outputs[7].hide = True
    group_input.outputs[8].hide = True
    group_input.outputs[9].hide = True
    group_input.outputs[10].hide = True
    group_input.outputs[11].hide = True

    # Node Ico Sphere.001
    ico_sphere_001 = gem_in_holder_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.name = "Ico Sphere.001"
    # Subdivisions
    ico_sphere_001.inputs[1].default_value = 2

    # Node Dual Mesh
    dual_mesh = gem_in_holder_1.nodes.new("GeometryNodeDualMesh")
    dual_mesh.name = "Dual Mesh"
    # Keep Boundaries
    dual_mesh.inputs[1].default_value = False

    # Node Curve Circle
    curve_circle = gem_in_holder_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.mode = 'RADIUS'
    # Resolution
    curve_circle.inputs[0].default_value = 24

    # Node Curve to Mesh.002
    curve_to_mesh_002 = gem_in_holder_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False

    # Node Points
    points = gem_in_holder_1.nodes.new("GeometryNodePoints")
    points.name = "Points"
    # Radius
    points.inputs[2].default_value = 0.10000000149011612

    # Node Random Value
    random_value = gem_in_holder_1.nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.data_type = 'FLOAT_VECTOR'
    # Min
    random_value.inputs[0].default_value = (-0.5, -1.0, 0.0)
    # Max
    random_value.inputs[1].default_value = (0.5, 1.0, 0.0)
    # ID
    random_value.inputs[7].default_value = 0

    # Node Points to Curves
    points_to_curves = gem_in_holder_1.nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0

    # Node Gradient Texture
    gradient_texture = gem_in_holder_1.nodes.new("ShaderNodeTexGradient")
    gradient_texture.name = "Gradient Texture"
    gradient_texture.gradient_type = 'RADIAL'
    # Vector
    gradient_texture.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Set Spline Cyclic
    set_spline_cyclic = gem_in_holder_1.nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = True

    # Node Set Spline Type
    set_spline_type = gem_in_holder_1.nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.spline_type = 'NURBS'
    # Selection
    set_spline_type.inputs[1].default_value = True

    # Node Transform Geometry.005
    transform_geometry_005 = gem_in_holder_1.nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.inputs[1].hide = True
    transform_geometry_005.inputs[3].hide = True
    transform_geometry_005.inputs[5].hide = True
    # Mode
    transform_geometry_005.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_005.inputs[2].default_value = (0.0, 0.0, 0.0020000000949949026)
    # Rotation
    transform_geometry_005.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_005.inputs[4].default_value = (1.0, 1.0, 0.6000000238418579)

    # Node Points to Vertices
    points_to_vertices = gem_in_holder_1.nodes.new("GeometryNodePointsToVertices")
    points_to_vertices.name = "Points to Vertices"
    # Selection
    points_to_vertices.inputs[1].default_value = True

    # Node Extrude Mesh.001
    extrude_mesh_001 = gem_in_holder_1.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.name = "Extrude Mesh.001"
    extrude_mesh_001.mode = 'VERTICES'
    # Offset Scale
    extrude_mesh_001.inputs[3].default_value = 0.0020000000949949026

    # Node Repeat Input.001
    repeat_input_001 = gem_in_holder_1.nodes.new("GeometryNodeRepeatInput")
    repeat_input_001.name = "Repeat Input.001"
    # Node Repeat Output.001
    repeat_output_001 = gem_in_holder_1.nodes.new("GeometryNodeRepeatOutput")
    repeat_output_001.name = "Repeat Output.001"
    repeat_output_001.active_index = 2
    repeat_output_001.inspection_index = 0
    repeat_output_001.repeat_items.clear()
    # Create item "Geometry"
    repeat_output_001.repeat_items.new('GEOMETRY', "Geometry")
    # Create item "Top"
    repeat_output_001.repeat_items.new('BOOLEAN', "Top")
    # Create item "Value"
    repeat_output_001.repeat_items.new('VECTOR', "Value")

    # Node Noise Texture
    noise_texture = gem_in_holder_1.nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.noise_dimensions = '4D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = False
    # Vector
    noise_texture.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Scale
    noise_texture.inputs[2].default_value = 30.0
    # Detail
    noise_texture.inputs[3].default_value = 0.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0

    # Node Mesh to Curve.003
    mesh_to_curve_003 = gem_in_holder_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_003.name = "Mesh to Curve.003"
    mesh_to_curve_003.mode = 'EDGES'
    # Selection
    mesh_to_curve_003.inputs[1].default_value = True

    # Node Curve to Mesh.003
    curve_to_mesh_003 = gem_in_holder_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.name = "Curve to Mesh.003"
    # Fill Caps
    curve_to_mesh_003.inputs[3].default_value = False

    # Node Spline Parameter.003
    spline_parameter_003 = gem_in_holder_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_003.name = "Spline Parameter.003"
    spline_parameter_003.outputs[1].hide = True
    spline_parameter_003.outputs[2].hide = True

    # Node Float Curve
    float_curve = gem_in_holder_1.nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    # Mapping settings
    float_curve.mapping.extend = 'EXTRAPOLATED'
    float_curve.mapping.tone = 'STANDARD'
    float_curve.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve.mapping.clip_min_x = 0.0
    float_curve.mapping.clip_min_y = 0.0
    float_curve.mapping.clip_max_x = 1.0
    float_curve.mapping.clip_max_y = 1.0
    float_curve.mapping.use_clip = True
    # Curve 0
    float_curve_curve_0 = float_curve.mapping.curves[0]
    float_curve_curve_0_point_0 = float_curve_curve_0.points[0]
    float_curve_curve_0_point_0.location = (0.0, 0.0)
    float_curve_curve_0_point_0.handle_type = 'AUTO'
    float_curve_curve_0_point_1 = float_curve_curve_0.points[1]
    float_curve_curve_0_point_1.location = (0.640483021736145, 0.3534482419490814)
    float_curve_curve_0_point_1.handle_type = 'AUTO'
    float_curve_curve_0_point_2 = float_curve_curve_0.points.new(0.870090663433075, 0.800000011920929)
    float_curve_curve_0_point_2.handle_type = 'AUTO'
    float_curve_curve_0_point_3 = float_curve_curve_0.points.new(1.0, 0.0)
    float_curve_curve_0_point_3.handle_type = 'AUTO'
    # Update curve after changes
    float_curve.mapping.update()
    # Factor
    float_curve.inputs[0].default_value = 1.0

    # Node Math
    math = gem_in_holder_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    # Value_001
    math.inputs[1].default_value = 0.004999999888241291

    # Node Points.001
    points_001 = gem_in_holder_1.nodes.new("GeometryNodePoints")
    points_001.name = "Points.001"
    # Position
    points_001.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Radius
    points_001.inputs[2].default_value = 0.10000000149011612

    # Node Index
    index = gem_in_holder_1.nodes.new("GeometryNodeInputIndex")
    index.name = "Index"

    # Node Capture Attribute.007
    capture_attribute_007 = gem_in_holder_1.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_007.name = "Capture Attribute.007"
    capture_attribute_007.active_index = 0
    capture_attribute_007.capture_items.clear()
    capture_attribute_007.capture_items.new('FLOAT', "Index")
    capture_attribute_007.capture_items["Index"].data_type = 'INT'
    capture_attribute_007.domain = 'POINT'

    # Node Math.001
    math_001 = gem_in_holder_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'MULTIPLY_ADD'
    math_001.use_clamp = False

    # Node Transform Geometry.006
    transform_geometry_006 = gem_in_holder_1.nodes.new("GeometryNodeTransform")
    transform_geometry_006.name = "Transform Geometry.006"
    # Mode
    transform_geometry_006.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_006.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_006.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_006.inputs[4].default_value = (-1.0, 1.0, 1.0)

    # Node Flip Faces.001
    flip_faces_001 = gem_in_holder_1.nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.name = "Flip Faces.001"
    # Selection
    flip_faces_001.inputs[1].default_value = True

    # Node Join Geometry.003
    join_geometry_003 = gem_in_holder_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.hide = True

    # Node Instance on Points.003
    instance_on_points_003 = gem_in_holder_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.name = "Instance on Points.003"
    # Selection
    instance_on_points_003.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_003.inputs[3].default_value = False
    # Instance Index
    instance_on_points_003.inputs[4].default_value = 0
    # Scale
    instance_on_points_003.inputs[6].default_value = (1.0, 1.0, 1.0)

    # Node Curve Circle.001
    curve_circle_001 = gem_in_holder_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.name = "Curve Circle.001"
    curve_circle_001.mode = 'RADIUS'
    # Radius
    curve_circle_001.inputs[4].default_value = 9.999999747378752e-05

    # Node Align Rotation to Vector.002
    align_rotation_to_vector_002 = gem_in_holder_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.name = "Align Rotation to Vector.002"
    align_rotation_to_vector_002.axis = 'X'
    align_rotation_to_vector_002.pivot_axis = 'AUTO'
    # Rotation
    align_rotation_to_vector_002.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Factor
    align_rotation_to_vector_002.inputs[1].default_value = 1.0

    # Node Curve Tangent
    curve_tangent = gem_in_holder_1.nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"

    # Node Join Geometry.004
    join_geometry_004 = gem_in_holder_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.hide = True

    # Node Realize Instances.003
    realize_instances_003 = gem_in_holder_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.name = "Realize Instances.003"
    # Selection
    realize_instances_003.inputs[1].default_value = True
    # Realize All
    realize_instances_003.inputs[2].default_value = True
    # Depth
    realize_instances_003.inputs[3].default_value = 0

    # Node Switch
    switch = gem_in_holder_1.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'GEOMETRY'

    # Node Group Input.001
    group_input_001 = gem_in_holder_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"

    # Node Group Input.002
    group_input_002 = gem_in_holder_1.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[0].hide = True
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[2].hide = True
    group_input_002.outputs[3].hide = True
    group_input_002.outputs[4].hide = True
    group_input_002.outputs[5].hide = True
    group_input_002.outputs[6].hide = True
    group_input_002.outputs[7].hide = True
    group_input_002.outputs[11].hide = True

    # Node Group Input.003
    group_input_003 = gem_in_holder_1.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.outputs[0].hide = True
    group_input_003.outputs[1].hide = True
    group_input_003.outputs[2].hide = True
    group_input_003.outputs[3].hide = True
    group_input_003.outputs[4].hide = True
    group_input_003.outputs[5].hide = True
    group_input_003.outputs[6].hide = True
    group_input_003.outputs[8].hide = True
    group_input_003.outputs[9].hide = True
    group_input_003.outputs[10].hide = True
    group_input_003.outputs[11].hide = True

    # Node Frame
    frame = gem_in_holder_1.nodes.new("NodeFrame")
    frame.label = "Profile"
    frame.name = "Frame"
    frame.label_size = 20
    frame.shrink = True

    # Node Frame.001
    frame_001 = gem_in_holder_1.nodes.new("NodeFrame")
    frame_001.label = "Gem"
    frame_001.name = "Frame.001"
    frame_001.label_size = 20
    frame_001.shrink = True

    # Node Frame.002
    frame_002 = gem_in_holder_1.nodes.new("NodeFrame")
    frame_002.label = "Strands"
    frame_002.name = "Frame.002"
    frame_002.label_size = 20
    frame_002.shrink = True

    # Node Frame.003
    frame_003 = gem_in_holder_1.nodes.new("NodeFrame")
    frame_003.label = "Mesh"
    frame_003.name = "Frame.003"
    frame_003.label_size = 20
    frame_003.shrink = True

    # Node Frame.004
    frame_004 = gem_in_holder_1.nodes.new("NodeFrame")
    frame_004.label = "Mirror"
    frame_004.name = "Frame.004"
    frame_004.label_size = 20
    frame_004.shrink = True

    # Node Frame.005
    frame_005 = gem_in_holder_1.nodes.new("NodeFrame")
    frame_005.label = "Radial Array"
    frame_005.name = "Frame.005"
    frame_005.label_size = 20
    frame_005.shrink = True

    # Node Store Named Attribute
    store_named_attribute = gem_in_holder_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'BOOLEAN'
    store_named_attribute.domain = 'POINT'
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "gold"
    # Value
    store_named_attribute.inputs[3].default_value = True

    # Node Join Geometry.005
    join_geometry_005 = gem_in_holder_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.hide = True

    # Node Store Named Attribute.001
    store_named_attribute_001 = gem_in_holder_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.data_type = 'BOOLEAN'
    store_named_attribute_001.domain = 'POINT'
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Value
    store_named_attribute_001.inputs[3].default_value = True

    # Node Mix
    mix = gem_in_holder_1.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'VECTOR'
    mix.factor_mode = 'UNIFORM'
    # A_Vector
    mix.inputs[4].default_value = (1.0, 1.0, 0.0)
    # B_Vector
    mix.inputs[5].default_value = (1.0, 1.0, 1.0)

    # Node Vector Math
    vector_math = gem_in_holder_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'MULTIPLY'

    # Node Position
    position = gem_in_holder_1.nodes.new("GeometryNodeInputPosition")
    position.name = "Position"

    # Node Vector Math.001
    vector_math_001 = gem_in_holder_1.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'LENGTH'

    # Node Map Range
    map_range = gem_in_holder_1.nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.clamp = True
    map_range.data_type = 'FLOAT'
    map_range.interpolation_type = 'LINEAR'
    # From Max
    map_range.inputs[2].default_value = 0.05000000074505806
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0

    # Node Group Input.004
    group_input_004 = gem_in_holder_1.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.outputs[1].hide = True
    group_input_004.outputs[2].hide = True
    group_input_004.outputs[3].hide = True
    group_input_004.outputs[4].hide = True
    group_input_004.outputs[5].hide = True
    group_input_004.outputs[6].hide = True
    group_input_004.outputs[7].hide = True
    group_input_004.outputs[8].hide = True
    group_input_004.outputs[9].hide = True
    group_input_004.outputs[10].hide = True
    group_input_004.outputs[11].hide = True

    # Node Store Named Attribute.002
    store_named_attribute_002 = gem_in_holder_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.data_type = 'BOOLEAN'
    store_named_attribute_002.domain = 'POINT'
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_002.inputs[3].default_value = True

    # Node Transform Geometry
    transform_geometry = gem_in_holder_1.nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry.inputs[2].default_value = (0.0, 0.0, 0.0020000000949949026)
    # Rotation
    transform_geometry.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Separate XYZ
    separate_xyz = gem_in_holder_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"

    # Node Combine XYZ
    combine_xyz = gem_in_holder_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"

    # Node Math.002
    math_002 = gem_in_holder_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'ABSOLUTE'
    math_002.use_clamp = False

    # Node Resample Curve
    resample_curve = gem_in_holder_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = 'Count'
    # Count
    resample_curve.inputs[3].default_value = 12
    # Length
    resample_curve.inputs[4].default_value = 0.10000000149011612

    # Node Resample Curve.001
    resample_curve_001 = gem_in_holder_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = 'Length'
    # Count
    resample_curve_001.inputs[3].default_value = 10
    # Length
    resample_curve_001.inputs[4].default_value = 0.0007999999797903001

    # Node Switch.001
    switch_001 = gem_in_holder_1.nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.input_type = 'GEOMETRY'

    # Node Group Input.005
    group_input_005 = gem_in_holder_1.nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    group_input_005.outputs[0].hide = True
    group_input_005.outputs[1].hide = True
    group_input_005.outputs[2].hide = True
    group_input_005.outputs[3].hide = True
    group_input_005.outputs[4].hide = True
    group_input_005.outputs[5].hide = True
    group_input_005.outputs[7].hide = True
    group_input_005.outputs[8].hide = True
    group_input_005.outputs[9].hide = True
    group_input_005.outputs[10].hide = True
    group_input_005.outputs[11].hide = True

    # Node Switch.002
    switch_002 = gem_in_holder_1.nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.input_type = 'VECTOR'
    # True
    switch_002.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Evaluate at Index
    evaluate_at_index = gem_in_holder_1.nodes.new("GeometryNodeFieldAtIndex")
    evaluate_at_index.name = "Evaluate at Index"
    evaluate_at_index.data_type = 'FLOAT_VECTOR'
    evaluate_at_index.domain = 'POINT'
    # Index
    evaluate_at_index.inputs[1].default_value = 0

    # Node Vector Math.002
    vector_math_002 = gem_in_holder_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'ADD'

    # Node Transform Geometry.001
    transform_geometry_001 = gem_in_holder_1.nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    # Mode
    transform_geometry_001.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_001.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Attribute Statistic
    attribute_statistic = gem_in_holder_1.nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.data_type = 'FLOAT_VECTOR'
    attribute_statistic.domain = 'POINT'
    # Selection
    attribute_statistic.inputs[1].default_value = True

    # Node Align Rotation to Vector
    align_rotation_to_vector = gem_in_holder_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.axis = 'X'
    align_rotation_to_vector.pivot_axis = 'AUTO'
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0

    # Node Invert Rotation
    invert_rotation = gem_in_holder_1.nodes.new("FunctionNodeInvertRotation")
    invert_rotation.name = "Invert Rotation"

    # Node Frame.006
    frame_006 = gem_in_holder_1.nodes.new("NodeFrame")
    frame_006.label = "Align to X"
    frame_006.name = "Frame.006"
    frame_006.label_size = 20
    frame_006.shrink = True

    # Node Store Named Attribute.003
    store_named_attribute_003 = gem_in_holder_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.data_type = 'BOOLEAN'
    store_named_attribute_003.domain = 'POINT'
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_003.inputs[3].default_value = True

    # Node Reroute
    reroute = gem_in_holder_1.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Process zone input Repeat Input.001
    repeat_input_001.pair_with_output(repeat_output_001)
    # Iterations
    repeat_input_001.inputs[0].default_value = 60
    # Item_1
    repeat_input_001.inputs[2].default_value = True
    # Item_2
    repeat_input_001.inputs[3].default_value = (0.0, 0.0, 0.0)



    # Set parents
    gem_in_holder_1.nodes["Group Input"].parent = gem_in_holder_1.nodes["Frame"]
    gem_in_holder_1.nodes["Ico Sphere.001"].parent = gem_in_holder_1.nodes["Frame.001"]
    gem_in_holder_1.nodes["Dual Mesh"].parent = gem_in_holder_1.nodes["Frame.001"]
    gem_in_holder_1.nodes["Curve Circle"].parent = gem_in_holder_1.nodes["Frame"]
    gem_in_holder_1.nodes["Curve to Mesh.002"].parent = gem_in_holder_1.nodes["Frame"]
    gem_in_holder_1.nodes["Points"].parent = gem_in_holder_1.nodes["Frame"]
    gem_in_holder_1.nodes["Random Value"].parent = gem_in_holder_1.nodes["Frame"]
    gem_in_holder_1.nodes["Points to Curves"].parent = gem_in_holder_1.nodes["Frame"]
    gem_in_holder_1.nodes["Gradient Texture"].parent = gem_in_holder_1.nodes["Frame"]
    gem_in_holder_1.nodes["Set Spline Cyclic"].parent = gem_in_holder_1.nodes["Frame"]
    gem_in_holder_1.nodes["Set Spline Type"].parent = gem_in_holder_1.nodes["Frame"]
    gem_in_holder_1.nodes["Transform Geometry.005"].parent = gem_in_holder_1.nodes["Frame.001"]
    gem_in_holder_1.nodes["Points to Vertices"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Extrude Mesh.001"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Repeat Input.001"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Repeat Output.001"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Noise Texture"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Mesh to Curve.003"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Curve to Mesh.003"].parent = gem_in_holder_1.nodes["Frame.003"]
    gem_in_holder_1.nodes["Spline Parameter.003"].parent = gem_in_holder_1.nodes["Frame.003"]
    gem_in_holder_1.nodes["Float Curve"].parent = gem_in_holder_1.nodes["Frame.003"]
    gem_in_holder_1.nodes["Math"].parent = gem_in_holder_1.nodes["Frame.003"]
    gem_in_holder_1.nodes["Points.001"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Index"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Capture Attribute.007"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Math.001"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Transform Geometry.006"].parent = gem_in_holder_1.nodes["Frame.004"]
    gem_in_holder_1.nodes["Flip Faces.001"].parent = gem_in_holder_1.nodes["Frame.004"]
    gem_in_holder_1.nodes["Join Geometry.003"].parent = gem_in_holder_1.nodes["Frame.004"]
    gem_in_holder_1.nodes["Instance on Points.003"].parent = gem_in_holder_1.nodes["Frame.005"]
    gem_in_holder_1.nodes["Curve Circle.001"].parent = gem_in_holder_1.nodes["Frame.005"]
    gem_in_holder_1.nodes["Align Rotation to Vector.002"].parent = gem_in_holder_1.nodes["Frame.005"]
    gem_in_holder_1.nodes["Curve Tangent"].parent = gem_in_holder_1.nodes["Frame.005"]
    gem_in_holder_1.nodes["Realize Instances.003"].parent = gem_in_holder_1.nodes["Frame.005"]
    gem_in_holder_1.nodes["Switch"].parent = gem_in_holder_1.nodes["Frame.001"]
    gem_in_holder_1.nodes["Group Input.001"].parent = gem_in_holder_1.nodes["Frame.001"]
    gem_in_holder_1.nodes["Group Input.002"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Group Input.003"].parent = gem_in_holder_1.nodes["Frame.005"]
    gem_in_holder_1.nodes["Store Named Attribute.001"].parent = gem_in_holder_1.nodes["Frame.001"]
    gem_in_holder_1.nodes["Mix"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Vector Math"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Position"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Vector Math.001"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Map Range"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Group Input.004"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Separate XYZ"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Combine XYZ"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Math.002"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Resample Curve"].parent = gem_in_holder_1.nodes["Frame"]
    gem_in_holder_1.nodes["Resample Curve.001"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Switch.002"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Evaluate at Index"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Vector Math.002"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Transform Geometry.001"].parent = gem_in_holder_1.nodes["Frame.006"]
    gem_in_holder_1.nodes["Attribute Statistic"].parent = gem_in_holder_1.nodes["Frame.002"]
    gem_in_holder_1.nodes["Align Rotation to Vector"].parent = gem_in_holder_1.nodes["Frame.006"]
    gem_in_holder_1.nodes["Invert Rotation"].parent = gem_in_holder_1.nodes["Frame.006"]
    gem_in_holder_1.nodes["Store Named Attribute.003"].parent = gem_in_holder_1.nodes["Frame.006"]
    gem_in_holder_1.nodes["Reroute"].parent = gem_in_holder_1.nodes["Frame.003"]

    # Set locations
    gem_in_holder_1.nodes["Group Output"].location = (2440.0, -400.0)
    gem_in_holder_1.nodes["Group Input"].location = (29.0, -135.79998779296875)
    gem_in_holder_1.nodes["Ico Sphere.001"].location = (189.0, -35.79998779296875)
    gem_in_holder_1.nodes["Dual Mesh"].location = (349.0, -35.79998779296875)
    gem_in_holder_1.nodes["Curve Circle"].location = (1289.0, -35.79998779296875)
    gem_in_holder_1.nodes["Curve to Mesh.002"].location = (1449.0, -35.79998779296875)
    gem_in_holder_1.nodes["Points"].location = (429.0, -195.79998779296875)
    gem_in_holder_1.nodes["Random Value"].location = (269.0, -195.79998779296875)
    gem_in_holder_1.nodes["Points to Curves"].location = (589.0, -195.79998779296875)
    gem_in_holder_1.nodes["Gradient Texture"].location = (429.0, -335.79998779296875)
    gem_in_holder_1.nodes["Set Spline Cyclic"].location = (749.0, -195.79998779296875)
    gem_in_holder_1.nodes["Set Spline Type"].location = (909.0, -195.79998779296875)
    gem_in_holder_1.nodes["Transform Geometry.005"].location = (689.0, -35.79998779296875)
    gem_in_holder_1.nodes["Points to Vertices"].location = (649.0, -215.13333129882812)
    gem_in_holder_1.nodes["Extrude Mesh.001"].location = (1769.0, -55.133331298828125)
    gem_in_holder_1.nodes["Repeat Input.001"].location = (1589.0, -55.133331298828125)
    gem_in_holder_1.nodes["Repeat Output.001"].location = (2289.0, -55.133331298828125)
    gem_in_holder_1.nodes["Noise Texture"].location = (589.0, -495.1333312988281)
    gem_in_holder_1.nodes["Mesh to Curve.003"].location = (2449.0, -55.133331298828125)
    gem_in_holder_1.nodes["Curve to Mesh.003"].location = (469.0, -35.80000305175781)
    gem_in_holder_1.nodes["Spline Parameter.003"].location = (49.0, -515.7999877929688)
    gem_in_holder_1.nodes["Float Curve"].location = (29.0, -175.8000030517578)
    gem_in_holder_1.nodes["Math"].location = (289.0, -175.8000030517578)
    gem_in_holder_1.nodes["Points.001"].location = (229.0, -315.1333312988281)
    gem_in_holder_1.nodes["Index"].location = (229.0, -495.1333312988281)
    gem_in_holder_1.nodes["Capture Attribute.007"].location = (409.0, -315.1333312988281)
    gem_in_holder_1.nodes["Math.001"].location = (429.0, -495.1333312988281)
    gem_in_holder_1.nodes["Transform Geometry.006"].location = (28.83331298828125, -79.56706237792969)
    gem_in_holder_1.nodes["Flip Faces.001"].location = (188.83331298828125, -79.56706237792969)
    gem_in_holder_1.nodes["Join Geometry.003"].location = (188.83331298828125, -39.56705856323242)
    gem_in_holder_1.nodes["Instance on Points.003"].location = (329.0, -155.8000030517578)
    gem_in_holder_1.nodes["Curve Circle.001"].location = (189.0, -35.79999923706055)
    gem_in_holder_1.nodes["Align Rotation to Vector.002"].location = (189.0, -435.79998779296875)
    gem_in_holder_1.nodes["Curve Tangent"].location = (189.0, -595.7999877929688)
    gem_in_holder_1.nodes["Join Geometry.004"].location = (2860.0, 280.0)
    gem_in_holder_1.nodes["Realize Instances.003"].location = (509.0, -155.8000030517578)
    gem_in_holder_1.nodes["Switch"].location = (509.0, -35.79998779296875)
    gem_in_holder_1.nodes["Group Input.001"].location = (29.0, -35.79998779296875)
    gem_in_holder_1.nodes["Group Input.002"].location = (29.0, -515.13330078125)
    gem_in_holder_1.nodes["Group Input.003"].location = (29.0, -95.80000305175781)
    gem_in_holder_1.nodes["Frame"].location = (-2249.0, 615.7999877929688)
    gem_in_holder_1.nodes["Frame.001"].location = (1151.0, 1015.7999877929688)
    gem_in_holder_1.nodes["Frame.002"].location = (-2709.0, -124.86666870117188)
    gem_in_holder_1.nodes["Frame.003"].location = (211.0, -24.19999885559082)
    gem_in_holder_1.nodes["Frame.004"].location = (875.6666870117188, -48.33333206176758)
    gem_in_holder_1.nodes["Frame.005"].location = (1271.0, -44.20000076293945)
    gem_in_holder_1.nodes["Store Named Attribute"].location = (2020.0, 460.0)
    gem_in_holder_1.nodes["Join Geometry.005"].location = (2380.0, 500.0)
    gem_in_holder_1.nodes["Store Named Attribute.001"].location = (869.0, -35.79998779296875)
    gem_in_holder_1.nodes["Mix"].location = (1549.0, -635.13330078125)
    gem_in_holder_1.nodes["Vector Math"].location = (1589.0, -295.1333312988281)
    gem_in_holder_1.nodes["Position"].location = (1189.0, -635.13330078125)
    gem_in_holder_1.nodes["Vector Math.001"].location = (1189.0, -695.13330078125)
    gem_in_holder_1.nodes["Map Range"].location = (1389.0, -635.13330078125)
    gem_in_holder_1.nodes["Group Input.004"].location = (1189.0, -815.13330078125)
    gem_in_holder_1.nodes["Store Named Attribute.002"].location = (2020.0, 160.0)
    gem_in_holder_1.nodes["Transform Geometry"].location = (2620.0, 360.0)
    gem_in_holder_1.nodes["Separate XYZ"].location = (789.0, -495.1333312988281)
    gem_in_holder_1.nodes["Combine XYZ"].location = (1129.0, -435.1333312988281)
    gem_in_holder_1.nodes["Math.002"].location = (949.0, -555.13330078125)
    gem_in_holder_1.nodes["Resample Curve"].location = (1069.0, -195.79998779296875)
    gem_in_holder_1.nodes["Resample Curve.001"].location = (2609.0, -55.133331298828125)
    gem_in_holder_1.nodes["Switch.001"].location = (3060.0, 460.0)
    gem_in_holder_1.nodes["Group Input.005"].location = (3060.0, 520.0)
    gem_in_holder_1.nodes["Switch.002"].location = (1769.0, -275.1333312988281)
    gem_in_holder_1.nodes["Evaluate at Index"].location = (1929.0, -275.1333312988281)
    gem_in_holder_1.nodes["Vector Math.002"].location = (2089.0, -275.1333312988281)
    gem_in_holder_1.nodes["Transform Geometry.001"].location = (389.0, -35.79998779296875)
    gem_in_holder_1.nodes["Attribute Statistic"].location = (2469.0, -255.13333129882812)
    gem_in_holder_1.nodes["Align Rotation to Vector"].location = (29.0, -155.79998779296875)
    gem_in_holder_1.nodes["Invert Rotation"].location = (229.0, -155.79998779296875)
    gem_in_holder_1.nodes["Frame.006"].location = (1311.0, -884.2000122070312)
    gem_in_holder_1.nodes["Store Named Attribute.003"].location = (549.0, -35.79998779296875)
    gem_in_holder_1.nodes["Reroute"].location = (315.669921875, -66.96894073486328)

    # Set dimensions
    gem_in_holder_1.nodes["Group Output"].width  = 140.0
    gem_in_holder_1.nodes["Group Output"].height = 100.0

    gem_in_holder_1.nodes["Group Input"].width  = 140.0
    gem_in_holder_1.nodes["Group Input"].height = 100.0

    gem_in_holder_1.nodes["Ico Sphere.001"].width  = 140.0
    gem_in_holder_1.nodes["Ico Sphere.001"].height = 100.0

    gem_in_holder_1.nodes["Dual Mesh"].width  = 140.0
    gem_in_holder_1.nodes["Dual Mesh"].height = 100.0

    gem_in_holder_1.nodes["Curve Circle"].width  = 140.0
    gem_in_holder_1.nodes["Curve Circle"].height = 100.0

    gem_in_holder_1.nodes["Curve to Mesh.002"].width  = 140.0
    gem_in_holder_1.nodes["Curve to Mesh.002"].height = 100.0

    gem_in_holder_1.nodes["Points"].width  = 140.0
    gem_in_holder_1.nodes["Points"].height = 100.0

    gem_in_holder_1.nodes["Random Value"].width  = 140.0
    gem_in_holder_1.nodes["Random Value"].height = 100.0

    gem_in_holder_1.nodes["Points to Curves"].width  = 140.0
    gem_in_holder_1.nodes["Points to Curves"].height = 100.0

    gem_in_holder_1.nodes["Gradient Texture"].width  = 140.0
    gem_in_holder_1.nodes["Gradient Texture"].height = 100.0

    gem_in_holder_1.nodes["Set Spline Cyclic"].width  = 140.0
    gem_in_holder_1.nodes["Set Spline Cyclic"].height = 100.0

    gem_in_holder_1.nodes["Set Spline Type"].width  = 140.0
    gem_in_holder_1.nodes["Set Spline Type"].height = 100.0

    gem_in_holder_1.nodes["Transform Geometry.005"].width  = 140.0
    gem_in_holder_1.nodes["Transform Geometry.005"].height = 100.0

    gem_in_holder_1.nodes["Points to Vertices"].width  = 140.0
    gem_in_holder_1.nodes["Points to Vertices"].height = 100.0

    gem_in_holder_1.nodes["Extrude Mesh.001"].width  = 140.0
    gem_in_holder_1.nodes["Extrude Mesh.001"].height = 100.0

    gem_in_holder_1.nodes["Repeat Input.001"].width  = 140.0
    gem_in_holder_1.nodes["Repeat Input.001"].height = 100.0

    gem_in_holder_1.nodes["Repeat Output.001"].width  = 140.0
    gem_in_holder_1.nodes["Repeat Output.001"].height = 100.0

    gem_in_holder_1.nodes["Noise Texture"].width  = 145.0
    gem_in_holder_1.nodes["Noise Texture"].height = 100.0

    gem_in_holder_1.nodes["Mesh to Curve.003"].width  = 140.0
    gem_in_holder_1.nodes["Mesh to Curve.003"].height = 100.0

    gem_in_holder_1.nodes["Curve to Mesh.003"].width  = 140.0
    gem_in_holder_1.nodes["Curve to Mesh.003"].height = 100.0

    gem_in_holder_1.nodes["Spline Parameter.003"].width  = 140.0
    gem_in_holder_1.nodes["Spline Parameter.003"].height = 100.0

    gem_in_holder_1.nodes["Float Curve"].width  = 240.0
    gem_in_holder_1.nodes["Float Curve"].height = 100.0

    gem_in_holder_1.nodes["Math"].width  = 140.0
    gem_in_holder_1.nodes["Math"].height = 100.0

    gem_in_holder_1.nodes["Points.001"].width  = 140.0
    gem_in_holder_1.nodes["Points.001"].height = 100.0

    gem_in_holder_1.nodes["Index"].width  = 140.0
    gem_in_holder_1.nodes["Index"].height = 100.0

    gem_in_holder_1.nodes["Capture Attribute.007"].width  = 140.0
    gem_in_holder_1.nodes["Capture Attribute.007"].height = 100.0

    gem_in_holder_1.nodes["Math.001"].width  = 140.0
    gem_in_holder_1.nodes["Math.001"].height = 100.0

    gem_in_holder_1.nodes["Transform Geometry.006"].width  = 140.0
    gem_in_holder_1.nodes["Transform Geometry.006"].height = 100.0

    gem_in_holder_1.nodes["Flip Faces.001"].width  = 140.0
    gem_in_holder_1.nodes["Flip Faces.001"].height = 100.0

    gem_in_holder_1.nodes["Join Geometry.003"].width  = 140.0
    gem_in_holder_1.nodes["Join Geometry.003"].height = 100.0

    gem_in_holder_1.nodes["Instance on Points.003"].width  = 140.0
    gem_in_holder_1.nodes["Instance on Points.003"].height = 100.0

    gem_in_holder_1.nodes["Curve Circle.001"].width  = 140.0
    gem_in_holder_1.nodes["Curve Circle.001"].height = 100.0

    gem_in_holder_1.nodes["Align Rotation to Vector.002"].width  = 140.0
    gem_in_holder_1.nodes["Align Rotation to Vector.002"].height = 100.0

    gem_in_holder_1.nodes["Curve Tangent"].width  = 140.0
    gem_in_holder_1.nodes["Curve Tangent"].height = 100.0

    gem_in_holder_1.nodes["Join Geometry.004"].width  = 140.0
    gem_in_holder_1.nodes["Join Geometry.004"].height = 100.0

    gem_in_holder_1.nodes["Realize Instances.003"].width  = 140.0
    gem_in_holder_1.nodes["Realize Instances.003"].height = 100.0

    gem_in_holder_1.nodes["Switch"].width  = 140.0
    gem_in_holder_1.nodes["Switch"].height = 100.0

    gem_in_holder_1.nodes["Group Input.001"].width  = 140.0
    gem_in_holder_1.nodes["Group Input.001"].height = 100.0

    gem_in_holder_1.nodes["Group Input.002"].width  = 140.0
    gem_in_holder_1.nodes["Group Input.002"].height = 100.0

    gem_in_holder_1.nodes["Group Input.003"].width  = 140.0
    gem_in_holder_1.nodes["Group Input.003"].height = 100.0

    gem_in_holder_1.nodes["Frame"].width  = 1618.0
    gem_in_holder_1.nodes["Frame"].height = 506.1333312988281

    gem_in_holder_1.nodes["Frame.001"].width  = 1038.0
    gem_in_holder_1.nodes["Frame.001"].height = 347.4666748046875

    gem_in_holder_1.nodes["Frame.002"].width  = 2778.0
    gem_in_holder_1.nodes["Frame.002"].height = 971.4666748046875

    gem_in_holder_1.nodes["Frame.003"].width  = 638.0
    gem_in_holder_1.nodes["Frame.003"].height = 594.13330078125

    gem_in_holder_1.nodes["Frame.004"].width  = 357.99993896484375
    gem_in_holder_1.nodes["Frame.004"].height = 416.6666564941406

    gem_in_holder_1.nodes["Frame.005"].width  = 678.0
    gem_in_holder_1.nodes["Frame.005"].height = 672.7999877929688

    gem_in_holder_1.nodes["Store Named Attribute"].width  = 140.0
    gem_in_holder_1.nodes["Store Named Attribute"].height = 100.0

    gem_in_holder_1.nodes["Join Geometry.005"].width  = 140.0
    gem_in_holder_1.nodes["Join Geometry.005"].height = 100.0

    gem_in_holder_1.nodes["Store Named Attribute.001"].width  = 140.0
    gem_in_holder_1.nodes["Store Named Attribute.001"].height = 100.0

    gem_in_holder_1.nodes["Mix"].width  = 140.0
    gem_in_holder_1.nodes["Mix"].height = 100.0

    gem_in_holder_1.nodes["Vector Math"].width  = 140.0
    gem_in_holder_1.nodes["Vector Math"].height = 100.0

    gem_in_holder_1.nodes["Position"].width  = 140.0
    gem_in_holder_1.nodes["Position"].height = 100.0

    gem_in_holder_1.nodes["Vector Math.001"].width  = 140.0
    gem_in_holder_1.nodes["Vector Math.001"].height = 100.0

    gem_in_holder_1.nodes["Map Range"].width  = 140.0
    gem_in_holder_1.nodes["Map Range"].height = 100.0

    gem_in_holder_1.nodes["Group Input.004"].width  = 140.0
    gem_in_holder_1.nodes["Group Input.004"].height = 100.0

    gem_in_holder_1.nodes["Store Named Attribute.002"].width  = 140.0
    gem_in_holder_1.nodes["Store Named Attribute.002"].height = 100.0

    gem_in_holder_1.nodes["Transform Geometry"].width  = 140.0
    gem_in_holder_1.nodes["Transform Geometry"].height = 100.0

    gem_in_holder_1.nodes["Separate XYZ"].width  = 140.0
    gem_in_holder_1.nodes["Separate XYZ"].height = 100.0

    gem_in_holder_1.nodes["Combine XYZ"].width  = 140.0
    gem_in_holder_1.nodes["Combine XYZ"].height = 100.0

    gem_in_holder_1.nodes["Math.002"].width  = 140.0
    gem_in_holder_1.nodes["Math.002"].height = 100.0

    gem_in_holder_1.nodes["Resample Curve"].width  = 140.0
    gem_in_holder_1.nodes["Resample Curve"].height = 100.0

    gem_in_holder_1.nodes["Resample Curve.001"].width  = 140.0
    gem_in_holder_1.nodes["Resample Curve.001"].height = 100.0

    gem_in_holder_1.nodes["Switch.001"].width  = 140.0
    gem_in_holder_1.nodes["Switch.001"].height = 100.0

    gem_in_holder_1.nodes["Group Input.005"].width  = 140.0
    gem_in_holder_1.nodes["Group Input.005"].height = 100.0

    gem_in_holder_1.nodes["Switch.002"].width  = 140.0
    gem_in_holder_1.nodes["Switch.002"].height = 100.0

    gem_in_holder_1.nodes["Evaluate at Index"].width  = 140.0
    gem_in_holder_1.nodes["Evaluate at Index"].height = 100.0

    gem_in_holder_1.nodes["Vector Math.002"].width  = 140.0
    gem_in_holder_1.nodes["Vector Math.002"].height = 100.0

    gem_in_holder_1.nodes["Transform Geometry.001"].width  = 140.0
    gem_in_holder_1.nodes["Transform Geometry.001"].height = 100.0

    gem_in_holder_1.nodes["Attribute Statistic"].width  = 140.0
    gem_in_holder_1.nodes["Attribute Statistic"].height = 100.0

    gem_in_holder_1.nodes["Align Rotation to Vector"].width  = 140.0
    gem_in_holder_1.nodes["Align Rotation to Vector"].height = 100.0

    gem_in_holder_1.nodes["Invert Rotation"].width  = 140.0
    gem_in_holder_1.nodes["Invert Rotation"].height = 100.0

    gem_in_holder_1.nodes["Frame.006"].width  = 718.0
    gem_in_holder_1.nodes["Frame.006"].height = 320.13336181640625

    gem_in_holder_1.nodes["Store Named Attribute.003"].width  = 140.0
    gem_in_holder_1.nodes["Store Named Attribute.003"].height = 100.0

    gem_in_holder_1.nodes["Reroute"].width  = 14.5
    gem_in_holder_1.nodes["Reroute"].height = 100.0


    # Initialize gem_in_holder_1 links

    # extrude_mesh_001.Top -> repeat_output_001.Top
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Extrude Mesh.001"].outputs[1],
        gem_in_holder_1.nodes["Repeat Output.001"].inputs[1]
    )
    # resample_curve.Curve -> curve_to_mesh_002.Profile Curve
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Resample Curve"].outputs[0],
        gem_in_holder_1.nodes["Curve to Mesh.002"].inputs[1]
    )
    # align_rotation_to_vector_002.Rotation -> instance_on_points_003.Rotation
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Align Rotation to Vector.002"].outputs[0],
        gem_in_holder_1.nodes["Instance on Points.003"].inputs[5]
    )
    # capture_attribute_007.Geometry -> points_to_vertices.Points
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Capture Attribute.007"].outputs[0],
        gem_in_holder_1.nodes["Points to Vertices"].inputs[0]
    )
    # vector_math.Vector -> extrude_mesh_001.Offset
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Vector Math"].outputs[0],
        gem_in_holder_1.nodes["Extrude Mesh.001"].inputs[2]
    )
    # points_001.Points -> capture_attribute_007.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Points.001"].outputs[0],
        gem_in_holder_1.nodes["Capture Attribute.007"].inputs[0]
    )
    # capture_attribute_007.Index -> math_001.Value
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Capture Attribute.007"].outputs[1],
        gem_in_holder_1.nodes["Math.001"].inputs[0]
    )
    # flip_faces_001.Mesh -> join_geometry_003.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Flip Faces.001"].outputs[0],
        gem_in_holder_1.nodes["Join Geometry.003"].inputs[0]
    )
    # curve_circle_001.Curve -> instance_on_points_003.Points
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Curve Circle.001"].outputs[0],
        gem_in_holder_1.nodes["Instance on Points.003"].inputs[0]
    )
    # set_spline_cyclic.Curve -> set_spline_type.Curve
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Set Spline Cyclic"].outputs[0],
        gem_in_holder_1.nodes["Set Spline Type"].inputs[0]
    )
    # join_geometry_003.Geometry -> instance_on_points_003.Instance
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Join Geometry.003"].outputs[0],
        gem_in_holder_1.nodes["Instance on Points.003"].inputs[2]
    )
    # points.Points -> points_to_curves.Points
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Points"].outputs[0],
        gem_in_holder_1.nodes["Points to Curves"].inputs[0]
    )
    # instance_on_points_003.Instances -> realize_instances_003.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Instance on Points.003"].outputs[0],
        gem_in_holder_1.nodes["Realize Instances.003"].inputs[0]
    )
    # curve_to_mesh_003.Mesh -> transform_geometry_006.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Curve to Mesh.003"].outputs[0],
        gem_in_holder_1.nodes["Transform Geometry.006"].inputs[0]
    )
    # index.Index -> capture_attribute_007.Index
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Index"].outputs[0],
        gem_in_holder_1.nodes["Capture Attribute.007"].inputs[1]
    )
    # points_to_curves.Curves -> set_spline_cyclic.Curve
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Points to Curves"].outputs[0],
        gem_in_holder_1.nodes["Set Spline Cyclic"].inputs[0]
    )
    # float_curve.Value -> math.Value
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Float Curve"].outputs[0],
        gem_in_holder_1.nodes["Math"].inputs[0]
    )
    # repeat_input_001.Top -> extrude_mesh_001.Selection
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Repeat Input.001"].outputs[2],
        gem_in_holder_1.nodes["Extrude Mesh.001"].inputs[1]
    )
    # math_001.Value -> noise_texture.W
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Math.001"].outputs[0],
        gem_in_holder_1.nodes["Noise Texture"].inputs[1]
    )
    # gradient_texture.Factor -> points_to_curves.Weight
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Gradient Texture"].outputs[1],
        gem_in_holder_1.nodes["Points to Curves"].inputs[2]
    )
    # extrude_mesh_001.Mesh -> repeat_output_001.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Extrude Mesh.001"].outputs[0],
        gem_in_holder_1.nodes["Repeat Output.001"].inputs[0]
    )
    # repeat_input_001.Geometry -> extrude_mesh_001.Mesh
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Repeat Input.001"].outputs[1],
        gem_in_holder_1.nodes["Extrude Mesh.001"].inputs[0]
    )
    # random_value.Value -> points.Position
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Random Value"].outputs[0],
        gem_in_holder_1.nodes["Points"].inputs[1]
    )
    # resample_curve_001.Curve -> curve_to_mesh_003.Curve
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Resample Curve.001"].outputs[0],
        gem_in_holder_1.nodes["Curve to Mesh.003"].inputs[0]
    )
    # curve_tangent.Tangent -> align_rotation_to_vector_002.Vector
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Curve Tangent"].outputs[0],
        gem_in_holder_1.nodes["Align Rotation to Vector.002"].inputs[2]
    )
    # curve_circle.Curve -> curve_to_mesh_002.Curve
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Curve Circle"].outputs[0],
        gem_in_holder_1.nodes["Curve to Mesh.002"].inputs[0]
    )
    # repeat_output_001.Geometry -> mesh_to_curve_003.Mesh
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Repeat Output.001"].outputs[0],
        gem_in_holder_1.nodes["Mesh to Curve.003"].inputs[0]
    )
    # points_to_vertices.Mesh -> repeat_input_001.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Points to Vertices"].outputs[0],
        gem_in_holder_1.nodes["Repeat Input.001"].inputs[1]
    )
    # ico_sphere_001.Mesh -> dual_mesh.Mesh
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Ico Sphere.001"].outputs[0],
        gem_in_holder_1.nodes["Dual Mesh"].inputs[0]
    )
    # reroute.Output -> curve_to_mesh_003.Profile Curve
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Reroute"].outputs[0],
        gem_in_holder_1.nodes["Curve to Mesh.003"].inputs[1]
    )
    # transform_geometry_006.Geometry -> flip_faces_001.Mesh
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Transform Geometry.006"].outputs[0],
        gem_in_holder_1.nodes["Flip Faces.001"].inputs[0]
    )
    # spline_parameter_003.Factor -> float_curve.Value
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Spline Parameter.003"].outputs[0],
        gem_in_holder_1.nodes["Float Curve"].inputs[1]
    )
    # math.Value -> curve_to_mesh_003.Scale
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Math"].outputs[0],
        gem_in_holder_1.nodes["Curve to Mesh.003"].inputs[2]
    )
    # switch_001.Output -> group_output.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Switch.001"].outputs[0],
        gem_in_holder_1.nodes["Group Output"].inputs[0]
    )
    # group_input.Count -> points.Count
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input"].outputs[4],
        gem_in_holder_1.nodes["Points"].inputs[0]
    )
    # group_input.Seed -> random_value.Seed
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input"].outputs[5],
        gem_in_holder_1.nodes["Random Value"].inputs[8]
    )
    # group_input.Gem Radius -> curve_circle.Radius
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input"].outputs[0],
        gem_in_holder_1.nodes["Curve Circle"].inputs[4]
    )
    # group_input.Scale -> curve_to_mesh_002.Scale
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input"].outputs[3],
        gem_in_holder_1.nodes["Curve to Mesh.002"].inputs[2]
    )
    # switch.Output -> transform_geometry_005.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Switch"].outputs[0],
        gem_in_holder_1.nodes["Transform Geometry.005"].inputs[0]
    )
    # dual_mesh.Dual Mesh -> switch.True
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Dual Mesh"].outputs[0],
        gem_in_holder_1.nodes["Switch"].inputs[2]
    )
    # ico_sphere_001.Mesh -> switch.False
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Ico Sphere.001"].outputs[0],
        gem_in_holder_1.nodes["Switch"].inputs[1]
    )
    # group_input_001.Gem Radius -> ico_sphere_001.Radius
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input.001"].outputs[0],
        gem_in_holder_1.nodes["Ico Sphere.001"].inputs[0]
    )
    # group_input_002.Strand Count -> points_001.Count
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input.002"].outputs[8],
        gem_in_holder_1.nodes["Points.001"].inputs[0]
    )
    # group_input_002.Split -> math_001.Value
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input.002"].outputs[9],
        gem_in_holder_1.nodes["Math.001"].inputs[1]
    )
    # group_input_002.Seed -> math_001.Value
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input.002"].outputs[10],
        gem_in_holder_1.nodes["Math.001"].inputs[2]
    )
    # group_input_003.Array Count -> curve_circle_001.Resolution
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input.003"].outputs[7],
        gem_in_holder_1.nodes["Curve Circle.001"].inputs[0]
    )
    # store_named_attribute.Geometry -> join_geometry_005.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Store Named Attribute"].outputs[0],
        gem_in_holder_1.nodes["Join Geometry.005"].inputs[0]
    )
    # transform_geometry_005.Geometry -> store_named_attribute_001.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Transform Geometry.005"].outputs[0],
        gem_in_holder_1.nodes["Store Named Attribute.001"].inputs[0]
    )
    # group_input_001.Gem Material -> store_named_attribute_001.Name
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input.001"].outputs[1],
        gem_in_holder_1.nodes["Store Named Attribute.001"].inputs[2]
    )
    # group_input_001.Gem Dual Mesh -> switch.Switch
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input.001"].outputs[2],
        gem_in_holder_1.nodes["Switch"].inputs[0]
    )
    # combine_xyz.Vector -> vector_math.Vector
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Combine XYZ"].outputs[0],
        gem_in_holder_1.nodes["Vector Math"].inputs[0]
    )
    # mix.Result -> vector_math.Vector
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Mix"].outputs[1],
        gem_in_holder_1.nodes["Vector Math"].inputs[1]
    )
    # position.Position -> vector_math_001.Vector
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Position"].outputs[0],
        gem_in_holder_1.nodes["Vector Math.001"].inputs[0]
    )
    # vector_math_001.Value -> map_range.Value
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Vector Math.001"].outputs[1],
        gem_in_holder_1.nodes["Map Range"].inputs[0]
    )
    # map_range.Result -> mix.Factor
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Map Range"].outputs[0],
        gem_in_holder_1.nodes["Mix"].inputs[0]
    )
    # group_input_004.Gem Radius -> map_range.From Min
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input.004"].outputs[0],
        gem_in_holder_1.nodes["Map Range"].inputs[1]
    )
    # curve_to_mesh_002.Mesh -> store_named_attribute.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Curve to Mesh.002"].outputs[0],
        gem_in_holder_1.nodes["Store Named Attribute"].inputs[0]
    )
    # realize_instances_003.Geometry -> store_named_attribute_002.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Realize Instances.003"].outputs[0],
        gem_in_holder_1.nodes["Store Named Attribute.002"].inputs[0]
    )
    # join_geometry_005.Geometry -> transform_geometry.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Join Geometry.005"].outputs[0],
        gem_in_holder_1.nodes["Transform Geometry"].inputs[0]
    )
    # store_named_attribute_002.Geometry -> join_geometry_004.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Store Named Attribute.002"].outputs[0],
        gem_in_holder_1.nodes["Join Geometry.004"].inputs[0]
    )
    # noise_texture.Color -> separate_xyz.Vector
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Noise Texture"].outputs[1],
        gem_in_holder_1.nodes["Separate XYZ"].inputs[0]
    )
    # separate_xyz.X -> combine_xyz.X
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Separate XYZ"].outputs[0],
        gem_in_holder_1.nodes["Combine XYZ"].inputs[0]
    )
    # separate_xyz.Y -> combine_xyz.Y
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Separate XYZ"].outputs[1],
        gem_in_holder_1.nodes["Combine XYZ"].inputs[1]
    )
    # separate_xyz.Z -> math_002.Value
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Separate XYZ"].outputs[2],
        gem_in_holder_1.nodes["Math.002"].inputs[0]
    )
    # math_002.Value -> combine_xyz.Z
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Math.002"].outputs[0],
        gem_in_holder_1.nodes["Combine XYZ"].inputs[2]
    )
    # set_spline_type.Curve -> resample_curve.Curve
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Set Spline Type"].outputs[0],
        gem_in_holder_1.nodes["Resample Curve"].inputs[0]
    )
    # mesh_to_curve_003.Curve -> resample_curve_001.Curve
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Mesh to Curve.003"].outputs[0],
        gem_in_holder_1.nodes["Resample Curve.001"].inputs[0]
    )
    # join_geometry_004.Geometry -> switch_001.True
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Join Geometry.004"].outputs[0],
        gem_in_holder_1.nodes["Switch.001"].inputs[2]
    )
    # join_geometry_005.Geometry -> switch_001.False
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Join Geometry.005"].outputs[0],
        gem_in_holder_1.nodes["Switch.001"].inputs[1]
    )
    # group_input_005.Wings -> switch_001.Switch
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Group Input.005"].outputs[6],
        gem_in_holder_1.nodes["Switch.001"].inputs[0]
    )
    # store_named_attribute_003.Geometry -> group_output.Wing
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Store Named Attribute.003"].outputs[0],
        gem_in_holder_1.nodes["Group Output"].inputs[3]
    )
    # repeat_input_001.Iteration -> switch_002.Switch
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Repeat Input.001"].outputs[0],
        gem_in_holder_1.nodes["Switch.002"].inputs[0]
    )
    # vector_math.Vector -> switch_002.False
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Vector Math"].outputs[0],
        gem_in_holder_1.nodes["Switch.002"].inputs[1]
    )
    # switch_002.Output -> evaluate_at_index.Value
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Switch.002"].outputs[0],
        gem_in_holder_1.nodes["Evaluate at Index"].inputs[0]
    )
    # vector_math_002.Vector -> repeat_output_001.Value
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Vector Math.002"].outputs[0],
        gem_in_holder_1.nodes["Repeat Output.001"].inputs[2]
    )
    # evaluate_at_index.Value -> vector_math_002.Vector
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Evaluate at Index"].outputs[0],
        gem_in_holder_1.nodes["Vector Math.002"].inputs[0]
    )
    # repeat_input_001.Value -> vector_math_002.Vector
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Repeat Input.001"].outputs[3],
        gem_in_holder_1.nodes["Vector Math.002"].inputs[1]
    )
    # curve_to_mesh_003.Mesh -> transform_geometry_001.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Curve to Mesh.003"].outputs[0],
        gem_in_holder_1.nodes["Transform Geometry.001"].inputs[0]
    )
    # repeat_output_001.Geometry -> attribute_statistic.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Repeat Output.001"].outputs[0],
        gem_in_holder_1.nodes["Attribute Statistic"].inputs[0]
    )
    # repeat_output_001.Value -> attribute_statistic.Attribute
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Repeat Output.001"].outputs[2],
        gem_in_holder_1.nodes["Attribute Statistic"].inputs[2]
    )
    # attribute_statistic.Min -> align_rotation_to_vector.Vector
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Attribute Statistic"].outputs[3],
        gem_in_holder_1.nodes["Align Rotation to Vector"].inputs[2]
    )
    # invert_rotation.Rotation -> transform_geometry_001.Rotation
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Invert Rotation"].outputs[0],
        gem_in_holder_1.nodes["Transform Geometry.001"].inputs[3]
    )
    # align_rotation_to_vector.Rotation -> invert_rotation.Rotation
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Align Rotation to Vector"].outputs[0],
        gem_in_holder_1.nodes["Invert Rotation"].inputs[0]
    )
    # transform_geometry_001.Geometry -> store_named_attribute_003.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Transform Geometry.001"].outputs[0],
        gem_in_holder_1.nodes["Store Named Attribute.003"].inputs[0]
    )
    # resample_curve_001.Curve -> group_output.Wing Curve
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Resample Curve.001"].outputs[0],
        gem_in_holder_1.nodes["Group Output"].inputs[4]
    )
    # resample_curve.Curve -> reroute.Input
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Resample Curve"].outputs[0],
        gem_in_holder_1.nodes["Reroute"].inputs[0]
    )
    # reroute.Output -> group_output.Profile Curve
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Reroute"].outputs[0],
        gem_in_holder_1.nodes["Group Output"].inputs[1]
    )
    # math.Value -> group_output.Profile Scale
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Math"].outputs[0],
        gem_in_holder_1.nodes["Group Output"].inputs[2]
    )
    # curve_to_mesh_003.Mesh -> join_geometry_003.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Curve to Mesh.003"].outputs[0],
        gem_in_holder_1.nodes["Join Geometry.003"].inputs[0]
    )
    # store_named_attribute_001.Geometry -> join_geometry_005.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Store Named Attribute.001"].outputs[0],
        gem_in_holder_1.nodes["Join Geometry.005"].inputs[0]
    )
    # transform_geometry.Geometry -> join_geometry_004.Geometry
    gem_in_holder_1.links.new(
        gem_in_holder_1.nodes["Transform Geometry"].outputs[0],
        gem_in_holder_1.nodes["Join Geometry.004"].inputs[0]
    )

    return gem_in_holder_1


def is_edge_boundary_1_node_group_1(node_tree_names: dict[typing.Callable, str]):
    """Initialize Is Edge Boundary node group"""
    is_edge_boundary_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Is Edge Boundary")

    is_edge_boundary_1.color_tag = 'INPUT'
    is_edge_boundary_1.description = ""
    is_edge_boundary_1.default_group_node_width = 140
    is_edge_boundary_1.show_modifier_manage_panel = True

    # is_edge_boundary_1 interface

    # Socket Is Edge Boundary
    is_edge_boundary_socket = is_edge_boundary_1.interface.new_socket(name="Is Edge Boundary", in_out='OUTPUT', socket_type='NodeSocketBool')
    is_edge_boundary_socket.default_value = False
    is_edge_boundary_socket.attribute_domain = 'POINT'
    is_edge_boundary_socket.description = "Selection of edges that are part of the boundary of a mesh surface"
    is_edge_boundary_socket.default_input = 'VALUE'
    is_edge_boundary_socket.structure_type = 'AUTO'

    # Initialize is_edge_boundary_1 nodes

    # Node Group Output
    group_output = is_edge_boundary_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Edge Neighbors
    edge_neighbors = is_edge_boundary_1.nodes.new("GeometryNodeInputMeshEdgeNeighbors")
    edge_neighbors.name = "Edge Neighbors"

    # Node Compare
    compare = is_edge_boundary_1.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'INT'
    compare.mode = 'ELEMENT'
    compare.operation = 'EQUAL'
    # B_INT
    compare.inputs[3].default_value = 1

    # Node Evaluate on Domain
    evaluate_on_domain = is_edge_boundary_1.nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.name = "Evaluate on Domain"
    evaluate_on_domain.data_type = 'BOOLEAN'
    evaluate_on_domain.domain = 'EDGE'

    # Set locations
    is_edge_boundary_1.nodes["Group Output"].location = (320.0, 0.0)
    is_edge_boundary_1.nodes["Edge Neighbors"].location = (-279.9999694824219, 0.0)
    is_edge_boundary_1.nodes["Compare"].location = (-80.0, 0.0)
    is_edge_boundary_1.nodes["Evaluate on Domain"].location = (119.99999237060547, 0.0)

    # Set dimensions
    is_edge_boundary_1.nodes["Group Output"].width  = 140.0
    is_edge_boundary_1.nodes["Group Output"].height = 100.0

    is_edge_boundary_1.nodes["Edge Neighbors"].width  = 140.0
    is_edge_boundary_1.nodes["Edge Neighbors"].height = 100.0

    is_edge_boundary_1.nodes["Compare"].width  = 140.0
    is_edge_boundary_1.nodes["Compare"].height = 100.0

    is_edge_boundary_1.nodes["Evaluate on Domain"].width  = 140.0
    is_edge_boundary_1.nodes["Evaluate on Domain"].height = 100.0


    # Initialize is_edge_boundary_1 links

    # edge_neighbors.Face Count -> compare.A
    is_edge_boundary_1.links.new(
        is_edge_boundary_1.nodes["Edge Neighbors"].outputs[0],
        is_edge_boundary_1.nodes["Compare"].inputs[2]
    )
    # evaluate_on_domain.Value -> group_output.Is Edge Boundary
    is_edge_boundary_1.links.new(
        is_edge_boundary_1.nodes["Evaluate on Domain"].outputs[0],
        is_edge_boundary_1.nodes["Group Output"].inputs[0]
    )
    # compare.Result -> evaluate_on_domain.Value
    is_edge_boundary_1.links.new(
        is_edge_boundary_1.nodes["Compare"].outputs[0],
        is_edge_boundary_1.nodes["Evaluate on Domain"].inputs[0]
    )

    return is_edge_boundary_1


def swap_attr_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Swap Attr node group"""
    swap_attr_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Swap Attr")

    swap_attr_1.color_tag = 'NONE'
    swap_attr_1.description = ""
    swap_attr_1.default_group_node_width = 140
    swap_attr_1.show_modifier_manage_panel = True

    # swap_attr_1 interface

    # Socket Geometry
    geometry_socket = swap_attr_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Geometry
    geometry_socket_1 = swap_attr_1.interface.new_socket(name="Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'
    geometry_socket_1.description = "Geometry to store a new attribute with the given name on"
    geometry_socket_1.default_input = 'VALUE'
    geometry_socket_1.structure_type = 'AUTO'

    # Socket ID
    id_socket = swap_attr_1.interface.new_socket(name="ID", in_out='INPUT', socket_type='NodeSocketInt')
    id_socket.default_value = 0
    id_socket.min_value = -2147483648
    id_socket.max_value = 2147483647
    id_socket.subtype = 'NONE'
    id_socket.attribute_domain = 'POINT'
    id_socket.hide_value = True
    id_socket.default_input = 'ID_OR_INDEX'
    id_socket.structure_type = 'AUTO'

    # Socket Old
    old_socket = swap_attr_1.interface.new_socket(name="Old", in_out='INPUT', socket_type='NodeSocketString')
    old_socket.default_value = "ruby"
    old_socket.subtype = 'NONE'
    old_socket.attribute_domain = 'POINT'
    old_socket.default_input = 'VALUE'
    old_socket.structure_type = 'AUTO'
    old_socket.optional_label = True

    # Socket New
    new_socket = swap_attr_1.interface.new_socket(name="New", in_out='INPUT', socket_type='NodeSocketString')
    new_socket.default_value = "saphire"
    new_socket.subtype = 'NONE'
    new_socket.attribute_domain = 'POINT'
    new_socket.default_input = 'VALUE'
    new_socket.structure_type = 'AUTO'
    new_socket.optional_label = True

    # Initialize swap_attr_1 nodes

    # Node Group Output
    group_output = swap_attr_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Group Input
    group_input = swap_attr_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    # Node Store Named Attribute.001
    store_named_attribute_001 = swap_attr_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.data_type = 'BOOLEAN'
    store_named_attribute_001.domain = 'POINT'
    # Value
    store_named_attribute_001.inputs[3].default_value = True

    # Node Random Value.001
    random_value_001 = swap_attr_1.nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.data_type = 'BOOLEAN'
    # Probability
    random_value_001.inputs[6].default_value = 0.5
    # Seed
    random_value_001.inputs[8].default_value = 0

    # Node Boolean Math.002
    boolean_math_002 = swap_attr_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.operation = 'AND'

    # Node Named Attribute
    named_attribute = swap_attr_1.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.data_type = 'BOOLEAN'

    # Node Store Named Attribute.002
    store_named_attribute_002 = swap_attr_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.data_type = 'BOOLEAN'
    store_named_attribute_002.domain = 'POINT'
    # Value
    store_named_attribute_002.inputs[3].default_value = False

    # Set locations
    swap_attr_1.nodes["Group Output"].location = (430.0, 0.0)
    swap_attr_1.nodes["Group Input"].location = (-440.0, 0.0)
    swap_attr_1.nodes["Store Named Attribute.001"].location = (80.0, 140.0)
    swap_attr_1.nodes["Random Value.001"].location = (-240.0, 20.0)
    swap_attr_1.nodes["Boolean Math.002"].location = (-80.0, 20.0)
    swap_attr_1.nodes["Named Attribute"].location = (-240.0, -140.0)
    swap_attr_1.nodes["Store Named Attribute.002"].location = (240.0, 140.0)

    # Set dimensions
    swap_attr_1.nodes["Group Output"].width  = 140.0
    swap_attr_1.nodes["Group Output"].height = 100.0

    swap_attr_1.nodes["Group Input"].width  = 140.0
    swap_attr_1.nodes["Group Input"].height = 100.0

    swap_attr_1.nodes["Store Named Attribute.001"].width  = 140.0
    swap_attr_1.nodes["Store Named Attribute.001"].height = 100.0

    swap_attr_1.nodes["Random Value.001"].width  = 140.0
    swap_attr_1.nodes["Random Value.001"].height = 100.0

    swap_attr_1.nodes["Boolean Math.002"].width  = 140.0
    swap_attr_1.nodes["Boolean Math.002"].height = 100.0

    swap_attr_1.nodes["Named Attribute"].width  = 140.0
    swap_attr_1.nodes["Named Attribute"].height = 100.0

    swap_attr_1.nodes["Store Named Attribute.002"].width  = 140.0
    swap_attr_1.nodes["Store Named Attribute.002"].height = 100.0


    # Initialize swap_attr_1 links

    # boolean_math_002.Boolean -> store_named_attribute_001.Selection
    swap_attr_1.links.new(
        swap_attr_1.nodes["Boolean Math.002"].outputs[0],
        swap_attr_1.nodes["Store Named Attribute.001"].inputs[1]
    )
    # named_attribute.Attribute -> boolean_math_002.Boolean
    swap_attr_1.links.new(
        swap_attr_1.nodes["Named Attribute"].outputs[0],
        swap_attr_1.nodes["Boolean Math.002"].inputs[1]
    )
    # random_value_001.Value -> boolean_math_002.Boolean
    swap_attr_1.links.new(
        swap_attr_1.nodes["Random Value.001"].outputs[3],
        swap_attr_1.nodes["Boolean Math.002"].inputs[0]
    )
    # store_named_attribute_001.Geometry -> store_named_attribute_002.Geometry
    swap_attr_1.links.new(
        swap_attr_1.nodes["Store Named Attribute.001"].outputs[0],
        swap_attr_1.nodes["Store Named Attribute.002"].inputs[0]
    )
    # boolean_math_002.Boolean -> store_named_attribute_002.Selection
    swap_attr_1.links.new(
        swap_attr_1.nodes["Boolean Math.002"].outputs[0],
        swap_attr_1.nodes["Store Named Attribute.002"].inputs[1]
    )
    # group_input.Geometry -> store_named_attribute_001.Geometry
    swap_attr_1.links.new(
        swap_attr_1.nodes["Group Input"].outputs[0],
        swap_attr_1.nodes["Store Named Attribute.001"].inputs[0]
    )
    # group_input.ID -> random_value_001.ID
    swap_attr_1.links.new(
        swap_attr_1.nodes["Group Input"].outputs[1],
        swap_attr_1.nodes["Random Value.001"].inputs[7]
    )
    # store_named_attribute_002.Geometry -> group_output.Geometry
    swap_attr_1.links.new(
        swap_attr_1.nodes["Store Named Attribute.002"].outputs[0],
        swap_attr_1.nodes["Group Output"].inputs[0]
    )
    # group_input.Old -> named_attribute.Name
    swap_attr_1.links.new(
        swap_attr_1.nodes["Group Input"].outputs[2],
        swap_attr_1.nodes["Named Attribute"].inputs[0]
    )
    # group_input.Old -> store_named_attribute_002.Name
    swap_attr_1.links.new(
        swap_attr_1.nodes["Group Input"].outputs[2],
        swap_attr_1.nodes["Store Named Attribute.002"].inputs[2]
    )
    # group_input.New -> store_named_attribute_001.Name
    swap_attr_1.links.new(
        swap_attr_1.nodes["Group Input"].outputs[3],
        swap_attr_1.nodes["Store Named Attribute.001"].inputs[2]
    )

    return swap_attr_1


def neck_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Neck node group"""
    neck_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Neck")

    neck_1.color_tag = 'NONE'
    neck_1.description = ""
    neck_1.default_group_node_width = 140
    neck_1.show_modifier_manage_panel = True

    # neck_1 interface

    # Socket Mesh
    mesh_socket = neck_1.interface.new_socket(name="Mesh", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    mesh_socket.attribute_domain = 'POINT'
    mesh_socket.default_input = 'VALUE'
    mesh_socket.structure_type = 'AUTO'

    # Socket Decor
    decor_socket = neck_1.interface.new_socket(name="Decor", in_out='INPUT', socket_type='NodeSocketBool')
    decor_socket.default_value = False
    decor_socket.attribute_domain = 'POINT'
    decor_socket.default_input = 'VALUE'
    decor_socket.structure_type = 'AUTO'

    # Initialize neck_1 nodes

    # Node Group Output
    group_output = neck_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Quadratic Bézier.003
    quadratic_b_zier_003 = neck_1.nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_b_zier_003.name = "Quadratic Bézier.003"
    # Resolution
    quadratic_b_zier_003.inputs[0].default_value = 40
    # Start
    quadratic_b_zier_003.inputs[1].default_value = (0.0, -0.13999998569488525, 0.3499999940395355)
    # Middle
    quadratic_b_zier_003.inputs[2].default_value = (0.0, -0.10000000149011612, 0.39500001072883606)

    # Node Bi-Rail Loft.001
    bi_rail_loft_001 = neck_1.nodes.new("GeometryNodeGroup")
    bi_rail_loft_001.name = "Bi-Rail Loft.001"
    bi_rail_loft_001.node_tree = bpy.data.node_groups[node_tree_names[bi_rail_loft_1_node_group]]
    # Socket_12
    bi_rail_loft_001.inputs[3].default_value = 0
    # Socket_4
    bi_rail_loft_001.inputs[4].default_value = 'Resolution'
    # Socket_13
    bi_rail_loft_001.inputs[5].default_value = 0.009999999776482582
    # Socket_3
    bi_rail_loft_001.inputs[6].default_value = 0.029999999329447746
    # Socket_5
    bi_rail_loft_001.inputs[7].default_value = 42
    # Socket_14
    bi_rail_loft_001.inputs[8].default_value = 148

    # Node Quadratic Bézier.004
    quadratic_b_zier_004 = neck_1.nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_b_zier_004.name = "Quadratic Bézier.004"
    # Resolution
    quadratic_b_zier_004.inputs[0].default_value = 40
    # Middle
    quadratic_b_zier_004.inputs[2].default_value = (0.0, -0.07999999821186066, 0.4399999976158142)
    # End
    quadratic_b_zier_004.inputs[3].default_value = (0.0, -0.08999999612569809, 0.45000001788139343)

    # Node Group.002
    group_002 = neck_1.nodes.new("GeometryNodeGroup")
    group_002.name = "Group.002"
    group_002.node_tree = bpy.data.node_groups[node_tree_names[join_splines_1_node_group]]

    # Node Join Geometry.005
    join_geometry_005 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"

    # Node Vector
    vector = neck_1.nodes.new("FunctionNodeInputVector")
    vector.name = "Vector"
    vector.vector = (0.0, -0.08999999612569809, 0.42000001668930054)

    # Node Frame.006
    frame_006 = neck_1.nodes.new("NodeFrame")
    frame_006.label = "Centre Profile"
    frame_006.name = "Frame.006"
    frame_006.label_size = 20
    frame_006.shrink = True

    # Node Quadratic Bézier.006
    quadratic_b_zier_006 = neck_1.nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_b_zier_006.name = "Quadratic Bézier.006"
    # Resolution
    quadratic_b_zier_006.inputs[0].default_value = 40
    # Start
    quadratic_b_zier_006.inputs[1].default_value = (-0.15000000596046448, 0.0, 0.429999977350235)
    # Middle
    quadratic_b_zier_006.inputs[2].default_value = (-0.10000000894069672, 0.0, 0.44999998807907104)

    # Node Quadratic Bézier.007
    quadratic_b_zier_007 = neck_1.nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_b_zier_007.name = "Quadratic Bézier.007"
    # Resolution
    quadratic_b_zier_007.inputs[0].default_value = 40
    # Middle
    quadratic_b_zier_007.inputs[2].default_value = (-0.0650000050663948, 0.0, 0.4899999797344208)
    # End
    quadratic_b_zier_007.inputs[3].default_value = (-0.07500000298023224, 0.0, 0.5)

    # Node Group.003
    group_003 = neck_1.nodes.new("GeometryNodeGroup")
    group_003.name = "Group.003"
    group_003.node_tree = bpy.data.node_groups[node_tree_names[join_splines_1_node_group]]

    # Node Join Geometry.006
    join_geometry_006 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"

    # Node Vector.001
    vector_001 = neck_1.nodes.new("FunctionNodeInputVector")
    vector_001.name = "Vector.001"
    vector_001.vector = (-0.08500001579523087, 0.0, 0.4699999988079071)

    # Node Frame.007
    frame_007 = neck_1.nodes.new("NodeFrame")
    frame_007.label = "Side Profile"
    frame_007.name = "Frame.007"
    frame_007.label_size = 20
    frame_007.shrink = True

    # Node Join Geometry.008
    join_geometry_008 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_008.name = "Join Geometry.008"

    # Node Transform Geometry.002
    transform_geometry_002 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    # Mode
    transform_geometry_002.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_002.inputs[2].default_value = (0.0, -0.019999999552965164, 0.4800000488758087)
    # Rotation
    transform_geometry_002.inputs[3].default_value = (0.4064871668815613, 0.0, 0.0)
    # Scale
    transform_geometry_002.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Transform Geometry.003
    transform_geometry_003 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    # Mode
    transform_geometry_003.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_003.inputs[2].default_value = (0.0, 0.0, 0.3700000047683716)
    # Rotation
    transform_geometry_003.inputs[3].default_value = (0.15620698034763336, 0.0, 0.0)
    # Scale
    transform_geometry_003.inputs[4].default_value = (1.2599999904632568, 1.0, 1.0)

    # Node Curve Circle
    curve_circle = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle.name = "Curve Circle"
    curve_circle.mode = 'RADIUS'
    # Radius
    curve_circle.inputs[4].default_value = 0.08000004291534424

    # Node Curve Circle.001
    curve_circle_001 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.name = "Curve Circle.001"
    curve_circle_001.mode = 'RADIUS'
    # Radius
    curve_circle_001.inputs[4].default_value = 0.12999996542930603

    # Node Set Position
    set_position = neck_1.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Position
    set_position.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Position
    position = neck_1.nodes.new("GeometryNodeInputPosition")
    position.name = "Position"

    # Node Separate XYZ
    separate_xyz = neck_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"
    separate_xyz.outputs[0].hide = True
    separate_xyz.outputs[2].hide = True

    # Node Map Range
    map_range = neck_1.nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.clamp = False
    map_range.data_type = 'FLOAT'
    map_range.interpolation_type = 'LINEAR'
    # From Min
    map_range.inputs[1].default_value = -0.14000000059604645
    # From Max
    map_range.inputs[2].default_value = 0.14000000059604645
    # To Min
    map_range.inputs[3].default_value = 0.0
    # To Max
    map_range.inputs[4].default_value = 1.0

    # Node Frame.008
    frame_008 = neck_1.nodes.new("NodeFrame")
    frame_008.label = "Profiles"
    frame_008.name = "Frame.008"
    frame_008.label_size = 20
    frame_008.shrink = True

    # Node Float Curve.001
    float_curve_001 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_001.name = "Float Curve.001"
    # Mapping settings
    float_curve_001.mapping.extend = 'EXTRAPOLATED'
    float_curve_001.mapping.tone = 'STANDARD'
    float_curve_001.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_001.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_001.mapping.clip_min_x = 0.0
    float_curve_001.mapping.clip_min_y = 0.0
    float_curve_001.mapping.clip_max_x = 1.0
    float_curve_001.mapping.clip_max_y = 1.0
    float_curve_001.mapping.use_clip = True
    # Curve 0
    float_curve_001_curve_0 = float_curve_001.mapping.curves[0]
    float_curve_001_curve_0_point_0 = float_curve_001_curve_0.points[0]
    float_curve_001_curve_0_point_0.location = (0.0, 0.0)
    float_curve_001_curve_0_point_0.handle_type = 'AUTO'
    float_curve_001_curve_0_point_1 = float_curve_001_curve_0.points[1]
    float_curve_001_curve_0_point_1.location = (0.6404833793640137, 0.06513792276382446)
    float_curve_001_curve_0_point_1.handle_type = 'AUTO'
    float_curve_001_curve_0_point_2 = float_curve_001_curve_0.points.new(1.0, 0.0)
    float_curve_001_curve_0_point_2.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_001.mapping.update()
    # Factor
    float_curve_001.inputs[0].default_value = 1.0

    # Node Combine XYZ
    combine_xyz = neck_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    # X
    combine_xyz.inputs[0].default_value = 0.0
    # Y
    combine_xyz.inputs[1].default_value = 0.0

    # Node Transform Geometry.004
    transform_geometry_004 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    transform_geometry_004.inputs[1].hide = True
    transform_geometry_004.inputs[2].hide = True
    transform_geometry_004.inputs[4].hide = True
    transform_geometry_004.inputs[5].hide = True
    # Mode
    transform_geometry_004.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_004.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_004.inputs[3].default_value = (0.0, 0.0, 1.5707963705062866)
    # Scale
    transform_geometry_004.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Transform Geometry.005
    transform_geometry_005 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_005.name = "Transform Geometry.005"
    transform_geometry_005.inputs[1].hide = True
    transform_geometry_005.inputs[2].hide = True
    transform_geometry_005.inputs[4].hide = True
    transform_geometry_005.inputs[5].hide = True
    # Mode
    transform_geometry_005.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_005.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_005.inputs[3].default_value = (0.0, 0.0, 1.5707963705062866)
    # Scale
    transform_geometry_005.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Closure Input.001
    closure_input_001 = neck_1.nodes.new("NodeClosureInput")
    closure_input_001.name = "Closure Input.001"
    # Node Closure Output.001
    closure_output_001 = neck_1.nodes.new("NodeClosureOutput")
    closure_output_001.name = "Closure Output.001"
    closure_output_001.active_input_index = 0
    closure_output_001.active_output_index = 0
    closure_output_001.define_signature = False
    closure_output_001.input_items.clear()
    closure_output_001.input_items.new('FLOAT', "Factor")
    closure_output_001.input_items[0].structure_type = 'AUTO'
    closure_output_001.output_items.clear()
    closure_output_001.output_items.new('FLOAT', "Factor")
    closure_output_001.output_items[0].structure_type = 'AUTO'

    # Node Math
    math = neck_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'PINGPONG'
    math.use_clamp = False
    # Value_001
    math.inputs[1].default_value = 0.25

    # Node Math.001
    math_001 = neck_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    # Value_001
    math_001.inputs[1].default_value = 4.0

    # Node Transform Geometry.001
    transform_geometry_001 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    # Mode
    transform_geometry_001.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_001.inputs[3].default_value = (1.5446162223815918, 0.0, 0.0)
    # Scale
    transform_geometry_001.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Transform Geometry.006
    transform_geometry_006 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_006.name = "Transform Geometry.006"
    # Mode
    transform_geometry_006.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_006.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_006.inputs[3].default_value = (0.0, 1.5707963705062866, 0.0)
    # Scale
    transform_geometry_006.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Integer
    integer = neck_1.nodes.new("FunctionNodeInputInt")
    integer.name = "Integer"
    integer.integer = 73

    # Node Frame.009
    frame_009 = neck_1.nodes.new("NodeFrame")
    frame_009.label = "Neck Rails"
    frame_009.name = "Frame.009"
    frame_009.label_size = 20
    frame_009.shrink = True

    # Node Frame.010
    frame_010 = neck_1.nodes.new("NodeFrame")
    frame_010.label = "Neck"
    frame_010.name = "Frame.010"
    frame_010.label_size = 20
    frame_010.shrink = True

    # Node Delete Geometry
    delete_geometry = neck_1.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.domain = 'FACE'
    delete_geometry.mode = 'ALL'

    # Node Position.001
    position_001 = neck_1.nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"

    # Node Separate XYZ.001
    separate_xyz_001 = neck_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_001.name = "Separate XYZ.001"

    # Node Compare
    compare = neck_1.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'FLOAT'
    compare.mode = 'ELEMENT'
    compare.operation = 'GREATER_EQUAL'
    # B
    compare.inputs[1].default_value = 0.0

    # Node Pipes
    pipes = neck_1.nodes.new("GeometryNodeGroup")
    pipes.name = "Pipes"
    pipes.node_tree = bpy.data.node_groups[node_tree_names[pipes_1_node_group]]

    # Node Join Geometry
    join_geometry = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"

    # Node Separate XYZ.002
    separate_xyz_002 = neck_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_002.name = "Separate XYZ.002"
    separate_xyz_002.outputs[1].hide = True
    separate_xyz_002.outputs[2].hide = True

    # Node Compare.001
    compare_001 = neck_1.nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.data_type = 'FLOAT'
    compare_001.mode = 'ELEMENT'
    compare_001.operation = 'EQUAL'
    # B
    compare_001.inputs[1].default_value = 0.8799999356269836
    # Epsilon
    compare_001.inputs[12].default_value = 0.02099999599158764

    # Node Separate Geometry
    separate_geometry = neck_1.nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.domain = 'POINT'

    # Node Join Geometry.001
    join_geometry_001 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"

    # Node Frame
    frame = neck_1.nodes.new("NodeFrame")
    frame.label = "Pipes"
    frame.name = "Frame"
    frame.label_size = 20
    frame.shrink = True

    # Node Rivet
    rivet = neck_1.nodes.new("GeometryNodeGroup")
    rivet.name = "Rivet"
    rivet.node_tree = bpy.data.node_groups[node_tree_names[rivet_1_node_group]]
    # Socket_2
    rivet.inputs[1].default_value = False
    # Socket_3
    rivet.inputs[2].default_value = -1.059999942779541
    # Socket_4
    rivet.inputs[3].default_value = 0.9399999976158142

    # Node Realize Instances
    realize_instances = neck_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0

    # Node Set Shade Smooth
    set_shade_smooth = neck_1.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.domain = 'FACE'
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True

    # Node Join Geometry.002
    join_geometry_002 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"

    # Node Switch
    switch = neck_1.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'GEOMETRY'

    # Node Group Input
    group_input = neck_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[1].hide = True

    # Node Set Spline Cyclic
    set_spline_cyclic = neck_1.nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = False

    # Node Trim Curve
    trim_curve = neck_1.nodes.new("GeometryNodeTrimCurve")
    trim_curve.name = "Trim Curve"
    trim_curve.mode = 'FACTOR'
    # Selection
    trim_curve.inputs[1].default_value = True
    # Start
    trim_curve.inputs[2].default_value = 0.0
    # End
    trim_curve.inputs[3].default_value = 0.5074577331542969

    # Node Resample Curve.001
    resample_curve_001 = neck_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = 'Count'
    # Count
    resample_curve_001.inputs[3].default_value = 47
    # Length
    resample_curve_001.inputs[4].default_value = 0.10000000149011612

    # Node Group.006
    group_006 = neck_1.nodes.new("GeometryNodeGroup")
    group_006.name = "Group.006"
    group_006.node_tree = bpy.data.node_groups[node_tree_names[gold_decorations_1_node_group]]
    # Socket_2
    group_006.inputs[1].default_value = 68
    # Socket_3
    group_006.inputs[2].default_value = 2.6999993324279785
    # Socket_4
    group_006.inputs[3].default_value = 56

    # Node Set Curve Normal
    set_curve_normal = neck_1.nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal.name = "Set Curve Normal"
    # Selection
    set_curve_normal.inputs[1].default_value = True
    # Mode
    set_curve_normal.inputs[2].default_value = 'Free'

    # Node Sample Nearest Surface
    sample_nearest_surface = neck_1.nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.name = "Sample Nearest Surface"
    sample_nearest_surface.data_type = 'FLOAT_VECTOR'
    # Group ID
    sample_nearest_surface.inputs[2].default_value = 0
    # Sample Position
    sample_nearest_surface.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Sample Group ID
    sample_nearest_surface.inputs[4].default_value = 0

    # Node Normal
    normal = neck_1.nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.legacy_corner_normals = False

    # Node Vector Math
    vector_math = neck_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'CROSS_PRODUCT'

    # Node Curve Tangent
    curve_tangent = neck_1.nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"

    # Node Frame.005
    frame_005 = neck_1.nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label_size = 20
    frame_005.shrink = True

    # Node Group.007
    group_007 = neck_1.nodes.new("GeometryNodeGroup")
    group_007.name = "Group.007"
    group_007.node_tree = bpy.data.node_groups[node_tree_names[gold_on_band_1_node_group]]
    # Socket_1
    group_007.inputs[1].default_value = 100000.0
    # Socket_2
    group_007.inputs[2].default_value = 8.669999122619629
    # Socket_3
    group_007.inputs[3].default_value = 1

    # Node Frame.011
    frame_011 = neck_1.nodes.new("NodeFrame")
    frame_011.label = "Gold"
    frame_011.name = "Frame.011"
    frame_011.use_custom_color = True
    frame_011.color = (0.6704087853431702, 0.49389249086380005, 0.16088831424713135)
    frame_011.label_size = 20
    frame_011.shrink = True

    # Node Gem in Holder
    gem_in_holder = neck_1.nodes.new("GeometryNodeGroup")
    gem_in_holder.name = "Gem in Holder"
    gem_in_holder.node_tree = bpy.data.node_groups[node_tree_names[gem_in_holder_1_node_group]]
    # Socket_3
    gem_in_holder.inputs[0].default_value = 0.009999999776482582
    # Socket_11
    gem_in_holder.inputs[1].default_value = "ruby"
    # Socket_12
    gem_in_holder.inputs[2].default_value = False
    # Socket_4
    gem_in_holder.inputs[3].default_value = 0.004999999888241291
    # Socket_13
    gem_in_holder.inputs[6].default_value = True

    # Node Curve to Points
    curve_to_points = neck_1.nodes.new("GeometryNodeCurveToPoints")
    curve_to_points.name = "Curve to Points"
    curve_to_points.mode = 'COUNT'
    # Count
    curve_to_points.inputs[1].default_value = 8

    # Node For Each Geometry Element Input
    for_each_geometry_element_input = neck_1.nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input.name = "For Each Geometry Element Input"
    # Node For Each Geometry Element Output
    for_each_geometry_element_output = neck_1.nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.name = "For Each Geometry Element Output"
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_input_index = 1
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = 'POINT'
    for_each_geometry_element_output.generation_items.clear()
    for_each_geometry_element_output.generation_items.new('GEOMETRY', "Geometry")
    for_each_geometry_element_output.generation_items[0].domain = 'POINT'
    for_each_geometry_element_output.input_items.clear()
    for_each_geometry_element_output.input_items.new('ROTATION', "Rotation")
    for_each_geometry_element_output.input_items.new('VECTOR', "Position")
    for_each_geometry_element_output.inspection_index = 0
    for_each_geometry_element_output.main_items.clear()

    # Node Position.002
    position_002 = neck_1.nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"

    # Node Transform Geometry.007
    transform_geometry_007 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_007.name = "Transform Geometry.007"
    # Mode
    transform_geometry_007.inputs[1].default_value = 'Components'

    # Node Rotate Rotation
    rotate_rotation = neck_1.nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.name = "Rotate Rotation"
    rotate_rotation.rotation_space = 'LOCAL'
    # Rotate By
    rotate_rotation.inputs[1].default_value = (0.0, 1.5707963705062866, 0.0)

    # Node Random Value
    random_value = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.data_type = 'INT'
    # Min_002
    random_value.inputs[4].default_value = 5
    # Max_002
    random_value.inputs[5].default_value = 7
    # Seed
    random_value.inputs[8].default_value = 0

    # Node Transform Geometry.008
    transform_geometry_008 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_008.name = "Transform Geometry.008"
    # Mode
    transform_geometry_008.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_008.inputs[2].default_value = (0.0, -0.004999999888241291, 0.0)
    # Rotation
    transform_geometry_008.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_008.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Random Value.001
    random_value_001 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.data_type = 'FLOAT'
    # Min_001
    random_value_001.inputs[2].default_value = 0.3499999940395355
    # Max_001
    random_value_001.inputs[3].default_value = 0.75
    # Seed
    random_value_001.inputs[8].default_value = 0

    # Node Store Named Attribute.001
    store_named_attribute_001 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.data_type = 'BOOLEAN'
    store_named_attribute_001.domain = 'POINT'
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_001.inputs[3].default_value = True

    # Node Random Value.002
    random_value_002 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_002.name = "Random Value.002"
    random_value_002.data_type = 'FLOAT'
    # Min_001
    random_value_002.inputs[2].default_value = 0.0
    # Max_001
    random_value_002.inputs[3].default_value = 100.0
    # Seed
    random_value_002.inputs[8].default_value = 24

    # Node Rotate Rotation.001
    rotate_rotation_001 = neck_1.nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.name = "Rotate Rotation.001"
    rotate_rotation_001.rotation_space = 'LOCAL'
    # Rotate By
    rotate_rotation_001.inputs[1].default_value = (0.0, 0.0, -1.5707963705062866)

    # Node Random Value.003
    random_value_003 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_003.name = "Random Value.003"
    random_value_003.data_type = 'FLOAT'
    # Min_001
    random_value_003.inputs[2].default_value = 0.0010000000474974513
    # Max_001
    random_value_003.inputs[3].default_value = 0.004999999888241291
    # Seed
    random_value_003.inputs[8].default_value = 0

    # Node Random Value.004
    random_value_004 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_004.name = "Random Value.004"
    random_value_004.data_type = 'INT'
    # Min_002
    random_value_004.inputs[4].default_value = 0
    # Max_002
    random_value_004.inputs[5].default_value = 100
    # Seed
    random_value_004.inputs[8].default_value = 0

    # Node Random Value.005
    random_value_005 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_005.name = "Random Value.005"
    random_value_005.data_type = 'INT'
    # Min_002
    random_value_005.inputs[4].default_value = 6
    # Max_002
    random_value_005.inputs[5].default_value = 20
    # Seed
    random_value_005.inputs[8].default_value = 0

    # Node Random Value.006
    random_value_006 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_006.name = "Random Value.006"
    random_value_006.data_type = 'INT'
    # Min_002
    random_value_006.inputs[4].default_value = 5
    # Max_002
    random_value_006.inputs[5].default_value = 30
    # Seed
    random_value_006.inputs[8].default_value = 0

    # Node Frame.012
    frame_012 = neck_1.nodes.new("NodeFrame")
    frame_012.label = "Broaches"
    frame_012.name = "Frame.012"
    frame_012.label_size = 20
    frame_012.shrink = True

    # Node Separate Geometry.001
    separate_geometry_001 = neck_1.nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_001.name = "Separate Geometry.001"
    separate_geometry_001.domain = 'FACE'

    # Node Separate XYZ.003
    separate_xyz_003 = neck_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_003.name = "Separate XYZ.003"

    # Node Compare.002
    compare_002 = neck_1.nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.data_type = 'FLOAT'
    compare_002.mode = 'ELEMENT'
    compare_002.operation = 'GREATER_THAN'
    # B
    compare_002.inputs[1].default_value = 0.8700000047683716

    # Node Join Geometry.004
    join_geometry_004 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"

    # Node Trim Curve.001
    trim_curve_001 = neck_1.nodes.new("GeometryNodeTrimCurve")
    trim_curve_001.name = "Trim Curve.001"
    trim_curve_001.mode = 'FACTOR'
    # Selection
    trim_curve_001.inputs[1].default_value = True
    # Start
    trim_curve_001.inputs[2].default_value = 0.18784530460834503
    # End
    trim_curve_001.inputs[3].default_value = 0.46817636489868164

    # Node Set Curve Normal.001
    set_curve_normal_001 = neck_1.nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_001.name = "Set Curve Normal.001"
    # Selection
    set_curve_normal_001.inputs[1].default_value = True
    # Mode
    set_curve_normal_001.inputs[2].default_value = 'Free'

    # Node Compare.003
    compare_003 = neck_1.nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.data_type = 'FLOAT'
    compare_003.mode = 'ELEMENT'
    compare_003.operation = 'LESS_THAN'
    # B
    compare_003.inputs[1].default_value = 0.25999999046325684

    # Node Boolean Math
    boolean_math = neck_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.operation = 'OR'

    # Node Boolean Math.001
    boolean_math_001 = neck_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.operation = 'OR'

    # Node Compare.004
    compare_004 = neck_1.nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.data_type = 'FLOAT'
    compare_004.mode = 'ELEMENT'
    compare_004.operation = 'EQUAL'
    # B
    compare_004.inputs[1].default_value = 0.5
    # Epsilon
    compare_004.inputs[12].default_value = 0.020999997854232788

    # Node Frame.001
    frame_001 = neck_1.nodes.new("NodeFrame")
    frame_001.label = "On Band"
    frame_001.name = "Frame.001"
    frame_001.label_size = 20
    frame_001.shrink = True

    # Node Boolean Math.002
    boolean_math_002 = neck_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.operation = 'AND'

    # Node Compare.005
    compare_005 = neck_1.nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.data_type = 'FLOAT'
    compare_005.mode = 'ELEMENT'
    compare_005.operation = 'LESS_THAN'
    # B
    compare_005.inputs[1].default_value = 0.5

    # Node Gem in Holder.001
    gem_in_holder_001 = neck_1.nodes.new("GeometryNodeGroup")
    gem_in_holder_001.name = "Gem in Holder.001"
    gem_in_holder_001.node_tree = bpy.data.node_groups[node_tree_names[gem_in_holder_1_node_group]]
    # Socket_3
    gem_in_holder_001.inputs[0].default_value = 0.009999990463256836
    # Socket_11
    gem_in_holder_001.inputs[1].default_value = "ruby"
    # Socket_12
    gem_in_holder_001.inputs[2].default_value = False
    # Socket_4
    gem_in_holder_001.inputs[3].default_value = 0.004999999888241291
    # Socket_1
    gem_in_holder_001.inputs[4].default_value = 20
    # Socket_2
    gem_in_holder_001.inputs[5].default_value = 10
    # Socket_13
    gem_in_holder_001.inputs[6].default_value = False
    # Socket_10
    gem_in_holder_001.inputs[7].default_value = 6
    # Socket_7
    gem_in_holder_001.inputs[8].default_value = 10

    # Node Mesh to Curve.002
    mesh_to_curve_002 = neck_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_002.name = "Mesh to Curve.002"
    mesh_to_curve_002.mode = 'EDGES'

    # Node Is Edge Boundary
    is_edge_boundary = neck_1.nodes.new("GeometryNodeGroup")
    is_edge_boundary.name = "Is Edge Boundary"
    is_edge_boundary.node_tree = bpy.data.node_groups[node_tree_names[is_edge_boundary_1_node_group_1]]

    # Node Set Spline Cyclic.001
    set_spline_cyclic_001 = neck_1.nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_001.name = "Set Spline Cyclic.001"
    # Selection
    set_spline_cyclic_001.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic_001.inputs[2].default_value = False

    # Node Trim Curve.004
    trim_curve_004 = neck_1.nodes.new("GeometryNodeTrimCurve")
    trim_curve_004.name = "Trim Curve.004"
    trim_curve_004.mode = 'FACTOR'
    # Selection
    trim_curve_004.inputs[1].default_value = True
    # Start
    trim_curve_004.inputs[2].default_value = 0.03867403417825699
    # End
    trim_curve_004.inputs[3].default_value = 0.4364641308784485

    # Node Curve to Points.001
    curve_to_points_001 = neck_1.nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_001.name = "Curve to Points.001"
    curve_to_points_001.mode = 'COUNT'
    # Count
    curve_to_points_001.inputs[1].default_value = 50

    # Node Set Curve Normal.002
    set_curve_normal_002 = neck_1.nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_002.name = "Set Curve Normal.002"
    # Selection
    set_curve_normal_002.inputs[1].default_value = True
    # Mode
    set_curve_normal_002.inputs[2].default_value = 'Free'

    # Node Position.004
    position_004 = neck_1.nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"

    # Node For Each Geometry Element Input.001
    for_each_geometry_element_input_001 = neck_1.nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_001.name = "For Each Geometry Element Input.001"
    # Node For Each Geometry Element Output.001
    for_each_geometry_element_output_001 = neck_1.nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_001.name = "For Each Geometry Element Output.001"
    for_each_geometry_element_output_001.active_generation_index = 0
    for_each_geometry_element_output_001.active_input_index = 1
    for_each_geometry_element_output_001.active_main_index = 0
    for_each_geometry_element_output_001.domain = 'POINT'
    for_each_geometry_element_output_001.generation_items.clear()
    for_each_geometry_element_output_001.generation_items.new('GEOMETRY', "Geometry")
    for_each_geometry_element_output_001.generation_items[0].domain = 'POINT'
    for_each_geometry_element_output_001.input_items.clear()
    for_each_geometry_element_output_001.input_items.new('VECTOR', "Position")
    for_each_geometry_element_output_001.input_items.new('ROTATION', "Rotation")
    for_each_geometry_element_output_001.inspection_index = 0
    for_each_geometry_element_output_001.main_items.clear()

    # Node Transform Geometry.009
    transform_geometry_009 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_009.name = "Transform Geometry.009"
    # Mode
    transform_geometry_009.inputs[1].default_value = 'Components'
    # Scale
    transform_geometry_009.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Rotate Rotation.002
    rotate_rotation_002 = neck_1.nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_002.name = "Rotate Rotation.002"
    rotate_rotation_002.rotation_space = 'LOCAL'
    # Rotate By
    rotate_rotation_002.inputs[1].default_value = (0.0, -1.5707963705062866, 0.0)

    # Node Frame.014
    frame_014 = neck_1.nodes.new("NodeFrame")
    frame_014.label = "Random Wings"
    frame_014.name = "Frame.014"
    frame_014.label_size = 20
    frame_014.shrink = True

    # Node Random Value.007
    random_value_007 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_007.name = "Random Value.007"
    random_value_007.data_type = 'FLOAT'
    # Min_001
    random_value_007.inputs[2].default_value = 6.0
    # Max_001
    random_value_007.inputs[3].default_value = 7.0
    # Seed
    random_value_007.inputs[8].default_value = 33

    # Node Random Value.008
    random_value_008 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_008.name = "Random Value.008"
    random_value_008.data_type = 'FLOAT'
    # Min_001
    random_value_008.inputs[2].default_value = 0.0
    # Max_001
    random_value_008.inputs[3].default_value = 0.003000000026077032
    # Seed
    random_value_008.inputs[8].default_value = 10

    # Node Distribute Points on Faces
    distribute_points_on_faces = neck_1.nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.name = "Distribute Points on Faces"
    distribute_points_on_faces.distribute_method = 'RANDOM'
    distribute_points_on_faces.use_legacy_normal = False
    # Selection
    distribute_points_on_faces.inputs[1].default_value = True
    # Density
    distribute_points_on_faces.inputs[4].default_value = 5000.0
    # Seed
    distribute_points_on_faces.inputs[6].default_value = 1

    # Node Instance on Points
    instance_on_points = neck_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Rotation
    instance_on_points.inputs[5].default_value = (0.0, 0.0, 0.0)

    # Node Ico Sphere
    ico_sphere = neck_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.004000000189989805
    # Subdivisions
    ico_sphere.inputs[1].default_value = 2

    # Node Store Named Attribute.002
    store_named_attribute_002 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.data_type = 'BOOLEAN'
    store_named_attribute_002.domain = 'INSTANCE'
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "ruby"

    # Node Random Value.009
    random_value_009 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_009.name = "Random Value.009"
    random_value_009.data_type = 'BOOLEAN'
    # Probability
    random_value_009.inputs[6].default_value = 0.5
    # ID
    random_value_009.inputs[7].default_value = 0
    # Seed
    random_value_009.inputs[8].default_value = 0

    # Node Boolean Math.003
    boolean_math_003 = neck_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.operation = 'NOT'

    # Node Store Named Attribute.003
    store_named_attribute_003 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.data_type = 'BOOLEAN'
    store_named_attribute_003.domain = 'INSTANCE'
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "saphire"

    # Node Realize Instances.001
    realize_instances_001 = neck_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0

    # Node Set Shade Smooth.003
    set_shade_smooth_003 = neck_1.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.name = "Set Shade Smooth.003"
    set_shade_smooth_003.domain = 'FACE'
    # Selection
    set_shade_smooth_003.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_003.inputs[2].default_value = True

    # Node Frame.015
    frame_015 = neck_1.nodes.new("NodeFrame")
    frame_015.label = "Random Jewels"
    frame_015.name = "Frame.015"
    frame_015.label_size = 20
    frame_015.shrink = True

    # Node Reroute.001
    reroute_001 = neck_1.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Node Distribute Points on Faces.001
    distribute_points_on_faces_001 = neck_1.nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces_001.name = "Distribute Points on Faces.001"
    distribute_points_on_faces_001.distribute_method = 'POISSON'
    distribute_points_on_faces_001.use_legacy_normal = False
    # Distance Min
    distribute_points_on_faces_001.inputs[2].default_value = 0.009999999776482582
    # Density Max
    distribute_points_on_faces_001.inputs[3].default_value = 5000.0
    # Density Factor
    distribute_points_on_faces_001.inputs[5].default_value = 1.0
    # Seed
    distribute_points_on_faces_001.inputs[6].default_value = 0

    # Node Geometry Proximity
    geometry_proximity = neck_1.nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.target_element = 'POINTS'
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Source Position
    geometry_proximity.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0

    # Node Compare.006
    compare_006 = neck_1.nodes.new("FunctionNodeCompare")
    compare_006.name = "Compare.006"
    compare_006.data_type = 'FLOAT'
    compare_006.mode = 'ELEMENT'
    compare_006.operation = 'LESS_THAN'
    # B
    compare_006.inputs[1].default_value = 0.0010000000474974513

    # Node Gem in Holder.002
    gem_in_holder_002 = neck_1.nodes.new("GeometryNodeGroup")
    gem_in_holder_002.name = "Gem in Holder.002"
    gem_in_holder_002.node_tree = bpy.data.node_groups[node_tree_names[gem_in_holder_1_node_group]]
    # Socket_3
    gem_in_holder_002.inputs[0].default_value = 0.009999990463256836
    # Socket_11
    gem_in_holder_002.inputs[1].default_value = "ruby"
    # Socket_12
    gem_in_holder_002.inputs[2].default_value = False
    # Socket_4
    gem_in_holder_002.inputs[3].default_value = 0.004999999888241291
    # Socket_1
    gem_in_holder_002.inputs[4].default_value = 20
    # Socket_2
    gem_in_holder_002.inputs[5].default_value = 10
    # Socket_13
    gem_in_holder_002.inputs[6].default_value = False
    # Socket_10
    gem_in_holder_002.inputs[7].default_value = 6
    # Socket_7
    gem_in_holder_002.inputs[8].default_value = 10
    # Socket_8
    gem_in_holder_002.inputs[9].default_value = 0.0010000000474974513
    # Socket_9
    gem_in_holder_002.inputs[10].default_value = 6.6099958419799805

    # Node Instance on Points.001
    instance_on_points_001 = neck_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0

    # Node Random Value.010
    random_value_010 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_010.name = "Random Value.010"
    random_value_010.data_type = 'FLOAT'
    # Min_001
    random_value_010.inputs[2].default_value = 0.10000000894069672
    # Max_001
    random_value_010.inputs[3].default_value = 0.4000000059604645
    # ID
    random_value_010.inputs[7].default_value = 0
    # Seed
    random_value_010.inputs[8].default_value = 0

    # Node Frame.016
    frame_016 = neck_1.nodes.new("NodeFrame")
    frame_016.label = "Larger Jewels"
    frame_016.name = "Frame.016"
    frame_016.label_size = 20
    frame_016.shrink = True

    # Node Realize Instances.002
    realize_instances_002 = neck_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.name = "Realize Instances.002"
    # Selection
    realize_instances_002.inputs[1].default_value = True
    # Realize All
    realize_instances_002.inputs[2].default_value = True
    # Depth
    realize_instances_002.inputs[3].default_value = 0

    # Node Transform Geometry.010
    transform_geometry_010 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_010.name = "Transform Geometry.010"
    # Mode
    transform_geometry_010.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_010.inputs[2].default_value = (0.0, 0.0, 0.004000000189989805)
    # Rotation
    transform_geometry_010.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_010.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Group.005
    group_005 = neck_1.nodes.new("GeometryNodeGroup")
    group_005.name = "Group.005"
    group_005.node_tree = bpy.data.node_groups[node_tree_names[swap_attr_1_node_group]]
    # Socket_3
    group_005.inputs[2].default_value = "ruby"
    # Socket_4
    group_005.inputs[3].default_value = "saphire"

    # Node Capture Attribute.001
    capture_attribute_001 = neck_1.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.active_index = 0
    capture_attribute_001.capture_items.clear()
    capture_attribute_001.capture_items.new('FLOAT', "Index")
    capture_attribute_001.capture_items["Index"].data_type = 'INT'
    capture_attribute_001.domain = 'INSTANCE'

    # Node Index
    index = neck_1.nodes.new("GeometryNodeInputIndex")
    index.name = "Index"

    # Node Set Position.001
    set_position_001 = neck_1.nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Geometry Proximity.001
    geometry_proximity_001 = neck_1.nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.target_element = 'FACES'
    # Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    # Source Position
    geometry_proximity_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0

    # Node Curve to Mesh
    curve_to_mesh = neck_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False

    # Node Separate Geometry.002
    separate_geometry_002 = neck_1.nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry_002.name = "Separate Geometry.002"
    separate_geometry_002.domain = 'CURVE'

    # Node Compare.007
    compare_007 = neck_1.nodes.new("FunctionNodeCompare")
    compare_007.name = "Compare.007"
    compare_007.data_type = 'FLOAT'
    compare_007.mode = 'ELEMENT'
    compare_007.operation = 'EQUAL'
    # B
    compare_007.inputs[1].default_value = 0.5
    # Epsilon
    compare_007.inputs[12].default_value = 0.0010000000474974513

    # Node Separate XYZ.004
    separate_xyz_004 = neck_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_004.name = "Separate XYZ.004"
    separate_xyz_004.outputs[0].hide = True
    separate_xyz_004.outputs[2].hide = True

    # Node Trim Curve.002
    trim_curve_002 = neck_1.nodes.new("GeometryNodeTrimCurve")
    trim_curve_002.name = "Trim Curve.002"
    trim_curve_002.mode = 'FACTOR'
    # Selection
    trim_curve_002.inputs[1].default_value = True
    # Start
    trim_curve_002.inputs[2].default_value = 0.0
    # End
    trim_curve_002.inputs[3].default_value = 0.8690060973167419

    # Node Resample Curve.002
    resample_curve_002 = neck_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.name = "Resample Curve.002"
    resample_curve_002.keep_last_segment = True
    # Selection
    resample_curve_002.inputs[1].default_value = True
    # Mode
    resample_curve_002.inputs[2].default_value = 'Count'
    # Count
    resample_curve_002.inputs[3].default_value = 47
    # Length
    resample_curve_002.inputs[4].default_value = 0.10000000149011612

    # Node Group.008
    group_008 = neck_1.nodes.new("GeometryNodeGroup")
    group_008.name = "Group.008"
    group_008.node_tree = bpy.data.node_groups[node_tree_names[gold_decorations_1_node_group]]
    # Socket_2
    group_008.inputs[1].default_value = 75
    # Socket_3
    group_008.inputs[2].default_value = 3.0999999046325684
    # Socket_4
    group_008.inputs[3].default_value = 6

    # Node Set Curve Normal.003
    set_curve_normal_003 = neck_1.nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_003.name = "Set Curve Normal.003"
    # Selection
    set_curve_normal_003.inputs[1].default_value = True
    # Mode
    set_curve_normal_003.inputs[2].default_value = 'Z Up'
    # Normal
    set_curve_normal_003.inputs[3].default_value = (0.0, 0.0, 1.0)

    # Node Frame.013
    frame_013 = neck_1.nodes.new("NodeFrame")
    frame_013.name = "Frame.013"
    frame_013.label_size = 20
    frame_013.shrink = True

    # Node Transform Geometry
    transform_geometry = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry.inputs[2].default_value = (0.0, -0.0010000000474974513, 0.0)
    # Rotation
    transform_geometry.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Random Value.011
    random_value_011 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_011.name = "Random Value.011"
    random_value_011.data_type = 'FLOAT'
    # Min_001
    random_value_011.inputs[2].default_value = 0.20000000298023224
    # Max_001
    random_value_011.inputs[3].default_value = 0.6000000238418579
    # ID
    random_value_011.inputs[7].default_value = 0
    # Seed
    random_value_011.inputs[8].default_value = 0

    # Node Trim Curve.003
    trim_curve_003 = neck_1.nodes.new("GeometryNodeTrimCurve")
    trim_curve_003.name = "Trim Curve.003"
    trim_curve_003.mode = 'FACTOR'
    # Selection
    trim_curve_003.inputs[1].default_value = True
    # Start
    trim_curve_003.inputs[2].default_value = 0.10000000149011612
    # End
    trim_curve_003.inputs[3].default_value = 0.5

    # Node Resample Curve.003
    resample_curve_003 = neck_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_003.name = "Resample Curve.003"
    resample_curve_003.keep_last_segment = True
    # Selection
    resample_curve_003.inputs[1].default_value = True
    # Mode
    resample_curve_003.inputs[2].default_value = 'Count'
    # Count
    resample_curve_003.inputs[3].default_value = 47
    # Length
    resample_curve_003.inputs[4].default_value = 0.10000000149011612

    # Node Group.009
    group_009 = neck_1.nodes.new("GeometryNodeGroup")
    group_009.name = "Group.009"
    group_009.node_tree = bpy.data.node_groups[node_tree_names[gold_decorations_1_node_group]]
    # Socket_2
    group_009.inputs[1].default_value = 78
    # Socket_3
    group_009.inputs[2].default_value = 3.1999998092651367
    # Socket_4
    group_009.inputs[3].default_value = 13

    # Node Set Curve Normal.004
    set_curve_normal_004 = neck_1.nodes.new("GeometryNodeSetCurveNormal")
    set_curve_normal_004.name = "Set Curve Normal.004"
    # Selection
    set_curve_normal_004.inputs[1].default_value = True
    # Mode
    set_curve_normal_004.inputs[2].default_value = 'Free'

    # Node Frame.017
    frame_017 = neck_1.nodes.new("NodeFrame")
    frame_017.name = "Frame.017"
    frame_017.label_size = 20
    frame_017.shrink = True

    # Node Transform Geometry.011
    transform_geometry_011 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_011.name = "Transform Geometry.011"
    # Mode
    transform_geometry_011.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_011.inputs[2].default_value = (0.0, 0.0, -0.003000000026077032)
    # Rotation
    transform_geometry_011.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_011.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Mesh to Curve
    mesh_to_curve = neck_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.mode = 'EDGES'
    # Selection
    mesh_to_curve.inputs[1].default_value = True

    # Node Set Curve Tilt
    set_curve_tilt = neck_1.nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Tilt
    set_curve_tilt.inputs[2].default_value = -0.34819304943084717

    # Node Reroute.002
    reroute_002 = neck_1.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Node Curve Circle.002
    curve_circle_002 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_002.name = "Curve Circle.002"
    curve_circle_002.mode = 'RADIUS'
    # Resolution
    curve_circle_002.inputs[0].default_value = 64
    # Radius
    curve_circle_002.inputs[4].default_value = 0.12999999523162842

    # Node Transform Geometry.012
    transform_geometry_012 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_012.name = "Transform Geometry.012"
    # Mode
    transform_geometry_012.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_012.inputs[2].default_value = (0.009999999776482582, -0.03999999910593033, 0.46000000834465027)
    # Rotation
    transform_geometry_012.inputs[3].default_value = (-0.027925267815589905, 0.0, 0.15533429384231567)
    # Scale
    transform_geometry_012.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Set Position.002
    set_position_002 = neck_1.nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    # Selection
    set_position_002.inputs[1].default_value = True

    # Node Position.003
    position_003 = neck_1.nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"

    # Node Separate XYZ.005
    separate_xyz_005 = neck_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_005.name = "Separate XYZ.005"
    separate_xyz_005.outputs[0].hide = True
    separate_xyz_005.outputs[2].hide = True

    # Node Map Range.001
    map_range_001 = neck_1.nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.clamp = True
    map_range_001.data_type = 'FLOAT'
    map_range_001.interpolation_type = 'LINEAR'
    # From Min
    map_range_001.inputs[1].default_value = 0.12999999523162842
    # From Max
    map_range_001.inputs[2].default_value = -0.12999999523162842
    # To Min
    map_range_001.inputs[3].default_value = 0.0
    # To Max
    map_range_001.inputs[4].default_value = 1.0

    # Node Float Curve
    float_curve = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    # Mapping settings
    float_curve.mapping.extend = 'EXTRAPOLATED'
    float_curve.mapping.tone = 'STANDARD'
    float_curve.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve.mapping.clip_min_x = 0.0
    float_curve.mapping.clip_min_y = 0.0
    float_curve.mapping.clip_max_x = 1.0
    float_curve.mapping.clip_max_y = 1.0
    float_curve.mapping.use_clip = True
    # Curve 0
    float_curve_curve_0 = float_curve.mapping.curves[0]
    float_curve_curve_0_point_0 = float_curve_curve_0.points[0]
    float_curve_curve_0_point_0.location = (0.0, 0.07379312813282013)
    float_curve_curve_0_point_0.handle_type = 'AUTO'
    float_curve_curve_0_point_1 = float_curve_curve_0.points[1]
    float_curve_curve_0_point_1.location = (0.2552628517150879, 0.0)
    float_curve_curve_0_point_1.handle_type = 'AUTO'
    float_curve_curve_0_point_2 = float_curve_curve_0.points.new(0.6486042737960815, 0.1399659961462021)
    float_curve_curve_0_point_2.handle_type = 'AUTO'
    float_curve_curve_0_point_3 = float_curve_curve_0.points.new(0.9075074791908264, 0.37147393822669983)
    float_curve_curve_0_point_3.handle_type = 'AUTO'
    float_curve_curve_0_point_4 = float_curve_curve_0.points.new(1.0, 1.0)
    float_curve_curve_0_point_4.handle_type = 'AUTO'
    # Update curve after changes
    float_curve.mapping.update()
    # Factor
    float_curve.inputs[0].default_value = 1.0

    # Node Math.002
    math_002 = neck_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    # Value_001
    math_002.inputs[1].default_value = -0.29999998211860657

    # Node Combine XYZ.001
    combine_xyz_001 = neck_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_001.name = "Combine XYZ.001"
    # X
    combine_xyz_001.inputs[0].default_value = 0.0

    # Node Position.005
    position_005 = neck_1.nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"

    # Node Vector Math.001
    vector_math_001 = neck_1.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'MULTIPLY'

    # Node Combine XYZ.002
    combine_xyz_002 = neck_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_002.name = "Combine XYZ.002"
    # Y
    combine_xyz_002.inputs[1].default_value = 1.0
    # Z
    combine_xyz_002.inputs[2].default_value = 1.0

    # Node Float Curve.002
    float_curve_002 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_002.name = "Float Curve.002"
    # Mapping settings
    float_curve_002.mapping.extend = 'EXTRAPOLATED'
    float_curve_002.mapping.tone = 'STANDARD'
    float_curve_002.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_002.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_002.mapping.clip_min_x = 0.0
    float_curve_002.mapping.clip_min_y = 0.0
    float_curve_002.mapping.clip_max_x = 1.0
    float_curve_002.mapping.clip_max_y = 1.0
    float_curve_002.mapping.use_clip = True
    # Curve 0
    float_curve_002_curve_0 = float_curve_002.mapping.curves[0]
    float_curve_002_curve_0_point_0 = float_curve_002_curve_0.points[0]
    float_curve_002_curve_0_point_0.location = (0.0, 1.0)
    float_curve_002_curve_0_point_0.handle_type = 'AUTO'
    float_curve_002_curve_0_point_1 = float_curve_002_curve_0.points[1]
    float_curve_002_curve_0_point_1.location = (0.6706947088241577, 0.7413797378540039)
    float_curve_002_curve_0_point_1.handle_type = 'AUTO'
    float_curve_002_curve_0_point_2 = float_curve_002_curve_0.points.new(1.0, 0.4310343861579895)
    float_curve_002_curve_0_point_2.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_002.mapping.update()
    # Factor
    float_curve_002.inputs[0].default_value = 1.0

    # Node Store Named Attribute
    store_named_attribute = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'BOOLEAN'
    store_named_attribute.domain = 'POINT'
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "skip"
    # Value
    store_named_attribute.inputs[3].default_value = True

    # Node Resample Curve
    resample_curve = neck_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = 'Length'
    # Count
    resample_curve.inputs[3].default_value = 10
    # Length
    resample_curve.inputs[4].default_value = 0.014999999664723873

    # Node Instance on Points.002
    instance_on_points_002 = neck_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_002.name = "Instance on Points.002"
    # Selection
    instance_on_points_002.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_002.inputs[3].default_value = False
    # Instance Index
    instance_on_points_002.inputs[4].default_value = 0
    # Scale
    instance_on_points_002.inputs[6].default_value = (0.699999988079071, 0.699999988079071, 0.699999988079071)

    # Node Align Rotation to Vector
    align_rotation_to_vector = neck_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.axis = 'X'
    align_rotation_to_vector.pivot_axis = 'AUTO'
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0

    # Node Curve Tangent.001
    curve_tangent_001 = neck_1.nodes.new("GeometryNodeInputTangent")
    curve_tangent_001.name = "Curve Tangent.001"

    # Node Align Rotation to Vector.001
    align_rotation_to_vector_001 = neck_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.axis = 'Y'
    align_rotation_to_vector_001.pivot_axis = 'AUTO'
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0

    # Node Normal.001
    normal_001 = neck_1.nodes.new("GeometryNodeInputNormal")
    normal_001.name = "Normal.001"
    normal_001.legacy_corner_normals = False

    # Node Rotate Rotation.003
    rotate_rotation_003 = neck_1.nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_003.name = "Rotate Rotation.003"
    rotate_rotation_003.rotation_space = 'LOCAL'
    # Rotate By
    rotate_rotation_003.inputs[1].default_value = (0.23108159005641937, 0.14137165248394012, 0.0)

    # Node Spline Parameter
    spline_parameter = neck_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"

    # Node Math.003
    math_003 = neck_1.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'SUBTRACT'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = 0.7400000095367432

    # Node Math.004
    math_004 = neck_1.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'ABSOLUTE'
    math_004.use_clamp = False

    # Node Set Curve Tilt.002
    set_curve_tilt_002 = neck_1.nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_002.name = "Set Curve Tilt.002"
    # Selection
    set_curve_tilt_002.inputs[1].default_value = True

    # Node Map Range.002
    map_range_002 = neck_1.nodes.new("ShaderNodeMapRange")
    map_range_002.name = "Map Range.002"
    map_range_002.clamp = True
    map_range_002.data_type = 'FLOAT'
    map_range_002.interpolation_type = 'LINEAR'
    # From Min
    map_range_002.inputs[1].default_value = 0.0
    # From Max
    map_range_002.inputs[2].default_value = 0.08000002801418304
    # To Min
    map_range_002.inputs[3].default_value = 0.6799999475479126
    # To Max
    map_range_002.inputs[4].default_value = 0.47999998927116394

    # Node Float Curve.003
    float_curve_003 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_003.name = "Float Curve.003"
    # Mapping settings
    float_curve_003.mapping.extend = 'EXTRAPOLATED'
    float_curve_003.mapping.tone = 'STANDARD'
    float_curve_003.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_003.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_003.mapping.clip_min_x = 0.0
    float_curve_003.mapping.clip_min_y = 0.0
    float_curve_003.mapping.clip_max_x = 1.0
    float_curve_003.mapping.clip_max_y = 1.0
    float_curve_003.mapping.use_clip = True
    # Curve 0
    float_curve_003_curve_0 = float_curve_003.mapping.curves[0]
    float_curve_003_curve_0_point_0 = float_curve_003_curve_0.points[0]
    float_curve_003_curve_0_point_0.location = (0.0, 0.0)
    float_curve_003_curve_0_point_0.handle_type = 'AUTO'
    float_curve_003_curve_0_point_1 = float_curve_003_curve_0.points[1]
    float_curve_003_curve_0_point_1.location = (0.7777792811393738, 0.0)
    float_curve_003_curve_0_point_1.handle_type = 'VECTOR'
    float_curve_003_curve_0_point_2 = float_curve_003_curve_0.points.new(0.8468345403671265, 1.0)
    float_curve_003_curve_0_point_2.handle_type = 'VECTOR'
    float_curve_003_curve_0_point_3 = float_curve_003_curve_0.points.new(0.8811957836151123, 0.0)
    float_curve_003_curve_0_point_3.handle_type = 'VECTOR'
    float_curve_003_curve_0_point_4 = float_curve_003_curve_0.points.new(1.0, 0.0)
    float_curve_003_curve_0_point_4.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_003.mapping.update()
    # Factor
    float_curve_003.inputs[0].default_value = 1.0

    # Node Spline Parameter.001
    spline_parameter_001 = neck_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.outputs[1].hide = True
    spline_parameter_001.outputs[2].hide = True

    # Node Math.005
    math_005 = neck_1.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'MULTIPLY'
    math_005.use_clamp = False
    # Value_001
    math_005.inputs[1].default_value = 0.014999999664723873

    # Node Curve Circle.003
    curve_circle_003 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.name = "Curve Circle.003"
    curve_circle_003.mode = 'RADIUS'
    # Resolution
    curve_circle_003.inputs[0].default_value = 20
    # Radius
    curve_circle_003.inputs[4].default_value = 0.014999999664723873

    # Node Instance on Points.003
    instance_on_points_003 = neck_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.name = "Instance on Points.003"
    # Selection
    instance_on_points_003.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_003.inputs[3].default_value = False
    # Instance Index
    instance_on_points_003.inputs[4].default_value = 0
    # Rotation
    instance_on_points_003.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points_003.inputs[6].default_value = (1.0, 1.0, 1.0)

    # Node Ico Sphere.001
    ico_sphere_001 = neck_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.name = "Ico Sphere.001"
    # Radius
    ico_sphere_001.inputs[0].default_value = 0.0020000000949949026
    # Subdivisions
    ico_sphere_001.inputs[1].default_value = 1

    # Node Cylinder.001
    cylinder_001 = neck_1.nodes.new("GeometryNodeMeshCylinder")
    cylinder_001.name = "Cylinder.001"
    cylinder_001.hide = True
    cylinder_001.fill_type = 'NGON'
    cylinder_001.inputs[0].hide = True
    cylinder_001.inputs[1].hide = True
    cylinder_001.inputs[2].hide = True
    cylinder_001.inputs[3].hide = True
    cylinder_001.inputs[4].hide = True
    cylinder_001.outputs[1].hide = True
    cylinder_001.outputs[2].hide = True
    cylinder_001.outputs[3].hide = True
    cylinder_001.outputs[4].hide = True
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

    # Node Join Geometry.003
    join_geometry_003 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"
    join_geometry_003.hide = True

    # Node Ico Sphere.002
    ico_sphere_002 = neck_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_002.name = "Ico Sphere.002"
    # Radius
    ico_sphere_002.inputs[0].default_value = 0.012000000104308128
    # Subdivisions
    ico_sphere_002.inputs[1].default_value = 2

    # Node Transform Geometry.013
    transform_geometry_013 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_013.name = "Transform Geometry.013"
    # Mode
    transform_geometry_013.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_013.inputs[2].default_value = (-0.006000000052154064, 0.0, 0.0010000000474974513)
    # Rotation
    transform_geometry_013.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_013.inputs[4].default_value = (0.4699999988079071, 0.8600000143051147, 0.05000000074505806)

    # Node Set Position.003
    set_position_003 = neck_1.nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    # Selection
    set_position_003.inputs[1].default_value = True
    # Position
    set_position_003.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Vector Math.002
    vector_math_002 = neck_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'SCALE'
    # Scale
    vector_math_002.inputs[3].default_value = 0.004999999888241291

    # Node Noise Texture
    noise_texture = neck_1.nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.noise_dimensions = '4D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = False
    # Vector
    noise_texture.inputs[0].default_value = (0.0, 0.0, 0.0)
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
    # Distortion
    noise_texture.inputs[8].default_value = 0.0

    # Node Transform Geometry.014
    transform_geometry_014 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_014.name = "Transform Geometry.014"
    # Mode
    transform_geometry_014.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_014.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_014.inputs[3].default_value = (0.0, 0.0, 3.1415927410125732)
    # Scale
    transform_geometry_014.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Frame.002
    frame_002 = neck_1.nodes.new("NodeFrame")
    frame_002.label = "Necklace Link"
    frame_002.name = "Frame.002"
    frame_002.label_size = 20
    frame_002.shrink = True

    # Node Rotate Rotation.004
    rotate_rotation_004 = neck_1.nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_004.name = "Rotate Rotation.004"
    rotate_rotation_004.rotation_space = 'LOCAL'
    # Rotate By
    rotate_rotation_004.inputs[1].default_value = (3.1415927410125732, 0.0, 1.5707963705062866)

    # Node Ico Sphere.003
    ico_sphere_003 = neck_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_003.name = "Ico Sphere.003"
    # Radius
    ico_sphere_003.inputs[0].default_value = 0.004999999888241291
    # Subdivisions
    ico_sphere_003.inputs[1].default_value = 1

    # Node Frame.003
    frame_003 = neck_1.nodes.new("NodeFrame")
    frame_003.label = "Align"
    frame_003.name = "Frame.003"
    frame_003.label_size = 20
    frame_003.shrink = True

    # Node Store Named Attribute.004
    store_named_attribute_004 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.data_type = 'BOOLEAN'
    store_named_attribute_004.domain = 'POINT'
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_004.inputs[3].default_value = True

    # Node Cylinder.002
    cylinder_002 = neck_1.nodes.new("GeometryNodeMeshCylinder")
    cylinder_002.name = "Cylinder.002"
    cylinder_002.fill_type = 'NGON'
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

    # Node Math.006
    math_006 = neck_1.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'ADD'
    math_006.use_clamp = False

    # Node Spline Parameter.002
    spline_parameter_002 = neck_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"
    spline_parameter_002.outputs[1].hide = True
    spline_parameter_002.outputs[2].hide = True

    # Node Float Curve.004
    float_curve_004 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_004.name = "Float Curve.004"
    # Mapping settings
    float_curve_004.mapping.extend = 'EXTRAPOLATED'
    float_curve_004.mapping.tone = 'STANDARD'
    float_curve_004.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_004.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_004.mapping.clip_min_x = 0.0
    float_curve_004.mapping.clip_min_y = 0.0
    float_curve_004.mapping.clip_max_x = 1.0
    float_curve_004.mapping.clip_max_y = 1.0
    float_curve_004.mapping.use_clip = True
    # Curve 0
    float_curve_004_curve_0 = float_curve_004.mapping.curves[0]
    float_curve_004_curve_0_point_0 = float_curve_004_curve_0.points[0]
    float_curve_004_curve_0_point_0.location = (0.0, 0.0)
    float_curve_004_curve_0_point_0.handle_type = 'AUTO'
    float_curve_004_curve_0_point_1 = float_curve_004_curve_0.points[1]
    float_curve_004_curve_0_point_1.location = (0.435045450925827, 0.0)
    float_curve_004_curve_0_point_1.handle_type = 'AUTO'
    float_curve_004_curve_0_point_2 = float_curve_004_curve_0.points.new(0.5679758787155151, 0.05972415208816528)
    float_curve_004_curve_0_point_2.handle_type = 'AUTO'
    float_curve_004_curve_0_point_3 = float_curve_004_curve_0.points.new(0.7069486379623413, 0.053413793444633484)
    float_curve_004_curve_0_point_3.handle_type = 'AUTO'
    float_curve_004_curve_0_point_4 = float_curve_004_curve_0.points.new(0.8489417433738708, 0.0)
    float_curve_004_curve_0_point_4.handle_type = 'AUTO'
    float_curve_004_curve_0_point_5 = float_curve_004_curve_0.points.new(1.0, 0.0)
    float_curve_004_curve_0_point_5.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_004.mapping.update()
    # Factor
    float_curve_004.inputs[0].default_value = 1.0

    # Node Set Position.004
    set_position_004 = neck_1.nodes.new("GeometryNodeSetPosition")
    set_position_004.name = "Set Position.004"
    # Selection
    set_position_004.inputs[1].default_value = True
    # Position
    set_position_004.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Position.006
    position_006 = neck_1.nodes.new("GeometryNodeInputPosition")
    position_006.name = "Position.006"

    # Node Separate XYZ.006
    separate_xyz_006 = neck_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_006.name = "Separate XYZ.006"

    # Node Math.007
    math_007 = neck_1.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.operation = 'ABSOLUTE'
    math_007.use_clamp = False

    # Node Combine XYZ.003
    combine_xyz_003 = neck_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_003.name = "Combine XYZ.003"
    # X
    combine_xyz_003.inputs[0].default_value = 0.0
    # Z
    combine_xyz_003.inputs[2].default_value = 0.0

    # Node Map Range.003
    map_range_003 = neck_1.nodes.new("ShaderNodeMapRange")
    map_range_003.name = "Map Range.003"
    map_range_003.clamp = True
    map_range_003.data_type = 'FLOAT'
    map_range_003.interpolation_type = 'LINEAR'
    # From Min
    map_range_003.inputs[1].default_value = -0.019999999552965164
    # From Max
    map_range_003.inputs[2].default_value = 0.019999999552965164
    # To Min
    map_range_003.inputs[3].default_value = 0.7999999523162842
    # To Max
    map_range_003.inputs[4].default_value = 0.19999998807907104

    # Node Math.008
    math_008 = neck_1.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.operation = 'MULTIPLY'
    math_008.use_clamp = False

    # Node Boolean Math.004
    boolean_math_004 = neck_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.name = "Boolean Math.004"
    boolean_math_004.operation = 'AND'

    # Node Mesh to Curve.001
    mesh_to_curve_001 = neck_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.mode = 'EDGES'

    # Node Ico Sphere.004
    ico_sphere_004 = neck_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_004.name = "Ico Sphere.004"
    # Radius
    ico_sphere_004.inputs[0].default_value = 0.0020000000949949026
    # Subdivisions
    ico_sphere_004.inputs[1].default_value = 1

    # Node Instance on Points.004
    instance_on_points_004 = neck_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_004.name = "Instance on Points.004"
    # Selection
    instance_on_points_004.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_004.inputs[3].default_value = False
    # Instance Index
    instance_on_points_004.inputs[4].default_value = 0
    # Rotation
    instance_on_points_004.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points_004.inputs[6].default_value = (1.0, 1.0, 1.0)

    # Node Transform Geometry.015
    transform_geometry_015 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_015.name = "Transform Geometry.015"
    # Mode
    transform_geometry_015.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_015.inputs[2].default_value = (0.0, 0.0, 0.0020000000949949026)
    # Rotation
    transform_geometry_015.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_015.inputs[4].default_value = (2.0, 1.0, 0.30000001192092896)

    # Node Ico Sphere.005
    ico_sphere_005 = neck_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_005.name = "Ico Sphere.005"
    # Radius
    ico_sphere_005.inputs[0].default_value = 0.004999999888241291
    # Subdivisions
    ico_sphere_005.inputs[1].default_value = 2

    # Node Dual Mesh
    dual_mesh = neck_1.nodes.new("GeometryNodeDualMesh")
    dual_mesh.name = "Dual Mesh"
    # Keep Boundaries
    dual_mesh.inputs[1].default_value = False

    # Node Join Geometry.007
    join_geometry_007 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_007.name = "Join Geometry.007"
    join_geometry_007.hide = True

    # Node Transform Geometry.016
    transform_geometry_016 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_016.name = "Transform Geometry.016"
    # Mode
    transform_geometry_016.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_016.inputs[2].default_value = (0.0, 0.003000000026077032, 0.0)
    # Rotation
    transform_geometry_016.inputs[3].default_value = (0.0, 0.0, 1.5707963705062866)
    # Scale
    transform_geometry_016.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Transform Geometry.017
    transform_geometry_017 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_017.name = "Transform Geometry.017"
    # Mode
    transform_geometry_017.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_017.inputs[2].default_value = (-0.009999999776482582, 0.009999999776482582, 0.0)
    # Rotation
    transform_geometry_017.inputs[3].default_value = (0.0, 0.0, 1.0471975803375244)
    # Scale
    transform_geometry_017.inputs[4].default_value = (0.6000000238418579, 0.6000000238418579, 1.0)

    # Node Transform Geometry.018
    transform_geometry_018 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_018.name = "Transform Geometry.018"
    # Mode
    transform_geometry_018.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_018.inputs[2].default_value = (0.009999999776482582, 0.009999999776482582, 0.0)
    # Rotation
    transform_geometry_018.inputs[3].default_value = (0.0, 0.0, -1.0471975803375244)
    # Scale
    transform_geometry_018.inputs[4].default_value = (0.6000000238418579, 0.6000000238418579, 1.0)

    # Node Transform Geometry.019
    transform_geometry_019 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_019.name = "Transform Geometry.019"
    # Mode
    transform_geometry_019.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_019.inputs[2].default_value = (0.0, -0.012000000104308128, 0.0)
    # Rotation
    transform_geometry_019.inputs[3].default_value = (0.0, 0.0, 1.5707963705062866)
    # Scale
    transform_geometry_019.inputs[4].default_value = (0.30000001192092896, 0.6000000238418579, 1.0)

    # Node Join Geometry.009
    join_geometry_009 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_009.name = "Join Geometry.009"
    join_geometry_009.hide = True

    # Node Store Named Attribute.005
    store_named_attribute_005 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.name = "Store Named Attribute.005"
    store_named_attribute_005.data_type = 'BOOLEAN'
    store_named_attribute_005.domain = 'POINT'
    # Selection
    store_named_attribute_005.inputs[1].default_value = True
    # Name
    store_named_attribute_005.inputs[2].default_value = "ruby"
    # Value
    store_named_attribute_005.inputs[3].default_value = True

    # Node Join Geometry.010
    join_geometry_010 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_010.name = "Join Geometry.010"
    join_geometry_010.hide = True

    # Node Store Named Attribute.006
    store_named_attribute_006 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_006.name = "Store Named Attribute.006"
    store_named_attribute_006.data_type = 'BOOLEAN'
    store_named_attribute_006.domain = 'POINT'
    # Selection
    store_named_attribute_006.inputs[1].default_value = True
    # Name
    store_named_attribute_006.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_006.inputs[3].default_value = True

    # Node Frame.004
    frame_004 = neck_1.nodes.new("NodeFrame")
    frame_004.label = "Pendant"
    frame_004.name = "Frame.004"
    frame_004.label_size = 20
    frame_004.shrink = True

    # Node Sample Curve
    sample_curve = neck_1.nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.data_type = 'FLOAT'
    sample_curve.mode = 'FACTOR'
    sample_curve.use_all_curves = True
    # Value
    sample_curve.inputs[1].default_value = 0.0
    # Factor
    sample_curve.inputs[2].default_value = 0.6780651807785034

    # Node Transform Geometry.020
    transform_geometry_020 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_020.name = "Transform Geometry.020"
    # Mode
    transform_geometry_020.inputs[1].default_value = 'Components'
    # Rotation
    transform_geometry_020.inputs[3].default_value = (1.5707963705062866, 0.0, 0.0)
    # Scale
    transform_geometry_020.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Join Geometry.011
    join_geometry_011 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_011.name = "Join Geometry.011"
    join_geometry_011.hide = True

    # Node Vector Math.003
    vector_math_003 = neck_1.nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.operation = 'ADD'
    # Vector_001
    vector_math_003.inputs[1].default_value = (0.0, -0.003000000026077032, -0.019999999552965164)

    # Node Float Curve.005
    float_curve_005 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_005.name = "Float Curve.005"
    # Mapping settings
    float_curve_005.mapping.extend = 'EXTRAPOLATED'
    float_curve_005.mapping.tone = 'STANDARD'
    float_curve_005.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_005.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_005.mapping.clip_min_x = 0.0
    float_curve_005.mapping.clip_min_y = 0.0
    float_curve_005.mapping.clip_max_x = 1.0
    float_curve_005.mapping.clip_max_y = 1.0
    float_curve_005.mapping.use_clip = True
    # Curve 0
    float_curve_005_curve_0 = float_curve_005.mapping.curves[0]
    float_curve_005_curve_0_point_0 = float_curve_005_curve_0.points[0]
    float_curve_005_curve_0_point_0.location = (0.0, 0.0)
    float_curve_005_curve_0_point_0.handle_type = 'AUTO'
    float_curve_005_curve_0_point_1 = float_curve_005_curve_0.points[1]
    float_curve_005_curve_0_point_1.location = (0.6667145490646362, 0.0)
    float_curve_005_curve_0_point_1.handle_type = 'VECTOR'
    float_curve_005_curve_0_point_2 = float_curve_005_curve_0.points.new(0.7147770524024963, 0.4300000071525574)
    float_curve_005_curve_0_point_2.handle_type = 'VECTOR'
    float_curve_005_curve_0_point_3 = float_curve_005_curve_0.points.new(0.7437674403190613, 0.0)
    float_curve_005_curve_0_point_3.handle_type = 'VECTOR'
    float_curve_005_curve_0_point_4 = float_curve_005_curve_0.points.new(1.0, 0.0)
    float_curve_005_curve_0_point_4.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_005.mapping.update()
    # Factor
    float_curve_005.inputs[0].default_value = 1.0

    # Node Spline Parameter.003
    spline_parameter_003 = neck_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_003.name = "Spline Parameter.003"
    spline_parameter_003.outputs[1].hide = True
    spline_parameter_003.outputs[2].hide = True

    # Node Math.009
    math_009 = neck_1.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.operation = 'MULTIPLY'
    math_009.use_clamp = False
    # Value_001
    math_009.inputs[1].default_value = -0.014999999664723873

    # Node Math.010
    math_010 = neck_1.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.operation = 'ADD'
    math_010.use_clamp = False

    # Node Frame.018
    frame_018 = neck_1.nodes.new("NodeFrame")
    frame_018.label = "Necklace 1"
    frame_018.name = "Frame.018"
    frame_018.label_size = 20
    frame_018.shrink = True

    # Node Curve Circle.004
    curve_circle_004 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_004.name = "Curve Circle.004"
    curve_circle_004.mode = 'RADIUS'
    # Resolution
    curve_circle_004.inputs[0].default_value = 64
    # Radius
    curve_circle_004.inputs[4].default_value = 0.12999999523162842

    # Node Transform Geometry.021
    transform_geometry_021 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_021.name = "Transform Geometry.021"
    # Mode
    transform_geometry_021.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_021.inputs[2].default_value = (-0.009999999776482582, -0.03999999910593033, 0.46000000834465027)
    # Rotation
    transform_geometry_021.inputs[3].default_value = (-0.027925267815589905, 0.0, -0.08691740036010742)
    # Scale
    transform_geometry_021.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Set Position.005
    set_position_005 = neck_1.nodes.new("GeometryNodeSetPosition")
    set_position_005.name = "Set Position.005"
    # Selection
    set_position_005.inputs[1].default_value = True

    # Node Position.007
    position_007 = neck_1.nodes.new("GeometryNodeInputPosition")
    position_007.name = "Position.007"

    # Node Separate XYZ.007
    separate_xyz_007 = neck_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_007.name = "Separate XYZ.007"
    separate_xyz_007.outputs[0].hide = True
    separate_xyz_007.outputs[2].hide = True

    # Node Map Range.004
    map_range_004 = neck_1.nodes.new("ShaderNodeMapRange")
    map_range_004.name = "Map Range.004"
    map_range_004.clamp = True
    map_range_004.data_type = 'FLOAT'
    map_range_004.interpolation_type = 'LINEAR'
    # From Min
    map_range_004.inputs[1].default_value = 0.12999999523162842
    # From Max
    map_range_004.inputs[2].default_value = -0.12999999523162842
    # To Min
    map_range_004.inputs[3].default_value = 0.0
    # To Max
    map_range_004.inputs[4].default_value = 1.0

    # Node Float Curve.006
    float_curve_006 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_006.name = "Float Curve.006"
    # Mapping settings
    float_curve_006.mapping.extend = 'EXTRAPOLATED'
    float_curve_006.mapping.tone = 'STANDARD'
    float_curve_006.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_006.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_006.mapping.clip_min_x = 0.0
    float_curve_006.mapping.clip_min_y = 0.0
    float_curve_006.mapping.clip_max_x = 1.0
    float_curve_006.mapping.clip_max_y = 1.0
    float_curve_006.mapping.use_clip = True
    # Curve 0
    float_curve_006_curve_0 = float_curve_006.mapping.curves[0]
    float_curve_006_curve_0_point_0 = float_curve_006_curve_0.points[0]
    float_curve_006_curve_0_point_0.location = (0.0, 0.07379312813282013)
    float_curve_006_curve_0_point_0.handle_type = 'AUTO'
    float_curve_006_curve_0_point_1 = float_curve_006_curve_0.points[1]
    float_curve_006_curve_0_point_1.location = (0.2401570975780487, 0.0)
    float_curve_006_curve_0_point_1.handle_type = 'AUTO'
    float_curve_006_curve_0_point_2 = float_curve_006_curve_0.points.new(0.5458858609199524, 0.09686256945133209)
    float_curve_006_curve_0_point_2.handle_type = 'AUTO'
    float_curve_006_curve_0_point_3 = float_curve_006_curve_0.points.new(0.8652117848396301, 0.4619910717010498)
    float_curve_006_curve_0_point_3.handle_type = 'AUTO'
    float_curve_006_curve_0_point_4 = float_curve_006_curve_0.points.new(1.0, 1.0)
    float_curve_006_curve_0_point_4.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_006.mapping.update()
    # Factor
    float_curve_006.inputs[0].default_value = 1.0

    # Node Math.011
    math_011 = neck_1.nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.operation = 'MULTIPLY'
    math_011.use_clamp = False
    # Value_001
    math_011.inputs[1].default_value = -0.19999998807907104

    # Node Combine XYZ.004
    combine_xyz_004 = neck_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_004.name = "Combine XYZ.004"
    # X
    combine_xyz_004.inputs[0].default_value = 0.0

    # Node Position.008
    position_008 = neck_1.nodes.new("GeometryNodeInputPosition")
    position_008.name = "Position.008"

    # Node Vector Math.004
    vector_math_004 = neck_1.nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.operation = 'MULTIPLY'

    # Node Combine XYZ.005
    combine_xyz_005 = neck_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_005.name = "Combine XYZ.005"
    # Y
    combine_xyz_005.inputs[1].default_value = 1.0
    # Z
    combine_xyz_005.inputs[2].default_value = 1.0

    # Node Float Curve.007
    float_curve_007 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_007.name = "Float Curve.007"
    # Mapping settings
    float_curve_007.mapping.extend = 'EXTRAPOLATED'
    float_curve_007.mapping.tone = 'STANDARD'
    float_curve_007.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_007.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_007.mapping.clip_min_x = 0.0
    float_curve_007.mapping.clip_min_y = 0.0
    float_curve_007.mapping.clip_max_x = 1.0
    float_curve_007.mapping.clip_max_y = 1.0
    float_curve_007.mapping.use_clip = True
    # Curve 0
    float_curve_007_curve_0 = float_curve_007.mapping.curves[0]
    float_curve_007_curve_0_point_0 = float_curve_007_curve_0.points[0]
    float_curve_007_curve_0_point_0.location = (0.0, 1.0)
    float_curve_007_curve_0_point_0.handle_type = 'AUTO'
    float_curve_007_curve_0_point_1 = float_curve_007_curve_0.points[1]
    float_curve_007_curve_0_point_1.location = (0.6706947088241577, 0.7413797378540039)
    float_curve_007_curve_0_point_1.handle_type = 'AUTO'
    float_curve_007_curve_0_point_2 = float_curve_007_curve_0.points.new(1.0, 0.4310343861579895)
    float_curve_007_curve_0_point_2.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_007.mapping.update()
    # Factor
    float_curve_007.inputs[0].default_value = 1.0

    # Node Resample Curve.004
    resample_curve_004 = neck_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_004.name = "Resample Curve.004"
    resample_curve_004.keep_last_segment = True
    # Selection
    resample_curve_004.inputs[1].default_value = True
    # Mode
    resample_curve_004.inputs[2].default_value = 'Length'
    # Count
    resample_curve_004.inputs[3].default_value = 10
    # Length
    resample_curve_004.inputs[4].default_value = 0.013799999840557575

    # Node Instance on Points.005
    instance_on_points_005 = neck_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_005.name = "Instance on Points.005"
    # Selection
    instance_on_points_005.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_005.inputs[3].default_value = False
    # Instance Index
    instance_on_points_005.inputs[4].default_value = 0
    # Scale
    instance_on_points_005.inputs[6].default_value = (0.699999988079071, 0.699999988079071, 0.699999988079071)

    # Node Align Rotation to Vector.002
    align_rotation_to_vector_002 = neck_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_002.name = "Align Rotation to Vector.002"
    align_rotation_to_vector_002.axis = 'X'
    align_rotation_to_vector_002.pivot_axis = 'AUTO'
    # Rotation
    align_rotation_to_vector_002.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Factor
    align_rotation_to_vector_002.inputs[1].default_value = 1.0

    # Node Curve Tangent.002
    curve_tangent_002 = neck_1.nodes.new("GeometryNodeInputTangent")
    curve_tangent_002.name = "Curve Tangent.002"

    # Node Align Rotation to Vector.003
    align_rotation_to_vector_003 = neck_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_003.name = "Align Rotation to Vector.003"
    align_rotation_to_vector_003.axis = 'Y'
    align_rotation_to_vector_003.pivot_axis = 'AUTO'
    # Factor
    align_rotation_to_vector_003.inputs[1].default_value = 1.0

    # Node Normal.002
    normal_002 = neck_1.nodes.new("GeometryNodeInputNormal")
    normal_002.name = "Normal.002"
    normal_002.legacy_corner_normals = False

    # Node Spline Parameter.004
    spline_parameter_004 = neck_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_004.name = "Spline Parameter.004"

    # Node Math.012
    math_012 = neck_1.nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.operation = 'SUBTRACT'
    math_012.use_clamp = False
    # Value_001
    math_012.inputs[1].default_value = 0.7400000095367432

    # Node Math.013
    math_013 = neck_1.nodes.new("ShaderNodeMath")
    math_013.name = "Math.013"
    math_013.operation = 'ABSOLUTE'
    math_013.use_clamp = False

    # Node Set Curve Tilt.003
    set_curve_tilt_003 = neck_1.nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt_003.name = "Set Curve Tilt.003"
    # Selection
    set_curve_tilt_003.inputs[1].default_value = True

    # Node Map Range.005
    map_range_005 = neck_1.nodes.new("ShaderNodeMapRange")
    map_range_005.name = "Map Range.005"
    map_range_005.clamp = True
    map_range_005.data_type = 'FLOAT'
    map_range_005.interpolation_type = 'LINEAR'
    # From Min
    map_range_005.inputs[1].default_value = 0.0
    # From Max
    map_range_005.inputs[2].default_value = 0.08000002801418304
    # To Min
    map_range_005.inputs[3].default_value = 0.6799999475479126
    # To Max
    map_range_005.inputs[4].default_value = 0.47999998927116394

    # Node Float Curve.008
    float_curve_008 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_008.name = "Float Curve.008"
    # Mapping settings
    float_curve_008.mapping.extend = 'EXTRAPOLATED'
    float_curve_008.mapping.tone = 'STANDARD'
    float_curve_008.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_008.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_008.mapping.clip_min_x = 0.0
    float_curve_008.mapping.clip_min_y = 0.0
    float_curve_008.mapping.clip_max_x = 1.0
    float_curve_008.mapping.clip_max_y = 1.0
    float_curve_008.mapping.use_clip = True
    # Curve 0
    float_curve_008_curve_0 = float_curve_008.mapping.curves[0]
    float_curve_008_curve_0_point_0 = float_curve_008_curve_0.points[0]
    float_curve_008_curve_0_point_0.location = (0.0, 0.0)
    float_curve_008_curve_0_point_0.handle_type = 'AUTO'
    float_curve_008_curve_0_point_1 = float_curve_008_curve_0.points[1]
    float_curve_008_curve_0_point_1.location = (0.5820088982582092, 0.0)
    float_curve_008_curve_0_point_1.handle_type = 'VECTOR'
    float_curve_008_curve_0_point_2 = float_curve_008_curve_0.points.new(0.6510641574859619, 1.0)
    float_curve_008_curve_0_point_2.handle_type = 'VECTOR'
    float_curve_008_curve_0_point_3 = float_curve_008_curve_0.points.new(0.7518903017044067, 0.0)
    float_curve_008_curve_0_point_3.handle_type = 'VECTOR'
    float_curve_008_curve_0_point_4 = float_curve_008_curve_0.points.new(1.0, 0.0)
    float_curve_008_curve_0_point_4.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_008.mapping.update()
    # Factor
    float_curve_008.inputs[0].default_value = 1.0

    # Node Spline Parameter.005
    spline_parameter_005 = neck_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_005.name = "Spline Parameter.005"
    spline_parameter_005.outputs[1].hide = True
    spline_parameter_005.outputs[2].hide = True

    # Node Math.014
    math_014 = neck_1.nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.operation = 'MULTIPLY'
    math_014.use_clamp = False
    # Value_001
    math_014.inputs[1].default_value = 0.014999999664723873

    # Node Frame.020
    frame_020 = neck_1.nodes.new("NodeFrame")
    frame_020.label = "Align"
    frame_020.name = "Frame.020"
    frame_020.label_size = 20
    frame_020.shrink = True

    # Node Math.015
    math_015 = neck_1.nodes.new("ShaderNodeMath")
    math_015.name = "Math.015"
    math_015.operation = 'ADD'
    math_015.use_clamp = False

    # Node Spline Parameter.006
    spline_parameter_006 = neck_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_006.name = "Spline Parameter.006"
    spline_parameter_006.outputs[1].hide = True
    spline_parameter_006.outputs[2].hide = True

    # Node Float Curve.009
    float_curve_009 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_009.name = "Float Curve.009"
    # Mapping settings
    float_curve_009.mapping.extend = 'EXTRAPOLATED'
    float_curve_009.mapping.tone = 'STANDARD'
    float_curve_009.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_009.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_009.mapping.clip_min_x = 0.0
    float_curve_009.mapping.clip_min_y = 0.0
    float_curve_009.mapping.clip_max_x = 1.0
    float_curve_009.mapping.clip_max_y = 1.0
    float_curve_009.mapping.use_clip = True
    # Curve 0
    float_curve_009_curve_0 = float_curve_009.mapping.curves[0]
    float_curve_009_curve_0_point_0 = float_curve_009_curve_0.points[0]
    float_curve_009_curve_0_point_0.location = (0.0, 0.051724132150411606)
    float_curve_009_curve_0_point_0.handle_type = 'AUTO'
    float_curve_009_curve_0_point_1 = float_curve_009_curve_0.points[1]
    float_curve_009_curve_0_point_1.location = (0.11480366438627243, 0.0)
    float_curve_009_curve_0_point_1.handle_type = 'AUTO'
    float_curve_009_curve_0_point_2 = float_curve_009_curve_0.points.new(0.5105739831924438, 0.0)
    float_curve_009_curve_0_point_2.handle_type = 'AUTO'
    float_curve_009_curve_0_point_3 = float_curve_009_curve_0.points.new(0.5921449661254883, 0.0)
    float_curve_009_curve_0_point_3.handle_type = 'AUTO'
    float_curve_009_curve_0_point_4 = float_curve_009_curve_0.points.new(0.6827790141105652, 0.0)
    float_curve_009_curve_0_point_4.handle_type = 'AUTO'
    float_curve_009_curve_0_point_5 = float_curve_009_curve_0.points.new(0.7579061985015869, 0.0)
    float_curve_009_curve_0_point_5.handle_type = 'AUTO'
    float_curve_009_curve_0_point_6 = float_curve_009_curve_0.points.new(0.8731111884117126, 0.06834486126899719)
    float_curve_009_curve_0_point_6.handle_type = 'AUTO'
    float_curve_009_curve_0_point_7 = float_curve_009_curve_0.points.new(0.9758309125900269, 0.056034475564956665)
    float_curve_009_curve_0_point_7.handle_type = 'AUTO'
    float_curve_009_curve_0_point_8 = float_curve_009_curve_0.points.new(1.0, 0.0)
    float_curve_009_curve_0_point_8.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_009.mapping.update()
    # Factor
    float_curve_009.inputs[0].default_value = 1.0

    # Node Float Curve.010
    float_curve_010 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_010.name = "Float Curve.010"
    # Mapping settings
    float_curve_010.mapping.extend = 'EXTRAPOLATED'
    float_curve_010.mapping.tone = 'STANDARD'
    float_curve_010.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_010.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_010.mapping.clip_min_x = 0.0
    float_curve_010.mapping.clip_min_y = 0.0
    float_curve_010.mapping.clip_max_x = 1.0
    float_curve_010.mapping.clip_max_y = 1.0
    float_curve_010.mapping.use_clip = True
    # Curve 0
    float_curve_010_curve_0 = float_curve_010.mapping.curves[0]
    float_curve_010_curve_0_point_0 = float_curve_010_curve_0.points[0]
    float_curve_010_curve_0_point_0.location = (0.0, 0.0)
    float_curve_010_curve_0_point_0.handle_type = 'AUTO'
    float_curve_010_curve_0_point_1 = float_curve_010_curve_0.points[1]
    float_curve_010_curve_0_point_1.location = (0.6054374575614929, 0.0)
    float_curve_010_curve_0_point_1.handle_type = 'VECTOR'
    float_curve_010_curve_0_point_2 = float_curve_010_curve_0.points.new(0.6326277852058411, 0.8665950298309326)
    float_curve_010_curve_0_point_2.handle_type = 'VECTOR'
    float_curve_010_curve_0_point_3 = float_curve_010_curve_0.points.new(0.6858005523681641, 0.0)
    float_curve_010_curve_0_point_3.handle_type = 'VECTOR'
    float_curve_010_curve_0_point_4 = float_curve_010_curve_0.points.new(0.7330248951911926, 0.0)
    float_curve_010_curve_0_point_4.handle_type = 'VECTOR'
    float_curve_010_curve_0_point_5 = float_curve_010_curve_0.points.new(0.7858133316040039, 0.412137895822525)
    float_curve_010_curve_0_point_5.handle_type = 'VECTOR'
    float_curve_010_curve_0_point_6 = float_curve_010_curve_0.points.new(0.8445226550102234, 0.0)
    float_curve_010_curve_0_point_6.handle_type = 'VECTOR'
    float_curve_010_curve_0_point_7 = float_curve_010_curve_0.points.new(1.0, 0.0)
    float_curve_010_curve_0_point_7.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_010.mapping.update()
    # Factor
    float_curve_010.inputs[0].default_value = 1.0

    # Node Spline Parameter.007
    spline_parameter_007 = neck_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_007.name = "Spline Parameter.007"
    spline_parameter_007.outputs[1].hide = True
    spline_parameter_007.outputs[2].hide = True

    # Node Math.018
    math_018 = neck_1.nodes.new("ShaderNodeMath")
    math_018.name = "Math.018"
    math_018.operation = 'MULTIPLY'
    math_018.use_clamp = False
    # Value_001
    math_018.inputs[1].default_value = -0.014999999664723873

    # Node Math.019
    math_019 = neck_1.nodes.new("ShaderNodeMath")
    math_019.name = "Math.019"
    math_019.operation = 'ADD'
    math_019.use_clamp = False

    # Node Frame.022
    frame_022 = neck_1.nodes.new("NodeFrame")
    frame_022.label = "Necklace 1"
    frame_022.name = "Frame.022"
    frame_022.label_size = 20
    frame_022.shrink = True

    # Node Quadrilateral
    quadrilateral = neck_1.nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
    quadrilateral.name = "Quadrilateral"
    quadrilateral.mode = 'RECTANGLE'
    # Width
    quadrilateral.inputs[0].default_value = 0.02500000037252903
    # Height
    quadrilateral.inputs[1].default_value = 0.014999999664723873

    # Node Fillet Curve
    fillet_curve = neck_1.nodes.new("GeometryNodeFilletCurve")
    fillet_curve.name = "Fillet Curve"
    # Radius
    fillet_curve.inputs[1].default_value = 0.007000000216066837
    # Limit Radius
    fillet_curve.inputs[2].default_value = True
    # Mode
    fillet_curve.inputs[3].default_value = 'Bézier'
    # Count
    fillet_curve.inputs[4].default_value = 1

    # Node Set Spline Type
    set_spline_type = neck_1.nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.spline_type = 'BEZIER'
    # Selection
    set_spline_type.inputs[1].default_value = True

    # Node Curve to Mesh.001
    curve_to_mesh_001 = neck_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    # Scale
    curve_to_mesh_001.inputs[2].default_value = 0.8519999980926514
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False

    # Node Curve Circle.005
    curve_circle_005 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_005.name = "Curve Circle.005"
    curve_circle_005.mode = 'RADIUS'
    # Resolution
    curve_circle_005.inputs[0].default_value = 6
    # Radius
    curve_circle_005.inputs[4].default_value = 0.003000000026077032

    # Node Frame.019
    frame_019 = neck_1.nodes.new("NodeFrame")
    frame_019.label = "Link"
    frame_019.name = "Frame.019"
    frame_019.label_size = 20
    frame_019.shrink = True

    # Node Rotate Rotation.006
    rotate_rotation_006 = neck_1.nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_006.name = "Rotate Rotation.006"
    rotate_rotation_006.rotation_space = 'LOCAL'

    # Node Rotate Rotation.005
    rotate_rotation_005 = neck_1.nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_005.name = "Rotate Rotation.005"
    rotate_rotation_005.rotation_space = 'LOCAL'

    # Node Random Value.012
    random_value_012 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_012.name = "Random Value.012"
    random_value_012.data_type = 'FLOAT_VECTOR'
    # Min
    random_value_012.inputs[0].default_value = (-0.29999998211860657, -0.09999999403953552, 0.0)
    # Max
    random_value_012.inputs[1].default_value = (0.2999999225139618, 0.09999999403953552, 0.0)
    # ID
    random_value_012.inputs[7].default_value = 0
    # Seed
    random_value_012.inputs[8].default_value = 3

    # Node Index.001
    index_001 = neck_1.nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"

    # Node Math.016
    math_016 = neck_1.nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.hide = True
    math_016.operation = 'FLOORED_MODULO'
    math_016.use_clamp = False
    # Value_001
    math_016.inputs[1].default_value = 2.0

    # Node Switch.001
    switch_001 = neck_1.nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.input_type = 'FLOAT'
    # False
    switch_001.inputs[1].default_value = -0.3799999952316284
    # True
    switch_001.inputs[2].default_value = 0.5

    # Node Combine XYZ.006
    combine_xyz_006 = neck_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_006.name = "Combine XYZ.006"
    combine_xyz_006.inputs[1].hide = True
    combine_xyz_006.inputs[2].hide = True
    # Y
    combine_xyz_006.inputs[1].default_value = 0.0
    # Z
    combine_xyz_006.inputs[2].default_value = 0.0

    # Node Join Geometry.012
    join_geometry_012 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_012.name = "Join Geometry.012"
    join_geometry_012.hide = True

    # Node Curve Circle.006
    curve_circle_006 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_006.name = "Curve Circle.006"
    curve_circle_006.mode = 'RADIUS'
    # Resolution
    curve_circle_006.inputs[0].default_value = 15
    # Radius
    curve_circle_006.inputs[4].default_value = 0.009999999776482582

    # Node Curve to Mesh.002
    curve_to_mesh_002 = neck_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    # Scale
    curve_to_mesh_002.inputs[2].default_value = 0.22200000286102295
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False

    # Node Sample Curve.001
    sample_curve_001 = neck_1.nodes.new("GeometryNodeSampleCurve")
    sample_curve_001.name = "Sample Curve.001"
    sample_curve_001.data_type = 'FLOAT'
    sample_curve_001.mode = 'FACTOR'
    sample_curve_001.use_all_curves = True
    # Value
    sample_curve_001.inputs[1].default_value = 0.0
    # Factor
    sample_curve_001.inputs[2].default_value = 0.7185045480728149

    # Node Transform Geometry.022
    transform_geometry_022 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_022.name = "Transform Geometry.022"
    # Mode
    transform_geometry_022.inputs[1].default_value = 'Components'
    # Rotation
    transform_geometry_022.inputs[3].default_value = (1.5707963705062866, 0.0, 0.34033918380737305)
    # Scale
    transform_geometry_022.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Join Geometry.013
    join_geometry_013 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_013.name = "Join Geometry.013"

    # Node Vector Math.005
    vector_math_005 = neck_1.nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.operation = 'ADD'
    # Vector_001
    vector_math_005.inputs[1].default_value = (0.0, 0.0, -0.012000000104308128)

    # Node Curve Circle.007
    curve_circle_007 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_007.name = "Curve Circle.007"
    curve_circle_007.mode = 'RADIUS'
    # Resolution
    curve_circle_007.inputs[0].default_value = 6
    # Radius
    curve_circle_007.inputs[4].default_value = 0.009999999776482582

    # Node Curve Line
    curve_line = neck_1.nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.mode = 'DIRECTION'
    # Start
    curve_line.inputs[0].default_value = (0.0, 0.0, -0.009999999776482582)
    # Direction
    curve_line.inputs[2].default_value = (0.0, 0.0, -1.0)
    # Length
    curve_line.inputs[3].default_value = 0.05000000074505806

    # Node Transform Geometry.023
    transform_geometry_023 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_023.name = "Transform Geometry.023"
    # Mode
    transform_geometry_023.inputs[1].default_value = 'Components'
    # Rotation
    transform_geometry_023.inputs[3].default_value = (0.0, 0.06632250547409058, -0.6752678751945496)
    # Scale
    transform_geometry_023.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Frame.021
    frame_021 = neck_1.nodes.new("NodeFrame")
    frame_021.label = "Loop"
    frame_021.name = "Frame.021"
    frame_021.label_size = 20
    frame_021.shrink = True

    # Node Vector Math.006
    vector_math_006 = neck_1.nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.operation = 'ADD'
    # Vector_001
    vector_math_006.inputs[1].default_value = (0.0, 0.0, -0.017999999225139618)

    # Node Curve to Mesh.003
    curve_to_mesh_003 = neck_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.name = "Curve to Mesh.003"
    # Fill Caps
    curve_to_mesh_003.inputs[3].default_value = True

    # Node Resample Curve.005
    resample_curve_005 = neck_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_005.name = "Resample Curve.005"
    resample_curve_005.keep_last_segment = True
    # Selection
    resample_curve_005.inputs[1].default_value = True
    # Mode
    resample_curve_005.inputs[2].default_value = 'Count'
    # Count
    resample_curve_005.inputs[3].default_value = 128
    # Length
    resample_curve_005.inputs[4].default_value = 0.10000000149011612

    # Node Curve Circle.008
    curve_circle_008 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_008.name = "Curve Circle.008"
    curve_circle_008.mode = 'RADIUS'
    # Resolution
    curve_circle_008.inputs[0].default_value = 32
    # Radius
    curve_circle_008.inputs[4].default_value = 0.003000000026077032

    # Node Spline Parameter.008
    spline_parameter_008 = neck_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_008.name = "Spline Parameter.008"

    # Node Float Curve.011
    float_curve_011 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_011.name = "Float Curve.011"
    # Mapping settings
    float_curve_011.mapping.extend = 'EXTRAPOLATED'
    float_curve_011.mapping.tone = 'STANDARD'
    float_curve_011.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_011.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_011.mapping.clip_min_x = 0.0
    float_curve_011.mapping.clip_min_y = 0.0
    float_curve_011.mapping.clip_max_x = 1.0
    float_curve_011.mapping.clip_max_y = 1.0
    float_curve_011.mapping.use_clip = True
    # Curve 0
    float_curve_011_curve_0 = float_curve_011.mapping.curves[0]
    float_curve_011_curve_0_point_0 = float_curve_011_curve_0.points[0]
    float_curve_011_curve_0_point_0.location = (0.0, 0.0)
    float_curve_011_curve_0_point_0.handle_type = 'AUTO'
    float_curve_011_curve_0_point_1 = float_curve_011_curve_0.points[1]
    float_curve_011_curve_0_point_1.location = (0.06646518409252167, 0.4784483015537262)
    float_curve_011_curve_0_point_1.handle_type = 'AUTO'
    float_curve_011_curve_0_point_2 = float_curve_011_curve_0.points.new(0.29607266187667847, 0.5715513229370117)
    float_curve_011_curve_0_point_2.handle_type = 'VECTOR'
    float_curve_011_curve_0_point_3 = float_curve_011_curve_0.points.new(0.3444109857082367, 1.0)
    float_curve_011_curve_0_point_3.handle_type = 'AUTO'
    float_curve_011_curve_0_point_4 = float_curve_011_curve_0.points.new(0.39274948835372925, 0.5456891059875488)
    float_curve_011_curve_0_point_4.handle_type = 'VECTOR'
    float_curve_011_curve_0_point_5 = float_curve_011_curve_0.points.new(0.41691839694976807, 0.9181031584739685)
    float_curve_011_curve_0_point_5.handle_type = 'AUTO'
    float_curve_011_curve_0_point_6 = float_curve_011_curve_0.points.new(0.453172504901886, 0.5370684862136841)
    float_curve_011_curve_0_point_6.handle_type = 'VECTOR'
    float_curve_011_curve_0_point_7 = float_curve_011_curve_0.points.new(0.7797576189041138, 0.5099135041236877)
    float_curve_011_curve_0_point_7.handle_type = 'VECTOR'
    float_curve_011_curve_0_point_8 = float_curve_011_curve_0.points.new(0.7978847026824951, 0.8547418713569641)
    float_curve_011_curve_0_point_8.handle_type = 'AUTO'
    float_curve_011_curve_0_point_9 = float_curve_011_curve_0.points.new(0.8129922151565552, 0.5135772824287415)
    float_curve_011_curve_0_point_9.handle_type = 'VECTOR'
    float_curve_011_curve_0_point_10 = float_curve_011_curve_0.points.new(0.9456192255020142, 0.4913792312145233)
    float_curve_011_curve_0_point_10.handle_type = 'AUTO'
    float_curve_011_curve_0_point_11 = float_curve_011_curve_0.points.new(1.0, 0.2364218682050705)
    float_curve_011_curve_0_point_11.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_011.mapping.update()
    # Factor
    float_curve_011.inputs[0].default_value = 1.0

    # Node Curve Circle.009
    curve_circle_009 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_009.name = "Curve Circle.009"
    curve_circle_009.mode = 'RADIUS'
    # Resolution
    curve_circle_009.inputs[0].default_value = 12
    # Radius
    curve_circle_009.inputs[4].default_value = 0.004000000189989805

    # Node Curve to Mesh.004
    curve_to_mesh_004 = neck_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_004.name = "Curve to Mesh.004"
    # Scale
    curve_to_mesh_004.inputs[2].default_value = 0.800000011920929
    # Fill Caps
    curve_to_mesh_004.inputs[3].default_value = True

    # Node Curve Circle.010
    curve_circle_010 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_010.name = "Curve Circle.010"
    curve_circle_010.mode = 'RADIUS'
    # Resolution
    curve_circle_010.inputs[0].default_value = 6
    # Radius
    curve_circle_010.inputs[4].default_value = 0.0020000000949949026

    # Node Join Geometry.014
    join_geometry_014 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_014.name = "Join Geometry.014"
    join_geometry_014.hide = True

    # Node Curve Circle.011
    curve_circle_011 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_011.name = "Curve Circle.011"
    curve_circle_011.mode = 'RADIUS'
    # Resolution
    curve_circle_011.inputs[0].default_value = 6
    # Radius
    curve_circle_011.inputs[4].default_value = 0.00800000037997961

    # Node Instance on Points.006
    instance_on_points_006 = neck_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_006.name = "Instance on Points.006"
    # Selection
    instance_on_points_006.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_006.inputs[3].default_value = False
    # Instance Index
    instance_on_points_006.inputs[4].default_value = 0
    # Rotation
    instance_on_points_006.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points_006.inputs[6].default_value = (1.0, 1.0, 1.0)

    # Node Transform Geometry.024
    transform_geometry_024 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_024.name = "Transform Geometry.024"
    # Mode
    transform_geometry_024.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_024.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_024.inputs[3].default_value = (1.5707963705062866, 0.5235987901687622, 0.0)
    # Scale
    transform_geometry_024.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Grid
    grid = neck_1.nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    # Size X
    grid.inputs[0].default_value = 0.014999999664723873
    # Size Y
    grid.inputs[1].default_value = 0.012000000104308128
    # Vertices X
    grid.inputs[2].default_value = 12
    # Vertices Y
    grid.inputs[3].default_value = 4

    # Node Delete Geometry.001
    delete_geometry_001 = neck_1.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.domain = 'FACE'
    delete_geometry_001.mode = 'ALL'

    # Node Random Value.013
    random_value_013 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_013.name = "Random Value.013"
    random_value_013.data_type = 'BOOLEAN'
    # Probability
    random_value_013.inputs[6].default_value = 0.2734806537628174
    # ID
    random_value_013.inputs[7].default_value = 0
    # Seed
    random_value_013.inputs[8].default_value = 78

    # Node Extrude Mesh
    extrude_mesh = neck_1.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.mode = 'FACES'
    # Selection
    extrude_mesh.inputs[1].default_value = True
    # Offset
    extrude_mesh.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset Scale
    extrude_mesh.inputs[3].default_value = 0.003000000026077032
    # Individual
    extrude_mesh.inputs[4].default_value = False

    # Node Flip Faces
    flip_faces = neck_1.nodes.new("GeometryNodeFlipFaces")
    flip_faces.name = "Flip Faces"
    # Selection
    flip_faces.inputs[1].default_value = True

    # Node Join Geometry.015
    join_geometry_015 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_015.name = "Join Geometry.015"
    join_geometry_015.hide = True

    # Node Merge by Distance
    merge_by_distance = neck_1.nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    # Selection
    merge_by_distance.inputs[1].default_value = True
    # Mode
    merge_by_distance.inputs[2].default_value = 'All'
    # Distance
    merge_by_distance.inputs[3].default_value = 9.999999747378752e-05

    # Node Transform Geometry.025
    transform_geometry_025 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_025.name = "Transform Geometry.025"
    # Mode
    transform_geometry_025.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_025.inputs[2].default_value = (0.006000000052154064, 0.001500000013038516, -0.04999999701976776)
    # Rotation
    transform_geometry_025.inputs[3].default_value = (1.5707963705062866, -1.5707963705062866, 0.0)
    # Scale
    transform_geometry_025.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Subdivision Surface
    subdivision_surface = neck_1.nodes.new("GeometryNodeSubdivisionSurface")
    subdivision_surface.name = "Subdivision Surface"
    # Level
    subdivision_surface.inputs[1].default_value = 1
    # Edge Crease
    subdivision_surface.inputs[2].default_value = 0.8063265681266785
    # Vertex Crease
    subdivision_surface.inputs[3].default_value = 0.0
    # Limit Surface
    subdivision_surface.inputs[4].default_value = True
    # UV Smooth
    subdivision_surface.inputs[5].default_value = 'Keep Boundaries'
    # Boundary Smooth
    subdivision_surface.inputs[6].default_value = 'All'

    # Node Set Shade Smooth.001
    set_shade_smooth_001 = neck_1.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.name = "Set Shade Smooth.001"
    set_shade_smooth_001.domain = 'FACE'
    # Selection
    set_shade_smooth_001.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_001.inputs[2].default_value = True

    # Node Frame.023
    frame_023 = neck_1.nodes.new("NodeFrame")
    frame_023.label = "Key"
    frame_023.name = "Frame.023"
    frame_023.label_size = 20
    frame_023.shrink = True

    # Node Store Named Attribute.007
    store_named_attribute_007 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_007.name = "Store Named Attribute.007"
    store_named_attribute_007.data_type = 'BOOLEAN'
    store_named_attribute_007.domain = 'POINT'
    # Selection
    store_named_attribute_007.inputs[1].default_value = True
    # Name
    store_named_attribute_007.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_007.inputs[3].default_value = True

    # Node Frame.024
    frame_024 = neck_1.nodes.new("NodeFrame")
    frame_024.label = "Necklaces"
    frame_024.name = "Frame.024"
    frame_024.label_size = 20
    frame_024.shrink = True

    # Node Ico Sphere.006
    ico_sphere_006 = neck_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_006.name = "Ico Sphere.006"
    # Radius
    ico_sphere_006.inputs[0].default_value = 0.029999999329447746
    # Subdivisions
    ico_sphere_006.inputs[1].default_value = 3

    # Node Transform Geometry.026
    transform_geometry_026 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_026.name = "Transform Geometry.026"
    # Mode
    transform_geometry_026.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_026.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_026.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_026.inputs[4].default_value = (1.0, 1.0, 0.5)

    # Node Instance on Points.007
    instance_on_points_007 = neck_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_007.name = "Instance on Points.007"
    # Selection
    instance_on_points_007.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_007.inputs[3].default_value = False
    # Instance Index
    instance_on_points_007.inputs[4].default_value = 0
    # Rotation
    instance_on_points_007.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points_007.inputs[6].default_value = (1.0, 1.0, 1.0)

    # Node Quadratic Bézier
    quadratic_b_zier = neck_1.nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_b_zier.name = "Quadratic Bézier"
    # Resolution
    quadratic_b_zier.inputs[0].default_value = 16
    # Start
    quadratic_b_zier.inputs[1].default_value = (-0.019999999552965164, 0.0, 0.0)
    # Middle
    quadratic_b_zier.inputs[2].default_value = (0.0, 0.009999999776482582, 0.009999999776482582)
    # End
    quadratic_b_zier.inputs[3].default_value = (0.019999999552965164, 0.0, 0.0)

    # Node Realize Instances.003
    realize_instances_003 = neck_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_003.name = "Realize Instances.003"
    # Selection
    realize_instances_003.inputs[1].default_value = True
    # Realize All
    realize_instances_003.inputs[2].default_value = True
    # Depth
    realize_instances_003.inputs[3].default_value = 0

    # Node Mesh to SDF Grid
    mesh_to_sdf_grid = neck_1.nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_sdf_grid.name = "Mesh to SDF Grid"
    # Voxel Size
    mesh_to_sdf_grid.inputs[1].default_value = 0.009999999776482582
    # Band Width
    mesh_to_sdf_grid.inputs[2].default_value = 1

    # Node Grid to Mesh
    grid_to_mesh = neck_1.nodes.new("GeometryNodeGridToMesh")
    grid_to_mesh.name = "Grid to Mesh"
    # Threshold
    grid_to_mesh.inputs[1].default_value = 0.0
    # Adaptivity
    grid_to_mesh.inputs[2].default_value = 0.0

    # Node Dual Mesh.001
    dual_mesh_001 = neck_1.nodes.new("GeometryNodeDualMesh")
    dual_mesh_001.name = "Dual Mesh.001"
    # Keep Boundaries
    dual_mesh_001.inputs[1].default_value = False

    # Node Triangulate
    triangulate = neck_1.nodes.new("GeometryNodeTriangulate")
    triangulate.name = "Triangulate"
    # Selection
    triangulate.inputs[1].default_value = True
    # Quad Method
    triangulate.inputs[2].default_value = 'Shortest Diagonal'
    # N-gon Method
    triangulate.inputs[3].default_value = 'Beauty'

    # Node SDF Grid Boolean
    sdf_grid_boolean = neck_1.nodes.new("GeometryNodeSDFGridBoolean")
    sdf_grid_boolean.name = "SDF Grid Boolean"
    sdf_grid_boolean.operation = 'INTERSECT'

    # Node Cube
    cube = neck_1.nodes.new("GeometryNodeMeshCube")
    cube.name = "Cube"
    # Size
    cube.inputs[0].default_value = (1.0, 1.0, 0.019999999552965164)
    # Vertices X
    cube.inputs[1].default_value = 2
    # Vertices Y
    cube.inputs[2].default_value = 2
    # Vertices Z
    cube.inputs[3].default_value = 2

    # Node Mesh to SDF Grid.001
    mesh_to_sdf_grid_001 = neck_1.nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_sdf_grid_001.name = "Mesh to SDF Grid.001"
    # Voxel Size
    mesh_to_sdf_grid_001.inputs[1].default_value = 0.009999999776482582
    # Band Width
    mesh_to_sdf_grid_001.inputs[2].default_value = 1

    # Node Transform Geometry.027
    transform_geometry_027 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_027.name = "Transform Geometry.027"
    # Mode
    transform_geometry_027.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_027.inputs[2].default_value = (0.0, 0.0, 0.009999999776482582)
    # Rotation
    transform_geometry_027.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_027.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Mesh Boolean
    mesh_boolean = neck_1.nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean.name = "Mesh Boolean"
    mesh_boolean.operation = 'DIFFERENCE'
    mesh_boolean.solver = 'MANIFOLD'

    # Node Cube.001
    cube_001 = neck_1.nodes.new("GeometryNodeMeshCube")
    cube_001.name = "Cube.001"
    # Size
    cube_001.inputs[0].default_value = (1.0, 1.0, 1.0)
    # Vertices X
    cube_001.inputs[1].default_value = 2
    # Vertices Y
    cube_001.inputs[2].default_value = 2
    # Vertices Z
    cube_001.inputs[3].default_value = 2

    # Node Transform Geometry.028
    transform_geometry_028 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_028.name = "Transform Geometry.028"
    # Mode
    transform_geometry_028.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_028.inputs[2].default_value = (0.5, 0.0, 0.0)
    # Rotation
    transform_geometry_028.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_028.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Delete Geometry.002
    delete_geometry_002 = neck_1.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.name = "Delete Geometry.002"
    delete_geometry_002.domain = 'FACE'
    delete_geometry_002.mode = 'ALL'

    # Node Mesh Boolean.001
    mesh_boolean_001 = neck_1.nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean_001.name = "Mesh Boolean.001"
    mesh_boolean_001.operation = 'INTERSECT'
    mesh_boolean_001.solver = 'MANIFOLD'

    # Node Cube.002
    cube_002 = neck_1.nodes.new("GeometryNodeMeshCube")
    cube_002.name = "Cube.002"
    # Size
    cube_002.inputs[0].default_value = (1.0, 1.0, 0.0010000000474974513)
    # Vertices X
    cube_002.inputs[1].default_value = 2
    # Vertices Y
    cube_002.inputs[2].default_value = 2
    # Vertices Z
    cube_002.inputs[3].default_value = 2

    # Node Transform Geometry.029
    transform_geometry_029 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_029.name = "Transform Geometry.029"
    # Mode
    transform_geometry_029.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_029.inputs[2].default_value = (0.0, 0.0, 0.004000000189989805)
    # Rotation
    transform_geometry_029.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_029.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Join Geometry.016
    join_geometry_016 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_016.name = "Join Geometry.016"
    join_geometry_016.hide = True

    # Node Delete Geometry.003
    delete_geometry_003 = neck_1.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_003.name = "Delete Geometry.003"
    delete_geometry_003.domain = 'POINT'
    delete_geometry_003.mode = 'ALL'

    # Node Normal.003
    normal_003 = neck_1.nodes.new("GeometryNodeInputNormal")
    normal_003.name = "Normal.003"
    normal_003.legacy_corner_normals = False

    # Node Compare.008
    compare_008 = neck_1.nodes.new("FunctionNodeCompare")
    compare_008.name = "Compare.008"
    compare_008.data_type = 'VECTOR'
    compare_008.mode = 'DIRECTION'
    compare_008.operation = 'EQUAL'
    # B_VEC3
    compare_008.inputs[5].default_value = (0.0, 0.0, 1.0)
    # Angle
    compare_008.inputs[11].default_value = 0.0
    # Epsilon
    compare_008.inputs[12].default_value = 1.5707963705062866

    # Node Mesh to Curve.003
    mesh_to_curve_003 = neck_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_003.name = "Mesh to Curve.003"
    mesh_to_curve_003.mode = 'EDGES'
    # Selection
    mesh_to_curve_003.inputs[1].default_value = True

    # Node Resample Curve.006
    resample_curve_006 = neck_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_006.name = "Resample Curve.006"
    resample_curve_006.keep_last_segment = True
    # Selection
    resample_curve_006.inputs[1].default_value = True
    # Mode
    resample_curve_006.inputs[2].default_value = 'Count'
    # Count
    resample_curve_006.inputs[3].default_value = 45
    # Length
    resample_curve_006.inputs[4].default_value = 0.10000000149011612

    # Node Set Spline Cyclic.002
    set_spline_cyclic_002 = neck_1.nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_002.name = "Set Spline Cyclic.002"
    # Selection
    set_spline_cyclic_002.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic_002.inputs[2].default_value = True

    # Node Curve to Mesh.005
    curve_to_mesh_005 = neck_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_005.name = "Curve to Mesh.005"
    # Scale
    curve_to_mesh_005.inputs[2].default_value = 0.009999999776482582
    # Fill Caps
    curve_to_mesh_005.inputs[3].default_value = False

    # Node Gem in Holder.003
    gem_in_holder_003 = neck_1.nodes.new("GeometryNodeGroup")
    gem_in_holder_003.name = "Gem in Holder.003"
    gem_in_holder_003.node_tree = bpy.data.node_groups[node_tree_names[gem_in_holder_1_node_group]]
    gem_in_holder_003.inputs[0].hide = True
    gem_in_holder_003.inputs[1].hide = True
    gem_in_holder_003.inputs[2].hide = True
    gem_in_holder_003.inputs[3].hide = True
    gem_in_holder_003.inputs[4].hide = True
    gem_in_holder_003.inputs[5].hide = True
    gem_in_holder_003.inputs[6].hide = True
    gem_in_holder_003.inputs[7].hide = True
    gem_in_holder_003.inputs[8].hide = True
    gem_in_holder_003.inputs[9].hide = True
    gem_in_holder_003.inputs[10].hide = True
    gem_in_holder_003.outputs[0].hide = True
    gem_in_holder_003.outputs[2].hide = True
    gem_in_holder_003.outputs[3].hide = True
    gem_in_holder_003.outputs[4].hide = True
    # Socket_3
    gem_in_holder_003.inputs[0].default_value = 0.009999999776482582
    # Socket_11
    gem_in_holder_003.inputs[1].default_value = "ruby"
    # Socket_12
    gem_in_holder_003.inputs[2].default_value = False
    # Socket_4
    gem_in_holder_003.inputs[3].default_value = 0.004999995231628418
    # Socket_1
    gem_in_holder_003.inputs[4].default_value = 6
    # Socket_2
    gem_in_holder_003.inputs[5].default_value = 41
    # Socket_13
    gem_in_holder_003.inputs[6].default_value = False
    # Socket_10
    gem_in_holder_003.inputs[7].default_value = 6
    # Socket_7
    gem_in_holder_003.inputs[8].default_value = 10
    # Socket_8
    gem_in_holder_003.inputs[9].default_value = 0.0020000000949949026
    # Socket_9
    gem_in_holder_003.inputs[10].default_value = 3.3099989891052246

    # Node Trim Curve.005
    trim_curve_005 = neck_1.nodes.new("GeometryNodeTrimCurve")
    trim_curve_005.name = "Trim Curve.005"
    trim_curve_005.mode = 'FACTOR'
    # Selection
    trim_curve_005.inputs[1].default_value = True
    # Start
    trim_curve_005.inputs[2].default_value = 0.010773210786283016
    # End
    trim_curve_005.inputs[3].default_value = 0.9906079769134521

    # Node Instance on Points.008
    instance_on_points_008 = neck_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_008.name = "Instance on Points.008"
    # Selection
    instance_on_points_008.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_008.inputs[3].default_value = False
    # Instance Index
    instance_on_points_008.inputs[4].default_value = 0

    # Node Resample Curve.007
    resample_curve_007 = neck_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_007.name = "Resample Curve.007"
    resample_curve_007.keep_last_segment = True
    # Selection
    resample_curve_007.inputs[1].default_value = True
    # Mode
    resample_curve_007.inputs[2].default_value = 'Count'
    # Count
    resample_curve_007.inputs[3].default_value = 10
    # Length
    resample_curve_007.inputs[4].default_value = 0.10000000149011612

    # Node Align Rotation to Vector.004
    align_rotation_to_vector_004 = neck_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_004.name = "Align Rotation to Vector.004"
    align_rotation_to_vector_004.axis = 'Y'
    align_rotation_to_vector_004.pivot_axis = 'AUTO'
    # Rotation
    align_rotation_to_vector_004.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Factor
    align_rotation_to_vector_004.inputs[1].default_value = 1.0

    # Node Curve Tangent.003
    curve_tangent_003 = neck_1.nodes.new("GeometryNodeInputTangent")
    curve_tangent_003.name = "Curve Tangent.003"

    # Node Realize Instances.004
    realize_instances_004 = neck_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_004.name = "Realize Instances.004"
    # Selection
    realize_instances_004.inputs[1].default_value = True
    # Realize All
    realize_instances_004.inputs[2].default_value = True
    # Depth
    realize_instances_004.inputs[3].default_value = 0

    # Node Transform Geometry.030
    transform_geometry_030 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_030.name = "Transform Geometry.030"
    # Mode
    transform_geometry_030.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_030.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_030.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_030.inputs[4].default_value = (-1.0, 1.0, 1.0)

    # Node Flip Faces.002
    flip_faces_002 = neck_1.nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.name = "Flip Faces.002"
    # Selection
    flip_faces_002.inputs[1].default_value = True

    # Node Join Geometry.018
    join_geometry_018 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_018.name = "Join Geometry.018"

    # Node Merge by Distance.001
    merge_by_distance_001 = neck_1.nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_001.name = "Merge by Distance.001"
    # Mode
    merge_by_distance_001.inputs[2].default_value = 'All'
    # Distance
    merge_by_distance_001.inputs[3].default_value = 0.0010000000474974513

    # Node Is Edge Boundary.001
    is_edge_boundary_001 = neck_1.nodes.new("GeometryNodeGroup")
    is_edge_boundary_001.name = "Is Edge Boundary.001"
    is_edge_boundary_001.node_tree = bpy.data.node_groups[node_tree_names[is_edge_boundary_1_node_group]]

    # Node Spline Parameter.009
    spline_parameter_009 = neck_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_009.name = "Spline Parameter.009"
    spline_parameter_009.outputs[1].hide = True
    spline_parameter_009.outputs[2].hide = True

    # Node Math.020
    math_020 = neck_1.nodes.new("ShaderNodeMath")
    math_020.name = "Math.020"
    math_020.operation = 'MULTIPLY'
    math_020.use_clamp = False
    # Value_001
    math_020.inputs[1].default_value = 2.0

    # Node Math.021
    math_021 = neck_1.nodes.new("ShaderNodeMath")
    math_021.name = "Math.021"
    math_021.operation = 'PINGPONG'
    math_021.use_clamp = False
    # Value_001
    math_021.inputs[1].default_value = 1.0

    # Node Curve to Points.002
    curve_to_points_002 = neck_1.nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_002.name = "Curve to Points.002"
    curve_to_points_002.mode = 'EVALUATED'

    # Node Points to Curves
    points_to_curves = neck_1.nodes.new("GeometryNodePointsToCurves")
    points_to_curves.name = "Points to Curves"
    # Curve Group ID
    points_to_curves.inputs[1].default_value = 0

    # Node Gradient Texture
    gradient_texture = neck_1.nodes.new("ShaderNodeTexGradient")
    gradient_texture.name = "Gradient Texture"
    gradient_texture.gradient_type = 'RADIAL'
    # Vector
    gradient_texture.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Math.022
    math_022 = neck_1.nodes.new("ShaderNodeMath")
    math_022.name = "Math.022"
    math_022.operation = 'ADD'
    math_022.use_clamp = False
    # Value_001
    math_022.inputs[1].default_value = 0.5

    # Node Math.023
    math_023 = neck_1.nodes.new("ShaderNodeMath")
    math_023.name = "Math.023"
    math_023.operation = 'FRACT'
    math_023.use_clamp = False

    # Node Delete Geometry.004
    delete_geometry_004 = neck_1.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_004.name = "Delete Geometry.004"
    delete_geometry_004.domain = 'POINT'
    delete_geometry_004.mode = 'ALL'

    # Node Position.009
    position_009 = neck_1.nodes.new("GeometryNodeInputPosition")
    position_009.name = "Position.009"

    # Node Separate XYZ.008
    separate_xyz_008 = neck_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_008.name = "Separate XYZ.008"

    # Node Compare.009
    compare_009 = neck_1.nodes.new("FunctionNodeCompare")
    compare_009.name = "Compare.009"
    compare_009.data_type = 'FLOAT'
    compare_009.mode = 'ELEMENT'
    compare_009.operation = 'GREATER_THAN'
    # B
    compare_009.inputs[1].default_value = 0.0

    # Node Float Curve.012
    float_curve_012 = neck_1.nodes.new("ShaderNodeFloatCurve")
    float_curve_012.name = "Float Curve.012"
    # Mapping settings
    float_curve_012.mapping.extend = 'EXTRAPOLATED'
    float_curve_012.mapping.tone = 'STANDARD'
    float_curve_012.mapping.black_level = (0.0, 0.0, 0.0)
    float_curve_012.mapping.white_level = (1.0, 1.0, 1.0)
    float_curve_012.mapping.clip_min_x = 0.0
    float_curve_012.mapping.clip_min_y = 0.0
    float_curve_012.mapping.clip_max_x = 1.0
    float_curve_012.mapping.clip_max_y = 1.0
    float_curve_012.mapping.use_clip = True
    # Curve 0
    float_curve_012_curve_0 = float_curve_012.mapping.curves[0]
    float_curve_012_curve_0_point_0 = float_curve_012_curve_0.points[0]
    float_curve_012_curve_0_point_0.location = (0.0, 1.0)
    float_curve_012_curve_0_point_0.handle_type = 'AUTO'
    float_curve_012_curve_0_point_1 = float_curve_012_curve_0.points[1]
    float_curve_012_curve_0_point_1.location = (0.21752268075942993, 0.6163792610168457)
    float_curve_012_curve_0_point_1.handle_type = 'AUTO'
    float_curve_012_curve_0_point_2 = float_curve_012_curve_0.points.new(0.5830820798873901, 0.9827589988708496)
    float_curve_012_curve_0_point_2.handle_type = 'AUTO'
    float_curve_012_curve_0_point_3 = float_curve_012_curve_0.points.new(1.0, 1.0)
    float_curve_012_curve_0_point_3.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_012.mapping.update()
    # Factor
    float_curve_012.inputs[0].default_value = 1.0

    # Node Transform Geometry.031
    transform_geometry_031 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_031.name = "Transform Geometry.031"
    # Mode
    transform_geometry_031.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_031.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_031.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_031.inputs[4].default_value = (-1.0, 1.0, 1.0)

    # Node Flip Faces.003
    flip_faces_003 = neck_1.nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.name = "Flip Faces.003"
    # Selection
    flip_faces_003.inputs[1].default_value = True

    # Node Join Geometry.019
    join_geometry_019 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_019.name = "Join Geometry.019"
    join_geometry_019.hide = True

    # Node Gem in Holder.004
    gem_in_holder_004 = neck_1.nodes.new("GeometryNodeGroup")
    gem_in_holder_004.name = "Gem in Holder.004"
    gem_in_holder_004.node_tree = bpy.data.node_groups[node_tree_names[gem_in_holder_1_node_group]]
    gem_in_holder_004.inputs[0].hide = True
    gem_in_holder_004.inputs[1].hide = True
    gem_in_holder_004.inputs[2].hide = True
    gem_in_holder_004.inputs[3].hide = True
    gem_in_holder_004.inputs[4].hide = True
    gem_in_holder_004.inputs[5].hide = True
    gem_in_holder_004.inputs[6].hide = True
    gem_in_holder_004.inputs[7].hide = True
    gem_in_holder_004.inputs[8].hide = True
    gem_in_holder_004.inputs[9].hide = True
    gem_in_holder_004.inputs[10].hide = True
    gem_in_holder_004.outputs[0].hide = True
    gem_in_holder_004.outputs[1].hide = True
    gem_in_holder_004.outputs[2].hide = True
    gem_in_holder_004.outputs[4].hide = True
    # Socket_3
    gem_in_holder_004.inputs[0].default_value = 0.009999999776482582
    # Socket_11
    gem_in_holder_004.inputs[1].default_value = "ruby"
    # Socket_12
    gem_in_holder_004.inputs[2].default_value = False
    # Socket_4
    gem_in_holder_004.inputs[3].default_value = 0.004999995231628418
    # Socket_1
    gem_in_holder_004.inputs[4].default_value = 6
    # Socket_2
    gem_in_holder_004.inputs[5].default_value = 41
    # Socket_13
    gem_in_holder_004.inputs[6].default_value = False
    # Socket_10
    gem_in_holder_004.inputs[7].default_value = 6
    # Socket_7
    gem_in_holder_004.inputs[8].default_value = 10
    # Socket_8
    gem_in_holder_004.inputs[9].default_value = 0.0020000000949949026
    # Socket_9
    gem_in_holder_004.inputs[10].default_value = 3.3099989891052246

    # Node Join Geometry.020
    join_geometry_020 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_020.name = "Join Geometry.020"

    # Node Gem in Holder.005
    gem_in_holder_005 = neck_1.nodes.new("GeometryNodeGroup")
    gem_in_holder_005.name = "Gem in Holder.005"
    gem_in_holder_005.node_tree = bpy.data.node_groups[node_tree_names[gem_in_holder_1_node_group]]
    gem_in_holder_005.inputs[0].hide = True
    gem_in_holder_005.inputs[1].hide = True
    gem_in_holder_005.inputs[2].hide = True
    gem_in_holder_005.inputs[3].hide = True
    gem_in_holder_005.inputs[4].hide = True
    gem_in_holder_005.inputs[5].hide = True
    gem_in_holder_005.inputs[6].hide = True
    gem_in_holder_005.inputs[7].hide = True
    gem_in_holder_005.inputs[8].hide = True
    gem_in_holder_005.inputs[9].hide = True
    gem_in_holder_005.inputs[10].hide = True
    gem_in_holder_005.outputs[0].hide = True
    gem_in_holder_005.outputs[1].hide = True
    gem_in_holder_005.outputs[2].hide = True
    gem_in_holder_005.outputs[4].hide = True
    # Socket_3
    gem_in_holder_005.inputs[0].default_value = 0.009999999776482582
    # Socket_11
    gem_in_holder_005.inputs[1].default_value = "ruby"
    # Socket_12
    gem_in_holder_005.inputs[2].default_value = False
    # Socket_4
    gem_in_holder_005.inputs[3].default_value = 0.004999995231628418
    # Socket_1
    gem_in_holder_005.inputs[4].default_value = 6
    # Socket_2
    gem_in_holder_005.inputs[5].default_value = 41
    # Socket_13
    gem_in_holder_005.inputs[6].default_value = False
    # Socket_10
    gem_in_holder_005.inputs[7].default_value = 6
    # Socket_7
    gem_in_holder_005.inputs[8].default_value = 10
    # Socket_8
    gem_in_holder_005.inputs[9].default_value = 0.0020000000949949026
    # Socket_9
    gem_in_holder_005.inputs[10].default_value = 5.109997272491455

    # Node Transform Geometry.032
    transform_geometry_032 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_032.name = "Transform Geometry.032"
    transform_geometry_032.hide = True
    transform_geometry_032.inputs[1].hide = True
    transform_geometry_032.inputs[2].hide = True
    transform_geometry_032.inputs[3].hide = True
    transform_geometry_032.inputs[4].hide = True
    transform_geometry_032.inputs[5].hide = True
    # Mode
    transform_geometry_032.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_032.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_032.inputs[3].default_value = (0.0, 0.0, 0.01745329238474369)
    # Scale
    transform_geometry_032.inputs[4].default_value = (1.0, -1.0, 1.0)

    # Node Join Geometry.021
    join_geometry_021 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_021.name = "Join Geometry.021"
    join_geometry_021.hide = True

    # Node Flip Faces.001
    flip_faces_001 = neck_1.nodes.new("GeometryNodeFlipFaces")
    flip_faces_001.name = "Flip Faces.001"
    flip_faces_001.hide = True
    flip_faces_001.inputs[1].hide = True
    # Selection
    flip_faces_001.inputs[1].default_value = True

    # Node Gem in Holder.006
    gem_in_holder_006 = neck_1.nodes.new("GeometryNodeGroup")
    gem_in_holder_006.name = "Gem in Holder.006"
    gem_in_holder_006.node_tree = bpy.data.node_groups[node_tree_names[gem_in_holder_1_node_group]]
    # Socket_3
    gem_in_holder_006.inputs[0].default_value = 0.009999999776482582
    # Socket_11
    gem_in_holder_006.inputs[1].default_value = "ruby"
    # Socket_12
    gem_in_holder_006.inputs[2].default_value = False
    # Socket_4
    gem_in_holder_006.inputs[3].default_value = 0.004999995231628418
    # Socket_1
    gem_in_holder_006.inputs[4].default_value = 6
    # Socket_2
    gem_in_holder_006.inputs[5].default_value = 41
    # Socket_13
    gem_in_holder_006.inputs[6].default_value = False
    # Socket_10
    gem_in_holder_006.inputs[7].default_value = 6
    # Socket_7
    gem_in_holder_006.inputs[8].default_value = 6
    # Socket_8
    gem_in_holder_006.inputs[9].default_value = 0.0010000000474974513
    # Socket_9
    gem_in_holder_006.inputs[10].default_value = 4.80999755859375

    # Node Transform Geometry.033
    transform_geometry_033 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_033.name = "Transform Geometry.033"
    # Mode
    transform_geometry_033.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_033.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_033.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_033.inputs[4].default_value = (1.0, -1.0, 1.0)

    # Node Join Geometry.022
    join_geometry_022 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_022.name = "Join Geometry.022"

    # Node Flip Faces.004
    flip_faces_004 = neck_1.nodes.new("GeometryNodeFlipFaces")
    flip_faces_004.name = "Flip Faces.004"
    # Selection
    flip_faces_004.inputs[1].default_value = True

    # Node Transform Geometry.034
    transform_geometry_034 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_034.name = "Transform Geometry.034"
    # Mode
    transform_geometry_034.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_034.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_034.inputs[3].default_value = (0.0, -0.4363323152065277, 0.0)
    # Scale
    transform_geometry_034.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Join Geometry.017
    join_geometry_017 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_017.name = "Join Geometry.017"
    join_geometry_017.hide = True

    # Node Store Named Attribute.008
    store_named_attribute_008 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_008.name = "Store Named Attribute.008"
    store_named_attribute_008.data_type = 'BOOLEAN'
    store_named_attribute_008.domain = 'POINT'
    # Selection
    store_named_attribute_008.inputs[1].default_value = True
    # Name
    store_named_attribute_008.inputs[2].default_value = "gold"
    # Value
    store_named_attribute_008.inputs[3].default_value = True

    # Node Store Named Attribute.009
    store_named_attribute_009 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_009.name = "Store Named Attribute.009"
    store_named_attribute_009.data_type = 'BOOLEAN'
    store_named_attribute_009.domain = 'POINT'
    # Selection
    store_named_attribute_009.inputs[1].default_value = True
    # Name
    store_named_attribute_009.inputs[2].default_value = "saphire"
    # Value
    store_named_attribute_009.inputs[3].default_value = True

    # Node Gem in Holder.007
    gem_in_holder_007 = neck_1.nodes.new("GeometryNodeGroup")
    gem_in_holder_007.name = "Gem in Holder.007"
    gem_in_holder_007.node_tree = bpy.data.node_groups[node_tree_names[gem_in_holder_1_node_group]]
    # Socket_3
    gem_in_holder_007.inputs[0].default_value = 0.006000000052154064
    # Socket_11
    gem_in_holder_007.inputs[1].default_value = "ruby"
    # Socket_12
    gem_in_holder_007.inputs[2].default_value = False
    # Socket_4
    gem_in_holder_007.inputs[3].default_value = 0.004000000189989805
    # Socket_1
    gem_in_holder_007.inputs[4].default_value = 6
    # Socket_2
    gem_in_holder_007.inputs[5].default_value = 41
    # Socket_13
    gem_in_holder_007.inputs[6].default_value = False
    # Socket_10
    gem_in_holder_007.inputs[7].default_value = 6
    # Socket_7
    gem_in_holder_007.inputs[8].default_value = 3
    # Socket_8
    gem_in_holder_007.inputs[9].default_value = 0.0010000000474974513
    # Socket_9
    gem_in_holder_007.inputs[10].default_value = 5.309997081756592

    # Node Instance on Points.009
    instance_on_points_009 = neck_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_009.name = "Instance on Points.009"
    # Selection
    instance_on_points_009.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_009.inputs[3].default_value = False
    # Instance Index
    instance_on_points_009.inputs[4].default_value = 0
    # Rotation
    instance_on_points_009.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points_009.inputs[6].default_value = (1.0, 1.0, 1.0)

    # Node Curve Circle.012
    curve_circle_012 = neck_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_012.name = "Curve Circle.012"
    curve_circle_012.mode = 'RADIUS'
    # Resolution
    curve_circle_012.inputs[0].default_value = 12
    # Radius
    curve_circle_012.inputs[4].default_value = 0.05000000074505806

    # Node Transform Geometry.035
    transform_geometry_035 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_035.name = "Transform Geometry.035"
    # Mode
    transform_geometry_035.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_035.inputs[2].default_value = (0.0, 0.003000000026077032, 0.009999999776482582)
    # Rotation
    transform_geometry_035.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_035.inputs[4].default_value = (1.4000000953674316, 0.8999999761581421, 1.0)

    # Node Frame.025
    frame_025 = neck_1.nodes.new("NodeFrame")
    frame_025.label = "Satalite Gems"
    frame_025.name = "Frame.025"
    frame_025.label_size = 20
    frame_025.shrink = True

    # Node Frame.026
    frame_026 = neck_1.nodes.new("NodeFrame")
    frame_026.label = "Main Broach"
    frame_026.name = "Frame.026"
    frame_026.use_custom_color = True
    frame_026.color = (0.20617154240608215, 0.3163784146308899, 0.3333292603492737)
    frame_026.label_size = 20
    frame_026.shrink = True

    # Node Transform Geometry.036
    transform_geometry_036 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_036.name = "Transform Geometry.036"
    # Mode
    transform_geometry_036.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_036.inputs[2].default_value = (0.0, -0.12600000202655792, 0.36497700214385986)
    # Rotation
    transform_geometry_036.inputs[3].default_value = (0.9428269863128662, 0.0, 0.0)
    # Scale
    transform_geometry_036.inputs[4].default_value = (0.4000000059604645, 0.4000000059604645, 0.4000000059604645)

    # Node Instance on Points.010
    instance_on_points_010 = neck_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_010.name = "Instance on Points.010"
    # Selection
    instance_on_points_010.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_010.inputs[3].default_value = False
    # Instance Index
    instance_on_points_010.inputs[4].default_value = 0
    # Scale
    instance_on_points_010.inputs[6].default_value = (0.6000000238418579, 0.6000000238418579, 0.6000000238418579)

    # Node Gem in Holder.008
    gem_in_holder_008 = neck_1.nodes.new("GeometryNodeGroup")
    gem_in_holder_008.name = "Gem in Holder.008"
    gem_in_holder_008.node_tree = bpy.data.node_groups[node_tree_names[gem_in_holder_1_node_group]]
    # Socket_3
    gem_in_holder_008.inputs[0].default_value = 0.009999999776482582
    # Socket_11
    gem_in_holder_008.inputs[1].default_value = "ruby"
    # Socket_12
    gem_in_holder_008.inputs[2].default_value = True
    # Socket_4
    gem_in_holder_008.inputs[3].default_value = 0.004999999888241291
    # Socket_1
    gem_in_holder_008.inputs[4].default_value = 20
    # Socket_2
    gem_in_holder_008.inputs[5].default_value = 10
    # Socket_13
    gem_in_holder_008.inputs[6].default_value = False
    # Socket_10
    gem_in_holder_008.inputs[7].default_value = 6
    # Socket_7
    gem_in_holder_008.inputs[8].default_value = 10
    # Socket_8
    gem_in_holder_008.inputs[9].default_value = 0.0020000000949949026
    # Socket_9
    gem_in_holder_008.inputs[10].default_value = 2.5099997520446777

    # Node Realize Instances.005
    realize_instances_005 = neck_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_005.name = "Realize Instances.005"
    # Selection
    realize_instances_005.inputs[1].default_value = True
    # Realize All
    realize_instances_005.inputs[2].default_value = True
    # Depth
    realize_instances_005.inputs[3].default_value = 0

    # Node Capture Attribute.002
    capture_attribute_002 = neck_1.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.name = "Capture Attribute.002"
    capture_attribute_002.active_index = 0
    capture_attribute_002.capture_items.clear()
    capture_attribute_002.capture_items.new('FLOAT', "Index")
    capture_attribute_002.capture_items["Index"].data_type = 'INT'
    capture_attribute_002.domain = 'INSTANCE'

    # Node Index.002
    index_002 = neck_1.nodes.new("GeometryNodeInputIndex")
    index_002.name = "Index.002"

    # Node Resample Curve.008
    resample_curve_008 = neck_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_008.name = "Resample Curve.008"
    resample_curve_008.keep_last_segment = True
    # Selection
    resample_curve_008.inputs[1].default_value = True
    # Mode
    resample_curve_008.inputs[2].default_value = 'Count'
    # Count
    resample_curve_008.inputs[3].default_value = 10
    # Length
    resample_curve_008.inputs[4].default_value = 0.10000000149011612

    # Node Align Rotation to Vector.005
    align_rotation_to_vector_005 = neck_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_005.name = "Align Rotation to Vector.005"
    align_rotation_to_vector_005.axis = 'X'
    align_rotation_to_vector_005.pivot_axis = 'AUTO'
    # Rotation
    align_rotation_to_vector_005.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Factor
    align_rotation_to_vector_005.inputs[1].default_value = 1.0

    # Node Normal.004
    normal_004 = neck_1.nodes.new("GeometryNodeInputNormal")
    normal_004.name = "Normal.004"
    normal_004.legacy_corner_normals = False

    # Node Align Rotation to Vector.006
    align_rotation_to_vector_006 = neck_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_006.name = "Align Rotation to Vector.006"
    align_rotation_to_vector_006.axis = 'Y'
    align_rotation_to_vector_006.pivot_axis = 'AUTO'
    # Factor
    align_rotation_to_vector_006.inputs[1].default_value = 1.0

    # Node Curve Tangent.004
    curve_tangent_004 = neck_1.nodes.new("GeometryNodeInputTangent")
    curve_tangent_004.name = "Curve Tangent.004"

    # Node Frame.027
    frame_027 = neck_1.nodes.new("NodeFrame")
    frame_027.label = "Collar Gems"
    frame_027.name = "Frame.027"
    frame_027.label_size = 20
    frame_027.shrink = True

    # Node Trim Curve.006
    trim_curve_006 = neck_1.nodes.new("GeometryNodeTrimCurve")
    trim_curve_006.name = "Trim Curve.006"
    trim_curve_006.mode = 'FACTOR'
    # Selection
    trim_curve_006.inputs[1].default_value = True
    # Start
    trim_curve_006.inputs[2].default_value = 0.009999999776482582
    # End
    trim_curve_006.inputs[3].default_value = 0.940000057220459

    # Node Gem in Holder.009
    gem_in_holder_009 = neck_1.nodes.new("GeometryNodeGroup")
    gem_in_holder_009.name = "Gem in Holder.009"
    gem_in_holder_009.node_tree = bpy.data.node_groups[node_tree_names[gem_in_holder_1_node_group]]
    # Socket_3
    gem_in_holder_009.inputs[0].default_value = 0.009999999776482582
    # Socket_11
    gem_in_holder_009.inputs[1].default_value = "ruby"
    # Socket_12
    gem_in_holder_009.inputs[2].default_value = False
    # Socket_4
    gem_in_holder_009.inputs[3].default_value = 0.004999999888241291
    # Socket_13
    gem_in_holder_009.inputs[6].default_value = True

    # Node Curve to Points.003
    curve_to_points_003 = neck_1.nodes.new("GeometryNodeCurveToPoints")
    curve_to_points_003.name = "Curve to Points.003"
    curve_to_points_003.mode = 'COUNT'
    # Count
    curve_to_points_003.inputs[1].default_value = 2

    # Node For Each Geometry Element Input.002
    for_each_geometry_element_input_002 = neck_1.nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input_002.name = "For Each Geometry Element Input.002"
    # Node For Each Geometry Element Output.002
    for_each_geometry_element_output_002 = neck_1.nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output_002.name = "For Each Geometry Element Output.002"
    for_each_geometry_element_output_002.active_generation_index = 0
    for_each_geometry_element_output_002.active_input_index = 1
    for_each_geometry_element_output_002.active_main_index = 0
    for_each_geometry_element_output_002.domain = 'POINT'
    for_each_geometry_element_output_002.generation_items.clear()
    for_each_geometry_element_output_002.generation_items.new('GEOMETRY', "Geometry")
    for_each_geometry_element_output_002.generation_items[0].domain = 'POINT'
    for_each_geometry_element_output_002.input_items.clear()
    for_each_geometry_element_output_002.input_items.new('ROTATION', "Rotation")
    for_each_geometry_element_output_002.input_items.new('VECTOR', "Position")
    for_each_geometry_element_output_002.inspection_index = 0
    for_each_geometry_element_output_002.main_items.clear()

    # Node Position.010
    position_010 = neck_1.nodes.new("GeometryNodeInputPosition")
    position_010.name = "Position.010"

    # Node Transform Geometry.037
    transform_geometry_037 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_037.name = "Transform Geometry.037"
    # Mode
    transform_geometry_037.inputs[1].default_value = 'Components'

    # Node Rotate Rotation.007
    rotate_rotation_007 = neck_1.nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_007.name = "Rotate Rotation.007"
    rotate_rotation_007.rotation_space = 'LOCAL'
    # Rotate By
    rotate_rotation_007.inputs[1].default_value = (1.5707963705062866, 0.0, 0.0)

    # Node Random Value.014
    random_value_014 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_014.name = "Random Value.014"
    random_value_014.data_type = 'INT'
    # Min_002
    random_value_014.inputs[4].default_value = 5
    # Max_002
    random_value_014.inputs[5].default_value = 7
    # Seed
    random_value_014.inputs[8].default_value = 0

    # Node Transform Geometry.038
    transform_geometry_038 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_038.name = "Transform Geometry.038"
    # Mode
    transform_geometry_038.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_038.inputs[2].default_value = (0.0, -0.004999999888241291, 0.0)
    # Rotation
    transform_geometry_038.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_038.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Trim Curve.007
    trim_curve_007 = neck_1.nodes.new("GeometryNodeTrimCurve")
    trim_curve_007.name = "Trim Curve.007"
    trim_curve_007.mode = 'FACTOR'
    # Selection
    trim_curve_007.inputs[1].default_value = True
    # Start
    trim_curve_007.inputs[2].default_value = 0.4000000059604645
    # End
    trim_curve_007.inputs[3].default_value = 0.75

    # Node Random Value.015
    random_value_015 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_015.name = "Random Value.015"
    random_value_015.data_type = 'FLOAT'
    # Min_001
    random_value_015.inputs[2].default_value = 0.25
    # Max_001
    random_value_015.inputs[3].default_value = 0.550000011920929
    # Seed
    random_value_015.inputs[8].default_value = 0

    # Node Store Named Attribute.010
    store_named_attribute_010 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_010.name = "Store Named Attribute.010"
    store_named_attribute_010.data_type = 'BOOLEAN'
    store_named_attribute_010.domain = 'POINT'
    # Selection
    store_named_attribute_010.inputs[1].default_value = True
    # Name
    store_named_attribute_010.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_010.inputs[3].default_value = True

    # Node Random Value.016
    random_value_016 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_016.name = "Random Value.016"
    random_value_016.data_type = 'FLOAT'
    # Min_001
    random_value_016.inputs[2].default_value = 0.0
    # Max_001
    random_value_016.inputs[3].default_value = 100.0
    # Seed
    random_value_016.inputs[8].default_value = 16

    # Node Rotate Rotation.008
    rotate_rotation_008 = neck_1.nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_008.name = "Rotate Rotation.008"
    rotate_rotation_008.rotation_space = 'LOCAL'
    # Rotate By
    rotate_rotation_008.inputs[1].default_value = (0.0, 0.0, -1.5707963705062866)

    # Node Random Value.017
    random_value_017 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_017.name = "Random Value.017"
    random_value_017.data_type = 'FLOAT'
    # Min_001
    random_value_017.inputs[2].default_value = 0.0010000000474974513
    # Max_001
    random_value_017.inputs[3].default_value = 0.004999999888241291
    # Seed
    random_value_017.inputs[8].default_value = 0

    # Node Random Value.018
    random_value_018 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_018.name = "Random Value.018"
    random_value_018.data_type = 'INT'
    # Min_002
    random_value_018.inputs[4].default_value = 0
    # Max_002
    random_value_018.inputs[5].default_value = 100
    # Seed
    random_value_018.inputs[8].default_value = 0

    # Node Random Value.019
    random_value_019 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_019.name = "Random Value.019"
    random_value_019.data_type = 'INT'
    # Min_002
    random_value_019.inputs[4].default_value = 6
    # Max_002
    random_value_019.inputs[5].default_value = 20
    # Seed
    random_value_019.inputs[8].default_value = 0

    # Node Random Value.020
    random_value_020 = neck_1.nodes.new("FunctionNodeRandomValue")
    random_value_020.name = "Random Value.020"
    random_value_020.data_type = 'INT'
    # Min_002
    random_value_020.inputs[4].default_value = 5
    # Max_002
    random_value_020.inputs[5].default_value = 30
    # Seed
    random_value_020.inputs[8].default_value = 0

    # Node Frame.028
    frame_028 = neck_1.nodes.new("NodeFrame")
    frame_028.label = "Broaches"
    frame_028.name = "Frame.028"
    frame_028.label_size = 20
    frame_028.shrink = True

    # Node Store Named Attribute.011
    store_named_attribute_011 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_011.name = "Store Named Attribute.011"
    store_named_attribute_011.data_type = 'BOOLEAN'
    store_named_attribute_011.domain = 'POINT'
    # Selection
    store_named_attribute_011.inputs[1].default_value = True
    # Name
    store_named_attribute_011.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_011.inputs[3].default_value = True

    # Node Store Named Attribute.012
    store_named_attribute_012 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_012.name = "Store Named Attribute.012"
    store_named_attribute_012.data_type = 'BOOLEAN'
    store_named_attribute_012.domain = 'POINT'
    # Selection
    store_named_attribute_012.inputs[1].default_value = True
    # Name
    store_named_attribute_012.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_012.inputs[3].default_value = True

    # Node Mesh Boolean.002
    mesh_boolean_002 = neck_1.nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean_002.name = "Mesh Boolean.002"
    mesh_boolean_002.operation = 'DIFFERENCE'
    mesh_boolean_002.solver = 'FLOAT'

    # Node Ico Sphere.007
    ico_sphere_007 = neck_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_007.name = "Ico Sphere.007"
    # Radius
    ico_sphere_007.inputs[0].default_value = 0.07800000160932541
    # Subdivisions
    ico_sphere_007.inputs[1].default_value = 3

    # Node Transform Geometry.039
    transform_geometry_039 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_039.name = "Transform Geometry.039"
    # Mode
    transform_geometry_039.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_039.inputs[2].default_value = (0.0, -0.019999999552965164, 0.47999998927116394)
    # Rotation
    transform_geometry_039.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_039.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Node Store Named Attribute.013
    store_named_attribute_013 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_013.name = "Store Named Attribute.013"
    store_named_attribute_013.data_type = 'BOOLEAN'
    store_named_attribute_013.domain = 'POINT'
    # Name
    store_named_attribute_013.inputs[2].default_value = "saphire"
    # Value
    store_named_attribute_013.inputs[3].default_value = True

    # Node Boolean Math.005
    boolean_math_005 = neck_1.nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.name = "Boolean Math.005"
    boolean_math_005.operation = 'AND'

    # Node Named Attribute
    named_attribute = neck_1.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.data_type = 'BOOLEAN'
    # Name
    named_attribute.inputs[0].default_value = "ruby"

    # Node Store Named Attribute.014
    store_named_attribute_014 = neck_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_014.name = "Store Named Attribute.014"
    store_named_attribute_014.data_type = 'BOOLEAN'
    store_named_attribute_014.domain = 'POINT'
    # Name
    store_named_attribute_014.inputs[2].default_value = "ruby"
    # Value
    store_named_attribute_014.inputs[3].default_value = False

    # Node Math.017
    math_017 = neck_1.nodes.new("ShaderNodeMath")
    math_017.name = "Math.017"
    math_017.operation = 'FLOORED_MODULO'
    math_017.use_clamp = False
    # Value_001
    math_017.inputs[1].default_value = 2.0

    # Node Transform Geometry.040
    transform_geometry_040 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_040.name = "Transform Geometry.040"
    # Mode
    transform_geometry_040.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_040.inputs[2].default_value = (0.0, 0.0, 0.0007999999797903001)
    # Rotation
    transform_geometry_040.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_040.inputs[4].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929)

    # Node Transform Geometry.041
    transform_geometry_041 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_041.name = "Transform Geometry.041"
    # Mode
    transform_geometry_041.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_041.inputs[2].default_value = (0.0, 0.0, 0.0007999999797903001)
    # Rotation
    transform_geometry_041.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_041.inputs[4].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929)

    # Node Scale Elements
    scale_elements = neck_1.nodes.new("GeometryNodeScaleElements")
    scale_elements.name = "Scale Elements"
    scale_elements.domain = 'FACE'
    # Selection
    scale_elements.inputs[1].default_value = True
    # Scale
    scale_elements.inputs[2].default_value = 1.2000000476837158
    # Center
    scale_elements.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale Mode
    scale_elements.inputs[4].default_value = 'Uniform'
    # Axis
    scale_elements.inputs[5].default_value = (1.0, 0.0, 0.0)

    # Node Transform Geometry.042
    transform_geometry_042 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_042.name = "Transform Geometry.042"
    # Mode
    transform_geometry_042.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_042.inputs[2].default_value = (0.0, 0.0, 0.0005000000237487257)
    # Rotation
    transform_geometry_042.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_042.inputs[4].default_value = (1.0, 1.0, 0.7000000476837158)

    # Node Join Geometry.023
    join_geometry_023 = neck_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_023.name = "Join Geometry.023"
    join_geometry_023.hide = True

    # Node Transform Geometry.043
    transform_geometry_043 = neck_1.nodes.new("GeometryNodeTransform")
    transform_geometry_043.name = "Transform Geometry.043"
    # Mode
    transform_geometry_043.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_043.inputs[2].default_value = (0.0, 0.0, 0.0005000000237487257)
    # Rotation
    transform_geometry_043.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_043.inputs[4].default_value = (1.0, 1.0, 1.0)

    # Process zone input For Each Geometry Element Input
    for_each_geometry_element_input.pair_with_output(for_each_geometry_element_output)
    # Selection
    for_each_geometry_element_input.inputs[1].default_value = True


    # Process zone input For Each Geometry Element Input.001
    for_each_geometry_element_input_001.pair_with_output(for_each_geometry_element_output_001)
    # Selection
    for_each_geometry_element_input_001.inputs[1].default_value = True


    # Process zone input For Each Geometry Element Input.002
    for_each_geometry_element_input_002.pair_with_output(for_each_geometry_element_output_002)
    # Selection
    for_each_geometry_element_input_002.inputs[1].default_value = True



    # Process zone input Closure Input.001
    closure_input_001.pair_with_output(closure_output_001)



    # Set parents
    neck_1.nodes["Quadratic Bézier.003"].parent = neck_1.nodes["Frame.006"]
    neck_1.nodes["Bi-Rail Loft.001"].parent = neck_1.nodes["Frame.010"]
    neck_1.nodes["Quadratic Bézier.004"].parent = neck_1.nodes["Frame.006"]
    neck_1.nodes["Group.002"].parent = neck_1.nodes["Frame.006"]
    neck_1.nodes["Join Geometry.005"].parent = neck_1.nodes["Frame.006"]
    neck_1.nodes["Vector"].parent = neck_1.nodes["Frame.006"]
    neck_1.nodes["Frame.006"].parent = neck_1.nodes["Frame.008"]
    neck_1.nodes["Quadratic Bézier.006"].parent = neck_1.nodes["Frame.007"]
    neck_1.nodes["Quadratic Bézier.007"].parent = neck_1.nodes["Frame.007"]
    neck_1.nodes["Group.003"].parent = neck_1.nodes["Frame.007"]
    neck_1.nodes["Join Geometry.006"].parent = neck_1.nodes["Frame.007"]
    neck_1.nodes["Vector.001"].parent = neck_1.nodes["Frame.007"]
    neck_1.nodes["Frame.007"].parent = neck_1.nodes["Frame.008"]
    neck_1.nodes["Join Geometry.008"].parent = neck_1.nodes["Frame.008"]
    neck_1.nodes["Transform Geometry.002"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Transform Geometry.003"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Curve Circle"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Curve Circle.001"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Set Position"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Position"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Separate XYZ"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Map Range"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Frame.008"].parent = neck_1.nodes["Frame.010"]
    neck_1.nodes["Float Curve.001"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Combine XYZ"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Transform Geometry.004"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Transform Geometry.005"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Closure Input.001"].parent = neck_1.nodes["Frame.010"]
    neck_1.nodes["Closure Output.001"].parent = neck_1.nodes["Frame.010"]
    neck_1.nodes["Math"].parent = neck_1.nodes["Frame.010"]
    neck_1.nodes["Math.001"].parent = neck_1.nodes["Frame.010"]
    neck_1.nodes["Transform Geometry.001"].parent = neck_1.nodes["Frame.007"]
    neck_1.nodes["Transform Geometry.006"].parent = neck_1.nodes["Frame.006"]
    neck_1.nodes["Integer"].parent = neck_1.nodes["Frame.009"]
    neck_1.nodes["Frame.009"].parent = neck_1.nodes["Frame.010"]
    neck_1.nodes["Pipes"].parent = neck_1.nodes["Frame"]
    neck_1.nodes["Separate XYZ.002"].parent = neck_1.nodes["Frame"]
    neck_1.nodes["Compare.001"].parent = neck_1.nodes["Frame"]
    neck_1.nodes["Separate Geometry"].parent = neck_1.nodes["Frame"]
    neck_1.nodes["Join Geometry.001"].parent = neck_1.nodes["Frame"]
    neck_1.nodes["Join Geometry.002"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Switch"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Group Input"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Set Spline Cyclic"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Trim Curve"].parent = neck_1.nodes["Frame.005"]
    neck_1.nodes["Resample Curve.001"].parent = neck_1.nodes["Frame.005"]
    neck_1.nodes["Group.006"].parent = neck_1.nodes["Frame.005"]
    neck_1.nodes["Set Curve Normal"].parent = neck_1.nodes["Frame.005"]
    neck_1.nodes["Sample Nearest Surface"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Normal"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Vector Math"].parent = neck_1.nodes["Frame.005"]
    neck_1.nodes["Curve Tangent"].parent = neck_1.nodes["Frame.005"]
    neck_1.nodes["Frame.005"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Group.007"].parent = neck_1.nodes["Frame.001"]
    neck_1.nodes["Gem in Holder"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Curve to Points"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["For Each Geometry Element Input"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["For Each Geometry Element Output"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Position.002"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Transform Geometry.007"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Rotate Rotation"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Random Value"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Transform Geometry.008"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Random Value.001"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Store Named Attribute.001"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Random Value.002"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Rotate Rotation.001"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Random Value.003"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Random Value.004"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Random Value.005"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Random Value.006"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Frame.012"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Separate Geometry.001"].parent = neck_1.nodes["Frame.001"]
    neck_1.nodes["Separate XYZ.003"].parent = neck_1.nodes["Frame.001"]
    neck_1.nodes["Compare.002"].parent = neck_1.nodes["Frame.001"]
    neck_1.nodes["Trim Curve.001"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Set Curve Normal.001"].parent = neck_1.nodes["Frame.012"]
    neck_1.nodes["Compare.003"].parent = neck_1.nodes["Frame.001"]
    neck_1.nodes["Boolean Math"].parent = neck_1.nodes["Frame.001"]
    neck_1.nodes["Boolean Math.001"].parent = neck_1.nodes["Frame.001"]
    neck_1.nodes["Compare.004"].parent = neck_1.nodes["Frame.001"]
    neck_1.nodes["Frame.001"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Boolean Math.002"].parent = neck_1.nodes["Frame.001"]
    neck_1.nodes["Compare.005"].parent = neck_1.nodes["Frame.001"]
    neck_1.nodes["Gem in Holder.001"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Mesh to Curve.002"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Is Edge Boundary"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Set Spline Cyclic.001"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Trim Curve.004"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Curve to Points.001"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Set Curve Normal.002"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Position.004"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["For Each Geometry Element Input.001"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["For Each Geometry Element Output.001"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Transform Geometry.009"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Rotate Rotation.002"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Frame.014"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Random Value.007"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Random Value.008"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Distribute Points on Faces"].parent = neck_1.nodes["Frame.015"]
    neck_1.nodes["Instance on Points"].parent = neck_1.nodes["Frame.015"]
    neck_1.nodes["Ico Sphere"].parent = neck_1.nodes["Frame.015"]
    neck_1.nodes["Store Named Attribute.002"].parent = neck_1.nodes["Frame.015"]
    neck_1.nodes["Random Value.009"].parent = neck_1.nodes["Frame.015"]
    neck_1.nodes["Boolean Math.003"].parent = neck_1.nodes["Frame.015"]
    neck_1.nodes["Store Named Attribute.003"].parent = neck_1.nodes["Frame.015"]
    neck_1.nodes["Realize Instances.001"].parent = neck_1.nodes["Frame.015"]
    neck_1.nodes["Set Shade Smooth.003"].parent = neck_1.nodes["Frame.015"]
    neck_1.nodes["Frame.015"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Reroute.001"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Distribute Points on Faces.001"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Geometry Proximity"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Compare.006"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Gem in Holder.002"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Instance on Points.001"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Random Value.010"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Frame.016"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Realize Instances.002"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Transform Geometry.010"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Group.005"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Capture Attribute.001"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Index"].parent = neck_1.nodes["Frame.016"]
    neck_1.nodes["Set Position.001"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Geometry Proximity.001"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Curve to Mesh"].parent = neck_1.nodes["Frame.014"]
    neck_1.nodes["Separate Geometry.002"].parent = neck_1.nodes["Frame.013"]
    neck_1.nodes["Compare.007"].parent = neck_1.nodes["Frame.013"]
    neck_1.nodes["Separate XYZ.004"].parent = neck_1.nodes["Frame.013"]
    neck_1.nodes["Trim Curve.002"].parent = neck_1.nodes["Frame.013"]
    neck_1.nodes["Resample Curve.002"].parent = neck_1.nodes["Frame.013"]
    neck_1.nodes["Group.008"].parent = neck_1.nodes["Frame.013"]
    neck_1.nodes["Set Curve Normal.003"].parent = neck_1.nodes["Frame.013"]
    neck_1.nodes["Frame.013"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Transform Geometry"].parent = neck_1.nodes["Frame.013"]
    neck_1.nodes["Random Value.011"].parent = neck_1.nodes["Frame.015"]
    neck_1.nodes["Trim Curve.003"].parent = neck_1.nodes["Frame.017"]
    neck_1.nodes["Resample Curve.003"].parent = neck_1.nodes["Frame.017"]
    neck_1.nodes["Group.009"].parent = neck_1.nodes["Frame.017"]
    neck_1.nodes["Set Curve Normal.004"].parent = neck_1.nodes["Frame.017"]
    neck_1.nodes["Frame.017"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Transform Geometry.011"].parent = neck_1.nodes["Frame.017"]
    neck_1.nodes["Mesh to Curve"].parent = neck_1.nodes["Frame.017"]
    neck_1.nodes["Set Curve Tilt"].parent = neck_1.nodes["Frame.017"]
    neck_1.nodes["Reroute.002"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Curve Circle.002"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Transform Geometry.012"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Set Position.002"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Position.003"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Separate XYZ.005"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Map Range.001"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Float Curve"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Math.002"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Combine XYZ.001"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Position.005"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Vector Math.001"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Combine XYZ.002"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Float Curve.002"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Store Named Attribute"].parent = neck_1.nodes["Frame.024"]
    neck_1.nodes["Resample Curve"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Instance on Points.002"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Align Rotation to Vector"].parent = neck_1.nodes["Frame.003"]
    neck_1.nodes["Curve Tangent.001"].parent = neck_1.nodes["Frame.003"]
    neck_1.nodes["Align Rotation to Vector.001"].parent = neck_1.nodes["Frame.003"]
    neck_1.nodes["Normal.001"].parent = neck_1.nodes["Frame.003"]
    neck_1.nodes["Rotate Rotation.003"].parent = neck_1.nodes["Frame.003"]
    neck_1.nodes["Spline Parameter"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Math.003"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Math.004"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Set Curve Tilt.002"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Map Range.002"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Float Curve.003"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Spline Parameter.001"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Math.005"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Curve Circle.003"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Instance on Points.003"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Ico Sphere.001"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Cylinder.001"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Join Geometry.003"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Ico Sphere.002"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Transform Geometry.013"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Set Position.003"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Vector Math.002"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Noise Texture"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Transform Geometry.014"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Frame.002"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Rotate Rotation.004"].parent = neck_1.nodes["Frame.003"]
    neck_1.nodes["Ico Sphere.003"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Frame.003"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Store Named Attribute.004"].parent = neck_1.nodes["Frame.002"]
    neck_1.nodes["Cylinder.002"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Math.006"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Spline Parameter.002"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Float Curve.004"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Set Position.004"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Position.006"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Separate XYZ.006"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Math.007"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Combine XYZ.003"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Map Range.003"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Math.008"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Boolean Math.004"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Mesh to Curve.001"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Ico Sphere.004"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Instance on Points.004"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Transform Geometry.015"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Ico Sphere.005"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Dual Mesh"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Join Geometry.007"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Transform Geometry.016"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Transform Geometry.017"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Transform Geometry.018"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Transform Geometry.019"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Join Geometry.009"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Store Named Attribute.005"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Join Geometry.010"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Store Named Attribute.006"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Frame.004"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Sample Curve"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Transform Geometry.020"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Join Geometry.011"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Vector Math.003"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Float Curve.005"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Spline Parameter.003"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Math.009"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Math.010"].parent = neck_1.nodes["Frame.018"]
    neck_1.nodes["Frame.018"].parent = neck_1.nodes["Frame.024"]
    neck_1.nodes["Curve Circle.004"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Transform Geometry.021"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Set Position.005"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Position.007"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Separate XYZ.007"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Map Range.004"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Float Curve.006"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Math.011"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Combine XYZ.004"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Position.008"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Vector Math.004"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Combine XYZ.005"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Float Curve.007"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Resample Curve.004"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Instance on Points.005"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Align Rotation to Vector.002"].parent = neck_1.nodes["Frame.020"]
    neck_1.nodes["Curve Tangent.002"].parent = neck_1.nodes["Frame.020"]
    neck_1.nodes["Align Rotation to Vector.003"].parent = neck_1.nodes["Frame.020"]
    neck_1.nodes["Normal.002"].parent = neck_1.nodes["Frame.020"]
    neck_1.nodes["Spline Parameter.004"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Math.012"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Math.013"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Set Curve Tilt.003"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Map Range.005"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Float Curve.008"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Spline Parameter.005"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Math.014"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Frame.020"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Math.015"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Spline Parameter.006"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Float Curve.009"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Float Curve.010"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Spline Parameter.007"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Math.018"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Math.019"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Frame.022"].parent = neck_1.nodes["Frame.024"]
    neck_1.nodes["Quadrilateral"].parent = neck_1.nodes["Frame.019"]
    neck_1.nodes["Fillet Curve"].parent = neck_1.nodes["Frame.019"]
    neck_1.nodes["Set Spline Type"].parent = neck_1.nodes["Frame.019"]
    neck_1.nodes["Curve to Mesh.001"].parent = neck_1.nodes["Frame.019"]
    neck_1.nodes["Curve Circle.005"].parent = neck_1.nodes["Frame.019"]
    neck_1.nodes["Frame.019"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Rotate Rotation.006"].parent = neck_1.nodes["Frame.020"]
    neck_1.nodes["Rotate Rotation.005"].parent = neck_1.nodes["Frame.020"]
    neck_1.nodes["Random Value.012"].parent = neck_1.nodes["Frame.020"]
    neck_1.nodes["Index.001"].parent = neck_1.nodes["Frame.020"]
    neck_1.nodes["Math.016"].parent = neck_1.nodes["Frame.020"]
    neck_1.nodes["Switch.001"].parent = neck_1.nodes["Frame.020"]
    neck_1.nodes["Combine XYZ.006"].parent = neck_1.nodes["Frame.020"]
    neck_1.nodes["Join Geometry.012"].parent = neck_1.nodes["Frame.024"]
    neck_1.nodes["Curve Circle.006"].parent = neck_1.nodes["Frame.021"]
    neck_1.nodes["Curve to Mesh.002"].parent = neck_1.nodes["Frame.021"]
    neck_1.nodes["Sample Curve.001"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Transform Geometry.022"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Join Geometry.013"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Vector Math.005"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Curve Circle.007"].parent = neck_1.nodes["Frame.021"]
    neck_1.nodes["Curve Line"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Transform Geometry.023"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Frame.021"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Vector Math.006"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Curve to Mesh.003"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Resample Curve.005"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Curve Circle.008"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Spline Parameter.008"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Float Curve.011"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Curve Circle.009"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Curve to Mesh.004"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Curve Circle.010"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Join Geometry.014"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Curve Circle.011"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Instance on Points.006"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Transform Geometry.024"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Grid"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Delete Geometry.001"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Random Value.013"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Extrude Mesh"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Flip Faces"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Join Geometry.015"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Merge by Distance"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Transform Geometry.025"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Subdivision Surface"].parent = neck_1.nodes["Frame.023"]
    neck_1.nodes["Set Shade Smooth.001"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Frame.023"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Store Named Attribute.007"].parent = neck_1.nodes["Frame.022"]
    neck_1.nodes["Ico Sphere.006"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Transform Geometry.026"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Instance on Points.007"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Quadratic Bézier"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Realize Instances.003"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Mesh to SDF Grid"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Grid to Mesh"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Dual Mesh.001"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Triangulate"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["SDF Grid Boolean"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Cube"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Mesh to SDF Grid.001"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Transform Geometry.027"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Mesh Boolean"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Cube.001"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Transform Geometry.028"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Delete Geometry.002"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Mesh Boolean.001"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Cube.002"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Transform Geometry.029"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Join Geometry.016"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Delete Geometry.003"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Normal.003"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Compare.008"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Mesh to Curve.003"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Resample Curve.006"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Set Spline Cyclic.002"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Curve to Mesh.005"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Gem in Holder.003"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Trim Curve.005"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Instance on Points.008"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Resample Curve.007"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Align Rotation to Vector.004"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Curve Tangent.003"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Realize Instances.004"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Transform Geometry.030"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Flip Faces.002"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Join Geometry.018"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Merge by Distance.001"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Is Edge Boundary.001"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Spline Parameter.009"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Math.020"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Math.021"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Curve to Points.002"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Points to Curves"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Gradient Texture"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Math.022"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Math.023"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Delete Geometry.004"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Position.009"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Separate XYZ.008"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Compare.009"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Float Curve.012"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Transform Geometry.031"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Flip Faces.003"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Join Geometry.019"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Gem in Holder.004"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Join Geometry.020"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Gem in Holder.005"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Transform Geometry.032"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Join Geometry.021"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Flip Faces.001"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Gem in Holder.006"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Transform Geometry.033"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Join Geometry.022"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Flip Faces.004"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Transform Geometry.034"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Join Geometry.017"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Store Named Attribute.008"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Store Named Attribute.009"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Gem in Holder.007"].parent = neck_1.nodes["Frame.025"]
    neck_1.nodes["Instance on Points.009"].parent = neck_1.nodes["Frame.025"]
    neck_1.nodes["Curve Circle.012"].parent = neck_1.nodes["Frame.025"]
    neck_1.nodes["Transform Geometry.035"].parent = neck_1.nodes["Frame.025"]
    neck_1.nodes["Frame.025"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Transform Geometry.036"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Instance on Points.010"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Gem in Holder.008"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Realize Instances.005"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Capture Attribute.002"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Index.002"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Resample Curve.008"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Align Rotation to Vector.005"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Normal.004"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Align Rotation to Vector.006"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Curve Tangent.004"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Frame.027"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Trim Curve.006"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Gem in Holder.009"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Curve to Points.003"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["For Each Geometry Element Input.002"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["For Each Geometry Element Output.002"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Position.010"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Transform Geometry.037"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Rotate Rotation.007"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Random Value.014"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Transform Geometry.038"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Trim Curve.007"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Random Value.015"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Store Named Attribute.010"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Random Value.016"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Rotate Rotation.008"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Random Value.017"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Random Value.018"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Random Value.019"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Random Value.020"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Frame.028"].parent = neck_1.nodes["Frame.011"]
    neck_1.nodes["Store Named Attribute.011"].parent = neck_1.nodes["Frame.026"]
    neck_1.nodes["Store Named Attribute.012"].parent = neck_1.nodes["Frame.028"]
    neck_1.nodes["Mesh Boolean.002"].parent = neck_1.nodes["Frame.017"]
    neck_1.nodes["Ico Sphere.007"].parent = neck_1.nodes["Frame.017"]
    neck_1.nodes["Transform Geometry.039"].parent = neck_1.nodes["Frame.017"]
    neck_1.nodes["Store Named Attribute.013"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Boolean Math.005"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Named Attribute"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Store Named Attribute.014"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Math.017"].parent = neck_1.nodes["Frame.027"]
    neck_1.nodes["Transform Geometry.040"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Transform Geometry.041"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Scale Elements"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Transform Geometry.042"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Join Geometry.023"].parent = neck_1.nodes["Frame.004"]
    neck_1.nodes["Transform Geometry.043"].parent = neck_1.nodes["Frame.004"]

    # Set locations
    neck_1.nodes["Group Output"].location = (12680.001953125, 400.0)
    neck_1.nodes["Quadratic Bézier.003"].location = (29.0, -35.79998779296875)
    neck_1.nodes["Bi-Rail Loft.001"].location = (1387.0, -631.5999145507812)
    neck_1.nodes["Quadratic Bézier.004"].location = (189.0, -155.79998779296875)
    neck_1.nodes["Group.002"].location = (369.0, -95.79998779296875)
    neck_1.nodes["Join Geometry.005"].location = (369.0, -35.79998779296875)
    neck_1.nodes["Vector"].location = (29.0, -295.79998779296875)
    neck_1.nodes["Frame.006"].location = (29.0, -495.8000183105469)
    neck_1.nodes["Quadratic Bézier.006"].location = (29.0, -35.80000305175781)
    neck_1.nodes["Quadratic Bézier.007"].location = (189.0, -155.8000030517578)
    neck_1.nodes["Group.003"].location = (369.0, -95.80000305175781)
    neck_1.nodes["Join Geometry.006"].location = (369.0, -35.80000305175781)
    neck_1.nodes["Vector.001"].location = (29.0, -295.79998779296875)
    neck_1.nodes["Frame.007"].location = (29.0, -35.80000305175781)
    neck_1.nodes["Join Geometry.008"].location = (778.0, -391.6000061035156)
    neck_1.nodes["Transform Geometry.002"].location = (549.0, -35.79998779296875)
    neck_1.nodes["Transform Geometry.003"].location = (549.0, -355.79998779296875)
    neck_1.nodes["Curve Circle"].location = (189.0, -35.79998779296875)
    neck_1.nodes["Curve Circle.001"].location = (189.0, -355.79998779296875)
    neck_1.nodes["Set Position"].location = (829.0, -395.79998779296875)
    neck_1.nodes["Position"].location = (29.0, -715.7999877929688)
    neck_1.nodes["Separate XYZ"].location = (29.0, -775.7999877929688)
    neck_1.nodes["Map Range"].location = (189.0, -715.7999877929688)
    neck_1.nodes["Frame.008"].location = (29.0, -1119.9998779296875)
    neck_1.nodes["Float Curve.001"].location = (349.0, -715.7999877929688)
    neck_1.nodes["Combine XYZ"].location = (649.0, -715.7999877929688)
    neck_1.nodes["Transform Geometry.004"].location = (369.0, -355.79998779296875)
    neck_1.nodes["Transform Geometry.005"].location = (369.0, -35.79998779296875)
    neck_1.nodes["Closure Input.001"].location = (1167.0, -1051.599853515625)
    neck_1.nodes["Closure Output.001"].location = (1647.0, -1051.599853515625)
    neck_1.nodes["Math"].location = (1327.0, -1051.599853515625)
    neck_1.nodes["Math.001"].location = (1487.0, -1051.599853515625)
    neck_1.nodes["Transform Geometry.001"].location = (529.0, -75.80000305175781)
    neck_1.nodes["Transform Geometry.006"].location = (529.0, -95.79998779296875)
    neck_1.nodes["Integer"].location = (189.0, -215.79998779296875)
    neck_1.nodes["Frame.009"].location = (38.0, -35.7999267578125)
    neck_1.nodes["Frame.010"].location = (-1287.0, 951.5999145507812)
    neck_1.nodes["Delete Geometry"].location = (2840.0, -300.0)
    neck_1.nodes["Position.001"].location = (2680.0, -460.0)
    neck_1.nodes["Separate XYZ.001"].location = (2680.0, -520.0)
    neck_1.nodes["Compare"].location = (2840.0, -460.0)
    neck_1.nodes["Pipes"].location = (749.0, -95.80000305175781)
    neck_1.nodes["Join Geometry"].location = (2480.0, -320.0)
    neck_1.nodes["Separate XYZ.002"].location = (29.0, -35.80000305175781)
    neck_1.nodes["Compare.001"].location = (189.0, -35.80000305175781)
    neck_1.nodes["Separate Geometry"].location = (349.0, -35.80000305175781)
    neck_1.nodes["Join Geometry.001"].location = (549.0, -75.80000305175781)
    neck_1.nodes["Frame"].location = (1351.0, -24.19999885559082)
    neck_1.nodes["Rivet"].location = (1520.0, -520.0)
    neck_1.nodes["Realize Instances"].location = (1700.0, -520.0)
    neck_1.nodes["Set Shade Smooth"].location = (3080.0, -300.0)
    neck_1.nodes["Join Geometry.002"].location = (6677.9990234375, -3251.60009765625)
    neck_1.nodes["Switch"].location = (6837.9990234375, -3251.60009765625)
    neck_1.nodes["Group Input"].location = (6638.0, -3191.60009765625)
    neck_1.nodes["Set Spline Cyclic"].location = (458.0, -2031.60009765625)
    neck_1.nodes["Trim Curve"].location = (29.0, -29.0)
    neck_1.nodes["Resample Curve.001"].location = (189.0, -29.0)
    neck_1.nodes["Group.006"].location = (529.0, -29.0)
    neck_1.nodes["Set Curve Normal"].location = (349.0, -29.0)
    neck_1.nodes["Sample Nearest Surface"].location = (438.0, -2291.60009765625)
    neck_1.nodes["Normal"].location = (438.0, -2511.60009765625)
    neck_1.nodes["Vector Math"].location = (189.0, -189.0)
    neck_1.nodes["Curve Tangent"].location = (189.0, -329.0)
    neck_1.nodes["Frame.005"].location = (1309.0, -1702.60009765625)
    neck_1.nodes["Group.007"].location = (1129.0, -335.800048828125)
    neck_1.nodes["Frame.011"].location = (2422.0, 5711.60009765625)
    neck_1.nodes["Gem in Holder"].location = (1249.0, -155.800048828125)
    neck_1.nodes["Curve to Points"].location = (389.0, -415.800048828125)
    neck_1.nodes["For Each Geometry Element Input"].location = (549.0, -415.800048828125)
    neck_1.nodes["For Each Geometry Element Output"].location = (2069.0, -475.800048828125)
    neck_1.nodes["Position.002"].location = (389.0, -615.800048828125)
    neck_1.nodes["Transform Geometry.007"].location = (1529.0, -475.800048828125)
    neck_1.nodes["Rotate Rotation"].location = (1189.0, -675.800048828125)
    neck_1.nodes["Random Value"].location = (789.0, -395.800048828125)
    neck_1.nodes["Transform Geometry.008"].location = (1709.0, -475.800048828125)
    neck_1.nodes["Random Value.001"].location = (769.0, -615.800048828125)
    neck_1.nodes["Store Named Attribute.001"].location = (2329.0, -95.13330078125)
    neck_1.nodes["Random Value.002"].location = (789.0, -215.800048828125)
    neck_1.nodes["Rotate Rotation.001"].location = (1349.0, -675.800048828125)
    neck_1.nodes["Random Value.003"].location = (789.0, -35.800048828125)
    neck_1.nodes["Random Value.004"].location = (1029.0, -255.800048828125)
    neck_1.nodes["Random Value.005"].location = (1029.0, -75.800048828125)
    neck_1.nodes["Random Value.006"].location = (1029.0, -435.800048828125)
    neck_1.nodes["Frame.012"].location = (729.0, -2155.800048828125)
    neck_1.nodes["Separate Geometry.001"].location = (969.0, -335.800048828125)
    neck_1.nodes["Separate XYZ.003"].location = (29.0, -195.800048828125)
    neck_1.nodes["Compare.002"].location = (269.0, -35.800048828125)
    neck_1.nodes["Join Geometry.004"].location = (12340.001953125, 360.0)
    neck_1.nodes["Trim Curve.001"].location = (29.0, -415.800048828125)
    neck_1.nodes["Set Curve Normal.001"].location = (209.0, -395.800048828125)
    neck_1.nodes["Compare.003"].location = (269.0, -195.800048828125)
    neck_1.nodes["Boolean Math"].location = (429.0, -55.800048828125)
    neck_1.nodes["Boolean Math.001"].location = (609.0, -215.800048828125)
    neck_1.nodes["Compare.004"].location = (269.0, -355.800048828125)
    neck_1.nodes["Frame.001"].location = (29.0, -3255.800048828125)
    neck_1.nodes["Boolean Math.002"].location = (789.0, -255.800048828125)
    neck_1.nodes["Compare.005"].location = (269.0, -535.800048828125)
    neck_1.nodes["Gem in Holder.001"].location = (1349.0, -75.13330078125)
    neck_1.nodes["Mesh to Curve.002"].location = (29.0, -55.13330078125)
    neck_1.nodes["Is Edge Boundary"].location = (29.0, -175.13330078125)
    neck_1.nodes["Set Spline Cyclic.001"].location = (349.0, -55.13330078125)
    neck_1.nodes["Trim Curve.004"].location = (509.0, -55.13330078125)
    neck_1.nodes["Curve to Points.001"].location = (669.0, -55.13330078125)
    neck_1.nodes["Set Curve Normal.002"].location = (189.0, -55.13330078125)
    neck_1.nodes["Position.004"].location = (669.0, -255.13330078125)
    neck_1.nodes["For Each Geometry Element Input.001"].location = (829.0, -55.13330078125)
    neck_1.nodes["For Each Geometry Element Output.001"].location = (2509.0, -75.13330078125)
    neck_1.nodes["Transform Geometry.009"].location = (1609.0, -75.13330078125)
    neck_1.nodes["Rotate Rotation.002"].location = (1009.0, -295.13330078125)
    neck_1.nodes["Frame.014"].location = (1449.0, -3056.466796875)
    neck_1.nodes["Random Value.007"].location = (1169.0, -55.13330078125)
    neck_1.nodes["Random Value.008"].location = (1169.0, -235.13330078125)
    neck_1.nodes["Distribute Points on Faces"].location = (209.0, -35.7999267578125)
    neck_1.nodes["Instance on Points"].location = (509.0, -55.7999267578125)
    neck_1.nodes["Ico Sphere"].location = (29.0, -255.7999267578125)
    neck_1.nodes["Store Named Attribute.002"].location = (689.0, -55.7999267578125)
    neck_1.nodes["Random Value.009"].location = (689.0, -215.7999267578125)
    neck_1.nodes["Boolean Math.003"].location = (869.0, -215.7999267578125)
    neck_1.nodes["Store Named Attribute.003"].location = (869.0, -55.7999267578125)
    neck_1.nodes["Realize Instances.001"].location = (1029.0, -55.7999267578125)
    neck_1.nodes["Set Shade Smooth.003"].location = (209.0, -255.7999267578125)
    neck_1.nodes["Frame.015"].location = (2169.0, -3975.80029296875)
    neck_1.nodes["Reroute.001"].location = (209.0, -75.7999267578125)
    neck_1.nodes["Distribute Points on Faces.001"].location = (409.0, -35.7999267578125)
    neck_1.nodes["Geometry Proximity"].location = (29.0, -195.7999267578125)
    neck_1.nodes["Compare.006"].location = (249.0, -195.7999267578125)
    neck_1.nodes["Gem in Holder.002"].location = (29.0, -415.7999267578125)
    neck_1.nodes["Instance on Points.001"].location = (669.0, -75.7999267578125)
    neck_1.nodes["Random Value.010"].location = (669.0, -315.7999267578125)
    neck_1.nodes["Frame.016"].location = (4649.0, -3755.80029296875)
    neck_1.nodes["Realize Instances.002"].location = (1009.0, -75.7999267578125)
    neck_1.nodes["Transform Geometry.010"].location = (269.0, -415.7999267578125)
    neck_1.nodes["Group.005"].location = (1169.0, -75.7999267578125)
    neck_1.nodes["Capture Attribute.001"].location = (849.0, -75.7999267578125)
    neck_1.nodes["Index"].location = (849.0, -195.7999267578125)
    neck_1.nodes["Set Position.001"].location = (1889.0, -75.13330078125)
    neck_1.nodes["Geometry Proximity.001"].location = (1709.0, -275.13330078125)
    neck_1.nodes["Curve to Mesh"].location = (2149.0, -95.13330078125)
    neck_1.nodes["Separate Geometry.002"].location = (29.0, -29.0)
    neck_1.nodes["Compare.007"].location = (29.0, -169.0)
    neck_1.nodes["Separate XYZ.004"].location = (29.0, -329.0)
    neck_1.nodes["Trim Curve.002"].location = (189.0, -29.0)
    neck_1.nodes["Resample Curve.002"].location = (349.0, -29.0)
    neck_1.nodes["Group.008"].location = (869.0, -29.0)
    neck_1.nodes["Set Curve Normal.003"].location = (509.0, -29.0)
    neck_1.nodes["Frame.013"].location = (1149.0, -1242.60009765625)
    neck_1.nodes["Transform Geometry"].location = (689.0, -49.0)
    neck_1.nodes["Random Value.011"].location = (509.0, -335.7999267578125)
    neck_1.nodes["Trim Curve.003"].location = (189.0, -29.0)
    neck_1.nodes["Resample Curve.003"].location = (349.0, -29.0)
    neck_1.nodes["Group.009"].location = (1029.0, -29.0)
    neck_1.nodes["Set Curve Normal.004"].location = (509.0, -29.0)
    neck_1.nodes["Frame.017"].location = (1149.0, -622.60009765625)
    neck_1.nodes["Transform Geometry.011"].location = (869.0, -29.0)
    neck_1.nodes["Mesh to Curve"].location = (29.0, -29.0)
    neck_1.nodes["Set Curve Tilt"].location = (689.0, -29.0)
    neck_1.nodes["Reroute.002"].location = (4178.0, -3711.60009765625)
    neck_1.nodes["Curve Circle.002"].location = (1229.0, -35.7998046875)
    neck_1.nodes["Transform Geometry.012"].location = (1949.0, -395.7998046875)
    neck_1.nodes["Set Position.002"].location = (1789.0, -395.7998046875)
    neck_1.nodes["Position.003"].location = (629.0, -635.7998046875)
    neck_1.nodes["Separate XYZ.005"].location = (629.0, -695.7998046875)
    neck_1.nodes["Map Range.001"].location = (789.0, -635.7998046875)
    neck_1.nodes["Float Curve"].location = (969.0, -635.7998046875)
    neck_1.nodes["Math.002"].location = (1429.0, -675.7998046875)
    neck_1.nodes["Combine XYZ.001"].location = (1589.0, -675.7998046875)
    neck_1.nodes["Position.005"].location = (1069.0, -155.7998046875)
    neck_1.nodes["Vector Math.001"].location = (1229.0, -155.7998046875)
    neck_1.nodes["Combine XYZ.002"].location = (1229.0, -295.7998046875)
    neck_1.nodes["Float Curve.002"].location = (969.0, -295.7998046875)
    neck_1.nodes["Store Named Attribute"].location = (5618.0, -2771.5986328125)
    neck_1.nodes["Resample Curve"].location = (2129.0, -395.7998046875)
    neck_1.nodes["Instance on Points.002"].location = (3469.0, -535.7998046875)
    neck_1.nodes["Align Rotation to Vector"].location = (29.0, -35.7998046875)
    neck_1.nodes["Curve Tangent.001"].location = (29.0, -195.7998046875)
    neck_1.nodes["Align Rotation to Vector.001"].location = (189.0, -35.7998046875)
    neck_1.nodes["Normal.001"].location = (189.0, -195.7998046875)
    neck_1.nodes["Rotate Rotation.003"].location = (349.0, -35.7998046875)
    neck_1.nodes["Spline Parameter"].location = (1669.0, -55.7998046875)
    neck_1.nodes["Math.003"].location = (1849.0, -55.7998046875)
    neck_1.nodes["Math.004"].location = (2029.0, -55.7998046875)
    neck_1.nodes["Set Curve Tilt.002"].location = (2589.0, -395.7998046875)
    neck_1.nodes["Map Range.002"].location = (2229.0, -75.7998046875)
    neck_1.nodes["Float Curve.003"].location = (269.0, -1115.7998046875)
    neck_1.nodes["Spline Parameter.001"].location = (29.0, -1355.7998046875)
    neck_1.nodes["Math.005"].location = (609.0, -1095.7998046875)
    neck_1.nodes["Curve Circle.003"].location = (29.0, -99.6669921875)
    neck_1.nodes["Instance on Points.003"].location = (189.0, -99.6669921875)
    neck_1.nodes["Ico Sphere.001"].location = (29.0, -239.6669921875)
    neck_1.nodes["Cylinder.001"].location = (189.0, -39.6669921875)
    neck_1.nodes["Join Geometry.003"].location = (1169.0, -39.6669921875)
    neck_1.nodes["Ico Sphere.002"].location = (349.0, -99.6669921875)
    neck_1.nodes["Transform Geometry.013"].location = (749.0, -119.6669921875)
    neck_1.nodes["Set Position.003"].location = (569.0, -139.6669921875)
    neck_1.nodes["Vector Math.002"].location = (569.0, -279.6669921875)
    neck_1.nodes["Noise Texture"].location = (369.0, -279.6669921875)
    neck_1.nodes["Transform Geometry.014"].location = (909.0, -179.6669921875)
    neck_1.nodes["Frame.002"].location = (1700.0, -1016.1328125)
    neck_1.nodes["Rotate Rotation.004"].location = (509.0, -35.7998046875)
    neck_1.nodes["Ico Sphere.003"].location = (29.0, -399.6669921875)
    neck_1.nodes["Frame.003"].location = (2220.0, -680.0)
    neck_1.nodes["Store Named Attribute.004"].location = (1369.0, -39.6669921875)
    neck_1.nodes["Cylinder.002"].location = (29.0, -115.7998046875)
    neck_1.nodes["Math.006"].location = (1249.0, -655.7998046875)
    neck_1.nodes["Spline Parameter.002"].location = (29.0, -935.7998046875)
    neck_1.nodes["Float Curve.004"].location = (269.0, -795.7998046875)
    neck_1.nodes["Set Position.004"].location = (869.0, -155.7998046875)
    neck_1.nodes["Position.006"].location = (229.0, -215.7998046875)
    neck_1.nodes["Separate XYZ.006"].location = (229.0, -275.7998046875)
    neck_1.nodes["Math.007"].location = (389.0, -215.7998046875)
    neck_1.nodes["Combine XYZ.003"].location = (709.0, -215.7998046875)
    neck_1.nodes["Map Range.003"].location = (389.0, -355.7998046875)
    neck_1.nodes["Math.008"].location = (549.0, -215.7998046875)
    neck_1.nodes["Boolean Math.004"].location = (969.0, -495.7998046875)
    neck_1.nodes["Mesh to Curve.001"].location = (1189.0, -375.7998046875)
    neck_1.nodes["Ico Sphere.004"].location = (1189.0, -515.7998046875)
    neck_1.nodes["Instance on Points.004"].location = (1369.0, -375.7998046875)
    neck_1.nodes["Transform Geometry.015"].location = (1909.0, -495.7998046875)
    neck_1.nodes["Ico Sphere.005"].location = (1569.0, -495.7998046875)
    neck_1.nodes["Dual Mesh"].location = (1749.0, -495.7998046875)
    neck_1.nodes["Join Geometry.007"].location = (2269.0, -315.7998046875)
    neck_1.nodes["Transform Geometry.016"].location = (2109.0, -355.7998046875)
    neck_1.nodes["Transform Geometry.017"].location = (2109.0, -675.7998046875)
    neck_1.nodes["Transform Geometry.018"].location = (2269.0, -675.7998046875)
    neck_1.nodes["Transform Geometry.019"].location = (2269.0, -355.7998046875)
    neck_1.nodes["Join Geometry.009"].location = (1809.0, -95.7998046875)
    neck_1.nodes["Store Named Attribute.005"].location = (2889.0, -255.7998046875)
    neck_1.nodes["Join Geometry.010"].location = (3109.0, -155.7998046875)
    neck_1.nodes["Store Named Attribute.006"].location = (2889.0, -55.7998046875)
    neck_1.nodes["Frame.004"].location = (640.0, -1760.0)
    neck_1.nodes["Sample Curve"].location = (3509.0, -1515.7998046875)
    neck_1.nodes["Transform Geometry.020"].location = (3949.0, -1515.7998046875)
    neck_1.nodes["Join Geometry.011"].location = (4229.0, -1015.7998046875)
    neck_1.nodes["Vector Math.003"].location = (3669.0, -1515.7998046875)
    neck_1.nodes["Float Curve.005"].location = (229.0, -1455.7998046875)
    neck_1.nodes["Spline Parameter.003"].location = (29.0, -1695.7998046875)
    neck_1.nodes["Math.009"].location = (609.0, -1435.7998046875)
    neck_1.nodes["Math.010"].location = (789.0, -1075.7998046875)
    neck_1.nodes["Frame.018"].location = (49.0, -35.798828125)
    neck_1.nodes["Curve Circle.004"].location = (1229.0, -35.7998046875)
    neck_1.nodes["Transform Geometry.021"].location = (1949.0, -395.7998046875)
    neck_1.nodes["Set Position.005"].location = (1789.0, -395.7998046875)
    neck_1.nodes["Position.007"].location = (629.0, -635.7998046875)
    neck_1.nodes["Separate XYZ.007"].location = (629.0, -695.7998046875)
    neck_1.nodes["Map Range.004"].location = (789.0, -635.7998046875)
    neck_1.nodes["Float Curve.006"].location = (969.0, -635.7998046875)
    neck_1.nodes["Math.011"].location = (1409.0, -655.7998046875)
    neck_1.nodes["Combine XYZ.004"].location = (1589.0, -675.7998046875)
    neck_1.nodes["Position.008"].location = (1069.0, -155.7998046875)
    neck_1.nodes["Vector Math.004"].location = (1229.0, -155.7998046875)
    neck_1.nodes["Combine XYZ.005"].location = (1229.0, -295.7998046875)
    neck_1.nodes["Float Curve.007"].location = (969.0, -295.7998046875)
    neck_1.nodes["Resample Curve.004"].location = (2129.0, -395.7998046875)
    neck_1.nodes["Instance on Points.005"].location = (3229.0, -555.7998046875)
    neck_1.nodes["Align Rotation to Vector.002"].location = (29.0, -35.7998046875)
    neck_1.nodes["Curve Tangent.002"].location = (29.0, -195.7998046875)
    neck_1.nodes["Align Rotation to Vector.003"].location = (189.0, -35.7998046875)
    neck_1.nodes["Normal.002"].location = (189.0, -195.7998046875)
    neck_1.nodes["Spline Parameter.004"].location = (1669.0, -55.7998046875)
    neck_1.nodes["Math.012"].location = (1849.0, -55.7998046875)
    neck_1.nodes["Math.013"].location = (2029.0, -55.7998046875)
    neck_1.nodes["Set Curve Tilt.003"].location = (2589.0, -395.7998046875)
    neck_1.nodes["Map Range.005"].location = (2229.0, -75.7998046875)
    neck_1.nodes["Float Curve.008"].location = (269.0, -1115.7998046875)
    neck_1.nodes["Spline Parameter.005"].location = (29.0, -1355.7998046875)
    neck_1.nodes["Math.014"].location = (609.0, -1095.7998046875)
    neck_1.nodes["Frame.020"].location = (2260.0, -520.0)
    neck_1.nodes["Math.015"].location = (1249.0, -655.7998046875)
    neck_1.nodes["Spline Parameter.006"].location = (29.0, -935.7998046875)
    neck_1.nodes["Float Curve.009"].location = (269.0, -795.7998046875)
    neck_1.nodes["Float Curve.010"].location = (229.0, -1455.7998046875)
    neck_1.nodes["Spline Parameter.007"].location = (29.0, -1695.7998046875)
    neck_1.nodes["Math.018"].location = (609.0, -1435.7998046875)
    neck_1.nodes["Math.019"].location = (789.0, -1075.7998046875)
    neck_1.nodes["Frame.022"].location = (29.0, -3035.798828125)
    neck_1.nodes["Quadrilateral"].location = (29.0, -35.7998046875)
    neck_1.nodes["Fillet Curve"].location = (349.0, -35.7998046875)
    neck_1.nodes["Set Spline Type"].location = (189.0, -35.7998046875)
    neck_1.nodes["Curve to Mesh.001"].location = (509.0, -35.7998046875)
    neck_1.nodes["Curve Circle.005"].location = (349.0, -155.7998046875)
    neck_1.nodes["Frame.019"].location = (2260.0, -980.0)
    neck_1.nodes["Rotate Rotation.006"].location = (509.0, -35.7998046875)
    neck_1.nodes["Rotate Rotation.005"].location = (349.0, -35.7998046875)
    neck_1.nodes["Random Value.012"].location = (509.0, -135.7998046875)
    neck_1.nodes["Index.001"].location = (189.0, -275.7998046875)
    neck_1.nodes["Math.016"].location = (189.0, -335.7998046875)
    neck_1.nodes["Switch.001"].location = (349.0, -235.7998046875)
    neck_1.nodes["Combine XYZ.006"].location = (349.0, -155.7998046875)
    neck_1.nodes["Join Geometry.012"].location = (5258.0, -2831.5986328125)
    neck_1.nodes["Curve Circle.006"].location = (29.0, -35.7998046875)
    neck_1.nodes["Curve to Mesh.002"].location = (289.0, -35.7998046875)
    neck_1.nodes["Sample Curve.001"].location = (3089.0, -1175.7998046875)
    neck_1.nodes["Transform Geometry.022"].location = (3449.0, -1215.7998046875)
    neck_1.nodes["Join Geometry.013"].location = (4109.0, -895.7998046875)
    neck_1.nodes["Vector Math.005"].location = (3269.0, -1255.7998046875)
    neck_1.nodes["Curve Circle.007"].location = (29.0, -155.7998046875)
    neck_1.nodes["Curve Line"].location = (29.0, -555.7998046875)
    neck_1.nodes["Transform Geometry.023"].location = (4009.0, -1575.7998046875)
    neck_1.nodes["Frame.021"].location = (2420.0, -1400.0)
    neck_1.nodes["Vector Math.006"].location = (3269.0, -1475.7998046875)
    neck_1.nodes["Curve to Mesh.003"].location = (529.0, -535.7998046875)
    neck_1.nodes["Resample Curve.005"].location = (209.0, -555.7998046875)
    neck_1.nodes["Curve Circle.008"].location = (529.0, -675.7998046875)
    neck_1.nodes["Spline Parameter.008"].location = (29.0, -835.7998046875)
    neck_1.nodes["Float Curve.011"].location = (209.0, -675.7998046875)
    neck_1.nodes["Curve Circle.009"].location = (649.0, -35.7998046875)
    neck_1.nodes["Curve to Mesh.004"].location = (829.0, -75.7998046875)
    neck_1.nodes["Curve Circle.010"].location = (649.0, -175.7998046875)
    neck_1.nodes["Join Geometry.014"].location = (2129.0, -255.7998046875)
    neck_1.nodes["Curve Circle.011"].location = (649.0, -315.7998046875)
    neck_1.nodes["Instance on Points.006"].location = (1009.0, -95.7998046875)
    neck_1.nodes["Transform Geometry.024"].location = (1189.0, -95.7998046875)
    neck_1.nodes["Grid"].location = (709.0, -635.7998046875)
    neck_1.nodes["Delete Geometry.001"].location = (889.0, -635.7998046875)
    neck_1.nodes["Random Value.013"].location = (889.0, -755.7998046875)
    neck_1.nodes["Extrude Mesh"].location = (1069.0, -635.7998046875)
    neck_1.nodes["Flip Faces"].location = (1069.0, -555.7998046875)
    neck_1.nodes["Join Geometry.015"].location = (1229.0, -635.7998046875)
    neck_1.nodes["Merge by Distance"].location = (1409.0, -635.7998046875)
    neck_1.nodes["Transform Geometry.025"].location = (1769.0, -575.7998046875)
    neck_1.nodes["Subdivision Surface"].location = (1589.0, -635.7998046875)
    neck_1.nodes["Set Shade Smooth.001"].location = (4309.0, -915.7998046875)
    neck_1.nodes["Frame.023"].location = (1520.0, -1820.0)
    neck_1.nodes["Store Named Attribute.007"].location = (4469.0, -895.7998046875)
    neck_1.nodes["Frame.024"].location = (1062.0, 14831.5986328125)
    neck_1.nodes["Ico Sphere.006"].location = (29.0, -1295.80029296875)
    neck_1.nodes["Transform Geometry.026"].location = (209.0, -1295.80029296875)
    neck_1.nodes["Instance on Points.007"].location = (389.0, -1195.80029296875)
    neck_1.nodes["Quadratic Bézier"].location = (29.0, -975.80029296875)
    neck_1.nodes["Realize Instances.003"].location = (569.0, -1195.80029296875)
    neck_1.nodes["Mesh to SDF Grid"].location = (729.0, -1195.80029296875)
    neck_1.nodes["Grid to Mesh"].location = (1089.0, -1195.80029296875)
    neck_1.nodes["Dual Mesh.001"].location = (1409.0, -1195.80029296875)
    neck_1.nodes["Triangulate"].location = (1249.0, -1195.80029296875)
    neck_1.nodes["SDF Grid Boolean"].location = (909.0, -1195.80029296875)
    neck_1.nodes["Cube"].location = (409.0, -1535.80029296875)
    neck_1.nodes["Mesh to SDF Grid.001"].location = (769.0, -1355.80029296875)
    neck_1.nodes["Transform Geometry.027"].location = (569.0, -1515.80029296875)
    neck_1.nodes["Mesh Boolean"].location = (1589.0, -1195.80029296875)
    neck_1.nodes["Cube.001"].location = (1249.0, -1335.80029296875)
    neck_1.nodes["Transform Geometry.028"].location = (1409.0, -1335.80029296875)
    neck_1.nodes["Delete Geometry.002"].location = (1769.0, -1195.80029296875)
    neck_1.nodes["Mesh Boolean.001"].location = (1449.0, -195.80029296875)
    neck_1.nodes["Cube.002"].location = (1089.0, -55.80029296875)
    neck_1.nodes["Transform Geometry.029"].location = (1249.0, -55.80029296875)
    neck_1.nodes["Join Geometry.016"].location = (5609.0, -795.80029296875)
    neck_1.nodes["Delete Geometry.003"].location = (1969.0, -175.80029296875)
    neck_1.nodes["Normal.003"].location = (1629.0, -275.80029296875)
    neck_1.nodes["Compare.008"].location = (1789.0, -275.80029296875)
    neck_1.nodes["Mesh to Curve.003"].location = (2129.0, -175.80029296875)
    neck_1.nodes["Resample Curve.006"].location = (3809.0, -35.80029296875)
    neck_1.nodes["Set Spline Cyclic.002"].location = (3649.0, -35.80029296875)
    neck_1.nodes["Curve to Mesh.005"].location = (3969.0, -35.80029296875)
    neck_1.nodes["Gem in Holder.003"].location = (3809.0, -155.80029296875)
    neck_1.nodes["Trim Curve.005"].location = (2289.0, -175.80029296875)
    neck_1.nodes["Instance on Points.008"].location = (4689.0, -655.80029296875)
    neck_1.nodes["Resample Curve.007"].location = (4529.0, -655.80029296875)
    neck_1.nodes["Align Rotation to Vector.004"].location = (4529.0, -775.80029296875)
    neck_1.nodes["Curve Tangent.003"].location = (4529.0, -935.80029296875)
    neck_1.nodes["Realize Instances.004"].location = (5029.0, -815.80029296875)
    neck_1.nodes["Transform Geometry.030"].location = (1949.0, -1295.80029296875)
    neck_1.nodes["Flip Faces.002"].location = (2109.0, -1295.80029296875)
    neck_1.nodes["Join Geometry.018"].location = (2269.0, -1235.80029296875)
    neck_1.nodes["Merge by Distance.001"].location = (2449.0, -1235.80029296875)
    neck_1.nodes["Is Edge Boundary.001"].location = (2269.0, -1315.80029296875)
    neck_1.nodes["Spline Parameter.009"].location = (3809.0, -1035.80029296875)
    neck_1.nodes["Math.020"].location = (3969.0, -1035.80029296875)
    neck_1.nodes["Math.021"].location = (4129.0, -1035.80029296875)
    neck_1.nodes["Curve to Points.002"].location = (2449.0, -175.80029296875)
    neck_1.nodes["Points to Curves"].location = (2609.0, -175.80029296875)
    neck_1.nodes["Gradient Texture"].location = (2129.0, -355.80029296875)
    neck_1.nodes["Math.022"].location = (2289.0, -355.80029296875)
    neck_1.nodes["Math.023"].location = (2449.0, -355.80029296875)
    neck_1.nodes["Delete Geometry.004"].location = (3149.0, -335.80029296875)
    neck_1.nodes["Position.009"].location = (2689.0, -415.80029296875)
    neck_1.nodes["Separate XYZ.008"].location = (2689.0, -475.80029296875)
    neck_1.nodes["Compare.009"].location = (2849.0, -415.80029296875)
    neck_1.nodes["Float Curve.012"].location = (4289.0, -1035.80029296875)
    neck_1.nodes["Transform Geometry.031"].location = (4869.0, -935.80029296875)
    neck_1.nodes["Flip Faces.003"].location = (5029.0, -935.80029296875)
    neck_1.nodes["Join Geometry.019"].location = (5229.0, -875.80029296875)
    neck_1.nodes["Gem in Holder.004"].location = (3149.0, -495.80029296875)
    neck_1.nodes["Join Geometry.020"].location = (4329.0, -735.80029296875)
    neck_1.nodes["Gem in Holder.005"].location = (3149.0, -595.80029296875)
    neck_1.nodes["Transform Geometry.032"].location = (3309.0, -675.80029296875)
    neck_1.nodes["Join Geometry.021"].location = (3309.0, -595.80029296875)
    neck_1.nodes["Flip Faces.001"].location = (3309.0, -635.80029296875)
    neck_1.nodes["Gem in Holder.006"].location = (3009.0, -775.80029296875)
    neck_1.nodes["Transform Geometry.033"].location = (3169.0, -855.80029296875)
    neck_1.nodes["Join Geometry.022"].location = (3329.0, -795.80029296875)
    neck_1.nodes["Flip Faces.004"].location = (3329.0, -855.80029296875)
    neck_1.nodes["Transform Geometry.034"].location = (3489.0, -795.80029296875)
    neck_1.nodes["Join Geometry.017"].location = (6009.0, -935.80029296875)
    neck_1.nodes["Store Named Attribute.008"].location = (5789.0, -795.80029296875)
    neck_1.nodes["Store Named Attribute.009"].location = (5789.0, -975.80029296875)
    neck_1.nodes["Gem in Holder.007"].location = (389.0, -215.80029296875)
    neck_1.nodes["Instance on Points.009"].location = (569.0, -155.80029296875)
    neck_1.nodes["Curve Circle.012"].location = (29.0, -35.80029296875)
    neck_1.nodes["Transform Geometry.035"].location = (209.0, -35.80029296875)
    neck_1.nodes["Frame.025"].location = (5180.0, -1240.0)
    neck_1.nodes["Frame.026"].location = (991.0, 8155.80029296875)
    neck_1.nodes["Transform Geometry.036"].location = (6189.0, -875.80029296875)
    neck_1.nodes["Instance on Points.010"].location = (749.0, -175.80029296875)
    neck_1.nodes["Gem in Holder.008"].location = (189.0, -175.80029296875)
    neck_1.nodes["Realize Instances.005"].location = (1109.0, -115.80029296875)
    neck_1.nodes["Capture Attribute.002"].location = (929.0, -175.80029296875)
    neck_1.nodes["Index.002"].location = (929.0, -295.80029296875)
    neck_1.nodes["Resample Curve.008"].location = (189.0, -35.80029296875)
    neck_1.nodes["Align Rotation to Vector.005"].location = (369.0, -315.80029296875)
    neck_1.nodes["Normal.004"].location = (529.0, -475.80029296875)
    neck_1.nodes["Align Rotation to Vector.006"].location = (529.0, -315.80029296875)
    neck_1.nodes["Curve Tangent.004"].location = (369.0, -475.80029296875)
    neck_1.nodes["Frame.027"].location = (2489.0, -35.7998046875)
    neck_1.nodes["Trim Curve.006"].location = (29.0, -35.80029296875)
    neck_1.nodes["Gem in Holder.009"].location = (1109.0, -155.80029296875)
    neck_1.nodes["Curve to Points.003"].location = (189.0, -475.80029296875)
    neck_1.nodes["For Each Geometry Element Input.002"].location = (409.0, -415.80029296875)
    neck_1.nodes["For Each Geometry Element Output.002"].location = (2029.0, -455.80029296875)
    neck_1.nodes["Position.010"].location = (189.0, -675.80029296875)
    neck_1.nodes["Transform Geometry.037"].location = (1389.0, -475.80029296875)
    neck_1.nodes["Rotate Rotation.007"].location = (1049.0, -675.80029296875)
    neck_1.nodes["Random Value.014"].location = (649.0, -395.80029296875)
    neck_1.nodes["Transform Geometry.038"].location = (1569.0, -475.80029296875)
    neck_1.nodes["Trim Curve.007"].location = (29.0, -475.80029296875)
    neck_1.nodes["Random Value.015"].location = (629.0, -615.80029296875)
    neck_1.nodes["Store Named Attribute.010"].location = (1809.0, -495.80029296875)
    neck_1.nodes["Random Value.016"].location = (649.0, -215.80029296875)
    neck_1.nodes["Rotate Rotation.008"].location = (1209.0, -675.80029296875)
    neck_1.nodes["Random Value.017"].location = (649.0, -35.80029296875)
    neck_1.nodes["Random Value.018"].location = (889.0, -255.80029296875)
    neck_1.nodes["Random Value.019"].location = (889.0, -75.80029296875)
    neck_1.nodes["Random Value.020"].location = (889.0, -435.80029296875)
    neck_1.nodes["Frame.028"].location = (3029.0, -915.7998046875)
    neck_1.nodes["Store Named Attribute.011"].location = (6369.0, -875.80029296875)
    neck_1.nodes["Store Named Attribute.012"].location = (2189.0, -455.80029296875)
    neck_1.nodes["Mesh Boolean.002"].location = (1329.0, -49.0)
    neck_1.nodes["Ico Sphere.007"].location = (1029.0, -209.0)
    neck_1.nodes["Transform Geometry.039"].location = (1189.0, -209.0)
    neck_1.nodes["Store Named Attribute.013"].location = (1449.0, -135.80029296875)
    neck_1.nodes["Boolean Math.005"].location = (1289.0, -255.80029296875)
    neck_1.nodes["Named Attribute"].location = (1109.0, -415.80029296875)
    neck_1.nodes["Store Named Attribute.014"].location = (1609.0, -135.80029296875)
    neck_1.nodes["Math.017"].location = (1109.0, -255.80029296875)
    neck_1.nodes["Transform Geometry.040"].location = (1209.0, -35.7998046875)
    neck_1.nodes["Transform Geometry.041"].location = (1409.0, -35.7998046875)
    neck_1.nodes["Scale Elements"].location = (2509.0, -155.7998046875)
    neck_1.nodes["Transform Geometry.042"].location = (2669.0, -155.7998046875)
    neck_1.nodes["Join Geometry.023"].location = (2669.0, -115.7998046875)
    neck_1.nodes["Transform Geometry.043"].location = (2669.0, -495.7998046875)

    # Set dimensions
    neck_1.nodes["Group Output"].width  = 140.0
    neck_1.nodes["Group Output"].height = 100.0

    neck_1.nodes["Quadratic Bézier.003"].width  = 140.0
    neck_1.nodes["Quadratic Bézier.003"].height = 100.0

    neck_1.nodes["Bi-Rail Loft.001"].width  = 280.0
    neck_1.nodes["Bi-Rail Loft.001"].height = 100.0

    neck_1.nodes["Quadratic Bézier.004"].width  = 140.0
    neck_1.nodes["Quadratic Bézier.004"].height = 100.0

    neck_1.nodes["Group.002"].width  = 140.0
    neck_1.nodes["Group.002"].height = 100.0

    neck_1.nodes["Join Geometry.005"].width  = 140.0
    neck_1.nodes["Join Geometry.005"].height = 100.0

    neck_1.nodes["Vector"].width  = 140.0
    neck_1.nodes["Vector"].height = 100.0

    neck_1.nodes["Frame.006"].width  = 698.0
    neck_1.nodes["Frame.006"].height = 438.79998779296875

    neck_1.nodes["Quadratic Bézier.006"].width  = 140.0
    neck_1.nodes["Quadratic Bézier.006"].height = 100.0

    neck_1.nodes["Quadratic Bézier.007"].width  = 140.0
    neck_1.nodes["Quadratic Bézier.007"].height = 100.0

    neck_1.nodes["Group.003"].width  = 140.0
    neck_1.nodes["Group.003"].height = 100.0

    neck_1.nodes["Join Geometry.006"].width  = 140.0
    neck_1.nodes["Join Geometry.006"].height = 100.0

    neck_1.nodes["Vector.001"].width  = 140.0
    neck_1.nodes["Vector.001"].height = 100.0

    neck_1.nodes["Frame.007"].width  = 698.0
    neck_1.nodes["Frame.007"].height = 438.79998779296875

    neck_1.nodes["Join Geometry.008"].width  = 140.0
    neck_1.nodes["Join Geometry.008"].height = 100.0

    neck_1.nodes["Transform Geometry.002"].width  = 140.0
    neck_1.nodes["Transform Geometry.002"].height = 100.0

    neck_1.nodes["Transform Geometry.003"].width  = 140.0
    neck_1.nodes["Transform Geometry.003"].height = 100.0

    neck_1.nodes["Curve Circle"].width  = 140.0
    neck_1.nodes["Curve Circle"].height = 100.0

    neck_1.nodes["Curve Circle.001"].width  = 140.0
    neck_1.nodes["Curve Circle.001"].height = 100.0

    neck_1.nodes["Set Position"].width  = 140.0
    neck_1.nodes["Set Position"].height = 100.0

    neck_1.nodes["Position"].width  = 140.0
    neck_1.nodes["Position"].height = 100.0

    neck_1.nodes["Separate XYZ"].width  = 140.0
    neck_1.nodes["Separate XYZ"].height = 100.0

    neck_1.nodes["Map Range"].width  = 140.0
    neck_1.nodes["Map Range"].height = 100.0

    neck_1.nodes["Frame.008"].width  = 947.0
    neck_1.nodes["Frame.008"].height = 963.5999755859375

    neck_1.nodes["Float Curve.001"].width  = 240.0
    neck_1.nodes["Float Curve.001"].height = 100.0

    neck_1.nodes["Combine XYZ"].width  = 140.0
    neck_1.nodes["Combine XYZ"].height = 100.0

    neck_1.nodes["Transform Geometry.004"].width  = 140.0
    neck_1.nodes["Transform Geometry.004"].height = 100.0

    neck_1.nodes["Transform Geometry.005"].width  = 140.0
    neck_1.nodes["Transform Geometry.005"].height = 100.0

    neck_1.nodes["Closure Input.001"].width  = 140.0
    neck_1.nodes["Closure Input.001"].height = 100.0

    neck_1.nodes["Closure Output.001"].width  = 140.0
    neck_1.nodes["Closure Output.001"].height = 100.0

    neck_1.nodes["Math"].width  = 140.0
    neck_1.nodes["Math"].height = 100.0

    neck_1.nodes["Math.001"].width  = 140.0
    neck_1.nodes["Math.001"].height = 100.0

    neck_1.nodes["Transform Geometry.001"].width  = 140.0
    neck_1.nodes["Transform Geometry.001"].height = 100.0

    neck_1.nodes["Transform Geometry.006"].width  = 140.0
    neck_1.nodes["Transform Geometry.006"].height = 100.0

    neck_1.nodes["Integer"].width  = 140.0
    neck_1.nodes["Integer"].height = 100.0

    neck_1.nodes["Frame.009"].width  = 998.0
    neck_1.nodes["Frame.009"].height = 1044.13330078125

    neck_1.nodes["Frame.010"].width  = 1816.0
    neck_1.nodes["Frame.010"].height = 2112.599853515625

    neck_1.nodes["Delete Geometry"].width  = 140.0
    neck_1.nodes["Delete Geometry"].height = 100.0

    neck_1.nodes["Position.001"].width  = 140.0
    neck_1.nodes["Position.001"].height = 100.0

    neck_1.nodes["Separate XYZ.001"].width  = 140.0
    neck_1.nodes["Separate XYZ.001"].height = 100.0

    neck_1.nodes["Compare"].width  = 140.0
    neck_1.nodes["Compare"].height = 100.0

    neck_1.nodes["Pipes"].width  = 140.0
    neck_1.nodes["Pipes"].height = 100.0

    neck_1.nodes["Join Geometry"].width  = 140.0
    neck_1.nodes["Join Geometry"].height = 100.0

    neck_1.nodes["Separate XYZ.002"].width  = 140.0
    neck_1.nodes["Separate XYZ.002"].height = 100.0

    neck_1.nodes["Compare.001"].width  = 140.0
    neck_1.nodes["Compare.001"].height = 100.0

    neck_1.nodes["Separate Geometry"].width  = 140.0
    neck_1.nodes["Separate Geometry"].height = 100.0

    neck_1.nodes["Join Geometry.001"].width  = 140.0
    neck_1.nodes["Join Geometry.001"].height = 100.0

    neck_1.nodes["Frame"].width  = 918.0
    neck_1.nodes["Frame"].height = 225.4666748046875

    neck_1.nodes["Rivet"].width  = 140.0
    neck_1.nodes["Rivet"].height = 100.0

    neck_1.nodes["Realize Instances"].width  = 140.0
    neck_1.nodes["Realize Instances"].height = 100.0

    neck_1.nodes["Set Shade Smooth"].width  = 140.0
    neck_1.nodes["Set Shade Smooth"].height = 100.0

    neck_1.nodes["Join Geometry.002"].width  = 140.0
    neck_1.nodes["Join Geometry.002"].height = 100.0

    neck_1.nodes["Switch"].width  = 140.0
    neck_1.nodes["Switch"].height = 100.0

    neck_1.nodes["Group Input"].width  = 140.0
    neck_1.nodes["Group Input"].height = 100.0

    neck_1.nodes["Set Spline Cyclic"].width  = 140.0
    neck_1.nodes["Set Spline Cyclic"].height = 100.0

    neck_1.nodes["Trim Curve"].width  = 140.0
    neck_1.nodes["Trim Curve"].height = 100.0

    neck_1.nodes["Resample Curve.001"].width  = 140.0
    neck_1.nodes["Resample Curve.001"].height = 100.0

    neck_1.nodes["Group.006"].width  = 140.0
    neck_1.nodes["Group.006"].height = 100.0

    neck_1.nodes["Set Curve Normal"].width  = 140.0
    neck_1.nodes["Set Curve Normal"].height = 100.0

    neck_1.nodes["Sample Nearest Surface"].width  = 150.0
    neck_1.nodes["Sample Nearest Surface"].height = 100.0

    neck_1.nodes["Normal"].width  = 140.0
    neck_1.nodes["Normal"].height = 100.0

    neck_1.nodes["Vector Math"].width  = 140.0
    neck_1.nodes["Vector Math"].height = 100.0

    neck_1.nodes["Curve Tangent"].width  = 140.0
    neck_1.nodes["Curve Tangent"].height = 100.0

    neck_1.nodes["Frame.005"].width  = 698.0
    neck_1.nodes["Frame.005"].height = 406.0

    neck_1.nodes["Group.007"].width  = 140.0
    neck_1.nodes["Group.007"].height = 100.0

    neck_1.nodes["Frame.011"].width  = 7007.0
    neck_1.nodes["Frame.011"].height = 4627.60009765625

    neck_1.nodes["Gem in Holder"].width  = 220.0
    neck_1.nodes["Gem in Holder"].height = 100.0

    neck_1.nodes["Curve to Points"].width  = 140.0
    neck_1.nodes["Curve to Points"].height = 100.0

    neck_1.nodes["For Each Geometry Element Input"].width  = 140.0
    neck_1.nodes["For Each Geometry Element Input"].height = 100.0

    neck_1.nodes["For Each Geometry Element Output"].width  = 140.0
    neck_1.nodes["For Each Geometry Element Output"].height = 100.0

    neck_1.nodes["Position.002"].width  = 140.0
    neck_1.nodes["Position.002"].height = 100.0

    neck_1.nodes["Transform Geometry.007"].width  = 140.0
    neck_1.nodes["Transform Geometry.007"].height = 100.0

    neck_1.nodes["Rotate Rotation"].width  = 140.0
    neck_1.nodes["Rotate Rotation"].height = 100.0

    neck_1.nodes["Random Value"].width  = 140.0
    neck_1.nodes["Random Value"].height = 100.0

    neck_1.nodes["Transform Geometry.008"].width  = 140.0
    neck_1.nodes["Transform Geometry.008"].height = 100.0

    neck_1.nodes["Random Value.001"].width  = 140.0
    neck_1.nodes["Random Value.001"].height = 100.0

    neck_1.nodes["Store Named Attribute.001"].width  = 140.0
    neck_1.nodes["Store Named Attribute.001"].height = 100.0

    neck_1.nodes["Random Value.002"].width  = 140.0
    neck_1.nodes["Random Value.002"].height = 100.0

    neck_1.nodes["Rotate Rotation.001"].width  = 140.0
    neck_1.nodes["Rotate Rotation.001"].height = 100.0

    neck_1.nodes["Random Value.003"].width  = 140.0
    neck_1.nodes["Random Value.003"].height = 100.0

    neck_1.nodes["Random Value.004"].width  = 140.0
    neck_1.nodes["Random Value.004"].height = 100.0

    neck_1.nodes["Random Value.005"].width  = 140.0
    neck_1.nodes["Random Value.005"].height = 100.0

    neck_1.nodes["Random Value.006"].width  = 140.0
    neck_1.nodes["Random Value.006"].height = 100.0

    neck_1.nodes["Frame.012"].width  = 2238.0
    neck_1.nodes["Frame.012"].height = 858.13330078125

    neck_1.nodes["Separate Geometry.001"].width  = 140.0
    neck_1.nodes["Separate Geometry.001"].height = 100.0

    neck_1.nodes["Separate XYZ.003"].width  = 140.0
    neck_1.nodes["Separate XYZ.003"].height = 100.0

    neck_1.nodes["Compare.002"].width  = 140.0
    neck_1.nodes["Compare.002"].height = 100.0

    neck_1.nodes["Join Geometry.004"].width  = 140.0
    neck_1.nodes["Join Geometry.004"].height = 100.0

    neck_1.nodes["Trim Curve.001"].width  = 140.0
    neck_1.nodes["Trim Curve.001"].height = 100.0

    neck_1.nodes["Set Curve Normal.001"].width  = 140.0
    neck_1.nodes["Set Curve Normal.001"].height = 100.0

    neck_1.nodes["Compare.003"].width  = 140.0
    neck_1.nodes["Compare.003"].height = 100.0

    neck_1.nodes["Boolean Math"].width  = 140.0
    neck_1.nodes["Boolean Math"].height = 100.0

    neck_1.nodes["Boolean Math.001"].width  = 140.0
    neck_1.nodes["Boolean Math.001"].height = 100.0

    neck_1.nodes["Compare.004"].width  = 140.0
    neck_1.nodes["Compare.004"].height = 100.0

    neck_1.nodes["Frame.001"].width  = 1298.0
    neck_1.nodes["Frame.001"].height = 707.4666748046875

    neck_1.nodes["Boolean Math.002"].width  = 140.0
    neck_1.nodes["Boolean Math.002"].height = 100.0

    neck_1.nodes["Compare.005"].width  = 140.0
    neck_1.nodes["Compare.005"].height = 100.0

    neck_1.nodes["Gem in Holder.001"].width  = 220.0
    neck_1.nodes["Gem in Holder.001"].height = 100.0

    neck_1.nodes["Mesh to Curve.002"].width  = 140.0
    neck_1.nodes["Mesh to Curve.002"].height = 100.0

    neck_1.nodes["Is Edge Boundary"].width  = 140.0
    neck_1.nodes["Is Edge Boundary"].height = 100.0

    neck_1.nodes["Set Spline Cyclic.001"].width  = 140.0
    neck_1.nodes["Set Spline Cyclic.001"].height = 100.0

    neck_1.nodes["Trim Curve.004"].width  = 140.0
    neck_1.nodes["Trim Curve.004"].height = 100.0

    neck_1.nodes["Curve to Points.001"].width  = 140.0
    neck_1.nodes["Curve to Points.001"].height = 100.0

    neck_1.nodes["Set Curve Normal.002"].width  = 140.0
    neck_1.nodes["Set Curve Normal.002"].height = 100.0

    neck_1.nodes["Position.004"].width  = 140.0
    neck_1.nodes["Position.004"].height = 100.0

    neck_1.nodes["For Each Geometry Element Input.001"].width  = 140.0
    neck_1.nodes["For Each Geometry Element Input.001"].height = 100.0

    neck_1.nodes["For Each Geometry Element Output.001"].width  = 140.0
    neck_1.nodes["For Each Geometry Element Output.001"].height = 100.0

    neck_1.nodes["Transform Geometry.009"].width  = 140.0
    neck_1.nodes["Transform Geometry.009"].height = 100.0

    neck_1.nodes["Rotate Rotation.002"].width  = 140.0
    neck_1.nodes["Rotate Rotation.002"].height = 100.0

    neck_1.nodes["Frame.014"].width  = 2678.0
    neck_1.nodes["Frame.014"].height = 506.13330078125

    neck_1.nodes["Random Value.007"].width  = 140.0
    neck_1.nodes["Random Value.007"].height = 100.0

    neck_1.nodes["Random Value.008"].width  = 140.0
    neck_1.nodes["Random Value.008"].height = 100.0

    neck_1.nodes["Distribute Points on Faces"].width  = 170.0
    neck_1.nodes["Distribute Points on Faces"].height = 100.0

    neck_1.nodes["Instance on Points"].width  = 140.0
    neck_1.nodes["Instance on Points"].height = 100.0

    neck_1.nodes["Ico Sphere"].width  = 140.0
    neck_1.nodes["Ico Sphere"].height = 100.0

    neck_1.nodes["Store Named Attribute.002"].width  = 140.0
    neck_1.nodes["Store Named Attribute.002"].height = 100.0

    neck_1.nodes["Random Value.009"].width  = 140.0
    neck_1.nodes["Random Value.009"].height = 100.0

    neck_1.nodes["Boolean Math.003"].width  = 140.0
    neck_1.nodes["Boolean Math.003"].height = 100.0

    neck_1.nodes["Store Named Attribute.003"].width  = 140.0
    neck_1.nodes["Store Named Attribute.003"].height = 100.0

    neck_1.nodes["Realize Instances.001"].width  = 140.0
    neck_1.nodes["Realize Instances.001"].height = 100.0

    neck_1.nodes["Set Shade Smooth.003"].width  = 140.0
    neck_1.nodes["Set Shade Smooth.003"].height = 100.0

    neck_1.nodes["Frame.015"].width  = 1198.0
    neck_1.nodes["Frame.015"].height = 526.13330078125

    neck_1.nodes["Reroute.001"].width  = 14.5
    neck_1.nodes["Reroute.001"].height = 100.0

    neck_1.nodes["Distribute Points on Faces.001"].width  = 170.0
    neck_1.nodes["Distribute Points on Faces.001"].height = 100.0

    neck_1.nodes["Geometry Proximity"].width  = 140.0
    neck_1.nodes["Geometry Proximity"].height = 100.0

    neck_1.nodes["Compare.006"].width  = 140.0
    neck_1.nodes["Compare.006"].height = 100.0

    neck_1.nodes["Gem in Holder.002"].width  = 220.0
    neck_1.nodes["Gem in Holder.002"].height = 100.0

    neck_1.nodes["Instance on Points.001"].width  = 140.0
    neck_1.nodes["Instance on Points.001"].height = 100.0

    neck_1.nodes["Random Value.010"].width  = 140.0
    neck_1.nodes["Random Value.010"].height = 100.0

    neck_1.nodes["Frame.016"].width  = 1338.0
    neck_1.nodes["Frame.016"].height = 842.7999267578125

    neck_1.nodes["Realize Instances.002"].width  = 140.0
    neck_1.nodes["Realize Instances.002"].height = 100.0

    neck_1.nodes["Transform Geometry.010"].width  = 140.0
    neck_1.nodes["Transform Geometry.010"].height = 100.0

    neck_1.nodes["Group.005"].width  = 140.0
    neck_1.nodes["Group.005"].height = 100.0

    neck_1.nodes["Capture Attribute.001"].width  = 140.0
    neck_1.nodes["Capture Attribute.001"].height = 100.0

    neck_1.nodes["Index"].width  = 140.0
    neck_1.nodes["Index"].height = 100.0

    neck_1.nodes["Set Position.001"].width  = 140.0
    neck_1.nodes["Set Position.001"].height = 100.0

    neck_1.nodes["Geometry Proximity.001"].width  = 140.0
    neck_1.nodes["Geometry Proximity.001"].height = 100.0

    neck_1.nodes["Curve to Mesh"].width  = 140.0
    neck_1.nodes["Curve to Mesh"].height = 100.0

    neck_1.nodes["Separate Geometry.002"].width  = 140.0
    neck_1.nodes["Separate Geometry.002"].height = 100.0

    neck_1.nodes["Compare.007"].width  = 140.0
    neck_1.nodes["Compare.007"].height = 100.0

    neck_1.nodes["Separate XYZ.004"].width  = 140.0
    neck_1.nodes["Separate XYZ.004"].height = 100.0

    neck_1.nodes["Trim Curve.002"].width  = 140.0
    neck_1.nodes["Trim Curve.002"].height = 100.0

    neck_1.nodes["Resample Curve.002"].width  = 140.0
    neck_1.nodes["Resample Curve.002"].height = 100.0

    neck_1.nodes["Group.008"].width  = 140.0
    neck_1.nodes["Group.008"].height = 100.0

    neck_1.nodes["Set Curve Normal.003"].width  = 140.0
    neck_1.nodes["Set Curve Normal.003"].height = 100.0

    neck_1.nodes["Frame.013"].width  = 1038.0
    neck_1.nodes["Frame.013"].height = 432.0

    neck_1.nodes["Transform Geometry"].width  = 140.0
    neck_1.nodes["Transform Geometry"].height = 100.0

    neck_1.nodes["Random Value.011"].width  = 140.0
    neck_1.nodes["Random Value.011"].height = 100.0

    neck_1.nodes["Trim Curve.003"].width  = 140.0
    neck_1.nodes["Trim Curve.003"].height = 100.0

    neck_1.nodes["Resample Curve.003"].width  = 140.0
    neck_1.nodes["Resample Curve.003"].height = 100.0

    neck_1.nodes["Group.009"].width  = 140.0
    neck_1.nodes["Group.009"].height = 100.0

    neck_1.nodes["Set Curve Normal.004"].width  = 140.0
    neck_1.nodes["Set Curve Normal.004"].height = 100.0

    neck_1.nodes["Frame.017"].width  = 1498.0
    neck_1.nodes["Frame.017"].height = 550.0

    neck_1.nodes["Transform Geometry.011"].width  = 140.0
    neck_1.nodes["Transform Geometry.011"].height = 100.0

    neck_1.nodes["Mesh to Curve"].width  = 140.0
    neck_1.nodes["Mesh to Curve"].height = 100.0

    neck_1.nodes["Set Curve Tilt"].width  = 140.0
    neck_1.nodes["Set Curve Tilt"].height = 100.0

    neck_1.nodes["Reroute.002"].width  = 14.5
    neck_1.nodes["Reroute.002"].height = 100.0

    neck_1.nodes["Curve Circle.002"].width  = 140.0
    neck_1.nodes["Curve Circle.002"].height = 100.0

    neck_1.nodes["Transform Geometry.012"].width  = 140.0
    neck_1.nodes["Transform Geometry.012"].height = 100.0

    neck_1.nodes["Set Position.002"].width  = 140.0
    neck_1.nodes["Set Position.002"].height = 100.0

    neck_1.nodes["Position.003"].width  = 140.0
    neck_1.nodes["Position.003"].height = 100.0

    neck_1.nodes["Separate XYZ.005"].width  = 140.0
    neck_1.nodes["Separate XYZ.005"].height = 100.0

    neck_1.nodes["Map Range.001"].width  = 140.0
    neck_1.nodes["Map Range.001"].height = 100.0

    neck_1.nodes["Float Curve"].width  = 240.0
    neck_1.nodes["Float Curve"].height = 100.0

    neck_1.nodes["Math.002"].width  = 140.0
    neck_1.nodes["Math.002"].height = 100.0

    neck_1.nodes["Combine XYZ.001"].width  = 140.0
    neck_1.nodes["Combine XYZ.001"].height = 100.0

    neck_1.nodes["Position.005"].width  = 140.0
    neck_1.nodes["Position.005"].height = 100.0

    neck_1.nodes["Vector Math.001"].width  = 140.0
    neck_1.nodes["Vector Math.001"].height = 100.0

    neck_1.nodes["Combine XYZ.002"].width  = 140.0
    neck_1.nodes["Combine XYZ.002"].height = 100.0

    neck_1.nodes["Float Curve.002"].width  = 240.0
    neck_1.nodes["Float Curve.002"].height = 100.0

    neck_1.nodes["Store Named Attribute"].width  = 140.0
    neck_1.nodes["Store Named Attribute"].height = 100.0

    neck_1.nodes["Resample Curve"].width  = 140.0
    neck_1.nodes["Resample Curve"].height = 100.0

    neck_1.nodes["Instance on Points.002"].width  = 140.0
    neck_1.nodes["Instance on Points.002"].height = 100.0

    neck_1.nodes["Align Rotation to Vector"].width  = 140.0
    neck_1.nodes["Align Rotation to Vector"].height = 100.0

    neck_1.nodes["Curve Tangent.001"].width  = 140.0
    neck_1.nodes["Curve Tangent.001"].height = 100.0

    neck_1.nodes["Align Rotation to Vector.001"].width  = 140.0
    neck_1.nodes["Align Rotation to Vector.001"].height = 100.0

    neck_1.nodes["Normal.001"].width  = 140.0
    neck_1.nodes["Normal.001"].height = 100.0

    neck_1.nodes["Rotate Rotation.003"].width  = 140.0
    neck_1.nodes["Rotate Rotation.003"].height = 100.0

    neck_1.nodes["Spline Parameter"].width  = 140.0
    neck_1.nodes["Spline Parameter"].height = 100.0

    neck_1.nodes["Math.003"].width  = 140.0
    neck_1.nodes["Math.003"].height = 100.0

    neck_1.nodes["Math.004"].width  = 140.0
    neck_1.nodes["Math.004"].height = 100.0

    neck_1.nodes["Set Curve Tilt.002"].width  = 140.0
    neck_1.nodes["Set Curve Tilt.002"].height = 100.0

    neck_1.nodes["Map Range.002"].width  = 140.0
    neck_1.nodes["Map Range.002"].height = 100.0

    neck_1.nodes["Float Curve.003"].width  = 240.0
    neck_1.nodes["Float Curve.003"].height = 100.0

    neck_1.nodes["Spline Parameter.001"].width  = 140.0
    neck_1.nodes["Spline Parameter.001"].height = 100.0

    neck_1.nodes["Math.005"].width  = 140.0
    neck_1.nodes["Math.005"].height = 100.0

    neck_1.nodes["Curve Circle.003"].width  = 140.0
    neck_1.nodes["Curve Circle.003"].height = 100.0

    neck_1.nodes["Instance on Points.003"].width  = 140.0
    neck_1.nodes["Instance on Points.003"].height = 100.0

    neck_1.nodes["Ico Sphere.001"].width  = 140.0
    neck_1.nodes["Ico Sphere.001"].height = 100.0

    neck_1.nodes["Cylinder.001"].width  = 140.0
    neck_1.nodes["Cylinder.001"].height = 100.0

    neck_1.nodes["Join Geometry.003"].width  = 140.0
    neck_1.nodes["Join Geometry.003"].height = 100.0

    neck_1.nodes["Ico Sphere.002"].width  = 140.0
    neck_1.nodes["Ico Sphere.002"].height = 100.0

    neck_1.nodes["Transform Geometry.013"].width  = 140.0
    neck_1.nodes["Transform Geometry.013"].height = 100.0

    neck_1.nodes["Set Position.003"].width  = 140.0
    neck_1.nodes["Set Position.003"].height = 100.0

    neck_1.nodes["Vector Math.002"].width  = 140.0
    neck_1.nodes["Vector Math.002"].height = 100.0

    neck_1.nodes["Noise Texture"].width  = 145.0
    neck_1.nodes["Noise Texture"].height = 100.0

    neck_1.nodes["Transform Geometry.014"].width  = 140.0
    neck_1.nodes["Transform Geometry.014"].height = 100.0

    neck_1.nodes["Frame.002"].width  = 1538.0
    neck_1.nodes["Frame.002"].height = 601.333984375

    neck_1.nodes["Rotate Rotation.004"].width  = 140.0
    neck_1.nodes["Rotate Rotation.004"].height = 100.0

    neck_1.nodes["Ico Sphere.003"].width  = 140.0
    neck_1.nodes["Ico Sphere.003"].height = 100.0

    neck_1.nodes["Frame.003"].width  = 678.0
    neck_1.nodes["Frame.003"].height = 294.1328125

    neck_1.nodes["Store Named Attribute.004"].width  = 140.0
    neck_1.nodes["Store Named Attribute.004"].height = 100.0

    neck_1.nodes["Cylinder.002"].width  = 140.0
    neck_1.nodes["Cylinder.002"].height = 100.0

    neck_1.nodes["Math.006"].width  = 140.0
    neck_1.nodes["Math.006"].height = 100.0

    neck_1.nodes["Spline Parameter.002"].width  = 140.0
    neck_1.nodes["Spline Parameter.002"].height = 100.0

    neck_1.nodes["Float Curve.004"].width  = 240.0
    neck_1.nodes["Float Curve.004"].height = 100.0

    neck_1.nodes["Set Position.004"].width  = 140.0
    neck_1.nodes["Set Position.004"].height = 100.0

    neck_1.nodes["Position.006"].width  = 140.0
    neck_1.nodes["Position.006"].height = 100.0

    neck_1.nodes["Separate XYZ.006"].width  = 140.0
    neck_1.nodes["Separate XYZ.006"].height = 100.0

    neck_1.nodes["Math.007"].width  = 140.0
    neck_1.nodes["Math.007"].height = 100.0

    neck_1.nodes["Combine XYZ.003"].width  = 140.0
    neck_1.nodes["Combine XYZ.003"].height = 100.0

    neck_1.nodes["Map Range.003"].width  = 140.0
    neck_1.nodes["Map Range.003"].height = 100.0

    neck_1.nodes["Math.008"].width  = 140.0
    neck_1.nodes["Math.008"].height = 100.0

    neck_1.nodes["Boolean Math.004"].width  = 140.0
    neck_1.nodes["Boolean Math.004"].height = 100.0

    neck_1.nodes["Mesh to Curve.001"].width  = 140.0
    neck_1.nodes["Mesh to Curve.001"].height = 100.0

    neck_1.nodes["Ico Sphere.004"].width  = 140.0
    neck_1.nodes["Ico Sphere.004"].height = 100.0

    neck_1.nodes["Instance on Points.004"].width  = 140.0
    neck_1.nodes["Instance on Points.004"].height = 100.0

    neck_1.nodes["Transform Geometry.015"].width  = 140.0
    neck_1.nodes["Transform Geometry.015"].height = 100.0

    neck_1.nodes["Ico Sphere.005"].width  = 140.0
    neck_1.nodes["Ico Sphere.005"].height = 100.0

    neck_1.nodes["Dual Mesh"].width  = 140.0
    neck_1.nodes["Dual Mesh"].height = 100.0

    neck_1.nodes["Join Geometry.007"].width  = 140.0
    neck_1.nodes["Join Geometry.007"].height = 100.0

    neck_1.nodes["Transform Geometry.016"].width  = 140.0
    neck_1.nodes["Transform Geometry.016"].height = 100.0

    neck_1.nodes["Transform Geometry.017"].width  = 140.0
    neck_1.nodes["Transform Geometry.017"].height = 100.0

    neck_1.nodes["Transform Geometry.018"].width  = 140.0
    neck_1.nodes["Transform Geometry.018"].height = 100.0

    neck_1.nodes["Transform Geometry.019"].width  = 140.0
    neck_1.nodes["Transform Geometry.019"].height = 100.0

    neck_1.nodes["Join Geometry.009"].width  = 140.0
    neck_1.nodes["Join Geometry.009"].height = 100.0

    neck_1.nodes["Store Named Attribute.005"].width  = 140.0
    neck_1.nodes["Store Named Attribute.005"].height = 100.0

    neck_1.nodes["Join Geometry.010"].width  = 140.0
    neck_1.nodes["Join Geometry.010"].height = 100.0

    neck_1.nodes["Store Named Attribute.006"].width  = 140.0
    neck_1.nodes["Store Named Attribute.006"].height = 100.0

    neck_1.nodes["Frame.004"].width  = 3278.0
    neck_1.nodes["Frame.004"].height = 1016.7998046875

    neck_1.nodes["Sample Curve"].width  = 140.0
    neck_1.nodes["Sample Curve"].height = 100.0

    neck_1.nodes["Transform Geometry.020"].width  = 140.0
    neck_1.nodes["Transform Geometry.020"].height = 100.0

    neck_1.nodes["Join Geometry.011"].width  = 140.0
    neck_1.nodes["Join Geometry.011"].height = 100.0

    neck_1.nodes["Vector Math.003"].width  = 140.0
    neck_1.nodes["Vector Math.003"].height = 100.0

    neck_1.nodes["Float Curve.005"].width  = 240.0
    neck_1.nodes["Float Curve.005"].height = 100.0

    neck_1.nodes["Spline Parameter.003"].width  = 140.0
    neck_1.nodes["Spline Parameter.003"].height = 100.0

    neck_1.nodes["Math.009"].width  = 140.0
    neck_1.nodes["Math.009"].height = 100.0

    neck_1.nodes["Math.010"].width  = 140.0
    neck_1.nodes["Math.010"].height = 100.0

    neck_1.nodes["Frame.018"].width  = 4398.0
    neck_1.nodes["Frame.018"].height = 2805.7998046875

    neck_1.nodes["Curve Circle.004"].width  = 140.0
    neck_1.nodes["Curve Circle.004"].height = 100.0

    neck_1.nodes["Transform Geometry.021"].width  = 140.0
    neck_1.nodes["Transform Geometry.021"].height = 100.0

    neck_1.nodes["Set Position.005"].width  = 140.0
    neck_1.nodes["Set Position.005"].height = 100.0

    neck_1.nodes["Position.007"].width  = 140.0
    neck_1.nodes["Position.007"].height = 100.0

    neck_1.nodes["Separate XYZ.007"].width  = 140.0
    neck_1.nodes["Separate XYZ.007"].height = 100.0

    neck_1.nodes["Map Range.004"].width  = 140.0
    neck_1.nodes["Map Range.004"].height = 100.0

    neck_1.nodes["Float Curve.006"].width  = 240.0
    neck_1.nodes["Float Curve.006"].height = 100.0

    neck_1.nodes["Math.011"].width  = 140.0
    neck_1.nodes["Math.011"].height = 100.0

    neck_1.nodes["Combine XYZ.004"].width  = 140.0
    neck_1.nodes["Combine XYZ.004"].height = 100.0

    neck_1.nodes["Position.008"].width  = 140.0
    neck_1.nodes["Position.008"].height = 100.0

    neck_1.nodes["Vector Math.004"].width  = 140.0
    neck_1.nodes["Vector Math.004"].height = 100.0

    neck_1.nodes["Combine XYZ.005"].width  = 140.0
    neck_1.nodes["Combine XYZ.005"].height = 100.0

    neck_1.nodes["Float Curve.007"].width  = 240.0
    neck_1.nodes["Float Curve.007"].height = 100.0

    neck_1.nodes["Resample Curve.004"].width  = 140.0
    neck_1.nodes["Resample Curve.004"].height = 100.0

    neck_1.nodes["Instance on Points.005"].width  = 140.0
    neck_1.nodes["Instance on Points.005"].height = 100.0

    neck_1.nodes["Align Rotation to Vector.002"].width  = 140.0
    neck_1.nodes["Align Rotation to Vector.002"].height = 100.0

    neck_1.nodes["Curve Tangent.002"].width  = 140.0
    neck_1.nodes["Curve Tangent.002"].height = 100.0

    neck_1.nodes["Align Rotation to Vector.003"].width  = 140.0
    neck_1.nodes["Align Rotation to Vector.003"].height = 100.0

    neck_1.nodes["Normal.002"].width  = 140.0
    neck_1.nodes["Normal.002"].height = 100.0

    neck_1.nodes["Spline Parameter.004"].width  = 140.0
    neck_1.nodes["Spline Parameter.004"].height = 100.0

    neck_1.nodes["Math.012"].width  = 140.0
    neck_1.nodes["Math.012"].height = 100.0

    neck_1.nodes["Math.013"].width  = 140.0
    neck_1.nodes["Math.013"].height = 100.0

    neck_1.nodes["Set Curve Tilt.003"].width  = 140.0
    neck_1.nodes["Set Curve Tilt.003"].height = 100.0

    neck_1.nodes["Map Range.005"].width  = 140.0
    neck_1.nodes["Map Range.005"].height = 100.0

    neck_1.nodes["Float Curve.008"].width  = 240.0
    neck_1.nodes["Float Curve.008"].height = 100.0

    neck_1.nodes["Spline Parameter.005"].width  = 140.0
    neck_1.nodes["Spline Parameter.005"].height = 100.0

    neck_1.nodes["Math.014"].width  = 140.0
    neck_1.nodes["Math.014"].height = 100.0

    neck_1.nodes["Frame.020"].width  = 678.0
    neck_1.nodes["Frame.020"].height = 446.1328125

    neck_1.nodes["Math.015"].width  = 140.0
    neck_1.nodes["Math.015"].height = 100.0

    neck_1.nodes["Spline Parameter.006"].width  = 140.0
    neck_1.nodes["Spline Parameter.006"].height = 100.0

    neck_1.nodes["Float Curve.009"].width  = 240.0
    neck_1.nodes["Float Curve.009"].height = 100.0

    neck_1.nodes["Float Curve.010"].width  = 240.0
    neck_1.nodes["Float Curve.010"].height = 100.0

    neck_1.nodes["Spline Parameter.007"].width  = 140.0
    neck_1.nodes["Spline Parameter.007"].height = 100.0

    neck_1.nodes["Math.018"].width  = 140.0
    neck_1.nodes["Math.018"].height = 100.0

    neck_1.nodes["Math.019"].width  = 140.0
    neck_1.nodes["Math.019"].height = 100.0

    neck_1.nodes["Frame.022"].width  = 4638.0
    neck_1.nodes["Frame.022"].height = 2853.7998046875

    neck_1.nodes["Quadrilateral"].width  = 140.0
    neck_1.nodes["Quadrilateral"].height = 100.0

    neck_1.nodes["Fillet Curve"].width  = 140.0
    neck_1.nodes["Fillet Curve"].height = 100.0

    neck_1.nodes["Set Spline Type"].width  = 140.0
    neck_1.nodes["Set Spline Type"].height = 100.0

    neck_1.nodes["Curve to Mesh.001"].width  = 140.0
    neck_1.nodes["Curve to Mesh.001"].height = 100.0

    neck_1.nodes["Curve Circle.005"].width  = 140.0
    neck_1.nodes["Curve Circle.005"].height = 100.0

    neck_1.nodes["Frame.019"].width  = 678.0
    neck_1.nodes["Frame.019"].height = 303.466796875

    neck_1.nodes["Rotate Rotation.006"].width  = 140.0
    neck_1.nodes["Rotate Rotation.006"].height = 100.0

    neck_1.nodes["Rotate Rotation.005"].width  = 140.0
    neck_1.nodes["Rotate Rotation.005"].height = 100.0

    neck_1.nodes["Random Value.012"].width  = 140.0
    neck_1.nodes["Random Value.012"].height = 100.0

    neck_1.nodes["Index.001"].width  = 140.0
    neck_1.nodes["Index.001"].height = 100.0

    neck_1.nodes["Math.016"].width  = 140.0
    neck_1.nodes["Math.016"].height = 100.0

    neck_1.nodes["Switch.001"].width  = 140.0
    neck_1.nodes["Switch.001"].height = 100.0

    neck_1.nodes["Combine XYZ.006"].width  = 140.0
    neck_1.nodes["Combine XYZ.006"].height = 100.0

    neck_1.nodes["Join Geometry.012"].width  = 140.0
    neck_1.nodes["Join Geometry.012"].height = 100.0

    neck_1.nodes["Curve Circle.006"].width  = 140.0
    neck_1.nodes["Curve Circle.006"].height = 100.0

    neck_1.nodes["Curve to Mesh.002"].width  = 140.0
    neck_1.nodes["Curve to Mesh.002"].height = 100.0

    neck_1.nodes["Sample Curve.001"].width  = 140.0
    neck_1.nodes["Sample Curve.001"].height = 100.0

    neck_1.nodes["Transform Geometry.022"].width  = 140.0
    neck_1.nodes["Transform Geometry.022"].height = 100.0

    neck_1.nodes["Join Geometry.013"].width  = 140.0
    neck_1.nodes["Join Geometry.013"].height = 100.0

    neck_1.nodes["Vector Math.005"].width  = 140.0
    neck_1.nodes["Vector Math.005"].height = 100.0

    neck_1.nodes["Curve Circle.007"].width  = 140.0
    neck_1.nodes["Curve Circle.007"].height = 100.0

    neck_1.nodes["Curve Line"].width  = 140.0
    neck_1.nodes["Curve Line"].height = 100.0

    neck_1.nodes["Transform Geometry.023"].width  = 140.0
    neck_1.nodes["Transform Geometry.023"].height = 100.0

    neck_1.nodes["Frame.021"].width  = 458.0
    neck_1.nodes["Frame.021"].height = 303.466796875

    neck_1.nodes["Vector Math.006"].width  = 140.0
    neck_1.nodes["Vector Math.006"].height = 100.0

    neck_1.nodes["Curve to Mesh.003"].width  = 140.0
    neck_1.nodes["Curve to Mesh.003"].height = 100.0

    neck_1.nodes["Resample Curve.005"].width  = 140.0
    neck_1.nodes["Resample Curve.005"].height = 100.0

    neck_1.nodes["Curve Circle.008"].width  = 140.0
    neck_1.nodes["Curve Circle.008"].height = 100.0

    neck_1.nodes["Spline Parameter.008"].width  = 140.0
    neck_1.nodes["Spline Parameter.008"].height = 100.0

    neck_1.nodes["Float Curve.011"].width  = 240.0
    neck_1.nodes["Float Curve.011"].height = 100.0

    neck_1.nodes["Curve Circle.009"].width  = 140.0
    neck_1.nodes["Curve Circle.009"].height = 100.0

    neck_1.nodes["Curve to Mesh.004"].width  = 140.0
    neck_1.nodes["Curve to Mesh.004"].height = 100.0

    neck_1.nodes["Curve Circle.010"].width  = 140.0
    neck_1.nodes["Curve Circle.010"].height = 100.0

    neck_1.nodes["Join Geometry.014"].width  = 140.0
    neck_1.nodes["Join Geometry.014"].height = 100.0

    neck_1.nodes["Curve Circle.011"].width  = 140.0
    neck_1.nodes["Curve Circle.011"].height = 100.0

    neck_1.nodes["Instance on Points.006"].width  = 140.0
    neck_1.nodes["Instance on Points.006"].height = 100.0

    neck_1.nodes["Transform Geometry.024"].width  = 140.0
    neck_1.nodes["Transform Geometry.024"].height = 100.0

    neck_1.nodes["Grid"].width  = 140.0
    neck_1.nodes["Grid"].height = 100.0

    neck_1.nodes["Delete Geometry.001"].width  = 140.0
    neck_1.nodes["Delete Geometry.001"].height = 100.0

    neck_1.nodes["Random Value.013"].width  = 140.0
    neck_1.nodes["Random Value.013"].height = 100.0

    neck_1.nodes["Extrude Mesh"].width  = 140.0
    neck_1.nodes["Extrude Mesh"].height = 100.0

    neck_1.nodes["Flip Faces"].width  = 140.0
    neck_1.nodes["Flip Faces"].height = 100.0

    neck_1.nodes["Join Geometry.015"].width  = 140.0
    neck_1.nodes["Join Geometry.015"].height = 100.0

    neck_1.nodes["Merge by Distance"].width  = 140.0
    neck_1.nodes["Merge by Distance"].height = 100.0

    neck_1.nodes["Transform Geometry.025"].width  = 140.0
    neck_1.nodes["Transform Geometry.025"].height = 100.0

    neck_1.nodes["Subdivision Surface"].width  = 150.0
    neck_1.nodes["Subdivision Surface"].height = 100.0

    neck_1.nodes["Set Shade Smooth.001"].width  = 140.0
    neck_1.nodes["Set Shade Smooth.001"].height = 100.0

    neck_1.nodes["Frame.023"].width  = 2298.0
    neck_1.nodes["Frame.023"].height = 1004.7998046875

    neck_1.nodes["Store Named Attribute.007"].width  = 140.0
    neck_1.nodes["Store Named Attribute.007"].height = 100.0

    neck_1.nodes["Frame.024"].width  = 5787.0
    neck_1.nodes["Frame.024"].height = 5918.5986328125

    neck_1.nodes["Ico Sphere.006"].width  = 140.0
    neck_1.nodes["Ico Sphere.006"].height = 100.0

    neck_1.nodes["Transform Geometry.026"].width  = 140.0
    neck_1.nodes["Transform Geometry.026"].height = 100.0

    neck_1.nodes["Instance on Points.007"].width  = 140.0
    neck_1.nodes["Instance on Points.007"].height = 100.0

    neck_1.nodes["Quadratic Bézier"].width  = 140.0
    neck_1.nodes["Quadratic Bézier"].height = 100.0

    neck_1.nodes["Realize Instances.003"].width  = 140.0
    neck_1.nodes["Realize Instances.003"].height = 100.0

    neck_1.nodes["Mesh to SDF Grid"].width  = 140.0
    neck_1.nodes["Mesh to SDF Grid"].height = 100.0

    neck_1.nodes["Grid to Mesh"].width  = 140.0
    neck_1.nodes["Grid to Mesh"].height = 100.0

    neck_1.nodes["Dual Mesh.001"].width  = 140.0
    neck_1.nodes["Dual Mesh.001"].height = 100.0

    neck_1.nodes["Triangulate"].width  = 140.0
    neck_1.nodes["Triangulate"].height = 100.0

    neck_1.nodes["SDF Grid Boolean"].width  = 140.0
    neck_1.nodes["SDF Grid Boolean"].height = 100.0

    neck_1.nodes["Cube"].width  = 140.0
    neck_1.nodes["Cube"].height = 100.0

    neck_1.nodes["Mesh to SDF Grid.001"].width  = 140.0
    neck_1.nodes["Mesh to SDF Grid.001"].height = 100.0

    neck_1.nodes["Transform Geometry.027"].width  = 140.0
    neck_1.nodes["Transform Geometry.027"].height = 100.0

    neck_1.nodes["Mesh Boolean"].width  = 140.0
    neck_1.nodes["Mesh Boolean"].height = 100.0

    neck_1.nodes["Cube.001"].width  = 140.0
    neck_1.nodes["Cube.001"].height = 100.0

    neck_1.nodes["Transform Geometry.028"].width  = 140.0
    neck_1.nodes["Transform Geometry.028"].height = 100.0

    neck_1.nodes["Delete Geometry.002"].width  = 140.0
    neck_1.nodes["Delete Geometry.002"].height = 100.0

    neck_1.nodes["Mesh Boolean.001"].width  = 140.0
    neck_1.nodes["Mesh Boolean.001"].height = 100.0

    neck_1.nodes["Cube.002"].width  = 140.0
    neck_1.nodes["Cube.002"].height = 100.0

    neck_1.nodes["Transform Geometry.029"].width  = 140.0
    neck_1.nodes["Transform Geometry.029"].height = 100.0

    neck_1.nodes["Join Geometry.016"].width  = 140.0
    neck_1.nodes["Join Geometry.016"].height = 100.0

    neck_1.nodes["Delete Geometry.003"].width  = 140.0
    neck_1.nodes["Delete Geometry.003"].height = 100.0

    neck_1.nodes["Normal.003"].width  = 140.0
    neck_1.nodes["Normal.003"].height = 100.0

    neck_1.nodes["Compare.008"].width  = 140.0
    neck_1.nodes["Compare.008"].height = 100.0

    neck_1.nodes["Mesh to Curve.003"].width  = 140.0
    neck_1.nodes["Mesh to Curve.003"].height = 100.0

    neck_1.nodes["Resample Curve.006"].width  = 140.0
    neck_1.nodes["Resample Curve.006"].height = 100.0

    neck_1.nodes["Set Spline Cyclic.002"].width  = 140.0
    neck_1.nodes["Set Spline Cyclic.002"].height = 100.0

    neck_1.nodes["Curve to Mesh.005"].width  = 140.0
    neck_1.nodes["Curve to Mesh.005"].height = 100.0

    neck_1.nodes["Gem in Holder.003"].width  = 140.0
    neck_1.nodes["Gem in Holder.003"].height = 100.0

    neck_1.nodes["Trim Curve.005"].width  = 140.0
    neck_1.nodes["Trim Curve.005"].height = 100.0

    neck_1.nodes["Instance on Points.008"].width  = 140.0
    neck_1.nodes["Instance on Points.008"].height = 100.0

    neck_1.nodes["Resample Curve.007"].width  = 140.0
    neck_1.nodes["Resample Curve.007"].height = 100.0

    neck_1.nodes["Align Rotation to Vector.004"].width  = 140.0
    neck_1.nodes["Align Rotation to Vector.004"].height = 100.0

    neck_1.nodes["Curve Tangent.003"].width  = 140.0
    neck_1.nodes["Curve Tangent.003"].height = 100.0

    neck_1.nodes["Realize Instances.004"].width  = 140.0
    neck_1.nodes["Realize Instances.004"].height = 100.0

    neck_1.nodes["Transform Geometry.030"].width  = 140.0
    neck_1.nodes["Transform Geometry.030"].height = 100.0

    neck_1.nodes["Flip Faces.002"].width  = 140.0
    neck_1.nodes["Flip Faces.002"].height = 100.0

    neck_1.nodes["Join Geometry.018"].width  = 140.0
    neck_1.nodes["Join Geometry.018"].height = 100.0

    neck_1.nodes["Merge by Distance.001"].width  = 140.0
    neck_1.nodes["Merge by Distance.001"].height = 100.0

    neck_1.nodes["Is Edge Boundary.001"].width  = 140.0
    neck_1.nodes["Is Edge Boundary.001"].height = 100.0

    neck_1.nodes["Spline Parameter.009"].width  = 140.0
    neck_1.nodes["Spline Parameter.009"].height = 100.0

    neck_1.nodes["Math.020"].width  = 140.0
    neck_1.nodes["Math.020"].height = 100.0

    neck_1.nodes["Math.021"].width  = 140.0
    neck_1.nodes["Math.021"].height = 100.0

    neck_1.nodes["Curve to Points.002"].width  = 140.0
    neck_1.nodes["Curve to Points.002"].height = 100.0

    neck_1.nodes["Points to Curves"].width  = 140.0
    neck_1.nodes["Points to Curves"].height = 100.0

    neck_1.nodes["Gradient Texture"].width  = 140.0
    neck_1.nodes["Gradient Texture"].height = 100.0

    neck_1.nodes["Math.022"].width  = 140.0
    neck_1.nodes["Math.022"].height = 100.0

    neck_1.nodes["Math.023"].width  = 140.0
    neck_1.nodes["Math.023"].height = 100.0

    neck_1.nodes["Delete Geometry.004"].width  = 140.0
    neck_1.nodes["Delete Geometry.004"].height = 100.0

    neck_1.nodes["Position.009"].width  = 140.0
    neck_1.nodes["Position.009"].height = 100.0

    neck_1.nodes["Separate XYZ.008"].width  = 140.0
    neck_1.nodes["Separate XYZ.008"].height = 100.0

    neck_1.nodes["Compare.009"].width  = 140.0
    neck_1.nodes["Compare.009"].height = 100.0

    neck_1.nodes["Float Curve.012"].width  = 240.0
    neck_1.nodes["Float Curve.012"].height = 100.0

    neck_1.nodes["Transform Geometry.031"].width  = 140.0
    neck_1.nodes["Transform Geometry.031"].height = 100.0

    neck_1.nodes["Flip Faces.003"].width  = 140.0
    neck_1.nodes["Flip Faces.003"].height = 100.0

    neck_1.nodes["Join Geometry.019"].width  = 140.0
    neck_1.nodes["Join Geometry.019"].height = 100.0

    neck_1.nodes["Gem in Holder.004"].width  = 140.0
    neck_1.nodes["Gem in Holder.004"].height = 100.0

    neck_1.nodes["Join Geometry.020"].width  = 140.0
    neck_1.nodes["Join Geometry.020"].height = 100.0

    neck_1.nodes["Gem in Holder.005"].width  = 140.0
    neck_1.nodes["Gem in Holder.005"].height = 100.0

    neck_1.nodes["Transform Geometry.032"].width  = 140.0
    neck_1.nodes["Transform Geometry.032"].height = 100.0

    neck_1.nodes["Join Geometry.021"].width  = 140.0
    neck_1.nodes["Join Geometry.021"].height = 100.0

    neck_1.nodes["Flip Faces.001"].width  = 140.0
    neck_1.nodes["Flip Faces.001"].height = 100.0

    neck_1.nodes["Gem in Holder.006"].width  = 140.0
    neck_1.nodes["Gem in Holder.006"].height = 100.0

    neck_1.nodes["Transform Geometry.033"].width  = 140.0
    neck_1.nodes["Transform Geometry.033"].height = 100.0

    neck_1.nodes["Join Geometry.022"].width  = 140.0
    neck_1.nodes["Join Geometry.022"].height = 100.0

    neck_1.nodes["Flip Faces.004"].width  = 140.0
    neck_1.nodes["Flip Faces.004"].height = 100.0

    neck_1.nodes["Transform Geometry.034"].width  = 140.0
    neck_1.nodes["Transform Geometry.034"].height = 100.0

    neck_1.nodes["Join Geometry.017"].width  = 140.0
    neck_1.nodes["Join Geometry.017"].height = 100.0

    neck_1.nodes["Store Named Attribute.008"].width  = 140.0
    neck_1.nodes["Store Named Attribute.008"].height = 100.0

    neck_1.nodes["Store Named Attribute.009"].width  = 140.0
    neck_1.nodes["Store Named Attribute.009"].height = 100.0

    neck_1.nodes["Gem in Holder.007"].width  = 140.0
    neck_1.nodes["Gem in Holder.007"].height = 100.0

    neck_1.nodes["Instance on Points.009"].width  = 140.0
    neck_1.nodes["Instance on Points.009"].height = 100.0

    neck_1.nodes["Curve Circle.012"].width  = 140.0
    neck_1.nodes["Curve Circle.012"].height = 100.0

    neck_1.nodes["Transform Geometry.035"].width  = 140.0
    neck_1.nodes["Transform Geometry.035"].height = 100.0

    neck_1.nodes["Frame.025"].width  = 738.0
    neck_1.nodes["Frame.025"].height = 642.80029296875

    neck_1.nodes["Frame.026"].width  = 6538.0
    neck_1.nodes["Frame.026"].height = 1911.80029296875

    neck_1.nodes["Transform Geometry.036"].width  = 140.0
    neck_1.nodes["Transform Geometry.036"].height = 100.0

    neck_1.nodes["Instance on Points.010"].width  = 140.0
    neck_1.nodes["Instance on Points.010"].height = 100.0

    neck_1.nodes["Gem in Holder.008"].width  = 160.0
    neck_1.nodes["Gem in Holder.008"].height = 100.0

    neck_1.nodes["Realize Instances.005"].width  = 140.0
    neck_1.nodes["Realize Instances.005"].height = 100.0

    neck_1.nodes["Capture Attribute.002"].width  = 140.0
    neck_1.nodes["Capture Attribute.002"].height = 100.0

    neck_1.nodes["Index.002"].width  = 140.0
    neck_1.nodes["Index.002"].height = 100.0

    neck_1.nodes["Resample Curve.008"].width  = 140.0
    neck_1.nodes["Resample Curve.008"].height = 100.0

    neck_1.nodes["Align Rotation to Vector.005"].width  = 140.0
    neck_1.nodes["Align Rotation to Vector.005"].height = 100.0

    neck_1.nodes["Normal.004"].width  = 140.0
    neck_1.nodes["Normal.004"].height = 100.0

    neck_1.nodes["Align Rotation to Vector.006"].width  = 140.0
    neck_1.nodes["Align Rotation to Vector.006"].height = 100.0

    neck_1.nodes["Curve Tangent.004"].width  = 140.0
    neck_1.nodes["Curve Tangent.004"].height = 100.0

    neck_1.nodes["Frame.027"].width  = 1778.0
    neck_1.nodes["Frame.027"].height = 574.1337890625

    neck_1.nodes["Trim Curve.006"].width  = 140.0
    neck_1.nodes["Trim Curve.006"].height = 100.0

    neck_1.nodes["Gem in Holder.009"].width  = 220.0
    neck_1.nodes["Gem in Holder.009"].height = 100.0

    neck_1.nodes["Curve to Points.003"].width  = 140.0
    neck_1.nodes["Curve to Points.003"].height = 100.0

    neck_1.nodes["For Each Geometry Element Input.002"].width  = 140.0
    neck_1.nodes["For Each Geometry Element Input.002"].height = 100.0

    neck_1.nodes["For Each Geometry Element Output.002"].width  = 140.0
    neck_1.nodes["For Each Geometry Element Output.002"].height = 100.0

    neck_1.nodes["Position.010"].width  = 140.0
    neck_1.nodes["Position.010"].height = 100.0

    neck_1.nodes["Transform Geometry.037"].width  = 140.0
    neck_1.nodes["Transform Geometry.037"].height = 100.0

    neck_1.nodes["Rotate Rotation.007"].width  = 140.0
    neck_1.nodes["Rotate Rotation.007"].height = 100.0

    neck_1.nodes["Random Value.014"].width  = 140.0
    neck_1.nodes["Random Value.014"].height = 100.0

    neck_1.nodes["Transform Geometry.038"].width  = 140.0
    neck_1.nodes["Transform Geometry.038"].height = 100.0

    neck_1.nodes["Trim Curve.007"].width  = 140.0
    neck_1.nodes["Trim Curve.007"].height = 100.0

    neck_1.nodes["Random Value.015"].width  = 140.0
    neck_1.nodes["Random Value.015"].height = 100.0

    neck_1.nodes["Store Named Attribute.010"].width  = 140.0
    neck_1.nodes["Store Named Attribute.010"].height = 100.0

    neck_1.nodes["Random Value.016"].width  = 140.0
    neck_1.nodes["Random Value.016"].height = 100.0

    neck_1.nodes["Rotate Rotation.008"].width  = 140.0
    neck_1.nodes["Rotate Rotation.008"].height = 100.0

    neck_1.nodes["Random Value.017"].width  = 140.0
    neck_1.nodes["Random Value.017"].height = 100.0

    neck_1.nodes["Random Value.018"].width  = 140.0
    neck_1.nodes["Random Value.018"].height = 100.0

    neck_1.nodes["Random Value.019"].width  = 140.0
    neck_1.nodes["Random Value.019"].height = 100.0

    neck_1.nodes["Random Value.020"].width  = 140.0
    neck_1.nodes["Random Value.020"].height = 100.0

    neck_1.nodes["Frame.028"].width  = 2358.0
    neck_1.nodes["Frame.028"].height = 858.133544921875

    neck_1.nodes["Store Named Attribute.011"].width  = 140.0
    neck_1.nodes["Store Named Attribute.011"].height = 100.0

    neck_1.nodes["Store Named Attribute.012"].width  = 140.0
    neck_1.nodes["Store Named Attribute.012"].height = 100.0

    neck_1.nodes["Mesh Boolean.002"].width  = 140.0
    neck_1.nodes["Mesh Boolean.002"].height = 100.0

    neck_1.nodes["Ico Sphere.007"].width  = 140.0
    neck_1.nodes["Ico Sphere.007"].height = 100.0

    neck_1.nodes["Transform Geometry.039"].width  = 140.0
    neck_1.nodes["Transform Geometry.039"].height = 100.0

    neck_1.nodes["Store Named Attribute.013"].width  = 140.0
    neck_1.nodes["Store Named Attribute.013"].height = 100.0

    neck_1.nodes["Boolean Math.005"].width  = 140.0
    neck_1.nodes["Boolean Math.005"].height = 100.0

    neck_1.nodes["Named Attribute"].width  = 140.0
    neck_1.nodes["Named Attribute"].height = 100.0

    neck_1.nodes["Store Named Attribute.014"].width  = 140.0
    neck_1.nodes["Store Named Attribute.014"].height = 100.0

    neck_1.nodes["Math.017"].width  = 140.0
    neck_1.nodes["Math.017"].height = 100.0

    neck_1.nodes["Transform Geometry.040"].width  = 140.0
    neck_1.nodes["Transform Geometry.040"].height = 100.0

    neck_1.nodes["Transform Geometry.041"].width  = 140.0
    neck_1.nodes["Transform Geometry.041"].height = 100.0

    neck_1.nodes["Scale Elements"].width  = 140.0
    neck_1.nodes["Scale Elements"].height = 100.0

    neck_1.nodes["Transform Geometry.042"].width  = 140.0
    neck_1.nodes["Transform Geometry.042"].height = 100.0

    neck_1.nodes["Join Geometry.023"].width  = 140.0
    neck_1.nodes["Join Geometry.023"].height = 100.0

    neck_1.nodes["Transform Geometry.043"].width  = 140.0
    neck_1.nodes["Transform Geometry.043"].height = 100.0


    # Initialize neck_1 links

    # join_geometry_006.Geometry -> group_003.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.006"].outputs[0],
        neck_1.nodes["Group.003"].inputs[0]
    )
    # vector_001.Vector -> quadratic_b_zier_006.End
    neck_1.links.new(
        neck_1.nodes["Vector.001"].outputs[0],
        neck_1.nodes["Quadratic Bézier.006"].inputs[3]
    )
    # join_geometry_008.Geometry -> bi_rail_loft_001.Profile Curves
    neck_1.links.new(
        neck_1.nodes["Join Geometry.008"].outputs[0],
        neck_1.nodes["Bi-Rail Loft.001"].inputs[2]
    )
    # transform_geometry_002.Geometry -> bi_rail_loft_001.Rail Curve
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.002"].outputs[0],
        neck_1.nodes["Bi-Rail Loft.001"].inputs[1]
    )
    # vector_001.Vector -> quadratic_b_zier_007.Start
    neck_1.links.new(
        neck_1.nodes["Vector.001"].outputs[0],
        neck_1.nodes["Quadratic Bézier.007"].inputs[1]
    )
    # transform_geometry_001.Geometry -> join_geometry_008.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.001"].outputs[0],
        neck_1.nodes["Join Geometry.008"].inputs[0]
    )
    # transform_geometry_005.Geometry -> transform_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.005"].outputs[0],
        neck_1.nodes["Transform Geometry.002"].inputs[0]
    )
    # closure_output_001.Closure -> bi_rail_loft_001.Profile Blending Curve
    neck_1.links.new(
        neck_1.nodes["Closure Output.001"].outputs[0],
        neck_1.nodes["Bi-Rail Loft.001"].inputs[9]
    )
    # combine_xyz.Vector -> set_position.Offset
    neck_1.links.new(
        neck_1.nodes["Combine XYZ"].outputs[0],
        neck_1.nodes["Set Position"].inputs[3]
    )
    # separate_xyz.Y -> map_range.Value
    neck_1.links.new(
        neck_1.nodes["Separate XYZ"].outputs[1],
        neck_1.nodes["Map Range"].inputs[0]
    )
    # closure_input_001.Factor -> math.Value
    neck_1.links.new(
        neck_1.nodes["Closure Input.001"].outputs[0],
        neck_1.nodes["Math"].inputs[0]
    )
    # position.Position -> separate_xyz.Vector
    neck_1.links.new(
        neck_1.nodes["Position"].outputs[0],
        neck_1.nodes["Separate XYZ"].inputs[0]
    )
    # map_range.Result -> float_curve_001.Value
    neck_1.links.new(
        neck_1.nodes["Map Range"].outputs[0],
        neck_1.nodes["Float Curve.001"].inputs[1]
    )
    # transform_geometry_003.Geometry -> set_position.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.003"].outputs[0],
        neck_1.nodes["Set Position"].inputs[0]
    )
    # integer.Integer -> curve_circle_001.Resolution
    neck_1.links.new(
        neck_1.nodes["Integer"].outputs[0],
        neck_1.nodes["Curve Circle.001"].inputs[0]
    )
    # quadratic_b_zier_004.Curve -> join_geometry_005.Geometry
    neck_1.links.new(
        neck_1.nodes["Quadratic Bézier.004"].outputs[0],
        neck_1.nodes["Join Geometry.005"].inputs[0]
    )
    # join_geometry_005.Geometry -> group_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.005"].outputs[0],
        neck_1.nodes["Group.002"].inputs[0]
    )
    # curve_circle.Curve -> transform_geometry_005.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve Circle"].outputs[0],
        neck_1.nodes["Transform Geometry.005"].inputs[0]
    )
    # vector.Vector -> quadratic_b_zier_003.End
    neck_1.links.new(
        neck_1.nodes["Vector"].outputs[0],
        neck_1.nodes["Quadratic Bézier.003"].inputs[3]
    )
    # vector.Vector -> quadratic_b_zier_004.Start
    neck_1.links.new(
        neck_1.nodes["Vector"].outputs[0],
        neck_1.nodes["Quadratic Bézier.004"].inputs[1]
    )
    # float_curve_001.Value -> combine_xyz.Z
    neck_1.links.new(
        neck_1.nodes["Float Curve.001"].outputs[0],
        neck_1.nodes["Combine XYZ"].inputs[2]
    )
    # math_001.Value -> closure_output_001.Factor
    neck_1.links.new(
        neck_1.nodes["Math.001"].outputs[0],
        neck_1.nodes["Closure Output.001"].inputs[0]
    )
    # math.Value -> math_001.Value
    neck_1.links.new(
        neck_1.nodes["Math"].outputs[0],
        neck_1.nodes["Math.001"].inputs[0]
    )
    # integer.Integer -> curve_circle.Resolution
    neck_1.links.new(
        neck_1.nodes["Integer"].outputs[0],
        neck_1.nodes["Curve Circle"].inputs[0]
    )
    # curve_circle_001.Curve -> transform_geometry_004.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve Circle.001"].outputs[0],
        neck_1.nodes["Transform Geometry.004"].inputs[0]
    )
    # set_position.Geometry -> bi_rail_loft_001.Rail Curve
    neck_1.links.new(
        neck_1.nodes["Set Position"].outputs[0],
        neck_1.nodes["Bi-Rail Loft.001"].inputs[0]
    )
    # group_002.Curve -> transform_geometry_006.Geometry
    neck_1.links.new(
        neck_1.nodes["Group.002"].outputs[0],
        neck_1.nodes["Transform Geometry.006"].inputs[0]
    )
    # quadratic_b_zier_007.Curve -> join_geometry_006.Geometry
    neck_1.links.new(
        neck_1.nodes["Quadratic Bézier.007"].outputs[0],
        neck_1.nodes["Join Geometry.006"].inputs[0]
    )
    # group_003.Curve -> transform_geometry_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Group.003"].outputs[0],
        neck_1.nodes["Transform Geometry.001"].inputs[0]
    )
    # transform_geometry_004.Geometry -> transform_geometry_003.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.004"].outputs[0],
        neck_1.nodes["Transform Geometry.003"].inputs[0]
    )
    # join_geometry_004.Geometry -> group_output.Mesh
    neck_1.links.new(
        neck_1.nodes["Join Geometry.004"].outputs[0],
        neck_1.nodes["Group Output"].inputs[0]
    )
    # join_geometry.Geometry -> delete_geometry.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry"].outputs[0],
        neck_1.nodes["Delete Geometry"].inputs[0]
    )
    # position_001.Position -> separate_xyz_001.Vector
    neck_1.links.new(
        neck_1.nodes["Position.001"].outputs[0],
        neck_1.nodes["Separate XYZ.001"].inputs[0]
    )
    # separate_xyz_001.X -> compare.A
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.001"].outputs[0],
        neck_1.nodes["Compare"].inputs[0]
    )
    # compare.Result -> delete_geometry.Selection
    neck_1.links.new(
        neck_1.nodes["Compare"].outputs[0],
        neck_1.nodes["Delete Geometry"].inputs[1]
    )
    # join_geometry_001.Geometry -> pipes.Mesh
    neck_1.links.new(
        neck_1.nodes["Join Geometry.001"].outputs[0],
        neck_1.nodes["Pipes"].inputs[0]
    )
    # bi_rail_loft_001.UVMap -> separate_xyz_002.Vector
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[2],
        neck_1.nodes["Separate XYZ.002"].inputs[0]
    )
    # separate_xyz_002.X -> compare_001.A
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.002"].outputs[0],
        neck_1.nodes["Compare.001"].inputs[0]
    )
    # bi_rail_loft_001.Mesh -> separate_geometry.Geometry
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[0],
        neck_1.nodes["Separate Geometry"].inputs[0]
    )
    # compare_001.Result -> separate_geometry.Selection
    neck_1.links.new(
        neck_1.nodes["Compare.001"].outputs[0],
        neck_1.nodes["Separate Geometry"].inputs[1]
    )
    # bi_rail_loft_001.Mesh -> join_geometry_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[0],
        neck_1.nodes["Join Geometry.001"].inputs[0]
    )
    # bi_rail_loft_001.Mesh -> rivet.Geometry
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[0],
        neck_1.nodes["Rivet"].inputs[0]
    )
    # realize_instances.Geometry -> join_geometry.Geometry
    neck_1.links.new(
        neck_1.nodes["Realize Instances"].outputs[0],
        neck_1.nodes["Join Geometry"].inputs[0]
    )
    # rivet.Mesh -> realize_instances.Geometry
    neck_1.links.new(
        neck_1.nodes["Rivet"].outputs[0],
        neck_1.nodes["Realize Instances"].inputs[0]
    )
    # join_geometry_002.Geometry -> switch.True
    neck_1.links.new(
        neck_1.nodes["Join Geometry.002"].outputs[0],
        neck_1.nodes["Switch"].inputs[2]
    )
    # group_input.Decor -> switch.Switch
    neck_1.links.new(
        neck_1.nodes["Group Input"].outputs[0],
        neck_1.nodes["Switch"].inputs[0]
    )
    # set_position.Geometry -> set_spline_cyclic.Curve
    neck_1.links.new(
        neck_1.nodes["Set Position"].outputs[0],
        neck_1.nodes["Set Spline Cyclic"].inputs[0]
    )
    # set_spline_cyclic.Curve -> trim_curve.Curve
    neck_1.links.new(
        neck_1.nodes["Set Spline Cyclic"].outputs[0],
        neck_1.nodes["Trim Curve"].inputs[0]
    )
    # set_curve_normal.Curve -> group_006.Curves
    neck_1.links.new(
        neck_1.nodes["Set Curve Normal"].outputs[0],
        neck_1.nodes["Group.006"].inputs[0]
    )
    # resample_curve_001.Curve -> set_curve_normal.Curve
    neck_1.links.new(
        neck_1.nodes["Resample Curve.001"].outputs[0],
        neck_1.nodes["Set Curve Normal"].inputs[0]
    )
    # normal.Normal -> sample_nearest_surface.Value
    neck_1.links.new(
        neck_1.nodes["Normal"].outputs[0],
        neck_1.nodes["Sample Nearest Surface"].inputs[1]
    )
    # vector_math.Vector -> set_curve_normal.Normal
    neck_1.links.new(
        neck_1.nodes["Vector Math"].outputs[0],
        neck_1.nodes["Set Curve Normal"].inputs[3]
    )
    # sample_nearest_surface.Value -> vector_math.Vector
    neck_1.links.new(
        neck_1.nodes["Sample Nearest Surface"].outputs[0],
        neck_1.nodes["Vector Math"].inputs[0]
    )
    # curve_tangent.Tangent -> vector_math.Vector
    neck_1.links.new(
        neck_1.nodes["Curve Tangent"].outputs[0],
        neck_1.nodes["Vector Math"].inputs[1]
    )
    # curve_to_points.Points -> for_each_geometry_element_input.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve to Points"].outputs[0],
        neck_1.nodes["For Each Geometry Element Input"].inputs[0]
    )
    # curve_to_points.Rotation -> for_each_geometry_element_input.Rotation
    neck_1.links.new(
        neck_1.nodes["Curve to Points"].outputs[3],
        neck_1.nodes["For Each Geometry Element Input"].inputs[2]
    )
    # position_002.Position -> for_each_geometry_element_input.Position
    neck_1.links.new(
        neck_1.nodes["Position.002"].outputs[0],
        neck_1.nodes["For Each Geometry Element Input"].inputs[3]
    )
    # gem_in_holder.Geometry -> transform_geometry_007.Geometry
    neck_1.links.new(
        neck_1.nodes["Gem in Holder"].outputs[0],
        neck_1.nodes["Transform Geometry.007"].inputs[0]
    )
    # for_each_geometry_element_input.Position -> transform_geometry_007.Translation
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input"].outputs[3],
        neck_1.nodes["Transform Geometry.007"].inputs[2]
    )
    # rotate_rotation_001.Rotation -> transform_geometry_007.Rotation
    neck_1.links.new(
        neck_1.nodes["Rotate Rotation.001"].outputs[0],
        neck_1.nodes["Transform Geometry.007"].inputs[3]
    )
    # for_each_geometry_element_input.Rotation -> rotate_rotation.Rotation
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input"].outputs[2],
        neck_1.nodes["Rotate Rotation"].inputs[0]
    )
    # for_each_geometry_element_input.Index -> random_value.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input"].outputs[0],
        neck_1.nodes["Random Value"].inputs[7]
    )
    # transform_geometry_007.Geometry -> transform_geometry_008.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.007"].outputs[0],
        neck_1.nodes["Transform Geometry.008"].inputs[0]
    )
    # for_each_geometry_element_input.Index -> random_value_001.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input"].outputs[0],
        neck_1.nodes["Random Value.001"].inputs[7]
    )
    # random_value_001.Value -> transform_geometry_007.Scale
    neck_1.links.new(
        neck_1.nodes["Random Value.001"].outputs[1],
        neck_1.nodes["Transform Geometry.007"].inputs[4]
    )
    # transform_geometry_008.Geometry -> for_each_geometry_element_output.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.008"].outputs[0],
        neck_1.nodes["For Each Geometry Element Output"].inputs[1]
    )
    # random_value.Value -> gem_in_holder.Array Count
    neck_1.links.new(
        neck_1.nodes["Random Value"].outputs[2],
        neck_1.nodes["Gem in Holder"].inputs[7]
    )
    # for_each_geometry_element_input.Index -> random_value_002.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input"].outputs[0],
        neck_1.nodes["Random Value.002"].inputs[7]
    )
    # random_value_002.Value -> gem_in_holder.Seed
    neck_1.links.new(
        neck_1.nodes["Random Value.002"].outputs[1],
        neck_1.nodes["Gem in Holder"].inputs[10]
    )
    # rotate_rotation.Rotation -> rotate_rotation_001.Rotation
    neck_1.links.new(
        neck_1.nodes["Rotate Rotation"].outputs[0],
        neck_1.nodes["Rotate Rotation.001"].inputs[0]
    )
    # for_each_geometry_element_input.Index -> random_value_003.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input"].outputs[0],
        neck_1.nodes["Random Value.003"].inputs[7]
    )
    # random_value_003.Value -> gem_in_holder.Split
    neck_1.links.new(
        neck_1.nodes["Random Value.003"].outputs[1],
        neck_1.nodes["Gem in Holder"].inputs[9]
    )
    # for_each_geometry_element_input.Index -> random_value_004.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input"].outputs[0],
        neck_1.nodes["Random Value.004"].inputs[7]
    )
    # random_value_004.Value -> gem_in_holder.Seed
    neck_1.links.new(
        neck_1.nodes["Random Value.004"].outputs[2],
        neck_1.nodes["Gem in Holder"].inputs[5]
    )
    # for_each_geometry_element_input.Index -> random_value_005.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input"].outputs[0],
        neck_1.nodes["Random Value.005"].inputs[7]
    )
    # random_value_005.Value -> gem_in_holder.Count
    neck_1.links.new(
        neck_1.nodes["Random Value.005"].outputs[2],
        neck_1.nodes["Gem in Holder"].inputs[4]
    )
    # for_each_geometry_element_input.Index -> random_value_006.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input"].outputs[0],
        neck_1.nodes["Random Value.006"].inputs[7]
    )
    # random_value_006.Value -> gem_in_holder.Strand Count
    neck_1.links.new(
        neck_1.nodes["Random Value.006"].outputs[2],
        neck_1.nodes["Gem in Holder"].inputs[8]
    )
    # trim_curve.Curve -> resample_curve_001.Curve
    neck_1.links.new(
        neck_1.nodes["Trim Curve"].outputs[0],
        neck_1.nodes["Resample Curve.001"].inputs[0]
    )
    # bi_rail_loft_001.Mesh -> sample_nearest_surface.Mesh
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[0],
        neck_1.nodes["Sample Nearest Surface"].inputs[0]
    )
    # bi_rail_loft_001.Mesh -> separate_geometry_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[0],
        neck_1.nodes["Separate Geometry.001"].inputs[0]
    )
    # bi_rail_loft_001.UVMap -> separate_xyz_003.Vector
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[2],
        neck_1.nodes["Separate XYZ.003"].inputs[0]
    )
    # separate_xyz_003.X -> compare_002.A
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.003"].outputs[0],
        neck_1.nodes["Compare.002"].inputs[0]
    )
    # set_shade_smooth.Mesh -> join_geometry_004.Geometry
    neck_1.links.new(
        neck_1.nodes["Set Shade Smooth"].outputs[0],
        neck_1.nodes["Join Geometry.004"].inputs[0]
    )
    # set_spline_cyclic.Curve -> trim_curve_001.Curve
    neck_1.links.new(
        neck_1.nodes["Set Spline Cyclic"].outputs[0],
        neck_1.nodes["Trim Curve.001"].inputs[0]
    )
    # set_curve_normal_001.Curve -> curve_to_points.Curve
    neck_1.links.new(
        neck_1.nodes["Set Curve Normal.001"].outputs[0],
        neck_1.nodes["Curve to Points"].inputs[0]
    )
    # trim_curve_001.Curve -> set_curve_normal_001.Curve
    neck_1.links.new(
        neck_1.nodes["Trim Curve.001"].outputs[0],
        neck_1.nodes["Set Curve Normal.001"].inputs[0]
    )
    # sample_nearest_surface.Value -> set_curve_normal_001.Normal
    neck_1.links.new(
        neck_1.nodes["Sample Nearest Surface"].outputs[0],
        neck_1.nodes["Set Curve Normal.001"].inputs[3]
    )
    # separate_xyz_003.X -> compare_003.A
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.003"].outputs[0],
        neck_1.nodes["Compare.003"].inputs[0]
    )
    # boolean_math_002.Boolean -> separate_geometry_001.Selection
    neck_1.links.new(
        neck_1.nodes["Boolean Math.002"].outputs[0],
        neck_1.nodes["Separate Geometry.001"].inputs[1]
    )
    # compare_002.Result -> boolean_math.Boolean
    neck_1.links.new(
        neck_1.nodes["Compare.002"].outputs[0],
        neck_1.nodes["Boolean Math"].inputs[0]
    )
    # compare_003.Result -> boolean_math.Boolean
    neck_1.links.new(
        neck_1.nodes["Compare.003"].outputs[0],
        neck_1.nodes["Boolean Math"].inputs[1]
    )
    # boolean_math.Boolean -> boolean_math_001.Boolean
    neck_1.links.new(
        neck_1.nodes["Boolean Math"].outputs[0],
        neck_1.nodes["Boolean Math.001"].inputs[0]
    )
    # separate_xyz_003.Y -> compare_004.A
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.003"].outputs[1],
        neck_1.nodes["Compare.004"].inputs[0]
    )
    # compare_004.Result -> boolean_math_001.Boolean
    neck_1.links.new(
        neck_1.nodes["Compare.004"].outputs[0],
        neck_1.nodes["Boolean Math.001"].inputs[1]
    )
    # separate_geometry_001.Selection -> group_007.Mesh
    neck_1.links.new(
        neck_1.nodes["Separate Geometry.001"].outputs[0],
        neck_1.nodes["Group.007"].inputs[0]
    )
    # boolean_math_001.Boolean -> boolean_math_002.Boolean
    neck_1.links.new(
        neck_1.nodes["Boolean Math.001"].outputs[0],
        neck_1.nodes["Boolean Math.002"].inputs[0]
    )
    # separate_xyz_003.Y -> compare_005.A
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.003"].outputs[1],
        neck_1.nodes["Compare.005"].inputs[0]
    )
    # compare_005.Result -> boolean_math_002.Boolean
    neck_1.links.new(
        neck_1.nodes["Compare.005"].outputs[0],
        neck_1.nodes["Boolean Math.002"].inputs[1]
    )
    # is_edge_boundary.Is Edge Boundary -> mesh_to_curve_002.Selection
    neck_1.links.new(
        neck_1.nodes["Is Edge Boundary"].outputs[0],
        neck_1.nodes["Mesh to Curve.002"].inputs[1]
    )
    # set_curve_normal_002.Curve -> set_spline_cyclic_001.Curve
    neck_1.links.new(
        neck_1.nodes["Set Curve Normal.002"].outputs[0],
        neck_1.nodes["Set Spline Cyclic.001"].inputs[0]
    )
    # set_spline_cyclic_001.Curve -> trim_curve_004.Curve
    neck_1.links.new(
        neck_1.nodes["Set Spline Cyclic.001"].outputs[0],
        neck_1.nodes["Trim Curve.004"].inputs[0]
    )
    # trim_curve_004.Curve -> curve_to_points_001.Curve
    neck_1.links.new(
        neck_1.nodes["Trim Curve.004"].outputs[0],
        neck_1.nodes["Curve to Points.001"].inputs[0]
    )
    # mesh_to_curve_002.Curve -> set_curve_normal_002.Curve
    neck_1.links.new(
        neck_1.nodes["Mesh to Curve.002"].outputs[0],
        neck_1.nodes["Set Curve Normal.002"].inputs[0]
    )
    # separate_geometry_001.Selection -> mesh_to_curve_002.Mesh
    neck_1.links.new(
        neck_1.nodes["Separate Geometry.001"].outputs[0],
        neck_1.nodes["Mesh to Curve.002"].inputs[0]
    )
    # curve_to_points_001.Points -> for_each_geometry_element_input_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve to Points.001"].outputs[0],
        neck_1.nodes["For Each Geometry Element Input.001"].inputs[0]
    )
    # store_named_attribute_001.Geometry -> for_each_geometry_element_output_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.001"].outputs[0],
        neck_1.nodes["For Each Geometry Element Output.001"].inputs[1]
    )
    # position_004.Position -> for_each_geometry_element_input_001.Position
    neck_1.links.new(
        neck_1.nodes["Position.004"].outputs[0],
        neck_1.nodes["For Each Geometry Element Input.001"].inputs[2]
    )
    # curve_to_points_001.Rotation -> for_each_geometry_element_input_001.Rotation
    neck_1.links.new(
        neck_1.nodes["Curve to Points.001"].outputs[3],
        neck_1.nodes["For Each Geometry Element Input.001"].inputs[3]
    )
    # for_each_geometry_element_input_001.Position -> transform_geometry_009.Translation
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.001"].outputs[2],
        neck_1.nodes["Transform Geometry.009"].inputs[2]
    )
    # rotate_rotation_002.Rotation -> transform_geometry_009.Rotation
    neck_1.links.new(
        neck_1.nodes["Rotate Rotation.002"].outputs[0],
        neck_1.nodes["Transform Geometry.009"].inputs[3]
    )
    # for_each_geometry_element_input_001.Rotation -> rotate_rotation_002.Rotation
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.001"].outputs[3],
        neck_1.nodes["Rotate Rotation.002"].inputs[0]
    )
    # for_each_geometry_element_input_001.Index -> random_value_007.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.001"].outputs[0],
        neck_1.nodes["Random Value.007"].inputs[7]
    )
    # random_value_007.Value -> gem_in_holder_001.Seed
    neck_1.links.new(
        neck_1.nodes["Random Value.007"].outputs[1],
        neck_1.nodes["Gem in Holder.001"].inputs[10]
    )
    # for_each_geometry_element_input_001.Index -> random_value_008.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.001"].outputs[0],
        neck_1.nodes["Random Value.008"].inputs[7]
    )
    # random_value_008.Value -> gem_in_holder_001.Split
    neck_1.links.new(
        neck_1.nodes["Random Value.008"].outputs[1],
        neck_1.nodes["Gem in Holder.001"].inputs[9]
    )
    # separate_geometry_001.Selection -> distribute_points_on_faces.Mesh
    neck_1.links.new(
        neck_1.nodes["Separate Geometry.001"].outputs[0],
        neck_1.nodes["Distribute Points on Faces"].inputs[0]
    )
    # distribute_points_on_faces.Points -> instance_on_points.Points
    neck_1.links.new(
        neck_1.nodes["Distribute Points on Faces"].outputs[0],
        neck_1.nodes["Instance on Points"].inputs[0]
    )
    # set_shade_smooth_003.Mesh -> instance_on_points.Instance
    neck_1.links.new(
        neck_1.nodes["Set Shade Smooth.003"].outputs[0],
        neck_1.nodes["Instance on Points"].inputs[2]
    )
    # instance_on_points.Instances -> store_named_attribute_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Instance on Points"].outputs[0],
        neck_1.nodes["Store Named Attribute.002"].inputs[0]
    )
    # random_value_009.Value -> store_named_attribute_002.Value
    neck_1.links.new(
        neck_1.nodes["Random Value.009"].outputs[3],
        neck_1.nodes["Store Named Attribute.002"].inputs[3]
    )
    # random_value_009.Value -> boolean_math_003.Boolean
    neck_1.links.new(
        neck_1.nodes["Random Value.009"].outputs[3],
        neck_1.nodes["Boolean Math.003"].inputs[0]
    )
    # store_named_attribute_002.Geometry -> store_named_attribute_003.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.002"].outputs[0],
        neck_1.nodes["Store Named Attribute.003"].inputs[0]
    )
    # boolean_math_003.Boolean -> store_named_attribute_003.Value
    neck_1.links.new(
        neck_1.nodes["Boolean Math.003"].outputs[0],
        neck_1.nodes["Store Named Attribute.003"].inputs[3]
    )
    # store_named_attribute_003.Geometry -> realize_instances_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.003"].outputs[0],
        neck_1.nodes["Realize Instances.001"].inputs[0]
    )
    # ico_sphere.Mesh -> set_shade_smooth_003.Mesh
    neck_1.links.new(
        neck_1.nodes["Ico Sphere"].outputs[0],
        neck_1.nodes["Set Shade Smooth.003"].inputs[0]
    )
    # reroute_001.Output -> distribute_points_on_faces_001.Mesh
    neck_1.links.new(
        neck_1.nodes["Reroute.001"].outputs[0],
        neck_1.nodes["Distribute Points on Faces.001"].inputs[0]
    )
    # geometry_proximity.Distance -> compare_006.A
    neck_1.links.new(
        neck_1.nodes["Geometry Proximity"].outputs[1],
        neck_1.nodes["Compare.006"].inputs[0]
    )
    # compare_006.Result -> distribute_points_on_faces_001.Selection
    neck_1.links.new(
        neck_1.nodes["Compare.006"].outputs[0],
        neck_1.nodes["Distribute Points on Faces.001"].inputs[1]
    )
    # distribute_points_on_faces_001.Points -> instance_on_points_001.Points
    neck_1.links.new(
        neck_1.nodes["Distribute Points on Faces.001"].outputs[0],
        neck_1.nodes["Instance on Points.001"].inputs[0]
    )
    # transform_geometry_010.Geometry -> instance_on_points_001.Instance
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.010"].outputs[0],
        neck_1.nodes["Instance on Points.001"].inputs[2]
    )
    # distribute_points_on_faces_001.Rotation -> instance_on_points_001.Rotation
    neck_1.links.new(
        neck_1.nodes["Distribute Points on Faces.001"].outputs[2],
        neck_1.nodes["Instance on Points.001"].inputs[5]
    )
    # random_value_010.Value -> instance_on_points_001.Scale
    neck_1.links.new(
        neck_1.nodes["Random Value.010"].outputs[1],
        neck_1.nodes["Instance on Points.001"].inputs[6]
    )
    # capture_attribute_001.Geometry -> realize_instances_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Capture Attribute.001"].outputs[0],
        neck_1.nodes["Realize Instances.002"].inputs[0]
    )
    # gem_in_holder_002.Geometry -> transform_geometry_010.Geometry
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.002"].outputs[0],
        neck_1.nodes["Transform Geometry.010"].inputs[0]
    )
    # instance_on_points_001.Instances -> capture_attribute_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Instance on Points.001"].outputs[0],
        neck_1.nodes["Capture Attribute.001"].inputs[0]
    )
    # index.Index -> capture_attribute_001.Index
    neck_1.links.new(
        neck_1.nodes["Index"].outputs[0],
        neck_1.nodes["Capture Attribute.001"].inputs[1]
    )
    # realize_instances_002.Geometry -> group_005.Geometry
    neck_1.links.new(
        neck_1.nodes["Realize Instances.002"].outputs[0],
        neck_1.nodes["Group.005"].inputs[0]
    )
    # capture_attribute_001.Index -> group_005.ID
    neck_1.links.new(
        neck_1.nodes["Capture Attribute.001"].outputs[1],
        neck_1.nodes["Group.005"].inputs[1]
    )
    # for_each_geometry_element_output_001.Geometry -> geometry_proximity.Geometry
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Output.001"].outputs[2],
        neck_1.nodes["Geometry Proximity"].inputs[0]
    )
    # sample_nearest_surface.Value -> set_curve_normal_002.Normal
    neck_1.links.new(
        neck_1.nodes["Sample Nearest Surface"].outputs[0],
        neck_1.nodes["Set Curve Normal.002"].inputs[3]
    )
    # group_005.Geometry -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Group.005"].outputs[0],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )
    # gem_in_holder_001.Wing Curve -> transform_geometry_009.Geometry
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.001"].outputs[4],
        neck_1.nodes["Transform Geometry.009"].inputs[0]
    )
    # transform_geometry_009.Geometry -> set_position_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.009"].outputs[0],
        neck_1.nodes["Set Position.001"].inputs[0]
    )
    # bi_rail_loft_001.Mesh -> geometry_proximity_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[0],
        neck_1.nodes["Geometry Proximity.001"].inputs[0]
    )
    # geometry_proximity_001.Position -> set_position_001.Position
    neck_1.links.new(
        neck_1.nodes["Geometry Proximity.001"].outputs[0],
        neck_1.nodes["Set Position.001"].inputs[2]
    )
    # set_position_001.Geometry -> curve_to_mesh.Curve
    neck_1.links.new(
        neck_1.nodes["Set Position.001"].outputs[0],
        neck_1.nodes["Curve to Mesh"].inputs[0]
    )
    # gem_in_holder_001.Profile Curve -> curve_to_mesh.Profile Curve
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.001"].outputs[1],
        neck_1.nodes["Curve to Mesh"].inputs[1]
    )
    # gem_in_holder_001.Profile Scale -> curve_to_mesh.Scale
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.001"].outputs[2],
        neck_1.nodes["Curve to Mesh"].inputs[2]
    )
    # bi_rail_loft_001.Interpolated Profiles -> separate_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[1],
        neck_1.nodes["Separate Geometry.002"].inputs[0]
    )
    # bi_rail_loft_001.UVMap -> separate_xyz_004.Vector
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[2],
        neck_1.nodes["Separate XYZ.004"].inputs[0]
    )
    # separate_xyz_004.Y -> compare_007.A
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.004"].outputs[1],
        neck_1.nodes["Compare.007"].inputs[0]
    )
    # compare_007.Result -> separate_geometry_002.Selection
    neck_1.links.new(
        neck_1.nodes["Compare.007"].outputs[0],
        neck_1.nodes["Separate Geometry.002"].inputs[1]
    )
    # transform_geometry.Geometry -> group_008.Curves
    neck_1.links.new(
        neck_1.nodes["Transform Geometry"].outputs[0],
        neck_1.nodes["Group.008"].inputs[0]
    )
    # resample_curve_002.Curve -> set_curve_normal_003.Curve
    neck_1.links.new(
        neck_1.nodes["Resample Curve.002"].outputs[0],
        neck_1.nodes["Set Curve Normal.003"].inputs[0]
    )
    # trim_curve_002.Curve -> resample_curve_002.Curve
    neck_1.links.new(
        neck_1.nodes["Trim Curve.002"].outputs[0],
        neck_1.nodes["Resample Curve.002"].inputs[0]
    )
    # separate_geometry_002.Selection -> trim_curve_002.Curve
    neck_1.links.new(
        neck_1.nodes["Separate Geometry.002"].outputs[0],
        neck_1.nodes["Trim Curve.002"].inputs[0]
    )
    # set_curve_normal_003.Curve -> transform_geometry.Geometry
    neck_1.links.new(
        neck_1.nodes["Set Curve Normal.003"].outputs[0],
        neck_1.nodes["Transform Geometry"].inputs[0]
    )
    # curve_to_mesh.Mesh -> store_named_attribute_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve to Mesh"].outputs[0],
        neck_1.nodes["Store Named Attribute.001"].inputs[0]
    )
    # random_value_011.Value -> instance_on_points.Scale
    neck_1.links.new(
        neck_1.nodes["Random Value.011"].outputs[1],
        neck_1.nodes["Instance on Points"].inputs[6]
    )
    # bi_rail_loft_001.Mesh -> reroute_001.Input
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[0],
        neck_1.nodes["Reroute.001"].inputs[0]
    )
    # transform_geometry_011.Geometry -> group_009.Curves
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.011"].outputs[0],
        neck_1.nodes["Group.009"].inputs[0]
    )
    # resample_curve_003.Curve -> set_curve_normal_004.Curve
    neck_1.links.new(
        neck_1.nodes["Resample Curve.003"].outputs[0],
        neck_1.nodes["Set Curve Normal.004"].inputs[0]
    )
    # trim_curve_003.Curve -> resample_curve_003.Curve
    neck_1.links.new(
        neck_1.nodes["Trim Curve.003"].outputs[0],
        neck_1.nodes["Resample Curve.003"].inputs[0]
    )
    # set_curve_tilt.Curve -> transform_geometry_011.Geometry
    neck_1.links.new(
        neck_1.nodes["Set Curve Tilt"].outputs[0],
        neck_1.nodes["Transform Geometry.011"].inputs[0]
    )
    # separate_geometry.Selection -> mesh_to_curve.Mesh
    neck_1.links.new(
        neck_1.nodes["Separate Geometry"].outputs[0],
        neck_1.nodes["Mesh to Curve"].inputs[0]
    )
    # mesh_to_curve.Curve -> trim_curve_003.Curve
    neck_1.links.new(
        neck_1.nodes["Mesh to Curve"].outputs[0],
        neck_1.nodes["Trim Curve.003"].inputs[0]
    )
    # vector_math.Vector -> set_curve_normal_004.Normal
    neck_1.links.new(
        neck_1.nodes["Vector Math"].outputs[0],
        neck_1.nodes["Set Curve Normal.004"].inputs[3]
    )
    # set_curve_normal_004.Curve -> set_curve_tilt.Curve
    neck_1.links.new(
        neck_1.nodes["Set Curve Normal.004"].outputs[0],
        neck_1.nodes["Set Curve Tilt"].inputs[0]
    )
    # group_007.Mesh -> reroute_002.Input
    neck_1.links.new(
        neck_1.nodes["Group.007"].outputs[0],
        neck_1.nodes["Reroute.002"].inputs[0]
    )
    # curve_circle_002.Curve -> set_position_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve Circle.002"].outputs[0],
        neck_1.nodes["Set Position.002"].inputs[0]
    )
    # position_003.Position -> separate_xyz_005.Vector
    neck_1.links.new(
        neck_1.nodes["Position.003"].outputs[0],
        neck_1.nodes["Separate XYZ.005"].inputs[0]
    )
    # separate_xyz_005.Y -> map_range_001.Value
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.005"].outputs[1],
        neck_1.nodes["Map Range.001"].inputs[0]
    )
    # map_range_001.Result -> float_curve.Value
    neck_1.links.new(
        neck_1.nodes["Map Range.001"].outputs[0],
        neck_1.nodes["Float Curve"].inputs[1]
    )
    # math_006.Value -> math_002.Value
    neck_1.links.new(
        neck_1.nodes["Math.006"].outputs[0],
        neck_1.nodes["Math.002"].inputs[0]
    )
    # combine_xyz_001.Vector -> set_position_002.Offset
    neck_1.links.new(
        neck_1.nodes["Combine XYZ.001"].outputs[0],
        neck_1.nodes["Set Position.002"].inputs[3]
    )
    # math_002.Value -> combine_xyz_001.Z
    neck_1.links.new(
        neck_1.nodes["Math.002"].outputs[0],
        neck_1.nodes["Combine XYZ.001"].inputs[2]
    )
    # set_position_002.Geometry -> transform_geometry_012.Geometry
    neck_1.links.new(
        neck_1.nodes["Set Position.002"].outputs[0],
        neck_1.nodes["Transform Geometry.012"].inputs[0]
    )
    # position_005.Position -> vector_math_001.Vector
    neck_1.links.new(
        neck_1.nodes["Position.005"].outputs[0],
        neck_1.nodes["Vector Math.001"].inputs[0]
    )
    # vector_math_001.Vector -> set_position_002.Position
    neck_1.links.new(
        neck_1.nodes["Vector Math.001"].outputs[0],
        neck_1.nodes["Set Position.002"].inputs[2]
    )
    # combine_xyz_002.Vector -> vector_math_001.Vector
    neck_1.links.new(
        neck_1.nodes["Combine XYZ.002"].outputs[0],
        neck_1.nodes["Vector Math.001"].inputs[1]
    )
    # map_range_001.Result -> float_curve_002.Value
    neck_1.links.new(
        neck_1.nodes["Map Range.001"].outputs[0],
        neck_1.nodes["Float Curve.002"].inputs[1]
    )
    # float_curve_002.Value -> combine_xyz_002.X
    neck_1.links.new(
        neck_1.nodes["Float Curve.002"].outputs[0],
        neck_1.nodes["Combine XYZ.002"].inputs[0]
    )
    # transform_geometry_012.Geometry -> resample_curve.Curve
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.012"].outputs[0],
        neck_1.nodes["Resample Curve"].inputs[0]
    )
    # set_curve_tilt_002.Curve -> instance_on_points_002.Points
    neck_1.links.new(
        neck_1.nodes["Set Curve Tilt.002"].outputs[0],
        neck_1.nodes["Instance on Points.002"].inputs[0]
    )
    # curve_tangent_001.Tangent -> align_rotation_to_vector.Vector
    neck_1.links.new(
        neck_1.nodes["Curve Tangent.001"].outputs[0],
        neck_1.nodes["Align Rotation to Vector"].inputs[2]
    )
    # align_rotation_to_vector.Rotation -> align_rotation_to_vector_001.Rotation
    neck_1.links.new(
        neck_1.nodes["Align Rotation to Vector"].outputs[0],
        neck_1.nodes["Align Rotation to Vector.001"].inputs[0]
    )
    # normal_001.Normal -> align_rotation_to_vector_001.Vector
    neck_1.links.new(
        neck_1.nodes["Normal.001"].outputs[0],
        neck_1.nodes["Align Rotation to Vector.001"].inputs[2]
    )
    # align_rotation_to_vector_001.Rotation -> rotate_rotation_003.Rotation
    neck_1.links.new(
        neck_1.nodes["Align Rotation to Vector.001"].outputs[0],
        neck_1.nodes["Rotate Rotation.003"].inputs[0]
    )
    # spline_parameter.Factor -> math_003.Value
    neck_1.links.new(
        neck_1.nodes["Spline Parameter"].outputs[0],
        neck_1.nodes["Math.003"].inputs[0]
    )
    # math_003.Value -> math_004.Value
    neck_1.links.new(
        neck_1.nodes["Math.003"].outputs[0],
        neck_1.nodes["Math.004"].inputs[0]
    )
    # resample_curve.Curve -> set_curve_tilt_002.Curve
    neck_1.links.new(
        neck_1.nodes["Resample Curve"].outputs[0],
        neck_1.nodes["Set Curve Tilt.002"].inputs[0]
    )
    # math_004.Value -> map_range_002.Value
    neck_1.links.new(
        neck_1.nodes["Math.004"].outputs[0],
        neck_1.nodes["Map Range.002"].inputs[0]
    )
    # map_range_002.Result -> set_curve_tilt_002.Tilt
    neck_1.links.new(
        neck_1.nodes["Map Range.002"].outputs[0],
        neck_1.nodes["Set Curve Tilt.002"].inputs[2]
    )
    # spline_parameter_001.Factor -> float_curve_003.Value
    neck_1.links.new(
        neck_1.nodes["Spline Parameter.001"].outputs[0],
        neck_1.nodes["Float Curve.003"].inputs[1]
    )
    # float_curve_003.Value -> math_005.Value
    neck_1.links.new(
        neck_1.nodes["Float Curve.003"].outputs[0],
        neck_1.nodes["Math.005"].inputs[0]
    )
    # math_010.Value -> combine_xyz_001.Y
    neck_1.links.new(
        neck_1.nodes["Math.010"].outputs[0],
        neck_1.nodes["Combine XYZ.001"].inputs[1]
    )
    # curve_circle_003.Curve -> instance_on_points_003.Points
    neck_1.links.new(
        neck_1.nodes["Curve Circle.003"].outputs[0],
        neck_1.nodes["Instance on Points.003"].inputs[0]
    )
    # ico_sphere_001.Mesh -> instance_on_points_003.Instance
    neck_1.links.new(
        neck_1.nodes["Ico Sphere.001"].outputs[0],
        neck_1.nodes["Instance on Points.003"].inputs[2]
    )
    # instance_on_points_003.Instances -> join_geometry_003.Geometry
    neck_1.links.new(
        neck_1.nodes["Instance on Points.003"].outputs[0],
        neck_1.nodes["Join Geometry.003"].inputs[0]
    )
    # set_position_003.Geometry -> transform_geometry_013.Geometry
    neck_1.links.new(
        neck_1.nodes["Set Position.003"].outputs[0],
        neck_1.nodes["Transform Geometry.013"].inputs[0]
    )
    # ico_sphere_002.Mesh -> set_position_003.Geometry
    neck_1.links.new(
        neck_1.nodes["Ico Sphere.002"].outputs[0],
        neck_1.nodes["Set Position.003"].inputs[0]
    )
    # vector_math_002.Vector -> set_position_003.Offset
    neck_1.links.new(
        neck_1.nodes["Vector Math.002"].outputs[0],
        neck_1.nodes["Set Position.003"].inputs[3]
    )
    # noise_texture.Factor -> vector_math_002.Vector
    neck_1.links.new(
        neck_1.nodes["Noise Texture"].outputs[0],
        neck_1.nodes["Vector Math.002"].inputs[0]
    )
    # transform_geometry_013.Geometry -> transform_geometry_014.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.013"].outputs[0],
        neck_1.nodes["Transform Geometry.014"].inputs[0]
    )
    # store_named_attribute_004.Geometry -> instance_on_points_002.Instance
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.004"].outputs[0],
        neck_1.nodes["Instance on Points.002"].inputs[2]
    )
    # rotate_rotation_003.Rotation -> rotate_rotation_004.Rotation
    neck_1.links.new(
        neck_1.nodes["Rotate Rotation.003"].outputs[0],
        neck_1.nodes["Rotate Rotation.004"].inputs[0]
    )
    # rotate_rotation_004.Rotation -> instance_on_points_002.Rotation
    neck_1.links.new(
        neck_1.nodes["Rotate Rotation.004"].outputs[0],
        neck_1.nodes["Instance on Points.002"].inputs[5]
    )
    # join_geometry_003.Geometry -> store_named_attribute_004.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.003"].outputs[0],
        neck_1.nodes["Store Named Attribute.004"].inputs[0]
    )
    # delete_geometry.Geometry -> set_shade_smooth.Mesh
    neck_1.links.new(
        neck_1.nodes["Delete Geometry"].outputs[0],
        neck_1.nodes["Set Shade Smooth"].inputs[0]
    )
    # float_curve.Value -> math_006.Value
    neck_1.links.new(
        neck_1.nodes["Float Curve"].outputs[0],
        neck_1.nodes["Math.006"].inputs[0]
    )
    # spline_parameter_002.Factor -> float_curve_004.Value
    neck_1.links.new(
        neck_1.nodes["Spline Parameter.002"].outputs[0],
        neck_1.nodes["Float Curve.004"].inputs[1]
    )
    # float_curve_004.Value -> math_006.Value
    neck_1.links.new(
        neck_1.nodes["Float Curve.004"].outputs[0],
        neck_1.nodes["Math.006"].inputs[1]
    )
    # cylinder_002.Mesh -> set_position_004.Geometry
    neck_1.links.new(
        neck_1.nodes["Cylinder.002"].outputs[0],
        neck_1.nodes["Set Position.004"].inputs[0]
    )
    # position_006.Position -> separate_xyz_006.Vector
    neck_1.links.new(
        neck_1.nodes["Position.006"].outputs[0],
        neck_1.nodes["Separate XYZ.006"].inputs[0]
    )
    # separate_xyz_006.X -> math_007.Value
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.006"].outputs[0],
        neck_1.nodes["Math.007"].inputs[0]
    )
    # math_008.Value -> combine_xyz_003.Y
    neck_1.links.new(
        neck_1.nodes["Math.008"].outputs[0],
        neck_1.nodes["Combine XYZ.003"].inputs[1]
    )
    # combine_xyz_003.Vector -> set_position_004.Offset
    neck_1.links.new(
        neck_1.nodes["Combine XYZ.003"].outputs[0],
        neck_1.nodes["Set Position.004"].inputs[3]
    )
    # separate_xyz_006.Y -> map_range_003.Value
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.006"].outputs[1],
        neck_1.nodes["Map Range.003"].inputs[0]
    )
    # math_007.Value -> math_008.Value
    neck_1.links.new(
        neck_1.nodes["Math.007"].outputs[0],
        neck_1.nodes["Math.008"].inputs[0]
    )
    # map_range_003.Result -> math_008.Value
    neck_1.links.new(
        neck_1.nodes["Map Range.003"].outputs[0],
        neck_1.nodes["Math.008"].inputs[1]
    )
    # cylinder_002.Top -> boolean_math_004.Boolean
    neck_1.links.new(
        neck_1.nodes["Cylinder.002"].outputs[1],
        neck_1.nodes["Boolean Math.004"].inputs[0]
    )
    # cylinder_002.Side -> boolean_math_004.Boolean
    neck_1.links.new(
        neck_1.nodes["Cylinder.002"].outputs[2],
        neck_1.nodes["Boolean Math.004"].inputs[1]
    )
    # set_position_004.Geometry -> mesh_to_curve_001.Mesh
    neck_1.links.new(
        neck_1.nodes["Set Position.004"].outputs[0],
        neck_1.nodes["Mesh to Curve.001"].inputs[0]
    )
    # boolean_math_004.Boolean -> mesh_to_curve_001.Selection
    neck_1.links.new(
        neck_1.nodes["Boolean Math.004"].outputs[0],
        neck_1.nodes["Mesh to Curve.001"].inputs[1]
    )
    # mesh_to_curve_001.Curve -> instance_on_points_004.Points
    neck_1.links.new(
        neck_1.nodes["Mesh to Curve.001"].outputs[0],
        neck_1.nodes["Instance on Points.004"].inputs[0]
    )
    # ico_sphere_004.Mesh -> instance_on_points_004.Instance
    neck_1.links.new(
        neck_1.nodes["Ico Sphere.004"].outputs[0],
        neck_1.nodes["Instance on Points.004"].inputs[2]
    )
    # ico_sphere_005.Mesh -> dual_mesh.Mesh
    neck_1.links.new(
        neck_1.nodes["Ico Sphere.005"].outputs[0],
        neck_1.nodes["Dual Mesh"].inputs[0]
    )
    # dual_mesh.Dual Mesh -> transform_geometry_015.Geometry
    neck_1.links.new(
        neck_1.nodes["Dual Mesh"].outputs[0],
        neck_1.nodes["Transform Geometry.015"].inputs[0]
    )
    # transform_geometry_015.Geometry -> transform_geometry_016.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.015"].outputs[0],
        neck_1.nodes["Transform Geometry.016"].inputs[0]
    )
    # transform_geometry_016.Geometry -> join_geometry_007.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.016"].outputs[0],
        neck_1.nodes["Join Geometry.007"].inputs[0]
    )
    # transform_geometry_015.Geometry -> transform_geometry_017.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.015"].outputs[0],
        neck_1.nodes["Transform Geometry.017"].inputs[0]
    )
    # transform_geometry_015.Geometry -> transform_geometry_018.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.015"].outputs[0],
        neck_1.nodes["Transform Geometry.018"].inputs[0]
    )
    # transform_geometry_015.Geometry -> transform_geometry_019.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.015"].outputs[0],
        neck_1.nodes["Transform Geometry.019"].inputs[0]
    )
    # set_position_004.Geometry -> join_geometry_009.Geometry
    neck_1.links.new(
        neck_1.nodes["Set Position.004"].outputs[0],
        neck_1.nodes["Join Geometry.009"].inputs[0]
    )
    # store_named_attribute_005.Geometry -> join_geometry_010.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.005"].outputs[0],
        neck_1.nodes["Join Geometry.010"].inputs[0]
    )
    # join_geometry_023.Geometry -> store_named_attribute_006.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.023"].outputs[0],
        neck_1.nodes["Store Named Attribute.006"].inputs[0]
    )
    # set_curve_tilt_002.Curve -> sample_curve.Curves
    neck_1.links.new(
        neck_1.nodes["Set Curve Tilt.002"].outputs[0],
        neck_1.nodes["Sample Curve"].inputs[0]
    )
    # join_geometry_010.Geometry -> transform_geometry_020.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.010"].outputs[0],
        neck_1.nodes["Transform Geometry.020"].inputs[0]
    )
    # vector_math_003.Vector -> transform_geometry_020.Translation
    neck_1.links.new(
        neck_1.nodes["Vector Math.003"].outputs[0],
        neck_1.nodes["Transform Geometry.020"].inputs[2]
    )
    # transform_geometry_020.Geometry -> join_geometry_011.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.020"].outputs[0],
        neck_1.nodes["Join Geometry.011"].inputs[0]
    )
    # sample_curve.Position -> vector_math_003.Vector
    neck_1.links.new(
        neck_1.nodes["Sample Curve"].outputs[1],
        neck_1.nodes["Vector Math.003"].inputs[0]
    )
    # spline_parameter_003.Factor -> float_curve_005.Value
    neck_1.links.new(
        neck_1.nodes["Spline Parameter.003"].outputs[0],
        neck_1.nodes["Float Curve.005"].inputs[1]
    )
    # float_curve_005.Value -> math_009.Value
    neck_1.links.new(
        neck_1.nodes["Float Curve.005"].outputs[0],
        neck_1.nodes["Math.009"].inputs[0]
    )
    # math_005.Value -> math_010.Value
    neck_1.links.new(
        neck_1.nodes["Math.005"].outputs[0],
        neck_1.nodes["Math.010"].inputs[0]
    )
    # math_009.Value -> math_010.Value
    neck_1.links.new(
        neck_1.nodes["Math.009"].outputs[0],
        neck_1.nodes["Math.010"].inputs[1]
    )
    # curve_circle_004.Curve -> set_position_005.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve Circle.004"].outputs[0],
        neck_1.nodes["Set Position.005"].inputs[0]
    )
    # position_007.Position -> separate_xyz_007.Vector
    neck_1.links.new(
        neck_1.nodes["Position.007"].outputs[0],
        neck_1.nodes["Separate XYZ.007"].inputs[0]
    )
    # separate_xyz_007.Y -> map_range_004.Value
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.007"].outputs[1],
        neck_1.nodes["Map Range.004"].inputs[0]
    )
    # map_range_004.Result -> float_curve_006.Value
    neck_1.links.new(
        neck_1.nodes["Map Range.004"].outputs[0],
        neck_1.nodes["Float Curve.006"].inputs[1]
    )
    # math_015.Value -> math_011.Value
    neck_1.links.new(
        neck_1.nodes["Math.015"].outputs[0],
        neck_1.nodes["Math.011"].inputs[0]
    )
    # combine_xyz_004.Vector -> set_position_005.Offset
    neck_1.links.new(
        neck_1.nodes["Combine XYZ.004"].outputs[0],
        neck_1.nodes["Set Position.005"].inputs[3]
    )
    # math_011.Value -> combine_xyz_004.Z
    neck_1.links.new(
        neck_1.nodes["Math.011"].outputs[0],
        neck_1.nodes["Combine XYZ.004"].inputs[2]
    )
    # set_position_005.Geometry -> transform_geometry_021.Geometry
    neck_1.links.new(
        neck_1.nodes["Set Position.005"].outputs[0],
        neck_1.nodes["Transform Geometry.021"].inputs[0]
    )
    # position_008.Position -> vector_math_004.Vector
    neck_1.links.new(
        neck_1.nodes["Position.008"].outputs[0],
        neck_1.nodes["Vector Math.004"].inputs[0]
    )
    # vector_math_004.Vector -> set_position_005.Position
    neck_1.links.new(
        neck_1.nodes["Vector Math.004"].outputs[0],
        neck_1.nodes["Set Position.005"].inputs[2]
    )
    # combine_xyz_005.Vector -> vector_math_004.Vector
    neck_1.links.new(
        neck_1.nodes["Combine XYZ.005"].outputs[0],
        neck_1.nodes["Vector Math.004"].inputs[1]
    )
    # map_range_004.Result -> float_curve_007.Value
    neck_1.links.new(
        neck_1.nodes["Map Range.004"].outputs[0],
        neck_1.nodes["Float Curve.007"].inputs[1]
    )
    # float_curve_007.Value -> combine_xyz_005.X
    neck_1.links.new(
        neck_1.nodes["Float Curve.007"].outputs[0],
        neck_1.nodes["Combine XYZ.005"].inputs[0]
    )
    # transform_geometry_021.Geometry -> resample_curve_004.Curve
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.021"].outputs[0],
        neck_1.nodes["Resample Curve.004"].inputs[0]
    )
    # set_curve_tilt_003.Curve -> instance_on_points_005.Points
    neck_1.links.new(
        neck_1.nodes["Set Curve Tilt.003"].outputs[0],
        neck_1.nodes["Instance on Points.005"].inputs[0]
    )
    # curve_tangent_002.Tangent -> align_rotation_to_vector_002.Vector
    neck_1.links.new(
        neck_1.nodes["Curve Tangent.002"].outputs[0],
        neck_1.nodes["Align Rotation to Vector.002"].inputs[2]
    )
    # align_rotation_to_vector_002.Rotation -> align_rotation_to_vector_003.Rotation
    neck_1.links.new(
        neck_1.nodes["Align Rotation to Vector.002"].outputs[0],
        neck_1.nodes["Align Rotation to Vector.003"].inputs[0]
    )
    # normal_002.Normal -> align_rotation_to_vector_003.Vector
    neck_1.links.new(
        neck_1.nodes["Normal.002"].outputs[0],
        neck_1.nodes["Align Rotation to Vector.003"].inputs[2]
    )
    # spline_parameter_004.Factor -> math_012.Value
    neck_1.links.new(
        neck_1.nodes["Spline Parameter.004"].outputs[0],
        neck_1.nodes["Math.012"].inputs[0]
    )
    # math_012.Value -> math_013.Value
    neck_1.links.new(
        neck_1.nodes["Math.012"].outputs[0],
        neck_1.nodes["Math.013"].inputs[0]
    )
    # resample_curve_004.Curve -> set_curve_tilt_003.Curve
    neck_1.links.new(
        neck_1.nodes["Resample Curve.004"].outputs[0],
        neck_1.nodes["Set Curve Tilt.003"].inputs[0]
    )
    # math_013.Value -> map_range_005.Value
    neck_1.links.new(
        neck_1.nodes["Math.013"].outputs[0],
        neck_1.nodes["Map Range.005"].inputs[0]
    )
    # map_range_005.Result -> set_curve_tilt_003.Tilt
    neck_1.links.new(
        neck_1.nodes["Map Range.005"].outputs[0],
        neck_1.nodes["Set Curve Tilt.003"].inputs[2]
    )
    # spline_parameter_005.Factor -> float_curve_008.Value
    neck_1.links.new(
        neck_1.nodes["Spline Parameter.005"].outputs[0],
        neck_1.nodes["Float Curve.008"].inputs[1]
    )
    # float_curve_008.Value -> math_014.Value
    neck_1.links.new(
        neck_1.nodes["Float Curve.008"].outputs[0],
        neck_1.nodes["Math.014"].inputs[0]
    )
    # math_019.Value -> combine_xyz_004.Y
    neck_1.links.new(
        neck_1.nodes["Math.019"].outputs[0],
        neck_1.nodes["Combine XYZ.004"].inputs[1]
    )
    # float_curve_006.Value -> math_015.Value
    neck_1.links.new(
        neck_1.nodes["Float Curve.006"].outputs[0],
        neck_1.nodes["Math.015"].inputs[0]
    )
    # spline_parameter_006.Factor -> float_curve_009.Value
    neck_1.links.new(
        neck_1.nodes["Spline Parameter.006"].outputs[0],
        neck_1.nodes["Float Curve.009"].inputs[1]
    )
    # float_curve_009.Value -> math_015.Value
    neck_1.links.new(
        neck_1.nodes["Float Curve.009"].outputs[0],
        neck_1.nodes["Math.015"].inputs[1]
    )
    # spline_parameter_007.Factor -> float_curve_010.Value
    neck_1.links.new(
        neck_1.nodes["Spline Parameter.007"].outputs[0],
        neck_1.nodes["Float Curve.010"].inputs[1]
    )
    # float_curve_010.Value -> math_018.Value
    neck_1.links.new(
        neck_1.nodes["Float Curve.010"].outputs[0],
        neck_1.nodes["Math.018"].inputs[0]
    )
    # math_014.Value -> math_019.Value
    neck_1.links.new(
        neck_1.nodes["Math.014"].outputs[0],
        neck_1.nodes["Math.019"].inputs[0]
    )
    # math_018.Value -> math_019.Value
    neck_1.links.new(
        neck_1.nodes["Math.018"].outputs[0],
        neck_1.nodes["Math.019"].inputs[1]
    )
    # set_spline_type.Curve -> fillet_curve.Curve
    neck_1.links.new(
        neck_1.nodes["Set Spline Type"].outputs[0],
        neck_1.nodes["Fillet Curve"].inputs[0]
    )
    # quadrilateral.Curve -> set_spline_type.Curve
    neck_1.links.new(
        neck_1.nodes["Quadrilateral"].outputs[0],
        neck_1.nodes["Set Spline Type"].inputs[0]
    )
    # fillet_curve.Curve -> curve_to_mesh_001.Curve
    neck_1.links.new(
        neck_1.nodes["Fillet Curve"].outputs[0],
        neck_1.nodes["Curve to Mesh.001"].inputs[0]
    )
    # curve_circle_005.Curve -> curve_to_mesh_001.Profile Curve
    neck_1.links.new(
        neck_1.nodes["Curve Circle.005"].outputs[0],
        neck_1.nodes["Curve to Mesh.001"].inputs[1]
    )
    # curve_to_mesh_001.Mesh -> instance_on_points_005.Instance
    neck_1.links.new(
        neck_1.nodes["Curve to Mesh.001"].outputs[0],
        neck_1.nodes["Instance on Points.005"].inputs[2]
    )
    # rotate_rotation_006.Rotation -> instance_on_points_005.Rotation
    neck_1.links.new(
        neck_1.nodes["Rotate Rotation.006"].outputs[0],
        neck_1.nodes["Instance on Points.005"].inputs[5]
    )
    # align_rotation_to_vector_003.Rotation -> rotate_rotation_005.Rotation
    neck_1.links.new(
        neck_1.nodes["Align Rotation to Vector.003"].outputs[0],
        neck_1.nodes["Rotate Rotation.005"].inputs[0]
    )
    # rotate_rotation_005.Rotation -> rotate_rotation_006.Rotation
    neck_1.links.new(
        neck_1.nodes["Rotate Rotation.005"].outputs[0],
        neck_1.nodes["Rotate Rotation.006"].inputs[0]
    )
    # random_value_012.Value -> rotate_rotation_006.Rotate By
    neck_1.links.new(
        neck_1.nodes["Random Value.012"].outputs[0],
        neck_1.nodes["Rotate Rotation.006"].inputs[1]
    )
    # index_001.Index -> math_016.Value
    neck_1.links.new(
        neck_1.nodes["Index.001"].outputs[0],
        neck_1.nodes["Math.016"].inputs[0]
    )
    # math_016.Value -> switch_001.Switch
    neck_1.links.new(
        neck_1.nodes["Math.016"].outputs[0],
        neck_1.nodes["Switch.001"].inputs[0]
    )
    # switch_001.Output -> combine_xyz_006.X
    neck_1.links.new(
        neck_1.nodes["Switch.001"].outputs[0],
        neck_1.nodes["Combine XYZ.006"].inputs[0]
    )
    # combine_xyz_006.Vector -> rotate_rotation_005.Rotate By
    neck_1.links.new(
        neck_1.nodes["Combine XYZ.006"].outputs[0],
        neck_1.nodes["Rotate Rotation.005"].inputs[1]
    )
    # join_geometry_011.Geometry -> join_geometry_012.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.011"].outputs[0],
        neck_1.nodes["Join Geometry.012"].inputs[0]
    )
    # join_geometry_012.Geometry -> store_named_attribute.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.012"].outputs[0],
        neck_1.nodes["Store Named Attribute"].inputs[0]
    )
    # curve_circle_006.Curve -> curve_to_mesh_002.Curve
    neck_1.links.new(
        neck_1.nodes["Curve Circle.006"].outputs[0],
        neck_1.nodes["Curve to Mesh.002"].inputs[0]
    )
    # set_curve_tilt_003.Curve -> sample_curve_001.Curves
    neck_1.links.new(
        neck_1.nodes["Set Curve Tilt.003"].outputs[0],
        neck_1.nodes["Sample Curve.001"].inputs[0]
    )
    # curve_to_mesh_002.Mesh -> transform_geometry_022.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve to Mesh.002"].outputs[0],
        neck_1.nodes["Transform Geometry.022"].inputs[0]
    )
    # vector_math_005.Vector -> transform_geometry_022.Translation
    neck_1.links.new(
        neck_1.nodes["Vector Math.005"].outputs[0],
        neck_1.nodes["Transform Geometry.022"].inputs[2]
    )
    # instance_on_points_005.Instances -> join_geometry_013.Geometry
    neck_1.links.new(
        neck_1.nodes["Instance on Points.005"].outputs[0],
        neck_1.nodes["Join Geometry.013"].inputs[0]
    )
    # sample_curve_001.Position -> vector_math_005.Vector
    neck_1.links.new(
        neck_1.nodes["Sample Curve.001"].outputs[1],
        neck_1.nodes["Vector Math.005"].inputs[0]
    )
    # curve_circle_007.Curve -> curve_to_mesh_002.Profile Curve
    neck_1.links.new(
        neck_1.nodes["Curve Circle.007"].outputs[0],
        neck_1.nodes["Curve to Mesh.002"].inputs[1]
    )
    # vector_math_006.Vector -> transform_geometry_023.Translation
    neck_1.links.new(
        neck_1.nodes["Vector Math.006"].outputs[0],
        neck_1.nodes["Transform Geometry.023"].inputs[2]
    )
    # vector_math_005.Vector -> vector_math_006.Vector
    neck_1.links.new(
        neck_1.nodes["Vector Math.005"].outputs[0],
        neck_1.nodes["Vector Math.006"].inputs[0]
    )
    # resample_curve_005.Curve -> curve_to_mesh_003.Curve
    neck_1.links.new(
        neck_1.nodes["Resample Curve.005"].outputs[0],
        neck_1.nodes["Curve to Mesh.003"].inputs[0]
    )
    # curve_line.Curve -> resample_curve_005.Curve
    neck_1.links.new(
        neck_1.nodes["Curve Line"].outputs[0],
        neck_1.nodes["Resample Curve.005"].inputs[0]
    )
    # curve_circle_008.Curve -> curve_to_mesh_003.Profile Curve
    neck_1.links.new(
        neck_1.nodes["Curve Circle.008"].outputs[0],
        neck_1.nodes["Curve to Mesh.003"].inputs[1]
    )
    # spline_parameter_008.Factor -> float_curve_011.Value
    neck_1.links.new(
        neck_1.nodes["Spline Parameter.008"].outputs[0],
        neck_1.nodes["Float Curve.011"].inputs[1]
    )
    # float_curve_011.Value -> curve_to_mesh_003.Scale
    neck_1.links.new(
        neck_1.nodes["Float Curve.011"].outputs[0],
        neck_1.nodes["Curve to Mesh.003"].inputs[2]
    )
    # curve_circle_009.Curve -> curve_to_mesh_004.Curve
    neck_1.links.new(
        neck_1.nodes["Curve Circle.009"].outputs[0],
        neck_1.nodes["Curve to Mesh.004"].inputs[0]
    )
    # curve_circle_010.Curve -> curve_to_mesh_004.Profile Curve
    neck_1.links.new(
        neck_1.nodes["Curve Circle.010"].outputs[0],
        neck_1.nodes["Curve to Mesh.004"].inputs[1]
    )
    # curve_to_mesh_003.Mesh -> join_geometry_014.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve to Mesh.003"].outputs[0],
        neck_1.nodes["Join Geometry.014"].inputs[0]
    )
    # join_geometry_014.Geometry -> transform_geometry_023.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.014"].outputs[0],
        neck_1.nodes["Transform Geometry.023"].inputs[0]
    )
    # curve_to_mesh_004.Mesh -> instance_on_points_006.Instance
    neck_1.links.new(
        neck_1.nodes["Curve to Mesh.004"].outputs[0],
        neck_1.nodes["Instance on Points.006"].inputs[2]
    )
    # curve_circle_011.Curve -> instance_on_points_006.Points
    neck_1.links.new(
        neck_1.nodes["Curve Circle.011"].outputs[0],
        neck_1.nodes["Instance on Points.006"].inputs[0]
    )
    # instance_on_points_006.Instances -> transform_geometry_024.Geometry
    neck_1.links.new(
        neck_1.nodes["Instance on Points.006"].outputs[0],
        neck_1.nodes["Transform Geometry.024"].inputs[0]
    )
    # grid.Mesh -> delete_geometry_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Grid"].outputs[0],
        neck_1.nodes["Delete Geometry.001"].inputs[0]
    )
    # random_value_013.Value -> delete_geometry_001.Selection
    neck_1.links.new(
        neck_1.nodes["Random Value.013"].outputs[3],
        neck_1.nodes["Delete Geometry.001"].inputs[1]
    )
    # delete_geometry_001.Geometry -> extrude_mesh.Mesh
    neck_1.links.new(
        neck_1.nodes["Delete Geometry.001"].outputs[0],
        neck_1.nodes["Extrude Mesh"].inputs[0]
    )
    # delete_geometry_001.Geometry -> flip_faces.Mesh
    neck_1.links.new(
        neck_1.nodes["Delete Geometry.001"].outputs[0],
        neck_1.nodes["Flip Faces"].inputs[0]
    )
    # extrude_mesh.Mesh -> join_geometry_015.Geometry
    neck_1.links.new(
        neck_1.nodes["Extrude Mesh"].outputs[0],
        neck_1.nodes["Join Geometry.015"].inputs[0]
    )
    # join_geometry_015.Geometry -> merge_by_distance.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.015"].outputs[0],
        neck_1.nodes["Merge by Distance"].inputs[0]
    )
    # subdivision_surface.Mesh -> transform_geometry_025.Geometry
    neck_1.links.new(
        neck_1.nodes["Subdivision Surface"].outputs[0],
        neck_1.nodes["Transform Geometry.025"].inputs[0]
    )
    # merge_by_distance.Geometry -> subdivision_surface.Mesh
    neck_1.links.new(
        neck_1.nodes["Merge by Distance"].outputs[0],
        neck_1.nodes["Subdivision Surface"].inputs[0]
    )
    # join_geometry_013.Geometry -> set_shade_smooth_001.Mesh
    neck_1.links.new(
        neck_1.nodes["Join Geometry.013"].outputs[0],
        neck_1.nodes["Set Shade Smooth.001"].inputs[0]
    )
    # set_shade_smooth_001.Mesh -> store_named_attribute_007.Geometry
    neck_1.links.new(
        neck_1.nodes["Set Shade Smooth.001"].outputs[0],
        neck_1.nodes["Store Named Attribute.007"].inputs[0]
    )
    # ico_sphere_006.Mesh -> transform_geometry_026.Geometry
    neck_1.links.new(
        neck_1.nodes["Ico Sphere.006"].outputs[0],
        neck_1.nodes["Transform Geometry.026"].inputs[0]
    )
    # transform_geometry_026.Geometry -> instance_on_points_007.Instance
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.026"].outputs[0],
        neck_1.nodes["Instance on Points.007"].inputs[2]
    )
    # quadratic_b_zier.Curve -> instance_on_points_007.Points
    neck_1.links.new(
        neck_1.nodes["Quadratic Bézier"].outputs[0],
        neck_1.nodes["Instance on Points.007"].inputs[0]
    )
    # instance_on_points_007.Instances -> realize_instances_003.Geometry
    neck_1.links.new(
        neck_1.nodes["Instance on Points.007"].outputs[0],
        neck_1.nodes["Realize Instances.003"].inputs[0]
    )
    # realize_instances_003.Geometry -> mesh_to_sdf_grid.Mesh
    neck_1.links.new(
        neck_1.nodes["Realize Instances.003"].outputs[0],
        neck_1.nodes["Mesh to SDF Grid"].inputs[0]
    )
    # sdf_grid_boolean.Grid -> grid_to_mesh.Grid
    neck_1.links.new(
        neck_1.nodes["SDF Grid Boolean"].outputs[0],
        neck_1.nodes["Grid to Mesh"].inputs[0]
    )
    # triangulate.Mesh -> dual_mesh_001.Mesh
    neck_1.links.new(
        neck_1.nodes["Triangulate"].outputs[0],
        neck_1.nodes["Dual Mesh.001"].inputs[0]
    )
    # grid_to_mesh.Mesh -> triangulate.Mesh
    neck_1.links.new(
        neck_1.nodes["Grid to Mesh"].outputs[0],
        neck_1.nodes["Triangulate"].inputs[0]
    )
    # cube.Mesh -> transform_geometry_027.Geometry
    neck_1.links.new(
        neck_1.nodes["Cube"].outputs[0],
        neck_1.nodes["Transform Geometry.027"].inputs[0]
    )
    # transform_geometry_027.Geometry -> mesh_to_sdf_grid_001.Mesh
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.027"].outputs[0],
        neck_1.nodes["Mesh to SDF Grid.001"].inputs[0]
    )
    # mesh_to_sdf_grid_001.SDF Grid -> sdf_grid_boolean.Grid
    neck_1.links.new(
        neck_1.nodes["Mesh to SDF Grid.001"].outputs[0],
        neck_1.nodes["SDF Grid Boolean"].inputs[1]
    )
    # dual_mesh_001.Dual Mesh -> mesh_boolean.Mesh 1
    neck_1.links.new(
        neck_1.nodes["Dual Mesh.001"].outputs[0],
        neck_1.nodes["Mesh Boolean"].inputs[0]
    )
    # cube_001.Mesh -> transform_geometry_028.Geometry
    neck_1.links.new(
        neck_1.nodes["Cube.001"].outputs[0],
        neck_1.nodes["Transform Geometry.028"].inputs[0]
    )
    # transform_geometry_028.Geometry -> mesh_boolean.Mesh 2
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.028"].outputs[0],
        neck_1.nodes["Mesh Boolean"].inputs[1]
    )
    # mesh_boolean.Mesh -> delete_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Mesh Boolean"].outputs[0],
        neck_1.nodes["Delete Geometry.002"].inputs[0]
    )
    # mesh_boolean.Intersecting Edges -> delete_geometry_002.Selection
    neck_1.links.new(
        neck_1.nodes["Mesh Boolean"].outputs[1],
        neck_1.nodes["Delete Geometry.002"].inputs[1]
    )
    # cube_002.Mesh -> transform_geometry_029.Geometry
    neck_1.links.new(
        neck_1.nodes["Cube.002"].outputs[0],
        neck_1.nodes["Transform Geometry.029"].inputs[0]
    )
    # dual_mesh_001.Dual Mesh -> mesh_boolean_001.Mesh
    neck_1.links.new(
        neck_1.nodes["Dual Mesh.001"].outputs[0],
        neck_1.nodes["Mesh Boolean.001"].inputs[1]
    )
    # curve_to_mesh_005.Mesh -> join_geometry_016.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve to Mesh.005"].outputs[0],
        neck_1.nodes["Join Geometry.016"].inputs[0]
    )
    # mesh_boolean_001.Mesh -> delete_geometry_003.Geometry
    neck_1.links.new(
        neck_1.nodes["Mesh Boolean.001"].outputs[0],
        neck_1.nodes["Delete Geometry.003"].inputs[0]
    )
    # normal_003.Normal -> compare_008.A
    neck_1.links.new(
        neck_1.nodes["Normal.003"].outputs[0],
        neck_1.nodes["Compare.008"].inputs[4]
    )
    # compare_008.Result -> delete_geometry_003.Selection
    neck_1.links.new(
        neck_1.nodes["Compare.008"].outputs[0],
        neck_1.nodes["Delete Geometry.003"].inputs[1]
    )
    # delete_geometry_003.Geometry -> mesh_to_curve_003.Mesh
    neck_1.links.new(
        neck_1.nodes["Delete Geometry.003"].outputs[0],
        neck_1.nodes["Mesh to Curve.003"].inputs[0]
    )
    # set_spline_cyclic_002.Curve -> resample_curve_006.Curve
    neck_1.links.new(
        neck_1.nodes["Set Spline Cyclic.002"].outputs[0],
        neck_1.nodes["Resample Curve.006"].inputs[0]
    )
    # resample_curve_006.Curve -> curve_to_mesh_005.Curve
    neck_1.links.new(
        neck_1.nodes["Resample Curve.006"].outputs[0],
        neck_1.nodes["Curve to Mesh.005"].inputs[0]
    )
    # gem_in_holder_003.Profile Curve -> curve_to_mesh_005.Profile Curve
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.003"].outputs[1],
        neck_1.nodes["Curve to Mesh.005"].inputs[1]
    )
    # mesh_to_curve_003.Curve -> trim_curve_005.Curve
    neck_1.links.new(
        neck_1.nodes["Mesh to Curve.003"].outputs[0],
        neck_1.nodes["Trim Curve.005"].inputs[0]
    )
    # resample_curve_007.Curve -> instance_on_points_008.Points
    neck_1.links.new(
        neck_1.nodes["Resample Curve.007"].outputs[0],
        neck_1.nodes["Instance on Points.008"].inputs[0]
    )
    # align_rotation_to_vector_004.Rotation -> instance_on_points_008.Rotation
    neck_1.links.new(
        neck_1.nodes["Align Rotation to Vector.004"].outputs[0],
        neck_1.nodes["Instance on Points.008"].inputs[5]
    )
    # curve_tangent_003.Tangent -> align_rotation_to_vector_004.Vector
    neck_1.links.new(
        neck_1.nodes["Curve Tangent.003"].outputs[0],
        neck_1.nodes["Align Rotation to Vector.004"].inputs[2]
    )
    # instance_on_points_008.Instances -> realize_instances_004.Geometry
    neck_1.links.new(
        neck_1.nodes["Instance on Points.008"].outputs[0],
        neck_1.nodes["Realize Instances.004"].inputs[0]
    )
    # delete_geometry_002.Geometry -> transform_geometry_030.Geometry
    neck_1.links.new(
        neck_1.nodes["Delete Geometry.002"].outputs[0],
        neck_1.nodes["Transform Geometry.030"].inputs[0]
    )
    # transform_geometry_030.Geometry -> flip_faces_002.Mesh
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.030"].outputs[0],
        neck_1.nodes["Flip Faces.002"].inputs[0]
    )
    # flip_faces_002.Mesh -> join_geometry_018.Geometry
    neck_1.links.new(
        neck_1.nodes["Flip Faces.002"].outputs[0],
        neck_1.nodes["Join Geometry.018"].inputs[0]
    )
    # join_geometry_018.Geometry -> merge_by_distance_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.018"].outputs[0],
        neck_1.nodes["Merge by Distance.001"].inputs[0]
    )
    # is_edge_boundary_001.Is Edge Boundary -> merge_by_distance_001.Selection
    neck_1.links.new(
        neck_1.nodes["Is Edge Boundary.001"].outputs[0],
        neck_1.nodes["Merge by Distance.001"].inputs[1]
    )
    # spline_parameter_009.Factor -> math_020.Value
    neck_1.links.new(
        neck_1.nodes["Spline Parameter.009"].outputs[0],
        neck_1.nodes["Math.020"].inputs[0]
    )
    # math_020.Value -> math_021.Value
    neck_1.links.new(
        neck_1.nodes["Math.020"].outputs[0],
        neck_1.nodes["Math.021"].inputs[0]
    )
    # trim_curve_005.Curve -> curve_to_points_002.Curve
    neck_1.links.new(
        neck_1.nodes["Trim Curve.005"].outputs[0],
        neck_1.nodes["Curve to Points.002"].inputs[0]
    )
    # curve_to_points_002.Points -> points_to_curves.Points
    neck_1.links.new(
        neck_1.nodes["Curve to Points.002"].outputs[0],
        neck_1.nodes["Points to Curves"].inputs[0]
    )
    # math_023.Value -> points_to_curves.Weight
    neck_1.links.new(
        neck_1.nodes["Math.023"].outputs[0],
        neck_1.nodes["Points to Curves"].inputs[2]
    )
    # gradient_texture.Factor -> math_022.Value
    neck_1.links.new(
        neck_1.nodes["Gradient Texture"].outputs[1],
        neck_1.nodes["Math.022"].inputs[0]
    )
    # math_022.Value -> math_023.Value
    neck_1.links.new(
        neck_1.nodes["Math.022"].outputs[0],
        neck_1.nodes["Math.023"].inputs[0]
    )
    # points_to_curves.Curves -> set_spline_cyclic_002.Curve
    neck_1.links.new(
        neck_1.nodes["Points to Curves"].outputs[0],
        neck_1.nodes["Set Spline Cyclic.002"].inputs[0]
    )
    # delete_geometry_004.Geometry -> resample_curve_007.Curve
    neck_1.links.new(
        neck_1.nodes["Delete Geometry.004"].outputs[0],
        neck_1.nodes["Resample Curve.007"].inputs[0]
    )
    # points_to_curves.Curves -> delete_geometry_004.Geometry
    neck_1.links.new(
        neck_1.nodes["Points to Curves"].outputs[0],
        neck_1.nodes["Delete Geometry.004"].inputs[0]
    )
    # position_009.Position -> separate_xyz_008.Vector
    neck_1.links.new(
        neck_1.nodes["Position.009"].outputs[0],
        neck_1.nodes["Separate XYZ.008"].inputs[0]
    )
    # separate_xyz_008.X -> compare_009.A
    neck_1.links.new(
        neck_1.nodes["Separate XYZ.008"].outputs[0],
        neck_1.nodes["Compare.009"].inputs[0]
    )
    # compare_009.Result -> delete_geometry_004.Selection
    neck_1.links.new(
        neck_1.nodes["Compare.009"].outputs[0],
        neck_1.nodes["Delete Geometry.004"].inputs[1]
    )
    # math_021.Value -> float_curve_012.Value
    neck_1.links.new(
        neck_1.nodes["Math.021"].outputs[0],
        neck_1.nodes["Float Curve.012"].inputs[1]
    )
    # float_curve_012.Value -> instance_on_points_008.Scale
    neck_1.links.new(
        neck_1.nodes["Float Curve.012"].outputs[0],
        neck_1.nodes["Instance on Points.008"].inputs[6]
    )
    # realize_instances_004.Geometry -> transform_geometry_031.Geometry
    neck_1.links.new(
        neck_1.nodes["Realize Instances.004"].outputs[0],
        neck_1.nodes["Transform Geometry.031"].inputs[0]
    )
    # transform_geometry_031.Geometry -> flip_faces_003.Mesh
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.031"].outputs[0],
        neck_1.nodes["Flip Faces.003"].inputs[0]
    )
    # realize_instances_004.Geometry -> join_geometry_019.Geometry
    neck_1.links.new(
        neck_1.nodes["Realize Instances.004"].outputs[0],
        neck_1.nodes["Join Geometry.019"].inputs[0]
    )
    # join_geometry_020.Geometry -> instance_on_points_008.Instance
    neck_1.links.new(
        neck_1.nodes["Join Geometry.020"].outputs[0],
        neck_1.nodes["Instance on Points.008"].inputs[2]
    )
    # gem_in_holder_005.Wing -> transform_geometry_032.Geometry
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.005"].outputs[3],
        neck_1.nodes["Transform Geometry.032"].inputs[0]
    )
    # transform_geometry_032.Geometry -> flip_faces_001.Mesh
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.032"].outputs[0],
        neck_1.nodes["Flip Faces.001"].inputs[0]
    )
    # flip_faces_001.Mesh -> join_geometry_021.Geometry
    neck_1.links.new(
        neck_1.nodes["Flip Faces.001"].outputs[0],
        neck_1.nodes["Join Geometry.021"].inputs[0]
    )
    # gem_in_holder_006.Wing -> transform_geometry_033.Geometry
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.006"].outputs[3],
        neck_1.nodes["Transform Geometry.033"].inputs[0]
    )
    # transform_geometry_033.Geometry -> flip_faces_004.Mesh
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.033"].outputs[0],
        neck_1.nodes["Flip Faces.004"].inputs[0]
    )
    # flip_faces_004.Mesh -> join_geometry_022.Geometry
    neck_1.links.new(
        neck_1.nodes["Flip Faces.004"].outputs[0],
        neck_1.nodes["Join Geometry.022"].inputs[0]
    )
    # transform_geometry_034.Geometry -> join_geometry_020.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.034"].outputs[0],
        neck_1.nodes["Join Geometry.020"].inputs[0]
    )
    # join_geometry_022.Geometry -> transform_geometry_034.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.022"].outputs[0],
        neck_1.nodes["Transform Geometry.034"].inputs[0]
    )
    # join_geometry_016.Geometry -> store_named_attribute_008.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.016"].outputs[0],
        neck_1.nodes["Store Named Attribute.008"].inputs[0]
    )
    # merge_by_distance_001.Geometry -> store_named_attribute_009.Geometry
    neck_1.links.new(
        neck_1.nodes["Merge by Distance.001"].outputs[0],
        neck_1.nodes["Store Named Attribute.009"].inputs[0]
    )
    # store_named_attribute_009.Geometry -> join_geometry_017.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.009"].outputs[0],
        neck_1.nodes["Join Geometry.017"].inputs[0]
    )
    # gem_in_holder_007.Geometry -> instance_on_points_009.Instance
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.007"].outputs[0],
        neck_1.nodes["Instance on Points.009"].inputs[2]
    )
    # transform_geometry_035.Geometry -> instance_on_points_009.Points
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.035"].outputs[0],
        neck_1.nodes["Instance on Points.009"].inputs[0]
    )
    # curve_circle_012.Curve -> transform_geometry_035.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve Circle.012"].outputs[0],
        neck_1.nodes["Transform Geometry.035"].inputs[0]
    )
    # join_geometry_017.Geometry -> transform_geometry_036.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.017"].outputs[0],
        neck_1.nodes["Transform Geometry.036"].inputs[0]
    )
    # gem_in_holder_008.Geometry -> instance_on_points_010.Instance
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.008"].outputs[0],
        neck_1.nodes["Instance on Points.010"].inputs[2]
    )
    # capture_attribute_002.Geometry -> realize_instances_005.Geometry
    neck_1.links.new(
        neck_1.nodes["Capture Attribute.002"].outputs[0],
        neck_1.nodes["Realize Instances.005"].inputs[0]
    )
    # instance_on_points_010.Instances -> capture_attribute_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Instance on Points.010"].outputs[0],
        neck_1.nodes["Capture Attribute.002"].inputs[0]
    )
    # index_002.Index -> capture_attribute_002.Index
    neck_1.links.new(
        neck_1.nodes["Index.002"].outputs[0],
        neck_1.nodes["Capture Attribute.002"].inputs[1]
    )
    # trim_curve_006.Curve -> resample_curve_008.Curve
    neck_1.links.new(
        neck_1.nodes["Trim Curve.006"].outputs[0],
        neck_1.nodes["Resample Curve.008"].inputs[0]
    )
    # resample_curve_008.Curve -> instance_on_points_010.Points
    neck_1.links.new(
        neck_1.nodes["Resample Curve.008"].outputs[0],
        neck_1.nodes["Instance on Points.010"].inputs[0]
    )
    # align_rotation_to_vector_006.Rotation -> instance_on_points_010.Rotation
    neck_1.links.new(
        neck_1.nodes["Align Rotation to Vector.006"].outputs[0],
        neck_1.nodes["Instance on Points.010"].inputs[5]
    )
    # align_rotation_to_vector_005.Rotation -> align_rotation_to_vector_006.Rotation
    neck_1.links.new(
        neck_1.nodes["Align Rotation to Vector.005"].outputs[0],
        neck_1.nodes["Align Rotation to Vector.006"].inputs[0]
    )
    # normal_004.Normal -> align_rotation_to_vector_006.Vector
    neck_1.links.new(
        neck_1.nodes["Normal.004"].outputs[0],
        neck_1.nodes["Align Rotation to Vector.006"].inputs[2]
    )
    # curve_tangent_004.Tangent -> align_rotation_to_vector_005.Vector
    neck_1.links.new(
        neck_1.nodes["Curve Tangent.004"].outputs[0],
        neck_1.nodes["Align Rotation to Vector.005"].inputs[2]
    )
    # set_curve_tilt.Curve -> trim_curve_006.Curve
    neck_1.links.new(
        neck_1.nodes["Set Curve Tilt"].outputs[0],
        neck_1.nodes["Trim Curve.006"].inputs[0]
    )
    # trim_curve_007.Curve -> curve_to_points_003.Curve
    neck_1.links.new(
        neck_1.nodes["Trim Curve.007"].outputs[0],
        neck_1.nodes["Curve to Points.003"].inputs[0]
    )
    # curve_to_points_003.Points -> for_each_geometry_element_input_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Curve to Points.003"].outputs[0],
        neck_1.nodes["For Each Geometry Element Input.002"].inputs[0]
    )
    # curve_to_points_003.Rotation -> for_each_geometry_element_input_002.Rotation
    neck_1.links.new(
        neck_1.nodes["Curve to Points.003"].outputs[3],
        neck_1.nodes["For Each Geometry Element Input.002"].inputs[2]
    )
    # position_010.Position -> for_each_geometry_element_input_002.Position
    neck_1.links.new(
        neck_1.nodes["Position.010"].outputs[0],
        neck_1.nodes["For Each Geometry Element Input.002"].inputs[3]
    )
    # gem_in_holder_009.Geometry -> transform_geometry_037.Geometry
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.009"].outputs[0],
        neck_1.nodes["Transform Geometry.037"].inputs[0]
    )
    # for_each_geometry_element_input_002.Position -> transform_geometry_037.Translation
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.002"].outputs[3],
        neck_1.nodes["Transform Geometry.037"].inputs[2]
    )
    # rotate_rotation_008.Rotation -> transform_geometry_037.Rotation
    neck_1.links.new(
        neck_1.nodes["Rotate Rotation.008"].outputs[0],
        neck_1.nodes["Transform Geometry.037"].inputs[3]
    )
    # for_each_geometry_element_input_002.Rotation -> rotate_rotation_007.Rotation
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.002"].outputs[2],
        neck_1.nodes["Rotate Rotation.007"].inputs[0]
    )
    # for_each_geometry_element_input_002.Index -> random_value_014.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.002"].outputs[0],
        neck_1.nodes["Random Value.014"].inputs[7]
    )
    # transform_geometry_037.Geometry -> transform_geometry_038.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.037"].outputs[0],
        neck_1.nodes["Transform Geometry.038"].inputs[0]
    )
    # for_each_geometry_element_input_002.Index -> random_value_015.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.002"].outputs[0],
        neck_1.nodes["Random Value.015"].inputs[7]
    )
    # random_value_015.Value -> transform_geometry_037.Scale
    neck_1.links.new(
        neck_1.nodes["Random Value.015"].outputs[1],
        neck_1.nodes["Transform Geometry.037"].inputs[4]
    )
    # store_named_attribute_010.Geometry -> for_each_geometry_element_output_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.010"].outputs[0],
        neck_1.nodes["For Each Geometry Element Output.002"].inputs[1]
    )
    # transform_geometry_038.Geometry -> store_named_attribute_010.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.038"].outputs[0],
        neck_1.nodes["Store Named Attribute.010"].inputs[0]
    )
    # random_value_014.Value -> gem_in_holder_009.Array Count
    neck_1.links.new(
        neck_1.nodes["Random Value.014"].outputs[2],
        neck_1.nodes["Gem in Holder.009"].inputs[7]
    )
    # for_each_geometry_element_input_002.Index -> random_value_016.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.002"].outputs[0],
        neck_1.nodes["Random Value.016"].inputs[7]
    )
    # random_value_016.Value -> gem_in_holder_009.Seed
    neck_1.links.new(
        neck_1.nodes["Random Value.016"].outputs[1],
        neck_1.nodes["Gem in Holder.009"].inputs[10]
    )
    # rotate_rotation_007.Rotation -> rotate_rotation_008.Rotation
    neck_1.links.new(
        neck_1.nodes["Rotate Rotation.007"].outputs[0],
        neck_1.nodes["Rotate Rotation.008"].inputs[0]
    )
    # for_each_geometry_element_input_002.Index -> random_value_017.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.002"].outputs[0],
        neck_1.nodes["Random Value.017"].inputs[7]
    )
    # random_value_017.Value -> gem_in_holder_009.Split
    neck_1.links.new(
        neck_1.nodes["Random Value.017"].outputs[1],
        neck_1.nodes["Gem in Holder.009"].inputs[9]
    )
    # for_each_geometry_element_input_002.Index -> random_value_018.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.002"].outputs[0],
        neck_1.nodes["Random Value.018"].inputs[7]
    )
    # random_value_018.Value -> gem_in_holder_009.Seed
    neck_1.links.new(
        neck_1.nodes["Random Value.018"].outputs[2],
        neck_1.nodes["Gem in Holder.009"].inputs[5]
    )
    # for_each_geometry_element_input_002.Index -> random_value_019.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.002"].outputs[0],
        neck_1.nodes["Random Value.019"].inputs[7]
    )
    # random_value_019.Value -> gem_in_holder_009.Count
    neck_1.links.new(
        neck_1.nodes["Random Value.019"].outputs[2],
        neck_1.nodes["Gem in Holder.009"].inputs[4]
    )
    # for_each_geometry_element_input_002.Index -> random_value_020.ID
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Input.002"].outputs[0],
        neck_1.nodes["Random Value.020"].inputs[7]
    )
    # random_value_020.Value -> gem_in_holder_009.Strand Count
    neck_1.links.new(
        neck_1.nodes["Random Value.020"].outputs[2],
        neck_1.nodes["Gem in Holder.009"].inputs[8]
    )
    # separate_geometry_002.Selection -> trim_curve_007.Curve
    neck_1.links.new(
        neck_1.nodes["Separate Geometry.002"].outputs[0],
        neck_1.nodes["Trim Curve.007"].inputs[0]
    )
    # transform_geometry_036.Geometry -> store_named_attribute_011.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.036"].outputs[0],
        neck_1.nodes["Store Named Attribute.011"].inputs[0]
    )
    # for_each_geometry_element_output_002.Geometry -> store_named_attribute_012.Geometry
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Output.002"].outputs[2],
        neck_1.nodes["Store Named Attribute.012"].inputs[0]
    )
    # transform_geometry_039.Geometry -> mesh_boolean_002.Mesh 2
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.039"].outputs[0],
        neck_1.nodes["Mesh Boolean.002"].inputs[1]
    )
    # ico_sphere_007.Mesh -> transform_geometry_039.Geometry
    neck_1.links.new(
        neck_1.nodes["Ico Sphere.007"].outputs[0],
        neck_1.nodes["Transform Geometry.039"].inputs[0]
    )
    # group_009.Geometry -> mesh_boolean_002.Mesh 1
    neck_1.links.new(
        neck_1.nodes["Group.009"].outputs[0],
        neck_1.nodes["Mesh Boolean.002"].inputs[0]
    )
    # boolean_math_005.Boolean -> store_named_attribute_013.Selection
    neck_1.links.new(
        neck_1.nodes["Boolean Math.005"].outputs[0],
        neck_1.nodes["Store Named Attribute.013"].inputs[1]
    )
    # named_attribute.Attribute -> boolean_math_005.Boolean
    neck_1.links.new(
        neck_1.nodes["Named Attribute"].outputs[0],
        neck_1.nodes["Boolean Math.005"].inputs[1]
    )
    # math_017.Value -> boolean_math_005.Boolean
    neck_1.links.new(
        neck_1.nodes["Math.017"].outputs[0],
        neck_1.nodes["Boolean Math.005"].inputs[0]
    )
    # store_named_attribute_013.Geometry -> store_named_attribute_014.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.013"].outputs[0],
        neck_1.nodes["Store Named Attribute.014"].inputs[0]
    )
    # boolean_math_005.Boolean -> store_named_attribute_014.Selection
    neck_1.links.new(
        neck_1.nodes["Boolean Math.005"].outputs[0],
        neck_1.nodes["Store Named Attribute.014"].inputs[1]
    )
    # realize_instances_005.Geometry -> store_named_attribute_013.Geometry
    neck_1.links.new(
        neck_1.nodes["Realize Instances.005"].outputs[0],
        neck_1.nodes["Store Named Attribute.013"].inputs[0]
    )
    # capture_attribute_002.Index -> math_017.Value
    neck_1.links.new(
        neck_1.nodes["Capture Attribute.002"].outputs[1],
        neck_1.nodes["Math.017"].inputs[0]
    )
    # set_position_004.Geometry -> transform_geometry_040.Geometry
    neck_1.links.new(
        neck_1.nodes["Set Position.004"].outputs[0],
        neck_1.nodes["Transform Geometry.040"].inputs[0]
    )
    # transform_geometry_040.Geometry -> transform_geometry_041.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.040"].outputs[0],
        neck_1.nodes["Transform Geometry.041"].inputs[0]
    )
    # join_geometry_007.Geometry -> scale_elements.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.007"].outputs[0],
        neck_1.nodes["Scale Elements"].inputs[0]
    )
    # transform_geometry_043.Geometry -> store_named_attribute_005.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.043"].outputs[0],
        neck_1.nodes["Store Named Attribute.005"].inputs[0]
    )
    # scale_elements.Geometry -> transform_geometry_042.Geometry
    neck_1.links.new(
        neck_1.nodes["Scale Elements"].outputs[0],
        neck_1.nodes["Transform Geometry.042"].inputs[0]
    )
    # transform_geometry_042.Geometry -> join_geometry_023.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.042"].outputs[0],
        neck_1.nodes["Join Geometry.023"].inputs[0]
    )
    # join_geometry_007.Geometry -> transform_geometry_043.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.007"].outputs[0],
        neck_1.nodes["Transform Geometry.043"].inputs[0]
    )
    # quadratic_b_zier_003.Curve -> join_geometry_005.Geometry
    neck_1.links.new(
        neck_1.nodes["Quadratic Bézier.003"].outputs[0],
        neck_1.nodes["Join Geometry.005"].inputs[0]
    )
    # quadratic_b_zier_006.Curve -> join_geometry_006.Geometry
    neck_1.links.new(
        neck_1.nodes["Quadratic Bézier.006"].outputs[0],
        neck_1.nodes["Join Geometry.006"].inputs[0]
    )
    # transform_geometry_006.Geometry -> join_geometry_008.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.006"].outputs[0],
        neck_1.nodes["Join Geometry.008"].inputs[0]
    )
    # bi_rail_loft_001.Mesh -> join_geometry.Geometry
    neck_1.links.new(
        neck_1.nodes["Bi-Rail Loft.001"].outputs[0],
        neck_1.nodes["Join Geometry"].inputs[0]
    )
    # separate_geometry.Selection -> join_geometry_001.Geometry
    neck_1.links.new(
        neck_1.nodes["Separate Geometry"].outputs[0],
        neck_1.nodes["Join Geometry.001"].inputs[0]
    )
    # switch.Output -> join_geometry_004.Geometry
    neck_1.links.new(
        neck_1.nodes["Switch"].outputs[0],
        neck_1.nodes["Join Geometry.004"].inputs[0]
    )
    # realize_instances_001.Geometry -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Realize Instances.001"].outputs[0],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )
    # cylinder_001.Mesh -> join_geometry_003.Geometry
    neck_1.links.new(
        neck_1.nodes["Cylinder.001"].outputs[0],
        neck_1.nodes["Join Geometry.003"].inputs[0]
    )
    # transform_geometry_017.Geometry -> join_geometry_007.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.017"].outputs[0],
        neck_1.nodes["Join Geometry.007"].inputs[0]
    )
    # store_named_attribute_006.Geometry -> join_geometry_010.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.006"].outputs[0],
        neck_1.nodes["Join Geometry.010"].inputs[0]
    )
    # instance_on_points_002.Instances -> join_geometry_011.Geometry
    neck_1.links.new(
        neck_1.nodes["Instance on Points.002"].outputs[0],
        neck_1.nodes["Join Geometry.011"].inputs[0]
    )
    # store_named_attribute_007.Geometry -> join_geometry_012.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.007"].outputs[0],
        neck_1.nodes["Join Geometry.012"].inputs[0]
    )
    # transform_geometry_022.Geometry -> join_geometry_013.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.022"].outputs[0],
        neck_1.nodes["Join Geometry.013"].inputs[0]
    )
    # transform_geometry_024.Geometry -> join_geometry_014.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.024"].outputs[0],
        neck_1.nodes["Join Geometry.014"].inputs[0]
    )
    # flip_faces.Mesh -> join_geometry_015.Geometry
    neck_1.links.new(
        neck_1.nodes["Flip Faces"].outputs[0],
        neck_1.nodes["Join Geometry.015"].inputs[0]
    )
    # mesh_to_sdf_grid.SDF Grid -> sdf_grid_boolean.Grid
    neck_1.links.new(
        neck_1.nodes["Mesh to SDF Grid"].outputs[0],
        neck_1.nodes["SDF Grid Boolean"].inputs[1]
    )
    # transform_geometry_029.Geometry -> mesh_boolean_001.Mesh
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.029"].outputs[0],
        neck_1.nodes["Mesh Boolean.001"].inputs[1]
    )
    # join_geometry_019.Geometry -> join_geometry_016.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.019"].outputs[0],
        neck_1.nodes["Join Geometry.016"].inputs[0]
    )
    # delete_geometry_002.Geometry -> join_geometry_018.Geometry
    neck_1.links.new(
        neck_1.nodes["Delete Geometry.002"].outputs[0],
        neck_1.nodes["Join Geometry.018"].inputs[0]
    )
    # flip_faces_003.Mesh -> join_geometry_019.Geometry
    neck_1.links.new(
        neck_1.nodes["Flip Faces.003"].outputs[0],
        neck_1.nodes["Join Geometry.019"].inputs[0]
    )
    # join_geometry_021.Geometry -> join_geometry_020.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.021"].outputs[0],
        neck_1.nodes["Join Geometry.020"].inputs[0]
    )
    # gem_in_holder_005.Wing -> join_geometry_021.Geometry
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.005"].outputs[3],
        neck_1.nodes["Join Geometry.021"].inputs[0]
    )
    # gem_in_holder_006.Wing -> join_geometry_022.Geometry
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.006"].outputs[3],
        neck_1.nodes["Join Geometry.022"].inputs[0]
    )
    # store_named_attribute_008.Geometry -> join_geometry_017.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.008"].outputs[0],
        neck_1.nodes["Join Geometry.017"].inputs[0]
    )
    # transform_geometry_040.Geometry -> join_geometry_009.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.040"].outputs[0],
        neck_1.nodes["Join Geometry.009"].inputs[0]
    )
    # join_geometry_009.Geometry -> join_geometry_023.Geometry
    neck_1.links.new(
        neck_1.nodes["Join Geometry.009"].outputs[0],
        neck_1.nodes["Join Geometry.023"].inputs[0]
    )
    # pipes.Mesh -> join_geometry.Geometry
    neck_1.links.new(
        neck_1.nodes["Pipes"].outputs[0],
        neck_1.nodes["Join Geometry"].inputs[0]
    )
    # for_each_geometry_element_output_001.Geometry -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Output.001"].outputs[2],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )
    # ico_sphere_003.Mesh -> join_geometry_003.Geometry
    neck_1.links.new(
        neck_1.nodes["Ico Sphere.003"].outputs[0],
        neck_1.nodes["Join Geometry.003"].inputs[0]
    )
    # transform_geometry_018.Geometry -> join_geometry_007.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.018"].outputs[0],
        neck_1.nodes["Join Geometry.007"].inputs[0]
    )
    # instance_on_points_004.Instances -> join_geometry_009.Geometry
    neck_1.links.new(
        neck_1.nodes["Instance on Points.004"].outputs[0],
        neck_1.nodes["Join Geometry.009"].inputs[0]
    )
    # transform_geometry_023.Geometry -> join_geometry_013.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.023"].outputs[0],
        neck_1.nodes["Join Geometry.013"].inputs[0]
    )
    # transform_geometry_025.Geometry -> join_geometry_014.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.025"].outputs[0],
        neck_1.nodes["Join Geometry.014"].inputs[0]
    )
    # gem_in_holder_004.Wing -> join_geometry_020.Geometry
    neck_1.links.new(
        neck_1.nodes["Gem in Holder.004"].outputs[3],
        neck_1.nodes["Join Geometry.020"].inputs[0]
    )
    # instance_on_points_009.Instances -> join_geometry_017.Geometry
    neck_1.links.new(
        neck_1.nodes["Instance on Points.009"].outputs[0],
        neck_1.nodes["Join Geometry.017"].inputs[0]
    )
    # for_each_geometry_element_output.Geometry -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["For Each Geometry Element Output"].outputs[2],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )
    # transform_geometry_013.Geometry -> join_geometry_003.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.013"].outputs[0],
        neck_1.nodes["Join Geometry.003"].inputs[0]
    )
    # transform_geometry_019.Geometry -> join_geometry_007.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.019"].outputs[0],
        neck_1.nodes["Join Geometry.007"].inputs[0]
    )
    # transform_geometry_041.Geometry -> join_geometry_009.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.041"].outputs[0],
        neck_1.nodes["Join Geometry.009"].inputs[0]
    )
    # reroute_002.Output -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Reroute.002"].outputs[0],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )
    # transform_geometry_014.Geometry -> join_geometry_003.Geometry
    neck_1.links.new(
        neck_1.nodes["Transform Geometry.014"].outputs[0],
        neck_1.nodes["Join Geometry.003"].inputs[0]
    )
    # group_006.Geometry -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Group.006"].outputs[0],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )
    # group_008.Geometry -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Group.008"].outputs[0],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )
    # mesh_boolean_002.Mesh -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Mesh Boolean.002"].outputs[0],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )
    # store_named_attribute.Geometry -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute"].outputs[0],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )
    # store_named_attribute_012.Geometry -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.012"].outputs[0],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )
    # store_named_attribute_011.Geometry -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.011"].outputs[0],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )
    # store_named_attribute_014.Geometry -> join_geometry_002.Geometry
    neck_1.links.new(
        neck_1.nodes["Store Named Attribute.014"].outputs[0],
        neck_1.nodes["Join Geometry.002"].inputs[0]
    )

    return neck_1


if __name__ == "__main__":
    # Maps node tree creation functions to the node tree 
    # name, such that we don't recreate node trees unnecessarily
    node_tree_names : dict[typing.Callable, str] = {}

    is_edge_boundary = is_edge_boundary_1_node_group(node_tree_names)
    node_tree_names[is_edge_boundary_1_node_group] = is_edge_boundary.name

    space___res_switch = space___res_switch_1_node_group(node_tree_names)
    node_tree_names[space___res_switch_1_node_group] = space___res_switch.name

    bi_rail_loft = bi_rail_loft_1_node_group(node_tree_names)
    node_tree_names[bi_rail_loft_1_node_group] = bi_rail_loft.name

    join_splines = join_splines_1_node_group(node_tree_names)
    node_tree_names[join_splines_1_node_group] = join_splines.name

    pipes = pipes_1_node_group(node_tree_names)
    node_tree_names[pipes_1_node_group] = pipes.name

    rivet = rivet_1_node_group(node_tree_names)
    node_tree_names[rivet_1_node_group] = rivet.name

    gold_wavies = gold_wavies_1_node_group(node_tree_names)
    node_tree_names[gold_wavies_1_node_group] = gold_wavies.name

    gold_decorations = gold_decorations_1_node_group(node_tree_names)
    node_tree_names[gold_decorations_1_node_group] = gold_decorations.name

    gold_on_band = gold_on_band_1_node_group(node_tree_names)
    node_tree_names[gold_on_band_1_node_group] = gold_on_band.name

    gem_in_holder = gem_in_holder_1_node_group(node_tree_names)
    node_tree_names[gem_in_holder_1_node_group] = gem_in_holder.name

    is_edge_boundary_1 = is_edge_boundary_1_node_group_1(node_tree_names)
    node_tree_names[is_edge_boundary_1_node_group_1] = is_edge_boundary_1.name

    swap_attr = swap_attr_1_node_group(node_tree_names)
    node_tree_names[swap_attr_1_node_group] = swap_attr.name

    neck = neck_1_node_group(node_tree_names)
    node_tree_names[neck_1_node_group] = neck.name

