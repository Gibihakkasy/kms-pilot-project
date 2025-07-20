# AI-Powered Knowledge Management System (KMS) Pilot

This project is a local prototype of an AI-powered Knowledge Management System (KMS) designed for semantic search and question-answering over a collection of PDF documents. It supports both English and Indonesian languages and provides a modern web chat interface for interaction.

---

## Architecture Overview

```
+-------------------+        +-------------------+        +-------------------+
|   Next.js Frontend| <----> |   FastAPI Backend | <----> |   OpenAI/FAISS    |
+-------------------+        +-------------------+        +-------------------+
        |                        |                            |
        |  User chat, upload     |  API: /api/chat, /api/upload, etc.
        |----------------------->|--------------------------->|
        |                        |                            |
        |  Answers, docs list    |  LLM, vector search, etc.
        |<-----------------------|<---------------------------|
```

---

## Features

- **PDF Document Ingestion**: Automatically loads and processes PDF files from a designated folder.
- **Text Chunking**: Splits document text into smaller, manageable chunks for effective embedding.
- **Semantic Embedding**: Uses OpenAI's `text-embedding-3-large` model to generate vector embeddings for text chunks.
- **Vector Storage**: Stores and indexes embeddings locally using FAISS for efficient similarity searches.
- **Semantic Retrieval**: Retrieves the most relevant document chunks based on a user's natural language query.
- **AI-Powered Q&A**: Leverages an OpenAI language model (GPT-4.1-nano) to generate coherent answers based on the retrieved context.
- **Session Memory & Summarization**: Remembers the last 5 Q&A pairs in a session; if the conversation is longer, older turns are summarized and included as context for follow-up questions.
- **Advanced Prompt Structuring**: Clearly separates previous Q&A, summarized history, and vector search results in the LLM prompt, with prompt logging for transparency.
- **Multilingual Support**: Handles queries and documents in both English and Indonesian.
- **Modern Web Chat UI**: Built with Next.js and React, supporting multi-turn chat, markdown rendering, and file uploads.
- **Token & Prompt Logging**: Logs token usage and all prompts sent to the LLM for auditing and cost tracking.

---

## Tech Stack

- **Frontend**: Next.js (React, TypeScript, Tailwind CSS)
- **Backend**: FastAPI (Python 3.10+)
- **PDF Parsing**: PyMuPDF
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **AI Models**: OpenAI API (for embeddings and answer generation)
- **Utilities**: `python-dotenv`, `numpy`, `langdetect`, `langchain`, `openai`, `watchdog`

---

## Setup and Installation

### 1. Prerequisites
- Python 3.10 or newer
- Node.js (for frontend)
- An API key from OpenAI

### 2. Clone the Repository
```bash
git clone <repository-url>
cd kms-pilot-project
```

### 3. Create a Virtual Environment (Backend)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### 5. Set Up Environment Variables
Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY="your_openai_api_key_here"
```

### 6. Ingest Documents and Create Vector Store
Place PDF files in `shared/documents/`.
Run:
```bash
python -m backend.embeddings.vector_store
```

### 7. Launch the Application
From the project root, run:
```bash
python app.py
```
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Usage
- Upload documents via the web UI or place them in `shared/documents/`.
- Ask questions in the chat interface.
- Answers will include source citations (file name and page number).

---

## Developer Onboarding
- See `backend/README.md` and `frontend/README.md` for architecture details.
- All tests are in the `tests/` directory. Run with:
  ```bash
  python -m unittest discover -s tests
  ```
- To contribute:
  - Follow the code style and structure in backend/frontend modules.
  - Add or update tests for new features.
  - Update documentation as needed.

---

## Limitations and Future Improvements
- No authentication or access control (prototype only)
- No real-time collaboration or document editing
- No enterprise integrations (e.g., SharePoint, GDrive)
- See `requirements/masterplan_refactor.md` for planned improvements

---

## Log Directory
- All logs (token usage, prompt logs, etc.) are written to `/shared/logs`.
- Only `/shared/logs` should exist; `/logs` and `/backend/logs` are obsolete and blocked by `.gitignore`.

---