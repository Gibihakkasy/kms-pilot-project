# Backend Architecture Overview

## Overview
This backend powers the Knowledge Management System (KMS) API, providing endpoints for chat-based Q&A, document ingestion, and semantic search over regulatory documents. All core logic is centralized in the assistant flow for maintainability and clarity.

---

## Key Components

### 1. FastAPI Application (`backend/app.py`)
- Exposes REST API endpoints for chat, document upload, and health checks.
- Endpoints are thin and delegate all business logic to the assistant flow or utility modules.

### 2. Assistant Flow (`backend/assistant/langgraph_flow.py`)
- Central entry point for all Q&A and summarization logic.
- Handles:
  - Intent classification (Q&A vs. summarization)
  - Multi-turn session memory
  - Routing to answer generation or summarization chains
  - Formatting responses with sources
- All chat requests from the API are processed here.

### 3. Q&A and Summarization Modules
- `backend/qa/answer_generator.py`: Generates answers using LLMs (used only by the assistant flow).
- `backend/chains/summarization_refine_chain.py`: Produces structured summaries (used only by the assistant flow).
- `backend/qa/retriever.py`: Retrieves relevant document chunks from the FAISS vector store.

### 4. Utility Modules (`backend/utils/`)
- `token_logger.py`: Logs token usage and cost for all LLM activities.
- `language_detect.py`: Detects the language of queries and documents.
- `file_monitor.py`: Monitors the documents folder for changes and triggers re-indexing.

---

## API Endpoints

- `POST /api/chat`: Process a chat message and return an answer or summary.
- `POST /api/upload`: Upload a new document and trigger ingestion.
- `GET /api/documents`: List all available documents.
- `DELETE /api/documents/{id}`: Delete a document.
- `GET /api/health`: Health check endpoint.

All endpoints delegate business logic to the assistant flow or utility modules.

---

## Development Notes
- All Q&A and summarization logic must go through the assistant flow.
- Utility functions are grouped in `backend/utils/` for clarity.
- Standalone test blocks have been removed; use the `tests/` directory for all test scripts.

---

## Contributor Onboarding
- See the main project README for setup instructions.
- To add new features, extend the assistant flow or utility modules as needed.
- Keep API endpoints thin and focused on request/response handling. 

---

## Log Directory
- All logs (token usage, prompt logs, etc.) are written to `/shared/logs`.
- Only `/shared/logs` should exist; `/logs` and `/backend/logs` are obsolete and blocked by `.gitignore`.

--- 