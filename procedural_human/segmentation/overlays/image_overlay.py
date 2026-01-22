import numpy as np
from procedural_human.logger import logger

_original_image_pixels = None  # Store original pixels for reset
def store_original_image(image):
    """Store the original image pixels for later restoration."""
    global _original_image_pixels
    if image is not None:
        _original_image_pixels = np.array(image.pixels[:]).copy()


def get_original_image_pixels():
    """Get the stored original image pixels."""
    return _original_image_pixels


def restore_original_image(image):
    """Restore the image to its original pixels."""
    global _original_image_pixels
    if _original_image_pixels is not None and image is not None:
        width, height = image.size
        expected_len = width * height * 4
        if len(_original_image_pixels) != expected_len:
            logger.warning(f"restore_original_image: Size mismatch (Stored: {len(_original_image_pixels)}, Target: {expected_len}). Skipping.")
            return
        image.pixels[:] = _original_image_pixels.tolist()
        image.update()
