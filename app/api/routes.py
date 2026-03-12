from fastapi import APIRouter, Depends, Query

from app.api.deps import get_knowledge_service
from app.schemas import (
    ContentItemCreate,
    ContentItemRead,
    ProjectCreate,
    ProjectRead,
    SearchResponse,
    TemplateCreate,
    TemplateRead,
    VaultCreate,
    VaultRead,
)
from app.services.knowledge_service import KnowledgeService

router = APIRouter(prefix="/api/v1")


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/vaults", response_model=VaultRead, status_code=201)
def create_vault(
    payload: VaultCreate, service: KnowledgeService = Depends(get_knowledge_service)
) -> VaultRead:
    return service.create_vault(payload)


@router.get("/vaults", response_model=list[VaultRead])
def list_vaults(service: KnowledgeService = Depends(get_knowledge_service)) -> list[VaultRead]:
    return service.list_vaults()


@router.post("/projects", response_model=ProjectRead, status_code=201)
def create_project(
    payload: ProjectCreate, service: KnowledgeService = Depends(get_knowledge_service)
) -> ProjectRead:
    return service.create_project(payload)


@router.get("/projects", response_model=list[ProjectRead])
def list_projects(
    vault_id: int | None = None,
    service: KnowledgeService = Depends(get_knowledge_service),
) -> list[ProjectRead]:
    return service.list_projects(vault_id=vault_id)


@router.post("/templates", response_model=TemplateRead, status_code=201)
def create_template(
    payload: TemplateCreate, service: KnowledgeService = Depends(get_knowledge_service)
) -> TemplateRead:
    return service.create_template(payload)


@router.get("/templates", response_model=list[TemplateRead])
def list_templates(
    service: KnowledgeService = Depends(get_knowledge_service),
) -> list[TemplateRead]:
    return service.list_templates()


@router.post("/content", response_model=ContentItemRead, status_code=201)
def create_content(
    payload: ContentItemCreate, service: KnowledgeService = Depends(get_knowledge_service)
) -> ContentItemRead:
    return service.create_content_item(payload)


@router.get("/content", response_model=list[ContentItemRead])
def list_content(
    project_id: int | None = None,
    service: KnowledgeService = Depends(get_knowledge_service),
) -> list[ContentItemRead]:
    return service.list_content_items(project_id=project_id)


@router.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(min_length=1, description="Natural language query"),
    limit: int = Query(default=10, ge=1, le=50),
    service: KnowledgeService = Depends(get_knowledge_service),
) -> SearchResponse:
    hits = service.semantic_search(query=q, limit=limit)
    return SearchResponse(query=q, total=len(hits), hits=hits)
