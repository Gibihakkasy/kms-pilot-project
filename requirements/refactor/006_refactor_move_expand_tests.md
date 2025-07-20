# Refactor Step 6: Move and Expand Tests

## Goal
Ensure all manual/standalone tests are moved to the `tests/` directory, expand automated test coverage for all new/cleaned code, and add integration tests for key flows.

---

## Sub-Tasks

1. **Move manual/standalone tests to `tests/`:**
   - Relocate any remaining test logic from modules to dedicated scripts in `tests/`.
2. **Expand automated test coverage:**
   - Add or update unit tests for all major backend and frontend modules, especially those refactored or cleaned.
   - Ensure new/cleaned code is covered by tests.
3. **Add integration tests:**
   - Test the full chat flow (frontend → backend → assistant flow → LLM → response).
   - Test document upload, ingestion, and retrieval end-to-end.
4. **Ensure tests are runnable and documented:**
   - Update test scripts and documentation so contributors can easily run all tests.

---

## Acceptance Criteria
- All manual/standalone tests are in the `tests/` directory.
- Automated test coverage includes all new/cleaned code.
- Integration tests cover key user flows.
- All tests are runnable and documented for contributors. 