"""
Intent classification module using Ollama LLM.
"""
import ollama
import json
from typing import Dict, Optional


SYSTEM_PROMPT = """You are an intent classification engine. Analyze the user's request and return ONLY a valid JSON object with these exact keys:
- "intent": one of "create_file", "write_code", "summarize", "web_search", "chat"
- "target_filename": filename string if user mentions a file, else null
- "language": programming language string if write_code intent, else null
- "content_hint": one sentence summarizing what the user wants
- "raw_text": the exact user input

Rules:
- If user wants to create/make/generate a file → "create_file"
- If user wants to write/generate code → "write_code"
- If user wants to summarize/condense text → "summarize"
- If user asks for current/live information, news, scores, weather, updates → "web_search"
- Otherwise → "chat"
- Return ONLY the JSON. No explanation. No markdown."""


def classify_intent(text: str, model: str = "phi3") -> Dict:
    """
    Send the transcribed text to a locally running Ollama LLM.
    
    Args:
        text: The transcribed user input text
        model: Ollama model name (default: llama3, fallback: mistral)
        
    Returns:
        Dict with keys: intent, target_filename, language, content_hint, raw_text
    """
    try:
        # Prepare the prompt
        user_prompt = f"User request: {text}"
        
        # Call Ollama
        print(f"Classifying intent with {model}...")
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        # Extract response content
        content = response.get("message", {}).get("content", "")
        
        # Clean markdown fences if present
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        # Parse JSON
        result = json.loads(content)
        
        # Validate required keys
        required_keys = ["intent", "target_filename", "language", "content_hint", "raw_text"]
        for key in required_keys:
            if key not in result:
                result[key] = None
        
        # Validate intent value
        valid_intents = ["create_file", "write_code", "summarize", "web_search", "chat"]
        if result["intent"] not in valid_intents:
            result["intent"] = "chat"
        
        # Ensure raw_text is preserved
        result["raw_text"] = text
        
        print(f"Intent classified: {result['intent']} - {result['content_hint']}")
        return result
        
    except ollama.ResponseError as e:
        print(f"Ollama error: {e}. Trying fallback model...")
        if model == "phi3":
            return classify_intent(text, model="tinyllama")
        else:
            return _fallback_intent(text, f"Ollama error: {e}")
            
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}. Using fallback classification.")
        return _fallback_intent(text, f"JSON parse error: {e}")
        
    except Exception as e:
        print(f"Intent classification failed: {e}")
        return _fallback_intent(text, str(e))


def _fallback_intent(text: str, error: str) -> Dict:
    """
    Fallback intent classification using simple keyword matching.
    
    Args:
        text: User input text
        error: Error message from primary classification
        
    Returns:
        Dict with fallback intent classification
    """
    text_lower = text.lower()
    
    # Simple keyword-based classification
    intent = "chat"
    target_filename = None
    language = None
    
    if any(word in text_lower for word in ["create file", "make file", "save to", "write to file"]):
        intent = "create_file"
        # Try to extract filename
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in ["to", "as", "named"] and i + 1 < len(words):
                target_filename = words[i + 1].strip('.,!?')
                break
    
    elif any(word in text_lower for word in ["write code", "generate code", "create function", "python", "javascript"]):
        intent = "write_code"
        # Detect language
        if "python" in text_lower:
            language = "python"
        elif "javascript" in text_lower or "js" in text_lower:
            language = "javascript"
        elif "java" in text_lower:
            language = "java"
        else:
            language = "python"  # default
    
    elif any(word in text_lower for word in ["summarize", "summary", "condense", "tldr"]):
        intent = "summarize"
    
    elif any(word in text_lower for word in ["search", "find", "look up", "current", "live", "latest", "news", "score", "update", "weather"]):
        intent = "web_search"
    
    return {
        "intent": intent,
        "target_filename": target_filename,
        "language": language,
        "content_hint": f"Fallback classification: {intent}",
        "raw_text": text,
        "error": error
    }


def test_ollama_connection(model: str = "phi3") -> Dict:
    """
    Test if Ollama is running and the model is available.
    
    Args:
        model: Model name to test
        
    Returns:
        Dict with keys: success, message, available_models
    """
    try:
        # Try to list models
        models = ollama.list()
        model_names = [m.get("name", "") for m in models.get("models", [])]
        
        # Check if requested model is available
        model_available = any(model in name for name in model_names)
        
        if not model_available:
            return {
                "success": False,
                "message": f"Model '{model}' not found. Available models: {', '.join(model_names)}",
                "available_models": model_names
            }
        
        # Try a simple chat
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        return {
            "success": True,
            "message": f"Ollama is running with model '{model}'",
            "available_models": model_names
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Ollama connection failed: {str(e)}",
            "available_models": []
        }
