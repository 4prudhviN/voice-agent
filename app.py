"""
Voice-Controlled Local AI Agent - Main Gradio UI
"""
import gradio as gr
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.orchestrator import run_agent, run_agent_from_text
from intent.classifier import test_ollama_connection
import ollama


def get_available_models():
    """Get list of available Ollama models."""
    try:
        models = ollama.list()
        model_names = [m.get("name", "").split(":")[0] for m in models.get("models", [])]
        # Remove duplicates and empty strings
        model_names = list(set([m for m in model_names if m]))
        
        if not model_names:
            return ["phi3"]  # Default fallback
        
        return model_names
    except:
        return ["phi3"]  # Default fallback


# Session history storage
session_history = []


def process_audio(audio_path, model_choice):
    """Process audio input through the agent pipeline."""
    if not audio_path:
        return (
            "No audio provided",
            "N/A",
            "No action taken",
            "",
            "",
            "❌ Error: No audio file",
            get_history_df()
        )
    
    try:
        # Run the agent
        result = run_agent(audio_path, model=model_choice)
        
        # Extract results
        transcription = result.get("transcription", "")
        intent = result.get("intent", "unknown")
        action_taken = result.get("action_taken", "")
        output = result.get("output", "")
        file_path = result.get("file_path", "") or "No file created"
        success = result.get("success", False)
        error = result.get("error")
        
        # Status message
        if success:
            status = f"✅ Success: {action_taken}"
        else:
            status = f"❌ Error: {error or 'Unknown error'}"
        
        # Add to history
        add_to_history(intent, action_taken, file_path)
        
        return (
            transcription,
            intent,
            action_taken,
            output,
            file_path,
            status,
            get_history_df()
        )
        
    except Exception as e:
        error_msg = f"Pipeline error: {str(e)}"
        return (
            error_msg,
            "error",
            "Failed",
            "",
            "",
            f"❌ Error: {error_msg}",
            get_history_df()
        )


def process_text(text_input, model_choice):
    """Process text input through the agent pipeline."""
    if not text_input or not text_input.strip():
        return (
            "No text provided",
            "N/A",
            "No action taken",
            "",
            "",
            "❌ Error: No text input",
            get_history_df()
        )
    
    try:
        # Run the agent
        result = run_agent_from_text(text_input, model=model_choice)
        
        # Extract results
        transcription = result.get("transcription", "")
        intent = result.get("intent", "unknown")
        action_taken = result.get("action_taken", "")
        output = result.get("output", "")
        file_path = result.get("file_path", "") or "No file created"
        success = result.get("success", False)
        error = result.get("error")
        
        # Status message
        if success:
            status = f"✅ Success: {action_taken}"
        else:
            status = f"❌ Error: {error or 'Unknown error'}"
        
        # Add to history
        add_to_history(intent, action_taken, file_path)
        
        return (
            transcription,
            intent,
            action_taken,
            output,
            file_path,
            status,
            get_history_df()
        )
        
    except Exception as e:
        error_msg = f"Pipeline error: {str(e)}"
        return (
            error_msg,
            "error",
            "Failed",
            "",
            "",
            f"❌ Error: {error_msg}",
            get_history_df()
        )


