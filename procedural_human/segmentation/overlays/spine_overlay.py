import numpy as np
_current_spine_path = None  # Store spine path for debug visualization (Nx2 image coords)

def get_current_spine_path():
    """Get the currently stored spine path (Nx2 array of image coordinates)."""
    return _current_spine_path


def set_current_spine_path(spine_path):
    """Store the spine path for debug visualization.
    
    Args:
        spine_path: Nx2 numpy array of (x, y) coordinates in image space
    """
    global _current_spine_path
    _current_spine_path = spine_path

def apply_spine_overlay(image, spine_path, color=(1.0, 0.0, 1.0), line_width=3):
    """
    Apply a spine path overlay onto a Blender image.
    
    Args:
        image: Blender image object
        spine_path: Nx2 numpy array of (x, y) coordinates in image space
        color: RGB tuple for the line color
        line_width: Width of the line in pixels
    """
    if spine_path is None or len(spine_path) < 2:
        return
    
    width, height = image.size
    pixels = np.array(image.pixels[:]).reshape(height, width, 4)
    for i in range(len(spine_path) - 1):
        x0, y0 = spine_path[i]
        x1, y1 = spine_path[i + 1]
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        steps = max(int(max(dx, dy)), 1)
        
        for t in range(steps + 1):
            frac = t / steps if steps > 0 else 0
            x = int(x0 + frac * (x1 - x0))
            y = int(y0 + frac * (y1 - y0))
            for ox in range(-line_width, line_width + 1):
                for oy in range(-line_width, line_width + 1):
                    px, py = x + ox, y + oy
                    py_flipped = height - 1 - py
                    if 0 <= px < width and 0 <= py_flipped < height:
                        pixels[py_flipped, px, 0] = color[0]
                        pixels[py_flipped, px, 1] = color[1]
                        pixels[py_flipped, px, 2] = color[2]
                        pixels[py_flipped, px, 3] = 1.0
    for idx, point in enumerate([spine_path[0], spine_path[-1]]):
        x, y = int(point[0]), int(point[1])
        endpoint_color = (0.0, 1.0, 0.0) if idx == 0 else (1.0, 0.0, 0.0)  # Green=start, Red=end
        radius = line_width + 2
        for ox in range(-radius, radius + 1):
            for oy in range(-radius, radius + 1):
                if ox*ox + oy*oy <= radius*radius:
                    px, py = x + ox, y + oy
                    py_flipped = height - 1 - py
                    if 0 <= px < width and 0 <= py_flipped < height:
                        pixels[py_flipped, px, 0] = endpoint_color[0]
                        pixels[py_flipped, px, 1] = endpoint_color[1]
                        pixels[py_flipped, px, 2] = endpoint_color[2]
                        pixels[py_flipped, px, 3] = 1.0
    
    image.pixels[:] = pixels.flatten()
    image.update()
