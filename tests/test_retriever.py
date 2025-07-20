import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qa.retriever import Retriever

class TestRetriever(unittest.TestCase):
    @patch.object(Retriever, '__init__', lambda x: None)
    def test_retrieve_chunks_no_index(self):
        retriever = Retriever()
        retriever.index = None
        retriever.metadata = None
        results = retriever.retrieve_chunks("test query")
        self.assertEqual(results, [])

    @patch.object(Retriever, 'embed_query', return_value=None)
    def test_retrieve_chunks_no_embedding(self, mock_embed):
        retriever = Retriever()
        retriever.index = MagicMock()
        retriever.metadata = {}
        results = retriever.retrieve_chunks("test query")
        self.assertEqual(results, [])

if __name__ == "__main__":
    unittest.main() 