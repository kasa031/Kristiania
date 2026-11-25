# Start lokal nettside for Oslo-historie (port 8080)
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
Write-Host "Kristiania (SPA): http://localhost:8080/home" -ForegroundColor Cyan
Write-Host "Kart: /kart  |  Gatur: /tur"
Write-Host "Oppgaveliste: http://localhost:8080/content/fremgang.html"
Write-Host "Avslutt med Ctrl+C"
python scripts/spa_server.py --port 8080