def add_to_history(intent, action, file_path):
    """Add an entry to the session history."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_created = "Yes" if file_path and file_path != "No file created" else "No"
    
    session_history.append({
        "Timestamp": timestamp,
        "Intent": intent,
        "Action": action,
        "File Created": file_created
    })


def get_history_df():
    """Get session history as a DataFrame."""
    if not session_history:
        return pd.DataFrame(columns=["Timestamp", "Intent", "Action", "File Created"])
    return pd.DataFrame(session_history)


def clear_history():
    """Clear the session history."""
    session_history.clear()
    return get_history_df()


def check_ollama_status(model_choice):
    """Check if Ollama is running and model is available."""
    result = test_ollama_connection(model=model_choice)
    
    if result["success"]:
        return f"✅ {result['message']}\n\nAvailable models: {', '.join(result['available_models'])}"
    else:
        return f"❌ {result['message']}\n\nPlease ensure Ollama is running and the model is pulled:\n  ollama pull {model_choice}"


# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="Voice-Controlled Local AI Agent") as app:
    
    # Header
    gr.Markdown("""
    # 🎙️ Voice-Controlled Local AI Agent
    ### Powered by Whisper + Ollama | Speak or upload audio to execute AI actions
    
    This system transcribes your voice, understands your intent, and executes actions locally using AI.
    """)
    
    # Model selection
    with gr.Row():
        available_models = get_available_models()
        default_model = "phi3" if "phi3" in available_models else available_models[0]
        
        model_selector = gr.Dropdown(
            choices=available_models,
            value=default_model,
            label="🤖 Select Ollama Model",
            info="Choose the LLM model for intent classification and generation"
        )
        ollama_status_btn = gr.Button("🔍 Check Ollama Status", size="sm")
    
    ollama_status_output = gr.Textbox(label="Ollama Status", interactive=False, visible=False)
    
    # Main tabs
    with gr.Tabs():
        # Tab 1: Audio Input
        with gr.Tab("🎤 Audio Input"):
            audio_input = gr.Audio(
                sources=["microphone", "upload"],
                type="filepath",
                label="Speak or Upload Audio"
            )
            audio_submit_btn = gr.Button("▶ Run Agent", variant="primary", size="lg")
            
            gr.Markdown("""
            **Examples:**
            - "Write a Python function to calculate fibonacci numbers"
            - "Create a file called notes.txt with my meeting notes"
            - "Summarize this text and save it to summary.txt"
            """)
        
        # Tab 2: Text Input (Debug)
        with gr.Tab("💬 Text Input (Debug)"):
            text_input = gr.Textbox(
                label="Type your command directly",
                placeholder="e.g. Write a Python function to sort a list",
                lines=3
            )
            text_submit_btn = gr.Button("▶ Run Agent", variant="primary", size="lg")
            
            gr.Markdown("""
            **Supported Intents:**
            - **write_code**: Generate code in any language
            - **create_file**: Create a file with content
            - **summarize**: Summarize text (optionally save to file)
            - **chat**: General conversation
            """)
    
    # Results Section
    gr.Markdown("---")
    gr.Markdown("## 📊 Results")
    
    with gr.Row():
        # Left column
        with gr.Column():
            transcription_output = gr.Textbox(
                label="📝 Transcription",
                interactive=False,
                lines=3
            )
            intent_output = gr.Textbox(
                label="🎯 Detected Intent",
                interactive=False
            )
            action_output = gr.Textbox(
                label="💡 Action Taken",
                interactive=False
            )
        
        # Right column
        with gr.Column():
            code_output = gr.Code(
                label="📄 Output / Generated Code",
                language=None,
                interactive=False,
                lines=10
            )
            filepath_output = gr.Textbox(
                label="📁 Saved File Path",
                interactive=False
            )
            status_output = gr.Textbox(
                label="✅ Status",
                interactive=False
            )
    
    # Session History
    gr.Markdown("---")
    gr.Markdown("## 📜 Session History")
    
    with gr.Row():
        history_df = gr.Dataframe(
            headers=["Timestamp", "Intent", "Action", "File Created"],
            datatype=["str", "str", "str", "str"],
            label="Action History",
            interactive=False
        )
    
    with gr.Row():
        clear_history_btn = gr.Button("🗑️ Clear History", size="sm")
    
    # Event handlers
    audio_submit_btn.click(
        fn=process_audio,
        inputs=[audio_input, model_selector],
        outputs=[
            transcription_output,
            intent_output,
            action_output,
            code_output,
            filepath_output,
            status_output,
            history_df
        ]
    )
    
    text_submit_btn.click(
        fn=process_text,
        inputs=[text_input, model_selector],
        outputs=[
            transcription_output,
            intent_output,
            action_output,
            code_output,
            filepath_output,
            status_output,
            history_df
        ]
    )
    
    clear_history_btn.click(
        fn=clear_history,
        outputs=[history_df]
    )
    
    ollama_status_btn.click(
        fn=check_ollama_status,
        inputs=[model_selector],
        outputs=[ollama_status_output]
    ).then(
        fn=lambda: gr.update(visible=True),
        outputs=[ollama_status_output]
    )
    
    # Footer
    gr.Markdown("""
    ---
    ### 🔒 Safety Notice
    All file operations are restricted to the `./output/` directory for security.
    
    ### 💡 Tips
    - Ensure Ollama is running: `ollama serve`
    - Pull required models: `ollama pull llama3`
    - Speak clearly for best transcription results
    - Check Ollama status if you encounter errors
    """)


if __name__ == "__main__":  
    # Ensure output directory exists
    Path("output").mkdir(exist_ok=True)
    
    # Setup ffmpeg
    print("\n" + "="*60)
    print("🎙️  Voice-Controlled Local AI Agent")
    print("="*60)
    
    try:
        from utils.ffmpeg_setup import setup_ffmpeg
        print("\nChecking ffmpeg...")
        if not setup_ffmpeg():
            print("\n⚠️  Warning: ffmpeg not available")
            print("Audio transcription will not work without ffmpeg")
            print("You can still use text input!")
    except Exception as e:
        print(f"\n⚠️  Could not setup ffmpeg: {e}")
        print("Audio transcription may not work")
    
    # Launch the app
    print("\nStarting Gradio interface...")
    print("Make sure Ollama is running: ollama serve")
    print("="*60 + "\n")
    
    app.launch(
        server_name="127.0.0.1",
        server_port=8080,
        share=True,  # Creates public HTTPS link
        show_error=True,
        ssl_verify=False
    )
