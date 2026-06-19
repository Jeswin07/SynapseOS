import uuid

from sqlalchemy.orm import Session

from src.ml.forecasting.trainer import ForecastTrainer
from src.models.forecast_model import ForecastModel
from src.modules.forecast.predictor import (
    ForecastPredictor,
)
from src.modules.forecast.repository import ForecastRepository
from src.shared.logging import logger


class ForecastService:
    """
    Forecast service.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.repository = ForecastRepository(db)

        self.trainer = ForecastTrainer()

        self.predictor = ForecastPredictor()

    def train(
        self,
        *,
        dataset_id: uuid.UUID,
        created_by: uuid.UUID,
        date_column: str,
        target_column: str,
        aggregation: str = "sum",
    ) -> ForecastModel:
        """
        Train a Prophet forecasting model.
        """

        latest_version = (
            self.repository.get_latest_dataset_version(
                dataset_id,
            )
        )

        if latest_version is None:
            raise ValueError(
                "Dataset version not found."
            )

        forecast = ForecastModel(
            dataset_id=dataset_id,
            name=f"forecast-{dataset_id}",
            date_column=date_column,
            target_column=target_column,
            artifact_path="",
            created_by=created_by,
        )

        try:

            self.repository.create(
                forecast,
            )

            self.repository.commit()

            self.repository.refresh(
                forecast,
            )

            artifact_path = (
                self.trainer.train(
                    storage_path=latest_version.storage_path,
                    date_column=date_column,
                    target_column=target_column,
                    forecast_id=forecast.id,
                    aggregation=aggregation,
                )
            )

            forecast.artifact_path = artifact_path

            self.repository.commit()

            self.repository.refresh(
                forecast,
            )

            logger.info(
                "Forecast model trained successfully.",
                extra={
                    "forecast_id": str(forecast.id),
                },
            )

            return forecast

        except Exception as exc:

            self.repository.rollback()

            logger.exception(
                "Forecast training failed.",
                extra={
                    "dataset_id": str(dataset_id),
                },
            )

            raise exc

    def predict(
        self,
        *,
        forecast_id: uuid.UUID,
        periods: int,
    ):

        forecast = self.repository.get_by_id(
            forecast_id,
        )

        if forecast is None:
            raise ValueError(
                "Forecast model not found."
            )

        return self.predictor.predict(
            artifact_path=forecast.artifact_path,
            periods=periods,
        )