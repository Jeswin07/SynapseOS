"""Pure metric functions for RAG evaluation."""

from __future__ import annotations


def precision_at_k(
    retrieved: list[str],
    expected: list[str],
) -> float:
    """
    Precision@K

    retrieved = [A, B, C]
    expected = [A, D]

    Precision = 1 / 3
    """

    if not retrieved:
        return 0.0

    relevant = len(set(retrieved) & set(expected))

    return round(relevant / len(retrieved), 4)


def recall_at_k(
    retrieved: list[str],
    expected: list[str],
) -> float:
    """
    Recall@K

    retrieved = [A, B]
    expected = [A, C]

    Recall = 1 / 2
    """

    if not expected:
        return 0.0

    relevant = len(set(retrieved) & set(expected))

    return round(relevant / len(expected), 4)


def hit_rate(
    retrieved: list[str],
    expected: list[str],
) -> float:
    """
    Hit Rate

    Returns

    1.0 -> at least one relevant document retrieved

    0.0 -> no relevant document retrieved
    """

    return float(
        len(set(retrieved) & set(expected)) > 0
    )


def mean_reciprocal_rank(
    retrieved: list[str],
    expected: list[str],
) -> float:
    """
    Mean Reciprocal Rank.

    First relevant document determines score.

    Rank 1 -> 1.0

    Rank 2 -> 0.5

    Rank 3 -> 0.333...
    """

    expected_set = set(expected)

    for rank, document in enumerate(retrieved, start=1):

        if document in expected_set:

            return round(1.0 / rank, 4)

    return 0.0


def average_similarity(
    similarities: list[float],
) -> float:
    """
    Mean similarity score.
    """

    if not similarities:
        return 0.0

    return round(
        sum(similarities) / len(similarities),
        4,
    )


def highest_similarity(
    similarities: list[float],
) -> float:
    """
    Highest similarity score.
    """

    if not similarities:
        return 0.0

    return round(
        max(similarities),
        4,
    )


def retrieval_latency(
    latency_ms: float,
) -> float:
    """
    Round retrieval latency.
    """

    return round(latency_ms, 2)