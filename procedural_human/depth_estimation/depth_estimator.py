"""
Depth Estimator for procedural human generation.

Uses 'Depth-Anything' (via transformers) to estimate object depth/thickness from a single image.
This is used to scale the side-view curve when creating mesh curves from a single view.
"""
from __future__ import annotations

import os
from typing import Optional, TYPE_CHECKING
import numpy as np

from procedural_human.logger import logger

if TYPE_CHECKING:
    from PIL import Image
    import torch
    from transformers import Pipeline

# Lazy import helpers
_torch = None
_pipeline = None

class DepthEstimator:
    """
    Singleton manager for Depth Estimation operations.
    """
    
    _instance: Optional["DepthEstimator"] = None
    _pipeline = None
    _device: str = "cpu"
    _initialized: bool = False
    _is_loading: bool = False
    _loading_error: Optional[str] = None
    
    # Model ID for Depth Anything (Small is fast and good enough)
    MODEL_ID = "LiheYoung/depth-anything-small-hf"
    
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
        return cls._pipeline is not None
        
    @classmethod
    def is_loading(cls) -> bool:
        return cls._is_loading
        
    def ensure_loaded(self):
        """Ensure the model is loaded (blocking)."""
        if not self._initialized:
            self._load_model()
            
    def _load_model(self):
        """Load the depth estimation model."""
        if self._initialized or self.__class__._is_loading:
            return
            
        logger.info("Loading Depth Estimator model...")
        self.__class__._is_loading = True
        
        try:
            import torch
            from transformers import pipeline
            
            if torch.cuda.is_available():
                self._device = "cuda"
            else:
                self._device = "cpu"
                
            logger.info(f"Depth Estimator running on: {self._device}")
            
            # Load pipeline
            self.__class__._pipeline = pipeline(
                task="depth-estimation", 
                model=self.MODEL_ID, 
                device=0 if self._device == "cuda" else -1
            )
            
            self._initialized = True
            logger.info("Depth Estimator loaded successfully.")
            
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
        
        # Inference
        # pipeline returns a dict with 'depth' (PIL Image) or 'predicted_depth' (tensor) depending on config
        # The standard depth-estimation pipeline returns a dict with 'depth' as a PIL image
        result = self.__class__._pipeline(image)
        
        depth_img = result["depth"]
        
        # Convert to numpy
        depth_map = np.array(depth_img).astype(np.float32)
        
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
        self.__class__._pipeline = None
        self._initialized = False
        if self._device == "cuda":
            import torch
            torch.cuda.empty_cache()
