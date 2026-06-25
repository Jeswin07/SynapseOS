"""Benchmark runner for Knowledge RAG."""

from __future__ import annotations

from src.ml.knowledge.evaluation.evaluator import KnowledgeEvaluator
from src.ml.knowledge.evaluation.schemas import (
    BenchmarkResult,
    EvaluationCase,
    EvaluationResult,
)


class KnowledgeBenchmark:
    """
    Runs multiple evaluation cases and aggregates results.
    """

    def __init__(self) -> None:
        self.evaluator = KnowledgeEvaluator()

    def run(
        self,
        cases: list[EvaluationCase],
    ) -> BenchmarkResult:

        results: list[EvaluationResult] = []

        if not cases:
            return BenchmarkResult(
                total_cases=0,
                average_precision_at_k=0.0,
                average_recall_at_k=0.0,
                average_hit_rate=0.0,
                average_mrr=0.0,
                average_similarity=0.0,
                average_latency_ms=0.0,
                results=[],
            )

        precision_scores = []
        recall_scores = []
        hit_rates = []
        mrr_scores = []
        similarities = []
        latencies = []

        for case in cases:

            result = self.evaluator.evaluate(case)

            results.append(result)

            metrics = result.metrics

            precision_scores.append(metrics.precision_at_k)
            recall_scores.append(metrics.recall_at_k)
            hit_rates.append(metrics.hit_rate)
            mrr_scores.append(metrics.mrr)
            similarities.append(metrics.average_similarity)
            latencies.append(metrics.retrieval_latency_ms)

        return BenchmarkResult(
            total_cases=len(results),
            average_precision_at_k=round(
                sum(precision_scores) / len(precision_scores),
                4,
            ),
            average_recall_at_k=round(
                sum(recall_scores) / len(recall_scores),
                4,
            ),
            average_hit_rate=round(
                sum(hit_rates) / len(hit_rates),
                4,
            ),
            average_mrr=round(
                sum(mrr_scores) / len(mrr_scores),
                4,
            ),
            average_similarity=round(
                sum(similarities) / len(similarities),
                4,
            ),
            average_latency_ms=round(
                sum(latencies) / len(latencies),
                2,
            ),
            results=results,
        )