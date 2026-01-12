"""
Novel View Generation operators for the segmentation workflow.

Generates 3D meshes from segmentation masks using Hunyuan3D,
then extracts side-view silhouettes for dual-contour mesh creation.
"""

import threading

import bpy
import numpy as np
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, BoolProperty

from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import logger


# Global storage for contour data
_front_contour = None  # Original mask contour (front view)
_side_contour = None   # Novel view contour (side view from 90 degrees)
_side_convex_hull = None  # Convex hull of side view


def get_front_contour():
    """Get the stored front view contour."""
    return _front_contour


def get_side_contour():
    """Get the stored side view contour."""
    return _side_contour


def get_side_convex_hull():
    """Get the convex hull of the side view contour."""
    return _side_convex_hull


def set_contours(front, side, side_hull=None):
    """Store contours for later use in mesh curve creation."""
    global _front_contour, _side_contour, _side_convex_hull
    _front_contour = front
    _side_contour = side
    _side_convex_hull = side_hull


def clear_contours():
    """Clear stored contours."""
    global _front_contour, _side_contour, _side_convex_hull
    _front_contour = None
    _side_contour = None
    _side_convex_hull = None


def compute_convex_hull(contour: np.ndarray) -> np.ndarray:
    """
    Compute the convex hull of a 2D contour.
    
    Args:
        contour: Nx2 array of 2D points
        
    Returns:
        Mx2 array of convex hull vertices in order
    """
    try:
        from scipy.spatial import ConvexHull
        
        if len(contour) < 3:
            return contour
        
        hull = ConvexHull(contour)
        hull_points = contour[hull.vertices]
        return hull_points
        
    except ImportError:
        logger.warning("scipy not available, using simple bounding box")
        # Fallback: return bounding box corners
        min_x, min_y = contour.min(axis=0)
        max_x, max_y = contour.max(axis=0)
        return np.array([
            [min_x, min_y],
            [max_x, min_y],
            [max_x, max_y],
            [min_x, max_y],
        ])


def extract_silhouette_contour(image) -> np.ndarray:
    """
    Extract the contour from a silhouette image.
    
    Args:
        image: PIL Image (grayscale silhouette, white on black)
        
    Returns:
        Nx2 array of contour points
    """
    from procedural_human.segmentation.mask_to_curve import find_contours, simplify_contour
    
    # Convert PIL image to numpy mask
    img_array = np.array(image)
    
    # Threshold to binary
    if len(img_array.shape) == 3:
        # RGB/RGBA - convert to grayscale
        mask = img_array.mean(axis=2) > 128
    else:
        mask = img_array > 128
    
    mask = mask.astype(np.uint8)
    
    # Find contours
    contours = find_contours(mask)
    
    if not contours:
        return np.array([])
    
    # Return the largest contour
    largest = max(contours, key=len)
    
    # Simplify
    simplified = simplify_contour(largest, epsilon=0.005)
    
    return simplified


