"""Conversation service."""

from __future__ import annotations

import logging
import uuid

from fastapi import HTTPException, status

from src.models.conversation import Conversation
from src.modules.conversations.repository import ConversationRepository
from src.modules.conversations.schemas import (
    ConversationCreateRequest,
    ConversationUpdateRequest,
)

logger = logging.getLogger(__name__)

class ConversationService:
    """Service for conversation operations."""

    def __init__(self, repository: ConversationRepository):
        self.repository = repository

    async def create(
        self,
        *,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
        request: ConversationCreateRequest,
    ) -> Conversation:

        logger.info(
            "Conversation creation requested | tenant_id=%s user_id=%s",
            tenant_id,
            user_id,
        )

        try:
            return await self.repository.create(
                tenant_id=tenant_id,
                user_id=user_id,
                dataset_version_id=request.dataset_version_id,
                title=request.title,
            )
        except Exception:
            logger.exception(
                "Conversation retrieval failed"
            )
            raise

    async def get(
        self,
        *,
        conversation_id: uuid.UUID,
    ) -> Conversation:

        try:
            conversation = await self.repository.get(conversation_id)

            if conversation is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found.",
                )

            return conversation
        
        except Exception:
            logger.exception(
                "Conversation retrieval failed | conversation_id=%s",
                conversation_id,
            )
            raise



    async def list(
        self,
        *,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> list[Conversation]:

        logger.info(
            "Conversation list requested | user_id=%s",
            user_id,
        )

        try:
            result = await self.repository.list_by_user(
                tenant_id=tenant_id,
                user_id=user_id,
            )

        except Exception:
            logger.exception(
                "Conversation listing failed | user_id=%s",
                user_id,
            )
            raise

        return result

    async def update(
        self,
        *,
        conversation_id: uuid.UUID,
        request: ConversationUpdateRequest,
    ) -> Conversation:

        logger.info(
            "Conversation update requested | conversation_id=%s",
            conversation_id,
        )

        try:
            conversation = await self.get(
                conversation_id=conversation_id,
            )

            result =  await self.repository.update_title(
                conversation,
                request.title,
            )
        except Exception:
            logger.exception(
                "Conversation update failed | conversation_id=%s",
                conversation_id,
            )
            raise

        return result         

    async def delete(
        self,
        *,
        conversation_id: uuid.UUID,
    ) -> None:

        logger.info(
            "Conversation deletion requested | conversation_id=%s",
            conversation_id,
        )

        try:
            conversation = await self.get(
                conversation_id=conversation_id,
            )

            await self.repository.delete(conversation)

        except Exception:
            logger.exception(
                "Conversation deletion failed | conversation_id=%s",
                conversation_id,
            )
            raise