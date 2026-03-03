@echo off
setlocal

REM Set working directory to script location
cd /d "%~dp0"

set "LISTENER=test_listener.py"
set "GUI=product\resources\sealink_utility.py"

if not exist "%LISTENER%" (
    echo Missing file: %LISTENER%
    pause
    exit /b 1
)

if not exist "%GUI%" (
    echo Missing file: %GUI%
    pause
    exit /b 1
)

REM Resolve Python command
set "PYCMD="
if exist ".venv\Scripts\python.exe" set "PYCMD=.venv\Scripts\python.exe"

if not defined PYCMD (
    where py >nul 2>nul
    if %errorlevel%==0 set "PYCMD=py"
)

if not defined PYCMD (
    where python >nul 2>nul
    if %errorlevel%==0 set "PYCMD=python"
)

if not defined PYCMD (
    echo Python executable not found. Install Python or create .venv in this folder.
    pause
    exit /b 1
)

echo Using: %PYCMD%
echo Starting listener window...
start "Sealink Listener" cmd /k "%PYCMD% "%LISTENER%""

timeout /t 1 /nobreak >nul

echo Starting utility window...
start "Sealink Utility" cmd /k "%PYCMD% "%GUI%""

echo.
echo Both processes launched.
exit /b 0
