@echo off
REM Batch file wrapper for running Python scrapers
REM This avoids Node.js shell issues that some AIs encounter
REM
REM Usage: run_scrapers.bat

echo.
echo ======================================================================
echo   SCRAPER LAUNCHER (Batch File)
echo ======================================================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo Working Directory: %CD%
echo.

echo Launching Python scraper orchestrator...
echo.

REM Run the Python scraper orchestrator
python scripts\run_all_scrapers.py

set EXITCODE=%ERRORLEVEL%

echo.
if %EXITCODE% EQU 0 (
    echo ======================================================================
    echo   SCRAPERS COMPLETED SUCCESSFULLY
    echo ======================================================================
) else (
    echo ======================================================================
    echo   SCRAPERS FAILED (Exit Code: %EXITCODE%^)
    echo ======================================================================
)

echo.
exit /b %EXITCODE%
