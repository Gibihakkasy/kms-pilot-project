# Task 010 – Refactor Legal Summarization using Chat Model

## 1. Summary

This task improves the summarization capability of the system to produce high-quality, structured bullet-point summaries for legal and regulatory documents. It replaces the completion-based LLM with a chat-based model (e.g., GPT-4.1 via ChatOpenAI), and introduces a refined prompt designed for legal summarization. The summary output will be clearer, more contextual, and aligned with the semantics of regulation texts.

## 2. Project Setup

### Files to be Created/Modified
- `chains/summarization_refine_chain.py`
- `run_summarizer.py` (optional CLI test script)

### Dependencies
To be added in `requirements.txt`:
```
openai
langchain
```

## 3. Implementation

1. Create `summarization_refine_chain.py`:
   - Define `summarize_documents(llm, documents)` function
   - Use `load_summarize_chain(llm, chain_type="refine")`
   - Accept `ChatOpenAI` instance and structured prompt template

2. Design legal-specific prompt:
   - Structured bullet-point output by legal categories:
     - [Provision], [Obligation], [Restriction], [Penalty], [Reporting Requirement], [Other Notes]

3. Instantiate the model externally:
   ```python
   from langchain.chat_models import ChatOpenAI
   llm = ChatOpenAI(model_name="gpt-4.1", temperature=0)
   ```

4. Create optional CLI entrypoint:
   - `run_summarizer.py`
   - Accepts `--model`, `--file`, and prints output summary

## 4. Integration

- Uses chunked documents from Task 008
- Does not depend on vector store (unlike QA flow)
- Supports LangGraph flow integration in Task 011
- Supports UI response rendering in Task 012

## 5. Testing

### Test Plan

- Load sample BI/OJK regulation from `/documents/`
- Call `summarize_documents(llm, docs)` using GPT-4.1
- Validate summary contains:
  - Bullet points grouped under expected labels
  - No hallucination (e.g., about metadata like signature)
  - Real legal content extraction (titles, responsibilities, penalties)
- From the project root: python tests/run_summarizer.py --file documents/Peraturan\ BI\ No.\ 3-10-PBI-2001.pdf

- Edge cases:
  - Empty document list
  - Very short vs very long documents
  - Improper encoding or non-PDF documents
