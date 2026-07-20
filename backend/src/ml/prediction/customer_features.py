"""Customer feature engineering for prediction."""

from __future__ import annotations

import pandas as pd


class CustomerFeatureBuilder:
    """
    Builds customer-level commerce intelligence features.

    Used by:
    - Predict Tool
    - Risk Tool
    - Scenario Agent
    """


    def build(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """Convert transactions into customer features."""

        frame = data.copy()


        customer_column = self._customer_column(
            frame,
        )


        frame["prediction_customer_id"] = (
            frame[customer_column]
            .astype(str)
        )


        aggregations = {}


        if "revenue" in frame.columns:

            aggregations["revenue"] = [
                "sum",
                "mean",
            ]

        if "order_date" in frame.columns:
            frame["order_date"] = pd.to_datetime(
                frame["order_date"],
                errors="coerce",
            )

            aggregations["order_date"] = "max"


        if "review_score" in frame.columns:

            aggregations["review_score"] = [
                "mean",
            ]


        if "delivery_delay_days" in frame.columns:

            aggregations[
                "delivery_delay_days"
            ] = [
                "mean",
                lambda value: (
                    value > 0
                ).sum(),
            ]


        customers = (
            frame
            .groupby(
                "prediction_customer_id",
            )
            .agg(
                aggregations,
            )
        )


        customers.columns = [
            "_".join(
                map(
                    str,
                    column,
                )
            )
            for column in customers.columns
        ]


        customers = (
            customers
            .reset_index()
            .rename(
                columns={
                    "prediction_customer_id":
                        "customer_id",

                    "revenue_sum":
                        "total_revenue",

                    "revenue_mean":
                        "average_order_value",

                    "review_score_mean":
                        "average_review",

                    "delivery_delay_days_mean":
                        "average_delivery_delay",

                    "delivery_delay_days_<lambda_0>":
                        "late_deliveries",

                    "order_date_max": "last_order_date",
                }
            )
        )
        print(customers.columns)


        orders = (
            frame.groupby(
                "prediction_customer_id",
            )
            .size()
            .reset_index(
                name="total_orders",
            )
        )


        customers = customers.merge(
            orders,
            left_on="customer_id",
            right_on="prediction_customer_id",
            how="left",
        )


        customers.drop(
            columns=[
                "prediction_customer_id",
            ],
            inplace=True,
        )


        defaults = {
            "total_revenue": 0,
            "average_order_value": 0,
            "average_review": 0,
            "average_delivery_delay": 0,
            "late_deliveries": 0,
        }


        for column, value in defaults.items():

            if column not in customers:

                customers[column] = value

        print(customers.head())
        print(customers.columns)
        
        return customers.fillna(
            0,
        )


    def _customer_column(
        self,
        frame: pd.DataFrame,
    ) -> str:
        """
        Find real customer identifier.
        """

        priority = [
            "customer_unique_id",
            "customer_id",
            "user_id",
            "client_id",
        ]


        for column in priority:

            if column in frame.columns:

                return column


        frame["generated_customer_id"] = (
            frame.index.astype(str)
        )


        return "generated_customer_id"