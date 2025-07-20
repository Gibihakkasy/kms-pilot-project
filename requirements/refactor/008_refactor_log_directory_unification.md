# Refactor Step 8: Log Directory Unification

## Goal
Ensure the entire codebase uses a single, unified log directory (`/shared/logs`). Remove all other log folders and references, and enforce this structure going forward.

---

## Sub-Tasks

1. **Audit all log directory usage:**
   - Search the entire codebase for any reference to `/logs`, `/backend/logs`, `/shared/logs`, or any log file path.
2. **Unify log directory usage:**
   - Update all code, configs, and tests to use only `/shared/logs` for all logging.
3. **Delete redundant log folders:**
   - Remove `/logs` and `/backend/logs` from the project.
4. **Enforce and document:**
   - Ensure `.gitignore` blocks `/logs` and `/backend/logs`.
   - Add a note in the documentation about the unified log directory.

---

## Acceptance Criteria
- All code, configs, and tests use only `/shared/logs` for logging.
- No references to `/logs` or `/backend/logs` remain in the codebase.
- Only `/shared/logs` exists in the project.
- `.gitignore` blocks the creation of other log folders.
- Documentation notes the unified log directory. 