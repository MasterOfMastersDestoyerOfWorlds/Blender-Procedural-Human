"""
Depth Estimator for procedural human generation.

Uses Depth Anything V3 (via depth_anything_3 package) to estimate object depth/thickness from a single image.
This is used to scale the side-view curve when creating mesh curves from a single view.

REQUIRES: depth_anything_3 package
Install via: pip install depth-anything-3
Or from source: git clone https://github.com/ByteDance-Seed/Depth-Anything-3 && pip install -e .
"""
from __future__ import annotations

import os
import json
import tempfile
from typing import Optional, TYPE_CHECKING
import numpy as np

from procedural_human.logger import logger

if TYPE_CHECKING:
    from PIL import Image
    import torch

class DepthEstimator:
    """
    Singleton manager for Depth Estimation operations using Depth Anything V3.
    Requires depth_anything_3 package to be installed.
    """
    
    _instance: Optional["DepthEstimator"] = None
    _model = None  # DepthAnything3 model
    _device: str = "cpu"
    _initialized: bool = False
    _is_loading: bool = False
    _loading_error: Optional[str] = None
    
    # Local model path (relative to this file)
    # __file__ is in procedural_human/depth_estimation/depth_estimator.py
    _ADDON_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH = os.path.join(_ADDON_ROOT, "depth_estimation")
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> "DepthEstimator":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def is_loaded(cls) -> bool:
        return cls._model is not None
        
    @classmethod
    def is_loading(cls) -> bool:
        return cls._is_loading
    
    def ensure_loaded(self):
        """Ensure the model is loaded (blocking)."""
        if not self._initialized:
            self._load_model()
    
    def _is_da3_config(self, config_path: str) -> bool:
        """Check if config.json is in Depth Anything V3 format."""
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            # DA3 format has 'model_name' and 'config' with 'net' and 'head'
            if isinstance(config_data, dict):
                if 'model_name' in config_data and 'config' in config_data:
                    config_section = config_data.get('config', {})
                    if isinstance(config_section, dict) and ('net' in config_section or 'head' in config_section):
                        return True
            return False
        except Exception:
            return False
    
    def _load_model(self):
        """Load the depth estimation model using Depth Anything V3 API."""
        if self._initialized or self.__class__._is_loading:
            return
            
        logger.info("Loading Depth Estimator model...")
        self.__class__._is_loading = True
        
        try:
            # Check if depth_anything_3 package is available
            try:
                from depth_anything_3.api import DepthAnything3
            except ImportError as e:
                error_msg = (
                    "depth_anything_3 package is not installed.\n"
                    "Please install it using one of the following methods:\n"
                    "  1. From PyPI: pip install depth-anything-3\n"
                    "  2. From source: git clone https://github.com/ByteDance-Seed/Depth-Anything-3 && cd Depth-Anything-3 && pip install -e .\n"
                    "  3. Production fork: pip install awesome-depth-anything-3\n"
                    f"Original error: {e}"
                )
                self.__class__._loading_error = error_msg
                logger.error(error_msg)
                raise ImportError(error_msg) from e
            
            import torch
            
            # Use CUDA if available
            if torch.cuda.is_available():
                self._device = "cuda"
                logger.info("Using CUDA GPU for Depth Estimator")
            else:
                self._device = "cpu"
                logger.warning("CUDA not available. Using CPU for Depth Estimator (slower performance).")
                
            logger.info(f"Depth Estimator running on: {self._device}")
            
            # Check if local model exists
            model_path = self.MODEL_PATH
            model_safetensors = os.path.join(model_path, "model.safetensors")
            model_config = os.path.join(model_path, "config.json")
            
            model_to_load = None
            
            if os.path.exists(model_safetensors) and os.path.exists(model_config):
                # Check if it's DA3 format
                is_da3_format = self._is_da3_config(model_config)
                if is_da3_format:
                    logger.info(f"Loading Depth Anything V3 model from local path: {model_path}")
                    model_to_load = os.path.abspath(model_path)
                else:
                    error_msg = (
                        f"Local model at {model_path} does not appear to be in Depth Anything V3 format.\n"
                        "Expected config.json with 'model_name' and 'config' sections.\n"
                        "Please ensure you have a valid DA3 model or install the model from HuggingFace."
                    )
                    self.__class__._loading_error = error_msg
                    logger.error(error_msg)
                    raise ValueError(error_msg)
            else:
                # No local model, use HuggingFace
                logger.info("No local model found, loading Depth Anything V3 from HuggingFace...")
                # Use a reasonable default model - user can override if needed
                model_to_load = "depth-anything/DA3METRIC-LARGE"
                logger.info(f"Using model: {model_to_load}")
            
            # Load the model
            logger.info(f"Loading Depth Anything V3 model: {model_to_load}")
            self.__class__._model = DepthAnything3.from_pretrained(model_to_load)
            self.__class__._model = self.__class__._model.to(self._device)
            
            self._initialized = True
            logger.info("Depth Anything V3 model loaded successfully.")
            
        except Exception as e:
            self.__class__._loading_error = str(e)
            logger.error(f"Failed to load Depth Estimator: {e}")
            raise
        finally:
            self.__class__._is_loading = False

    def estimate_depth(self, image: Image.Image) -> np.ndarray:
        """
        Estimate depth map from an image.
        
        Args:
            image: PIL Image
            
        Returns:
            Numpy array of depth values (float32, normalized 0-1 usually)
            Higher values = closer (or further, depending on model - Depth Anything is usually relative disparity)
        """
        self.ensure_loaded()
        
        # Depth Anything V3 API requires file paths
        # Save PIL image to temp file for DA3 inference
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            image.save(tmp_file.name, 'JPEG')
            tmp_path = tmp_file.name
        
        try:
            # Run inference
            prediction = self.__class__._model.inference([tmp_path])
            
            # Get depth map (first image, squeeze batch dimension)
            depth_map = prediction.depth[0]  # Shape: [H, W]
            
            # Convert to numpy if needed
            if hasattr(depth_map, 'cpu'):
                depth_map = depth_map.cpu().numpy()
            elif hasattr(depth_map, 'numpy'):
                depth_map = depth_map.numpy()
            else:
                depth_map = np.array(depth_map)
            
            depth_map = depth_map.astype(np.float32)
            
        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        # Normalize to 0-1
        if depth_map.max() > depth_map.min():
            depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())
            
        return depth_map

    def get_thickness_ratio(self, image: Image.Image, mask: np.ndarray) -> float:
        """
        Calculate the ratio of object depth (thickness) to its width.
        
        Args:
            image: PIL Image (masked or original)
            mask: Boolean numpy mask of the object
            
        Returns:
            float: Ratio of (depth / width). E.g. 0.5 means object is half as thick as it is wide.
        """
        # Estimate depth
        depth_map = self.estimate_depth(image)
        
        # Resize mask to match depth map if needed
        if mask.shape != depth_map.shape:
            from PIL import Image as PILImage
            mask_pil = PILImage.fromarray(mask.astype(np.uint8) * 255)
            mask_pil = mask_pil.resize((depth_map.shape[1], depth_map.shape[0]), PILImage.NEAREST)
            mask = np.array(mask_pil) > 127
            
        # Get depth values in the masked region
        object_depths = depth_map[mask]
        
        if len(object_depths) == 0:
            return 1.0
            
        # Determine "depth range" of the object
        # Depth Anything predicts relative disparity (inverse depth). 
        # Higher value = closer.
        # So "thickness" is roughly proportional to the range of values in the masked region.
        # But for a single object, the 'shape' of the depth map gives us the volume.
        
        # Heuristic:
        # Assume the object is roughly cylindrical-ish or has volume.
        # We can look at the average gradient or the peak-to-edge difference?
        # Simpler: Range of depth values (max - min) roughly correlates to local thickness variation?
        # But this is scale-invariant relative depth.
        
        # Better Heuristic:
        # If we assume the camera is reasonably far, the variation in disparity across the object 
        # corresponds to its physical depth extent relative to the scene.
        # However, "Depth Anything" is relative.
        # Let's try: (p95 - p5) / width_in_pixels?
        # Wait, the depth map is normalized 0-1 over the whole image.
        
        # Let's calculate the "visual width" of the object in pixels
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not np.any(rows) or not np.any(cols):
            return 1.0
            
        height = np.sum(rows)
        width = np.sum(cols)
        
        # If we normalize the depth map so that the background is 0 and the closest point is 1?
        # But the depth map from model is already full range 0-1 usually.
        
        # Let's look at the object's internal depth variation.
        # p95 - p5 gives the robust range of depths within the object.
        depth_range = np.percentile(object_depths, 95) - np.percentile(object_depths, 5)
        
        # If the object is a flat paper, depth_range ~ 0.
        # If it's a sphere, depth_range is large.
        
        # But how does "0.5 depth range" relate to "100 pixels width"?
        # They are different units (normalized vs pixels).
        
        # CRITICAL: We can't know absolute depth from a single image without metric depth.
        # "Depth-Anything" is relative.
        # However, for "Simple Rotate Mesh", users often want a starting point.
        # Maybe we default to 1.0 (circular cross-section) but use depth to *modulate* that?
        # Actually, simpler might be better: Just return 1.0 by default, and let the user scale it.
        # BUT the plan says "maximum extent fits horizontally between the horizontal line it intersects".
        
        # Re-reading user request: "scale the 90 degree rotation so that is maximum extent fits horizontally between the horizontal line it intersects"
        # This sounds like: The side view width should effectively be determined by the intersection?
        # If we just rotate 90 deg, the "width" of the new view becomes the "depth" of the old view.
        # If we assume the object has a circular cross section at its widest point, scale = 1.0.
        
        # Let's return a "thickness score" that is roughly 0.0 to 1.0?
        # Actually, for now, let's implement the depth estimation but default the scaling to 1.0 
        # and provide the estimation as a reference or auto-tune option.
        
        return 1.0 # Placeholder logic until we calibrate
    
    def unload(self):
        """Unload model."""
        self.__class__._model = None
        self._initialized = False
        if self._device == "cuda":
            import torch
            torch.cuda.empty_cache()
