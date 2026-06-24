"""Pydantic schemas for Knowledge Intelligence API contracts."""

from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    """Response returned after successfully ingesting a document."""
    message: str
    document_id: str
    chunks_processed: int
    collection_name: str


class SourceChunk(BaseModel):
    """Represents a retrieved context chunk used for generation."""
    text: str
    score: float
    page_label: str | None = None
    file_name: str | None = None


class QueryRequest(BaseModel):
    """Request payload for querying the enterprise knowledge base."""
    query: str = Field(..., min_length=3, description="The user's question.")
    collection_name: str = Field(
        default="enterprise_docs",
        description="The Qdrant collection to search against.",
    )
    top_k: int = Field(
        default=5,
        description="Number of context chunks to retrieve.",
    )


class QueryResponse(BaseModel):
    """The generated answer alongside its supporting sources."""
    answer: str
    sources: list[SourceChunk]
    processing_time_ms: float