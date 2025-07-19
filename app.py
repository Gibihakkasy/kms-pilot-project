import gradio as gr
from gradio import themes
import os
import glob
import threading
import atexit
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Import existing functionality
from assistant.langgraph_flow import run_assistant
from utils.file_monitor import DocumentMonitor
from embeddings.vector_store import create_and_save_vector_store

# --- CONFIGURATION & INITIALIZATION ---
DOCUMENTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'documents')
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Initialize the document monitor
monitor = DocumentMonitor(path=DOCUMENTS_DIR, callback=create_and_save_vector_store)

# Register a cleanup function to stop the monitor on exit
atexit.register(monitor.stop)

class KnowledgeAssistantUI:
    def __init__(self):
        self.documents_dir = DOCUMENTS_DIR
        self.logs_dir = LOGS_DIR
        
    def get_document_list(self) -> List[dict]:
        """Get list of documents with metadata"""
        documents = []
        for ext in ['*.pdf', '*.txt', '*.docx']:
            files = glob.glob(os.path.join(self.documents_dir, ext))
            for file_path in files:
                stat = os.stat(file_path)
                documents.append({
                    'name': os.path.basename(file_path),
                    'path': file_path,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                })
        return sorted(documents, key=lambda x: x['modified'], reverse=True)
    
    def format_document_list_html(self) -> str:
        """Format document list as HTML"""
        documents = self.get_document_list()
        if not documents:
            return "<div style='color: #666; font-style: italic; padding: 20px;'>No documents found</div>"
        
        html = "<div style='padding: 10px;'>"
        for doc in documents:
            size_kb = doc['size'] / 1024
            html += f"""
            <div style='border-bottom: 1px solid #eee; padding: 10px 0; cursor: pointer;' 
                 onclick='document.querySelector(\"#chat_input\").value = \"Tell me about {doc["name"]}\"; document.querySelector(\"#chat_input\").focus();'>
                <div style='font-weight: 500; color: #333; margin-bottom: 4px;'>{doc['name']}</div>
                <div style='font-size: 12px; color: #666;'>Added: {doc['modified']}</div>
                <div style='font-size: 12px; color: #666;'>{size_kb:.1f} KB</div>
            </div>
            """
        html += "</div>"
        return html
    
    def handle_file_upload(self, files) -> str:
        """Handle file uploads"""
        if not files:
            return "No files selected"
        
        uploaded = []
        for file in files:
            try:
                filename = os.path.basename(file.name)
                dest_path = os.path.join(self.documents_dir, filename)
                
                # Copy file to documents directory
                with open(dest_path, 'wb') as dest_file:
                    with open(file.name, 'rb') as src_file:
                        dest_file.write(src_file.read())
                
                uploaded.append(filename)
            except Exception as e:
                return f"Error uploading files: {str(e)}"
        
        # Trigger reindexing if monitor is available
        try:
            create_and_save_vector_store()
        except Exception as e:
            print(f"Error during reindexing: {e}")
        
        return f"✅ Successfully uploaded: {', '.join(uploaded)}"
    
    def chat_response(self, message: str, history: List[Tuple[str, str]]) -> str:
        """Generate chat response"""
        if not message.strip():
            return "Please enter a question or request."
        
        try:
            # Convert Gradio history format to assistant format
            history_tuples = [(user, assistant) for user, assistant in history] if history else []
            
            # Get response from assistant
            result = run_assistant(message, history_tuples)
            reply = result.get("content", "I'm sorry, I couldn't process your request.")
            
            # Add sources if available
            sources = result.get("sources", [])
            if sources:
                reply += "\n\n**Sources:**\n"
                for src in sources:
                    if src.get('document'):
                        page_info = f" (Page {src['page']})" if src.get('page') else ""
                        reply += f"- {src['document']}{page_info}\n"
            
            return reply
            
        except Exception as e:
            return f"Error processing request: {str(e)}"
    
    def create_interface(self):
        """Create the Gradio interface"""
        
        # Custom CSS for professional styling
        css = """
        .status-progress .progress {
            background: #007bff;
            border-radius: 4px;
            height: 100%;
            width: 0%;
            transition: width 0.3s ease;
        }
        .suggestion-item {
            cursor: pointer;
            color: #007bff;
            text-decoration: underline;
            margin: 2px 0;
        }
        .suggestion-item:hover {
            color: #0056b3;
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
        }
        .sidebar {
            background: #f8f9fa;
            border-right: 1px solid #dee2e6;
            height: 100vh;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        .document-list-container {
            flex: 1;
            overflow-y: auto;
            max-height: 400px;
        }
        .documents-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .header-buttons {
            display: flex;
            gap: 5px;
        }
        .document-item:hover {
            background-color: #e9ecef;
        }
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #28a745;
            margin-right: 8px;
        }
        """
        
        with gr.Blocks(css=css, title="Knowledge Assistant", theme=themes.Soft()) as interface:
            
            # Header
            with gr.Row():
                gr.HTML("""
                <div style='display: flex; align-items: center; padding: 20px 0; border-bottom: 1px solid #dee2e6;'>
                    <div style='background: #007bff; color: white; width: 40px; height: 40px; border-radius: 50%; 
                                display: flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold;'>
                        KA
                    </div>
                    <div>
                        <h2 style='margin: 0; color: #333;'>Knowledge Assistant</h2>
                        <div style='color: #666; font-size: 14px;'>
                            <span class='status-indicator'></span>Online
                        </div>
                    </div>
                </div>
                """)
            
            with gr.Row():
                # Sidebar
                with gr.Column(scale=1, min_width=300):
                    # Documents header with inline buttons
                    with gr.Row():
                        gr.Markdown("### Documents")
                        with gr.Row():
                            refresh_btn = gr.Button("🔄", size="sm", variant="secondary", scale=1, min_width=40)
                            upload_btn = gr.UploadButton(
                                "📁", 
                                file_count="multiple",
                                file_types=[".pdf", ".txt", ".docx"],
                                size="sm",
                                variant="secondary",
                                scale=1,
                                min_width=40
                            )
                    
                    # Document list with controlled height
                    document_list = gr.HTML(
                        value=self.format_document_list_html(),
                        label="",
                        elem_classes=["document-list-container"]
                    )
                    
                    upload_status = gr.Textbox(
                        label="Upload Status",
                        interactive=False,
                        visible=False
                    )
                    
                    # Processing status
                    document_count = len(self.get_document_list())
                    processing_status = gr.HTML(
                        f"""
                        <div style='margin-top: 20px; padding: 10px; background: #f8f9fa; border-radius: 6px; font-size: 12px;'>
                            <div style='margin-bottom: 5px;'><strong>Processing Status:</strong></div>
                            <div>📄 {document_count} document{'s' if document_count != 1 else ''} available</div>
                            <div style='color: #666;'>Press Enter to send, Shift+Enter for new line</div>
                        </div>
                        """
                    )
                
                # Main chat area
                with gr.Column(scale=3):
                    gr.Markdown("### Chat with Knowledge Assistant")
                    
                    # Welcome message with clickable suggestions
                    welcome_msg = """Selamat datang! Saya adalah Asisten Pengetahuan Anda. Saya dapat membantu menjawab pertanyaan tentang dokumen Anda.

Berikut beberapa pertanyaan yang bisa Anda coba:
<div class="suggestion-item" onclick="document.querySelector('#chat_input input, #chat_input textarea').value='Apa itu kecerdasan artifisial dalam perbankan?'; document.querySelector('#chat_input input, #chat_input textarea').focus();">• Apa itu kecerdasan artifisial dalam perbankan?</div>
<div class="suggestion-item" onclick="document.querySelector('#chat_input input, #chat_input textarea').value='Bagaimana tata kelola AI di Indonesia?'; document.querySelector('#chat_input input, #chat_input textarea').focus();">• Bagaimana tata kelola AI di Indonesia?</div>
<div class="suggestion-item" onclick="document.querySelector('#chat_input input, #chat_input textarea').value='Jelaskan tentang prinsip-prinsip AI yang bertanggung jawab'; document.querySelector('#chat_input input, #chat_input textarea').focus();">• Jelaskan tentang prinsip-prinsip AI yang bertanggung jawab</div>
<div class="suggestion-item" onclick="document.querySelector('#chat_input input, #chat_input textarea').value='Apa saja risiko penggunaan AI dalam perbankan?'; document.querySelector('#chat_input input, #chat_input textarea').focus();">• Apa saja risiko penggunaan AI dalam perbankan?</div>

Klik salah satu pertanyaan di atas atau ketik pertanyaan Anda sendiri!"""
                    
                    # Chat interface
                    chatbot = gr.Chatbot(
                        value=[["", welcome_msg]],
                        height=500,
                        show_label=False,
                        container=False,
                        bubble_full_width=False
                    )
                    
                    # Input area
                    with gr.Row():
                        chat_input = gr.Textbox(
                            placeholder="Ask a question about your documents...",
                            show_label=False,
                            scale=4,
                            container=False,
                            elem_id="chat_input"
                        )
                        send_btn = gr.Button("Send", variant="primary", scale=1)
                    
            
            # Event handlers
            def respond(message, history):
                if message.strip():
                    response = self.chat_response(message, history)
                    history = history + [[message, response]]
                return "", history
            
            def refresh_documents():
                return self.format_document_list_html()
            
            def handle_upload(files):
                status = self.handle_file_upload(files)
                return status, self.format_document_list_html(), gr.update(visible=True)
            
            # Wire up events
            chat_input.submit(respond, [chat_input, chatbot], [chat_input, chatbot])
            send_btn.click(respond, [chat_input, chatbot], [chat_input, chatbot])
            refresh_btn.click(refresh_documents, outputs=[document_list])
            upload_btn.upload(
                handle_upload, 
                [upload_btn], 
                [upload_status, document_list, upload_status]
            )
        
        return interface

