"""
File operations tool - create files and folders safely in output/ directory.
"""
import os
from pathlib import Path
from typing import Dict


OUTPUT_DIR = Path("output")


def _sanitize_path(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    
    Args:
        filename: User-provided filename
        
    Returns:
        Sanitized filename (basename only)
    """
    # Remove any path components, keep only the filename
    filename = os.path.basename(filename)
    
    # Remove any remaining dangerous characters
    filename = filename.replace("..", "")
    filename = filename.replace("/", "_")
    filename = filename.replace("\\", "_")
    
    return filename


def _ensure_output_dir() -> None:
    """Ensure the output directory exists."""
    OUTPUT_DIR.mkdir(exist_ok=True)


def create_file(filename: str, content: str = "") -> Dict:
    """
    Create a file inside ./output/ directory ONLY.
    
    Args:
        filename: Name of the file to create
        content: Content to write to the file
        
    Returns:
        Dict with keys: success, path, message
    """
    try:
        # Ensure output directory exists
        _ensure_output_dir()
        
        # Sanitize filename
        safe_filename = _sanitize_path(filename)
        
        if not safe_filename:
            return {
                "success": False,
                "path": None,
                "message": "Invalid filename provided"
            }
        
        # Construct safe path
        file_path = OUTPUT_DIR / safe_filename
        
        # Write content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "path": str(file_path),
            "message": f"File '{safe_filename}' created successfully with {len(content)} characters"
        }
        
    except PermissionError:
        return {
            "success": False,
            "path": None,
            "message": f"Permission denied: Cannot write to {filename}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "path": None,
            "message": f"Error creating file: {str(e)}"
        }


def create_folder(foldername: str) -> Dict:
    """
    Create a folder inside ./output/ directory ONLY.
    
    Args:
        foldername: Name of the folder to create
        
    Returns:
        Dict with keys: success, path, message
    """
    try:
        # Ensure output directory exists
        _ensure_output_dir()
        
        # Sanitize folder name
        safe_foldername = _sanitize_path(foldername)
        
        if not safe_foldername:
            return {
                "success": False,
                "path": None,
                "message": "Invalid folder name provided"
            }
        
        # Construct safe path
        folder_path = OUTPUT_DIR / safe_foldername
        
        # Create folder
        folder_path.mkdir(exist_ok=True)
        
        return {
            "success": True,
            "path": str(folder_path),
            "message": f"Folder '{safe_foldername}' created successfully"
        }
        
    except PermissionError:
        return {
            "success": False,
            "path": None,
            "message": f"Permission denied: Cannot create folder {foldername}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "path": None,
            "message": f"Error creating folder: {str(e)}"
        }


def read_file(filename: str) -> Dict:
    """
    Read a file from the output directory.
    
    Args:
        filename: Name of the file to read
        
    Returns:
        Dict with keys: success, content, message
    """
    try:
        safe_filename = _sanitize_path(filename)
        file_path = OUTPUT_DIR / safe_filename
        
        if not file_path.exists():
            return {
                "success": False,
                "content": None,
                "message": f"File '{safe_filename}' not found in output directory"
            }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "success": True,
            "content": content,
            "message": f"File '{safe_filename}' read successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "content": None,
            "message": f"Error reading file: {str(e)}"
        }


def list_output_files() -> Dict:
    """
    List all files in the output directory.
    
    Returns:
        Dict with keys: success, files, message
    """
    try:
        _ensure_output_dir()
        
        files = []
        for item in OUTPUT_DIR.iterdir():
            if item.is_file() and item.name != '.gitkeep':
                files.append({
                    "name": item.name,
                    "size": item.stat().st_size,
                    "modified": item.stat().st_mtime
                })
        
        return {
            "success": True,
            "files": files,
            "message": f"Found {len(files)} files in output directory"
        }
        
    except Exception as e:
        return {
            "success": False,
            "files": [],
            "message": f"Error listing files: {str(e)}"
        }
