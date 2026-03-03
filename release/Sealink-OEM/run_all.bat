@echo off
cd /d "%~dp0"
start "Sealink Listener" /min cmd /c "SealinkListener.exe"
timeout /t 1 /nobreak >nul
start "Sealink GUI" "SealinkGUI.exe"
exit /b 0
