"""Prediction intelligence schemas."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PredictionType(str, Enum):
    """Supported prediction workflows."""

    CUSTOMER_CHURN = "customer_churn"
    DELIVERY_DELAY = "delivery_delay"


class PredictionLevel(str, Enum):
    """Prediction severity."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class EntityPrediction(BaseModel):
    """Single entity prediction."""

    entity_id: str

    probability: float

    level: PredictionLevel

    drivers: list[str]

    metrics: dict[str, Any] = Field(
        default_factory=dict,
    )


class PredictionSummary(BaseModel):
    """Prediction summary."""

    total_entities: int

    high_risk_entities: int

    average_probability: float

    business_impact: dict[str, Any] = Field(
        default_factory=dict,
    )


class PredictionResult(BaseModel):
    """
    Prediction output contract.

    Used by:
    - Intelligence Agent
    - Risk Tool
    - Scenario Agent
    """

    prediction_type: PredictionType

    summary: PredictionSummary

    predictions: list[EntityPrediction]

    recommendations: list[str]

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )