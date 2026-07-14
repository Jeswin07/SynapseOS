"""Prediction target builder."""

from __future__ import annotations

import pandas as pd

from src.ml.prediction.schemas import (
    PredictionType,
)


class PredictionTargetBuilder:
    """Creates business prediction targets."""


    def build(
        self,
        data: pd.DataFrame,
        prediction_type: PredictionType,
    ) -> pd.Series:

        if (
            prediction_type
            ==
            PredictionType.CUSTOMER_CHURN
        ):
            return self._churn(data)


        if (
            prediction_type
            ==
            PredictionType.DELIVERY_DELAY
        ):
            return self._delivery(data)


        raise ValueError(
            "Unsupported prediction type",
        )


    def _churn(
        self,
        data: pd.DataFrame,
    ) -> pd.Series:
        """
        Behaviour based churn proxy.
        """

        risk = pd.Series(
            0,
            index=data.index,
        )


        if "total_orders" in data:
            risk += (
                data["total_orders"]
                <= 1
            ).astype(int)


        if "average_review" in data:
            risk += (
                data["average_review"]
                < 3
            ).astype(int)


        if "late_deliveries" in data:
            risk += (
                data["late_deliveries"]
                > 0
            ).astype(int)


        return (
            risk >= 2
        ).astype(int)


    def _delivery(
        self,
        data: pd.DataFrame,
    ) -> pd.Series:

        if "late_deliveries" not in data:
            return pd.Series(
                0,
                index=data.index,
            )


        return (
            data["late_deliveries"]
            > 0
        ).astype(int)