
# Task 008 – Refactor Ingestion Using LangChain

## 1. Summary

This task refactors the document ingestion process using LangChain components. The goal is to load PDFs from the `/documents` folder, split them into context-aware chunks, and attach meaningful metadata to each chunk for traceable downstream processing.

## 2. Project Setup

### Files to be Created/Modified
- `ingest/pdf_ingester.py`

### Dependencies
To be added in `requirements.txt`:
```
langchain
pymupdf
```

## 3. Implementation

1. Load PDFs from the `/documents/` folder using `PyMuPDFLoader`.
2. For each document:
   - Apply `RecursiveCharacterTextSplitter`
     - Chunk size: 500 characters or tokens
     - Overlap: 100
     - Use sentence or paragraph-aware separators: `["\n\n", "\n", ".", " ", ""]`
3. Add metadata to each chunk:
   - `file_name`, `page_number`
   - (Optional) add `doc_title` or `language` if parsed

4. Output a list of LangChain `Document` objects with `page_content` and `metadata`.

## 4. Integration

- This output is used in:
  - Task 009: Embedding and vector store creation
  - Task 010: LangChain QA/Summarization chains
  - Task 013: Document summarization (partial)

## 5. Testing

### Test Plan

- Place 2–3 PDF files into `/documents`
- Run the ingestion module
- Check output:
  - Total number of chunks printed
  - Each chunk includes:
    - Reasonable text boundaries (not split mid-sentence)
    - `metadata` fields with `file_name` and `page_number`
- Edge cases:
  - Empty PDFs (should be skipped with warning)
  - Non-PDF files (should be ignored)
  - Duplicate files (should not break processing)
