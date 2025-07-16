# Task 001 – PDF Loader and Text Chunking

## 1. Summary

This task focuses on building the document ingestion pipeline for the KMS prototype. The goal is to extract text from PDF files stored in a local directory, chunk the extracted text into manageable segments, and enrich each chunk with metadata (file name, page number, chunk ID). These structured chunks will serve as the base input for semantic embedding and retrieval in subsequent tasks.

## 2. Project Setup

### Files to be Created
- `ingest/pdf_loader.py`: contains the main function to load and chunk PDF files.

### Directory Required
- `documents/`: the folder where input PDF files will be placed for ingestion.

### Dependencies
To be added in `requirements.txt`:
```
pymupdf
```

No external services or APIs are required for this task.

## 3. Implementation

1. Create `load_and_chunk_pdfs(pdf_folder: str)` function in `ingest/pdf_loader.py`.
2. Use PyMuPDF (`fitz`) to:
   - Read all `.pdf` files in the given folder.
   - Extract text from each page, skip blank pages.
3. Chunk each page’s text into smaller blocks (~300–500 tokens).
4. For each chunk, return a dictionary containing:
   - `text`: the chunk content.
   - `metadata`: includes `file_name`, `page_number`, and a generated `chunk_id`.
5. Return a list of all extracted chunks.

## 4. Integration

This task produces the text chunks that will be passed to:
- **Task 002**: Embedding and vector storage using FAISS.
- **Task 004**: LLM-based QA that depends on chunk-level granularity for source citation.

Ensure the format is consistent for downstream consumption.

## 5. Testing

### Test Plan

- **Functional Tests**:
  - Use sample PDFs (1 short, 1 long, 1 Indonesian, 1 empty) in the `documents/` folder.
  - Confirm chunk count matches content length.
  - Print chunk metadata and inspect accuracy.

- **Validation Cases**:
  - Empty `documents/` folder returns an empty list.
  - Corrupted or unreadable PDF is skipped without crashing.
  - Blank pages are ignored.
  - Metadata fields (`file_name`, `page_number`, `chunk_id`) are correctly populated.

- **Optional Output Inspection**:
  - Export chunk list as JSON for manual review.