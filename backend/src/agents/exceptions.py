"""Exceptions used by the AI Agent framework."""

from __future__ import annotations


class AgentError(Exception):
    """Base exception for all agent errors."""


class AgentNotRegisteredError(AgentError):
    """Raised when an agent has not been registered."""