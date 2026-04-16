"""
Agent orchestrator - coordinates the full pipeline from audio to result.
"""
import ollama
from typing import Dict
from stt.transcriber import transcribe
from intent.classifier import classify_intent
from tools.code_gen import generate_code
from tools.file_ops import create_file
from tools.summarizer import summarize
from tools.web_search import search_web


def run_agent(audio_path: str, model: str = "phi3") -> Dict:
    """
    Full pipeline orchestration from audio input.
    
    Args:
        audio_path: Path to audio file
        model: Ollama model to use for LLM tasks
        
    Returns:
        Dict with keys: transcription, intent, content_hint, action_taken, 
                       output, file_path, success, error
    """
    try:
        # Step 1: Transcribe audio
        print(f"\n=== Step 1: Transcribing audio ===")
        transcription = transcribe(audio_path)
        
        # Check for transcription errors
        if transcription.startswith("ERROR:"):
            return {
                "transcription": transcription,
                "intent": None,
                "content_hint": None,
                "action_taken": "Transcription failed",
                "output": transcription,
                "file_path": None,
                "success": False,
                "error": transcription
            }
        
        # Step 2: Classify intent
        print(f"\n=== Step 2: Classifying intent ===")
        intent_data = classify_intent(transcription, model=model)
        
        # Step 3: Route to appropriate tool
        print(f"\n=== Step 3: Executing action ===")
        result = _execute_intent(intent_data, model=model)
        
        # Step 4: Build unified response
        return {
            "transcription": transcription,
            "intent": intent_data.get("intent"),
            "content_hint": intent_data.get("content_hint"),
            "action_taken": result.get("action_taken"),
            "output": result.get("output"),
            "file_path": result.get("file_path"),
            "success": result.get("success", True),
            "error": result.get("error")
        }
        
    except Exception as e:
        return {
            "transcription": None,
            "intent": None,
            "content_hint": None,
            "action_taken": "Pipeline failed",
            "output": None,
            "file_path": None,
            "success": False,
            "error": f"Orchestrator error: {str(e)}"
        }


def run_agent_from_text(text: str, model: str = "phi3") -> Dict:
    """
    Same as run_agent but skips STT step - takes text directly.
    
    Args:
        text: User input text
        model: Ollama model to use for LLM tasks
        
    Returns:
        Dict with keys: transcription, intent, content_hint, action_taken,
                       output, file_path, success, error
    """
    try:
        # Step 1: Classify intent
        print(f"\n=== Step 1: Classifying intent ===")
        intent_data = classify_intent(text, model=model)
        
        # Step 2: Route to appropriate tool
        print(f"\n=== Step 2: Executing action ===")
        result = _execute_intent(intent_data, model=model)
        
        # Step 3: Build unified response
        return {
            "transcription": text,
            "intent": intent_data.get("intent"),
            "content_hint": intent_data.get("content_hint"),
            "action_taken": result.get("action_taken"),
            "output": result.get("output"),
            "file_path": result.get("file_path"),
            "success": result.get("success", True),
            "error": result.get("error")
        }
        
    except Exception as e:
        return {
            "transcription": text,
            "intent": None,
            "content_hint": None,
            "action_taken": "Pipeline failed",
            "output": None,
            "file_path": None,
            "success": False,
            "error": f"Orchestrator error: {str(e)}"
        }


