# PDF Knowledge Base (RAG)

A chatbot that answers questions about your own PDF documents. It uses Retrieval-Augmented Generation (RAG): relevant passages are retrieved from your documents first, then a local LLaMA model writes an answer grounded in those passages. Everything runs on your own machine, so there are no API keys, no usage costs, and your documents never leave your computer.

## Features

- Ask questions about one or many PDFs in natural language
- Answers are grounded in your documents; the bot says so when the answer isn't in them
- Every answer shows the exact source chunks it used
- Chat interface with conversation history
- Simple intent handling so greetings and small talk don't trigger document search
- 100% local: LLaMA 3.2 runs through Ollama

## How it works

```
Indexing (run once per set of PDFs)
PDFs -> load pages -> split into 500-character chunks (50 overlap)
     -> embed each chunk -> store vectors in ChromaDB

Answering (every question)
Question -> embed -> find the 3 most similar chunks in ChromaDB
         -> build a prompt with those chunks -> LLaMA 3.2 -> answer + sources
```

The key idea: the model is never retrained on your documents. It is shown the most relevant passages right before it answers, like an open-book exam.

## Tech stack

| Component | Tool |
|---|---|
| Orchestration | LangChain |
| Vector database | ChromaDB |
| LLM and embeddings | LLaMA 3.2 via Ollama |
| PDF parsing | PyPDF |
| Interface | Streamlit |

## Project structure

```
rag-project/
├── app.py             # Streamlit chat interface
├── ingest.py          # Loads PDFs, chunks, embeds, stores in ChromaDB
├── query.py           # Terminal version of the Q&A loop
├── requirements.txt
└── data/              # Put your PDFs here (not tracked by git)
```

## Setup

Requires macOS or Linux, Python 3.9 or newer, and [Ollama](https://ollama.com).

### 1. Install Ollama and pull the model

```bash
brew install ollama
brew services start ollama
ollama pull llama3.2
```

### 2. Clone the repo and create a virtual environment

```bash
git clone https://github.com/YOUR_USERNAME/rag-project.git
cd rag-project
python3 -m venv rag-env
source rag-env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your PDFs and build the index

```bash
mkdir -p data
cp /path/to/your-document.pdf data/
python3 ingest.py
```

`ingest.py` clears any previous index and rebuilds it from every PDF in `data/`. Run it again whenever you add or change documents.

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`. You can also use the terminal version with `python3 query.py`.

## Configuration

Settings you can change in the code:

| Setting | Location | Default |
|---|---|---|
| Chunk size and overlap | `ingest.py` | 500 / 50 characters |
| Chunks retrieved per question | `app.py`, `query.py` | 3 |
| Model | `app.py`, `ingest.py`, `query.py` | `llama3.2` |

Smaller chunks give more precise retrieval; larger chunks keep more context. Tune these against your own documents.

## Limitations

- Scanned PDFs that contain only images have no extractable text. Use PDFs with selectable text, or add OCR.
- A small local model can miss details or phrase answers imperfectly, especially for questions that span many pages.
- Embeddings use the same LLaMA model as generation, which works but is slower than a dedicated embedding model.

## Possible improvements

- Upload PDFs directly in the interface
- Use a dedicated embedding model and compare retrieval quality
- Add reranking and hybrid keyword search
- Evaluate retrieval precision on a labeled question set

## Skills demonstrated

RAG pipeline design, text chunking, vector embeddings and semantic search, working with a vector database, running local LLMs, prompt design for grounded answers, and building a Streamlit application.
