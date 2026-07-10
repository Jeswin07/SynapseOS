"""Generic feature builder."""

from __future__ import annotations

import pandas as pd

from src.ml.features.base import BaseFeatureBuilder


class GenericFeatureBuilder(BaseFeatureBuilder):
    """
    Generic feature builder.

    Used when dataset does not follow
    a predefined schema.

    Examples:
    - single CSV sales data
    - Flipkart exports
    - CRM exports
    - finance data
    - custom business datasets
    """


    def build(
        self,
        datasets: dict[str, pd.DataFrame],
    ) -> pd.DataFrame:


        if not datasets:

            raise ValueError(
                "No datasets provided."
            )


        # ----------------------------
        # Single file dataset
        # ----------------------------

        if len(datasets) == 1:

            return (
                list(
                    datasets.values()
                )[0]
                .copy()
            )


        # ----------------------------
        # Multiple unknown files
        # fallback merge strategy
        # ----------------------------

        frames = list(
            datasets.values()
        )


        base = (
            frames[0]
            .copy()
        )


        for frame in frames[1:]:


            common_columns = (
                set(base.columns)
                &
                set(frame.columns)
            )


            join_keys = [
                col
                for col in common_columns
                if (
                    "id" in col.lower()
                    or
                    col.lower().endswith("_id")
                )
            ]


            if join_keys:

                base = base.merge(
                    frame,
                    on=join_keys[0],
                    how="left",
                )


        return base