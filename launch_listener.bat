@echo off
setlocal

REM Set working directory to script location
cd /d "%~dp0"

set "SCRIPT=test_listener.py"

if not exist "%SCRIPT%" (
    echo Missing file: %SCRIPT%
    pause
    exit /b 1
)

echo Starting listener...

REM Use local virtual environment when available
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" "%SCRIPT%"
    goto :done
)

REM Use system Python launcher if needed
where py >nul 2>nul
if %errorlevel%==0 (
    py "%SCRIPT%"
    goto :done
)

where python >nul 2>nul
if %errorlevel%==0 (
    python "%SCRIPT%"
    goto :done
)

echo Python executable not found. Install Python or create .venv in this folder.

:done
echo.
echo Listener exited.
pause >nul
exit /b 0
