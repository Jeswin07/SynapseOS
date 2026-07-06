"""Schemas for Business AI Assistant."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class AssistantChatRequest(BaseModel):
    """
    User request to the Business AI Assistant.
    """

    message: str

    metadata: dict = Field(
        default_factory=dict,
    )


class AssistantChatResponse(BaseModel):
    """
    Unified AI assistant response.
    """

    answer: str

    sources: list[dict[str, Any]] = Field(
        default_factory=list,
    )

    recommendations: list[str] = Field(
        default_factory=list,
    )

    data: dict[str, Any] = Field(
        default_factory=dict,
    )

    agent: str | None = None

    tenant_id: UUID | None = None