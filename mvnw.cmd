@echo off
REM Lightweight mvnw shim: downloads Maven if missing and runs it.
setlocal
set MAVEN_DIR=%~dp0\.mvn\apache-maven
set MAVEN_BIN=%MAVEN_DIR%\bin\mvn.cmd
if exist "%MAVEN_BIN%" (
  "%MAVEN_BIN%" %*
  exit /b %ERRORLEVEL%
)

echo Maven not found locally. Downloading a portable Maven (~10-20MB)...
set MAVEN_VERSION=3.8.8
set MAVEN_ZIP=apache-maven-%MAVEN_VERSION%-bin.zip
set DOWNLOAD_URL=https://archive.apache.org/dist/maven/maven-3/%MAVEN_VERSION%/binaries/%MAVEN_ZIP%
set TMPZIP=%TEMP%\%MAVEN_ZIP%

powershell -NoProfile -Command "if (-Not (Test-Path '%TMPZIP%')) { Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%TMPZIP%' }"

if not exist "%TMPZIP%" (
  echo Failed to download Maven. Please install Maven manually and add to PATH.
  exit /b 1
)

powershell -NoProfile -Command "Expand-Archive -LiteralPath '%TMPZIP%' -DestinationPath '%~dp0\.mvn' -Force"

if exist "%MAVEN_BIN%" (
  "%MAVEN_BIN%" %*
  exit /b %ERRORLEVEL%
) else (
  echo Extraction failed or mvn not found. Please check permissions.
  exit /b 1
)
