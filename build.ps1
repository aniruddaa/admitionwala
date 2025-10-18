Param(
  [string]$PomPath = "C:\Users\hp\Desktop\New folder (3)\pom.xml"
)

Write-Host "Running mvnw wrapper to build project (pom: $PomPath)"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$mvnw = Join-Path $scriptDir 'mvnw.cmd'

if (-Not (Test-Path $mvnw)) {
  Write-Error "mvnw.cmd not found in $scriptDir"
  exit 1
}

Push-Location $scriptDir
try {
  Write-Host "Changing directory to $scriptDir and running mvnw.cmd"
  & .\mvnw.cmd clean package -DskipTests
} finally {
  Pop-Location
}