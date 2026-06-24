"""Enterprise semantic retriever for the Knowledge module."""

from __future__ import annotations

import time
from dataclasses import dataclass

from qdrant_client.models import ScoredPoint

from src.ml.knowledge.embeddings import EmbeddingEngine
from src.modules.knowledge.repository import QdrantRepository


@dataclass(slots=True)
class RetrievalResult:
    """Container for retrieval results."""

    points: list[ScoredPoint]
    retrieval_time_ms: float


class Retriever:
    """Handles semantic retrieval from the vector database."""

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
        Retrieve the most relevant chunks.

        Steps
        -----
        1. Embed query
        2. Search Qdrant
        3. Return ranked chunks
        """

        start = time.perf_counter()

        query_vector = self.embedding_engine.generate_embeddings([query])[0]

        points = self.repository.search(
            collection_name=collection_name,
            query_vector=query_vector,
            top_k=top_k,
        )

        retrieval_time_ms = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

        return RetrievalResult(
            points=points,
            retrieval_time_ms=retrieval_time_ms,
        )