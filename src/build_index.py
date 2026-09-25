from pathlib import Path
import pickle

import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


PDF_DIR = Path("data/raw_pdfs")
MODEL_DIR = Path("models")

CHUNKS_PATH = MODEL_DIR / "chunks.pkl"
INDEX_PATH = MODEL_DIR / "college_index.faiss"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_pages():
    pages = []

    for pdf_path in sorted(PDF_DIR.glob("*.pdf")):
        reader = PdfReader(pdf_path)

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text and text.strip():
                pages.append({
                    "filename": pdf_path.name,
                    "page": page_number,
                    "text": text,
                })

    return pages


def create_chunks(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = []

    for page in pages:
        page_chunks = splitter.split_text(page["text"])

        for text in page_chunks:
            chunks.append({
                "filename": page["filename"],
                "page": page["page"],
                "text": text,
            })

    return chunks


def build_index(chunks):
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index


def main():
    if not PDF_DIR.exists():
        raise RuntimeError(f"PDF directory not found: {PDF_DIR}")

    pdf_files = list(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        raise RuntimeError("No PDF files found.")

    print(f"Found {len(pdf_files)} PDF files.")

    pages = load_pages()
    print(f"Extracted {len(pages)} pages.")

    chunks = create_chunks(pages)
    print(f"Created {len(chunks)} chunks.")

    index = build_index(chunks)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

    faiss.write_index(index, str(INDEX_PATH))

    print(f"Saved chunks to {CHUNKS_PATH}")
    print(f"Saved FAISS index to {INDEX_PATH}")
    print("Knowledge base rebuild complete.")


if __name__ == "__main__":
    main()
