"""Analytics result cache."""

from __future__ import annotations

from threading import Lock
from typing import Any


class AnalyticsCache:
    """
    Caches computed analytics results.

    Key:
        dataset_version

    Value:
        analytics dictionary
    """

    _cache: dict[str, dict[str, Any]] = {}

    _lock = Lock()

    @classmethod
    def get(
        cls,
        key: str,
    ) -> dict[str, Any] | None:

        with cls._lock:
            return cls._cache.get(
                key,
            )

    @classmethod
    def set(
        cls,
        key: str,
        value: dict[str, Any],
    ) -> None:

        with cls._lock:
            cls._cache[key] = value

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