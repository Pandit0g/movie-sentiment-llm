import streamlit as st
from sentiment_llm import analyze_review   # <- handles API key & Gemini config

# Streamlit UI
st.set_page_config(page_title="Movie Sentiment Analyzer", page_icon="🎬")

st.title("🎬 Movie Review Sentiment Analyzer")
st.write("Paste a movie review below and get instant sentiment analysis.")

# User input
review_text = st.text_area("Enter your review:", height=150)

if st.button("Analyze"):
    if review_text.strip():
        with st.spinner("Analyzing..."):
            result = analyze_review(review_text)  # string result
        st.subheader("Result")
        st.write(result)  # ✅ Use write instead of json
    else:
        st.warning("⚠️ Please enter some review text first.")
