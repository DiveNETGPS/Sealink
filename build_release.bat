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

if not exist "product\resources\sealink_utility.py" (
    echo Missing utility script: product\resources\sealink_utility.py
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

echo Building utility executable...
"%PY%" -m PyInstaller --noconfirm --clean --onefile --windowed --name SealinkUtility --add-data "product\resources\uart-getRange.py;." --hidden-import serial --hidden-import serial.tools.list_ports "product\resources\sealink_utility.py"
if errorlevel 1 goto :fail

echo Building listener executable...
"%PY%" -m PyInstaller --noconfirm --clean --onefile --name SealinkListener "test_listener.py"
if errorlevel 1 goto :fail

echo Creating release folder...
mkdir "release\Sealink-OEM"
copy /y "dist\SealinkUtility.exe" "release\Sealink-OEM\SealinkUtility.exe" >nul
copy /y "dist\SealinkListener.exe" "release\Sealink-OEM\SealinkListener.exe" >nul
copy /y "release_assets\run_utility.bat" "release\Sealink-OEM\run_utility.bat" >nul
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
