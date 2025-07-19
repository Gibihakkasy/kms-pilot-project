# Task 012 – Redesign Chat UI with Gradio

## 1. Summary

This task updates the chat interface using Gradio's `ChatInterface` or `Blocks`. It enables multi-turn interactions, displays chat history, and accepts PDF uploads. This task is purely frontend-focused and does not yet invoke LangGraph or model inference. It also introduces comprehensive token usage tracking in the UI development phase to benchmark cost and performance.

## 2. Project Setup

### Files to be Created/Modified
- `app.py` (refactored)
- `ui/chat_interface.py`
- `utils/token_logger.py`

### Dependencies
To be added in `requirements.txt`:
```
gradio
langchain
openai
tiktoken
```

## 3. Implementation

1. **Refactor to Gradio ChatInterface**
   - Replace `gr.Interface` with `gr.ChatInterface` or `Blocks`
   - Display chat history and user/assistant roles
   - Support file upload (PDF or zip)

2. **Basic Input and Upload Flow**
   - Accept user queries and file uploads
   - Store uploaded files in `/documents/`
   - Do not invoke LangGraph or summarization yet

3. **Comprehensive Token Usage Monitoring**
   - Use `tiktoken` for accurate token counting across all LLM activities
   - Implement model-specific pricing (GPT-4, GPT-3.5-turbo, etc.) for accurate cost estimation
   - Track both input and output tokens for all LLM calls
   - Log token usage and costs for:
     - Document embedding (text-embedding-3-large)
     - Answer generation (GPT models)
     - Document summarization (refine chain)
     - Chat history summarization (for long conversations)
   - Persist comprehensive token logs to `logs/token_usage.log` with timestamps and activity types
   - Include model name, input/output tokens, and estimated cost per activity

4. **Frontend Polish**
   - Display messages in markdown
   - Show filename and upload status
   - Prepare slots for rendering model output in future tasks

## 4. Integration

- Backend logic is still mocked or stubbed (e.g., `return "Work in progress..."`)
- Model invocation will be implemented in Task 015

## 5. Testing

### Test Plan

- Confirm multi-turn chat renders correctly
- Upload PDF and confirm file appears in `/documents/`
- Log printed token usage per mock query with accurate pricing
- Confirm interface does not crash on invalid input
- Validate UI layout is production-ready
