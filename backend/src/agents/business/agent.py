"""Business Agent implementation."""

from __future__ import annotations

from src.agents.base import BaseAgent
from src.agents.business.aggregator import BusinessAggregator
from src.agents.business.planner import BusinessPlanner
from src.agents.models import (
    AgentInput,
    AgentOutput,
)
from src.agents.registry import AgentRegistry
from src.agents.types import AgentType
from src.orchestration.executor import WorkflowExecutor


class BusinessAgent(BaseAgent):
    """
    Supervisor agent responsible for orchestrating
    enterprise AI workflows.

    Responsibilities
    ----------------

    - Understand user requests
    - Create execution plans
    - Coordinate specialized agents
    - Aggregate responses
    """

    def __init__(
        self,
        registry: AgentRegistry,
    ) -> None:

        super().__init__(
            agent_type=AgentType.BUSINESS,
            agent_name="Business Agent",
        )

        self.planner = BusinessPlanner()

        self.executor = WorkflowExecutor(
            registry,
        )

        self.aggregator = BusinessAggregator()

    async def _execute(
        self,
        request: AgentInput,
    ) -> AgentOutput:
        """
        Executes an enterprise AI workflow.
        """

        plan = self.planner.plan(
            request.query,
        )

        outputs = await self.executor.execute(
            plan,
            request,
        )

        return self.aggregator.aggregate(
            outputs,
        )