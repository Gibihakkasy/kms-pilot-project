import gradio as gr
from qa.retriever import Retriever
from qa.answer_generator import AnswerGenerator
from utils.language_detect import detect_language

# --- INITIALIZATION ---
# Load the retriever and answer generator once to be reused across requests
print("Initializing the KMS system...")
retriever = Retriever()
answer_generator = AnswerGenerator()
print("KMS system initialized successfully.")

# --- CORE FUNCTION ---
def get_answer(query: str):
    """
    The main function to handle a user query from the Gradio interface.
    It retrieves chunks, generates an answer, and formats the sources.
    """
    if not query:
        return "Please enter a question.", ""

    # 1. Detect the language of the query
    lang = detect_language(query)
    print(f"Detected language: {lang}")

    # 1. Retrieve relevant chunks
    print(f"Retrieving chunks for query: '{query}'")
    retrieved_chunks = retriever.retrieve_chunks(query, k=3)

    # 2. Generate an answer
    print(f"Generating answer for query: '{query}'")
    final_answer = answer_generator.generate_answer(query, retrieved_chunks)

    # 3. Format the sources for display
    if retrieved_chunks:
        sources = "\n--- Sources ---\n"
        sources += "\n".join(
            f"- {chunk['metadata']['file_name']} (Page {chunk['metadata']['page_number']})"
            for chunk in retrieved_chunks
        )
    else:
        sources = "No sources found."
    
    return final_answer, sources

# --- GRADIO INTERFACE ---
with gr.Blocks(theme=gr.themes.Soft(), title="AI-Powered KMS") as demo:  # type: ignore
    gr.Markdown(
        """
        # AI-Powered Knowledge Management System
        Ask a question about your documents in English or Indonesian. The system will retrieve relevant information and generate an answer.
        """
    )
    with gr.Row():
        query_input = gr.Textbox(
            label="Enter your question",
            placeholder="Type your question here...",
            lines=3
        )
    
    submit_button = gr.Button("Get Answer")

    with gr.Column():
        answer_output = gr.Textbox(label="Answer", lines=10, interactive=False)
        sources_output = gr.Textbox(label="Sources", lines=5, interactive=False)

        gr.Examples(
            examples=[
                "What are the AI principles recommended by OJK?",
                "Apa saja prinsip AI yang bertanggung jawab menurut OJK?",
                "Summarize the document about digital banking transformation."
            ],
            inputs=query_input
        )

    submit_button.click(
        get_answer, 
        inputs=[query_input], 
        outputs=[answer_output, sources_output]
    ).then(lambda: "", outputs=query_input) # Clear input on submit

# --- LAUNCH THE APP ---
if __name__ == "__main__":
    print("Launching Gradio interface...")
    demo.launch()