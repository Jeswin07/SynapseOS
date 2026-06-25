"""Cross Encoder reranker for Hybrid RAG."""

from __future__ import annotations

from sentence_transformers import CrossEncoder

from src.ml.knowledge.retrieval_models import RetrievedChunk


class CrossEncoderReranker:
    """
    Re-ranks retrieved candidates using a Cross Encoder.

    Input:
        Query
        +
        Candidate Chunks

    Output:
        Better ranked chunks
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
    ) -> None:

        self.model = CrossEncoder(
            model_name,
            trust_remote_code=True,
        )

    def rerank(
        self,
        query: str,
        candidates: list[RetrievedChunk],
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Returns the best candidates after reranking.
        """

        if not candidates:
            return []

        sentence_pairs = [
            (
                query,
                chunk.payload["text"],
            )
            for chunk in candidates
        ]

        scores = self.model.predict(
            sentence_pairs
        )

        ranked = sorted(
            zip(
                candidates,
                scores,
            ),
            key=lambda x: x[1],
            reverse=True,
        )

        results: list[RetrievedChunk] = []

        for chunk, score in ranked[:top_k]:

            chunk.score = float(score)

            results.append(chunk)

        return results