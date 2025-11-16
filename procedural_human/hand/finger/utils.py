"""
Finger utility functions for Procedural Human Generator
"""

import bpy
from mathutils import Vector
from ... import utils as base_utils
from . import nodes as finger_nodes
from . import proportions


def _get_numeric_value(value, default):
    """Extract numeric value from Blender property or return as-is if already numeric"""
    try:
        if hasattr(value, '_default'):
            return value._default
        elif hasattr(value, 'default'):
            return value.default
        elif str(type(value)) == "<class 'bpy.props._PropertyDeferred'>":
            return default
        else:
            return float(value)
    except Exception:
        return default


def realize_finger_geometry(finger_object):
    """
    Apply Geometry Nodes modifier to finger object to get final mesh
    
    Args:
        finger_object: Finger object with Geometry Nodes modifier
    
    Returns:
        finger_object with modifier applied
    """
    # Find Geometry Nodes modifier
    modifier = None
    for mod in finger_object.modifiers:
        if mod.type == 'NODES':
            modifier = mod
            break
    
    if not modifier:
        raise RuntimeError("No Geometry Nodes modifier found on finger object")
    
    # Update view layer to evaluate modifier
    bpy.context.view_layer.objects.active = finger_object
    bpy.context.view_layer.update()
    
    # Force evaluation of the modifier
    depsgraph = bpy.context.evaluated_depsgraph_get()
    finger_eval = finger_object.evaluated_get(depsgraph)
    
    # Check if we have valid geometry
    if not finger_eval.data or len(finger_eval.data.vertices) == 0:
        raise RuntimeError("Geometry Nodes modifier did not produce any geometry")
    
    # Apply modifier by copying evaluated data
    finger_object.data = finger_eval.data.copy()
    
    # Remove the modifier since we've copied the evaluated data
    finger_object.modifiers.remove(modifier)
    
    bpy.context.view_layer.update()
    return finger_object


def add_finger_armature_to_object(finger_object, finger_type="INDEX", curl_direction="Y", create_animation=True):
    """
    Add armature, bones, weights, IK, and animation to an existing finger object
    
    Args:
        finger_object: Finger mesh object (should have Geometry Nodes modifier applied)
        finger_type: One of "THUMB", "INDEX", "MIDDLE", "RING", "LITTLE"
        curl_direction: Curl direction axis ("X", "Y", or "Z")
        create_animation: Whether to create keyframe animation
    
    Returns:
        armature object
    """
    # Get finger proportions
    finger_data = proportions.get_finger_proportions(finger_type)
    num_segments = finger_data["segments"]
    total_length = 1.0  # Finger should already be scaled to 1 unit
    segment_lengths = proportions.get_segment_lengths_blender_units(finger_type, total_length)
    
    # Create armature
    armature = create_finger_armature(finger_object, num_segments, segment_lengths, curl_direction)
    
    # Create animation if requested
    if create_animation:
        from . import animation
        animation.create_finger_curl_animation(armature, num_segments)
    
    return armature


