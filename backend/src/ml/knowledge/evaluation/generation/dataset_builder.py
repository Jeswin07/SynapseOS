"""Builds RAGAS evaluation datasets."""

from __future__ import annotations

from ragas import EvaluationDataset

from src.ml.knowledge.evaluation.generation.schemas import (
    GenerationEvaluationCase,
)


class GenerationDatasetBuilder:
    """
    Converts benchmark cases into a RAGAS EvaluationDataset.
    """

    @staticmethod
    def build(
        cases: list[GenerationEvaluationCase],
        generated_answers: list[str],
        retrieved_contexts: list[list[str]],
    ) -> EvaluationDataset:
        """
        Build a RAGAS EvaluationDataset.
        """

        samples = []

        for case, answer, contexts in zip(
            cases,
            generated_answers,
            retrieved_contexts,
            strict=True,
        ):

            samples.append(
                {
                    "user_input": case.question,
                    "response": answer,
                    "reference": case.expected_answer,
                    "retrieved_contexts": contexts,
                }
            )

        return EvaluationDataset.from_list(samples)