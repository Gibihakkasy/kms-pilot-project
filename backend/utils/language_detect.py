from langdetect import detect, LangDetectException

def detect_language(text: str) -> str:
    """
    Detects the language of a given text string.

    Args:
        text: The input text.

    Returns:
        The ISO 639-1 language code ('en', 'id') or 'unknown' if detection fails.
    """
    if not text or not text.strip():
        return 'unknown'
    
    try:
        # Detect the language
        lang = detect(text)
        # We are primarily concerned with English and Indonesian
        if lang in ['en', 'id']:
            return lang
        else:
            # Return the detected language if it's something else but supported
            # For this project, we'll consider other languages as 'unknown' for simplicity
            return 'unknown'
    except LangDetectException:
        # This exception is thrown for texts that are too short or ambiguous
        return 'unknown'

if __name__ == '__main__':
    # --- Test Cases ---
    test_texts = {
        "English Query": "What are the main principles of responsible AI?",
        "Indonesian Query": "Apa saja prinsip utama AI yang bertanggung jawab?",
        "Mixed Language": "This is a test, apa kabar? I hope you are well.",
        "Short Text": "Test",
        "Empty Text": "",
        "Japanese Text": "こんにちは世界"
    }

    for name, text in test_texts.items():
        detected_lang = detect_language(text)
        print(f"- Query: '{text}'")
        print(f"  Detected Language: {detected_lang}\n")