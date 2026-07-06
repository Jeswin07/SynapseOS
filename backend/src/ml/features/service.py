"""Feature generation service."""

from __future__ import annotations

import uuid

import pandas as pd
from sqlalchemy.orm import Session

from src.ml.data.dataset_loader import (
    DatasetLoader,
)

from src.ml.features.registry import (
    FeatureBuilderRegistry,
)

from src.modules.data.repository import (
    DatasetRepository,
)
from src.ml.data.version_resolver import (
    DatasetVersionResolver,
)

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


        versions = self.resolver.resolve(
            dataset_id=dataset_id,
            version_id=dataset_version_id,
            version_ids=version_ids,
            mode=mode,
        )


        combined = {}


        for version in versions:

            datasets = self.loader.load_version(
                version.id,
            )


            for name, frame in datasets.items():

                if name not in combined:
                    combined[name] = []

                combined[name].append(
                    frame,
                )


        final_datasets = {
            name: pd.concat(
                frames,
                ignore_index=True,
            )
            for name, frames in combined.items()
        }


        dataset = (
            self.repository.get_dataset(
                versions[0].dataset_id,
            )
        )

        if dataset is None:
            raise ValueError(
                "Dataset not found."
            )
        
        builder = (
            FeatureBuilderRegistry
            .get_builder(
                dataset.business_domain,
            )
        )


        return builder.build(
            final_datasets,
        )