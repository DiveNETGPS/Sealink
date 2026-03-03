@echo off
setlocal

cd /d "%~dp0"

set "SRC=release\Sealink-OEM"
if not exist "%SRC%\SealinkUtility.exe" (
    echo Release files not found in %SRC%
    echo Run build_release.bat.
    pause
    exit /b 1
)

set "VER=0.0.0"
if exist "VERSION.txt" (
    set /p VER=<"VERSION.txt"
)

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmm"') do set "STAMP=%%I"
set "OUT=release\Sealink-OEM-Utility-v%VER%-%STAMP%.zip"

if exist "%OUT%" del /f /q "%OUT%"

echo Creating %OUT% ...
powershell -NoProfile -Command "Compress-Archive -Path '%SRC%\*' -DestinationPath '%OUT%' -CompressionLevel Optimal"
if errorlevel 1 (
    echo Zip creation failed.
    pause
    exit /b 1
)

echo.
echo Zip created: %OUT%
exit /b 0
