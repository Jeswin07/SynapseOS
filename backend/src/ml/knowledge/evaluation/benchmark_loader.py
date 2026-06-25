"""Loads benchmark datasets for retrieval evaluation."""

from __future__ import annotations

import json
from pathlib import Path

from src.ml.knowledge.evaluation.schemas import EvaluationCase


class BenchmarkLoader:
    """Loads benchmark JSON files into EvaluationCase objects."""

    def load(
        self,
        benchmark_path: str | Path,
    ) -> list[EvaluationCase]:

        path = Path(benchmark_path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        return [
            EvaluationCase(**item)
            for item in data
        ]