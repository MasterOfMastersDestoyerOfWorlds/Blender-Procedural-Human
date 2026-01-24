import numpy as np

def apply_ridge_curves_overlay(image, curves, color=(0.0, 1.0, 0.0), line_width=2):
    """
    Apply ridge curves overlay onto a Blender image.
    """
    if not curves:
        return
        
    width, height = image.size
    pixels = np.array(image.pixels[:]).reshape(height, width, 4)
    for curve in curves:
        if len(curve) < 2:
            continue
            
        for i in range(len(curve) - 1):
            x0, y0 = curve[i]
            x1, y1 = curve[i+1]
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            steps = max(int(max(dx, dy)), 1)
            
            for t in range(steps + 1):
                frac = t / steps if steps > 0 else 0
                x = int(x0 + frac * (x1 - x0))
                y = int(y0 + frac * (y1 - y0))
                for ox in range(-line_width//2, line_width//2 + 1):
                    for oy in range(-line_width//2, line_width//2 + 1):
                        px, py = x + ox, y + oy
                        py_flipped = height - 1 - py
                        if 0 <= px < width and 0 <= py_flipped < height:
                            pixels[py_flipped, px, 0] = color[0]
                            pixels[py_flipped, px, 1] = color[1]
                            pixels[py_flipped, px, 2] = color[2]
                            pixels[py_flipped, px, 3] = 1.0
                            
    image.pixels[:] = pixels.flatten()
    image.update()