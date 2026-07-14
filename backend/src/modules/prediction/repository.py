"""Prediction repository."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from src.models.prediction import (
    PredictionRun,
)


class PredictionRepository:
    """
    Handles prediction persistence.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db


    def create(
        self,
        *,
        created_by: UUID,
        dataset_version_id: UUID,
        prediction_type: str,
        result: dict,
    ) -> PredictionRun:
        """
        Save prediction execution result.
        """

        run = PredictionRun(
            created_by=created_by,
            dataset_version_id=dataset_version_id,
            prediction_type=prediction_type,
            result=result,
        )


        self.db.add(
            run,
        )

        self.db.commit()

        self.db.refresh(
            run,
        )


        return run


    def list(
        self,
        created_by: UUID,
    ) -> list[PredictionRun]:
        """
        Get prediction history for a user.
        """

        return (
            self.db.query(
                PredictionRun,
            )
            .filter(
                PredictionRun.created_by
                ==
                created_by
            )
            .order_by(
                PredictionRun.created_at.desc(),
            )
            .all()
        )
    
    def latest(
        self,
        *,
        created_by: UUID,
        limit: int = 10,
    ) -> list[PredictionRun]:
        """
        Get latest prediction runs for risk analysis.
        """

        return (
            self.db.query(
                PredictionRun,
            )
            .filter(
                PredictionRun.created_by
                ==
                created_by,
            )
            .order_by(
                PredictionRun.created_at.desc(),
            )
            .limit(
                limit,
            )
            .all()
        )