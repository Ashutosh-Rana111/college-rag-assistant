import streamlit as st

from src.rag_pipeline import ask_rag


st.set_page_config(
    page_title="College Knowledge Assistant",
    page_icon="🎓",
    layout="centered",
)


st.title("🎓 College Knowledge Assistant")
st.write(
    "Ask questions about the college, academics, facilities, "
    "departments, rules, procedures, and more."
)


question = st.text_input(
    "Ask your question:",
    placeholder="e.g. How many semesters are there in CSE?",
)


if st.button("Ask") and question.strip():

    with st.spinner("Searching..."):

        result = ask_rag(question)

    st.markdown("### Answer")
    st.write(result["answer"])

    if result["sources"]:
        st.markdown("### Sources")

        for source in result["sources"]:
            st.write(f"- {source}")

    if result["model"]:
        st.caption(f"Model: {result['model']}")