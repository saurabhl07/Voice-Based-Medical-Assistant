# main.py

import streamlit as st
from audio.transcriber import transcribe_audio
from rag.responder_local import generate_response_local

st.set_page_config(page_title="Medical Assistant", layout="centered")

st.title("Voice-Based Medical Assistant (Offline + Gemini API)")
st.markdown("**Speak your symptoms and get a medical suggestion.**")

if st.button("🎙 Speak Now"):
    with st.spinner("Listening..."):
        user_input = transcribe_audio()
        st.success("Recording complete")
        st.markdown(f"**You said:** `{user_input}`")

    if user_input.strip():
        with st.spinner("Generating response..."):
            response, symptoms = generate_response_local(user_input)

        st.success("Done")
        st.markdown(f"**Detected Symptoms:** `{', '.join(symptoms) if symptoms else 'None'}`")
        st.markdown(f"**AI Response:**\n\n{response}")
    else:
        st.error("Didn't catch that. Please try again.")
