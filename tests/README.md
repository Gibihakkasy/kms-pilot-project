# Tests Directory

This directory contains unit and integration tests for the KMS Pilot Project backend.

## How to Run All Tests

From the project root, run:

```
python -m unittest discover -s tests
```

Or run individual test scripts:

```
python tests/test_answer_generator.py
python tests/test_retriever.py
python tests/test_integration_chat_flow.py
python tests/run_summarizer.py --file <path-to-pdf>
```

## Test Scripts

- `test_answer_generator.py`: Unit tests for the answer generation (Q&A) module.
- `test_retriever.py`: Unit tests for the retriever module (semantic search).
- `test_integration_chat_flow.py`: Integration test for the chat API endpoint (end-to-end flow).
- `run_summarizer.py`: CLI tool for testing document summarization. 