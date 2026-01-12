# Novel View Generation with Hunyuan3D-2

This module generates 3D novel views from segmentation masks using Tencent's Hunyuan3D-2 model.

## Prerequisites

- **Python 3.11** (managed via uv)
- **CUDA Toolkit** (12.1 recommended, or 11.8)
- **uv** package manager: `powershell -c 'irm https://astral.sh/uv/install.ps1 | iex'`
- **~6GB GPU VRAM** for shape generation (16GB for full texture generation)

## Setup

### 1. Initialize the Hunyuan3D-2 Submodule

If you cloned the repository without submodules:

```powershell
git submodule update --init --recursive
```

### 2. Run the Setup Script

```powershell
cd procedural_human/novel_view_gen
.\setup_hunyuan3d.ps1
```

This will:
- Create a Python virtual environment at `Hunyuan3D-2/.venv`
- Install PyTorch with CUDA 12.1 support
- Install Hunyuan3D dependencies
- Build custom CUDA rasterizer extensions

### Setup Options

```powershell
# Use CUDA 11.8 instead
.\setup_hunyuan3d.ps1 -CudaVersion cu118

# Skip CUDA extension building (shape-only generation)
.\setup_hunyuan3d.ps1 -SkipExtensions

# Also download the mini-turbo model (~3GB)
.\setup_hunyuan3d.ps1 -DownloadModel

# CPU-only (no GPU required, slower)
.\setup_hunyuan3d.ps1 -CudaVersion cpu -SkipExtensions
```

## Usage

### Automatic (Blender Addon)

The addon automatically:
1. Detects the Hunyuan3D-2 installation in this directory
2. Starts the API server when Blender loads
3. Stops the server when Blender quits

No manual configuration needed if you followed the setup above.

### Manual Testing

```powershell
cd procedural_human/novel_view_gen/Hunyuan3D-2
.\.venv\Scripts\Activate.ps1
python api_server.py --host localhost --port 8082 --model_path tencent/Hunyuan3D-2mini --subfolder hunyuan3d-dit-v2-mini-turbo --enable_flashvdm --low_vram_mode
```

Then test with:
```powershell
curl http://localhost:8082/health
```

## Environment Variable (Alternative)

Instead of using the submodule, you can point to an external Hunyuan3D-2 installation:

```powershell
$env:HUNYUAN3D_PATH = "C:\path\to\Hunyuan3D-2"
```

The addon checks locations in this order:
1. Addon preferences (if configured)
2. `HUNYUAN3D_PATH` environment variable
3. This submodule (`procedural_human/novel_view_gen/Hunyuan3D-2`)
4. Common locations (`~/Hunyuan3D-2`, `C:/Hunyuan3D-2`)

## Troubleshooting

### "setuptools not found" when building extensions

Run the setup script again - it now installs setuptools automatically.

### CUDA extension build fails

- Ensure CUDA Toolkit is installed and `nvcc` is in PATH
- Try `.\setup_hunyuan3d.ps1 -SkipExtensions` (texture generation won't work, but shape generation will)

### Out of VRAM

The mini-turbo model with `--low_vram_mode` requires ~6GB. If you have less:
- Close other GPU applications
- Use CPU mode: `.\setup_hunyuan3d.ps1 -CudaVersion cpu`

### Server won't start

Check the Blender console for error messages. Common issues:
- Port 8082 already in use
- Missing CUDA drivers
- Model not downloaded (first run downloads ~3GB)
