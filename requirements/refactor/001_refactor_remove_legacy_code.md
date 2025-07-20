# Refactor Step 1: Remove Legacy Code and Update Documentation

## Goal
Eliminate all legacy, redundant, and unused code or documentation from the project. Ensure the codebase only supports the FastAPI backend and Next.js frontend, and that all documentation reflects the current architecture.

---

## Sub-Tasks

1. **Remove all references to Gradio UI and legacy Python-based UIs:**
   - Delete any documentation, requirements, or scripts referencing `ui/chat_interface.py`, Gradio, or legacy app flows.
   - Remove any code or files related to Gradio UI if present.
2. **Remove standalone test blocks in backend modules:**
   - Delete `if __name__ == '__main__':` blocks from modules like `answer_generator.py` and `summarization_refine_chain.py`.
   - Move any useful test logic to dedicated scripts in `tests/`.
3. **Update documentation:**
   - Remove outdated instructions or references to legacy UIs from `README.md` and other docs.
   - Ensure all setup, usage, and architecture documentation reflects only the FastAPI backend and Next.js frontend.

---

## Acceptance Criteria
- No references to Gradio UI or legacy Python-based UIs remain in the codebase or documentation.
- All backend modules are free of standalone test blocks; tests are in `tests/` only.
- Documentation is up-to-date and accurately describes the current system architecture and usage. 