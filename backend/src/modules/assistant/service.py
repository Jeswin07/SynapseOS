"""Business AI Assistant service."""

from __future__ import annotations

import asyncio
import json
from uuid import UUID

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.agents.models import AgentInput
from src.bootstrap.agents import create_business_agent
from src.modules.assistant.emitter import StreamEmitter
from src.modules.assistant.schemas import (
    AssistantChatRequest,
    AssistantChatResponse,
)
from src.modules.conversation_messages.repository import (
    ConversationMessageRepository,
)
from src.modules.conversation_messages.schemas import ChatMessage
from src.modules.conversation_messages.service import (
    ConversationMessageService,
)
from src.modules.conversations.repository import (
    ConversationRepository,
)


class AssistantService:
    """
    Entry point for user interaction with SynapseOS AI.
    """

    def __init__(self, db: Session) -> None:

        self.db = db

        self.agent = create_business_agent(db,)

    async def chat(
        self,
        request: AssistantChatRequest,
        tenant_id: UUID,
        user_id: UUID,
    ) -> AssistantChatResponse:

        conversation = await ConversationRepository(
            self.db,
        ).get(request.conversation_id)

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found.",
            )
        
        message_service = ConversationMessageService(
            ConversationMessageRepository(self.db)
        )

        history = await message_service.history(
            conversation_id=conversation.id,
            limit=20,
        )

        history.append(
            ChatMessage(
                role="user",
                content=request.message,
            )
        )

        response = await self.agent.invoke(
            AgentInput(
                query=request.message,
                history=history,
                tenant_id=tenant_id,
                user_id=user_id,
                conversation_id=conversation.id,
                metadata={
                    **request.metadata,
                    "dataset_version_id": str(
                        conversation.dataset_version_id
                    ),
                },
            )
        )

        await message_service.add_user_message(
            conversation_id=conversation.id,
            content=request.message,
        )

        await message_service.add_assistant_message(
            conversation_id=conversation.id,
            content=response.answer,
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

        conversation = await ConversationRepository(
            self.db,
        ).get(request.conversation_id)

        if conversation is None:
            raise ValueError("Conversation not found.")
        
        message_service = ConversationMessageService(
            ConversationMessageRepository(self.db)
        )

        history = await message_service.history(
            conversation_id=conversation.id,
        )

        history.append(
            ChatMessage(
                role="user",
                content=request.message,
            )
        )

        response_task = asyncio.create_task(
            self.agent.invoke(
                AgentInput(
                    query=request.message,
                    history=history,
                    tenant_id=tenant_id,
                    user_id=user_id,
                    conversation_id=conversation.id,
                    metadata={
                        **request.metadata,
                        "dataset_version_id": str(
                            conversation.dataset_version_id
                        ),
                    },
                ),
                emitter=emitter,
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

        await message_service.add_user_message(
            conversation_id=conversation.id,
            content=request.message,
        )

        await message_service.add_assistant_message(
            conversation_id=conversation.id,
            content=response.answer,
        )

        payload = {
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

        yield (
            "data: "
            + json.dumps(jsonable_encoder(payload))
            + "\n\n"
        )