"""Shared enums for the AI Agent framework."""

from __future__ import annotations

from enum import StrEnum


class AgentType(StrEnum):
    """
    Supported AI agents within SynapseOS.
    """

    BUSINESS = "business"

    KNOWLEDGE = "knowledge"

    INTELLIGENCE = "intelligence"

    SCENARIO = "scenario"