"""
Hunyuan3D API Client

HTTP client for communicating with the Hunyuan3D API server.
Sends images and receives 3D meshes (GLB format).

Usage:
    from procedural_human.novel_view_gen.api_client import generate_3d_mesh
    
    # Generate 3D mesh from PIL image
    glb_bytes = generate_3d_mesh(pil_image)
    
    # Save to file
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
    
    # Load image if path provided
    if isinstance(image, (str, Path)):
        image = Image.open(image)
    
    # Convert to base64
    image_b64 = image_to_base64(image)
    
    # Build request
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
    
    logger.info(f"[Hunyuan3D] Sending image to API (size: {image.size})")
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                glb_bytes = response.read()
                logger.info(f"[Hunyuan3D] Received GLB mesh ({len(glb_bytes)} bytes)")
                return glb_bytes
            else:
                logger.error(f"[Hunyuan3D] API returned status {response.status}")
                return None
                
    except urllib.error.HTTPError as e:
        logger.error(f"[Hunyuan3D] HTTP error: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode("utf-8")
            logger.error(f"[Hunyuan3D] Error details: {error_body}")
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
    
    # Remember existing objects
    existing_objects = set(bpy.data.objects)
    
    try:
        # Import GLB
        bpy.ops.import_scene.gltf(filepath=glb_path)
        
        # Find newly imported objects
        new_objects = set(bpy.data.objects) - existing_objects
        
        if new_objects:
            # Return the first mesh object found
            for obj in new_objects:
                if obj.type == 'MESH':
                    return obj
            # If no mesh, return any new object
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
    # Generate mesh
    glb_bytes = generate_3d_mesh(image, **kwargs)
    
    if glb_bytes is None:
        return None
    
    # Save to temp file
    temp_path = save_glb_to_temp(glb_bytes)
    
    # Import to Blender
    obj = import_glb_to_blender(temp_path)
    
    # Clean up temp file
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
    
    # Store original rotation
    original_rotation = mesh_obj.rotation_euler.copy()
    
    try:
        # Rotate mesh
        mesh_obj.rotation_euler = Euler((0, 0, math.radians(rotation_degrees)), 'XYZ')
        bpy.context.view_layer.update()
        
        # Create a temporary camera looking at the mesh
        bpy.ops.object.camera_add(location=(0, -5, 0), rotation=(math.pi/2, 0, 0))
        temp_camera = bpy.context.active_object
        
        # Point camera at mesh center
        temp_camera.location = mesh_obj.location + mesh_obj.matrix_world.to_translation()
        temp_camera.location.y -= 5  # Move back from mesh
        
        # Set up render settings for silhouette
        scene = bpy.context.scene
        original_camera = scene.camera
        scene.camera = temp_camera
        
        # Store original render settings
        original_resolution_x = scene.render.resolution_x
        original_resolution_y = scene.render.resolution_y
        original_film_transparent = scene.render.film_transparent
        
        # Configure for silhouette render
        scene.render.resolution_x = resolution[0]
        scene.render.resolution_y = resolution[1]
        scene.render.film_transparent = True
        
        # Create a simple material for silhouette (white emission)
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
        
        # Render to file
        temp_render = Path(bpy.app.tempdir) / "silhouette_render.png"
        scene.render.filepath = str(temp_render)
        bpy.ops.render.render(write_still=True)
        
        # Load rendered image
        rendered_image = Image.open(temp_render)
        
        # Convert to silhouette (alpha channel -> white on black)
        if rendered_image.mode == 'RGBA':
            alpha = np.array(rendered_image)[:, :, 3]
            silhouette = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
            silhouette[alpha > 128] = 255
            result = Image.fromarray(silhouette, mode='L')
        else:
            result = rendered_image.convert('L')
        
        # Cleanup
        bpy.data.objects.remove(temp_camera)
        bpy.data.materials.remove(silhouette_mat)
        
        # Restore original materials
        mesh_obj.data.materials.clear()
        for mat in original_materials:
            mesh_obj.data.materials.append(mat)
        
        # Restore render settings
        scene.camera = original_camera
        scene.render.resolution_x = original_resolution_x
        scene.render.resolution_y = original_resolution_y
        scene.render.film_transparent = original_film_transparent
        
        return result
        
    except Exception as e:
        logger.error(f"[Hunyuan3D] Silhouette render failed: {e}")
        return None
        
    finally:
        # Restore original rotation
        mesh_obj.rotation_euler = original_rotation
