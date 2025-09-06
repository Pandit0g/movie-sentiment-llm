"""
LLM prompting logic for movie-review sentiment.
Returns a dict: {label, confidence, explanation, evidence_phrases}
"""
import os, json, re

try:
    import streamlit as st  # available only in Streamlit Cloud/app
except Exception:
    st = None

import google.generativeai as genai

MODEL_NAME = "gemini-1.5-flash"

def _get_api_key():
    # Prefer Streamlit Secrets when running on Streamlit Cloud
    if st is not None:
        try:
            return st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
    # Fallback to environment variables (Colab/local)
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

def _get_model(temperature: float = 0.2):
    key = _get_api_key()
    if not key:
        raise RuntimeError(
            "Missing API key. Set GEMINI_API_KEY (or GOOGLE_API_KEY) "
            "in Streamlit Secrets or as an environment variable."
        )
    genai.configure(api_key=key)
    return genai.GenerativeModel(
        MODEL_NAME,
        generation_config={
            "temperature": float(temperature),
            # Many SDK versions honor this; if ignored, we still JSON-parse below.
            "response_mime_type": "application/json",
        },
    )

FEW_SHOTS = [
    {
        "review": "A joyful, clever film with sharp writing and heartfelt performances.",
        "label": "Positive",
        "confidence": 0.92,
        "explanation": "Praise for writing and performances indicates strong approval.",
        "evidence_phrases": ["joyful", "clever", "sharp writing", "heartfelt performances"]
    },
    {
        "review": "Beautiful cinematography but the plot drags and the ending falls flat.",
        "label": "Neutral",
        "confidence": 0.62,
        "explanation": "Mixed signals: visuals praised while story criticized.",
        "evidence_phrases": ["Beautiful cinematography", "plot drags", "ending falls flat"]
    },
    {
        "review": "This was a mess—wooden acting and cringe-worthy dialogue.",
        "label": "Negative",
        "confidence": 0.90,
        "explanation": "Strong negative adjectives point to dislike.",
        "evidence_phrases": ["mess", "wooden acting", "cringe-worthy dialogue"]
    },
]

INSTRUCTIONS = """You are a careful movie-review sentiment judge.
Classify the review as one of: Positive, Negative, Neutral.
Be concise and ground your decision ONLY in the review text.
Return STRICT JSON with keys:
- label: "Positive" | "Negative" | "Neutral"
- confidence: float between 0 and 1 (your certainty from the language)
- explanation: 1–2 sentences grounded in the text
- evidence_phrases: list of 2–6 short phrases copied or closely paraphrased from the review
"""

def _build_prompt(user_review: str) -> str:
    rows = ["TASK:\n" + INSTRUCTIONS, "\nFEW-SHOTS:"]
    for eg in FEW_SHOTS:
        rows.append(json.dumps(eg, ensure_ascii=False))
    rows.append("\nREVIEW:\n" + user_review.strip())
    rows.append("\nRespond ONLY with the JSON object.")
    return "\n".join(rows)

def analyze_review(text: str, temperature: float = 0.2) -> dict:
    """Return dict(label, confidence, explanation, evidence_phrases)."""
    model = _get_model(temperature=temperature)
    prompt = _build_prompt(text)
    resp = model.generate_content(prompt)

    content = resp.text or ""

    # If the model adds extra text, extract the JSON block
    match = re.search(r"\{.*\}", content, re.S)
    j = content if match is None else match.group(0)

    try:
        data = json.loads(j)
    except Exception:
        data = {
            "label": "Neutral",
            "confidence": 0.5,
            "explanation": "Model response could not be parsed; defaulting to Neutral.",
            "evidence_phrases": [],
        }

    # Normalize
    data["label"] = str(data.get("label", "Neutral")).title()
    try:
        data["confidence"] = float(data.get("confidence", 0.5))
    except Exception:
        data["confidence"] = 0.5
    data["explanation"] = str(data.get("explanation", "")).strip()
    if not isinstance(data.get("evidence_phrases"), list):
        data["evidence_phrases"] = []
    return data
