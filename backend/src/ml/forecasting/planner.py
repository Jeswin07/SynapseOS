"""LLM forecast planner."""

from __future__ import annotations

import json

from src.agents.common.llm import LLMClient
from src.ml.features.semantic_resolver import (
    SemanticColumnResolver,
)
from src.ml.forecasting.schemas import (
    ForecastPlan,
)


class ForecastPlanner:
    """
    Converts user forecast request
    into executable forecast config.
    """
    def __init__(
        self,
    ) -> None:

        self.llm = LLMClient()
        self.resolver = SemanticColumnResolver()


    async def plan(
        self,
        *,
        query: str,
        columns: list[str],
    ) -> ForecastPlan:


        prompt = f"""
You are an enterprise forecasting planner.

Convert the user's request into executable JSON.

Available dataset columns:
{columns}

Rules:

General:
- Pick the best date column.
- Pick the metric based on business intent.
- Revenue/sales means money column.
- Orders means count order identifier.
- Demand means product quantity/count.
- Customer satisfaction means review/rating metric.
- Detect forecast horizon.


Revenue examples:
"forecast revenue"
"predict sales"

Use:
target_column = revenue OR price OR sales amount
aggregation = sum


Order examples:
"forecast orders"
"future order volume"

Use:
target_column = order_id
aggregation = count


Demand examples:
"product demand"
"inventory requirement"

Use:
target_column = product_count OR quantity
aggregation = sum


Delivery rules:

If user asks:
"delivery volume"
"number of deliveries"
"deliveries next month"

Use:
date_column = delivered date column
target_column = order id column
aggregation = count


If user asks:
"delivery time"
"delivery delay"
"shipping performance"

Use:
target_column = delivery_days
aggregation = mean


IMPORTANT:
Do not always use order purchase date.
Choose date based on question meaning.


Return ONLY JSON.

Schema:

{{
 "date_column":"",
 "target_column":"",
 "aggregation":"sum/count/mean",
 "frequency":"D/W/M",
 "periods":30,
 "filters":{{}}
}}


User request:
{query}
"""


        response = await self.llm.generate(
            prompt,
        )


        response = (
            response
            .replace(
                "```json",
                "",
            )
            .replace(
                "```",
                "",
            )
            .strip()
        )


        data = json.loads(response)


        if (
            not data.get("date_column")
            or data["date_column"] not in columns
        ):

            data["date_column"] = (
                self.resolver.resolve_date(
                    columns,
                )
            )


        if (
            not data.get("target_column")
            or data["target_column"] not in columns
        ):

            metric, aggregation = (
                self.resolver.resolve_metric(
                    columns=columns,
                    query=query,
                )
            )

            data["target_column"] = metric
            data["aggregation"] = aggregation


        return ForecastPlan(
            **data,
        )