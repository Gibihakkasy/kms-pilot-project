# AI-Powered Knowledge Management System (KMS) Pilot

This project is a local prototype of an AI-powered Knowledge Management System (KMS) designed for semantic search and question-answering over a collection of PDF documents. It supports both English and Indonesian languages and provides a modern web chat interface for interaction.

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
- **Modern Web Chat UI**: Built with Gradio Blocks, supporting multi-turn chat, markdown rendering, and file uploads.
- **Token & Prompt Logging**: Logs token usage and all prompts sent to the LLM for auditing and cost tracking.

## Tech Stack

- **Programming Language**: Python 3.10+
- **PDF Parsing**: PyMuPDF
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **AI Models**: OpenAI API (for embeddings and answer generation)
- **Web UI**: Gradio (Blocks-based chat interface)
- **Dependencies**: `python-dotenv`, `numpy`, `langdetect`, `gradio`, `langchain`, `openai`, `watchdog`

## Project Structure

```
kms-pilot-project/
├── app.py                  # Main Gradio application (legacy, full pipeline)
├── ui/
│   └── chat_interface.py   # Modern Gradio chat UI (Blocks-based, multi-turn, upload, logging)
├── assistant/
│   ├── langgraph_flow.py   # LangGraph-based assistant flow with session memory
│   └── query_classifier.py # Intent classifier for routing
├── documents/              # Folder for input PDF files
├── embeddings/
│   ├── vector_store.py     # Creates and manages the FAISS vector store
│   └── faiss_index/        # (Generated) Stores the FAISS index and metadata
├── ingest/
│   └── pdf_loader.py       # Handles PDF loading and text chunking
├── qa/
│   ├── retriever.py        # Retrieves relevant chunks from the vector store
│   └── answer_generator.py # Generates answers using an LLM, logs prompts
├── chains/
│   └── summarization_refine_chain.py # Summarization chain for long conversations
├── utils/
│   ├── language_detect.py  # Utility for detecting query language
│   └── file_monitor.py     # Monitors /documents for changes (auto re-index)
├── logs/
│   ├── answer_generator_prompt.log   # All prompts sent to the LLM
│   └── token_usage.log               # Token usage and cost per query
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (e.g., API keys)
└── README.md               # This file
```

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Prerequisites

- Python 3.10 or newer.
- An API key from OpenAI.

### 2. Clone the Repository

```bash
# This step is optional if you already have the project files
git clone <repository-url>
cd kms-pilot-project
```

### 3. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a file named `.env` in the root of the project directory and add your OpenAI API key:

```
OPENAI_API_KEY="your_openai_api_key_here"
```

## Usage

### 1. Add Documents

Place the PDF files you want to query into the `documents/` folder.

### 2. Create the Vector Store

Before running the application for the first time (or after adding new documents), you must run the ingestion script to process the PDFs and create the vector store. 

Run the following command from the project root:

```bash
python -m embeddings.vector_store
```

This will create a `faiss_index` sub-directory inside `embeddings/` containing the vector index and metadata.

### 3. Launch the Application

You can start the modern chat UI or the legacy app:

**Modern Chat UI (recommended):**
```bash
python ui/chat_interface.py
```

**Legacy App (full pipeline, auto re-index, file monitoring):**
```bash
python app.py
```

The application will be available at a local URL (e.g., `http://127.0.0.1:7860`), which will be displayed in the console.

### 4. Ask Questions

Open the URL in your web browser. Type your question into the input box and click "Send". The system will provide an answer along with the sources (file name and page number) it used to generate the response. The assistant supports follow-up questions, session memory, and will summarize long conversations as needed.

## Limitations and Future Improvements

- **Manual Data Refresh (Legacy App):** The legacy system does not automatically detect new or updated documents unless you use the file monitor. To include new information, you must place the files in the `documents/` folder and re-run the `embeddings.vector_store` script.
- **API Dependency:** The quality of embeddings and answers is dependent on the OpenAI API. An internet connection and a valid API key are required.
- **No Access Control:** The application is designed for local, single-user access and does not include any user authentication or security features.
- **Potential Enhancements:**
    - Implement more advanced token-based memory management.
    - Add support for more document formats (e.g., `.docx`, `.txt`).
    - Integrate a local, open-source model to remove the OpenAI dependency.
    - Expand UI features: feedback, download session summary, etc.
    - Improve summarization and context handling for very long sessions.