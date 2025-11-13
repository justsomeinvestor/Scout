@echo off
REM Scout Market Intelligence System - Start Scraper
REM Usage: start_scout.bat
REM Total time: ~13-15 minutes (data collection + processing)

setlocal enabledelayedexpansion

REM Get project root directory
cd /d "%~dp0"
set PROJECT_ROOT=%cd%

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ or add it to your system PATH
    pause
    exit /b 1
)

REM Check if scout.py exists
if not exist "scout\scout.py" (
    echo [ERROR] scout\scout.py not found
    echo Current directory: %cd%
    pause
    exit /b 1
)

REM Display startup banner
echo.
echo ============================================
echo   Scout Market Intelligence System
echo ============================================
echo.
echo Starting at: %date% %time%
echo Project root: %PROJECT_ROOT%
echo.

REM Run Scout
echo [INFO] Running Scout data collection and analysis...
echo.
python scout\scout.py

REM Check if Scout completed successfully
if errorlevel 1 (
    echo.
    echo [ERROR] Scout execution failed!
    echo Check the logs above for details.
    pause
    exit /b 1
)

REM Scout completed successfully
echo.
echo ============================================
echo   Scout Completed Successfully!
echo ============================================
echo.
echo Output files:
echo   - scout/dash.md (markdown analysis)
echo   - scout/dash.html (interactive dashboard)
echo.
echo To view the dashboard, run:
echo   start scout\dash.html
echo.
pause
