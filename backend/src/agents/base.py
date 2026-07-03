"""Base class for all SynapseOS AI agents."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod

from src.agents.models import (
    AgentInput,
    AgentMetadata,
    AgentOutput,
)
from src.agents.types import AgentType


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.

    Every agent follows the same lifecycle:

        invoke()
            ↓
        validate()
            ↓
        _execute()
            ↓
        AgentOutput

    Child classes only implement `_execute()`.
    """

    agent_type: AgentType

    agent_name: str

    def __init__(
        self,
        agent_type: AgentType,
        agent_name: str,
    ) -> None:
        self.agent_type = agent_type
        self.agent_name = agent_name

    async def invoke(
        self,
        request: AgentInput,
    ) -> AgentOutput:
        """
        Executes the agent lifecycle.
        """

        self.validate(request)

        start = time.perf_counter()

        response = await self._execute(request)

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        response.metadata = AgentMetadata(
            agent_name=self.agent_name,
            agent_type=self.agent_type.value,
            execution_time_ms=round(
                elapsed,
                2,
            ),
            success=True,
        )

        return response

    def validate(
        self,
        request: AgentInput,
    ) -> None:
        """
        Validates the incoming request.

        Child classes may override this if additional
        validation is required.
        """

        if not request.query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

    @abstractmethod
    async def _execute(
        self,
        request: AgentInput,
    ) -> AgentOutput:
        """
        Executes the agent-specific business logic.
        """