import streamlit as st

st.set_page_config(
    page_title="CodeMate",
    page_icon="💻",
    layout="wide"
)

st.title("💻 CodeMate")
st.subheader("Your AI-powered coding companion")

st.divider()

st.write("Welcome to CodeMate! 🚀")
st.write(
    "Understand code, find bugs, improve your solutions, "
    "and practice programming concepts."
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🧠 Code Explainer")
    st.write("Understand what your code does.")

with col2:
    st.markdown("### 🐛 Bug Finder")
    st.write("Find and understand errors in your code.")

with col3:
    st.markdown("### ✨ Code Improver")
    st.write("Make your code cleaner and easier to read.")

st.divider()

st.info("🚧 CodeMate is currently under development.")