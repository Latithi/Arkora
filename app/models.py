from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Vault(Base, TimestampMixin):
    __tablename__ = "vaults"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    projects = relationship("Project", back_populates="vault", cascade="all, delete-orphan")


class Project(Base, TimestampMixin):
    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("vault_id", "slug", name="uq_project_vault_slug"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vault_id: Mapped[int] = mapped_column(ForeignKey("vaults.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(140), nullable=False)
    slug: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="planning")
    category: Mapped[str | None] = mapped_column(String(80), nullable=True)

    vault = relationship("Vault", back_populates="projects")
    content_items = relationship(
        "ContentItem", back_populates="project", cascade="all, delete-orphan"
    )


class ContentTemplate(Base, TimestampMixin):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    schema: Mapped[dict] = mapped_column(JSON, default=dict)

    content_items = relationship("ContentItem", back_populates="template")


class ContentItem(Base, TimestampMixin):
    __tablename__ = "content_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    template_id: Mapped[int] = mapped_column(ForeignKey("templates.id", ondelete="RESTRICT"))
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    body: Mapped[str] = mapped_column(Text, default="")
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    project = relationship("Project", back_populates="content_items")
    template = relationship("ContentTemplate", back_populates="content_items")
