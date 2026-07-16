"""Commerce feature builder."""

from __future__ import annotations

import pandas as pd

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
        print(features[["revenue"]].head())
        print(features["revenue"].dtype)
        print(features.columns.tolist())
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
        Add enterprise canonical columns without removing
        original dataset columns.

        Existing code continues to work while newer modules
        can rely on standardized names.
        """

        aliases = {

            "revenue": [
                "payment_value",
                "selling_price",
                "sale_price",
                "price",
                "amount",
                "sales",
                "revenue",
                "total_amount",
            ],

            "customer_id": [
                "customer_unique_id",
                "customer_id",
                "buyer_id",
                "user_id",
            ],

            "seller_id": [
                "seller_id",
                "merchant_id",
                "vendor_id",
            ],

            "category": [
                "product_category_name",
                "category",
                "product_category",
                "vertical",
            ],

            "brand": [
                "brand",
                "manufacturer",
            ],

            "order_date": [
                "order_purchase_timestamp",
                "purchase_date",
                "order_date",
                "created_at",
                "date",
            ],

            "delivery_date": [
                "order_delivered_customer_date",
                "delivery_date",
            ],

            "estimated_delivery_date": [
                "order_estimated_delivery_date",
                "estimated_delivery_date",
            ],

            "review_score": [
                "review_score",
                "rating",
                "stars",
            ],

            "state": [
                "customer_state",
                "state",
                "province",
            ],

            "city": [
                "customer_city",
                "city",
            ],

            "quantity": [
                "quantity",
                "qty",
            ],

            "discount": [
                "discount",
                "discount_amount",
            ],
        }

        lower = {
            c.lower(): c
            for c in dataframe.columns
        }

        for canonical, possible in aliases.items():

            if canonical in dataframe.columns:
                continue

            for alias in possible:

                real = lower.get(alias.lower())

                if real:

                    dataframe[canonical] = dataframe[real]

                    break

        return dataframe
    
    def _engineer_common_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        if "order_date" in dataframe.columns:

            dates = pd.to_datetime(
                dataframe["order_date"],
                errors="coerce",
            )

            dataframe["year"] = dates.dt.year

            dataframe["month"] = dates.dt.month

            dataframe["quarter"] = dates.dt.quarter

            dataframe["weekday"] = dates.dt.day_name()

            dataframe["week"] = dates.dt.isocalendar().week.astype("Int64")

        if (
            "delivery_date" in dataframe.columns
            and
            "order_date" in dataframe.columns
        ):

            delivery = pd.to_datetime(
                dataframe["delivery_date"],
                errors="coerce",
            )

            purchase = pd.to_datetime(
                dataframe["order_date"],
                errors="coerce",
            )

            dataframe["delivery_days"] = (
                delivery - purchase
            ).dt.days

        if (
            "estimated_delivery_date" in dataframe.columns
            and
            "delivery_date" in dataframe.columns
        ):

            estimated = pd.to_datetime(
                dataframe["estimated_delivery_date"],
                errors="coerce",
            )

            delivered = pd.to_datetime(
                dataframe["delivery_date"],
                errors="coerce",
            )

            dataframe["delivery_delay_days"] = (
                delivered - estimated
            ).dt.days

        return dataframe