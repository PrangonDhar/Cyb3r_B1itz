@echo off
title CYBER BLITZ

cd /d "%~dp0"

echo ==========================================
echo          CYBER BLITZ LAUNCHER
echo ==========================================
echo.
echo Starting Cyber BLITZ server...
echo.

python web\app.py

pause