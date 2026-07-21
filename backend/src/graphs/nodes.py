"""LangGraph workflow nodes."""

from __future__ import annotations

import asyncio
import time

from src.agents.business.aggregator import (
    BusinessAggregator,
)
from src.agents.business.planner import (
    BusinessPlanner,
)
from src.agents.registry import (
    AgentRegistry,
)
from src.agents.types import AgentType
from src.graphs.state import (
    BusinessGraphState,
)
from src.modules.assistant.emitter import StreamEmitter
from src.modules.assistant.events import (
    StreamEvent,
    StreamEventType,
)


class BusinessGraphNodes:
    """
    Nodes executed by LangGraph.
    """


    def __init__(
        self,
        registry: AgentRegistry,
        emitter: StreamEmitter | None = None,
    ):
        self.registry = registry

        self.planner = BusinessPlanner()

        self.aggregator = BusinessAggregator()

        self.emitter = emitter


    async def supervisor(
        self,
        state: BusinessGraphState,
    ) -> BusinessGraphState:

        if self.emitter:

            await self.emitter.emit(
                StreamEvent(
                    type=StreamEventType.STATUS,
                    message="Planning request...",
                )
            )
        
        state["execution"] = {
            "start": time.perf_counter(),
        }


        plan = await self.planner.plan(
            state["request"].query,
            history=state["request"].history,
        )

        print(
            f"[Supervisor] Routed -> {len(plan.agents)} agent(s)"
        )


        state["selected_agents"] = (
            plan.agents
        )

        if self.emitter:

            await self.emitter.emit(
                StreamEvent(
                    type=StreamEventType.STATUS,
                    message=f"Planner selected {len(plan.agents)} agent(s).",
                )
            )

        state["planner_reason"] = plan.reasoning

        return state


    async def execute_agents(
        self,
        state: BusinessGraphState,
    ) -> BusinessGraphState:
        """
        Execute all selected agents concurrently.
        """

        async def run_agent(agent_type: AgentType):

            start = time.perf_counter()

            print(f"[{agent_type.value}] Started")

            agent = self.registry.get(agent_type)

            if self.emitter:

                await self.emitter.emit(
                    StreamEvent(
                        type=StreamEventType.AGENT_STARTED,
                        agent=agent_type.value,
                        message=f"{agent_type.value.title()} Agent started.",
                    )
                )

            response = await agent.invoke(
                state["request"],
            )

            if self.emitter:

                await self.emitter.emit(
                    StreamEvent(
                        type=StreamEventType.AGENT_COMPLETED,
                        agent=agent_type.value,
                        message=f"{agent_type.value.title()} Agent completed.",
                    )
                )

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            print(
                f"[{agent_type.value}] ✓ {elapsed:.0f} ms"
            )

            return agent_type, response

        results = await asyncio.gather(
            *[
                run_agent(agent_type)
                for agent_type in state["selected_agents"]
            ]
        )

        state["outputs"] = {
            agent_type: response
            for agent_type, response in results
        }

        return state


    async def respond(
        self,
        state: BusinessGraphState,
    ) -> BusinessGraphState:

        if self.emitter:

            await self.emitter.emit(
                StreamEvent(
                    type=StreamEventType.STATUS,
                    message="Preparing executive response...",
                )
            )

        response = self.aggregator.aggregate(
            state["outputs"],
        )

        state["final_response"] = response

        if self.emitter:

            await self.emitter.emit(
                StreamEvent(
                    type=StreamEventType.COMPLETE,
                    message="Workflow completed.",
                )
            )

        total = (
            time.perf_counter()
            - state["execution"]["start"]
        )

        print(
            f"[Business Graph] Completed in {total:.2f}s"
        )

        return state

    def route(
        self,
        state: BusinessGraphState,
    ) -> str:
        """
        Decide the next node after planning.
        """

        if state["selected_agents"]:
            return "agents"

        return "response"