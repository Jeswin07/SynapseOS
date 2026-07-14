"""Builds a RAGAS evaluation dataset from benchmark questions."""

from __future__ import annotations

from pathlib import Path

from datasets import Dataset

from api_client import KnowledgeApiClient
from config import BENCHMARK_DIR

from src.ml.knowledge.evaluation.benchmark_loader import (
    BenchmarkLoader,
)


BENCHMARK_FILES = [
    "dataset.json",
    "legal.json",
    "industry.json",
    "cross_document.json",
]


class DatasetBuilder:
    """
    Builds a HuggingFace Dataset compatible with RAGAS.
    """

    def __init__(self) -> None:

        self.loader = BenchmarkLoader()
        self.client = KnowledgeApiClient()

    def build(self) -> Dataset:

        samples: list[dict] = []

        for benchmark in BENCHMARK_FILES:

            benchmark_path = Path(BENCHMARK_DIR) / benchmark

            cases = self.loader.load(
                benchmark_path,
            )

            print(f"\nLoading {benchmark}")

            for case in cases:

                response = self.client.query(
                    question=case.question,
                )

                contexts = [
                    source["text"]
                    for source in response["sources"]
                ]

                samples.append(
                    {
                        "id": case.id,
                        "question": case.question,
                        "answer": response["answer"],
                        "contexts": contexts,
                        "ground_truth": case.expected_answer,
                        "reference_contexts": case.expected_documents,
                        "metadata": {
                            "difficulty": case.difficulty,
                            "category": case.category,
                        },
                    }
                )

                print(f"✓ {case.id}")

        return Dataset.from_list(samples)