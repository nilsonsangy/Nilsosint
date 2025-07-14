# 1. Check if Python 3.11 is already installed
$python311Path = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
if (Test-Path $python311Path) {
    Write-Output "Python 3.11 is already installed at $python311Path. Skipping download and installation."
    $pythonPath = $python311Path
} else {
    Write-Output "Python 3.11 not found. Downloading Python 3.11 installer..."
    $installerUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
    $installerPath = "python-3.11.0-amd64.exe"
    curl.exe -o $installerPath $installerUrl
    Write-Output "Installing Python 3.11..."
    Start-Process -Wait -FilePath .\$installerPath -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0"
    if (!(Test-Path $python311Path)) {
        Write-Error "Python 3.11 was not installed correctly."
        exit 1
    }
    Write-Output "Removing Python installer..."
    Remove-Item -Force .\$installerPath
    $pythonPath = $python311Path
}

# Python version check and instructions for snscrape compatibility
$pythonVersion = & $pythonPath --version
Write-Output "Detected Python version: $pythonVersion"
if ($pythonVersion -match "Python 3\.(1[2-9]|[4-9][0-9])") {
    Write-Output "ERROR: snscrape does not support Python 3.12 or newer. Please install Python 3.11 or earlier."
    Write-Output "Download Python 3.11 from https://www.python.org/downloads/release/python-3110/"
    exit 1
}

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
