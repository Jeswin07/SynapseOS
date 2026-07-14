"""Deterministic formatter for intelligence results."""

from __future__ import annotations

from typing import Any


class IntelligenceFormatter:

    def format(
        self,
        tool: str,
        data: dict[str, Any],
    ) -> str:

        if tool == "prediction":
            return self._prediction(data)

        if tool == "analytics":
            return self._analytics(data)

        if tool == "forecast":
            return self._forecast(data)

        if tool == "risk":
            return self._risk(data)

        return "No results found."

    def _prediction(
        self,
        data: dict,
    ) -> str:

        summary = data["summary"]

        revenue = (
            summary["business_impact"]
            .get("revenue_at_risk", 0)
        )

        return f"""
Customer Churn Prediction

• Total entities analysed: {summary["total_entities"]:,}
• High-risk entities: {summary["high_risk_entities"]}
• Average probability: {summary["average_probability"]:.2%}
• Revenue at risk: ${revenue:,.2f}

Recommendations:

{chr(10).join("- "+r for r in data["recommendations"])}
""".strip()

    def _risk(
        self,
        data: dict,
    ) -> str:

        lines = [
            f"Overall Business Risk: {data['level']} ({data['overall_risk']})",
            "",
        ]

        for risk in data["risks"]:

            revenue = (
                risk["impact"]
                .get(
                    "revenue_at_risk",
                    0,
                )
            )

            lines.extend(
                [
                    f"{risk['type'].replace('_',' ').title()}",
                    f"Severity: {risk['severity']}",
                    f"Affected: {risk['affected_entities']}",
                    f"Revenue at risk: ${revenue:,.2f}",
                    "",
                ]
            )

        return "\n".join(lines)

    def _forecast(
        self,
        data: dict,
    ) -> str:

        summary = data["summary"]

        metric = (
            data["forecast_config"]["metric"]
        )

        return f"""
Forecast Summary

Metric: {metric}

Forecast Horizon:
{summary["forecast_days"]} days

Expected Total:
{summary["total_expected_value"]:,.2f}

Average Daily:
{summary["average_daily_value"]:,.2f}
""".strip()

    def _analytics(
        self,
        data: dict,
    ) -> str:

        revenue = data["revenue"]

        customers = data["customers"]

        return f"""
Business Analytics Summary

Revenue

• Total Revenue:
${revenue["total_revenue"]:,.2f}

• Average Order:
${revenue["average_order_value"]:,.2f}

Customers

• Customers:
{customers["total_customers"]:,}

• Repeat Rate:
{customers["repeat_customer_rate"]}%

Insights

{chr(10).join("- "+x for x in data["insights"])}
""".strip()