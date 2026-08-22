import streamlit as st
import re
from modules.ai_helper import (
    explain_code,
    find_bug,
    improve_code,
    generate_question,
    evaluate_answer
)

from modules.progress_tracker import (
    load_progress,
    save_progress
)

st.set_page_config(
    page_title="CodeMate",
    page_icon="💻",
    layout="wide"
)

st.markdown("""
<style>

.main-title {
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 0;
}

.subtitle {
    font-size: 20px;
    opacity: 0.75;
    margin-top: 0;
}

.feature-card {
    padding: 25px;
    border-radius: 15px;
    border: 1px solid rgba(128, 128, 128, 0.25);
    margin-bottom: 15px;
}

.feature-card h3 {
    margin-bottom: 8px;
}

.section-title {
    font-size: 30px;
    font-weight: 650;
}

</style>
""", unsafe_allow_html=True)

def extract_score(feedback):

    match = re.search(
        r"SCORE:\s*(\d+)",
        feedback,
        re.IGNORECASE
    )

    if match:

        return int(match.group(1))

    return 0

# Sidebar
st.sidebar.markdown(
    "# 💻 CodeMate"
)

st.sidebar.caption(
    "Your AI Coding Companion"
)

st.sidebar.divider()

st.sidebar.markdown("### 🧭 Navigation")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🧠 Code Explainer",
        "🐛 Bug Finder",
        "✨ Code Improver",
        "📚 Practice Mode",
        "📊 My Progress"
    ]
)

