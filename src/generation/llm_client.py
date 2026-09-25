import streamlit as st

from google import genai

from src.config import (
    PRIMARY_MODEL,
    FALLBACK_MODEL,
    GEMINI_API_KEY_ENV,
)


api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=api_key)


def generate_answer(prompt):
    """Generate an answer using Gemini."""

    try:
        response = client.models.generate_content(
            model=PRIMARY_MODEL,
            contents=prompt,
        )

        return {
            "answer": response.text,
            "model": PRIMARY_MODEL,
        }

    except Exception as e:
        print("PRIMARY GEMINI ERROR:", repr(e))
        print("Primary model failed. Using fallback model...")

        try:
            response = client.models.generate_content(
                model=FALLBACK_MODEL,
                contents=prompt,
            )

            return {
                "answer": response.text,
                "model": FALLBACK_MODEL,
            }

        except Exception as e:
            print("FALLBACK GEMINI ERROR:", repr(e))
            return {
                "answer": "Sorry, the AI service is currently unavailable.",
                "model": None,
            }
