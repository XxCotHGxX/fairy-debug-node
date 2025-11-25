
# helper to submit jobs, pretty simple

$SERVER_URL = "https://ceriferous-hoelike-jeffie.ngrok-free.dev"
$SUBMISSIONS_DIR = "..\submissions"

# check config exists
if (-not (Test-Path "$SUBMISSIONS_DIR\config.yaml")) {
    Write-Host "error: config.yaml missing in $SUBMISSIONS_DIR" -ForegroundColor Red
    exit 1
}

# check solution exists
if (-not (Test-Path "$SUBMISSIONS_DIR\solution.py")) {
    Write-Host "error: solution.py missing in $SUBMISSIONS_DIR" -ForegroundColor Red
    exit 1
}

# submit it (async by default)
Write-Host "submitting..." -ForegroundColor Green
Push-Location $SUBMISSIONS_DIR

$response = curl.exe -X POST "$SERVER_URL/api/submit?wait=false" `
  -F "code=@solution.py" `
  -F "config_file=@config.yaml"

$response | Out-File -FilePath "..\results\last_submission.json" -Encoding utf8
$response | ConvertFrom-Json | Select-Object job_id, status, node_id | Format-List

Pop-Location
Write-Host "`ndone! check results\last_submission.json for job_id" -ForegroundColor Green
