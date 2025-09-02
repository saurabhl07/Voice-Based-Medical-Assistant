def extract_symptoms(text):
    """
    Dummy symptom extractor for testing.
    Replace with proper NLP extraction later.
    """
    # Simple example: just return known words
    keywords = ["fever", "cough", "diarrhoea", "headache", "nausea"]
    return [word for word in keywords if word in text.lower()]
