"""Risk analysis engine."""

from __future__ import annotations

from src.ml.risk.scorer import RiskScorer


class RiskEngine:
    """
    Converts predictions into business risks.
    """

    def __init__(
        self,
    ) -> None:

        self.scorer = RiskScorer()


    def analyze(
        self,
        predictions: list,
    ) -> dict:


        latest = {}


        for prediction in predictions:

            if (
                prediction.prediction_type
                not in latest
            ):
                latest[
                    prediction.prediction_type
                ] = prediction


        risks = []


        for prediction in latest.values():

            summary = (
                prediction.result
                .get(
                    "summary",
                    {},
                )
            )


            impact = (
                summary
                .get(
                    "business_impact",
                    {},
                )
                .get(
                    "revenue_at_risk",
                    0,
                )
            )


            score = self.scorer.calculate_score(
                probability=summary.get(
                    "average_probability",
                    0,
                ),
                impact=impact,
                entities=summary.get(
                    "high_risk_entities",
                    0,
                ),
            )


            risks.append(
                {
                    "type": prediction.prediction_type,
                    "score": score,
                    "severity": (
                        self.scorer.severity(
                            score,
                        )
                    ),
                    "impact": summary.get(
                        "business_impact",
                        {},
                    ),
                    "affected_entities": summary.get(
                        "high_risk_entities",
                    ),
                    "recommendations": (
                        self.recommendations(
                            prediction.prediction_type,
                        )
                    ),
                }
            )


        overall = max(
            [
                risk["score"]
                for risk in risks
            ],
            default=0,
        )


        return {
            "overall_risk": overall,
            "level": self.scorer.severity(
                overall,
            ),
            "risks": risks,
        }

    def recommendations(
        self,
        risk_type: str,
    ) -> list[str]:

        mapping = {
            "customer_churn": [
                "Launch targeted retention campaigns.",
                "Improve customer satisfaction."
            ],

            "delivery_delay": [
                "Optimize delivery operations.",
                "Investigate logistics bottlenecks."
            ],
        }

        return mapping.get(
            risk_type,
            [
                "Review operational risks."
            ],
        )