def check_and_reindex():
    """Check if reindexing is needed and perform it if necessary"""
    need_reindex = False
    retriever_index_path = os.path.join("embeddings", "index.faiss")
    retriever_metadata_path = os.path.join("embeddings", "metadata.json")
    
    if not os.path.exists(retriever_index_path) or not os.path.exists(retriever_metadata_path):
        print("Vector store not found. Running initial indexing...")
        need_reindex = True
    else:
        # Check if any PDF in documents/ is missing from metadata.json
        pdf_files = set([f for f in os.listdir(DOCUMENTS_DIR) if f.lower().endswith('.pdf')])
        try:
            with open(retriever_metadata_path, 'r') as f:
                metadata = json.load(f)
            embedded_files = set(chunk['metadata']['file_name'] for chunk in metadata.values())
            missing_pdfs = pdf_files - embedded_files
            if missing_pdfs:
                print(f"Detected new PDFs not yet embedded: {missing_pdfs}. Running re-indexing...")
                need_reindex = True
        except Exception as e:
            print(f"Error reading metadata for startup check: {e}")
            need_reindex = True
    
    if need_reindex:
        create_and_save_vector_store()
        print("Initial indexing complete.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("🚀 Starting Knowledge Assistant...")
    print(f"📁 Documents directory: {DOCUMENTS_DIR}")
    
    # Check and run initial indexing if needed
    check_and_reindex()
    
    # Start the file monitor in a background thread
    monitor_thread = threading.Thread(target=monitor.start, daemon=True)
    monitor_thread.start()
    print(f"📡 File monitor started on: {DOCUMENTS_DIR}")
    
    # Initialize and launch the UI
    assistant_ui = KnowledgeAssistantUI()
    interface = assistant_ui.create_interface()
    
    print("🌐 Web interface starting...")
    print("💡 Upload PDF documents and start chatting!")
    print("-" * 50)
    
    # Launch the interface
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True
    )