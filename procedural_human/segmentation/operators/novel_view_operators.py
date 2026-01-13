"""
Novel View Generation operators for the segmentation workflow.

Generates 3D meshes from segmentation masks using Hunyuan3D,
then extracts side-view silhouettes for dual-contour mesh creation.
"""

import threading

import bpy
import numpy as np
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, BoolProperty, StringProperty

from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.logger import logger


# ============================================================================
# Collection Management
# ============================================================================

HUNYUAN_COLLECTION_NAME = "Hunyuan_Meshes"
DEBUG_COLLECTION_NAME = "Segmentation_Debug"


def get_or_create_collection(name: str) -> bpy.types.Collection:
    """
    Get or create a collection by name.
    
    Args:
        name: Collection name
        
    Returns:
        The collection
    """
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    
    logger.info(f"[Hunyuan3D] Created collection: {name}")
    return collection


def get_or_create_hunyuan_collection() -> bpy.types.Collection:
    """
    Get or create the Hunyuan_Meshes collection.
    
    Returns:
        The Hunyuan_Meshes collection
    """
    # Check if collection exists
    if HUNYUAN_COLLECTION_NAME in bpy.data.collections:
        return bpy.data.collections[HUNYUAN_COLLECTION_NAME]
    
    # Create new collection
    collection = bpy.data.collections.new(HUNYUAN_COLLECTION_NAME)
    
    # Link to scene collection
    bpy.context.scene.collection.children.link(collection)
    
    logger.info(f"[Hunyuan3D] Created collection: {HUNYUAN_COLLECTION_NAME}")
    return collection


def get_next_mesh_name() -> str:
    """
    Get the next available mesh name in the Hunyuan collection.
    
    Returns:
        Name like "Hunyuan_Mask_001", "Hunyuan_Mask_002", etc.
    """
    collection = get_or_create_hunyuan_collection()
    
    # Find highest existing number
    max_num = 0
    for obj in collection.objects:
        if obj.name.startswith("Hunyuan_Mask_"):
            try:
                num = int(obj.name.split("_")[-1])
                max_num = max(max_num, num)
            except ValueError:
                pass
    
    return f"Hunyuan_Mask_{max_num + 1:03d}"


def link_object_to_hunyuan_collection(obj: bpy.types.Object, name: str = None):
    """
    Link an object to the Hunyuan_Meshes collection.
    
    Args:
        obj: Blender object to link
        name: Optional new name for the object
    """
    collection = get_or_create_hunyuan_collection()
    
    # Rename if specified
    if name:
        obj.name = name
    
    # Unlink from all current collections
    for coll in obj.users_collection:
        coll.objects.unlink(obj)
    
    # Link to Hunyuan collection
    collection.objects.link(obj)


def link_object_to_collection(obj: bpy.types.Object, collection: bpy.types.Collection):
    """
    Link an object to a specific collection.
    
    Args:
        obj: Blender object to link
        collection: Target collection
    """
    # Unlink from all current collections
    for coll in obj.users_collection:
        coll.objects.unlink(obj)
    
    # Link to target collection
    collection.objects.link(obj)


