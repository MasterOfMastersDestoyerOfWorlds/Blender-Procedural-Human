"""
Hunyuan3D API Client

HTTP client for communicating with the Hunyuan3D API server.
Sends images and receives 3D meshes (GLB format).

Usage:
    from procedural_human.novel_view_gen.api_client import generate_3d_mesh
    glb_bytes = generate_3d_mesh(pil_image)
    with open("output.glb", "wb") as f:
        f.write(glb_bytes)
"""

import base64
import io
import json
import tempfile
from pathlib import Path
from typing import Optional, Union, Tuple
import urllib.request
import urllib.error

from procedural_human.logger import logger
from procedural_human.novel_view_gen.server_manager import (
    get_server_url,
    is_server_running,
    get_server_host,
    get_server_port,
)


def image_to_base64(image) -> str:
    """
    Convert a PIL Image to base64 string.
    
    Args:
        image: PIL Image object
        
    Returns:
        Base64 encoded string of the image (PNG format)
    """
    from PIL import Image
    
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def validate_image_for_generation(image) -> Tuple[bool, str]:
    """
    Validate that an image is suitable for 3D generation.
    
    Args:
        image: PIL Image
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    from PIL import Image as PILImage
    import numpy as np
    width, height = image.size
    if width < 128 or height < 128:
        return False, f"Image too small ({width}x{height}). Minimum 128x128."
    img_array = np.array(image)
    if len(img_array.shape) == 3:
        rgb = img_array[:, :, :3]
        white_pixels = np.all(rgb > 250, axis=2)
        white_ratio = np.mean(white_pixels)
        if white_ratio > 0.95:  # More than 95% white
            return False, f"Image is {white_ratio*100:.0f}% white. Need more subject content."
        mean_value = rgb.mean()
        if mean_value > 252:
            return False, "Image is almost entirely white. Add a subject with non-white pixels."
    if len(img_array.shape) == 3 and img_array.shape[2] == 4:
        alpha_mean = img_array[:, :, 3].mean()
        if alpha_mean < 10:
            return False, "Image is almost entirely transparent."
    variance = np.var(img_array[:, :, :3])
    if variance < 50:
        return False, "Image has very low contrast. Ensure subject is visible."
    
    return True, ""


def crop_to_mask_bounds(image, mask, min_size: int = 256) -> Tuple:
    """
    Crop image to the bounding box of the mask with minimum size enforcement.
    
    Args:
        image: PIL Image
        mask: numpy boolean array (H, W) - True where mask is present
        min_size: Minimum dimension size for the crop (will pad if smaller)
        
    Returns:
        Tuple of (cropped_image, bounds) where bounds is (x_min, y_min, x_max, y_max)
        Returns (original_image, None) if mask is empty or invalid
    """
    import numpy as np
    from PIL import Image as PILImage
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    
    if not np.any(rows) or not np.any(cols):
        logger.warning("[Hunyuan3D] Mask is empty, cannot crop")
        return image, None
    row_indices = np.where(rows)[0]
    col_indices = np.where(cols)[0]
    
    y_min, y_max = int(row_indices[0]), int(row_indices[-1])
    x_min, x_max = int(col_indices[0]), int(col_indices[-1])
    if y_max <= y_min or x_max <= x_min:
        logger.warning("[Hunyuan3D] Invalid mask bounds, cannot crop")
        return image, None
    crop_width = x_max - x_min + 1
    crop_height = y_max - y_min + 1
    
    img_width, img_height = image.size
    if crop_width < min_size:
        expand = (min_size - crop_width) // 2
        x_min = max(0, x_min - expand)
        x_max = min(img_width - 1, x_max + expand)
        while (x_max - x_min + 1) < min_size and (x_min > 0 or x_max < img_width - 1):
            if x_min > 0:
                x_min -= 1
            if x_max < img_width - 1:
                x_max += 1
    
    if crop_height < min_size:
        expand = (min_size - crop_height) // 2
        y_min = max(0, y_min - expand)
        y_max = min(img_height - 1, y_max + expand)
        while (y_max - y_min + 1) < min_size and (y_min > 0 or y_max < img_height - 1):
            if y_min > 0:
                y_min -= 1
            if y_max < img_height - 1:
                y_max += 1
    bounds = (x_min, y_min, x_max + 1, y_max + 1)
    cropped = image.crop(bounds)
    
    logger.info(f"[Hunyuan3D] Cropped image from {image.size} to {cropped.size} (bounds: {bounds})")
    final_width, final_height = cropped.size
    if final_width < min_size or final_height < min_size:
        scale = max(min_size / final_width, min_size / final_height)
        new_size = (int(final_width * scale), int(final_height * scale))
        cropped = cropped.resize(new_size, PILImage.Resampling.LANCZOS)
        logger.info(f"[Hunyuan3D] Scaled up small crop to {cropped.size}")
    
    return cropped, bounds


def generate_3d_mesh(
    image,
    num_steps: int = 5,
    guidance_scale: float = 5.5,
    seed: int = -1,
    octree_depth: int = 8,
    timeout: float = 300.0,
) -> Optional[bytes]:
    """
    Generate a 3D mesh from an image using the Hunyuan3D API.
    
    Args:
        image: PIL Image or path to image file
        num_steps: Number of inference steps (turbo model uses fewer)
        guidance_scale: Guidance scale for generation
        seed: Random seed (-1 for random)
        octree_depth: Octree depth for mesh extraction
        timeout: Request timeout in seconds
        
    Returns:
        GLB file bytes or None if generation failed
    """
    from PIL import Image
    
    if not is_server_running():
        logger.error("[Hunyuan3D] Server is not running")
        return None
    if isinstance(image, (str, Path)):
        image = Image.open(image)
    is_valid, error_msg = validate_image_for_generation(image)
    if not is_valid:
        logger.error(f"[Hunyuan3D] Image validation failed: {error_msg}")
        return None
    logger.info(f"[Hunyuan3D] Image info: size={image.size}, mode={image.mode}")
    image_b64 = image_to_base64(image)
    url = f"http://{get_server_host()}:{get_server_port()}/generate"
    
    payload = {
        "image": image_b64,
        "num_steps": num_steps,
        "guidance_scale": guidance_scale,
        "seed": seed,
        "octree_depth": octree_depth,
    }
    
    data = json.dumps(payload).encode("utf-8")
    
    headers = {
        "Content-Type": "application/json",
    }
    
    logger.info(f"[Hunyuan3D] Sending image to API (size: {image.size}, payload: {len(data)} bytes)")
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                glb_bytes = response.read()
                logger.info(f"[Hunyuan3D] Received GLB mesh ({len(glb_bytes)} bytes)")
                if len(glb_bytes) < 100:
                    logger.error("[Hunyuan3D] Received suspiciously small GLB data - generation may have failed")
                    return None
                
                return glb_bytes
            else:
                logger.error(f"[Hunyuan3D] API returned status {response.status}")
                return None
                
    except urllib.error.HTTPError as e:
        logger.error(f"[Hunyuan3D] HTTP error: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode("utf-8")
            logger.error(f"[Hunyuan3D] Error details: {error_body}")
            if "min()" in error_body and "non-zero size" in error_body:
                logger.error("[Hunyuan3D] Empty mesh error - the model produced no geometry. "
                           "This usually means the input image doesn't contain a clear subject "
                           "or the model configuration is incorrect.")
            elif "NETWORK ERROR" in error_body:
                logger.error("[Hunyuan3D] Server reported network error - this is likely a model/inference issue, not network.")
                
        except:
            pass
        return None
        
    except urllib.error.URLError as e:
        logger.error(f"[Hunyuan3D] URL error: {e.reason}")
        return None
        
    except TimeoutError:
        logger.error(f"[Hunyuan3D] Request timed out after {timeout}s")
        return None
        
    except Exception as e:
        logger.error(f"[Hunyuan3D] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None


def save_glb_to_temp(glb_bytes: bytes) -> Path:
    """
    Save GLB bytes to a temporary file.
    
    Args:
        glb_bytes: GLB file content
        
    Returns:
        Path to the temporary GLB file
    """
    temp_dir = Path(tempfile.gettempdir()) / "hunyuan3d"
    temp_dir.mkdir(exist_ok=True)
    
    temp_file = temp_dir / f"mesh_{id(glb_bytes)}.glb"
    temp_file.write_bytes(glb_bytes)
    
    return temp_file


def import_glb_to_blender(glb_path: Union[str, Path]) -> Optional[object]:
    """
    Import a GLB file into Blender.
    
    Args:
        glb_path: Path to the GLB file
        
    Returns:
        The imported object or None if import failed
    """
    import bpy
    
    glb_path = str(glb_path)
    existing_objects = set(bpy.data.objects)
    
    try:
        bpy.ops.import_scene.gltf(filepath=glb_path)
        new_objects = set(bpy.data.objects) - existing_objects
        
        if new_objects:
            for obj in new_objects:
                if obj.type == 'MESH':
                    return obj
            return list(new_objects)[0]
        else:
            logger.warning("[Hunyuan3D] No objects were imported from GLB")
            return None
            
    except Exception as e:
        logger.error(f"[Hunyuan3D] Failed to import GLB: {e}")
        return None


def generate_and_import(
    image,
    **kwargs
) -> Optional[object]:
    """
    Generate a 3D mesh from an image and import it into Blender.
    
    This is a convenience function that combines generate_3d_mesh,
    save_glb_to_temp, and import_glb_to_blender.
    
    Args:
        image: PIL Image or path to image file
        **kwargs: Additional arguments passed to generate_3d_mesh
        
    Returns:
        The imported Blender object or None if generation/import failed
    """
    glb_bytes = generate_3d_mesh(image, **kwargs)
    
    if glb_bytes is None:
        return None
    temp_path = save_glb_to_temp(glb_bytes)
    obj = import_glb_to_blender(temp_path)
    try:
        temp_path.unlink()
    except:
        pass
    
    return obj


def render_mesh_silhouette(
    mesh_obj,
    rotation_degrees: float = 90.0,
    resolution: Tuple[int, int] = (512, 512),
) -> Optional["Image"]:
    """
    Render a mesh from a rotated angle and extract the silhouette.
    
    Args:
        mesh_obj: Blender mesh object
        rotation_degrees: Rotation around Z axis in degrees (90 = side view)
        resolution: Output image resolution (width, height)
        
    Returns:
        PIL Image with the silhouette (white on black) or None if rendering failed
    """
    import bpy
    import numpy as np
    from PIL import Image
    from mathutils import Euler
    import math
    original_rotation = mesh_obj.rotation_euler.copy()
    
    try:
        mesh_obj.rotation_euler = Euler((0, 0, math.radians(rotation_degrees)), 'XYZ')
        bpy.context.view_layer.update()
        bpy.ops.object.camera_add(location=(0, -5, 0), rotation=(math.pi/2, 0, 0))
        temp_camera = bpy.context.active_object
        temp_camera.location = mesh_obj.location + mesh_obj.matrix_world.to_translation()
        temp_camera.location.y -= 5  # Move back from mesh
        scene = bpy.context.scene
        original_camera = scene.camera
        scene.camera = temp_camera
        original_resolution_x = scene.render.resolution_x
        original_resolution_y = scene.render.resolution_y
        original_film_transparent = scene.render.film_transparent
        scene.render.resolution_x = resolution[0]
        scene.render.resolution_y = resolution[1]
        scene.render.film_transparent = True
        original_materials = list(mesh_obj.data.materials)
        
        silhouette_mat = bpy.data.materials.new(name="SilhouetteMat")
        silhouette_mat.use_nodes = True
        nodes = silhouette_mat.node_tree.nodes
        nodes.clear()
        
        output = nodes.new('ShaderNodeOutputMaterial')
        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = (1, 1, 1, 1)
        emission.inputs['Strength'].default_value = 1.0
        silhouette_mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        mesh_obj.data.materials.clear()
        mesh_obj.data.materials.append(silhouette_mat)
        temp_render = Path(bpy.app.tempdir) / "silhouette_render.png"
        scene.render.filepath = str(temp_render)
        bpy.ops.render.render(write_still=True)
        rendered_image = Image.open(temp_render)
        if rendered_image.mode == 'RGBA':
            alpha = np.array(rendered_image)[:, :, 3]
            silhouette = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
            silhouette[alpha > 128] = 255
            result = Image.fromarray(silhouette, mode='L')
        else:
            result = rendered_image.convert('L')
        bpy.data.objects.remove(temp_camera)
        bpy.data.materials.remove(silhouette_mat)
        mesh_obj.data.materials.clear()
        for mat in original_materials:
            mesh_obj.data.materials.append(mat)
        scene.camera = original_camera
        scene.render.resolution_x = original_resolution_x
        scene.render.resolution_y = original_resolution_y
        scene.render.film_transparent = original_film_transparent
        
        return result
        
    except Exception as e:
        logger.error(f"[Hunyuan3D] Silhouette render failed: {e}")
        return None
        
    finally:
        mesh_obj.rotation_euler = original_rotation
