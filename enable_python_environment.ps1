
# 1. Check if any Python version is already installed
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonPath) {
    Write-Output "No Python installation found. Fetching latest Python version..."
    $latestInfo = Invoke-RestMethod -Uri "https://www.python.org/downloads/windows/" -UseBasicParsing
    $latestVersion = ($latestInfo -split 'Latest Python 3 Release - Python ')[1] -split '<' | Select-Object -First 1
    if (-not $latestVersion) {
        Write-Error "Could not determine latest Python version."
        exit 1
    }
    $installerUrl = "https://www.python.org/ftp/python/$latestVersion/python-$latestVersion-amd64.exe"
    $installerPath = "python-$latestVersion-amd64.exe"
    Write-Output "Downloading Python $latestVersion installer..."
    curl.exe -o $installerPath $installerUrl
    Write-Output "Installing Python $latestVersion..."
    Start-Process -Wait -FilePath .\$installerPath -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0"
    $pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
    if (-not $pythonPath) {
        Write-Error "Python was not installed correctly."
        exit 1
    }
    Write-Output "Removing Python installer..."
    Remove-Item -Force .\$installerPath
} else {
    Write-Output "Python is already installed at $pythonPath. Skipping download and installation."
}

# Python version check
$pythonVersion = & $pythonPath --version
Write-Output "Detected Python version: $pythonVersion"

# 2. Create virtual environment
Write-Output "Creating virtual environment 'venv'..."
& $pythonPath -m venv venv

# 3. Activate virtual environment
Write-Output "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# 4. Upgrade pip
Write-Output "Upgrading pip..."
.\venv\Scripts\python.exe -m pip install --upgrade pip

# 5. Install packages
Write-Output "Installing packages..."
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# 6. Confirmation
Write-Output "✅ Environment created and packages installed successfully!"
