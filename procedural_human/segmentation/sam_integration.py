"""
SAM3 (Segment Anything Model 3) integration for Blender.

This module provides a lazy-loading singleton wrapper around the SAM3 model.
The model files are bundled with the addon at procedural_human/image_seg/.
The model is loaded on first use and kept in memory until Blender quits.
"""
from __future__ import annotations  # PEP 563: Postponed evaluation of annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Patch transformers version check before importing
# The 5.0.0.dev0 version has outdated deps check requiring huggingface_hub<1.0
# but actually needs >=1.2 at runtime
def _patch_transformers_deps():
    import sys
    import types
    
    # Create a fake dependency_versions_check module with all expected exports
    if 'transformers.dependency_versions_check' not in sys.modules:
        fake_module = types.ModuleType('transformers.dependency_versions_check')
        # Add the function that deepspeed.py imports
        fake_module.dep_version_check = lambda *args, **kwargs: None
        sys.modules['transformers.dependency_versions_check'] = fake_module

from typing import Optional, List, Tuple, TYPE_CHECKING

from procedural_human.logger import logger

# Heavy imports are lazy-loaded to speed up addon startup
# torch, transformers, numpy, PIL are only imported when SAM features are used
if TYPE_CHECKING:
    import numpy as np
    from PIL import Image
    import torch
    from transformers import Sam3Processor, Sam3Model

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
    _torch = None  # Lazily imported torch module
    _np = None  # Lazily imported numpy module
    
    @classmethod
    def _get_torch(cls):
        """Get lazily imported torch module."""
        if cls._torch is None:
            import torch
            cls._torch = torch
        return cls._torch
    
    @classmethod
    def _get_numpy(cls):
        """Get lazily imported numpy module."""
        if cls._np is None:
            import numpy as np
            cls._np = np
        return cls._np
    
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
            # Lazy import heavy dependencies
            _patch_transformers_deps()
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
        
        self.ensure_loaded()
        
        if labels is None:
            labels = [1] * len(points)
        
        logger.info(f"Segmenting by {len(points)} points")
        
        torch = self._get_torch()
        
        # Process image first (without points - new API)
        inputs = self._processor(
            images=image,
            return_tensors="pt"
        ).to(self._device)
        
        # Create point and label tensors separately
        # Shape: (batch_size, num_points, 2) for points
        # Shape: (batch_size, num_points) for labels
        input_points = torch.tensor([points], dtype=torch.float32, device=self._device)
        input_labels = torch.tensor([labels], dtype=torch.int64, device=self._device)
        
        # Run inference with points passed directly to model
        with self._get_torch().no_grad():
            outputs = self._model(
                **inputs,
                input_points=input_points,
                input_labels=input_labels,
            )
        
        # Post-process results using mask output
        # SAM3 returns pred_masks of shape (batch, num_masks, H, W)
        masks = []
        if hasattr(outputs, 'pred_masks') and outputs.pred_masks is not None:
            pred_masks = outputs.pred_masks
            # Get scores if available
            scores = outputs.iou_scores if hasattr(outputs, 'iou_scores') else None
            
            # Select best mask based on IoU score
            if scores is not None and len(scores.shape) > 1:
                best_idx = scores[0].argmax().item()
                mask = pred_masks[0, best_idx]
            else:
                mask = pred_masks[0, 0]
            
            # Resize mask to original image size and threshold
            mask_resized = torch.nn.functional.interpolate(
                mask.unsqueeze(0).unsqueeze(0).float(),
                size=(image.height, image.width),
                mode='bilinear',
                align_corners=False
            )[0, 0]
            
            mask_np = (mask_resized > mask_threshold).cpu().numpy().astype(bool)
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
        
        self.ensure_loaded()
        
        logger.info(f"Segmenting by box: {box}")
        
        torch = self._get_torch()
        
        # Process image first (without boxes - new API)
        inputs = self._processor(
            images=image,
            return_tensors="pt"
        ).to(self._device)
        
        # Create box tensor separately
        # Shape: (batch_size, num_boxes, 4) - format is (x_min, y_min, x_max, y_max)
        input_boxes = torch.tensor([[list(box)]], dtype=torch.float32, device=self._device)
        
        # Run inference with boxes passed directly to model
        with torch.no_grad():
            outputs = self._model(
                **inputs,
                input_boxes=input_boxes,
            )
        
        # Post-process results using mask output
        masks = []
        if hasattr(outputs, 'pred_masks') and outputs.pred_masks is not None:
            pred_masks = outputs.pred_masks
            scores = outputs.iou_scores if hasattr(outputs, 'iou_scores') else None
            
            # Select best mask based on IoU score
            if scores is not None and len(scores.shape) > 1:
                best_idx = scores[0].argmax().item()
                mask = pred_masks[0, best_idx]
            else:
                mask = pred_masks[0, 0]
            
            # Resize mask to original image size and threshold
            mask_resized = torch.nn.functional.interpolate(
                mask.unsqueeze(0).unsqueeze(0).float(),
                size=(image.height, image.width),
                mode='bilinear',
                align_corners=False
            )[0, 0]
            
            mask_np = (mask_resized > mask_threshold).cpu().numpy().astype(bool)
            masks.append(mask_np)
        
        logger.info(f"Found {len(masks)} segments.")
        return masks
    
    @classmethod
    def unload(cls):
        """Unload the model from memory."""
        if cls._model is not None:
            del cls._model
            del cls._processor
            cls._model = None
            cls._processor = None
            cls._initialized = False
            if cls._torch is not None and cls._torch.cuda.is_available():
                cls._torch.cuda.empty_cache()
            logger.info("SAM3 model unloaded.")
