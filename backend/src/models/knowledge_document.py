import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.models.knowledge_enums import KnowledgeDocumentStatus
from enum import Enum

class KnowledgeDocument(Base):
    """
    Metadata for uploaded knowledge documents.

    Actual document chunks live in Qdrant.
    Graph entities live in Neo4j.

    This table stores searchable metadata and ownership.
    """

    __tablename__ = "knowledge_documents"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    document_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    chunk_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[KnowledgeDocumentStatus] = mapped_column(
        SQLEnum(KnowledgeDocumentStatus),
        default=KnowledgeDocumentStatus.PROCESSING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )