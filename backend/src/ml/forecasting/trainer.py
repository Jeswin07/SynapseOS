from uuid import UUID

from src.core.storage.artifact_storage import (
    FORECAST_ARTIFACTS_DIR,
    ensure_artifact_directories,
)
from src.ml.forecasting.detector import (
    ForecastColumnDetector,
)
from src.ml.forecasting.prophet_trainer import (
    ProphetTrainer,
)
from src.ml.preprocessing.loader import (
    DatasetLoader,
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
        frequency: str = "D",
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
            frequency=frequency,
        )

        ensure_artifact_directories()

        artifact_path = (
            FORECAST_ARTIFACTS_DIR
            / f"{forecast_id}.joblib"
        )

        self.trainer.save(
            model,
            str(artifact_path),
        )

        return str(artifact_path)


