from fastapi import FastAPI
import requests
import os

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
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

- 3 Key Bullet Points
- 1-Sentence TL;DR Summary

Text:
{text}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_URL, json=body, headers=headers)
    output = response.json()

    try:
        result = output["choices"][0]["message"]["content"]
    except Exception as e:
        print("OpenRouter response:", output)
        result = f"Error: Could not generate summary. {str(e)}"

    return {"summary": result}


@app.post("/sentiment")
def sentiment(payload: dict):
    text = payload.get("text", "")

    if not text:
        return {"error": "No text provided."}

    prompt = f"""
Analyze the sentiment of the following text.
Provide:

- Sentiment: Positive, Neutral, or Negative
- Confidence (0–1)
- One-sentence explanation

Text:
{text}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_URL, json=body, headers=headers)
    output = response.json()

    try:
        result = output["choices"][0]["message"]["content"]
    except Exception as e:
        print("OpenRouter response:", output)
        result = f"Error: Could not analyze sentiment. {str(e)}"

    return {"sentiment": result}

