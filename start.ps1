# IndexTTS2 One-Click Startup Script for Windows PowerShell
# This script will install dependencies and launch the WebUI

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  IndexTTS2 - One-Click Startup (Windows PS)" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Function to print colored output
function Print-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Print-OK {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Print-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Print-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

# Check if Python is installed
try {
    $pythonVersion = & python --version 2>&1
    Print-OK "Python found: $pythonVersion"
} catch {
    Print-Error "Python is not installed or not in PATH"
    Write-Host "Please install Python 3.10+ from https://www.python.org/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Git is installed
try {
    $gitVersion = & git --version 2>&1
    Print-OK "Git found: $gitVersion"
} catch {
    Print-Error "Git is not installed"
    Write-Host "Please install Git from https://git-scm.com/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Git LFS is installed
Write-Host ""
Print-Info "Checking Git LFS setup..."
try {
    $lfsVersion = & git lfs version 2>&1
    Print-OK "Git LFS found"
} catch {
    Print-Warning "Git LFS not found. Large files may not download correctly."
    Write-Host "Install Git LFS from https://git-lfs.com/"
}

# Pull Git LFS files
Write-Host ""
Print-Info "Pulling Git LFS files..."
& git lfs pull

# Install uv if not present
Write-Host ""
Print-Info "Checking uv package manager..."
try {
    $uvVersion = & uv --version 2>&1
    Print-OK "uv found: $uvVersion"
} catch {
    Print-Info "Installing uv package manager..."
    & pip install -U uv
    if ($LASTEXITCODE -ne 0) {
        Print-Error "Failed to install uv"
        Write-Host "Try running: pip install -U uv"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Install dependencies
Write-Host ""
Print-Info "Installing dependencies (this may take 5-10 minutes)..."
Print-Info "This downloads PyTorch, transformers, and other libraries..."
& uv sync --all-extras
if ($LASTEXITCODE -ne 0) {
    Print-Error "Failed to install dependencies"
    Write-Host "Try running manually: uv sync --all-extras"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if models exist
Write-Host ""
Print-Info "Checking for model files..."
if (-not (Test-Path "checkpoints\config.yaml")) {
    Print-Warning "Model files not found!"
    Write-Host ""
    Print-Info "Downloading IndexTTS-2 models (requires internet, ~5GB)..."
    Print-Info "This may take 10-30 minutes depending on your connection..."
    Write-Host ""
    
    try {
        & uv tool install "huggingface-hub[cli,hf_xet]"
        if ($LASTEXITCODE -eq 0) {
            & hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
            if ($LASTEXITCODE -eq 0) {
                Print-OK "Models downloaded successfully"
            } else {
                Print-Warning "Failed to download models from Hugging Face"
                Write-Host "Try downloading manually: https://huggingface.co/IndexTeam/IndexTTS-2"
                Write-Host "Or use ModelScope: https://modelscope.cn/models/IndexTeam/IndexTTS-2"
                Write-Host ""
            }
        }
    } catch {
        Print-Warning "Failed to install huggingface-hub CLI"
        Write-Host "Try downloading models manually from:"
        Write-Host "  https://huggingface.co/IndexTeam/IndexTTS-2"
        Write-Host ""
    }
} else {
    Print-OK "Model files found"
}

# Check GPU
Write-Host ""
Print-Info "Checking GPU support..."
& uv run tools\gpu_check.py
if ($LASTEXITCODE -ne 0) {
    Print-Warning "GPU check failed. System will use CPU (slower inference)"
}

# Launch WebUI
Write-Host ""
Print-Info "Starting IndexTTS2 WebUI..."
Print-Info "Opening http://127.0.0.1:7860 in your browser..."
Write-Host ""
Write-Host "Press Ctrl+C to stop the server"
Write-Host ""

& uv run webui.py
