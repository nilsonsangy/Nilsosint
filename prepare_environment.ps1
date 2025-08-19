# Prepare Environment Script for Nilsosint
# This script will:
# - Check/install Python
# - Create/activate venv
# - Install requirements.txt
# - Download spaCy en_core_web_sm model
# - Check/install ffmpeg (Windows only)

$ErrorActionPreference = 'Stop'

# 1. Check if Python is installed
$pythonCmd = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonCmd) {
    Write-Output "Python not found. Installing latest Python..."
    $latestInfo = Invoke-RestMethod -Uri "https://www.python.org/downloads/windows/" -UseBasicParsing
    $latestVersion = ($latestInfo -split 'Latest Python 3 Release - Python ')[1] -split '<' | Select-Object -First 1
    if (-not $latestVersion) {
        Write-Error "Could not determine latest Python version."
        exit 1
    }
    $installerUrl = "https://www.python.org/ftp/python/$latestVersion/python-$latestVersion-amd64.exe"
    $installerPath = "python-$latestVersion-amd64.exe"
    curl.exe -o $installerPath $installerUrl
    Start-Process -Wait -FilePath .\$installerPath -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0"
    $pythonCmd = (Get-Command python -ErrorAction SilentlyContinue).Source
    if (-not $pythonCmd) {
        Write-Error "Python was not installed correctly."
        exit 1
    }
    Remove-Item -Force .\$installerPath
    Write-Output "Python installed successfully."
} else {
    Write-Output "Python found at $pythonCmd."
}


# 2. Create .venv if not exists
if (-not (Test-Path ".venv")) {
    Write-Output "Creating virtual environment in .venv..."
    & $pythonCmd -m venv .venv
}

# 3. Activate .venv
Write-Output "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1

# 4. Upgrade pip (before anything else)
Write-Output "Upgrading pip..."
python -m pip install --upgrade pip


# 5. Install requirements
Write-Output "Installing requirements..."
pip install -r requirements.txt


# 6. Download spaCy English model only if not present
Write-Output "Checking for spaCy en_core_web_sm model..."
$spacyCheck = python -c "import spacy; spacy.load('en_core_web_sm')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Output "Model not found. Downloading spaCy en_core_web_sm model..."
    python -m spacy download en_core_web_sm
} else {
    Write-Output "spaCy en_core_web_sm model already installed."
}

# 7. Check/install ffmpeg (Windows only)
if ($env:OS -eq "Windows_NT") {
    $ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
    if (-not $ffmpeg) {
        Write-Output "ffmpeg not found. Downloading and installing ffmpeg..."
    $ffmpegZipUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    $ffmpegZip = "ffmpeg.zip"
    curl.exe -L -o $ffmpegZip $ffmpegZipUrl
    $ffmpegDir = "ffmpeg-bin"
    Expand-Archive -Path $ffmpegZip -DestinationPath $ffmpegDir -Force
    $binPath = Get-ChildItem -Path $ffmpegDir -Recurse -Filter ffmpeg.exe | Select-Object -First 1 | Split-Path
    $destPath = "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps"
    Copy-Item "$binPath\ffmpeg.exe" $destPath -Force
    # Clean up ffmpeg files
    Remove-Item $ffmpegZip -Force
    Remove-Item -Recurse -Force $ffmpegDir
    Write-Output "ffmpeg installed to $destPath and temporary files cleaned up."
    } else {
        Write-Output "ffmpeg found."
    }
}

Write-Output "Environment setup complete!"
