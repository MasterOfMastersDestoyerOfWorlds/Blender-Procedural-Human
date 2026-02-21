import bpy
from bpy.types import GeometryNodeGroup
from bpy.props import FloatVectorProperty, FloatProperty
from math import radians
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes

@geo_node_group
def create_blocker_group():
    group_name = "Blocker"
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
    group_output.location = (1991.1298828125, -100.0)
    group_output.bl_label = "Group Output"
    group_output.is_active_output = True
    # Links for group_output

    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    join_geometry.label = ""
    join_geometry.location = (1511.1298828125, -100.0)
    join_geometry.bl_label = "Join Geometry"
    # Links for join_geometry

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.label = ""
    set_shade_smooth.location = (1671.1298828125, -100.0)
    set_shade_smooth.bl_label = "Set Shade Smooth"
    set_shade_smooth.domain = "FACE"
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True
    # Links for set_shade_smooth
    links.new(set_shade_smooth.outputs[0], group_output.inputs[0])
    links.new(join_geometry.outputs[0], set_shade_smooth.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.label = ""
    store_named_attribute.location = (7331.1298828125, -712.0)
    store_named_attribute.bl_label = "Store Named Attribute"
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "blocker"
    # Value
    store_named_attribute.inputs[3].default_value = True
    # Links for store_named_attribute
    links.new(store_named_attribute.outputs[0], join_geometry.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    ico_sphere.label = ""
    ico_sphere.location = (30.0, -276.0)
    ico_sphere.bl_label = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.1300000250339508
    # Subdivisions
    ico_sphere.inputs[1].default_value = 3
    # Links for ico_sphere

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    transform_geometry.label = ""
    transform_geometry.location = (330.0, -376.0)
    transform_geometry.bl_label = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = "Components"
    # Translation
    transform_geometry.inputs[2].default_value = Vector((-0.03999999910593033, 0.0, 0.25))
    # Rotation
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.2000000476837158))
    # Links for transform_geometry
    links.new(ico_sphere.outputs[0], transform_geometry.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.name = "Frame.001"
    frame_001.label = "Chest"
    frame_001.location = (-1910.0, 696.0)
    frame_001.bl_label = "Frame"
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20
    # Links for frame_001

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    transform_geometry_001.label = ""
    transform_geometry_001.location = (330.0, -36.0)
    transform_geometry_001.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_001.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_001.inputs[2].default_value = Vector((-0.10000000149011612, 0.019999999552965164, 0.33000001311302185))
    # Rotation
    transform_geometry_001.inputs[3].default_value = Euler((0.0, -0.13439033925533295, 0.18500488996505737), 'XYZ')
    # Scale
    transform_geometry_001.inputs[4].default_value = Vector((1.0199999809265137, 0.8300000429153442, 0.8400001525878906))
    # Links for transform_geometry_001
    links.new(ico_sphere.outputs[0], transform_geometry_001.inputs[0])

    mesh_to_s_d_f_grid = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid.name = "Mesh to SDF Grid"
    mesh_to_s_d_f_grid.label = ""
    mesh_to_s_d_f_grid.location = (570.0, -436.0)
    mesh_to_s_d_f_grid.bl_label = "Mesh to SDF Grid"
    # Voxel Size
    mesh_to_s_d_f_grid.inputs[1].default_value = 0.004999999888241291
    # Band Width
    mesh_to_s_d_f_grid.inputs[2].default_value = 2
    # Links for mesh_to_s_d_f_grid
    links.new(transform_geometry.outputs[0], mesh_to_s_d_f_grid.inputs[0])

    mesh_to_s_d_f_grid_001 = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid_001.name = "Mesh to SDF Grid.001"
    mesh_to_s_d_f_grid_001.label = ""
    mesh_to_s_d_f_grid_001.location = (570.0, -296.0)
    mesh_to_s_d_f_grid_001.bl_label = "Mesh to SDF Grid"
    # Voxel Size
    mesh_to_s_d_f_grid_001.inputs[1].default_value = 0.004999999888241291
    # Band Width
    mesh_to_s_d_f_grid_001.inputs[2].default_value = 2
    # Links for mesh_to_s_d_f_grid_001
    links.new(transform_geometry_001.outputs[0], mesh_to_s_d_f_grid_001.inputs[0])

    s_d_f_grid_boolean = nodes.new("GeometryNodeSDFGridBoolean")
    s_d_f_grid_boolean.name = "SDF Grid Boolean"
    s_d_f_grid_boolean.label = ""
    s_d_f_grid_boolean.location = (730.0, -296.0)
    s_d_f_grid_boolean.bl_label = "SDF Grid Boolean"
    s_d_f_grid_boolean.operation = "UNION"
    # Grid 1
    s_d_f_grid_boolean.inputs[0].default_value = 0.0
    # Links for s_d_f_grid_boolean
    links.new(mesh_to_s_d_f_grid.outputs[0], s_d_f_grid_boolean.inputs[1])
    links.new(mesh_to_s_d_f_grid_001.outputs[0], s_d_f_grid_boolean.inputs[1])

    grid_to_mesh = nodes.new("GeometryNodeGridToMesh")
    grid_to_mesh.name = "Grid to Mesh"
    grid_to_mesh.label = ""
    grid_to_mesh.location = (1050.0, -296.0)
    grid_to_mesh.bl_label = "Grid to Mesh"
    # Threshold
    grid_to_mesh.inputs[1].default_value = 0.0
    # Adaptivity
    grid_to_mesh.inputs[2].default_value = 0.0
    # Links for grid_to_mesh

    s_d_f_grid_fillet = nodes.new("GeometryNodeSDFGridFillet")
    s_d_f_grid_fillet.name = "SDF Grid Fillet"
    s_d_f_grid_fillet.label = ""
    s_d_f_grid_fillet.location = (890.0, -296.0)
    s_d_f_grid_fillet.bl_label = "SDF Grid Fillet"
    # Iterations
    s_d_f_grid_fillet.inputs[1].default_value = 3
    # Links for s_d_f_grid_fillet
    links.new(s_d_f_grid_boolean.outputs[0], s_d_f_grid_fillet.inputs[0])
    links.new(s_d_f_grid_fillet.outputs[0], grid_to_mesh.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    instance_on_points.label = ""
    instance_on_points.location = (1730.0, -276.0)
    instance_on_points.bl_label = "Instance on Points"
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Scale
    instance_on_points.inputs[6].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))
    # Links for instance_on_points
    links.new(grid_to_mesh.outputs[0], instance_on_points.inputs[0])

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.name = "Curve Circle.001"
    curve_circle_001.label = ""
    curve_circle_001.location = (870.0, -476.0)
    curve_circle_001.bl_label = "Curve Circle"
    curve_circle_001.mode = "RADIUS"
    # Resolution
    curve_circle_001.inputs[0].default_value = 9
    # Point 1
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_001.inputs[4].default_value = 0.004999999888241291
    # Links for curve_circle_001

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    curve_to_mesh_001.label = ""
    curve_to_mesh_001.location = (1050.0, -476.0)
    curve_to_mesh_001.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_001.inputs[2].default_value = 0.21000000834465027
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False
    # Links for curve_to_mesh_001
    links.new(curve_circle_001.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(curve_circle_001.outputs[0], curve_to_mesh_001.inputs[1])
    links.new(curve_to_mesh_001.outputs[0], instance_on_points.inputs[2])

    position_002 = nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    position_002.label = ""
    position_002.location = (1370.0, -416.0)
    position_002.bl_label = "Position"
    # Links for position_002

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_001.name = "Separate XYZ.001"
    separate_x_y_z_001.label = ""
    separate_x_y_z_001.location = (1370.0, -476.0)
    separate_x_y_z_001.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_001
    links.new(position_002.outputs[0], separate_x_y_z_001.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.label = ""
    compare_001.location = (1530.0, -416.0)
    compare_001.bl_label = "Compare"
    compare_001.operation = "LESS_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    # B
    compare_001.inputs[1].default_value = -0.09999999403953552
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
    links.new(separate_x_y_z_001.outputs[0], compare_001.inputs[0])
    links.new(compare_001.outputs[0], instance_on_points.inputs[1])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.label = ""
    align_rotation_to_vector.location = (1210.0, -616.0)
    align_rotation_to_vector.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector.axis = "Z"
    align_rotation_to_vector.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.name = "Normal.001"
    normal_001.label = ""
    normal_001.location = (1050.0, -616.0)
    normal_001.bl_label = "Normal"
    normal_001.legacy_corner_normals = False
    # Links for normal_001
    links.new(normal_001.outputs[0], align_rotation_to_vector.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.name = "Rotate Rotation"
    rotate_rotation.label = ""
    rotate_rotation.location = (1370.0, -616.0)
    rotate_rotation.bl_label = "Rotate Rotation"
    rotate_rotation.rotation_space = "LOCAL"
    # Rotate By
    rotate_rotation.inputs[1].default_value = Euler((-0.3707079291343689, 0.3525564670562744, 0.0), 'XYZ')
    # Links for rotate_rotation
    links.new(align_rotation_to_vector.outputs[0], rotate_rotation.inputs[0])

    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.name = "Rotate Rotation.001"
    rotate_rotation_001.label = ""
    rotate_rotation_001.location = (1550.0, -616.0)
    rotate_rotation_001.bl_label = "Rotate Rotation"
    rotate_rotation_001.rotation_space = "LOCAL"
    # Links for rotate_rotation_001
    links.new(rotate_rotation_001.outputs[0], instance_on_points.inputs[5])
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.label = ""
    random_value.location = (1550.0, -736.0)
    random_value.bl_label = "Random Value"
    random_value.data_type = "FLOAT_VECTOR"
    # Min
    random_value.inputs[0].default_value = [-0.10000000149011612, -0.10000000149011612, -0.10000000149011612]
    # Max
    random_value.inputs[1].default_value = [0.10000000149011612, 0.10000000149011612, 0.10000000149011612]
    # Min
    random_value.inputs[2].default_value = 0.0
    # Max
    random_value.inputs[3].default_value = 1.0
    # Min
    random_value.inputs[4].default_value = 0
    # Max
    random_value.inputs[5].default_value = 100
    # Probability
    random_value.inputs[6].default_value = 0.5
    # ID
    random_value.inputs[7].default_value = 0
    # Seed
    random_value.inputs[8].default_value = 2
    # Links for random_value
    links.new(random_value.outputs[0], rotate_rotation_001.inputs[1])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    realize_instances.label = ""
    realize_instances.location = (1890.0, -276.0)
    realize_instances.bl_label = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0
    # Links for realize_instances
    links.new(instance_on_points.outputs[0], realize_instances.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.label = ""
    switch.location = (2110.0, -156.0)
    switch.bl_label = "Switch"
    switch.input_type = "GEOMETRY"
    # Links for switch
    links.new(switch.outputs[0], join_geometry.inputs[0])
    links.new(realize_instances.outputs[0], switch.inputs[2])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"
    join_geometry_002.label = ""
    join_geometry_002.location = (590.0, -156.0)
    join_geometry_002.bl_label = "Join Geometry"
    # Links for join_geometry_002
    links.new(transform_geometry_001.outputs[0], join_geometry_002.inputs[0])
    links.new(transform_geometry.outputs[0], join_geometry_002.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.label = ""
    reroute.location = (2010.0, -196.0)
    reroute.bl_label = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Links for reroute
    links.new(reroute.outputs[0], switch.inputs[1])
    links.new(join_geometry_002.outputs[0], reroute.inputs[0])

    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.label = ""
    group_input.location = (2110.0, -96.0)
    group_input.bl_label = "Group Input"
    # Links for group_input
    links.new(group_input.outputs[0], switch.inputs[0])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    curve_to_mesh_002.label = ""
    curve_to_mesh_002.location = (1170.0, -416.0)
    curve_to_mesh_002.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False
    # Links for curve_to_mesh_002

    curve_circle_002 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_002.name = "Curve Circle.002"
    curve_circle_002.label = ""
    curve_circle_002.location = (470.0, -496.0)
    curve_circle_002.bl_label = "Curve Circle"
    curve_circle_002.mode = "RADIUS"
    # Resolution
    curve_circle_002.inputs[0].default_value = 105
    # Point 1
    curve_circle_002.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_002.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_002.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_002.inputs[4].default_value = 0.10000000149011612
    # Links for curve_circle_002

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.label = ""
    spline_parameter_001.location = (30.0, -596.0)
    spline_parameter_001.bl_label = "Spline Parameter"
    # Links for spline_parameter_001

    float_curve_001 = nodes.new("ShaderNodeFloatCurve")
    float_curve_001.name = "Float Curve.001"
    float_curve_001.label = ""
    float_curve_001.location = (190.0, -476.0)
    float_curve_001.bl_label = "Float Curve"
    # Factor
    float_curve_001.inputs[0].default_value = 1.0
    # Links for float_curve_001
    links.new(spline_parameter_001.outputs[0], float_curve_001.inputs[1])
    links.new(float_curve_001.outputs[0], curve_to_mesh_002.inputs[2])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.label = ""
    resample_curve_001.location = (190.0, -256.0)
    resample_curve_001.bl_label = "Resample Curve"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = "Count"
    # Count
    resample_curve_001.inputs[3].default_value = 34
    # Length
    resample_curve_001.inputs[4].default_value = 0.10000000149011612
    # Links for resample_curve_001

    quadratic_bézier_001 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_001.name = "Quadratic Bézier.001"
    quadratic_bézier_001.label = ""
    quadratic_bézier_001.location = (30.0, -256.0)
    quadratic_bézier_001.bl_label = "Quadratic Bézier"
    # Resolution
    quadratic_bézier_001.inputs[0].default_value = 16
    # Start
    quadratic_bézier_001.inputs[1].default_value = Vector((0.0, -0.009999999776482582, 0.4000000059604645))
    # Middle
    quadratic_bézier_001.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.44999995827674866))
    # End
    quadratic_bézier_001.inputs[3].default_value = Vector((0.0, -0.04999999701976776, 0.5199999809265137))
    # Links for quadratic_bézier_001
    links.new(quadratic_bézier_001.outputs[0], resample_curve_001.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.label = ""
    set_position_001.location = (1041.1298828125, -36.0)
    set_position_001.bl_label = "Set Position"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Position
    set_position_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_001

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.label = ""
    vector_math_002.location = (641.1298828125, -176.0)
    vector_math_002.bl_label = "Vector Math"
    vector_math_002.operation = "SCALE"
    # Vector
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_002.inputs[3].default_value = 0.0020000000949949026
    # Links for vector_math_002

    noise_texture_001 = nodes.new("ShaderNodeTexNoise")
    noise_texture_001.name = "Noise Texture.001"
    noise_texture_001.label = ""
    noise_texture_001.location = (301.1298828125, -316.0)
    noise_texture_001.bl_label = "Noise Texture"
    noise_texture_001.noise_dimensions = "2D"
    noise_texture_001.noise_type = "FBM"
    noise_texture_001.normalize = False
    # W
    noise_texture_001.inputs[1].default_value = 0.0
    # Scale
    noise_texture_001.inputs[2].default_value = 5.669999599456787
    # Detail
    noise_texture_001.inputs[3].default_value = 0.0
    # Roughness
    noise_texture_001.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture_001.inputs[5].default_value = 2.0
    # Offset
    noise_texture_001.inputs[6].default_value = 0.0
    # Gain
    noise_texture_001.inputs[7].default_value = 1.0
    # Distortion
    noise_texture_001.inputs[8].default_value = 0.0
    # Links for noise_texture_001
    links.new(noise_texture_001.outputs[1], vector_math_002.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.label = ""
    vector_math_003.location = (141.12982177734375, -316.0)
    vector_math_003.bl_label = "Vector Math"
    vector_math_003.operation = "MULTIPLY"
    # Vector
    vector_math_003.inputs[1].default_value = [1.0, 2.5999999046325684, 24.950000762939453]
    # Vector
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_003.inputs[3].default_value = 1.0
    # Links for vector_math_003
    links.new(vector_math_003.outputs[0], noise_texture_001.inputs[0])

    quadrilateral = nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
    quadrilateral.name = "Quadrilateral"
    quadrilateral.label = ""
    quadrilateral.location = (230.0, -732.0)
    quadrilateral.bl_label = "Quadrilateral"
    quadrilateral.mode = "RECTANGLE"
    # Width
    quadrilateral.inputs[0].default_value = 0.5
    # Height
    quadrilateral.inputs[1].default_value = 0.15000000596046448
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
    fillet_curve.location = (550.0, -732.0)
    fillet_curve.bl_label = "Fillet Curve"
    # Limit Radius
    fillet_curve.inputs[2].default_value = False
    # Mode
    fillet_curve.inputs[3].default_value = "Bézier"
    # Count
    fillet_curve.inputs[4].default_value = 1
    # Links for fillet_curve

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.label = ""
    set_spline_type.location = (390.0, -732.0)
    set_spline_type.bl_label = "Set Spline Type"
    set_spline_type.spline_type = "BEZIER"
    # Selection
    set_spline_type.inputs[1].default_value = True
    # Links for set_spline_type
    links.new(set_spline_type.outputs[0], fillet_curve.inputs[0])
    links.new(quadrilateral.outputs[0], set_spline_type.inputs[0])

    index_switch = nodes.new("GeometryNodeIndexSwitch")
    index_switch.name = "Index Switch"
    index_switch.label = ""
    index_switch.location = (550.0, -852.0)
    index_switch.bl_label = "Index Switch"
    index_switch.data_type = "FLOAT"
    # 0
    index_switch.inputs[1].default_value = 0.09000000357627869
    # 1
    index_switch.inputs[2].default_value = 0.09000000357627869
    # Links for index_switch
    links.new(index_switch.outputs[0], fillet_curve.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    index.name = "Index"
    index.label = ""
    index.location = (390.0, -852.0)
    index.bl_label = "Index"
    # Links for index
    links.new(index.outputs[0], index_switch.inputs[0])

    fill_curve = nodes.new("GeometryNodeFillCurve")
    fill_curve.name = "Fill Curve"
    fill_curve.label = ""
    fill_curve.location = (710.0, -732.0)
    fill_curve.bl_label = "Fill Curve"
    # Group ID
    fill_curve.inputs[1].default_value = 0
    # Mode
    fill_curve.inputs[2].default_value = "N-gons"
    # Links for fill_curve
    links.new(fillet_curve.outputs[0], fill_curve.inputs[0])

    extrude_mesh_002 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_002.name = "Extrude Mesh.002"
    extrude_mesh_002.label = ""
    extrude_mesh_002.location = (890.0, -732.0)
    extrude_mesh_002.bl_label = "Extrude Mesh"
    extrude_mesh_002.mode = "FACES"
    # Selection
    extrude_mesh_002.inputs[1].default_value = True
    # Offset
    extrude_mesh_002.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh_002.inputs[3].default_value = 0.009999999776482582
    # Individual
    extrude_mesh_002.inputs[4].default_value = False
    # Links for extrude_mesh_002
    links.new(fill_curve.outputs[0], extrude_mesh_002.inputs[0])

    flip_faces_002 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.name = "Flip Faces.002"
    flip_faces_002.label = ""
    flip_faces_002.location = (890.0, -632.0)
    flip_faces_002.bl_label = "Flip Faces"
    # Selection
    flip_faces_002.inputs[1].default_value = True
    # Links for flip_faces_002
    links.new(fill_curve.outputs[0], flip_faces_002.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.label = ""
    join_geometry_004.location = (1070.0, -692.0)
    join_geometry_004.bl_label = "Join Geometry"
    # Links for join_geometry_004
    links.new(extrude_mesh_002.outputs[0], join_geometry_004.inputs[0])
    links.new(flip_faces_002.outputs[0], join_geometry_004.inputs[0])

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.name = "Merge by Distance.002"
    merge_by_distance_002.label = ""
    merge_by_distance_002.location = (1070.0, -732.0)
    merge_by_distance_002.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance_002.inputs[1].default_value = True
    # Mode
    merge_by_distance_002.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_002
    links.new(join_geometry_004.outputs[0], merge_by_distance_002.inputs[0])

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    grid.label = ""
    grid.location = (30.0, -332.0)
    grid.bl_label = "Grid"
    # Size X
    grid.inputs[0].default_value = 0.6000000238418579
    # Size Y
    grid.inputs[1].default_value = 0.30000001192092896
    # Vertices X
    grid.inputs[2].default_value = 13
    # Vertices Y
    grid.inputs[3].default_value = 7
    # Links for grid

    extrude_mesh_003 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_003.name = "Extrude Mesh.003"
    extrude_mesh_003.label = ""
    extrude_mesh_003.location = (210.0, -332.0)
    extrude_mesh_003.bl_label = "Extrude Mesh"
    extrude_mesh_003.mode = "FACES"
    # Selection
    extrude_mesh_003.inputs[1].default_value = True
    # Offset
    extrude_mesh_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh_003.inputs[3].default_value = 0.0
    # Individual
    extrude_mesh_003.inputs[4].default_value = True
    # Links for extrude_mesh_003
    links.new(grid.outputs[0], extrude_mesh_003.inputs[0])

    scale_elements = nodes.new("GeometryNodeScaleElements")
    scale_elements.name = "Scale Elements"
    scale_elements.label = ""
    scale_elements.location = (370.0, -332.0)
    scale_elements.bl_label = "Scale Elements"
    scale_elements.domain = "FACE"
    # Scale
    scale_elements.inputs[2].default_value = 0.0
    # Center
    scale_elements.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Scale Mode
    scale_elements.inputs[4].default_value = "Uniform"
    # Axis
    scale_elements.inputs[5].default_value = [1.0, 0.0, 0.0]
    # Links for scale_elements
    links.new(extrude_mesh_003.outputs[0], scale_elements.inputs[0])
    links.new(extrude_mesh_003.outputs[1], scale_elements.inputs[1])

    merge_by_distance_003 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_003.name = "Merge by Distance.003"
    merge_by_distance_003.label = ""
    merge_by_distance_003.location = (530.0, -332.0)
    merge_by_distance_003.bl_label = "Merge by Distance"
    # Mode
    merge_by_distance_003.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_003.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_003
    links.new(scale_elements.outputs[0], merge_by_distance_003.inputs[0])
    links.new(extrude_mesh_003.outputs[1], merge_by_distance_003.inputs[1])

    subdivide_mesh = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh.name = "Subdivide Mesh"
    subdivide_mesh.label = ""
    subdivide_mesh.location = (690.0, -332.0)
    subdivide_mesh.bl_label = "Subdivide Mesh"
    # Level
    subdivide_mesh.inputs[1].default_value = 3
    # Links for subdivide_mesh
    links.new(merge_by_distance_003.outputs[0], subdivide_mesh.inputs[0])

    mesh_boolean = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean.name = "Mesh Boolean"
    mesh_boolean.label = ""
    mesh_boolean.location = (1230.0, -332.0)
    mesh_boolean.bl_label = "Mesh Boolean"
    mesh_boolean.operation = "INTERSECT"
    mesh_boolean.solver = "MANIFOLD"
    # Self Intersection
    mesh_boolean.inputs[2].default_value = False
    # Hole Tolerant
    mesh_boolean.inputs[3].default_value = False
    # Links for mesh_boolean
    links.new(merge_by_distance_002.outputs[0], mesh_boolean.inputs[1])

    extrude_mesh_004 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_004.name = "Extrude Mesh.004"
    extrude_mesh_004.label = ""
    extrude_mesh_004.location = (870.0, -332.0)
    extrude_mesh_004.bl_label = "Extrude Mesh"
    extrude_mesh_004.mode = "FACES"
    # Selection
    extrude_mesh_004.inputs[1].default_value = True
    # Offset
    extrude_mesh_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Offset Scale
    extrude_mesh_004.inputs[3].default_value = 0.009999999776482582
    # Individual
    extrude_mesh_004.inputs[4].default_value = False
    # Links for extrude_mesh_004
    links.new(subdivide_mesh.outputs[0], extrude_mesh_004.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.name = "Flip Faces.003"
    flip_faces_003.label = ""
    flip_faces_003.location = (870.0, -232.0)
    flip_faces_003.bl_label = "Flip Faces"
    # Selection
    flip_faces_003.inputs[1].default_value = True
    # Links for flip_faces_003
    links.new(subdivide_mesh.outputs[0], flip_faces_003.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.label = ""
    join_geometry_005.location = (1050.0, -292.0)
    join_geometry_005.bl_label = "Join Geometry"
    # Links for join_geometry_005
    links.new(extrude_mesh_004.outputs[0], join_geometry_005.inputs[0])
    links.new(flip_faces_003.outputs[0], join_geometry_005.inputs[0])

    merge_by_distance_004 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_004.name = "Merge by Distance.004"
    merge_by_distance_004.label = ""
    merge_by_distance_004.location = (1050.0, -332.0)
    merge_by_distance_004.bl_label = "Merge by Distance"
    # Selection
    merge_by_distance_004.inputs[1].default_value = True
    # Mode
    merge_by_distance_004.inputs[2].default_value = "All"
    # Distance
    merge_by_distance_004.inputs[3].default_value = 0.0010000000474974513
    # Links for merge_by_distance_004
    links.new(join_geometry_005.outputs[0], merge_by_distance_004.inputs[0])
    links.new(merge_by_distance_004.outputs[0], mesh_boolean.inputs[1])

    delete_geometry_002 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.name = "Delete Geometry.002"
    delete_geometry_002.label = ""
    delete_geometry_002.location = (1390.0, -332.0)
    delete_geometry_002.bl_label = "Delete Geometry"
    delete_geometry_002.mode = "ALL"
    delete_geometry_002.domain = "POINT"
    # Links for delete_geometry_002
    links.new(mesh_boolean.outputs[0], delete_geometry_002.inputs[0])
    links.new(extrude_mesh_004.outputs[1], delete_geometry_002.inputs[1])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    set_position_002.label = ""
    set_position_002.location = (1230.0, -316.0)
    set_position_002.bl_label = "Set Position"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Position
    set_position_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for set_position_002
    links.new(delete_geometry_002.outputs[0], set_position_002.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.label = ""
    geometry_proximity.location = (30.0, -36.0)
    geometry_proximity.bl_label = "Geometry Proximity"
    geometry_proximity.target_element = "EDGES"
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0
    # Links for geometry_proximity

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.label = ""
    separate_geometry.location = (690.0, -112.0)
    separate_geometry.bl_label = "Separate Geometry"
    separate_geometry.domain = "EDGE"
    # Links for separate_geometry
    links.new(merge_by_distance_003.outputs[0], separate_geometry.inputs[0])

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.label = ""
    geometry_proximity_001.location = (210.0, -112.0)
    geometry_proximity_001.bl_label = "Geometry Proximity"
    geometry_proximity_001.target_element = "EDGES"
    # Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0
    # Links for geometry_proximity_001
    links.new(grid.outputs[0], geometry_proximity_001.inputs[0])

    compare_003 = nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.label = ""
    compare_003.location = (370.0, -112.0)
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
    links.new(geometry_proximity_001.outputs[1], compare_003.inputs[0])
    links.new(compare_003.outputs[0], separate_geometry.inputs[1])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.label = ""
    combine_x_y_z.location = (830.0, -36.0)
    combine_x_y_z.bl_label = "Combine XYZ"
    # X
    combine_x_y_z.inputs[0].default_value = 0.0
    # Y
    combine_x_y_z.inputs[1].default_value = 0.0
    # Links for combine_x_y_z
    links.new(combine_x_y_z.outputs[0], set_position_002.inputs[3])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.label = ""
    map_range.location = (190.0, -36.0)
    map_range.bl_label = "Map Range"
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    # From Min
    map_range.inputs[1].default_value = 0.0
    # From Max
    map_range.inputs[2].default_value = 0.009999999776482582
    # To Min
    map_range.inputs[3].default_value = 1.0
    # To Max
    map_range.inputs[4].default_value = 0.0
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
    links.new(geometry_proximity.outputs[1], map_range.inputs[0])

    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.label = ""
    math_002.location = (350.0, -36.0)
    math_002.bl_label = "Math"
    math_002.operation = "POWER"
    math_002.use_clamp = False
    # Value
    math_002.inputs[1].default_value = 2.0
    # Value
    math_002.inputs[2].default_value = 0.5
    # Links for math_002
    links.new(map_range.outputs[0], math_002.inputs[0])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.label = ""
    math_003.location = (670.0, -36.0)
    math_003.bl_label = "Math"
    math_003.operation = "MULTIPLY"
    math_003.use_clamp = False
    # Value
    math_003.inputs[1].default_value = 0.0020000000949949026
    # Value
    math_003.inputs[2].default_value = 0.5
    # Links for math_003
    links.new(math_003.outputs[0], combine_x_y_z.inputs[2])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.label = ""
    math_004.location = (510.0, -36.0)
    math_004.bl_label = "Math"
    math_004.operation = "SUBTRACT"
    math_004.use_clamp = False
    # Value
    math_004.inputs[0].default_value = 1.0
    # Value
    math_004.inputs[2].default_value = 0.5
    # Links for math_004
    links.new(math_004.outputs[0], math_003.inputs[0])
    links.new(math_002.outputs[0], math_004.inputs[1])

    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.name = "Curve to Mesh.003"
    curve_to_mesh_003.label = ""
    curve_to_mesh_003.location = (1530.0, -56.0)
    curve_to_mesh_003.bl_label = "Curve to Mesh"
    # Scale
    curve_to_mesh_003.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh_003.inputs[3].default_value = False
    # Links for curve_to_mesh_003

    curve_circle_003 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.name = "Curve Circle.003"
    curve_circle_003.label = ""
    curve_circle_003.location = (770.0, -196.0)
    curve_circle_003.bl_label = "Curve Circle"
    curve_circle_003.mode = "RADIUS"
    # Resolution
    curve_circle_003.inputs[0].default_value = 57
    # Point 1
    curve_circle_003.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_003.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_003.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_003.inputs[4].default_value = 0.004999999888241291
    # Links for curve_circle_003

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    transform_geometry_002.label = ""
    transform_geometry_002.location = (950.0, -196.0)
    transform_geometry_002.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_002.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_002.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_002.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 0.5, 1.0))
    # Links for transform_geometry_002
    links.new(curve_circle_003.outputs[0], transform_geometry_002.inputs[0])

    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.name = "Resample Curve.002"
    resample_curve_002.label = ""
    resample_curve_002.location = (1050.0, -36.0)
    resample_curve_002.bl_label = "Resample Curve"
    resample_curve_002.keep_last_segment = True
    # Selection
    resample_curve_002.inputs[1].default_value = True
    # Mode
    resample_curve_002.inputs[2].default_value = "Length"
    # Count
    resample_curve_002.inputs[3].default_value = 10
    # Length
    resample_curve_002.inputs[4].default_value = 0.009999999776482582
    # Links for resample_curve_002
    links.new(resample_curve_002.outputs[0], curve_to_mesh_003.inputs[0])
    links.new(fillet_curve.outputs[0], resample_curve_002.inputs[0])

    frame_002 = nodes.new("NodeFrame")
    frame_002.name = "Frame.002"
    frame_002.label = "Piping"
    frame_002.location = (180.0, -1616.0)
    frame_002.bl_label = "Frame"
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20
    # Links for frame_002

    frame_003 = nodes.new("NodeFrame")
    frame_003.name = "Frame.003"
    frame_003.label = "Quilting"
    frame_003.location = (1560.0, -36.0)
    frame_003.bl_label = "Frame"
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20
    # Links for frame_003

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    transform_geometry_003.label = ""
    transform_geometry_003.location = (3010.0, -412.0)
    transform_geometry_003.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_003.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_003.inputs[4].default_value = Vector((1.0, 1.0, -1.0))
    # Links for transform_geometry_003
    links.new(set_position_002.outputs[0], transform_geometry_003.inputs[0])

    flip_faces_004 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_004.name = "Flip Faces.004"
    flip_faces_004.label = ""
    flip_faces_004.location = (3010.0, -332.0)
    flip_faces_004.bl_label = "Flip Faces"
    # Selection
    flip_faces_004.inputs[1].default_value = True
    # Links for flip_faces_004
    links.new(set_position_002.outputs[0], flip_faces_004.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.label = ""
    join_geometry_006.location = (3210.0, -372.0)
    join_geometry_006.bl_label = "Join Geometry"
    # Links for join_geometry_006
    links.new(transform_geometry_003.outputs[0], join_geometry_006.inputs[0])
    links.new(flip_faces_004.outputs[0], join_geometry_006.inputs[0])

    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_007.name = "Join Geometry.007"
    join_geometry_007.label = ""
    join_geometry_007.location = (1130.0, -152.0)
    join_geometry_007.bl_label = "Join Geometry"
    # Links for join_geometry_007
    links.new(join_geometry_007.outputs[0], geometry_proximity.inputs[0])
    links.new(separate_geometry.outputs[0], join_geometry_007.inputs[0])
    links.new(fill_curve.outputs[0], join_geometry_007.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.name = "Set Shade Smooth.001"
    set_shade_smooth_001.label = ""
    set_shade_smooth_001.location = (3390.0, -332.0)
    set_shade_smooth_001.bl_label = "Set Shade Smooth"
    set_shade_smooth_001.domain = "FACE"
    # Selection
    set_shade_smooth_001.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_001.inputs[2].default_value = True
    # Links for set_shade_smooth_001
    links.new(join_geometry_006.outputs[0], set_shade_smooth_001.inputs[0])

    set_shade_smooth_002 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_002.name = "Set Shade Smooth.002"
    set_shade_smooth_002.label = ""
    set_shade_smooth_002.location = (3570.0, -332.0)
    set_shade_smooth_002.bl_label = "Set Shade Smooth"
    set_shade_smooth_002.domain = "EDGE"
    # Shade Smooth
    set_shade_smooth_002.inputs[2].default_value = False
    # Links for set_shade_smooth_002
    links.new(set_shade_smooth_001.outputs[0], set_shade_smooth_002.inputs[0])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.label = ""
    compare_004.location = (3390.0, -452.0)
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
    links.new(geometry_proximity.outputs[1], compare_004.inputs[0])
    links.new(compare_004.outputs[0], set_shade_smooth_002.inputs[1])

    frame_004 = nodes.new("NodeFrame")
    frame_004.name = "Frame.004"
    frame_004.label = "Gambeson Pattern"
    frame_004.location = (30.0, -920.0)
    frame_004.bl_label = "Frame"
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20
    # Links for frame_004

    sample_u_v_surface = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface.name = "Sample UV Surface"
    sample_u_v_surface.label = ""
    sample_u_v_surface.location = (4751.1298828125, -692.0)
    sample_u_v_surface.bl_label = "Sample UV Surface"
    sample_u_v_surface.data_type = "FLOAT_VECTOR"
    # Links for sample_u_v_surface

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.label = ""
    capture_attribute.location = (910.0, -576.0)
    capture_attribute.bl_label = "Capture Attribute"
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    # Links for capture_attribute
    links.new(capture_attribute.outputs[0], curve_to_mesh_002.inputs[1])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.label = ""
    capture_attribute_001.location = (910.0, -376.0)
    capture_attribute_001.bl_label = "Capture Attribute"
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "POINT"
    # Links for capture_attribute_001
    links.new(capture_attribute_001.outputs[0], curve_to_mesh_002.inputs[0])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"
    spline_parameter_002.label = ""
    spline_parameter_002.location = (450.0, -356.0)
    spline_parameter_002.bl_label = "Spline Parameter"
    # Links for spline_parameter_002
    links.new(spline_parameter_002.outputs[0], capture_attribute_001.inputs[1])
    links.new(spline_parameter_002.outputs[0], capture_attribute.inputs[1])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.name = "Combine XYZ.001"
    combine_x_y_z_001.label = ""
    combine_x_y_z_001.location = (1170.0, -576.0)
    combine_x_y_z_001.bl_label = "Combine XYZ"
    # Z
    combine_x_y_z_001.inputs[2].default_value = 0.0
    # Links for combine_x_y_z_001
    links.new(capture_attribute_001.outputs[1], combine_x_y_z_001.inputs[1])
    links.new(capture_attribute.outputs[1], combine_x_y_z_001.inputs[0])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    set_spline_cyclic.label = ""
    set_spline_cyclic.location = (650.0, -516.0)
    set_spline_cyclic.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = False
    # Links for set_spline_cyclic
    links.new(set_spline_cyclic.outputs[0], capture_attribute.inputs[0])
    links.new(curve_circle_002.outputs[0], set_spline_cyclic.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    set_curve_tilt.label = ""
    set_curve_tilt.location = (650.0, -236.0)
    set_curve_tilt.bl_label = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Tilt
    set_curve_tilt.inputs[2].default_value = -1.472708821296692
    # Links for set_curve_tilt
    links.new(set_curve_tilt.outputs[0], capture_attribute_001.inputs[0])
    links.new(resample_curve_001.outputs[0], set_curve_tilt.inputs[0])

    position_005 = nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"
    position_005.label = ""
    position_005.location = (4500.0, -652.0)
    position_005.bl_label = "Position"
    # Links for position_005
    links.new(position_005.outputs[0], sample_u_v_surface.inputs[1])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    set_position_003.label = ""
    set_position_003.location = (5631.1298828125, -892.0)
    set_position_003.bl_label = "Set Position"
    # Selection
    set_position_003.inputs[1].default_value = True
    # Links for set_position_003
    links.new(set_position_003.outputs[0], set_position_001.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    bounding_box.label = ""
    bounding_box.location = (281.1298828125, -96.0)
    bounding_box.bl_label = "Bounding Box"
    # Use Radius
    bounding_box.inputs[1].default_value = False
    # Links for bounding_box

    position_006 = nodes.new("GeometryNodeInputPosition")
    position_006.name = "Position.006"
    position_006.label = ""
    position_006.location = (30.0, -36.0)
    position_006.bl_label = "Position"
    # Links for position_006

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.label = ""
    map_range_001.location = (481.1298828125, -36.0)
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
    map_range_001.inputs[9].default_value = [0.009999999776482582, 0.009999999776482582, 0.009999999776482582]
    # To Max
    map_range_001.inputs[10].default_value = [0.9900000095367432, 0.9900000095367432, 0.9900000095367432]
    # Steps
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    # Links for map_range_001
    links.new(position_006.outputs[0], map_range_001.inputs[6])
    links.new(bounding_box.outputs[1], map_range_001.inputs[7])
    links.new(bounding_box.outputs[2], map_range_001.inputs[8])
    links.new(map_range_001.outputs[1], sample_u_v_surface.inputs[3])

    sample_u_v_surface_001 = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface_001.name = "Sample UV Surface.001"
    sample_u_v_surface_001.label = ""
    sample_u_v_surface_001.location = (4751.1298828125, -792.0)
    sample_u_v_surface_001.bl_label = "Sample UV Surface"
    sample_u_v_surface_001.data_type = "FLOAT_VECTOR"
    # Links for sample_u_v_surface_001
    links.new(map_range_001.outputs[1], sample_u_v_surface_001.inputs[3])

    normal_003 = nodes.new("GeometryNodeInputNormal")
    normal_003.name = "Normal.003"
    normal_003.label = ""
    normal_003.location = (4500.0, -752.0)
    normal_003.bl_label = "Normal"
    normal_003.legacy_corner_normals = False
    # Links for normal_003
    links.new(normal_003.outputs[0], sample_u_v_surface_001.inputs[1])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_003.name = "Separate XYZ.003"
    separate_x_y_z_003.label = ""
    separate_x_y_z_003.location = (30.0, -80.0)
    separate_x_y_z_003.bl_label = "Separate XYZ"
    # Links for separate_x_y_z_003
    links.new(position_006.outputs[0], separate_x_y_z_003.inputs[0])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.label = ""
    vector_math_004.location = (441.1298828125, -40.0)
    vector_math_004.bl_label = "Vector Math"
    vector_math_004.operation = "SCALE"
    # Vector
    vector_math_004.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Links for vector_math_004
    links.new(vector_math_004.outputs[0], set_position_003.inputs[3])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.label = ""
    math_005.location = (190.0, -80.0)
    math_005.bl_label = "Math"
    math_005.operation = "MULTIPLY"
    math_005.use_clamp = False
    # Value
    math_005.inputs[1].default_value = 1.2499998807907104
    # Value
    math_005.inputs[2].default_value = 0.5
    # Links for math_005
    links.new(separate_x_y_z_003.outputs[2], math_005.inputs[0])
    links.new(math_005.outputs[0], vector_math_004.inputs[3])

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.name = "Capture Attribute.002"
    capture_attribute_002.label = ""
    capture_attribute_002.location = (5091.1298828125, -952.0)
    capture_attribute_002.bl_label = "Capture Attribute"
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "POINT"
    # Links for capture_attribute_002
    links.new(sample_u_v_surface_001.outputs[0], capture_attribute_002.inputs[2])
    links.new(capture_attribute_002.outputs[2], vector_math_004.inputs[0])
    links.new(map_range_001.outputs[1], capture_attribute_002.inputs[3])
    links.new(capture_attribute_002.outputs[3], vector_math_003.inputs[0])
    links.new(sample_u_v_surface.outputs[0], capture_attribute_002.inputs[1])
    links.new(capture_attribute_002.outputs[1], set_position_003.inputs[2])

    noise_texture_002 = nodes.new("ShaderNodeTexNoise")
    noise_texture_002.name = "Noise Texture.002"
    noise_texture_002.label = ""
    noise_texture_002.location = (30.0, -656.0)
    noise_texture_002.bl_label = "Noise Texture"
    noise_texture_002.noise_dimensions = "4D"
    noise_texture_002.noise_type = "FBM"
    noise_texture_002.normalize = False
    # Vector
    noise_texture_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    # W
    noise_texture_002.inputs[1].default_value = 44.769989013671875
    # Scale
    noise_texture_002.inputs[2].default_value = 17.969999313354492
    # Detail
    noise_texture_002.inputs[3].default_value = 0.0
    # Roughness
    noise_texture_002.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture_002.inputs[5].default_value = 2.0
    # Offset
    noise_texture_002.inputs[6].default_value = 0.0
    # Gain
    noise_texture_002.inputs[7].default_value = 1.0
    # Distortion
    noise_texture_002.inputs[8].default_value = 0.0
    # Links for noise_texture_002

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.label = ""
    vector_math_006.location = (841.1298828125, -256.0)
    vector_math_006.bl_label = "Vector Math"
    vector_math_006.operation = "ADD"
    # Vector
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_006.inputs[3].default_value = 1.0
    # Links for vector_math_006
    links.new(vector_math_006.outputs[0], set_position_001.inputs[3])
    links.new(vector_math_002.outputs[0], vector_math_006.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.label = ""
    vector_math_005.location = (410.0, -536.0)
    vector_math_005.bl_label = "Vector Math"
    vector_math_005.operation = "SCALE"
    # Vector
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    # Vector
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Scale
    vector_math_005.inputs[3].default_value = 0.006000000052154064
    # Links for vector_math_005
    links.new(noise_texture_002.outputs[1], vector_math_005.inputs[0])
    links.new(vector_math_005.outputs[0], vector_math_006.inputs[1])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.label = ""
    store_named_attribute_001.location = (7171.1298828125, -712.0)
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
    links.new(store_named_attribute_001.outputs[0], store_named_attribute.inputs[0])

    frame_005 = nodes.new("NodeFrame")
    frame_005.name = "Frame.005"
    frame_005.label = "Thickness"
    frame_005.location = (4950.0, -1212.0)
    frame_005.bl_label = "Frame"
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20
    # Links for frame_005

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.label = ""
    reroute_001.location = (4420.0, -712.0)
    reroute_001.bl_label = "Reroute"
    reroute_001.socket_idname = "NodeSocketVector"
    # Links for reroute_001
    links.new(reroute_001.outputs[0], sample_u_v_surface.inputs[2])
    links.new(reroute_001.outputs[0], sample_u_v_surface_001.inputs[2])
    links.new(combine_x_y_z_001.outputs[0], reroute_001.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.label = ""
    reroute_002.location = (4420.0, -672.0)
    reroute_002.bl_label = "Reroute"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Links for reroute_002
    links.new(reroute_002.outputs[0], sample_u_v_surface.inputs[0])
    links.new(reroute_002.outputs[0], sample_u_v_surface_001.inputs[0])
    links.new(curve_to_mesh_002.outputs[0], reroute_002.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.name = "Frame.006"
    frame_006.label = "UVMap"
    frame_006.location = (4130.0, -896.0)
    frame_006.bl_label = "Frame"
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20
    # Links for frame_006

    frame_007 = nodes.new("NodeFrame")
    frame_007.name = "Frame.007"
    frame_007.label = "General Collar Shape"
    frame_007.location = (2850.0, -36.0)
    frame_007.bl_label = "Frame"
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20
    # Links for frame_007

    frame_008 = nodes.new("NodeFrame")
    frame_008.name = "Frame.008"
    frame_008.label = "Displacement"
    frame_008.location = (5730.0, -836.0)
    frame_008.bl_label = "Frame"
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20
    # Links for frame_008

    frame_009 = nodes.new("NodeFrame")
    frame_009.name = "Frame.009"
    frame_009.label = "Collar"
    frame_009.location = (-6800.0, -428.0)
    frame_009.bl_label = "Frame"
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20
    # Links for frame_009

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.label = ""
    store_named_attribute_002.location = (5351.1298828125, -812.0)
    store_named_attribute_002.bl_label = "Store Named Attribute"
    store_named_attribute_002.data_type = "FLOAT2"
    store_named_attribute_002.domain = "CORNER"
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "UVMap"
    # Links for store_named_attribute_002
    links.new(store_named_attribute_002.outputs[0], set_position_003.inputs[0])
    links.new(capture_attribute_002.outputs[0], store_named_attribute_002.inputs[0])
    links.new(capture_attribute_002.outputs[3], store_named_attribute_002.inputs[3])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.label = ""
    switch_001.location = (7011.1298828125, -712.0)
    switch_001.bl_label = "Switch"
    switch_001.input_type = "GEOMETRY"
    # Links for switch_001
    links.new(switch_001.outputs[0], store_named_attribute_001.inputs[0])
    links.new(set_position_001.outputs[0], switch_001.inputs[2])

    group_input_001 = nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.label = ""
    group_input_001.location = (6760.0, -632.0)
    group_input_001.bl_label = "Group Input"
    # Links for group_input_001
    links.new(group_input_001.outputs[0], switch_001.inputs[0])

    curve_to_mesh_004 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_004.name = "Curve to Mesh.004"
    curve_to_mesh_004.label = ""
    curve_to_mesh_004.location = (1170.0, -196.0)
    curve_to_mesh_004.bl_label = "Curve to Mesh"
    # Fill Caps
    curve_to_mesh_004.inputs[3].default_value = False
    # Links for curve_to_mesh_004
    links.new(curve_to_mesh_004.outputs[0], switch_001.inputs[1])
    links.new(set_curve_tilt.outputs[0], curve_to_mesh_004.inputs[0])
    links.new(float_curve_001.outputs[0], curve_to_mesh_004.inputs[2])

    curve_circle_004 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_004.name = "Curve Circle.004"
    curve_circle_004.label = ""
    curve_circle_004.location = (710.0, -36.0)
    curve_circle_004.bl_label = "Curve Circle"
    curve_circle_004.mode = "RADIUS"
    # Resolution
    curve_circle_004.inputs[0].default_value = 24
    # Point 1
    curve_circle_004.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    # Point 2
    curve_circle_004.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    # Point 3
    curve_circle_004.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    # Radius
    curve_circle_004.inputs[4].default_value = 0.10000000149011612
    # Links for curve_circle_004

    set_spline_cyclic_001 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_001.name = "Set Spline Cyclic.001"
    set_spline_cyclic_001.label = ""
    set_spline_cyclic_001.location = (890.0, -56.0)
    set_spline_cyclic_001.bl_label = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic_001.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic_001.inputs[2].default_value = False
    # Links for set_spline_cyclic_001
    links.new(curve_circle_004.outputs[0], set_spline_cyclic_001.inputs[0])
    links.new(set_spline_cyclic_001.outputs[0], curve_to_mesh_004.inputs[1])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.label = ""
    mesh_to_curve.location = (570.0, -56.0)
    mesh_to_curve.bl_label = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    # Selection
    mesh_to_curve.inputs[1].default_value = True
    # Links for mesh_to_curve

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.label = ""
    resample_curve.location = (1190.0, -36.0)
    resample_curve.bl_label = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = "Length"
    # Count
    resample_curve.inputs[3].default_value = 101
    # Length
    resample_curve.inputs[4].default_value = 0.003000000026077032
    # Links for resample_curve

    subdivide_mesh_001 = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh_001.name = "Subdivide Mesh.001"
    subdivide_mesh_001.label = ""
    subdivide_mesh_001.location = (30.0, -136.0)
    subdivide_mesh_001.bl_label = "Subdivide Mesh"
    # Level
    subdivide_mesh_001.inputs[1].default_value = 4
    # Links for subdivide_mesh_001
    links.new(separate_geometry.outputs[0], subdivide_mesh_001.inputs[0])

    geometry_proximity_002 = nodes.new("GeometryNodeProximity")
    geometry_proximity_002.name = "Geometry Proximity.002"
    geometry_proximity_002.label = ""
    geometry_proximity_002.location = (30.0, -216.0)
    geometry_proximity_002.bl_label = "Geometry Proximity"
    geometry_proximity_002.target_element = "FACES"
    # Group ID
    geometry_proximity_002.inputs[1].default_value = 0
    # Sample Position
    geometry_proximity_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    # Sample Group ID
    geometry_proximity_002.inputs[3].default_value = 0
    # Links for geometry_proximity_002
    links.new(fill_curve.outputs[0], geometry_proximity_002.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.label = ""
    compare.location = (190.0, -216.0)
    compare.bl_label = "Compare"
    compare.operation = "GREATER_THAN"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    # B
    compare.inputs[1].default_value = 0.0010000000474974513
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
    links.new(geometry_proximity_002.outputs[1], compare.inputs[0])

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.label = ""
    delete_geometry.location = (410.0, -56.0)
    delete_geometry.bl_label = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "POINT"
    # Links for delete_geometry
    links.new(delete_geometry.outputs[0], mesh_to_curve.inputs[0])
    links.new(subdivide_mesh_001.outputs[0], delete_geometry.inputs[0])
    links.new(compare.outputs[0], delete_geometry.inputs[1])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    instance_on_points_001.label = ""
    instance_on_points_001.location = (1390.0, -36.0)
    instance_on_points_001.bl_label = "Instance on Points"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0
    # Links for instance_on_points_001
    links.new(resample_curve.outputs[0], instance_on_points_001.inputs[0])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.label = ""
    align_rotation_to_vector_001.location = (1190.0, -156.0)
    align_rotation_to_vector_001.bl_label = "Align Rotation to Vector"
    align_rotation_to_vector_001.axis = "X"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    # Rotation
    align_rotation_to_vector_001.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    # Links for align_rotation_to_vector_001
    links.new(align_rotation_to_vector_001.outputs[0], instance_on_points_001.inputs[5])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"
    curve_tangent.label = ""
    curve_tangent.location = (1010.0, -196.0)
    curve_tangent.bl_label = "Curve Tangent"
    # Links for curve_tangent
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_001.inputs[2])

    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.name = "Ico Sphere.001"
    ico_sphere_001.label = ""
    ico_sphere_001.location = (990.0, -296.0)
    ico_sphere_001.bl_label = "Ico Sphere"
    # Radius
    ico_sphere_001.inputs[0].default_value = 0.0007999999797903001
    # Subdivisions
    ico_sphere_001.inputs[1].default_value = 2
    # Links for ico_sphere_001

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    transform_geometry_004.label = ""
    transform_geometry_004.location = (1190.0, -316.0)
    transform_geometry_004.bl_label = "Transform Geometry"
    # Mode
    transform_geometry_004.inputs[1].default_value = "Components"
    # Translation
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    # Rotation
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    # Scale
    transform_geometry_004.inputs[4].default_value = Vector((1.5, 0.5, 0.3199999928474426))
    # Links for transform_geometry_004
    links.new(transform_geometry_004.outputs[0], instance_on_points_001.inputs[2])
    links.new(ico_sphere_001.outputs[0], transform_geometry_004.inputs[0])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    realize_instances_001.label = ""
    realize_instances_001.location = (1570.0, -36.0)
    realize_instances_001.bl_label = "Realize Instances"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0
    # Links for realize_instances_001
    links.new(instance_on_points_001.outputs[0], realize_instances_001.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.label = ""
    set_position.location = (1170.0, -196.0)
    set_position.bl_label = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    # Links for set_position
    links.new(transform_geometry_002.outputs[0], set_position.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    position.label = ""
    position.location = (30.0, -536.0)
    position.bl_label = "Position"
    # Links for position

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z.name = "Separate XYZ"
    separate_x_y_z.label = ""
    separate_x_y_z.location = (190.0, -536.0)
    separate_x_y_z.bl_label = "Separate XYZ"
    # Links for separate_x_y_z
    links.new(position.outputs[0], separate_x_y_z.inputs[0])

    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.name = "Map Range.002"
    map_range_002.label = ""
    map_range_002.location = (350.0, -536.0)
    map_range_002.bl_label = "Map Range"
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    # From Min
    map_range_002.inputs[1].default_value = -0.004999999888241291
    # From Max
    map_range_002.inputs[2].default_value = 0.004999999888241291
    # To Min
    map_range_002.inputs[3].default_value = 0.0
    # To Max
    map_range_002.inputs[4].default_value = 1.0
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
    links.new(separate_x_y_z.outputs[0], map_range_002.inputs[0])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.name = "Float Curve"
    float_curve.label = ""
    float_curve.location = (530.0, -536.0)
    float_curve.bl_label = "Float Curve"
    # Factor
    float_curve.inputs[0].default_value = 1.0
    # Links for float_curve
    links.new(map_range_002.outputs[0], float_curve.inputs[1])

    math = nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.label = ""
    math.location = (790.0, -536.0)
    math.bl_label = "Math"
    math.operation = "MULTIPLY"
    math.use_clamp = False
    # Value
    math.inputs[2].default_value = 0.5
    # Links for math
    links.new(separate_x_y_z.outputs[1], math.inputs[0])
    links.new(float_curve.outputs[0], math.inputs[1])

    combine_x_y_z_002 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_002.name = "Combine XYZ.002"
    combine_x_y_z_002.label = ""
    combine_x_y_z_002.location = (950.0, -536.0)
    combine_x_y_z_002.bl_label = "Combine XYZ"
    # Links for combine_x_y_z_002
    links.new(separate_x_y_z.outputs[0], combine_x_y_z_002.inputs[0])
    links.new(math.outputs[0], combine_x_y_z_002.inputs[1])
    links.new(separate_x_y_z.outputs[2], combine_x_y_z_002.inputs[2])
    links.new(combine_x_y_z_002.outputs[0], set_position.inputs[2])

    capture_attribute_003 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.name = "Capture Attribute.003"
    capture_attribute_003.label = ""
    capture_attribute_003.location = (1350.0, -196.0)
    capture_attribute_003.bl_label = "Capture Attribute"
    capture_attribute_003.active_index = 0
    capture_attribute_003.domain = "POINT"
    # Links for capture_attribute_003
    links.new(capture_attribute_003.outputs[0], curve_to_mesh_003.inputs[1])
    links.new(set_position.outputs[0], capture_attribute_003.inputs[0])

    index_001 = nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"
    index_001.label = ""
    index_001.location = (1170.0, -396.0)
    index_001.bl_label = "Index"
    # Links for index_001

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.label = ""
    compare_002.location = (1350.0, -436.0)
    compare_002.bl_label = "Compare"
    compare_002.operation = "EQUAL"
    compare_002.data_type = "INT"
    compare_002.mode = "ELEMENT"
    # A
    compare_002.inputs[0].default_value = 0.0
    # B
    compare_002.inputs[1].default_value = 0.0
    # B
    compare_002.inputs[3].default_value = 39
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
    links.new(index_001.outputs[0], compare_002.inputs[2])
    links.new(compare_002.outputs[0], capture_attribute_003.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.label = ""
    mesh_to_curve_001.location = (1730.0, -96.0)
    mesh_to_curve_001.bl_label = "Mesh to Curve"
    mesh_to_curve_001.mode = "EDGES"
    # Links for mesh_to_curve_001
    links.new(curve_to_mesh_003.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(capture_attribute_003.outputs[1], mesh_to_curve_001.inputs[1])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.label = ""
    join_geometry_001.location = (830.0, -76.0)
    join_geometry_001.bl_label = "Join Geometry"
    # Links for join_geometry_001
    links.new(mesh_to_curve_001.outputs[0], join_geometry_001.inputs[0])
    links.new(mesh_to_curve.outputs[0], join_geometry_001.inputs[0])
    links.new(join_geometry_001.outputs[0], resample_curve.inputs[0])

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_008.name = "Join Geometry.008"
    join_geometry_008.label = ""
    join_geometry_008.location = (3570.0, -1492.0)
    join_geometry_008.bl_label = "Join Geometry"
    # Links for join_geometry_008

    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.name = "Set Shade Smooth.003"
    set_shade_smooth_003.label = ""
    set_shade_smooth_003.location = (3390.0, -612.0)
    set_shade_smooth_003.bl_label = "Set Shade Smooth"
    set_shade_smooth_003.domain = "FACE"
    # Selection
    set_shade_smooth_003.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_003.inputs[2].default_value = True
    # Links for set_shade_smooth_003
    links.new(join_geometry_008.outputs[0], set_shade_smooth_003.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    join_geometry_009.name = "Join Geometry.009"
    join_geometry_009.label = ""
    join_geometry_009.location = (3750.0, -372.0)
    join_geometry_009.bl_label = "Join Geometry"
    # Links for join_geometry_009
    links.new(join_geometry_009.outputs[0], bounding_box.inputs[0])
    links.new(join_geometry_009.outputs[0], capture_attribute_002.inputs[0])
    links.new(set_shade_smooth_002.outputs[0], join_geometry_009.inputs[0])
    links.new(set_shade_smooth_003.outputs[0], join_geometry_009.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.name = "Frame"
    frame.label = "Stitching"
    frame.location = (1200.0, -876.0)
    frame.bl_label = "Frame"
    frame.text = None
    frame.shrink = True
    frame.label_size = 20
    # Links for frame

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.label = ""
    store_named_attribute_003.location = (1750.0, -36.0)
    store_named_attribute_003.bl_label = "Store Named Attribute"
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "stitching"
    # Value
    store_named_attribute_003.inputs[3].default_value = True
    # Links for store_named_attribute_003
    links.new(store_named_attribute_003.outputs[0], join_geometry_008.inputs[0])
    links.new(realize_instances_001.outputs[0], store_named_attribute_003.inputs[0])

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.label = ""
    store_named_attribute_004.location = (3190.0, -1492.0)
    store_named_attribute_004.bl_label = "Store Named Attribute"
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "piping"
    # Value
    store_named_attribute_004.inputs[3].default_value = True
    # Links for store_named_attribute_004
    links.new(store_named_attribute_004.outputs[0], join_geometry_008.inputs[0])
    links.new(curve_to_mesh_003.outputs[0], store_named_attribute_004.inputs[0])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.label = ""
    random_value_001.location = (1390.0, -296.0)
    random_value_001.bl_label = "Random Value"
    random_value_001.data_type = "FLOAT_VECTOR"
    # Min
    random_value_001.inputs[0].default_value = [0.699999988079071, 0.699999988079071, 0.699999988079071]
    # Max
    random_value_001.inputs[1].default_value = [1.0, 1.5, 1.2999999523162842]
    # Min
    random_value_001.inputs[2].default_value = 0.0
    # Max
    random_value_001.inputs[3].default_value = 1.0
    # Min
    random_value_001.inputs[4].default_value = 0
    # Max
    random_value_001.inputs[5].default_value = 100
    # Probability
    random_value_001.inputs[6].default_value = 0.5
    # ID
    random_value_001.inputs[7].default_value = 0
    # Seed
    random_value_001.inputs[8].default_value = 0
    # Links for random_value_001
    links.new(random_value_001.outputs[0], instance_on_points_001.inputs[6])

    auto_layout_nodes(group)
    return group
