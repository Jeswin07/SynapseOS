"""Enterprise semantic retriever for the Knowledge module."""

from __future__ import annotations

import time

from src.ml.knowledge.embeddings import EmbeddingEngine
from src.ml.knowledge.retrieval_models import (
    RetrievedChunk,
    RetrievalResult,
)
from src.modules.knowledge.repository import QdrantRepository


class Retriever:
    """Dense semantic retriever backed by Qdrant."""

    def __init__(self) -> None:
        self.embedding_engine = EmbeddingEngine()
        self.repository = QdrantRepository()

    def retrieve(
        self,
        query: str,
        collection_name: str,
        top_k: int = 5,
    ) -> RetrievalResult:
        """
        Retrieve the most relevant chunks using dense vector search.
        """

        start = time.perf_counter()

        query_vector = self.embedding_engine.generate_embeddings(
            [query]
        )[0]

        points = self.repository.search(
            collection_name=collection_name,
            query_vector=query_vector,
            top_k=top_k,
        )

        retrieval_time_ms = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

        retrieved_points: list[RetrievedChunk] = []

        similarities: list[float] = []

        for point in points:

            score = float(point.score)

            similarities.append(score)

            retrieved_points.append(
                RetrievedChunk(
                    payload=point.payload or {},
                    score=score,
                    dense_score=score,
                )
            )

        average_similarity = (
            round(
                sum(similarities) / len(similarities),
                4,
            )
            if similarities
            else 0.0
        )

        highest_similarity = (
            max(similarities)
            if similarities
            else 0.0
        )

        return RetrievalResult(
            points=retrieved_points,
            retrieval_time_ms=retrieval_time_ms,
            average_similarity=average_similarity,
            highest_similarity=highest_similarity,
        )