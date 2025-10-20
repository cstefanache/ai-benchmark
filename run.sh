#!/bin/bash

# AI Benchmark - Startup Script

echo "=================================="
echo "AI Benchmark - LLM Comparison Tool"
echo "=================================="
echo ""

# Check if Python is available
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "Error: Python is not installed"
    exit 1
fi

# Use python3 if available, otherwise python
if command -v python3 &> /dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

echo "Using Python: $PYTHON"
echo ""

# Check if requirements are installed
echo "Checking dependencies..."
$PYTHON -c "import gradio" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    $PYTHON -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

echo "Dependencies OK"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found"
    echo "Copy .env.example to .env and add your API keys"
    echo ""
fi

echo "Starting AI Benchmark application..."
echo "Once started, open http://localhost:7860 in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
$PYTHON app.py
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "Error: Application failed to start (exit code: $EXIT_CODE)"
    echo "Please check the error messages above"
    exit $EXIT_CODE
fi
