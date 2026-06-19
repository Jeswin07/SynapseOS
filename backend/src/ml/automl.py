from src.models.ml_enums import MLAlgorithm


class AutoMLRunner:
    """
    AutoML orchestrator.

    Responsible only for selecting which algorithms
    should be trained and compared.
    """

    def get_algorithms(
        self,
    ) -> list[str]:
        """
        Return all algorithms participating in AutoML.
        """

        return [
            MLAlgorithm.LINEAR_REGRESSION.value,
            MLAlgorithm.RANDOM_FOREST.value,
            MLAlgorithm.XGBOOST.value,
        ]