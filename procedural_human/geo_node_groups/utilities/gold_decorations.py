import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.utilities.gold_wavies import create_gold__wavies_group

@geo_node_group
def create_gold__decorations_group():
    group_name = "Gold Decorations"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

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
    group_output.name = "Group Output"
    group_output.label = ""
    group_output.location = (2080.0, 200.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (280.0, -340.0)
    group_input.bl_label = "Group Input"
    # Links for group_input

    mesh_line = nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.label = ""
    mesh_line.location = (-1140.0, 220.0)
    mesh_line.bl_label = "Mesh Line"
    mesh_line.mode = "OFFSET"
    mesh_line.count_mode = "TOTAL"
    # Resolution
    mesh_line.inputs[1].default_value = 1.0
    # Start Location
    mesh_line.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset
    mesh_line.inputs[3].default_value = Vector((0.004999999888241291, 0.0, 0.0))
    # Links for mesh_line

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (-960.0, 220.0)
    instance_on_points.bl_label = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = True
    # Rotation
    instance_on_points.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    instance_on_points.inputs[6].default_value = Vector((1.0, 1.0, 1.0))
    # Links for instance_on_points
    links.new(mesh_line.outputs[0], instance_on_points.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (-960.0, -100.0)
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
    random_value.inputs[4].default_value = 0
    # Probability
    random_value.inputs[6].default_value = 0.5
    # ID
    random_value.inputs[7].default_value = 0
    # Links for random_value
    links.new(random_value.outputs[2], instance_on_points.inputs[4])

    scale_instances_001 = nodes.new("GeometryNodeScaleInstances")
    scale_instances_001.name = "Scale Instances.001"
    scale_instances_001.label = ""
    scale_instances_001.location = (-780.0, 160.0)
    scale_instances_001.bl_label = "Scale Instances"
    # Selection
    scale_instances_001.inputs[1].default_value = True
    # Scale
    scale_instances_001.inputs[2].default_value = Vector((1.0, -1.0, 1.0))
    # Center
    scale_instances_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Local Space
    scale_instances_001.inputs[4].default_value = True
    # Links for scale_instances_001
    links.new(instance_on_points.outputs[0], scale_instances_001.inputs[0])

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_008.name = "Join Geometry.008"
    join_geometry_008.label = ""
    join_geometry_008.location = (-440.0, 220.0)
    join_geometry_008.bl_label = "Join Geometry"
    # Links for join_geometry_008
    links.new(instance_on_points.outputs[0], join_geometry_008.inputs[0])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (-260.0, 220.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(join_geometry_008.outputs[0], realize_instances.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.name = "Flip Faces.003"
    flip_faces_003.label = ""
    flip_faces_003.location = (-620.0, 160.0)
    flip_faces_003.bl_label = "Flip Faces"
    # Selection
    flip_faces_003.inputs[1].default_value = True
    # Links for flip_faces_003
    links.new(scale_instances_001.outputs[0], flip_faces_003.inputs[0])
    links.new(flip_faces_003.outputs[0], join_geometry_008.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    bounding_box.label = ""
    bounding_box.location = (-80.0, -80.0)
    bounding_box.bl_label = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = True
    # Links for bounding_box
    links.new(realize_instances.outputs[0], bounding_box.inputs[0])

    sample_curve = nodes.new("GeometryNodeSampleCurve")
    sample_curve.name = "Sample Curve"
    sample_curve.label = ""
    sample_curve.location = (480.0, -80.0)
    sample_curve.bl_label = "Sample Curve"
    sample_curve.mode = "FACTOR"
    sample_curve.use_all_curves = True
    sample_curve.data_type = "FLOAT"
    # Value
    sample_curve.inputs[1].default_value = 0.0
    # Length
    sample_curve.inputs[3].default_value = 0.0
    # Curve Index
    sample_curve.inputs[4].default_value = 0
    # Links for sample_curve
    links.new(group_input.outputs[0], sample_curve.inputs[0])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (-80.0, -20.0)
    position_002.bl_label = "Position"
    # Links for position_002

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.label = ""
    map_range_001.location = (100.0, -20.0)
    map_range_001.bl_label = "Map Range"
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT_VECTOR"
    # Value
    map_range_001.inputs[0].default_value = 1.0
    # From Min
    map_range_001.inputs[1].default_value = 0.0
    # From Max
    map_range_001.inputs[2].default_value = 1.0
    # To Min
    map_range_001.inputs[3].default_value = 0.0
    # To Max
    map_range_001.inputs[4].default_value = 1.0
    # Steps
    map_range_001.inputs[5].default_value = 4.0
    # To Min
    map_range_001.inputs[9].default_value = [0.0, 0.0, 0.0]
    # To Max
    map_range_001.inputs[10].default_value = [1.0, 1.0, 1.0]
    # Steps
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_001
    links.new(position_002.outputs[0], map_range_001.inputs[6])
    links.new(bounding_box.outputs[1], map_range_001.inputs[7])
    links.new(bounding_box.outputs[2], map_range_001.inputs[8])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_003.name = "Separate XYZ.003"
    separate_x_y_z_003.label = ""
    separate_x_y_z_003.location = (280.0, -20.0)
    separate_x_y_z_003.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_003
    links.new(map_range_001.outputs[1], separate_x_y_z_003.inputs[0])
    links.new(separate_x_y_z_003.outputs[0], sample_curve.inputs[2])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1280.0, 220.0)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Offset
    set_position_001.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position_001
    links.new(realize_instances.outputs[0], set_position_001.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (900.0, 40.0)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "ADD"
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(sample_curve.outputs[1], vector_math_003.inputs[0])

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.label = ""
    vector_math.location = (720.0, -160.0)
    vector_math.bl_label = "Vector Math"
    vector_math.operation = "SCALE"
    # Vector
    vector_math.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math
    links.new(vector_math.outputs[0], vector_math_003.inputs[1])
    links.new(sample_curve.outputs[3], vector_math.inputs[0])

    separate_x_y_z_004 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_004.name = "Separate XYZ.004"
    separate_x_y_z_004.label = ""
    separate_x_y_z_004.location = (720.0, -440.0)
    separate_x_y_z_004.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_004
    links.new(separate_x_y_z_004.outputs[1], vector_math.inputs[3])

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.label = ""
    vector_math_001.location = (720.0, -300.0)
    vector_math_001.bl_label = "Vector Math"
    vector_math_001.operation = "CROSS_PRODUCT"
    # Vector
    vector_math_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_001.inputs[3].default_value = 1.0
    # Links for vector_math_001
    links.new(sample_curve.outputs[3], vector_math_001.inputs[1])
    links.new(sample_curve.outputs[2], vector_math_001.inputs[0])

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (880.0, -300.0)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_002
    links.new(vector_math_001.outputs[0], vector_math_002.inputs[0])
    links.new(separate_x_y_z_004.outputs[2], vector_math_002.inputs[3])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (1080.0, 40.0)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "ADD"
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_004.inputs[3].default_value = 1.0
    # Links for vector_math_004
    links.new(vector_math_003.outputs[0], vector_math_004.inputs[0])
    links.new(vector_math_004.outputs[0], set_position_001.inputs[2])
    links.new(vector_math_002.outputs[0], vector_math_004.inputs[1])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (500.0, -380.0)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "SCALE"
    # Vector
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_005
    links.new(vector_math_005.outputs[0], separate_x_y_z_004.inputs[0])
    links.new(position_002.outputs[0], vector_math_005.inputs[0])
    links.new(group_input.outputs[2], vector_math_005.inputs[3])

    gold_wavies = nodes.new("GeometryNodeGroup")
    gold_wavies.name = "Group.002"
    gold_wavies.label = ""
    gold_wavies.location = (-1320.0, 20.0)
    gold_wavies.node_tree = create_gold__wavies_group()
    gold_wavies.bl_label = "Group"
    # Links for gold_wavies
    links.new(gold_wavies.outputs[0], instance_on_points.inputs[2])

    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.label = ""
    domain_size.location = (-1320.0, -40.0)
    domain_size.bl_label = "Domain Size"
    domain_size.component = "INSTANCES"
    # Links for domain_size
    links.new(gold_wavies.outputs[0], domain_size.inputs[0])
    links.new(domain_size.outputs[5], random_value.inputs[5])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (-1160.0, -200.0)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[1], random_value.inputs[8])
    links.new(group_input_001.outputs[3], mesh_line.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (1500.0, 220.0)
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
    links.new(store_named_attribute.outputs[0], group_output.inputs[0])
    links.new(set_position_001.outputs[0], store_named_attribute.inputs[0])

    auto_layout_nodes(group)
    return group
