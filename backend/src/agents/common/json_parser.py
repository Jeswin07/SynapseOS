"""Utilities for parsing LLM JSON responses."""

from __future__ import annotations

import json
import re
from typing import Any


def parse_llm_json(
    text: str,
) -> dict[str, Any]:
    """
    Extract JSON object from LLM output.
    """


    text = text.strip()


    # remove markdown json fences
    text = (
        text.replace(
            "```json",
            "",
        )
        .replace(
            "```",
            "",
        )
        .strip()
    )


    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL,
    )


    if match is None:

        raise ValueError(
            f"No JSON found in LLM response: {text}"
        )


    return json.loads(
        match.group(),
    )