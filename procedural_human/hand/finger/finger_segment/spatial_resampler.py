import bpy
from procedural_human.hand.finger.finger_segment.finger_segment_properties import (
    FingerSegmentProperties,
)
from procedural_human.hand.finger.finger_segment.finger_segment_curve_utils import (
    get_default_profile_curve_from_data,
)
from procedural_human.hand.finger.finger_segment.finger_segment_profiles import (
    ProfileType,
)


def create_spatial_profile_offset_node_group(
    axis_name,
    parent_input_node,
    parent_node_group,
    length_clamp_node,
    angle_param_node,
    segment_length,
    segment_type,
):
    """
    Creates a node group that samples a profile curve SPATIALLY (by projecting X coordinates)
    using a 'Flattened Lookup' strategy.
    
    FIX 2: Uses INDEX-based socket access (e.g. inputs[1]) for Capture/Sample nodes.
    This prevents KeyErrors when Blender dynamic socket names change (e.g. "Value" vs "Vector").
    """

    group_name = f"{axis_name} Profile Lookup"
    
    if group_name in bpy.data.node_groups:
        profile_group = bpy.data.node_groups[group_name]
        profile_group.nodes.clear()
        profile_group.interface.clear()
    else:
        profile_group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")

    
    profile_group.interface.new_socket(name="Length Clamp", in_out="INPUT", socket_type="NodeSocketFloat")
    profile_group.interface.new_socket(name="Sin Theta", in_out="INPUT", socket_type="NodeSocketFloat")
    profile_group.interface.new_socket(name=FingerSegmentProperties.SEGMENT_RADIUS.value, in_out="INPUT", socket_type="NodeSocketFloat")
    profile_group.interface.new_socket(name="Y Profile", in_out="INPUT", socket_type="NodeSocketGeometry")
    
    profile_group.interface.new_socket(name="Offset", in_out="OUTPUT", socket_type="NodeSocketFloat")
    profile_group.interface.new_socket(name="Point Count", in_out="OUTPUT", socket_type="NodeSocketInt")
    profile_group.interface.new_socket(name="Y Profile", in_out="OUTPUT", socket_type="NodeSocketGeometry")

    
    nodes = profile_group.nodes
    links = profile_group.links
    
    input_node = nodes.new("NodeGroupInput")
    input_node.location = (-1800, 0)

    
    scene = bpy.context.scene
    p_type = ProfileType.Y_PROFILE if axis_name == "Y" else ProfileType.X_PROFILE
    
    y_profile_obj = get_default_profile_curve_from_data(
        scene, segment_type, p_type, segment_length, 1.0
    )

    y_profile_info = nodes.new("GeometryNodeObjectInfo")
    y_profile_info.label = "Profile (Relative)"
    y_profile_info.location = (-1600, -200)
    y_profile_info.inputs["Object"].default_value = y_profile_obj
    y_profile_info.transform_space = 'RELATIVE' 

    
    resample = nodes.new("GeometryNodeResampleCurve")
    resample.location = (-1400, -200)
    resample.mode = 'COUNT'
    resample.inputs['Count'].default_value = 256
    links.new(y_profile_info.outputs["Geometry"], resample.inputs["Curve"])

    
    bound_box = nodes.new("GeometryNodeBoundBox")
    bound_box.location = (-1400, -500)
    links.new(y_profile_info.outputs["Geometry"], bound_box.inputs["Geometry"])

    sep_min = nodes.new("ShaderNodeSeparateXYZ")
    sep_min.location = (-1200, -500)
    links.new(bound_box.outputs["Min"], sep_min.inputs["Vector"])

    sep_max = nodes.new("ShaderNodeSeparateXYZ")
    sep_max.location = (-1200, -650)
    links.new(bound_box.outputs["Max"], sep_max.inputs["Vector"])

    sub_width = nodes.new("ShaderNodeMath")
    sub_width.operation = "SUBTRACT"
    sub_width.location = (-1000, -550)
    links.new(sep_max.outputs["X"], sub_width.inputs[0])
    links.new(sep_min.outputs["X"], sub_width.inputs[1])

    mul_pos = nodes.new("ShaderNodeMath")
    mul_pos.operation = "MULTIPLY"
    mul_pos.location = (-800, -450)
    links.new(sub_width.outputs["Value"], mul_pos.inputs[0])
    links.new(input_node.outputs["Length Clamp"], mul_pos.inputs[1])

    add_pos = nodes.new("ShaderNodeMath")
    add_pos.operation = "ADD"
    add_pos.label = "Target X"
    add_pos.location = (-600, -450)
    links.new(sep_min.outputs["X"], add_pos.inputs[0])
    links.new(mul_pos.outputs["Value"], add_pos.inputs[1])

    
    
    
    capture_pos = nodes.new("GeometryNodeCaptureAttribute")
    capture_pos.label = "Store Orig Pos"
    capture_pos.location = (-1200, -50)
    capture_pos.domain = 'POINT'
    
    links.new(resample.outputs["Curve"], capture_pos.inputs[0])
    
    pos_input = nodes.new("GeometryNodeInputPosition")
    pos_input.location = (-1400, 0)
    
    
    links.new(pos_input.outputs["Position"], capture_pos.inputs[1])

    
    set_pos = nodes.new("GeometryNodeSetPosition")
    set_pos.label = "Flatten to X"
    set_pos.location = (-1000, -50)
    
    links.new(capture_pos.outputs[0], set_pos.inputs["Geometry"])
    
    separate_orig = nodes.new("ShaderNodeSeparateXYZ")
    separate_orig.location = (-1200, 100)
    links.new(pos_input.outputs["Position"], separate_orig.inputs["Vector"])
    
    combine_flat = nodes.new("ShaderNodeCombineXYZ")
    combine_flat.location = (-1200, 250)
    links.new(separate_orig.outputs["X"], combine_flat.inputs["X"])
    
    links.new(combine_flat.outputs["Vector"], set_pos.inputs["Position"])

    
    
    
    target_vec = nodes.new("ShaderNodeCombineXYZ")
    target_vec.label = "Search Point"
    target_vec.location = (-400, -300)
    links.new(add_pos.outputs["Value"], target_vec.inputs["X"])
    
    
    sample_nearest = nodes.new("GeometryNodeSampleNearest")
    sample_nearest.label = "Find Closest X"
    sample_nearest.location = (-200, -200)
    links.new(set_pos.outputs["Geometry"], sample_nearest.inputs["Geometry"])
    links.new(target_vec.outputs["Vector"], sample_nearest.inputs["Sample Position"])
    
    
    sample_index = nodes.new("GeometryNodeSampleIndex")
    sample_index.label = "Retrieve Radius"
    sample_index.location = (0, -200)
    
    
    links.new(set_pos.outputs["Geometry"], sample_index.inputs[0])
    
    links.new(sample_nearest.outputs["Index"], sample_index.inputs[1])
    
    
    
    links.new(capture_pos.outputs[1], sample_index.inputs[2])

    
    sep_result = nodes.new("ShaderNodeSeparateXYZ")
    sep_result.location = (200, -200)
    
    links.new(sample_index.outputs[0], sep_result.inputs["Vector"])
    
    radius_val = sep_result.outputs["Z"] 

    y_radius_abs = nodes.new("ShaderNodeMath")
    y_radius_abs.operation = "ABSOLUTE"
    y_radius_abs.location = (400, -200)
    links.new(radius_val, y_radius_abs.inputs[0])

    y_radius_scale = nodes.new("ShaderNodeMath")
    y_radius_scale.operation = "MULTIPLY"
    y_radius_scale.location = (600, -200)
    links.new(y_radius_abs.outputs["Value"], y_radius_scale.inputs[0])
    links.new(input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value], y_radius_scale.inputs[1])

    y_offset = nodes.new("ShaderNodeMath")
    y_offset.operation = "MULTIPLY"
    y_offset.location = (800, -200)
    links.new(y_radius_scale.outputs["Value"], y_offset.inputs[0])
    links.new(input_node.outputs["Sin Theta"], y_offset.inputs[1])

    
    domain_size = nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.component = "CURVE"
    domain_size.location = (0, 0)
    links.new(y_profile_info.outputs["Geometry"], domain_size.inputs["Geometry"])

    output_node = nodes.new("NodeGroupOutput")
    output_node.location = (1000, 0)
    
    links.new(y_offset.outputs["Value"], output_node.inputs["Offset"])
    links.new(domain_size.outputs["Point Count"], output_node.inputs["Point Count"])
    links.new(y_profile_info.outputs["Geometry"], output_node.inputs["Y Profile"])

    
    profile_instance = parent_node_group.nodes.new("GeometryNodeGroup")
    profile_instance.node_tree = profile_group
    profile_instance.label = f"{axis_name} Profile Lookup"
    profile_instance.location = (0, 0)
    
    parent_node_group.links.new(
        length_clamp_node.outputs["Result"],
        profile_instance.inputs["Length Clamp"],
    )
    parent_node_group.links.new(
        parent_input_node.outputs[FingerSegmentProperties.SEGMENT_RADIUS.value],
        profile_instance.inputs[
            FingerSegmentProperties.SEGMENT_RADIUS.value
        ],
    )
    parent_node_group.links.new(
        angle_param_node.outputs["Value"],
        profile_instance.inputs["Sin Theta"],
    )
    
    return profile_instance