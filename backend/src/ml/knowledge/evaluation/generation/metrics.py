"""RAGAS metrics used for generation evaluation."""

from __future__ import annotations

from ragas.metrics import (
    AnswerCorrectness,
    AnswerRelevancy,
    ContextRecall,
    Faithfulness,
    SemanticSimilarity,
)

GENERATION_METRICS = [
    Faithfulness(),
    AnswerRelevancy(),
    ContextRecall(),
    SemanticSimilarity(),
    AnswerCorrectness(),
]