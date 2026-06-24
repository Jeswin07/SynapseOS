import numpy as np
import polars as pl
from sklearn.ensemble import IsolationForest

from src.ml.risk.preprocessor import (
    RiskPreprocessor,
)


class RiskDetector:
    """
    Detect anomalies using Isolation Forest.
    """

    def analyze(
        self,
        dataframe: pl.DataFrame,
    ) -> dict:

        preprocessor = RiskPreprocessor()

        x, _ = preprocessor.prepare(
            dataframe,
        )

        print(
            "Shape:",
            x.shape,
        )

        model = IsolationForest(
            contamination=0.02,
            random_state=42,
            n_jobs=-1,
        )

        predictions = model.fit_predict(
            x,
        )

        anomaly_indices = np.where(
            predictions == -1
        )[0].tolist()

        anomaly_count = int(
            (predictions == -1).sum()
        )

        total_rows = len(
            predictions,
        )

        print(
            "Anomalies:",
            anomaly_count,
        )

        risk_score = (
            anomaly_count / total_rows
        ) * 100

        if risk_score < 5:
            risk_level = "LOW"

        elif risk_score < 15:
            risk_level = "MEDIUM"

        else:
            risk_level = "HIGH"

        if risk_level == "LOW":

            summary = (
                "Only a small percentage of records are anomalous. "
                "The dataset appears healthy."
            )

        elif risk_level == "MEDIUM":

            summary = (
                "Several unusual records were detected. "
                "Review the anomalies before making decisions."
            )

        else:

            summary = (
                "A high number of anomalies were detected. "
                "The dataset requires investigation."
            )

        return {
            "risk_score": round(
                risk_score,
                2,
            ),
            "risk_level": risk_level,
            "anomalies": anomaly_count,
            "rows": total_rows,
            "anomaly_indices": anomaly_indices,
            "summary":summary
        }