<#
.SYNOPSIS
    Setup script for Hunyuan3D-2 submodule.

.DESCRIPTION
    This script sets up the Hunyuan3D-2 environment:
    - Creates a Python virtual environment
    - Installs PyTorch with CUDA support
    - Installs Hunyuan3D dependencies
    - Builds custom CUDA rasterizer extensions
    - Optionally downloads the mini-turbo model

.PARAMETER CudaVersion
    CUDA version for PyTorch. Default: cu121 (CUDA 12.1)
    Options: cu118, cu121, cu124, cpu

.PARAMETER SkipExtensions
    Skip building custom CUDA extensions (useful if you only need shape generation)

.PARAMETER DownloadModel
    Download the Hunyuan3D-2mini turbo model after setup

.EXAMPLE
    .\setup_hunyuan3d.ps1
    
.EXAMPLE
    .\setup_hunyuan3d.ps1 -CudaVersion cu118 -DownloadModel

param(
    [ValidateSet("cu118", "cu121", "cu124", "cpu")]
    [string]$CudaVersion = "cu121",
    
    [switch]$SkipExtensions,
    
    [switch]$DownloadModel
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Hunyuan3DDir = Join-Path $ScriptDir "Hunyuan3D-2"
$VenvDir = Join-Path $Hunyuan3DDir ".venv"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Hunyuan3D-2 Setup Script" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
if (-not (Test-Path (Join-Path $Hunyuan3DDir "api_server.py"))) {
    Write-Host "ERROR: Hunyuan3D-2 submodule not found at $Hunyuan3DDir" -ForegroundColor Red
    Write-Host "Run: git submodule update --init" -ForegroundColor Yellow
    exit 1
}
$uvPath = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvPath) {
    Write-Host "ERROR: 'uv' is not installed." -ForegroundColor Red
    Write-Host "Install it with: powershell -c 'irm https://astral.sh/uv/install.ps1 | iex'" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] uv found: $($uvPath.Source)" -ForegroundColor Green
