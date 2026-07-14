"""Prediction result cache."""

from __future__ import annotations

from threading import Lock
from typing import Any


class PredictionCache:

    _cache: dict[str, Any] = {}

    _lock = Lock()

    @classmethod
    def get(
        cls,
        key: str,
    ) -> Any:

        with cls._lock:
            return cls._cache.get(key)

    @classmethod
    def set(
        cls,
        key: str,
        value: Any,
    ) -> None:

        with cls._lock:
            cls._cache[key] = value

    @classmethod
    def clear(
        cls,
    ) -> None:

        with cls._lock:
            cls._cache.clear()