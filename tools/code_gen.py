"""
Code generation tool using Ollama LLM.
"""
import ollama
from datetime import datetime
from typing import Dict, Optional
from .file_ops import create_file


LANGUAGE_EXTENSIONS = {
    "python": "py",
    "javascript": "js",
    "typescript": "ts",
    "java": "java",
    "c": "c",
    "cpp": "cpp",
    "c++": "cpp",
    "csharp": "cs",
    "c#": "cs",
    "go": "go",
    "rust": "rs",
    "ruby": "rb",
    "php": "php",
    "swift": "swift",
    "kotlin": "kt",
    "html": "html",
    "css": "css",
    "sql": "sql",
    "bash": "sh",
    "shell": "sh"
}


def generate_code(description: str, language: str = "python", filename: Optional[str] = None, model: str = "phi3") -> Dict:
    """
    Use Ollama LLM to generate code based on the description.
    
    Args:
        description: Description of what code to generate
        language: Programming language (default: python)
        filename: Optional filename to save to (auto-generated if None)
        model: Ollama model to use (default: llama3)
        
    Returns:
        Dict with keys: success, code, path, message
    """
    try:
        # Normalize language
        language = language.lower().strip()
        if language not in LANGUAGE_EXTENSIONS:
            language = "python"  # fallback
        
        # Prepare the prompt
        system_prompt = f"""You are an expert programmer. Write clean, well-commented, production-quality {language} code. Return ONLY the code, no explanation, no markdown fences."""
        
        user_prompt = description
        
        # Call Ollama
        print(f"Generating {language} code with {model}...")
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        # Extract code
        code = response.get("message", {}).get("content", "")
        
        # Clean markdown fences if present
        code = code.strip()
        if code.startswith("```"):
            lines = code.split("\n")
            # Remove first line (```language)
            lines = lines[1:]
            # Remove last line if it's ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            code = "\n".join(lines)
        
        # Remove any trailing explanations (lines starting with "In this", "This code", etc.)
        lines = code.split("\n")
        cleaned_lines = []
        for line in lines:
            # Stop at common explanation patterns
            if line.strip().startswith(("In this", "This code", "This function", "Note:", "Example:")):
                break
            # Stop at markdown-style bullet points
            if line.strip().startswith("- ") and not line.strip().startswith("- "):
                break
            cleaned_lines.append(line)
        
        code = "\n".join(cleaned_lines).strip()
        
        if not code:
            return {
                "success": False,
                "code": None,
                "path": None,
                "message": "Code generation resulted in empty output"
            }
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = LANGUAGE_EXTENSIONS.get(language, "txt")
            filename = f"generated_{timestamp}.{ext}"
        else:
            # Ensure filename has correct extension
            ext = LANGUAGE_EXTENSIONS.get(language, "txt")
            if not filename.endswith(f".{ext}"):
                filename = f"{filename}.{ext}"
        
        # Save to file
        result = create_file(filename, code)
        
        if result["success"]:
            return {
                "success": True,
                "code": code,
                "path": result["path"],
                "message": f"Generated {len(code)} characters of {language} code and saved to {filename}"
            }
        else:
            return {
                "success": False,
                "code": code,
                "path": None,
                "message": f"Code generated but failed to save: {result['message']}"
            }
        
    except ollama.ResponseError as e:
        print(f"Ollama error: {e}. Trying fallback model...")
        if model == "phi3":
            return generate_code(description, language, filename, model="tinyllama")
        else:
            return {
                "success": False,
                "code": None,
                "path": None,
                "message": f"Ollama error: {str(e)}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "code": None,
            "path": None,
            "message": f"Error generating code: {str(e)}"
        }


def generate_code_with_tests(description: str, language: str = "python", model: str = "phi3") -> Dict:
    """
    Generate code along with unit tests.
    
    Args:
        description: Description of what code to generate
        language: Programming language
        model: Ollama model to use
        
    Returns:
        Dict with keys: success, code, tests, code_path, tests_path, message
    """
    try:
        # Generate main code
        code_result = generate_code(description, language, model=model)
        
        if not code_result["success"]:
            return {
                "success": False,
                "code": None,
                "tests": None,
                "code_path": None,
                "tests_path": None,
                "message": f"Failed to generate code: {code_result['message']}"
            }
        
        # Generate tests
        test_description = f"Write unit tests for the following {language} code:\n\n{code_result['code']}"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = LANGUAGE_EXTENSIONS.get(language, "txt")
        test_filename = f"test_generated_{timestamp}.{ext}"
        
        test_result = generate_code(test_description, language, test_filename, model=model)
        
        return {
            "success": True,
            "code": code_result["code"],
            "tests": test_result.get("code"),
            "code_path": code_result["path"],
            "tests_path": test_result.get("path"),
            "message": f"Generated code and tests successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "code": None,
            "tests": None,
            "code_path": None,
            "tests_path": None,
            "message": f"Error generating code with tests: {str(e)}"
        }
