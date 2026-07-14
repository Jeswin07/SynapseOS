"""Scenario Planner normalizer."""

from __future__ import annotations

from src.agents.scenario.models import (
    ParameterOperation,
    ScenarioIntent,
    ScenarioParameter,
    ScenarioPlan,
    ScenarioType,
)


class PlannerNormalizer:
    """
    Converts raw LLM JSON into a validated ScenarioPlan.
    """

    @staticmethod
    def normalize(
        data: dict,
    ) -> ScenarioPlan:

        # -----------------------------
        # Intent
        # -----------------------------

        intent = PlannerNormalizer._intent(
            data.get(
                "intent",
                "what_if",
            ),
        )

        # -----------------------------
        # Scenario Type
        # -----------------------------

        scenario_type = PlannerNormalizer._scenario_type(
            data.get(
                "scenario_type",
                "general",
            ),
        )

        # -----------------------------
        # Parameters
        # -----------------------------

        parameters = []

        for parameter in data.get(
            "parameters",
            [],
        ):

            parameters.append(
                ScenarioParameter(
                    metric=parameter.get(
                        "metric",
                        "",
                    ),

                    operation=PlannerNormalizer._operation(
                        parameter.get(
                            "operation",
                            "unknown",
                        ),
                    ),

                    current_value=parameter.get(
                        "current_value",
                    ),

                    target_value=parameter.get(
                        "target_value",
                    ),

                    value=parameter.get(
                        "value",
                    ),

                    unit=parameter.get(
                        "unit",
                    ),
                )
            )

        return ScenarioPlan(
            intent=intent,
            scenario_type=scenario_type,
            reasoning=data.get(
                "reasoning",
                "",
            ),
            parameters=parameters,
        )

    # =====================================================

    @staticmethod
    def _intent(
        value: str,
    ) -> ScenarioIntent:

        value = (
            value.lower()
            .strip()
            .replace(
                " ",
                "_",
            )
        )

        try:
            return ScenarioIntent(value)

        except Exception:
            return ScenarioIntent.WHAT_IF

    # =====================================================

    @staticmethod
    def _scenario_type(
        value: str,
    ) -> ScenarioType:

        value = (
            value.lower()
            .strip()
            .replace(
                " ",
                "_",
            )
        )

        try:
            return ScenarioType(value)

        except Exception:
            return ScenarioType.GENERAL

    # =====================================================

    @staticmethod
    def _operation(
        value: str,
    ) -> ParameterOperation:

        value = (
            value.lower()
            .strip()
            .replace(
                " ",
                "_",
            )
        )

        try:
            return ParameterOperation(value)

        except Exception:
            return ParameterOperation.UNKNOWN