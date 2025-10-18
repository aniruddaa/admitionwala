param(
    [int]$Port = 5500
)

Write-Host "Serving ./frontend on http://localhost:$Port/ (Ctrl-C to stop)"

$root = (Resolve-Path .\frontend).ProviderPath
if (-not (Test-Path $root)) { Write-Error "frontend directory not found at $root"; exit 1 }

$listener = New-Object System.Net.HttpListener
 $prefix = "http://localhost:$Port/"
try {
    $listener.Prefixes.Add($prefix)
    $listener.Start()
} catch {
    Write-Error "Failed to start HttpListener on $prefix. Try running PowerShell as Administrator or choose another port."; exit 1
}

function Get-ContentType($ext){
    switch ($ext.ToLower()){
        '.html' { 'text/html' }
        '.css'  { 'text/css' }
        '.js'   { 'application/javascript' }
        '.json' { 'application/json' }
        '.png'  { 'image/png' }
        '.jpg'  { 'image/jpeg' }
        '.jpeg' { 'image/jpeg' }
        '.svg'  { 'image/svg+xml' }
        default { 'application/octet-stream' }
    }
}

try {
    while ($true) {
        $ctx = $listener.GetContext()
        Start-Job -ScriptBlock {
            param($ctx, $root)
            try {
                $req = $ctx.Request
                $resp = $ctx.Response
                $urlPath = $req.Url.AbsolutePath.TrimStart('/')
                if ([string]::IsNullOrWhiteSpace($urlPath)) { $urlPath = 'index.html' }
                $filePath = Join-Path $root ($urlPath -replace '/','\')
                if (-not (Test-Path $filePath)){
                    $resp.StatusCode = 404
                    $buf = [System.Text.Encoding]::UTF8.GetBytes('Not found')
                    $resp.ContentLength64 = $buf.Length
                    $resp.OutputStream.Write($buf,0,$buf.Length)
                    $resp.Close()
                    return
                }
                $bytes = [System.IO.File]::ReadAllBytes($filePath)
                $ext = [System.IO.Path]::GetExtension($filePath)
                $resp.ContentType = Get-ContentType $ext
                $resp.ContentLength64 = $bytes.Length
                $resp.OutputStream.Write($bytes,0,$bytes.Length)
                $resp.Close()
            } catch {
                try { $ctx.Response.StatusCode = 500; $buf = [System.Text.Encoding]::UTF8.GetBytes('Server error'); $ctx.Response.OutputStream.Write($buf,0,$buf.Length); $ctx.Response.Close() } catch {}
            }
        } -ArgumentList $ctx, $root | Out-Null
    }
} finally {
    $listener.Stop()
    $listener.Close()
}
