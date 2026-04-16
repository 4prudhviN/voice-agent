# 🚀 Complete Setup Guide

This guide will walk you through setting up the Voice-Controlled Local AI Agent from scratch.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installing Prerequisites](#installing-prerequisites)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)
5. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **CPU**: 4 cores (Intel i5 or equivalent)
- **RAM**: 8GB
- **Storage**: 5GB free space
- **Python**: 3.10 or higher

### Recommended Requirements
- **CPU**: 8 cores (Intel i7 or equivalent)
- **RAM**: 16GB
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster processing)
- **Storage**: 10GB free space

## Installing Prerequisites

### 1. Install Python 3.10+

#### Windows
Download from [python.org](https://www.python.org/downloads/) and run the installer.
Make sure to check "Add Python to PATH" during installation.

#### macOS
```bash
brew install python@3.11
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### 2. Install ffmpeg

#### Windows
Using Chocolatey:
```bash
choco install ffmpeg
```

Or download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

#### macOS
```bash
brew install ffmpeg
```

#### Linux
```bash
sudo apt update
sudo apt install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

### 3. Install Ollama

#### All Platforms
1. Visit [https://ollama.ai](https://ollama.ai)
2. Download the installer for your OS
3. Run the installer
4. Verify installation:
```bash
ollama --version
```

## Project Setup

### Step 1: Navigate to Project Directory

```bash
cd voice-agent
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- openai-whisper (speech-to-text)
- gradio (web interface)
- ollama (LLM client)
- torch (deep learning framework)
- And other dependencies

**Note**: First installation may take 5-10 minutes depending on your internet speed.

### Step 4: Start Ollama Service

Open a **new terminal window** and run:

```bash
ollama serve
```

Keep this terminal open. You should see:
```
Ollama is running on http://localhost:11434
```

### Step 5: Pull Required Models

In another terminal (with venv activated):

```bash
# Pull the primary model (required)
ollama pull llama3

# Optional: Pull alternative models
ollama pull mistral
ollama pull codellama
```

**Note**: Model downloads are 4-7GB each and may take 10-30 minutes depending on your internet speed.

Verify models are installed:
```bash
ollama list
```

### Step 6: Test Components

Run the test script to verify everything is working:

```bash
python test_components.py
```

You should see all tests pass with ✅ marks.

## Running the Application

### Option 1: Using Startup Scripts (Recommended)

#### Windows
```bash
start.bat
```

#### macOS/Linux
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Start

```bash
# Make sure venv is activated
# Make sure Ollama is running in another terminal

python app.py
```

### Accessing the UI

Once started, open your browser and navigate to:
```
http://localhost:7860
```

You should see the Voice-Controlled AI Agent interface.

## First Steps

### 1. Check Ollama Status

Click the "🔍 Check Ollama Status" button in the UI to verify connection.

### 2. Try Text Input First

Go to the "💬 Text Input (Debug)" tab and try:
```
Write a Python function to add two numbers
```

Click "▶ Run Agent" and verify you get code output.

### 3. Try Audio Input

Go to the "🎤 Audio Input" tab:
- Click the microphone icon to record
- Say: "Write a Python function to calculate factorial"
- Click "▶ Run Agent"

## Troubleshooting

### Issue: "Ollama is not responding"

**Solution:**
1. Check if Ollama is running: `ollama serve`
2. Verify model is pulled: `ollama list`
3. Try pulling the model again: `ollama pull llama3`

### Issue: "ModuleNotFoundError"

**Solution:**
1. Ensure virtual environment is activated (you should see `(venv)` in prompt)
2. Reinstall requirements: `pip install -r requirements.txt`

### Issue: "ffmpeg not found"

**Solution:**
1. Install ffmpeg (see prerequisites section)
2. Verify installation: `ffmpeg -version`
3. Restart your terminal after installation

### Issue: Whisper model download fails

**Solution:**
1. Check internet connection
2. The model downloads automatically on first use (~140MB)
3. If it fails, try running again - it will resume the download

### Issue: "CUDA out of memory" or GPU errors

**Solution:**
1. Whisper will automatically fall back to CPU
2. To force CPU mode, set environment variable:
   ```bash
   export CUDA_VISIBLE_DEVICES=""
   ```

### Issue: Audio transcription is empty or incorrect

**Solution:**
1. Ensure audio is clear and not too quiet
2. Speak clearly and at a normal pace
3. Try uploading a pre-recorded audio file instead
4. Check supported formats: .wav, .mp3, .ogg, .m4a

### Issue: Port 7860 already in use

**Solution:**
Edit `app.py` and change the port:
```python
app.launch(
    server_port=7861,  # Change this
    ...
)
```

## Performance Tips

### For Faster Transcription
- Use a GPU if available (CUDA-enabled NVIDIA GPU)
- Use shorter audio clips (under 30 seconds)
- Use the "tiny" or "small" Whisper model (edit `stt/transcriber.py`)

### For Faster LLM Responses
- Use smaller models: `mistral` is faster than `llama3`
- Reduce context length in prompts
- Use GPU acceleration if available

### For Lower Memory Usage
- Use Whisper "tiny" model instead of "base"
- Use smaller Ollama models
- Close other applications

## Next Steps

Once everything is working:

1. **Explore the UI**: Try different commands and intents
2. **Check Output Files**: Look in the `output/` directory for generated files
3. **Review Session History**: See the history table at the bottom of the UI
4. **Customize**: Modify prompts in the code to suit your needs
5. **Add Models**: Pull more Ollama models for different capabilities

## Getting Help

If you encounter issues not covered here:

1. Check the main README.md for additional information
2. Review error messages carefully - they often indicate the solution
3. Ensure all prerequisites are properly installed
4. Try the test script: `python test_components.py`

## Security Notes

- All file operations are restricted to the `./output/` directory
- No data is sent to external servers (fully local)
- Audio files are processed locally and not stored permanently
- Generated files are saved only in the designated output folder

---

**Congratulations!** You now have a fully functional voice-controlled AI agent running locally on your machine. 🎉
