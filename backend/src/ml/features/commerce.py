"""Commerce feature builder."""

from __future__ import annotations

import pandas as pd

from src.ml.features.base import BaseFeatureBuilder


class CommerceFeatureBuilder(BaseFeatureBuilder):
    """
    Creates commerce analytics feature table.

    Converts raw commerce datasets into
    a unified business view.
    """


    def build(
        self,
        datasets: dict[str, pd.DataFrame],
    ) -> pd.DataFrame:


        if "orders" not in datasets:
            raise ValueError(
                "orders dataset required."
            )


        features = datasets[
            "orders"
        ].copy()


        # ----------------------------
        # Customers
        # ----------------------------

        customers = datasets.get(
            "customers",
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
        # Payments
        # ----------------------------

        payments = datasets.get(
            "payments",
        )


        if (
            payments is not None
            and "order_id" in payments.columns
        ):

            payments = (
                payments
                .groupby(
                    "order_id",
                    as_index=False,
                )
                .agg(
                    revenue=(
                        "payment_value",
                        "sum",
                    )
                )
            )


            features = features.merge(
                payments,
                on="order_id",
                how="left",
            )


        # ----------------------------
        # Reviews
        # ----------------------------

        reviews = datasets.get(
            "reviews",
        )


        if (
            reviews is not None
            and "order_id" in reviews.columns
        ):

            reviews = (
                reviews
                .groupby(
                    "order_id",
                    as_index=False,
                )
                .agg(
                    review_score=(
                        "review_score",
                        "mean",
                    )
                )
            )


            features = features.merge(
                reviews,
                on="order_id",
                how="left",
            )


        # ----------------------------
        # Order Items
        # ----------------------------

        items = datasets.get(
            "order_items",
        )


        if (
            items is not None
            and "order_id" in items.columns
        ):

            item_features = (
                items.groupby(
                    "order_id",
                    as_index=False,
                )
                .agg(
                    product_count=(
                        "product_id",
                        "count",
                    ),
                    total_price=(
                        "price",
                        "sum",
                    ),
                    freight_value=(
                        "freight_value",
                        "sum",
                    ),
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
            "products",
        )


        if (
            products is not None
            and items is not None
            and "product_id" in items.columns
        ):

            product_map = (
                items[
                    [
                        "order_id",
                        "product_id",
                    ]
                ]
                .merge(
                    products,
                    on="product_id",
                    how="left",
                )
            )


            product_map = (
                product_map.groupby(
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
            "sellers",
        )


        if (
            sellers is not None
            and items is not None
            and "seller_id" in items.columns
        ):

            seller_map = (
                items[
                    [
                        "order_id",
                        "seller_id",
                    ]
                ]
                .merge(
                    sellers,
                    on="seller_id",
                    how="left",
                )
            )


            seller_map = (
                seller_map.groupby(
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


        return features