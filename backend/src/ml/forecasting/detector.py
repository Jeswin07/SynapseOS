"""Forecast column detector."""

from __future__ import annotations

import pandas as pd
import polars as pl


class ForecastColumnDetector:
    """
    Automatically detects forecasting columns.
    """


    DATE_KEYWORDS = [
        "date",
        "time",
        "created",
        "timestamp",
        "purchase",
        "order",
    ]


    TARGET_KEYWORDS = [
        "revenue",
        "sales",
        "amount",
        "price",
        "total",
        "value",
    ]


    def detect(
        self,
        dataframe: pl.DataFrame,
    ) -> dict[str, str]:


        columns = dataframe.columns


        date_column = self._find_date_column(
            dataframe,
        )


        target_column = self._find_target_column(
            dataframe,
        )


        if date_column is None:

            raise ValueError(
                "Could not detect date column."
            )


        if target_column is None:

            raise ValueError(
                "Could not detect forecast target column."
            )


        return {
            "date_column": date_column,
            "target_column": target_column,
        }


    def _find_date_column(
        self,
        dataframe,
    ) -> str | None:

        priority = [
            "date",
            "order_date",
            "created_at",
            "order_purchase_timestamp",
        ]


        for column in priority:

            if column in dataframe.columns:

                try:

                    parsed = (
                        pd.to_datetime(
                            dataframe[column],
                            errors="coerce",
                        )
                    )

                    if (
                        parsed.notna().mean()
                        > 0.8
                    ):

                        return column

                except Exception:

                    pass


        for column in dataframe.columns:

            name = column.lower()


            if (
                "id" in name
                or "uuid" in name
            ):

                continue


            if any(
                keyword in name
                for keyword in self.DATE_KEYWORDS
            ):

                parsed = (
                    pd.to_datetime(
                        dataframe[column],
                        errors="coerce",
                    )
                )


                if (
                    parsed.notna().mean()
                    > 0.8
                ):

                    return column


        return None


    def _find_target_column(
        self,
        dataframe: pl.DataFrame,
    ) -> str | None:


        priority = [
            "revenue",
            "sales",
            "profit",
            "orders",
        ]


        for column in priority:

            if column in dataframe.columns:

                return column


        if isinstance(
            dataframe,
            pl.DataFrame,
        ):

            numeric_columns = [
                column
                for column, dtype
                in zip(
                    dataframe.columns,
                    dataframe.dtypes,
                )
                if dtype.is_numeric()
            ]


        else:

            numeric_columns = (
                dataframe
                .select_dtypes(
                    include="number",
                )
                .columns
                .tolist()
            )


        for column in numeric_columns:

            name = column.lower()

            if any(
                keyword in name
                for keyword in self.TARGET_KEYWORDS
            ):

                return column


        return None