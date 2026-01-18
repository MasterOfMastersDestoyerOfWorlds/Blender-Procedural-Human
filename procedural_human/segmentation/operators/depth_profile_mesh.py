import bpy
from bpy.types import Operator
from bpy.props import IntProperty, BoolProperty, FloatProperty
import numpy as np
from mathutils import Vector, Euler, Matrix
from procedural_human.logger import logger
from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.segmentation.operators.mesh_curve_operators import (
    create_dual_loop_mesh, 
    apply_bezier_handles, 
    apply_charrot_gregory_patch_modifier,
    create_spine_contour_from_depth
)

@procedural_operator
class CreateDepthProfileMeshOperator(Operator):
    """Create a mesh from segmentation mask and depth map, aligned to camera"""
    
    bl_idname = "segmentation.create_depth_profile_mesh"
    bl_label = "Create Depth Profile Mesh"
    bl_description = "Create mesh from mask and depth map, aligned to main camera with Charrot-Gregory patch"
    bl_options = {'REGISTER', 'UNDO'}
    
    points_per_half: IntProperty(
        name="Points per Half",
        description="Number of vertices per half-loop (excluding shared vertices)",
        default=16,
        min=4,
        max=64
    )
    
    subdivisions: IntProperty(
        name="Patch Subdivisions",
        description="Subdivisions for Charrot-Gregory patch surface",
        default=4,
        min=1,
        max=8
    )
    
    merge_by_distance: BoolProperty(
        name="Merge By Distance",
        description="Merge vertices at patch boundaries for smooth surface",
        default=True
    )
    
    depth_scale: FloatProperty(
        name="Depth Scale",
        description="Scale factor for depth-based thickness",
        default=1.0,
        min=0.1,
        max=5.0
    )
    
    def execute(self, context):
        from procedural_human.segmentation.operators.segmentation_operators import (
            get_current_masks, get_active_image, get_current_depth_map
        )
        from procedural_human.segmentation.mask_to_curve import find_contours
        
        # Get camera
        camera = context.scene.camera
        if camera is None:
            self.report({'WARNING'}, "No camera found in scene. Please set a camera as active.")
            return {'CANCELLED'}
        
        # Get mask
        masks = get_current_masks()
        if not masks:
            self.report({'WARNING'}, "No segmentation masks available. Run segmentation first.")
            return {'CANCELLED'}
        
        # Use first enabled mask or first mask
        settings = context.scene.segmentation_mask_settings
        mask_index = 0
        if len(settings.masks) > 0:
            enabled_indices = [item.mask_index for item in settings.masks if item.enabled and item.mask_index >= 0]
            if enabled_indices:
                mask_index = enabled_indices[0]
        
        if mask_index >= len(masks):
            mask_index = 0
        
        mask = masks[mask_index]
        
        # Get depth map
        depth_map = get_current_depth_map()
        if depth_map is None:
            self.report({'WARNING'}, "No depth map available. Run depth estimation first.")
            return {'CANCELLED'}
        
        # Get image dimensions
        image = get_active_image(context)
        if image:
            image_width, image_height = image.size
        else:
            image_height, image_width = mask.shape[:2]
        
        try:
            # Create front contour from mask
            contours = find_contours(mask)
            if not contours:
                self.report({'WARNING'}, "Could not extract contour from mask")
                return {'CANCELLED'}
            
            # Use largest contour
            front_contour = max(contours, key=len)
            
            # Calculate Visual Center using Distance Transform for better alignment
            # This ensures the "spine" aligns with the thickest part of the object
            try:
                from scipy.ndimage import distance_transform_edt
                dist = distance_transform_edt(mask)
                max_idx = np.argmax(dist)
                max_y, max_x = np.unravel_index(max_idx, dist.shape)
                center_x, center_y = float(max_x), float(max_y)
                # logger.info(f"Using visual center at ({center_x}, {center_y})")
            except ImportError:
                # Fallback to centroid
                M = cv2.moments(mask.astype(np.uint8)) if 'cv2' in locals() else None
                if M and M["m00"] != 0:
                    center_x = M["m10"] / M["m00"]
                    center_y = M["m01"] / M["m00"]
                else:
                    # Bounding box center
                    y_indices, x_indices = np.where(mask)
                    center_x = (np.min(x_indices) + np.max(x_indices)) / 2
                    center_y = (np.min(y_indices) + np.max(y_indices)) / 2
            
            # Normalize front contour to image coordinates centered on visual center
            front_contour_norm = front_contour.astype(np.float32).copy()
            
            # Normalize to 0-1 then center around visual center
            # Image coords: X=0..W, Y=0..H (down)
            # Blender coords: X=-0.5..0.5, Y=-0.5..0.5 (up)
            
            # Shift points so that (center_x, center_y) becomes (0,0)
            front_contour_norm[:, 0] = (front_contour_norm[:, 0] - center_x) / image_width
            
            # Flip Y and center
            # Image Y is down, Blender Y is up.
            # (y - center_y) / height -> if y > center (lower in image), result > 0.
            # We want y > center (lower image) -> y < 0 (lower blender).
            # So -(y - center_y) / height
            front_contour_norm[:, 1] = -(front_contour_norm[:, 1] - center_y) / image_height
            
            # Determine Z-depth and Positioning
            # Calculate mean depth value in the mask to handle layering (0=far, 1=close)
            # Mask depth values
            # Resize depth map to match mask if needed before indexing
            if depth_map.shape != mask.shape:
                from PIL import Image as PILImage
                depth_pil = PILImage.fromarray((depth_map * 255).astype(np.uint8))
                depth_pil = depth_pil.resize((mask.shape[1], mask.shape[0]), PILImage.BILINEAR)
                depth_map_resized = np.array(depth_pil).astype(np.float32) / 255.0
                mask_depths = depth_map_resized[mask]
            else:
                mask_depths = depth_map[mask]
            
            if len(mask_depths) > 0:
                mean_depth_val = np.mean(mask_depths)
            else:
                mean_depth_val = 0.5
                
            # Define depth range for layering
            # Close objects (val ~1) should be closer to camera
            # Far objects (val ~0) should be further
            base_distance = 5.0
            depth_layering_range = 2.0  # Objects spread over 2 meters depth
            
            # Higher depth value = Closer = Smaller distance
            # distance = base - (val - 0.5) * range
            object_distance = base_distance - (mean_depth_val - 0.5) * depth_layering_range
            
            # Unproject visual center to 3D view plane
            # We assume the "center" of our mesh (0,0,0) should align with the ray through (center_x, center_y)
            
            # Camera parameters (approximated if not available)
            # Sensor width in mm, focal length in mm
            sensor_width = camera.data.sensor_width
            focal_length = camera.data.lens
            
            # Normalized coordinates of center (-0.5 to 0.5)
            # Account for aspect ratio if render settings available, otherwise assume square pixels
            render = context.scene.render
            aspect_ratio = render.resolution_x / render.resolution_y
            
            norm_cx = (center_x / image_width) - 0.5
            norm_cy = 0.5 - (center_y / image_height)  # Blender Y is up
            
            # Calculate view plane offsets at object_distance
            # tan(theta/2) = (sensor/2) / focal
            # view_width = 2 * distance * tan(theta/2) = distance * sensor / focal
            view_plane_width = object_distance * sensor_width / focal_length
            view_plane_height = view_plane_width / aspect_ratio
            
            offset_x = norm_cx * view_plane_width
            offset_y = norm_cy * view_plane_height
            
            # Create spine contour from depth map
            # Use the improved function that uses distance transform and local contrast
            spine_contour = create_spine_contour_from_depth(
                mask,
                depth_map,
                image_width,
                image_height,
                num_points=self.points_per_half * 2 + 2
            )
            
            # Apply depth scale
            # Spine X is Z-thickness.
            spine_contour[:, 0] *= self.depth_scale
            
            # Create the mesh
            obj = create_dual_loop_mesh(
                front_contour_norm,
                spine_contour,
                name=f"DepthMesh_{mask_index}",
                points_per_half=self.points_per_half,
            )
            
            # Scale the mesh to match view plane size
            # front_contour_norm is normalized to image dimensions (roughly -0.5 to 0.5)
            # We need to scale it up to physical dimensions at that distance
            obj.scale.x = view_plane_width
            obj.scale.y = view_plane_height  # Assuming normalized Y was also scaled by image height ratio?
            # Wait, front_contour_norm was divided by image_width/height separately.
            # So X units are fractions of width, Y units are fractions of height.
            # So scaling X by view_width and Y by view_height is correct.
            obj.scale.z = view_plane_width # Scale thickness proportionally to width? 
            # Or assume depth_scale handled it. Let's keep Z scale same as X for consistency.
            
            logger.info(f"Created depth profile mesh: {obj.name} at dist {object_distance:.2f}")
            
            # Apply Bezier handles
            try:
                apply_bezier_handles(obj)
            except Exception as e:
                logger.warning(f"Could not apply Bezier handles: {e}")
            
            # Apply Charrot-Gregory patch modifier
            try:
                apply_charrot_gregory_patch_modifier(
                    obj,
                    self.subdivisions,
                    self.merge_by_distance
                )
            except Exception as e:
                logger.warning(f"Could not apply Charrot-Gregory patch: {e}")
            
            # Transform mesh to align with camera
            # Get camera matrix
            camera_matrix = camera.matrix_world
            camera_location = camera_matrix.translation
            camera_rotation = camera_matrix.to_euler()
            
            # Calculate world position
            # Start at camera
            # Move forward (-Z local) by object_distance
            # Move right (+X local) by offset_x
            # Move up (+Y local) by offset_y
            
            # Get camera local axes
            cam_rot_mat = camera_rotation.to_matrix()
            cam_right = cam_rot_mat.col[0] # X
            cam_up = cam_rot_mat.col[1]    # Y
            cam_back = cam_rot_mat.col[2]  # Z
            
            target_location = camera_location - cam_back * object_distance + cam_right * offset_x + cam_up * offset_y
            
            # Set mesh location
            obj.location = target_location
            
            # Rotate to face camera (billboard)
            # Mesh "Front" is +Z? No, our contours are in XY plane.
            # create_dual_loop_mesh creates in XY.
            # We want Mesh XY plane to be parallel to Camera XY plane.
            # So Mesh Rotation = Camera Rotation.
            obj.rotation_euler = camera_rotation
            
            # Select the new object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            self.report({'INFO'}, f"Created depth profile mesh: {obj.name}")
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Failed to create depth profile mesh: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Failed: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "points_per_half")
        layout.prop(self, "depth_scale")
        layout.separator()
        layout.prop(self, "subdivisions")
        layout.prop(self, "merge_by_distance")
