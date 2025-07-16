# Task 003 – Semantic Search and Retriever

## 1. Summary

This task enables semantic document retrieval by implementing a search interface over the FAISS vector index built in Task 002. It takes a natural language query, converts it into an embedding using OpenAI, searches for the most relevant document chunks, and returns them for further processing or question-answering.

## 2. Project Setup

### Files to be Created
- `qa/retriever.py`: contains logic for vector search and retrieval.

### Dependencies
Already covered in Task 002:
```
faiss-cpu
openai
```

### Environment
Requires access to the FAISS index and metadata saved during Task 002.

## 3. Implementation

1. Implement `retrieve_chunks(query: str, k: int = 5) -> List[Dict]` in `retriever.py`.
2. Load FAISS index and metadata from disk.
3. Embed the user query using OpenAI `text-embedding-3-large`.
4. Use FAISS to search the top `k` nearest chunks.
5. Return the matching chunk data including text and metadata (file name, page number).

## 4. Integration

This task connects the vector database from **Task 002** to downstream QA in:
- **Task 004**: where these retrieved chunks are passed into GPT for answer generation.

It is also a prerequisite for enabling search from the Gradio UI in Task 005.

## 5. Testing

### Test Plan

- Use sample queries such as:
  - "Apa saja prinsip dasar AI yang bertanggung jawab menurut OJK?"
  - "Langkah-langkah ketahanan terhadap gangguan digital dalam Panduan Resiliensi Digital?"
  - "Bagaimana OJK mengatur pemanfaatan AI di sektor fintech?"
- Confirm that returned chunks:
  - Are topically relevant to the query
  - Include accurate metadata (file name, page number)
- Validate multilingual support for both English and Indonesian queries
- Test resilience for:
  - Empty or low-relevance queries (should return fallback response)
  - Similar but differently worded questions
- Log similarity scores from FAISS for top results to help manual verification
