@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel% equ 0 (
  py -3 chapter3_lab.py %*
) else (
  python chapter3_lab.py %*
)
pause
