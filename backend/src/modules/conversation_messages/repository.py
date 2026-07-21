"""Conversation message repository."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.conversation_message import ConversationMessage


class ConversationMessageRepository:
    """Repository for ConversationMessage operations."""

    def __init__(self, session: Session):
        self.session = session

    async def add_message(
        self,
        *,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
    ) -> ConversationMessage:
        """
        Store a conversation message.
        """

        message = ConversationMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)

        return message

    async def get_recent_messages(
        self,
        *,
        conversation_id: uuid.UUID,
        limit: int = 20,
    ) -> list[ConversationMessage]:
        """
        Retrieve the latest conversation messages.

        Returned in chronological order.
        """

        result = self.session.execute(
            select(ConversationMessage)
            .where(
                ConversationMessage.conversation_id == conversation_id
            )
            .order_by(
                ConversationMessage.created_at.desc()
            )
            .limit(limit)
        )

        messages = list(result.scalars().all())

        messages.reverse()

        return messages

    async def delete_by_conversation(
        self,
        *,
        conversation_id: uuid.UUID,
    ) -> None:
        """
        Delete all messages belonging to a conversation.
        """

        result = self.session.execute(
            select(ConversationMessage).where(
                ConversationMessage.conversation_id == conversation_id
            )
        )

        messages = result.scalars().all()

        for message in messages:
            self.session.delete(message)

        self.session.commit()