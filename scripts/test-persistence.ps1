$ErrorActionPreference = 'Stop'
Push-Location (Join-Path $PSScriptRoot '..')
try {
    $baseUrl = if ($env:API_BASE_URL) { $env:API_BASE_URL } else { 'http://localhost:8000' }
    $body = @{ cliente = 'Teste persistencia'; produto = 'Mouse'; quantidade = 3; valor_unitario = 19.90 } | ConvertTo-Json
    $pedido = Invoke-RestMethod "$baseUrl/pedidos" -Method Post -ContentType 'application/json' -Body $body
    docker compose restart pedidos
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao reiniciar a API' }
    $ready = $false
    for ($attempt = 0; $attempt -lt 30; $attempt++) {
        try {
            $health = Invoke-RestMethod "$baseUrl/health" -TimeoutSec 5
            if ($health.status -eq 'ok') { $ready = $true; break }
        } catch { }
        Start-Sleep -Seconds 2
    }
    if (-not $ready) { throw 'API indisponivel apos reinicio' }
    $salvo = Invoke-RestMethod "$baseUrl/pedidos/$($pedido.id)"
    foreach ($field in @('id', 'cliente', 'produto', 'quantidade', 'valor_unitario', 'valor_total', 'status', 'data_criacao')) {
        if ($salvo.$field -ne $pedido.$field) { throw "Campo diferente apos reinicio: $field" }
    }
    Write-Output "PASS: pedido $($pedido.id) preservado integralmente apos reiniciar a API."
    $salvo | ConvertTo-Json
} finally {
    Pop-Location
}
