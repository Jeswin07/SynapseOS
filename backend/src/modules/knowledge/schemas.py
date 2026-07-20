"""Pydantic schemas for Knowledge Intelligence API contracts."""

from pydantic import BaseModel, Field

from src.core.config import settings
from uuid import UUID
from datetime import datetime
from src.models.knowledge_document import KnowledgeDocumentStatus

class DocumentUploadResponse(BaseModel):
    """Response returned after successfully ingesting a document."""

    message: str
    document_id: str
    chunks_processed: int
    collection_name: str


class SourceChunk(BaseModel):
    """Represents a retrieved context chunk."""

    text: str
    score: float
    file_name: str
    page_label: str
    page_number: int | None = None
    chunk_index: int | None = None
    file_type: str | None = None
    chunk_length: int | None = None
    chunk_id: str | None = None


class QueryMetrics(BaseModel):
    """Execution metrics for a query."""

    retrieval_time_ms: float
    generation_time_ms: float
    total_time_ms: float
    chunks_retrieved: int
    average_similarity: float
    highest_similarity: float


class QueryRequest(BaseModel):
    """Request payload for querying the knowledge base."""

    query: str = Field(
        ...,
        min_length=3,
        description="The user's question.",
    )

    collection_name: str = Field(
        default=settings.knowledge_collection,
        description="The Qdrant collection to search.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of chunks to retrieve.",
    )


class QueryResponse(BaseModel):
    """Generated answer along with supporting evidence."""

    answer: str

    sources: list[SourceChunk]

    metrics: QueryMetrics



class KnowledgeDocumentResponse(BaseModel):
    """Knowledge document metadata."""

    id: UUID
    tenant_id: UUID
    uploaded_by: UUID

    document_id: str
    filename: str
    file_type: str

    chunk_count: int

    status: KnowledgeDocumentStatus

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class KnowledgeDocumentListResponse(BaseModel):
    """List of uploaded documents."""

    documents: list[KnowledgeDocumentResponse]


class DeleteDocumentResponse(BaseModel):
    """Delete response."""

    message: str