"""LangGraph state models."""

from __future__ import annotations

from typing import Any, TypedDict

from src.agents.models import (
    AgentInput,
    AgentOutput,
)
from src.agents.types import (
    AgentType,
)


class BusinessGraphState(TypedDict):
    """
    Shared state between graph nodes.
    """

    request: AgentInput

    selected_agents: list[AgentType]

    planner_reason: str | None

    outputs: dict[
        AgentType,
        AgentOutput,
    ]

    final_response: AgentOutput | None

    execution: dict[str, Any]