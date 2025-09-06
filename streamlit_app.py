import os, re
import streamlit as st

# Show a friendly message if the key isn't set (prevents import-time crash)
has_key = (
    ("GEMINI_API_KEY" in st.secrets)
    or bool(os.getenv("GEMINI_API_KEY"))
    or bool(os.getenv("GOOGLE_API_KEY"))
)

if not has_key:
    st.error(
        "API key not configured.\n\n"
        "In Streamlit Cloud: Manage app → Settings → Secrets → add\n"
        'GEMINI_API_KEY = "YOUR_REAL_KEY"\n\nThen click Rerun.'
    )
    st.stop()

from sentiment_llm import analyze_review  # safe to import after guard

st.set_page_config(page_title="Movie Sentiment Analyzer", page_icon="🎬")
st.title("🎬 Movie Review Sentiment Analyzer")
st.write("Paste a review, click **Analyze**, and get Label + Confidence + Explanation.")

temp = st.slider("Temperature (lower = more deterministic)", 0.0, 1.0, 0.2, 0.05)
review = st.text_area("Enter your movie review:", height=160)

def highlight_phrases(text, phrases):
    out = text
    for p in phrases or []:
        if not p: 
            continue
        pattern = re.compile(re.escape(p), flags=re.IGNORECASE)
        out = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", out)
    return out

if st.button("Analyze"):
    if review.strip():
        with st.spinner("Analyzing..."):
            result = analyze_review(review, temperature=temp)  # dict
        st.subheader("Result")
        st.json(result)

        st.markdown("**Evidence highlights in your text:**")
        st.markdown(
            highlight_phrases(review, result.get("evidence_phrases")),
            unsafe_allow_html=True,
        )
    else:
        st.warning("Please enter some text first.")
