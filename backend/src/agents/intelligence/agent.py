"""Business intelligence agent."""

from __future__ import annotations

import logging

from src.agents.base import BaseAgent
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

logger = logging.getLogger(__name__)

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


    async def _execute(
        self,
        request: AgentInput,
    ) -> AgentOutput:
        """
        Execute intelligence workflow.
        """

        logger.info(
            "Intelligence Agent execution started | conversation_id=%s",
            request.conversation_id,
        )

        try:

            forced_tools = request.metadata.get(
                "forced_tools",
            )

            if forced_tools:

                logger.info(
                    "Using forced MCP tools from Scenario Agent"
                )

                class ForcedPlan:

                    def __init__(self, tools):
                        self.tools = tools

                    def model_dump(self):
                        return {
                            "tools": [
                                tool.value
                                for tool in self.tools
                            ],
                            "reasoning": "Forced by Scenario Agent.",
                        }

                plan = ForcedPlan(
                    forced_tools,
                )

            else:

                logger.info(
                    "Generating intelligence execution plan"
                )

                plan = await self.planner.plan(
                    request.query,
                )

                logger.info(
                    "Planner selected tools: %s",
                    [tool.value for tool in plan.tools],
                )


            results = {}

            logger.info(
                "Executing %d MCP tool(s)",
                len(plan.tools),
            )
            # Execute MCP tools
            for tool in plan.tools:

                logger.info(
                    "Executing MCP tool: %s",
                    tool.value,
                )

                response = await self.mcp.execute(
                    tool=tool,
                    tenant_id=request.tenant_id,
                    user_id=request.user_id,
                    query=request.query,
                    dataset_version_id=request.metadata.get(
                        "dataset_version_id",
                    ),
                )

                logger.info(
                    "Completed MCP tool: %s",
                    tool.value,
                )

                results[
                    tool.value
                ] = response.data.get(
                    tool.value,
                    response.data,
                )

            logger.info(
                "Intelligence Agent execution completed"
            )

            return AgentOutput(
                answer="",
                data={
                    "query": request.query,
                    "plan": plan.model_dump(),
                    "results": results,
                },
            )

        except Exception:
            logger.exception(
                "Intelligence Agent execution failed | conversation_id=%s",
                request.conversation_id,
            )
            raise