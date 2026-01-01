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

# Download wheels only (for Blender's Python)
Write-Host "Downloading wheels for Python $PythonVersion (Blender)..."
uv tool run pip download . `
    --dest $WheelsDir `
    --only-binary=:all: `
    --python-version $PythonVersion `

Remove-Item -Path "$WheelsDir\numpy*" -Recurse -Force
    
Write-Host "Updating blender_manifest.toml with wheel list..."

# Get all wheel files and format as TOML array entries
$WheelFiles = Get-ChildItem -Path $WheelsDir -Filter "*.whl" | 
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
