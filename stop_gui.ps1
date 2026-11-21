# Stop JoBSearchAntigravity Web GUI
$conn = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue
if ($conn) {
    foreach ($c in $conn) {
        $pId = $c.OwningProcess
        Stop-Process -Id $pId -Force -ErrorAction SilentlyContinue
        Write-Host "Killed process on port 5000 (PID: $pId)" -ForegroundColor Green
    }
    Write-Host "JoBSearchAntigravity Web GUI stopped." -ForegroundColor Green
} else {
    Write-Host "No process was running on port 5000. Port is free." -ForegroundColor Yellow
}
