"""Cross Encoder reranker for Hybrid RAG."""

from __future__ import annotations

from sentence_transformers import CrossEncoder

from src.core.config import settings
from src.ml.knowledge.retrieval_models import RetrievedChunk
from src.shared.logging import logger


class CrossEncoderReranker:
    """
    Re-ranks retrieved candidates using a Cross Encoder.

    The CrossEncoder model is loaded only once and shared
    across all instances.
    """

    _model: CrossEncoder | None = None

    def __init__(
        self,
        model_name: str = settings.reranker_model,
    ) -> None:

        if CrossEncoderReranker._model is None:

            logger.info(
                "Loading reranker model '%s'.",
                model_name,
            )

            try:

                CrossEncoderReranker._model = CrossEncoder(
                    model_name,
                    trust_remote_code=True,
                    local_files_only=True,
                )

                logger.info(
                    "Loaded reranker model from local cache.",
                )

            except Exception:

                logger.warning(
                    "Local reranker model not found. Downloading from Hugging Face..."
                )

                CrossEncoderReranker._model = CrossEncoder(
                    model_name,
                    trust_remote_code=True,
                )

                logger.info(
                    "Downloaded reranker model successfully.",
                )

        self.model = CrossEncoderReranker._model

    def rerank(
        self,
        query: str,
        candidates: list[RetrievedChunk],
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Re-rank retrieved candidates.

        CrossEncoder scores are used only for ranking.
        The original dense similarity score is preserved
        for API responses.
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

        reranker_scores = self.model.predict(
            sentence_pairs,
        )

        ranked = sorted(
            zip(
                candidates,
                reranker_scores,
            ),
            key=lambda x: x[1],
            reverse=True,
        )

        results: list[
            RetrievedChunk
        ] = []

        for chunk, reranker_score in ranked[:top_k]:

            chunk.reranker_score = float(
                reranker_score,
            )

            if chunk.dense_score is not None:

                chunk.score = chunk.dense_score

            elif chunk.score is None:

                chunk.score = 0.0

            results.append(
                chunk,
            )

        return results