# sentiment_llm.py
import os
import streamlit as st
import google.generativeai as genai


def _get_api_key():
    # 1) Prefer Streamlit Secrets if available
    if st and "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]

    # 2) Fallback to environment variables
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError(
            "❌ Missing API key. Set GEMINI_API_KEY (or GOOGLE_API_KEY) "
            "in Streamlit Secrets or as an environment variable."
        )
    return key


# Configure Gemini only once
genai.configure(api_key=_get_api_key())


def analyze_review(text: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    resp = model.generate_content(
        f"Classify the sentiment of this movie review as 'positive' or 'negative':\n\n{text}"
    )
    return resp.text.strip()
