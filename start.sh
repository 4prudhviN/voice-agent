#!/bin/bash

# Voice-Controlled AI Agent Startup Script

echo "=========================================="
echo "Voice-Controlled Local AI Agent"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import gradio" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Check if Ollama is running
echo ""
echo "Checking Ollama status..."
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "⚠️  Ollama is not running!"
    echo "Please start Ollama in another terminal:"
    echo "  ollama serve"
    echo ""
    read -p "Press Enter when Ollama is running, or Ctrl+C to exit..."
fi

# Check if llama3 model is available
echo "Checking for llama3 model..."
if ! ollama list | grep -q "llama3"; then
    echo "⚠️  llama3 model not found!"
    echo "Pulling llama3 model (this may take a few minutes)..."
    ollama pull llama3
fi

echo ""
echo "✅ All checks passed!"
echo ""
echo "Starting the application..."
echo "Access the UI at: http://localhost:7860"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Run the application
python app.py
