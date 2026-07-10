"""Prediction target generation."""

from __future__ import annotations

import pandas as pd

from src.ml.prediction.schemas import (
    PredictionType,
)


class PredictionTargetBuilder:
    """
    Creates ML targets from commerce data.

    Commerce datasets usually do not contain
    ready-made ML labels like churn.

    This component converts business behaviour
    into trainable targets.
    """


    def build(
        self,
        data: pd.DataFrame,
        prediction_type: PredictionType,
    ) -> pd.Series:
        """
        Build prediction target column.
        """

        if (
            prediction_type
            ==
            PredictionType.CUSTOMER_CHURN
        ):
            return self._customer_churn(
                data,
            )

        if (
            prediction_type
            ==
            PredictionType.DELIVERY_DELAY
        ):
            return self._delivery_delay(
                data,
            )

        raise ValueError(
            "Unsupported prediction type.",
        )


    def _customer_churn(
        self,
        data: pd.DataFrame,
    ) -> pd.Series:
        """
        Estimate churn from customer behaviour.
        """

        if "review_score" in data.columns:

            return (
                data["review_score"]
                .fillna(5)
                .lt(3)
                .astype(int)
            )

        return pd.Series(
            0,
            index=data.index,
        )


    def _delivery_delay(
        self,
        data: pd.DataFrame,
    ) -> pd.Series:
        """
        Detect delayed deliveries.
        """

        if "delivery_delay_days" in data.columns:

            return (
                data["delivery_delay_days"]
                .fillna(0)
                .gt(0)
                .astype(int)
            )

        return pd.Series(
            0,
            index=data.index,
        )