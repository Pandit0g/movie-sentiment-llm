# sentiment_llm.py
import os
import google.generativeai as genai

try:
    import streamlit as st
except Exception:
    st = None


def _get_api_key():
    # Prefer Streamlit Secrets when available
    if st is not None:
        try:
            return st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
    # Fallback to environment variables
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def _get_model():
    api_key = _get_api_key()
    if not api_key:
        # raise here, but only when we actually need the model
        raise RuntimeError(
            "Missing API key. Set GEMINI_API_KEY (or GOOGLE_API_KEY) "
            "in Streamlit Secrets or as an environment variable."
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def analyze_review(text: str) -> str:
    model = _get_model()
    resp = model.generate_content(
        "Classify the sentiment of this movie review as 'positive' or 'negative':\n\n" + text
    )
    return (resp.text or "").strip()
