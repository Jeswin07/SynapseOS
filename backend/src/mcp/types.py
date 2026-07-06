"""Shared enums for the MCP layer."""

from __future__ import annotations

from enum import StrEnum


class MCPTool(StrEnum):
    """
    Supported MCP tools exposed by SynapseOS.
    """

    KNOWLEDGE_SEARCH = "knowledge.search"

    ANALYTICS_SUMMARY = "analytics.summary"

    ML_TRAIN = "ml.train"

    ML_PREDICT = "ml.predict"

    ML_EXPLAIN = "ml.explain"

    FORECAST_GENERATE = "forecast.generate"

    RISK_ANALYZE = "risk.analyze"

    ANALYTICS = "analytics"

    KNOWLEDGE = "knowledge"

    FORECAST = "forecast"