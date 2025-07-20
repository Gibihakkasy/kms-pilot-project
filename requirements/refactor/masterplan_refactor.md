# KMS Pilot Project – Refactor & Cleanup Masterplan

## Objective
Refactor and clean the codebase to eliminate duplication, enforce best practices, and clarify the separation between backend and frontend. Ensure maintainability, scalability, and ease of onboarding for new contributors. 

**Additionally, ensure codebase hygiene by removing all unused, obsolete, or trash files and code, cleaning up test/debug artifacts, and maintaining a clean, professional, and minimal project structure at every level (not just architecture and logic).**

---

## 1. Remove Legacy and Redundant Code

- **Delete all references to Gradio UI and legacy Python-based UIs**
  - Remove any documentation, requirements, or scripts referencing `ui/chat_interface.py` or Gradio-based flows.
  - Ensure only the FastAPI backend and Next.js frontend are documented and supported.
- **Remove standalone test blocks** in backend modules (e.g., `if __name__ == '__main__':` in `answer_generator.py`, `summarization_refine_chain.py`).
  - Move any useful test logic to dedicated test scripts in `tests/`.

---

## 2. Backend Refactor

- **Centralize all business logic in the assistant flow**
  - Ensure all Q&A and summarization requests are routed through `backend/assistant/langgraph_flow.py`.
  - Remove or refactor any direct calls to `AnswerGenerator` or `summarize_documents` outside the assistant flow.
- **Clarify API boundaries**
  - Keep FastAPI endpoints in `backend/app.py` thin; delegate all logic to the assistant flow.
  - Standardize API request/response schemas (e.g., for chat, documents).
- **Consolidate utility functions**
  - Group token logging, language detection, and file monitoring utilities in a clear `backend/utils/` structure.
- **Document the backend architecture**
  - Add or update a `README.md` in `backend/` to describe the assistant flow, API endpoints, and utility modules.

---

## 3. Frontend Refactor

- **Enforce separation of concerns**
  - Keep all API logic in `frontend/lib/api.ts`.
  - Use hooks (`use-chat`, `use-documents`) only for state management and API calls.
  - Ensure UI components are presentational and stateless.
- **Standardize error and loading handling**
  - Use consistent patterns for error, loading, and progress states across hooks and components.
- **Document the frontend architecture**
  - Add or update a `README.md` in `frontend/` to describe the main hooks, API client, and component structure.

---

## 4. Remove Unused/Obsolete Files

- **Audit the entire repository for unused, obsolete, or trash files:**
  - Remove files like `config.py`, `setup.py`, `.DS_Store`, backup files, editor temp files, and any other files not required for running, developing, or maintaining the project.
  - Archive or document any files intentionally kept for legacy/reference reasons.

---

## 5. Clean Up Unused/Test/Trash Code

- **Audit all code for unused, test, or trash code and lines:**
  - Remove commented-out code, dead code (unused functions, classes, variables), leftover debug prints, TODOs, and temporary hacks.
  - Remove redundant or obsolete test code, manual test blocks, or test files not covered by proper automated tests.
  - Remove unused imports and variables.
  - Ensure all modules are clean, readable, and maintainable.

---

## 6. Move and Expand Tests

- **Move all manual/standalone tests to `tests/`**
  - Ensure there are CLI or script-based tests for answer generation, summarization, and document ingestion.
- **Add integration tests**
  - Test the full chat flow (frontend → backend → assistant flow → LLM → response).
  - Test document upload, ingestion, and retrieval end-to-end.
- **Ensure all new/cleaned code is covered by tests.**

---

## 7. Finalize Documentation and Onboarding

- **Update the main `README.md`**
  - Remove references to legacy UIs and clarify the current architecture.
  - Add diagrams or flowcharts for backend and frontend flows.
- **Add developer onboarding notes**
  - How to run, test, and contribute to the project.
- **Ensure all documentation reflects the final, tested state of the codebase.**

---

## Optional Improvements

- **Consider API versioning** for future extensibility.
- **Add type hints and docstrings** throughout the backend for clarity.
- **Adopt a linter/formatter** (e.g., Black for Python, Prettier for JS/TS) and enforce via CI.

---

## Implementation Order
1. Remove legacy code and update documentation.
2. Refactor backend for unified assistant flow and utilities.
3. Refactor frontend for best practice separation.
4. Remove unused/obsolete files.
5. Clean up unused/test/trash code.
6. Move and expand tests (ensure all new/cleaned code is covered).
7. Finalize documentation and onboarding materials.
8. (Optional) Apply further improvements and automation. 