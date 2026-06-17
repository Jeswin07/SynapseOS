import polars as pl


class OlistJoiner:
    """
    Joins all Olist datasets into a single dataframe.
    """

    def join(
        self,
        *,
        orders: pl.DataFrame,
        order_items: pl.DataFrame,
        products: pl.DataFrame,
        customers: pl.DataFrame,
        payments: pl.DataFrame,
        reviews: pl.DataFrame,
        translations: pl.DataFrame,
    ) -> pl.DataFrame:
        """
        Join all datasets.
        """

        # Products + English Category Names
        products = (
            products.join(
                translations,
                on="product_category_name",
                how="left",
            )
        )

        # Order Items + Product Details
        order_items = (
            order_items.join(
                products,
                on="product_id",
                how="left",
            )
        )

        # Orders + Customers
        dataframe = (
            orders.join(
                customers,
                on="customer_id",
                how="left",
            )
        )

        # + Order Items
        dataframe = (
            dataframe.join(
                order_items,
                on="order_id",
                how="left",
            )
        )

        # Payments
        payments = (
            payments.group_by(
                "order_id",
            ).agg(
                [
                    pl.sum("payment_value").alias(
                        "payment_value",
                    ),
                    pl.first("payment_type").alias(
                        "payment_type",
                    ),
                    pl.max("payment_installments").alias(
                        "payment_installments",
                    ),
                ]
            )
        )

        dataframe = (
            dataframe.join(
                payments,
                on="order_id",
                how="left",
            )
        )

        # Reviews
        reviews = (
            reviews.select(
                [
                    "order_id",
                    "review_score",
                ]
            )
        )

        dataframe = (
            dataframe.join(
                reviews,
                on="order_id",
                how="left",
            )
        )

        return dataframe