@procedural_operator
class GenerateNovelViewOperator(Operator):
    """Generate a 3D mesh from segmentation mask and extract side view silhouette"""
    
    bl_idname = "segmentation.generate_novel_view"
    bl_label = "Generate Novel View"
    bl_description = "Generate 3D mesh from mask using Hunyuan3D and extract 90-degree side view"
    bl_options = {'REGISTER', 'UNDO'}
    
    num_steps: IntProperty(
        name="Inference Steps",
        description="Number of diffusion steps (fewer = faster, turbo model uses 5)",
        default=5,
        min=1,
        max=50
    )
    
    guidance_scale: FloatProperty(
        name="Guidance Scale",
        description="Classifier-free guidance scale",
        default=5.5,
        min=1.0,
        max=15.0
    )
    
    rotation_angle: FloatProperty(
        name="Side View Angle",
        description="Rotation angle for side view (degrees)",
        default=90.0,
        min=0.0,
        max=360.0
    )
    
    use_convex_hull: BoolProperty(
        name="Use Convex Hull",
        description="Compute convex hull of side silhouette for cleaner contour",
        default=True
    )
    
    keep_3d_mesh: BoolProperty(
        name="Keep 3D Mesh",
        description="Keep the generated 3D mesh in the scene",
        default=False
    )
    
    def execute(self, context):
        # Get current masks
        from procedural_human.segmentation.operators.segmentation_operators import (
            get_current_masks,
            get_active_image,
            blender_image_to_pil,
        )
        
        masks = get_current_masks()
        if not masks:
            self.report({'WARNING'}, "No segmentation masks available. Run segmentation first.")
            return {'CANCELLED'}
        
        # Get the active image
        image = get_active_image(context)
        if image is None:
            self.report({'WARNING'}, "No image loaded in Image Editor")
            return {'CANCELLED'}
        
        try:
            # Convert to PIL
            pil_image = blender_image_to_pil(image)
            
            # Apply mask to create masked image (white background)
            from PIL import Image as PILImage
            import numpy as np
            
            img_array = np.array(pil_image)
            
            # Combine all masks
            combined_mask = np.zeros(masks[0].shape, dtype=bool)
            for mask in masks:
                combined_mask |= mask
            
            # Flip mask to match image coordinates
            combined_mask = np.flipud(combined_mask)
            
            # Resize mask if needed
            if combined_mask.shape != (img_array.shape[0], img_array.shape[1]):
                mask_pil = PILImage.fromarray(combined_mask.astype(np.uint8) * 255)
                mask_pil = mask_pil.resize((img_array.shape[1], img_array.shape[0]), PILImage.NEAREST)
                combined_mask = np.array(mask_pil) > 127
            
            # Apply mask: keep masked pixels, white background
            masked_img = np.ones_like(img_array) * 255
            for c in range(3):
                masked_img[:, :, c] = np.where(combined_mask, img_array[:, :, c], 255)
            
            masked_pil = PILImage.fromarray(masked_img.astype(np.uint8))
            
            # Extract front contour from mask
            from procedural_human.segmentation.mask_to_curve import find_contours, simplify_contour
            
            front_contours = find_contours(combined_mask.astype(np.uint8))
            if front_contours:
                front_contour = simplify_contour(max(front_contours, key=len), epsilon=0.005)
            else:
                self.report({'WARNING'}, "Could not extract front contour from mask")
                return {'CANCELLED'}
            
            self.report({'INFO'}, "Sending masked image to Hunyuan3D API...")
            
            # Check if server is running
            from procedural_human.novel_view_gen.server_manager import is_server_running
            
            if not is_server_running():
                self.report({'WARNING'}, "Hunyuan3D server is not running. "
                           "Set HUNYUAN3D_PATH environment variable and restart Blender.")
                return {'CANCELLED'}
            
            # Generate 3D mesh
            from procedural_human.novel_view_gen.api_client import generate_and_import
            
            mesh_obj = generate_and_import(
                masked_pil,
                num_steps=self.num_steps,
                guidance_scale=self.guidance_scale,
            )
            
            if mesh_obj is None:
                self.report({'ERROR'}, "Failed to generate 3D mesh from image")
                return {'CANCELLED'}
            
            self.report({'INFO'}, f"Generated 3D mesh: {mesh_obj.name}")
            
            # Render from side angle
            from procedural_human.novel_view_gen.api_client import render_mesh_silhouette
            
            silhouette = render_mesh_silhouette(
                mesh_obj,
                rotation_degrees=self.rotation_angle,
                resolution=(512, 512),
            )
            
            if silhouette is None:
                self.report({'WARNING'}, "Failed to render side silhouette")
                if not self.keep_3d_mesh:
                    bpy.data.objects.remove(mesh_obj, do_unlink=True)
                return {'CANCELLED'}
            
            # Extract side contour
            side_contour = extract_silhouette_contour(silhouette)
            
            if len(side_contour) < 3:
                self.report({'WARNING'}, "Side silhouette contour too small")
                if not self.keep_3d_mesh:
                    bpy.data.objects.remove(mesh_obj, do_unlink=True)
                return {'CANCELLED'}
            
            # Compute convex hull if requested
            if self.use_convex_hull:
                side_hull = compute_convex_hull(side_contour)
            else:
                side_hull = None
            
            # Store contours
            set_contours(front_contour, side_contour, side_hull)
            
            # Store in scene for UI feedback
            context.scene["novel_view_front_points"] = len(front_contour)
            context.scene["novel_view_side_points"] = len(side_contour)
            if side_hull is not None:
                context.scene["novel_view_hull_points"] = len(side_hull)
            
            # Clean up 3D mesh if not keeping
            if not self.keep_3d_mesh:
                bpy.data.objects.remove(mesh_obj, do_unlink=True)
            
            self.report({'INFO'}, f"Extracted contours: front={len(front_contour)} points, "
                        f"side={len(side_contour)} points")
            
            return {'FINISHED'}
            
        except Exception as e:
            logger.error(f"Novel view generation failed: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Generation failed: {e}")
            return {'CANCELLED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "num_steps")
        layout.prop(self, "guidance_scale")
        layout.prop(self, "rotation_angle")
        layout.prop(self, "use_convex_hull")
        layout.prop(self, "keep_3d_mesh")


@procedural_operator
class ClearNovelViewContoursOperator(Operator):
    """Clear stored novel view contours"""
    
    bl_idname = "segmentation.clear_novel_contours"
    bl_label = "Clear Novel View Contours"
    bl_description = "Clear stored front and side view contours"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        clear_contours()
        
        # Clear scene properties
        if "novel_view_front_points" in context.scene:
            del context.scene["novel_view_front_points"]
        if "novel_view_side_points" in context.scene:
            del context.scene["novel_view_side_points"]
        if "novel_view_hull_points" in context.scene:
            del context.scene["novel_view_hull_points"]
        
        self.report({'INFO'}, "Novel view contours cleared")
        return {'FINISHED'}


# Global state for async server check
_server_check_result: dict = {"done": False, "running": False, "url": ""}


def _check_server_thread():
    """Background thread to check server status."""
    global _server_check_result
    from procedural_human.novel_view_gen.server_manager import (
        refresh_server_status,
        get_server_host,
        get_server_port,
    )
    
    try:
        is_running = refresh_server_status()
        url = f"http://{get_server_host()}:{get_server_port()}"
        _server_check_result = {"done": True, "running": is_running, "url": url}
    except Exception as e:
        _server_check_result = {"done": True, "running": False, "url": "", "error": str(e)}


@procedural_operator
class CheckHunyuanServerOperator(Operator):
    """Check if Hunyuan3D server is running (non-blocking)"""
    
    bl_idname = "segmentation.check_hunyuan_server"
    bl_label = "Check Hunyuan3D Server"
    bl_description = "Check if the Hunyuan3D API server is running and responding"
    bl_options = {'REGISTER'}
    
    _timer = None
    
    def modal(self, context, event):
        global _server_check_result
        
        if event.type == 'TIMER':
            if _server_check_result.get("done", False):
                # Check complete, report result
                self.cancel(context)
                
                if _server_check_result.get("running", False):
                    url = _server_check_result.get("url", "")
                    self.report({'INFO'}, f"Hunyuan3D server is running at {url}")
                else:
                    self.report({'WARNING'}, "Hunyuan3D server is not running. "
                               "Set HUNYUAN3D_PATH and restart Blender.")
                
                # Force panel redraw
                for area in context.screen.areas:
                    area.tag_redraw()
                
                return {'FINISHED'}
        
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        global _server_check_result
        
        # Reset state and start background thread
        _server_check_result = {"done": False, "running": False, "url": ""}
        
        thread = threading.Thread(target=_check_server_thread, daemon=True)
        thread.start()
        
        # Start timer to poll for completion
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}
    
    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
