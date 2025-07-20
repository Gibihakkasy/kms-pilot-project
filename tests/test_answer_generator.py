import os
import sys
import unittest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qa.answer_generator import AnswerGenerator

class TestAnswerGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = AnswerGenerator()

    def test_generate_answer_with_chunks(self):
        query = "What is AI?"
        chunks = [
            {"text": "AI stands for Artificial Intelligence.", "metadata": {"file_name": "test.pdf", "page_number": 1}},
            {"text": "It is a field of computer science.", "metadata": {"file_name": "test.pdf", "page_number": 2}},
        ]
        answer = self.generator.generate_answer(query, chunks)
        self.assertIsInstance(answer, str)
        self.assertTrue(len(answer) > 0)

    def test_generate_answer_no_chunks(self):
        query = "What is AI?"
        chunks = []
        answer = self.generator.generate_answer(query, chunks)
        self.assertIn("could not find", answer.lower())

if __name__ == "__main__":
    unittest.main() 