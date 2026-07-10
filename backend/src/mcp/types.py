"""MCP types."""

from enum import Enum


class MCPTool(
    Enum,
):

    KNOWLEDGE_SEARCH = "knowledge_search"

    ANALYTICS = "analytics"

    FORECAST = "forecast"

    PREDICTION = "prediction"

    RISK = "risk"