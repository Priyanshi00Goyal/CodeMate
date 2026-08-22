import streamlit as st
import re
from modules.ai_helper import (
    explain_code,
    find_bug,
    improve_code,
    generate_question,
    evaluate_answer,
    analyze_code,
    review_code,
    explain_error
)

from modules.progress_tracker import (
    load_progress,
    save_progress,
    get_learning_insights
)

from modules.code_analyzer import check_python_syntax

st.set_page_config(
    page_title="CodeMate",
    page_icon="💻",
    layout="wide"
)

st.markdown("""
<style>
/* ---------- Global ---------- */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,.18);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

.main-title {
    font-size: clamp(42px, 5vw, 64px);
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1;
    margin: 0;
}

.subtitle {
    font-size: 21px;
    opacity: .72;
    margin: 10px 0 18px;
}

.hero {
    padding: 34px 36px;
    border-radius: 24px;
    border: 1px solid rgba(128,128,128,.20);
    background: linear-gradient(
        135deg,
        rgba(99,102,241,.12),
        rgba(59,130,246,.06)
    );
    margin-bottom: 28px;
}

.hero-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    border: 1px solid rgba(99,102,241,.25);
    background: rgba(99,102,241,.10);
    margin-bottom: 14px;
}

.feature-card {
    min-height: 165px;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid rgba(128,128,128,.20);
    background: rgba(128,128,128,.035);
    margin-bottom: 16px;
    transition: transform .2s ease, border-color .2s ease;
}

.feature-card:hover {
    transform: translateY(-3px);
    border-color: rgba(99,102,241,.45);
}

.feature-card h3 {
    margin: 0 0 9px;
    font-size: 20px;
}

.feature-card p {
    opacity: .72;
    line-height: 1.55;
}

.section-title {
    font-size: 30px;
    font-weight: 750;
    margin-top: 10px;
}

.page-header {
    padding: 10px 0 8px;
    margin-bottom: 20px;
}

.page-header h1 {
    margin-bottom: 4px;
}

.page-description {
    opacity: .70;
    font-size: 16px;
}

.tip-card {
    padding: 18px 20px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,.18);
    background: rgba(128,128,128,.035);
}

.footer {
    text-align: center;
    opacity: .55;
    padding: 35px 0 5px;
    font-size: 13px;
}

div.stButton > button {
    border-radius: 10px;
    font-weight: 650;
}

textarea {
    border-radius: 12px !important;
}

[data-testid="stMetric"] {
    padding: 12px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,.16);
    background: rgba(128,128,128,.025);
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

def extract_metric(text, metric):

    pattern = rf"{metric}:\s*(\d+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return 0

# Sidebar
st.sidebar.markdown(
    """
    <div style="padding: 8px 0 18px;">
        <div style="font-size:30px;font-weight:800;">💻 CodeMate</div>
        <div style="opacity:.65;font-size:14px;margin-top:4px;">
            Your AI Coding Companion
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

st.sidebar.caption("LEARNING TOOLS")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🔍 Analyze Code",
        "🧪 Python Checker",
        "🧠 Code Explainer",
        "🐛 Bug Finder",
        "✨ Code Improver",
        "⭐ Code Review",
        "📚 Practice Mode",
        "📊 My Progress"
    ]
)

