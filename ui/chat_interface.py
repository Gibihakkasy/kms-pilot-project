import gradio as gr
import os
from datetime import datetime

DOCUMENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'documents')
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
TOKEN_LOG = os.path.join(LOGS_DIR, 'token_usage.log')

os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

def log_token_usage(user_message, tokens=0, cost=0.0):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(TOKEN_LOG, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] User: {user_message}\nTokens: {tokens}, Cost: ${cost:.6f}\n\n")

def handle_upload(files):
    uploaded = []
    for file in files:
        filename = os.path.basename(file.name)
        dest = os.path.join(DOCUMENTS_DIR, filename)
        with open(dest, 'wb') as out_f, open(file.name, 'rb') as in_f:
            out_f.write(in_f.read())
        uploaded.append(filename)
    return uploaded

def chat_fn(message, history, files=None):
    # Log token usage (mocked)
    log_token_usage(message, tokens=42, cost=0.0001)
    # Handle file uploads
    uploaded_files = []
    if files:
        uploaded_files = handle_upload(files)
    upload_status = ''
    if uploaded_files:
        upload_status = f"Uploaded: {', '.join(uploaded_files)}"
    # Return mock response
    reply = f"Work in progress...\n{upload_status}"
    return reply

def main():
    with gr.Blocks(title="AI-Powered KMS Chat UI") as demo:
        gr.Markdown("""
        # AI-Powered Knowledge Management System (Chat UI)
        - Multi-turn chat
        - PDF upload (stored in /documents/)
        - Token usage logging (mocked)
        """)
        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot()
                user_input = gr.Textbox(placeholder="Ask a question or upload a PDF...", label="Your message")
                send_btn = gr.Button("Send")
            with gr.Column(scale=1):
                file_upload = gr.File(label="Upload PDF(s)", file_count="multiple", file_types=[".pdf", ".zip"])
        def respond(user_message, chat_history, files):
            reply = chat_fn(user_message, chat_history, files)
            chat_history = chat_history + [[user_message, reply]]
            return "", chat_history
        send_btn.click(
            respond,
            inputs=[user_input, chatbot, file_upload],
            outputs=[user_input, chatbot]
        )
        user_input.submit(
            respond,
            inputs=[user_input, chatbot, file_upload],
            outputs=[user_input, chatbot]
        )
    demo.launch()

if __name__ == "__main__":
    main() 