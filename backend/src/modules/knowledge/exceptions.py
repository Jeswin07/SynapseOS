"""Knowledge module exceptions."""

from __future__ import annotations


class KnowledgeException(Exception):
    """Base exception for the Knowledge module."""


class KnowledgeDocumentNotFoundException(KnowledgeException):
    """Raised when a knowledge document cannot be found."""

    def __init__(self, document_id: str) -> None:
        super().__init__(
            f"Knowledge document '{document_id}' not found."
        )


class KnowledgeAccessDeniedException(KnowledgeException):
    """Raised when a tenant attempts to access another tenant's document."""

    def __init__(self) -> None:
        super().__init__(
            "You do not have permission to access this document."
        )


class KnowledgeUploadException(KnowledgeException):
    """Raised when document upload fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class KnowledgeQueryException(KnowledgeException):
    """Raised when querying the knowledge base fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class KnowledgeDeleteException(KnowledgeException):
    """Raised when deleting a knowledge document fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)