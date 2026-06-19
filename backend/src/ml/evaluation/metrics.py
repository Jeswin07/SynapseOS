from dataclasses import dataclass

import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


@dataclass(slots=True)
class EvaluationResult:
    """
    Model evaluation metrics.
    """

    mse: float
    rmse: float
    mae: float
    r2: float

    training_time_seconds: float = 0.0
    rows: int = 0
    features: int = 0

class ModelEvaluator:
    """
    Evaluate regression models.
    """

    def evaluate(
        self,
        model,
        x_test,
        y_test,
    ) -> EvaluationResult:
        """
        Evaluate a trained model.

        Args:
            model: Trained sklearn model.
            x_test: Test features.
            y_test: Test targets.

        Returns:
            EvaluationResult.
        """

        predictions = model.predict(
            x_test,
        )

        mse = mean_squared_error(
            y_test,
            predictions,
        )

        rmse = np.sqrt(mse)

        mae = mean_absolute_error(
            y_test,
            predictions,
        )

        r2 = r2_score(
            y_test,
            predictions,
        )

        return EvaluationResult(
            mse=float(mse),
            rmse=float(rmse),
            mae=float(mae),
            r2=float(r2),
        )