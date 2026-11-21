# PowerShell Daily Runner for JoBSearchAntigravity
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BaseDir = Split-Path -Parent $ScriptDir
$PipelineScript = Join-Path $BaseDir "scripts\run_pipeline.py"

Write-Host "Starting JoBSearchAntigravity overnight run..." -ForegroundColor Cyan
python "$PipelineScript"
Write-Host "Overnight run finished. Check tracker/tracker.md for drafted applications." -ForegroundColor Green
