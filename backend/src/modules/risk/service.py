"""Risk service."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from src.ml.risk.engine import RiskEngine
from src.modules.prediction.repository import (
    PredictionRepository,
)


class RiskService:
    """
    Risk application layer.

    Uses previous ML prediction results
    and converts them into business risks.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.repository = PredictionRepository(
            db,
        )

        self.engine = RiskEngine()


    def analyze(
        self,
        *,
        created_by: UUID,
    ) -> dict:
        """
        Analyze business risk.
        """

        predictions = (
            self.repository.latest(
                created_by=created_by,
                limit=10,
            )
        )


        return self.engine.analyze(
            predictions,
        )