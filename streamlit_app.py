import streamlit as st
import os
import google.generativeai as genai
from sentiment_llm import analyze_review   # <-- using our engine from sentiment_llm.py

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="Movie Sentiment Analyzer", page_icon="🎬")

st.title("🎬 Movie Review Sentiment Analyzer")
st.write("Paste a movie review below and get instant sentiment analysis.")

# User input
review_text = st.text_area("Enter your review:", height=150)

if st.button("Analyze"):
    if review_text.strip():
        with st.spinner("Analyzing..."):
            result = analyze_review(review_text)   # call our function
        st.subheader("Result")
        st.json(result)   # Pretty JSON display
    else:
        st.warning("⚠️ Please enter some review text first.")
