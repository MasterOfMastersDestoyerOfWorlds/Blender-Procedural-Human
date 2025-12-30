"""
SAM3 (Segment Anything Model 3) integration for Blender.

This module provides a lazy-loading singleton wrapper around the SAM3 model.
The model files are bundled with the addon at procedural_human/image_seg/.
The model is loaded on first use and kept in memory until Blender quits.
"""

import os
from typing import Optional, List, Tuple
import numpy as np
from PIL import Image

from procedural_human.logger import logger

# Get path relative to this file
# __file__ is in procedural_human/segmentation/sam_integration.py
# So go up two levels to get to procedural_human/
_ADDON_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODEL_PATH = os.path.join(_ADDON_ROOT, "image_seg")


class SAM3Manager:
    """
    Singleton manager for SAM3 model operations.
    
    The model is loaded lazily on first use and kept in memory for subsequent calls.
    Supports point-based, box-based, and text prompt segmentation.
    """
    
    _instance: Optional["SAM3Manager"] = None
    _model = None
    _processor = None
    _device: str = "cpu"
    _initialized: bool = False
    
    # Path to bundled model files
    MODEL_PATH = _MODEL_PATH
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> "SAM3Manager":
        """Get the singleton instance of SAM3Manager."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def is_loaded(cls) -> bool:
        """Check if the model is currently loaded."""
        return cls._model is not None
    
    def _load_model(self):
        """Load the SAM3 model and processor."""
        if self._initialized:
            return
        
        logger.info("Loading SAM3 model...")
        
        try:
            import torch
            from transformers import Sam3Processor, Sam3Model
            
            # Determine device
            if torch.cuda.is_available():
                self._device = "cuda"
            else:
                logger.warning("CUDA not available. Using CPU (slower performance).")
                self._device = "cpu"
            
            logger.info(f"SAM3 running on: {self._device}")
            
            # Load model and processor
            self.__class__._model = Sam3Model.from_pretrained(self.MODEL_PATH).to(self._device)
            self.__class__._processor = Sam3Processor.from_pretrained(self.MODEL_PATH)
            self.__class__._model.eval()
            
            self._initialized = True
            logger.info("SAM3 model loaded successfully.")
            
        except ImportError as e:
            logger.error(f"Failed to import SAM3 dependencies: {e}")
            logger.error("Please install: pip install torch torchvision transformers")
            raise
        except Exception as e:
            logger.error(f"Failed to load SAM3 model: {e}")
            raise
    
    def ensure_loaded(self):
        """Ensure the model is loaded (lazy loading)."""
        if not self._initialized:
            self._load_model()
    
    def segment_by_prompt(
        self, 
        image: Image.Image, 
        text_prompt: str,
        threshold: float = 0.5,
        mask_threshold: float = 0.5
    ) -> List[np.ndarray]:
        """
        Segment an image using a text prompt.
        
        Args:
            image: PIL Image to segment
            text_prompt: Text description of what to segment
            threshold: Detection threshold
            mask_threshold: Mask binarization threshold
            
        Returns:
            List of binary mask arrays
        """
        import torch
        
        self.ensure_loaded()
        
        logger.info(f"Segmenting by prompt: '{text_prompt}'")
        
        # Prepare inputs
        inputs = self._processor(
            images=image, 
            text=text_prompt, 
            return_tensors="pt"
        ).to(self._device)
        
        # Run inference
        with torch.no_grad():
            outputs = self._model(**inputs)
        
        # Post-process results
        results = self._processor.post_process_instance_segmentation(
            outputs,
            threshold=threshold,
            mask_threshold=mask_threshold,
            target_sizes=inputs.get("original_sizes").tolist()
        )[0]
        
        masks = []
        for mask_tensor in results.get("masks", []):
            mask_np = mask_tensor.cpu().numpy().astype(bool)
            masks.append(mask_np)
        
        logger.info(f"Found {len(masks)} segments.")
        return masks
    
    def segment_by_point(
        self, 
        image: Image.Image, 
        points: List[Tuple[int, int]],
        labels: Optional[List[int]] = None,
        threshold: float = 0.5,
        mask_threshold: float = 0.5
    ) -> List[np.ndarray]:
        """
        Segment an image using point prompts.
        
        Args:
            image: PIL Image to segment
            points: List of (x, y) point coordinates
            labels: List of labels (1 for foreground, 0 for background)
                   If None, all points are treated as foreground
            threshold: Detection threshold
            mask_threshold: Mask binarization threshold
            
        Returns:
            List of binary mask arrays
        """
        import torch
        
        self.ensure_loaded()
        
        if labels is None:
            labels = [1] * len(points)
        
        logger.info(f"Segmenting by {len(points)} points")
        
        # Convert points to numpy arrays
        input_points = np.array(points)
        input_labels = np.array(labels)
        
        # Prepare inputs with point prompts
        inputs = self._processor(
            images=image,
            input_points=[input_points.tolist()],
            input_labels=[input_labels.tolist()],
            return_tensors="pt"
        ).to(self._device)
        
        # Run inference
        with torch.no_grad():
            outputs = self._model(**inputs)
        
        # Post-process results
        results = self._processor.post_process_instance_segmentation(
            outputs,
            threshold=threshold,
            mask_threshold=mask_threshold,
            target_sizes=[[image.height, image.width]]
        )[0]
        
        masks = []
        for mask_tensor in results.get("masks", []):
            mask_np = mask_tensor.cpu().numpy().astype(bool)
            masks.append(mask_np)
        
        logger.info(f"Found {len(masks)} segments.")
        return masks
    
    def segment_by_box(
        self, 
        image: Image.Image, 
        box: Tuple[int, int, int, int],
        threshold: float = 0.5,
        mask_threshold: float = 0.5
    ) -> List[np.ndarray]:
        """
        Segment an image using a bounding box prompt.
        
        Args:
            image: PIL Image to segment
            box: Bounding box as (x_min, y_min, x_max, y_max)
            threshold: Detection threshold
            mask_threshold: Mask binarization threshold
            
        Returns:
            List of binary mask arrays
        """
        import torch
        
        self.ensure_loaded()
        
        logger.info(f"Segmenting by box: {box}")
        
        # Prepare inputs with box prompt
        inputs = self._processor(
            images=image,
            input_boxes=[[list(box)]],
            return_tensors="pt"
        ).to(self._device)
        
        # Run inference
        with torch.no_grad():
            outputs = self._model(**inputs)
        
        # Post-process results
        results = self._processor.post_process_instance_segmentation(
            outputs,
            threshold=threshold,
            mask_threshold=mask_threshold,
            target_sizes=[[image.height, image.width]]
        )[0]
        
        masks = []
        for mask_tensor in results.get("masks", []):
            mask_np = mask_tensor.cpu().numpy().astype(bool)
            masks.append(mask_np)
        
        logger.info(f"Found {len(masks)} segments.")
        return masks
    
    @classmethod
    def unload(cls):
        """Unload the model from memory."""
        if cls._model is not None:
            import torch
            del cls._model
            del cls._processor
            cls._model = None
            cls._processor = None
            cls._initialized = False
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            logger.info("SAM3 model unloaded.")
