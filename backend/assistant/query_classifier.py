def classify_intent(query: str) -> str:
    """
    Classify the user query as either 'qa' (question answering) or 'summarize' (summarization request).
    Uses simple keyword-based heuristics.
    """
    summarize_keywords = [
        'summarize', 'summary', 'ringkas', 'ikhtisar', 'resume', 'intisari',
        'give me a summary', 'can you summarize', 'summarization', 'summarize page', 'summarize section',
        'what is the summary', 'buatkan ringkasan', 'tolong ringkas', 'mohon ringkasan', 'berikan ringkasan'
    ]
    query_lower = query.lower()
    for kw in summarize_keywords:
        if kw in query_lower:
            return 'summarize'
    return 'qa' 