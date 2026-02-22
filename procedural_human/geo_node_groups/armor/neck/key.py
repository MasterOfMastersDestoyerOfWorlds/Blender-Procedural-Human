import bpy
from procedural_human.decorators.geo_node_decorator import geo_node_group
from mathutils import Euler, Vector
from procedural_human.geo_node_groups.utilities.bi_rail_loft import create_bi_rail_loft_group
from procedural_human.geo_node_groups.utilities.gem_in_holder import create_gem_in__holder_group
from procedural_human.geo_node_groups.utilities.gold_decorations import create_gold__decorations_group
from procedural_human.geo_node_groups.utilities.gold_on_band import create_gold_on__band_group
from procedural_human.geo_node_groups.utilities.is_edge_boundary import create_is__edge__boundary_group
from procedural_human.geo_node_groups.utilities.join_splines import create_join__splines_group
from procedural_human.geo_node_groups.utilities.pipes import create_pipes_group
from procedural_human.geo_node_groups.utilities.rivet import create_rivet_group
from procedural_human.geo_node_groups.utilities.swap_attr import create_swap__attr_group
from procedural_human.geo_node_groups.node_helpers import get_or_rebuild_node_group, vec_math_op
from procedural_human.utils.node_layout import auto_layout_nodes


@geo_node_group
def create_neck_key_group():
    group_name = "Neck_key"
    group, needs_rebuild = get_or_rebuild_node_group(group_name)
    if not needs_rebuild:
        return group

    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    nodes = group.nodes
    links = group.links
    group_output = nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    curve_line = nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.mode = "DIRECTION"
    curve_line.inputs[0].default_value = Vector((0.0, 0.0, -0.009999999776482582))
    curve_line.inputs[1].default_value = Vector((0.0, 0.0, 1.0))
    curve_line.inputs[2].default_value = [0.0, 0.0, -1.0]
    curve_line.inputs[3].default_value = 0.05000000074505806


    curve_to_mesh_003 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_003.inputs[3].default_value = True


    resample_curve_005 = nodes.new("GeometryNodeResampleCurve")
    resample_curve_005.keep_last_segment = True
    resample_curve_005.inputs[1].default_value = True
    resample_curve_005.inputs[2].default_value = "Count"
    resample_curve_005.inputs[3].default_value = 128
    resample_curve_005.inputs[4].default_value = 0.10000000149011612


    curve_circle_008 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_008.mode = "RADIUS"
    curve_circle_008.inputs[0].default_value = 32
    curve_circle_008.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_008.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_008.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_008.inputs[4].default_value = 0.003000000026077032


    spline_parameter_008 = nodes.new("GeometryNodeSplineParameter")


    float_curve_011 = nodes.new("ShaderNodeFloatCurve")
    float_curve_011.inputs[0].default_value = 1.0


    curve_circle_009 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_009.mode = "RADIUS"
    curve_circle_009.inputs[0].default_value = 12
    curve_circle_009.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_009.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_009.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_009.inputs[4].default_value = 0.004000000189989805


    curve_to_mesh_004 = nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh_004.inputs[2].default_value = 0.800000011920929
    curve_to_mesh_004.inputs[3].default_value = True


    curve_circle_010 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_010.mode = "RADIUS"
    curve_circle_010.inputs[0].default_value = 6
    curve_circle_010.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_010.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_010.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_010.inputs[4].default_value = 0.0020000000949949026


    join_geometry_014 = nodes.new("GeometryNodeJoinGeometry")


    curve_circle_011 = nodes.new("GeometryNodeCurvePrimitiveCircle")
    curve_circle_011.mode = "RADIUS"
    curve_circle_011.inputs[0].default_value = 6
    curve_circle_011.inputs[1].default_value = Vector((-1.0, 0.0, 0.0))
    curve_circle_011.inputs[2].default_value = Vector((0.0, 1.0, 0.0))
    curve_circle_011.inputs[3].default_value = Vector((1.0, 0.0, 0.0))
    curve_circle_011.inputs[4].default_value = 0.00800000037997961


    instance_on_points_006 = nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_006.inputs[1].default_value = True
    instance_on_points_006.inputs[3].default_value = False
    instance_on_points_006.inputs[4].default_value = 0
    instance_on_points_006.inputs[5].default_value = Euler((0.0, 0.0, 0.0), 'XYZ')
    instance_on_points_006.inputs[6].default_value = Vector((1.0, 1.0, 1.0))


    transform_geometry_024 = nodes.new("GeometryNodeTransform")
    transform_geometry_024.inputs[1].default_value = "Components"
    transform_geometry_024.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    transform_geometry_024.inputs[3].default_value = Euler((1.5707963705062866, 0.5235987901687622, 0.0), 'XYZ')
    transform_geometry_024.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    grid = nodes.new("GeometryNodeMeshGrid")
    grid.inputs[0].default_value = 0.014999999664723873
    grid.inputs[1].default_value = 0.012000000104308128
    grid.inputs[2].default_value = 12
    grid.inputs[3].default_value = 4


    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "FACE"


    random_value_013 = nodes.new("FunctionNodeRandomValue")
    random_value_013.data_type = "BOOLEAN"
    random_value_013.inputs[0].default_value = [0.0, 0.0, 0.0]
    random_value_013.inputs[1].default_value = [1.0, 1.0, 1.0]
    random_value_013.inputs[2].default_value = 0.0
    random_value_013.inputs[3].default_value = 1.0
    random_value_013.inputs[4].default_value = 0
    random_value_013.inputs[5].default_value = 100
    random_value_013.inputs[6].default_value = 0.2734806537628174
    random_value_013.inputs[7].default_value = 0
    random_value_013.inputs[8].default_value = 78


    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.mode = "FACES"
    extrude_mesh.inputs[1].default_value = True
    extrude_mesh.inputs[2].default_value = Vector((0.0, 0.0, 0.0))
    extrude_mesh.inputs[3].default_value = 0.003000000026077032
    extrude_mesh.inputs[4].default_value = False


    flip_faces = nodes.new("GeometryNodeFlipFaces")
    flip_faces.inputs[1].default_value = True


    join_geometry_015 = nodes.new("GeometryNodeJoinGeometry")


    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.inputs[1].default_value = True
    merge_by_distance.inputs[2].default_value = "All"
    merge_by_distance.inputs[3].default_value = 9.999999747378752e-05


    transform_geometry_025 = nodes.new("GeometryNodeTransform")
    transform_geometry_025.inputs[1].default_value = "Components"
    transform_geometry_025.inputs[2].default_value = Vector((0.006000000052154064, 0.001500000013038516, -0.04999999701976776))
    transform_geometry_025.inputs[3].default_value = Euler((1.5707963705062866, -1.5707963705062866, 0.0), 'XYZ')
    transform_geometry_025.inputs[4].default_value = Vector((1.0, 1.0, 1.0))


    subdivision_surface = nodes.new("GeometryNodeSubdivisionSurface")
    subdivision_surface.inputs[1].default_value = 1
    subdivision_surface.inputs[2].default_value = 0.8063265681266785
    subdivision_surface.inputs[3].default_value = 0.0
    subdivision_surface.inputs[4].default_value = True
    subdivision_surface.inputs[5].default_value = "Keep Boundaries"
    subdivision_surface.inputs[6].default_value = "All"


    frame_023 = nodes.new("NodeFrame")
    frame_023.label = "Key"
    frame_023.text = None
    frame_023.shrink = True
    frame_023.label_size = 20


    # Parent assignments
    curve_circle_008.parent = frame_023
    curve_circle_009.parent = frame_023
    curve_circle_010.parent = frame_023
    curve_circle_011.parent = frame_023
    curve_line.parent = frame_023
    curve_to_mesh_003.parent = frame_023
    curve_to_mesh_004.parent = frame_023
    delete_geometry_001.parent = frame_023
    extrude_mesh.parent = frame_023
    flip_faces.parent = frame_023
    float_curve_011.parent = frame_023
    grid.parent = frame_023
    instance_on_points_006.parent = frame_023
    join_geometry_014.parent = frame_023
    join_geometry_015.parent = frame_023
    merge_by_distance.parent = frame_023
    random_value_013.parent = frame_023
    resample_curve_005.parent = frame_023
    spline_parameter_008.parent = frame_023
    subdivision_surface.parent = frame_023
    transform_geometry_024.parent = frame_023
    transform_geometry_025.parent = frame_023

    # Internal links
    links.new(resample_curve_005.outputs[0], curve_to_mesh_003.inputs[0])
    links.new(curve_line.outputs[0], resample_curve_005.inputs[0])
    links.new(curve_circle_008.outputs[0], curve_to_mesh_003.inputs[1])
    links.new(spline_parameter_008.outputs[0], float_curve_011.inputs[1])
    links.new(float_curve_011.outputs[0], curve_to_mesh_003.inputs[2])
    links.new(curve_circle_009.outputs[0], curve_to_mesh_004.inputs[0])
    links.new(curve_circle_010.outputs[0], curve_to_mesh_004.inputs[1])
    links.new(curve_to_mesh_003.outputs[0], join_geometry_014.inputs[0])
    links.new(curve_to_mesh_004.outputs[0], instance_on_points_006.inputs[2])
    links.new(curve_circle_011.outputs[0], instance_on_points_006.inputs[0])
    links.new(instance_on_points_006.outputs[0], transform_geometry_024.inputs[0])
    links.new(transform_geometry_024.outputs[0], join_geometry_014.inputs[0])
    links.new(grid.outputs[0], delete_geometry_001.inputs[0])
    links.new(random_value_013.outputs[3], delete_geometry_001.inputs[1])
    links.new(delete_geometry_001.outputs[0], extrude_mesh.inputs[0])
    links.new(delete_geometry_001.outputs[0], flip_faces.inputs[0])
    links.new(extrude_mesh.outputs[0], join_geometry_015.inputs[0])
    links.new(flip_faces.outputs[0], join_geometry_015.inputs[0])
    links.new(join_geometry_015.outputs[0], merge_by_distance.inputs[0])
    links.new(transform_geometry_025.outputs[0], join_geometry_014.inputs[0])
    links.new(subdivision_surface.outputs[0], transform_geometry_025.inputs[0])
    links.new(merge_by_distance.outputs[0], subdivision_surface.inputs[0])

    links.new(curve_line.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
