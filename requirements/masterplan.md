## AI-Powered Knowledge Management System (KMS) Pilot – Masterplan

### Objective
Build a local prototype to demonstrate AI-powered semantic search and question-answering over PDF-based OJK regulatory documents. The pilot will run for 1 week, targeting internal usage by a single user with minimal technical setup. The system will monitor a folder for new or updated PDFs and automatically reprocess them. It will also support a conversational assistant-style interface for more natural interaction.

### Target Outcome
- Semantic search capability over local PDFs (English and Indonesian)
- Natural language QA with source reference (file name and page number)
- Assistant-style Gradio web interface with conversational history
- End-to-end offline-compatible setup with OpenAI API
- Automatic document refresh and vector index updates when files change

### Scope

#### In Scope
- Local ingestion of PDF files from a folder
- Chunking, embedding, and indexing documents using OpenAI
- Semantic retrieval and LLM-based answering with citation
- Gradio UI for assistant-style conversational interface
- Multilingual support (English & Indonesian)
- Local vector database (FAISS)
- Automatic detection and reprocessing of new or modified PDFs

#### Out of Scope
- Access control / user authentication
- Real-time collaboration or document editing
- Integration with enterprise systems (e.g. SharePoint, GDrive)

### Tools & Tech Stack

| Layer                     | Tool / Stack                                |
|---------------------------|---------------------------------------------|
| UI                        | Gradio (local web interface)                |
| Chat Interaction Framework| Gradio ChatInterface / Gradio Blocks        |
| PDF Parser                | PyMuPDF or pdfplumber                       |
| Embedding                 | OpenAI `text-embedding-3-large`             |
| Vector Store              | FAISS (lightweight, local)                  |
| File Monitoring           | watchdog                                    |
| LLM for QA                | OpenAI GPT-4                                |
| Language Detection        | langdetect or fasttext                      |
| Programming Language      | Python 3.10+                                |
| Deployment                | Local-only                                  |

### Folder Structure

```
kms_pilot/
├── app.py
├── config.py
├── ingest/
│   └── pdf_loader.py
├── embeddings/
│   └── vector_store.py
├── qa/
│   ├── retriever.py
│   └── answer_generator.py
├── documents/
├── utils/
│   └── language_detect.py
├── requirements.txt
└── README.md
```

### Tasks

1. Implement chunking, embedding, and FAISS indexer  
  - Split text into chunks and store them in a local vector database

2. Build semantic search and retriever with query-to-chunk pipeline  
  - Create retrieval logic to fetch relevant chunks based on user queries

3. Create LLM-based answer generator (OpenAI)  
  - Use OpenAI to generate answers and cite source document & page

4. Add Gradio interface for document input and Q&A  
  - Develop a local web UI to interact with the system

5. Test on Indonesian documents, add language detection  
  - Ensure multilingual support works and detect document/query language

6. Polish UI, add README, validate edge cases  
  - Final refinement, document usage, and handle edge/corner cases

7. Implement automatic document monitoring and re-indexing  
  - Use `watchdog` to monitor the `/documents` folder  
  - On detection of a new or modified file, re-trigger ingestion, chunking, embedding, and vector indexing  

8. Refactor ingestion using LangChain  
  - Replace manual PDF reading with PyMuPDFLoader  
  - Use RecursiveCharacterTextSplitter for chunking  
  - Attach metadata to each chunk

### Success Criteria

- Documents can be uploaded or placed in a folder
- Natural language questions return relevant answers with source
- Works on both English and Indonesian documents
- Fully usable through a local Gradio UI