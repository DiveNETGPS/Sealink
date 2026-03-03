@echo off
cd /d "%~dp0"
start "Sealink Listener" /min cmd /c "SealinkListener.exe"
timeout /t 1 /nobreak >nul
start "Sealink Utility" "SealinkUtility.exe"
exit /b 0
