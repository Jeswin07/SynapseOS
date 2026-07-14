"""Prediction engine."""

from __future__ import annotations

from src.ml.prediction.customer_features import (
    CustomerFeatureBuilder,
)
from src.ml.prediction.explainer import (
    PredictionExplainer,
)
from src.ml.prediction.predictor import (
    PredictionExecutor,
)
from src.ml.prediction.schemas import *
from src.ml.prediction.trainer import (
    PredictionTrainer,
)
from src.ml.cache.model_cache import ModelCache


class PredictionEngine:
    """Business prediction engine."""


    def __init__(self):

        self.builder = CustomerFeatureBuilder()
        self.trainer = PredictionTrainer()
        self.predictor = PredictionExecutor()
        self.explainer = PredictionExplainer()


    def predict(
        self,
        data,
        prediction_type,
    ):

        customers = self.builder.build(
            data,
        )


        cache_key = (
            prediction_type.value
            + "_"
            + str(
                len(customers),
            )
        )

        model = ModelCache.get(
            cache_key,
        )

        if model is None:

            model = self.trainer.train(
                customers,
                prediction_type,
            )

            ModelCache.set(
                cache_key,
                model,
            )


        features = self.trainer.prepare_features(
            customers,
        )


        probabilities = self.predictor.predict(
            model,
            features,
        )


        customers["_risk"] = probabilities


        ranked = customers.sort_values(
            "_risk",
            ascending=False,
        )


        predictions = []


        for _, row in ranked.head(20).iterrows():

            probability = float(row["_risk"])


            predictions.append(
                EntityPrediction(
                    entity_id=row[
                        "customer_id"
                    ],
                    probability=probability,
                    level=self._level(
                        probability,
                    ),
                    drivers=self.explainer.explain(
                        row,
                    ),
                    metrics={
                        "orders": row.get(
                            "total_orders",
                            0,
                        ),
                        "revenue": row.get(
                            "total_revenue",
                            0,
                        ),
                        "rating": row.get(
                            "average_review",
                            0,
                        ),
                    },
                )
            )


        high = sum(
            p.level == PredictionLevel.HIGH
            for p in predictions
        )


        revenue_at_risk = sum(
            p.metrics["revenue"]
            for p in predictions
        )


        return PredictionResult(
            prediction_type=prediction_type,
            summary=PredictionSummary(
                total_entities=len(customers),
                high_risk_entities=high,
                average_probability=sum(
                    probabilities,
                )
                /
                len(probabilities),
                business_impact={
                    "revenue_at_risk":
                        revenue_at_risk,
                },
            ),
            predictions=predictions,
            recommendations=[
                "Launch retention campaigns for high-risk customers.",
                "Improve satisfaction and delivery performance.",
            ],
        )


    def _level(
        self,
        probability,
    ):

        if probability >= 0.7:
            return PredictionLevel.HIGH

        if probability >= 0.4:
            return PredictionLevel.MEDIUM

        return PredictionLevel.LOW