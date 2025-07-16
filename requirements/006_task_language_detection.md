
# Task 006 – Language Detection and Multilingual Handling

## 1. Summary

This task ensures that the system can handle user queries and document content in both English and Indonesian. It introduces a lightweight language detection step that identifies the language of user input and optionally applies preprocessing steps to optimize embedding and answer generation.

## 2. Project Setup

### Files to be Created
- `utils/language_detect.py`: a utility module for detecting the language of a given text.

### Dependencies
To be added in `requirements.txt` if not yet present:
```
langdetect
```

No external APIs are required.

## 3. Implementation

1. Create a utility function `detect_language(text: str) -> str` that returns `'id'` or `'en'`.
2. Use `langdetect` or `fasttext` to identify language of:
   - User queries
   - Document chunks (optional tagging)
3. Ensure:
   - English and Indonesian queries are treated the same by the retriever and LLM pipeline.
   - Optionally log or display the detected language for debug.

## 4. Integration

This detection step can be used in:
- Task 003: to validate or adjust query processing
- Task 004: to handle language-specific prompt formatting (if needed)
- Task 005: UI display of language detection or warnings

No downstream component depends on this task, but it ensures quality in multilingual retrieval and QA.

## 5. Testing

### Test Plan

- Feed known English and Indonesian questions such as:
  - "What are the AI principles recommended by OJK?"
  - "Apa saja prinsip AI yang bertanggung jawab menurut OJK?"
- Validate that `detect_language()` returns the correct ISO code (`'en'` or `'id'`)
- Run the QA pipeline and verify:
  - English queries get correct embeddings and answers
  - Indonesian queries work equally well
- Handle:
  - Empty queries (should return `'unknown'` or safe fallback)
  - Mixed-language input (choose dominant language)
