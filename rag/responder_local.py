import os
import requests
from dotenv import load_dotenv
from nlp.symptom_extractor import extract_symptoms  # your module
from tts.speaker import speak                        # your TTS module

# Load .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
if not API_KEY:
    raise ValueError("Set GOOGLE_GENAI_API_KEY in .env")

def generate_response_local(user_input: str):
    """
    Generate medical response using Gemini API
    """
    # Extract symptoms
    symptoms = extract_symptoms(user_input)

    # Prepare prompt
    prompt_text = f"""
You are a helpful offline medical assistant.

Patient says: {user_input}
Detected symptoms: {', '.join(symptoms) if symptoms else 'None'}

Give a short and medically useful reply.
"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }
    body = {"contents": [{"parts": [{"text": prompt_text}]}]}

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()

    # Extract generated text safely
    try:
        generated_text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        generated_text = "No response generated"

    # Speak
    speak(generated_text)

    return generated_text, symptoms

# ---------------- TEST ----------------
if __name__ == "__main__":
    user_input = input("Enter patient symptoms: ")
    reply, symptoms = generate_response_local(user_input)
    print("\nDetected Symptoms:", symptoms)
    print("AI Response:", reply)
