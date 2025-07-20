import os
import json
import numpy as np
import faiss
from openai import OpenAI
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


# Add project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from ingest.pdf_loader import load_and_chunk_pdfs
from utils.token_logger import token_logger

# --- Configuration ---
EMBEDDING_MODEL = "text-embedding-3-large"
FAISS_INDEX_PATH = os.path.join(project_root, 'embeddings', 'index.faiss')
METADATA_PATH = os.path.join(project_root, 'embeddings', 'metadata.json')
DOCUMENTS_DIR = os.path.join(project_root, 'documents')

def get_openai_client():
    """Initializes and returns the OpenAI client, checking for API key."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)

def embed_chunks(chunks):
    """
    Generates embeddings for a list of text chunks using OpenAI, batching requests to stay under the 300,000 token limit using tiktoken for accurate counting.
    """
    import tiktoken
    client = get_openai_client()
    texts = [chunk['text'] for chunk in chunks]
    max_tokens_per_request = 300000

    # Use tiktoken for the OpenAI embedding model
    try:
        encoding = tiktoken.encoding_for_model(EMBEDDING_MODEL)
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(text):
        return len(encoding.encode(text))

    batches = []
    current_batch = []
    current_tokens = 0
    for text in texts:
        tokens = count_tokens(text)
        if tokens > max_tokens_per_request:
            print(f"Warning: A single chunk exceeds the max token limit and will be processed alone (length: {tokens} tokens).")
            if current_batch:
                batches.append(current_batch)
                current_batch = []
                current_tokens = 0
            batches.append([text])
            continue
        if current_tokens + tokens > max_tokens_per_request:
            if current_batch:
                batches.append(current_batch)
            current_batch = [text]
            current_tokens = tokens
        else:
            current_batch.append(text)
            current_tokens += tokens
    if current_batch:
        batches.append(current_batch)

    all_embeddings = []
    try:
        for i, batch in enumerate(batches):
            print(f"Requesting embeddings for batch {i+1}/{len(batches)} (batch size: {len(batch)})...")
            # Log embedding token usage for this batch
            batch_text = "\n".join(batch)
            token_logger.log_embedding(batch_text, EMBEDDING_MODEL, f"batch_{i+1}")
            response = client.embeddings.create(input=batch, model=EMBEDDING_MODEL)
            all_embeddings.extend([item.embedding for item in response.data])
        return np.array(all_embeddings, dtype='float32')
    except Exception as e:
        print(f"An error occurred while generating embeddings: {e}")
        return None


def create_and_save_vector_store():
    """
    Loads PDF chunks, generates embeddings, and saves them to a FAISS index.
    """
    print("Loading and chunking PDFs...")
    chunks = load_and_chunk_pdfs(DOCUMENTS_DIR)
    if not chunks:
        print("No chunks were loaded. Aborting.")
        return

    print(f"Generating embeddings for {len(chunks)} chunks...")
    embeddings = embed_chunks(chunks)
    if embeddings is None:
        print("Failed to generate embeddings. Aborting.")
        return

    # Create a FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIDMap(index)

    # Add vectors to the index with their original indices as IDs
    ids = np.arange(len(chunks))
    index.add_with_ids(embeddings, ids) # type: ignore

    print(f"Saving FAISS index to {FAISS_INDEX_PATH}")
    faiss.write_index(index, FAISS_INDEX_PATH)

    # Save metadata
    # Save metadata, now including the text for context
    metadata = {str(i): chunk for i, chunk in enumerate(chunks)}
    print(f"Saving metadata to {METADATA_PATH}")
    with open(METADATA_PATH, 'w') as f:
        json.dump(metadata, f, indent=4)

    print("\nVector store created successfully!")
    print(f"- FAISS index saved at: {FAISS_INDEX_PATH}")
    print(f"- Metadata saved at: {METADATA_PATH}")

if __name__ == '__main__':
    # Make sure to set your OPENAI_API_KEY environment variable before running
    # Example: export OPENAI_API_KEY='your_key_here'
    create_and_save_vector_store()