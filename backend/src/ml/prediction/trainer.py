"""Prediction model trainer."""

from __future__ import annotations

import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from src.ml.prediction.schemas import PredictionType
from src.ml.prediction.target_builder import (
    PredictionTargetBuilder,
)


class PredictionTrainer:
    """ML training pipeline."""


    def __init__(self) -> None:

        self.targets = PredictionTargetBuilder()


    def train(
        self,
        data: pd.DataFrame,
        prediction_type: PredictionType,
    ):

        features = self.prepare_features(
            data,
        )

        target = self.targets.build(
            data,
            prediction_type,
        )


        model = RandomForestClassifier(
            n_estimators=120,
            random_state=42,
            class_weight="balanced",
        )


        model.fit(
            features,
            target,
        )


        return model


    def prepare_features(
        self,
        data: pd.DataFrame,
    ):

        drop = [
            "customer_id",
        ]


        return (
            data.drop(
                columns=[
                    c
                    for c in drop
                    if c in data
                ],
            )
            .select_dtypes(
                include=[
                    "number",
                    "bool",
                ],
            )
            .fillna(0)
        )