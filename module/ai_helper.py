from openai import OpenAI
import streamlit as st


def get_client():
    return OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )


def explain_code(code, language):

    client = get_client()

    prompt = f"""
You are CodeMate, a friendly programming tutor.

Explain the following {language} code to a beginner.

Code:
{code}

Give:
1. What the code does
2. Step-by-step explanation
3. Important programming concepts used
4. Time complexity
5. Space complexity

Keep the explanation clear and easy to understand.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text
