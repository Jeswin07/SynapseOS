"""Scenario simulation engine."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class SimulationEngine:
    """
    Applies business scenario assumptions before
    executive reasoning.

    This class performs NO LLM calls.

    It modifies analytics based on scenario parameters
    to create a simulated business outcome.
    """

    def simulate(
        self,
        *,
        scenario: dict[str, Any],
        analytics: dict[str, Any] | None,
    ) -> dict[str, Any]:

        if analytics is None:
            return {}

        result = deepcopy(analytics)

        parameters = scenario.get("parameters", [])

        scenario_type = scenario.get(
            "scenario_type",
            "",
        )

        parameter = parameters[0] if parameters else {}

        metric = parameter.get(
            "metric",
            "",
        )

        operation = parameter.get(
            "operation",
            "",
        )

        value = (
            parameter.get("value")
            or parameter.get("target_value")
            or 0
        )

        # -----------------------------
        # Marketing
        # -----------------------------

        if (scenario_type == "marketing" or metric == "marketing"):

            increase = value

            revenue = result.get("revenue")

            if revenue:

                total = revenue.get("total_revenue")

                if total is not None:

                    revenue["simulated_total_revenue"] = round(
                        total * (1 + (increase * 0.40 / 100)),
                        2,
                    )

                    revenue["expected_growth"] = (
                        f"+{round(increase * 0.40,2)}%"
                    )

        # -----------------------------
        # Pricing
        # -----------------------------

        elif (
            scenario_type == "pricing"
            or metric == "price"
        ):

            decrease = value

            revenue = result.get("revenue")

            if revenue:

                total = revenue.get("total_revenue")

                if total is not None:

                    simulated = total * (
                        1 - (decrease * 0.15 / 100)
                    )

                    revenue["simulated_total_revenue"] = round(
                        simulated,
                        2,
                    )

                    revenue["expected_order_growth"] = (
                        f"+{round(decrease * 1.8,2)}%"
                    )

        # -----------------------------
        # Delivery
        # -----------------------------

        elif (
            scenario_type == "delivery"
            or metric == "delivery"
        ):

            improve = value

            operations = result.get("operations")

            if operations:

                delivery = operations.get(
                    "average_delivery_days"
                )

                if delivery:

                    operations[
                        "simulated_delivery_days"
                    ] = round(
                        delivery * (
                            1 - improve / 100
                        ),
                        2,
                    )

                    operations[
                        "expected_customer_satisfaction"
                    ] = (
                        f"+{round(improve * 0.25,2)}%"
                    )

        # -----------------------------
        # Customer Churn
        # -----------------------------

        elif (
            scenario_type == "customer"
            or metric == "customer"
        ):

            increase = value

            customers = result.get("customers")

            if customers:

                repeat = customers.get(
                    "repeat_customer_rate"
                )

                if repeat:

                    customers[
                        "simulated_repeat_rate"
                    ] = round(
                        repeat * (
                            1 + increase / 100
                        ),
                        2,
                    )

        # -----------------------------
        # Inventory
        # -----------------------------

        elif (
            scenario_type == "inventory"
            or metric == "inventory"
        ):

            operations = result.get("operations")

            if operations:

                operations["inventory_optimization"] = (
                    f"{value}%"
                )

                operations["expected_storage_cost_change"] = (
                    f"-{round(value * 0.30, 2)}%"
                )

        # -----------------------------
        # Finance
        # -----------------------------

        elif (
            scenario_type == "finance"
            or metric == "finance"
        ):

            revenue = result.get("revenue")

            if revenue:

                total = revenue.get("total_revenue")

                if total:

                    revenue["simulated_profit_change"] = (
                        f"+{round(value * 0.50,2)}%"
                    )

        result["simulation"] = {
            "scenario_type": scenario_type,
            "parameters": parameters,
            "status": "completed",
        }

        return result

    def run(
        self,
        *,
        scenario: dict[str, Any],
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        
        return self.simulate(
            scenario=scenario,
            analytics=evidence.get("analytics"),
        )