"""Business AI Assistant service."""

from __future__ import annotations
import json
import asyncio
from uuid import UUID

from sqlalchemy.orm import Session
from src.modules.assistant.emitter import StreamEmitter
from src.agents.models import AgentInput
from src.bootstrap.agents import create_business_agent
from src.modules.assistant.schemas import (
    AssistantChatRequest,
    AssistantChatResponse,
)


class AssistantService:
    """
    Entry point for user interaction with SynapseOS AI.
    """

    def __init__(self, db: Session) -> None:

        self.agent = create_business_agent(db,)

    async def chat(
        self,
        request: AssistantChatRequest,
        tenant_id: UUID,
        user_id: UUID,
    ) -> AssistantChatResponse:

        response = await self.agent.invoke(
            AgentInput(
                query=request.message,
                tenant_id=tenant_id,
                user_id=user_id,
                metadata=request.metadata,
            ),
        )

        return AssistantChatResponse(
            answer=response.answer,
            sources=response.sources,
            recommendations=response.recommendations,
            data=response.data,
            tenant_id=tenant_id,
            agent=(
                response.metadata.agent_name
                if response.metadata
                else None
            ),
        )

    
    async def chat_stream(
        self,
        request: AssistantChatRequest,
        tenant_id: UUID,
        user_id: UUID,
    ):
        """
        Stream assistant progress using
        Server-Sent Events (SSE).
        """
        emitter = StreamEmitter()

        response_task = asyncio.create_task(
            self.agent.invoke(
                AgentInput(
                    query=request.message,
                    tenant_id=tenant_id,
                    user_id=user_id,
                    metadata=request.metadata,
                ),
                emitter=emitter
            )
        )

        async for event in emitter.stream():

            yield (
                "data: "
                + event.model_dump_json()
                + "\n\n"
            )

            if event.type.value == "complete":
                break

        response = await response_task

        yield (
            "data: "
            + json.dumps(
                {
                    "type": "final",
                    "response": {
                        "answer": response.answer,
                        "sources": response.sources,
                        "recommendations": response.recommendations,
                        "data": response.data,
                        "agent": (
                            response.metadata.agent_name
                            if response.metadata
                            else None
                        ),
                        "tenant_id": str(tenant_id),
                    },
                }
            )
            + "\n\n"
        )