def create_finger_geometry(
    finger_type="INDEX",
    radius=0.007,
    nail_size=0.003,
    taper_factor=0.15,
    curl_direction="Y",
    total_length=1.0,
):
    """
    Create a standalone finger with variable segments and fingernail using Geometry Nodes
    
    Args:
        finger_type: One of "THUMB", "INDEX", "MIDDLE", "RING", "LITTLE"
        radius: Base finger radius
        nail_size: Fingernail size
        taper_factor: How much radius decreases per segment
        curl_direction: Curl direction axis ("X", "Y", or "Z")
        total_length: Total finger length in blender units (default 1.0)
        create_armature: Whether to create armature and bones
        create_animation: Whether to create keyframe animation
    """
    # Extract numeric values from Blender properties
    radius = _get_numeric_value(radius, 0.007)
    nail_size = _get_numeric_value(nail_size, 0.003)
    taper_factor = _get_numeric_value(taper_factor, 0.15)
    total_length = _get_numeric_value(total_length, 1.0)
    
    # Get finger proportions
    finger_data = proportions.get_finger_proportions(finger_type)
    num_segments = finger_data["segments"]
    segment_lengths = proportions.get_segment_lengths_blender_units(finger_type, total_length)
    
    # Create a single vertex mesh as the base (grows from a point)
    # Geometry Nodes will generate the actual finger geometry procedurally
    mesh = bpy.data.meshes.new("FingerMesh")
    mesh.from_pydata([(0, 0, 0)], [], [])
    finger = bpy.data.objects.new("Finger", mesh)
    bpy.context.collection.objects.link(finger)
    
    # Add Geometry Nodes modifier
    modifier, node_group = base_utils.create_geometry_nodes_modifier(finger, "FingerShape")
    
    # Use advanced node setup
    try:
        finger_nodes.create_finger_nodes(
            node_group,
            num_segments=num_segments,
            segment_lengths=segment_lengths,
            radius=radius,
            nail_size=nail_size,
            taper_factor=taper_factor,
            curl_direction=curl_direction,
        )
        
        # Verify node group structure
        print(f"Node group created with {len(node_group.nodes)} nodes")
        print(f"Node group links: {len(node_group.links)}")
        
        # Check if output node exists and has Geometry input
        output_nodes = [n for n in node_group.nodes if n.type == 'GROUP_OUTPUT']
        if output_nodes:
            output_node = output_nodes[0]
            if "Geometry" not in output_node.inputs:
                print(f"Warning: Output node inputs: {[inp.name for inp in output_node.inputs]}")
        else:
            print("Warning: No GROUP_OUTPUT node found in node group")
            
    except Exception as e:
        print(f"Error creating finger nodes: {e}")
        import traceback
        traceback.print_exc()
        raise RuntimeError(f"Failed to create finger Geometry Nodes: {e}")
    
    # Update view layer to evaluate modifier
    bpy.context.view_layer.objects.active = finger
    bpy.context.view_layer.update()
    
    # Force evaluation of the modifier
    depsgraph = bpy.context.evaluated_depsgraph_get()
    finger_eval = finger.evaluated_get(depsgraph)
    
    # Check if we have valid geometry
    if not finger_eval.data:
        # Try to force update and check again
        bpy.context.view_layer.update()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        finger_eval = finger.evaluated_get(depsgraph)
        
        if not finger_eval.data:
            # Debug: Check modifier status
            print(f"Modifier: {modifier.name}, Type: {modifier.type}")
            print(f"Node group: {node_group.name}")
            print(f"Node group nodes: {len(node_group.nodes)}")
            raise RuntimeError("Geometry Nodes modifier did not produce any geometry. Check node setup.")
    
    # Check vertex count
    if len(finger_eval.data.vertices) == 0:
        raise RuntimeError("Geometry Nodes modifier produced empty geometry (0 vertices). Check node connections.")
    
    # Don't apply modifier or create armature here - those are separate operations
    # Just return the finger with the Geometry Nodes modifier
    
    # Scale to ensure exactly 1 blender unit
    # Calculate current bounding box from evaluated geometry
    bbox = [finger_eval.matrix_world @ Vector(corner) for corner in finger_eval.bound_box]
    
    # Find length along Z axis (or appropriate axis based on curl direction)
    if curl_direction == "Y":
        axis_idx = 2  # Z
    elif curl_direction == "X":
        axis_idx = 2  # Z
    else:  # Z
        axis_idx = 1  # Y
    
    current_length = max(bbox, key=lambda v: v[axis_idx])[axis_idx] - min(bbox, key=lambda v: v[axis_idx])[axis_idx]
    if current_length > 0:
        scale_factor = 1.0 / current_length
        finger.scale = (scale_factor, scale_factor, scale_factor)
    
    bpy.context.view_layer.update()
    
    return finger


def create_finger_armature(finger, num_segments, segment_lengths, curl_direction="Y"):
    """
    Create armature with bones for finger segments
    
    Args:
        finger: Finger mesh object
        num_segments: Number of segments
        segment_lengths: List of segment lengths
        curl_direction: Curl direction axis
    """
    # Create armature
    armature_data = bpy.data.armatures.new("Finger_Armature")
    armature = bpy.data.objects.new("Finger_Armature", armature_data)
    bpy.context.collection.objects.link(armature)
    
    # Parent armature to finger
    armature.parent = finger
    armature.location = finger.location
    
    # Enter edit mode to create bones
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Determine bone orientation based on curl direction
    if curl_direction == "Y":
        bone_direction = Vector((0, 0, 1))  # Point along Z
        bone_roll_axis = Vector((0, 1, 0))  # Roll around Y
    elif curl_direction == "X":
        bone_direction = Vector((0, 0, 1))  # Point along Z
        bone_roll_axis = Vector((1, 0, 0))  # Roll around X
    else:  # Z
        bone_direction = Vector((0, 1, 0))  # Point along Y
        bone_roll_axis = Vector((0, 0, 1))  # Roll around Z
    
    # Create bones for each segment
    bones = []
    cumulative_length = 0.0
    
    for seg_idx in range(num_segments):
        seg_length = segment_lengths[seg_idx]
        bone_name = f"Finger_Segment_{seg_idx + 1}"
        
        # Create bone
        bone = armature_data.edit_bones.new(bone_name)
        bone.head = bone_direction * cumulative_length
        bone.tail = bone_direction * (cumulative_length + seg_length)
        
        # Set bone roll to 0.0 for straight alignment (no curl in rest position)
        bone.roll = 0.0
        
        # Set parent relationship
        if seg_idx > 0:
            bone.parent = armature_data.edit_bones[f"Finger_Segment_{seg_idx}"]
            bone.use_connect = True
        
        bones.append(bone)
        cumulative_length += seg_length
    
    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Verify bones are in rest position (zero rotation)
    # Enter pose mode to check and reset if needed
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    # Reset all bones to rest position (zero rotation)
    for seg_idx in range(num_segments):
        bone_name = f"Finger_Segment_{seg_idx + 1}"
        if bone_name in armature.pose.bones:
            bone = armature.pose.bones[bone_name]
            bone.rotation_euler = (0.0, 0.0, 0.0)
    
    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Add armature modifier to finger
    armature_mod = finger.modifiers.new(name="Armature", type='ARMATURE')
    armature_mod.object = armature
    
    # Paint weights
    paint_finger_weights(finger, num_segments, segment_lengths)
    
    # Setup IK
    setup_finger_ik(armature, num_segments, segment_lengths)
    
    return armature


