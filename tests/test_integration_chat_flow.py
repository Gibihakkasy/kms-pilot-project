import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app

class TestChatIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_chat_endpoint(self):
        payload = {
            "content": "Apa itu AI?",
            "conversation_history": []
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("content", data)
        self.assertIsInstance(data["content"], str)
        self.assertTrue(len(data["content"]) > 0)

if __name__ == "__main__":
    unittest.main() 