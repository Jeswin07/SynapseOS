"""Schemas for Knowledge RAG evaluation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EvaluationCase(BaseModel):
    """
    One benchmark example.
    """

    question: str = Field(...)

    expected_documents: list[str] = Field(default_factory=list)

    expected_pages: list[str] = Field(default_factory=list)

    collection_name: str = Field(
        default="enterprise_docs_v2",
    )

    top_k: int = Field(
        default=5,
        ge=1,
    )


class EvaluationMetrics(BaseModel):
    """
    Retrieval metrics.
    """

    precision_at_k: float

    recall_at_k: float

    hit_rate: float

    mrr: float

    average_similarity: float

    highest_similarity: float

    retrieval_latency_ms: float


class EvaluationResult(BaseModel):
    """
    Complete evaluation output.
    """

    question: str

    retrieved_documents: list[str]

    retrieved_chunk_ids: list[str] = []

    retrieved_pages: list[str]

    metrics: EvaluationMetrics

    similarities: list[float] = []


class BenchmarkResult(BaseModel):
    """
    Result of multiple evaluation cases.
    """

    total_cases: int

    average_precision_at_k: float

    average_recall_at_k: float

    average_hit_rate: float

    average_mrr: float

    average_similarity: float

    average_latency_ms: float

    results: list[EvaluationResult]

class EvaluationCase(BaseModel):
    id: str
    difficulty: str
    category: str
    question: str
    expected_documents: list[str]
    collection_name: str = "enterprise_docs_v3"
    top_k: int = 5