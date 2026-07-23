"""Executive response generator."""

from __future__ import annotations

import json
import logging

from src.agents.business.executive_evidence_builder import (
    ExecutiveEvidenceBuilder,
)
from src.agents.common.llm import LLMClient
from src.agents.models import AgentOutput
from src.modules.conversation_messages.schemas import ChatMessage

logger = logging.getLogger(__name__)

class ExecutiveResponseGenerator:
    """
    Converts structured outputs from all business agents
    into a single executive-level response.

    This is the ONLY LLM call made by the Business Agent.
    """

    def __init__(self) -> None:

        self.llm = LLMClient()

        self.builder = ExecutiveEvidenceBuilder()

    async def generate(
        self,
        *,
        query: str,
        history: list[ChatMessage],
        response: AgentOutput,
    ) -> AgentOutput:

        try:
            logger.info("Executive response generation started")

            evidence = self.builder.build(
                response,
            )

            logger.info(
                "Executive evidence prepared"
            )

            history_text = ""

            if history:

                history_text = "\n\n".join(
                f"{msg.role.upper()}:\n{msg.content}"
                for msg in history
            )

            payload = json.dumps(
                evidence,
                indent=2,
                default=str,
            )

            prompt = f"""
    You are SynapseOS Executive AI.

    You are the FINAL executive reasoning layer.

    The specialist agents have already completed their work.

    Your responsibility is NOT to calculate analytics,
    predict values,
    or simulate scenarios.

    Those tasks are already complete.

    Your ONLY responsibility is to synthesize all available evidence
    into an executive-level business briefing.

    ==========================================================

    USER CONVERSATION

    {history_text}

    ==================================================

    CURRENT USER QUESTION

    {query}

    ==================================================

    BUSINESS EVIDENCE

    {payload}

    ==========================================================

    STRICT RULES

    Use ONLY the supplied evidence.

    Never invent numbers.

    Never invent KPIs.

    Never invent recommendations.

    Never assume missing information.

    Never infer missing business evidence.

    Every recommendation must be supported by the supplied evidence.

    Never mention:

    - JSON
    - agents
    - LLM
    - simulation engine
    - internal reasoning
    - business planner

    If every evidence section is empty,
    state that there is insufficient evidence.

    If at least one evidence section exists,
    base the response ONLY on that evidence.

    If the current question depends on previous conversation,
    use the supplied conversation history.

    If the current question introduces a new topic,
    focus primarily on the current question.

    Do not invent previous conversation.

    If conversation history is empty,
    answer only from the current question.

    Never say there is insufficient evidence simply because some evidence types are unavailable.

    Do NOT fabricate anything.

    ==========================================================

    PRIORITY ORDER

    When producing your answer, prioritize:
    Generate only the sections that are supported by the available evidence.

    1. Executive Summary

    2. Business Decision

    3. Key Findings

    4. Strategic Insights

    5. Business Risks

    6. Business Opportunities

    7. Recommendations

    8. Next Actions

    9. Confidence

    Do not fabricate content to fill a section.

    Maximum 500 words.
    ==========================================================

    IF KNOWLEDGE EXISTS

    Use enterprise documents only when relevant.

    Never repeat document text.

    Summarize the business meaning.

    ==========================================================

    IF ANALYTICS EXISTS

    Focus on

    • KPIs

    • Trends

    • Operational performance

    • Customer behaviour

    Explain what matters.

    Not every metric.

    ==========================================================

    IF FORECAST EXISTS

    Explain

    • expected future

    • business impact

    • uncertainty

    ==========================================================

    IF PREDICTION EXISTS

    Explain

    • predicted outcome

    • business impact

    • affected entities

    ==========================================================

    IF RISK EXISTS

    Explain

    • severity

    • financial impact

    • mitigation

    ==========================================================

    IF SCENARIO EXISTS

    Treat the scenario output as the highest-priority strategic evidence.

    Explain:

    • executive decision

    • reasoning

    • trade-offs

    • expected business impact

    • risks

    • opportunities

    Do NOT repeat the simulation values unnecessarily.

    Explain what they mean.

    ==========================================================

    STYLE

    Write like an executive consultant.

    Clear.

    Confident.

    Business-oriented.

    No fluff.

    No repetition.

    Short paragraphs.

    Use headings.

    ==========================================================

    OUTPUT

    Generate ONLY the sections supported by the available evidence.

    Possible sections:

    # Executive Summary

    # Business Decision

    # Key Findings

    # Strategic Insights

    # Risks

    # Opportunities

    # Recommendations

    # Next Actions

    # Confidence

    Do not create empty headings.

    Do not invent risks.

    Do not invent opportunities.

    Do not invent recommendations.

    STYLE

    Return VALID GitHub Markdown.

    VERY IMPORTANT:

    - Every heading MUST begin with Markdown heading syntax.
    - Use exactly:

    # Executive Summary

    ## Key Findings

    ## Strategic Insights

    ## Business Risks

    ## Recommendations

    ## Confidence

    - Leave one blank line after every heading.
    - Use bullet lists instead of long paragraphs.
    - Bold all important numbers and KPIs.
    - Maximum 250 words.
    - Never output plain text headings.
    - Never output HTML.

    Maximum 450 words.
    """


            logger.info(
                "Generating executive response using LLM"
            )

            answer = await self.llm.generate(
                prompt,
            )

            logger.info(
                "Executive response generated successfully"
            )

            response.answer = answer

            return response

        except Exception:
            logger.exception(
                "Executive response generation failed"
            )
            raise