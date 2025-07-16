
# Task 004 – Answer Generator using LLM

## 1. Summary

This task implements a retrieval-augmented generation (RAG) pipeline that uses the semantically retrieved document chunks (from Task 003) and generates a natural language answer using an LLM (OpenAI GPT-4). It enhances user experience by providing concise answers and citing document sources (file name and page number).

## 2. Project Setup

### Files to be Created
- `qa/answer_generator.py`: builds the LLM-based answer engine using OpenAI.

### Dependencies
Already covered:
```
openai
```

Ensure `OPENAI_API_KEY` is available in your environment.

## 3. Implementation

1. Implement `generate_answer(query: str, retrieved_chunks: List[Dict]) -> str`.
2. Format the context from retrieved chunks into a prompt:
   - Include both content and metadata (file name, page number).
3. Send the formatted prompt to OpenAI GPT-4 API using `chat/completions`.
4. Parse the response and return the generated answer.
5. Ensure citation formatting is consistent (e.g., "Source: policy_guide.pdf, page 3").

## 4. Integration

This module:
- Consumes query and retrieved chunks from **Task 003**
- Will be invoked from the user interface in **Task 005**
- Finalizes the RAG loop (retrieve + generate)

Ensure output is human-readable and safe for internal use.

## 5. Testing

### Test Plan

- Use known queries with expected answers from your test PDFs
- Validate:
  - Clarity and correctness of answers
  - Proper citation (filename and page number)
- Handle failure cases:
  - No retrieved chunks → return "No information found."
  - OpenAI errors → graceful fallback or retry logic
- Manually verify Indonesian and English prompt effectiveness
