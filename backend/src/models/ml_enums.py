from enum import StrEnum


class MLAlgorithm(StrEnum):
    """
    Supported machine learning algorithms.
    """

    AUTO = "auto"

    LINEAR_REGRESSION = "linear_regression"

    RANDOM_FOREST = "random_forest"

    XGBOOST = "xgboost"

    PROPHET = "prophet"