if ($CudaVersion -ne "cpu") {
    $nvccPath = Get-Command nvcc -ErrorAction SilentlyContinue
    if (-not $nvccPath) {
        Write-Host "[WARN] CUDA compiler (nvcc) not found in PATH." -ForegroundColor Yellow
        Write-Host "       Building custom extensions may fail." -ForegroundColor Yellow
        Write-Host "       Make sure CUDA Toolkit is installed and in PATH." -ForegroundColor Yellow
    } else {
        Write-Host "[OK] CUDA found: $($nvccPath.Source)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  - Hunyuan3D directory: $Hunyuan3DDir"
Write-Host "  - Virtual environment: $VenvDir"
Write-Host "  - CUDA version: $CudaVersion"
Write-Host "  - Build extensions: $(-not $SkipExtensions)"
Write-Host "  - Download model: $DownloadModel"
Write-Host ""
Write-Host "Step 1: Creating virtual environment..." -ForegroundColor Cyan
Push-Location $Hunyuan3DDir
try {
    if (Test-Path $VenvDir) {
        Write-Host "  Virtual environment already exists, skipping creation." -ForegroundColor Yellow
    } else {
        uv venv --python 3.11 .venv
        if ($LASTEXITCODE -ne 0) { throw "Failed to create virtual environment" }
        Write-Host "  [OK] Virtual environment created" -ForegroundColor Green
    }
    $activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
    if (-not (Test-Path $activateScript)) {
        throw "Activation script not found: $activateScript"
    }
    . $activateScript
    Write-Host "  [OK] Virtual environment activated" -ForegroundColor Green
    Write-Host ""
    Write-Host "Step 2: Installing PyTorch with $CudaVersion..." -ForegroundColor Cyan
    if ($CudaVersion -eq "cpu") {
        uv pip install torch torchvision torchaudio
    } else {
        uv pip install torch torchvision torchaudio --index-url "https://download.pytorch.org/whl/$CudaVersion"
    }
    if ($LASTEXITCODE -ne 0) { throw "Failed to install PyTorch" }
    Write-Host "  [OK] PyTorch installed" -ForegroundColor Green
    Write-Host ""
    Write-Host "Step 3: Installing Hunyuan3D requirements..." -ForegroundColor Cyan
    uv pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw "Failed to install requirements" }
    Write-Host "  [OK] Requirements installed" -ForegroundColor Green
    Write-Host ""
    Write-Host "Step 4: Installing Hunyuan3D package..." -ForegroundColor Cyan
    uv pip install -e .
    if ($LASTEXITCODE -ne 0) { throw "Failed to install package" }
    Write-Host "  [OK] Package installed" -ForegroundColor Green
    if (-not $SkipExtensions) {
        Write-Host ""
        Write-Host "Step 5: Building custom CUDA extensions..." -ForegroundColor Cyan
        Write-Host "  Installing build dependencies (setuptools, wheel)..." -ForegroundColor Gray
        uv pip install setuptools wheel
        if ($LASTEXITCODE -ne 0) { 
            Write-Host "  [WARN] Failed to install setuptools" -ForegroundColor Yellow
        }
        $rasterizerDir = Join-Path $Hunyuan3DDir "hy3dgen\texgen\custom_rasterizer"
        if (Test-Path $rasterizerDir) {
            Write-Host "  Building custom_rasterizer..." -ForegroundColor Gray
            Push-Location $rasterizerDir
            try {
                python setup.py install
                if ($LASTEXITCODE -ne 0) { 
                    Write-Host "  [WARN] Failed to build custom_rasterizer" -ForegroundColor Yellow
                } else {
                    Write-Host "  [OK] custom_rasterizer built" -ForegroundColor Green
                }
            } finally {
                Pop-Location
            }
        }
        $rendererDir = Join-Path $Hunyuan3DDir "hy3dgen\texgen\differentiable_renderer"
        if (Test-Path $rendererDir) {
            Write-Host "  Building differentiable_renderer..." -ForegroundColor Gray
            Push-Location $rendererDir
            try {
                python setup.py install
                if ($LASTEXITCODE -ne 0) { 
                    Write-Host "  [WARN] Failed to build differentiable_renderer" -ForegroundColor Yellow
                } else {
                    Write-Host "  [OK] differentiable_renderer built" -ForegroundColor Green
                }
            } finally {
                Pop-Location
            }
        }
    } else {
        Write-Host ""
        Write-Host "Step 5: Skipping custom CUDA extensions (--SkipExtensions)" -ForegroundColor Yellow
    }
    if ($DownloadModel) {
        Write-Host ""
        Write-Host "Step 6: Downloading Hunyuan3D-2mini turbo model..." -ForegroundColor Cyan
        Write-Host "  This may take a while (several GB)..." -ForegroundColor Gray
        python -c "from huggingface_hub import snapshot_download; snapshot_download('tencent/Hunyuan3D-2mini', allow_patterns=['hunyuan3d-dit-v2-mini-turbo/*'])"
        if ($LASTEXITCODE -ne 0) { 
            Write-Host "  [WARN] Failed to download model" -ForegroundColor Yellow
        } else {
            Write-Host "  [OK] Model downloaded" -ForegroundColor Green
        }
    }

    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  Setup Complete!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "To use Hunyuan3D with Blender:" -ForegroundColor Cyan
    Write-Host "  1. The addon will auto-detect this installation"
    Write-Host "  2. Or set: `$env:HUNYUAN3D_PATH = '$Hunyuan3DDir'"
    Write-Host ""
    Write-Host "To test manually:" -ForegroundColor Cyan
    Write-Host "  cd $Hunyuan3DDir"
    Write-Host "  .\.venv\Scripts\Activate.ps1"
    Write-Host "  python api_server.py --host localhost --port 8082"
    Write-Host ""

} finally {
    Pop-Location
}
