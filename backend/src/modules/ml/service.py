import uuid

import polars as pl
from sqlalchemy.orm import Session

from src.ml.algorithms.registry import (
    AlgorithmRegistry,
)
from src.ml.automl import AutoMLRunner
from src.ml.explainability.explainer import (
    ModelExplainer,
)
from src.ml.mlflow_manager import (
    MLflowManager,
)
from src.ml.training.trainer import MLTrainer
from src.ml.utils.model_loader import (
    ModelLoader,
)
from src.models.ml_model import MLModel
from src.modules.ml.repository import MLRepository
from src.shared.logging import logger


class MLService:
    """
    Machine Learning service.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.repository = MLRepository(db)

        self.trainer = MLTrainer()

        self.explainer = ModelExplainer()

    def train_model(
        self,
        *,
        dataset_id: uuid.UUID,
        created_by: uuid.UUID,
        algorithm: str,
        target_column: str,
        time_column: str,
        training_group: uuid.UUID | None = None,
    ) -> MLModel:
        """
        Train a machine learning model.
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
        
        if training_group is None:
            training_group = uuid.uuid4()

        model = MLModel(
            dataset_id=dataset_id,
            name=f"{algorithm}-{dataset_id}",
            algorithm=algorithm,
            target_column=target_column,
            time_column=time_column,
            metrics={},
            artifact_path="",
            created_by=created_by,
            training_group=training_group,
            is_best=False
        )

        try:

            self.repository.create_model(
                model,
            )

            self.repository.commit()

            self.repository.refresh(
                model,
            )

            artifact_path, metrics = (
                self.trainer.train(
                    storage_path=latest_version.storage_path,
                    algorithm=algorithm,
                    target_column=target_column,
                    time_column=time_column,
                    model_id=model.id,
                )
            )

            model.artifact_path = artifact_path

            model.metrics = {
                "dataset": {
                    "rows": metrics.rows,
                    "features": metrics.features,
                    "target": target_column,
                },
                "training": {
                    "algorithm": algorithm,
                    "time_seconds": metrics.training_time_seconds,
                },
                "metrics": {
                    "mse": metrics.mse,
                    "rmse": metrics.rmse,
                    "mae": metrics.mae,
                    "r2": metrics.r2,
                },
            }

            MLflowManager().log_training(
                algorithm=algorithm,
                metrics=model.metrics,
                artifact_path=artifact_path,
            )

            self.repository.commit()

            self.repository.refresh(
                model,
            )

            logger.info(
                "Model trained successfully.",
                extra={
                    "model_id": str(model.id),
                    "algorithm": algorithm,
                },
            )

            return model

        except Exception as exc:

            logger.exception(
                "Model training failed.",
                extra={
                    "dataset_id": str(dataset_id),
                    "algorithm": algorithm,
                },
            )

            self.repository.rollback()

            raise exc
        
    def train_auto(
        self,
        *,
        dataset_id: uuid.UUID,
        created_by: uuid.UUID,
        target_column: str,
        time_column: str,
    ):
        """
        Train all supported algorithms and select the best model.
        """

        runner = AutoMLRunner()

        training_group = uuid.uuid4()

        models = []

        for algorithm in runner.get_algorithms():

            model = self.train_model(
                dataset_id=dataset_id,
                created_by=created_by,
                algorithm=algorithm,
                target_column=target_column,
                time_column=time_column,
                training_group=training_group,
            )

            models.append(model)

        winner = min(
            models,
            key=lambda model: model.metrics["metrics"]["rmse"],
        )

        winner.is_best = True

        self.repository.commit()

        self.repository.refresh(winner)

        return {
            "training_group": training_group,
            "winner": winner,
            "models": models,
        }
        
    def predict(
        self,
        *,
        model_id: uuid.UUID,
        data: list[dict],
    ):
        """
        Run inference using a trained model.
        """

        model_record = self.repository.get_model_by_id(
            model_id,
        )

        if model_record is None:
            raise ValueError(
                "Model not found."
            )

        model, preprocessor = (
            ModelLoader.load(
                model_record.artifact_path,
            )
        )

        dataframe = pl.DataFrame(
            data,
        )

        algorithm = AlgorithmRegistry.get(
            model_record.algorithm,
        )

        return algorithm.predict(
            model,
            preprocessor,
            dataframe,
        )
    
    def explain(
        self,
        *,
        model_id: uuid.UUID,
        data: list[dict],
        sample_index: int = 0,
    ):
        """
        Explain a prediction using SHAP.
        """

        model_record = self.repository.get_model_by_id(
            model_id,
        )

        if model_record is None:
            raise ValueError(
                "Model not found."
            )

        model, preprocessor = (
            ModelLoader.load(
                model_record.artifact_path,
            )
        )

        dataframe = pl.DataFrame(
            data,
        )

        return self.explainer.explain(
            model=model,
            preprocessor=preprocessor,
            dataframe=dataframe,
            sample_index=sample_index,
        )