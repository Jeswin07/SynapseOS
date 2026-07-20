"""Commerce feature builder."""

from __future__ import annotations
import numpy as np
import pandas as pd

import re

from src.ml.features.canonical_aliases import (
    CANONICAL_ALIASES,
)

from src.ml.features.base import BaseFeatureBuilder


class CommerceFeatureBuilder(BaseFeatureBuilder):
    """
    Converts commerce datasets into a unified
    analytics / forecasting feature table.
    """


    def build(
        self,
        datasets: dict[str, pd.DataFrame],
    ) -> pd.DataFrame:


        if "orders" not in datasets:


    # ----------------------------
    # Generic single dataset support
    # ----------------------------

            if len(datasets) == 1:

                features = list(datasets.values())[0].copy()

                features = self._apply_canonical_columns(features)

                features = self._engineer_common_features(features)

                return features


    # ----------------------------
    # Multi-file fallback
    # Try to find order-like table
    # ----------------------------

            order_table = None


            for name, frame in datasets.items():


                columns = [
                    col.lower()
                    for col in frame.columns
                ]


                if any(
                    "order" in col
                    for col in columns
                ):

                    order_table = name
                    break


            if order_table:

                datasets[
                    "orders"
                ] = datasets[
                    order_table
                ]


            else:

                features = list(datasets.values())[0].copy()

                features = self._apply_canonical_columns(features)

                features = self._engineer_common_features(features)

                return features


        features = (
            datasets["orders"]
            .copy()
        )


        # ----------------------------
        # Customers
        # ----------------------------

        customers = datasets.get(
            "customers"
        )


        if (
            customers is not None
            and "customer_id" in features.columns
            and "customer_id" in customers.columns
        ):

            features = features.merge(
                customers,
                on="customer_id",
                how="left",
            )


        # ----------------------------
        # Payments -> revenue
        # ----------------------------

        payments = datasets.get(
            "payments"
        )


        if (
            payments is not None
            and "order_id" in payments.columns
        ):

            payment_col = self.find_column(
                payments,
                [
                    "payment_value",
                    "order_total",
                    "total_amount",
                    "payment",
                    "amount",
                    "price",
                    "value",
                    "total",
                ],
            )


            if payment_col:

                payment_features = (
                    payments
                    .groupby(
                        "order_id",
                        as_index=False,
                    )
                    .agg(
                        revenue=(
                            payment_col,
                            "sum",
                        )
                    )
                )


                features = features.merge(
                    payment_features,
                    on="order_id",
                    how="left",
                )


        # ----------------------------
        # Reviews
        # ----------------------------

        reviews = datasets.get(
            "reviews"
        )


        if (
            reviews is not None
            and "order_id" in reviews.columns
        ):

            score_col = self.find_column(
                reviews,
                [
                    "review_score",
                    "rating",
                    "stars",
                    "score",
                ],
            )


            if score_col:

                review_features = (
                    reviews
                    .groupby(
                        "order_id",
                        as_index=False,
                    )
                    .agg(
                        review_score=(
                            score_col,
                            "mean",
                        )
                    )
                )


                features = features.merge(
                    review_features,
                    on="order_id",
                    how="left",
                )


        # ----------------------------
        # Order Items
        # ----------------------------

        items = datasets.get(
            "order_items"
        )


        if (
            items is not None
            and "order_id" in items.columns
        ):

            agg_rules = {}


            product_col = self.find_column(
                items,
                [
                    "product",
                    "item",
                ],
            )


            price_col = self.find_column(
                items,
                [
                    "price",
                    "amount",
                    "value",
                ],
            )


            if product_col:

                agg_rules[
                    "quantity"
                ] = (
                    product_col,
                    "count",
                )


            if price_col:

                agg_rules[
                    "total_price"
                ] = (
                    price_col,
                    "sum",
                )


            if agg_rules:

                item_features = (
                    items
                    .groupby(
                        "order_id",
                        as_index=False,
                    )
                    .agg(
                        **agg_rules
                    )
                )


                features = features.merge(
                    item_features,
                    on="order_id",
                    how="left",
                )

                # ----------------------------
        # Products
        # ----------------------------

        products = datasets.get(
            "products"
        )


        if (
            products is not None
            and items is not None
        ):

            product_key = self.find_column(
                items,
                [
                    "product_id",
                    "product",
                ],
            )


            if (
                product_key
                and product_key in products.columns
            ):

                product_map = (
                    items[
                        [
                            "order_id",
                            product_key,
                        ]
                    ]
                    .merge(
                        products,
                        on=product_key,
                        how="left",
                    )
                )


                product_map = (
                    product_map
                    .groupby(
                        "order_id",
                        as_index=False,
                    )
                    .first()
                )


                features = features.merge(
                    product_map,
                    on="order_id",
                    how="left",
                )


        # ----------------------------
        # Sellers
        # ----------------------------

        sellers = datasets.get(
            "sellers"
        )


        if (
            sellers is not None
            and items is not None
        ):

            seller_key = self.find_column(
                items,
                [
                    "seller_id",
                    "seller",
                ],
            )


            if (
                seller_key
                and seller_key in sellers.columns
            ):

                seller_map = (
                    items[
                        [
                            "order_id",
                            seller_key,
                        ]
                    ]
                    .merge(
                        sellers,
                        on=seller_key,
                        how="left",
                    )
                )


                seller_map = (
                    seller_map
                    .groupby(
                        "order_id",
                        as_index=False,
                    )
                    .first()
                )


                features = features.merge(
                    seller_map,
                    on="order_id",
                    how="left",
                )


        # ----------------------------
        # Generic date normalization
        # ----------------------------

        date_col = self.find_column(
            features,
            [
                "purchase",
                "order_date",
                "created",
                "timestamp",
                "date",
            ],
        )


        if (
            date_col
            and date_col != "date"
        ):

            features["date"] = (
                features[
                    date_col
                ]
            )


        # ----------------------------
        # Delivery Features
        # ----------------------------

        delivered_col = self.find_column(
            features,
            [
                "delivered",
                "delivery_date",
                "shipped",
            ],
        )


        estimated_col = self.find_column(
            features,
            [
                "estimated",
                "expected",
            ],
        )


        if (
            delivered_col
            and date_col
        ):

            features[
                "delivery_days"
            ] = (
                pd.to_datetime(
                    features[
                        delivered_col
                    ],
                    errors="coerce",
                )
                -
                pd.to_datetime(
                    features[
                        date_col
                    ],
                    errors="coerce",
                )
            ).dt.days


        if (
            delivered_col
            and estimated_col
        ):

            features[
                "delivery_delay_days"
            ] = (
                pd.to_datetime(
                    features[
                        delivered_col
                    ],
                    errors="coerce",
                )
                -
                pd.to_datetime(
                    features[
                        estimated_col
                    ],
                    errors="coerce",
                )
            ).dt.days

        features = self._apply_canonical_columns(features)

        features = self._engineer_common_features(features)

        return features


    def find_column(
        self,
        df,
        keywords: list[str],
    ) -> str | None:


        if df is None:

            return None


        columns = {
            col.lower(): col
            for col in df.columns
        }


    # exact priority first
        for keyword in keywords:

            for lower, original in columns.items():

                if lower == keyword:

                    return original


    # partial fallback
        for keyword in keywords:

            for lower, original in columns.items():

                if keyword in lower:

                    return original


        return None


    def _apply_canonical_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Creates enterprise canonical columns.

        Rules
        -----
        • Preserve valid canonical columns.
        • Replace empty/invalid canonical columns.
        • First valid alias wins.
        • Matching is case-insensitive.
        """

        normalized_columns = {
            self._normalize_column_name(col): col
            for col in dataframe.columns
        }

        mapped_columns: dict[str, str] = {}

    # ==========================================================
    # Revenue (special case)
    # ==========================================================

        revenue_aliases = [
            "payment_value",
            "order_total_inr",
            "gross_amount",
            "net_amount",
            "total_order_value",
            "selling_price",
            "discounted_price_inr",
            "sale_price",
            "amount",
            "price",
        ]

        revenue_ok = False

        if "revenue" in dataframe.columns:

            revenue = pd.to_numeric(
                dataframe["revenue"],
                errors="coerce",
            )

            if revenue.notna().sum() > 0:

                dataframe["revenue"] = revenue
                mapped_columns["revenue"] = "revenue"
                revenue_ok = True

        if not revenue_ok:

            for alias in revenue_aliases:

                real_column = normalized_columns.get(
                    self._normalize_column_name(alias)
                )

                if real_column is None:
                    continue

                values = pd.to_numeric(
                    dataframe[real_column],
                    errors="coerce",
                )

                if values.notna().sum() == 0:
                    continue

                dataframe["revenue"] = values

                mapped_columns["revenue"] = real_column


                break

    # ==========================================================
    # Everything else
    # ==========================================================

        for canonical, aliases in CANONICAL_ALIASES.items():

            if canonical == "revenue":
                continue

            if canonical in dataframe.columns:

                candidate = dataframe[canonical]

                if canonical in {
                    "quantity",
                    "discount",
                    "review_score",
                }:

                    candidate = pd.to_numeric(
                        candidate,
                        errors="coerce",
                    )

                if candidate.notna().sum() > 0:

                    dataframe[canonical] = candidate

                    mapped_columns[canonical] = canonical

                    continue

            for alias in aliases:

                real_column = normalized_columns.get(
                    self._normalize_column_name(alias)
                )

                if real_column is None:
                    continue

                candidate = dataframe[real_column]

                if canonical in {
                    "quantity",
                    "discount",
                    "review_score",
                }:

                    candidate = pd.to_numeric(
                        candidate,
                        errors="coerce",
                    )

                if candidate.notna().sum() == 0:
                    continue

                dataframe[canonical] = candidate

                mapped_columns[canonical] = real_column


                break

        return dataframe
    
    def _engineer_common_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Create reusable business features.

        The function must NEVER fail if columns are missing.
        """

    #
    # -----------------------------
    # Order Date Features
    # -----------------------------
    #

        if "order_date" in dataframe.columns:

            dataframe["order_date"] = pd.to_datetime(
                dataframe["order_date"],
                errors="coerce",
            )

            dataframe["order_year"] = (
                dataframe["order_date"]
                .dt.year
            )

            dataframe["order_month"] = (
                dataframe["order_date"]
                .dt.month
            )

            dataframe["order_week"] = (
                dataframe["order_date"]
                .dt.isocalendar()
                .week
                .astype("Int64")
            )

            dataframe["order_day"] = (
                dataframe["order_date"]
                .dt.day
            )

            dataframe["order_day_name"] = (
                dataframe["order_date"]
                .dt.day_name()
            )

            dataframe["order_quarter"] = (
                dataframe["order_date"]
                .dt.quarter
            )

    #
    # -----------------------------
    # Delivery Features
    # -----------------------------
    #

        if (
            "order_date" in dataframe.columns
            and
            "delivery_date" in dataframe.columns
        ):

            delivery = pd.to_datetime(
                dataframe["delivery_date"],
                errors="coerce",
            )

            dataframe["delivery_days"] = (
                delivery
                -
                dataframe["order_date"]
            ).dt.days

    #
    # -----------------------------
    # Customer Features
    # -----------------------------
    #

        if "customer_id" in dataframe.columns:

            dataframe["customer_orders"] = (

                dataframe
                .groupby("customer_id")["customer_id"]
                .transform("count")

            )

            dataframe["repeat_customer"] = (

                dataframe["customer_orders"] > 1

            )

    #
    # -----------------------------
    # Revenue Features
    # -----------------------------
    #

        if "revenue" in dataframe.columns:

            dataframe["revenue"] = pd.to_numeric(
                dataframe["revenue"],
                errors="coerce",
            )

            dataframe["average_order_value"] = (

                dataframe["revenue"]

            )

    #
    # -----------------------------
    # Discount %
    # -----------------------------
    #

        if (
            "discount" in dataframe.columns
            and
            "revenue" in dataframe.columns
        ):

            discount = pd.to_numeric(
                dataframe["discount"],
                errors="coerce",
            )

            revenue = pd.to_numeric(
                dataframe["revenue"],
                errors="coerce",
            )

            total = revenue + discount

            dataframe["discount_percentage"] = np.where(

                total > 0,

                (discount / total) * 100,

                np.nan,

            )

    #
    # -----------------------------
    # Review Features
    # -----------------------------
    #

        if "review_score" in dataframe.columns:

            dataframe["review_score"] = pd.to_numeric(
                dataframe["review_score"],
                errors="coerce",
            )

            dataframe["positive_review"] = (

                dataframe["review_score"] >= 4

            )

            dataframe["negative_review"] = (

                dataframe["review_score"] <= 2

            )

        engineered = [

            "delivery_days",

            "order_year",

            "order_month",

            "order_week",

            "customer_orders",

            "repeat_customer",

            "average_order_value",

            "discount_percentage",

        ]


        return dataframe


    @staticmethod
    def _normalize_column_name(
        column: str,
    ) -> str:
        """
        Normalize column names for matching.

        Examples
        --------
        Customer ID
        customer-id
        CUSTOMER_ID
        customerId

        →

        customerid
        """

        return re.sub(
            r"[^a-z0-9]",
            "",
            column.lower(),
        )