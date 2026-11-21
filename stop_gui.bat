@echo off
echo ==========================================================
echo    Stopping JoBSearchAntigravity Web GUI
echo ==========================================================

set FOUND=0
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    echo Found process listening on port 5000 with PID: %%a
    taskkill /f /pid %%a >nul 2>&1
    set FOUND=1
)

if "%FOUND%"=="1" (
    echo JoBSearchAntigravity Web GUI stopped successfully.
) else (
    echo No process was found running on port 5000. It is already free.
)

echo ==========================================================
pause
