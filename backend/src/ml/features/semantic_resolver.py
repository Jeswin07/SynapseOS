from __future__ import annotations


class SemanticColumnResolver:

    DATE_KEYWORDS = [
        "purchase",
        "order_date",
        "created",
        "timestamp",
        "date",
        "delivered",
        "delivery",
        "shipping",
        "shipped",
    ]


    REVENUE_KEYWORDS = [
        "revenue",
        "amount",
        "payment",
        "price",
        "sales",
        "value",
        "total",
    ]


    ORDER_KEYWORDS = [
        "order_id",
        "order",
        "transaction",
    ]


    def resolve_date(
        self,
        columns: list[str],
    ) -> str | None:

        for col in columns:
            name = col.lower()

            if any(
                key in name
                for key in self.DATE_KEYWORDS
            ):
                return col

        return None


    def resolve_metric(
        self,
        *,
        columns: list[str],
        query: str,
    ) -> tuple[str | None, str]:

        query = query.lower()


        if "revenue" in query or "sales" in query:

            for col in columns:

                if any(
                    key in col.lower()
                    for key in self.REVENUE_KEYWORDS
                ):
                    return col, "sum"


        if "order" in query or "delivery" in query:

            for col in columns:

                if "order" in col.lower():

                    return col, "count"


        return None, "sum"