@echo off
REM IndexTTS2 One-Click Startup Script for Windows
REM This script will install dependencies and launch the WebUI

setlocal enabledelayedexpansion

echo.
echo ================================================
echo     IndexTTS2 - One-Click Startup (Windows)
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if Git LFS is initialized
echo.
echo [INFO] Checking Git LFS setup...
git lfs version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Git LFS not found. Large files may not download correctly.
    echo Install Git LFS from https://git-lfs.com/
) else (
    echo [OK] Git LFS found
)

REM Check and pull Git LFS files
echo.
echo [INFO] Pulling Git LFS files...
git lfs pull

REM Install uv if not present
echo.
echo [INFO] Checking uv package manager...
where uv >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing uv package manager...
    pip install -U uv
    if errorlevel 1 (
        echo [ERROR] Failed to install uv
        echo Try running: pip install -U uv
        pause
        exit /b 1
    )
) else (
    echo [OK] uv found
)

REM Install dependencies
echo.
echo [INFO] Installing dependencies (this may take 5-10 minutes)...
echo [INFO] This downloads PyTorch, transformers, and other libraries...
call uv sync --all-extras
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo Try running manually: uv sync --all-extras
    pause
    exit /b 1
)

REM Check if models exist
echo.
echo [INFO] Checking for model files...
if not exist "checkpoints\config.yaml" (
    echo [WARNING] Model files not found!
    echo.
    echo [INFO] Downloading IndexTTS-2 models (requires internet, ~5GB)...
    echo [INFO] This may take 10-30 minutes depending on your connection...
    echo.
    
    call uv tool install "huggingface-hub[cli,hf_xet]"
    if errorlevel 1 (
        echo [WARNING] Failed to install huggingface-hub CLI
        echo Try downloading manually: https://huggingface.co/IndexTeam/IndexTTS-2
        echo.
    ) else (
        call hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
        if errorlevel 1 (
            echo [WARNING] Failed to download models
            echo Try using ModelScope instead: https://modelscope.cn/models/IndexTeam/IndexTTS-2
            echo.
        )
    )
) else (
    echo [OK] Model files found
)

REM Check GPU
echo.
echo [INFO] Checking GPU support...
call uv run tools\gpu_check.py
if errorlevel 1 (
    echo [WARNING] GPU check failed. System will use CPU (slower inference)
)

REM Launch WebUI
echo.
echo [INFO] Starting IndexTTS2 WebUI...
echo [INFO] Opening http://127.0.0.1:7860 in your browser...
echo.
echo Press Ctrl+C to stop the server
echo.

call uv run webui.py
pause
