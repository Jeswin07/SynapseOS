"""Hybrid business agent planner."""

from __future__ import annotations

from src.agents.business.models import ExecutionPlan
from src.agents.common.json_parser import parse_llm_json
from src.agents.common.llm import LLMClient
from src.agents.types import AgentType
from src.modules.conversation_messages.schemas import ChatMessage


class BusinessPlanner:
    """
    Fast deterministic routing with LLM fallback.
    """

    def __init__(self) -> None:
        self.llm = LLMClient()


    async def plan(
        self,
        query: str,
        history: list[ChatMessage] | None = None,
    ) -> ExecutionPlan:

        query_lower = query.lower().strip()

        history = history or []


        FOLLOW_UP_WORDS = {
            "only",
            "also",
            "compare",
            "same",
            "those",
            "them",
            "it",
            "that",
            "these",
            "top",
            "bottom",
            "last",
            "previous",
            "next",
            "before",
            "after",
            "today",
            "yesterday",
        }


        # -------------------------
    # Greeting Detection
    # -------------------------

        greetings = [
            "hi",
            "hello",
            "hey",
           "good morning",
            "good afternoon",
            "good evening",
            "thanks",
            "thank you",
            "bye",
        ]

        if query_lower in greetings:
            return ExecutionPlan(
                agents=[],
                parallel=False,
                reasoning="Greeting.",
            )

    # -------------------------
    # Capability Keywords
    # -------------------------

        knowledge_keywords = [
            "document",
            "documents",
            "policy",
            "policies",
            "contract",
            "contracts",
            "manual",
            "manuals",
            "sop",
            "procedure",
            "knowledge",
            "knowledge base",
            "pdf",
            "file",
            "enterprise",
            "according to",
            "based on our documents",
            "handbook",
            "guideline",
            "company policy",
        ]

        STRATEGIC_KEYWORDS = [
            "should",
            "recommend",
            "recommendation",
            "strategy",
            "strategic",
            "focus",
            "priority",
            "prioritize",
            "decision",
            "decide",
            "next quarter",
            "next year",
            "improve",
            "optimize",
            "opportunity",
            "risk",
        ]

        intelligence_keywords = [
            "sales",
            "revenue",
            "profit",
            "income",
            "customer",
            "customers",
            "seller",
            "product",
            "products",
            "analytics",
            "dashboard",
            "kpi",
            "metric",
            "metrics",
            "performance",
            "forecast",
            "forecasting",
            "predict",
            "prediction",
            "trend",
            "growth",
            "risk",
            "orders",
            "delivery",
            "inventory",
            "margin",
            "cost",
            "expense",
            "finance",
            "business",
        ]

        decision_terms = [
            "should",
            "recommend",
            "recommendation",
            "strategy",
            "strategic",
            "decision",
            "focus",
            "focus on",
            "prioritize",
            "best",
            "best option",
            "improve",
            "optimization",
            "optimize",
            "increase",
            "decrease",
            "reduce",
            "simulate",
            "simulation",
            "what if",
            "what-if",
            "impact",
            "effect",
            "tradeoff",
            "trade-off",
            "next quarter",
        ]

        business_terms = [
            "sales",
            "revenue",
            "profit",
            "customer",
            "customers",
            "delivery",
            "orders",
            "inventory",
            "marketing",
            "forecast",
            "prediction",
            "risk",
            "operations",
            "supplier",
            "product",
            "business",
        ]

        KNOWLEDGE_ONLY_TERMS = [
            "policy",
            "policies",
            "documentation",
            "document",
            "manual",
            "guide",
            "contract",
            "terms",
            "faq",
            "return policy",
            "refund policy",
            "privacy policy",
            "how do",
            "what is",
            "where can i find",
        ]

        BUSINESS_KEYWORDS = (
            knowledge_keywords
            + intelligence_keywords
            + decision_terms
            + STRATEGIC_KEYWORDS
            + business_terms
        )


        def find_last_business_query() -> str:
            """
            Walk backwards through the conversation and return the
            latest user message that actually contains business intent.
            """
            for msg in reversed(history[:-1]):
                if msg.role != "user":
                    continue

                text = msg.content.lower()

                if any(keyword in text for keyword in BUSINESS_KEYWORDS):
                    return text

            return ""
        
        previous_query = find_last_business_query()

        if (
            previous_query
            and (
                len(query_lower.split()) <= 5
                or query_lower.split()[0] in FOLLOW_UP_WORDS
            )
        ):
            planner_query = f"{previous_query} {query_lower}"
        else:
            planner_query = query_lower

        knowledge_only = any(
            term in planner_query
            for term in KNOWLEDGE_ONLY_TERMS
        )

        analytics_match = any(
            term in planner_query
            for term in intelligence_keywords
        )

        scenario_match = any(
            term in planner_query
            for term in decision_terms + STRATEGIC_KEYWORDS
        )

    # -------------------------
    # Capability Detection
    # -------------------------

        if knowledge_only and not analytics_match and not scenario_match:
            return ExecutionPlan(
                agents=[AgentType.KNOWLEDGE],
                reasoning="Knowledge/document lookup."
            )
        
        
        needs_documents = any(
            keyword in planner_query
            for keyword in knowledge_keywords
        )

        needs_analytics = any(
            keyword in planner_query
            for keyword in intelligence_keywords
        )

        needs_decision = (
            (
                any(term in planner_query for term in decision_terms)
                or any(term in planner_query for term in STRATEGIC_KEYWORDS)
            )
            and any(term in planner_query for term in business_terms)
        )


    # -------------------------
    # Build Agent List
    # -------------------------

        agents: list[AgentType] = []

        if needs_documents:
            agents.append(
                AgentType.KNOWLEDGE
            )

        if needs_analytics:
            agents.append(
                AgentType.INTELLIGENCE
            )

        if needs_decision:
            agents.append(
                AgentType.SCENARIO
            )

        agents = list(
            dict.fromkeys(
                agents
            )
        )

    # -------------------------
    # Invalid Input
    # -------------------------

        if (
            not agents
            and len(planner_query.split()) <= 1
        ):
            return ExecutionPlan(
                agents=[],
                parallel=False,
                reasoning="No business intent detected.",
            )

    # -------------------------
    # Deterministic Match
    # -------------------------

        if agents:

            reasons: list[str] = []

            if needs_documents:
                reasons.append("documents")

            if needs_analytics:
                reasons.append("analytics")

            if needs_decision:
                reasons.append("decision")

            return ExecutionPlan(
                agents=agents,
                parallel=len(agents) > 1,
                reasoning=" + ".join(reasons),
            )


        # fallback only for complex questions

        prompt = """
You are the SynapseOS Business Agent Planner.

Your ONLY responsibility is to decide which specialist agents should execute.

DO NOT answer the user's question.
DO NOT summarize.
DO NOT explain.

Return ONLY valid JSON.

=========================
AVAILABLE AGENTS
=========================

1. knowledge

Purpose:
- Enterprise documents
- Policies
- SOPs
- Manuals
- Contracts
- PDFs
- Knowledge Base
- RAG
- Questions asking "according to the documents"

Examples:
- What is our return policy?
- Explain our leave policy.
- What does the contract say?
- Summarize this document.

2. intelligence

Purpose:
- Business analytics
- KPIs
- Dashboards
- Revenue
- Sales
- Customers
- Products
- Trends
- Forecasting
- Prediction
- Risk Analysis
- Business Metrics

Examples:
- Show sales summary.
- Forecast next month's revenue.
- Predict customer churn.
- Analyze business risks.
- Show KPI dashboard.

3. scenario

Purpose:
- What-if analysis
- Strategic planning
- Decision support
- Optimization
- Trade-offs
- Recommendations
- Simulations
- Executive decision making

Examples:
- What happens if delivery time improves by 20%?
- Should we increase marketing spend?
- Which strategy is better?
- What is the impact of reducing prices?
- Recommend the best business decision.

=========================
ROUTING RULES
=========================

Use ONLY the minimum required agents.

Examples

User:
"What is our return policy?"

Return:

{
  "agents": ["knowledge"],
  "parallel": false,
  "reasoning": "Document lookup."
}

User:
"Predict customer churn."

Return:

{
  "agents": ["intelligence"],
  "parallel": false,
  "reasoning": "Prediction request."
}

User:
"What if customer churn increases by 10%?"

Return:

{
  "agents": ["scenario"],
  "parallel": false,
  "reasoning": "Scenario simulation."
}

User:
"Should management invest in faster delivery?"

Return:

{
  "agents": ["scenario"],
  "parallel": false,
  "reasoning": "Strategic decision support."
}

User:
"Based on our current sales performance, what should management focus on?"

Return:

{
  "agents": ["intelligence", "scenario"],
  "parallel": true,
  "reasoning": "Business metrics plus executive recommendations."
}

User:
"Based on our documents and current sales performance, what should management focus on?"

Return:

{
  "agents": ["knowledge", "intelligence", "scenario"],
  "parallel": true,
  "reasoning": "Needs enterprise knowledge, analytics and strategic planning."
}

User:
"Summarize our business performance."

Return:

{
  "agents": ["intelligence"],
  "parallel": false,
  "reasoning": "Business analytics request."
}

User:
"Explain the onboarding policy and recommend improvements."

Return:

{
  "agents": ["knowledge", "scenario"],
  "parallel": true,
  "reasoning": "Needs document understanding and recommendations."
}

Greetings:

- hello
- hi
- hey
- good morning
- good evening
- thanks
- thank you
- bye

Return:

{
  "agents": [],
  "parallel": false,
  "reasoning": "Greeting."
}

Completely unrelated or invalid input:

Return:

{
  "agents": [],
  "parallel": false,
  "reasoning": "No suitable business agents required."
}

=========================
OUTPUT FORMAT
=========================

Return ONLY valid JSON.

Schema:

{
  "agents": [],
  "parallel": false,
  "reasoning": "short explanation"
}

Rules:
- agents must contain zero or more of:
  - knowledge
  - intelligence
  - scenario
- parallel must be true only when more than one agent is required.
- reasoning must be one short sentence.
- Do not return markdown.
- Do not return code blocks.
- Do not return any explanation.

Return ONLY the JSON object.
"""


        response = await self.llm.generate(
            prompt,
        )


        data = parse_llm_json(
            response,
        )


        return ExecutionPlan(
            agents=[
                AgentType(agent)
                for agent in data["agents"]
            ],
            parallel=data.get(
                "parallel",
                False,
            ),
            reasoning=data.get(
                "reasoning",
            ),
        )