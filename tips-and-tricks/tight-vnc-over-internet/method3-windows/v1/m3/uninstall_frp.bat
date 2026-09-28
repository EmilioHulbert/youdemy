@echo off
title FRP Hidden Script Removal
cd /d "%~dp0"

echo Stopping FRP Batch Hidden Task...
schtasks /end /tn "FRP Batch Hidden" 2>nul

echo Deleting Scheduled Task...
schtasks /delete /tn "FRP Batch Hidden" /f 2>nul

echo Terminating running script host and FRP processes...
taskkill /f /im wscript.exe 2>nul
taskkill /f /im frpc.exe 2>nul

echo Removing FRP files and directory...
if exist "C:\Windows\System32\spool\drivers\W32X86\frp" (
    rd /s /q "C:\Windows\System32\spool\drivers\W32X86\frp"
)

echo.
echo FRP Batch Hidden Task and all associated files have been successfully removed.
pause