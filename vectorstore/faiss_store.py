"""
FAISS vector store creation with plug-and-play embedding backend (HuggingFace or OpenAI) using LangChain.
"""
import os
import json
from typing import List, Literal
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from ingest.pdf_ingester import load_and_chunk_pdfs_langchain

DEFAULT_MODEL = "BAAI/bge-base-id"
VECTORSTORE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(VECTORSTORE_DIR, "index.faiss")
METADATA_PATH = os.path.join(VECTORSTORE_DIR, "metadata.json")


def get_embedding_backend(backend: Literal["huggingface", "openai"] = "huggingface"):
    """
    Returns a LangChain embedding object for the selected backend.
    """
    if backend == "huggingface":
        return HuggingFaceEmbeddings(
            model_name=DEFAULT_MODEL,
            encode_kwargs={"normalize_embeddings": True}
        )
    elif backend == "openai":
        return OpenAIEmbeddings()
    else:
        raise ValueError(f"Unknown embedding backend: {backend}")


def create_and_save_faiss_store(
    pdf_folder: str,
    backend: Literal["huggingface", "openai"] = "huggingface"
):
    """
    Loads chunked documents, generates embeddings, and saves FAISS index and metadata.
    """
    print(f"Loading and chunking PDFs from {pdf_folder}...")
    docs = load_and_chunk_pdfs_langchain(pdf_folder)
    if not docs:
        print("No chunks were loaded. Aborting.")
        return

    print(f"Generating embeddings for {len(docs)} chunks using {backend} backend...")
    embeddings = get_embedding_backend(backend)
    try:
        vectorstore = FAISS.from_documents(docs, embeddings)
    except Exception as e:
        print(f"Error creating FAISS vectorstore: {e}")
        return

    print(f"Saving FAISS index to {INDEX_PATH}")
    vectorstore.save_local(VECTORSTORE_DIR)

    # Save metadata (page_content + metadata for each chunk)
    metadata = {
        str(i): {"text": doc.page_content, "metadata": doc.metadata}
        for i, doc in enumerate(docs)
    }
    print(f"Saving metadata to {METADATA_PATH}")
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)

    print("\nVector store created successfully!")
    print(f"- FAISS index saved at: {INDEX_PATH}")
    print(f"- Metadata saved at: {METADATA_PATH}")

if __name__ == "__main__":
    # Example CLI usage
    import argparse
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    documents_folder = os.path.join(project_root, "documents")
    parser = argparse.ArgumentParser(description="Create FAISS vector store with selected embedding backend.")
    parser.add_argument("--backend", choices=["huggingface", "openai"], default="huggingface", help="Embedding backend to use.")
    parser.add_argument("--pdf_folder", default=documents_folder, help="Folder containing PDFs.")
    args = parser.parse_args()
    create_and_save_faiss_store(args.pdf_folder, args.backend)
