import time
from pathlib import Path
from uuid import UUID

from src.ml.algorithms.registry import AlgorithmRegistry
from src.ml.evaluation.metrics import (
    EvaluationResult,
    ModelEvaluator,
)
from src.ml.preprocessing.loader import DatasetLoader


class MLTrainer:
    """
    Orchestrates the end-to-end machine learning workflow.
    """

    def __init__(self) -> None:

        self.loader = DatasetLoader()

        self.evaluator = ModelEvaluator()

    def train(
        self,
        *,
        storage_path: str,
        algorithm: str,
        target_column: str,
        time_column: str,
        model_id: UUID,
    ) -> tuple[str, EvaluationResult]:
        """
        Train and evaluate a machine learning model.
        """

        dataframe = self.loader.load_csv(
            storage_path,
        )

        start = time.perf_counter()

        algorithm_instance = AlgorithmRegistry.get(
            algorithm,
        )

        training_result = algorithm_instance.train(
            dataframe,
            target_column,
            time_column,
        )

        training_time = (
            time.perf_counter() - start
        )

        metrics = self.evaluator.evaluate(
            training_result.model,
            training_result.x_test,
            training_result.y_test,
        )

        metrics.training_time_seconds = round(
            training_time,
            3,
        )

        metrics.rows = dataframe.height

        metrics.features = len(
            dataframe.columns
        ) - 1

        Path("artifacts").mkdir(
            exist_ok=True,
        )

        artifact_path = (
            f"artifacts/{model_id}.joblib"
        )

        algorithm_instance.save(
            training_result.model,
            training_result.preprocessor,
            artifact_path,
        )

        return (
            artifact_path,
            metrics,
        )