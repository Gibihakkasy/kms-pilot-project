from assistant.query_classifier import classify_intent
from qa.answer_generator import AnswerGenerator
from qa.retriever import Retriever
from chains.summarization_refine_chain import summarize_documents
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
import os

MAX_HISTORY_PAIRS = 5

# Helper to truncate history and summarize if needed
def _prepare_context(history):
    """
    history: list of (user, assistant) tuples
    Returns: (context_history, summary_text or None)
    """
    if not history:
        return [], None
    if len(history) <= MAX_HISTORY_PAIRS:
        return history, None
    # Summarize older turns
    to_summarize = history[:-MAX_HISTORY_PAIRS]
    recent = history[-MAX_HISTORY_PAIRS:]
    # Format as chat for summarization
    chat_text = ""
    for user, assistant in to_summarize:
        chat_text += f"User: {user}\nAssistant: {assistant}\n"
    summary = "[Summary unavailable]"
    if ChatOpenAI is not None:
        try:
            llm = ChatOpenAI(model_name="gpt-4.1-nano", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
            prompt = f"Summarize the following conversation between a user and an assistant. Focus on the key topics, questions, and answers discussed so far.\n\n{chat_text}\n\nSummary:"
            response = llm.invoke(prompt)
            summary = response.content.strip() if hasattr(response, 'content') else str(response)
        except Exception as e:
            summary = "[Summary unavailable due to error]"
    return recent, summary

def _extract_sources_from_chunks(chunks):
    sources = []
    for chunk in chunks:
        meta = chunk.get('metadata', {})
        sources.append({
            'document': meta.get('file_name'),
            'page': meta.get('page_number')
        })
    return sources

def _build_context_string(history, summary=None):
    context = ""
    if summary:
        context += f"Previous conversation summary:\n{summary}\n\n"
    for user, assistant in history:
        context += f"User: {user}\nAssistant: {assistant}\n"
    return context

def run_assistant(user_query, history=None):
    """
    Main entry point for the LangGraph assistant flow.
    Args:
        user_query (str): The user's query.
        history (list): List of (user, assistant) tuples.
    Returns:
        dict: Structured response with type, content, and sources.
    """
    history = history or []
    context_history, summary = _prepare_context(history)
    context_str = _build_context_string(context_history, summary)
    intent = classify_intent(user_query)
    if intent == 'summarize':
        retriever = Retriever()
        if ChatOpenAI is not None and summarize_documents is not None:
            llm = ChatOpenAI(model_name="gpt-4.1-nano", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
            # Use both user_query and context_str for retrieval
            retrieval_query = f"{context_str}\nCurrent user request: {user_query}"
            chunks = retriever.retrieve_chunks(retrieval_query, k=5)
            if chunks:
                docs = [Document(page_content=chunk['text'], metadata=chunk['metadata']) for chunk in chunks]
                # Pass context as part of the prompt if possible
                summary_prompt = f"{context_str}\nSummarize the following content based on the conversation above and the user request: {user_query}"
                # Optionally, inject context into the first doc
                if docs:
                    docs[0].page_content = summary_prompt + "\n" + docs[0].page_content
                summary_text = summarize_documents(llm, docs)
                sources = _extract_sources_from_chunks(chunks)
            else:
                summary_text = "I could not find relevant content to summarize."
                sources = []
        else:
            summary_text = "Summarization functionality is not available."
            sources = []
        return {
            "type": "summary",
            "content": summary_text,
            "sources": sources
        }
    else:
        retriever = Retriever()
        answer_generator = AnswerGenerator()
        # Use both user_query and context_str for retrieval
        retrieval_query = f"{context_str}\nCurrent user question: {user_query}"
        chunks = retriever.retrieve_chunks(retrieval_query, k=5)
        if chunks:
            # Pass context to the LLM by prepending to the prompt
            context_for_llm = f"{context_str}\nUser: {user_query}"
            # Patch: inject context into the first chunk for the LLM
            if chunks:
                chunks[0]['text'] = context_for_llm + "\n" + chunks[0]['text']
            answer = answer_generator.generate_answer(user_query, chunks)
            sources = _extract_sources_from_chunks(chunks)
        else:
            answer = "I could not find relevant information to answer your question."
            sources = []
        return {
            "type": "answer",
            "content": answer,
            "sources": sources
        } 