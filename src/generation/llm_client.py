import os

from google import genai
from google.genai import types

from src.config import (
    PRIMARY_MODEL,
    FALLBACK_MODEL,
    GEMINI_API_KEY_ENV,
)


api_key = os.getenv(GEMINI_API_KEY_ENV)

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=api_key)


def generate_answer(prompt):
    """Generate an answer using Gemini with Google Search grounding."""

    google_search_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    try:
        response = client.models.generate_content(
            model=PRIMARY_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[google_search_tool]
            ),
        )

        return {
            "answer": response.text,
            "model": PRIMARY_MODEL,
        }

    except Exception:
        print("Primary model failed. Using fallback model...")

        try:
            response = client.models.generate_content(
                model=FALLBACK_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[google_search_tool]
                ),
            )

            return {
                "answer": response.text,
                "model": FALLBACK_MODEL,
            }

        except Exception:
            return {
                "answer": "Sorry, the AI service is currently unavailable.",
                "model": None,
            }