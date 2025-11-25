# grab results for a job, saves to results folder

param(
    [Parameter(Mandatory=$true)]
    [string]$JobId,
    
    [string]$Token = $env:TOKEN
)

$SERVER_URL = "https://ceriferous-hoelike-jeffie.ngrok-free.dev"
$RESULTS_DIR = "..\results"

if (-not $Token) {
    Write-Host "error: need token. set TOKEN env var or pass -Token" -ForegroundColor Red
    exit 1
}

Write-Host "fetching results for job $JobId..." -ForegroundColor Green

$headers = @{
    "Authorization" = "Bearer $Token"
}

$response = Invoke-RestMethod -Uri "$SERVER_URL/api/results/$JobId" -Headers $headers -Method Get
$response.stdout | Out-File -FilePath "$RESULTS_DIR\results_${JobId}.jsonl" -Encoding utf8

Write-Host "saved to $RESULTS_DIR\results_${JobId}.jsonl" -ForegroundColor Green
Get-Content "$RESULTS_DIR\results_${JobId}.jsonl" -TotalCount 5
