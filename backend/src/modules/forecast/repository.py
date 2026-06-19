import uuid

from sqlalchemy.orm import Session

from src.models.dataset_version import DatasetVersion
from src.models.forecast_model import ForecastModel


class ForecastRepository:
    """
    Forecast repository.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

    def get_latest_dataset_version(
        self,
        dataset_id: uuid.UUID,
    ) -> DatasetVersion | None:
        """
        Get latest dataset version.
        """

        return (
            self.db.query(
                DatasetVersion,
            )
            .filter(
                DatasetVersion.dataset_id == dataset_id,
            )
            .order_by(
                DatasetVersion.version.desc(),
            )
            .first()
        )

    def create(
        self,
        forecast: ForecastModel,
    ) -> None:

        self.db.add(
            forecast,
        )

    def refresh(
        self,
        forecast: ForecastModel,
    ) -> None:

        self.db.refresh(
            forecast,
        )

    def commit(
        self,
    ) -> None:

        self.db.commit()

    def rollback(
        self,
    ) -> None:

        self.db.rollback()

    def get_by_id(
        self,
        forecast_id: uuid.UUID,
    ) -> ForecastModel | None:

        return (
            self.db.query(
                ForecastModel,
            )
            .filter(
                ForecastModel.id == forecast_id,
            )
            .first()
        )