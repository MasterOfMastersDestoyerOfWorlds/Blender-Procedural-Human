import bpy
from mathutils import Vector, Color, Matrix, Euler
from procedural_human.decorators.geo_node_decorator import geo_node_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group
from procedural_human.geo_node_groups.node_helpers import combine_xyz, compare_op, create_float_curve, math_op, separate_xyz, vec_math_op
from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.geo_node_groups.armor.blocker.collar.gambeson_pattern.piping import create_blocker_collar_gambeson_pattern_piping_group
from procedural_human.geo_node_groups.armor.blocker.collar.gambeson_pattern.quilting import create_blocker_collar_gambeson_pattern_quilting_group
from procedural_human.geo_node_groups.armor.blocker.collar.gambeson_pattern.stitching import create_blocker_collar_gambeson_pattern_stitching_group


@geo_node_group
def create_blocker_collar_gambeson_pattern_group():
    group_name = "BlockerCollarGambesonPattern"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True
    piping = nodes.new("GeometryNodeGroup")
    piping.node_tree = create_blocker_collar_gambeson_pattern_piping_group()

    quilting = nodes.new("GeometryNodeGroup")
    quilting.node_tree = create_blocker_collar_gambeson_pattern_quilting_group()

    stitching = nodes.new("GeometryNodeGroup")
    stitching.node_tree = create_blocker_collar_gambeson_pattern_stitching_group()

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

    index = nodes.new("GeometryNodeInputIndex")

    grid = nodes.new("GeometryNodeMeshGrid")
    grid.inputs[0].default_value = 0.6000000238418579
    grid.inputs[1].default_value = 0.30000001192092896
    grid.inputs[2].default_value = 13
    grid.inputs[3].default_value = 7

    transform_geometry_003 = nodes.new("GeometryNodeTransform")
    transform_geometry_003.inputs[1].default_value = "Components"
    transform_geometry_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_003.inputs[3].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    transform_geometry_003.inputs[4].default_value = Vector((1.0, 1.0, -1.0))

    flip_faces_004 = nodes.new("GeometryNodeFlipFaces")
    flip_faces_004.inputs[1].default_value = True

    compare_004 = compare_op(group, "EQUAL", "FLOAT", quilting.outputs[1], 0.0)
    compare_004.node.inputs[10].default_value = 0.8999999761581421
    compare_004.node.inputs[11].default_value = 0.08726649731397629
    compare_004.node.inputs[12].default_value = 0.0010000000474974513

    store_named_attribute_004 = nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.data_type = "BOOLEAN"
    store_named_attribute_004.domain = "POINT"
    store_named_attribute_004.inputs[1].default_value = True
    store_named_attribute_004.inputs[2].default_value = "piping"
    store_named_attribute_004.inputs[3].default_value = True

    set_spline_type = nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.spline_type = "BEZIER"
    set_spline_type.inputs[1].default_value = True
    links.new(quadrilateral.outputs[0], set_spline_type.inputs[0])

    index_switch = nodes.new("GeometryNodeIndexSwitch")
    index_switch.data_type = "FLOAT"
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.inputs[1].default_value = 0.09000000357627869
    index_switch.inputs[2].default_value = 0.09000000357627869
    links.new(index.outputs[0], index_switch.inputs[0])

    geometry_proximity_001 = nodes.new("GeometryNodeProximity")
    geometry_proximity_001.target_element = "EDGES"
    geometry_proximity_001.inputs[1].default_value = 0
    geometry_proximity_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    geometry_proximity_001.inputs[3].default_value = 0
    links.new(grid.outputs[0], geometry_proximity_001.inputs[0])

    extrude_mesh_003 = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_003.mode = "FACES"
    extrude_mesh_003.inputs[1].default_value = True
    extrude_mesh_003.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    extrude_mesh_003.inputs[3].default_value = 0.0
    extrude_mesh_003.inputs[4].default_value = True
    links.new(grid.outputs[0], extrude_mesh_003.inputs[0])

    join_geometry_006 = nodes.new("GeometryNodeJoinGeometry")
    links.new(transform_geometry_003.outputs[0], join_geometry_006.inputs[0])
    links.new(flip_faces_004.outputs[0], join_geometry_006.inputs[0])

    join_geometry_008 = nodes.new("GeometryNodeJoinGeometry")
    links.new(store_named_attribute_004.outputs[0], join_geometry_008.inputs[0])

    fillet_curve = nodes.new("GeometryNodeFilletCurve")
    fillet_curve.inputs[2].default_value = False
    fillet_curve.inputs[3].default_value = "Bézier"
    fillet_curve.inputs[4].default_value = 1
    links.new(set_spline_type.outputs[0], fillet_curve.inputs[0])
    links.new(index_switch.outputs[0], fillet_curve.inputs[1])

    compare_003 = compare_op(group, "GREATER_THAN", "FLOAT", geometry_proximity_001.outputs[1], 0.0)
    compare_003.node.inputs[10].default_value = 0.8999999761581421
    compare_003.node.inputs[11].default_value = 0.08726649731397629
    compare_003.node.inputs[12].default_value = 0.0010000000474974513

    scale_elements = nodes.new("GeometryNodeScaleElements")
    scale_elements.domain = "FACE"
    scale_elements.inputs[2].default_value = 0.0
    scale_elements.inputs[3].default_value = Vector((0.0, 0.0, 0.0))
    scale_elements.inputs[4].default_value = "Uniform"
    scale_elements.inputs[5].default_value = [1.0, 0.0, 0.0]
    links.new(extrude_mesh_003.outputs[0], scale_elements.inputs[0])
    links.new(extrude_mesh_003.outputs[1], scale_elements.inputs[1])

    set_shade_smooth_001 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_001.domain = "FACE"
    set_shade_smooth_001.inputs[1].default_value = True
    set_shade_smooth_001.inputs[2].default_value = True
    links.new(join_geometry_006.outputs[0], set_shade_smooth_001.inputs[0])

    set_shade_smooth_003 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_003.domain = "FACE"
    set_shade_smooth_003.inputs[1].default_value = True
    set_shade_smooth_003.inputs[2].default_value = True
    links.new(join_geometry_008.outputs[0], set_shade_smooth_003.inputs[0])

    fill_curve = nodes.new("GeometryNodeFillCurve")
    fill_curve.inputs[1].default_value = 0
    fill_curve.inputs[2].default_value = "N-gons"
    links.new(fillet_curve.outputs[0], fill_curve.inputs[0])

    merge_by_distance_003 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_003.inputs[2].default_value = "All"
    merge_by_distance_003.inputs[3].default_value = 0.0010000000474974513
    links.new(scale_elements.outputs[0], merge_by_distance_003.inputs[0])
    links.new(extrude_mesh_003.outputs[1], merge_by_distance_003.inputs[1])

    set_shade_smooth_002 = nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth_002.domain = "EDGE"
    set_shade_smooth_002.inputs[2].default_value = False
    links.new(set_shade_smooth_001.outputs[0], set_shade_smooth_002.inputs[0])
    links.new(compare_004, set_shade_smooth_002.inputs[1])

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

    separate_geometry = nodes.new("GeometryNodeSeparateGeometry")
    separate_geometry.domain = "EDGE"
    links.new(merge_by_distance_003.outputs[0], separate_geometry.inputs[0])
    links.new(compare_003, separate_geometry.inputs[1])

    subdivide_mesh = nodes.new("GeometryNodeSubdivideMesh")
    subdivide_mesh.inputs[1].default_value = 3
    links.new(merge_by_distance_003.outputs[0], subdivide_mesh.inputs[0])

    join_geometry_009 = nodes.new("GeometryNodeJoinGeometry")
    links.new(set_shade_smooth_002.outputs[0], join_geometry_009.inputs[0])
    links.new(set_shade_smooth_003.outputs[0], join_geometry_009.inputs[0])

    join_geometry_004 = nodes.new("GeometryNodeJoinGeometry")
    links.new(extrude_mesh_002.outputs[0], join_geometry_004.inputs[0])
    links.new(flip_faces_002.outputs[0], join_geometry_004.inputs[0])

    join_geometry_007 = nodes.new("GeometryNodeJoinGeometry")
    links.new(separate_geometry.outputs[0], join_geometry_007.inputs[0])
    links.new(fill_curve.outputs[0], join_geometry_007.inputs[0])

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

    merge_by_distance_002 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.inputs[1].default_value = True
    merge_by_distance_002.inputs[2].default_value = "All"
    merge_by_distance_002.inputs[3].default_value = 0.0010000000474974513
    links.new(join_geometry_004.outputs[0], merge_by_distance_002.inputs[0])

    join_geometry_005 = nodes.new("GeometryNodeJoinGeometry")
    links.new(extrude_mesh_004.outputs[0], join_geometry_005.inputs[0])
    links.new(flip_faces_003.outputs[0], join_geometry_005.inputs[0])

    merge_by_distance_004 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_004.inputs[1].default_value = True
    merge_by_distance_004.inputs[2].default_value = "All"
    merge_by_distance_004.inputs[3].default_value = 0.0010000000474974513
    links.new(join_geometry_005.outputs[0], merge_by_distance_004.inputs[0])

    mesh_boolean = nodes.new("GeometryNodeMeshBoolean")
    mesh_boolean.operation = "INTERSECT"
    mesh_boolean.solver = "MANIFOLD"
    mesh_boolean.inputs[2].default_value = False
    mesh_boolean.inputs[3].default_value = False
    links.new(merge_by_distance_002.outputs[0], mesh_boolean.inputs[1])
    links.new(merge_by_distance_004.outputs[0], mesh_boolean.inputs[1])

    delete_geometry_002 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.mode = "ALL"
    delete_geometry_002.domain = "POINT"
    links.new(mesh_boolean.outputs[0], delete_geometry_002.inputs[0])
    links.new(extrude_mesh_004.outputs[1], delete_geometry_002.inputs[1])

    links.new(fillet_curve.outputs[0], piping.inputs[0])
    links.new(piping.outputs[1], store_named_attribute_004.inputs[0])
    links.new(delete_geometry_002.outputs[0], quilting.inputs[0])
    links.new(join_geometry_007.outputs[0], quilting.inputs[1])
    links.new(quilting.outputs[0], transform_geometry_003.inputs[0])
    links.new(quilting.outputs[0], flip_faces_004.inputs[0])
    links.new(separate_geometry.outputs[0], stitching.inputs[0])
    links.new(fill_curve.outputs[0], stitching.inputs[1])
    links.new(piping.outputs[0], stitching.inputs[2])
    links.new(stitching.outputs[0], join_geometry_008.inputs[0])
    links.new(join_geometry_009.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group