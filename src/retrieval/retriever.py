import pickle

import faiss
from sentence_transformers import SentenceTransformer

from src.config import (
    CHUNKS_PATH,
    FAISS_INDEX_PATH,
    EMBEDDING_MODEL,
    TOP_K,
)


# Load saved RAG data
with open(CHUNKS_PATH, "rb") as f:
    chunks = pickle.load(f)

index = faiss.read_index(str(FAISS_INDEX_PATH))

embedding_model = SentenceTransformer(EMBEDDING_MODEL)


def retrieve(question, k=TOP_K):
    """Retrieve the most relevant chunks for a question."""

    query_embedding = embedding_model.encode(
        [question]
    ).astype("float32")

    distances, indices = index.search(query_embedding, k)

    results = []

    for rank, idx in enumerate(indices[0], start=1):
        idx = int(idx)
        chunk = chunks[idx]

        results.append({
            "rank": rank,
            "distance": float(distances[0][rank - 1]),
            "text": chunk["text"],
            "filename": chunk["filename"],
            "page": chunk["page"],
        })

    return results