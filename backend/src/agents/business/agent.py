"""Business Agent implementation."""

from __future__ import annotations

from src.agents.base import BaseAgent

from src.agents.business.aggregator import (
    BusinessAggregator,
)

from src.agents.business.planner import (
    BusinessPlanner,
)

from src.agents.models import (
    AgentInput,
    AgentOutput,
)

from src.agents.registry import (
    AgentRegistry,
)

from src.agents.types import (
    AgentType,
)


class BusinessAgent(BaseAgent):
    """
    Supervisor agent responsible for
    orchestrating specialist agents.
    """


    def __init__(
        self,
        registry: AgentRegistry,
    ) -> None:

        super().__init__(
            agent_type=AgentType.BUSINESS,
            agent_name="Business Agent",
        )


        self.registry = registry

        self.planner = BusinessPlanner()

        self.aggregator = BusinessAggregator()


    async def _execute(
        self,
        request: AgentInput,
    ) -> AgentOutput:


        plan = await self.planner.plan(
            request.query,
        )


        outputs: dict[
            AgentType,
            AgentOutput,
        ] = {}


        for agent_type in plan.agents:


            agent = self.registry.get(
                agent_type,
            )


            response = await agent.invoke(
                request,
            )


            outputs[
                agent_type
            ] = response


        return self.aggregator.aggregate(
            outputs,
        )