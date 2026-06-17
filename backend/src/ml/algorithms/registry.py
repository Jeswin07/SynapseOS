from src.ml.trainers.linear_regression import (
    LinearRegressionTrainer,
)
from src.ml.trainers.random_forest import (
    RandomForestTrainer,
)
from src.ml.trainers.xgboost import (
    XGBoostTrainer,
)


class AlgorithmRegistry:
    """
    Registry for all supported machine learning algorithms.
    """

    _algorithms = {
        "linear_regression": LinearRegressionTrainer(),
        "random_forest": RandomForestTrainer(),
        "xgboost": XGBoostTrainer(),
    }

    @classmethod
    def get(
        cls,
        algorithm: str,
    ):
        """
        Retrieve a registered algorithm.
        """

        try:
            return cls._algorithms[algorithm]

        except KeyError as exc:
            raise ValueError(
                f"Unsupported algorithm: {algorithm}"
            ) from exc

    @classmethod
    def get_all(
        cls,
    ) -> dict[str, object]:
        """
        Return all registered algorithms.
        """

        return cls._algorithms.copy()