# HOME
if page == "🏠 Home":

    st.markdown(
        '<p class="main-title">💻 CodeMate</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Your AI-powered coding companion</p>',
        unsafe_allow_html=True
    )

    st.write(
        "Understand code, find bugs, improve your solutions, "
        "and practice programming concepts."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="feature-card">
            <h3>🧠 Code Explainer</h3>
            <p>
            Understand unfamiliar code with
            beginner-friendly explanations.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="feature-card">
            <h3>🐛 Bug Finder</h3>
            <p>
            Find programming problems and
            understand how to fix them.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="feature-card">
            <h3>✨ Code Improver</h3>
            <p>
            Make your code cleaner,
            clearer and easier to maintain.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        '<p class="section-title">🚀 What can CodeMate do?</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        ### 🧑‍💻 Learn

        - Understand difficult code
        - Learn programming concepts
        - Practice DSA problems
        - Get beginner-friendly explanations
        """)

    with col2:

        st.markdown("""
        ### ⚡ Improve

        - Find bugs
        - Improve code quality
        - Get AI feedback
        - Track your coding progress
        """)

    st.divider()

    st.success("🚀 CodeMate is ready to help you code!")

# CODE EXPLAINER
elif page == "🧠 Code Explainer":

    st.title("🧠 Code Explainer")

    language = st.selectbox(
        "Select programming language",
        ["Python", "C++", "C", "Java", "JavaScript"]
    )

    code = st.text_area(
        "Paste your code here",
        height=300,
        placeholder="Paste your code..."
    )

    if st.button("🔍 Explain Code"):

        if code.strip():

            with st.spinner("🧠 CodeMate is analyzing your code..."):

                try:
                    explanation = explain_code(
                        code,
                        language
                    )

                    st.markdown("## 💡 Explanation")
                    st.write(explanation)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        else:
            st.warning("Please paste some code first.")

# BUG FINDER
elif page == "🐛 Bug Finder":

    st.title("🐛 Bug Finder")

    language = st.selectbox(
        "Select programming language",
        ["Python", "C++", "C", "Java", "JavaScript"],
        key="bug_language"
    )

    code = st.text_area(
        "Paste your code",
        height=250
    )

    error = st.text_area(
        "Paste the error message (optional)",
        height=150
    )

    if st.button("🔎 Find Bug"):

        if code.strip():

            with st.spinner("🐛 CodeMate is searching for bugs..."):
    
                try:
                    analysis = find_bug(
                        code,
                        language,
                        error
                    )

                    st.markdown("## 🧠 Bug Analysis")
                    st.write(analysis)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        else:
            st.warning("Please paste your code first.")

# CODE IMPROVER
elif page == "✨ Code Improver":

    st.title("✨ Code Improver")

    st.write(
        "Paste your code and CodeMate will suggest a cleaner "
        "and more maintainable version."
    )

    language = st.selectbox(
        "Select programming language",
        ["Python", "C++", "C", "Java", "JavaScript"],
        key="improve_language"
    )

    code = st.text_area(
        "Paste your code",
        height=300,
        placeholder="Paste your code here..."
    )

    if st.button("✨ Improve Code"):

        if code.strip():

            with st.spinner("✨ CodeMate is improving your code..."):

                try:

                    improved = improve_code(
                        code,
                        language
                    )

                    st.markdown("## 🚀 Improved Version")

                    st.markdown(improved)

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )

        else:

            st.warning(
                "Please paste some code first."
            )

# PRACTICE MODE
elif page == "📚 Practice Mode":

    st.title("📚 Practice Mode")

    st.write(
        "Practice coding problems and get AI-powered feedback."
    )

    topic = st.selectbox(
        "Choose a topic",
        [
            "Arrays",
            "Strings",
            "Linked Lists",
            "Stacks",
            "Queues",
            "Trees",
            "Graphs",
            "Dynamic Programming"
        ]
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("🎯 Generate Question"):

        with st.spinner("🧠 Creating your question..."):

            try:

                question = generate_question(
                    topic,
                    difficulty
                )

                st.session_state.practice_question = question
                st.session_state.practice_topic = topic

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )

    if "practice_question" in st.session_state:

        st.divider()

        st.markdown("## 📝 Your Challenge")

        st.markdown(
            st.session_state.practice_question
        )

        answer = st.text_area(
            "💻 Write your solution here",
            height=300,
            placeholder="Write your code..."
        )

        if st.button("🚀 Submit Answer"):

            if answer.strip():

                with st.spinner(
                    "🔍 CodeMate is evaluating your solution..."
                ):

                    try:

                        feedback = evaluate_answer(
                            st.session_state.practice_question,
                            answer,
                            st.session_state.practice_topic
                        )

                        score = extract_score(feedback)

                        if "CORRECT" in feedback.upper():

                            result = "Correct"

                        elif "PARTIALLY CORRECT" in feedback.upper():

                            result = "Partially Correct"

                        else:

                            result = "Incorrect"

                        save_progress(
                            st.session_state.practice_topic,
                            difficulty,
                            score,
                            result
                        )

                        st.markdown("## 📊 Your Feedback")

                        st.markdown(feedback)

                        st.success(
                            f"Your score has been saved: {score}/10"
                        )

                    except Exception as e:

                        st.error(
                            f"Something went wrong: {e}"
                        )

            else:

                st.warning(
                    "Please write your solution first."
                )

# PROGRESS
elif page == "📊 My Progress":

    st.title("📊 My Progress")

    df = load_progress()

    if df.empty:

        st.info(
            "You haven't completed any practice "
            "questions yet. Start practicing! 🚀"
        )

    else:

        total_problems = len(df)

        average_score = round(
            df["score"].mean(),
            1
        )

        best_score = df["score"].max()

        topics = df["topic"].nunique()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Problems Solved",
                total_problems
            )

        with col2:

            st.metric(
                "Average Score",
                f"{average_score}/10"
            )

        with col3:

            st.metric(
                "Best Score",
                f"{best_score}/10"
            )

        with col4:

            st.metric(
                "Topics Practiced",
                topics
            )

        st.divider()

        st.subheader("📈 Score History")

        chart_data = df[
            ["date", "score"]
        ].copy()

        chart_data = chart_data.set_index("date")

        st.line_chart(chart_data)

        st.subheader("📚 Topics Practiced")

        topic_counts = (
            df["topic"]
            .value_counts()
        )

        st.bar_chart(topic_counts)

        st.subheader("🎯 Difficulty Distribution")

        difficulty_counts = (
            df["difficulty"]
            .value_counts()
        )

        st.bar_chart(difficulty_counts)

        st.subheader("📝 Practice History")

        st.dataframe(
            df,
            use_container_width=True
        )
