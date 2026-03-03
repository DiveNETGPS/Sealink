@echo off
setlocal

cd /d "%~dp0"

echo ========================================
echo Building Windows customer release zip...
echo ========================================
call build_release.bat
if errorlevel 1 (
    echo Windows release build failed.
    exit /b 1
)

call make_release_zip.bat
if errorlevel 1 (
    echo Windows release zip creation failed.
    exit /b 1
)

echo ========================================
echo Building integrator release zip...
echo ========================================
call make_integrator_zip.bat
if errorlevel 1 (
    echo Integrator release zip creation failed.
    exit /b 1
)

echo.
echo All release packages created successfully.
echo Output folder: release
echo.
exit /b 0
