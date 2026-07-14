from uuid import UUID

from sqlalchemy.orm import Session

from src.models.dataset_file import DatasetFile
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
        dataset_id: UUID,
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
        forecast_id: UUID,
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

    
    def get_latest_forecast(
        self,
        dataset_id,
    ):

        return (
            self.db.query(
                ForecastModel,
            )
            .filter(
                ForecastModel.dataset_id
                ==
                dataset_id,
            )
            .order_by(
                ForecastModel.created_at.desc(),
            )
            .first()
        )
    
    def get_dataset_version(
        self,
        version_id: UUID,
    ) -> DatasetVersion | None:

        return (
            self.db.query(
                DatasetVersion,
            )
            .filter(
                DatasetVersion.id == version_id,
            )
            .first()
        )


    def get_version_files(
        self,
        version_id: UUID,
    ):

        return (
            self.db.query(
                DatasetFile,
            )
            .filter(
                DatasetFile.dataset_version_id
                ==
                version_id,
            )
            .all()
        )

    def get_existing_forecast(
        self,
        *,
        dataset_id,
        target_column: str,
        aggregation: str,
        frequency: str,
    ):

        return (
            self.db
            .query(
                ForecastModel,
            )
            .filter(
                ForecastModel.dataset_id
                ==
                dataset_id,

                ForecastModel.target_column
                ==
                target_column,

                ForecastModel.aggregation
                ==
                aggregation,

                ForecastModel.frequency
                ==
                frequency,
            )
            .order_by(
                ForecastModel.created_at.desc(),
            )
            .first()
        )