@echo off
title FRP Script Removal
cd /d "%~dp0"

echo Stopping FRP Client Service...
schtasks /end /tn "FRP Client Service1" 2>nul

echo Deleting Scheduled Task...
schtasks /delete /tn "FRP Client Service1" /f 2>nul

echo Terminating any remaining frpc processes...
taskkill /f /im frpc.exe 2>nul

echo Removing FRP files and directory...
if exist "C:\Windows\System32\spool\drivers\W32X86\frp" (
    rd /s /q "C:\Windows\System32\spool\drivers\W32X86\frp"
)

echo.
echo FRP Client Service and files have been successfully removed.
pause