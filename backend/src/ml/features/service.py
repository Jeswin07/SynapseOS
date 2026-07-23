"""Feature generation service."""

from __future__ import annotations

import logging
import uuid

import pandas as pd
from sqlalchemy.orm import Session

from src.ml.cache.feature_cache import (
    FeatureCache,
)
from src.ml.data.dataset_loader import (
    DatasetLoader,
)
from src.ml.data.version_resolver import (
    DatasetVersionResolver,
)
from src.ml.features.registry import (
    FeatureBuilderRegistry,
)
from src.modules.data.repository import (
    DatasetRepository,
)

logger = logging.getLogger(__name__)

class FeatureService:
    """
    Generates analytics and ML ready datasets.
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

        self.repository = DatasetRepository(
            db,
        )

        self.loader = DatasetLoader(
            db,
        )
        self.resolver = DatasetVersionResolver(
            self.repository,
        )


    def build_features(
        self,
        dataset_version_id: uuid.UUID | None = None,
        dataset_id: uuid.UUID | None = None,
        version_ids: list[uuid.UUID] | None = None,
        mode: str = "single",
    ) -> pd.DataFrame:

        logger.info(
            "Feature generation requested | dataset_id=%s dataset_version_id=%s mode=%s",
            dataset_id,
            dataset_version_id,
            mode,
        )

        try:

            versions = self.resolver.resolve(
                dataset_id=dataset_id,
                version_id=dataset_version_id,
                version_ids=version_ids,
                mode=mode,
            )

            logger.info(
                "Dataset versions resolved | versions=%d",
                len(versions),
            )

            cache_key = "|".join(
                sorted(
                    str(
                        version.id,
                    )
                    for version in versions
                )
            )

            cached = FeatureCache.get(
                cache_key,
            )

            if cached is not None:
                logger.info(
                    "Feature cache hit | cache_key=%s",
                    cache_key,
                )

                return cached.copy(
                    deep=False,
                )

            logger.info(
                "Feature cache miss | cache_key=%s",
                cache_key,
            )

            combined: dict[str, list[pd.DataFrame]] = {}

            logger.info(
                "Loading datasets | versions=%d",
                len(versions),
            )

            for version in versions:

                datasets = self.loader.load_version(
                    version.id,
                )

                logger.info(
                    "Loading datasets | versions=%d",
                    len(versions),
                )

                for name, frame in datasets.items():

                    combined.setdefault(
                        name,
                        [],
                    ).append(
                        frame,
                    )

            final_datasets = {

                name: pd.concat(
                    frames,
                    ignore_index=True,
                )

                for name, frames in combined.items()

            }

            logger.info(
                "Datasets combined | logical_datasets=%d",
                len(final_datasets),
            )

            dataset = self.repository.get_dataset(
                versions[0].dataset_id,
            )

            if dataset is None:

                raise ValueError(
                    "Dataset not found.",
                )

            logger.info(
                "Dataset loaded | dataset_id=%s business_domain=%s",
                dataset.id,
                dataset.business_domain,
            )

            builder = FeatureBuilderRegistry.get_builder(
                dataset.business_domain,
            )

            logger.info(
                "Feature builder selected | domain=%s builder=%s",
                dataset.business_domain,
                builder.__class__.__name__,
            )

            features = builder.build(
                final_datasets,
            )

            logger.info(
                "Feature generation completed | rows=%d columns=%d",
                len(features),
                len(features.columns),
            )

            FeatureCache.set(
                cache_key,
                features,
            )

            return features.copy(
                deep=False,
        )

        except Exception:
            logger.exception(
                "Feature generation failed | dataset_id=%s dataset_version_id=%s",
                dataset_id,
                dataset_version_id,
            )
            raise   