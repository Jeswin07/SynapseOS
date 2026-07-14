"""Scenario evidence planner."""

from __future__ import annotations

from src.agents.scenario.models import (
    EvidencePlan,
    ScenarioIntent,
    ScenarioPlan,
    ScenarioType,
)

from src.mcp.types import MCPTool


class EvidencePlanner:
    """
    Determines which MCP tools are required
    to evaluate a business scenario.

    This planner does not execute any tools.
    It only decides which evidence should
    be collected.
    """

    def plan(
        self,
        scenario: ScenarioPlan,
    ) -> EvidencePlan:

        tools: list[MCPTool] = []

        reasoning: list[str] = []

        # --------------------------------------------------
        # Scenario Type Rules
        # --------------------------------------------------

        match scenario.scenario_type:

            case ScenarioType.SALES:

                tools.extend([
                    MCPTool.ANALYTICS,
                    MCPTool.FORECAST,
                    MCPTool.PREDICTION,
                ])

                reasoning.append(
                    "Sales scenarios require analytics, forecasting, and prediction.",
                )

            case ScenarioType.REVENUE:

                tools.extend([
                    MCPTool.ANALYTICS,
                    MCPTool.FORECAST,
                    MCPTool.RISK,
                ])

                reasoning.append(
                    "Revenue scenarios require financial analysis and risk evaluation.",
                )

            case ScenarioType.CUSTOMER:

                tools.extend([
                    MCPTool.ANALYTICS,
                    MCPTool.PREDICTION,
                ])

                reasoning.append(
                    "Customer scenarios require analytics and prediction.",
                )

            case ScenarioType.MARKETING:

                tools.extend([
                    MCPTool.ANALYTICS,
                    MCPTool.FORECAST,
                    MCPTool.PREDICTION,
                ])

                reasoning.append(
                    "Marketing scenarios require historical trends and future demand.",
                )

            case ScenarioType.DELIVERY:

                tools.extend([
                    MCPTool.FORECAST,
                    MCPTool.PREDICTION,
                    MCPTool.RISK,
                ])

                reasoning.append(
                    "Delivery scenarios require operational forecasting "
                    "and risk analysis.",
                )

            case ScenarioType.INVENTORY:

                tools.extend([
                    MCPTool.ANALYTICS,
                    MCPTool.FORECAST,
                ])

                reasoning.append(
                    "Inventory scenarios require demand forecasting.",
                )

            case ScenarioType.PRICING:

                tools.extend([
                    MCPTool.ANALYTICS,
                    MCPTool.PREDICTION,
                    MCPTool.RISK,
                ])

                reasoning.append(
                    "Pricing scenarios require customer behaviour prediction and risk.",
                )

            case ScenarioType.OPERATIONS:

                tools.extend([
                    MCPTool.ANALYTICS,
                    MCPTool.RISK,
                ])

                reasoning.append(
                    "Operational changes require analytics and risk assessment.",
                )

            case ScenarioType.FINANCE:

                tools.extend([
                    MCPTool.ANALYTICS,
                    MCPTool.FORECAST,
                    MCPTool.RISK,
                ])

                reasoning.append(
                    "Financial decisions require forecasting and risk evaluation.",
                )

            case _:

                tools.extend([
                    MCPTool.ANALYTICS,
                ])

                reasoning.append(
                    "General scenarios require business analytics.",
                )

        # --------------------------------------------------
        # Intent Rules
        # --------------------------------------------------

        if scenario.intent is ScenarioIntent.WHAT_IF:

            reasoning.append(
                "Evaluating impact of hypothetical change.",
            )

        elif scenario.intent is ScenarioIntent.COMPARISON:

            if MCPTool.ANALYTICS not in tools:
                tools.append(
                    MCPTool.ANALYTICS,
                )

            reasoning.append(
                "Comparisons require baseline analytics.",
            )

        elif scenario.intent is ScenarioIntent.OPTIMIZATION:

            if MCPTool.PREDICTION not in tools:
                tools.append(
                    MCPTool.PREDICTION,
                )

            if MCPTool.FORECAST not in tools:
                tools.append(
                    MCPTool.FORECAST,
                )

            reasoning.append(
                "Optimization requires prediction and forecasting.",
            )

        elif scenario.intent is ScenarioIntent.RISK_MITIGATION:

            if MCPTool.RISK not in tools:
                tools.append(
                    MCPTool.RISK,
                )

            reasoning.append(
                "Risk mitigation requires dedicated risk analysis.",
            )

        # --------------------------------------------------
        # Remove duplicates while preserving order
        # --------------------------------------------------

        unique_tools: list[MCPTool] = []

        for tool in tools:

            if tool not in unique_tools:

                unique_tools.append(
                    tool,
                )

        return EvidencePlan(
            tools=unique_tools,
            reasoning="\n".join(
                reasoning,
            ),
        )