"""Business Agent using LangGraph."""

from __future__ import annotations

import logging
import time

from src.agents.base import BaseAgent
from src.agents.business.executive_response import (
    ExecutiveResponseGenerator,
)
from src.agents.business.fallback import BusinessFallback
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
from src.graphs.state import BusinessGraphState
from src.graphs.workflow import (
    create_business_graph,
)
from src.modules.assistant.emitter import StreamEmitter

logger = logging.getLogger(__name__)

class BusinessAgent(BaseAgent):

    def __init__(
        self,
        registry: AgentRegistry,
    ) -> None:

        super().__init__(
            agent_type=AgentType.BUSINESS,
            agent_name="Business Agent",
        )

        self.registry = registry

        self.executive = (
            ExecutiveResponseGenerator()
        )
        

    async def _execute(
        self,
        request: AgentInput,
        emitter: StreamEmitter | None = None,
    ) -> AgentOutput:

        start = time.perf_counter()

        logger.info(
            "Business Agent execution started | conversation_id=%s",
            request.conversation_id,
        )
        try:
            graph = create_business_graph(
                registry=self.registry,
                emitter=emitter,
            )

            logger.info(
                "Business LangGraph workflow created"
            )

            initial_state: BusinessGraphState = {
                "request": request,
                "selected_agents": [],
                "outputs": {},
                "planner_reason": "",
                "final_response": None,
                "execution": {},
            }

            logger.info(
                "Executing Business LangGraph workflow"
            )

            graph_result = await graph.ainvoke(
                initial_state
            )

            logger.info(
                "Workflow execution completed"
            )

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            selected = graph_result["selected_agents"]

            logger.info(
                "Planner selected agents: %s",
                selected,
            )

            if not selected:
                logger.warning(
                    "Planner did not select any specialized agent"
                )

                reason = graph_result["planner_reason"]

                if reason == "Greeting.":
                    logger.info(
                        "Returning greeting response"
                    )
                    response = BusinessFallback.greeting()
                else:
                    logger.info(
                        "Returning fallback response"
                    )
                    response = BusinessFallback.invalid()

                response.data = {
                    "execution": {
                        "total_time_ms": round(elapsed, 2),
                        "agents_executed": [],
                    }
                }

                return response

            merged_response = graph_result[
                "final_response"
            ]

            if not graph_result["selected_agents"]:
                merged_response.data["execution"] = {
                    "total_time_ms": round(elapsed, 2),
                    "agents_executed": [],
                }
                return merged_response

            logger.info(
                "Generating executive response"
            )

            final_response = (
                await self.executive.generate(
                    query=request.query,
                    history=request.history,
                    response=merged_response,
                )
            )

            logger.info(
                "Executive response generated"
            )

            final_response.data["execution"] = {
                "total_time_ms": round(elapsed, 2),
                "agents_executed": graph_result["selected_agents"],
            }

            logger.info(
                "Business Agent completed | execution_time_ms=%.2f agents=%s",
                elapsed,
                graph_result["selected_agents"],
            )

            return final_response

        except Exception:
            logger.exception(
                "Business Agent execution failed | conversation_id=%s",
                request.conversation_id,
            )
            raise