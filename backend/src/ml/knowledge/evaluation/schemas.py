"""Schemas for Knowledge RAG evaluation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EvaluationCase(BaseModel):
    """
    One benchmark evaluation case.
    """
    id: str
    difficulty: str
    category: str
    question: str
    expected_documents: list[str]
    expected_answer: str
    collection_name: str = "enterprise_docs_v5"
    top_k: int = 5
    expected_pages: list[str] = Field(
        default_factory=list,
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

    retrieved_chunk_ids: list[str] = Field(default_factory=list)

    retrieved_pages: list[str]

    metrics: EvaluationMetrics

    similarities: list[float] = Field(default_factory=list)


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

