@echo off
REM AI Benchmark - Startup Script for Windows

echo ==================================
echo AI Benchmark - LLM Comparison Tool
echo ==================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Using Python: 
python --version
echo.

REM Check if requirements are installed
echo Checking dependencies...
python -c "import gradio" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies OK
echo.

REM Check if .env exists
if not exist .env (
    echo Warning: .env file not found
    echo Copy .env.example to .env and add your API keys
    echo.
)

echo Starting AI Benchmark application...
echo Once started, open http://localhost:7860 in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the application
python app.py
if errorlevel 1 (
    echo.
    echo Error: Application failed to start
    echo Please check the error messages above
    pause
    exit /b 1
)

pause
