"""Business intelligence agent."""

from __future__ import annotations

from src.agents.base import BaseAgent

from src.agents.intelligence.aggregator import (
    IntelligenceAggregator,
)

from src.agents.intelligence.planner import (
    IntelligencePlanner,
)

from src.agents.models import (
    AgentInput,
    AgentOutput,
)

from src.agents.types import AgentType

from src.mcp.service import (
    MCPService,
)


class IntelligenceAgent(BaseAgent):
    """
    Agent responsible for enterprise intelligence.

    Responsibilities:
    - Analytics
    - Forecasting
    - ML insights
    - Risk detection
    """

    def __init__(
        self,
        mcp: MCPService,
    ) -> None:

        super().__init__(
            agent_type=AgentType.INTELLIGENCE,
            agent_name="Intelligence Agent",
        )

        self.mcp = mcp

        self.planner = IntelligencePlanner()

        self.aggregator = IntelligenceAggregator()


    async def _execute(
        self,
        request: AgentInput,
    ) -> AgentOutput:
        """
        Execute intelligence workflow.
        """


        # LLM decides required tools
        plan = await self.planner.plan(
            request.query,
        )


        results = {}


        # Execute MCP tools
        for tool in plan.tools:

            response = await self.mcp.execute(
                tool=tool,
                tenant_id=request.tenant_id,
                dataset_version_id=request.metadata.get(
                    "dataset_version_id",
                ),
            )


            results[
                tool.value
            ] = response.data.get(
                tool.value,
                response.data,
            )


        # Generate final intelligence answer
        answer = await self.aggregator.aggregate(
            query=request.query,
            plan=plan,
            results=results,
        )


        return AgentOutput(
            answer=answer,
            data=results,
        )