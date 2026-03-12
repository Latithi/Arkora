# Arkora

Arkora is a production-ready backend foundation for an advanced knowledge-management platform inspired by the concept in `concept.md`.

This implementation focuses on clean architecture, extensible domain modeling, and a practical API surface that supports:

- Local-first friendly data structures (vaults/workspaces)
- Project organization and taxonomy-ready metadata
- User-defined content templates (custom objects)
- Structured content items with flexible metadata
- Semantic-style search over knowledge content

## Stack

- **FastAPI** for the HTTP API
- **SQLAlchemy 2.x** for persistence
- **SQLite** by default (easy local setup)
- **Pytest** + FastAPI TestClient for integration testing

## Project Structure

```text
app/
  api/
    deps.py
    routes.py
  core/
    config.py
    database.py
  services/
    knowledge_service.py
  utils/
    text.py
  main.py
  models.py
  schemas.py
tests/
  test_api.py
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Environment Configuration

Optional `.env`:

```env
APP_NAME=Arkora API
APP_VERSION=0.1.0
DATABASE_URL=sqlite:///./arkora.db
```

## API Overview

Base path: `/api/v1`

- `GET /health`
- `POST /vaults`, `GET /vaults`
- `POST /projects`, `GET /projects?vault_id=...`
- `POST /templates`, `GET /templates`
- `POST /content`, `GET /content?project_id=...`
- `GET /search?q=...&limit=10`

## Design Notes

- **Service layer pattern** keeps route handlers thin and business logic centralized.
- **Pydantic schemas** enforce request/response validation and API contract clarity.
- **Unique constraints** protect data consistency (e.g., project slug uniqueness per vault).
- **Search utility** currently uses tokenized cosine similarity and can be swapped for true embedding/vector backends later without changing API contracts.

## Testing

```bash
pytest -q
```

The included test validates a realistic flow:

1. Create vault
2. Create template
3. Create project
4. Create content item
5. Retrieve result through semantic search

## Production Hardening Next Steps

- Add authN/authZ (JWT/SSO), RBAC, and audit logs
- Add migrations (Alembic)
- Add background indexing workers for large content/attachments
- Replace lexical search with embeddings + vector index
- Add observability (structured logging, tracing, metrics)
- Add CI pipeline and Docker deployment
