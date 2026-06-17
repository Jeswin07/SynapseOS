import joblib


class ModelLoader:
    """
    Load trained ML models.
    """

    @staticmethod
    def load(
        artifact_path: str,
    ):

        artifact = joblib.load(
            artifact_path,
        )

        return (
            artifact["model"],
            artifact["preprocessor"],
        )