"""
Utility functions for Procedural Human Generator
"""

import bpy
from mathutils import Vector
from . import advanced_nodes


def create_geometry_nodes_modifier(obj, name):
    """Add Geometry Nodes modifier to object"""
    modifier = obj.modifiers.new(name, "NODES")
    node_group = bpy.data.node_groups.new(name, "GeometryNodeTree")
    modifier.node_group = node_group
    return modifier, node_group


def setup_basic_nodes(node_group):
    """Setup basic input/output nodes"""
    # Add geometry socket to node group interface
    if "Geometry" not in [socket.name for socket in node_group.interface.items_tree]:
        node_group.interface.new_socket(
            name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
        )
        node_group.interface.new_socket(
            name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
        )

    # Create input/output nodes
    input_node = node_group.nodes.new("NodeGroupInput")
    output_node = node_group.nodes.new("NodeGroupOutput")

    # Position nodes
    input_node.location = (-600, 0)
    output_node.location = (600, 0)

    return input_node, output_node


def create_spine_curve():
    """Create the spine curve scaffold"""
    # Define spine points with natural S-curve
    spine_points = [
        (0, 0, 0),  # Pelvis
        (0, 0.1, 0.3),  # Lower back
        (0, 0.2, 0.6),  # Mid back
        (0, 0.1, 0.9),  # Upper back
        (0, 0, 1.2),  # Neck base
    ]

    # Create curve data
    curve_data = bpy.data.curves.new("Spine", "CURVE")
    curve_data.dimensions = "3D"
    curve_data.fill_mode = "FULL"

    polyline = curve_data.splines.new("POLY")
    polyline.points.add(len(spine_points) - 1)

    for i, point in enumerate(spine_points):
        polyline.points[i].co = (*point, 1)

    spine = bpy.data.objects.new("Spine", curve_data)
    bpy.context.collection.objects.link(spine)
    return spine


def create_torso_geometry(height=1.7, build=0.5):
    """Create the main torso object with Geometry Nodes"""
    # Create base cylinder for torso, scaled by height
    torso_height = height * 0.7  # Torso is about 70% of total height
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.4 + (build * 0.2),  # Radius affected by build
        depth=torso_height,
        location=(0, 0, torso_height / 2),
    )
    torso = bpy.context.object
    torso.name = "Torso"

    # Add Geometry Nodes modifier
    modifier, node_group = create_geometry_nodes_modifier(torso, "TorsoShape")

    # Add custom properties for parameters
    node_group["height"] = height
    node_group["build"] = build

    # Use advanced node setup
    try:
        advanced_nodes.create_advanced_torso_nodes(node_group)
    except Exception:
        # Fallback to basic setup
        input_node, output_node = setup_basic_nodes(node_group)

        # Add torso shaping nodes
        set_position = node_group.nodes.new("GeometryNodeSetPosition")
        set_position.location = (0, 0)

        # Add map range for torso silhouette
        map_range_torso = node_group.nodes.new("ShaderNodeMapRange")
        map_range_torso.location = (-200, 200)
        map_range_torso.inputs["From Min"].default_value = 0.0
        map_range_torso.inputs["From Max"].default_value = 1.0
        map_range_torso.inputs["To Min"].default_value = 0.8 + (build * 0.4)
        map_range_torso.inputs["To Max"].default_value = 1.2 + (build * 0.6)

        # Add spline parameter for height-based shaping
        spline_param = node_group.nodes.new("GeometryNodeSplineParameter")
        spline_param.location = (-400, 200)

        # Connect nodes
        node_group.links.new(
            input_node.outputs["Geometry"], set_position.inputs["Geometry"]
        )
        node_group.links.new(
            spline_param.outputs["Factor"], map_range_torso.inputs["Value"]
        )
        node_group.links.new(
            map_range_torso.outputs["Result"], set_position.inputs["Offset"]
        )
        node_group.links.new(
            set_position.outputs["Geometry"], output_node.inputs["Geometry"]
        )

    return torso


