"""Knowledge retrieval evaluator."""

from __future__ import annotations

from src.ml.knowledge.evaluation.metrics import (
    average_similarity,
    highest_similarity,
    hit_rate,
    mean_reciprocal_rank,
    precision_at_k,
    recall_at_k,
    retrieval_latency,
)
from src.ml.knowledge.evaluation.schemas import (
    EvaluationCase,
    EvaluationMetrics,
    EvaluationResult,
)
from src.core.config import settings
from src.ml.knowledge.hybrid_retriever import HybridRetriever
from src.ml.knowledge.reranker import CrossEncoderReranker


class KnowledgeEvaluator:
    """
    Evaluates retrieval quality using the production
    retrieval pipeline.

    Generation quality is not evaluated.
    """

    def __init__(self) -> None:
        self.retriever = HybridRetriever()
        self.reranker = CrossEncoderReranker()

    def evaluate(
        self,
        case: EvaluationCase,
    ) -> EvaluationResult:

        retrieval = self.retriever.retrieve(
            query=case.question,
            collection_name=case.collection_name,
            candidate_k=settings.rag_candidate_k,
        )

        retrieval.points = self.reranker.rerank(
            query=case.question,
            candidates=retrieval.points,
            top_k=case.top_k,
        )

        retrieved_documents: list[str] = []
        retrieved_chunk_ids: list[str] = []
        retrieved_pages: list[str] = []
        similarities: list[float] = []

        for point in retrieval.points:

            payload = point.payload or {}

            retrieved_documents.append(
                str(
                    payload.get(
                        "file_name",
                        "",
                    )
                )
            )

            retrieved_chunk_ids.append(
                str(
                    payload.get(
                        "chunk_id",
                        "",
                    )
                )
            )

            retrieved_pages.append(
                str(
                    payload.get(
                        "page_label",
                        "",
                    )
                )
            )

            similarities.append(
                float(point.score)
            )

        metrics = EvaluationMetrics(
            precision_at_k=precision_at_k(
                retrieved_documents,
                case.expected_documents,
            ),
            recall_at_k=recall_at_k(
                retrieved_documents,
                case.expected_documents,
            ),
            hit_rate=hit_rate(
                retrieved_documents,
                case.expected_documents,
            ),
            mrr=mean_reciprocal_rank(
                retrieved_documents,
                case.expected_documents,
            ),
            average_similarity=average_similarity(
                similarities,
            ),
            highest_similarity=highest_similarity(
                similarities,
            ),
            retrieval_latency_ms=retrieval_latency(
                retrieval.retrieval_time_ms,
            ),
        )

        return EvaluationResult(
            question=case.question,
            retrieved_documents=retrieved_documents,
            retrieved_chunk_ids=retrieved_chunk_ids,
            retrieved_pages=retrieved_pages,
            metrics=metrics,
            similarities=similarities,
        )