"""
SAM3 (Segment Anything Model 3) integration for Blender.

This module provides a lazy-loading singleton wrapper around the SAM3 model.
The model files are bundled with the addon at procedural_human/image_seg/.
The model is loaded on first use and kept in memory until Blender quits.
"""
from __future__ import annotations  # PEP 563: Postponed evaluation of annotations

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
def _patch_transformers_deps():
    import sys
    import types
    if 'transformers.dependency_versions_check' not in sys.modules:
        fake_module = types.ModuleType('transformers.dependency_versions_check')
        fake_module.dep_version_check = lambda *args, **kwargs: None
        sys.modules['transformers.dependency_versions_check'] = fake_module

from typing import Optional, List, Tuple, TYPE_CHECKING

from procedural_human.logger import logger
if TYPE_CHECKING:
    import numpy as np
    from PIL import Image
    import torch
    from transformers import Sam3Processor, Sam3Model
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
    _Sam3Model = None
    _Sam3Processor = None
    _is_loading: bool = False
    _loading_progress: str = ""
    _loading_error: Optional[str] = None
    _loading_thread = None  # Threading for async loading
    
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
    
    @classmethod
    def is_loading(cls) -> bool:
        """Check if the model is currently being loaded."""
        return cls._is_loading
    
    @classmethod
    def get_loading_progress(cls) -> str:
        """Get the current loading progress message."""
        return cls._loading_progress
    
    @classmethod
    def get_loading_error(cls) -> Optional[str]:
        """Get the last loading error, if any."""
        return cls._loading_error
    
    def _load_model(self):
        """Load the SAM3 model and processor."""
        if self._initialized:
            return
        
        if self.__class__._is_loading:
            logger.warning("SAM3 model is already loading...")
            return
        
        logger.info("Loading SAM3 model...")
        
        self.__class__._is_loading = True
        self.__class__._loading_error = None
        self.__class__._loading_progress = "Starting..."
        import bpy
        wm = bpy.context.window_manager
        wm.progress_begin(0, 100)
        
        def set_status(msg: str):
            """Set status text in all areas that support it."""
            self.__class__._loading_progress = msg
            try:
                for window in bpy.context.window_manager.windows:
                    for area in window.screen.areas:
                        area.header_text_set(msg)
                        if area.type == 'IMAGE_EDITOR':
                            area.tag_redraw()
            except:
                pass
        
        try:
            set_status("Loading SAM3: Importing dependencies...")
            wm.progress_update(10)
            _patch_transformers_deps()
            import torch
            from transformers import Sam3Processor, Sam3Model
            wm.progress_update(20)
            if torch.cuda.is_available():
                self._device = "cuda"
                set_status("Loading SAM3: Using CUDA GPU...")
            else:
                logger.warning("CUDA not available. Using CPU (slower performance).")
                self._device = "cpu"
                set_status("Loading SAM3: Using CPU (no CUDA)...")
            
            logger.info(f"SAM3 running on: {self._device}")
            set_status("Loading SAM3: Loading model weights (this may take a moment)...")
            wm.progress_update(30)
            self.__class__._model = Sam3Model.from_pretrained(self.MODEL_PATH).to(self._device)
            set_status("Loading SAM3: Loading processor...")
            wm.progress_update(90)
            self.__class__._processor = Sam3Processor.from_pretrained(self.MODEL_PATH)
            self.__class__._model.eval()
            wm.progress_update(100)
            self._initialized = True
            set_status("SAM3 model loaded successfully!")
            logger.info("SAM3 model loaded successfully.")
            
        except ImportError as e:
            self.__class__._loading_error = f"Missing dependencies: {e}"
            set_status("SAM3 loading failed - missing dependencies")
            logger.error(f"Failed to import SAM3 dependencies: {e}")
            logger.error("Please install: pip install torch torchvision transformers")
            raise
        except Exception as e:
            self.__class__._loading_error = str(e)
            set_status(f"SAM3 loading failed: {e}")
            logger.error(f"Failed to load SAM3 model: {e}")
            raise
        finally:
            self.__class__._is_loading = False
            wm.progress_end()
            def clear_status():
                self.__class__._loading_progress = ""
                try:
                    for window in bpy.context.window_manager.windows:
                        for area in window.screen.areas:
                            area.header_text_set(None)
                except:
                    pass
                return None  # Don't repeat
            bpy.app.timers.register(clear_status, first_interval=2.0)
    
    def ensure_loaded(self):
        """Ensure the model is loaded (lazy loading)."""
        if not self._initialized:
            self._load_model()
    
    @classmethod
    def start_loading_async(cls):
        """
        Start loading the model in a background thread.
        
        Returns True if loading started, False if already loaded/loading.
        
        Pre-imports heavy modules on the main thread to avoid regex compilation
        issues in background threads (Blender's embedded Python has threading issues
        with Python's regex module).
        """
        if cls._initialized:
            return False  # Already loaded
        
        if cls._is_loading:
            return False  # Already loading
        
        import threading
        
        cls._is_loading = True
        cls._loading_error = None
        cls._loading_progress = "Pre-importing modules..."
        try:
            _patch_transformers_deps()
            os.environ["TOKENIZERS_PARALLELISM"] = "false"
            os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
            os.environ["TRANSFORMERS_VERBOSITY"] = "error"
            import torch
            from transformers import Sam3Processor, Sam3Model
            cls._Sam3Model = Sam3Model
            cls._Sam3Processor = Sam3Processor
            cls._torch = torch
            
            logger.info("Pre-imported transformers modules on main thread")
        except Exception as e:
            cls._loading_error = f"Failed to import dependencies: {e}"
            cls._is_loading = False
            logger.error(f"SAM3 pre-import failed: {e}")
            return False
        
        cls._loading_progress = "Starting background load..."
        
        def load_thread():
            try:
                cls._load_model_internal()
            except Exception as e:
                cls._loading_error = str(e)
                logger.error(f"SAM3 async load failed: {e}")
            finally:
                cls._is_loading = False
        
        cls._loading_thread = threading.Thread(target=load_thread, daemon=True)
        cls._loading_thread.start()
        return True
    
    @classmethod
    def _load_model_internal(cls):
        """
        Internal model loading - runs in background thread.
        
        Uses pre-imported classes from start_loading_async() to avoid
        regex compilation issues in threads.
        Does not use Blender UI functions (not thread-safe).
        """
        if cls._initialized:
            return
        
        logger.info("Loading SAM3 model (background thread)...")
        
        try:
            Sam3Model = cls._Sam3Model
            Sam3Processor = cls._Sam3Processor
            torch = cls._torch
            cls._loading_progress = "Detecting device..."
            if torch.cuda.is_available():
                device = "cuda"
            else:
                logger.warning("CUDA not available. Using CPU (slower performance).")
                device = "cpu"
            
            logger.info(f"SAM3 running on: {device}")
            cls._loading_progress = "Loading model weights..."
            cls._model = Sam3Model.from_pretrained(cls.MODEL_PATH).to(device)
            cls._loading_progress = "Loading processor..."
            cls._processor = Sam3Processor.from_pretrained(cls.MODEL_PATH)
            cls._model.eval()
            
            cls._device = device
            cls._initialized = True
            cls._loading_progress = "Ready"
            logger.info("SAM3 model loaded successfully (async).")
            
        except Exception as e:
            cls._loading_error = str(e)
            logger.error(f"Failed to load SAM3 model: {e}")
            raise
    
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
        inputs = self._processor(
            images=image, 
            text=text_prompt, 
            return_tensors="pt"
        ).to(self._device)
        with self._get_torch().no_grad():
            outputs = self._model(**inputs)
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
        inputs = self._processor(
            images=image,
            return_tensors="pt"
        ).to(self._device)
        input_points = torch.tensor([points], dtype=torch.float32, device=self._device)
        input_labels = torch.tensor([labels], dtype=torch.int64, device=self._device)
        with self._get_torch().no_grad():
            outputs = self._model(
                **inputs,
                input_points=input_points,
                input_labels=input_labels,
            )
        masks = []
        if hasattr(outputs, 'pred_masks') and outputs.pred_masks is not None:
            pred_masks = outputs.pred_masks
            scores = outputs.iou_scores if hasattr(outputs, 'iou_scores') else None
            if scores is not None and len(scores.shape) > 1:
                best_idx = scores[0].argmax().item()
                mask = pred_masks[0, best_idx]
            else:
                mask = pred_masks[0, 0]
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
        inputs = self._processor(
            images=image,
            return_tensors="pt"
        ).to(self._device)
        input_boxes = torch.tensor([[list(box)]], dtype=torch.float32, device=self._device)
        with torch.no_grad():
            outputs = self._model(
                **inputs,
                input_boxes=input_boxes,
            )
        masks = []
        if hasattr(outputs, 'pred_masks') and outputs.pred_masks is not None:
            pred_masks = outputs.pred_masks
            scores = outputs.iou_scores if hasattr(outputs, 'iou_scores') else None
            if scores is not None and len(scores.shape) > 1:
                best_idx = scores[0].argmax().item()
                mask = pred_masks[0, best_idx]
            else:
                mask = pred_masks[0, 0]
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
