"""
Text summarization tool using Ollama LLM.
"""
import ollama
from typing import Dict, Optional
from .file_ops import create_file


def summarize(text: str, save_to_file: Optional[str] = None, model: str = "phi3") -> Dict:
    """
    Use Ollama LLM to summarize the provided text.
    
    Args:
        text: Text to summarize
        save_to_file: Optional filename to save summary to
        model: Ollama model to use (default: llama3)
        
    Returns:
        Dict with keys: success, summary, path, message
    """
    try:
        # Prepare the prompt
        system_prompt = """You are an expert at creating concise, informative summaries. 
Summarize the provided text in a clear, structured way. 
Include key points and main ideas.
Keep the summary concise but comprehensive."""
        
        user_prompt = f"Please summarize the following text:\n\n{text}"
        
        # Call Ollama
        print(f"Generating summary with {model}...")
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        # Extract summary
        summary = response.get("message", {}).get("content", "").strip()
        
        if not summary:
            return {
                "success": False,
                "summary": None,
                "path": None,
                "message": "Summarization resulted in empty output"
            }
        
        # Save to file if requested
        file_path = None
        if save_to_file:
            # Ensure .txt extension
            if not save_to_file.endswith('.txt'):
                save_to_file = f"{save_to_file}.txt"
            
            result = create_file(save_to_file, summary)
            
            if result["success"]:
                file_path = result["path"]
            else:
                return {
                    "success": False,
                    "summary": summary,
                    "path": None,
                    "message": f"Summary generated but failed to save: {result['message']}"
                }
        
        message = f"Generated summary of {len(summary)} characters"
        if file_path:
            message += f" and saved to {save_to_file}"
        
        return {
            "success": True,
            "summary": summary,
            "path": file_path,
            "message": message
        }
        
    except ollama.ResponseError as e:
        print(f"Ollama error: {e}. Trying fallback model...")
        if model == "phi3":
            return summarize(text, save_to_file, model="tinyllama")
        else:
            return {
                "success": False,
                "summary": None,
                "path": None,
                "message": f"Ollama error: {str(e)}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "summary": None,
            "path": None,
            "message": f"Error generating summary: {str(e)}"
        }


def summarize_with_bullets(text: str, save_to_file: Optional[str] = None, model: str = "phi3") -> Dict:
    """
    Generate a bullet-point summary of the text.
    
    Args:
        text: Text to summarize
        save_to_file: Optional filename to save summary to
        model: Ollama model to use
        
    Returns:
        Dict with keys: success, summary, path, message
    """
    try:
        system_prompt = """You are an expert at creating concise summaries. 
Summarize the provided text as a bullet-point list.
Each bullet should capture a key point or main idea.
Use clear, concise language."""
        
        user_prompt = f"Please summarize the following text as bullet points:\n\n{text}"
        
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        summary = response.get("message", {}).get("content", "").strip()
        
        if not summary:
            return {
                "success": False,
                "summary": None,
                "path": None,
                "message": "Summarization resulted in empty output"
            }
        
        file_path = None
        if save_to_file:
            if not save_to_file.endswith('.txt'):
                save_to_file = f"{save_to_file}.txt"
            
            result = create_file(save_to_file, summary)
            if result["success"]:
                file_path = result["path"]
        
        message = f"Generated bullet-point summary"
        if file_path:
            message += f" and saved to {save_to_file}"
        
        return {
            "success": True,
            "summary": summary,
            "path": file_path,
            "message": message
        }
        
    except Exception as e:
        return {
            "success": False,
            "summary": None,
            "path": None,
            "message": f"Error generating summary: {str(e)}"
        }


def extract_key_points(text: str, num_points: int = 5, model: str = "phi3") -> Dict:
    """
    Extract key points from the text.
    
    Args:
        text: Text to analyze
        num_points: Number of key points to extract
        model: Ollama model to use
        
    Returns:
        Dict with keys: success, key_points, message
    """
    try:
        system_prompt = f"""You are an expert at analyzing text and extracting key information.
Extract exactly {num_points} key points from the provided text.
Return them as a numbered list.
Each point should be concise and capture an important idea."""
        
        user_prompt = f"Extract {num_points} key points from this text:\n\n{text}"
        
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        key_points = response.get("message", {}).get("content", "").strip()
        
        return {
            "success": True,
            "key_points": key_points,
            "message": f"Extracted {num_points} key points"
        }
        
    except Exception as e:
        return {
            "success": False,
            "key_points": None,
            "message": f"Error extracting key points: {str(e)}"
        }