def _execute_intent(intent_data: Dict, model: str = "phi3") -> Dict:
    """
    Execute the appropriate tool based on classified intent.
    
    Args:
        intent_data: Intent classification result
        model: Ollama model to use
        
    Returns:
        Dict with keys: action_taken, output, file_path, success, error
    """
    intent = intent_data.get("intent")
    raw_text = intent_data.get("raw_text", "")
    target_filename = intent_data.get("target_filename")
    language = intent_data.get("language", "python")
    
    try:
        # Route based on intent
        if intent == "write_code":
            print(f"Generating {language} code...")
            result = generate_code(
                description=raw_text,
                language=language,
                filename=target_filename,
                model=model
            )
            
            if result["success"]:
                return {
                    "action_taken": f"Generated {language} code",
                    "output": result["code"],
                    "file_path": result["path"],
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "action_taken": "Code generation failed",
                    "output": result["message"],
                    "file_path": None,
                    "success": False,
                    "error": result["message"]
                }
        
        elif intent == "create_file":
            print(f"Creating file...")
            # Extract content from raw_text
            # If target_filename is specified, use it; otherwise generate one
            if not target_filename:
                target_filename = "output.txt"
            
            result = create_file(
                filename=target_filename,
                content=raw_text
            )
            
            if result["success"]:
                return {
                    "action_taken": f"Created file '{target_filename}'",
                    "output": f"File created with content:\n{raw_text}",
                    "file_path": result["path"],
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "action_taken": "File creation failed",
                    "output": result["message"],
                    "file_path": None,
                    "success": False,
                    "error": result["message"]
                }
        
        elif intent == "summarize":
            print(f"Summarizing text...")
            result = summarize(
                text=raw_text,
                save_to_file=target_filename,
                model=model
            )
            
            if result["success"]:
                action = "Generated summary"
                if target_filename:
                    action += f" and saved to '{target_filename}'"
                
                return {
                    "action_taken": action,
                    "output": result["summary"],
                    "file_path": result["path"],
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "action_taken": "Summarization failed",
                    "output": result["message"],
                    "file_path": None,
                    "success": False,
                    "error": result["message"]
                }
        
        elif intent == "web_search":
            print(f"Searching the web...")
            result = search_web(raw_text, model=model)
            
            if result["success"]:
                return {
                    "action_taken": "Information retrieved",
                    "output": result["results"],
                    "file_path": None,
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "action_taken": "Search failed",
                    "output": result["results"],
                    "file_path": None,
                    "success": False,
                    "error": result["message"]
                }
        
        elif intent == "chat":
            print(f"Generating chat response...")
            # Use Ollama for general chat with shorter, faster responses
            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Provide clear, concise responses. Keep answers brief unless asked for details."},
                    {"role": "user", "content": raw_text}
                ],
                options={
                    "num_predict": 200,  # Limit response length for speed
                    "temperature": 0.7
                }
            )
            
            chat_response = response.get("message", {}).get("content", "I'm here to help!")
            
            return {
                "action_taken": "Generated chat response",
                "output": chat_response,
                "file_path": None,
                "success": True,
                "error": None
            }
        
        else:
            return {
                "action_taken": "Unknown intent",
                "output": f"I'm not sure how to handle the intent: {intent}",
                "file_path": None,
                "success": False,
                "error": f"Unknown intent: {intent}"
            }
    
    except ollama.ResponseError as e:
        return {
            "action_taken": "Ollama error",
            "output": f"Ollama is not responding. Please ensure Ollama is running and the model '{model}' is available.",
            "file_path": None,
            "success": False,
            "error": f"Ollama error: {str(e)}"
        }
    
    except Exception as e:
        return {
            "action_taken": "Execution failed",
            "output": f"An error occurred: {str(e)}",
            "file_path": None,
            "success": False,
            "error": str(e)
        }


def handle_compound_intent(intent_data: Dict, model: str = "phi3") -> Dict:
    """
    Handle compound intents (e.g., "summarize AND save to file").
    
    Args:
        intent_data: Intent classification result
        model: Ollama model to use
        
    Returns:
        Dict with combined results from multiple actions
    """
    # Check if this is a compound intent
    raw_text = intent_data.get("raw_text", "").lower()
    has_save = "save" in raw_text or "write to" in raw_text
    has_summarize = "summarize" in raw_text or "summary" in raw_text
    
    if has_summarize and has_save:
        # Execute summarize with file save
        target_filename = intent_data.get("target_filename", "summary.txt")
        result = summarize(
            text=intent_data.get("raw_text"),
            save_to_file=target_filename,
            model=model
        )
        
        return {
            "action_taken": f"Summarized text and saved to '{target_filename}'",
            "output": result.get("summary"),
            "file_path": result.get("path"),
            "success": result.get("success"),
            "error": result.get("message") if not result.get("success") else None
        }
    
    # Otherwise, use standard single-intent execution
    return _execute_intent(intent_data, model=model)
