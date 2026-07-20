"""Conversation schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreateRequest(BaseModel):
    """Request schema for creating a conversation."""

    dataset_version_id: uuid.UUID
    title: str = Field(default="New Conversation", max_length=255)


class ConversationUpdateRequest(BaseModel):
    """Request schema for updating a conversation."""

    title: str = Field(..., max_length=255)


class ConversationResponse(BaseModel):
    """Conversation response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    user_id: uuid.UUID
    dataset_version_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime