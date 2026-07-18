"""Analytics schemas."""

from __future__ import annotations

import uuid

from pydantic import BaseModel
from src.ml.core.filtering.schemas import DatasetFilters


class AnalyticsRequest(BaseModel):
    """
    Analytics generation request.
    """

    dataset_version_id: uuid.UUID
    filters: DatasetFilters | None = None


class AnalyticsMetric(BaseModel):
    """
    Single analytics metric.
    """

    name: str

    value: float | int | str | None


class AnalyticsResponse(BaseModel):
    """
    Business analytics result.
    """

    dataset_version_id: uuid.UUID

    metrics: list[AnalyticsMetric]