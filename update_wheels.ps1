# Fail immediately on error
$ErrorActionPreference = "Stop"

# Resolve project root (directory containing this script)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Path to procedural_human directory
$ProjectDir = Join-Path $ScriptDir ".\procedural_human" | Resolve-Path

# Wheels directory
$WheelsDir = Join-Path $ProjectDir "wheels"

Write-Host "Project dir: $ProjectDir"

# Change working directory (temporarily)
Push-Location $ProjectDir

try {

# Safety check
if (-not (Test-Path "pyproject.toml")) {
    throw "pyproject.toml not found aborting."
}

# Extract Python version from pyproject.toml (single source of truth)
$PyProjectContent = Get-Content "pyproject.toml" -Raw
if ($PyProjectContent -match 'requires-python\s*=\s*"[=~><]*(\d+\.\d+)') {
    $PythonVersion = $Matches[1]
    Write-Host "Target Python version from pyproject.toml: $PythonVersion"
} else {
    throw "Could not parse requires-python from pyproject.toml"
}

# Clean wheels directory
if (Test-Path $WheelsDir) {
    Write-Host "Cleaning wheels directory..."
    Remove-Item -Recurse -Force $WheelsDir
}

# Recreate wheels directory
New-Item -ItemType Directory -Path $WheelsDir | Out-Null

# Download wheels (allow source if needed)
Write-Host "Downloading wheels for Python $PythonVersion (Blender)..."
uv run --with pip --python $PythonVersion python -m pip download . `
    --dest $WheelsDir `
    --prefer-binary `
    --find-links https://download.pytorch.org/whl/cu118 `

# Attempt to build wheels for any source distributions (zip/tar.gz) found
# This avoids shipping source distributions that require compilation on the user's machine
$SourceFiles = Get-ChildItem -Path $WheelsDir | Where-Object { $_.Name -match '\.(zip|tar\.gz)$' }

foreach ($file in $SourceFiles) {
    if ($file.Name -match "xformers") {
        Write-Host "Skipping build/install for xformers source (requires compiler). Removing it."
        Remove-Item $file.FullName
        continue
    }

    Write-Host "Building wheel for $($file.Name)..."
    # Build wheel using the downloaded wheels as links for build dependencies
    uv run --with pip --python $PythonVersion python -m pip wheel "$($file.FullName)" `
        --wheel-dir "$WheelsDir" `
        --no-deps `
        --no-cache-dir `
        --find-links "$WheelsDir"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Successfully built wheel. Removing source file."
        Remove-Item $file.FullName
    } else {
        Write-Warning "Failed to build wheel for $($file.Name). User might face installation issues."
    }
}

Remove-Item -Path "$WheelsDir\numpy*" -Recurse -Force
    
Write-Host "Updating blender_manifest.toml with wheel list..."

# Get all wheel files and format as TOML array entries
$WheelFiles = Get-ChildItem -Path $WheelsDir | 
    Where-Object { $_.Name -match '\.(whl|zip|tar\.gz)$' } |
    Sort-Object Name |
    ForEach-Object { "    `"./wheels/$($_.Name)`"," }

# Read the manifest file
$ManifestPath = Join-Path $ProjectDir "blender_manifest.toml"
$ManifestContent = Get-Content $ManifestPath -Raw

# Build the new wheels section
$WheelsList = $WheelFiles -join "`n"
# Remove trailing comma from last entry
$WheelsList = $WheelsList -replace ",`$", ""
$NewWheelsSection = "wheels = [`n$WheelsList`n]"

# Replace the wheels array in the manifest using regex
# This matches from 'wheels = [' to the closing ']' (handling multiline)
$Pattern = '(?s)wheels\s*=\s*\[.*?\]'
$ManifestContent = $ManifestContent -replace $Pattern, $NewWheelsSection

# Write the updated manifest
Set-Content -Path $ManifestPath -Value $ManifestContent -NoNewline

Write-Host "Updated blender_manifest.toml with $($WheelFiles.Count) wheels."
Write-Host "Done."

} finally {
    # Restore original directory
    Pop-Location
}
