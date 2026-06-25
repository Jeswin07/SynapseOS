"""Hybrid retriever combining Dense Search and BM25."""

from __future__ import annotations

import time
from collections import defaultdict

from src.ml.knowledge.bm25 import BM25Retriever
from src.ml.knowledge.retrieval_models import (
    RetrievedChunk,
    RetrievalResult,
)
from src.ml.knowledge.retriever import Retriever
from src.modules.knowledge.repository import QdrantRepository


class HybridRetriever:
    """
    Hybrid Retriever using:

    - Dense Retrieval (Qdrant)
    - BM25
    - Reciprocal Rank Fusion (RRF)
    """

    def __init__(self) -> None:

        self.dense = Retriever()
        self.repository = QdrantRepository()

        self.bm25 = BM25Retriever()

        self._indexed_collection: str | None = None

    def build_bm25(
        self,
        collection_name: str,
    ) -> None:
        """
        Build a BM25 index from all chunks.
        """

        records = self.repository.get_all_chunks(
            collection_name,
        )

        self.bm25.build(records)

        self._indexed_collection = collection_name

    def retrieve(
        self,
        query: str,
        collection_name: str,
        candidate_k: int = 20,
    ) -> RetrievalResult:

        start = time.perf_counter()

        if (
            not self.bm25.ready
            or self._indexed_collection != collection_name
        ):
            self.build_bm25(collection_name)

        dense = self.dense.retrieve(
            query=query,
            collection_name=collection_name,
            top_k=candidate_k,
        )

        bm25 = self.bm25.search(
            query=query,
            top_k=candidate_k,
        )

        points = self._rrf(
            dense.points,
            bm25,
        )

        points = points[:candidate_k]

        retrieval_time_ms = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

        similarities = [
            point.score
            for point in points
        ]

        return RetrievalResult(
            points=points,
            retrieval_time_ms=retrieval_time_ms,
            average_similarity=(
                round(
                    sum(similarities) / len(similarities),
                    4,
                )
                if similarities
                else 0.0
            ),
            highest_similarity=(
                max(similarities)
                if similarities
                else 0.0
            ),
        )

    @staticmethod
    def _rrf(
        dense_results: list[RetrievedChunk],
        bm25_results: list[dict],
        k: int = 60,
    ) -> list[RetrievedChunk]:

        scores = defaultdict(float)

        chunks: dict[str, RetrievedChunk] = {}

        # Dense
        for rank, point in enumerate(dense_results):

            payload = point.payload

            chunk_id = payload["chunk_id"]

            rrf_score = 1 / (k + rank + 1)

            scores[chunk_id] += rrf_score

            chunks[chunk_id] = RetrievedChunk(
                payload=payload,
                score=rrf_score,
                dense_score=point.score,
                rrf_score=rrf_score,
            )

        # BM25
        for rank, doc in enumerate(bm25_results):

            payload = doc["payload"]

            chunk_id = payload["chunk_id"]

            rrf_score = 1 / (k + rank + 1)

            scores[chunk_id] += rrf_score

            if chunk_id not in chunks:

                chunks[chunk_id] = RetrievedChunk(
                    payload=payload,
                    score=rrf_score,
                    bm25_score=doc["bm25_score"],
                    rrf_score=rrf_score,
                )
            else:

                chunks[chunk_id].bm25_score = doc["bm25_score"]

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        results: list[RetrievedChunk] = []

        for chunk_id, rrf_score in ranked:

            chunk = chunks[chunk_id]

            chunk.rrf_score = rrf_score

            if chunk.dense_score is not None:
                chunk.score = chunk.dense_score
            else:
                chunk.score = 0.0

            results.append(chunk)

        return results
    
    def invalidate_index(self) -> None:
        """
        Force BM25 to rebuild on the next query.
        """

        self.bm25 = BM25Retriever()

        self._indexed_collection = None