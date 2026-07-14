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
from src.ml.cache.analytics_cache import (
    AnalyticsCache,
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

        cache_key = str(
            dataset_version_id,
        )

        cached = AnalyticsCache.get(
            cache_key,
        )

        if cached is not None:
            return cached

        features = (
            self.feature_service.build_features(
                dataset_version_id=dataset_version_id,
            )
        )

        result = self.engine.analyze(
            features,
        )

        AnalyticsCache.set(
            cache_key,
            result,
        )

        return result