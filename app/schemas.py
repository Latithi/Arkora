from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class VaultCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=500)


class VaultRead(VaultCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectCreate(BaseModel):
    vault_id: int
    name: str = Field(min_length=2, max_length=140)
    status: str = Field(default="planning", max_length=50)
    category: str | None = Field(default=None, max_length=80)


class ProjectRead(BaseModel):
    id: int
    vault_id: int
    name: str
    slug: str
    status: str
    category: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TemplateCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    schema: dict[str, Any] = Field(default_factory=dict)


class TemplateRead(TemplateCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ContentItemCreate(BaseModel):
    project_id: int
    template_id: int
    title: str = Field(min_length=2, max_length=180)
    body: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContentItemRead(BaseModel):
    id: int
    project_id: int
    template_id: int
    title: str
    body: str
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SearchHit(BaseModel):
    item_id: int
    score: float
    title: str
    project_id: int
    snippet: str


class SearchResponse(BaseModel):
    query: str
    total: int
    hits: list[SearchHit]
