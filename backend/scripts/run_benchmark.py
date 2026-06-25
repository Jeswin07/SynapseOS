"""Runs the complete retrieval benchmark."""

from __future__ import annotations

import json
from pathlib import Path

from src.ml.knowledge.evaluation.benchmark_loader import (
    BenchmarkLoader,
)
from src.ml.knowledge.evaluation.evaluator import (
    KnowledgeEvaluator,
)

BENCHMARK_DIR = Path(
    "datasets/knowledge/benchmark/v1"
)

OUTPUT_DIR = Path(
    "artifacts/evaluation"
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

    loader = BenchmarkLoader()
    evaluator = KnowledgeEvaluator()

    overall_results = []

    precision = []
    recall = []
    hit_rate = []
    mrr = []
    similarity = []
    latency = []

    for benchmark in BENCHMARK_FILES:

        benchmark_path = BENCHMARK_DIR / benchmark

        cases = loader.load(benchmark_path)

        print(f"\nRunning {benchmark}")

        for case in cases:

            result = evaluator.evaluate(case)

            overall_results.append(
                result.model_dump()
            )

            precision.append(
                result.metrics.precision_at_k
            )

            recall.append(
                result.metrics.recall_at_k
            )

            hit_rate.append(
                result.metrics.hit_rate
            )

            mrr.append(
                result.metrics.mrr
            )

            similarity.append(
                result.metrics.average_similarity
            )

            latency.append(
                result.metrics.retrieval_latency_ms
            )

            print(
                f"✓ {case.id}"
            )

    report = {
        "retriever": "dense",
        "collection": "enterprise_docs_v3",
        "documents": 3,
        "questions": len(overall_results),
        "precision_at_k": round(
            sum(precision) / len(precision),
            4,
        ),
        "recall_at_k": round(
            sum(recall) / len(recall),
            4,
        ),
        "hit_rate": round(
            sum(hit_rate) / len(hit_rate),
            4,
        ),
        "mrr": round(
            sum(mrr) / len(mrr),
            4,
        ),
        "average_similarity": round(
            sum(similarity) / len(similarity),
            4,
        ),
        "average_latency_ms": round(
            sum(latency) / len(latency),
            2,
        ),
        "results": overall_results,
    }

    output = OUTPUT_DIR / "basic_rag_v1.json"

    with output.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=4,
        )

    print("\n===================================")
    print("Benchmark Complete")
    print("===================================")
    print(f"Questions            : {len(overall_results)}")
    print(f"Precision@K          : {report['precision_at_k']}")
    print(f"Recall@K             : {report['recall_at_k']}")
    print(f"Hit Rate             : {report['hit_rate']}")
    print(f"MRR                  : {report['mrr']}")
    print(f"Average Similarity   : {report['average_similarity']}")
    print(f"Average Latency (ms) : {report['average_latency_ms']}")
    print(f"\nSaved to {output}")


if __name__ == "__main__":
    main()