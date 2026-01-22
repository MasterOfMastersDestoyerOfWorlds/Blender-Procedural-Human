$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Join-Path $ScriptDir ".\procedural_human" | Resolve-Path
$WheelsDir = Join-Path $ProjectDir "wheels"

Write-Host "Project dir: $ProjectDir"
Push-Location $ProjectDir

try {
if (-not (Test-Path "pyproject.toml")) {
    throw "pyproject.toml not found aborting."
}
$PyProjectContent = Get-Content "pyproject.toml" -Raw
if ($PyProjectContent -match 'requires-python\s*=\s*"[=~><]*(\d+\.\d+)') {
    $PythonVersion = $Matches[1]
    Write-Host "Target Python version from pyproject.toml: $PythonVersion"
} else {
    throw "Could not parse requires-python from pyproject.toml"
}
if (Test-Path $WheelsDir) {
    Write-Host "Cleaning wheels directory..."
    Remove-Item -Recurse -Force $WheelsDir
}
New-Item -ItemType Directory -Path $WheelsDir | Out-Null
Write-Host "Downloading wheels for Python $PythonVersion (Blender)..."
uv run --with pip --python $PythonVersion python -m pip download . `
    --dest $WheelsDir `
    --prefer-binary `
    --find-links https://download.pytorch.org/whl/cu118 `
$SourceFiles = Get-ChildItem -Path $WheelsDir | Where-Object { $_.Name -match '\.(zip|tar\.gz)$' }

foreach ($file in $SourceFiles) {
    if ($file.Name -match "xformers") {
        Write-Host "Skipping build/install for xformers source (requires compiler). Removing it."
        Remove-Item $file.FullName
        continue
    }

    Write-Host "Building wheel for $($file.Name)..."
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
$WheelFiles = Get-ChildItem -Path $WheelsDir | 
    Where-Object { $_.Name -match '\.(whl|zip|tar\.gz)$' } |
    Sort-Object Name |
    ForEach-Object { "    `"./wheels/$($_.Name)`"," }
$ManifestPath = Join-Path $ProjectDir "blender_manifest.toml"
$ManifestContent = Get-Content $ManifestPath -Raw
$WheelsList = $WheelFiles -join "`n"
$WheelsList = $WheelsList -replace ",`$", ""
$NewWheelsSection = "wheels = [`n$WheelsList`n]"
$Pattern = '(?s)wheels\s*=\s*\[.*?\]'
$ManifestContent = $ManifestContent -replace $Pattern, $NewWheelsSection
Set-Content -Path $ManifestPath -Value $ManifestContent -NoNewline

Write-Host "Updated blender_manifest.toml with $($WheelFiles.Count) wheels."
Write-Host "Done."

} finally {
    Pop-Location
}
