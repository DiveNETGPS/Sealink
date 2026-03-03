@echo off
setlocal

cd /d "%~dp0"

set "SRC_ROOT=product"
set "OUT=release\Sealink-Integrator-Pack"

if not exist "%SRC_ROOT%\resources\uart-getRange.py" (
    echo Missing required file: %SRC_ROOT%\resources\uart-getRange.py
    pause
    exit /b 1
)

if not exist "%SRC_ROOT%\integrations\arduino\SealinkOEM_Basic.ino" (
    echo Missing required file: %SRC_ROOT%\integrations\arduino\SealinkOEM_Basic.ino
    pause
    exit /b 1
)

if not exist "%SRC_ROOT%\integrations\raspberry-pi\run_sealink_cli.sh" (
    echo Missing required file: %SRC_ROOT%\integrations\raspberry-pi\run_sealink_cli.sh
    pause
    exit /b 1
)

echo Cleaning integrator pack...
if exist "%OUT%" rmdir /s /q "%OUT%"

echo Creating folder layout...
mkdir "%OUT%\resources" >nul
mkdir "%OUT%\integrations\arduino" >nul
mkdir "%OUT%\integrations\raspberry-pi" >nul
mkdir "%OUT%\docs" >nul

echo Copying platform files...
copy /y "%SRC_ROOT%\resources\uart-getRange.py" "%OUT%\resources\uart-getRange.py" >nul
copy /y "%SRC_ROOT%\resources\requirements.txt" "%OUT%\resources\requirements.txt" >nul
copy /y "%SRC_ROOT%\resources\sealink_utility.py" "%OUT%\resources\sealink_utility.py" >nul

copy /y "%SRC_ROOT%\integrations\arduino\SealinkOEM_Basic.ino" "%OUT%\integrations\arduino\SealinkOEM_Basic.ino" >nul
copy /y "%SRC_ROOT%\integrations\raspberry-pi\run_sealink_cli.sh" "%OUT%\integrations\raspberry-pi\run_sealink_cli.sh" >nul
copy /y "%SRC_ROOT%\integrations\PLATFORM_INTEGRATOR_GUIDE.md" "%OUT%\PLATFORM_INTEGRATOR_GUIDE.md" >nul

echo Copying core docs...
copy /y "%SRC_ROOT%\docs\Sealink-OEM_Getting_Started.md" "%OUT%\docs\Sealink-OEM_Getting_Started.md" >nul
copy /y "%SRC_ROOT%\docs\Sealink-OEM_Communication_Protocol.md" "%OUT%\docs\Sealink-OEM_Communication_Protocol.md" >nul
copy /y "%SRC_ROOT%\docs\Sealink-OEM_Pinout_and_Interface.md" "%OUT%\docs\Sealink-OEM_Pinout_and_Interface.md" >nul
copy /y "%SRC_ROOT%\docs\Sealink-OEM_Basic_Ranging_Guide.md" "%OUT%\docs\Sealink-OEM_Basic_Ranging_Guide.md" >nul
if exist "%SRC_ROOT%\docs\Sealink-OEM_Technical_Drawing.pdf" (
    copy /y "%SRC_ROOT%\docs\Sealink-OEM_Technical_Drawing.pdf" "%OUT%\docs\Sealink-OEM_Technical_Drawing.pdf" >nul
)

echo.
echo Integrator pack ready: %OUT%
echo.
exit /b 0
