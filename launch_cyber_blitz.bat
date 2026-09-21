@echo off

cd /d "%~dp0"


echo ==========================================
echo          CYBER BLITZ LAUNCHER
echo ==========================================
echo.
echo Starting Cyber BLITZ server...
echo.


start "" "C:\Users\YourName\AppData\Local\Programs\Python\Python313\python.exe" web\app.py

timeout /t 3 /nobreak >nul

start "" http://127.0.0.1:5000

exit