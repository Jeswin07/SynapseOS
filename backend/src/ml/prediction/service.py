"""Prediction engine."""

from __future__ import annotations

from src.ml.cache.model_cache import ModelCache
from src.ml.prediction.customer_features import (
    CustomerFeatureBuilder,
)
from src.ml.prediction.delivery_features import (
    DeliveryFeatureBuilder,
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


class PredictionEngine:
    """Business prediction engine."""


    def __init__(self):

        self.builder = CustomerFeatureBuilder()
        self.delivery_builder = DeliveryFeatureBuilder()
        self.trainer = PredictionTrainer()
        self.predictor = PredictionExecutor()
        self.explainer = PredictionExplainer()


    def predict(
        self,
        data,
        prediction_type,
    ):

        if prediction_type == PredictionType.CUSTOMER_CHURN:
            records = self.builder.build(data)

        else:
            records = self.delivery_builder.build(data)


        cache_key = (
            prediction_type.value
            + "__"
            + str(
                len(records),
            )
        )

        cached = ModelCache.get(
            cache_key,
        )

        if cached is None:

            model, evaluation = self.trainer.train(
                records,
                prediction_type,
                )

            ModelCache.set(
                cache_key,
                (model, evaluation),
            )

        else:
            model, evaluation = cached


        features = self.trainer.prepare_features(
            records,
            prediction_type
        )


        probabilities = self.predictor.predict(
            model,
            features,
        )


        records["_risk"] = probabilities


        ranked = records.sort_values(
            "_risk",
            ascending=False,
        )


        predictions = []

        top_n = min(
            max(int(len(records) * 0.05), 20),
            100,
        )
        
        for _, row in ranked.head(top_n).iterrows():

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
                total_entities=len(records),
                high_risk_entities=high,
                average_probability=sum(probabilities) / len(probabilities),
                business_impact={
                    "revenue_at_risk": revenue_at_risk,
                },
            ),
            predictions=predictions,
            recommendations=[
                "Launch retention campaigns for high-risk customers.",
                "Improve satisfaction and delivery performance.",
            ],
            metadata=evaluation
        )


    def _level(
        self,
        probability,
    ):

        if probability >= 0.80:
            return PredictionLevel.HIGH

        if probability >= 0.60:
            return PredictionLevel.MEDIUM

        return PredictionLevel.LOW