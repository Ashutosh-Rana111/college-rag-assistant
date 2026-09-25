import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from src.rag_pipeline import ask_rag


# --------------------------------------------------
# Page configuration

st.set_page_config(
    page_title="UIET KUK Knowledge Assistant",
    page_icon="🎓",
    layout="centered",
)

# --------------------------------------------------
# Custom styling

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.6rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1.05rem;
            color: #aab2c0;
            margin-bottom: 1.5rem;
        }

        .info-card {
            padding: 1rem 1.2rem;
            border-radius: 12px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 1.5rem;
        }

        .source-box {
            padding: 0.7rem 1rem;
            border-radius: 8px;
            background: rgba(255,255,255,0.035);
            margin-bottom: 0.4rem;
        }

        .footer {
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            text-align: center;
            color: #8d96a5;
            font-size: 0.9rem;
        }

        .stButton > button {
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Header

st.markdown(
    '<div class="main-title">🎓 UIET, Kurukshetra University<br>'
    'Knowledge Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Ask questions about UIET, academics, departments, facilities, "
    "rules, procedures, courses, and more."
    "</div>",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Info card

st.markdown(
    """
    <div class="info-card">
        <b>📚 College Knowledge Base</b><br>
        This assistant uses college documents and retrieves relevant
        information before generating an answer with Gemini.
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Question form

with st.form("question_form"):

    question = st.text_input(
        "Ask your question:",
        placeholder="e.g. How many semesters are there in CSE?",
    )

    submitted = st.form_submit_button(
        "🔍 Ask",
        use_container_width=False,
    )


# --------------------------------------------------
# Main answer

if submitted and question.strip():

    with st.spinner("Searching the college knowledge base..."):

        result = ask_rag(question.strip())

    st.markdown("## Answer")

    st.write(result["answer"])

    if result["sources"]:

        st.markdown("## 📚 Sources")

        with st.expander("View source documents"):

            for source in result["sources"]:
                st.markdown(
                    f'<div class="source-box">📄 {source}</div>',
                    unsafe_allow_html=True,
                )

    if result["model"]:
        st.caption(f"Generated using {result['model']}")


# --------------------------------------------------
# Example / Demo section
# Hidden until user clicks

st.markdown("---")

with st.expander("✨ See the assistant in action"):

    st.write(
        "Click an example below to run a real query through the "
        "RAG pipeline."
    )

    example_questions = [
        "How many semesters are there in CSE?",
        "What are the laboratory policies?",
        "How do students register for hostel facilities?",
    ]

    for i, example in enumerate(example_questions):

        if st.button(
            example,
            key=f"example_{i}",
            use_container_width=True,
        ):

            with st.spinner("Searching..."):

                result = ask_rag(example)

            st.markdown("### Answer")

            st.write(result["answer"])

            if result["sources"]:

                st.markdown("### 📚 Sources")

                for source in result["sources"]:
                    st.markdown(f"- {source}")

            if result["model"]:
                st.caption(f"Model: {result['model']}")


# --------------------------------------------------
# Footer

st.markdown(
    """
    <div class="footer">
        <b>UIET, Kurukshetra University Knowledge Assistant</b><br>
        Built using RAG, FAISS, Sentence Transformers, Gemini and Streamlit.<br><br>
        📂
        <a href="https://drive.google.com/drive/folders/1jSM7QkAaE5sfkPfToyazpeyz9geavI-F?usp=drive_link"
           target="_blank">
            View the college document collection
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
