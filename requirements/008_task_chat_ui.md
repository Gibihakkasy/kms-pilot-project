
# Task 008 – Assistant-Style Chat UI

## 1. Summary

This task upgrades the current Gradio interface to an assistant-style chat interface. Instead of a single-turn question and answer format, the system will support a chat conversation flow, showing the full message history and allowing follow-up questions. This creates a more natural user experience.

## 2. Project Setup

### Files to be Modified
- `app.py`: Update interface from standard input/output to conversational format

### Dependencies
Ensure the following is in `requirements.txt`:
```
gradio
```

No additional libraries are required if using Gradio's built-in `ChatInterface` or `Blocks`.

## 3. Implementation

1. Replace the static Gradio `Textbox` interface with `ChatInterface` or `Blocks`.
2. Display:
   - User messages
   - AI-generated responses (from retrieval + GPT pipeline)
3. Maintain message history across interactions.
4. On each message:
   - Embed the latest user query
   - Retrieve top chunks from FAISS
   - Generate a new response using GPT-4
   - Append to conversation history
5. Optionally implement:
   - Typing indicators
   - Message timestamps
   - Citations inline or as message footer

## 4. Integration

This task connects all major components:
- Retrieval and QA (Tasks 003–004)
- Display logic (Task 005)

It replaces the prior UI pattern and enhances usability for multi-turn scenarios, paving the way for future contextual memory handling.

## 5. Testing

### Test Plan

- Run full app and interact using:
  - English and Indonesian queries
  - Follow-up questions referencing earlier answers
- Confirm message flow and history is maintained
- Check:
  - Responses appear under user message
  - Source file names and page numbers are shown or cited
- Test edge cases:
  - Rapid user input
  - Invalid prompts
  - Long conversation threads
