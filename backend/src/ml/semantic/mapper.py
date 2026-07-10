"""LLM based semantic mapper."""

from __future__ import annotations

import json

from src.agents.common.llm import LLMClient

from src.ml.semantic.schemas import (
    SemanticMapping,
    SemanticProfile,
)


class SemanticMapper:
    """
    Converts raw dataset schemas into
    business concepts.
    """

    def __init__(
        self,
    ) -> None:

        self.llm = LLMClient()


    async def map(
        self,
        profile: SemanticProfile,
    ) -> SemanticMapping:


        prompt = f"""
You are a senior data architect.

Your task:
Convert unknown commerce datasets into a standard
business semantic model.


The dataset may be:
- Olist ecommerce
- Flipkart
- Amazon
- Shopify
- Custom commerce data


Analyze:
- table names
- column names
- data types
- sample values


Dataset profile:

{profile.model_dump_json()}


Return ONLY valid JSON.

Schema:


{{
 "sales": {{

    "order_id":"",
    "revenue":"",
    "price":"",
    "quantity":"",
    "order_date":""

 }},


 "products": {{

    "product_id":"",
    "category":"",
    "brand":""

 }},


 "customers": {{

    "customer_id":"",
    "city":"",
    "state":"",
    "segment":""

 }},


 "sellers": {{

    "seller_id":"",
    "city":"",
    "state":""

 }},


 "operations": {{

    "order_status":"",

    "approved_date":"",

    "shipped_date":"",

    "delivery_date":"",

    "estimated_delivery_date":""

 }},


 "experience": {{

    "rating":"",

    "review_text":""

 }},


 "geography": {{

    "city":"",
    "state":"",
    "country":""

 }},


 "relationships":[

    {{
      "from":"",
      "to":""
    }}

 ],


 "unmapped": {{}}

}}


Rules:

1. Use full references:

table.column


Example:

payments.payment_value


2. Do not invent columns.

3. Missing fields should be null.

4. Detect relationships using ids.

Example:

orders.order_id
connects to
payments.order_id


5. Prefer business meaning over column names.

Example:

payment_value = revenue

review_score = customer satisfaction

"""


        response = await self.llm.generate(
            prompt,
        )


        cleaned = (
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


        data = json.loads(
            cleaned,
        )


        return SemanticMapping(
            **data,
        )