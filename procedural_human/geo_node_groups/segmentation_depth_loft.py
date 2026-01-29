import math

import bpy
from mathutils import Vector

from procedural_human.utils.node_layout import auto_layout_nodes
from procedural_human.decorators.geo_node_decorator import geo_node_group


@geo_node_group
def create_segmentation_depth_loft_group():
    group_name = "Segmentation Depth Loft"
    if group_name in bpy.data.node_groups:
        return bpy.data.node_groups[group_name]

    group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    # --- Interface ---
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    
    socket = group.interface.new_socket(name="Resolution", in_out="INPUT", socket_type="NodeSocketInt")
    socket.default_value = 1000
    socket.min_value = 2
    socket.max_value = 1000
    
    socket = group.interface.new_socket(name="SegmentationMask", in_out="INPUT", socket_type="NodeSocketImage")
    socket.default_value = None
    
    socket = group.interface.new_socket(name="DepthMask", in_out="INPUT", socket_type="NodeSocketImage")
    socket.default_value = None
    
    socket = group.interface.new_socket(name="OutlineMergeDistance", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.004
    socket.min_value = 0.0
    
    socket = group.interface.new_socket(name="MergeDistance", in_out="INPUT", socket_type="NodeSocketFloat")
    socket.default_value = 0.001
    socket.min_value = 0.0

    # --- Nodes ---
    nodes = group.nodes
    links = group.links
    
    group_input = nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    group_output = nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # --- Mask sampling ---
    image_texture = nodes.new("GeometryNodeImageTexture")
    image_texture.name = "Image Texture"
    image_texture.interpolation = "Linear"
    image_texture.extension = "REPEAT"
    image_texture.inputs[2].default_value = 0
    links.new(group_input.outputs[2], image_texture.inputs[0])  # SegmentationMask

    position = nodes.new("GeometryNodeInputPosition")
    position.name = "Position"

    vector_math = nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = "ADD"
    vector_math.inputs[1].default_value = [0.5, 0.5, 0.0]
    links.new(position.outputs[0], vector_math.inputs[0])
    links.new(vector_math.outputs[0], image_texture.inputs[1])

    separate_color = nodes.new("FunctionNodeSeparateColor")
    separate_color.name = "Separate Color"
    separate_color.mode = "RGB"
    links.new(image_texture.outputs[0], separate_color.inputs[0])

    # --- Grid creation ---
    grid = nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    grid.inputs[0].default_value = 1.0  # Size X
    grid.inputs[1].default_value = 1.0  # Size Y

    reroute = nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.socket_idname = "NodeSocketInt"
    links.new(group_input.outputs[1], reroute.inputs[0])  # Resolution
    links.new(reroute.outputs[0], grid.inputs[2])
    links.new(reroute.outputs[0], grid.inputs[3])

    # --- Delete points outside mask ---
    math_less_than = nodes.new("ShaderNodeMath")
    math_less_than.name = "Math"
    math_less_than.operation = "LESS_THAN"
    math_less_than.inputs[1].default_value = 0.1
    links.new(separate_color.outputs[3], math_less_than.inputs[0])  # Alpha

    delete_geometry = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.mode = "ALL"
    delete_geometry.domain = "POINT"
    links.new(grid.outputs[0], delete_geometry.inputs[0])
    links.new(math_less_than.outputs[0], delete_geometry.inputs[1])

    # --- Delete interior edges ---
    edge_neighbors = nodes.new("GeometryNodeInputMeshEdgeNeighbors")
    edge_neighbors.name = "Edge Neighbors"

    compare = nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.operation = "NOT_EQUAL"
    compare.data_type = "INT"
    compare.mode = "ELEMENT"
    compare.inputs[3].default_value = 1  # B (int)
    links.new(edge_neighbors.outputs[0], compare.inputs[2])

    delete_geometry_001 = nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.mode = "ALL"
    delete_geometry_001.domain = "EDGE"
    links.new(delete_geometry.outputs[0], delete_geometry_001.inputs[0])
    links.new(compare.outputs[0], delete_geometry_001.inputs[1])

    # --- Mesh to curve and fill ---
    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    mesh_to_curve.name = "Mesh to Curve"
    mesh_to_curve.mode = "EDGES"
    mesh_to_curve.inputs[1].default_value = True
    links.new(delete_geometry_001.outputs[0], mesh_to_curve.inputs[0])

    fill_curve = nodes.new("GeometryNodeFillCurve")
    fill_curve.name = "Fill Curve"
    fill_curve.inputs[1].default_value = 0  # Group ID
    fill_curve.inputs[2].default_value = "Triangles"
    links.new(mesh_to_curve.outputs[0], fill_curve.inputs[0])

    # --- Merge by distance (outline) ---
    merge_by_distance_001 = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_001.name = "Merge by Distance.001"
    merge_by_distance_001.inputs[1].default_value = True
    merge_by_distance_001.inputs[2].default_value = "All"
    links.new(fill_curve.outputs[0], merge_by_distance_001.inputs[0])
    links.new(group_input.outputs[4], merge_by_distance_001.inputs[3])  # OutlineMergeDistance

    # --- Depth sampling ---
    image_texture_001 = nodes.new("GeometryNodeImageTexture")
    image_texture_001.name = "Image Texture.001"
    image_texture_001.interpolation = "Linear"
    image_texture_001.extension = "REPEAT"
    image_texture_001.inputs[2].default_value = 0
    links.new(group_input.outputs[3], image_texture_001.inputs[0])  # DepthMask

    position_001 = nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"

    vector_math_001 = nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = "ADD"
    vector_math_001.inputs[1].default_value = [0.5, 0.5, 0.0]
    links.new(position_001.outputs[0], vector_math_001.inputs[0])
    links.new(vector_math_001.outputs[0], image_texture_001.inputs[1])

    separate_color_001 = nodes.new("FunctionNodeSeparateColor")
    separate_color_001.name = "Separate Color.001"
    separate_color_001.mode = "RGB"
    links.new(image_texture_001.outputs[0], separate_color_001.inputs[0])

    # --- Average RGB for depth ---
    math_002 = nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = "ADD"
    links.new(separate_color_001.outputs[0], math_002.inputs[0])
    links.new(separate_color_001.outputs[1], math_002.inputs[1])

    math_003 = nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = "ADD"
    links.new(separate_color_001.outputs[2], math_003.inputs[0])
    links.new(math_002.outputs[0], math_003.inputs[1])

    math_004 = nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = "DIVIDE"
    math_004.inputs[1].default_value = 3.0
    links.new(math_003.outputs[0], math_004.inputs[0])

    # --- Depth multiplier ---
    math_001 = nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = "MULTIPLY"
    math_001.inputs[1].default_value = 0.5
    links.new(math_004.outputs[0], math_001.inputs[0])

    combine_x_y_z = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z.name = "Combine XYZ"
    combine_x_y_z.inputs[0].default_value = 0.0
    combine_x_y_z.inputs[1].default_value = 0.0
    links.new(math_001.outputs[0], combine_x_y_z.inputs[2])

    # --- Set position (front mesh) ---
    set_position = nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    set_position.inputs[1].default_value = True
    set_position.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(merge_by_distance_001.outputs[0], set_position.inputs[0])
    links.new(combine_x_y_z.outputs[0], set_position.inputs[3])

    # --- Duplicate front for attribute statistic ---
    duplicate_elements = nodes.new("GeometryNodeDuplicateElements")
    duplicate_elements.name = "Duplicate Elements"
    duplicate_elements.domain = "FACE"
    duplicate_elements.inputs[1].default_value = True
    duplicate_elements.inputs[2].default_value = 1
    links.new(set_position.outputs[0], duplicate_elements.inputs[0])

    # --- Find max Z ---
    position_stat = nodes.new("GeometryNodeInputPosition")
    position_stat.name = "Position.Stat"
    position_stat.label = "Position for Stats"

    separate_x_y_z_stat = nodes.new("ShaderNodeSeparateXYZ")
    separate_x_y_z_stat.name = "Separate XYZ Stat"
    separate_x_y_z_stat.label = "Get Z for Max"
    links.new(position_stat.outputs[0], separate_x_y_z_stat.inputs[0])

    attribute_statistic = nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.label = "Find Max Z"
    attribute_statistic.data_type = "FLOAT"
    attribute_statistic.domain = "POINT"
    attribute_statistic.inputs[1].default_value = True
    links.new(duplicate_elements.outputs[0], attribute_statistic.inputs[0])
    links.new(separate_x_y_z_stat.outputs[2], attribute_statistic.inputs[2])

    # --- Extrude mesh (0 distance for back half) ---
    vector_zero = nodes.new("FunctionNodeInputVector")
    vector_zero.name = "Vector"
    vector_zero.vector = Vector((0.0, 0.0, 0.0))

    extrude_mesh = nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.name = "Extrude Mesh"
    extrude_mesh.mode = "FACES"
    extrude_mesh.inputs[1].default_value = True
    extrude_mesh.inputs[3].default_value = 1.0  # Offset Scale
    extrude_mesh.inputs[4].default_value = False  # Individual
    links.new(set_position.outputs[0], extrude_mesh.inputs[0])
    links.new(vector_zero.outputs[0], extrude_mesh.inputs[2])

    # --- Scale elements (invert Z on extruded faces) ---
    scale_elements = nodes.new("GeometryNodeScaleElements")
    scale_elements.name = "Scale Elements"
    scale_elements.domain = "FACE"
    scale_elements.inputs[2].default_value = -1.0  # Scale
    scale_elements.inputs[4].default_value = "Single Axis"
    scale_elements.inputs[5].default_value = [0.0, 0.0, 1.0]  # Axis
    links.new(extrude_mesh.outputs[0], scale_elements.inputs[0])
    links.new(extrude_mesh.outputs[1], scale_elements.inputs[1])  # Top selection
    links.new(vector_zero.outputs[0], scale_elements.inputs[3])  # Center

    # --- Offset back half by 2*maxZ ---
    vector_math_002 = nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = "SCALE"
    vector_math_002.inputs[3].default_value = 2.0
    links.new(attribute_statistic.outputs[4], vector_math_002.inputs[0])  # Max Z

    combine_x_y_z_002 = nodes.new("ShaderNodeCombineXYZ")
    combine_x_y_z_002.name = "Combine XYZ.002"
    combine_x_y_z_002.inputs[0].default_value = 0.0
    combine_x_y_z_002.inputs[1].default_value = 0.0
    links.new(vector_math_002.outputs[0], combine_x_y_z_002.inputs[2])

    # --- Set position for back half offset ---
    set_position_001 = nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    set_position_001.inputs[2].default_value = [0.0, 0.0, 0.0]
    links.new(scale_elements.outputs[0], set_position_001.inputs[0])
    links.new(extrude_mesh.outputs[1], set_position_001.inputs[1])  # Top selection
    links.new(combine_x_y_z_002.outputs[0], set_position_001.inputs[3])

    # --- Join front and back ---
    join_geometry = nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"
    links.new(duplicate_elements.outputs[0], join_geometry.inputs[0])
    links.new(set_position_001.outputs[0], join_geometry.inputs[0])

    # --- Final merge by distance ---
    merge_by_distance = nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.inputs[1].default_value = True
    merge_by_distance.inputs[2].default_value = "All"
    links.new(join_geometry.outputs[0], merge_by_distance.inputs[0])
    links.new(group_input.outputs[5], merge_by_distance.inputs[3])  # MergeDistance

    # --- Geometry to Instance ---
    geometry_to_instance = nodes.new("GeometryNodeGeometryToInstance")
    geometry_to_instance.name = "Geometry to Instance"
    links.new(merge_by_distance.outputs[0], geometry_to_instance.inputs[0])

    # --- Rotate Instances (X 90 degrees, local space, pivot 0,0,0) ---
    rotate_instances = nodes.new("GeometryNodeRotateInstances")
    rotate_instances.name = "Rotate Instances"
    rotate_instances.inputs[1].default_value = True  # Selection
    rotate_instances.inputs[2].default_value = [math.radians(90), 0.0, 0.0]  # Rotation (X=90 deg)
    rotate_instances.inputs[3].default_value = [0.0, 0.0, 0.0]  # Pivot Point
    rotate_instances.inputs[4].default_value = True  # Local Space
    links.new(geometry_to_instance.outputs[0], rotate_instances.inputs[0])

    # --- Image aspect ratio scaling ---
    image_info = nodes.new("GeometryNodeImageInfo")
    image_info.name = "Image Info"
    image_info.inputs[1].default_value = 0  # Frame
    links.new(group_input.outputs[2], image_info.inputs[0])  # SegmentationMask

    math_aspect_ratio = nodes.new("ShaderNodeMath")
    math_aspect_ratio.name = "Math.005"
    math_aspect_ratio.operation = "DIVIDE"
    links.new(image_info.outputs[0], math_aspect_ratio.inputs[0])  # Width
    links.new(image_info.outputs[1], math_aspect_ratio.inputs[1])  # Height

    scale_elements_aspect = nodes.new("GeometryNodeScaleElements")
    scale_elements_aspect.name = "Scale Elements.001"
    scale_elements_aspect.domain = "FACE"
    scale_elements_aspect.inputs[1].default_value = True  # Selection
    scale_elements_aspect.inputs[3].default_value = [0.0, 0.0, 0.0]  # Center
    scale_elements_aspect.inputs[4].default_value = "Single Axis"
    scale_elements_aspect.inputs[5].default_value = [1.0, 0.0, 0.0]  # Axis (X)
    links.new(rotate_instances.outputs[0], scale_elements_aspect.inputs[0])
    links.new(math_aspect_ratio.outputs[0], scale_elements_aspect.inputs[2])  # Scale
    links.new(scale_elements_aspect.outputs[0], group_output.inputs[0])

    auto_layout_nodes(group)
    return group
