# TruthGuard

**Adversarial verification for multi-document question answering.** TruthGuard is a runnable full-stack MVP: React + Vite frontend, FastAPI backend, SQLite metadata store, PDF/DOCX/TXT ingestion, chunking, lexical evidence retrieval, extractive synthesis, candidate contradiction checks, explicit abstention, citations, and question history.

> Important: this repository implements an honest baseline, not a production-grade autonomous multi-agent AI system yet. The current retriever is transparent lexical overlap, the synthesizer is extractive, and adversarial checks are heuristic candidate flags. It does not claim that an NLI model, embeddings, LangGraph, OCR, authentication, RBAC, or LLM generation is implemented. The resolution engine abstains on detected candidate conflicts because document authority/version metadata is not yet captured.

## Features
- Upload PDF, DOCX and TXT files (20 MB default limit).
- Extract text and preserve PDF page numbers.
- Chunk text with configurable overlap.
- Search chunks using a transparent lexical baseline.
- Return source snippets and traceable document/page/chunk references.
- Run heuristic adversarial checks and report possible negation conflicts.
- Abstain rather than automatically select a winning source when a conflict is flagged.
- Delete documents and their chunks; review recent question history.
- Swagger API documentation at `/docs`.

## Requirements
- Python 3.11+
- Node.js 20+

## Run locally

### 1. Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```
Backend health: http://localhost:8000/health  
API docs: http://localhost:8000/docs

### 2. Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173. Set `VITE_API_URL` if the backend is hosted elsewhere (base URL should end in `/api`).

## API
- `POST /api/documents/upload` — multipart upload (`file`)
- `GET /api/documents` — list uploaded documents
- `DELETE /api/documents/{id}` — delete document and chunks
- `POST /api/query` — JSON body `{ "question": "..." }`
- `GET /api/history` — recent questions

## Deploy

### Backend (Render / Railway / any Python host)
- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Configure `CORS_ORIGINS` to your deployed frontend origin.
- Configure a persistent disk for SQLite database and uploaded files, or change `DATABASE_URL` to managed PostgreSQL and `UPLOAD_DIR` to persistent object storage. Ephemeral filesystems can lose uploads and the SQLite DB on redeploy.

### Frontend (Vercel / Netlify)
- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Environment variable: `VITE_API_URL=https://YOUR-BACKEND-DOMAIN/api`

Do not commit `.env`, API keys, uploaded private documents, or database files.

## GitHub upload
```bash
git init
git add .
git commit -m "Initial TruthGuard MVP"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/truthguard.git
git push -u origin main
```

## Tests
```bash
cd backend
pip install pytest
PYTHONPATH=. pytest -q
```

## Known limitations / next engineering phases
1. Add real BM25 + dense embeddings + vector index and evaluate retrieval recall.
2. Add an LLM provider adapter with structured output, claim extraction, and citation validation. Never pass document instructions as system instructions.
3. Add NLI model inference as a signal, not as an authoritative conflict verdict.
4. Capture issuer, authority level, jurisdiction, scope, publication/effective dates, version, supersedes, and exception metadata; implement a documented precedence policy.
5. Add OCR for scanned PDFs.
6. Add authentication, server-side RBAC, tenant isolation, rate limits, audit controls, malware scanning, and secure storage before handling sensitive documents.
7. Add LangGraph orchestration with bounded retries and human-review paths.
8. Build a labeled evaluation set and compare this baseline against upgraded RAG using answer correctness, citation support, conflict precision/recall, false positives, abstention quality, latency, and cost.

## Security note
This is a development MVP, not a hardened production system. Do not upload confidential, regulated, or sensitive documents until authentication, authorization, retention, encryption, and deployment controls are implemented.
