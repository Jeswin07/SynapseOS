"""Shared models used by all AI agents."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class AgentMetadata(BaseModel):
    """
    Metadata describing an agent execution.
    """

    agent_name: str

    agent_type: str

    execution_time_ms: float = 0.0

    success: bool = True


class AgentInput(BaseModel):
    """
    Standard request passed to an AI agent.
    """

    query: str

    tenant_id: UUID

    user_id: UUID | None = None

    session_id: str | None = None

    conversation_id: str | None = None

    context: dict[str, Any] = Field(
        default_factory=dict,
    )

    metadata: dict = Field(
        default_factory=dict,
    )


class AgentOutput(BaseModel):
    """
    Standard response returned by an AI agent.
    """

    answer: str

    metadata: AgentMetadata | None = None

    data: dict[str, Any] = Field(
        default_factory=dict,
    )

    sources: list[dict[str, Any]] = Field(
        default_factory=list,
    )

    recommendations: list[str] = Field(
        default_factory=list,
    )