"""Shared models for all retrieval engines."""

from __future__ import annotations

from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    """
    A single retrieved chunk returned by any retriever.
    """

    payload: dict

    score: float

    dense_score: float | None = None

    bm25_score: float | None = None

    rrf_score: float | None = None


class RetrievalResult(BaseModel):
    """
    Standard retrieval response shared by all retrievers.
    """

    points: list[RetrievedChunk]

    retrieval_time_ms: float

    average_similarity: float

    highest_similarity: float