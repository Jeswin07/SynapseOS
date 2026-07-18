"""Forecast model evaluation."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import polars as pl
from prophet import Prophet
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)


class ForecastEvaluator:
    """
    Evaluates Prophet forecasting models using
    a simple hold-out validation.

    Last 20% of observations are used for validation.
    """

    def evaluate(
        self,
        dataframe: pl.DataFrame | pd.DataFrame,
        *,
        date_column: str,
        target_column: str,
        aggregation: str = "sum",
        frequency: str = "D",
    ) -> dict:
        """
        Returns evaluation metrics.

        {
            "performance_score": 91,
            "performance_label": "Excellent",
            "mae": ...,
            "rmse": ...,
            "mape": ...
        }
        """

        # ----------------------------
        # Convert dataframe
        # ----------------------------

        if isinstance(dataframe, pl.DataFrame):
            df = dataframe.select(
                [
                    date_column,
                    target_column,
                ]
            ).to_pandas()

        else:
            df = dataframe[
                [
                    date_column,
                    target_column,
                ]
            ].copy()

        df = df.rename(
            columns={
                date_column: "ds",
                target_column: "y",
            }
        )

        df["ds"] = pd.to_datetime(df["ds"])

        df["y"] = pd.to_numeric(
            df["y"],
            errors="coerce",
        )

        df = df.dropna()

        if df.empty:
            raise ValueError(
                "No data available for evaluation."
            )

        # ----------------------------
        # Aggregate
        # ----------------------------

        frequency = frequency.upper()

        if frequency == "D":
            df["ds"] = df["ds"].dt.floor("D")
            pandas_frequency = "D"

        elif frequency == "W":
            df["ds"] = (
                df["ds"]
                .dt.to_period("W")
                .dt.start_time
            )
            pandas_frequency = "W-MON"

        elif frequency == "M":
            df["ds"] = (
                df["ds"]
                .dt.to_period("M")
                .dt.start_time
            )
            pandas_frequency = "MS"

        else:
            df["ds"] = df["ds"].dt.floor("D")
            pandas_frequency = "D"

        df = (
            df.groupby(
                "ds",
                as_index=False,
            )
            .agg({"y": aggregation})
            .sort_values("ds")
            .reset_index(drop=True)
        )

        # Remove incomplete final period
        last_date = df["ds"].max()

        if frequency == "M":
            if last_date.day < last_date.days_in_month:
                df = df.iloc[:-1]

        elif frequency == "W":
            if last_date.weekday() != 6:
                df = df.iloc[:-1]

        # Fill missing periods
        df = (
            df.set_index("ds")
            .asfreq(pandas_frequency)
        )

        if aggregation == "mean":
            df["y"] = (
                df["y"]
                .interpolate()
                .bfill()
                .ffill()
            )
        else:
            df["y"] = df["y"].fillna(0)

        df = (
            df.reset_index()
            .sort_values("ds")
        )

        if len(df) < 20:
            raise ValueError(
                "Not enough historical observations "
                "to evaluate forecast."
            )

        # ----------------------------
        # Train / Validation split
        # ----------------------------

        split = int(len(df) * 0.8)

        train = df.iloc[:split]

        validation = df.iloc[split:]
        validation = validation.iloc[:-1].copy()

        model = Prophet(
            yearly_seasonality="auto",
            weekly_seasonality="auto",
            daily_seasonality="auto",
            changepoint_prior_scale=0.05,
        )

        model.fit(train)

        future = model.make_future_dataframe(
            periods=len(validation),
            freq=pandas_frequency,
        )

        forecast = model.predict(future)

        prediction = (
            forecast.tail(len(validation))["yhat"]
            .to_numpy(dtype=float)
        )

        actual = (
            validation["y"]
            .to_numpy(dtype=float)
        )

        # ----------------------------
        # Metrics
        # ----------------------------

        mae = float(
            mean_absolute_error(
                actual,
                prediction,
            )
        )

        rmse = float(
            math.sqrt(
                mean_squared_error(
                    actual,
                    prediction,
                )
            )
        )

        actual = actual.astype(float)
        prediction = prediction.astype(float)

        non_zero = actual != 0

        if np.any(non_zero):

            mape = float(
                np.mean(
                    np.abs(
                        (
                            actual[non_zero]
                            - prediction[non_zero]
                        )
                        / actual[non_zero]
                    )
                )
                * 100
            )

        else:
            mape = 100.0

        score = self._performance_score(
            mape
        )


        return {
            "performance_score": score,
            "performance_label": self._label(
                score
            ),
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "mape": round(mape, 2),
        }

    def _performance_score(
        self,
        mape: float,
    ) -> int:
        """
        Convert MAPE to a
        business-friendly score.
        """

        if mape <= 5:
            score = 98
        elif mape <= 10:
            score = 95
        elif mape <= 15:
            score = 90
        elif mape <= 20:
            score = 85
        elif mape <= 30:
            score = 75
        elif mape <= 40:
            score = 65
        else:
            score = 50

        return score

    def _label(
        self,
        score: int,
    ) -> str:

        if score >= 90:
            return "Excellent"

        if score >= 80:
            return "Very Good"

        if score >= 70:
            return "Good"

        if score >= 60:
            return "Fair"

        return "Needs Improvement"