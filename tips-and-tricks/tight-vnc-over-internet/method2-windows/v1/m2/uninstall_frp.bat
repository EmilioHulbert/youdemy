@echo off
title FRP Batch Script Removal
cd /d "%~dp0"

echo Stopping FRP Batch Service...
schtasks /end /tn "FRP Batch Service" 2>nul

echo Deleting Scheduled Task...
schtasks /delete /tn "FRP Batch Service" /f 2>nul

echo Terminating running FRP processes...
taskkill /f /im frpc.exe 2>nul

echo Removing FRP files and directory...
if exist "C:\Windows\System32\spool\drivers\W32X86\frp" (
    rd /s /q "C:\Windows\System32\spool\drivers\W32X86\frp"
)

echo.
echo FRP Batch Service and all associated files have been successfully removed.
pause