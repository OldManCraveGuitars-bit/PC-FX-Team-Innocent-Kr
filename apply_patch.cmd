@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
    if "%~1"=="" (py -3 apply_patch.py) else (py -3 apply_patch.py --source "%~1")
) else (
    if "%~1"=="" (python apply_patch.py) else (python apply_patch.py --source "%~1")
)
if errorlevel 1 (
    echo.
    echo Patch failed. The original disc files were not modified.
    pause
    exit /b 1
)
echo.
echo Patched disc is in the patched_disc folder.
pause
