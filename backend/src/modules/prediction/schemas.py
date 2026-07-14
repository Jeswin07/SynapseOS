"""Prediction API schemas."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel


class PredictionRequest(
    BaseModel,
):
    """Prediction execution request."""

    dataset_version_id: UUID

    prediction_type: str = "customer_churn"


class PredictionResponse(
    BaseModel,
):
    """Prediction response."""

    id: UUID | None = None

    prediction_type: str

    result: dict[str, Any]


class PredictionHistoryItem(
    BaseModel,
):
    """Previous prediction run."""

    id: UUID

    prediction_type: str

    result: dict[str, Any]


    class Config:
        from_attributes = True