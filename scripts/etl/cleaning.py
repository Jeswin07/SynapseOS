import polars as pl


class DataCleaner:
    """
    Cleans the engineered Olist dataset for machine learning.
    """

    def clean(
        self,
        dataframe: pl.DataFrame,
    ) -> pl.DataFrame:
        """
        Clean dataset.
        """

        # Remove cancelled / unavailable orders
        dataframe = dataframe.filter(
            pl.col("order_status").is_in(
                [
                    "delivered",
                ]
            )
        )

        # Remove duplicate orders
        dataframe = dataframe.unique(
            subset=["order_id"],
        )

        # Remove rows without target values
        dataframe = dataframe.filter(
            pl.col("price").is_not_null()
            &
            pl.col("payment_value").is_not_null()
            &
            pl.col("review_score").is_not_null()
        )

        # Remove impossible delivery dates
        dataframe = dataframe.filter(
            (
                pl.col("delivery_days").is_null()
            )
            |
            (
                pl.col("delivery_days") >= 0
            )
        )

        # Fill missing numeric values
        dataframe = dataframe.with_columns(

            pl.col("product_weight_g").fill_null(0),

            pl.col("product_length_cm").fill_null(0),

            pl.col("product_height_cm").fill_null(0),

            pl.col("product_width_cm").fill_null(0),

            pl.col("product_volume_cm3").fill_null(0),

            pl.col("delivery_delay").fill_null(0),

            pl.col("freight_ratio").fill_null(0),

            pl.col("price_per_kg").fill_null(0),
        )

        # Fill missing categorical values
        dataframe = dataframe.with_columns(

            pl.col(
                "product_category_name_english"
            ).fill_null("Unknown"),

            pl.col(
                "payment_type"
            ).fill_null("Unknown"),

            pl.col(
                "customer_state"
            ).fill_null("Unknown"),
        )

        # Keep only useful columns
        dataframe = dataframe.select(

            [
                "order_id",

                "order_purchase_timestamp",

                "customer_state",

                "product_category_name_english",

                "price",

                "freight_value",

                "payment_value",

                "payment_type",

                "payment_installments",

                "review_score",

                "product_weight_g",

                "product_length_cm",

                "product_height_cm",

                "product_width_cm",

                "product_volume_cm3",

                "purchase_year",

                "purchase_month",

                "purchase_weekday",

                "purchase_hour",

                "weekend_purchase",

                "delivery_days",

                "estimated_delivery_days",

                "delivery_delay",

                "freight_ratio",

                "price_per_kg",
            ]
        )

        return dataframe