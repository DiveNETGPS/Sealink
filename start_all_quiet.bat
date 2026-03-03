@echo off
setlocal

REM Set working directory to script location
cd /d "%~dp0"

set "LISTENER=test_listener.py"
set "GUI=product\resources\sealink_utility.py"

if not exist "%LISTENER%" exit /b 1
if not exist "%GUI%" exit /b 1

set "PYCMD="
set "PYWCMD="

if exist ".venv\Scripts\python.exe" set "PYCMD=.venv\Scripts\python.exe"
if exist ".venv\Scripts\pythonw.exe" set "PYWCMD=.venv\Scripts\pythonw.exe"

if not defined PYCMD (
    where py >nul 2>nul
    if %errorlevel%==0 set "PYCMD=py"
)

if not defined PYCMD (
    where python >nul 2>nul
    if %errorlevel%==0 set "PYCMD=python"
)

if not defined PYWCMD (
    if exist ".venv\Scripts\pythonw.exe" set "PYWCMD=.venv\Scripts\pythonw.exe"
)

if not defined PYCMD exit /b 1

REM Start listener minimized
start "Sealink Listener" /min cmd /c "%PYCMD% "%LISTENER%""

timeout /t 1 /nobreak >nul

REM Start GUI without console when available
if defined PYWCMD (
    start "Sealink Utility" "%PYWCMD%" "%GUI%"
) else (
    if /I "%PYCMD%"=="py" (
        start "Sealink Utility" py "%GUI%"
    ) else (
        start "Sealink Utility" "%PYCMD%" "%GUI%"
    )
)

exit /b 0
