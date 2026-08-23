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

# =========================================================
# NOTE: st.markdown() treats any line indented 4+ spaces as
# a markdown code block, which is why the HTML was showing
# up as raw text in the UI. Every HTML string below is kept
# flush-left (no leading indentation) to avoid that.
# =========================================================

st.markdown("""
<style>

/* =========================================================
   CODEMATE — GLOBAL UI
   ========================================================= */

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
    max-width: 1380px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,.16);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

[data-testid="stSidebar"] div.stButton > button {
    min-height: 42px;
    border-radius: 11px;
    border: 1px solid rgba(128,128,128,.12);
    background: rgba(128,128,128,.035);
    font-size: 13px;
    font-weight: 600;
    text-align: left;
    transition: all .18s ease;
}

[data-testid="stSidebar"] div.stButton > button:hover {
    border-color: rgba(99,102,241,.40);
    background: rgba(99,102,241,.09);
    transform: translateX(2px);
}

[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: rgba(99,102,241,.15);
    border-color: rgba(99,102,241,.35);
}

/* Sidebar brand */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 4px 2px 11px;
}

.sidebar-logo {
    width: 43px;
    height: 43px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    font-size: 22px;
    background: linear-gradient(
        135deg,
        rgba(99,102,241,.22),
        rgba(59,130,246,.16)
    );
    border: 1px solid rgba(99,102,241,.22);
}

.sidebar-title {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -.5px;
}

.sidebar-subtitle {
    font-size: 11px;
    opacity: .55;
    margin-top: 2px;
}

.sidebar-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 5px 10px;
    margin: 2px 0 5px 1px;
    border-radius: 999px;
    font-size: 11px;
    border: 1px solid rgba(34,197,94,.22);
    background: rgba(34,197,94,.07);
    opacity: .85;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #22c55e;
    display: inline-block;
}

.nav-label {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.2px;
    opacity: .43;
    margin: 14px 0 7px;
}

.sidebar-footer {
    padding: 7px 4px 2px;
    font-size: 13px;
}


/* =========================================================
   HOME — HERO
   ========================================================= */

.home-hero {
    position: relative;
    overflow: hidden;
    padding: 34px 38px;
    border-radius: 24px;
    border: 1px solid rgba(99,102,241,.20);
    background:
        radial-gradient(
            circle at 85% 20%,
            rgba(99,102,241,.18),
            transparent 34%
        ),
        linear-gradient(
            135deg,
            rgba(99,102,241,.12),
            rgba(59,130,246,.055)
        );
    margin-bottom: 22px;
}

.home-hero::after {
    content: "";
    position: absolute;
    width: 190px;
    height: 190px;
    right: -70px;
    bottom: -90px;
    border-radius: 50%;
    border: 1px solid rgba(99,102,241,.15);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .4px;
    border: 1px solid rgba(99,102,241,.25);
    background: rgba(99,102,241,.10);
    margin-bottom: 13px;
}

.main-title {
    font-size: clamp(38px, 4vw, 54px);
    font-weight: 850;
    letter-spacing: -2px;
    line-height: 1;
    margin: 0;
}

.hero-subtitle {
    font-size: 20px;
    font-weight: 600;
    margin-top: 10px;
    opacity: .78;
}

.hero-description {
    max-width: 700px;
    font-size: 15px;
    line-height: 1.65;
    opacity: .65;
    margin-top: 10px;
}


/* =========================================================
   HOME — STATS
   ========================================================= */

.home-stat {
    padding: 15px 17px;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,.15);
    background: rgba(128,128,128,.025);
    text-align: center;
}

.home-stat-icon {
    font-size: 20px;
    margin-bottom: 3px;
}

.home-stat-value {
    font-size: 20px;
    font-weight: 800;
}

.home-stat-label {
    font-size: 11px;
    opacity: .55;
    margin-top: 2px;
}


/* =========================================================
   HOME — SECTION HEADERS
   ========================================================= */

.home-section {
    margin-top: 27px;
    margin-bottom: 13px;
}

.home-section-title {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -.6px;
    margin: 0;
}

.home-section-description {
    font-size: 13px;
    opacity: .58;
    margin-top: 4px;
}


/* =========================================================
   HOME — PRIMARY TOOL CARDS
   ========================================================= */

.tool-card {
    min-height: 145px;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(128,128,128,.17);
    background: rgba(128,128,128,.025);
    transition:
        transform .18s ease,
        border-color .18s ease,
        background .18s ease;
}

.tool-card:hover {
    transform: translateY(-3px);
    border-color: rgba(99,102,241,.42);
    background: rgba(99,102,241,.045);
}

.tool-icon {
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    font-size: 22px;
    margin-bottom: 12px;
    background: rgba(99,102,241,.10);
    border: 1px solid rgba(99,102,241,.15);
}

.tool-title {
    font-size: 17px;
    font-weight: 750;
    margin-bottom: 5px;
}

.tool-description {
    font-size: 12px;
    line-height: 1.5;
    opacity: .60;
}


/* =========================================================
   HOME — SECONDARY TOOLS
   ========================================================= */

.mini-tool {
    min-height: 112px;
    padding: 17px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,.15);
    background: rgba(128,128,128,.025);
    transition: all .18s ease;
}

.mini-tool:hover {
    transform: translateY(-2px);
    border-color: rgba(99,102,241,.35);
}

.mini-tool-icon {
    font-size: 24px;
    margin-bottom: 8px;
}

.mini-tool-title {
    font-size: 15px;
    font-weight: 700;
}

.mini-tool-description {
    font-size: 11px;
    opacity: .58;
    line-height: 1.45;
    margin-top: 3px;
}


/* =========================================================
   HOME — GETTING STARTED
   ========================================================= */

.step-card {
    min-height: 125px;
    padding: 19px;
    border-radius: 17px;
    border: 1px solid rgba(128,128,128,.15);
    background: rgba(128,128,128,.025);
}

.step-number {
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 1.2px;
    opacity: .42;
}

.step-title {
    font-size: 16px;
    font-weight: 750;
    margin-top: 7px;
}

.step-description {
    font-size: 12px;
    line-height: 1.5;
    opacity: .58;
    margin-top: 4px;
}


/* =========================================================
   HOME — CTA
   ========================================================= */

.home-cta {
    margin-top: 27px;
    padding: 25px 30px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(99,102,241,.18);
    background: linear-gradient(
        135deg,
        rgba(99,102,241,.10),
        rgba(59,130,246,.045)
    );
}

.cta-title {
    font-size: 22px;
    font-weight: 800;
}

.cta-description {
    font-size: 13px;
    opacity: .60;
    margin-top: 5px;
}


/* =========================================================
   GENERAL APP
   ========================================================= */

.page-header {
    padding: 5px 0 10px;
    margin-bottom: 17px;
}

.page-header h1 {
    margin-bottom: 3px;
}

.page-description {
    opacity: .68;
    font-size: 15px;
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
    border: 1px solid rgba(128,128,128,.15);
    background: rgba(128,128,128,.025);
}

.footer {
    text-align: center;
    opacity: .42;
    padding: 28px 0 4px;
    font-size: 12px;
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
st.sidebar.markdown("""
<div class="sidebar-brand">
<div class="sidebar-logo">💻</div>
<div>
<div class="sidebar-title">CodeMate</div>
<div class="sidebar-subtitle">AI Programming Mentor</div>
</div>
</div>
<div class="sidebar-status">
<span class="status-dot"></span>
Gemini AI • Online
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown('<div class="nav-label">HOME</div>', unsafe_allow_html=True)
home_page = st.sidebar.button(
    "🏠  Home",
    use_container_width=True,
    type="secondary"
)

st.sidebar.markdown('<div class="nav-label">LEARN</div>', unsafe_allow_html=True)

learn_col1, learn_col2 = st.sidebar.columns(2)
with learn_col1:
    explain_btn = st.button("🧠\nExplain", use_container_width=True)
with learn_col2:
    analyze_btn = st.button("🔍\nAnalyze", use_container_width=True)

st.sidebar.markdown('<div class="nav-label">DEBUG</div>', unsafe_allow_html=True)

debug_col1, debug_col2 = st.sidebar.columns(2)
with debug_col1:
    bug_btn = st.button("🐛\nFind Bug", use_container_width=True)
with debug_col2:
    checker_btn = st.button("🧪\nPython", use_container_width=True)

error_btn = st.sidebar.button(
    "🔧  Explain Error",
    use_container_width=True
)

st.sidebar.markdown('<div class="nav-label">IMPROVE</div>', unsafe_allow_html=True)

improve_btn = st.sidebar.button(
    "✨  Improve Code",
    use_container_width=True
)

review_btn = st.sidebar.button(
    "⭐  Code Review",
    use_container_width=True
)

st.sidebar.markdown('<div class="nav-label">PRACTICE</div>', unsafe_allow_html=True)

practice_btn = st.sidebar.button(
    "📚  Practice Mode",
    use_container_width=True
)

progress_btn = st.sidebar.button(
    "📊  My Progress",
    use_container_width=True
)

# Keep navigation state across Streamlit reruns.
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

button_routes = {
    "home_page": "🏠 Home",
    "explain_btn": "🧠 Code Explainer",
    "analyze_btn": "🔍 Analyze Code",
    "bug_btn": "🐛 Bug Finder",
    "checker_btn": "🧪 Python Checker",
    "error_btn": "🔧 Explain Error",
    "improve_btn": "✨ Code Improver",
    "review_btn": "⭐ Code Review",
    "practice_btn": "📚 Practice Mode",
    "progress_btn": "📊 My Progress",
}

for button_name, route in button_routes.items():
    if locals().get(button_name):
        st.session_state.page = route

page = st.session_state.page

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div class="sidebar-footer">
<div style="font-weight:700;">⚡ CodeMate</div>
<div style="opacity:.58;font-size:12px;margin-top:4px;">
Learn • Debug • Improve • Practice
</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":

    # -----------------------------------------------------
    # HERO
    # -----------------------------------------------------

    st.markdown("""
<div class="home-hero">
<div class="hero-badge">
⚡ AI-POWERED PROGRAMMING MENTOR
</div>
<div class="main-title">
💻 CodeMate
</div>
<div class="hero-subtitle">
Your personal AI programming mentor.
</div>
<div class="hero-description">
Understand code, find bugs, improve your solutions,
practice programming, and track your learning journey —
all from one place.
</div>
</div>
""", unsafe_allow_html=True)

    # -----------------------------------------------------
    # QUICK STATS
    # -----------------------------------------------------

    s1, s2, s3, s4 = st.columns(4, gap="medium")

    with s1:
        st.markdown("""
<div class="home-stat">
<div class="home-stat-icon">🤖</div>
<div class="home-stat-value">8</div>
<div class="home-stat-label">AI Tools</div>
</div>
""", unsafe_allow_html=True)

    with s2:
        st.markdown("""
<div class="home-stat">
<div class="home-stat-icon">💻</div>
<div class="home-stat-value">5+</div>
<div class="home-stat-label">Languages</div>
</div>
""", unsafe_allow_html=True)

    with s3:
        st.markdown("""
<div class="home-stat">
<div class="home-stat-icon">📚</div>
<div class="home-stat-value">24/7</div>
<div class="home-stat-label">Learning</div>
</div>
""", unsafe_allow_html=True)

    with s4:
        st.markdown("""
<div class="home-stat">
<div class="home-stat-icon">⚡</div>
<div class="home-stat-value">Instant</div>
<div class="home-stat-label">AI Feedback</div>
</div>
""", unsafe_allow_html=True)

    # -----------------------------------------------------
    # PRIMARY TOOLS
    # -----------------------------------------------------

    st.markdown("""
<div class="home-section">
<div class="home-section-title">
🚀 Start coding smarter
</div>
<div class="home-section-description">
Choose what you want CodeMate to help you with.
</div>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        st.markdown("""
<div class="tool-card">
<div class="tool-icon">🧠</div>
<div class="tool-title">
Explain Code
</div>
<div class="tool-description">
Understand unfamiliar code with
simple, beginner-friendly explanations.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button(
            "Open Explainer →",
            key="home_explain",
            use_container_width=True
        ):
            st.session_state.page = "🧠 Code Explainer"
            st.rerun()

    with col2:
        st.markdown("""
<div class="tool-card">
<div class="tool-icon">🐛</div>
<div class="tool-title">
Find Bugs
</div>
<div class="tool-description">
Discover bugs, understand why they happen,
and learn how to fix them.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button(
            "Open Bug Finder →",
            key="home_bug",
            use_container_width=True
        ):
            st.session_state.page = "🐛 Bug Finder"
            st.rerun()

    with col3:
        st.markdown("""
<div class="tool-card">
<div class="tool-icon">✨</div>
<div class="tool-title">
Improve Code
</div>
<div class="tool-description">
Make your code cleaner, clearer,
more readable, and maintainable.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button(
            "Improve My Code →",
            key="home_improve",
            use_container_width=True
        ):
            st.session_state.page = "✨ Code Improver"
            st.rerun()

    with col4:
        st.markdown("""
<div class="tool-card">
<div class="tool-icon">🔍</div>
<div class="tool-title">
Analyze Code
</div>
<div class="tool-description">
Get a complete analysis of logic,
quality, complexity, and concepts.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button(
            "Analyze My Code →",
            key="home_analyze",
            use_container_width=True
        ):
            st.session_state.page = "🔍 Analyze Code"
            st.rerun()

    # -----------------------------------------------------
    # MORE TOOLS
    # -----------------------------------------------------

    st.markdown("""
<div class="home-section">
<div class="home-section-title">
🛠️ More CodeMate tools
</div>
<div class="home-section-description">
Additional tools for reviewing, practicing,
checking, and tracking your code.
</div>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5, gap="small")

    with col1:
        st.markdown("""
<div class="mini-tool">
<div class="mini-tool-icon">⭐</div>
<div class="mini-tool-title">
Code Review
</div>
<div class="mini-tool-description">
Get structured code quality feedback.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button("Open →", key="home_review", use_container_width=True):
            st.session_state.page = "⭐ Code Review"
            st.rerun()

    with col2:
        st.markdown("""
<div class="mini-tool">
<div class="mini-tool-icon">📚</div>
<div class="mini-tool-title">
Practice
</div>
<div class="mini-tool-description">
Generate coding challenges with AI.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button("Open →", key="home_practice", use_container_width=True):
            st.session_state.page = "📚 Practice Mode"
            st.rerun()

    with col3:
        st.markdown("""
<div class="mini-tool">
<div class="mini-tool-icon">🧪</div>
<div class="mini-tool-title">
Python Checker
</div>
<div class="mini-tool-description">
Detect Python syntax errors quickly.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button("Open →", key="home_python", use_container_width=True):
            st.session_state.page = "🧪 Python Checker"
            st.rerun()

    with col4:
        st.markdown("""
<div class="mini-tool">
<div class="mini-tool-icon">🔧</div>
<div class="mini-tool-title">
Explain Error
</div>
<div class="mini-tool-description">
Turn confusing errors into simple explanations.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button("Open →", key="home_error", use_container_width=True):
            st.session_state.page = "🔧 Explain Error"
            st.rerun()

    with col5:
        st.markdown("""
<div class="mini-tool">
<div class="mini-tool-icon">📊</div>
<div class="mini-tool-title">
My Progress
</div>
<div class="mini-tool-description">
Track scores, topics, and learning progress.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button("Open →", key="home_progress", use_container_width=True):
            st.session_state.page = "📊 My Progress"
            st.rerun()

    # -----------------------------------------------------
    # GETTING STARTED
    # -----------------------------------------------------

    st.markdown("""
<div class="home-section">
<div class="home-section-title">
💡 How to use CodeMate
</div>
<div class="home-section-description">
A simple workflow for learning and improving your programming.
</div>
</div>
""", unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3, gap="medium")

    with h1:
        st.markdown("""
<div class="step-card">
<div class="step-number">
STEP 01
</div>
<div class="step-title">
💻 Share your code
</div>
<div class="step-description">
Paste your code or programming error
into one of CodeMate's tools.
</div>
</div>
""", unsafe_allow_html=True)

    with h2:
        st.markdown("""
<div class="step-card">
<div class="step-number">
STEP 02
</div>
<div class="step-title">
🎯 Choose your goal
</div>
<div class="step-description">
Explain, debug, improve, review,
analyze, or practice.
</div>
</div>
""", unsafe_allow_html=True)

    with h3:
        st.markdown("""
<div class="step-card">
<div class="step-number">
STEP 03
</div>
<div class="step-title">
🧠 Learn from feedback
</div>
<div class="step-description">
Understand the reasoning behind the
solution and improve your skills.
</div>
</div>
""", unsafe_allow_html=True)

    # -----------------------------------------------------
    # CTA
    # -----------------------------------------------------

    st.markdown("""
<div class="home-cta">
<div class="cta-title">
🎯 Ready to code smarter?
</div>
<div class="cta-description">
Start with Code Explainer if you're learning,
or Analyze Code for a complete overview.
</div>
</div>
""", unsafe_allow_html=True)

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    st.markdown("""
<div class="footer">
💻 CodeMate &nbsp;•&nbsp;
Learn &nbsp;•&nbsp;
Debug &nbsp;•&nbsp;
Improve &nbsp;•&nbsp;
Practice
</div>
""", unsafe_allow_html=True)

# CODE ANALYZER
elif page == "🔍 Analyze Code":

    st.markdown("""<div class="page-header"><h1>🔍 Analyze Code</h1><div class="page-description">Get a complete AI-powered analysis of your code.</div></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        language = st.selectbox(
            "💻 Programming Language",
            ["Python", "C++", "C", "Java", "JavaScript"],
            key="analyze_language"
        )

    with col2:
        level = st.selectbox(
            "🎓 Your Level",
            ["Beginner", "Intermediate", "Advanced"],
            key="analyze_level"
        )

    code = st.text_area(
        "💻 Paste your code",
        height=350,
        placeholder="Paste your code here..."
    )

    if st.button("🔍 Analyze Code", type="primary"):

        if code.strip():

            with st.spinner("🧠 CodeMate is analyzing your code..."):

                try:
                    analysis = analyze_code(code, language, level)

                    st.session_state.last_analysis = analysis

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
                    st.session_state.last_analysis = None

        else:
            st.warning("Please paste some code first.")

    if st.session_state.get("last_analysis"):

        st.divider()
        st.markdown("## 📊 Code Analysis")
        st.markdown(st.session_state.last_analysis)

        st.divider()
        st.markdown("## 🎯 Continue Learning")
        st.write("Want to practice what you just learned?")

        practice_topic = st.selectbox(
            "Choose a topic to practice",
            [
                "Arrays", "Strings", "Loops", "Functions", "Recursion",
                "Linked Lists", "Stacks", "Queues", "Trees", "Graphs",
                "Dynamic Programming", "Binary Search"
            ],
            key="analysis_practice_topic"
        )

        practice_difficulty = st.selectbox(
            "Choose difficulty",
            ["Easy", "Medium", "Hard"],
            key="analysis_practice_difficulty"
        )

        if st.button("🎯 Practice This Topic"):

            with st.spinner("🧠 Creating a personalized question..."):

                try:
                    question = generate_question(practice_topic, practice_difficulty)

                    st.session_state.practice_question = question
                    st.session_state.practice_topic = practice_topic

                    st.success("Question generated! Go to 📚 Practice Mode to solve it.")

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

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
        options=["Beginner", "Intermediate", "Advanced"],
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
                    explanation = explain_code(code, language, level)

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

    code = st.text_area("Paste your code", height=250)
    error = st.text_area("Paste the error message (optional)", height=150)

    if st.button("🔎 Find Bug"):

        if code.strip():

            with st.spinner("🐛 CodeMate is searching for bugs..."):

                try:
                    analysis = find_bug(code, language, error)

                    st.markdown("## 🧠 Bug Analysis")
                    st.write(analysis)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        else:
            st.warning("Please paste your code first.")

# PYTHON CHECKER
elif page == "🧪 Python Checker":

    st.markdown("""<div class="page-header"><h1>🧪 Python Checker</h1><div class="page-description">Quickly check your Python code for syntax errors.</div></div>""", unsafe_allow_html=True)

    code = st.text_area(
        "Paste your Python code",
        height=350,
        placeholder="Paste your Python code here..."
    )

    if st.button("🧪 Check Syntax", type="primary"):

        if code.strip():

            with st.spinner("🧪 Checking syntax..."):

                try:
                    result = check_python_syntax(code)

                    if result.get("valid"):
                        st.success("✅ No syntax errors found!")
                    else:
                        st.error(f"❌ Syntax error: {result.get('error')}")

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        else:
            st.warning("Please paste some code first.")

# EXPLAIN ERROR
elif page == "🔧 Explain Error":

    st.markdown("""<div class="page-header"><h1>🔧 Explain Error</h1><div class="page-description">Turn a confusing error message into a simple explanation.</div></div>""", unsafe_allow_html=True)

    language = st.selectbox(
        "Select programming language",
        ["Python", "C++", "C", "Java", "JavaScript"],
        key="error_language"
    )

    code = st.text_area(
        "Paste your code (optional but helps)",
        height=250
    )

    error_message = st.text_area(
        "Paste the error message",
        height=150,
        placeholder="Paste the full error / traceback here..."
    )

    if st.button("🔧 Explain Error", type="primary"):

        if error_message.strip():

            with st.spinner("🔧 CodeMate is decoding the error..."):

                try:
                    explanation = explain_error(code, language, error_message)

                    st.markdown("## 💡 Error Explained")
                    st.write(explanation)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        else:
            st.warning("Please paste the error message first.")

# CODE IMPROVER
elif page == "✨ Code Improver":

    st.markdown("""<div class="page-header"><h1>✨ Code Improver</h1><div class="page-description">Make your code cleaner, clearer, and easier to maintain.</div></div>""", unsafe_allow_html=True)

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
                    improved = improve_code(code, language)

                    st.markdown("## 🚀 Improved Version")
                    st.markdown(improved)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        else:
            st.warning("Please paste some code first.")

# PRACTICE MODE
elif page == "📚 Practice Mode":

    st.markdown("""<div class="page-header"><h1>📚 Practice Mode</h1><div class="page-description">Practice coding problems and get personalized AI feedback.</div></div>""", unsafe_allow_html=True)

    if "practice_topic" in st.session_state:
        st.info(f"🎯 Current topic: **{st.session_state.practice_topic}**")

    col1, col2 = st.columns(2)

    with col1:
        topic = st.selectbox(
            "📚 Topic",
            [
                "Arrays", "Strings", "Loops", "Functions", "Recursion",
                "Linked Lists", "Stacks", "Queues", "Trees", "Graphs",
                "Dynamic Programming", "Binary Search"
            ],
            key="practice_topic_select"
        )

    with col2:
        difficulty = st.selectbox(
            "🎯 Difficulty",
            ["Easy", "Medium", "Hard"],
            key="practice_difficulty"
        )

    if st.button("🎯 Generate Question", type="primary"):

        with st.spinner("🧠 Creating your coding challenge..."):

            try:
                question = generate_question(topic, difficulty)

                st.session_state.practice_question = question
                st.session_state.practice_topic = topic
                st.session_state.practice_difficulty = difficulty

                st.success("Your challenge is ready! 🚀")

            except Exception as e:
                st.error(f"Could not generate question: {e}")

    if "practice_question" in st.session_state:

        st.divider()
        st.markdown("## 📝 Your Challenge")
        st.markdown(st.session_state.practice_question)

        answer = st.text_area(
            "💻 Your Solution",
            height=300,
            placeholder="Write your solution here..."
        )

        if st.button("🚀 Submit Solution", type="primary"):

            if not answer.strip():
                st.warning("Please write a solution first.")

            else:
                with st.spinner("🔍 CodeMate is evaluating your solution..."):

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
                        st.markdown("## 📊 CodeMate Feedback")
                        st.markdown(feedback)

                        st.metric("Your Score", f"{score}/10")

                        st.success("✅ Your progress has been saved!")

                    except Exception as e:
                        st.error(f"Evaluation failed: {e}")

# PROGRESS
elif page == "📊 My Progress":

    st.markdown("""<div class="page-header"><h1>📊 My Progress</h1><div class="page-description">Track your practice, scores, strengths, and next steps.</div></div>""", unsafe_allow_html=True)

    df = load_progress()

    if df.empty:
        st.info("You haven't completed any practice questions yet. Start practicing! 🚀")

    else:
        insights = get_learning_insights()

        total_problems = len(df)
        average_score = round(df["score"].mean(), 1)
        best_score = df["score"].max()
        topics = df["topic"].nunique()

        # Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Problems Solved", total_problems)

        with col2:
            st.metric("Average Score", f"{average_score}/10")

        with col3:
            st.metric("Best Score", f"{best_score}/10")

        with col4:
            st.metric("Topics Practiced", topics)

        st.divider()

        # Learning Insights
        st.markdown("## 🧠 Learning Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.success(
                f"🏆 **Strongest Topic**\n\n"
                f"{insights['strongest_topic']}\n\n"
                f"Average Score: **{insights['strongest_score']}/10**"
            )

        with col2:
            st.warning(
                f"⚠️ **Needs More Practice**\n\n"
                f"{insights['weakest_topic']}\n\n"
                f"Average Score: **{insights['weakest_score']}/10**"
            )

        st.divider()

        # Recommendation
        st.markdown("## 🎯 Recommended Next Step")

        if insights["weakest_score"] < 6:
            st.info(
                f"CodeMate recommends focusing on **{insights['weakest_topic']}**.\n\n"
                f"Try 3 Easy problems on this topic before moving to a harder difficulty."
            )

        elif insights["weakest_score"] < 8:
            st.info(
                f"You're making progress!\n\n"
                f"Practice more **{insights['weakest_topic']}** to strengthen your understanding."
            )

        else:
            st.success("🎉 You're performing consistently well! Try a new topic or increase the difficulty.")

        st.divider()

        # Score history
        st.markdown("## 📈 Score History")

        chart_data = df[["date", "score"]].copy()
        chart_data = chart_data.set_index("date")

        st.line_chart(chart_data)

        # Topic performance
        st.markdown("## 📚 Topic Performance")

        topic_performance = (
            df.groupby("topic")["score"]
            .mean()
            .round(2)
            .sort_values(ascending=False)
        )

        st.bar_chart(topic_performance)

        # Difficulty
        st.markdown("## 🎯 Difficulty Distribution")

        difficulty_counts = df["difficulty"].value_counts()

        st.bar_chart(difficulty_counts)

        # History
        st.markdown("## 📝 Practice History")

        st.dataframe(df, use_container_width=True)

# CODE REVIEW
elif page == "⭐ Code Review":

    st.markdown("""<div class="page-header"><h1>⭐ Code Review</h1><div class="page-description">Get a structured review of readability, efficiency, naming, and best practices.</div></div>""", unsafe_allow_html=True)

    language = st.selectbox(
        "Language",
        ["Python", "C++", "C", "Java", "JavaScript"],
        key="review_language"
    )

    code = st.text_area("Paste your code", height=350)

    if st.button("⭐ Review Code", type="primary"):

        if code.strip():

            with st.spinner("Reviewing code..."):

                try:
                    review = review_code(code, language)

                    readability = extract_metric(review, "READABILITY")
                    efficiency = extract_metric(review, "EFFICIENCY")
                    structure = extract_metric(review, "STRUCTURE")
                    naming = extract_metric(review, "NAMING")
                    error_handling = extract_metric(review, "ERROR_HANDLING")
                    best_practices = extract_metric(review, "BEST_PRACTICES")

                    overall = round(
                        (
                            readability + efficiency + structure +
                            naming + error_handling + best_practices
                        ) / 6,
                        1
                    )

                    st.metric("Overall Score", f"{overall}/10")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Readability", readability)
                        st.metric("Structure", structure)

                    with col2:
                        st.metric("Efficiency", efficiency)
                        st.metric("Naming", naming)

                    with col3:
                        st.metric("Error Handling", error_handling)
                        st.metric("Best Practices", best_practices)

                    st.divider()
                    st.markdown(review)

                except Exception as e:
                    st.error(f"Review failed: {e}")

        else:
            st.warning("Please paste some code.")
