# 🏗️ System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│                     (Gradio Web UI)                          │
│  ┌──────────────┐              ┌──────────────┐            │
│  │ Audio Input  │              │ Text Input   │            │
│  │ 🎤 Mic/File  │              │ ✏️ Direct    │            │
│  └──────┬───────┘              └──────┬───────┘            │
└─────────┼──────────────────────────────┼──────────────────┘
          │                              │
          ▼                              │
┌─────────────────────┐                 │
│   STT MODULE        │                 │
│  (Whisper Local)    │                 │
│                     │                 │
│  - Load audio       │                 │
│  - Transcribe       │                 │
│  - Return text      │                 │
└─────────┬───────────┘                 │
          │                             │
          └─────────────┬───────────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │  INTENT CLASSIFIER      │
          │  (Ollama LLM)           │
          │                         │
          │  - Analyze text         │
          │  - Extract intent       │
          │  - Parse parameters     │
          │  - Return JSON          │
          └────────────┬────────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │    ORCHESTRATOR         │
          │  (Pipeline Manager)     │
          │                         │
          │  - Route intent         │
          │  - Call tool            │
          │  - Handle errors        │
          │  - Format response      │
          └────────────┬────────────┘
                       │
        ┌──────────────┼──────────────┬──────────────┐
        │              │              │              │
        ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ CODE GEN    │ │ FILE OPS    │ │ SUMMARIZER  │ │ CHAT        │
│             │ │             │ │             │ │             │
│ - Generate  │ │ - Create    │ │ - Summarize │ │ - Respond   │
│ - Save code │ │ - Sanitize  │ │ - Save text │ │ - Converse  │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │               │
       └───────────────┴───────────────┴───────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  OUTPUT FOLDER  │
              │  (./output/)    │
              │                 │
              │  - Safe storage │
              │  - Generated    │
              │    files        │
              └─────────────────┘
```

## Data Flow

### Audio Input Flow

```
User speaks → Microphone → Audio file
                              │
                              ▼
                    Whisper transcribe()
                              │
                              ▼
                         Text string
                              │
                              ▼
                    [Continue to Intent Flow]
```

### Text Input Flow

```
User types → Text input → Text string
                             │
                             ▼
                [Continue to Intent Flow]
```

### Intent Classification Flow

```
Text string
    │
    ▼
Ollama LLM (with system prompt)
    │
    ▼
JSON response:
{
  "intent": "write_code",
  "target_filename": "sort.py",
  "language": "python",
  "content_hint": "sorting function",
  "raw_text": "..."
}
    │
    ▼
Parse and validate
    │
    ▼
Intent dict
```

### Tool Execution Flow

```
Intent dict
    │
    ├─ intent == "write_code" ──→ code_gen.generate_code()
    │                                      │
    │                                      ▼
    │                              Ollama generates code
    │                                      │
    │                                      ▼
    │                              Save to output/file.ext
    │
    ├─ intent == "create_file" ──→ file_ops.create_file()
    │                                      │
    │                                      ▼
    │                              Sanitize filename
    │                                      │
    │                                      ▼
    │                              Write to output/file
    │
    ├─ intent == "summarize" ────→ summarizer.summarize()
    │                                      │
    │                                      ▼
    │                              Ollama generates summary
    │                                      │
    │                                      ▼
    │                              Optionally save to file
    │
    └─ intent == "chat" ─────────→ Ollama chat response
                                           │
                                           ▼
                                   Return response text
```

## Module Dependencies

```
app.py
  │
  ├─→ agent.orchestrator
  │     │
  │     ├─→ stt.transcriber
  │     │     └─→ whisper (external)
  │     │
  │     ├─→ intent.classifier
  │     │     └─→ ollama (external)
  │     │
  │     └─→ tools.*
  │           ├─→ tools.code_gen
  │           │     ├─→ ollama (external)
  │           │     └─→ tools.file_ops
  │           │
  │           ├─→ tools.file_ops
  │           │     └─→ pathlib, os
  │           │
  │           └─→ tools.summarizer
  │                 ├─→ ollama (external)
  │                 └─→ tools.file_ops
  │
  └─→ gradio (external)
