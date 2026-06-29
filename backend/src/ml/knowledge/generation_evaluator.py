"""Generation evaluation metrics."""

from __future__ import annotations

from pydantic import BaseModel

from src.ml.knowledge.llm_judge import LLMJudge
from src.ml.knowledge.semantic_similarity import (
    SemanticSimilarity,
)


class GenerationMetrics(BaseModel):
    """
    Generation quality metrics.
    """

    faithfulness: float

    answer_correctness: float

    answer_relevancy: float

    semantic_similarity: float

    context_recall: float

    faithfulness_reason: str

    correctness_reason: str

    relevancy_reason: str

    recall_reason: str


class GenerationEvaluator:
    """
    Production generation evaluator.

    Uses:
        - LLM Judge
        - Sentence Transformers
    """

    def __init__(self) -> None:

        self.judge = LLMJudge()

        self.semantic = SemanticSimilarity()

    def evaluate(
        self,
        question: str,
        generated_answer: str,
        reference_answer: str,
        contexts: list[str],
    ) -> GenerationMetrics:
        """
        Evaluate one generated answer.
        """

        context = "\n\n".join(
            contexts,
        )

        judge_results = self.judge.evaluate(
            question=question,
            answer=generated_answer,
            reference=reference_answer,
            context=context,
        )

        semantic_similarity = self.semantic.score(
            generated_answer=generated_answer,
            reference_answer=reference_answer,
        )

        return GenerationMetrics(
            faithfulness=round(
                judge_results["faithfulness"],
                4,
            ),
            answer_correctness=round(
                judge_results["answer_correctness"],
                4,
            ),
            answer_relevancy=round(
                judge_results["answer_relevancy"],
                4,
            ),
            semantic_similarity=round(
                semantic_similarity,
                4,
            ),
            context_recall=round(
                judge_results["context_recall"],
                4,
            ),
            faithfulness_reason=judge_results[
                "faithfulness_reason"
            ],
            correctness_reason=judge_results[
                "correctness_reason"
            ],
            relevancy_reason=judge_results[
                "relevancy_reason"
            ],
            recall_reason=judge_results[
                "recall_reason"
            ],
        )