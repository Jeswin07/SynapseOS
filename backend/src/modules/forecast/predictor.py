
import joblib
from prophet import Prophet


class ForecastPredictor:
    """
    Generate forecasts using a trained Prophet model.
    """

    def predict(
        self,
        *,
        artifact_path: str,
        periods: int,
        frequency: str = "D",
    ) -> list[dict]:

        model: Prophet = joblib.load(
            artifact_path,
        )

        future = model.make_future_dataframe(
            periods=periods,
            freq=frequency,
        )

        forecast = model.predict(
            future,
        )

        future_rows = forecast.tail(
            periods,
        )
        print(future_rows[["ds", "yhat", "yhat_lower", "yhat_upper"]])

        return [
            {
                "date": row.ds.strftime(
                    "%Y-%m-%d",
                ),
                "prediction": round(
                    max(float(row.yhat),0),
                    2,
                ),
                "lower": round(
                    max(float(row.yhat_lower),0),
                    2,
                ),
                "upper": round(
                    max(float(row.yhat_upper),0),
                    2,
                ),
            }
            for _, row in future_rows.iterrows()
        ]