def paint_finger_weights(finger, num_segments, segment_lengths):
    """
    Paint weights for finger segments with smooth joint falloff
    
    Args:
        finger: Finger mesh object
        num_segments: Number of segments
        segment_lengths: List of segment lengths
    """
    # Ensure we're in object mode
    bpy.context.view_layer.objects.active = finger
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create vertex groups for each bone
    vertex_groups = []
    for seg_idx in range(num_segments):
        vg_name = f"Finger_Segment_{seg_idx + 1}"
        vg = finger.vertex_groups.new(name=vg_name)
        vertex_groups.append(vg)
    
    # Get mesh data
    mesh = finger.data
    cumulative_length = 0.0
    
    # Assign weights to vertices
    for vert_idx, vert in enumerate(mesh.vertices):
        # Get vertex position in local space
        vert_z = vert.co.z
        
        # Find which segment(s) this vertex belongs to
        current_length = 0.0
        weights = [0.0] * num_segments
        
        for seg_idx in range(num_segments):
            seg_length = segment_lengths[seg_idx]
            seg_start = current_length
            seg_end = current_length + seg_length
            seg_center = (seg_start + seg_end) / 2
            
            # Calculate distance from segment center
            dist_from_center = abs(vert_z - seg_center)
            max_dist = seg_length / 2
            
            # Weight falls off smoothly from center
            if dist_from_center <= max_dist:
                # Within segment: full weight
                weight = 1.0 - (dist_from_center / max_dist) * 0.5
            elif seg_idx < num_segments - 1 and vert_z > seg_end:
                # Between segments: blend
                next_seg_start = seg_end
                blend_dist = seg_length * 0.1  # 10% blend zone
                if vert_z < next_seg_start + blend_dist:
                    weight = 1.0 - (vert_z - seg_end) / blend_dist
                else:
                    weight = 0.0
            else:
                weight = 0.0
            
            weights[seg_idx] = max(0.0, min(1.0, weight))
            current_length = seg_end
        
        # Normalize weights to sum to 1.0
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        else:
            # Fallback: assign to nearest segment
            nearest_seg = min(range(num_segments), key=lambda i: abs(vert_z - (sum(segment_lengths[:i]) + segment_lengths[i] / 2)))
            weights[nearest_seg] = 1.0
        
        # Assign weights to vertex groups
        for seg_idx, weight in enumerate(weights):
            if weight > 0.001:  # Only assign if weight is significant
                vertex_groups[seg_idx].add([vert_idx], weight, 'REPLACE')


def setup_finger_ik(armature, num_segments, segment_lengths):
    """
    Setup Inverse Kinematics for finger
    
    Args:
        armature: Armature object
        num_segments: Number of segments
        segment_lengths: List of segment lengths
    """
    # Get tip bone (last segment)
    tip_bone_name = f"Finger_Segment_{num_segments}"
    
    # Create IK target empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, sum(segment_lengths)))
    ik_target = bpy.context.object
    ik_target.name = "Finger_IK_Target"
    ik_target.parent = armature.parent  # Parent to same as armature
    
    # Enter pose mode
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    
    # Get tip bone
    tip_bone = armature.pose.bones[tip_bone_name]
    
    # Add IK constraint
    ik_constraint = tip_bone.constraints.new(type='IK')
    ik_constraint.target = ik_target
    ik_constraint.chain_count = num_segments
    ik_constraint.iterations = 20
    
    # Exit pose mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return ik_target

