# Åpne siste app i standard nettleser (server må kjøre: .\scripts\serve.ps1)
$root = Split-Path -Parent $PSScriptRoot
$bust = Get-Content -Raw (Join-Path $root "sw.js") | Select-String -Pattern 'oslo-historie-v(\d+)' | ForEach-Object { $_.Matches[0].Groups[1].Value }
$url = "http://localhost:8080/index.html?v=$bust"
Write-Host "Åpner $url" -ForegroundColor Cyan
Start-Process $url