# Start JoBSearchAntigravity Web GUI
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Starting JoBSearchAntigravity Web Application GUI      " -ForegroundColor Green
Write-Host "   URL: http://localhost:5000                             " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

Start-Process "http://localhost:5000"
python web\app.py
