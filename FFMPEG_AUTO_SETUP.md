# 🎵 Automatic ffmpeg Setup

Your voice agent now includes **automatic ffmpeg installation**!

## What Happens on First Run

When you run `python app.py` for the first time:

1. ✅ Checks if ffmpeg is installed
2. ✅ If not found, automatically downloads ffmpeg (~100MB)
3. ✅ Extracts it to `ffmpeg_bin/` folder
4. ✅ Configures it for use with Whisper
5. ✅ Ready to use!

## First Run Output

You'll see:
```
============================================================
🎙️  Voice-Controlled Local AI Agent
============================================================

Checking ffmpeg...
ffmpeg not found. Downloading ffmpeg...
This is a one-time setup (~100MB download)
============================================================

Downloading ffmpeg... (this may take a few minutes)
Progress: 100.0%

Extracting ffmpeg...
✅ ffmpeg installed successfully!
============================================================

✅ ffmpeg is now ready to use

Starting Gradio interface...
```

## What Gets Downloaded

- **Source**: Official FFmpeg builds from GitHub
- **Size**: ~100MB
- **Location**: `voice-agent/ffmpeg_bin/`
- **Platform**: Windows 64-bit
- **License**: GPL (open source)

## Manual Installation (Alternative)

If automatic download fails, you can install manually:

### Option 1: Chocolatey
```powershell
choco install ffmpeg -y
```

### Option 2: Manual Download
1. Download from: https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH

## Troubleshooting

### Download Fails
- Check internet connection
- Try running as Administrator
- Or install manually (see above)

### Still Not Working
The agent will show:
```
⚠️  Warning: ffmpeg not available
Audio transcription will not work without ffmpeg
You can still use text input!
```

You can use the **💬 Text Input** tab while fixing ffmpeg.

## Verifying Installation

After setup, verify ffmpeg works:
```powershell
# If using bundled version
.\ffmpeg_bin\bin\ffmpeg.exe -version

# If using system version
ffmpeg -version
```

## Cleanup

To remove the downloaded ffmpeg:
```powershell
Remove-Item -Recurse -Force ffmpeg_bin
```

It will be re-downloaded on next run if needed.

---

**Note**: The automatic download only works on Windows. For Linux/Mac, ffmpeg is usually available via package managers (apt, brew, etc.).
