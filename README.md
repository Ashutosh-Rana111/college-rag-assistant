# 🎓 College Knowledge Assistant

A Retrieval-Augmented Generation (RAG) based college knowledge assistant built specifically for the **University Institute of Engineering and Technology, Kurukshetra University (UIET KUK)**.

The system answers questions using a collection of college documents.
When the required information is not available in the provided documents, the assistant can use Google Search grounding to retrieve information from the official college websites.

## 📚 Source Documents

The original college PDFs used to build the knowledge base are available here:

[College PDF Collection](https://drive.google.com/drive/folders/1jSM7QkAaE5sfkPfToyazpeyz9geavI-F?usp=drive_link)

The assistant also uses the following official websites for additional
college-specific information:

- [UIET KUK](https://www.uietkuk.ac.in)
- [Kurukshetra University](https://kuk.ac.in/index.html)

## ✨ Features

- PDF-based knowledge retrieval
- Semantic search using Sentence Transformers
- FAISS vector database for fast retrieval
- Gemini-powered answer generation
- Primary and fallback Gemini models
- Google Search grounding for additional official information
- Source document and page references
- Streamlit web interface
- Answers grounded in provided sources rather than unrestricted
  general knowledge

## 🧠 Architecture

```text
                    User Question
                         │
                         ▼
                  Sentence Transformer
                         │
                         ▼
                    FAISS Retrieval
                         │
                         ▼
              Relevant College Documents
                         │
                         ▼
                       Gemini
                    /           \
                   /             \
          Documents sufficient?  No
                 │                │
                Yes               ▼
                 │        Google Search Grounding
                 │                │
                 │                ▼
                 │       Official College Websites
                 │                │
                 └───────┬────────┘
                         ▼
                       Answer
                         │
                         ▼
                 Streamlit Interface
```

## Technology Stack
- Python
- Streamlit -> web interface
- Sentence Transformers -> semantic embeddings
- FAISS -> vector similarity search
Google Gemini API -> answer generation
Google Search grounding -> additional web-based retrieval

## Gemini Models

The application uses:

Primary: `gemini-3.6-flash`
Fallback: `gemini-3.5-flash-lite`

If the primary model fails, the fallback model is used.

## 📁 Project Structure
```text
college-rag-assistant/
├── data/
│   ├── raw_pdfs/Drive_Link.txt
├── models/
│   ├── chunks.pkl
│   ├── embeddings.npy
│   └── college_index.faiss
├── src/
│   ├── ingestion/
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── web_search.py
│   ├── generation/
│   │   ├── prompts.py
│   │   └── llm_client.py
│   ├── config.py
│   └── rag_pipeline.py
├── app/
│   └── college_rag_assistant.py
├── tests/
├── notebooks/RAG.ipynb
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## RAG Knowledge Base

The deployed application uses pre-built RAG artifacts stored in the `models/` directory:

chunks.pkl -> text chunks and their document/page metadata
college_index.faiss -> FAISS vector index
embeddings.npy -> saved embedding vectors

The original PDFs are not required by the deployed application for normal
question answering because the relevant text has already been processed
into the RAG knowledge base.

## ⚠️ Current Limitations
- The knowledge base is limited to the documents used during indexing.
- Website information depends on the availability and accessibility of the official college websites.
- Answers are limited to information that can be retrieved from the available sources.
- The system does not guarantee that every piece of information on the college websites or in the source documents will be retrieved for every question.
