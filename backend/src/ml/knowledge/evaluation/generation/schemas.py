"""Schemas for generation evaluation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class GenerationEvaluationCase(BaseModel):
    """
    One generation benchmark case.
    """

    id: str

    difficulty: str

    category: str

    question: str

    expected_answer: str

    expected_documents: list[str] = Field(
        default_factory=list,
    )

    collection_name: str = "enterprise_docs_v5"

    top_k: int = 5


class GenerationMetrics(BaseModel):
    """
    Generation evaluation metrics.
    """

    faithfulness: float

    answer_relevancy: float

    context_recall: float

    semantic_similarity: float


class GenerationEvaluationResult(BaseModel):
    """
    Complete generation evaluation result.
    """

    question: str

    generated_answer: str

    expected_answer: str

    metrics: GenerationMetrics


class GenerationBenchmarkResult(BaseModel):
    """
    Overall benchmark report.
    """

    total_cases: int

    average_faithfulness: float

    average_answer_relevancy: float

    average_context_recall: float

    average_semantic_similarity: float

    results: list[GenerationEvaluationResult]