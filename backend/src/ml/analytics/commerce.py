"""Commerce analytics engine."""

from __future__ import annotations

from typing import Any
import numpy as np
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
        """
        Dataset overview.

        Uses enterprise canonical columns only.
        """

        return {

            "total_records": int(len(data)),

            "columns": int(len(data.columns)),

            "missing_values": int(
                data.isna().sum().sum()
            ),

            "duplicate_records": int(
                data.duplicated().sum()
            ),

            "available_metrics": {

                "revenue":
                    "revenue" in data.columns,

                "customers":
                    "customer_id" in data.columns,

                "categories":
                    "category" in data.columns,

                "reviews":
                    "review_score" in data.columns,

                "geography":
                    (
                        "state" in data.columns
                        or
                        "city" in data.columns
                    ),

                "delivery":
                    (
                        "delivery_days"
                        in data.columns
                    ),

                "time":
                    (
                        "order_date"
                        in data.columns
                    ),

                "seller":
                    (
                        "seller_id"
                        in data.columns
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
        """
        Revenue analytics.
        """

        if "revenue" not in data.columns:
            return {}

        revenue = pd.to_numeric(
            data["revenue"],
            errors="coerce",
        )

        revenue = revenue.dropna()

        if revenue.empty:
            return {}

        return {

            "total_revenue": float(
                revenue.sum()
            ),

            "average_order_value": float(
                revenue.mean()
            ),

            "highest_order_value": float(
                revenue.max()
            ),

            "lowest_order_value": float(
                revenue.min()
            ),

            "median_order_value": float(
                revenue.median()
            ),

        }


    # -----------------------------
    # Customers
    # -----------------------------

    def _customers(
        self,
        data: pd.DataFrame,
    ):

        if "customer_id" not in data.columns:
            return {}

        customers = data["customer_id"]

        total = customers.nunique()

        counts = customers.value_counts()

        repeat = int(
            (counts > 1).sum()
        )

        return {

            "total_customers": int(total),

            "repeat_customers": repeat,

            "repeat_customer_rate": round(

                repeat / total * 100,

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

        if "category" not in data.columns:
            return {}

        result = {

            "top_categories_by_orders": (

                data["category"]

                .value_counts()

                .head(10)

                .to_dict()

            )

        }

        if "revenue" in data.columns:

            revenue = data.copy()

            revenue["revenue"] = pd.to_numeric(

                revenue["revenue"],

                errors="coerce",

            )

            result["top_categories_by_revenue"] = (

                revenue

                .groupby("category")["revenue"]

                .sum()

                .sort_values(

                    ascending=False

                )

                .head(10)

                .to_dict()

            )

        if "review_score" in data.columns:

            reviews = data.copy()

            reviews["review_score"] = pd.to_numeric(

                reviews["review_score"],

                errors="coerce",

            )

            result["top_categories_by_rating"] = (

                reviews

                .groupby("category")["review_score"]

                .mean()

                .sort_values(

                    ascending=False

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

        if "seller_id" not in data.columns:
            return {}

        result: dict[str, Any] = {}
        result["total_sellers"] = int(
            data["seller_id"].nunique()
        )

        if "revenue" in data.columns:

            revenue = data.copy()

            revenue["revenue"] = pd.to_numeric(
                revenue["revenue"],
                errors="coerce",
            )

            result["top_sellers_by_revenue"] = (

                revenue
                .groupby("seller_id")["revenue"]
                .sum()
                .sort_values(
                    ascending=False,
                )
                .head(10)
                .to_dict()

            )

        if "review_score" in data.columns:

            reviews = data.copy()

            reviews["review_score"] = pd.to_numeric(
                reviews["review_score"],
                errors="coerce",
            )

            result["top_sellers_by_rating"] = (

                reviews
                .groupby("seller_id")["review_score"]
                .mean()
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

        if "review_score" not in data.columns:
            return {}

        reviews = pd.to_numeric(
            data["review_score"],
            errors="coerce",
        )

        reviews = reviews.dropna()

        if reviews.empty:
            return {}

        return {

            "average_rating": float(
                reviews.mean()
            ),

            "highest_rating": float(
                reviews.max()
            ),

            "lowest_rating": float(
                reviews.min()
            ),

            "low_rating_orders": int(
                (reviews <= 2).sum()
            ),

        }


    # -----------------------------
    # Operations
    # -----------------------------

    def _operations(
        self,
        data: pd.DataFrame,
    ):

        if "delivery_days" not in data.columns:
            return {}

        days = pd.to_numeric(
            data["delivery_days"],
            errors="coerce",
        )

        days = days.dropna()

        if days.empty:
            return {}

        return {

            "average_delivery_days": float(
                days.mean()
            ),

            "late_orders": int(
                (days > 15).sum()
            ),

            "fast_deliveries": int(
                (days <= 3).sum()
            ),

        }


    # -----------------------------
    # Geography
    # -----------------------------

    def _geography(
        self,
        data: pd.DataFrame,
    ):

        if "state" not in data.columns:
            return {}

        return {

            "top_regions": (

                data["state"]

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

        if (
            "order_date" not in data.columns
            or
            "revenue" not in data.columns
        ):
            return {}

        temp = data.copy()

        temp["order_date"] = pd.to_datetime(
            temp["order_date"],
            errors="coerce",
        )

        temp["month"] = (

            temp["order_date"]

            .dt.to_period("M")

            .astype(str)

        )

        temp["revenue"] = pd.to_numeric(
            temp["revenue"],
            errors="coerce",
        )

        revenue = (

            temp

            .groupby("month")["revenue"]

            .sum()

        )

        growth = (

            revenue

            .pct_change()

            .fillna(0)

            * 100

        )

        growth = growth.replace([np.inf, -np.inf], 0).fillna(0)

        return {

            "monthly_revenue":
                revenue.to_dict(),

            "monthly_growth_percentage":
                growth.round(2).to_dict(),

        }


    # -----------------------------
    # Insights
    # -----------------------------

    def _insights(
        self,
        data: pd.DataFrame,
    ):

        insights = []

        if "review_score" in data.columns:

            rating = pd.to_numeric(
                data["review_score"],
                errors="coerce",
            ).mean()

            if pd.notna(rating):

                if rating >= 4:

                    insights.append(
                        "Customer satisfaction is healthy."
                    )

                elif rating >= 3:

                    insights.append(
                        "Customer satisfaction is moderate."
                    )

                else:

                    insights.append(
                        "Customer satisfaction requires improvement."
                    )

        if "delivery_days" in data.columns:

            delivery = pd.to_numeric(
                data["delivery_days"],
                errors="coerce",
            ).mean()

            if pd.notna(delivery):

                if delivery > 10:

                    insights.append(
                        "Delivery time optimization opportunity detected."
                    )

                elif delivery <= 5:

                    insights.append(
                        "Delivery performance is strong."
                    )

        return insights