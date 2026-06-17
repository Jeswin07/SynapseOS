import uuid

from sqlalchemy.orm import Session

from src.models.dataset_version import DatasetVersion
from src.models.ml_model import MLModel


class MLRepository:
    """
    Repository for machine learning operations.
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
        Retrieve the latest dataset version.
        """

        return (
            self.db.query(DatasetVersion)
            .filter(
                DatasetVersion.dataset_id == dataset_id,
            )
            .order_by(
                DatasetVersion.version.desc(),
            )
            .first()
        )

    def create_model(
        self,
        model: MLModel,
    ) -> None:
        """
        Persist a trained model.
        """

        self.db.add(model)

    def commit(
        self,
    ) -> None:

        self.db.commit()

    def rollback(
        self,
    ) -> None:

        self.db.rollback()

    def refresh(
        self,
        model: MLModel,
    ) -> None:

        self.db.refresh(model)

    def get_model_by_id(
        self,
        model_id: uuid.UUID,
    ) -> MLModel | None:
        """
        Retrieve model by ID.
        """

        return (
            self.db.query(MLModel)
            .filter(
                MLModel.id == model_id,
            )
            .first()
        )
    
    def list_training_group(
        self,
        training_group: uuid.UUID,
    ) -> list[MLModel]:

        return (
            self.db.query(MLModel)
            .filter(
                MLModel.training_group == training_group,
            )
            .all()
        )