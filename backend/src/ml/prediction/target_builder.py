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
        Commerce churn based on customer inactivity.
        """

        if "last_order_date" not in data.columns:
            raise ValueError(
                "last_order_date is required for customer churn prediction."
            )

        frame = data.copy()

        frame["last_order_date"] = pd.to_datetime(
            frame["last_order_date"],
            errors="coerce",
        )

        latest_date = frame["last_order_date"].max()

        days_since_last_purchase = (
            latest_date - frame["last_order_date"]
        ).dt.days

        print(days_since_last_purchase.describe())

        for threshold in [90, 120, 150, 180, 210]:
            target = (days_since_last_purchase >= threshold).astype(int)
            print(threshold)
            print(target.value_counts(normalize=True))

        return (
            days_since_last_purchase >= 180
        ).astype(int)


    def _delivery(
        self,
        data: pd.DataFrame,
    ) -> pd.Series:
        """
        Build delivery delay target.

        Target:
            1 -> Delivered after estimated date
            0 -> Delivered on/before estimated date
        """
        frame = data.copy()

         # Case 1
        if "delivery_delay_days" in frame.columns:
            delay = pd.to_numeric(
                frame["delivery_delay_days"],
                errors="coerce",
            ).fillna(0)

    # Case 2
        elif (
            "actual_delivery_days" in frame.columns
            and "estimated_delivery_days" in frame.columns
        ):
            delay = (
                pd.to_numeric(
                    frame["actual_delivery_days"],
                    errors="coerce",
                )
                -
                pd.to_numeric(
                    frame["estimated_delivery_days"],
                    errors="coerce",
                )
            ).fillna(0)

        # Case 3
        elif (
            "delivery_date" in frame.columns
            and "estimated_delivery_date" in frame.columns
        ):
            delay = (
                pd.to_datetime(frame["delivery_date"])
                -
                pd.to_datetime(frame["estimated_delivery_date"])
            ).dt.days.fillna(0)

        else:
            raise ValueError(
                "Dataset does not contain enough information "
                "to build delivery prediction target."
            )

        target = (delay > 0).astype(int)

        print("=" * 80)
        print("Delivery Target Distribution")
        print(target.value_counts())
        print(target.value_counts(normalize=True))
        print("=" * 80)

        return target