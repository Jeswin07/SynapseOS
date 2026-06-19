import uuid

from sqlalchemy.orm import Session

from src.ml.risk.trainer import RiskTrainer
from src.models.risk_analysis import RiskAnalysis
from src.modules.risk.repository import RiskRepository
from src.shared.logging import logger


class RiskService:
    """
    Risk analysis service.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.repository = RiskRepository(db)

        self.trainer = RiskTrainer()

    def analyze(
        self,
        *,
        dataset_id: uuid.UUID,
        created_by: uuid.UUID,
    ) -> tuple[RiskAnalysis, dict]:
        """
        Analyze a dataset for anomalies.
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

        result = self.trainer.analyze(
            storage_path=latest_version.storage_path,
        )

        risk = RiskAnalysis(
            dataset_id=dataset_id,
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            anomalies=result["anomalies"],
            anomaly_indices=result["anomaly_indices"],
            created_by=created_by,
        )

        try:

            self.repository.create(
                risk,
            )

            self.repository.commit()

            self.repository.refresh(
                risk,
            )

            logger.info(
                "Risk analysis completed.",
                extra={
                    "risk_id": str(risk.id),
                },
            )

            return (
                risk,
                result,
            )

        except Exception as exc:

            self.repository.rollback()

            logger.exception(
                "Risk analysis failed.",
                extra={
                    "dataset_id": str(dataset_id),
                },
            )

            raise exc