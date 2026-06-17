import polars as pl


class FeatureEngineer:
    """
    Generate machine learning features from the merged Olist dataset.
    """

    def transform(
        self,
        dataframe: pl.DataFrame,
    ) -> pl.DataFrame:

        dataframe = dataframe.with_columns(

            # Purchase timestamp
            pl.col("order_purchase_timestamp")
            .dt.year()
            .alias("purchase_year"),

            pl.col("order_purchase_timestamp")
            .dt.month()
            .alias("purchase_month"),

            pl.col("order_purchase_timestamp")
            .dt.weekday()
            .alias("purchase_weekday"),

            pl.col("order_purchase_timestamp")
            .dt.hour()
            .alias("purchase_hour"),

            # Delivery duration
            (
                pl.col("order_delivered_customer_date")
                -
                pl.col("order_purchase_timestamp")
            )
            .dt.total_days()
            .alias("delivery_days"),

            (
                pl.col("order_estimated_delivery_date")
                -
                pl.col("order_purchase_timestamp")
            )
            .dt.total_days()
            .alias("estimated_delivery_days"),

            # Product volume
            (
                pl.col("product_length_cm")
                *
                pl.col("product_height_cm")
                *
                pl.col("product_width_cm")
            ).alias("product_volume_cm3"),
        )

        dataframe = dataframe.with_columns(

            # Delivery delay
            (
                pl.col("delivery_days")
                -
                pl.col("estimated_delivery_days")
            ).alias("delivery_delay"),

            # Weekend purchase
            (
                pl.col("purchase_weekday") >= 5
            ).cast(pl.Int8)
            .alias("weekend_purchase"),

            # Freight ratio
            (
                pl.col("freight_value")
                /
                (
                    pl.col("price")
                    + 1
                )
            ).alias("freight_ratio"),

            # Price per KG
            (
                pl.col("price")
                /
                (
                    pl.col("product_weight_g")
                    / 1000
                    + 0.001
                )
            ).alias("price_per_kg"),
        )

        return dataframe