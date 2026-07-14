"""Prediction business explanations."""


class PredictionExplainer:
    """Creates business drivers."""


    def explain(
        self,
        row,
    ) -> list[str]:

        drivers = []


        if row.get(
            "total_orders",
            99,
        ) <= 1:

            drivers.append(
                "Low repeat purchase activity",
            )


        if row.get(
            "average_review",
            5,
        ) < 3:

            drivers.append(
                "Below average satisfaction",
            )


        if row.get(
            "late_deliveries",
            0,
        ) > 0:

            drivers.append(
                "Delivery issues experienced",
            )


        return drivers or [
            "Customer behaviour indicates risk"
        ]