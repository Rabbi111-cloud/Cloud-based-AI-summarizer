from fastapi import FastAPI
import requests
import os

app = FastAPI()

# Load API key correctly
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY not found! Add it in Render dashboard.")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


@app.get("/")
def home():
    return {"status": "running", "service": "AI Summarizer & Sentiment Analyzer"}


@app.post("/summarize")
def summarize(payload: dict):
    text = payload.get("text", "")

    if not text:
        return {"error": "No text provided."}

    prompt = f"""
Summarize the following text in:

• 3 Key Bullet Points
• 1-Sentence TL;DR Summary

Text:
{text}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-render-service.com",
        "X-Title": "AI Text Summarizer"
    }

    body = {
        "model": "openai/gpt-4o-mini",   # CORRECT model name
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_URL, json=body, headers=headers)

    # DEBUG PRINT
    print("RAW RESPONSE:", response.text)

    try:
        output = response.json()
        result = output["choices"][0]["message"]["content"]
        return {"summary": result}

    except Exception as e:
        return {
            "summary": None,
            "error": "OpenRouter did not return a valid response.",
            "details": str(e),
            "raw_response": response.text
        }


@app.post("/sentiment")
def sentiment(payload: dict):
    text = payload.get("text", "")

    if not text:
        return {"error": "No text provided."}

    prompt = f"""
Analyze the sentiment of the following text.
Provide:

- Sentiment (Positive, Neutral, or Negative)
- Confidence (0–1)
- A one-sentence explanation

Text:
{text}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-render-service.com",
        "X-Title": "AI Sentiment Analyzer"
    }

    body = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_URL, json=body, headers=headers)

    # DEBUG PRINT
    print("RAW SENTIMENT RESPONSE:", response.text)

    try:
        output = response.json()
        result = output["choices"][0]["message"]["content"]
        return {"sentiment": result}

    except Exception as e:
        return {
            "sentiment": None,
            "error": "OpenRouter did not return a valid response.",
            "details": str(e),
            "raw_response": response.text
        }

