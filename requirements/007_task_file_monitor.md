
# Task 007 – Automatic Document Monitoring and Re-indexing

## 1. Summary

This task implements a background monitoring system to automatically detect when new or modified PDF files are added to the `/documents` folder. When a change is detected, the system will re-run the ingestion, chunking, embedding, and vector indexing processes to ensure the knowledge base stays up to date.

## 2. Project Setup

### Files to be Created
- `utils/file_monitor.py`: Script or module to handle directory watching and trigger updates

### Dependencies
To be added in `requirements.txt`:
```
watchdog
```

## 3. Implementation

1. Use the `watchdog` library to watch the `/documents` folder for file creation or modification events.
2. Maintain a file state cache (e.g. based on MD5 hash or last modified time) to avoid redundant processing.
3. On detection of new or changed files:
   - Run `load_and_chunk_pdfs()` from `pdf_loader.py`
   - Run `embed_chunks()` and re-index with FAISS from `vector_store.py`
4. Log file events and ingestion outcomes.
5. Allow the monitor to run in a background thread or as a separate process.

## 4. Integration

This task connects to and automates:
- Task 001: PDF ingestion
- Task 002: Embedding and vector indexing

It ensures the semantic search and QA pipeline always operates on the most up-to-date documents without manual restarts.

## 5. Testing

### Test Plan

- Add a new PDF file to `/documents` and confirm:
  - It is detected and processed
  - New vectors are added to the FAISS index
- Modify an existing PDF and confirm it is reprocessed
- Test error cases:
  - Unsupported or corrupted PDFs
  - Duplicate files or unchanged timestamps
- Confirm processing is not triggered unnecessarily on read-only access
