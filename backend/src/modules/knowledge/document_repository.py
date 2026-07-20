"""Repository layer for KnowledgeDocument persistence."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from src.models.knowledge_document import (
    KnowledgeDocument,
    KnowledgeDocumentStatus,
)



class KnowledgeDocumentRepository:
    """
    Repository responsible for KnowledgeDocument persistence.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize repository.

        Args:
            db: SQLAlchemy session.
        """
        self.db = db

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def create_document(
        self,
        document: KnowledgeDocument,
    ) -> KnowledgeDocument:
        """
        Persist a knowledge document.
        """

        self.db.add(document)

        return document

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_document(
        self,
        document_id: uuid.UUID,
    ) -> KnowledgeDocument | None:
        """
        Retrieve document by ID.
        """

        return (
            self.db.query(KnowledgeDocument)
            .filter(
                KnowledgeDocument.id == document_id,
            )
            .first()
        )

    def get_document_by_tenant(
        self,
        *,
        document_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> KnowledgeDocument | None:
        """
        Retrieve document belonging to a tenant.
        """

        return (
            self.db.query(KnowledgeDocument)
            .filter(
                KnowledgeDocument.id == document_id,
                KnowledgeDocument.tenant_id == tenant_id,
            )
            .first()
        )

    def get_document_by_document_id(
        self,
        document_id: str,
    ) -> KnowledgeDocument | None:
        """
        Retrieve document using external document_id.
        """

        return (
            self.db.query(KnowledgeDocument)
            .filter(
                KnowledgeDocument.document_id == document_id,
            )
            .first()
        )

    def list_documents(
        self,
        tenant_id: uuid.UUID,
    ) -> list[KnowledgeDocument]:
        """
        Retrieve all knowledge documents for a tenant.
        """

        return (
            self.db.query(KnowledgeDocument)
            .filter(
                KnowledgeDocument.tenant_id == tenant_id,
            )
            .order_by(
                KnowledgeDocument.created_at.desc(),
            )
            .all()
        )

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update_status(
        self,
        *,
        document: KnowledgeDocument,
        status: KnowledgeDocumentStatus,
    ) -> KnowledgeDocument:
        """
        Update processing status.
        """

        document.status = status

        return document

    def update_chunk_count(
        self,
        *,
        document: KnowledgeDocument,
        chunk_count: int,
    ) -> KnowledgeDocument:
        """
        Update processed chunk count.
        """

        document.chunk_count = chunk_count

        return document

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete_document(
        self,
        document: KnowledgeDocument,
    ) -> None:
        """
        Delete document.
        """

        self.db.delete(document)

    # ------------------------------------------------------------------
    # Transaction
    # ------------------------------------------------------------------

    def commit(self) -> None:
        """Commit transaction."""

        self.db.commit()

    def rollback(self) -> None:
        """Rollback transaction."""

        self.db.rollback()

    def refresh(
        self,
        instance: object,
    ) -> None:
        """
        Refresh ORM instance.
        """

        self.db.refresh(instance)

    def flush(self) -> None:
        """
        Flush pending changes.
        """

        self.db.flush()