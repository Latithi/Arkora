from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import create_app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)
app = create_app()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_end_to_end_knowledge_flow() -> None:
    vault = client.post("/api/v1/vaults", json={"name": "Team Vault"})
    assert vault.status_code == 201
    vault_id = vault.json()["id"]

    template = client.post(
        "/api/v1/templates",
        json={
            "name": "API Call",
            "description": "Template for API knowledge",
            "schema": {"method": "string", "endpoint": "string"},
        },
    )
    assert template.status_code == 201
    template_id = template.json()["id"]

    project = client.post(
        "/api/v1/projects",
        json={"vault_id": vault_id, "name": "Auth Service", "status": "active"},
    )
    assert project.status_code == 201
    project_id = project.json()["id"]

    content = client.post(
        "/api/v1/content",
        json={
            "project_id": project_id,
            "template_id": template_id,
            "title": "Token endpoint",
            "body": "Use OAuth2 client credentials against /oauth/token endpoint.",
            "metadata": {"method": "POST", "endpoint": "/oauth/token"},
        },
    )
    assert content.status_code == 201

    response = client.get("/api/v1/search", params={"q": "oauth token endpoint"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["hits"][0]["title"] == "Token endpoint"
