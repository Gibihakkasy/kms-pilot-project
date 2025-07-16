import os
import fitz  # PyMuPDF
import uuid
from typing import List, Dict, Any

def load_and_chunk_pdfs(pdf_folder: str) -> List[Dict[str, Any]]:
    """
    Loads PDFs from a folder, extracts text, and splits it into chunks.

    Args:
        pdf_folder: The path to the folder containing PDF files.

    Returns:
        A list of dictionaries, where each dictionary represents a chunk.
    """
    all_chunks = []
    if not os.path.isdir(pdf_folder):
        print(f"Error: Directory '{pdf_folder}' not found.")
        return []

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(pdf_folder, filename)
            try:
                doc = fitz.open(file_path)
                for page_num, page in enumerate(doc, start=1):
                    text = page.get_text().strip()
                    if not text:
                        continue  # Skip blank pages

                    # Simple chunking by splitting text into words
                    words = text.split()
                    chunk_size = 400  # Approximate words per chunk
                    for i in range(0, len(words), chunk_size):
                        chunk_text = " ".join(words[i:i + chunk_size])
                        chunk_id = str(uuid.uuid4())
                        
                        chunk_data = {
                            "text": chunk_text,
                            "metadata": {
                                "file_name": filename,
                                "page_number": page_num,
                                "chunk_id": chunk_id
                            }
                        }
                        all_chunks.append(chunk_data)
                doc.close()
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    return all_chunks

if __name__ == '__main__':
    # Example usage:
    # 1. Make sure you have a 'documents' folder in your project root.
    # 2. Place some PDF files inside the 'documents' folder.
    # 3. Run this script from the project root: python ingest/pdf_loader.py
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    documents_folder = os.path.join(project_root, 'documents')

    if not os.path.exists(documents_folder):
        os.makedirs(documents_folder)
        print(f"Created directory: {documents_folder}")
        print("Please add PDF files to the 'documents' directory to test the script.")
    
    pdf_chunks = load_and_chunk_pdfs(documents_folder)

    if pdf_chunks:
        print(f"Successfully extracted {len(pdf_chunks)} chunks.")
        # Print details of the first chunk as a sample
        print("\n--- Sample Chunk ---")
        print(f"Text: {pdf_chunks[0]['text'][:200]}...")
        print(f"Metadata: {pdf_chunks[0]['metadata']}")
        print("--------------------\n")
    else:
        print("No chunks were extracted. Check if the 'documents' folder contains PDF files.")