# 🎓 College Knowledge Assistant

A Retrieval-Augmented Generation (RAG) based college knowledge assistant.
This is made specifically for **University Institute of Engineering and Technology, Kurukshetra University**

The system answers questions using a collection of college documents and can also use the official college websites when the required information is not available in the documents.

### Drive Link for all pdfs:
https://drive.google.com/drive/folders/1jSM7QkAaE5sfkPfToyazpeyz9geavI-F?usp=drive_link

## Features

- PDF-based knowledge retrieval
- Semantic search using Sentence Transformers
- FAISS vector database
- Gemini-powered answer generation
- Google Search grounding for official college websites
- Source document and page references
- Streamlit web interface
- Gemini fallback model for improved reliability

## Architecture

```text
User Question
      ↓
FAISS Retrieval
      ↓
Relevant College Documents
      ↓
Gemini
      ↓
Answer
      │
      └── If required → Official College Websites

## Technology Stack

- Python
- Streamlit
- Sentence Transformers
- FAISS
- Google Gemini API
- Google Search grounding

## Knowledge Sources

The assistant uses:

- College-provided documents:
https://drive.google.com/drive/folders/1jSM7QkAaE5sfkPfToyazpeyz9geavI-F?usp=drive_link

- https://www.uietkuk.ac.in
- https://kuk.ac.in/index.html

