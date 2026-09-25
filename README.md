# 🎓 College Knowledge Assistant

A Retrieval-Augmented Generation (RAG) based college knowledge assistant built for the **University Institute of Engineering and Technology, Kurukshetra University (UIET KUK)**.

The application lets users ask questions about college academics, facilities, departments, rules, procedures, and other information contained in the college's source documents.

## ✨ Features

- PDF-based knowledge retrieval
- Page-aware document processing
- Semantic search using Sentence Transformers
- FAISS vector similarity search
- Gemini-powered answer generation
- Primary and fallback Gemini models
- Source document and page references
- Streamlit web interface
- Automated knowledge-base updates from Google Drive
- Monthly GitHub Actions rebuild
- Manual knowledge-base rebuild through GitHub Actions
- Safe temporary PDF ingestion during automated updates

## 🧠 How It Works

```text
                         User Question
                              │
                              ▼
                  Sentence Transformer
                    (MiniLM embeddings)
                              │
                              ▼
                       FAISS Retrieval
                         Top 5 chunks
                              │
                              ▼
                 Retrieved document context
                 + filename + page metadata
                              │
                              ▼
                         Gemini API
                       /            \
                      /              \
             Primary model       If primary fails
                      │              │
                      │              ▼
                      │       Fallback model
                      │              │
                      └──────┬───────┘
                             ▼
                       Grounded Answer
                             │
                             ▼
                    Sources / Page Numbers
                             │
                             ▼
                    Streamlit Interface
```

## 🔄 Automated Knowledge-Base Updates

The source PDFs are maintained in a Google Drive folder rather than being stored permanently in the GitHub repository.

The automated pipeline is:

```text
Google Drive
     │
     ▼
GitHub Actions
     │
     ▼
Download current PDFs to temporary runner
     │
     ▼
Extract text + create chunks
     │
     ▼
Generate MiniLM embeddings
     │
     ▼
Build FAISS index
     │
     ▼
Save updated RAG artifacts
     │
     ▼
Commit changes to GitHub
     │
     ▼
Streamlit automatically redeploys
```

The workflow runs automatically on the **1st day of every month** and can also be triggered manually from GitHub Actions.

If a PDF is added or removed from the Google Drive source folder, the next rebuild creates the knowledge base from the current PDF collection.

The PDFs are downloaded into a temporary GitHub Actions runner during the rebuild. They are **not committed to the repository**.

### Source Documents

The source PDF collection is maintained here:

[College PDF Collection](https://drive.google.com/drive/folders/1jSM7QkAaE5sfkPfToyazpeyz9geavI-F?usp=drive_link)

## 🤖 Gemini Models

The application currently uses:

- **Primary:** `gemini-3.6-flash`
- **Fallback:** `gemini-3.5-flash-lite`

If the primary Gemini request fails, the application automatically attempts the fallback model.

The Gemini API key is stored as a Streamlit secret and is not included in the repository.

## 🧩 Technology Stack

- **Python** — application and data-processing logic
- **Streamlit** — web interface
- **Sentence Transformers** — semantic embeddings
- **all-MiniLM-L6-v2** — embedding model
- **FAISS** — vector similarity search
- **Google Gemini API** — answer generation
- **PyPDF** — PDF text extraction
- **LangChain Text Splitters** — document chunking
- **Google Drive API** — source document retrieval
- **GitHub Actions** — automated knowledge-base rebuilding

## 📁 Project Structure

```text
college-rag-assistant/
├── .github/
│   └── workflows/
│       └── update-knowledge-base.yml
│
├── app/
│   └── college_rag_assistant.py
│
├── models/
│   ├── chunks.pkl
│   └── college_index.faiss
│
├── notebooks/
│   ├── RAG1.ipynb
│   └── RAG2.ipynb
│
├── src/
│   ├── ingestion/
│   │   └── download_pdfs.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── generation/
│   │   ├── prompts.py
│   │   └── llm_client.py
│   │
│   ├── build_index.py
│   ├── config.py
│   └── rag_pipeline.py
│
├── requirements.txt
├── requirements-ingestion.txt
├── .env.example
├── .gitignore
└── README.md
```

## 📦 RAG Knowledge Base

The deployed application uses two pre-built artifacts:

```text
models/
├── chunks.pkl
└── college_index.faiss
```

### `chunks.pkl`

Contains the processed text chunks together with metadata such as:

- source filename
- page number
- extracted text

### `college_index.faiss`

Contains the FAISS vector index used for semantic similarity retrieval.

The original PDFs are not required by the deployed application during normal question answering because their relevant content has already been processed into the RAG knowledge base.

## 🛠️ Local Setup

Clone the repository:

```bash
git clone https://github.com/Ashutosh-Rana111/college-rag-assistant.git
cd college-rag-assistant
```

Install the application dependencies:

```bash
pip install -r requirements.txt
```

Set the Gemini API key as an environment variable:

```text
GEMINI_API_KEY=your_api_key
```

Then run the Streamlit application:

```bash
streamlit run app/college_rag_assistant.py
```

## 🔧 Rebuilding the Knowledge Base

The repository contains a separate ingestion dependency file:

```text
requirements-ingestion.txt
```

The automated rebuild process uses:

```text
src/ingestion/download_pdfs.py
src/build_index.py
```

The build process:

1. Downloads the current PDF collection from Google Drive.
2. Extracts text page by page.
3. Splits the extracted text into chunks.
4. Generates embeddings using `all-MiniLM-L6-v2`.
5. Builds a FAISS `IndexFlatL2` index.
6. Saves `chunks.pkl` and `college_index.faiss`.

The GitHub Actions workflow performs this process automatically.

## 🔐 Secrets and Security

The project uses secrets for credentials that should not be committed to GitHub.

The automated Google Drive workflow uses:

```text
GDRIVE_SERVICE_ACCOUNT_JSON
```

The deployed Streamlit application uses:

```text
GEMINI_API_KEY
```

Neither credential should be committed to the repository.

## 🌐 Deployment

The application is deployed using Streamlit.

The deployed application uses the processed artifacts in `models/` and does not need access to the original Google Drive PDFs during normal question answering.

When GitHub Actions produces a new knowledge-base commit, the Streamlit deployment can automatically redeploy from the updated repository.

## ⚠️ Current Limitations

- The knowledge base is limited to the content available in the source PDF collection.
- PDF extraction quality depends on the structure and encoding of the source PDFs.
- Scanned/image-only PDFs may not provide usable text without OCR.
- Answers depend on the quality of retrieved chunks.
- Gemini API availability and response latency can vary.
- The system does not guarantee that every relevant piece of information will be retrieved for every question.
- The automated update process currently processes PDFs directly contained in the configured Google Drive folder.

## 📌 Project Status

The project currently includes:

- RAG-based question answering
- FAISS semantic retrieval
- Gemini answer generation with fallback
- Streamlit deployment
- Google Drive document source
- Automated GitHub Actions knowledge-base rebuilding
- Monthly scheduled synchronization
- Manual knowledge-base update capability

