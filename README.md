# Arkora

Arkora now includes:

- A **FastAPI backend** implementing the concept's core domain (vaults, projects, templates, content, search)
- A **Next.js frontend console** for viewing platform stats and running semantic search

## Monorepo Structure

```text
app/                      # Backend source (FastAPI)
  api/
  core/
  services/
  utils/
  main.py
  models.py
  schemas.py
frontend/                 # Frontend source (Next.js + React)
  src/
    app/
    components/
    lib/
requirements.txt          # Backend dependencies
tests/                    # Backend tests
concept.md                # Product concept
```

---

## Backend (FastAPI)

### Features

- Layered architecture (`core`, `api`, `services`, `utils`)
- SQLAlchemy models for:
  - `Vault`
  - `Project`
  - `ContentTemplate`
  - `ContentItem`
- Validated Pydantic request/response schemas
- REST API routes for create/list flows
- Semantic-style search using tokenization + cosine similarity

### Backend Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Backend Environment Configuration

Optional `.env`:

```env
APP_NAME=Arkora API
APP_VERSION=0.1.0
DATABASE_URL=sqlite:///./arkora.db
```

### Backend API Overview

Base path: `/api/v1`

- `GET /health`
- `POST /vaults`, `GET /vaults`
- `POST /projects`, `GET /projects?vault_id=...`
- `POST /templates`, `GET /templates`
- `POST /content`, `GET /content?project_id=...`
- `GET /search?q=...&limit=10`

---

## Frontend (Next.js)

### Features

- Clean dashboard for Arkora platform visibility
- Live API-backed counters for vaults, projects, and templates
- Semantic search panel connected to backend `/search`
- Responsive, production-style CSS without framework lock-in
- Error and loading states for resilient UX

### Frontend Quick Start

```bash
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:3000`.

### Frontend Environment Configuration

Set the backend API base URL with:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

If omitted, the frontend defaults to `http://127.0.0.1:8000/api/v1`.

---

## Testing

Backend test:

```bash
pytest -q
```

---

## Production Hardening Roadmap

- Add authN/authZ (JWT/SSO), RBAC, and audit logs
- Add migrations (Alembic)
- Replace lexical search with embeddings + vector index
- Add background indexing workers for large content/attachments
- Add observability (structured logging, tracing, metrics)
- Add Docker + CI pipelines for backend/frontend
