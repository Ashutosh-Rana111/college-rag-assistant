from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent


# Saved RAG artifacts
MODEL_DIR = BASE_DIR / "models"

CHUNKS_PATH = MODEL_DIR / "chunks.pkl"
FAISS_INDEX_PATH = MODEL_DIR / "college_index.faiss"


# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# Gemini models
PRIMARY_MODEL = "gemini-3.6-flash"
FALLBACK_MODEL = "gemini-3.5-flash-lite"


# Retrieval
TOP_K = 5


# Environment variable containing the Gemini API key
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"