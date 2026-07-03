"""Execution engine for AI agent workflows."""

from __future__ import annotations

import asyncio

from src.agents.business.models import ExecutionPlan
from src.agents.models import (
    AgentInput,
    AgentOutput,
)
from src.agents.registry import AgentRegistry
from src.agents.types import AgentType


class WorkflowExecutor:
    """
    Executes execution plans produced by the Business Planner.

    Supports both sequential and parallel execution.
    """

    def __init__(
        self,
        registry: AgentRegistry,
    ) -> None:
        self.registry = registry

    async def execute(
        self,
        plan: ExecutionPlan,
        request: AgentInput,
    ) -> dict[AgentType, AgentOutput]:
        """
        Executes the supplied execution plan.
        """

        if plan.parallel:
            return await self._execute_parallel(
                plan,
                request,
            )

        return await self._execute_sequential(
            plan,
            request,
        )

    async def _execute_sequential(
        self,
        plan: ExecutionPlan,
        request: AgentInput,
    ) -> dict[AgentType, AgentOutput]:

        outputs: dict[
            AgentType,
            AgentOutput,
        ] = {}

        for agent_type in plan.agents:

            agent = self.registry.get(agent_type)

            outputs[agent_type] = await agent.invoke(
                request,
            )

        return outputs

    async def _execute_parallel(
        self,
        plan: ExecutionPlan,
        request: AgentInput,
    ) -> dict[AgentType, AgentOutput]:

        agents = [
            (
                agent_type,
                self.registry.get(agent_type),
            )
            for agent_type in plan.agents
        ]

        responses = await asyncio.gather(
            *[
                agent.invoke(request)
                for _, agent in agents
            ]
        )

        return {
            agent_type: response
            for (
                agent_type,
                _,
            ), response in zip(
                agents,
                responses,
                strict=True,
            )
        }