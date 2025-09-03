import streamlit as st
import io
import speech_recognition as sr
from rag.responder_local import generate_response_local  # Your Gemini logic
from streamlit_audiorec import st_audiorec

st.set_page_config(page_title="Voice-Based Medical Assistant", layout="centered")

st.title("Voice-Based Medical Assistant (Browser Mic + Gemini API)")
st.markdown("**Speak your symptoms and get a medical suggestion.**")

# Browser-based audio recorder
audio_bytes = st_audiorec()

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio = recognizer.record(source)

    try:
        user_input = recognizer.recognize_google(audio)
        st.markdown(f"**You said:** `{user_input}`")
        response, symptoms = generate_response_local(user_input)
        st.markdown(f"**Detected Symptoms:** `{', '.join(symptoms) if symptoms else 'None'}`")
        st.markdown(f"**AI Response:**\n\n{response}")
    except Exception as e:
        st.error(f"Could not transcribe audio: {e}")
