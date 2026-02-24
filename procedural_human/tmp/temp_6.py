import bpy
import mathutils
import os
import typing


def blocker_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Blocker node group"""
    blocker_1 = bpy.data.node_groups.new(type='GeometryNodeTree', name="Blocker")

    blocker_1.color_tag = 'NONE'
    blocker_1.description = ""
    blocker_1.default_group_node_width = 140
    blocker_1.show_modifier_manage_panel = True

    # blocker_1 interface

    # Socket Geometry
    geometry_socket = blocker_1.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'
    geometry_socket.default_input = 'VALUE'
    geometry_socket.structure_type = 'AUTO'

    # Socket Decor
    decor_socket = blocker_1.interface.new_socket(name="Decor", in_out='INPUT', socket_type='NodeSocketBool')
    decor_socket.default_value = False
    decor_socket.attribute_domain = 'POINT'
    decor_socket.default_input = 'VALUE'
    decor_socket.structure_type = 'AUTO'

    # Initialize blocker_1 nodes

    # Node Group Output
    group_output = blocker_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Join Geometry
    join_geometry = blocker_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"

    # Node Set Shade Smooth
    set_shade_smooth = blocker_1.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.domain = 'FACE'
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = True

    # Node Store Named Attribute
    store_named_attribute = blocker_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'BOOLEAN'
    store_named_attribute.domain = 'POINT'
    # Selection
    store_named_attribute.inputs[1].default_value = True
    # Name
    store_named_attribute.inputs[2].default_value = "blocker"
    # Value
    store_named_attribute.inputs[3].default_value = True

    # Node Ico Sphere
    ico_sphere = blocker_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.name = "Ico Sphere"
    # Radius
    ico_sphere.inputs[0].default_value = 0.1300000250339508
    # Subdivisions
    ico_sphere.inputs[1].default_value = 3

    # Node Transform Geometry
    transform_geometry = blocker_1.nodes.new("GeometryNodeTransform")
    transform_geometry.name = "Transform Geometry"
    # Mode
    transform_geometry.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry.inputs[2].default_value = (-0.03999999910593033, 0.0, 0.25)
    # Rotation
    transform_geometry.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry.inputs[4].default_value = (1.0, 1.0, 1.2000000476837158)

    # Node Frame.001
    frame_001 = blocker_1.nodes.new("NodeFrame")
    frame_001.label = "Chest"
    frame_001.name = "Frame.001"
    frame_001.label_size = 20
    frame_001.shrink = True

    # Node Transform Geometry.001
    transform_geometry_001 = blocker_1.nodes.new("GeometryNodeTransform")
    transform_geometry_001.name = "Transform Geometry.001"
    # Mode
    transform_geometry_001.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_001.inputs[2].default_value = (-0.10000000149011612, 0.019999999552965164, 0.33000001311302185)
    # Rotation
    transform_geometry_001.inputs[3].default_value = (0.0, -0.13439033925533295, 0.18500488996505737)
    # Scale
    transform_geometry_001.inputs[4].default_value = (1.0199999809265137, 0.8300000429153442, 0.8400001525878906)

    # Node Mesh to SDF Grid
    mesh_to_sdf_grid = blocker_1.nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_sdf_grid.name = "Mesh to SDF Grid"
    # Voxel Size
    mesh_to_sdf_grid.inputs[1].default_value = 0.004999999888241291
    # Band Width
    mesh_to_sdf_grid.inputs[2].default_value = 2

    # Node Mesh to SDF Grid.001
    mesh_to_sdf_grid_001 = blocker_1.nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_sdf_grid_001.name = "Mesh to SDF Grid.001"
    # Voxel Size
    mesh_to_sdf_grid_001.inputs[1].default_value = 0.004999999888241291
    # Band Width
    mesh_to_sdf_grid_001.inputs[2].default_value = 2

    # Node SDF Grid Boolean
    sdf_grid_boolean = blocker_1.nodes.new("GeometryNodeSDFGridBoolean")
    sdf_grid_boolean.name = "SDF Grid Boolean"
    sdf_grid_boolean.operation = 'UNION'

    # Node Grid to Mesh
    grid_to_mesh = blocker_1.nodes.new("GeometryNodeGridToMesh")
    grid_to_mesh.name = "Grid to Mesh"
    # Threshold
    grid_to_mesh.inputs[1].default_value = 0.0
    # Adaptivity
    grid_to_mesh.inputs[2].default_value = 0.0

    # Node SDF Grid Fillet
    sdf_grid_fillet = blocker_1.nodes.new("GeometryNodeSDFGridFillet")
    sdf_grid_fillet.name = "SDF Grid Fillet"
    # Iterations
    sdf_grid_fillet.inputs[1].default_value = 3

    # Node Instance on Points
    instance_on_points = blocker_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    # Pick Instance
    instance_on_points.inputs[3].default_value = False
    # Instance Index
    instance_on_points.inputs[4].default_value = 0
    # Scale
    instance_on_points.inputs[6].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929)

    # Node Curve Circle.001
    curve_circle_001 = blocker_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.name = "Curve Circle.001"
    curve_circle_001.mode = 'RADIUS'
    # Resolution
    curve_circle_001.inputs[0].default_value = 9
    # Radius
    curve_circle_001.inputs[4].default_value = 0.004999999888241291

    # Node Curve to Mesh.001
    curve_to_mesh_001 = blocker_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.name = "Curve to Mesh.001"
    # Scale
    curve_to_mesh_001.inputs[2].default_value = 0.21000000834465027
    # Fill Caps
    curve_to_mesh_001.inputs[3].default_value = False

    # Node Position.002
    position_002 = blocker_1.nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"

    # Node Separate XYZ.001
    separate_xyz_001 = blocker_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_001.name = "Separate XYZ.001"
    separate_xyz_001.outputs[1].hide = True
    separate_xyz_001.outputs[2].hide = True

    # Node Compare.001
    compare_001 = blocker_1.nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.data_type = 'FLOAT'
    compare_001.mode = 'ELEMENT'
    compare_001.operation = 'LESS_THAN'
    # B
    compare_001.inputs[1].default_value = -0.09999999403953552

    # Node Align Rotation to Vector
    align_rotation_to_vector = blocker_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.name = "Align Rotation to Vector"
    align_rotation_to_vector.axis = 'Z'
    align_rotation_to_vector.pivot_axis = 'AUTO'
    # Rotation
    align_rotation_to_vector.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Factor
    align_rotation_to_vector.inputs[1].default_value = 1.0

    # Node Normal.001
    normal_001 = blocker_1.nodes.new("GeometryNodeInputNormal")
    normal_001.name = "Normal.001"
    normal_001.legacy_corner_normals = False

    # Node Rotate Rotation
    rotate_rotation = blocker_1.nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.name = "Rotate Rotation"
    rotate_rotation.rotation_space = 'LOCAL'
    # Rotate By
    rotate_rotation.inputs[1].default_value = (-0.3707079291343689, 0.3525564670562744, 0.0)

    # Node Rotate Rotation.001
    rotate_rotation_001 = blocker_1.nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.name = "Rotate Rotation.001"
    rotate_rotation_001.rotation_space = 'LOCAL'

    # Node Random Value
    random_value = blocker_1.nodes.new("FunctionNodeRandomValue")
    random_value.name = "Random Value"
    random_value.hide = True
    random_value.data_type = 'FLOAT_VECTOR'
    # Min
    random_value.inputs[0].default_value = (-0.10000000149011612, -0.10000000149011612, -0.10000000149011612)
    # Max
    random_value.inputs[1].default_value = (0.10000000149011612, 0.10000000149011612, 0.10000000149011612)
    # ID
    random_value.inputs[7].default_value = 0
    # Seed
    random_value.inputs[8].default_value = 2

    # Node Realize Instances
    realize_instances = blocker_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Realize All
    realize_instances.inputs[2].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 0

    # Node Switch
    switch = blocker_1.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'GEOMETRY'

    # Node Join Geometry.002
    join_geometry_002 = blocker_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"

    # Node Reroute
    reroute = blocker_1.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    # Node Group Input
    group_input = blocker_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[1].hide = True

    # Node Curve to Mesh.002
    curve_to_mesh_002 = blocker_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.name = "Curve to Mesh.002"
    # Fill Caps
    curve_to_mesh_002.inputs[3].default_value = False

    # Node Curve Circle.002
    curve_circle_002 = blocker_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_002.name = "Curve Circle.002"
    curve_circle_002.mode = 'RADIUS'
    # Resolution
    curve_circle_002.inputs[0].default_value = 105
    # Radius
    curve_circle_002.inputs[4].default_value = 0.10000000149011612

    # Node Spline Parameter.001
    spline_parameter_001 = blocker_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"
    spline_parameter_001.outputs[1].hide = True
    spline_parameter_001.outputs[2].hide = True

    # Node Float Curve.001
    float_curve_001 = blocker_1.nodes.new("ShaderNodeFloatCurve")
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
    float_curve_001_curve_0_point_0.location = (0.0, 0.7650688290596008)
    float_curve_001_curve_0_point_0.handle_type = 'AUTO'
    float_curve_001_curve_0_point_1 = float_curve_001_curve_0.points[1]
    float_curve_001_curve_0_point_1.location = (0.46223577857017517, 0.6594827175140381)
    float_curve_001_curve_0_point_1.handle_type = 'AUTO'
    float_curve_001_curve_0_point_2 = float_curve_001_curve_0.points.new(0.8187312483787537, 0.7587241530418396)
    float_curve_001_curve_0_point_2.handle_type = 'AUTO'
    float_curve_001_curve_0_point_3 = float_curve_001_curve_0.points.new(1.0, 0.7294828295707703)
    float_curve_001_curve_0_point_3.handle_type = 'AUTO'
    # Update curve after changes
    float_curve_001.mapping.update()
    # Factor
    float_curve_001.inputs[0].default_value = 1.0

    # Node Resample Curve.001
    resample_curve_001 = blocker_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.keep_last_segment = True
    # Selection
    resample_curve_001.inputs[1].default_value = True
    # Mode
    resample_curve_001.inputs[2].default_value = 'Count'
    # Count
    resample_curve_001.inputs[3].default_value = 34
    # Length
    resample_curve_001.inputs[4].default_value = 0.10000000149011612

    # Node Quadratic Bézier.001
    quadratic_b_zier_001 = blocker_1.nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_b_zier_001.name = "Quadratic Bézier.001"
    # Resolution
    quadratic_b_zier_001.inputs[0].default_value = 16
    # Start
    quadratic_b_zier_001.inputs[1].default_value = (0.0, -0.009999999776482582, 0.4000000059604645)
    # Middle
    quadratic_b_zier_001.inputs[2].default_value = (0.0, 0.009999999776482582, 0.44999995827674866)
    # End
    quadratic_b_zier_001.inputs[3].default_value = (0.0, -0.04999999701976776, 0.5199999809265137)

    # Node Set Position.001
    set_position_001 = blocker_1.nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    # Selection
    set_position_001.inputs[1].default_value = True
    # Position
    set_position_001.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Vector Math.002
    vector_math_002 = blocker_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'SCALE'
    # Scale
    vector_math_002.inputs[3].default_value = 0.0020000000949949026

    # Node Noise Texture.001
    noise_texture_001 = blocker_1.nodes.new("ShaderNodeTexNoise")
    noise_texture_001.name = "Noise Texture.001"
    noise_texture_001.noise_dimensions = '2D'
    noise_texture_001.noise_type = 'FBM'
    noise_texture_001.normalize = False
    # Scale
    noise_texture_001.inputs[2].default_value = 5.669999599456787
    # Detail
    noise_texture_001.inputs[3].default_value = 0.0
    # Roughness
    noise_texture_001.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture_001.inputs[5].default_value = 2.0
    # Distortion
    noise_texture_001.inputs[8].default_value = 0.0

    # Node Vector Math.003
    vector_math_003 = blocker_1.nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.operation = 'MULTIPLY'
    # Vector_001
    vector_math_003.inputs[1].default_value = (1.0, 2.5999999046325684, 24.950000762939453)

    # Node Quadrilateral
    quadrilateral = blocker_1.nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
    quadrilateral.name = "Quadrilateral"
    quadrilateral.mode = 'RECTANGLE'
    # Width
    quadrilateral.inputs[0].default_value = 0.5
    # Height
    quadrilateral.inputs[1].default_value = 0.15000000596046448

    # Node Fillet Curve
    fillet_curve = blocker_1.nodes.new("GeometryNodeFilletCurve")
    fillet_curve.name = "Fillet Curve"
    # Limit Radius
    fillet_curve.inputs[2].default_value = False
    # Mode
    fillet_curve.inputs[3].default_value = 'Bézier'
    # Count
    fillet_curve.inputs[4].default_value = 1

    # Node Set Spline Type
    set_spline_type = blocker_1.nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.spline_type = 'BEZIER'
    # Selection
    set_spline_type.inputs[1].default_value = True

    # Node Index Switch
    index_switch = blocker_1.nodes.new("GeometryNodeIndexSwitch")
    index_switch.name = "Index Switch"
    index_switch.data_type = 'FLOAT'
    index_switch.index_switch_items.clear()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    # Item_0
    index_switch.inputs[1].default_value = 0.09000000357627869
    # Item_1
    index_switch.inputs[2].default_value = 0.09000000357627869

    # Node Index
    index = blocker_1.nodes.new("GeometryNodeInputIndex")
    index.name = "Index"

    # Node Fill Curve
    fill_curve = blocker_1.nodes.new("GeometryNodeFillCurve")
    fill_curve.name = "Fill Curve"
    # Group ID
    fill_curve.inputs[1].default_value = 0
    # Mode
    fill_curve.inputs[2].default_value = 'N-gons'

    # Node Extrude Mesh.002
    extrude_mesh_002 = blocker_1.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_002.name = "Extrude Mesh.002"
    extrude_mesh_002.mode = 'FACES'
    # Selection
    extrude_mesh_002.inputs[1].default_value = True
    # Offset
    extrude_mesh_002.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset Scale
    extrude_mesh_002.inputs[3].default_value = 0.009999999776482582
    # Individual
    extrude_mesh_002.inputs[4].default_value = False

    # Node Flip Faces.002
    flip_faces_002 = blocker_1.nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.name = "Flip Faces.002"
    # Selection
    flip_faces_002.inputs[1].default_value = True

    # Node Join Geometry.004
    join_geometry_004 = blocker_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_004.name = "Join Geometry.004"
    join_geometry_004.hide = True

    # Node Merge by Distance.002
    merge_by_distance_002 = blocker_1.nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.name = "Merge by Distance.002"
    # Selection
    merge_by_distance_002.inputs[1].default_value = True
    # Mode
    merge_by_distance_002.inputs[2].default_value = 'All'
    # Distance
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513

    # Node Grid
    grid = blocker_1.nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    # Size X
    grid.inputs[0].default_value = 0.6000000238418579
    # Size Y
    grid.inputs[1].default_value = 0.30000001192092896
    # Vertices X
    grid.inputs[2].default_value = 13
    # Vertices Y
    grid.inputs[3].default_value = 7

    # Node Extrude Mesh.003
    extrude_mesh_003 = blocker_1.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_003.name = "Extrude Mesh.003"
    extrude_mesh_003.mode = 'FACES'
    # Selection
    extrude_mesh_003.inputs[1].default_value = True
    # Offset
    extrude_mesh_003.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset Scale
    extrude_mesh_003.inputs[3].default_value = 0.0
    # Individual
    extrude_mesh_003.inputs[4].default_value = True

    # Node Scale Elements
    scale_elements = blocker_1.nodes.new("GeometryNodeScaleElements")
    scale_elements.name = "Scale Elements"
    scale_elements.domain = 'FACE'
    # Scale
    scale_elements.inputs[2].default_value = 0.0
    # Center
    scale_elements.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale Mode
    scale_elements.inputs[4].default_value = 'Uniform'
    # Axis
    scale_elements.inputs[5].default_value = (1.0, 0.0, 0.0)

    # Node Merge by Distance.003
    merge_by_distance_003 = blocker_1.nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_003.name = "Merge by Distance.003"
    # Mode
    merge_by_distance_003.inputs[2].default_value = 'All'
    # Distance
    merge_by_distance_003.inputs[3].default_value = 0.0010000000474974513

    # Node Subdivide Mesh
    subdivide_mesh = blocker_1.nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh.name = "Subdivide Mesh"
    # Level
    subdivide_mesh.inputs[1].default_value = 3

    # Node Mesh Boolean
    mesh_boolean = blocker_1.nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean.name = "Mesh Boolean"
    mesh_boolean.operation = 'INTERSECT'
    mesh_boolean.solver = 'MANIFOLD'

    # Node Extrude Mesh.004
    extrude_mesh_004 = blocker_1.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_004.name = "Extrude Mesh.004"
    extrude_mesh_004.mode = 'FACES'
    # Selection
    extrude_mesh_004.inputs[1].default_value = True
    # Offset
    extrude_mesh_004.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Offset Scale
    extrude_mesh_004.inputs[3].default_value = 0.009999999776482582
    # Individual
    extrude_mesh_004.inputs[4].default_value = False

    # Node Flip Faces.003
    flip_faces_003 = blocker_1.nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.name = "Flip Faces.003"
    # Selection
    flip_faces_003.inputs[1].default_value = True

    # Node Join Geometry.005
    join_geometry_005 = blocker_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_005.name = "Join Geometry.005"
    join_geometry_005.hide = True

    # Node Merge by Distance.004
    merge_by_distance_004 = blocker_1.nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_004.name = "Merge by Distance.004"
    # Selection
    merge_by_distance_004.inputs[1].default_value = True
    # Mode
    merge_by_distance_004.inputs[2].default_value = 'All'
    # Distance
    merge_by_distance_004.inputs[3].default_value = 0.0010000000474974513

    # Node Delete Geometry.002
    delete_geometry_002 = blocker_1.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.name = "Delete Geometry.002"
    delete_geometry_002.domain = 'POINT'
    delete_geometry_002.mode = 'ALL'

    # Node Set Position.002
    set_position_002 = blocker_1.nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    # Selection
    set_position_002.inputs[1].default_value = True
    # Position
    set_position_002.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Geometry Proximity
    geometry_proximity = blocker_1.nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.target_element = 'EDGES'
    # Group ID
    geometry_proximity.inputs[1].default_value = 0
    # Source Position
    geometry_proximity.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Sample Group ID
    geometry_proximity.inputs[3].default_value = 0

    # Node Separate Geometry
    separate_geometry = blocker_1.nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.name = "Separate Geometry"
    separate_geometry.domain = 'EDGE'

    # Node Geometry Proximity.001
    geometry_proximity_001 = blocker_1.nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.target_element = 'EDGES'
    # Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    # Source Position
    geometry_proximity_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0

    # Node Compare.003
    compare_003 = blocker_1.nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.data_type = 'FLOAT'
    compare_003.mode = 'ELEMENT'
    compare_003.operation = 'GREATER_THAN'
    # B
    compare_003.inputs[1].default_value = 0.0

    # Node Combine XYZ
    combine_xyz = blocker_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    # X
    combine_xyz.inputs[0].default_value = 0.0
    # Y
    combine_xyz.inputs[1].default_value = 0.0

    # Node Map Range
    map_range = blocker_1.nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.clamp = True
    map_range.data_type = 'FLOAT'
    map_range.interpolation_type = 'LINEAR'
    # From Min
    map_range.inputs[1].default_value = 0.0
    # From Max
    map_range.inputs[2].default_value = 0.009999999776482582
    # To Min
    map_range.inputs[3].default_value = 1.0
    # To Max
    map_range.inputs[4].default_value = 0.0

    # Node Math.002
    math_002 = blocker_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'POWER'
    math_002.use_clamp = False
    # Value_001
    math_002.inputs[1].default_value = 2.0

    # Node Math.003
    math_003 = blocker_1.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'MULTIPLY'
    math_003.use_clamp = False
    # Value_001
    math_003.inputs[1].default_value = 0.0020000000949949026

    # Node Math.004
    math_004 = blocker_1.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'SUBTRACT'
    math_004.use_clamp = False
    # Value
    math_004.inputs[0].default_value = 1.0

    # Node Curve to Mesh.003
    curve_to_mesh_003 = blocker_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.name = "Curve to Mesh.003"
    # Scale
    curve_to_mesh_003.inputs[2].default_value = 1.0
    # Fill Caps
    curve_to_mesh_003.inputs[3].default_value = False

    # Node Curve Circle.003
    curve_circle_003 = blocker_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.name = "Curve Circle.003"
    curve_circle_003.mode = 'RADIUS'
    # Resolution
    curve_circle_003.inputs[0].default_value = 57
    # Radius
    curve_circle_003.inputs[4].default_value = 0.004999999888241291

    # Node Transform Geometry.002
    transform_geometry_002 = blocker_1.nodes.new("GeometryNodeTransform")
    transform_geometry_002.name = "Transform Geometry.002"
    # Mode
    transform_geometry_002.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_002.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_002.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_002.inputs[4].default_value = (1.0, 0.5, 1.0)

    # Node Resample Curve.002
    resample_curve_002 = blocker_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.name = "Resample Curve.002"
    resample_curve_002.keep_last_segment = True
    # Selection
    resample_curve_002.inputs[1].default_value = True
    # Mode
    resample_curve_002.inputs[2].default_value = 'Length'
    # Count
    resample_curve_002.inputs[3].default_value = 10
    # Length
    resample_curve_002.inputs[4].default_value = 0.009999999776482582

    # Node Frame.002
    frame_002 = blocker_1.nodes.new("NodeFrame")
    frame_002.label = "Piping"
    frame_002.name = "Frame.002"
    frame_002.label_size = 20
    frame_002.shrink = True

    # Node Frame.003
    frame_003 = blocker_1.nodes.new("NodeFrame")
    frame_003.label = "Quilting"
    frame_003.name = "Frame.003"
    frame_003.label_size = 20
    frame_003.shrink = True

    # Node Transform Geometry.003
    transform_geometry_003 = blocker_1.nodes.new("GeometryNodeTransform")
    transform_geometry_003.name = "Transform Geometry.003"
    # Mode
    transform_geometry_003.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_003.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_003.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_003.inputs[4].default_value = (1.0, 1.0, -1.0)

    # Node Flip Faces.004
    flip_faces_004 = blocker_1.nodes.new("GeometryNodeFlipFaces")
    flip_faces_004.name = "Flip Faces.004"
    # Selection
    flip_faces_004.inputs[1].default_value = True

    # Node Join Geometry.006
    join_geometry_006 = blocker_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_006.name = "Join Geometry.006"
    join_geometry_006.hide = True

    # Node Join Geometry.007
    join_geometry_007 = blocker_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_007.name = "Join Geometry.007"
    join_geometry_007.hide = True

    # Node Set Shade Smooth.001
    set_shade_smooth_001 = blocker_1.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.name = "Set Shade Smooth.001"
    set_shade_smooth_001.domain = 'FACE'
    # Selection
    set_shade_smooth_001.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_001.inputs[2].default_value = True

    # Node Set Shade Smooth.002
    set_shade_smooth_002 = blocker_1.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_002.name = "Set Shade Smooth.002"
    set_shade_smooth_002.domain = 'EDGE'
    # Shade Smooth
    set_shade_smooth_002.inputs[2].default_value = False

    # Node Compare.004
    compare_004 = blocker_1.nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.data_type = 'FLOAT'
    compare_004.mode = 'ELEMENT'
    compare_004.operation = 'EQUAL'
    # B
    compare_004.inputs[1].default_value = 0.0
    # Epsilon
    compare_004.inputs[12].default_value = 0.0010000000474974513

    # Node Frame.004
    frame_004 = blocker_1.nodes.new("NodeFrame")
    frame_004.label = "Gambeson Pattern"
    frame_004.name = "Frame.004"
    frame_004.label_size = 20
    frame_004.shrink = True

    # Node Sample UV Surface
    sample_uv_surface = blocker_1.nodes.new("GeometryNodeSampleUVSurface")
    sample_uv_surface.name = "Sample UV Surface"
    sample_uv_surface.hide = True
    sample_uv_surface.data_type = 'FLOAT_VECTOR'

    # Node Capture Attribute
    capture_attribute = blocker_1.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.active_index = 0
    capture_attribute.capture_items.clear()
    capture_attribute.capture_items.new('FLOAT', "Factor")
    capture_attribute.capture_items["Factor"].data_type = 'FLOAT'
    capture_attribute.domain = 'POINT'

    # Node Capture Attribute.001
    capture_attribute_001 = blocker_1.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.name = "Capture Attribute.001"
    capture_attribute_001.active_index = 0
    capture_attribute_001.capture_items.clear()
    capture_attribute_001.capture_items.new('FLOAT', "Factor")
    capture_attribute_001.capture_items["Factor"].data_type = 'FLOAT'
    capture_attribute_001.domain = 'POINT'

    # Node Spline Parameter.002
    spline_parameter_002 = blocker_1.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"

    # Node Combine XYZ.001
    combine_xyz_001 = blocker_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_001.name = "Combine XYZ.001"
    combine_xyz_001.inputs[2].hide = True
    # Z
    combine_xyz_001.inputs[2].default_value = 0.0

    # Node Set Spline Cyclic
    set_spline_cyclic = blocker_1.nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.name = "Set Spline Cyclic"
    # Selection
    set_spline_cyclic.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic.inputs[2].default_value = False

    # Node Set Curve Tilt
    set_curve_tilt = blocker_1.nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.name = "Set Curve Tilt"
    # Selection
    set_curve_tilt.inputs[1].default_value = True
    # Tilt
    set_curve_tilt.inputs[2].default_value = -1.472708821296692

    # Node Position.005
    position_005 = blocker_1.nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"
    position_005.hide = True

    # Node Set Position.003
    set_position_003 = blocker_1.nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    # Selection
    set_position_003.inputs[1].default_value = True

    # Node Bounding Box
    bounding_box = blocker_1.nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    bounding_box.inputs[1].hide = True
    bounding_box.outputs[0].hide = True
    # Use Radius
    bounding_box.inputs[1].default_value = False

    # Node Position.006
    position_006 = blocker_1.nodes.new("GeometryNodeInputPosition")
    position_006.name = "Position.006"

    # Node Map Range.001
    map_range_001 = blocker_1.nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.clamp = True
    map_range_001.data_type = 'FLOAT_VECTOR'
    map_range_001.interpolation_type = 'LINEAR'
    # To_Min_FLOAT3
    map_range_001.inputs[9].default_value = (0.009999999776482582, 0.009999999776482582, 0.009999999776482582)
    # To_Max_FLOAT3
    map_range_001.inputs[10].default_value = (0.9900000095367432, 0.9900000095367432, 0.9900000095367432)

    # Node Sample UV Surface.001
    sample_uv_surface_001 = blocker_1.nodes.new("GeometryNodeSampleUVSurface")
    sample_uv_surface_001.name = "Sample UV Surface.001"
    sample_uv_surface_001.hide = True
    sample_uv_surface_001.data_type = 'FLOAT_VECTOR'

    # Node Normal.003
    normal_003 = blocker_1.nodes.new("GeometryNodeInputNormal")
    normal_003.name = "Normal.003"
    normal_003.hide = True
    normal_003.legacy_corner_normals = False
    normal_003.outputs[1].hide = True

    # Node Separate XYZ.003
    separate_xyz_003 = blocker_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_003.name = "Separate XYZ.003"
    separate_xyz_003.outputs[0].hide = True
    separate_xyz_003.outputs[1].hide = True

    # Node Vector Math.004
    vector_math_004 = blocker_1.nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.hide = True
    vector_math_004.operation = 'SCALE'

    # Node Math.005
    math_005 = blocker_1.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'MULTIPLY'
    math_005.use_clamp = False
    # Value_001
    math_005.inputs[1].default_value = 1.2499998807907104

    # Node Capture Attribute.002
    capture_attribute_002 = blocker_1.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.name = "Capture Attribute.002"
    capture_attribute_002.active_index = 0
    capture_attribute_002.capture_items.clear()
    capture_attribute_002.capture_items.new('FLOAT', "Position")
    capture_attribute_002.capture_items["Position"].data_type = 'FLOAT_VECTOR'
    capture_attribute_002.capture_items.new('FLOAT', "Normal")
    capture_attribute_002.capture_items["Normal"].data_type = 'FLOAT_VECTOR'
    capture_attribute_002.capture_items.new('FLOAT', "UVMap")
    capture_attribute_002.capture_items["UVMap"].data_type = 'FLOAT_VECTOR'
    capture_attribute_002.domain = 'POINT'

    # Node Noise Texture.002
    noise_texture_002 = blocker_1.nodes.new("ShaderNodeTexNoise")
    noise_texture_002.name = "Noise Texture.002"
    noise_texture_002.noise_dimensions = '4D'
    noise_texture_002.noise_type = 'FBM'
    noise_texture_002.normalize = False
    # Vector
    noise_texture_002.inputs[0].default_value = (0.0, 0.0, 0.0)
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
    # Distortion
    noise_texture_002.inputs[8].default_value = 0.0

    # Node Vector Math.006
    vector_math_006 = blocker_1.nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.hide = True
    vector_math_006.operation = 'ADD'

    # Node Vector Math.005
    vector_math_005 = blocker_1.nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.operation = 'SCALE'
    # Scale
    vector_math_005.inputs[3].default_value = 0.006000000052154064

    # Node Store Named Attribute.001
    store_named_attribute_001 = blocker_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.data_type = 'BOOLEAN'
    store_named_attribute_001.domain = 'POINT'
    # Selection
    store_named_attribute_001.inputs[1].default_value = True
    # Name
    store_named_attribute_001.inputs[2].default_value = "skip"
    # Value
    store_named_attribute_001.inputs[3].default_value = True

    # Node Frame.005
    frame_005 = blocker_1.nodes.new("NodeFrame")
    frame_005.label = "Thickness"
    frame_005.name = "Frame.005"
    frame_005.label_size = 20
    frame_005.shrink = True

    # Node Reroute.001
    reroute_001 = blocker_1.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.socket_idname = "NodeSocketVector"
    # Node Reroute.002
    reroute_002 = blocker_1.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.socket_idname = "NodeSocketGeometry"
    # Node Frame.006
    frame_006 = blocker_1.nodes.new("NodeFrame")
    frame_006.label = "UVMap"
    frame_006.name = "Frame.006"
    frame_006.label_size = 20
    frame_006.shrink = True

    # Node Frame.007
    frame_007 = blocker_1.nodes.new("NodeFrame")
    frame_007.label = "General Collar Shape"
    frame_007.name = "Frame.007"
    frame_007.label_size = 20
    frame_007.shrink = True

    # Node Frame.008
    frame_008 = blocker_1.nodes.new("NodeFrame")
    frame_008.label = "Displacement"
    frame_008.name = "Frame.008"
    frame_008.label_size = 20
    frame_008.shrink = True

    # Node Frame.009
    frame_009 = blocker_1.nodes.new("NodeFrame")
    frame_009.label = "Collar"
    frame_009.name = "Frame.009"
    frame_009.label_size = 20
    frame_009.shrink = True

    # Node Store Named Attribute.002
    store_named_attribute_002 = blocker_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.data_type = 'FLOAT2'
    store_named_attribute_002.domain = 'CORNER'
    # Selection
    store_named_attribute_002.inputs[1].default_value = True
    # Name
    store_named_attribute_002.inputs[2].default_value = "UVMap"

    # Node Switch.001
    switch_001 = blocker_1.nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.input_type = 'GEOMETRY'

    # Node Group Input.001
    group_input_001 = blocker_1.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[1].hide = True

    # Node Curve to Mesh.004
    curve_to_mesh_004 = blocker_1.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_004.name = "Curve to Mesh.004"
    # Fill Caps
    curve_to_mesh_004.inputs[3].default_value = False

    # Node Curve Circle.004
    curve_circle_004 = blocker_1.nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_004.name = "Curve Circle.004"
    curve_circle_004.mode = 'RADIUS'
    # Resolution
    curve_circle_004.inputs[0].default_value = 24
    # Radius
    curve_circle_004.inputs[4].default_value = 0.10000000149011612

    # Node Set Spline Cyclic.001
    set_spline_cyclic_001 = blocker_1.nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_001.name = "Set Spline Cyclic.001"
    # Selection
    set_spline_cyclic_001.inputs[1].default_value = True
    # Cyclic
    set_spline_cyclic_001.inputs[2].default_value = False

    # Node Mesh to Curve
    mesh_to_curve = blocker_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.mode = 'EDGES'
    # Selection
    mesh_to_curve.inputs[1].default_value = True

    # Node Resample Curve
    resample_curve = blocker_1.nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.keep_last_segment = True
    # Selection
    resample_curve.inputs[1].default_value = True
    # Mode
    resample_curve.inputs[2].default_value = 'Length'
    # Count
    resample_curve.inputs[3].default_value = 101
    # Length
    resample_curve.inputs[4].default_value = 0.003000000026077032

    # Node Subdivide Mesh.001
    subdivide_mesh_001 = blocker_1.nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh_001.name = "Subdivide Mesh.001"
    # Level
    subdivide_mesh_001.inputs[1].default_value = 4

    # Node Geometry Proximity.002
    geometry_proximity_002 = blocker_1.nodes.new("GeometryNodeProximity")
    geometry_proximity_002.name = "Geometry Proximity.002"
    geometry_proximity_002.target_element = 'FACES'
    # Group ID
    geometry_proximity_002.inputs[1].default_value = 0
    # Source Position
    geometry_proximity_002.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Sample Group ID
    geometry_proximity_002.inputs[3].default_value = 0

    # Node Compare
    compare = blocker_1.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'FLOAT'
    compare.mode = 'ELEMENT'
    compare.operation = 'GREATER_THAN'
    # B
    compare.inputs[1].default_value = 0.0010000000474974513

    # Node Delete Geometry
    delete_geometry = blocker_1.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.domain = 'POINT'
    delete_geometry.mode = 'ALL'

    # Node Instance on Points.001
    instance_on_points_001 = blocker_1.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.name = "Instance on Points.001"
    # Selection
    instance_on_points_001.inputs[1].default_value = True
    # Pick Instance
    instance_on_points_001.inputs[3].default_value = False
    # Instance Index
    instance_on_points_001.inputs[4].default_value = 0

    # Node Align Rotation to Vector.001
    align_rotation_to_vector_001 = blocker_1.nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.name = "Align Rotation to Vector.001"
    align_rotation_to_vector_001.axis = 'X'
    align_rotation_to_vector_001.pivot_axis = 'AUTO'
    # Rotation
    align_rotation_to_vector_001.inputs[0].default_value = (0.0, 0.0, 0.0)
    # Factor
    align_rotation_to_vector_001.inputs[1].default_value = 1.0

    # Node Curve Tangent
    curve_tangent = blocker_1.nodes.new("GeometryNodeInputTangent")
    curve_tangent.name = "Curve Tangent"

    # Node Ico Sphere.001
    ico_sphere_001 = blocker_1.nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.name = "Ico Sphere.001"
    # Radius
    ico_sphere_001.inputs[0].default_value = 0.0007999999797903001
    # Subdivisions
    ico_sphere_001.inputs[1].default_value = 2

    # Node Transform Geometry.004
    transform_geometry_004 = blocker_1.nodes.new("GeometryNodeTransform")
    transform_geometry_004.name = "Transform Geometry.004"
    # Mode
    transform_geometry_004.inputs[1].default_value = 'Components'
    # Translation
    transform_geometry_004.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_004.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_004.inputs[4].default_value = (1.5, 0.5, 0.3199999928474426)

    # Node Realize Instances.001
    realize_instances_001 = blocker_1.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"
    # Selection
    realize_instances_001.inputs[1].default_value = True
    # Realize All
    realize_instances_001.inputs[2].default_value = True
    # Depth
    realize_instances_001.inputs[3].default_value = 0

    # Node Set Position
    set_position = blocker_1.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    # Selection
    set_position.inputs[1].default_value = True
    # Offset
    set_position.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Node Position
    position = blocker_1.nodes.new("GeometryNodeInputPosition")
    position.name = "Position"

    # Node Separate XYZ
    separate_xyz = blocker_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"

    # Node Map Range.002
    map_range_002 = blocker_1.nodes.new("ShaderNodeMapRange")
    map_range_002.name = "Map Range.002"
    map_range_002.clamp = True
    map_range_002.data_type = 'FLOAT'
    map_range_002.interpolation_type = 'LINEAR'
    # From Min
    map_range_002.inputs[1].default_value = -0.004999999888241291
    # From Max
    map_range_002.inputs[2].default_value = 0.004999999888241291
    # To Min
    map_range_002.inputs[3].default_value = 0.0
    # To Max
    map_range_002.inputs[4].default_value = 1.0

    # Node Float Curve
    float_curve = blocker_1.nodes.new("ShaderNodeFloatCurve")
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
    float_curve_curve_0_point_1.location = (0.16918471455574036, 0.04741369187831879)
    float_curve_curve_0_point_1.handle_type = 'AUTO'
    float_curve_curve_0_point_2 = float_curve_curve_0.points.new(0.22054383158683777, 1.0)
    float_curve_curve_0_point_2.handle_type = 'AUTO'
    float_curve_curve_0_point_3 = float_curve_curve_0.points.new(0.2765861451625824, 0.3771551549434662)
    float_curve_curve_0_point_3.handle_type = 'VECTOR'
    float_curve_curve_0_point_4 = float_curve_curve_0.points.new(0.41087615489959717, 1.0)
    float_curve_curve_0_point_4.handle_type = 'AUTO'
    float_curve_curve_0_point_5 = float_curve_curve_0.points.new(1.0, 1.0)
    float_curve_curve_0_point_5.handle_type = 'AUTO'
    # Update curve after changes
    float_curve.mapping.update()
    # Factor
    float_curve.inputs[0].default_value = 1.0

    # Node Math
    math = blocker_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'MULTIPLY'
    math.use_clamp = False

    # Node Combine XYZ.002
    combine_xyz_002 = blocker_1.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_002.name = "Combine XYZ.002"

    # Node Capture Attribute.003
    capture_attribute_003 = blocker_1.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.name = "Capture Attribute.003"
    capture_attribute_003.active_index = 0
    capture_attribute_003.capture_items.clear()
    capture_attribute_003.capture_items.new('FLOAT', "Result")
    capture_attribute_003.capture_items["Result"].data_type = 'BOOLEAN'
    capture_attribute_003.domain = 'POINT'

    # Node Index.001
    index_001 = blocker_1.nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"

    # Node Compare.002
    compare_002 = blocker_1.nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.data_type = 'INT'
    compare_002.mode = 'ELEMENT'
    compare_002.operation = 'EQUAL'
    # B_INT
    compare_002.inputs[3].default_value = 39

    # Node Mesh to Curve.001
    mesh_to_curve_001 = blocker_1.nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.name = "Mesh to Curve.001"
    mesh_to_curve_001.mode = 'EDGES'

    # Node Join Geometry.001
    join_geometry_001 = blocker_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    join_geometry_001.hide = True

    # Node Join Geometry.008
    join_geometry_008 = blocker_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_008.name = "Join Geometry.008"
    join_geometry_008.hide = True

    # Node Set Shade Smooth.003
    set_shade_smooth_003 = blocker_1.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.name = "Set Shade Smooth.003"
    set_shade_smooth_003.domain = 'FACE'
    # Selection
    set_shade_smooth_003.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth_003.inputs[2].default_value = True

    # Node Join Geometry.009
    join_geometry_009 = blocker_1.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_009.name = "Join Geometry.009"
    join_geometry_009.hide = True

    # Node Frame
    frame = blocker_1.nodes.new("NodeFrame")
    frame.label = "Stitching"
    frame.name = "Frame"
    frame.label_size = 20
    frame.shrink = True

    # Node Store Named Attribute.003
    store_named_attribute_003 = blocker_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.data_type = 'BOOLEAN'
    store_named_attribute_003.domain = 'POINT'
    # Selection
    store_named_attribute_003.inputs[1].default_value = True
    # Name
    store_named_attribute_003.inputs[2].default_value = "stitching"
    # Value
    store_named_attribute_003.inputs[3].default_value = True

    # Node Store Named Attribute.004
    store_named_attribute_004 = blocker_1.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.data_type = 'BOOLEAN'
    store_named_attribute_004.domain = 'POINT'
    # Selection
    store_named_attribute_004.inputs[1].default_value = True
    # Name
    store_named_attribute_004.inputs[2].default_value = "piping"
    # Value
    store_named_attribute_004.inputs[3].default_value = True

    # Node Random Value.001
    random_value_001 = blocker_1.nodes.new("FunctionNodeRandomValue")
    random_value_001.name = "Random Value.001"
    random_value_001.data_type = 'FLOAT_VECTOR'
    # Min
    random_value_001.inputs[0].default_value = (0.699999988079071, 0.699999988079071, 0.699999988079071)
    # Max
    random_value_001.inputs[1].default_value = (1.0, 1.5, 1.2999999523162842)
    # ID
    random_value_001.inputs[7].default_value = 0
    # Seed
    random_value_001.inputs[8].default_value = 0

    # Set parents
    blocker_1.nodes["Store Named Attribute"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Ico Sphere"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Transform Geometry"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Transform Geometry.001"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Mesh to SDF Grid"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Mesh to SDF Grid.001"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["SDF Grid Boolean"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Grid to Mesh"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["SDF Grid Fillet"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Instance on Points"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Curve Circle.001"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Curve to Mesh.001"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Position.002"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Separate XYZ.001"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Compare.001"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Align Rotation to Vector"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Normal.001"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Rotate Rotation"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Rotate Rotation.001"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Random Value"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Realize Instances"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Switch"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Join Geometry.002"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Reroute"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Group Input"].parent = blocker_1.nodes["Frame.001"]
    blocker_1.nodes["Curve to Mesh.002"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Curve Circle.002"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Spline Parameter.001"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Float Curve.001"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Resample Curve.001"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Quadratic Bézier.001"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Set Position.001"].parent = blocker_1.nodes["Frame.008"]
    blocker_1.nodes["Vector Math.002"].parent = blocker_1.nodes["Frame.008"]
    blocker_1.nodes["Noise Texture.001"].parent = blocker_1.nodes["Frame.008"]
    blocker_1.nodes["Vector Math.003"].parent = blocker_1.nodes["Frame.008"]
    blocker_1.nodes["Quadrilateral"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Fillet Curve"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Set Spline Type"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Index Switch"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Index"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Fill Curve"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Extrude Mesh.002"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Flip Faces.002"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Join Geometry.004"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Merge by Distance.002"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Grid"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Extrude Mesh.003"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Scale Elements"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Merge by Distance.003"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Subdivide Mesh"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Mesh Boolean"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Extrude Mesh.004"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Flip Faces.003"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Join Geometry.005"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Merge by Distance.004"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Delete Geometry.002"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Set Position.002"].parent = blocker_1.nodes["Frame.003"]
    blocker_1.nodes["Geometry Proximity"].parent = blocker_1.nodes["Frame.003"]
    blocker_1.nodes["Separate Geometry"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Geometry Proximity.001"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Compare.003"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Combine XYZ"].parent = blocker_1.nodes["Frame.003"]
    blocker_1.nodes["Map Range"].parent = blocker_1.nodes["Frame.003"]
    blocker_1.nodes["Math.002"].parent = blocker_1.nodes["Frame.003"]
    blocker_1.nodes["Math.003"].parent = blocker_1.nodes["Frame.003"]
    blocker_1.nodes["Math.004"].parent = blocker_1.nodes["Frame.003"]
    blocker_1.nodes["Curve to Mesh.003"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Curve Circle.003"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Transform Geometry.002"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Resample Curve.002"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Frame.002"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Frame.003"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Transform Geometry.003"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Flip Faces.004"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Join Geometry.006"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Join Geometry.007"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Set Shade Smooth.001"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Set Shade Smooth.002"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Compare.004"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Frame.004"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Sample UV Surface"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Capture Attribute"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Capture Attribute.001"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Spline Parameter.002"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Combine XYZ.001"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Set Spline Cyclic"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Set Curve Tilt"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Position.005"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Set Position.003"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Bounding Box"].parent = blocker_1.nodes["Frame.006"]
    blocker_1.nodes["Position.006"].parent = blocker_1.nodes["Frame.006"]
    blocker_1.nodes["Map Range.001"].parent = blocker_1.nodes["Frame.006"]
    blocker_1.nodes["Sample UV Surface.001"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Normal.003"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Separate XYZ.003"].parent = blocker_1.nodes["Frame.005"]
    blocker_1.nodes["Vector Math.004"].parent = blocker_1.nodes["Frame.005"]
    blocker_1.nodes["Math.005"].parent = blocker_1.nodes["Frame.005"]
    blocker_1.nodes["Capture Attribute.002"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Noise Texture.002"].parent = blocker_1.nodes["Frame.008"]
    blocker_1.nodes["Vector Math.006"].parent = blocker_1.nodes["Frame.008"]
    blocker_1.nodes["Vector Math.005"].parent = blocker_1.nodes["Frame.008"]
    blocker_1.nodes["Store Named Attribute.001"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Frame.005"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Reroute.001"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Reroute.002"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Frame.006"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Frame.007"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Frame.008"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Store Named Attribute.002"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Switch.001"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Group Input.001"].parent = blocker_1.nodes["Frame.009"]
    blocker_1.nodes["Curve to Mesh.004"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Curve Circle.004"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Set Spline Cyclic.001"].parent = blocker_1.nodes["Frame.007"]
    blocker_1.nodes["Mesh to Curve"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Resample Curve"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Subdivide Mesh.001"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Geometry Proximity.002"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Compare"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Delete Geometry"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Instance on Points.001"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Align Rotation to Vector.001"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Curve Tangent"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Ico Sphere.001"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Transform Geometry.004"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Realize Instances.001"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Set Position"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Position"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Separate XYZ"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Map Range.002"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Float Curve"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Math"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Combine XYZ.002"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Capture Attribute.003"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Index.001"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Compare.002"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Mesh to Curve.001"].parent = blocker_1.nodes["Frame.002"]
    blocker_1.nodes["Join Geometry.001"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Join Geometry.008"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Set Shade Smooth.003"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Join Geometry.009"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Frame"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Store Named Attribute.003"].parent = blocker_1.nodes["Frame"]
    blocker_1.nodes["Store Named Attribute.004"].parent = blocker_1.nodes["Frame.004"]
    blocker_1.nodes["Random Value.001"].parent = blocker_1.nodes["Frame"]

    # Set locations
    blocker_1.nodes["Group Output"].location = (1991.1298828125, -100.0)
    blocker_1.nodes["Join Geometry"].location = (1511.1298828125, -100.0)
    blocker_1.nodes["Set Shade Smooth"].location = (1671.1298828125, -100.0)
    blocker_1.nodes["Store Named Attribute"].location = (7331.1298828125, -712.0)
    blocker_1.nodes["Ico Sphere"].location = (30.0, -276.0)
    blocker_1.nodes["Transform Geometry"].location = (330.0, -376.0)
    blocker_1.nodes["Frame.001"].location = (-1910.0, 696.0)
    blocker_1.nodes["Transform Geometry.001"].location = (330.0, -36.0)
    blocker_1.nodes["Mesh to SDF Grid"].location = (570.0, -436.0)
    blocker_1.nodes["Mesh to SDF Grid.001"].location = (570.0, -296.0)
    blocker_1.nodes["SDF Grid Boolean"].location = (730.0, -296.0)
    blocker_1.nodes["Grid to Mesh"].location = (1050.0, -296.0)
    blocker_1.nodes["SDF Grid Fillet"].location = (890.0, -296.0)
    blocker_1.nodes["Instance on Points"].location = (1730.0, -276.0)
    blocker_1.nodes["Curve Circle.001"].location = (870.0, -476.0)
    blocker_1.nodes["Curve to Mesh.001"].location = (1050.0, -476.0)
    blocker_1.nodes["Position.002"].location = (1370.0, -416.0)
    blocker_1.nodes["Separate XYZ.001"].location = (1370.0, -476.0)
    blocker_1.nodes["Compare.001"].location = (1530.0, -416.0)
    blocker_1.nodes["Align Rotation to Vector"].location = (1210.0, -616.0)
    blocker_1.nodes["Normal.001"].location = (1050.0, -616.0)
    blocker_1.nodes["Rotate Rotation"].location = (1370.0, -616.0)
    blocker_1.nodes["Rotate Rotation.001"].location = (1550.0, -616.0)
    blocker_1.nodes["Random Value"].location = (1550.0, -736.0)
    blocker_1.nodes["Realize Instances"].location = (1890.0, -276.0)
    blocker_1.nodes["Switch"].location = (2110.0, -156.0)
    blocker_1.nodes["Join Geometry.002"].location = (590.0, -156.0)
    blocker_1.nodes["Reroute"].location = (2010.0, -196.0)
    blocker_1.nodes["Group Input"].location = (2110.0, -96.0)
    blocker_1.nodes["Curve to Mesh.002"].location = (1170.0, -416.0)
    blocker_1.nodes["Curve Circle.002"].location = (470.0, -496.0)
    blocker_1.nodes["Spline Parameter.001"].location = (30.0, -596.0)
    blocker_1.nodes["Float Curve.001"].location = (190.0, -476.0)
    blocker_1.nodes["Resample Curve.001"].location = (190.0, -256.0)
    blocker_1.nodes["Quadratic Bézier.001"].location = (30.0, -256.0)
    blocker_1.nodes["Set Position.001"].location = (1041.1298828125, -36.0)
    blocker_1.nodes["Vector Math.002"].location = (641.1298828125, -176.0)
    blocker_1.nodes["Noise Texture.001"].location = (301.1298828125, -316.0)
    blocker_1.nodes["Vector Math.003"].location = (141.12982177734375, -316.0)
    blocker_1.nodes["Quadrilateral"].location = (230.0, -732.0)
    blocker_1.nodes["Fillet Curve"].location = (550.0, -732.0)
    blocker_1.nodes["Set Spline Type"].location = (390.0, -732.0)
    blocker_1.nodes["Index Switch"].location = (550.0, -852.0)
    blocker_1.nodes["Index"].location = (390.0, -852.0)
    blocker_1.nodes["Fill Curve"].location = (710.0, -732.0)
    blocker_1.nodes["Extrude Mesh.002"].location = (890.0, -732.0)
    blocker_1.nodes["Flip Faces.002"].location = (890.0, -632.0)
    blocker_1.nodes["Join Geometry.004"].location = (1070.0, -692.0)
    blocker_1.nodes["Merge by Distance.002"].location = (1070.0, -732.0)
    blocker_1.nodes["Grid"].location = (30.0, -332.0)
    blocker_1.nodes["Extrude Mesh.003"].location = (210.0, -332.0)
    blocker_1.nodes["Scale Elements"].location = (370.0, -332.0)
    blocker_1.nodes["Merge by Distance.003"].location = (530.0, -332.0)
    blocker_1.nodes["Subdivide Mesh"].location = (690.0, -332.0)
    blocker_1.nodes["Mesh Boolean"].location = (1230.0, -332.0)
    blocker_1.nodes["Extrude Mesh.004"].location = (870.0, -332.0)
    blocker_1.nodes["Flip Faces.003"].location = (870.0, -232.0)
    blocker_1.nodes["Join Geometry.005"].location = (1050.0, -292.0)
    blocker_1.nodes["Merge by Distance.004"].location = (1050.0, -332.0)
    blocker_1.nodes["Delete Geometry.002"].location = (1390.0, -332.0)
    blocker_1.nodes["Set Position.002"].location = (1230.0, -316.0)
    blocker_1.nodes["Geometry Proximity"].location = (30.0, -36.0)
    blocker_1.nodes["Separate Geometry"].location = (690.0, -112.0)
    blocker_1.nodes["Geometry Proximity.001"].location = (210.0, -112.0)
    blocker_1.nodes["Compare.003"].location = (370.0, -112.0)
    blocker_1.nodes["Combine XYZ"].location = (830.0, -36.0)
    blocker_1.nodes["Map Range"].location = (190.0, -36.0)
    blocker_1.nodes["Math.002"].location = (350.0, -36.0)
    blocker_1.nodes["Math.003"].location = (670.0, -36.0)
    blocker_1.nodes["Math.004"].location = (510.0, -36.0)
    blocker_1.nodes["Curve to Mesh.003"].location = (1530.0, -56.0)
    blocker_1.nodes["Curve Circle.003"].location = (770.0, -196.0)
    blocker_1.nodes["Transform Geometry.002"].location = (950.0, -196.0)
    blocker_1.nodes["Resample Curve.002"].location = (1050.0, -36.0)
    blocker_1.nodes["Frame.002"].location = (180.0, -1616.0)
    blocker_1.nodes["Frame.003"].location = (1560.0, -36.0)
    blocker_1.nodes["Transform Geometry.003"].location = (3010.0, -412.0)
    blocker_1.nodes["Flip Faces.004"].location = (3010.0, -332.0)
    blocker_1.nodes["Join Geometry.006"].location = (3210.0, -372.0)
    blocker_1.nodes["Join Geometry.007"].location = (1130.0, -152.0)
    blocker_1.nodes["Set Shade Smooth.001"].location = (3390.0, -332.0)
    blocker_1.nodes["Set Shade Smooth.002"].location = (3570.0, -332.0)
    blocker_1.nodes["Compare.004"].location = (3390.0, -452.0)
    blocker_1.nodes["Frame.004"].location = (30.0, -920.0)
    blocker_1.nodes["Sample UV Surface"].location = (4751.1298828125, -692.0)
    blocker_1.nodes["Capture Attribute"].location = (910.0, -576.0)
    blocker_1.nodes["Capture Attribute.001"].location = (910.0, -376.0)
    blocker_1.nodes["Spline Parameter.002"].location = (450.0, -356.0)
    blocker_1.nodes["Combine XYZ.001"].location = (1170.0, -576.0)
    blocker_1.nodes["Set Spline Cyclic"].location = (650.0, -516.0)
    blocker_1.nodes["Set Curve Tilt"].location = (650.0, -236.0)
    blocker_1.nodes["Position.005"].location = (4500.0, -652.0)
    blocker_1.nodes["Set Position.003"].location = (5631.1298828125, -892.0)
    blocker_1.nodes["Bounding Box"].location = (281.1298828125, -96.0)
    blocker_1.nodes["Position.006"].location = (30.0, -36.0)
    blocker_1.nodes["Map Range.001"].location = (481.1298828125, -36.0)
    blocker_1.nodes["Sample UV Surface.001"].location = (4751.1298828125, -792.0)
    blocker_1.nodes["Normal.003"].location = (4500.0, -752.0)
    blocker_1.nodes["Separate XYZ.003"].location = (30.0, -80.0)
    blocker_1.nodes["Vector Math.004"].location = (441.1298828125, -40.0)
    blocker_1.nodes["Math.005"].location = (190.0, -80.0)
    blocker_1.nodes["Capture Attribute.002"].location = (5091.1298828125, -952.0)
    blocker_1.nodes["Noise Texture.002"].location = (30.0, -656.0)
    blocker_1.nodes["Vector Math.006"].location = (841.1298828125, -256.0)
    blocker_1.nodes["Vector Math.005"].location = (410.0, -536.0)
    blocker_1.nodes["Store Named Attribute.001"].location = (7171.1298828125, -712.0)
    blocker_1.nodes["Frame.005"].location = (4950.0, -1212.0)
    blocker_1.nodes["Reroute.001"].location = (4420.0, -712.0)
    blocker_1.nodes["Reroute.002"].location = (4420.0, -672.0)
    blocker_1.nodes["Frame.006"].location = (4130.0, -896.0)
    blocker_1.nodes["Frame.007"].location = (2850.0, -36.0)
    blocker_1.nodes["Frame.008"].location = (5730.0, -836.0)
    blocker_1.nodes["Frame.009"].location = (-6800.0, -428.0)
    blocker_1.nodes["Store Named Attribute.002"].location = (5351.1298828125, -812.0)
    blocker_1.nodes["Switch.001"].location = (7011.1298828125, -712.0)
    blocker_1.nodes["Group Input.001"].location = (6760.0, -632.0)
    blocker_1.nodes["Curve to Mesh.004"].location = (1170.0, -196.0)
    blocker_1.nodes["Curve Circle.004"].location = (710.0, -36.0)
    blocker_1.nodes["Set Spline Cyclic.001"].location = (890.0, -56.0)
    blocker_1.nodes["Mesh to Curve"].location = (570.0, -56.0)
    blocker_1.nodes["Resample Curve"].location = (1190.0, -36.0)
    blocker_1.nodes["Subdivide Mesh.001"].location = (30.0, -136.0)
    blocker_1.nodes["Geometry Proximity.002"].location = (30.0, -216.0)
    blocker_1.nodes["Compare"].location = (190.0, -216.0)
    blocker_1.nodes["Delete Geometry"].location = (410.0, -56.0)
    blocker_1.nodes["Instance on Points.001"].location = (1390.0, -36.0)
    blocker_1.nodes["Align Rotation to Vector.001"].location = (1190.0, -156.0)
    blocker_1.nodes["Curve Tangent"].location = (1010.0, -196.0)
    blocker_1.nodes["Ico Sphere.001"].location = (990.0, -296.0)
    blocker_1.nodes["Transform Geometry.004"].location = (1190.0, -316.0)
    blocker_1.nodes["Realize Instances.001"].location = (1570.0, -36.0)
    blocker_1.nodes["Set Position"].location = (1170.0, -196.0)
    blocker_1.nodes["Position"].location = (30.0, -536.0)
    blocker_1.nodes["Separate XYZ"].location = (190.0, -536.0)
    blocker_1.nodes["Map Range.002"].location = (350.0, -536.0)
    blocker_1.nodes["Float Curve"].location = (530.0, -536.0)
    blocker_1.nodes["Math"].location = (790.0, -536.0)
    blocker_1.nodes["Combine XYZ.002"].location = (950.0, -536.0)
    blocker_1.nodes["Capture Attribute.003"].location = (1350.0, -196.0)
    blocker_1.nodes["Index.001"].location = (1170.0, -396.0)
    blocker_1.nodes["Compare.002"].location = (1350.0, -436.0)
    blocker_1.nodes["Mesh to Curve.001"].location = (1730.0, -96.0)
    blocker_1.nodes["Join Geometry.001"].location = (830.0, -76.0)
    blocker_1.nodes["Join Geometry.008"].location = (3570.0, -1492.0)
    blocker_1.nodes["Set Shade Smooth.003"].location = (3390.0, -612.0)
    blocker_1.nodes["Join Geometry.009"].location = (3750.0, -372.0)
    blocker_1.nodes["Frame"].location = (1200.0, -876.0)
    blocker_1.nodes["Store Named Attribute.003"].location = (1750.0, -36.0)
    blocker_1.nodes["Store Named Attribute.004"].location = (3190.0, -1492.0)
    blocker_1.nodes["Random Value.001"].location = (1390.0, -296.0)

    # Set dimensions
    blocker_1.nodes["Group Output"].width  = 140.0
    blocker_1.nodes["Group Output"].height = 100.0

    blocker_1.nodes["Join Geometry"].width  = 140.0
    blocker_1.nodes["Join Geometry"].height = 100.0

    blocker_1.nodes["Set Shade Smooth"].width  = 140.0
    blocker_1.nodes["Set Shade Smooth"].height = 100.0

    blocker_1.nodes["Store Named Attribute"].width  = 140.0
    blocker_1.nodes["Store Named Attribute"].height = 100.0

    blocker_1.nodes["Ico Sphere"].width  = 140.0
    blocker_1.nodes["Ico Sphere"].height = 100.0

    blocker_1.nodes["Transform Geometry"].width  = 140.0
    blocker_1.nodes["Transform Geometry"].height = 100.0

    blocker_1.nodes["Frame.001"].width  = 2280.0
    blocker_1.nodes["Frame.001"].height = 804.0

    blocker_1.nodes["Transform Geometry.001"].width  = 140.0
    blocker_1.nodes["Transform Geometry.001"].height = 100.0

    blocker_1.nodes["Mesh to SDF Grid"].width  = 140.0
    blocker_1.nodes["Mesh to SDF Grid"].height = 100.0

    blocker_1.nodes["Mesh to SDF Grid.001"].width  = 140.0
    blocker_1.nodes["Mesh to SDF Grid.001"].height = 100.0

    blocker_1.nodes["SDF Grid Boolean"].width  = 140.0
    blocker_1.nodes["SDF Grid Boolean"].height = 100.0

    blocker_1.nodes["Grid to Mesh"].width  = 140.0
    blocker_1.nodes["Grid to Mesh"].height = 100.0

    blocker_1.nodes["SDF Grid Fillet"].width  = 140.0
    blocker_1.nodes["SDF Grid Fillet"].height = 100.0

    blocker_1.nodes["Instance on Points"].width  = 140.0
    blocker_1.nodes["Instance on Points"].height = 100.0

    blocker_1.nodes["Curve Circle.001"].width  = 140.0
    blocker_1.nodes["Curve Circle.001"].height = 100.0

    blocker_1.nodes["Curve to Mesh.001"].width  = 140.0
    blocker_1.nodes["Curve to Mesh.001"].height = 100.0

    blocker_1.nodes["Position.002"].width  = 140.0
    blocker_1.nodes["Position.002"].height = 100.0

    blocker_1.nodes["Separate XYZ.001"].width  = 140.0
    blocker_1.nodes["Separate XYZ.001"].height = 100.0

    blocker_1.nodes["Compare.001"].width  = 140.0
    blocker_1.nodes["Compare.001"].height = 100.0

    blocker_1.nodes["Align Rotation to Vector"].width  = 140.0
    blocker_1.nodes["Align Rotation to Vector"].height = 100.0

    blocker_1.nodes["Normal.001"].width  = 140.0
    blocker_1.nodes["Normal.001"].height = 100.0

    blocker_1.nodes["Rotate Rotation"].width  = 140.0
    blocker_1.nodes["Rotate Rotation"].height = 100.0

    blocker_1.nodes["Rotate Rotation.001"].width  = 140.0
    blocker_1.nodes["Rotate Rotation.001"].height = 100.0

    blocker_1.nodes["Random Value"].width  = 140.0
    blocker_1.nodes["Random Value"].height = 100.0

    blocker_1.nodes["Realize Instances"].width  = 140.0
    blocker_1.nodes["Realize Instances"].height = 100.0

    blocker_1.nodes["Switch"].width  = 140.0
    blocker_1.nodes["Switch"].height = 100.0

    blocker_1.nodes["Join Geometry.002"].width  = 140.0
    blocker_1.nodes["Join Geometry.002"].height = 100.0

    blocker_1.nodes["Reroute"].width  = 10.0
    blocker_1.nodes["Reroute"].height = 100.0

    blocker_1.nodes["Group Input"].width  = 140.0
    blocker_1.nodes["Group Input"].height = 100.0

    blocker_1.nodes["Curve to Mesh.002"].width  = 140.0
    blocker_1.nodes["Curve to Mesh.002"].height = 100.0

    blocker_1.nodes["Curve Circle.002"].width  = 140.0
    blocker_1.nodes["Curve Circle.002"].height = 100.0

    blocker_1.nodes["Spline Parameter.001"].width  = 140.0
    blocker_1.nodes["Spline Parameter.001"].height = 100.0

    blocker_1.nodes["Float Curve.001"].width  = 240.0
    blocker_1.nodes["Float Curve.001"].height = 100.0

    blocker_1.nodes["Resample Curve.001"].width  = 140.0
    blocker_1.nodes["Resample Curve.001"].height = 100.0

    blocker_1.nodes["Quadratic Bézier.001"].width  = 140.0
    blocker_1.nodes["Quadratic Bézier.001"].height = 100.0

    blocker_1.nodes["Set Position.001"].width  = 140.0
    blocker_1.nodes["Set Position.001"].height = 100.0

    blocker_1.nodes["Vector Math.002"].width  = 140.0
    blocker_1.nodes["Vector Math.002"].height = 100.0

    blocker_1.nodes["Noise Texture.001"].width  = 145.0
    blocker_1.nodes["Noise Texture.001"].height = 100.0

    blocker_1.nodes["Vector Math.003"].width  = 140.0
    blocker_1.nodes["Vector Math.003"].height = 100.0

    blocker_1.nodes["Quadrilateral"].width  = 140.0
    blocker_1.nodes["Quadrilateral"].height = 100.0

    blocker_1.nodes["Fillet Curve"].width  = 140.0
    blocker_1.nodes["Fillet Curve"].height = 100.0

    blocker_1.nodes["Set Spline Type"].width  = 140.0
    blocker_1.nodes["Set Spline Type"].height = 100.0

    blocker_1.nodes["Index Switch"].width  = 140.0
    blocker_1.nodes["Index Switch"].height = 100.0

    blocker_1.nodes["Index"].width  = 140.0
    blocker_1.nodes["Index"].height = 100.0

    blocker_1.nodes["Fill Curve"].width  = 140.0
    blocker_1.nodes["Fill Curve"].height = 100.0

    blocker_1.nodes["Extrude Mesh.002"].width  = 140.0
    blocker_1.nodes["Extrude Mesh.002"].height = 100.0

    blocker_1.nodes["Flip Faces.002"].width  = 140.0
    blocker_1.nodes["Flip Faces.002"].height = 100.0

    blocker_1.nodes["Join Geometry.004"].width  = 140.0
    blocker_1.nodes["Join Geometry.004"].height = 100.0

    blocker_1.nodes["Merge by Distance.002"].width  = 140.0
    blocker_1.nodes["Merge by Distance.002"].height = 100.0

    blocker_1.nodes["Grid"].width  = 140.0
    blocker_1.nodes["Grid"].height = 100.0

    blocker_1.nodes["Extrude Mesh.003"].width  = 140.0
    blocker_1.nodes["Extrude Mesh.003"].height = 100.0

    blocker_1.nodes["Scale Elements"].width  = 140.0
    blocker_1.nodes["Scale Elements"].height = 100.0

    blocker_1.nodes["Merge by Distance.003"].width  = 140.0
    blocker_1.nodes["Merge by Distance.003"].height = 100.0

    blocker_1.nodes["Subdivide Mesh"].width  = 140.0
    blocker_1.nodes["Subdivide Mesh"].height = 100.0

    blocker_1.nodes["Mesh Boolean"].width  = 140.0
    blocker_1.nodes["Mesh Boolean"].height = 100.0

    blocker_1.nodes["Extrude Mesh.004"].width  = 140.0
    blocker_1.nodes["Extrude Mesh.004"].height = 100.0

    blocker_1.nodes["Flip Faces.003"].width  = 140.0
    blocker_1.nodes["Flip Faces.003"].height = 100.0

    blocker_1.nodes["Join Geometry.005"].width  = 140.0
    blocker_1.nodes["Join Geometry.005"].height = 100.0

    blocker_1.nodes["Merge by Distance.004"].width  = 140.0
    blocker_1.nodes["Merge by Distance.004"].height = 100.0

    blocker_1.nodes["Delete Geometry.002"].width  = 140.0
    blocker_1.nodes["Delete Geometry.002"].height = 100.0

    blocker_1.nodes["Set Position.002"].width  = 140.0
    blocker_1.nodes["Set Position.002"].height = 100.0

    blocker_1.nodes["Geometry Proximity"].width  = 140.0
    blocker_1.nodes["Geometry Proximity"].height = 100.0

    blocker_1.nodes["Separate Geometry"].width  = 140.0
    blocker_1.nodes["Separate Geometry"].height = 100.0

    blocker_1.nodes["Geometry Proximity.001"].width  = 140.0
    blocker_1.nodes["Geometry Proximity.001"].height = 100.0

    blocker_1.nodes["Compare.003"].width  = 140.0
    blocker_1.nodes["Compare.003"].height = 100.0

    blocker_1.nodes["Combine XYZ"].width  = 140.0
    blocker_1.nodes["Combine XYZ"].height = 100.0

    blocker_1.nodes["Map Range"].width  = 140.0
    blocker_1.nodes["Map Range"].height = 100.0

    blocker_1.nodes["Math.002"].width  = 140.0
    blocker_1.nodes["Math.002"].height = 100.0

    blocker_1.nodes["Math.003"].width  = 140.0
    blocker_1.nodes["Math.003"].height = 100.0

    blocker_1.nodes["Math.004"].width  = 140.0
    blocker_1.nodes["Math.004"].height = 100.0

    blocker_1.nodes["Curve to Mesh.003"].width  = 140.0
    blocker_1.nodes["Curve to Mesh.003"].height = 100.0

    blocker_1.nodes["Curve Circle.003"].width  = 140.0
    blocker_1.nodes["Curve Circle.003"].height = 100.0

    blocker_1.nodes["Transform Geometry.002"].width  = 140.0
    blocker_1.nodes["Transform Geometry.002"].height = 100.0

    blocker_1.nodes["Resample Curve.002"].width  = 140.0
    blocker_1.nodes["Resample Curve.002"].height = 100.0

    blocker_1.nodes["Frame.002"].width  = 1900.0
    blocker_1.nodes["Frame.002"].height = 877.0

    blocker_1.nodes["Frame.003"].width  = 1400.0
    blocker_1.nodes["Frame.003"].height = 460.0

    blocker_1.nodes["Transform Geometry.003"].width  = 140.0
    blocker_1.nodes["Transform Geometry.003"].height = 100.0

    blocker_1.nodes["Flip Faces.004"].width  = 140.0
    blocker_1.nodes["Flip Faces.004"].height = 100.0

    blocker_1.nodes["Join Geometry.006"].width  = 140.0
    blocker_1.nodes["Join Geometry.006"].height = 100.0

    blocker_1.nodes["Join Geometry.007"].width  = 140.0
    blocker_1.nodes["Join Geometry.007"].height = 100.0

    blocker_1.nodes["Set Shade Smooth.001"].width  = 140.0
    blocker_1.nodes["Set Shade Smooth.001"].height = 100.0

    blocker_1.nodes["Set Shade Smooth.002"].width  = 140.0
    blocker_1.nodes["Set Shade Smooth.002"].height = 100.0

    blocker_1.nodes["Compare.004"].width  = 140.0
    blocker_1.nodes["Compare.004"].height = 100.0

    blocker_1.nodes["Frame.004"].width  = 3920.0
    blocker_1.nodes["Frame.004"].height = 2523.0

    blocker_1.nodes["Sample UV Surface"].width  = 140.0
    blocker_1.nodes["Sample UV Surface"].height = 100.0

    blocker_1.nodes["Capture Attribute"].width  = 140.0
    blocker_1.nodes["Capture Attribute"].height = 100.0

    blocker_1.nodes["Capture Attribute.001"].width  = 140.0
    blocker_1.nodes["Capture Attribute.001"].height = 100.0

    blocker_1.nodes["Spline Parameter.002"].width  = 140.0
    blocker_1.nodes["Spline Parameter.002"].height = 100.0

    blocker_1.nodes["Combine XYZ.001"].width  = 140.0
    blocker_1.nodes["Combine XYZ.001"].height = 100.0

    blocker_1.nodes["Set Spline Cyclic"].width  = 140.0
    blocker_1.nodes["Set Spline Cyclic"].height = 100.0

    blocker_1.nodes["Set Curve Tilt"].width  = 140.0
    blocker_1.nodes["Set Curve Tilt"].height = 100.0

    blocker_1.nodes["Position.005"].width  = 140.0
    blocker_1.nodes["Position.005"].height = 100.0

    blocker_1.nodes["Set Position.003"].width  = 140.0
    blocker_1.nodes["Set Position.003"].height = 100.0

    blocker_1.nodes["Bounding Box"].width  = 140.0
    blocker_1.nodes["Bounding Box"].height = 100.0

    blocker_1.nodes["Position.006"].width  = 140.0
    blocker_1.nodes["Position.006"].height = 100.0

    blocker_1.nodes["Map Range.001"].width  = 140.0
    blocker_1.nodes["Map Range.001"].height = 100.0

    blocker_1.nodes["Sample UV Surface.001"].width  = 140.0
    blocker_1.nodes["Sample UV Surface.001"].height = 100.0

    blocker_1.nodes["Normal.003"].width  = 140.0
    blocker_1.nodes["Normal.003"].height = 100.0

    blocker_1.nodes["Separate XYZ.003"].width  = 140.0
    blocker_1.nodes["Separate XYZ.003"].height = 100.0

    blocker_1.nodes["Vector Math.004"].width  = 140.0
    blocker_1.nodes["Vector Math.004"].height = 100.0

    blocker_1.nodes["Math.005"].width  = 140.0
    blocker_1.nodes["Math.005"].height = 100.0

    blocker_1.nodes["Capture Attribute.002"].width  = 140.0
    blocker_1.nodes["Capture Attribute.002"].height = 100.0

    blocker_1.nodes["Noise Texture.002"].width  = 145.0
    blocker_1.nodes["Noise Texture.002"].height = 100.0

    blocker_1.nodes["Vector Math.006"].width  = 140.0
    blocker_1.nodes["Vector Math.006"].height = 100.0

    blocker_1.nodes["Vector Math.005"].width  = 140.0
    blocker_1.nodes["Vector Math.005"].height = 100.0

    blocker_1.nodes["Store Named Attribute.001"].width  = 140.0
    blocker_1.nodes["Store Named Attribute.001"].height = 100.0

    blocker_1.nodes["Frame.005"].width  = 611.0
    blocker_1.nodes["Frame.005"].height = 258.0

    blocker_1.nodes["Reroute.001"].width  = 10.0
    blocker_1.nodes["Reroute.001"].height = 100.0

    blocker_1.nodes["Reroute.002"].width  = 10.0
    blocker_1.nodes["Reroute.002"].height = 100.0

    blocker_1.nodes["Frame.006"].width  = 651.0
    blocker_1.nodes["Frame.006"].height = 429.0

    blocker_1.nodes["Frame.007"].width  = 1340.0
    blocker_1.nodes["Frame.007"].height = 817.0

    blocker_1.nodes["Frame.008"].width  = 1211.0
    blocker_1.nodes["Frame.008"].height = 989.0

    blocker_1.nodes["Frame.009"].width  = 7501.0
    blocker_1.nodes["Frame.009"].height = 3473.0

    blocker_1.nodes["Store Named Attribute.002"].width  = 140.0
    blocker_1.nodes["Store Named Attribute.002"].height = 100.0

    blocker_1.nodes["Switch.001"].width  = 140.0
    blocker_1.nodes["Switch.001"].height = 100.0

    blocker_1.nodes["Group Input.001"].width  = 140.0
    blocker_1.nodes["Group Input.001"].height = 100.0

    blocker_1.nodes["Curve to Mesh.004"].width  = 140.0
    blocker_1.nodes["Curve to Mesh.004"].height = 100.0

    blocker_1.nodes["Curve Circle.004"].width  = 140.0
    blocker_1.nodes["Curve Circle.004"].height = 100.0

    blocker_1.nodes["Set Spline Cyclic.001"].width  = 140.0
    blocker_1.nodes["Set Spline Cyclic.001"].height = 100.0

    blocker_1.nodes["Mesh to Curve"].width  = 140.0
    blocker_1.nodes["Mesh to Curve"].height = 100.0

    blocker_1.nodes["Resample Curve"].width  = 140.0
    blocker_1.nodes["Resample Curve"].height = 100.0

    blocker_1.nodes["Subdivide Mesh.001"].width  = 140.0
    blocker_1.nodes["Subdivide Mesh.001"].height = 100.0

    blocker_1.nodes["Geometry Proximity.002"].width  = 140.0
    blocker_1.nodes["Geometry Proximity.002"].height = 100.0

    blocker_1.nodes["Compare"].width  = 140.0
    blocker_1.nodes["Compare"].height = 100.0

    blocker_1.nodes["Delete Geometry"].width  = 140.0
    blocker_1.nodes["Delete Geometry"].height = 100.0

    blocker_1.nodes["Instance on Points.001"].width  = 140.0
    blocker_1.nodes["Instance on Points.001"].height = 100.0

    blocker_1.nodes["Align Rotation to Vector.001"].width  = 140.0
    blocker_1.nodes["Align Rotation to Vector.001"].height = 100.0

    blocker_1.nodes["Curve Tangent"].width  = 140.0
    blocker_1.nodes["Curve Tangent"].height = 100.0

    blocker_1.nodes["Ico Sphere.001"].width  = 140.0
    blocker_1.nodes["Ico Sphere.001"].height = 100.0

    blocker_1.nodes["Transform Geometry.004"].width  = 140.0
    blocker_1.nodes["Transform Geometry.004"].height = 100.0

    blocker_1.nodes["Realize Instances.001"].width  = 140.0
    blocker_1.nodes["Realize Instances.001"].height = 100.0

    blocker_1.nodes["Set Position"].width  = 140.0
    blocker_1.nodes["Set Position"].height = 100.0

    blocker_1.nodes["Position"].width  = 140.0
    blocker_1.nodes["Position"].height = 100.0

    blocker_1.nodes["Separate XYZ"].width  = 140.0
    blocker_1.nodes["Separate XYZ"].height = 100.0

    blocker_1.nodes["Map Range.002"].width  = 140.0
    blocker_1.nodes["Map Range.002"].height = 100.0

    blocker_1.nodes["Float Curve"].width  = 240.0
    blocker_1.nodes["Float Curve"].height = 100.0

    blocker_1.nodes["Math"].width  = 140.0
    blocker_1.nodes["Math"].height = 100.0

    blocker_1.nodes["Combine XYZ.002"].width  = 140.0
    blocker_1.nodes["Combine XYZ.002"].height = 100.0

    blocker_1.nodes["Capture Attribute.003"].width  = 140.0
    blocker_1.nodes["Capture Attribute.003"].height = 100.0

    blocker_1.nodes["Index.001"].width  = 140.0
    blocker_1.nodes["Index.001"].height = 100.0

    blocker_1.nodes["Compare.002"].width  = 140.0
    blocker_1.nodes["Compare.002"].height = 100.0

    blocker_1.nodes["Mesh to Curve.001"].width  = 140.0
    blocker_1.nodes["Mesh to Curve.001"].height = 100.0

    blocker_1.nodes["Join Geometry.001"].width  = 140.0
    blocker_1.nodes["Join Geometry.001"].height = 100.0

    blocker_1.nodes["Join Geometry.008"].width  = 140.0
    blocker_1.nodes["Join Geometry.008"].height = 100.0

    blocker_1.nodes["Set Shade Smooth.003"].width  = 140.0
    blocker_1.nodes["Set Shade Smooth.003"].height = 100.0

    blocker_1.nodes["Join Geometry.009"].width  = 140.0
    blocker_1.nodes["Join Geometry.009"].height = 100.0

    blocker_1.nodes["Frame"].width  = 1920.0
    blocker_1.nodes["Frame"].height = 668.0

    blocker_1.nodes["Store Named Attribute.003"].width  = 140.0
    blocker_1.nodes["Store Named Attribute.003"].height = 100.0

    blocker_1.nodes["Store Named Attribute.004"].width  = 140.0
    blocker_1.nodes["Store Named Attribute.004"].height = 100.0

    blocker_1.nodes["Random Value.001"].width  = 140.0
    blocker_1.nodes["Random Value.001"].height = 100.0


    # Initialize blocker_1 links

    # set_shade_smooth.Mesh -> group_output.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Set Shade Smooth"].outputs[0],
        blocker_1.nodes["Group Output"].inputs[0]
    )
    # join_geometry.Geometry -> set_shade_smooth.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Join Geometry"].outputs[0],
        blocker_1.nodes["Set Shade Smooth"].inputs[0]
    )
    # ico_sphere.Mesh -> transform_geometry.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Ico Sphere"].outputs[0],
        blocker_1.nodes["Transform Geometry"].inputs[0]
    )
    # store_named_attribute.Geometry -> join_geometry.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Store Named Attribute"].outputs[0],
        blocker_1.nodes["Join Geometry"].inputs[0]
    )
    # ico_sphere.Mesh -> transform_geometry_001.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Ico Sphere"].outputs[0],
        blocker_1.nodes["Transform Geometry.001"].inputs[0]
    )
    # transform_geometry.Geometry -> mesh_to_sdf_grid.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Transform Geometry"].outputs[0],
        blocker_1.nodes["Mesh to SDF Grid"].inputs[0]
    )
    # transform_geometry_001.Geometry -> mesh_to_sdf_grid_001.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Transform Geometry.001"].outputs[0],
        blocker_1.nodes["Mesh to SDF Grid.001"].inputs[0]
    )
    # mesh_to_sdf_grid.SDF Grid -> sdf_grid_boolean.Grid
    blocker_1.links.new(
        blocker_1.nodes["Mesh to SDF Grid"].outputs[0],
        blocker_1.nodes["SDF Grid Boolean"].inputs[1]
    )
    # sdf_grid_boolean.Grid -> sdf_grid_fillet.Grid
    blocker_1.links.new(
        blocker_1.nodes["SDF Grid Boolean"].outputs[0],
        blocker_1.nodes["SDF Grid Fillet"].inputs[0]
    )
    # sdf_grid_fillet.Grid -> grid_to_mesh.Grid
    blocker_1.links.new(
        blocker_1.nodes["SDF Grid Fillet"].outputs[0],
        blocker_1.nodes["Grid to Mesh"].inputs[0]
    )
    # grid_to_mesh.Mesh -> instance_on_points.Points
    blocker_1.links.new(
        blocker_1.nodes["Grid to Mesh"].outputs[0],
        blocker_1.nodes["Instance on Points"].inputs[0]
    )
    # curve_circle_001.Curve -> curve_to_mesh_001.Curve
    blocker_1.links.new(
        blocker_1.nodes["Curve Circle.001"].outputs[0],
        blocker_1.nodes["Curve to Mesh.001"].inputs[0]
    )
    # curve_circle_001.Curve -> curve_to_mesh_001.Profile Curve
    blocker_1.links.new(
        blocker_1.nodes["Curve Circle.001"].outputs[0],
        blocker_1.nodes["Curve to Mesh.001"].inputs[1]
    )
    # curve_to_mesh_001.Mesh -> instance_on_points.Instance
    blocker_1.links.new(
        blocker_1.nodes["Curve to Mesh.001"].outputs[0],
        blocker_1.nodes["Instance on Points"].inputs[2]
    )
    # position_002.Position -> separate_xyz_001.Vector
    blocker_1.links.new(
        blocker_1.nodes["Position.002"].outputs[0],
        blocker_1.nodes["Separate XYZ.001"].inputs[0]
    )
    # separate_xyz_001.X -> compare_001.A
    blocker_1.links.new(
        blocker_1.nodes["Separate XYZ.001"].outputs[0],
        blocker_1.nodes["Compare.001"].inputs[0]
    )
    # compare_001.Result -> instance_on_points.Selection
    blocker_1.links.new(
        blocker_1.nodes["Compare.001"].outputs[0],
        blocker_1.nodes["Instance on Points"].inputs[1]
    )
    # rotate_rotation_001.Rotation -> instance_on_points.Rotation
    blocker_1.links.new(
        blocker_1.nodes["Rotate Rotation.001"].outputs[0],
        blocker_1.nodes["Instance on Points"].inputs[5]
    )
    # normal_001.Normal -> align_rotation_to_vector.Vector
    blocker_1.links.new(
        blocker_1.nodes["Normal.001"].outputs[0],
        blocker_1.nodes["Align Rotation to Vector"].inputs[2]
    )
    # align_rotation_to_vector.Rotation -> rotate_rotation.Rotation
    blocker_1.links.new(
        blocker_1.nodes["Align Rotation to Vector"].outputs[0],
        blocker_1.nodes["Rotate Rotation"].inputs[0]
    )
    # rotate_rotation.Rotation -> rotate_rotation_001.Rotation
    blocker_1.links.new(
        blocker_1.nodes["Rotate Rotation"].outputs[0],
        blocker_1.nodes["Rotate Rotation.001"].inputs[0]
    )
    # random_value.Value -> rotate_rotation_001.Rotate By
    blocker_1.links.new(
        blocker_1.nodes["Random Value"].outputs[0],
        blocker_1.nodes["Rotate Rotation.001"].inputs[1]
    )
    # instance_on_points.Instances -> realize_instances.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Instance on Points"].outputs[0],
        blocker_1.nodes["Realize Instances"].inputs[0]
    )
    # realize_instances.Geometry -> switch.True
    blocker_1.links.new(
        blocker_1.nodes["Realize Instances"].outputs[0],
        blocker_1.nodes["Switch"].inputs[2]
    )
    # transform_geometry_001.Geometry -> join_geometry_002.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Transform Geometry.001"].outputs[0],
        blocker_1.nodes["Join Geometry.002"].inputs[0]
    )
    # reroute.Output -> switch.False
    blocker_1.links.new(
        blocker_1.nodes["Reroute"].outputs[0],
        blocker_1.nodes["Switch"].inputs[1]
    )
    # join_geometry_002.Geometry -> reroute.Input
    blocker_1.links.new(
        blocker_1.nodes["Join Geometry.002"].outputs[0],
        blocker_1.nodes["Reroute"].inputs[0]
    )
    # group_input.Decor -> switch.Switch
    blocker_1.links.new(
        blocker_1.nodes["Group Input"].outputs[0],
        blocker_1.nodes["Switch"].inputs[0]
    )
    # capture_attribute_001.Geometry -> curve_to_mesh_002.Curve
    blocker_1.links.new(
        blocker_1.nodes["Capture Attribute.001"].outputs[0],
        blocker_1.nodes["Curve to Mesh.002"].inputs[0]
    )
    # capture_attribute.Geometry -> curve_to_mesh_002.Profile Curve
    blocker_1.links.new(
        blocker_1.nodes["Capture Attribute"].outputs[0],
        blocker_1.nodes["Curve to Mesh.002"].inputs[1]
    )
    # spline_parameter_001.Factor -> float_curve_001.Value
    blocker_1.links.new(
        blocker_1.nodes["Spline Parameter.001"].outputs[0],
        blocker_1.nodes["Float Curve.001"].inputs[1]
    )
    # float_curve_001.Value -> curve_to_mesh_002.Scale
    blocker_1.links.new(
        blocker_1.nodes["Float Curve.001"].outputs[0],
        blocker_1.nodes["Curve to Mesh.002"].inputs[2]
    )
    # quadratic_b_zier_001.Curve -> resample_curve_001.Curve
    blocker_1.links.new(
        blocker_1.nodes["Quadratic Bézier.001"].outputs[0],
        blocker_1.nodes["Resample Curve.001"].inputs[0]
    )
    # vector_math_003.Vector -> noise_texture_001.Vector
    blocker_1.links.new(
        blocker_1.nodes["Vector Math.003"].outputs[0],
        blocker_1.nodes["Noise Texture.001"].inputs[0]
    )
    # set_spline_type.Curve -> fillet_curve.Curve
    blocker_1.links.new(
        blocker_1.nodes["Set Spline Type"].outputs[0],
        blocker_1.nodes["Fillet Curve"].inputs[0]
    )
    # quadrilateral.Curve -> set_spline_type.Curve
    blocker_1.links.new(
        blocker_1.nodes["Quadrilateral"].outputs[0],
        blocker_1.nodes["Set Spline Type"].inputs[0]
    )
    # index_switch.Output -> fillet_curve.Radius
    blocker_1.links.new(
        blocker_1.nodes["Index Switch"].outputs[0],
        blocker_1.nodes["Fillet Curve"].inputs[1]
    )
    # index.Index -> index_switch.Index
    blocker_1.links.new(
        blocker_1.nodes["Index"].outputs[0],
        blocker_1.nodes["Index Switch"].inputs[0]
    )
    # fillet_curve.Curve -> fill_curve.Curve
    blocker_1.links.new(
        blocker_1.nodes["Fillet Curve"].outputs[0],
        blocker_1.nodes["Fill Curve"].inputs[0]
    )
    # fill_curve.Mesh -> extrude_mesh_002.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Fill Curve"].outputs[0],
        blocker_1.nodes["Extrude Mesh.002"].inputs[0]
    )
    # fill_curve.Mesh -> flip_faces_002.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Fill Curve"].outputs[0],
        blocker_1.nodes["Flip Faces.002"].inputs[0]
    )
    # extrude_mesh_002.Mesh -> join_geometry_004.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Extrude Mesh.002"].outputs[0],
        blocker_1.nodes["Join Geometry.004"].inputs[0]
    )
    # join_geometry_004.Geometry -> merge_by_distance_002.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Join Geometry.004"].outputs[0],
        blocker_1.nodes["Merge by Distance.002"].inputs[0]
    )
    # grid.Mesh -> extrude_mesh_003.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Grid"].outputs[0],
        blocker_1.nodes["Extrude Mesh.003"].inputs[0]
    )
    # extrude_mesh_003.Mesh -> scale_elements.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Extrude Mesh.003"].outputs[0],
        blocker_1.nodes["Scale Elements"].inputs[0]
    )
    # extrude_mesh_003.Top -> scale_elements.Selection
    blocker_1.links.new(
        blocker_1.nodes["Extrude Mesh.003"].outputs[1],
        blocker_1.nodes["Scale Elements"].inputs[1]
    )
    # scale_elements.Geometry -> merge_by_distance_003.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Scale Elements"].outputs[0],
        blocker_1.nodes["Merge by Distance.003"].inputs[0]
    )
    # extrude_mesh_003.Top -> merge_by_distance_003.Selection
    blocker_1.links.new(
        blocker_1.nodes["Extrude Mesh.003"].outputs[1],
        blocker_1.nodes["Merge by Distance.003"].inputs[1]
    )
    # merge_by_distance_003.Geometry -> subdivide_mesh.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Merge by Distance.003"].outputs[0],
        blocker_1.nodes["Subdivide Mesh"].inputs[0]
    )
    # merge_by_distance_002.Geometry -> mesh_boolean.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Merge by Distance.002"].outputs[0],
        blocker_1.nodes["Mesh Boolean"].inputs[1]
    )
    # subdivide_mesh.Mesh -> extrude_mesh_004.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Subdivide Mesh"].outputs[0],
        blocker_1.nodes["Extrude Mesh.004"].inputs[0]
    )
    # subdivide_mesh.Mesh -> flip_faces_003.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Subdivide Mesh"].outputs[0],
        blocker_1.nodes["Flip Faces.003"].inputs[0]
    )
    # extrude_mesh_004.Mesh -> join_geometry_005.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Extrude Mesh.004"].outputs[0],
        blocker_1.nodes["Join Geometry.005"].inputs[0]
    )
    # join_geometry_005.Geometry -> merge_by_distance_004.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Join Geometry.005"].outputs[0],
        blocker_1.nodes["Merge by Distance.004"].inputs[0]
    )
    # mesh_boolean.Mesh -> delete_geometry_002.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Mesh Boolean"].outputs[0],
        blocker_1.nodes["Delete Geometry.002"].inputs[0]
    )
    # extrude_mesh_004.Top -> delete_geometry_002.Selection
    blocker_1.links.new(
        blocker_1.nodes["Extrude Mesh.004"].outputs[1],
        blocker_1.nodes["Delete Geometry.002"].inputs[1]
    )
    # delete_geometry_002.Geometry -> set_position_002.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Delete Geometry.002"].outputs[0],
        blocker_1.nodes["Set Position.002"].inputs[0]
    )
    # merge_by_distance_003.Geometry -> separate_geometry.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Merge by Distance.003"].outputs[0],
        blocker_1.nodes["Separate Geometry"].inputs[0]
    )
    # grid.Mesh -> geometry_proximity_001.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Grid"].outputs[0],
        blocker_1.nodes["Geometry Proximity.001"].inputs[0]
    )
    # geometry_proximity_001.Distance -> compare_003.A
    blocker_1.links.new(
        blocker_1.nodes["Geometry Proximity.001"].outputs[1],
        blocker_1.nodes["Compare.003"].inputs[0]
    )
    # compare_003.Result -> separate_geometry.Selection
    blocker_1.links.new(
        blocker_1.nodes["Compare.003"].outputs[0],
        blocker_1.nodes["Separate Geometry"].inputs[1]
    )
    # join_geometry_007.Geometry -> geometry_proximity.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Join Geometry.007"].outputs[0],
        blocker_1.nodes["Geometry Proximity"].inputs[0]
    )
    # math_003.Value -> combine_xyz.Z
    blocker_1.links.new(
        blocker_1.nodes["Math.003"].outputs[0],
        blocker_1.nodes["Combine XYZ"].inputs[2]
    )
    # combine_xyz.Vector -> set_position_002.Offset
    blocker_1.links.new(
        blocker_1.nodes["Combine XYZ"].outputs[0],
        blocker_1.nodes["Set Position.002"].inputs[3]
    )
    # geometry_proximity.Distance -> map_range.Value
    blocker_1.links.new(
        blocker_1.nodes["Geometry Proximity"].outputs[1],
        blocker_1.nodes["Map Range"].inputs[0]
    )
    # map_range.Result -> math_002.Value
    blocker_1.links.new(
        blocker_1.nodes["Map Range"].outputs[0],
        blocker_1.nodes["Math.002"].inputs[0]
    )
    # math_004.Value -> math_003.Value
    blocker_1.links.new(
        blocker_1.nodes["Math.004"].outputs[0],
        blocker_1.nodes["Math.003"].inputs[0]
    )
    # math_002.Value -> math_004.Value
    blocker_1.links.new(
        blocker_1.nodes["Math.002"].outputs[0],
        blocker_1.nodes["Math.004"].inputs[1]
    )
    # resample_curve_002.Curve -> curve_to_mesh_003.Curve
    blocker_1.links.new(
        blocker_1.nodes["Resample Curve.002"].outputs[0],
        blocker_1.nodes["Curve to Mesh.003"].inputs[0]
    )
    # capture_attribute_003.Geometry -> curve_to_mesh_003.Profile Curve
    blocker_1.links.new(
        blocker_1.nodes["Capture Attribute.003"].outputs[0],
        blocker_1.nodes["Curve to Mesh.003"].inputs[1]
    )
    # curve_circle_003.Curve -> transform_geometry_002.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Curve Circle.003"].outputs[0],
        blocker_1.nodes["Transform Geometry.002"].inputs[0]
    )
    # fillet_curve.Curve -> resample_curve_002.Curve
    blocker_1.links.new(
        blocker_1.nodes["Fillet Curve"].outputs[0],
        blocker_1.nodes["Resample Curve.002"].inputs[0]
    )
    # set_position_002.Geometry -> transform_geometry_003.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Set Position.002"].outputs[0],
        blocker_1.nodes["Transform Geometry.003"].inputs[0]
    )
    # transform_geometry_003.Geometry -> join_geometry_006.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Transform Geometry.003"].outputs[0],
        blocker_1.nodes["Join Geometry.006"].inputs[0]
    )
    # fill_curve.Mesh -> join_geometry_007.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Fill Curve"].outputs[0],
        blocker_1.nodes["Join Geometry.007"].inputs[0]
    )
    # set_position_002.Geometry -> flip_faces_004.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Set Position.002"].outputs[0],
        blocker_1.nodes["Flip Faces.004"].inputs[0]
    )
    # join_geometry_006.Geometry -> set_shade_smooth_001.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Join Geometry.006"].outputs[0],
        blocker_1.nodes["Set Shade Smooth.001"].inputs[0]
    )
    # set_shade_smooth_001.Mesh -> set_shade_smooth_002.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Set Shade Smooth.001"].outputs[0],
        blocker_1.nodes["Set Shade Smooth.002"].inputs[0]
    )
    # geometry_proximity.Distance -> compare_004.A
    blocker_1.links.new(
        blocker_1.nodes["Geometry Proximity"].outputs[1],
        blocker_1.nodes["Compare.004"].inputs[0]
    )
    # compare_004.Result -> set_shade_smooth_002.Selection
    blocker_1.links.new(
        blocker_1.nodes["Compare.004"].outputs[0],
        blocker_1.nodes["Set Shade Smooth.002"].inputs[1]
    )
    # reroute_002.Output -> sample_uv_surface.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Reroute.002"].outputs[0],
        blocker_1.nodes["Sample UV Surface"].inputs[0]
    )
    # set_spline_cyclic.Curve -> capture_attribute.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Set Spline Cyclic"].outputs[0],
        blocker_1.nodes["Capture Attribute"].inputs[0]
    )
    # set_curve_tilt.Curve -> capture_attribute_001.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Set Curve Tilt"].outputs[0],
        blocker_1.nodes["Capture Attribute.001"].inputs[0]
    )
    # spline_parameter_002.Factor -> capture_attribute_001.Factor
    blocker_1.links.new(
        blocker_1.nodes["Spline Parameter.002"].outputs[0],
        blocker_1.nodes["Capture Attribute.001"].inputs[1]
    )
    # spline_parameter_002.Factor -> capture_attribute.Factor
    blocker_1.links.new(
        blocker_1.nodes["Spline Parameter.002"].outputs[0],
        blocker_1.nodes["Capture Attribute"].inputs[1]
    )
    # curve_circle_002.Curve -> set_spline_cyclic.Curve
    blocker_1.links.new(
        blocker_1.nodes["Curve Circle.002"].outputs[0],
        blocker_1.nodes["Set Spline Cyclic"].inputs[0]
    )
    # resample_curve_001.Curve -> set_curve_tilt.Curve
    blocker_1.links.new(
        blocker_1.nodes["Resample Curve.001"].outputs[0],
        blocker_1.nodes["Set Curve Tilt"].inputs[0]
    )
    # reroute_001.Output -> sample_uv_surface.UV Map
    blocker_1.links.new(
        blocker_1.nodes["Reroute.001"].outputs[0],
        blocker_1.nodes["Sample UV Surface"].inputs[2]
    )
    # position_005.Position -> sample_uv_surface.Value
    blocker_1.links.new(
        blocker_1.nodes["Position.005"].outputs[0],
        blocker_1.nodes["Sample UV Surface"].inputs[1]
    )
    # store_named_attribute_002.Geometry -> set_position_003.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Store Named Attribute.002"].outputs[0],
        blocker_1.nodes["Set Position.003"].inputs[0]
    )
    # join_geometry_009.Geometry -> bounding_box.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Join Geometry.009"].outputs[0],
        blocker_1.nodes["Bounding Box"].inputs[0]
    )
    # position_006.Position -> map_range_001.Vector
    blocker_1.links.new(
        blocker_1.nodes["Position.006"].outputs[0],
        blocker_1.nodes["Map Range.001"].inputs[6]
    )
    # bounding_box.Min -> map_range_001.From Min
    blocker_1.links.new(
        blocker_1.nodes["Bounding Box"].outputs[1],
        blocker_1.nodes["Map Range.001"].inputs[7]
    )
    # bounding_box.Max -> map_range_001.From Max
    blocker_1.links.new(
        blocker_1.nodes["Bounding Box"].outputs[2],
        blocker_1.nodes["Map Range.001"].inputs[8]
    )
    # map_range_001.Vector -> sample_uv_surface.Sample UV
    blocker_1.links.new(
        blocker_1.nodes["Map Range.001"].outputs[1],
        blocker_1.nodes["Sample UV Surface"].inputs[3]
    )
    # reroute_002.Output -> sample_uv_surface_001.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Reroute.002"].outputs[0],
        blocker_1.nodes["Sample UV Surface.001"].inputs[0]
    )
    # reroute_001.Output -> sample_uv_surface_001.UV Map
    blocker_1.links.new(
        blocker_1.nodes["Reroute.001"].outputs[0],
        blocker_1.nodes["Sample UV Surface.001"].inputs[2]
    )
    # map_range_001.Vector -> sample_uv_surface_001.Sample UV
    blocker_1.links.new(
        blocker_1.nodes["Map Range.001"].outputs[1],
        blocker_1.nodes["Sample UV Surface.001"].inputs[3]
    )
    # normal_003.Normal -> sample_uv_surface_001.Value
    blocker_1.links.new(
        blocker_1.nodes["Normal.003"].outputs[0],
        blocker_1.nodes["Sample UV Surface.001"].inputs[1]
    )
    # position_006.Position -> separate_xyz_003.Vector
    blocker_1.links.new(
        blocker_1.nodes["Position.006"].outputs[0],
        blocker_1.nodes["Separate XYZ.003"].inputs[0]
    )
    # vector_math_004.Vector -> set_position_003.Offset
    blocker_1.links.new(
        blocker_1.nodes["Vector Math.004"].outputs[0],
        blocker_1.nodes["Set Position.003"].inputs[3]
    )
    # separate_xyz_003.Z -> math_005.Value
    blocker_1.links.new(
        blocker_1.nodes["Separate XYZ.003"].outputs[2],
        blocker_1.nodes["Math.005"].inputs[0]
    )
    # math_005.Value -> vector_math_004.Scale
    blocker_1.links.new(
        blocker_1.nodes["Math.005"].outputs[0],
        blocker_1.nodes["Vector Math.004"].inputs[3]
    )
    # capture_attribute_001.Factor -> combine_xyz_001.Y
    blocker_1.links.new(
        blocker_1.nodes["Capture Attribute.001"].outputs[1],
        blocker_1.nodes["Combine XYZ.001"].inputs[1]
    )
    # capture_attribute.Factor -> combine_xyz_001.X
    blocker_1.links.new(
        blocker_1.nodes["Capture Attribute"].outputs[1],
        blocker_1.nodes["Combine XYZ.001"].inputs[0]
    )
    # set_position_003.Geometry -> set_position_001.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Set Position.003"].outputs[0],
        blocker_1.nodes["Set Position.001"].inputs[0]
    )
    # join_geometry_009.Geometry -> capture_attribute_002.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Join Geometry.009"].outputs[0],
        blocker_1.nodes["Capture Attribute.002"].inputs[0]
    )
    # sample_uv_surface_001.Value -> capture_attribute_002.Normal
    blocker_1.links.new(
        blocker_1.nodes["Sample UV Surface.001"].outputs[0],
        blocker_1.nodes["Capture Attribute.002"].inputs[2]
    )
    # capture_attribute_002.Normal -> vector_math_004.Vector
    blocker_1.links.new(
        blocker_1.nodes["Capture Attribute.002"].outputs[2],
        blocker_1.nodes["Vector Math.004"].inputs[0]
    )
    # map_range_001.Vector -> capture_attribute_002.UVMap
    blocker_1.links.new(
        blocker_1.nodes["Map Range.001"].outputs[1],
        blocker_1.nodes["Capture Attribute.002"].inputs[3]
    )
    # capture_attribute_002.UVMap -> vector_math_003.Vector
    blocker_1.links.new(
        blocker_1.nodes["Capture Attribute.002"].outputs[3],
        blocker_1.nodes["Vector Math.003"].inputs[0]
    )
    # vector_math_006.Vector -> set_position_001.Offset
    blocker_1.links.new(
        blocker_1.nodes["Vector Math.006"].outputs[0],
        blocker_1.nodes["Set Position.001"].inputs[3]
    )
    # vector_math_002.Vector -> vector_math_006.Vector
    blocker_1.links.new(
        blocker_1.nodes["Vector Math.002"].outputs[0],
        blocker_1.nodes["Vector Math.006"].inputs[0]
    )
    # noise_texture_002.Color -> vector_math_005.Vector
    blocker_1.links.new(
        blocker_1.nodes["Noise Texture.002"].outputs[1],
        blocker_1.nodes["Vector Math.005"].inputs[0]
    )
    # vector_math_005.Vector -> vector_math_006.Vector
    blocker_1.links.new(
        blocker_1.nodes["Vector Math.005"].outputs[0],
        blocker_1.nodes["Vector Math.006"].inputs[1]
    )
    # switch_001.Output -> store_named_attribute_001.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Switch.001"].outputs[0],
        blocker_1.nodes["Store Named Attribute.001"].inputs[0]
    )
    # store_named_attribute_001.Geometry -> store_named_attribute.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Store Named Attribute.001"].outputs[0],
        blocker_1.nodes["Store Named Attribute"].inputs[0]
    )
    # sample_uv_surface.Value -> capture_attribute_002.Position
    blocker_1.links.new(
        blocker_1.nodes["Sample UV Surface"].outputs[0],
        blocker_1.nodes["Capture Attribute.002"].inputs[1]
    )
    # capture_attribute_002.Position -> set_position_003.Position
    blocker_1.links.new(
        blocker_1.nodes["Capture Attribute.002"].outputs[1],
        blocker_1.nodes["Set Position.003"].inputs[2]
    )
    # combine_xyz_001.Vector -> reroute_001.Input
    blocker_1.links.new(
        blocker_1.nodes["Combine XYZ.001"].outputs[0],
        blocker_1.nodes["Reroute.001"].inputs[0]
    )
    # curve_to_mesh_002.Mesh -> reroute_002.Input
    blocker_1.links.new(
        blocker_1.nodes["Curve to Mesh.002"].outputs[0],
        blocker_1.nodes["Reroute.002"].inputs[0]
    )
    # capture_attribute_002.Geometry -> store_named_attribute_002.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Capture Attribute.002"].outputs[0],
        blocker_1.nodes["Store Named Attribute.002"].inputs[0]
    )
    # capture_attribute_002.UVMap -> store_named_attribute_002.Value
    blocker_1.links.new(
        blocker_1.nodes["Capture Attribute.002"].outputs[3],
        blocker_1.nodes["Store Named Attribute.002"].inputs[3]
    )
    # noise_texture_001.Color -> vector_math_002.Vector
    blocker_1.links.new(
        blocker_1.nodes["Noise Texture.001"].outputs[1],
        blocker_1.nodes["Vector Math.002"].inputs[0]
    )
    # set_position_001.Geometry -> switch_001.True
    blocker_1.links.new(
        blocker_1.nodes["Set Position.001"].outputs[0],
        blocker_1.nodes["Switch.001"].inputs[2]
    )
    # curve_to_mesh_004.Mesh -> switch_001.False
    blocker_1.links.new(
        blocker_1.nodes["Curve to Mesh.004"].outputs[0],
        blocker_1.nodes["Switch.001"].inputs[1]
    )
    # group_input_001.Decor -> switch_001.Switch
    blocker_1.links.new(
        blocker_1.nodes["Group Input.001"].outputs[0],
        blocker_1.nodes["Switch.001"].inputs[0]
    )
    # curve_circle_004.Curve -> set_spline_cyclic_001.Curve
    blocker_1.links.new(
        blocker_1.nodes["Curve Circle.004"].outputs[0],
        blocker_1.nodes["Set Spline Cyclic.001"].inputs[0]
    )
    # set_spline_cyclic_001.Curve -> curve_to_mesh_004.Profile Curve
    blocker_1.links.new(
        blocker_1.nodes["Set Spline Cyclic.001"].outputs[0],
        blocker_1.nodes["Curve to Mesh.004"].inputs[1]
    )
    # set_curve_tilt.Curve -> curve_to_mesh_004.Curve
    blocker_1.links.new(
        blocker_1.nodes["Set Curve Tilt"].outputs[0],
        blocker_1.nodes["Curve to Mesh.004"].inputs[0]
    )
    # float_curve_001.Value -> curve_to_mesh_004.Scale
    blocker_1.links.new(
        blocker_1.nodes["Float Curve.001"].outputs[0],
        blocker_1.nodes["Curve to Mesh.004"].inputs[2]
    )
    # delete_geometry.Geometry -> mesh_to_curve.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Delete Geometry"].outputs[0],
        blocker_1.nodes["Mesh to Curve"].inputs[0]
    )
    # separate_geometry.Selection -> subdivide_mesh_001.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Separate Geometry"].outputs[0],
        blocker_1.nodes["Subdivide Mesh.001"].inputs[0]
    )
    # fill_curve.Mesh -> geometry_proximity_002.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Fill Curve"].outputs[0],
        blocker_1.nodes["Geometry Proximity.002"].inputs[0]
    )
    # geometry_proximity_002.Distance -> compare.A
    blocker_1.links.new(
        blocker_1.nodes["Geometry Proximity.002"].outputs[1],
        blocker_1.nodes["Compare"].inputs[0]
    )
    # subdivide_mesh_001.Mesh -> delete_geometry.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Subdivide Mesh.001"].outputs[0],
        blocker_1.nodes["Delete Geometry"].inputs[0]
    )
    # compare.Result -> delete_geometry.Selection
    blocker_1.links.new(
        blocker_1.nodes["Compare"].outputs[0],
        blocker_1.nodes["Delete Geometry"].inputs[1]
    )
    # resample_curve.Curve -> instance_on_points_001.Points
    blocker_1.links.new(
        blocker_1.nodes["Resample Curve"].outputs[0],
        blocker_1.nodes["Instance on Points.001"].inputs[0]
    )
    # align_rotation_to_vector_001.Rotation -> instance_on_points_001.Rotation
    blocker_1.links.new(
        blocker_1.nodes["Align Rotation to Vector.001"].outputs[0],
        blocker_1.nodes["Instance on Points.001"].inputs[5]
    )
    # curve_tangent.Tangent -> align_rotation_to_vector_001.Vector
    blocker_1.links.new(
        blocker_1.nodes["Curve Tangent"].outputs[0],
        blocker_1.nodes["Align Rotation to Vector.001"].inputs[2]
    )
    # transform_geometry_004.Geometry -> instance_on_points_001.Instance
    blocker_1.links.new(
        blocker_1.nodes["Transform Geometry.004"].outputs[0],
        blocker_1.nodes["Instance on Points.001"].inputs[2]
    )
    # ico_sphere_001.Mesh -> transform_geometry_004.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Ico Sphere.001"].outputs[0],
        blocker_1.nodes["Transform Geometry.004"].inputs[0]
    )
    # instance_on_points_001.Instances -> realize_instances_001.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Instance on Points.001"].outputs[0],
        blocker_1.nodes["Realize Instances.001"].inputs[0]
    )
    # transform_geometry_002.Geometry -> set_position.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Transform Geometry.002"].outputs[0],
        blocker_1.nodes["Set Position"].inputs[0]
    )
    # position.Position -> separate_xyz.Vector
    blocker_1.links.new(
        blocker_1.nodes["Position"].outputs[0],
        blocker_1.nodes["Separate XYZ"].inputs[0]
    )
    # separate_xyz.X -> map_range_002.Value
    blocker_1.links.new(
        blocker_1.nodes["Separate XYZ"].outputs[0],
        blocker_1.nodes["Map Range.002"].inputs[0]
    )
    # map_range_002.Result -> float_curve.Value
    blocker_1.links.new(
        blocker_1.nodes["Map Range.002"].outputs[0],
        blocker_1.nodes["Float Curve"].inputs[1]
    )
    # separate_xyz.Y -> math.Value
    blocker_1.links.new(
        blocker_1.nodes["Separate XYZ"].outputs[1],
        blocker_1.nodes["Math"].inputs[0]
    )
    # float_curve.Value -> math.Value
    blocker_1.links.new(
        blocker_1.nodes["Float Curve"].outputs[0],
        blocker_1.nodes["Math"].inputs[1]
    )
    # separate_xyz.X -> combine_xyz_002.X
    blocker_1.links.new(
        blocker_1.nodes["Separate XYZ"].outputs[0],
        blocker_1.nodes["Combine XYZ.002"].inputs[0]
    )
    # math.Value -> combine_xyz_002.Y
    blocker_1.links.new(
        blocker_1.nodes["Math"].outputs[0],
        blocker_1.nodes["Combine XYZ.002"].inputs[1]
    )
    # separate_xyz.Z -> combine_xyz_002.Z
    blocker_1.links.new(
        blocker_1.nodes["Separate XYZ"].outputs[2],
        blocker_1.nodes["Combine XYZ.002"].inputs[2]
    )
    # combine_xyz_002.Vector -> set_position.Position
    blocker_1.links.new(
        blocker_1.nodes["Combine XYZ.002"].outputs[0],
        blocker_1.nodes["Set Position"].inputs[2]
    )
    # set_position.Geometry -> capture_attribute_003.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Set Position"].outputs[0],
        blocker_1.nodes["Capture Attribute.003"].inputs[0]
    )
    # index_001.Index -> compare_002.A
    blocker_1.links.new(
        blocker_1.nodes["Index.001"].outputs[0],
        blocker_1.nodes["Compare.002"].inputs[2]
    )
    # compare_002.Result -> capture_attribute_003.Result
    blocker_1.links.new(
        blocker_1.nodes["Compare.002"].outputs[0],
        blocker_1.nodes["Capture Attribute.003"].inputs[1]
    )
    # curve_to_mesh_003.Mesh -> mesh_to_curve_001.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Curve to Mesh.003"].outputs[0],
        blocker_1.nodes["Mesh to Curve.001"].inputs[0]
    )
    # capture_attribute_003.Result -> mesh_to_curve_001.Selection
    blocker_1.links.new(
        blocker_1.nodes["Capture Attribute.003"].outputs[1],
        blocker_1.nodes["Mesh to Curve.001"].inputs[1]
    )
    # mesh_to_curve_001.Curve -> join_geometry_001.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Mesh to Curve.001"].outputs[0],
        blocker_1.nodes["Join Geometry.001"].inputs[0]
    )
    # join_geometry_001.Geometry -> resample_curve.Curve
    blocker_1.links.new(
        blocker_1.nodes["Join Geometry.001"].outputs[0],
        blocker_1.nodes["Resample Curve"].inputs[0]
    )
    # store_named_attribute_003.Geometry -> join_geometry_008.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Store Named Attribute.003"].outputs[0],
        blocker_1.nodes["Join Geometry.008"].inputs[0]
    )
    # join_geometry_008.Geometry -> set_shade_smooth_003.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Join Geometry.008"].outputs[0],
        blocker_1.nodes["Set Shade Smooth.003"].inputs[0]
    )
    # set_shade_smooth_002.Mesh -> join_geometry_009.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Set Shade Smooth.002"].outputs[0],
        blocker_1.nodes["Join Geometry.009"].inputs[0]
    )
    # realize_instances_001.Geometry -> store_named_attribute_003.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Realize Instances.001"].outputs[0],
        blocker_1.nodes["Store Named Attribute.003"].inputs[0]
    )
    # curve_to_mesh_003.Mesh -> store_named_attribute_004.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Curve to Mesh.003"].outputs[0],
        blocker_1.nodes["Store Named Attribute.004"].inputs[0]
    )
    # random_value_001.Value -> instance_on_points_001.Scale
    blocker_1.links.new(
        blocker_1.nodes["Random Value.001"].outputs[0],
        blocker_1.nodes["Instance on Points.001"].inputs[6]
    )
    # switch.Output -> join_geometry.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Switch"].outputs[0],
        blocker_1.nodes["Join Geometry"].inputs[0]
    )
    # mesh_to_sdf_grid_001.SDF Grid -> sdf_grid_boolean.Grid
    blocker_1.links.new(
        blocker_1.nodes["Mesh to SDF Grid.001"].outputs[0],
        blocker_1.nodes["SDF Grid Boolean"].inputs[1]
    )
    # transform_geometry.Geometry -> join_geometry_002.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Transform Geometry"].outputs[0],
        blocker_1.nodes["Join Geometry.002"].inputs[0]
    )
    # flip_faces_002.Mesh -> join_geometry_004.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Flip Faces.002"].outputs[0],
        blocker_1.nodes["Join Geometry.004"].inputs[0]
    )
    # flip_faces_003.Mesh -> join_geometry_005.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Flip Faces.003"].outputs[0],
        blocker_1.nodes["Join Geometry.005"].inputs[0]
    )
    # merge_by_distance_004.Geometry -> mesh_boolean.Mesh
    blocker_1.links.new(
        blocker_1.nodes["Merge by Distance.004"].outputs[0],
        blocker_1.nodes["Mesh Boolean"].inputs[1]
    )
    # flip_faces_004.Mesh -> join_geometry_006.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Flip Faces.004"].outputs[0],
        blocker_1.nodes["Join Geometry.006"].inputs[0]
    )
    # separate_geometry.Selection -> join_geometry_007.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Separate Geometry"].outputs[0],
        blocker_1.nodes["Join Geometry.007"].inputs[0]
    )
    # mesh_to_curve.Curve -> join_geometry_001.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Mesh to Curve"].outputs[0],
        blocker_1.nodes["Join Geometry.001"].inputs[0]
    )
    # store_named_attribute_004.Geometry -> join_geometry_008.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Store Named Attribute.004"].outputs[0],
        blocker_1.nodes["Join Geometry.008"].inputs[0]
    )
    # set_shade_smooth_003.Mesh -> join_geometry_009.Geometry
    blocker_1.links.new(
        blocker_1.nodes["Set Shade Smooth.003"].outputs[0],
        blocker_1.nodes["Join Geometry.009"].inputs[0]
    )

    return blocker_1


if __name__ == "__main__":
    # Maps node tree creation functions to the node tree 
    # name, such that we don't recreate node trees unnecessarily
    node_tree_names : dict[typing.Callable, str] = {}

    blocker = blocker_1_node_group(node_tree_names)
    node_tree_names[blocker_1_node_group] = blocker.name

