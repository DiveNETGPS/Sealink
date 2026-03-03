@echo off
setlocal

REM Set working directory to script location
cd /d "%~dp0"

set "SCRIPT=product\resources\sealink_utility.py"

if not exist "%SCRIPT%" (
    echo Missing file: %SCRIPT%
    pause
    exit /b 1
)

REM Use local virtual environment when available
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" "%SCRIPT%"
    exit /b 0
)

if exist ".venv\Scripts\python.exe" (
    start "" ".venv\Scripts\python.exe" "%SCRIPT%"
    exit /b 0
)

REM Use system Python launcher if needed
where py >nul 2>nul
if %errorlevel%==0 (
    start "" py "%SCRIPT%"
    exit /b 0
)

where python >nul 2>nul
if %errorlevel%==0 (
    start "" python "%SCRIPT%"
    exit /b 0
)

echo Python executable not found. Install Python or create .venv in this folder.
pause
exit /b 1
