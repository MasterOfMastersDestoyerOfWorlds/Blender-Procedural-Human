import bpy
import math
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_loft_curve_parts_group():
    group_name = "LoftCurveParts"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    socket = group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Input", in_out="INPUT", socket_type="NodeSocketGeometry")
    socket = group.interface.new_socket(name="Vertices Y", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 3
    socket.min_value = 2
    socket.max_value = 1000

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (1255.2569580078125, 23.529390335083008)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (-829.52099609375, -36.41956329345703)
    group_input.bl_label = "Group Input"
    # Links for group_input

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (-394.2906494140625, 30.0992431640625)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketGeometry"
    # Links for reroute_001

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    grid.label = ""
    grid.location = (88.71722412109375, 116.20465087890625)
    grid.bl_label = "Grid"
    # Size X
    grid.inputs[0].default_value = 1.0
    # Size Y
    grid.inputs[1].default_value = 1.0
    # Vertices Y
    grid.inputs[3].default_value = 2
    # Links for grid

    domain_size_002 = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size_002.name = "Domain Size.002"
    domain_size_002.label = ""
    domain_size_002.location = (-377.7928466796875, 235.4501495361328)
    domain_size_002.bl_label = "Domain Size"
    domain_size_002.component = "CURVE"
    # Links for domain_size_002
    links.new(reroute_001.outputs[0], domain_size_002.inputs[0])

    sample_index_001 = nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.label = ""
    sample_index_001.location = (202.83853149414062, -203.06390380859375)
    sample_index_001.bl_label = "Sample Index"
    sample_index_001.data_type = "FLOAT_VECTOR"
    sample_index_001.domain = "POINT"
    sample_index_001.clamp = False
    # Links for sample_index_001

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    position_001.label = ""
    position_001.location = (-266.4889831542969, -316.2491455078125)
    position_001.bl_label = "Position"
    # Links for position_001
    links.new(position_001.outputs[0], sample_index_001.inputs[1])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (764.8751831054688, 109.17431640625)
    set_position.bl_label = "Set Position"
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position
    links.new(grid.outputs[0], set_position.inputs[0])
    links.new(sample_index_001.outputs[0], set_position.inputs[2])

    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    curve_to_mesh.label = ""
    curve_to_mesh.location = (-384.3772888183594, -122.1737060546875)
    curve_to_mesh.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh.inputs[3].default_value = False
    # Links for curve_to_mesh
    links.new(curve_to_mesh.outputs[0], sample_index_001.inputs[0])
    links.new(reroute_001.outputs[0], curve_to_mesh.inputs[0])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (-118.58908081054688, 165.6099853515625)
    math.bl_label = "Math"
    math.operation = "MULTIPLY"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(group_input.outputs[1], math.inputs[0])
    links.new(domain_size_002.outputs[4], math.inputs[1])
    links.new(math.outputs[0], grid.inputs[2])

    set_spline_resolution = nodes.new("GeometryNodeSetSplineResolution")
    set_spline_resolution.name = "Set Spline Resolution"
    set_spline_resolution.label = ""
    set_spline_resolution.location = (-626.55029296875, 66.59427642822266)
    set_spline_resolution.bl_label = "Set Spline Resolution"
    # Selection
    set_spline_resolution.inputs[1].default_value = True
    # Links for set_spline_resolution
    links.new(set_spline_resolution.outputs[0], reroute_001.inputs[0])
    links.new(group_input.outputs[0], set_spline_resolution.inputs[0])
    links.new(group_input.outputs[1], set_spline_resolution.inputs[2])

    index_002 = nodes.new("GeometryNodeInputIndex")
    index_002.name = "Index.002"
    index_002.label = ""
    index_002.location = (-374.6027526855469, -656.0223388671875)
    index_002.bl_label = "Index"
    # Links for index_002
    links.new(index_002.outputs[0], sample_index_001.inputs[2])

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (-604.625, -325.7002868652344)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "MESH"
    # Links for domain_size
    links.new(curve_to_mesh.outputs[0], domain_size.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (986.3859252929688, 77.2415771484375)
    set_position_001.bl_label = "Set Position"
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001
    links.new(set_position_001.outputs[0], group_output.inputs[0])
    links.new(set_position.outputs[0], set_position_001.inputs[0])

    integer_math = nodes.new("FunctionNodeIntegerMath")
    integer_math.name = "Integer Math"
    integer_math.label = ""
    integer_math.location = (669.9136352539062, -668.1951293945312)
    integer_math.bl_label = "Integer Math"
    integer_math.operation = "MODULO"
    # Value
    integer_math.inputs[1].default_value = 2
    # Value
    integer_math.inputs[2].default_value = 0
    # Links for integer_math

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (898.0842895507812, -666.5128173828125)
    compare.bl_label = "Compare"
    compare.operation = "EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    # A
    compare.inputs[0].default_value = 0.0
    # B
    compare.inputs[1].default_value = 0.0
    # B
    compare.inputs[3].default_value = 1
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
    links.new(integer_math.outputs[0], compare.inputs[2])
    links.new(compare.outputs[0], set_position.inputs[1])

    boolean_math = nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.label = ""
    boolean_math.location = (1152.7901611328125, -266.4172668457031)
    boolean_math.bl_label = "Boolean Math"
    boolean_math.operation = "NOT"
    # Boolean
    boolean_math.inputs[1].default_value = False
    # Links for boolean_math
    links.new(compare.outputs[0], boolean_math.inputs[0])
    links.new(boolean_math.outputs[0], set_position_001.inputs[1])

    sample_index_002 = nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.label = ""
    sample_index_002.location = (396.6791076660156, -362.68695068359375)
    sample_index_002.bl_label = "Sample Index"
    sample_index_002.data_type = "FLOAT_VECTOR"
    sample_index_002.domain = "POINT"
    sample_index_002.clamp = False
    # Links for sample_index_002
    links.new(curve_to_mesh.outputs[0], sample_index_002.inputs[0])
    links.new(position_001.outputs[0], sample_index_002.inputs[1])
    links.new(sample_index_002.outputs[0], set_position_001.inputs[2])
    links.new(index_002.outputs[0], sample_index_002.inputs[2])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (130.1511688232422, -704.9738159179688)
    math_002.bl_label = "Math"
    math_002.operation = "ADD"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 1.0
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(index_002.outputs[0], math_002.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (310.0, -718.643798828125)
    math_003.bl_label = "Math"
    math_003.operation = "DIVIDE"
    math_003.use_clamp = False
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_002.outputs[0], math_003.inputs[0])
    links.new(group_input.outputs[1], math_003.inputs[1])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (489.9999694824219, -736.5201416015625)
    math_004.bl_label = "Math"
    math_004.operation = "TRUNC"
    math_004.use_clamp = False
    # Value
    math_004.inputs[1].default_value = 0.5
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(math_004.outputs[0], integer_math.inputs[0])
    links.new(math_003.outputs[0], math_004.inputs[0])

    auto_layout_nodes(group)
    return group