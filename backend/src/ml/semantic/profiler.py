"""Dataset semantic profiler."""

from __future__ import annotations

import pandas as pd

from src.ml.semantic.schemas import (
    ColumnProfile,
    SemanticProfile,
    TableProfile,
)


class SemanticProfiler:
    """
    Extracts schema information from datasets.

    No business logic here.
    """

    def profile(
        self,
        tables: dict[str, pd.DataFrame],
    ) -> SemanticProfile:


        table_profiles = []


        for (
            table_name,
            dataframe,
        ) in tables.items():


            columns = []


            for column in dataframe.columns:


                samples = (
                    dataframe[column]
                    .dropna()
                    .head(5)
                    .tolist()
                )


                columns.append(
                    ColumnProfile(
                        name=column,
                        dtype=str(
                            dataframe[column].dtype,
                        ),
                        samples=samples,
                    )
                )


            table_profiles.append(
                TableProfile(
                    table_name=table_name,
                    columns=columns,
                )
            )


        return SemanticProfile(
            tables=table_profiles,
        )