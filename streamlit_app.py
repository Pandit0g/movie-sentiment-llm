# streamlit_app.py
import os
import streamlit as st

# quick pre-check so we can render a helpful UI instead of crashing
has_key = (
    ("GEMINI_API_KEY" in st.secrets)
    or bool(os.getenv("GEMINI_API_KEY"))
    or bool(os.getenv("GOOGLE_API_KEY"))
)

if not has_key:
    st.error(
        "API key not configured.\n\n"
        "In Streamlit Cloud: Manage app → Settings → Secrets → add\n"
        'GEMINI_API_KEY = "YOUR_REAL_KEY"\n\n'
        "Then click Rerun."
    )
    st.stop()

from sentiment_llm import analyze_review  # safe to import now

st.set_page_config(page_title="Movie Sentiment Analyzer", page_icon="🎬")
st.title("🎬 Movie Review Sentiment Analyzer")
st.write("Paste a movie review below and get instant sentiment analysis.")

review_text = st.text_area("Enter your review:", height=150)

if st.button("Analyze"):
    if review_text.strip():
        with st.spinner("Analyzing..."):
            result = analyze_review(review_text)  # returns a string
        st.subheader("Result")
        st.write(result)
    else:
        st.warning("Please enter some review text first.")
