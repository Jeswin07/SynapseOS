from pathlib import Path
from uuid import UUID

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

    def train(
        self,
        *,
        storage_path: str,
        date_column: str,
        target_column: str,
        forecast_id: UUID,
        aggregation: str
    ) -> str:
        """
        Train a forecasting model.

        Returns:
            Artifact path.
        """

        dataframe = self.loader.load_csv(
            storage_path,
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