"""Risk schemas."""

from __future__ import annotations

from pydantic import BaseModel


class RiskItem(BaseModel):
    """
    Individual business risk.
    """

    type: str

    score: int

    severity: str

    impact: dict

    affected_entities: int | None

    recommendations: list[str]


class RiskResponse(BaseModel):

    overall_risk: int

    level: str

    risks: list[RiskItem]