"""Generic dataset filter option builder."""

from __future__ import annotations

from typing import Any

import pandas as pd


class DatasetFilterOptions:
    """
    Builds available filter options from a canonical feature dataframe.

    Since the Feature Builder standardizes all supported commerce datasets
    into canonical columns, this service works automatically for Olist,
    Flipkart, Shopify, WooCommerce and future datasets.
    """

    def build(
        self,
        dataframe: pd.DataFrame,
    ) -> dict[str, Any]:
        """
        Build all available frontend filter options.
        """

        return {
            "date": self._date_option(dataframe),

            "categories": self._unique_option(
                dataframe,
                "category",
            ),

            "brands": self._unique_option(
                dataframe,
                "brand",
            ),

            "states": self._unique_option(
                dataframe,
                "state",
            ),

            "revenue": self._range_option(
                dataframe,
                "revenue",
            ),

            "review_score": self._range_option(
                dataframe,
                "review_score",
            ),
        }

    # ------------------------------------------------------------------
    # Unique value filters
    # ------------------------------------------------------------------

    def _unique_option(
        self,
        dataframe: pd.DataFrame,
        column: str,
    ) -> dict[str, Any]:
        """
        Build dropdown values for a categorical filter.
        """

        if column not in dataframe.columns:
            return {
                "enabled": False,
                "values": [],
            }

        values = (
            dataframe[column]
            .dropna()
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .unique()
            .tolist()
        )

        values = sorted(values)

        return {
            "enabled": len(values) > 0,
            "values": values,
        }

    # ------------------------------------------------------------------
    # Date filter
    # ------------------------------------------------------------------

    def _date_option(
        self,
        dataframe: pd.DataFrame,
    ) -> dict[str, Any]:
        """
        Build date range filter.
        """

        if "order_date" not in dataframe.columns:
            return {
                "enabled": False,
                "min": None,
                "max": None,
            }

        dates = pd.to_datetime(
            dataframe["order_date"],
            errors="coerce",
        ).dropna()

        if dates.empty:
            return {
                "enabled": False,
                "min": None,
                "max": None,
            }

        return {
            "enabled": True,
            "min": dates.min().strftime("%Y-%m-%d"),
            "max": dates.max().strftime("%Y-%m-%d"),
        }

    # ------------------------------------------------------------------
    # Numeric range filters
    # ------------------------------------------------------------------

    def _range_option(
        self,
        dataframe: pd.DataFrame,
        column: str,
    ) -> dict[str, Any]:
        """
        Build min/max values for numeric filters.
        """

        if column not in dataframe.columns:
            return {
                "enabled": False,
                "min": None,
                "max": None,
            }

        values = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        ).dropna()

        if values.empty:
            return {
                "enabled": False,
                "min": None,
                "max": None,
            }

        return {
            "enabled": True,
            "min": float(values.min()),
            "max": float(values.max()),
        }