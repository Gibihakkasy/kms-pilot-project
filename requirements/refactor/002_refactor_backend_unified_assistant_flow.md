# Refactor Step 2: Backend Unified Assistant Flow

## Goal
Ensure all backend business logic for Q&A and summarization is centralized in the assistant flow (`backend/assistant/langgraph_flow.py`). Clarify API boundaries and consolidate utility functions for maintainability and clarity.

---

## Sub-Tasks

1. **Centralize all business logic in the assistant flow:**
   - Ensure all Q&A and summarization requests are routed through `langgraph_flow.py`.
   - Remove or refactor any direct calls to `AnswerGenerator` or `summarize_documents` outside the assistant flow.
2. **Clarify API boundaries:**
   - Keep FastAPI endpoints in `backend/app.py` thin; delegate all logic to the assistant flow.
   - Standardize API request/response schemas (e.g., for chat, documents).
3. **Consolidate utility functions and log directories:**
   - Group token logging, language detection, and file monitoring utilities in a clear `backend/utils/` structure.
   - Consolidate all log directories into a single location (e.g., `/shared/logs`).
   - Update all code to reference this unified log directory.
   - Remove redundant or legacy log folders (`/logs`, `/backend/logs`, etc.).
4. **Document the backend architecture:**
   - Add or update a `README.md` in `backend/` to describe the assistant flow, API endpoints, and utility modules.

---

## Acceptance Criteria
- All Q&A and summarization logic is routed through the assistant flow.
- FastAPI endpoints are thin and only delegate to the assistant flow.
- Utility functions are organized and documented in `backend/utils/`.
- **All logs are written to a single, unified directory, and redundant log folders are removed.**
- Backend architecture is documented for contributors. 