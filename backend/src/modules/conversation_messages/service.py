"""Conversation message service."""

from __future__ import annotations

import logging
import uuid

from src.modules.conversation_messages.repository import (
    ConversationMessageRepository,
)
from src.modules.conversation_messages.schemas import ChatMessage

logger = logging.getLogger(__name__)

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

        logger.info(
            "User message received | conversation_id=%s",
            conversation_id,
        )

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

        logger.info(
            "Assistant message generated | conversation_id=%s",
            conversation_id,
        )

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

        logger.info(
            "Conversation history requested | conversation_id=%s",
            conversation_id,
        )

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