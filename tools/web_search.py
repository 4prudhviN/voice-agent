"""
Web search tool for getting live information.
"""
import requests
from typing import Dict, Optional
import ollama


def search_web(query: str, model: str = "phi3") -> Dict:
    """
    Search the web for current information using LLM to generate response.
    
    Args:
        query: Search query
        model: LLM model to use for generating response
        
    Returns:
        Dict with keys: success, results, message
    """
    try:
        # Use LLM to provide information about the query
        # Note: This won't have real-time data, but will provide general knowledge
        prompt = f"""The user is asking about: {query}

Please provide helpful information about this topic. If this is about current events, sports scores, or live updates, explain that you don't have access to real-time data, but provide general information about the topic.

Be concise and helpful."""

        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Provide accurate information based on your knowledge."},
                {"role": "user", "content": prompt}
            ]
        )
        
        result_text = response.get("message", {}).get("content", "Unable to generate response.")
        
        return {
            "success": True,
            "results": result_text,
            "message": f"Search completed for: {query}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "results": f"Unable to process search query. Error: {str(e)}",
            "message": f"Error during search: {str(e)}"
        }


def get_ipl_updates(model: str = "phi3") -> Dict:
    """
    Get IPL information.
    
    Returns:
        Dict with keys: success, updates, message
    """
    try:
        prompt = """Provide information about the Indian Premier League (IPL) cricket tournament. Include:
- What IPL is
- Current season information (if known)
- Popular teams
- Format of the tournament

Note: Explain that you don't have access to live scores or current match updates."""

        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": "You are a cricket expert. Provide helpful information about IPL."},
                {"role": "user", "content": prompt}
            ]
        )
        
        result_text = response.get("message", {}).get("content", "Unable to get IPL information.")
        
        return {
            "success": True,
            "updates": result_text,
            "message": "IPL information retrieved"
        }
            
    except Exception as e:
        return {
            "success": False,
            "updates": f"Unable to get IPL information. Error: {str(e)}",
            "message": f"Error getting IPL updates: {str(e)}"
        }
