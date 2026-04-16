# 🎯 Quick Reference Guide

## Starting the Application

```bash
# Windows
start.bat

# macOS/Linux
./start.sh

# Or manually
python app.py
```

Access at: **http://localhost:7860**

## Command Examples

### Code Generation

| Command | Result |
|---------|--------|
| "Write a Python function to sort a list" | Generates Python code, saves to `output/generated_*.py` |
| "Create a JavaScript function to validate email" | Generates JS code, saves to `output/generated_*.js` |
| "Generate Java code for a binary search" | Generates Java code, saves to `output/generated_*.java` |

### File Creation

| Command | Result |
|---------|--------|
| "Create a file called notes.txt" | Creates `output/notes.txt` |
| "Save this to ideas.txt: Build an AI agent" | Creates `output/ideas.txt` with content |
| "Make a file named todo.txt with my tasks" | Creates `output/todo.txt` |

### Text Summarization

| Command | Result |
|---------|--------|
| "Summarize this text: [long text]" | Displays summary |
| "Summarize and save to summary.txt" | Saves summary to `output/summary.txt` |
| "Give me a summary of this article" | Displays summary |

### General Chat

| Command | Result |
|---------|--------|
| "Hello, how are you?" | Friendly chat response |
| "What can you do?" | Explains capabilities |
| "Tell me about Python" | Informative response |

## Supported Programming Languages

- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- C (.c)
- C++ (.cpp)
- C# (.cs)
- Go (.go)
- Rust (.rs)
- Ruby (.rb)
- PHP (.php)
- Swift (.swift)
- Kotlin (.kt)
- HTML (.html)
- CSS (.css)
- SQL (.sql)
- Bash (.sh)

## Keyboard Shortcuts

- **Tab**: Switch between Audio and Text input
- **Enter**: Submit text input (when focused)
- **Ctrl+C**: Stop the server (in terminal)

## UI Components

### Audio Input Tab
- 🎤 **Microphone**: Click to record voice
- 📁 **Upload**: Upload audio file (.wav, .mp3, .ogg, .m4a)
- ▶ **Run Agent**: Process the audio

### Text Input Tab
- ✏️ **Text Box**: Type command directly
- ▶ **Run Agent**: Process the text

### Results Section
- 📝 **Transcription**: What was heard/typed
- 🎯 **Intent**: Detected action type
- 💡 **Action Taken**: What the agent did
- 📄 **Output**: Generated content
- 📁 **File Path**: Where file was saved
- ✅ **Status**: Success or error message

### Session History
- 📜 **History Table**: All actions in current session
- 🗑️ **Clear History**: Reset the history

## Model Selection

Available models (select in dropdown):
- **llama3**: Best overall performance (recommended)
- **mistral**: Faster, good quality
- **llama2**: Alternative option
- **codellama**: Optimized for code generation

## Common Issues & Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| "Ollama not responding" | Run `ollama serve` in terminal |
| "Model not found" | Run `ollama pull llama3` |
| Empty transcription | Speak louder and clearer |
| Slow performance | Use smaller model (mistral) |
| Port already in use | Change port in `app.py` |

## File Locations

- **Generated Files**: `./output/`
- **Logs**: Terminal output
- **Models**: `~/.ollama/models/` (Ollama) and `~/.cache/whisper/` (Whisper)

## Tips for Best Results

### Voice Input
- Speak clearly and at normal pace
- Minimize background noise
- Use a good quality microphone
- Keep commands concise (under 30 seconds)

### Text Input
- Be specific about what you want
- Mention programming language for code
- Specify filename when creating files
- Use natural language

### Code Generation
- Describe the function/feature clearly
- Mention edge cases if important
- Specify language explicitly
- Review generated code before use

### File Operations
- Always specify filename with extension
- Use descriptive filenames
- Check `output/` folder for results
- Files are automatically saved

## Safety Features

✅ All files saved to `./output/` only
✅ Path traversal protection
✅ Filename sanitization
✅ No external API calls
✅ Fully local processing

## Performance Benchmarks

Typical processing times (on recommended hardware):

- **Audio Transcription**: 2-5 seconds (for 10s audio)
- **Intent Classification**: 1-2 seconds
- **Code Generation**: 3-10 seconds
- **Summarization**: 2-5 seconds
- **File Creation**: <1 second

## Stopping the Application

1. Go to terminal where app is running
2. Press `Ctrl+C`
3. Wait for graceful shutdown
4. Deactivate venv: `deactivate`

## Updating

To update dependencies:
```bash
pip install --upgrade -r requirements.txt
```

To update Ollama models:
```bash
ollama pull llama3
```

## Environment Variables

Optional configuration:

```bash
# Force CPU mode (disable GPU)
export CUDA_VISIBLE_DEVICES=""

# Change Ollama host
export OLLAMA_HOST="http://localhost:11434"
```

## API Endpoints (Advanced)

The Gradio app exposes these functions:
- `process_audio(audio_path, model)`: Process audio input
- `process_text(text, model)`: Process text input
- `check_ollama_status(model)`: Check Ollama connection

## Logs and Debugging

Enable verbose logging:
```bash
# In terminal before running app
export GRADIO_DEBUG=1
python app.py
```

Check component status:
```bash
python test_components.py
```

## Resource Usage

Typical memory usage:
- **Whisper (base)**: ~1GB RAM
- **Ollama (llama3)**: ~4-6GB RAM
- **Gradio UI**: ~200MB RAM
- **Total**: ~6-8GB RAM

## Customization

Quick customization points:

1. **Change Whisper model**: Edit `stt/transcriber.py`, line with `load_model("base")`
2. **Change default LLM**: Edit `app.py`, change `model_selector` default value
3. **Modify prompts**: Edit system prompts in `intent/classifier.py` and `tools/`
4. **Change UI theme**: Edit `app.py`, change `gr.themes.Soft()` to other themes
5. **Add new intents**: Extend `intent/classifier.py` and `agent/orchestrator.py`

## Getting Help

1. Check error messages in terminal
2. Use "Check Ollama Status" button
3. Run `python test_components.py`
4. Review SETUP_GUIDE.md
5. Check README.md for detailed info

---

**Happy voice commanding!** 🎙️✨
