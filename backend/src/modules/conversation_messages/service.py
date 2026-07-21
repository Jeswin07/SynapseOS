"""Conversation message service."""

from __future__ import annotations

import uuid

from src.modules.conversation_messages.repository import (
    ConversationMessageRepository,
)
from src.modules.conversation_messages.schemas import ChatMessage


class ConversationMessageService:
    """Service for conversation message operations."""

    def __init__(
        self,
        repository: ConversationMessageRepository,
    ):
        self.repository = repository

    async def add_user_message(
        self,
        *,
        conversation_id: uuid.UUID,
        content: str,
    ) -> None:
        """
        Save a user message.
        """

        await self.repository.add_message(
            conversation_id=conversation_id,
            role="user",
            content=content,
        )

    async def add_assistant_message(
        self,
        *,
        conversation_id: uuid.UUID,
        content: str,
    ) -> None:
        """
        Save an assistant message.
        """

        await self.repository.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=content,
        )

    async def history(
        self,
        *,
        conversation_id: uuid.UUID,
        limit: int = 20,
    ) -> list[ChatMessage]:
        """
        Return recent conversation history
        formatted for the LLM.
        """

        messages = await self.repository.get_recent_messages(
            conversation_id=conversation_id,
            limit=limit,
        )

        return [
            ChatMessage(
                role=message.role,
                content=message.content,
            )
            for message in messages
        ]