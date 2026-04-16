"""
Speech-to-Text transcription module using OpenAI Whisper (local).
"""
import os
from typing import Optional

# Try to import whisper, but make it optional
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️  Warning: Whisper not available. Audio transcription disabled.")
    print("   You can still use text input!")


# Set ffmpeg path if using bundled version
def _setup_ffmpeg():
    """Setup ffmpeg for Whisper."""
    if not WHISPER_AVAILABLE:
        return
    
    try:
        from utils.ffmpeg_setup import setup_ffmpeg, get_ffmpeg_path
        if setup_ffmpeg():
            # Set environment variable for ffmpeg
            ffmpeg_path = get_ffmpeg_path()
            if os.path.exists(ffmpeg_path):
                os.environ["FFMPEG_BINARY"] = ffmpeg_path
    except ImportError:
        pass  # utils not available, assume system ffmpeg


# Setup ffmpeg on module import
_setup_ffmpeg()


def transcribe(audio_path: str) -> str:
    """
    Load the audio file from audio_path and transcribe using Whisper.
    
    Args:
        audio_path: Path to the audio file (.wav, .mp3, .ogg, .m4a)
        
    Returns:
        Transcribed text string, or error message starting with "ERROR:"
    """
    if not WHISPER_AVAILABLE:
        return "ERROR: Whisper is not installed. Audio transcription is not available. Please use text input instead."
    
    try:
        # Validate file exists
        if not os.path.exists(audio_path):
            return f"ERROR: Audio file not found at {audio_path}"
        
        # Validate file extension
        valid_extensions = ['.wav', '.mp3', '.ogg', '.m4a', '.flac', '.webm']
        file_ext = os.path.splitext(audio_path)[1].lower()
        if file_ext not in valid_extensions:
            return f"ERROR: Unsupported audio format {file_ext}. Supported: {', '.join(valid_extensions)}"
        
        # Load Whisper model (base for speed/accuracy balance)
        print(f"Loading Whisper model...")
        model = whisper.load_model("base")
        
        # Transcribe audio
        print(f"Transcribing audio from {audio_path}...")
        result = model.transcribe(audio_path, fp16=False)
        
        # Extract and clean text
        text = result.get("text", "").strip()
        
        if not text:
            return "ERROR: Transcription resulted in empty text. Audio may be silent or unintelligible."
        
        print(f"Transcription successful: {text[:100]}...")
        return text
        
    except FileNotFoundError as e:
        if "ffmpeg" in str(e).lower() or "ffprobe" in str(e).lower():
            return "ERROR: ffmpeg is not installed. Please install ffmpeg: 'choco install ffmpeg' or download from https://ffmpeg.org/download.html"
        return f"ERROR: File not found - {str(e)}"
    except Exception as e:
        return f"ERROR: Transcription failed - {str(e)}"


def transcribe_with_language(audio_path: str, language: Optional[str] = None) -> dict:
    """
    Transcribe audio with optional language specification.
    
    Args:
        audio_path: Path to the audio file
        language: Optional ISO language code (e.g., 'en', 'es', 'fr')
        
    Returns:
        Dict with keys: text, language, success, error
    """
    if not WHISPER_AVAILABLE:
        return {
            "text": "",
            "language": None,
            "success": False,
            "error": "Whisper is not installed. Audio transcription is not available."
        }
    
    try:
        if not os.path.exists(audio_path):
            return {
                "text": "",
                "language": None,
                "success": False,
                "error": f"Audio file not found at {audio_path}"
            }
        
        model = whisper.load_model("base")
        
        # Transcribe with optional language hint
        kwargs = {"fp16": False}
        if language:
            kwargs["language"] = language
            
        result = model.transcribe(audio_path, **kwargs)
        
        text = result.get("text", "").strip()
        detected_language = result.get("language", "unknown")
        
        return {
            "text": text,
            "language": detected_language,
            "success": True,
            "error": None
        }
        
    except Exception as e:
        return {
            "text": "",
            "language": None,
            "success": False,
            "error": str(e)
        }
