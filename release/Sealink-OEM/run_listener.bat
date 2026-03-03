@echo off
cd /d "%~dp0"
"SealinkListener.exe"
echo.
echo Listener exited. Press any key to close.
pause >nul
exit /b 0
