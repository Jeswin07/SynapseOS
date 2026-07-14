class IntentRouter:

    def route(self, message: str) -> str | None:

        message = message.lower()

        prediction_words = [
            "predict",
            "prediction",
            "forecast churn",
            "customer churn",
            "delivery delay",
        ]

        analytics_words = [
            "analytics",
            "dashboard",
            "summary",
            "insights",
            "sales",
            "revenue",
            "customers",
            "orders",
            "why did",
            "trend",
        ]

        forecast_words = [
            "forecast",
            "future",
            "next month",
            "next quarter",
            "next year",
            "projection",
        ]

        risk_words = [
            "risk",
            "risks",
            "business risk",
            "high risk",
        ]

        if any(x in message for x in prediction_words):
            return "prediction"

        if any(x in message for x in analytics_words):
            return "analytics"

        if any(x in message for x in forecast_words):
            return "forecast"

        if any(x in message for x in risk_words):
            return "risk"

        return None