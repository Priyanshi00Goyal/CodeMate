import streamlit as st

st.set_page_config(
    page_title="CodeMate",
    page_icon="💻",
    layout="wide"
)

# Sidebar
st.sidebar.title("💻 CodeMate")
st.sidebar.caption("Your AI Coding Companion")

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

    st.title("💻 CodeMate")
    st.subheader("Your AI-powered coding companion")

    st.write(
        "Understand code, find bugs, improve your solutions, "
        "and practice programming concepts."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🧠 Code Explainer")
        st.write("Understand code line by line.")

    with col2:
        st.markdown("### 🐛 Bug Finder")
        st.write("Find and understand programming errors.")

    with col3:
        st.markdown("### ✨ Code Improver")
        st.write("Make your code cleaner and easier to understand.")

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
            st.info(
                f"Code explanation for {language} will appear here."
            )
        else:
            st.warning("Please paste some code first.")

# BUG FINDER
elif page == "🐛 Bug Finder":

    st.title("🐛 Bug Finder")

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
            st.info("Bug analysis will appear here.")
        else:
            st.warning("Please paste your code first.")

# CODE IMPROVER
elif page == "✨ Code Improver":

    st.title("✨ Code Improver")

    code = st.text_area(
        "Paste your code",
        height=300
    )

    if st.button("✨ Improve Code"):
        if code.strip():
            st.info("Improved code will appear here.")
        else:
            st.warning("Please paste your code first.")

# PRACTICE MODE
elif page == "📚 Practice Mode":

    st.title("📚 Practice Mode")

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
        st.info(
            f"A {difficulty} {topic} question will appear here."
        )

# PROGRESS
elif page == "📊 My Progress":

    st.title("📊 My Progress")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Problems Solved", 0)

    with col2:
        st.metric("Concepts Learned", 0)

    with col3:
        st.metric("Practice Streak", "0 days")

    st.divider()

    st.info(
        "Your coding progress tracker will be connected here."
    )