```

## Component Responsibilities

### 1. Gradio UI (app.py)
**Responsibility**: User interface and interaction
- Render web interface
- Handle user input (audio/text)
- Display results
- Manage session state
- Track history

**Inputs**: User audio/text, model selection
**Outputs**: Formatted results, status messages

### 2. STT Module (stt/transcriber.py)
**Responsibility**: Audio to text conversion
- Load audio files
- Validate format
- Transcribe using Whisper
- Handle errors

**Inputs**: Audio file path
**Outputs**: Transcribed text or error message

### 3. Intent Classifier (intent/classifier.py)
**Responsibility**: Understand user intent
- Send text to LLM
- Parse JSON response
- Validate intent
- Fallback to keywords

**Inputs**: Text string
**Outputs**: Intent dict with metadata

### 4. Orchestrator (agent/orchestrator.py)
**Responsibility**: Pipeline coordination
- Coordinate full pipeline
- Route intents to tools
- Handle errors gracefully
- Format unified response

**Inputs**: Audio path or text
**Outputs**: Unified result dict

### 5. Tools (tools/*)
**Responsibility**: Execute actions

**file_ops.py**:
- Create files/folders
- Sanitize paths
- Validate safety

**code_gen.py**:
- Generate code via LLM
- Detect language
- Save with correct extension

**summarizer.py**:
- Generate summaries via LLM
- Format output
- Optionally save

**Inputs**: Varies by tool
**Outputs**: Result dict with success/error

## Error Handling Strategy

```
┌─────────────────┐
│  User Action    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Try Block      │
│  - Execute      │
│  - Process      │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Success?│
    └────┬────┘
         │
    ┌────┴────┐
    │   Yes   │   No
    │         │   │
    ▼         ▼   ▼
┌─────────┐ ┌─────────────┐
│ Return  │ │ Catch Error │
│ Success │ │             │
│ Result  │ │ - Log       │
└─────────┘ │ - Format    │
            │ - Return    │
            │   Error     │
            └─────────────┘
                  │
                  ▼
            ┌─────────────┐
            │ Graceful    │
            │ Degradation │
            │             │
            │ - Fallback  │
            │ - User msg  │
            └─────────────┘
```

## Security Architecture

```
┌──────────────────────────────────────┐
│         User Input                    │
│  (Potentially malicious)              │
└─────────────┬────────────────────────┘
              │
              ▼
┌──────────────────────────────────────┐
│      Input Validation                 │
│  - Check file format                  │
│  - Validate text length               │
│  - Sanitize special chars             │
└─────────────┬────────────────────────┘
              │
              ▼
┌──────────────────────────────────────┐
│      Path Sanitization                │
│  - Extract basename only              │
│  - Remove .. sequences                │
│  - Replace / and \                    │
│  - Validate not empty                 │
└─────────────┬────────────────────────┘
              │
              ▼
┌──────────────────────────────────────┐
│      Output Restriction               │
│  - Force ./output/ prefix             │
│  - Prevent path traversal             │
│  - Check directory exists             │
└─────────────┬────────────────────────┘
              │
              ▼
┌──────────────────────────────────────┐
│      Safe File Operation              │
│  - Write to validated path            │
│  - Handle permissions                 │
│  - Catch exceptions                   │
└──────────────────────────────────────┘
```

## State Management

```
┌─────────────────────────────────────┐
│        Gradio Session State          │
│                                      │
│  session_history = []                │
│    │                                 │
│    ├─ Timestamp                      │
│    ├─ Intent                         │
│    ├─ Action                         │
│    └─ File Created                   │
│                                      │
│  Updated on each agent run           │
│  Displayed in history table          │
│  Cleared on user request             │
└─────────────────────────────────────┘
```

## Concurrency Model

```
Single-threaded execution:
1. User submits request
2. UI blocks (shows processing)
3. Pipeline executes sequentially
4. Results returned
5. UI updates

No concurrent requests handled
(Gradio default behavior)
```

## External Dependencies

```
┌──────────────────┐
│  Whisper Model   │  (Local, ~/.cache/whisper/)
│  - base.pt       │
│  - ~140MB        │
└──────────────────┘

┌──────────────────┐
│  Ollama Service  │  (Local, port 11434)
│  - llama3        │
│  - mistral       │
│  - ~4-7GB each   │
└──────────────────┘

┌──────────────────┐
│  ffmpeg          │  (System binary)
│  - Audio codec   │
└──────────────────┘
```

## Performance Bottlenecks

```
1. Whisper Transcription
   - CPU/GPU intensive
   - ~2-5s for 10s audio
   - Mitigation: Use GPU, smaller model

2. LLM Inference (Ollama)
   - RAM intensive
   - ~1-10s per call
   - Mitigation: Smaller model, GPU

3. File I/O
   - Minimal impact
   - <100ms typically
   - Mitigation: SSD storage
```

## Scalability Considerations

### Current Limitations
- Single user at a time
- No request queuing
- No caching
- No distributed processing

### Potential Improvements
- Add request queue
- Implement caching for common requests
- Use async processing
- Add load balancing for multiple users

## Deployment Architecture

```
┌─────────────────────────────────────┐
│         Local Machine                │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Ollama Service                │ │
│  │  (Background process)          │ │
│  │  Port: 11434                   │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Voice Agent App               │ │
│  │  (Python process)              │ │
│  │  Port: 7860                    │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Web Browser                   │ │
│  │  http://localhost:7860         │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

This architecture provides a clean separation of concerns, robust error handling, and secure file operations while maintaining simplicity and ease of understanding.
