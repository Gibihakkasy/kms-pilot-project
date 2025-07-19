from typing import List
from langchain.schema import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import token_logger, but don't fail if it's not available
try:
    from utils.token_logger import token_logger
    TOKEN_LOGGING_AVAILABLE = True
except ImportError:
    TOKEN_LOGGING_AVAILABLE = False
    print("[WARNING] Token logging not available")

def summarize_documents(llm: ChatOpenAI, documents: List[Document]) -> str:
    """
    Generate a structured summary of legal/regulatory documents using a refine chain.
    
    Args:
        llm: Initialized ChatOpenAI instance
        documents: List of LangChain Document objects to summarize
        
    Returns:
        str: Structured summary of the documents
    """
    print(f"Processing {len(documents)} document chunks...")
    
    # Define the prompt template for the initial summary
    prompt_template = """You are a legal expert summarizing regulatory documents in Indonesian.
    Your task is to provide a clear, structured summary focusing on key legal aspects.
    
    Document: {text}
    
    Please provide a detailed summary in Indonesian that includes the following sections:
    - [Ketentuan]: Ketentuan hukum dan pasal-pasal kunci
    - [Kewajiban]: Kewajiban dan persyaratan utama
    - [Pembatasan]: Setiap pembatasan atau larangan
    - [Sanksi]: Sanksi potensial untuk ketidakpatuhan
    - [Persyaratan Pelaporan]: Persyaratan pelaporan atau dokumentasi
    - [Catatan Lainnya]: Informasi penting tambahan
    
    Ringkasan:"""
    
    # Define the refine prompt
    refine_template = """Anda adalah ahli hukum yang menyempurnakan ringkasan dokumen peraturan.
    Tugas Anda adalah menggabungkan ringkasan yang ada dengan informasi baru.
    
    Ringkasan saat ini: {existing_answer}
    
    Informasi baru: {text}
    
    Sempurnakan ringkasan untuk memasukkan informasi baru sambil mempertahankan format terstruktur.
    Fokuslah untuk menambahkan detail baru, mengklarifikasi ambiguitas, dan memastikan konsistensi.
    
    Ringkasan yang disempurnakan:"""
    
    # Create prompt templates
    prompt = PromptTemplate.from_template(prompt_template)
    refine_prompt = PromptTemplate.from_template(refine_template)
    
    # Create and run the summarization chain with smaller chunks
    chain = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=False,
        verbose=True  # Show progress
    )
    
    # Process in smaller batches if there are many documents
    batch_size = 5
    total_batches = (len(documents) + batch_size - 1) // batch_size
    
    print(f"Processing in {total_batches} batches...")
    
    all_summaries = []
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        print(f"\nProcessing batch {i//batch_size + 1}/{total_batches}...")
        
        # Run the chain on this batch
        result = chain({"input_documents": batch}, return_only_outputs=True)
        batch_summary = result["output_text"]
        all_summaries.append(batch_summary)
        
        # Log summarization token usage for this batch
        if TOKEN_LOGGING_AVAILABLE:
            try:
                batch_text = "\n".join([doc.page_content for doc in batch])
                model_name = getattr(llm, 'model_name', 'gpt-4.1-nano') or 'gpt-4.1-nano'
                token_logger.log_summarization(batch_text, batch_summary, model_name, "document_batch")
            except Exception as e:
                print(f"[TOKEN LOGGING ERROR] Could not log summarization: {e}")
        
        print(f"Completed batch {i//batch_size + 1}/{total_batches}")
    
    # If we have multiple batches, combine the summaries
    if len(all_summaries) > 1:
        print("\nCombining batch summaries...")
        combined_summary = "\n\n".join(all_summaries)
        return combined_summary
    
    return all_summaries[0] if all_summaries else ""

if __name__ == "__main__":
    # Example usage
    from langchain.document_loaders import PyPDFLoader
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model_name="gpt-4.1-nano",  # or "gpt-3.5-turbo" if preferred
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Load a sample document
    pdf_path = input("Enter the path to the PDF file: ")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    # Generate and print the summary
    summary = summarize_documents(llm, docs)
    print("\n" + "="*80)
    print("SUMMARY:")
    print("="*80)
    print(summary)
