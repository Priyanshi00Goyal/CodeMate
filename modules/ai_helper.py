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

def find_bug(code, language, error_message):

    client = get_client()

    prompt = f"""
You are CodeMate, a friendly programming debugging tutor.

Analyze the following {language} code and identify potential bugs.

Code:
{code}

Error message:
{error_message if error_message else "No error message provided."}

Give the response in this structure:

1. 🐛 Problem
Explain what is wrong.

2. 🔍 Why it happens
Explain the cause in beginner-friendly language.

3. 🔧 How to fix it
Give a clear solution.

4. ✅ Corrected Code
Provide the corrected version of the code.

5. 💡 Prevention Tip
Give one short tip to avoid this type of bug in the future.

Do not invent an error if the code appears correct.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text

def improve_code(code, language):

    client = get_client()

    prompt = f"""
You are CodeMate, a professional programming mentor.

Improve the following {language} code while preserving its original
functionality.

Code:
{code}

Your response must contain:

1. ✨ Improved Code
Provide the complete improved code in a code block.

2. 🔍 What Was Improved
Explain the important changes.

3. 🚀 Why It Is Better
Explain improvements related to readability, structure,
maintainability, or efficiency.

4. 💡 Tip
Give one useful programming tip related to this code.

Do not change the intended behavior of the program.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text
    
