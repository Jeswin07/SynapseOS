"""Internal models used by the Scenario Agent."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from src.mcp.types import MCPTool

# ==========================================================
# Enums
# ==========================================================


class ScenarioIntent(StrEnum):
    """
    High-level intent detected from a user's scenario.
    """

    WHAT_IF = "what_if"

    COMPARISON = "comparison"

    OPTIMIZATION = "optimization"

    RISK_MITIGATION = "risk_mitigation"


class ScenarioType(StrEnum):
    """
    Business domain affected.
    """

    SALES = "sales"

    REVENUE = "revenue"

    CUSTOMER = "customer"

    MARKETING = "marketing"

    DELIVERY = "delivery"

    INVENTORY = "inventory"

    PRICING = "pricing"

    OPERATIONS = "operations"

    FINANCE = "finance"

    GENERAL = "general"


class ParameterOperation(StrEnum):
    """
    Supported parameter operations.
    """

    INCREASE = "increase"

    DECREASE = "decrease"

    SET = "set"

    COMPARE = "compare"

    UNKNOWN = "unknown"


class ConfidenceLevel(StrEnum):
    """
    Confidence assigned to the final decision.
    """

    HIGH = "high"

    MEDIUM = "medium"

    LOW = "low"


# ==========================================================
# Planner Models
# ==========================================================


class ScenarioParameter(BaseModel):
    """
    Structured parameter extracted from
    the user's request.
    """

    metric: str

    operation: ParameterOperation

    current_value: float | None = None

    target_value: float | None = None

    value: float | None = None

    unit: str | None = None


class ScenarioPlan(BaseModel):
    """
    Output of the Scenario Planner.
    """

    intent: ScenarioIntent

    scenario_type: ScenarioType

    reasoning: str

    parameters: list[
        ScenarioParameter
    ] = Field(
        default_factory=list,
    )


class EvidencePlan(BaseModel):
    """
    MCP execution plan.
    """

    tools: list[
        MCPTool
    ] = Field(
        default_factory=list,
    )

    reasoning: str

# ==========================================================
# Decision Models
# ==========================================================


class ImpactItem(BaseModel):
    """
    Business impact identified from the evidence.
    """

    title: str

    description: str

    severity: str = "MEDIUM"

    positive: bool = True


class TradeoffItem(BaseModel):
    """
    Business trade-off.

    Every benefit should have an associated cost.
    """

    benefit: str

    cost: str


class DecisionReport(BaseModel):
    """
    Internal decision object built by the
    Decision Builder.

    This object is intentionally completely
    structured.

    The Business Agent is responsible for
    converting it into executive language.
    """

    summary: str = ""

    impacts: list[
        ImpactItem
    ] = Field(
        default_factory=list,
    )

    tradeoffs: list[
        TradeoffItem
    ] = Field(
        default_factory=list,
    )

    risks: list[
        str
    ] = Field(
        default_factory=list,
    )

    evidence: dict[
        str,
        Any,
    ] = Field(
        default_factory=dict,
    )

    confidence: ConfidenceLevel = (
        ConfidenceLevel.MEDIUM
    )