from src.retrieval.retriever import retrieve
from src.generation.prompts import build_prompt
from src.generation.llm_client import generate_answer


def ask_rag(question, k=None):
    """Run the complete RAG pipeline."""

    if k is None:
        results = retrieve(question)
    else:
        results = retrieve(question, k=k)

    prompt = build_prompt(question, results)

    response = generate_answer(prompt)

    sources = []

    for r in results:
        source = f"{r['filename']} — Page {r['page']}"

        if source not in sources:
            sources.append(source)

    return {
        "answer": response["answer"],
        "sources": sources,
        "model": response["model"],
    }