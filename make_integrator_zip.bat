@echo off
setlocal

cd /d "%~dp0"

call build_integrator_pack.bat
if errorlevel 1 (
    echo Integrator pack build failed.
    exit /b 1
)

set "SRC=release\Sealink-Integrator-Pack"
if not exist "%SRC%\PLATFORM_INTEGRATOR_GUIDE.md" (
    echo Integrator pack not found in %SRC%
    exit /b 1
)

set "VER=0.0.0"
if exist "VERSION.txt" (
    set /p VER=<"VERSION.txt"
)

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmm"') do set "STAMP=%%I"
set "OUT=release\Sealink-Integrator-Pack-v%VER%-%STAMP%.zip"

if exist "%OUT%" del /f /q "%OUT%"

echo Creating %OUT% ...
powershell -NoProfile -Command "Compress-Archive -Path '%SRC%\*' -DestinationPath '%OUT%' -CompressionLevel Optimal"
if errorlevel 1 (
    echo Zip creation failed.
    exit /b 1
)

echo.
echo Zip created: %OUT%
exit /b 0
