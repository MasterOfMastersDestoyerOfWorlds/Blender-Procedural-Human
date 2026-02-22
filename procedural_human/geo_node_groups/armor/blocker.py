import bpy
from mathutils import Euler, Vector
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, math_op

@geo_node_group
def create_blocker_group():
    group_name = "Blocker"
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

    join_geometry = nodes.new("GeometryNodeJoinGeometry")

    set_shade_smooth = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.domain = "FACE"
    set_shade_smooth.inputs[1].default_value = True
    set_shade_smooth.inputs[2].default_value = True
    links.new(set_shade_smooth.outputs[0], group_output.inputs[0])
    links.new(join_geometry.outputs[0], set_shade_smooth.inputs[0])

    store_named_attribute = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.data_type = "BOOLEAN"
    store_named_attribute.domain = "POINT"
    store_named_attribute.inputs[1].default_value = True
    store_named_attribute.inputs[2].default_value = "blocker"
    store_named_attribute.inputs[3].default_value = True
    links.new(store_named_attribute.outputs[0], join_geometry.inputs[0])

    ico_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere.inputs[0].default_value = 0.1300000250339508
    ico_sphere.inputs[1].default_value = 3

    transform_geometry = nodes.new("GeometryNodeTransform")
    transform_geometry.inputs[1].default_value = "Components"
    transform_geometry.inputs[2].default_value = Vector((-0.03999999910593033, 0.0, 0.25))
    transform_geometry.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry.inputs[4].default_value = Vector((1.0, 1.0, 1.2000000476837158))
    links.new(ico_sphere.outputs[0], transform_geometry.inputs[0])

    frame_001 = nodes.new("NodeFrame")
    frame_001.text = None
    frame_001.shrink = True
    frame_001.label_size = 20

    transform_geometry_001 = nodes.new("GeometryNodeTransform")
    transform_geometry_001.inputs[1].default_value = "Components"
    transform_geometry_001.inputs[2].default_value = Vector((-0.10000000149011612, 0.019999999552965164, 0.33000001311302185))
    transform_geometry_001.inputs[3].default_value = Euler((0.0, -0.13439033925533295, 0.18500488996505737), 'XYZ')
    transform_geometry_001.inputs[4].default_value = Vector((1.0199999809265137, 0.8300000429153442, 0.8400001525878906))
    links.new(ico_sphere.outputs[0], transform_geometry_001.inputs[0])

    mesh_to_s_d_f_grid = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid.inputs[1].default_value = 0.004999999888241291
    mesh_to_s_d_f_grid.inputs[2].default_value = 2
    links.new(transform_geometry.outputs[0], mesh_to_s_d_f_grid.inputs[0])

    mesh_to_s_d_f_grid_001 = nodes.new("GeometryNodeMeshToSDFGrid")
    mesh_to_s_d_f_grid_001.inputs[1].default_value = 0.004999999888241291
    mesh_to_s_d_f_grid_001.inputs[2].default_value = 2
    links.new(transform_geometry_001.outputs[0], mesh_to_s_d_f_grid_001.inputs[0])

    s_d_f_grid_boolean = nodes.new("GeometryNodeSDFGridBoolean")
    s_d_f_grid_boolean.operation = "UNION"
    s_d_f_grid_boolean.inputs[0].default_value = 0.0
    links.new(mesh_to_s_d_f_grid.outputs[0], s_d_f_grid_boolean.inputs[1])
    links.new(mesh_to_s_d_f_grid_001.outputs[0], s_d_f_grid_boolean.inputs[1])

    grid_to_mesh = nodes.new("GeometryNodeGridToMesh")
    grid_to_mesh.inputs[1].default_value = 0.0
    grid_to_mesh.inputs[2].default_value = 0.0

    s_d_f_grid_fillet = nodes.new("GeometryNodeSDFGridFillet")
    s_d_f_grid_fillet.inputs[1].default_value = 3
    links.new(s_d_f_grid_boolean.outputs[0], s_d_f_grid_fillet.inputs[0])
    links.new(s_d_f_grid_fillet.outputs[0], grid_to_mesh.inputs[0])

    instance_on_points = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.inputs[3].default_value = False
    instance_on_points.inputs[4].default_value = 0
    instance_on_points.inputs[6].default_value = Vector((0.800000011920929, 0.800000011920929, 0.800000011920929))
    links.new(grid_to_mesh.outputs[0], instance_on_points.inputs[0])

    curve_circle_001 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_001.mode = "RADIUS"
    curve_circle_001.inputs[0].default_value = 9
    curve_circle_001.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_001.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_001.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_001.inputs[4].default_value = 0.004999999888241291

    curve_to_mesh_001 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_001.inputs[2].default_value = 0.21000000834465027
    curve_to_mesh_001.inputs[3].default_value = False
    links.new(curve_circle_001.outputs[0], curve_to_mesh_001.inputs[0])
    links.new(curve_circle_001.outputs[0], curve_to_mesh_001.inputs[1])
    links.new(curve_to_mesh_001.outputs[0], instance_on_points.inputs[2])

    position_002 = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z_001 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_002.outputs[0], separate_x_y_z_001.inputs[0])

    compare_001 = nodes.new("FunctionNodeCompare")
    compare_001.operation = "LESS_THAN"
    compare_001.data_type = "FLOAT"
    compare_001.mode = "ELEMENT"
    compare_001.inputs[1].default_value = -0.09999999403953552
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
    links.new(separate_x_y_z_001.outputs[0], compare_001.inputs[0])
    links.new(compare_001.outputs[0], instance_on_points.inputs[1])

    align_rotation_to_vector = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector.axis = "Z"
    align_rotation_to_vector.pivot_axis = "AUTO"
    align_rotation_to_vector.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector.inputs[1].default_value = 1.0

    normal_001 = nodes.new("GeometryNodeInputNormal")
    normal_001.legacy_corner_normals = False
    links.new(normal_001.outputs[0], align_rotation_to_vector.inputs[2])

    rotate_rotation = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation.rotation_space = "LOCAL"
    rotate_rotation.inputs[1].default_value = Euler((-0.3707079291343689, 0.3525564670562744, 0.0), 'XYZ')
    links.new(align_rotation_to_vector.outputs[0], rotate_rotation.inputs[0])

    rotate_rotation_001 = nodes.new("FunctionNodeRotateRotation")
    rotate_rotation_001.rotation_space = "LOCAL"
    links.new(rotate_rotation_001.outputs[0], instance_on_points.inputs[5])
    links.new(rotate_rotation.outputs[0], rotate_rotation_001.inputs[0])

    random_value = nodes.new("FunctionNodeRandomValue")
    random_value.data_type = "FLOAT_VECTOR"
    random_value.inputs[0].default_value = [-0.10000000149011612, -0.10000000149011612, -0.10000000149011612]
    random_value.inputs[1].default_value = [0.10000000149011612, 0.10000000149011612, 0.10000000149011612]
    random_value.inputs[2].default_value = 0.0
    random_value.inputs[3].default_value = 1.0
    random_value.inputs[4].default_value = 0
    random_value.inputs[5].default_value = 100
    random_value.inputs[6].default_value = 0.5
    random_value.inputs[7].default_value = 0
    random_value.inputs[8].default_value = 2
    links.new(random_value.outputs[0], rotate_rotation_001.inputs[1])

    realize_instances = nodes.new("GeometryNodeRealizeInstances")
    realize_instances.inputs[1].default_value = True
    realize_instances.inputs[2].default_value = True
    realize_instances.inputs[3].default_value = 0
    links.new(instance_on_points.outputs[0], realize_instances.inputs[0])

    switch = nodes.new("GeometryNodeSwitch")
    switch.input_type = "GEOMETRY"
    links.new(switch.outputs[0], join_geometry.inputs[0])
    links.new(realize_instances.outputs[0], switch.inputs[2])

    join_geometry_002 = nodes.new("GeometryNodeJoinGeometry")
    links.new(transform_geometry_001.outputs[0], join_geometry_002.inputs[0])
    links.new(transform_geometry.outputs[0], join_geometry_002.inputs[0])

    reroute = nodes.new("NodeReroute")
    reroute.socket_idname = "NodeSocketGeometry"
    links.new(reroute.outputs[0], switch.inputs[1])
    links.new(join_geometry_002.outputs[0], reroute.inputs[0])

    group_input = nodes.new("NodeGroupInput")
    links.new(group_input.outputs[0], switch.inputs[0])

    curve_to_mesh_002 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_002.inputs[3].default_value = False

    curve_circle_002 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_002.mode = "RADIUS"
    curve_circle_002.inputs[0].default_value = 105
    curve_circle_002.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_002.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_002.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_002.inputs[4].default_value = 0.10000000149011612

    spline_parameter_001 = nodes.new("GeometryNodeSplineParameter")

    float_curve_001 = nodes.new("ShaderNodeFloatCurve")
    float_curve_001.inputs[0].default_value = 1.0
    links.new(spline_parameter_001.outputs[0], float_curve_001.inputs[1])
    links.new(float_curve_001.outputs[0], curve_to_mesh_002.inputs[2])

    resample_curve_001 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.keep_last_segment = True
    resample_curve_001.inputs[1].default_value = True
    resample_curve_001.inputs[2].default_value = "Count"
    resample_curve_001.inputs[3].default_value = 34
    resample_curve_001.inputs[4].default_value = 0.10000000149011612

    quadratic_bézier_001 = nodes.new("GeometryNodeCurveQuadraticBezier")
    quadratic_bézier_001.inputs[0].default_value = 16
    quadratic_bézier_001.inputs[1].default_value = Vector((0.0, -0.009999999776482582, 0.4000000059604645))
    quadratic_bézier_001.inputs[2].default_value = Vector((0.0, 0.009999999776482582, 0.44999995827674866))
    quadratic_bézier_001.inputs[3].default_value = Vector((0.0, -0.04999999701976776, 0.5199999809265137))
    links.new(quadratic_bézier_001.outputs[0], resample_curve_001.inputs[0])

    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.inputs[1].default_value = True
    set_position_001.inputs[2].default_value = [0.0, 0.0, 0.0]

    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.operation = "SCALE"
    vector_math_002.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_002.inputs[3].default_value = 0.0020000000949949026

    noise_texture_001 = nodes.new("ShaderNodeTexNoise")
    noise_texture_001.noise_dimensions = "2D"
    noise_texture_001.noise_type = "FBM"
    noise_texture_001.normalize = False
    noise_texture_001.inputs[1].default_value = 0.0
    noise_texture_001.inputs[2].default_value = 5.669999599456787
    noise_texture_001.inputs[3].default_value = 0.0
    noise_texture_001.inputs[4].default_value = 0.5
    noise_texture_001.inputs[5].default_value = 2.0
    noise_texture_001.inputs[6].default_value = 0.0
    noise_texture_001.inputs[7].default_value = 1.0
    noise_texture_001.inputs[8].default_value = 0.0
    links.new(noise_texture_001.outputs[1], vector_math_002.inputs[0])

    vector_math_003 = nodes.new("ShaderNodeVectorMath")
    vector_math_003.operation = "MULTIPLY"
    vector_math_003.inputs[1].default_value = [1.0, 2.5999999046325684, 24.950000762939453]
    vector_math_003.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_003.inputs[3].default_value = 1.0
    links.new(vector_math_003.outputs[0], noise_texture_001.inputs[0])

    quadrilateral = nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
    quadrilateral.mode = "RECTANGLE"
    quadrilateral.inputs[0].default_value = 0.5
    quadrilateral.inputs[1].default_value = 0.15000000596046448
    quadrilateral.inputs[2].default_value = 4.0
    quadrilateral.inputs[3].default_value = 2.0
    quadrilateral.inputs[4].default_value = 1.0
    quadrilateral.inputs[5].default_value = 3.0
    quadrilateral.inputs[6].default_value = 1.0
    quadrilateral.inputs[7].default_value = Vector((-1.0, -1.0, 0.0))
    quadrilateral.inputs[8].default_value = Vector((1.0, -1.0, 0.0))
    quadrilateral.inputs[9].default_value = Vector((1.0, 1.0, 0.0))
    quadrilateral.inputs[10].default_value = Vector((-1.0, 1.0, 0.0))

    fillet_curve = nodes.new("GeometryNodeFilletCurve")
    fillet_curve.inputs[2].default_value = False
    fillet_curve.inputs[3].default_value = "Bézier"
    fillet_curve.inputs[4].default_value = 1

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.spline_type = "BEZIER"
    set_spline_type.inputs[1].default_value = True
    links.new(set_spline_type.outputs[0], fillet_curve.inputs[0])
    links.new(quadrilateral.outputs[0], set_spline_type.inputs[0])

    index_switch = nodes.new("GeometryNodeIndexSwitch")
    index_switch.data_type = "FLOAT"
    index_switch.inputs[1].default_value = 0.09000000357627869
    index_switch.inputs[2].default_value = 0.09000000357627869
    links.new(index_switch.outputs[0], fillet_curve.inputs[1])

    index = nodes.new("GeometryNodeInputIndex")
    links.new(index.outputs[0], index_switch.inputs[0])

    fill_curve = nodes.new("GeometryNodeFillCurve")
    fill_curve.inputs[1].default_value = 0
    fill_curve.inputs[2].default_value = "N-gons"
    links.new(fillet_curve.outputs[0], fill_curve.inputs[0])

    extrude_mesh_002 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_002.mode = "FACES"
    extrude_mesh_002.inputs[1].default_value = True
    extrude_mesh_002.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    extrude_mesh_002.inputs[3].default_value = 0.009999999776482582
    extrude_mesh_002.inputs[4].default_value = False
    links.new(fill_curve.outputs[0], extrude_mesh_002.inputs[0])

    flip_faces_002 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_002.inputs[1].default_value = True
    links.new(fill_curve.outputs[0], flip_faces_002.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    links.new(extrude_mesh_002.outputs[0], join_geometry_004.inputs[0])
    links.new(flip_faces_002.outputs[0], join_geometry_004.inputs[0])

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.inputs[1].default_value = True
    merge_by_distance_002.inputs[2].default_value = "All"
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    links.new(join_geometry_004.outputs[0], merge_by_distance_002.inputs[0])

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.inputs[0].default_value = 0.6000000238418579
    grid.inputs[1].default_value = 0.30000001192092896
    grid.inputs[2].default_value = 13
    grid.inputs[3].default_value = 7

    extrude_mesh_003 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_003.mode = "FACES"
    extrude_mesh_003.inputs[1].default_value = True
    extrude_mesh_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    extrude_mesh_003.inputs[3].default_value = 0.0
    extrude_mesh_003.inputs[4].default_value = True
    links.new(grid.outputs[0], extrude_mesh_003.inputs[0])

    scale_elements = nodes.new("GeometryNodeScaleElements")
    scale_elements.domain = "FACE"
    scale_elements.inputs[2].default_value = 0.0
    scale_elements.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    scale_elements.inputs[4].default_value = "Uniform"
    scale_elements.inputs[5].default_value = [1.0, 0.0, 0.0]
    links.new(extrude_mesh_003.outputs[0], scale_elements.inputs[0])
    links.new(extrude_mesh_003.outputs[1], scale_elements.inputs[1])

    merge_by_distance_003 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_003.inputs[2].default_value = "All"
    merge_by_distance_003.inputs[3].default_value = 0.0010000000474974513
    links.new(scale_elements.outputs[0], merge_by_distance_003.inputs[0])
    links.new(extrude_mesh_003.outputs[1], merge_by_distance_003.inputs[1])

    subdivide_mesh = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh.inputs[1].default_value = 3
    links.new(merge_by_distance_003.outputs[0], subdivide_mesh.inputs[0])

    mesh_boolean = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean.operation = "INTERSECT"
    mesh_boolean.solver = "MANIFOLD"
    mesh_boolean.inputs[2].default_value = False
    mesh_boolean.inputs[3].default_value = False
    links.new(merge_by_distance_002.outputs[0], mesh_boolean.inputs[1])

    extrude_mesh_004 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_004.mode = "FACES"
    extrude_mesh_004.inputs[1].default_value = True
    extrude_mesh_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    extrude_mesh_004.inputs[3].default_value = 0.009999999776482582
    extrude_mesh_004.inputs[4].default_value = False
    links.new(subdivide_mesh.outputs[0], extrude_mesh_004.inputs[0])

    flip_faces_003 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_003.inputs[1].default_value = True
    links.new(subdivide_mesh.outputs[0], flip_faces_003.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    links.new(extrude_mesh_004.outputs[0], join_geometry_005.inputs[0])
    links.new(flip_faces_003.outputs[0], join_geometry_005.inputs[0])

    merge_by_distance_004 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_004.inputs[1].default_value = True
    merge_by_distance_004.inputs[2].default_value = "All"
    merge_by_distance_004.inputs[3].default_value = 0.0010000000474974513
    links.new(join_geometry_005.outputs[0], merge_by_distance_004.inputs[0])
    links.new(merge_by_distance_004.outputs[0], mesh_boolean.inputs[1])

    delete_geometry_002 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.mode = "ALL"
    delete_geometry_002.domain = "POINT"
    links.new(mesh_boolean.outputs[0], delete_geometry_002.inputs[0])
    links.new(extrude_mesh_004.outputs[1], delete_geometry_002.inputs[1])

    set_position_002 = nodes.new("GeometryNodeSetPosition")
    set_position_002.inputs[1].default_value = True
    set_position_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(delete_geometry_002.outputs[0], set_position_002.inputs[0])

    geometry_proximity = nodes.new("GeometryNodeProximity")
    geometry_proximity.target_element = "EDGES"
    geometry_proximity.inputs[1].default_value = 0
    geometry_proximity.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity.inputs[3].default_value = 0

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.domain = "EDGE"
    links.new(merge_by_distance_003.outputs[0], separate_geometry.inputs[0])

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.target_element = "EDGES"
    geometry_proximity_001.inputs[1].default_value = 0
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_001.inputs[3].default_value = 0
    links.new(grid.outputs[0], geometry_proximity_001.inputs[0])

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
    links.new(geometry_proximity_001.outputs[1], compare_003.inputs[0])
    links.new(compare_003.outputs[0], separate_geometry.inputs[1])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.inputs[0].default_value = 0.0
    combine_x_y_z.inputs[1].default_value = 0.0
    links.new(combine_x_y_z.outputs[0], set_position_002.inputs[3])

    map_range = nodes.new("ShaderNodeMapRange")
    map_range.clamp = True
    map_range.interpolation_type = "LINEAR"
    map_range.data_type = "FLOAT"
    map_range.inputs[1].default_value = 0.0
    map_range.inputs[2].default_value = 0.009999999776482582
    map_range.inputs[3].default_value = 1.0
    map_range.inputs[4].default_value = 0.0
    map_range.inputs[5].default_value = 4.0
    map_range.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(geometry_proximity.outputs[1], map_range.inputs[0])

    height_falloff = math_op(group, "POWER", map_range.outputs[0], 2.0)
    links.new(
        math_op(group, "MULTIPLY", math_op(group, "SUBTRACT", 1.0, height_falloff), 0.0020000000949949026),
        combine_x_y_z.inputs[2],
    )

    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.inputs[2].default_value = 1.0
    curve_to_mesh_003.inputs[3].default_value = False

    curve_circle_003 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_003.mode = "RADIUS"
    curve_circle_003.inputs[0].default_value = 57
    curve_circle_003.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_003.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_003.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_003.inputs[4].default_value = 0.004999999888241291

    transform_geometry_002 = nodes.new("GeometryNodeTransform")
    transform_geometry_002.inputs[1].default_value = "Components"
    transform_geometry_002.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_002.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_002.inputs[4].default_value = Vector((1.0, 0.5, 1.0))
    links.new(curve_circle_003.outputs[0], transform_geometry_002.inputs[0])

    resample_curve_002 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.keep_last_segment = True
    resample_curve_002.inputs[1].default_value = True
    resample_curve_002.inputs[2].default_value = "Length"
    resample_curve_002.inputs[3].default_value = 10
    resample_curve_002.inputs[4].default_value = 0.009999999776482582
    links.new(resample_curve_002.outputs[0], curve_to_mesh_003.inputs[0])
    links.new(fillet_curve.outputs[0], resample_curve_002.inputs[0])

    frame_002 = nodes.new("NodeFrame")
    frame_002.text = None
    frame_002.shrink = True
    frame_002.label_size = 20

    frame_003 = nodes.new("NodeFrame")
    frame_003.text = None
    frame_003.shrink = True
    frame_003.label_size = 20

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.inputs[1].default_value = "Components"
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_003.inputs[4].default_value = Vector((1.0, 1.0, -1.0))
    links.new(set_position_002.outputs[0], transform_geometry_003.inputs[0])

    flip_faces_004 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_004.inputs[1].default_value = True
    links.new(set_position_002.outputs[0], flip_faces_004.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    links.new(transform_geometry_003.outputs[0], join_geometry_006.inputs[0])
    links.new(flip_faces_004.outputs[0], join_geometry_006.inputs[0])

    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_007.outputs[0], geometry_proximity.inputs[0])
    links.new(separate_geometry.outputs[0], join_geometry_007.inputs[0])
    links.new(fill_curve.outputs[0], join_geometry_007.inputs[0])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.domain = "FACE"
    set_shade_smooth_001.inputs[1].default_value = True
    set_shade_smooth_001.inputs[2].default_value = True
    links.new(join_geometry_006.outputs[0], set_shade_smooth_001.inputs[0])

    set_shade_smooth_002 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_002.domain = "EDGE"
    set_shade_smooth_002.inputs[2].default_value = False
    links.new(set_shade_smooth_001.outputs[0], set_shade_smooth_002.inputs[0])

    compare_004 = nodes.new("FunctionNodeCompare")
    compare_004.operation = "EQUAL"
    compare_004.data_type = "FLOAT"
    compare_004.mode = "ELEMENT"
    compare_004.inputs[1].default_value = 0.0
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
    compare_004.inputs[12].default_value = 0.0010000000474974513
    links.new(geometry_proximity.outputs[1], compare_004.inputs[0])
    links.new(compare_004.outputs[0], set_shade_smooth_002.inputs[1])

    frame_004 = nodes.new("NodeFrame")
    frame_004.text = None
    frame_004.shrink = True
    frame_004.label_size = 20

    sample_u_v_surface = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface.data_type = "FLOAT_VECTOR"

    capture_attribute = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.capture_items.new("FLOAT", "Value")
    capture_attribute.active_index = 0
    capture_attribute.domain = "POINT"
    links.new(capture_attribute.outputs[0], curve_to_mesh_002.inputs[1])

    capture_attribute_001 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_001.capture_items.new("FLOAT", "Value")
    capture_attribute_001.active_index = 0
    capture_attribute_001.domain = "POINT"
    links.new(capture_attribute_001.outputs[0], curve_to_mesh_002.inputs[0])

    spline_parameter_002 = nodes.new("GeometryNodeSplineParameter")
    links.new(spline_parameter_002.outputs[0], capture_attribute_001.inputs[1])
    links.new(spline_parameter_002.outputs[0], capture_attribute.inputs[1])

    combine_x_y_z_001 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_001.inputs[2].default_value = 0.0
    links.new(capture_attribute_001.outputs[1], combine_x_y_z_001.inputs[1])
    links.new(capture_attribute.outputs[1], combine_x_y_z_001.inputs[0])

    set_spline_cyclic = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic.inputs[1].default_value = True
    set_spline_cyclic.inputs[2].default_value = False
    links.new(set_spline_cyclic.outputs[0], capture_attribute.inputs[0])
    links.new(curve_circle_002.outputs[0], set_spline_cyclic.inputs[0])

    set_curve_tilt = nodes.new("GeometryNodeSetCurveTilt")
    set_curve_tilt.inputs[1].default_value = True
    set_curve_tilt.inputs[2].default_value = -1.472708821296692
    links.new(set_curve_tilt.outputs[0], capture_attribute_001.inputs[0])
    links.new(resample_curve_001.outputs[0], set_curve_tilt.inputs[0])

    position_005 = nodes.new("GeometryNodeInputPosition")
    links.new(position_005.outputs[0], sample_u_v_surface.inputs[1])

    set_position_003 = nodes.new("GeometryNodeSetPosition")
    set_position_003.inputs[1].default_value = True
    links.new(set_position_003.outputs[0], set_position_001.inputs[0])

    bounding_box = nodes.new("GeometryNodeBoundBox")
    bounding_box.inputs[1].default_value = False

    position_006 = nodes.new("GeometryNodeInputPosition")

    map_range_001 = nodes.new("ShaderNodeMapRange")
    map_range_001.clamp = True
    map_range_001.interpolation_type = "LINEAR"
    map_range_001.data_type = "FLOAT_VECTOR"
    map_range_001.inputs[0].default_value = 1.0
    map_range_001.inputs[1].default_value = 0.0
    map_range_001.inputs[2].default_value = 1.0
    map_range_001.inputs[3].default_value = 0.0
    map_range_001.inputs[4].default_value = 1.0
    map_range_001.inputs[5].default_value = 4.0
    map_range_001.inputs[9].default_value = [0.009999999776482582, 0.009999999776482582, 0.009999999776482582]
    map_range_001.inputs[10].default_value = [0.9900000095367432, 0.9900000095367432, 0.9900000095367432]
    map_range_001.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(position_006.outputs[0], map_range_001.inputs[6])
    links.new(bounding_box.outputs[1], map_range_001.inputs[7])
    links.new(bounding_box.outputs[2], map_range_001.inputs[8])
    links.new(map_range_001.outputs[1], sample_u_v_surface.inputs[3])

    sample_u_v_surface_001 = nodes.new("GeometryNodeSampleUVSurface")
    sample_u_v_surface_001.data_type = "FLOAT_VECTOR"
    links.new(map_range_001.outputs[1], sample_u_v_surface_001.inputs[3])

    normal_003 = nodes.new("GeometryNodeInputNormal")
    normal_003.legacy_corner_normals = False
    links.new(normal_003.outputs[0], sample_u_v_surface_001.inputs[1])

    separate_x_y_z_003 = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position_006.outputs[0], separate_x_y_z_003.inputs[0])

    vector_math_004 = nodes.new("ShaderNodeVectorMath")
    vector_math_004.operation = "SCALE"
    vector_math_004.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_004.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(vector_math_004.outputs[0], set_position_003.inputs[3])

    math_005 = nodes.new("ShaderNodeMath")
    math_005.operation = "MULTIPLY"
    math_005.inputs[1].default_value = 1.2499998807907104
    math_005.inputs[2].default_value = 0.5
    links.new(separate_x_y_z_003.outputs[2], math_005.inputs[0])
    links.new(math_005.outputs[0], vector_math_004.inputs[3])

    capture_attribute_002 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_002.capture_items.new("VECTOR", "Value")
    capture_attribute_002.capture_items.new("VECTOR", "Value")
    capture_attribute_002.capture_items.new("VECTOR", "Value")
    capture_attribute_002.active_index = 0
    capture_attribute_002.domain = "POINT"
    links.new(sample_u_v_surface.outputs[0], capture_attribute_002.inputs[1])
    links.new(capture_attribute_002.outputs[1], set_position_003.inputs[2])
    links.new(sample_u_v_surface_001.outputs[0], capture_attribute_002.inputs[2])
    links.new(capture_attribute_002.outputs[2], vector_math_004.inputs[0])
    links.new(map_range_001.outputs[1], capture_attribute_002.inputs[3])
    links.new(capture_attribute_002.outputs[3], vector_math_003.inputs[0])

    noise_texture_002 = nodes.new("ShaderNodeTexNoise")
    noise_texture_002.noise_dimensions = "4D"
    noise_texture_002.noise_type = "FBM"
    noise_texture_002.normalize = False
    noise_texture_002.inputs[0].default_value = [0.0, 0.0, 0.0]
    noise_texture_002.inputs[1].default_value = 44.769989013671875
    noise_texture_002.inputs[2].default_value = 17.969999313354492
    noise_texture_002.inputs[3].default_value = 0.0
    noise_texture_002.inputs[4].default_value = 0.5
    noise_texture_002.inputs[5].default_value = 2.0
    noise_texture_002.inputs[6].default_value = 0.0
    noise_texture_002.inputs[7].default_value = 1.0
    noise_texture_002.inputs[8].default_value = 0.0

    vector_math_006 = nodes.new("ShaderNodeVectorMath")
    vector_math_006.operation = "ADD"
    vector_math_006.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_006.inputs[3].default_value = 1.0
    links.new(vector_math_006.outputs[0], set_position_001.inputs[3])
    links.new(vector_math_002.outputs[0], vector_math_006.inputs[0])

    vector_math_005 = nodes.new("ShaderNodeVectorMath")
    vector_math_005.operation = "SCALE"
    vector_math_005.inputs[1].default_value = [0.0, 0.0, 0.0]
    vector_math_005.inputs[2].default_value = [0.0, 0.0, 0.0]
    vector_math_005.inputs[3].default_value = 0.006000000052154064
    links.new(noise_texture_002.outputs[1], vector_math_005.inputs[0])
    links.new(vector_math_005.outputs[0], vector_math_006.inputs[1])

    store_named_attribute_001 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.data_type = "BOOLEAN"
    store_named_attribute_001.domain = "POINT"
    store_named_attribute_001.inputs[1].default_value = True
    store_named_attribute_001.inputs[2].default_value = "skip"
    store_named_attribute_001.inputs[3].default_value = True
    links.new(store_named_attribute_001.outputs[0], store_named_attribute.inputs[0])

    frame_005 = nodes.new("NodeFrame")
    frame_005.text = None
    frame_005.shrink = True
    frame_005.label_size = 20

    reroute_001 = nodes.new("NodeReroute")
    reroute_001.socket_idname = "NodeSocketVector"
    links.new(reroute_001.outputs[0], sample_u_v_surface.inputs[2])
    links.new(reroute_001.outputs[0], sample_u_v_surface_001.inputs[2])
    links.new(combine_x_y_z_001.outputs[0], reroute_001.inputs[0])

    reroute_002 = nodes.new("NodeReroute")
    reroute_002.socket_idname = "NodeSocketGeometry"
    links.new(reroute_002.outputs[0], sample_u_v_surface.inputs[0])
    links.new(reroute_002.outputs[0], sample_u_v_surface_001.inputs[0])
    links.new(curve_to_mesh_002.outputs[0], reroute_002.inputs[0])

    frame_006 = nodes.new("NodeFrame")
    frame_006.text = None
    frame_006.shrink = True
    frame_006.label_size = 20

    frame_007 = nodes.new("NodeFrame")
    frame_007.text = None
    frame_007.shrink = True
    frame_007.label_size = 20

    frame_008 = nodes.new("NodeFrame")
    frame_008.text = None
    frame_008.shrink = True
    frame_008.label_size = 20

    frame_009 = nodes.new("NodeFrame")
    frame_009.text = None
    frame_009.shrink = True
    frame_009.label_size = 20

    store_named_attribute_002 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.data_type = "FLOAT2"
    store_named_attribute_002.domain = "CORNER"
    store_named_attribute_002.inputs[1].default_value = True
    store_named_attribute_002.inputs[2].default_value = "UVMap"
    links.new(store_named_attribute_002.outputs[0], set_position_003.inputs[0])
    links.new(capture_attribute_002.outputs[0], store_named_attribute_002.inputs[0])
    links.new(capture_attribute_002.outputs[3], store_named_attribute_002.inputs[3])

    switch_001 = nodes.new("GeometryNodeSwitch")
    switch_001.input_type = "GEOMETRY"
    links.new(switch_001.outputs[0], store_named_attribute_001.inputs[0])
    links.new(set_position_001.outputs[0], switch_001.inputs[2])

    group_input_001 = nodes.new("NodeGroupInput")
    links.new(group_input_001.outputs[0], switch_001.inputs[0])

    curve_to_mesh_004 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_004.inputs[3].default_value = False
    links.new(curve_to_mesh_004.outputs[0], switch_001.inputs[1])
    links.new(set_curve_tilt.outputs[0], curve_to_mesh_004.inputs[0])
    links.new(float_curve_001.outputs[0], curve_to_mesh_004.inputs[2])

    curve_circle_004 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_004.mode = "RADIUS"
    curve_circle_004.inputs[0].default_value = 24
    curve_circle_004.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_004.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_004.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_004.inputs[4].default_value = 0.10000000149011612

    set_spline_cyclic_001 = nodes.new("GeometryNodeSetSplineCyclic")
    set_spline_cyclic_001.inputs[1].default_value = True
    set_spline_cyclic_001.inputs[2].default_value = False
    links.new(curve_circle_004.outputs[0], set_spline_cyclic_001.inputs[0])
    links.new(set_spline_cyclic_001.outputs[0], curve_to_mesh_004.inputs[1])

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.mode = "EDGES"
    mesh_to_curve.inputs[1].default_value = True

    resample_curve = nodes.new("GeometryNodeResampleCurve")
    resample_curve.keep_last_segment = True
    resample_curve.inputs[1].default_value = True
    resample_curve.inputs[2].default_value = "Length"
    resample_curve.inputs[3].default_value = 101
    resample_curve.inputs[4].default_value = 0.003000000026077032

    subdivide_mesh_001 = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh_001.inputs[1].default_value = 4
    links.new(separate_geometry.outputs[0], subdivide_mesh_001.inputs[0])

    geometry_proximity_002 = nodes.new("GeometryNodeProximity")
    geometry_proximity_002.target_element = "FACES"
    geometry_proximity_002.inputs[1].default_value = 0
    geometry_proximity_002.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_002.inputs[3].default_value = 0
    links.new(fill_curve.outputs[0], geometry_proximity_002.inputs[0])

    compare = nodes.new("FunctionNodeCompare")
    compare.operation = "GREATER_THAN"
    compare.data_type = "FLOAT"
    compare.mode = "ELEMENT"
    compare.inputs[1].default_value = 0.0010000000474974513
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
    compare.inputs[12].default_value = 0.0010000000474974513
    links.new(geometry_proximity_002.outputs[1], compare.inputs[0])

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "POINT"
    links.new(delete_geometry.outputs[0], mesh_to_curve.inputs[0])
    links.new(subdivide_mesh_001.outputs[0], delete_geometry.inputs[0])
    links.new(compare.outputs[0], delete_geometry.inputs[1])

    instance_on_points_001 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_001.inputs[1].default_value = True
    instance_on_points_001.inputs[3].default_value = False
    instance_on_points_001.inputs[4].default_value = 0
    links.new(resample_curve.outputs[0], instance_on_points_001.inputs[0])

    align_rotation_to_vector_001 = nodes.new("FunctionNodeAlignRotationToVector")
    align_rotation_to_vector_001.axis = "X"
    align_rotation_to_vector_001.pivot_axis = "AUTO"
    align_rotation_to_vector_001.inputs[0].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    align_rotation_to_vector_001.inputs[1].default_value = 1.0
    links.new(align_rotation_to_vector_001.outputs[0], instance_on_points_001.inputs[5])

    curve_tangent = nodes.new("GeometryNodeInputTangent")
    links.new(curve_tangent.outputs[0], align_rotation_to_vector_001.inputs[2])

    ico_sphere_001 = nodes.new("GeometryNodeMeshIcoSphere")
    ico_sphere_001.inputs[0].default_value = 0.0007999999797903001
    ico_sphere_001.inputs[1].default_value = 2

    transform_geometry_004 = nodes.new("GeometryNodeTransform")
    transform_geometry_004.inputs[1].default_value = "Components"
    transform_geometry_004.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_004.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_004.inputs[4].default_value = Vector((1.5, 0.5, 0.3199999928474426))
    links.new(transform_geometry_004.outputs[0], instance_on_points_001.inputs[2])
    links.new(ico_sphere_001.outputs[0], transform_geometry_004.inputs[0])

    realize_instances_001 = nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.inputs[1].default_value = True
    realize_instances_001.inputs[2].default_value = True
    realize_instances_001.inputs[3].default_value = 0
    links.new(instance_on_points_001.outputs[0], realize_instances_001.inputs[0])

    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.inputs[1].default_value = True
    set_position.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    links.new(transform_geometry_002.outputs[0], set_position.inputs[0])

    position = nodes.new("GeometryNodeInputPosition")

    separate_x_y_z = nodes.new("ShaderNodeSeparateXYZ")
    links.new(position.outputs[0], separate_x_y_z.inputs[0])

    map_range_002 = nodes.new("ShaderNodeMapRange")
    map_range_002.clamp = True
    map_range_002.interpolation_type = "LINEAR"
    map_range_002.data_type = "FLOAT"
    map_range_002.inputs[1].default_value = -0.004999999888241291
    map_range_002.inputs[2].default_value = 0.004999999888241291
    map_range_002.inputs[3].default_value = 0.0
    map_range_002.inputs[4].default_value = 1.0
    map_range_002.inputs[5].default_value = 4.0
    map_range_002.inputs[6].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[7].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[8].default_value = [1.0, 1.0, 1.0]
    map_range_002.inputs[9].default_value = [0.0, 0.0, 0.0]
    map_range_002.inputs[10].default_value = [1.0, 1.0, 1.0]
    map_range_002.inputs[11].default_value = [4.0, 4.0, 4.0]
    links.new(separate_x_y_z.outputs[0], map_range_002.inputs[0])

    float_curve = nodes.new("ShaderNodeFloatCurve")
    float_curve.inputs[0].default_value = 1.0
    links.new(map_range_002.outputs[0], float_curve.inputs[1])

    y_offset = math_op(group, "MULTIPLY", separate_x_y_z.outputs[1], float_curve.outputs[0])

    combine_x_y_z_002 = nodes.new("ShaderNodeCombineXYZ")
    links.new(separate_x_y_z.outputs[0], combine_x_y_z_002.inputs[0])
    links.new(y_offset, combine_x_y_z_002.inputs[1])
    links.new(separate_x_y_z.outputs[2], combine_x_y_z_002.inputs[2])
    links.new(combine_x_y_z_002.outputs[0], set_position.inputs[2])

    capture_attribute_003 = nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute_003.capture_items.new("BOOLEAN", "Value")
    capture_attribute_003.active_index = 0
    capture_attribute_003.domain = "POINT"
    links.new(capture_attribute_003.outputs[0], curve_to_mesh_003.inputs[1])
    links.new(set_position.outputs[0], capture_attribute_003.inputs[0])

    index_001 = nodes.new("GeometryNodeInputIndex")

    compare_002 = nodes.new("FunctionNodeCompare")
    compare_002.operation = "EQUAL"
    compare_002.data_type = "INT"
    compare_002.mode = "ELEMENT"
    compare_002.inputs[0].default_value = 0.0
    compare_002.inputs[1].default_value = 0.0
    compare_002.inputs[3].default_value = 39
    compare_002.inputs[4].default_value = [0.0, 0.0, 0.0]
    compare_002.inputs[5].default_value = [0.0, 0.0, 0.0]
    compare_002.inputs[6].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[7].default_value = [0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0]
    compare_002.inputs[8].default_value = ""
    compare_002.inputs[9].default_value = ""
    compare_002.inputs[10].default_value = 0.8999999761581421
    compare_002.inputs[11].default_value = 0.08726649731397629
    compare_002.inputs[12].default_value = 0.0010000000474974513
    links.new(index_001.outputs[0], compare_002.inputs[2])
    links.new(compare_002.outputs[0], capture_attribute_003.inputs[1])

    mesh_to_curve_001 = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve_001.mode = "EDGES"
    links.new(curve_to_mesh_003.outputs[0], mesh_to_curve_001.inputs[0])
    links.new(capture_attribute_003.outputs[1], mesh_to_curve_001.inputs[1])

    join_geometry_001 = nodes.new("GeometryNodeJoinGeometry")
    links.new(mesh_to_curve_001.outputs[0], join_geometry_001.inputs[0])
    links.new(mesh_to_curve.outputs[0], join_geometry_001.inputs[0])
    links.new(join_geometry_001.outputs[0], resample_curve.inputs[0])

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")

    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.domain = "FACE"
    set_shade_smooth_003.inputs[1].default_value = True
    set_shade_smooth_003.inputs[2].default_value = True
    links.new(join_geometry_008.outputs[0], set_shade_smooth_003.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    links.new(join_geometry_009.outputs[0], bounding_box.inputs[0])
    links.new(join_geometry_009.outputs[0], capture_attribute_002.inputs[0])
    links.new(set_shade_smooth_002.outputs[0], join_geometry_009.inputs[0])
    links.new(set_shade_smooth_003.outputs[0], join_geometry_009.inputs[0])

    frame = nodes.new("NodeFrame")
    frame.text = None
    frame.shrink = True
    frame.label_size = 20

    store_named_attribute_003 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.data_type = "BOOLEAN"
    store_named_attribute_003.domain = "POINT"
    store_named_attribute_003.inputs[1].default_value = True
    store_named_attribute_003.inputs[2].default_value = "stitching"
    store_named_attribute_003.inputs[3].default_value = True
    links.new(store_named_attribute_003.outputs[0], join_geometry_008.inputs[0])
    links.new(realize_instances_001.outputs[0], store_named_attribute_003.inputs[0])

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    store_named_attribute_004.inputs[1].default_value = True
    store_named_attribute_004.inputs[2].default_value = "piping"
    store_named_attribute_004.inputs[3].default_value = True
    links.new(store_named_attribute_004.outputs[0], join_geometry_008.inputs[0])
    links.new(curve_to_mesh_003.outputs[0], store_named_attribute_004.inputs[0])

    random_value_001 = nodes.new("FunctionNodeRandomValue")
    random_value_001.data_type = "FLOAT_VECTOR"
    random_value_001.inputs[0].default_value = [0.699999988079071, 0.699999988079071, 0.699999988079071]
    random_value_001.inputs[1].default_value = [1.0, 1.5, 1.2999999523162842]
    random_value_001.inputs[2].default_value = 0.0
    random_value_001.inputs[3].default_value = 1.0
    random_value_001.inputs[4].default_value = 0
    random_value_001.inputs[5].default_value = 100
    random_value_001.inputs[6].default_value = 0.5
    random_value_001.inputs[7].default_value = 0
    random_value_001.inputs[8].default_value = 0
    links.new(random_value_001.outputs[0], instance_on_points_001.inputs[6])

    auto_layout_nodes(group)
    return group