def create_limb_geometry(
    name, start_pos, end_pos, joint_pos=None, radius=0.1, length_scale=1.0, build=0.5
):
    """Create limb geometry with Geometry Nodes"""
    # Scale positions by length factor
    scaled_start = (start_pos[0], start_pos[1], start_pos[2] * length_scale)
    scaled_end = (end_pos[0], end_pos[1], end_pos[2] * length_scale)

    # Create base cylinder
    length = (Vector(scaled_end) - Vector(scaled_start)).length
    final_radius = radius + (build * 0.05)  # Build affects limb thickness
    bpy.ops.mesh.primitive_cylinder_add(
        radius=final_radius,
        depth=length,
        location=(
            (scaled_start[0] + scaled_end[0]) / 2,
            (scaled_start[1] + scaled_end[1]) / 2,
            (scaled_start[2] + scaled_end[2]) / 2,
        ),
    )
    limb = bpy.context.object
    limb.name = name

    # Add Geometry Nodes modifier
    modifier, node_group = create_geometry_nodes_modifier(limb, f"{name}Shape")

    # Use advanced node setup
    try:
        limb_type = "arm" if "arm" in name.lower() else "leg"
        advanced_nodes.create_advanced_limb_nodes(node_group, limb_type)
    except Exception:
        # Fallback to basic setup
        input_node, output_node = setup_basic_nodes(node_group)

        # Add muscle shaping
        set_position = node_group.nodes.new("GeometryNodeSetPosition")
        set_position.location = (0, 0)

        # Add noise for muscle variation
        noise_texture = node_group.nodes.new("ShaderNodeTexNoise")
        noise_texture.location = (-200, 100)
        noise_texture.inputs["Scale"].default_value = 5.0

        # Connect nodes
        node_group.links.new(
            input_node.outputs["Geometry"], set_position.inputs["Geometry"]
        )
        node_group.links.new(
            noise_texture.outputs["Fac"], set_position.inputs["Offset"]
        )
        node_group.links.new(
            set_position.outputs["Geometry"], output_node.inputs["Geometry"]
        )

    return limb


def create_head_geometry(head_scale=1.0, height=1.7):
    """Create the head with Geometry Nodes"""
    # Create base sphere - position based on total height
    head_radius = 0.3 * head_scale
    head_z = height * 0.85  # Head at 85% of total height
    bpy.ops.mesh.primitive_uv_sphere_add(radius=head_radius, location=(0, 0, head_z))
    head = bpy.context.object
    head.name = "Head"

    # Add Geometry Nodes modifier
    modifier, node_group = create_geometry_nodes_modifier(head, "HeadShape")

    # Use advanced node setup
    try:
        advanced_nodes.create_advanced_head_nodes(node_group)
    except Exception:
        # Fallback to basic setup
        input_node, output_node = setup_basic_nodes(node_group)

        # Add displacement using SetPosition
        set_position = node_group.nodes.new("GeometryNodeSetPosition")
        set_position.location = (0, 0)

        # Add vector math for displacement scale
        vector_math = node_group.nodes.new("ShaderNodeVectorMath")
        vector_math.location = (-100, 100)
        vector_math.operation = "MULTIPLY"
        vector_math.inputs[1].default_value = (0.02, 0.02, 0.02)  # Scale factor

        # Add noise for facial features
        noise_texture = node_group.nodes.new("ShaderNodeTexNoise")
        noise_texture.location = (-200, 100)
        noise_texture.inputs["Scale"].default_value = 10.0

        # Connect nodes
        node_group.links.new(
            input_node.outputs["Geometry"], set_position.inputs["Geometry"]
        )
        node_group.links.new(noise_texture.outputs["Color"], vector_math.inputs[0])
        node_group.links.new(vector_math.outputs[0], set_position.inputs["Offset"])
        node_group.links.new(
            set_position.outputs["Geometry"], output_node.inputs["Geometry"]
        )

    return head


