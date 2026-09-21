@echo off
title CYBER BLITZ

cd /d "%~dp0"

echo Starting CYBER BLITZ...
echo.

start "" python web\app.py

timeout /t 3 /nobreak >nul

start "" "http://127.0.0.1:5000"

exit