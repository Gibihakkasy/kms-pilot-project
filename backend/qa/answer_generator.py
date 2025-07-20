import os
import sys
from typing import List, Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

# Add the project root to the Python path to allow for package-like imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qa.retriever import Retriever
from utils.token_logger import token_logger

load_dotenv()

class AnswerGenerator:
    """Generates answers using an LLM based on a query and retrieved context."""

    def __init__(self, model: str = "gpt-4.1-nano"):
        """Initializes the AnswerGenerator with an OpenAI client."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate_answer(self, query: str, chunks: List[Dict[str, Any]], previous_questions: str = "", summarized_history: str = "") -> str:
        """
        Generates an answer by synthesizing information from retrieved chunks.

        Args:
            query: The user's question.
            chunks: A list of dictionaries, where each dictionary is a retrieved chunk
                    containing text and metadata.
            previous_questions: (Optional) String of previous Q&A pairs to include in the prompt.
            summarized_history: (Optional) Summarized history string to include in the prompt.

        Returns:
            A string containing the generated answer.
        """
        if not chunks:
            return "I could not find any relevant information in the documents to answer your question."

        # Combine the text from all chunks to form the context
        context = "\n\n---\n\n".join([chunk['text'] for chunk in chunks])

        # Build prompt sections
        prompt_sections = []
        previous_questions = previous_questions or ""
        summarized_history = summarized_history or ""
        if summarized_history:
            prompt_sections.append(f"Summarized Conversation:\n{summarized_history}")
        if previous_questions:
            prompt_sections.append(f"Previous Q&A:\n{previous_questions}")
        prompt_sections.append(f"Vector Search Result:\n{context}")
        prompt_sections.append(f"User Question:\n{query}")
        prompt = "\n\n====\n\n".join(prompt_sections) + "\n\nAnswer:"

        # Log the prompt
        try:
            with open("logs/answer_generator_prompt.log", "a", encoding="utf-8") as logf:
                logf.write("\n\n====================\nPROMPT SENT TO LLM\n====================\n")
                logf.write(prompt)
                logf.write("\n====================\nEND PROMPT\n====================\n")
        except Exception as e:
            print(f"[LOGGING ERROR] Could not write prompt log: {e}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Lower temperature for more factual answers
            )
            content = response.choices[0].message.content
            answer = content.strip() if content else "The model did not return a valid answer."
            
            # Log token usage using the comprehensive token logger
            token_logger.log_answer_generation(prompt, answer, self.model, query)
            
            return answer
        except Exception as e:
            print(f"An error occurred while generating the answer: {e}")
            return "I encountered an error while trying to generate an answer. Please try again."

if __name__ == '__main__':
    # This demonstrates the full pipeline: retrieve and then generate an answer
    retriever = Retriever()
    answer_generator = AnswerGenerator()

    # --- Test Case 1: Indonesian Query ---
    test_query_id = "Apa saja prinsip dasar AI yang bertanggung jawab menurut OJK?"
    print(f"\n--- Testing Query: '{test_query_id}' ---")
    
    retrieved_chunks_id = retriever.retrieve_chunks(test_query_id, k=3)
    
    if retrieved_chunks_id:
        print(f"Retrieved {len(retrieved_chunks_id)} chunks.")
        final_answer_id = answer_generator.generate_answer(test_query_id, retrieved_chunks_id)
        
        print("\n--- Generated Answer ---")
        print(final_answer_id)
        
        print("\n--- Sources ---")
        for i, chunk in enumerate(retrieved_chunks_id, 1):
            print(f"{i}. {chunk['metadata']['file_name']} (Page {chunk['metadata']['page_number']})")
        print("------------------------\n")
    else:
        print("No chunks were retrieved for this query.")

    # --- Test Case 2: English Query ---
    test_query_en = "What are the steps for digital resilience?"
    print(f"\n--- Testing Query: '{test_query_en}' ---")

    retrieved_chunks_en = retriever.retrieve_chunks(test_query_en, k=3)

    if retrieved_chunks_en:
        print(f"Retrieved {len(retrieved_chunks_en)} chunks.")
        final_answer_en = answer_generator.generate_answer(test_query_en, retrieved_chunks_en)

        print("\n--- Generated Answer ---")
        print(final_answer_en)

        print("\n--- Sources ---")
        for i, chunk in enumerate(retrieved_chunks_en, 1):
            print(f"{i}. {chunk['metadata']['file_name']} (Page {chunk['metadata']['page_number']})")
        print("------------------------\n")
    else:
        print("No chunks were retrieved for this query.")