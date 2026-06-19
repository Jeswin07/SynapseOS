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
        dataframe: pl.DataFrame,
        *,
        date_column: str,
        target_column: str,
        aggregation: str = "sum",
    ) -> Prophet:
        """
        Train a Prophet forecasting model.
        """

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
        print(dataframe.columns)
        print(date_column)

        df = df.rename(
            columns={
                date_column: "ds",
                target_column: "y",
            }
        )

        df["ds"] = pd.to_datetime(
            df["ds"]
        )
        print(df.columns)

# ------------------------------------
# Aggregate to daily business metrics
# ------------------------------------

        
        df["ds"] = df["ds"].dt.normalize()

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
        )

        df["ds"] = pd.to_datetime(df["ds"])

        df = df.sort_values(
            "ds"
        )

        df = df.reset_index(
            drop=True,
        )

        model = Prophet()

        model.fit(
            df,
        )

        return model

    def save(
        self,
        model: Prophet,
        path: str,
    ) -> None:
        """
        Save Prophet model.
        """

        Path(
            path,
        ).parent.mkdir(
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
        """
        Load Prophet model.
        """

        return joblib.load(
            path,
        )