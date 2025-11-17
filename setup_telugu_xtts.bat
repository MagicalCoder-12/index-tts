@echo off
echo ============================================================
echo Installing Coqui TTS for Telugu Voice Cloning
echo ============================================================
echo.

echo Installing TTS library...
uv pip install TTS
if %errorlevel% neq 0 (
    echo ERROR: Installation failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo To generate Telugu speech with voice cloning:
echo   uv run python telugu_tts_xtts.py --text "మీ తెలుగు వచనం" --reference your_voice.wav
echo.
echo For examples:
echo   uv run python telugu_tts_xtts.py --batch
echo.
pause
