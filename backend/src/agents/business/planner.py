"""LLM based business agent planner."""

from __future__ import annotations

import json

from src.agents.business.models import (
    ExecutionPlan,
)

from src.agents.common.llm import (
    LLMClient,
)

from src.agents.types import (
    AgentType,
)
from src.agents.common.json_parser import (
    parse_llm_json,
)


class BusinessPlanner:
    """
    Uses LLM reasoning to select specialist agents.
    """


    def __init__(
        self,
    ) -> None:

        self.llm = LLMClient()


    async def plan(
        self,
        query: str,
    ) -> ExecutionPlan:
        """
        Create agent execution plan.
        """


        prompt = f"""
You are SynapseOS Business Orchestrator.

Your job:
Select which AI agents should answer the user.

Available agents:

knowledge:
Use for:
- uploaded documents
- company policies
- contracts
- manuals
- document Q&A


intelligence:
Use for:
- business analytics
- revenue
- sales
- customers
- products
- reviews
- operations
- KPIs
- forecasting
- predictions


scenario:
Use for:
- simulations
- what-if analysis
- business impact analysis


User request:

{query}


Return ONLY JSON.

Example:

{{
 "agents":["intelligence"],
 "parallel":false,
 "reasoning":"Requires business metrics."
}}
"""


        response = await self.llm.generate(
            prompt,
        )
        
        print(response)

        data = parse_llm_json(
            response,
        )


        return ExecutionPlan(
            agents=[
                AgentType(agent)
                for agent in data[
                    "agents"
                ]
            ],
            parallel=data.get(
                "parallel",
                False,
            ),
            reasoning=data.get(
                "reasoning",
            ),
        )