@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo  Deep-Live-Cam-Cuda - First-time setup
echo ============================================================
echo.

where python >nul 2>nul
if %errorlevel%==0 goto haspython

echo Python was not found on this system.
where winget >nul 2>nul
if not %errorlevel%==0 (
    echo Could not find winget either. Please install Python 3.11 manually from:
    echo   https://www.python.org/downloads/
    echo Then re-run this setup.bat
    pause
    exit /b 1
)

echo Installing Python 3.11 via winget - this may take a minute...
winget install -e --id Python.Python.3.11 --accept-source-agreements --accept-package-agreements
echo.
echo Python installed. Please CLOSE this window and re-run setup.bat
echo so the new PATH takes effect.
pause
exit /b 0

:haspython
python --version
echo.
python setup.py
echo.
pause
