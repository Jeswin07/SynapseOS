"""Model cache."""

from __future__ import annotations

from threading import Lock


class ModelCache:

    _cache = {}

    _lock = Lock()

    @classmethod
    def get(
        cls,
        key: str,
    ):

        with cls._lock:

            return cls._cache.get(
                key,
            )

    @classmethod
    def set(
        cls,
        key: str,
        model,
    ):

        with cls._lock:

            cls._cache[key] = model

    @classmethod
    def clear(
        cls,
    ):

        with cls._lock:

            cls._cache.clear()