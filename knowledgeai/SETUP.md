# KnowledgeAI — Setup Guide

## Prerequisites
- Python 3.10 or higher
- Your OpenAI API key

---

## 1. Install dependencies

```bash
cd knowledgeai
pip install -r requirements.txt
```

---

## 2. Configure environment

```bash
cp .env.example .env
```

Open `.env` and set your API key:

```
OPENAI_API_KEY=sk-your-key-here
```

---

## 3. Add your BRD documents

Copy your requirement documents (PDF, DOCX, TXT, MD) into the `BRDs/` folder.
The server will automatically detect and ingest them on startup.

```
knowledgeai/
└── BRDs/
    ├── project-alpha-brd.pdf
    ├── payment-module-spec.docx
    └── ...
```

---

## 4. Start the server

```bash
python run.py
```

Then open your browser at: **http://localhost:8000**

---

## How it works

| Step | What happens |
|------|-------------|
| **Startup** | Server scans `BRDs/` and ingests all documents |
| **File watcher** | Any new/modified file in `BRDs/` is auto-ingested |
| **Upload tab** | Drag & drop files via the UI to ingest manually |
| **Ask tab** | Type a question → hybrid search → GPT-4o answers with citations |
| **Knowledge Base** | Browse, search, and delete documents |
| **Analytics** | View query counts, cache hit rate, confidence, latency |

---

## Architecture summary

```
User query
  → API Gateway (FastAPI)
  → Access Control
  → Semantic Cache (in-memory)   ← hit: <100ms, no LLM call
  → Embed query (OpenAI)
  → Hybrid Search (ChromaDB vector + SQLite BM25)
  → Re-ranker (token overlap + vector score blend)
  → Confidence threshold check
  → Prompt Builder
  → GPT-4o (streaming via WebSocket)
  → Citation Formatter
  → Answer with sources shown in UI
```

Document ingestion:
```
File drop / BRDs folder
  → Parser (pdfplumber / python-docx / text)
  → Chunker (400 words, 50-word overlap)
  → OpenAI Embeddings (text-embedding-3-small)
  → ChromaDB (vector index)
  → SQLite FTS5 (keyword/BM25 index)
  → SQLite metadata (doc_id, version, folder, page count)
```

---

## Configuration (`.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_MODEL` | `gpt-4o` | OpenAI chat model |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `CHUNK_SIZE` | `400` | Words per chunk |
| `CHUNK_OVERLAP` | `50` | Overlap words between chunks |
| `TOP_K` | `10` | Candidates retrieved before re-ranking |
| `RERANK_TOP_N` | `3` | Chunks sent to LLM after re-ranking |
| `CONFIDENCE_THRESHOLD` | `0.35` | Min confidence to call LLM (else fallback) |
| `CACHE_SIMILARITY_THRESHOLD` | `0.92` | Cosine similarity for cache hit |
| `PORT` | `8000` | Server port |
