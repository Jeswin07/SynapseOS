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


        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features)[:, 1]
        else:
            probabilities = model.predict(features).astype(float)

        probabilities = np.clip(probabilities, 0.0, 1.0)

        return probabilities.round(3)
