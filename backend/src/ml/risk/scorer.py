"""Business risk scoring."""

from __future__ import annotations


class RiskScorer:
    """
    Enterprise business risk scorer.
    """


    def calculate_score(
        self,
        *,
        probability: float,
        impact: float,
        entities: int,
    ) -> int:

        probability_score = (
            probability
            *
            40
        )

        impact_score = min(
            impact / 200,
            40,
        )

        entity_score = min(
            entities,
            20,
        )


        return int(
            min(
                probability_score
                +
                impact_score
                +
                entity_score,
                100,
            )
        )


    def severity(
        self,
        score: int,
    ) -> str:

        if score >= 75:
            return "CRITICAL"

        if score >= 55:
            return "HIGH"

        if score >= 30:
            return "MEDIUM"

        return "LOW"