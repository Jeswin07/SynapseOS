from pathlib import Path

import joblib
import pandas as pd
import polars as pl
from prophet import Prophet


class ProphetTrainer:
    """
    Train and save Prophet forecasting models.
    """

    def train(
        self,
        dataframe: pl.DataFrame | pd.DataFrame,
        *,
        date_column: str,
        target_column: str,
        aggregation: str = "sum",
        frequency: str = "D",
    ) -> Prophet:
        """
        Train Prophet model using frequency-aware
        business aggregation.
        """

        # ----------------------------
        # Convert dataframe
        # ----------------------------

        if isinstance(dataframe, pl.DataFrame):

            df = (
                dataframe
                .select(
                    [
                        date_column,
                        target_column,
                    ]
                )
                .to_pandas()
            )

        else:

            df = (
                dataframe[
                    [
                        date_column,
                        target_column,
                    ]
                ]
                .copy()
            )

        df = df.rename(
            columns={
                date_column: "ds",
                target_column: "y",
            }
        )

        df["ds"] = pd.to_datetime(
            df["ds"],
            errors="coerce",
        )

        df["y"] = pd.to_numeric(
            df["y"],
            errors="coerce",
        )

        df = df.dropna()

        if df.empty:
            raise ValueError(
                "No numeric values available for forecasting."
            )

        # ----------------------------
        # Frequency-aware aggregation
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
            .agg(
                {
                    "y": aggregation,
                }
            )
            .sort_values("ds")
            .reset_index(drop=True)
        )

        # ----------------------------
        # Remove incomplete last period
        # (important for Olist)
        # ----------------------------

        if len(df) > 2:
            df = df.iloc[:-1].copy()

        # ----------------------------
        # Fill missing periods
        # ----------------------------

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

        if len(df) < 10:
            raise ValueError(
                "Not enough historical observations for forecasting."
            )

        # ----------------------------
        # Prophet
        # ----------------------------

        model = Prophet(
            yearly_seasonality="auto",
            weekly_seasonality="auto",
            daily_seasonality="auto",
            changepoint_prior_scale=0.05,
        )

        model.fit(df)

        return model

    def save(
        self,
        model: Prophet,
        path: str,
    ) -> None:

        Path(path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        joblib.dump(
            model,
            path,
        )

    def load(
        self,
        path: str,
    ) -> Prophet:

        return joblib.load(path)