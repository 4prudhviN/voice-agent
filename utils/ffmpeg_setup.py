"""
Automatic ffmpeg setup for Windows.
Downloads and configures ffmpeg if not found.
"""
import os
import sys
import zipfile
import urllib.request
from pathlib import Path


FFMPEG_DIR = Path("ffmpeg_bin")
FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"


def is_ffmpeg_available():
    """Check if ffmpeg is available in PATH or local directory."""
    # Check in PATH
    try:
        import subprocess
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, 
                              timeout=5)
        if result.returncode == 0:
            return True
    except:
        pass
    
    # Check in local directory
    local_ffmpeg = FFMPEG_DIR / "bin" / "ffmpeg.exe"
    if local_ffmpeg.exists():
        return True
    
    return False


def download_ffmpeg():
    """Download and extract ffmpeg to local directory."""
    print("\n" + "="*60)
    print("ffmpeg not found. Downloading ffmpeg...")
    print("This is a one-time setup (~100MB download)")
    print("="*60 + "\n")
    
    try:
        # Create directory
        FFMPEG_DIR.mkdir(exist_ok=True)
        
        # Download
        zip_path = FFMPEG_DIR / "ffmpeg.zip"
        print("Downloading ffmpeg... (this may take a few minutes)")
        
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(downloaded * 100 / total_size, 100)
            print(f"\rProgress: {percent:.1f}%", end="")
        
        urllib.request.urlretrieve(FFMPEG_URL, zip_path, show_progress)
        print("\n\nExtracting ffmpeg...")
        
        # Extract
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(FFMPEG_DIR)
        
        # Find the extracted folder (it has a version-specific name)
        extracted_folders = [f for f in FFMPEG_DIR.iterdir() if f.is_dir()]
        if extracted_folders:
            # Move bin folder to root
            source_bin = extracted_folders[0] / "bin"
            target_bin = FFMPEG_DIR / "bin"
            
            if source_bin.exists():
                if target_bin.exists():
                    import shutil
                    shutil.rmtree(target_bin)
                source_bin.rename(target_bin)
        
        # Clean up
        zip_path.unlink()
        
        print("✅ ffmpeg installed successfully!")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to download ffmpeg: {e}")
        print("\nPlease install ffmpeg manually:")
        print("1. Download from: https://ffmpeg.org/download.html")
        print("2. Or run: choco install ffmpeg")
        print("="*60 + "\n")
        return False


def setup_ffmpeg():
    """Setup ffmpeg - download if needed and add to PATH."""
    if is_ffmpeg_available():
        print("✅ ffmpeg is available")
        return True
    
    # Try to download
    if download_ffmpeg():
        # Add to PATH for this session
        ffmpeg_bin = str((FFMPEG_DIR / "bin").absolute())
        os.environ["PATH"] = ffmpeg_bin + os.pathsep + os.environ["PATH"]
        
        # Verify it works
        if is_ffmpeg_available():
            print("✅ ffmpeg is now ready to use")
            return True
    
    return False


def get_ffmpeg_path():
    """Get the path to ffmpeg executable."""
    # Check local installation
    local_ffmpeg = FFMPEG_DIR / "bin" / "ffmpeg.exe"
    if local_ffmpeg.exists():
        return str(local_ffmpeg.absolute())
    
    # Return system ffmpeg
    return "ffmpeg"


if __name__ == "__main__":
    # Test the setup
    if setup_ffmpeg():
        print("\nTesting ffmpeg...")
        import subprocess
        result = subprocess.run([get_ffmpeg_path(), "-version"], 
                              capture_output=True, 
                              text=True)
        print(result.stdout[:200])
