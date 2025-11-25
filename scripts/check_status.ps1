# check job status, need job id and token

param(
    [Parameter(Mandatory=$true)]
    [string]$JobId,
    
    [string]$Token = $env:TOKEN
)

$SERVER_URL = "https://ceriferous-hoelike-jeffie.ngrok-free.dev"

if (-not $Token) {
    Write-Host "error: need token. set TOKEN env var or pass -Token" -ForegroundColor Red
    exit 1
}

$headers = @{
    "Authorization" = "Bearer $Token"
}

$response = Invoke-RestMethod -Uri "$SERVER_URL/api/status/$JobId" -Headers $headers -Method Get
$response | ConvertTo-Json -Depth 10 | Write-Host
