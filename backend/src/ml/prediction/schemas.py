"""Schemas for ML prediction intelligence."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PredictionType(
    str,
    Enum,
):
    """
    Supported business prediction workflows.
    """

    CUSTOMER_CHURN = "customer_churn"

    DELIVERY_DELAY = "delivery_delay"


class PredictionLevel(
    str,
    Enum,
):
    """
    Business friendly prediction severity.
    """

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"


class EntityPrediction(BaseModel):
    """
    Single entity prediction result.
    """

    entity_id: str | None = None

    probability: float

    level: PredictionLevel

    drivers: list[str] = Field(
        default_factory=list,
    )


class PredictionSummary(BaseModel):
    """
    Aggregated prediction overview.
    """

    total_entities: int

    high_risk_entities: int

    average_probability: float


class PredictionResult(BaseModel):
    """
    Final prediction response.

    Designed for:
    - MCP
    - Risk engine
    - Scenario simulations
    """

    prediction_type: PredictionType

    summary: PredictionSummary

    predictions: list[
        EntityPrediction
    ]

    recommendations: list[str] = Field(
        default_factory=list,
    )

    metadata: dict[
        str,
        Any,
    ] = Field(
        default_factory=dict,
    )