def create_debug_plane(pil_image, name: str, location=None) -> bpy.types.Object:
    """
    Create a plane with the masked image as texture for debugging.
    Places the plane in the 'Segmentation_Debug' collection.
    
    Args:
        pil_image: PIL Image to use as texture
        name: Name for the plane object
        location: Optional location tuple (x, y, z). Default is origin.
        
    Returns:
        The created plane object
    """
    import tempfile
    from pathlib import Path
    
    if location is None:
        location = (0, 0, 0)
    
    # Get or create debug collection
    debug_collection = get_or_create_collection(DEBUG_COLLECTION_NAME)
    
    # Calculate aspect ratio for plane sizing
    width, height = pil_image.size
    aspect = width / height
    
    # Create plane
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    plane = bpy.context.active_object
    plane.name = name
    plane.scale = (aspect, 1, 1)
    
    # Save PIL image to temp file
    temp_dir = Path(tempfile.gettempdir()) / "segmentation_debug"
    temp_dir.mkdir(exist_ok=True)
    temp_path = temp_dir / f"{name}.png"
    pil_image.save(str(temp_path))
    
    # Load image into Blender
    blender_image = bpy.data.images.load(str(temp_path))
    blender_image.name = f"{name}_Texture"
    
    # Create material with image texture
    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Add nodes
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (300, 0)
    
    bsdf_node = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)
    
    tex_node = nodes.new('ShaderNodeTexImage')
    tex_node.location = (-300, 0)
    tex_node.image = blender_image
    
    # Connect nodes
    links.new(tex_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    # Assign material to plane
    plane.data.materials.append(mat)
    
    # Move to debug collection
    link_object_to_collection(plane, debug_collection)
    
    logger.info(f"[Debug] Created debug plane: {name} at {location}")
    
    return plane


# ============================================================================
# Global storage for contour data
# ============================================================================

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


# ============================================================================
# Async Generation State
# ============================================================================

_generation_state = {
    "running": False,
    "cancelled": False,
    "current_mask": 0,
    "total_masks": 0,
    "current_step": "",  # "generating", "importing", "rendering"
    "glb_bytes": None,  # Result from background thread
    "error": None,
    "mask_data": [],  # List of {mask_idx, masked_image, front_contour, debug_image}
    "generated_meshes": [],
    "all_front_contours": [],
    "all_side_contours": [],
    "debug_mask": False,  # Whether to create debug planes
}


def _reset_generation_state():
    """Reset the generation state."""
    global _generation_state
    _generation_state = {
        "running": False,
        "cancelled": False,
        "current_mask": 0,
        "total_masks": 0,
        "current_step": "",
        "glb_bytes": None,
        "error": None,
        "mask_data": [],
        "generated_meshes": [],
        "all_front_contours": [],
        "all_side_contours": [],
        "debug_mask": False,
    }


def _generate_mesh_thread(masked_image, num_steps: int, guidance_scale: float):
    """
    Background thread function to call Hunyuan3D API.
    
    Only makes the HTTP request - does NOT modify Blender data.
    Stores result in _generation_state["glb_bytes"].
    """
    global _generation_state
    
    try:
        from procedural_human.novel_view_gen.api_client import generate_3d_mesh
        
        logger.info("[Hunyuan3D] Starting mesh generation in background thread...")
        
        glb_bytes = generate_3d_mesh(
            masked_image,
            num_steps=num_steps,
            guidance_scale=guidance_scale,
        )
        
        _generation_state["glb_bytes"] = glb_bytes
        
        if glb_bytes is None:
            _generation_state["error"] = "API returned no mesh data"
        else:
            logger.info(f"[Hunyuan3D] Received {len(glb_bytes)} bytes from API")
            
    except Exception as e:
        logger.error(f"[Hunyuan3D] Background generation failed: {e}")
        _generation_state["error"] = str(e)
        _generation_state["glb_bytes"] = None


def get_generation_progress() -> str:
    """Get current generation progress as a string for UI display."""
    if not _generation_state["running"]:
        return ""
    
    current = _generation_state["current_mask"] + 1
    total = _generation_state["total_masks"]
    step = _generation_state["current_step"]
    
    if step == "generating":
        return f"Generating mesh {current}/{total}..."
    elif step == "importing":
        return f"Importing mesh {current}/{total}..."
    elif step == "rendering":
        return f"Rendering silhouette {current}/{total}..."
    else:
        return f"Processing {current}/{total}..."


def is_generation_running() -> bool:
    """Check if generation is currently running."""
    return _generation_state["running"]


@procedural_operator
class GenerateNovelViewOperator(Operator):
    """Generate 3D meshes from selected segmentation masks (async)"""
    
    bl_idname = "segmentation.generate_novel_view"
    bl_label = "Generate Novel View"
    bl_description = "Generate 3D meshes from selected masks using Hunyuan3D (one mesh per mask)"
    bl_options = {'REGISTER'}
    
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
    
    debug_mask: BoolProperty(
        name="Debug Segmentation Mask",
        description="Create a plane with the masked image texture for debugging",
        default=False
    )
    
    _timer = None
    _thread = None
    
    def modal(self, context, event):
        """Poll for generation completion and handle results."""
        global _generation_state
        
        if event.type == 'TIMER':
            # Check for cancellation
            if _generation_state["cancelled"]:
                self.cancel(context)
                self.report({'WARNING'}, "Generation cancelled")
                return {'CANCELLED'}
            
            # Check if thread finished
            if self._thread is not None and not self._thread.is_alive():
                # Thread completed - handle result
                return self._handle_thread_result(context)
            
            # Redraw panels to show progress
            for area in context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    area.tag_redraw()
        
        elif event.type == 'ESC':
            # User pressed escape - cancel
            _generation_state["cancelled"] = True
            self.cancel(context)
            self.report({'WARNING'}, "Generation cancelled by user")
            return {'CANCELLED'}
        
        return {'PASS_THROUGH'}
    
    def _handle_thread_result(self, context):
        """Handle result from background thread."""
        global _generation_state
        
        from procedural_human.novel_view_gen.api_client import save_glb_to_temp, import_glb_to_blender, render_mesh_silhouette
        
        current_idx = _generation_state["current_mask"]
        mask_data = _generation_state["mask_data"]
        mesh_obj = None  # Track if we got a mesh
        
        # Always create debug plane first (even if generation fails)
        if _generation_state["debug_mask"] and current_idx < len(mask_data):
            debug_image = mask_data[current_idx].get("debug_image")
            if debug_image is not None:
                # Position debug plane at a default location (will update if mesh exists)
                debug_loc = (current_idx * 3.0, 0, 0)  # Space out by mask index
                debug_name = f"Debug_Mask_{current_idx + 1:03d}"
                create_debug_plane(debug_image, debug_name, debug_loc)
                logger.info(f"[Hunyuan3D] Created debug plane: {debug_name}")
        
        # Check for error
        if _generation_state["error"]:
            error = _generation_state["error"]
            logger.error(f"[Hunyuan3D] Mask {current_idx} failed: {error}")
            # Continue to next mask
            _generation_state["error"] = None
            _generation_state["glb_bytes"] = None
            return self._process_next_mask(context)
        
        # Check for GLB data
        glb_bytes = _generation_state["glb_bytes"]
        if glb_bytes is None:
            logger.warning("[Hunyuan3D] No GLB data received")
            return self._process_next_mask(context)
        
        # Import mesh (must be done in main thread)
        _generation_state["current_step"] = "importing"
        
        try:
            temp_path = save_glb_to_temp(glb_bytes)
            mesh_obj = import_glb_to_blender(temp_path)
            
            # Clean up temp file
            try:
                temp_path.unlink()
            except:
                pass
            
            if mesh_obj is None:
                logger.error("[Hunyuan3D] Failed to import GLB")
                return self._process_next_mask(context)
            
            # Rename and move to Hunyuan collection
            mesh_name = get_next_mesh_name()
            link_object_to_hunyuan_collection(mesh_obj, mesh_name)
            _generation_state["generated_meshes"].append(mesh_obj)
            
            logger.info(f"[Hunyuan3D] Imported mesh: {mesh_name}")
            
            # Render side silhouette
            _generation_state["current_step"] = "rendering"
            
            silhouette = render_mesh_silhouette(
                mesh_obj,
                rotation_degrees=self.rotation_angle,
                resolution=(512, 512),
            )
            
            if silhouette is not None:
                side_contour = extract_silhouette_contour(silhouette)
                if len(side_contour) >= 3:
                    _generation_state["all_side_contours"].append(side_contour)
            
            # Store front contour
            if current_idx < len(mask_data):
                front_contour = mask_data[current_idx].get("front_contour")
                if front_contour is not None:
                    _generation_state["all_front_contours"].append(front_contour)
                    
        except Exception as e:
            logger.error(f"[Hunyuan3D] Import/render failed: {e}")
        
        # Clear GLB bytes
        _generation_state["glb_bytes"] = None
        
        # Process next mask
        return self._process_next_mask(context)
    
    def _process_next_mask(self, context):
        """Start processing the next mask or finish."""
        global _generation_state
        
        _generation_state["current_mask"] += 1
        
        if _generation_state["current_mask"] >= _generation_state["total_masks"]:
            # All done
            return self._finish_generation(context)
        
        # Start next mask
        return self._start_mask_generation(context)
    
    def _start_mask_generation(self, context):
        """Start generation for the current mask."""
        global _generation_state
        
        current_idx = _generation_state["current_mask"]
        mask_data = _generation_state["mask_data"]
        
        if current_idx >= len(mask_data):
            return self._finish_generation(context)
        
        data = mask_data[current_idx]
        masked_image = data["masked_image"]
        
        _generation_state["current_step"] = "generating"
        _generation_state["glb_bytes"] = None
        _generation_state["error"] = None
        
        # Start background thread
        self._thread = threading.Thread(
            target=_generate_mesh_thread,
            args=(masked_image, self.num_steps, self.guidance_scale),
            daemon=True
        )
        self._thread.start()
        
        return {'PASS_THROUGH'}
    
    def _finish_generation(self, context):
        """Finish generation and store results."""
        global _generation_state
        
        self.cancel(context)
        
        generated_meshes = _generation_state["generated_meshes"]
        all_front_contours = _generation_state["all_front_contours"]
        all_side_contours = _generation_state["all_side_contours"]
        
        if not generated_meshes:
            self.report({'ERROR'}, "Failed to generate any 3D meshes")
            _reset_generation_state()
            return {'CANCELLED'}
        
        # Store contours (use first mask's contours)
        if all_front_contours and all_side_contours:
            front_contour = all_front_contours[0]
            side_contour = all_side_contours[0]
            
            if self.use_convex_hull:
                side_hull = compute_convex_hull(side_contour)
            else:
                side_hull = None
            
            set_contours(front_contour, side_contour, side_hull)
            
            # Store in scene for UI feedback
            context.scene["novel_view_front_points"] = len(front_contour)
            context.scene["novel_view_side_points"] = len(side_contour)
            if side_hull is not None:
                context.scene["novel_view_hull_points"] = len(side_hull)
        
        # Store generated mesh count
        context.scene["hunyuan_mesh_count"] = len(generated_meshes)
        
        self.report({'INFO'}, f"Generated {len(generated_meshes)} meshes in '{HUNYUAN_COLLECTION_NAME}' collection")
        
        _reset_generation_state()
        return {'FINISHED'}
    
    def execute(self, context):
        """Validate and start async generation."""
        global _generation_state
        
        if _generation_state["running"]:
            self.report({'WARNING'}, "Generation already in progress")
            return {'CANCELLED'}
        
        from procedural_human.segmentation.operators.segmentation_operators import (
            get_current_masks,
            get_active_image,
            blender_image_to_pil,
            get_enabled_mask_indices,
        )
        
        masks = get_current_masks()
        if not masks:
            self.report({'WARNING'}, "No segmentation masks available. Run segmentation first.")
            return {'CANCELLED'}
        
        enabled_indices = get_enabled_mask_indices(context)
        if not enabled_indices:
            self.report({'WARNING'}, "No masks selected. Enable at least one mask in the list.")
            return {'CANCELLED'}
        
        image = get_active_image(context)
        if image is None:
            self.report({'WARNING'}, "No image loaded in Image Editor")
            return {'CANCELLED'}
        
        from procedural_human.novel_view_gen.server_manager import is_server_running
        
        if not is_server_running():
            self.report({'WARNING'}, "Hunyuan3D server is not running. "
                       "Set HUNYUAN3D_PATH environment variable and restart Blender.")
            return {'CANCELLED'}
        
        # Prepare mask data (done in main thread before async)
        try:
            from PIL import Image as PILImage
            from procedural_human.segmentation.mask_to_curve import find_contours, simplify_contour
            from procedural_human.novel_view_gen.api_client import crop_to_mask_bounds
            
            pil_image = blender_image_to_pil(image)
            img_array = np.array(pil_image)
            
            mask_data = []
            
            for mask_idx in enabled_indices:
                if mask_idx >= len(masks):
                    continue
                
                mask = masks[mask_idx]
                
                # Flip mask to match image coordinates
                mask_flipped = np.flipud(mask)
                
                # Resize mask if needed
                if mask_flipped.shape != (img_array.shape[0], img_array.shape[1]):
                    mask_pil = PILImage.fromarray(mask_flipped.astype(np.uint8) * 255)
                    mask_pil = mask_pil.resize((img_array.shape[1], img_array.shape[0]), PILImage.NEAREST)
                    mask_flipped = np.array(mask_pil) > 127
                
                # Apply mask: keep masked pixels, white background
                masked_img = np.ones_like(img_array) * 255
                for c in range(3):
                    masked_img[:, :, c] = np.where(mask_flipped, img_array[:, :, c], 255)
                
                masked_pil = PILImage.fromarray(masked_img.astype(np.uint8))
                
                # Store uncropped image for debug plane (if enabled)
                debug_image = masked_pil.copy() if self.debug_mask else None
                
                # Crop to mask bounding box (no padding)
                cropped_pil, bounds = crop_to_mask_bounds(masked_pil, mask_flipped)
                
                # Extract front contour
                front_contours = find_contours(mask_flipped.astype(np.uint8))
                front_contour = None
                if front_contours:
                    front_contour = simplify_contour(max(front_contours, key=len), epsilon=0.005)
                
                mask_data.append({
                    "mask_idx": mask_idx,
                    "masked_image": cropped_pil,  # Use cropped image for generation
                    "debug_image": debug_image,   # Original uncropped for debug plane
                    "front_contour": front_contour,
                    "crop_bounds": bounds,
                })
            
            if not mask_data:
                self.report({'WARNING'}, "Could not prepare any masks for generation")
                return {'CANCELLED'}
            
            # Initialize state
            _reset_generation_state()
            _generation_state["running"] = True
            _generation_state["total_masks"] = len(mask_data)
            _generation_state["mask_data"] = mask_data
            _generation_state["debug_mask"] = self.debug_mask
            
            # Start timer
            wm = context.window_manager
            self._timer = wm.event_timer_add(0.1, window=context.window)
            wm.modal_handler_add(self)
            
            self.report({'INFO'}, f"Starting generation of {len(mask_data)} meshes...")
            
            # Start first mask
            self._start_mask_generation(context)
            
            return {'RUNNING_MODAL'}
            
        except Exception as e:
            logger.error(f"Failed to prepare masks: {e}")
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, f"Preparation failed: {e}")
            return {'CANCELLED'}
    
    def cancel(self, context):
        """Clean up timer."""
        global _generation_state
        _generation_state["running"] = False
        
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        
        # Show how many masks are selected
        from procedural_human.segmentation.operators.segmentation_operators import get_enabled_mask_indices
        enabled_indices = get_enabled_mask_indices(context)
        layout.label(text=f"Will generate {len(enabled_indices)} mesh(es)")
        
        layout.separator()
        layout.prop(self, "num_steps")
        layout.prop(self, "guidance_scale")
        layout.prop(self, "rotation_angle")
        layout.prop(self, "use_convex_hull")
        
        layout.separator()
        layout.prop(self, "debug_mask")


@procedural_operator
class CancelNovelViewGenerationOperator(Operator):
    """Cancel ongoing novel view generation"""
    
    bl_idname = "segmentation.cancel_novel_view"
    bl_label = "Cancel Generation"
    bl_description = "Cancel the ongoing mesh generation"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        global _generation_state
        if _generation_state["running"]:
            _generation_state["cancelled"] = True
            self.report({'INFO'}, "Cancellation requested...")
        else:
            self.report({'INFO'}, "No generation in progress")
        return {'FINISHED'}


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
