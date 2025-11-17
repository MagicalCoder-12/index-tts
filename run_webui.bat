@echo off
REM Voice Cloner WebUI Launcher
REM This script activates the virtual environment and runs the WebUI

REM Change to the directory where this script is located
cd /d "%~dp0"

REM Activate the virtual environment
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo Error: Virtual environment not found at .venv\Scripts\activate.bat
    pause
    exit /b 1
)

echo.
echo ============================================
echo Voice Cloner WebUI Launcher
echo ============================================
echo.
echo Starting Voice Cloner WebUI...
echo If this is the first run, dependencies will be installed.
echo The WebUI will be available at: http://localhost:7860
echo.

REM Allow specifying a custom port via command line argument
if not "%1"==" " (
    set PORT=%1
    echo Custom port specified: %PORT%
    set GRADIO_SERVER_PORT=%PORT%
) else (
    set GRADIO_SERVER_PORT=7860
)

python webui.py

pause
