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

def generate_question(topic, difficulty):

    client = get_client()

    prompt = f"""
You are CodeMate, a coding practice mentor.

Generate ONE programming question.

Topic: {topic}
Difficulty: {difficulty}

Return the response in this exact structure:

QUESTION:
<the coding question>

EXAMPLE INPUT:
<example input>

EXAMPLE OUTPUT:
<example output>

HINT:
<a useful but not complete hint>

Do not provide the solution.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text

def evaluate_answer(question, answer, topic):

    client = get_client()

    prompt = f"""
You are CodeMate, a friendly coding mentor.

Evaluate a student's answer to this programming question.

Topic:
{topic}

Question:
{question}

Student Answer:
{answer}

Give:

1. SCORE: Give a score from 0 to 10.
2. RESULT: Correct, Partially Correct, or Incorrect.
3. WHAT WAS GOOD: Mention what the student did well.
4. WHAT TO IMPROVE: Explain mistakes clearly.
5. BETTER APPROACH: Explain a better approach if needed.
6. LEARNING TIP: Give one useful tip.

Be encouraging and educational.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text
