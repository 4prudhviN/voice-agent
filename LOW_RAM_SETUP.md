# 🔧 Low RAM Setup Guide

If you have less than 8GB of available RAM, follow this guide to use smaller models.

## Your Situation

You're getting this error:
```
Error: model requires more system memory (4.6 GiB) than is available (3.0 GiB)
```

## Solution: Use Smaller Models

### Step 1: Remove Large Models

```powershell
ollama rm llama3
ollama rm mistral
```

### Step 2: Install Smaller Models

**Option A: phi3 (Recommended - ~2.3GB RAM)**
```powershell
ollama pull phi3
```

**Option B: tinyllama (Smallest - ~637MB RAM)**
```powershell
ollama pull tinyllama
```

### Step 3: Test the Model

```powershell
ollama run phi3 "Say hello"
```

Type `/bye` to exit.

### Step 4: Run Your Voice Agent

The app has been updated to use phi3 by default:

```powershell
cd voice-agent
python app.py
```

## Model Comparison

| Model | RAM Required | Quality | Speed |
|-------|-------------|---------|-------|
| **tinyllama** | ~637MB | Basic | Very Fast |
| **phi3** | ~2.3GB | Good | Fast |
| llama3 | ~4.6GB | Excellent | Medium |
| mistral | ~4.1GB | Excellent | Medium |

## Tips for Low RAM Systems

1. **Close other applications** before running the voice agent
2. **Use phi3** for best balance of quality and RAM usage
3. **Use tinyllama** if phi3 still doesn't fit
4. **Restart your computer** to free up RAM if needed
5. **Check Task Manager** (Ctrl+Shift+Esc) to see RAM usage

## Checking Available RAM

```powershell
# Check total and available RAM
systeminfo | findstr /C:"Total Physical Memory" /C:"Available Physical Memory"
```

## If Still Having Issues

### Free Up More RAM

1. Close Chrome/Edge browsers
2. Close unnecessary applications
3. Restart your computer
4. Disable startup programs

### Use Even Smaller Model

If phi3 doesn't work, use tinyllama:

```powershell
ollama pull tinyllama
```

Then in the UI, select "tinyllama" from the model dropdown.

## Performance Expectations

### With phi3:
- Intent classification: 2-3 seconds
- Code generation: 5-15 seconds
- Summarization: 3-8 seconds

### With tinyllama:
- Intent classification: 1-2 seconds
- Code generation: 3-10 seconds
- Summarization: 2-5 seconds
- Quality may be lower than phi3

## Your System is Ready!

The voice agent has been configured to use phi3 by default, which should work on your system. Just run:

```powershell
cd voice-agent
python app.py
```

And access at: http://localhost:7860
