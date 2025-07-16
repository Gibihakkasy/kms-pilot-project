
# Task 002 – Embedding and Vector Storage

## 1. Summary

This task builds the semantic embedding layer for the KMS system. It will convert the chunked PDF text (from Task 001) into vector embeddings using OpenAI’s `text-embedding-3-large` model and store them in a local FAISS vector database. This enables fast and semantically aware document retrieval in later stages.

## 2. Project Setup

### Files to be Created
- `embeddings/vector_store.py`: Handles embedding generation and FAISS storage.

### Directory Required
- None (reuse chunks from memory or from JSON dump from Task 001)

### Dependencies
To be added in `requirements.txt`:
```
faiss-cpu
openai
```

You will also need an OpenAI API key set in your environment.

## 3. Implementation

1. Define `embed_chunks(chunks: List[Dict[str, Any]]) -> None` in `vector_store.py`.
2. Use OpenAI’s embedding API (`text-embedding-3-large`) to generate vectors.
3. Store vectors in FAISS index, along with corresponding metadata.
4. Save the FAISS index locally (e.g., `vector_store/index.faiss`).
5. Optionally, store metadata separately as JSON for retrieval during search.

## 4. Integration

This task consumes output from **Task 001** and is essential for:
- **Task 003**: Semantic search and chunk retrieval
- **Task 004**: Retrieval-augmented generation (RAG) pipeline for QA

The chunk structure must remain consistent for metadata lookups.

## 5. Testing

### Test Plan

- Use sample chunks (5–10 entries) from Task 001 output
- Ensure all vectors are created and stored successfully
- Test FAISS index creation and loading:
  - `faiss.read_index()`
  - Query with dummy vector and check retrieval
- Validate that metadata matches the corresponding embedding entry
- Ensure embedding runs without crashing on Indonesian and English text
