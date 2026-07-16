"""Commerce analytics engine."""

from __future__ import annotations

from typing import Any

import pandas as pd


class CommerceAnalyticsEngine:
    """
    Generates commerce business intelligence.
    """


    def _col(
        self,
        df: pd.DataFrame,
        canonical: str,
        *fallbacks: str,
    ) -> str | None:
    
        """
        Resolve canonical column first.
        Falls back to legacy Olist names.
        """

        if canonical in df.columns:
            return canonical

        for col in fallbacks:
            if col in df.columns:
                return col

        return None
    
    def analyze(
        self,
        data: pd.DataFrame,
    ) -> dict[str, Any]:


        return {
            "overview": self._overview(data),
            "revenue": self._revenue(data),
            "customers": self._customers(data),
            "products": self._products(data),
            "sellers": self._sellers(data),
            "reviews": self._reviews(data),
            "operations": self._operations(data),
            "geography": self._geography(data),
            "trends": self._trends(data),
            "insights": self._insights(data),
        }


    # -----------------------------
    # Overview
    # -----------------------------

    def _overview(
        self,
        data: pd.DataFrame,
    ):

        return {

            "total_records": len(data),

            "columns": len(data.columns),

            "missing_values": int(
                data.isna().sum().sum()
            ),

            "duplicate_records": int(
                data.duplicated().sum()
            ),

            "available_metrics": {

                "revenue": self._col(
                    data,
                    "revenue",
                    "payment_value",
                )
                is not None,

                "customers": self._col(
                    data,
                    "customer_id",
                    "customer_unique_id",
                )
                is not None,

                "categories": self._col(
                    data,
                    "category",
                    "product_category_name",
                )
                is not None,

                "reviews": self._col(
                    data,
                    "review_score",
                    "rating",
                )
                is not None,

                "geography": self._col(
                    data,
                    "state",
                    "customer_state",
                )
                is not None,

                "delivery": (
                    "delivery_days" in data.columns
                    or
                    (
                        self._col(
                            data,
                            "delivery_date",
                            "order_delivered_customer_date",
                        )
                        is not None
                    )
                ),
            },
        }


    # -----------------------------
    # Revenue
    # -----------------------------

    def _revenue(
        self,
        data: pd.DataFrame,
    ):


        column = self._col(
            data,
            "revenue",
            "payment_value",
            "selling_price",
            "amount",
        )


        if column not in data.columns:
            return {}


        return {
            "total_revenue": float(
                data[column].sum()
            ),

            "average_order_value": float(
                data[column].mean()
            ),

            "highest_order_value": float(
                data[column].max()
            ),
        }


    # -----------------------------
    # Customers
    # -----------------------------

    def _customers(
        self,
        data: pd.DataFrame,
    ):

        customer_col = self._col(
            data,
            "customer_id",
            "customer_unique_id",
        )

        if customer_col is None:
            return {}

        orders = data.groupby(customer_col).size()

        repeat = int((orders > 1).sum())

        total = int(orders.count())

        return {
            "total_customers": total,
            "repeat_customers": repeat,
            "repeat_customer_rate": round(
                (repeat / total) * 100,
                2,
            ) if total else 0,
        }


    # -----------------------------
    # Products
    # -----------------------------

    def _products(
        self,
        data: pd.DataFrame,
    ):

        category_col = self._col(
            data,
            "category",
            "product_category_name",
        )

        if category_col is None:
            return {}

        result = {
            "top_categories_by_orders": (
                data[category_col]
                .value_counts()
                .head(10)
                .to_dict()
            )
        }

        revenue_col = self._col(
            data,
            "revenue",
            "payment_value",
            "selling_price",
            "amount",
        )

        if revenue_col:

            result["top_categories_by_revenue"] = (
                data.groupby(category_col)[revenue_col]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .to_dict()
            )

        rating_col = self._col(
            data,
            "review_score",
            "rating",
        )

        if rating_col:

            result["top_categories_by_rating"] = (
                data.groupby(category_col)[rating_col]
                .mean()
                .sort_values(ascending=False)
                .head(10)
                .to_dict()
            )

        return result


    # -----------------------------
    # Sellers
    # -----------------------------

    def _sellers(
        self,
        data: pd.DataFrame,
    ):

        if "seller_id" not in data:

            return {}


        result: dict[str, Any] = {
            "total_sellers": int(
                data[
                    "seller_id"
                ]
                .nunique()
            )
        }


        if "revenue" in data:

            result[
                "top_sellers_by_revenue"
            ] = (
                data.groupby(
                    "seller_id"
                )[
                    "revenue"
                ]
                .sum()
                .sort_values(
                    ascending=False,
                )
                .head(10)
                .to_dict()
            )


        if "review_score" in data:

            seller_stats = (
                data.groupby(
                    "seller_id",
                )
                .agg(
                    average_rating=(
                        "review_score",
                        "mean",
                    ),
                    orders=(
                        "seller_id",
                        "count",
                    ),
                )
            )


            seller_stats = seller_stats[
                seller_stats[
                    "orders"
                ]
                >= 50
            ]


            result[
                "top_sellers_by_rating"
            ] = (
                seller_stats[
                    "average_rating"
                ]
                .sort_values(
                    ascending=False,
                )
                .head(10)
                .to_dict()
            )


        return result


    # -----------------------------
    # Reviews
    # -----------------------------

    def _reviews(
        self,
        data: pd.DataFrame,
    ):


        if "review_score" not in data:
            return {}


        return {
            "average_rating": float(
                data[
                    "review_score"
                ].mean()
            ),

            "low_rating_orders": int(
                (
                    data[
                        "review_score"
                    ]
                    <= 2
                ).sum()
            ),
        }


    # -----------------------------
    # Operations
    # -----------------------------

    def _operations(
        self,
        data: pd.DataFrame,
    ):

        if "delivery_days" in data.columns:

            return {
                "average_delivery_days": float(
                    data["delivery_days"].mean()
                ),
                "late_orders": int(
                    (data["delivery_days"] > 15).sum()
                ),
            }

        purchase_col = self._col(
            data,
            "order_date",
            "order_purchase_timestamp",
        )

        delivery_col = self._col(
            data,
            "delivery_date",
            "order_delivered_customer_date",
        )

        if not purchase_col or not delivery_col:
            return {}

        delivered = pd.to_datetime(
            data[delivery_col],
            errors="coerce",
        )

        purchased = pd.to_datetime(
            data[purchase_col],
            errors="coerce",
        )

        days = (delivered - purchased).dt.days

        return {
            "average_delivery_days": float(days.mean()),
            "late_orders": int((days > 15).sum()),
        }


    # -----------------------------
    # Geography
    # -----------------------------

    def _geography(
        self,
        data: pd.DataFrame,
    ):

        state_col = self._col(
            data,
            "state",
            "customer_state",
        )

        if state_col is None:
            return {}

        return {
            "top_regions": (
                data[state_col]
                .value_counts()
                .head(10)
                .to_dict()
            )
        }


    # -----------------------------
    # Trends
    # -----------------------------

    def _trends(
        self,
        data: pd.DataFrame,
    ):

        date_col = self._col(
            data,
            "order_date",
            "order_purchase_timestamp",
        )

        revenue_col = self._col(
            data,
            "revenue",
            "payment_value",
            "selling_price",
            "amount",
        )

        if not date_col or not revenue_col:
            return {}

        temp = data.copy()

        temp["month"] = (
            pd.to_datetime(
                temp[date_col],
                errors="coerce",
            )
            .dt.to_period("M")
            .astype(str)
        )

        revenue = (
            temp.groupby("month")[revenue_col]
            .sum()
        )

        growth = (
            revenue
            .pct_change()
            .fillna(0)
            * 100
        )

        return {
            "monthly_revenue": revenue.to_dict(),
            "monthly_growth_percentage": growth.round(2).to_dict(),
        }


    # -----------------------------
    # Insights
    # -----------------------------

    def _insights(
        self,
        data: pd.DataFrame,
    ) -> list[str]:

        insights: list[str] = []

        rating_col = self._col(
            data,
            "review_score",
            "rating",
        )

        if rating_col:

            rating = data[rating_col].mean()

            if rating >= 4:
                insights.append(
                    "Customer satisfaction is healthy."
                )
            else:
                insights.append(
                    "Customer satisfaction requires improvement."
                )

        if "delivery_days" in data.columns:

            if data["delivery_days"].mean() > 10:
                insights.append(
                    "Delivery time optimization opportunity detected."
                )

        else:

            purchase_col = self._col(
                data,
                "order_date",
                "order_purchase_timestamp",
            )

            delivery_col = self._col(
                data,
                "delivery_date",
                "order_delivered_customer_date",
            )

            if purchase_col and delivery_col:

                delivery_days = (
                    pd.to_datetime(
                        data[delivery_col],
                        errors="coerce",
                    )
                    -
                    pd.to_datetime(
                        data[purchase_col],
                        errors="coerce",
                    )
                ).dt.days

                if delivery_days.mean() > 10:
                    insights.append(
                        "Delivery time optimization opportunity detected."
                    )

        return insights