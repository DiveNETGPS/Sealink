@echo off
setlocal

cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" (
    echo Missing .venv\Scripts\python.exe
    echo Create virtual environment and install requirements.
    pause
    exit /b 1
)

if not exist "product\resources\sealink_gui.py" (
    echo Missing GUI script: product\resources\sealink_gui.py
    pause
    exit /b 1
)

if not exist "test_listener.py" (
    echo Missing listener script: test_listener.py
    pause
    exit /b 1
)

echo Installing Python dependencies...
"%PY%" -m pip install -r "product\resources\requirements.txt"
if errorlevel 1 goto :fail

"%PY%" -m pip install --upgrade pyinstaller
if errorlevel 1 goto :fail

echo Cleaning artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist release rmdir /s /q release

echo Building GUI executable...
"%PY%" -m PyInstaller --noconfirm --clean --onefile --windowed --name SealinkGUI "product\resources\sealink_gui.py"
if errorlevel 1 goto :fail

echo Building listener executable...
"%PY%" -m PyInstaller --noconfirm --clean --onefile --name SealinkListener "test_listener.py"
if errorlevel 1 goto :fail

echo Creating release folder...
mkdir "release\Sealink-OEM"
copy /y "dist\SealinkGUI.exe" "release\Sealink-OEM\SealinkGUI.exe" >nul
copy /y "dist\SealinkListener.exe" "release\Sealink-OEM\SealinkListener.exe" >nul
copy /y "release_assets\run_gui.bat" "release\Sealink-OEM\run_gui.bat" >nul
copy /y "release_assets\run_listener.bat" "release\Sealink-OEM\run_listener.bat" >nul
copy /y "release_assets\run_all.bat" "release\Sealink-OEM\run_all.bat" >nul
copy /y "release_assets\README_CUSTOMER.txt" "release\Sealink-OEM\README_CUSTOMER.txt" >nul

echo.
echo Build complete.
echo Release package: release\Sealink-OEM
echo.
exit /b 0

:fail
echo.
echo Build failed.
pause
exit /b 1
