# Task 011 – Build LangGraph Assistant Flow

## 1. Summary

This task introduces a LangGraph-based assistant flow that intelligently routes user queries to the appropriate chain based on intent: either a semantic question (Q&A) or a summarization request. The assistant will maintain multi-turn context, remembering the last 5 Q&A pairs. If the conversation exceeds 5 Q&A, older turns are summarized by GPT-4.1-nano and the summary is included as part of the context. The assistant returns formatted, structured responses including source metadata and supports follow-up questions and long-session continuity.

## 2. Project Setup

### Files to be Created/Modified
- `assistant/langgraph_flow.py`
- `assistant/query_classifier.py`

### Dependencies
Add to `requirements.txt` if not already present:
```
langgraph
langchain
```

## 3. Implementation

1. **Query Intent Classification**
   - Build a basic keyword-based classifier (`query_classifier.py`)
   - Classify into two categories: `qa` or `summarize`

2. **LangGraph Flow Definition**
   - Create a graph using LangGraph
   - Define nodes for:
     - Intent detection
     - QA chain (Task 003 or similar)
     - Summarization chain (Task 010)

3. **State and Memory Handling**
   - Pass multi-turn history as part of state
   - Remember the last 5 Q&A pairs (user question and assistant answer)
   - If the conversation exceeds 5 Q&A, summarize older turns using GPT-4.1-nano and include the summary as part of the context for subsequent answers
   - This enables follow-up questions and long-session memory within a session

4. **Output Formatting**
   - Wrap responses in unified schema:
     ```json
     {
       "type": "answer" or "summary",
       "content": "...",
       "sources": [
         {"document": "filename.pdf", "page": 3}
       ]
     }
     ```

5. **Flow Entry Point**
   - Create callable function `run_assistant(user_query, history)` returning structured output

## 4. Integration

- Called by Gradio chat interface (Task 012)
- Utilizes summarization chain from Task 010
- Uses retriever and generator from Task 003

## 5. Testing

### Test Plan

- Unit test `classify_intent()` with various questions:
  - “What is the penalty for non-compliance?”
  - “Summarize page 3–6 of this document”
- Simulate assistant query with and without history
- Validate:
  - Correct routing to Q&A or summarization
  - History is passed correctly
  - Citations returned for Q&A
  - Summary result is coherent and accurate
  - Long conversations: verify that after 5 Q&A, older turns are summarized and included as context, and follow-up questions referencing earlier answers are handled appropriately
