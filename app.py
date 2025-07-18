import gradio as gr
import gradio.themes
import os
import threading
import atexit
from assistant.langgraph_flow import run_assistant
from utils.language_detect import detect_language
from utils.file_monitor import DocumentMonitor
from embeddings.vector_store import create_and_save_vector_store

# --- CONFIGURATION & INITIALIZATION ---
DOCUMENTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'documents')

# Load the retriever and answer generator once
print("Initializing the KMS system...")
print("KMS system initialized successfully.")

# Initialize the document monitor
monitor = DocumentMonitor(path=DOCUMENTS_DIR, callback=create_and_save_vector_store)

# Register a cleanup function to stop the monitor on exit
atexit.register(monitor.stop)

# --- CHAT HANDLER ---
def chat_handler(message, history):
    """
    message: str (current user message)
    history: list of [user, assistant] pairs (Gradio chat format)
    Returns: (assistant_reply, updated_history)
    """
    # Convert Gradio's history format to tuples
    history_tuples = [(u, a) for u, a in history] if history else []
    result = run_assistant(message, history_tuples)
    reply = result.get("content", "[No answer]")
    # Add sources if available
    sources = result.get("sources", [])
    if sources:
        reply += "\n\nSources:\n" + "\n".join(f"- {src['document']} (Page {src['page']})" for src in sources if src['document'])
    return reply

# --- GRADIO CHAT INTERFACE ---
with gr.Blocks(theme=gradio.themes.Soft(), title="AI-Powered KMS") as demo:
    gr.Markdown(
        """
        # AI-Powered Knowledge Management System
        Ask a question or request a summary about your documents in English or Indonesian. The assistant remembers the last 5 Q&A and summarizes longer conversations for context.
        """
    )
    chatbot = gr.Chatbot()
    with gr.Row():
        user_input = gr.Textbox(
            label="Your message",
            placeholder="Ask a question or request a summary...",
            lines=3
        )
        send_btn = gr.Button("Send")

    def respond(user_message, chat_history):
        reply = chat_handler(user_message, chat_history)
        chat_history = chat_history + [[user_message, reply]]
        return "", chat_history

    send_btn.click(
        respond,
        inputs=[user_input, chatbot],
        outputs=[user_input, chatbot]
    )
    user_input.submit(
        respond,
        inputs=[user_input, chatbot],
        outputs=[user_input, chatbot]
    )

# --- LAUNCH THE APP ---
if __name__ == "__main__":
    # Smarter startup check: ensure all PDFs are embedded
    need_reindex = False
    retriever_index_path = os.path.join("embeddings", "index.faiss")
    retriever_metadata_path = os.path.join("embeddings", "metadata.json")
    if not os.path.exists(retriever_index_path) or not os.path.exists(retriever_metadata_path):
        print("Vector store not found. Running initial indexing...")
        need_reindex = True
    else:
        # Check if any PDF in documents/ is missing from metadata.json
        import json
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

    # Start the file monitor in a background thread
    monitor_thread = threading.Thread(target=monitor.start, daemon=True)
    monitor_thread.start()

    print("Launching Gradio interface...")
    demo.launch()