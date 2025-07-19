# Task 012 – Redesign Chat UI with Gradio

## 1. Summary

This task updates the chat interface using Gradio's `ChatInterface` or `Blocks`. It enables multi-turn interactions, displays chat history, and accepts PDF uploads. This task is purely frontend-focused and does not yet invoke LangGraph or model inference. It also introduces token usage tracking in the UI development phase to benchmark cost and performance.

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

3. **Token Usage Monitoring**
   - Use `langchain.callbacks.get_openai_callback()`
   - Print tokens and cost per user query
   - persist token log to a logs file alongside the prompt

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
- Log printed token usage per mock query
- Confirm interface does not crash on invalid input
- Validate UI layout is production-ready
