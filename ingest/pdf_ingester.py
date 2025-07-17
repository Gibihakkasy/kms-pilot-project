"""
PDF ingestion and chunking using LangChain's PyMuPDFLoader and RecursiveCharacterTextSplitter.
"""
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
from typing import List


def load_and_chunk_pdfs_langchain(pdf_folder: str) -> List[Document]:
    """
    Loads PDFs from a folder, splits into chunks, and attaches metadata using LangChain.

    Args:
        pdf_folder: Path to the folder containing PDF files.

    Returns:
        List of LangChain Document objects with page_content and metadata.
    """
    all_docs = []
    if not os.path.isdir(pdf_folder):
        print(f"Error: Directory '{pdf_folder}' not found.")
        return []

    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    for filename in pdf_files:
        file_path = os.path.join(pdf_folder, filename)
        try:
            loader = PyMuPDFLoader(file_path)
            pages = loader.load()
            for page in pages:
                # Each page is a Document with page_content and metadata
                text = page.page_content
                page_num = page.metadata.get('page_number', None)
                metadata = {
                    'file_name': filename,
                    'page_number': page_num
                }
                # Optionally add doc_title or language if available
                if 'title' in page.metadata:
                    metadata['doc_title'] = page.metadata['title']
                if 'language' in page.metadata:
                    metadata['language'] = page.metadata['language']
                # Chunk the page
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=100,
                    separators=["\n\n", "\n", ".", " ", ""]
                )
                chunks = splitter.split_text(text)
                for chunk_text in chunks:
                    doc = Document(page_content=chunk_text, metadata=metadata.copy())
                    all_docs.append(doc)
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
    return all_docs

if __name__ == "__main__":
    # Example usage for testing
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    documents_folder = os.path.join(project_root, 'documents')
    docs = load_and_chunk_pdfs_langchain(documents_folder)
    print(f"Extracted {len(docs)} chunks.")
    if docs:
        print("\n--- Sample Chunk ---")
        print(f"Text: {docs[0].page_content[:200]}...")
        print(f"Metadata: {docs[0].metadata}")
        print("--------------------\n")
    else:
        print("No chunks were extracted. Check if the 'documents' folder contains PDF files.")
