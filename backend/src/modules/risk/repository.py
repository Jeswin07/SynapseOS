import uuid

from sqlalchemy.orm import Session

from src.models.dataset_version import DatasetVersion
from src.models.risk_analysis import RiskAnalysis


class RiskRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def get_latest_dataset_version(
        self,
        dataset_id: uuid.UUID,
    ):

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
        risk: RiskAnalysis,
    ):

        self.db.add(risk)

    def commit(self):

        self.db.commit()

    def rollback(self):

        self.db.rollback()

    def refresh(
        self,
        risk: RiskAnalysis,
    ):

        self.db.refresh(risk)