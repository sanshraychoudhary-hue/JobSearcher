@echo off
cd /d "%~dp0"
echo ==========================================================
echo    Starting JoBSearchAntigravity Web GUI
echo    Opening http://localhost:5000 in your browser...
echo ==========================================================
start http://localhost:5000
python web\app.py
pause
