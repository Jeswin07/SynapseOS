"""Prediction execution engine."""

from __future__ import annotations

import numpy as np
import pandas as pd


class PredictionExecutor:
    """
    Executes trained ML models and calibrates
    prediction probabilities for business use.
    """


    def predict(
        self,
        model,
        features: pd.DataFrame,
    ) -> np.ndarray:
        """
        Run model prediction and return calibrated
        probability scores.
        """

        if hasattr(
            model,
            "predict_proba",
        ):

            probabilities = (
                model.predict_proba(
                    features,
                )[:, 1]
            )

        else:

            probabilities = (
                model.predict(
                    features,
                )
            )


        probabilities = (
            probabilities
            *
            0.85
            +
            0.05
        )


        probabilities = np.clip(
            probabilities,
            0.05,
            0.95,
        )


        return probabilities.round(
            2,
        )