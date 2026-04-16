"""
Test script to verify all components are working correctly.
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("="*60)
print("Voice-Controlled AI Agent - Component Test")
print("="*60)

# Test 1: Check imports
print("\n[1/5] Testing imports...")
try:
    from stt.transcriber import transcribe
    from intent.classifier import classify_intent, test_ollama_connection
    from tools.file_ops import create_file, create_folder
    from tools.code_gen import generate_code
    from tools.summarizer import summarize
    from agent.orchestrator import run_agent_from_text
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Check output directory
print("\n[2/5] Checking output directory...")
try:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    print(f"✅ Output directory exists: {output_dir.absolute()}")
except Exception as e:
    print(f"❌ Output directory check failed: {e}")
    sys.exit(1)

# Test 3: Test Ollama connection
print("\n[3/5] Testing Ollama connection...")
try:
    result = test_ollama_connection("llama3")
    if result["success"]:
        print(f"✅ {result['message']}")
        print(f"   Available models: {', '.join(result['available_models'][:3])}...")
    else:
        print(f"⚠️  {result['message']}")
        print("   Make sure Ollama is running: ollama serve")
        print("   And model is pulled: ollama pull llama3")
except Exception as e:
    print(f"⚠️  Ollama connection test failed: {e}")
    print("   This is expected if Ollama is not running")

# Test 4: Test file operations
print("\n[4/5] Testing file operations...")
try:
    test_result = create_file("test_file.txt", "This is a test file.")
    if test_result["success"]:
        print(f"✅ File creation successful: {test_result['path']}")
    else:
        print(f"❌ File creation failed: {test_result['message']}")
except Exception as e:
    print(f"❌ File operations test failed: {e}")

# Test 5: Test intent classification (if Ollama is available)
print("\n[5/5] Testing intent classification...")
try:
    test_text = "Write a Python function to add two numbers"
    intent_result = classify_intent(test_text)
    print(f"✅ Intent classification successful")
    print(f"   Input: '{test_text}'")
    print(f"   Detected intent: {intent_result.get('intent')}")
    print(f"   Language: {intent_result.get('language')}")
except Exception as e:
    print(f"⚠️  Intent classification test failed: {e}")
    print("   This is expected if Ollama is not running")

# Summary
print("\n" + "="*60)
print("Component Test Complete")
print("="*60)
print("\nNext steps:")
print("1. Ensure Ollama is running: ollama serve")
print("2. Pull required model: ollama pull llama3")
print("3. Run the app: python app.py")
print("="*60)
