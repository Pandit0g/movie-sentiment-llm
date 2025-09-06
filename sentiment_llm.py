import os
import streamlit as st
import google.generativeai as genai

def _get_api_key():
    # Prefer Streamlit Secrets
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]

    # Fallback to env vars
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        # Helpful error – caught by streamlit_app.py if you use the guard above
        raise RuntimeError(
            "Missing API key. Set GEMINI_API_KEY (or GOOGLE_API_KEY) in Streamlit Secrets "
            "or as an environment variable."
        )
    return key

genai.configure(api_key=_get_api_key())

def analyze_review(text: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    resp = model.generate_content(
        "Classify the sentiment of this movie review as 'positive' or 'negative':\n\n" + text
    )
    return (resp.text or "").strip()
