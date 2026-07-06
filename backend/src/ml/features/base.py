"""Base feature builder."""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)

import pandas as pd


class BaseFeatureBuilder(ABC):
    """
    Base class for domain feature builders.

    Converts raw enterprise datasets into
    analytics/ML-ready datasets.
    """


    @abstractmethod
    def build(
        self,
        datasets: dict[str, pd.DataFrame],
    ) -> pd.DataFrame:
        """
        Build feature dataset.

        Args:
            datasets:
                Mapping of logical dataset names
                to DataFrames.

        Example:
            {
              "orders": df,
              "customers": df
            }

        Returns:
            Feature DataFrame.
        """

        raise NotImplementedError