# Force delete a log file by closing any processes that have it open

param(
    [string]$LogPath = "logs/d1ff74007a904fba8fcb4dc83e3e90e0/0.raw.log"
)

Write-Host "Attempting to delete: $LogPath" -ForegroundColor Yellow

# Try normal delete first
try {
    Remove-Item -Path $LogPath -Force -ErrorAction Stop
    Write-Host "File deleted successfully!" -ForegroundColor Green
    exit 0
} catch {
    Write-Host "File is locked. Checking for processes..." -ForegroundColor Yellow
    
    # Find processes that might be using Python/bash
    $pythonProcs = Get-Process python -ErrorAction SilentlyContinue
    $bashProcs = Get-Process bash -ErrorAction SilentlyContinue
    
    if ($pythonProcs) {
        Write-Host "Found Python processes. You may need to stop:" -ForegroundColor Yellow
        foreach ($proc in $pythonProcs) {
            Write-Host "  PID: $($proc.Id) - $($proc.ProcessName)" -ForegroundColor Cyan
        }
        Write-Host ""
        Write-Host "To stop all Python processes, run:" -ForegroundColor Yellow
        Write-Host "  Stop-Process -Name python -Force" -ForegroundColor Cyan
    }
    
    # Alternative: Try to delete after a short wait
    Write-Host ""
    Write-Host "Waiting 2 seconds and retrying..." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    
    try {
        Remove-Item -Path $LogPath -Force -ErrorAction Stop
        Write-Host "File deleted successfully after wait!" -ForegroundColor Green
    } catch {
        Write-Host "Still locked. The file is likely being written to by gpu_submit.sh" -ForegroundColor Red
        Write-Host ""
        Write-Host "Options:" -ForegroundColor Yellow
        Write-Host "1. Stop gpu_submit.sh if it's running" -ForegroundColor Cyan
        Write-Host "2. Stop the Fairy Debugger server if it's running" -ForegroundColor Cyan
        Write-Host "3. Manually close the file in your editor" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Or you can just leave it - the script will overwrite it on next run" -ForegroundColor Green
    }
}

