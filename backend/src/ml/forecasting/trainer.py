from pathlib import Path
from uuid import UUID

from src.ml.forecasting.prophet_trainer import (
    ProphetTrainer,
)
from src.ml.preprocessing.loader import (
    DatasetLoader,
)
from src.ml.forecasting.detector import (
    ForecastColumnDetector,
)


class ForecastTrainer:
    """
    Orchestrates forecast model training.
    """

    def __init__(self) -> None:

        self.loader = DatasetLoader()

        self.trainer = ProphetTrainer()

        self.detector = ForecastColumnDetector()

    def train(
        self,
        *,
        dataframe,
        forecast_id: UUID,
        aggregation: str,
        date_column: str | None = None,
        target_column: str | None = None,
    ) -> str:
        """
        Train a forecasting model.

        Returns:
            Artifact path.
        """

        if (
            date_column is None
            or target_column is None
        ):

            columns = self.detector.detect(
                dataframe
            )

            date_column = (
                date_column
                or columns["date_column"]
            )

            target_column = (
                target_column
                or columns["target_column"]
            )

        model = self.trainer.train(
            dataframe,
            date_column=date_column,
            target_column=target_column,
            aggregation=aggregation,
        )

        Path(
            "artifacts/forecast",
        ).mkdir(
            parents=True,
            exist_ok=True,
        )

        artifact_path = (
            f"artifacts/forecast/{forecast_id}.joblib"
        )

        self.trainer.save(
            model,
            artifact_path,
        )

        return artifact_path


