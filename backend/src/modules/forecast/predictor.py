
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
    ) -> list[dict]:

        model: Prophet = joblib.load(
            artifact_path,
        )

        future = model.make_future_dataframe(
            periods=periods,
            freq="D",
        )

        forecast = model.predict(
            future,
        )

        future_rows = forecast.tail(
            periods,
        )

        return [
            {
                "date": row.ds.strftime(
                    "%Y-%m-%d",
                ),
                "prediction": round(
                    float(row.yhat),
                    2,
                ),
                "lower": round(
                    float(row.yhat_lower),
                    2,
                ),
                "upper": round(
                    float(row.yhat_upper),
                    2,
                ),
            }
            for _, row in future_rows.iterrows()
        ]