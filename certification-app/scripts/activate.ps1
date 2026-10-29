$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $projectRoot '.venv'
$activateScript = Join-Path $venvPath 'Scripts\Activate.ps1'

if (-not (Test-Path $activateScript)) {
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        throw 'Failed to create the virtual environment.'
    }
}

. $activateScript
