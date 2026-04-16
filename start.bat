@echo off
REM Voice-Controlled AI Agent Startup Script for Windows

echo ==========================================
echo Voice-Controlled Local AI Agent
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
python -c "import gradio" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed
)

REM Check if Ollama is running
echo.
echo Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama is not running!
    echo Please start Ollama in another terminal:
    echo   ollama serve
    echo.
    pause
)

REM Check if llama3 model is available
echo Checking for llama3 model...
ollama list | findstr "llama3" >nul
if errorlevel 1 (
    echo WARNING: llama3 model not found!
    echo Pulling llama3 model (this may take a few minutes)...
    ollama pull llama3
)

echo.
echo All checks passed!
echo.
echo Starting the application...
echo Access the UI at: http://localhost:7860
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

REM Run the application
python app.py

pause
