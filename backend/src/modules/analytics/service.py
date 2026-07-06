"""Business analytics service."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from src.ml.analytics.commerce import (
    CommerceAnalyticsEngine,
)

from src.ml.features.service import (
    FeatureService,
)


class AnalyticsService:
    """
    Generates business intelligence analytics.
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        self.feature_service = FeatureService(
            db,
        )

        self.engine = CommerceAnalyticsEngine()


    def analyze(
        self,
        dataset_version_id: uuid.UUID,
    ) -> dict:
        """
        Generate analytics from dataset features.
        """


        features = (
            self.feature_service.build_features(
                dataset_version_id=dataset_version_id,
            )
        )


        return self.engine.analyze(
            features,
        )