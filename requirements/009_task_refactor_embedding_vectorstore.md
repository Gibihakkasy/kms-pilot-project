
# Task 009 – Refactor Embedding and Vector Store

## 1. Summary

This task handles embedding the chunked documents and storing them in a persistent FAISS vector database. It replaces OpenAI embeddings with a plug-and-play architecture that also supports HuggingFace embeddings (e.g., BGE). The module will be refactored to match the new folder structure.

## 2. Project Setup

### Files to be Created/Modified
- `vectorstore/faiss_store.py`

### Dependencies
To be added in `requirements.txt`:
```
faiss-cpu
sentence-transformers
langchain
```

## 3. Implementation

1. Import the embedding model:
   - Use `HuggingFaceEmbeddings` (e.g. `"BAAI/bge-base-id"` or fallback to `OpenAIEmbeddings`)
   - Normalize vectors with `encode_kwargs={"normalize_embeddings": True}`

2. Implement two functions:
   - `create_and_save_vector_store(docs)`
     - Build FAISS index from list of `Document` objects
     - Persist to `embeddings/faiss_index/`
   - `load_vector_store()`
     - Load FAISS index and return a retriever

3. Save files to:
   ```
   embeddings/faiss_index/
   ├── index.faiss
   └── index.pkl
   ```

4. Update code to align with new folder structure:
   - Place logic in `vectorstore/faiss_store.py`
   - Adjust imports in `app.py` and any utilities that rely on vector retrieval

## 4. Integration

- Consumes chunked documents from Task 008
- Required by:
  - Task 010: LangChain QA and summarization chains
  - Task 011: LangGraph flow
  - Task 007: Automatic re-indexing

## 5. Testing

### Test Plan

- Run ingestion to produce `Document` objects
- Embed and persist them using `create_and_save_vector_store()`
- Reload using `load_vector_store()` and perform a test query
- Validate:
  - Embedding shape and count match input chunks
  - Metadata is retained and query returns the correct documents
- Edge cases:
  - Empty doc list
  - Corrupt index folder
