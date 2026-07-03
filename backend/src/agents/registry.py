"""Registry for AI agents."""

from __future__ import annotations

from src.agents.base import BaseAgent
from src.agents.exceptions import (
    AgentNotRegisteredError,
)
from src.agents.types import AgentType


class AgentRegistry:
    """
    Stores all registered AI agents.

    The Business Agent uses the registry to locate
    specialized agents at runtime.
    """

    def __init__(self) -> None:

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
        """
        Returns a registered AI agent.

        Raises:
            AgentNotRegisteredError:
                If the requested agent has not been registered.
        """

        agent = self._agents.get(agent_type)

        if agent is None:
            raise AgentNotRegisteredError(
                (
                    f"Agent '{agent_type.value}' "
                    "has not been registered."
                ),
            )

        return agent

    def exists(
        self,
        agent_type: AgentType,
    ) -> bool:

        return agent_type in self._agents