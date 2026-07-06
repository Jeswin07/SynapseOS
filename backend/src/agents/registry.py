"""Agent registry."""

from __future__ import annotations

from src.agents.base import BaseAgent
from src.agents.exceptions import (
    AgentNotRegisteredError,
)
from src.agents.types import AgentType


class AgentRegistry:
    """
    Registry containing available agents.
    """

    def __init__(
        self,
    ) -> None:

        self._agents: dict[
            AgentType,
            BaseAgent,
        ] = {}


    def register(
        self,
        agent: BaseAgent,
    ) -> None:

        self._agents[
            agent.agent_type
        ] = agent


    def get(
        self,
        agent_type: AgentType,
    ) -> BaseAgent:

        if agent_type not in self._agents:

            raise AgentNotRegisteredError(
                f"Agent '{agent_type.value}' "
                "has not been registered."
            )

        return self._agents[
            agent_type
        ]