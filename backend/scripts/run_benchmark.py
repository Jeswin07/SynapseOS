"""Runs the Knowledge Retrieval benchmark."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from src.ml.knowledge.evaluation.benchmark_loader import (
    BenchmarkLoader,
)
from src.ml.knowledge.evaluation.evaluator import (
    KnowledgeEvaluator,
)

# ---------------------------------------------------------
# Benchmark Configuration
# ---------------------------------------------------------

PIPELINE_NAME = "Hybrid + CrossEncoder"

BENCHMARK_VERSION = "v1"

COLLECTION_NAME = "enterprise_docs_v5"

DOCUMENT_COUNT = 3

BENCHMARK_DIR = Path(
    "datasets/knowledge/benchmark/v1",
)

OUTPUT_DIR = Path(
    "artifacts/evaluation",
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

BENCHMARK_FILES = [
    "dataset.json",
    "legal.json",
    "industry.json",
    "cross_document.json",
]


def main() -> None:
    """
    Execute the complete retrieval benchmark.
    """

    loader = BenchmarkLoader()

    evaluator = KnowledgeEvaluator()

    overall_results = []

    precision_scores = []

    recall_scores = []

    hit_rates = []

    mrr_scores = []

    similarities = []

    latencies = []

    for benchmark in BENCHMARK_FILES:

        benchmark_path = BENCHMARK_DIR / benchmark

        print(f"\nRunning {benchmark}")

        cases = loader.load(benchmark_path)

        for case in cases:

            result = evaluator.evaluate(case)

            overall_results.append(
                result.model_dump(),
            )

            precision_scores.append(
                result.metrics.precision_at_k,
            )

            recall_scores.append(
                result.metrics.recall_at_k,
            )

            hit_rates.append(
                result.metrics.hit_rate,
            )

            mrr_scores.append(
                result.metrics.mrr,
            )

            similarities.append(
                result.metrics.average_similarity,
            )

            latencies.append(
                result.metrics.retrieval_latency_ms,
            )

            print(f"✓ {case.id}")

    report = {
        "benchmark_version": BENCHMARK_VERSION,
        "created_at": datetime.now().isoformat(),
        "pipeline": PIPELINE_NAME,
        "collection": COLLECTION_NAME,
        "documents": DOCUMENT_COUNT,
        "questions": len(overall_results),
        "precision_at_k": round(
            sum(precision_scores) / len(precision_scores),
            4,
        ),
        "recall_at_k": round(
            sum(recall_scores) / len(recall_scores),
            4,
        ),
        "hit_rate": round(
            sum(hit_rates) / len(hit_rates),
            4,
        ),
        "mrr": round(
            sum(mrr_scores) / len(mrr_scores),
            4,
        ),
        "average_similarity": round(
            sum(similarities) / len(similarities),
            4,
        ),
        "average_latency_ms": round(
            sum(latencies) / len(latencies),
            2,
        ),
        "results": overall_results,
    }

    output_file = (
        OUTPUT_DIR
        / "hybrid_reranker_v1.json"
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
        )

    print("\n===================================")
    print("Knowledge Benchmark Complete")
    print("===================================")
    print(f"Pipeline             : {PIPELINE_NAME}")
    print(f"Collection           : {COLLECTION_NAME}")
    print(f"Questions            : {len(overall_results)}")
    print(f"Precision@K          : {report['precision_at_k']}")
    print(f"Recall@K             : {report['recall_at_k']}")
    print(f"Hit Rate             : {report['hit_rate']}")
    print(f"MRR                  : {report['mrr']}")
    print(
        f"Average Similarity   : {report['average_similarity']}"
    )
    print(
        f"Average Latency (ms) : {report['average_latency_ms']}"
    )
    print(f"\nSaved to {output_file}")


if __name__ == "__main__":
    main()