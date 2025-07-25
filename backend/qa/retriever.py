import os
import json
import numpy as np
import faiss
from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAISS_INDEX_PATH = os.path.join(project_root, 'embeddings', 'index.faiss')
METADATA_PATH = os.path.join(project_root, 'embeddings', 'metadata.json')
EMBEDDING_MODEL = "text-embedding-3-large"

class Retriever:
    def __init__(self):
        """Initializes the retriever, loading the FAISS index and metadata."""
        print("Initializing retriever...")
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = OpenAI(api_key=self.api_key)
        self.index_path = FAISS_INDEX_PATH
        self.metadata_path = METADATA_PATH
        
        try:
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)
            print("Retriever initialized successfully.")
        except Exception as e:
            print(f"Error initializing retriever: {e}")
            print("Please ensure 'embeddings/index.faiss' and 'embeddings/metadata.json' exist.")
            print("You can generate them by running 'embeddings/vector_store.py'.")
            self.index = None
            self.metadata = None

    def embed_query(self, query: str) -> Optional[np.ndarray]:
        """Generates an embedding for the user's query."""
        try:
            response = self.client.embeddings.create(input=[query], model=EMBEDDING_MODEL)
            return np.array(response.data[0].embedding, dtype='float32').reshape(1, -1)
        except Exception as e:
            print(f"An error occurred while embedding the query: {e}")
            return None

    def retrieve_chunks(self, query: str, k: int = 5) -> list:
        """Retrieves the top-k most relevant chunks for a given query."""
        if not self.index or not self.metadata:
            print("Retriever is not initialized. Cannot retrieve chunks.")
            return []

        query_embedding = self.embed_query(query)
        if query_embedding is None:
            return []

        # Search the FAISS index
        distances, indices = self.index.search(query_embedding, k)

        # Collect the results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # FAISS returns -1 for no result
                chunk_metadata = self.metadata.get(str(idx))
                if chunk_metadata:
                    # Assuming you might want the text later, for now just metadata
                    # You would typically load the text from a source or have it in metadata
                    # The entire chunk data (including text) is now in metadata
                    chunk_data = self.metadata.get(str(idx))
                    if chunk_data:
                        chunk_data['retrieval_score'] = float(distances[0][i])
                        results.append(chunk_data)
        return results