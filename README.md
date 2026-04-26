# Islam-QA Search Service

> ⚠️ This project is in early development. Contributions and feedback are welcome.

## Related Repositories

| Service | Repository |
|---|---|
| ⚙️ Backend Service | [Islam-QA](https://github.com/alikashlan10/Islam-QA) |
| 🖥️ Frontend UI | [Islam-QA-UI](https://github.com/alikashlan10/Islam-QA-UI) |

---

## Overview

Islam-QA Search Service is the retrieval engine of the Islam-QA system. It accepts a user query, performs hybrid semantic search against the Qdrant vector database, reranks results using Cohere, and generates a grounded answer using an LLM.

It is intentionally kept lightweight and separate from the backend ingestion service — making it easy to deploy independently.

---

## Architecture

```
User Query
    │
    ▼
Embedder — embed query (dense vector)
    │
    ▼
Qdrant Hybrid Search — dense + BM25 sparse (top K results)
    │
    ▼
Reranker (Cohere) — reorder by relevance (top N results)
    │
    ▼
LLM (Groq / Gemini / OpenAI) — generate grounded answer
    │
    ▼
Answer + Sources (video title, thumbnail, chunk text)
```

---

## Features

- Hybrid search — dense semantic + BM25 sparse vectors
- Reranking via Cohere for improved relevance
- LLM answer generation grounded in retrieved context
- API key authentication
- Fully swappable providers via environment config
- Clean Architecture — modular and maintainable
- Deployed on Azure Container Apps

---

## Tech Stack

| Component | Technology |
|---|---|
| API | FastAPI |
| Vector Store | Qdrant Cloud |
| Embeddings | LangChain (HuggingFace / OpenAI / Cohere / Google) |
| Reranker | Cohere Rerank |
| LLM | Groq / Gemini / OpenAI via LangChain |

---

## Project Structure

```
src/
├── domain/              # models and enums
├── application/         # use cases and factories
│   ├── factories/       # embedder, vector store, reranker, LLM factories
│   └── use_cases/       # RetrieveAnswerUseCase
├── infrastructure/      # concrete implementations
└── api/                 # FastAPI routers, auth, dependencies
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Qdrant Cloud account (or local Qdrant instance)
- API keys for your chosen providers

### Installation

```bash
git clone https://github.com/alikashlan10/Islam-QA-Search
cd Islam-QA-Search
pip install -r requirements.txt
```

### Environment Variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

All required variables are documented in `.env.example`.

### Run Locally

```bash
uvicorn src.api.main:app --reload --port 8000
```

### Test

```bash
curl -X POST http://localhost:8000/search \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"query": "ما حكم الميراث للعم؟"}'
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/search` | Submit a query and get an answer with sources |
| GET | `/health` | Health check |

### Request

```json
{
  "query": "ما حكم الميراث للعم؟"
}
```

### Response

```json
{
  "answer": "يرث العم إذا...",
  "sources": [
    {
      "video_id": "dQw4w9WgXcQ",
      "title": "شرح الميراث",
      "thumbnail_url": "https://img.youtube.com/...",
      "chunk_index": 2,
      "chunk": "..."
    }
  ]
}
```

---

## Authentication

All endpoints require an API key passed in the request header:

```
X-API-Key: your_secret_api_key
```


---

## Deployment

The service is deployed on Azure Container Apps. See the GitHub Actions workflow at `.github/workflows/deploy.yml` for the full CI/CD pipeline.

---

## License

MIT
