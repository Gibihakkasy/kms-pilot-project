from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import glob
import atexit
from typing import List, Dict, Optional
from datetime import datetime
import shutil

# Import existing functionality
from backend.assistant.langgraph_flow import run_assistant
from backend.utils.file_monitor import DocumentMonitor
from backend.embeddings.vector_store import create_and_save_vector_store

# --- CONFIGURATION & INITIALIZATION ---
DOCUMENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'shared', 'documents')
# LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'shared', 'logs')
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
# os.makedirs(LOGS_DIR, exist_ok=True)

# Initialize FastAPI app
app = FastAPI(title="Knowledge Assistant API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the document monitor
monitor = DocumentMonitor(path=DOCUMENTS_DIR, callback=create_and_save_vector_store)

# Register a cleanup function to stop the monitor on exit
atexit.register(monitor.stop)

# --- PYDANTIC MODELS ---
class ChatMessage(BaseModel):
    content: str
    conversation_history: Optional[List[Dict]] = []

class DocumentInfo(BaseModel):
    id: str
    name: str
    size: int
    modified: str
    type: str

class ChatResponse(BaseModel):
    content: str
    source: Optional[str] = None
    timestamp: datetime

# --- API ENDPOINTS ---

@app.get("/")
async def root():
    return {"message": "Knowledge Assistant API is running"}

@app.get("/api/documents", response_model=List[DocumentInfo])
async def get_documents():
    """Get list of documents with metadata"""
    documents = []
    for ext in ['*.pdf', '*.txt', '*.docx']:
        files = glob.glob(os.path.join(DOCUMENTS_DIR, ext))
        for file_path in files:
            stat = os.stat(file_path)
            documents.append(DocumentInfo(
                id=os.path.basename(file_path),
                name=os.path.basename(file_path),
                size=stat.st_size,
                modified=datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                type=os.path.splitext(file_path)[1][1:]  # Remove the dot
            ))
    return sorted(documents, key=lambda x: x.modified, reverse=True)

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a new document"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file type
    allowed_extensions = {'.pdf', '.txt', '.docx'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file_ext} not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Save file
    file_path = os.path.join(DOCUMENTS_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Trigger reindexing
        create_and_save_vector_store()
        
        return {"message": f"File {file.filename} uploaded successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Process chat message and return assistant response"""
    try:
        # Robustly convert conversation history from frontend format to assistant format
        history = []
        msgs = message.conversation_history or []
        # Skip initial assistant-only message (welcome)
        if msgs and msgs[0].get("type") == "assistant" and len(msgs) > 1:
            msgs = msgs[1:]
        # Only include up to the last complete user-assistant pair (exclude current user question if unpaired)
        last_index = len(msgs)
        if last_index > 0 and msgs[-1].get("type") == "user":
            last_index -= 1
        i = 0
        while i < last_index:
            if msgs[i].get("type") == "user":
                user_msg = msgs[i]["content"]
                assistant_msg = ""
                if i + 1 < last_index and msgs[i + 1].get("type") == "assistant":
                    assistant_msg = msgs[i + 1]["content"]
                    i += 1
                history.append((user_msg, assistant_msg))
            i += 1
        # Run the assistant with the user's message and conversation history
        response = run_assistant(message.content, history)
        
        # Extract content and source from response
        content = response.get('content', 'Sorry, I encountered an error processing your request.')
        sources = response.get('sources', [])
        
        # Format sources for frontend
        source_text = None
        if sources:
            source_list = []
            for src in sources:
                if src.get('document'):
                    page_info = f" (Page {src['page']})" if src.get('page') else ""
                    source_list.append(f"{src['document']}{page_info}")
            source_text = "; ".join(source_list)
        
        return ChatResponse(
            content=content,
            source=source_text,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document"""
    file_path = os.path.join(DOCUMENTS_DIR, document_id)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        os.remove(file_path)
        # Trigger reindexing after deletion
        create_and_save_vector_store()
        return {"message": f"Document {document_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "documents_count": len(glob.glob(os.path.join(DOCUMENTS_DIR, "*"))),
        "timestamp": datetime.now()
    }

# --- REINDEXING CHECK ---
def check_and_reindex():
    """Check if reindexing is needed and perform it if necessary"""
    try:
        # Check if vector store exists
        vectorstore_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'vectorstore')
        if not os.path.exists(vectorstore_dir) or not os.listdir(vectorstore_dir):
            print("🔄 Vector store not found. Creating initial index...")
            create_and_save_vector_store()
            print("✅ Initial indexing completed!")
        else:
            print("✅ Vector store found. Ready to serve!")
    except Exception as e:
        print(f"❌ Error during reindexing check: {e}")

# Check if reindexing is needed and perform it if necessary
check_and_reindex()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Knowledge Assistant API...")
    print(f"📁 Documents directory: {DOCUMENTS_DIR}")
    # print(f"📝 Logs directory: {LOGS_DIR}") # This line is removed as per the edit hint
    print("🌐 API will be available at: http://localhost:8000")
    print("📚 API docs will be available at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
