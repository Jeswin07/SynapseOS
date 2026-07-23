"""Risk service."""

from __future__ import annotations

import logging
from uuid import UUID

from sqlalchemy.orm import Session

from src.ml.risk.engine import RiskEngine
from src.modules.prediction.repository import (
    PredictionRepository,
)

logger = logging.getLogger(__name__)

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
        try:
            logger.info(
                "Risk analysis requested | user_id=%s",
                created_by,
            )

            predictions = (
                self.repository.latest(
                    created_by=created_by,
                    limit=10,
                )
            )

            result = self.engine.analyze(
                predictions,
            )

            logger.info(
                "Risk analysis completed | user_id=%s overall_risk=%s",
                created_by,
                result["overall_risk"],
            )
        except:
            logger.exception(
                "Risk analysis failed | user_id=%s",
                created_by,
            )
            raise

        return result