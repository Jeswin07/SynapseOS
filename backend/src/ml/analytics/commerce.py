"""Commerce analytics engine."""

from __future__ import annotations

from typing import Any

import pandas as pd


class CommerceAnalyticsEngine:
    """
    Generates commerce business intelligence.
    """


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
        }


    # -----------------------------
    # Revenue
    # -----------------------------

    def _revenue(
        self,
        data: pd.DataFrame,
    ):


        column = (
            "revenue"
            if "revenue" in data.columns
            else "payment_value"
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

        customer_column = None


        if "customer_unique_id" in data.columns:

            customer_column = "customer_unique_id"


        elif "customer_id" in data.columns:

            customer_column = "customer_id"


        if customer_column is None:

            return {}


        orders = (
            data.groupby(
                customer_column,
            )
            .size()
        )


        return {
            "total_customers": int(
                orders.count()
            ),

            "repeat_customers": int(
                (
                    orders > 1
                ).sum()
            ),

            "repeat_customer_rate": round(
                float(
                    (
                        (orders > 1).sum()
                        /
                        orders.count()
                    )
                    * 100
                ),
                2,
            ),
        }


    # -----------------------------
    # Products
    # -----------------------------

    def _products(
        self,
        data: pd.DataFrame,
    ):


        if "product_category_name" not in data:

            return {}


        result = {
            "top_categories_by_orders":
                data[
                    "product_category_name"
                ]
                .value_counts()
                .head(10)
                .to_dict()
        }


        if "revenue" in data.columns:

            result[
                "top_categories_by_revenue"
            ] = (
                data.groupby(
                    "product_category_name"
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


        if "review_score" in data.columns:

            result[
                "top_categories_by_rating"
            ] = (
                data.groupby(
                    "product_category_name"
                )[
                    "review_score"
                ]
                .mean()
                .sort_values(
                    ascending=False,
                )
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


        result = {}


        if (
            "order_delivered_customer_date"
            in data
            and
            "order_purchase_timestamp"
            in data
        ):


            delivered = pd.to_datetime(
                data[
                    "order_delivered_customer_date"
                ],
                errors="coerce",
            )


            purchased = pd.to_datetime(
                data[
                    "order_purchase_timestamp"
                ],
                errors="coerce",
            )


            days = (
                delivered
                -
                purchased
            ).dt.days


            result[
                "average_delivery_days"
            ] = float(
                days.mean()
            )


            result[
                "late_orders"
            ] = int(
                (
                    days > 15
                ).sum()
            )


        return result


    # -----------------------------
    # Geography
    # -----------------------------

    def _geography(
        self,
        data: pd.DataFrame,
    ):


        if "customer_state" not in data:
            return {}


        return {
            "top_regions":
                data[
                    "customer_state"
                ]
                .value_counts()
                .head(10)
                .to_dict()
        }


    # -----------------------------
    # Trends
    # -----------------------------

    def _trends(
        self,
        data: pd.DataFrame,
    ):


        if (
            "order_purchase_timestamp"
            not in data
            or
            "revenue"
            not in data
        ):
            return {}


        temp = data.copy()


        temp["month"] = (
            pd.to_datetime(
                temp[
                    "order_purchase_timestamp"
                ]
            )
            .dt
            .to_period("M")
            .astype(str)
        )


        revenue = (
            temp.groupby(
                "month"
            )[
                "revenue"
            ]
            .sum()
        )


        growth = (
            revenue
            .pct_change()
            .fillna(0)
            * 100
        )


        return {
            "monthly_revenue":
                revenue.to_dict(),

            "monthly_growth_percentage":
                growth.round(
                    2,
                )
                .to_dict(),
        }


    # -----------------------------
    # Insights
    # -----------------------------

    def _insights(
        self,
        data: pd.DataFrame,
    ) -> list[str]:


        insights = []


        if "review_score" in data:


            rating = (
                data[
                    "review_score"
                ]
                .mean()
            )


            if rating >= 4:

                insights.append(
                    "Customer satisfaction is healthy."
                )

            else:

                insights.append(
                    "Customer satisfaction requires improvement."
                )


        if (
            "order_delivered_customer_date"
            in data
            and
            "order_purchase_timestamp"
            in data
        ):


            delivery_days = (
                pd.to_datetime(
                    data[
                        "order_delivered_customer_date"
                    ],
                    errors="coerce",
                )
                -
                pd.to_datetime(
                    data[
                        "order_purchase_timestamp"
                    ],
                    errors="coerce",
                )
            ).dt.days


            if delivery_days.mean() > 10:

                insights.append(
                    "Delivery time optimization opportunity detected."
                )


        return insights