def create_hand_geometry():
    """Create hand with separate finger objects and bones"""
    # Create palm base - flattened cube
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    hand = bpy.context.object
    hand.name = "Hand_Palm"

    # Scale to hand proportions
    hand.scale = (0.12, 0.06, 0.18)  # Width, depth, length
    bpy.context.view_layer.update()

    # Create armature for hand bones
    bpy.ops.object.armature_add(location=(0, 0, 0))
    armature = bpy.context.object
    armature.name = "Hand_Armature"
    bpy.context.view_layer.update()

    # Enter edit mode to create finger bones
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')

    # Remove default bone
    armature.data.edit_bones.remove(armature.data.edit_bones[0])

    # Define finger data: (name, segments, base_pos, length, radius)
    finger_data = [
        ("Thumb", 3, (-0.05, 0.08, 0.025), 0.06, 0.008),
        ("Index", 3, (-0.03, 0.12, 0.0), 0.08, 0.007),
        ("Middle", 3, (0.0, 0.12, 0.0), 0.09, 0.007),
        ("Ring", 3, (0.03, 0.12, 0.0), 0.08, 0.006),
        ("Pinky", 3, (0.06, 0.10, 0.0), 0.07, 0.005),
    ]

    finger_objects = []

    # Create bones and finger objects for each finger
    for finger_name, segments, base_pos, length, radius in finger_data:
        segment_length = length / segments
        
        # Create finger segments as separate objects
        for segment_idx in range(segments):
            # Calculate position for this segment
            segment_offset = segment_idx * segment_length
            pos_x, pos_y, pos_z = base_pos
            segment_pos = (pos_x, pos_y + segment_offset, pos_z)
            
            # Create bone for this segment
            bone = armature.data.edit_bones.new(f"{finger_name}_Segment_{segment_idx+1}")
            bone.head = segment_pos
            bone.tail = (pos_x, pos_y + segment_offset + segment_length, pos_z)
            
            # Parent bones in chain
            if segment_idx > 0:
                parent_bone_name = f"{finger_name}_Segment_{segment_idx}"
                bone.parent = armature.data.edit_bones[parent_bone_name]

    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Now create finger segment objects
    for finger_name, segments, base_pos, length, radius in finger_data:
        segment_length = length / segments
        
        for segment_idx in range(segments):
            # Calculate position for this segment
            segment_offset = segment_idx * segment_length
            pos_x, pos_y, pos_z = base_pos
            segment_pos = (pos_x, pos_y + segment_offset + segment_length/2, pos_z)
            
            # Create cylinder for finger segment
            bpy.ops.mesh.primitive_cylinder_add(
                radius=radius,
                depth=segment_length,
                location=segment_pos,
                vertices=16
            )
            
            finger_segment = bpy.context.object
            finger_segment.name = f"{finger_name}_Segment_{segment_idx+1}"
            
            # Add slight taper for more natural look
            if segment_idx == segments - 1:  # Last segment (fingertip)
                finger_segment.scale = (0.8, 0.8, 1.0)
            
            # Add slight rotation for natural finger positioning
            if finger_name == "Thumb":
                finger_segment.rotation_euler = (0, 0, 0.5)
            elif finger_name in ["Ring", "Pinky"] and segment_idx > 0:
                curl = segment_idx * 0.1
                finger_segment.rotation_euler = (curl, 0, 0)
            
            # Parent to hand palm
            finger_segment.parent = hand
            finger_objects.append(finger_segment)
            
            # Add bone constraint
            constraint = finger_segment.constraints.new(type='COPY_TRANSFORMS')
            constraint.target = armature
            constraint.subtarget = f"{finger_name}_Segment_{segment_idx+1}"

    # Parent armature to hand
    armature.parent = hand

    # Create collection for hand parts
    hand_collection = bpy.data.collections.new("Hand_Parts")
    bpy.context.scene.collection.children.link(hand_collection)
    
    # Move all hand parts to collection
    hand_collection.objects.link(hand)
    hand_collection.objects.link(armature)
    for finger_obj in finger_objects:
        hand_collection.objects.link(finger_obj)
        # Remove from scene collection to avoid duplicates
        try:
            bpy.context.scene.collection.objects.unlink(finger_obj)
        except Exception:
            pass

    bpy.context.view_layer.update()
    return hand


# End of file
