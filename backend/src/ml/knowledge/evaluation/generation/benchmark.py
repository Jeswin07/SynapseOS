"""Runs generation benchmark evaluation."""

from __future__ import annotations

import json
import time
from pathlib import Path

from src.ml.knowledge.evaluation.benchmark_loader import (
    BenchmarkLoader,
)
from src.ml.knowledge.generation_evaluator import (
    GenerationEvaluator,
)
from src.modules.knowledge.schemas import QueryRequest
from src.modules.knowledge.service import (
    KnowledgeService,
)

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

    loader = BenchmarkLoader()

    evaluator = GenerationEvaluator()

    service = KnowledgeService()

    results = []

    faithfulness_scores = []
    correctness_scores = []
    relevancy_scores = []
    semantic_scores = []
    recall_scores = []

    for benchmark in BENCHMARK_FILES:

        benchmark_path = BENCHMARK_DIR / benchmark

        cases = loader.load(
            benchmark_path,
        )

        print(f"\nRunning {benchmark}")

        for case in cases:

            request = QueryRequest(
                query=case.question,
                collection_name=case.collection_name,
                top_k=case.top_k,
            )

            response = service.query_knowledge_base(
                request,
            )

            metrics = evaluator.evaluate(
                question=case.question,
                generated_answer=response.answer,
                reference_answer=case.expected_answer,
                contexts=[
                    source.text
                    for source in response.sources
                ],
            )

            results.append(
                {
                    "id": case.id,
                    "question": case.question,
                    "metrics": metrics.model_dump(),
                }
            )

            faithfulness_scores.append(
                metrics.faithfulness,
            )

            correctness_scores.append(
                metrics.answer_correctness,
            )

            relevancy_scores.append(
                metrics.answer_relevancy,
            )

            semantic_scores.append(
                metrics.semantic_similarity,
            )

            recall_scores.append(
                metrics.context_recall,
            )

            print(f"✓ {case.id}")

            time.sleep(2)

    report = {
        "pipeline": "Generation Evaluation",
        "questions": len(results),
        "faithfulness": round(
            sum(faithfulness_scores)
            / len(faithfulness_scores),
            4,
        ),
        "answer_correctness": round(
            sum(correctness_scores)
            / len(correctness_scores),
            4,
        ),
        "answer_relevancy": round(
            sum(relevancy_scores)
            / len(relevancy_scores),
            4,
        ),
        "semantic_similarity": round(
            sum(semantic_scores)
            / len(semantic_scores),
            4,
        ),
        "context_recall": round(
            sum(recall_scores)
            / len(recall_scores),
            4,
        ),
        "results": results,
    }

    output = OUTPUT_DIR / "generation_evaluation.json"

    with output.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
        )

    save_markdown_report(
        report,
        OUTPUT_DIR,
    )
    print("\n===================================")
    print("Generation Evaluation Complete")
    print("===================================")
    print(
        f"Faithfulness         : {report['faithfulness']}"
    )
    print(
        f"Answer Correctness   : {report['answer_correctness']}"
    )
    print(
        f"Answer Relevancy     : {report['answer_relevancy']}"
    )
    print(
        f"Semantic Similarity  : {report['semantic_similarity']}"
    )
    print(
        f"Context Recall       : {report['context_recall']}"
    )
    print(f"\nSaved to {output}")

def save_markdown_report(
    report: dict,
    output_dir: Path,
) -> None:
    """
    Save a human-readable Markdown report.
    """

    markdown = f"""# SynapseOS Generation Evaluation Report

## Overall Metrics

| Metric | Score |
|--------|-------:|
| Faithfulness | {report["faithfulness"]:.4f} |
| Answer Correctness | {report["answer_correctness"]:.4f} |
| Answer Relevancy | {report["answer_relevancy"]:.4f} |
| Semantic Similarity | {report["semantic_similarity"]:.4f} |
| Context Recall | {report["context_recall"]:.4f} |

---

Questions Evaluated: **{report["questions"]}**

Pipeline: **{report["pipeline"]}**
"""

    output = output_dir / "generation_evaluation.md"

    output.write_text(
        markdown,
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()