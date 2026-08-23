from google import genai
import streamlit as st


def get_client():
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )


def ask_ai(prompt):
    client = get_client()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


def explain_code(code, language, level):
    client = get_client()

    prompt = f"""
You are CodeMate, an expert programming tutor.

Analyze the following {language} code.

User level: {level}

CODE:
{code}

Provide these sections:

## What This Code Does
Give a short overview.

## Step-by-Step Explanation
Explain the important parts of the code.

## Concepts Used
List the programming concepts used.

## Time Complexity
Explain the time complexity and why.

## Space Complexity
Explain the space complexity and why.

## Potential Issues
Mention bugs, edge cases, or questionable practices.
If there are none, say so.

## Learning Tip
Give one useful concept the student should learn next.

Adjust the explanation to the selected user level.
Do not change the code.
Do not invent problems that do not exist.
"""

    return ask_ai(prompt)


def find_bug(code, language, error_message):
    client = get_client()

    prompt = f"""
You are CodeMate, a programming debugging tutor.

Analyze this {language} code.

CODE:
{code}

ERROR MESSAGE:
{error_message if error_message else "No error message provided."}

Provide:

## Problem
Explain what is wrong.

## Why It Happens
Explain the cause.

## How To Fix It
Give a clear solution.

## Corrected Code
Provide corrected code if necessary.

## Prevention Tip
Give one useful debugging tip.

Do not invent an error if the code appears correct.
"""

    return ask_ai(prompt)


def improve_code(code, language):
    client = get_client()

    prompt = f"""
You are CodeMate, a professional programming mentor.

Improve the following {language} code while preserving
its original functionality.

CODE:
{code}

Provide:

## Improved Code
Provide the complete improved code.

## What Was Improved
Explain the important changes.

## Why It Is Better
Explain readability, structure, maintainability,
and efficiency improvements.

## Tip
Give one useful programming tip.

Do not change the intended behavior.
"""

    return ask_ai(prompt)

    return response.output_text


def generate_question(topic, difficulty):
    client = get_client()

    prompt = f"""
You are CodeMate, a coding practice mentor.

Generate ONE programming problem.

Topic:
{topic}

Difficulty:
{difficulty}

Return:

## Question
<problem statement>

## Example Input
<example input>

## Example Output
<example output>

## Hint
<useful hint>

Do not provide the solution.
"""

    return ask_ai(prompt)


def evaluate_answer(question, answer, topic):
    client = get_client()

    prompt = f"""
You are CodeMate, a friendly coding mentor.

Evaluate this student's answer.

TOPIC:
{topic}

QUESTION:
{question}

STUDENT ANSWER:
{answer}

Provide:

## SCORE
Give a score from 0 to 10.

## RESULT
Correct, Partially Correct, or Incorrect.

## WHAT WAS GOOD
Explain what was done well.

## WHAT TO IMPROVE
Explain mistakes.

## BETTER APPROACH
Explain a better approach if needed.

## LEARNING TIP
Give one useful programming tip.

Be encouraging and educational.
"""

    return ask_ai(prompt)


def analyze_code(code, language, level):
    client = get_client()

    prompt = f"""
You are CodeMate, an expert programming tutor and code reviewer.

Analyze this {language} code.

STUDENT LEVEL:
{level}

CODE:
{code}

Return these sections:

## Code Summary
Explain what the program does.

## Step-by-Step Logic
Explain the important operations.

## Bugs & Issues
Identify syntax, runtime, logical errors,
edge cases, or questionable practices.

If there are no issues, say:
"No major issues detected."

## Code Quality
Evaluate:
- Readability
- Naming
- Structure
- Maintainability

Give a Code Quality Score from 0 to 10.

## Efficiency
Explain:
- Time Complexity
- Space Complexity
- Possible optimizations

## Concepts Used
List the programming concepts demonstrated.

## Recommended Practice
Suggest two concepts the student should practice next.

## Mentor Tip
Give one practical programming tip.

Do not invent bugs.
Do not rewrite the code unless necessary.
Adapt the explanation to the student's level.
"""

    return ask_ai(prompt)

def review_code(code, language):

    client = get_client()

    prompt = f"""
You are a senior software engineer.

Review this {language} code.

CODE:
{code}

Return ONLY this format:

READABILITY: X/10
EFFICIENCY: X/10
STRUCTURE: X/10
NAMING: X/10
ERROR_HANDLING: X/10
BEST_PRACTICES: X/10

SUMMARY:
Short review.

IMPROVEMENTS:
Bullet points of improvements.

Use realistic scores.
"""
    
    return ask_ai(prompt)

def explain_error(code, language, error_message):

    client = get_client()

    prompt = f"""
You are CodeMate, an expert programming debugger.

A student received an error while working with
{language}.

CODE:
{code}

ERROR:
{error_message}

Explain the problem in beginner-friendly language.

Return exactly these sections:

## 🐛 What Went Wrong
Explain the error.

## 🔍 Why It Happened
Explain the underlying cause.

## 🔧 How To Fix It
Give clear steps.

## ✅ Corrected Code
Show the corrected code.

## 💡 Remember
Give one short tip to prevent this error.

Do not invent additional errors.
"""

    return ask_ai(prompt)
