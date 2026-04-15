# Vedra — Verified Intelligence Engine

Vedra is a production-ready full-stack platform that upgrades the original prototype chatbot into a **multi-model, multi-source verification engine**.

## What changed

- ✅ Removed Streamlit runtime from the final system.
- ✅ Added async FastAPI backend with modular services.
- ✅ Added multi-model orchestration (OpenAI + Anthropic + graceful fallback).
- ✅ Added YouTube HD video retrieval + ranking pipeline.
- ✅ Added high-resolution image retrieval pipeline (Unsplash / Google CSE fallback).
- ✅ Added verification engine that compares model consistency and computes confidence.
- ✅ Added Next.js + Tailwind frontend with tabs and structured result views.
- ✅ Added privacy mode handling end-to-end.
- ✅ Added i18n dictionary for 7 languages.
- ✅ Added Redis-backed caching with in-memory fallback.
- ✅ Added Dockerfiles + docker-compose for production deployment.

---

## Architecture

### Backend (FastAPI)

`backend/app/main.py`
- App bootstrap, CORS, logging middleware, health endpoint.

`backend/app/api/routes.py`
- `POST /api/v1/query`: runs model orchestration, verification, videos, images.
- `POST /api/v1/videos`: video-only search.
- `POST /api/v1/images`: image-only search.

`backend/app/services/`
- `ai_orchestrator.py`: parallel calls to OpenAI + Anthropic, with error isolation.
- `verification_engine.py`: consistency scoring + confidence computation + answer merge.
- `youtube_service.py`: YouTube API fetch + HD filtering + ranking by views and recency.
- `image_service.py`: Unsplash or Google CSE fetch + HD filtering + deduplication.

`backend/app/core/`
- `config.py`: environment-driven config.
- `cache.py`: Redis cache with in-memory fallback.
- `logging_middleware.py`: request timing and structured logs.

### Frontend (Next.js + Tailwind)

`frontend/src/components/`
- `SearchBar`: query + language + privacy toggle.
- `ResultTabs`: Answer/Videos/Images tabs.
- `VideoCard`: thumbnail, title, views, publish date.
- `ImageGrid`: lazy-loaded image cards.
- `ConfidenceIndicator`: visual confidence score.

`frontend/src/lib/`
- `api.ts`: backend integration.
- `types.ts`: shared API response types.
- `i18n.ts`: language dictionary for EN, HI, BN, KN, TA, TE, MR.

---

## API response shape (`POST /api/v1/query`)

```json
{
  "query": "...",
  "final_answer": "...",
  "model_outputs": [
    {"model": "openai", "response": "..."},
    {"model": "anthropic", "response": "..."}
  ],
  "confidence_score": 0.87,
  "verification_notes": "...",
  "sources": [],
  "videos": [],
  "images": []
}
```

---

## Environment Variables

Create a `.env` file in repo root:

```bash
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
YOUTUBE_API_KEY=
UNSPLASH_API_KEY=
GOOGLE_CSE_API_KEY=
GOOGLE_CSE_ID=
REDIS_URL=redis://redis:6379/0
```

---

## Local development

### Backend

```bash
pip install -r requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
NEXT_PUBLIC_API_BASE=http://localhost:8000/api/v1 npm run dev
```

### Docker Compose

```bash
docker compose up --build
```

---

## Migration steps completed

1. Extracted logic from prototype and replaced streamlit flow.
2. Implemented async AI multi-model orchestrator.
3. Implemented YouTube pipeline with HD filtering and ranking.
4. Implemented image pipeline with quality + dedupe filtering.
5. Implemented verification engine.
6. Exposed all APIs in FastAPI.
7. Built Next.js + Tailwind UI components.
8. Connected frontend to backend.
9. Added parallel execution and graceful error handling.
10. Added caching + Docker + request logging middleware.

