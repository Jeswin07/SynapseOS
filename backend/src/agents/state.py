"""Shared LangGraph state for SynapseOS AI orchestration."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from src.agents.models import AgentOutput
from src.agents.types import AgentType


class AgentState(BaseModel):
    """
    Shared state passed between LangGraph nodes.

    Every AI agent receives the current state, performs its task,
    updates the relevant fields, and returns the modified state.
    """

    # ------------------------------------------------------------------
    # User Information
    # ------------------------------------------------------------------

    tenant_id: UUID

    user_id: UUID | None = None

    session_id: str | None = None

    conversation_id: str | None = None

    # ------------------------------------------------------------------
    # User Query
    # ------------------------------------------------------------------

    query: str

    # ------------------------------------------------------------------
    # Conversation Context
    # ------------------------------------------------------------------

    context: dict[str, Any] = Field(
        default_factory=dict,
    )

    # ------------------------------------------------------------------
    # Execution Plan
    # ------------------------------------------------------------------

    execution_plan: list[AgentType] = Field(
        default_factory=list,
    )

    current_agent: AgentType | None = None

    completed_agents: list[AgentType] = Field(
        default_factory=list,
    )

    # ------------------------------------------------------------------
    # Agent Outputs
    # ------------------------------------------------------------------

    outputs: dict[AgentType, AgentOutput] = Field(
        default_factory=dict,
    )

    # ------------------------------------------------------------------
    # Final Response
    # ------------------------------------------------------------------

    final_output: AgentOutput | None = None