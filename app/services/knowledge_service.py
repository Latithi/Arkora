from collections import Counter

from fastapi import HTTPException, status
from slugify import slugify
from sqlalchemy.orm import Session

from app.models import ContentItem, ContentTemplate, Project, Vault
from app.schemas import (
    ContentItemCreate,
    ProjectCreate,
    TemplateCreate,
    VaultCreate,
)
from app.utils.text import cosine_similarity, tokenize


class KnowledgeService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_vault(self, payload: VaultCreate) -> Vault:
        existing = self.db.query(Vault).filter(Vault.name == payload.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vault with this name already exists.",
            )
        vault = Vault(name=payload.name, description=payload.description)
        self.db.add(vault)
        self.db.commit()
        self.db.refresh(vault)
        return vault

    def list_vaults(self) -> list[Vault]:
        return self.db.query(Vault).order_by(Vault.name.asc()).all()

    def create_project(self, payload: ProjectCreate) -> Project:
        vault = self.db.get(Vault, payload.vault_id)
        if not vault:
            raise HTTPException(status_code=404, detail="Vault not found.")

        slug = slugify(payload.name)
        exists = (
            self.db.query(Project)
            .filter(Project.vault_id == payload.vault_id, Project.slug == slug)
            .first()
        )
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Project slug already exists in this vault.",
            )

        project = Project(
            vault_id=payload.vault_id,
            name=payload.name,
            slug=slug,
            status=payload.status,
            category=payload.category,
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def list_projects(self, vault_id: int | None = None) -> list[Project]:
        query = self.db.query(Project)
        if vault_id is not None:
            query = query.filter(Project.vault_id == vault_id)
        return query.order_by(Project.created_at.desc()).all()

    def create_template(self, payload: TemplateCreate) -> ContentTemplate:
        exists = self.db.query(ContentTemplate).filter_by(name=payload.name).first()
        if exists:
            raise HTTPException(status_code=409, detail="Template name already exists.")

        template = ContentTemplate(
            name=payload.name,
            description=payload.description,
            schema=payload.schema,
        )
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def list_templates(self) -> list[ContentTemplate]:
        return self.db.query(ContentTemplate).order_by(ContentTemplate.name.asc()).all()

    def create_content_item(self, payload: ContentItemCreate) -> ContentItem:
        project = self.db.get(Project, payload.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found.")

        template = self.db.get(ContentTemplate, payload.template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found.")

        content_item = ContentItem(
            project_id=payload.project_id,
            template_id=payload.template_id,
            title=payload.title,
            body=payload.body,
            metadata=payload.metadata,
        )
        self.db.add(content_item)
        self.db.commit()
        self.db.refresh(content_item)
        return content_item

    def list_content_items(self, project_id: int | None = None) -> list[ContentItem]:
        query = self.db.query(ContentItem)
        if project_id is not None:
            query = query.filter(ContentItem.project_id == project_id)
        return query.order_by(ContentItem.updated_at.desc()).all()

    def semantic_search(self, query: str, limit: int = 10) -> list[dict]:
        if not query.strip():
            return []

        query_vector = Counter(tokenize(query))
        rows = self.db.query(ContentItem).all()
        scored_hits: list[dict] = []

        for row in rows:
            full_text = f"{row.title}\n{row.body}".strip()
            similarity = cosine_similarity(query_vector, Counter(tokenize(full_text)))
            if similarity <= 0:
                continue
            snippet = row.body[:180] + ("..." if len(row.body) > 180 else "")
            scored_hits.append(
                {
                    "item_id": row.id,
                    "project_id": row.project_id,
                    "title": row.title,
                    "score": round(similarity, 4),
                    "snippet": snippet,
                }
            )

        scored_hits.sort(key=lambda item: item["score"], reverse=True)
        return scored_hits[:limit]
