import google.generativeai as genai
import os

# Configure Gemini API (expects your API key in environment variable)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def analyze_review(review_text: str):
    """
    Analyze a movie review using Gemini.
    Returns JSON with label, confidence, explanation, and evidence phrases.
    """

    prompt = f"""
    You are a movie review sentiment analyzer.
    Review: {review_text}
    Task: Classify as Positive, Negative, or Neutral.
    Return JSON with fields:
    - label (Positive/Negative/Neutral)
    - confidence (0 to 1)
    - explanation (short reason grounded in text)
    - evidence_phrases (key phrases that justify sentiment)
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    try:
        return eval(response.text)  # assumes Gemini returns JSON-like
    except:
        return {
            "label": "Error",
            "confidence": 0.0,
            "explanation": "Parsing issue",
            "evidence_phrases": []
        }
