"""In-memory feature cache."""

from __future__ import annotations

from threading import Lock

import pandas as pd


class FeatureCache:
    """
    Caches engineered feature dataframes.

    Cache key:
        dataset_version_id(s)

    Value:
        pandas DataFrame
    """

    _cache: dict[str, pd.DataFrame] = {}

    _lock = Lock()


    @classmethod
    def get(
        cls,
        key: str,
    ) -> pd.DataFrame | None:

        with cls._lock:

            return cls._cache.get(
                key,
            )


    @classmethod
    def set(
        cls,
        key: str,
        value: pd.DataFrame,
    ) -> None:

        with cls._lock:

            cls._cache[key] = value.copy(
                deep=False,
            )


    @classmethod
    def invalidate(
        cls,
        key: str,
    ) -> None:

        with cls._lock:

            cls._cache.pop(
                key,
                None,
            )


    @classmethod
    def clear(
        cls,
    ) -> None:

        with cls._lock:

            cls._cache.clear()