# HOME
if page == "🏠 Home":

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">⚡ AI-POWERED LEARNING PLATFORM</div>
        <div class="main-title">💻 CodeMate</div>
        <div class="subtitle">Your personal AI programming mentor.</div>
        <p style="font-size:17px;line-height:1.7;max-width:760px;opacity:.78;">
            Understand code. Find bugs. Improve your solutions.
            Practice smarter and track your progress — all in one place.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick stats / value strip
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric("🤖 AI Tools", "8")
    with s2:
        st.metric("💻 Languages", "5+")
    with s3:
        st.metric("📚 Learning", "24/7")
    with s4:
        st.metric("🎯 Practice", "AI Feedback")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<p class="section-title">Everything you need to become a better coder</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="page-description">Choose a tool from the sidebar and let CodeMate help you learn by doing.</p>',
        unsafe_allow_html=True
    )

    # Feature grid
    features = [
        ("🧠", "Understand Code", "Break down unfamiliar code into simple, level-based explanations.", "Code Explainer"),
        ("🐛", "Find Bugs", "Identify problems, understand why they happen, and learn how to fix them.", "Bug Finder"),
        ("✨", "Improve Code", "Make your solutions cleaner, more readable, maintainable, and efficient.", "Code Improver"),
        ("🔍", "Analyze Code", "Get a complete review of logic, complexity, quality, issues, and concepts.", "Analyze Code"),
        ("⭐", "Review Code", "Get structured scores for readability, efficiency, naming, and best practices.", "Code Review"),
        ("📚", "Practice", "Generate coding challenges and receive personalized feedback on your answer.", "Practice Mode"),
    ]

    for row in range(0, len(features), 3):
        cols = st.columns(3, gap="medium")
        for col, feature in zip(cols, features[row:row+3]):
            icon, title, desc, label = feature
            with col:
                st.markdown(f"""
                <div class="feature-card">
                    <div style="font-size:32px;margin-bottom:10px;">{icon}</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                    <div style="font-size:12px;font-weight:700;opacity:.55;margin-top:14px;">
                        CODEMATE • {label.upper()}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # How it works
    st.markdown(
        '<p class="section-title">🚀 How CodeMate works</p>',
        unsafe_allow_html=True
    )

    h1, h2, h3 = st.columns(3)

    with h1:
        st.markdown("""
        <div class="tip-card">
            <div style="font-size:28px;">01</div>
            <h3>Paste your code</h3>
            <p style="opacity:.7;">Share your code, error, or coding answer with CodeMate.</p>
        </div>
        """, unsafe_allow_html=True)

    with h2:
        st.markdown("""
        <div class="tip-card">
            <div style="font-size:28px;">02</div>
            <h3>Choose your goal</h3>
            <p style="opacity:.7;">Explain, debug, improve, review, analyze, or practice.</p>
        </div>
        """, unsafe_allow_html=True)

    with h3:
        st.markdown("""
        <div class="tip-card">
            <div style="font-size:28px;">03</div>
            <h3>Learn & improve</h3>
            <p style="opacity:.7;">Use the AI feedback to understand the concept and keep practicing.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main CTA
    st.markdown("""
    <div class="hero" style="text-align:center;padding:28px;">
        <div style="font-size:30px;">🎯 Ready to code smarter?</div>
        <p style="opacity:.72;margin-bottom:0;">
            Start with <b>Code Explainer</b> if you're learning,
            or <b>Analyze Code</b> if you want a complete review.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="footer">💻 CodeMate • Learn. Debug. Improve. Practice.</div>',
        unsafe_allow_html=True
    )

# PYTHON CHECKER
elif page == "🧪 Python Checker":

    st.markdown("""<div class="page-header"><h1>🧪 Python Code Checker</h1><div class="page-description">Check your Python code for syntax errors before running it.</div></div>""", unsafe_allow_html=True)

    st.write(
        "Check your Python code for syntax errors "
        "before running it."
    )

    code = st.text_area(
        "💻 Paste Python code",
        height=350,
        placeholder="""Example:

numbers = [1, 2, 3]

for number in numbers:
    print(number)
"""
    )

    if st.button(
        "🔎 Check Code",
        type="primary"
    ):

        if not code.strip():

            st.warning(
                "Please enter some Python code."
            )

        else:

            # Clear previous result
            st.session_state.pop(
                "syntax_result",
                None
            )

            st.session_state.pop(
                "error_explanation",
                None
            )

            result = check_python_syntax(code)

            st.session_state.syntax_result = result
            st.session_state.checked_code = code

    # Display stored result
    if "syntax_result" in st.session_state:

        result = st.session_state.syntax_result

        st.divider()

        if result["valid"]:

            st.success(
                "✅ No syntax errors detected!"
            )

            st.markdown(
                "Your code passed the Python syntax check."
            )

        else:

            st.error(
                "❌ Syntax error detected!"
            )

            st.markdown(
                f"**Error:** {result['message']}"
            )

            if result["line"]:

                st.markdown(
                    f"**Line:** {result['line']}"
                )

            if result["offset"]:

                st.markdown(
                    f"**Position:** {result['offset']}"
                )

            st.info(
                "CodeMate found a syntax problem. "
                "Let's understand it."
            )

            if st.button(
                "🤖 Explain This Error",
                type="primary"
            ):

                error_message = (
                    f"{result['message']} "
                    f"(Line {result['line']})"
                )

                with st.spinner(
                    "🧠 CodeMate is explaining the error..."
                ):

                    try:

                        explanation = explain_error(
                            st.session_state.checked_code,
                            "Python",
                            error_message
                        )

                        st.session_state.error_explanation = (
                            explanation
                        )

                    except Exception as e:

                        st.error(
                            f"Could not explain the error: {e}"
                        )

        # Display AI explanation
        if "error_explanation" in st.session_state:

            st.divider()

            st.markdown(
                "## 🤖 CodeMate's Explanation"
            )

            st.markdown(
                st.session_state.error_explanation
            )

#CODE ANALYZER
elif page == "🔍 Analyze Code":

    st.markdown("""<div class="page-header"><h1>🔍 Analyze Code</h1><div class="page-description">Get a complete AI-powered analysis of your code.</div></div>""", unsafe_allow_html=True)

    st.write(
        "Get a complete AI-powered analysis of your code."
    )

    col1, col2 = st.columns(2)

    with col1:

        language = st.selectbox(
            "💻 Programming Language",
            [
                "Python",
                "C++",
                "C",
                "Java",
                "JavaScript"
            ],
            key="analyze_language"
        )

    with col2:

        level = st.selectbox(
            "🎓 Your Level",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ],
            key="analyze_level"
        )

    code = st.text_area(
        "💻 Paste your code",
        height=350,
        placeholder="Paste your code here..."
    )

    if st.button(
        "🔍 Analyze Code",
        type="primary"
    ):

        if code.strip():

            with st.spinner(
                "🧠 CodeMate is analyzing your code..."
            ):

                    analysis = analyze_code(
                        code,
                        language,
                        level
                    )

                    st.divider()

                    st.markdown(
                        "## 📊 Code Analysis"
                    )

                    st.markdown(
                        analysis
                    )

                    st.divider()

                    st.markdown("## 🎯 Continue Learning")

                    st.write(
                        "Want to practice what you just learned?"
                    )

                    practice_topic = st.selectbox(
                        "Choose a topic to practice",
                        [
                            "Arrays",
                            "Strings",
                            "Loops",
                            "Functions",
                            "Recursion",
                            "Linked Lists",
                            "Stacks",
                            "Queues",
                            "Trees",
                            "Graphs",
                            "Dynamic Programming",
                            "Binary Search"
                        ],
                        key="analysis_practice_topic"
                    )


                    practice_difficulty = st.selectbox(
                        "Choose difficulty",
                        ["Easy", "Medium", "Hard"],
                        key="analysis_practice_difficulty"
                    )

                    if st.button("🎯 Practice This Topic"):

                        with st.spinner(
                            "🧠 Creating a personalized question..."
                        ):

                            try:

                                question = generate_question(
                                    practice_topic,
                                    practice_difficulty
                                )

                                st.session_state.practice_question = question
                                st.session_state.practice_topic = practice_topic

                                st.success(
                                    "Question generated! Go to 📚 Practice Mode to solve it."
                                )

                            except Exception as e:

                                st.error(
                                    f"Something went wrong: {e}"
                                )


        else:

            st.warning(
                "Please paste some code first."
            )

# CODE EXPLAINER
elif page == "🧠 Code Explainer":

    st.markdown("""<div class="page-header"><h1>🧠 Code Explainer</h1><div class="page-description">Understand unfamiliar code with a clear, level-adjusted explanation.</div></div>""", unsafe_allow_html=True)

    language = st.selectbox(
        "Select programming language",
        ["Python", "C++", "C", "Java", "JavaScript"],
        key="explain_language"
    )

    level = st.select_slider(
        "🎓 Explanation Level",
        options=[
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        value="Beginner"
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
                        language,
                        level
                    )

                    st.markdown("## 💡 Explanation")
                    st.write(explanation)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        else:
            st.warning("Please paste some code first.")

# BUG FINDER
elif page == "🐛 Bug Finder":

    st.markdown("""<div class="page-header"><h1>🐛 Bug Finder</h1><div class="page-description">Find bugs, understand their causes, and learn how to fix them.</div></div>""", unsafe_allow_html=True)

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

    st.markdown("""<div class="page-header"><h1>✨ Code Improver</h1><div class="page-description">Make your code cleaner, clearer, and easier to maintain.</div></div>""", unsafe_allow_html=True)

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

    st.markdown("""<div class="page-header"><h1>📚 Practice Mode</h1><div class="page-description">Practice coding problems and get personalized AI feedback.</div></div>""", unsafe_allow_html=True)

    st.write(
        "Practice coding problems and get personalized AI feedback."
    )

    if "practice_topic" in st.session_state:

        st.info(
            f"🎯 Current topic: "
            f"**{st.session_state.practice_topic}**"
        )

    col1, col2 = st.columns(2)

    with col1:

        topic = st.selectbox(
            "📚 Topic",
            [
                "Arrays",
                "Strings",
                "Loops",
                "Functions",
                "Recursion",
                "Linked Lists",
                "Stacks",
                "Queues",
                "Trees",
                "Graphs",
                "Dynamic Programming",
                "Binary Search"
            ],
            key="practice_topic_select"
        )

    with col2:

        difficulty = st.selectbox(
            "🎯 Difficulty",
            ["Easy", "Medium", "Hard"],
            key="practice_difficulty"
        )

    if st.button(
        "🎯 Generate Question",
        type="primary"
    ):

        with st.spinner(
            "🧠 Creating your coding challenge..."
        ):

            try:

                question = generate_question(
                    topic,
                    difficulty
                )

                st.session_state.practice_question = question
                st.session_state.practice_topic = topic
                st.session_state.practice_difficulty = difficulty

                st.success(
                    "Your challenge is ready! 🚀"
                )

            except Exception as e:

                st.error(
                    f"Could not generate question: {e}"
                )

    if "practice_question" in st.session_state:

        st.divider()

        st.markdown("## 📝 Your Challenge")

        st.markdown(
            st.session_state.practice_question
        )

        answer = st.text_area(
            "💻 Your Solution",
            height=300,
            placeholder="Write your solution here..."
        )

        if st.button(
            "🚀 Submit Solution",
            type="primary"
        ):

            if not answer.strip():

                st.warning(
                    "Please write a solution first."
                )

            else:

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

                        if "PARTIALLY CORRECT" in feedback.upper():

                            result = "Partially Correct"

                        elif "CORRECT" in feedback.upper():

                            result = "Correct"

                        else:

                            result = "Incorrect"

                        save_progress(
                            st.session_state.practice_topic,
                            st.session_state.practice_difficulty,
                            score,
                            result
                        )

                        st.divider()

                        st.markdown(
                            "## 📊 CodeMate Feedback"
                        )

                        st.markdown(feedback)

                        st.metric(
                            "Your Score",
                            f"{score}/10"
                        )

                        st.success(
                            "✅ Your progress has been saved!"
                        )

                    except Exception as e:

                        st.error(
                            f"Evaluation failed: {e}"
                        )

# PROGRESS
elif page == "📊 My Progress":

    st.markdown("""<div class="page-header"><h1>📊 My Progress</h1><div class="page-description">Track your practice, scores, strengths, and next steps.</div></div>""", unsafe_allow_html=True)

    df = load_progress()

    if df.empty:

        st.info(
            "You haven't completed any practice "
            "questions yet. Start practicing! 🚀"
        )

    else:

        insights = get_learning_insights()

        total_problems = len(df)

        average_score = round(
            df["score"].mean(),
            1
        )

        best_score = df["score"].max()

        topics = df["topic"].nunique()

        # Metrics

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

        # Learning Insights

        st.markdown(
            "## 🧠 Learning Insights"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                f"""
                🏆 **Strongest Topic**

                {insights["strongest_topic"]}

                Average Score:
                **{insights["strongest_score"]}/10**
                """
            )

        with col2:

            st.warning(
                f"""
                ⚠️ **Needs More Practice**

                {insights["weakest_topic"]}

                Average Score:
                **{insights["weakest_score"]}/10**
                """
            )

        st.divider()

        # Recommendation

        st.markdown(
            "## 🎯 Recommended Next Step"
        )

        if insights["weakest_score"] < 6:

            st.info(
                f"""
                CodeMate recommends focusing on
                **{insights["weakest_topic"]}**.

                Try 3 Easy problems on this topic
                before moving to a harder difficulty.
                """
            )

        elif insights["weakest_score"] < 8:

            st.info(
                f"""
                You're making progress!

                Practice more **{insights["weakest_topic"]}**
                to strengthen your understanding.
                """
            )

        else:

            st.success(
                "🎉 You're performing consistently well!"

                " Try a new topic or increase the difficulty."
            )

        st.divider()

        # Score history

        st.markdown(
            "## 📈 Score History"
        )

        chart_data = df[
            ["date", "score"]
        ].copy()

        chart_data = chart_data.set_index(
            "date"
        )

        st.line_chart(chart_data)

        # Topic performance

        st.markdown(
            "## 📚 Topic Performance"
        )

        topic_performance = (
            df.groupby("topic")["score"]
            .mean()
            .round(2)
            .sort_values(ascending=False)
        )

        st.bar_chart(
            topic_performance
        )

        # Difficulty

        st.markdown(
            "## 🎯 Difficulty Distribution"
        )

        difficulty_counts = (
            df["difficulty"]
            .value_counts()
        )

        st.bar_chart(
            difficulty_counts
        )

        # History

        st.markdown(
            "## 📝 Practice History"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

# CODE REVIEW
elif page == "⭐ Code Review":

    st.markdown("""<div class="page-header"><h1>⭐ Code Review</h1><div class="page-description">Get a structured review of readability, efficiency, naming, and best practices.</div></div>""", unsafe_allow_html=True)

    language = st.selectbox(
        "Language",
        [
            "Python",
            "C++",
            "C",
            "Java",
            "JavaScript"
        ],
        key="review_language"
    )

    code = st.text_area(
        "Paste your code",
        height=350
    )

    if st.button(
        "⭐ Review Code",
        type="primary"
    ):

        if code.strip():

            with st.spinner(
                "Reviewing code..."
            ):

                try:

                    review = review_code(
                        code,
                        language
                    )

                    readability = extract_metric(
                        review,
                        "READABILITY"
                    )

                    efficiency = extract_metric(
                        review,
                        "EFFICIENCY"
                    )

                    structure = extract_metric(
                        review,
                        "STRUCTURE"
                    )

                    naming = extract_metric(
                        review,
                        "NAMING"
                    )

                    error_handling = extract_metric(
                        review,
                        "ERROR_HANDLING"
                    )

                    best_practices = extract_metric(
                        review,
                        "BEST_PRACTICES"
                    )

                    overall = round(
                        (
                            readability +
                            efficiency +
                            structure +
                            naming +
                            error_handling +
                            best_practices
                        ) / 6,
                        1
                    )

                    st.metric(
                        "Overall Score",
                        f"{overall}/10"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Readability",
                            readability
                        )

                        st.metric(
                            "Structure",
                            structure
                        )

                    with col2:
                        st.metric(
                            "Efficiency",
                            efficiency
                        )

                        st.metric(
                            "Naming",
                            naming
                        )

                    with col3:
                        st.metric(
                            "Error Handling",
                            error_handling
                        )

                        st.metric(
                            "Best Practices",
                            best_practices
                        )

                    st.divider()

                    st.markdown(review)

                except Exception as e:

                    st.error(
                        f"Review failed: {e}"
                    )

        else:

            st.warning(
                "Please paste some code."
            )
