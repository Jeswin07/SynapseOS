"""Scenario Decision Builder."""

from __future__ import annotations

from typing import Any

from src.agents.scenario.models import (
    ConfidenceLevel,
    DecisionReport,
    ImpactItem,
    TradeoffItem,
)


class DecisionBuilder:
    """
    Builds a structured business decision from
    collected evidence.

    No LLMs.

    No executive summaries.

    No recommendations.

    Pure deterministic business reasoning.
    """

    async def build(
        self,
        *,
        scenario: str,
        evidence: dict[str, Any],
        simulation: dict[str, Any],
    ) -> DecisionReport:

        report = DecisionReport()

        report.evidence = evidence

        summary: list[str] = []

        confidence = ConfidenceLevel.HIGH

        # =====================================================
        # Analytics
        # =====================================================

        analytics = simulation or evidence.get("analytics")

        if analytics:

            operations = analytics.get(
                "operations",
                {},
            )

            simulated_delivery = operations.get(
                "simulated_delivery_days"
            )

            expected_satisfaction = operations.get(
                "expected_customer_satisfaction"
            )

            revenue = analytics.get(
                "revenue",
                {},
            )

            simulated_revenue = revenue.get(
                "simulated_total_revenue"
            )

            expected_growth = revenue.get(
                "expected_growth"
            )

            expected_order_growth = revenue.get(
                "expected_order_growth"
            )

            reviews = analytics.get(
                "reviews",
                {},
            )

            customers = analytics.get(
                "customers",
                {},
            )

            late_orders = operations.get(
                "late_orders",
                0,
            )

            avg_delivery = operations.get(
                "average_delivery_days",
                0,
            )

            repeat_rate = customers.get(
                "repeat_customer_rate",
                0,
            )

            avg_rating = reviews.get(
                "average_rating",
                0,
            )

            if late_orders > 20000:

                report.impacts.append(
                    ImpactItem(
                        title="Delivery Performance",

                        description=(
                            f"{late_orders:,} late orders "
                            "indicate operational inefficiencies."
                        ),

                        severity="HIGH",

                        positive=False,
                    )
                )

            if simulated_delivery:

                report.impacts.append(
                    ImpactItem(
                        title="Delivery Simulation",

                        description=(
                            f"Average delivery improves "
                            f"to {simulated_delivery:.2f} days."
                        ),

                        severity="LOW",

                        positive=True,
                    )
                )

            if expected_satisfaction:

                report.tradeoffs.append(
                    TradeoffItem(
                        benefit=(
                            f"Customer satisfaction "
                            f"{expected_satisfaction}"
                        ),

                        cost="Higher logistics cost.",
                    )
                )

                report.tradeoffs.append(
                    TradeoffItem(
                        benefit="Lower logistics costs",

                        cost="Reduced customer satisfaction",
                    )
                )

                report.risks.append(
                    "High delivery delays may increase customer churn."
                )

            if avg_rating >= 4:

                report.impacts.append(
                    ImpactItem(
                        title="Customer Satisfaction",

                        description=(
                            f"Average rating of "
                            f"{avg_rating:.2f} "
                            "indicates healthy customer satisfaction."
                        ),

                        severity="LOW",

                        positive=True,
                    )
                )

            if repeat_rate < 10:

                report.risks.append(
                    "Low repeat customer rate limits long-term revenue growth."
                )


            if expected_growth:

                report.tradeoffs.append(
                    TradeoffItem(
                        benefit=f"Revenue growth {expected_growth}",

                        cost="Higher marketing investment required.",
                    )
                )

            if expected_order_growth:

                report.tradeoffs.append(
                    TradeoffItem(
                        benefit=f"Order volume {expected_order_growth}",

                        cost="Lower average margin.",
                    )
                )
            # ----------------------------------------
            # Revenue Simulation
            # ----------------------------------------

            if simulated_revenue is not None:

                report.impacts.append(
                    ImpactItem(
                        title="Revenue Simulation",

                        description=(
                            f"Projected revenue after simulation "
                            f"is ${simulated_revenue:,.2f}."
                        ),

                        severity="LOW",

                        positive=True,
                    )
                )

            if expected_growth:

                report.tradeoffs.append(
                    TradeoffItem(
                        benefit=(
                            f"Expected revenue growth "
                            f"{expected_growth}"
                        ),

                        cost=(
                            "Additional marketing investment "
                            "may be required."
                        ),
                    )
                )

            if expected_order_growth:

                report.tradeoffs.append(
                    TradeoffItem(
                        benefit=(
                            f"Expected order increase "
                            f"{expected_order_growth}"
                        ),

                        cost=(
                            "Reduced average profit margin."
                        ),
                    )
                )


            summary.append(
                "Business analytics evaluated."
            )

        # =====================================================
        # Prediction
        # =====================================================

        prediction = evidence.get(
            "prediction",
        )

        if prediction:

            summary_data = prediction.get(
                "summary",
                {},
            )

            high_risk = summary_data.get(
                "high_risk_entities",
                0,
            )

            revenue_risk = (
                summary_data.get(
                    "business_impact",
                    {},
                ).get(
                    "revenue_at_risk",
                    0,
                )
            )

            if high_risk > 0:

                report.impacts.append(
                    ImpactItem(
                        title="Customer Churn",

                        description=(
                            f"{high_risk} customers "
                            "are considered high risk."
                        ),

                        severity="HIGH",

                        positive=False,
                    )
                )

                report.risks.append(
                    f"${revenue_risk:,.2f} revenue is at risk from churn."
                )

            summary.append(
                "Customer prediction analysed."
            )

        # =====================================================
        # Risk
        # =====================================================

        risk = evidence.get(
            "risk",
        )

        if risk:

            level = risk.get(
                "level",
                "MEDIUM",
            )

            overall = risk.get(
                "overall_risk",
                0,
            )

            report.impacts.append(
                ImpactItem(
                    title="Business Risk",

                    description=(
                        f"Overall risk level is "
                        f"{level} ({overall})."
                    ),

                    severity=level,

                    positive=False,
                )
            )

            if level == "HIGH":

                confidence = (
                    ConfidenceLevel.HIGH
                )

            summary.append(
                "Risk assessment completed."
            )

        # =====================================================
        # Forecast
        # =====================================================

        forecast = evidence.get(
            "forecast",
        )

        if forecast:

            forecast_summary = forecast.get(
                "summary",
                {},
            )

            expected = forecast_summary.get(
                "total_expected_value",
                0,
            )

            report.impacts.append(
                ImpactItem(
                    title="Revenue Forecast",

                    description=(
                        f"Expected revenue "
                        f"${expected:,.2f}"
                    ),

                    severity="LOW",

                    positive=True,
                )
            )

            summary.append(
                "Revenue forecast generated."
            )

        # =====================================================
        # Final Summary
        # =====================================================

        report.summary = (
            f"Scenario '{scenario}' evaluated using available "
            "business evidence. "
            + " ".join(summary)
        )

        report.confidence = confidence

        return report